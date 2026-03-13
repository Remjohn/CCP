# **SkillOrchestra: Learning to Route Agents via** **Skill Transfer**

**Jiayu Wang** [1] **, Yifei Ming** [2] **, Zixuan Ke** [2] **, Shafiq Joty** [2] **, Aws Albarghouthi** [1] **, and Frederic Sala** [1]


1 2
University of Wisconsin-Madison, Salesforce AI Research

### **Abstract**


Compound AI systems promise capabilities beyond those of individual models, yet their success depends
critically on effective orchestration. Existing routing approaches face two limitations: (1) input-level routers
make coarse query-level decisions that ignore evolving task requirements; (2) RL-trained orchestrators are
expensive to adapt and often suffer from _routing collapse_, repeatedly invoking one strong but costly option
in multi-turn scenarios. We introduce **`SkillOrchestra`**, a framework for **skill-aware orchestration** . Instead
of directly learning a routing policy end-to-end, **`SkillOrchestra`** learns fine-grained skills from execution
experience and models agent-specific competence and cost under those skills. At deployment, the orchestrator
infers the skill demands of the current interaction and selects agents that best satisfy them under an explicit
performance-cost trade-off. Extensive experiments across ten benchmarks demonstrate that **`SkillOrchestra`**
outperforms SoTA RL-based orchestrators by up to 22.5% with 700× and 300× learning cost reduction
compared to Router-R1 and ToolOrchestra, respectively. These results show that explicit skill modeling enables
scalable, interpretable, and sample-efficient orchestration, offering a principled alternative to data-intensive
RL-based approaches. The code is available at: `[https://github.com/jiayuww/SkillOrchestra](https://github.com/jiayuww/SkillOrchestra)` .

### **1. Introduction**

































**Figure 1:** Performance-cost tradoffs in multi-turn model routing (left) and agent orchestration (right). SkillOrchestra
and SkillOrchestra+ lie on the Pareto frontier, with higher accuracy at lower cost than all baselines.


Modern AI systems are increasingly built as compound agents that coordinate multiple large language models
(LLMs) and tools to solve complex, multi-step tasks such as deep research (Gemini, 2024, OpenAI, 2025b)
and scientific discovery (Gottweis et al., 2025). Instead of relying on a single model, these systems interleave
operations such as web search, code execution, and answer synthesis, dynamically invoking models with
different strengths and costs (Ke et al., 2025). In this setting, _orchestration_, the process deciding what
capability is required at each interaction state and which model–tool combination to invoke, is central to


_Correspondence:_ _Jiayu Wang:_ _milawang@cs.wisc.edu_


SkillOrchestra: Learning to Route Agents via Skill Transfer



Model Routing



Direct Agent Orchestration





















Single-turn/static selection

No dynamic mode/tool selection

















Explicit skill-level capability modeling



**Figure 2:** Comparison of model routing and agent orchestration approaches. **(Left)** Model routing performs static,
query-level model selection without dynamic mode or tool reasoning. **(Middle)** Direct agent orchestration learns
routing end-to-end with implicit capability modeling and is prone to routing collapse. **(Right)** Skill-aware agent
orchestration leverages a reusable Skill Handbook with explicit skill-level capability modeling, enabling balanced agent
utilization and extensibility.


both performance and efficiency.


A common form of orchestration is model routing, where a controller selects a model from a model pool (Chen
et al., 2024a, Hu et al., 2024, Ong et al., 2025). However, existing routing methods are often ill-suited
to modern agentic workloads. Most routers make single-shot, query-level decisions, assuming one model
suffices for the entire task. This assumption breaks down in multi-turn interactions, where different states
require distinct capabilities. Agentic workflows often interleave operational modes (e.g., web search and
coding), each demanding different skills. Routing should therefore operate at the level of fine-grained
capability requirements conditioned on the current interaction state, rather than treating the entire query as
a single decision unit (Figure 2, left). Recent RL-based orchestration methods (Zhang et al., 2025a, Su et al.,
2025) address this by learning sequential routing policies with LLMs. While more flexible, these approaches
introduce new challenges: expensive training, limited adaptability to evolving model and tool pools, and a
tendency toward what we term _routing collapse_ : the degeneration of the orchestration policy into repeatedly
selecting a single option at one or more decision levels (e.g., agent type or backbone model), despite the
availability of alternatives with better accuracy-cost trade-offs (Figure 2, middle).


To address these limitations, we introduce **SkillOrchestra**, a framework for _skill-aware orchestration_ . Rather
than directly optimizing a routing policy end-to-end, SkillOrchestra learns a reusable Skill Handbook from
execution experience. The handbook encodes (i) mode-level execution insights that guide what operation
should be performed at each interaction state, (ii) fine-grained skills that characterize capability requirements
within each mode, and (iii) agent profiles that summarize skill-conditioned performance, cost characteristics,
and practical usage insights. At deployment, the orchestrator first selects the appropriate operational mode
conditioned on the current state, then chooses the agent that best satisfies the required skills under an
explicit performance-cost trade-off (Figure 2, right).


2


SkillOrchestra: Learning to Route Agents via Skill Transfer


This skill-centric perspective brings three systemic advantages. First, it enables state-conditioned, fine-grained
orchestration, allowing different models to specialize across capabilities. Second, it promotes stable and
balanced routing behavior, mitigating routing collapse seen in RL-tuned orchestrator. Third, it produces
transferable orchestration knowledge: the learned Skill Handbook can be reused across different orchestrator
backbones and updated model pools, decoupling orchestration knowledge from router parameters.


We evaluate SkillOrchestra in both multi-turn model routing and full agent orchestration settings. As
shown in Figure 1, SkillOrchestra and SkillOrchestra+ lie on the Pareto frontier, achieving higher accuracy
at lower cost than all baselines. Across ten diverse benchmarks, SkillOrchestra consistently outperforms
heuristic, discriminative, and RL-based approaches. For example, SkillOrchestra outperforms SoTA RL-trained
orchestrators, achieving up to 22.5% absolute improvement, with 700× and 300× cost reduction compared
to Router-R1 (Zhang et al., 2025a) and ToolOrchestra (Su et al., 2025), respectively. Moreover, it exhibits
more balanced routing patterns and transfers effectively across orchestrator models without retraining. We
summarize our contributions as follows:


❶ **Skill-aware** **orchestration.** We propose SkillOrchestra, a new paradigm that structures orchestration
decisions around explicit capability abstractions and agent profiles, enabling state-conditioned, performancecost-aware orchestration.


❷ **Skill Handbook learning.** We introduce a data-efficient framework to discover and refine reusable skills
and execution insights from agent traces, while estimating skill-conditioned agent performance and cost.


❸ **Granularity-aware** **skill** **handbook** **selection.** We show that optimal skill granularity depends on
orchestrator capacity, and develop a validation strategy to select orchestrator-specific handbooks that balance
expressiveness and decision reliability under performance-cost trade-offs.


❹ **Empirical gains and transferability.** Extensive experiments across ten benchmarks demonstrate improved
accuracy, efficiency, and routing stability over strong RL-tuned baselines, alleviating routing collapse and
transferring across orchestrator backbones without retraining.

### **2. Related Works**


**Model Routing.** Model routing aims to select the most appropriate model from a pool to balance performance
and inference cost. Early approaches rely on heuristic or cascade strategies (Chen et al., 2024a) that escalate
queries based on predicted difficulty or budget constraints (Ding et al., 2024, Šakota et al., 2024). Prior
approaches are largely heuristic or discriminative, learning static mappings from query features to model
choice (Jiang et al., 2023b) or relying on cascades (Chen et al., 2024a) and difficulty estimation. Instead, a
large body of work learns discriminative query-model matching, using similarity-based methods (Hu et al.,
2024, Ong et al., 2025), neural classifiers or ensembles (Jiang et al., 2023b, Lu et al., 2024), and graph-based
formulations (Feng et al., 2025) to predict which model should answer a query (Chen et al., 2024b, Stripelis
et al., 2024). Despite their effectiveness, routing decisions for these approaches are typically made once per
query using input-level features only, without modeling how model competence differs across intermediate
stages. As a result, they struggle to support fine-grained, multi-step orchestration.


**RL-based Routing and Orchestration.** To enable multi-step decisions, recent work formulates routing as a
sequential decision process and trains an LLM-based router using reinforcement learning (Schulman et al.,
2017, Shao et al., 2024). Systems such as Router-R1 (Zhang et al., 2025a) and ToolOrchestra (Su et al.,


3


SkillOrchestra: Learning to Route Agents via Skill Transfer











































**Figure** **3:** Overview of SkillOrchestra. **(Left)** A global Skill Handbook is constructed by discovering and refining
reusable skills and execution-level insights from agent traces, while jointly estimating each agent’s skill competence and
associated cost. **(Middle)** An orchestrator-specific handbook is selected via Pareto validation to achieve a principled
trade-off between performance and cost. **(Right)** At deployment, the orchestrator performs mode-aware and skillgrounded agent selection using the selected handbook.


2025) that interleave reasoning and routing, optimizing performance-cost trade-offs via trajectory-level
rewards. While more flexible than single-shot routers, RL-based approaches introduce new challenges such
as high training cost, poor adaptability to new model pools or tasks, and policy routing collapse, where the
router converges to repeatedly invoking a single strong but expensive model. In contrast, we introduce _**skill**_
as an intermediate abstraction and construct a reusable Skill Handbook that captures mode-conditioned
competence patterns. This design enables data-efficient, transferable, and more balanced orchestration
without end-to-end RL training.

