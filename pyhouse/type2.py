from typing import List, Optional, TypedDict                                                                                 
import datetime                                                                                 


##############
# Categories #
##############

class Category(TypedDict, total=False):                                                                                 
    """A Category can be used to associate Milestones."""                                                                                 
    archived: bool                                             # A true/false boolean indicating if the Category has been archived.
    color: Optional[str]                                       # The hex color to be displayed with the Category (for example, “#ff0000”).
    created_at: datetime.datetime                              # The time/date that the Category was created.
    entity_type: str                                           # A string description of this resource.
    external_id: Optional[str]                                 # This field can be set to another unique ID. In the case that the Category has been imported from another tool, the ID in the other tool can be indicated here.
    id: int                                                    # The unique ID of the Category.
    name: str                                                  # The name of the Category.
    type: str                                                  # The type of entity this Category is associated with; currently Milestone is the only type of Category.
    updated_at: datetime.datetime                              # The time/date that the Category was updated.

class CreateCategoryParams(TypedDict, total=False):                                                                                 
    """Request parameters for creating a Category with a Milestone."""                                                                                 
    color: str                                                 # The hex color to be displayed with the Category (for example, “#ff0000”).
    external_id: str                                           # This field can be set to another unique ID. In the case that the Category has been imported from another tool, the ID in the other tool can be indicated here.
    name: str                                                  # The name of the new Category.


####################
# Entity Templates #
####################

class CreateEntityTemplateExternalTicket(TypedDict, total=False):                                                                                 
    external_id: str                                           # The id of the ticket in the external system.
    external_url: str                                          # The url for the ticket in the external system.

class EntityTemplateTask(TypedDict, total=False):                                                                                 
    """Request parameters for specifying how to pre-populate a task through a template."""                                                                                 
    complete: bool                                             # True/false boolean indicating whether the Task is completed. Defaults to false.
    description: str                                           # The Task description.
    external_id: str                                           # This field can be set to another unique ID. In the case that the Task has been imported from another tool, the ID in the other tool can be indicated here.
    owner_ids: List[str]                                       # An array of UUIDs for any members you want to add as Owners on this new Task.

class CreateStoryContents(TypedDict, total=False):                                                                                 
    """A map of story attributes this template populates."""                                                                                 
    deadline: Optional[datetime.datetime]                      # The due date of the story.
    description: str                                           # The description of the story.
    entity_type: str                                           # A string description of this resource.
    epic_id: Optional[int]                                     # The ID of the epic the to be populated.
    estimate: Optional[int]                                    # The numeric point estimate to be populated.
    external_tickets: List[CreateEntityTemplateExternalTicket] # An array of the external ticket IDs to be populated.
    file_ids: List[int]                                        # An array of the attached file IDs to be populated.
    files: List['File']                                        # An array of files attached to the story.
    follower_ids: List[str]                                    # An array of UUIDs for any Members listed as Followers.
    iteration_id: Optional[int]                                # The ID of the iteration the to be populated.
    labels: List['CreateLabelParams']                          # An array of labels to be populated by the template.
    linked_file_ids: List[int]                                 # An array of the linked file IDs to be populated.
    linked_files: List['LinkedFile']                           # An array of linked files attached to the story.
    name: str                                                  # The name of the story.
    owner_ids: List[str]                                       # An array of UUIDs of the owners of this story.
    project_id: int                                            # The ID of the project the story belongs to.
    story_type: str                                            # The type of story (feature, bug, chore).
    tasks: List[EntityTemplateTask]                            # An array of tasks to be populated by the template.
    workflow_state_id: int                                     # The ID of the workflow state the story is currently in.

class CreateEntityTemplate(TypedDict, total=False):                                                                                 
    """Request paramaters for creating an entirely new entity template."""                                                                                 
    author_id: str                                             # The id of the user creating this template.
    name: str                                                  # The name of the new entity template
    story_contents: CreateStoryContents                        # A map of story attributes this template populates.

class ResponseStoryContentsTasks(TypedDict, total=False):                                                                                 
    """Alias of Response1337718StoryContentsTasks Response1337764StoryContentsTasks Response1337785StoryContentsTasks EntityTemplateStoryContentsTasks"""
    complete: bool
    description: str
    external_id: str
    owner_ids: List[str]
    position: int

class StoryContents(TypedDict, total=False):                                                                                 
    """A container entity for the attributes this template should populate."""                                                                                 
    deadline: datetime.datetime                                # The due date of the story.
    description: str                                           # The description of the story.
    entity_type: str                                           # A string description of this resource.
    epic_id: int                                               # The ID of the epic the story belongs to.
    estimate: int                                              # The numeric point estimate of the story. Can also be null, which means unestimated.
    external_tickets: List['ExternalTicket']                   # An array of external tickets connected to the story.
    files: List['File']                                        # An array of files attached to the story.
    follower_ids: List[str]                                    # An array of UUIDs for any Members listed as Followers.
    iteration_id: int                                          # The ID of the iteration the story belongs to.
    labels: List['Label']                                      # An array of labels attached to the story.
    linked_files: List['LinkedFile']                           # An array of linked files attached to the story.
    name: str                                                  # The name of the story.
    owner_ids: List[str]                                       # An array of UUIDs of the owners of this story.
    project_id: int                                            # The ID of the project the story belongs to.
    story_type: str                                            # The type of story (feature, bug, chore).
    tasks: List[ResponseStoryContentsTasks]                    # An array of tasks connected to the story.
    workflow_state_id: int                                     # The ID of the workflow state the story is currently in.

class EntityTemplate(TypedDict, total=False):                                                                                 
    """An entity template can be used to prefill various fields when creating new stories."""                                                                                 
    author_id: str                                             # The unique ID of the member who created the template.
    created_at: datetime.datetime                              # The time/date when the entity template was created.
    entity_type: str                                           # A string description of this resource.
    id: str                                                    # The unique identifier for the entity template.
    last_used_at: datetime.datetime                            # The last time that someone created an entity using this template.
    name: str                                                  # The template’s name.
    story_contents: StoryContents                              # A container entity for the attributes this template should populate.
    updated_at: datetime.datetime                              # The time/date when the entity template was last updated.
                                                                                     
class UpdateEntityTemplate(TypedDict, total=False):                                                                                 
    """Request parameters for changing either a template’s name or any of the attributes it is designed to pre-populate."""                                                                                 
    name: str                                                  # The updated template name.
    story_contents: CreateStoryContents                        # A map of story attributes this template populates.


#########
# Epics #
#########

