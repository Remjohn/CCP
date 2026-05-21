# **SkillClaw: Let Skills Evolve Collectively** **with Agentic Evolver**

**Ziyu** **Ma** [1] _[∗]_, **Shidong** **Yang** [1] _[∗]_, **Yuxiang** **Ji** [1] _[∗]_, **Xucong** **Wang** [1] _[∗]_, **Yong** **Wang** [1] _[†]_, **Yiming** **Hu** [1],
**Tongwen** **Huang** [1], **Xiangxiang** **Chu** [1]


1DreamX Team, _∗_ Equal contribution, _†_ Project lead


Large language model (LLM) agents such as OpenClaw rely on reusable skills to perform complex
tasks, yet these skills remain largely static after deployment. As a result, similar workflows, tool usage
patterns, and failure modes are repeatedly rediscovered across users, preventing the system from
improving with experience. While interactions from different users provide complementary signals
about when a skill works or fails, existing systems lack a mechanism to convert such heterogeneous
experiences into reliable skill updates. To address these issues, we present SkillClaw, a framework
for collective skill evolution in multi-user agent ecosystems, which treats cross-user and over-time
interactions as the primary signal for improving skills. SkillClaw continuously aggregates trajectories
generated during use and processes them with an autonomous evolver, which identifies recurring
behavioral patterns and translates them into updates to the skill set by refining existing skills or
extending them with new capabilities. The resulting skills are maintained in a shared repository and
synchronized across users, allowing improvements discovered in one context to propagate system-wide
while requiring no additional effort from users. By integrating multi-user experience into ongoing skill
updates, SkillClaw enables cross-user knowledge transfer and cumulative capability improvement, and
experiments on WildClawBench show that limited interaction and feedback, it significantly improves
the performance of Qwen3-Max in real-world agent scenarios.


**Github:** `[https://github.com/AMAP-ML/SkillClaw](https://github.com/AMAP-ML/SkillClaw)`

### **1 Introduction**


Large language model (LLM) agents (Yao et al., 2022; Shinn et al., 2023) have rapidly made personal AI
assistants practical in real-world settings, with systems such as OpenClaw enabling users to complete complex
tasks through natural conversation. A user can now ask an agent to configure a service, debug an API call,
or automate a multi-step workflow, relying on it to coordinate tool usage and intermediate reasoning. These
capabilities are largely driven by skills, which encode structured procedures for interacting with tools and
solving tasks. In current deployments, users typically select and install skills from a centralized skill hub
to meet their needs, and these skills serve as the primary building blocks for agent behavior. However, the
skill ecosystem remains largely static (Zhang et al., 2025b; Naihin et al., 2023; Song et al., 2026), as skills
are manually installed and maintained and solutions discovered during interaction rarely persist beyond
individual sessions.


This limitation becomes evident in everyday usage. For example, users often ask agents to complete multi-step
tasks such as automating data processing workflows, where failures frequently arise from subtle issues such
as incorrect argument formats or mismatched tool calls. Through several rounds of trial and error, an agent
may eventually arrive at a working solution or even a more stable procedure. However, these improvements
remain confined to the current session and are not consolidated into the skill set or carried forward to future
interactions. As similar tasks recur across different users and over time, the same patterns of failure and
recovery are repeatedly observed, yet the system does not improve its behavior. This is fundamentally
problematic because users operate in overlapping task spaces where similar workflows, tools, and failure
modes are shared, but the system fails to leverage these recurring experiences. Consequently, each user is
forced to rediscover solutions independently, preventing knowledge from accumulating at the system level.
Therefore, the key challenge is not only to improve performance within a single session, but also to enable


1
_Work_ _in_ _Progress_


**Figure 1** **Overview of SkillClaw.** SkillClaw enables collective skill evolution in a multi-user agent ecosystem through a
closed-loop pipeline. Independent agents interact with their environments and produce structured session trajectories
that preserve full action–feedback causal chains. These trajectories are aggregated across users and grouped by
referenced skills, forming a shared evidence base that exposes consistent success patterns and recurring failure modes.
An agentic evolver analyzes each skill-specific group and performs evidence-driven updates via refinement or creation,
while preserving validated behaviors from successful executions. The updated skill repository is then synchronized
back to all agents, allowing improvements discovered in one user’s interaction to benefit others and continuously
accumulate over time.


knowledge to accumulate and evolve across users.


Existing approaches to agent adaptation fail to support the accumulation and evolution of skills across users
and over time. Memory-based methods store past trajectories for retrieval (Shinn et al., 2023; Zhao et al.,
2024; Fang et al., 2025a; Tang et al., 2025; Ouyang et al., 2025a; Chhikara et al., 2025; Liu et al., 2026), but
such records remain tied to specific instances and are difficult to generalize into improved behavior. Skill-based
methods compress experience into structured instructions (Xia et al., 2026a; Zhang et al., 2025a, 2026b; Wu
et al., 2025; Zhang et al., 2026a), yet treat the resulting skill library as a static resource that does not evolve
through usage. While local refinement can improve individual agent instances, these improvements remain
isolated and do not accumulate across users, leading to fragmented skills rather than collective improvement
over time. What is missing is a mechanism that turns ordinary interactions into continuous skill evolution
and enables skills to improve collectively across users.


Building on this insight, we propose **SkillClaw**, a framework for skill collective evolution in multi-user
OpenClaw-style agent ecosystems (Fig 1). SkillClaw adopts a centralized evolution architecture, where
agents deployed across different users continuously generate interaction sessions during everyday usage. These
trajectories are aggregated across users and over time as evidence of real-world task execution and are processed by a centralized evolution engine to drive skill updates. Given accumulated interaction trajectories,
the evolver analyzes both successful and failed executions, identifies recurring issues and effective procedures,
and updates the shared skill set by refining existing skills, creating new ones, or adjusting their descriptions.
Unlike predefined pipelines, this evolution process is driven by an autonomous agent that performs openended reasoning over interaction evidence and directly edits skill definitions. The updated skills are then
synchronized across agents, allowing improvements discovered in one context to propagate to future interactions across users and over time. This forms a continuous evolution loop in which interaction data drives
skill updates, and updated skills improve subsequent interactions. From the user’s perspective, this process


2


requires no additional effort, as data collection, evolution, and synchronization all occur automatically in the
background.


This design introduces three key properties that distinguish SkillClaw from existing systems. First, SkillClaw enables _collective_ _evolution_, where knowledge from individual interactions contributes to a shared and
continuously improving skill ecosystem. Second, it is _fully_ _automatic_, with skill evolution driven by runtime
interaction without manual curation or explicit user intervention. Third, it adopts an _agentic_ _evolution_
_paradigm_, where skill updates are produced through open-ended reasoning rather than predefined update
rules, enabling flexible and context-aware improvements.


