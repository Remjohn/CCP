"""
CCP FR18 Psychological Routing Brief Generator — Payload Masking Library (Unit 2)
Static string templates for payload_masking_instruction keyed to mood_state_primary.

Spec reference: FR18_Psychological_Routing_Brief_Tech_Spec.md
                §4 Stage 3 Step 1: "Dynamically fetch the appropriate
                  payload_masking_instruction string based on mood_state_primary."
                §Testing Strategy: "Payload Masking String Test: Trigger Escape mode.
                  Retrieve the final generation prompt payload. Use regex matching to verify
                  the explicit literal string 'The truth is the punchline, not the lesson'
                  is present in the prompt context window."
                §5 Output Schema example: Escape mode instruction quoted verbatim.
                §Technical Decisions: "The generator outputs a literal
                  payload_masking_instruction string that is directly glued into the
                  Emilio prompt to force structural Trojan Horse behavior."

The Escape instruction string MUST contain the literal:
  "The truth is the punchline, not the lesson."
(Spec §5 Output Schema example + §Testing Strategy regex assertion.)
"""

from src.ccp.models.psych_routing_models import MoodStatePrimary


# ─── Payload Masking Instruction Library ─────────────────────────────────────
# One instruction per MoodStatePrimary value.
# These strings are injected verbatim into the Emilio generation prompt.
# They force structural Trojan Horse delivery — payload arrives through the vehicle.

PAYLOAD_MASKING_INSTRUCTIONS: dict[MoodStatePrimary, str] = {

    MoodStatePrimary.ESCAPE: (
        "You are writing in ESCAPE collision mode. "
        "The L3 payload must arrive through the vehicle's natural resolution. "
        "The audience must feel entertained BEFORE they feel seen. "
        "Never signal the transition from vehicle to payload. "
        "The truth is the punchline, not the lesson."
    ),

    MoodStatePrimary.DISCOVERY: (
        "You are writing in DISCOVERY expansion mode. "
        "The L3 payload must arrive as an earned insight — never asserted, always revealed. "
        "Build curiosity first; answer only what the reader is already leaning toward. "
        "The audience must feel competent for seeing what they see. "
        "The discovery belongs to them, not to you."
    ),

    MoodStatePrimary.STATUS: (
        "You are writing in STATUS activation mode. "
        "The L3 payload must arrive through social proof and aspirational contrast. "
        "Surface the gap between where they are and where the observed outcome sits. "
        "The audience must feel the pull of upward comparison before the message lands. "
        "Identity comes before instruction — who they are becoming precedes what to do."
    ),

    MoodStatePrimary.PROCESSING: (
        "You are writing in PROCESSING depth mode. "
        "The L3 payload must arrive as a companion to meaning-making, not as a conclusion. "
        "The audience is in contemplative space — meet them there before you move them. "
        "Heavy truths require relational scaffolding. "
        "The insight lands only after the reader feels held."
    ),
}


def get_payload_masking_instruction(mood_state: MoodStatePrimary) -> str:
    """Retrieve the payload masking instruction string for a given mood state.

    Spec §4 Stage 3 Step 1: "Dynamically fetch the appropriate
    payload_masking_instruction string based on mood_state_primary."

    Args:
        mood_state: The primary mood state for this compilation slot.

    Returns:
        Literal instruction string for direct injection into the Emilio prompt.

    Raises:
        KeyError: If the mood state is not registered in the library.
                  (All four MoodStatePrimary values MUST be registered — this
                   should never raise in production.)
    """
    return PAYLOAD_MASKING_INSTRUCTIONS[mood_state]
