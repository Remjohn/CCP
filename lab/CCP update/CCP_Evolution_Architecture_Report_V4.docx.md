

**CONSCIOUS COACHING PLATFORM**

**CCP Evolution**

Architecture Report

***V4.0 — CRAL Integration & Research Intelligence Architecture***

| 6 FoundationalInnovations | 8 ArchitectureComponents | 12 ImplementationImperatives |
| :---: | :---: | :---: |

Dependency Registry v4.0  ·  Adapter Registry v2.0  ·  Design Brief Template Library v1.2  ·  Design Brief Builder Engine

JIT Skill Assembler v2.0  ·  Container Module Library  ·  Fingerprint Archive  ·  CRAL Research Intelligence System

Type-Specific Skill Authoring Guides  ·  Standing Trigger Intelligence Library  ·  Research Analyst Taxonomy v2.0

**Version 4.0  ·  March 2026  ·  CCP Engineering Division**  
*Supersedes: CCP Evolution Architecture Report V3.0 (March 2026\)*

# **00  Executive Summary**

**The CCP Evolution Architecture Report V4.0** is the definitive system architecture specification for the Conscious Coaching Platform. It supersedes V3.0 by completing what V3.0 left architecturally pending: the upstream intelligence infrastructure that ensures content generation never begins without pre-addressed, quality-gated research intelligence for every moment it needs.

V3.0 established and fully operationally wired the JIT Skill Compiler as a seven-component system — Dependency Registry, Adapter Registry, Container Module Library, Design Brief Template Library, Design Brief Builder Engine, JIT Skill Assembler v2.0, and Fingerprint Archive. The compiler replaced ad-hoc skill authoring with a traceable, psychologically-routed, self-improving compilation pipeline. V4.0 accepts all seven components as resolved architecture and extends the system with four structural additions that address its remaining upstream and methodological gaps.

**The four V4.0 additions are:**

* **CRAL — Conscious Research Alchemy Lab**: The eighth JIT Compiler component. A nine-skill research intelligence subsystem that pre-addresses all seven content production moments (RELEVANT, BELIEVABLE, UNDENIABLE, RESONANT, SURPRISING, IRREFUTABLE, RELATABLE) before any compilation begins. CRAL eliminates the final remaining failure mode V3.0 documented but did not resolve: generating content intelligence inside the production step.  
* **Type-Specific Skill Authoring Guides**: The first formally specified methodology layer in the architecture. Three guides — Script Generation, Research Analyst, Voice Processing — that govern how all skills of each type are authored, structured, and validated. Script Generation Guide is the highest-priority build, as it defines the methodology that produces all Design Brief Templates.  
* **Design Brief Template Library v1.2 Migration Standard**: The migration specification for upgrading all 92 archetype templates from v1.1 to v1.2, incorporating CRAL wiring, DEP-ENG-021/022 registration, and Builder Engine Step 3.5 conflict detection. Achievement Story v1.2 is the validated reference migration template.  
* **Research Analyst Taxonomy v2.0 and Standing Trigger Intelligence Library**: The reclassification of all 41 deep research analysts from archetype-indexed to trigger-category-indexed, enabling reuse across archetypes. Standing Trigger Intelligence — the persistent, quality-gated library of pre-addressed research findings — is the compounding asset this reclassification unlocks.

| ARCHITECTURAL STATUS — V4.0 V3.0 JIT Compiler 7-component system: RESOLVED ARCHITECTURE — carried forward unmodified CRAL 9-skill research intelligence subsystem: SPECIFICATION COMPLETE — eighth compiler component DEP-ENG-021 (CRAL Finding Index) \+ DEP-ENG-022 (Session Research Plan): REGISTERED — Dependency Registry v4.0 cral-finding-router-adapter: REGISTERED — Adapter Registry v2.0 Builder Engine Step 3.5 (Research Synthesis Protocol): SPECIFICATION COMPLETE Design Brief Template v1.2 Migration Standard: SPECIFICATION COMPLETE — Achievement Story v1.2 validated Script Generation Skill Type Guide: SPECIFIED — pending build Research Analyst Taxonomy v2.0: SPECIFICATION COMPLETE — 41 analysts reclassified Standing Trigger Intelligence Library: SPECIFICATION COMPLETE — pending initial population Implementation imperatives: 12 total (10 from V3.0 \+ 2 new) Implementation build sequence: 14 steps (10 from V3.0 \+ 4 new) |
| ----- |

# **I  The Six Foundational Innovations — V2.0 Architecture, Retained**

The six foundational innovations specified in V2.0 and operationally wired in V3.0 are carried forward without modification in V4.0. Each remains the resolved architecture it became in V3.0. V4.0 extends the system above and adjacent to these innovations — it does not revise them.

| Innovation | Name | V3.0 Status | MCDA | V4.0 Role |
| ----- | ----- | ----- | :---: | ----- |
| 1 | **Client Intelligence Layer** | Fully operational — feeds DEP-ENG-016/017/018 | 4.55 | CRAL Stage 1 (M1\_RELEVANT) consumes Tier 1–3 signals |
| 2 | **Psychological Routing & Mood State System** | Operationally wired — 5-stage routing flow complete | 4.55 | CRAL moment register calibrated to active mood state |
| 3 | **Trigger-First Engine Inversion** | TTT enforcement mechanical — Block C C-08 | 4.40 | CRAL M1\_RELEVANT shapes trigger quality upstream |
| 4 | **3-Dimensional Voice DNA** | DEP-ENG-003/004/LIB-001 fully loaded at Tier 1 | 4.35 | CRAL ↔ Voice DNA collision replaces raw research ↔ Voice collision in Distillation Funnel |
| 5 | **CCSB Two-Phase Skill Architecture** | Builder Engine Phase 1 \+ Assembler v2.0 Phase 2 | 4.00 | Builder Engine gains Step 3.5 — CRAL conflict detection |
| 6 | **L3 Context Premise** | 3 outputs: Pain Map, Mood Context Map, Psychometric Feed | 3.95 | CRAL M7\_RELATABLE constrained by L3 vocabulary. L3 \= register gate not content source |

*All scientific foundations (LIWC-22, MMT, RFT, SDT, TMT, iRAV, Linguistic Relativity) are unchanged. V4.0 does not revise the scientific grounding of any foundational innovation.*

# **II  The JIT Skill Compiler — Eight-Component Architecture**

V3.0 established the JIT Skill Compiler as a seven-component system. V4.0 adds CRAL (Conscious Research Alchemy Lab) as the eighth component — the upstream research intelligence layer that ensures every compilation begins with pre-addressed, quality-gated findings rather than processing research inside the generation step.

## **2.1 Eight-Component Dependency Map**

