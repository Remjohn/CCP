## **Knocking-Heads Attention**

**Zhanchao Zhou** [1] _[,]_ [2] _[,]_ [3] **, Xiaodong Chen** [1] _[,]_ [4] **, Haoxing Chen** [1] **, Zhenzhong Lan** [1] _[,]_ [3] _[†]_ **,**
**Jianguo Li** [1] _[†]_


1 Ant Group 2 Zhejiang University 3 Westlake University 4 Renmin University of China


**Abstract**


Multi-head attention (MHA) has become the cornerstone of modern large language
models, enhancing representational capacity through parallel attention heads. However, increasing the number of heads inherently weakens individual head capacity,
and existing attention mechanisms — whether standard MHA or its variants like
grouped-query attention (GQA) and grouped-tied attention (GTA) — simply concatenate outputs from isolated heads without strong interaction. To address this
limitation, we propose knocking-heads attention (KHA), which enables attention
heads to “knock" on each other — facilitating cross-head feature-level interactions
before the scaled dot-product attention. This is achieved by applying a shared,
diagonally-initialized projection matrix across all heads. The diagonal initialization
preserves head-specific specialization at the start of training while allowing the
model to progressively learn integrated cross-head representations. KHA adds only
minimal parameters and FLOPs and can be seamlessly integrated into MHA, GQA,
GTA, and other attention variants. We validate KHA by training a 6.1B parameter
MoE model (1.01B activated) on 1T high-quality tokens. Compared to baseline
attention mechanisms, KHA brings superior and more stable training dynamics,
achieving better performance across downstream tasks.


**1** **Introduction**


One of the key factors behind the success of large language models is the design of multi-head
attention (Vaswani et al., 2017), which has been preserved across various subsequent attention

















2.6


2.4


2.2


2.0



1.8


1.6

|Col1|Col2|
|---|---|
|Baselin<br>Knocki|e<br>ng-Heads Attention|
|||
|||
|||
|||
|||



0.0B 200.0B 400.0B 600.0B 800.0B 1000.0B
Tokens (Billion)











Figure 1: (Left) The knocking-heads attention architecture. Purple represents the original multi-head
attention, while pink represents the added knocking-heads projections. _T_ _[Q]_ and _T_ _[K]_ within the dashed
box are optional projections due to their lower importance compared to _T_ _[V]_ . (Right) Training loss
over 1T tokens for 6.1B MoE models (1.01B activated parameters): baseline _vs._ knocking-heads
attention. KHA reduces loss spikes and maintains consistently lower training loss.


variants (Shazeer et al., 2020; Ainslie et al., 2023; Liu et al., 2024; Zadouri et al., 2025). Multi-head
attention (MHA) enables models to simultaneously process information from multiple representation
subspaces across different sequence positions, with each attention head serving distinct functions in
sequence modeling (Xiao et al., 2023, 2024; Qin et al., 2025).


However, different heads operate independently when modeling attention, with each head computing its output separately before concatenation and forward propagation, lacking mutual interaction.
Talking-heads attention (Shazeer et al., 2020) addresses this limitation by introducing linear projections on either logits before the attention softmax operation or attention scores after the softmax operation to enable inter-head communication. Nevertheless, talking-heads projections on
quadratically-scaling attention matrices lead to dramatically increased computational complexity,
especially when the number of heads is large.


In this paper, we propose knocking-heads attention (KHA) (Fig. 1 (Left)), a variant of multi-head
attention that achieves inter-head interaction at the feature level through unified transformations
applied to all heads. Compared to standard multi-head attention, KHA introduces additional shared
projections for query, key, and value representations, supplementing the original head-specific
projections. Among these, the knocking-heads projections for queries and keys are optional since they
provide smaller improvements compared to the value projections. We initialize these knocking-heads
projections with diagonal matrices, allowing the model to start from isolated heads and gradually
develop inter-head communication during training, eventually reaching an optimal balance between
head specialization and cross-head collaboration. This additional head-sharing mechanism not
only facilitates information sharing and coordination between different heads while preserving their
individual specializations, but also serves as an implicit regularization constraint applied to all heads.
Knocking-heads projections introduce minimal overhead ( _<_ 1% additional FLOPs and parameters)
during training and, when implemented as linear transformations rather than MLPs, can be fully
integrated into the original projections at inference time.


We conduct extensive experiments on language modeling. We first perform architectural exploration
to identify the optimal configuration for knocking-heads projections, examining different projection
types (linear, MLP-based, gated), target components (queries, keys, values), attention variants (MHA,
MQA, GQA, GTA), and head configurations. Our analysis reveals that applying MLP-based knockingheads projections to values yields the most significant improvements, with the benefits becoming
evident at 4 value/key heads. Based on these findings, we adopt GQA with 32 query heads and 4 KV
groups, enabling knocking-heads projections to achieve high performance while maintaining efficient
KV caching. We validate our approach through comprehensive experiments on 1T tokens using
1.01B-active-parameter, 6.1B-total-parameter MoE models, with results shown in Fig. 1 (Right). Our
method achieves significant improvements in Language Understanding (+4.32), Code (+3.9), and
Math (+1.62) tasks, with an overall average score improvement of 1.26 points across all evaluated
tasks. Additional experiments across various MoE and dense model scales further demonstrate the
effectiveness of our method. We summarize our main contributions as follows:


    - We introduce knocking-heads attention, a novel head interaction mechanism that enables
cross-head communication through shared transformation matrices with minimal computational overhead. To preserve head specialization, we propose diagonal initialization that
allows heads to maintain their distinct roles while gradually developing beneficial cross-head
interactions.

    - We conduct extensive experiments validating KHA’s universality across different attention mechanisms, model types (MoE and dense), and model scales, demonstrating broad
applicability and identifying optimal configurations.

    - We demonstrate scalability through large-scale experiments on 1T tokens using 1.01B-activeparameter, 6.1B-total-parameter models, achieving consistent improvements in training
stability and model performance.


**2** **Related Work**


**2.1** **Parameter Sharing in Architecture Design**


Parameter sharing is a fundamental design principle in deep learning architectures. In CNNs (LeCun
et al., 2002), shared convolutional kernels enable translation equivariance and improve generalization


2


capability. ALBERT (Lan et al., 2020) achieves significant parameter reduction through cross-layer
parameter sharing. DeepSeek-MoE (Dai et al., 2024) introduces shared experts to reduce parameter
redundancy across routed experts. In this work, we introduce additional shared projection matrices
( _i.e._, knocking-heads projections) across different attention heads on top of the original head-specific
projections to facilitate inter-head interaction and provide regularization effects.


**2.2** **Attention Head Interaction**