### **3. Preliminaries**


**Agent Orchestration.** We consider an agentic task environment where a user instruction _q_ ∈ _𝒬_ initiates a
multi-step reasoning process. The system consists of the following components:


[✱] The Orchestrator ( _𝒪_ ): A central controller responsible for high-level planning and resource allocation.

[✱] Operational Modes (Ψ). A set of abstract action modes Ψ = { `search`, `code`, . . . } defined at the capability
level. At each turn, the orchestrator chooses a mode _ψ_ ∈ Ψ that specifies the type of operation required (e.g.,
retrieving external information, or code execution).

[✱] Model Pool ( _ℳ_ ). A set of candidate foundation models _ℳ_ = { _m_ 1, . . ., _mKM_ }, which may include
general-purpose and specialized LLMs (e.g., GPT-5, Claude, Qwen-3, or domain-specific coder and math
models).


4


SkillOrchestra: Learning to Route Agents via Skill Transfer


[✱] Tool Pool ( _𝒯_ ). A set of executable tools _𝒯_ = { _t_ 1, . . ., _tKT_ }, such as web search engines (e.g., Google
Search, Tavily Search), code execution environments (e.g., Python), database retrieval systems, or other
external APIs.


[✱] Agent Instantiation. An _agent_ is defined as a pair


_A_ = ( _m_, _𝒯A_ ), _m_ ∈ _ℳ_, _𝒯A_ ⊆ _𝒯_,


where _m_ is the backbone model and _𝒯A_ is the subset of tools accessible during execution.


Each operational mode _ψ_ ∈ Ψ restricts the allowable tools, inducing a set of valid agents


_𝒜ψ_ = {( _m_, _𝒯A_ ) ∣ _m_ ∈ _ℳ_, _𝒯A_ ⊆ _𝒯ψ_ },


where _𝒯ψ_ ⊆ _𝒯_ denotes the tools relevant to mode _ψ_ .


**Task** **Execution** **Workflow.** Given query _q_, the system evolves over turns _t_ = 0, . . ., _T_ . Let _st_ denote the
system state at turn _t_, which consists of the original query and the accumulated interaction history up to
that point. At each turn, the orchestrator selects a mode _ψt_ ∈ Ψ (what to do) and an agent _At_ ∈ _𝒜ψt_
(who executes it), forming the action _at_ = ( _ψt_, _At_ ). The selected agent produces an execution trace
_zt_ (e.g., search results or generated code), after which the environment returns an observation _ot_ (e.g.,
tool outputs or execution results), leading to the next state _st_ +1. This interaction induces a trajectory
_τ_ = ( _s_ 0, _a_ 0, _z_ 0, _o_ 0, _s_ 1, _a_ 1, _z_ 1, _o_ 1, . . ., _sT_ ). An example multi-step workflow is illustrated in Fig. 3 (right).


**Problem Formulation.** The orchestrator aims to learn a policy _π_ that optimizes performance-cost tradeoffs
over trajectories. Formally, we seek to maximize the expected reward _R_ ( _τ_ ) and minimizing the cumulative
execution cost:



max _J_ ( _τ_ ) = **E** _τ_ ∼ _π_ [ _R_ ( _τ_ ) − _λ_
_π_



_T_
∑ _C_ ( _At_, _zt_ )],

_t_ =0



where _C_ ( _At_, _zt_ ) denotes the cost incurred by the selected agent _At_ when producing trace _zt_ (e.g., token
usage and/or latency), and _λ_ is a tradeoff hyperparameter. We factorize the policy as


_π_ ( _at_ ∣ _st_ ) = _π_ mode( _ψt_ ∣ _st_ ) ⋅ _π_ route( _At_ ∣ _st_, _ψt_ ),


where _π_ mode determines the next operational mode (e.g., _Search_ vs. _Coding_ ), and _π_ route selects the optimal
agent _At_ conditioned on the current state and mode.


Under this formulation, traditional model routing (Hu et al., 2024, Chen et al., 2024b) can be viewed as a
special case with a single timestep _T_ = 0, a single operational mode Ψ = _answer_, and no external tools. The
objective reduces to max _π_ route **E** _A_ ∼ _π_ route(⋅∣ _q_ ) [ _R_ ( _A_, _q_ ) − _λC_ ( _A_, _z_ )], where the state _s_ 0 = _q_ is the user query and
routing consists of choosing one model to generate the final answer in a single step.


Prior work typically instantiates this optimization via RL such as GRPO (Shao et al., 2024) by directly finetuning the orchestrator parameters _θ_ toward the optimal policy (Su et al., 2025). In contrast, **`SkillOrchestra`**
reframes orchestration as a problem of **skill** **acquisition** rather than parameter adaptation. Instead of
updating _θ_, we learn a **Skill Handbook** _ℋ_, a reusable experience base that captures (i) mode-level execution
insights about what operation to perform at a given interaction state, (ii) fine-grained skills that characterize
capability requirements within each mode, and (iii) agent profiles that summarize competence and cost


5


SkillOrchestra: Learning to Route Agents via Skill Transfer


under those skills (e.g., _high-precision arithmetic_, _symbolic logic coding_ ). Under this view, the optimization
shifts from learning a routing policy to identifying the optimal handbook structure:


_ℋ_ [∗] = argmax **E** _τ_ ∼ _π_ (⋅∣ _ℋ_ ) [ _J_ ( _τ_ )] .
_ℋ_


By optimizing the Skill Handbook _ℋ_, we explicitly align abstract task demands with concrete agent capabilities,
enabling the orchestrator to reason over the competence landscape of the agent pool even without costly
end-to-end RL finetuning.

### **4. SkillOrchestra**


**`SkillOrchestra`** reframes orchestration as skill-grounded decision making rather than direct policy optimization. Instead of learning a monolithic routing policy, we learn a structured Skill Handbook that captures
reusable execution knowledge. During training, the handbook is incrementally constructed and refined
from execution traces, including skills, agent profiles, and execution insights. At test time, the orchestrator
consults a selected subset of this handbook to guide mode selection and agent routing.


**Definition 4.1** (Skill) **.** _A skill is a reusable capability abstraction that specifies the type of competence required_
_to perform a task under an operational mode_ _ψ._ _Skills form an intermediate layer between high-level modes_
_(e.g.,_ _`search`_ _,_ _`code`_ _) and individual agents, enabling the system to decouple capability requirements from agent_
_identity._


_Formally, a skill σ is represented as_
_σ_ ≜ ⟨ _𝒟_, _ℐ_ ⟩,


_where 𝒟_ _is a natural-language description of the capability, and ℐ_ _denotes contextual indicators (e.g., keywords,_
_structural patterns, or exemplar queries) that signal when the skill is applicable._


**Definition** **4.2** (Agent Profile) **.** _An agent profile summarizes an agent’s mode-conditioned competence, cost,_
_and routing characteristics for skill-aware orchestration._ _For agent_ _A under operational mode ψ, the profile is_
_defined as_
_𝒫A_, _ψ_ = ({ _ϕA_, _σ_ } _σ_ ∈Σ _ψ_, _C_ [ˆ] _A_ ( _ψ_ ), _ℛA_, _ψ_, Γ _A_ ),

_where_ _ϕA_, _σ_ _denotes the estimated success probability of agent_ _A_ _on skill_ _σ,_ _C_ [ˆ] _A_ ( _ψ_ ) _is the estimated execution_
_cost (e.g., latency, token usage) under mode ψ, ℛA_, _ψ_ _encodes mode-conditioned routing signals such as usage_
_constraints or systematic failures,_ Γ _A_ _provides a high-level summary of the agent’s strengths and weaknesses._


**4.1.** **Agent Orchestration via Skill Handbook**


We now describe runtime orchestration using the Skill Handbook (Fig. 3, right).


**Skill** **Handbook.** The Skill Handbook _ℋ_ organizes reusable orchestration knowledge at three levels: (i)
mode-level execution insights that guide what operation to perform under different interaction states, (ii) a
registry of fine-grained skills that capture capability requirements within each mode, and (iii) agent profiles
that model skill-conditioned competence, routing signals, and execution cost. It can be viewed as a graph
_𝒢ℋ_ = ( _𝒱_, _ℰ_ ), _𝒱_ = _𝒱_ Ψ ∪ _𝒱_ Σ ∪ _𝒱𝒫_ stores mode selection insights, skills, and agent profiles. The edge structure
encodes associations between operational modes and relevant skills.


