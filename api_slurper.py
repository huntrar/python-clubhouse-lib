import pyperclip
from typing import List, Union

requiredTypes = {
    'String': 'str',
    'UUID': 'str',
    'Integer': 'int',
    'Boolean': 'bool',
    'Date': 'datetime',
    'Enum (milestone)': 'CategoryType',
    'Enum (done, in progress, to do)': 'MilestoneWorkflowState',
    'Enum (bug, chore, feature)': 'StoryType',
    'Enum (blocks, duplicates, relates to)': 'StoryLinkVerb',
    'Enum (box, dropbox, google, onedrive, url)': 'LinkedFileType'
}

# Vestigial
optionalTypes = {
    'str': 'Str',
    'int': 'Int',
    'datetime': 'Date',
    'bool': 'Bool'
}


class Param:
    """Represents a clubhouse API parameter. Sortable by required first, then alphabetically"""
    def __init__(self, name: str, type: str, desc: str, required: bool, body_param: bool):
        self.name:str = name
        self.type:str = type
        self.desc:str = desc
        self.required:bool = required
        self.body_param:bool = body_param
    def __lt__(self, other):
        if self.required != other.required:
            return self.required
        if self.name != other.name:
            return self.name < other.name
        if self.type != other.type:
            return self.type < other.type
        return self.desc < other.desc

parameters : List[Param] = []

def LoadParam(line:str, is_body:bool=True):
    try:
        half = line.split('\t', 1)
        quarter = half[0].split(' ', 1)
        name = quarter[0].strip()
        type = quarter[1].strip()
        desc = half[1].strip()
        required = desc.startswith("Required.")
        is_array = type.startswith("Array")
        nullable = False
        if is_array:
            idx = type.find('[')
            ridx = type.rfind(']')
            if idx != -1 and ridx != -1:
                type = type[idx + 1:ridx].strip()
        if type.endswith(' or null'):
            nullable = True
            type = type[:-8].strip()
        
        if type in requiredTypes:
            type = requiredTypes[type]
        # Otherwise assume it's a Clubhouse type

        if is_array:
            type = 'List[{}]'.format(type)
        #if not required:
        #    if type in optionalTypes:
        #        type = optionalTypes[type]
        #    else:
        #        type = 'Union[{}, Omit]'.format(type)
        if nullable:
            type = 'Optional[{}]'.format(type)
        parameters.append(Param(name, type, desc, required, is_body))

    except:
        pass

# Define a reconfigurable state machine. The behavior changes at a given "stopword." Proccessing always begins by marking the first non-empty line as a title.
title:str = ''
description:List[str] = []
endpoint:str = ''
response:str = ''

def feed_skip(line:str, stripped:str):
    return

def feed_title(line:str, stripped:str):
    global title
    title = stripped

def feed_description(line:str, stripped:str):
    global description
    description.append(stripped)

def feed_endpoint(line:str, stripped:str):
    global endpoint
    endpoint += stripped

def feed_query_param(line:str, stripped:str):
    if line == 'Name \tDescription':
        return
    LoadParam(line, False)

def feed_body_param(line:str, stripped:str):
    if line == 'Name \tDescription':
        return
    LoadParam(line, True)

def feed_response(line:str, stripped:str):
    global response
    if line == 'Code \tDescription':
        return
    s = line.split('\t',1)
    if s[0].strip().startswith('2'):
        response = s[1].strip()
        if response.startswith('[ ') and response.endswith(', … ]'):
            response = 'List[{}]'.format(response[2:-5])

# These describe lines that, if encountered, alter the state machine to a new processing configuration
stopwords = {
    '    Definition': feed_endpoint, 
    '    Example Request': feed_skip, 
    '    Example Response': feed_skip, 
    'URL Parameters': feed_query_param, 
    'Body Parameters': feed_body_param, 
    'Responses': feed_response
}


action = feed_title
getting_title = True

data = str(pyperclip.paste())
for line in data.splitlines(False):
    stripped = line.strip()
    if stripped != '':
        if getting_title:
            # Special case handling for grabbing the title from the input
            action(line, stripped)
            action = feed_description
            getting_title = False
        else:
            if line in stopwords:
                action = stopwords[line]
            else:
                action(line, stripped)

# Convert hyphens in URL parameters into underscores
url_formatting = []
for param in parameters:
    if not param.body_param:
        if  '-' in param.name:
            new_name = param.name.replace('-', '_')
            endpoint = endpoint.replace('{' + param.name + '}', '{' + new_name + '}')
            param.name = new_name
        url_formatting.append(param.name)

# Convert the fully qualified URL into a path fragment for our internal use
endpoint_data = endpoint.split(' ', 1)
http_verb = endpoint_data[0].lower()
url_path = endpoint_data[1]
trimstr = 'https://api.clubhouse.io/api/v3'
if url_path.startswith(trimstr):
    url_path = url_path[len(trimstr):]

# Build the string used to fetch data from Clubhouse
request_string = 'self.{}("{}"'.format(http_verb, url_path)
if len(url_formatting) > 0:
    request_string += '.format(' + ','.join([f + '=' + f for f in url_formatting]) + ')'
if len(parameters) - len(url_formatting) > 0:
    request_string += ', PrepareLocals(locals())'
request_string += ').json()'


parameters.sort()

# Convert the title from arbitrary case with spaces between the words into camelCase
split_title = title.title().split(' ')
split_title[0] = split_title[0].lower()
title = ''.join(split_title)

# Build the Python parameter list and documentation parameter list
py_parameter_list = []
doc_parameter_list = []
for p in parameters:
    np = ''
    if not p.required:
        np = ' = Omit'
    py_parameter_list.append('{}: {}{}'.format(p.name, p.type, np))
    doc_parameter_list.append('param {}: {}'.format(p.name, p.desc))

# Generate the function and throw it on the clipboard
result = """
    def {title}(self,
        {py_params} # type: ignore
    ) -> {result}:
        \"\"\"
        {description}

        {doc_params}
        \"\"\"
        return {request_string}
""".format(
    title=title, 
    py_params=', # type: ignore\n        '.join(py_parameter_list),
    result=response,
    description='\n        '.join(description),
    doc_params='\n        '.join(doc_parameter_list),
    request_string=request_string
)

pyperclip.copy(result)