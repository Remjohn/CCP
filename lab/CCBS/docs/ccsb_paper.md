# The Conscious Composable Skill Builder (CCSB): A Two-Phase Architecture for Modular Skill Construction in Domain-Specific Agentic Systems

*A First-Principles Design for Composable, Ecologically Adaptive Skill Authoring in the Conscious Coaching Platform*

---

## 1. Abstract and Motivation

The proliferation of agentic AI systems has exposed a fundamental gap between the theoretical promise of reusable skills and the practical reality of authoring them at scale. Current approaches treat skill creation as a monolithic activity: an author writes a complete SKILL.md from scratch, merging design intent with algorithmic implementation in a single pass. This conflation produces three systemic failures. First, managerial oversight becomes impossible because the only reviewable artifact is an 800-line technical document that obscures strategic intent behind implementation detail. Second, quality variance across skills escalates because each author independently reinvents reasoning patterns that should be standardized. Third, ecological adaptation — the mutation of reasoning modules to fit specific domains — happens implicitly or not at all, producing skills that import generic logic into specialized environments.

The Conscious Composable Skill Builder (CCSB) addresses these failures through a two-phase architecture that separates *design specification* from *modular implementation*. Phase 1 produces an 11-field **Skill Design Brief** — a schema that captures Intent, Target, Context, Trigger, Inputs, Action, Method, Modules, Constraints, Output Artifact, and Success Criteria. This artifact is optimized for managerial review: its fields are legible without technical expertise, and its scope can be validated against the platform's strategic objectives before any implementation begins. Phase 2 consumes the approved Design Brief and assembles a complete SKILL.md by composing ecologically adapted **Cognitive Modules** — reusable reasoning packages whose core DNA is preserved but whose expression mutates to fit the specific domain. This paper formalizes CCSB as the proprietary skill construction system for the Conscious Coaching Platform (CCP), grounding each architectural decision in empirical findings from SkillNet (Liang et al., 2025), Evolving Programmatic Skill Networks (Shi et al., 2025), SkillCraft (Zhou et al., 2025), SkillFactory (Deng et al., 2025), SteerEval (Xu et al., 2025), and SkillOrchestra (Chen et al., 2025).

---

## 2. The Problem: Why Monolithic Skill Authoring Fails at Scale

The CCP operates 65+ specialized skills across five sub-systems (CCF, CMF, CBCS, V2WS, Excalidraw), serving a multi-agent pipeline where each skill's output becomes the next skill's input. At this scale, monolithic authoring — writing complete SKILL.md files from scratch — introduces three compounding failure modes that empirical research independently confirms.

**Failure Mode 1: The Reinvention Tax.** SkillNet's analysis of 200,000+ skills reveals that agents "frequently reinvent the wheel, rediscovering solutions in isolated contexts without leveraging prior strategies" (Liang et al., 2025). In the CCP, this manifests when a new Hunter skill re-derives the Distillation Funnel logic instead of composing from a standardized module. Each re-derivation introduces subtle variance — slightly different scoring thresholds, incompatible compression definitions — that compounds across the pipeline. SkillNet demonstrates that formalizing skills as "evolving, composable assets" improves agent performance by 40% and reduces execution steps by 30%, directly attributable to eliminating redundant discovery.

**Failure Mode 2: Creator Quality Dominates.** The Agent Skills benchmark (Li et al., 2025) establishes that "curated agent Skills significantly boost LLM agent performance (+16.2 pp on average) while self-generated Skills offer no gain." This finding — Signal 17 in our architecture paper — reveals that the quality of the skill *author* matters more than the capability of the executing *agent*. Monolithic authoring places the full cognitive burden on individual authors, guaranteeing inconsistent quality. CCSB addresses this by standardizing the highest-leverage components (reasoning modules) as pre-authored, pre-validated packages.

**Failure Mode 3: Controllability Degrades with Granularity.** SteerEval (Xu et al., 2025) demonstrates that LLM behavioral control "often degrades at finer-grained levels," with activation-based steering dropping from 2.76 at L1 (intent) to 0.07 at L3 (implementation). This has direct implications for skill authoring: high-level intent ("extract viral quotes") is easy to specify, but the fine-grained implementation detail ("score using Frame Alignment Multiplier with cluster-specific thresholds") is precisely where LLMs lose controllability. CCSB's two-phase architecture separates these concerns: Phase 1 operates at L1-L2 (intent and strategy), Phase 2 operates at L3 (implementation) using pre-validated modules that have already solved the controllability problem for their specific domain of reasoning.

