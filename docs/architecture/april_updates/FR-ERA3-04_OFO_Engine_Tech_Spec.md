# PRE-WORK LOG

1. **Protocol:** `docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md` — Read sections 2, 3, and 4.
2. **PRD Modules:** PRD-09 loaded. **PROOF:** "FR-ERA3-04 (OFO Engine): The Object-First Outreach engine that generates high-end proof assets as a Trojan Horse wedge for acquiring new high-value coaches (PRD-09)."
3. **Phase Epic:** `docs/architecture/april_updates/Phase5_Growth_Epics.md` loaded. **PROOF:** "**Given** an identified high-value coach target,"
4. **CBAR Audit:** `docs/architecture/cbar_audits/CBAR_Audit_Phase5_Growth.md` loaded. Mandates M-03 and M-04 confirmed and integrated.
5. **Primitives:** Checked `primitives/experience/`. **PROOF:** `id: EXP-TRS-004`, `name: Epic Meaning Framing (The Crusade Narrative)`. `id: EXP-PRG-001`, `name: Hook Cycle Velocity`. Banned `EXP-TRB-*` avoided.
6. **Backend Python Files:** Audited 3 services. **PROOF:** `ContentMachinePipeline.process_session(self, session_report: dict[str, Any], coach_id: str, coach_acronym: str = "CCH") -> ContentMachineResult`
7. **Test Files:** `test_cpsc_fr51_challenge_funnel.py` and `test_cbcs12_coping_invitation.py` reviewed to match section 10 testing patterns.

---

# FR-ERA3-04: OFO Engine (Object First Outreach) Technical Specification

## 1. Files Read

1. `docs/prd/modules/PRD_09_CPSC_Silent_Referral.md`
2. `docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md`
3. `docs/architecture/april_updates/Phase5_Growth_Epics.md`
4. `docs/architecture/cbar_audits/CBAR_Audit_Phase5_Growth.md`
5. `src/ccp/services/content_machine.py`
6. `src/ccp/services/trait_scoring_engine.py`
7. `src/ccp/services/abel_vcb_generator.py`
8. `primitives/experience/trust_branding/EXP-TRS-004.yaml`
9. `primitives/experience/progression_replay/EXP-PRG-001.yaml`

---

## 2. Overview

### 2.1 Problem
The Conscious Coaching Platform fundamentally relies on acquiring high-value coaches as its primary market wedge and future node network. Traditional cold-outreach methodologies (e.g., direct messaging via Instagram, email sequences, or generic PDF lead magnets) suffer from near-zero conversion rates because elite coaches are continuously inundated with generic SaaS pitches, agency offers, and automated bots. These high-value targets possess formidable ego defenses and are highly protective of their authority and brand identity. A standard SaaS trial, or a clinical critique of their existing content, immediately triggers these defenses—leading to instant bounces, reputational damage, and permanent loss of the prospect. The system requires an acquisition engine that deposits immense, undeniable value upfront without triggering the target's internal alarm systems.

### 2.2 Solution
The Object First Outreach (OFO) Engine acts as a highly sophisticated "Trojan Horse" acquisition strategy. Rather than aggressively pitching a software platform, the OFO Engine programmatically analyzes a high-value coach target's existing, publicly available content (such as a YouTube video or an Instagram Reel). It processes this content through the platform's proprietary Negative Metrics engine (`trait_scoring_engine.py`) and utilizes our media synthesis pipelines to automatically generate a premium 4-Asset Proof Package. This package is delivered to the target entirely for free. Crucially, it is framed not as a clinical critique or a sales pitch, but as a defense of their legacy against "algorithmic compression"—a narrative that aligns completely with their internal worldview. By providing undeniable proof of the platform's intelligence through a highly personalized, high-production-value asset, we bypass the target's ego defense. This trust-transfer mechanism invites them to interact natively within Telegram, seamlessly initiating the Hook Cycle and drawing them into the $0 Proof Layer.

