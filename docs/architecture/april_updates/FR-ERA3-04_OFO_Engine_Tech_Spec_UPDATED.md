# PRE-WORK LOG

<!-- UPDATED: Added Wave 0 SDA proof sources and the exact baseline proof-object gap. -->

1. **Protocol:** `docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md` - Read sections 2, 3, and 4.
2. **PRD Modules:** `PRD_09_CPSC_Silent_Referral.md` loaded. Proof quote retained: "FR-ERA3-04 (OFO Engine): The Object-First Outreach engine that generates high-end proof assets as a Trojan Horse wedge for acquiring new high-value coaches."
3. **Phase Epic:** `docs/architecture/april_updates/Phase5_Growth_Epics.md` loaded. Proof quote retained: "**Given** an identified high-value coach target,"
4. **CBAR Audit:** `docs/architecture/cbar_audits/CBAR_Audit_Phase5_Growth.md` loaded. Mandates M-03 and M-04 confirmed and preserved.
5. **Primitives:** Checked `primitives/experience/`. Proof retained:
   - `id: EXP-TRS-004`, `name: Epic Meaning Framing (The Crusade Narrative)`
   - `id: EXP-PRG-001`, `name: Hook Cycle Velocity`
6. **Backend Python Files:** Audited:
   - `src/ccp/services/content_machine.py`
   - `src/ccp/services/trait_scoring_engine.py`
   - `src/ccp/services/abel_vcb_generator.py`
   Proof retained: `ContentMachinePipeline.process_session(self, session_report: dict[str, Any], coach_id: str, coach_acronym: str = "CCH") -> ContentMachineResult`
7. **Test Files:** `test_cpsc_fr51_challenge_funnel.py` and `test_cbcs12_coping_invitation.py` reviewed to match section 10 testing patterns.
8. **Existing Spec Re-read / Exact Gap Proof:** Re-read `FR-ERA3-04_OFO_Engine_Tech_Spec.md`. The exact section that now requires SDA direction controls is **2.2 Solution**, where the package is framed as a defense of the coach's legacy against "algorithmic compression" and the proof package is meant to "bypass the target's ego defense." That logic can be commercially effective while still failing semantic integrity if it drifts into false transcendence, coercive pressure, or ego manipulation.
9. **Wave 0 PRD Alignment:** Re-read `PRD_09_CPSC_Silent_Referral.md`, including `5.3A Relationship to the Semantic Discernment Architecture` and `1.4 SDA-Aware Trust Transfer and Commercial Integrity`. Confirmed the commercial layer must distinguish healthy authority from prestige theater, proof from vanity, and urgency from coercion.
10. **Mandatory SDA Source Set:** Re-read:
   - `lab/semantic_discernment_architecture_content_engine_v_1.md`
   - `lab/semantic_discernment_architecture_artifact_taxonomy_v_1.md`
   - `lab/CCP APRIL Updates/05_Core_Experience/Perceptual_Primitives_Architecture.md`
   - `lab/CCP APRIL Updates/05_Core_Experience/Matrix of Edging.md`
11. **Wave 1 SDA Specs:** Re-read:
   - `FR-ERA3-20_SDA_Ontology_And_Registry_Tech_Spec.md`
   - `FR-ERA3-21_SDA_Query_And_Crosswalk_Service_Tech_Spec.md`
   - `FR-ERA3-22_Directional_Integrity_Engine_Tech_Spec.md`
   These are now consumed directly by this update for ontology lookup, crosswalk resolution, and dispatch gating.

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
10. `docs/architecture/april_updates/FR-ERA3-04_OFO_Engine_Tech_Spec.md`
11. `lab/semantic_discernment_architecture_content_engine_v_1.md`
12. `lab/semantic_discernment_architecture_artifact_taxonomy_v_1.md`
13. `lab/CCP APRIL Updates/05_Core_Experience/Perceptual_Primitives_Architecture.md`
14. `lab/CCP APRIL Updates/05_Core_Experience/Matrix of Edging.md`
15. `docs/architecture/april_updates/FR-ERA3-20_SDA_Ontology_And_Registry_Tech_Spec.md`
16. `docs/architecture/april_updates/FR-ERA3-21_SDA_Query_And_Crosswalk_Service_Tech_Spec.md`
17. `docs/architecture/april_updates/FR-ERA3-22_Directional_Integrity_Engine_Tech_Spec.md`

---