---

## 3. First Principles: The Ontological Foundation

CCSB rests on three ontological primitives established in the CCP Skill Architecture Paper (Directives 1, 6):

**Primitive 1 — The Agent/Skill Separation.** An Agent is an autonomous entity with an OODA loop, working memory, and decision authority. A Skill is a passive instruction set — the rulebook an Agent reads to execute one transformation. Conflating these primitives degrades system performance because the Skill inherits decision-making responsibilities it cannot fulfill. CCSB enforces this boundary at the schema level: the Skill Design Brief's fields (Intent, Action, Method) describe *procedures*, never *autonomous behaviors*. If a proposed skill requires open-ended routing ("if the user asks X, do Y"), the schema forces reclassification as an Agent definition.

**Primitive 2 — The Module as Cognitive DNA.** Drawing from the Reasoning Modules Ecology analysis, a Cognitive Module is a reusable reasoning pattern whose *core laws* are universal but whose *expression* mutates to fit specific environments. The Distillation Funnel always operates through Saturation → Classification → Compression → Gate, but what "Compression" means changes fundamentally between content generation (the Collapse Test), visual search (the Evidence Test), and voice emulation (Cross-Input Collision). Modules are not functions — they are biological species.

**Primitive 3 — Flat Composition, Not Hierarchical Nesting.** Evolving PSN demonstrates that while hierarchical skill compositions enable complex behavior, the credit assignment problem becomes intractable when nesting exceeds two levels. PSN's REFLECT mechanism performs "top-down symbolic differentiation" along executed traces, but failure signals attenuate rapidly through deep hierarchies. CCSB enforces flat composition: the Skill Builder Agent orchestrates Module-Skills independently, collecting their outputs before assembly. No Module-Skill invokes another Module-Skill. This architectural constraint ensures that every adapted module is independently inspectable and independently debuggable.

---

## 4. The Skill Design Brief: An 11-Field Schema for Phase 1

The Skill Design Brief is the sole deliverable of Phase 1. Its purpose is to capture the *strategic intent* of a skill in a format that enables managerial review without technical expertise. The schema was derived by synthesizing the 5-dimension framework from the CCP Architecture Refinement paper (Intent, Goals, Method, Outcome, Success Criteria) with empirical findings from SkillNet's Skill Ontology (relational modeling, cost-awareness) and SkillCraft's cross-task transfer requirements (parameter independence).

| # | Field | Definition | Review Question |
|---|-------|-----------|-----------------|
| 1 | **Intent** | The fundamental "Why" — the procedural mandate and routing value | *Why does this Skill need to exist? What gap does it fill?* |
| 2 | **Target** | The desired end-state of the data payload after successful execution | *What does "done" look like? What artifact exists that didn't before?* |
| 3 | **Context** | The environmental assumptions under which the Skill is valid | *What must be true in the pipeline before this Skill can run?* |
| 4 | **Trigger** | The event or condition that activates consideration of this Skill | *What observable signal causes the Orchestrator to load this Skill?* |
| 5 | **Inputs** | The information or parameters required, expressed as true variables | *What data does the Skill consume? Is every input parameterized?* |
| 6 | **Action** | The cognitive operation — a verb phrase describing the transformation | *What single operation does this Skill perform?* |
| 7 | **Method** | The procedure, algorithm, or tool combination used to perform the Action | *How does the Skill execute the transformation?* |
| 8 | **Modules** | The Cognitive Modules to be composed and ecologically adapted | *Which reusable reasoning packages does this Skill require?* |
| 9 | **Constraints** | Rules, limitations, and conditions that restrict execution | *What is the Skill NOT allowed to do?* |
| 10 | **Output Artifact** | The exact data payload schema, file format, and file path | *What is the precise shape of the output?* |
| 11 | **Success Criteria** | Observable conditions that confirm the Skill achieved its intended outcome | *How do we algorithmically verify successful execution?* |

The schema's power lies in its *separation of concerns*. Fields 1-4 (Intent, Target, Context, Trigger) are purely strategic — they answer "why, what, when, where" and require no technical knowledge to evaluate. Fields 5-7 (Inputs, Action, Method) bridge strategy and implementation. Field 8 (Modules) explicitly names the cognitive packages to be composed, creating a direct link to Phase 2. Fields 9-11 (Constraints, Output Artifact, Success Criteria) define the boundary conditions. A manager reviewing this schema sees the complete strategic picture in 11 fields without ever reading a line of algorithm pseudocode.

