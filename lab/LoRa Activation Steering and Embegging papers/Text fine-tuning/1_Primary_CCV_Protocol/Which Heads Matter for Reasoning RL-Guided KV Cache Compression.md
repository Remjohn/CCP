## **Which Heads Matter for Reasoning? RL-Guided KV Cache Compression**

**Wenjie Du** [1] **Li Jiang** [2 3] **Keda Tao** [1 4] **Xue Liu** [2 5] **Huan Wang** [1]


[https://kurt232.github.io/RLKV](https://kurt232.github.io/RLKV)



**Abstract**


Reasoning large language models exhibit complex reasoning behaviors via extended chain-ofthought generation that are highly fragile to information loss during decoding, creating critical
challenges for KV cache compression. Existing
token-dropping methods directly disrupt reasoning chains by removing intermediate steps, while
head-reallocation methods, designed for retrieval
tasks, fail to preserve the heads essential for generative reasoning. However, no existing method can
identify which attention heads genuinely maintain
reasoning consistency and control generation termination. To address this, we propose RLKV,
which uses reinforcement learning as a probe
to discover which heads contribute to reasoning
quality by directly optimizing their cache usage
against actual generation outcomes. This discovery naturally leads to an efficient compression
strategy: we allocate full KV cache to reasoningcritical heads while aggressively compressing others. Experiments reveal that a fraction of heads
proves essential for reasoning, enabling **20–50%**
cache reduction with near-lossless performance
and up to **1.21** _×_ speedup.


**1. Introduction**


Recent advanced reasoning large language models (LLMs)
(Jaech et al., 2024; Team et al., 2025; Guo et al., 2025; DeepMind, 2025) exhibit complex reasoning behaviors, such as
self-reflection to revisit previous steps and exploration of
alternative approaches, and achieve revolutionary performance on challenging mathematical and coding problems.
However, this breakthrough comes at a cost: the extended
chain-of-thought (CoT) reasoning generates significantly
more tokens compared to instruct models, creating substan

1Westlake University 2McGill University 3Mila  - Quebec
AI Institute [4] Zhejiang University [5] Mohamed bin Zayed University of Artificial Intelligence. Correspondence to: Huan Wang
_<_ wanghuan@westlake.edu.cn _>_ .


_Preprint._ _February 2, 2026._



tial deployment challenges. More critically, these extended
reasoning chains prove highly fragile to information loss,
where KV cache compression methods that work well for
instruct models severely degrade reasoning scenarios.


As illustrated in Figure 1 (a), existing KV cache compression methods typically follow one of two strategies: token
dropping or head reallocation. Token-dropping methods
selectively evict less important tokens from each head’s KV
cache (Zhang et al., 2023; Li et al., 2024; Cai et al., 2025;
Yang et al., 2024b; Qin et al., 2024), while head-reallocation
methods identify critical heads and allocate full KV cache
to them, applying compressed KV cache to the remaining
heads. However, as shown in Figure 1 (b, left), two representative methods, including token-dropping method RKV (Cai et al., 2025) and head-reallocation method DuoAttention (Xiao et al., 2024), degrade significantly when applied to reasoning models, while maintaining stable performance on their instruct counterparts. In the MBPP (Austin
et al., 2021) coding task, both model variants achieve nearly
identical uncompressed performance. This controlled comparison isolates extended CoT generation as the primary
cause of compression challenges, rather than differences in
model capability. In reasoning models, the KV cache serves
not merely as computational optimization but as the carrier
of reasoning behaviors, storing critical states for CoT consistency and controlling generation flow. This fundamental
shift raises a critical question: **which KV attention heads**
**matter for reasoning behaviors?**


Existing methods fail to answer this question due to fundamental limitations in their design. As illustrated in Figure 1 (b, right), the two compression strategies exhibit distinct error modes as compression rates increase. Models
with token-dropping methods (R-KV) apply compression
uniformly across all heads by selectively evicting tokens,
inevitably discarding reasoning-critical information that disrupts CoT consistency and leads to repetitive loops that fail
to progress toward solutions. Although the R-KV approach
(Cai et al., 2025) is designed specifically for reasoning models, it still cannot escape this inherent limitation. In contrast,
models with head-reallocation compression preserve complete sequence information in selected heads by allocating
full KV cache to them while compressing others. This
approach maintains more coherent reasoning than token


1


**Which Heads Matter for Reasoning?** **RL-Guided KV Cache Compression**























_Figure 1._ **(a) Overviews of Two Methods** _Left:_ Token-dropping method removes less important tokens from each head’s KV cache.
_Right:_ Head-reallocation method allocates full KV cache to critical heads while assigning constant-size KV cache to the remaining heads.
**(b) Case study.** _Left:_ The token-dropping method (R-KV) and the head-reallocation method (DuoAttention) maintain relatively stable
performance on Llama-3.1-8B-Inst but degrade substantially on Llama-3.1-8B-R1, largely due to the longer generations produced by
the reasoning model. _Right:_ In terms of error modes, the token-dropping method (R-KV) tends to degenerate into repetitive behavior
whereas the head-reallocation method (DuoAttention) often produces over-extended CoT that exhausts the length budget without reaching
a correct solution. See Section A for complete results.



dropping, but remains ineffective: for problems that the
uncompressed model can solve, the compressed model goes
astray in its reasoning process and is unable to reach a solution within the maximum budget. This failure stems from
their head identification mechanisms, which target retrieval
heads (Wu et al., 2024) for recall tasks. This motivates our
key insight: **identifying reasoning-critical heads requires**
**directly observing how each head’s compression affects**
**actual reasoning outcomes during generation.**


To achieve this, we propose RLKV, which employs reinforcement learning (RL) as a probe to directly observe the
relationship between each head’s KV cache compression
and reasoning quality. As illustrated in Figure 2, our method
generates reasoning samples during RL training and assigns
rewards based on their quality. These reward signals guide
the optimization of learnable gating adapters that control
the mixing of full attention and compressed local attention for each head, with L1 penalty encouraging sparsity.
Through this RL optimization process, the learned gating
scores reveal a critical insight: only a small subset of heads
requires full KV cache to maintain reasoning consistency,
while others can be aggressively compressed without performance loss. We term these heads requiring full cache
as **reasoning-critical heads** . Our method naturally translates this finding into an efficient compression strategy: we
allocate full KV cache to reasoning-critical heads while applying compressed constant KV cache to others, effectively
preserving reasoning behaviors during inference.


Our work makes three main contributions: **First**, we introduce RLKV, a novel method that employs lightweight
reinforcement learning as a probe to identify reasoningcritical heads. It functions by directly observing how cache
compression impacts reasoning quality during generation.
**Second**, RLKV achieves state-of-the-art compression performance, enabling near-lossless reasoning with a 20–50%
reduction in KV cache usage across diverse tasks and mod


els. It also delivers a **1.09–1.21** _×_ end-to-end speedup in
practice. **Third**, to our knowledge, RLKV is the first to identify specific attention heads essential for reasoning. Through
comprehensive analyses of performance, head sensitivity,
error modes, and response length, we provide a new perspective on understanding reasoning models from a KV cache
compression viewpoint.


**2. Related Work**


**Efficient LLM Inference.** Various techniques reduce KV
cache overhead through architectural or system optimizations. Grouped-Query Attention (GQA) (Ainslie et al.,
2023) and Multi-head Latent Attention (MLA) (Liu et al.,
2024a) reduce the number of KV heads by sharing them
across query heads, achieving significant memory reduction
but requiring expensive pre-training from scratch. Linear
attention methods (Gu & Dao, 2023; Yang et al., 2025b)
maintain constant memory usage during inference by avoiding the quadratic attention computation, but exhibit reduced
modeling capacity compared to standard transformer architectures. KV cache quantization (Liu et al., 2024b; Tao et al.,
2025; Hooper et al., 2024; Duanmu et al., 2024; Su et al.,
2025; Yue et al., 2024) and system-level optimizations, such
as paged KV cache (Kwon et al., 2023), KV cache reuse
(Zheng et al., 2024), and sparsely loading KV cache (Tang
et al., 2024b), provide orthogonal improvements by reducing the precision or optimizing the storage and retrieval
methods of cached states. While sparse attention methods
(Child et al., 2019; Beltagy et al., 2020; Lu et al., 2025; Yuan
et al., 2025) further accelerate inference by utilizing intrahead sparsity, they often still require full KV cache storage.
Ultimately, these methods treat KV cache as opaque data
without exploiting the inherent head-level sparsity patterns.


**KV Cache Compression.** Recent works mainly exploit
sparsity in long-context scenarios for instruct models, including token-dropping and head-reallocation methods. (1)



2


**Which Heads Matter for Reasoning?** **RL-Guided KV Cache Compression**











































_Figure 2._ **Overview of RLKV:** Our method proposes to utilize RL as a probe to identify reasoning-critical heads. The RL pipeline
naturally captures reasoning behaviors, since it samples the current model’s generations to produce reward signals. The reward function
evaluates the samples to assess reasoning quality. We employ _L × H_ learnable gating adapters to mix full attention and local attention for
each head, quantifying each head’s reliance on full versus local KV cache access. We apply an L1 penalty to encourage adapter sparsity,
while RL optimizes the adapters to preserve reasoning behaviors. After training, we identify reasoning-critical heads with high adapter
values and allocate full KV cache to them while applying compressed KV cache to others for efficient inference.



Token-dropping methods (Zhang et al., 2023; Li et al., 2024;
Cai et al., 2025; Yang et al., 2024b; Qin et al., 2024) apply
eviction strategies across all heads or intra-layer heads based
on attention scores. H2O (Zhang et al., 2023) maintains important tokens’ KV cache based on accumulated attention
scores plus a sliding window for recent tokens. Specifically, recent R-KV (Cai et al., 2025), designed for reasoning
models, primarily adds similarity-based clustering to priority evict redundancy tokens’ KV cache during both prefill
and decoding phases. However, they inevitably discard
reasoning-critical information and disrupt the CoT consistency as compression rates increase. (2) head-reallocation
methods (Fu et al., 2024; Tang et al., 2024a; Xiao et al.,
2024; Bhaskar et al., 2025) maintain full KV cache only for
identified retrieval heads (Wu et al., 2024) in long-context
scenarios while applying compressed KV cache (Xiao et al.,
2023) to others. Ada-KV (Fu et al., 2024) and RazorAttention (Tang et al., 2024a) use proxy metrics of attention
scores, while DuoAttention (Xiao et al., 2024) and PruLong
(Bhaskar et al., 2025) are learning-based methods for head
identification. DuoAttention minimizes single-forward output deviation on a synthetic long-context recall task, while
PruLong uses next-token loss on long-context pre-training
corpora. However, these methods do not capture the reasoning behaviors that emerge during dynamically extending
CoT generation, resulting in degraded reasoning performance as compression rates increase.


**Reinforcement Learning for Efficiency.** RL has proven
effective in Neural architecture search (Zoph & Le, 2017;
Zoph et al., 2018), where it treats architecture choices as
sequential decisions, and model pruning (He et al., 2018),
where it learns layer-wise pruning ratios that maximize accuracy under resource constraints. However, the limitation
is the high computational cost due to the large optimization



space. Our work utilizes gating values assigned to each KV
head to reduce the optimization space and make RL feasible and efficient. For reasoning language models, recent
works apply RL tuning to mitigate overthinking (Hou et al.,
2025; Liu et al., 2025) by learning to reduce CoT length
while maintaining reasoning capability, thereby indirectly
decreasing KV cache requirements. Our work is orthogonal to these methods, employing lightweight RL training
to identify reasoning-critical heads that guide KV cache
compression while preserving reasoning capability.


**3. Methodology**


In this section, we present RLKV, a novel reasoning-critical
head identification method to guide efficient KV cache compression for reasoning LLMs, as illustrated in Figure 2.
In this paper, we operationally define “ **reasoning-critical**
**heads** ” as the KV heads that:


significantly degrade reasoning

performance under local KV cache

access.


These identified reasoning-critical heads are essential for
reasoning behaviors, which naturally require a full KV cache
to maintain CoT consistency, while others are compressible.
To achieve this, we first use mixed attention with gating
adapters to quantify each head’s reliance on complete or
compressed KV cache usage. Then we apply RL with sparsity pressure to optimize the gating adapters based on a
verifiable reward signal, naturally capturing reasoning behaviors. Finally, we introduce two complementary stabilization techniques to address the conflict between dense
regularization and sparse rewards as the sparsity increases.



3


**Which Heads Matter for Reasoning?** **RL-Guided KV Cache Compression**



**3.1. Mixed Attention with Gating Adapters**


Identifying reasoning-critical heads requires estimating the
sensitivity to complete KV cache usage of individual KV
heads; therefore, we employ an extra gating parameter
_αl,h_ _∈_ [0 _,_ 1] _[L][×][H]_ to each head _h_ and each layer _l_ after
scaled dot product attention(Yuan et al., 2025; Xiao et al.,
2024; Lu et al., 2025; Qiu et al., 2025). And we can construct the full KV cache and local KV cache access via
attention mask ( **M** _casual_ and **M** _local_ ):


out mix ~~a~~ ttn _i,j_ = _αi,j_ _·_ out ~~f~~ ull ~~a~~ ttn +

(1)
(1 _−_ _αi,j_ ) _·_ out local ~~a~~ ttn


which uses lightweight gating adapters to quantify each
head’s reliance on full versus local KV cache access. We
use the local attention mask (Xiao et al., 2023) with the
constant initial sink tokens and recent tokens for numeric
stability. This design dramatically reduces the optimization
space to only _L × H_ gating parameters by freezing all LLM
parameters, making it feasible to apply RL for identifying
reasoning-critical heads.


**3.2. RL for Reasoning Head Identification**


Qwen-2.5-7B-R1 Llama-3.1-8B-R1 Qwen-3-4B-Thinking


_Figure 3._ Gating score distribution after RLKV training on three
models, all of which adopt the GQA architecture. Qwen-2.5-7BR1 has 4 KV heads per layer across 28 layers with a group size
of 8. Llama-3.1-8B-R1 has 8 KV heads per layer across 32 layers
with a group size of 4. Qwen-3-4B-Thinking has 8 KV heads per
layer across 36 layers with a group size of 4. Qwen-2.5-7B-R1
exhibits inherent limitations in achievable sparsification without
compromising reasoning behavior, due to its substantially fewer
KV heads and larger KV group size.


Reasoning LLMs are often post-trained using reinforcement
learning with verifiable reward (RLVR) (Guo et al., 2025;
Team et al., 2025), which enhances reasoning capabilities
by evaluating generated samples based solely on final answer correctness. During this RL training process, reasoning behaviors are naturally exhibited in the sampled CoT
sequences, while reward signals directly reflect reasoning
quality. These two characteristics make RLVR ideal for
reasoning-critical heads identification.



In concrete, we optimize the gating adapters _**α**_ using Group
Relative Policy Optimization (GRPO) (Shao et al., 2024) on
mathematical reasoning problems with two key modifications. First, to maximize the discriminative power of reward
signals for _reasoning head_ identification, we remove the KL
penalty that conventionally limits reward signal strength to
prevent over-optimization. Second, we apply L1 regularization (Tibshirani, 1996) to the adapters by incorporating
the scaled L1 penalty term _β_ = _∥_ _**α**_ _∥_ 1 _/_ ( _L × H_ )into the
objective function to encourage adapter sparsity. The reward signal preserves high _αi,j_ values for reasoning-critical
heads requiring full KV cache access, while the L1 penalty
drives _αi,j_ toward 0 for compressible heads.


The overall objective is defined to maximize:


|Stabilized Adapter Avg.<br>Original Adapter Avg.|Stabilized Reward Avg.<br>Original Reward Avg.|
|---|---|
|||
|||
|||
|||
|**Collapsing**||
|||



_Figure_ _4._ The conflict of sparse reward versus dense penalty
leads to training collapse without our stabilization techniques. As
adapters become sparse (decreasing average), model performance
degrades (dropping reward), creating a vicious cycle where dense
L1 penalties dominate increasingly sparse rewards.



_β_

_−_
_L × H_ _[∥]_ _**[α]**_ _[∥]_ [1]

 - L1 penalty��  


1

_G_




- _i_ =1 _G_ min - _ππ_ _**αα**_ old(( _ooi|iq|q_ )) _[A][i][,]_ [ clip] - _ππ_ _**αα**_ old(( _ooi|iq|q_ )) _[,]_ [ 1] _[ −]_ _[ϵ,]_ [ 1 +] _[ ϵ]_ - _Ai_








- reward signal�� 


(2)
where _q_ is the input query, _{oi}_ _[G]_ _i_ =1 [are sampled outputs,] _[ A][i]_
is the normalized advantage, computed using a group of
rewards _{r_ 1 _, r_ 2 _, · · ·_ _, rG}_ tailored to outputs:


_[, r][G]_ [)]
_Ai_ = _[r][i][ −]_ [mean][(] _[r]_ [1] _[, r]_ [2] _[,][ · · ·]_ _._ (3)

std( _r_ 1 _, r_ 2 _, · · ·_ _, rG_ )


The clipping mechanism with threshold _ϵ_ prevents excessive
policy updates, and _β_ controls the regularization strength.
The policy _π_ _**α**_ represents the model’s generation probability
distribution conditioned on the current gating parameters
_**α**_, and the advantage _Ai_ is positive for outputs leading
to correct reasoning and negative for incorrect reasoning.
This optimization naturally converges to a sparse solution
where reasoning-critical heads maintain high _α_ values, as
demonstrated in Figure 3.


**3.3. Stabilization for RL Training**


Sparse Reward versus Dense Penalty



1.0


0.9


0.8


0.7


0.6


0.5


0.4



0 25 50 75 100 125 150 175
Training Steps







1.0


0.8


0.6


0.4


0.2


0.0



4


**Which Heads Matter for Reasoning?** **RL-Guided KV Cache Compression**



As adapters become increasingly sparse, the mixed attention
of reasoning-critical heads degenerates to the streaming attention, severely degrading the model’s reasoning capacity,
as shown in Figure 4. This degradation renders the reward
signal increasingly sparse and unstable, while the L1 penalty
remains dense across all parameters. This imbalance creates a vicious cycle, where degraded performance leads to
sparser rewards, making the dense L1 penalty relatively
stronger, which further drives adapters toward zero with
no recovery capability. To resolve this destructive training
dynamic and stabilize the training process, we introduce
two complementary techniques that address this challenge
from both the reward and penalty perspectives.


**Self-distillation Sampling.** Overly challenging problems
during RL training lead to frequent failures and unstable reward signals. In contrast to typical RLVR that utilizes sparse
rewards for capability enhancement, our work leverages RL
for capability preservation under sparsity constraints. Consequently, we focus on constructing high-quality training
data that produces stable reward signals to improve learning
efficiency. We construct training data by first filtering all
problems the model initially solves correctly, then curating
them to 3k using a curriculum sampling strategy (Team et al.,
2025). We use output token lengths as a proxy for difficulty,
enabling curriculum control that maintains stable reward
signals throughout the training process. See Section 4.1 for
training dataset details.


**Adaptive Penalty Weighting.** To address the penalty imbalance, we modulate the scaling weight _β_ of the L1 penalty
based on the reward signal. Our design incorporates two
protective mechanisms to prevent training collapse. First,
we use adaptive scaling centered around a target reward of
_r_ ¯ _≈_ 0 _._ 7 to smoothly decay penalty when performance degrades and increase it when performance improves. Second,
we implement a hard cutoff at threshold _τ_ to completely
eliminate regularization when reasoning capability severely
degrades. We implement this through a dynamic weight that
replaces the constant hyperparameter _β_ :


_β_ _[′]_ (¯ _r, τ_ ) = I(¯ _r_ _> τ_ ) _· β ·_ (exp(¯ _r_ ) _−_ 1) _,_

(4)
_r_ ¯ = mean( _r_ 1 _, r_ 2 _, · · ·_ _, rG_ ) _,_


where the exponential function (exp(¯ _r_ ) _−_ 1) provides the
adaptive scaling, and the indicator function I(¯ _r_ _>_ _τ_ ) provides the hard cutoff based on mean reward ¯ _r_ in the current
group.


The end result is a set of identified reasoning-critical heads
that require full KV cache access, while less relevant heads
can utilize compressed KV cache access, achieving significant memory compression without sacrificing reasoning
capability. During inference, we use the learned gating parameters to rank all KV heads and select the top-k heads
with the highest _α_ values to maintain full KV cache access



according to the target compression ratio. The remaining
heads still use full attention but with compressed KV cache,
which retains only initial sink tokens and recent tokens.
Refer to Section 4.1 for further details of deployment and
inference.


**4. Experiments**


**4.1. Experimental Settings**


**Models,** **Datasets,** **and** **Baselines.** We evaluate RLKV
on three mainstream small-scale reasoning models: Llama3.1-8B-R1 (Guo et al., 2025), Qwen-2.5-7B-R1 (Guo et al.,
2025), and Qwen-3-4B-Thinking (Yang et al., 2025a). We
conduct experiments on four reasoning benchmarks as well
as four subsets of the challenge knowledge QA benchmark
MMLU-Pro (Wang et al., 2024). The reasoning benchmarks
include three mathematical reasoning datasets—GSM8K
(Cobbe et al., 2021) for elementary problems, Math500
(Lightman et al., 2023) for intermediate problems, and
AIME24 (MMA, 2024) for advanced problems—to evaluate
performance across difficulty levels, together with MBPP
(Austin et al., 2021) for Python programming to assess
generalization beyond the training domain. To further evaluate generalization, we additionally select four MMLU-Pro
subsets: Chemistry, Computer Science, Law, and Physics,
with up to 500 randomly sampled instances per subset.
We compare our method with KV cache compression approaches including H2O (Zhang et al., 2023) and R-KV
(Cai et al., 2025), which are typical token-dropping methods, and DuoAttention (Xiao et al., 2024), which is a headreallocation method. Given the significant length variation
in reasoning tasks (see Section E), fixed budgets lead to
inconsistent compression ratios. To address this, we adopt
H2O and R-KV with dynamic budgets to ensure fair comparison. As shown in Section F, this modification is crucial
for fairness and does not penalize the baselines; in fact, it
enhances their performance compared to fixed budgets.


**Implementation** **Details.** We implement RLKV in
AReaL(Fu et al., 2025) for RL training and SGLang(Zheng
et al., 2024) as the rollout engine, where the attention function is replaced by mixed attention. We optimize gating
adapters using GRPO with 4 samples per query and AdamW
(Loshchilov & Hutter, 2017) with learning rate 0 _._ 01. We
filter 3,000 mathematical problems from DeepScaleR (Luo
et al., 2025) following our curriculum sampling strategy.
And we train the models for 185 steps on 2 NVIDIA A100
GPUs (80GB) for several hours. During training, local attention uses 128 sink tokens and 256 local tokens; during
evaluation, we apply the compressed KV cache size with 16
sink tokens and 64 local tokens. We augment all baselines
with equivalent token overhead for fair evaluation. Details
are provided in Section B.



5


**Which Heads Matter for Reasoning?** **RL-Guided KV Cache Compression**


Full H2O R-KV DuoAttn Ours



GSM8K

(Math)

1.0
0.9
0.8
0.7
0.6
0.5
0.4
0.3
0.2
0.1
0.0
0.0 0.2 0.4 0.6 0.8



Math500

(Math)

0.9
0.8
0.7
0.6
0.5
0.4
0.3
0.2
0.1
0.0
0.0 0.2 0.4 0.6 0.8



0.0
0.0 0.2 0.4 0.6 0.8



0.6

0.5

0.4

0.3

0.2

0.1



0.6

0.5

0.4

0.3

0.2

0.1



0.4


0.3


0.2


0.1



0.5

0.4

0.3

0.2

0.1



0.5

0.4

0.3

0.2

0.1



AIME24

(Math)



MBPP
(Code)



MMLU-Pro

(Chem.)



MMLU-Pro

(CS)



MMLU-Pro

(Law)



MMLU-Pro

(Phys.)



0.7

0.6

0.5

0.4

0.3

0.2

0.1



0.0
0.0 0.2 0.4 0.6 0.8



0.0
0.0 0.2 0.4 0.6 0.8



0.0
0.0 0.2 0.4 0.6 0.8



0.0
0.0 0.2 0.4 0.6 0.8



0.0
0.0 0.2 0.4 0.6 0.8



GSM8K

(Math)

1.0
0.9
0.8
0.7
0.6
0.5
0.4
0.3
0.2
0.1
0.0
0.0 0.2 0.4 0.6 0.8



Math500

(Math)

1.0
0.9
0.8
0.7
0.6
0.5
0.4
0.3
0.2
0.1
0.0
0.0 0.2 0.4 0.6 0.8



0.0
0.0 0.2 0.4 0.6 0.8



0.3


0.2


0.1



0.6

0.5

0.4

0.3

0.2

0.1



AIME24

(Math)



MBPP
(Code)



MMLU-Pro

(Chem.)



MMLU-Pro

(CS)



MMLU-Pro

(Law)



MMLU-Pro

(Phys.)



0.7

0.6

0.5

0.4

0.3

0.2

0.1



0.0
0.0 0.2 0.4 0.6 0.8



0.7

0.6

0.5

0.4

0.3

0.2

0.1



0.0
0.0 0.2 0.4 0.6 0.8



0.7

0.6

0.5

0.4

0.3

0.2

0.1



0.0
0.0 0.2 0.4 0.6 0.8



0.0
0.0 0.2 0.4 0.6 0.8



0.7

0.6

0.5

0.4

0.3

0.2

0.1



0.0
0.0 0.2 0.4 0.6 0.8



GSM8K

(Math)

1.0
0.9
0.8
0.7
0.6
0.5
0.4
0.3
0.2
0.1
0.0
0.0 0.2 0.4 0.6 0.8



Math500

(Math)

0.9
0.8
0.7
0.6
0.5
0.4
0.3
0.2
0.1
0.0
0.0 0.2 0.4 0.6 0.8



0.0
0.0 0.2 0.4 0.6 0.8



MBPP
(Code)



MMLU-Pro



0.4


0.3


0.2


0.1



MMLU-Pro



(Phys.)



0.6

0.5

0.4

0.3

0.2

0.1



AIME24

(Math)



0.8
0.7
0.6
0.5
0.4
0.3
0.2
0.1
0.0
0.0 0.2 0.4 0.6 0.8



(Chem.)



0.7

0.6

0.5

0.4

0.3

0.2

0.1



0.0
0.0 0.2 0.4 0.6 0.8



MMLU-Pro

(CS)



MMLU-Pro

(Law)



0.9
0.8
0.7
0.6
0.5
0.4
0.3
0.2
0.1
0.0
0.0 0.2 0.4 0.6 0.8



KV Cache Budget Sparsity



0.0
0.0 0.2 0.4 0.6 0.8



0.8
0.7
0.6
0.5
0.4
0.3
0.2
0.1
0.0
0.0 0.2 0.4 0.6 0.8



_Figure 5._ **Main Results.** RLKV (Ours) achieves better accuracy-efficiency trade-off across four reasoning benchmarks (GSM8K, MATH,
AIME24, MBPP) and four subsets of the knowledge benchmark MMLU-Pro (Chemistry, Computer Science, Law, Physics).



**4.2. Main Results**


Figure 5 compares RLKV with baselines on four reasoning
benchmarks (GSM8K, Math500, AIME24, MBPP) and four
knowledge subsets of MMLU-Pro (Chemistry, Computer
Science, Law, Physics) at sparsity levels of 0.2, 0.4, 0.6, and
0.8. Complete numerical results are provided in Section C.
Overall, RLKV outperforms the baselines by up to 20%, and
on some tasks even surpasses the full KV cache baseline.


**Reasoning** **Tasks.** RLKV consistently outperforms all
methods across sparsity levels, with particularly strong advantages at high sparsity, such as 0.4 and 0.6, where baselines degrade substantially. Section 4.2 further summarizes
the near-lossless sparsity thresholds, showing that RLKV
achieves 20–50% KV cache reduction with near lossless
performance, while the baselines suffer a notable drop.


**Knowledge Tasks.** RLKV also maintains competitive accuracy on the four MMLU-Pro subsets across all sparsity
levels. This suggests the effectiveness and robustness of our
approach beyond the mathematical reasoning domain.









Qwen-3-4B-Thinking



0.9
0.8
0.7
0.6
0.5
0.4
0.3
0.2
0.1
0.0
0.0 0.1 0.2 0.3 0.4



0.0 0.1 0.2 0.3 0.4





KV Cache Budget Sparsity



Varying Seq Len (Sparsity: 0.5)



32k


16k


4k


2k


1k



Varying Sparsity (Seq Len: 16k)



0.8

0.7

0.6

0.5

0.4

0.3

0.2

0.1



2.0

1.8

1.6

1.4

1.2

1.0



|Col1|32k|Col3|Col4|
|---|---|---|---|
|||||
|||~~2k~~<br>4k<br>16k||
||||1k|
|||||
|||||
|||||


1.0 1.2 1.4
Latency Ratio ( better)



6

5

4

3

2

1



|0.8|Col2|Col3|
|---|---|---|
||||
||||
||0.7||
||0.|6|
||0.2<br>0.3<br>~~0.4~~|~~0.5~~|
||||


0.8 1.0 1.2
Latency Ratio ( better)



_Figure 6._ **Single-layer attention latency and throughput.** We
report results with FlashAttention-2. _Left_ : Fixed sequence length
at 16K, varying sparsity. _Right_ : Fixed sparsity at 0.5, varying
sequence length.



_Figure 7._ **Head sensitivity from high to low gating scores.** We
rank heads by the learned gating scores and progressively replace
the top fraction of heads with a compressed KV cache during
inference. We compare performance degradation with three control
groups: randomly initialized heads, retrieval heads identified by
DuoAttention, and reasoning-critical heads identified by RLKV.


**4.3. Inference Efficiency**


Figure 6 reports single-layer attention latency and throughput under head reallocation, where extra overhead comes
from regrouping _Q/K/V_ into full and compressed KV head
blocks, running attention separately, and concatenating outputs along the head dimension. Despite this, RLKV still
achieves end-to-end speedups in a vanilla inference pipeline
without quantization or continuous batching, as shown in
Table 2. We expect further gains with custom CUDA
kernels and by integrating head-reallocation attention into
continuous-batching engines such as SGLang (Zheng et al.,
2024) and vLLM (Kwon et al., 2023).


**4.4. Ablation Studies**


We conduct ablation studies on Math500 with Qwen-2.57B-R1 to evaluate three key components of RLKV: adaptive



6


**Which Heads Matter for Reasoning?** **RL-Guided KV Cache Compression**



Effect of Adaptive Penalty Weight







0.9

0.8

0.7

0.6

0.5

0.4

0.3

0.2

0.1



1.0

0.9

0.8

0.7

0.6

0.5

0.4

0.3

0.2

0.1








|Col1|Col2|Col3|Col4|Col5|
|---|---|---|---|---|
||||||
||||||
||||||
|~~Full~~<br>~~w/o a~~<br>|~~ daptive~~<br>||||
|<br>~~penal~~<br>~~RLKV~~|<br>~~ty weight~~<br>~~ (Ours)~~||||


|Col1|Col2|Col3|Col4|Col5|
|---|---|---|---|---|
||||||
||||||
||||||
|~~Full~~<br>~~w/o s~~<br>|~~ elf-distillati~~<br>|~~ on~~|||
|<br>~~samp~~<br>~~RLKV~~|<br>~~ling~~<br>~~ (Ours)~~||||


|Col1|Col2|Col3|Col4|Col5|Col6|
|---|---|---|---|---|---|
|||||||
|||||||
|||||||
|~~Full~~<br>~~beta~~<br>|~~ = 5e-3 (~~<br>|~~   larger)~~<br>||||
|~~beta~~<br>~~beta~~|~~  2e-4 (~~<br>~~ = 1e-3 (~~|~~   smaller)~~<br>~~   Ours)~~||||



0.0
0.0 0.2 0.4 0.6 0.8



0.9

0.8

0.7

0.6

0.5

0.4

0.3

0.2

0.1



0.0
0.0 0.2 0.4 0.6 0.8



0.0
0.0 0.2 0.4 0.6 0.8



KV Cache Budget Sparsity
_Figure 8._ **Ablation of key components in RLKV training.** We conduct ablation studies on Qwen-2.5-7B-R1 with evaluation on Math500.
_Left_ : Adaptive penalty weighting stabilizes training under sparsity. _Middle_ : Self-distillation sampling yields more stable reward signals
than using overly difficult problems. _Right_ : Base L1 penalty weight _β_ = 0 _._ 001 provides the best sparsity–performance trade-off.



penalty weighting, self-distillation sampling, and the base
L1 penalty weight.


**Adaptive** **Penalty** **Weighting.** Figure 8 (left) demonstrates that adaptive penalty weighting significantly enhances performance by breaking the vicious cycle between
sparse rewards and dense L1 penalty. Without this mechanism, increasing adapter sparsity leads to degraded reasoning performance, which generates sparser reward signals
while the L1 penalty remains dense, creating an imbalance
that drives training toward collapse without recovery.


**Self-distillation Sampling.** Self-distillation sampling provides stable reward signals throughout training, as shown
in Figure 8 (middle). In contrast to typical RLVR, training on problems suited to the model’s reasoning capability
maintains relatively stable reward signals throughout optimization, while training on challenging problems leads to
unstable and sparse reward signals that provide weak and
insufficient guidance for head identification.


**Base L1 penalty Weight.** The base regularization weight
_β_ controls the strength of the L1 penalty applied to gating
adapters during RL training. Figure 8 (right) shows that
a moderate _β_ value of 0.001 achieves an optimal balance
between sparsity and reward signal strength. Excessive
penalty ( _β_ = 0 _._ 005) dominates the optimization process,
weakening reward signals through over-compression, while
insufficient penalty ( _β_ = 0 _._ 0002) fails to induce adequate
sparsity, leading to premature convergence with limited
exploration of the reward landscape.


**5. Qualitative Analyses**


In this section, we provide qualitative analyses to understand
reasoning behaviors and reasoning models from a view of
KV cache compression.


**Head** **sensitivity.** Figure 7 quantifies how sensitive the
model is when compressing heads from high to low gating
scores. For Llama-3.1-8B-R1 and Qwen-2.5-7B-R1, replacing reasoning-critical heads causes a significantly sharper
performance drop than replacing retrieval or random heads,



confirming these heads are vital for maintaining reasoning
behaviors. In Qwen-3-4B-Thinking, although the sensitivity
of reasoning and retrieval heads is comparable, reasoningcritical heads remain more impactful; as shown in Figure 5,
preserving these heads leads to superior accuracy at high
sparsity. This indicates that the heads identified by RLKVare
the primary drivers of reasoning performance.


_Figure 9._ **Error modes induced by compressing different heads.**
We categorize failures into repetitive, incorrect, and overlength
errors, evaluated on instances that are solved correctly by the full
KV cache baseline. See Section D for complete details.


**Error modes.** We break down failures caused by KV cache
compression into three categories: repetitive errors (excessively repeating token sequences), incorrect errors (wrong
final answers), and overlength errors (generation exceeding
the maximum context length), as shown in Figure 13. Note
that this analyses focuses on samples that the full KV cache
baseline can solve correctly, while models using compressed
KV caches fail. Compressing retrieval heads primarily leads
to overlength errors, suggesting the model retains linguistic
fluency but fails to reason efficiently toward a conclusion
within the length budget. This observation also validates our
initial analyses regarding the shortcomings of DuoAttention
in reasoning models. Conversely, compressing reasoningcritical heads predominantly triggers repetitive and incorrect
errors. This indicates that the context within these heads is
essential for maintaining CoT consistency. Notably, overlength errors rarely occur in this group, implying that as
long as the reasoning behavior itself persists, the model
keeps the capacity to terminate the generation.



7


**Which Heads Matter for Reasoning?** **RL-Guided KV Cache Compression**



_Table 1._ **Near lossless performance achieved by RLKVacross**
**four** **reasoning** **benchmarks.** Red background denotes performance below the full KV cache baseline, whereas green background denotes performance above it. RLKV exhibits the smallest
performance degradation among the other methods and, on some
benchmarks, even improves over the full KV cache baseline. For
all values, higher is better. The best result of the metric in each
benchmark is in **bold** . All values are reported as percentages.


**(a) Llama-3.1-8B-R1**


Lossless Sparsity Threshold
Method

GSM8K Math500 AIME24 MBPP
0.4 0.5 0.4 0.4


**(b) Qwen-2.5-7B-R1**


Lossless Sparsity Threshold
Method

GSM8K Math500 AIME24 MBPP
0.4 0.4 0.2 0.3


**(c) Qwen-3-4B-Thinking**


Lossless Sparsity Threshold
Method

GSM8K Math500 AIME24 MBPP
0.5 0.5 0.5 0.5


**Average response length.** We analyze the average response
length on samples that remain correct under both the full
KV cache baseline and each compressed setting (model,
method and sparsity level). Figure 10 shows that tokendropping methods can appear to produce shorter outputs under aggressive compression, largely because they only solve
easier instances in those regimes. Although R-KV claims
to preserve effective information, it often results in longer
reasoning steps and poor performance. In contrast, DuoAttention often requires significantly longer reasoning steps to
reach correct solutions, paying a higher computational cost
for its retrieval-based allocation. Overall, RLKV maintains
strong accuracy with competitive response lengths, suggesting a better trade-off between capability preservation and
inference efficiency.


**6. Conclusion**


In this paper, we propose RLKV, a novel reasoning-critical
head identification method to guide KV cache compression



_Table 2._ **End-to-end speedup on Math500.** We report batch size,
peak GPU memory, latency, speedup, and accuracy for Llama3.1-8B-R1 at sparsity 0.5 using a vanilla PyTorch/Transformers +
FlashAttention-2 implementation.


Method Batch GPU (GB) Latency (s) Accuracy Speedup


Full 2 19.08 24,374 0.810
**1.16** _×_
RLKV 4 19.40 21,080 0.792


Full 4 23.57 16,838 0.784
**1.16** _×_
RLKV 8 23.84 14,569 0.792


Full 8 32.23 14,222 0.776
**1.21** _×_
RLKV 16 32.82 11,767 0.768


Full 16 49.79 11,752 0.770
**1.09** _×_
RLKV 32 50.88 10,809 0.764



_Figure_ _10._ **Average** **response** **length** **of** **correct** **samples.** We
report the average output length over samples that are answered
correctly under both the full KV cache baseline and each compressed setting.


in reasoning models. RLKV directly optimizes the relationship between each head’s KV cache usage and reasoning
quality through reinforcement learning and we achieve competitive performance on reasoning and knowledge tasks at
diverse KV cache budget sparsity levels. We further analyze
the head sensitivity of reasoning models, error modes of
instances solved by the uncompressed model, and the average response length of mutually correct samples across both
compressed and uncompressed settings Our findings reveal
the importance and complexity of reasoning-critical heads
in reasoning models. RLKV provides a new perspective on
understanding reasoning models and opens up new avenues
for efficient inference of reasoning LLMs.


**7. Future Work**


RLKV opens several avenues for future research. First,
subdividing reasoning-critical heads into more granular categories, such as retrieval or induction heads, could further
reveal the complex mechanisms of reasoning behaviors.
Second, transitioning from static gating scores to queryadaptive dynamic guidance is a promising direction, achievable with lightweight training rather than training models
from scratch (Yuan et al., 2025; Lu et al., 2025; Qiu et al.,
2025). Third, co-designing specialized kernels with headreallocation mechanisms could bridge the gap between theoretical cache reduction and actual end-to-end speedup.



**H2O** **R-KV** **DuoAttention** **RLKV**
Avg. Length of Uncompressed & Correct Samples



3k


2k


1k



6k



Qwen-3-4B-Thinking



Qwen-2.5-7B-R1



4k


2k



4k

3k

2k

1k



Llama-3.1-8B-R1



0
0.2 0.4 0.6 0.8



0
0.2 0.4 0.6 0.8



0
0.2 0.4 0.6 0.8



KV Cache Budget Sparsity



8


**Which Heads Matter for Reasoning?** **RL-Guided KV Cache Compression**



**Impact Statements**


RLKV seeks to identify reasoning-critical heads to reveal
inherent mechanisms underlying reasoning in reasoning
large language models and use those heads to guide KV
cache compression to improve the efficiency in reasoning
decoding. By reducing memory usage and computational
overhead during inference, this approach may contribute to
more environmentally sustainable deployment of large-scale
language models. As a KV cache compression technique,
RLKV may introduce some degree of performance degradation, as is common for efficiency methods. Such effects
can vary depending on downstream tasks and deployment
settings, and should therefore be carefully evaluated when
applied in real-world systems.


**References**


Ainslie, J., Lee-Thorp, J., de Jong, M., Zemlyanskiy, Y.,
Lebron, F., and Sanghai, S. Gqa: Training generalized
multi-query transformer models from multi-head checkpoints. In _EMNLP_, 2023.


Austin, J., Odena, A., Nye, M., Bosma, M., Michalewski,
H., Dohan, D., Jiang, E., Cai, C., Terry, M., Le, Q., et al.
Program synthesis with large language models. _arXiv_
_preprint arXiv:2108.07732_, 2021.


Beltagy, I., Peters, M. E., and Cohan, A. Longformer: The long-document transformer. _arXiv preprint_
_arXiv:2004.05150_, 2020.


Bhaskar, A., Wettig, A., Gao, T., Dong, Y., and Chen,
D. Cache me if you can: How many kvs do you
need for effective long-context lms? _arXiv_ _preprint_
_arXiv:2506.17121_, 2025.


Cai, Z., Xiao, W., Sun, H., Luo, C., Zhang, Y., Wan, K.,
Li, Y., Zhou, Y., Chang, L.-W., Gu, J., et al. R-kv:
Redundancy-aware kv cache compression for trainingfree reasoning models acceleration. _arXiv_ _preprint_
_arXiv:2505.24133_, 2025.


Child, R., Gray, S., Radford, A., and Sutskever, I. Generating long sequences with sparse transformers. _arXiv_
_preprint arXiv:1904.10509_, 2019.


Cobbe, K., Kosaraju, V., Bavarian, M., Chen, M., Jun, H.,
Kaiser, L., Plappert, M., Tworek, J., Hilton, J., Nakano,
R., et al. Training verifiers to solve math word problems.
_arXiv preprint arXiv:2110.14168_, 2021.


DeepMind, G. Gemini.
https://deepmind.google/models/gemini/, 2025.


Duanmu, H., Yuan, Z., Li, X., Duan, J., Zhang, X., and
Lin, D. Skvq: Sliding-window key and value cache



quantization for large language models. _arXiv preprint_
_arXiv:2405.06219_, 2024.


Dubey, A., Jauhri, A., Pandey, A., et al. The Llama 3 Herd
of Models, July 2024.


Fu, W., Gao, J., Shen, X., Zhu, C., Mei, Z., He, C., Xu, S.,
Wei, G., Mei, J., Wang, J., et al. Areal: A large-scale
asynchronous reinforcement learning system for language
reasoning. _arXiv preprint arXiv:2505.24298_, 2025.


Fu, Y., Cai, Z., Asi, A., Xiong, W., Dong, Y., and Xiao, W.
Not all heads matter: A head-level kv cache compression
method with integrated retrieval and reasoning. _arXiv_
_preprint arXiv:2410.19258_, 2024.


Gu, A. and Dao, T. Mamba: Linear-time sequence
modeling with selective state spaces. _arXiv_ _preprint_
_arXiv:2312.00752_, 2023.


Guo, D., Yang, D., Zhang, H., Song, J., Zhang, R., Xu, R.,
Zhu, Q., Ma, S., Wang, P., Bi, X., et al. Deepseek-r1: Incentivizing reasoning capability in llms via reinforcement
learning. _arXiv preprint arXiv:2501.12948_, 2025.


Guo, J., Tang, H., Yang, S., Zhang, Z., Liu, Z., and Han,
S. Block Sparse Attention. [https://github.com/](https://github.com/mit-han-lab/Block-Sparse-Attention)
[mit-han-lab/Block-Sparse-Attention,](https://github.com/mit-han-lab/Block-Sparse-Attention)
2024.


He, Y., Lin, J., Liu, Z., Wang, H., Li, L.-J., and Han, S.
Amc: Automl for model compression and acceleration
on mobile devices. In _ECCV_, 2018.


Hooper, C. R. C., Kim, S., Mohammadzadeh, H., Mahoney,
M. W., Shao, S., Keutzer, K., and Gholami, A. Kvquant:
Towards 10 million context length llm inference with kv
cache quantization. In _NeurIPS_, 2024.


Hou, B., Zhang, Y., Ji, J., Liu, Y., Qian, K., Andreas,
J., and Chang, S. Thinkprune: Pruning long chain-ofthought of llms via reinforcement learning. _arXiv preprint_
_arXiv:2504.01296_, 2025.


Jaech, A., Kalai, A., Lerer, A., Richardson, A., El-Kishky,
A., Low, A., Helyar, A., Madry, A., Beutel, A., Carney, A., et al. Openai o1 system card. _arXiv_ _preprint_
_arXiv:2412.16720_, 2024.


Kwon, W., Li, Z., Zhuang, S., Sheng, Y., Zheng, L., Yu,
C. H., Gonzalez, J., Zhang, H., and Stoica, I. Efficient
memory management for large language model serving
with pagedattention. In _Proceedings of the 29th sympo-_
_sium on operating systems principles_, 2023.


Li, Y., Huang, Y., Yang, B., Venkitesh, B., Locatelli, A., Ye,
H., Cai, T., Lewis, P., and Chen, D. Snapkv: Llm knows
what you are looking for before generation. _NeurIPS_,
2024.



9


**Which Heads Matter for Reasoning?** **RL-Guided KV Cache Compression**



Lightman, H., Kosaraju, V., Burda, Y., Edwards, H., Baker,
B., Lee, T., Leike, J., Schulman, J., Sutskever, I., and
Cobbe, K. Let’s verify step by step. In _ICLR_, 2023.


Liu, A., Feng, B., Wang, B., Wang, B., Liu, B., Zhao, C.,
Dengr, C., Ruan, C., Dai, D., Guo, D., et al. Deepseek-v2:
A strong, economical, and efficient mixture-of-experts
language model. _arXiv_ _preprint_ _arXiv:2405.04434_,
2024a.


Liu, W., Zhou, R., Deng, Y., Huang, Y., Liu, J., Deng, Y.,
Zhang, Y., and He, J. Learn to reason efficiently with
adaptive length-based reward shaping. _arXiv_ _preprint_
_arXiv:2505.15612_, 2025.


Liu, Z., Yuan, J., Jin, H., Zhong, S., Xu, Z., Braverman, V.,
Chen, B., and Hu, X. Kivi: A tuning-free asymmetric
2bit quantization for kv cache. In _ICML_, 2024b.


Loshchilov, I. and Hutter, F. Decoupled weight decay regularization. _arXiv preprint arXiv:1711.05101_, 2017.


Lu, E., Jiang, Z., Liu, J., Du, Y., Jiang, T., Hong, C., Liu,
S., He, W., Yuan, E., Wang, Y., et al. Moba: Mixture
of block attention for long-context llms. _arXiv preprint_
_arXiv:2502.13189_, 2025.


Luo, M., Tan, S., Wong, J., Shi, X., Tang, W., Roongta,
M., Cai, C., Luo, J., Zhang, T., Li, E., Popa, R. A.,
and Stoica, I. Deepscaler: Surpassing o1-preview
with a 1.5b model by scaling rl, 2025. URL
[https://pretty-radio-b75.notion.site/](https://pretty-radio-b75.notion.site/DeepScaleR-Surpassing-O1-Preview\-with-a-1-5B-Model-by-Scaling-RL-\19681902c1468005bed8ca303013a4e2)

[DeepScaleR-Surpassing-O1-Preview\](https://pretty-radio-b75.notion.site/DeepScaleR-Surpassing-O1-Preview\-with-a-1-5B-Model-by-Scaling-RL-\19681902c1468005bed8ca303013a4e2)

[-with-a-1-5B-Model-by-Scaling-RL-\](https://pretty-radio-b75.notion.site/DeepScaleR-Surpassing-O1-Preview\-with-a-1-5B-Model-by-Scaling-RL-\19681902c1468005bed8ca303013a4e2)
[19681902c1468005bed8ca303013a4e2.](https://pretty-radio-b75.notion.site/DeepScaleR-Surpassing-O1-Preview\-with-a-1-5B-Model-by-Scaling-RL-\19681902c1468005bed8ca303013a4e2) Notion
Blog.


MMA. American invitational mathematics examination  - aime, February 2024. URL
[https://maa.org/math-competitions/](https://maa.org/math-competitions/american-invitational-mathematics\-examination-aime)

[american-invitational-mathematics\](https://maa.org/math-competitions/american-invitational-mathematics\-examination-aime)
[-examination-aime.](https://maa.org/math-competitions/american-invitational-mathematics\-examination-aime)


Qin, Z., Cao, Y., Lin, M., Hu, W., Fan, S., Cheng, K., Lin,
W., and Li, J. Cake: Cascading and adaptive kv cache
eviction with layer preferences. In _ICLR_, 2024.


Qiu, Z., Wang, Z., Zheng, B., Huang, Z., Wen, K., Yang, S.,
Men, R., Yu, L., Huang, F., Huang, S., et al. Gated attention for large language models: Non-linearity, sparsity,
and attention-sink-free. In _NeurIPS_, 2025.


Shao, Z., Wang, P., Zhu, Q., Xu, R., Song, J., Bi, X., Zhang,
H., Zhang, M., Li, Y., Wu, Y., et al. Deepseekmath: Pushing the limits of mathematical reasoning in open language
models. _arXiv preprint arXiv:2402.03300_, 2024.



Su, Z., Chen, Z., Shen, W., Wei, H., Li, L., Yu, H., and
Yuan, K. Rotatekv: Accurate and robust 2-bit kv cache
quantization for llms via outlier-aware adaptive rotations.
_arXiv preprint arXiv:2501.16383_, 2025.


Tang, H., Lin, Y., Lin, J., Han, Q., Ke, D., Hong, S., Yao,
Y., and Wang, G. Razorattention: Efficient kv cache
compression through retrieval heads. In _ICLR_, 2024a.


Tang, J., Zhao, Y., Zhu, K., Xiao, G., Kasikci, B., and Han,
S. Quest: query-aware sparsity for efficient long-context
llm inference. In _ICML_, 2024b.


Tao, K., You, H., Sui, Y., Qin, C., and Wang, H. Plug-andplay 1. x-bit kv cache quantization for video large language models. _arXiv preprint arXiv:2503.16257_, 2025.


Team, K., Du, A., Gao, B., Xing, B., Jiang, C., Chen, C.,
Li, C., Xiao, C., Du, C., Liao, C., et al. Kimi k1. 5:
Scaling reinforcement learning with llms. _arXiv preprint_
_arXiv:2501.12599_, 2025.


Tibshirani, R. Regression shrinkage and selection via the
lasso. _Journal of the Royal Statistical Society Series B:_
_Statistical Methodology_, 58(1):267–288, 1996.


Wang, Y., Ma, X., Zhang, G., Ni, Y., Chandra, A., Guo,
S., Ren, W., Arulraj, A., He, X., Jiang, Z., et al. Mmlupro: A more robust and challenging multi-task language
understanding benchmark. In _NeurIPS_, 2024.


Wu, W., Wang, Y., Xiao, G., Peng, H., and Fu, Y. Retrieval head mechanistically explains long-context factuality. _arXiv preprint arXiv:2404.15574_, 2024.


Xiao, G., Tian, Y., Chen, B., Han, S., and Lewis, M. Efficient streaming language models with attention sinks. In
_ICLR_, 2023.


Xiao, G., Tang, J., Zuo, J., Guo, J., Yang, S., Tang, H., Fu,
Y., and Han, S. Duoattention: Efficient long-context llm
inference with retrieval and streaming heads. In _ICLR_,
2024.


Yang, A., Zhang, B., Hui, B., Gao, B., Yu, B., Li, C., Liu,
D., Tu, J., Zhou, J., Lin, J., et al. Qwen2. 5-math technical report: Toward mathematical expert model via selfimprovement. _arXiv preprint arXiv:2409.12122_, 2024a.


Yang, A., Li, A., Yang, B., Zhang, B., Hui, B., Zheng, B.,
Yu, B., Gao, C., Huang, C., Lv, C., et al. Qwen3 technical
report. _arXiv preprint arXiv:2505.09388_, 2025a.


Yang, D., Han, X., Gao, Y., Hu, Y., Zhang, S., and Zhao,
H. Pyramidinfer: Pyramid kv cache compression for
high-throughput llm inference. In _ACL_, 2024b.



10


**Which Heads Matter for Reasoning?** **RL-Guided KV Cache Compression**


Yang, S., Wang, B., Zhang, Y., Shen, Y., and Kim, Y. Parallelizing linear transformers with the delta rule over sequence length. In _NeurIPS_, 2025b.


Yuan, J., Gao, H., Dai, D., Luo, J., Zhao, L., Zhang, Z.,
Xie, Z., Wei, Y., Wang, L., Xiao, Z., Wang, Y., Ruan,
C., Zhang, M., Liang, W., and Zeng, W. Native sparse
attention: Hardware-aligned and natively trainable sparse
attention. In _ACL_, 2025.


Yue, Y., Yuan, Z., Duanmu, H., Zhou, S., Wu, J., and Nie,
L. Wkvquant: Quantizing weight and key/value cache
for large language models gains more. _arXiv_ _preprint_
_arXiv:2402.12065_, 2024.


Zhang, Z., Sheng, Y., Zhou, T., Chen, T., Zheng, L., Cai,
R., Song, Z., Tian, Y., Re, C., Barrett, C., Wang, Z., and´
Chen, B. H2o: Heavy-hitter oracle for efficient generative
inference of large language models. In _NeurIPS_, 2023.


Zheng, L., Yin, L., Xie, Z., Sun, C., Huang, J., Yu, C. H.,
Cao, S., Kozyrakis, C., Stoica, I., Gonzalez, J. E., Barrett, C., and Sheng, Y. Sglang: Efficient execution of
structured language model programs. In _NeurIPS_, 2024.


Zoph, B. and Le, Q. Neural architecture search with reinforcement learning. In _ICLR_, 2017.


Zoph, B., Vasudevan, V., Shlens, J., and Le, Q. V. Learning
transferable architectures for scalable image recognition.
In _CVPR_, 2018.


11


**Which Heads Matter for Reasoning?** **RL-Guided KV Cache Compression**


**A. Motivation Study**


We provide a comprehensive motivation study on three mainstream reasoning models: Llama-3.1-8B-R1 (Guo et al.,
2025), Qwen-2.5-7B-R1 (Guo et al., 2025), and Qwen-3-4B-Thinking [1] (Yang et al., 2025a), and their instruct variants:
Llama-3.1-8B-Inst (Dubey et al., 2024), Qwen-2.5-7B-Inst [2] (Yang et al., 2024a), and Qwen-3-4B-Instruct [3] (Yang et al.,
2025a). We conduct the evaluation on two typical token-dropping methods: H2O (Zhang et al., 2023) and R-KV (Cai et al.,
2025), and one head-reallocation method: DuoAttention (Xiao et al., 2024), across four benchmarks, including GSM8K
(Cobbe et al., 2021), Math500 (Lightman et al., 2023), AIME24 (MMA, 2024), MBPP (Austin et al., 2021). Figure 11
presents that all compression methods maintain relatively stable performance on instruct models but drop substantially on
reasoning models as compression increases.


We further analyze the error modes on reasoning models in the above evaluation. We observed three error modes: repetitive
errors (excessively repeating token sequences), incorrect errors (generating wrong answers), and overlength errors (generating
sequences that exceed normal length baselines), as illustrated in Figure 13. The detailed error modes can be seen in Figure 12.



0.0


0.1


0.2


0.3



0.0

0.1

0.2

0.3

0.4

0.5

0.6



0.0

0.1

0.2

0.3

0.4

0.5

0.6

0.7

0.8



Llama-3.1-8B series



Llama-3.1-8B series



Llama-3.1-8B series



Llama-3.1-8B series



0.9

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

0.0 0.2 0.4 0.6 0.8



0.0

0.1

0.2

0.3

0.4

0.5

0.6

0.7

0.8



0.9

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

0.0 0.2 0.4 0.6 0.8



0.4

|Col1|Col2|Col3|Col4|Col5|Col6|
|---|---|---|---|---|---|
|||||||
|||||||
|||||||
|||||||

0.0 0.2 0.4 0.6 0.8



0.7

|Col1|Col2|Col3|Col4|Col5|Col6|
|---|---|---|---|---|---|
|||||||
|||||||
|||||||
|||||||
|||||||
|||||||

0.0 0.2 0.4 0.6 0.8



Qwen-2.5-7B series



0.0


0.1


0.2


0.3


0.4



0.0

0.1

0.2

0.3

0.4

0.5

0.6





0.0
0.1
0.2
0.3
0.4
0.5
0.6
0.7
0.8
0.9
1.0

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

0.0 0.2 0.4 0.6 0.8



0.0

0.1

0.2

0.3

0.4

0.5

0.6

0.7

0.8



0.9

|Col1|Col2|Col3|Col4|Col5|Col6|
|---|---|---|---|---|---|
|||||||
|||||||
|||||||
|||||||
|||||||
|||||||
|||||||

0.0 0.2 0.4 0.6 0.8



Qwen-2.5-7B series



Qwen-2.5-7B series



Qwen-2.5-7B series



0.5

|Col1|Col2|Col3|Col4|Col5|Col6|
|---|---|---|---|---|---|
|||||||
|||||||
|||||||
|||||||
|||||||

0.0 0.2 0.4 0.6 0.8



0.7

|Col1|Col2|Col3|Col4|Col5|Col6|
|---|---|---|---|---|---|
|||||||
|||||||
|||||||
|||||||
|||||||
|||||||

0.0 0.2 0.4 0.6 0.8



Qwen-3-4B series



0.5

|Col1|Col2|Col3|Col4|Col5|Col6|
|---|---|---|---|---|---|
|||||||
|||||||
|||||||
|||||||
|||||||

0.0 0.2 0.4 0.6 0.8





0.0
0.1
0.2
0.3
0.4
0.5
0.6
0.7
0.8
0.9
1.0

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

0.0 0.2 0.4 0.6 0.8



Qwen-3-4B series

0.0
0.1
0.2
0.3
0.4
0.5
0.6
0.7
0.8
0.9
1.0

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

0.0 0.2 0.4 0.6 0.8



0.0


0.1


0.2


0.3


0.4



Qwen-3-4B series



Qwen-3-4B series



0.0

0.1

0.2

0.3

0.4

0.5

0.6

0.7

0.8



0.9

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

0.0 0.2 0.4 0.6 0.8



KV Cache Budget Sparsity


_Figure_ _11._ Comprehensive evaluation of KV cache compression methods across all model pairs and benchmarks reveals consistent
patterns of performance degradation. H2O, R-KV, and DuoAttention maintain relatively stable performance on instruction-following
models but exhibit significant drops on their reasoning counterparts as the KV cache budget decreases. This performance degradation
becomes particularly severe at higher sparsity levels, with notable declines observed on reasoning-intensive benchmarks including GSM8k,
Math500, AIME24, and MBPP.


1It is the Qwen3-4B-Thinking-2507 instead of Qwen3-4B, which is a hybrid model in reasoning and instruct.
2We use Qwen-2.5-Math-7B-Instruct (Yang et al., 2024a) as the instruct baseline, abbreviated as Qwen-2.5-7B-Inst for naming
consistency, since Qwen-2.5-7B-R1 (deepseek-ai/DeepSeek-R1-Distill-Qwen-7B) was based on Qwen-2.5-Math-7B
3It is the Qwen3-4B-Instruct-2507.


12


**Which Heads Matter for Reasoning?** **RL-Guided KV Cache Compression**


**H2O** **R-KV** **DuoAttention**

Overlength Repetitive Incorrect



Llama-3.1-8B-R1



Llama-3.1-8B-R1



Llama-3.1-8B-R1



GSM8K (Math)



1.0
0.9
0.8
0.7
0.6
0.5
0.4
0.3
0.2
0.1
0.0
0.2 0.4 0.6 0.8



Llama-3.1-8B-R1

Math500 (Math)



1.0
0.9
0.8
0.7
0.6
0.5
0.4
0.3
0.2
0.1
0.0
0.2 0.4 0.6 0.8



1.0
0.9
0.8
0.7
0.6
0.5
0.4
0.3
0.2
0.1
0.0
0.2 0.4 0.6 0.8



AIME24 (Math)



1.0
0.9
0.8
0.7
0.6
0.5
0.4
0.3
0.2
0.1
0.0
0.2 0.4 0.6 0.8



MBPP (Code)



Qwen-2.5-7B-R1



Qwen-2.5-7B-R1



AIME24 (Math)



Qwen-2.5-7B-R1



GSM8K (Math)



1.0
0.9
0.8
0.7
0.6
0.5
0.4
0.3
0.2
0.1
0.0
0.2 0.4 0.6 0.8



1.0
0.9
0.8
0.7
0.6
0.5
0.4
0.3
0.2
0.1
0.0
0.2 0.4 0.6 0.8

Qwen-2.5-7B-R1
Math500 (Math)

1.0
0.9
0.8
0.7
0.6
0.5
0.4
0.3
0.2
0.1
0.0
0.2 0.4 0.6 0.8



Qwen-2.5-7B-R1
Math500 (Math)



1.0
0.9
0.8
0.7
0.6
0.5
0.4
0.3
0.2
0.1
0.0
0.2 0.4 0.6 0.8



MBPP (Code)



Qwen-3-4B-Thinking



Qwen-3-4B-Thinking



Math500 (Math)



Qwen-3-4B-Thinking



AIME24 (Math)



Qwen-3-4B-Thinking





GSM8K (Math)



1.0
0.9
0.8
0.7
0.6
0.5
0.4
0.3
0.2
0.1
0.0
0.2 0.4 0.6 0.8



1.0
0.9
0.8
0.7
0.6
0.5
0.4
0.3
0.2
0.1
0.0
0.2 0.4 0.6 0.8



KV Cache Budget Sparsity



1.0
0.9
0.8
0.7
0.6
0.5
0.4
0.3
0.2
0.1
0.0
0.2 0.4 0.6 0.8



1.0
0.9
0.8
0.7
0.6
0.5
0.4
0.3
0.2
0.1
0.0
0.2 0.4 0.6 0.8



_Figure_ _12._ Comprehensive error mode analyses of KV cache compression methods across reasoning models reveal distinct failure
patterns. Token-dropping methods (H2O, R-KV) consistently exhibit repetitive errors, as they inevitably discard reasoning-critical
information during compression. In contrast, the head-reallocation method DuoAttention tends to show more over-length errors compared
to token-dropping methods, suggesting that while it relatively preserves sequence information integrity, it still struggles to fully preserve
reasoning capability.


**B. Experiment Details**


**Dataset Construction.** We construct training data from the DeepScaleR dataset (Luo et al., 2025), which contains about
40,000 diverse and challenging mathematical reasoning problems. For each model, we generate solutions using the respective
reasoning model with greedy decoding, filter correct solutions, then randomly sample 3,000 problems for training. The
selected problems are distributed across different output token lengths as follows: 600 problems each for 0-2k and 2k-4k
tokens, 1,000 problems for 4k-6k tokens, and 800 problems for 6k-8k tokens.


**Hardware and Hyperparameter Settings.** All trainings are conducted on 2 NVIDIA A100 GPUs (80GB) for several hours,
one for backward computation and one for sample generation. Training runs for 2 epochs, totaling 185 steps with a batch
size of 32. All evaluations are conducted on NVIDIA RTX5090 GPUs. We optimize the gating adapters using AdamW
optimizer with _β_ 1 = 0 _._ 9, _β_ 2 = 0 _._ 999, weight decay of 0.017, and learning rate of 0.01 with constant schedule. For GRPO
training configuration, we disable KL penalty and use recommendation setting of AReaL; for GRPO sampling configuration,
we use 4 samples per query with sampling temperature of 1.0. The hyperparameters are shown in Table Table 3.


**Local Attention Implementation.** During training, we employ an efficient block-sparse attention approximation implementation (Guo et al., 2024) in the FSDP engine of AReaL (Fu et al., 2025) to update adapter weights, while using mask
matrices for prefilling and custom Triton kernels for decoding in SGLang (Zheng et al., 2024) to generate samples. For


13


**Which Heads Matter for Reasoning?** **RL-Guided KV Cache Compression**


_Figure 13._ The instances of three error modes, including repetitive errors (excessively repeating token sequences), incorrect errors (wrong
final answers), and overlength errors (generation exceeding the maximum context length).


_Table 3._ Training Hyperparameters.


Parameter Llama-3.1-8B-R1 Qwen-2.5-7B-R1 Qwen-3-4B-Thinking


Regularization weight _β_ 1e-3 1e-3 2.5e-3
Reward threshold _τ_ 0.5 0.55 0.5
Top ~~P~~ 1.0 1.0 0.95
Sink token size 128 128 128
Local token size 256 256 256
Max sequence length 8192 8192 8192


inference, we only store the full KV cache for reasoning-critical heads, while others only maintain the partial KV cache of
the first 16 sink tokens and the recent 64 local tokens.


**Baseline Implementation.** To ensure fair comparison with baseline methods, we make several adjustments. For H2O and
R-KV, we augment them with the same sink and local token overhead (16+64 tokens) that our method uses. Since H2O and
R-KV only support preset fixed KV cache budgets, we convert their fixed budgets to dynamic allocation that increases with
sequence length. For example, if the fixed budget is 50% of the full KV cache, then at sequence length 1000, they use 500
tokens of KV cache, and at sequence length 2000, they use 1000 tokens of KV cache. For DuoAttention, we replicate their
approach with default settings on our models and use the same inference settings as our method.


**Training Cost.** The training of the adapters is computationally modest: on 2 A100 GPUs, our method consumes 40, 22,
and 36 GPU-hours for Llama-3.1-8B-R1, Qwen-2.5-7B-R1, and Qwen-3-4B-Thinking, respectively.


**Evaluation Settings.** We evaluate all methods using greedy decoding on RTX 5090 36G GPUs or RTX 4090 24G GPUs
with batch size of 1. For all datasets, we use regex to extract the final answer from the generated text, using Pass@1 as the
evaluation metric. For GSM8K, Math500, MBPP and MMLU-Pro subsets, we use 8192 max sequence length; for AIME24,
we use 16384 max sequence length. We achieved near official reported performance without KV cache compression. We
use eager attention implementation for H2O and R-KV since they need to use attention scores, while we use flash attention
for DuoAttention and our method.


**Prompt Template.** We follow the prompt setting recommended by DeepSeek-R1 (Guo et al., 2025) in both training and
evaluation without additional prompt engineering. For example, we use the following template in math problems:


Solve the following math problem efficiently and clearly. The last line

of your response should be of the following format: ’Therefore, the

final answer is: $\\boxed{ANSWER}$. I hope it is correct’ (without

quotes) where ANSWER is just the final number or expression that solves

the problem. Think step by step before answering.


**QUESTION**


14


**Which Heads Matter for Reasoning?** **RL-Guided KV Cache Compression**


**C. Complete numerical results**


Table 4, Table 5 and Table 6 present the complete numerical results of RLKV and baselines for Llama-3.1-8B-R1 and
Qwen-2.5-7B-R1 respectively, across all benchmarks and KV cache compression budgets. Values in parentheses indicate
the performance difference compared to the full KV cache setting, with positive values in green indicating improvement and
negative values in red indicating degradation.


_Table_ _4._ Llama-3.1-8B-R1 performance (%) under different KV cache compression methods and budgets. RLKV ( **Ours** ) shows
competitive performance across settings. Red background denotes performance below the full-KV-cache baseline, whereas green
background denotes performance above it. For all values, higher is better. The best result of the metric in each benchmark is in **bold** .


KV Cache Budget Sparsity
Dataset Method

0.2 0.4 0.6 0.8







**D. Details of Error Modes Analyses**


Figure 14 presents the comprehensive error mode analyses across all models and benchmarks. Our findings in Figure 9 is
consistent with our observations in the main experiments, except for the evaluation of Qwen-3-4B-Thinking on Math500
and MBPP at 0.8 sparsity.


15


**Which Heads Matter for Reasoning?** **RL-Guided KV Cache Compression**



GSM8K

(Math)

1.0
0.9
0.8
0.7
0.6
0.5
0.4
0.3
0.2
0.1
0.0
0.2 0.4 0.6 0.8



0.9
0.8
0.7
0.6
0.5
0.4
0.3
0.2
0.1
0.0
0.2 0.4 0.6 0.8



**DuoAttention (retrieval heads)** **RLKV (reasoning-critical heads)** **Baseline Accuracy (Upper Bound of Error)**
Overlength Repetitive Incorrect



Math500



MBPP
(Code)



MMLU-Pro



MMLU-Pro



MMLU-Pro



(Math)



0.6

0.5

0.4

0.3

0.2

0.1



0.4


0.3


0.2


0.1



0.5

0.4

0.3

0.2

0.1



0.5

0.4

0.3

0.2

0.1



0.0
0.2 0.4 0.6 0.8



AIME24

(Math)



0.6

0.5

0.4

0.3

0.2

0.1



0.0
0.2 0.4 0.6 0.8



(Chem.)



(CS)



(Law)



MMLU-Pro

(Phys.)



0.0
0.2 0.4 0.6 0.8



0.0
0.2 0.4 0.6 0.8



0.0
0.2 0.4 0.6 0.8



0.0
0.2 0.4 0.6 0.8



GSM8K

(Math)

1.0
0.9
0.8
0.7
0.6
0.5
0.4
0.3
0.2
0.1
0.0
0.2 0.4 0.6 0.8



1.0
0.9
0.8
0.7
0.6
0.5
0.4
0.3
0.2
0.1
0.0
0.2 0.4 0.6 0.8



Math500



MBPP
(Code)



0.6

0.5

0.4

0.3

0.2

0.1



MMLU-Pro



(CS)



MMLU-Pro



(Phys.)



(Math)



0.5

0.4

0.3

0.2

0.1



0.0
0.2 0.4 0.6 0.8



AIME24

(Math)



MMLU-Pro

(Chem.)



0.2


0.1



0.0
0.2 0.4 0.6 0.8



MMLU-Pro

(Law)



0.7
0.6
0.5
0.4
0.3
0.2
0.1
0.0
0.2 0.4 0.6 0.8

MBPP
(Code)

0.7
0.6
0.5
0.4
0.3
0.2
0.1
0.0
0.2 0.4 0.6 0.8



0.7
0.6
0.5
0.4
0.3
0.2
0.1
0.0
0.2 0.4 0.6 0.8



0.7
0.6
0.5
0.4
0.3
0.2
0.1
0.0
0.2 0.4 0.6 0.8



GSM8K

(Math)

1.0
0.9
0.8
0.7
0.6
0.5
0.4
0.3
0.2
0.1
0.0
0.2 0.4 0.6 0.8



0.9
0.8
0.7
0.6
0.5
0.4
0.3
0.2
0.1
0.0
0.2 0.4 0.6 0.8



Math500



MBPP
(Code)



MMLU-Pro



0.4


0.3


0.2


0.1



MMLU-Pro



(Phys.)



(Math)



0.5

0.4

0.3

0.2

0.1



0.0
0.2 0.4 0.6 0.8



AIME24

(Math)



0.8
0.7
0.6
0.5
0.4
0.3
0.2
0.1
0.0
0.2 0.4 0.6 0.8



(Chem.)



0.6

0.5

0.4

0.3

0.2

0.1



0.0
0.2 0.4 0.6 0.8



MMLU-Pro

(CS)



MMLU-Pro

(Law)



0.9
0.8
0.7
0.6
0.5
0.4
0.3
0.2
0.1
0.0
0.2 0.4 0.6 0.8



KV Cache Budget Sparsity



0.0
0.2 0.4 0.6 0.8



0.8
0.7
0.6
0.5
0.4
0.3
0.2
0.1
0.0
0.2 0.4 0.6 0.8



_Figure 14._ **Error modes induced by compressing different heads.** We categorize failures into repetitive, incorrect, and overlength
errors, evaluated on instances that are solved correctly by the full KV cache baseline.


**E. An Implicitly Unfair Comparison in Fixed-Budget Evaluation**


This section discusses the motivation for using a dynamic budget instead of a fixed budget for KV cache compression
evaluation. Existing long-context compression works (Li et al., 2024; Yang et al., 2024b; Qin et al., 2024; Fu et al., 2024;
Tang et al., 2024a; Xiao et al., 2024; Bhaskar et al., 2025) typically evaluate on in-context recall tasks, where each sample’s
prompt length is fixed/controlled. A fixed budget of the form budget = sparsity _×_ prompt ~~l~~ ength then yields a roughly
consistent compression ratio per sample, so fixed budgets are fair in that setting.


For reasoning tasks, however, the response length is often much larger than the prompt, as shown in Figure 15. If we use
a global fixed budget (e.g., 1k tokens), any sample whose full output fits within 1k tokens is uncompressed, while longer
samples are compressed. Thus, different samples experience very different compression ratios, and fixed budgets are not fair
at the per-sample level.


In R-KV (Cai et al., 2025), the reported compression rate is computed as budget _/_ average ~~f~~ ull ~~l~~ ength. For example, R-KV
achieves the compression ratio of 66.2% for Math500 on Llama-3.1-8B-R1, with a fixed budget of 200 and an average full
length of 3019. However, a large fraction of samples are uncompressed and thus produce the same responses as the full
model. This makes the reported compression ratio optimistic.


**F. Comparison of Fixed Budget and Dynamic Budget for R-KV and H2O**


In our evaluations, we adopt a dynamic budget strategy where each sample’s budget is determined by its full length
multiplied by the target sparsity, to ensure consistent compression ratios across samples. To illustrate the impact of this
choice, we compare the performance of R-KV and H2O under both fixed and dynamic budget settings on Llama-3.1-8B-R1,
Qwen-2.5-7B-R1, and Qwen-3-4B-Thinking across Math500 and AIME24 at sparsity levels of 0.2, 0.4, 0.6, and 0.8. In
this comparison, the fixed budget per-sample is estimated as budget(sample) = sparsity _×_ full ~~l~~ ength(sample), where
full ~~l~~ ength(sample) is the length of the response generated by the full KV cache model for that specific sample.


As shown in Figure 16, fixed-budget R-KV performs significantly worse than our dynamic-budget variant at 0.2–0.6 sparsity,
and only surpasses at 0.8 sparsity, while H2O maintains similar performance. This shows that our modification does not
weaken the baselines; instead, it corrects an overly optimistic compression estimate and yields a more faithful comparison.


16


**Which Heads Matter for Reasoning?** **RL-Guided KV Cache Compression**


Tokens per Sample Distribution with Full KV Cache



80

70

60

50

40

30

20

10

0


70

60

50

40

30

20

10

0


100


80


60


40


20


0



8


6


4


2


0


8


6


4


2


0


10


8


6


4


2


0



100


80


60


40


20


0


60


50


40


30


20


10


0


60


50


40


30


20


10


0



400

350

300

250

200

150

100

50

0


500


400


300


200


100


0


250


200


150


100


50


0



GSM8K (Math)

|Col1|Col2|Col3|I|Correc<br>ncorre|t (117<br>ct (14|6)<br>3)|Col8|
|---|---|---|---|---|---|---|---|
||||<br> <br>|<br>Correc<br>|<br>t avg<br>|<br> =842<br>||
||||<br>|~~ncorr~~<br>Overal|~~ct av~~<br>l avg|~~ =32~~<br> 1100|~~ 1~~|
|||||||||
|||||||||
|||||||||



GSM8K (Math)

|Col1|Col2|Col3|Col4|Correc|t (117|5)|Col8|
|---|---|---|---|---|---|---|---|
||||<br>I<br> <br>|<br>ncorr<br>Correc<br>|<br>ct (14<br>t avg<br>|<br> 4)<br> =714<br>||
||||<br>~~I~~<br>|<br>~~ncorr~~<br>Overal|<br>~~ct av~~<br>l avg=|<br>~~ g=252~~<br> 911|~~ 6~~|
|||||||||
|||||||||



GSM8K (Math)



Math500 (Math)

|Col1|Col2|Col3|Col4|
|---|---|---|---|
||~~Correct (41~~<br>Incorrect (85<br>|~~ )~~<br> )<br>||
||<br>Correct avg<br>|<br> =2179<br>||
||~~Incorrect av~~<br>Overall avg|~~ =71~~<br> 3019|~~ 9~~|
|||||
|||||
|||||



Math500 (Math)

|Col1|Correct (439|)|Col4|
|---|---|---|---|
||<br>Incorrect (61<br>~~Correct avg~~<br>|<br> )<br>~~ =1699~~<br>||
||<br>Incorrect av<br>~~Overall avg~~|<br> g=571<br>~~ 2188~~|0|
|||||
|||||
|||||



Math500 (Math)



MBPP (Code)

|Col1|Col2|
|---|---|
||~~Correct (313)~~<br>Incorrect (187)<br>Correct avg=3334<br>|
||~~Incorrect avg=3353~~<br>Overall avg=3341|
||<br>|
|||



MBPP (Code)

|Col1|Correct (316)|
|---|---|
||<br>~~Incorrect (184)~~<br>Correct avg=2998<br>|
||<br>~~Incorrect avg=2907~~<br>Overall avg=2964|
|||
|||



MBPP (Code)



AIME24 (Math)

|Col1|Correc<br>Incorre|t (11)<br>ct (19)|
|---|---|---|
||<br>Correc<br>Incorre<br>Overal|<br> avg=5216<br>ct avg=13024<br> avg=10161|
||||
||||



AIME24 (Math)

|Col1|Correc|t (13)|
|---|---|---|
||<br>Incorre<br>Correc<br>Incorre<br>Overal|<br>ct (17)<br>t avg=3728<br>ct avg=12395<br> avg=8639|
||||
||||



AIME24 (Math)


|Col1|Col2|Col3|Col4|Col5|Col6|Col7|Col8|
|---|---|---|---|---|---|---|---|
||||<br>I<br> <br>~~I~~<br>|~~orre~~<br>ncorre<br>Correc<br>~~ncorre~~<br>|~~t (12~~<br>ct (65<br>t avg<br>~~ct av~~<br>|~~ 4)~~<br> )<br> =1139<br>~~ g=315~~<br>|<br>~~ 3~~|
|||||Overal|l avg|1239||
|||||||||


|Col1|Correct (388<br>Incorrect (11|)<br>2)|Col4|
|---|---|---|---|
||<br>Correct avg<br>Incorrect av<br>|<br> =2859<br> g=704<br>|2|
||Overall avg|3796||
|||||


|Col1|Correc<br>Incorre|t (13)<br>ct (17)|
|---|---|---|
||<br>Correc<br>Incorre<br>|<br>t avg=10677<br>ct avg=13248<br>|
||Overal|avg=12134|
||||


|Col1|Col2|
|---|---|
||~~Correct (406)~~<br>Incorrect (94)<br>~~Correct avg=3579~~|
||<br>Incorrect avg=3556<br>|
||<br>Overall avg=3575|
|||



Output Length


_Figure 15._ The distribution of output lengths on Math500 and AIME24 benchmarks with Llama-3.1-8B-R1, Qwen-2.5-7B-R1, and
Qwen-3-4B-Thinking models with full KV cache.


17


**Which Heads Matter for Reasoning?** **RL-Guided KV Cache Compression**


_Table 5._ Qwen-2.5-7B-R1 performance (%) under different KV cache compression methods and budgets. RLKV ( **Ours** ) shows competitive
performance across settings. Red background denotes performance below the full-KV-cache baseline, whereas green background denotes
performance above it. For all values, higher is better. The best result of the metric in each benchmark is in **bold** .


KV Cache Budget Sparsity
Dataset Method

0.2 0.4 0.6 0.8





18


**Which Heads Matter for Reasoning?** **RL-Guided KV Cache Compression**


_Table 6._ Qwen-3-4B-Thinking performance (%) under different KV cache compression methods and budgets. RLKV ( **Ours** ) shows
competitive performance across settings. Red background denotes performance below the full-KV-cache baseline, whereas green
background denotes performance above it. For all values, higher is better. The best result of the metric in each benchmark is in **bold** .


KV Cache Budget Sparsity
Dataset Method

0.2 0.4 0.6 0.8





19


**Which Heads Matter for Reasoning?** **RL-Guided KV Cache Compression**


Full H2O (Dynamic) H2O (Fixed) R-KV (Dynamic) R-KV (Fixed)



Math500 (Math) - R-KV
0.9



0.0
0.0 0.2 0.4 0.6 0.8



0.5


0.4


0.3


0.2


0.1



0.9

0.8

0.7

0.6

0.5

0.4

0.3

0.2

0.1



Math500 (Math) - H2O



AIME24 (Math) - R-KV



0.0
0.0 0.2 0.4 0.6 0.8

Math500 (Math) - H2O

1.0
0.9
0.8
0.7
0.6
0.5
0.4
0.3
0.2
0.1
0.0
0.0 0.2 0.4 0.6 0.8



0.8

0.7

0.6

0.5

0.4

0.3

0.2

0.1



0.0
0.0 0.2 0.4 0.6 0.8

Math500 (Math) - R-KV
1.0
0.9
0.8
0.7
0.6
0.5
0.4
0.3
0.2
0.1
0.0
0.0 0.2 0.4 0.6 0.8



0.0



0.0



Math500 (Math) - H2O



0.5


0.4


0.3


0.2


0.1



AIME24 (Math) - R-KV



Math500 (Math) - R-KV
0.9



0.5


0.4


0.3


0.2


0.1



0.9

0.8

0.7

0.6

0.5

0.4

0.3

0.2

0.1



Math500 (Math) - H2O



AIME24 (Math) - R-KV



0.0
0.0 0.2 0.4 0.6 0.8



AIME24 (Math) - H2O
0.5


0.4


0.3


0.2


0.1


0.0
0.0 0.2 0.4 0.6 0.8

AIME24 (Math) - H2O
0.5


0.4


0.3


0.2


0.1


0.0
0.0 0.2 0.4 0.6 0.8

AIME24 (Math) - H2O
0.5


0.4


0.3


0.2


0.1


0.0
0.0 0.2 0.4 0.6 0.8



0.8

0.7

0.6

0.5

0.4

0.3

0.2

0.1



0.0



KV Cache Budget Sparsity


_Figure 16._ Performance comparison of R-KV and H2O under fixed budget and dynamic budget settings on Llama-3.1-8B-R1, Qwen2.5-7B-R1, and Qwen-3-4B-Thinking across Math500 and AIME24 at sparsity levels of 0.2, 0.4, 0.6, and 0.8. The fixed-budget R-KV
performs significantly worse than the dynamic-budget variant at 0.2, 0.4, and 0.6 sparsity, and only becomes better at 0.8 sparsity, while
H2O maintains similar performance across both settings.


20


