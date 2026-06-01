# ERA3 Spec Prompts — Master Index

> Each file in this folder is a **complete, ready-to-paste prompt** for writing one Era 3 Tech Spec.
> Copy the file contents → paste into a clean session → the agent reads the required files and writes the spec.
>
> **Prerequisite:** The session should have `ERA3_Spec_Writing_Briefing.md` loaded as context, OR the agent must read `docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md` as Step 1 of the Pre-Work Log.
>
> **Recommended session strategy:** Run one Phase per session (see batching below).

---

## Execution Order & Dependency Map

> [!IMPORTANT]
> Phase 1 specs have zero dependencies. Phase 2 specs depend on Phase 1. Do NOT write Phase 2 specs before Phase 1 specs are complete and reviewed.

```
Phase 1 (Foundation — write first)
  └── S01 FR-ERA3-08 Host Shell
  └── S02 FR-ERA3-06 Primitive Registry
  └── S03 FR-ERA3-02 Payments

Phase 2 (depends on Phase 1)
  └── S04 FR-ERA3-05-CORE  ← write this before any other Phase 2 spec
      ├── S05 FR-ERA3-05a Solo Reaction
      ├── S06 FR-ERA3-05b Debate with Jury
      ├── S07 FR-ERA3-05c Reaction Duel
      ├── S08 FR-ERA3-05d Tierlist Authority
      ├── S09 FR-ERA3-05e Audience Mirror Quiz
      ├── S10 FR-ERA3-05f Blind Rank Reveal
      ├── S11 FR-ERA3-05g Alphabet Challenge
      ├── S12 FR-ERA3-05h Last One Standing
      ├── S13 FR-ERA3-05i Authority Quiz
      └── S14 FR-ERA3-05j Ranking Quiz Co-Creation

Phase 3 (depends on Phase 1, partially Phase 2)
  ├── S15 FR-ERA3-01 Webinar Companion
  ├── S16 FR-ERA3-11 Challenge Arena
  ├── S17 FR-ERA3-09 Conscious Editor
  ├── S18 FR-ERA3-19 Testimonial Builder & User Cards
  ├── S19 Score Card Viewer
  └── S20 FR-ERA3-10 Onboarding Flow

Phase 4 (depends on Phase 1-3 — AUDIT backend services first)
  ├── S21 FR-ERA3-07 AFFiNE Broadcasting Pipeline
  ├── S22 FR-ERA3-12 CMF Arc-Governed Rendering
  ├── S23 FR-ERA3-13 Four-Surface Async Skill Ladder
  ├── S24 FR-ERA3-15 Trigger-First Execution Guard
  ├── S25 FR-ERA3-16 Archetype Container Runtime
  ├── S26 FR-ERA3-17 Voice Prompt Engine
  └── S27 FR-ERA3-18 CBCS Four-Engine Runtime

Phase 5 (depends on Phase 1-4)
  ├── S28 FR-ERA3-03 Silent Referral Architecture
  ├── S29 FR-ERA3-04 OFO Engine
  └── S30 FR-ERA3-14 Stealth Course Commercial Ladder

Phase 6 (spec updates — can run in parallel with Phase 4-5)
  ├── S31 FR-APR-08 Update: ADR-05 + Dual-Source
  ├── S32 FR-CA11-16 Update: AFFiNE Broadcast Path
  ├── S33 FR-COM-01 Update: Pricing Tiers
  └── S34 FR58 Update: Offer Tier Governor

Phase 7 (Living Commentary & Coach Communication Stack)
  ├── Wave A: CMF & Archetype Updates (S58-S59)
  ├── Wave B: Eval & Scorecard Updates (S60-S61)
  ├── Wave C: Coach Communication Modules (S62-S65)
  ├── Wave D: Speaking & Webinar Programs (S66-S69)
  ├── Wave E: Global Supervisor & Workflow (S70-S74)
  └── Wave F: Extensions & Intelligence (S75-S79)
```

---

## Full Spec Inventory