### 2.3 Scope
This technical specification details the comprehensive, end-to-end architecture for the OFO Engine. It covers:
- The programmatic ingestion, normalization, and processing of a coach's public content (audio/video extraction).
- The complex orchestration of the 4-Asset Proof Package generation (comprising a Carousel, a Storytelling Video, a fast-paced Reels Explainer, and the apex Animated Video Audit).
- The strict, programmatic enforcement of the Animated Video Audit's framing using the Crusade Narrative (Epic Meaning Framing).
- The delivery mechanism via the Telegram Bot API.
- The immediate inline transition into the Stealth Course Accountability Hook, capturing the user within a single, unbroken session to satisfy the velocity requirements of the Hook Cycle.

---

## 3. Context for Development

### 3.1 Architecture Traceability (DEP-IDs)

| DEP-ID | Component | Description |
|---|---|---|
| DEP-OFO-001 | OFO Orchestrator | The main pipeline that orchestrates content ingestion, parallel processing, and asynchronous asset generation across multiple microservices. |
| DEP-OFO-002 | Crusade Narrative Fitter | Textual processor module that wraps raw biometric score output in Epic Meaning framing using strict regular expressions and LLM templating. |
| DEP-OFO-003 | OFO Delivery Agent | The Telegram-bound conversational agent responsible for the chronological delivery of the asset package and the inline capture. |
| DEP-OFO-004 | Stealth Course Transition | The state machine logic moving a target from passive asset consumption to their first active accountability challenge. |

### 3.2 Existing Backend Integration

The OFO Engine operates as a **NEW** top-level orchestration service, but it heavily **CONSUMES** existing, validated Era 3 components to guarantee architectural consistency and prevent duplicated business logic:
- `src/ccp/services/content_machine.py`: Used to extract micro-content pieces from the raw analysis. The OFO Engine invokes `MicroContentExtractor.extract(...)` to generate the required text structures for the Carousel and Reels Explainer assets.
- `src/ccp/services/trait_scoring_engine.py`: Leveraged to perform the deep biometric analysis of the public content. The engine calls `TraitScoringEngine.score_all_traits()` to extract the Negative Metrics scores (e.g., Embodied Confidence, Vocal Resonance) that power the audit.
- `src/ccp/services/abel_vcb_generator.py`: Called to produce the Visual Composition Briefs (VCBs) required to render the Animated Video Audit and the Storytelling Video. Specifically, the engine interfaces with `AbelVCBGenerator.generate(inp: VCBGenerationInput)`.
- `src/ccp/models/leadership_scorecard_models.py`: The OFO schema extends the existing biometric models to ensure the audit report schema matches the platform's canonical data structures.

### 3.3 ADR-05 Primitives

- **`EXP-TRS-004` (Epic Meaning Framing / The Crusade Narrative)**: This primitive dictates the emotional and rhetorical posture of the Animated Video Audit. The asset must explicitly position the CCP not as an algorithmic judge criticizing the coach, but as an elite ally defending the coach's authority, depth, and nuance against the flattening, destructive effect of social media algorithms. 
- **`EXP-PRG-001` (Hook Cycle Velocity)**: This primitive governs the absolute speed of the conversion funnel. After the target receives the audit, they must be presented with an immediate, actionable, and low-friction way to improve their score (specifically, a 60-second voice correction) directly within the exact same Telegram session. Any latency or application switching destroys the Hook Cycle.

### 3.4 CBAR Mandate Enforcement

- **Phase5-M03 (The OFO Ego-Defense Rule)**
  - *Origin Story:* Phase 5, Epic 2, Story 2.1 (The 4-Asset Proof Package Delivery)
  - *Enforcement Mechanism:* The `CrusadeNarrativeFitter` service structurally enforces that any biometric flaw identified by the `trait_scoring_engine.py` is dynamically prefixed and suffixed with specific ideological framing strings defined in the Pydantic schema. If the output payload contains negative, clinical words like "poor", "weak", "bad", or "needs improvement" without being properly wrapped in the algorithmic defense context, the asset will fail validation, log a critical error, and will not be dispatched to the user.
- **Phase5-M04 (The Inline Capture Hook)**
  - *Origin Story:* Phase 5, Epic 2, Story 2.2 (Stealth Course Accountability Hook)
  - *Enforcement Mechanism:* The Telegram delivery payload is strictly prohibited from including external links to web landing pages or Calendly links. The final asset delivered (the Animated Video Audit) must include an inline Telegram Bot API `InlineKeyboardMarkup` button prompting the user to "Re-record your 60-second intro to fix this metric." Tapping this button immediately invokes the recording state machine within the active Telegram context, preventing any session breakage and maintaining full conversational continuity.

