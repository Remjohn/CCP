# CCP SKILL Architecture Refinement: The Core 5 Dimensions

*A First-Principles, System-Thinking Approach to Intent, Goals, Method, Outcome, and Success Criteria*

**CRITICAL ONTOLOGICAL BOUNDARY:** Before defining the architecture of a `SKILL.md`, we must strictly separate the concepts of Agent, Subagent, and Skill, as defined in the GLM-5 "Agentic Engineering" research and MATTRL principles:
*   **The Agent**: The autonomous intelligence (e.g., The Orchestrator, The Story Doctor). The Agent runs the execution loop (OODA), manages working memory, folds context, and makes decisions.
*   **The Subagent**: A transient persona or specialized child-process (e.g., Scout, Planner, Reviewer). Subagents are instantiated by the Agent to constrain context and isolate specific cognitive evaluations.
*   **The Skill**: A passive, instructional procedure (the `SKILL.md`). A Skill is *not* autonomous. It does not "think." It is the explicitly engineered rulebook, constraints, and operational logic that an Agent reads to know *how* to execute a highly specialized transformation.

If we anthropomorphize the Skill by assigning it Agentic capabilities, the system breaks. The following architectural guidelines define the 5 core dimensions strictly for **Skills**—the procedural tools wielded by the Agents.

---

## 1. Intent (The "Why" and Ecosystem Alignment)

The **Intent** represents the fundamental "Why" behind this specific *procedure*. Viewed through the lens of First Principles, the Intent is not about the Agent's autonomy; it is the "Expertise Tag" used by the Orchestrator to route tasks, directly mapping to the *SkillOrchestra* framework's routing logic.

When a user request triggers the Orchestrator's "Orient" phase, the Orchestrator must select a tool to use. The Intent block is the machine-readable advertisement of the Skill's utility. 

To author a high-scoring Intent, you must define the procedural value proposition:
1. **The Procedural Mandate**: A single, unambiguous sentence defining exactly what transformation this rulebook facilitates (e.g., "Transforms authenticated chronological footage into a rhythmically coherent narrative script").
2. **The Orchestrator Routing Value**: Explicit guidance instructing the Orchestrator *when* to load this skill into an Agent's context over an alternative. 
3. **The Cognitive Stance Requirement**: While the Skill cannot "think," it *requires* the executing Agent to adopt a specific posture (e.g., "The Agent executing this skill must operate as a hyper-critical auditor").
4. **The Negative Space (Boundary Definition):** As seen in *MATTRL's* expert catalog, explicit boundaries prevent scope creep. The Intent must explicitly state what the procedure does *not* cover, instructing the Orchestrator when to spawn a different Subagent instead (e.g., "This skill analyzes audio transcripts; it does NOT analyze visual composition").

By treating the Intent as a precise routing mechanism rather than an autonomous mission statement, we prevent redundant loop cycles and ensure Orchestrator accuracy.

---

## 2. Goals (The Directed Payload State)

If the Agent's goal is to "Solve the user's problem," the **Skill's Goal** is "Produce a deterministic, structurally verified artifact." Leveraging System Thinking, a Skill's Goal must be defined as the required end-state of the *data payload*, not the terminal state of the *Agent*.

In the Event-Condition-Action (ECA) paradigm, the Agent runs the loop. The Skill's Goals section defines the **Condition** that the Agent uses to mathematically prove the action was successful before folding its memory and moving to the next pipeline stage.

A properly architected Goals section must be structured hierarchically:
1. **The Terminal Payload State**: The ultimate reality of the output data (e.g., "A mathematically verified mapping of audio transients to visual cuts exists in the required JSON format").
2. **The Enabling States (Micro-Deliverables)**: The sequential data conditions that must be met along the way (e.g., "All filler words are removed," "Tribal terms are dynamically inserted").
3. **The Global Optimization Target**: The underlying metric the Agent should maximize while generating this artifact (e.g., "Maximal compression of thought, minimal token count").

Applying *Multi-Agent Chain-of-Draft Reasoning (DRAFT-RL)*, the Skill's Goal must define the *characteristics* of a valid solution, allowing the executing Agent to generate multiple drafts and evaluate them against these characteristics. The Goal is the rigid yardstick against which the Agent measures its own divergent drafts.

---

