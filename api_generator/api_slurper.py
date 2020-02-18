"""Converts snippets of the Clubhouse documentation into JSON objects."""
import json
import os
from typing import List, TypedDict

import pyperclip


class DocParameter(TypedDict, total=False):
    name: str
    type: str
    desc: str
    required: bool
    body_param: bool


class Documentation(TypedDict, total=False):
    title: str
    identifier: str
    response: str
    params: List[DocParameter]
    description: List[str]
    http_verb: str
    url_path: str
    category: str


def readAPIDoc(doc: str) -> Documentation:
    typeTransforms = {
        "String": "str",
        "UUID": "str",
        "Integer": "int",
        "Boolean": "bool",
        "Date": "datetime",
        "Enum (milestone)": "CategoryType",
        "Enum (done, in progress, to do)": "MilestoneWorkflowState",
        "Enum (bug, chore, feature)": "StoryType",
        "Enum (blocks, duplicates, relates to)": "StoryLinkVerb",
        "Enum (box, dropbox, google, onedrive, url)": "LinkedFileType",
        "Enum (done, started, unstarted)": "WorkflowStateTypes",
        "No Content": "void",
    }

    class Param:
        """Represents a clubhouse API parameter. Sortable by required first, then alphabetically"""

        def __init__(
            self, name: str, type: str, desc: str, required: bool, body_param: bool
        ):
            self.name: str = name
            self.type: str = type
            self.desc: str = desc
            self.required: bool = required
            self.body_param: bool = body_param

        def __lt__(self, other):
            if self.required != other.required:
                return self.required
            if self.name != other.name:
                return self.name < other.name
            if self.type != other.type:
                return self.type < other.type
            return self.desc < other.desc

    parameters: List[Param] = []

    def LoadParam(line: str, is_body: bool = True):
        try:
            half = line.split("\t", 1)
            quarter = half[0].split(" ", 1)
            name = quarter[0].strip()
            type = quarter[1].strip()
            desc = half[1].strip()
            required = desc.startswith("Required.")
            is_array = type.startswith("Array")
            nullable = False
            if is_array:
                idx = type.find("[")
                ridx = type.rfind("]")
                if idx != -1 and ridx != -1:
                    type = type[idx + 1 : ridx].strip()
            if type.endswith(" or null"):
                nullable = True
                type = type[:-8].strip()

            if type in typeTransforms:
                type = typeTransforms[type]
            # Otherwise assume it's a Clubhouse type

            if is_array:
                type = "List[{}]".format(type)
            # if not required:
            #    if type in optionalTypes:
            #        type = optionalTypes[type]
            #    else:
            #        type = 'Union[{}, Omit]'.format(type)
            if nullable:
                type = "Optional[{}]".format(type)
            parameters.append(Param(name, type, desc, required, is_body))

        except:
            pass

    # Define a reconfigurable state machine. The behavior changes at a given "stopword." Proccessing always begins by marking the first non-empty line as a title.
    title: str = ""
    description: List[str] = []
    endpoint: str = ""
    response: str = ""

    def feed_skip(line: str, stripped: str):
        return

    def feed_title(line: str, stripped: str):
        nonlocal title
        # Special case handling to determine if we accidentally got some response info from the previous function
        split = stripped.split("\t")
        if len(split) == 2:
            if (
                split[0].strip() == "Code" and split[1].strip() == "Description"
            ) or split[0].strip().isdigit():
                raise ValueError("Response info found where title should be")
        stripped = stripped.replace(".", "")
        title = stripped

    def feed_description(line: str, stripped: str):
        nonlocal description
        description.append(stripped)

    def feed_endpoint(line: str, stripped: str):
        nonlocal endpoint
        endpoint += stripped

    def feed_query_param(line: str, stripped: str):
        if line == "Name \tDescription":
            return
        LoadParam(line, False)

    def feed_body_param(line: str, stripped: str):
        if line == "Name \tDescription":
            return
        LoadParam(line, True)

    def feed_response(line: str, stripped: str):
        nonlocal response
        if line == "Code \tDescription":
            return
        s = line.split("\t", 1)
        if s[0].strip().startswith("2"):
            response = s[1].strip()
            is_list = False
            if response.startswith("[ ") and response.endswith(", … ]"):
                response = response[2:-5]
                is_list = True
            if response in typeTransforms:
                response = typeTransforms[response]
            if is_list:
                response = "List[{}]".format(response)

    # These describe lines that, if encountered, alter the state machine to a new processing configuration
    stopwords = {
        "    Definition": feed_endpoint,
        "    Example Request": feed_skip,
        "    Example Response": feed_skip,
        "URL Parameters": feed_query_param,
        "Body Parameters": feed_body_param,
        "Responses": feed_response,
    }

    action = feed_title
    getting_title = True

    data = doc
    for line in data.splitlines(False):
        stripped = line.strip()
        if stripped != "":
            if line in stopwords:
                action = stopwords[line]
                getting_title = False
            elif getting_title:
                # Special case handling for grabbing the title from the input
                action(line, stripped)
                action = feed_description
                getting_title = False
            else:
                action(line, stripped)

    # Validate our outputs
    if title == "":
        raise ValueError("Title could not be found")
    if endpoint == "" or endpoint.find(" ") == -1:
        raise ValueError("Endpoint definition was not found")
    if endpoint.lower().find("https://api.clubhouse.io/") == -1:
        raise ValueError("Endpoint does not refer to Clubhouse")
    if response == "":
        raise ValueError("Response could not be found")

    # Convert hyphens in URL parameters into underscores
    url_formatting = []
    for param in parameters:
        if not param.body_param:
            if "-" in param.name:
                new_name = param.name.replace("-", "_")
                endpoint = endpoint.replace(
                    "{" + param.name + "}", "{" + new_name + "}"
                )
                param.name = new_name
            url_formatting.append(param.name)

    # Convert the fully qualified URL into a path fragment for our internal use
    endpoint_data = endpoint.split(" ", 1)
    http_verb = endpoint_data[0].lower()
    url_path = endpoint_data[1]
    trimstr = "https://api.clubhouse.io/api/v3"
    if url_path.startswith(trimstr):
        url_path = url_path[len(trimstr) :]

    if http_verb not in ["get", "post", "put", "delete", "head", "options", "patch"]:
        raise ValueError("Unsupported HTTP verb: {}".format(http_verb))

    parameters.sort()

    # Convert the title from arbitrary case with spaces between the words into camelCase
    split_title = title.replace("(", "").replace(")", "").title().split(" ")
    split_title[0] = split_title[0].lower()
    title_ident = "".join(split_title)

    return Documentation(
        title=title,
        identifier=title_ident,
        response=response,
        params=[DocParameter(**p.__dict__) for p in parameters],
        description=description,
        http_verb=http_verb,
        url_path=url_path,
        category="N/A",
    )


