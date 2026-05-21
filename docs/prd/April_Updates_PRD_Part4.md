# Product Requirements Document: April Updates — Sovereign Telegram Mini App Ecosystem

**Status:** In Progress (Part 4 - Technical Deep Dive & Schemas)

---

## 9. Data Schemas & API Contracts

To ensure absolute determinism across the 48-hour launch, the data structures connecting the Next.js Mini App, the FastAPI Gateway, and the backend Supabase/Redis instances must be strictly defined. Ambiguity in these JSON structures will crash the JIT compiler.

### 9.1 The WebRTC Roleplay Biometric Payload (FR-APR-05)
When a 1440-second Roleplay session concludes, the Pipecat Modal instance does not merely send a text summary. It must inject a structured biometric analysis into the *existing* `cbcs_interaction_logs` table in Supabase. This ensures the CPSC (Sales Engine) can instantly read roleplay performance without requiring new database queries.

**Schema (JSONB format for `interaction_metadata` column):**
```json
{
  "module_type": "webRtc_roleplay",
  "room_id": "dl_x789_alpha",
  "duration_seconds": 1440,
  "termination_reason": "scarcity_timeout",
  "biometric_score": {
    "interrupt_frequency": 4,
    "wpm_average": 145,
    "mood_state_resonance_compliance": 0.88,
    "objection_handling_flag": "PASSED"
  },
  "opponent_id": "external_guest_55",
  "ai_moderator_interventions": 2
}
```

### 9.2 Trivianar Redis Fast-Queue Schema (FR-APR-06)
During a live Trivianar, 5,000 users clicking answers generates a massive UDP flood. The React Native Mini App sends this payload via WebSocket to FastAPI, which executes an `LPUSH` into Redis.

**Schema (WebSocket Payload -> Redis `LPUSH`):**
```json
{
  "event_type": "TRIVIANAR_SUBMISSION",
  "data": {
    "room_id": "tv_epoch_101",
    "question_id": "q_04",
    "user_id": "telegram_uid_998877",
    "selected_answer_id": "ans_b",
    "reaction_time_ms": 1204,
    "timestamp_utc": "2026-05-02T20:45:00Z"
  }
}
```
*Architecture Note:* A Celery worker (`trivianar_sweep.py`) pops these payloads every 500ms, calculates the aggregate percentages (e.g., "45% chose A, 55% chose B"), and broadcasts the updated `TRIVIANAR_STATE` back to the active WebSockets to trigger DOM re-renders in the Next.js shell.

### 9.3 Speaker Audit Output Specification (FR-APR-03)
The top-of-funnel acquisition engine must return a brutal, mathematically precise critique of the coach's video submission. 

**Schema (Audit Report Payload):**
```json
{
  "audit_id": "aud_001_sigma",
  "target_video_url": "https://youtube.com/watch?v=...",
  "biometric_analysis": {
    "filler_word_density_percent": 18.4,
    "pacing_decay_variance": "high",
    "eye_contact_break_frequency": 12
  },
  "psychological_routing_suggestion": "Escape Mode / Downward Comparison",
  "content_trinity_preview_urls": [
    "s3://ccp/previews/short_watermarked.mp4",
    "s3://ccp/previews/carousel_watermarked.pdf",
    "s3://ccp/previews/meme_watermarked.png"
  ],
  "tripwire_checkout_url": "https://pay.stripe.com/buy/..."
}
```

### 9.4 The 28-Command Slash Architecture (FR-APR-09)
The `InteractComp` agent boundary is expanded. Instead of relying purely on natural language understanding, users can trigger exact deterministic workflows using Telegram slash commands. The FastAPI router maps these directly to Celery tasks.

**Core Command Mapping Table:**
| Command | Caller | Action Triggered | Latency Target |
|---|---|---|---|
| `/start_challenge` | Client | Initializes FR-APR-02 state machine for the user. | < 200ms |
| `/audit_me [url]` | Coach | Kicks off FR-APR-03 biometric video analysis. | < 500ms (Async Return) |
| `/trivianar_join` | Client | Opens Next.js WebApp, establishes WS handshake. | < 100ms |
| `/roleplay_init` | Coach | Boots the Modal.com Pipecat instance, creates Daily.co room. | < 1500ms |
| `/billing_status` | Coach | Queries Stripe API + Redis limits, returns current usage. | < 300ms |
| `/export_trinity` | Coach | Fires FR-APR-10 limits check. If passed, triggers generation. | < 400ms |

### 9.5 The Redis Export Limiter Architecture (FR-APR-01 & FR-APR-10)
To enforce the "No Credit Loopholes" rule, the export limiter must be atomically secure.

**Redis Keyspace Structure:**
*   `export_limits:{coach_id}:{iso_week}` -> **Hash** (Tracks the 4/week limit per format).
*   `active_clients:{coach_id}:{iso_month}` -> **Set** (Tracks unique Telegram IDs for the $3.90/user B2B2C charge).
*   `trivianar_state:{room_id}` -> **JSON** (Holds the current question, timer, and aggregate answers for the live game).

**The HINCRBY Transaction Block (`redis_limits.py`):**
Whenever a coach requests a visual asset or script export, FastAPI executes the following Lua script or `MULTI/EXEC` block:
```python
async def check_and_increment_limit(coach_id: str, format_type: str) -> bool:
    # 1. WATCH the key to prevent race conditions
    # 2. HGET total_weekly_count
    # 3. HGET {format_type}
    # 4. IF total >= 8 OR format >= 4 -> UNWATCH, Return False
    # 5. MULTI
    # 6. HINCRBY total_weekly_count 1
    # 7. HINCRBY {format_type} 1
    # 8. EXEC -> Return True
```

### 9.6 DSPy & Pydantic Boundaries (FR-APR-08)
To prevent the "Statistical Centroid Failure," LLMs must not make routing decisions. They must only execute defined tasks and return structured data.

**The DSPy Signature Example (For generating a Meme Hook):**
```python
import dspy
from pydantic import BaseModel, Field

class MemeHookSchema(BaseModel):
    setup_text: str = Field(max_length=40)
    punchline_text: str = Field(max_length=30)
    v_code: str = Field(description="Violation Type (V1-V4)")
    r_code: str = Field(description="Resolution Domain (R1-R3)")

class GenerateMemeHook(dspy.Signature):
    """Generates a concise, psychologically targeted meme hook based on the active Context Premise."""
    context_premise = dspy.InputField()
    target_mood_state = dspy.InputField()
    
    # The output MUST conform to the Pydantic schema
    output: MemeHookSchema = dspy.OutputField()
```
*Architectural Law:* If the `output` does not pass Pydantic validation, the DSPy `Assert` framework forces the LLM to retry up to 3 times with the validation error appended to the prompt. If it fails 3 times, the pipeline throws a `PydanticValidationError` and triggers the `DamageControl` Pi Extension, rather than passing hallucinated data to the next step.
