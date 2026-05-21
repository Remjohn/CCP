## **Towards Reliable Code-as-Policies: A Neuro-Symbolic** **Framework for Embodied Task Planning**

**Sanghyun Ahn** [1] **, Wonje Choi** [1] **, Junyong Lee** [1] **, Jinwoo Park** [2] **, Honguk Woo** [1] _[,]_ [2] _[∗]_

1Department of Computer Science and Engineering, Sungkyunkwan University
2Department of Artificial Intelligence, Sungkyunkwan University
{shyuni5, wjchoi1995, ljy7488, pjw971022, hwoo}@skku.edu


**Abstract**


Recent advances in large language models (LLMs) have enabled the automatic
generation of executable code for task planning and control in embodied agents
such as robots, demonstrating the potential of LLM-based embodied intelligence.
However, these LLM-based code-as-policies approaches often suffer from limited
environmental grounding, particularly in dynamic or partially observable settings,
leading to suboptimal task success rates due to incorrect or incomplete code
generation. In this work, we propose a neuro-symbolic embodied task planning
framework that incorporates explicit symbolic verification and interactive validation
processes during code generation. In the validation phase, the framework generates
exploratory code that actively interacts with the environment to acquire missing
observations while preserving task-relevant states. This integrated process enhances
the grounding of generated code, resulting in improved task reliability and success
rates in complex environments. We evaluate our framework on RLBench and in realworld settings across dynamic, partially observable scenarios. Experimental results
demonstrate that our framework improves task success rates by 46.2% over Code
as Policies baselines and attains over 86.8% executability of task-relevant actions,
thereby enhancing the reliability of task planning in dynamic environments.


**1** **Introduction**


Recent advances in embodied control have leveraged large language models (LLMs) to enable
flexible, instruction following, effectively bridging natural language understanding with executable
actions in physical environments. For instance, SayCan [1] combines LLM-based task interpretation
with a reinforcement learning (RL) affordance model to construct a hybrid policy that grounds highlevel language instructions, such as “bring me the sponge.” into sequences of low-level, predefined
robotic skills. Building on this foundation, subsequent approaches have explored more expressive
and compositional modes of action specification through code generation, introducing the paradigm
of code-as-policies [2, 3, 4], where LLMs directly generate executable code to control embodied
agents. This shift enables task planning that is more modular, interpretable, and adaptable to diverse
environments, highlighting the potential of LLMs as general-purpose planners for robotic control.


While LLM-based code-as-policies approaches have demonstrated promising capabilities in fully
observable and well-structured settings, their reliability deteriorates in dynamic or partially observable
environments, where perceptual input is often sparse, delayed, or ambiguous. These limitations lead
to incorrect or incomplete code generation, ultimately resulting in suboptimal task performance. For
example, attempting to grasp a fragile object without access to accurate depth or height estimation may
lead to dropping or damaging the object, preventing task completion. These challenges underscore


_∗_ Corresponding author


39th Conference on Neural Information Processing Systems (NeurIPS 2025).


**(2) Verified & Validated Code Generation (ours)**






|Col1|Check if drawers are empty|
|---|---|
|**Ungrounded Code**<br>…<br>…<br>pick(**middle_drawer_handle**, …)<br>pull(**middle_drawer_handle**, …)|**Ungrounded Code**<br>…<br>…<br>pick(**middle_drawer_handle**, …)<br>pull(**middle_drawer_handle**, …)|
































|top_drawer is empty<br>bottom_drawer is full|Col2|Col3|
|---|---|---|
|**top_drawer is empty**<br>**bottom_drawer is full**|||











Figure 1: Concept of our NESYRO framework illustrated with an example of a room-cleaning task
where drawer states are initially unknown. While (1) naive code generation fails without detecting
missing observations, (2) NESYRO recursively probes the environment to recover drawer states,
enabling the generation of grounded code that successfully completes the task.


the critical need for embodied agents to explicitly reason about uncertainty through exploratory yet
safe interactions, and to verify the correctness of generated code prior to execution.


To address these challenges, we propose NESYRO, a neuro-symbolic robot task planning framework
that incorporates explicit symbolic verification and interactive validation processes during code
generation. Drawing inspiration from the long-standing software engineering principle of verification
and validation (V&V) [5, 6, 7], our framework distinguishes between two key processes: verification
ensures that the generated code is logically consistent and satisfies symbolic preconditions, while
validation assesses whether the code is suitable for the current environment and task objectives.
Specifically, symbolic verification statically checks code correctness using domain-specific symbolic
tools, whereas interactive validation enables the agent to actively explore its environment to resolve
ambiguities and acquire missing observations before task-specific execution.


Our NESYRO framework operates through a recursive composition of two phases: (i) Neuro-symbolic
Code Verification, and (ii) Neuro-symbolic Code Validation. Following symbolic verification for
code correctness, the interactive validation phase grounds each skill by identifying preconditions
and invoking exploratory actions that establish those preconditions as effects, thereby transforming
the environment state to enable the intended skill. This process resembles a form of backtracking
search, where the agent navigates the environment to construct a valid execution path, progressively
verifying and validating the code based on current observations and feedback from symbolic tools.


Figure 1 shows the concept of our framework through an object relocation task, comparing a naive
code generation method and our approach. The naive method attempts to move an object without
adequately accounting for uncertain factors, which results in the execution of actions that prevent
task success. In contrast, our framework identifies the need for exploratory actions, ensures they are
conducted safely, and successfully completes the task without causing damage.


We evaluate NESYRO on four task categories, including object relocation, object interaction, auxiliary
manipulation, and long-horizon tasks, using both the RLBench [8] simulation and real-world settings.
Experimental results demonstrate that NESYRO improves task success rate by 46.2% over the stateof-the-art baseline, Code as Policies [2], while achieving over 86.8% executability of task-relevant
actions in real-world settings. These underscore the enhanced reliability of our framework for robust
task planning in dynamic, partially observable environments


The contributions of this work are summarized as follows:


- We present the NESYRO framework to enable the automatic generation of executable code for task
planning in dynamic, partially observable environments.

- We propose a novel recursive mechanism that combines symbolic verification and interactive validation to actively infer and satisfy task-relevant preconditions through exploratory code execution.


2


- Extensive evaluations on RLBench and real-world tasks demonstrate that NESYRO significantly
improves both task success rates and the executability of task-relevant skills.


**2** **Related work**


**LLM-based** **embodied** **control.** In the field of embodied control, there is an emerging trend of
utilizing LLMs for reasoning and planning tasks [1, 9, 10, 11, 12, 13, 14, 15, 16, 3]. Building on the
high-level reasoning capabilities of LLMs, recent approaches have explored generating executable
code as a direct control policy, a paradigm often referred to as code-as-policies [2, 4, 17, 18, 19].
Rather than mapping instructions to predefined skills or discrete action primitives, these methods
prompt LLMs to generate Python-like scripts that can be directly executed by embodied agents
such as robots. This demonstrates that LLMs are capable of synthesizing low-level control logic,
enabling greater flexibility and generalization across a diverse range of tasks. Yet, in dynamic or
partially observable settings, the generated code often lacks proper grounding, resulting in incomplete
or non-executable outputs. To mitigate this, NESYRO enhances the environmental grounding and
reliability of generated code by integrating explicit feedback into the code generation process.


**Code verification and validation.** Verification and validation are foundational techniques in software
engineering for ensuring the correctness and robustness of programs. Verification typically involves
static analysis methods such as formal verification, theorem proving, and model checking [20, 21, 22,
23, 24], aiming to prove that a program satisfies its specification before execution. Validation assesses
runtime behavior through unit testing, integration testing, system-level evaluation, and runtime
verification [7, 25, 6, 26, 27], ensuring that the code performs as intended under real-world conditions.
Recent works have explored combining these principles with LLMs to improve code reliability via
various forms of static analysis and runtime feedback [28, 29, 5]. Still, existing approaches are
limited to static or simulated settings and lack grounding in real-world environments, which is an
essential requirement for embodied agents. Our framework addresses this by enabling agents to
identify missing task-relevant observations in dynamic and partially observable environments.


**Neuro-symbolic system.** Recent neuro-symbolic systems combine the generalization capabilities
of LLMs with the robustness and interpretability of symbolic reasoning tools. This hybrid approach
has been actively investigated in areas such as symbolic problem solving, planning, and program
synthesis [30, 31, 32, 33, 34, 35, 36]. Neuro-symbolic approaches in embodied agents commonly
employ LLMs for perception and natural language instruction understanding, while utilizing symbolic
tools to perform high-level task planning [37, 38, 39, 40, 41]. However, existing neuro-symbolic
agents rely on fixed modular structures or pre-defined procedures, limiting their adaptability to missing
observations and environmental uncertainty. NESYRO integrates symbolic reasoning with interactive
validation and exploratory interactions, enabling reliable task planning in dynamic environments.


**3** **NESYRO Framework**


**3.1** **Problem Formulation**


We tackle the automatic generation of executable code for task planning and control in embodied
agents operating in dynamic, partially observable environments. The environment is modeled as
a Partially Observable Markov Decision Process (POMDP) _M_ = ( _S, A, G, T, R,_ Ω _, O_ ) [42, 43,
14], where _s_ _∈S_ is a state, _a_ _∈A_ an action, and _g_ _∈G_ is a high-level goal (e.g., “pick up the
red mug”). _T_ : _S_ _× A_ _→S_ is the transition function describing dynamics. The reward function
_R_ : _S × A × G_ _→{_ 0 _,_ 1 _}_ returns a binary success signal, which is common in robotics where only
task completion is observable. Due to partial observability, observations _o_ _∈_ Ω are received via
_O_ : _S_ _× A_ _→_ Ω, where observations are represented in symbolic form, composed of structured
predicate-based expressions (e.g., `is_locked(drawer)`, `on(object,` `surface)` ). Under the codeas-policies paradigm, the LLM generates policy code _π_ from observation history and goal as input
and internally encodes the actions necessary to complete the task. When executed via tool exe, it
yields policy exe( _π_ ). The set of policy codes is Π = _{π_ _|_ exe( _π_ ) : Ω _[∗]_ _→A}_, where Ω _[∗]_ is the set of
all finite observation histories _o≤t_ = ( _o_ 0 _, . . ., ot_ ) with each _oi_ _∈_ Ω. Our goal is to find the policy
code _π_ that maximizes the expected return:


