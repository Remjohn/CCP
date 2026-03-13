# Signal Extraction — Batch 2: Skills as Living Systems

> **Papers analyzed:**
> 1. *Agent Skills: A Data-Driven Analysis of Claude Skills* (Ling, Zhong, Huang — Bosch/CMU)
> 2. *Evolving Programmatic Skill Networks* (Shi, Yuan, Liu — Montréal/Microsoft Research)
> 3. *SkillCraft: Can LLM Agents Learn to Use Tools Skillfully?* (Chen et al. — Oxford/CUHK/HKUST)
> 4. *SkillFactory: Self-Distillation For Learning Cognitive Behaviors* (Sprague et al. — NYU)

---

## Signal 15 — Skills-as-Code Compositions Reduce Token Usage by Up to 80%

**Source:** SkillCraft, Table 2 — GPT-5.2 token usage drops from 1.23M to 0.26M (-79%) with Skill Mode.

**Expanded Finding:** When agents consolidate frequently co-occurring tool chains into a single executable unit (code-based Skills), they achieve massive efficiency gains. The key mechanism is that code compactly represents data flow, control logic, and iteration. Instead of the LLM generating a natural language thought process for each step, parsing the output of Tool A, and then reasoning about what to pass to Tool B, the executable code handles the deterministic state passing directly. This eliminates redundant token generation between consecutive tool calls and prevents context window saturation over long horizons.

**Expanded CCP Implication:** Currently, our Skills (like the Witness Hunter) are 100% prose. Every scoring formula, every SRT parsing instruction, and every threshold check is described in natural language that the LLM must interpret and execute conceptually each time. This creates a high token burden and introduces the risk of hallucination on deterministic math. Extracting these deterministic computations into the `scripts/` folder (e.g., a python script that calculates the "Witness Score" based on predefined metrics) would let the Skill focus its expensive token budget purely on high-level cognitive judgment (e.g., quote selection, deliberation, narrative resonance) while offloading the heavy lifting to executable code. This is the primary driver for integrating `scripts/` into the Talent Paradigm.

---

## Signal 16 — Hierarchical/Deep Composition HURTS Performance (Skills vs. Sub-Agents)

**Source:** SkillCraft, Table 3 — GPT-5.2 drops from 90% to 79% success when moving from flat Skill to hierarchical composition.

**Expanded Finding:** The paper explicitly tests "hierarchical skills" (where a code-based Skill programmatically calls another code-based Skill inside its execution block). Despite high per-skill execution rates (95-99%), nesting skills inside skills creates three failure modes: 
1. **Compounding failures:** Success degrades exponentially with depth (a 95% reliable skill calling a 95% reliable skill drops overall reliability to ~90%).
2. **Latent bugs:** Edge cases in low-level skills only surface upon reuse in higher contexts, acting as invisible landmines.
3. **Debugging overhead:** Tracing nested failures costs more than re-executing with flat calls, meaning the LLM gets confused when trying to fix an error deep in the stack. 
The paper concludes: *"shallow, well-tested skill libraries are currently more reliable and cost-effective than deep, automatically generated hierarchies."*

