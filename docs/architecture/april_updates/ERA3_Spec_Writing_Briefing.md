# Era 3 Spec Writing Briefing — Conscious Coaching Platform

> [!CAUTION]
> **This document is the MANDATORY first read for ANY agent or human writing Era 3 Tech Specs.**
> It supersedes the retired `SPEC_REWRITE_BRIEFING.md` (CA11 Studio pivot, March 2026).

## 1. What Is Era 3 and Why It Matters
- **Context:** The Conscious Coaching Platform (CCP) is a Telegram-native coaching OS designed to drive action without friction.
- **Architecture:** Era 3 shifts to a Mini App architecture + verifiable behavioral primitives + CBAR-hardened epics.
- **Scope:** 34 specs across 6 phases, governed by 33 binding CBAR mandates.
- **Integration:** The platform already has a fully built Python/FastAPI backend (201 services, 45 models, 17 pipelines, 17 agents). **Specs EXTEND, they do not reinvent.**

## 2. The Spec Writing Pipeline (Step-by-Step)
1. **Read THIS briefing.**
2. **Read the `ERA3_Tech_Spec_Writing_Protocol.md`** (the master protocol).
3. **Identify the Phase and Spec number** you are writing from the Master Inventory (§4).
4. **Execute the 7-step Pre-Flight Checklist** (§7) loading PRDs, Epic stories, and CBAR mandates.
5. **Write the spec using the exact 10-Section Format** (§6).
6. **Self-audit** against the assigned CBAR mandates.
7. **Submit for review** against the Quality Gates (§13).

## 3. Source Documents Hierarchy
| Source Level | Document Type | What to Extract |
|---|---|---|
| **Foundation** | `docs/prd/modules/PRD_01-09_*.md` | Functional requirements, modes, quality gates, Brownfield Analysis (NEW/EXISTING/OBSOLETE). |
| **Logic/Rules** | `docs/architecture/april_updates/Phase1-5_*_Epics.md` | User stories, Acceptances Criteria, Mapped Primitives, and Canonical CBAR Mandates. |
| **Audit Trail** | `docs/architecture/cbar_audits/CBAR_Audit_Phase*.md` | Adversarial resolution logic for why a rule exists and hallucination correction logs. |
| **Protocol** | `ERA3_Tech_Spec_Writing_Protocol.md` | Master execution order, existing backend architecture, and 10-section spec format template. |
| **Constraints** | `primitives/**/*.yaml` | Behavioral quality constraints governing friction, progression, social proof, and trust. |

## 4. The 34 Specs — Master Inventory
> **Status:** All 34 specs are currently **Not Started**.

### Phase 1 — Infrastructure
| # | Spec | Source PRD | Epic File | Story IDs | CBAR Mandates | Backend Relationship |
|---|---|---|---|---|---|---|
| 1 | FR-ERA3-08: Mini App Host Shell | PRD-01, 04 | Phase 1 | 1.1, 1.2, 1.3 | M-01, M-02, M-03 | **NEW** frontend. **CONSUMES** `dpa_engine.py` |
| 2 | FR-ERA3-06: Primitive Registry Query | PRD-08 | Phase 1 | 2.1, 2.2 | M-04, M-05 | **NEW** FastAPI service. **READS** `primitives/` |
| 3 | FR-ERA3-02: In-Chat Telegram Payments | PRD-09 | Phase 1 | 3.1, 3.2, 3.3 | M-06, M-07 | **NEW** payment. **CONSUMES** `offer_tier_governor.py` |