| \# | Component | Role | Depends On | Fails Without |
| ----- | ----- | ----- | ----- | ----- |
| 1 | **Dependency Registry v4.0** | Canonical data layer — formal IDs for all inputs | None — foundational | All components reference ghost variables |
| 2 | **Adapter Registry v2.0** | Transformation layer — how modules mutate per context | Registry v4.0 | Adapters invoke undefined resources |
| 3 | **Container Module Library** | Intelligence layer — ecological adaptations per archetype | Registry v4.0 \+ Adapter Registry | Generic reasoning; no adapter wiring |
| 4 | **Design Brief Template Library v1.2** | Specification layer — Block A \+ compilation metadata | Module Library \+ CRAL Finding Map (v1.2) | Templates without CRAL wiring; research in generation |
| 5 | **Design Brief Builder Engine \+ Step 3.5** | Phase 1 compiler — populates Block B, resolves CRAL conflicts | All above \+ DEP-ENG-016/017/018/021 | CRAL-vs-SoC conflicts propagate silently |
| 6 | **JIT Skill Assembler v2.0** | Phase 2 compiler — assembles skills from validated briefs | All above | Unrecoverable pipeline failures |
| 7 | **Fingerprint Archive** | Memory layer — links every skill to outputs and performance | Assembler v2.0 | No learning loop; no compounding |
| 8 NEW | **CRAL — Conscious Research Alchemy Lab** | Research intelligence layer — pre-addresses all 7 content moments before compilation | Registry v4.0 \+ Adapter Registry \+ Dependency Registry (DEP-ENG-021/022) | Research executed inside generation; statistical centroid findings; no human evidence guarantee |

## **2.2 Where CRAL Sits in the Production Flow**

| PRODUCTION FLOW — V4.0 PRE-COMPILATION (CRAL fires here)   Stage 0: Telegram Bot intake — M1\_RELEVANT cultural NOW signal   Stages 1–3: M2 through M7 research moments addressed by 7 executor skills   DEP-ENG-021 CRAL Finding Index assembled — all 7 findings quality-gated   DEP-ENG-022 CRAL Session Research Plan archived BUILDER ENGINE — Phase 1   Step 1: DEP resolution check   Step 2: Context Premise load   Step 3: Psychological Routing Brief generation   Step 3.5: Research Synthesis Protocol — CRAL conflict detection (NEW)   Step 4: Template selection \+ Block A load   Step 5: Block B population \+ Block C validation ASSEMBLER v2.0 — Phase 2   Tier 0: Pre-flight (C-01 through C-10)   Tier 1: Mandatory adapters (includes cral-finding-router-adapter)   Tier 2: Conditional adapters   Tier 3: Section assembly (CRAL finding injected per arc phase)   Post-assembly: SG-01–SG-08 \+ PC-01–PC-05 GENERATION   Generation agent executes against pre-addressed CRAL intelligence   No research at generation time — execution only |
| :---- |

# **III  Registry Architecture — V4.0 Additions**

V3.0 registered 8 new DEP IDs and 3 new adapters, bringing the system to Dependency Registry v4.0 and Adapter Registry v2.0. All 11 V3.0 registrations are carried forward with status updated from PROPOSED to REGISTERED. V4.0 adds 2 new DEP IDs and 1 new adapter required by the CRAL subsystem.

## **3.1 V3.0 Registrations — Status Update: PROPOSED → REGISTERED**

The following items were marked PROPOSED in V3.0. All are confirmed REGISTERED in V4.0 as the CRAL architecture depends on them being formally present.

| DEP ID | Name | File | Tier | V4.0 Status |
| ----- | ----- | ----- | ----- | ----- |
| DEP-ENG-016 | Psychological Routing Brief | psych\_routing\_brief.json | Tier 1 | **REGISTERED** |
| DEP-ENG-017 | Audience Maturity Profile | audience\_maturity.json | Tier 1 | **REGISTERED** |
| DEP-ENG-018 | Mood Context Map | mood\_context\_map.json | Tier 2 | **REGISTERED** |
| DEP-ENG-019 | Session Transcript Intelligence | transcript\_intel.json | Tier 2 | **REGISTERED** |
| DEP-ENG-020 | Fingerprint Archive Index | fingerprint\_archive.json | Tier 3 | **REGISTERED** |
| DEP-LIB-008 | Archetype Classification Library | archetype\_psych\_map.yaml | Tier 0 | **REGISTERED** |
| DEP-LIB-009 | Compiled Skill Template Registry | skill\_template\_registry.yaml | Tier 0 | **REGISTERED** |
| DEP-PROTO-011 | Semantic Affinity Guard Protocol | Protocol definition | Proto | **REGISTERED** |
| DEP-PROTO-012 | Fingerprint Scoring Protocol | Fingerprint Archive | Proto | **REGISTERED** |
| DEP-PROTO-013 | Anti-Draft Calibration Protocol | Contrastive Anchor \+ Deliberation | Proto | **REGISTERED** |

## **3.2 V4.0 New DEP Registrations — CRAL Subsystem**

| DEP ID | Name | File | Tier | Required By | Status |
| ----- | ----- | ----- | ----- | ----- | ----- |
| **DEP-ENG-021** | CRAL Finding Index | cral\_finding\_index.json | Tier 2 (orchestration) | All v1.2 Design Brief Templates, Builder Engine Step 3.5, Assembler cral-finding-router-adapter | **REGISTERED** |
| **DEP-ENG-022** | CRAL Session Research Plan | cral\_session\_plan.json | Tier 3 (archive) | Fingerprint Archive — links content output to research session. Standing Trigger Intelligence library accumulation | **REGISTERED** |

**DEP-ENG-021 Structure — CRAL Finding Index:**

| Seven finding objects keyed by moment\_id. Each object: { finding, register, use\_at, verifiability\_citation, human\_evidence: { name, source, cultural\_proximity } } Moment IDs: M1\_RELEVANT | M2\_BELIEVABLE | M3\_UNDENIABLE | M4\_RESONANT | M5\_SURPRISING | M6\_IRREFUTABLE | M7\_RELATABLE Degradation rule: If absent, flag CRAL\_DEGRADED per phase, fall back to v1.1 source chain. Assembly continues. Operator alert required. |
| :---- |

## **3.3 V4.0 New Adapter Registration**

| Adapter | Tier | Mandatory For | Inputs | Core Function |
| ----- | ----- | ----- | ----- | ----- |
| **cral-finding-router-adapter** | Standard | All v1.2 Design Brief Template compilations | DEP-ENG-021 Finding Index \+ arc phase map from field\_5b | Routes each of the 7 CRAL moment findings to the correct arc phase at assembly time. Fires at phase entry, injects pre-addressed finding as structured constraint before section assembler runs. Prevents research at generation time. |

**Routing Map — cral-finding-router-adapter (Storytelling archetype family):**

| Arc Phase | CRAL Moments Injected | Function |
| ----- | ----- | ----- |
| Stakes | M2\_BELIEVABLE \+ M3\_UNDENIABLE | Named mechanism instance \+ audience prediction error. Stakes land at exact cognitive register where audience is wrong. |
| Mechanism | M4\_RESONANT | Complete narrative unit — protagonist, status, documented moment of contact, outcome. |
| Turn | M5\_SURPRISING | Counter-intuitive finding at optimal incongruity. The Turn IS the finding. |
| Result | M6\_IRREFUTABLE | Maximum source proximity evidence. Audience cannot unknow it. |
| Implication | M7\_RELATABLE | Tribal recognition anchor — vernacular-precise human evidence. Quality gate: tribal recognition, not factual accuracy. |

# **IV  Design Brief Architecture — v1.2 Migration Standard**