SkillClaw is designed as a general framework that is compatible with a wide range of Claw-style agent
systems, including OpenClaw as well as variants such as CoPaw, IronClaw, PicoClaw, ZeroClaw, NanoClaw,
and NemoClaw. We evaluate SkillClaw on WildClawBench using `qwen3-max` as the backbone model and
simulate a multi-user deployment setting. Experimental results demonstrate that SkillClaw yields substantial
improvements across tasks, highlighting the effectiveness of multi-user driven collective evolution for building
continuously improving agent systems in real-world environments.

### **2 Method**


We present **SkillClaw**, a framework for collective skill evolution in a multi-user agent ecosystem (Fig 1).
In our setting, different users independently interact with their own deployed OpenClaw agents, potentially
across different devices, environments, and time. Although these interactions are isolated at runtime, they
share a common behavioral space: similar workflows, overlapping tool usage, and recurring failure modes
appear across users. SkillClaw builds on the observation that _different_ _users_ _exercising_ _the_ _same_ _skill_ _under_
_diverse contexts produce complementary views of that skill’s behavioral boundary_, revealing both the conditions
under which it works and those under which it breaks. A single user rarely generates enough signal to
separate a generalizable improvement from an idiosyncratic fix. Aggregating evidence across users provides
the grounding that makes stable skill evolution possible.


Formally, let _S_ = _{s_ 1 _, . . ., sM_ _}_ denote a shared skill set, where each skill is a reusable procedural artifact.
Each user interaction produces a session trajectory _τ_, which records the full interaction loop: the prompt,
the agent’s actions, feedback from the environment or the user, and the final agent response. Given a set of
trajectories _T_ = _{τi}_ collected across users, our goal is to update the shared skill set:


_S_ _[′]_ = Φ( _S, T_ ) _,_


such that improvements discovered in one interaction can benefit future users.


**2.1** **From** **Isolated** **Sessions** **to** **Shared** **Evidence**


Multi-user skill evolution requires converting a stream of isolated, heterogeneous interaction sessions into
a form that supports cross-user reasoning. SkillClaw does this in two stages: it first structures individual
sessions to preserve causal information, then aggregates them into a shared evidence base.


At the system level, SkillClaw connects independently deployed agents through a common skill repository.
Each agent has access to the current skill set and produces interaction sessions during normal usage. These
sessions are recorded and uploaded as shared evidence. A centralized evolution engine periodically processes
the collected sessions, updates the skill repository, and synchronizes the updated skills back to all agents,
forming a closed loop:


Multi-user Interaction _→_ Session Collection _→_ Skill Evolution _→_ Skill Synchronization _._


At inference time, the agent receives a catalogue of available skills in its prompt and can dynamically select
and load those relevant to the current task. Users do not interact directly, and no coordination among agents
is required. Collective improvement arises entirely from shared skill evolution.


Within this loop, each interaction session contains more than plain dialogue. SkillClaw records the full causal
chain: the user prompt, the agent’s actions (including tool calls), intermediate feedback (tool results, errors,


3


**Algorithm** **1** Agentic Collective Skill Evolution


**Require:** Skill repository _S_, user sessions _T_
**Ensure:** Updated repository _S_ _[′]_

1: Convert _T_ into structured evidence _E_
2: Group _E_ by referenced skills to obtain _{G_ ( _s_ ) _}_ and _G_ (∅)
3: _S_ _[′]_ _←S_
4: **for** **all** group _G_ ( _s_ ) **do**
5: Use the agentic evolver to analyze recurring success and failure patterns

6: Select an evolution action from { `refine`, `create`, `skip` }
7: Generate a candidate skill update if the evidence supports modification
8: Apply conservative editing and validation
9: Merge approved updates into _S_ _[′]_

10: **end** **for**
11: Analyze _G_ (∅) for missing but reusable procedures

12: Add validated new skills into _S_ _[′]_

13: Synchronize _S_ _[′]_ back to all agents
14: **return** _S_ _[′]_


and explicit user responses), and the final agent response. We record all of this because most skill-level
failures are _procedural_ . An incorrect argument format, a missing validation step, or a misordered tool call can
cause a task to fail, yet none of these problems appears in the final response. They can only be diagnosed
from the intermediate action-feedback trace. Each raw session is converted into a structured representation
that preserves this chain:


prompt _→_ action _→_ feedback _→· · · →_ agent response _._


We also extract lightweight metadata from each session: (i) which skills were referenced, (ii) whether tool
errors occurred, and (iii) a coarse quality estimate. These signals help organize sessions but do not impose
rigid labels.


Once sessions are structured, they are grouped by the skills they reference to enable cross-user reasoning.
For each skill _s_, we collect all sessions that invoked _s_ :


_G_ ( _s_ ) = _{τi_ _| s ∈Ki},_


and place sessions that did not use any skill into a separate group _G_ (∅). This grouping does more than
organize the data. When multiple sessions invoke the same skill but produce different outcomes across
different users, tasks, or environments, the comparison directly reveals where the skill works and where
it fails, with the skill itself as the controlled factor. This amounts to a _natural_ _ablation_ and enables two
operations that would be unreliable from single-user data alone: (1) evaluating how an existing skill actually
performs under diverse real-world usage, and (2) identifying recurring procedures that no existing skill covers,
surfaced by patterns in _G_ (∅).


**2.2** **Agentic** **Skill** **Evolution**


The core of SkillClaw is an _agentic evolver_ that updates the shared skill repository with open-ended reasoning.
SkillClaw instantiate an _agentic_ _evolver_, an LLM agent equipped with a structured harness that supplies the
grouped session evidence, the current skill definitions, and a set of permitted evolution actions. The harness
provides structured inputs but does not constrain the evolver’s reasoning. The evolver diagnoses root causes
from sessions of varying context lengths and skills of different formats, and decides how to act. This separation
between a fixed harness and open-ended reasoning allows SkillClaw to handle diverse failure modes without
hand-crafted rules for each type.


Concretely, given a skill _s_ and its associated session group _G_ ( _s_ ), the evolver examines both successful and
failed executions and selects one of three actions:


4


 - **Refine.** Update the skill to correct identified errors or improve robustness based on observed failure
patterns.


 - **Create.** Introduce a new skill when _G_ ( _s_ ) reveals recurring sub-procedures that are not captured by any
existing skill.


 - **Skip.** Leave the skill unchanged when the available evidence is insufficient to justify a modification.


For sessions in _G_ (∅), i.e., those that did not invoke any skill, the evolver focuses on discovering missing
but reusable procedures. New skills are created only when the observed patterns are specific enough to be
teachable and likely to recur.


Regardless of which action is chosen, the evolver always reasons over successful and failed sessions _jointly_ .
Successful sessions define the _invariants_ of a skill, the parts that work and must not be altered. Failed
sessions define the _targets_, the specific behaviors that need correction. This joint view is what prevents a
naive failure: fixing one problem while inadvertently breaking a previously effective procedure. Each update
corrects identified deficiencies while preserving what successful sessions have validated, making evolution
cumulative. The complete procedure is given in Algorithm 1.


**2.3** **Skill** **Synchronization** **and** **the** **Evolution** **Loop**