### 3.5 Technical Decisions

1. **Asynchronous Batch Generation vs. Streaming:** Due to the heavy computational processing required by the `AbelVCBGenerator` and the Skia visual renderer, the OFO 4-Asset Package must be generated asynchronously in the background. The target only receives the Telegram payload *after* all 4 assets are fully rendered, verified, and safely stored in the `visual-assets` S3 bucket. We deliberately avoid "streaming" partial asset generation for OFO to ensure the first touch is perfectly polished and devoid of loading states.
2. **Strict Pydantic Validation for Narrative Framing:** To prevent LLM hallucination and ensure the Crusade Narrative is maintained, we implement a custom Pydantic validator (`@field_validator`) inside the core schema. The validation step uses explicit regex patterns to ensure keywords like "algorithmic compression", "flattening", or "legacy" are present, while actively rejecting clinical critique terms.
3. **Single Telegram Session Continuity:** The OFO Delivery Agent utilizes Redis to hold the target's interaction state for an ephemeral 15-minute window post-delivery. This state lock (`AWAITING_CORRECTION`) ensures that any audio message sent by the target is automatically interpreted as the "Inline Capture" recording attempt. This eliminates the need for complex command parsing during the most critical 15 minutes of the conversion window.

---

## 4. Implementation Plan

The implementation is broken down into four distinct, logical phases, representing a progression from foundational data contracts to complex service orchestration and final UX delivery.

### Phase 1: Core Pydantic Schema and State Definitions
The foundation must be established first to ensure all internal data passing adheres to strict, validated types. This prevents downstream crashes and enforces business logic at the earliest possible stage.
1. **Define the `OFOAssetPackage` Model:** Create the central Pydantic schema in `src/ccp/models/ofo_models.py` incorporating the 4 specific asset references (Carousel, Storytelling Video, Reels Explainer, Animated Video Audit).
2. **Define the `CrusadeNarrativeAudit` Model:** Implement this Pydantic model with a strict `@field_validator` on the `transcript` field to guarantee enforcement of Phase5-M03. It must use regex to mandate the inclusion of specific ideological keywords and explicitly reject clinical critique terminology.
3. **Define the `OFOTargetState` Enum:** Create an enumeration to manage the Redis-backed state machine for Telegram delivery, explicitly including the `AWAITING_CORRECTION` state.
4. **Define the `OFOConversionEvent` Model:** Construct the telemetry model to track the latency of the Hook Cycle (Phase5-M04) for downstream analytics and optimization.

### Phase 2: Pipeline Orchestration
Building the central engine (`OFOEnginePipeline`) that coordinates the ingestion of public media and dispatch to existing, independent processing services.
5. **Implement `ingest_target()`:** Build the method within `src/ccp/services/ofo_engine_pipeline.py` to download, compress, and normalize the target's public media from provided URLs.
6. **Integrate Trait Scoring:** Connect the pipeline to `TraitScoringEngine.score_all_traits()`. Ensure that it cleanly handles audio processing and extracts the raw `ScoredTrait` list, specifically isolating the lowest-performing metric to serve as the "Hook" for the audit.
7. **Integrate Content Machine:** Connect the pipeline to `ContentMachinePipeline`. Pass the raw transcript and metadata to `MicroContentExtractor` to generate the textual frameworks for the `carousel` and `reels_explainer` assets.
8. **Integrate VCB Generation:** Connect the pipeline to `AbelVCBGenerator`. This task involves mapping the outputs of the Content Machine and the Crusade Narrative Fitter into `VCBGenerationInput` payloads to asynchronously request the rendering of the Storytelling Video and Animated Video Audit.

