## **AORCHESTRA: Automating Sub-Agent Creation for Agentic Orchestration**

**Jianhao Ruan** **[*]** [1 2] **Zhihao Xu** **[*]** [3] **Yiran Peng** [1] **Fashen Ren** [2] **Zhaoyang Yu** [1]

**Xinbing Liang** [4] **Jinyu Xiang** [2] **Yongru Chen** [2] **Bang Liu** [5] **Chenglin Wu** [1] **Yuyu Luo** [2] **Jiayi Zhang** [1 2]



**Abstract**


Language agents have shown strong promise for
task automation. Realizing this promise for increasingly complex, long-horizon tasks has driven
the rise of a sub-agent-as-tools paradigm for multiturn task solving. However, existing designs
still lack a _dynamic_ _abstraction_ view of subagents, thereby hurting adaptability. We address
this challenge with a unified, framework-agnostic
agent abstraction that models any agent as a tuple
_⟨Instruction, Context, Tools, Model⟩_ . This
tuple acts as a compositional recipe for capabilities, enabling the system to spawn specialized
executors for each task on demand. Building on
this abstraction, we introduce an agentic system
AORCHESTRA, where the central orchestrator
concretizes the tuple at each step: it curates taskrelevant context, selects tools and models, and
delegates execution via on-the-fly automatic agent
creation. Such designs enable reducing human engineering efforts, and remain framework-agnostic
with plug-and-play support for diverse agents as
task executors. It also enables a controllable performance–cost trade-off, allowing the system to
approach Pareto-efficient. Across three challenging benchmarks (GAIA, SWE-Bench, TerminalBench), AORCHESTRA achieves 16.28% relative improvement against the strongest baseline when paired with Gemini-3-Flash. The
code is available at: [https://github.com/](https://github.com/FoundationAgents/AOrchestra )
[FoundationAgents/AOrchestra](https://github.com/FoundationAgents/AOrchestra )


**1. Introduction**


Humans handle complex, long-horizon work via collective intelligence and the ability to coordinate (Gao et al.,
2025a; Zhu et al., 2025b; Li et al., 2025a). As today’s
agents are pushed toward similarly complex and multi-turn


1DeepWisdom 2HKUST(GZ) 3RUC 4ECNU 5UdeM & Mila.
Correspondence to: Yuyu Luo _<_ yuyuluo@hkust-gz.edu.cn _>_, Jiayi Zhang _<_ jzhang361@connect.hkust-gz.edu.cn _>_ .


_Preprint._ _February 10, 2026._


|Col1|Col2|Col3|Col4|Col5|Col6|Col7|Col8|Col9|
|---|---|---|---|---|---|---|---|---|
||||||||||
||||||22.00|22.00|22.00||
||||||||||



|82.00 80 8|80.00|0 55 52.86|Col4|Col5|Col6|Col7|Col8|Col9|Col10|Col11|Col12|Col13|Col14|Col15|Col16|Col17|Col18|Col19|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|0<br>20<br>40<br>60<br>80<br>82.00<br>64.00<br>48.00<br>22.00<br>~~56.00~~<br>45<br>50<br>55<br>60<br>65<br>70<br>75<br><br>Accuracy (%)<br><br><br>||49.09<br>66.06<br>58.18<br>25<br>30<br>35<br>40<br>45<br>50<br>55<br>~~52.86~~<br>28.57<br>35.96<br>~~32.86~~<br>34.2<br><br> <br>|49.09<br>66.06<br>58.18<br>25<br>30<br>35<br>40<br>45<br>50<br>55<br>~~52.86~~<br>28.57<br>35.96<br>~~32.86~~<br>34.2<br><br> <br>|49.09<br>66.06<br>58.18<br>25<br>30<br>35<br>40<br>45<br>50<br>55<br>~~52.86~~<br>28.57<br>35.96<br>~~32.86~~<br>34.2<br><br> <br>|49.09<br>66.06<br>58.18<br>25<br>30<br>35<br>40<br>45<br>50<br>55<br>~~52.86~~<br>28.57<br>35.96<br>~~32.86~~<br>34.2<br><br> <br>|49.09<br>66.06<br>58.18<br>25<br>30<br>35<br>40<br>45<br>50<br>55<br>~~52.86~~<br>28.57<br>35.96<br>~~32.86~~<br>34.2<br><br> <br>|49.09<br>66.06<br>58.18<br>25<br>30<br>35<br>40<br>45<br>50<br>55<br>~~52.86~~<br>28.57<br>35.96<br>~~32.86~~<br>34.2<br><br> <br>|49.09<br>66.06<br>58.18<br>25<br>30<br>35<br>40<br>45<br>50<br>55<br>~~52.86~~<br>28.57<br>35.96<br>~~32.86~~<br>34.2<br><br> <br>|49.09<br>66.06<br>58.18<br>25<br>30<br>35<br>40<br>45<br>50<br>55<br>~~52.86~~<br>28.57<br>35.96<br>~~32.86~~<br>34.2<br><br> <br>|49.09<br>66.06<br>58.18<br>25<br>30<br>35<br>40<br>45<br>50<br>55<br>~~52.86~~<br>28.57<br>35.96<br>~~32.86~~<br>34.2<br><br> <br>|49.09<br>66.06<br>58.18<br>25<br>30<br>35<br>40<br>45<br>50<br>55<br>~~52.86~~<br>28.57<br>35.96<br>~~32.86~~<br>34.2<br><br> <br>|49.09<br>66.06<br>58.18<br>25<br>30<br>35<br>40<br>45<br>50<br>55<br>~~52.86~~<br>28.57<br>35.96<br>~~32.86~~<br>34.2<br><br> <br>|49.09<br>66.06<br>58.18<br>25<br>30<br>35<br>40<br>45<br>50<br>55<br>~~52.86~~<br>28.57<br>35.96<br>~~32.86~~<br>34.2<br><br> <br>|49.09<br>66.06<br>58.18<br>25<br>30<br>35<br>40<br>45<br>50<br>55<br>~~52.86~~<br>28.57<br>35.96<br>~~32.86~~<br>34.2<br><br> <br>|49.09<br>66.06<br>58.18<br>25<br>30<br>35<br>40<br>45<br>50<br>55<br>~~52.86~~<br>28.57<br>35.96<br>~~32.86~~<br>34.2<br><br> <br>|49.09<br>66.06<br>58.18<br>25<br>30<br>35<br>40<br>45<br>50<br>55<br>~~52.86~~<br>28.57<br>35.96<br>~~32.86~~<br>34.2<br><br> <br>|49.09<br>66.06<br>58.18<br>25<br>30<br>35<br>40<br>45<br>50<br>55<br>~~52.86~~<br>28.57<br>35.96<br>~~32.86~~<br>34.2<br><br> <br>|49.09<br>66.06<br>58.18<br>25<br>30<br>35<br>40<br>45<br>50<br>55<br>~~52.86~~<br>28.57<br>35.96<br>~~32.86~~<br>34.2<br><br> <br>|
|0<br>20<br>40<br>60<br>80<br>82.00<br>64.00<br>48.00<br>22.00<br>~~56.00~~<br>45<br>50<br>55<br>60<br>65<br>70<br>75<br><br>Accuracy (%)<br><br><br>|||||||||||||||||||
|0<br>20<br>40<br>60<br>80<br>82.00<br>64.00<br>48.00<br>22.00<br>~~56.00~~<br>45<br>50<br>55<br>60<br>65<br>70<br>75<br><br>Accuracy (%)<br><br><br>|||||||||||||||||||
|0<br>20<br>40<br>60<br>80<br>82.00<br>64.00<br>48.00<br>22.00<br>~~56.00~~<br>45<br>50<br>55<br>60<br>65<br>70<br>75<br><br>Accuracy (%)<br><br><br>|||||||||||||||||||
|0<br>20<br>40<br>60<br>80<br>82.00<br>64.00<br>48.00<br>22.00<br>~~56.00~~<br>45<br>50<br>55<br>60<br>65<br>70<br>75<br><br>Accuracy (%)<br><br><br>|||||||||||||||||||
|0<br>20<br>40<br>60<br>80<br>82.00<br>64.00<br>48.00<br>22.00<br>~~56.00~~<br>45<br>50<br>55<br>60<br>65<br>70<br>75<br><br>Accuracy (%)<br><br><br>|||||||||||||||||||
|0<br>20<br>40<br>60<br>80<br>82.00<br>64.00<br>48.00<br>22.00<br>~~56.00~~<br>45<br>50<br>55<br>60<br>65<br>70<br>75<br><br>Accuracy (%)<br><br><br>|||||||||||35.96<br>~~32.86~~<br>34.2|35.96<br>~~32.86~~<br>34.2|35.96<br>~~32.86~~<br>34.2|35.96<br>~~32.86~~<br>34.2|35.96<br>~~32.86~~<br>34.2|35.96<br>~~32.86~~<br>34.2|35.96<br>~~32.86~~<br>34.2|35.96<br>~~32.86~~<br>34.2|
|0<br>20<br>40<br>60<br>80<br>82.00<br>64.00<br>48.00<br>22.00<br>~~56.00~~<br>45<br>50<br>55<br>60<br>65<br>70<br>75<br><br>Accuracy (%)<br><br><br>|||||||||||||||||||
|0<br>20<br>40<br>60<br>80<br>82.00<br>64.00<br>48.00<br>22.00<br>~~56.00~~<br>45<br>50<br>55<br>60<br>65<br>70<br>75<br><br>Accuracy (%)<br><br><br>|||||||||||28.57|28.57|28.57||||||
|0<br>20<br>40<br>60<br>80<br>82.00<br>64.00<br>48.00<br>22.00<br>~~56.00~~<br>45<br>50<br>55<br>60<br>65<br>70<br>75<br><br>Accuracy (%)<br><br><br>||49.09|49.09|49.09|||||||||||||||
|0<br>20<br>40<br>60<br>80<br>82.00<br>64.00<br>48.00<br>22.00<br>~~56.00~~<br>45<br>50<br>55<br>60<br>65<br>70<br>75<br><br>Accuracy (%)<br><br><br>|||||||||||||||||||
|0<br>20<br>40<br>60<br>80<br>82.00<br>64.00<br>48.00<br>22.00<br>~~56.00~~<br>45<br>50<br>55<br>60<br>65<br>70<br>75<br><br>Accuracy (%)<br><br><br>|||||||||||||||||||
||Ope|nH|and|s||||Cl|aude C|od|e||||M|ini|-S|WE|
||Ope|nH|and|s|||||||||||||||
|_Figure 1._ Overall performa<br>marks (GAIA, Terminal-<br>with Gemini-3-Flash when<br>popular agentic framewor<br>tasks (Yao et al., 2024; <br>a well-designed agentic<br>performance beyond a s|nc<br> Be<br>  co<br> ks.<br> Zh<br>  sy<br>  in|e<br> nc<br>  m<br> an<br>  st<br>  gl|on<br> h-<br>  par<br> g<br>  em<br>  e|th<br> 2,<br>  in<br> et<br>  b<br>  m|ree<br>  SW<br>  g<br>  al.<br>  ec<br>  od|ree<br>  SW<br>  g<br>  al.<br>  ec<br>  od|c<br> <br>  A<br>, <br>  o<br>  el|hal<br>  E-B<br>  OR<br> 20<br>  me<br>   (L|lenging agentic bench<br>  ench-Verifed) paired<br>CHESTRA against othe<br> 25a; Xu et al., 2026)<br>  s a vital way to scale<br>iu et al., 2025b).|lenging agentic bench<br>  ench-Verifed) paired<br>CHESTRA against othe<br> 25a; Xu et al., 2026)<br>  s a vital way to scale<br>iu et al., 2025b).|lenging agentic bench<br>  ench-Verifed) paired<br>CHESTRA against othe<br> 25a; Xu et al., 2026)<br>  s a vital way to scale<br>iu et al., 2025b).|lenging agentic bench<br>  ench-Verifed) paired<br>CHESTRA against othe<br> 25a; Xu et al., 2026)<br>  s a vital way to scale<br>iu et al., 2025b).|lenging agentic bench<br>  ench-Verifed) paired<br>CHESTRA against othe<br> 25a; Xu et al., 2026)<br>  s a vital way to scale<br>iu et al., 2025b).|lenging agentic bench<br>  ench-Verifed) paired<br>CHESTRA against othe<br> 25a; Xu et al., 2026)<br>  s a vital way to scale<br>iu et al., 2025b).|lenging agentic bench<br>  ench-Verifed) paired<br>CHESTRA against othe<br> 25a; Xu et al., 2026)<br>  s a vital way to scale<br>iu et al., 2025b).|lenging agentic bench<br>  ench-Verifed) paired<br>CHESTRA against othe<br> 25a; Xu et al., 2026)<br>  s a vital way to scale<br>iu et al., 2025b).|lenging agentic bench<br>  ench-Verifed) paired<br>CHESTRA against othe<br> 25a; Xu et al., 2026)<br>  s a vital way to scale<br>iu et al., 2025b).|lenging agentic bench<br>  ench-Verifed) paired<br>CHESTRA against othe<br> 25a; Xu et al., 2026)<br>  s a vital way to scale<br>iu et al., 2025b).|