## 2. Overview

<!-- UPDATED: Added dignity-vs-coercion and false-transcendence directional integrity framing. -->

### 2.1 Problem
The Conscious Coaching Platform fundamentally relies on acquiring high-value coaches as its primary market wedge and future node network. Traditional cold-outreach methodologies such as direct messages, generic email sequences, or PDF lead magnets have near-zero conversion rates because elite coaches are continuously inundated with generic pitches, agency offers, and automated bots. These targets possess strong ego defenses and are highly protective of their authority and brand identity. A standard SaaS pitch, or a clinical critique of their content, immediately triggers those defenses and causes instant bounce, reputational damage, and permanent loss of the prospect.

### 2.2 Solution
The Object First Outreach (OFO) Engine acts as a Trojan Horse acquisition strategy. Rather than pitching software directly, the engine programmatically analyzes a high-value coach target's public content and generates a premium 4-Asset Proof Package. The package is delivered for free and framed not as a sales pitch but as a defense of the target's legacy against algorithmic compression. By providing undeniable proof of the platform's intelligence through a highly personalized and high-production-value asset, the engine creates trust transfer and invites the target to interact natively within Telegram, initiating the Hook Cycle and drawing them into the $0 Proof Layer.

This revised specification preserves that object-first logic but adds a mandatory SDA directional-integrity layer around the proof object itself. OFO now treats the 4-Asset Package as a high-prestige commercial-semantic artifact that can succeed locally while still being directionally wrong if it:
- manufactures false transcendence
- flatters ego in a manipulative way
- packages urgency as coercive pressure
- or relies on prestige-coded dominance rather than dignified proof

The governing distinction is now explicit:
- **Dignified proof** is premium, relevant, truthful, and invitational. It protects the target's agency while still demonstrating real diagnostic intelligence.
- **Coercive pressure** is premium-looking but semantically corrosive. It relies on shame capture, superiority framing, prestige extraction, destiny theater, or compulsive reply pressure to force response.

The Crusade Narrative remains necessary, but it is no longer sufficient by itself. Representation geometry, hard-negative resistance, and feedback-loop safety must now be validated before an OFO package is dispatched.

### 2.3 Scope
This technical specification covers:
- ingestion, normalization, and processing of a coach's public content
- orchestration of the 4-Asset Proof Package generation
- strict enforcement of the Animated Video Audit's Crusade Narrative framing
- Telegram delivery and same-session inline capture
- SDA directional-integrity controls over proof-object packaging, including representation geometry, hard-negative rejection, and repeated-outreach loop awareness

---

## 3. Context for Development

### 3.1 Architecture Traceability (DEP-IDs)

| DEP-ID | Data Object | Description |
|---|---|---|
| DEP-OFO-001 | OFOAssetPackage | The complete 4-asset proof package generated by the orchestration pipeline. |
| DEP-OFO-002 | CrusadeNarrativeAudit | The validated textual transcript wrapping the biometric scores in Epic Meaning framing. |
| DEP-OFO-003 | OFOConversionEvent | The telemetry event payload tracking the successful execution of the inline capture hook. |
| DEP-OFO-004 | OFOIntegrityEnvelope | The runtime state envelope wrapping the package with SDA representation geometry and loop safety status. |
| DEP-SDA-020 | SDA Ontology + Registry | Canonical representation geometry references are resolved through `FR-ERA3-20`. |
| DEP-SDA-021 | SDA Query + Crosswalk Service | OFO resolves canonical geometry / crosswalk references through `FR-ERA3-21`. |
| DEP-SDA-022 | Directional Integrity Engine | Prestige-bearing outreach packages must pass `FR-ERA3-22` before dispatch. |

### 3.2 Existing Backend Integration
The OFO Engine remains a new top-level orchestration service, but it heavily consumes existing, validated Era 3 components:
- `src/ccp/services/content_machine.py`: used to extract micro-content structures for the Carousel and Reels Explainer assets
- `src/ccp/services/trait_scoring_engine.py`: used to perform deep biometric analysis and identify the prioritized flaw / hook
- `src/ccp/services/abel_vcb_generator.py`: used to generate VCBs for the Storytelling Video and Animated Video Audit
- `src/ccp/models/leadership_scorecard_models.py`: used as the canonical shape basis for biometric audit output
- `FR-ERA3-21 SDA Query and Crosswalk Service`: used to resolve canonical `representation_geometry_id` values for outreach packaging
- `FR-ERA3-22 Directional Integrity Engine`: used to evaluate whether a candidate proof package remains dignified and trust-building or has drifted into prestige theater, coercion, or false transcendence