Multi-head attention mechanisms allow different attention heads to learn diverse patterns (Xiao et al.,
2023, 2024), but these heads lack interconnection and often exhibit significant redundancy (Cordonnier et al., 2020; Jin et al., 2024). Several approaches have explored inter-head communication
to address this issue. Talking-heads attention (Shazeer et al., 2020) applies learnable transformations to attention weight matrices, but requires materializing these matrices, making it incompatible
with FlashAttention (Dao et al., 2022), not to mention its substantial computational overhead when
head counts are large relative to head dimensions. Collaborated multi-head attention (Cordonnier
et al., 2020) shares projection matrices across heads with head-wise dimension-specific mixers, yet
increases training FLOPs while limiting head specialization to feature reweighting. Mixture-of-head
attention (Jin et al., 2024) dynamically selects head subsets per token but provides limited inter-head
communication while incurring complex router training. Our proposed knocking-heads attention
adopts head-sharing projections similar to collaborated attention but preserves head specialization
through keeping original head-specific projections and diagonal initialization. The plug-and-play
mechanism is compatible with any attention variants and FlashAttention framework, adding minimal
FLOPs and parameters. More detailed comparisons are provided in Table 6 in the appendix.


**2.3** **Loss Spikes in Pre-training**


Loss spikes are a common challenge in large-scale pretraining. Recent work has identified various
underlying causes and solutions beyond simply skipping problematic data batches (Chowdhery et al.,
2023). Takase et al. (2023) found correlations between loss spikes and gradient spikes in specific
parameters on 1.7B parameter models, proposing scaled initialization for embedding layers. Qiu et al.
(2025) reduced loss spikes by introducing gating mechanisms to avoid massive activations. Kimi-K2
(Team et al., 2025) identified attention logit spikes in certain heads as the primary cause and proposed
QK-clip for mitigation. Our knocking-heads structure addresses this issue differently—by sharing
transformation matrices across attention heads, it introduces regularization effects that effectively
mitigate loss spikes.


**3** **Method**


**3.1** **Classical Attention**


Multi-head attention (MHA) enables the model to jointly attend to information from different
representation subspaces. Given an input sequence **X** _∈_ R _[L][×][d]_ where _L_ is the sequence length and
_d_ is the hidden dimension, MHA employs _n_ parallel attention heads to capture diverse attention
patterns.


For each attention head _i ∈{_ 1 _,_ 2 _, . . ., n}_, the queries, keys, and values are computed as:

**Q** _i_ = **XW** _i_ _[Q][,]_ **W** _i_ _[Q]_ _[∈]_ [R] _[d][×][d][k]_ _[,]_ (1)

**K** _i_ = **XW** _i_ _[K][,]_ **W** _i_ _[K]_ _[∈]_ [R] _[d][×][d][k]_ _[,]_ (2)

**V** _i_ = **XW** _i_ _[V]_ _[,]_ **W** _i_ _[V]_ _[∈]_ [R] _[d][×][d][v]_ _[,]_ (3)


where _dk_ = _dv_ = _d/n_ represents the dimension of each head. The attention output for head _i_
is computed as **O** _i_ = Attention( **Q** _i,_ **K** _i,_ **V** _i_ ) = Softmax - **Q** ~~_√_~~ _i_ **K** _dk_ _[T]_ _i_ - **V** _i_, following the scaled dot
product attention mechanism. The final MHA output concatenates all head outputs and applies a
linear projection:
MHA( **X** ) = Concat( **O** 1 _,_ **O** 2 _, . . .,_ **O** _n_ ) **W** _[O]_ _,_ (4)

where **W** _[O]_ _∈_ R _[d][×][d]_ is the output projection matrix. Group Query Attention (GQA) extends this
framework by partitioning _n_ query heads into _g_ groups, where each group shares the same key

3


value pair. This design reduces computational overhead while maintaining representational capacity,
effectively interpolating between MHA ( _g_ = _n_ ) and multi-query qttention ( _g_ = 1) (Shazeer, 2019).


**3.2** **Knocking-Heads Attention**


In multi-head attention, each head operates with reduced dimensions, creating a low-rank bottleneck
that limits individual head expressiveness (Bhojanapalli et al., 2020). Inspired by talking-heads
attention (Shazeer et al., 2020) and head-sharing projections in collaborated attention (Cordonnier
et al., 2020), we propose knocking-heads attention (KHA). After **W** _[Q]_, **W** _[K]_, **W** _[V]_ projections but
before individual scaled dot-product attention computations, KHA introduces head-sharing projection
matrices ( _i.e._ knocking-heads projections) alongside the original head-specific projections that enable
head interaction while keeping head specification.


We explore two variants of knocking-heads projections that offer complementary advantages: linear
transformations provide inference efficiency through matrix absorption, while MLP transformations
offer enhanced expressiveness through non-linearity.


**KHA-Linear** KHA-Linear applies shared linear transformations to enhance head coordination. For
each head _i_, the transformed queries, keys, and values are computed as:
**Q** ˜ _i_ = **Q** _i_ **T** _[Q]_ _,_ **T** _[Q]_ _∈_ R _[d][k][×][d][k]_ _,_ (5)
**K** ˜ _i_ = **K** _i_ **T** _[K]_ _,_ **T** _[K]_ _∈_ R _[d][k][×][d][k]_ _,_ (6)
**V** ˜ _i_ = **V** _i_ **T** _[V]_ _,_ **T** _[V]_ _∈_ R _[d][v][×][d][v]_ _,_ (7)


where **T** _[Q]_, **T** _[K]_, and **T** _[V]_ are shared transformation matrices across all heads. Crucially, during
inference, these transformations can be absorbed into the original projection matrices:


_[′]_

**W** _i_ _[Q][′]_ = **W** _i_ _[Q]_ **[T]** _[Q][,]_ **W** _i_ _[K][′]_ = **W** _i_ _[K]_ **[T]** _[K][,]_ **W** _i_ _[V]_ = **W** _i_ _[V]_ **[T]** _[V][,]_ (8)

eliminating computational overhead while preserving the benefits of enhanced head coordination.


**Key Takeway** As we will demonstrate in Section 4.2.3, **T** _[V]_ is the most critical component, as values
learn head interactions most effectively. The transformations **T** _[Q]_ and **T** _[K]_ are optional, as their
removal causes negligible performance degradation.


**KHA-MLP** To leverage non-linear expressiveness, we introduce an MLP-based transformation that
our experiments show outperforms pure linear approaches. Given the parameter overhead of applying
MLP to all queries, keys, and values, we focus solely on the most critical values, which maintains the
same parameter count as the linear variant while providing superior representational capacity:
**V** ˜ _i_ = MLP( **V** _i_ ) = 2 _·_     - **V** _i_ **W** [up] _⊙_ Sigmoid( **V** _i_ **W** [gate] )� **W** [down] _,_ (9)