The Design Brief Template architecture specified in V3.0 is extended in V4.0 with the v1.2 upgrade — the integration of CRAL intelligence wiring into the three-block template system. V3.0 templates (v1.1) were architecturally complete but contained one structural deficiency: the generation step was responsible for processing research intelligence at assembly time. V4.0 closes this gap.

## **4.1 The v1.1 → v1.2 Structural Deficiency**

| Element | v1.1 Behaviour (V3.0 templates) | v1.2 Behaviour (V4.0 templates) |
| ----- | ----- | ----- |
| **Implication phase intelligence** | Loaded from DEP-ENG-006 Context Premise L3 layer — constructed at generation time | Delivered from DEP-ENG-021\[M7\_RELATABLE\] — pre-addressed, vernacular-precise. L3 \= register gate only |
| **Stakes evidentiary layer** | Derived from DEP-ENG-010 SoC Batch only | SoC \= authentic voice. DEP-ENG-021\[M2+M3\] \= evidentiary layer. Both mandatory |
| **Mechanism narrative unit** | Extracted from SoC candidate passages | M4\_RESONANT delivers pre-structured narrative unit. SoC cross-referenced via Step 3.5 |
| **Turn specificity** | Reconstructed from SoC | M5\_SURPRISING IS the Turn. Counter-intuitive at optimal incongruity calibration |
| **Result anchor** | DEP-ENG-010 \+ DEP-ENG-005 validation | M6\_IRREFUTABLE as evidentiary anchor \+ DEP-ENG-005 validation |
| **Psychological adapters** | psych-routing, payload-masking, audience-maturity: PROPOSED. Inline logic in field\_9 | All three: REGISTERED. Inline logic is now human-readable reference only. Adapter Registry v2.0 is authoritative |
| **CRAL wiring** | None — DEP-ENG-021 not registered | field\_5b CRAL Finding Map \+ cral\_finding\_index\_ref in Block B \+ C-09/C-10 in Block C |

## **4.2 Builder Engine Step 3.5 — Research Synthesis Protocol**

Step 3.5 is inserted between Builder Engine Step 3 (DEP-ENG-016 Psychological Routing Brief generation) and Step 4 (template selection). It is the conflict detection pass that prevents CRAL findings and SoC source material from producing contradictory intelligence in the same compilation.

| BUILDER ENGINE STEP 3.5 — RESEARCH SYNTHESIS PROTOCOL Input: DEP-ENG-021 (CRAL Finding Index) \+ DEP-ENG-010 (SoC Batch) \+ DEP-ENG-005 (Authentication Certificate) Trigger: Runs on every compilation where DEP-ENG-021 is present (cral\_coverage\_status ≠ ABSENT) Conflict Type 1: M2 external document vs M6 internal document — same mechanism, contradictory claims   Resolution: M6 internal institutional evidence outranks M2 external documentary evidence. Log in assembly\_report.json. Conflict Type 2: M4 narrative unit mechanism vs DEP-ENG-010 SoC mechanism — structural mismatch   Resolution: CRAL M4 provides evidentiary structure. SoC provides authentic voice. If mechanism type differs materially, FLAG for coach review. Do not auto-resolve — block until cleared. Conflict Type 3: M6 irrefutable evidence vs DEP-ENG-005 Authentication Certificate — result authenticity conflict   Resolution: BLOCK. M6 cannot contradict the coach's authenticated result. Return conflict\_type\_3 \+ resolution\_instruction to Phase 1\. Do not proceed. Output: cral\_conflict\_resolution\[\] array in assembly\_report.json. All decisions logged. |
| :---- |

## **4.3 Block C — Two New Validation Gates**

V4.0 adds C-09 and C-10 to the Block C compilation validation gate. The existing C-01 through C-08 are unchanged.

| Check | Name | Pass Condition | Failure Behaviour | New In |
| ----- | ----- | ----- | ----- | ----- |
| C-09 | **CRAL Coverage Check** | DEP-ENG-021 present with ≥5 of 7 moment findings \= COMPLETE. 3–4 findings \= PARTIAL. \<3 or absent \= ABSENT | COMPLETE: proceed. PARTIAL: assemble with CRAL\_DEGRADED flags. ABSENT: full v1.1 source chain fallback \+ operator alert | **V4.0** |
| C-10 | **CRAL Moment Object Completeness** | Each DEP-ENG-021 finding object must contain: finding, register, use\_at, verifiability\_citation | Incomplete object treated as absent for its phase. Phase falls back to v1.1 source chain. Flag at HIGH severity for M2 and M7. | **V4.0** |

## **4.4 Migration Guide — 92 Archetype Templates**

Achievement Story v1.2 is the validated reference migration template. All 91 remaining archetype templates follow the same upgrade pattern. The migration standard defines eight steps applicable to every archetype family.

| Step | Target | What Changes | Archetype-Specific Note |
| ----- | ----- | ----- | ----- |
| 1 | meta block | template\_version: '1.2', migration\_from: '1.1', cral\_integration: true | Identical for all archetypes |
| 2 | field\_7 arc phases | Add cral\_source per phase. Add v1\_1\_source and v1\_2\_source audit trail. | Phase labels differ per archetype family — map moments to the specific arc structure |
| 3 | field\_8 Distillation Funnel | Update Cross-Input Collision: DEP-ENG-021 ↔ DEP-ENG-003 replaces raw research ↔ voice. Add cral-finding-router-adapter as mandatory. | Collision variant names differ per archetype but the CRAL ↔ Voice upgrade pattern is universal |
| 4 | field\_9 constraints | Add 3 universal CRAL rules. Add DEP-ENG-021 \+ moment findings to graceful\_degradation\_map. | Degradation severity may be adjusted per archetype — M2+M7 always HIGH for Storytelling family |
| 5 | field\_11 structural gates | Add SG-06 (M2 deployed), SG-07 (M7 tribal recognition), SG-08 (Step 3.5 resolved). | Gate names remain SG-06/07/08. Gate descriptions reference archetype-specific phases |
| 6 | Block B inputs | Add DEP-ENG-021 to tier\_2\_orchestration (CRITICAL). Add DEP-ENG-022 to tier\_3\_archive (IMPORTANT). | Identical for all archetypes |
| 7 | field\_5b CRAL Finding Map | New field. Explicit use\_at address for each of 7 moments. Contracts between CRAL and Assembler. | Moment-to-phase mapping DIFFERS by archetype family. See archetype family mapping table below. |
| 8 | Block C gates | Add Step 3.5 block. Add C-09 \+ C-10. Promote all 3 psychological adapters from PROPOSED to REGISTERED. | Identical for all archetypes |

### **Moment-to-Phase Mapping by Archetype Family**

| Archetype Family | M2\_BELIEVABLE | M3\_UNDENIABLE | M4\_RESONANT | M5\_SURPRISING | M7\_RELATABLE |
| ----- | ----- | ----- | ----- | ----- | ----- |
| Storytelling (Achievement, Transformation) | Stakes phase | Stakes phase | Mechanism phase | Turn phase | Implication phase |
| Myth & Scam (Indignation, Empowering) | Myth establishment | Audience belief confirmation | Origin exposure | Hidden mechanism reveal | Tribal belief anchor |
| Listicle (Fear-Anxiety, Shocking) | Item 1 evidence anchor | Audience prediction gap for list | Highest-stakes item narrative unit | Most counter-intuitive item | Tribal relatable close |
| Case Study (Surprising, Relatable) | Result evidence anchor | Audience's prior belief about result | Subject narrative unit | Turn point / pivot | Audience parallel close |
| Comparison (Shocking, Surprising) | Delta evidence anchor | Expected vs actual prediction gap | Winner/loser narrative unit | Most surprising delta item | Tribal validation close |