### Phase 3: The Crusade Narrative Fitter
Developing the critical natural language processing module that translates raw biometric scores into ego-defended, highly persuasive narrative scripts.
9. **Implement `CrusadeNarrativeFitter.apply_framing()`:** Create this service in `src/ccp/services/crusade_narrative_fitter.py`. It must accept the raw `ScoredTrait` list and use an LLM prompt wrapped in strict context to generate the audit transcript.
10. **Build Deterministic Fallback Logic:** If the LLM generation fails the Pydantic regex check (e.g., outputs insulting text), the module must catch the `ValueError` and automatically fallback to a set of pre-approved, deterministic template strings to guarantee safe delivery.
11. **Wire Output to VCB:** Connect the finalized, validated narrative transcript back into the main pipeline, passing it as the `script_content` for the Animated Video Audit's VCB request.
12. **Implement "Baseline Discovery" Path:** If the initial audio quality is too poor for `TraitScoringEngine` to process, the fitter must shift strategies, generating a "Baseline Discovery" narrative that blames social media compression for the poor audio and requests a clean Telegram voice note.

### Phase 4: Telegram Delivery and Inline Capture
Executing the "final mile": delivering the payload with perfect timing and flawlessly executing the Phase5-M04 capture mandate.
13. **Implement `OFODeliveryAgent.dispatch_package()`:** Create this agent in `src/ccp/agents/ofo_delivery_agent.py`. It must use `python-telegram-bot` to send the assets in a highly specific sequence: Carousel as a media group, followed by the explainer videos, capped with the Animated Audit.
14. **Attach Inline Keyboards:** Ensure the final Animated Audit message attaches an `InlineKeyboardMarkup` with the immediate "Re-record 60s correction" button.
15. **Implement Redis State Lock:** Upon sending the final message, write the target's session state to Redis (`target:{telegram_id}:state = AWAITING_CORRECTION`) with a strict 15-minute Time-To-Live (TTL).
16. **Update Webhook Router:** Modify `telegram_webhook.py` to check this Redis state. If a user in `AWAITING_CORRECTION` sends an audio message, the router must bypass standard conversational logic, accept the audio as the correction challenge, log the `OFOConversionEvent`, and instantly route the user into the Stealth Course initialization logic.

---

## 5. Primary Output Schema

```python
from pydantic import BaseModel, Field, field_validator
from typing import List, Optional
from datetime import datetime
import re

class AssetReference(BaseModel):
    asset_id: str
    asset_url: str
    asset_type: str = Field(
        ...,
        pattern="^(carousel|storytelling_video|reels_explainer|animated_audit)$",
        description="The strict classification of the visual asset."
    )

class CrusadeNarrativeAudit(BaseModel):
    transcript: str = Field(
        ...,
        description="The voiceover script for the Animated Video Audit. Must strictly use Epic Meaning Framing."
    )
    detected_flaw: str = Field(
        ...,
        description="The primary biometric negative metric identified (e.g., 'Embodied Confidence')."
    )
    biometric_score: float

    @field_validator("transcript")
    @classmethod
    def validate_crusade_narrative(cls, v: str) -> str:
        """
        Enforces CBAR Phase5-M03 (OFO Ego-Defense Rule).
        The transcript must contain words indicating an external algorithmic enemy
        rather than a personal failing to prevent triggering target ego-defense.
        """
        lower_v = v.lower()
        
        # Mandate the inclusion of thematic ideological keywords
        required_themes = [
            r"algorithm", r"compression", r"flattening", 
            r"legacy", r"defend", r"protect"
        ]
        
        matches = sum(1 for theme in required_themes if re.search(theme, lower_v))
        if matches < 2:
            raise ValueError(
                "Transcript fails the Crusade Narrative mandate (Phase5-M03). "
                "It must explicitly frame the critique against the algorithm or system, not the user."
            )
        
        # Explicitly ban clinical, negative critique terminology
        forbidden_words = [
            r"\bpoor\b", r"\bweak\b", r"\bbad\b", r"needs improvement", r"\binadequate\b"
        ]
        for forbidden in forbidden_words:
            if re.search(forbidden, lower_v):
                raise ValueError(
                    f"Transcript contains forbidden clinical critique word: '{forbidden}'. "
                    "This violates Phase5-M03."
                )
                
        return v

class OFOAssetPackage(BaseModel):
    target_id: str
    generated_at: datetime
    carousel: AssetReference
    storytelling_video: AssetReference
    reels_explainer: AssetReference
    animated_audit: AssetReference
    audit_data: CrusadeNarrativeAudit

class OFOConversionEvent(BaseModel):
    target_id: str
    telegram_session_id: str
    audio_correction_asset_id: str
    hook_cycle_latency_ms: int = Field(
        ...,
        description="Time delta between audit delivery and correction receipt. Used to track Phase5-M04 compliance."
    )
    conversion_successful: bool = True
```