class ThreadedComment(TypedDict, total=False):                                                                                 
    """Comments associated with Epic Discussions."""                                                                                 
    app_url: str                                               # The Clubhouse application url for the Comment.
    author_id: str                                             # The unique ID of the Member that authored the Comment.
    comments: List['ThreadedComment']                          # A nested array of threaded comments.
    created_at: datetime.datetime                              # The time/date the Comment was created.
    deleted: bool                                              # True/false boolean indicating whether the Comment is deleted.
    entity_type: str                                           # A string description of this resource.
    external_id: Optional[str]                                 # This field can be set to another unique ID. In the case that the Comment has been imported from another tool, the ID in the other tool can be indicated here.
    group_mention_ids: List[str]                               # An array of Group IDs that have been mentioned in this Comment.
    id: int                                                    # The unique ID of the Comment.
    member_mention_ids: List[str]                              # An array of Member IDs that have been mentioned in this Comment.
    mention_ids: List[str]                                     # Deprecated: use member_mention_ids.
    text: str                                                  # The text of the Comment.
    updated_at: datetime.datetime                              # The time/date the Comment was updated.

class EpicStats(TypedDict, total=False):                                                                                 
    """A group of calculated values for this Epic."""                                                                                 
    average_cycle_time: int                                    # The average cycle time (in seconds) of completed stories in this Epic.
    average_lead_time: int                                     # The average lead time (in seconds) of completed stories in this Epic.
    last_story_update: Optional[datetime.datetime]             # The date of the last update of a Story in this Epic.
    num_points: int                                            # The total number of points in this Epic.
    num_points_done: int                                       # The total number of completed points in this Epic.
    num_points_started: int                                    # The total number of started points in this Epic.
    num_points_unstarted: int                                  # The total number of unstarted points in this Epic.
    num_stories_done: int                                      # The total number of done Stories in this Epic.
    num_stories_started: int                                   # The total number of started Stories in this Epic.
    num_stories_unestimated: int                               # The total number of Stories with no point estimate.
    num_stories_unstarted: int                                 # The total number of unstarted Stories in this Epic.

class Epic(TypedDict, total=False):                                                                                 
    """An Epic is a collection of stories that together might make up a release, a milestone, or some other large initiative that your organization is working on."""                                                                                 
    app_url: str                                               # The Clubhouse application url for the Epic.
    archived: bool                                             # True/false boolean that indicates whether the Epic is archived or not.
    comments: List[ThreadedComment]                            # A nested array of threaded comments.
    completed: bool                                            # A true/false boolean indicating if the Epic has been completed.
    completed_at: Optional[datetime.datetime]                  # The time/date the Epic was completed.
    completed_at_override: Optional[datetime.datetime]         # A manual override for the time/date the Epic was completed.
    created_at: Optional[datetime.datetime]                    # The time/date the Epic was created.
    deadline: Optional[datetime.datetime]                      # The Epic’s deadline.
    description: str                                           # The Epic’s description.
    entity_type: str                                           # A string description of this resource.
    epic_state_id: int                                         # The ID of the Epic State.
    external_id: Optional[str]                                 # This field can be set to another unique ID. In the case that the Epic has been imported from another tool, the ID in the other tool can be indicated here.
    external_tickets: List['ExternalTicket']                   # 
    follower_ids: List[str]                                    # An array of UUIDs for any Members you want to add as Followers on this Epic.
    group_mention_ids: List[str]                               # An array of Group IDs that have been mentioned in the Epic description.
    id: int                                                    # The unique ID of the Epic.
    labels: List['Label']                                      # An array of Labels attached to the Epic.
    member_mention_ids: List[str]                              # An array of Member IDs that have been mentioned in the Epic description.
    mention_ids: List[str]                                     # Deprecated: use member_mention_ids.
    milestone_id: Optional[int]                                # The ID of the Milestone this Epic is related to.
    name: str                                                  # The name of the Epic.
    owner_ids: List[str]                                       # An array of UUIDs for any members you want to add as Owners on this new Epic.
    position: int                                              # The Epic’s relative position in the Epic workflow state.
    project_ids: List[int]                                     # The IDs of Projects related to this Epic.
    requested_by_id: str                                       # The ID of the Member that requested the epic.
    started: bool                                              # A true/false boolean indicating if the Epic has been started.
    started_at: Optional[datetime.datetime]                    # The time/date the Epic was started.
    started_at_override: Optional[datetime.datetime]           # A manual override for the time/date the Epic was started.
    state: str                                                 # Deprecated The workflow state that the Epic is in.
    stats: EpicStats                                           # A group of calculated values for this Epic.
    updated_at: Optional[datetime.datetime]                    # The time/date the Epic was updated.

class EpicSlim(TypedDict, total=False):                                                                                 
    """EpicSlim represents the same resource as an Epic but is more light-weight, including all Epic fields except the description string and comments List. Use the Get Epic endpoint to fetch the unabridged payload for an Epic."""                                                                                 
    app_url: str                                               # The Clubhouse application url for the Epic.
    archived: bool                                             # True/false boolean that indicates whether the Epic is archived or not.
    completed: bool                                            # A true/false boolean indicating if the Epic has been completed.
    completed_at: Optional[datetime.datetime]                  # The time/date the Epic was completed.
    completed_at_override: Optional[datetime.datetime]         # A manual override for the time/date the Epic was completed.
    created_at: Optional[datetime.datetime]                    # The time/date the Epic was created.
    deadline: Optional[datetime.datetime]                      # The Epic’s deadline.
    entity_type: str                                           # A string description of this resource.
    epic_state_id: int                                         # The ID of the Epic State.
    external_id: Optional[str]                                 # This field can be set to another unique ID. In the case that the Epic has been imported from another tool, the ID in the other tool can be indicated here.
    external_tickets: List['ExternalTicket']                   # 
    follower_ids: List[str]                                    # An array of UUIDs for any Members you want to add as Followers on this Epic.
    group_mention_ids: List[str]                               # An array of Group IDs that have been mentioned in the Epic description.
    id: int                                                    # The unique ID of the Epic.
    labels: List['Label']                                      # An array of Labels attached to the Epic.
    member_mention_ids: List[str]                              # An array of Member IDs that have been mentioned in the Epic description.
    mention_ids: List[str]                                     # Deprecated: use member_mention_ids.
    milestone_id: Optional[int]                                # The ID of the Milestone this Epic is related to.
    name: str                                                  # The name of the Epic.
    owner_ids: List[str]                                       # An array of UUIDs for any members you want to add as Owners on this new Epic.
    position: int                                              # The Epic’s relative position in the Epic workflow state.
    project_ids: List[int]                                     # The IDs of Projects related to this Epic.
    requested_by_id: str                                       # The ID of the Member that requested the epic.
    started: bool                                              # A true/false boolean indicating if the Epic has been started.
    started_at: Optional[datetime.datetime]                    # The time/date the Epic was started.
    started_at_override: Optional[datetime.datetime]           # A manual override for the time/date the Epic was started.
    state: str                                                 # Deprecated The workflow state that the Epic is in.
    stats: EpicStats                                           # A group of calculated values for this Epic.
    updated_at: Optional[datetime.datetime]                    # The time/date the Epic was updated.