After evolution, candidate skill updates are validated before being written back to the shared repository.
Validation is performed during the nighttime and executed in available idle user environments, ensuring
that evaluation reflects real deployment conditions. For a skill _s_ and its candidate update _s_ _[′]_, the system
selects relevant tasks from the interaction data collected during the day. Both versions are executed under
the same environment using the full toolchain, including multi-step interactions and intermediate feedback.
After execution, the system uses the model to compare the outcomes produced by _s_ and _s_ _[′]_ . The decision is
based on overall task success and execution stability. If the updated skill demonstrates better performance,
it is marked as `Accept` ; otherwise, it is marked as `Reject` . Accepted updates are merged into the shared
repository and synchronized to all agents for the next day. Rejected updates are retained only as candidates
and are not deployed. As a result, users always interact with the best validated skill pool from the previous
night, rather than unverified updates. This validation step induces a monotonic deployment behavior. Since
only improvements are accepted, the deployed skill pool does not degrade over time. Combined with the
evolution process, the system forms a closed loop:


Interaction _→_ Evidence _→_ Evolution _→_ Validation _→_ Deployment _._


where updated skills shape future interactions and generate new evidence for the next round of evolution.


Three properties follow from this design. First, _collective_ _evolution_ . Sessions are aggregated across users,
and knowledge discovered in one interaction is propagated to a shared skill ecosystem that benefits all users.
Second, _full_ _automation_ . The entire pipeline, from session recording to skill synchronization, runs without
manual curation or explicit user intervention. The only human input is normal agent usage. Third, _agentic_
_adaptability_ . Skill updates are produced through open-ended reasoning rather than predefined rules, enabling
the system to handle previously unseen failure modes and usage patterns.


From the user’s perspective, none of this is visible. Users interact with their agents as usual, while skill
evolution happens in the background. Over time, isolated user experiences are consolidated into a shared
skill set that improves with continued use.

### **3 Experiments**


**3.1** **Benchmark:** **WildClawBench**


We evaluate SkillClaw on **WildClawBench** (Ding et al. (2026)), a real-world agent benchmark consisting of
60 complex tasks across six capability domains. As summarized in Table 1, the benchmark covers diverse
scenarios including productivity workflows, code execution, social interaction, retrieval, creative generation,


5


**Table 1** Task categories in WildClawBench. The benchmark spans six domains covering a wide spectrum of real-world
agent scenarios, from procedural workflows to multimodal generation and safety-critical decision making.


**Category** **Example** **Tasks** **Challenges**


Productivity Flow arXiv classification, scheduling, SCP multi-step pipelines
Code Intelligence debugging, puzzle solving execution correctness
Social Interaction negotiation, chat analysis multi-turn reasoning
Search & Retrieval academic search, conflict resolution API usage
Creative Synthesis video notes, poster generation multimodal generation
Safety & Alignment prompt injection, leakage detection constraint satisfaction


**Table** **2** Key properties of WildClawBench, highlighting its realistic execution environment, multimodal inputs, and
long-horizon, failure-sensitive evaluation setting.


**Property** **Description**


Execution Environment Full Linux container with tools
Multimodality Text, code, image, video
Evaluation 3–27 metrics aggregated
Hard Constraints Critical errors _→_ zero score
Task Length 15–50 steps
External Dependency APIs and model downloads


and safety alignment. Unlike prior benchmarks, WildClawBench requires full end-to-end execution in realistic environments with multimodal tool usage. Table 2 highlights its key properties, including fine-grained
evaluation metrics and hard constraints that enforce strict correctness.


**3.2** **Experimental** **Setup**


We simulate a realistic deployment scenario using a continuous day–night skill evolution process. The experiment runs for 6 days (6 rounds), where each day consists of two phases: a daytime online interaction
phase and a nighttime skill evolution and validation phase. During the daytime, users interact with deployed
OpenClaw agents to complete tasks in WildClawBench. These interactions generate session trajectories that
capture failure modes, edge cases, and recurring bottlenecks encountered during execution. During the nighttime, the system processes the collected interaction data to generate candidate skill updates targeting these
observed deficiencies. A validator then filters candidate updates, and only approved skills are added to the
shared deployment pool for the next day. This process forms a closed loop: users operate with the current
best skill pool during the day, while the system absorbs feedback and produces updated skills at night, which
are then redeployed for subsequent interactions. Our setup involves 8 concurrent users, each interacting
with the system under WildClawBench tasks based on their individual goals and task requirements. All
execution, skill evolution, and validation processes are powered by Qwen3-Max. At the system level, we
maintain a shared current best skill pool. Day 1 starts with an initial skill set corresponding to the baseline.
In subsequent rounds, only skills that are triggered during interaction and exhibit potential for improvement
are considered for candidate updates. Results are reported on four representative categories, with additional
categories to be included in the future version.


_Validation_ _Mechanism._ The validation mechanism is a critical component of our experimental design. During the nighttime phase, the system first identifies candidate skill updates based on interaction logs accumulated during the day. These candidate updates are then deployed to available user environments and
evaluated under real execution conditions. The validator follows a simple decision rule. If a candidate skill
outperforms the currently deployed best skill on the corresponding validation tasks, it is marked as `Accept` ;
otherwise, it is marked as `Reject` . Accepted skills are merged into the current best skill pool and deployed
to all users on the following day. Rejected skills are retained only as candidate records and are not deployed.
As a result, users always interact with the best validated skill pool from the previous night, rather than
unverified updates. This validation strategy introduces additional token cost, as candidate skills must be


6


executed in real environments with full tool interaction. However, compared to direct deployment without
validation, this overhead leads to significantly more stable user-facing performance.


**Table** **3** User-side daytime results (best-skill deployment view). Day 1 is the baseline experience; Day 2–6 reflect the
best skill pool carried forward after each nightly validator decision. Absolute and relative gains are computed w.r.t.
Day 1.


Category Day 1 Day 2 Day 3 Day 4 Day 5 Day 6 Abs. Gain Rel. Gain


Social Interaction 54.01% **60.34%** 60.34% 60.34% 60.34% 60.34% +6.33 +11.72%


Search & Retrieval 22.73% 30.00% 30.00% **34.55%** 34.55% 34.55% +11.82 +52.00%


Creative Synthesis 11.57% **21.80%** 21.80% 21.80% 21.80% 21.80% +10.23 +88.41%


Safety & Alignment 24.00% 24.00% 24.00% 24.00% **32.00%** 32.00% +8.00 +33.33%


**3.3** **Main** **Results**


As shown in Table 3, all four categories exhibit a consistent evolution pattern over 6 days. The system first
resolves primary bottlenecks, then stabilizes deployment around the current best skill pool. The trajectory
is not characterized by daily fluctuations, but by progressively consolidating locally effective updates into a
stable skill set deployed to users.


Social Interaction improves earliest and most sharply. Performance increases from 54.01% to 60.34% on
Day 2 and remains stable thereafter. This indicates the presence of a high-impact workflow bottleneck with
broad coverage. Once the corresponding skill is improved, the system quickly gains capability in cross-source
integration, task organization, and high-level summarization. Although additional skill updates are proposed
in later rounds, Day 2 already establishes the current best skill pool for this category, leading to consistently
strong user-side performance.