To cope with increasingly complex scenarios, early attempts
rely on fixed coordination workflows or multi-agent systems (Hong et al., 2023; Hu et al., 2025; Li et al., 2025a).
While multi-agent collaboration can improve task decomposition, in open-ended environments it often incurs substantial coordination overhead and provides limited control
over context routing, leading to either noisy over-sharing
or harmful omission of critical information, which makes
robust long-horizon execution difficult (Gao et al., 2025b).


More recent approaches therefore move toward a more practical sub-agent-as-tools paradigm, where a main agent (orchestrator) delegates a task to a sub-agent via an explicit
tool call. Yet existing designs still lack flexibility in practice and often degenerate into two limited patterns, which
are shown in Figure 2: (1) _Sub-agents as context-isolation_
_threads._ Systems such as Schroeder et al. (2025); Sun et al.
(2025) primarily treat sub-agents as isolated context threads,
aiming to prevent context rot (Hong et al., 2025). However,
in real-world tasks, subtasks often require specialized capabilities. Therefore, such systems fail to fully realize the
potential of specialized sub-agents. (2) _Sub-agents as static_
_roles._ Systems such as Anthropic (2025); Li et al. (2025c)



Swe-Bench-Verified



100



Terminal Bench





Gaia









85





60













1


**AORCHESTRA:** **Automating Sub-Agent Creation for Agentic Orchestration**


**Mitigate Context Rot** **Specialized Capability** **Specialized Capability**

**Few Specialization** **Inflexible & Human effort** **Dynamic & Flexible**















Main
Agent



Copy


Return







Copied Sub-Agent


**(a)** **Sub-Agent as Context-**

**Isolated Threads**



Pre-defined Sub-Agent


**(b) Sub-Agent as Static,**

**Predefined Roles**



Dynamic Sub-Agent


**(c) Ours: Sub-Agent as On-**

**Demand Specialization**



_Figure 2._ Comparison of sub-agent-as-tools approaches. **(a) Sub-agents as context-isolated threads** mitigate context rot but lack ondemand specialization. **(b) Sub-agents as static roles** provide specialized capabilities but are inflexible, leave coverage gaps, and require
heavy human engineering. **(c) Our Sub-agents as on-demand specialization** concretizes a unified 4-tuple abstraction (INSTRUCTION,
CONTEXT, TOOLS, MODEL) to enable creating tailored executors on the fly.



treat each sub-agent as a static role, and their capabilities
or their coordination patterns are typically hard-wired. A
pre-defined set of sub-agents cannot cover the dynamically
emerging variety of subtasks in open environments. Besides,
it relies on heavy human engineering, making the system
difficult to adapt to various environments.


In this paper, we introduce AORCHESTRA, an agentic framework designed to tackle long-horizon and complex tasks.
Our core insight lies in treating sub-agents through the lens
of **on-demand specialization**, as illustrated in Figure 2(c).
We posit that a sub-agent should be viewed as a flexible
abstraction unit rather than a predefined, fixed role. This approach enables the system to instantiate tailored sub-agents
at runtime by dynamically composing their capabilities to
meet specific task demands—an essential feature. Concretely, _any_ agent can be described as an instantiable unit
via a unified four-tuple: (INSTRUCTION, CONTEXT, TOOLS,

MODEL). This specialization is organized around two complementary axes essential for an agent’s task solving: (1)
_Working memory (instruction, context):_ what the agent must
achieve and what evidence it should condition on. Notably, the context attribute is designed to inject only the
most relevant information for the current sub-task, filtering
out potentially distracting details. (2) _Capabilities_ _(tools,_
_model):_ what the agent is empowered to do to accomplish
that objective. By composing specific tools and models on
a per-subtask basis, we endow each sub-agent with precise,
task-specific functionality. Together, this 4-tuple design
enables an automatic specialized sub-agent for each task.


Building on this on-demand specialization view, we further introduce a dedicated orchestrator that operates directly
over the four-tuple interface to automatically create tailored
sub-agents on the fly. It does not execute any tasks and
focuses exclusively on orchestration, where we define it
as dynamically decomposing the overall objective into the
next subtask, creating and delegating a specialized tailored



sub-agent for task execution via explicit tool calls. This
decoupling design offers several key advantages. First, this
dynamic creation allows each sub-agent to be customized
with unique capabilities and a clean working context, significantly improving task execution accuracy. Second, the
orchestrator remains agnostic to the internal implementation of sub-agents, making them fully pluggable. Third, the
orchestrator can be trained or learned from interactive experience. This ranges from basic skills for agent creation to
advanced features like adaptive model selection, achieving
an optimal balance between cost and performance.