---

## 6. Backward Compatibility Fallback

The OFO Engine is a brand-new top-level service and does not replace or deprecate any legacy API endpoints. However, because it heavily relies on the upstream `TraitScoringEngine`, it requires robust fallback mechanisms to prevent catastrophic failure loops if the input data is suboptimal. 

If the `TraitScoringEngine` fails to confidently score the ingested public media—for example, if the target's video has severe background noise, heavy music overlays, or is shorter than the minimum threshold—the OFO pipeline will catch the resulting `InsufficientSignalError`. Instead of crashing or returning an empty payload, it will gracefully default to generating a **"Baseline Discovery"** package.

In this fallback path, instead of producing an Animated Video Audit detailing specific biometric flaws, the system generates an audit that highlights the *absence* of high-fidelity signals. The transcript will blame the "heavy compression of the social media platform" for destroying the coach's natural vocal resonance, and the inline capture button will prompt the coach to "Record a clean 60-second voice note directly into Telegram to establish your true acoustic baseline." This strategic fallback preserves the integrity of the Hook Cycle (Phase5-M04) and maintains the Crusade Narrative, turning a technical failure into a compelling reason for the user to interact.

---

## 7. Tasks

1. Create `src/ccp/models/ofo_models.py` and implement the Pydantic schemas: `OFOAssetPackage`, `CrusadeNarrativeAudit`, `AssetReference`, and `OFOConversionEvent`.
2. Write rigorous unit tests for `CrusadeNarrativeAudit` to strictly verify the regex constraints and ensure compliance with Phase5-M03.
3. Create the `src/ccp/services/crusade_narrative_fitter.py` module to handle the LLM prompt wrapping, validation execution, and deterministic fallback logic.
4. Create the main orchestration module `src/ccp/services/ofo_engine_pipeline.py`.
5. Implement the `ingest_target(url)` method in `ofo_engine_pipeline.py` to securely download, compress, and normalize public media streams.
6. Connect `ofo_engine_pipeline.py` to `TraitScoringEngine` to execute biometric analysis and extract the prioritized `ScoredTrait` list.
7. Connect `ofo_engine_pipeline.py` to `CrusadeNarrativeFitter` to generate the validated, ego-defended transcript.
8. Connect `ofo_engine_pipeline.py` to `AbelVCBGenerator`, mapping the transcript into a `VCBGenerationInput` payload to generate the `animated_audit` VCB.
9. Connect `ofo_engine_pipeline.py` to `ContentMachinePipeline` to process the text and generate the `carousel` and `reels_explainer` copy.
10. Create the delivery module `src/ccp/agents/ofo_delivery_agent.py`.
11. Implement `dispatch_package()` in `ofo_delivery_agent.py` using `python-telegram-bot` to send media groups in the correct chronological sequence.
12. Configure the `InlineKeyboardMarkup` integration within the final audit message.
13. Implement the Redis state transition logic (`target:{id}:state = AWAITING_CORRECTION`) setting a 15-minute TTL upon message delivery.
14. Update the core `telegram_webhook.py` router to intercept audio messages from senders in the `AWAITING_CORRECTION` state, explicitly routing them to the Stealth Course logic.
15. Add end-to-end integration tests mapping the full asynchronous flow from `ingest_target` to `dispatch_package`.

---

## 8. Acceptance Criteria

**AC1: Complete 4-Asset Package Generation**
- *Given* an identified high-value coach target's public video URL,
- *When* `OFOEnginePipeline.process_target()` is invoked asynchronously,
- *Then* the system must return a complete, validated `OFOAssetPackage` containing exactly 4 `AssetReference` objects (carousel, storytelling_video, reels_explainer, animated_audit).
- *FAILURE EXAMPLE:* The pipeline only generates 3 assets because the `content_machine` failed to extract sufficient copy, and attempts to return a partial object. This must raise an exception, halt delivery, and flag the operator.