Search & Retrieval follows a more staged improvement trajectory, increasing from 22.73% to 30.00%, and
then further to 34.55%. Unlike Social Interaction, the gains are not driven by a single skill update but by
a sequence of improvements. The system first resolves input validation and file accessibility, then builds
toward constraint-aware retrieval planning. This reflects a key property of retrieval tasks, where higher-level
reasoning becomes effective only after lower-level reliability is ensured.


Creative Synthesis shows a large early jump from 11.57% to 21.80% on Day 2 and then plateaus. This
suggests that the primary bottleneck lies not in content generation itself, but in environment setup, including
file handling, working directory configuration, and multimodal pipelines. Once these foundational issues are
resolved, user-facing performance improves rapidly. More complex multimodal skills continue to emerge and
pass validation, but within the 6-day window, they do not surpass the early-established best skill pool.


Safety & Alignment improves later, from 24.00% to 32.00%. Improvements in this category primarily target
execution reliability in real-world environments rather than surface-level task performance. Effective updates
focus on mechanisms such as Git fallback, directory cloning protocols, and safe execution in non-interactive
settings. These changes may not immediately yield higher scores but, once validated, are retained in the
deployment pool and contribute to long-term system robustness.


From a deployment perspective, Table 3 reflects not a sequence of independent experiments, but a continuously running system that consolidates nightly verified updates into a unified skill pool for daytime usage. It
is important to note that this study represents a small-scale test of collective skill evolution, with limited user
queries, feedback signals, and interaction depth. Despite these constraints, SkillClaw still achieves consistent
performance gains, demonstrating its effectiveness in realistic interaction settings. Scaling up the number of
users, extending the time horizon, and introducing more diverse tasks and validation conditions are likely to
further enrich the evolution trajectory and further improve system performance.


7


**Table** **4** Social Interaction: nightly skill evolution and validator decisions. The only skill update that entered the
deployed best pool was `03_task6` (accepted after Night 1).


**Day** **Candidate** **Skill** **Skill** **Function** **Change** **Summary** **Validator** **Next-Day** **Action**



1 `03_task6`



Cross-dept Slack
summarization, data
reconciliation, risk
identification, board-level
brief drafting



Rewrote workflow into strictly-ordered
steps; strengthened project keyword
filtering, finance priority, change detection,
COO contact confirmation



Day 2: upgrade to
Accept
new best pool



Continued using current Day 3: keep Day 2
2 (none) Same-pool retest; no new skill text landed Reject
Social best pool best pool



Gmail + Calendar
3 `03_task1`
meeting coordination



Extended workflow with meeting-param
extraction, multi-participant availability
check, confirmation loop, reschedule on
rejection



Not admitted; Day 4
Reject keeps current best
pool



Continued using current Day 5: keep current
4 (none) Same-pool retest; no new skill text landed Reject
Social best pool best pool


Continued using current Day 6: keep current
5 (none) Same-pool retest; no new skill text landed Reject
Social best pool best pool


Added fallback & grounding constraints;
Not admitted to next
6 `03_task3` Slack feasibility analysis analysis must rely on real API results or Reject
cycle
user-provided context


**3.4** **Analysis**


As shown in Table 4–Table 7, skill evolution is highly heterogeneous across categories, following distinct
capability trajectories rather than a uniform pattern.


In Social Interaction, evolution primarily improves workflow explicitness and execution reliability. The category already starts with relatively complete task-oriented skills, including meeting coordination, Slack task
extraction, feasibility analysis, status reporting, support triage, and executive summarization. The limitation is therefore not missing capabilities, but insufficient executability. The most impactful update comes
from executive-level summarization, which spans message retrieval, information filtering, data verification,
risk extraction, and structured output. Once this skill is rewritten from a descriptive instruction into an
explicit procedural workflow, performance improves sharply. Subsequent updates to meeting coordination
and feasibility analysis mainly refine and strengthen this existing structure.


Search & Retrieval exhibits a staged evolution pattern. Early updates focus on file existence checks, path resolution, and multimodal input validation, indicating that initial failures stem from unreliable input handling
rather than high-level reasoning. As these issues are resolved, evolution shifts toward higher-level capabilities such as constraint-aware retrieval planning and missing input recovery. This _input-first,_ _strategy-later_
progression aligns with real-world retrieval systems and explains why improvements emerge incrementally
through multiple skill updates rather than a single change.


In Creative Synthesis, evolution centers on organizing multimodal processing pipelines. Early gains come
from establishing reliable execution environments, including working directory validation, input checking,
and media preprocessing. This suggests that the primary bottleneck lies in entering a correct execution
flow rather than generating creative content. Later updates extend toward higher-level multimodal pipelines,
such as PDF-to-poster generation, video summarization, and image-based synthesis. These updates indicate
a transition from _getting_ _tasks_ _to_ _run_ to _running_ _tasks_ _professionally_ . However, the early-established best
skill pool already provides strong performance, and later improvements do not yet surpass this level within
the 6-day window.


Safety & Alignment follows a reliability-driven evolution path. Updates in this category focus on robust
execution under real-world constraints rather than expanding task capabilities. Typical improvements include
fallback strategies for Git authentication failures and correct directory cloning procedures. These skills do
not primarily increase apparent intelligence but reduce failure rates under edge conditions. Once validated,
they are retained in the deployment pool and form the foundation of system stability.


Overall, Table 4–Table 7 show that skill evolution is not a simple accumulation of rules, but a structured


8


**Table** **5** Search & Retrieval: nightly skill evolution and validator decisions. Key accepted updates:
`validate-file-existence` (Night 1) and best-so-far confirmation (Night 3).


**Day** **Candidate** **Skill** **Skill** **Function** **Change** **Summary** **Validator** **Next-Day** **Action**



1 `validate-file-` Pre-processing file
`existence` existence check



Before any file parsing / image reading /
Day 2: upgrade to
multimodal call, first confirm the input file Accept
new best pool
actually exists



2 `debug-missing-` Missing-file path List parent directory, verify naming, Reject Day 3: keep Day 2
`file-path` debugging correct path instead of halting on “missing” best pool



Continued using current
3 (none)
Search best pool


`robust-file-validation-` Stronger multimodal
4 `before-multimodal` pre-validation


`constrained-technical-` Budget-constrained
5 `search-planning` technical / academic
search planning


6 `recover-missing-` Recover / locate real
`input-file` input file from workspace



Same-pool retest; nightly readout was
Day 4: continue same
stronger, confirming current pool as Accept
best pool
best-so-far


Upgraded from “exists?” to “exists +
Day 5: keep current
parent-dir search + hard pre-multimodal Reject
best pool
validation”


Added feasibility check, sub-question
Day 6: keep current
decomposition, official-source priority, Reject
best pool
evidence-chain output


When benchmark’s expected path fails,
Not admitted to next
proactively search the working directory for Reject
cycle
the actual input file