---

## 5. The Module Architecture: Cognitive DNA and Ecological Adaptation

The Module Architecture transforms the implicit reasoning patterns scattered across 65+ CCP skills into explicit, reusable, ecologically adaptable packages. Each Module is a standalone document stored in `intelligence/modules/` that defines three components: Core DNA (the universal pattern), the Adaptation Protocol (how to mutate it), and a Reference Example (a production mutation from an existing skill).

This architecture is grounded in two empirical observations. First, the Reasoning Modules Ecology analysis proves that copying reasoning logic between skills without adaptation causes "intelligence collapse." The Distillation Funnel's Compression law means "merge signals for density" in content generation but means "test if the image proves the narrator's sentence with audio muted" in visual search. The Module Architecture formalizes this insight: Core DNA is preserved, but every deployment requires explicit ecological adaptation. Second, SkillFactory's self-distillation research (Deng et al., 2025) demonstrates that cognitive behaviors can be reliably transferred between LLM instances when they are explicitly tagged with structural markers rather than embedded in flowing prose. Their finding that "explicit tags outperform implicit reasoning" directly informs our requirement that every module adaptation must produce structured, tagged output — not narrative descriptions.

### The Initial Module Registry

| Module | Core DNA | Adaptation Axis |
|--------|---------|-----------------|
| **Distillation Funnel** | Saturation → Classification → Compression → Gate | What "Compression" and "Gate" mean changes per domain |
| **Contrastive Anchor** | Generate the domain-specific "generic AI failure mode" as negative baseline | The failure mode profile must be calibrated to each skill's output type |
| **Draft → Critic → Synthesis** | Multi-pass deliberation with explicit structural tags | Critic questions and synthesis rules adapt to the evaluation domain |
| **I-R-E-V-C Protocol** | Ingest → Reason → Emit → Validate → Checkpoint | Loading sequence and validation gates adapt to pipeline position |
| **Negative Space Loader** | Boundaries-first input loading | Forbidden vocabulary, tones, and rhetorical moves adapt to voice profile |
| **Three-Layer Voice Separation** | Soul + Mechanics + Emotion as independent channels | Layer weights shift based on whether skill generates, audits, or transforms |
| **Pre-Generation Constraints** | Front-loaded quality gates (not post-hoc checklists) | Specific constraints (word limits, structural tests) adapt to output type |
| **Graceful Degradation** | `[MISSING_DATA]` fallback pattern | Fallback behavior adapts: typed defaults for CBCS, explicit gaps for CMF |

---

## 6. The Skill Factory Pipeline: How Phase 2 Works

Phase 2 is an automated pipeline that consumes the approved Skill Design Brief and produces a complete, architecturally compliant SKILL.md. The pipeline follows SkillNet's three-step Discovery-Activation-Execution lifecycle, applied at the meta-level: the Skill Builder Agent discovers which Modules are needed, activates each Module-Skill to produce an adapted configuration, and executes the final assembly.

**Step 1: Module Identification.** The Skill Builder Agent reads the approved Design Brief's `Modules` field. This field explicitly names the Cognitive Modules required (e.g., "Distillation Funnel, Contrastive Anchor, Draft → Critic → Synthesis"). The Agent validates each module against the Module Registry, confirming that every named module exists and that no required module has been omitted.

**Step 2: Parallel Module Adaptation.** For each identified module, the Skill Builder Agent invokes the corresponding Module-Skill. Each Module-Skill is a focused adapter (approximately 100-150 lines) that takes two inputs: the generic module template (Core DNA) and the domain context extracted from the Design Brief (Intent, Action, Constraints, Output Artifact). The Module-Skill produces a JSON output containing the ecologically adapted module configuration. Critically, these invocations happen at the Orchestrator level — the hierarchy belongs to the Agent, not inside any Skill, compliant with Directive 6 (Flat Architecture).

**Step 3: Skill Assembly.** The Skill Assembler Agent takes all adapted module JSONs, the approved Design Brief, and the V3 Skill Authoring Guide as inputs. It assembles the final SKILL.md by mapping each adapted module to its corresponding section in the Skill anatomy (Reasoning Architecture, Deliberation Protocol, Pre-Generation Constraints, Negative Space, etc.), filling in the YAML frontmatter from the Design Brief, and producing the I-R-E-V-C protocol from the Input/Output/Success Criteria fields.

