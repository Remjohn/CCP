## **Cut Your Losses! Learning to Prune Paths Early for Efficient Parallel** **Reasoning**

**Jiaxi Bi** [1] _[,]_ [3][*†] **Tongxu Luo** [1] _[,]_ [2] _[∗]_ **Wenyu Du** [4] **Zhengyang Tang** [1] **Benyou Wang** [1] _[,]_ [2][‡]

1The Chinese University of Hong Kong, Shenzhen
2Shenzhen Loop Area Institute
3USTB 4DualityRL
jiaxibi@xs.ustb.edu.cn tongxuluo@cuhk.edu.cn wangbenyou@cuhk.edu.cn



**Abstract**


Parallel reasoning enhances Large Reasoning
Models (LRMs) but incurs prohibitive costs
due to futile paths caused by early errors. To
mitigate this, path pruning at the prefix level
is essential, yet existing research remains fragmented without a standardized framework. In
this work, we propose the first systematic taxonomy of path pruning, categorizing methods
by their signal _source_ (internal vs. external)
and _learnability_ (learnable vs. non-learnable).
This classification reveals the unexplored potential of _learnable internal methods_, motivating our proposal of **STOP** ( **S** uper **TO** ken for
**P** runing). Extensive evaluations across LRMs
ranging from 1.5B to 20B parameters demonstrate that STOP achieves superior effectiveness and efficiency compared to existing baselines. Furthermore, we rigorously validate the
scalability of STOP under varying compute
budgets—for instance, boosting GPT-OSS-20B
accuracy on AIME25 from 84% to nearly 90%
under fixed compute budgets. Finally, we distill
our findings into formalized empirical guidelines to facilitate optimal real-world deployment. Code, data and models are available at
[https://bijiaxihh.github.io/STOP.](https://bijiaxihh.github.io/STOP)


**1** **Introduction**


Parallel reasoning has established itself as a standard paradigm for solving complex problems (OpenAI, 2024; Wang et al., 2025b). The core principle
is to sample multiple independent reasoning paths
and subsequently aggregate them to derive a robust
consensus. However, this accuracy gain comes
at a prohibitive cost. Generating dozens or even
hundreds of trajectories per query increases computational overhead by orders of magnitude (Jin
et al., 2025) and escalates inference costs to nearly
$6 per query (NVIDIA Corporation, 2025).


  - Equal contribution; alphabetical by last name.

  - Work done during interning at CUHK-Shenzhen.

  - Corresponding author.



Figure 1: The necessity of pruning early. Early errors
often lead to irreversible failure. Pruning these futile
paths early not only saves computation but also purifies
the candidate set for better consensus.


**Why Prune Early in Parallel Reasoning?** Crucially, recent studies (Luo et al., 2025; Hassid et al.,
2025) reveal that this extensive computation is
largely squandered: **not every path contributes to**
**the solution** . Many trajectories are flawed from inception, yet they consume equal resources to generate and subsequently pollute the final answer aggregation. As illustrated in Figure 1, once a reasoning
path begins with a flawed prefix, the LRM struggles to self-correct, inevitably spiraling into a futile
trajectory (Luo et al., 2025). Consequently, identifying and terminating these unpromising paths at
the _prefix level_ —a technique known as **path prun-**
**ing (or prefix rejection)** —is essential.


**A** **Unified** **Taxonomy** While existing methods
attempt to filter paths using auxiliary reward models (Liao et al., 2025), internal confidence (Fu et al.,
2025), or semantic redundancy (Hong et al., 2025),
they lack a standardized evaluation protocol, leading to fragmented research. So first, we propose the
















































first systematic taxonomy of path pruning, classifying methods based on the _source_ (internal vs. external) and _learnability_ (learnable vs. non-learnable)
of their signals (see Figure 2). This taxonomy reveals a significant research gap: the unexplored potential of _learnable internal methods_ . Conceptually,
learnable internal methods offer unique advantages,
as learning enables task-specific accuracy gains,
while internal signals provide early, fine-grained
indicators of reasoning failure without incurring
extra computational overhead. To bridge this gap,
we introduce **STOP** ( **S** uper **TO** ken for **P** runing),
the first efficient instantiation of this paradigm. Extensive evaluations demonstrate that STOP outperforms existing baselines in both effectiveness and
efficiency.


**Further** **Evaluation** **and** **Empirical** **Analysis**
Despite the promise of path pruning, its widespread
adoption is currently hindered by unverified scalability across varying computational budgets and
model sizes; and the absence of empirical guidelines for determining optimal pruning configurations in real-world scenarios. To overcome them,
we rigorously validate the utility of path pruning
in practical settings. We conduct extensive experiments across diverse model sizes (1.5B to 20B) and
compute budgets, confirming that STOP exhibits
robust scalability. Moreover, we distill our empirical analysis into actionable guidelines, providing a
formalized method to determine the optimal retention ratio for varying resource constraints.


**Contributions** In summary, this work makes four
primary contributions: (1) We present the first systematic investigation and taxonomy of path pruning. (2) We propose STOP, a novel pruning method
based on learnable internal signals. (3) We provide
a comprehensive evaluation demonstrating STOP’s
superior scalability and effectiveness. (4) We establish empirical guidelines to support the practical
implementation of path pruning.


**2** **A Unified Taxonomy of Path Pruning**


**2.1** **Problem Definition**


Consider a LRM Θ and an input query _x_, parallel reasoning improves accuracy by generating
_N_ independent trajectories _T_ = _{τi}_ _[N]_ _i_ =1 [,] [where]
_τi_ _∼_ _P_ Θ( _x_ ), and aggregating them through a consensus strategy, such as majority voting. The final
prediction _y_ ˆ is typically computed as:


_y_ ˆ = vote( _{τi}_ _[N]_ _i_ =1 [)] _[.]_ (1)












































|Col1|Qu<br>𝐋𝐑𝐌|Col3|ery Query<br>𝐋𝐑𝐌 𝒉𝒕 𝐋𝐑<br>𝐓𝐧 𝐓𝐧<br>𝐈𝐧𝐭𝐞𝐫𝐧𝐚𝐥𝐆𝐞𝐧𝐞𝐫𝐚𝐭𝐨𝐫<br>Pruning Signal Generator AA<br>s =|Col5|𝒉𝒕 𝐋𝐑|Col7|
|---|---|---|---|---|---|---|
|𝐋𝐑𝐌|𝐋𝐑𝐌|𝐋𝐑𝐌|𝐋𝐑𝐌|𝐋𝐑𝐌|𝐋𝐑𝐌|𝐋𝐑𝐌|
|𝐓𝐧|𝐓𝐧|𝐓𝐧|𝐓𝐧|𝐓𝐧|𝐓𝐧|𝐓𝐧|
|𝐓𝐧|𝜃<br>𝑬𝒙𝒕𝒆𝒓𝒏𝒂𝒍 𝑺𝒕𝒂𝒕𝒆𝒔<br>𝜃<br>𝐄𝐱𝐭𝐞𝐫𝐧𝐚𝐥 𝐆𝐞𝐧𝐞𝐫𝐚𝐭𝐨𝐫|𝜃<br>𝑬𝒙𝒕𝒆𝒓𝒏𝒂𝒍 𝑺𝒕𝒂𝒕𝒆𝒔<br>𝜃<br>𝐄𝐱𝐭𝐞𝐫𝐧𝐚𝐥 𝐆𝐞𝐧𝐞𝐫𝐚𝐭𝐨𝐫|𝜃<br>𝑬𝒙𝒕𝒆𝒓𝒏𝒂𝒍 𝑺𝒕𝒂𝒕𝒆𝒔<br>𝜃<br>𝐄𝐱𝐭𝐞𝐫𝐧𝐚𝐥 𝐆𝐞𝐧𝐞𝐫𝐚𝐭𝐨𝐫|<br>A<br><br>A<br><br>𝐈𝐧𝐭𝐞𝐫𝐧𝐚𝐥𝐆𝐞𝐧𝐞𝐫𝐚𝐭𝐨𝐫|<br>A<br><br>A<br><br>𝐈𝐧𝐭𝐞𝐫𝐧𝐚𝐥𝐆𝐞𝐧𝐞𝐫𝐚𝐭𝐨𝐫|<br>A<br><br>A<br><br>𝐈𝐧𝐭𝐞𝐫𝐧𝐚𝐥𝐆𝐞𝐧𝐞𝐫𝐚𝐭𝐨𝐫|
|𝐓𝐧|**Type Ⅰ**<br>**Type Ⅱ**|**Type Ⅰ**<br>**Type Ⅱ**|**Type Ⅰ**<br>**Type Ⅱ**|**Type Ⅰ**<br>**Type Ⅱ**|**Type Ⅰ**<br>**Type Ⅱ**|**Type Ⅰ**<br>**Type Ⅱ**|
|𝐓𝐧|𝐧∗𝐬𝐢|𝐧∗𝐬𝐢|𝐧∗𝐬𝐢|𝐧∗𝐬𝐢|𝐧∗𝐬𝐢|𝐧∗𝐬𝐢|
|𝐓𝐦|𝐓𝐦|𝐓𝐦|𝐓𝐦|𝐓𝐦|𝐓𝐦|𝐓𝐦|
|**Continu**<br>**Reasoni**|**Continu**<br>**Reasoni**|**Continu**<br>**Reasoni**|**Continu**<br>**Reasoni**|**Continu**<br>**Reasoni**|**Continu**<br>**Reasoni**|**Continu**<br>**Reasoni**|


|Col1|𝐧∗𝐬𝐢|𝐧∗𝐬𝐢|Col4|
|---|---|---|---|
|𝐓|𝐓|𝐓|𝐓𝐦|
|𝐓|𝐓|𝐓|**ntinual**<br>**asoning**|











Figure 2: The proposed taxonomy of path pruning.


However, generating _N_ complete trajectories incurs a linear computational cost ( _C_ _∝_ _N_ ). To
mitigate this cost, path pruning aims to identify
and discard unpromising trajectories early in the
decoding process.


**The Path Pruning Formulation** Formally, we
define a checkpoint at length _L_ prefix where the generation is paused. At this stage, the model has
produced a set of prefixes _P_ = _{pi}_ _[N]_ _i_ =1 [.] [The core]
of path pruning is a **pruning signal generator** _S_,
which maps each prefix to a scalar score representing its potential correctness:


_si_ = _S_ ( _pi_ _| x,_ Θ) _,_ (2)


where _si_ _∈_ [0 _,_ 1] denotes the pruning signal. Based
on these signals, we retain only the top- _k_ promising
paths (where _k_ _≪_ _N_ ) for full completion, discarding the rest. The final aggregated answer is then
derived exclusively from this pruned subset:


_y_ ˆpruned = vote( _{_ finish( _pi_ ) _| si_ _∈{sj}_ _[k]_ _j_ =1 _[}]_ [)] _[.]_ [(3)]


So, the objective of path pruning is to design an _S_
that maximizes _y_ ˆpruned’s accuracy while minimizing the computational cost (the number of generated tokens). Therefore, the design of _S_ dictates
the effectiveness of the entire framework.


**2.2** **A Unified Taxonomy of Pruning Signal**
**Generators**


As defined in Section 2.1, the efficacy of path pruning hinges entirely on the quality of the pruning
signal generator _S_ . While the function of _S_ is consistent—scoring prefixes—existing methods differ
fundamentally in _how_ this signal is produced. To
systematically evaluate these approaches, we categorize them based on two critical dimensions: the
_source_ of the signal (External vs. Internal) and the
_learnability_ of the generator (Learnable vs. Nonlearnable), as summarized in Table 1.


Table 1: A Unified Taxonomy of Path Pruning Methods. We categorize methods based on the pruning signal source
and learnability. **Type IV** satisfies both **Desideratum 1** (Internal) and **Desideratum 2** (Learnable).








|Col1|Non-Learnable|Learnable<br>(Desideratum 2)|
|---|---|---|
|**External Source**|**Type I**<br>**SlimSC** (Hong et al., 2025)|**Type II**<br>**DeepPrune** (Tu et al., 2025),** LaBoR** (Liao et al., 2025)<br>**ThinkPRM** (Khalifa et al., 2025),** MAV** (Lifshitz et al., 2025)|
|**Internal Source**<br>(Desideratum 1)|**Type III**<br>**DeepConf** (Fu et al., 2025),** AdaDec** (He et al., 2025)<br>**Think Just Enough** (Sharma and Chopra, 2025)|**Type IV**<br>**STOP (Ours)**|



**Two Desiderata for Signal Generators** Before
categorizing specific methods, we establish two
desiderata for an ideal signal generator:


**Desideratum** **1.** _**Internal**_ _**Source**_ _An_ _ideal_ _S_
_should leverage the rich, high-dimensional internal_
_states of the LRM._


Internal signals contain fine-grained information
about uncertainty and reasoning dynamics that are
often lost in the final text output used by external
methods.


**Desideratum 2.** _**Learnability**_ _An ideal S_ _should_
_be trainable to adapt to specific data distributions._


Learnable parameters allow the generator to capture complex, non-linear patterns of error that rigid,
pre-defined heuristics cannot model.
Based on these axes, we classify existing works
into four distinct types.


**External Signal Source** Methods in this category
derive pruning signals from the generated textual
output or by querying separate models. They fail
to satisfy Desideratum 1.


**Type I.** _**Surface Heuristics**_ _These methods rely on_
_human-designed rules (e.g._ _similarity) applied to_
_the surface form of the generated text._


While computationally cheap, these heuristics
are rigid and blind to the model’s actual confidence.
To overcome these, the next type introduces learnability into the external evaluation process.


**Type II.** _**External Judges**_ _These approaches em-_
_ploy a separate, trained model to evaluate the rea-_
_soning path._


Although they satisfy Desideratum 2, they incur
significant computational overhead due to the need
for additional model inference and fail to access the
LRM’s internal certainty. To overcome this rigidity,
the next category introduces learnability into the
external evaluation process.


**Internal Signal Source** Methods in this category
extract signals directly from the LRM’s internal



states, accessing to richer information (satisfying
Desideratum 1).

**Type III.** _**Raw Confidence**_ _This paradigm utilizes_
_intrinsic metrics directly derived from the decoding_
_process, such as perplexity or token probability._

However, these methods rely on fixed definitions
of confidence, violating Desideratum 2; raw probability does not always correlate with reasoning
correctness.

**Type** **IV.** _**Learned**_ _**Intuition**_ _The_ _final_ _category_
_represents_ _the_ _intersection_ _of_ _both_ _desiderata:_ _a_
_trainable module inserted into the LRM to process_
_internal states._

This approach can leverage rich hidden representations (Internal) while adapting to the specific
error patterns of the task (Learnable).


**3** **Methodology:** **Super Token for Pruning**


As established in our taxonomy, Type IV represents the ideal pruning paradigm but remains unexplored. In this section, we introduce **STOP** ( **S** uper
**TO** ken for **P** runing), the first efficient instantiation
of this paradigm. We delineate the motivation in
Section 3.1, followed by the architectural design
and workflow in Section 3.2.


**3.1** **Motivation for Type IV Pruning**


As illustrated in Figure 2, prior methods compromise on either information richness or adaptability.
Type II suffers from high latency, while Type III
lacks the capacity to model complex error patterns.
Type IV represents an ideal optimum: it combines
the _efficiency_ of accessing internal states with the
_adaptability_ of learnable parameters. However, this
type remains unexplored due to the challenge of designing a module that extracts these signals without
disrupting the LRM’s generative capabilities.


**3.2** **Instantiation of Type IV Pruning:** **STOP**


To instantiate this type, we design **STOP** as a
lightweight, non-invasive module that integrates
seamlessly with the backbone LRM.


|Col1|Col2|Col3|Col4|Col5|Col6|
|---|---|---|---|---|---|
|𝐋𝐑𝐌<br>(𝐅𝐫𝐨𝐳𝐞𝐧)|𝐋𝐑𝐌<br>(𝐅𝐫𝐨𝐳𝐞𝐧)|𝐋𝐑𝐌<br>(𝐅𝐫𝐨𝐳𝐞𝐧)|𝐋𝐑𝐌<br>(𝐅𝐫𝐨𝐳𝐞𝐧)|𝐋𝐑𝐌<br>(𝐅𝐫𝐨𝐳𝐞𝐧)|𝐋𝐑𝐌<br>(𝐅𝐫𝐨𝐳𝐞𝐧)|





Figure 3: The inference process comprises three stages: caching initial prefixes ( **Launch** ), scoring them via the
**STOP** module ( **Check** ), and completing only the top-ranked candidates ( **Resume** ).



**Components** We augment the fixed LRM Θ with
three learnable components: (1) **A Super Token**
**([STOP])** added to the vocabulary, acting as a specialized query vector to aggregate information; (2)
**A Critique Adapter** LoRA ( _θ_ LoRA), activated only
when processing the [STOP] token to extract errorspecific features without altering the LRM’s general reasoning capabilities; (3) **A** **Classification**
**Head** ( _W_ cls), which projects the hidden state of the

[STOP] token to a scalar probability.
This design ensures **modularity** : the original parameters Θ remain frozen, preserving the
LRM’s generative capability while enabling efficient parameter-efficient fine-tuning (PEFT).


**Training:** **Learn** **to** **Use** **Internal** **Information**
The goal of training is simple: teach the model
to distinguish promising prefixes from futile ones.
Formally, for a prefix _pi_, we derive a soft label
_s_ _[mc]_ _i_ _∈_ [0 _,_ 1] via Monte Carlo estimation (details
in Appendix B). The training process involves two
steps: First, we compute the KV cache of the prefix
using the frozen LRM: _Cpi_ = LRM( _pi_ ; Θ). Second, we append a sequence of learnable [STOP]
tokens, denoted as _Ts_, and process them using the
LoRA-augmented model. The final hidden state _hi_
is fed into the classifier to minimize the soft binary
cross-entropy loss:

_L_ = _−_ [ _s_ _[mc]_ _i_ log _σ_ ( _Wclshi_ ) (4)
+(1 _−_ _s_ _[mc]_ _i_ ) log(1 _−_ _σ_ ( _Wclshi_ ))] _,_


where _hi_ = LRM( _Ts_ _| Cpi_ ; Θ _, θ_ LoRA) _−_ 1.


**Training Cost** Constructing the MC supervision
requires sampling multiple continuations per prefix
to estimate _s_ _[mc]_ _i_ (e.g., _K_ = 32), which introduces
an upfront computational cost during data construction. However, this cost is incurred only once,



and the resulting STOP module is lightweight and
reusable across tasks. To facilitate transparency and
reproducibility, we provide detailed cost statistics
in Appendix B.3 and will release the constructed
dataset and trained checkpoints, allowing practitioners to bypass this step entirely. Importantly,
this one-time cost is amortized during deployment,
where STOP improves efficiency by pruning unpromising paths early.


**Inference:** **“Launch-Check-Resume”** To efficiently prune paths without slowing down generation, we design a three-stage pipeline (Figure 3):
**Stage 1:** **Launch** Instead of generating the full
trajectories immediately, we first generate _N_ short
prefixes (e.g., first 1024 tokens) for the query. Crucially, we cache the internal states (KV Cache) of
these prefixes.
**Stage 2:** **Check** We append the [STOP] tokens
to the cached prefixes. The trained module reads
the KV cache and outputs a quality score for each
prefix. _Note:_ This step is extremely fast because it
processes only a few tokens (the [STOP] sequence)
and reuses the heavy computation already done in
Stage 1.
**Stage 3:** **Resume** We rank the prefixes by their
scores and apply a **Top-** _k_ **Filter** . Futile paths are
discarded immediately to free up memory. Only
the top- _k_ most promising prefixes are resumed and
generated to completion to obtain the final answers.


**4** **A Close Look at Path Pruning through**
**the Lens of Signal Generators**


**4.1** **On the Effectiveness of Pruning**


To systematically evaluate the effectiveness of four
types of pruning signal generators in our taxonomy,


Table 2: Results of avg@k (avg@m|k) across various models and benchmarks. The best result in each row is **bolded**
and the second best is underlined.


**No pruning (Baseline)** **Type I** **Type II** **Type III** **Type IV**
**Model** **Dataset**

avg@64 ( _↑_ ) Tokens ( _↓_ ) avg@8|64 ( _↑_ ) Tokens (% _↓_ ) avg@8|64 ( _↑_ ) Tokens (% _↓_ ) avg@8|64 ( _↑_ ) Tokens (% _↓_ ) avg@8|64 ( _↑_ ) Tokens (% _↓_ )







we conduct extensive experiments on five reasoning
benchmarks. We employ a diverse suite of LRMs
ranging from 1.5B to 20B parameters, specifically
the DeepSeek-R1-Distill-Qwen series (Guo et al.,
2025) and gpt-oss-20b (OpenAI, 2025).


**Standardized protocol.** To ensure a fair comparison, we establish a standardized evaluation protocol: for each query, we generate 64 initial reasoning paths. We prune these to the top 8 candidates.
For each _S_, we apply pruning at **2,048 tokens** to
rigorously evaluate their ability to identify futile
paths with limited context.


**Evaluation metrics.** We report two metrics: **(1)**
**avg@k**, defined as the average accuracy over the
_k_ paths. In the context of pruning, we denote this
metric as **avg@m|k** (selecting _m_ from _k_ ). Since
random pruning theoretically yields an average accuracy equivalent to the no-pruning baseline, **a**
**pruning method is considered effective only if its**
**avg@m|k surpasses the baseline avg@k**, thereby
indicating a higher density of correct answers in
the selected subset. **(2) total tokens**, which is used
to quantify computational cost. We calculate the
relative token reduction ∆ as:


Tokensoriginal _−_ Tokenspruned
∆= _×_ 100% _._ (5)

Tokensoriginal


We list the detailed experimental settings, including
infrastructure and hyperparameters in Appendix C.


**Performance Hierarchy across Four Types Prun-**
**ing** As presented in Table 2, while most pruning signals demonstrate effectiveness, we observe
distinct performance hierarchies. First, internalbased generators (Type III and Type IV) consistently outperform external-based ones (Type I and
Type II). This advantage stems from their access
to internal LRM states—such as hidden states
and KV caches—which encode significantly richer



representations than the constrained natural language outputs used by external methods. Second, learnable generators (Type IV and Type II)
surpass non-learnable baselines, as both leverage
training data to detect reasoning errors at early
stages; we further validate this by explicitly training Type II on our data (see Appendix D). Most
remarkably, **Type IV (STOP) dominates all other**
**paradigms** in both effectiveness and efficiency.
For instance, on the AIME 24 benchmark (1.5B),
STOP increases average accuracy from 30.10% to
**37.92%** —significantly exceeding Type II (32.50%)
and Type III (32.92%)—while simultaneously reducing total token consumption by over **73%** .


**Findings** **1.** _Type_ _IV_ _pruning_ _offers_ _better_
_efficiency-accuracy trade-off._


**4.2** **On the Scalability of Pruning**


After validating the effectiveness, we now put these
_S_ into practical parallel inference settings to assess
their scalability. We show the cons@N vs. total
compute (tokens) in Figure 4. We fix the retention
ratio at _γ_ = _M/N_ = 1 _/_ 2 for all methods and vary
the initial sample size _N_ to cover different compute
budgets. All other configurations remain consistent
with Section 4.1.


**Robustness across Tasks and Model Scales** We
observe a key phenomenon: across all tasks and
model scales, some pruning signals achieve better
performance than the no-pruning baseline. However, most existing methods do not exhibit consistent improvements across different tasks and models. For example, Type III outperforms the baseline
on AIME 2024 with the 1.5B model but falls below it on AIME 2025. In contrast, our proposed
Type IV demonstrates stable and consistently superior scalability across nearly all tasks. We attribute
this robustness to the fact that Type IV captures the


Total Compute (Thousands of Tokens)


Figure 4: Performance vs. compute for four types of _S_ on math and stem benchmarks.



**intrinsic** **logical** **consistency** of reasoning paths,
which we further analyze in Section 5.3.


**Findings 2.** _Type IV pruning scales robustly across_
_varying compute budgets._


**5** **A Closer Look at STOP**


**5.1** **Determining the Optimal remaining ratios**


While the effectiveness of Type IV is established,
optimal deployment requires precise tuning of two
critical hyperparameters: the prefix length ( _L_ prefix)
and the retention ratio ( _γ_ ). Since increasing _L_ prefix
generally enhances error detection at the cost of
higher latency, users typically fix this parameter
according to their specific latency budget. However,
determining the optimal retention ratio _γ_ remains
non-trivial. To provide a practical guideline, we
formalize the objective as finding a function _γ_ =
_f_ ( _C, L_ prefix _, L_ task) that maximizes accuracy given
a compute budget _C_ (in tokens) and a reference
task length _L_ task:


arg max Accuracy( _C, L_ prefix _, L_ task _, γ_ ) _,_ (6)
_f_


where _γ_ determines the proportion of paths retained. Identifying this function _f_ enables the prediction of the optimal _γ_ for any given configuration.


**Consistent Empirical Trends across Various Set-**
**tings** To derive _f_, we conduct experiments using DS-Qwen-2.5-1.5B on AIME 2024 and GPQA
Diamond, sweeping _γ_ from 1 _/_ 32 to 1 _/_ 2 across
four distinct _L_ prefix settings. The results, plotted in



Figure 5, exhibit consistent trends: the optimal _γ_
decreases as either the compute budget _C_ or the
prefix length _L_ prefix increases. These observations
indicate that with sufficient compute or richer context, the model identifies futile paths more reliably, thereby allowing for more aggressive pruning
(lower _γ_ ) without compromising accuracy.


**Formalizing** **Empirical** **Findings** Building on
these insights, we model the relationship using a
power-law formulation:

_[L]_ pref _[c]_ x
_γ_ _[−]_ [1] = _f_ ( _C, L_ prefix _, L_ task) = _aC_ _[b]_ _._ (7)
_L_ _[d]_
task


In this formulation, all input variables are normalized to units of 1,024 tokens. Fitting this model
to our empirical data yields empirical coefficients
_a ≈_ 1 _._ 17 _×_ 10 [4], _b ≈_ 0 _._ 46, _c ≈_ 0 _._ 40, and _d ≈_ 4 _._ 55.
As illustrated in Figure 6, the predicted curve aligns
closely with the empirical optimal points, offering
a robust guideline for parameter selection in practical deployments.


**Applying** **the** **Empirical** **Guideline** To facilitate practical deployment, we apply the derived
guideline to predict the optimal retention ratio
_γ_ for specific configurations without exhaustive
search. Specifically, for a task with a shorter response horizon ( _L_ task _≈_ 8 _,_ 650), a prefix length
of _L_ prefix = 2 _,_ 048, and a total compute budget of
_C_ = 158k tokens, the scaling law predicts an optimal inverse retention ratio of _γ_ _[−]_ [1] _≈_ 9 _._ 63, corresponding to _γ_ _≈_ 10%. Conversely, for a task with a


65.0


62.5


60.0


57.5


55.0


52.5


50.0


47.5



40.0


39.0


38.0


37.0



48.0


47.0


46.0


45.0


44.0


43.0


42.0





175.8


156.2


136.7


117.2


97.7


78.1


58.6



185.5


175.8


166.0


156.2


146.5


136.7


127.0


117.2


107.4


97.7



65.0


60.0


55.0


50.0


45.0


40.0


35.0



537.1


488.3


439.5


390.6


341.8


293.0


244.1


195.3



537.1


488.3


439.5


390.6


341.8


293.0


244.1


195.3


|Col1|Col2|Col3|
|---|---|---|
||||
||||
||||
||||


|Col1|Col2|Col3|Col4|
|---|---|---|---|
|||||
|||||
|||||
|||||
|||||
|||||
|||||


|Col1|Col2|Col3|Col4|
|---|---|---|---|
|||||
|||||
|||||
|||||
|||||


|Col1|Col2|Col3|Col4|
|---|---|---|---|
|||||
|||||
|||||
|||||
|||||
|||||
|||||



(a) GPQA ( _L_ prefix = 512)



(b) GPQA ( _L_ prefix = 1024)



(c) AIME ( _L_ prefix = 2048)



(d) AIME ( _L_ prefix = 4096)



Figure 5: Performance comparison under different retention ratios ( _γ_ ) and prefix lengths ( _L_ prefix).



25


15


10


5


3


2





3.50e-04


3.00e-04


2.50e-04


2.00e-04


1.50e-04


1.00e-04


5.00e-05


|Col1|Col2|Col3|Col4|Col5|Col6|
|---|---|---|---|---|---|
|||||||
|||||||
|||||||
|||||||
|||||||
|||||||
|||||||
|||||||
|||||||
|||||||
|||||||
|||||~~AIME 20~~<br>|~~ 48 (~~<br>~~1.84e~~<br>~~05)~~<br> <br><br>|
|||||~~AIME 40~~<br>~~GPQA 5~~<br>~~GPQA 1~~|~~ 96 (~~<br>~~2.43~~e<br>~~05)~~<br>~~ 12 (~~<br>~~1.21~~e<br>~~04)~~<br>~~ 024 (~~<br>~~1.59e~~<br>~~04)~~|



40 60 100 200 300 500

Compute / Prefix Ratio


Figure 6: Inverse retention ratio _γ_ _[−]_ [1] vs. compute-toprefix ratio. The theoretical curves (Eq. 7) closely align
with empirical observations across varying reasoning
progress levels.


longer reasoning chain ( _L_ task _≈_ 12k, _L_ prefix = 3k,
and _C_ = 275k), it yields a more conservative estimate of _γ_ _[−]_ [1] _≈_ 3 _._ 36.
These predictions are consistent with our empirical observations, indicating that the scaling law
naturally adapts to variations in task complexity.
For detailed lookup guidelines across a broader
range of configurations, we refer readers to **Ap-**
**pendix E.2** .


**5.2** **Ablations and Analysis**


To validate the core design choices of **STOP**, we
examine two critical dimensions: the quality of the
supervision signal and the computational overhead
during inference.


**Ablation:** **Quality** **of** **the** **Supervision** **Signal**
**STOP** uses Monte Carlo (MC) estimation with
_K_ = 32 samples to generate probabilistic soft labels ( _s_ _[mc]_ ), and we compare this setting with binary hard-label supervision, which corresponds to
a single-sample estimate ( _K_ = 1). While hard
labels are computationally cheap, they introduce
high variance because prefix quality depends on
a single stochastic continuation. As shown in Table 3, increasing the sampling budget from _K_ = 1
to _K_ = 32 consistently improves performance. On
AIME 2024, soft supervision improves Cons@N



from 46.67% to 53.33%. These results indicate that
MC-based soft labels provide a low-variance signal
that enables the lightweight **STOP** module to learn
stable pruning boundaries.


Table 3: Performance comparison between hard labels
( _K_ = 1) and MC-estimated soft labels ( _K_ = 32).


**Dataset** **Supervision Type** **avg@8|64 (%)** **Cons@N (%)**


Hard Labels ( _K_ = 1) 35.42 46.67
AIME 24
**Soft Labels (** _K_ = 32 **)** **36.67** **53.33**


Hard Labels ( _K_ = 1) 40.78 47.98
GPQA
**Soft Labels (** _K_ = 32 **)** **41.73** **48.48**


**Findings 3.** _When training pruning method, soft_
_labels (0.0 to 1.0) have lower variance than hard_
_labels (0 or 1)._


**Ablation:** **Necessity of Critique Adapter** Given
that the LRM’s internal states already encode rich
reasoning history, a natural question arises: Is a
simple linear classifier sufficient to decode the pruning signal? As shown in Table 4, the answer is
negative. Removing the LoRA adapter leads to a
significant performance drop (e.g., from **36.67%**
to **31.67%** on AIME 2024). This phenomenon
highlights a fundamental misalignment: the LRM’s
native representations are optimized for predicting
next token, not value discrimination. A linear head
alone struggles to extract quality assessments from
this generation-centric feature space.


Table 4: Comparing the STOP module with a simple
linear classifier confirms that raw internal states require
adaptation to perform effective self-evaluation.


**Dataset** **Configuration** **avg@8|64 (%)** **Cons@N (%)**


STOP w/o Adapter 31.67 46.67
AIME 24
**STOP** **36.67** **53.33**


STOP w/o Adapter 33.96 35.35
GPQA
**STOP** **41.73** **48.48**


**Findings** **4.** _High-quality_ _self-correction_ _cannot_
_be achieved by merely probing the states in LRMs;_
_it requires a specialized transformation to bridge_
_the gap between thinking forward (generation) and_
_looking back (reflection)._


**Ablation:** **Sensitivity to Design Choices** We further examine the sensitivity of **STOP** to key de

sign choices, namely the number of [STOP] tokens
and the LoRA rank. As shown in Table 5, performance improves with more tokens, peaks at 4–6,
and then degrades with further increases, indicating
a trade-off between expressive capacity and overfitting. Similarly, Table 6 shows that moderate ranks
(e.g., _r_ = 128) achieve the best performance, while
larger ranks lead to slight degradation, suggesting
that excessive capacity is unnecessary.


**Findings** **5.** _STOP_ _is_ _robust_ _to_ _reasonable_ _hy-_
_perparameter choices and does not require large_
_adapters to perform effectively._


Table 5: Effect of the number of [STOP] tokens (DSQwen-2.5-1.5B, AIME 2024, _L_ prefix = 2048).

|# Tokens avg@32|256|# Tokens avg@32|256|
|---|---|
|1<br>30.10<br>2<br>33.54<br>3<br>35.94<br>4<br>36.86<br>5<br>36.77|6<br>**37.71**<br>7<br>36.15<br>8<br>35.00<br>9<br>33.65<br>-<br>-|



Table 6: Effect of LoRA rank (DS-Qwen-2.5-1.5B,
AIME 2024).


Rank Params (M) avg@8 _|_ 64


32 36.9 32.50
64 73.9 36.25
**128** **147.7** **36.67**
256 295.4 35.83


**Analysis:** **Computational Overhead** We quantify the inference latency on a single NVIDIA H100
GPU using DS-Qwen-2.5-7B with a fixed prefix
length of 2 _,_ 048. As detailed in Table 7, existing
paradigms incur notable costs: Type II requires
full sequence re-encoding, resulting in the highest
latency ( **1.13 s**, 3.37% overhead), while Type I suffers from the computational bottleneck of pairwise
similarity calculations ( **0.38 s** ). In stark contrast,
**STOP** (Type IV) minimizes overhead to a negligible **0.20 s** ( **0.59%** ). This efficiency stems directly
from our architectural design: by **reusing the pre-**
**computed KV cache** and restricting verification
to a single forward pass of special tokens, STOP
eliminates redundant computation, ensuring highthroughput deployment.


Table 7: Inference overhead analysis. STOP achieves
near-zero cost by avoiding re-encoding.


**Pruning Paradigm** **Latency / Check** **Relative Overhead**


Type II 1.13 s 3.37%
Type I 0.38 s 0.93%


**Analysis:** **Generalization to Non-Math/STEM**
**Tasks** To assess whether **STOP** captures univer


Table 8: **Generalization** **on** **ZebraLogic.** **STOP** **ro-**
**bustly generalizes** beyond math and science tasks.


**No pruning (Baseline)** **STOP**
**Model** **Gain**
**avg@64 (%)** **avg@8|64 (%)**


DS-Qwen-2.5-7B 73.73 **77.23** **+3.50%**


sal reasoning patterns beyond mathematics and science, we extend our evaluation to **ZebraLogic**,
a benchmark designed to evaluate combinatorial
reasoning and constraint satisfaction capabilities
through logic grid puzzles. Specifically, we conduct experiments on the multiple-choice mode
(mc_mode) to test reasoning under constraints. Using the **DS-Qwen-2.5-7B** model, we evaluate 500
randomly sampled instances of moderate difficulty
(Rows, Cols _≤_ 4). As shown in Table 8, **STOP**
improves accuracy from 73.73% to **77.23%** . This
consistent gain confirms that the pruning signals
learned by the module are not strictly domaindependent, but rather transferable to general logical
inference tasks.


**Analysis:** **Generalization to Tool Use** We further evaluate whether **STOP** generalizes to realistic
tool-use scenarios by submitting our system to the
**AIMO3** competition, where models solve mathematical problems with access to external tools
under a fixed evaluation protocol. Built on a **GPT-**
**OSS-120B + tool** framework, we compare against
a baseline that directly performs parallel reasoning without pruning under the same resource constraints; due to the competition setting (single H100
GPU and a 5-hour limit for 50 problems), the baseline cannot scale to larger sampling budgets. As
shown in Table 9, both STOP configurations consistently outperform the baseline, improving the
score from **39** to **42** (24 _→_ 8) and **43** (16 _→_ 8), with
the best configuration reaching **silver-level perfor-**
**mance** on the public leaderboard, demonstrating
that **STOP** remains effective in tool-augmented
reasoning and translates into tangible gains in realworld competitive settings.


Table 9: Results on the AIMO3 competition setting with
tool use (GPT-OSS-120B).


**Method** **Score**


Baseline + Tool 39
STOP (24 _→_ 8) 42
STOP (16 _→_ 8) **43**


(a) **High-scoring Path** (b) **Low-scoring Path**
Figure 7: **Attention** **Analysis** **of** **[STOP]** **Decision-Making.** High-scoring paths prioritize logical pivots (e.g.,
self-correction markers), whereas low-scoring paths fixate on terminal answer tokens. This contrast confirms that
**STOP** functions as a process-oriented evaluator, rewarding reasoning integrity over premature closure.



**5.3** **How STOP Attends**


To understand how **STOP** distinguishes valid reasoning trajectories, we visualize the attention distribution of the [STOP] token (Figure 7). Overall, the
module exhibits a broad attention pattern. It consistently attends to **multiple-choice options** (A, B,
C, D) as well as discourse markers (e.g., “Hmm”,
“Wait”), which enables it to track the structural progression of the reasoning process.


**Process-oriented Evaluation** Importantly, highscoring and low-scoring trajectories present clearly
distinct attention signatures. In the **high-score case**
(Figure 7a), attention prioritizes the reasoning process rather than the final outcome. Specifically,
the [STOP] token focuses on **cognitive pivots** (e.g.,
the negation “don’t”), indicating an emphasis on
logical operations that trigger self-correction. In
contrast, the **low-score** **case** (Figure 7b) demonstrates a pattern of **premature closure** : attention
shifts early to the terminal token (e.g., “B”) while
critical logical markers receive little attention. Consequently, **STOP** penalizes such trajectories and
interprets the lack of attention to logical pivots as
evidence of reasoning failure. See Appendix G for
more cases.


**6** **Conclusion**


In this work, we address the critical efficiency bottleneck of parallel reasoning by establishing the
first unified taxonomy of path pruning. This framework not only resolves the fragmentation in existing research but also reveals the unexplored potential of _learnable_ _internal_ _methods_ (Type IV). To
bridge this gap, we introduce **STOP**, a lightweight
method that leverages internal representations to
identify and terminate futile prefixes effectively.
Extensive evaluations demonstrate that STOP consistently dominates existing paradigms, significantly enhancing reasoning accuracy while reduc


ing token consumption by over 70%. Moreover,
we resolve scalability and deployment uncertainties by deriving a robust interaction formulation.
This provides practitioners with a precise empirical guideline for optimizing the trade-off between
exploration and exploitation under varying computational constraints. Finally, our in-depth analysis
of the mechanism and architectural choices offers
valuable insights to guide future research.


**Acknowledgment**


This work was supported by Major Frontier Exploration Program (Grant No. C10120250085)
from the Shenzhen Medical Academy of Research
and Translation (SMART), Shenzhen Medical Research Fund (B2503005), NSFC grant 72495131,
the 1+1+1 CUHK-CUHK(SZ)-GDSTC Joint Collaboration Fund, Guangdong Provincial Key Laboratory of Mathematical Foundations for Artificial
Intelligence (2023B1212010001), and the International Science and Technology Cooperation Center,
Ministry of Science and Technology of China (under grant 2024YFE0203000).


**Limitations**


As the pioneering instantiation of the internal learnable paradigm (Type IV), **STOP** validates the potential of intrinsic representations for trajectory
pruning. However, we acknowledge specific limitations in our current scope and highlight promising
directions for future research.


**Limitations.**


  - **Verification at Extreme Scales** Our current
evaluation spans models up to 20B parameters
and standard compute budgets (e.g., _N_ = 64).
The behavior of STOP on substantially larger
models (e.g., 70B+) and under massive sampling regimes (e.g., _N_ _≥_ 1000) remains to be
empirically verified.


  - **Structural Flexibility** This work focuses on
single-stage pruning at fixed positions (e.g.,
_L_ prefix = 2048). We have not yet explored
more complex settings, such as multi-stage
sequential pruning or unstructured pruning
where checkpoints are determined dynamically rather than at fixed token indices.


**Future Directions.**


  - **Progressive** **Multi-Stage** **Pruning** A natural extension is to apply STOP in a cascading manner (e.g., funneling candidates from
64 _→_ 32 _→_ 16 at successive checkpoints).
This "progressive filtering" strategy could further optimize the compute allocation by dynamically narrowing the search space as reasoning deepens.


  - **Accelerating RL Training** Beyond inference,
STOP holds significant potential for training
efficiency. In Reinforcement Learning (e.g.,
PPO or GRPO), STOP can serve as an online rejection mechanism during the rollout
phase, terminating low-value trajectories early
to increase the density of high-quality training
signals per unit of compute.


**References**


Tom B. Brown, Benjamin Mann, Nick Ryder, Melanie
Subbiah, Jared Kaplan, et al. 2024. Large language models are few-shot learners. _arXiv preprint_
_arXiv:2005.14165_ .


Han Cai, Jing Li, Wei Liu, and Tianqi Chen. 2024.
Medusa: Simple framework for accelerating llm generation with multiple decoding heads. _arXiv preprint_
_arXiv:2401.10774_ .


Brendan Chan, Chen Liang, Yiming Yang, and Tian
Wang. 2023. Chameleon: Plug-and-play compositional reasoning with large language models. _arXiv_
_preprint arXiv:2304.09842_ .


Yichao Fu, Xuewei Wang, Yuandong Tian, and Jiawei
Zhao. 2025. Deep think [with](https://arxiv.org/abs/2508.15260) confidence. _arXiv_
_preprint arXiv:2508.15260_ .


Daya Guo, Dejian Yang, Haowei Zhang, Junxiao
Song, Ruoyu Zhang, Runxin Xu, Qihao Zhu,
Shirong Ma, Peiyi Wang, Xiao Bi, et al. 2025.
Deepseek-r1: [Incentivizing reasoning capability in](https://arxiv.org/abs/2501.12948)
LLMs via [reinforcement](https://arxiv.org/abs/2501.12948) learning. _arXiv_ _preprint_
_arXiv:2501.12948_ .


Michael Hassid, Gabriel Synnaeve, Yossi Adi, and
Roy Schwartz. 2025. [Don’t overthink it. preferring](https://arxiv.org/abs/2505.17813)
[shorter thinking chains for improved llm reasoning.](https://arxiv.org/abs/2505.17813)
_arXiv preprint arXiv:2505.17813_ .



Kaifeng He, Mingwei Liu, Chong Wang, Zike Li, Yanlin
Wang, Xin Peng, and Zibin Zheng. 2025. [Adadec:](https://arxiv.org/abs/2506.08980)
[Uncertainty-guided adaptive decoding for llm-based](https://arxiv.org/abs/2506.08980)
[code generation.](https://arxiv.org/abs/2506.08980) _arXiv preprint arXiv:2506.08980_ .


Colin Hong, Xu Guo, Anand Chaanan Singh, Esha
Choukse, and Dmitrii Ustiugov. 2025. [Slim-sc:](https://arxiv.org/abs/2509.13990)
Thought pruning for [efficient](https://arxiv.org/abs/2509.13990) scaling with self[consistency.](https://arxiv.org/abs/2509.13990) _arXiv preprint arXiv:2509.13990_ .


Yunho Jin, Gu-Yeon Wei, and David Brooks. 2025.

[The energy cost of reasoning:](https://arxiv.org/abs/2505.14733) Analyzing energy us[age in llms with test-time compute.](https://arxiv.org/abs/2505.14733) _arXiv preprint_
_arXiv:2505.14733_ .


Muhammad Khalifa, Rishabh Agarwal, Lajanugen Logeswaran, Jaekyeom Kim, Hao Peng, Moontae Lee,
Honglak Lee, and Lu Wang. 2025. [Process reward](https://arxiv.org/abs/2504.16828)
[models that think.](https://arxiv.org/abs/2504.16828) _arXiv preprint arXiv:2504.16828_ .


Woosuk Kwon, Zhuohan Li, Siyuan Zhuang, Ying
Sheng, Lianmin Zheng, Cody Hao Yu, Joseph E. Gonzalez, Hao Zhang, and Ion Stoica. 2023. Efficient
memory management for large language model serving with pagedattention. In _Proceedings of the 29th_
_ACM Symposium on Operating Systems Principles_ .


Baohao Liao, Xinyi Chen, Sara Rajaee, Yuhui Xu, Christian Herold, Anders Søgaard, Maarten de Rijke, and
Christof Monz. 2025. Lost at the beginning of reasoning. _arXiv preprint arXiv:2506.22058_ .


Shalev Lifshitz, Sheila A. McIlraith, and Yilun Du.
2025. Multi-agent [verification:](https://arxiv.org/abs/2502.20379) Scaling test-time
compute with [multiple](https://arxiv.org/abs/2502.20379) verifiers. _arXiv_ _preprint_
_arXiv:2502.20379_ .


Tongxu Luo, Wenyu Du, Jiaxi Bi, Stephen Chung,
Zhengyang Tang, Hao Yang, Min Zhang, and Benyou
Wang. 2025. [Learning from peers in reasoning mod-](https://arxiv.org/abs/2505.07787)
[els.](https://arxiv.org/abs/2505.07787) _arXiv preprint arXiv:2505.07787_ .


Mathematical Association of America. 2024. American invitational mathematics examination (aime)
2024. [https://maa.org/math-competitions/](https://maa.org/math-competitions/american-invitational-mathematics-examination-aime)
[american-invitational-mathematics-examination-aime.](https://maa.org/math-competitions/american-invitational-mathematics-examination-aime)
Accessed: February 2024.


Mathematical Association of America. 2025. American invitational mathematics examination (aime)
2025. [https://maa.org/math-competitions/](https://maa.org/math-competitions/american-invitational-mathematics-examination-aime)
[american-invitational-mathematics-examination-aime.](https://maa.org/math-competitions/american-invitational-mathematics-examination-aime)
Accessed: February 2025.


NVIDIA Corporation. 2025. Llm inference benchmarking: How much does your llm inference
cost? [https://developer.nvidia.com/blog/](https://developer.nvidia.com/blog/llm-inference-benchmarking-how-much-does-your-llm-inference-cost/)
[llm-inference-benchmarking-how-much-does-your-llm-infer](https://developer.nvidia.com/blog/llm-inference-benchmarking-how-much-does-your-llm-inference-cost/)
Accessed: 2025-11-05.


OpenAI. 2024. Learning to [reason](https://openai.com/index/learning-to-reason-with-llms/) with LLMs. Accessed: 2025-11-01.


OpenAI. 2025. gpt-oss model [card](https://openai.com/index/gpt-oss-model-card/) (gpt-oss-120b &
[gpt-oss-20b).](https://openai.com/index/gpt-oss-model-card/) Accessed: 2025-11-01.


David Rein, Betty Li Hou, Asa Cooper Stickland, Jackson Petty, Richard Yuanzhe Pang, Julien Dirani, Julian Michael, and Samuel R. Bowman. 2024. [Gpqa:](https://openreview.net/forum?id=Ti67584b98)
[A graduate-level google-proof q&a benchmark.](https://openreview.net/forum?id=Ti67584b98) In
_First Conference on Language Modeling (COLM)_ .


Aman Sharma and Paras Chopra. 2025. [Think](https://arxiv.org/abs/2510.08146)
just enough: [Sequence-level](https://arxiv.org/abs/2510.08146) entropy as a confidence signal [for](https://arxiv.org/abs/2510.08146) llm reasoning. _arXiv_ _preprint_
_arXiv:2510.08146_ .


Shangqing Tu, Yaxuan Li, Yushi Bai, Lei Hou, and
Juanzi Li. 2025. Deepprune: Parallel scaling
without inter-trace redundancy. _arXiv_ _preprint_
_arXiv:2510.08483_ .


Peiyi Wang, Lifan Li, Zhenyu Shao, Ruixuan Xu, Dong
Dai, Yanzhe Li, Yuzhuo Yao, and Zhifang Sui. 2024.
Math-shepherd: Verify and reinforce llms step-bystep without human annotations. In _Proceedings_
_of_ _the_ _62nd_ _Annual_ _Meeting_ _of_ _the_ _Association_ _for_
_Computational Linguistics (Volume 1:_ _Long Papers)_,
pages 9426–9439, Bangkok, Thailand. Association
for Computational Linguistics.


Xuezhi Wang, Jason Wei, Dale Schuurmans, Quoc Le,
Ed Chi, and Sharan Narang. 2022. Self-consistency
improves chain of thought reasoning in language
models. _arXiv preprint arXiv:2203.11171_ .


Yifan Wang, Yichi Zhang, Xinyi Li, and Jie Zhou.
2025a. A survey on parallel reasoning. _arXiv_
_preprint arXiv:2510.12164_ .


Ziqi Wang, Boye Niu, Zipeng Gao, Zhi Zheng, Tong Xu,
Linghui Meng, Zhongli Li, Jing Liu, Yilong Chen,
Chen Zhu, Hua Wu, Haifeng Wang, and Enhong
Chen. 2025b. [A survey on parallel reasoning.](https://arxiv.org/abs/2510.12164)


Shunyu Yao, Dian Yu, Jeffrey Zhao, Izhak Shafran,
Tom Griffiths, Yuan Cao, and Karthik Narasimhan.
2023. Tree of thoughts: Deliberate problem solving
with large language models. In _Advances in Neural_
_Information Processing Systems_, volume 36, pages
11809–11822.


Jian Zhao, Rui Liu, Kai Zhang, Zihan Zhou, Jun Gao,
Dong Li, and Bowen Zhou. 2025. Genprm: Scaling
test-time compute of process reward models via generative reasoning. _arXiv preprint arXiv:2504.00891_ .



**A** **Related Work**


**A.1** **Parallel Reasoning**


Parallel reasoning, which generates multiple trajectories to verify or aggregate answers, has become
a standard paradigm for enhancing LRM performance. A recent survey by (Wang et al., 2025a)
systematically categorizes these approaches into
three dimensions: **(1)** **Non-interactive** **Reason-**
**ing**, which generates independent paths without
communication, including majority voting in _Self-_
_Consistency_ (Wang et al., 2022), ranking in _Best-of-_
_N_ (Brown et al., 2024), and structured exploration
in _Tree-of-Thoughts_ (Yao et al., 2023). **(2) Interac-**
**tive Reasoning**, which enables active information
exchange among paths, for example, internal state
sharing in _Leap_ (Luo et al., 2025) or multi-agent
collaboration (Chan et al., 2023). **(3)** **Efficiency**
**Optimization**, which focuses on accelerating decoding mechanics, such as speculative decoding in
_Medusa_ (Cai et al., 2024). Although these methods
enhance reasoning performance, they still suffer
from substantial inference costs, which remain a
major limitation.


**A.2** **Path Pruning (Prefix Rejection)**


To mitigate the high inference cost of parallel reasoning, path pruning strategies aim to terminate
unpromising trajectories early. Consistent with the
taxonomy in Section 2.2, we categorize existing
works based on signal source and learnability.
Regarding **external** signals, **non-learnable**
methods (Type I) like SlimSC (Hong et al., 2025)
prune paths utilizing heuristic metrics such as semantic similarity to minimize redundancy. In
contrast, **learnable** approaches (Type II) rely on
trained verifiers. This category encompasses discriminative classifiers used in DeepPrune (Tu
et al., 2025) and LaBoR (Liao et al., 2025), as
well as generative verifiers in ThinkPRM (Khalifa et al., 2025) and multi-agent frameworks like
MAV (Lifshitz et al., 2025). Shifting to **internal**
sources, **non-learnable** methods (Type III) derive
signals directly from intrinsic statistics. Representative works include confidence-based estimation
in DeepConf (Fu et al., 2025) and AdaDec (He
et al., 2025), or entropy-based metrics in Think
Just Enough (Sharma and Chopra, 2025).
Notably, **prior works** leave the quadrant of **in-**
**ternal learnable** modules (Type IV) unexplored.
**STOP** is designed to bridge this gap, utilizing a
trainable adapter to extract rich internal semantics,


Figure 8: MC-based construction of prefix–potential
supervision.


thus offering a solution that is both structurally
efficient and data-driven.


**B** **Data Construction Details**


To train our **STOP** module, we require a dataset
that directly maps prefixes of reasoning paths to
the probability that the final answer succeeds. A
single binary label on a complete path provides
an insufficient and noisy signal, because a promising prefix may still end in an accidental failure,
while a flawed prefix may occasionally be recovered by chance. Therefore, we construct a dataset
of (prefix, success probability) pairs using
**Monte Carlo (MC) estimation** (Wang et al., 2024;
Zhao et al., 2025).


**B.1** **Source Benchmarks and**
**Decontamination**


We constructed a supervised fine-tuning dataset
derived from high-quality mathematical and scientific benchmarks. Specifically, we aggregated
approximately 1,000 problems from the **AIME**
competition (spanning years 1984 to 2023) (Mathematical Association of America, 2024, 2025),
augmented with the non-Diamond portion of the
**GPQA** dataset (Rein et al., 2024). _Crucially,_ _to_
_ensure zero data leakage, we strictly excluded the_
_evaluation sets from this training corpus:_ _specif-_
_ically,_ _**AIME 2024**_ _,_ _**AIME 2025**_ _,_ _and the_ _**GPQA**_
_**Diamond**_ _subset were entirely removed._


**B.2** **Model-Specific Construction Pipeline**


Since reasoning capabilities vary across model
scales, we adopted a **model-specific** **pipeline**
where each LRM (e.g., 1.5B) generates its own
training data. The procedure proceeds as follows:



Table 10: **Statistics** **of** **model-specific** **training** **data.**
Prefixes are extracted from Math (AIME) and Science
(GPQA). Data volume decreases for larger models due
to filtering of trivial samples.


**Model** **Math** **Science** **Total**


DS-Qwen-2.5-1.5B 14,816 8,448 **23,264**
DS-Qwen-2.5-7B 12,092 5,666 **17,758**
DS-Qwen-3-8B 10,848 4,456 **15,304**
GPT-OSS-20B 7,872 2,378 **10,250**


**Difficulty Stratification (Filtering).** Before generating prefixes, we first filter source problems to
focus on the model’s _learnable boundary_ . For each
problem, we generate _N_ = 32 reasoning paths
and calculate the pass rate. We explicitly exclude
**trivial** **samples** ( _>_ 28 correct answers) that the
model has already mastered, as well as **intractable**
**samples** ( _<_ 4 correct answers) likely beyond its
current capacity. This ensures that the training data
consists of problems where the pruning signal is
most valuable.


**Prefix Generation.** From the retained problems,
we use the LRM to generate a prefix _p_ that forms
part of a complete reasoning trajectory. To simulate
a realistic mid-generation checkpoint, we truncate
these paths at a fixed length of _L_ **prefix** = 2 _,_ 048
tokens.


**Potential Estimation via MC Rollouts.** To estimate the potential of _p_, we fix the prefix and generate _K_ = 32 continuations under a temperature of
0 _._ 6. This procedure produces a set of full-length
responses _{τ_ 1 _[′]_ _[, τ]_ 2 _[ ′]_ _[, . . ., τ]_ _K_ _[ ′]_ _[}]_ [.]


**MC** **Score** **Calculation.** We evaluate each response for correctness (1 if correct and 0 otherwise). The MC-estimated success probability _s_ _[mc]_

is defined as the empirical accuracy:



The resulting label _s_ _[mc]_ _∈_ [0 _._ 0 _,_ 1 _._ 0] provides a finegrained probabilistic target used to train the STOP
module.


**Data Statistics and Insights.** Table 10 summarizes the composition of the constructed datasets.
We observe a distinct **inverse** **scaling** **trend** : as
the model size increases, the number of valid training samples decreases (e.g., from 23,264 for 1.5B
to 10,250 for 20B). This confirms the efficacy of
our difficulty stratification strategy: larger models (e.g., GPT-OSS-20B) achieve high pass rates



_s_ _[mc]_ = [1]

_K_



_K_

- is_correct( _τj_ _[′]_ [)] _[.]_ (8)


_j_ =1


Table 11: **Training** **Cost** **for** **MC** **Supervision** **Construction.** We report the number of training pairs and the
estimated wall-clock cost (in 8 _×_ H100 GPU hours) required to construct the dataset with _K_ = 32 Monte Carlo
samples per prefix.


**Model** **Math** **Science** **Total Training Pairs** **8** _×_ **H100 Hours**


DS-Qwen-2.5-1.5B 14,816 8,448 **23,264** 43.08
DS-Qwen-2.5-7B 12,092 5,666 **17,758** 39.46
DS-Qwen-3-8B 10,844 4,456 **15,304** 37.79
GPT-OSS-20B 7,872 2,378 **10,250** 75.93


Table 12: **Training hyperparameters across model scales.**


**Hyperparameter** **1.5B** **7B** **8B** **20B**


Per-Device Batch Size 16 8 8 2
Gradient Accumulation 1 2 2 8
Learning Rate 2 _×_ 10 _[−]_ [5] 2 _×_ 10 _[−]_ [5] 2 _×_ 10 _[−]_ [5] 2 _×_ 10 _[−]_ [5]

LoRA Rank ( _r_ ) 128 256 256 2048
LoRA Alpha ( _α_ ) 256 512 512 4096
Target Modules All Linear All Linear All Linear All Linear
Optimizer AdamW AdamW AdamW AdamW
Max Prefix Length 2048 2048 2048 2048
Training Epochs 15 15 15 15
Precision bf16 bf16 bf16 bf16



( _>_ 28 _/_ 32) on a larger portion of the source benchmarks, causing these “trivial” instances to be filtered out. Consequently, the training data naturally
adapts to focus on the _learnable boundary_ specific
to each model’s capability.


**B.3** **Training Cost Details**


Constructing the MC supervision dataset requires
sampling multiple continuations per prefix (e.g.,
_K_ = 32) as described in Section 3.1. In practice,
we find that moderate sampling budgets provide
a good balance between estimation stability and
computational cost, as also reflected in our ablation results. We report the estimated cost across
different model scales in Table 11.

These costs correspond to a one-time data construction process. Once constructed, the dataset
can be reused across training runs and model variants, amortizing the cost of data construction. The
trained STOP module introduces negligible overhead during inference. These costs are reported to
provide transparency and should be interpreted as
approximate estimates depending on implementation and hardware configurations.


**C** **Detailed Experimental Settings**


In this appendix, we provide the complete experimental details to ensure reproducibility, covering
infrastructure, datasets, input formats, training hyperparameters, and baseline implementations.



**C.1** **Infrastructure and Sampling**
**Configuration**


**Infrastructure.** All experiments were conducted
on NVIDIA H100 (80GB) GPUs. We utilized the
vLLM framework (Kwon et al., 2023) to support
efficient batched inference during the evaluation
phases.
**Sampling Configuration.** To ensure consistency
across all pruning methods, we adopted a unified
generation configuration. Specifically, the temperature was set to 0 _._ 6, top- _p_ to 0 _._ 95, and top- _k_ to 40.
The maximum generation length was set to 16 _,_ 384
tokens for the 1.5B and 7B models, and 32 _,_ 768
tokens for the 8B and 20B models. For gpt-oss
models, the reasoning effort was set to “medium”.


**C.2** **Evaluation Protocol**


We strictly adhered to established evaluation protocols to ensure fair comparison and reproducibility.
The **GPQA-Diamond** subset, consisting of 198
high-difficulty questions, was reserved exclusively
as a held-out test set. Consequently, all remaining
GPQA questions were used solely during the training stage. This rigorous separation guarantees zero
information leakage from the training corpus to the
evaluation benchmarks.


**C.3** **Prompt Templates and Input Format**


To ensure rigorous reproducibility, we detail the
exact prompt templates and input construction used
in our experiments. We utilized the standard zeroshot Chain-of-Thought (CoT) format.


**C.4** **STOP Module Training Details**


We developed a custom training pipeline utilizing the Hugging Face Accelerate and PEFT libraries. All experiments were conducted on 8
NVIDIA H100 GPUs using a LoRA-only approach.
We froze the base model parameters and strictly
trained low-rank adapters attached to **all** **linear**
**layers** within the transformer blocks. Specifically,
we targeted the full set of projections: q_proj,
k_proj, v_proj, o_proj, gate_proj, up_proj,
and down_proj. The specific hyperparameters, including the varying LoRA configurations for different model scales, are detailed in Table 12.


**C.5** **Baseline Descriptions**


We provide additional details on the baseline implementations used in Section 4:


  - **SlimSC (Hong et al., 2025) (Type I):** Computes the pairwise Jaccard similarity between
the current generation and previously explored
reasoning paths. It prunes trajectories that
exhibit high semantic redundancy to ensure
diversity.


  - **LaBoR (Liao et al., 2025) (Type II):** Relies
on a separate, trained Process Reward Model
(PRM) to score generated prefixes. We used



the official checkpoints released by the authors where available.


  - **DeepConf (Fu et al., 2025) (Type III):** Estimates confidence by computing perplexity
and entropy directly from the model logits
of the generated tokens, serving as a nonlearnable internal baseline.


**D** **Ablation:** **Data Quality vs.**
**Architecture**


**D.1** **Motivation and Setup**


A potential confounding factor in our main results is the quality of the training data. Since
**STOP** is trained on a high-quality dataset constructed via Monte Carlo rollouts, it is natural to
hypothesize that the observed performance gains
mainly arise from superior supervision rather than
from the **Type** **IV** architecture itself. To disentangle these two factors, we introduce a controlled baseline, **Type II** **[retrain]** **(Retrained Early**
**Pruning)** . LaBoR (Liao et al., 2025) propose
an Early Pruning strategy based on an external Process Reward Model (PRM), specifically
Qwen2.5-Math-PRM-7B, but their model is not
trained on our MC-estimated soft labels. For a fair
comparison, we adopt the same architecture and
fine-tune it on the _same dataset_ of prefix–success
probability pairs used to train **STOP** . This comparison isolates the architectural effect between an
internal, learnable method ( **Type IV** ) with access
to full hidden states and an external reward model
( **Type** **II** ) that relies only on token-level outputs,
thereby ruling out data quality as the sole source
of improvement. **Note:** Because the backbone of
Type II is specialized for mathematics, we exclude
the GPQA (Science) benchmark from this ablation,
as the external PRM lacks sufficient domain knowledge for scientific reasoning.


**D.2** **Detailed Analysis**


Table 13 reports results across models and benchmarks. We observe that **Type** **II-retrain** consistently outperforms the standard Type II baseline,
which is typically trained on public PRM datasets
or heuristic labels. This result confirms that MCestimated soft labels provide a stronger and more
informative supervision signal than conventional binary labels, even for external reward models. More
importantly, despite being trained on identical data,
**STOP** consistently outperforms **Type II-retrain**
across different model scales. For example, at the


Table 13: **Ablation Study:** **Architecture vs.** **Data.** Comparison of avg@8 and token efficiency. **Type II** refers to
the standard external PRM baseline (Early Pruning). **Type II** **[retrain]** denotes the same external architecture retrained
on our MC-estimated data. **STOP** ( **Type IV** ) outperforms both, demonstrating that architectural access to internal
states yields gains beyond data quality alone. Note: Type II variants are not evaluated on GPQA due to the domain
limitation of the math-specialized PRM backbone.


**Full Paths (Baseline)** **Type II** **Type II** **[retrain]** **Type IV**
**Model** **Dataset**

avg@8|64 ( _↑_ ) Tokens ( _↓_ ) avg@8|64 ( _↑_ ) Tokens (% _↓_ ) avg@8|64 ( _↑_ ) Tokens (% _↓_ ) avg@8|64 ( _↑_ ) Tokens (% _↓_ )



DS-Qwen-2.5-1.5B


DS-Qwen-2.5-7B


DS-Qwen-3-8B


GPT-OSS-20B



AIME24 30.10 782.3k 32.50 325.9k (-58.34%) 37.50 318.2k (-59.33%) **37.92** **204.3k** (-73.88%)
AIME25 22.76 784.8k 24.17 325.0k (-58.59%) 24.16 323.2k (-58.82%) **26.67** **206.6k** (-73.68%)
BRUMO25 30.99 774.6k 31.67 325.6k (-57.96%) 32.50 320.5k (-58.62%) **33.75** **204.4k** (-73.61%)
HMMT25 15.05 856.4k 15.00 337.2k (-60.63%) 16.67 333.8k (-61.03%) **17.92** **215.5k** (-74.84%)
GPQA-D 33.08 550.9k - - - - **48.42** **179.4k** (-67.43%)


AIME24 54.69 666.2k 54.58 312.5k (-53.09%) 59.17 308.6k (-53.68%) **61.67** **189.0k** (-71.63%)
AIME25 39.67 703.0k 39.17 317.6k (-54.82%) 37.08 315.5k (-55.13%) **42.50** **197.5k** (-71.91%)
BRUMO25 50.99 656.6k 51.25 312.1k (-52.46%) 53.33 309.1k (-52.92%) **56.67** **190.2k** (-71.03%)
HMMT25 23.91 808.9k 23.33 330.8k (-59.11%) 24.17 328.8k (-59.35%) **27.08** **211.6k** (-73.84%)
GPQA-D 45.95 443.8k - - - - **55.75** **165.9k** (-62.61%)


AIME24 76.93 1361k 78.75 398.4k (-70.73%) 77.92 396.5k (-70.87%) **79.17** **279.0k** (-79.51%)
AIME25 70.68 1427k 72.50 408.4k (-71.39%) **73.33** 407.5k (-71.44%) 72.92 **290.9k** (-79.62%)
BRUMO25 75.00 1320k 75.83 394.9k (-70.10%) 75.00 396.1k (-70.01%) **78.75** **277.5k** (-78.98%)
HMMT25 51.04 1601k 50.83 427.8k (-73.28%) 52.08 427.7k (-73.28%) **54.58** **311.7k** (-80.53%)
GPQA-D 56.87 652.6k - - - - **63.32** **193.5k** (-70.35%)


AIME24 75.26 594.2k 76.25 299.8k (-49.55%) 74.16 302.5k (-49.09%) **77.50** **184.4k** (-68.98%)
AIME25 70.99 673.4k 69.17 311.7k (-53.71%) 69.58 310.4k (-53.91%) **75.42** **191.1k** (-71.62%)
BRUMO25 68.02 575.6k 66.25 298.8k (-48.09%) 67.50 297.9k (-48.24%) **70.00** **183.6k** (-68.11%)
HMMT25 48.13 910.8k 45.42 336.9k (-63.01%) 48.75 333.3k (-63.41%) **52.92** **216.1k** (-76.27%)
GPQA-D 65.55 277.2k - - - - **77.46** 143.4k (-48.26%)



1.5B scale, **STOP** achieves higher avg@8 on AIME
25 (26.67% vs. 24.16%) and BRUMO 25 (33.75%
vs. 32.50%), while at the 7B scale it surpasses
Type II [retrain] on AIME 24 (61.67% vs. 59.17%). In
addition, while Type II is restricted to mathematical tasks due to its specialized backbone, **STOP**,
implemented via LoRA, naturally generalizes to
the scientific domain on GPQA during training,
demonstrating greater flexibility. The only exception is a minor difference on DS-Qwen-3-8B for
AIME 25 (72.92% vs. 73.33%), which lies within
normal variance; in all other settings, **STOP** shows
clear and consistent advantages.


**D.3** **Discussion:** **The Advantage of Internal**
**Signals**


The superiority of **STOP** ( **Type** **IV** ) can be attributed to its ability to mitigate the _information_
_bottleneck_ inherent in external evaluation. An external PRM ( **Type II** ) judges reasoning quality solely
from generated text, which is a discrete and lowdimensional projection of the model’s internal reasoning process and often discards subtle signals of
uncertainty and coherence. In contrast, **STOP** is
integrated directly into the generator and has access to dense internal representations, including
hidden states and attention patterns. These internal
signals preserve rich information about confidence
and logical consistency that is largely lost during
decoding. By leveraging such first-person internal
signals, **STOP** evaluates the potential of a prefix



more accurately than a third-person external reward
model.


**E** **Derivation and Validation of the**
**Scaling Law**


In Section 5.1, we introduced the Interaction Scaling Law to describe the relationship among the optimal pruning ratio _γ_, the compute budget _C_, and
task complexity. In this appendix, we first examine
the empirical optimization surfaces that validate
this formulation (Appendix E.1), and then provide
detailed reference tables for practical deployment
(Appendix E.2).


**E.1** **Empirical Observations on Optimal**
**Retention**


We study how the optimal retention ratio _γ_ _[∗]_, defined as the peak of the performance envelope under a fixed compute budget, varies across benchmarks and prefix lengths _L_ prefix. Visualizations of
these empirical surfaces are presented in Figure 9.
**Scientific** **Reasoning** **(GPQA).** For GPQA with
_L_ prefix = 512 and 1024, the optimal strategy shifts
toward more aggressive pruning as the compute
budget increases. With short contexts ( _L_ prefix =
512), _γ_ _[∗]_ is around 1 _/_ 8 at low budgets ( _∼_ 24k
tokens), reflecting a balance between exploration
and exploitation. As the budget increases to 195k
tokens, the performance peak moves to smaller
values ( _γ_ _≈_ 1 _/_ 16), indicating that **STOP** effec

tively discards low-quality candidates when sufficient samples are available. For medium contexts
( _L_ prefix = 1024), conservative retention ( _γ_ = 1 _/_ 2)
consistently underperforms. The optimal _γ_ _[∗]_ starts
near 1 _/_ 8 and rapidly decreases toward _γ_ _≈_ 1 _/_ 28
as compute increases.
This pruning pattern arises from the concise reasoning structure of GPQA. GPQA solutions typically require few steps, so the fixed prefix captures
a large portion of the full reasoning trajectory. As
a result, the prefix contains high information density and provides a strong pruning signal, enabling
**STOP** to aggressively filter candidates with low
risk of removing correct solutions.
**Mathematical** **Reasoning** **(AIME).** In contrast,
AIME shows a strong dependence on prefix length,
reflecting the higher sunk cost of long mathematical derivations. For _L_ prefix = 2048, increasing the
compute budget shifts the optimal _γ_ _[∗]_ from conservative values ( _γ_ _≈_ 1 _/_ 2) toward more aggressive pruning ( _γ_ _≈_ 1 _/_ 4). Compared with GPQA,
AIME consistently requires higher retention because mathematical reasoning is deeply sequential,
and a fixed prefix represents only an initial portion
of the full solution, leading to greater downstream
uncertainty.
When the context length increases to _L_ prefix =
4096, we observe a further shift toward selectivity.
Contrary to the expectation that longer contexts
require conservative retention, the optimal _γ_ _[∗]_ decreases to the range _γ_ _∈_ [1 _/_ 6 _,_ 1 _/_ 8]. This behavior
indicates that a longer prefix provides richer evidence for evaluating trajectory quality. With more
reasoning history available, the **STOP** module identifies flawed paths with higher confidence, allowing
more aggressive pruning than in the _L_ prefix = 2048
setting without sacrificing correct solutions.
**Alignment with the Unified Formula.** These results support the coupled structure of the Interaction Scaling Law. Across all tasks, _γ_ _[∗]_ consistently
decreases as the compute budget _C_ increases. At
the same time, the optimal pruning level is modulated by the interaction between task domain and
available context. Overall, the scaling law adapts
to differences in reasoning density across domains
and prefix lengths, and it aligns well with the observed empirical optimization landscapes.


**E.2** **Recommended Retention Guidelines**


Based on the derived scaling law, we provide reference tables for selecting optimal pruning strategies.
To **improve** **visual** **clarity** **and** **facilitate** **quick**



**lookup**, we present the guidelines in two separate
tables, each corresponding to a different compute
budget regime.
These tables are intended primarily as **illustra-**
**tive references** for representative task lengths. For
other tasks, whether they are similar to GPQA or
Math and have different response characteristics,
practitioners can directly substitute the task length
( _Ltask_ ), prefix length ( _Lprefix_ ), and compute budget ( _C_ ) into the derived formula (Eq. 7) to obtain
the exact optimal retention ratio.
Tables 14 and 15 report the recommended **in-**
**verse** **retention** **ratio** ( _γ_ _[−]_ [1] ) for representative
short-horizon tasks ( _Ltask_ _≈_ 8 _,_ 650) and longhorizon tasks ( _Ltask_ _≈_ 11 _,_ 950), respectively.


**F** **Detailed Latency and Throughput**
**Benchmarking**


In this appendix, we present a detailed analysis
of the system efficiency discussed in Section 5.2.
We conduct controlled micro-benchmarks on a single NVIDIA H100 GPU using **DS-Qwen-2.5-7B** .
The evaluation uses a batch size of 16 and a fixed
prefix length of 2,048 tokens to simulate realistic
inference conditions.


**F.1** **Metric Definitions**


We adopt the following metrics to evaluate computational overhead:

- **Generation Time (** _T_ **gen):** The wall-clock time
required for autoregressive decoding of reasoning
tokens, excluding any verification operations.

- **Verification Latency (** _T_ **verify):** The explicit computation time required by the pruning signal generator to produce scores for a batch.

- **System** **Throughput:** The effective inference
speed measured in tokens per second (tok/s).
Unlike latency metrics, throughput captures implicit system-level overheads, including CPU–
GPU synchronization and pipeline inefficiencies
caused by context switching.


**F.2** **Quantitative Analysis**


Table 16 reports the detailed timing breakdown
across different pruning paradigms. The results
reveal a clear mismatch between explicit verification latency and the realized system throughput,
especially for heuristic-based methods.
**Throughput degradation in heuristic methods.**
A key observation is the pronounced throughput
drop in Type I (SlimSC). Although the cumulative


65.0


60.0


55.0


50.0


45.0


40.0


35.0


30.0



65.0


60.0


55.0


50.0


45.0


40.0


35.0



= [1] ~~2~~

= [1] ~~3~~

= [1] ~~4~~

= [1] ~~5~~

= [1] ~~6~~

= [1] ~~8~~

= ~~10~~ [1]

= ~~12~~ [1]

= ~~16~~ [1]

= ~~20~~ [1]

= ~~24~~ [1]

= ~~28~~ [1]

= ~~32~~ [1]



97.7k 195.3k 293.0k 390.6k 488.3k
Total Tokens



= [1] ~~2~~

= [1] ~~3~~

= [1] ~~4~~

= [1] ~~5~~

= [1] ~~6~~

= [1] ~~7~~

= [1] ~~8~~

= ~~10~~ [1]

= ~~12~~ [1]

= ~~14~~ [1]

= ~~16~~ [1]

= ~~18~~ [1]

= ~~20~~ [1]

= ~~24~~ [1]

= ~~28~~ [1]

= ~~32~~ [1]

= ~~36~~ [1]



(a) **AIME 2024 (** _L_ _**prefix**_ _**= 2048**_ **)** . Optimal _γ_ shifts to aggressive pruning as budget increases.


= [1] ~~2~~

= [1] ~~3~~



97.7k 195.3k 293.0k 390.6k 488.3k
Total Tokens


(b) **AIME 2024 (** _L_ _**prefix=4096**_ **)** . Longer context enables
stable pruning at higher selectivity.


= [1] ~~2~~

= [1] ~~3~~



= [1] ~~4~~

= [1] ~~5~~

= [1] ~~6~~

= [1] ~~7~~

= [1] ~~8~~

= ~~10~~ [1]

= ~~12~~ [1]

= ~~14~~ [1]

= ~~16~~ [1]

= ~~20~~ [1]

= ~~24~~ [1]

= ~~28~~ [1]

= ~~32~~ [1]



48.0


46.0


44.0


42.0


40.0


38.0



40.0


38.0


36.0


34.0



= [1] ~~4~~

= [1] ~~5~~

= [1] ~~6~~

= [1] ~~7~~

= [1] ~~8~~

= ~~10~~ [1]

= ~~12~~ [1]

= ~~14~~ [1]

= ~~16~~ [1]

= ~~20~~ [1]

= ~~24~~ [1]

= ~~28~~ [1]

= ~~32~~ [1]



24.4k 48.8k 73.2k 97.7k 122.1k 146.5k 170.9k 195.3k
Total Tokens


(c) **GPQA (** _L_ _**prefix=512**_ **)** . Higher compute budgets drive
more aggressive pruning.



24.4k 48.8k 73.2k 97.7k 122.1k 146.5k 170.9k 195.3k
Total Tokens


(d) **GPQA (** _L_ _**prefix=1024**_ **)** . Scaling behavior remains consistent with longer contexts.



Figure 9: **Empirical optimization surfaces.** Impact of retention ratio _γ_ across increasing compute budgets.


Table 14: **GPQA (Science, Short-Horizon).** Recommended inverse retention ratios ( _γ_ _[−]_ [1] ) for tasks with shorter
reference lengths ( _L_ task _≈_ 8 _,_ 650). Pruning is more aggressive (higher values) even at lower budgets.


**Compute Budget** _C_ **(Total Tokens)**
**Prefix Length**

( _L_ prefix) **140k** **160k** **180k** **200k** **220k** **240k** **260k** **280k** **300k**


512 5.23 5.56 5.87 6.16 6.44 6.70 6.95 7.19 7.42
1024 6.90 7.34 7.75 8.13 8.49 8.84 9.17 9.49 9.80
1536 8.11 8.63 9.11 9.56 9.99 10.40 10.79 11.16 11.52
2048 9.10 9.68 10.22 10.73 11.21 11.67 12.10 12.52 12.93
2560 9.95 10.59 11.17 11.73 12.26 12.76 13.23 13.69 14.13



verification latency is small, the method requires
frequent similarity computations during chunkwise generation. These repeated interventions fragment GPU kernel execution, prevent sustained high
utilization, and increase the base generation time
from 33.20s to 40.64s.


**Efficiency and implementation of STOP.** In contrast, the proposed STOP module introduces a minimal verification latency of 0.20s. By reusing the
resident KV cache, STOP performs verification by
processing the sequence _Ts_ in a single forward pass.
During standard generation, the LoRA adapter remains disabled to strictly preserve the behavior of
the base model and is activated only during the
verification step. The prefix KV cache serves as
a shared and immutable reference, and verification appends _Ts_ to a temporary view of this cache
to compute the score. Once scoring is complete,



the temporary branch is discarded. This design
removes the need for context rollbacks or cache
cleanup operations, ensuring that verification introduces no structural overhead into the generation
pipeline. As a result, the total wall-clock time of
STOP (34.33s) remains close to that of the baseline.


**Memory Footprint and Deployment Complex-**
**ity.** Beyond temporal latency, the spatial overhead
of model deployment is a decisive factor. Methods relying on external verifiers (Type II) impose a
**dual-model burden** : deploying Type II (External
PRM) requires hosting a separate PRM alongside
the generator. For example, using a 7B generator
with a 7B reward model effectively doubles the
VRAM requirement and increases orchestration
complexity. In contrast, STOP is implemented as
a lightweight LoRA adapter attached directly to


Table 15: **AIME** **(Math,** **Long-Horizon).** Recommended inverse retention ratios ( _γ_ _[−]_ [1] ) for tasks with longer
reference lengths ( _L_ task _≈_ 11 _,_ 950). Pruning is more conservative (lower values) due to higher reasoning complexity.


**Compute Budget** _C_ **(Total Tokens)**
**Prefix Length**

( _L_ prefix) **200k** **250k** **300k** **350k** **400k** **450k** **500k** **550k** **600k**


1024 1.87 2.07 2.25 2.42 2.57 2.71 2.85 2.98 3.10
2048 2.47 2.73 2.97 3.19 3.39 3.58 3.76 3.93 4.09
3072 2.90 3.21 3.49 3.75 3.99 4.21 4.42 4.62 4.81
4096 3.25 3.60 3.92 4.21 4.48 4.72 4.96 5.18 5.39
5120 3.56 3.94 4.29 4.60 4.89 5.17 5.42 5.66 5.90


Table 16: **Breakdown of Inference Latency and Throughput.** Note the discrepancy between _explicit cost_ and
_system impact_ for heuristic methods. Although Type I (SlimSC) shows a low explicit verification cost (1.74%), the
pipeline fragmentation significantly slows down generation, causing a massive **17.71% drop in throughput** . In
contrast, STOP operates in-situ, keeping the throughput drop minimal ( _<_ 3%) with negligible verification cost
(0.59%).


**Method** **Gen.** **Time (s)** **Verify Latency (s)** **Total Time (s)** **Throughput (tok/s)** **Throughput Drop (** _↓_ **)** **Explicit Verify Cost**


**Baseline** (No Pruning) 33.20    - 33.20 986.9    -    

Type I (SlimSC) 40.64 0.38 41.02 812.1 **17.71%** 1.74%
Type II (LaBoR) 33.53 1.13 34.68 977.3 0.97% 3.37%
Type IV ( **STOP** ) 34.13 **0.20** 34.33 **960.1** **2.71%** **0.59%**



the frozen generator. This **integrated architecture**
adds only a minimal number of parameters, incurring **negligible additional VRAM overhead** for
model weights. It eliminates the need for managing secondary inference services, making STOP a
"plug-and-play" solution for existing pipelines.


**G** **Extended Attention Analysis**


In Section 5.3, we hypothesize that the **STOP** module acts as a process-oriented evaluator. To empirically validate this, we analyze the attention patterns
in Figure 10.
**Universal Attention Pattern.** Consistent with the
findings in Section 5.3, **STOP** exhibits a broad attention pattern across all samples. Regardless of
the score, the module consistently tracks structural
discourse markers (e.g., “Wait”, “Hmm”, “Therefore”, “but”, “\n\n”) as well as the final answer
text. This confirms that the module monitors the
structural progression of the reasoning chain.
**Distinguishing** **Quality** **via** **Attention** **Focus.**
However, a critical distinction determines the quality score. In **High-Scoring** **Trajectories** (Figures 10a and c), attention prioritizes **logical nega-**
**tions** (e.g., “don’t” and “doesn’t”)—which serve
as cognitive pivots—over the final answer options,
indicating that **STOP** values the validity of the
logical derivation. Conversely, **Low-Scoring Tra-**
**jectories** (Figures 10b and d) exhibit a pattern of
**premature closure** : attention disproportionately
fixates on the **answer options themselves** (e.g., the



token “C”) while neglecting the reasoning context,
serving as a robust signal for identifying guessing
behavior.


(a) **High-scoring Case.** The module focuses on the logical
negation “don’t” (a cognitive pivot) rather than simply jumping to the answer option.


(c) **High-scoring Case.** Similar to (a), the module attends to
the logical marker “doesn’t,” prioritizing the validity of the
reasoning process over the final outcome.



(b) **Low-scoring** **Case.** Attention concentrates heavily on
the answer option itself (“C”), ignoring the sparse reasoning
context.


(d) **Low-scoring Case.** The module demonstrates premature
closure by fixating on the terminal choice (“C”) while bypassing critical logical intermediates.



Figure 10: **Extended Visualization of [STOP] Attention Maps.** While **STOP** broadly tracks structural markers
(e.g., “Wait”, “Therefore”) in all cases, it distinguishes reasoning quality by focus: **High-scoring** **paths** (left)
prioritize logical pivots (e.g., “don’t”), whereas **Low-scoring paths** (right) exhibit **premature closure** by fixating
on the terminal answer options.


