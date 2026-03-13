## **Collaborative Multi-Agent Test-Time Reinforcement Learning for Reasoning**

**Zhiyuan Hu** [1] _[,]_ [2][*] **Yunhai Hu** [3] **Juncheng Liu** [4] **Shuyue Stella Li** [5] **Yucheng Wang** [2] **Zhen Xu** [6]

**See-Kiong Ng** [2] **Anh Tuan Luu** [7] **Xinxing Xu** [4] **Bryan Hooi** [2] **Cynthia Breazeal** [1] **Hae Won Park** [1]

1 MIT 2 NUS 3 NYU 4 Microsoft 5 UW 6 Columbia 7 NTU



**Abstract**


Multi-agent systems have evolved into practical LLM-driven collaborators for many applications, gaining robustness from diversity
and cross-checking. However, multi-agent
RL (MARL) training is resource-intensive and
unstable: co-adapting teammates induce nonstationarity, and rewards are often sparse and
high-variance. Therefore, we introduce **Multi-**
**Agent** **Test-Time** **Reinforcement** **Learning**
**(MATTRL)**, a framework that injects structured textual experience into multi-agent deliberation at inference time. MATTRL forms
a multi-expert team of specialists for multiturn discussions, retrieves and integrates testtime experiences, and reaches consensus for
final decision-making. We also study credit
assignment for constructing a turn-level experience pool, then reinjecting it into the dialogue.
Across challenging benchmarks in medicine,
math, and education, MATTRL improves accuracy by an average of 3.67% over a multi-agent
baseline, and by 8.67% over comparable singleagent baselines. Ablation studies examine different credit-assignment schemes and provide a
detailed comparison of how they affect training
outcomes. MATTRL offers a stable, effective
and efficient path to distribution-shift-robust
multi-agent reasoning without tuning. Code
can be found here. [1]


**1** **Introduction**


Multi-agent systems have moved from early algorithmic prototypes to practical LLM-driven collaborators. Across math, coding, web interaction,
and analytical benchmarks, these multi-agent systems reliably outperform comparable single-agent
baselines, as diversity and cross-checking improve
robustness under distribution shift.
Recent works explore collaborative multi-agent
frameworks to enhance LLM agents’ capabilities.