# **V  JIT Skill Assembler v2.0 — V4.0 Updates Only**

The JIT Skill Assembler v2.0 architecture specified in V3.0 is carried forward without modification to its four-tier structure, diagnostic repair protocol, or Deployment Quarantine Rule. V4.0 adds three elements:

**Tier 0 addition:** C-09 (CRAL Coverage Check) and C-10 (CRAL Moment Object Completeness) added to Block C validation checks. The pre-flight gate now runs C-01 through C-10.

**Tier 1 addition:** cral-finding-router-adapter added as mandatory adapter alongside irevc-adapter, negative-space-loader-adapter, pre-generation-constraints-adapter, graceful-degradation-adapter, psych-routing-adapter, and audience-maturity-adapter. Failure → HALT with specific adapter diagnostic.

**Post-assembly addition:** SG-06 (M2 deployed in primary evidence phase), SG-07 (M7 tribal recognition test), and SG-08 (Builder Engine Step 3.5 conflict resolved) added to structural quality gates. Total structural gates: SG-01 through SG-08.

# **VI–IX  Container Module Library, Fingerprint Archive, Anti-Draft Intelligence, Mood State Architecture — Carried Forward**

Sections VI (Container Module Library), VII (Fingerprint Archive), VIII (Anti-Draft Intelligence), and IX (Mood State Architecture) are carried forward from V3.0 without modification to their core specifications. Three targeted updates apply:

**Section VI update:** Container Module Library modules must now include a field\_5b CRAL guidance block specifying the moment-to-phase mapping for their archetype family. This guidance is consumed by the Script Generation Skill Type Guide methodology when authoring Block A field\_5b for templates in that family. Module update follows the IMMUTABLE-after-STABLE rule — existing STABLE modules receive this as an augmentation, not a modification to the stable core.

**Section VII update:** Fingerprint Archive records are updated to include cral\_session\_id (linking to DEP-ENG-022) and cral\_coverage\_status in the dep\_snapshot object. This enables the learning loop to distinguish between compilations that used full CRAL intelligence and those that degraded to v1.1 source chains — allowing performance scoring to isolate the CRAL contribution.

**Section IX update:** The Upward Spiral Platform Strategy section gains one operational note: M1\_RELEVANT cultural NOW research (CRAL) is a signal input to Stage 1 Mood Context Detection. Tribes experiencing shared cultural events (industry disruptions, viral trends, shared crises) produce predictable mood state shifts that a 14-day Netnography scan captures and which the probabilistic Mood Context Map should weight accordingly.

# **XIII  CRAL — Conscious Research Alchemy Lab**

**CRAL is the eighth JIT Compiler component.** It is a nine-skill research intelligence subsystem that pre-addresses all seven content production moments before any compilation begins. Its output is DEP-ENG-021 — the CRAL Finding Index — which carries pre-addressed, quality-gated intelligence for every arc phase. Compilation consumes this index. Generation executes against pre-addressed signal. Research never happens inside the production step.

## **13.1 The Upstream Intelligence Gap — What V3.0 Left Open**

V3.0's JIT Compiler was architecturally complete from the compilation trigger forward. The gap it documented but did not resolve was upstream: at the moment a batch slot needed research intelligence, the system had no formal mechanism to pre-address it. The generation agent was implicitly responsible for synthesising or inferring research context it had no formal instruction to retrieve. This produced the statistical centroid failure mode the Anti-Draft Architecture was designed to catch — but Anti-Draft catches failures after generation, not before.

CRAL resolves this by making research upstream, explicit, and quality-gated. The seven content production moments have specific research needs. CRAL addresses each need with a dedicated executor skill, a quality gate grounded in a named academic discipline, and a verifiability standard that ensures every finding in DEP-ENG-021 is independently confirmable before it enters the compilation pipeline.

## **13.2 The Seven Production Moments — CRAL Mapping**

| Moment ID | Name | Research Function | Academic Discipline | Depth Layer | Quality Gate |
| ----- | ----- | ----- | ----- | ----- | ----- |
| **M1\_RELEVANT** | RELEVANT | Cultural NOW — the conversation this tribe is already having | Netnography | Surface | Frequency threshold: 3+ independent sources, 14-day window |
| **M2\_BELIEVABLE** | BELIEVABLE | Named, verifiable, unchallengeable mechanism instance | Precision Journalism | Mid | Verifiability: named entity \+ documented decision \+ verifiable date \+ internal industry term |
| **M3\_UNDENIABLE** | UNDENIABLE | Audience's measurably wrong prediction at this mood state | Cognitive Bias Research | Mid | Calibration: prediction error must exceed 30% in documented study or equivalent |
| **M4\_RESONANT** | RESONANT | Complete narrative unit — protagonist, status, documented moment, outcome | Narrative Non-Fiction | Deep | Emotional architecture: all four narrative elements present; source verifiable |
| **M5\_SURPRISING** | SURPRISING | Counter-intuitive finding at optimal incongruity — violates held belief | Productive Surprise Research | Mid-Deep | Incongruity calibration: enough structure to be taken seriously; enough prediction error to demand revision |
| **M6\_IRREFUTABLE** | IRREFUTABLE | Maximum source proximity evidence — enemy's own document, internal admission | Investigative Journalism | Deep | Source proximity: primary \> secondary \> tertiary. Internal institutional source outranks external analysis |
| **M7\_RELATABLE** | RELATABLE | Tribal recognition anchor — named person from inside the tribe, vernacular-precise | Oral History / Digital Ethnography | Mid | Tribal recognition test: a tribe member reading this would recognise the language as their own internal language |

## **13.3 The Nine-Skill Architecture**

CRAL is implemented as nine skills operating within a hierarchical orchestration structure. Two governing skills orchestrate and plan. Seven executor skills address each production moment independently.