### Phase 2 — Conscious Reactions
| # | Spec | Source PRD | Epic File | Story IDs | CBAR Mandates | Backend Relationship |
|---|---|---|---|---|---|---|
| 4 | FR-ERA3-05-CORE: Core Engine | PRD-06 | Phase 2 | 1.1–1.4, 3.1–3.3, 4.1 | P2-M-01, 02, 03 | **NEW** engine. **REPLACES** `trivianar_engine_service.py` |
| 5 | FR-ERA3-05a: Solo Reaction | PRD-06 | Phase 2 | 2.1 | P2-M-04 | **NEW** Mini App. **CONSUMES** CORE |
| 6 | FR-ERA3-05b: Debate with Jury | PRD-06 | Phase 2 | 2.2 | P2-M-05 | **NEW** Mini App. **CONSUMES** CORE |
| 7 | FR-ERA3-05c: Reaction Duel | PRD-06 | Phase 2 | 2.3 | P2-M-06 | **NEW** Mini App. **CONSUMES** CORE |
| 8 | FR-ERA3-05d: Tierlist Authority | PRD-06 | Phase 2 | 5.1 | None | **NEW** Mini App. **CONSUMES** CORE |
| 9 | FR-ERA3-05e: Audience Mirror Quiz | PRD-06 | Phase 2 | 6.3 | None | **NEW** Mini App. **CONSUMES** CORE |
| 10 | FR-ERA3-05f: Blind Rank Reveal | PRD-06 | Phase 2 | 5.2 | None | **NEW** Mini App. **CONSUMES** CORE |
| 11 | FR-ERA3-05g: Alphabet Challenge | PRD-06 | Phase 2 | 6.1 | P2-M-07 | **NEW** Mini App. **CONSUMES** CORE |
| 12 | FR-ERA3-05h: Last One Standing | PRD-06 | Phase 2 | 5.3 | None | **NEW** Mini App. **CONSUMES** CORE |
| 13 | FR-ERA3-05i: Authority Quiz | PRD-06 | Phase 2 | 6.2 | None | **NEW** Mini App. **CONSUMES** CORE |
| 14 | FR-ERA3-05j: Ranking Quiz Co-Creation | PRD-06 | Phase 2 | 5.4 | None | **NEW** Mini App. **CONSUMES** CORE |

### Phase 3 — Experience Mini Apps
| # | Spec | Source PRD | Epic File | Story IDs | CBAR Mandates | Backend Relationship |
|---|---|---|---|---|---|---|
| 15 | FR-ERA3-01: Webinar Companion | PRD-07 | Phase 3 | 1.1, 1.2 | P3-M-01, 02 | **NEW** Mini App. **READS** v2ws data |
| 16 | FR-ERA3-11: Challenge Arena | PRD-05 | Phase 3 | 2.1, 2.2 | P3-M-03, 04 | **NEW** Mini App. **CONSUMES** `learning_path_builder.py` |
| 17 | FR-ERA3-09: Conscious Editor | PRD-02, 03 | Phase 3 | 3.1, 3.2 | P3-M-05 | **NEW** Mini App. **CONSUMES** `content_machine.py` |
| 18 | FR-ERA3-19: Testimonial Builder & Cards | PRD-05, 09 | Phase 3 | 4.1, 4.2 | P3-M-06 | **NEW** Mini App |
| 19 | Score Card Viewer | PRD-04, 05 | Phase 3 | 5.1 | None | **NEW** Mini App. **READS** `leadership_scorecard.json` |
| 20 | FR-ERA3-10: Onboarding Flow | PRD-01, 04 | Phase 3 | 6.1 | P3-M-07 | **NEW** Mini App |

### Phase 4 — Pipelines & Engines
| # | Spec | Source PRD | Epic File | Story IDs | CBAR Mandates | Backend Relationship |
|---|---|---|---|---|---|---|
| 21 | FR-ERA3-07: AFFiNE Broadcasting Pipeline | PRD-01, 07 | Phase 4 | 1.1 | P4-M-01 | **TBD** |
| 22 | FR-ERA3-12: OmniShotCut CMF Intelligence | PRD-03 | Phase 4 | 2.1 | P4-M-02 | **NEW** pipeline. **CONSUMES** Skia Renderer sidecar |
| 23 | FR-ERA3-13: Four-Surface Async Skill Ladder | PRD-04 | Phase 4 | 3.1 | P4-M-03 | **NEW** service. **CONSUMES** `learning_path_builder.py` |
| 24 | FR-ERA3-15: Trigger-First Execution Guard | PRD-02 | Phase 4 | 4.1 | P4-M-04 | **TBD** |
| 25 | FR-ERA3-16: Archetype Container Runtime | PRD-02 | Phase 4 | 5.1 | P4-M-05 | **TBD** |
| 26 | FR-ERA3-17: Voice Prompt Engine | PRD-04 | Phase 4 | 6.1 | P4-M-06 | **TBD** |
| 27 | FR-ERA3-18: CBCS Four-Engine Runtime | PRD-05 | Phase 4 | 7.1 | P4-M-07 | **TBD** |

