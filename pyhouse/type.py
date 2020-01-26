from enum import Enum
from typing import List, TypedDict
import datetime

class Entity(TypedDict, total=False):
    id: int
    entity_type: str
    created_at: datetime.datetime
    updated_at: datetime.datetime


##############
# Categories #
##############
class CategoryType(str, Enum):
    MILESTONE = "milestone"

class Category(Entity):
    """A Category can be used to associate Milestones."""
    archived: bool
    color: str
    external_id: str
    name: str
    type: CategoryType

class CategoryCreateRequired(TypedDict, total=False):
    name: str
    type: CategoryType

class CategoryCreate(CategoryCreateRequired):
    color: str
    external_id: str

class CategoryUpdate(TypedDict, total=False):
    archived: bool
    color: str
    name: str

#########
# Files #
#########
class File(Entity):
    """A File is any document uploaded to your Clubhouse. Files attached from a third-party service can be accessed using the Linked Files endpoint."""
    content_type: str
    description: str
    external_id: str
    filename: str
    group_mention_ids: List[str]
    member_mention_ids: List[str]
    mention_ids: List[str]
    name: str
    size: int
    story_ids: List[int]
    thumbnail_url: str
    uploader_id: str
    url: str


##########
# Labels #
##########
class LabelStats(TypedDict, total=False):
    """A group of calculated values for this Label."""
    num_epics: int
    num_points_completed: int
    num_points_in_progress: int
    num_points_total: int
    num_stories_completed: int
    num_stories_in_progress: int
    num_stories_total: int
    num_stories_unestimated: int

class Label(Entity):
    """A Label can be used to associate and filter Stories and Epics, and also create new Workspaces."""
    archived: bool
    color: str
    description: str
    external_id: str
    name: str
    stats: LabelStats

class LabelCreate(Entity):
    color: str
    description: str
    external_id: str
    name: str


################
# Linked-Files #
################
class LinkedFile(Entity):
    """Linked files are stored on a third-party website and linked to one or more Stories. Clubhouse currently supports linking files from Google Drive, Dropbox, Box, and by URL."""
    content_type: str
    description: str
    group_mention_ids: List[str]
    member_mention_ids: List[str]
    mention_ids: List[str]
    name: str
    size: int
    story_ids: List[int]
    thumbnail_url: str
    type: str
    uploader_id: str
    url: str


###########
# Stories #
###########
class ExternalTicket(TypedDict, total=False):
    """A External Ticket allows you to create a link between an external system, like Zendesk, and a Clubhouse story."""
    epic_ids: List[int]
    external_id: str
    external_url: str
    id: str
    story_ids: List[int]

class ExternalTicketCreate(TypedDict, total=False):
    external_id: str
    external_url: str

class StoryContentsTasks(TypedDict, total=False):
    """A task connected to a story."""
    complete: bool
    description: str
    external_id: str
    owner_ids: List[str]
    position: int

class EntityTemplateTask(TypedDict, total=False):
    """Request parameters for specifying how to pre-populate a task through a template."""
    complete: bool
    description: str
    external_id: str
    owner_ids: List[str]

class StoryContents(TypedDict, total=False):
    """A container entity for the attributes this template should populate."""
    deadline: datetime.datetime
    description: str
    entity_type: str
    epic_id: int
    estimate: int
    external_tickets: List[ExternalTicket]
    files: List[File]
    follower_ids: List[str]
    iteration_id: int
    labels: List[Label]
    linked_files: List[LinkedFile]
    name: str
    owner_ids: List[str]
    project_id: int
    story_type: str
    tasks: List[StoryContentsTasks]
    workflow_state_id: int

class StoryContentsCreate(TypedDict, total=False):
    deadline: datetime.datetime
    description: str
    entity_type: str
    epic_id: int
    estimate: int
    external_tickets: List[ExternalTicketCreate]
    files: List[File]
    follower_ids: List[str]
    iteration_id: int
    labels: List[LabelCreate]
    linked_files: List[LinkedFile]
    name: str
    owner_ids: List[str]
    project_id: int
    story_type: str
    tasks: List[EntityTemplateTask]
    workflow_state_id: int


####################
# Entity-Templates #
####################
class EntityTemplate(Entity):
    """An entity template can be used to prefill various fields when creating new stories."""
    author_id: str
    last_used_at: datetime.datetime
    name: str
    story_contents: StoryContents

class EntityTemplateCreateRequired(Entity):
    name: str
    story_contents: StoryContentsCreate

class EntityTemplateCreate(EntityTemplateCreateRequired):
    author_id: str

class EntityTemplateUpdate(TypedDict, total=False):
    name: str
    story_contents: StoryContentsCreate

##############
# Milestones #
##############
class MilestoneStats(TypedDict, total=False):
    """A group of calculated values for this Milestone."""
    average_cycle_time: int
    average_lead_time: int

class Milestone(Entity):
    """A Milestone is a collection of Epics that represent a release or some other large initiative that your organization is working on."""
    categories: List[Category]
    completed: bool
    completed_at: datetime.datetime
    completed_at_override: datetime.datetime
    description: str
    name: str
    position: int
    started: bool
    started_at: datetime.datetime
    started_at_override: datetime.datetime
    state: str
    stats: MilestoneStats