### 3.3 ADR-05 Primitives
- **`EXP-TRS-004` (Epic Meaning Framing / The Crusade Narrative):** dictates the emotional and rhetorical posture of the Animated Video Audit. The asset must position CCP as an ally defending the coach's authority, depth, and nuance against algorithmic flattening.
- **`EXP-PRG-001` (Hook Cycle Velocity):** governs the speed of the conversion funnel. After the target receives the audit, they must be presented with an immediate, actionable, low-friction correction path in the exact same Telegram session.

Under SDA, these primitives must now be interpreted more carefully:
- `EXP-TRS-004` can support dignified authority transfer or degenerate into false-transcendence theater depending on representation geometry.
- `EXP-PRG-001` can preserve friction-zero continuity or drift into coercive pressure if urgency is used to collapse agency.

### 3.4 CBAR Mandate Enforcement
- **Phase5-M03 (The OFO Ego-Defense Rule)**
  - *Origin Story:* Phase 5, Epic 2, Story 2.1
  - *Enforcement Mechanism:* `CrusadeNarrativeFitter` enforces that biometric flaws are wrapped in algorithmic-defense framing. If insulting or clinical wording appears without proper ideological framing, the asset fails validation and cannot dispatch.
- **Phase5-M04 (The Inline Capture Hook)**
  - *Origin Story:* Phase 5, Epic 2, Story 2.2
  - *Enforcement Mechanism:* The Telegram delivery payload cannot include external landing pages or Calendly links. The final asset must include an inline button that immediately invokes the recording state machine inside the active Telegram context.
- **Wave0-SDA Commercial Integrity Rule**
  - *Origin Story:* `PRD-09` sections `5.3A` and `1.4 SDA-Aware Trust Transfer and Commercial Integrity`
  - *Enforcement Mechanism:* Before dispatch, each OFO proof package must resolve canonical representation geometry and pass `FR-ERA3-22` directional-integrity screening. Packages that encode false transcendence, ego manipulation, coercive urgency, vanity proof, or superiority theater are blocked or downgraded before delivery.

### 3.5 Technical Decisions
1. **Asynchronous Batch Generation vs. Streaming:** All 4 assets must be fully rendered and verified before the first touch is delivered. OFO does not stream partial proof objects.
2. **Strict Pydantic Validation for Narrative Framing:** `CrusadeNarrativeAudit` retains a custom validator to enforce required themes and reject clinical critique language.
3. **Single Telegram Session Continuity:** Redis-backed `AWAITING_CORRECTION` state remains mandatory for the 15-minute correction window.
4. **Dignified Proof over Coercive Pressure:** Premium visuals and authority framing are rejected if they function as ego manipulation rather than truthful proof.
5. **Representation Geometry is Mandatory for Outreach Packaging:** Narrative safety is not guaranteed by keywords alone. Each package must declare a canonical `representation_geometry_id`.
6. **Hard-Negative and Feedback-Loop Awareness:** OFO must reject deceptively close outreach packages that look inspirational but actually encode false transcendence, mystified authority, shame capture, or compulsive reply pressure. Repeated outreach object classes must also be monitored for drift at scale.

---

## 4. Implementation Plan

<!-- UPDATED: Added SDA packaging, release gate, and loop-safety phases while preserving baseline OFO sequencing. -->

The implementation remains a four-phase rollout, with targeted SDA additions inserted into the existing sequence.

### Phase 1: Core Pydantic Schema and State Definitions
1. Define `OFOAssetPackage` in `src/ccp/models/ofo_models.py` with the 4 specific asset references.
2. Define `CrusadeNarrativeAudit` with strict validator logic for Phase5-M03.
3. Define `OFOTargetState` including `AWAITING_CORRECTION`.
4. Define `OFOConversionEvent` for Hook Cycle telemetry.
5. Define `OFOIntegrityEnvelope` to record `representation_geometry_id`, directional-integrity decision, hard-negative result, and loop-safety state for each outreach package.

