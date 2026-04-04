# Implementation Plan — Chapter 9 Unit 1: AFFiNE Architecture — CRDT & BlockSuite

This plan outlines the authoring of Unit 9.1 for the Launch Manual, focusing on the architectural transition from Notion to a self-hosted, thin-forked AFFiNE instance. The unit will bridge the gap between backend agentic intelligence and frontend delivery, explaining the Conflict-free Replicated Data Type (CRDT) mechanics that allow 76 agents to write headlessly to a coach's workspace without collisions.

## User Review Required

> [!IMPORTANT]
> **Architectural Shift:** This unit formalizes the retirement of Notion (ADR-02) in favor of AFFiNE (ADR-05). 
> **Word Count Mandate:** The unit will be strictly 700-1140 words, adhering to the Eight-Section Expansion Protocol.
> **Fact-Check:** 2026 technical status for BlockSuite, Yjs, and OctoBase has been verified.

## Proposed Changes

### [Launch Manual Chapter 09: Coach Dashboard]

#### [NEW] [Unit_9.1_AFFiNE_Architecture_CRDT_BlockSuite.md](file:///d:/Work/The%20Conscious%20Coaching%20Factory/Conscious%20Architect%20University/Launch%20Manual/Chapter_09_Coach_Dashboard/Units/Unit_9.1_AFFiNE_Architecture_CRDT_BlockSuite.md)
Expansion of Unit 9.1 into an 8-section action unit:
1.  **🧠 THE SCIENCE:** First Principles of **Conflict-Free Convergence**. Why state merging is superior to state locking. Analogy: **Hippocampal Indexing** — how the brain maintains a flat associative map that masks as a hierarchy.
2.  **🧠 TECHNICAL KNOWLEDGE:** Deconstruction of the BlockSuite stack. The `@blocksuite/store` as the headless data layer. Yjs as the synchronization protocol. OctoBase as the Rust-powered persistence layer.
3.  **📂 OUR CODE:** References to `docs/MCDA_AFFiNE_Integration_Analysis.md` and the upcoming `affine_sync.py`. Annotating the "Thin Fork" strategy goals.
4.  **🤖 AGENT PROMPT:** [Optional] Prompt for generating a headless AFFiNE writer that inserts a "Session Recap" block into a workspace.
5.  **⌨️ TERMINAL:** [Optional] Commands for starting the AFFiNE self-hosted Docker Compose stack.
6.  **✅ IMPLEMENTATION STEPS:** Reading the MCDA, understanding the BlockSuite store API, and mapping the 76-agent write pipeline to the CRDT model.
7.  **✅ VERIFY:** Concrete check: AFFiNE server responds on localhost with an active workspace ID.
8.  **🔗 BRIDGE:** Transition to Unit 9.2: Workspace Provisioning — Coach Isolation.

## Open Questions

- Should we include the `y-octo` Rust implementation details or focus on the TypeScript `yjs` API surface for the student? (Recommendation: Keep it at the TypeScript/Architecture level for mastery).

## Verification Plan

### Automated Tests
- Word count verification: 700-1140 words.
- Structural verification: All 8 sections present in order.
- Fact-check verification: `<!-- FACT-CHECK -->` comments for BlockSuite, Yjs, and OctoBase 2026 status.

### Manual Verification
- Ensure the **Hippocampal Indexing** analogy is technically precise.
- Verify the **Warm Precision (L4)** tone and absence of **Forbidden Vocabulary**.
