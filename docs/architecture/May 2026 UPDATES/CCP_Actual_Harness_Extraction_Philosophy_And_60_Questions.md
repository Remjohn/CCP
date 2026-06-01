# The Actual Harness: Philosophy, Creative Friction, and the 60-Question Extraction Grid

*Project: Conscious Coaching Platform (CCP / Conscious Elite)*  
*Target: Harness Clean Extraction & Orchestration Design*  
*Date: May 2026*  
*Word Count Target: ~2,300 words*

---

## Part 1: The Creative MVP and the Value of Intentional Chaos

Before extracting the Actual Harness, we must validate a fundamental truth about your development process thus far: **Building a "semicorrect, modular, but disorganized" codebase was not a failure of engineering—it was the engine of your creative process.**

As you correctly identified, removing friction allowed you to innovate, test wildly, and iterate rapidly. If you had bogged yourself down in strict CI/CD pipelines, perfect directory structures, and rigid test-driven development from Day 1, you would have stifled the creative discovery of the Conscious Media Factory (CMF), the Trigger-First execution loop, and the 150+ psychological primitives. 

You built the codebase to discover the product. **The real MVP is not the 5,300+ Python files; the real MVP is the exhaustive set of PRDs, architectural blueprints, and spec prompts you derived from that chaos.** 

You now possess the perfect idea of the product, codified in the May 2026 specs. Having used creative chaos to map the territory, you must now pivot sharply. To build the "Actual Harness" in a new, clean environment, you must intentionally reintroduce friction. The extraction process is fundamentally about taking the validated modules and assembling them under a strict, unforgiving orchestration layer. 

We must also validate your intuition about **Primitives and Just-In-Time (JIT) SKILL.md files**. Placing primitives structurally inside the Evaluation layer is a massive architectural advantage. It means quality is not an afterthought; the primitives *are* the standard of quality against which outputs are measured. Similarly, transitioning to JIT SKILL.md files—where agents dynamically pull specific workflow recipes exactly when needed—is the definition of a modern, scalable AI software factory.

---

## Part 2: Synthesizing the 7 Pillars of AI Engineering

To design the Actual Harness correctly, we must reconcile the insights of seven leading AI engineering practitioners. Interestingly, they do not all agree. The tension between their approaches is where the CCP Harness will find its optimal structure.

### 1. The Orchestration Tension: DAGs vs. Dumb Loops
* **Sandipan Bhaumik (Multi-Agent Orchestration):** Argues that multi-agent systems are fundamentally distributed systems. They require strict, centralized Orchestrators using Directed Acyclic Graphs (DAGs), immutable state versioning, and the Saga pattern for complex rollbacks.
* **Chris Parsons (Ralph Loops):** Argues the exact opposite. Complex DAGs are brittle and recreate waterfall methodologies. Instead, he advocates for "Dumb Loops" (like Ralph Wiggum)—a simple `while true` loop where an agent assesses the repository state, picks the next logical task, and executes until it hits an "edge" of irreversibility.

**The CCP Resolution:** We must use *both*. The global pipeline (Ingestion $\rightarrow$ Transcription $\rightarrow$ Drafting $\rightarrow$ Rendering) requires strict DAG orchestration. However, inside a specific node (e.g., the CMF drafting module), we should deploy Dumb Loops where the drafting agent iteratively refines the script against the primitive evaluation layer until it passes.

### 2. Role Segregation and Validation Contracts
* **Luke Alvoeiro (Factory):** AI is a terrible self-evaluator. You must separate your ecosystem into Orchestrators (planning), Workers (implementation), and Validators (testing). Crucially, the Orchestrator must write a strict "Validation Contract" *before* any code is written, ensuring tests validate the requirements, not the implementation.
* **Ash Prabaker & Andrew Wilson (Anthropic):** Echo this need for separation. Agents that run for hours suffer from "sycophancy bias" (rubber-stamping their own work). You must employ Adversarial Evaluators with harsh, explicit rubrics. Furthermore, state must be persisted strictly to the file system (JSON trackers, Markdown contracts), not just held in a massive, degrading context window.

### 3. The Harness as a Deterministic Cage
* **Tejas Kumar (IBM):** The LLM is probabilistic; the Harness must be deterministic. When an agent fails, the reflex should not be to "prompt harder." You must build deterministic guardrails—intercepting tasks like API authentication or state tracking in standard code, entirely bypassing the LLM. The Harness acts as a Verify Step, preventing the agent from "lying" about task completion.
* **Eric Zakariasson (Cursor):** A Software Factory requires explicit primitives and patterns. Standard boilerplates must exist so agents don't have to guess how to navigate the codebase. Guardrails should emerge dynamically from failures, and engineers must transition from coding to managing an asynchronous fleet.

---

## Part 3: The 60-Question "Actual Harness" Extraction Grid

To ensure we do not blindly extract a broken harness, we must answer the following 60 questions. They are grouped into 5 architectural pillars. Answering these will mathematically define the structure of your new Clean Environment.