where **W** [up] _,_ **W** [gate] _,_ **W** [down] _∈_ R _[d][v][×][d][v]_ are shared across all heads. We use sigmoid-activated MLPs
to facilitate zero initialization. Our ablation studies confirm that applying gating alone introduces
detrimental effects, while the complete MLP structure enhances model expressiveness.


**3.3** **Initialization Strategy**


The effectiveness of KHA relies critically on “zero" initialization of shared matrices to ensure they
approximate identity mappings during early training. Our experiments show that random initialization
causes loss to converge to much higher values, potentially making all heads overly similar.


For the KHA-Linear, we apply diagonal initialization to **T** _[Q]_, **T** _[K]_, and **T** _[V]_ . For the KHAMLP, **W** [up] and **W** [down] are diagonal-initialized, while **W** [gate] is zero-initialized. This ensures that
sigmoid( **V** _i_ **W** [gate] ) _·_ 2 = 1 initially, which motivates our choice of sigmoid activation in Equation 9.


This initialization allows off-diagonal elements to progressively learn non-zero values, enabling the
model to first establish head specialization before learning inter-head interactions.


**3.4** **Complexity Analysis**


The training FLOPs for multi-head attention can be computed as:

FLOPMHA = 6 _Ld_ [2] + 4 _nL_ [2] _dk_ + 2 _Ld_ [2] = 8 _Ld_ [2] + 4 _L_ [2] _d,_ (10)


4


where 6 _Ld_ [2] accounts for query, key, and value projection forward and backward passes, 4 _nL_ [2] _dk_
represents attention score computation and attention-value multiplication, and 2 _Ld_ [2] corresponds
to the output projection matrix **W** _[O]_ . Assuming _d_ ff = 3 _d_, the training FLOPs for the feed-forward
network (FFN) with up-gate-down structure can be computed as: FLOPFFN = 6 _Ld ·_ 3 _d_ = 18 _Ld_ [2],
where the factor of 6 accounts for forward and backward passes through three linear layers (up, gate,
and down projection). Therefore, the total single-layer training FLOPs is:

FLOPtotal = FLOPMHA + FLOPFFN = 26 _Ld_ [2] + 4 _L_ [2] _d._ (11)


For both knocking-heads variants, the additional training FLOPs are identical:

FLOPKHA = [6] _[Ld]_ [2] _._ (12)

_n_

where _n_ is the number of attention heads. For a concrete example with _L_ = 2048, _d_ = 1024 and
_n_ = 32, the knocking-heads overhead represents only 0.55% of the total layer computation and
1.17% of the original MHA computation, demonstrating the efficiency of our approach.


**4** **Experiment**


**4.1** **Training Setup**


We conduct two sets of experiments: main experiments on 1T tokens and exploratory experiments on
100B tokens, both using high-quality multi-domain data.


**Architecture** We adopt MoE architectures for most of our experiments, as they consistently
outperform dense models under equivalent training FLOPs (Dai et al., 2024). To maintain expert load
balancing, we implement an updated loss-free balancing strategy (Wang et al., 2024a; Su, 2025). We
follow Qwen’s design (Yang et al., 2025) for attention implementation with QK RMS normalization,
and maintain a head dimension of 128 throughout all experiments. For the main experiments, we use
a configuration with 128 experts where 8 are activated, yielding 6.1B total parameters with 1.01B
active parameters. We employ 32 attention heads with grouped query attention (group size _g_ = 4) For
exploratory experiments, we scale down to 64 experts with 4 activated and vary the hidden dimension
to create model variants ranging from A0.44B-2.3B up to A1.6B-14.6B. These experiments evaluate
different attention mechanisms including MHA, MQA, GTA, MLA, and GLA, as well as various
GQA configurations.


**Hyperparameters** All models are trained using Adam optimizer with weight decay 0.1, _β_ 1 = 0 _._ 9,
_β_ 2 = 0 _._ 95, and gradient clipping at 1.0. We use FSDP for distributed training. The learning rate
schedule includes 5% warmup steps followed by cosine annealing to 10% of peak rate at training
completion. For main experiments, we use learning rate 4.78e-4, sequence length 8,192, and batch
size 4.2M tokens. Exploratory experiments use learning rate 7.5e-4, sequence length 4,096, and batch
size 2.1M tokens.


**4.2** **Architecture Exploration On Attention**


We conduct exploratory experiments to evaluate KHA from the following perspectives. First, we
examine the impact of different numbers of heads on KHA performance (Section 4.2.1). Second,
we explore different positions and methods for applying knocking-heads projections (Section 4.2.2).
Third, we test the compatibility of KHA with other attention variants (Section 4.2.3).


**4.2.1** **KHA with Varying Head Number**


KHA’s core mechanism relies on head-sharing, making it sensitive to the number of attention heads.
We evaluate both KHA variants on GQA with varying KV head groups while fixing query heads.
All experiments were performed using a 0.8B activated parameter model (6.6B total parameters)
trained on 75B tokens. As shown in Table 1, the effectiveness of KHA scales with KV head count.
Both variants show significant improvements as KV heads increase from 1 to 4, confirming that
more heads provide greater opportunities for cross-head information sharing. KHA-MLP show
more stable performance across different configurations than the linear-based ones, likely due to the
diagonal-initialized MLP introducing beneficial non-linearity beyond head-sharing alone.


5


Table 1: Loss of knocking-heads variants with different KV heads number in GQA (32 query heads).
All models reported are A0.8-6.6B MoE trained on 75B tokens. ∆ _L_ denotes the loss difference after
adopting KHA, where lower values indicate better performance.


# KV heads
Model

1 2 4 8 16 32


Baseline 1.864 1.855 1.856 1.851 1.849 1.846

KHA-MLP 1.846 1.835 1.832 1.832 1.833 1.83

∆ _L_ **-0.017** **-0.020** **-0.024** **-0.019** **-0.016** **-0.016**

KHA-Linear 1.857 1.845 1.838 1.841 1.832 1.834


Table 2: Loss comparison of knocking-heads variants across different shared projection types (linear,
gate, MLP) and positions (query, key, value). All models reported are A0.8-6.6B MoE with GQA
( _g_ = 4) trained on 75B tokens. Green indicates the **best** setting and red indicates the **worst** setting.