6


SkillOrchestra: Learning to Route Agents via Skill Transfer

































































**Figure 4:** Example instantiation of a learned Skill Handbook. The handbook decouples capability requirements from
agent identity through three components: (left) mode-level routing insights, (middle) a hierarchical registry of reusable
skills, and (right) agent profiles encoding skill-specific competence estimates and execution cost statistics.


**Example (Skill Handbook Instantiation).** Figure 4 shows a concrete instantiation of _ℋ_ . For example, under
mode _ψ_ = `code`, the handbook stores mode-level metadata (left) capturing when to code. The skill registry
(middle) may include a high-level skill `data_processing`, which further specializes into subskills such
as `symbolic_logic` . Each agent is associated with a profile (right) providing competence estimates over
these skills, mode-conditioned routing signals, and execution cost statistics. Together, these components
enable structured, skill-grounded agent selection.


[✱] **Mode-level metadata** _𝒱_ Ψ **.** For each operational mode _ψ_ ∈ Ψ, the handbook stores mode-level routing
insights _ℛψ_ learned from execution traces, guiding high-level transitions (e.g., when to switch from _Search_
to _Code_ ).


[✱] **Skill** **registry** _𝒱_ Σ **.** The handbook maintains a registry of skills (Definition 4.1), each representing a
task-conditioned capability that may be required during execution.


[✱] **Agent** **profiles** _𝒱𝒫_ **.** Each agent _A_ is associated with an agent profile (Definition 4.2), which stores
agent-specific performance estimates over skills, routing insights of this agent, and cost characteristics. Agent
profiles are queried during routing but are not indexed by graph edges.

[✱] **Mode–skill index** _ℰ_ **.** The graph structure induces a mapping _M_ ∶ Ψ → 2 [Σ], where Σ _ψ_ ∶= _M_ ( _ψ_ ) denotes
the set of skills associated with operational mode _ψ_ . This index restricts routing decisions to mode-consistent
skills without searching over the full skill space at runtime.


**Orchestration with Skill Handbook.** At inference time, the orchestrator interacts with the Skill Handbook
in a task-conditioned manner. Given a user query _q_, the system follows a _retrieval–execution_ cycle.


**Step 1:** **Handbook Selection.** The effectiveness of a handbook depends on how well its structural granularity
aligns with the reasoning capacity of the target orchestrator. Although the learned handbook _ℋ_ [∗] may contain
fine-grained skills and detailed routing insights derived from prior experience, not all such structure is equally
beneficial for every orchestrator.


Fine-grained skill decompositions require accurate inference of which subskill is active in the current interaction state. While a strong orchestrator may reliably distinguish between subskills such as `symbolic_logic`
and `numerical_approximation` under `code` mode, a lower-capacity orchestrator may misidentify the
active skill, introducing routing bias and degrading end-to-end performance. For example, in a coding query re

7


SkillOrchestra: Learning to Route Agents via Skill Transfer


quiring logical constraint verification, activating `numerical_approximation` instead of `symbolic_logic`
may route to an agent specialized in numeric computation but suboptimal for symbolic reasoning. Operating
at a coarser granularity (e.g., using a broader skill such as `data_processing` ) reduces sensitivity to such
misidentification and yields more stable routing decisions.


Starting from the learned handbook _ℋ_ [∗] (Section 4.2), we therefore select an orchestrator-specific subset

( _𝒪_ )
_ℋ_ [This selection determines which skills,]
base [for orchestrator] _[ 𝒪]_ [via Pareto-optimal validation (Section][ 4.3][).]
agent profiles, and routing metadata are retained, as well as their effective granularity, so as to maximize

( _𝒪_ )
end-to-end performance given target orchestrator under a given cost budget. Formally, _ℋ_
base [is an induced]

( _𝒪_ )
subgraph of _ℋ_ [∗] : _ℋ_ base [=][ (] _[𝒱]_ Ψ [base] ∪ _𝒱_ Σ [base] ∪ _𝒱𝒫_ [base], _ℰ_ [base] ), where _𝒱_ Ψ [base] contains mode-level routing metadata
useful for the orchestrator to select operational modes, _𝒱_ Σ [base] contains the skills retained for those modes at
the selected granularity, and _𝒱𝒫_ [base] contains the corresponding agent profiles. The edge set _ℰ_ [base] ⊆ _ℰ_ restricts
mode–skill associations to the retained nodes. All node attributes, including routing insights, performance
estimates, and cost statistics, are inherited from _ℋ_ [∗] .

( _𝒪_ ) ( _𝒪_ )
At inference time, the orchestrator retrieves _ℋ_ [Optionally,] [the retrieval operator may augment] _[ℋ]_
base [.] base
with additional skills whose semantic similarity to the query exceeds a threshold, yielding the final handbook

( _𝒪_ )
_ℋq_ used for query _q_ and orchestrator _𝒪_ : _ℋq_ = _ℋ_ base [∪] [⋃] _σ_ ∈ _𝒩k_ ( _q_ ) [({] _[σ]_ [}] [∪] [{] _[𝒫][A]_ [,] _[ψ]_ [∣] _[A]_ [ ∈] _[𝒜][ψ]_ [})][,][ where] _[ 𝒩][k]_ [(] _[q]_ [)][ is]
the _k_ nearest skills in the embedding space.


**Step 2:** **Skill-Grounded Agent Routing.** Guided by the retrieved handbook _ℋq_, the orchestrator performs
skill-grounded routing through an iterative decision process. An illustration can be found in Figure 3 (right).
At each time step _t_, it decides:


✦ **Mode Selection.** The mode policy _π_ mode selects the current operational mode _ψt_ based on the interaction
state _st_ and the mode-level routing metadata stored in the handbook: _ψt_ ∼ _π_ mode( _ψ_ ∣ _st_ ; _ℛψ_ ). This decision
determines the operational mode to execute next (e.g., _Search_, _Code_ ).


✦ **Competence-Aware Agent Routing.** Conditioned on the selected mode _ψt_, the orchestrator identifies
a set of relevant skills Σ _t_ ⊆ Σ _ψt_ that are active for the current state. Agent selection is then performed by
aggregating competence estimates over this skill set and trading them off against execution cost:


_A_ [∗] _t_ [=][ argmax] [ **E** _σ_ ∈Σ _t_ [ _ϕA_, _σ_ ] − _λc_ ⋅ _C_ [ˆ] _A_ ( _ψt_ )] .
_A_ ∈ _𝒜ψt_


where _ϕA_, _σ_ is the performance estimate stored in the agent profile _𝒫A_, _ψt_ . In practice, we approximate the
expected competence by aggregating the posterior means over the active skill set and optionally incorporating
semantic alignment between the current state and the agent profile:



_A_ [∗] _t_ [=][ argmax] [ ∑ _wt_, _σ_ _αA_, _σ_
_A_ ∈ _𝒜ψt_    - _σ_ **�������������������������������������������������������������** ∈Σ _t_ _αA_, _σ_ + _β_ _A_, _σ_    
Estimated Competence




- _λc_ ⋅ - _C_ ˆ **��������** _A_ (� _ψ_ **��������** _t_ )�
Mode-Specific Cost



].



This ensures that each decision is grounded in task-relevant skills, agent-specific competence estimates, and
explicit cost constraints. The full algorithm is provided in Appendix B (Algorithm 1).


8


SkillOrchestra: Learning to Route Agents via Skill Transfer


**4.2.** **Skill Handbook Learning**


We construct and refine the Skill Handbook _ℋ_ from execution traces rather than learning a monolithic routing
policy. The procedure iteratively updates the skill registry, agent profiles, and mode-level routing metadata
(Figure 3, left).

**Phase 1:** **Skill Discovery and Profile Construction.** We assume an exploratory dataset _𝒟_ train = {( _qi_, _ℬi_ )} _i_ _[N]_ =1 [,]

(1) (2)
where _ℬi_ = { _τi_, _τi_, . . .} are trajectories obtained by varying the agent choice at specific modes.

For each query and mode _ψ_, we contrast a successful trajectory _τ_ + _ψ_ [with a failed one] _[ τ]_ - _ψ_ [.] [Their difference]
_𝒟_ diff( _τ_ + _ψ_ [∥] _[τ]_ - _ψ_ [)][ isolates the missing capability.] [An LLM-based discoverer abstracts this capability gap into a]
reusable skill definition _σ_ new, which is added to the registry _𝒱_ Σ together with its associated mode mapping
_M_ .


Agent profiles are then estimated from aggregated outcomes. For each agent _A_, mode _ψ_, and skill _σ_ ∈ Σ _ψ_,
we model success probability as _ϕA_, _σ_ ∼ Beta( _αA_, _σ_, _β_ _A_, _σ_ ), updated via


( _t_ +1) ( _t_ )
_αA_, _σ_ ← _αA_, _σ_ [+] [∑] **I** [ _A_ succeeds on _σ_ in _τ_ ],

