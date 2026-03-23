"""
CCP Story Archive Approval Gate — FR1 Unit 5
DEP-PROTO-016: Coach Story Archive Extraction & Operator Approval

Spec reference: FR1 Tech Spec §Phase 0, Step 0-B
Architecture reference: CCP_Technical_Architecture.md §3.1

Story extraction via 5-category Telegram interview.
Hartian 5-element schema enforcement.
Operator approve/reject per story — never automatic.
Gate: ≥3 approved stories across ≥2 story types.

Tagging: story_type, mechanism_tag, arc_phase_fit, cral_moment_fit, emotional_register.

C-11 Persona Masking Gate: no agent names in model-facing prompts.
"""

import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from src.ccp.models.v5_models import (
    CoachStoryEntry,
    CoachStoryArchive,
    HartianStorySchema,
    StoryType,
    HumorMechanismTag,
)
from src.ccp.core.receipt_chain import ReceiptChain


# CRAL Phase identifiers
CRAL_PHASES = ["M1_ATTENTION", "M2_AUTHORITY", "M3_RESONANT", "M4_RESONANT", "M5_CONVERSION"]

# Arc phases
ARC_PHASES = ["origin", "struggle", "turning_point", "breakthrough", "integration"]

# Emotional registers (tone fingerprints)
EMOTIONAL_REGISTERS = [
    "inspirational", "vulnerable", "provocative", "instructional",
    "empathetic", "confrontational", "celebratory"
]


# DEP-PROTO-016 interview prompts — one per story type category
# C-11: no agent names in model-facing text
_STORY_INTERVIEW_QUESTIONS: dict[str, dict] = {
    "personal_transformation": {
        "type": StoryType.PERSONAL_TRANSFORMATION,
        "question": (
            "Tell me about a time you personally transformed — "
            "a moment when you fundamentally changed how you see yourself or the world. "
            "What happened, what shifted inside you, and what became possible after?"
        ),
    },
    "professional_failures": {
        "type": StoryType.PROFESSIONAL_FAILURE,
        "question": (
            "Tell me about a significant professional failure or setback — "
            "a time something didn't work, a client you lost, a decision that cost you. "
            "What actually happened, and what did you learn that you couldn't have learned any other way?"
        ),
    },
    "client_breakthrough": {
        "type": StoryType.CLIENT_BREAKTHROUGH,
        "question": (
            "Tell me about a client breakthrough moment — "
            "a specific client (no names needed) who had a breakthrough that moved you. "
            "What was the moment? What did it tell you about your coaching?"
        ),
    },
    "inflection_points": {
        "type": StoryType.INFLECTION_POINT,
        "question": (
            "Tell me about a decisive inflection point in your career — "
            "a fork in the road where you chose a harder, less obvious path. "
            "What was the choice? What made it hard? What did the choice reveal?"
        ),
    },
    "collective_wound": {
        "type": StoryType.COLLECTIVE_WOUND,
        "question": (
            "Tell me about a wound your audience shares — "
            "something your people have collectively experienced that shaped who they are. "
            "This could be an industry failure, a generational experience, or a cultural moment. "
            "How does it show up in your clients' lives and in your coaching?"
        ),
    },
}


_HARTIAN_ANALYSIS_PROMPT = """You are a story structure analyst trained in the Hartian coaching narrative framework.

Analyze the following coach story and extract the 5-element Hartian story schema.

COACH STORY:
{story_text}

STORY TYPE: {story_type}

Extract and return ONLY valid JSON with this exact structure:
{{
  "protagonist_status": "Description of who the protagonist is in this story (the coach, a client, or a collective)",
  "moment_of_contact": "The specific moment when the problem/challenge became undeniable",
  "internal_shift": "What shifted internally — the realization, decision, or recognition",
  "outcome": "What became possible or different after the shift",
  "tribal_markers": ["phrase or reference that signals cultural belonging", "..."],
  "mechanism_tag": "mechanism that makes this story work (identity_mirror|wound_activation|aspiration_bridge|enemy_unification|legacy_frame)",
  "arc_phase_fit": "{arc_phase_options}",
  "cral_moment_fit": "{cral_options}",
  "emotional_register": "{emotional_options}"
}}

Rules:
- tribal_markers: 2-5 specific phrases, references, or cultural signals in the story
- mechanism_tag: pick ONE of the listed options that best describes the story's primary mechanism
- arc_phase_fit: pick ONE arc phase where this story is most powerful
- cral_moment_fit: pick ONE CRAL phase where this story best serves the audience
- emotional_register: pick ONE that describes the dominant tone
- Return only the JSON object, no commentary
"""


