## **Heterogeneous Agent Collaborative Reinforcement Learning**

**Zhixia Zhang** [1 *] **Zixuan Huang** [1 2 *] **Xin Xia** [2] **Deqing Wang** [1] **Fuzhen Zhuang** [1] **Shuai Ma** [1] **Ning Ding** [3]

**Yaodong Yang** [4] **Jianxin Li** [1] **Yikun Ban** [1] _[ †]_


1 _**Beihang University**_ 2 _**Bytedance China**_ 3 _**Tsinghua University**_ 4 _**Peking University**_


    - Github Page: [https://zzx-peter.github.io/hacrl/](https://zzx-peter.github.io/hacrl/)


**Abstract**



We introduce **H** eterogeneous **A** gent **C** ollaborative
**R** einforcement **L** earning ( **HACRL** ), a new learning paradigm that addresses the inefficiencies of
isolated on-policy optimization. HACRL enables
collaborative optimization with independent execution: heterogeneous agents share verified rollouts during training to mutually improve, while
operating independently at inference time. Unlike LLM-based multi-agent reinforcement learning (MARL), HACRL does not require coordinated deployment, and unlike on-/off-policy distillation, it enables bidirectional _mutual_ _learn-_
_ing_ among _heterogeneous agents_ rather than onedirectional teacher-to-student transfer. Building
on this paradigm, we propose **HACPO**, a collaborative RL algorithm that enables principled
rollout sharing to maximize sample utilization
and cross-agent knowledge transfer. To mitigate
capability discrepancies and policy distribution
shifts, HACPO introduces four tailored mechanisms with theoretical guarantees on unbiased advantage estimation and optimization correctness.
Extensive experiments across diverse heterogeneous model combinations and reasoning benchmarks show that HACPO consistently improves
all participating agents, outperforming GSPO by
an average of 3.3% while using only half the rollout cost.


**1. Introduction**


Reinforcement Learning with Verifiable Rewards (RLVR)
has emerged as a highly effective paradigm for training


**For** **implement** **details,** **feel** **free** **to** **contact** **Zhixia** **Zhang**
22376220@buaa.edu.cn. - Equal Contribution. 1Beihang
University [2] Bytedance China [3] Tsinghua University [4] Peking University. Correspondence to: Yikun Ban _<_ yikunb@buaa.edu.cn _>_ .


_Preprint._ _March 4, 2026._



_Figure_ _1._ The significant differences among Multi-Agent RL,
Knowledge Distillation, and the proposed HACRL. HACRL targets independent execution with collaborative optimization.


strong reasoning models via automatically checkable reward signals (e.g., unit tests and formal verifiers)(Yang et al.,
2026b). Compared with SFT (Chen et al., 2026; Zou et al.,
2025; Chen et al., 2025; Ouyang et al., 2022a) and DPO
(Rafailov et al., 2023; Huang et al., 2025; Xie et al., 2026),
RL Optimization (Stiennon et al., 2020; Huang et al., 2026a)
more directly aligns the model with downstream objectives,
and RLVR further strengthens this alignment through verifiability. Within RLVR, group-based policy optimization
algorithms such as GRPO (Shao et al., 2024; Yang et al.,
2026b) replace the critic in PPO (Schulman et al., 2017) by
computing group-relative advantages (Yang et al., 2026b),
motivating variants including DAPO (Yu et al., 2025) and
GSPO (Zheng et al., 2025). Despite these advances, RLVR
remains bottlenecked by expensive on-policy sampling and



1


**Heterogeneous Agent Collaborative Reinforcement Learning**























































Optimization, HACPO introduces four algorithmic innovations to mitigate capability and policy distribution discrepancy.



verification, which frequently dominate the overall training
overhead and limit scalability. Meanwhile, modern LLM
ecosystems are inherently _heterogeneous_ : agents differ in
parameter states, model size, architecture, and are often designed or adapted for different downstream tasks, such as
instruction following (Ouyang et al., 2022b), mathematical
problem solving (Cobbe et al., 2021), and code generation
(Weyssow et al., 2025). This heterogeneity becomes even
more pronounced when models come from different vendors or families(Yang et al., 2025a; Grattafiori et al., 2024),
with mismatched pretraining corpora, tokenizers, and architectural choices.


Typically, given _one_ identical task, _multiple_ agents execute
RLVR optimization _independently_ of one another. For essentially the same objective, they repeatedly generate trajectories and yield verifiable rewards, while these costly
intermediate results are only utilized for self-training.


To break through this wasteful practice, we propose a collaborative policy optimization problem for RLVR: _given_
_a set of heterogeneous agents, can an agent improve both_
_effectiveness and efficiency by leveraging rollouts generated_
_by other agents,_ _rather than relying solely on its own on-_
_policy rollouts?_ Our goal is to enable _mutual benefit_ across
agents—each agent can reuse rollouts from others—while
controlling distribution shift induced by heterogeneity.


We first formalize this setting as **H** eterogeneous **A** gent
**C** ollaborative **R** einforcement **L** earning ( **HACRL** ), which
captures collaborative policy optimization among heterogeneous agents that execute independently at inference time.
HACRL differs fundamentally from existing paradigms as
illustrated in Figure 1: (1) **LLM-based Multi-Agent Rein-**
**forcement Learning (MARL).** (Liao et al., 2025b) MARL



trains agents to coordinate and jointly solve tasks through
interaction within a coupled multi-agent system. In contrast,
HACRL does not require coordinated execution. In many
practical scenarios, only a single agent is deployed at inference time; however, we still desire that this agent benefits
from knowledge acquired from other agents during training.
(2) **On-/Off-Policy Distillation.** Distillation typically follows a one-directional “teacher-to-student” paradigm, often
among homogeneous agents. HACRL instead enables bidirectional **mutual learning** among **heterogeneous agents**,
where each agent simultaneously acts as both a knowledge
provider and a learner.


We then propose **H** eterogeneous **A** gent **C** ollaborative **P** olicy
**O** ptimization ( **HACPO** ) to solve HACRL (Figure 2). Compared to vanilla RL optimization, HACPO improves training
in two critical aspects: **(1)** **Maximized** **Sample** **Utiliza-**
**tion.** In an _n_ -agent system, each rollout can be reused up
to _n_ times, substantially improving sample efficiency. **(2)**
**Bidirectional Knowledge Transfer.** By learning from one
another, agents acquire complementary knowledge unavailable through self-learning alone, enabling all agents to break
performance bottlenecks.


In this work, our contributions can be summarized as:


**[Problem Definition].** We formulate HACRL as a collaborative policy optimization paradigm for heterogeneous agents
under RLVR, aiming to achieve mutual benefit through
cross-agent rollout reuse while controlling distribution shifts
caused by heterogeneity.


**[Algorithm].** We propose HACPO to address this problem,
with four following modifications: **(1)** Agent-CapabilityAware Advantage Estimation, **(2)** Model Capabilities Dis


2


**Heterogeneous Agent Collaborative Reinforcement Learning**



crepancy Coefficient, **(3)** Exponential Importance Sampling,
and **(4)** Stepwise Clipping, as shown in Figure 2. These
tailored techniques enable the agents to engage in effective
and stable mutual learning.


**[Performance].** We evaluate HACPO across three types
of heterogeneity and seven challenging mathematical reasoning benchmarks, demonstrating consistent performance
improvements, averaging 3.3%, compared to GSPO while
utilizing only half the rollout cost.


**2. Heterogeneous Agent Collaborative**
**Reinforcement Learning**


**2.1. Heterogeneous LLM Agent Taxonomy**


Let _πθ_ denote a large language model (LLM) agent parameterized by _θ_ _∈_ Θ, where Θ specifies the complete parameter
space, including architecture, dimensionality, and trainable
weights. Let _Vπ_ denote the output vocabulary of agent _πθ_ .
We consider a collaborative policy optimization setting in
which multiple LLM agents are jointly optimized toward a
shared or coupled objective.


We categorize heterogeneity among distinct LLM agents
into three types: (1) heterogeneous state; (2) heterogeneous
size; (3) heterogeneous model.


**Definition 2.1** ( **Heterogeneous State** ) **.** Two LLM agents
_πθ_ [(1)] 1 [and] _[ π]_ _θ_ [(2)] 2 [are said to exhibit] _[ heterogeneous state]_ [ if][ Θ][1] [=]
Θ2 and dim( _θ_ 1) = dim( _θ_ 2), but _θ_ 1 = _θ_ 2 at the start of
collaborative policy optimization.


**Definition** **2.2** ( **Heterogeneous** **Size** ) **.** Two LLM agents
_πθ_ [(1)] 1 [and] _[ π]_ _θ_ [(2)] 2 [are said to exhibit] _[ heterogeneous size]_ [ if they]
belong to the same model family and share the same architectural design principles, but have different parameter
dimensionalities, i.e., dim( _θ_ 1) _̸_ = dim( _θ_ 2), with _θ_ 1 = _θ_ 2 at
the start of collaborative policy optimization.


**Definition 2.3** ( **Heterogeneous Model** ) **.** Given two LLM
agents _πθ_ [(1)] 1 [and] _[π]_ _θ_ [(2)] 2 [,] [we] [define] [them] [to] [exhibit] _[heteroge-]_
_neous model_ heterogeneity if their model architectures differ
(e.g., tokenizer, attention mechanism, or training objective),
their parameter spaces and sizes are distinct (i.e., Θ1 = Θ2),
and their initial parameter instantiations are unique (i.e.,
_θ_ 1 = _θ_ 2).


_Remark_ 2.4 _._ This taxonomy represents increasing degrees
of heterogeneity: heterogeneous state differs only in optimization state, heterogeneous size introduces capacity mismatch, and heterogeneous model captures architectural and
representational divergence. This hierarchy enables a systematic study of collaborative policy optimization among
heterogeneous LLM agents.



**2.2. Problem Formalization**


We consider the Heterogeneous Agent Collaborative Reinforcement Learning (HACRL) framework with _n_ LLM
agents. Each agent _k_ _∈{_ 1 _, . . ., n}_ is associated with a
policy _πθk_ . All agents operate on a shared task distribution
_D_ and exhibit heterogeneity as defined in Section 2.1.


During training, for a query _q_ _∼D_, each agent _k_ independently samples _G_ candidate responses from its policy:


_Yk_ ( _q_ ) = _{yk,_ 1 _, . . ., yk,G} ∼_ _πθk_ ( _· | q_ ) _._ (1)


The joint response set across all agents is _Y_ ( _q_ ) =

- _n_
_k_ =1 _[Y][k]_ [(] _[q]_ [)] _[.]_ [ Since all agents solve the same task, a shared]
reward function _R_ ( _·_ ) is applied to every response. The joint
reward set is


_R_ ( _q_ ) = _{R_ ( _yk,i_ ) _| k_ = 1 _, . . ., n,_ _i_ = 1 _, . . ., G}._ (2)


For notational convenience, we denote by


_Rk_ ( _q_ ) = _{R_ ( _yk,i_ ) _| i_ = 1 _, . . ., G}_ (3)


the rewards corresponding to responses generated by agent
_k_ .

**Definition 2.5** ( **HACRL Problem** ) **.** Consider a system of
_n_ heterogeneous agents. For a query _q_ _∼D_, let _Y_ ( _q_ )
and _R_ ( _q_ ) denote the joint response and reward sets, respectively. The objective of _Heterogeneous Agent Collab-_
_orative Reinforcement Learning_ is to optimize each agent
_k_ _∈{_ 1 _, . . ., n}_ by maximizing


_J_ [(] _[k]_ [)] = _J_ homo [(] _[k]_ [)] [(] _[Y][k]_ [(] _[q]_ [)] _[,][ R][k]_ [(] _[q]_ [))+] _[J]_ hete [(] _[k]_ [)] [(] _[{][Y][j]_ [(] _[q]_ [)] _[,][ R][j]_ [(] _[q]_ [)] _[}][j]_ [=] _[k]_ [)] _[,]_
(4)
where _J_ homo [(] _[k]_ [)] [is computed using rollouts generated by agent]
_k_ itself, and _J_ hete [(] _[k]_ [)] [leverages rollouts generated by the other]
agents.


This formulation enables each agent to benefit from both
self-generated experiences and cross-agent information under collaborative reinforcement learning.


**3. Heterogeneous Agent Collaborative Policy**
**Optimization**


In this section, we propose HACPO, a novel multi-agent collaborative optimization framework (Algorithm Procedure
is shown in Appendix E): for _one_ given task, _multiple_ heterogeneous LLM agents execute independently and learn
from each other. We summarize the key challenges and
corresponding design principles below.





3


**Heterogeneous Agent Collaborative Reinforcement Learning**





The quantity _P_ [ˆ] _t_ [(] _[k]_ [)] denotes a smoothed estimate of the recent
performance of agent _k_, obtained by averaging the per-batch
mean rewards over a sliding window of the most recent _K_
steps:



_P_ ˆ _t_ [(] _[k]_ [)] = _K_ [1]



(9)



_Pτ_ [(] _[k]_ [)] = _G_ [1]



_t_

 - _Pτ_ [(] _[k]_ [)]

_τ_ = _t−K_ +1


_G_

- _R_ - _yτ,i_ [(] _[k]_ [)] - _._

_i_ =1



**3.1. Agent-Capability-Aware Advantage Estimation**


At training step _t_, for each prompt x, each agent _k_ _∈_
_{_ 1 _, ..., n}_ generates _G_ responses _{yt,i_ [(] _[k]_ [)] _[}]_ _i_ _[G]_ =1 _[∼]_ _[π]_ _θ_ [(] _[k]_ _t_ [)][(] _[·]_ _[|]_ _[x]_ [)][.]
For a single agent, the standard group-relative advantage
estimator is



_G_ [1] - _Gi_ =1 _[R]_ - _yt,i_ [(] _[k]_ [)] 



      -       _R_ _yt,i_ [(] _[k]_ [)] _−_ _G_ [1]
_A_ [(] _t,i_ _[k]_ [)][(single) =]



_,_ (5)
_σt_ [(] _[k]_ [)]



Intuitively, when estimating the advantage baseline in a
group for agent _k_, rewards from other agents are reweighted
according to their relative capabilities, allowing all responses to contribute while preserving agent-specific calibration. The temporal smoothing over the most recent _K_
batches stabilizes the capability estimates and reduces variance. We further show that this advantage estimation is
unbiased in Theorem 4.1.


**3.2. Model Capabilities Discrepancy Coefficient**


To address capability discrepancies across heterogeneous
agents, we employ the capability ratio _ωt_ [(] _[k,j]_ [)], introduced
earlier, as a quantitative measure of relative model competence. When training agent _k_, advantages computed from
samples generated by other agents are rescaled according to
their relative capability. This design encourages an agent to
learn more aggressively from stronger agents, while adopting a more conservative update when incorporating samples
from weaker ones.


Formally, suppose that agent _k_ is updated at training step _t_
using a response _yt,i_ [(] _[j]_ [)] [generated by agent] _[ j]_ [.] [The effective]
advantage used for updating agent _k_ is defined as



where _σt_ [(] _[k]_ [)] denote the mean and standard deviation of rewards within the group of agent _k_, respectively.


While Eq. (5) is appropriate for training a single model in
isolation, it becomes suboptimal in a multi-agent settings
where agents exhibit heterogeneous capabilities. Relying
solely on self-generated responses fails to leverage valuable
information from other agents, while _naively_ _averaging_
_rewards across all agents disregards inter-model capability_
_differences_ _and_ _often_ _results_ _in_ _miscalibrated_ _advantage_
_estimates_ .


To address this issue, we propose an _agent-capability-aware_
advantage estimator. The advantage of response _yt,i_ [(] _[k]_ [)] [for]
agent _k_ is defined as


    -     _R_ _yt,i_ [(] _[k]_ [)] _−_ _µ_ ˆ [(] _t_ _[k]_ [)]
_A_ [(] _t,i_ _[k]_ [)] [=] _,_ _σt,joint_ = _std{Rt_ ( _q_ ) _}_ (6)
_σt,joint_


where _Rt_ ( _q_ ) refers to rewards from all agents at step _t_ (Eq.
2), the capability-adjusted baseline _µ_ ˆ [(] _t_ _[k]_ [)] is computed by



_A_ ˜ [(] _t,i_ _[k]_ [)] [=]








_A_ [(] _t,i_ _[k]_ [)] _yt,i_ [(] _[k]_ [)] _[∈D]_ _t_ [(] _[k]_ [)]



(10)
_ωt_ [(] _[j,k]_ [)] _A_ [(] _t,i_ _[j]_ [)] _yt,i_ [(] _[j]_ [)] _[∈D]_ _t_ [(] _[j]_ [)] _[,]_ _[j]_ [=] _[ k]_







_G_

- _ωt_ [(] _[k,j]_ [)] _R_ - _yt,i_ [(] _[j]_ [)] - _._ (7)

_i_ =1



where _Dt_ [(] _[j]_ [)] denotes the set of samples generated by agent
_j_ at step _t_ . Here, _ωt_ [(] _[k,j]_ [)] represents the performance ratio
between agents _k_ and _j_ at training step _t_, with larger values
indicating that agent _k_ outperforms agent _j_ .

_Remark_ 3.1 _._ We emphasize that the capability ratio _ωt_ [(] _[k,j]_ [)]
appears in two distinct but complementary roles in our
framework. Together, they enable stable and capabilityaware collaboration across heterogeneous agents.
**(i) Baseline Calibration.** In Section 3.1, _ωt_ [(] _[k,j]_ [)] is used to
rescale rewards from agent _j_ when estimating the capabilityaware baseline _µ_ ˆ [(] _t_ _[k]_ [)] . Its role is to _align_ _reward_ _statistics_
_across heterogeneous agents_, ensuring that the baseline used
for agent _k_ is properly calibrated.
**(ii) Gradient Modulation.** In Eq. (10), the same ratio _ωt_ [(] _[k,j]_ [)]



1
_µ_ ˆ [(] _t_ _[k]_ [)] = _nG_



_n_



_j_ =1



Here, _ωt_ [(] _[k,j]_ [)] is a _capability ratio_ that rescales responses from
agent _j_ when estimating the baseline for agent _k_, defined as

_ωt_ [(] _[k,j]_ [)] = _PP_ ˆˆ _tt_ [(][(] _[k][j]_ [)][)] _._ (8)



4


**Heterogeneous Agent Collaborative Reinforcement Learning**



is applied directly to the advantage of responses generated
by agent _j_ when updating agent _k_ . Here, _ωt_ [(] _[k,j]_ [)] serves as a
_learning-rate–like modulation factor_, amplifying gradients
from stronger agents while attenuating those from weaker
ones.


**3.3. Exponential Importance Sampling**


Importance sampling is commonly used to correct distributional mismatches between samples generated by different
policies. Following GSPO, we adopt a sequence-level importance ratio and extend it to the heterogeneous multi-agent
setting. When updating agent _k_ at step _t_, for a response _yt,i_ [(] _[j]_ [)]
generated by agent _j_, we define



**Asymmetric Clipping bounds for Cross-Agent.** Due to
the above distinctions, conventional symmetric clipping
of the form [1 _−_ _ϵ_ low _,_ 1 + _ϵ_ high] is no longer appropriate
for cross-agent importance sampling. This is because, unlike self-agent importance sampling, cross-agent importance
sampling _s_ [(] _t,i_ _[k,j]_ [)] _>_ 1 corresponds to assigning a higher likelihood to responses generated by another agent than to those
generated by the current agent itself. Such amplification
is undesirable in heterogeneous settings although highly
rare, as it may guide cross-agent rollouts to dominate the
gradient updates of the current agent, thereby introducing
severe distributional bias. Instead, we adopt the following
asymmetric clipping scheme, where _δ_ is a hyperparameter
that controls the lower clipping bound:


_s_ [(] _t,i_ _[k,j]_ [)] _∈_ [1 _._ 0 _−_ _δ,_ 1 _._ 0] _, k_ = _j,_ (13)


In Eq.13, we deliberately limit the upper bound of clipping
to 1 _._ 0. This simple modification ensures that cross-agent
responses can only downweight, but never upweight the
learning signals relative to on-policy responses. If _s_ [(] _t,i_ _[k,j]_ [)] _<_
1 _−_ _δ_, the corresponding sample is considered too far from
the current policy and is discarded. In practice, we typically
set _δ_ = 0 _._ 2.


**Stepwise** **Clipping.** To account for the accumulation of
policy drift, we additionally introduce a stepwise clipping
strategy within each training step. Let _k_ denote the number
of parameter updates performed so far within the current
step, and let _δ_ step denote the per-update tightening factor.
The clipping operator is defined as


       -        clip( _s_ [(] _t,i_ _[k,j]_ [)] ) = clip _s_ [(] _t,i_ _[k,j]_ [)] _,_ 1 _−_ _δ_ + _k · δ_ step _,_ 1 _._ 0 _,_ (14)


where _k_ = _j_ . Under this scheme, cross-agent responses
appearing in later mini-batches are subject to increasingly
stricter clipping bounds. This prevents cross-agent rollouts
from dominating late-stage updates within a batch, thereby
improving training stability in heterogeneous collaborative
policy optimization.


**4. Theoretical Analysis of HACPO**


In this section, we establish the theoretical foundations
of HACPO by addressing two fundamental questions: **(i)**
Whether the mixed-response advantage baseline introduces
systematic bias; **(ii)** Whether learning from cross-agent rollouts yields a valid optimization direction.


**4.1. Unbiasedness of Advantage Estimation**


We first demonstrate that the proposed _Agent-Capability-_
_Aware Advantage Estimation_ in HACPO is unbiased.



1

_|yt,i_ [(] _[j]_ [)] _[|]_
_._ (11)








- _yt,i_ [(] _[j]_ [)]


- _yt,i_ [(] _[j]_ [)]



_s_ [(] _t,i_ _[k,j]_ [)] =





_πθ_ [(] _[k]_ _t_ [)]




_πθ_ [(] _[j]_ old [)]










For combinations of heterogeneous agents that satisfy Definition 2.3 with incompatible tokenizers, we detokenize the
response into text and retokenize it using the target agent’s
tokenizer. Through sequence-level normalization, the slight
length discrepancies arising from re-tokenization become
negligible.


In heterogeneous settings, inter-agent policy discrepancies
can be much larger than on-policy updates, making direct
use of this ratio overly aggressive. To mitigate this issue,
we introduce a non-gradient exponential reweighting:


_s_ ˜ [(] _t,i_ _[k,j]_ [)] = _s_ [(] _t,i_ _[k,j]_ [)] _·_ �sg[ _s_ [(] _t,i_ _[k,j]_ [)] ]� _α_ _k_ = _j, s_ [(] _t,i_ _[k,j]_ [)] _<_ 1 _._ 0 (12)


where sg[ _·_ ] denotes the stop-gradient operator and _α_ _≥_ 0
controls the degree of conservativeness.


This design biases agent _k_ toward learning from agents
whose output distributions are more aligned with its own,
while reducing the impact of large cross-agent distribution
shifts.


**3.4. Stepwise Clipping**


We argue that the cross-agent importance sampling ratio
_s_ [(] _t,i_ _[k,j]_ [)] exhibits following fundamentally different behaviors

from the self-agent ratio _s_ [(] _t,i_ _[k,k]_ [)] :


**(1)** _s_ [(] _t,i_ _[k,j]_ [)] evolves dynamically across training iterations;


**(2)** Within a single training step, _s_ [(] _t,i_ _[k,j]_ [)] fluctuates irregularly
as the number of parameter updates increases, in contrast to
the self-agent ratio, which typically decays smoothly.


Additional experimental details on importance sampling in
the heterogeneous-agent setting are provided in Appendix C
due to space constraints.



5


**Heterogeneous Agent Collaborative Reinforcement Learning**



Furthermore, define the advantage for the _i_ -th response of
agent _k_ as:


         -          _A_ [(] _t,i_ _[k]_ [)] := _R_ _yt,i_ [(] _[k]_ [)] _−_ _µ_ [(] _t_ _[k]_ [)] _._ (15)


Consequently, the unbiasedness of _A_ [(] _t,i_ _[k]_ [)] [is] [established] [as]
follows:





|Col1|Col2|Col3|Col4|Col5|Col6|Col7|
|---|---|---|---|---|---|---|
||||||||
||||||||
||||||||
||||||4B(<br>|HACPO)<br>|
||||||4B(|GSPO)|


Training Steps



Theorem 4.3 shows that cross-agent responses provide a
directionally consistent learning signal. As a result, HACPO
preserves the optimization direction of standard on-policy
learning while enabling agents to leverage additional crossagent experience, thereby improving data efficiency without
introducing adverse optimization bias. The complete proof
is provided in Appendix D.3.


**5. Experiment**



|Col1|Col2|Col3|Col4|Col5|Col6|Col7|
|---|---|---|---|---|---|---|
||||||||
||||||||
||||||||
||||||||
||||||||
|||||4B-In<br>|struct(<br>|HACPO)<br>|
|||||~~4B-In~~|~~struct(~~|~~GSPO)~~|


Training Steps


|Col1|Col2|Col3|Col4|Col5|Col6|Col7|
|---|---|---|---|---|---|---|
||||||||
||||||||
||||||||
||||||||
||||||||
|||||~~1.7B_~~<br>1.7B_|~~Base(~~<br>Base(|~~ACPO)~~<br>GSPO)|


|Col1|Col2|Col3|Col4|Col5|Col6|
|---|---|---|---|---|---|
|||||||
|||||||
|||||||
||||4B<br>4B_|Base(<br>Base(G|ACPO)<br>SPO)|



|Col1|Col2|Col3|Col4|Col5|Col6|Col7|
|---|---|---|---|---|---|---|
||||||||
||||||||
||||||||
||||||||
||||||||
|||||~~Qwe~~<br>Qwen|~~3-4B(~~<br>3-4B(|~~ACPO)~~<br>GSPO)|


0 10 20 30 40 50 60
Training Steps



0.875


0.870


0.865


0.860


0.855


0.850





_(a)_ Qwen3: 4B vs 4B-Instruct

0.80


0.75



0 10 20 30 40 50 60
Training Steps



0.70


0.65


0.60



Theorem 4.1 states that, although HACPO computes the
baseline _µ_ [(] _t_ _[k]_ [)] using a mixture of responses collected from
multiple agents, this mixed baseline remains _unbiased_ for
the on-policy expected reward of the trained agent _k_ . This
result provides theoretical justification for incorporating
cross-agent responses into advantage estimation without
introducing systematic bias, as shown in Corollary 4.2.


**4.2. Gradient Consistency and Effectiveness**


The effectiveness of HACPO relies on the premise that
learning from cross-agent rollouts induces an optimization
direction consistent with standard on-policy learning. In
this section, we formalize this intuition by showing that the
gradient of the heterogeneous objective is positively aligned
with that of the homogeneous objective.


We analyze the optimization directions induced by the homogeneous objective _J_ homo [(] _[k]_ [)] [and the heterogeneous objective]
_J_ hete [(] _[k]_ [)] [for agent] _[ k]_ [.] [Detailed gradient derivations are deferred]
to Appendix D.2; here, we focus on their directional properties.

For the heterogeneous objective _J_ hete [(] _[k]_ [)] [,] [HACPO] [incorpo-]
rates cross-agent responses through importance weighting,
clipping, and capability-aware scaling. Under this design,
we establish the following result.


|Col1|Col2|Col3|Col4|Col5|Col6|
|---|---|---|---|---|---|
|||||||
|||||||
|||||||
|||||||
||||~~Llama3~~<br>Llama3|~~2-3B(~~<br>.2-3B(G|~~ACPO)~~<br>SPO)|



_(c)_ Qwen 4B vs Llama 3B


_Figure 3._ Training curves of GSPO and HACPO


**Setting Details.** We adopt 7.5k high quality math questions
from the MATH dataset (Hendrycks et al., 2021) for training.
During evaluation, we select a comprehensive set of benchmarks: MATH-500, MATH, GSM8K (Cobbe et al., 2021),
AIME2025, AMC23(Cairns, 1916), Minerva(Lewkowycz
et al., 2022) and Olympiad(He et al., 2024).


To verify the effectiveness of our method, we conduct experiments on the three heterogeneity settings mentioned
in Section 2.1.We compare our approach against the following baselines: (1) **Standard** **Single-Agent** **Baselines**
**(GRPO, GSPO)**, which serve as benchmarks for isolated



0.86


0.84


0.82


0.80


0.650

0.625

0.600

0.575

0.550

0.525

0.500


0.750

0.725

0.700

0.675

0.650

0.625

0.600



0 10 20 30 40 50 60
Training Steps



_(b)_ Qwen3: 1.7B-Base vs 4B-Base


0.55


0.50



0 10 20 30 40 50 60
Training Steps



0.45


0.40


0.35


0.30


0.25



6


**Heterogeneous Agent Collaborative Reinforcement Learning**


_Table 1._ Main results across three heterogeneity settings. We compare our method against Standard Single-Agent Baselines (GRPO,
GSPO), a Resource-Equivalent Baseline (GSPO _×_ 2) and a Naive multi-agent rollout share baseline(Naive).


Model MATH-500 MATH GSM8K AIME2025 AMC23 Minerva Olympiad AVG


Qwen3-4B + Qwen3-4B-Instruct


4B 0.802 0.836 0.907 0.335 0.65 0.39 0.524 0.635
4B (GRPO) 0.88 0.889 0.918 0.582 0.775 0.386 0.592 0.717
4B (GSPO) 0.854 0.87 0.925 0.485 0.675 0.412 0.564 0.684
4B (GSPO _×_ 2) 0.876 0.875 0.923 0.522 0.675 0.39 0.579 0.691
4B (Naive) 0.728 0.737 0.891 0.378 0.6 0.353 0.394 0.583
4B(HACPO) **0.91** **0.905** **0.933** **0.622** **0.85** **0.423** **0.643** **0.755**
4B-Instruct 0.938 0.937 0.936 0.696 0.85 0.441 0.722 0.789
4B-Instruct (GRPO) 0.93 0.933 0.933 0.676 0.875 0.43 0.72 0.785
4B-Instruct (GSPO) 0.938 0.94 0.939 0.72 0.9 0.43 0.726 0.799
4B-Instruct (GSPO _×_ 2) 0.932 0.939 0.942 0.74 0.9 0.43 0.711 0.799
4B-Instruct(Naive) 0.844 0.845 0.936 0.547 0.725 0.39 0.552 0.691
4B-Instruct(HACPO) **0.948** **0.943** **0.946** **0.757** **0.95** **0.452** **0.732** **0.813**


Qwen3-1.7B-Base + Qwen3-4B-Base


1.7B-Base 0.5 0.483 0.616 0.033 0.3 0.206 0.229 0.338
1.7B-Base (GRPO) 0.682 0.652 0.824 0.16 0.375 0.272 0.298 0.466
1.7B-Base (GSPO) 0.648 0.641 0.826 0.148 0.45 0.272 0.287 0.467
1.7B-Base (GSPO _×_ 2) 0.664 0.65 **0.829** 0.177 0.375 0.265 0.293 0.475
1.7B-Base(Naive) 0.608 0.601 0.798 0.147 0.325 0.235 0.263 0.425
1.7B-Base(HACPO) **0.69** **0.674** 0.822 **0.225** **0.45** **0.279** **0.314** **0.493**
4B-Base 0.61 0.676 0.445 0.1 0.4 0.308 0.347 0.412
4B-Base (GRPO) 0.796 0.788 0.885 **0.307** 0.475 0.349 0.454 0.579
4B-Base (GSPO) 0.782 0.787 0.877 0.25 0.525 0.368 0.46 0.578
4B-Base (GSPO _×_ 2) 0.756 0.794 0.873 0.208 0.55 0.382 0.463 0.575
4B-Base (Naive) 0.708 0.712 0.895 0.196 0.475 0.342 0.354 0.526
4B-Base(HACPO) **0.808** **0.801** **0.903** 0.267 **0.575** **0.386** **0.467** **0.601**


Qwen3-4B-Base + Llama3.2-3B-Instruct


qwen3-4B 0.61 0.676 0.445 0.1 0.4 0.308 0.347 0.412
qwen3-4B (GRPO) **0.796** 0.788 0.885 **0.307** 0.475 0.349 0.454 0.579
qwen3-4B (GSPO) 0.782 0.787 0.877 0.25 0.525 0.368 **0.46** 0.578
qwen3-4B (GSPO _×_ 2) 0.756 **0.794** 0.873 0.208 0.55 **0.382** 0.463 0.575
qwen3-4B (Naive) 0.734 0.712 0.895 0.143 0.55 0.342 0.354 0.526
qwen3-4B (HACPO) 0.786 0.783 **0.921** 0.268 **0.6** 0.379 0.442 **0.597**
llama3.2-3B 0.267 0.441 0.788 0.0 0.2 0.169 0.158 0.289
llama3.2-3B (GRPO) 0.502 0.507 0.814 0.0 0.25 **0.199** 0.174 0.349
llama3.2-3B (GSPO) 0.512 0.501 0.812 0.054 0.225 0.184 0.17 0.351
llama3.2-3B (GSPO _×_ 2) 0.488 0.498 **0.829** 0.0 0.175 0.188 0.159 0.334
llama3.2-3B (Naive) 0.406 0.407 0.734 0.0 0.225 0.177 0.107 0.294
llama3.2-3B (HACPO) **0.566** **0.548** 0.826 **0.054** **0.35** 0.176 **0.208** **0.39**



training performance (same rollout cost as HACPO but with
half the policy updates); (2) **Resource-Equivalent Baseline**
**(GSPO** _×_ **2)**, a single-agent GSPO setting with double rollouts and updates in every step. This serves to rule out the
impact of increased data volume and verify the complementary value of heterogeneous agents (double the rollout cost
of HACPO but with the same policy updates); (3) **Naive**
**Collaborative Baseline (Naive)**, a two-agent setting with
shared rollouts but lacking the algorithmic innovations in
Section 3, used to validate the necessity of our proposed
discrepancy mitigation techniques (same rollout and policy
update costs as HACPO).



**5.1. Result and Analysis**


As detailed in Table 1, HACPO demonstrates superior final
performance compared to all baselines across various heterogeneous settings. To illustrate the learning dynamics, Figure
3 presents the training curves of HACPO versus the singleagent GSPO baseline. We attribute these performance gains
to two primary mechanisms inherent in the HACPO: (1)
Capability-driven guidance, where stronger models assist in
enhancing the performance of weaker ones; and (2) Mutual
knowledge exchange, which involves the sharing of complementary rollouts—encompassing both correct solutions and
informative errors—between agents.


**Heterogeneous State.** In the Qwen3-4B and Qwen3-4BInstruct setting, we observe asymmetric but non-trivial gains:



7


**Heterogeneous Agent Collaborative Reinforcement Learning**


_Table 2._ Ablation of Advantage Estimator


Model MATH-500 math gsm8k aime2025 ACM23 minerva olympiad AVG


1.7B(HACPO - Adv) **0.696** 0.659 **0.825** 0.126 0.375 0.261 0.313 0.465
1.7B(HACPO) 0.69 **0.674** 0.822 **0.225** **0.45** **0.279** **0.314** **0.493**
4B(HACPO - Adv) 0.774 0.771 **0.912** **0.308** 0.55 0.348 0.442 0.586
4B(HACPO) **0.808** **0.801** 0.903 0.267 **0.575** **0.386** **0.467** **0.601**


_Table 3._ Ablation of Model Capabilities Discrepancy Coefficient


Model MATH-500 math gsm8k aime2025 ACM23 minerva olympiad AVG


1.7B(HACPO - _ω_ ) 0.666 0.657 0.806 0.105 0.425 0.25 **0.324** 0.462
1.7B(HACPO) **0.69** **0.674** **0.822** **0.225** **0.45** **0.279** 0.314 **0.493**
4B(HACPO - _ω_ ) **0.816** 0.797 0.902 0.261 0.55 **0.401** **0.475** 0.6
4B(HACPO) 0.808 **0.801** **0.903** **0.267** **0.575** 0.386 0.467 **0.601**



while the 4B model improves more substantially, the Instruct
model also exhibits consistent performance improvements.
Although this setting corresponds to heterogeneous state,
where agents differ only due to post-training stages, HACPO
still enables the stronger agent to benefit from the weaker
one. Specifically, the weaker agent contributes complementary exploration signals—such as alternative reasoning
paths and informative errors—that are underrepresented in
the stronger agent’s own rollouts. As a result, learning
is not purely unidirectional. Even when capability-driven
guidance dominates, the stronger agent can still extract useful supervisory signals from the weaker agent, leading to
measurable performance gains.


**Heterogeneous Size.** In the Qwen3-1.7B-Base and Qwen34B-Base setting, both models improve significantly, validating the mechanism of mutual knowledge exchange. Even
with lower capability, the 1.7B model serves as a distinct
explorer, generating valuable erroneous responses and a few
unique correct solutions that the 4B model fails to produce,
thereby facilitating bidirectional knowledge transfer. **Het-**
**erogeneous Model.** Finally, we consider the heterogeneous
model setting involving Qwen3-4B-Base and Llama3.2-3BInstruct, which differ substantially in architecture, tokenizer,
and training objectives. Despite this high degree of heterogeneity, we observe consistent performance improvements
in both models. These results demonstrate that HACPO is
able to extract transferable knowledge from cross-model
rollouts and effectively share it across heterogeneous agents.
By leveraging verified responses—including correct solutions and informative failure cases—each model can learn
from complementary reasoning patterns that are absent from
its own policy distribution.


The experimental results show that HACPO significantly
improves performance across all three types of heterogeneity, validating its generality and robustness. Additionally,
the differences observed among the three settings shed light
on the two underlying mechanisms of HACPO.



_Table 4._ Qwen3-1.7B-Base and Qwen3-4B-Base


_α_ 0.0 **1.0** 2.0 3.0


Qwen3-1.7B-Base and Qwen3-4B-Base


1.7B-Base 0.63 0.664 0.654 **0.668**
4B-Base 0.756 **0.792** 0.768 0.77


Qwen3-4B-Base and Qwen3-8B-Base


4B-Base 0.772 0.776 0.77 **0.776**
8B-Base 0.764 0.772 0.766 **0.778**


**5.2. Ablation Study**


**Agent-Capability-Aware Advantage Estimation.** Ablation on the Qwen3-1.7B/4B-Base combination (Table 2)
confirms that removing this module significantly degrades
performance. This decline stems from the systematic bias
in standard group-relative advantages in multi-agent setting due to the capability discrepancy cross heterogenous
agents. Our method addresses this by constructing _agent-_
_capability-aware_ advantage baselines—raising the standard
for the stronger models and lowering it for the weaker
ones—thereby preserving the unbiasedness of the advantage
estimator established in Theorem 4.1.


**Model Capabilities Discrepancy Coefficient.** We isolate
this coefficient in gradient modulation by disabling it in
Eq.10, while retaining it for advantage estimation. Table
3 confirms that removing this modulation degrades performance. This validates the coefficient’s critical function as a
capability-aware scaler: it amplifies gradients from stronger
agents to accelerate learning, while attenuating updates from
weaker ones to mitigate potential noise.


**Exponential Importance Sampling.** We examined the impact of _α_ on Qwen3-1.7B/4B-Base and Qwen3-4B/8B-Base
combinations (Table 4). Results highlight a critical trade-off:
increasing _α_ enforces a more conservative policy towards
cross-agent responses, which aids stability by suppressing
large distribution shifts but hinders efficiency by reducing
the effective learning signal. Thus, the optimal _α_ is model



8


**Heterogeneous Agent Collaborative Reinforcement Learning**



combination dependent, necessitating a balance between
stable convergence and maximal information extraction.


**Stepwise Clipping.** We assess the necessity of this mechanism on the Qwen3-4B/8B-Base combination. As visualized in Figure 4, removing the clipping constraint ( **no**
**Clip** ) causes severe instability, while omitting the stepwise
schedule ( **no** **Stepwise** ) leads to suboptimal convergence
compared to the full HACPO. This confirms that the stepwise clipping is indispensable for stabilizing collaborative
learning, as neither unconstrained nor statically bounded updates suffice to handle high-variance cross-agent responses.



0.80


0.75


0.70


0.65


0.60



|Col1|Col2|Col3|Col4|Col5|Col6|Col7|
|---|---|---|---|---|---|---|
||||||||
||||||||
||||||||
|||<br>|~~4B_Bas~~<br>4B_Bas<br>4B_Bas|~~e(HACP~~<br>e(HACP<br>e(HACP|~~O)~~<br>O no S<br>O no C|tepwise)<br> lip)|


0 25 50 75 100 125 150
Training Steps


_(a)_ Qwen3-4B-Base



|Col1|Col2|Col3|Col4|Col5|Col6|Col7|Col8|
|---|---|---|---|---|---|---|---|
|||||||||
|||||||||
|||||||||
|||||||||
||||8B_Base<br>|(HACP<br>|O)<br>|O)<br>||
|||<br>|~~8B_Bas~~<br>~~8B_Base~~|~~(HACP~~<br>~~(HACP~~|~~O no S~~<br>~~O no Cl~~|~~O no S~~<br>~~O no Cl~~|~~ epwise)~~<br>~~ ip)~~|