---

## 7. The Controllability Hierarchy: Why Two Phases Are Necessary

SteerEval's hierarchical framework provides the theoretical justification for CCSB's two-phase separation. Their L1-L2-L3 hierarchy — "what to express" → "how to express" → "how to instantiate" — maps precisely onto the skill authoring problem.

**Phase 1 operates at L1-L2.** The Skill Design Brief captures *what* the skill should do (Intent, Target, Action) and *how* it should approach the task (Method, Modules, Constraints). At these abstraction levels, LLM controllability remains strong. SteerEval demonstrates that prompt-based steering at L1 achieves concept scores of 3.0+ on a 4-point scale, with Harmonic Mean staying stable "around 3.0 from L1 to L3" for prompt-based methods. The Design Brief leverages this by operating in the zone where AI-assisted authoring is most reliable.

**Phase 2 operates at L3.** The Module-Skills must produce fine-grained, domain-specific adaptations — the exact ecological mutations, the precise scoring thresholds, the specific failure mode profiles. This is the L3 "implementational level" where SteerEval shows that "most steering methods struggle to satisfy fine-grained requirements." CCSB solves this by *pre-solving* the L3 controllability problem: each Module-Skill is a curated, verified artifact that has already been authored at L3 quality by a skilled creator. The Skill Factory doesn't ask an LLM to reason at L3 from scratch — it asks it to *apply* a pre-validated L3-quality module, which is a fundamentally easier task.

This mirrors SteerEval's finding that "3-shot prompting" significantly outperforms zero-shot at fine-grained levels. The Module-Skills function as the "shots" — they provide the concrete, domain-specific examples that anchor the LLM's behavior at the implementational level, preventing the controllability degradation that occurs when LLMs attempt fine-grained generation without reference implementations.

---

## 8. Maturity-Aware Gating: Protecting Converged Modules

Evolving PSN's most important finding for CCSB is the necessity of maturity-aware update gating. Their experiments demonstrate that "without stabilization, converged skills are repeatedly modified by downstream failures, leading to oscillatory behavior." This directly threatens the Module Architecture: if a well-validated Distillation Funnel module is continuously modified by edge-case failures in new skills, its reliability degrades for all existing skills that depend on it.

CCSB implements a three-tier maturity classification for both Skills and Modules:

**Draft** (high plasticity): New modules and newly assembled skills. Accept breaking changes. Iterate freely based on execution feedback. All new outputs from the Skill Factory start here. The maturity promotion threshold requires passing 3+ real executions without structural failure.

**Tested** (medium plasticity): Modules and skills that have demonstrated reliable performance across multiple diverse inputs. Changes require written justification and must not break documented behavior. Promotion to Stable requires 10+ successful executions across diverse input types, with no regression in downstream pipeline performance.

**Stable** (locked — low plasticity): Reference-quality modules and skills. Only structural augmentations are permitted; no behavioral modifications without full regression review. This mirrors PSN's finding that "mature skills with high V(s) receive infrequent updates, analogous to freezing converged layers."

Crucially, CCSB enforces PSN's critical finding about online versus offline refactoring: "When evaluated on compositional tasks, Voyager with offline refactoring achieves a success rate of 0.6875, compared to 0.8462 for PSN with online refactoring." All module and skill refinement in CCSB must be performed *online* — tightly coupled with real execution failures — never through batch offline rewrites that process 20 skills in a single session without execution feedback.

---

## 9. The Skill Relation Graph: Preventing Ecosystem Fragmentation

SkillNet's Skill Ontology introduces four relational primitives that CCSB adopts directly into the YAML frontmatter of every SKILL.md: `similar_to`, `compose_with`, `depend_on`, and `belong_to`. These relations form the **Skill Relation Graph** — a directed, typed multi-relational graph where nodes represent skills and edges encode functional associations.

The Relation Graph serves three critical functions in CCSB. First, **redundancy prevention**: before the Skill Factory assembles a new skill, it queries the `similar_to` edges to verify that no existing skill already provides functionally equivalent capability. SkillNet's deduplication pipeline demonstrates that "filtering eliminates low-quality, incomplete, or semantically meaningless skills through rule-based validation and model-based checking." CCSB applies this principle proactively at the Design Brief stage, not reactively after skills proliferate.