class EpicState(TypedDict, total=False):                                                                                 
    """Epic State is any of the at least 3 columns. Epic States correspond to one of 3 types: Unstarted, Started, or Done."""                                                                                 
    color: str                                                 # The hex color for this Epic State.
    created_at: datetime.datetime                              # The time/date the Epic State was created.
    description: str                                           # The description of what sort of Epics belong in that Epic State.
    entity_type: str                                           # A string description of this resource.
    id: int                                                    # The unique ID of the Epic State.
    name: str                                                  # The Epic State’s name.
    position: int                                              # The position that the Epic State is in, starting with 0 at the left.
    type: str                                                  # The type of Epic State (Unstarted, Started, or Done)
    updated_at: datetime.datetime                              # When the Epic State was last updated.

class EpicWorkflow(TypedDict, total=False):                                                                                 
    """Epic Workflow is the Listof defined Epic States. Epic Workflow can be queried using the API but must be updatetime.datetimed in the Clubhouse UI."""                                                                                 
    created_at: datetime.datetime                              # The date the Epic Workflow was created.
    default_epic_state_id: int                                 # The unique ID of the default Epic State that new Epics are assigned by default.
    entity_type: str                                           # A string description of this resource.
    epic_states: List[EpicState]                               # A map of the Epic States in this Epic Workflow.
    id: int                                                    # The unique ID of the Epic Workflow.
    updated_at: datetime.datetime                              # The date the Epic Workflow was updated.


####################
# External Tickets #
####################

class CreateExternalTicketParams(TypedDict, total=False):                                                                                 
    external_id: str                                           # The id of the ticket in the external system.
    external_url: str                                          # The url for the ticket in the external system.
                                                                                     
class ExternalTicket(TypedDict, total=False):                                                                                 
    """A External Ticket allows you to create a link between an external system, like Zendesk, and a Clubhouse story."""                                                                                 
    epic_ids: List[int]                                        # The Clubhouse Epics associated with this External Ticket
    external_id: str                                           # The ID used in the external system.
    external_url: str                                          # The full qualified url of the external ticket.
    id: str                                                    # A unique ID internal to Clubhouse.
    story_ids: List[int]                                       # The Clubhouse Story ids associated with this External Ticket.


#########
# Files #
#########

class File(TypedDict, total=False):                                                                                 
    """A File is any document uploaded to your Clubhouse. Files attached from a third-party service can be accessed using the Linked Files endpoint."""                                                                                 
    content_type: str                                          # Free form string corresponding to a text or image file.
    created_at: datetime.datetime                              # The time/date that the file was created.
    description: Optional[str]                                 # The description of the file.
    entity_type: str                                           # A string description of this resource.
    external_id: Optional[str]                                 # This field can be set to another unique ID. In the case that the File has been imported from another tool, the ID in the other tool can be indicated here.
    filename: str                                              # The name assigned to the file in Clubhouse upon upload.
    group_mention_ids: List[str]                               # The unique IDs of the Groups who are mentioned in the file description.
    id: int                                                    # The unique ID for the file.
    member_mention_ids: List[str]                              # The unique IDs of the Members who are mentioned in the file description.
    mention_ids: List[str]                                     # Deprecated: use member_mention_ids.
    name: str                                                  # The optional User-specified name of the file.
    size: int                                                  # The size of the file.
    story_ids: List[int]                                       # The unique IDs of the Stories associated with this file.
    thumbnail_url: Optional[str]                               # The url where the thumbnail of the file can be found in Clubhouse.
    updated_at: Optional[datetime.datetime]                    # The time/date that the file was updated.
    uploader_id: str                                           # The unique ID of the Member who uploaded the file.
    url: Optional[str]                                         # The URL for the file.

class LinkedFile(TypedDict, total=False):                                                                                 
    """Linked files are stored on a third-party website and linked to one or more Stories. Clubhouse currently supports linking files from Google Drive, Dropbox, Box, and by URL."""                                                                                 
    content_type: Optional[str]                                # The content type of the image (e.g. txt/plain).
    created_at: datetime.datetime                              # The time/date the LinkedFile was created.
    description: Optional[str]                                 # The description of the file.
    entity_type: str                                           # A string description of this resource.
    group_mention_ids: List[str]                               # The groups that are mentioned in the description of the file.
    id: int                                                    # The unique identifier for the file.
    member_mention_ids: List[str]                              # The members that are mentioned in the description of the file.
    mention_ids: List[str]                                     # Deprecated: use member_mention_ids.
    name: str                                                  # The name of the linked file.
    size: Optional[int]                                        # The filesize, if the integration provided it.
    story_ids: List[int]                                       # The IDs of the stories this file is attached to.
    thumbnail_url: Optional[str]                               # The URL of the file thumbnail, if the integration provided it.
    type: str                                                  # The integration type (e.g. google, dropbox, box).
    updated_at: datetime.datetime                              # The time/date the LinkedFile was updated.
    uploader_id: str                                           # The UUID of the member that uploaded the file.
    url: str                                                   # The URL of the file.

class Icon(TypedDict, total=False):                                                                                 
    """Icons are used to attach images to Organizations, Members, and Loading screens in the Clubhouse web application."""                                                                                 
    created_at: datetime.datetime                              # The time/date that the Icon was created.
    entity_type: str                                           # A string description of this resource.
    id: str                                                    # The unique ID of the Icon.
    updated_at: datetime.datetime                              # The time/date that the Icon was updated.
    url: str                                                   # The URL of the Icon.

######################
# GitHub integration #
######################

class Identity(TypedDict, total=False):                                                                                 
    """The Identity of the GitHub user that authored the Commit."""                                                                                 
    entity_type: str                                           # A string description of this resource.
    name: Optional[str]                                        # This is your login in GitHub.
    type: Optional[str]                                        # The type of Identity; currently only type is github.