### Phase 2: Pipeline Orchestration
6. Implement `ingest_target()` in `src/ccp/services/ofo_engine_pipeline.py`.
7. Integrate `TraitScoringEngine.score_all_traits()` and isolate the priority hook.
8. Integrate `ContentMachinePipeline` for textual structures.
9. Integrate `AbelVCBGenerator` for Storytelling Video and Animated Audit VCB generation.
10. Add a packaging stage that resolves the canonical representation geometry for the proof object through `FR-ERA3-21`.

### Phase 3: The Crusade Narrative Fitter and Integrity Gate
11. Implement `CrusadeNarrativeFitter.apply_framing()` in `src/ccp/services/crusade_narrative_fitter.py`.
12. Build deterministic fallback templates if LLM output fails validator checks.
13. Wire the validated transcript into the Animated Audit VCB request.
14. Implement the "Baseline Discovery" path for insufficient audio quality.
15. Call `FR-ERA3-22` before dispatch so packages that pass keyword safety but still encode coercive authority, false transcendence, or vanity prestige are blocked or downgraded.

### Phase 4: Telegram Delivery, Inline Capture, and Loop Safety
16. Implement `OFODeliveryAgent.dispatch_package()` in `src/ccp/agents/ofo_delivery_agent.py`.
17. Attach `InlineKeyboardMarkup` to the final Animated Audit message.
18. Implement the Redis state lock with a 15-minute TTL, explicitly storing the `delivery_timestamp` alongside the `AWAITING_CORRECTION` state to enable latency calculations.
19. Update `telegram_webhook.py` so audio replies in `AWAITING_CORRECTION` route directly into Stealth Course initialization, using the stored timestamp to calculate `hook_cycle_latency_ms`, and mandating a Receipt Chain Guard write before transitioning the user state.
20. Track repeated use of the same prestige-bearing packaging style and cool or pause it when loop telemetry indicates ego-hook dependence or coercive reply pressure.

---

## 5. Primary Output Schema

<!-- UPDATED: Added representation geometry and runtime integrity state for OFO outreach packages. -->

```python
from pydantic import BaseModel, Field, field_validator
from typing import Optional
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
    representation_geometry_id: str = Field(
        ...,
        description="Canonical SDA representation geometry selected for this proof object."
    )
    dignity_class: str = Field(
        "dignified_proof",
        description="Runtime outreach class. Must remain dignity-preserving rather than coercive."
    )
    directional_integrity_status: str = Field(
        "pending",
        description="Release state returned by FR-ERA3-22."
    )

    @field_validator("transcript")
    @classmethod
    def validate_crusade_narrative(cls, v: str) -> str:
        lower_v = v.lower()

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
    hard_negative_status: str = Field(
        "pending",
        description="Whether false-transcendence / ego-manipulation near-neighbors were detected."
    )
    directional_integrity_report_id: Optional[str] = Field(
        None,
        description="Reference to the directional integrity evaluation used to approve dispatch."
    )


class OFOConversionEvent(BaseModel):
    target_id: str
    telegram_session_id: str
    audio_correction_asset_id: str
    hook_cycle_latency_ms: int = Field(
        ...,
        description="Time delta between audit delivery and correction receipt. Used to track Phase5-M04 compliance."
    )
    conversion_successful: bool = True
    loop_safety_status: str = Field(
        "healthy",
        description="Runtime status tracking repeated outreach feedback-loop safety."
    )


class OFOIntegrityEnvelope(BaseModel):
    target_id: str
    representation_geometry_id: str
    directional_integrity_decision: str
    hard_negative_status: str
    loop_safety_status: str = "healthy"
    blocked_reason: Optional[str] = None
```

---

## 6. Backward Compatibility Fallback

<!-- UPDATED: Added fail-closed behavior for semantically unsafe prestige-bearing outreach packages. -->

The OFO Engine remains a new top-level service and does not replace or deprecate legacy API endpoints. It still requires robust fallback behavior because it depends on upstream scoring quality.

If `TraitScoringEngine` cannot confidently score the ingested public media because of noise, music overlays, or short duration (specifically, failing the exact numeric thresholds of < 15.0 seconds of clear speech or < 0.65 signal confidence score), the pipeline must catch `InsufficientSignalError` and generate a **Baseline Discovery** package instead of crashing. In that fallback path, the audit emphasizes signal absence caused by social-media compression and invites the coach to record a clean 60-second Telegram voice note.

If SDA geometry resolution is unavailable, or if `FR-ERA3-22` returns `REVIEW` or `FAIL` because the package encodes false transcendence, coercive urgency, vanity prestige, or ego manipulation, the engine must fail closed on the prestige-bearing package. It may then either:
- downgrade to a dignity-safe Baseline Discovery outreach variant, or
- hold the package for operator review.