*Zhiyuan Hu. Email: [hzycs@mit.edu](mailto:hzycs@mit.edu)
[1https://github.com/zhiyuanhubj/MATTRL](https://github.com/zhiyuanhubj/MATTRL)



For example, AutoGen (Wu et al., 2024) (orchestrated multi-agent dialogues with tool use and
human-in-the-loop), CAMEL (Li et al., 2023) (roleplaying with inception prompting), AgentVerse
(Chen et al., 2023) (an open platform for cooperative problem solving and social simulation), ChatDev (Qian et al., 2023) (specialized software agents
for design, coding, and testing), and MagenticOne (Fourney et al., 2024) (an orchestrator that
routes tasks among specialized agents for web/local
workflows). In parallel, the success of DeepSeekR1 (Guo et al., 2025) has catalyzed reinforcement learning (RL) as a post-training paradigm
for stronger reasoning. Efforts to extend RL to the
multi-agent setting include MAPoRL (Park et al.,
2025), which jointly optimizes multi-model discussions and final answers via RL, and ReMA
(Wan et al., 2025), which separates high-level metathinking from low-level reasoning into two agents
and trains them with GRPO.
However, MARL remains resource-intensive and
can erode general abilities when adapted to a single
domain. Training stability is also difficult to guarantee due to (i) non-stationarity from simultaneously evolving teammates, which shifts state and return distributions, and (ii) sparse, high-variance rewards. Hence, we propose Multi-Agent Test-Time
Reinforcement Learning (MATTRL), an adaptation
framework that injects test-time textual experience
into the collaborative process. Instead of updating
weights, MATTRL conditions behavior with structured experience, enabling rapid, distribution-shiftrobust adaptation to new tasks/domains without
harming original generality. Additionally, textual
experience provides richer turn-level signals about
collaboration quality and reasoning than scalar rewards alone. Textual experience mitigates key
MARL pain points by keeping policies fixed and
providing dense, stepwise experience at every turn.
The crucial components of MATTRL include
(1) various group-to-agent credit assignment strate


1


gies for experience selection, (2) construction of an
experience pool from test time examples, and (3)
integration of the experience pool into the multiagent collaborative process. MATTRL first instantiates a team of specialized agents. The agents
deliberate in multi-turn discussions, drawing on
relevant prior experience to aggregate evidence
and move toward agreement. The process terminates when agreement is reached or a predefined
turn limit is met. A designated coordinator agent
then summarizes the discussion, consolidates the
accumulated evidence, and outputs the final decision. To retrieve experience, each agent utterance
is first scored using both individual-performance
signals and a decayed terminal shared reward. For
constructing the experience pool, high-scoring utterances are distilled into textual experiences and
added to the pool for subsequent retrieval and integration. Experiments show that, on benchmarks
spanning medicine, math, and education, MATTRL boosts average performance by 3.67% over
the multi-agent framework and by 8.67% over comparable single-agent baselines. Furthermore, we
systematically explored multiple credit-assignment
schemes for group-credit attribution in experience
selection, ranging from naïve shared credit to difference rewards and Shapley-style approximations.
To summarize, our contributions focus on these
three perspectives:


  - We propose the first Multi-agent Test Time Reinforcement Learning framework, MATTRL,
leveraging textual experience to enhance the
multi-agent system.

  - We further validate the effect of different
credit assignments on experience construction
and the final decision.

  - Experiments conducted on medical, math and
education benchmarks achieve a new SOTA
performance based on MATTRL.


**2** **Related Work**


**LLM-based multi-agent collaboration.** Recent
advancements in LLM-based multi-agent systems
have emphasized scalable collaboration mechanisms for complex task-solving. Surveys (Tran
et al., 2025) outline key coordination strategies in
LLM-driven multi-agent systems, enabling groups
of agents to work collectively at scale. MacNet
(Qian et al., 2024) explores the benefits of continuously adding agents to enhance performance
in collaborative settings. Multi-agent systems uti


lizing LLMs also emerge as tools for enhancing
medical decision-making processes. MDAgents
(Kim et al., 2024) introduces adaptive collaboration
among LLMs to address gaps in clinical reasoning
and diagnostics. Multi-agent conversational framework, MAC(Chen et al., 2025) boost diagnostic
accuracy through interactive agent dialogues.


**Reinforcement** **learning** **for** **LLM** **reasoning.**
Reinforcement learning techniques have been increasingly applied to refine reasoning capabilities in large language models. Models such as
DeepSeek-R1 (Guo et al., 2025) demonstrate RL’s
potential to enhance LLM reasoning without relying on human-annotated data. Recent work
also systematize RL for reasoning-centric LLMs.
SimpleRL-Zoo (Zeng et al., 2025) conducts a
broad, controlled study of RL on open-base models, showing that careful reward formatting and
difficulty curation drive reliable gains across benchmarks. Understanding R1-Zero-Like Training (Liu
et al., 2025) disentangles base-model priors from
optimizer effects, identifies length-inducing biases in GRPO, and introduces a debiased variant
(Dr.GRPO) that yields strong math results with
lightweight recipes. Complementing these, Beyond
“Aha!” (Hu et al., 2025b) aligns meta-abilities explicitly, spanning deductive, inductive, and abductive skills, via automatically verifiable tasks and
targeted RL, achieving consistent improvements
over instruction-tuned baselines.


**Test-time adaptation and structured experience.**
Test-time adaptation methods allow LLMs to dynamically adjust to new domains during inference
without additional training. The Test-Time Learning (TTL) paradigm, such as TLM (Hu et al.,
2025a), adapts models using only unlabeled test
data to handle domain shifts effectively. Test-Time
Reinforcement Learning (TTRL) (Zuo et al., 2025)
converts test-time scaling signals into pseudorewards to train LLMs on unlabeled data, enabling
self-evolution and substantial gains. Study (Wang
et al., 2025) also evaluate LLM improvements from
structured experience using semantic games as
testbeds resistant to saturation.


**Credit assignment under collaboration.** Credit
assignment in multi-agent collaborations involving
LLMs tackles the challenge of fairly attributing
contributions in cooperative settings. LLM-based
methods reformulate credit assignment as pattern
recognition to achieve efficient and effective dis


2


tribution in Multi-agent system. Approaches like
Shapley-Coop (Hua et al., 2025) address emergent
cooperation in self-interested multi-agent systems
through value-based credit allocation. Frameworks
such as LLM-MCA (Nagpal et al., 2025) utilize
large language models for multi-agent credit assignment in reinforcement learning contexts. Systems
like CollabUIAgents (He et al.) advance multiagent learning by incorporating LLM-guided credit
re-assignment and synthetic preference data.


**3** **Methodology**


**3.1** **Multi-Expert Team Collaboration**


We study a general multi-agent decision-making
setting. Each instance provides: (i) a task record (or
user context) _X_, (ii) a coordinator agent LLMCoo,
(iii) an expert catalog _SP_ (a pool of specialist
agents with textual expertise descriptions), and (iv)
a callable test-time experience pool _E_ (Sec. 3.2).
At test time, LLMCoo optionally retrieves relevant
experiences to strengthen the current decision. The
expert-team consultation follows three stages with
a preset maximum of _R_ max discussion rounds. Our
hospital consultation experiments are a concrete
instantiation by interpreting _X_ as a patient record
and _SP_ as clinical departments.


**Stage** **I:** **Team** **formation.** Rather than letting
LLMs freely invent roles, we select an expert team
TEAM _⊆SP_ based on the task record _X_ using a
recruitment prompt (Appendix A.4) that conditions
on _X_ and each specialist’s expertise description:


TEAM _←_ LLMCoo( _X_ _, SP_ ) _._ (1)


Each specialist _s_ _∈_ TEAM maintains a roundindexed opinion set _Os_ [(] _[r]_ [)][(] _[X]_ [)] [and] [a] [convergence]
flag _fs_ _[c]_ _[∈{]_ [False] _[,]_ [ True] _[}]_ [ (initialized to][ False][).] [We]
denote the team union at round _r_ as

_O_ [(] _[r]_ [)] ( _X_ ) =   - _Os_ [(] _[r]_ [)][(] _[X]_ [)] _[.]_ (2)

_s∈_ TEAM


**Stage II: Consensus via experience-augmented**
**dialogue.** The team proceeds in synchronized
rounds _r_ = 0 _,_ 1 _, . . ., R_ max. In each round, each
non-converged specialist _s_ retrieves task-relevant
experiences and then issues a revised opinion.
We denote the retrieved experience set for _s_ as


ER _s_ _←_ Retrieve� _E_ ; _X_ _, u_ [(] _s_ _[r]_ [)]   - _,_ (3)


where _u_ [(] _s_ _[r]_ [)] is the current utterance/contextual query
formed by specialist _s_ at round _r_ . In our implementation, Retrieve( _·_ ) uses a shared encoder _f_ ( _·_ )



(Qwen3-Embedding-4B (Zhang et al., 2025)) and
a FAISS index (Douze et al., 2024) to select top_K_ entries by cosine similarity. Details are in Appendix A.7, B.9 and C.1.1. The retrieved entries
are appended to the prompt under a fixed template.
The specialist then updates its opinion conditioned on its previous state and retrieved evidence:


_Os_ [(] _[r]_ [)][(] _[X]_ [)] _[←]_ [LLM] _[s]_ - _X_ _,_ _Os_ [(] _[r][−]_ [1)] ( _X_ ) _,_ ER _s_ - _._ (4)


We define the incremental update as


∆ _Os_ [(] _[r]_ [)] := _Os_ [(] _[r]_ [)][(] _[X]_ [)] _[ \ O]_ _s_ [(] _[r][−]_ [1)] ( _X_ ) _._ (5)


Opinions are then synchronized in a meeting
step that shares salient updates with all members.
Specifically, MEETING( _·_ ) is a lightweight aggregation operator that takes all specialists’ incremental updates _{_ ∆ _Os_ [(] _[r]_ [)] _[}]_ _s∈_ TEAM [and produces a dedu-]
plicated, concise shared bulletin ∆ _O_ share [(] _[r]_ [)] [:]


         -          ∆ _O_ share [(] _[r]_ [)] _[←]_ [MEETING] _{_ ∆ _Os_ [(] _[r]_ [)] _[}][s][∈]_ [TEAM] _._
(6)
Each specialist receives ∆ _O_ share [(] _[r]_ [)] [in] [the] [next]
round’s context to align beliefs and avoid redundant
discussion. Each specialist receives ∆ _O_ share [(] _[r]_ [)] [in the]
next round’s context. A specialist is marked converged when no further changes are proposed, i.e.,
∆ _Os_ [(] _[r]_ [)] = ∅. The process halts when all specialists
converge or when _r_ = _R_ max.


**Stage** **III:** **Report** **synthesis** **and** **final** **decision.**
After the bounded discussion, the coordinator agent
synthesizes the team’s cumulative evidence into a
discussion report DR:



(7)
The coordinator agent may also perform its own
retrieval ER from _E_ ( _X_ ), and outputs the final decision _A_ conditioned on the task record and aggregated evidence:


_A_ _←_ LLMCoo� _X_ _,_ DR _,_ ER� _._ (8)


**Remarks.** Stage I grounds role selection in a
predefined expert catalog _SP_, Stage II enforces a
bounded multi-turn consensus process with explicit
convergence checks and retrieval-augmented evidence, and Stage III separates evidence aggregation
(report synthesis) from decision making, improving
controllability and auditability.




 - _Os_ [(] _[r]_ [)][(] _[X]_ [)]

_s∈_ TEAM





_._



DR = SUMMARY




- _R_ max

 

_r_ =0



3


Figure 1: MATTRL overview. The figure uses **medical diagnosis** as a running example, but the framework is
domain-general. **Math** and **education** instantiations are in Appendix B.1 and C.1.



**3.2** **Test-Time Experience Construction**


Given a multi-agent transcript with _R_ turns, let
TEAM denote the set of specialist agents. At turn
_t_ _∈{_ 1 _, . . ., R}_, agent _i_ _∈_ TEAM produces an
utterance _ui,t_ under its observable context/history
_Hi,t_ . We employ an LLM judge (rubrics in Appendix A.5, B.6, and C.4.6) to evaluate each utterance along domain-relevant axes (e.g., correctness,
information gain, relevance to the task, clarity, _etc._ ),
yielding an _individual score_ :


_si,t_ = _ϕ_ LLM� _ui,t,_ _Hi,t_ ; Rubric� _∈_ [0 _,_ 1] _._ (9)


**Contribution ratio and terminal shared reward.**
Assume we obtain a single _terminal_ team-level outcome score _G_ at the end of the consultation (e.g.,
task success), where _G ∈_ [0 _,_ 1]. Let _R_ be the actual
number of turns (with _R ≤_ _R_ max). We allocate _G_
back to each turn via a decay kernel and split each
turn’s share across agents by contribution ratios.
Define per-turn decay weights

_wt_ = _γ_ _[R][−][t]_ (10)


The later turns receive higher weight when _γ_ _<_
1. Each agent’s contribution ratio _ci,t_ is estimated
by proportional normalization of per-agent scores
within each turn:

_si,t_
_ci,t_ =   - _si,t_ _≥_ 0 _,_ (11)
_j∈_ TEAM _[s][j,t]_ [ +] _[ ϵ,]_


where _ϵ_ avoids division by zero.



**Turn-level reward for each agent.** We fuse individual and terminal team signals:


_ri,t_ = _λ si,t_ + (1 _−λ_ ) _G·wt_ _·ci,t,_ _λ ∈_ [0 _,_ 1] _._
(12)


**Selection of high-value utterances.** To construct
reusable test-time experiences, we select highvalue snippets using a threshold:


_Ii_ [keep] =        - _t_ �� _ri,t_ _≥_ _τ_        - _._ (13)


**From high-scoring utterances to textual experi-**
**ence.** For each ( _i, t_ ) _∈Ii_ [keep], we map the context
_Hi,t_, utterance _ui,t_, and quantitative signals _ri,t_
into a structured, retrievable _textual experience en-_
_try_ using an LLM summarizer (prompt templates
in Appendix A.6):


      -      _ei,t_ = ΨLLM _Hi,t,_ _ui,t,_ _ri,t_ ; Templateexp _._
(14)
This yields a test-time experience pool


_E_ =  - _ei,t_ �� _i ∈_ TEAM _,_ _t ∈Ii_ keep  - _,_ (15)


We define a _textual experience entry_ as a compact,
structured text record that is easy to retrieve and
reuse. Each entry stores (i) minimal task context
for retrieval, (ii) the actionable step taken, and (iii)
a short rationale for the assigned credit.



4


|Method|Hit@1 Hit@3 Hit@5 Hit@10 MRR|
|---|---|
|MDAgent<br>RareAgents<br>RareAgent-Refned<br>MATTRL|0.32<br>0.49<br>0.57<br>0.68<br>0.46<br>0.29<br>0.38<br>0.47<br>0.68<br>0.42<br>0.35<br>0.49<br>0.57<br>0.70<br>0.47<br>**0.39**<br>**0.51**<br>**0.61**<br>**0.75**<br>**0.51**|


Table 1: Experimental Results on Baselines and MATTRL for medicine benchmark



**4** **Experiments**


**4.1** **Setup**


**Datasets and Domain Settings** In **Medicine** setting, RareBench (Chen et al., 2024b) evaluates
LLMs as rare-disease specialists across four tasks.
We focus on Task 4 (differential diagnosis among
universal rare diseases) with 2,185 cases covering
421 diseases, and cast the task as a multi-agent
consultation: an attending agent orchestrates domain specialists to independently propose and justify differential diagnoses from the patient record,
critique peers’ evidence, and iteratively refine toward a consensus shortlist. **Math** : We utilize HLE
(Humanity’s Last Exam) (Phan et al., 2025) with
text-only math problems (856 samples), a challenging benchmark of expert-level questions, to assess
collaborative problem solving. We report exactmatch solve rate via LLM judgement and quantify
the improvement brought by multi-agent deliberation with test time experience. **Education** :We
study teaching-oriented interaction with a threestage designs: pre-test, instruction, and post-test.
The student first answers with reasoning. Then a
teacher, given the question, gold answer, and the
student’s response, conducts a two-round teaching dialogue. Finally, the student re-answers. We
sample 300 questions from SuperGPQA (Du et al.,
2025) with GPT-4o as the student and GPT-5 as the
teacher, and measure learning gains by post-test
accuracy improvement. We also demonstrate the
detailed examples, settings and prompts for these
three domains in Appendix A, B and C.


**Baselines.** In **medicine** settings, We compare
against two agentic baselines. _MDAgents_ (Kim
et al., 2024) is an adaptive collaboration framework that estimates case complexity, recruits
an appropriate team, performs multi-turn analysis–synthesis, and ends with moderator review.
Its dynamic structure and moderation/knowledge
components improve medical QA and diagnosis. RareAgents (Chen et al., 2024a) targets raredisease diagnosis via a patient-centered Multidisciplinary Team (MDT) with specialist orchetra


tion, case-memory retrieval, and tool use. Since its
memory corpus and tool library are not released,
we reimplement the MDT-only version. We also introduce _RareAgents-Refined_, a prompt-engineered
variant that enforces role-focused, critical peer review and discourages fabricated tests/results, reducing confirmation bias and hallucinations and
yielding consistent gains. For **math** and **education**
domains, we use a **single-agent** solver/teacher that
directly performs the task as one baseline. We then
compare it against our **multi-agent** instantiation
described in Section 3.1, where multiple experts
independently propose, critique, and iteratively refine solutions (or teaching moves) with periodic
synchronization/aggregation. This isolates the effect of test-time experience.


**Metrics** **Medicine.** We report _Hit@k_ and _MRR_
on the attending agent’s _final_ _ranked_ _differential_
_list/shortlist_, where Hit@k is the fraction of cases
whose ground-truth disease appears within the top_k_ predictions, and MRR averages 1 _/_ rank of the
correct disease. Higher is better. **Math.** We report exact-match solve rate ( _Acc_ ), where a problem
is counted as solved if the final answer matches
the reference under an LLM judge. **Education**
**(SuperGPQA).** We measure learning by pre-test
and post-test accuracy and report learning gains as
∆ _Acc_ = _Acc_ post _−_ _Acc_ pre (higher indicates stronger
instructional improvement).


**Paremeters** **Settings** We use GPT-5 (OpenAI,
2025) as the backbone model is our MATTRL
framework and other aforementioned LLMs are
also GPT-5. The number of experts is 3, and the
maximum conversation turns are limited to 3. For
experience text construction, we select 30 cases.
For all utterance from agents, we extract the Top
25% scored records for further construction.


**4.2** **Results**


As demonstrated in Table 1, in medicine task,
MATTRL achieves the strongest overall retrieval
quality. Averaged over k = 1, 3, 5, and 10, its
Hit@k is 0.565, higher than MDAgent at 0.515 and
RareAgents-Refined at 0.528, and it also attains



5


|Method|Single Agent Multi-Agent MATTRL|
|---|---|
|_Acc_|0.27<br>0.33 (+0.06)<br>0.36 (+0.09)|


Table 2: **Math** **(Accuracy** **Comparison** **with** **Per-**
**Method** **Improvement).** We report exact-match accuracy on HLE math problems. Numbers in the bottomright indicate the absolute change in accuracy relative
to the single agent baseline


the highest MRR of 0.51. The most pronounced
advantages appear at Hit@1, indicating better toprank precision, and at Hit@10, indicating more
reliable shortlist coverage. Overall, the results suggest that test-time collaborative adaptation yields
benefits beyond those achievable through prompt
optimization alone.


As shown in Table 2, the single-agent baseline
achieves an exact-match accuracy of 0.27 on HLE.
Introducing multi-agent deliberation improves performance to 0.33, indicating a modest benefit from
parallel proposal and critique. MATTRL yields
a larger gain, reaching 0.36, suggesting that testtime experience further strengthens collaborative
problem solving beyond deliberation alone.


For Education, as shown in Table 3, all methods
start from the same pre-test accuracy ( _Acc_ pre =
0 _._ 44), ensuring a controlled comparison where
improvements reflect instructional effectiveness
rather than initial student performance. The singleagent teacher increases accuracy to _Acc_ post = 0 _._ 60
(∆ _Acc_ = 0 _._ 16). Replacing it with a multi-agent
teacher that proposes and critiques teaching moves
yields a much larger gain, suggesting that deliberation helps identify misconceptions and select more
effective explanations. MATTRL further achieves
the best post-test performance at _Acc_ post = 0 _._ 77
with the highest learning gain (∆ _Acc_ = 0 _._ 33),
nearly doubling the improvement of the singleagent baseline. Overall, the results indicate that
collaboration substantially enhances teaching outcomes, and test-time experience provides additional benefits beyond collaboration alone.

|Method|Acc Acc ∆Acc<br>pre post|
|---|---|
|Single Agent<br>Multi-Agent<br>MATTRL|0.44<br>0.60<br>0.16<br>0.44<br>0.73<br>0.29<br>0.44<br>0.77<br>0.33|



Table 3: **Education (Learning Gains in a Pre-test** _→_
**Tutoring** _→_ **Post-test Setup).** We report pre-test accuracy ( _Acc_ pre), post-test accuracy ( _Acc_ post), and learning
gain (∆ _Acc_ = _Acc_ post _−_ _Acc_ pre).



**5** **Analysis**


**All ablations and analysis conducted below are**
**based on medicien dataset (RareBench)** .


**5.1** **Group-to-Agent Credit Assignment**


We compare naive averaging, Difference Rewards,
and Shapley-style approximations for attributing
team returns at each turn to individual agents.
As we mentioned in section 3.2, We compute
agent-specific _credit scores qi,t_ for agent _i_ at turn
_t_ and map them to contribution ratios via a shared
normalization to ensure comparability:


exp( _β qi,t_ )
_ci,t_ =  - _β_ _>_ 0 _._ (16)
_j∈_ TEAM [exp(] _[β q][j,t]_ [)]


**Difference Rewards.** For agent _i_ at turn _t_, define the counterfactual where _i_ is neutralized while
others remain:


_qi,t_ [Diff] = _Ft_ (TEAM) _−_ _Ft_ (TEAM _\ {i}_ ) (17)


where _Ft_ ( _·_ ) is the turn- _t_ team objective (e.g., consensus gain or hypothesis-space reduction). In practice, _Ft_ (MDT _\ {i}_ ) is approximated by rerunning
the turn with _i_ ’s utterance replaced by a no-op, or
via a learned proxy (Appendix).
**Shapley-style** **approximations.** The Shapley
value averages _i_ ’s marginal effect across orders:


_qi,t_ [Shap] = E _π_   - _Ft_   - _Sπ_ _[<i]_ _[∪{][i][}]_   - _−_ _Ft_   - _Sπ_ _[<i]_ �� (18)


with _Sπ_ _[<i]_ [the set of agents preceding] _[ i]_ [ in permu-]
tation _π_ . We estimate _qi,t_ [Shap] via _K_ Monte Carlo
permutations (or small-coalition sampling) with
cached _Ft_ ( _·_ ) to control cost. Unless stated otherwise, all schemes use the same _Ft_ ( _·_ ) and the same
normalization (identical _β_ ) before feeding _ci,t_ into
the decay-weighted terminal allocation in _Contri-_
_bution ratio and terminal shared reward._

|Method|Hit@1 Hit@3 Hit@5 Hit@10|
|---|---|
|Naive<br>Difference<br>Shapley|0.39<br>0.51<br>0.61<br>0.75<br>0.40<br>0.53<br>0.61<br>0.74<br>0.35<br>0.49<br>0.59<br>0.75|



Table 4: Performance comparison among different
credit assignments for experience construction. Naive
represents the Naive method we mentioned in section 3.2, Difference denotes the Difference Rewards
and Shapley is Shapley-style approximations.


As shown in Table 4, DIFFERENCE yields
the best strict-precision performance (Hit@1/3 =
0.40/0.53), outperforming NAIVE (0.39/0.51) and



6


SHAPLEY (0.35/0.49). At broader cutoffs the
methods are similar: Hit@5 is tied for DIFFER
ENCE/NAIVE (0.61) and Hit@10 is nearly identical
(0.74–0.75). We attribute DIFFERENCE’s gains on
tight metrics to reduced free-riding noise: contrasting the full team with a counterfactual where agent
_i_ is neutralized better isolates decisive turns and
produces sharper credit peaks after normalization.
By contrast, SHAPLEY tends to spread credit across
coalitions (and is variance-prone under limited permutations), which dilutes peaks and hurts Hit@1/3
despite comparable Hit@10.


**Why Shapley underperforms.** We observe that
Shapley-style selection tends to reward _peer-_
_review/alignment_ _behaviors_ that improve coherence and consensus but have limited influence on
the decisive inference steps. Since Shapley averages marginal effects across many coalitions, sharp
decision moves are diluted while low-variance
meta-behaviors accumulate steady credit (e.g.,
“integrate peer comments coherently,” “maintain
cross-specialty consensus”). By contrast, Naive
more often elevates _decision-centric_ _hints_ with
short feedback loops because it ties credit to singlerun outcome deltas (e.g., “prioritize MMA over PA
when biomarkers dominate,” “merge weakly anchored subtypes into a low-priority bucket”), yielding sharper hypothesis ranking and stronger toprank accuracy. Beyond hit rates, compute and stability also favor Difference. Shapley needs many
marginal evaluations and has higher estimator variance unless heavily sampled; Naive is cheapest but
sensitive to correlated noise. Difference offers a
practical middle ground with one counterfactual
per agent, providing a low-variance, high-leverage
signal at modest cost. Overall, we recommend
Shapley when fairness is paramount and budget allows, Naive as a low-cost baseline, and Difference
as the default when precision and efficiency matter.


**5.2** **Adaptive collaboration between single**
**agent and multi-agent framework**


To further improve the practicality of MATTRL, we
additionally compare against a single-agent baseline using chain-of-thought (CoT) reasoning and
develop an Adaptive method that learns to route
each case to either the single agent or MATTRL.
The classifier makes the routing decision based on
features capturing symptom complexity, need for
multidisciplinary consultation, number of specialties involved, cross-specialty divergence, and risk



of single-expert misguidance. As shown in Table 5,
the single-agent CoT baseline is already strong, and
the Adaptive router further improves performance,
achieving average gains of 10% over the single
agent and 5.5% over MATTRL.

|Method|Hit@1 Hit@3 Hit@5 Hit@10|
|---|---|
|Single-Agent<br>MATTRL<br>Adaptive|0.39<br>0.49<br>0.56<br>0.64<br>0.39<br>0.51<br>0.61<br>0.75<br>**0.45**<br>**0.58**<br>**0.66**<br>**0.79**|



Table 5: Results of Single-Agent, MATTRL, and Adaptive Router (Adaptive in below table).


Single-agent excels when cases show standardized diagnostic “fingerprints” that a one-shot integration can resolve, evidence is concentrated in
one specialty, and the task prioritizes internal consistency with a concise explanation. Multi-agent
is stronger when evidence spans multiple specialties or modalities and needs cross-validation, the
goal extends to risk assessment/care planning/test
prioritization, and the task benefits from systematic counterfactuals and competing hypotheses for
robust differentials. This aligns with our analysis
for the classifier in adaptive method and the error
analysis for both single agent and MATTRL.
Our classifier routed 282 cases to the singleagent solver and 840 to MATTRL. Empirically,
many instances that are internally consistent are
solvable by the single agent, yet the multi-agent
discussion can introduce noise that harms accuracy on those same cases. A Venn-style breakdown of correctness shows: Only the single agent
solves around 300 cases, only MATTRL solves
400+ cases, and both solve 357 cases.


**5.3** **Scaling with Team Size**


We study how performance scales as the number
of collaborating agents increases (e.g., 1, 3, 7, 9).
As shown in Figure 2, increasing the number of
agents does not uniformly improve performance.
For Hit@1, accuracy peaks at three agents and then
declines as the team grows. Because Hit@1 requires strict precision, larger teams introduce more
divergent opinions and make consensus harder to
reach. In contrast, Hit@3 and Hit@5 exhibit modest, steady gains with scale. Hit@10 benefits the
most from scaling, as broader discussions surface
more plausible candidates and are more tolerant to
noise. Notably, a three-agent team outperforms a
single agent by about 14% on Hit@10. Practically,
smaller teams (e.g., three agents) are preferable



7


80


60


40


1 3 5 7 9


Team size (number of experts)


Figure 2: GPT-5 Multi-Agent: Acc. by Team Size.


for high-precision decisions, whereas larger teams
help when broader recall is desired.



weak. _Disease-specific_ _experiences_ are concise,
concrete checks that guide fine-grained ordering
among close candidates (e.g., first clarify the locus of leukocoria before assuming a subtype; let
high-weight skeletal markers adjust relative ranks;
keep craniosynostosis low without direct evidence
of suture involvement). Practically, we select utterances with higher reward via credit assignment,
distill their underlying rationale into brief, textual
experience snippets, and retrieve them at inference
to stabilize multi-agent deliberation and improve
accuracy without updating model weights.


**5.5** **Few-shot vs.** **Test-time Experience**


To test whether MATTRL’s gains stem merely from
supplying extra context, we compare MATTRL
with RareAgents augmented by few-shot exemplars
(containing patient information and the final diagnosis). For each test case, 3 random exemplars
are prepended to the conversation. As shown in
Table 6, few-shot prompting yields only a minor
improvement in Hit@1 while reducing Hit@3/5/10.
This indicates that MATTRL’s advantage arises
from its structured experience integration rather
than from simply adding more information.

|Method|Hit@1 Hit@3 Hit@5 Hit@10|
|---|---|
|RareAgents<br>+ Fewshot|0.35<br>0.49<br>0.57<br>0.70<br> 0.37<br>0.48<br>0.55<br>0.68|
|MATTRL|0.39<br>0.51<br>0.61<br>0.75|



Table 6: Comparison with fewshot learning, where we
add 3 examples at the beginning of each conversation.

**6** **Conclusion**


We introduced **MATTRL**, a test-time adaptation
framework that strengthens multi-agent reasoning
by injecting _structured textual experience_ into deliberation. MATTRL builds a small expert team,
curates an experience pool from high-value dialogue turns via group-to-agent credit assignment,
and retrieves these experiences to guide subsequent
collaboration. Across **medicine**, **math**, and **ed-**
**ucation**, it consistently outperforms single- and
multi-agent baselines, showing that experienceconditioned collaboration improves robustness under distribution shift. We further analyzed creditassignment strategies and find that DIFFERENCE
rewards provide a strong accuracy and efficiency
trade-off for experience construction. Finally, an
adaptive router that selects between single-agent
inference and MATTRL yields additional gains by
matching collaboration style to case complexity.







Figure 3: General & disease-specific experience


**5.4** **Experience Examples**


Figure 6 shows two kinds of reusable test-time
experiences that MATTRL extracts from consultation transcripts. _General_ _experiences_ are crossdisease rules that improve discriminability and
keep discussion disciplined. For instance, they require mechanism-grounded justifications instead of
vague “seems consistent”, prioritize a small set of
high-yield discriminators as the ranking backbone,
and state uncertainty explicitly when evidence is



8


**Limitations**


We recognize two practical limitations remain.
First, the method’s inference-time compute and
latency grow with multi-agent rollouts and exploration budget. Second, a continually growing testtime experience pool is vulnerable to drift: stale,
duplicated, or spurious heuristics may accumulate.
Looking ahead, we will (i) introduce dynamic budget controllers and confidence-based early stopping to cap cost without hurting accuracy, and (ii)
add lifecycle management for experiences (recency
weighting, de-duplication, anomaly screening) to
preserve precision over time.


**References**


Weize Chen, Yusheng Su, Jingwei Zuo, Cheng Yang,
Chenfei Yuan, Chen Qian, Chi-Min Chan, Yujia Qin,
Yaxi Lu, Ruobing Xie, and 1 others. 2023. Agentverse: Facilitating multi-agent collaboration and exploring emergent behaviors in agents. _arXiv preprint_
_arXiv:2308.10848_, 2(4):6.


Xi Chen, Huahui Yi, Mingke You, WeiZhi Liu, Li Wang,
Hairui Li, Xue Zhang, Yingman Guo, Lei Fan, Gang
Chen, and 1 others. 2025. Enhancing diagnostic
capability with multi-agents conversational large language models. _NPJ digital medicine_, 8(1):159.


Xuanzhong Chen, Ye Jin, Xiaohao Mao, Lun Wang,
Shuyang Zhang, and Ting Chen. 2024a. Rareagents:
Autonomous multi-disciplinary team for rare disease
diagnosis and treatment. _arXiv e-prints_, pages arXiv–
2412.


Xuanzhong Chen, Xiaohao Mao, Qihan Guo, Lun Wang,
Shuyang Zhang, and Ting Chen. 2024b. Rarebench:
can llms serve as rare diseases specialists? In _Pro-_
_ceedings of the 30th ACM SIGKDD conference on_
_knowledge discovery and data mining_, pages 4850–
4861.


Matthijs Douze, Alexandr Guzhva, Chengqi Deng,
Jeff Johnson, Gergely Szilvasy, Pierre-Emmanuel
Mazaré, Maria Lomeli, Lucas Hosseini, and Hervé
Jégou. 2024. The faiss library. _arXiv_ _preprint_
_arXiv:2401.08281_ .


Xinrun Du, Yifan Yao, Kaijing Ma, Bingli Wang,
Tianyu Zheng, King Zhu, Minghao Liu, Yiming
Liang, Xiaolong Jin, Zhenlin Wei, and 1 others. 2025.
Supergpqa: Scaling llm evaluation across 285 graduate disciplines. _arXiv preprint arXiv:2502.14739_ .


Adam Fourney, Gagan Bansal, Hussein Mozannar,
Cheng Tan, Eduardo Salinas, Friederike Niedtner,
Grace Proebsting, Griffin Bassman, Jack Gerrits, Jacob Alber, and 1 others. 2024. Magentic-one: A
generalist multi-agent system for solving complex
tasks. _arXiv preprint arXiv:2411.04468_ .



Daya Guo, Dejian Yang, Haowei Zhang, Junxiao
Song, Ruoyu Zhang, Runxin Xu, Qihao Zhu, Shirong Ma, Peiyi Wang, Xiao Bi, and 1 others. 2025.
Deepseek-r1: Incentivizing reasoning capability in
llms via reinforcement learning. _arXiv_ _preprint_
_arXiv:2501.12948_ .


Zhitao He, Zijun Liu, Peng Li, Yi R Fung, Ming Yan,
Ji Zhang, Fei Huang, and Yang Liu. Advancing language multi-agent learning with credit re-assignment
for interactive environment generalization. In _Second_
_Conference on Language Modeling_ .


Jinwu Hu, Zhitian Zhang, Guohao Chen, Xutao Wen,
Chao Shuai, Wei Luo, Bin Xiao, Yuanqing Li, and
Mingkui Tan. 2025a. Test-time learning for large
language models. _arXiv preprint arXiv:2505.20633_ .


Zhiyuan Hu, Yibo Wang, Hanze Dong, Yuhui Xu, Amrita Saha, Caiming Xiong, Bryan Hooi, and Junnan
Li. 2025b. Beyond’aha!’: Toward systematic metaabilities alignment in large reasoning models. _arXiv_
_preprint arXiv:2505.10554_ .


Yun Hua, Haosheng Chen, Shiqin Wang, Wenhao Li,
Xiangfeng Wang, and Jun Luo. 2025. Shapleycoop: Credit assignment for emergent cooperation in self-interested llm agents. _arXiv_ _preprint_
_arXiv:2506.07388_ .


Yubin Kim, Chanwoo Park, Hyewon Jeong, Yik S Chan,
Xuhai Xu, Daniel McDuff, Hyeonhoon Lee, Marzyeh
Ghassemi, Cynthia Breazeal, and Hae W Park. 2024.
Mdagents: An adaptive collaboration of llms for medical decision-making. _Advances in Neural Informa-_
_tion Processing Systems_, 37:79410–79452.


Guohao Li, Hasan Hammoud, Hani Itani, Dmitrii
Khizbullin, and Bernard Ghanem. 2023. Camel:
Communicative agents for" mind" exploration of
large language model society. _Advances in Neural_
_Information Processing Systems_, 36:51991–52008.


Zichen Liu, Changyu Chen, Wenjun Li, Penghui Qi,
Tianyu Pang, Chao Du, Wee Sun Lee, and Min Lin.
2025. Understanding r1-zero-like training: A critical
perspective. _arXiv preprint arXiv:2503.20783_ .


Kartik Nagpal, Dayi Dong, Jean-Baptiste Bouvier, and
Negar Mehr. 2025. Leveraging large language models for effective and explainable multi-agent credit
assignment. _arXiv preprint arXiv:2502.16863_ .


OpenAI. 2025. [Introducing gpt-5.](https://openai.com/index/introducing-gpt-5/)


Chanwoo Park, Seungju Han, Xingzhi Guo, Asuman
Ozdaglar, Kaiqing Zhang, and Joo-Kyung Kim. 2025.
Maporl: Multi-agent post-co-training for collaborative large language models with reinforcement learning. _arXiv preprint arXiv:2502.18439_ .


Long Phan, Alice Gatti, Ziwen Han, Nathaniel Li,
Josephina Hu, Hugh Zhang, Chen Bo Calvin Zhang,
Mohamed Shaaban, John Ling, Sean Shi, and 1 others. 2025. Humanity’s last exam. _arXiv_ _preprint_
_arXiv:2501.14249_ .



9


Chen Qian, Wei Liu, Hongzhang Liu, Nuo Chen, Yufan
Dang, Jiahao Li, Cheng Yang, Weize Chen, Yusheng
Su, Xin Cong, and 1 others. 2023. Chatdev: Communicative agents for software development. _arXiv_
_preprint arXiv:2307.07924_ .


Chen Qian, Zihao Xie, Yifei Wang, Wei Liu, Kunlun
Zhu, Hanchen Xia, Yufan Dang, Zhuoyun Du, Weize
Chen, Cheng Yang, and 1 others. 2024. Scaling
large language model-based multi-agent collaboration. _arXiv preprint arXiv:2406.07155_ .


Khanh-Tung Tran, Dung Dao, Minh-Duong Nguyen,
Quoc-Viet Pham, Barry O’Sullivan, and Hoang D
Nguyen. 2025. Multi-agent collaboration mechanisms: A survey of llms. _arXiv_ _preprint_
_arXiv:2501.06322_ .


Ziyu Wan, Yunxiang Li, Xiaoyu Wen, Yan Song,
Hanjing Wang, Linyi Yang, Mark Schmidt, Jun
Wang, Weinan Zhang, Shuyue Hu, and 1 others.
2025. Rema: Learning to meta-think for llms with
multi-agent reinforcement learning. _arXiv preprint_
_arXiv:2503.09501_ .


Jiayin Wang, Zhiquang Guo, Weizhi Ma, and Min
Zhang. 2025. How far can llms improve from
experience? measuring test-time learning ability
in llms with human comparison. _arXiv_ _preprint_
_arXiv:2506.14448_ .


Qingyun Wu, Gagan Bansal, Jieyu Zhang, Yiran Wu,
Beibin Li, Erkang Zhu, Li Jiang, Xiaoyun Zhang,
Shaokun Zhang, Jiale Liu, and 1 others. 2024. Autogen: Enabling next-gen llm applications via multiagent conversations. In _First_ _Conference_ _on_ _Lan-_
_guage Modeling_ .


Weihao Zeng, Yuzhen Huang, Qian Liu, Wei Liu, Keqing He, Zejun Ma, and Junxian He. 2025. Simplerlzoo: Investigating and taming zero reinforcement
learning for open base models in the wild. _arXiv_
_preprint arXiv:2503.18892_ .


Yanzhao Zhang, Mingxin Li, Dingkun Long, Xin Zhang,
Huan Lin, Baosong Yang, Pengjun Xie, An Yang,
Dayiheng Liu, Junyang Lin, and 1 others. 2025.
Qwen3 embedding: Advancing text embedding and
reranking through foundation models. _arXiv preprint_
_arXiv:2506.05176_ .


Yuxin Zuo, Kaiyan Zhang, Li Sheng, Shang Qu, Ganqu
Cui, Xuekai Zhu, Haozhan Li, Yuchen Zhang, Xinwei Long, Ermo Hua, and 1 others. 2025. Ttrl:
Test-time reinforcement learning. _arXiv_ _preprint_
_arXiv:2504.16084_ .



10


**A** **Medicine**


**A.1** **Detailed Setup**


**Task and data (RareBench Task 4).** We instantiate MATTRL as an MDT-style workflow for raredisease differential diagnosis on RareBench Task
4 (Chen et al., 2024b). Each instance provides a
patient record _X_ and the system outputs a ranked
top-10 differential list. We evaluate with Hit@k
and MRR as defined in the main text.


**Agents, specialist pool, and recruitment.** The
system consists of a coordinator/chair agent
LLMCoo and a predefined specialist catalog _SP_
(Appendix A.2). LLMCoo recruits a small MDT
TEAM _⊆SP_ using the recruitment prompt (Appendix A.4), grounding role selection in real clinical departments rather than free-form role invention.


**MDT interaction protocol and prompts.** Given
TEAM, specialists follow role-specific opinion
prompts and produce a strict top-10 list each round
(Appendix A.4). We run synchronized multi-round
discussion with a maximum of _R_ max rounds as described in Sec. 3.1. The chair then synthesizes a
discussion report and outputs the final ranked list
using the final-decision prompt (Appendix A.4).
Experience-augmented prompting uses the standardized injection template in Appendix A.3.


**Utterance scoring and judge rubric.** To score
specialist utterances for experience construction,
we use an LLM judge with the rubric defined
in Appendix A.5, producing per-utterance scores
_si,t_ _∈_ [0 _,_ 1] (Eq. (9) in the main text). These individual scores are combined with a terminal caselevel outcome signal via the decay-weighted allocation (Eq. (10)–(12) in the main text).


**Experience** **extraction** **and** **summarization.**
High-scoring utterances are distilled into structured textual experiences using an LLM summarizer with the template in Appendix A.6. Each entry follows the ACTION/EXPERIENCE schema used
in our experience-augmented prompt template (Appendix A.3).


**Indexing and retrieval.** At test time, each specialist retrieves relevant experience entries conditioned on the case and round context. We detail
the embedding model, similarity metric, and top- _K_
retrieval procedure in Appendix **??** . Retrieved experiences are appended to prompts via the injection



block in Appendix A.3, keeping model weights
fixed while providing dense guidance.


**A.2** **Description of Specialist Pool**


This pool covers core inpatient and outpatient specialties frequently involved in complex differential
diagnosis. It is designed to balance breadth with
depth, enabling targeted and efficient MDT assembly.


Pediatrics Urology
Hematology Rheumatology
Psychiatry Pulmonology
Dentistry Endocrinology
Allergy and Immunology Cardiology
Pathology Neurology
Obstetrics and Gynecology Ophthalmology
Dermatology Geriatrics
Traditional Chinese Medicine Nephrology
Oncology General Practice
Gastroenterology Infectious Diseases
Rehabilitation Medicine Otorhinolaryngology


Table 7: List of 24 Departments from Specialist Pool.


**A.3** **Experience-Augmented Prompt Template**


This template integrates retrieved experience into
the base diagnostic instruction. The _Experi-_
_ence Context_ block is formatted to remain modelfriendly while improving calibration and coverage
of edge patterns.





11


**A.4** **Prompts for Multi-disciplinary Team**
**Collaboration**


These prompts orchestrate role selection, rolespecific reasoning, and peer oversight. The design favors minimal, structured outputs to simplify
downstream aggregation and evaluation.







12


**A.6** **Prompts for LLM Summarizer**


The summarizer condenses multi-turn MDT content into an actionable brief for clinicians or downstream modules, emphasizing signal over verbosity
and avoiding speculative language.



**A.5** **Rubrics for LLM Judge in Agent’s**
**Utterance**


This rubric converts free-form predictions into a
single categorical judgment for evaluation. The instructions prefer clinical synonymy while rejecting
incompatible subtypes, balancing sensitivity and
specificity for leaderboard scoring.







**A.7** **Retrieval Implementation Details**


We implement the retrieval module _M_ using a dense vector index to inject relevant
reasoning priors. Specifically, we employ
Qwen/Qwen3-Embedding-4B as the backbone encoder _E_ ( _·_ ). To ensure the inner product search is
equivalent to cosine similarity, we apply _L_ 2 normalization to the embeddings of all key-value experience pairs ( _ki, vi_ ) stored in the database, yielding index vectors **u** _i_ = _E_ ( _ki_ ) _/∥E_ ( _ki_ ) _∥_ 2, which
are stored using the FAISS library’s IndexFlatIP.
During inference at time _t_, the current agent’s instruction _xt_ is encoded into a normalized query vec


13


tor **q** _t_ = _E_ ( _xt_ ) _/∥E_ ( _xt_ ) _∥_ 2. The system retrieves
the top- _K_ entries (default _K_ = 8) by maximizing
the similarity score _si_ = **q** _[⊤]_ _t_ **[u]** _[i]_ [and appends them]
to the prompt using a strict “EXPERIENCE HINTS”
template to guide the model’s reasoning.


**B** **Mathematics**


**B.1** **Detailed Setup**


We instantiate MATTRL for multi-agent mathematical problem solving (Figure 4). Given a math
problem (task record _X_ ), the coordinator agent
LLMCoo forms a small team of specialists, runs a
bounded multi-round collaboration with optional
experience retrieval, and finally synthesizes a discussion report and outputs the final solution. This
appendix specifies the concrete collaboration protocol and prompts used in the math setting.


**Baseline run (no experience)** We first run MATTRL (math) with experience augmentation disabled
(–use_experience off). For each problem, the
pipeline outputs a final solution artifact and a detailed interaction log recording each specialist opinion, peer review, and round summary.


**B.2** **Free recruitment team formation**


In math, because of the flexibility of math problem,
we use free recruitment: instead of selecting from
a fixed catalog, the coordinator directly proposes
a small set of specialist descriptions tailored to the
current problem, and forms TEAM accordingly.
This corresponds to the team-formation stage of
our pipeline, where the coordinator constructs a
small set of role-specialized agents on-the-fly for
each problem.







**B.3** **Multi-round collaboration (Stage II)**


We run up to _R_ max collaboration rounds. In each
round, every non-converged specialist proposes a
solution attempt; other specialists then provide targeted critiques and minimal fixes in a structured
format. The coordinator aggregates these critiques
into a concise feedback bulletin, which is provided
to specialists in the next round for revision. A specialist is marked converged once their solution no
longer changes under critique.









**B.4** **Structured peer review and acceptance**
**rule**


For each specialist’s attempt, all other specialists generate a structured peer review in raw
JSON, including an overall appraisal, a verdict (accept/revise/reject), validated parts,
and a list of concrete issues with severities
(fatal/major/minor) and minimal fixes. A specialist’s attempt is marked accepted _only if_ (i) all
peer verdicts are accept and (ii) the issues list
is empty. When critiques identify no remaining
issues, we treat the specialist’s update as converged
(i.e., no further changes are proposed in subsequent
rounds). The collaboration halts when all specialists converge or when reaching round budget.



14


**B.6** **Rubrics for LLM Judge in Math**
**Utterance Scoring**


We use an LLM judge to score (i) the terminal
correctness of the final answer and (ii) the perutterance contribution within the multi-agent transcript. The terminal judgment provides the team
outcome signal _G_ _∈{_ 0 _,_ 1 _}_, while the utterance


{delta_json}


Please think step by step from your expert perspec
tive, and produce ONE integrated, concise message

addressing feedback (no step numbering).

State the refined reasoning and the final answer if

applicable.

Be precise and minimal; no special tags.


**B.5** **Chair aggregation (final decision)**


After bounded discussion, the coordinator LLMCoo
synthesizes a discussion report DR from all specialists’ updates (Stage III), and outputs the final
solution. If the first chair output does not contain
these tags, the system triggers a rewrite pass that
preserves mathematical content but enforces the
target format.









15


level score _si,t_ measures how much a given agent
utterance helps (or hurts) reaching the correct final
solution. In implementation, the judge outputs an
integer score in [0 _,_ 5], and we optionally normalize
it to [0 _,_ 1] by _si,t_ = score _/_ 5.



**B.7** **Interaction scoring and selection (train**
**split only)**


We score each specialist utterance with an LLM
judge to obtain an individual score _si,t_, then combine it with a terminal correctness signal allocated
back to turns using a decay factor. Each specialist utterance is scored by an LLM judge to obtain
an individual score _si,t_, and a terminal correctness
signal _G_ is allocated back to turns with decay. We
then select high-value utterances (e.g., top quantile
or thresholded by _ri,t_ ) to form the candidate set for
experience extraction.


**B.8** **Experience extraction and indexing (train**
**split only)**


Selected high-value utterances are distilled into
concise textual experiences using a fixed LLMbased summarization template, producing key–
value entries that are easy to retrieve. We embed
the keys, build a dense index (Appendix A.7), and
retrieve top- _K_ experiences at inference time. Retrieved experiences are appended to prompts using
the standardized EXPERIENCE HINTS block.


**B.9** **Test-Time Experience Retrieval**


At test time, each non-converged specialist retrieves relevant experiences from the shared pool _E_
based on the current problem and its round context.
Retrieval is implemented with dense embeddings
and a FAISS index. The retrieved entries are appended to the prompt using the same EXPERIENCE
HINTS template as other domains, serving as consultable guidance without updating model weights.











We then combine the utterance score with the
decayed terminal signal: the terminal correctness
_G_ is allocated to turns with a decay factor and distributed among agents within the same turn proportionally to their utterance scores, and finally fused
with the direct utterance score to obtain _ri,t_ used
for experience selection.





16


Figure 4: MATTRL in Math: Multi-Specialist Math Problem-solving Collaboration.



**C** **Education**


**C.1** **Detailed Setup**


Large language models are increasingly serving as
educational tools, yet evaluating their teaching capabilities remains challenging. In this experiment,
we adapt the MATTRL framework and create a
realistic learning scenario in which a team of pedagogy specialists works together to guide students
through complex problem-solving tasks (Figure 5).
This setup allows us to test how effective the MARRLL is at improving the teaching performance of
multi-agent systems.


**Pre-test** A pre-test is conducted to establish baseline student performance before any instruction.
A student agent (GPT-4o, temperature=0.3) is
prompted (in C.4.1) to solve multiple-choice questions from SuperGPQA, providing both the answer
and reasoning to surface its thinking and uncertainties. Pre-test questions are selected via stratified
sampling across 13 subject matters and three difficulty levels to ensure balanced coverage. The
pre-test is run once before any teaching sessions,
and the same student agent instance is reused across
all experimental conditions.


**Pedagogy Specialist Team Formation** Before
the instructional session, a pedagogy specialist
team of three members is formed based on an
analysis of the question and the students’ pre-test



performance. Team members are selected from a
predefined pool (C.4.2, Table C.3) that includes
subject-matter experts, pedagogical specialists, and
cross-disciplinary specialists. Each team member
is assigned a specific role: the diagnostician identifies the reasons for the student’s incorrect response,
the pedagogy strategist proposes appropriate instructional strategies, and the subject matter expert
provides discipline-specific explanations.


**Multi-round teaching session** During the teaching session, the teaching agent (GPT-5, temperature=0.3) is provided with the full question text
and the correct answer, the student’s pre-test response and reasoning, and the correctness status.
The teacher agent guides the student toward the
correct answer through a structured, three-round
question–answer dialog that diagnoses and clarifies misconceptions while scaffolding the student’s
reasoning, without directly revealing the answer.
Three teaching conditions are evaluated for comparison: (1) a _Single-Teacher_ condition, in which a
single agent conducts the full dialog using a fixed
instructional prompt (C.4.3); (2) a _Multi-Teacher_
condition, in which multiple specialist agents generate each instructional strategy analysis based on
their role-specific perspectives first and collaboratively plan before interacting with the student agent
( Prompt: C.4.4); and (3) a _Multi-Teacher with Ex-_
_perience_ condition, which extends the collabora


17


Figure 5: MATTRL in Education: Multi-Specialist Teaching Collaboration.



tive setting by incorporating role-, subject-, and
difficulty-specific teaching experiences retrieved
from the experience pool to inform instructional
strategy generation (Prompt: C.4.5).


**Post-test** In the post-test, the student agent answers the same question again using the same response format as the pre-test. If the student answered correctly on the pre-test, the teaching session will be skipped, and the pre-test answer will
be reused in the post-test.


**Interaction scoring and selection** To construct
the pedagogy experience pool, additional teaching
interactions are generated using stratified sampling
over subject domains and difficulty levels from the
SuperGPQA dataset under the multi-agent teaching setting described above. 28 successful cases
are finally identified and scored using two complementary signals. First, a global outcome score
captures overall instructional success and is defined as a binary indicator of post-test correctness,
assigning a value of 1 _._ 0 if the student’s post-test
answer is correct and 0 _._ 0 otherwise. Second, a
step-level influence score evaluates the contribution of each teaching-strategy utterance to student
learning. Each utterance is rated on a 0–5 scale
by an LLM adjudicator, measuring its causal influence on the student’s progress relative to the
pre-test baseline. In addition, each role of teachers’
pedagogy analyzing utterance is evaluated using a



rubric-based utterance quality score (C.4.6). The
binary global outcome score is temporally allocated across dialogue turns using decay with factor
_γ_ = 0 _._ 85, assigning higher credit to earlier instructional turns. Within each turn, the allocated global
credit is distributed across utterances in proportion
to their step-level influence scores. Finally, each utterance is assigned a combined score computed as a
weighted average of its share of the decayed global
credit and its direct instructional contribution, with
weights of 0.6 and 0.4, respectively.


**Experience** **extraction** **and** **summarization**
From each scored teaching interaction, the topranked (25%) utterances are selected based on their
_final_score_ and converted into transferable pedagogical experiences using an LLM-based extractor
(C.4.7). Each extracted experience follows a constrained instructional format and is categorized as
either general or subject-specific. Experiences are
indexed by the teacher role, subject domain, and
difficulty level, and stored in a structured format.
We provide example experiences here in C.2.


**C.1.1** **Test-Time Experience Retrieval**

At test time, when experience augmentation is enabled, each teacher agent first attempts to load a
role-specific pedagogy experience knowledge base
according to the corresponding question subject
matter and difficulty level. The role-specific knowledge base is identified using the agent’s assigned



18


instructional role (e.g., Diagnostician, Subject Matter Expert, or Pedagogy Strategist). Retrieved experiences are appended to the agent’s prompt in a
_Experience Hints_ section, explicitly marked as consultative guidance intended to inform the agent’s
instructional decisions, rather than to be quoted
verbatim in generated responses.


**C.2** **Experience Examples**







**C.4** **Prompts**


**C.4.1** **Prompt for Student Agent in Pre-test**


This prompt guides the student agent to answer a
multiple-choice question while explicitly articulating its reasoning process.


**C.4.2** **Pedagogy Specialist Recruitment**
**Prompt**


This prompt guides the pedagogy specialist to assemble an appropriate teaching team by identifying
the pedagogical expertise required for the given
pre-test question.





Figure 6: General & subject-specific experience


**C.3** **Description of Specialist Pool**


This specialist pool spans key academic domains,
pedagogical expertise, and cross-disciplinary perspectives, enabling flexible and targeted formation
of specialist teams for instructional support.


**Category** **Specialist Pool**


Domain Experts Mathematics; Engineering; Physics;
Chemistry; Biology; Computer Science;
Medicine; Agriculture; Economics; Management; Law; Education; Military Science; History; Literature; Philosophy; Sociology; Language Arts
Pedagogical Pedagogy; Educational Psychology; AsSpecialists sessment and Evaluation; Curriculum Design
Cross- STEM; Humanities; Social Sciences
Disciplinary
Specialists


Table 8: Specialist pool used for pedagogy team formation.







19


**C.4.3** **Prompts for Single-Teacher Instruction**


This prompt guides the teacher agent to generate
instructional feedback based on the student’s pretest answers and reasoning.



question now (just the question, no preamble):

**Student Response Prompt:**

The teacher just asked you: {question} Please re
spond to the teacher’s question thoughtfully.

**Round 2 Prompt:**

The student just responded to your previous question.

Based on their response, ask a follow-up question to

continue guiding them. Ask your follow-up question

now (just the question, no preamble):

**Final Guidance Prompt:**

Now that you’ve had a dialogue with the student,

provide final teaching guidance:

 - Summarize key concepts they should understand

 - Clarify any remaining misconceptions

 - Guide them on how to approach this type of problem

correctly

 - Explain the underlying principles and reasoning

process

 - DO NOT directly state which option/letter is the

correct answer


**C.4.4** **Prompt for Multi-Teacher Instruction**

This prompt guides the teacher agent to generate
instructional feedback based on the student’s pretest answer and reasoning.







20


 - Reasoning: {reasoning}

CORRECT ANSWER: {gold answer (You know this,

but DO NOT reveal it directly)

INDIVIDUAL TEACHER ANALYSES:{analyses

summary}

YOUR COLLABORATIVE TASK:

Based on all the analyses above, work together to

plan specific and targeted questions that will guide the

student to discover the correct answer.

Requirements:

1. Each question should be specific and directly related

to the student’s reasoning

2. DO NOT directly state which option/letter is correct

Return your planned questions in this EXACT format:

ROUND 1: [specific question here]

**Student Response Prompt:**

The teacher just asked you: {question} Please re
spond to the teacher’s question thoughtfully.

**Round 2 - Individual Analysis Prompt**

The student just responded to Round {num}:

Teacher’s Question: {question}

Student’s Response: {response}

Based on your role ({teacher.role}), analyze the

teaching strategy from your perspective. Provide your

analysis in 2-3 sentences.

**Round 2 - Collaborative Planning Prompt:**

You are a team of specialized teachers collaborating to

generate the next question for Round {num + 1.

CONVERSATION HISTORY SO FAR: {history}

STUDENT’S LATEST RESPONSE (Round

{num}):{student response}

INDIVIDUAL TEACHER ANALYSES:{analyses

summary}

YOUR COLLABORATIVE TASK:

Based on all the analyses above, work together to plan

a specific and targeted question for Round {num +

1} that will guide the student to discover the correct

answer

Return your planned questions in this EXACT format:

ROUND 2: [specific question here]

**Final Guidance Prompt:**

Now that you’ve had a dialogue with the student,

provide final teaching guidance:

 - Summarize key concepts they should understand

 - Clarify any remaining misconceptions

 - Guide them on how to approach this type of problem

correctly

 - Explain the underlying principles and reasoning

process

 - DO NOT directly state which option/letter is the

correct answer


**C.4.5** **Prompt for Experience Integration**


This prompt guides the teacher agent to incorporate
retrieved teaching experiences into instruction.







**C.4.6** **Prompt for Teaching Utterance**
**Evaluation**


This prompt guides an expert evaluator agent to
assess a teaching utterance across multiple instructional quality dimensions, including correctness,
information gain, relevance, and clarity.





21


**C.4.7** **Prompts for Experience Summarizer**


This prompt guides an experience summarizer
agent to extract and structure reusable teaching
guidance and strategies from teaching interactions.







22


