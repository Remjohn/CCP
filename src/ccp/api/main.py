"""
CCP FastAPI Application
Main entry point for the coach instance API server.

Handles:
- Telegram webhook (CBCS client interactions)
- Notion webhook (status change triggers)
- Sacred Audio upload endpoint
- Health check and diagnostics
"""

import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="CCP - Conscious Coaching Platform",
    description="Coach instance API server for the Conscious Coaching Platform",
    version="1.0.0",
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
    return {
        "status": "healthy",
        "coach_acronym": os.getenv("COACH_ACRONYM", "UNKNOWN"),
        "version": "1.0.0",
    }


# Import and register route modules
from src.ccp.api.sacred_audio import router as sacred_audio_router
from src.ccp.api.telegram_webhook import router as telegram_router
from src.ccp.api.notion_webhook import router as notion_router
from src.ccp.api.canvas_api import router as canvas_router

app.include_router(sacred_audio_router, prefix="/api", tags=["Sacred Audio"])
app.include_router(telegram_router, prefix="/api", tags=["Telegram"])
app.include_router(notion_router, prefix="/api", tags=["Notion"])
app.include_router(canvas_router, prefix="/api", tags=["Canvas"])