It must not auto-dispatch a premium-looking outreach artifact whose semantics are directionally unsafe.

---

## 7. Tasks

<!-- UPDATED: Added concrete engineering work for SDA-aware outreach filtering. -->

1. Create `src/ccp/models/ofo_models.py` and implement `OFOAssetPackage`, `CrusadeNarrativeAudit`, `AssetReference`, `OFOConversionEvent`, and `OFOIntegrityEnvelope`.
2. Write rigorous unit tests for `CrusadeNarrativeAudit` validator behavior.
3. Create `src/ccp/services/crusade_narrative_fitter.py` for prompt wrapping, validation, and deterministic fallback.
4. Create `src/ccp/services/ofo_engine_pipeline.py`.
5. Implement `ingest_target(url)` for secure download, compression, and normalization.
6. Connect the pipeline to `TraitScoringEngine`.
7. Connect the pipeline to `CrusadeNarrativeFitter`.
8. Connect the pipeline to `AbelVCBGenerator`.
9. Connect the pipeline to `ContentMachinePipeline`.
10. Create `src/ccp/agents/ofo_delivery_agent.py`.
11. Implement `dispatch_package()` using `python-telegram-bot`.
12. Configure `InlineKeyboardMarkup` on the final audit message.
13. Implement the Redis `AWAITING_CORRECTION` state with a 15-minute TTL, storing the exact `delivery_timestamp` alongside it.
14. Update `telegram_webhook.py` to route correction audio directly to Stealth Course logic, calculate `hook_cycle_latency_ms`, and write the state transition to the Receipt Chain Guard.
15. Add end-to-end integration tests for `ingest_target` through `dispatch_package`.
16. Add `representation_geometry_id`, `dignity_class`, and directional-integrity fields to OFO models.
17. Implement geometry resolution through `FR-ERA3-21`.
18. Implement OFO directional-integrity dispatch gating through `FR-ERA3-22`.
19. Add downgrade / operator-review handling for semantically unsafe packages.
20. Implement repeated-outreach loop telemetry and throttling hooks.

---

## 8. Acceptance Criteria

<!-- UPDATED: Added dignity-vs-coercion, representation geometry, and loop-safety criteria. -->

**AC1: Complete 4-Asset Package Generation**
- *Given* an identified high-value coach target's public video URL,
- *When* `OFOEnginePipeline.process_target()` is invoked asynchronously,
- *Then* the system must return a complete, validated `OFOAssetPackage` containing exactly 4 `AssetReference` objects (`carousel`, `storytelling_video`, `reels_explainer`, `animated_audit`).
- *FAILURE EXAMPLE:* The pipeline only generates 3 assets because `content_machine` fails to extract sufficient copy and attempts to return a partial object. This must raise an exception, halt delivery, and flag the operator.

**AC2: OFO Ego-Defense Rule (Phase5-M03)**
- *Given* the `TraitScoringEngine` detects a critically low "Embodied Confidence" score,
- *When* the `CrusadeNarrativeFitter` generates the audit transcript,
- *Then* the transcript must pass the `CrusadeNarrativeAudit` validator, framing the issue as algorithmic compression rather than as a direct insult to the coach.
- *FAILURE EXAMPLE:* The transcript outputs "Your embodied confidence is weak and needs improvement." The Pydantic model must raise `ValueError` and prevent dispatch.
- *Mandate Reference:* Phase5-M03.

**AC3: The Inline Capture Hook (Phase5-M04)**
- *Given* the `OFODeliveryAgent` successfully sends the complete 4-Asset Package via Telegram,
- *When* the user views the Animated Video Audit message,
- *Then* the final message must contain an inline button labeled "Fix This Metric Now" that sets the internal chat state to expect an immediate audio recording without requiring the user to open an external browser, schedule a call, or leave the app.
- *FAILURE EXAMPLE:* The message says "Book a strategy call to review your audit," pushing the user to Calendly and breaking same-session Hook Cycle Velocity.
- *Mandate Reference:* Phase5-M04.

