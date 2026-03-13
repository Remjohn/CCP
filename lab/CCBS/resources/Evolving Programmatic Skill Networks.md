## **Evolving Programmatic Skill Networks**

**Haochen Shi** [1] _[,]_ [2] **Xingdi Yuan** [3][*] **Bang Liu** [1] _[,]_ [2] _[,]_ [4][*]

1 DIRO & Institut Courtois, Université de Montréal 2 Mila – Québec AI Institute
3 Microsoft Research 4 Canada CIFAR AI Chair


haochen.shi@umontreal.ca eric.yuan@microsoft.com bang.liu@umontreal.ca



**Abstract**


We study continual skill acquisition in openended embodied environments where an agent
must construct, refine, and reuse an expanding
library of executable skills. We introduce the
Programmatic Skill Network (PSN), a framework in which skills are executable symbolic
programs forming a compositional network that
evolves through experience. PSN defines three
core mechanisms instantiated via large language models: (1) REFLECT for structured fault
localization over skill compositions, (2) progressive optimization with maturity-aware update gating that stabilizes reliable skills while
maintaining plasticity for uncertain ones, and
(3) canonical structural refactoring under rollback validation that maintains network compactness. We further show that PSN’s learning dynamics exhibit structural parallels to neural network training. Experiments on MineDojo and Crafter demonstrate robust skill reuse,
rapid adaptation, and strong generalization
across open-ended task distributions. [1]


**1** **Introduction**


Embodied agents operating in open-ended environments must continually acquire, refine, and
reuse a growing repertoire of skills. Existing approaches (Wang et al., 2024a; Yao et al., 2023)
suffer from two limitations: (1) skills are typically
represented as flat libraries or static graphs lacking
principled mechanisms for continual improvement,
and (2) agents lack unified frameworks for assigning credit over hierarchical skill compositions, repairing symbolic programs, and reorganizing structure as new tasks arise.
We introduce the Programmatic Skill Network
(PSN), a framework for continually evolving skill
libraries. In a PSN, each skill is a symbolic program (e.g., in JavaScript for Minecraft, Python for


*Equal advising
1We plan to open-source the code.



Crafter) with explicit control flow, parameters, and
preconditions that specify applicability and effects.
Skills invoke each other through dependency links,
forming a directed graph that grows and reorganizes as the agent learns. While recent work has
explored programmatic skill representations for
agents (Wang et al., 2024b; Stengel-Eskin et al.,
2024; Wang et al., 2025c), PSN uniquely maintains an explicit computational graph of executable
programs that supports trace-based credit assignment, maturity-aware stabilization, and principled
structural refactoring.
The framework structures continual learning through three components: a _network-_
_aware_ _planner_ that prioritizes skill reuse via
backward-chaining, a _fault_ _localization_ _mecha-_
_nism_ (REFLECT) that assigns credit over skill compositions by analyzing execution traces, and a
_refactor module_ that reorganizes network structure.
These components are instantiated using LLMs for
program synthesis, but the continual learning behavior emerges from the architectural scaffolding
rather than the LLM itself. Figure 1 provides an
overview of the PSN framework, illustrating the
agent–environment interaction under a curriculum
task stream (left) and the internal evolution of the
programmatic skill network through planning, repairing, and structural refactoring (right).
A key insight is that PSN’s learning dynamics exhibit structural parallels to neural network
training. Fault localization over skill compositions resembles backpropagation through computational graphs (Rumelhart et al., 1986); maturitybased update gating induces stability-plasticity
tradeoffs analogous to layer freezing and learning
rate scheduling (Howard and Ruder, 2018; Yosinski et al., 2014; Rusu et al., 2016); and structural
refactoring performs a form of symbolic neural architecture search (Zoph and Le, 2017; Han et al.,
2016; Tan and Le, 2019). These parallels suggest
that principles of neural network optimization ex


1


tend to programmatic learning systems.
The contributions of this work are threefold:

_•_ **Programmatic Skill Networks.** We introduce
a framework for continual skill learning in which
skills are executable symbolic programs with explicit control flow, parameters, and pre/postconditions, forming a compositional network through
invocation links and yielding an inspectable computational graph that grows and reorganizes as the
agent learns.

_•_ **PSN learning mechanisms.** We develop three
complementary mechanisms for continual skill improvement: (1) REFLECT for fault localization;
(2) maturity-aware update gating for stabilizing reliable skills while maintaining plasticity for uncertain ones; and (3) canonical structural refactoring
with rollback validation for eliminating redundancy
while preserving performance.

_•_ **An** **optimization** **perspective.** We show that
PSN’s architectural design induces learning dynamics with structural parallels to neural network
training, suggesting general principles for continual learning across representational paradigms.


**2** **Method**


**Problem setup.** We consider an embodied agent
acting in a partially observable Markov decision
process (POMDP) (Kaelbling et al., 1998). The
agent receives a stream of open-ended tasks _T_ =
_τ_ 1 _, τ_ 2 _, . . ._, each specified in natural language and
_{_ _}_
associated with a goal predicate _gτ_ : 0 _,_ 1,
_S_ _→{_ _}_
where _S_ denotes the state space. Tasks arrive
sequentially and may vary in difficulty, horizon
length, and compositional structure. The agent
must continually acquire, refine, and reorganize
reusable skills to solve future tasks by leveraging
past experience.
We present an online framework for continually
constructing, optimizing, and refactoring a Programmatic Skill Network. It evolves through a
recurrent loop that couples symbolic planning, execution, failure-driven repair, and success-driven
structural refactoring. We first define the core objects and operators that constitute the network, then
describe the planning and learning mechanisms.


**2.1** **Programmatic Skill Networks (PSN)**


A skill _s_ = ( _s,_ _s,_ _s,_ CHILDREN( _s_ )) is a sym_C_ _P_ _E_
bolic program where _s_ denotes control flow, _s_
_C_ _P_
parameters, _Es_ = ( _Es_ [pre] _[,][ E]_ _s_ [post] ) preconditions/postconditions, and CHILDREN( _s_ ) invoked subskills.



This precondition-effect structure is analogous to
programmatic laws in symbolic world modeling
(Khan et al., 2025a). The agent maintains a directed network _Nt_ = ( _St, Lt_ ) where nodes _St_ are
skills and edges _Lt_ represent invocations.

Executing skill _s_ yields ( _fs, δs_ ) where _δs_
_∈_
0 _,_ 1 indicates success and _fs_ aggregates feed_{_ _}_
back from the environment. The system records a
finite invocation trace . Given feedback _fs_, RE_T_

FLECT computes repair proposal [˜] _s_ identifying
_∇_
faulty control flow, preconditions, parameters, or
subskills. For invoked subskills _s_ _[′]_ _∈_ Children( _s_ ),
responsibility propagates as


˜ _s′_ = REFLECT( ˜ _s, s_ _[′]_ ) _,_ (1)
_∇_ _∇_


yielding finite credit assignment over executed subgraphs.


Each skill maintains scalar value _V_ ( _s_ ) = _p_ ˆ _s_ _us_

_−_
where _p_ ˆ _s_ is success rate with Laplace smoothing
and _us_ is an uncertainty term that decreases as
more executions are observed. This value summarizes long-term skill reliability and serves a dual
role: guiding skill selection during planning and
modulating update frequency during optimization.


Beyond behavioral repair, the PSN evolves
through structure-level rewrites such as merging redundant skills, abstracting shared routines, pruning
irrelevant branches, and rewiring invocation links.
These operations are treated as discrete architecture
updates and are validated through rollback-based
safety checks (Section 2.5).


**LLM implementation.** In our implementation,
operators such as REFLECT are instantiated via
prompted LLMs. The framework defines information flow _structure_ (e.g., what information is available, output formats, update timing) while LLMs
provide the generative capacity to synthesize, diagnose, and repair programs within this structure.
Critically, the learning dynamics we observe (Section 3) emerge from the _architectural_ _choices_ of
PSN (e.g., the compositional network structure,
the execution trace-based credit assignment, the
maturity-gated updates, and the canonical refactor operations) rather than from the internal mechanisms of the LLM. This separation allows the
framework to be instantiated with different code
generation backends while preserving its continual
learning properties.



2


Observation





















































Action



_ot_ : Observation at time step
_ft_ : Feedback at time step _t_



_s_
_ωt_



_S_ ( _g_ ) : Selected skill based on goal _[g]_



: Skill node
: Task success indicator



_ωt_ : Task at time step
_Nt_ : PSN at time step



_Pt_ : LLM generated plan at time step



_t_ _t_ _ωst_ : Skill node: Task success indicator _ωtt_ : Task at time step: PSN at time step _tt_ _S_ ( _Pg_ ) _t_ : Selected skill based on goal : LLM generated plan at time step _t_ _→P_ ˜ _ts_ : Repair proposal for skill: LLM generated plan at time step _s_ _t_



_→P_ ˜ _ts_ : Repair proposal for skill: LLM generated plan at time step _s_



Figure 1: The Programmatic Skill Network (PSN) framework. The agent maintains a skill network _t_ where
_N_
the _hybrid planner_ selects or synthesizes skills; the _PSN manager_ executes them. On failure, the _skill optimizer_
performs trace-based credit assignment; on success, the _online refactor_ restructures the network. This induces
learning dynamics analogous to neural network training: fault localization as backpropagation, maturity gating as
learning rate scheduling, and refactoring as architecture search.



**2.2** **Network-Aware Hybrid Planner**


The planner prioritizes reuse of the existing PSN
via symbolic backward-chaining before invoking
LLM-based forward planning. Each skill _s_ is
treated as an operator with preconditions _s_ and
_E_ [pre]
postconditions _s_ . Starting from the goal pred_E_ [post]
icate, the planner selects skills whose postconditions satisfy current subgoals:


_S_ ( _g_ ) = _s_ : _s_ _g_ _,_ (2)
_{_ _E_ [post] _⇒_ _}_


and recursively expands unmet preconditions.
When multiple skills satisfy a subgoal, ties are broken by _V_ ( _s_ ), favoring skills with higher empirical
reliability. Skill selection uses Boltzmann exploration (Sutton et al., 1998) over the value function
_V_ ( _s_ ), balancing exploitation of reliable skills with
exploration of uncertain ones. If no skill can reduce
a subgoal, the planner invokes an LLM-based forward planner _Pt_ [LLM] = PLAN( _gτt,_ _t_ ). Successful
_N_
plans are distilled into new symbolic skills via the
execution pipeline described next.


**2.3** **Execution and Trace Construction**


Given a plan _Pt_ = [ _s_ 1 _, . . ., sk_ ], the PSN manager
synthesizes a candidate skill


_st_ = CODEGEN( _Pt,_ Context _t_ ) _,_ (3)


where Context _t_ includes the task description, current network _t_, and execution history. The syn_N_
thesized skill defines control flow _st_, parameters
_C_
_st_, and pre/postconditions _st_, and is inserted into
_P_ _E_



the PSN with invocation links to its children. Executing _st_ produces a skill execution trace:


EXECUTE( _st_ ) ( _ft, δt,_ _t_ ) _,_ (4)
_→_ _T_


where _δt_ 0 _,_ 1 indicates task success, _ft_ ag_∈{_ _}_
gregates environment feedback and critic signals,
and the trace _Tt_ records each invoked skill as a tuple _⟨s, σ_ [pre] _, σ_ [post] _,_ status _⟩_ with symbolic state snapshots _σ_ . The trace serves as supervision for both
optimization and refactoring. Preconditions and
postconditions are incrementally calibrated from
observed success/fail states and empirical transitions.


**2.4** **Skill Optimization via Trace-Based Credit**
**Assignment**