_τ_ ∈ _ℬi_

( _t_ +1) ( _t_ )
_β_ _A_, _σ_ ← _β_ _A_, _σ_ [+] [∑] **I** [ _A_ fails on _σ_ in _τ_ ].

_τ_ ∈ _ℬi_


Mode-level routing signals (e.g., frequent transitions or systematic failures or recurring recovery patterns)
are distilled into reusable mode-selection insights and stored as routing metadata _ℛψ_ .


**Phase 2:** **Handbook Refinement.** To prevent over-fragmentation or redundancy, we periodically refine the
skill set using agent profile statistics.


✦ **Splitting.** A skill _σ_ is marked as a split candidate if agent performance exhibits high variance across its
associated queries, indicating multiple underlying capabilities.

✦ **Merging.** A pair of skills ( _σi_, _σj_ ) is marked as a merge candidate when their agent performance profiles
are statistically indistinguishable, suggesting redundancy for routing.


Given these candidates, an LLM-based reflector (e.g., GPT-5) reviews the proposed operations and, if
appropriate, generates revised skill definitions. Approved refinements update both the skill registry and the
associated competence statistics ( _αA_, _σ_, _β_ _A_, _σ_ ). The final refined handbook _ℋ_ [∗] encodes learned skills, agent
profiles, and routing metadata, and serves as the reusable knowledge base for inference-time handbook
selection (Section 4.1).


**4.3.** **Pareto-Optimal Skill Handbook Selection**


This subsection formalizes the handbook selection step introduced in Section 4.1, where an orchestratorspecific subset is chosen to match the reasoning capacity and cost budget of the target orchestrator. An
illustration can be found in Figure 3 (middle).


Given the learned handbook _ℋ_ [∗] (Section 4.2), our goal is to select, for a target orchestrator _𝒪_, a subset
_ℋ_ ⊆ _ℋ_ [∗] that achieves the best end-to-end performance-cost tradeoff.

Each candidate subset _ℋ_ induces a routing policy _πℋ_, which produces a trajectory _τℋ_ ( _q_ ) for a query _q_ . We


9


SkillOrchestra: Learning to Route Agents via Skill Transfer


**Table 1:** Experimental results on QA datasets. **Bold** = best, underline = second best in each column. SkillOrchestra
uses the same orchestrator model as baselines. SkillOrchestra+ reports the best performance obtained by switching
among different orchestrator models within the same agent pool while using the same learned Skill Handbook.


**Method** **General QA** **Multi-Hop QA** **Avg.**


**NQ** **TriviaQA** **PopQA** **HotpotQA** **2wiki** **Musique** **Bamboogle**


Vanilla 9.2 26.0 12.2 14.0 26.6 2.6 4.0 13.5


_**No Routing**_
SFT 21.2 40.0 16.0 19.8 25.6 5.2 11.2 19.9
RAG 29.8 54.0 36.6 21.6 14.6 7.8 22.4 26.7
CoT (Wei et al., 2022) 12.6 35.8 16.0 16.8 20.8 4.6 22.4 18.4
Search-R1 (Jin et al., 2025) 32.8 51.0 32.4 23.6 27.8 9.0 27.2 29.1


_**Heuristic & Discriminative Routing**_
Largest LLM 29.6 57.8 35.4 27.8 27.4 10.4 48.0 33.8
Prompt LLM 30.0 58.0 34.0 26.8 26.2 10.8 44.8 32.9
Prompt LLM+ (multi turn) 25.8 50.0 25.6 20.6 24.8 7.8 47.2 28.8
KNN Router (Hu et al., 2024) 26.2 52.8 22.2 22.4 19.6 6.6 36.0 26.5
KNN Router+ (multi turn) 23.6 47.8 23.2 15.4 23.4 7.2 38.4 25.6
MLP Router (Hu et al., 2024) 25.2 46.0 22.2 19.8 21.0 7.2 36.0 25.3
BERT Router (Ong et al., 2025) 23.0 51.6 19.2 21.6 20.6 5.8 31.2 24.7
RouterDC (Chen et al., 2024b) 27.8 59.2 28.2 24.4 21.8 8.0 50.4 31.4
GraphRouter (Feng et al., 2025) 27.6 58.6 28.0 23.4 18.0 7.6 44.8 29.7
FrugalGPT (Chen et al., 2024a) 26.5 56.2 36.2 23.4 26.8 10.3 43.0 31.8


_**RL-based Routing**_
Router-R1 (Zhang et al., 2025a) 38.8 70.6 38.4 35.2 43.4 13.8 51.2 41.6


**Ours**
**`SkillOrchestra`** 54.2 71.6 42.6 39.0 48.0 18.2 58.4 47.4
**`SkillOrchestra`** + **54.8** **80.2** **48.8** **44.2** **49.6** **20.6** **63.2** **51.6**


evaluate candidate subsets on a held-out validation set _𝒟_ val and solve:



∣ _τℋ_ ( _q_ )∣
∑ _C_ ( _ψt_, _At_ ) .

_t_ =0
⎤⎥⎥⎥⎥⎥⎥⎦



( _𝒪_ )
_ℋ_ base [=][ argmax]
_ℋ_ ⊆ _ℋ_ [∗] **[E]** _[q]_ [∼] _[𝒟]_ [val]



_R_ ( _τℋ_ ( _q_ )) − _λ_
⎡⎢⎢⎢⎢⎢⎢⎣



Here, _R_ ( _τℋ_ ( _q_ )) ∈ [0, 1] denotes task success, and _C_ ( _ψt_, _At_ ) is the execution cost at step _t_ . The coefficient _λ_
controls the performance-cost tradeoff. This objective directly evaluates entire trajectories rather than local
routing accuracy, ensuring that the selected handbook lies on the Pareto frontier for the target orchestrator.

### **5. Experiments**


We conduct extensive experiments to answer:


**(RQ1) Effectiveness:** Does a learned Skill Handbook improve end-to-end accuracy over heuristic, discriminative, and RL-based methods?


**(RQ2) Efficiency:** Does skill-based orchestration yield a better performance-cost trade-off?


**(RQ3) Routing Behavior:** Does skill-based orchestration reduce routing collapse and better match model
capacity to task difficulty across modes?


**(RQ4) Transferability:** Can a Skill Handbook be reused across orchestrators without retraining?


10


SkillOrchestra: Learning to Route Agents via Skill Transfer


**(RQ5) Component Contribution:** How do different components of the Skill Handbook contribute to overall
performance and cost efficiency?


**5.1.** **SkillOrchestra for Model Routing**


We first evaluate SkillOrchestra in the model routing setting (Chen et al., 2024a, Feng et al., 2025, Zhang
et al., 2025a), where no external tools or knowledge base are provided. Therefore, the performance gaps
directly reflect the quality of model orchestration.


**Benchmarks.** We consider a diverse suite of knowledge and reasoning-intensive tasks including (1) General
QA: Natural Question (Kwiatkowski et al., 2019), TriviaQA (Joshi et al., 2017), PopQA (Mallen et al., 2023);
(2) Multi-hop QA: HotpotQA (Yang et al., 2018), 2WikiMultiHopQA (Ho et al., 2020), Musique (Trivedi
et al., 2022), and Bamboogle (Press et al., 2023); (3) Math Reasoning: MATH (Hendrycks et al., 2021) and
AMC23 (MAA, 2023).


**Experimental** **setup** **and** **baselines.** We use Qwen2.5-3B (Qwen, 2024) as the orchestrator and adopt
the same configuration as Router-R1 for controlled comparison with all routing baselines. Model pool and
implementation details are included in Appendix A.1. We compare SkillOrchestra against three categories of
methods: **(1) No routing** : methods that do not dynamically consult different models, including supervised
finetuning, RAG as in Zhang et al. (2025a), CoT (Wei et al., 2022), and Search-R1 (Jin et al., 2025); **(2)**
**Heuristic & Discriminative routing** : methods that select models based on input-level signals or learned
classifiers, including Largest LLM, Prompt LLM, Prompt LLM+ (explicit task decomposition+multi-turn),
KNN Router (Hu et al., 2024), KNN Router+ (explicit task decomposition and route each subtask to different
models which matching query similarity with KNN router), MLP Router (Hu et al., 2024), BERT Router (Ong
et al., 2025), RouterDC (Chen et al., 2024b), GraphRouter (Feng et al., 2025), and FrugalGPT (Chen
et al., 2024a); **(3) RL-based routing** : Router-R1 (Zhang et al., 2025a), a strong PPO-trained (Schulman
et al., 2017) multi-turn router with 14k samples, which represents the current SoTA in learned end-to-end
orchestration.