|Type Place Loss ∆L|Type Place Loss ∆L|
|---|---|
|Q<br>K<br>V|Q<br>K<br>V|
|-<br>-<br>-<br>-<br>1.856<br>**–**|Gate<br>-<br>-<br>✓<br>1.919<br>**+0.063**|
|Linear<br>✓<br>-<br>-<br>1.849<br>**-0.007**<br>-<br>✓<br>-<br>1.848<br>**-0.008**<br>-<br>-<br>✓<br>1.839<br>**-0.017**<br>✓<br>✓<br>✓<br>1.838<br>**-0.018**|MLP<br>✓<br>-<br>-<br>1.848<br>**-0.008**<br>-<br>✓<br>-<br>1.848<br>**-0.008**<br>-<br>-<br>✓<br>1.832<br>**-0.024**<br>✓<br>✓<br>✓<br>1.832<br>**-0.024**|



**4.2.2** **Ablation Studies on Different Variants of Knocking-heads**


We experiment with knocking-heads variants beyond the KHA-Linear and KHA-MLP presented
in Section 3.2, exploring different architectural choices for inter-head knowledge sharing. The
training setup is similar as Section 4.2.1 and we fix the group size _g_ = 4 in GQA based on the
results in Table 1. Our investigation focused on two key design dimensions: (1) the type of shared
transformation matrices (linear layers, gating mechanisms, or MLPs) and (2) their placement within
the attention mechanism (query, key, or value projections).


Table 2 reveals several interesting findings. First, incorporating shared transformations across
attention heads consistently improves performance, with benefits observed across all three projection
positions (Query, Key, Value) and for both linear and MLP-based transformations. Interestingly,
value projections benefit most from the knocking-heads mechanism, suggesting that sharing learned
representations in the value space is particularly effective for capturing cross-head dependencies.
When comparing transformation types, MLPs demonstrate better performance over linear layers
for value projections. This advantage likely stems from non-linear activations in MLPs, but using
standalone gating mechanisms as shared transformations proves detrimental to model performance.


**4.2.3** **Compatibility with Other Attention Variants**


KHA can actually adapt to any form of multi-head attention mechanism, but we focus specifically on
softmax-based attention here. Except for MLA, which only works with KHA-Linear because they
don’t explicitly materialize queries/keys/values during inference, other variants are compatible with
both KHA-Linear and KHA-MLP. Therefore, for MLA, we use KHA-Linear, while for others, based
on the results in Table 2, we use KHA-MLP. All experiments were performed using a model with
approximately 0.8B activated parameters (around 6.6B total parameters) trained on 100B tokens.


As shown in Table 3, KHA consistently improves all tested variants including GQA, MHA, GTA,
and MQA. The results demonstrate the ability of knocking-heads projections to recover performance
losses incurred by KV-cache optimizations, allowing models to maintain memory efficiency without
sacrificing quality. For example, baseline GQA4(32) underperforms MHA16(16) by 0.012 loss
despite using 4 _×_ less KV-cache. When both apply knocking-heads projections, GQA4(32) achieves


6


Table 3: Loss of knocking-heads on various attention variants with different head configurations. All
models reported are roughly A0.8-6.6B MoE trained on 100B tokens. ∆ _L_ denotes the loss difference
after adopting KHA, where lower values indicate better performance. KHA-MLP is used for all

|nts except MLA, which uses KHA-Linear.|Col2|
|---|---|
|Model<br>Head<br># KV<br># Query<br>Cache<br>Activated<br>Dim.<br>Head<br>Head<br>Params|Baseline<br>Knocking-<br>∆_L_<br>Heads|
|MLA<br>128<br>4<br>8<br>512+64<br>970M<br>GTA<br>128<br>4<br>32<br>512+64<br>868M<br>MQA<br>128<br>1<br>32<br>256<br>859M<br>GQA<br>128<br>8<br>16<br>2048<br>795M<br>GQA<br>128<br>4<br>32<br>1024<br>880M<br>MHA<br>128<br>16<br>16<br>4096<br>852M|1.812<br>1.801<br>**-0.011**<br>1.819<br>1.802<br>**-0.017**<br>1.814<br>1.801<br>**-0.013**<br>1.801<br>1.791<br>**-0.010**<br>1.807<br>1.787<br>**-0.020**<br>1.795<br>1.785<br>**-0.010**|



a 0.02 loss reduction, shrinking the gap between GQA4(32) and MHA16(16) to just 0.002. Notably,
knocking-heads projections even benefits GTA, which shares non-RoPE features between keys and
values, highlighting knocking-heads projection’s broad generalizability.


Table 4: Performance comparison with and without KHA (32 query heads, 4 key/value heads), trained
on 1T tokens with 1.01B active and 6.1B total parameters. “Overall Average" is the average score of
all sub-tasks. Green values indicate **improvements**, while red indicate **decreases** .


Metric Baseline Knocking-Heads ∆ Score







Overall Average 49.13 50.39 +1.26


**4.3** **Large-scale Pretraining On 1T Tokens**


To validate KHA’s effectiveness in large-scale pre-training scenarios, we conducted controlled
experiments on a 6.1B-parameter MoE model with 1.01B activated parameters, training on 1T tokens.
Based on results in Section 4.2, we chose a baseline configuration with GQA ( _g_ = 4) and 32 query
heads to evaluate adding KHA-MLP’s impact. As shown in Fig. 1(right), the baseline model exhibited


7


numerous training spikes during the first half of training, whereas applying KHA significantly reduced
spike frequency. Furthermore, once loss stabilized in the latter half of training, the model with KHA
consistently achieved **0.015** lower loss at equivalent training steps.


We comprehensively evaluated the final trained models on the downstream tasks mentioned in
Appendix A.2. The results in Table 4 demonstrate that while performance on general knowledge
and professional knowledge tasks remained comparable between models with and without KHA,
significant improvements were observed in language understanding, code, and math tasks, with
average score increases of **4.32**, **3.9**, and **1.62** points, respectively. The overall average improvement
across all tasks was **1.26** points. In summary, KHA has proven effective in large-scale training, not
only substantially reducing training loss spikes but also delivering superior model performance.


Table 5: Performance of KHA on different architectures with varying model sizes. All models are
trained on 100B tokens and adopt 4 key/value heads. The best results in each row are shown in **bold** .

