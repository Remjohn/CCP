from typing import TypedDict, Annotated, List, Optional, Dict, Any
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage


class UserProfile(TypedDict):
    id: str
    username: Optional[str]
    first_name: Optional[str]
    role: str  # 'user', 'coach', or 'admin'
    coach_id: Optional[str]  # Links users to their coach
    identity_pillar: Optional[str]
    capacity_score: Optional[int]


class CoachConfig(TypedDict):
    """Per-coach configuration loaded from coach_configs table."""
    coach_name: str
    interview_day: str
    ideas_day: str
    recording_day: str
    timezone: str
    content_format: str  # 'tierlist', 'rating', 'mixed', 'auto'
    ideas_per_week: int
    preferred_archetypes: List[str]
    project_root: Optional[str]


class ContentIdea(TypedDict):
    """A single generated content idea."""
    title: str
    description: str
    format: str  # 'tierlist' or 'rating'
    archetype: str
    estimated_duration: str


class AgentState(TypedDict):
    # Conversation history (standard LangGraph)
    messages: Annotated[List[BaseMessage], add_messages]

    # User/Coach identity
    user_id: int
    user_profile: Optional[UserProfile]
    role: str  # 'user' or 'coach' — determines which subgraph to run

    # Processing State
    buffer: List[dict]  # Raw buffered messages from Redis

    # ── Context Extraction (Story 21.5) ──
    context_extraction: Optional[Dict[str, Any]]  # Aria's ContextExtraction output

    # Flags
    is_processing: bool

    # ── Coach-Specific State ──
    coach_config: Optional[CoachConfig]
    current_week: Optional[str]  # ISO week e.g., '2026-W08'

    # Content workflow
    weekly_themes: Optional[List[Dict[str, Any]]]  # From dynamic_content_themes.json
    generated_ideas: Optional[List[ContentIdea]]
    selected_idea_index: Optional[int]  # Which idea the coach picked
    recording_prep_url: Optional[str]  # Hosted recording page URL

    # Voice note processing
    transcription: Optional[str]  # Latest transcribed voice note
    extracted_themes: Optional[List[str]]  # Themes from voice note

    # ── User Monitoring State (coach sees this) ──
    monitored_users: Optional[List[Dict[str, Any]]]  # Users requiring attention
    alert_type: Optional[str]  # 'inactivity', 'crisis', 'milestone'

