# Tech-Spec: FR-GA — Guardian Agent (Capability Area 0)

**Created:** 2026-03-18
**Status:** Ready for Development
**Version:** 2.0 (Aligned to CCP Architecture V2)
**Architecture Reference:** CCP_Architecture_Documentation_V2 §2–§8, PRD §Capability Area 0 (FR-GA)

---

## Overview

### Problem Statement
Foundational intelligence pipelines require sequential execution, strict quality gates, and ongoing relevance tracking. Without a central orchestrator, data degrades (stale lexicons, campaign fatigue), and downstream pipelines execute against unverified or failing inputs. 

### Solution
The Guardian Agent orchestrates the Pre-Production Intelligence Layer in two modes:
- **Genesis Mode:** Executes FR0A → FR0B → FR0C → FR0D → FR0E. Issues the Genesis Clearance Certificate (DEP-ENG-052).
- **Stewardship Mode:** Weekly Signal Monitoring Protocol detects drift/fatigue. Recommends refreshes (requiring human approval).

### Scope
**In scope:**
- Genesis Mode (Pipeline orchestration, verdict logic, DEP-ENG-052 issuance)
- 5-Phase Interview Protocol (DEP-PROTO-019) orchestration
- Stewardship Mode (Signal Monitoring Protocol: DEP-PROTO-020)
- Slash Command Architecture (`/ccf-guardian`, `/ccf-interview`)

**Crisis Response Origin Bifurcation:**
When the Circuit Breaker trips on a crisis keyword, the routing logic MUST check the originator ID.
1. `If client_id matches audience_db:` Halt pipeline, log event, push Telegram SOS to human coach.
2. `If client_id matches coach_master_id:` Halt pipeline, suppress Coach Telegram routing (prevents dangerous loop), and instantly route an SOS webhook directly to the central System Operator.

---

## Context for Development

### Architecture Traceability
| DEP-ID | Name | Role | Producing FR | Consuming FRs |
|---|---|---|---|---|
| `PROPOSED: DEP-ENG-052` | Genesis Clearance Certificate | Immutable proof that production foundation is authenticated | FR-GA | FR1 (prerequisite gate) |
| `PROPOSED: DEP-ENG-053` | Stewardship Report | Quarterly foundational relevance audit | FR-GA (Steward) | Operator review |
| `PROPOSED: DEP-PROTO-019` | 5-Phase Interview Protocol | OARS-structured onboarding interview specification | FR-GA (Genesis) | FR0A, FR0B seed |
| `PROPOSED: DEP-PROTO-020` | Signal Monitoring Protocol | 3-dimension weekly drift detection specification | FR-GA (Steward) | Background ops |

### Agent Roster
| Agent | Role |
|---|---|
| **Guardian Agent** | Sequential orchestrator for all 5 stages, issues decisions/verdicts |

### Technical Decisions
| Decision | Rationale | ADR-01 Impact |
|---|---|---|
| **Sequential vs. Parallel** | FR0B requires FR0A's audience parameters. Pipeline strict sequence prevents orphaned objects. | All reads/writes scoped to coach tenant. |
| **Operator Approval (Stewardship)** | The system never autonomously overwrites its foundation to prevent cascading, unpredictable changes downstream. | Action execution filtered to coach tenant requests. |

---

## Implementation Plan

### Guardian Agent — Genesis Mode Orchestration

#### Genesis Flow
1. **5-Phase Interview Protocol (DEP-PROTO-019)**: OARS-structured Telegram conversation.
2. **Stage 3a. Collision DNA Extraction & Invariance Check:** Before generating `coach_soul.json`, the Guardian Agent must execute the 3-Topic Invariance Test. The agent pulls transcripts from three maximally different coaching topics. If the identified Collision DNA signature does not exist mathematically across all three segments, it is flagged as topic-specific modulation and discarded. Only invariant structures proceed to `DEP-ENG-003`.
3. **FR0A (Business Intel)** → Verdict
3. **FR0B (Tribe Soul)** → Verdict
4. **FR0C (Characters)** → Verdict
5. **FR0D (Semiotic)** → Verdict
6. **FR0E (Brand Avatars)** → Verdict
7. **Genesis Clearance Certificate (DEP-ENG-052)** Issued upon all PASS.

#### Verdict Logic
| Verdict | Condition | Downstream Effect |
|---|---|---|
| **AUTHENTICATED** | All quality gates pass. | Full production clearance. |
| **PROVISIONAL** | Minimum viable quality met. Specific gaps flagged. | Production permitted with degradation flag. Operator warned. |
| **FAILED** | Quality gate not met. | Pipeline HALTS. Must intervene. |

#### Genesis Clearance Certificate (DEP-ENG-052)
Stores `stage_verdicts`, `provisional_gaps[]`, `receipt_chain_root`, `is_valid`.

---

### Guardian Agent — Stewardship Mode