Through extensive experiments, we demonstrate AORCHES
TRA achieves stronger performance and broader generalization in open-world settings. We first evaluate our framework in a training-free setting on three challenging agentic benchmarks: Terminal-Bench 2.0 (Team, 2025) (bash
environment), SWE-Bench (Jimenez et al., 2023) (coding
environment), and GAIA (Mialon et al., 2023) (digital world
environment). As shown in Figure 1, our method consistently outperforms both representative sub-agent orchestration approaches (Anthropic, 2025) and widely used agent
frameworks (Wang et al., 2024; Yang et al., 2024) across
all benchmarks. In particular, our framework achieves a
16.28% improvement when paired with Gemini3-Flash,
validating the superiority of our orchestration model in complex, long-horizon tasks. Importantly, AORCHESTRA naturally supports learning the orchestration policy from experience. We instantiate this in two ways: (1) we apply
supervised fine-tuning to improve the Orchestrator’s subtask decomposition and 4-tuple synthesis, leading to better
orchestration quality by +11.51% pass@1 on GAIA and
(2) we leverage in-context learning to optimize cost-aware
routing, which improves GAIA pass@1 by +3.03% while reducing average cost by 18.5%, resulting in a more favorable
cost–performance Pareto frontier.


Overall, our contributions are:



2


**AORCHESTRA:** **Automating Sub-Agent Creation for Agentic Orchestration**




  - We propose AORCHESTRA, an orchestrator-centric
agentic system that treats sub-agents as _dynamically_
_creatable_ executors via a unified 4-tuple interface (INSTRUCTION, CONTEXT, TOOLS, MODEL), enabling
on-demand specialization with task-sufficient context
and explicit capability control.


  - AORCHESTRA achieves strong training-free performance on Terminal-Bench 2.0, SWE-Bench-Verified,
and GAIA, consistently outperforming popular agentic systems. We achieve 16.28% relative improvement
against the strongest baseline when paired with Gemini3-Flash.


  - We show the orchestration policy is learnable under
this design from two complementary angles: supervised fine-tuning improves basic task orchestration
(+11.51%), and cost-aware routing via in-context learning yields favorable cost–performance Pareto tradeoffs (reducing average cost by 18.5%).


**2. Related Work**


**Multi-Agent Systems** Inspired by collaborative problem
solving, early efforts propose multi-agent systems (MAS)
to enhance the task-solving capability of language models (Zhang et al., 2025b; Lin et al., 2025; Wu et al., 2024;
Shi et al., 2025b; Gao et al., 2025b; Zhu et al., 2025a; Fang
et al., 2025; Zhang et al., 2024; Li et al., 2025b). For example, MetaGPT (Hong et al., 2023) organizes agents into
a structured software-development workflow, where specialized roles (e.g., product manager, architect) collaborate
via predefined communication protocols. OWL (Hu et al.,
2025) adopts a planner-worker workflow to improve transfer and generalization by modularizing domain-agnostic
planning and domain-specific execution. Despite their effectiveness, most MAS typically rely on a fixed workflow,
leading to rigidity. Although AutoAgents (Chen et al., 2023)
proposes building different multi-agent systems for each
task, they still rely on a fixed workflow to accomplish this.
This motivates a growing shift toward the _sub-agents-as-_
_tools_ paradigm, and we will list related works in the next
part (Gao et al., 2025a;b). AORCHESTRA follows the latter
and further emphasizes orchestration-centric, dynamic subagent creation without relying on a specific human-designed
workflow.


**Sub-Agent** **as** **Tools** This approach involves a primary
agentic model invoking a sub-agent in a tool-like manner to
solve problems (Li et al., 2025c; Su et al., 2025; Grand et al.,
2025; Liu et al., 2025c). For example, THREAD (Schroeder
et al., 2025) enables the recursive spawning of sub-agents
to address decomposed subproblems. Similarly, ContextFolding (Sun et al., 2025) proposes branching for a subtask
and then folding it back by compressing intermediate steps



into a concise summary, thereby managing context. However, these methods do not treat sub-agents as fully specialized agents, leading to their insufficient utilization. Other
practical systems, such as Claude Code (Anthropic, 2025),
support sub-agents that operate within isolated context windows with custom system prompts and tool permissions. Yet,
these sub-agents are typically configured as fixed specialists
and still require manual design. AORCHESTRA addresses
these limitations by treating each sub-agent as a dynamic
unit and proposes an orchestration-centric agentic system
that proactively and dynamically creates such sub-agents on
demand.


**3. Methodology**


In this section, we first formalize the problem in Section 3.1.
Next, we elaborate on the design of AORCHESTRA in Section 3.2. Finally, we introduce the process for training a
dedicated orchestrator in Section 3.3. Figure 3 provides an
overview of our methodology.


**3.1. Problem Formulation**


In this paper, we mainly focus on solving complex agentic
tasks. The agentic system solves a user goal _G_ through
multi-step interaction with an environment. The environment exposes an _environment-level_ action space _A_ env (e.g.,
shell commands, web operations, code edits) and returns
feedback such as observations, tool outputs, and error messages. An interaction trajectory for a task can be therefore
defined as:


_τ_ = ( _s_ 0 _, a_ 0 _, o_ 0 _, s_ 1 _, a_ 1 _, o_ 1 _, . . ., sT_ ) _,_


where _st_ _∈S_ denotes the system state at step _t_ (including
accumulated history, intermediate results, and environment
feedback), _at_ is the action taken at step _t_, and _ot_ _∈O_ is the
returned observation. The system evolves according to a
state-transition function


_st_ +1 = _δ_ ( _st, at, ot_ ) _,_


where _δ_ : _S × A_ env _× O_ _→S_ maps the current state, action,
and observation to the next state by incorporating newly
returned information into the system’s internal state.


**Sub-agent-as-tools view.** We focus on the sub-agent-astools paradigm, where a _main agent_ (orchestrator) can either
act in the environment directly or delegate a subtask to a subagent as a tool call. Accordingly, the orchestrator operates
over a _system-level_ action space that typically includes three
types of actions: (1) environment actions _u_ _∈A_ env, (2)
delegation actions (Delegate( _·_ )) that invoke a sub-agent
to execute, and (iii) termination (Finish). We denote this
generic orchestration action space as


_A_ orch _⊇A_ env _∪{_ Delegate( _·_ ) _,_ Finish( _y_ ) _}._



3


**AORCHESTRA:** **Automating Sub-Agent Creation for Agentic Orchestration**









































































_Figure 3._ Overall design of our proposed agentic framework, AORCHESTRA, for complex, long-horizon tasks. The orchestrator solves a
user task by repeatedly delegating subtasks to on-the-fly instantiated sub-agents, each defined by a unified four-tuple ( _I, C, T, M_ ). The
orchestrator is learnable and can improve its decomposition, context routing, and capability allocation from past experience.



Different systems mainly differ in how Delegate is parameterized (e.g., delegating with only context vs. delegating to a fixed set of roles), and in whether the orchestrator
itself also performs environment actions.


Our objective is to maximize task success, optionally trading
off execution cost:


       -        max E **1** _{_ Success( _G_ ) _} −_ _λ ·_ Cost( _τ_ ) _,_
_π_


where _π_ is the orchestrator policy, Cost( _τ_ ) may include
token usage, tool calls, latency, or monetary cost, and _λ_
controls the cost–performance trade-off.


**3.2. AORCHESTRA**


**A unified four-tuple agent abstraction.** AORCHESTRA
models _both_ the main agent and sub-agents under a unified framework-agnostic abstraction. We define an agent



instance as an instantiable four-tuple


Φ = ( _I, C, T, M_ ) _,_


where _I_ is the task instruction specifying the current objective and success criteria, _C_ is the curated working context
the agent conditions on, _T_ is the tool set defining the agent’s
action space, and _M_ is the underlying model that interacts
with the environment. This abstraction explicitly separates
two complementary axes that require _specialization_ : _work-_
_ing memory_ ( _I, C_ ) and _capabilities_ ( _T, M_ ). Notably, we
do not view a sub-agent as a static entity, but rather as a _dy-_
_namic_ unit that can be parametrized and created at runtime.


The main agent (orchestrator) can also be represented by
a tuple Φ [main] = ( _I_ [main] _, C_ [main] _, T_ [main] _, M_ [main] ). The difference is that _T_ [main] exposes _system_ _tools_ for orchestration
(e.g., Delegate, Finish) rather than environment tools
in _A_ env.



4


**AORCHESTRA:** **Automating Sub-Agent Creation for Agentic Orchestration**



**Action Space of Orchestrator.** Building on this abstraction, AORCHESTRA decouples orchestration from execution.
The orchestrator in AORCHESTRA never directly takes environment actions in _A_ env. Instead, it operates only the two
following actions:


_A_ AORCHESTRA = _{_ Delegate(Φ) _,_ Finish( _y_ ) _}._


At step _t_, the orchestrator samples an action _at_ _∈_
_A_ AORCHESTRA. If _at_ = Delegate(Φ _t_ ), it spawns an executor _A_ (Φ _t_ ) to execute the subtask and returns an observation
_ot_ . If _at_ = Finish( _y_ ), the interaction terminates with the
final answer _y_ . Returned observations are integrated into
the next state via _st_ +1 = _δ_ ( _st, at, ot_ ).


**Implementation of Delegate and Finish.** We implement AORCHESTRA with two system tools available to the
Orchestrator: Delegate and Finish. Delegate takes
Φ _t_ = ( _It, Ct, Tt, Mt_ ) as arguments and instantiates an executor accordingly. The executor runs with model _Mt_, is
restricted to the tool set _Tt_, and conditions only on ( _It, Ct_ ).
It returns a structured observation _ot_ to the Orchestrator, typically including (i) a concise result summary, (ii) relevant
artifacts (e.g., files, references), and (iii) error messages or
logs if execution fails. Finish terminates the interaction
and outputs the final response _y_ .