class StoryArchiveApprovalGate:
    """DEP-PROTO-016: Coach Story Archive Extraction & Operator Approval.

    Spec Step 0-B:
    - 'Morgan dispatches 5-category Telegram interview'
    - 'Operator reviews all submitted stories for Hartian schema compliance'
    - 'Stories are NOT written automatically — the Agent structures, the operator approves'
    - Gate: '≥3 approved stories across ≥2 story types'

    The Hartian schema enforces:
    - protagonist_status
    - moment_of_contact
    - internal_shift
    - outcome
    - tribal_markers
    """

    def __init__(
        self,
        coach_id: str,
        coach_acronym: str,
        coach_dir: Path,
        receipt_chain: ReceiptChain,
        gemini_api_key: Optional[str] = None,
    ):
        import os
        self.coach_id = coach_id
        self.coach_acronym = coach_acronym.upper()
        self.coach_dir = coach_dir
        self.receipt_chain = receipt_chain
        self.api_key = gemini_api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY required for story archive extraction")

    def build_interview_dispatch_message(self) -> str:
        """Build the Telegram interview dispatch for all 5 story categories.

        Spec: 'Morgan dispatches 5-category Telegram interview'

        Returns:
            Formatted Telegram message to send to the coach.
        """
        lines = [
            "📖 *Story Archive Interview — 5 Categories*",
            "",
            "To build your authentic story library, please answer each of the following "
            "5 prompts. Take your time — these become the foundation of your voice.",
            "",
            "Reply to each numbered question separately. Start with *Story 1:*",
            "",
        ]
        for i, (key, config) in enumerate(_STORY_INTERVIEW_QUESTIONS.items(), 1):
            story_type_label = config["type"].value.replace("_", " ").title()
            lines.append(f"*Story {i}: {story_type_label}*")
            lines.append(config["question"])
            lines.append("")

        lines.append("Reply when you have answered all 5 (or as many as you can). "
                     "There is no minimum length — authenticity matters more than length.")
        return "\n".join(lines)

    async def analyze_story(
        self,
        story_text: str,
        story_type: StoryType,
    ) -> CoachStoryEntry:
        """Apply Hartian schema analysis to a raw story.

        Spec: 'Hartian 5-element schema enforcement'

        The result has operator_approved=False until confirm_stories() is called.

        Args:
            story_text: Raw story text from the coach.
            story_type: The story type category for this story.

        Returns:
            CoachStoryEntry with Hartian schema populated, pending operator approval.
        """
        from google import genai

        prompt = _HARTIAN_ANALYSIS_PROMPT.format(
            story_text=story_text,
            story_type=story_type.value,
            arc_phase_options="|".join(ARC_PHASES),
            cral_options="|".join(CRAL_PHASES),
            emotional_options="|".join(EMOTIONAL_REGISTERS),
        )

        client = genai.Client(api_key=self.api_key)
        response = await client.aio.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
        )

        response_text = response.text.strip()
        if response_text.startswith("```"):
            response_text = response_text.split("\n", 1)[1]
            response_text = response_text.rsplit("```", 1)[0]

        analysis = json.loads(response_text)

        # Build Hartian schema
        hartian = HartianStorySchema(
            protagonist_status=analysis.get("protagonist_status", ""),
            moment_of_contact=analysis.get("moment_of_contact", ""),
            internal_shift=analysis.get("internal_shift", ""),
            outcome=analysis.get("outcome", ""),
            tribal_markers=analysis.get("tribal_markers", []),
        )

        # Build humor mechanism tag — AC8: empty architectures → explicit no_applicable_mechanism
        architectures = analysis.get("humor_architectures_fired", [])
        humor_tag = HumorMechanismTag(
            architectures_fired=architectures,
            reason=analysis.get("humor_reason") if architectures else "no_applicable_mechanism",
        )

        story_id = f"STORY-{self.coach_acronym}-{story_type.value[:4].upper()}-{uuid.uuid4().hex[:8].upper()}"
        entry = CoachStoryEntry(
            story_id=story_id,
            coach_id=self.coach_id,
            story_type=story_type,
            story_text=story_text,
            hartian_schema=hartian,
            mechanism_tag=analysis.get("mechanism_tag", "identity_mirror"),
            arc_phase_fit=analysis.get("arc_phase_fit", "origin"),
            cral_moment_fit=analysis.get("cral_moment_fit", "M2_AUTHORITY"),
            emotional_register=analysis.get("emotional_register", "empathetic"),
            humor_mechanism_tag=humor_tag,
            operator_approved=False,  # Never automatic — spec mandate
        )

        return entry

    async def run_full_extraction(
        self,
        raw_stories: dict[str, str],
    ) -> CoachStoryArchive:
        """Run full story archive extraction across all submitted stories.

        Args:
            raw_stories: Dict mapping story type key (e.g., 'personal_transformation')
                         to the raw story text submitted by the coach.

        Returns:
            CoachStoryArchive with all entries pending operator approval.
        """
        entries: list[CoachStoryEntry] = []

        for category_key, story_text in raw_stories.items():
            if not story_text or not story_text.strip():
                continue
            config = _STORY_INTERVIEW_QUESTIONS.get(category_key)
            if config is None:
                continue
            story_type: StoryType = config["type"]
            entry = await self.analyze_story(story_text, story_type)
            entries.append(entry)

        archive_id = f"ARC-{self.coach_acronym}-{uuid.uuid4().hex[:8].upper()}"
        archive = CoachStoryArchive(
            archive_id=archive_id,
            coach_id=self.coach_id,
            entries=entries,
            status="in_progress",
        )

        # Save pending review
        archive_path = self.coach_dir / "config" / "story_archive.json"
        archive_path.write_text(archive.model_dump_json(indent=2), encoding="utf-8")

        return archive

    def build_operator_review_message(self, archive: CoachStoryArchive) -> str:
        """Build the Telegram review message for operator approval of stories.

        Spec: 'Operator reviews all submitted stories for Hartian schema compliance'

        Agent names NOT included (C-11 compliance).
        """
        lines = [
            f"📚 *Story Archive — Operator Review Required*",
            f"Coach: {self.coach_acronym} | Archive ID: `{archive.archive_id}`",
            f"Stories extracted: {len(archive.entries)}",
            "",
            "Review each story below. Reply with entry IDs to approve/reject.",
            "Format: `APPROVE_STORY: [story_id_1, story_id_2, ...]`",
            "Format: `REJECT_STORY: [story_id_1, ...]`",
            "",
            f"Gate requirement: ≥3 approved stories across ≥2 story types.",
            "",
        ]

        for entry in archive.entries:
            story_type_label = entry.story_type.value.replace("_", " ").title()
            lines.append(f"*{story_type_label}* | `{entry.story_id}`")
            lines.append(f"Arc phase: {entry.arc_phase_fit} | CRAL: {entry.cral_moment_fit}")
            lines.append(f"Mechanism: {entry.mechanism_tag} | Register: {entry.emotional_register}")
            lines.append(f"Protagonist: {entry.hartian_schema.protagonist_status}")
            lines.append(f"Moment: {entry.hartian_schema.moment_of_contact}")
            lines.append(f"Shift: {entry.hartian_schema.internal_shift}")
            lines.append(f"Outcome: {entry.hartian_schema.outcome}")
            if entry.hartian_schema.tribal_markers:
                lines.append(f"Tribal markers: {', '.join(entry.hartian_schema.tribal_markers[:3])}")
            preview = entry.story_text[:200] + "..." if len(entry.story_text) > 200 else entry.story_text
            lines.append(f"Story preview: {preview}")
            lines.append("")

        return "\n".join(lines)

    def confirm_stories(
        self,
        archive: CoachStoryArchive,
        approved_story_ids: list[str],
        rejected_story_ids: Optional[list[str]] = None,
    ) -> CoachStoryArchive:
        """Process operator approval/rejection of story archive entries.

        Spec: 'Stories are NOT written automatically — the Agent structures,
        the operator approves'

        Args:
            archive: The CoachStoryArchive to update.
            approved_story_ids: Story IDs the operator approved.
            rejected_story_ids: Story IDs the operator rejected.

        Returns:
            Updated CoachStoryArchive with operator decisions applied.
        """
        approved_ids = set(approved_story_ids)
        rejected_ids = set(rejected_story_ids or [])
        now = datetime.now(timezone.utc)

        for entry in archive.entries:
            if entry.story_id in approved_ids:
                entry.operator_approved = True
                entry.approved_at = now
            elif entry.story_id in rejected_ids:
                entry.operator_approved = False

        # Check gate
        passes = archive.passes_proto016_gate()
        if passes:
            archive.status = "gate_passed"
            archive.updated_at = now
        else:
            archive.status = "in_progress"
            archive.updated_at = now

        # Persist
        archive_path = self.coach_dir / "config" / "story_archive.json"
        archive_path.write_text(archive.model_dump_json(indent=2), encoding="utf-8")

        return archive

    def load_archive(self) -> Optional[CoachStoryArchive]:
        """Load the current story archive from local config."""
        archive_path = self.coach_dir / "config" / "story_archive.json"
        if not archive_path.exists():
            return None
        data = json.loads(archive_path.read_text(encoding="utf-8"))
        return CoachStoryArchive.model_validate(data)


class StoryArchiveGateError(Exception):
    """Raised when story archive does not meet DEP-PROTO-016 gate."""
    def __init__(self, approved_count: int, story_type_count: int):
        self.approved_count = approved_count
        self.story_type_count = story_type_count
        super().__init__(
            f"STORY_ARCHIVE_GATE_FAILED: {approved_count} approved stories "
            f"across {story_type_count} story types. "
            f"Required: ≥3 stories across ≥2 types."
        )
