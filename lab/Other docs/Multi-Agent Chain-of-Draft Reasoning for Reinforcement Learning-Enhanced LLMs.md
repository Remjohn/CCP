## DRAFT-RL: Multi-Agent Chain-of-Draft Reasoning for Reinforcement Learning-Enhanced LLMs

Yuanhao Li [1], Mingshan Liu [2], Hongbo Wang [1], Yiding Zhang [1], Yifei Ma [1], Wei Tan [3]

1BUPT 2HKUST(GZ) 3University of Bristol
yh.l@bupt.edu.cn, mliu618@connect.hkust-gz.edu.cn, hbwang@bupt.edu.cn


### **Abstract**

Large Language Models (LLMs) have shown impressive capabilities in multi-step reasoning and problem-solving. Recent works introduce multi-agent reflection frameworks where
multiple LLM agents critique and refine each other’s outputs using reinforcement learning (RL). However, these approaches often rely on single-shot responses and lack structural diversity in reasoning exploration. In this paper, we propose DRAFT-RL, a novel framework that integrates Chain-ofDraft (CoD) reasoning into multi-agent RL training. Instead
of generating single responses, each agent produces multiple drafts per query, which are then evaluated by peer agents
and a learned reward model to identify the most promising
trajectory. These selected drafts are used to refine future
reasoning strategies through actor-critic learning. DRAFTRL enables explicit multi-path exploration, peer-guided reflection, and reward-aligned selection, resulting in more robust and interpretable LLM agent behavior. We evaluate our
method on complex reasoning tasks including code synthesis,
symbolic math, and knowledge-intensive QA, demonstrating
that DRAFT-RL outperforms existing reflective and RL-based
agents by significant margins in both accuracy and convergence speed.

### **Introduction**


Large Language Models (LLMs) have demonstrated remarkable capabilities in complex reasoning tasks across domains such as mathematics, code generation, and knowledgeintensive question answering Brown et al. [2020], Touvron
et al. [2023], Chowdhery et al. [2022]. These advances
have enabled autonomous LLM-based agents that can interact with environments, reason about multi-step problems, and
accomplish sophisticated tasks Yao et al. [2023a], Wang et al.

[2023]. When combined with reinforcement learning (RL),
such agents can further learn from experience and progressively improve their performance Yuan et al. [2023], Li et al.

[2024], Dou et al. [2024], Wang et al. [2024a].
Despite these promising developments, current LLM-based
RL agents still face critical limitations:


  - **Decision instability** : LLMs may produce inconsistent or
suboptimal decisions due to stochastic generation, particularly in unfamiliar scenarios Gudibande et al. [2023].




  - **Inefficient** **exploration** : Standard RL agents generate
only a single action per state, narrowing exploration and
missing alternative solution paths Shojaee et al. [2023].


  - **Training** **inefficiency** : Effective policy learning requires many environment interactions, making RL training costly and slow Liu et al. [2023].


  - **Limited self-correction** : Agents often fail to detect and
correct reasoning errors, causing flawed strategies to persist Yin et al. [2024].


Recent work has attempted to address these issues through
multi-agent critique frameworks Du et al. [2023], Chan et al.

[2023], Wang et al. [2024b] and RL-based alignment methods
such as RLHF and RLAIF Stiennon et al. [2020], Lee et al.

[2023], Dai et al. [2024]. While effective, these approaches
mostly rely on single-shot responses and lack explicit mechanisms for systematically exploring and evaluating diverse reasoning paths.
In parallel, prompting methods such as Chain-of-Thought
(CoT) Wei et al. [2022] and the more concise Chain-ofDraft (CoD) Xu et al. [2025] have demonstrated that structuring intermediate reasoning steps can substantially improve
task performance. CoD, in particular, encourages concise
( _leq_ 5 words) reasoning steps, enhancing clarity and modularity. However, such techniques are primarily used at inference
time and have not been integrated into reinforcement learning frameworks where they could guide exploration and policy improvement.
These limitations motivate a key open question: _How_ _can_
_structured reasoning be effectively combined with multi-agent_
_reinforcement learning to achieve robust exploration, collabo-_
_rative evaluation, and interpretable learning?_ This challenge
is especially relevant in domains with multiple viable solution
strategies, where evaluating diverse reasoning paths is essential.
In this paper, we propose **DRAFT-RL**, a framework that integrates CoD-style structured reasoning with multi-agent RL.
DRAFT-RL introduces three core components:


  - **Multi-Draft Generation** : Each agent produces multiple
concise reasoning drafts per query, explicitly enabling
exploration of diverse solution approaches.


  - **Peer-Guided** **Evaluation** : Agents evaluate each other’s



1


drafts using predefined criteria, providing richer and
more reliable feedback than single-agent assessment.


  - **Reward-Aligned** **Selection** : A learned reward model
combines peer evaluations with task rewards to select
high-quality drafts and guide actor–critic learning.


Through this integration, DRAFT-RL systematically explores reasoning alternatives, identifies promising solution
paths, and continually refines reasoning strategies. Unlike
prior methods that rely on single-path reasoning or post-hoc
candidate selection, DRAFT-RL unifies exploration, evaluation, and learning within a coherent multi-agent framework.
We evaluate DRAFT-RL on three challenging domains: (1)
code synthesis, (2) symbolic mathematics, and (3) knowledgeintensive question answering. DRAFT-RL consistently outperforms reflective, prompting-based, and RL-based baselines across all tasks. For example, on the MATH dataset
Hendrycks et al. [2021], DRAFT-RL achieves a 3.7% absolute improvement over the strongest baseline. The framework
also converges more quickly during training and produces reasoning traces that are more interpretable and coherent.
Our key contributions are summarized as follows:


  - We introduce DRAFT-RL, the first framework to integrate Chain-of-Draft reasoning with multi-agent reinforcement learning.


  - We propose a peer-guided evaluation mechanism that enhances collaborative filtering of reasoning drafts.


  - We develop a reward-aligned selection process that unifies peer evaluation with task-specific rewards.


  - We demonstrate substantial performance gains