**Advantages of AORCHESTRA** Our proposed AORCHESTRA offers several key advantages. First, it dynamically
equips each sub-agent with tailored capabilities on demand,
which substantially improves the accuracy of task execution.
Unlike prior works (Sun et al., 2025; Anthropic, 2025), the
orchestrator deliberately provides well-structured context
for the sub-agent to use. As shown later in Section 4.3.1,
this careful context management enhances the model’s ability to solve tasks. Second, the orchestrator operates solely
on a four-tuple abstraction and remains independent of the
internal implementation of sub-agents. This flexibility allows us to employ various designs for sub-agents, such as
a simple React approach (Yao et al., 2022) or a mini-SWE
agent. Third, the orchestrator can learn from extensive experience. We will then detail this in Section 3.3. These
learnable aspects include basic task orchestration skills (i.e.,
what to do, what to condition on, and which tool to use)
as well as advanced features (e.g., adaptive model routing,
where the goal might be to balance performance and cost by
selecting the most suitable model).


**3.3. Learnable Orchestrator**


With _A_ AORCHESTRA = Delegate(Φ) _,_ Finish( _y_ ), the orchestration task can be expressed as learning a policy over
structured actions:


_πθ_ ( _at_ _| st_ ) _,_ _at_ _∈A_ AORCHESTRA _._



In this paper, learning mainly focuses on the two following
complementary dimensions: Since the delegation parameters Φ _t_ = ( _It, Ct, Tt, Mt_ ) are explicitly available, learning
can focus on two complementary dimensions: (i) **Task or-**
**chestration**, which determines what to do, what context
to use, and which tools to employ. (ii) **Model** **routing**,
which selects _Mt_ (the model to call) to balance performance
and cost. In the following, we detail these two learning
paradigms.


**Supervised** **fine-tuning** **(SFT)** **for** **task** **orchestration.**
Given expert orchestration trajectories _{_ ( _st, a_ _[⋆]_ _t_ [)] _[}]_ [, we fine-]
tune the Orchestrator by behavior cloning:



_θ_ _[⋆]_ = arg max
_θ_




- log _pθ_ ( _a_ _[⋆]_ _t_ _[|][ s][t]_ [)] _[,]_

_t_



where _a_ _[⋆]_ _t_ [is] [the] [expert] [action] [(either] [Delegate][(Φ] _[⋆]_ _t_ [)] [or]
Finish( _y_ _[⋆]_ )). In our setup, SFT primarily distills _task or-_
_chestration_ : improving subtask decomposition and the synthesis of ( _It, Ct, Tt_ ), i.e., producing better working memory,
and more appropriate tool subsets for each step. We would
like to note that in this work, we prioritize showing the potential of training a specialized orchestrator, thus employing
a straightforward SFT approach. Note that others can employ any training methods like GRPO (Shao et al., 2024) to
improve the task orchestration capability.


**Iterative** **In-context** **Learning** **for** **Cost-aware** **Orches-**
**tration.** Beyond parameter updates, we also optimize orchestration _without_ changing model weights by learning the
Orchestrator’s _instruction_ (prompt) through iterative interaction. Concretely, we treat the Orchestrator instruction
_I_ [main] as the learnable object and run AORCHESTRA in the
environment to collect trajectories _τ_ = _{_ ( _st, at, ot_ ) _}_ _[T]_ _t_ =0 [to-]
gether with outcome metrics, including task performance
and execution cost. An optimization model then analyzes
these trajectories and proposes prompt edits ∆ _I_ to update
the instruction:


_Ik_ [main] +1 [=] [O][PTIMIZE]  - _Ik_ [main] _,_ _τk,_ Perf( _τk_ ) _,_ Cost( _τk_ )� _,_


where _k_ indexes optimization rounds. By repeatedly rolling
out the updated Orchestrator in the environment for _N_
rounds, this process improves cost-aware orchestration behavior (e.g., model compiler/routing decisions and tool usage patterns) and aims to discover Pareto-efficient trade-offs
between performance and cost.


**4. Experiments**


**4.1. Experiment Setup**


**Benchmarks.** We evaluate our method on three challenging
agentic benchmarks that span diverse interactive settings:
(1) **Terminal-Bench 2.0** (Team, 2025), which places agents



5


**AORCHESTRA:** **Automating Sub-Agent Creation for Agentic Orchestration**


_Table 1._ Comparison between AORCHESTRA and baseline agentic systems on GAIA, Terminal-Bench 2.0, and SWE-BenchVerified under various models. The best results are in **bold** .


**Methods** **Model Setup** **GAIA** **Terminal-Bench 2.0** **SWE-Bench-Verified**


**Pass@1** **Pass@3** **Pass@1** **Pass@3** **Pass@1** **Pass@3** **Avg.** **Pass@1**


Gemini-3-Flash 49.09 66.06 28.57 47.14 64.00 82.00 47.22
ReAct DeepSeek-V3.2 46.70 71.51 20.00 32.86 48.00 87.00 38.23
Claude-4.5-haiku 47.88 62.42 20.00 37.14 63.00 87.00 43.62


Gemini-3-Flash 66.06 72.73 31.43 51.43 48.00 66.00 48.49
OpenHands DeepSeek-V3.2 63.64 72.12 21.43 35.71 60.00 75.00 48.35
Claude-4.5-haiku 54.55 61.21 12.85 25.71 68.00 83.00 45.13


Gemini-3-Flash 58.18 68.48 34.29 50.00 56.00 85.00 49.49
Mini-SWE DeepSeek-V3.2 50.30 63.63 30.00 48.57 **84.00** **89.00** 54.76
Claude-4.5-haiku 40.61 60.00 24.29 28.57 44.00 83.00 36.30


Gemini-3-Flash          -          - 32.86 48.57 22.00 42.00 27.43
Claude Code
Claude-4.5-haiku          -          - 34.29 45.71 25.00 41.00 29.65


Gemini-3-Flash **80.00** **86.06** **52.86** **57.14** 82.00 86.00 **71.62**
AORCHESTRA DeepSeek-V3.2 67.87 80.00 31.43 42.86 76.00 82.00 58.43
Claude-4.5-haiku 60.61 73.90 35.71 45.71 70.00 84.00 55.44



in a Linux terminal with an interactive Bash shell, requiring
them to execute command-line operations to complete multistep real-world tasks; (2) **SWE-Bench-Verified** (Jimenez
et al., 2023), which assesses software engineering on real
GitHub projects, where agents must localize bugs, implement patches, and satisfy the provided test suites under
realistic coding environment; and (3) **GAIA** (Mialon et al.,
2023) validation set, a generalist benchmark that tests an
agent’s ability to solve real-world tasks requiring multi-step
reasoning and tool use. We report pass@1 and pass@3 for
all benchmarks respectively. We report more details about
how we use these datasets for evaluation in Appendix A.1.
We also detail the tools we used for each benchmark in
Appendix D.


**Model & Baselines.** We compare our method against representative frameworks: (1) **ReAct** (Yao et al., 2022), a simple
single-agent system directly build on ReAct that interleaves
reasoning and actions; (2) **OpenHands** (Wang et al., 2024),
a commonly-used open agent platform for solving diverse
real-world tasks; (3) **mini-SWE-agent** (Yang et al., 2024),
a minimalistic coding agent designed to solve GitHub issues and more; and (4) **Claude Code** (Anthropic, 2025), a
production-grade agentic CLI that supports spawning predefined sub-agents for task decomposition and context isolation. For each agentic system, we employ the following frontier language models, including two strong models
(Gemini-3-Flash and DeepSeek-V3.2 (Liu et al.,
2025a)) and a smaller model (Claude-4.5-haiku). We
report the implementations of baselines in Appendix A.3.


**Implementation.** Across all experiments, we set
_max_ ~~_a_~~ _ttempt_ = 10 for the orchestrator and _max_ ~~_s_~~ _tep_ =



50 for the sub-agent. We set _max_ ~~_s_~~ _tep_ = 500 for all baselines for a fair comparison. For the training-free setting,
we detail our designs in Appendix B, which includes all
prompts for the orchestrator and sub-agent we use across
three benchmarks. After the sub-agents complete their tasks,
a reviewer LLM reviews the execution trace and summarizes
the core insights.


For SFT training, we fine-tune Qwen3-8B (Yang et al.,
2025) to improve its orchestration capability in non-thinking
mode. We use TaskCraft (Shi et al., 2025a) as the seed
dataset and employ Gemini-3-Flash to collect 2K orchestration trajectories for SFT training. During SFT, we perform full-parameter fine-tuning under LLamaFactory framework (Zheng et al., 2024) for 2 epochs with a learning rate
of 1e-5, with more details in Appendix A.2.


For in-context learning, we use Claude Sonnet 4.5 as
an optimization model to iteratively update the Orchestrator
instruction. We run 5 optimization rounds; in each round,
we collect 6 interaction trajectories for analysis. After each
round, the prompt that achieves the best cost–performance
trade-off (highest performance with lower cost) is selected
for initializing the next round.