process driven by category-specific bottlenecks. Social Interaction emphasizes workflow executability, Search
& Retrieval emphasizes input reliability and planning, Creative Synthesis emphasizes multimodal pipeline
organization, and Safety & Alignment emphasizes robust and recoverable execution in real-world environments.


_Controlled_ _validation_ _of_ _skill_ _evolution._ Table 8 provides a controlled validation of the evolution mechanism
using three custom queries: basic extraction, deadline parsing, and save report. Unlike the full benchmark,
these queries are designed to isolate common failure modes observed in the main results, allowing us to
examine whether skill evolution can directly resolve them. We observe a consistent improvement after a
single round of evolution, with an average gain of +42.1%. In particular, _save_ _report_ improves from 28.3% to
100.0%, where the initial failure is caused by missing environment-specific procedures (e.g., output path or
format), which can be fully corrected once encoded as a reusable skill. Similarly, _basic extraction_ shows a large
gain (+47.8%), indicating that recurring execution patterns can be effectively captured through evolution.
In contrast, _deadline_ _parsing_ exhibits a smaller improvement (+6.9%), suggesting that tasks relying more on
nuanced reasoning are less sensitive to procedural skill updates. Overall, these controlled results complement
the main benchmark findings by showing that skill evolution is particularly effective when failures arise
from missing or incorrect procedural knowledge, providing a direct mechanism-level explanation for the gains
observed in earlier experiments.


**3.5** **Case** **Study**


Figure 2 illustrates how skill evolution improves task execution on a Slack message analysis task. The original
agent follows a naive workflow that retrieves all messages and processes them uniformly, while also relying
on trial-and-error to handle tool failures (e.g., incorrect API port configuration). As a result, execution is
both inefficient and error-prone. In contrast, the evolved skill introduces a structured and reliable workflow.
It first scans message previews to identify task-relevant candidates, then selectively retrieves full message
content when necessary, and finally extracts actionable items. At the same time, previously observed tool
failures are corrected by encoding the proper API configuration directly into the skill. This transformation
reflects three key improvements: (1) **task** **decomposition**, where the problem is divided into filtering and
extraction stages; (2) **error** **correction**, where tool-level failures are resolved proactively rather than through
reactive retries; and (3) **selective** **retrieval**, which focuses computation on relevant messages and improves
extraction quality. Overall, this example demonstrates that skill evolution not only fixes execution errors but
also restructures the interaction pipeline into a more efficient and reliable strategy.


9


**Table** **6** Creative Synthesis: nightly skill evolution and validator decisions. The only accepted skill was
`validate-tmp-workspace-inputs` (Night 1).


**Day** **Candidate** **Skill** **Skill** **Function** **Change** **Summary** **Validator** **Next-Day** **Action**



Before creative tasks, verify
Day 2: upgrade to
`/tmp_workspace` inputs, directories, and Accept
new best pool
symlinks are correct


Check video / image / PDF / audio files
Day 3: keep current
exist, are readable, and format-correct; Reject
best pool
prepare output directories


New unified pipeline: extract content from
Day 4: keep current
PDF / video / image and generate posters, Reject
best pool
webpages, slides, etc.


Added image classification, visual
Day 5: keep current
generation, garment synthesis, structured Reject
best pool
output validation


Pipeline added audio/video fallback &
Day 6: keep current
halt on missing input; new skill forces Reject
best pool
per-file validation for all named inputs


Extended PDF-to-poster /
Not admitted to next
document-to-visual paths; did not yield Reject
cycle
better deployment results



1 `validate-tmp-`
```
  workspace-inputs

```

2 `multimodal-input-`
```
  validation-and-setup

```


Check `/tmp_workspace`
inputs & environment
setup


Multimodal input
validation & output
env init



3 `multimodal-creative-` Multimodal creative
`task-pipeline` pipeline


4 `multimodal-creative-` Multimodal creative
`task-pipeline` (impr.) pipeline


```
  multimodal-creative```

5 `task-pipeline` (impr.);
```
  validate-required  input-files

```


Creative pipeline +
per-file fail-fast
validation



6 `multimodal-creative-` Multimodal creative
`task-pipeline` (cand.) pipeline



**Table** **7** Safety & Alignment: nightly skill evolution and validator decisions. Skills were accepted on Nights 1–4;
candidate improvements on Nights 5–6 were rejected.


**Day** **Candidate** **Skill** **Skill** **Function** **Change** **Summary** **Validator** **Next-Day** **Action**



1 `git-push-with-` Patch / bundle fallback
`auth-fallback` on git push failure



In no-credential / auth-failure scenarios,
Day 2: add to Safety
provide safe fallback instead of blocking on Accept
best pool
push



Unified patch / bundle filenames and
2 `git-push-with-` Git auth-failure fallback verification; reduced filename inconsistency Accept Day 3: keep updated
`auth-fallback` during fallback best pool


```
  git-push-with```

3 `auth-fallback` ;
```
  git-clone-to  directory

```


Push fallback + correct
clone-to-dir



Push: added auth-alternative paths &
Day 4: keep current
secrets audit; Clone: fixed `mkdir` `&&` `cd` `&&` Accept
best pool
`git` `clone` subshell pitfalls


Same-pool retest; validator read a higher
Day 5: continue same
result, confirming current pool as Accept
best pool
best-so-far



Continued using current
4 (none)
Safety best pool



Added “push hang treated as auth failure”
5 `git-push-with-` Git auth-failure fallback and other non-interactive environment Reject Day 6: keep current
`auth-fallback` details; no improvement best pool


Added identity config & filename
6 `git-push-with-` Git auth-failure fallback consistency requirements; did not exceed Reject Not admitted to next
`auth-fallback` current best validation result cycle


**Table** **8** Controlled validation results (Skill Evolve Lite) on three custom queries (basic extraction, deadline parsing,
and save report).


Query Baseline (%) Post-Evolve (%) Gain


basic extraction 21.7% **69.6%** +47.8%
deadline parsing 41.1% **48.0%** +6.9%
save report 28.3% **100.0%** +71.7%


Average 30.4% **72.5%** +42.1%


10


TASK : I‘ve been swamped lately and I think I’m dropping the ball on things. Can you go through my recent messages and pull out
everything I need to actually do? I want to make sure nothing’s slipping through the cracks — deadlines, requests, whatever people are
waiting on me for.



















**Figure 2** Case study on Slack message analysis. The original agent follows a naive workflow that retrieves all messages
and handles tool errors via trial-and-error, leading to inefficient and unstable execution. The evolved skill introduces
a structured pipeline that first filters task-relevant messages using previews, then selectively retrieves full content,
while correcting tool configuration errors (e.g., API port). This results in more efficient, reliable, and accurate task
completion.


TASK : Help me compile the Oral papers accepted at ICCV 2025, and determine how many of them have SJTU (Shanghai Jiao Tong University) as
the first affiliation and how many have FDU (Fudan University) as the first affiliation. Please provide both the counts and the
corresponding list of papers. - Save the results into `/tmp_workspace/results/results.md`.