When execution fails (i.e., _δt_ = 0), the skill optimizer performs localized behavioral repair via
structured fault localization. Unlike approaches
that discover world dynamics in natural language
(Sun et al., 2024) or learn function libraries offline
(Stengel-Eskin et al., 2024), PSN performs online,
trace-based credit assignment over executable skill
compositions. Given feedback _ft_ and trace _Tt_, the
REFLECT operator computes a repair proposal for
each executed skill:


˜ _s_ = REFLECT( _ft, s_ ; _t_ ) _,_ (5)
_∇_ _T_


identifying faulty control flow, violated preconditions, misaligned parameters, or incorrect subskill
effects. Concretely, PSN separates _credit assign-_
_ment_ from _code modification_ through a two-phase



3


process: failure signals are first propagated _top-_
_down_ along the executed skill invocation trace to
decompose responsibility across composite skills
and their subskills (symbolic differentiation), after
which localized symbolic edits are applied _bottom-_
_up_ to individual skills in a dependency-respecting
order (gradient application). Proposals propagate
in reverse execution order along the invocation
trace; skills not in _Tt_ receive no updates. Each affected skill is updated via _s_ PATCH( _s,_ [˜] _s_ ). The
_←_ _∇_
complete two-phase optimization procedure of the
skill optimizer, including the top-down symbolic
differentiation and bottom-up gradient application
are described in Appendix A.
To stabilize learning, updates are constrained
by a rolling buffer of the 5 most recent repair proposals, preventing contradictory edits. Update frequency is further modulated by skill maturity:


_P_ (update _s_ ) = (1 _−ϵ_ ) _·σ_ ( _γ_ (0 _._ 6 _−V_ ( _s_ )))+ _ϵ,_ (6)

The constant 0 _._ 6 serves as a soft maturity pivot
rather than a bound on _V_ ( _s_ ): it marks the inflection
point at which a skill is considered sufficiently reliable to gradually reduce update frequency, while
still allowing occasional repairs under compositional failures. _σ_ is the sigmoid function, _γ_ = 5 _._ 0
controls threshold sharpness, and _ϵ_ = 0 _._ 1 ensures minimum update probability. Mature skills
( _V_ ( _s_ ) _≈_ 1) stabilize with low update probability,
while immature skills remain plastic.


**2.5** **Online Structural Refactoring**


The online skill refactor controls structural growth
via semantics-preserving refactorings, applying
architecture-level rewrites that increase skill reuse
and maintain network compactness. While code
refactoring has been used to discover generalizable
abstractions offline (Stengel-Eskin et al., 2024),
PSN performs online refactoring that adapts to errors and redundancies emerging during continual
learning. While the skill optimizer repairs individual skill programs, refactor operates at the network
level, targeting redundancy and missed abstractions
that emerge over continual learning.


**Canonical refactor cases.** We restrict refactor to
five structural relationships: (i) _Parametric cover-_
_age_ : one skill is a strict specialization of another
admitting parameterized generalization. (ii) _Be-_
_havioral coverage_ : a composite skill reimplements
existing functionality. (iii) _Sibling specializations_ :
multiple skills suggest a missing abstraction. (iv)



_Common subskill extraction_ : multiple skills share
identical sub-operations. (v) _Duplication_ : two
skills are functionally equivalent. Each admits a
fixed rewrite rule; visual illustrations are provided
in Appendix B.


**Candidate discovery and rewrites.** Given a successfully executed skill _st_, refactor operates on a
restricted candidate set: parents and children of _st_,
plus top-5 semantically related skills by embedding
similarity. For each detected relationship, deterministic rewrites are applied (wrapper conversion, call
substitution, abstract skill synthesis, shared subskill extraction, or canonical merging). Refactor
does not introduce new behavioral logic, it only reorganizes existing programs and invocation links.


**Safety via rollback validation.** All refactor proposals are tentative. Given a refactored candidate
network _Nt_ _[′]_ [,] [the] [system] [evaluates] [short-horizon]
performance on a sliding window of 3 recent tasks
involving affected skills. If the task success rate
drops by more than 20%, the refactor is reverted
using logged inverse operations.


**3** **An Optimization Perspective on PSN**


Having presented PSN’s concrete mechanisms
(Section 2), we can observe that the system’s learning dynamics exhibit structural parallels to neural
network training. While other neuro-symbolic systems embed symbolic rules inside differentiable
models (d’Avila Garcez et al., 2019; Manhaeve
et al., 2018) or use gradient-free skill-based routing
(Chen et al., 2025), PSN embeds learning dynamics
inside symbolic programs. This interpretive lens
clarifies how PSN’s architectural choices collectively induce coherent continual learning behavior,
independent of the LLM backend.


**Implicit structure-behavior trade-off.** Let _N_ =
( _S, L_ ) denote the current PSN. The system’s behavior can be viewed as implicitly optimizing a
composite objective:


_J_ ( _N_ ) = _R_ task + _R_ reliab + _R_ struct + _R_ cons _,_ (7)


balancing **task** success, skill **reliab** ility, **struct** ural
compactness, and semantic **cons** istency. While
never explicitly optimized, each PSN module performs localized improvements to different components of _J_ ( _N_ ).

**Operator-objective correspondence.** REFLECT
acts as _symbolic differentiation_ : when a task fails,



4


**Method** **Wooden Tool** **Stone Tool** **Iron Tool** **Diamond Tool** **Obsidian**


ReAct N/A (0/3) N/A (0/3) N/A (0/3) N/A (0/3)     Reflexion N/A (0/3) N/A (0/3) N/A (0/3) N/A (0/3)      AutoGPT 92 _±_ 72 (3/3) 94 _±_ 72 (3/3) 135 _±_ 103 (3/3) N/A (0/3)     Voyager 6 _±_ 2 (3/3) **11** _±_ **2 (3/3)** 21 _±_ 7 (3/3) 102 (1/3)     Voyager* 6 _±_ 2 (3/3) 12 _±_ 3 (3/3) 23 _±_ 5 (3/3) N/A (0/3) N/A (0/3)
PSN w/o Optimizer **5** _±_ **2 (3/3)** 12 _±_ 2 (3/3) 25 _±_ 4 (3/3) N/A (0/3) N/A (0/3)
PSN (Ours) **5** _±_ **2 (3/3)** **11** _±_ **3 (3/3)** **19** _±_ **4 (3/3)** **51** _±_ **9 (3/3)** **77 (1/3)**


Table 1: Tech tree mastery on Minecraft. We report the mean/std iterations an agent uses to unlock an item over
three runs. For example, PSN successfully unlocks the diamond tool in all three runs, on average using 51 iterations;
while Voyager (Wang et al., 2024a) succeeds in one run using 102 iterations. Results of previous methods are from
the Voyager paper. - indicates results obtained using Voyager’s open-sourced code with GPT-5-mini (same as ours).
N/A represents the failure to unlock an item across all runs. - represents unreported previous result.



it identifies which control-flow branches, preconditions, parameters, and subskill compositions contributed to the error, producing structured repair
proposals that reduce _R_ task and _R_ cons. Like backpropagation, credit is assigned only along the executed path, with non-executed skills receiving no
updates. This selective credit assignment avoids the
noise of updating uninvolved skills, mirroring how
gradients flow only through activated paths in neural nets. Maturity-aware gating functions as _adap-_
_tive learning rates_ : mature skills with high _V_ ( _s_ )
receive infrequent updates (analogous to freezing
converged layers), while immature skills remain
plastic, reducing _R_ reliab by preventing catastrophic
forgetting. Refactor performs _symbolic neural ar-_
_chitecture_ _search_ : merging redundant skills, extracting reusable abstractions, and pruning unnecessary branches to reduce struct. Rollback-based
_R_
validation functions as a symbolic trust region.


**Multi-scale** **learning** **dynamics.** PSN learning
unfolds across three coupled timescales: (1) _Fast_ :
fault localization performs frequent behavioral repair at every execution. (2) _Intermediate_ : maturitybased stabilization progressively freezes reliable
skills over 10–50 executions. (3) _Slow_ : structural
refactor reorganizes stabilized behaviors every 5–
10 successful executions. This yields a coherent
dynamic: optimize behavior locally and rapidly,
stabilize reliable skills over time, and restructure
only after behaviors have converged.


**Scope of the analogy.** The neural network analogy is **partial** . PSN operates over discrete symbolic programs rather than continuous parameters,
produces structured edit proposals rather than numeric derivatives, and relies on binary success/failure signals rather than differentiable losses. Nevertheless, it reveals that stability-plasticity tradeoffs,



Figure 2: Tech tree mastery on Minecraft.


compositional credit assignment, and architecture
search emerge as general principles when learning structured representations. This suggests that
insights from neural network optimization may inform symbolic learning systems, and vice versa.


**4** **Experiments and Analysis**


We evaluate Programmatic Skill Networks (PSN)
on two complementary embodied benchmarks:
**MineDojo** (Fan et al., 2022), which supports longhorizon open-ended Minecraft tasks with rich action spaces and diverse goal specifications, and
**Crafter** (Hafner, 2022), a lightweight survival environment with a structured technology progression that stresses continual learning and compositional reuse. Across both environments, we evaluate (i) end-task performance, (ii) continual learning
dynamics (learning/forgetting), (iii) compositional
generalization, and (iv) network structural properties (growth, reuse, redundancy) induced by refactor and maturity-aware optimization.


**4.1** **Experimental Setup**


We leverage OpenAI’s gpt-5-mini-2025-08-07
for all the operators across both environments. The



5


Figure 3: Cumulative Reward on Crafter. Shorter curves
indicate earlier _agent_ _death_ due to Crafter’s survival
mechanics (hostile mobs, hunger, hazards).


Minecraft simulator is built on top of MineDojo
and leverages Mineflayer JavaScript APIs for motor
controls (PrismarineJS). For the Crafter environment, we implemented a Mineflayer-like Python
API system for the control of the Crafter bot. PSN
operators (e.g., CODEGEN and REFLECT) are instantiated by prompted LLMs. Example prompts
are provided in Appendix D.
We compare PSN against representative LLMagent baselines and ablations. **ReAct** (Yao et al.,
2023), a prompting-based agent that interleaves
reasoning and action without persistent structured
skills. **Reflexion** (Shinn et al., 2023), an agent
self-reflects over failures but does not maintain a
compositional programmatic skill network. **Au-**
**toGPT** (Significant Gravitas, 2023), a planningcentric agent that decomposes tasks into multi-step
plans and executes generated code or action sequences autonomously. It maintains a short-term
memory of past actions and observations, but treats
generated plans and code fragments as ephemeral
artifacts rather than persistent, reusable skills. **Voy-**
**ager** (Wang et al., 2024a), an agent that maintains
a flat skill library and retrieves skills via similarity, without trace-based symbolic credit assignment
and canonical structural refactor as in PSN.


**4.2** **Main Results**


**Minecraft Tech Tree Mastery.** Figure 2 and Table 1 compare agents in terms of technology tree
progression, measured by the number of iterations.
Progressing along the tech tree requires solving
increasingly long-horizon and compositional tasks,
where later-stage tools depend on reliable execution
and reuse of earlier skills. PSN exhibits substantially faster and more stable progression than all
baselines. ReAct and Reflexion fail to unlock any
tool-level milestones. AutoGPT completes early


Figure 4: Skill Retention Rate under continual learning
setting on Minecraft. PSN consistently preserves previously mastered skills, while Voyager exhibits severe
catastrophic forgetting as training progresses.