class PullRequest(TypedDict, total=False):                                                                                 
    """Corresponds to a GitHub Pull Request attached to a Clubhouse story."""                                                                                 
    branch_id: int                                             # The ID of the branch for the particular pull request.
    branch_name: str                                           # The name of the branch for the particular pull request.
    closed: bool                                               # True/False boolean indicating whether the GitHub pull request has been closed.
    created_at: datetime.datetime                              # The time/date the pull request was created.
    entity_type: str                                           # A string description of this resource.
    id: int                                                    # The unique ID associated with the pull request in Clubhouse.
    num_added: int                                             # Number of lines added in the pull request, according to GitHub.
    num_commits: Optional[int]                                 # The number of commits on the pull request.
    num_modified: Optional[int]                                # Number of lines modified in the pull request, according to GitHub.
    num_removed: int                                           # Number of lines removed in the pull request, according to GitHub.
    number: int                                                # The pull requests unique number ID in GitHub.
    target_branch_id: int                                      # The ID of the target branch for the particular pull request.
    target_branch_name: str                                    # The name of the target branch for the particular pull request.
    title: str                                                 # The title of the pull request.
    updated_at: datetime.datetime                              # The time/date the pull request was created.
    url: str                                                   # The URL for the pull request.

class Branch(TypedDict, total=False):                                                                                 
    """Branch refers to a GitHub branch. Branches are feature branches associated with Clubhouse Stories."""                                                                                 
    created_at: Optional[datetime.datetime]                    # The time/date the Branch was created.
    deleted: bool                                              # A true/false boolean indicating if the Branch has been deleted.
    entity_type: str                                           # A string description of this resource.
    id: Optional[int]                                          # The unique ID of the Branch.
    merged_branch_ids: List[int]                               # The IDs of the Branches the Branch has been merged into.
    name: str                                                  # The name of the Branch.
    persistent: bool                                           # A true/false boolean indicating if the Branch is persistent; e.g. master.
    pull_requests: List[PullRequest]                           # An array of PullRequests attached to the Branch (there is usually only one).
    repository_id: Optional[int]                               # The ID of the Repository that contains the Branch.
    updated_at: Optional[datetime.datetime]                    # The time/date the Branch was updated.
    url: str                                                   # The URL of the Branch.

class Commit(TypedDict, total=False):                                                                                 
    """Commit refers to a GitHub commit and all associated details."""                                                                                 
    author_email: str                                          # The email address of the GitHub user that authored the Commit.
    author_id: Optional[str]                                   # The ID of the Member that authored the Commit, if known.
    author_identity: Identity                                  # The Identity of the GitHub user that authored the Commit.
    created_at: datetime.datetime                              # The time/date the Commit was created.
    entity_type: str                                           # A string description of this resource.
    hash: str                                                  # The Commit hash.
    id: Optional[int]                                          # The unique ID of the Commit.
    merged_branch_ids: List[int]                               # The IDs of the Branches the Commit has been merged into.
    message: str                                               # The Commit message.
    repository_id: Optional[int]                               # The ID of the Repository that contains the Commit.
    timestamp: datetime.datetime                               # The time/date the Commit was pushed.
    updated_at: Optional[datetime.datetime]                    # The time/date the Commit was updated.
    url: str                                                   # The URL of the Commit.

class Repository(TypedDict, total=False):                                                                                 
    """Repository refers to a GitHub repository."""                                                                                 
    created_at: Optional[datetime.datetime]                    # The time/date the Repository was created.
    entity_type: str                                           # A string description of this resource.
    external_id: Optional[str]                                 # The GitHub unique identifier for the Repository.
    full_name: Optional[str]                                   # The full name of the GitHub repository.
    id: Optional[int]                                          # The ID associated to the GitHub repository in Clubhouse.
    name: Optional[str]                                        # The shorthand name of the GitHub repository.
    type: str                                                  # The type of Repository. Currently this can only be “github”.
    updated_at: Optional[datetime.datetime]                    # The time/date the Repository was updated.
    url: Optional[str]                                         # The URL of the Repository.


##########
# Groups #
##########

class CreateGroup(TypedDict, total=False):                                                                                 
    description: str                                           # The description of the Group.
    display_icon_id: str                                       # The Icon id for the avatar of this Group.
    member_ids: List[str]                                      # The Member ids to add to this Group.
    mention_name: str                                          # The mention name of this Group.
    name: str                                                  # The name of this Group.

class Group(TypedDict, total=False):                                                                                 
    """A Group."""                                                                                 
    archived: bool                                             # Whether or not the Group is archived.
    description: str                                           # The description of the Group.
    display_icon: Optional[Icon]                               # Icons are used to attach images to Organizations, Members, and Loading screens in the Clubhouse web application.
    entity_type: str                                           # A string description of this resource.
    id: str                                                    # The id of the Group.
    member_ids: List[str]                                      # The Member IDs contain within the Group.
    mention_name: str                                          # The mention name of the Group.
    name: str                                                  # The name of the Group.

class UpdateGroup(TypedDict, total=False):                                                                                 
    archived: Optional[bool]                                   # Whether or not this Group is archived.
    description: str                                           # The description of this Group.
    display_icon_id: Optional[str]                             # The Icon id for the avatar of this Group.
    member_ids: List[str]                                      # The Member ids to add to this Group.
    mention_name: str                                          # The mention name of this Group.
    name: str                                                  # The name of this Group.


##############
# Iterations #
##############

class CreateIteration(TypedDict, total=False):                                                                                 
    description: str                                           # The description of the Iteration.
    end_date: str                                              # The date this Iteration ends, e.g. 2019-07-01.
    follower_ids: List[str]                                    # An array of UUIDs for any Members you want to add as Followers.
    labels: List['CreateLabelParams']                          # An array of Labels attached to the Iteration.
    name: str                                                  # The name of this Iteration.
    start_date: str                                            # The date this Iteration begins, e.g. 2019-07-01.

class IterationStats(TypedDict, total=False):                                                                                 
    """A group of calculated values for this Iteration."""                                                                                 
    average_cycle_time: int                                    # The average cycle time (in seconds) of completed stories in this Iteration.
    average_lead_time: int                                     # The average lead time (in seconds) of completed stories in this Iteration.
    num_points: int                                            # The total number of points in this Iteration.
    num_points_done: int                                       # The total number of completed points in this Iteration.
    num_points_started: int                                    # The total number of started points in this Iteration.
    num_points_unstarted: int                                  # The total number of unstarted points in this Iteration.
    num_stories_done: int                                      # The total number of done Stories in this Iteration.
    num_stories_started: int                                   # The total number of started Stories in this Iteration.
    num_stories_unestimated: int                               # The total number of Stories with no point estimate.
    num_stories_unstarted: int                                 # The total number of unstarted Stories in this Iteration.