| # | File | Spec ID | Title | Phase | CBAR Mandates | Status |
|---|------|---------|-------|-------|---------------|--------|
| 01 | P1_S01_FR-ERA3-08_Mini_App_Host_Shell.md | FR-ERA3-08 | Mini App Host Shell | 1 | P1-M01, P1-M02, P1-M03 | 🔲 Not Started |
| 02 | P1_S02_FR-ERA3-06_Primitive_Registry_Query_Service.md | FR-ERA3-06 | Primitive Registry Query Service | 1 | P1-M04, P1-M05 | 🔲 Not Started |
| 03 | P1_S03_FR-ERA3-02_In_Chat_Telegram_Payments.md | FR-ERA3-02 | In-Chat Telegram Payments | 1 | P1-M06, P1-M07 | 🔲 Not Started |
| 04 | P2_S04_FR-ERA3-05-CORE_Core_Reaction_Engine.md | FR-ERA3-05-CORE | Core Reaction Engine | 2 | P2-M01, P2-M02, P2-M03, P2-M04 | 🔲 Not Started |
| 05 | P2_S05_FR-ERA3-05a_Solo_Reaction.md | FR-ERA3-05a | Solo Reaction Mini App | 2 | P2-M04 | 🔲 Not Started |
| 06 | P2_S06_FR-ERA3-05b_Debate_With_Jury.md | FR-ERA3-05b | Debate with Jury Mini App | 2 | P2-M05 | 🔲 Not Started |
| 07 | P2_S07_FR-ERA3-05c_Reaction_Duel.md | FR-ERA3-05c | Reaction Duel Mini App | 2 | P2-M06 | 🔲 Not Started |
| 08 | P2_S08_FR-ERA3-05d_Tierlist_Authority.md | FR-ERA3-05d | Tierlist Authority Mini App | 2 | (CORE inherited) | 🔲 Not Started |
| 09 | P2_S09_FR-ERA3-05e_Audience_Mirror_Quiz.md | FR-ERA3-05e | Audience Mirror Quiz Mini App | 2 | (CORE inherited) | 🔲 Not Started |
| 10 | P2_S10_FR-ERA3-05f_Blind_Rank_Reveal.md | FR-ERA3-05f | Blind Rank Reveal Mini App | 2 | (CORE inherited) | 🔲 Not Started |
| 11 | P2_S11_FR-ERA3-05g_Alphabet_Challenge.md | FR-ERA3-05g | Alphabet Challenge Mini App | 2 | P2-M07 | 🔲 Not Started |
| 12 | P2_S12_FR-ERA3-05h_Last_One_Standing.md | FR-ERA3-05h | Last One Standing Mini App | 2 | (CORE inherited) | 🔲 Not Started |
| 13 | P2_S13_FR-ERA3-05i_Authority_Quiz.md | FR-ERA3-05i | Authority Quiz Mini App | 2 | (CORE inherited) | 🔲 Not Started |
| 14 | P2_S14_FR-ERA3-05j_Ranking_Quiz_Co_Creation.md | FR-ERA3-05j | Ranking Quiz Co-Creation Mini App | 2 | (CORE inherited) | 🔲 Not Started |
| 15 | P3_S15_FR-ERA3-01_Webinar_Companion.md | FR-ERA3-01 | Webinar Companion Mini App | 3 | P3-M01, P3-M02 | 🔲 Not Started |
| 16 | P3_S16_FR-ERA3-11_Challenge_Arena.md | FR-ERA3-11 | Challenge Arena Mini App | 3 | P3-M03, P3-M04 | 🔲 Not Started |
| 17 | P3_S17_FR-ERA3-09_Conscious_Editor.md | FR-ERA3-09 | Conscious Editor Mini App | 3 | P3-M05 | 🔲 Not Started |
| 18 | P3_S18_FR-ERA3-19_Testimonial_Builder_User_Cards.md | FR-ERA3-19 | Testimonial Builder & User Cards | 3 | P3-M06 (FATAL CONFLICT) | 🔲 Not Started |
| 19 | P3_S19_Score_Card_Viewer.md | FR-ERA3-ScoreCard | Score Card Viewer Mini App | 3 | (EXP-FBK-001) | 🔲 Not Started |
| 20 | P3_S20_FR-ERA3-10_Onboarding_Flow.md | FR-ERA3-10 | Zero-Config Onboarding Flow | 3 | P3-M07 | 🔲 Not Started |
| 21 | P4_S21_FR-ERA3-07_AFFiNE_Broadcasting_Pipeline.md | FR-ERA3-07 | AFFiNE Studio Block Orchestration | 4 | P4-M01 | 🔲 Not Started |
| 22 | P4_S22_FR-ERA3-12_CMF_Arc_Governed_Rendering.md | FR-ERA3-12 | CMF Arc-Governed Rendering | 4 | P4-M02 | 🔲 Not Started |
| 23 | P4_S23_FR-ERA3-13_Four_Surface_Async_Skill_Ladder.md | FR-ERA3-13 | Four-Surface Async Skill Ladder | 4 | P4-M03 | 🔲 Not Started |
| 24 | P4_S24_FR-ERA3-15_Trigger_First_Execution_Guard.md | FR-ERA3-15 | Trigger-First Execution Guard | 4 | P4-M04 | 🔲 Not Started |
| 25 | P4_S25_FR-ERA3-16_Archetype_Container_Runtime.md | FR-ERA3-16 | Archetype Container Runtime | 4 | P4-M05 | 🔲 Not Started |
| 26 | P4_S26_FR-ERA3-17_Voice_Prompt_Engine.md | FR-ERA3-17 | Voice Prompt Engine | 4 | P4-M06 | 🔲 Not Started |
| 27 | P4_S27_FR-ERA3-18_CBCS_Four_Engine_Runtime.md | FR-ERA3-18 | CBCS Four-Engine Runtime | 4 | P4-M07 | 🔲 Not Started |
| 28 | P5_S28_FR-ERA3-03_Silent_Referral_Architecture.md | FR-ERA3-03 | Silent Referral Architecture | 5 | P5-M01, P5-M02 | 🔲 Not Started |
| 29 | P5_S29_FR-ERA3-04_OFO_Engine.md | FR-ERA3-04 | OFO Engine | 5 | P5-M03, P5-M04 | 🔲 Not Started |
| 30 | P5_S30_FR-ERA3-14_Stealth_Course_Commercial_Ladder.md | FR-ERA3-14 | B2B2C Commercial Ladder & Stealth Course | 5 | P5-M05 | 🔲 Not Started |
| 31 | P6_S31_FR-APR-08_Update_ADR05_Dual_Source.md | FR-APR-08 | UPDATE: ADR-05 + Dual-Source | 6 | N/A | 🔲 Not Started |
| 32 | P6_S32_FR-CA11-16_Update_AFFiNE_Broadcast_Path.md | FR-CA11-16 | UPDATE: AFFiNE Broadcast Path | 6 | N/A | 🔲 Not Started |
| 33 | P6_S33_FR-COM-01_Update_Pricing_Tiers.md | FR-COM-01 | UPDATE: Pricing Tiers | 6 | N/A | 🔲 Not Started |
| 34 | P6_S34_FR58_Update_Offer_Tier_Architecture.md | FR58 | UPDATE: Offer Tier Governor | 6 | N/A | 🔲 Not Started |
| 35 | P7_S58_Update_FR-ERA3-12_CMF_Arc_Governed_Rendering_for_Living_Commentary.md | FR-ERA3-12 | Update CMF Arc Governed Rendering | 7 | N/A | 🔲 Not Started |
| 36 | P7_S59_Update_FR-ERA3-16_Archetype_Container_Runtime_for_Living_Commentary_Bundles.md | FR-ERA3-16 | Update Archetype Container Runtime | 7 | N/A | 🔲 Not Started |
| 37 | P7_S60_Update_FR-ERA3-35B_Content_Benchmark_Profiles_for_Presence_Weighted_Living_Commentary.md | FR-ERA3-35B | Update Content Benchmark Profiles | 7 | N/A | 🔲 Not Started |
| 38 | P7_S61_Update_FR-ERA3-35C_Eval_Card_System_for_Living_Commentary_And_SSS.md | FR-ERA3-35C | Update Eval Card System for SSS | 7 | N/A | 🔲 Not Started |
| 39 | P7_S62_FR-ERA3-48_Persuasive_Speaking_Program_Runtime_And_Telemetry.md | FR-ERA3-48 | Persuasive Speaking Program Runtime | 7 | N/A | 🔲 Not Started |
| 40 | P7_S63_FR-ERA3-50A_Communication_Module_Library_And_Primitive_Crosswalk.md | FR-ERA3-50A | Communication Module Library | 7 | N/A | 🔲 Not Started |
| 41 | P7_S64_FR-ERA3-50C_Communication_Module_Recipe_Library_And_Delivery_Patterns.md | FR-ERA3-50C | Communication Module Recipe Library | 7 | N/A | 🔲 Not Started |
| 42 | P7_S65_FR-ERA3-50D_Persuasive_State_Shift_Evaluator_And_Delivery_Scoring.md | FR-ERA3-50D | Persuasive State Shift Evaluator | 7 | N/A | 🔲 Not Started |
| 43 | P7_S66_FR-ERA3-49A_Seminar_Speaking_Score_Card_And_Badge_Runtime.md | FR-ERA3-49A | Seminar Speaking Score Card Runtime | 7 | N/A | 🔲 Not Started |
| 44 | P7_S67_FR-ERA3-49_Transformational_Webinar_Program_And_Module_Compiler.md | FR-ERA3-49 | Transformational Webinar Program | 7 | N/A | 🔲 Not Started |
| 45 | P7_S68_Update_Voice_To_Lesson_Runtime_for_FR-ERA3-50.md | FR-ERA3-50 | Update Voice-To-Lesson Runtime | 7 | N/A | 🔲 Not Started |
| 46 | P7_S69_Update_FR-ERA3-01_Webinar_Companion_for_Recorded_Distribution_And_Telegram_Discussion.md | FR-ERA3-01 | Update Webinar Companion | 7 | N/A | 🔲 Not Started |
| 47 | P7_S70_FR-ERA3-45_Telegram_Webinar_Moderator_Bot.md | FR-ERA3-45 | Telegram Webinar Moderator Bot | 7 | N/A | 🔲 Not Started |
| 48 | P7_S71_FR-ERA3-41_Global_Signal_Telemetry_Constitution.md | FR-ERA3-41 | Global Signal Telemetry Constitution | 7 | N/A | 🔲 Not Started |
| 49 | P7_S72_FR-ERA3-42_Global_Supervisor_Agent.md | FR-ERA3-42 | Global Supervisor Agent | 7 | N/A | 🔲 Not Started |
| 50 | P7_S73_FR-ERA3-55_CCP_Workflow_And_Pipeline_Registry.md | FR-ERA3-55 | CCP Workflow And Pipeline Registry | 7 | N/A | 🔲 Not Started |
| 51 | P7_S74_FR-ERA3-56_Command_Surface_And_Experience_Router.md | FR-ERA3-56 | Command Surface And Experience Router | 7 | N/A | 🔲 Not Started |
| 52 | P7_S75_Update_FR39_Pi_Extension_Harness_for_ERA3_Execution_Graph.md | FR39 | Update Pi Extension Harness (Graph) | 7 | N/A | 🔲 Not Started |
| 53 | P7_S76_Update_FR39_Pi_Extension_Harness_for_Semantic_And_Perceptual_Extensions.md | FR39 | Update Pi Harness (Semantic) | 7 | N/A | 🔲 Not Started |
| 54 | P7_S77_Update_FR39_Pi_Extension_Harness_for_SCRE_And_SVRE_Operations.md | FR39 | Update Pi Harness (SCRE/SVRE) | 7 | N/A | 🔲 Not Started |
| 55 | P7_S78_FR-ERA3-50E_Expressive_Memory_Bank_And_Proof_Archive.md | FR-ERA3-50E | Expressive Memory Bank | 7 | N/A | 🔲 Not Started |
| 56 | P7_S79_FR-ERA3-50F_Objection_Intelligence_And_Response_Compiler.md | FR-ERA3-50F | Objection Intelligence Compiler | 7 | N/A | 🔲 Not Started |

