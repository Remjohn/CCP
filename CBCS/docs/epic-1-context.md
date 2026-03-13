# Epic 1: The Nervous System - Technical Context

## Architecture Overview
Epic 1 establishes the "Nervous System" of the CBCS, handling the high-speed ingestion of signals (messages) and the cognitive processing pipeline.

### Core Components
1.  **Ingress Layer (FastAPI)**:
    - **Role**: Receives webhooks from Telegram.
    - **Constraint**: Must respond with `200 OK` in < 200ms.
    - **Security**: Validates `X-Telegram-Bot-Api-Secret-Token`.

2.  **Buffering Layer (Redis)**:
    - **Role**: "Listening Window" buffer.
    - **Data Structure**: Redis List `buffer:{user_id}`.
    - **TTL**: 90 seconds (Silence Timer).

3.  **Cognitive Core (LangGraph)**:
    - **Role**: State machine for the conversation.
    - **States**: `Sleep`, `Priming`, `Listening`, `Analyzing`, `Strategizing`, `Speaking`.
    - **Persistence**: Supabase (`AsyncPostgresSaver`).

4.  **Perception Engine (Groq)**:
    - **Role**: Transcribes audio.
    - **Model**: Whisper Large v3.

## Implementation Details

### Directory Structure
```
backend/
├── main.py                 # FastAPI Entry Point
├── config.py               # Environment Variables
├── ingress.py              # Webhook Handlers
├── core/
│   ├── redis_client.py     # Redis Connection
│   ├── graph.py            # LangGraph Definition
│   └── state.py            # State Schemas
└── agents/
    └── perception/
        └── transcriber.py  # Groq Client
```

### Dependencies
- `fastapi`
- `uvicorn`
- `redis`
- `langgraph`
- `pydantic-ai`
- `groq`
- `supabase`

### Environment Variables
- `TELEGRAM_BOT_TOKEN`
- `TELEGRAM_SECRET_TOKEN`
- `REDIS_URL`
- `SUPABASE_URL`
- `SUPABASE_KEY`
- `GROQ_API_KEY`