| Skill | Type | Function | Output |
| ----- | ----- | ----- | ----- |
| **Research Orchestrator** | Orchestrator Agent | OODA loop execution across all 7 executor skills. Maintains DEP-ENG-021 Finding Registry. Forward-passes context between skills. Detects dependency failures and reroutes. | Session directive \+ finding registry state |
| **Research Planner (JIT)** | Planning Skill | Just-In-Time compilation of research directives. Reads compiled brief \+ mood state \+ CRAL session context. Produces 40–60 word targeted directive per moment executor. Enforces 4-constraint architecture: scope, register, verifiability, use\_at. | 7 directed executors per session |
| **M1 RELEVANT Executor** | Moment Executor | Netnography scan of tribal discourse. 14-day window. Frequency-threshold filtered. Source diversity required. | DEP-ENG-021\[M1\] |
| **M2 BELIEVABLE Executor** | Moment Executor | Precision journalism extraction. Named entity \+ documented decision \+ verifiable date. Internal industry terminology required. | DEP-ENG-021\[M2\] |
| **M3 UNDENIABLE Executor** | Moment Executor | Cognitive bias research. Maps audience's specific measurably wrong prediction at current mood state calibration. | DEP-ENG-021\[M3\] |
| **M4 RESONANT Executor** | Moment Executor | Narrative non-fiction construction. Four-element narrative unit: protagonist \+ status \+ documented moment of contact \+ outcome. All four elements verifiable. | DEP-ENG-021\[M4\] |
| **M5 SURPRISING Executor** | Moment Executor | Productive surprise targeting. Violates audience's held belief at optimal incongruity calibration. Neither too familiar nor too distant. | DEP-ENG-021\[M5\] |
| **M6 IRREFUTABLE Executor** | Moment Executor | Investigative journalism source hierarchy. Primary source proximity maximised. Internal admission preferred over external analysis. | DEP-ENG-021\[M6\] |
| **M7 RELATABLE Executor** | Moment Executor | Oral history / digital ethnography. Named tribal member. Vernacular-precise documented testimony. Portelli quality gate: tribal recognition, not factual accuracy. | DEP-ENG-021\[M7\] |

## **13.4 The Diagonal Research Method**

CRAL's fundamental methodological innovation is the Diagonal Research Method — the structured integration of horizontal breadth research (cultural scanning) with vertical depth research (evidentiary drilling) to produce findings that operate simultaneously at the audience's surface recognition layer and their deep evidential conviction layer.

| Dimension | Definition | CRAL Moments | Failure Without It |
| ----- | ----- | ----- | ----- |
| **Horizontal** | Cultural breadth scan — what is the tribe currently discussing across multiple sources and channels | M1\_RELEVANT (primary), M3\_UNDENIABLE (secondary) | Research is locally accurate but culturally invisible — the finding is true but nobody is thinking about it right now |
| **Vertical** | Evidentiary depth drill — maximum source proximity for the specific mechanism or claim being made | M2\_BELIEVABLE, M6\_IRREFUTABLE (primary) | Research is culturally visible but epistemically weak — the audience recognises the topic but cannot fully trust the claim |
| **Diagonal** | Cross-registered findings that are both culturally NOW and evidentiary maximum — the intersection where recognition and conviction are simultaneously activated | All 7 moments operating as a system | The statistical centroid failure — content that is accurate but not compelling, or compelling but not accurate |

## **13.5 Human Evidence Bias — Culturally Favorable Evidence Standard**

CRAL operates under a structural human evidence bias: every finding in DEP-ENG-021 must carry a human evidence object. The finding index is not complete without named human evidence in the form appropriate to each moment. This is not an editorial preference — it is an architectural constraint that prevents the most common research failure mode in content production: factually accurate but humanly inert intelligence.

| Verifiability Standard | Definition | CRAL Application | Quality Gate |
| ----- | ----- | ----- | ----- |
| Named Attribution | Human evidence carries a name, role, and documentable context | All moments | Anonymous source does not satisfy human evidence requirement |
| Cultural Proximity | The named person is from inside the tribe or is an aspirational reference the tribe already recognises | M7\_RELATABLE (critical), M4\_RESONANT | Cultural outsider does not satisfy tribal recognition test even if named and verifiable |
| Vernacular Precision | The testimony uses the tribe's own internal language — not paraphrase, not academic description | M7\_RELATABLE | Paraphrase fails. Direct documented testimony in tribal language required. |

## **13.6 CRAL Integration Points in the Production Pipeline**

| Integration Point | What CRAL Provides | Architectural Impact |
| ----- | ----- | ----- |
| Telegram Bot Intake (M1\_RELEVANT) | Cultural NOW signal for this coach in this tribal moment | Shapes trigger activation quality before voice note elicitation. Ensures the content the coach produces is entering a conversation the tribe is already having. |
| Builder Engine Step 3.5 | DEP-ENG-021 for conflict detection pass | CRAL-vs-SoC conflicts resolved before template selection. No contradictory intelligence enters the compilation. |
| Assembler Tier 1 — cral-finding-router-adapter | DEP-ENG-021 routed to correct arc phases | Each finding injected at the specific moment it is needed. Not global context — targeted injection per phase. |
| DEP-ENG-021 in field\_5b | Explicit use\_at contract per moment | The architectural contract between CRAL and the Assembler. Phase entry triggers retrieval. Generation never handles research. |

| *⬡  Netnography (Kozinets, 2002): Online communities produce authentic, unsolicited discourse that reveals the actual language, concerns, and self-definitions of a cultural group — not the mediated version they produce for outsiders. M1\_RELEVANT must be sourced from native tribal discourse, not from descriptions of that discourse.* |
| :---- |

| *⬡  Productive Surprise (Berlyne, 1960 / Schmidhuber, 2010): Optimal incongruity — the sweet spot between the expected and the genuinely incomprehensible — produces maximum curiosity and retention. M5\_SURPRISING requires calibration at this optimal point, not at maximum novelty.* |
| :---- |

# **XIV  Type-Specific Skill Authoring Guides — Architecture Layer**

The CCP V3.0 architecture specified how skills are compiled and assembled. It did not specify how skills are authored — the methodology by which a skill author produces a Block A Structural Invariant section, validates its ecological adaptations, integrates its anti-draft architecture, and certifies it for TESTED maturity promotion. This gap is closed in V4.0 by the Type-Specific Skill Authoring Guide layer.

## **14.1 The Authoring Layer in the Architecture**

The Type-Specific Skill Authoring Guides are a formal architectural layer that sits between the Container Module Library (which defines what every module must contain) and the Design Brief Template Library (which is the output the authoring process produces). Without this layer, authors apply the module specifications with inconsistent interpretations, producing templates that are structurally conforming but methodologically inconsistent.

| ARCHITECTURE LAYER STACK   Layer 1 — Registry Foundation: Dependency Registry v4.0 \+ Adapter Registry v2.0   Layer 2 — Module Intelligence: Container Module Library (ecological adaptations, mood state matrices, anti-draft)   Layer 3 — Authoring Methodology: Type-Specific Skill Authoring Guides (NEW in V4.0)   Layer 4 — Template Library: Design Brief Template Library v1.2 (output of Layer 3 process)   Layer 5 — Compilation Engine: Builder Engine \+ Assembler v2.0   Layer 6 — Research Intelligence: CRAL subsystem (DEP-ENG-021/022)   Layer 7 — Learning Loop: Fingerprint Archive \+ Maturity Promotion Protocol |
| ----- |

## **14.2 Three Guide Specifications**

| Guide | Status | Governs | Priority |
| ----- | ----- | ----- | ----- |
| **Script Generation Skill Type Guide** | **SPECIFIED — Build next** | How all CCF script skills are authored. The methodology that produces every Design Brief Template. Eight Architectural Mandates, Three-Layer SPR loading protocol, Anti-Draft Three-Level Architecture, Causal Construction Sequence, Emotional DNA Integration Test for TESTED maturity promotion. | **HIGHEST**  — the Design Brief Template is the guide's output product |
| **Research Analyst Skill Type Guide** | SPECIFIED — Build second | How all 41 Research Analyst skills are authored. Governs trigger-category indexing, session scoping, moment-to-executor mapping, and CRAL output quality standards. | HIGH — required before any CRAL executor skill can reach TESTED |
| **Voice Processing Skill Type Guide** | SPECIFIED — Build third | How all voice processing and audio transcription skills are authored. Governs DEP-ENG-019 output format, LIWC-22 extraction standards, and Live Psychometric Feed production. | MEDIUM — required before Tier 2+ client intelligence can reach full production quality |