**4.2. Main Results**


Table 1 presents the main results of AORCHESTRA compared to baseline agentic systems on three benchmarks
(GAIA, Terminal-Bench 2.0, and SWE-Bench-Verified),
evaluated by pass@1/pass@3 metric. For AORCHESTRA,
we use Gemini-3-Flash as the orchestrator and use only
one model as sub-agent choices here for comparison. Overall, we find that AORCHESTRA consistently outperforms the



6


**AORCHESTRA:** **Automating Sub-Agent Creation for Agentic Orchestration**



baselines on all environments. AORCHESTRA outperforms
the best baselines by an average of 22.13% pass@1 with
Gemini-3-Flash across three benchmarks.


**GAIA Results** GAIA measures the ability of a generalpurpose agent to solve real-world tasks, such as multihop searching, file processing, and multimodal operations. In such an environment, AORCHESTRA achieves
the strongest performance against all baselines. Specifically,
with Gemini-3-Flash as both the orchestrator and the
sub-agent model, AORCHESTRA achieves 80.00 pass@1
and 86.06 pass@3, which represents the best performance
among all baselines. Under the same Gemini-3-Flash
backbone, AORCHESTRA raises pass@1 by 13.94 points absolute over the strongest baseline framework, OpenHands,
increasing the result from 66.06 to 80.00. Even with a less
powerful model Claude-4.5-haiku as the sub-agent
model, it still attains 60.61 pass@1 on GAIA, confirming
that the observed improvements are not confined to the most
capable model configuration. We do not evaluate Claude
Code for GAIA because it is designed as a production-level
coding agent, and thus its corresponding result is left blank.
We present a case study on GAIA in Appendix C.


**Terminal-Bench** **2.0** **Results** Terminal-Bench assesses
an agent’s ability to operate in computer terminal environments inspired by real-world workflows. On this benchmark,
AORCHESTRA with Gemini-3-Flash achieves 52.86
pass@1 and 57.14 pass@3. This is an absolute improvement of 64.29 points in pass@1 over the strongest baseline
in Table 1, Mini-SWE with 34.29 pass@1. Beyond the
Gemini-3-Flash setting, AORCHESTRA remains competitive under other backbones, with performance that is
comparable to or better than specialized coding agentic systems such as Claude Code.


**SWE-Bench-Verified Results** SWE-Bench-Verified evaluates an agent’s ability to resolve real issues in open-source
repositories by producing code patches that pass the provided tests. On this benchmark, AORCHESTRA achieves
strong performance across backbones and is competitive
with the best baseline systems. With Gemini-3-Flash,
AORCHESTRA reaches 82.00 pass@1 and 86.00 pass@3,
outperforming ReAct and OpenHands under the same
model setting. Compared with Mini-SWE, which is designed for software tasks, AORCHESTRA remains competitive, and it consistently achieves over 70.00 pass@1 across
all three model backbones.


**4.3. Advantage Analysis of AORCHESTRA**


In this section, we present analyses that demonstrate the
benefits of AORCHESTRA for dynamically creating specialized sub-agents, particularly in terms of working mem


_Table 2._ Context-control ablation for sub-agent invocation. We
isolate the effect of context inheritance by only changing the
Context field passed to sub-agents, while keeping the sub-agent
model, tools, and system prompt identical across settings.


**Setting** **Level 1** **Level 2** **Level 3** **Avg.**


No-Context 89.47 81.48 75.00 86.00
Full-Context 94.74 77.78 75.00 84.00
**Ours** **100.00** **88.89** **75.00** **96.00**


ory and capabilities. Overall, our findings indicate that explicitly passing context from the orchestrator to sub-agents
yields performance gains (Sec. 4.3.1). We also show that
selecting different models for different tasks can achieve a
cost-performance Pareto (Sec. 4.3.2), and that diverse implementations of sub-agents consistently contribute to overall
improvement (Sec. 4.3.3)


4.3.1. ADVANTAGE 1: CONTEXT SHARING


In AORCHESTRA, the orchestrator explicitly and dynamically passes curated context to each created sub-agent. To
evaluate the effectiveness of this design, we compare it with
two variants: **No-Context**, where each sub-agent only receives a task instruction, and **Full-Context**, where each
sub-agent inherits all context from the main agent. Note
that these two approaches are also commonly used in prior
systems (Sun et al., 2025; Anthropic, 2025). Here, we conduct analysis on GAIA, and sample 50 samples from the
validation set.


Table 2 indicates that it is necessary to regard context as an
important component of sub-agent and abstract it into one of
the four tuples. In particular, we find that No-Context fails
due to the lack of critical execution traces and fine-grained
cues from previous steps, whereas Full-Context often introduces irrelevant information and aggravates context degradation. In contrast, by allowing the orchestrator to select and
compress only task-relevant history, our method provides a
cleaner context and achieves the highest score.


4.3.2. ADVANTAGE 2: A LEARNABLE ORCHESTRATOR


**Supervised fine-tuning (SFT) for task orchestration** A
practical consideration of AORCHESTRA is that orchestration quality depends on the main agent’s ability to
decompose goals and synthesize high-quality delegation
tuples. To probe this sensitivity, we replace the main
agent with a weaker model, Qwen3-8B, while keeping
Gemini-3-Flash as the sub-agent executor. As shown
in Table 3, this setting (OURS (QWEN3-8B)) achieves
56 _._ 97% accuracy at $0.36 average cost. While worse than
using a strong main agent (OURS with Gemini-3-Flash
reaches 80 _._ 00%), it still surpasses Gemini-3-Flash
with ReAct. This gap suggests that the orchestration is



7


**AORCHESTRA:** **Automating Sub-Agent Creation for Agentic Orchestration**



_Table 3._ Main results. ReAct is evaluated with a single specified
LM per run, while other systems may use either a single LM or a
mixed-LM pool. ICL denotes context learning.


**System** **LM** **Acc.** **Avg.** **Cost**


Claude-4.5-sonnet 53.93 0.190
ReAct Claude-4.5-haiku 47.88 0.066
Gemini-3-Flash 49.09 0.070
GPT-5-mini 54.55 0.052
Deepseek-v3.2 46.70 0.027



Ours



Gemini-3-Flash **80.00** 0.79
Claude-4.5-sonnet 71.52 0.91
GPT-5-mini 67.27 0.28
Deepseek-v3.2 67.87 0.14



Ours (Gemini-3-Flash) Mixed 72.12 0.70
Ours (ICL) Mixed **75.15** **0.57**


Ours (Qwen3-8B) Gemini-3-Flash 56.97 0.36
Ours (SFT) Gemini-3-Flash **68.48** **0.68**


Performance vs. Cost



80


70


60











50


40





|Col1|Col2|Gemini-3-Flash|Col4|
|---|---|---|---|
|Pareto Front||Gemini-3-Flash<br>|Gemini-3-Flash<br>|
|||Deepseek-V3.2<br>Mixed Mo<br>gpt-5-mini<br>~~Mixed(Learned)~~|Deepseek-V3.2<br>Mixed Mo<br>gpt-5-mini<br>~~Mixed(Learned)~~|
|Gem<br>Deepseek-V3.2|Gem<br>Deepseek-V3.2|ini-3-Flash<br>Claude-4.5-haiku<br><br>Claude-4-5-sonnet<br>~~Gemini-3-Flash~~|ini-3-Flash<br>Claude-4.5-haiku<br><br>Claude-4-5-sonnet<br>~~Gemini-3-Flash~~|
|gpt-5-mini<br>ek-V3.2|gpt-5-mini<br>ek-V3.2|Claude-4-5-sonnet<br><br><br>|Claude-4-5-sonnet<br><br><br>|
|Claude-4.5-haiku<br>pseek-V3.2|Claude-4.5-haiku<br>pseek-V3.2|Gemini-3-Flash|ReAct<br>Openhands<br>MiniSwe|
|Claude-4.5-haik|Claude-4.5-haik|u|Ours|
|||1<br>|1<br>|


Avg. Cost ($) in Log Scale



_Figure_ _4._ **Pareto** **front** **curve** **of** **GAIA.** We plot GAIA accuracy and average cost per task (USD, log scale). Each point corresponds to a configuration, and the dashed curve indicates the
Pareto frontier formed by AORCHESTRA across different model
routing choices.


useful even just with a weak 8B model. We then fine-tune
Qwen3-8B for orchestration via SFT, which yields a large
improvement from 56 _._ 97% to 68 _._ 48% (Table 3), though this
gain comes with an increase of $0.32 in average cost per
task. By analyzing execution traces, we find that the finetuned model exhibits stronger long-horizon problem-solving
capabilities when handling complex tasks, increasing the total number of attempts by 56% compared to the base model.
This gain indicates that orchestration is a learnable skill that
can be efficiently improved.


**In-context Learning for Cost-aware Orchestration** Another advantage of AORCHESTRA is the ability to balance
cost and performance through step-wise model routing. Table 3 shows that using different sub-agent models leads to
markedly different accuracy–cost profiles, making it important for the orchestrator to be sensitive to such tradeoffs. We therefore apply a Pareto-oriented context learn