|Activated Total Hidden FFN<br>Type Layers<br>Params Params Size Size|KHA- KHA-<br>GQA<br>MLP Linear|
|---|---|
|MoE<br>0.44B<br>2.3B<br>12<br>1152<br>768×4<br>0.8B<br>6.6B<br>18<br>1536<br>1152×4<br>1.6B<br>14.6B<br>23<br>2048<br>1536×4|1.896<br>**1.881**_−_0_._015<br>1.882_−_0_._014<br>1.807<br>**1.787**_−_0_._020<br>1.791_−_0_._016<br>1.762<br>**1.737**_−_0_._025<br>1.742_−_0_._020|
|Dense<br>0.61B<br>0.61B<br>24<br>1024<br>3072<br>1.68B<br>1.68B<br>24<br>2048<br>6144<br>3.94B<br>3.94B<br>36<br>2560<br>9728|2.017<br>2.013_−_0_._004<br>**2.007**_−_0_._014<br>1.892<br>1.884_−_0_._008<br>**1.872**_−_0_._020<br>1.815<br>1.811_−_0_._004<br>**1.807**_−_0_._008|



**4.4** **Scalability Compared with Transformer**


As shown in Table 5, we evaluate KHA across different model architectures and scales, training MoE
models (2.3B-14.6B parameters) and dense models (0.61B-3.94B parameters) on 100B tokens. All
models employ GQA with 4 KV heads, 32 query heads, and 128 head dimensions. Knocking-heads
delivers substantial improvements for MoE architectures: while scaling baseline MoE from 6.6B
to 14.6B parameters reduces loss by 0.045, knocking-heads attention achieves a loss reduction of
0.02 with negligible training overhead. The benefits become more pronounced at larger MoE scales.
Additionally, we find that KHA-Linear provides greater improvements on dense models.


**4.5** **Visualization**


**4.5.1** **Training Stablity**


We present the loss curves for selected experiments from Section 4.3 and Section 4.4 in Fig.1 and
Fig.2, respectively. Loss spikes occur more frequently during the first half of training, with the 1.6B
activated MoE model exhibiting significantly higher spike frequency than the 0.4B activated mode.
Across all model scales, KHA effectively mitigates loss spikes and improves training stability. For the
0.8B activated MoE model, we compare loss curves of both KHA-Linear and KHA-MLP against the
baseline. Both variants successfully reduce loss spikes, confirming that the head-sharing mechanism
itself suppresses training instability. We hypothesize this stems from the head-sharing mechanism
acting as implicit regularization.


**4.5.2** **Learnt Weight of Shared Matrix**


We visualize the learned knocking-heads projection parameters in Fig. 3. _T_ _[Q]_ and _T_ _[K]_, both applied
before QK normalization, show similar block-structured patterns: some feature dimensions exhibit
low diagonal values indicating inter-head interaction learning, while others retain high diagonal values
for head-specific information. Some layers even exhibit minimal inter-head interaction, highlighting
the adaptive nature of our method. Notably, _T_ _[V]_ displays a distinct pattern with consistently low
diagonal values across layers, indicating aggressive head-sharing. This may explain why value
projections yield greater improvements in Table. 2. When using MLPs, the gate matrices also exhibit
clear structural patterns.


8


2.8


2.6


2.4


2.2


2.0


1.8



2.8


2.6


2.4


2.2


2.0


1.8



2.8


2.6


2.4


2.2


2.0


1.8









2.8


2.6


2.4


2.2


2.0





(a) A0.44b-2.3B



(b) A1.6b-14.6B



0.0B 20.0B 40.0BTokens (Billion)60.0B 80.0B 100.0B


(c) A0.8b-6.6B(MLP)



0.0B 20.0B 40.0BTokens (Billion)60.0B 80.0B 100.0B


(d) A0.8b-6.6B(Linear)



Figure 2: Training loss curves before and after applying knocking-heads across different model sizes,
and the loss curves in (c) and (d) are smoothed for better visualization.



10010210410610811011211411611812012212412610121416182022242628303234363840424446485052545658606264666870727476788082848688909294969802468



T [Q], Layer 3


T [V], Layer 3


Head Dim



1001010410610811011211411611812012212412101214161820222262830323436384042444648552545658606264666870727477880828486889092949698024684 ~~062~~ 6



T [Q], Layer 12


Value Up, Layer 3


Head Dim



10010104106108110112114116118120122124121012141618202222283032343638404244464855545658606264666870727477880828486889092949698 ~~0~~ 24684 ~~6~~ 02 ~~62~~ 6



T [K], Layer 3


Value Down, Layer 3


Head Dim



1001010410610811011211411611812012212412101214161820222262830323436384042444648552545658606264666870727477880828486889092949698024684 ~~062~~ 6


1.0


0.8


0.6


0.4


0.2


0.0



10010210410610811011211411611812012212412610121416182022242628303234363840424446485052545658606264666870727476788082848688909294969802468



101010410610811011211411611812012212412101214161820222262830323436384042444648552545658606264666870727477880828486889092949698024684 ~~06~~ 0 ~~2~~ 6



101010410610811011211411611812012212412101214161820222628303234363840424446455254565860626466687072777880828486889092949698024682 ~~4~~ 8 ~~0~~ 4 ~~6~~ 0 ~~2~~ 6



10010210410610811011211411611812012212412610121416182022242628303234363840424446485052545658606264666870727476788082848688909294969802468



T [K], Layer 12


Value Gate, Layer 3


Head Dim



1.0


0.8


0.6


0.4


0.2


0.0


0.10


0.05


0.00


0.0


0.1



Figure 3: Visualization of learned knocking-heads projection weights across different layers and
types. We apply 0-1 clipping to all knocking-heads projection weights except _W_ _[gate]_, including _T_ _[K]_,
_T_ _[Q]_, _T_ _[V]_, _W_ _[up]_, and _W_ _[down]_, for comparative analysis.


**5** **Conclusion**


In this work, we introduced knocking-heads attention, a simple enhancement to MHA that enables
cross-head communication through shared, diagonally-initialized transformation matrices. Our
method addresses the limitation that attention heads operate in isolation while adding less than 1%
computational overhead. Through experiments on 1T tokens using 6.1B parameter MoE models,
we demonstrate that Knocking-Heads Attention achieves superior performance and significantly
improves training stability compared to standard MHA. The diagonal initialization proves crucial for
balancing head specialization with cross-head collaboration. As a drop-in replacement for standard
MHA, our approach offers a practical enhancement for transformer architectures.


9


**References**


Joshua Ainslie, James Lee-Thorp, Michiel De Jong, Yury Zemlyanskiy, Federico Lebrón, and Sumit
Sanghai. Gqa: Training generalized multi-query transformer models from multi-head checkpoints.
_arXiv preprint arXiv:2305.13245_, 2023.


Sumithra Bhakthavatsalam, Daniel Khashabi, Tushar Khot, Bhavana Dalvi Mishra, Kyle Richardson,
Ashish Sabharwal, Carissa Schoenick, Oyvind Tafjord, and Peter Clark. Think you have solved
direct-answer question answering? try arc-da, the direct-answer AI2 reasoning challenge. _CoRR_,
abs/2102.03315, 2021. URL `[https://arxiv.org/abs/2102.03315](https://arxiv.org/abs/2102.03315)` .