**Observation** ❶ **SkillOrchestra** **outperforms** **all**
**routing baselines, including expensive RL-based**
**methods (RQ1).** SkillOrchestra surpasses all baselines on both general and multi-hop QA (Table 1).
Compared to Router-R1 (41.6 EM), SkillOrchestra
reaches 47.4 (+5.8), and SkillOrchestra+ achieves
51.6 (+10.0). Gains are especially large on multihop tasks such as Musique (13.8 →18.2 →20.6)
and Bamboogle (51.2 →58.4 →63.2). Similar
trends hold for math reasoning (Figure 5), with
up to +22.5 accuracy over Router-R1 at substantially lower cost. Notably, these gains require only
a small fraction of the training data, demonstrating
higher data efficiency than RL-based routing.



80


60


40



Performance

73.6


55.8


25.0



Cost



52.5



6


4


2





1.6



20
MATH AMC



0.5

0



**Figure 5:** Performance and cost comparison: SkillOrchestra vs. Router-R1. SkillOrchestra achieves up to a 22.5
percentage-point improvement in accuracy while reducing
inference cost by ∼ 2.0×.



**Observation** ❷ **SkillOrchestra lies on the Pareto frontier (RQ2).** Figure 1 (left) shows that SkillOrchestra
and SkillOrchestra+ achieve higher accuracy at lower or comparable cost than all heuristic, discriminative,
and RL-based baselines. Importantly, higher per-token price does not necessarily imply higher total inference


11


SkillOrchestra: Learning to Route Agents via Skill Transfer













**Figure 6:** Skill-based orchestration mitigates routing collapse and generalizes across orchestrators. (Left) Router-R1
collapses to a single large model (98% Llama3.1-70B), while SkillOrchestra distributes calls according to capability
differences. (right) A Skill Handbook learned from Qwen2.5-3B transfers across orchestrator backbones without
retraining, consistently improving performance and achieving larger gains with stronger backbones.


cost. Total cost depends jointly on (i) the per-token price of the selected backbone model, (ii) the number of
generated tokens, and (iii) the number of routing steps. In practice, some lower per-token models produce
substantially longer reasoning chains, leading to higher overall cost. SkillOrchestra explicitly accounts for this
trade-off, often selecting capable yet more cost-efficient models (e.g., Mixtral-8×22B) instead of consistently
escalating to the most expensive model (LLaMA-3.1-70B). For example, Router-R1 attains 41.6 EM at a
high cost (51.8¢), whereas SkillOrchestra achieves higher accuracy (47.4 EM) at a lower cost (38.4¢).
SkillOrchestra+ further improves to 51.6 EM at 41.6¢. Router-R1 attains 41.6 EM at a high cost (51.8¢),
whereas SkillOrchestra achieves higher accuracy (47.4 EM) at a lower cost (38.4¢). SkillOrchestra+ further
improves to 51.6 EM at 41.6¢. Similar advantages appear in math reasoning (Figure 5), where SkillOrchestra
improves accuracy while reducing cost by about 2×. These results indicate that skill-aware routing allocates
models more efficiently and shortens reasoning chains.


**Observation** ❸ **Skill-based** **routing** **alleviates** **routing** **collapse** **seen** **in** **RL-based** **routing** **(RQ3).** To
understand the performance and efficiency gap, Figure 6 (left) compares model selection distributions
across nine benchmarks. Router-R1 shows clear _routing collapse_ : it selects LLaMA-3.1-70B for 98.02% of all
calls, while all other models are almost unused (each ≤0.92%; e.g., Qwen2.5-7B 0.35%, Mistral-7B 0.92%,
Mixtral-8×22B 0.04%, Qwen2.5-3B 0.00%). Despite being trained as a multi-model router, its RL policy
converges to repeatedly invoking a single large model, limiting specialization and inflating cost. In contrast,
**`SkillOrchestra`** produces a much more balanced routing pattern: e.g., Mixtral-8×22B 44.53%, Qwen2.57B 25.99%, LLaMA-3.1-70B 15.38%, and Qwen2.5-3B 11.50%. This distribution reflects capability-aware
specialization, where stronger models are used only when necessary and lighter models handle simpler
steps. Importantly, skill-based routing also makes the orchestrator itself more effective. In some cases, the
orchestrator can directly answer the query without escalating to a larger model, further reducing unnecessary
calls and lowering the total cost. An example in shown in Figure 8.


**Observation** ❹ **The learned skill handbook transfers across orchestrator backbones without retraining**
**(RQ4).** We reuse the skill handbook learned from traces where Qwen2.5-3B serves as the orchestrator, and
directly apply it to other backbone models without any additional handbook training. Figure 6 (right) shows


12


SkillOrchestra: Learning to Route Agents via Skill Transfer


performance before and after introducing the same skill handbook, with results averaged over three general
QA datasets. The learned handbook consistently improves all tested models. Qwen2.5-3B itself improves
from 40.7% to 56.1% (+15.4). When transferred to larger or stronger models, the gains remain substantial:
Qwen2.5-7B improves from 35.7% to 60.0% (+24.3), Llama3.1-8B from 35.5% to 58.0% (+22.5), and
Mistral-7B from 36.5% to 59.8% (+23.3). Even larger-scale models benefit from such handbook: Mixtral8x22B from 46.5% to 61.3% (+14.8). These results show that the skill handbook captures transferable,
model-agnostic orchestration knowledge. Notably, stronger models often achieve the highest absolute
performance when paired with the transferred handbook, suggesting that improved backbone capability and
structured skill guidance are complementary.


**5.2.** **SkillOrchestra on Agent Orchestration**


We next evaluate whether SkillOrchestra extends beyond model routing to full agent orchestration, where
the system must coordinate multiple operational modes and tools beyond model selection. We use the same
configuration as ToolOrchestra (Su et al., 2025), detailed in the following.


**Experimental** **setup** **and** **baselines.** We evaluate on FRAMES (Krishna et al., 2024) and consider three
operational modes: `search` (web and local search), `code`, and `answer` . Each mode corresponds to a
different model pool, detailed in Appendix A.2. The maximum interaction horizon is 50 turns. With Qwen38B as the orchestrator, we compare against ToolOrchestra (Su et al., 2025), which trains the orchestrator
using GRPO. We also compare against strong proprietary model orchestrators such as GPT-5 (OpenAI, 2025a),
Gemini-3-Pro (Google, 2025), or Claude-Opus-4.5 (Anthropic, 2025), while keeping modes, model pools,
tools, and execution environments fixed.



**Observation** ❺ **SkillOrchestra** **achieves** **better**
**performance-cost trade-offs in full agent orches-** **Table 2:** Analysis of SkillOrchestra’s Skill Handbook design.
**tration** **(RQ1,** **RQ2).** Figure 1 (right) shows that HB: Has Handbook, Disc: Skill Discovery, Ref: Handbook

Refinement, Sel: Handbook Selection, FG: Fine-grained

SkillOrchestra remains on the Pareto frontier in

Skills. Orchestrator: Qwen3-8B.

the more complex agent orchestration setting with

racy (84.3%) while also incurring the lowest total No Ref + Sel ✔ ✔ - - ✔ 79.0 5.5
cost ($72.7) among strong learned and proprietary- No Selection ✔ ✔ ✔ - ✔ 79.3 3.4
model baselines. Compared to the RL-trained No FG Skills ✔ ✔ ✔ ✔ - 80.4 15.1
ToolOrchestra (76.3%, $92.7), SkillOrchestra im- Full System ✔ ✔ ✔ ✔ ✔ 85.0 9.3
proves accuracy by +8.0 points while reducing cost
by 21.6%. It also outperforms stronger proprietary orchestrators such as GPT-5 (74.6%, $120.4), Claude
Opus 4.5 (77.9%, $758.1), and Gemini 3 Pro (78.9%, $1729.3). These results highlight an important
system-level trade-off: while using a stronger model as the orchestrator can improve raw task performance,
it often does so at a prohibitive cost due to expensive per-token pricing and long multi-step trajectories. In
contrast, SkillOrchestra improves both accuracy and efficiency by coordinating specialized models and tools
through explicit skill modeling, rather than relying on a single large model to carry the entire process.



**Table 2:** Analysis of SkillOrchestra’s Skill Handbook design.
HB: Has Handbook, Disc: Skill Discovery, Ref: Handbook
Refinement, Sel: Handbook Selection, FG: Fine-grained
Skills. Orchestrator: Qwen3-8B.



No HB - - - - - 71.0 122.9
No Ref + Sel ✔ ✔ - - ✔ 79.0 5.5
No Selection ✔ ✔ ✔ - ✔ 79.3 3.4
No FG Skills ✔ ✔ ✔ ✔ - 80.4 15.1



Full System ✔ ✔ ✔ ✔ ✔ 85.0 9.3



**Observation** ❻ **More skills are not always better; optimal performance-cost trade-offs require refining**
**and** **selecting** **skills** **to** **match** **the** **orchestrator’s** **capability** **(RQ1,** **RQ3,** **RQ5).** To understand the
contribution of each component of SkillOrchestra, we conduct a controlled ablation study on 100 randomly


13


SkillOrchestra: Learning to Route Agents via Skill Transfer