class Iteration(TypedDict, total=False):                                                                                 
    """An Iteration is a defined, time-boxed period of development for a collection of Stories. See https://help.clubhouse.io/hc/en-us/articles/360028953452-Iterations-Overview for more information."""                                                                                 
    app_url: str                                               # The Clubhouse application url for the Iteration.
    created_at: datetime.datetime                              # The instant when this iteration was created.
    description: str                                           # The description of the iteration.
    end_date: datetime.datetime                                # The date this iteration begins.
    entity_type: str                                           # A string description of this resource
    follower_ids: List[str]                                    # An array of UUIDs for any Members listed as Followers.
    group_mention_ids: List[str]                               # An array of Group IDs that have been mentioned in the Story description.
    id: int                                                    # The ID of the iteration.
    labels: List['Label']                                      # An array of labels attached to the iteration.
    member_mention_ids: List[str]                              # An array of Member IDs that have been mentioned in the Story description.
    mention_ids: List[str]                                     # Deprecated: use member_mention_ids.
    name: str                                                  # The name of the iteration.
    start_date: datetime.datetime                              # The date this iteration begins.
    stats: IterationStats                                      # A group of calculated values for this Iteration.
    status: str                                                # The status of the iteration. Values are either “unstarted”, “started”, or “done”.
    updated_at: datetime.datetime                              # The instant when this iteration was last updated.

class IterationSlim(TypedDict, total=False):                                                                                 
    """IterationSlim represents the same resource as an Iteration, but is more light-weight. Use the Get Iteration endpoint to fetch the unabridged payload for an Iteration."""                                                                                 
    app_url: str                                               # The Clubhouse application url for the Iteration.
    created_at: datetime.datetime                              # The instant when this iteration was created.
    end_date: datetime.datetime                                # The date this iteration begins.
    entity_type: str                                           # A string description of this resource
    follower_ids: List[str]                                    # An array of UUIDs for any Members listed as Followers.
    group_mention_ids: List[str]                               # An array of Group IDs that have been mentioned in the Story description.
    id: int                                                    # The ID of the iteration.
    labels: List['Label']                                      # An array of labels attached to the iteration.
    member_mention_ids: List[str]                              # An array of Member IDs that have been mentioned in the Story description.
    mention_ids: List[str]                                     # Deprecated: use member_mention_ids.
    name: str                                                  # The name of the iteration.
    start_date: datetime.datetime                              # The date this iteration begins.
    stats: IterationStats                                      # A group of calculated values for this Iteration.
    status: str                                                # The status of the iteration. Values are either “unstarted”, “started”, or “done”.
    updated_at: datetime.datetime                              # The instant when this iteration was last updated.

class UpdateIteration(TypedDict, total=False):                                                                                 
    description: str                                           # The description of the Iteration.
    end_date: str                                              # The date this Iteration ends, e.g. 2019-07-05.
    follower_ids: List[str]                                    # An array of UUIDs for any Members you want to add as Followers.
    labels: List['CreateLabelParams']                          # An array of Labels attached to the Iteration.
    name: str                                                  # The name of this Iteration
    start_date: str                                            # The date this Iteration begins, e.g. 2019-07-01


##############
# Milestones #
##############

class MilestoneStats(TypedDict, total=False):                                                                                 
    """A group of calculated values for this Milestone."""                                                                                 
    average_cycle_time: int                                    # The average cycle time (in seconds) of completed stories in this Milestone.
    average_lead_time: int                                     # The average lead time (in seconds) of completed stories in this Milestone.


class Milestone(TypedDict, total=False):                                                                                 
    """A Milestone is a collection of Epics that represent a release or some other large initiative that your organization is working on."""                                                                                 
    app_url: str                                               # The Clubhouse application url for the Milestone.
    categories: List[Category]                                 # An array of Categories attached to the Milestone.
    completed: bool                                            # A true/false boolean indicating if the Milestone has been completed.
    completed_at: Optional[datetime.datetime]                  # The time/date the Milestone was completed.
    completed_at_override: Optional[datetime.datetime]         # A manual override for the time/date the Milestone was completed.
    created_at: datetime.datetime                              # The time/date the Milestone was created.
    description: str                                           # The Milestone’s description.
    entity_type: str                                           # A string description of this resource.
    id: int                                                    # The unique ID of the Milestone.
    name: str                                                  # The name of the Milestone.
    position: int                                              # A number representing the position of the Milestone in relation to every other Milestone within the Organization.
    started: bool                                              # A true/false boolean indicating if the Milestone has been started.
    started_at: Optional[datetime.datetime]                    # The time/date the Milestone was started.
    started_at_override: Optional[datetime.datetime]           # A manual override for the time/date the Milestone was started.
    state: str                                                 # The workflow state that the Milestone is in.
    stats: MilestoneStats                                      # A group of calculated values for this Milestone.
    updated_at: datetime.datetime                              # The time/date the Milestone was updated.


################
# Organization #
################

class Profile(TypedDict, total=False):                                                                                 
    """A group of Member profile details."""                                                                                 
    deactivated: bool                                          # A true/false boolean indicating whether the Member has been deactivated within Clubhouse.
    display_icon: Optional[Icon]                               # Icons are used to attach images to Organizations, Members, and Loading screens in the Clubhouse web application.
    email_address: Optional[str]                               # The primary email address of the Member with the Organization.
    entity_type: str                                           # A string description of this resource.
    gravatar_hash: Optional[str]                               # This is the gravatar hash associated with email_address.
    id: str                                                    # The unique identifier of the profile.
    mention_name: str                                          # The Member’s username within the Organization.
    name: Optional[str]                                        # The Member’s name within the Organization.
    two_factor_auth_activated: bool                            # If Two Factor Authentication is activated for this User.

class Member(TypedDict, total=False):                                                                                 
    """Details about individual Clubhouse user within the Clubhouse organization that has issued the token."""                                                                                 
    created_at: Optional[datetime.datetime]                    # The time/date the Member was created.
    disabled: bool                                             # True/false boolean indicating whether the Member has been disabled within this Organization.
    entity_type: str                                           # A string description of this resource.
    id: str                                                    # The Member’s ID in Clubhouse.
    profile: Profile                                           # A group of Member profile details.
    role: str                                                  # The Member’s role in the Clubhouse organization.
    updated_at: Optional[datetime.datetime]                    # The time/date the Member was last updated.

class BasicWorkspaceInfo(TypedDict, total=False):                                                                                 
    estimate_scale: List[int] 
    url_slug: str 

class MemberInfo(TypedDict, total=False):                                                                                 
    id: str 
    mention_name: str 
    name: str 
    workspace2: BasicWorkspaceInfo 


############
# Projects #
############

class ProjectStats(TypedDict, total=False):                                                                                 
    """A group of calculated values for this Project."""                                                                                 
    num_points: int                                            # The total number of points in this Project.
    num_stories: int                                           # The total number of stories in this Project.

