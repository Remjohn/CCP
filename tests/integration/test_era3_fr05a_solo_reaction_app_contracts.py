from src.ccp.models.reaction_solo_models import (
    SoloReactionLaunchPayload,
    SoloRecordingViewState,
    SoloScoreRevealPayload,
    SoloDeploymentDecision
)

class TestSoloContracts:
    def test_launch_payload_uses_startapp_react_solo(self):
        assert SoloReactionLaunchPayload.__fields__["startapp"].default == "react_solo"

    def test_recording_state_contains_upload_ticket(self):
        assert "upload_ticket" in SoloRecordingViewState.__fields__

    def test_score_reveal_payload_requires_approval_before_deploy(self):
        assert SoloScoreRevealPayload.__fields__["approval_required"].default is True

    def test_redemption_branch_contains_no_cmf_success_state(self):
        assert hasattr(SoloDeploymentDecision, "redemption_required")