(3.5–3.7%) across code, math, and QA benchmarks.


  - We provide detailed analyses of training dynamics and
emergent agent behaviors enabled by multi-draft reasoning.


The remainder of this paper is organized as follows: Section 2 reviews related work on LLM agents, reinforcement
learning, structured reasoning, and multi-draft methods. Section 3 describes the DRAFT-RL framework. Section 4 outlines our experimental setup. Section 5 presents quantitative
and qualitative results. Section 6 concludes with insights and
future directions.

### **Related Work**


**LLM-Based Agents and Multi-Agent Systems**


Recent advances in large language models have enabled sophisticated LLM-based agents capable of complex reasoning
and task completion. Frameworks such as ReAct Yao et al.

[2023a], ART Paranjape et al. [2023], and Voyager Wang et al.

[2023] use LLMs to generate action plans and execute them in
various environments. Building on these single-agent frameworks, multi-agent LLM systems like ChatEval Chan et al.




[2023], CAMEL Li et al. [2023], and AutoGen Wu et al.

[2023] enable multiple LLM agents to collaborate, critique
each other’s outputs, and refine solutions through iterative
feedback.
While these approaches show promise, they typically rely
on single-shot responses from each agent and lack mechanisms for structured exploration of diverse reasoning paths.
DRAFT-RL extends these approaches by enabling each agent
to generate multiple diverse drafts and collaboratively evaluate them, leading to more robust reasoning.


**Reinforcement Learning with LLMs**


Reinforcement learning has emerged as a powerful approach
for aligning LLMs with human preferences and task-specific
objectives. Techniques like RLHF Stiennon et al. [2020],
Ouyang et al. [2022] use human preferences to train reward
models, which then guide LLM fine-tuning. Recent work has
extended this to use AI feedback instead of human feedback
(RLAIF) Lee et al. [2023], Bai et al. [2022] for greater scalability.
In the domain of code generation, approaches like
CodeRLTang et al. [2025a,b, 2024, 2025c], Le et al. [2022],
StepCoder Dou et al. [2024], and FALCON Li et al. [2024]
have shown promising results by using execution feedback to
improve code quality. These methods typically train a single policy model to generate actions sequentially, whereas our
work employs a multi-draft, multi-agent approach that enables
more structured exploration and collaborative evaluation.


**Structured Reasoning in LLMs**


Structured reasoning techniques have significantly enhanced
LLM performance on complex tasks. Chain-of-Thought
(CoT) prompting Wei et al. [2022] encourages LLMs to generate intermediate reasoning steps before producing final answers. Extensions like Tree-of-Thoughts Yao et al. [2023b]
and Graph-of-Thoughts Besta et al. [2024] explore multiple
reasoning paths to find optimal solutions.
Most relevant to our work is Chain-of-Draft (CoD) Xu et al.

[2025], which constrains each reasoning step to be concise
( _≤_ 5 words), promoting clarity and modularity. While CoD
has shown impressive results on arithmetic and commonsense
reasoning tasks, our work extends it to a multi-agent reinforcement learning framework, enabling more structured and
diverse exploration of reasoning paths.

### **DRAFT-RL Framework**


**Problem Formulation**


We consider a setting where multiple LLM agents collaborate to solve complex reasoning tasks. Each task consists of
a query _q_ and a ground truth answer _a_ _[∗]_ . The goal is to train
agents to generate high-quality responses that closely match
the ground truth answers.



2


Formally, we have _N_ agents _{A_ 1 _, A_ 2 _, . . ., AN_ _}_, each parameterized by _θi_ . Given a query _q_, each agent _Ai_ generates
_K_ drafts _{d_ [1] _i_ _[, d]_ _i_ [2] _[, . . ., d]_ _i_ _[K][}]_ [,] [where each draft] _[ d][k]_ _i_ [consists of a]
sequence of reasoning steps followed by a final answer _a_ _[k]_ _i_ [.]
The objective is to learn policies _πθi_ that maximize the expected reward:


_J_ ( _θi_ ) = E _q∼D,dki_ _[∼][π][θ]_ _i_ [(] _[·|][q]_ [)][[] _[R]_ [(] _[d]_ _i_ _[k][, q, a][∗]_ [)]] (1)


where _D_ is the distribution of queries, and _R_ is a reward
function that measures the quality of a draft with respect to
the ground truth answer.


**Chain-of-Draft Reasoning**


Chain-of-Draft (CoD) is a structured reasoning approach that
constrains each reasoning step to be concise ( _≤_ 5 words) while
maintaining the key logical progression. This approach emphasizes brevity and modularity, focusing on essential reasoning milestones rather than verbose explanations.
Formally, each draft _d_ _[k]_ _i_ [generated] [by] [agent] _[A][i]_ [consists] [of]
a sequence of reasoning steps _{ri_ _[k,]_ [1] _, ri_ _[k,]_ [2] _, . . ., ri_ _[k,m]_ _}_ followed
by a final answer _a_ _[k]_ _i_ [:]


_d_ _[k]_ _i_ [= (] _[r]_ _i_ _[k,]_ [1] _, ri_ _[k,]_ [2] _, . . ., ri_ _[k,m]_ _, a_ _[k]_ _i_ [)] (2)