3


|Verified Policy Code 𝜋𝑚𝑡𝑎𝑖𝑛→(𝑓0, 𝑓1, …, 𝑓𝑁−1, 𝑓𝑁)|𝑓𝑛<br>𝑔|Demonstrations ℰ𝑑𝑒𝑚𝑜<br>𝒟 Obs. Buffer 𝑜≤𝑡|
|---|---|---|
|𝚽𝒗𝒂𝒍𝒊: 𝒟, ℰ𝑑𝑒𝑚𝑜, 𝑜≤𝑡, 𝑔, 𝑓𝑛<br>↦𝐶𝑆𝐶𝑓𝑛<br> <br>𝚿𝒗𝒂𝒍𝒊: 𝒟, 𝑜≤𝑡, 𝑔, 𝑓𝑛<br>↦𝐿𝐶𝑓𝑛<br> <br>𝑛= 𝑛+ 1<br>**Policy Code Refinement**<br><br><br>Safe Probe Pipeline<br>Obs. Buffer𝑜≤𝑡+1<br>**Verification**<br>𝑛<br>𝜋𝑚𝑎𝑖𝑛<br>𝑡+1|𝚽𝒗𝒂𝒍𝒊: 𝒟, ℰ𝑑𝑒𝑚𝑜, 𝑜≤𝑡, 𝑔, 𝑓𝑛<br>↦𝐶𝑆𝐶𝑓𝑛<br> <br>𝚿𝒗𝒂𝒍𝒊: 𝒟, 𝑜≤𝑡, 𝑔, 𝑓𝑛<br>↦𝐿𝐶𝑓𝑛<br> <br>𝑛= 𝑛+ 1<br>**Policy Code Refinement**<br><br><br>Safe Probe Pipeline<br>Obs. Buffer𝑜≤𝑡+1<br>**Verification**<br>𝑛<br>𝜋𝑚𝑎𝑖𝑛<br>𝑡+1|𝚽𝒗𝒂𝒍𝒊: 𝒟, ℰ𝑑𝑒𝑚𝑜, 𝑜≤𝑡, 𝑔, 𝑓𝑛<br>↦𝐶𝑆𝐶𝑓𝑛<br> <br>𝚿𝒗𝒂𝒍𝒊: 𝒟, 𝑜≤𝑡, 𝑔, 𝑓𝑛<br>↦𝐿𝐶𝑓𝑛<br> <br>𝑛= 𝑛+ 1<br>**Policy Code Refinement**<br><br><br>Safe Probe Pipeline<br>Obs. Buffer𝑜≤𝑡+1<br>**Verification**<br>𝑛<br>𝜋𝑚𝑎𝑖𝑛<br>𝑡+1|













Figure 2: The NESYRO framework with _Neuro-Symbolic_ _Code_ _Verification_ and _Neuro-Symbolic_
_Code Validation_ phases. It recursively verifies and validates the policy code, while incrementally
acquiring observations.







_π_ _[∗]_ = argmax E
_π∈_ Π _g∼G,τ_ _∼P_ (exe( _π_ ) _,g_ )




- _∞_




_R_ ( _st,_ exe( _π_ )( _o≤t_ ) _, g_ )

_t_ =0



_._ (1)



Here, _τ_ = ( _s_ 0 _, o_ 0 _, a_ 0 _, s_ 1 _, o_ 1 _, a_ 1 _, . . ._ ) denotes the trajectory generated by executing exe( _π_ ) in the
environment, and _P_ (exe( _π_ ) _, g_ ) is the resulting trajectory distribution induced by exe( _π_ ) under _g_,
_T_, and _O_ . In our implementation, each action _at_ in _τ_ corresponds to a skill function composed of
multiple low-level control APIs encoded within _π_ . Since _M_ is partially observable, _π_ _[∗]_ must balance
exploration (to reduce uncertainty) and exploitation (to achieve goals), ensuring reliable task planning
in dynamic environments.


**3.2** **Overall Framework**


To achieve the objective described in Eq. (1), we introduce NESYRO, designed to achieve the generation of executable and grounded code through dynamic reconfiguration of reasoning components.
As illustrated in Figure 2, NESYRO operates in two key phases: Phase i), _Neuro-Symbolic_ _Code_
_Verification_, which ensures the logical correctness of the policy code with respect to the generated
task specification; and Phase ii), _Neuro-Symbolic_ _Code_ _Validation_, which ensures environmental
feasibility by evaluating and refining skills based on their grounding.


In the verification phase i), given a language instruction _g_ and current observation _o≤t_, the LLM
generates a task specification _T_ spec along with the initial policy code _π_ main. The symbolic tool then
verifies whether _π_ main satisfies _T_ spec. If verification fails, the symbolic tool provides feedback to the
LLM, which iteratively refines _π_ main until a verified version is obtained. In the validation phase ii),
the sequence of skills defined in _π_ main is validated sequentially using a neuro-symbolic confidence
score, NeSyConf, which integrates symbolic feasibility and commonsense plausibility. If a skill’s
confidence score falls below a threshold _ϵ_, NESYRO synthesizes a safe probe policy code _π_ probe
to recover missing observations. _π_ probe is recursively processed through the composition of the
verification and validation phases until all skills are grounded.


This recursive structure induces a policy tree rooted at _π_ main, where each _π_ probe serves as a subroutine
that enables successful validation of its parent. The recursive process continues until all required
observations have been acquired and every skill in _π_ main is validated. The final output is a grounded
version of _π_ main, aligned with both _T_ spec and the current environment.


**3.3** **Neuro-symbolic Code Verification**


**LLM-based code generation.** Given a language instruction _g_ and observation _o≤t_, a verification
LLM, denoted as Φveri, is prompted to reason in a chain-of-thought (CoT) manner [44, 45], synthesizing key objectives and constraints into a task specification _T_ spec. It then uses this specification to
generate the policy code _π_ main _[i]_ [, for instance in Python, defining a sequence of skills along with their]


4


parameters and required libraries.

Φveri : ( _o≤t, g, l_ cot _, D, π_ main _[i][−]_ [1] _[,][ F]_ veri _[i][−]_ [1] _[, n]_ [)] _[ �→]_ [(] _[T]_ [spec] _[, π]_ main _[i]_ [)] (2)


Here, _o≤t_ is the current observation, initially from _o_ 0 and incrementally updated via probe. _l_ cot is the
CoT prompt guiding the Φveri to generate the specification as an intermediate step. _D_ denotes domain
knowledge, consisting of available skills represented as parameterized function calls, each defined
by its applicability conditions and resulting effects, as well as object types and attributes that map
these skills to the environment. _F_ veri _[i][−]_ [1] [is verification feedback from the previous iteration, used by the]
LLM to generate the revised _π_ main _[i]_ [. Importantly,] _[ π]_ main _[i][−]_ [1] [and] _[ F]_ veri _[i][−]_ [1] [are provided only when the previous]
verification attempt has failed. The index _n_ indicates the skill function call order in _π_ main from which
the code refinement begins, while calls prior to _n_ remain unchanged. When _n_ =0, it corresponds to
the initial code generation. The resulting _T_ spec captures the high-level intent, constraints, and relevant
subgoals derived from the _g_ and _o≤t_ . _π_ main _[i]_ [is then passed to the symbolic verification tool.]

**Symbolic-based code verification.** Next, a symbolic verification tool Ψveri (i.e., SMT solver) checks
whether _π_ main _[i]_ [satisfies] _[ T]_ [spec][, identifying any violations of constraints defined in the specification.]

Ψveri : ( _T_ spec _, π_ main _[i]_ [)] _[ �→]_ �verified _π_ main _,_ if verification succeeds (3)
_F_ veri _[i]_ _[,]_ if verification fails


If verification fails, Ψveri provides detailed _F_ veri _[i]_ [that identifies the specific parts of] _[ π]_ main _[i]_ [violating]
_T_ spec, such as incorrect parameter bindings or structural mismatches. This feedback is then passed
to the next Φveri iteration to generate a revised _π_ main _[i]_ [. Once] _[ π]_ main _[i]_ [passes verification, resulting in a]
verified version of _π_ main, we proceed to the _Neuro-Symbolic Code Validation_ phase.


**3.4** **Neuro-symbolic Code Validation**


The verified policy code _π_ main is parsed into a sequence of skill function calls, _π_ main =
( _f_ 0 _, f_ 1 _, . . ., fN_ ), where _N_ denotes the maximum skill step. Unlike the _Neuro-symbolic code verifi-_
_cation_ phase, which reasons over the entire _π_ main holistically, the validation process evaluates and
refines each skill sequentially to assess its feasibility in the current environment. The index _n_, as in
Eq. (2), denotes the skill step under validation and represents the first unvalidated step in _π_ main.


**Neuro-symbolic confidence score.** To assess skill feasibility, we introduce Neuro-Symbolic Confidence score (NeSyConf), which combines Common Sense Confidence (CSC) from a validation
LLM denoted Φvali and Logic Confidence (LC) from a symbolic validation tool Ψvali in parallel.


Φvali : ( _D, E_ demo _, o≤t, g, fn_ ) _�→_ CSC _fn_ (4)


The CSC _fn_ estimates the likelihood that a given skill _fn_ _∈_ _π_ main will succeed under the current
observation _o≤t_ and instruction _g_, based on both domain knowledge _D_ and retrieved demonstrations
_E_ demo. To compute this, we insert the code snippet corresponding to _fn_ into the LLM prompt
along with _D_, _o≤t_, _g_, and _E_ demo. Φvali then assigns token-wise probabilities to the _fn_, and we
compute a perplexity-based score to estimate the skill’s plausibility. The cumulative log probabilities
are normalized to produce a consistent confidence CSC _fn_ . To reduce hallucinations and improve
estimation accuracy, we retrieve skill-level demonstrations _E_ demo whose contexts closely resemble
the current situation and include them in the prompt as guidance.


Ψvali : ( _D, o≤t, g, fn_ ) _�→_ LC _fn_ (5)