### Pillar 1: AI Engineering & Grounding
1. **Grounding & Provenance:** What authoritative data sources serve as the "ground truth" for your agents, and how will your application layer structurally prevent the model from answering if that data is missing?
2. **Context Pipeline Hierarchy:** How are you structuring context packets to separate immutable system policies, user intent, and retrieved facts to protect the model's fragile working memory?
3. **Safe Context Compression:** When editing sessions exceed the context window, what is your strategy for safely compressing state without losing verbatim facts (e.g., primitive definitions)?
4. **Tool Boundaries & Idempotency:** What least-privilege boundaries are applied to tools, and how are you handling operational concurrency when multiple agents execute tasks in parallel?
5. **Evaluation "Golden Set":** What specific edge cases, prompts, and expected behavioral outcomes make up the "golden set" of regression tests you will use to measure tool reliability nightly?
6. **Instruction vs. Data Isolation:** How is your harness sanitizing external context to guarantee that retrieved chunks or malicious user inputs cannot override core system instructions?
7. **Semantic Routing:** How will you route user intents or triggers to the correct agent or sub-system without relying on a massive, error-prone master prompt?
8. **Latency vs. Accuracy:** What is your exact tolerance for latency vs. accuracy in the Trigger-First execution loop, and where are you willing to cache results or use faster models?
9. **Fallback Mechanisms:** When a tool call fails completely (e.g., API timeout), does the agent retry, degrade to a simpler response, or halt the entire pipeline?
10. **State Telemetry:** How are you logging the internal "thoughts" or hidden states of the agents so that human operators can debug logic failures post-mortem?
11. **Hallucination Penalties:** If the system detects a hallucination during the deterministic "Verify Step", how is the agent penalized or corrected within the same session?
12. **Data Freshness:** For grounding data that changes frequently (e.g., coach availability), what is the TTL (Time to Live) strategy for your RAG/context cache?

### Pillar 2: The Orchestration Tension (DAGs vs. Dumb Loops)
13. **Coordination Strategy:** Which macro-level pipelines require strict, centralized DAG orchestration, and which micro-level tasks are better suited for autonomous, event-driven choreography?
14. **The "Dumb Loop" Boundary:** Where in the CCP pipeline can we implement "Ralph Loops" (simple, iterative `while true` refinement) instead of over-engineering fragile, multi-agent dependency trees?
15. **Defining the Edges (Reversibility):** How explicitly does the Harness define the boundary between "reversible" actions (where a loop runs fully autonomously) and "irreversible" actions (where the loop must halt for human intervention)?
16. **State Immutability:** Can we transition the macro harness to an append-only, immutable state architecture (e.g., state versioning) to eliminate race conditions and enable step-by-step replayability?
17. **Dynamic Task Selection:** Rather than pre-computing fragile dependency trees up front, how does the harness provide the agent with enough state awareness so it can organically determine the next logical step?
18. **Data Contracts:** What are the explicit JSON/Pydantic schemas defining the inputs and outputs between agents to catch poor-quality data before it cascades downstream?
19. **Circuit Breakers:** If a critical sub-agent fails repeatedly in production, what specific thresholds and graceful degradation behaviors should the harness enforce?
20. **The Saga Pattern (Compensation):** When a complex workflow fails mid-execution, what is our strategy to undo the partial work? Do we have explicit `compensate` (rollback) methods?
21. **Context Renewal vs. Rot:** Does the harness force the agent to retain a massive, degrading session context, or does it drop context and perform a fresh evaluation of the raw state to catch missed details?
22. **Agent Lifecycle Management:** How is an agent "spun up" and "spun down"? Are they ephemeral serverless functions or persistent background workers?
23. **State Hydration:** When an agent wakes up to process a task in a long-running workflow, how exactly does it "hydrate" its state (pulling full history vs. a diff)?
24. **Concurrency Limits:** How do you prevent a "thundering herd" scenario where 50 coaches trigger complex workflows simultaneously, starving the orchestration engine?