0 25 50 75 100 125 150
Training Steps


_(b)_ Qwen3-8B-Base



0.825

0.800

0.775

0.750

0.725

0.700

0.675

0.650



_Figure 4._ The Ablation of Stepwise Clipping


**6. Related Work**


Our work is most closely related to Reinforcement Learning with Verifiable Rewards (RLVR), with Group Sequence
Policy Optimization (GSPO) being the most relevant prior
study. GSPO demonstrates the efficacy of sequence-level
importance sampling in Mixture-of-Experts (MoE) models,
where tokens may originate from different networks. This
insight inspires our approach to facilitate rollout sharing
among heterogeneous agents. Additionally, our work shares
conceptual parallels with Multi-Agent Reinforcement Learning (MARL). A more detailed discussion of related work is
provided in Appendix B.


**7. Conclusion**


We propose HACRL, a collaborative multi-agent reinforcement learning paradigm tailored for heterogeneous agent
ecosystems. HACRL enables principled rollout sharing
among heterogeneous agents, improving sample utilization
efficiency while promoting cross-agent knowledge transfer. To instantiate this paradigm, we introduce HACPO,
which incorporates four tailored mechanisms to mitigate
capability discrepancies and policy distribution shifts arising during collaborative policy optimization. We provide
the theoretical analysis establishing the unbiasedness of the
proposed advantage estimation scheme and the validity of
the resulting optimization direction under controlled heterogeneity. Extensive experiments demonstrate that HACPO
consistently and significantly improves performance across
all heterogeneity types.