class Project(TypedDict, total=False):                                                                                 
    """Projects typically map to teams (such as Frontend, Backend, Mobile, Devops, etc) but can represent any open-ended product, component, or initiative."""                                                                                 
    abbreviation: Optional[str]                                # The Project abbreviation used in Story summaries. Should be kept to 3 characters at most.
    app_url: str                                               # The Clubhouse application url for the Project.
    archived: bool                                             # True/false boolean indicating whether the Project is in an Archived state.
    color: Optional[str]                                       # The color associated with the Project in the Clubhouse member interface.
    created_at: Optional[datetime.datetime]                    # The time/date that the Project was created.
    days_to_thermometer: int                                   # The number of days before the thermometer appears in the Story summary.
    description: Optional[str]                                 # The description of the Project.
    entity_type: str                                           # A string description of this resource.
    external_id: Optional[str]                                 # This field can be set to another unique ID. In the case that the Project has been imported from another tool, the ID in the other tool can be indicated here.
    follower_ids: List[str]                                    # An array of UUIDs for any Members listed as Followers.
    id: int                                                    # The unique ID of the Project.
    iteration_length: int                                      # The number of weeks per iteration in this Project.
    name: str                                                  # The name of the Project
    show_thermometer: bool                                     # Configuration to enable or disable thermometers in the Story summary.
    start_time: datetime.datetime                              # The date at which the Project was started.
    stats: ProjectStats                                        # A group of calculated values for this Project.
    team_id: int                                               # The ID of the team the project belongs to.
    updated_at: Optional[datetime.datetime]                    # The time/date that the Project was last updated.


##########
# Search #
##########

class EpicSearchResults(TypedDict, total=False):                                                                                 
    """The results of the Epic search query."""                                                                                 
    cursors: List[str]                                         # 
    data: List[Epic]                                           # A list of search results.
    next: Optional[str]                                        # The URL path and query string for the next page of search results.
    total: int                                                 # The total number of matches for the search query. The first 1000 matches can be paged through via the API.

class StorySearchResults(TypedDict, total=False):                                                                                 
    """The results of the Story search query."""                                                                                 
    cursors: List[str]                                         # 
    data: List['Story']                                        # A list of search results.
    next: Optional[str]                                        # The URL path and query string for the next page of search results.
    total: int                                                 # The total number of matches for the search query. The first 1000 matches can be paged through via the API.
                                                                                     
class SearchResults(TypedDict, total=False):                                                                                 
    """The results of the multi-entity search query."""                                                                                 
    epics: EpicSearchResults                                   # The results of the Epic search query.
    stories: StorySearchResults                                # The results of the Story search query.

class MaxSearchResultsExceededError(TypedDict, total=False):                                                                                 
    """Error returned when total maximum supported results have been reached."""                                                                                 
    error: str                                                 # The name for this type of error, maximum-results-exceeded
    maximum_results: int                                       # The maximum number of search results supported, 1000. Note for integration: This is in the documentation as maximum-results. It has been changed here under the assumption that it's a typo and would actually be maximum_results.
    message: str                                               # An explanatory message: “A maximum of 1000 search results are supported.”


###########
# Stories #
###########

class Comment(TypedDict, total=False):                                                                                 
    """A Comment is any note added within the Comment field of a Story."""                                                                                 
    app_url: str                                               # The Clubhouse application url for the Comment.
    author_id: Optional[str]                                   # The unique ID of the Member who is the Comment’s author.
    created_at: datetime.datetime                              # The time/date when the Comment was created.
    entity_type: str                                           # A string description of this resource.
    external_id: Optional[str]                                 # This field can be set to another unique ID. In the case that the Comment has been imported from another tool, the ID in the other tool can be indicated here.
    group_mention_ids: List[str]                               # The unique IDs of the Group who are mentioned in the Comment.
    id: int                                                    # The unique ID of the Comment.
    member_mention_ids: List[str]                              # The unique IDs of the Member who are mentioned in the Comment.
    mention_ids: List[str]                                     # Deprecated: use member_mention_ids.
    position: int                                              # The Comments numerical position in the list from oldest to newest.
    story_id: int                                              # The ID of the Story on which the Comment appears.
    text: str                                                  # The text of the Comment.
    updated_at: Optional[datetime.datetime]                    # The time/date when the Comment was updated.

class CreateLabelParams(TypedDict, total=False):                                                                                 
    """Request parameters for creating a Label on a Clubhouse story."""                                                                                 
    color: str                                                 # The hex color to be displayed with the Label (for example, “#ff0000”).
    description: str                                           # The description of the new Label.
    external_id: str                                           # This field can be set to another unique ID. In the case that the Label has been imported from another tool, the ID in the other tool can be indicated here.
    name: str                                                  # The name of the new Label.

class CreateStoryCommentParams(TypedDict, total=False):                                                                                 
    """Request parameters for creating a Comment on a Clubhouse Story."""                                                                                 
    author_id: str                                             # The Member ID of the Comment’s author. Defaults to the user identified by the API token.
    created_at: datetime.datetime                              # Defaults to the time/date the comment is created, but can be set to reflect another date.
    external_id: str                                           # This field can be set to another unique ID. In the case that the comment has been imported from another tool, the ID in the other tool can be indicated here.
    text: str                                                  # The comment text.
    updated_at: datetime.datetime                              # Defaults to the time/date the comment is last updated, but can be set to reflect another date.

class CreateTaskParams(TypedDict, total=False):                                                                                 
    """Request parameters for creating a Task on a Story."""                                                                                 
    complete: bool                                             # True/false boolean indicating whether the Task is completed. Defaults to false.
    created_at: datetime.datetime                              # Defaults to the time/date the Task is created but can be set to reflect another creation time/date.
    description: str                                           # The Task description.
    external_id: str                                           # This field can be set to another unique ID. In the case that the Task has been imported from another tool, the ID in the other tool can be indicated here.
    owner_ids: List[str]                                       # An array of UUIDs for any members you want to add as Owners on this new Task.
    updated_at: datetime.datetime                              # Defaults to the time/date the Task is created in Clubhouse but can be set to reflect another time/date.
                                                                                     
class LabelStats(TypedDict, total=False):                                                                                 
    """A group of calculated values for this Label."""                                                                                 
    num_epics: int                                             # The total number of Epics with this Label.
    num_points_completed: int                                  # The total number of completed points with this Label.
    num_points_in_progress: int                                # The total number of in-progress points with this Label.
    num_points_total: int                                      # The total number of points with this Label.
    num_stories_completed: int                                 # The total number of completed Stories with this Label.
    num_stories_in_progress: int                               # The total number of in-progress Stories with this Label.
    num_stories_total: int                                     # The total number of Stories with this Label.
    num_stories_unestimated: int                               # The total number of Stories with no point estimate with this Label.
                                                                                     