Second, **composition planning**: the `compose_with` edges identify skills that are frequently co-invoked — one's output feeds the other's input. During Phase 2, the Skill Assembler uses these edges to verify that the new skill's output schema is compatible with the schemas expected by downstream skills. This prevents the silent interface breakage that occurs when a skill author inadvertently changes an output format without updating downstream consumers.

Third, **impact analysis**: the `depend_on` edges enable the system to calculate the blast radius of any proposed change. When a Stable-tier module is modified, the Relation Graph traces all skills that depend on it, enabling targeted regression testing rather than full-pipeline re-validation. This directly implements PSN's rollback validation principle: "If the task success rate drops by more than 20%, the refactor is reverted."

---

## 10. The Five-Dimension Evaluation Rubric

SkillNet's multi-dimensional evaluation framework provides the formal quality assurance layer for CCSB. Every skill produced by the Skill Factory is scored across five dimensions before it can be promoted beyond Draft maturity:

**Safety** evaluates potential risks, including unauthorized actions, prompt injection vulnerabilities, and boundary violations. For CCP skills, this specifically includes voice identity leakage (a skill generating content in a voice profile that doesn't belong to the current coach) and privacy boundary violations (a skill accessing data outside its declared input scope).

**Completeness** evaluates whether the skill encapsulates all procedural steps and explicitly defines prerequisites, dependencies, and execution constraints. In CCSB, completeness is verified by checking that every field from the Skill Design Brief has a corresponding implementation in the assembled SKILL.md — no Intent without a Cognitive State Instruction, no Constraints without a Negative Space section, no Success Criteria without Structural Completion Criteria.

**Executability** verifies that the skill can be successfully executed by agents. For CCSB, this means validated against real pipeline inputs, not synthetic test cases. SteerEval's finding that controllability degrades at finer granularities means that executability must be tested at the L3 level — with actual coach transcripts, real voice DNA profiles, and production-scale inputs.

**Maintainability** measures modularity and composability. CCSB scores this dimension by analyzing how many of the skill's reasoning components are composed from standardized modules versus custom-written logic. A skill that imports 80% of its reasoning from validated modules scores higher than one that implements everything from scratch, because the modular skill benefits from upstream improvements to its constituent modules.

**Cost-awareness** quantifies execution overhead. Every CCSB-produced skill must declare `estimated_tokens` and `execution_tier` in its YAML frontmatter, enabling the Orchestrator to make routing decisions that balance quality against computational cost. This directly implements SkillNet's finding that cost-awareness must be a first-class evaluation dimension, not an afterthought.

---

## 11. Cross-Task Transfer: The Parameter Independence Principle

SkillCraft's most direct contribution to CCSB is the empirical demonstration that skills must encode *procedures*, never *instances*. Their cross-task transfer experiments reveal that skills parameterized with true variables outperform skills with hardcoded values by a significant margin, because the parameterized skill generalizes to novel inputs while the hardcoded skill fails silently when input characteristics change.

CCSB enforces parameter independence at two levels. At the Design Brief level, the `Inputs` field requires all dynamic values to be expressed as named variables. The schema rejects any Design Brief where the Inputs field contains hardcoded content — "Process the 30-minute English interview" fails validation; "Process the input transcript (language and duration auto-detected)" passes. At the Module level, each Module-Skill's adaptation process is parameterized by the Design Brief's domain context, not by specific instance data. The Distillation Funnel Adapter produces a mutation for "testimonial extraction" — not for "Jean-Pierre's French testimonial about Maman Adele."

This principle has a direct connection to SkillOrchestra's routing logic. SkillOrchestra demonstrates that effective skill routing requires skills to advertise their capabilities through crisp, parameterized descriptions. If a skill's description contains instance-specific language, the router cannot generalize its capability assessment to novel inputs. CCSB's requirement that the `description` field follow the format "Takes [Input] to perform [Transformation] resulting in [Output]" ensures that every skill produced by the Factory is routable by capability, not by instance.

---

## 12. The Managerial Review Gate: Bridging Strategy and Implementation

CCSB's two-phase architecture introduces a natural checkpoint that solves a problem no existing skill framework addresses: how does a non-technical manager verify that a skill aligns with strategic objectives before engineering resources are committed?

In monolithic authoring, the manager sees either nothing (the skill is built without review) or everything (an 800-line technical document that requires engineering fluency to evaluate). CCSB's Phase 1 deliverable — the 11-field Skill Design Brief — is designed specifically for managerial legibility. The manager evaluates: Does the *Intent* align with the current pipeline gaps? Does the *Target* produce an artifact that downstream systems actually need? Does the *Context* accurately describe when this skill should activate? Are the *Modules* appropriate for the cognitive complexity of the task? Do the *Constraints* prevent the skill from overstepping its boundaries?

This review gate also prevents a failure mode that SkillFactory's self-distillation research identifies: the tendency of AI systems to produce skills that are "surface-level satisfying but structurally hollow." A generated skill might have correct YAML frontmatter and plausible algorithm phases while completely lacking the ecological adaptations that make reasoning modules perform in their specific domain. The Design Brief forces the *intent* to be stated before implementation, making it impossible to produce a structurally hollow skill that passes surface inspection — because the implementation has not yet been written. If the Intent is hollow, the manager catches it in 11 fields rather than hunting for it in 800 lines of pseudocode.

Furthermore, the managerial review gate implements what Evolving PSN calls the "separation of credit assignment from code modification." In PSN, failure signals are first propagated to identify *which* component is responsible before any repair is attempted. CCSB applies this same principle to the authoring process itself: Phase 1 identifies *what* needs to be built and verifies it against strategic requirements. Only after this verification does Phase 2 commence with *how* to build it. This prevents the common failure pattern where an author builds a technically excellent skill that solves a problem no one actually has.

---

## 13. Conclusion: The Arsenal's Keystone

The Conscious Composable Skill Builder represents the convergence of six independent lines of empirical research into a single, proprietary construction system. SkillNet proves that skills must be composable assets with relational graphs, not isolated files. Evolving PSN proves that maturity-aware gating and online refactoring are essential for skill ecosystem stability. SkillCraft proves that parameterized skills transfer across tasks while instance-specific skills fail. SkillFactory proves that cognitive behaviors must be explicitly tagged, not implicitly embedded. SteerEval proves that controllability degrades with granularity, requiring separation of intent from implementation. SkillOrchestra proves that routing efficiency depends on crisp capability descriptions and relation-aware selection.

CCSB synthesizes these findings into an architecture that separates design from implementation, composes from standardized modules instead of reinventing, protects converged capabilities through maturity gating, prevents ecosystem fragmentation through relation graphs, and provides managerial visibility through a legible 11-field schema. For the CCP — a platform operating 65+ skills across five sub-systems serving production coaching clients — CCSB is not an optimization. It is the foundational infrastructure that determines whether the skill ecosystem grows with compounding quality or degrades with compounding variance.

The Skill Design Brief ensures that every skill begins with strategic clarity. The Module Architecture ensures that every skill composes from validated cognitive DNA. The Skill Factory Pipeline ensures that every skill is assembled with consistent structural rigor. The Maturity Classification ensures that every skill's reliability is protected as the ecosystem evolves. Together, these components form the arsenal's keystone — the single system upon which all downstream skill quality, pipeline reliability, and platform scalability ultimately depend.

---

**References**

- Liang, Y., et al. (2025). *SkillNet: Create, Evaluate, and Connect AI Skills*. Zhejiang University, Alibaba Group.
- Shi, H., Yuan, X., & Liu, B. (2025). *Evolving Programmatic Skill Networks*. Université de Montréal, Microsoft Research.
- Zhou, J., et al. (2025). *SkillCraft: Can LLM Agents Learn to Use Tools Skillfully?*
- Deng, S., et al. (2025). *SkillFactory: Self-Distillation For Learning Cognitive Behaviors*.
- Xu, Z., et al. (2025). *How Controllable Are Large Language Models? A Unified Evaluation across Behavioral Granularities*. Zhejiang University, Alibaba Group.
- Chen, L., et al. (2025). *SkillOrchestra: Learning to Route Agents via Skill Transfer*.
- Li, Y., et al. (2025). *Agent Skills: A Data-Driven Analysis of Claude Skills for Extending Large Language Model Functionality*.
- CCP Architecture Papers: *CCP Skill Architecture Refinement* (5-Dimension Schema), *The Ecology of Reasoning Modules* (Cognitive Adaptability), *CCP Skill Architecture Paper* (25 Empirical Signals + 12 Directives).