stage objectives but struggles to sustain progress
beyond iron-level tools, exhibiting high variance.
Voyager achieves consistent progress through iron
tools, but slows significantly at the diamond stage.
In contrast, PSN continues to unlock higher-tier
items with fewer attempts and lower variance, indicating that persistent programmatic skills, tracebased credit assignment, and structural refactoring
enable sustained long-horizon competence. For
obsidian acquisition, PSN executes a multi-step
procedure (i.e., bucket crafting, water-lava interaction, and diamond-pickaxe mining) which encapsulated as a single composed skill that extensively reuses previously learned subskills, illustrating PSN’s ability to compress long-horizon behaviors into reusable programmatic abstractions.


**Crafter.** Figure 3 reports cumulative episode reward on Crafter, which reflects the agent’s ability
to survive, gather resources, and make continual
progress under dense feedback. Unlike Minecraftstyle benchmarks that emphasize sparse milestone
completion, Crafter requires sustained stability
where early mistakes can compound. PSN consistently achieves higher cumulative reward. Voyager
achieves more stable returns than planning-only
baselines, but remains limited by its flat skill library.
By contrast, PSN maintains stable and steadily increasing reward throughout training, demonstrating
that its mechanisms generalize beyond sparse, longhorizon tasks to dense-reward continual learning
settings.


**4.3** **Generalization**


**Continual Learning over Task Streams (Tempo-**
**ral Generalization).** Since the continual skill ac


6


Figure 5: The cumulative success rate of tasks for PSN
w/ and w/o maturity gating, on Minecraft.


quisition efficiency of PSN can be observed in Figure 2, we evaluate PSN’s ability to acquire increasingly complex skills from a sequential task stream
while avoiding catastrophic forgetting. Tasks are
presented in a fixed curriculum following the technology tree [2] . Each task is trained until its success
rate exceeds a predefined threshold (marked as mastered), or until a maximum number of attempts is
reached. To measure forgetting, we introduce the
_Skill Retention Rate (SRR)_ : once a task is mastered,
it is periodically re-evaluated after each subsequent
task is mastered, and SRR is defined as the cumulative success rate across all such re-evaluations. As
shown in Figure 4, PSN consistently preserves earlier skills as training progresses, whereas Voyager
exhibits severe backward interference, with retention rapidly degrading as new skills are learned.
These results demonstrate that structured credit
assignment and maturity-aware stabilization are
critical for robust continual skill acquisition.


**Compositional** **Generalization** **via** **Network-**
**Aware** **Skill** **Reuse.** We hypothesize that PSN
solves unseen compositional tasks by reusing and
recombining existing skills rather than synthesizing new ones. To test this, we introduce a controlled baseline, PSN (Create New Skills), which
bypasses backward chaining and always synthesizes a new skill for each task. Figure 6 compares
skill repertoire sizes as training progresses. Early
in training, both variants grow similarly as foundational skills are acquired. However, the gap widens
over time: PSN’s repertoire plateaus while PSN
(Create New Skills) continues to accumulate skills.
This indicates that PSN increasingly grounds new


2 _Mine wood_ _→_ _Craft table →_ _Craft wooden pickaxe →_
_Craft stone pickaxe →_ _Mine iron →_ _Smelt iron →_ _Craft iron_
_pickaxe_ .



Figure 6: Growth of the skill library over training. In
PSN (Create New Skills), the agent always synthesizes
a new skill for each task. Compared to baselines, PSN
reuses and optimizes existing skills, maintaining a compact skill repertoire.


tasks in its existing skill network via backward
chaining, achieving compositional generalization
through reuse rather than proliferation. Notably,
PSN’s repertoire even decreases in later iterations,
suggesting that the refactoring mechanism actively
merges redundant helper functions over time.


**4.4** **Ablation Study**


**End-to-End Optimizer.** We ablate the symbolic
optimizer to disentangle the effect of optimization
from that of skill representation. As shown in Table 1, PSN without the optimizer achieves performance comparable to Voyager on early- and midstage tools (wooden, stone, and iron). However,
this variant fails to reliably progress to later-stage
objectives such as diamond tools and obsidian, mirroring Voyager’s degradation under increasing task
depth. In contrast, the full PSN consistently unlocks higher-tier items with substantially fewer iterations. This gap indicates that the optimizer is not
required to make skills functional, but is critical for
repairing brittle behaviors and enabling stable scaling to long-horizon, deeply compositional tasks.


**Maturity-aware update gating gradually stabi-**
**lizes learned skills.** Figure 5 compares cumulative task success rates for PSN with and without
maturity-aware update gating. Without stabilization, converged skills are repeatedly modified by
downstream failures, leading to oscillatory behavior. By contrast, maturity-aware gating progressively reduces the update frequency of reliable
skills while allowing immature skills to remain
plastic. As a result, PSN with stabilization achieves
higher cumulative success rates and more stable



7


learning dynamics.


**Refactor Regulates the Network Growth.** Figure 6 shows how the size of the skill library evolves
as learning progresses. Without structural refactoring, Voyager’s skill library grows rapidly, accumulating redundant or overly specialized skills. This
uncontrolled growth increases planning complexity
and degrades efficiency. In contrast, PSN maintains a significantly more compact skill network by
identifying canonical redundancy patterns and applying semantics-preserving rewrites. As a result,
the effective growth rate is substantially reduced
even as task complexity increases.


**Offline Refactor vs.** **Online Refactor.** To test
whether structural compression alone is sufficient,
we apply an _offline refactor_ to Voyager’s learned
skill library using a strong LLM (Claude Opus 4.5),
which refactored its 58 existing skills into 7 generic
skills, 20 lightweight wrappers, and 38 unchanged
skills (65 total), denoted as Voyager-R. While this
offline refactoring significantly reduces redundancy
(in terms of repeating code blocks), it does not yield
the same behavioral robustness. When evaluated on
a fixed sequence of compositional tasks [3], VoyagerR achieves a success rate of 0.6875, compared to
0.8462 for PSN with online refactoring. This gap
indicates that refactoring is most effective when
performed _online_ and tightly coupled with execution feedback, rather than applied once to a static
skill library.


**5** **Related Work**


**Skill Learning and Hierarchical RL.** Hierarchical
RL studies temporal abstraction via options (Sutton
et al., 1999; Barto and Mahadevan, 2003; Bacon
et al., 2017; Eysenbach et al., 2019) and modular routing (Andreas et al., 2016; Xu et al., 2018;
Zhang et al., 2018; Shazeer et al., 2017; Riquelme
et al., 2021). LLM-guided approaches segment
trajectories into reusable skills via variational inference (Fu et al., 2024). Unlike these work, PSN
represents skills as executable programs with explicit control flow and pre/postconditions.
**LLM-based** **Agents** **and** **Program** **Synthesis.**
LLM agents maintain code memories or skill repositories (Yao et al., 2023; Schick et al., 2023; Ahn


3Fixed task sequence: _Mine_ _wood_ _→_ _Craft_ _planks_ _→_
_Craft_ _table_ _→_ _Craft_ _wooden_ _pickaxe_ _→_ _Mine_ _cobblestone_
_→_ _Craft stone pickaxe →_ _Mine iron →_ _Smelt iron →_ _Craft_
_iron pickaxe_ . All methods are evaluated on the identical task
sequence without retraining.



et al., 2022; Wang et al., 2024a; Prabhu et al., 2025).
CodeAct (Wang et al., 2024b) uses executable code
as a unified action space; ReGAL (Stengel-Eskin
et al., 2024) learns function libraries via refactoring capturing environment dynamics; MINDcraft
(White et al., 2025) studies multi-agent task solving; ASI (Wang et al., 2025c) induces programmatic skills on-the-fly for web agents; AgentCoder
(Huang et al., 2023) uses multi-agent code generation; DiVE (Sun et al., 2024) builds natural language knowledge repertoires. Wang et al. (2025a)
show refactoring facilitates coding agents. Selfimproving agents learn via RL-based skill accumulation (Wang et al., 2025b), reasoning memory
(Ouyang et al., 2025), or progressive skill disclosure (Anthropic, 2025). PSN organizes skills into
a compositional network with trace-based credit
assignment and structural refactoring.

**Neuro-Symbolic Learning and Architecture Op-**
**timization.** Neuro-symbolic systems integrate
symbolic structures with differentiable computation (d’Avila Garcez et al., 2019; Baydin et al.,
2018; Badreddine et al., 2022; Manhaeve et al.,
2018). OneLife (Khan et al., 2025a) models dynamics via programmatic laws with precondition-effect
structures, analogous to PSN’s skill representation.
Symbolic-MoE (Chen et al., 2025) routes through
skill-based experts; EFA (Khan et al., 2025b) infers executable abstractions for math. Neural architecture search prunes and restructures networks
(Zoph and Le, 2017; Han et al., 2016; Tan and Le,
2019), with techniques like learning rate scheduling enabling stability-plasticity tradeoffs (Howard
and Ruder, 2018; Yosinski et al., 2014; Rusu et al.,
2016). PSN draws on both traditions: it embeds
learning dynamics inside symbolic programs rather
than embedding symbols in differentiable models,
while performing architecture-search-like refactoring under rollback validation.


**6** **Conclusion**


We introduced PSN, a framework for continual skill
acquisition where executable symbolic programs
form a compositional network that evolves through
experience. PSN’s three mechanisms (i.e., tracebased credit assignment, maturity-aware update
gating, and canonical structural refactoring) induce
learning dynamics with structural parallels to neural network training. Experiments on Minecraft
and Crafter demonstrated faster skill acquisition,
reduced forgetting, and superior compositional gen


8


eralization, suggesting that principles from neural
network optimization can inform the design of symbolic learning systems.


**Limitations**


Our current implementation of PSN operates under constrained computational resources, resulting in an effectively batch-size-one online learning
regime. This significantly limits the degree of parallelism in both skill execution and reflection-driven
optimization, and prevents us from fully exploring
large-scale network-level learning dynamics.
Moreover, the current reflection and refactoring process lacks a formal projection guarantee in
the symbolic program space. While empirical improvements are consistently observed, the theoretical properties of symbolic projection, convergence,
and optimality remain to be established.
Nevertheless, we believe these limitations are
not fundamental to the PSN paradigm. With the
continued scaling of large language models, increased computational budgets, and more efficient
parallel execution infrastructures, future iterations
of PSN are expected to support large-batch learning, stronger theoretical guarantees, and substantially improved optimization efficiency.


**Acknowledgements**


This work is supported by the Canada CIFAR AI
Chair Program and the Canada NSERC Discovery
Grant (RGPIN-2021-03115).


**References**


Michael Ahn, Anthony Brohan, Noah Brown, Yevgen Chebotar, Omar Cortes, Byron David, Chelsea
Finn, Chuyuan Fu, Keerthana Gopalakrishnan, Karol
Hausman, Alex Herzog, Daniel Ho, Jasmine Hsu,
Julian Ibarz, Brian Ichter, Alex Irpan, Eric Jang,
Rosario Jauregui Ruano, Kyle Jeffrey, and 26 others. 2022. Do as i can, not as i say: Grounding
language in robotic affordances. In _Conference on_
_Robot Learning (CoRL)_ .


Jacob Andreas, Marcus Rohrbach, Trevor Darrell, and
Dan Klein. 2016. Neural module networks. In _Pro-_
_ceedings of the IEEE Conference on Computer Vision_
_and Pattern Recognition (CVPR)_, pages 39–48.


Anthropic. 2025. [Equipping agents for the real world](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)
[with agent skills.](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills) Anthropic Engineering Blog.


Pierre-Luc Bacon, Jean Harb, and Doina Precup. 2017.
The option-critic architecture. _Proceedings_ _of_ _the_
_AAAI Conference on Artificial Intelligence_ .