**Expanded CCP Implication:** This is a crucial distinction for our architecture. The finding proves that **Skill-calling-Skill code hierarchies are brittle**. This validates our current flat architecture where the Witness Hunter is a single-file procedure. **However, this does NOT invalidate sub-agents.** Sub-agents (where an orchestrator Agent spawns an entirely separate Agent process with its own context window and tools) are fundamentally different from nested code-skills. 
- **What to avoid (Nested Skills):** A [SKILL.md](file:///d:/Work/The%20Conscious%20Coaching%20Factory/lab/SKILL.md) file that programmatically invokes another [SKILL.md](file:///d:/Work/The%20Conscious%20Coaching%20Factory/lab/SKILL.md) as an invisible subroutine.
- **What to embrace (Sub-Agents / Harness Routing):** An orchestrator (like Pi or our Agent Harness) transparently delegating a task to a specialized sub-agent (who uses a flat skill). The hierarchy belongs exclusively in the **orchestrator layer**, while the Skills themselves remain flat, shallow, and highly transparent to the executing agent.

---

## Signal 17 — Skill Creator Quality > Executor Capability

**Source:** SkillCraft, Section 5.3, Figure 7 — Claude-created skills achieve 100% success across all executor models; poorly designed skills INCREASE token cost by 48%.

**Expanded Finding:** In cross-model transfer experiments, researchers took skills authored by one model (e.g., Claude) and had them executed by another (e.g., Gemini, GLM, Minimax). The quality of the original skill author matters far more than the capability of the model executing it. Well-abstracted skills with clear parameter interfaces achieve universal transferability and token savings across the board. In contrast, poorly designed procedures cause confusion, loop failures, and token bloat—regardless of how smart the executing LLM is. The paper states: *"Skill creator quality matters more than executor capability... poorly designed skills can harm performance regardless of which model executes them."*

**Expanded CCP Implication:** This is the ultimate "slow down to speed up" validation. It justifies every minute we have spent rigorously defining the SKILL.md authoring rules, the Talent Paradigm, and reference implementations. A brilliantly authored Skill like our upgraded Witness Hunter forms an enduring asset that will perform beautifully whether run by Claude 3.5 Sonnet, a future GPT-5, or a local open-source model. We must never accept quick, sloppy prompt-dumps masquerading as Skills. Strict quality gates on Skill authoring are not bureaucracy; they are the foundation of scalable agentic performance.

---

## Signal 18 — Skills Generalize Across Difficulty Levels (Cross-Task Transfer)

**Source:** SkillCraft, Table 4 — Skills learned on easy tasks transfer to hard tasks with 95-100% execution success and 19-76% token savings.

**Expanded Finding:** When Skills successfully capture the *reusable procedural structure* of a workflow rather than the instance-specific solution, they transfer seamlessly from simpler to more complex tasks within the same domain. For example, a Skill designed to extract information from 3 documents generalized perfectly when asked to process 5 or 10 documents, because the loop logic was sound. The key requirement is that the Skill must encode the *procedure* (how to do something universally), not the *instance* (what exactly to do for this initial test case).

**Expanded CCP Implication:** Our Skills must be strictly parameterized procedures, entirely divorced from hardcoded content. The Witness Hunter [SKILL.md](file:///d:/Work/The%20Conscious%20Coaching%20Factory/lab/SKILL.md) must be written so that it works identically on a 3-minute TikTok edit transcript and a 3-hour Huberman Lab podcast. The procedural steps (identifying thematic blocks, scoring resonance) remain identical; only the variables (input length, output quantity) change. This dictates how we write the inputs/outputs section of the YAML frontmatter: they must be true variables.

---

## Signal 19 — Stronger Models Benefit More from Skill Reuse (Capability Amplifier)

**Source:** SkillCraft, Section 4, Figure 5 — Correlation r=0.65 between skill execution rate and task success; r=0.53 between baseline success and efficiency savings.

**Expanded Finding:** The paper found a strong positive correlation between a model's baseline intelligence and its ability to squeeze efficiency out of skills. Skill Mode acts as a *capability amplifier*: models that possess the baseline reasoning to synthesize correct skills AND execute them reliably reap massive compound benefits. Closed-source frontier models (Claude 4.5 Sonnet: -71% tokens, GPT-5.2: -79% tokens) benefited far more heavily from Skill reuse than weaker, open-source models, which sometimes struggled to sequence the tools properly even when provided.

**Expanded CCP Implication:** The ROI on our Skill authoring increases as the underlying LLMs get smarter. We are not building scaffolding to compensate for weak models; we are building an operational OS (the Talent Paradigm) that allows frontier models to run at maximum acceleration. This means our investment in high-complexity cognitive skills (like CMF Art Direction or Scene Sequencing) is future-proof. 

---

## Signal 20 — Maturity-Aware Update Gating Prevents Catastrophic Forgetting

**Source:** Evolving PSN, Section 2.4 & Figure 5 — Skills that have proven reliable receive fewer updates; immature skills remain plastic.

**Expanded Finding:** The Programmatic Skill Networks paper introduces a mathematical maturity function. Highly mature skills that have succeeded reliably are protected by a "gating mechanism" that restricts how often they can be modified. Immature, newly generated skills remain highly plastic and subject to frequent rewrites based on feedback. Without this gating mechanism, researchers observed a phenomenon where *"converged skills are repeatedly modified by downstream [edge case] failures, leading to oscillatory behavior"* (i.e., fixing a weird edge case breaks the core functionality that works 99% of the time).

**Expanded CCP Implication:** We are currently at risk of this "oscillatory behavior" if we allow agents to indiscriminately rewrite the Talent Paradigm or core [SKILL.md](file:///d:/Work/The%20Conscious%20Coaching%20Factory/lab/SKILL.md) files every time they encounter a minor anomaly. We must implement a strict maturity classification for our Skills. The Skill Authoring Guide should define formal maturity tiers:
- **Draft:** Highly plastic, iterate constantly.
- **Tested:** Requires explicit justification to change.
- **Stable / Reference (like the Witness Hunter):** Locked. Only structural augmentations allowed, requiring a full regression review to ensure previous workflows aren't broken.

---

## Signal 21 — Structural Refactoring Must Be Online, Not Offline

**Source:** Evolving PSN, Section 4.4 — Offline refactoring of Voyager's 58 skills achieves 0.6875 success rate vs. 0.8462 for PSN's online refactoring.

**Expanded Finding:** Researchers attempted to apply a strong LLM (like Claude Opus 4.5) to analyze and refactor a library of 58 skills in a single "offline" batch, purely by looking at the code. This achieved significantly worse results than continuously "online" refactoring skills as they were actively used. The reason is that offline refactoring lacks empirical execution feedback—an LLM optimizing structure theoretically often inadvertently breaks subtle operational logic that the original author relied on. *"Refactoring is most effective when performed online and tightly coupled with execution feedback."*

**Expanded CCP Implication:** We cannot simply open 20 old CMF or CCF [SKILL.md](file:///d:/Work/The%20Conscious%20Coaching%20Factory/lab/SKILL.md) files and ask the agent to "upgrade them to the Talent Paradigm." Skill improvement must be a live, iterative process driven by real-world usage. The proper upgrade path is: Trigger a real pipeline phase → observe how the old Skill fails or is inefficient → diagnose the root cause from the terminal output → apply the Talent Paradigm upgrade to fix that specific failure mode → verify the fix. Theoretical overhauls without execution context are dangerous.

---

## Signal 22 — 46.3% of the Skills Ecosystem Is Duplicated (Redundancy Tax)

**Source:** Agent Skills (Bosch/CMU), Section 3.2 — Under strict name matching, 46.3% of 40,285 skills share a normalized name with at least one other listing.

**Expanded Finding:** Nearly half of the published Skills ecosystem is composed of redundant duplicates—the exact same underlying intent (e.g., "search weather" or "parse PDF") re-packaged with slightly different wording by different authors. The paper notes: *"Developer effort is often spent re-packaging common workflows rather than expanding coverage into less served tasks."* This extreme redundancy fragments the ecosystem, confuses orchestrators trying to route intent, and makes it impossible for high-quality "canonical" implementations to gain adoption traction. 

**Expanded CCP Implication:** If we are not careful, our own internal CMF/CCF workspace will suffer this exact fate as we scale. We must treat identical intents as single entities. The Skill Authoring Guide must enforce a strict **"one canonical Skill per intent"** policy. Before an agent or human creates a "New Scene Generator" skill, they must definitively prove that the existing Art Director or Blueprint Orchestrator skills cannot handle the parameterization. This is precisely why we added the `similar_to` and `compose_with` JSON/YAML fields to the Witness Hunter—they force authors to explicitly map the Skills ecology and prevent isolated duplication.

---

## Signal 23 — Cognitive Skills Must Be Explicitly Tagged, Not Incidentally Expressed

**Source:** SkillFactory, Section 2.1 & Figure 3 — Explicit `<sample>` and `<reflect>` tags outperform natural-language-embedded cognitive behaviors.

**Expanded Finding:** When researchers tried to teach models to exhibit cognitive behaviors (like retrying a failed step, verifying an output, or pausing to reflect), embedding these instructions organically within natural language prose proved wildly inconsistent. However, when the exact same cognitive demands were explicitly demarcated with rigid structural tags (e.g., `<reflect> ... </reflect>`), the models deployed them much more reliably. This structural scaffolding achieved higher verification F1 scores and generalized significantly better to out-of-domain tasks. The crucial insight is: *"focusing on the structure alone of a skill can be highly effective."*

**Expanded CCP Implication:** Our internal deliberation loops and quality gates within [SKILL.md](file:///d:/Work/The%20Conscious%20Coaching%20Factory/lab/SKILL.md) files must use explicit structural markers. The Draft → Critic → Synthesis pattern we brilliantly added to the Witness Hunter is conceptually correct, but it must be expressed as a highly visible, tagged protocol (e.g., using explicit markdown headers like `### DELIBERATION_LOOP: CRITIC_CHALLENGE` and `### SYNTHESIS`) rather than as flowing paragraphs that the LLM might gloss over. We must force the LLM to output these headers during its thought process to guarantee cognitive adherence.

---

## Signal 24 — SFT Accuracy < Structural Priming for Post-Training Performance

**Source:** SkillFactory, Section 5.1, Table 1 — R1 Distill achieves 11.7% SFT accuracy vs. SkillFactory's 2.8%, but SkillFactory→GRPO (25.1%) overtakes R1 Distill→GRPO (21.2%) after RL.

**Expanded Finding:** In fine-tuning experiments, the traditional belief is that you want the model to solve the task perfectly on the first try (high Supervised Fine-Tuning accuracy). The paper proved this wrong for agentic workflows. *"Stronger SFT task solving does not reliably translate into better post-RL performance."* What matters exponentially more is whether the *structural inductive biases* (the scaffolding of how to approach a problem) are correctly set. Giving the model "silver" traces—which are imperfect outputs that nonetheless follow the correct structural reasoning process (try, fail, reflect, correct)—primes the model to learn and adapt during Reinforced Learning far better than giving it "perfect" one-shot answers from a stronger model.

**Expanded CCP Implication:** We are shifting our perspective on what makes a "good" Skill output. Our [SKILL.md](file:///d:/Work/The%20Conscious%20Coaching%20Factory/lab/SKILL.md) files do not need to produce a flawless, A+ final deliverable in a single, massive API call. What they must do is establish the absolute correct **structural scaffolding**. We want the LLM to follow the right phases, hit the right decision trees, and pass through the right quality gates. A structurally sound Skill that produces an imperfect B+ draft, recognizes the flaw via the Critic module, and synthesizes an A final output is vastly superior to a monolithic prompt trying to guess the A+ answer instantly. The former is a scalable, resilient agentic pattern; the latter is a fragile parlor trick. This finding validates the entire foundation of the Talent Paradigm.

---

## Signal Map Summary

| # | Signal | Source Paper | Key Implication |
|---|--------|-------------|-----------------|
| 15 | Code compositions cut tokens 80% | SkillCraft | Extract deterministic computations (math, sorting) to `scripts/` |
| 16 | Deep nesting hurts performance | SkillCraft | Keep code Skills flat; push hierarchy upwards to Sub-Agent Orchestrators |
| 17 | Creator quality > executor capability | SkillCraft | Rigorous Skill authoring standards are the highest ROI investment |
| 18 | Skills transfer across difficulty | SkillCraft | Parameterize strictly—encode the universal procedure, not the instance |
| 19 | Stronger models benefit more | SkillCraft | Skill investment compounds; OS-level scaffolding accelerates frontier models |
| 20 | Maturity gating prevents forgetting | PSN | Define Skill maturity tiers (Draft→Tested→Stable) to prevent oscillatory rewrites |
| 21 | Online refactoring > offline | PSN | Upgrade legacy skills via live execution feedback, not theoretical batches |
| 22 | 46% ecosystem is duplicated | Agent Skills | Enforce strict "one canonical Skill per intent" mapping via YAML ecology fields |
| 23 | Explicit tags > incidental expression | SkillFactory | Force cognitive behaviors (Reflection/Critic) into explicit markdown structural tags |
| 24 | Structure > accuracy for priming | SkillFactory | Value structural deliberation (Try→Critique→Fix) over monolithic perfect-first-shot prompts |