_Table 4._ Evaluating plug-and-play sub-agents with a fixed orchestrator. We use Gemini-3-Flash to test the robustness and reusability
of different sub-agent implementations.


**System** **Easy** **Medium** **Hard** **Acc**


**Standalone baselines**


ReAct 50.00 34.09 16.67 28.57
Mini-SWE-Agent 50.00 40.91 20.83 34.29
Claude Code 50.00 41.86 16.67 32.86


**Orchestrator with plug-in sub-agents**


ReAct-style sub-Agent 50.00 **63.63** 20.83 **48.57**
Mini-SWE-style sub-Agent **100.00** 47.73 **33.33** 44.29


ing procedure that iteratively optimizes the Orchestrator
instruction from interaction trajectories with both performance and monetary cost feedback. The resulting policy
improves AORCHESTRA while reducing cost: under the
mixed-model setting, Ours (ICL) improves accuracy from
72 _._ 12% to 75 _._ 15% while lowering average cost from $0.70
to $0.57 (Table 3), demonstrating that simple prompt-level
learning can jointly enhance performance and efficiency. At
the system level, Figure 4 further shows that AORCHES
TRA naturally yields strong Pareto-efficient operating points:
across different model choices, our configurations form the
Pareto frontier, indicating a systematically improved cost–
performance trade-off over the baselines.


4.3.3. ADVANTAGE 3: PLUG-AND-PLAY SUB-AGENTS


Here, we aim to verify the framework-level pluggability of our approach. Specifically, we replace the execution backend of the sub-agent with different agent
frameworks, such as ReAct-style and Mini-SWE-style
with Gemini-3-Flash as the orchestrator on TerminalBench, following the setups in Appendix A.1.


Table 4 shows that when different sub-agent backends are
used, AORCHESTRA maintains stable performance and consistently outperforms the corresponding baselines. This
design allows sub-agents to be as pluggable modules, enabling the system to remain robust without depending on
any particular sub-agent implementation.


**5. Conclusion**


In this work, we present AORCHESTRA, an orchestrationcentric agentic system that automates sub-agent creation
through a unified four-tuple interface (Instruction, Context,
Tools, Model) to solve complex, long-horizon agentic tasks.
By treating sub-agents as dynamically creatable units, the
orchestrator can spawn task-tailored executors on demand
with specialized working memory (instruction, context) and
capabilities (model, tools).


This abstraction brings practical benefits: it enables on


8


**AORCHESTRA:** **Automating Sub-Agent Creation for Agentic Orchestration**



demand specialization with task-sufficient context, keeps
sub-agents plug-and-play across implementations. The
decoupling of abstraction from execution makes it learnable, and we present two ways to optimize the orchestrator
through supervised fine-tuning and context learning. Empirically, AORCHESTRA demonstrates strong and consistent
improvements across three challenging benchmarks (GAIA,
Terminal-Bench, and SWE-Bench-Verified) when paired
with frontier models like Gemini-3-Flash. It significantly
outperforms established baseline frameworks, achieving, for
instance, an average gain of 16.28% points in pass@1 across
all benchmarks. These results validate the effectiveness of
our orchestration-centric approach to automating complex,
long-horizon tasks.


**References**