Srinadh Bhojanapalli, Chulhee Yun, Ankit Singh Rawat, Sashank Reddi, and Sanjiv Kumar. Low-rank
bottleneck in multi-head attention models. In _International conference on machine learning_, pp.
864–873. PMLR, 2020.


Yonatan Bisk, Rowan Zellers, Ronan Le Bras, Jianfeng Gao, and Yejin Choi. PIQA: reasoning about
physical commonsense in natural language. In _The Thirty-Fourth AAAI Conference on Artificial_
_Intelligence, AAAI 2020, The Thirty-Second Innovative Applications of Artificial Intelligence Con-_
_ference, IAAI 2020, The Tenth AAAI Symposium on Educational Advances in Artificial Intelligence,_
_EAAI 2020, New York, NY, USA, February 7-12, 2020_, pp. 7432–7439. AAAI Press, 2020. doi:
10.1609/AAAI.V34I05.6239. URL `[https://doi.org/10.1609/aaai.v34i05.6239](https://doi.org/10.1609/aaai.v34i05.6239)` .


Aakanksha Chowdhery, Sharan Narang, Jacob Devlin, Maarten Bosma, Gaurav Mishra, Adam
Roberts, Paul Barham, Hyung Won Chung, Charles Sutton, Sebastian Gehrmann, et al. Palm:
Scaling language modeling with pathways. _Journal of Machine Learning Research_, 24(240):1–113,
2023.


Karl Cobbe, Vineet Kosaraju, Mohammad Bavarian, Mark Chen, Heewoo Jun, Lukasz Kaiser,
Matthias Plappert, Jerry Tworek, Jacob Hilton, Reiichiro Nakano, Christopher Hesse, and John
Schulman. Training verifiers to solve math word problems. _CoRR_, abs/2110.14168, 2021. URL
`[https://arxiv.org/abs/2110.14168](https://arxiv.org/abs/2110.14168)` .


Jean-Baptiste Cordonnier, Andreas Loukas, and Martin Jaggi. Multi-head attention: Collaborate
instead of concatenate. _arXiv preprint arXiv:2006.16362_, 2020.


Damai Dai, Chengqi Deng, Chenggang Zhao, RX Xu, Huazuo Gao, Deli Chen, Jiashi Li, Wangding
Zeng, Xingkai Yu, Yu Wu, et al. Deepseekmoe: Towards ultimate expert specialization in mixtureof-experts language models. _arXiv preprint arXiv:2401.06066_, 2024.


Tri Dao, Dan Fu, Stefano Ermon, Atri Rudra, and Christopher Ré. Flashattention: Fast and memoryefficient exact attention with io-awareness. _Advances in neural information processing systems_, 35:
16344–16359, 2022.


Dan Hendrycks, Collin Burns, Steven Basart, Andy Zou, Mantas Mazeika, Dawn Song, and Jacob
Steinhardt. Measuring massive multitask language understanding. In _9th International Conference_
_on Learning Representations, ICLR 2021, Virtual Event, Austria, May 3-7, 2021_ . OpenReview.net,
2021a. URL `[https://openreview.net/forum?id=d7KBjmI3GmQ](https://openreview.net/forum?id=d7KBjmI3GmQ)` .


Dan Hendrycks, Collin Burns, Saurav Kadavath, Akul Arora, Steven Basart, Eric Tang, Dawn Song,
and Jacob Steinhardt. Measuring mathematical problem solving with the MATH dataset. In Joaquin
Vanschoren and Sai-Kit Yeung (eds.), _Proceedings of the Neural Information Processing Systems_
_Track on Datasets and Benchmarks 1, NeurIPS Datasets and Benchmarks 2021, December 2021,_
_virtual_, 2021b. URL `[https://datasets-benchmarks-proceedings.neurips.cc/paper/](https://datasets-benchmarks-proceedings.neurips.cc/paper/2021/hash/be83ab3ecd0db773eb2dc1b0a17836a1-Abstract-round2.html)`
`[2021/hash/be83ab3ecd0db773eb2dc1b0a17836a1-Abstract-round2.html](https://datasets-benchmarks-proceedings.neurips.cc/paper/2021/hash/be83ab3ecd0db773eb2dc1b0a17836a1-Abstract-round2.html)` .


Yuzhen Huang, Yuzhuo Bai, Zhihao Zhu, Junlei Zhang, Jinghan Zhang, Tangjun Su, Junteng
Liu, Chuancheng Lv, Yikai Zhang, Jiayi Lei, Yao Fu, Maosong Sun, and Junxian He. Ceval: A multi-level multi-discipline chinese evaluation suite for foundation models. In Alice Oh, Tristan Naumann, Amir Globerson, Kate Saenko, Moritz Hardt, and Sergey Levine
(eds.), _Advances_ _in_ _Neural_ _Information_ _Processing_ _Systems_ _36:_ _Annual_ _Conference_ _on_ _Neu-_
_ral_ _Information_ _Processing_ _Systems_ _2023,_ _NeurIPS_ _2023,_ _New_ _Orleans,_ _LA,_ _USA,_ _Decem-_
_ber 10 - 16, 2023_, 2023. URL `[http://papers.nips.cc/paper_files/paper/2023/hash/](http://papers.nips.cc/paper_files/paper/2023/hash/c6ec1844bec96d6d32ae95ae694e23d8-Abstract-Datasets_and_Benchmarks.html)`
`[c6ec1844bec96d6d32ae95ae694e23d8-Abstract-Datasets_and_Benchmarks.html](http://papers.nips.cc/paper_files/paper/2023/hash/c6ec1844bec96d6d32ae95ae694e23d8-Abstract-Datasets_and_Benchmarks.html)` .


10


Peng Jin, Bo Zhu, Li Yuan, and Shuicheng Yan. Moh: Multi-head attention as mixture-of-head
attention. _arXiv preprint arXiv:2410.11842_, 2024.


Guokun Lai, Qizhe Xie, Hanxiao Liu, Yiming Yang, and Eduard H. Hovy. RACE: large-scale reading
comprehension dataset from examinations. In Martha Palmer, Rebecca Hwa, and Sebastian Riedel
(eds.), _Proceedings of the 2017 Conference on Empirical Methods in Natural Language Processing,_
_EMNLP_ _2017,_ _Copenhagen,_ _Denmark,_ _September_ _9-11,_ _2017_, pp. 785–794. Association for
Computational Linguistics, 2017. doi: 10.18653/V1/D17-1082. URL `[https://doi.org/10.](https://doi.org/10.18653/v1/d17-1082)`
`[18653/v1/d17-1082](https://doi.org/10.18653/v1/d17-1082)` .


