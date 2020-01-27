import os
import json
import requests
import datetime
from typing import List, Union, TypedDict

from .type2 import *

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

    def delete(self, endpoint: str, data: dict = None) -> requests.Response:
        headers = {"Content-Type": "application/json"}
        if self.debug:
            print(
                "curl -X DELETE -H \"Content-Type: application/json\" '{}/{}?token={}'".format(
                    self.apiURL, endpoint.lstrip("/"), self.token
                )
            )
        pass_data = data
        if pass_data != None:
            pass_data = json.dumps(data),
        r = requests.delete(
            "{}/{}?token={}".format(self.apiURL, endpoint.lstrip("/"), self.token),
            data=pass_data,
            headers=headers,
        )
        r.raise_for_status()
        return r


    ##############
    # Categories #
    ##############

    def createCategory(self,
        name: str,
        type: CategoryType,
        color: str = Omit, # type: ignore
        external_id: str = Omit # type: ignore
    ) -> Category:
        """
        Create Category allows you to create a new Category in Clubhouse.
        
        param name: Required. The name of the new Category.
        param type: Required. The type of entity this Category is associated with; currently Milestone is the only type of Category.
        param color: The hex color to be displayed with the Category (for example, “#ff0000”).
        param external_id: This field can be set to another unique ID. In the case that the Category has been imported from another tool, the ID in the other tool can be indicated here.
        """
        return self.post("/categories", PrepareLocals({
            'name': name,
            'type': type,
            'color': color,
            'external_id': external_id
        })).json()
        

    def deleteCategory(self, category_public_id: int):
        """
        Delete Category can be used to delete any Category.
        
        param category_public_id: Required. The unique ID of the Category.
        """
        self.delete("/categories/{category_public_id}".format(category_public_id=category_public_id))
        

    def getCategory(self, category_public_id: int) -> Category:
        """
        Get Category returns information about the selected Category.
        
        param category_public_id: Required. The unique ID of the Category.
        """
        return self.get("/categories/{category_public_id}".format(category_public_id=category_public_id)).json()
        

    def listCategories(self) -> List[Category]:
        """List Categories returns a list of all Categories and their attributes."""
        return self.get("/categories").json()
        

    def listCategoryMilestones(self, category_public_id: int) -> List[Milestone]:
        """
        List Category Milestones returns a list of all Milestones with the Category.
        
        param category_public_id: Required. The unique ID of the Category.
        """
        return self.get("/categories/{category_public_id}/milestones".format(category_public_id=category_public_id)).json()
        

    def updateCategory(self,
        category_public_id: int,
        archived: bool = Omit, # type: ignore
        color: Optional[str] = Omit, # type: ignore
        name: str = Omit # type: ignore
    ) -> Category:
        """
        Update Category allows you to replace a Category name with another name. If you try to name a Category something that already exists, you will receive a 422 response.
        
        param category_public_id: Required. The unique ID of the Category you wish to update.
        param archived: A true/false boolean indicating if the Category has been archived.
        param color: The hex color to be displayed with the Category (for example, “#ff0000”).
        param name: The new name of the Category.
        """
        return self.put("/categories/{category_public_id}".format(category_public_id=category_public_id), PrepareLocals({
            'archived': archived,
            'color': color,
            'name': name
        })).json()
        

    ####################
    # Entity-Templates #
    ####################

    def createEntityTemplate(self,
        name: str,
        story_contents: CreateStoryContents,
        author_id: str = Omit # type: ignore
    ) -> EntityTemplate:
        """
        Create a new entity template for your organization.
        
        param name: Required. The name of the new entity template
        param story_contents: Required. A map of story attributes this template populates.
        param author_id: The id of the user creating this template.
        """
        return self.post("/entity-templates", PrepareLocals({
            'name': name,
            'story_contents': story_contents,
            'author_id': author_id
        })).json()
        

    def deleteEntityTemplate(self, entity_template_public_id: str):
        """param entity_template_public_id: Required. The unique ID of the entity template."""
        self.delete("/entity-templates/{entity_template_public_id}".format(entity_template_public_id=entity_template_public_id))
        

    def disableStoryTemplates(self):
        """Disables the Story Template feature for the given Organization."""
        self.put("/entity-templates/disable")
        

    def enableStoryTemplates(self):
        """Enables the Story Template feature for the given Organization."""
        self.put("/entity-templates/enable")
        

    def getEntityTemplate(self, entity_template_public_id: str) -> EntityTemplate:
        """
        Get Entity Template returns information about a given entity template.
        
        param entity_template_public_id: Required. The unique ID of the entity template.
        """
        return self.get("/entity-templates/{entity_template_public_id}".format(entity_template_public_id=entity_template_public_id)).json()
        

    def listEntityTemplates(self) -> List[EntityTemplate]:
        """List all the entity templates for an organization."""
        return self.get("/entity-templates").json()
        

    def updateEntityTemplate(self,
        entity_template_public_id: str,
        name: str = Omit, # type: ignore
        story_contents: CreateStoryContents = Omit # type: ignore
    ) -> EntityTemplate:
        """
        Update an entity template’s name or its contents.
        
        param entity_template_public_id: Required. The unique ID of the template to be updated.
        param name: The updated template name.
        param story_contents: A map of story attributes this template populates.
        """
        return self.put("/entity-templates/{entity_template_public_id}".format(entity_template_public_id=entity_template_public_id), PrepareLocals({
            'name': name,
            'story_contents': story_contents
        })).json()
        

    #################
    # Epic-Workflow #
    #################

    def getEpicWorkflow(self) -> EpicWorkflow:
        """Get Epic Workflow returns the Epic Workflow for the organization."""
        return self.get("/epic-workflow").json()
        

    #########
    # Epics #
    #########

    def createEpic(self,
        name: str,
        completed_at_override: datetime = Omit, # type: ignore
        created_at: datetime = Omit, # type: ignore
        deadline: Optional[datetime] = Omit, # type: ignore
        description: str = Omit, # type: ignore
        epic_state_id: int = Omit, # type: ignore
        external_id: str = Omit, # type: ignore
        follower_ids: List[str] = Omit, # type: ignore
        labels: List[CreateLabelParams] = Omit, # type: ignore
        milestone_id: Optional[int] = Omit, # type: ignore
        owner_ids: List[str] = Omit, # type: ignore
        requested_by_id: str = Omit, # type: ignore
        started_at_override: datetime = Omit, # type: ignore
        state: MilestoneWorkflowState = Omit, # type: ignore
        updated_at: datetime = Omit # type: ignore
    ) -> Epic:
        """
        Create Epic allows you to create a new Epic in Clubhouse.
        
        param name: Required. The Epic’s name.
        param completed_at_override: A manual override for the time/date the Epic was completed.
        param created_at: Defaults to the time/date it is created but can be set to reflect another date.
        param deadline: The Epic’s deadline.
        param description: The Epic’s description.
        param epic_state_id: The ID of the Epic State.
        param external_id: This field can be set to another unique ID. In the case that the Epic has been imported from another tool, the ID in the other tool can be indicated here.
        param follower_ids: An array of UUIDs for any Members you want to add as Followers on this new Epic.
        param labels: An array of Labels attached to the Epic.
        param milestone_id: The ID of the Milestone this Epic is related to.
        param owner_ids: An array of UUIDs for any members you want to add as Owners on this new Epic.
        param requested_by_id: The ID of the member that requested the epic.
        param started_at_override: A manual override for the time/date the Epic was started.
        param state: Deprecated The Epic’s state (to do, in progress, or done); will be ignored when epic_state_id is set.
        param updated_at: Defaults to the time/date it is created but can be set to reflect another date.
        """
        return self.post("/epics", PrepareLocals({
            'name': name,
            'completed_at_override': completed_at_override,
            'created_at': created_at,
            'deadline': deadline,
            'description': description,
            'epic_state_id': epic_state_id,
            'external_id': external_id,
            'follower_ids': follower_ids,
            'labels': labels,
            'milestone_id': milestone_id,
            'owner_ids': owner_ids,
            'requested_by_id': requested_by_id,
            'started_at_override': started_at_override,
            'state': state,
            'updated_at': updated_at
        })).json()
        

    def createEpicComment(self,
        epic_public_id: int,
        text: str,
        author_id: str = Omit, # type: ignore
        created_at: datetime = Omit, # type: ignore
        external_id: str = Omit, # type: ignore
        updated_at: datetime = Omit # type: ignore
    ) -> ThreadedComment:
        """
        This endpoint allows you to create a threaded Comment on an Epic.
        
        param epic_public_id: Required. The ID of the associated Epic.
        param text: Required. The comment text.
        param author_id: The Member ID of the Comment’s author. Defaults to the user identified by the API token.
        param created_at: Defaults to the time/date the comment is created, but can be set to reflect another date.
        param external_id: This field can be set to another unique ID. In the case that the comment has been imported from another tool, the ID in the other tool can be indicated here.
        param updated_at: Defaults to the time/date the comment is last updated, but can be set to reflect another date.
        """
        return self.post("/epics/{epic_public_id}/comments".format(epic_public_id=epic_public_id), PrepareLocals({
            'text': text,
            'author_id': author_id,
            'created_at': created_at,
            'external_id': external_id,
            'updated_at': updated_at
        })).json()
        

    def createEpicCommentComment(self,
        comment_public_id: int,
        epic_public_id: int,
        text: str,
        author_id: str = Omit, # type: ignore
        created_at: datetime = Omit, # type: ignore
        external_id: str = Omit, # type: ignore
        updated_at: datetime = Omit # type: ignore
    ) -> ThreadedComment:
        """
        This endpoint allows you to create a nested Comment reply to an existing Epic Comment.
        
        param comment_public_id: Required. The ID of the parent Epic Comment.
        param epic_public_id: Required. The ID of the associated Epic.
        param text: Required. The comment text.
        param author_id: The Member ID of the Comment’s author. Defaults to the user identified by the API token.
        param created_at: Defaults to the time/date the comment is created, but can be set to reflect another date.
        param external_id: This field can be set to another unique ID. In the case that the comment has been imported from another tool, the ID in the other tool can be indicated here.
        param updated_at: Defaults to the time/date the comment is last updated, but can be set to reflect another date.
        """
        return self.post("/epics/{epic_public_id}/comments/{comment_public_id}".format(comment_public_id=comment_public_id,epic_public_id=epic_public_id), PrepareLocals({
            'text': text,
            'author_id': author_id,
            'created_at': created_at,
            'external_id': external_id,
            'updated_at': updated_at
        })).json()
        

    def deleteEpic(self, epic_public_id: int):
        """
        Delete Epic can be used to delete the Epic. The only required parameter is Epic ID.
        
        param epic_public_id: Required. The unique ID of the Epic.
        """
        self.delete("/epics/{epic_public_id}".format(epic_public_id=epic_public_id))
        

    def deleteEpicComment(self, comment_public_id: int, epic_public_id: int):
        """
        This endpoint allows you to delete a Comment from an Epic.
        
        param comment_public_id: Required. The ID of the Comment.
        param epic_public_id: Required. The ID of the associated Epic.
        """
        self.delete("/epics/{epic_public_id}/comments/{comment_public_id}".format(comment_public_id=comment_public_id,epic_public_id=epic_public_id))
        

    def getEpic(self, epic_public_id: int) -> Epic:
        """
        Get Epic returns information about the selected Epic.
        
        param epic_public_id: Required. The unique ID of the Epic.
        """
        return self.get("/epics/{epic_public_id}".format(epic_public_id=epic_public_id)).json()
        

    def getEpicComment(self, comment_public_id: int, epic_public_id: int) -> ThreadedComment:
        """
        This endpoint returns information about the selected Epic Comment.
        
        param comment_public_id: Required. The ID of the Comment.
        param epic_public_id: Required. The ID of the associated Epic.
        """
        return self.get("/epics/{epic_public_id}/comments/{comment_public_id}".format(comment_public_id=comment_public_id,epic_public_id=epic_public_id)).json()
        

    def listEpicComments(self, epic_public_id: int) -> List[ThreadedComment]:
        """
        Get a list of all Comments on an Epic.
        
        param epic_public_id: Required. The unique ID of the Epic.
        """
        return self.get("/epics/{epic_public_id}/comments".format(epic_public_id=epic_public_id)).json()
        

    def listEpics(self) -> List[EpicSlim]:
        """List Epics returns a list of all Epics and their attributes."""
        return self.get("/epics").json()
        

    def updateEpic(self,
        epic_public_id: int,
        after_id: int = Omit, # type: ignore
        archived: bool = Omit, # type: ignore
        before_id: int = Omit, # type: ignore
        completed_at_override: Optional[datetime] = Omit, # type: ignore
        deadline: Optional[datetime] = Omit, # type: ignore
        description: str = Omit, # type: ignore
        epic_state_id: int = Omit, # type: ignore
        follower_ids: List[str] = Omit, # type: ignore
        labels: List[CreateLabelParams] = Omit, # type: ignore
        milestone_id: Optional[int] = Omit, # type: ignore
        name: str = Omit, # type: ignore
        owner_ids: List[str] = Omit, # type: ignore
        requested_by_id: str = Omit, # type: ignore
        started_at_override: Optional[datetime] = Omit, # type: ignore
        state: MilestoneWorkflowState = Omit # type: ignore
    ) -> Epic:
        """
        Update Epic can be used to update numerous fields in the Epic. The only required parameter is Epic ID, which can be found in the Clubhouse UI.
        
        param epic_public_id: Required. The unique ID of the Epic.
        param after_id: The ID of the Epic we want to move this Epic after.
        param archived: A true/false boolean indicating whether the Epic is in archived state.
        param before_id: The ID of the Epic we want to move this Epic before.
        param completed_at_override: A manual override for the time/date the Epic was completed.
        param deadline: The Epic’s deadline.
        param description: The Epic’s description.
        param epic_state_id: The ID of the Epic State.
        param follower_ids: An array of UUIDs for any Members you want to add as Followers on this Epic.
        param labels: An array of Labels attached to the Epic.
        param milestone_id: The ID of the Milestone this Epic is related to.
        param name: The Epic’s name.
        param owner_ids: An array of UUIDs for any members you want to add as Owners on this Epic.
        param requested_by_id: The ID of the member that requested the epic.
        param started_at_override: A manual override for the time/date the Epic was started.
        param state: Deprecated The Epic’s state (to do, in progress, or done); will be ignored when epic_state_id is set.
        """
        return self.put("/epics/{epic_public_id}".format(epic_public_id=epic_public_id), PrepareLocals({
            'after_id': after_id,
            'archived': archived,
            'before_id': before_id,
            'completed_at_override': completed_at_override,
            'deadline': deadline,
            'description': description,
            'epic_state_id': epic_state_id,
            'follower_ids': follower_ids,
            'labels': labels,
            'milestone_id': milestone_id,
            'name': name,
            'owner_ids': owner_ids,
            'requested_by_id': requested_by_id,
            'started_at_override': started_at_override,
            'state': state
        })).json()
        

    def updateEpicComment(self, comment_public_id: int, epic_public_id: int, text: str) -> ThreadedComment:
        """
        This endpoint allows you to update a threaded Comment on an Epic.
        
        param comment_public_id: Required. The ID of the Comment.
        param epic_public_id: Required. The ID of the associated Epic.
        param text: Required. The updated comment text.
        """
        return self.put("/epics/{epic_public_id}/comments/{comment_public_id}".format(comment_public_id=comment_public_id,epic_public_id=epic_public_id), PrepareLocals({
            'text': text
        })).json()
        

    #########
    # Files #
    #########

    def deleteFile(self, file_public_id: int):
        """
        Delete File can be used to delete any previously attached File.
        
        param file_public_id: Required. The File’s unique ID.
        """
        self.delete("/files/{file_public_id}".format(file_public_id=file_public_id))
        

    def getFile(self, file_public_id: int) -> File:
        """
        Get File returns information about the selected File.
        
        param file_public_id: Required. The File’s unique ID.
        """
        return self.get("/files/{file_public_id}".format(file_public_id=file_public_id)).json()
        

    def listFiles(self) -> List[File]:
        """List Files returns a list of all Files and related attributes in your Clubhouse."""
        return self.get("/files").json()
        

    def updateFile(self,
        file_public_id: int,
        created_at: datetime = Omit, # type: ignore
        description: str = Omit, # type: ignore
        external_id: str = Omit, # type: ignore
        name: str = Omit, # type: ignore
        updated_at: datetime = Omit, # type: ignore
        uploader_id: str = Omit # type: ignore
    ) -> File:
        """
        Update File can used to update the properties of a file uploaded to Clubhouse.
        
        param file_public_id: Required. The unique ID assigned to the file in Clubhouse.
        param created_at: The time/date that the file was uploaded.
        param description: The description of the file.
        param external_id: An additional ID that you may wish to assign to the file.
        param name: The name of the file.
        param updated_at: The time/date that the file was last updated.
        param uploader_id: The unique ID assigned to the Member who uploaded the file to Clubhouse.
        """
        return self.put("/files/{file_public_id}".format(file_public_id=file_public_id), PrepareLocals({
            'created_at': created_at,
            'description': description,
            'external_id': external_id,
            'name': name,
            'updated_at': updated_at,
            'uploader_id': uploader_id
        })).json()
        

    def uploadFiles(self) -> List[File]:
        """Upload one or more Files, which can then be associated to a Story Description, Story Comment, or Epic Comment."""
        return self.post("/files").json()
        

    ##########
    # Groups #
    ##########

    def createGroup(self,
        mention_name: str,
        name: str,
        description: str = Omit, # type: ignore
        display_icon_id: str = Omit, # type: ignore
        member_ids: List[str] = Omit # type: ignore
    ) -> Group:
        """
        param mention_name: Required. The mention name of this Group.
        param name: Required. The name of this Group.
        param description: The description of the Group.
        param display_icon_id: The Icon id for the avatar of this Group.
        param member_ids: The Member ids to add to this Group.
        """
        return self.post("/groups", PrepareLocals({
            'mention_name': mention_name,
            'name': name,
            'description': description,
            'display_icon_id': display_icon_id,
            'member_ids': member_ids
        })).json()
        

    def getGroup(self, group_public_id: str) -> Group:
        """param group_public_id: Required. The unique ID of the Group."""
        return self.get("/groups/{group_public_id}".format(group_public_id=group_public_id)).json()
        

    def listGroups(self) -> List[Group]:
        return self.get("/groups").json()
        

    def updateGroup(self,
        group_public_id: str,
        archived: Optional[bool] = Omit, # type: ignore
        description: str = Omit, # type: ignore
        display_icon_id: Optional[str] = Omit, # type: ignore
        member_ids: List[str] = Omit, # type: ignore
        mention_name: str = Omit, # type: ignore
        name: str = Omit # type: ignore
    ) -> Group:
        """
        param group_public_id: Required. The unique ID of the Group.
        param archived: Whether or not this Group is archived.
        param description: The description of this Group.
        param display_icon_id: The Icon id for the avatar of this Group.
        param member_ids: The Member ids to add to this Group.
        param mention_name: The mention name of this Group.
        param name: The name of this Group.
        """
        return self.put("/groups/{group_public_id}".format(group_public_id=group_public_id), PrepareLocals({
            'archived': archived,
            'description': description,
            'display_icon_id': display_icon_id,
            'member_ids': member_ids,
            'mention_name': mention_name,
            'name': name
        })).json()
        

    ##############
    # Iterations #
    ##############

    def createIteration(self,
        end_date: str,
        name: str,
        start_date: str,
        description: str = Omit, # type: ignore
        follower_ids: List[str] = Omit, # type: ignore
        labels: List[CreateLabelParams] = Omit # type: ignore
    ) -> Iteration:
        """
        param end_date: Required. The date this Iteration ends, e.g. 2019-07-01.
        param name: Required. The name of this Iteration.
        param start_date: Required. The date this Iteration begins, e.g. 2019-07-01.
        param description: The description of the Iteration.
        param follower_ids: An array of UUIDs for any Members you want to add as Followers.
        param labels: An array of Labels attached to the Iteration.
        """
        return self.post("/iterations", PrepareLocals({
            'end_date': end_date,
            'name': name,
            'start_date': start_date,
            'description': description,
            'follower_ids': follower_ids,
            'labels': labels
        })).json()
        

    def deleteIteration(self, iteration_public_id: int):
        """param iteration_public_id: Required. The unique ID of the Iteration."""
        self.delete("/iterations/{iteration_public_id}".format(iteration_public_id=iteration_public_id))
        

    def disableIterations(self):
        """Disables Iterations for the current workspace"""
        self.put("/iterations/disable")
        

    def enableIterations(self):
        """Enables Iterations for the current workspace"""
        self.put("/iterations/enable")
        

    def getIteration(self, iteration_public_id: int) -> Iteration:
        """param iteration_public_id: Required. The unique ID of the Iteration."""
        return self.get("/iterations/{iteration_public_id}".format(iteration_public_id=iteration_public_id)).json()
        

    def listIterations(self) -> List[IterationSlim]:
        return self.get("/iterations").json()
        

    def updateIteration(self,
        iteration_public_id: int,
        description: str = Omit, # type: ignore
        end_date: str = Omit, # type: ignore
        follower_ids: List[str] = Omit, # type: ignore
        labels: List[CreateLabelParams] = Omit, # type: ignore
        name: str = Omit, # type: ignore
        start_date: str = Omit # type: ignore
    ) -> Iteration:
        """
        param iteration_public_id: Required. The unique ID of the Iteration.
        param description: The description of the Iteration.
        param end_date: The date this Iteration ends, e.g. 2019-07-05.
        param follower_ids: An array of UUIDs for any Members you want to add as Followers.
        param labels: An array of Labels attached to the Iteration.
        param name: The name of this Iteration
        param start_date: The date this Iteration begins, e.g. 2019-07-01
        """
        return self.put("/iterations/{iteration_public_id}".format(iteration_public_id=iteration_public_id), PrepareLocals({
            'description': description,
            'end_date': end_date,
            'follower_ids': follower_ids,
            'labels': labels,
            'name': name,
            'start_date': start_date
        })).json()
        

    ##########
    # Labels #
    ##########

    def createLabel(self,
        name: str,
        color: str = Omit, # type: ignore
        description: str = Omit, # type: ignore
        external_id: str = Omit # type: ignore
    ) -> Label:
        """
        Create Label allows you to create a new Label in Clubhouse.
        
        param name: Required. The name of the new Label.
        param color: The hex color to be displayed with the Label (for example, “#ff0000”).
        param description: The description of the new Label.
        param external_id: This field can be set to another unique ID. In the case that the Label has been imported from another tool, the ID in the other tool can be indicated here.
        """
        return self.post("/labels", PrepareLocals({
            'name': name,
            'color': color,
            'description': description,
            'external_id': external_id
        })).json()
        

    def deleteLabel(self, label_public_id: int):
        """
        Delete Label can be used to delete any Label.
        
        param label_public_id: Required. The unique ID of the Label.
        """
        self.delete("/labels/{label_public_id}".format(label_public_id=label_public_id))
        

    def getLabel(self, label_public_id: int) -> Label:
        """
        Get Label returns information about the selected Label.
        
        param label_public_id: Required. The unique ID of the Label.
        """
        return self.get("/labels/{label_public_id}".format(label_public_id=label_public_id)).json()
        

    def listLabelEpics(self, label_public_id: int) -> List[EpicSlim]:
        """
        List all of the Epics with the Label.
        
        param label_public_id: Required. The unique ID of the Label.
        """
        return self.get("/labels/{label_public_id}/epics".format(label_public_id=label_public_id)).json()
        

    def listLabels(self) -> List[Label]:
        """List Labels returns a list of all Labels and their attributes."""
        return self.get("/labels").json()
        

    def updateLabel(self,
        label_public_id: int,
        archived: bool = Omit, # type: ignore
        color: Optional[str] = Omit, # type: ignore
        description: str = Omit, # type: ignore
        name: str = Omit # type: ignore
    ) -> Label:
        """
        Update Label allows you to replace a Label name with another name. If you try to name a Label something that already exists, you will receive a 422 response.
        
        param label_public_id: Required. The unique ID of the Label you wish to update.
        param archived: A true/false boolean indicating if the Label has been archived.
        param color: The hex color to be displayed with the Label (for example, “#ff0000”).
        param description: The new description of the label.
        param name: The new name of the label.
        """
        return self.put("/labels/{label_public_id}".format(label_public_id=label_public_id), PrepareLocals({
            'archived': archived,
            'color': color,
            'description': description,
            'name': name
        })).json()
        

    ################
    # Linked-Files #
    ################

    def createLinkedFile(self,
        name: str,
        type: LinkedFileType,
        url: str,
        content_type: str = Omit, # type: ignore
        description: str = Omit, # type: ignore
        size: int = Omit, # type: ignore
        story_id: int = Omit, # type: ignore
        thumbnail_url: str = Omit, # type: ignore
        uploader_id: str = Omit # type: ignore
    ) -> LinkedFile:
        """
        Create Linked File allows you to create a new Linked File in Clubhouse.
        
        param name: Required. The name of the file.
        param type: Required. The integration type of the file (e.g. google, dropbox, box).
        param url: Required. The URL of linked file.
        param content_type: The content type of the image (e.g. txt/plain).
        param description: The description of the file.
        param size: The filesize, if the integration provided it.
        param story_id: The ID of the linked story.
        param thumbnail_url: The URL of the thumbnail, if the integration provided it.
        param uploader_id: The UUID of the member that uploaded the file.
        """
        return self.post("/linked-files", PrepareLocals({
            'name': name,
            'type': type,
            'url': url,
            'content_type': content_type,
            'description': description,
            'size': size,
            'story_id': story_id,
            'thumbnail_url': thumbnail_url,
            'uploader_id': uploader_id
        })).json()
        

    def deleteLinkedFile(self, linked_file_public_id: int):
        """
        Delete Linked File can be used to delete any previously attached Linked-File.
        
        param linked_file_public_id: Required. The unique identifier of the linked file.
        """
        self.delete("/linked-files/{linked_file_public_id}".format(linked_file_public_id=linked_file_public_id))
        

    def getLinkedFile(self, linked_file_public_id: int) -> LinkedFile:
        """
        Get File returns information about the selected Linked File.
        
        param linked_file_public_id: Required. The unique identifier of the linked file.
        """
        return self.get("/linked-files/{linked_file_public_id}".format(linked_file_public_id=linked_file_public_id)).json()
        

    def listLinkedFiles(self) -> List[LinkedFile]:
        """List Linked Files returns a list of all Linked-Files and their attributes."""
        return self.get("/linked-files").json()
        

    def updateLinkedFile(self,
        linked_file_public_id: int,
        description: str = Omit, # type: ignore
        name: str = Omit, # type: ignore
        size: int = Omit, # type: ignore
        story_id: int = Omit, # type: ignore
        thumbnail_url: str = Omit, # type: ignore
        type: LinkedFileType = Omit, # type: ignore
        uploader_id: str = Omit, # type: ignore
        url: str = Omit # type: ignore
    ) -> LinkedFile:
        """
        Updated Linked File allows you to update properties of a previously attached Linked-File.
        
        param linked_file_public_id: Required. The unique identifier of the linked file.
        param description: The description of the file.
        param name: The name of the file.
        param size: The filesize, if the integration provided it.
        param story_id: The ID of the linked story.
        param thumbnail_url: The URL of the thumbnail, if the integration provided it.
        param type: The integration type of the file (e.g. google, dropbox, box).
        param uploader_id: The UUID of the member that uploaded the file.
        param url: The URL of linked file.
        """
        return self.put("/linked-files/{linked_file_public_id}".format(linked_file_public_id=linked_file_public_id), PrepareLocals({
            'description': description,
            'name': name,
            'size': size,
            'story_id': story_id,
            'thumbnail_url': thumbnail_url,
            'type': type,
            'uploader_id': uploader_id,
            'url': url
        })).json()
        

    ##########
    # Member #
    ##########

    def getCurrentMemberInfo(self) -> MemberInfo:
        """Returns information about the authenticated member."""
        return self.get("/member").json()
        

    ###########
    # Members #
    ###########

    def getMember(self,
        member_public_id: str,
        org_public_id: str = Omit # type: ignore
    ) -> Member:
        """
        Returns information about a Member.
        
        param member_public_id: Required. The Member’s unique ID.
        param org_public_id: The unique ID of the Organization to limit the lookup to.
        """
        return self.get("/members/{member_public_id}".format(member_public_id=member_public_id), PrepareLocals({
            'org-public-id': org_public_id
        })).json()
        

    def listMembers(self,
        org_public_id: str = Omit # type: ignore
    ) -> List[Member]:
        """
        List Members returns information about members of the organization.
        
        param org_public_id: The unique ID of the Organization to limit the list to.
        """
        return self.get("/members", PrepareLocals({
            'org-public-id': org_public_id
        })).json()
        

    ##############
    # Milestones #
    ##############

    def createMilestone(self,
        name: str,
        categories: List[CreateCategoryParams] = Omit, # type: ignore
        completed_at_override: datetime = Omit, # type: ignore
        description: str = Omit, # type: ignore
        started_at_override: datetime = Omit, # type: ignore
        state: MilestoneWorkflowState = Omit # type: ignore
    ) -> Milestone:
        """
        Create Milestone allows you to create a new Milestone in Clubhouse.
        
        param name: Required. The name of the Milestone.
        param categories: An array of IDs of Categories attached to the Milestone.
        param completed_at_override: A manual override for the time/date the Milestone was completed.
        param description: The Milestone’s description.
        param started_at_override: A manual override for the time/date the Milestone was started.
        param state: The workflow state that the Milestone is in.
        """
        return self.post("/milestones", PrepareLocals({
            'name': name,
            'categories': categories,
            'completed_at_override': completed_at_override,
            'description': description,
            'started_at_override': started_at_override,
            'state': state
        })).json()
        

    def deleteMilestone(self, milestone_public_id: int):
        """
        Delete Milestone can be used to delete any Milestone.
        
        param milestone_public_id: Required. The ID of the Milestone.
        """
        self.delete("/milestones/{milestone_public_id}".format(milestone_public_id=milestone_public_id))
        

    def getMilestone(self, milestone_public_id: int) -> Milestone:
        """
        Get Milestone returns information about a chosen Milestone.
        
        param milestone_public_id: Required. The ID of the Milestone.
        """
        return self.get("/milestones/{milestone_public_id}".format(milestone_public_id=milestone_public_id)).json()
        

    def listMilestoneEpics(self, milestone_public_id: int) -> List[EpicSlim]:
        """
        List all of the Epics within the Milestone.
        
        param milestone_public_id: Required. The ID of the Milestone.
        """
        return self.get("/milestones/{milestone_public_id}/epics".format(milestone_public_id=milestone_public_id)).json()
        

    def listMilestones(self) -> List[Milestone]:
        """List Milestones returns a list of all Milestones and their attributes."""
        return self.get("/milestones").json()
        

    def updateMilestone(self,
        milestone_public_id: int,
        after_id: int = Omit, # type: ignore
        before_id: int = Omit, # type: ignore
        categories: List[CreateCategoryParams] = Omit, # type: ignore
        completed_at_override: Optional[datetime] = Omit, # type: ignore
        description: str = Omit, # type: ignore
        name: str = Omit, # type: ignore
        started_at_override: Optional[datetime] = Omit, # type: ignore
        state: MilestoneWorkflowState = Omit # type: ignore
    ) -> Milestone:
        """
        Update Milestone can be used to update Milestone properties.
        
        param milestone_public_id: Required. The ID of the Milestone.
        param after_id: The ID of the Milestone we want to move this Milestone after.
        param before_id: The ID of the Milestone we want to move this Milestone before.
        param categories: An array of IDs of Categories attached to the Milestone.
        param completed_at_override: A manual override for the time/date the Milestone was completed.
        param description: The Milestone’s description.
        param name: The name of the Milestone.
        param started_at_override: A manual override for the time/date the Milestone was started.
        param state: The workflow state that the Milestone is in.
        """
        return self.put("/milestones/{milestone_public_id}".format(milestone_public_id=milestone_public_id), PrepareLocals({
            'after_id': after_id,
            'before_id': before_id,
            'categories': categories,
            'completed_at_override': completed_at_override,
            'description': description,
            'name': name,
            'started_at_override': started_at_override,
            'state': state
        })).json()
        

    ############
    # Projects #
    ############

    def createProject(self,
        name: str,
        team_id: int,
        abbreviation: str = Omit, # type: ignore
        color: str = Omit, # type: ignore
        created_at: datetime = Omit, # type: ignore
        description: str = Omit, # type: ignore
        external_id: str = Omit, # type: ignore
        follower_ids: List[str] = Omit, # type: ignore
        iteration_length: int = Omit, # type: ignore
        start_time: datetime = Omit, # type: ignore
        updated_at: datetime = Omit # type: ignore
    ) -> Project:
        """
        Create Project is used to create a new Clubhouse Project.
        
        param name: Required. The name of the Project.
        param team_id: Required. The ID of the team the project belongs to.
        param abbreviation: The Project abbreviation used in Story summaries. Should be kept to 3 characters at most.
        param color: The color you wish to use for the Project in the system.
        param created_at: Defaults to the time/date it is created but can be set to reflect another date.
        param description: The Project description.
        param external_id: This field can be set to another unique ID. In the case that the Project has been imported from another tool, the ID in the other tool can be indicated here.
        param follower_ids: An array of UUIDs for any members you want to add as Owners on this new Epic.
        param iteration_length: The number of weeks per iteration in this Project.
        param start_time: The date at which the Project was started.
        param updated_at: Defaults to the time/date it is created but can be set to reflect another date.
        """
        return self.post("/projects", PrepareLocals({
            'name': name,
            'team_id': team_id,
            'abbreviation': abbreviation,
            'color': color,
            'created_at': created_at,
            'description': description,
            'external_id': external_id,
            'follower_ids': follower_ids,
            'iteration_length': iteration_length,
            'start_time': start_time,
            'updated_at': updated_at
        })).json()
        

    def deleteProject(self, project_public_id: int):
        """
        Delete Project can be used to delete a Project. Projects can only be deleted if all associated Stories are moved or deleted. In the case that the Project cannot be deleted, you will receive a 422 response.
        
        param project_public_id: Required. The unique ID of the Project.
        """
        self.delete("/projects/{project_public_id}".format(project_public_id=project_public_id))
        

    def getProject(self, project_public_id: int) -> Project:
        """
        Get Project returns information about the selected Project.
        
        param project_public_id: Required. The unique ID of the Project.
        """
        return self.get("/projects/{project_public_id}".format(project_public_id=project_public_id)).json()
        

    def listProjects(self) -> List[Project]:
        """List Projects returns a list of all Projects and their attributes."""
        return self.get("/projects").json()
        

    def listStories(self, project_public_id: int) -> List[StorySlim]:
        """
        List Stories returns a list of all Stories in a selected Project and their attributes.
        
        param project_public_id: Required. The unique ID of the Project.
        """
        return self.get("/projects/{project_public_id}/stories".format(project_public_id=project_public_id)).json()
        

    def updateProject(self,
        project_public_id: int,
        abbreviation: str = Omit, # type: ignore
        archived: bool = Omit, # type: ignore
        color: str = Omit, # type: ignore
        days_to_thermometer: int = Omit, # type: ignore
        description: str = Omit, # type: ignore
        follower_ids: List[str] = Omit, # type: ignore
        name: str = Omit, # type: ignore
        show_thermometer: bool = Omit, # type: ignore
        team_id: int = Omit # type: ignore
    ) -> Project:
        """
        Update Project can be used to change properties of a Project.
        
        param project_public_id: Required. The unique ID of the Project.
        param abbreviation: The Project abbreviation used in Story summaries. Should be kept to 3 characters at most.
        param archived: A true/false boolean indicating whether the Story is in archived state.
        param color: The color that represents the Project in the UI.
        param days_to_thermometer: The number of days before the thermometer appears in the Story summary.
        param description: The Project’s description.
        param follower_ids: An array of UUIDs for any Members you want to add as Followers.
        param name: The Project’s name.
        param show_thermometer: Configuration to enable or disable thermometers in the Story summary.
        param team_id: The ID of the team the project belongs to.
        """
        return self.put("/projects/{project_public_id}".format(project_public_id=project_public_id), PrepareLocals({
            'abbreviation': abbreviation,
            'archived': archived,
            'color': color,
            'days_to_thermometer': days_to_thermometer,
            'description': description,
            'follower_ids': follower_ids,
            'name': name,
            'show_thermometer': show_thermometer,
            'team_id': team_id
        })).json()
        

    ################
    # Repositories #
    ################

    def getRepository(self, repo_public_id: int) -> Repository:
        """
        Get Repository returns information about the selected Repository.
        
        param repo_public_id: Required. The unique ID of the Repository.
        """
        return self.get("/repositories/{repo_public_id}".format(repo_public_id=repo_public_id)).json()
        

    def listRepositories(self) -> List[Repository]:
        """List Repositories returns a list of all Repositories and their attributes."""
        return self.get("/repositories").json()
        

    ##########
    # Search #
    ##########

    def search(self,
        query: str,
        page_size: int = Omit # type: ignore
    ) -> SearchResults:
        """
        Search lets you search Epics and Stories based on desired parameters. Since ordering of the results can change over time (due to search ranking decay, new Epics and Stories being created), the next value from the previous response can be used as the path and query string for the next page to ensure stable ordering.
        
        param query: Required. See our help center article on search operators
        param page_size: The number of search results to include in a page. Minimum of 1 and maximum of 25.
        """
        return self.get("/search", PrepareLocals({
            'query': query,
            'page_size': page_size
        })).json()
        

    def searchEpics(self,
        query: str,
        page_size: int = Omit # type: ignore
    ) -> EpicSearchResults:
        """
        Search Epics lets you search Epics based on desired parameters. Since ordering of stories can change over time (due to search ranking decay, new Epics being created), the next value from the previous response can be used as the path and query string for the next page to ensure stable ordering.
        
        param query: Required. See our help center article on search operators
        param page_size: The number of search results to include in a page. Minimum of 1 and maximum of 25.
        """
        return self.get("/search/epics", PrepareLocals({
            'query': query,
            'page_size': page_size
        })).json()
        

    def searchStories(self,
        query: str,
        page_size: int = Omit # type: ignore
    ) -> StorySearchResults:
        """
        Search Stories lets you search Stories based on desired parameters. Since ordering of stories can change over time (due to search ranking decay, new stories being created), the next value from the previous response can be used as the path and query string for the next page to ensure stable ordering.
        
        param query: Required. See our help center article on search operators
        param page_size: The number of search results to include in a page. Minimum of 1 and maximum of 25.
        """
        return self.get("/search/stories", PrepareLocals({
            'query': query,
            'page_size': page_size
        })).json()
        

    ###########
    # Stories #
    ###########

    def createComment(self,
        story_public_id: int,
        text: str,
        author_id: str = Omit, # type: ignore
        created_at: datetime = Omit, # type: ignore
        external_id: str = Omit, # type: ignore
        updated_at: datetime = Omit # type: ignore
    ) -> Comment:
        """
        Create Comment allows you to create a Comment on any Story.
        
        param story_public_id: Required. The ID of the Story that the Comment is in.
        param text: Required. The comment text.
        param author_id: The Member ID of the Comment’s author. Defaults to the user identified by the API token.
        param created_at: Defaults to the time/date the comment is created, but can be set to reflect another date.
        param external_id: This field can be set to another unique ID. In the case that the comment has been imported from another tool, the ID in the other tool can be indicated here.
        param updated_at: Defaults to the time/date the comment is last updated, but can be set to reflect another date.
        """
        return self.post("/stories/{story_public_id}/comments".format(story_public_id=story_public_id), PrepareLocals({
            'text': text,
            'author_id': author_id,
            'created_at': created_at,
            'external_id': external_id,
            'updated_at': updated_at
        })).json()
        

    def createMultipleStories(self, stories: List[CreateStoryParams]) -> List[StorySlim]:
        """
        Create Multiple Stories allows you to create multiple stories in a single request using the same syntax as Create Story.
        
        param stories: Required. An array of stories to be created.
        """
        return self.post("/stories/bulk", PrepareLocals({
            'stories': stories
        })).json()
        

    def createReaction(self, comment_public_id: int, emoji: str, story_public_id: int) -> List[Reaction]:
        """
        Create a reaction to a comment.
        
        param comment_public_id: Required. The ID of the Comment.
        param emoji: Required. The emoji short-code to add / remove. E.g. :thumbsup::skin-tone-4:.
        param story_public_id: Required. The ID of the Story that the Comment is in.
        """
        return self.post("/stories/{story_public_id}/comments/{comment_public_id}/reactions".format(comment_public_id=comment_public_id,story_public_id=story_public_id), PrepareLocals({
            'emoji': emoji
        })).json()
        

    def createStory(self,
        name: str,
        project_id: int,
        archived: bool = Omit, # type: ignore
        comments: List[CreateStoryCommentParams] = Omit, # type: ignore
        completed_at_override: datetime = Omit, # type: ignore
        created_at: datetime = Omit, # type: ignore
        deadline: Optional[datetime] = Omit, # type: ignore
        description: str = Omit, # type: ignore
        epic_id: Optional[int] = Omit, # type: ignore
        estimate: Optional[int] = Omit, # type: ignore
        external_id: str = Omit, # type: ignore
        external_tickets: List[CreateExternalTicketParams] = Omit, # type: ignore
        file_ids: List[int] = Omit, # type: ignore
        follower_ids: List[str] = Omit, # type: ignore
        iteration_id: Optional[int] = Omit, # type: ignore
        labels: List[CreateLabelParams] = Omit, # type: ignore
        linked_file_ids: List[int] = Omit, # type: ignore
        owner_ids: List[str] = Omit, # type: ignore
        requested_by_id: str = Omit, # type: ignore
        started_at_override: datetime = Omit, # type: ignore
        story_links: List[CreateStoryLinkParams] = Omit, # type: ignore
        story_type: StoryType = Omit, # type: ignore
        tasks: List[CreateTaskParams] = Omit, # type: ignore
        updated_at: datetime = Omit, # type: ignore
        workflow_state_id: int = Omit # type: ignore
    ) -> Story:
        """
        Create Story is used to add a new story to your Clubhouse.
        
        param name: Required. The name of the story.
        param project_id: Required. The ID of the project the story belongs to.
        param archived: Controls the story’s archived state.
        param comments: An array of comments to add to the story.
        param completed_at_override: A manual override for the time/date the Story was completed.
        param created_at: The time/date the Story was created.
        param deadline: The due date of the story.
        param description: The description of the story.
        param epic_id: The ID of the epic the story belongs to.
        param estimate: The numeric point estimate of the story. Can also be null, which means unestimated.
        param external_id: This field can be set to another unique ID. In the case that the Story has been imported from another tool, the ID in the other tool can be indicated here.
        param external_tickets: An array of External Tickets associated with this story. These External Tickets must have unquie external id. Duplicated External Tickets will be removed.
        param file_ids: An array of IDs of files attached to the story.
        param follower_ids: An array of UUIDs of the followers of this story.
        param iteration_id: The ID of the iteration the story belongs to.
        param labels: An array of labels attached to the story.
        param linked_file_ids: An array of IDs of linked files attached to the story.
        param owner_ids: An array of UUIDs of the owners of this story.
        param requested_by_id: The ID of the member that requested the story.
        param started_at_override: A manual override for the time/date the Story was started.
        param story_links: An array of story links attached to the story.
        param story_type: The type of story (feature, bug, chore).
        param tasks: An array of tasks connected to the story.
        param updated_at: The time/date the Story was updated.
        param workflow_state_id: The ID of the workflow state the story is currently in.
        """
        return self.post("/stories", PrepareLocals({
            'name': name,
            'project_id': project_id,
            'archived': archived,
            'comments': comments,
            'completed_at_override': completed_at_override,
            'created_at': created_at,
            'deadline': deadline,
            'description': description,
            'epic_id': epic_id,
            'estimate': estimate,
            'external_id': external_id,
            'external_tickets': external_tickets,
            'file_ids': file_ids,
            'follower_ids': follower_ids,
            'iteration_id': iteration_id,
            'labels': labels,
            'linked_file_ids': linked_file_ids,
            'owner_ids': owner_ids,
            'requested_by_id': requested_by_id,
            'started_at_override': started_at_override,
            'story_links': story_links,
            'story_type': story_type,
            'tasks': tasks,
            'updated_at': updated_at,
            'workflow_state_id': workflow_state_id
        })).json()
        

    def createTask(self,
        description: str,
        story_public_id: int,
        complete: bool = Omit, # type: ignore
        created_at: datetime = Omit, # type: ignore
        external_id: str = Omit, # type: ignore
        owner_ids: List[str] = Omit, # type: ignore
        updated_at: datetime = Omit # type: ignore
    ) -> Task:
        """
        Create Task is used to create a new task in a Story.
        
        param description: Required. The Task description.
        param story_public_id: Required. The ID of the Story that the Task will be in.
        param complete: True/false boolean indicating whether the Task is completed. Defaults to false.
        param created_at: Defaults to the time/date the Task is created but can be set to reflect another creation time/date.
        param external_id: This field can be set to another unique ID. In the case that the Task has been imported from another tool, the ID in the other tool can be indicated here.
        param owner_ids: An array of UUIDs for any members you want to add as Owners on this new Task.
        param updated_at: Defaults to the time/date the Task is created in Clubhouse but can be set to reflect another time/date.
        """
        return self.post("/stories/{story_public_id}/tasks".format(story_public_id=story_public_id), PrepareLocals({
            'description': description,
            'complete': complete,
            'created_at': created_at,
            'external_id': external_id,
            'owner_ids': owner_ids,
            'updated_at': updated_at
        })).json()
        

    def deleteComment(self, comment_public_id: int, story_public_id: int):
        """
        Delete a Comment from any story.
        
        param comment_public_id: Required. The ID of the Comment.
        param story_public_id: Required. The ID of the Story that the Comment is in.
        """
        self.delete("/stories/{story_public_id}/comments/{comment_public_id}".format(comment_public_id=comment_public_id,story_public_id=story_public_id))
        

    def deleteMultipleStories(self, story_ids: List[int]):
        """
        Delete Multiple Stories allows you to delete multiple archived stories at once.
        
        param story_ids: Required. An array of IDs of Stories to delete.
        """
        self.delete("/stories/bulk", PrepareLocals({
            'story_ids': story_ids
        }))
        

    def deleteReaction(self, comment_public_id: int, emoji: str, story_public_id: int):
        """
        Delete a Reaction from any comment.
        
        param comment_public_id: Required. The ID of the Comment.
        param emoji: Required. The emoji short-code to add / remove. E.g. :thumbsup::skin-tone-4:.
        param story_public_id: Required. The ID of the Story that the Comment is in.
        """
        self.delete("/stories/{story_public_id}/comments/{comment_public_id}/reactions".format(comment_public_id=comment_public_id,story_public_id=story_public_id), PrepareLocals({
            'emoji': emoji
        }))
        

    def deleteStory(self, story_public_id: int):
        """
        Delete Story can be used to delete any Story.
        
        param story_public_id: Required. The ID of the Story.
        """
        self.delete("/stories/{story_public_id}".format(story_public_id=story_public_id))
        

    def deleteTask(self, story_public_id: int, task_public_id: int):
        """
        Delete Task can be used to delete any previously created Task on a Story.
        
        param story_public_id: Required. The unique ID of the Story this Task is associated with.
        param task_public_id: Required. The unique ID of the Task.
        """
        self.delete("/stories/{story_public_id}/tasks/{task_public_id}".format(story_public_id=story_public_id,task_public_id=task_public_id))
        

    def getComment(self, comment_public_id: int, story_public_id: int) -> Comment:
        """
        Get Comment is used to get Comment information.
        
        param comment_public_id: Required. The ID of the Comment.
        param story_public_id: Required. The ID of the Story that the Comment is in.
        """
        return self.get("/stories/{story_public_id}/comments/{comment_public_id}".format(comment_public_id=comment_public_id,story_public_id=story_public_id)).json()
        

    def getStory(self, story_public_id: int) -> Story:
        """
        Get Story returns information about a chosen Story.
        
        param story_public_id: Required. The ID of the Story.
        """
        return self.get("/stories/{story_public_id}".format(story_public_id=story_public_id)).json()
        

    def getTask(self, story_public_id: int, task_public_id: int) -> Task:
        """
        Returns information about a chosen Task.
        
        param story_public_id: Required. The unique ID of the Story this Task is associated with.
        param task_public_id: Required. The unique ID of the Task.
        """
        return self.get("/stories/{story_public_id}/tasks/{task_public_id}".format(story_public_id=story_public_id,task_public_id=task_public_id)).json()
        

    def searchStoriesOld(self,
        archived: bool = Omit, # type: ignore
        completed_at_end: datetime = Omit, # type: ignore
        completed_at_start: datetime = Omit, # type: ignore
        created_at_end: datetime = Omit, # type: ignore
        created_at_start: datetime = Omit, # type: ignore
        deadline_end: datetime = Omit, # type: ignore
        deadline_start: datetime = Omit, # type: ignore
        epic_id: Optional[int] = Omit, # type: ignore
        epic_ids: List[int] = Omit, # type: ignore
        estimate: int = Omit, # type: ignore
        external_id: str = Omit, # type: ignore
        iteration_id: Optional[int] = Omit, # type: ignore
        iteration_ids: List[int] = Omit, # type: ignore
        label_ids: List[int] = Omit, # type: ignore
        label_name: str = Omit, # type: ignore
        owner_id: Optional[str] = Omit, # type: ignore
        owner_ids: List[str] = Omit, # type: ignore
        project_id: int = Omit, # type: ignore
        project_ids: List[int] = Omit, # type: ignore
        requested_by_id: str = Omit, # type: ignore
        story_type: StoryType = Omit, # type: ignore
        updated_at_end: datetime = Omit, # type: ignore
        updated_at_start: datetime = Omit, # type: ignore
        workflow_state_id: int = Omit, # type: ignore
        workflow_state_types: List[WorkflowStateTypes] = Omit # type: ignore
    ) -> List[StorySlim]:
        """
        Search Stories lets you search Stories based on desired parameters.
        
        param archived: A true/false boolean indicating whether the Story is in archived state.
        param completed_at_end: Stories should have been completed before this date.
        param completed_at_start: Stories should have been competed after this date.
        param created_at_end: Stories should have been created before this date.
        param created_at_start: Stories should have been created after this date.
        param deadline_end: Stories should have a deadline before this date.
        param deadline_start: Stories should have a deadline after this date.
        param epic_id: The Epic IDs that may be associated with the Stories.
        param epic_ids: The Epic IDs that may be associated with the Stories.
        param estimate: The number of estimate points associate with the Stories.
        param external_id: An ID or URL that references an external resource. Useful during imports.
        param iteration_id: The Iteration ID that may be associated with the Stories.
        param iteration_ids: The Iteration IDs that may be associated with the Stories.
        param label_ids: The Label IDs that may be associated with the Stories.
        param label_name: The name of any associated Labels.
        param owner_id: An array of UUIDs for any Users who may be Owners of the Stories.
        param owner_ids: An array of UUIDs for any Users who may be Owners of the Stories.
        param project_id: The IDs for the Projects the Stories may be assigned to.
        param project_ids: The IDs for the Projects the Stories may be assigned to.
        param requested_by_id: The UUID of any Users who may have requested the Stories.
        param story_type: The type of Stories that you want returned.
        param updated_at_end: Stories should have been updated before this date.
        param updated_at_start: Stories should have been updated after this date.
        param workflow_state_id: The unique IDs of the specific Workflow States that the Stories should be in.
        param workflow_state_types: The type of Workflow State the Stories may be in.
        """
        return self.post("/stories/search", PrepareLocals({
            'archived': archived,
            'completed_at_end': completed_at_end,
            'completed_at_start': completed_at_start,
            'created_at_end': created_at_end,
            'created_at_start': created_at_start,
            'deadline_end': deadline_end,
            'deadline_start': deadline_start,
            'epic_id': epic_id,
            'epic_ids': epic_ids,
            'estimate': estimate,
            'external_id': external_id,
            'iteration_id': iteration_id,
            'iteration_ids': iteration_ids,
            'label_ids': label_ids,
            'label_name': label_name,
            'owner_id': owner_id,
            'owner_ids': owner_ids,
            'project_id': project_id,
            'project_ids': project_ids,
            'requested_by_id': requested_by_id,
            'story_type': story_type,
            'updated_at_end': updated_at_end,
            'updated_at_start': updated_at_start,
            'workflow_state_id': workflow_state_id,
            'workflow_state_types': workflow_state_types
        })).json()
        

    def updateComment(self, comment_public_id: int, story_public_id: int, text: str) -> Comment:
        """
        Update Comment replaces the text of the existing Comment.
        
        param comment_public_id: Required. The ID of the Comment
        param story_public_id: Required. The ID of the Story that the Comment is in.
        param text: Required. The updated comment text.
        """
        return self.put("/stories/{story_public_id}/comments/{comment_public_id}".format(comment_public_id=comment_public_id,story_public_id=story_public_id), PrepareLocals({
            'text': text
        })).json()
        

    def updateMultipleStories(self,
        story_ids: List[int],
        after_id: int = Omit, # type: ignore
        archived: bool = Omit, # type: ignore
        before_id: int = Omit, # type: ignore
        deadline: Optional[datetime] = Omit, # type: ignore
        epic_id: Optional[int] = Omit, # type: ignore
        estimate: Optional[int] = Omit, # type: ignore
        follower_ids_add: List[str] = Omit, # type: ignore
        follower_ids_remove: List[str] = Omit, # type: ignore
        iteration_id: Optional[int] = Omit, # type: ignore
        labels_add: List[CreateLabelParams] = Omit, # type: ignore
        labels_remove: List[CreateLabelParams] = Omit, # type: ignore
        owner_ids_add: List[str] = Omit, # type: ignore
        owner_ids_remove: List[str] = Omit, # type: ignore
        project_id: int = Omit, # type: ignore
        requested_by_id: str = Omit, # type: ignore
        story_type: StoryType = Omit, # type: ignore
        workflow_state_id: int = Omit # type: ignore
    ) -> List[StorySlim]:
        """
        Update Multiple Stories allows you to make changes to numerous stories at once.
        
        param story_ids: Required. The unique IDs of the Stories you wish to update.
        param after_id: The ID of the story that the stories are to be moved below.
        param archived: If the Stories should be archived or not.
        param before_id: The ID of the story that the stories are to be moved before.
        param deadline: The due date of the story.
        param epic_id: The ID of the epic the story belongs to.
        param estimate: The numeric point estimate of the story. Can also be null, which means unestimated.
        param follower_ids_add: The UUIDs of the new followers to be added.
        param follower_ids_remove: The UUIDs of the followers to be removed.
        param iteration_id: The ID of the iteration the story belongs to.
        param labels_add: An array of labels to be added.
        param labels_remove: An array of labels to be removed.
        param owner_ids_add: The UUIDs of the new owners to be added.
        param owner_ids_remove: The UUIDs of the owners to be removed.
        param project_id: The ID of the Project the Stories should belong to.
        param requested_by_id: The ID of the member that requested the story.
        param story_type: The type of story (feature, bug, chore).
        param workflow_state_id: The ID of the workflow state the story is currently in.
        """
        return self.put("/stories/bulk", PrepareLocals({
            'story_ids': story_ids,
            'after_id': after_id,
            'archived': archived,
            'before_id': before_id,
            'deadline': deadline,
            'epic_id': epic_id,
            'estimate': estimate,
            'follower_ids_add': follower_ids_add,
            'follower_ids_remove': follower_ids_remove,
            'iteration_id': iteration_id,
            'labels_add': labels_add,
            'labels_remove': labels_remove,
            'owner_ids_add': owner_ids_add,
            'owner_ids_remove': owner_ids_remove,
            'project_id': project_id,
            'requested_by_id': requested_by_id,
            'story_type': story_type,
            'workflow_state_id': workflow_state_id
        })).json()
        

    def updateStory(self,
        story_public_id: int,
        after_id: int = Omit, # type: ignore
        archived: bool = Omit, # type: ignore
        before_id: int = Omit, # type: ignore
        branch_ids: List[int] = Omit, # type: ignore
        commit_ids: List[int] = Omit, # type: ignore
        completed_at_override: Optional[datetime] = Omit, # type: ignore
        deadline: Optional[datetime] = Omit, # type: ignore
        description: str = Omit, # type: ignore
        epic_id: Optional[int] = Omit, # type: ignore
        estimate: Optional[int] = Omit, # type: ignore
        file_ids: List[int] = Omit, # type: ignore
        follower_ids: List[str] = Omit, # type: ignore
        iteration_id: Optional[int] = Omit, # type: ignore
        labels: List[CreateLabelParams] = Omit, # type: ignore
        linked_file_ids: List[int] = Omit, # type: ignore
        name: str = Omit, # type: ignore
        owner_ids: List[str] = Omit, # type: ignore
        project_id: int = Omit, # type: ignore
        pull_request_ids: List[int] = Omit, # type: ignore
        requested_by_id: str = Omit, # type: ignore
        started_at_override: Optional[datetime] = Omit, # type: ignore
        story_type: StoryType = Omit, # type: ignore
        workflow_state_id: int = Omit # type: ignore
    ) -> Story:
        """
        Update Story can be used to update Story properties.
        
        param story_public_id: Required. The unique identifier of this story.
        param after_id: The ID of the story we want to move this story after.
        param archived: True if the story is archived, otherwise false.
        param before_id: The ID of the story we want to move this story before.
        param branch_ids: An array of IDs of Branches attached to the story.
        param commit_ids: An array of IDs of Commits attached to the story.
        param completed_at_override: A manual override for the time/date the Story was completed.
        param deadline: The due date of the story.
        param description: The description of the story.
        param epic_id: The ID of the epic the story belongs to.
        param estimate: The numeric point estimate of the story. Can also be null, which means unestimated.
        param file_ids: An array of IDs of files attached to the story.
        param follower_ids: An array of UUIDs of the followers of this story.
        param iteration_id: The ID of the iteration the story belongs to.
        param labels: An array of labels attached to the story.
        param linked_file_ids: An array of IDs of linked files attached to the story.
        param name: The title of the story.
        param owner_ids: An array of UUIDs of the owners of this story.
        param project_id: The ID of the project the story belongs to.
        param pull_request_ids: An array of IDs of Pull/Merge Requests attached to the story.
        param requested_by_id: The ID of the member that requested the story.
        param started_at_override: A manual override for the time/date the Story was started.
        param story_type: The type of story (feature, bug, chore).
        param workflow_state_id: The ID of the workflow state the story is currently in.
        """
        return self.put("/stories/{story_public_id}".format(story_public_id=story_public_id), PrepareLocals({
            'after_id': after_id,
            'archived': archived,
            'before_id': before_id,
            'branch_ids': branch_ids,
            'commit_ids': commit_ids,
            'completed_at_override': completed_at_override,
            'deadline': deadline,
            'description': description,
            'epic_id': epic_id,
            'estimate': estimate,
            'file_ids': file_ids,
            'follower_ids': follower_ids,
            'iteration_id': iteration_id,
            'labels': labels,
            'linked_file_ids': linked_file_ids,
            'name': name,
            'owner_ids': owner_ids,
            'project_id': project_id,
            'pull_request_ids': pull_request_ids,
            'requested_by_id': requested_by_id,
            'started_at_override': started_at_override,
            'story_type': story_type,
            'workflow_state_id': workflow_state_id
        })).json()
        

    def updateTask(self,
        story_public_id: int,
        task_public_id: int,
        after_id: int = Omit, # type: ignore
        before_id: int = Omit, # type: ignore
        complete: bool = Omit, # type: ignore
        description: str = Omit, # type: ignore
        owner_ids: List[str] = Omit # type: ignore
    ) -> Task:
        """
        Update Task can be used to update Task properties.
        
        param story_public_id: Required. The unique identifier of the parent Story.
        param task_public_id: Required. The unique identifier of the Task you wish to update.
        param after_id: Move task after this task ID.
        param before_id: Move task before this task ID.
        param complete: A true/false boolean indicating whether the task is complete.
        param description: The Task’s description.
        param owner_ids: An array of UUIDs of the owners of this story.
        """
        return self.put("/stories/{story_public_id}/tasks/{task_public_id}".format(story_public_id=story_public_id,task_public_id=task_public_id), PrepareLocals({
            'after_id': after_id,
            'before_id': before_id,
            'complete': complete,
            'description': description,
            'owner_ids': owner_ids
        })).json()
        

    ###############
    # Story-Links #
    ###############

    def createStoryLink(self, object_id: int, subject_id: int, verb: StoryLinkVerb) -> StoryLink:
        """
        Story Links (called Story Relationships in the UI) allow you create semantic relationships between two stories. The parameters read like an active voice grammatical sentence: subject -> verb -> object.
        The subject story acts on the object Story; the object story is the direct object of the sentence.
        The subject story “blocks”, “duplicates”, or “relates to” the object story. Examples:
        “story 5 blocks story 6” – story 6 is now “blocked” until story 5 is moved to a Done workflow state.
        “story 2 duplicates story 1” – Story 2 represents the same body of work as Story 1 (and should probably be archived).
        “story 7 relates to story 3”
        
        param object_id: Required. The ID of the object Story.
        param subject_id: Required. The ID of the subject Story.
        param verb: Required. The type of link.
        """
        return self.post("/story-links", PrepareLocals({
            'object_id': object_id,
            'subject_id': subject_id,
            'verb': verb
        })).json()
        

    def deleteStoryLink(self, story_link_public_id: int):
        """
        Delete Story Link can be used to delete any Story Link.
        
        param story_link_public_id: Required. The unique ID of the Story Link.
        """
        self.delete("/story-links/{story_link_public_id}".format(story_link_public_id=story_link_public_id))
        

    def getStoryLink(self, story_link_public_id: int) -> StoryLink:
        """
        Returns information about the selected Story Link.
        
        param story_link_public_id: Required. The unique ID of the Story Link.
        """
        return self.get("/story-links/{story_link_public_id}".format(story_link_public_id=story_link_public_id)).json()
        

    def updateStoryLink(self, story_link_public_id: int, verb: StoryLinkVerb) -> StoryLink:
        """
        Update the relationship for the Story Link.
        
        param story_link_public_id: Required. The unique ID of the Story Link.
        param verb: Required. The type of link.
        """
        return self.put("/story-links/{story_link_public_id}".format(story_link_public_id=story_link_public_id), PrepareLocals({
            'verb': verb
        })).json()
        

    #########
    # Teams #
    #########

    def getTeam(self, team_public_id: int) -> Team:
        """
        Get Team is used to get Team information.
        
        param team_public_id: Required. The ID of the team.
        """
        return self.get("/teams/{team_public_id}".format(team_public_id=team_public_id)).json()
        

    def listTeams(self) -> List[Team]:
        """List Teams returns a list of all Teams in the organization."""
        return self.get("/teams").json()
        

    #############
    # Workflows #
    #############

    def listWorkflows(self) -> List[Workflow]:
        """List Workflows returns a list of all Workflows in the organization."""
        return self.get("/workflows").json()
        



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