### Phase 5 — Growth
| # | Spec | Source PRD | Epic File | Story IDs | CBAR Mandates | Backend Relationship |
|---|---|---|---|---|---|---|
| 28 | FR-ERA3-03: Silent Referral Architecture | PRD-09 | Phase 5 | 1.1, 1.2 | P5-M-01, 02 | **NEW** mechanism. **CONSUMES** `conversion_sequence_router.py` |
| 29 | FR-ERA3-04: OFO Engine | PRD-09 | Phase 5 | 2.1, 2.2 | P5-M-03, 04 | **NEW** service. |
| 30 | FR-ERA3-14: CAU Knowledge Transfer | PRD-01 | Phase 5 | 3.1 | P5-M-05 | **NEW** service. **READS** existing SKILL files |

### Phase 6 — Existing Spec Updates
| # | Spec | Source PRD | What Changes |
|---|---|---|---|
| 31 | FR-APR-08 | PRD-08 | Add primitive-loading mandate |
| 32 | FR-CA11-16 | PRD-07 | Add AFFiNE broadcast routing |
| 33 | FR-COM-01 | PRD-09 | Update pricing ($39.99/$99.99) |
| 34 | FR58 | PRD-09 | Align `OfferTierGovernor` tier ceilings |

## 5. The 33 CBAR Mandates — Quick Reference
| Phase | # | Mandate | Governing Primitive | Spec(s) Affected |
|---|---|---|---|---|
| **1** | M-01 | The Optimistic Render Rule | `EXP-FRC-002` | Spec 1 |
| **1** | M-02 | The Zero-Network Theme Rule | `EXP-TRS-001` | Spec 1 |
| **1** | M-03 | The Primer Screen Rule | `EXP-FRC-003` | Spec 1 |
| **1** | M-04 | The Hot-Reload Rule | `EXP-FBK-001` | Spec 2 |
| **1** | M-05 | The Deterministic Override Rule | Orchestration Engine | Spec 2 |
| **1** | M-06 | The Stored Value Rule | `EXP-PER-003` | Spec 3 |
| **1** | M-07 | The Payment Masking Rule | `EXP-FBK-001` | Spec 3 |
| **2** | M-01 | The Ephemeral Decay Mandate | `EXP-TRG-002` | Spec 4 (CORE) |
| **2** | M-02 | The Background Upload Rule | `EXP-FRC-003` | Spec 4 (CORE) |
| **2** | M-03 | The Streaming Audio SLA | `EXP-FBK-001` | Spec 4 (CORE) |
| **2** | M-04 | The Earned Export Gate | `EXP-PRG-002` | Spec 5 |
| **2** | M-05 | The Visual Adversary Rule | `EXP-SOC-002` | Spec 6 |
| **2** | M-06 | The Bracket Matchmaking Rule | `EXP-SOC-004` | Spec 7 |
| **2** | M-07 | The Client-Side Timing Rule | `EXP-FRC-006` | Spec 11 |
| **3** | M-01 | Ambient Prompt Rule | `EXP-TRS-003` | Spec 15 |
| **3** | M-02 | Per-Slide Feedback Rule | `EXP-FBK-001` | Spec 15 |
| **3** | M-03 | Lateral Progression Rule | `EXP-PRG-002` | Spec 16 |
| **3** | M-04 | Telemetry Surfacing Rule | `EXP-FBK-004` | Spec 16 |
| **3** | M-05 | Modular CMF Recovery Rule | `EXP-SAF-002` | Spec 17 |
| **3** | M-06 | Peer-Gated Apex Rule | `EXP-SOC-001` | Spec 18 |
| **3** | M-07 | Auth-Free Benchmark Rule | `EXP-FRC-002` | Spec 20 |
| **4** | M-01 | The Intelligence-Gated Intercept Rule | `EXP-PER-003` | Spec 21 |
| **4** | M-02 | The Cinematic Meaning Rule | `EXP-TRS-004` | Spec 22 |
| **4** | M-03 | The Inline Routing SLA | `EXP-PRG-001` | Spec 23 |
| **4** | M-04 | The Frictionless Block Rule | `EXP-FRC-006` | Spec 24 |
| **4** | M-05 | The Actionable Rejection Rule | `EXP-FBK-001` | Spec 25 |
| **4** | M-06 | The Sonic Prestige Rule | `EXP-TRS-003` | Spec 26 |
| **4** | M-07 | The Long Loop Framing Rule | `EXP-PRG-004` | Spec 27 |
| **5** | M-01 | The Verifiable Artifact Rule | `EXP-SOC-001` | Spec 28 |
| **5** | M-02 | The Earned Escalation Rule | `EXP-TRG-005` | Spec 28 |
| **5** | M-03 | The OFO Ego-Defense Rule | `EXP-TRS-004` | Spec 29 |
| **5** | M-04 | The Inline Capture Hook | `EXP-PRG-001` | Spec 29 |
| **5** | M-05 | The 1-Tap Paywall Rule | `EXP-FRC-002` | Spec 30 |