Zhenzhong Lan, Mingda Chen, Sebastian Goodman, Kevin Gimpel, Piyush Sharma, and Radu
Soricut. ALBERT: A lite BERT for self-supervised learning of language representations. In _8th_
_International Conference on Learning Representations, ICLR 2020, Addis Ababa, Ethiopia, April_
_26-30, 2020_ . OpenReview.net, 2020.


Yann LeCun, Léon Bottou, Yoshua Bengio, and Patrick Haffner. Gradient-based learning applied to
document recognition. _Proceedings of the IEEE_, 86(11):2278–2324, 2002.


Haonan Li, Yixuan Zhang, Fajri Koto, Yifei Yang, Hai Zhao, Yeyun Gong, Nan Duan, and Timothy
Baldwin. CMMLU: measuring massive multitask language understanding in chinese. In Lun-Wei
Ku, Andre Martins, and Vivek Srikumar (eds.), _Findings of the Association for Computational_
_Linguistics, ACL 2024, Bangkok, Thailand and virtual meeting, August 11-16, 2024_, pp. 11260–
11285. Association for Computational Linguistics, 2024. doi: 10.18653/V1/2024.FINDINGS-ACL.
671. URL `[https://doi.org/10.18653/v1/2024.findings-acl.671](https://doi.org/10.18653/v1/2024.findings-acl.671)` .


Aixin Liu, Bei Feng, Bin Wang, Bingxuan Wang, Bo Liu, Chenggang Zhao, Chengqi Dengr, Chong
Ruan, Damai Dai, Daya Guo, et al. Deepseek-v2: A strong, economical, and efficient mixture-ofexperts language model. _arXiv preprint arXiv:2405.04434_, 2024.


Jiawei Liu, Chunqiu Steven Xia, Yuyao Wang, and Lingming Zhang. Is your code generated
by chatGPT really correct? rigorous evaluation of large language models for code generation.
In _Thirty-seventh_ _Conference_ _on_ _Neural_ _Information_ _Processing_ _Systems_, 2023. URL `[https:](https://openreview.net/forum?id=1qvx610Cu7)`
`[//openreview.net/forum?id=1qvx610Cu7](https://openreview.net/forum?id=1qvx610Cu7)` .


Zhen Qin, Xuyang Shen, and Yiran Zhong. Elucidating the design space of decay in linear attention.
_arXiv preprint arXiv:2509.05282_, 2025.


Zihan Qiu, Zekun Wang, Bo Zheng, Zeyu Huang, Kaiyue Wen, Songlin Yang, Rui Men, Le Yu, Fei
Huang, Suozhi Huang, et al. Gated attention for large language models: Non-linearity, sparsity,
and attention-sink-free. _arXiv preprint arXiv:2505.06708_, 2025.


David Rein, Betty Li Hou, Asa Cooper Stickland, Jackson Petty, Richard Yuanzhe Pang, Julien
Dirani, Julian Michael, and Samuel R. Bowman. GPQA: A graduate-level google-proof q&a
benchmark. _CoRR_, abs/2311.12022, 2023. doi: 10.48550/ARXIV.2311.12022. URL `[https:](https://doi.org/10.48550/arXiv.2311.12022)`
`[//doi.org/10.48550/arXiv.2311.12022](https://doi.org/10.48550/arXiv.2311.12022)` .


Noam Shazeer. Fast transformer decoding: One write-head is all you need. _arXiv_ _preprint_
_arXiv:1911.02150_, 2019.


Noam Shazeer, Zhenzhong Lan, Youlong Cheng, Nan Ding, and Le Hou. Talking-heads attention.
_arXiv preprint arXiv:2003.02436_, 2020.


Jianlin Su. Moe travels 3, 3 2025. URL `[https://spaces.ac.cn/archives/10757](https://spaces.ac.cn/archives/10757)` .


Sho Takase, Shun Kiyono, Sosuke Kobayashi, and Jun Suzuki. Spike no more: Stabilizing the
pre-training of large language models. _arXiv preprint arXiv:2312.16903_, 2023.


Alon Talmor, Jonathan Herzig, Nicholas Lourie, and Jonathan Berant. Commonsenseqa: A question
answering challenge targeting commonsense knowledge. _arXiv preprint arXiv:1811.00937_, 2018.


Ning Tao, Anthony Ventresque, Vivek Nallur, and Takfarinas Saber. Enhancing program synthesis with large language models using many-objective grammar-guided genetic programming.
_Algorithms_, 17(7):287, 2024. doi: 10.3390/A17070287. URL `[https://doi.org/10.3390/](https://doi.org/10.3390/a17070287)`
`[a17070287](https://doi.org/10.3390/a17070287)` .


11


Kimi Team, Yifan Bai, Yiping Bao, Guanduo Chen, Jiahao Chen, Ningxin Chen, Ruijue Chen, Yanru
Chen, Yuankun Chen, Yutian Chen, et al. Kimi k2: Open agentic intelligence. _arXiv preprint_
_arXiv:2507.20534_, 2025.


Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N Gomez, Łukasz
Kaiser, and Illia Polosukhin. Attention is all you need. _Advances in neural information processing_
_systems_, 30, 2017.


Lean Wang, Huazuo Gao, Chenggang Zhao, Xu Sun, and Damai Dai. Auxiliary-loss-free load
balancing strategy for mixture-of-experts. _arXiv preprint arXiv:2408.15664_, 2024a.


Yubo Wang, Xueguang Ma, Ge Zhang, Yuansheng Ni, Abhranil Chandra, Shiguang Guo,
Weiming Ren, Aaran Arulraj, Xuan He, Ziyan Jiang, Tianle Li, Max Ku, Kai Wang, Alex
Zhuang, Rongqi Fan, Xiang Yue, and Wenhu Chen. Mmlu-pro: A more robust and challenging multi-task language understanding benchmark. In Amir Globersons, Lester Mackey,
Danielle Belgrave, Angela Fan, Ulrich Paquet, Jakub M. Tomczak, and Cheng Zhang (eds.),
_Advances_ _in_ _Neural_ _Information_ _Processing_ _Systems_ _38:_ _Annual_ _Conference_ _on_ _Neural_
_Information_ _Processing_ _Systems_ _2024,_ _NeurIPS_ _2024,_ _Vancouver,_ _BC,_ _Canada,_ _December_
_10_ _-_ _15,_ _2024_, 2024b. URL `[http://papers.nips.cc/paper_files/paper/2024/hash/](http://papers.nips.cc/paper_files/paper/2024/hash/ad236edc564f3e3156e1b2feafb99a24-Abstract-Datasets_and_Benchmarks_Track.html)`
```
 ad236edc564f3e3156e1b2feafb99a24-Abstract-Datasets_and_Benchmarks_Track.
```

