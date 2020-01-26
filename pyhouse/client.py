import os
import json
import requests
import datetime
from typing import List, Union, TypedDict

from .type2 import *
from .type import (
    CategoryType,
    CategoryCreate,
    CategoryUpdate,
    EntityTemplateCreate,
    EntityTemplateUpdate,
    StoryContentsCreate,
)

"""
Note to future readers: The API for this library opts to define an additional None-like type, called Omit. 
This is due to the fact that Clubhouse makes a meaningful distinction between parameters which are omitted 
and parameters which are passed as null. This does cause problems with type validators, however. Many
functions herein follow a pattern of defining parameters of some type and defaulting to the value `Omit`.
This error is intentional, however it does lead to some questionable looking function signatures due to
the liberal use of "# type: ignore" comments on each parameter line.

We have explored alternatives, and we have deemed this option to be the least harmful overall. We 
experimented with using union types and type aliases, however those expand to a ton of noise in all of the
autocompletion engines we tested, which somewhat limited the utility of having named parameters in the first
place.
"""

class omitType:
    pass
Omit = omitType()


def PrepareLocals(data: dict) -> dict:
    keys = []
    for key in data:
        if data[key] is Omit or key == 'self':
            keys.append(key)
    for key in keys:
        del data[key]
    return data

class ClubhouseClient:
    Int = Union[int, None, Omit]
    Str = Union[str, None, Omit]
    Bool = Union[bool, None, Omit]
    Date = Union[datetime.datetime, None, Omit]

    def __init__(
        self,
        token: str,
        baseURL: str = "https://api.clubhouse.io",
        version: str = "v3",
        debug: bool = False,
    ) -> None:
        self.token = token
        self.baseURL = baseURL
        self.version = version
        self.debug = debug
        self.apiURL = baseURL.rstrip("/") + "/api/" + version

    ############
    # Requests #
    ############
    def get(self, endpoint: str, params: dict = None) -> requests.Response:
        print(PrepareLocals(locals()))
        if params is None:
            params = {}
        params["token"] = self.token
        headers = {"Content-Type": "application/json"}
        if self.debug:
            print(
                "curl -X GET -H \"Content-Type: application/json\" '{}/{}?{}'".format(
                    self.apiURL,
                    endpoint.lstrip("/"),
                    "&".join("{}={}".format(k, v) for k, v in params.items()),
                )
            )
        r = requests.get(
            "{}/{}".format(self.apiURL, endpoint.lstrip("/")),
            params=params,
            headers=headers,
        )
        r.raise_for_status()
        return r

    def put(self, endpoint: str, data: dict = None) -> requests.Response:
        if data is None:
            data = {}
        headers = {"Content-Type": "application/json"}
        if self.debug:
            print(
                "curl -X PUT -H \"Content-Type: application/json\" '{}/{}?token={}' --data '{}'".format(
                    self.apiURL, endpoint.lstrip("/"), self.token, json.dumps(data)
                )
            )
        r = requests.put(
            "{}/{}?token={}".format(self.apiURL, endpoint.lstrip("/"), self.token),
            data=json.dumps(data),
            headers=headers,
        )
        r.raise_for_status()
        return r

    def post(self, endpoint: str, data: dict = None) -> requests.Response:
        if data is None:
            data = {}
        headers = {"Content-Type": "application/json"}
        if self.debug:
            print(
                "curl -X POST -H \"Content-Type: application/json\" '{}/{}?token={}' --data '{}'".format(
                    self.apiURL, endpoint.lstrip("/"), self.token, json.dumps(data)
                )
            )
        r = requests.post(
            "{}/{}?token={}".format(self.apiURL, endpoint.lstrip("/"), self.token),
            data=json.dumps(data),
            headers=headers,
        )
        r.raise_for_status()
        return r

    def delete(self, endpoint: str) -> requests.Response:
        headers = {"Content-Type": "application/json"}
        if self.debug:
            print(
                "curl -X DELETE -H \"Content-Type: application/json\" '{}/{}?token={}'".format(
                    self.apiURL, endpoint.lstrip("/"), self.token
                )
            )
        r = requests.delete(
            "{}/{}?token={}".format(self.apiURL, endpoint.lstrip("/"), self.token),
            headers=headers,
        )
        r.raise_for_status()
        return r

    ##############
    # Categories #
    ##############
    def listCategories(self) -> List[Category]:
        """List Categories returns a list of all Categories and their attributes."""
        return self.get("categories").json()

    def createCategory(self, 
        name: str, # Test
        type: CategoryType,
        color: Str = Omit,
        external_id: Str = Omit
    ) -> Category:
        """
        Create Category allows you to create a new Category in Clubhouse.
        
        param name: The name of the new Category.
        param type: The type of entity this Category is associated with; currently Milestone is the only type of Category.
        param color: The hex color to be displayed with the Category (for example, “#ff0000”).
        param external_id: This field can be set to another unique ID. In the case that the Category has been imported from another tool, the ID in the other tool can be indicated here.
        """
        return self.post("categories", PrepareLocals(locals())).json()

    def getCategory(self, category_public_id: int) -> Category:
        """Get Category returns information about the selected Category."""
        result: Category = self.get("categories/" + str(category_public_id)).json()
        return result

    def updateCategory(
        self, category_public_id: int, category: CategoryUpdate
    ) -> Category:
        """Update Category allows you to replace a Category name with another name.
        If you try to name a Category something that already exists, you will receive a 422 response."""
        return Category(
            self.put("categories/" + str(category_public_id), category).json()
        )

    def deleteCategory(self, category_public_id: int) -> requests.Response:
        """Delete Category can be used to delete any Category."""
        return self.delete("categories/" + str(category_public_id))

    def listCategoryMilestones(self, category_public_id: int) -> List[Milestone]:
        """List Category Milestones returns a list of all Milestones with the Category."""
        return [
            Milestone(j)
            for j in self.get(
                "categories/" + str(category_public_id) + "/milestones"
            ).json()
        ]

    ####################
    # Entity-Templates #
    ####################
    def listEntityTemplates(self) -> List[EntityTemplate]:
        """List all the entity templates for an organization."""
        return self.get("entity-templates").json()

    def createEntityTemplate(
        self, entityTemplate: EntityTemplateCreate
    ) -> EntityTemplate:
        """Create a new entity template for your organization."""
        return EntityTemplate(self.post("entity-templates", entityTemplate).json())

    def disableStoryTemplates(self) -> requests.Response:
        """Disables the Story Template feature for the given Organization."""
        return self.put("entity-templates/disable")

    def enableStoryTemplates(self) -> requests.Response:
        """Enables the Story Template feature for the given Organization."""
        return self.put("entity-templates/enable")

    def getEntityTemplate(self, entity_template_public_id: str) -> EntityTemplate:
        """Get Entity Template returns information about a given entity template."""
        return EntityTemplate(
            self.get("entity-templates/" + entity_template_public_id).json()
        )

    def updateEntityTemplate(
        self, entity_template_public_id: str, entityTemplate: EntityTemplateUpdate
    ) -> EntityTemplate:
        """Update an entity template’s name or its contents."""
        return self.put(
                "entity-templates/" + entity_template_public_id, entityTemplate
            ).json()

    def deleteEntityTemplate(self, entity_template_public_id: str) -> requests.Response:
        """Delete an entity template."""
        return self.delete("entity-templates/" + entity_template_public_id)