#### Authenticity Floor Calibration:
The LIWC-22 generic authenticity floor is 7/10. However, during Genesis, the Guardian Agent extracts an `authentic_multiplier` for the specific coach. If a coach's natural, high-engagement speech scores a baseline of 5/10, the pipeline floor adjusts dynamically to 4/10. The 7/10 floor is NOT an immutable ceiling for naturally stoic profiles.

**Evolutionary Recalibration Handshake:**
To prevent the "Coach Straitjacket" effect where Sophia rejects genuine growth, the Signal Monitoring Protocol evaluates TTT drift contextually. If a coach sustains a `>15%` drift towards a *new* authentic vector for 4 consecutive weeks, the Guardian Agent does not quarantine the content. Instead, it mechanically triggers a `DEP-ENG-005` Re-Extraction Event. Sophia's baseline is permanently updated to the new parameters. The system architecture expects and adapts to human psychological evolution.

**Data Promotion Timeout Deadlock:**
Azaria requires System Operator approval to promote patterns from Episodic to Semantic memory. If a pattern achieves the 14-consecutive-session threshold and sits unreviewed in the queue for 21 days, Azaria escalates the pattern status from `PENDING` to `CRITICAL_BLOCKING`. The coach's weekly pipeline execution is mathematically halted until the operator resolves the queue. There is NO silent auto-promotion bypass.

#### Signal Monitoring Protocol (DEP-PROTO-020)
Runs weekly. Monitors 3 signal categories:
1. **Lexicon Drift:** Unmapped vocabulary detected. Triggers recommendation for Tribe Lexicon addition.
2. **Cultural Evolution:** CMM tensions shift or character relevance drops below 0.4. Recommends partial dossier refresh or character rescore.
3. **Campaign Fatigue:** Semiotic combo conversions drop or character repeats >3 times in 8 weeks. Adjusts deployment weights.

#### Stewardship Report (DEP-ENG-053)
Quarterly compiled output. Includes relevance assessments, signal occurrences, logged approved refreshes, and upcoming recommendations.

---

### Slash Command Integration
Context Window Management: Each command loads only relevant state boundary variables.
- `/ccf-guardian genesis` / `status` / `approve [id]` / `refresh [component]`
- `/ccf-interview start` / `resume [phase]` / `status`

---

## Backward Compatibility Fallback
| Scenario | Fallback |
|---|---|
| **Existing coaches without Cap Area 0** | Operator runs Genesis Mode retroactively. Guardian Agent issues PROVISIONAL clearance. |
| **Genesis Clearance Certificate pending** | Manual operator override logged as `genesis_certificate_override: true`. |

---

## Tasks

- [ ] **Task 1:** Implement Guardian Agent orchestrator — Genesis Mode gate checks (sequential execution, verdict logic, certificate issuance)
- [ ] **Task 2:** Build 5-Phase Interview Protocol (DEP-PROTO-019)
- [ ] **Task 3:** Implement Genesis Clearance Certificate (DEP-ENG-052)
- [ ] **Task 4:** Implement Stewardship Mode — Signal Monitoring Protocol (DEP-PROTO-020) + Stewardship Report (DEP-ENG-053) + Operator Approval workflow
- [ ] **Task 5:** Implement Slash Command architecture (`/ccf-guardian`, `/ccf-interview` families)

---

## Acceptance Criteria

- [ ] **AC1 (Production Lock):** Without a Genesis Clearance Certificate (DEP-ENG-052), triggering FR1's `ccf-init` returns `GENESIS_CLEARANCE_REQUIRED` — code-level gate. Test: attempt FR1 without certificate → verify hard rejection.
- [ ] **AC2 (Stewardship Signal Detection):** When 5+ `character_lexicon` entries drop below `relevance_score` 0.4, Stewardship Mode generates a Cultural Evolution Signal.
- [ ] **AC3 (Operator Approval):** A Stewardship refresh recommendation is NOT executed until `/ccf-guardian approve [recommendation_id]` is issued.
- [ ] **AC4 (Receipt Chain Integrity):** After complete Genesis Mode execution, all receipts are stored in Supabase `receipts` table with resolvable `predecessor_receipt_id`.

---

## Dependencies

| Dependency | Type | Notes |
|---|---|---|
| FR1 Genesis Pipeline | Internal downstream | Cannot execute without GA Clearance |
| Telegram Bot API | External service | Slash commands, operator approvals |
| LangGraph | Internal framework | Agent orchestration + Guardian Agent state management |

---

## Testing Strategy

### Genesis Mode Integration Test
- Run complete Genesis Mode against a test coach instance.
- Validate strict sequential order and halting on FAILED verdicts.
- Validate Receipt chain integrity.

### Slash Command State Test
- Invoke `/ccf-interview start` then interrupt.
- Validate `/ccf-interview resume` restores only the boundary state context.