The logic-based confidence LC _fn_ is computed by the symbolic validation tool (i.e., PDDL planner),
which assesses whether the _fn_ is symbolically feasible under the _o≤t_, _g_, and _D_ . We use a Ψvali to
check whether _fn_ ’s preconditions hold in _o≤t_ . If the planner successfully generates a plan including
_fn_, we set LC _fn_ = 1; otherwise, we set LC _fn_ = 0, indicating symbolic infeasibility under the _o≤t_ .

NeSyConf _fn_ = CSC _fn ×_ LC _fn_ with: �proceed to NeSyConf _fn_ +1 _,_ if NeSyConf _fn_ _≥_ _ϵ_ (6)
generate _π_ probe using _F_ csc _, F_ lc otherwise


The NeSyConf _fn_ represents the final confidence score for _fn_, computed by multiplying CSC _fn_ and
LC _fn_ . This score estimates whether _fn_ is correctly grounded in the environment and likely to succeed
upon execution. If NeSyConf _fn_ _< ϵ_, our framework initiates a safe probe policy code _π_ probe using
feedback from each component, namely _F_ csc and _F_ lc.


5


**Safe probe.** If a _fn_ receives a low confidence score, our framework responds by generating a safe
probe policy code _π_ probe to recover missing observations. Constructed using _F_ csc from CSC and _F_ lc
from LC, _π_ probe undergoes the same verification and validation process as _π_ main. Because _π_ probe is
validated before execution, the framework ensures that only safe and grounded code is deployed.
This recursive structure generates a policy tree rooted at _π_ main, where each _π_ probe functions as a
subroutine that enables successful validation of its parent skill. Once _π_ probe is executed, it collects
new observations and updates the current observation to _o≤t_ +1. This updated observation is then used
in the subsequent _Policy code refinement_ process to update _π_ main.


**Policy code refinement.** Following safe probe, the _o≤t_ +1 is used to refine _π_ main at the skill level.
Specifically, instead of regenerating the entire policy, our framework targets the current _fn_ and
prompts the LLM to regenerate only its code segment using the _o≤t_ +1. This regeneration is conducted
through our _Neuro-symbolic Code Verification_ process. The updated code for _fn_ is then evaluated
using Eq. (6), where its confidence score NeSyConf _fn_ is reassessed. This process of refinement and
safe probe is repeated until NeSyConf _fn_ _≥_ _ϵ_ . Once all skills _fn_ _∈_ _π_ main have been successfully
validated, the grounded _π_ main is executed.


Further implementation details, and algorithmic pseudocode are provided in Appendix A.


**4** **Experiment**


**4.1** **Experiment Setting**


**Environments.** We conducted experiments in both RLBench [8] and real-world settings using a 7DoF Franka Emika Research 3 robotic arm, enabling reproducible evaluations via randomized initial
states and instructions to analyze safe probe strategies in dynamic, partially observable scenarios. In
contrast, real-world experiments evaluated robustness and generalizability under real-world noise
and variability. In dynamic, partially observable scenarios, we defined four observability levels based
on initial observation availability: _High Incompleteness_ condition removes more than half of the
essential observations, constraining the task-solving process. _Low Incompleteness_ condition retains
most observations, though the observation remains partially incomplete. _Stochastic Incompleteness_
condition provides a randomly selected subset of observations, with the incompleteness level varying
across episodes. Finally, _Complete_ condition offers full relevant observations, rendering probe
unnecessary. We denote these four levels as _High_, _Low_, _Stochastic_, and _Complete_, respectively, each
evaluated over ten randomized trials with varied initial conditions and instructions.


Table 1: Task types and their corresponding probe types


**Task Type** **Probe Type**


_Object Relocation_ Robot Pose Adjust
(e.g., moving tomatoes on a plate) (e.g., verifying which item is a tomato)


_Object Interaction_ Object State Check
(e.g., opening a drawer) (e.g., checking whether a drawer is locked)


_Auxiliary Manipulation_ Object State Change
(e.g., opening a drawer in a dark room) (e.g., turning on the light to locate the drawer)


_Long-Horizon_ Uses two or more of the above probe types depending
(e.g., placing a tomato inside a drawer) on task structure and uncertainty


**Task and probe types.** In dynamic, partially observable environments, tasks often require acquiring
missing observations before execution. To support structured analysis of the probe, we define task
types based on manipulation goals and missing observation roles. Specifically, we distinguish whether
the uncertainty concerns object identity, object state, or auxiliary conditions. These distinctions define
three task types, each reflecting a distinct observation-seeking pattern. In addition, _long-horizon_ tasks
involve multi-step goals. Correspondingly, we define three probe types to characterize observation
acquisition: (1) Robot Pose Adjust, adjusting viewpoint to resolve ambiguity; (2) Object State Check,
identifying hidden object states relevant to the task; and (3) Object State Change, performing auxiliary
skills to enable observation of otherwise inaccessible states. These categories are functionally defined


6


Table 2: Task performance under varying levels of observability incompleteness in RLBench


**Methods** _High_ _Low_ _Stochastic_ _Complete_


SR GC SR GC SR GC SR GC


**Task Type: Object Relocation**


CaP 25.0 _±_ 7.1 41.5 _±_ 8.8 30.0 _±_ 0.0 43.8 _±_ 1.8 10.0 _±_ 0.0 36.3 _±_ 1.8 90.0 _±_ 0.0 92.5 _±_ 3.5
CaP w/ Lemur 25.0 _±_ 7.1 43.8 _±_ 5.3 30.0 _±_ 0.0 43.8 _±_ 1.8 10.0 _±_ 0.0 36.3 _±_ 1.8 90.0 _±_ 0.0 96.3 _±_ 1.8
CaP w/ CodeSift 55.0 _±_ 7.1 72.5 _±_ 3.5 50.0 _±_ 0.0 57.5 _±_ 3.5 40.0 _±_ 0.0 52.5 _±_ 3.5 95.0 _±_ 7.1 95.0 _±_ 7.1
LLM-Planner 30.0 _±_ 0.0 35.0 _±_ 7.1 50.0 _±_ 0.0 58.8 _±_ 5.3 30.0 _±_ 0.0 43.8 _±_ 5.3 80.0 _±_ 0.0 88.8 _±_ 5.3
AutoGen 30.0 _±_ 0.0 35.0 _±_ 7.1 55.0 _±_ 7.1 60.0 _±_ 7.1 40.0 _±_ 14.1 47.5 _±_ 10.6 85.0 _±_ 7.1 87.5 _±_ 10.6
NESYRO 70.0 _±_ 14.1 72.5 _±_ 10.6 75.0 _±_ 7.1 87.5 _±_ 3.5 65.0 _±_ 7.1 75.0 _±_ 0.0 95.0 _±_ 7.1 97.5 _±_ 3.5


**Task Type: Object Interaction**


CaP 20.0 _±_ 14.1 35.0 _±_ 7.1 25.0 _±_ 7.1 40.0 _±_ 3.5 35.0 _±_ 7.1 51.3 _±_ 5.3 75.0 _±_ 7.1 77.5 _±_ 7.1
CaP w/ Lemur 35.0 _±_ 7.1 47.5 _±_ 7.1 35.0 _±_ 7.1 47.5 _±_ 3.5 30.0 _±_ 14.1 46.3 _±_ 12.1 85.0 _±_ 7.1 86.3 _±_ 8.8
CaP w/ CodeSift 40.0 _±_ 0.0 65.0 _±_ 7.1 50.0 _±_ 14.1 55.0 _±_ 7.1 40.0 _±_ 0.0 60.0 _±_ 14.1 90.0 _±_ 14.1 90.0 _±_ 14.1
LLM-Planner 5.0 _±_ 7.1 15.0 _±_ 0.0 40.0 _±_ 14.1 53.8 _±_ 5.3 35.0 _±_ 7.1 42.5 _±_ 14.1 55.0 _±_ 7.1 63.8 _±_ 8.8
AutoGen 40.0 _±_ 0.0 48.8 _±_ 1.8 50.0 _±_ 0.0 58.8 _±_ 5.3 50.0 _±_ 0.0 57.5 _±_ 0.0 75.0 _±_ 7.1 76.3 _±_ 8.8
NESYRO 70.0 _±_ 0.0 76.3 _±_ 1.8 80.0 _±_ 0.0 83.8 _±_ 1.8 70.0 _±_ 14.1 73.8 _±_ 8.8 90.0 _±_ 0.0 92.5 _±_ 0.0


**Task Type: Auxiliary Manipulation**


CaP 25.0 _±_ 7.1 25.0 _±_ 7.1 50.0 _±_ 0.0 51.3 _±_ 1.8 40.0 _±_ 0.0 45.8 _±_ 8.3 85.0 _±_ 7.1 90.0 _±_ 4.7
CaP w/ Lemur 30.0 _±_ 14.1 30.0 _±_ 14.1 50.0 _±_ 14.1 58.3 _±_ 7.1 30.0 _±_ 14.1 34.2 _±_ 15.3 85.0 _±_ 7.1 90.8 _±_ 3.5
CaP w/ CodeSift 5.0 _±_ 7.1 5.0 _±_ 7.1 55.0 _±_ 7.1 57.5 _±_ 3.5 35.0 _±_ 7.1 35.0 _±_ 7.1 90.0 _±_ 0.0 93.3 _±_ 0.0
LLM-Planner 15.0 _±_ 7.1 15.0 _±_ 7.1 30.0 _±_ 0.0 37.5 _±_ 3.5 10.0 _±_ 14.1 15.0 _±_ 7.1 75.0 _±_ 7.1 80.0 _±_ 0.0
AutoGen 15.0 _±_ 7.1 15.0 _±_ 7.1 35.0 _±_ 7.1 40.0 _±_ 0.0 20.0 _±_ 0.0 22.5 _±_ 3.5 80.0 _±_ 0.0 80.0 _±_ 0.0
NESYRO 60.0 _±_ 0.0 80.8 _±_ 1.2 70.0 _±_ 14.1 74.2 _±_ 13.0 70.0 _±_ 14.1 85.8 _±_ 5.9 95.0 _±_ 7.1 96.7 _±_ 4.7


**Task Type: Long-Horizon**