**Figure** **3** Case study on ICCV 2025 oral paper analysis. The original agent relies on heuristic matching of university
names, leading to incorrect counting of non-first affiliations. The evolved skill introduces a stricter definition of _first_
_affiliation_ based on official PDF first pages, aligns papers with OpenAccess records, and performs targeted re-checks
on ambiguous cases. This results in more accurate and reliable counting under noisy document conditions.


11


TASK : 你是一名AI 编程专家。在/tmp_workspace 目录下有一个SAM3（Segment Anything Model 3）的完整代码库，但没有任何文档、README 或示例Notebook。你需要通过阅读源
代码，理解SAM3的使用方法，然后编写推理脚本完成以下4 个目标检测用例。请编写一个Python 推理脚本，在测试图像上运行以下4 个用例，并将结果保存到
/tmp_workspace/results/predictions.json…











**Figure** **4** Case study on SAM3 inference under incomplete execution environments. The original agent assumes that
required files and execution conditions are fully available, leading to failures when paths are missing or environment
assumptions (e.g., CUDA support) are violated. The evolved skill introduces an environment-aware workflow that
performs workspace inspection, treats missing paths as non-blocking, searches for nearby task-specific assets, and
adapts execution to system constraints. This results in more robust and reliable task execution under imperfect
conditions.


TASK : 我想购买一部手机，请根据以下条件找出最符合的型号：手机条件：1.品牌来自中国厂商；2.使用骁龙8Gen3；3.主摄1英寸传感器；4.支持卫星通信；5.发布时间2024；6.内存
512 GB；7. 电池5400mAh以上；请给出1.给我推荐符合以上要求的手机；2. 结果保存为.md文件，保存到/tmp_workspace/results/results.md

















**Figure** **5** Case study on multi-criteria product selection. The original agent relies on heuristic matching and may
stop early after finding a seemingly plausible candidate, leading to incorrect conclusions under strict constraints. The
evolved skill introduces a structured constraint-aware workflow that verifies each requirement against authoritative
sources and evaluates candidates jointly across all conditions. When no candidate fully satisfies all constraints, it
reports this explicitly and provides a breakdown of partial matches, resulting in more reliable and calibrated decisions.


12


Figure 3 further demonstrates how skill evolution improves decision correctness in a document analysis task.
The original agent relies on weak heuristics, such as matching the presence of university names in affiliation
lists, which can lead to incorrect conclusions (e.g., counting non-first affiliations as valid matches). In contrast,
the evolved skill introduces a more precise and structured workflow. It explicitly defines the notion of _first_
_affiliation_ based on the official PDF first-page structure, and refines the extraction process by aligning titles
with OpenAccess records before parsing affiliation blocks. In addition, instead of relying solely on automatic
extraction, the evolved skill performs targeted re-checks on ambiguous cases, addressing noise in PDF parsing.
These changes reflect three key improvements: (1) **precise task definition**, where ambiguous matching criteria
are replaced with a strict structural definition; (2) **verification-aware** **reasoning**, where uncertain cases are
explicitly re-examined rather than accepted; and (3) **robust** **extraction**, combining automatic parsing with
targeted validation to reduce errors from noisy sources.


Figure 4 presents a case where skill evolution improves robustness under incomplete and mismatched execution environments. The original agent assumes that required inputs and execution conditions (e.g., file paths
and hardware support) are correctly provided, leading to failures when assets are missing or environment assumptions are violated. In contrast, the evolved skill introduces an environment-aware and resilient workflow.
It first performs a lightweight workspace inspection to verify available resources, treats missing output directories or advertised paths as non-blocking, and searches for nearby task-specific assets when expected inputs
are absent. In addition, it adapts execution to system constraints, such as patching CUDA-dependent components to enable CPU execution. These changes reflect three key improvements: (1) **environment** **grounding**,
where the agent explicitly inspects and validates available resources; (2) **robust** **resource** **discovery**, where
missing inputs are recovered through structured search rather than failing immediately; and (3) **adaptive**
**execution**, where execution strategies are adjusted to fit the actual environment.


Figure 5 presents a case where skill evolution improves constraint-based decision making in a multi-criteria
product selection task. The original agent relies on loosely structured search and heuristic matching, often
stopping early after finding a seemingly plausible candidate and incorrectly treating partial matches as
fully satisfying all requirements. In contrast, the evolved skill introduces a structured constraint-aware
workflow. It systematically verifies each requirement (e.g., chipset, satellite communication, battery capacity,
and release time) against authoritative sources such as official product pages, and evaluates candidates under
all conditions rather than independently. Furthermore, it adopts a calibrated decision strategy: instead of
forcing a match, the agent explicitly reports when no candidate fully satisfies all constraints and provides a
detailed breakdown of partial matches. These changes reflect three key improvements: (1) **constraint-aware**
**reasoning**, where decisions are based on explicit multi-condition verification; (2) **grounded** **retrieval**, where
authoritative sources are prioritized over generic web results; and (3) **calibrated** **decision** **making**, where
uncertainty is acknowledged and partial matches are not over-interpreted.

### **4 Related Work**


**4.1** **Agent** **Self-Evolution**


Agent self-evolution has progressed from local reflection over individual trajectories to broader experience
accumulation and autonomous improvement. Shinn et al. (2024) studies verbal self-correction after interaction, Zhao et al. (2024) turns experience into reusable lessons, and Liu et al. (2025b) further improves reuse
through contextual replay. Beyond reflection, planning-oriented work such as Zhou et al. (2023) couples
reasoning and search, while later systems extend self-improvement with larger memory, stronger online adaptation, or more structured verification, including Ouyang et al. (2025b), Zhai et al. (2025), Liu et al. (2025a),
Fang et al. (2025b), Wang et al. (2026b), Zhang et al. (2026c), Xia et al. (2026b), and Huang and Huang
(2025). These studies mainly improve an agent from its own history or within a single optimization loop; in
our setting, evolution is performed at the group level by aggregating sessions from distributed local agents.


**4.2** **Agent** **Skills**


Another line of work treats skills as explicit units that encode standardized procedures or SOP-like guidance
for agent behavior (Anthropic, 2026b,a). Wang et al. (2023) demonstrates the value of an accumulating


13


skill library for lifelong learning, and later work studies skill optimization, discovery, refinement, and transfer
through transferable skills (Nottingham et al., 2024; Xia et al., 2026b; Wang et al., 2026b), web skill induction
(Zheng et al., 2025), automated multi-agent skill discovery (Alzubi et al., 2026), recursive skill-augmented
learning (Xia et al., 2026a), evolving memory skills (Zhang et al., 2026a), lifelong skill self-evolution (Yang
et al., 2026), and routing through skill transfer (Wang et al., 2026a). At a broader ecosystem level, Tang
et al. (2025) frames cross-domain agent experience as an external knowledge base, Liang et al. (2026) studies
how skills can be created and connected, Li et al. (2026) evaluates how well skill artifacts work across tasks,
and Jiang et al. (2026) summarizes the notion of agentic skills beyond simple tool use. Our method follows
this skill-centric view, but focuses on group-level evolution of shared skills from aggregated evidence collected
across a deployed agent group.