## 3. Method (The ECA Execution Scaffolding)

The **Method** is the algorithmic scaffolding. While the Agent provides the engine, the Method provides the tracks. To architect this section, we fully engage the OODA/ECA paradigm as a set of *instructions* given to the Agent.

**Observe (Input Loading Sequence)**
The Method must explicitly dictate to the Agent *what* inputs to load and in *what sequence*. Drawing from the *DeepAgent* architecture, this is the environment ingestion phase. The Skill instructs the Agent to read specific files, parse PRDs, or load metadata constraints (like `voice_dna`). 

**Orient (Chain-of-Draft Constraints)**
Once the data is loaded, the Skill dictates *how* the Agent must orient itself. Applying *DRAFT-RL*, the Method should force the Agent to use "Chain-of-Draft" (CoD) reasoning steps before generating the final artifact. The Skill imposes the constraint: "Before writing the final text, output a 5-word micro-draft of the underlying logic." 

**Decide (Internal Rubrics)**
The Skill provides the decision-making rubrics. If the procedure requires complex problem-solving, the Method instructs the Agent to instantiate Subagents. For example, the Method might say: "Spawn a 'Critic Subagent' to evaluate your generated draft against the Negative Space parameters. Do not proceed until the Critic Subagent returns a pass." This mirrors the *MATTRL* methodology of multi-expert deliberation, but codified procedurally within the Skill's instructions.

**Act (Step-by-Step Logic)**
The Method lists the exact procedural logic the Agent must execute. It is critical that the Method does not dictate *how the framework operates* (the Skill doesn't say "Now fold your memory," because the harness manages memory). Instead, it says "Now execute the compression algorithm applying the LiWC fidelity gate."

---

## 4. Outcome (Systemic Interface Protocols)

The **Outcome** represents the strict data payload the Agent must yield. Applying System Thinking, the Outcome is the exact input the next chronological Agent in the CCP pipeline will consume. Without absolute rigidity in the Outcome specification, the entire pipeline crashes.

Leveraging *Agentic Context Engineering (ACE)*, the Outcome must be viewed as an "Evolutionary Delta." The Skill guarantees that if the Agent follows the Method, the global context will mutate in this specific, predefined way.

The Outcome section must define:
1. **The Primary Artifact Schema**: The explicitly engineered data shape (JSON, Markdown frontmatter, specific headers). It must provide concrete, zero-ambiguity examples of output boundaries.
2. **The Procedural Log Request**: Instructions for the Agent to output a structured summary of *why* it made certain decisions during the execution of the Skill. This allows downstream Agents to read the rationale, not just the result.
3. **The Failure Payload**: Crucially, the Skill must define what the Agent should output if the Method cannot be completed (e.g., missing input files). Defining the exact structure of a `{"status": "failed", "reason": "..."}` payload ensures the Orchestrator can ingest the failure and launch an error-recovery OODA loop without crashing the system.

---

## 5. Success Criteria (Algorithmic Verification and Agent Evaluation)

The **Success Criteria** answers: How does the system algorithmically prove the Skill was executed correctly by the Agent? This is the boundary protecting the CCP from LRM hallucination.

In reinforcement learning paradigms like *MATTRL* and *DRAFT-RL*, success is evaluated through reward-aligned rubrics. The Success Criteria section of a `SKILL.md` provides the exact rubrics that an LLM-as-a-judge (a Reviewer Subagent) will use to score the performing Agent's output.

1. **Structural Validation (The Syntax Check)**: Does the generated output perfectly match the schema defined in the Outcome section? 
2. **Procedural Adherence (The Method Check)**: Did the Agent actually generate the mandated Chain-of-Draft reasoning steps requested in the Method, or did it skip straight to the final answer?
3. **Semantic Integrity (The Difference Reward Check)**: Applying *MATTRL's* Credit Assignment, the Success Criteria must establish the "counterfactual baseline." If the Agent had not used this Skill, what would the output look like? The criterion measures the semantic delta. For example, "When parsed by the Content Auditor, does this specific output contain exactly the Voice DNA rhythm patterns required, proving the Agent didn't just write generic LLM prose?"

By structuring Success Criteria as explicitly testable rules, the Skill allows the CCP to continuously evaluate the performance of its Agents, enabling true test-time reinforcement learning and preventing procedural degradation.