**AC2: OFO Ego-Defense Rule (Phase5-M03)**
- *Given* the `TraitScoringEngine` detects a critically low "Embodied Confidence" score (e.g., 3/10),
- *When* the `CrusadeNarrativeFitter` generates the audit transcript,
- *Then* the transcript MUST successfully pass the `CrusadeNarrativeAudit` Pydantic validator, framing the issue as "social algorithms compressing your natural physical authority" rather than "you have poor confidence."
- *FAILURE EXAMPLE:* The transcript outputs "Your embodied confidence is weak and needs improvement." The Pydantic model raises a `ValueError` during instantiation, preventing the insulting audit from ever being rendered or dispatched to the target.
- *Mandate Reference:* Phase5-M03.

**AC3: The Inline Capture Hook (Phase5-M04)**
- *Given* the `OFODeliveryAgent` successfully sends the complete 4-Asset Package via Telegram,
- *When* the user views the Animated Video Audit message,
- *Then* the final message must contain an Inline Button labeled "Fix This Metric Now" that, when tapped, sets the internal chat state to expect an immediate audio recording without requiring the user to open an external web browser, schedule a call, or leave the app.
- *FAILURE EXAMPLE:* The message text says "Click here to book a strategy call to review your audit," pushing the user to Calendly and completely breaking the same-session Hook Cycle Velocity.
- *Mandate Reference:* Phase5-M04.

---

## 9. Dependencies

### Internal Services
- `TraitScoringEngine` (`src/ccp/services/trait_scoring_engine.py`): Mandatory for generating the Negative Metrics that power the audit logic.
- `ContentMachinePipeline` (`src/ccp/services/content_machine.py`): Required for textual extraction for visual assets.
- `AbelVCBGenerator` (`src/ccp/services/abel_vcb_generator.py`): Required to turn text scripts into structured visual briefs.
- `VidyeRouter` / `telegram_webhook.py`: Required for intercepting the inline capture audio response.

### External Services
- **Telegram Bot API:** Essential for dispatching the rich media assets and rendering the interactive `InlineKeyboardMarkup`.
- **Redis Server:** Mandatory for maintaining the ephemeral 15-minute `AWAITING_CORRECTION` session state lock efficiently.
- **Skia Renderer (Sidecar Process):** Relied upon indirectly via VCB generation to physically render the final MP4 visual assets before delivery.

---

## 10. Testing Strategy

The OFO Engine will be rigorously tested strictly following the existing pytest architectural patterns defined within `tests/integration/`.

### Unit Tests
1. `test_crusade_narrative_validator.py`: Directly tests the custom Pydantic `@field_validator` on the `CrusadeNarrativeAudit` class. Supplies simulated transcripts containing forbidden words ("poor", "bad", "inadequate") to guarantee `ValueError` is raised, and supplies transcripts with required themes ("algorithm", "compression", "defend") to ensure successful validation.
2. `test_crusade_narrative_fitter.py`: Mocks the external LLM response API to ensure that the internal fallback deterministic templates are successfully engaged if the LLM repeatedly violates the Phase5-M03 regex constraints.
3. `test_ofo_pipeline_fallback_baseline.py`: Explicitly mocks the `TraitScoringEngine` throwing an `InsufficientSignalError` (due to simulated poor audio) and verifies that the OFO Pipeline correctly detects this and successfully generates a "Baseline Discovery" package instead of crashing.

### Integration Tests
1. `test_cpsc_fr_era3_04_ofo_end_to_end.py`: End-to-end simulation using a known, stable test-video URL. Mocks the Skia visual renderer but executes the entire Python logic stack: ingests the video, runs trait scoring, extracts content, generates the VCBs, applies the Crusade Narrative, and asserts that the resulting `OFOAssetPackage` is perfectly formed and conforms to the schema.
2. `test_cpsc_fr_era3_04_telegram_capture_loop.py`: Uses a mock Telegram Update object to simulate a user tapping the "Fix This Metric Now" inline button. It verifies that the backend Redis state correctly transitions to `AWAITING_CORRECTION`, and subsequently simulates an incoming Telegram voice note to verify it is correctly routed to the Stealth Course initialization logic, confirming Phase5-M04 compliance.
