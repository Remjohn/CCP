## **Inference-Time Computations for LLM Reasoning and** **Planning: A Benchmark and Insights**

**Shubham Parashar** _**[∗]**_ **Blake Olson** _[∗]_ **Sambhav Khurana** _[∗]_ **Eric Li** _[∗]_ **Hongyi Ling**
**James Caverlee** **Shuiwang Ji**


Department of Computer Science & Engineering
Texas A&M University


**Abstract**


We examine the reasoning and planning capabilities of large language models
(LLMs) in solving complex tasks. Recent advances in inference-time techniques
demonstrate the potential to enhance LLM reasoning without additional training
by exploring intermediate steps during inference. Notably, OpenAI’s o1 model
shows promising performance through its novel use of multi-step reasoning and
verification. Here, we explore how scaling inference-time techniques can improve reasoning and planning, focusing on understanding the tradeoff between
computational cost and performance. To this end, we construct a comprehensive
benchmark, known as _Sys2Bench_, and perform extensive experiments evaluating
existing inference-time techniques on eleven diverse tasks across five categories,
including arithmetic reasoning, logical reasoning, common sense reasoning, algorithmic reasoning, and planning. Our findings indicate that simply scaling
inference-time computation has limitations, as no single inference-time technique
consistently performs well across all reasoning and planning tasks.


**1** **Introduction**


Large language models (LLMs) [Brown et al., 2020] have demonstrated exceptional performance
across a range of natural language processing (NLP) tasks, including question answering, machine
translation, sentiment analysis, and text summarization [Devlin et al., 2019, Vaswani et al., 2017].
Beyond NLP, LLMs have also been adapted for multimodal tasks involving vision [Parashar et al.,
2024, Lin et al., 2025] and audio [Wu et al., 2024]. Building on their success in these diverse
domains, researchers are increasingly using LLMs as AI agents [Deng et al., 2024, Wang et al., 2024]
for complex tasks, such as robotics [Liu et al., 2023] and scientific discovery [Wang et al., 2024].
These tasks require the reasoning and planning capabilities of LLMs, extending beyond simpler text
comprehension.


Reasoning and planning in LLMs refer to their ability to solve complex problems by understanding,
processing, and generating solutions across various domains [Hao et al., 2024]. These capabilities
can be analyzed from multiple perspectives; we propose a classification that organizes reasoning
and planning tasks into five categories, namely arithmetic, logical, commonsense, algorithmic, and
plan generation challenges. Recent advances in inference-time techniques demonstrate the potential
to enhance LLM reasoning and planning without additional training. These techniques focus on
decomposing complex problems into simpler intermediate steps during inference. For instance,
Chain-of-Thought [Wei et al., 2022] encourages step-by-step reasoning, while Tree-of-Thought [Yao
et al., 2024] chooses optimal reasoning paths using tree search. Notably, OpenAI’s O1 model, a
large reasoning model (LRM) [Valmeekam et al., 2024], achieves state-of-the-art performance on