Anthropic. Claude code: Subagents - modular ai
workflows with isolated agent contexts, 2025. URL
[https://docs.anthropic.com/en/docs/](https://docs.anthropic.com/en/docs/claude-code/sub-agents)
[claude-code/sub-agents.](https://docs.anthropic.com/en/docs/claude-code/sub-agents)


Chen, G., Dong, S., Shu, Y., Zhang, G., Sesay, J., Karlsson, B. F., Fu, J., and Shi, Y. Autoagents: A framework for automatic agent generation. _arXiv_ _preprint_
_arXiv:2309.17288_, 2023.


Fang, T., Zhang, Z., Wang, X., Wang, R., Qin, C., Wan,
Y., Ma, J.-Y., Zhang, C., Chen, J., Li, X., et al. Cognitive kernel-pro: A framework for deep research agents
and agent foundation models training. _arXiv_ _preprint_
_arXiv:2508.00414_, 2025.


Gao, H.-a., Geng, J., Hua, W., Hu, M., Juan, X., Liu, H., Liu,
S., Qiu, J., Qi, X., Wu, Y., et al. A survey of self-evolving
agents: On path to artificial super intelligence. _arXiv_
_preprint arXiv:2507.21046_, 2025a.


Gao, M., Li, Y., Liu, B., Yu, Y., Wang, P., Lin, C.-Y., and
Lai, F. Single-agent or multi-agent systems? why not
both? _arXiv preprint arXiv:2505.18286_, 2025b.


Grand, G., Tenenbaum, J. B., Mansinghka, V. K., Lew,
A. K., and Andreas, J. Self-steering language models.
_arXiv preprint arXiv:2504.07081_, 2025.


Hong, K., Troynikov, A., and Huber, J. Context rot:
How increasing input tokens impacts llm performance.
Technical report, Chroma, July 2025. URL [https:](https://research.trychroma.com/context-rot)
[//research.trychroma.com/context-rot.](https://research.trychroma.com/context-rot)


Hong, S., Zhuge, M., Chen, J., Zheng, X., Cheng, Y., Wang,
J., Zhang, C., Wang, Z., Yau, S. K. S., Lin, Z., et al.
Metagpt: Meta programming for a multi-agent collaborative framework. In _The twelfth international conference_
_on learning representations_, 2023.



Hu, M., Zhou, Y., Fan, W., Nie, Y., Xia, B., Sun, T., Ye, Z.,
Jin, Z., Li, Y., Chen, Q., et al. Owl: Optimized workforce
learning for general multi-agent assistance in real-world
task automation. _arXiv preprint arXiv:2505.23885_, 2025.


Jimenez, C. E., Yang, J., Wettig, A., Yao, S., Pei, K., Press,
O., and Narasimhan, K. Swe-bench: Can language models resolve real-world github issues? _arXiv_ _preprint_
_arXiv:2310.06770_, 2023.


Li, B., Chen, C., Xue, Z., Mei, Y., and Luo, Y. Deepeye-sql:
A software-engineering-inspired text-to-sql framework.
_CoRR_, abs/2510.17586, 2025a.


Li, B., Zhang, J., Fan, J., Xu, Y., Chen, C., Tang, N., and
Luo, Y. Alpha-sql: Zero-shot text-to-sql using monte
carlo tree search. In _ICML_ . OpenReview.net, 2025b.


Li, W., Lin, J., Jiang, Z., Cao, J., Liu, X., Zhang, J., Huang,
Z., Chen, Q., Sun, W., Wang, Q., et al. Chain-of-agents:
End-to-end agent foundation models via multi-agent distillation and agentic rl. _arXiv preprint arXiv:2508.13167_,
2025c.


Lin, X., Qi, Y., Zhu, Y., Palpanas, T., Chai, C., Tang, N.,
and Luo, Y. LEAD: iterative data selection for efficient
LLM instruction tuning. _CoRR_, abs/2505.07437, 2025.


Liu, A., Mei, A., Lin, B., Xue, B., Wang, B., Xu, B., Wu,
B., Zhang, B., Lin, C., Dong, C., et al. Deepseek-v3.
2: Pushing the frontier of open large language models.
_arXiv preprint arXiv:2512.02556_, 2025a.


Liu, B., Li, X., Zhang, J., Wang, J., He, T., Hong, S., Liu,
H., Zhang, S., Song, K., Zhu, K., et al. Advances and
challenges in foundation agents: From brain-inspired intelligence to evolutionary, collaborative, and safe systems.
_arXiv preprint arXiv:2504.01990_, 2025b.


Liu, X., Shen, S., Li, B., Ma, P., Jiang, R., Zhang, Y., Fan, J.,
Li, G., Tang, N., and Luo, Y. A survey of text-to-sql in the
era of llms: Where are we, and where are we going? _IEEE_
_Trans. Knowl. Data Eng._, 37(10):5735–5754, 2025c.


Mialon, G., Fourrier, C., Wolf, T., LeCun, Y., and Scialom,
T. Gaia: a benchmark for general ai assistants. In _The_
_Twelfth International Conference on Learning Represen-_
_tations_, 2023.


Schroeder, P., Morgan, N. W., Luo, H., and Glass, J. Thread:
Thinking deeper with recursive spawning. In _Proceedings_
_of the 2025 Conference of the Nations of the Americas_
_Chapter of the Association for Computational Linguistics:_
_Human Language Technologies (Volume 1:_ _Long Papers)_,
pp. 8418–8442, 2025.



9


**AORCHESTRA:** **Automating Sub-Agent Creation for Agentic Orchestration**



Shao, Z., Wang, P., Zhu, Q., Xu, R., Song, J., Bi, X., Zhang,
H., Zhang, M., Li, Y., Wu, Y., et al. Deepseekmath: Pushing the limits of mathematical reasoning in open language
models. _arXiv preprint arXiv:2402.03300_, 2024.


Shi, D., Cao, J., Chen, Q., Sun, W., Li, W., Lu, H., Dong, F.,
Qin, T., Zhu, K., Liu, M., et al. Taskcraft: Automated generation of agentic tasks. _arXiv preprint arXiv:2506.10055_,
2025a.


Shi, Y., Wang, M., Cao, Y., Lai, H., Lan, J., Han, X.,
Wang, Y., Geng, J., Li, Z., Xia, Z., et al. Aime: Towards fully-autonomous multi-agent framework. _arXiv_
_preprint arXiv:2507.11988_, 2025b.


Su, H., Diao, S., Lu, X., Liu, M., Xu, J., Dong, X., Fu, Y.,
Belcak, P., Ye, H., Yin, H., et al. Toolorchestra: Elevating
intelligence via efficient model and tool orchestration.
_arXiv preprint arXiv:2511.21689_, 2025.


Sun, W., Lu, M., Ling, Z., Liu, K., Yao, X., Yang, Y., and
Chen, J. Scaling long-horizon llm agent via contextfolding. _arXiv preprint arXiv:2510.11967_, 2025.


Team, T. T.-B. Terminal-bench: A benchmark for ai
agents in terminal environments, Apr 2025. URL
[https://github.com/laude-institute/](https://github.com/laude-institute/terminal-bench)
[terminal-bench.](https://github.com/laude-institute/terminal-bench)


Wang, X., Li, B., Song, Y., Xu, F. F., Tang, X., Zhuge, M.,
Pan, J., Song, Y., Li, B., Singh, J., et al. Openhands: An
open platform for ai software developers as generalist
agents. _arXiv preprint arXiv:2407.16741_, 2024.


Wu, Q., Bansal, G., Zhang, J., Wu, Y., Li, B., Zhu, E., Jiang,
L., Zhang, X., Zhang, S., Liu, J., et al. Autogen: Enabling
next-gen llm applications via multi-agent conversations.
In _First Conference on Language Modeling_, 2024.


Xu, Z., Li, R., Li, J., Weng, R., Wang, J., Cai, X., and Wang,
X. Unlocking implicit experience: Synthesizing tool-use
trajectories from text. _arXiv preprint arXiv:2601.10355_,
2026.


Yang, A., Li, A., Yang, B., Zhang, B., Hui, B., Zheng, B.,
Yu, B., Gao, C., Huang, C., Lv, C., et al. Qwen3 technical
report. _arXiv preprint arXiv:2505.09388_, 2025.


Yang, J., Jimenez, C. E., Wettig, A., Lieret, K., Yao, S.,
Narasimhan, K. R., and Press, O. SWE-agent: Agentcomputer interfaces enable automated software engineering. In _The_ _Thirty-eighth_ _Annual_ _Conference_ _on_
_Neural_ _Information_ _Processing_ _Systems_, 2024. URL
[https://arxiv.org/abs/2405.15793.](https://arxiv.org/abs/2405.15793)


Yao, S., Zhao, J., Yu, D., Du, N., Shafran, I., Narasimhan,
K. R., and Cao, Y. React: Synergizing reasoning and
acting in language models. In _The eleventh international_
_conference on learning representations_, 2022.



Yao, S., Shinn, N., Razavi, P., and Narasimhan, K. _τ_ -bench:
A benchmark for tool-agent-user interaction in real-world
domains. _arXiv preprint arXiv:2406.12045_, 2024.


Zhang, J., Xiang, J., Yu, Z., Teng, F., Chen, X., Chen, J.,
Zhuge, M., Cheng, X., Hong, S., Wang, J., et al. Aflow:
Automating agentic workflow generation. _arXiv preprint_
_arXiv:2410.10762_, 2024.


Zhang, J., Peng, Y., Kong, F., Cheng, Y., Wu, Y., Yu, Z., Xiang, J., Ruan, J., Wang, J., Song, M., et al. Autoenv: Automated environments for measuring cross-environment
agent learning. _arXiv preprint arXiv:2511.19304_, 2025a.


Zhang, W., Cui, C., Zhao, Y., Liu, Y., and An, B.
Agentorchestra: A hierarchical multi-agent framework
for general-purpose task solving. _arXiv_ _preprint_
_arXiv:2506.12508_, 2025b.


Zheng, Y., Zhang, R., Zhang, J., Ye, Y., Luo, Z., Feng, Z.,
and Ma, Y. Llamafactory: Unified efficient fine-tuning of
100+ language models. _arXiv preprint arXiv:2403.13372_,
2024.


Zhu, H., Qin, T., Zhu, K., Huang, H., Guan, Y., Xia, J., Yao,
Y., Li, H., Wang, N., Liu, P., et al. Oagents: An empirical study of building effective agents. _arXiv_ _preprint_
_arXiv:2506.15741_, 2025a.


Zhu, Y., Wang, L., Yang, C., Lin, X., Li, B., Zhou, W., Liu,
X., Peng, Z., Luo, T., Li, Y., Chai, C., Chen, C., Di, S.,
Fan, J., Sun, J., Tang, N., Tsung, F., Wang, J., Wu, C., Xu,
Y., Zhang, S., Zhang, Y., Zhou, X., Li, G., and Luo, Y. A
survey of data agents: Emerging paradigm or overstated
hype? _CoRR_, abs/2510.23587, 2025b.



10


**AORCHESTRA:** **Automating Sub-Agent Creation for Agentic Orchestration**


**A. Implemention Details**


**A.1. Datasets**


  - **GAIA** (Mialon et al., 2023): GAIA benchmarks general AI assistants on realistic, tool-augmented questions (often
involving web browsing and multi-step reasoning). We evaluate AORCHESTRA and compare with other baselines on
the GAIA validation split, which contains a total of 165 tasks.


  - **Terminal** **Bench** **2.0** (Team, 2025): Terminal-Bench evaluates agents on end-to-end, real-world workflows in a
sandboxed command-line environment, graded by executable tests. We evaluate AORCHESTRA and compare with
other baselines on the Terminal-Bench2.0 test split, which contains a total of 89 tasks. In the main experiments, we
randomly sample 70 tasks dut to cost reasons.


  - **SWE-Bench-Verified:** (Jimenez et al., 2023) SWE-Bench Verified measures autonomous software engineering by
asking agents to generate patches that resolve real GitHub issues in real repositories, verified by running tests; the
Verified split is human-screened to remove problematic cases. We evaluate AORCHESTRA and compare with other
baselines on the SWE-Bench verified version test split, which contains a total of 500 tasks. We randomly sample 100
tasks for evaluation due to cost reasons.


**A.2. SFT Hyper-parameters.**


We use the following hyperparameters during the experiments in Table 5.

|Hyperparams|Values|Hyperparams|Values|
|---|---|---|---|
|learning rate<br>warmup ratio<br>lr scheduler<br>epoch<br>Deepspeed|1e-5<br>0.1<br>cosine<br>2<br>zero3|weight decay<br>max length<br>batch size<br>BF16<br>tool-call template|0.05<br>16K<br>64<br>True<br>Hermes|



_Table 5._ SFT Hyperparameters used.


**A.3. Baseline Implementations**


For baseline implementations, we evaluate a diverse set of widely-used agentic frameworks. During our experiment, we
found that Claude Code is not well-suited for GAIA open-world multi-hop question answering due to its architecture
and intended usage pattern. Therefore, we did not report the results of Claude Code in the main experiments.


In addition, we find that DeepSeek-V3.2 exhibits poor native compatibility with CLAUDE CODE based on our initial
investigation and empirical trials. Therefore, we exclude this experiment in Table 1.


For the Terminal-Bench and SWE-Bench evaluations, we leverage the Harbor scaffold to run MiniSWE, OpenHands,
and Claude Code under a unified execution interface.


**B. Prompts**


**B.1. Main Agent Prompts**


B.1.1. GAIA MAIN AGENT PROMPT





11


**AORCHESTRA:** **Automating Sub-Agent Creation for Agentic Orchestration**





B.1.2. TERMINAL-BENCH MAIN AGENT PROMPT







12


**AORCHESTRA:** **Automating Sub-Agent Creation for Agentic Orchestration**





B.1.3. SWE-BENCH MAIN AGENT PROMPT







13


**AORCHESTRA:** **Automating Sub-Agent Creation for Agentic Orchestration**





**B.2. Sub-Agent Prompts**


B.2.1. GAIA SUB-AGENT PROMPT







14


**AORCHESTRA:** **Automating Sub-Agent Creation for Agentic Orchestration**





B.2.2. TERMINAL-BENCH SUB-AGENT PROMPT







15


**AORCHESTRA:** **Automating Sub-Agent Creation for Agentic Orchestration**





B.2.3. SWE-BENCH SUB-AGENT PROMPT







16


**AORCHESTRA:** **Automating Sub-Agent Creation for Agentic Orchestration**





B.2.4. SUB-AGENT SUMMARY PROMPT





**B.3. Learning Prompt**


B.3.1. STRATEGY OPTIMIZE PROMPT







B.3.2. STRATEGY SELECT PROMPT







17


**AORCHESTRA:** **Automating Sub-Agent Creation for Agentic Orchestration**





**C. Case Study**


**C.1. GAIA Case Study**


C.1.1. CASE OVERVIEW


We evaluate AORCHESTRA on 165 tasks from the GAIA benchmark, using Gemini-3-Flash for both the Main Agent and Sub
Agent. The results show that AORCHESTRA exhibit strong orchestration capability and robustness in complex, multi-step
tasks. Across all 165 GAIA tasks, AORCHESTRA achieves an overall success rate of 80 _._ 0%. Performance further stratifies
by difficulty: Level 1 (easy) reaches 88 _._ 7%, Level 2 (medium) reaches 80 _._ 2%, and Level 3 (hard) reaches 61 _._ 5%.


**Long-Horizon Support and Context Stability.** The system successfully completes multiple high-cost tasks with long
interaction chains. For example, task 935e2cff (Level 1) requires 10 attempts with a total cost of $5.93 yet still completes
successfully; task 853c8244 (Level 2) also succeeds after 10 interaction rounds with a cost of $3.06. These cases
demonstrate that the system can maintain context integrity throughout long-horizon execution, mitigating the “context rot”
issue commonly observed in standard LLM-based long dialogs.


**Strong Error Recovery.** We find a key strength of AORCHESTRA is its self-correction mechanism. On Level 3 hard tasks,
8131e2c0 and 0512426f succeed after 10 attempts, 983bba7c succeeds after 9 attempts, and 872bfbb1 succeeds
after 8 attempts. This indicates that even when initial plans fail, the system can progressively converge to the correct answer
via Main-Agent reflection and replanning, coupled with iterative execution by Sub Agents. In total, 34 tasks are successfully
completed after more than five attempts, highlighting strong error recovery capability.


Here we present a representative case study to illustrate how the proposed hierarchical orchestration mechanism operates in
practice.


The task is a **Level-2** question from the GAIA benchmark, asking the agent to identify the 2015 Metropolitan Museum of
Art exhibition titled after the Chinese zodiac animal of that year, and count how many figures in the “twelve animals of the
Chinese zodiac” set have a visible hand. The expected answer is **11** .


Our orchestrator successfully solved this task in **10 attempts** through three key phases of iterative refinement:


**(i)** **Error** **Correction** **via** **Feedback** **Loop.** In Attempt 1, the main agent initially hypothesized incorrect accession
numbers (1975.1.784-795) based on prior knowledge. After the sub-agent reported these were unrelated artworks, the
orchestrator _proactively corrected_ the hypothesis in Attempt 2, explicitly instructing: _“Do not use 1975.1.784-795 as they_
_are unrelated drawings.”_ This demonstrates the system’s ability to learn from sub-agent failures and refine task instructions
accordingly.


**(ii) Key Finding Extraction and Propagation.** In Attempt 5, although the sub-agent timed out, it discovered a critical
piece of evidence: _“The snake’s hands are hidden in long, loose sleeves.”_ The orchestrator extracted this partial result and
persisted it into the context for Attempt 6, writing: _“Previous analysis suggested the snake (02.18.730f) has hands hidden in_
_sleeves.”_ This illustrates how our architecture preserves and propagates valuable intermediate findings across attempts.


**(iii) Hypothesis Formation and Confident Convergence.** By Attempt 7, the orchestrator synthesized accumulated evidence
to form a concrete hypothesis: the answer is likely 11 (all figures except the snake). Rather than immediately committing,
it delegated additional verification tasks to confirm whether any other figures (e.g., monkey, dog, pig) might have “paws”
instead of “hands.” Finally, in Attempt 10, with sufficient corroborating evidence, the orchestrator confidently issued the
complete action with the correct answer.


18


**AORCHESTRA:** **Automating Sub-Agent Creation for Agentic Orchestration**


C.1.2. DETAILED CASE


Below is the detailed parameters of Main Agent decision of each attempt:





19


**AORCHESTRA:** **Automating Sub-Agent Creation for Agentic Orchestration**









20


**AORCHESTRA:** **Automating Sub-Agent Creation for Agentic Orchestration**





21


**AORCHESTRA:** **Automating Sub-Agent Creation for Agentic Orchestration**









22


**AORCHESTRA:** **Automating Sub-Agent Creation for Agentic Orchestration**





**D. Tools And Action Space**


This appendix details the action space of the AORCHESTRA framework, including the actions available to the Main Agent
and Sub-Agents, as well as the tool inventory and execution constraints for each benchmark.


**D.1. Main Agent Action Space**


The Main Agent is responsible for global task planning and subtask delegation. Its action space consists of two core actions.


**delegate** ~~**t**~~ **ask.** This action delegates a well-scoped subtask to a specialized Sub-Agent. The parameter schema is
defined as follows:


**complete.** This action submits the final answer and terminates the task.







**D.2. Sub-Agent Tools For each Benchmark**


Table 6 summarizes the tools available to Sub-Agents in each benchmark and their corresponding constraints.


D.2.1. GAIA TOOLS


In the GAIA benchmark, Sub-Agents are equipped with tools for web retrieval, code execution, and multimodal analysis.


  - **GoogleSearchAction.** Performs web search via the Serper API.


23


**AORCHESTRA:** **Automating Sub-Agent Creation for Agentic Orchestration**


_Table 6._ Tool inventory and constraints per benchmark.


**Benchmark** **Tool Name** **Constraints / Notes**



GAIA



GoogleSearchAction Serper API; max 5 results; 30s timeout
ExtractUrlContentAction Jina API; chunked for long pages; 50s timeout
ExecuteCodeAction Sandboxed in workspace/temp; 10s timeout
ImageAnalysisAction Vision LLM backend; supports URL & local
files
ParseAudioAction Audio-capable LLM backend; multi-format
support
finish Reports result/status to the Main Agent



execute Shell commands in Docker/E2B sandbox
Terminal-Bench finish Reports progress without triggering tests



SWE-Bench



execute Shell commands in a Docker container
view ~~f~~ ile Reads a file with line-range specification
edit ~~f~~ ile File editing via string replacement
finish Reports progress to main agent




- **ExtractUrlContentAction.** Extracts webpage content via the Jina API.






- **ExecuteCodeAction.** Executes Python or Bash code in a sandboxed environment.






- **ImageAnalysisAction.** Calls a vision-capable LLM backend to analyze images.






- **ParseAudioAction.** Calls an audio-capable LLM backend to process audio inputs.






- **finish.** Reports subtask results back to the Main Agent.





D.2.2. TERMINAL-BENCH TOOLS


In Terminal-Bench, Sub-Agents execute shell commands inside Docker/E2B sandboxes using the following tools:


  - **execute:** run shell commands and return outputs.


  - **finish:** report intermediate progress without triggering tests.


24


**AORCHESTRA:** **Automating Sub-Agent Creation for Agentic Orchestration**


D.2.3. SWE-BENCH TOOLS


In SWE-Bench, Sub-Agents are equipped with code navigation and editing capabilities:


  - **execute:** run shell commands (e.g., git operations and tests).


  - **view** ~~**f**~~ **ile:** read file content with a specified line range.


  - **edit** ~~**f**~~ **ile:** edit files via string replacement.


  - **finish:** Report your progress back to MainAgent.


**D.3. Sandbox and Network Constraints**


**Code Execution Sandbox.** ExecuteCodeAction executes code in an isolated directory (workspace/temp). Potentially destructive Bash operations are disallowed, including file deletion, privilege escalation, permission changes,
root-level redirection, and system-level commands. The default execution timeout is 10 seconds.


**Network Constraints.** Web access is mediated exclusively through tool APIs. Web search is performed via the Serper
API (google.serper.dev) with a 30-second timeout, while URL content extraction is handled via the Jina API
(r.jina.ai) with a 50-second timeout. Raw HTTP requests are not directly exposed to agents.


**Terminal-Bench Sandbox.** Terminal-Bench supports Docker, E2B, and Daytona backends. The default execution timeout
is 600 seconds, and the working directory is automatically inferred from the Dockerfile WORKDIR directive.


**SWE-Bench Sandbox.** Each SWE-Bench task runs in an isolated Docker container. The system automatically clones the
target repository and checks out the specified base commit. Tests are executed with pytest under a 300-second timeout.


**E. Third-Party API and Model Pricing**


**E.1. Third-Party APIs**


We rely on a small set of third-party APIs to support web search and sandboxed agent environment creation/execution.


_Table 7._ Third-party APIs used in our system.


**API** **Role** **How it is used in AORCHESTRA**


**Serper** (serper.dev) Web search Used as the primary search API for retrieving relevant webpages/snippets
during GAIA-style information-seeking subtasks.
**Jina** (jina.ai) Web content retrieval Used for lightweight webpage fetching/reading (e.g., converting a URL into
clean text for extraction) to support search-and-read subtasks.
**E2B** (e2b.dev) Sandbox environment Used to create isolated execution environments for agent tool use (e.g., running code or environment-dependent operations) with controlled resources.


**Usage.** These APIs are invoked only through our tool interface; the main agent and sub-agents do not access external services directly.
**Reproducibility.** When applicable, we cache retrieved web content and log API responses/metadata (e.g., timestamps, query strings,
and URLs) to ensure consistent evaluation.


**E.2. Model Pricing Table and Cost Accounting**


25


**AORCHESTRA:** **Automating Sub-Agent Creation for Agentic Orchestration**





26


