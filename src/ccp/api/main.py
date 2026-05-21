"""
CCP FastAPI Application
Main entry point for the coach instance API server.

Handles:
- Telegram webhook (CBCS client interactions)
- Notion webhook (status change triggers)
- Sacred Audio upload endpoint
- Primitive registry query and invalidation
- Health check and diagnostics
"""

import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    from src.ccp.services.primitive_registry_service import build_default_primitive_registry_service

    primitive_registry_service = build_default_primitive_registry_service()
    primitive_registry_service.warm_registry()
    app.state.primitive_registry_service = primitive_registry_service
    yield


app = FastAPI(
    title="CCP - Conscious Coaching Platform",
    description="Coach instance API server for the Conscious Coaching Platform",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring and Docker healthcheck."""
    registry_health = None
    primitive_registry_service = getattr(app.state, "primitive_registry_service", None)
    if primitive_registry_service is not None:
        registry_health = primitive_registry_service.health().model_dump(mode="json")
    return {
        "status": "healthy",
        "coach_acronym": os.getenv("COACH_ACRONYM", "UNKNOWN"),
        "version": "1.0.0",
        "primitive_registry": registry_health,
    }


# Import and register route modules
from src.ccp.api.sacred_audio import router as sacred_audio_router
from src.ccp.api.telegram_webhook import router as telegram_router
from src.ccp.api.primitive_registry_api import router as primitive_router
from src.ccp.api.solo_reaction_api import router as solo_reaction_router
from src.ccp.api.debate_with_jury_api import router as debate_router
from src.ccp.api.reaction_duel_api import router as reaction_duel_router
from src.ccp.api.reaction_tierlist_api import router as tierlist_router
from src.ccp.api.reaction_mirror_quiz_api import router as mirror_quiz_router
from src.ccp.api.reaction_blind_rank_api import router as blind_rank_router
from src.ccp.api.reaction_alphabet_api import router as alphabet_router
from src.ccp.api.reaction_elimination_api import router as elimination_router
from src.ccp.api.reaction_authority_quiz_api import router as authority_quiz_router
from src.ccp.api.reaction_ranking_quiz_api import router as ranking_quiz_router
from src.ccp.api.webinar_companion_api import router as webinar_companion_router
from src.ccp.api.onboarding_api import router as onboarding_router
from src.ccp.api.challenge_arena_api import router as challenge_arena_router
from src.ccp.api.experience_ladder_api import router as experience_ladder_router
from src.ccp.api.testimonial_api import router as testimonial_router
from src.ccp.api.score_viewer_api import router as score_viewer_router
from src.ccp.api.stealth_course_api import router as stealth_course_router
from src.ccp.api.sda_query_api import router as sda_query_router
from src.ccp.api.stripe_webhook import router as stripe_router
from src.ccp.api.billing_api import router as billing_router
from src.ccp.api.overlay_interaction_api import router as overlay_router
from src.ccp.api.archetype_runtime import router as archetype_runtime_router
from src.ccp.api.affine_studio_api import router as affine_studio_router
from src.ccp.api.conscious_editor_api import router as conscious_editor_router
from src.ccp.api.cmf_arc_render_api import router as cmf_arc_render_router
from src.ccp.api.voice_prompt_api import router as voice_prompt_router
from src.ccp.api.referral_api import router as referral_router
from src.ccp.api.phase0_intake import router as phase0_intake_router
from src.ccp.api.phase0_workspace import router as phase0_workspace_router
from src.ccp.api.phase0_audit import router as phase0_audit_router
from src.ccp.api.phase0_eval_cards import router as phase0_eval_cards_router
from src.ccp.api.phase0_commercial import router as phase0_commercial_router
from src.ccp.api.phase0_operator_console import router as phase0_operator_console_router
from src.ccp.api.phase0_campaign_workspace import router as phase0_campaign_workspace_router
from src.ccp.api.global_admin_api import router as global_admin_router


app.include_router(sacred_audio_router, prefix="/api", tags=["Sacred Audio"])
app.include_router(telegram_router, prefix="/api", tags=["Telegram"])
app.include_router(primitive_router, prefix="/api", tags=["Primitives"])
app.include_router(solo_reaction_router, prefix="/api", tags=["Reactions"])
app.include_router(debate_router, prefix="/api", tags=["Debates"])
app.include_router(reaction_duel_router, prefix="/api", tags=["Duels"])
app.include_router(tierlist_router, prefix="/api", tags=["Tierlist"])
app.include_router(mirror_quiz_router, prefix="/api", tags=["Mirror Quiz"])
app.include_router(blind_rank_router, prefix="/api", tags=["Blind Rank"])
app.include_router(alphabet_router, prefix="/api", tags=["Alphabet Challenge"])
app.include_router(elimination_router, prefix="/api", tags=["Last One Standing"])
app.include_router(authority_quiz_router, prefix="/api", tags=["Authority Quiz"])
app.include_router(ranking_quiz_router, prefix="/api", tags=["Ranking Quiz Co-Creation"])
app.include_router(webinar_companion_router, prefix="/api", tags=["Webinar Companion"])
app.include_router(onboarding_router, prefix="/api", tags=["Onboarding"])
app.include_router(challenge_arena_router, prefix="/api", tags=["Challenge Arena"])
app.include_router(experience_ladder_router, prefix="/api", tags=["Experience Ladder"])
app.include_router(testimonial_router, prefix="/api", tags=["Testimonial Builder"])
app.include_router(score_viewer_router, prefix="/api", tags=["Score Viewer"])
app.include_router(stealth_course_router, prefix="/api", tags=["Stealth Course"])
app.include_router(sda_query_router, prefix="/api", tags=["SDA Query"])
app.include_router(stripe_router, prefix="/api", tags=["Stripe Payments"])
app.include_router(billing_router, prefix="/api", tags=["Billing"])
app.include_router(overlay_router, prefix="/api", tags=["AR Overlay"])
app.include_router(archetype_runtime_router, prefix="/api", tags=["Archetype Runtime"])
app.include_router(affine_studio_router, prefix="/api", tags=["AFFiNE Studio"])
app.include_router(conscious_editor_router, prefix="/api", tags=["Conscious Editor"])
app.include_router(cmf_arc_render_router, prefix="/api", tags=["CMF Arc Render"])
app.include_router(voice_prompt_router, prefix="/api", tags=["Voice Prompt Engine"])
app.include_router(referral_router, prefix="/api", tags=["Silent Referral"])
app.include_router(phase0_intake_router, prefix="/api/phase0", tags=["Phase-0 Intake Console"])
app.include_router(phase0_workspace_router, prefix="/api/phase0", tags=["Phase-0 Workspace"])
app.include_router(phase0_audit_router, prefix="/api/phase0", tags=["Phase-0 Audit Intelligence"])
app.include_router(phase0_eval_cards_router, prefix="/api/phase0", tags=["Eval Card System"])
app.include_router(phase0_commercial_router, prefix="/api/phase0", tags=["Phase-0 Commercial Bridge"])
app.include_router(phase0_operator_console_router, prefix="/api/phase0", tags=["Phase-0 Operator Console"])
app.include_router(phase0_campaign_workspace_router, prefix="/api/phase0", tags=["Phase-0 Campaign Workspace"])
app.include_router(global_admin_router, prefix="/api", tags=["Global Admin Dashboard"])