## **14.3 Script Generation Skill Type Guide — Content Specification**

The Script Generation Skill Type Guide is the highest priority build because it defines the authoring doctrine that produces every Design Brief Template. Without it, template authorship is informal and template quality is inconsistent. The guide must contain the following mandatory sections:

| Section | Name | Content |
| ----- | ----- | ----- |
| 1 | **Eight Architectural Mandates** | The non-negotiable laws governing every CCF script skill. Anti-draft is mandatory. CRAL wiring is mandatory in v1.2+. Negative Space loads first. TTT is never pre-specified. Ghost variables are prohibited. All eight stated as laws with violation consequences. |
| 2 | **Three-Layer SPR Loading Protocol** | Semantic Pointer Register (SPR) loading sequence for Positive Space (DEP-ENG-003), Negative Space (DEP-ENG-004), and Emotional DNA (DEP-LIB-001). Load order is absolute. The guide specifies the exact cognitive state each layer establishes and what the author must verify before loading the next. |
| 3 | **Anti-Draft Three-Level Architecture** | Authoring methodology for all three anti-draft levels. Level 1: how to write the archetypal failure mode as prose (not description). Level 2: how the payload-masking-adapter produces the mode-specific failure mode at compilation time. Level 3: how to extract coach-specific drift patterns from DEP-ENG-004 and convert them into the Forbidden Vocabulary List. |
| 4 | **Causal Construction Sequence** | The 5-step process for building a Block A field\_7 arc phase specification. Step 1: name the phase's cognitive function. Step 2: identify the DEP ID that carries primary intelligence for this phase. Step 3: write the structural law. Step 4: write the CRAL source mapping. Step 5: write the graceful degradation path. |
| 5 | **CRAL Wiring Protocol** | How to complete field\_5b CRAL Finding Map for a new archetype. Moment-to-phase mapping methodology. How to determine which moments have the highest leverage for a given archetype family. The builder test for validating CRAL wiring before submitting to Architecture Review. |
| 6 | **Emotional DNA Integration Test** | The quality gate for TESTED maturity promotion. The test verifies: (1) every arc phase has a traceable DEP source, (2) the CRAL finding map is complete and mapped, (3) the anti-draft Level 3 is populated from actual DEP-ENG-004 data, (4) Block C passes without human override, (5) a test compilation produces COMPLETE assembly status. |

# **XV  Research Analyst Taxonomy v2.0 — Reclassification & Standing Trigger Intelligence**

V3.0 did not formally specify the research analyst component of the system. The 41 Deep Research Analysts that support CRAL were implicitly assumed to be archetype-indexed — one analyst per archetype or archetype cluster. V4.0 replaces this assumption with a formally specified taxonomy that reclassifies analysts by trigger category, enabling cross-archetype reuse and the accumulation of the Standing Trigger Intelligence Library.

## **15.1 The Problem with Archetype Indexing**

Archetype-indexed research analysts duplicate research effort across archetypes that share the same underlying trigger category. An Achievement Story analyst and a Transformation Story analyst addressing the same coach's mechanism — leadership — are conducting near-identical research under different archetype labels. The archetype is a structural container. The trigger category is the content domain. Research is always about content domains, not structural containers.

| V1.0 — Archetype Indexing (V3.0 assumption) | V2.0 — Trigger-Category Indexing (V4.0) | Impact |
| ----- | ----- | ----- |
| Achievement Story Analyst \+ Transformation Story Analyst \+ Case Study Analyst all research 'career transitions' separately | Career Transitions Analyst researches once, produces DEP-ENG-021 findings reusable across Achievement, Transformation, Case Study archetypes | 3× research effort → 1× research effort. Standing library accumulates per trigger category, not per archetype. |
| Research sessions expire with the archetype — cannot be reused | Research sessions expire with the trigger category's cultural NOW window — reused across all archetypes that reference the same category | M1\_RELEVANT 14-day window is per trigger category. One cultural scan serves all archetypes addressing that category. |
| 41 analysts → 41 siloed knowledge stores | 41 analysts → shared knowledge store organised by trigger category | Standing Trigger Intelligence library grows across every production cycle that touches any archetype in a category. |

## **15.2 Trigger Category Taxonomy**

The 41 research analysts are reclassified across the following trigger categories. Each trigger category produces a DEP-ENG-021 Finding Index that is valid for any archetype whose production moment overlaps with that category's content domain.

| Trigger Category | Representative Mechanisms | Archetype Families Served | Cultural NOW Window |
| ----- | ----- | ----- | ----- |
| **Leadership & Authority** | Promotion, hierarchy, decision-making | Storytelling, Case Study, Tier List | 14-day scan / 30-day library expiry |
| **Career Transitions** | Pivots, promotions, exits, new roles | Storytelling, Comparison, Myth | 14-day scan / 30-day library expiry |
| **Performance & Achievement** | Metrics, results, overcoming limitations | Storytelling, Case Study, Listicle | 14-day scan / 30-day library expiry |
| **Relationships & Communication** | Conflict, trust, vulnerability | Storytelling, Core Formats | 14-day scan / 21-day library expiry |
| **Identity & Belonging** | Values, impostor syndrome, status | Storytelling, Myth, Tier List | 14-day scan / 45-day library expiry |
| **System Failures & Injustice** | Institutional dysfunction, bias, broken incentives | Myth & Scam, Listicle, Comparison | 7-day scan / 14-day library expiry — fastest changing |
| **Well-being & Sustainability** | Burnout, rest, boundaries, energy | Core Formats, Listicle, Storytelling | 14-day scan / 30-day library expiry |

## **15.3 Standing Trigger Intelligence Library**

The Standing Trigger Intelligence Library is the persistent, quality-gated repository of CRAL finding indexes organised by trigger category. It is the compounding asset unlocked by trigger-category indexing. Every production cycle that generates a DEP-ENG-021 index contributes a quality-gated finding set to the library. The library grows across production cycles. Future compilations in the same trigger category can load pre-existing, quality-scored findings rather than beginning from scratch.

| Library Record | Contents | Expiry | Reuse Condition | Source |
| ----- | ----- | ----- | ----- | ----- |
| trigger\_category\_id | 7 moment findings (DEP-ENG-021 schema) | Per category window | mood\_state \+ audience\_cohort must match within ±1 maturity tier | DEP-ENG-022 |
| quality\_score | Derived from Fingerprint Archive performance data for outputs using these findings | Never expires | Scores decay toward baseline if no production outputs registered within 90 days | DEP-ENG-020 |
| human\_evidence\_status | COMPLETE | PARTIAL | ABSENT per moment | Per moment finding | PARTIAL or ABSENT findings must be refreshed before reuse in high-visibility compilations | DEP-ENG-021 |