`[html](http://papers.nips.cc/paper_files/paper/2024/hash/ad236edc564f3e3156e1b2feafb99a24-Abstract-Datasets_and_Benchmarks_Track.html)` .


Tianwen Wei, Jian Luan, Wei Liu, Shuang Dong, and Bin Wang. CMATH: can your language model
pass chinese elementary school math test? _CoRR_, abs/2306.16636, 2023. doi: 10.48550/ARXIV.
2306.16636. URL `[https://doi.org/10.48550/arXiv.2306.16636](https://doi.org/10.48550/arXiv.2306.16636)` .


Guangxuan Xiao, Yuandong Tian, Beidi Chen, Song Han, and Mike Lewis. Efficient streaming
language models with attention sinks. _arXiv preprint arXiv:2309.17453_, 2023.


Guangxuan Xiao, Jiaming Tang, Jingwei Zuo, Junxian Guo, Shang Yang, Haotian Tang, Yao Fu, and
Song Han. Duoattention: Efficient long-context llm inference with retrieval and streaming heads.
_arXiv preprint arXiv:2410.10819_, 2024.


An Yang, Anfeng Li, Baosong Yang, Beichen Zhang, Binyuan Hui, Bo Zheng, Bowen Yu, Chang
Gao, Chengen Huang, Chenxu Lv, et al. Qwen3 technical report. _arXiv preprint arXiv:2505.09388_,
2025.


Ted Zadouri, Hubert Strauss, and Tri Dao. Hardware-efficient attention for fast decoding. _arXiv_
_preprint arXiv:2505.21487_, 2025.


Rowan Zellers, Ari Holtzman, Yonatan Bisk, Ali Farhadi, and Yejin Choi. Hellaswag: Can a
machine really finish your sentence? In Anna Korhonen, David R. Traum, and Lluís Màrquez
(eds.), _Proceedings_ _of_ _the_ _57th_ _Conference_ _of_ _the_ _Association_ _for_ _Computational_ _Linguistics,_
_ACL_ _2019,_ _Florence,_ _Italy,_ _July_ _28-_ _August_ _2,_ _2019,_ _Volume_ _1:_ _Long_ _Papers_, pp. 4791–4800.
Association for Computational Linguistics, 2019. doi: 10.18653/V1/P19-1472. URL `[https:](https://doi.org/10.18653/v1/p19-1472)`
`[//doi.org/10.18653/v1/p19-1472](https://doi.org/10.18653/v1/p19-1472)` .


Wanjun Zhong, Ruixiang Cui, Yiduo Guo, Yaobo Liang, Shuai Lu, Yanlin Wang, Amin Saied, Weizhu
Chen, and Nan Duan. Agieval: A human-centric benchmark for evaluating foundation models. In
Kevin Duh, Helena Gómez-Adorno, and Steven Bethard (eds.), _Findings of the Association for_
_Computational Linguistics:_ _NAACL 2024, Mexico City, Mexico, June 16-21, 2024_, pp. 2299–2314.
Association for Computational Linguistics, 2024. doi: 10.18653/V1/2024.FINDINGS-NAACL.
149. URL `[https://doi.org/10.18653/v1/2024.findings-naacl.149](https://doi.org/10.18653/v1/2024.findings-naacl.149)` .


12


**A** **Appendix**


**A.1** **Comparison of Interactive-heads Attention Mechanisms**


We provide a comprehensive comparison of our knocking-heads attention with existing interactivehead mechanisms across multiple dimensions, as summarized in Table 6. Our analysis encompasses
three representative approaches: talking-heads attention (Shazeer et al., 2020), collaborated multihead attention (CollabHead) (Cordonnier et al., 2020), and mixture-of-head (MoH) (Jin et al., 2024).


The compared methods employ fundamentally different interaction strategies. Talking-heads attention
uses learnable transition matrices to directly combine attention weights across heads, achieving strong
interaction but with high complexity and FlashAttention incompatibility. MoH learns routers to
select heads for different tokens, promoting head specialization but lacking direct head interaction.
CollabHead enables head interaction by replacing individual head transformation matrices with one
large shared matrix across all heads, which compromises head specification and increases training
FLOPs due to the enlarged shared matrix. Our knocking-heads mechanism achieves head interaction
through lightweight feature-sharing modules inserted into existing attention variants, maintaining
both strong interaction and head specification with minimal overhead.


Table 6: Comparison of interactive-heads attention mechanisms: talking-heads (Shazeer et al.,
2020), collaborated multi-head (Cordonnier et al., 2020), mixture-of-head (Jin et al., 2024), and our
knocking-heads attention. “compute control" is about FLOPs, “compatibility" includes attention
variants and FlashAttention support, and “training stability" indicates loss spike frequency.


Interaction Head- Head- Compa- Compute Param Training
Method Interaction Specifiction tibility Control Control Stability


Talking-heads Mixing ✓Strong ✓Strong ✗ ✗ ✓ unknown
Collaborated-heads Sharing ✓Strong ✗Weak ✗ ✗ ✓ unknown
Mixture-of-head Re-weight ✗Weak ✓Strong ✓ ✓ ✓ unknown
Knocking-heads(Ours) Sharing ✓Strong ✓strong ✓ ✓ ✓ ✓


**A.2** **Evaluation Benchmark**


We assess model performance using a comprehensive benchmark spanning multiple downstream
tasks, which collectively measure different aspects of model competence. The evaluation framework
is organized into distinct task categories, including: (a) General Knowledge ( _e.g.,_ ARC (Bhakthavatsalam et al., 2021), AGIEval (Zhong et al., 2024), PIQA (Bisk et al., 2020), HellaSwag (Zellers
et al., 2019)) (b) Language Understanding ( _e.g.,_ RACE (Lai et al., 2017)) (c) Professional Knowledge
( _e.g.,_ MMLU (Hendrycks et al., 2021a), CMMLU (Li et al., 2024), MMLU-Pro (Wang et al., 2024b),
GPQA (Rein et al., 2023), C-Eval (Huang et al., 2023), CommonsenseQA (Talmor et al., 2018)))
(d) Math ( _e.g.,_ GSM8K (Cobbe et al., 2021), MATH (Hendrycks et al., 2021b), CMATH (Wei et al.,
2023) (e) Code ( _e.g.,_ HumanEval-plus (Liu et al., 2023), MBPP (Tao et al., 2024), MBPP-Plus (Liu
et al., 2023).


13