---

## Recommended Session Batching (7 sessions total)

| Session | Files to Paste | Specs |
|---------|---------------|-------|
| Session A | P1_S01 + P1_S02 + P1_S03 | 3 Phase 1 specs |
| Session B | P2_S04 (CORE first, alone) | 1 CORE spec |
| Session C | P2_S05 through P2_S09 | 5 Phase 2 Mini Apps |
| Session D | P2_S10 through P2_S14 | 5 Phase 2 Mini Apps |
| Session E | P3_S15 through P3_S20 | 6 Phase 3 specs |
| Session F | P4_S21 through P4_S27 | 7 Phase 4 specs |
| Session G | P5_S28 through P6_S34 | 7 Phase 5+6 specs |
| Session H | P7_S58 through P7_S61 | 4 Phase 7 specs (Wave A+B) |
| Session I | P7_S62 through P7_S65 | 4 Phase 7 specs (Wave C) |
| Session J | P7_S66 through P7_S69 | 4 Phase 7 specs (Wave D) |
| Session K | P7_S70 through P7_S74 | 5 Phase 7 specs (Wave E) |
| Session L | P7_S75 through P7_S79 | 5 Phase 7 specs (Wave F) |
> [!WARNING]
> **Session B (CORE) must complete and be reviewed before Sessions C and D begin.** All 10 Mini App specs depend on the CORE engine contracts defined in FR-ERA3-05-CORE.

---

## Status Legend

| Symbol | Meaning |
|--------|---------|
| 🔲 Not Started | Prompt exists, spec not yet written |
| 🔄 In Progress | Session open, spec being written |
| ✅ Complete | Spec written and reviewed |
| ❌ Rejected | Returned for revision |

*Update this file as specs are completed.*
