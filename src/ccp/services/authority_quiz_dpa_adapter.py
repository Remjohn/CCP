from typing import Any
from src.ccp.services.dpa_engine import DPAEngine, BrandHueAnalysis, OverrideMode, DPAResult
from src.ccp.models.reaction_authority_quiz_models import AuthorityQuizEscalationProfile, AuthorityQuizVisualPressureProjection

class AuthorityQuizDPAAdapter:
    def __init__(self, engine: DPAEngine):
        self.engine = engine
        
    async def resolve_with_escalation(
        self,
        coach_id: str,
        content_archetype: str,
        audience_mood_state: str = "",
        brand_hue_analysis: BrandHueAnalysis | None = None,
        override_mode: OverrideMode = OverrideMode.adaptive,
        identity_tokens: dict[str, Any] | None = None,
        escalation_profile: AuthorityQuizEscalationProfile | None = None,
    ) -> AuthorityQuizVisualPressureProjection:
        # Base resolution
        base_result = await self.engine.resolve(
            coach_id, content_archetype, audience_mood_state, brand_hue_analysis, override_mode, identity_tokens
        )
        
        level_index = 1
        border_emphasis = 0.0
        ambient_glow = 0.0
        
        # Apply escalation
        if escalation_profile:
            level_index = escalation_profile.level_index
            frac = escalation_profile.escalation_fraction
            border_emphasis = 1.0 * frac
            ambient_glow = 1.0 * frac
            
        return AuthorityQuizVisualPressureProjection(
            level_index=level_index,
            escalation_profile=escalation_profile,
            audience_mood_state=audience_mood_state or "neutral",
            background_primary=base_result.background_primary,
            background_secondary=base_result.background_secondary,
            accent=base_result.accent,
            border_emphasis=border_emphasis,
            ambient_glow_strength=ambient_glow
        )