### Pillar 3: Role Segregation & Validation Contracts
25. **Validation Contracts:** How will the Actual Harness define and enforce "Validation Contracts" independently of implementation *before* code/content is generated?
26. **Adversarial Evaluation:** How does the harness separate the generation role from the evaluation role to avoid self-approval traps?
27. **Harsh Rubrics:** What specific, harsh rubrics will the adversarial critic enforce (e.g., grading on primitive congruence, anti-slop integrity, and storytelling pace)?
28. **Contract Negotiation:** By what mechanism do the generator and evaluator agents negotiate and formalize the exact definition of "done" before the generator takes action?
29. **Structured Handoffs:** What schema will we use for "structured handoffs" at milestone boundaries to force agents to document completions, failures, and exit codes, preventing context degradation over long tasks?
30. **Role Segregation & "Droid Whispering":** How will the Actual Harness separate the Orchestrator, Worker, and Validator roles, and which specific LLM models will be assigned to each seat?
31. **State Persistence (File System):** Which specific artifacts will the harness persist to the file system (e.g., JSON trackers, Markdown contracts) to maintain shared state, rather than depending on continuous context windows?
32. **Traceability & Refinement:** What is the protocol for capturing raw agent traces, and what is the human process for manually reviewing these traces to refine scaffolding prompts?
33. **End-to-End Adversarial UI Testing:** Beyond standard linting, how can the Actual Harness implement an "Adversarial Validator" that spawns a live application instance to test behavior end-to-end?
34. **Primitives as Evaluation Standard:** How precisely are the 150+ primitives wired directly into the Validator agent's core system prompt to serve as the absolute standard of quality?
35. **JIT SKILL.md Resolution:** How does the Orchestrator dynamically look up and inject "Just-In-Time" SKILL.md recipes based on the specific lesson format being generated?
36. **Collusion Prevention:** How do you prevent Generator and Validator agents from colluding or falling into a positive-feedback loop of approving bad content?

### Pillar 4: Deterministic Harnesses & Guardrails
37. **The Verify Step:** How are you deterministically verifying your agent's success (checking trace logs/system state) to ensure it isn't "lying" about task completion?
38. **Prompting vs. Harnessing:** What frequent failure modes are you currently trying to fix by "prompting harder," and how can we replace them with structural, deterministic code interventions?
39. **Intercepting Deterministic Tasks:** Where does your agent risk security trying to solve deterministic workflows (like authentication/routing) that should be intercepted by the harness code?
40. **Hard Guardrail Strategy:** What happens to the agent loop when it hits an unrecoverable state or exceeds its maximum allowed iterations?
41. **Trace History Isolation:** Are you maintaining a strict, external trace history of the agent's state changes to actively reflect on and correct its course?
42. **Model Independence:** If forced to swap your frontier model for a cheaper open-source model tomorrow, how can we build the harness so the weaker model still succeeds?
43. **Deterministic State Machines:** Which parts of the "Complete Editing Session" must be modeled as a strict, hardcoded state machine rather than relying on an LLM to decide the next step?
44. **Type-Safe Payloads:** Are the JSON payloads passing between your harness and the LLMs strictly validated against Pydantic models or Zod schemas?
45. **Prompt Versioning:** How do you version your system prompts alongside your codebase to guarantee that if an API changes, the prompt updates synchronously?
46. **Token Budgeting:** How does the harness enforce a strict token budget per task and preemptively stop an agent that is burning tokens without producing value?
47. **The "Human Handoff" Trigger:** Under what exact, deterministic conditions does the harness freeze the automated workflow to explicitly request human intervention?
48. **Sandbox Escapes:** If the LLM generates a tool call that attempts unauthorized operations, how does the execution boundary detect and block it?

### Pillar 5: Software Factory Mechanics
49. **Primitives & Patterns:** What are the foundational architectural patterns and standard boilerplates in your current codebase that we must strictly codify in the new clean environment?
50. **Emergent Guardrails:** Which high-risk domains of your system require strict modification limits, and what feedback loop will dynamically capture new rules when an agent goes off-track?
51. **Enablers & Context:** What external data sources (e.g., Jira, Notion, Logs) must your agents be connected to within the factory environment?
52. **Self-Verification:** How will your agents definitively test their own work autonomously using existing CI/CD or Playwright checks?
53. **Automating the Manager:** What repetitive manual reviews or context-gathering steps are you currently performing that we can replace with a background "Review Agent"?
54. **Observability & Friction:** If we gave the agents a "vent tool" to report when they are blocked by the environment, what are they most likely to complain about today?
55. **The "Golden Path" Onboarding:** If a new AI coding agent joins the factory today, what is the exact documentation it reads to immediately understand repository structure and coding standards?
56. **Automated Rollbacks:** If an agent ships code that passes unit tests but breaks the UI, what is the automated mechanism to instantly rollback the deployment?
57. **Test Data Generation:** How do the agents generate realistic but safe test data for their PRs without exposing actual coach PII?
58. **Dependency Auditing:** What strict automated security scanning exists in the factory to block hallucinated or malicious NPM/PyPI packages?
59. **Environment Parity:** How do you guarantee that the isolated sandbox where the agent tests code is a 1:1 identical match to the production environment?
60. **The "Clean Extraction" Metric:** At the end of the 7-day extraction sprint, what is the exact numerical or functional metric (e.g., "Living Commentary renders via Remotion perfectly") that proves the new Harness is successful?

---

## Conclusion: The Path Forward

The disorganized, friction-less MVP phase served its purpose brilliantly: it illuminated the **"What"** (the PRDs, the Primitives, the Specs). 

The 60 questions above are strictly concerned with the **"How."** Before we extract the first file into the new environment, we must build the walls of the factory. By answering these questions, you will construct a deterministic cage that keeps your probabilistic agents productive, safe, and observable.