class Label(TypedDict, total=False):                                                                                 
    """A Label can be used to associate and filter Stories and Epics, and also create new Workspaces."""                                                                                 
    app_url: str                                               # The Clubhouse application url for the Label.
    archived: bool                                             # A true/false boolean indicating if the Label has been archived.
    color: Optional[str]                                       # The hex color to be displayed with the Label (for example, “#ff0000”).
    created_at: Optional[datetime.datetime]                    # The time/date that the Label was created.
    description: Optional[str]                                 # The description of the Label.
    entity_type: str                                           # A string description of this resource.
    external_id: Optional[str]                                 # This field can be set to another unique ID. In the case that the Label has been imported from another tool, the ID in the other tool can be indicated here.
    id: int                                                    # The unique ID of the Label.
    name: str                                                  # The name of the Label.
    stats: LabelStats                                          # A group of calculated values for this Label.
    updated_at: Optional[datetime.datetime]                    # The time/date that the Label was updated.

class StoryLink(TypedDict, total=False):                                                                                 
    """Story links allow you create semantic relationships between two stories. Relationship types are relates to, blocks / blocked by, and duplicates / is duplicated by. The format is subject -> link -> object, or for example “story 5 blocks story 6”."""                                                                                 
    created_at: datetime.datetime                              # The time/date when the Story Link was created.
    entity_type: str                                           # A string description of this resource.
    id: int                                                    # The unique identifier of the Story Link.
    object_id: int                                             # The ID of the object Story.
    subject_id: int                                            # The ID of the subject Story.
    updated_at: datetime.datetime                              # The time/date when the Story Link was last updated.
    verb: str                                                  # How the subject Story acts on the object Story. This can be “blocks”, “duplicates”, or “relates to”.

class TypedStoryLink(TypedDict, total=False):                                                                                 
    """The type of Story Link. The string can be subject or object."""                                                                                 
    created_at: datetime.datetime                              # The time/date when the Story Link was created.
    entity_type: str                                           # A string description of this resource.
    id: int                                                    # The unique identifier of the Story Link.
    object_id: int                                             # The ID of the object Story.
    subject_id: int                                            # The ID of the subject Story.
    type: str                                                  # This indicates whether the Story is the subject or object in the Story Link.
    updated_at: datetime.datetime                              # The time/date when the Story Link was last updated.
    verb: str                                                  # How the subject Story acts on the object Story. This can be “blocks”, “duplicates”, or “relates to”.
                                                                                     
class Task(TypedDict, total=False):                                                                                 
    complete: bool                                             # True/false boolean indicating whether the Task has been completed.
    completed_at: Optional[datetime.datetime]                  # The time/date the Task was completed.
    created_at: datetime.datetime                              # The time/date the Task was created.
    description: str                                           # Full text of the Task.
    entity_type: str                                           # A string description of this resource.
    external_id: Optional[str]                                 # This field can be set to another unique ID. In the case that the Task has been imported from another tool, the ID in the other tool can be indicated here.
    group_mention_ids: List[str]                               # An array of UUIDs of Groups mentioned in this Task.
    id: int                                                    # The unique ID of the Task.
    member_mention_ids: List[str]                              # An array of UUIDs of Members mentioned in this Task.
    mention_ids: List[str]                                     # Deprecated: use member_mention_ids.
    owner_ids: List[str]                                       # An array of UUIDs of the Owners of this Task.
    position: int                                              # The number corresponding to the Task’s position within a list of Tasks on a Story.
    story_id: int                                              # The unique identifier of the parent Story.
    updated_at: Optional[datetime.datetime]                    # The time/date the Task was updated.

class Story(TypedDict, total=False):                                                                                 
    """Stories are the standard unit of work in Clubhouse and represent individual features, bugs, and chores."""                                                                                 
    app_url: str                                               # The Clubhouse application url for the Story.
    archived: bool                                             # True if the story has been archived or not.
    blocked: bool                                              # A true/false boolean indicating if the Story is currently blocked.
    blocker: bool                                              # A true/false boolean indicating if the Story is currently a blocker of another story.
    branches: List[Branch]                                     # An array of Git branches attached to the story.
    comments: List[Comment]                                    # An array of comments attached to the story.
    commits: List[Commit]                                      # An array of commits attached to the story.
    completed: bool                                            # A true/false boolean indicating if the Story has been completed.
    completed_at: Optional[datetime.datetime]                  # The time/date the Story was completed.
    completed_at_override: Optional[datetime.datetime]         # A manual override for the time/date the Story was completed.
    created_at: datetime.datetime                              # The time/date the Story was created.
    cycle_time: int                                            # The cycle time (in seconds) of this story when complete.
    deadline: Optional[datetime.datetime]                      # The due date of the story.
    description: str                                           # The description of the story.
    entity_type: str                                           # A string description of this resource.
    epic_id: Optional[int]                                     # The ID of the epic the story belongs to.
    estimate: Optional[int]                                    # The numeric point estimate of the story. Can also be null, which means unestimated.
    external_id: Optional[str]                                 # This field can be set to another unique ID. In the case that the Story has been imported from another tool, the ID in the other tool can be indicated here.
    external_tickets: List[ExternalTicket]                     # An array of External Tickets associated with a Story
    files: List[File]                                          # An array of files attached to the story.
    follower_ids: List[str]                                    # An array of UUIDs for any Members listed as Followers.
    group_mention_ids: List[str]                               # An array of Group IDs that have been mentioned in the Story description.
    id: int                                                    # The unique ID of the Story.
    iteration_id: Optional[int]                                # The ID of the iteration the story belongs to.
    labels: List[Label]                                        # An array of labels attached to the story.
    lead_time: int                                             # The lead time (in seconds) of this story when complete.
    linked_files: List[LinkedFile]                             # An array of linked files attached to the story.
    member_mention_ids: List[str]                              # An array of Member IDs that have been mentioned in the Story description.
    mention_ids: List[str]                                     # Deprecated: use member_mention_ids.
    moved_at: Optional[datetime.datetime]                      # The time/date the Story was last changed workflow-state.
    name: str                                                  # The name of the story.
    owner_ids: List[str]                                       # An array of UUIDs of the owners of this story.
    position: int                                              # A number representing the position of the story in relation to every other story in the current project.
    previous_iteration_ids: List[int]                          # The IDs of the iteration the story belongs to.
    project_id: int                                            # The ID of the project the story belongs to.
    pull_requests: List[PullRequest]                           # An array of Pull/Merge Requests attached to the story.
    requested_by_id: str                                       # The ID of the Member that requested the story.
    started: bool                                              # A true/false boolean indicating if the Story has been started.
    started_at: Optional[datetime.datetime]                    # The time/date the Story was started.
    started_at_override: Optional[datetime.datetime]           # A manual override for the time/date the Story was started.
    story_links: List[TypedStoryLink]                          # An array of story links attached to the Story.
    story_type: str                                            # The type of story (feature, bug, chore).
    tasks: List[Task]                                          # An array of tasks connected to the story.
    updated_at: Optional[datetime.datetime]                    # The time/date the Story was updated.
    workflow_state_id: int                                     # The ID of the workflow state the story is currently in.