**AC4: Dignified Proof Packaging**
- *Given* a complete OFO package is generated successfully,
- *When* the final package is prepared for delivery,
- *Then* the package must resolve a canonical `representation_geometry_id` and pass directional-integrity screening as dignified proof rather than coercive pressure.
- *FAILURE EXAMPLE:* The package uses grandiose destiny language, superiority cues, and urgency framing that imply the coach is chosen and must respond immediately to preserve greatness. Even if all assets are visually premium, the package must be blocked or downgraded before dispatch.

**AC5: False-Transcendence / Ego-Manipulation Rejection**
- *Given* the content analysis is real and the Crusade Narrative validator passes,
- *When* the proof object still resembles a hard negative such as false transcendence, mystified authority, or vanity prestige,
- *Then* `FR-ERA3-22` must return a non-pass decision and the engine must not auto-dispatch the package.
- *FAILURE EXAMPLE:* The copy says the coach has a destiny too rare for ordinary audiences and implies CCP alone can preserve their sacred authority. This is manipulative transcendence packaging and must be rejected.

**AC6: Repeated Outreach Loop Safety**
- *Given* the OFO engine repeatedly reuses one successful prestige-coded packaging style across many targets,
- *When* loop telemetry shows that style is creating reply pressure or ego-hook dependence rather than healthy curiosity,
- *Then* the engine must mark the loop as degraded and cool or pause that packaging strategy.
- *FAILURE EXAMPLE:* One coercive representation geometry produces strong reply rates and is scaled broadly without semantic checks, teaching the engine to normalize manipulative outreach.

---

## 9. Dependencies

<!-- UPDATED: Added the mandatory SDA foundation services consumed by OFO packaging. -->

### Internal Services
- `TraitScoringEngine` (`src/ccp/services/trait_scoring_engine.py`): mandatory for generating the negative metrics that power the audit logic
- `ContentMachinePipeline` (`src/ccp/services/content_machine.py`): required for textual extraction for visual assets
- `AbelVCBGenerator` (`src/ccp/services/abel_vcb_generator.py`): required to turn text scripts into structured visual briefs
- `VidyeRouter` / `telegram_webhook.py`: required for intercepting the inline capture audio response
- `FR-ERA3-20_SDA_Ontology_And_Registry_Tech_Spec.md`: canonical ontology / geometry ownership
- `FR-ERA3-21_SDA_Query_And_Crosswalk_Service_Tech_Spec.md`: canonical geometry / crosswalk lookup
- `FR-ERA3-22_Directional_Integrity_Engine_Tech_Spec.md`: mandatory dispatch gate for dignity-preserving outreach proof

### External Services
- **Telegram Bot API:** required for rich media dispatch and inline keyboards
- **Redis Server:** required for the 15-minute `AWAITING_CORRECTION` state lock
- **Skia Renderer (Sidecar Process):** required indirectly via VCB generation to render the final assets

---

## 10. Testing Strategy

<!-- UPDATED: Added semantic-direction tests for coercion rejection and repeated outreach loops. -->

The OFO Engine will continue following existing pytest patterns used in `tests/integration/`.

### Unit Tests
1. `test_crusade_narrative_validator.py`: verifies required Crusade themes pass and forbidden clinical critique language fails.
2. `test_crusade_narrative_fitter.py`: verifies deterministic fallback templates engage if the LLM violates Phase5-M03 constraints.
3. `test_ofo_pipeline_fallback_baseline.py`: verifies `InsufficientSignalError` produces a Baseline Discovery package instead of a crash.
4. `test_ofo_directional_integrity_block.py`: verifies a premium-looking package is blocked or downgraded when `FR-ERA3-22` detects false transcendence, coercive pressure, or ego-manipulation geometry.
5. `test_ofo_geometry_resolution_fail_closed.py`: verifies the engine refuses auto-dispatch if canonical representation geometry cannot be resolved.

### Integration Tests
1. `test_cpsc_fr_era3_04_ofo_end_to_end.py`: end-to-end simulation from video ingest through asset package formation, ensuring a valid `OFOAssetPackage` is produced.
2. `test_cpsc_fr_era3_04_telegram_capture_loop.py`: simulates the inline button tap and follow-up voice note, verifying correct Redis state transition and Stealth Course routing.
3. `test_ofo_dignified_package_dispatch_only.py`: verifies a package that passes render generation but fails directional integrity is not auto-dispatched.
4. `test_ofo_repeated_outreach_loop_cooling.py`: simulates repeated use of the same prestige-coded outreach object until loop telemetry degrades and verifies the packaging strategy is cooled or paused.
