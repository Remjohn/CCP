# Spec Audit Report: Batch D — Capability Area 11 (Phase 4 - CCP Studio)

**Review Date:** 2026-03-26
**Reviewer:** Principal CCP Architecture Reviewer
**Scope:** FR-CA11-16 through FR-CA11-22 (7 specs)

---

## AUDIT SUMMARY

- **Total specs reviewed:** 7
- **Specs with zero flags:** 3
- **Total CRITICAL flags:** 1
- **Total WARNING flags:** 2
- **Total NOTE flags:** 3
- **Cross-spec consistency issues requiring arbitration:** 2

---

## PASS 
*(Specs with zero flags across all five lenses)*

- **FR-CA11-16 — CCP Studio Block (Recording & Streaming)**
- **FR-CA11-18 — Conscious Social Scheduling & Performance Analysis**
- **FR-CA11-22 — Stream Overlay & Trivianar Display**

---

## FLAGS

### FR-CA11-19 | LENS 5 | CRITICAL
- **Finding:** Identifier namespace collision separating session telemetries. FR-CA11-19 uses `stream_id` (UUID) throughout its data model (`trivia_responses`) and endpoints. However, FR-CA11-16 (the Studio Block) generates a `session_id` (UUID) in the `studio_sessions` table which technically represents the exact same event. If the trivia engine and the studio block use disconnected IDs, analytics cannot join stream data with trivia data.
- **Location:** Section 5 (Data Model) & Section 4 Stage 1.
- **Required Action:** Update FR-CA11-19 to explicitly declare that `stream_id` is a direct Foreign Key reference to `studio_sessions.id` (from FR-CA11-16) to guarantee referential integrity across the quad-platform layer.

### FR-CA11-20 | LENS 4 | WARNING
- **Finding:** Missing Receipt Chain Guard integration. Stage 1 inserts a new lead into `trivia_leads` and Stage 2 updates it with contact info, but no `receipt_chain_guard` (DEP-ENG-041) write is mandated. All system state mutations involving PII/lead acquisition must be cryptographically receipted in CCP Architecture.
- **Location:** Section 4 (Implementation Plan) - Stages 1 & 2.
- **Required Action:** Add a Receipt Chain Guard write step at the end of Stage 2 (or upon contact capture) to securely document the data acquisition event.

### FR-CA11-20 | LENS 5 | WARNING
- **Finding:** Unclear relationship between user identities. FR-CA11-20 creates `trivia_leads` with `telegram_user_id` (BIGINT). FR-CA11-19 uses `user_id` (BIGINT) in `trivia_responses`.
- **Location:** Section 5 (Data Model).
- **Required Action:** Ensure both specs explicitly state that these fields represent the exact same Telegram internal ID, and consider adding an FK from `trivia_responses.user_id` to `trivia_leads.telegram_user_id` (or vice versa) so leads can be joined to their responses natively.

### FR-CA11-17 | LENS 4 | NOTE
- **Finding:** Missing Receipt documentation for preferences update. Stage 4 saves new custom audio selections to the `studio_preferences` JSONB fields without emitting a receipt. While this is low-risk configuration data, the PRD mandates receipts for all data mutations.
- **Location:** Section 4 Stage 4.
- **Required Action:** Add a small step to write a configuration-change receipt to the Receipt Chain Guard.

### FR-CA11-19 | LENS 4 | NOTE
- **Finding:** Lack of explicit handling for high-volume receipting. Stage 3 (Qualifying Questions) inserts responses into `trivia_responses`. Writing a receipt for every single trivia button press (potentially thousands per stream) will overwhelm the Receipt Chain constraint.
- **Location:** Section 4 Stage 3.
- **Required Action:** The spec must explicitly declare an "exemption" for individual `trivia_responses` to avoid single-row receipting, OR it must specify a post-stream "Batch Receipt" that hashes the entire stream's response set into a single Receipt Chain entry.

### FR-CA11-21 | LENS 4 | NOTE
- **Finding:** Missing Receipt for guest session creation. The `studio_guest_sessions` table is updated when a guest connects/disconnects, but no receipt is logged.
- **Location:** Section 4 Stage 2.
- **Required Action:** Add a Receipt Chain Guard write when the `join_token` is exhausted/used.