_∗_ [Co-first authors; Project page at https://github.com/divelab/sys2bench.](https://github.com/divelab/sys2bench)


Preprint. Under review.


Table 1: Summary of the 11 datasets included in Sys2Bench.


Algorithmic Reasoning Planning


Game of 24 Binpacking Blocksworld Trip Plan Calendar Plan Rubik’s Cube


Propose an arithmetic Pack items into the Plan actions to transform Plan a trip across cities Schedule a meeting considering Unscramble a scrambled
Task expression to reach 24. fewest bins. blocks from initial to goal state. for a set number of days. time constraints of people. 2×2 Rubik’s Cube.


List of item weights Initial state of blocks Cities, days per city, total Calendars with meetings and A scrambled 2×2 Rubik’s
Input A list of 4 numbers. and bin capacity. and goal state. days, and possible flights. time constraints. Cube.


Final list with items A sequence of actions A meeting time fitting all A sequence of rotations
Output [An arithmetic] expression. arranged in bins. as the plan. A trip itinerary. schedules. that unscramble the cube.


Arithmetic Reasoning Logical Reasoning Common Sense Reasoning


GSM8K AQuA ProntoQA StrategyQA HotPotQA


Solve high school Solve algebraic Draw a logical conclusion Answer general knowledge Answer general knowledge
Task arithmetic problems. problems. from a set of predicates. questions. questions using provided facts.


Arithmetic problem Algebraic problem A clause to verify as true or General knowledge question
Input description. description. false using logical predicates. A yes/no question. with supporting facts.


Output A numerical value. A multiple-choice option. True or False, with reasoning. Yes or No. Short answer of 1 or 2 words.


various reasoning tasks, demonstrating the effectiveness of inference-time techniques. This success
has inspired the research community to focus more on scaling inference-time techniques in the hope
of similar performance improvements.


Although inference time techniques have improved LLM reasoning and planning, evaluation of
these methods has been limited to specific tasks, models, and datasets. Moreover, these methods
have additional computational costs, presenting a trade-off between computational overhead and
performance gains. To overcome this limitation we introduce Sys2Bench, a comprehensive benchmark
covering multiple tasks and models. Specifically, we perform experiments on eleven datasets and
seven different LLMs, testing four widely used inference-time techniques. Based on our findings, we
argue that simply scaling inference-time computation has limitations. Instead, we need to explore
diverse approaches to enhance the holistic reasoning capabilities of LLMs, as no single inference-time
technique consistently outperforms others across all tasks.


**2** **Related Work**


**LLM Reasoning** is the ability of LLMs to logically process information and draw coherent conclusions, enabling them to solve complex problems [Saparov and He, 2023]. The success of LLMs in
Natural Language Generation [Radford et al., 2018] and Natural Language Understanding [Vaswani
et al., 2017, Devlin et al., 2019] has sparked interest in exploring reasoning capabilities. A range of
datasets have been introduced to evaluate reasoning, covering tasks in arithmetic [Ling et al., 2017,
Cobbe et al., 2021], logic [Chollet, 2019, Wang et al., 2022], common sense [Yang et al., 2018, Geva
et al., 2021], and algorithmic reasoning [Yao et al., 2024]. We introduce these tasks in more detail in
Section 3, and report results across these tasks in Section 5.


**LLM Planning** involves constructing a sequence of actions to achieve defined goals [Valmeekam
et al., 2023, Zheng et al., 2024]. LLMs have been employed as planners or high-level controllers for
robotic tasks Liu et al. [2023], Huang et al. [2022] and as agents for web navigation [Deng et al.,
2024], scientific discovery [Wang et al., 2024], and autonomous vehicles [Yang et al., 2023]. Despite
their broad adoption, studies reveal that LLMs often struggle to generate valid plans for complex
tasks [Kambhampati et al., 2024, Xie et al., 2024]. We provide details on evaluated planning problems
in Section 3, with results and analyses in Section 5.


**Inference Time Techniques** for LLMs are methods applied during output generation to improve
performance, and alignment with downstream tasks [Welleck et al., 2024]. These techniques aid
reasoning and planning by breaking complex tasks into smaller, manageable steps for systematic
problem-solving. For instance, Chain-of-Thought prompting (CoT) [Wei et al., 2022] and its variants [Zhou et al., 2023, Kojima et al., 2022] decompose problems into sequential steps, while
self-consistency [Wang et al., 2023] refines CoT by aggregating multiple responses through voting.
Tree of Thought [Yao et al., 2024], Graph of Thought [Besta et al., 2024], and Monte Carlo Tree
Search [Hao et al., 2023, Zhou et al., 2024] enhance problem-solving by systematically exploring
reasoning paths. Details on inference-time methods are in Section 4, with results in Section 5.


2


**3** **Sys2Bench Problems and Datasets**


In this section, we introduce _**Sys2Bench**_, a benchmark designed to systematically evaluate the
reasoning and planning capabilities of Large Language Models (LLMs) across diverse tasks. The
name Sys2Bench reflects its focus on evaluating Systematic Reasoning and Planning, providing a
structured framework for assessing inference-time techniques.


A key motivation for this benchmark is to _demonstrate the limitations of simply scaling inference-_
_time computation_, showing that it does not consistently lead to better reasoning or problem-solving
abilities. While inference-time techniques have gained traction in improving LLM performance, no
single approach consistently outperforms others across all tasks. Thus, we argue that a more holistic
exploration of reasoning strategies is essential. Sys2Bench facilitates this by benchmarking LLMs
on eleven datasets, categorized into five primary reasoning types: Arithmetic Reasoning, Logical
Reasoning, Common Sense Reasoning, Algorithmic Reasoning, and Planning (summarized in Table
1).


**3.1** **Arithmetic Reasoning**


The ability of Large Language Models (LLMs) to solve multi-step arithmetic problems remains an
active area of research Snell et al. [2024], Kumar et al. [2024b], Hendrycks et al. [2021]. Additionally,
OpenAI’s o1 models [OpenAI, 2024] have prompted the research community to explore inferencetime techniques to improve the arithmetic reasoning of LLMs [Zhao et al., 2024a]. We evaluate
the arithmetic reasoning of LLMs, on **GSM8K** [Cobbe et al., 2021] and **AQuA** [Ling et al., 2017]
benchmark.


**GSM8K** is a popular dataset of high-quality, linguistically diverse elementary school math word
problems, designed to evaluate multi-step arithmetic reasoning. The problems typically require 2 to 8
steps of arithmetic operations, testing the ability of LLMs to perform logical deduction and basic
calculations.


**AQuA** is a dataset of around 100,000 algebraic word problems with multiple-choice answers and
detailed rationales. It is designed to evaluate the arithmetic reasoning and problem-solving capabilities
of models, making it a challenging benchmark for LLMs.


**3.2** **Logical Reasoning**


Logical reasoning involves deriving conclusions based on a structured sequence of rules, or premises.
The evaluation of the ability to reason logically by LLM helps assess their ability to solve structured
and complex decision-making problems [Chollet, 2019]. We use **ProntoQA** [Saparov and He, 2023]
to evaluate the logical reasoning ability of LLMs.


**ProntoQA** is a dataset developed to evaluate an LLM’s ability to reason and generate explicit
reasoning chains for first-order logic-based queries [Barwise, 1977]. It challenges models to not
only produce correct answers but also provide detailed, step-by-step reasoning paths that justify their
conclusions.


**3.3** **Common Sense Reasoning**


Common Sense Reasoning is the process of drawing conclusions from implicit everyday knowledge.
Evaluating this skill ensures that LLMs provide accurate and contextually appropriate responses. We
evaluate this type of reasoning using the **StrategyQA** Geva et al. [2021] and **HotPotQA** Yang et al.

[2018] datasets.


**StrategyQA** is a benchmark designed to assess a model’s ability to perform implicit multi-step
reasoning using general knowledge or common sense facts. It consists of yes/no questions where the
goal is to arrive at the correct answer by generating and verifying intermediate reasoning steps.


**HotPotQA** is a large-scale dataset designed to evaluate how effectively models combine information
from multiple documents to answer general knowledge questions. It features diverse question types
and tests the use of sentence-level evidence for accurate and explainable multi-hop reasoning.


3


**3.4** **Algorithmic Reasoning**


We focus on applying LLMs to solve complex NP-hard and NP-complete tasks, requiring them to
evaluate constraints and propose optimized algorithms that achieve practical and effective solutions.
Such problems assess the application of LLMs to combinatorial optimization and resource allocation
tasks [Liu et al., 2024, Romera-Paredes et al., 2024]. We use **Game of 24** [Yao et al., 2024], and a
novel dataset, **Bin Packing** .


**Game of 24** is a dataset where the goal is to form an arithmetic expression evaluating to 24 using
’+’, ’-’, ’*’, or ’/’ with a list of four numbers. As an NP-complete problem with multiple solutions, it
challenges an LLM to efficiently generate expressions by focusing only on operations that can lead to
the target value.


**Bin Packing** is a new task introduced by us, inspired by the combinatorial optimization problems
studied by Liu et al. [2024], Romera-Paredes et al. [2024]. In this task, the goal is to find the least
number of bins needed to pack a list of items. Specifically, a list of _N_ items of weight [ _W_ 1 _, W_ 2 _, ...Wn_ ]
is given, which must be divided into bins _B_ 1 _, B_ 2 _, B_ 3 _...Bm_ . The sum of weights in each bin must not
exceed the bin capacity _C_, and the objective is to minimize the total number of bins _m_ . Formally, the
task can be written as:




- _mj_ =1 _[B][j]_ [=] _[ {]_ [1] _[, . . ., n][}][,]_ _Bj_ _∩_ _Bj′_ = ∅ ( _∀j_ = _j_ _[′]_ ) _,_


- _i∈Bj_ _[W][i]_ _[≤]_ _[C]_ ( _∀j_ ) _._



min _m_ subject to











(1)



**3.5** **Planning**


A planning problem is defined by ( _S_ 0 _, A, G_ ), where _S_ 0 stands for an initial state, _A_ is the set of
actions needed to achieve the goal _G_ . Planning problems require LLMs to demonstrate multistep
reasoning, and sound decision making to arrive at correct solutions. These problems have broad
applications in robotics and agent-based systems. Our evaluation focuses on four planning problems: BlocksWorld [Valmeekam et al., 2023], Rubik’s Cube [Ding et al., 2024], TripPlan, and
CalendarPlan [Zheng et al., 2024].


**BlocksWorld** is a popular dataset to evaluate the planning capabilities of LLMs. Each task involves
transitioning from an initial block configuration to a target configuration, which requires LLMs to
generate a sequence of actions to achieve the goal.


**Rubik’s Cube** requires an LLM to solve a scrambled 2 _×_ 2 cube by restoring each face to a uniform
color. Starting from a scrambled cube, the LLM must generate a valid plan of cube rotations to
achieve the goal.


**Trip Plan** challenges an LLM to plan a travel itinerary that satisfies constraints on cities, dates, and
flight connectivity, ensuring that all cities are visited as specified.


**Calendar Plan** is a dataset designed to schedule a meeting by aligning the availability of a group
of people. The goal is to find a feasible time slot that accommodates all the constraints of the
participants.


**4** **Sys2Bench Baseline Methods**


In Sys2Bench we evaluate popular inference-time techniques commonly used to enhance System 2
abilities of LLMs. While these techniques have typically been applied to specific tasks, we analyze
their performance comprehensively in Sys2Bench. Sys2Bench allows us to uncover patterns and
limitations that may not be previously evident. We summarize these methods in Fig. 1.


**Chain of Thought** (CoT) enables LLMs to solve complex problems by breaking them into intermediate reasoning steps, improving their logical coherence and accuracy Wei et al. [2022]. CoT enhances
structured problem-solving of LLMs by providing in-context examples of step-by-step reasoning
during inference.


**Self** **Consistency** (SC) extends CoT by generating multiple reasoning paths for a problem and
selecting the most consistent answer through majority voting [Wang et al., 2023].


4


|r0 1+2|r 3*4|
|---|---|
|r1<br>r2<br>3+3<br>6*4<br>3-3<br>4-2<br>_6,4_<br>_3,3,4_<br>_0_|r3<br>r5<br>r6<br>r7<br>r8<br>2*1<br>12-2<br>2-1<br>r4<br>_10_<br>_1,12_<br>_2,12_<br>_1,2,12_<br><br>_,4_|
|_(1+2+3)*4_<br><br>_24_<br>_2_|_(1+2+3)*4_<br><br>_24_<br>_2_|



Figure 1: Overview of Inference-Time Techniques evaluated on the Game of 24 dataset. We evaluate four
inference-time reasoning techniques. Chain of Thought (CoT) [Wei et al., 2022] solves problems through a
linear sequence of reasoning steps. Self-Consistency (SC) [Wang et al., 2023] extends CoT by selecting answers
through majority voting over multiple reasoning chains. Tree of Thoughts (ToT) [Yao et al., 2024] uses tree
search to explore and expand reasoning paths. Reasoning as Planning (RAP) Hao et al. [2023] combines Monte
Carlo Tree Search (MCTS) with the LLM as a world model to reward reasoning steps and guide tree growth
toward the answer.


**Tree of Thoughts** (ToT) uses structured tree search to enhance reasoning in LLMs by systematically
exploring multiple paths, with the LLM evaluating its own intermediate generations to decide which
paths to expand [Yao et al., 2024]. Evaluation can be performed by rating LLM generation on a scale
of 1-10 or using logits for scoring.


ToT has three search strategies: depth-first search (DFS), breadth-first search (BFS), and beam search.
In our experiments, we use beam search because it performs the best amongst all variants.


**Reasoning as Planning with World Models** (RAP) reformulates reasoning as a planning problem,
where the LLM acts as both the reasoning agent and the world model [Hao et al., 2023]. The reasoning
agent generates potential reasoning paths, while the world model simulates and evaluates these paths.
Specifically, RAP uses Monte Carlo Tree Search (MCTS) [Coulom, 2006] to explore and refine
reasoning paths.


Unlike ToT, which does exhaustive tree search, RAP dynamically prioritizes high-potential paths
using MCTS, resulting in improved performance. RAP requires logits for MCTS, which is why it is
exclusively implemented on LLaMA. Since RAP requires extensive prompt engineering to frame all
tasks as planning problems, we evaluate it on a subset of tasks, including GSM8K, AQuA, ProntoQA,
StrategyQA, Game of 24, Binpacking, Blocksworld, and Rubik’s Cube.


**5** **Experiments**


In this section, we present the experiments conducted on various tasks in the Sys2Bench benchmark.
We begin by outlining the experimental setup, detailing the models and implementation specifics of
the inference-time methods. Next, the results for the different inference-time methods are shown in
Table 2 and Table 3.


**5.1** **Setup**


In this subsection, we provide details about the experimental setup used to evaluate the performance
of various inference-time techniques in Sys2Bench. We describe the models, the implementation
specifics of the inference-time methods, and the metrics used for evaluation.


**Models** evaluated in Sys2Bench, consist of three LLaMa 3.1 models, two GPT-based models, and
two large reasoning models (LRMs). The LLaMa 3.1 variants are 8B, 70B, and 405B, while the


5


GPT-based models include GPT-4o and GPT-4o-mini. Additionally, the O1 and O1-mini models are
tested as part of our LRM evaluation. By default, we use a temperature of 0.8 across all models for
generation.


**Chain of Thought (CoT)** involves including in-context learning examples in the prompt. In our
benchmark, we limit this to five examples per prompt. These examples are selected from the incontext examples provided by the dataset or the training set. If neither is available, we use a subset of
test examples and evaluate the remaining test instances.


**Self Consistency (SC)** follows the same settings as CoT. We generate five CoT responses from the
LLM and determine the final output through majority voting.


**Tree of Thought (ToT)** implementation in Sys2Bench uses beam search. The beam size is 5 for
most tasks except planning tasks, where the number of possible actions at each state is larger, thus,
the beam size is increased to 10. By default, beam ranking is performed by asking the LLM to rate
outputs on a scale of 1 to 10, except for LLaMa 3.1 8B, where logits are used instead. Finally, the
search depth is task-dependent, ranging from 4 for Game of 24 to 20 for Trip Plan.


**Reasoning as Planning (RAP)** uses Monte Carlo Tree Search (MCTS) with up to 10 rollouts during
inference. Due to its reliance on a reward model that requires logits, RAP is implemented exclusively
on LLaMa 3.1 8B. Similar to ToT, the search depth in RAP varies depending on the task.


**Input Output Prompting (IO)** is utilized with LRMs, as they generate their own reasoning steps and
do not require in-context learning examples. Instead, we provide the necessary format and instruct
the models to respond in the same format.


**Metric** used across all tasks is accuracy. Note that the context of accuracy differs depending each
task. For arithmetic, commonsense, and algorithmic reasoning tasks, accuracy is measured on the
correctness of the final answer. Logical reasoning tasks, namely, ProntoQA, accuracy measures the
ability of an LLM to generate the correct reasoning chain. Finally, for planning tasks, accuracy
measures the correctness of the proposed plan.


**5.2** **Results**


In this subsection, we present the results of the Sys2Bench benchmark, organized by the types of
reasoning outlined in Section 3. This grouping allows for a clearer comparison of performance across
tasks, demonstrating the strengths and limitations of different inference-time techniques.


**Arithmetic Reasoning** tasks in Table 2 have strong results with CoT. Performance further improves
with SC, as it reduces the impact of randomness in the CoT answers. However, this strong performance
does not transfer to tree search methods. ToT significantly underperforms on this task, as its approach
of prompting the LLM to explore multiple reasoning paths relies on the LLM generating and selecting
correct intermediate reasoning steps. Since LLMs struggle with self-verification [Huang et al., 2024],
it selects incorrect intermediate arithmetic steps, leading to wrong answers. In contrast, RAP shows
modest gains on the GSM8K dataset, benefiting from the LLM’s role as a world model to select
better arithmetic steps. However, RAP still underperforms SC on AQuA, indicating that tree search
methods are not well-suited for arithmetic reasoning tasks. Meanwhile, LRMs deliver exceptional
arithmetic reasoning performance, as shown in Table 3, highlighting their strength in arithmetic.


**Logical Reasoning** results in Table 2 show interesting trends. For instance, SC improves performance
over CoT on LLaMa 3.1 8B and 70B. However, for LLaMa 3.1 405B and GPT-based models,
SC results in performance drops, as it increases the likelihood of generating multiple incorrect
reasoning chains in the ProntoQA task, where evaluation focuses on the accuracy of these chains.
Majority voting does not help when the LLM outputs multiple wrong reasoning chains. Consistent
with arithmetic reasoning, tree search methods such as ToT and RAP also underperform in this
task, indicating their limitations in logical reasoning. Finally, as shown in Table 3, LRMs do not
consistently outperform LLMs on this task, with O1 performing worse than GPT-4o on this task.


**Common** **Sense** **Reasoning** performance of CoT and SC improves with increasing LLM size.
However, tree search methods show unique trends. Specifically, both RAP and ToT generate
supporting facts for each question, but their effectiveness varies by task. To be specific, in StrategyQA,
the binary output (yes or no) enables LLaMA models to effectively utilize the generated facts, leading
to improved performance. In contrast, for HotPotQA, tree search is not effective as the LLM needs


6


to output short answers. Additional facts often cause LLM hallucinations and increased error rates.
Furthermore, compared to other tasks, performance improvements seen with LRMs are limited (see
Table 3).


**Algorithmic** **Reasoning** tasks include the Game of 24 and Binpacking datasets, as described in
Section 3. Table 2 shows that both CoT and SC underperform on these tasks. Due to the combinatorial
optimization nature of these tasks, that require extensive search, tree search methods perform well on
all models, except LLaMa 3.1 8B. The smaller size of LLaMa 3.1 8B limits the model to accurately
evaluate and determine the next steps toward a solution. When comparing LLMs to LRMs, results in
Table 3 highlight the potential of O1-mini and O1 in solving NP-Hard and NP-Complete problems,
with O1 slightly underperforming O1-mini on Game of 24.


**Planning** tasks are the most challenging in Sys2Bench. Generally, CoT and SC performance improves
with larger model sizes, and SC consistently outperforming CoT.


Tree search methods show mixed results across tasks and models. On smaller models, such as
LLaMa 3.1 8B and GPT-4o-mini, ToT shows improvements on tasks like Blocksworld and TripPlan.
However for larger models and other tasks, ToT often decreases performance. This is because
planning tasks require LLMs to generate actions to solve problems, and incorrect actions can lead
to incorrect solutions. Although ToT is intended to help LLMs explore multiple reasoning paths,
which in planning means considering different actions, LLMs often fail to generate accurate actions,
ultimately reducing performance. The other tree search method, RAP, performs exceptionally well
on Blocksworld by leveraging the LLM as a world model to predict future states and rewards.


Compared to LLMs, LRMs perform significantly better on planning tasks, with O1 achieving nearperfect results on Blocksworld. However, the Rubik’s Cube task remains challenging for all methods
and models, as it requires advanced spatial reasoning and precise prediction of the consequences of
each action. Both LLMs and LRMs currently lack the reasoning capabilities needed for this task,
making it out-of-distribution (OOD) for current language models.


**5.3** **Insights**


We extend our main experiments to provide additional insights and uncover important trends. As
the research community shows increasing interest in inference-time techniques and improving LLM
reasoning, these findings offer valuable contributions to ongoing discussions.


**Inference-time compute scaling is limited by LLM bias** . These techniques aim to improve LLM
reasoning by guiding them to generate intermediate steps, simplifying complex tasks into smaller,
manageable parts. However, this premise is flawed as LLMs do not exhaustively search for all
reasoning paths and remain biased toward certain ones. As inference-time compute scales, this bias
persists, limiting exploration and leading to diminished performance. As task complexity increases,
this issue becomes worse, exacerbating errors in reasoning and decision-making.


Our Sys2Bench experiments show this trend in arithmetic and logical reasoning. In these tasks, LLMs
excel with CoT but struggle with tree search, failing to explore reasoning paths and select the correct
one.


**Tree** **search** **struggles** **with** **increasing** **complexity,** **performing** **significantly** **worse** **than** **CoT.**
As shown in Fig 2, its benefits diminish beyond a depth of 4 for the TripPlanning and Blocksworld
tasks on LLaMa 3.1 405B. Note that, LLaMa 3.1 405B has a strong CoT performance in challenging
planning tasks and ideally ToT should lead to further improvements. However, as complexity
grows, generating the right intermediate steps becomes crucial, leading to worse performance of
ToT compared to CoT. A potential explanation for this observation is the inherent bias of LLMs at
each step of the reasoning process. These biases may propagate through successive steps, leading to
cumulative errors that degrade ToT performance.


**Language models rely on retrieval rather than true understanding** . Despite advancements in
reasoning abilities with LRMs such as O1 and O1-Mini, they still appear to be pattern matching
rather than genuine reasoning. This issue has been observed in prior studies for LLMs [Valmeekam
et al., 2023], but we are the first to demonstrate it for LRMs, including O1 and O1-Mini.


7


Table 2: Results of Inference Time Techniques across diverse tasks show that as model size increases, performance of CoT (CoT) [Wei et al., 2022] and Self Consistency (SC) [Wang et al., 2023] improves. However, this
trend doesn’t extend to tree search methods like Tree of Thought (ToT) [Yao et al., 2024], where performance
does not improve with the bigger models. Furthermore, a comparison between ToT and Reasoning as Planning
with World Models (RAP) [Hao et al., 2023] shows that RAP outperforms ToT in planning and arithmetic
reasoning tasks but lags in commonsense reasoning while performing equally in algorithmic reasoning tasks. All
methods and LLMs fail to solve the Rubik’s Cube planning task. This failure can be attributed to the spatial
understanding capabilities required for the task, which are currently out of distribution (OOD) for existing LLMs.


Algorithmic Reasoning Logical Reasoning



Methods



GSM8K AQuA ProntoQA


LLaMa 3.1 GPT LLaMa 3.1 GPT LLaMa 3.1 GPT


8B 70B 405B 4o mini 4o 8B 70B 405B 4o mini 4o 8B 70B 405B 4o mini 4o


Chain of Thought Methods



CoT 79.8 95.5 97.0 92.6 94.7 58.7 77.2 78.0 73.6 79.9 45.8 82.6 91.0 61.4 91.8
SC @ 5 86.7 96.5 97.5 93.3 94.9 70.9 85.8 86.2 79.9 83.9 54.2 88.4 89.0 58.0 91.4


Tree Search Methods


ToT 60.0 91.5 96.0 91.5 93.5 44.8 78.0 85.8 81.1 78.0 13.5 24.2 62.6 42.0 32.8
RAP 87.3 - - - - 68.1 - - - - 0.0 - - - 

Common Sense Reasoning Algorithmic Reasoning


HotPotQA StrategyQA Game of 24 Binpacking


LLaMa 3.1 GPT LLaMa 3.1 GPT LLaMa 3.1 GPT LLaMA 3.1 GPT


8B 70B 405B 4o mini 4o 8B 70B 405B 4o mini 4o 8B 70B 405B 4o mini 4o 8B 70B 405B 4o mini 4o


Chain of Thought Methods


CoT 13.8 30.6 41.0 38.6 52.8 46.0 61.5 76.0 76.6 79.2 6.0 8.0 7.0 13.0 14.0 6.0 33.0 45.0 31.0 75.0
SC @ 5 20.6 36.6 45.6 40.6 52.6 53.5 66.0 78.5 76.0 79.8 6.0 8.0 6.0 15.0 18.0 6.0 45.0 64.0 41.0 86.0


Tree Search Methods


ToT 23.0 30.0 31.5 31.4 38.2 68.0 82.0 79.5 67.5 73.5 1.0 59.0 69.0 42.0 62.0 1.0 46.0 81.0 53.0 77.0
RAP - - - - - 58.5 - - - - 1.0 - - - - 1.0 - - - 

Planning


Blocksworld Trip Plan Calendar Plan Rubik’s Cube


LLaMa 3.1 GPT LLaMa 3.1 GPT LLaMa 3.1 GPT LLaMa 3.1 GPT


8B 70B 405B 4o mini 4o 8B 70B 405B 4o mini 4o 8B 70B 405B 4o mini 4o 8B 70B 405B 4o mini 4o


Chain of Thought Methods


CoT 3.5 26.1 48.7 18.4 37.5 12.3 29.5 27.0 5.3 6.3 10.4 31.2 44.8 26.0 47.0 0.6 0.0 0.0 0.6 0.0
SC @ 5 4.5 30.7 52.1 21.2 41.5 12.0 32.3 34.3 5.0 5.8 11.6 38.0 45.6 29.6 47.4 0.0 0.6 0.6 0.6 0.6


Tree Search Methods


ToT 13.9 4.6 19.9 23.1 12.4 2.0 32.5 29.5 7.8 19.5 16.8 32.0 40.0 29.0 41.4 0.6 0.6 0.6 0.0 0.6
RAP 46.8 - - - - - - - - - - - - - - 0.6 - - - 

Table 3: Results of large reasoning models (LRMs). We report the results of IO prompting on LRMs,
including OpenAI O1-mini and O1, without providing any in-context learning examples, as recommended by
OpenAI [OpenAI, 2024]. Overall, LRMs achieve state-of-the-art performance, with O1 outperforming O1-mini
on all tasks except the Game of 24. Similar to LLMs, LRMs also struggle with the Rubik’s Cube task, indicating
a lack of spatial understanding.


Arithmetic Logical Common Sense Algorithmic
Planning
Reasoning Reasoning Reasoning Reasoning


GSM8K AQuA ProntoQA HotPotQA StrategyQA Game of 24 Binpacking Blocksworld Trip Plan Calendar Plan Rubik’s Cube


O1 Mini 98.0 92.0 64.0 35.0 74.0 77.0 90.0 48.3 24.0 88.2 0.0
O1 98.0 91.0 74.0 59.0 81.0 73.0 99.0 99.2 58.3 90.0 0.6


As shown in Fig. 3, we compare GPT-4o, O1-Mini, and O1 based on how frequently their generated
moves in the Rubik’s Cube task align with known online algorithms. Our analysis shows that GPT-4o
and O1-Mini repeat these popular moves in nearly all cases, with rates of 75% and 90%, respectively.
While O1 performs better, it still follows common move sequences about 20% of the time.


**There** **is** **a** **tradeoff** **between** **performance** **and** **the** **cost** **of** **inference-time** **methods** . Table 4
includes results across Blocksworld, Game of 24, and GSM8K using LLaMa 3.1 8B, along with the
number of tokens generated per task. Compared to CoT and SC, ToT and RAP have significantly


8


(b) Blocksworld

|Col1|Col2|Col3|Col4|Col5|Col6|Col7|
|---|---|---|---|---|---|---|
||||||||
||||||ToT||
||||||||
||||||||
||||||||



Steps



80

60

40

20

0



(a) Trip Plan

|Col1|Col2|Col3|CoT|Col5|Col6|
|---|---|---|---|---|---|
||||~~Co~~|||
||||ToT|ToT||
|||||||
|||||||
|||||||
|||||||



Cities



60


40


20



Figure 2: Tree of Thought (ToT) performance declines as task complexity increases. In (a) Trip Plan and (b)
Blocksworld, the number of steps or cities represents the required tree depth for LLM inference-time search.
While ToT performs well for smaller depths, performance deteriorates as problem complexity grows, eventually
falling below CoT. Notably, CoT achieves better performance with significantly lower computational resources,
as shown in Table 4. These results are on the LLaMa 405B model.



100


80


60


40


20


0



|Col1|Col2|Model<br>4o|Col4|Col5|
|---|---|---|---|---|
||~~O1 mini~~<br>O1|~~O1 mini~~<br>O1|~~O1 mini~~<br>O1||
||||||
||||||
||<br>|<br>|<br>||


Moves Popularity





Figure 3: Moves are grouped based on their popularity in online Rubik’s Cube solutions. LLMs like
GPT-4o frequently generate moves commonly found
in online algorithms. This issue is even more pronounced in O1-mini, where nearly 90% of the moves
are repeated! O1 exhibits this behavior less frequently,
but it remains a notable pattern.



Table 4: Token count comparison of CoT, SC, ToT,
and RAP on LLaMA 3.1 8B across Blocksworld,
Game of 24, and GSM8K. The results highlight that
scaling up inference-time techniques increases computational cost without proportionate performance gains,
contrasting with the trends observed by Snell et al.

[2024].


Blocksworld Game of 24 GSM8K


Acc _↑_ Tokens _↓_ Acc _↑_ Tokens _↓_ Acc _↑_ Tokens _↓_


CoT 3.5 3 _._ 2 _×_ 10 [4] 6.0 8 _._ 0 _×_ 10 [3] 79.8 1 _._ 9 _×_ 10 [4]

SC 4.5 1 _._ 7 _×_ 10 [5] 6.0 4 _._ 0 _×_ 10 [4] 86.7 2 _._ 4 _×_ 10 [5]

ToT 13.9 1 _._ 1 _×_ 10 [6] 1.0 3 _._ 6 _×_ 10 [7] 60.0 4 _._ 4 _×_ 10 [6]

RAP 46.8 4 _._ 9 _×_ 10 [5] 1.0 1 _._ 5 _×_ 10 [7] 87.3 9 _._ 9 _×_ 10 [6]



higher computational costs. However, increased token usage does not mean better performance.
Additionally, solving 100 Game of 24 problems with GPT-4o and ToT costs around $60 due to high
token usage, with costs rising for larger models and harder tasks. This tradeoff underscores that
increasing inference-time computation does not necessarily translate to proportional improvements in
performance.


**6** **Discussions**


While our study highlights certain limitations, there is growing interest in scaling inference-time
computation to further enhance LLM performance [Snell et al., 2024]. These methods have demonstrated strong results in arithmetic [Kumar et al., 2024a] and gameplay tasks [Schultz et al., 2024].
However, these improvements rely on verifiers or external models to guide reasoning, and without
them, performance gains disappear. Moreover, tasks like Common Sense Reasoning lack verifiers,
higlighting the limitation of verifier-dependent inference-time scaling.


On the other hand, LRMs like O1 leverage reinforcement learning (RL) with inference-time search to
improve reasoning [OpenAI, 2024, Zhao et al., 2024b]. These models are trained to generate correct
reasoning steps, enabling better performance (see Table 2). Despite significant gains, our experiments
highlight limitations, particularly in planning and common sense reasoning tasks. With inference
costs reaching 60 _×_ that of standard LLMs, it is crucial to assess their limitations.


9


In contrast to alternative views, we argue that simply scaling inference-time computation is not the
solution. Instead, improving LLM reasoning requires a more strategic approach, and combination of
RL with inference-time methods has been promising [DeepSeek-AI et al., 2025]. The recent release
of DeepSeek-R1 hints at progress in this direction, offering a glimpse of what more refined models
could achieve in the future.


**7** **Conclusion**


This paper examines the impact of scaling inference-time computation on improving the reasoning
and planning abilities of LLMs. We show that scaling inference-time computation has limitations.
Instead, we need to explore diverse approaches to enhance the holistic reasoning capabilities of
LLMs. We explore this by introducing Sys2Bench, a new benchmark, and conduct extensive
experiments evaluating inference-time techniques across eleven diverse tasks spanning five categories,
namely, arithmetic reasoning, logical reasoning, common sense reasoning, algorithmic reasoning, and
planning. Our findings provide important insights into the limitations of inference-time techniques.
Finally, we discuss alternative perspectives from the literature, critically analyze their implications,
and outline potential directions for future research.


**Acknowledgments**


This work was supported in part by National Institutes of Health under grant U01AG070112 and
National Science Foundation under grant CNS-2328395.


**References**


Jon Barwise. An introduction to first-order logic. In _Studies in Logic and the Foundations of Mathematics_,
volume 90, pages 5–46. Elsevier, 1977.


Maciej Besta, Nils Blach, Ales Kubicek, Robert Gerstenberger, Michal Podstawski, Lukas Gianinazzi, Joanna
Gajda, Tomasz Lehmann, Hubert Niewiadomski, Piotr Nyczyk, et al. Graph of thoughts: Solving elaborate
problems with large language models. In _Proceedings of the AAAI Conference on Artificial Intelligence_,
volume 38, pages 17682–17690, 2024.


Tom Brown, Benjamin Mann, Nick Ryder, Melanie Subbiah, Jared Kaplan, Prafulla Dhariwal, Arvind Neelakantan, Pranav Shyam, Girish Sastry, Amanda Askell, et al. Language models are few-shot learners. In _Advances_
_in Neural Information Processing Systems (NeurIPS)_, volume 33, pages 1877–1901, 2020.


François Chollet. On the measure of intelligence. _arXiv preprint arXiv:1911.01547_, 2019.


Karl Cobbe, Vineet Kosaraju, Mohammad Bavarian, Mark Chen, Heewoo Jun, Lukasz Kaiser, Matthias Plappert,
Jerry Tworek, Jacob Hilton, Reiichiro Nakano, Christopher Hesse, and John Schulman. Training verifiers to
solve math word problems. _arXiv preprint arXiv:2110.14168_, 2021.


Rémi Coulom. Efficient selectivity and backup operators in monte-carlo tree search. In _International conference_
_on computers and games_, pages 72–83. Springer, 2006.


DeepSeek-AI, Daya Guo, Dejian Yang, Haowei Zhang, Junxiao Song, Ruoyu Zhang, Runxin Xu, Qihao Zhu,
Shirong Ma, Peiyi Wang, Xiao Bi, Xiaokang Zhang, Xingkai Yu, Yu Wu, Z. F. Wu, Zhibin Gou, Zhihong
Shao, Zhuoshu Li, Ziyi Gao, Aixin Liu, Bing Xue, Bingxuan Wang, Bochao Wu, Bei Feng, Chengda Lu,
Chenggang Zhao, Chengqi Deng, Chenyu Zhang, Chong Ruan, Damai Dai, Deli Chen, Dongjie Ji, Erhang Li,
Fangyun Lin, Fucong Dai, Fuli Luo, Guangbo Hao, Guanting Chen, Guowei Li, H. Zhang, Han Bao, Hanwei
Xu, Haocheng Wang, Honghui Ding, Huajian Xin, Huazuo Gao, Hui Qu, Hui Li, Jianzhong Guo, Jiashi Li,
Jiawei Wang, Jingchang Chen, Jingyang Yuan, Junjie Qiu, Junlong Li, J. L. Cai, Jiaqi Ni, Jian Liang, Jin
Chen, Kai Dong, Kai Hu, Kaige Gao, Kang Guan, Kexin Huang, Kuai Yu, Lean Wang, Lecong Zhang, Liang
Zhao, Litong Wang, Liyue Zhang, Lei Xu, Leyi Xia, Mingchuan Zhang, Minghua Zhang, Minghui Tang,
Meng Li, Miaojun Wang, Mingming Li, Ning Tian, Panpan Huang, Peng Zhang, Qiancheng Wang, Qinyu
Chen, Qiushi Du, Ruiqi Ge, Ruisong Zhang, Ruizhe Pan, Runji Wang, R. J. Chen, R. L. Jin, Ruyi Chen,
Shanghao Lu, Shangyan Zhou, Shanhuang Chen, Shengfeng Ye, Shiyu Wang, Shuiping Yu, Shunfeng Zhou,
Shuting Pan, S. S. Li, Shuang Zhou, Shaoqing Wu, Shengfeng Ye, Tao Yun, Tian Pei, Tianyu Sun, T. Wang,
Wangding Zeng, Wanjia Zhao, Wen Liu, Wenfeng Liang, Wenjun Gao, Wenqin Yu, Wentao Zhang, W. L.
Xiao, Wei An, Xiaodong Liu, Xiaohan Wang, Xiaokang Chen, Xiaotao Nie, Xin Cheng, Xin Liu, Xin Xie,
Xingchao Liu, Xinyu Yang, Xinyuan Li, Xuecheng Su, Xuheng Lin, X. Q. Li, Xiangyue Jin, Xiaojin Shen,


10


Xiaosha Chen, Xiaowen Sun, Xiaoxiang Wang, Xinnan Song, Xinyi Zhou, Xianzu Wang, Xinxia Shan, Y. K.
Li, Y. Q. Wang, Y. X. Wei, Yang Zhang, Yanhong Xu, Yao Li, Yao Zhao, Yaofeng Sun, Yaohui Wang, Yi Yu,
Yichao Zhang, Yifan Shi, Yiliang Xiong, Ying He, Yishi Piao, Yisong Wang, Yixuan Tan, Yiyang Ma, Yiyuan
Liu, Yongqiang Guo, Yuan Ou, Yuduan Wang, Yue Gong, Yuheng Zou, Yujia He, Yunfan Xiong, Yuxiang
Luo, Yuxiang You, Yuxuan Liu, Yuyang Zhou, Y. X. Zhu, Yanhong Xu, Yanping Huang, Yaohui Li, Yi Zheng,
Yuchen Zhu, Yunxian Ma, Ying Tang, Yukun Zha, Yuting Yan, Z. Z. Ren, Zehui Ren, Zhangli Sha, Zhe Fu,
Zhean Xu, Zhenda Xie, Zhengyan Zhang, Zhewen Hao, Zhicheng Ma, Zhigang Yan, Zhiyu Wu, Zihui Gu,
Zijia Zhu, Zijun Liu, Zilin Li, Ziwei Xie, Ziyang Song, Zizheng Pan, Zhen Huang, Zhipeng Xu, Zhongyu
Zhang, and Zhen Zhang. Deepseek-r1: Incentivizing reasoning capability in llms via reinforcement learning,
2025. URL `[https://arxiv.org/abs/2501.12948](https://arxiv.org/abs/2501.12948)` .


Xiang Deng, Yu Gu, Boyuan Zheng, Shijie Chen, Sam Stevens, Boshi Wang, Huan Sun, and Yu Su. Mind2web:
Towards a generalist agent for the web. _Advances in Neural Information Processing Systems_, 36, 2024.


Jacob Devlin, Ming-Wei Chang, Kenton Lee, and Kristina Toutanova. BERT: Pre-training of deep bidirectional
transformers for language understanding. In _Proceedings of the 2019 Conference of the North American_
_Chapter of the Association for Computational Linguistics:_ _Human Language Technologies_, pages 4171–4186,
2019. URL `[https://arxiv.org/abs/1810.04805](https://arxiv.org/abs/1810.04805)` .


Ruomeng Ding, Chaoyun Zhang, Lu Wang, Yong Xu, Minghua Ma, Wei Zhang, Si Qin, Saravan Rajmohan,
Qingwei Lin, and Dongmei Zhang. Everything of thoughts: Defying the law of penrose triangle for thought
generation. In Lun-Wei Ku, Andre Martins, and Vivek Srikumar, editors, _Findings of the Association for_
_Computational Linguistics:_ _ACL 2024_, pages 1638–1662, Bangkok, Thailand, August 2024. Association for
Computational Linguistics. doi: 10.18653/v1/2024.findings-acl.95. URL `[https://aclanthology.org/](https://aclanthology.org/2024.findings-acl.95/)`
`[2024.findings-acl.95/](https://aclanthology.org/2024.findings-acl.95/)` .


Mor Geva, Daniel Khashabi, Elad Segal, Tushar Khot, Dan Roth, and Jonathan Berant. Did aristotle use a
laptop? a question answering benchmark with implicit reasoning strategies. _Transactions of the Association_
_for Computational Linguistics_, 9:346–361, 2021.


Shibo Hao, Yi Gu, Haodi Ma, Joshua Jiahua Hong, Zhen Wang, Daisy Zhe Wang, and Zhiting Hu. Reasoning
with language model is planning with world model. In _The 2023 Conference on Empirical Methods in Natural_
_Language Processing_, 2023. URL `[https://openreview.net/forum?id=VTWWvYtF1R](https://openreview.net/forum?id=VTWWvYtF1R)` .


Shibo Hao, Yi Gu, Haotian Luo, Tianyang Liu, Xiyan Shao, Xinyuan Wang, Shuhua Xie, Haodi Ma, Adithya
Samavedhi, Qiyue Gao, et al. Llm reasoners: New evaluation, library, and analysis of step-by-step reasoning
with large language models. _arXiv preprint arXiv:2404.05221_, 2024.


Dan Hendrycks, Collin Burns, Saurav Kadavath, Akul Arora, Steven Basart, Eric Tang, Dawn Song, and Jacob
Steinhardt. Measuring mathematical problem solving with the math dataset. _arXiv preprint arXiv:2103.03874_,
2021.


Jie Huang, Xinyun Chen, Swaroop Mishra, Huaixiu Steven Zheng, Adams Wei Yu, Xinying Song, and Denny
Zhou. Large language models cannot self-correct reasoning yet. In _The Twelfth International Conference on_
_Learning Representations_, 2024. URL `[https://openreview.net/forum?id=IkmD3fKBPQ](https://openreview.net/forum?id=IkmD3fKBPQ)` .


Wenlong Huang, Pieter Abbeel, Deepak Pathak, and Igor Mordatch. Language models as zero-shot planners:
Extracting actionable knowledge for embodied agents. In _International conference on machine learning_,
pages 9118–9147. PMLR, 2022.


Subbarao Kambhampati, Karthik Valmeekam, Lin Guan, Mudit Verma, Kaya Stechly, Siddhant Bhambri,
Lucas Paul Saldyt, and Anil B Murthy. Position: Llms can’t plan, but can help planning in llm-modulo
frameworks. In _Forty-first International Conference on Machine Learning_, 2024.


Takeshi Kojima, Shixiang Shane Gu, Machel Reid, Yutaka Matsuo, and Yusuke Iwasawa. Large language
models are zero-shot reasoners. _Advances in neural information processing systems_, 35:22199–22213, 2022.


Aviral Kumar, Vincent Zhuang, Rishabh Agarwal, Yi Su, John D Co-Reyes, Avi Singh, Kate Baumli, Shariq
Iqbal, Colton Bishop, Rebecca Roelofs, Lei M Zhang, Kay McKinney, Disha Shrivastava, Cosmin Paduraru,
George Tucker, Doina Precup, Feryal Behbahani, and Aleksandra Faust. Training language models to
self-correct via reinforcement learning, 2024a. URL `[https://arxiv.org/abs/2409.12917](https://arxiv.org/abs/2409.12917)` .


Aviral Kumar, Vincent Zhuang, Rishabh Agarwal, Yi Su, John D Co-Reyes, Avi Singh, Kate Baumli, Shariq
Iqbal, Colton Bishop, Rebecca Roelofs, et al. Training language models to self-correct via reinforcement
learning. _arXiv preprint arXiv:2409.12917_, 2024b.


Zhiqiu Lin, Deepak Pathak, Baiqi Li, Jiayao Li, Xide Xia, Graham Neubig, Pengchuan Zhang, and Deva
Ramanan. Evaluating text-to-visual generation with image-to-text generation. In _European Conference on_
_Computer Vision_, pages 366–384. Springer, 2025.


11


Wang Ling, Dani Yogatama, Chris Dyer, and Phil Blunsom. Program induction by rationale generation:
Learning to solve and explain algebraic word problems. In Regina Barzilay and Min-Yen Kan, editors,
_Proceedings of the 55th Annual Meeting of the Association for Computational Linguistics (Volume 1:_ _Long_
_Papers)_, pages 158–167, Vancouver, Canada, July 2017. Association for Computational Linguistics. doi:
10.18653/v1/P17-1015. URL `[https://aclanthology.org/P17-1015/](https://aclanthology.org/P17-1015/)` .


Bo Liu, Yuqian Jiang, Xiaohan Zhang, Qiang Liu, Shiqi Zhang, Joydeep Biswas, and Peter Stone. Llm+p:
Empowering large language models with optimal planning proficiency. _arXiv preprint arXiv:2304.11477_,
2023.


Fei Liu, Tong Xialiang, Mingxuan Yuan, Xi Lin, Fu Luo, Zhenkun Wang, Zhichao Lu, and Qingfu Zhang.
Evolution of heuristics: Towards efficient automatic algorithm design using large language model. In
_Forty-first International Conference on Machine Learning_, 2024.


OpenAI. Openai o1 system card, 2024. URL `[https://openai.com/index/openai-o1-system-card/](https://openai.com/index/openai-o1-system-card/)` .


Shubham Parashar, Zhiqiu Lin, Tian Liu, Xiangjue Dong, Yanan Li, Deva Ramanan, James Caverlee, and
Shu Kong. The neglected tails in vision-language models. In _Proceedings of the IEEE/CVF Conference on_
_Computer Vision and Pattern Recognition_, pages 12988–12997, 2024.


Alec Radford, Karthik Narasimhan, Tim Salimans, and Ilya Sutskever. Improving language understanding by generative pre-training. _OpenAI_, 2018. URL `[https://cdn.openai.com/research-covers/](https://cdn.openai.com/research-covers/language-unsupervised/language_understanding_paper.pdf)`
`[language-unsupervised/language_understanding_paper.pdf](https://cdn.openai.com/research-covers/language-unsupervised/language_understanding_paper.pdf)` .


Bernardino Romera-Paredes, Mohammadamin Barekatain, Alexander Novikov, Matej Balog, M Pawan Kumar,
Emilien Dupont, Francisco JR Ruiz, Jordan S Ellenberg, Pengming Wang, Omar Fawzi, et al. Mathematical
discoveries from program search with large language models. _Nature_, 625(7995):468–475, 2024.


Abulhair Saparov and He He. Language models are greedy reasoners: A systematic formal analysis of
chain-of-thought. In _The_ _Eleventh_ _International_ _Conference_ _on_ _Learning_ _Representations_, 2023. URL
`[https://openreview.net/forum?id=qFVVBzXxR2V](https://openreview.net/forum?id=qFVVBzXxR2V)` .


John Schultz, Jakub Adamek, Matej Jusup, Marc Lanctot, Michael Kaisers, Sarah Perrin, Daniel Hennes, Jeremy
Shar, Cannada Lewis, Anian Ruoss, Tom Zahavy, Petar Veliˇckovi´c, Laurel Prince, Satinder Singh, Eric Malmi,
and Nenad Tomašev. Mastering board games by external and internal planning with language models, 2024.
URL `[https://arxiv.org/abs/2412.12119](https://arxiv.org/abs/2412.12119)` .


Charlie Snell, Jaehoon Lee, Kelvin Xu, and Aviral Kumar. Scaling llm test-time compute optimally can be more
effective than scaling model parameters. _arXiv preprint arXiv:2408.03314_, 2024.


Karthik Valmeekam, Matthew Marquez, Sarath Sreedharan, and Subbarao Kambhampati. On the planning
abilities of large language models-a critical investigation. _Advances in Neural Information Processing Systems_,
36:75993–76005, 2023.


Karthik Valmeekam, Kaya Stechly, and Subbarao Kambhampati. Llms still can’t plan; can lrms? a preliminary
evaluation of openai’s o1 on planbench. _arXiv preprint arXiv:2409.13373_, 2024.


Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N Gomez, Łukasz Kaiser,
and Illia Polosukhin. Attention is all you need. In _Advances_ _in_ _Neural_ _Information_ _Processing_ _Systems_,
volume 30, 2017. URL `[https://arxiv.org/abs/1706.03762](https://arxiv.org/abs/1706.03762)` .


Lei Wang, Chen Ma, Xueyang Feng, Zeyu Zhang, Hao Yang, Jingsen Zhang, Zhiyuan Chen, Jiakai Tang,
Xu Chen, Yankai Lin, et al. A survey on large language model based autonomous agents. _Frontiers_ _of_
_Computer Science_, 18(6):186345, 2024.


Siyuan Wang, Zhongkun Liu, Wanjun Zhong, Ming Zhou, Zhongyu Wei, Zhumin Chen, and Nan Duan. From
lsat: The progress and challenges of complex reasoning. _IEEE/ACM Transactions on Audio, Speech, and_
_Language Processing_, 2022.


Xuezhi Wang, Jason Wei, Dale Schuurmans, Quoc V Le, Ed H. Chi, Sharan Narang, Aakanksha Chowdhery,
and Denny Zhou. Self-consistency improves chain of thought reasoning in language models. In _The Eleventh_
_International Conference on Learning Representations_, 2023. URL `[https://openreview.net/forum?](https://openreview.net/forum?id=1PL1NIMMrw)`
`[id=1PL1NIMMrw](https://openreview.net/forum?id=1PL1NIMMrw)` .


Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten Bosma, Fei Xia, Ed Chi, Quoc V Le, Denny Zhou, et al.
Chain-of-thought prompting elicits reasoning in large language models. _Advances in neural information_
_processing systems_, 35:24824–24837, 2022.


12


Sean Welleck, Amanda Bertsch, Matthew Finlayson, Hailey Schoelkopf, Alex Xie, Graham Neubig, Ilia
Kulikov, and Zaid Harchaoui. From decoding to meta-generation: Inference-time algorithms for large
language models. _Transactions_ _on_ _Machine_ _Learning_ _Research_, 2024. ISSN 2835-8856. URL `[https:](https://openreview.net/forum?id=eskQMcIbMS)`
`[//openreview.net/forum?id=eskQMcIbMS](https://openreview.net/forum?id=eskQMcIbMS)` . Survey Certification.


Haibin Wu, Xuanjun Chen, Yi-Cheng Lin, Kai-wei Chang, Ho-Lam Chung, Alexander H Liu, and Hung-yi Lee.
Towards audio language modeling-an overview. _arXiv preprint arXiv:2402.13236_, 2024.


Jian Xie, Kai Zhang, Jiangjie Chen, Tinghui Zhu, Renze Lou, Yuandong Tian, Yanghua Xiao, and Yu Su.
Travelplanner: A benchmark for real-world planning with language agents. In _Forty-first_ _International_
_Conference on Machine Learning_, 2024.


Zhenjie Yang, Xiaosong Jia, Hongyang Li, and Junchi Yan. Llm4drive: A survey of large language models for
autonomous driving. In _NeurIPS 2024 Workshop on Open-World Agents_, 2023.


Zhilin Yang, Peng Qi, Saizheng Zhang, Yoshua Bengio, William W Cohen, Ruslan Salakhutdinov, and Christopher D Manning. Hotpotqa: A dataset for diverse, explainable multi-hop question answering. _arXiv preprint_
_arXiv:1809.09600_, 2018.


Shunyu Yao, Dian Yu, Jeffrey Zhao, Izhak Shafran, Tom Griffiths, Yuan Cao, and Karthik Narasimhan. Tree
of thoughts: Deliberate problem solving with large language models. _Advances_ _in_ _Neural_ _Information_
_Processing Systems_, 36, 2024.


Yu Zhao, Huifeng Yin, Bo Zeng, Hao Wang, Tianqi Shi, Chenyang Lyu, Longyue Wang, Weihua Luo,
and Kaifu Zhang. Marco-o1: Towards open reasoning models for open-ended solutions. _arXiv_ _preprint_
_arXiv:2411.14405_, 2024a.


Yu Zhao, Huifeng Yin, Bo Zeng, Hao Wang, Tianqi Shi, Chenyang Lyu, Longyue Wang, Weihua Luo, and
Kaifu Zhang. Marco-o1: Towards open reasoning models for open-ended solutions, 2024b. URL `[https:](https://arxiv.org/abs/2411.14405)`
`[//arxiv.org/abs/2411.14405](https://arxiv.org/abs/2411.14405)` .


Huaixiu Steven Zheng, Swaroop Mishra, Hugh Zhang, Xinyun Chen, Minmin Chen, Azade Nova, Le Hou,
Heng-Tze Cheng, Quoc V Le, Ed H Chi, et al. Natural plan: Benchmarking llms on natural language planning.
_arXiv preprint arXiv:2406.04520_, 2024.


Andy Zhou, Kai Yan, Michal Shlapentokh-Rothman, Haohan Wang, and Yu-Xiong Wang. Language agent
tree search unifies reasoning, acting, and planning in language models. In _ICML_, 2024. URL `[https:](https://openreview.net/forum?id=njwv9BsGHF)`
`[//openreview.net/forum?id=njwv9BsGHF](https://openreview.net/forum?id=njwv9BsGHF)` .


Denny Zhou, Nathanael Schärli, Le Hou, Jason Wei, Nathan Scales, Xuezhi Wang, Dale Schuurmans, Claire
Cui, Olivier Bousquet, Quoc V Le, and Ed H. Chi. Least-to-most prompting enables complex reasoning in
large language models. In _The Eleventh International Conference on Learning Representations_, 2023. URL
`[https://openreview.net/forum?id=WZH7099tgfM](https://openreview.net/forum?id=WZH7099tgfM)` .


13


