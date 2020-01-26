import os
import json
import requests
import datetime
from typing import List, Union

from .type2 import (
    Category,
    Milestone,
    EntityTemplate
)
from .type import (
    CategoryType,
    CategoryCreate,
    CategoryUpdate,
    EntityTemplateCreate,
    EntityTemplateUpdate,
    StoryContentsCreate,
)

class notProvided:
    pass
NotProvided = notProvided()



def PrepareLocals(data: dict) -> dict:
    keys = []
    for key in data:
        if data[key] is NotProvided or key == 'self':
            keys.append(key)
    for key in keys:
        del data[key]
    return data

class ClubhouseClient:
    Int = Union[int, None, NotProvided]
    Str = Union[str, None, NotProvided]
    Date = Union[datetime.datetime, None, NotProvided]

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
        return [Category(j) for j in self.get("categories").json()]

    def createCategory(self, category: CategoryCreate) -> Category:
        """Create Category allows you to create a new Category in Clubhouse."""
        return Category(self.post("categories", category).json())

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