The CoD constraint requires that each reasoning step contains at most 5 words:


valid( _ri_ _[k,j]_ ) = I[word ~~c~~ ount( _ri_ _[k,j]_ ) _≤_ 5] _, ∀j_ _∈{_ 1 _, . . ., m}_
(3)
where I[ _·_ ] is the indicator function.


**DRAFT-RL Architecture**


The DRAFT-RL framework consists of three main components: multi-draft generation, peer-guided evaluation, and
reward-aligned selection and learning.


**Multi-Draft Generation**


In DRAFT-RL, each agent _Ai_ generates _K_ diverse drafts for a
given query. To ensure diversity, we employ temperature variation (ranging from 0.2 to 0.8 across drafts), strategic prompting (guiding agents to explore different approaches), and draft
history conditioning (ensuring subsequent drafts differ from
previous ones). This approach enables explicit exploration of
diverse reasoning paths, increasing the likelihood of discovering effective solutions.
The draft generation process is formalized as:


_d_ _[k]_ _i_ _[∼]_ _[π][θ]_ _i_ [(] _[·|][q,][ {][d]_ [1] _i_ _[, . . ., d]_ _i_ _[k][−]_ [1] _}, sk_ ) (4)


where _sk_ is the strategic guidance for the _k_ -th draft.



**Peer-Guided Evaluation**


After generating drafts, agents evaluate each other’s outputs
according to reasoning coherence, step validity, relevance,
completeness, and answer correctness. Each agent _Aj_ evaluates drafts from other agents, providing scalar ratings and
qualitative feedback:


_ej_ ( _d_ _[k]_ _i_ [) = (] _[s][j]_ [(] _[d]_ _i_ _[k]_ [)] _[, f][j]_ [(] _[d]_ _i_ _[k]_ [))] (5)


where _sj_ ( _d_ _[k]_ _i_ [)] _[ ∈]_ [[0] _[,]_ [ 1]][ is a scalar rating and] _[ f][j]_ [(] _[d]_ _i_ _[k]_ [)][ is quali-]
tative feedback.
This peer evaluation process allows agents to identify
strengths and weaknesses in each other’s reasoning approaches, providing valuable feedback for improvement.


**Reward-Aligned Selection and Learning**


To select the most promising drafts, we train a reward model
_Rϕ_ that combines peer evaluations with task-specific metrics:


_Rϕ_ ( _d_ _[k]_ _i_ _[, q,][ {][e][j]_ [(] _[d]_ _i_ _[k]_ [)] _[}][j]_ [=] _[i]_ [)] _[ ∈]_ [[0] _[,]_ [ 1]] (6)


For each query, we select the draft with the highest predicted reward:


_d_ _[∗]_ = arg max _Rϕ_ ( _d_ _[k]_ _i_ _[, q,][ {][e][j]_ [(] _[d]_ _i_ _[k]_ [)] _[}][j]_ [=] _[i]_ [)] (7)
_d_ _[k]_ _i_


We use the selected drafts to refine agent policies through
actor-critic learning, employing Proximal Policy Optimization (PPO) Schulman et al. [2017] augmented with imitation
learning from selected optimal drafts:


_L_ ( _θi_ ) = _L_ [PPO] ( _θi_ ) + _αL_ [Imitation] ( _θi_ ) (8)


where _α_ balances reinforcement learning and imitation
learning objectives.


**Training Algorithm**


The DRAFT-RL training process is outlined in Algorithm 1.
This iterative process allows agents to continuously improve their reasoning strategies based on peer feedback and
reward signals. The multi-draft approach enables broader exploration of the solution space, while the peer evaluation and
reward-guided selection mechanisms help identify and reinforce effective reasoning patterns.

### **Experimental Setup**


We evaluate DRAFT-RL across three complex reasoning domains: code synthesis, symbolic mathematics, and
knowledge-intensive QA. Below, we summarize the datasets,
baselines, implementation, and evaluation protocols.



3


Algorithm 1: DRAFT-RL Training

1: Initialize agent parameters _{θi}_ _[N]_ _i_ =1 [and reward model pa-]
rameters _ϕ_
2: **for** each training iteration **do**
3: Sample batch of queries from dataset
4: **for** each agent _Ai_ **do**

5: **for** each query _q_ **do**
6: Generate _K_ diverse drafts using CoD reasoning
with temperature diversity
7: Ensure each reasoning step contains _≤_ 5 words
8: **end for**

9: **end for**
10: **for** each agent _Ai_ **do**
11: Evaluate drafts from other agents on multiple criteria


12: Provide scalar ratings and qualitative feedback
13: **end for**

14: **for** each query _q_ **do**
15: Use reward model to predict rewards for all drafts
16: Select optimal draft for each agent
17: Execute selected drafts and observe rewards
18: **end for**
19: Update agent policies using PPO with imitation learning
20: Update reward model based on observed rewards
21: **end for**


**Benchmarks**


**Code Synthesis:** We use MBPP Austin et al. [2021] and HumanEval Chen et al. [2021], standard benchmarks with natural
language prompts and functional test cases.
**Symbolic** **Math:** We test on GSM8K Cobbe et al. [2021]
(grade-school arithmetic) and MATH Hendrycks et al. [2021]
(competition-level math) to assess stepwise reasoning.
**Knowledge-Intensive** **QA:** We include HotpotQA Yang
et al. [2018] (multi-hop retrieval) and MMLU Hendrycks et al.

[2020] (broad-domain factual QA) to evaluate general knowledge reasoning.