if __name__ == "__main__":
    print(
        """This is the API slurper. It is designed to accept snippets of the Clubhouse API documentation that have been copied from the website to the clipboard.

    You will be prompted for a category. If provided upon pressing enter, the current category will be set to what you provided. If an empty line is provided, the current clipboard contents will be treated as a clubhouse API snippet and stored with the current category in ./api_description

    A category MUST be provided prior to any API processing. To exit, submit the category \\q
    """
    )

    no_category = "<Specify Category>"
    category = no_category
    while True:
        new_cat = input(category + ": ")
        if new_cat == "\\q":
            break
        if new_cat != "":
            if not new_cat.replace(" ", "").replace("-", "").isalnum():
                print("Err: Invalid category", new_cat)
            else:
                category = new_cat
        elif category == no_category:
            print("Err: Must specify a category")
        else:
            try:
                doc = readAPIDoc(pyperclip.paste())
                doc["category"] = category
                try:
                    os.mkdir("api_def")
                except FileExistsError:
                    pass
                do_write = True
                fname = "api_def/{}.json".format(doc["identifier"])
                try:
                    with open(fname, "r") as f:
                        other = json.load(f)
                        do_write = False
                        if doc != other:
                            replace = input(
                                '"{}" already exists under category "{}". Replace? (Y/n):'.format(
                                    doc["title"], other["category"]
                                )
                            )
                            if replace.lower() == "y" or replace == "":
                                do_write = True
                            else:
                                print("Err: Unrecognized option", replace)
                        else:
                            print(
                                '"{}" already exists and is identical to the provided information. Skipping...'.format(
                                    doc["title"]
                                )
                            )
                except json.JSONDecodeError:
                    print(
                        '"{}" already exists but appears to be corrupted, so it will be overwritten.'.format(
                            doc["title"]
                        )
                    )
                except FileNotFoundError:
                    pass
                if do_write:
                    with open(fname, "w") as f:
                        json.dump(doc, f, indent=4)
                    print('Wrote function "{}" to {}'.format(doc["title"], fname))
            except Exception as e:
                print("Err: Failed to read API info:", e)
                raise e