class StorySlim(TypedDict, total=False):                                                                                 
    """StorySlim represents the same resource as a Story, but is more light-weight. For certain fields it provides ids rather than full resources (e.g., comment_ids and file_ids) and it also excludes certain aggregate values (e.g., cycle_time). Use the Get Story endpoint to fetch the unabridged payload for a Story."""                                                                                 
    app_url: str                                               # The Clubhouse application url for the Story.
    archived: bool                                             # True if the story has been archived or not.
    blocked: bool                                              # A true/false boolean indicating if the Story is currently blocked.
    blocker: bool                                              # A true/false boolean indicating if the Story is currently a blocker of another story.
    comment_ids: List[int]                                     # An array of IDs of Comments attached to the story.
    completed: bool                                            # A true/false boolean indicating if the Story has been completed.
    completed_at: Optional[datetime.datetime]                  # The time/date the Story was completed.
    completed_at_override: Optional[datetime.datetime]         # A manual override for the time/date the Story was completed.
    created_at: datetime.datetime                              # The time/date the Story was created.
    deadline: Optional[datetime.datetime]                      # The due date of the story.
    entity_type: str                                           # A string description of this resource.
    epic_id: Optional[int]                                     # The ID of the epic the story belongs to.
    estimate: Optional[int]                                    # The numeric point estimate of the story. Can also be null, which means unestimated.
    external_id: Optional[str]                                 # This field can be set to another unique ID. In the case that the Story has been imported from another tool, the ID in the other tool can be indicated here.
    external_tickets: List[ExternalTicket]                     # An array of External Tickets associated with a Story
    file_ids: List[int]                                        # An array of IDs of Files attached to the story.
    follower_ids: List[str]                                    # An array of UUIDs for any Members listed as Followers.
    group_mention_ids: List[str]                               # An array of Group IDs that have been mentioned in the Story description.
    id: int                                                    # The unique ID of the Story.
    iteration_id: Optional[int]                                # The ID of the iteration the story belongs to.
    labels: List[Label]                                        # An array of labels attached to the story.
    linked_file_ids: List[int]                                 # An array of IDs of LinkedFiles attached to the story.
    member_mention_ids: List[str]                              # An array of Member IDs that have been mentioned in the Story description.
    mention_ids: List[str]                                     # Deprecated: use member_mention_ids.
    moved_at: Optional[datetime.datetime]                      # The time/date the Story was last changed workflow-state.
    name: str                                                  # The name of the story.
    owner_ids: List[str]                                       # An array of UUIDs of the owners of this story.
    position: int                                              # A number representing the position of the story in relation to every other story in the current project.
    previous_iteration_ids: List[int]                          # The IDs of the iteration the story belongs to.
    project_id: int                                            # The ID of the project the story belongs to.
    requested_by_id: str                                       # The ID of the Member that requested the story.
    started: bool                                              # A true/false boolean indicating if the Story has been started.
    started_at: Optional[datetime.datetime]                    # The time/date the Story was started.
    started_at_override: Optional[datetime.datetime]           # A manual override for the time/date the Story was started.
    story_links: List[TypedStoryLink]                          # An array of story links attached to the Story.
    story_type: str                                            # The type of story (feature, bug, chore).
    task_ids: List[int]                                        # An array of IDs of Tasks attached to the story.
    updated_at: Optional[datetime.datetime]                    # The time/date the Story was updated.
    workflow_state_id: int                                     # The ID of the workflow state the story is currently in.


#############
# Workflows #
#############

class WorkflowState(TypedDict, total=False):                                                                                 
    """Workflow State is any of the at least 3 columns. Workflow States correspond to one of 3 types: Unstarted, Started, or Done."""                                                                                 
    color: str                                                 # The hex color for this Workflow State.
    created_at: datetime.datetime                              # The time/date the Workflow State was created.
    description: str                                           # The description of what sort of Stories belong in that Workflow state.
    entity_type: str                                           # A string description of this resource.
    id: int                                                    # The unique ID of the Workflow State.
    name: str                                                  # The Workflow State’s name.
    num_stories: int                                           # The number of Stories currently in that Workflow State.
    num_story_templates: int                                   # The number of Story Templates associated with that Workflow State.
    position: int                                              # The position that the Workflow State is in, starting with 0 at the left.
    type: str                                                  # The type of Workflow State (Unstarted, Started, or Finished)
    updated_at: datetime.datetime                              # When the Workflow State was last updated.
    verb: Optional[str]                                        # The verb that triggers a move to that Workflow State when making GitHub commits.
                                                                                     
class Workflow(TypedDict, total=False):                                                                                 
    """Details of the workflow associated with the Team."""                                                                                 
    auto_assign_owner: bool                                    # Indicates if an owner is automatically assigned when an unowned story is started.
    created_at: datetime.datetime                              # The date the Workflow was created.
    default_state_id: int                                      # The unique ID of the default state that new Stories are entered into.
    description: str                                           # A description of the workflow.
    entity_type: str                                           # A string description of this resource.
    id: int                                                    # The unique ID of the Workflow.
    name: str                                                  # The name of the workflow.
    project_ids: List[int]                                     # An array of IDs of projects within the Workflow.
    states: List[WorkflowState]                                # A map of the states in this Workflow.
    team_id: int                                               # The ID of the team the workflow belongs to.
    updated_at: datetime.datetime                              # The date the Workflow was updated.

class Team(TypedDict, total=False):                                                                                 
    """Group of Projects with the same Workflow."""                                                                                 
    created_at: datetime.datetime                              # The time/date the Team was created.
    description: str                                           # The description of the Team.
    entity_type: str                                           # A string description of this resource.
    id: int                                                    # The unique identifier of the Team.
    name: str                                                  # The name of the Team.
    position: int                                              # A number representing the position of the Team in relation to every other Team within the Organization.
    project_ids: List[int]                                     # An array of IDs of projects within the Team.
    updated_at: datetime.datetime                              # The time/date the Team was last updated.
    workflow: Workflow                                         # Details of the workflow associated with the Team.