CaP 0.0 _±_ 0.0 0.0 _±_ 0.0 20.0 _±_ 0.0 40.4 _±_ 6.6 0.0 _±_ 0.0 0.7 _±_ 1.0 40.0 _±_ 14.1 53.8 _±_ 3.4
CaP w/ Lemur 0.0 _±_ 0.0 0.0 _±_ 0.0 30.0 _±_ 0.0 47.1 _±_ 0.0 0.0 _±_ 0.0 1.6 _±_ 0.2 55.0 _±_ 7.1 67.1 _±_ 5.1
CaP w/ CodeSift 0.0 _±_ 0.0 0.0 _±_ 0.0 30.0 _±_ 14.1 45.8 _±_ 7.9 5.0 _±_ 7.1 5.0 _±_ 7.1 65.0 _±_ 7.1 71.4 _±_ 6.7
LLM-Planner 0.0 _±_ 0.0 0.0 _±_ 0.0 10.0 _±_ 0.0 11.4 _±_ 0.0 5.0 _±_ 0.0 12.9 _±_ 8.1 35.0 _±_ 7.1 44.4 _±_ 9.9
AutoGen 0.0 _±_ 0.0 5.5 _±_ 3.0 30.0 _±_ 14.1 39.2 _±_ 10.3 20.0 _±_ 0.0 28.5 _±_ 7.2 50.0 _±_ 0.0 55.1 _±_ 0.8
NESYRO 45.0 _±_ 7.1 65.2 _±_ 6.7 45.0 _±_ 7.1 58.1 _±_ 6.1 35.0 _±_ 7.1 41.9 _±_ 8.1 65.0 _±_ 7.1 73.7 _±_ 8.3


and implemented for distinct behavioral purposes, thereby enabling generalization to varied settings.
We describe the task types and their associated probe types in Table 1.


**Evaluation metrics.** To assess the objectives in Section 3.1, we adopt metrics from prior work [46,
11, 47, 48]. Success Rate (SR) assigns 100% for full task completion and 0% otherwise. Goal
Condition (GC) measures the percentage of sub-goals achieved. In real-world experiments, we report
Irreversible Actions (IA), counting irreversible actions during task execution.