sampled FRAMES tasks. As shown in Table 2, removing the Skill Handbook causes a large drop in accuracy
(85.0% →71.0%) and a sharp increase in cost (9.3 →122.9), showing that structured skill guidance is crucial
for both effectiveness and efficiency. Using discovered skills without handbook refinement and selection,
which includes redundant, overlapping or overly broad skills, still achieves reasonable accuracy (79.0%) at low
cost (5.5), suggesting that even an unrefined skill set still provides useful routing signals. Enabling refinement
further reduces cost (3.4) while maintaining similar accuracy (79.3%), indicating that reorganizing skills by
merging redundant ones and splitting indistinguishable ones improves efficiency. Disabling fine-grained skills
degrades both accuracy (80.4%) and efficiency (15.1), showing that appropriately detailed skills help the
orchestrator make better decisions. Overall, the best performance-cost trade-off is achieved when skills are
discovered, reorganized, and selectively applied at a level of detail that the orchestrator can use effectively.

### **6. Conclusion**


In this work, we propose SkillOrchestra, an agentic orchestration framework that reframes multi-turn routing
as skill-grounded decision making. By learning a Skill Handbook, the orchestrator makes state-aware,
competence-aware decisions that explicitly optimize the performance-cost trade-off. Across both model
routing and agent orchestration settings, SkillOrchestra achieves superior performance with significantly
lower cost compared to competitive baselines. Moreover, the handbook is transferable across orchestrator
backbones without retraining, enabling scalable deployment as model pools evolve. We hope this work serves
as a springboard for scalable orchestration that improves the performance-cost frontier as agent pools grow
and diversify.

### **References**


Anthropic. Introducing Claude Opus 4.5, 2025. URL `[https://www.anthropic.com/news/](https://www.anthropic.com/news/claude-opus-4-5)`
`[claude-opus-4-5](https://www.anthropic.com/news/claude-opus-4-5)` .


Lingjiao Chen, Matei Zaharia, and James Zou. FrugalGPT: How to use large language models while reducing
cost and improving performance. Transactions on Machine Learning Research, 2024a. ISSN 2835-8856.
URL `[https://openreview.net/forum?id=cSimKw5p6R](https://openreview.net/forum?id=cSimKw5p6R)` . Featured Certification.


Shuhao Chen, Weisen Jiang, Baijiong Lin, James Kwok, and Yu Zhang. RouterDC: Query-based router by dual
contrastive learning for assembling large language models. In The Thirty-eighth Annual Conference
on Neural Information Processing Systems, 2024b. URL `[https://openreview.net/forum?id=](https://openreview.net/forum?id=7RQvjayHrM)`
`[7RQvjayHrM](https://openreview.net/forum?id=7RQvjayHrM)` .


Dujian Ding, Ankur Mallick, Chi Wang, Robert Sim, Subhabrata Mukherjee, Victor Ruhle, Laks VS Lakshmanan,
and Ahmed Hassan Awadallah. Hybrid llm: Cost-efficient and quality-aware query routing. arXiv preprint
arXiv:2404.14618, 2024.


Tao Feng, Yanzhen Shen, and Jiaxuan You. Graphrouter: A graph-based router for LLM selections. In The

Thirteenth International Conference on Learning Representations, 2025. URL `[https://openreview.](https://openreview.net/forum?id=eU39PDsZtT)`
`[net/forum?id=eU39PDsZtT](https://openreview.net/forum?id=eU39PDsZtT)` .


Gemini. Gemini deep research, 2024. URL `[https://gemini.google/overview/deep-research/](https://gemini.google/overview/deep-research/)` .


14


SkillOrchestra: Learning to Route Agents via Skill Transfer


Team Gemma, Morgane Riviere, Shreya Pathak, Pier Giuseppe Sessa, Cassidy Hardin, Surya Bhupatiraju,
Léonard Hussenot, Thomas Mesnard, Bobak Shahriari, Alexandre Ramé, et al. Gemma 2: Improving open
language models at a practical size. arXiv preprint arXiv:2408.00118, 2024.


Google. A new era of intelligence with Gemini 3, 2025. URL `[https://blog.google/](https://blog.google/products-and-platforms/products/gemini/gemini-3/)`
`[products-and-platforms/products/gemini/gemini-3/](https://blog.google/products-and-platforms/products/gemini/gemini-3/)` .


Juraj Gottweis, Wei-Hung Weng, Alexander Daryin, Tao Tu, Anil Palepu, Petar Sirkovic, Artiom Myaskovsky,
Felix Weissenberger, Keran Rong, Ryutaro Tanno, Khaled Saab, Dan Popovici, Jacob Blum, Fan Zhang,
Katherine Chou, Avinatan Hassidim, Burak Gokturk, Amin Vahdat, Pushmeet Kohli, Yossi Matias, Andrew
Carroll, Kavita Kulkarni, Nenad Tomasev, Yuan Guan, Vikram Dhillon, Eeshit Dhaval Vaishnav, Byron Lee,
Tiago R D Costa, José R Penadés, Gary Peltz, Yunhan Xu, Annalisa Pawlosky, Alan Karthikesalingam, and
Vivek Natarajan. Towards an ai co-scientist. 2025. URL `[https://arxiv.org/abs/2502.18864](https://arxiv.org/abs/2502.18864)` .


Aaron Grattafiori, Abhimanyu Dubey, Abhinav Jauhri, Abhinav Pandey, Abhishek Kadian, Ahmad Al-Dahle,
Aiesha Letman, et al. The llama 3 herd of models, 2024. URL `[https://arxiv.org/abs/2407.21783](https://arxiv.org/abs/2407.21783)` .


Dan Hendrycks, Collin Burns, Saurav Kadavath, Akul Arora, Steven Basart, Eric Tang, Dawn Song, and Jacob
Steinhardt. Measuring mathematical problem solving with the math dataset. NeurIPS, 2021.


Xanh Ho, Anh-Khoa Duong Nguyen, Saku Sugawara, and Akiko Aizawa. Constructing a multi-hop QA
dataset for comprehensive evaluation of reasoning steps. In Donia Scott, Nuria Bel, and Chengqing Zong,
editors, Proceedings of the 28th International Conference on Computational Linguistics, pages 6609–6625,
Barcelona, Spain (Online), December 2020. International Committee on Computational Linguistics. doi:
10.18653/v1/2020.coling-main.580. URL `[https://aclanthology.org/2020.coling-main.580/](https://aclanthology.org/2020.coling-main.580/)` .


Qitian Jason Hu, Jacob Bieker, Xiuyu Li, Nan Jiang, Benjamin Keigwin, Gaurav Ranganath, Kurt Keutzer, and
Shriyash Kaustubh Upadhyay. Routerbench: A benchmark for multi-llm routing system. arXiv preprint
arXiv:2403.12031, 2024.


Albert Q. Jiang, Alexandre Sablayrolles, Arthur Mensch, Chris Bamford, Devendra Singh Chaplot, Diego
de las Casas, Florian Bressand, Gianna Lengyel, Guillaume Lample, Lucile Saulnier, et al. Mistral 7b,
2023a. URL `[https://arxiv.org/abs/2310.06825](https://arxiv.org/abs/2310.06825)` .


Albert Q Jiang, Alexandre Sablayrolles, Antoine Roux, Arthur Mensch, Blanche Savary, Chris Bamford,
Devendra Singh Chaplot, Diego de las Casas, Emma Bou Hanna, Florian Bressand, et al. Mixtral of experts.
arXiv preprint arXiv:2401.04088, 2024.


Dongfu Jiang, Xiang Ren, and Bill Yuchen Lin. LLM-blender: Ensembling large language models with
pairwise ranking and generative fusion. In Anna Rogers, Jordan Boyd-Graber, and Naoaki Okazaki, editors,
Proceedings of the 61st Annual Meeting of the Association for Computational Linguistics (Volume 1: Long
Papers), pages 14165–14178, Toronto, Canada, July 2023b. Association for Computational Linguistics.
doi: 10.18653/v1/2023.acl-long.792. URL `[https://aclanthology.org/2023.acl-long.792/](https://aclanthology.org/2023.acl-long.792/)` .


Bowen Jin, Hansi Zeng, Zhenrui Yue, Jinsung Yoon, Sercan O Arik, Dong Wang, Hamed Zamani, and
Jiawei Han. Search-r1: Training LLMs to reason and leverage search engines with reinforcement learning.
In Second Conference on Language Modeling, 2025. URL `[https://openreview.net/forum?id=](https://openreview.net/forum?id=Rwhi91ideu)`
`[Rwhi91ideu](https://openreview.net/forum?id=Rwhi91ideu)` .


15


SkillOrchestra: Learning to Route Agents via Skill Transfer