if __name__ == "__main__":
    key = os.environ.get("CLUBHOUSE_API_TOKEN")
    if key is not None and key != '':
        client = ClubhouseClient(key, debug=True)

        # Categories
        # print([x for x in client.listCategories()])
        # print(
        #     client.createCategory(CategoryCreate(name="foof", type=CategoryType.MILESTONE))
        # )
        # print(client.getCategory(36))
        # print(client.deleteCategory(33))
        # print(client.updateCategory(38, CategoryUpdate(color="#0000ff")))
        # print([x for x in client.listCategoryMilestones(36)])

        # Entity-Templates
        # print(client.enableStoryTemplates())
        # print([x for x in client.listEntityTemplates()])
        # print(
        #     client.createEntityTemplate(
        #         EntityTemplateCreate(
        #             name="deez", story_contents=StoryContentsCreate(description="test")
        #         )
        #     )
        # )
        # print(client.getEntityTemplate("5e05cf80-bb9f-4acd-95e8-18a695d59bca"))
        # print(
        #     client.updateEntityTemplate(
        #         "5e05d5d6-ed99-41e0-a0c3-a8f50490034d",
        #         EntityTemplateUpdate(
        #             name="meese", story_contents=StoryContentsCreate(description="lul")
        #         ),
        #     )
        # )
        # print(client.deleteEntityTemplate("5e05cf80-bb9f-4acd-95e8-18a695d59bca"))
        # print(client.disableStoryTemplates())