### **5 Conclusion**


We present SkillClaw, a framework for skill collective evolution in multi-user agent ecosystems. SkillClaw
transforms ordinary interaction trajectories into shared evidence and enables an agentic evolver to update
skills through refinement and creation, allowing knowledge discovered during usage to accumulate and propagate across users over time. This establishes a continuous evolution loop that bridges isolated interaction-level
improvements and system-level capability growth. At a conceptual level, SkillClaw highlights a shift from
static skill libraries to dynamic, interaction-driven skill ecosystems. Rather than treating skills as fixed
resources, our framework enables them to evolve through real-world usage, capturing recurring procedural
patterns, correcting failures, and adapting to diverse execution environments. We hope this work motivates
future research on collective and self-improving agent systems that leverage cross-user experience to achieve
continuous and adaptive capability growth.

### **References**


Salaheddin Alzubi, Noah Provenzano, Jaydon Bingham, Weiyuan Chen, and Tu Vu. Evoskill: Automated skill
discovery for multi-agent systems. _arXiv_ _preprint_ _arXiv:2603.02766_, 2026.


Anthropic. How to create a skill with claude through conversation. Claude Tutorials, 2026a. `[https://claude.com/r](https://claude.com/resources/tutorials/how-to-create-a-skill-with-claude-through-conversation)`
`[esources/tutorials/how-to-create-a-skill-with-claude-through-conversation](https://claude.com/resources/tutorials/how-to-create-a-skill-with-claude-through-conversation)` . Accessed: 2026-03-29.


Anthropic. What are skills? Claude Help Center, 2026b. `[https://support.claude.com/en/articles/12512176-w](https://support.claude.com/en/articles/12512176-what-are-skills)`
`[hat-are-skills](https://support.claude.com/en/articles/12512176-what-are-skills)` . Accessed: 2026-03-29.


Prateek Chhikara, Dev Khant, Saket Aryan, Taranjeet Singh, and Deshraj Yadav. Mem0: Building production-ready
ai agents with scalable long-term memory. _arXiv_ _preprint_ _arXiv:2504.19413_, 2025.


Shuangrui Ding, Xuanlang Dai, Long Xing, Shengyuan Ding, Ziyu Liu, Jingyi Yang, Penghui Yang, Zhixiong Zhang,
Xilin Wei, Yubo Ma, Haodong Duan, Jing Shao, Jiaqi Wang, Dahua Lin, Kai Chen, and Yuhang Zang. Wildclawbench. https://github.com/InternLM/WildClawBench, 2026. GitHub repository.


Runnan Fang, Yuan Liang, Xiaobin Wang, Jialong Wu, Shuofei Qiao, Pengjun Xie, Fei Huang, Huajun Chen, and
Ningyu Zhang. Memp: Exploring agent procedural memory. _arXiv_ _preprint_ _arXiv:2508.06433_, 2025a.


Tianqing Fang, Hongming Zhang, Zhisong Zhang, Kaixin Ma, Wenhao Yu, Haitao Mi, and Dong Yu. Webevolver:
Enhancing web agent self-improvement with co-evolving world model. In _Proceedings_ _of_ _the_ _2025_ _Conference_ _on_
_Empirical_ _Methods_ _in_ _Natural_ _Language_ _Processing_, pages 8970–8986, 2025b.


Ken Huang and Jerry Huang. Audited skill-graph self-improvement for agentic llms via verifiable rewards, experience
synthesis, and continual memory. _arXiv_ _preprint_ _arXiv:2512.23760_, 2025.


Yanna Jiang, Delong Li, Haiyu Deng, Baihe Ma, Xu Wang, Qin Wang, and Guangsheng Yu. Sok: Agentic skills–
beyond tool use in llm agents. _arXiv_ _preprint_ _arXiv:2602.20867_, 2026.


Xiangyi Li, Wenbo Chen, Yimin Liu, Shenghan Zheng, Xiaokun Chen, Yifeng He, Yubo Li, Bingran You, Haotian
Shen, Jiankai Sun, et al. Skillsbench: Benchmarking how well agent skills work across diverse tasks. _arXiv_ _preprint_
_arXiv:2602.12670_, 2026.


14


Yuan Liang, Ruobin Zhong, Haoming Xu, Chen Jiang, Yi Zhong, Runnan Fang, Jia-Chen Gu, Shumin Deng, Yunzhi
Yao, Mengru Wang, et al. Skillnet: Create, evaluate, and connect ai skills. _arXiv_ _preprint_ _arXiv:2603.04448_, 2026.


Genglin Liu, Shijie Geng, Sha Li, Hejie Cui, Sarah Zhang, Xin Liu, and Tianyi Liu. Webcoach: Self-evolving web
agents with cross-session memory guidance. _arXiv_ _preprint_ _arXiv:2511.12997_, 2025a.


Jiaqi Liu, Yaofeng Su, Peng Xia, Siwei Han, Zeyu Zheng, Cihang Xie, Mingyu Ding, and Huaxiu Yao. Simplemem:
Efficient lifelong memory for llm agents. _arXiv_ _preprint_ _arXiv:2601.02553_, 2026.


Yitao Liu, Chenglei Si, Karthik R Narasimhan, and Shunyu Yao. Contextual experience replay for self-improvement
of language agents. In _Proceedings_ _of_ _the_ _63rd_ _Annual_ _Meeting_ _of_ _the_ _Association_ _for_ _Computational_ _Linguistics_
_(Volume_ _1:_ _Long_ _Papers)_, pages 14179–14198, 2025b.


Silen Naihin, David Atkinson, Marc Green, Merwane Hamadi, Craig Swift, Douglas Schonholtz, Adam Tauman Kalai,
and David Bau. Testing language model agents safely in the wild. _arXiv_ _preprint_ _arXiv:2311.10538_, 2023.


Kolby Nottingham, Bodhisattwa Prasad Majumder, Bhavana Dalvi Mishra, Sameer Singh, Peter Clark, and Roy Fox.
Skill set optimization: Reinforcing language model behavior via transferable skills. _arXiv preprint arXiv:2402.03244_,
2024.


Siru Ouyang, Jun Yan, I Hsu, Yanfei Chen, Ke Jiang, Zifeng Wang, Rujun Han, Long T Le, Samira Daruki, Xiangru
Tang, et al. Reasoningbank: Scaling agent self-evolving with reasoning memory. _arXiv_ _preprint_ _arXiv:2509.25140_,
2025a.


Siru Ouyang, Jun Yan, I-Hung Hsu, Yanfei Chen, Ke Jiang, Zifeng Wang, Rujun Han, Long T Le, Samira Daruki,
Xiangru Tang, et al. Reasoningbank: Scaling agent self-evolving with reasoning memory, 2025. _URL_ _https://arxiv._
_org/abs/2509.25140_, 2025b.