**Impact Statement**


This paper presents a collaborative policy optimization
framework for heterogeneous Large Language Models, aiming to enhance the efficiency and effectiveness of posttraining through cross-agent rollout sharing and verifiable
rewards. There are many potential societal consequences
of our work, none which we feel must be specifically highlighted here.


**References**


Agarwal, R., Vieillard, N., Zhou, Y., Stanczyk, P., Garea,
S. R., Geist, M., and Bachem, O. On-policy distillation
of language models: Learning from self-generated mistakes. In _The twelfth international conference on learning_
_representations_, 2024a.


Agarwal, R., Vieillard, N., Zhou, Y., Stanczyk, P., Garea,
S. R., Geist, M., and Bachem, O. C. In _The_ _Twelfth_
_International Conference on Learning Representations_,
2024b.


Anil, R., Pereyra, G., Passos, A., Ormandi, R., Dahl, G. E.,
and Hinton, G. E. Large scale distributed neural network training through online distillation. _arXiv preprint_
_arXiv:1804.03235_, 2018.


Cai, W., Liu, Q., and Wang, Y. Learning historical status
prompt for accurate and robust visual tracking. _arXiv_
_preprint arXiv:2311.02072_, 7, 2023.


Cai, W., Liu, Q., and Wang, Y. Hiptrack: Visual tracking
with historical prompts. In _Proceedings of the IEEE/CVF_
_Conference on Computer Vision and Pattern Recognition_,
pp. 19258–19267, 2024.