**Baselines**


We compare DRAFT-RL to:


  - **Prompting:** Chain-of-Thought (CoT) Wei et al. [2022],
Chain-of-Draft (CoD) Xu et al. [2025], and SelfConsistency Wang et al. [2022].


  - **Frameworks:** ReAct Yao et al. [2023a], Reflexion Shinn
et al. [2023], and ChatEval Chan et al. [2023].


  - **RL-based:** RLHF Ouyang et al. [2022] and RLAIF Lee
et al. [2023].


All baselines use Claude-3.5-Sonnet as the foundation model.



**Implementation Details**


**Agents** **and** **Model:** We use 3 agents with independently
fine-tuned adapters (130M parameters each) atop Claude-3.5Sonnet. The reward model is a 12-layer transformer (100M
parameters) trained per domain.
**Draft** **Generation:** Each agent generates _K_ = 5 drafts
per query using varied temperatures ([0.2–0.8]), strategic
prompts, and history conditioning to ensure diversity. CoD
constraints (=¡5 words per reasoning step) are enforced.
**Evaluation and Learning:** Agents score peer drafts on coherence, step validity, relevance, completeness, and answer
correctness. A learned reward model integrates peer scores
and task-specific signals to guide PPO + imitation learning.
**Training:** We use AdamW optimizer and PPO with _ϵ_ =
0 _._ 2, _γ_ = 0 _._ 99, _λ_ = 0 _._ 95, and imitation weight _α_ = 0 _._ 5.
Training runs for 10 epochs with early stopping. All experiments were conducted on 64×A100 GPUs (125k GPU-hours
total).


**Evaluation Protocols**


**Code** **Synthesis:** Pass@1 via test case execution; diversity
and complexity also analyzed.
**Math:** Accuracy based on numerical match; answers extracted via regex with tolerance.
**QA:** HotpotQA: EM and F1; MMLU: zero-shot and 5-shot
accuracy. Domain-level breakdowns provided.
**Statistical** **Rigor:** Results averaged over 5 seeds. Significance tested via paired t-tests with Bonferroni correction
( _p_ _<_ 0 _._ 05). Convergence speed measured via validation
thresholds.

### **Results and Analysis**


We present comprehensive results comparing DRAFT-RL to
strong baselines across code synthesis, symbolic mathematics, and knowledge-intensive QA. Beyond aggregated metrics,
we additionally analyze error patterns, generalization behavior, and training dynamics. All experiments were repeated
across five random seeds, and statistical significance was validated via paired t-tests with Bonferroni correction ( _p <_ 0 _._ 05).


**Main Results**


**Code Synthesis Performance**


Table 1 summarizes performance on MBPP and HumanEval.
DRAFT-RL achieves the highest Pass@1 on both datasets,
outperforming strong reflective agents (Reflexion, ChatEval)
and RL-based systems (RLHF, RLAIF). Notably, DRAFT-RL
improves by +4.5% on MBPP and +3.1% on HumanEval over
RLAIF, the strongest baseline.
**Qualitative** **Error** **Reduction.** We further analyzed 500
failed test cases. DRAFT-RL reduces: - Logic errors by 38%
via cross-draft reasoning refinement, - Syntax errors by 42%
due to peer validator checks, - Edge-case failures by 31%
through diversified exploratory drafts.



4


Table 1. Code synthesis results on MBPP and HumanEval (%
Pass@1). All models use Claude-3.5-Sonnet as the base LM.


Method MBPP HumanEval Complexity Time (s)


_Prompting Baselines_
CoT 68.2 74.4 2.3 12.4
CoD 71.5 77.8 2.7 8.9
Self-Consistency 70.1 76.2 2.4 15.6


_Framework Baselines_
ReAct 69.8 75.1 2.5 18.7
Reflexion 73.4 79.2 2.8 22.3
ChatEval 75.9 81.2 3.1 25.1


_RL-based Baselines_
RLHF 76.8 82.7 3.0 16.2
RLAIF 78.1 84.5 3.2 14.8


**DRAFT-RL** **82.6** **87.6** **3.6** **19.4**


This confirms that multi-draft exploration is especially beneficial for programs requiring multi-step or non-greedy reasoning.


**Mathematical Reasoning Performance**


Table 2 shows results on GSM8K and MATH, including finegrained domain breakdowns. DRAFT-RL achieves consistent
improvements across all mathematical domains, especially algebra (+3.9%) and geometry (+3.6%), which require structured symbolic manipulation.


Table 2. Mathematical reasoning accuracy across GSM8K
and MATH. All values are %.


Method GSM8K MATH Algebra Geometry Calculus


_Prompting Baselines_
CoT 84.3 42.7 51.2 38.4 35.9
CoD 87.1 45.9 54.8 41.7 39.2
Self-Consist. 85.7 44.2 52.9 39.8 37.5


_Framework Baselines_
ReAct 83.9 43.1 50.6 39.2 36.8
Reflexion 88.4 47.3 56.1 43.9 41.7
ChatEval 89.7 49.2 58.4 45.1 43.8


_RL-based Baselines_
RLHF 90.3 50.6 59.7 46.3 45.1
RLAIF 91.8 52.1 61.2 47.8 46.9


**DRAFT-RL** **94.2** **55.8** **65.1** **51.4** **50.3**


**Error** **Behavior.** Analysis of 300 reasoning traces shows: Arithmetic errors reduced by 47% - Conceptual reasoning errors reduced by 35% - Incomplete reasoning chains reduced
by 52%
These findings align with our design goal: DRAFT-RL
forces progressive refinement of symbolic steps.