| STANDING TRIGGER INTELLIGENCE — ECONOMIC ARGUMENT Production cycle 1: Achievement Story, Leadership trigger category. CRAL runs full 7-moment research. DEP-ENG-021 populated. DEP-ENG-022 archived. Standing library: 1 record. Production cycle 2: Transformation Story, Leadership trigger category, same mood state window. CRAL loads cycle 1 record. Validates cultural NOW (M1) — still within 14-day window. Runs M6 refresh only (irrefutable evidence has highest source decay rate). DEP-ENG-021 populated at 85% from library. Research effort: 15% of full session. Production cycle 10: Case Study, Leadership trigger category. Library has 9 records. Quality scores calculated from 8 production outputs. Top-scoring M2, M4, M7 findings loaded automatically. Cultural NOW scan only. Research effort: \<10% of full session. The Standing Trigger Intelligence Library is the architecture's primary long-term leverage mechanism. It transforms CRAL from a per-session cost to a per-domain investment that pays down with every production cycle. |
| :---- |

# **X  MCDA Evaluation — V4.0 Architecture Scoring**

The MCDA framework is updated to reflect V4.0 additions. Five evaluation dimensions remain unchanged: Strategic Leverage, Operational Necessity, Psychological Validity, Implementation Feasibility, and Learning Loop Contribution. V3.0 components carry their V3.0 scores forward. V4.0 additions are scored on their own merit.

| Architecture Component | Score | Primary Driver | V4.0 Status / Change |
| ----- | :---: | ----- | ----- |
| **Client Intelligence Layer** | 4.55 | Tier 3 data unlocks 100% routing accuracy | Unchanged from V3.0. CRAL M1\_RELEVANT extends its signal reach. |
| **Psychological Routing & Mood State System** | 4.55 | Fully wired — elevated from 4.45 in V2.0 | Unchanged from V3.0. CRAL moment register is now calibrated to active mood state. |
| **Trigger-First Engine Inversion** | 4.40 | TTT enforcement is mechanical — Block C | Unchanged. CRAL M1\_RELEVANT shapes trigger quality upstream. |
| **3-Dimensional Voice DNA** | 4.35 | Anti-draft Level 3 requires DEP-ENG-004 | Unchanged. Distillation Funnel collision upgraded to CRAL ↔ Voice in v1.2 templates. |
| **Container Module Library** | 4.30 | Highest leverage: one update improves all compilations | Unchanged. Modules must be updated to include field\_5b CRAL Finding Map guidance per archetype family. |
| **CRAL — Conscious Research Alchemy Lab** | **4.28** | NEW — eliminates research-in-generation failure mode | **NEW in V4.0** . High SL: every compilation benefits. High ON: generation without pre-addressed research produces statistical centroid. PV: 14 academic frameworks. IF: moderate — 9 skills to build. LLC: DEP-ENG-022 feeds Standing Trigger Intelligence library permanently. |
| **Anti-Draft Intelligence Layer** | 4.25 | Immune system against mean-reversion at generation | Unchanged. CRAL findings reduce the volume of anti-draft failures that reach the critic. |
| **JIT Skill Assembler v2.0** | 4.15 | Four-tier isolation eliminates single-point failure | Unchanged. Assembler gains cral-finding-router-adapter at Tier 1 and C-09/C-10 at Tier 0\. |
| **Fingerprint Archive & Skill ID System** | 4.10 | Closes learning loop; enables compounding | Unchanged. DEP-ENG-022 links every output to its CRAL session — research quality now enters the learning loop. |
| **Standing Trigger Intelligence Library** | **4.05** | NEW — compounding research economics | **NEW in V4.0** . Leverage is low initially, increases with every production cycle. LLC score is maximum (5.0): the library is the compounding mechanism. SL increases over time — early production cycles are subsidising permanent intelligence assets. |
| **CCSB Two-Phase Architecture** | 4.00 | Separates intelligence specification from assembly | Unchanged. Builder Engine gains Step 3.5. |
| **Design Brief Builder Engine** | 3.95 | Without it, incomplete briefs reach assembler silently | Unchanged. Step 3.5 addition increases operational necessity marginally. |
| **L3 Context Premise** | 3.95 | Foundation for routing; quality ceiling for outputs | Unchanged. Now serves as register gate for M7\_RELATABLE rather than content source. |
| **Type-Specific Skill Authoring Guides** | **3.90** | NEW — methodology layer closing authoring inconsistency | **NEW in V4.0** . ON score is high: templates authored without the guide are methodologically inconsistent. SL is moderate at first, high once Script Guide governs all 92 archetype templates. |
| **Design Brief Template Library v1.2** | 3.80 | Codifies invariant archetype intelligence | Stable score. v1.2 migration standard implemented — all 92 templates will reach v1.2 once Script Guide is built. |

# **XI  Implementation Imperatives — Twelve Non-Negotiable Rules**

The ten imperatives from V3.0 are carried forward without modification. V4.0 adds two new imperatives governing CRAL integration. All twelve are architectural laws.

| \# | Imperative | Violation Consequence | Priority | Version |
| ----- | ----- | ----- | ----- | ----- |
| 1 | Every field in every Design Brief Template that references a data source MUST have a formal DEP ID. | Ghost variable execution — adapters synthesise inputs, producing specification-satisfying but intent-violating skills | CRITICAL | V3.0 |
| 2 | TTT is NEVER a compilation variable. Any Design Brief containing hardcoded TTT is REJECTED by Block C. | Compiled skills become emotionally static. iRAV virality mechanism collapses. | CRITICAL | V3.0 |
| 3 | No compiled skill may deploy without its assembly\_report.json being read by the Orchestrator. PARTIAL\_MANUAL and REJECTED skills are QUARANTINED. | Partial skills deploy with gap placeholders. Generation agents skip constraints. | CRITICAL | V3.0 |
| 4 | The Semantic Affinity Guard (DEP-PROTO-011) must run before every Escape Mode compilation. HIGH affinity \+ Escape \= BLOCK — no exceptions. | Escape Mode content directly amplifies active stress. Mood Management Theory homeostasis reverses. | CRITICAL | V3.0 |
| 5 | The CCF pipeline must include the 5-Stage Mood Routing Flow as mandatory pre-generation stage. No batch slot receives a compilation trigger without a validated DEP-ENG-016. | Routing operates on defaults not actual audience state. All adaptation is inference. | HIGH | V3.0 |
| 6 | Smart Mix Synthesis Protocol must read from DEP-ENG-017 Audience Maturity Profile and enforce cohort-specific batch allocation before assembling any batch. | Audience receives wrong depth/mode ratio. Upward spiral training effect does not occur. | HIGH | V3.0 |
| 7 | Module Library modules are IMMUTABLE after reaching STABLE maturity. New findings must be implemented as augmentations, not modifications to the stable core. | Evolving PSN oscillatory regression — converged modules regress when modified by downstream pressure. | HIGH | V3.0 |
| 8 | The Fingerprint Archive must be updated before production compilations begin. Performance data must be registered within 48 hours of publication. | Learning loop never closes. Reference-tier promotion cannot occur. | HIGH | V3.0 |
| 9 | The Anti-Draft Instruction Block must contain all three levels. A compiled skill missing any level is PARTIAL\_AUTO at best — not COMPLETE. | Statistical mean-reversion not caught at compilation level. Level 3 drift patterns survive into production. | HIGH | V3.0 |
| 10 | DEP-LIB-008, DEP-LIB-009, and all PROTO registrations must be completed before any Design Brief Template is authored. | Templates reference unregistered resources. Block C cannot validate what the registry cannot confirm. | CRITICAL | V3.0 |
| **11** | **DEP-ENG-021 must be populated before any v1.2 Design Brief Template compilation. If CRAL was not run, cral\_coverage\_status must be explicitly set to ABSENT before Builder Engine Step 3.5 executes — not inferred.** | Implicit ABSENT status means Step 3.5 may skip conflict detection. A brief that skips Step 3.5 silently propagates CRAL-vs-SoC conflicts into the compiled skill. | **CRITICAL** | **V4.0 NEW** |
| **12** | **All 41 Research Analyst skills must be reclassified to trigger-category indexing before the Standing Trigger Intelligence Library is populated. Archetype-indexed sessions must not be added to the library — they produce siloed records that cannot compound.** | Standing Trigger Intelligence Library accumulates non-reusable records. The compounding mechanism never activates. The economic justification for CRAL collapses. | **HIGH** | **V4.0 NEW** |