Mandar Joshi, Eunsol Choi, Daniel Weld, and Luke Zettlemoyer. TriviaQA: A large scale distantly supervised
challenge dataset for reading comprehension. In Regina Barzilay and Min-Yen Kan, editors, Proceedings
of the 55th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers),
pages 1601–1611, Vancouver, Canada, July 2017. Association for Computational Linguistics. doi: 10.
18653/v1/P17-1147. URL `[https://aclanthology.org/P17-1147/](https://aclanthology.org/P17-1147/)` .


Zixuan Ke, Fangkai Jiao, Yifei Ming, Xuan-Phi Nguyen, Austin Xu, Do Xuan Long, Minzhi Li, Chengwei
Qin, PeiFeng Wang, silvio savarese, Caiming Xiong, and Shafiq Joty. A survey of frontiers in LLM reasoning: Inference scaling, learning to reason, and agentic systems. Transactions on Machine Learning
Research, 2025. ISSN 2835-8856. URL `[https://openreview.net/forum?id=SlsZZ25InC](https://openreview.net/forum?id=SlsZZ25InC)` . Survey
Certification.


Satyapriya Krishna, Kalpesh Krishna, Anhad Mohananey, Steven Schwarcz, Adam Stambler, Shyam Upadhyay,
and Manaal Faruqui. Fact, fetch, and reason: A unified evaluation of retrieval-augmented generation,
2024. URL `[https://arxiv.org/abs/2409.12941](https://arxiv.org/abs/2409.12941)` .


Tom Kwiatkowski, Jennimaria Palomaki, Olivia Redfield, Michael Collins, Ankur Parikh, Chris Alberti,
Danielle Epstein, Illia Polosukhin, Jacob Devlin, Kenton Lee, et al. Natural questions: a benchmark for
question answering research. Transactions of the Association for Computational Linguistics, 7:453–466,
2019.


Keming Lu, Hongyi Yuan, Runji Lin, Junyang Lin, Zheng Yuan, Chang Zhou, and Jingren Zhou. Routing to
the expert: Efficient reward-guided ensemble of large language models. In Kevin Duh, Helena Gomez,
and Steven Bethard, editors, Proceedings of the 2024 Conference of the North American Chapter of
the Association for Computational Linguistics: Human Language Technologies (Volume 1: Long Papers),
pages 1964–1974, Mexico City, Mexico, June 2024. Association for Computational Linguistics. doi:
10.18653/v1/2024.naacl-long.109. URL `[https://aclanthology.org/2024.naacl-long.109/](https://aclanthology.org/2024.naacl-long.109/)` .


MAA. American mathematics competitions 2023 problems (amc23), 2023. URL `[https://maa.org/](https://maa.org/student-programs/amc/)`
`[student-programs/amc/](https://maa.org/student-programs/amc/)` .


Alex Mallen, Akari Asai, Victor Zhong, Rajarshi Das, Daniel Khashabi, and Hannaneh Hajishirzi. When not
to trust language models: Investigating effectiveness of parametric and non-parametric memories. In
Anna Rogers, Jordan Boyd-Graber, and Naoaki Okazaki, editors, Proceedings of the 61st Annual Meeting
of the Association for Computational Linguistics (Volume 1: Long Papers), pages 9802–9822, Toronto,
Canada, July 2023. Association for Computational Linguistics. doi: 10.18653/v1/2023.acl-long.546. URL
`[https://aclanthology.org/2023.acl-long.546/](https://aclanthology.org/2023.acl-long.546/)` .


Isaac Ong, Amjad Almahairi, Vincent Wu, Wei-Lin Chiang, Tianhao Wu, Joseph E. Gonzalez, M Waleed
Kadous, and Ion Stoica. RouteLLM: Learning to route LLMs from preference data. In The Thirteenth
International Conference on Learning Representations, 2025. URL `[https://openreview.net/forum?](https://openreview.net/forum?id=8sSqNntaMr)`
`[id=8sSqNntaMr](https://openreview.net/forum?id=8sSqNntaMr)` .


OpenAI. Gpt-5 system card, 2025a. URL `[https://cdn.openai.com/gpt-5-system-card.pdf](https://cdn.openai.com/gpt-5-system-card.pdf)` .


OpenAI. Introducing deep research, 2025b. URL `[https://openai.com/index/](https://openai.com/index/introducing-deep-research/)`
`[introducing-deep-research/](https://openai.com/index/introducing-deep-research/)` .


16


SkillOrchestra: Learning to Route Agents via Skill Transfer


Ofir Press, Muru Zhang, Sewon Min, Ludwig Schmidt, Noah Smith, and Mike Lewis. Measuring and narrowing
the compositionality gap in language models. In Houda Bouamor, Juan Pino, and Kalika Bali, editors,
Findings of the Association for Computational Linguistics: EMNLP 2023, pages 5687–5711, Singapore,
December 2023. Association for Computational Linguistics. doi: 10.18653/v1/2023.findings-emnlp.378.
URL `[https://aclanthology.org/2023.findings-emnlp.378/](https://aclanthology.org/2023.findings-emnlp.378/)` .


Qwen. Qwen2.5: A party of foundation models, September 2024. URL `[https://qwenlm.github.io/](https://qwenlm.github.io/blog/qwen2.5/)`
`[blog/qwen2.5/](https://qwenlm.github.io/blog/qwen2.5/)` .


Marija Šakota, Maxime Peyrard, and Robert West. Fly-swat or cannon? cost-effective language model choice
via meta-modeling. In Proceedings of the 17th ACM International Conference on Web Search and Data
Mining, pages 606–615, 2024.


John Schulman, Filip Wolski, Prafulla Dhariwal, Alec Radford, and Oleg Klimov. Proximal policy optimization
algorithms. arXiv preprint arXiv:1707.06347, 2017.


Zhihong Shao, Peiyi Wang, Qihao Zhu, Runxin Xu, Junxiao Song, Xiao Bi, Haowei Zhang, Mingchuan Zhang,
YK Li, Yang Wu, et al. Deepseekmath: Pushing the limits of mathematical reasoning in open language
models. arXiv preprint arXiv:2402.03300, 2024.


Dimitris Stripelis, Zhaozhuo Xu, Zijian Hu, Alay Dilipbhai Shah, Han Jin, Yuhang Yao, Jipeng Zhang, Tong
Zhang, Salman Avestimehr, and Chaoyang He. TensorOpera router: A multi-model router for efficient LLM
inference. In Franck Dernoncourt, Daniel Preoţiuc-Pietro, and Anastasia Shimorina, editors, Proceedings
of the 2024 Conference on Empirical Methods in Natural Language Processing: Industry Track, pages
452–462, Miami, Florida, US, November 2024. Association for Computational Linguistics. doi: 10.18653/
v1/2024.emnlp-industry.34. URL `[https://aclanthology.org/2024.emnlp-industry.34/](https://aclanthology.org/2024.emnlp-industry.34/)` .


Hongjin Su, Shizhe Diao, Ximing Lu, Mingjie Liu, Jiacheng Xu, Xin Dong, Yonggan Fu, Peter Belcak, Hanrong
Ye, Hongxu Yin, Yi Dong, Evelina Bakhturina, Tao Yu, Yejin Choi, Jan Kautz, and Pavlo Molchanov.
Toolorchestra: Elevating intelligence via efficient model and tool orchestration, 2025. URL `[https:](https://arxiv.org/abs/2511.21689)`
`[//arxiv.org/abs/2511.21689](https://arxiv.org/abs/2511.21689)` .


Harsh Trivedi, Niranjan Balasubramanian, Tushar Khot, and Ashish Sabharwal. MuSiQue: Multihop questions
via single-hop question composition. Transactions of the Association for Computational Linguistics, 10:
539–554, 2022. doi: 10.1162/tacl_a_00475. URL `[https://aclanthology.org/2022.tacl-1.31/](https://aclanthology.org/2022.tacl-1.31/)` .


Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten Bosma, Fei Xia, Ed Chi, Quoc V Le, Denny Zhou, et al.
Chain-of-thought prompting elicits reasoning in large language models. Advances in neural information
processing systems, 35:24824–24837, 2022.


Zhilin Yang, Peng Qi, Saizheng Zhang, Yoshua Bengio, William W. Cohen, Ruslan Salakhutdinov, and
Christopher D. Manning. HotpotQA: A dataset for diverse, explainable multi-hop question answering. In
Conference on Empirical Methods in Natural Language Processing (EMNLP), 2018.


Haozhen Zhang, Tao Feng, and Jiaxuan You. Router-r1: Teaching llms multi-round routing and aggregation
via reinforcement learning. In The Thirty-ninth Annual Conference on Neural Information Processing
Systems, 2025a.


17


SkillOrchestra: Learning to Route Agents via Skill Transfer


Yanzhao Zhang, Mingxin Li, Dingkun Long, Xin Zhang, Huan Lin, Baosong Yang, Pengjun Xie, An Yang,
Dayiheng Liu, Junyang Lin, Fei Huang, and Jingren Zhou. Qwen3 embedding: Advancing text embedding
and reranking through foundation models. arXiv preprint arXiv:2506.05176, 2025b.


18