Samy Badreddine, Artur d’Avila Garcez, Luciano Serafini, and Michael Spranger. 2022. [Logic tensor net-](https://doi.org/10.1016/j.artint.2021.103649)
[works.](https://doi.org/10.1016/j.artint.2021.103649) _Artificial Intelligence_, 303:103649.


Andrew G Barto and Sridhar Mahadevan. 2003. Recent advances in hierarchical reinforcement learning.
_Discrete Event Dynamic Systems_ .


Atilim Gunes Baydin, Barak A. Pearlmutter, Alexey Andreyevich Radul, and Jeffrey Mark Siskind. 2018.
Automatic [differentiation](http://jmlr.org/papers/v18/17-468.html) in machine learning: a
[survey.](http://jmlr.org/papers/v18/17-468.html) _Journal_ _of_ _Machine_ _Learning_ _Research_,
18(153):1–43.


Justin Chih-Yao Chen, Sukwon Yun, Elias StengelEskin, Tianlong Chen, and Mohit Bansal. 2025. Symbolic mixture-of-experts: Adaptive skill-based routing for heterogeneous reasoning. _arXiv_ _preprint_
_arXiv:2503.05641_ .


Artur d’Avila Garcez, Marco Gori, Luis C. Lamb,
Luciano Serafini, Michael Spranger, and Son N.
Tran. 2019. Neural-symbolic [computing:](https://arxiv.org/abs/1905.06088) An effective methodology for principled integration of
machine [learning](https://arxiv.org/abs/1905.06088) and reasoning. _arXiv_ _preprint_
_arXiv:1905.06088_ .


Benjamin Eysenbach, Abhishek Gupta, Julian Ibarz,
and Sergey Levine. 2019. Diversity is all you need:
Learning skills without a reward function. In _Inter-_
_national_ _Conference_ _on_ _Learning_ _Representations_
_(ICLR)_ .


Linxi Fan, Guanzhi Wang, Yunfan Jiang, Ajay Mandlekar, Yuncong Yang, Haoyi Zhu, Andrew Tang,
De-An Huang, Yuke Zhu, and Anima Anandkumar.
2022. Minedojo: Building open-ended embodied
agents with internet-scale knowledge. In _Advances_
_in Neural Information Processing Systems (NeurIPS),_
_Datasets and Benchmarks Track_ . Outstanding Paper
Award.


Haotian Fu, Pratyusha Sharma, Elias Stengel-Eskin,
George Konidaris, Nicolas Le Roux, Marc-Alexandre
Côté, and Xingdi Yuan. 2024. [Language-guided skill](https://proceedings.mlr.press/v235/fu24e.html)
[learning with temporal variational inference.](https://proceedings.mlr.press/v235/fu24e.html) In _Pro-_
_ceedings_ _of_ _the_ _41st_ _International_ _Conference_ _on_
_Machine_ _Learning_, volume 235 of _Proceedings_ _of_
_Machine_ _Learning_ _Research_, pages 14135–14156.
PMLR. ICML 2024.


Danijar Hafner. 2022. Benchmarking the spectrum of
agent capabilities. In _International_ _Conference_ _on_
_Learning Representations (ICLR)_ .


Song Han, Huizi Mao, and William J Dally. 2016. Deep
compression: Compressing deep neural networks
with pruning, trained quantization and huffman coding. In _International Conference on Learning Repre-_
_sentations (ICLR)_ .


Jeremy Howard and Sebastian Ruder. 2018. Universal
language model fine-tuning for text classification.
In _Proceedings_ _of_ _the_ _56th_ _Annual_ _Meeting_ _of_ _the_
_Association for Computational Linguistics (ACL)_ .



9


Dong Huang, Jie M Zhang, Michael Luck, Qingwen
Bu, Yuhao Qing, and Heming Cui. 2023. Agentcoder: Multi-agent-based code generation with iterative testing and optimisation. _arXiv_ _preprint_
_arXiv:2312.13010_ .


Leslie Pack Kaelbling, Michael L Littman, and Anthony R Cassandra. 1998. Planning and acting in
partially observable stochastic domains. _Artificial_
_Intelligence_, 101(1–2):99–134.


Zaid Khan, Archiki Prasad, Elias Stengel-Eskin, Jaemin
Cho, and Mohit Bansal. 2025a. One life to learn:
Inferring symbolic world models for stochastic environments from unguided exploration. _arXiv preprint_
_arXiv:2510.12088_ .


Zaid Khan, Elias Stengel-Eskin, Archiki Prasad, Jaemin
Cho, and Mohit Bansal. 2025b. Executable functional abstractions: Inferring generative programs
for advanced math problems. _arXiv_ _preprint_
_arXiv:2504.09763_ .


Robin Manhaeve, Sebastijan Dumancic, Angelika Kimmig, Thomas Demeester, and Luc De Raedt. 2018.
DeepProbLog: [Neural probabilistic logic program-](https://proceedings.neurips.cc/paper/2018/hash/dc5d637ed5e62c36ecb73b654b05ba2a-Abstract.html)
[ming.](https://proceedings.neurips.cc/paper/2018/hash/dc5d637ed5e62c36ecb73b654b05ba2a-Abstract.html) In _Advances in Neural Information Processing_
_Systems_, volume 31, pages 3753–3763. Curran Associates, Inc.


Siru Ouyang, Jun Yan, I Hsu, Yanfei Chen, Ke Jiang,
Zifeng Wang, Rujun Han, Long T Le, Samira Daruki,
Xiangru Tang, and 1 others. 2025. Reasoningbank:
Scaling agent self-evolving with reasoning memory.
_arXiv preprint arXiv:2509.25140_ .


Viraj Prabhu, Yutong Dai, Matthew Fernandez, Jing Gu,
Krithika Ramakrishnan, Yanqi Luo, Silvio Savarese,
Caiming Xiong, Junnan Li, Zeyuan Chen, and 1 others. 2025. Walt: Web agents that learn tools. _arXiv_
_preprint arXiv:2510.01524_ .


PrismarineJS. Mineflayer: A [minecraft](https://github.com/PrismarineJS/mineflayer) bot api for
[node.js.](https://github.com/PrismarineJS/mineflayer) GitHub repository.


Carlos Riquelme, Joan Puigcerver, Basil Mustafa,
Maxim Neumann, Rodolphe Jenatton, André Susano Pinto, Daniel Keysers, and Neil Houlsby. 2021.
Scaling vision with sparse mixture of experts. In
_Advances in Neural Information Processing Systems_
_(NeurIPS)_ .


David E Rumelhart, Geoffrey E Hinton, and Ronald J
Williams. 1986. Learning representations by backpropagating errors. _Nature_, 323(6088):533–536.


Andrei A Rusu, Neil C Rabinowitz, Guillaume Desjardins, Hubert Soyer, James Kirkpatrick, Koray
Kavukcuoglu, Razvan Pascanu, and Raia Hadsell.
2016. Progressive neural networks. _arXiv preprint_
_arXiv:1606.04671_ .


Timo Schick, Jane Dwivedi-Yu, Roberto Dessì, Roberta
Raileanu, Maria Lomeli, Luke Zettlemoyer, Nicola
Cancedda, and Thomas Scialom. 2023. Toolformer:
Language models can teach themselves to use tools.



In _Advances in Neural Information Processing Sys-_
_tems (NeurIPS)_ .


Noam Shazeer, Azalia Mirhoseini, Krzysztof Maziarz,
Andy Davis, Quoc Le, Geoffrey Hinton, and Jeff
Dean. 2017. Outrageously large neural networks:
The sparsely-gated mixture-of-experts layer. In _In-_
_ternational Conference on Learning Representations_
_(ICLR)_ .


Noah Shinn, Federico Cassano, Ashwin Gopinath,
Karthik Narasimhan, and Shunyu Yao. 2023. Reflexion: Language agents with verbal reinforcement
learning. In _Advances_ _in_ _Neural_ _Information_ _Pro-_
_cessing Systems (NeurIPS)_ .


Significant Gravitas. 2023. [Autogpt.](https://github.com/Significant-Gravitas/AutoGPT) Open-source software.


Elias Stengel-Eskin, Archiki Prasad, and Mohit Bansal.
2024. ReGAL: Refactoring programs to discover
[generalizable](https://proceedings.mlr.press/v235/stengel-eskin24a.html) abstractions. In _Proceedings_ _of_ _the_
_41st International Conference on Machine Learning_,
volume 235 of _Proceedings_ _of_ _Machine_ _Learning_
_Research_, pages 46605–46624. PMLR. ICML 2024.


Zhiyuan Sun, Haochen Shi, Marc-Alexandre Côté, Glen
Berseth, Xingdi Yuan, and Bang Liu. 2024. [Enhanc-](https://doi.org/10.18653/v1/2024.findings-emnlp.202)
[ing agent learning through world dynamics modeling.](https://doi.org/10.18653/v1/2024.findings-emnlp.202)
In _Findings_ _of_ _the_ _Association_ _for_ _Computational_
_Linguistics:_ _EMNLP_ _2024_, pages 3534–3568, Miami, Florida, USA. Association for Computational
Linguistics.


Richard S Sutton, Andrew G Barto, and 1 others. 1998.
_Reinforcement learning:_ _An introduction_, volume 1.
MIT press Cambridge.


Richard S Sutton, Doina Precup, and Satinder Singh.
1999. Between mdps and semi-mdps: A framework
for temporal abstraction in reinforcement learning.
_Artificial Intelligence_, 112(1–2):181–211.


Mingxing Tan and Quoc V. Le. 2019. Efficientnet: Rethinking model scaling for convolutional neural networks. In _Proceedings of the International Confer-_
_ence on Machine Learning (ICML)_ .


Guanzhi Wang, Yuqi Xie, Yunfan Jiang, Ajay Mandlekar, Chaowei Xiao, Yuke Zhu, Linxi Fan, and Anima Anandkumar. 2024a. Voyager: An open-ended
embodied agent with large language models. _Trans-_
_actions on Machine Learning Research (TMLR)_ .


Haonan Wang, Junfeng Sun, Xingdi Yuan,
Ruoyao Wang, and Ziang Xiao. 2025a. Bytesized32refactored: Towards an extensible interactive
text games corpus for llm world modeling and
evaluation. _arXiv preprint arXiv:2509.23979_ .


Jiongxiao Wang, Qiaojing Yan, Yawei Wang, Yijun
Tian, Soumya Smruti Mishra, Zhichao Xu, Megha
Gandhi, Panpan Xu, and Lin Lee Cheong. 2025b.
Reinforcement learning for self-improving agent with
skill library. _arXiv preprint arXiv:2512.17102_ .



10


Xingyao Wang, Yangyi Chen, Lifan Yuan, Yizhe Zhang,
Yunzhu Li, Hao Peng, and Heng Ji. 2024b. [Exe-](https://proceedings.mlr.press/v235/wang24h.html)
cutable code actions [elicit](https://proceedings.mlr.press/v235/wang24h.html) better LLM agents. In
_Proceedings of the 41st International Conference on_
_Machine_ _Learning_, volume 235 of _Proceedings_ _of_
_Machine_ _Learning_ _Research_, pages 50208–50232.
PMLR. ICML 2024.


Zora Zhiruo Wang, Apurva Gandhi, Graham Neubig, and Daniel Fried. 2025c. Inducing programmatic skills for agentic tasks. _arXiv_ _preprint_
_arXiv:2504.06821_ .


Isadora White, Kolby Nottingham, Ayush Maniar, Max
Robinson, Hansen Lillemark, Mehul Maheshwari,
Lianhui Qin, and Prithviraj Ammanabrolu. 2025.
Collaborating action by action: A multi-agent llm
framework for embodied reasoning. _arXiv preprint_
_arXiv:2504.17950_ .


Danfei Xu, Suraj Nair, Yuke Zhu, Julian Gao, Animesh
Garg, Li Fei-Fei, and Silvio Savarese. 2018. Neural
task programming: Learning to generalize across
hierarchical tasks. In _IEEE International Conference_
_on Robotics and Automation (ICRA)_, pages 1–8.


Shunyu Yao, Jeffrey Zhao, Dian Yu, Nan Du, Izhak
Shafran, Karthik Narasimhan, and Yuan Cao. 2023.
React: Synergizing reasoning and acting in language
models. In _International_ _Conference_ _on_ _Learning_
_Representations (ICLR)_ .


Jason Yosinski, Jeff Clune, Yoshua Bengio, and Hod
Lipson. 2014. How transferable are features in deep
neural networks? In _Advances in Neural Information_
_Processing Systems (NeurIPS)_ .


Amy Zhang, Sainbayar Sukhbaatar, Adam Lerer, Arthur
Szlam, and Rob Fergus. 2018. Composable planning
with attributes. In _Proceedings_ _of_ _the_ _35th_ _Inter-_
_national Conference on Machine Learning (ICML)_,
pages 5842–5851.


Barret Zoph and Quoc V Le. 2017. Neural architecture
search with reinforcement learning. In _International_
_Conference on Learning Representations (ICLR)_ .



**A** **Two-Phase Optimization Algorithm of**
**Skill Optimizer**


This section provides a formal algorithmic specification of the two-phase skill optimization process
described in the main paper. Algorithm 1 summarizes the complete procedure. A key distinction in
our framework is between a skill’s _feedback_ and
its _gradients_ : feedback indicates _what went wrong_,
while gradients encode _how the skill should be mod-_
_ified_ .


**A.1** **Feedback vs.** **Gradients**


For a skill _s_, we denote by _fs_ the feedback signal
assigned to _s_ after task execution. This feedback
may arise from task failure, unmet subgoals, or
trace-level diagnostics. Crucially, _fs_ does not directly specify how to modify _s_ .
Instead, PSN performs a symbolic analysis step
that converts feedback into gradients. We denote
this process as:


               -                REFLECT( _s, fs,_ Subskill( _s_ )) _gs,_ _fs′_ _s′∈_ Subskill( _s_ ) _,_
_→_ _{_ _}_

where _gs_ (also written as [˜] _s_ ) is a gradient-like
_∇_
modification proposal for _s_, and _fs′_ are newly generated feedback signals for each sub-skill invoked
by _s_ .
This operation implements a symbolic form of
differentiation over the skill invocation structure.


**A.2** **Phase I: Top-down Feedback**
**Backpropagation**


Phase I performs _top-down feedback backpropaga-_
_tion_ over the skill network. Starting from a skill
that fails to complete a task, PSN recursively applies REFLECT following the invocation relations
induced by the execution trace.
At each skill _s_, symbolic differentiation decomposes _fs_ into:


 - a local gradient proposal _gs_ describing how _s_
itself should be modified, and


 - feedback signals _fs′_ assigned to sub-skills
_{_ _}_
_s_ _[′]_ _∈_ Subskill( _s_ ).

This process continues until no further sub-skills
require feedback propagation. The result of Phase
I is a _pending optimization subgraph_ consisting of:


opt = ( _s, gs_ ) _,_
_G_ _{_ _}_

i.e., a connected subgraph of skills paired with
their gradient proposals. No skill code is modified
during this phase.



11


**A.3** **Phase II: Bottom-up Gradient**
**Application**


Phase II applies gradients in a _bottom-up_ manner over opt. Skills are updated in an order that
_G_
respects dependency relations, starting from leaf
skills and proceeding toward higher-level skills.
For a skill _s_ with gradient proposal _gs_, the update
is performed via:


             -             APPLYGRADIENTS _s,_ _gs,_ _s_ _._
_C_


Here, _s_ is a _context object_ that aggregates op_C_
timization reports returned by sub-skills that have
already been updated. Let


_s_ := Subskill( _s_ )
_S_


denote the set of sub-skills invoked by _s_ . The context _Cs_ is constructed as:


          -          _s_ := CONSIDER OPTIMIZEREPORT( _s_ ) _,_
_C_ _S_


which summarizes feedback signals derived from
the updated sub-skills.
Updates are realized through program-level
rewrite, patch, or diff operations on the skill code.
After updating _s_, the optimizer generates an _opti-_
_mization report_ summarizing the changes and their
effects. This report is propagated upward and used
to inform subsequent updates of parent skills, allowing higher-level skills to adapt consistently to
changes in their dependencies.


**A.4** **Algorithmic Interpretation**


The complete optimization step thus consists of
two strictly separated phases:


 - **Phase I:** Top-down symbolic differentiation to
propagate feedback _fs_ .
_{_ _}_

 - **Phase** **II:** Bottom-up application of gradient
proposals _gs_ .
_{_ _}_

This design explicitly decouples _credit assign-_
_ment_ from _code modification_ . While Phase I follows a chain-rule-like decomposition of feedback
signals, Phase II ensures that updates are applied
in a dependency-consistent order, preventing interference between skills during optimization.


**A.5** **Discussion**


By separating feedback propagation from gradient application, PSN generalizes the backward–
forward separation of neural backpropagation to



symbolic, programmatic skill networks. We find
this two-phase structure essential for stable optimization in deeply compositional and long-horizon
tasks.


**B** **Refactor Casebook**


This appendix presents a visual casebook of the
canonical refactor patterns supported by the Programmatic Skill Network (PSN). Each case corresponds to a distinct structural relationship between
skills and induces a deterministic graph rewrite.
All cases referenced in Section 2.5 are illustrated
in the Table 2 and below.

These refactor cases are exhaustive with respect
to the structural patterns observed in our experiments.


**B.1** **Case A: Parametric Coverage**


**Pattern.** One skill is a strict specialization of another skill that admits a parameterized generalization.


**Rewrite.** The specialized skill is replaced by a
thin wrapper that calls the generalized skill with
fixed parameter values.


**B.2** **Case B: Behavioral / Subgraph Coverage**


**Pattern.** A composite skill reimplements functionality that already exists as an independent skill
in the PSN, resulting in duplicated subgraphs.


**Rewrite.** The duplicated subgraph is removed
and replaced by a direct invocation of the existing
skill, yielding a simpler and more compositional
program structure.


**B.3** **Case C: Sibling Specializations**


**Pattern.** Two or more skills are specializations
of a latent, more general operation that is not yet
represented as a standalone skill in the network.


**Rewrite.** A new abstract skill is synthesized to
capture the shared structure, and all specialized
skills are rewritten as thin wrappers that invoke the
abstract skill with appropriate parameters.


**B.4** **Case D: Common Subskill Extraction**


**Pattern.** Multiple skills contain an identical or
highly similar sub-operation that is implemented
independently within each skill.



12


**Algorithm 1:** Two-Phase Skill Optimization in PSN ( _Phase I_ : top-down feedback backpropagation;
_Phase II_ : bottom-up gradient application)

**Input:** Root skill _s_ root, task feedback _fs_ root, execution trace
_T_
**Output:** Updated skills and optimization reports

**Definitions.** Subskill( _s_ ; _T_ ): sub-skills invoked by _s_ in _T_ ;
REFLECT( _s, fs,_ Subskill) ( _gs,_ _fs′_ );
_→_ _{_ _}_
APPLYGRADIENTS( _s, gs,_ ) ( _s_ [+] _, rs_ );
_C_ _→_



**Phase I: Top-down feedback backpropagation (symbolic differentiation).**
Initialize maps _G_ _←∅_ (gradients), _F_ _←∅_ (feedback);
Initialize queue _Q_ [( _s_ root _, fs_ root)];
_←_
**while** _Q ̸_ = _∅_ **do**



Pop ( _s, fs_ ) from _Q_ ;

[ _s_ ] _fs_ ;
_F_ _←_
_S_ _←_ Subskill( _s_ ; _T_ );
( _gs,_ _fs′_ _s′∈S_ ) REFLECT( _s, fs,_ );
_{_ _}_ _←_ _S_

[ _s_ ] _gs_ ;
_G_ _←_
**foreach** _s_ _[′]_ _∈S_ **do**



**if** _fs′_ = ∅ **then**

_[′]_



Push ( _s_ _[′]_ _, fs′_ ) into _Q_ ;



Let _H_ be the induced pending optimization subgraph over Dom( _G_ );



**Phase II: Bottom-up gradients application (dependency-respecting updates).**
Compute bottom-up order _π_ _←_ POSTORDER( _H_ );
Initialize report map _R ←∅_ ;
**foreach** _s in π_ **do**



_C_ _←_ CONSIDER( _{_ OPTIMIZEFEEDBACK( _s_ _[′]_ ) _| s_ _[′]_ _∈_ Subskill( _s_ ) _∩_ Dom( _R_ ) _}_ );
( _s_ [+] _, rs_ ) APPLYGRADIENTS( _s,_ [ _s_ ] _,_ );
_←_ _G_ _C_
Replace _s ←_ _s_ [+] in the skill net;

[ _s_ ] _rs_ ;
_R_ _←_



**return** _{s_ [+] _} and R_ ;



**Rewrite.** The shared subgraph is extracted into a
new reusable skill, and all original skills are rewritten to invoke this subskill instead of duplicating its
logic.


**B.5** **Case E: Duplication Removal**


**Pattern.** Two skills are functionally equivalent
up to naming differences or minor surface variations, leading to redundant representations in the
PSN.


**Rewrite.** The skill with higher empirical value
is retained as the canonical implementation, and
all invocation links to the redundant skill are redirected. The redundant skill is demoted to an alias
or removed from planning.



**C** **Operator Summary**


**C.1** **Symbolic Operators**


Table 3 summarizes the core symbolic operators
used in the Programmatic Skill Network (PSN),
which define the symbolic forward and backward
passes over program-structured skills.


**C.2** **System Operators**


Table 4 summarizes the system-level operators that
orchestrate planning, learning, and structural evolution of the Programmatic Skill Network (PSN).


**D** **Example Prompt Templates**


This appendix provides example prompt templates
used to instantiate PSN operators in our implementation. We emphasize that PSN does not rely on
specific prompt wording; the examples below serve



13


**Case** **Pattern** **Example and rewrite** **Illustration**


(A) Parametric coverage **Example:** mineLogs(type,num) generalizes mineOakLogs(num). Figure 7
**Rewrite:** mineOakLogs(num) := mineLogs(OAK,num).



(B) Behavioral / subgraph **Example:** craftCraftingTable inlines routines that exist as skills.
coverage **Rewrite:** replace duplicated blocks by calls to mineLogs and
craftPlanks.

(C) Sibling specializations **Example:** mineOakLogs(num) and mineBirchLogs(num) indicate a
missing abstraction. **Rewrite:** synthesize mineLogs(type,num) and
rewrite both as wrappers.

(D) Extract common sub- **Example:** both craftSticks and craftTable require
skill ensurePlanks(k). **Rewrite:** extract ensurePlanks(k) as a new
skill and replace both occurrences by a call.

(E) Duplication **Example:** two skills are near-identical up to naming/surface variations.
**Rewrite:** keep higher- _V_ ( _s_ ) canonical skill; redirect incoming links;
demote the other to an alias.



Figure 8


Figure 9


Figure 10


Figure 11



Table 2: Index of canonical refactor cases supported by PSN. Each case corresponds to a distinct structural
relationship and rewrite rule, with detailed illustrations provided in Appendix B.


**Parametric Coverage**















**Wrapper**



















Figure 7: Parametric coverage. A specialized skill is rewritten as a wrapper around a more general, parameterized
skill.



only as concrete realizations of the abstract operator interfaces defined in Section 2.


**D.1** **REFLECT Operator**


The example prompt for REFLECT Operator is
demonstrated in Figure 12. Note that, to accelerate
the speed of REFLECT Operator, we implement an
hybrid REFLECT Operator that combine the LLM
REFLECT with an rule-based REFLECT function
that extract frequent patterns recognized by LLM
REFLECT as a set of rules.


**Input.**


- Skill name and implementation code


- Execution feedback and failure signals




- Optional execution state, environment context,
and child-skill information


**Output.** A structured JSON record containing:


- Self-responsible issues with gradient type, magnitude, and direction


- Child-skill attributions with responsibility
weights


- Concrete code-level modification suggestions


**D.2** **Skill Optimization Operator**


We instantiate the skill optimization operator as a
patching procedure _s_ PATCH( _s,_ [˜] _s_ ), where [˜] _s_
_←_ _∇_ _∇_



14


**Subgraph Coverage**














|Before Refactoring<br>𝒩<br>𝑡|Col2|
|---|---|
|𝑎𝑠𝑦𝑛𝑐𝑓𝑢𝑛𝑐𝑡𝑖𝑜𝑛𝒄𝒓𝒂𝒇𝒕𝑷𝒊𝒄𝒌𝒂𝒙𝒆𝑡𝑦𝑝𝑒, 𝑛𝑢𝑚{<br>// Codes toGather & Craft Materials<br>// Codes toCraft Pickaxe in CratingTable<br>}<br><br>|𝑎𝑠𝑦𝑛𝑐𝑓𝑢𝑛𝑐𝑡𝑖𝑜𝑛𝒄𝒓𝒂𝒇𝒕𝑷𝒊𝒄𝒌𝒂𝒙𝒆𝑡𝑦𝑝𝑒, 𝑛𝑢𝑚{<br>// Codes toGather & Craft Materials<br>// Codes toCraft Pickaxe in CratingTable<br>}<br><br>|
|**craftSticks**<br>**craftPickaxe**(type, num)<br>**Refactor**<br>**Relationship**<br>**Detected**<br>**useCraftingTable**<br>**craftPlanks**|**craftSticks**<br>**craftPickaxe**(type, num)<br>**Refactor**<br>**Relationship**<br>**Detected**<br>**useCraftingTable**<br>**craftPlanks**|


|Call<br>Substitution|After Refactoring<br>𝒩<br>𝑡+1|
|---|---|
|**Call**<br>**Substitution**|𝑎𝑠𝑦𝑛𝑐𝑓𝑢𝑛𝑐𝑡𝑖𝑜𝑛𝒄𝒓𝒂𝒇𝒕𝑷𝒊𝒄𝒌𝒂𝒙𝒆𝑡𝑦𝑝𝑒, 𝑛𝑢𝑚{<br>…;<br>𝒄𝒓𝒂𝒇𝒕𝑺𝒕𝒊𝒄𝒌𝒔(𝑠𝑡𝑖𝑐𝑘_𝑛𝑢𝑚);<br>𝒄𝒓𝒂𝒇𝒕𝑰𝒏𝑪𝒓𝒂𝒇𝒕𝒊𝒏𝒈𝑻𝒂𝒃𝒍𝒆(𝑝𝑖𝑐𝑘𝑎𝑥𝑒, 𝑛𝑢𝑚)<br>}<br>**craftPlanks**<br>|
|𝒔𝟎𝒙→𝒔𝟎(𝒙|𝒔𝟏(𝒙))|𝒔𝟎𝒙→𝒔𝟎(𝒙|𝒔𝟏(𝒙))|
|𝒔𝟎𝒙→𝒔𝟎(𝒙|𝒔𝟏(𝒙))|**craftSticks**<br>**craftPickaxe**(type, num)<br>**useCraftingTable**<br><br>**Subgraph**<br>**Covering**|
|||



Figure 8: Behavioral (subgraph) coverage. Duplicated logic inside a composite skill is replaced by a call to an
existing reusable skill, preserving behavior while reducing redundancy.



is a structured set of issues and modification directions produced by REFLECT. The operator consumes a skill implementation together with layered
constraints and execution feedback, and outputs
a revised implementation along with an explicit
requirement-by-requirement audit trail for mandatory fixes. The detailed prompt is demonstrated in
Figure 13.


**E** **Additional Optimization Examples**


This appendix provides representative examples of
execution-level optimizations performed by PSN.
All examples are drawn from actual training runs
and are selected to illustrate recurring optimization patterns rather than to exhaustively enumerate
all repairs. Together, they demonstrate how tracebased symbolic credit assignment enables both localized fixes and coordinated optimization across
skill hierarchies. **Complete** **code** **diffs** **for** **opti-**
**mization cases are provided in Section F.**


**E.1** **Optimization Taxonomy**


Across experiments, frequent optimizations of PSN
fall into several recurring categories. Table 5 summarizes the most common failure signals and corresponding repair strategies.


**E.2** **Representative Optimization Cases**


**Example** **1:** **Resource** **Miscalculation**
**(craftWoodenPickaxe).** **Failure** **signal.**
The skill fails during execution with an error



indicating insufficient wooden planks. **Root cause.**
The original implementation underestimates
required resources by ignoring planks consumed
during intermediate stick crafting. **Repair.** Using
execution traces, PSN localizes the failure to
the resource calculation logic and updates the
material requirements to account for intermediate
crafting steps. A validation check is added
before execution to ensure sufficient materials
are available. **Outcome.** After repair, the skill
reliably computes correct resource requirements
and succeeds across repeated executions.


**Example** **2:** **Unsafe** **Fallback** **(ensureFlint).**
**Failure signal.** The skill exhibits silent or inconsistent failures when attempting to mine gravel. **Root**
**cause.** An unsafe fallback bypasses the system’s
primitive execution contract, preventing proper failure propagation to the planner. **Repair.** PSN removes the unsafe fallback and enforces fail-fast
behavior, ensuring that execution failures are explicitly surfaced and handled by upstream skills.
**Outcome.** The repaired skill behaves consistently
and enables reliable replanning under failure.


**Example** **3:** **Boundary** **Condition**
**(openChestAndRetrieve).** **Failure** **signal.**
Execution fails when attempting to retrieve items
from a chest due to insufficient inventory capacity.
**Root cause.** The skill assumes unlimited inventory
space and does not model capacity constraints.
**Repair.** The optimizer inserts an explicit capacity



15


|𝒔𝟎 𝒙|Col2|
|---|---|
|𝒔𝟏𝒙|𝒔𝟏𝒙|


|Col1|𝒔𝟎 𝒙|Col3|𝒔𝟐(𝜽, 𝒙)|𝒔𝟐(𝜽, 𝒙)|
|---|---|---|---|---|
|𝒩𝑡+|1<br>|𝒔𝟏𝒙|𝒔𝟏𝒙|𝒔𝟏𝒙|





















**Sibling Specializations**


|Before Refactoring<br>𝒔𝟎 𝒙<br>𝒔𝟏 𝒙 𝒩𝑡<br>𝑎𝑠𝑦𝑛𝑐𝑓𝑢𝑛𝑐𝑡𝑖𝑜𝑛𝒎𝒊𝒏𝒆𝑶𝒂𝒌𝑳𝒐𝒈𝒔 𝑛𝑢𝑚 {<br>// Implementation}|Abstract Skill<br>Synthesis<br>𝒔 (𝒙), 𝒔 (𝒙) →𝒔 (𝜽, 𝒙)<br>𝟎 𝟏 𝟐|
|---|---|
|𝑎𝑠𝑦𝑛𝑐𝑓𝑢𝑛𝑐𝑡𝑖𝑜𝑛𝒎𝒊𝒏𝒆𝑶𝒂𝒌𝑳𝒐𝒈𝒔𝑛𝑢𝑚{<br>// Implementation}|𝑎𝑠𝑦𝑛𝑐𝑓𝑢𝑛𝑐𝑡𝑖𝑜𝑛𝒎𝒊𝒏𝒆𝑶𝒂𝒌𝑳𝒐𝒈𝒔𝑛𝑢𝑚{<br>// Implementation}|
|𝑎𝑠𝑦𝑛𝑐𝑓𝑢𝑛𝑐𝑡𝑖𝑜𝑛𝒎𝒊𝒏𝒆𝑩𝒊𝒓𝒄𝒉𝑳𝒐𝒈𝒔𝑛𝑢𝑚{<br>// Implementation}|𝑎𝑠𝑦𝑛𝑐𝑓𝑢𝑛𝑐𝑡𝑖𝑜𝑛𝒎𝒊𝒏𝒆𝑩𝒊𝒓𝒄𝒉𝑳𝒐𝒈𝒔𝑛𝑢𝑚{<br>// Implementation}|
|**Refactor**<br>**Relationship**<br>**Detected**<br>**mine**<br>**mine**|**Refactor**<br>**Relationship**<br>**Detected**<br>**mine**<br>**mine**|


|Col1|After Refactoring<br>𝒔𝟎 𝒙 𝒔𝟐(𝜽, 𝒙)<br>𝒩𝑡+1 𝒔𝟏 𝒙<br>𝑎𝑠𝑦𝑛𝑐𝑓𝑢𝑛𝑐𝑡𝑖𝑜𝑛𝒎𝒊𝒏𝒆𝑶𝒂𝒌𝑳𝒐𝒈𝒔 𝑛𝑢𝑚 {<br>𝒎𝒊𝒏𝒆𝑳𝒐𝒈𝒔 ”𝑂𝑎𝑘𝐿𝑜𝑔”, 𝑛𝑢𝑚 }|Col3|
|---|---|---|
||**After Refactoring**<br>𝑎𝑠𝑦𝑛𝑐𝑓𝑢𝑛𝑐𝑡𝑖𝑜𝑛𝒎𝒊𝒏𝒆𝑶𝒂𝒌𝑳𝒐𝒈𝒔𝑛𝑢𝑚{<br>𝒎𝒊𝒏𝒆𝑳𝒐𝒈𝒔”𝑂𝑎𝑘𝐿𝑜𝑔”, 𝑛𝑢𝑚}<br>𝒩𝑡+1<br>𝒔𝟎𝒙<br>𝒔𝟏𝒙<br>𝒔𝟐(𝜽, 𝒙)|𝑎𝑠𝑦𝑛𝑐𝑓𝑢𝑛𝑐𝑡𝑖𝑜𝑛𝒎𝒊𝒏𝒆𝑶𝒂𝒌𝑳𝒐𝒈𝒔𝑛𝑢𝑚{<br>𝒎𝒊𝒏𝒆𝑳𝒐𝒈𝒔”𝑂𝑎𝑘𝐿𝑜𝑔”, 𝑛𝑢𝑚}|
||𝑎𝑠𝑦𝑛𝑐𝑓𝑢𝑛𝑐𝑡𝑖𝑜𝑛𝒎𝒊𝒏𝒆𝑩𝒊𝒓𝒄𝒉𝑳𝒐𝒈𝒔𝑛𝑢𝑚{<br>𝒎𝒊𝒏𝒆𝑳𝒐𝒈𝒔”𝐵𝑖𝑟𝑐ℎ𝐿𝑜𝑔”, 𝑛𝑢𝑚}|𝑎𝑠𝑦𝑛𝑐𝑓𝑢𝑛𝑐𝑡𝑖𝑜𝑛𝒎𝒊𝒏𝒆𝑩𝒊𝒓𝒄𝒉𝑳𝒐𝒈𝒔𝑛𝑢𝑚{<br>𝒎𝒊𝒏𝒆𝑳𝒐𝒈𝒔”𝐵𝑖𝑟𝑐ℎ𝐿𝑜𝑔”, 𝑛𝑢𝑚}|
||**mineLogs**(LogType, num)<br>**Sibling**<br>**Specializatoins**<br>**mine**<br>**mine**|**mineLogs**(LogType, num)<br>**Sibling**<br>**Specializatoins**<br>**mine**<br>**mine**|



Figure 9: Sibling specializations. Multiple specialized skills expose a missing higher-level abstraction that can be
explicitly synthesized and reused.



check and dynamically constrains the withdrawal
amount based on available inventory slots. **Out-**
**come.** The optimized skill adapts to varying
inventory states and avoids execution-time errors.


**Example** **4:** **Missing** **Preconditions**
**(ensureMetalIngots).** **Failure** **signal.** The
skill fails when attempting to smelt metal ingots
without access to a crafting table or furnace. **Root**
**cause.** The original implementation relies on
implicit assumptions about environmental setup.
**Repair.** PSN makes these assumptions explicit
by validating the presence of required crafting
stations and inserting corrective actions to locate
or construct them when missing. **Outcome.** The
repaired skill succeeds robustly across diverse
environment configurations.


**E.3** **Advanced Optimization:** **Cross-Skill**
**Credit Assignment**


Beyond single-skill repairs, PSN is able to propagate optimization signals across skill boundaries.In
particular, failures in a parent skill can trigger coordinated updates to both the parent and its dependent
subskills.


**Example** **5:** **Parent–Child** **Co-**
**Optimization** **(ensureRawIronAndFuel** _→_
**ensureFuel).** **Context.** The parent skill
ensureRawIronAndFuel invokes the subskill
ensureFuel to acquire sufficient fuel before mining and smelting iron. **Failure signal.** Execution



traces show that the parent skill proceeds despite
insufficient fuel being present in the inventory,
leading to cascading failures in downstream steps.
**Root** **cause.** The parent skill implicitly assumes
that successful completion of ensureFuel guarantees the availability of the required fuel.However,
the subskill employs coarse fallback behaviors
and does not explicitly verify that the desired fuel
items are obtained. **Coordinated** **repair.** PSN
assigns credit to both levels of the skill hierarchy
and performs simultaneous optimizations:


  - **Parent skill repair:** the parent skill is updated
to explicitly verify postconditions after invoking the subskill, checking for the presence of
coal or charcoal and triggering targeted recovery actions when verification fails.


  - **Subskill** **repair:** the subskill ensureFuel
is refined to reduce overly coarse fallbacks,
prioritize specific fuel types, and handle
inventory-capacity constraints more robustly.


**Outcome.** After co-optimization, the parent skill
reliably enforces its fuel preconditions, and the refined subskill consistently delivers the required resources. This example demonstrates PSN’s ability
to localize responsibility across skill boundaries
and to perform coordinated, semantics-preserving
optimization over compositional skill hierarchies.



16


|Col1|Afte|
|---|---|
||<br>𝒔𝟐(𝒙)|
|𝓝𝒕+𝟏|𝓝𝒕+𝟏|



















**Common Subskill**


|Before Refactoring<br>𝒔𝟎 𝒙<br>𝒔𝟏 𝒙 𝓝𝒕|Common Subskill<br>Extraction<br>𝒔 𝒙, 𝒔 𝒙<br>𝟎 𝟏<br>→𝒔 𝒙𝒔, 𝒔 𝒙𝒔<br>𝟎 𝟐 𝟏 𝟐|
|---|---|
|𝑎𝑠𝑦𝑛𝑐𝑓𝑢𝑛𝑐𝑡𝑖𝑜𝑛𝒄𝒓𝒂𝒇𝒕𝑪𝒓𝒂𝒇𝒕𝒊𝒏𝒈𝑻𝒂𝒃𝒍𝒆() {<br>// Implementation}|𝑎𝑠𝑦𝑛𝑐𝑓𝑢𝑛𝑐𝑡𝑖𝑜𝑛𝒄𝒓𝒂𝒇𝒕𝑪𝒓𝒂𝒇𝒕𝒊𝒏𝒈𝑻𝒂𝒃𝒍𝒆() {<br>// Implementation}|
|𝑎𝑠𝑦𝑛𝑐𝑓𝑢𝑛𝑐𝑡𝑖𝑜𝑛𝒄𝒓𝒂𝒇𝒕𝑾𝒐𝒐𝒅𝒆𝒏𝒑𝒊𝒄𝒌𝒂𝒙𝒆()<br>{// Implementation}||
|**Refactor**<br>**Relationship**<br>**Detected**<br>**craft**<br>**craft**|**Refactor**<br>**Relationship**<br>**Detected**<br>**craft**<br>**craft**|


|Col1|After Refactoring<br>𝒔𝟐(𝒙) 𝒔𝟎 𝒙𝒔𝟐<br>𝒔𝟏 𝒙𝒔𝟐<br>𝓝𝒕+𝟏<br>𝑎𝑠𝑦𝑛𝑐𝑓𝑢𝑛𝑐𝑡𝑖𝑜𝑛𝒄𝒓𝒂𝒇𝒕𝑪𝒓𝒂𝒇𝒕𝒊𝒏𝒈𝑻𝒂𝒃𝒍𝒆() {<br>… ; ensurePlanks(4); … }|
|---|---|
||𝑎𝑠𝑦𝑛𝑐𝑓𝑢𝑛𝑐𝑡𝑖𝑜𝑛𝒄𝒓𝒂𝒇𝒕𝑪𝒓𝒂𝒇𝒕𝒊𝒏𝒈𝑻𝒂𝒃𝒍𝒆() {<br>… ; **ensurePlanks**(4); … }|
||𝑎𝑠𝑦𝑛𝑐𝑓𝑢𝑛𝑐𝑡𝑖𝑜𝑛𝒄𝒓𝒂𝒇𝒕𝑾𝒐𝒐𝒅𝒆𝒏𝒑𝒊𝒄𝒌𝒂𝒙𝒆()<br>… ; **ensurePlanks**(2); … }|
||**Common**<br>**Subskill**<br>**craft**<br>**craft**<br>**ensurePlanks**(num)|



Figure 10: Common subskill extraction. Repeated sub-operations across different skills are factored into a shared
subskill, improving reuse and reducing duplication.


**Duplication**
















|𝒂𝒓𝒈𝒎𝒂𝒙 𝑽 𝒔<br>𝒔∈𝒔𝟎,𝒔𝟏|Col2|
|---|---|
|||










|Before Refactoring<br>𝒔𝟎 𝒙<br>𝒔𝟏 𝒙 𝓝𝒕<br>𝑎𝑠𝑦𝑛𝑐𝑓𝑢𝑛𝑐𝑡𝑖𝑜𝑛𝒎𝒊𝒏𝒆𝑰𝒓𝒐𝒏𝑶𝒓𝒆_𝒐𝒍𝒅() {<br>// Implementation}|Duplication<br>Removal|After Refactoring<br>𝒂𝒓𝒈𝒎𝒂𝒙 𝑽 𝒔<br>𝒔∈𝒔𝟎,𝒔𝟏<br>𝓝𝒕+𝟏|
|---|---|---|
|𝑎𝑠𝑦𝑛𝑐𝑓𝑢𝑛𝑐𝑡𝑖𝑜𝑛𝒎𝒊𝒏𝒆𝑰𝒓𝒐𝒏𝑶𝒓𝒆_𝒐𝒍𝒅() {<br>// Implementation}|𝑎𝑠𝑦𝑛𝑐𝑓𝑢𝑛𝑐𝑡𝑖𝑜𝑛𝒎𝒊𝒏𝒆𝑰𝒓𝒐𝒏𝑶𝒓𝒆_𝒐𝒍𝒅() {<br>// Implementation}|𝑎𝑠𝑦𝑛𝑐𝑓𝑢𝑛𝑐𝑡𝑖𝑜𝑛𝒎𝒊𝒏𝒆𝑰𝒓𝒐𝒏𝑶𝒓𝒆() {<br>// Implementation}|
|𝑎𝑠𝑦𝑛𝑐𝑓𝑢𝑛𝑐𝑡𝑖𝑜𝑛𝒎𝒊𝒏𝒆𝑰𝒓𝒐𝒏𝑶𝒓𝒆_𝒏𝒆𝒘() {<br>// Implementation}|𝑎𝑠𝑦𝑛𝑐𝑓𝑢𝑛𝑐𝑡𝑖𝑜𝑛𝒎𝒊𝒏𝒆𝑰𝒓𝒐𝒏𝑶𝒓𝒆_𝒏𝒆𝒘() {<br>// Implementation}|**mine**<br>**mine**<br>**mine**<br>**Duplication**<br>**Removal**|
|𝑎𝑠𝑦𝑛𝑐𝑓𝑢𝑛𝑐𝑡𝑖𝑜𝑛𝒎𝒊𝒏𝒆𝑰𝒓𝒐𝒏𝑶𝒓𝒆_𝒏𝒆𝒘() {<br>// Implementation}|𝒔𝟎𝒙, 𝒔𝟏𝒙→𝒂𝒓𝒈𝒎𝒂𝒙<br>𝒔∈𝒔𝟎,𝒔𝟏<br>𝑽𝒔|𝒔𝟎𝒙, 𝒔𝟏𝒙→𝒂𝒓𝒈𝒎𝒂𝒙<br>𝒔∈𝒔𝟎,𝒔𝟏<br>𝑽𝒔|
|**Refactor**<br>**Relationship**<br>**Detected**<br>**mine**<br>**mine**|**Refactor**<br>**Relationship**<br>**Detected**<br>**mine**<br>**mine**|**Refactor**<br>**Relationship**<br>**Detected**<br>**mine**<br>**mine**|
|**Refactor**<br>**Relationship**<br>**Detected**<br>**mine**<br>**mine**|||



Figure 11: Duplication removal. Functionally equivalent skills are merged into a single canonical representation.


17


**Operator** **Domain** _→_ **Codomain** **Semantic role** **Example in PSN**
EXECUTE ( _s, E_ ) _→_ ( _fs, δs_ ) Symbolic forward operator that ex- EXECUTE( _s_ craftTable) runs the
ecutes a skill program _s_ in environ- composed skill craft crafting
ment _E_, producing structured feed- table, records the invocation
back _fs_ and a success flag _δs_ _∈_ trace and state transitions, and
_{_ 0 _,_ 1 _}_ . returns whether the goal predicate

_gτ_ is satisfied.



REFLECT ( _fs, s_ ) _→_ _∇_ [�] _s_ Symbolic differentiation operator
that performs top-down credit assignment over the PSN, yielding a
finite, localized symbolic pseudogradient _∇_ [�] _s_ = _∂sfs_ . The operator
identifies faulty control flow, misaligned parameters, incorrect preconditions, or subskill effects, and
serves as a discrete, structural analogue of backpropagation in neural
networks.



REFLECT( _fs_ craftTable _, s_ craftTable)
detects that craftTable failed due
to missing planks and proposes
edits to collect wood logs and craft
planks for crafting CraftingTable.



Table 3: Symbolic operators defining forward execution and backward credit assignment over program-structured
skills in the PSN.


**Operator** **Domain** _→_ **Codomain** **System role** **Example in PSN**
PLAN ( _gτt_ _, Nt_ ) _→_ _Pt_ [LLM] Fallback forward planner in- For the task “obtain diamond”,
voked when backward-chaining PLAN proposes a long-horizon
over existing skills cannot plan involving mining iron, smeltground a subgoal, producing ing ingots, crafting pickaxes, and
exploratory plans beyond the mining diamond ore.
current PSN.



CODEGEN ( _Pt,_ Context _t_ ) _→_ _st_ Skill synthesis operator that distills a high-level plan into a new
symbolic skill neuron with control flow, parameters, and pre/postconditions.


OPTIMIZE ( _Nt, st, ft_ ) _→Nt_ +1 Skill optimizer that applies
symbolic backpropagation when
a task fails, repairing the
faulty subnetwork N( _st_ ) via REFLECT.


REFACTOR ( _Nt, st, ft_ ) _→Nt_ +1 Online structural refactor operator that performs symbolic neural architecture search (NAS)
when a task succeeds, merging, abstracting, pruning, and
rewiring skills.


embed _s �→_ embed( _s_ ) Semantic embedding operator
used for similarity-based retrieval during refactor, enabling
detection of related skills beyond local graph neighborhoods.

_P_ (update _s_ ) _V_ ( _s_ ) _�→_ [0 _,_ 1] Maturity-aware update gate that
controls how frequently symbolic derivatives are applied to
a skill, stabilizing mature skills
while keeping immature ones
plastic.



Given a plan _Pt_ =

[getWood _,_ craftPlanks _,_ craftTable],
CODEGEN creates a reusable skill
craftCraftingTable with an
explicit loop and parameterized
inventory checks.


If craftStonePickaxe fails
due to insufficient cobblestone,
OPTIMIZE propagates symbolic
edits to mineCobblestone, inserting a loop until enough stone is
collected.


After learning both mineOakLogs
and mineBirchLogs, REFACTOR
synthesizes a generalized
mineLogs(log_type, num)
and rewrites both original skills as
wrappers.


High similarity between
embed( _s_ craftStick) and
embed( _s_ craftTable) helps identify
a common subroutine for ensuring
plank availability.


For a navigation skill with high
_V_ ( _s_ ), _P_ (update _s_ ) becomes small,
so OPTIMIZE rarely modifies it;
newly synthesized skills are updated aggressively until they stabilize.



Table 4: System-level operators that orchestrate planning, optimization, and structural evolution of the PSN.


18


1

2 **Skill:** {input.skill_name}


3

4 **Code:**

5 ‘‘‘javascript

6 {input.skill_code}

7 ‘‘‘


8

9 **Feedback:**

10 {input.feedback_content}


11

12 **Feedback Type:** {input.feedback_type}

13 {execution_state_section}

14 {children_section}

15 {env_section}

16 {primitive_section}

17 {propagated_section}

18 {api_knowledge_section}

19 {reasoning_examples_section}


20

21 **Analysis Tasks:**

22 1. Identify the root cause of the failure

23 2. Determine if the issue is in THIS skill or in a child skill

24 3. For each identified issue, specify:

25 - The type of gradient (logic, parameter_semantic, physical_constraint, error_handling, etc.)

26 - The magnitude (0.0 to 1.0, higher = more urgent)

27 - The direction (what needs to change)

28 - The suggested_fix (REQUIRED: concrete code modification suggestions)


29

30 **IMPORTANT:** For physical_constraint issues (placement, resource depletion, pathfinding):

31 - Provide SPECIFIC code changes in suggested_fix

32 - Example: "Expand maxDistance from 6 to 16, expand vertical search from [-1,1] to [-2,2]"


33

34 Return JSON:

35 {{

36 "self_issues": [

37 {{

38 "gradient_type": "logic|parameter_semantic|physical_constraint|error_handling|interface",

39 "magnitude": 0.0-1.0,

40 "direction": "what needs to change",

41 "evidence": "supporting evidence from feedback",

42 "suggested_fix": "REQUIRED: specific code changes to make"

43 }}

44 ],

45 "child_issues": [

46 {{

47 "child_skill": "name",

48 "issue_description": "...",

49 "responsibility": "...",

50 "weight": 0.0-1.0

51 }}

52 ],

53 "reasoning": "overall analysis"

54 }}


Figure 12: Example prompt template instantiating the REFLECT operator.


19


1 === SYSTEM ===
2 You are a helpful assistant that optimizes Minecraft skill code.
3
4 READ THE LAYERED CONTEXT CAREFULLY!
5 The context is organized in layers of importance:
6 - LAYER 1 (MUST FIX): Critical issues that MUST be addressed. Your code will be REJECTED if not fixed.
7 - LAYER 2 (LOCALIZATION): Specific lines and areas to focus on.
8 - LAYER 3 (CONSTRAINTS): Rules you must follow (don’t change signature, don’t redefine external skills).
9
10 CRITICAL RULES:
11 1. Fix ALL issues mentioned in LAYER 1 - these are mandatory
12 2. Focus your changes on the areas mentioned in LAYER 2
13 3. Follow ALL constraints in LAYER 3
14 4. Return COMPLETE code with all brackets matched - do NOT truncate
15 5. Keep the function signature unchanged
16 6. Do NOT add new functions with same names as external skills
17 7. AUTOMATION ONLY - We only support fully automated skills:
18 - Use Mineflayer APIs (bot.craft, bot.dig, bot.placeBlock, bot.equip, etc.)
19 - Do NOT require user interaction (windowOpen events, "press E", manual operations)
20 - Do NOT convert automated code to interactive/manual flows
21 - All operations must be programmatic and automatic
22 8. CODE CONCISENESS: Keep code concise. Do NOT add unnecessary helper functions.
23 - Only keep helper functions that are ACTUALLY USED
24 - Remove redundant code. If optimized code is longer than original, review and simplify.
25 9. DO NOT REDEFINE SYSTEM CONTROL PRIMITIVES: The following functions are PROVIDED BY THE SYSTEM.
26 DO NOT create local functions with these exact names - they already exist externally:
27
28 mineBlock, craftItem, smeltItem, exploreUntil, placeItem,
29 killMob, useChest, givePlacedItemBack, shoot, waitForMobRemoved
30
31 CONTROL PRIMITIVE API SIGNATURES (CRITICAL - Parameter Types):
32 {primitives_knowledge}
33
34 SIMPLIFICATION PRINCIPLE (MANDATORY - Code Bloat Prevention):
35 {simplification_principle}
36
37 ENVIRONMENT KNOWLEDGE AWARENESS:
38 {environment_knowledge}
39
40 Return a JSON object:
41 {
42 "issues": [
43 { "type": "issue_type", "description": "brief description" }
44 ],
45 "optimized_code": "complete optimized code in JavaScript",
46 "change_summary": "brief description of changes",
47 "requirements_addressed": [
48 {
49 "requirement_index": 1,
50 "how_addressed": "how LAYER 1 requirement was addressed",
51 "code_location": "line number or function name"
52 }
53 ]
54 }
55
56 The "requirements_addressed" field is MANDATORY!
57 You must explain how EACH requirement from LAYER 1 was addressed.
58
59 === HUMAN ===
60 Skill: {skill_name}
61
62 {edit_context}
63
64 FULL CODE (for reference):
65 {skill_code}
66 {wrapper_warning}
67
68 ADDITIONAL CONTEXT:
69 Skill description:
70 {skill_description}
71
72 Gradient:
73 {gradient_summary}
74
75 Child skills feedback:
76 {child_feedback_summary}
77
78 {forward_propagation_info}
79 {current_state_info}
80
81 Recent optimization history (last {momentum_window} feedbacks):
82 {optimization_history}
83
84 Statistics:
85 - Total executions: {total_executions}
86 - Success rate: {success_rate}
87 - Failed executions: {failed_executions}
88
89 CODE FORMATTING REQUIREMENTS:
90 - The optimized_code MUST be properly formatted with:
91 - One statement per line
92 - Proper indentation (2 spaces)
93 - Newlines after { and before }
94 - DO NOT compress multiple statements into a single line
95
96 Return only JSON.


Figure 13: Example prompt template instantiating the20skill optimization operator ( _s_ PATCH( _s,_ [˜] _s_ )) as a
_←_ _∇_
constrained program-repair step.


Category Failure Signal Typical Repair


Resource miscalculation insufficient materials Correct resource accounting
Unsafe fallback silent execution failure Enforce fail-fast behavior
Boundary condition inventory full Add capacity-aware constraints
Missing preconditions missing crafting station Explicit precondition validation
API misuse invalid recipe or action Correct API invocation
Cross-skill contract downstream semantic failure Parent–child co-optimization


Table 5: Common optimization patterns discovered and
repaired by PSN.


21


**F** **Detailed Code Diffs for Optimization Examples**


This section provides complete code diffs for the representative optimization cases described in Section E.
Table 6 summarizes all cases, and Table 7 shows the mapping from gradient signals to implemented fixes.


**Skill** **Bug Type** **Error Pattern** **Key Fix**


craftWoodenPickaxe Resource Calc insufficient materials Count planks for sticks
ensureFlint Unsafe Fallback Invalid token Remove bot.dig() fallback
openChestAndRetrieve Boundary destination full Pre-check capacity
ensureMetalIngots Precondition requires crafting table Validate & place table


Table 6: Summary of optimization cases with bug types and key fixes.


**Gradient Signal** **Interpretation** **Resulting Fix**


“Fix resource_management” Math error in counting Add plank calculation for sticks
“fail loudly rather than fallback” Unsafe silent failure Replace fallback with explicit error
“Limit withdraw amounts” Boundary violation Add capacity calculation
“guarantee crafting table present” Missing precondition Add validation and placement logic


Table 7: Mapping from gradient signals to implemented fixes.


22


**F.1** **Example 1:** **craftWoodenPickaxe (Resource Miscalculation)**


**Failure Signal.**


Error: Cannot craft wooden_pickaxe: insufficient planks. Needed 3, have 0.


**Root Cause.** The original implementation underestimates required resources by ignoring planks consumed
during intermediate stick crafting.
**Gradient Signal.**







**Code Diff.**









23


24


**F.2** **Example 2:** **ensureFlint (Unsafe Fallback)**


**Failure Signal.**


**Root Cause.** An unsafe fallback using bot.dig() directly bypasses the system’s primitive execution
contract, preventing proper failure propagation.
**Gradient Signal.**







**Code Diff.**













25


26


**F.3** **Example 3:** **openChestAndRetrieve (Boundary Condition)**


**Failure Signal.**


Error: Destination full while withdrawing items from chest


**Root Cause.** The skill assumes unlimited inventory space and does not model capacity constraints.
**Gradient Signal.**







**Code Diff.**





27


**F.4** **Example 4:** **ensureMetalIngots (Missing Precondition)**


**Failure Signal.**


**Root** **Cause.** The original implementation relies on implicit assumptions about environmental setup
without validating the presence of required crafting stations.

**Gradient Signal.**







**Code Diff.**


28


29


**F.5** **Example 5:** **Cross-Skill Co-Optimization**


Beyond single-skill repairs, PSN propagates optimization signals across skill boundaries. This example
shows coordinated parent–child optimization between ensureRawIronAndFuel (parent) and ensureFuel
(child).


**Failure Signal.** The parent skill proceeds despite insufficient fuel, causing cascading failures in downstream smelting steps.
**Coordinated** **Repair.** PSN assigns credit to both levels of the hierarchy and performs simultaneous
optimizations.


_Parent skill repair_ (ensureRawIronAndFuel):


_Child skill repair_ (ensureFuel):


This demonstrates PSN’s ability to localize responsibility across skill boundaries and perform coordinated optimization over compositional skill hierarchies.


30