Cai, W., Jiang, J., Wang, F., Tang, J., Kim, S., and Huang, J.
A survey on mixture of experts in large language models.
_IEEE Transactions on Knowledge and Data Engineering_,
2025a.


Cai, W., Liu, Q., and Wang, Y. Spmtrack: spatio-temporal
parameter-efficient fine-tuning with mixture of experts for
scalable visual tracking. In _Proceedings of the computer_
_vision_ _and_ _pattern_ _recognition_ _conference_, pp. 16871–
16881, 2025b.


Cai, W., Zhu, D., Liu, Q., and Min, Q. Seednorm:
Self-rescaled dynamic normalization. _arXiv_ _preprint_
_arXiv:2510.22777_, 2025c.


Cairns, W. The mathematical association of america. _The_
_American Mathematical Monthly_, 23(1):1–6, 1916.


Chen, Z., Ai, T., Li, Y., Li, G., Wei, Y., Zhou, W., Li, G.,
Yu, B., Chen, Z., Sun, H., Zhuang, F., Li, J., Wang, D.,
and Ban, Y. Llmboost: Make large language models



9


**Heterogeneous Agent Collaborative Reinforcement Learning**



stronger with boosting, 2025. [URL https://arxiv.](https://arxiv.org/abs/2512.22309)
[org/abs/2512.22309.](https://arxiv.org/abs/2512.22309)


Chen, Z., Li, G., Ai, T., Li, Y., Huang, Z., Zhou, W.,
Zhuang, F., Liu, X., Li, J., Wang, D., and Ban, Y. Weakdriven learning: How weak agents make strong agents
stronger, 2026. URL [https://arxiv.org/abs/](https://arxiv.org/abs/2602.08222)
[2602.08222.](https://arxiv.org/abs/2602.08222)


Cobbe, K., Kosaraju, V., Bavarian, M., Chen, M., Jun, H.,
Kaiser, L., Plappert, M., Tworek, J., Hilton, J., Nakano,
R., et al. Training verifiers to solve math word problems.
_arXiv preprint arXiv:2110.14168_, 2021.


Du, Y., Li, S., Torralba, A., Tenenbaum, J. B., and Mordatch,
I. Improving factuality and reasoning in language models
through multiagent debate. In _Forty-first International_
_Conference on Machine Learning_, 2023.


Foerster, J., Farquhar, G., Afouras, T., Nardelli, N., and
Whiteson, S. Counterfactual multi-agent policy gradients. In _Proceedings of the AAAI conference on artificial_
_intelligence_, volume 32, 2018.


Fu, Z., Fu, Z., Liu, Q., Cai, W., and Wang, Y. Sparsett:
Visual tracking with sparse transformers. _arXiv preprint_
_arXiv:2205.03776_, 2022.


Gou, J., Yu, B., Maybank, S. J., and Tao, D. Knowledge
distillation: A survey. _International journal of computer_
_vision_, 129(6):1789–1819, 2021.


Grattafiori, A., Dubey, A., Jauhri, A., Pandey, A., Kadian,
A., Al-Dahle, A., Letman, A., Mathur, A., Schelten, A.,
Vaughan, A., et al. The llama 3 herd of models. _arXiv_
_preprint arXiv:2407.21783_, 2024.


He, C., Luo, R., Bai, Y., Hu, S., Thai, Z., Shen, J., Hu, J.,
Han, X., Huang, Y., Zhang, Y., et al. Olympiadbench: A
challenging benchmark for promoting agi with olympiadlevel bilingual multimodal scientific problems. In _Pro-_
_ceedings of the 62nd Annual Meeting of the Association_
_for Computational Linguistics (Volume 1:_ _Long Papers)_,
pp. 3828–3850, 2024.


Hendrycks, D., Burns, C., Kadavath, S., Arora, A., Basart,
S., Tang, E., Song, D., and Steinhardt, J. Measuring mathematical problem solving with the math dataset. _arXiv_
_preprint arXiv:2103.03874_, 2021.


Hinton, G., Vinyals, O., and Dean, J. Distilling
the knowledge in a neural network. _arXiv_ _preprint_
_arXiv:1503.02531_, 2015.


Ho, N., Schmid, L., and Yun, S.-Y. Large language models
are reasoning teachers. In _Proceedings of the 61st annual_
_meeting of the association for computational linguistics_
_(volume 1:_ _long papers)_, pp. 14852–14882, 2023.


10



Hsieh, C.-Y., Li, C.-L., Yeh, C.-K., Nakhost, H., Fujii, Y.,
Ratner, A., Krishna, R., Lee, C.-Y., and Pfister, T. Distilling step-by-step! outperforming larger language models
with less training data and smaller model sizes. In _Find-_
_ings_ _of_ _the_ _Association_ _for_ _Computational_ _Linguistics:_
_ACL 2023_, pp. 8003–8017, 2023.


Huang, Z., Ban, Y., Fu, L., Li, X., Dai, Z., Li, J., and
deqing wang. Adaptive batch-wise sample scheduling
for direct preference optimization. In _The Thirty-ninth_
_Annual_ _Conference_ _on_ _Neural_ _Information_ _Processing_
_Systems_, 2025. [URL https://openreview.net/](https://openreview.net/forum?id=8FN25PlktS)
[forum?id=8FN25PlktS.](https://openreview.net/forum?id=8FN25PlktS)


Huang, Z., Xia, X., Ren, Y., Zheng, J., Wang, X., Zhang, Z.,
Xie, H., Liang, S., Chen, Z., Xiao, X., et al. Does your
reasoning model implicitly know when to stop thinking?
_arXiv preprint arXiv:2602.08354_, 2026a.


Huang, Z., Xia, X., Ren, Y., Zheng, J., Xiao, X., Xie, H.,
Huaqiu, L., Liang, S., Dai, Z., Zhuang, F., et al. Real-time
aligned reward model beyond semantics. _arXiv preprint_
_arXiv:2601.22664_, 2026b.


Kuba, J. G., Chen, R., Wen, M., Wen, Y., Sun, F., Wang,
J., and Yang, Y. Trust region policy optimisation
in multi-agent reinforcement learning. _arXiv_ _preprint_
_arXiv:2109.11251_, 2021.


Lewkowycz, A., Andreassen, A., Dohan, D., Dyer, E.,
Michalewski, H., Ramasesh, V., Slone, A., Anil, C.,
Schlag, I., Gutman-Solo, T., et al. Solving quantitative
reasoning problems with language models. _Advances in_
_neural_ _information_ _processing_ _systems_, 35:3843–3857,
2022.


Li, H., Hu, X., and Wang, H. Interpretable unsupervised
joint denoising and enhancement for real-world low-light
scenarios. _arXiv preprint arXiv:2503.14535_, 2025a.


Li, H., Wang, Y., Huang, T., Huang, H., Wang, H., and Chu,
X. Ld-rps: Zero-shot unified image restoration via latent
diffusion recurrent posterior sampling. In _Proceedings_
_of the IEEE/CVF International Conference on Computer_
_Vision_, pp. 13684–13694, 2025b.


Li, H., Zhang, W., Hu, X., Jiang, T., Chen, Z., and Wang,
H. Prompt-sid: Learning structural representation prompt
via latent diffusion for single image denoising. In _Pro-_
_ceedings_ _of_ _the_ _AAAI_ _Conference_ _on_ _Artificial_ _Intelli-_
_gence_, volume 39, pp. 4734–4742, 2025c.


Li, Y., Zhang, Y., and Sun, L. Metaagents: Simulating interactions of human behaviors for llm-based task-oriented
coordination via collaborative generative agents. _arXiv_
_preprint arXiv:2310.06500_, 2023.


**Heterogeneous Agent Collaborative Reinforcement Learning**



Liao, J., Wen, M., Wang, J., and Zhang, W. Marft:
Multi-agent reinforcement fine-tuning. _arXiv_ _preprint_
_arXiv:2504.16129_, 2025a.


Liao, J., Wen, M., Wang, J., and Zhang, W. Marft:
Multi-agent reinforcement fine-tuning. _arXiv_ _preprint_
_arXiv:2504.16129_, 2025b.


Liu, S., Liang, Z., Lyu, X., and Amato, C. Llm collaboration
with multi-agent reinforcement learning. _arXiv preprint_
_arXiv:2508.04652_, 2025.


Liu, W., Wu, H., Kuang, Y., Han, X., Zhong, T., Feng,
J., and Lu, W. Automated optimization modeling via
a localizable error-driven perspective. _arXiv_ _preprint_
_arXiv:2602.11164_, 2026.


Lowe, R., Wu, Y. I., Tamar, A., Harb, J., Pieter Abbeel,
O., and Mordatch, I. Multi-agent actor-critic for mixed
cooperative-competitive environments. _Advances in neu-_
_ral information processing systems_, 30, 2017.


Ma, H., Hu, T., Pu, Z., Boyin, L., Ai, X., Liang, Y., and
Chen, M. Coevolving with the other you: Fine-tuning llm
with sequential cooperative multi-agent reinforcement
learning. _Advances_ _in_ _Neural_ _Information_ _Processing_
_Systems_, 37:15497–15525, 2024.


Madaan, L., Didolkar, A., Gururangan, S., Quan, J., Silva,
R., Salakhutdinov, R., Zaheer, M., Arora, S., and Goyal,
A. Rethinking thinking tokens: Llms as improvement
operators. _arXiv preprint arXiv:2510.01123_, 2025.


Ouyang, L., Wu, J., Jiang, X., Almeida, D., Wainwright, C.,
Mishkin, P., Zhang, C., Agarwal, S., Slama, K., Ray, A.,
et al. Training language models to follow instructions
with human feedback. _Advances in neural information_
_processing systems_, 35:27730–27744, 2022a.


Ouyang, L., Wu, J., Jiang, X., Almeida, D., Wainwright, C.,
Mishkin, P., Zhang, C., Agarwal, S., Slama, K., Ray, A.,
et al. Training language models to follow instructions
with human feedback. _Advances in neural information_
_processing systems_, 35:27730–27744, 2022b.


Park, C., Han, S., Guo, X., Ozdaglar, A., Zhang, K., and
Kim, J.-K. Maporl: Multi-agent post-co-training for
collaborative large language models with reinforcement
learning. _arXiv preprint arXiv:2502.18439_, 2025.


Rafailov, R., Sharma, A., Mitchell, E., Manning, C. D.,
Ermon, S., and Finn, C. Direct preference optimization: Your language model is secretly a reward model.
_Advances in neural information processing systems_, 36:
53728–53741, 2023.


Rashid, T., Samvelyan, M., De Witt, C. S., Farquhar, G.,
Foerster, J., and Whiteson, S. Monotonic value function



factorisation for deep multi-agent reinforcement learning.
_Journal_ _of_ _Machine_ _Learning_ _Research_, 21(178):1–51,
2020.


Romero, A. Fitnets: Hints for thin deep nets. _arXiv preprint_
_arXiv:1412.6550_, 2014.


Sanh, V., Debut, L., Chaumond, J., and Wolf, T. Distilbert,
a distilled version of bert: smaller, faster, cheaper and
lighter. _arXiv preprint arXiv:1910.01108_, 2019.


Schulman, J., Wolski, F., Dhariwal, P., Radford, A., and
Klimov, O. Proximal policy optimization algorithms.
_arXiv preprint arXiv:1707.06347_, 2017.


Shao, Z., Wang, P., Zhu, Q., Xu, R., Song, J., Bi, X., Zhang,
H., Zhang, M., Li, Y., Wu, Y., et al. Deepseekmath: Pushing the limits of mathematical reasoning in open language
models. _arXiv preprint arXiv:2402.03300_, 2024.


Sheng, G., Zhang, C., Ye, Z., Wu, X., Zhang, W., Zhang,
R., Peng, Y., Lin, H., and Wu, C. Hybridflow: A flexible
and efficient rlhf framework. _CoRR_, abs/2409.19256,
2024. doi: 10.48550/ARXIV.2409.19256. [URL https:](https://arxiv.org/abs/2409.19256)
[//arxiv.org/abs/2409.19256.](https://arxiv.org/abs/2409.19256)


Stiennon, N., Ouyang, L., Wu, J., Ziegler, D., Lowe, R.,
Voss, C., Radford, A., Amodei, D., and Christiano, P. F.
Learning to summarize with human feedback. _Advances_
_in neural information processing systems_, 33:3008–3021,
2020.


Wan, Z., Li, Y., Wen, X., Song, Y., Wang, H., Yang, L.,
Schmidt, M., Wang, J., Zhang, W., Hu, S., et al. Rema:
Learning to meta-think for llms with multi-agent reinforcement learning. _arXiv_ _preprint_ _arXiv:2503.09501_,
2025.


Wang, J., Liu, R., Lin, L., Hu, W., Li, X., Zhang, F., Zhou,
G., and Gai, K. Aspo: Asymmetric importance sampling
policy optimization. _arXiv preprint arXiv:2510.06062_,
2025.


Weyssow, M., Zhou, X., Kim, K., Lo, D., and Sahraoui,
H. Exploring parameter-efficient fine-tuning techniques
for code generation with large language models. _ACM_
_Transactions on Software Engineering and Methodology_,
34(7):1–25, 2025.


Xie, H., Ban, Y., Fang, R., Huang, Z., Wang, D., Li, J., Yao,
Y., Wang, C., and Song, S. Uniarm: Towards a unified
autoregressive reward model for multi-objective test-time
alignment. _arXiv preprint arXiv:2602.09538_, 2026.


Yang, A., Li, A., Yang, B., Zhang, B., Hui, B., Zheng, B.,
Yu, B., Gao, C., Huang, C., Lv, C., et al. Qwen3 technical
report. _arXiv preprint arXiv:2505.09388_, 2025a.



11


**Heterogeneous Agent Collaborative Reinforcement Learning**


Yang, F., Chen, Z., Wang, X., Lu, X., Chai, J., Yin, G., Lin,
W., Ma, S., Zhuang, F., Wang, D., Yang, Y., Li, J., and
Ban, Y. Your group-relative advantage is biased, 2026a.
[URL https://arxiv.org/abs/2601.08521.](https://arxiv.org/abs/2601.08521)


Yang, F., Chen, Z., Wang, X., Lu, X., Chai, J., Yin,
G., Lin, W., Ma, S., Zhuang, F., Wang, D., et al.
Your group-relative advantage is biased. _arXiv preprint_
_arXiv:2601.08521_, 2026b.


Yang, S., Dou, C., Guo, P., Lu, K., Ju, Q., Deng, F., and Xin,
R. Dcpo: Dynamic clipping policy optimization. _arXiv_
_preprint arXiv:2509.02333_, 2025b.


Yu, C., Velu, A., Vinitsky, E., Gao, J., Wang, Y., Bayen, A.,
and Wu, Y. The surprising effectiveness of ppo in cooperative multi-agent games. _Advances in neural information_
_processing systems_, 35:24611–24624, 2022.


Yu, Q., Zhang, Z., Zhu, R., Yuan, Y., Zuo, X., Yue, Y., Dai,
W., Fan, T., Liu, G., Liu, L., et al. Dapo: An open-source
llm reinforcement learning system at scale. _arXiv preprint_
_arXiv:2503.14476_, 2025.


Zhao, F., Lu, C., Xie, Z., Liu, Z., Qian, H., Huang, J., Shi,
F., Meng, Z., Guo, H., He, M., et al. Redone: Revealing domain-specific llm post-training in social networking services. In _Proceedings_ _of_ _the_ _2025_ _Conference_
_on Empirical Methods in Natural Language Processing:_
_Industry Track_, pp. 2648–2674, 2025a.


Zhao, Y., Liu, Y., Liu, J., Chen, J., Wu, X., Hao, Y., Lv, T.,
Huang, S., Cui, L., Ye, Q., et al. Geometric-mean policy
optimization. _arXiv preprint arXiv:2507.20673_, 2025b.


Zheng, C., Liu, S., Li, M., Chen, X.-H., Yu, B., Gao,
C., Dang, K., Liu, Y., Men, R., Yang, A., et al.
Group sequence policy optimization. _arXiv_ _preprint_
_arXiv:2507.18071_, 2025.


Zhong, Y., Kuba, J. G., Feng, X., Hu, S., Ji, J., and Yang, Y.
Heterogeneous-agent reinforcement learning. _Journal of_
_Machine Learning Research_, 25(32):1–67, 2024.


Zou, J., Ban, Y., Li, Z., Qi, Y., Qiu, R., Yang, L., and
He, J. Transformer copilot: Learning from the mistake
log in LLM fine-tuning. In _The_ _Thirty-ninth_ _Annual_
_Conference on Neural Information Processing Systems_,
2025. [URL https://openreview.net/forum?](https://openreview.net/forum?id=MRvxlTlkNQ)
[id=MRvxlTlkNQ.](https://openreview.net/forum?id=MRvxlTlkNQ)


12


**Heterogeneous Agent Collaborative Reinforcement Learning**


**A. Training and Evalution Details**


All experiments in this paper are conducted using verl (Sheng et al., 2024). In the experiments, we set the maximum prompt
length to 1024 and the maximum response length to 4096. We use the MATH dataset for training. The learning rate is
set to 1 _×_ 10 _[−]_ [6] . For the responses generated by the trained agents in HACPO or single GSPO, we set _ϵ_ low = 0 _._ 0003 and
_ϵ_ high = 0 _._ 0004, which is consistent with the setting mentioned in GSPO(Zheng et al., 2025). As for the single GRPO, we set
_ϵ_ low = 0 _._ 2 and _ϵ_ high = 0 _._ 28, which follows the trick mentioned in DAPO (Yu et al., 2025) and is widely used. The batch
size is set to 128, with a mini-batch size of 64 and _n_ = 8 rollouts per prompt. The total batch size is set to 128, with a
mini-batch size of 64 and _n_ = 8 rollouts per prompt. In the Resource-Equivalent Baseline (GSPO _×_ 2), we use a mini-batch
size of 32 and _n_ = 16 rollouts per prompt to ensure double updates per step, while maintaining a consistent number of
rollouts per update with other settings. We train for one epoch, except when examining the impact of stepwise clipping
on stabilizing the training process. During evaluation, due to the high complexity of benchmarks such as AIME2025, we
adopt a maximum response length of 8196 tokens in the main experiments and the ablation of Agent-Capability-Aware
Advantage Estimator and Model Capability Discrepancy Coefficient (Table 1, Table 7, Table 3 and Table 2). For all other
ablation studies, the maximum response length is kept consistent with the training configuration and is set to 4096 tokens.
For the main experimental results, we report best@30 on AIME2025, while avg@1 is used for all other benchmarks. Our
experiment is conducted on eight GPUs.


Regarding the models used in our experiments, We employed the Qwen3 (Yang et al., 2025a) and Llama3.2 (Grattafiori
et al., 2024) series of models. In detail, Qwen3-(1.7B/4B/8B)-Base denotes the base models, while Qwen3-(1.7B/4B/8B)
refer to the distilled variants obtained through strong model distillation from their corresponding base models. In addition,
Qwen3-4B-Instruct is a further fine-tuned version of Qwen3-4B, designed to better follow user instructions and generate
more accurate responses.


In the parameter design of HACPO, when evaluating model capabilities, we use the results from the most recent _K_ batches
to perform smoothing. In all experiments, we set _K_ = 5. For the clipping boundary _δ_ in the exponential importance
sampling of _α_, as well as the gradient clipping step size _δ_ step, each experiment has slight variations. We provide the specific
settings used for each experiment in the Table 5. A commonly used set of parameters is _α_ = 1, _δ_ = 0 _._ 8, and _δ_ step = 0 _._ 025.


_Table 5._ The Details of Hyperparameter


Model Combination _α_ _δ_ _δstep_


qwen3-4B + qwen3-4B-Instruct 3.0 0.8 0.01
qwen3-1.7B-Base + qwen3-4B-Base 1.0 0.8 0.025
qwen3-4B-Base + qwen3-8B-Base 3.0 0.8 0.025
llama3.2-1B-Instruct + llama3.2-3B-Instruct 1.0 0.9 0.01
qwen3-1.7B-Base + llama3.2-1B-Instruct 1.0 0.8 0.025
qwen3-4B-Base + llama3.2-3B-Instruct 1.0 0.8 0.025


**B. Additional Related Work**


**B.1. Reinforcement Learning From Verifiable Rewards**


GRPO is one of the main algorithms used in Reinforcement Learning From Verifiable Rewards, and (Yang et al., 2026a)
provides a principled theoretical analysis of group-based advantage estimation. The primary modification of GRPO(Shao
et al., 2024) involves the formation of a set of responses generated from the same prompt, within which the advantage for
each response is computed. This approach eliminates the need for a critic network, thereby significantly reducing both
memory and computational overhead. Several variants of GRPO (Yu et al., 2025; Yang et al., 2025b; Zhao et al., 2025b;
Wang et al., 2025; Huang et al., 2026a; Liu et al., 2026; Huang et al., 2026b) have been proposed to address issues in GRPO,
the most related one is GSPO(Zheng et al., 2025), which improve the performance and generalization of GRPO.


GSPO replaces the token-level importance sampling ratio in GRPO with a sequence-level ratio. GSPO demonstrates greater
suitability than GRPO for fine-tuning Mixture-of-Experts (MoE) models. During inference, MoE models dynamically
activate different expert networks(Cai et al., 2025a). When employing GRPO, if the current policy and the sampling policy
activate different experts for a given token, the importance sampling weight for that token can become an outlier, leading to
training instability. In contrast, GSPO averages the importance sampling ratio across all tokens within the response, thereby
significantly enhancing stability. Importance sampling essentially acts as a weighting mechanism to diminish the gradient


13


**Heterogeneous Agent Collaborative Reinforcement Learning**


contributions from samples that deviate substantially from the current policy’s distribution. The sequence-level importance
sampling employed by GSPO proves particularly effective for MoE models with varying expert networks. This success
inspires a broader consideration of measuring the deviation between a sample from other models and the current policy
distribution.


In addition to the methods discussed above, a wide range of advanced techniques have been proposed in recent years
to address various challenges in representation learning, model optimization, and generative modeling. These include
progress in interpretable representation learning (Li et al., 2025a), prompt-based structural modeling (Li et al., 2025c),
diffusion-driven restoration (Li et al., 2025b), efficient transformer architectures for visual modeling (Fu et al., 2022),
prompt-guided sequence modeling (Cai et al., 2023; 2024), parameter-efficient tuning strategies (Cai et al., 2025b), as well
as novel normalization mechanisms for improving model stability (Cai et al., 2025c). Although these works are designed for
different task scenarios, they collectively enrich the toolkit of modern machine learning research and provide useful insights
for understanding the generalization and optimization of neural models.


Traditional RLVR methods like GRPO and GSPO optimize agents independently, often leading to costly on-policy
sampling and underutilized intermediate rollouts. **HACPO** builds upon these group-based paradigms by enabling
cross-agent rollout sharing. It maximizes sample utilization by allowing each rollout in an _n_ -agent system to be
leveraged up to _n_ times, directly addressing the efficiency bottlenecks of isolated RLVR training.


**B.2. Multi-Agent Reinforcement Learning (MARL)**


Multi-Agent Reinforcement Learning (MARL) represents a paradigm in Reinforcement Learning (RL), where multiple
agents evolve collectively (Lowe et al., 2017; Kuba et al., 2021; Yu et al., 2022; Zhong et al., 2024; Rashid et al., 2020;
Foerster et al., 2018). MARL has gradually been applied to LLM-based agent scenarios. Most works in MARL focus on
employing multiple agents to build a comprehensive system, where the agents collaborate to accomplish tasks (Liao et al.,
2025a; Park et al., 2025; Wan et al., 2025; Liu et al., 2025; Li et al., 2023; Du et al., 2023). These works primarily focus
on constructing a holistic system in which agents collaborate to accomplish tasks. In contrast, our work targets scenarios
in which multiple agents are required to perform tasks independently. Although these works address different settings
compared to ours, they still provide valuable inspiration: even when using only the output text as an input prompt, different
models can learn from each other. The model’s sampling not only includes the generated text but also the corresponding
probability distribution information. By directly utilizing these samples for policy updates, rather than as inputs, the model
can more effectively learn the knowledge of other models.


Several works have used MARL frameworks to fine-tune models. For example, in COPY(Ma et al., 2024), two copies of the
same model are assigned as the pioneer and the observer, respectively, with the input of the pioneer serving as the output
of the observer. The roles are then exchanged to further facilitate knowledge transfer. However, homogeneous models
struggle to transcend their intrinsic performance ceilings(Madaan et al., 2025). Besides, such fine-tuning approaches require
numerous sampling iterations, leading to low utilization efficiency. Furthermore, using the same model makes it difficult to
inject knowledge beyond the model’s intrinsic capabilities.


While MARL typically focuses on collaborative execution where multiple agents coordinate to solve a task jointly,
**HACPO** introduces a distinct paradigm: independent execution with collaborative optimization. By facilitating
mutual knowledge transfer during training while ensuring agents act independently at inference, HACPO bridges the
gap between collective learning benefits and the practical need for autonomous agent operation.


**B.3. Knowledge Distillation (KD)**


Knowledge Distillation (KD) is a widely adopted technique in the field of Large Language Models (LLMs), where a
high-capacity teacher model is utilized to guide the training of a more compact student model (Hinton et al., 2015; Gou
et al., 2021; Sanh et al., 2019). The core mechanism involves the teacher conveying not just its final predictions but its
nuanced output distribution (dark knowledge), enabling the student to mimic the teacher’s internal logic and probabilistic
insights (Hinton et al., 2015; Romero, 2014).


Beyond traditional static methods, recent advancements have transitioned the distillation process from offline to online and
on-policy settings (Anil et al., 2018; Agarwal et al., 2024a; Gou et al., 2021; Agarwal et al., 2024b; Huang et al., 2025;


14


**Heterogeneous Agent Collaborative Reinforcement Learning**


Zhao et al., 2025a). These approaches allow for the dynamic transfer of knowledge, often leveraging the student’s own
generated trajectories to bridge the distribution gap between models. In the context of LLMs, distillation has also evolved
into Black-box Distillation, where students learn from the teacher’s generated responses or chain-of-thought rationales when
model weights are inaccessible (Hsieh et al., 2023; Ho et al., 2023). The distinction between distillation and our approach
lies in the fact that, in our method, there are no ”teacher” or ”student” models; instead, all models can learn from each
other simultaneously. Furthermore, our approach enables models to engage in both self-exploration and learning from other
models concurrently.


Standard Knowledge Distillation (KD) relies on a fixed, one-way path where a student mimics a stronger teacher,
potentially limiting the system’s ceiling. **HACPO** transcends this by treating heterogeneous agents as peer co-learners.
Through Agent-Capability-Aware Advantage Estimation and bidirectional transfer, it allows even weaker models
to contribute unique exploration trajectories, facilitating a mutual performance boost that self-learning or one-way
distillation cannot achieve.


**C. Heterogeneous Agent Importance Sampling Analysis**


In the reinforcement learning paradigm, importance sampling is commonly used to stabilize updates, often through a
clipping mechanism. The clipping range typically centers around 1.0. For instance, in GSPO, the upper and lower bounds
for clipping are set to 1.0004 and 0.9997, respectively. However, in a multi-agent setting, the importance sampling values
for samples from other agents do not exhibit the same pattern and fluctuate as training progresses.


In the experiment involving Qwen3-1.7B-Base and Qwen3-4B-Base, we distinguish between self-generated responses and
cross-agent responses, denoted as _s_ [homo] and _s_ [hete], respectively. These values represent the average importance sampling
across each training step. It is important to note that while _s_ [homo] remains stable and tends to stay around 1 throughout
training, _s_ [hete] does not follow a fixed range and fluctuates as training progresses. The results are shown in Table 6


_Table 6._ _s_ _[homo]_ and _s_ _[hete]_ of Qwen3-1.7B-Base in all steps


Model mean max min range


_s_ _[homo]_ 1.00002 1.00020 0.99960 0.00060
_s_ _[hete]_ 0.89550 0.93615 0.86198 0.07417


For self-generated responses, as the number of updates(mini batches) within a batch increases, the discrepancy between
the sampling policy _π_ old( _θ_ ) and the current policy _π_ ( _θ_ ) grows, leading to an increased _s_ [homo] and a higher ratio of clipped
tokens. However, for cross-agent responses, the discrepancy between the current policy _π_ [(] _[k]_ [)] ( _θ_ ) and the sampling model’s
policy _π_ old [(] _[j]_ [)][(] _[θ]_ [)][ fluctuates unpredictably, leading to a variable] _[ s]_ [hete][ and the ratio of clipped tokens.]


In a batch with multiple mini-batches, as the number of updates increases, self-generated responses become more heavily
clipped in later mini-batches due to the growing discrepancy between the current and old policies. Therefore, the influence
of cross-agent responses is likely to increase in later mini-batches, as their importance sampling values are less predictable,
leading to an instability if they dominate the update.


**D. Theoretical Analysis**


**D.1. Proof of the Unbiasedness of the Advantage Estimator**


In this section, we formally establish that the Agent-Capability-Aware advantage estimator introduced in HACPO provides
an unbiased estimation of the baseline, equivalent in expectation to the standard single-agent baseline.

**Assumption** **D.1** (Ideal Capability Ratio) **.** While the practical algorithm estimates _ωt_ [(] _[k,j]_ [)] using a moving average that
includes the current batch to strictly track non-stationary policy changes, we assume that the capability ratio _ω_ [(] _[k,j]_ [)] is an
estimator of the true performance ratio that is statistically independent of the specific stochastic realization of rewards in the
current batch.



E _{yt,i_ ( _j_ ) _[}]_ _i_ _[G]_ =1 _[∼][π][θ]_ _j_




- _ω_ [(] _[k,j]_ [)] _· R_ ( _yt,i_ [(] _[j]_ [)][)] = E _{yt,i_ ( _k_ ) _[}]_ _i_ _[G]_ =1 _[∼][π][θ]_ _k_


15




- _R_ ( _yt,i_ [(] _[k]_ [)][)] (16)


**Heterogeneous Agent Collaborative Reinforcement Learning**


_Remark_ D.2 _._ Justification: As the sliding window size _K_ increases, the contribution of the current batch to _ω_ diminishes
( _O_ (1 _/K_ )), thereby asymptotically satisfying the independence assumption. However, excessively large _K_ introduces
estimation bias due to the non-stationarity of evolving policies. In practice, we select a finite _K_ as a necessary tradeoff: sufficiently large to approximate independence, yet responsive enough to track dynamic capability changes without
significant lag.


**Theorem D.3** (Unbiasedness of Coupled Baseline) **.** _Consider a set of heterogeneous agents._ _The expected value of the_
_capability-aware baseline_ _µ_ ˆ [(] _[k]_ [)] _computed using samples from multiple agents is equivalent to the expected reward of agent k_
_computed solely from its own samples._




 -  E _µ_ [(] _t_ _[k]_ [)] = E _{yt,i_ ( _k_ ) _[}]_ _i_ _[G]_ =1 _[∼][π][θ]_ _k_




- _R_ ( _yt,i_ [(] _[k]_ [)][)] (17)



_Proof._ Without loss of generality, consider the case of two agents, _k_ = 1 and _j_ = 2. The capability-aware baseline for agent
1 is given by:



_G_

- _R_ ( _yt,i_ [(2)][)] _[.]_ (18)

_i_ =1



_µ_ [(1)] _t_ = 2 [1] _G_



_G_





- _R_ ( _yt,i_ [(1)][) +] _[ω]_ [(1] _[,]_ [2)]

2 _G_

_i_ =1



2 _G_



Taking the expectation with respect to the policies _πθ_ 1 and _πθ_ 2:




- _R_ ( _yt,i_ [(1)][) +] _[ω]_ [(1] _[,]_ [2)]

2 _G_

_i_ =1



2 _G_







(19)



_G_





- _R_ ( _yt,i_ [(2)][)]

_i_ =1



E[ _µ_ [(1)] _t_ [] =][ E] _{yt,i_ [(1)] _[}∼][π][θ]_ 1 _[,][{][y]_ _t,i_ [(2)] _[}∼][π][θ]_ 2




1

2 _G_



_G_




2 [1] [E] _[y]_ _t,i_ [(1)] _[∼][π][θ]_ 1 [[] _[R]_ [(] _[y]_ _t,i_ [(1)][)] +] _[ω]_ [(1] 2 _[,]_ [2)]



= [1]



2 E _yt,i_ (2) _[∼][π][θ]_ 2 [[] _[R]_ [(] _[y]_ _t,i_ [(2)][)]] _[.]_ (20)



Invoking Assumption D.1, we treat _ω_ [(1] _[,]_ [2)] as independent of the current batch’s reward realization _R_ ( _y_ [(2)] ). This allows us
to factorize the expectation:



E[ _µ_ [(1)] _t_ [] =] [1]




[1] 2 [E] _[y]_ _t,i_ [(1)] _[∼][π][θ]_ 1 [[] _[R]_ [(] _[y]_ _t,i_ [(1)][)] +] [1] 2



2 [E] _[y]_ _t,i_ [(1)] _[∼][π][θ]_ 1 [[] _[R]_ [(] _[y]_ _t,i_ [(1)][)]]



_t,i_ 1 _t,i_ 1 (21)

= E _yt,i_ (1) _[∼][π][θ]_ 1 [[] _[R]_ [(] _[y]_ _t,i_ [(1)][)]] _[.]_



Thus, we can obtain the Theorem D.3.


**Proof of Corollary 4.2.**


_Proof._ By linearity of expectation and the definition in (15),


                   -                   -                   -                   - ��                   -                   E _A_ [(] _t,i_ _[k]_ [)] = E _R_ _yt,i_ [(] _[k]_ [)] _−_ E _µ_ [(] _t_ _[k]_ [)] _._


                -                - ��
Since _yt,i_ [(] _[k]_ [)] _[∼]_ _[π][θ]_ _k_ [(] _[·]_ _[|]_ _[q][t]_ [)][, we have][ E] _R_ _yt,i_ [(] _[k]_ [)] = E _y∼πθk_ ( _·|qt_ )[ _R_ ( _y_ )] _._ Applying Theorem 4.1 yields E[ _A_ [(] _t,i_ _[k]_ [)][]] [=] [0][, which]
proves the claim.


**D.2. Gradient Analaysis**


For notational convenience, define the reference direction



**v** := E _x∼D,_ _y∼πθk_




- 1 _A_ ˆ [(] _[k]_ [)] ( _x, y_ ) _∇θk_ log _πθk_ ( _y_ _| x_ ) _,_ (22)
_|y|_



where _A_ [ˆ][(] _[k]_ [)] ( _x, y_ ) denotes the advantage signal used to update agent _k_ .


The homogeneous objective _J_ homo [(] _[k]_ [)] [coincides with the GSPO objective (][Zheng et al.][,][ 2025][).] [As a consequence, its gradient]
satisfies:
_∇θk_ _J_ homo [(] _[k]_ [)] _[≈]_ **[v]** (23)


16


**Heterogeneous Agent Collaborative Reinforcement Learning**


For the heterogeneous objective _J_ hete [(] _[k]_ [)] [, HACPO incorporates cross-agent responses through importance weighting, clipping,]
and capability-aware scaling. Using the Importance Sampling Lemma (Lemma D.10) and the non-negativity of the effective
reweighting terms, we show that the heterogeneous gradient admits the same reference direction:

                 - _∇θk_ _J_ hete [(] _[k]_ [)] _[,]_ **[v]**                 - _>_ 0 _._ (24)


We analyze the gradients of the HACPO objective, decomposing it into self-generated ( _Jhomo_ ) and cross-agent ( _Jhete_ )
components.


**Definition D.4** (Sequence-Level Importance Sampling) **.** The sequence level importance sampling ratio is defined as:




- - _|y|_
_t_ =1 _[π][θ]_ [(] _[y][i,t][|][x, y][<t]_ [)]

 - _|y|_
_t_ =1 _[π][θ]_ _old_ [(] _[y][i,t][|][x, y][<t]_ [)]



_si_ ( _θ_ ) =




- _|y_ [1] _|_
_._ (25)



D.2.1. HOMOGENEOUS GRADIENT


For the homogeneous component _Jhomo_, the gradient derivation follows the standard GSPO formulation.


**Proposition D.5.** _The gradient of the homogeneous objective is given by:_




- _si_ ( _θ_ ) _A_ [ˆ] _i ·_ [1]

_|y_

_i_ =1



_|yi|_







 _._ (26)



_|y|_




_∇θJhomo_ = E _yi∼πθold_ (1)





 [1]

_G_



_G_




_∇θ_ log _πθ_ ( _yi,t|x, y<t_ )

_t_ =1



_Proof._ Starting from the objective _JGSP O_ = E _y∼πold_ [ _si_ ( _θ_ ) _A_ [ˆ] _i_ ], we apply the log-derivative trick:







_πθ_ ( _yi,t|x, y<t_ )

_t_ =1






log



















 _−_ log







_∇θs_ ( _θ_ ) = _∇θ_ exp





 [1]

_|y|_



_|y|_








_|y|_




_πθold_ ( _yi,t|x, y<t_ )

_t_ =1







 (27)



= _s_ ( _θ_ ) _·_ [1]

_|y|_



_|y|_

- _∇θ_ log _πθ_ ( _yi,t|x, y<t_ ) _._ (28)


_t_ =1



Substituting this into the gradient of the expectation yields the result.


D.2.2. HETEROGENEOUS GRADIENT


For the heterogeneous component, we consider agent 1 learning from agent 2. The objective utilizes the exponential
importance sampling weight.


**Proposition D.6.** _The gradient of the heterogeneous objective Jhete with respect to θ_ 1 _is:_



_∇θ_ 1 log _πθ_ 1( _yi,t|x, y<t_ )
_t_ =1







 _._ (29)



_∇θ_ 1 _Jhete_ = E _yi∼πθold_ (2)





 _ω_ [(2] _[,]_ [1)] _· sg_ - _s_ _[hete]_ _i_ ( _θ_ 1 _, θ_ 2)� _α_ +1 _A_ ˆ _i ·_ _|y_ 1 _|_



_|y|_





        - _πθ_ [(1)] 1 [(] _[y][i]_ [)]
_Proof._ Let _s_ _[hete]_ _i_ ( _θ_ 1 _, θ_ 2) = _πθ_ [(2)] 2 _old_ [(] _[y][i]_ [)]




- _|y_ [1] _|_
. The objective is defined as:



_Jhete_ = E _y∼πold_ (2)




- _ω_ [(2] _[,]_ [1)] _·_ sg( _s_ _[hete]_ ) _[α]_ _· s_ _[hete]_ _·_ _A_ [ˆ] _._ (30)



Noting that sg[ _·_ ] denotes the stop-gradient operator and _πold_ [(2)] [is] [independent] [of] _[θ]_ [1][,] [the] [gradient] [acts] [only] [on] [the] [term]
_s_ _[hete]_ _i_ ( _θ_ 1 _, θ_ 2). Using the derivative property derived in Proof D.2.1, _∇θ_ 1 _s_ _[hete]_ _i_ ( _θ_ 1 _, θ_ 2) = _s_ _[hete]_ _i_ ( _θ_ 1 _, θ_ 2) _|y_ [1] _|_ _[∇][θ]_ [1] [log] _[ π]_ _θ_ [(1)] 1 [(] _[y][i]_ [)][.]

Substituting this yields the proposition.


17


**Heterogeneous Agent Collaborative Reinforcement Learning**


**D.3. Proof of the Effectiveness of HACPO**


In this section, we formally establish the effectiveness of HACPO by demonstrating that the heterogeneous objective _Jhete_
provides an optimization direction consistent with the homogeneous objective _Jhomo_ . Specifically, we prove that the
gradient of _Jhete_ with respect to the policy parameters is aligned with the gradient of the log-likelihood of the optimal
policy.


**Assumption D.7.** (Importance Sampling Approximation). We assume that the sequence-level importance sampling ratio
_si_ ( _θ_ ) for the learner’s self-generated responses remains approximately unity during the gradient update step. That is, we
approximate:




   - _πθ_ ( _yi_ )
_si_ ( _θ_ ) =
_πθold_ ( _yi_ )



1

- _|yi|_
_≈_ 1 (31)



_Remark_ D.8 _._ Unlike standard token-level importance sampling, which suffers from high variance due to the product of
probabilities, our method is based on GSPO (Zheng et al., 2025), which employs sequence-level length normalization
(geometric mean). This normalization effectively counteracts the cumulative divergence of probability ratios, constraining
the value of _si_ ( _θ_ ) to a stable range centered at 1.0.


**Definition D.9.** With Assumption D.7, we can only focus on the discrepancy between _πθ_ 1 and _πθ_ 2. For succinctness, let
_P_ ( _y_ ) and _Q_ ( _y_ ) denote the sequence-level likelihood probabilities of a response _y_ generated by the current policy of Agent 1
( _πθ_ 1) and Agent 2 ( _πθ_ 2), respectively:



_|y|_

- _πθ_ 2( _yt_ _| x, y<t_ ) _._ (32)


_t_ =1



_P_ ( _y_ ) =



_|y|_

- _πθ_ 1( _yt_ _| x, y<t_ ) _,_ _Q_ ( _y_ ) =


_t_ =1



Recall from Assumption D.7 and Section D.2.1 that the gradient of the homogeneous objective satisfies the alignment
condition:



_∇θ_ 1 _Jhomo_ _≈_ E _y∼P_




- _A_ ˆ [1] (33)

_|y|_ _[∇][θ]_ [1][ log] _[ P]_ [(] _[y]_ [)]



To prove the effectiveness of _Jhete_, it suffices to show that _∇θ_ 1 _Jhete_ shares this orientation.


**Lemma D.10.** _For two probability distributions P_ ( _y_ ) _and Q_ ( _y_ ) _, the following equality holds:_



E _y∼Q_




- _P_ ( _y_ ) = E _y∼P_ [ _f_ ( _y_ )] _._
_Q_ ( _y_ ) _[f]_ [(] _[y]_ [)]



Using the importance sampling lemma in Lemma D.10, we present the following theorem regarding the alignment of the
heterogeneous gradient.


**Theorem** **D.11.** _The_ _gradient_ _of_ _the_ _heterogeneous_ _objective_ _∇θ_ 1 _Jhete_ _has_ _a_ _positive_ _angle_ _with_ _the_ _gradient_ _of_ _the_
_homogeneous objective ∇θ_ 1 _Jhomo._ _That is:_


_⟨∇θ_ 1 _Jhete, ∇θ_ 1 _Jhomo⟩_ _>_ 0 _._ (34)


_Proof._ The heterogeneous objective is defined as an expectation over samples _y_ drawn from Agent 2 ( _y_ _∼_ _Q_ ):


_Jhete_ = E _y∼Q_                   - _ω_ [(2] _[,]_ [1)] _sg_ [ _s_ _[hete]_ _i_ ] _[α]_ _A_ [ˆ] _is_ _[hete]_ _i_                   - _._ (35)


We replace the corresponding term in Equation (29) with _P_ ( _y_ ) and _Q_ ( _y_ ) defined in Definition D.9, and then apply Lemma
D.10:




- _[α]_ _|_ [+1] _y|_
1

_·_ _A_ [ˆ] _i_ _|y|_ _[∇][θ]_ [1][ log] _[ P]_ [(] _[y]_ [)]







_∇θ_ 1 _J_ hete( _θ_ 1 _, θ_ 2) = E _y∼Q_


= E _y∼Q_




- - _P_ ( _y_ )

_ω_ [(2] _[,]_ [1)]
_Q_ ( _y_ )



��
_P_ ( _y_ )

_Q_ ( _y_ )



(36)





- - _P_ ( _y_ )

_· ω_ [(2] _[,]_ [1)]
_Q_ ( _y_ )


18




- _[α]_ _|_ [+1] _y|_ _[−]_ [1]
1

_·_ _A_ [ˆ] _i_ _|y|_ _[∇][θ]_ [1][ log] _[ P]_ [(] _[y]_ [)]


**Heterogeneous Agent Collaborative Reinforcement Learning**


Using the identity E _y∼Q_ [ _Q_ _[P]_ [ (] ( _[y]_ _y_ [)] ) _[f]_ [(] _[y]_ [)] =][ E] _[y][∼][P]_ [ [] _[f]_ [(] _[y]_ [)]][:]










(37)




_∇θ_ 1 _Jhete_ ( _θ_ 1 _, θ_ 2) = E _y∼Q_


= E _y∼P_



_P_ ( _y_ ) - _P_ ( _y_ )
_Q_ ( _y_ ) _[·][ ω]_ [(2] _[,]_ [1)] _Q_ ( _y_ )







_ω_ (2 _,_ 1) - _P_ ( _y_ )
_Q_ ( _y_ )





  -  - _[α]_ _|_ [+1] _y|_ _[−]_ [1]
_P_ ( _y_ ) 1

[(2] _[,]_ [1)] _·_ _A_ [ˆ] _i_
_Q_ ( _y_ ) _|y|_ _[∇][θ]_ [1][ log] _[ P]_ [(] _[y]_ [)]


- �� _f_ ( _y_ )




- _[α]_ _|_ [+1] _y|_ _[−]_ [1]



1
_·A_ [ˆ] _i_ _|y|_ _[∇][θ]_ [1][ log] _[ P]_ [(] _[y]_ [)]






_._ (38)





                      - ��                       _C_ ( _y_ )


For succinctness, let _g_ ( _y_ ) = _A_ [ˆ] _i_ _|y_ [1] _|_ _[∇][θ]_ [1] [log] _[ P]_ [(] _[y]_ [)][:]


_∇θ_ 1 _Jhete_ ( _θ_ 1 _, θ_ 2) = E _y∼P_ [ _C_ ( _y_ ) _· g_ ( _y_ )] (39)

= E _y∼P_ [ _C_ ( _y_ )] _·_ E _y∼P_ [ _g_ ( _y_ )] + _Cov_ ( _C_ ( _y_ ) _, g_ ( _y_ ))


Let define a constant vector **v** as:
**v** := E _y∼P_ [ _g_ ( _y_ )] _,_ _∇θ_ 1 _Jhomo_ _≈_ **v** (40)


To prove that the heterogeneous update provides a valid optimization direction, we analyze the inner product between the
two gradients. Let _I_ = _⟨∇θ_ 1 _Jhete, ∇θ_ 1 _Jhomo⟩_ .


_I_ _≈⟨_ E _y∼P_ [ _C_ ( _y_ )] _·_ **v** + Cov( _C_ ( _y_ ) _, g_ ( _y_ )) _,_ **v** _⟩_



= E _y∼P_ [ _C_ ( _y_ )] _· ⟨_ **v** _,_ **v** _⟩_ + _⟨_ Cov( _C_ ( _y_ ) _, g_ ( _y_ )) _,_ **v** _⟩_

= E _y∼P_ [ _C_ ( _y_ )] _· ∥_ **v** _∥_ [2] + Cov( _C_ ( _y_ ) _, ⟨g_ ( _y_ ) _,_ **v** _⟩_ )



(41)



Let _Z_ ( _y_ ) = _⟨g_ ( _y_ ) _,_ **v** _⟩_ be a scalar random variable representing the alignment between the single-sample gradient _g_ ( _y_ ) and
the expected homogeneous gradient direction **v** . Substituting this into Equation (44), we obtain:


_I_ = E _y∼P_ [ _C_ ( _y_ )] _· ∥_ **v** _∥_ [2] + Cov( _C_ ( _y_ ) _, Z_ ( _y_ )) (42)


For the heterogeneous update to provide a valid optimization direction (i.e., _I_ _>_ 0), the weighting coefficient _C_ ( _y_ ) must
satisfy the following condition:


Cov( _C_ ( _y_ ) _, Z_ ( _y_ )) _> −_ E _y∼P_ [ _C_ ( _y_ )] _· ∥_ **v** _∥_ [2] (43)


Let _ρC,Z_ be the correlation coefficient between _C_ ( _y_ ) and _Z_ ( _y_ ), and let _σC, σZ_ denote their respective standard deviations.
The condition for positive alignment (Eq. 43) can be rewritten as:


_ρC,Z_ _· σC_ _· σZ_ _> −_ E[ _C_ ( _y_ )] _· ∥_ **v** _∥_ [2] (44)



It is worth to notion that:



_C_ ( _y_ ) _≈_ _ω_ [(2] _[,]_ [1)] _[ Q]_ [(] _[y]_ [)] (45)

_P_ ( _y_ ) _[,]_



because that _α_ + 1 is far less than _|y|_, therefor _[α]_ _|_ [+1] _y|_ _[−]_ [1] _[ ≈−]_ [1][.]


To guarantee the satisfaction of the condition in Eq. 44, we introduce a mild assumption regarding the collaborative nature
of the heterogeneous agents.


**Assumption D.12** (Positive Competence Alignment) **.** We assume that the Agent 2 is a competent collaborator, meaning
its confidence is positively correlated with the response quality. Mathematically, the correlation coefficient between the
weighting coefficient _C_ ( _y_ ) and the gradient alignment _Z_ ( _y_ ) is positive:


_ρC,Z_ _>_ 0 _._ (46)


19


**Heterogeneous Agent Collaborative Reinforcement Learning**


_Remark_ D.13 (Physical Interpretation) _._ The assumption _ρC,Z_ _>_ 0 essentially posits that the sampler (Agent 2) acts as a
competent collaborator rather than an adversary. A high weight _C_ ( _y_ ) indicates the sampler’s superior confidence relative
to the learner, while a high _Z_ ( _y_ ) indicates a high-quality response. The positive correlation implies that the sampler’s
confidence is generally aligned with the ground-truth reward signal, thereby facilitating effective knowledge transfer.


The coefficient term (Equation _C_ ( _y_ )) is strictly positive for all valid trajectories because the capability ratio _ω_ [(2] _[,]_ [1)] _>_ 0, and
the probability ratio is non-negative. Thus, the condition in Eq. 44 will be satisfied.


This confirms that the optimization direction of _Jhete_ is consistent with that of _Jhomo_, ensuring that cross-agent responses
effectively contribute to the improvement of Agent 1.


**E. Formulation and Pseudocode of HACPO**


To facilitate a precise understanding of HACPO, we present the complete algorithmic formulation and training procedure.


Taking two agents (1 and 2) as an example. The optimization objective for agent 1 consists of two terms: the loss computed
from its own samples, _J_ homo( _θ_ ), and the loss computed from samples of other agents, _J_ hete( _θ_ ). The final loss is the sum of
these two terms. Similarly, agent 2 is updated using a loss function of the same form, but with different values.



_J_ homo [(1)] [=] [1]

_G_



_G_



_i_ =1




- - - �� min _s_ [(1] _t,i_ _[,]_ [1)] _,_ clip _s_ [(1] _t,i_ _[,]_ [2)] _· A_ [(1)] _t,i_ (47)



1

- _|yi|_
(48)



_s_ [(1] _t,i_ _[,]_ [1)] =




_πθ_ [(1)][(] _[y][i]_ [)]

_πθ_ [(1)] old [(] _[y][i]_ [)]



_clip_ ( _s_ [(1] _t,i_ _[,]_ [1)] ) = clip( _s_ [(1] _t,i_ _[,]_ [1)] _,_ 1 _−_ _ϵl,_ 1 + _ϵh_ ) (49)



1
_J_ hete [(1)] [=]
_G_



_G_

- �clip� _s_ [(1] _t,i_ _[,]_ [2)] - sg� _s_ [(1] _t,i_ _[,]_ [2)] - _α_ _ωt_ [(2] _[,]_ [1)] _· A_ [(1)] _t,i_ - _,_ (50)

_i_ =1



1

- _|yi|_
(51)



_s_ [(1] _t,i_ _[,]_ [2)] =




_πθ_ [(1)][(] _[y][i]_ [)]

_πθ_ [(2)] old [(] _[y][i]_ [)]



_clip_ ( _s_ [(1] _t,i_ _[,]_ [2)] ) = clip( _s_ [(1] _t,i_ _[,]_ [2)] _,_ 1 _._ 0 _−_ _δ_ + _k · δ_ step _,_ 1 _._ 0) (52)


_J_ = _J_ homo + _J_ hete (53)


In the Equation 50, ˜ _s_ [(1] _t,i_ _[,]_ [2)] and _A_ [˜][(1)] _t,i_ [are unfolded as mentioned in Section][ 3.2][ and][ 3.3][.]


**F. Additional Experimental Results**


Here, we present additional experiments in Table 7, including comparisons between Qwen3-4B-Base + Qwen3-8B-Base,
Llama3.2-1B-Instruct + Llama3.2-3B-Instruct, and Qwen3-1.7B-Base + Llama3.2-1B-Instruct.


20


**Heterogeneous Agent Collaborative Reinforcement Learning**


**Algorithm 1** Heterogeneous Agent Collaborative Policy Optimization


**Require:** n initial policy models _π_ init1 _, π_ init2 _, ...π_ init _n_, reward models _R_, task prompts _D_, each prompt has G outputs

1: **for** i = 1 to n **do**
2: policy model _πθi_ _←_ _π_ init _i_
3: **end for**
4: **for** step = 1 to _N_ **do**
5: Sample a batch _D_ batch from _D_
6: **for** i = 1 to n **do**
7: Update the old policy model _πθi_ old _←_ _πθi_
8: **end for**
9: **for** i = 1 to n **do**
10: Sample G output _o ∼_ _π_ old _i_ ( _· | q_ ) for each question _q_ _∈D_ batch
11: Compute rewards _rj_ for each output _oj_ in the batch
12: Compute accuracy for the sampling model
13: **end for**
14: **for** i = 1 to n **do**
15: Compute _Ai,o_ for the response in batch (agent i)
16: **for** mini batch = 1 to _k_ **do**
17: Update the policy model _πθi_ by maximizing the HACPO objective
18: **end for**
19: **end for**
20: **end for**
**Ensure:** _πθi|i_ = 1 _,_ 2 _, ..., n_


21


**Heterogeneous Agent Collaborative Reinforcement Learning**


_Table 7._ Additional Experimental Results


Model MATH-500 math gsm8k aime2025 AMC23 minerva olympiad AVG


Qwen3-4B-Base and Qwen3-8B-Base


4B-Base 0.61 0.676 0.445 0.1 0.4 0.308 0.347 0.412
4B-Base(GRPO) 0.796 0.788 0.885 **0.307** 0.475 0.349 0.454 0.579
4B-Base(GSPO) 0.782 0.787 0.877 0.25 0.525 **0.368** 0.46 0.578
4B-Base(GSPO _×_ 2) 0.756 0.794 0.873 0.208 0.55 0.382 0.463 0.575
4B-Base(Naive) 0.734 0.712 0.895 0.143 0.55 0.342 0.354 0.526
4b-Base(HACPO) **0.81** **0.803** **0.904** 0.275 **0.6** 0.364 **0.463** **0.614**
8B-Base 0.647 0.713 0.684 0.033 0.4 0.232 0.375 0.441
8B-Base(GRPO) 0.814 0.812 0.921 0.265 0.575 0.415 **0.479** 0.612
8b-Base(GSPO) 0.794 0.804 0.923 0.225 0.6 **0.426** 0.468 0.606
8b-Base(GSPO _×_ 2) 0.8 0.803 0.92 0.2 0.575 0.404 0.46 0.595
8b-Base(Naive) 0.79 0.783 0.921 0.252 0.5 0.408 0.429 0.583
8B-base(HACPO) **0.828** **0.813** **0.933** **0.323** **0.625** 0.423 0.467 **0.63**


Llama3.2-1B-Instruct and Llama3.2-3B-Instruct


llama3.2-1B 0.176 0.297 0.489 0 0.15 0.052 0.061 0.18
llama3.2-1B(GRPO) 0.35 0.349 0.569 0 0.125 0.008 0.097 0.214
llama3.2-1B(GSPO) **0.356** 0.346 0.523 0.021 0.125 0.066 0.088 0.218
llama3.2-1B(GSPO _×_ 2) 0.352 0.349 **0.573** 0.07 0.125 0.079 **0.103** 0.227
llama3.2-1B(Naive) 0.284 0.302 0.45 0.0 0.025 0.066 0.073 0.171
llama3.2-1B(HACPO) 0.35 **0.352** 0.541 **0.022** **0.2** **0.081** 0.085 **0.233**
llama3.2-3B 0.267 0.441 0.788 0.0 0.2 0.169 0.158 0.289
llama3.2-3B(GRPO) 0.502 0.507 0.814 0.0 0.25 0.199 0.174 0.349
llama3.2-3B(GSPO) 0.512 0.501 0.812 0.054 0.225 0.184 0.17 0.351
llama3.2-3B (GSPO _×_ 2) 0.488 0.498 **0.829** 0.0 0.175 0.188 0.159 0.334
llama3.2-3B(Naive) 0.406 0.407 0.734 0.0 0.225 0.177 0.107 0.294
llama3.2-3B(HACPO) **0.522** **0.51** 0.828 **0.067** **0.275** **0.199** **0.188** **0.37**


Qwen3-1.7B-Base and Llama3.2-1B-Instruct


qwen3-1.7B 0.5 0.483 0.616 0.033 0.3 0.206 0.229 0.338
qwen3-1.7B(GRPO) **0.682** 0.652 0.824 0.16 0.375 0.272 0.298 0.466
qwen3-1.7B(GSPO) 0.648 0.641 0.826 0.148 0.45 0.272 0.287 0.467
qwen3-1.7B(GSPO _×_ 2) 0.664 0.65 0.829 0.177 0.375 0.265 0.293 0.475
qwen3-1.7B(Naive) 0.59 0.596 0.798 0.105 0.3 0.221 0.241 0.407
qwen3-1.7B(HACPO) 0.676 **0.661** **0.838** **0.22** **0.45** **0.305** **0.32** **0.496**
llama3.2-1B 0.176 0.297 0.489 0.033 0.15 0.052 0.061 0.18
llama3.2-1B(GRPO) 0.35 0.349 **0.569** 0 0.125 0.008 0.097 0.214
llama3.2-1B(GSPO) 0.356 0.346 0.523 0.021 0.125 0.066 0.088 0.218
llama3.2-1B(GSPO _×_ 2) 0.352 0.349 0.573 0.07 0.125 0.079 **0.103** 0.227
llama3.2-1B(Naive) 0.336 0.337 0.512 0.0 0.125 0.066 0.071 0.214
llama3.2-1B(HACPO) **0.356** **0.368** 0.533 **0.033** **0.15** **0.066** 0.091 **0.228**


22