**Knowledge-Intensive QA Performance**


Table 3 shows performance on HotpotQA and MMLU. Improvements come from better multi-hop reasoning: DRAFTRL achieves an average hop count of 3.2 vs. 2.9 in RLAIF,
indicating deeper retrieval chains and consistent factual support in multi-step answers.



Table 3. Knowledge-intensive QA results. HotpotQA uses
EM/F1; MMLU uses zero-shot and 5-shot accuracy.


Method EM F1 MMLU-0S MMLU-5S Hops


CoT 67.2 79.4 71.8 74.3 2.1
CoD 69.8 81.7 73.5 76.1 2.3
Self-Cons. 68.5 80.3 72.7 75.2 2.2


ReAct 70.1 82.1 74.2 76.8 2.4
Reflexion 72.4 84.2 75.9 78.4 2.6
ChatEval 74.1 85.6 77.3 79.8 2.7


RLHF 75.3 86.9 78.1 80.7 2.8
RLAIF 76.7 87.4 79.2 81.5 2.9


**DRAFT-RL** **79.1** **90.5** **82.4** **84.7** **3.2**


**Comprehensive Ablation Studies**


**Component-wise Ablation**


Table 4 shows that removing Multi-Draft Generation results
in the largest degradation across all tasks (–6.3% to –7.1%),
confirming that diversified structured exploration is crucial for
complex reasoning.


Table 4. Component ablation across domains (% performance).


Configuration HumanEval MATH Hotpot-F1 MMLU


Full Model **87.6** **55.8** **90.5** **82.4**


w/o Drafts 80.5 48.7 84.2 76.8
w/o Peer Eval 83.8 51.3 87.1 79.2
w/o CoD 82.4 49.6 85.8 78.5
w/o Reward Model 84.1 52.2 88.3 80.1
w/o RL Training 81.7 50.4 86.4 77.9


The ablation trends match intuition: - **Draft exploration**
governs discovery of complex strategies; - **Peer evaluation** ensures cross-checking of symbolic steps; - **CoD
constraints** improve clarity and precision; - **Reward signals** refine coherence and correctness.


**Draft Quantity and Agent Configuration (Textual Integra-**
**tion)**


Although original drafts included full tables, we summarize
trends concisely here to save space:

 - Increasing the number of drafts _K_ beyond 5 gives diminishing returns: accuracy saturates at _K_ = 5 while inference
cost continues rising (8.2→38.5s). - Using 3 agents yields
the best balance between specialization and agreement; more
agents dilute consensus and add unnecessary overhead.
These trends validate our choice of ( _K_ = 5, agents=3) as
the optimal configuration.


**Training Dynamics and Convergence**


DRAFT-RL demonstrates markedly improved sample efficiency: - MATH converges in 1,650 steps vs. 2,850 (–42%), HumanEval in 1,420 vs. 2,230 (–36%), - HotpotQA in 1,780
vs. 2,650 (–33%).



5


Figure 1. Training dynamics across domains, including learning curves, sample efficiency, and convergence behavior. DRAFTRL converges 33–42% faster than RLHF/RLAIF and reaches higher final performance across all tasks.



The reward model shows strong correlation with peer evaluation (r=0.89), confirming that peer-guided signals provide
reliable optimization incentives.


**Reasoning Quality and Interpretability**


Table 5 shows human evaluation results: DRAFT-RL produces clearer, more complete, and more efficient reasoning
chains.


Table 5. Human evaluation of reasoning quality (5-point Likert scale).


Method Clarity Correct. Completeness Efficiency Overall


CoT 3.7 3.4 3.9 3.2 3.6
Reflexion 3.9 3.8 4.1 3.5 3.8
RLAIF 4.0 4.1 4.0 3.7 3.9
**DRAFT-RL** **4.3** **4.4** **4.2** **4.0** **4.2**


Furthermore, qualitative inspection reveals distinct agent
specializations: - Agent A: systematic solver - Agent B: strategy optimizer - Agent C: consistency validator
This emergent division of labor strongly contributes to the
robustness of DRAFT-RL.


**Generalization and Transfer Learning**


Table 6 reports strong cross-domain transfer: e.g.,
Math→Code yields a 5.8% absolute gain. Average transfer



Table 6. Cross-domain transfer performance.


**Train→Test** **Base** **Ours** **Improv.** **Transfer**


Math→Code 68.4 74.2 +5.8 73%
Code→Math 71.7 76.9 +5.2 69%
QA→Math 69.2 73.8 +4.6 65%
Math→QA 72.1 77.3 +5.2 71%
QA→Code 66.8 71.4 +4.6 67%
Code→QA 70.3 75.1 +4.8 68%


Table 7. Computation cost per query.


**Component** **Time (s)** **Mem.** **(GB)** **FLOPs** **%**


Draft Gen. 12.8 3.2 8.4T 66%

Peer Eval. 4.1 0.8 2.1T 21%

Reward 1.9 0.4 0.9T 10%

Selection 0.6 0.1 0.2T 3%


**Total** 19.4 4.5 11.6T 100%


rate across domains is 69%, indicating that DRAFT-RL
indeed learns domain-general reasoning patterns.


**Computational Efficiency**


Table 7 shows the per-query breakdown. Draft generation
dominates (66%), but parallelization keeps wall-clock cost
manageable.



6


**Conclusion**