**Baselines.** We compare our approach against several state-of-the-art baselines that use LLMs to
generate robot control code, covering different paradigms of V&V, reasoning, and replanning. **Code**
**as** **Policies** **(CaP)** [2] generates reusable control code from task instructions via LLM. **CaP** **w/**
**Lemur** [49] integrates SMT verification into the code generation pipeline. **CaP w/ CodeSift** [5]
improves the reliability of LLM-generated code through multi-stage syntactic and semantic validation,
without relying on reference code or actual execution. **LLM-Planner** [11] introduces an executionaware replanning framework, replans after failure using new observations from the environment.
**AutoGen** [50] extends LLM-Planner by enabling multi-agent collaborative reasoning.


**NESYRO** **implementation.** We employ `GPT-4o-mini` [51] for code generation and feedback
generation. Additionally, `Llama-3.2-3B` [52] is used to compute the CSC. The decoding temperature
is fixed at 0.0 for all generation steps. For the verification phase (i), the Z3 SMT solver [20] is
employed as the symbolic verification tool, while for the validation phase (ii), the Fast Downward
planner [53] is used as the symbolic validation tool.


Detailed descriptions of the experimental settings are provided in the Appendix B and C.


**4.2** **Main Result**


**Task** **performance** **on** **RLBench.** Table 2 reports the performance of robot control code across
all task types in dynamic, partially observable scenarios. For each task, we consider four levels


7


Table 3: Task performance across task types in the real-world under partial observability ( _High_ and
_Low Incompleteness_ averaged). NESYRO-Complete reports results under _Complete_ .


|Real-World|CaP|CaP w/ CodeSift|NeSyRo|NeSyRo-Complete|
|---|---|---|---|---|
|Task Type|SR (_↑_)<br>GC (_↑_)<br>IA (_↓_)|SR (_↑_)<br>GC (_↑_)<br>IA (_↓_)|SR (_↑_)<br>GC (_↑_)<br>IA (_↓_)|SR (_↑_)<br>GC (_↑_)<br>IA (_↓_)|
|Object Relocation<br>Object Interaction<br>Auxiliary Manipulation<br>Long-Horizon|7.5_±_3.5<br>11.3_±_1.8<br>19<br>30.0_±_7.1<br>37.5_±_7.1<br>12<br>0.0_±_0.0<br>0.0_±_0.0<br>4<br>5.0_±_0.0<br>14.2_±_3.5<br>18|12.5_±_3.5<br>19.4_±_4.4<br>4<br>20.0_±_7.1<br>24.4_±_9.7<br>4<br>2.5_±_3.5<br>8.3_±_4.7<br>5<br>7.5_±_10.6<br>13.1_±_7.4<br>16|82.5_±_3.5<br>83.8_±_3.5<br>2<br>75.0_±_14.1<br>77.5_±_17.7<br>0<br>20.0_±_0.0<br>20.0_±_0.0<br>2<br>52.5_±_3.5<br>54.2_±_3.5<br>3|85.0_±_7.1<br>90.0_±_3.5<br>2<br>90.0_±_14.1<br>90.0_±_14.1<br>0<br>20.0_±_14.1<br>20.0_±_14.1<br>2<br>60.0_±_0.0<br>65.8_±_8.3<br>2|
|Total|10.6_±_0.9<br>15.7_±_0.4<br>53|10.6_±_4.4<br>16.3_±_4.4<br>29|57.5_±_3.5<br>58.9_±_4.4<br>7|68.8_±_5.3<br>71.5_±_6.5<br>6|
















|Col1|Col2|
|---|---|
|**NeSyRo**<br>Move the cup from the floor to the shelf<br>**Code as Policies**|**NeSyRo**<br>Move the cup from the floor to the shelf<br>**Code as Policies**|



Figure 3: Representative failure scenarios under partial observability across real-world tasks


of observability incompleteness, requiring each method to recover missing observations. NESYRO
consistently outperforms baselines (AutoGen and CaP w/ CodeSift) by 26.3% in SR and 24.3% in
GC across all levels of observability incompleteness.


CaP w/ Lemur outperforms the base CaP model, indicating that pre-execution verification improves
robustness even without explicit safe probe. LLM-based replanning methods, such as AutoGen
and LLM-Planner, perform well compared to V&V-based approaches, such as CaP w/ CodeSift,
under the _Low Incompleteness_ condition, but their performance degrades significantly as uncertainty
increases and critical observations are missing. In contrast, NESYRO sustains strong results across
every observability regime and task type. It accurately detects missing observations and performs
safe probes, avoiding irreversible actions. Under the _Complete_ condition, all methods achieve high
performance since no additional probe is required. As observability grows more incomplete, baseline
performance drops sharply. Meanwhile, NESYRO detects the missing observations, explores safely,
and maintains performance close to that of the Complete setting. This tendency becomes even more
pronounced in long-horizon tasks, where extensive probe is required and bridging observation gaps
becomes especially difficult.


**Task performance on Real-World.** Table 3 reports the real-world evaluation results under partial
observability. The NESYRO-Complete configuration serves as an upper bound, representing the ideal
performance achievable when all relevant observations are fully available. Across all task categories,
NESYRO consistently achieves the highest SR and GC, outperforming existing baselines such as
CaP and CaP w/ CodeSift. On average, NESYRO improves SR by an average of 47.0% and GC by
42.6% compared to CaP w/ CodeSift, while simultaneously reducing IA from 29 to 7.


In particular, for _Object Relocation_ and _Object Interaction_, baseline methods achieve less than 30%
SR, primarily due to their failure to account for missing observations. In contrast, NESYRO exceeds
75% SR by recovering these observations. Performance on _Auxiliary Manipulation_ remains low across
all models, including NESYRO-Complete, primarily due to failure in pressing the light switch with
sufficient accuracy. Nevertheless, NESYRO achieves the same SR and GC as its Complete variant,
indicating upper-bound performance despite the physical difficulty. This highlights the challenge as
one of execution, rather than perceptual or reasoning limitations. On _Long-Horizon_ tasks, baseline
methods remain below 10% SR due to observation gaps and planning complexity. Nonetheless,
NESYRO reaches 52.5% SR, approaching the 60.0% score of the _Complete_ setting. This shows that
our framework bridges long-range dependencies through safe probing. These results confirm that
NESYRO enables robust real-world execution through safe recovery of missing observations, even
under severe observability incompleteness.


Figure 3 illustrates failure modes associated with high IA scores. Among many failure cases, we
present three representative scenarios where CaP fails due to irreversible actions, while NESYRO
completes the tasks by recovering missing observations through safe probe. This selection illustrates
that NESYRO not only improves success rates but also ensures safe execution grounded in safe probe.


8


**4.3** **Ablation**


Table 4: Code generation performance across LLMs on longhorizon tasks under partial observability in RLBench



Figure 4: Real-world compile
error rate over all task types



80


60


40


20





Object Relocation
Object Interaction



Auxiliary Manipulation
Long-Horizon


|RLBench|CaP|NeSyRo|NeSyRo-Complete|
|---|---|---|---|
|LLM Type|SR<br>GC|SR<br>GC|SR<br>GC|
|GPT-4o-mini<br>o4-mini<br>GPT-4.1<br>o3|10.0_±_0.0<br>20.2_±_3.3<br>12.5_±_3.5<br>22.0_±_1.4<br>32.5_±_3.5<br>59.6_±_4.8<br>45.0_±_0.0<br>64.0_±_1.9|45.0_±_0.0<br>61.7_±_0.3<br>42.5_±_3.5<br>54.9_±_2.2<br>50.0_±_7.1<br>70.9_±_1.8<br>75.0_±_7.1<br>87.6_±_3.0|65.0_±_7.1<br>73.7_±_8.3<br>50.0_±_14.1<br>51.7_±_11.8<br>75.0_±_7.1<br>78.1_±_2.7<br>85.0_±_7.1<br>93.8_±_0.7|



**Effect** **of** **neuro-symbolic** **code** **verification** Table 4 reports performance across different LLMs
used for code generation, evaluated on long-horizon tasks and averaged over _High_ and _Low Incom-_
_pleteness_ conditions. Stronger LLMs improve performance. On average, NESYRO improves SR
by 28.1% and GC by 27.3% over CaP across all LLMs. The SR difference between NESYRO and
the upper-bound NESYRO-Complete remains at 15.6% on average, indicating that our framework
consistently approaches the optimal performance achievable under complete observations. This shows
that NESYRO performs consistently across LLMs. Figure 4 reports real-world task failures due
to compile errors across task types. NESYRO consistently exhibits the lowest compile error rate,
highlighting the robustness of its verification and validation pipeline. In contrast, CaP w/ CodeSift
incurs more compile errors than the base CaP under partial observability, primarily due to hallucinated
evaluations by the LLM in the absence of grounded feedback. NESYRO addresses this issue through
environment-aware validation, enabling reliable execution even with incomplete observations.



Table 5: Comparison of performance on long-horizon RLBench
tasks when without LC or CSC from NESYRO



Table 6: Effect of LLM parameter
scale on CSC in RLBench


**RLBench** Long-Horizon Tasks


LLM Type SR GC


Llama-3.2-1B 32.5 _±_ 3.5 55.4 _±_ 2.7
Llama-3.2-3B 45.0 _±_ 0.0 61.7 _±_ 0.3
Llama-3.1-8B 45.0 _±_ 7.1 57.7 _±_ 0.3
Qwen3-30B-A3B 45.0 _±_ 0.0 64.9 _±_ 5.1


|RLBench|NeSyRo w/o LC|NeSyRo w/o CSC|NeSyRo|
|---|---|---|---|
|Task Type|SR<br>GC|SR<br>GC|SR<br>GC|
|Object Relocation<br>Object Interaction<br>Auxiliary Manipulation <br>Long-Horizon|50.0_±_8.2<br>60.0_±_4.1 <br>45.0_±_7.1<br>56.3_±_5.3 <br> 57.5_±_3.5<br>65.4_±_4.1 <br>25.0_±_0.0<br>36.0_±_6.3|35.0_±_5.8<br>51.3_±_4.8 <br> 55.0_±_7.1<br>62.5_±_3.5<br> 35.0_±_7.1<br>39.2_±_3.5<br> 32.5_±_3.5<br>52.9_±_8.4|67.5_±_10.6<br>73.8_±_5.3<br>70.0_±_7.1<br>75.0_±_3.5<br>65.0_±_7.1<br>77.5_±_7.1<br>45.0_±_0.0<br>61.7_±_0.3|
|Total|44.3_±_2.0<br>54.2_±_0.1|37.1_±_4.0<br>49.9_±_4.4|61.9_±_6.2<br>72.0_±_3.9|



**Effect** **of** **neuro-symbolic** **code** **validation** Tables 5 and 6 report results on long-horizon tasks,
averaged over _High_ and _Low_ _Incompleteness_ conditions. Table 5 compares performance when
removing either LC ( _w/o LC_ ) or CSC ( _w/o CSC_ ) from our neuro-symbolic code validation phase. The
results indicate that both LC and CSC contribute comparably to overall performance across task types,
with an average SR drop of 21.2% and GC drop of 20.0% when either component is removed. This
validates the importance of the parallel neuro-symbolic structure in reliably guiding execution under
uncertainty. To analyze CSC robustness, Table 6 examines the effect of the LLM parameter scale
used in computing the CSC. While smaller models (e.g., Llama-3.2-1B) show degraded performance,
models with 3B parameters or more achieve the same SR and differ in GC by less than 7.2%. These
results suggest that CSC computation is robust to LLM scaling beyond a moderate threshold, allowing
flexible deployment depending on available compute resources.


**4.4** **Analysis**


**Real-world** **analysis.** Figure 5 showcases how NESYRO addresses real-world uncertainty in a
partially observable setting involving a dark room and unknown drawer states. Initially, the LLM
generates an ungrounded policy code without access to key observations, such as whether the drawers
are locked, what objects are inside, or where to safely place the dice. As each skill is validated,
NESYRO computes NeSyConf. If the confidence falls below a threshold, the system initiates a
targeted safe probe, such as checking individual drawers, to acquire missing observations. These safe
probes trigger policy code refinement by updating parameters (e.g., selecting a different drawer) or
regenerating the policy for the skill. This iterative validation process adapts the skill sequence and
produces a fully grounded policy code that completes the task without causing irreversible failures. A
full execution sequence and extended analysis of Figure 5 are provided in Appendix D.


9


|Col1|Col2|Col3|
|---|---|---|
||||
||||









































Figure 5: Real-world example of safe probe and policy code refinement in partially observable setting


**5** **Conclusion**


In this work, we presented NESYRO, a neuro-symbolic framework that integrates _Neuro-symbolic_
_Code_ _Verification_ and _Neuro-Symbolic_ _Code_ _Validation_ to generate reliable robot control code
under dynamic, partially observable settings. The framework operates through a recursive process
alternating between symbolic verification and interactive validation, ensuring that each skill is both
logically consistent and environmentally grounded. By incorporating neuro-symbolic confidence
estimation that combines commonsense and logic-based reasoning, NESYRO enables exploratory yet
safe interactions and adaptive code refinement under uncertainty. Extensive evaluation in simulation
and real-world environments demonstrates the strong performance of NESYRO across diverse tasks.


**Limitation and future work.** While the NeSyConf formulation is designed to allow LC and CSC to
complement each other, similar to how SayCan [1] integrates LLM scores with affordance functions,
the current implementation of NESYRO employs a binary LC and predefined domain knowledge,
which limits its generality in real-world applications. Future work will address this limitation by
incorporating probabilistic and temporal reasoning, such as probabilistic PDDL [54]. We also plan
to relax these assumptions and explore the framework’s applicability to more diverse and dynamic
domains by extending validation to skills that are not explicitly defined in the domain knowledge.


**Ethical** **concern.** LLM-based robot control may lead to unsafe behavior when interacting with
hazardous tools (e.g., knives, scissors). To mitigate such risks, we incorporate explicit safety checks
and enforce transparent safeguard mechanisms that verify tool affordances and action preconditions
before execution, ensuring safe and interpretable operation.


10


**Acknowledgement**


This work was supported by Institute of Information & communications Technology Planning
& Evaluation (IITP) grant funded by the Korea government (MSIT), (RS-2022-II220043 (20220-00043), Adaptive Personality for Intelligent Agents, RS-2022-II221045 (2022-0-01045), Selfdirected multi-modal Intelligence for solving unknown, open domain problems, RS-2025-02218768,
Accelerated Insight Reasoning via Continual Learning, RS-2025-25442569, AI Star Fellowship
Support Program (Sungkyunkwan Univ.), and RS-2019-II190421, Artificial Intelligence Graduate
School Program (Sungkyunkwan University)), IITP-ITRC (Information Technology Research Center)
grant funded by the Korea government (MIST) (IITP-2025-RS-2024-00437633, 10%), IITP-ICT
Creative Consilience Program grant funded by the Korea government (MSIT) (IITP-2025-RS-2020II201821, 10%), and by Samsung Electronics.


**References**


[1] Anthony Brohan et al. “Do as I can, not as I say: Grounding language in robotic affordances”.
In: _Proceedings of the 6th Conference on Robot Learning (CoRL)_ . PMLR, 2023, pp. 287–318.

[2] Jacky Liang et al. “Code as policies: language model programs for embodied control”. In:
_Proceedings of the 40th International Conference on Robotics and Automation (ICRA)_ . IEEE,
2023, pp. 9493–9500.

[3] Wenlong Huang et al. “VoxPoser: Composable 3D Value Maps for Robotic Manipulation
with Language Models”. In: _Proceedings of the 7th Conference on Robot Learning (CoRL)_ .
Vol. 229. 2023, pp. 540–562.

[4] Yao Mu et al. “Robocodex: multimodal code generation for robotic behavior synthesis”. In:
_Proceedings of the 41st International Conference on Machine Learning (ICML)_ . PMLR, 2024,
pp. 36434–36454.

[5] Pooja Aggarwal et al. “CodeSift: An LLM-Based Reference-Less Framework for Automatic
Code Validation”. In: _arXiv preprint arXiv:2408.15630_ (2024).

[6] Stefan Mitsch and André Platzer. “ModelPlex: verified runtime validation of verified cyberphysical system models”. In: _Formal Methods in System Design_ 49 (2016), pp. 33–74.

[7] Martin Leucker and Christian Schallhart. “A brief account of runtime verification”. In: _The_
_Journal of Logic and Algebraic Programming_ 78.5 (2009), pp. 293–303.

[8] Stephen James et al. “RLBench: The Robot Learning Benchmark & Learning Environment”.
In: _IEEE Robotics and Automation Letters_ 5.2 (2020), pp. 3019–3026.

[9] Wenlong Huang et al. “Inner Monologue: Embodied Reasoning through Planning with Language Models”. In: _Proceedings of the 6th Conference on Robot Learning (CoRL)_ . Vol. 205.
2022, pp. 1769–1782.

[10] Wenlong Huang et al. “Language models as zero-shot planners: Extracting actionable knowledge for embodied agents”. In: _Proceedings of the 39th International Conference on Machine_
_Learning_ . PMLR. 2022, pp. 9118–9147.

[11] Chan Hee Song et al. “LLM-planner: Few-shot grounded planning for embodied agents with
large language models”. In: _Proceedings of the 19th International Conference on Computer_
_Vision (ICCV)_ . 2023, pp. 2998–3009.

[12] Zhenyu Wu et al. “Embodied task planning with large language models”. In: _arXiv preprint_
_arXiv:2307.01848_ (2023).

[13] Zihao Wang et al. “Describe, explain, plan and select: Interactive planning with LLMs enables
open-world multi-task agents”. In: _Proceedings of the 37th Advances in Neural Information_
_Processing Systems (NeurIPS)_ . 2023.

[14] Ishika Singh et al. “ProgPrompt: Generating situated robot task plans using large language
models”. In: _Proceedings of the 40th International Conference on Robotics and Automation_
_(ICRA)_ . IEEE, 2023, pp. 11523–11530.

[15] Anthony Brohan et al. “RT-2: Vision-Language-Action Models Transfer Web Knowledge to
Robotic Control”. In: _Proceedings of the 7th Conference on Robot Learning (CoRL)_ . PMLR,
2023, pp. 2165–2183.

[16] Danny Driess et al. “PaLM-E: an embodied multimodal language model”. In: _Proceedings of_
_the 40th International Conference on Machine Learning (ICML)_ . 2023, pp. 8469–8488.


11


[17] Kaylee Burns et al. “GenCHiP: generating robot policy code for high-precision and contactrich manipulation tasks”. In: _Proceedings of the 37th IEEE/RSJ International Conference on_
_Intelligent Robots and Systems (IROS)_ . IEEE, 2024, pp. 9596–9603.

[18] Yin Li et al. “MCCoder: streamlining motion control with LLM-assisted code generation and
rigorous verification”. In: _arXiv preprint arXiv:2410.15154_ (2024).

[19] Xiao Wang et al. “AutoMisty: a multi-agent LLM framework for automated code generation
in the Misty social robot”. In: _arXiv preprint arXiv:2503.06791_ (2025).

[20] Leonardo De Moura and Nikolaj Bjørner. “Z3: An efficient smt solver”. In: _International_
_Conference on Tools and Algorithms for the Construction and Analysis of Systems_ . Springer,
2008, pp. 337–340.

[21] Xiang Yin and John Knight. “Formal verification of large software systems”. In: _Proceedings_
_of the Second NASA Formal Methods Symposium (NFM)_ . 2010.

[22] Daniel Kroening, Peter Schrammel, and Michael Tautschnig. “CBMC – C Bounded Model
Checker”. In: _Tools and Algorithms for the Construction and Analysis of Systems_ . Vol. 8413.
Springer, 2014, pp. 389–391.

[23] Leonardo de Moura et al. “The Lean theorem prover (system description)”. In: _Automated_
_Deduction – CADE-25_ . Vol. 9195. Springer, 2015, pp. 378–388.

[24] Jasmin Christian Blanchette and Lawrence C. Paulson. “Three Years of Experience with
Sledgehammer, a Practical Link between Automatic and Interactive Theorem Provers”. In:
_Proceedings of the 8th International Workshop on the Implementation of Logics (IWIL)_ . 2010,
pp. 1–11.

[25] Sina Shamshiri et al. “Do automatically generated unit tests find real faults? An empirical
study of effectiveness and challenges”. In: _Proceedings of the 30th IEEE/ACM International_
_Conference on Automated Software Engineering (ASE)_ . IEEE, 2015, pp. 201–211.

[26] Yun Tang et al. “Systematic testing of autonomous driving systems using map topology-based
scenario classification”. In: _Proceedings of the 36th IEEE/ACM International Conference on_
_Automated Software Engineering (ASE)_ . IEEE, 2021, pp. 1342–1346.

[27] James A. Whittaker. “What is software testing? And why is it so hard?” In: _IEEE Software_
17.1 (2000), pp. 70–79.

[28] Jingkang Yang et al. “Octopus: embodied vision-language programmer from environmental
feedback”. In: _Proceedings of the European Conference on Computer Vision (ECCV)_ . Springer,
2024, pp. 20–38.

[29] Greta Dolcetti et al. “Helping LLMs improve code generation using feedback from testing and
static analysis”. In: _arXiv preprint arXiv:2412.14841_ (2024).

[30] Jundong Xu et al. “Faithful logical reasoning via symbolic chain-of-thought”. In: _Proceedings_
_of the 62nd Annual Meeting of the Association for Computational Linguistics (ACL)_ . 2024.

[31] Shraddha Barke et al. “HYSYNTH: context-free LLM approximation for guiding program
synthesis”. In: _Proceedings of the 38th Annual Conference on Neural Information Processing_
_Systems (NeurIPS)_ . 2024.

[32] Sumit Kumar Jha et al. “Counterexample Guided Inductive Synthesis Using Large Language
Models and Satisfiability Solving”. In: _Proceedings of the IEEE Military Communications_
_Conference (MILCOM)_ . 2023, pp. 944–949.

[33] Theo X. Olausson et al. “LINC: A Neurosymbolic Approach for Logical Reasoning by
Combining Language Models with First-Order Logic Provers”. In: _Proceedings of the 2023_
_Conference on Empirical Methods in Natural Language Processing (EMNLP)_ . Association for
Computational Linguistics, 2023, pp. 5153–5176.

[34] Liangming Pan et al. “LOGIC-LM: Empowering Large Language Models with Symbolic
Solvers for Faithful Logical Reasoning”. In: _Findings of the Association for Computational_
_Linguistics (EMNLP)_ . Association for Computational Linguistics, 2023, pp. 3806–3824.

[35] Debargha Ganguly et al. “Proof of thought: neurosymbolic program synthesis allows robust
and interpretable reasoning”. In: _Workshop on System 2 Reasoning at Scale, NeurIPS_ . 2024.

[36] Xin Quan et al. “Verification and refinement of natural language explanations through LLMsymbolic theorem proving”. In: _Proceedings of the 2024 Conference on Empirical Methods in_
_Natural Language Processing (EMNLP)_ . Association for Computational Linguistics, 2024,
pp. 2933–2958.


12


[37] Xinrui Lin et al. “CLMASP: Coupling Large Language Models with Answer Set Programming
for Robotic Task Planning”. In: _arXiv preprint arXiv:2406.03367_ (2024).

[38] Alessio Capitanelli and Fulvio Mastrogiovanni. “A framework for neurosymbolic robot action
planning using large language models”. In: _Frontiers in Neurorobotics_ 18 (2024), p. 1342786.

[39] Vinh Luong et al. “DANA: domain-aware neurosymbolic agents for consistency and accuracy”.
In: _arXiv preprint arXiv:2410.02823_ (2024).

[40] Kaizhi Zheng et al. “JARVIS: a neuro-symbolic commonsense reasoning framework for
conversational embodied agents”. In: _arXiv preprint arXiv:2208.13266_ (2022).

[41] Yujie Lu et al. “Neuro-symbolic procedural planning with commonsense prompting”. In:
_Proceedings of the 11th International Conference on Learning Representations (ICLR)_ . 2023.

[42] Richard S. Sutton and Andrew G. Barto. _Reinforcement learning: an introduction_ . MIT Press,
2018.

[43] Lingfeng Sun et al. “Interactive planning using large language models for partially observable robotic tasks”. In: _Proceedings_ _of_ _the_ _41st_ _International_ _Conference_ _on_ _Robotics_ _and_
_Automation (ICRA)_ . IEEE, 2024, pp. 14054–14061.

[44] Jason Wei et al. “Chain-of-thought prompting elicits reasoning in large language models”. In:
_Advances in neural information processing systems_ 35 (2022), pp. 24824–24837.

[45] Wonje Choi et al. “NeSyC: A Neuro-symbolic Continual Learner For Complex Embodied
Tasks in Open Domains”. In: _Proceedings of the 13th International Conference on Learning_
_Representations (ICLR)_ . 2025.

[46] Mohit Shridhar et al. “ALFRED: A Benchmark for Interpreting Grounded Instructions for
Everyday Tasks”. In: _The_ _IEEE_ _Conference_ _on_ _Computer_ _Vision_ _and_ _Pattern_ _Recognition_
_(CVPR)_ . 2020.

[47] So Yeon Min et al. “FILM: Following Instructions in Language with Modular Methods”. In:
_Proceedings of the 10th International Conference on Learning Representations (ICLR)_ . 2022.

[48] Aishwarya Padmakumar et al. “TEACh: Task-Driven Embodied Agents That Chat”. In: _Pro-_
_ceedings of the 36th AAAI Conference on Artificial Intelligence_ . Vol. 36. 2. 2022, pp. 2017–
2025.

[49] Haoze Wu, Clark Barrett, and Nina Narodytska. “LEMUR: Integrating Large Language Models
in Automated Program Verification”. In: _Proceedings of the 12th International Conference on_
_Learning Representations (ICLR)_ . 2024.

[50] Qingyun Wu et al. “AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation”. In: _arXiv preprint arXiv:2308.08155_ (2023).

[51] OpenAI. “GPT-4o system card”. In: _arXiv preprint arXiv:2410.21276_ (2024).

[52] AI@Meta Llama Team. “The Llama 3 Herd of Models”. In: _arXiv preprint arXiv:2407.21783_
(2024).

[53] Malte Helmert. “The Fast Downward Planning System”. In: _Journal of Artificial Intelligence_
_Research_ 26 (2006), pp. 191–246.

[54] Håkan LS Younes and Michael L Littman. “PPDDL1. 0: An extension to PDDL for expressing
planning domains with probabilistic effects”. In: _Techn. Rep. CMU-CS-04-162_ 2 (2004), p. 99.

[55] David Coleman et al. “Reducing the barrier to entry of complex robotic software: a moveit!
case study”. In: _arXiv preprint arXiv:1404.3785_ (2014).

[56] Lirui Wang et al. “GenSim: Generating Robotic Simulation Tasks via Large Language Models”.
In: _Proceedings of the 12th International Conference on Learning Representations (ICLR)_ .
2024.


13


**A** **Details of the NESYRO Framework**


NESYRO enables exploration through a recursive composition of Neuro-symbolic Code Verification
and Neuro-symbolic Code Validation. A policy code produced by the LLM is first subjected to explicit
symbolic verification, which statically checks logical consistency against the task specification. The
verified policy code then enters interactive validation, where each skill is evaluated in neuro-symbolic
manner; if an unmet precondition is detected, the system synthesizes exploratory safe probe policy
code to gather the missing observations. Every probe is fed back through the same verification and
validation (V&V) cycle, producing a policy tree whose nodes are recursively grounded until all skills
achieve a satisfactory Neuro-symbolic Confidence Score. This recursive V&V framework guarantees
that the policy code is both executable and environmentally grounded, even under dynamic, partially
observable conditions.


**A.1** **NESYRO Algorithm**


We provide the full pseudocode for our neuro-symbolic task execution pipeline in Algorithm 1 and
Algorithm 2. Below, we briefly describe the functional roles of each procedure and its interaction
within the recursive planning framework.


**Algorithm 1** Task Execution Pipeline


**Agent:**

env — environment interface _D_   - domain knowledge
_E_ demo   - demonstration set _ϵ_   - confidence threshold
_a_   - primitive action _o≤t_   - observation history up to _t_
_A_  - action set


**Returns:**

_τ_   - executed trajectory _π_ main — policy code


**procedure** RUNTASK(env _, D, E_ demo _, ϵ_ )

( _o≤_ 0 _, g_ ) _←_ env _._ reset()
_τ_ _←_ () _▷_ Initialize empty trajectory
( _π_ main _, o≤t,_ env _, τ_ ) _←_ NESYRO( _g, o≤_ 0 _, D, E_ demo _, ϵ,_ 0 _,_ env _, τ_ )
( _τ_ exe _, o≤t_ +1 _,_ env) _←_ EXE( _π_ main _, o≤t,_ env)
_τ_ _←_ _τ_ _∪_ _τ_ exe
**return** ( _τ,_ _o≤t_ +1 _,_ _π_ main)
**end procedure**


**procedure** EXE( _π, o≤t,_ env)

_τ_ exe _←_ [ ]
**for each** _f_ **in** _π_ **do**

_A ←_ EXPANDSKILL( _f, o≤t_ )
**for each** _a_ **in** _A_ **do**

_o_ next _←_ env _._ step( _a_ )
_τ_ exe _←_ _τ_ exe _∪_ ( _a, o_ next)
_o≤t_ _←_ _o≤t ∪_ _o_ next
**end for**
**end for**
**return** ( _τ_ exe _, o≤t,_ env)
**end procedure**


**RunTask and execution loop.** The RUNTASK procedure (Algorithm 1) initializes the environment
and launches the neuro-symbolic reasoning process. It first resets the environment to obtain the
initial observation _o≤_ 0 and instruction _g_, and initializes an empty trajectory _τ_ . The main grounding
routine NESYRO is then called to synthesize a grounded policy code _π_ main based on the instruction
and current context. Once obtained, the policy is executed via EXE, which expands symbolic skills
into primitive actions and steps through the environment. The complete trajectory _τ_ and updated
observation history _o≤t_ are returned. The EXE procedure handles the execution of symbolic skills. For


14


each skill _f_ in _π_, it calls EXPANDSKILL to retrieve the sequence of corresponding low-level actions.
These are executed sequentially in the environment, and the resulting observations are appended to
both the trajectory and the observation history.


**Algorithm 2** Recursive Neuro-symbolic Verifcation & Validation


**procedure** NESYRO( _g, o≤t, D, E_ demo _, ϵ, k,_ env _, τ_ )

( _T_ spec _, π_ main) _←_ NEURO_SYMBOLIC_VERIFICATION( _g, o≤t, D, k_ )
( _π_ main _, o≤t,_ env _, τ_ ) _←_

NEURO_SYMBOLIC_VALIDATION( _g, o≤t, D, E_ demo _, π_ main _,ϵ, k,_ env _, τ_ )
**return** ( _π_ main _, o≤t,_ env _, τ_ ) _▷_ grounding policy code _π_ main
**end procedure**


**procedure** NEURO_SYMBOLIC_VERIFICATION( _g, o≤t, D, k_ )

( _T_ spec _, π_ main) _←_ Φveri( _o≤t, g, l_ cot _, D, k_ )
**while** Ψveri( _T_ spec _, π_ main) = fail **do**

_F_ veri _←_ Ψveri( _T_ spec _, π_ main)
( _T_ spec _, π_ main) _←_ Φveri( _o≤t, g, l_ cot _, D, π_ main _, F_ veri _, k_ )
**end while**
**return** ( _T_ spec _, π_ main)
**end procedure**


**procedure** NEURO_SYMBOLIC_VALIDATION( _g, o≤t, D, E_ demo _, π_ main _, ϵ, k,_ env _, τ_ )

_n ←_ _k_
**while** _n < |π_ main _|_ **do**

_fn_ _←_ _π_ main[ _n_ ]
CSC _←_ Φvali( _D, E_ demo _, o≤t, g, fn_ )
LC _←_ Ψvali( _D, o≤t, g, fn_ )
NeSyConf _←_ CSC _×_ LC
**if** NeSyConf _< ϵ_ **then**

_g_ probe _←_ MAKEPROBEGOAL( _fn, F_ csc _, F_ lc)
( _π_ probe _, o≤t,_ env _, τ_ ) _←_ NESYRO( _g_ probe _, o≤t, D, E_ demo _, ϵ,_ 0 _,_ env _, τ_ ) _▷_ recursive
( _τ_ exe _, o≤t_ +1 _,_ env) _←_ EXE( _π_ probe _, o≤t,_ env)
_τ_ _←_ _τ_ _∪_ _τ_ exe
( _T_ spec _, π_ main) _←_ NEURO_SYMBOLIC_VERIFICATION( _g, o≤t_ +1 _, D, n_ )
**else**

_n ←_ _n_ + 1
**end if**
**end while**
**return** ( _π_ main _, o≤t_ + _α,_ env _, τ_ ) _▷α_ : number of recursive _π_ probe executed during validation.
**end procedure**


**Recursive** **neuro-symbolic** **reasoning.** Algorithm 2 outlines the recursive grounding logic of
NESYRO. The NESYRO procedure first invokes NEURO_SYMBOLIC_VERIFICATION to obtain a
symbolic task specification _T_ spec and initial policy code _π_ main. Logical correctness is ensured through
iterative verification using Φveri and Ψveri, which checks whether _π_ main satisfies _T_ spec. After verification,
the policy is passed to NEURO_SYMBOLIC_VALIDATION for skill-wise confidence assessment. For
each skill _fn_, the framework computes neuro-symbolic confidence score (NeSyConf). If NeSyConf
falls below threshold _ϵ_, a probing goal _g_ probe is generated and recursively passed into NESYRO.


To construct this probing goal _g_ probe, the MAKEPROBEGOAL function synthesizes a new instruction
that addresses the failure feedback. Specifically, it leverages NeSyConf feedback ( _F_ csc _, F_ lc) to
identify missing observations. This recursive routine allows a skill that fails to exceed the confidence
threshold _ϵ_ to be refined and validated using updated observations gathered from safe probe executions.
Once all skills pass validation, the final grounded policy and accumulated trajectory are returned.


15


**B** **Environment Settings**


**B.1** **RLBench**


We use RLBench [8] as the simulation environment for our experiments. RLBench offers a wide
range of tabletop manipulation tasks and provides realistic simulations of both robot control and
visual observations. All experiments are performed using a 7-DoF Franka Emika Panda robotic arm,
which is supported natively by RLBench. The environment is particularly suitable for evaluating
planning and interaction under partial observability, as it supports randomized object configurations
and sensor data, including RGB, depth, and segmentation masks. Its compatibility with Python also
allows straightforward integration with our code generation and execution framework.


Figure 6: Example scenes illustrating the "open drawer" task in the RLBench. The top row shows the
overhead view, and the bottom row shows the front view.


**Object configuration.** Each episode initializes a workspace containing seven unique objects placed
on a table. The objects include two tomatoes, a piece of trash, a bin, a three-level drawer, a desk
lamp, and a switch for the desk lamp. The position of each object is randomized in every episode,
introducing perceptual variability and scene diversity across tasks. Figure 6 shows an example scene
from the RLBench environment used in our experiments.


**Task** **composition.** We categorize the tasks into four types to enable structured evaluation, as
summarized in Table 7. Each task type contains multiple language instructions, with associated probe
targets indicating the source of uncertainty that must be resolved during execution.


Table 7: Task types, example of instructions, and associated probe targets in RLBench.


**Task Type** **Example Instructions** **Probe Target**


Move two tomatoes onto plate Tomato identity
Object Relocation
Put the trash into bin Trash identity


Open a drawer Drawer locked/unlocked state
Object Interaction
Open two drawers Drawer locked/unlocked state


Move two tomatoes onto plate in dark room Missing visual observation (requires light activation)
Auxiliary Manipulation
Open drawer in dark room Missing visual observation (requires light activation)


Move a die into the drawer Die identity, Drawer locked/unlocked state
Long-Horizon Tasks
Move dice into the drawer Dice identity, Drawer locked/unlocked state


**B.2** **Real-world**


**Environment** **setup.** We conducted our real-world experiments using a 7-DoF Franka Emika
Research 3 robotic arm mounted on a tabletop workspace. An Intel RealSense D435 RGB-D camera
was positioned above the table to provide top-down RGB and depth information. This input was
processed by an object detection module to identify the categories and bounding boxes of task-relevant
objects. Depth measurements were used to compute 3D coordinates, which were then transformed
into the robot’s coordinate frame. This setup enabled accurate object localization and real-time
observation grounding, providing the necessary perception for reliable execution.


16


Figure 7: Example scenes from the real-world environment used in our experiments.


**Object configuration.** The real-world environment contains ten unique objects arranged on a tabletop
workspace. These include two dice, two pieces of trash, a bin, a three-level drawer, a small cardboard
box, a paper cup filled with liquid, a roll of tape, and a light switch. The initial positions of all objects
are randomized for each trial, introducing diverse spatial configurations and observation conditions
across task instances. This variability supports evaluation under partial observability and enables
direct comparison with the RLBench-based simulation setup. Figure 7 shows a representative setup
of the real-world environment used in our experiments.


**Task composition.** We maintain the RLBench task categorization in the real-world setup to ensure
consistency and enable direct comparison. Each of the four task types corresponds to a distinct source
of uncertainty and is associated with multiple language instructions and probe targets, as summarized
in Table 8.


Table 8: Task types, example of instructions, and associated probe targets in real-world.


**Task Type** **Example Instructions** **Probe Target**


Place a die into drawer Die identity
Object Relocation
Move dice into drawer Dice identity


Open a drawer Drawer locked/unlocked state
Object Interaction
Open two drawers Drawer locked/unlocked state


Place a die into drawer in dark room Missing visual observation (requires light activation)
Auxiliary Manipulation
Open drawer in dark room Missing visual observation (requires light activation)


Place a die into drawer Die identity, Drawer locked/unlocked state
Long-Horizon Tasks
Move a die into drawer Die identity, Drawer locked/unlocked, empty/occupied state


**Low-Level Control.** For motion planning and control in the real-world environment, we employed
MoveIt [55], an open-source motion planning framework widely used for robotic manipulation. Once
the target object positions were obtained from the perception pipeline, we invoked parameterized skill
primitives such as `pick`, `place`, and `open`, which are designed to operate over arbitrary object poses.
Each skill was instantiated using the transformed 3D coordinates of the corresponding object and
passed to the planner as goal constraints. Trajectory optimization was handled by MoveIt’s built-in
planners, which computed collision-free joint-space paths that respect the robot’s kinematic limits and
workspace constraints. The resulting trajectories were executed using the robot’s internal controller
through ROS. Although continuous force control was not used for the gripper, we implemented
discrete grasping strategies based on object geometry and semantic role (e.g., trash, dice). This
ensured consistent and safe execution across a variety of physical configurations.


Unlike the RLBench setting, where code execution is simulated through parameterized low-level
APIs, our real-world system closes the loop by grounding skill calls with real sensor observations and
executing planned trajectories on physical hardware. This setup allows us to evaluate the reliability of
the proposed planning framework under real-world uncertainties.


17


**C** **Experiment Details**


**C.1** **Compute Resources**


Most experiments were conducted on a local machine with an Intel(R) Core(TM) i7-9700KF CPU
and an NVIDIA GeForce RTX 4080 GPU (16GB VRAM). Each task instance used a single GPU,
and RLBench simulation was executed with up to 32GB of system memory. Symbolic verification
and PDDL planning were run on the CPU. For experiments using the larger language models listed in
Table 6 in main paper, such as Llama-3.1-8B and Qwen3-30B-A3B, we used a cloud-based CUDA
cluster with GPUs equipped with approximately 82GB of VRAM. All OpenAI models, including
GPT-4o and GPT-4.1, were accessed via the OpenAI API.


**C.2** **NESYRO Implementation**


**LLM** **usage** **overview.** Our framework utilizes LLM as core reasoning engines in three tightly
integrated components of the code generation and validation pipeline:


    - **Code Generation (** Φ **veri):** Given the instruction _g_ and the current observation history _o≤t_,
the verification LLM Φveri performs chain-of-thought reasoning to produce an intermediate
symbolic task specification _T_ spec and corresponding Python policy code _π_ main. If the code
fails symbolic verification via Ψveri, structured feedback _F_ veri is returned and used by the
LLM to iteratively revise the code. Only the unvalidated portion of _π_ main is regenerated at
each step, preserving previously verified components.

    - **CSC** **Computation** **(** Φ **vali):** For each skill _fn_ in the primary policy _π_ main, the validation
LLM Φvali computes CSC _fn_ that estimates the likelihood of successful execution under
the current observation _o≤t_ and instruction _g_ . The LLM is prompted with the code for _fn_,
domain knowledge _D_, retrieved single-skill demonstrations _E_ demo, and task context. Tokenlevel probabilities are aggregated and transformed into a negative log-likelihood score. This
value is normalized to produce a scalar confidence score CSC _fn_ used for validation. Before
normalization, CSC _fn_ ranges over [0 _, ∞_ ); after normalization, it is scaled to the interval

[0 _,_ 1].

    - **CSC** **Feedback** **Generation** **(** _F_ **csc):** If NeSyConf _fn_ _<_ _ϵ_, the skill _fn_ is considered to
require a safe probe. In such cases, CSC feedback _F_ csc is constructed based on _fn_, the
failure context, current observation _o≤t_, instruction _g_, and single-skill demonstrations _E_ demo.
This feedback is then used to prompt the LLM to generate a safe probe policy code _π_ probe.
The resulting policy code is recursively verified and validated through the NESYRO pipeline
before execution.


**Example of prompt.** Below are the representative prompts used in each stage of our framework:
generating executable robot code, computing CSC for each skill, and generating feedback when the
NeSyConf falls below a threshold.





18


19


**Hyperparameter setting.** The only hyperparameter in our framework is the confidence threshold
_ϵ_ used during neuro-symbolic validation. For each skill, we perform five safe exploration probes


20


under varied initial conditions to estimate its execution confidence. To determine a suitable value of _ϵ_
for a given environment, we exclude outlier trials in which the probe failed due to non-informative
reasons, which could otherwise deflate confidence estimates. This ensures that _ϵ_ reflects a realistic
and actionable lower bound of confidence for successfully grounded skills.


1.0


0.8


0.6


0.4


0.2


0.0









Figure 8: Confidence scores over five safe probes for each of 7 skills in a long-horizon task.
Figure 8 illustrates this process using one of the long-horizon tasks in the RLBench environment.
Each of the 7 skills was probed five times, and confidence scores were recorded before and after each
probe. The figure shows that while confidence increases with repeated probing, it typically saturates
after a few trials, indicating convergence. Based on this observation, we compute the final confidence
distribution by averaging only those probe outcomes that resulted in a successful skill grounding. We
then set _ϵ_ to the lower quartile of this filtered distribution, ensuring a conservative yet robust threshold
that filters out unreliable executions while accepting skills with moderately confident grounding.


**Single-skill demonstrations format.** To support symbolic validation and LLM-based reasoning,
we constructed a general-purpose demonstration library consisting of synthetic examples. These
demonstrations were generated entirely via a large language model (GPT-4o) [56], given domain-level
PDDL definitions and representative symbolic contexts, without requiring environment-specific execution or human annotation. Each example encodes typical task-relevant transitions across common
household activities (e.g., opening a drawer, placing an object, turning on a light), and captures both
successful and failure cases under varied symbolic states. In total, we synthesized approximately **500**
such demonstrations spanning over **15 diverse skill types** . These examples are reused across all tasks
to provide reusable prior knowledge for CSC computation and to guide safe probing decisions when
symbolic grounding confidence is low.





**C.3** **Baselines Implementation**


**Code as Policies (CaP)** [2] serves as the foundation of our framework and is implemented by invoking
the Code Generator Prompt with the frozen code length set to zero. Although a symbolic specification
is also produced, this baseline does not include any verification process.


21


**CaP w/ Lemur** [49] extends CaP by performing verification over the generated specification. This
process is conducted in the exact same manner as the Neuro-symbolic verification phase.


**CaP w/ CodeSift** [5] extends CaP by incorporating LLM-based verification and validation. In the
verification stage, CodeSift performs static syntax checks using language-specific tools ( `pylint`
for Python, `shellcheck` for Bash) and prompts the LLM to summarize the code’s functionality.
This summary is then used in the validation stage to assess semantic alignment with the original
task instruction. The validation consists of multiple sub-steps: semantic similarity scoring, listing
all functional mismatches, and determining whether the implementation is exact. If the code fails
validation, the framework automatically generates refinement feedback and prompts the LLM to
revise the code accordingly. The entire process is orchestrated via a modular pipeline that yields
detailed diagnostic outputs and a refined version of the code when necessary.


**LLM-Planner** [11] follows the same initial procedure as CaP by generating code from the instruction
using a Code Generator Prompt. During execution in the environment, if an action fails, the planner
captures the current observation and provides it as additional context to the LLM. The previously
executed portion of the code is marked as frozen, and a new code segment is generated to continue
the task from the failure point. As in CaP, a symbolic specification is produced, but no verification or
validation is performed throughout the process.


**AutoGen** [50] adopts the same iterative replanning strategy as LLM-Planner, where code is regenerated during execution upon failure by freezing the executed portion and providing the current
observation as context. The key difference is that it uses a dedicated reasoning model, specifically
`o4-mini`, to enhance task understanding and decision making. This improved reasoning enables
more accurate replanning. As with LLM-Planner, no explicit verification or validation is performed.


22


**D** **Real-world Experiment Details**


**D.1** **Figure 1 in Main Paper Details**


In this section, we provide a detailed explanation of Figure 1 in main paper. The complete execution
sequence depicted in Figure 1 including all safe probes is illustrated in Figure 9. To demonstrate
the reliability of NESYRO in a real-world setting, we tasked an embodied agent with the instruction
“Clean up the desk” and compared NESYRO against a naive code generation approach. As depicted
in Figure 1, the naive approach failed in partially observable environments, leading it to execute an
irreversible action by not recognizing that the middle drawer might be locked. In contrast, NESYRO
addresses this uncertainty using a safe probe pipeline to acquire the missing observations. It initially
plans a safe probe to determine whether the drawers are empty. However, through its recursive
validation phase, it subsequently identifies the need to observe the locked status of the drawers.
Consequently, Safe Probe 1, which checks the locked status of the drawers, is executed first, as shown
in Figure 9. Upon its completion, the agent adds observations confirming that the middle drawer
is locked and that the top and bottom drawers are unlocked. Subsequently, Safe Probe 2, which
checks whether the drawers are empty, is executed and adds observations confirming that both the top
and bottom drawers are empty. With these observations acquired, the policy code is now grounded.
NESYRO proceeds to successfully execute the “Clean up the desk” instruction.


**D.2** **Figure 5 in Main Paper Details**


This section provides a detailed explanation of Figure 5 in main paper. The complete execution
sequence depicted in Figure 5 of main paper including all safe probes is illustrated in Figure 10. To
further evaluate the robustness of NESYRO in a real-world setting, we implemented the instruction
“Place one dice into a drawer in a dark room” which represents partially observable environments.
This requires auxiliary manipulation such as turning on the light to restore visibility before executing
the main task. The initial policy code _π_ main was ungrounded, missing observations regarding drawer
visibility and lock status. To resolve this, NESYRO activates its safe probe pipeline and first generates
Safe Probe 1 to turn on the light, enabling the agent to perceive object locations. However, even
after Safe Probe 1, the NeSyConf for the skill `pick(middle_H,` `...)` remains below a threshold.
In response, NESYRO generates Safe Probe 2 to check the lock status of the drawers. This probe
confirms that the top and bottom drawers are unlocked, while the middle drawer is locked. Based
on these observations, the code is refined by replacing the initial skills that placed one dice into the
middle drawer with new skills that place it into the top drawer. As a result, the skill `pick(top_H,`
`...)` becomes ready to execute. Subsequently, during the validation of `pick(dice,` `...)`, the agent
identifies the need to check whether the drawers are empty. Consequently, NESYRO generates Safe
Probe 3 to check whether the drawers are empty. This probe detects trash inside the top drawer,
leading to the insertion of additional code that removes it. These added skills also undergo the same
validation phase in sequence. Once all skills are marked as ready to execute, the policy code is
considered grounded. NESYRO proceeds to successfully execute the given instruction.


23


### Instruction: Clean up the desk





Figure 9: Real-world execution sequence of the instruction “Clean up the desk”


24


### Instruction: Place one dice into a drawer in dark room





Figure 10: Real-world execution sequence of the instruction “Place one dice into a drawer in dark
room”


25