SkillOrchestra: Learning to Route Agents via Skill Transfer

### **A. Experimental Details**


**A.1.** **Experimental Details for Model Routing**


**Implementation Details.** We use the same evaluation protocol as Router-R1 for controlled comparison with
all routing baselines. We use Qwen2.5-3B (Qwen, 2024) as the orchestrator, and the model pool consists
of Qwen2.5-7B (Qwen, 2024), LLaMA-3.1-8B (Grattafiori et al., 2024), LLaMA-3.1-70B (Grattafiori et al.,
2024), Mistral-7B (Jiang et al., 2023a), Mixtral-8x22B (Jiang et al., 2024), and Gemma-2-27B (Gemma
et al., 2024). Routing operates in two modes: (1) search mode, where the orchestrator selects a model
from the pool to perform subtasks (provide knowledge or solve the subtask); and (2) answer mode, where
the orchestrator aggregates intermediate results and produce the final answer. We set the max number of
turns to 4. We evaluate the performance using Exact Match (EM) and efficiency using total completion
cost. SkillOrchestra is trained in a low-data regime: by default, we select _k_ ( _k_ < 50) samples from each
dataset to train the Skill Handbook and _k_ additional samples for validation and handbook retrieval. We use
SkillOrchestra+ to denote the best performance obtained by switching among different orchestrator models
within the same agent pool while using the same learned Skill Handbook.


**A.2.** **Experimental Details for Agent Orchestration**


**Implementation Details.** We follow the same evaluation protocol and experimental setup as ToolOrchestra
to ensure a controlled and comparable evaluation. We consider three operational modes: For _ψ_ = `search`,
the allowable tools are _T_ `search` = { `WebSearch`, `LocalSearch` }, where WebSearch uses the Tavily API
and LocalSearch uses a FAISS index built with Qwen3-Embedding-8B (Zhang et al., 2025b). The model
set is _ℳ_ `search` = {GPT-5, GPT-5-mini, Qwen3-32B}. Valid agents are compositions ( _m_, _T_ `search` ) with _m_ ∈
_ℳ_ `search` . For _ψ_ = `code`, the tool set is _T_ `code` = { `PythonExec` } operating in a sandbox, and _ℳ_ `code` =
{GPT-5, GPT-5-mini, Qwen2.5-Coder-32B}. Valid agents are ( _m_, _T_ `code` ) with _m_ ∈ _ℳ_ `code` . For _ψ_ = `answer`,
no external tools are used ( _T_ `answer` = ∅), and _ℳ_ `answer` = {GPT-5, GPT-5-mini, Llama-3.3-70B-Instruct,
Qwen3-32B, Qwen2.5-Math-72B, Qwen2.5-Math-7B}. Valid agents are ( _m_, ∅) with _m_ ∈ _ℳ_ `answer` . The
maximum interaction horizon is 50 turns. Final answers are evaluated for accuracy using GPT-5-mini as a
judge, and total system cost (USD) is measured.

### **B. Skill-Grounded Agent Routing Algorithm Pseudocode**


We present an algorithm block for Skill-grounded Agent Routing in Algorithm 1. A concrete illustration can
be found in Figure 3 (Deployment).

### **C. A Closer Look at Model Selection: SkillOrchestra vs. ToolOrchestra**


**Skill-grounded routing leads to more efficient tool-model allocation (RQ3).** To understand the benefits
of SkillOrchestra compared to ToolOrchestra, we also take a closer look at the model selection ratio at each
operational mode. We found that the cost reduction of SkillOrchestra comes from smarter allocation of
models across different operational modes, rather than simply reducing the number of calls. In search mode,
ToolOrchestra routes 99.7% of calls to GPT-5-mini, whereas SkillOrchestra instead uses Qwen3-32B (also


19


SkillOrchestra: Learning to Route Agents via Skill Transfer


**Algorithm 1** Skill-Grounded Agent Routing by Orchestrator _𝒪_
**Input** **:** State _st_ ; query handbook _ℋq_ ; cost weight _λc_
**Output** **:** Selected mode _ψt_, agent _At_, trace _zt_, observation _ot_, updated state _st_ +1


- **`Mode`** **`selection`**
Select operational mode _ψt_ ∼ _π_ mode(⋅ ∣ _st_ ; _ℛψ_ )


- **`Retrieve`** **`active`** **`skills`**
Retrieve active skills Σ _t_ ⊆ Σ _ψt_ from _ℋq_


- **`Competence-aware`** **`routing`**
**foreach** _A_ ∈ _𝒜ψ_ ~~_t_~~ **do**

 - `posterior-mean` `competence` `from` `estimated` `stats` `in` `the` `Handbook`

_P_ ̂( _A_ ) ← ∑ _σ_ ∈Σ _t wt_, _σ_ _αA_, _σα_ + _A_, _βσ_ _A_, _σ_

 - `utility` `=` `competence` `-` `mode-specific` `cost`
_U_ ( _A_ ) ← _P_ [̂] ( _A_ ) − _λc_ ⋅ _C_ [̂] _A_ ( _ψt_ )

_At_ ← arg max _A_ ∈ _𝒜ψt_ _U_ ( _A_ )


- **`Execute`** **`+`** **`state`** **`transition`**
( _zt_, _ot_ ) ← Execute( _At_, _ψt_, _st_ ) `//` _zt_ `=` `agent` `trace,` _ot_ `=` `env` `observation`
_st_ +1 ← UpdateState( _st_, _ψt_, _At_, _zt_, _ot_ )


the cheapest) for 100% of search calls, identifying it as sufficiently capable and more cost-efficient for the
search task. In answer mode, ToolOrchestra similarly exhibits routing collapse, routing 97.9% of calls to
GPT-5. SkillOrchestra distributes answer generation more strategically: GPT-5 is used in 58.4% of calls, with
the remainder handled by cheaper or specialized models such as GPT-5-mini (10.0%) and Qwen3-32B or
math-expert models. This diversification allows the system to reserve expensive models for truly difficult
reasoning steps while offloading simpler synthesis or domain-specific subtasks to more efficient models.

### **D. Demonstrations of Skill-Aware Orchestration**


We provide full execution traces of the skill-based router in Figures 7–9, along with the orchestration
instruction template in Figure 10. The instruction integrates the task query, execution context, and the
selected Skill Handbook used for routing decisions.





20


SkillOrchestra: Learning to Route Agents via Skill Transfer





21


SkillOrchestra: Learning to Route Agents via Skill Transfer





22


SkillOrchestra: Learning to Route Agents via Skill Transfer





23


SkillOrchestra: Learning to Route Agents via Skill Transfer





24


SkillOrchestra: Learning to Route Agents via Skill Transfer





**Figure** **7:** Full trace of an AMC example. The router first analyzes the required skills, calls Mixtral-8x22B-Instruct,
which derives the correct form but miscounts the solutions; it then routes to LLaMA-3.1-70B-Instruct to correctly
restrict _θ_ ∈ [0, 2 _π_ ) and count distinct solutions, producing the correct final answer.







25


SkillOrchestra: Learning to Route Agents via Skill Transfer





26


SkillOrchestra: Learning to Route Agents via Skill Transfer





27


SkillOrchestra: Learning to Route Agents via Skill Transfer





28


SkillOrchestra: Learning to Route Agents via Skill Transfer





**Figure** **8:** Full trace of an AMC example. While the router (Qwen2.5-3B) has access to the Skill Handbook, it
autonomously determines that the problem can be solved using its internal capability, refrains from issuing any
`<search>` calls, and produces the correct final answer. This example highlights the flexibility of skill-based routing,
where external model invocation is optional rather than mandatory.







29


SkillOrchestra: Learning to Route Agents via Skill Transfer





30


SkillOrchestra: Learning to Route Agents via Skill Transfer





31


SkillOrchestra: Learning to Route Agents via Skill Transfer





32


SkillOrchestra: Learning to Route Agents via Skill Transfer





33


SkillOrchestra: Learning to Route Agents via Skill Transfer





**Figure** **9:** Full trace for a PopQA example. Guided by skill-based analysis, the router detects that the initial model
response is incomplete or ambiguous, re-routes to alternative models, and performs cross-model verification before
finalizing the answer. This demonstrates robust recovery from intermediate errors.







34


SkillOrchestra: Learning to Route Agents via Skill Transfer





35


SkillOrchestra: Learning to Route Agents via Skill Transfer





36


SkillOrchestra: Learning to Route Agents via Skill Transfer





37


SkillOrchestra: Learning to Route Agents via Skill Transfer





38


SkillOrchestra: Learning to Route Agents via Skill Transfer





39


SkillOrchestra: Learning to Route Agents via Skill Transfer





40


SkillOrchestra: Learning to Route Agents via Skill Transfer





41


SkillOrchestra: Learning to Route Agents via Skill Transfer





**Figure 10:** Agent orchestration instruction used for FRAMES, integrating the task query, execution history context, and
the selected Skill Handbook to enable skill-aware orchestration.


42