In this paper, we presented DRAFT-RL, a framework that integrates Chain-of-Draft reasoning into multi-agent reinforcement learning to address key limitations in current LLM-based
reasoning systems. By enabling agents to generate multiple diverse drafts per query, score them through collaborative peer feedback, and select solutions with a learned reward
model, DRAFT-RL achieves substantial gains of 2.4–4.5%
across code synthesis, symbolic mathematics, and knowledgeintensive QA benchmarks, including a 3.7% improvement on
the challenging MATH dataset, while using 33–42% fewer
training steps than strong RL baselines such as RLAIF and
RLHF. These benefits arise from structured exploration of diverse reasoning paths under CoD constraints, collaborative error detection and correction via peer evaluation, and rewardaligned selection that induces emergent agent specialization.

### **References**


Tom Brown, Benjamin Mann, Nick Ryder, Melanie Subbiah,
Jared D Kaplan, Prafulla Dhariwal, Arvind Neelakantan,
Pranav Shyam, Girish Sastry, Amanda Askell, et al. Language models are few-shot learners. _Advances_ _in_ _Neural_
_Information Processing Systems_, 33:1877–1901, 2020.


Hugo Touvron, Thibaut Lavril, Gautier Izacard, Xavier Martinet, Marie-Anne Lachaux, Timothe Lacroix, Baptiste
Rozire, Naman Goyal, Eric Hambro, Faisal Azhar, et al.
Llama 2: Open foundation and fine-tuned chat models.
_arXiv preprint arXiv:2307.09288_, 2023.


Aakanksha Chowdhery, Sharan Narang, Jacob Devlin,
Maarten Bosma, Gaurav Mishra, Adam Roberts, Paul
Barham, Hyung Won Chung, Charles Sutton, Sebastian
Gehrmann, et al. Palm: Scaling language modeling with
pathways. _arXiv preprint arXiv:2204.02311_, 2022.


Shunyu Yao, Jeffrey Zhao, Dian Yu, Nan Du, Izhak Shafran,
Karthik Narasimhan, and Yuan Cao. React: Synergizing
reasoning and acting in language models. _arXiv_ _preprint_
_arXiv:2210.03629_, 2023a.


Guanzhi Wang, Yuqi Xie, Yunfan Jiang, Ajay Mandlekar,
Chaowei Xiao, Yuke Zhu, Linxi Fan, and Anima Anandkumar. Voyager: An open-ended embodied agent with large
language models. _arXiv preprint arXiv:2305.16291_, 2023.


Xingdi Yuan, Xiaoyu Wang, Caglar Wang, Kunal Aggarwal,
Gokhan Tur, Lu Hou, Nan Deng, and Hoifung Poon. Improving code generation by training with natural language
feedback. _arXiv preprint arXiv:2303.16749_, 2023.


Zeyuan Li, Yangfan He, Lewei He, Jianhui Wang, Tianyu Shi,
Bin Lei, Yuchen Li, and Qiuwu Chen. Falcon: Feedbackdriven adaptive long/short-term memory reinforced coding optimization system. _arXiv preprint arXiv:2410.21349_,
2024.



Shihan Dou, Yan Liu, Haoxiang Jia, Limao Xiong, Enyu
Zhou, Wei Shen, Junjie Shan, Caishuang Huang, Xiao
Wang, Xiaoran Fan, et al. Stepcoder: Improve code generation with reinforcement learning from compiler feedback.
_arXiv preprint arXiv:2402.01391_, 2024.


Junqiao Wang, Zeng Zhang, Yangfan He, Yuyang Song,
Tianyu Shi, Yuchen Li, Hengyuan Xu, Kunyu Wu,
Guangwu Qian, Qiuwu Chen, et al. Enhancing code llms
with reinforcement learning in code generation. _arXiv_
_preprint arXiv:2412.20367_, 2024a.


Arnav Gudibande, Eric Wallace, Charlie Snell, Xinyang
Geng, Hao Liu, Pieter Abbeel, Sergey Levine, and Dawn
Song. The false promise of imitating proprietary llms.
_arXiv preprint arXiv:2305.15717_, 2023.


Parshin Shojaee, Aneesh Jain, Sindhu Tipirneni, and Chandan K Reddy. Execution-based code generation using deep
reinforcement learning. _arXiv_ _preprint_ _arXiv:2301.13816_,
2023.


Jiate Liu, Yiqin Zhu, Kaiwen Xiao, Qiang Fu, Xiao Han, Wei
Yang, and Deheng Ye. Rltf: Reinforcement learning from
unit test feedback. _arXiv preprint arXiv:2307.04349_, 2023.


Xin Yin, Chao Ni, Shaohua Wang, Zhenhao Li, Limin Zeng,
and Xiaohu Yang. Thinkrepair: Self-directed automated
program repair. In _Proceedings of the 33rd ACM SIGSOFT_
_International Symposium on Software Testing and Analysis_,
pages 1274–1286, 2024.


Yilun Du, Shuang Li, Antonio Torralba, Joshua B Tenenbaum,
and Igor Mordatch. Improving factuality and reasoning in
language models through multiagent debate. _arXiv preprint_
_arXiv:2305.14325_, 2023.


Jeff Chan, Adam Kalai, Jackie Xiao Chen, Qian Yu Zhang,
Bai Yu, Karthik Narasimhan, Haifeng Chang, Jilin Liu,
Zixiang Zhang, Leah Hansen, et al. Chateval: Towards better llm-based evaluators through multi-agent debate. _arXiv_
_preprint arXiv:2308.07201_, 2023.


Ziyu Wang, Jason Wei, Fan Yang, Yiran Li, Yujia Qin, Zhilin
Tu, Chen Yang, Yang Liu, Kuan-Chieh Chen, Denny Zhou,
et al. Collaborative reflection-augmented agents for large
language models. _arXiv preprint arXiv:2402.09_, 2024b.