## 6. The 10-Section Spec Format (with CBAR integration)
Use this exact markdown structure for every new spec:

```markdown
## 1. Files Read
*Must explicitly list the PRD module, Epic file, and specific primitive YAMLs read.*

## 2. Overview
*The Problem, Solution, and Scope of the spec.*

## 3. Context for Development
### 3.1 Existing Backend Integration
*List exact Python files, tables, and API routes this extends.*
### 3.2 ADR-05 Primitives
*List specific YAML IDs and constraint summaries.*
### 3.3 CBAR Mandate Enforcement
*Example:* 
**Phase1-M1: The Optimistic Render Rule** (From Story 1.1)
- **How Enforced:** The React app `initData` is validated async. The first screen renders optimistically without waiting for backend approval.
### 3.4 Technical Decisions

## 4. Implementation Plan
*Staged roll-out referencing existing code.*

## 5. Primary Output Schema
*JSON/Pydantic schemas. Must extend existing `src/ccp/models/` where applicable.*

## 6. Backward Compatibility Fallback
*What happens if an old client hits the new route.*

## 7. Tasks
*Component-level breakdown.*

## 8. Acceptance Criteria
*Example:*
- **Given** I tap a Web App button
- **When** the shell loads
- **Then** it renders optimistically without blocking for network [CBAR Phase1-M1]
- **FAILURE EXAMPLE:** The UI shows a spinning loader waiting for `bot_token` validation.

## 9. Dependencies
*Internal services and external APIs.*

## 10. Testing Strategy
*How to test, mimicking the `tests/integration/` pattern.*
```

## 7. The 7-Step Pre-Flight Checklist
Before writing a spec, the writer must load the following files:
1. **Load PRD Module:** `docs/prd/modules/PRD_XX_*.md` (Extract NEW vs EXISTING).
2. **Load Referenced Specs:** Any existing spec referenced in the PRD's Brownfield Analysis.
3. **Map to Existing Backend:** Check `src/ccp/services/`, `src/ccp/models/`, `src/ccp/api/main.py`.
4. **Load Primitives:** `primitives/experience/**/*.yaml` based on the PRD's active primitive keys.
5. **Determine Mini App Separation:** Identify the specific `startapp` target (see §9).
6. **Cross-Reference PRD_INDEX:** Check `docs/prd/modules/PRD_INDEX.md` for overlaps.
7. **Load CBAR Epic:** `docs/architecture/april_updates/PhaseX_*_Epics.md` to extract mandates and User Stories.

## 8. Experience Primitive Families — Quick Reference
| Key | Family | What It Governs | YAML Directory Path |
|---|---|---|---|
| **TRG** | Trigger & Timing | When system speaks/sends | `primitives/experience/trigger_timing/` |
| **FRC** | Friction & Ability | Reducing cost of action | `primitives/experience/friction_ability/` |
| **TRS** | Trust & Status | Premium authority feel | `primitives/experience/trust_branding/` |
| **FBK** | Feedback & Scoring | Quality of score reveals | `primitives/experience/feedback_scoring/` |
| **PRG** | Progression & Replay | Visual advancement | `primitives/experience/progression_replay/` |
| **SOC** | Social & Referral | Converting to spread | `primitives/experience/social_referral/` |
| **SAF** | Safe Failure & Recovery | Pressure survivability | `primitives/experience/safe_failure_recovery/` |
| **PER** | Personalization & Identity | Identity accretion | `primitives/experience/personalization_identity/` |

## 9. Mini App Architecture Categories
The 14 Conscious Reactions elements fall into 4 distinct architectures:
- **Category A — Reaction Modes (Standalone Mini Apps):** Solo (`react_solo`), Debate (`react_debate`), Duel (`react_duel`).
- **Category B — User Roles (CORE Engine features):** Audience Jury, Supervisor Pairing, Vote Then React.
- **Category C — Options/Mechanics (CORE Engine features):** Redemption Round.
- **Category D — Content Creation (Standalone Mini Apps):** Tierlist (`react_tierlist`), Mirror Quiz (`react_mirror_quiz`), Blind Rank (`react_blind_rank`), Alphabet Challenge (`react_alphabet`), Last One Standing (`react_elimination`), Authority Quiz (`react_authority_quiz`), Ranking Quiz Co-Creation (`react_ranking_quiz`).