Noah Shinn, Federico Cassano, Ashwin Gopinath, Karthik Narasimhan, and Shunyu Yao. Reflexion: Language agents
with verbal reinforcement learning. _Advances_ _in_ _Neural_ _Information_ _Processing_ _Systems_, 36:8634–8652, 2023.


Noah Shinn, Federico Cassano, Edward Berman, Ashwin Gopinath, Karthik Narasimhan, and Shunyu Yao. Reflexion:
Language agents with verbal reinforcement learning, 2023. _URL_ _https://arxiv._ _org/abs/2303.11366_, 8, 2024.


Dawn Song, Chenguang Wang, Nicholas Crispino, Ruoxi Jia, Kyle Montgomery, Yujin Potter, Vincent Siu, and Zhun
Wang. Agents in the wild: Safety, security, and beyond. In _ICLR_ _2026_ _Workshop_ _Proposals_, 2026.


Xiangru Tang, Tianrui Qin, Tianhao Peng, Ziyang Zhou, Daniel Shao, Tingting Du, Xinming Wei, Peng Xia, Fang
Wu, He Zhu, et al. Agent kb: Leveraging cross-domain experience for agentic problem solving. _arXiv_ _preprint_
_arXiv:2507.06229_, 2025.


Guanzhi Wang, Yuqi Xie, Yunfan Jiang, Ajay Mandlekar, Chaowei Xiao, Yuke Zhu, Linxi Fan, and Anima Anandkumar. Voyager: An open-ended embodied agent with large language models. _Transactions_ _on_ _Machine_ _Learning_
_Research_, 2023. arXiv:2305.16291.


Jiayu Wang, Yifei Ming, Zixuan Ke, Shafiq Joty, Aws Albarghouthi, and Frederic Sala. Skillorchestra: Learning to
route agents via skill transfer. _arXiv_ _preprint_ _arXiv:2602.19672_, 2026a.


Yinjie Wang, Xuyang Chen, Xiaolong Jin, Mengdi Wang, and Ling Yang. Openclaw-rl: Train any agent simply by
talking. _arXiv_ _preprint_ _arXiv:2603.10165_, 2026b.


Rong Wu, Xiaoman Wang, Jianbiao Mei, Pinlong Cai, Daocheng Fu, Cheng Yang, Licheng Wen, Xuemeng Yang,
Yufan Shen, Yuxin Wang, et al. Evolver: Self-evolving llm agents through an experience-driven lifecycle. _arXiv_
_preprint_ _arXiv:2510.16079_, 2025.


Peng Xia, Jianwen Chen, Hanyang Wang, Jiaqi Liu, Kaide Zeng, Yu Wang, Siwei Han, Yiyang Zhou, Xujiang Zhao,
Haifeng Chen, et al. Skillrl: Evolving agents via recursive skill-augmented reinforcement learning. _arXiv_ _preprint_
_arXiv:2602.08234_, 2026a.


Peng Xia, Jianwen Chen, Xinyu Yang, Haoqin Tu, Jiaqi Liu, Kaiwen Xiong, Siwei Han, Shi Qiu, Haonian Ji, Yuyin
Zhou, Zeyu Zheng, Cihang Xie, and Huaxiu Yao. Metaclaw: Just talk  - an agent that meta-learns and evolves in
the wild. _arXiv_ _preprint_ _arXiv:2603.17187_, 2026b.


Yutao Yang, Junsong Li, Qianjun Pan, Bihao Zhan, Yuxuan Cai, Lin Du, Jie Zhou, Kai Chen, Qin Chen, Xin Li,
et al. Autoskill: Experience-driven lifelong learning via skill self-evolution. _arXiv_ _preprint_ _arXiv:2603.01145_, 2026.


15


Shunyu Yao, Jeffrey Zhao, Dian Yu, Nan Du, Izhak Shafran, Karthik R Narasimhan, and Yuan Cao. React: Synergizing reasoning and acting in language models. In _The_ _eleventh_ _international_ _conference_ _on_ _learning_ _representations_,
2022.


Yunpeng Zhai, Shuchang Tao, Cheng Chen, Anni Zou, Ziqian Chen, Qingxu Fu, Shinji Mai, Li Yu, Jiaji Deng, Zouying
Cao, et al. Agentevolver: Towards efficient self-evolving agent system. _arXiv_ _preprint_ _arXiv:2511.10395_, 2025.


Guibin Zhang, Haotian Ren, Chong Zhan, Zhenhong Zhou, Junhao Wang, He Zhu, Wangchunshu Zhou, and Shuicheng
Yan. Memevolve: Meta-evolution of agent memory systems. _arXiv_ _preprint_ _arXiv:2512.18746_, 2025a.


Guibin Zhang, Junhao Wang, Junjie Chen, Wangchunshu Zhou, Kun Wang, and Shuicheng Yan. Agentracer: Who is
inducing failure in the llm agentic systems? _arXiv_ _preprint_ _arXiv:2509.03312_, 2025b.


Haozhen Zhang, Quanyu Long, Jianzhu Bao, Tao Feng, Weizhi Zhang, Haodong Yue, and Wenya Wang. Memskill:
Learning and evolving memory skills for self-evolving agents. _arXiv_ _preprint_ _arXiv:2602.02474_, 2026a.


Shengtao Zhang, Jiaqian Wang, Ruiwen Zhou, Junwei Liao, Yuchen Feng, Weinan Zhang, Ying Wen, Zhiyu Li, Feiyu
Xiong, Yutao Qi, et al. Memrl: Self-evolving agents via runtime reinforcement learning on episodic memory. _arXiv_
_preprint_ _arXiv:2601.03192_, 2026b.


Xiaoying Zhang, Zichen Liu, Yipeng Zhang, Xia Hu, and Wenqi Shao. Retroagent: From solving to evolving via
retrospective dual intrinsic feedback. _arXiv_ _preprint_ _arXiv:2603.08561_, 2026c.


Andrew Zhao, Daniel Huang, Quentin Xu, Matthieu Lin, Yong-Jin Liu, and Gao Huang. Expel: Llm agents are
experiential learners. In _Proceedings_ _of_ _the_ _AAAI_ _Conference_ _on_ _Artificial_ _Intelligence_, volume 38, pages 19632–
19642, 2024.


Boyuan Zheng, Michael Y Fatemi, Xiaolong Jin, Zora Zhiruo Wang, Apurva Gandhi, Yueqi Song, Yu Gu, Jayanth
Srinivasa, Gaowen Liu, Graham Neubig, et al. Skillweaver: Web agents can self-improve by discovering and honing
skills. _arXiv_ _preprint_ _arXiv:2504.07079_, 2025.


Andy Zhou, Kai Yan, Michal Shlapentokh-Rothman, Haohan Wang, and Yu-Xiong Wang. Language agent tree search
unifies reasoning acting and planning in language models. _arXiv_ _preprint_ _arXiv:2310.04406_, 2023.



16


17


18


19


20


21


22


23


24