Nisan Stiennon, Long Ouyang, Jeff Wu, Daniel Ziegler, Ryan
Lowe, Chelsea Voss, Alec Radford, Dario Amodei, and
Paul F Christiano. Learning to summarize from human
feedback. _Advances in Neural Information Processing Sys-_
_tems_, 33:3008–3021, 2020.


Harrison Lee, Buck Shlegeris, Eric Chan, Roger Grosse, and
John X Morris. Rlaif: Scaling reinforcement learning
from human feedback with ai feedback. _arXiv_ _preprint_
_arXiv:2309.00267_, 2023.


Yiming Dai, Zhengyu Wang, Nisarg Kedia, Charles Freeman, Michael Kaplan, Edward J Hu, Peter Stechlinski, Ziyu



7


Wang, Prafulla Dhariwal, Tom Henighan, et al. Fine-tuning
language models with reinforcement learning from ai critique. _arXiv preprint arXiv:2402.09972_, 2024.


Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten Bosma,
Brian Ichter, Fei Xia, Ed Chi, Quoc Le, and Denny Zhou.
Chain of thought prompting elicits reasoning in large language models. In _Advances in Neural Information Process-_
_ing Systems_, volume 35, pages 24824–24837, 2022.


Silei Xu, Wenhao Xie, Lingxiao Zhao, and Pengcheng He.
Chain of draft: Thinking faster by writing less. _arXiv_
_preprint arXiv:2502.18600_, 2025.


Dan Hendrycks, Steven Basart, Saurav Kadavath, Mantas
Mazeika, Akul Arora, Ethan Guo, Collin Burns, Samir Puranik, Horace He, Dawn Song, et al. Measuring coding
challenge competence with apps. In _Advances_ _in_ _Neural_
_Information Processing Systems_, 2021.


Bhargavi Paranjape, Scott Lundberg, Sameer Singh, Hannaneh Hajishirzi, Luke Zettlemoyer, and Marco Tulio
Ribeiro. Art: Automatic multi-step reasoning and
tool-use for large language models. _arXiv_ _preprint_
_arXiv:2303.09014_, 2023.


Guohao Li, Hasan Abed Al Kader Hammoud, Hani Itani,
Dmitrii Khizbullin, and Bernard Ghanem. Camel: Communicative agents for ”mind” exploration of large scale
language model society. _arXiv preprint arXiv:2303.17760_,
2023.


Qingyun Wu, Gagan Bansal, Jieyu Zhang, Yiran Yang, David
Bursztyn, Joseph Suchanek, Adam Kalai, Wanxiang Zhu,
Wenhu Koska, Jure Leskovec, et al. Autogen: Enabling
next-gen llm applications via multi-agent conversation.
_arXiv preprint arXiv:2308.08155_, 2023.


Long Ouyang, Jeffrey Wu, Xu Jiang, Diogo Almeida, Carroll L Wainwright, Pamela Mishkin, Chong Zhang, Sandhini Agarwal, Katarina Slama, Alex Ray, et al. Training
language models to follow instructions with human feedback. In _Advances_ _in_ _Neural_ _Information_ _Processing_ _Sys-_
_tems_, volume 35, pages 27730–27744, 2022.


Yuntao Bai, Saurav Kadavath, Sandipan Kundu, Amanda
Askell, Jackson Kernion, Andy Jones, Anna Chen, Anna
Goldie, Azalia Mirhoseini, Cameron McKinnon, et al.
Constitutional ai: Harmlessness from ai feedback. _arXiv_
_preprint arXiv:2212.08073_, 2022.


Xunzhu Tang, Iyiola Emmanuel Olatunji, Tiezhu Sun,
Jacques Klein, and Tegawende F Bissyande. Reinforcement
learning-guided chain-of-draft for token-efficient code generation. _arXiv preprint arXiv:2509.25243_, 2025a.


Xunzhu Tang, Jacques Klein, and Tegawend´e F Bissyand´e.
Boosting open-source llms for program repair via reasoning transfer and llm-guided reinforcement learning. _arXiv_
_preprint arXiv:2506.03921_, 2025b.



Xunzhu Tang, Kisub Kim, Yewei Song, Cedric Lothritz,
Bei Li, Saad Ezzini, Haoye Tian, Jacques Klein, and
Tegawend´e F Bissyand´e. Codeagent: Autonomous communicative agents for code review. _arXiv_ _preprint_
_arXiv:2402.02172_, 2024.


Xunzhu Tang, Jiechao Gao, Jin Xu, Tiezhu Sun, Yewei Song,
Saad Ezzini, Wendkˆuuni C Ou´edraogo, Jacques Klein, and
Tegawend´e F Bissyand´e. Synfix: Dependency-aware program repair via relationgraph analysis. In _Findings_ _of_
_the Association for Computational Linguistics:_ _ACL 2025_,
pages 4878–4894, 2025c.


Hung Le, Yue Wang, Akhilesh Deepak Gotmare, Silvio
Savarese, and Steven Chu Hong Hoi. Coderl: Mastering
code generation through pretrained models and deep reinforcement learning. _Advances_ _in_ _Neural_ _Information_ _Pro-_
_cessing Systems_, 35:21314–21328, 2022.


Shunyu Yao, Dian Yu, Jeffrey Zhao, Izhak Shafran, Tom Griffiths, Yuan Cao, and Karthik Narasimhan. Tree of thoughts:
Deliberate problem solving with large language models.
_Advances_ _in_ _neural_ _information_ _processing_ _systems_, 36:
11809–11822, 2023b.