## 10. Execution Order & Dependencies
```text
Phase 1 (Infrastructure) -> Phase 2 (Conscious Reactions) -> Phase 3 (Experience Mini Apps) -> Phase 4 (Pipelines) -> Phase 5 (Growth)
```
- Spec 1 (Host Shell) must be understood before any Mini App specs.
- Spec 4 (CORE Engine) must be written before Specs 5-14 (Reaction/Content Mini Apps).
- Phase 4 services act as the backend logic for Phase 2/3 interfaces.

## 11. Existing Backend Quick Reference
- **API Gateway:** FastAPI `src/ccp/api/main.py`
- **DB:** Supabase (PostgreSQL) `src/ccp/scripts/setup_supabase.py`
- **Graph:** Neo4j `src/ccp/scripts/setup_neo4j.py`
- **Models:** Pydantic `src/ccp/models/` (45 files)
- **Services:** `src/ccp/services/` (201+ files), including `dpa_engine.py`, `content_machine.py`, `trait_scoring_engine.py`, `learning_path_builder.py`
- **Pipelines:** `src/ccp/pipelines/` (17 files)
- **Agents:** `src/ccp/agents/` (17 files)

## 12. Anti-Slop Mandate
> [!CAUTION]
> **STRICT RULES FOR SPEC WRITERS:**
> 1. **No hallucinated primitive IDs.** The `EXP-TRB-*` prefix is a known hallucination and MUST NOT be used. The correct prefix is `EXP-TRS-*` (Trust & Status). Every `EXP-*` ID must be verified against the YAML registry in `primitives/`.
> 2. **No speculative architecture.** Every service, model, and route must trace to an existing backend file or be explicitly marked `[NEW]`.
> 3. **No CBAR mandate gaps.** Every spec MUST declare its applicable mandates in Section 3 and enforce them in Section 8 Acceptance Criteria.
> 4. **No format deviations.** The 10-section format is mandatory.
> 5. **Phase 2 Epics file formatting:** Note that the Phase 2 Epics file lists mandates at the *bottom*, not the top.

## 13. Quality Gates
Before marking a spec "Ready for Development", verify:
- [ ] Section 1 lists ALL read files (PRD, Epic, Primitives, existing code).
- [ ] Section 3 includes exact Python file paths in "Existing Backend Integration".
- [ ] Section 3 includes "CBAR Mandate Enforcement" block.
- [ ] Section 3 references specific YAML IDs (not just family names).
- [ ] Section 8 Acceptance Criteria include FAILURE EXAMPLES and CBAR references.
- [ ] All primitive IDs verified against YAML registry.
- [ ] Backend relationship is explicit (NEW / CONSUMES / REPLACES / READS).
- [ ] New models follow the existing Pydantic pattern.
- [ ] Testing strategy references existing pytest patterns.

## 14. File Paths — Complete Reference
| File | Path | Purpose |
|---|---|---|
| Master Protocol | `docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md` | Master execution tracking & architecture state |
| PRD Index | `docs/prd/modules/PRD_INDEX.md` | PRD routing & cross-referencing |
| PRD Modules | `docs/prd/modules/PRD_01-09_*.md` | Source of truth functional requirements |
| Phase Epics | `docs/architecture/april_updates/Phase1-5_*_Epics.md` | Stories, ACs, and CBAR mandates |
| CBAR Audits | `docs/architecture/cbar_audits/CBAR_Audit_Phase1-5_*.md` | Hallucination correction logs & logic |
| CBAR Protocol | `docs/architecture/spec updates/CBAR_Constraint_Based_Adversarial_Reasoning.md` | Reason framework definition |
| Story Protocol | `docs/architecture/april_updates/ERA3_Epic_and_Story_Writing_Protocol.md` | How Epics map to specs |
| Primitives | `primitives/experience/`, `primitives/meaning/` | YAML registries for constraints |
| FastAPI App | `src/ccp/api/main.py` | API Entry point |
| Models/Services | `src/ccp/models/`, `src/ccp/services/` | Existing backend implementation |
| DB Scripts | `src/ccp/scripts/setup_supabase.py`, `setup_neo4j.py` | Database schemas |
| Legacy Specs | `docs/architecture/april_updates/previous specs/FR-APR-*.md` | SUPERSEDED examples, do not use format |
| CA11 Example | `docs/architecture/FR-CA11-01_Coach_Workspace_Provisioning_Tech_Spec.md` | Deepest spec example (reference only) |