# **XII  Implementation Build Sequence — Fourteen Steps**

V3.0 specified a 10-step topological build sequence. V4.0 adds 4 steps for CRAL, Type-Specific Guides, Template Migration, and Research Analyst Reclassification. The 10 V3.0 steps are unchanged and carry their original dependency relationships. The 4 V4.0 steps are inserted at the appropriate positions in the topological order.

| Step | Build Target | Unblocks | Effort | Why This Step First |
| ----- | ----- | ----- | ----- | ----- |
| 1 | **Dependency Registry v4.0**  — all DEP IDs including DEP-ENG-021/022 | Everything | ½ day | Ghost variable prevention. DEP-ENG-021/022 must exist before CRAL can formally reference them. |
| 2 | **Adapter Registry v2.0**  — 3 psychological adapters \+ cral-finding-router-adapter | Assembler v2.0, all CCF compiled skills | 1 day | cral-finding-router-adapter must be registered before any v1.2 template can be formally validated. |
| 3 | **DEP-PROTO-011**  Semantic Affinity Guard \+ DEP-PROTO-012/013 | Builder Engine Stage 4, Escape Mode skills | ½ day | Guard must be formally defined before any Escape Mode brief passes Block C. |
| 4 | **DEP-LIB-008**  Archetype Classification Library — 8-variable YAML for all 22+ archetypes | Orchestrator routing, all Design Brief Templates | 2 days | This is the routing database. Templates reference it. |
| 5 | **Container Module Library**  — all 7 archetype families including Mood State Interaction Matrices and field\_5b CRAL guidance | Design Brief Templates, Assembler Tier 3 | 3–4 days | Highest leverage investment. Module quality compounds. Module must include CRAL moment-to-phase mapping guidance per family. |
| **6 NEW** | **Script Generation Skill Type Guide**  — Eight Mandates, SPR Protocol, Anti-Draft Architecture, Causal Construction Sequence, CRAL Wiring Protocol, Emotional DNA Integration Test | All Design Brief Template authoring (steps 7 onwards) | 2 days | **Critical path addition** . Without this guide, all templates authored in step 7 are methodologically inconsistent. The guide is the methodology; the templates are the output. |
| 7 | **Design Brief Template Library v1.2**  — three-block templates for all archetypes using completed modules, upgraded to v1.2 standard per Script Guide | Design Brief Builder Engine | 3 days | Templates consume modules and follow Script Guide methodology. Both must pre-exist. v1.2 requires CRAL wiring — Achievement Story v1.2 is the reference migration template. |
| 8 | **Design Brief Builder Engine**  — 5-step Phase 1 compiler including Step 3.5 Research Synthesis Protocol | JIT Assembler v2.0 | 2 days | Builder produces validated briefs. Step 3.5 resolves CRAL-vs-SoC conflicts before any template is selected. |
| 9 | **JIT Skill Assembler v2.0**  — 4-tier resilient compiler with C-09, C-10, and cral-finding-router-adapter at Tier 1 | All compiled skill production | 2 days | Assembler consumes validated briefs and adapters. All must pre-exist. |
| 10 | **Fingerprint Archive Engine**  — ID schema \+ DEP-ENG-020 \+ DEP-ENG-022 linkage \+ scoring protocol | Performance learning loop \+ Standing Trigger Intelligence accumulation | 1 day | Must be active before first production compilation. DEP-ENG-022 linkage enables CRAL quality scoring. |
| **11 NEW** | **CRAL Subsystem Build**  — 9 skills: Research Orchestrator \+ Research Planner JIT \+ 7 Moment Executors. Research Analyst Skill Type Guide authored first. | DEP-ENG-021 production, Standing Trigger Intelligence Library population, Builder Engine Step 3.5 population | 5–6 days | **CRAL unlocks the full v1.2 template benefit** . Without operational CRAL, all v1.2 compilations degrade to v1.1 source chains and assembly\_report.json fills with CRAL\_DEGRADED flags. |
| **12 NEW** | **Research Analyst Reclassification**  — 41 analysts reclassified from archetype-indexed to trigger-category-indexed. Standing Trigger Intelligence Library structure initialised. | Standing Trigger Intelligence Library population, CRAL session economics | 1 day | Must be complete before any CRAL session populates the library. Archetype-indexed sessions must not be allowed to create library records. |
| 13 | **First Production Compilations — Pilot** : 2 archetypes × 2 coaches × 4 mood states \= 16 skills. CRAL sessions run for each. Standing library seeded. | Full pipeline validation \+ Reference tier promotion \+ Standing library initial records | Ongoing | Online validation. CRAL sessions run, DEP-ENG-021 populated, compilations executed, performance tracked, library begins accumulating. |
| **14 NEW** | **Voice Processing Skill Type Guide**  \+ DEP-ENG-019 production pipeline upgrade → Tier 2+ client intelligence activation | Full 5-stage Mood Routing Flow at empirical quality (Tier 2+) | 2 days | **Completes the intelligence tier stack** . Tier 2+ client intelligence activates the full LIWC-22 psychometric pipeline. Context Premise Output 3 (Live Psychometric Feed) becomes operational. |

| CRITICAL PATH — V4.0 Steps 1 → 2 → 3 → 4 → 6 → 11: The CRAL critical path. No CRAL executor skill can reach production quality until Steps 1–4 are complete and the Script Generation Skill Type Guide (Step 6\) has defined the authoring doctrine. Steps 5 → 6 → 7: The template quality critical path. Container Module Library provides the intelligence. Script Guide provides the methodology. Templates are the output. All three must be completed in order. Step 10 before Step 11: Fingerprint Archive must be active before the first CRAL session populates DEP-ENG-022. Standing Trigger Intelligence Library records cannot be created without the archive structure. Step 12 before library population begins: Analyst reclassification is a prerequisite for the Standing Trigger Intelligence Library. Do not begin populating the library with archetype-indexed records that cannot compound. |
| :---- |

——

**CCP Evolution Architecture Report**  
Version 4.0  ·  March 2026

*Supersedes V1.0 (March 2026), V2.0 (March 2026), and V3.0 (March 2026\)*