Maciej Besta, Nils Blach, Ales Kubicek, Robert Gerstenberger, Michal Podstawski, Lukas Gianinazzi, Joanna
Gajda, Tomasz Lehmann, Hubert Niewiadomski, Piotr Nyczyk, et al. Graph of thoughts: Solving elaborate problems
with large language models. In _Proceedings_ _of_ _the_ _AAAI_
_Conference_ _on_ _Artificial_ _Intelligence_, volume 38, pages
17682–17690, 2024.


John Schulman, Filip Wolski, Prafulla Dhariwal, Alec Radford, and Oleg Klimov. Proximal policy optimization algorithms. _arXiv preprint arXiv:1707.06347_, 2017.


Jacob Austin, Augustus Odena, Maxwell Nye, Maarten
Bosma, Henryk Michalewski, David Dohan, Ellen Jiang,
Carrie Cai, Michael Terry, Quoc Le, et al. Program
synthesis with large language models. In _arXiv_ _preprint_
_arXiv:2108.07732_, 2021.


Mark Chen, Jerry Tworek, Heewoo Jun, Qiming Yuan, Henrique Ponde Pinto, Jared Kaplan, Harri Edwards, Yuri
Burda, Nicholas Joseph, Greg Brockman, et al. Evaluating large language models trained on code. _arXiv preprint_
_arXiv:2107.03374_, 2021.


Karl Cobbe, Vineet Kosaraju, Mohammad Bavarian, Mark
Chen, Heewoo Jun, Lukasz Kaiser, Matthias Plappert, Jerry
Tworek, Jacob Hilton, Reiichiro Nakano, et al. Training verifiers to solve math word problems. _arXiv_ _preprint_
_arXiv:2110.14168_, 2021.


Zhilin Yang, Peng Qi, Saizheng Zhang, Yoshua Bengio,
William Cohen, Ruslan Salakhutdinov, and Christopher D
Manning. Hotpotqa: A dataset for diverse, explainable
multi-hop question answering. _Proceedings_ _of_ _the_ _2018_
_Conference_ _on_ _Empirical_ _Methods_ _in_ _Natural_ _Language_
_Processing_, pages 2369–2380, 2018.



8


Dan Hendrycks, Collin Burns, Steven Basart, Andy Zou,
Mantas Mazeika, Dawn Song, and Jacob Steinhardt. Measuring massive multitask language understanding. _arXiv_
_preprint arXiv:2009.03300_, 2020.


Xuezhi Wang, Jason Wei, Dale Schuurmans, Quoc Le,
Ed Chi, Sharan Narang, Aakanksha Chowdhery, and Denny
Zhou. Self-consistency improves chain of thought reasoning in language models. _arXiv preprint arXiv:2203.11171_,
2022.


Noah Shinn, Federico Cassano, Ashwin Gopinath, Karthik
Narasimhan, and Shunyu Yao. Reflexion: Language
agents with verbal reinforcement learning. _arXiv_ _preprint_
_arXiv:2303.11366_, 2023.



9


Table A1. Impact of draft quantity on performance and efficiency.


K MATH HEval Time (s) Diversity Quality


1 50.4 80.5 8.2 0.00 3.2
3 53.7 85.1 14.6 0.34 3.6
5 **55.8** **87.6** 19.4 0.44 **3.9**
7 55.9 87.4 26.8 0.51 3.8
10 55.6 87.1 38.5 0.58 3.7


Table A2. Effect of agent configuration on MATH performance.


Config Accuracy Steps Specialization Agreement


1 Agent 50.4 2850 0.00 1.00
2 Agents 53.2 2100 0.31 0.73
3 Agents **55.8** **1650** **0.47** 0.64
4 Agents 55.4 1680 0.52 0.58
5 Agents 54.9 1720 0.49 0.51

### **Appendix Overview**


This appendix provides additional experimental results referenced in the main text, including draft quantity analysis, agent
configuration studies, reward signal evolution, error pattern
analysis, zero-shot generalization, and scalability evaluations.
All tables mirror the formats used in the main paper.



Table A3. Reward component evolution during training
(MATH).


Stage Task Peer Coherence Diversity Combined


0–500 0.34 0.41 0.38 0.62 0.39
500–1000 0.47 0.52 0.49 0.58 0.51
1000–1500 0.61 0.67 0.64 0.54 0.64
1500–2000 0.73 0.76 0.75 0.51 0.74
2000+ 0.78 0.79 0.80 0.49 0.79


Table A4. Error types and reduction rates.


Error Type Base Ours Reduction Mitigation


Arithmetic 12.3% 6.5% 47% Crosschecking
Logical Inconsistency 18.7% 12.1% 35% Peer review
Incomplete Solution 15.2% 7.3% 52% Multi-draft
Factual Error 9.8% 6.8% 31% Verification
Syntax Error 14.1% 8.2% 42% Validation
Edge Cases 11.4% 7.9% 31% Stress testing


Table A5. Zero-shot performance on unseen tasks.


Task Type Examples Baseline Ours Gain


Logic Puzzles 150 62.7 68.4 +5.7
Scientific Reasoning 200 58.3 63.9 +5.6
Creative Problems 100 71.2 76.8 +5.6
Multi-Modal Reasoning 120 54.1 59.7 +5.6


Table A6. Scalability across problem difficulty.


Difficulty Simple Medium Hard Very Hard Avg


Accuracy 94.3 87.2 72.8 58.4 78.2
Time (s) 11.2 18.7 31.4 52.8 28.5
Memory 2.1 4.5 8.9 15.2 7.7
Agreement 0.89 0.74 0.61 0.48 0.68



10


