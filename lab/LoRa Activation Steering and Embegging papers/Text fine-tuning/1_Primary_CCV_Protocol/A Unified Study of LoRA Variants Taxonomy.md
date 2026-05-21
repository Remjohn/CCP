JOURNAL OF L [A] TEX CLASS FILES, VOL. 18, NO. 9, SEPTEMBER 2020 1

## A Unified Study of LoRA Variants: Taxonomy, Review, Codebase, and Empirical Evaluation


Haonan He [1,2] _[†]_, Jingqi Ye [1,2] _[†]_, Minglei Li [1,3] _[†]_, Zhengbo Wang [2,5], Mengqi Li [6],
Tao Chen [3], Lei Bai [1], Peng Ye [1,3,4] _[∗]_

1Shanghai Artificial Intelligence Laboratory, Shanghai 200233, China
2University of Science and Technology of China, Hefei 230026, China
3Fudan University, Shanghai 200433, China
4The Chinese University of Hong Kong, Hong Kong SAR 999077, China
5Institute of Automation, Chinese Academy of Sciences, Beijing 100190, China
6The Chinese University of Hong Kong, Shenzhen, Shenzhen 518172, China



_**Abstract**_ **—Low-Rank** **Adaptation** **(LoRA)** **is** **a** **fundamental**
**parameter-efficient** **fine-tuning** **method** **that** **balances** **efficiency**
**and** **performance** **in** **large-scale** **neural** **networks.** **However,** **the**
**proliferation** **of** **LoRA** **variants** **has** **led** **to** **fragmentation** **in**
**methodology, theory, code, and evaluation. To this end, this work**
**presents** **the** **first** **unified** **study** **of** **LoRA** **variants,** **offering** **a**
**systematic** **taxonomy,** **unified** **theoretical** **review,** **structured** **code-**
**base, and standardized empirical assessment. First, we categorize**
**LoRA** **variants** **along** **four** **principal** **axes:** **rank,** **optimization**
**dynamics, initialization, and integration with Mixture-of-Experts.**
**Then,** **we** **review** **their** **relationships** **and** **evolution** **within** **a**
**common** **theoretical** **framework** **focused** **on** **low-rank** **update** **dy-**
**namics. Further, we introduce LoRAFactory, a modular codebase**
**that** **implements** **variants** **through** **a** **unified** **interface,** **supporting**
**plug-and-play** **experimentation** **and** **fine-grained** **analysis.** **Last,**
**using** **this** **codebase,** **we** **conduct** **a** **large-scale** **evaluation** **across**
**natural** **language** **generation,** **natural** **language** **understanding,**
**and image classification tasks, systematically exploring key hyper-**
**parameters. Our results uncover several findings, notably: LoRA**
**and** **its** **variants** **exhibit** **pronounced** **sensitivity** **to** **the** **choices**
**of** **learning** **rate** **compared** **to** **other** **hyperparameters;** **moreover,**
**with** **proper** **hyperparameter** **configurations,** **LoRA** **consistently**
**matches or surpasses the performance of most of its variants. All**
**code** **and** **configurations** **are** **publicly** **available** **at** **this** **[link.](https://anonymous.4open.science/r/MyTransformers-4EC3)**


_**Index**_ _**Terms**_ **—PEFT,** **LoRA,** **LLMs,** **Optimization.**


I. INTRODUCTION

ARGE-SCALE models with billions of parameters, such
as large language models (LLMs), which are pretrained
# **L**
on massive corpora, have demonstrated remarkable performance across diverse tasks, transforming fields ranging from
natural language processing to multimodal reasoning [1]–

[3]. However, full fine-tuning large-scale models is highly
resource-intensive, primarily due to the substantial GPU memory required to store optimizer states. To alleviate this burden, numerous parameter-efficient fine-tuning (PEFT) methods
have been proposed [4]–[8]. These approaches drastically
reduce memory usage by either minimizing the number of
trainable parameters or optimizing the management of optimizer states, especially for adaptive optimizers [9], [10].
Consequently, PEFT methods also enhance the training efficiency under distributed frameworks, such as ZeRO [11] and
FSDP [12], by reducing communication overhead.
Low-Rank Adaptation (LORA) [8] has emerged as one of
the most widely adopted PEFT methods. Its popularity stems


_†_ Equal contribution.
_∗_ Correspondence: yepeng@pjlab.org.cn.



from strong empirical performance, implementation simplicity,
and broad generalization across domains, including parametric
knowledge memory [13], [14], multimodal learning [15], [16],
and federated learning [17], [18]. Despite its efficiency and
effectiveness, such as fine-tuning 32B-scale models on a
consumer-level GPU through quantization methods [19], [20],
LORA still exhibits limitations, such as the low-rank structure,
which often results in a performance gap compared to full finetuning, particularly on complex downstream tasks.
To bridge this gap, numerous variants of LORA have been
developed, which can be broadly classified as follows: _Rank_
_Adjustment_ _Based_ _Variants_ (Section II-B) include methods
such as RELORA [21], which composes multiple low-rank
update subspaces; ADALORA [22], which dynamically masks
less important ranks; and RANDLORA [23], which enables
high-rank training via rank-sharing strategies. _Optimization_
_Process_ _Adjustment_ _Based_ _Variants_ (Section II-C) cover approaches like LORA+ [24], which decouples the learning
rates of low-rank weights for optimization stability; LORAPRO [25], which reduces the discrepancy with full fine-tuning
via parameter update space alignment. _Initialization_ _Adjust-_
_ment_ _Based_ _Variants_ (Section II-D) comprise techniques such
as PISSA [26], which applies Singular Value Decomposition
(SVD) on pretrained weights to extract dominant features for
initializing low-rank weights, and LORA-GA [27], which
performs SVD on the gradients of pretrained weights for
initialization. Lastly, _Mixture-of-Experts_ _(MoE)_ _Integration_
_Based_ _Variants_ (Section II-E) combine LORA with MoE
mechanisms to enable adaptive parameter activation, as exemplified by MIXTURE-OF-LORAS [28], which distributes lowrank updates across multiple conditionally activated experts.
Despite the rapid development, critical gaps remain in the field.
**First**, existing taxonomies in the general field of PEFT or
LORA outline broad and superficial organization, and thus
fail to render a fine-grained and systematic framework focused
on LORA variants based on their principal operational axes.
**Second,** there is a lack of an in-depth review. Surveys on
LORA do not provide a thorough review of the theoretical
foundations, design principles, and operational mechanisms
that distinguish LoRA variants. This limitation, combined with
the mathematical sophistication of many proposals, impedes
accessibility, especially for non-specialists. **Third,** code support is fragmented and unwieldy. While the popular PEFT
library [29] provides a basic LORA implementation with
useful features (e.g., multi-LoRA serving), it supports only


JOURNAL OF L [A] TEX CLASS FILES, VOL. 18, NO. 9, SEPTEMBER 2020 2





































Fig. 1. Hierarchical taxonomy of LoRA variants based on four core principle operational axes.



a limited set of variants. Worse, its codebase has become
cluttered with deeply nested logic and tight interdependencies,
making it difficult to read and extend. **Fourth,** evaluations
are inconsistent and limited in scope. The original LORA
paper conducts the evaluation using models like RoBERTa [30]
(GLUE [31]), GPT-2 [32] (E2E NLG [33]), and GPT-3 [34]
(WikiSQL [35], MNLI [31], SAMSum [36]). Recent works
now use large models such as LLaMA3 [37] and Qwen3 [38]
for evaluation, creating a comparison gap. Moreover, evaluations remain largely confined to language tasks, despite the
growing use of LORA in various domains.
To address these challenges, this work presents the **first** unified study of LORA variants: (1) We propose a structured and
fine-grained taxonomy (Figure 1) focused on LORA variants
according to their operational principles; (2) Building upon
the taxonomy, we conduct an in-depth review in Section II
grounded in a unified theoretical framework; (3) Further, we
provide a clean, modular codebase detailed in Section III that
implements variants as subclasses of a LORA base class,
thereby significantly enhancing readability and extensibility;
(4) Building on these infrastructures, we launch a large-scale
empirical study across three domains: natural language generation, natural language understanding, and image classification,
evaluating 20 representative variants that have been accepted in
top AI/ML venues under extensive hyperparameter sweeping.
We discover several important key findings as shown in
Section IV, especially, LORA can match or outperform most
of its variants with appropriate hyperparameter configurations.
Our work provides a solid foundation for future research. The
contributions are summarized as follows:


1) We formulate a structured taxonomy of LORA variants,
providing a **fine-grained** **systematic** **framework** based
on the principal operational axes of LORA variants.
2) We present a theoretical review of LORA variants,
which establishes a **unified** **foundation** rooted in lowrank adaptation dynamics to promote understanding.
3) We introduce **LoRAFactory**, which implements over
50 LORA variants and functions beyond a toolkit by
enabling standardized and extensible evaluations.



4) We conduct **large-scale** **evaluations** with over 3,000
experiments across 3 model architectures and 22 tasks,
spanning natural language generation, natural language
understanding, and image classification.
5) We uncover several **key findings**, with two being particularly noteworthy: (1) LORA and its variants are highly
sensitive to the learning rate compared to other hyperparameters; (2) LORA can match or outperform its most
variants with proper hyperparameter configurations.


II. REVIEW OF LORA AND ITS VARIANTS


In this section, we conduct a theoretical review; details of
the notations we used can be found in the Appendix B.


_A._ _Overview_ _of_ LORA


_1)_ _Mechanism_ _of_ LORA _:_ LORA is grounded in the hypothesis that the updates to pretrained weights during finetuning possess _low_ _intrinsic_ _ranks_, aligning with observations
that over-parameterized models often reside on a low intrinsic
dimension [98]. Specifically, at each fine-tuning step _t_, for a
pretrained weight matrix _W_ _∈_ R _[m][×][n]_, LORA approximates

[�]
the corresponding update ∆ _Wt_ using low-rank matrices _At_ _∈_
R _[m][×][r]_ and _Bt_ _∈_ R _[r][×][n]_, with _r_ _≪_ min( _m, n_ ). Formally:

_Wt_ = _W_ [�] + ∆ _Wt_ = _W_ [�] + _[α]_ _r_ _[A][t][B][t][.]_ (1)


Here, the product _AtBt_ is normalized by the rank _r_ and
scaled by a hyperparameter _α_ . This design ensures that the
magnitude of ∆ _Wt_ depends primarily on _α_ rather than the
rank _r_, allowing for more controllable fine-tuning. However,
empirical studies [99], [100] suggest setting _α_ to 2 _r_, as a
constant _α_ may lead LoRA to converge to low-rank solutions
even under large- _r_ settings.
_2)_ _Comparison_ _between_ LORA _and_ _Full_ _Fine-tuning:_
LORA is fundamentally related to full fine-tuning, though still
demonstrates differences in both optimization dynamics and
final performance. Mathematically, the gradients of a low-rank
adapter at the _t_ -th step are expressed as:



_∇At_ = _[α]_




_[α]_ _WtBt_ _[⊤][,]_ _∇Bt_ = _[α]_

_r_ _[∇]_ [�] _r_



_r_ _[A]_ _t_ _[⊤][∇]_ _W_ [�] _t._ (2)


JOURNAL OF L [A] TEX CLASS FILES, VOL. 18, NO. 9, SEPTEMBER 2020 3







As demonstrated in prior research [62], [70], under standard
LORA initialization with either small learning rates or a frozen
_A_ matrix (as in LORA-FA [101], [102]), the update can
be approximated, with exact simplification for frozen _A_ or
approximate simplification under small learning rates as:



(a) Rank Expansion
























|W|𝐵$#<br>L 𝐴#<br>$|𝐵$%<br>𝐴%<br>$|⋯|𝐵$&|Col6|
|---|---|---|---|---|---|
|W|L<br>𝐴$<br>#<br>𝐵$<br>#|𝐴$<br>%<br>𝐵$<br>%|⋯<br><br><br><br>|𝐴$<br>&<br>|𝐴$<br>&<br>|



|W|𝐵##<br>1 𝐴#<br>#|𝐵#%<br>𝐴#%|⋯|𝐵#&|Col6|
|---|---|---|---|---|---|
|W|1<br>𝐴#<br>#<br>𝐵#<br>#|𝐴#<br>%<br>𝐵#<br>%|⋯<br><br><br><br>|𝐴#<br>&<br>|𝐴#<br>&<br>|


X



∆ _Wt_ = _AtBt_ = _−η_ _[α]_

_r_



_t−_ 1

- _A_ 0 _A_ _[⊤]_ 0 _[∇]_ _W_ [�] _i._ (3)

_i_ =0























Moreover, the step-wise update obtained from the low-rank
adapter can be expressed as:


∆ _Wt_ +1 _−_ ∆ _Wt_ = ( _At_ +1 _−_ _η∇At_ )( _Bt_ +1 _−_ _η∇Bt_ ) _−_ _AtBt_
= _−ηAt∇Bt −_ _η∇AtBt_ + _η_ [2] _∇At∇Bt_

_≈−_ _[ηα]_ _t_ _[∇]_ _W_ [�] _t_ + _∇W_ [�] _tBt_ _[⊤][B][t]_ [)] _[,]_

_r_ [(] _[A][t][A][⊤]_
(4)
where the approximation holds under the assumption of a
small learning rate, such that the _O_ ( _η_ [2] ) term is negligible.
Eqs. (3)-(4) uncover the relationship between LORA
adapters and the gradients of pretrained weights. Especially,
Eq. (3) reveals that a LORA adapter essentially functions as a
gradient compressor, which first compresses the gradient of
the corresponding pretrained weight through _A_ _[⊤]_, and then
decompresses it via _A_ .
Despite the connection, LoRA differs in its optimization
dynamics, final performance, and applicable use cases. Ghosh
et al. [103] empirically show that during instruction tuning,
models fine-tuned with LORA retain closer alignment with
the pretrained knowledge, whereas full fine-tuning tends to
fit the instruction data closer. Specifically, LORA results
in a reduced token-level distribution shift compared to full
fine-tuning. It learns localized adaptations, such as sentence
initiation, leading to a more concentrated distribution shift. As
further validated by Biderman et al. [99] and Shuttleworth et
al. [100], LoRA better mitigates catastrophic forgetting [104].
Additionally, Biderman et al. [99], and Schulman et al. [105]
find that LORA is more sensitive to hyperparameters than full
fine-tuning, especially to the learning rate.
_3)_ _Advantages_ _of_ LORA _:_ LORA’s primary benefit lies
in its ability to significantly reduce the memory footprint
of optimizer states—particularly in mixed-precision training,
where stateful optimizers [9], [10], [106] require storing
states in 32-bit precision. Contrary to popular belief, LORA
introduces additional FLOPs in both training and inference
(without merging). This overhead is especially noticeable in
single-GPU and non-offload setups. However, in distributed
training settings, LORA can reduce communication costs
between devices and nodes, especially for optimizer offloading
strategies such as ZERO-OFFLOAD [107] and data parallelism
strategies such as ZERO [11] and FSDP [12], leading to faster
overall training processes.


_B._ _Rank_ _Adjustment_ _Based_ LORA _Variants_


Vanilla LORA applies a uniform small rank to all adapters
for simplicity, though this design can hinder both expressiveness and parameter efficiency. Since different modules and
layers contribute unevenly to downstream performance, a fixed
small-rank allocation can be inherently suboptimal.



Within phase _τ_ (i.e., for _tτ_ _−_ 1 _< t ≤_ _tτ_ ), the model weight is:

_Wt_ = _Wtτ_ _−_ 1 + _[α]_ _r_ _[A][t][B][t][.]_ (13)


After merging, low-rank matrices are reinitialized, and their
optimizer states are reset, enabling the exploration of a new



Fig. 2. Illustration of rank adjustment based LORA variants.


As shown in Figure 2, recent research investigates three
approaches: (a) Rank Expansion Methods, which composite
low-rank matrices through linear algebraic principles; (b) Rank
Sharing Methods, which share low-rank parameters across
adapters to enable larger rank configurations; (c) Rank Budgeting Methods, which dynamically allocate rank across modules
during or before training.
_1)_ _Rank_ _Expansion_ _Methods:_ Rank expansion methods
share a common objective: to preserve the parameter efficiency
(not equal to computational efficiency) of LORA while expanding the effective ranks. At their core, several well-known
rank inequalities and identities from linear algebra provide
theoretical justification for their effectiveness. These include:


_R_ ( _M_ 1 + _M_ 2) _≤R_ ( _M_ 1) + _R_ ( _M_ 2) _,_ (5)

_R_ ( _M_ 1 _⊙_ _M_ 2) _≤R_ ( _M_ 1) _· R_ ( _M_ 2) _,_ (6)

_R_ ( _M_ 1 _⊗_ _M_ 2) = _R_ ( _M_ 1) _· R_ ( _M_ 2) _,_ (7)

_R_ ( _M_ 1 _M_ 2) _≤_ min( _R_ ( _M_ 1) _, R_ ( _M_ 2)) _,_ (8)

max( _R_ ( _M_ 1) _, R_ ( _M_ 2)) _≤R_ ([ _M_ 1 _|M_ 2]) (9)

_R_ ([ _M_ 1 _|M_ 2]) _≤R_ ( _M_ 1) + _R_ ( _M_ 2) _,_ (10)







_R_




- _k−_ 1

 - _Mi_


_i_ =0



=



_n_

- _R_ ( _Mi_ ) _,_ (11)


_i_ =1



where _R_ ( _M_ ) denotes the rank of matrix _M_, _⊙_ the Hadamard
product, _⊗_ the Kronecker product, and [�] represents blockdiagonal concatenation. These guide the construction of composite structures, enabling richer representations without a
proportional increase in trainable parameters.
Inspired by Eq. (5), **RELORA** [21] introduces a _merge-_
_and-reinit_ strategy to construct higher-rank updates by accumulating low-rank subspaces.
Training is divided into _N_ phases, each consisting of _T_
steps. At step _t_, the current phase index is defined as _τ_ =
_⌊_ ( _t −_ 1) _/T_ _⌋_ + 1. Let _tτ_ := _τT_ denote the final step of phase
_τ_, with _t_ 0 := 0. At the end of phase _τ_, the low-rank update
is merged into the base weight:



_Wtτ_ =



�� _W,_ _τ_ = 0 _,_



_Wtτ_ _−_ 1 + _[α]_




_[α]_ _τ_ = 1 _,_ 2 _, . . ., N,_ (12)

_r_ _[A][t][τ][ B][t][τ][,]_


JOURNAL OF L [A] TEX CLASS FILES, VOL. 18, NO. 9, SEPTEMBER 2020 4



low-rank subspace. To mitigate instability from optimizer
resets, a jagged learning rate schedule, which re-warmups the
learning rate from zero at the next phase, is adopted.
**PERIODICLORA** [39] implements a method similar to
RELORA but introduces a momentum-based merging mechanism to enhance training stability. Additionally, **COLA** [40]
also proposes a similar approach with a motivation from
the Frank Wolfe algorithm [108]. Moreover, the _merge-and-_
_reinit_ method can also be viewed as a gradient boosting (GB)
method. From this perspective, Zhang et al. [41] draw inspiration from GB algorithms such as GBDT [109], proposing
**XGBLORA**, which randomly selects 2 layers to be trained
by rank-one adapters at each _merge-and-reinit_ phase.
However, the method of RELORA lacks a lower bound of
effective rank. Furthermore, as the _merge-and-reinit_ process
directly modifies the pretrained weights, these weights must be
saved after training, leading to substantial storage requirements
compared to LORA. To address these issues, **MELORA** [42]
draws inspiration from Eq. (11). Specifically, it partitions both
_At_ and _Bt_ into _k_ mini blocks and stacks them along the
diagonal to form the overall update:



�� _k_

 - _Bt_ _[i]_


_i_ =1







∆ _Wt_ =




- _k_

 - _A_ _[i]_ _t_


_i_ =1



_,_ (14)



_nd_ = max( _u ≤_ min( _k,_ _[√]_ _n_ ) _|n_ mod _u_ = 0) _,_ (19)

_At_ _∈_ R _[m][d][×][r]_ _,_ _Bt_ _∈_ R _[r][×][n][d]_ _,_ _Ct_ _∈_ R _[m/m][d][×][n/n][d]_ _,_ (20)

∆ _Wt_ = _[α]_ (21)

_r_ _[A][t][B][t][ ⊗]_ _[C][t][,]_


where _k_ is a hyperparameter. LOKR maintains comparable
parameter counts to LORA while significantly increasing
effective ranks.
_2)_ _Rank_ _Sharing_ _Methods:_ Parameter sharing is a widely
adopted strategy for neural networks [111], [112]. Recently,
it has also become prevalent for improving the parameter
efficiency of LORA, as it allows for sharing low-rank weights
across modules, thereby reducing the number of trainable parameters [47], [48], [54], [55]. For example, **VB-LORA** [54]
implements an extreme parameter efficiency method using a
shared vector bank strategy to composite low-rank matrices. In
this paper, we focus on another function of parameter sharing,
i.e., increasing the overall rank of adapters by sharing, and we
refer to this as _rank_ _sharing_ _strategies_ .
An intuitive parameter sharing strategy is to share the trainable low-rank matrices across all modules. Following this idea,
**SHARELORA** [47] investigates the performance of sharing
different components of the low-rank matrices, namely, matrix
_A_, matrix _B_, or both, across modules. Empirical results show
that sharing both _A_ and _B_ significantly reduces the trainable
parameter count but incurs a noticeable performance drop. In
contrast, sharing matrix _A_ achieves performance on par with
vanilla LORA while halving the trainable parameter count.
This observation suggests a practical strategy: by sharing
matrix _A_ and doubling the rank _r_, one can **potentially** surpass
the performance of standard LORA with the same trainable
parameter count. Formally, when both low-rank matrices _A_
and _B_ are shared across targeted modules, the update of a
SHARELORA adapter is defined as:



_mk_ _[×][r][′]_ _,_ _Bt_ _[i]_ _[∈]_ [R] _[r][′][×]_ _[n]_ _k_



_m_
_A_ _[i]_ _t_ _[∈]_ [R] _k_



_k_ _._ (15)



This construction ensures that the effective rank is equal to
_kr_ _[′]_ . When _r_ _[′]_ = _r_, MELORA increases the rank from _r_ to _kr_
without increasing the trainable parameter count. Conversely,
when _r_ _[′]_ = _k_ _[r]_ [, MEL][O][RA reduces the trainable parameter count]

by a factor of _k_, while preserving the rank of _r_ .
Hyeon-Woo et al. [43] draw inspiration from the Hadamard
product to enhance the expressiveness of LORA, proposing
FEDPARA (also known as **LOHA** [44]). Specifically, a LOHA
adapter reparameterizes the update to a pretrained weight
matrix via the Hadamard product of two low-rank matrix pairs:
_A_ [1] _t_ _[∈]_ [R] _[m][×][r]_ [,] _[A]_ [2] _t_ _[∈]_ [R] _[m][×][r]_ [and] _[B]_ _t_ [1] _[∈]_ [R] _[r][×][n]_ [,] _[B]_ _t_ [2] _[∈]_ [R] _[r][×][n]_ [.] [The]
adaptation update can be formally expressed as:



_A_ _[S]_ _t_ _[∈]_ [R] _[m]_ [max] _[×][r][,]_ _Bt_ _[S]_ _[∈]_ [R] _[r][×][n]_ [max] _[,]_ (22)



∆ _Wt_ = _[α]_



_t_ [[:] _[ m,]_ [ :]] _[B]_ _t_ _[S]_ [[:] _[,]_ [ :] _[ n]_ []] _[,]_ ∆ _Wt_ _∈_ R _[m][×][n]_ _,_ (23)
_r_ _[A][S]_



∆ _Wt_ = _[α]_ _t_ _[B]_ _t_ [1] _[⊙]_ _[A]_ _t_ [2] _[B]_ _t_ [2][)] _[.]_ (16)

_r_ [(] _[A]_ [1]



where _A_ _[S]_ _t_ _[, B]_ _t_ _[S]_ [are] [shared] [low-rank] [matrices] [at] [step] _[t]_ [,] _[m]_ [max]
and _n_ max denote the maximum input and output dimensions
across all adapted modules.
Building upon shared low-rank matrices, **VERA** [48] proposes a vector-based fine-tuning approach. It shares and fixes
randomly initialized low-rank matrices across modules, while
introducing trainable scaling vectors to modulate the adaptation. This design is motivated by findings that tuning small,
strategically chosen parts of randomly initialized models can
yield surprisingly strong performance [113]–[115]. Formally,
the adaptation in VERA is expressed as:


_A_ _[S]_ _∈_ R _[m]_ [max] _[×][r]_ _,_ _B_ _[S]_ _∈_ R _[r][×][n]_ [max] _,_ (24)



As shown in Eq. (6), LOHA enables an upper effective rank
bound of _r_ [2], while only doubling the trainable parameter count
compared to LORA with the same hyperparameter _r_ .
To approximate even higher-rank updates, **HIRA** [45] constructs the update to a pretrained weight via the Hadamard
product between the pretrained weight and the low-rank update. This update is formally expressed as:

∆ _Wt_ = _W_ [�] _⊙_ _[α]_ _r_ _[A][t][B][t][.]_ (17)


By leveraging the multiplicative interaction, HIRA allows
potential high-rank update bounding by the product of the rank
of the pretrained weight and the rank of the low-rank update.
Inspired by LOHA and **KRONA** [110], which employ
Kronecker products for matrix decomposition, Yeh et al. [44]
propose **LOKR**, which can be formally expressed as:

_md_ = max( _u ≤_ min( _k,_ _[√]_ _m_ ) _|m_ mod _u_ = 0) _,_ (18)



∆ _Wt_ = _[α]_



Λ _[d]_ _t_ _[∈]_ [R] _[r][×][r][,]_ Λ _[b]_ _t_ _[∈]_ [R] _[n][×][n][,]_ (25)



_t_ _[B][S]_ [[:] _[,]_ [ :] _[ n]_ []Λ] _t_ _[b][,]_ ∆ _Wt_ _∈_ R _[m][×][n]_ _,_ (26)
_r_ _[A][S]_ [[:] _[ m,]_ [ :]Λ] _[d]_



where Λ _[d]_ _t_ [and][ Λ] _t_ _[b]_ [are diagonal matrices constructed at the] _[ t]_ [-th]
step from the trainable vectors _dt_ _∈_ R _[r]_ and _bt_ _∈_ R _[n]_ .
**TIED-LORA** [53] further investigates the performance of
freezing different parts of shared low-rank matrices and scaling


JOURNAL OF L [A] TEX CLASS FILES, VOL. 18, NO. 9, SEPTEMBER 2020 5



vectors upon the architecture of VERA. This vector-based
formulation shifts the optimization focus to the scaling vectors,
enabling a substantial increase in rank while maintaining a
trainable parameter count smaller than that of vanilla LORA.
**RASA** [49] decomposes low-rank adaptation matrices into
shared and module-specific (local) components. For a lowrank adapter of rank _r_, RASA allocates _k_ ranks to be shared
across all modules of the same type (e.g., query projection
modules). Since these shared components have consistent
shapes, no slicing operations are required during computation.
The remaining _r −_ _k_ ranks are kept specific to each module.
In a model with _L_ layers, the effective rank of each RASA
adapter becomes ( _r_ _−_ _k_ ) + _L_ _×_ _k_, while the total number
of trainable parameters remains identical to a LORA adapter
of rank _r_ . Formally, the update ∆ _Wt_ computed by a RASA
adapter is given by:



efficiency of RANDLORA, and ~~_√_~~ 2 _nb_ is a scaling factor. Here,
_A_ _[S]_ _t_ _[∈]_ [R][min(] _[d,k]_ [)] _[×][r]_ [and] _[B]_ _t_ _[S][i]_ _∈_ R _[r][×]_ [max(] _[d,k]_ [)] are shared random
basis matrices ( _A_ _[S]_ _t_ [is] [further] [shared] [across] [random] [bases),]
and Γ _[i]_ _t_ _[∈]_ [R] _[m][×][m]_ [,] [Λ] _[i]_ _t_ _[∈]_ [R] _[r][×][r]_ [are] [module-specific] [trainable]
scaling coefficients. For compatibility between adapted layers
with distinct input and output dimensions and the fixed random
_⊤_ _S_ _⊤_
bases, RANDLORA swaps _A_ _[S]_ _t_ [and] _[B]_ _t_ _[S][i]_ with _Bt_ _[S][i]_ and _At_

when the largest dimension of an adapted module is not its
output dimension.
**DENSELORA** [50] proposes a strategy that additionally
refines the low-rank hidden states rather than only fine-tuning
the low-rank weights. Specifically, DENSELORA shares lowrank weights _A_ _[S]_ _t_ [and] _[ B]_ _t_ _[S]_ [across modules of the same type and]
introduces an intermediate module-specific trainable matrix
_Ct_ _∈_ R _[r][×][r]_ to refine the hidden states. Formally, the adaptation
form of DENSELORA can be expressed as:

∆ _Wt_ = _[α]_ _t_ _[C][t][B]_ _t_ _[S][.]_ (33)

_r_ _[A][S]_


By sharing low-rank matrices, DenseLoRA sharply reduces the
trainable parameters, enabling high-rank configurations with
smaller or comparable parameter counts compared with LoRA.
The aforementioned sharing-based methods share ranks
across modules. In contrast, **PROLORA** [51] shares ranks
intra low-rank matrices. The computation of a PROLORA
adapter can be expressed as:


∆ _Wt_ = _AtBt_ =

 - ��  - _⊤_ (34)
_A_ _[L]_ _t_ _[|][ A]_ _t_ _[S]_ [1] _| · · · | A_ _[S]_ _t_ _[P][ −]_ [1] _Bt_ _[L]_ _[|][ B]_ _t_ _[S]_ [1] _| · · · | BStP −_ 1 _,_

where _A_ _[L]_ _t_ _[, B]_ _t_ _[L]_ [are local (rank-specific) low-rank matrices, and]
_A_ _[S]_ _t_ _[i][, B]_ _t_ _[S][i]_ are components obtained by applying a row-wise
cyclic shift to a shared base matrix: _A_ _[S]_ _t_ _[i]_ = Roll( _A_ _[S]_ _t_ [0] _[, i][ ·][ δ][A]_ [)][,]
_Bt_ _[S][i]_ = Roll( _Bt_ _[S]_ [0] _[, i][ ·][ δ][B]_ [)][.] [Here,] _[δ][A]_ [and] _[δ][B]_ [are] [the] **[strides]** [that]
control the shift offset. This share and shift strategy allows
parameters to be reused between ranks, enabling a larger
effective rank.
_3)_ _Rank_ _Budgeting_ _Methods:_ As we mentioned before,
LORA neglects different modules contribute unequally to taskspecific adaptation [22], [117]–[119]. Allocating overmuch
ranks to less critical modules may waste parameter budgets
and potentially lead to overfitting, while assigning insufficient
ranks to pivotal modules could constrain their ability to learn
task-specific information. Consequently, the core challenge of
such methods lies in intelligently and adaptively allocating the
ranks of low-rank adapters with a predefined budget.
To facilitate masking ranks to a budget, **ADALORA** [22]
parameterizes a low-rank adapter as ∆ _Wt_ = _AtDtBt_ _[⊤]_ [, factor-]
ized form analogous to truncated SVD, where _At_ _∈_ R _[m][×][r]_ and
_Bt_ _∈_ R _[n][×][r]_ are matrices containing vectors simulating singular
vectors, and _Dt_ _∈_ R _[r][×][r]_ is a diagonal matrix containing values
simulating singular values. To simulate the orthogonality of
SVD during training, an auxiliary regularization term _L_ reg is
added to the training loss with a hyperparameter _λ_ :


_R_ orth( _A, B_ ) = _∥A_ _[⊤]_ _A −_ _I∥_ [2] F [+] _[ ∥][B][⊤][B][ −]_ _[I][∥]_ F [2] _[,]_ (35)



∆ _Wt_ = - _Bt_ _[L]_ _Bt_ _[S]_ - _Dt_ _[L]_




- _ALt_
_A_ _[S]_ _t_




_,_ (27)



where _A_ _[L]_ _t_ [and] _[B]_ _t_ _[L]_ [are] [the] [local] [low-rank] [weights,] [and] _[D]_ _t_ _[L]_ [is]
a trainable diagonal scaling matrix.
Similar to RASA, **BSLORA** [52] decomposes low-rank
adapters into three parts: _inter-layer_ _shared_ _parts_, _intra-layer_
_shared_ _parts_, and _local_ _parts_ . This stems from an entropybased analysis [116] on fine-tuned low-rank adapters, revealing
high similarity of adapters within and between adjacent layers,
indicating redundancy and sharing potential. Formally, the
update ∆ _Wt_ of BSLORA is:


∆ _Wt_ = 2 _×_ ( _A_ _[L]_ _t_ _[B]_ _t_ _[L]_ [+] _[ T]_ [ (] _[A]_ _t_ _[S]_ [1] _[B]_ _t_ _[S]_ [1][) +] _[ T]_ [ (] _[A]_ _t_ _[S]_ [2] _[B]_ _t_ _[S]_ [2][))] _[,]_ (28)


where _T_ ( _·_ ) enables shape-flexible parameter sharing, and 2 is
a fixed scaling factor (adopted in the official [implementation).](https://github.com/yuhua-zhou/BSLoRA/blob/bf2f69c295e183578706d35a19c849ef8623e10b/peft/tuners/share_lora/layer.py#L137)
Here, _A_ _[S]_ _t_ [1] _[, B]_ _t_ _[S]_ [1] are shared within a layer, and _A_ _[S]_ _t_ [2] _[, B]_ _t_ _[S]_ [2] are
shared across layers. As slicing (Eq. (23)) requires shared
weights to be initialized at the maximum module dimension,
BSLORA introduces two compact transformations _T_ ( _AB_ ) as:


_Tg_ ( _AB_ ) = _GioGidABGodGou,_ _AB_ _∈_ R _[k][×][d]_ _,_ (29)

_Tk_ ( _AB_ ) = ( _KA ⊗_ _A_ )( _KB_ _⊗_ _B_ ) _,_ (30)


where _Gid_ _∈_ R [1] _[×][k]_, _God_ _∈_ R _[d][×]_ [1], _Giu_ _∈_ R _[m][×]_ [1], _Gou_ _∈_ R [1] _[×][n]_

are gating matrices, and _KA_ _∈_ R _[m/k][×]_ [1], _KB_ _∈_ R [1] _[×][n/d]_ are
Kronecker kernels. These allow shared weights of an arbitrary
size _k × d_ to be efficiently transformed to target dimensions
_m × n_, enabling flexible, efficient, and adaptive sharing.
**RANDLORA** [23] performs full-rank weight updates by
decomposing a weight update ∆ _Wt_ _∈_ R _[m][×][n]_ into a sum of
products involving shared, fixed, randomly initialized low-rank
bases and trainable scaling coefficients:


_nb_ = _⌈_ min( _ds, U_ ) _/r⌉_ _,_ (31)



2
∆ _Wt_ = ~~_√_~~
_nb_



_nb_

- Γ _[i]_ _t_ _[A][S]_ _t_ [[:] _[ m,]_ [ :]Λ] _t_ _[i][B]_ _t_ _[S][i]_ [[:] _[,]_ [ :] _[ n]_ []] _[,]_ (32)

_i_ =1



where _ds_ denotes the smaller dimension of the module with the
largest output dimension among all target modules. (adopted
in the PEFT [implementation),](https://github.com/huggingface/peft/blob/337be05f03fd5c631154ba58afcc95c2c86529d8/src/peft/tuners/randlora/model.py#L198) _U_ is an additional hyperparameter introduced in LoRAFactory to balance computational



_L_ reg = _λ ·_



_k_

- _R_ orth( _A_ _[i]_ _t_ _[, B]_ _t_ _[i]_ [)] (36)


_i_ =1


JOURNAL OF L [A] TEX CLASS FILES, VOL. 18, NO. 9, SEPTEMBER 2020 6



where _k_ is the number of ADALORA adapters in the model.
ADALORA incorporates an importance scoring mechanism
to mask less critical ranks. At each training step _t_, the _i_ -th
diagonal value of _Dt_ is masked to zero or retained after each
backpropagation update, according to the importance score _St_ _[i]_
of the _i_ -th triplet of the adapter, comprising the _i_ -th columns
_a_ _[i]_ _t_ _[∈]_ [R] _[m]_ [and] _[b][i]_ _t_ _[∈]_ [R] _[n]_ [of] _[A][t]_ [and] _[B][t]_ [,] [and] [the] _[i]_ [-th] [diagonal]
value _d_ _[i]_ _t_ [of] _[D][t]_ [,] [as] [follows:]



During fine-tuning, additional rank-one components with randomly initialized _a, b_ ( _d_ will be initialized with a small value)
are allocated every _tn_ steps to the top- _h_ most important
modules at that interval. Both _h_ and _tn_ are hyperparameters. A
separate learning rate warmup and decay schedule is applied
for newly added rank-one components. As a result, the ranks of
modules with high importance are incrementally increased at
every _tn_ steps until the total rank budget is exhausted. The importance score used by INCRELORA adopts the same smoothing strategy as ADALORA; the raw (unsmoothed) modulewise importance is computed by averaging all sensitivity
scores in the corresponding update matrix. The orthogonality
regularization (Eq. 36) is also applied by INCRELORA.
SALORA [56] extends ADALORA with a distinct masking
strategy that formulates rank budgeting as an optimizable
objective via _L_ 0 regularization on simulated singular values.
This is achieved through two techniques: (1) a differentiable
surrogate _RL_ 0 approximating the non-differentiable _L_ 0 norm,
and (2) Lagrangian relaxation to embed the rank budget
constraint _b_ into the loss for automatic budget control.
SALORA maps the diagonal entries of matrix _D_ to [0 _,_ 1]
using a Hard-Concrete (HC) distribution with _u ∼U_ (0 _,_ 1):



_d_ _[i]_ _t_ _[←]_ _[m]_ _t_ _[i]_ _[·][ d]_ _t_ _[i][,]_ where _m_ _[i]_ _t_ [=]




1 if _St_ _[i]_ _[≥]_ _[θ][t][,]_
(37)
0 otherwise _._



Here, the threshold _θt_ is set to the _bt_ -th largest value of
importance scores of all triplets in the model, such that exactly
_bt_ singular values remain masked. The budget _bt_, which
controls the number of active singular values at each step _t_,
follows a piecewise schedule across _T_ total steps:



_bt_ =








_b_ 0 _,_ 0 _≤_ _t < ti,_
_b_ [anneal] _t_ _,_ _ti_ _≤_ _t < T_ _−_ _tf_ _,_ (38)
_bT,_ otherwise _,_







where _b_ 0 and _bT_ are the initial and final budgets, respectively.
During the annealing phase, _b_ [anneal] _t_ decreases cubically from
_b_ 0 to _bT_ over the interval [ _ti, T_ _−_ _tf_ ), following:



_d_ ˜ _[i]_ _t_ [=] _[ σ]_



 log� 1 _−uu_ - + log( _d_ _[i]_ _t_ [)]









_τ_






 _·_ ( _ζ −_ _γ_ ) + _γ,_ (46)




       - _t −_ _ti_
_b_ [anneal] _t_ = _bT_ + ( _b_ 0 _−_ _bT_ ) 1 _−_ _T_ _−_ _ti −_ _tf_



�3
_._ (39)



∆ _Wt_ =



_r_

- min�1 _,_ max(0 _,_ _d_ [˜] _[i]_ _t_ [)] - _· a_ _[i]_ _t_ _[b]_ _t_ _[i]_ _⊤,_ (47)


_i_ =1



One of the metrics for accurately estimating importance scores
is a sensitivity measurement, defined below to capture the
influence of parameter _w_ on the loss across update steps:


_I_ ( _w_ ) = _|w · g|,_ (40)
_I_ ¯ _t_ ( _w_ ) = _β_ 1 ¯ _It−_ 1( _w_ ) + (1 _−_ _β_ 1) _It_ ( _w_ ) _,_ (41)
_U_ ¯ _t_ = _β_ 2 ¯ _Ut−_ 1( _w_ ) + (1 _−_ _β_ 2) _|I_ ( _w_ ) _−_ _I_ ¯ _t−_ 1( _w_ ) _|,_ (42)

_st_ ( _w_ ) = _I_ [¯] _t_ ( _w_ ) _·_ _U_ [¯] _t_ ( _w_ ) _,_ (43)


where _g_ is the gradient of _w_, _β_ 1 and _β_ 2 are hyperparameters
that are smaller than 1. The importance score of ADALORA
is therefore defined as:



where _σ_ is the sigmoid function, _τ_ is its temperature, and
_γ_ _<_ 0, _ζ_ _>_ 1 are HC hyperparameters that push most values
outside [0 _,_ 1] toward ( _−∞,_ 0) or (1 _, ∞_ ). The surrogate _RL_ 0
has a closed-form expression based on the HC distribution:



��
_._



_RL_ 0( _D_ ) = P( _d_ [˜] _[i]_ _t_ _[>]_ [ 0) =]



_r_





- _σ_ �log( _di_ ) _−_ _τ_ log� _−γ_

_ζ_
_i_ =1



(48)
Given a target rank budget _b_, **SALORA** combines _RL_ 0 with
orthogonality regularization _R_ orth in Eq. 35 via Lagrangian
relaxation, yielding the following regulation loss with hyperparameters _λ_ and _β_ :



_L_ reg = _λ ·_



_St_ _[i]_ [=] _[ s][t]_ [(] _[d]_ _t_ _[i]_ [) +] [1]

_m_



_m_





- _st_ ( _a_ _[ij]_ _t_ [) +] [1]

_n_

_j_ =1



_n_




- _RL_ 0( _Dt_ _[i]_ [)] _[ −]_ _[b]_


_i_ =1



2




_._



_n_

- _st_ ( _b_ _[ij]_ _t_ [)] (44)

_j_ =1



_k_





1

_r_



_k_





- _R_ orth( _A_ _[i]_ _t_ _[, B]_ _t_ _[i]_ [) +] _[ β][ ·]_


_i_ =1



These designs enable ADALORA to adaptively allocate representational capacity during training, pruning less informative
directions while preserving those critical for performance.
However, due to the masking mechanism, ADALORA initializes low-rank adapters with a uniform initial rank slightly
larger than the final average rank (e.g., 1.5 times), leading
to parameter redundancy, and the maximum rank of each
adapter is bounded by the initial rank, limiting the model’s
capacity to expand its representational budget. To address
this issue, **INCRELORA** [59] adopts an incremental rank
allocation strategy. It first views the parameterization _AtDtBt_ _[⊤]_
with the sum of the product of rank-one components _a_, _b_, and
_d_ :



(49)
**ALORA** [60] introduces a rank reallocation strategy based
on a train-evaluate-reallocate-retrain loop. At its core lies
Ablation-based LoRA (AB-LORA), an importance estimation
method designed to guide rank reallocation. For a given rank
component _ri_, its importance score is computed as:


IS( _ri_ ) = _S_ ( _M_ ) _−_ _S_ ( _M\ri_ ) + _S_ ( _Mri_ ) _,_ (50)


where _S_ ( _M_ ) denotes the performance of the fully fine-tuned
model, _S_ ( _M\ri_ ) is the performance after removing the component with rank _ri_, and _S_ ( _Mri_ ) is the performance of the model
when only rank _ri_ is retained. Based on these scores, the least
important ranks are removed from their respective modules
and reallocated to more critical ones. The model is then further
fine-tuned to adapt to the updated rank configuration.



∆ _Wt_ = _AtDtBt_ _[⊤]_ [=]



_r_





- _d_ _[i]_ _t_ _[·][ a]_ _t_ _[i][b][i]_ _t⊤._ (45)

_i_ =1


JOURNAL OF L [A] TEX CLASS FILES, VOL. 18, NO. 9, SEPTEMBER 2020 7





The core idea of **GORA** [62] is to perform a one-off gradient computation on a small subset of training data before training, jointly achieving adaptive rank allocation and gradientdriven weight initialization (detailed in Section II-D2). By
initializing low-rank matrices with allocated ranks, GORA
adaptively assigns more parameters to modules that have
a greater impact on final performance, avoiding parameter
redundancy and maintaining training stability. Specifically,
GORA first measures the advantage of each weight on _k_
pretrained weights to be adapted _{W_ [�] _i}_ _[k]_ _i_ =0 [with corresponding]
gradients _{Gi}_ _[k]_ _i_ =0 [based] [on] [loss] [sensitivity:]


_Ii_
_Ii_ = avg( _|W_ [�] _i ⊙_ _Gi|_ ) _,_ _αi_ =       - _k_ _._ (51)
_i_ =1 _[I][i]_


The rank for the _i_ -th low-rank adapter is determined by:





















_P_ total =



_k_
�( _mi_ + _ni_ ) _· r_ ref (52)


_i_ =1



_ri_ = round( ~~_√_~~ _[P]_ [total] _[ ·][ α][i]_ ) _,_ s _._ t _._ _r_ min _≤_ _ri_ _≤_ _r_ max _,_ (53)
_mi_ + _ni_


Where round( _·_ ) denotes rounding to the nearest integer, and
_r_ ref is a reference rank to control the parameter budget, and
_r_ min _, r_ max are predefined bounds of rank allocation.
Building upon the framework of GORA, **RALORA(-**
**PRO)** [63] further introduces an entropy-based effective rank
estimator to measure the intrinsic dimensionality of gradient
matrices _{Gi}_ _[k]_ _i_ =0 [:]



_n_

- _pi_ log _pi_


_i_ =1



_σi_
_, pi_ = - _n_ _,_ (54)
_j_ =1 _[σ][j]_







Fig. 3. Illustration of optimization process adjustment based LORA variants.


_C._ _Optimization_ _Process_ _Adjustment_ _Based_ LORA _Variants_


As shown in Figure 3, this section introduces LORA variants that directly adjust the optimization process of LORA,
including:(a) Stability Enhancement Methods focus on regulating training dynamics to prevent collapse or instability. (b)
Update Alignment Methods aim to bridge the gap between
low-rank adaptation and full fine-tuning.
_1)_ _Stability_ _Enhancing_ _Methods:_ **RSLORA** [65] introduces an optimized scaling factor for LORA to achieve a
rank-stabilized optimization process, ensuring two key rankstability properties: (1) **Forward** **Stability** : If the input _X_ _∈_
R _[bs][×][m]_ to the low-rank adapter is i.i.d. with an m’th moment
of Θ _r_ (1) per entry, then the m’th moment of the adapter’s
outputs remains Θ _r_ (1) per entry. (2) **Backward** **Stability** : If
the gradients of the loss with respect to the adapter outputs
are Θ _r_ (1) per entry, then the gradients propagated back to
the adapter’s inputs also maintain Θ _r_ (1) per entry. Consider
_r→∞_
the scaling factor to be optimized _γr_ _∈_ R with _γr_ _−−−→_ 0,
which constrains the product of low-rank matrices as the rank
_r_ increases. For any training step _t >_ 1, the low-rank matrices
evolve according to the gradient formula in Eq (2) and the
inductive derivation:


_At_ = ( _I_ + _Or_ ( _γr_ [2][))] _[A]_ [0] _[,]_ (56)



erank( _Gi_ ) = exp





_−_



where _pi_ denotes the normalized singular value distribution.
The core insight of RALORA(-PRO) is revealing the substantial gap between the fixed small rank of the low-rank
adapter (typically 8) and the gradient’s intrinsic dimensionality
(GID), which can be up to 300. Building on this observation,
using the block-diagonal structure in Eq. (14), RaLoRA aligns
each low-rank adapter’s effective rank to the corresponding
GID by adaptively increasing the number of diagonal blocks
without increasing the total parameter count. RaLoRA-Pro further incorporates the parameter allocation strategy of GORA,
achieving dual adaptive alignment at both intra-layer and interlayer levels with a manual parameter budget.
**EVA** [64] performs incremental SVD on downstream activation vectors and selects the top- _r_ right singular vectors
to initialize the low-rank matrix _A_, thereby capturing the
highest-variance directions in activation space and theoretically maximizing the initial gradient signal (in this section, we
focus solely on EVA’s adaptive rank allocation; initialization
is discussed in Section II-D3). Specifically, EVA computes the
explained variance ratio for each singular vector:


_σj_ _[i]_ [2]
_ξj_ _[i]_ [=] _,_ (55)
( _M_ _−_ 1) _||_ _**σ**_ _[i]_ _||_ 1


and globally redistributes the rank budget by prioritizing directions with the largest explained variance, effectively reducing
redundancy while preserving the most informative subspaces.



_,_ (57)



_t−_ 1





- _∇W_ [�] _i_ + _Or_ ( _γr_ [2][)]


_i_ =0







_Bt_ = _A_ _[⊤]_ 0


_γrAtBt_ = _−ηγr_ [2]





_−ηγr_



_t−_ 1

- _A_ 0 _A_ _[⊤]_ 0 _[∇]_ _W_ [�] _i_ + _A_ 0 _A_ _[⊤]_ 0 _[O][r]_ [(] _[γ]_ _r_ [3][)] _[.]_ (58)

_i_ =0



Assuming the entries of _A_ 0 are i.i.d. with mean 0, variance _σA_
(E _A_ 0[ _A_ 0 _A_ _[⊤]_ 0 [] =] _[ rσ][A][I]_ [),] [the] [expectation] [of] [Eq.] [(58)] [becomes:]



E _A_ 0[ _γrAtBt_ ] = _−γr_ [2] _[rσ][A][η]_



_t−_ 1

- _∇W_ [�] _i_ + _Or_ ( _γr_ [3] _[r]_ [)] _[,]_ (59)


_i_ =0



For an adapted linear model where _Y_ = _X_ ( _W_ [�] + _AB_ ), the
gradient _G_ and output _O_ of the adapter satisfy:



_G_ = _−γr_ [2] _[rσ][A][η]_



_t−_ 1

- _∇XtYi_ _[⊤][X][i]_ [+] _[ O][r]_ [(] _[γ]_ _r_ [3] _[r]_ [)] _[,]_ (60)

_i_ =0



E _X,A_ 0[ _O_ ] = _−γr_ [2] _[rσ][A][η]_



_t−_ 1


_∇_ E _X_ [ _XtXi_ _[⊤]_ []] _[Y][i]_ [+] _[ O][r]_ [(] _[γ]_ _r_ [3] _[r]_ [)] _[,]_
_i_ =0

(61)


JOURNAL OF L [A] TEX CLASS FILES, VOL. 18, NO. 9, SEPTEMBER 2020 8



where _G_ _∈Or_ ( _γr_ [2] _[r]_ [)] [and] [E] _[X,A]_ 0 [[] _[O]_ []] _[∈O][r]_ [(] _[γ]_ _r_ [2] _[r]_ [)][.] [To] [maintain]
both forward and backward stability, we require _Or_ ( _γr_ [2] _[r]_ [)] [=]
_Or_ (1), implying _γr_ _∈Or_ (1 _/_ _[√]_ _r_ ). Therefore, RSLORA recommends setting the scaling factor from _[α]_ _r_ [to] ~~_√_~~ _αr_ .

Hayou et al. [24] analyze the optimization dynamics of
models adapted via low-rank adapters in the limit as the model
width _m_ _→∞_ increases and propose **LORA+** which sets
the learning rate of matrix _B_ 2 [4] times that of matrix _A_ . In
the wide-network regime, one expects the change in model
predictions at any training step _t_ to remain stable—specifically,
that the prediction increment ∆ _ft_ ( _x_ ) = _ft_ ( _x_ ) _−ft−_ 1( _x_ ) scales
as Θ(1), meaning it neither vanishes nor diverges.
To investigate this behavior, Hayou et al. consider a simplified, analytically tractable model defined as _f_ ( _x_ ) = _x_ _[⊤]_ ( _w_ +
                                _ab_ ), where _w_ _∈_ R _[m]_ is a fixed pretrained weight vector,

     _a_ _∈_ R _[m]_ and _b_ _∈_ R are trainable rank-one components, and
the input _x_ _∈_ R _[m]_ satisfies _∥x∥_ = Θ(1). Following standard
LoRA initialization, the variances of the initial parameters are
_σa_ [2] 0 [= Θ(] _[m][−]_ [1][)][ and] _[ σ]_ _b_ [2] 0 [= Θ(1)][. In this setting, the prediction]
increment at step _t_ is given by:



∆ _ft_ ( _x_ ) = _−ηb_ [2] _t−_ 1 [(] _[f][t][−]_ [1][(] _[x]_ [)] _[ −]_ _[y]_ [)] _[∥][x][∥]_ 2 [2]

_−_ _η_ ( _a_ _[⊤]_ _t−_ 1 _[x]_ [)][2][(] _[f][t][−]_ [1][(] _[x]_ [)] _[ −]_ _[y]_ [)]

+ _η_ [2] ( _ft−_ 1( _x_ ) _−_ _y_ ) [2] _bt−_ 1( _a_ _[⊤]_ _t−_ 1 _[x]_ [)] _[∥][x][∥]_ 2 [2] _[,]_



(62)



Zhang et al. [66] investigate another solution for
stable ∆ _ft_ ( _x_ ) under _m_ _→_ _∞_ increases, leveraging Riemannian preconditioning. Specifically, their approach—RIEMANNIAN PRECONDITIONED LORA (which we
denote as **RPLORA** )—employs a Riemannian metric derived
from a regularized Lagrangian framework. This metric is
grounded in the geometric optimization principles for low-rank
matrices with objectives and constraints introduced by Mishra
and Sepulchre [120]. Following this, RPLORA modifies the
gradients of the low-rank adapter parameters according to the
natural gradient flow on the manifold of fixed-rank matrices,
effectively preconditioning the optimization dynamics to maintain stability:


_∇A_ _[∗]_ _t_ [=] _[ ∇][A][t]_ [(] _[B][t][B]_ _t_ _[⊤]_ [)] _[−]_ [1] _[,]_ _∇Bt_ _[∗]_ [= (] _[A]_ _t_ _[⊤][A][t]_ [)] _[−]_ [1] _[∇][B][t][,]_ (65)


where _∇A_ _[∗]_ and _∇B_ _[∗]_ are the modified gradients of RPLORA
for a low-rank adapter. Under the modified gradients, the
prediction increment shown in Eq. (62) can be rewritten as:


∆ _ft_ ( _x_ ) = _−η_ ( _ft−_ 1( _x_ ) _−_ _y_ ) _∥x∥_ [2] 2

_−_ _η_ ( _a_ _[⊤]_ _t−_ 1 _[x]_ [)][2][(] _[f][t][−]_ [1][(] _[x]_ [)] _[ −]_ _[y]_ [)] _[ ∥][a][t][−]_ [1] _[∥][−]_ 2 [2]
+ _η_ [2] ( _ft−_ 1( _x_ ) _−_ _y_ ) [2] _b_ _[−]_ _t−_ [1] 1 _[∥][a][t][−]_ [1] _[∥]_ 2 _[−]_ [2] ( _a_ _[⊤]_ _t−_ 1 _[x]_ [)] _[∥][x][∥]_ 2 [2] _[.]_
(66)
Similar to Eq. (63), defining _δt_ [1] _[, δ]_ _t_ [2] _[, δ]_ _t_ [3] [with] [the] [three] [terms] [of]
Eq. (66), we can rewrite the constraints shown in Eq. (64) as:



where _y_ denotes the ground-truth label, the learning rate is
_η_ = Θ( _m_ _[c]_ ) for some constant _c ∈_ R, and the loss function is
21 [(] _[f]_ [(] _[x]_ [)] _[ −]_ _[y]_ [)][2][.] [For] [clarity,] [define] [the] [following] [terms:]


_δt_ [1] [=] _[ ηb]_ _t_ [2] _−_ 1 [(] _[f][t][−]_ [1][(] _[x]_ [)] _[ −]_ _[y]_ [)] _[∥][x][∥]_ 2 [2] _[,]_








_δt_ [2] [=] _[ η]_ [(] _[a]_ _t_ _[⊤]_ _−_ 1 _[x]_ [)][2][(] _[f][t][−]_ [1][(] _[x]_ [)] _[ −]_ _[y]_ [)] _[,]_

_δt_ [3] [=] _[ η]_ [2][(] _[f][t][−]_ [1][(] _[x]_ [)] _[ −]_ _[y]_ [)][2] _[b][t][−]_ [1][(] _[a]_ _t_ _[⊤]_ _−_ 1 _[x]_ [)] _[∥][x][∥]_ 2 [2] _[.]_



(63)



 _c_ + 1 = 0 (for _δt_ [1] [= Θ(1)][)] _[,]_

_c_ + 2 _γ_ [ _a_ _[⊤]_ _t−_ 1 _[x]_ []] _[ −]_ _[γ]_ [[] _[∥][a][t][−]_ [1] _[∥]_ [2] 2 [] = 0] (for _δt_ [2] [= Θ(1)][)] _[,]_

 _γ_ [ _bt−_ 1] + _γ_ [ _a_ _[⊤]_ _t−_ 1 _[x]_ [] = 0] (for _ft_ ( _x_ ) = Θ(1)) _,_

(67)
where we can drive _c_ = _−_ 1 and correspondingly _η_ = _m_ _[−]_ [1] .
Under _σb_ [2] 0 [=] [Θ(1)] [and] _[a][⊤]_ 0 _[x]_ _[∈O]_ [(1)][,] [one] [can] [recursively]
derive _bt, a_ _[⊤]_ _t_ _[x, δ]_ _t_ [1] _[, δ]_ _t_ [2] _[, δ]_ _t_ [3] _[∈O]_ [(1)] [for] [all] _[t]_ [.] [Hence,] [the] [stable]
training dynamics are achieved.

_2)_ _Alignment_ _Enhancing_ _Methods:_ Liu et al. [67] perform
a weight decomposition analysis on the fine-tuning updates
from both LORA and full fine-tuning, revealing an interesting
contrast: while LORA’s updates demonstrate a positive correlation between magnitude and directional changes, full finetuning exhibits a slightly inverse relationship. This discrepancy
motivates their proposed method, **DORA**, which decouples
magnitude and directional learning in LORA, addressing the
potential complexity of jointly optimizing both components
and achieving an optimization pattern more closely aligning
that of full fine-tuning. Formally, the adapted weight of DORA
can be expressed as:







The stable optimization dynamics requires _δt_ [1] _[, δ]_ _t_ [2] _[, δ]_ _t_ [3] _∈_
Θ(1), which further implies _ft_ ( _x_ ) _∈_ Θ(1) throughout training.
Notably, _δt_ [3] _[∈]_ [Θ(1)][ is automatically satisfied if] _[ δ]_ _t_ [1] _[, δ]_ _t_ [2] _[∈]_ [Θ(1)][,]
since it is a higher-order term in _η_ .
Notation _γ_ [ _·_ ] introduced such that _ν_ = Θ( _m_ _[γ]_ [[] _[ν]_ []] ) captures
the asymptotic scaling of any quantity _ν_ . The conditions for
stable dynamics yield the following system of constraints:

 _c_ + 2 _γ_ [ _bt−_ 1] + 1 = 0 (for _δt_ [1] [= Θ(1)][)] _[,]_



_c_ + 2 _γ_ [ _bt−_ 1] + 1 = 0 (for _δt_ [1] [= Θ(1)][)] _[,]_
_c_ + 2 _γ_ [ _a_ _[⊤]_ _t−_ 1 _[x]_ [] = 0] (for _δt_ [2] [= Θ(1)][)] _[,]_ (64)
_γ_ [ _bt−_ 1] + _γ_ [ _a_ _[⊤]_ _t−_ 1 _[x]_ [] = 0] (for _ft_ ( _x_ ) = Θ(1)) _._







Solving this system yields _c_ = _−_ [1] 2 [,] [implying] [that] [the]

learning rate should scale as _η_ _∈O_ ( _m_ _[−]_ [1] _[/]_ [2] ). However, due
to the initialization _σb_ [2] 0 = Θ(1) and _a_ _[⊤]_ 0 _[x]_ _[∈O]_ [(1)] [(by]
the _Central_ _Limit_ _Theorem_ ), one can inductively show that
_bt_ _∈O_ ( _m_ _[−]_ [1] _[/]_ [2] ) and _a_ _[⊤]_ _t_ _[x][ ∈O]_ [(] _[m][−]_ [1] _[/]_ [2][)] [for] [all] _[t >]_ [ 0][,] [resulting]
in _ft_ ( _x_ ) _∈O_ ( _m_ _[−]_ [1] _[/]_ [2] ). Consequently, the parameter updates
for _at_ and _bt_ are of order _O_ ( _m_ _[−]_ [1] ) and _O_ ( _m_ _[−]_ [1] _[/]_ [2] ).
This analysis reveals that _δt_ [1] [and] _[δ]_ _t_ [2] [cannot] [simultaneously]
be Θ(1) under standard LoRA configurations with a shared
learning rate. To resolve this, Hayou et al. propose decoupling
the learning rates for _a_ and _b_, suggesting that _ηb_ _∈O_ (1) (for _b_ )
and _ηa_ _∈O_ ( _m_ _[−]_ [1] ) (for _a_ ) can restore stable training dynamics.



_Wt_ = _mt ·_ _W_ - + _γrAtBt_
���� _W_ + _γrAtBt_ ��� _F_



_,_ _γr_ = _[α]_ (68)

_r_ _[,]_



where _mt_ is a learnable magnitude vector, initialized as the
Frobenius norm on the input dimension of the pretrained
weight.
Similarly, **DELORA** [68] introduces a strategy that decouples the directional and magnitude updates by combining


JOURNAL OF L [A] TEX CLASS FILES, VOL. 18, NO. 9, SEPTEMBER 2020 9



LORA with the idea of **ETHER** [121]. Formally, the adaptation in DELORA can be expressed as:



_λ_ �� _W_ ��
∆ _Wt_ = _AtDtBt_ = ���2
_r_



_r_



_i_ =1



from the singular components of the gradient to retain gradient
information as much as possible.
**LORA-PRO** [25] enhances the alignment between LORA’s
optimization dynamics and full fine-tuning by explicitly minimizing the **step-wise** **discrepancy** between: the indirect updates to pretrained weights via LORA (Eq. (4)) and the direct
weight updates from full fine-tuning. LORA-PRO’s objective
can be viewed as an operational extension of LORA-GA’s
principle (Section II-D2), generalizing the single-step gradient
alignment to step-wise matching. LORA-PRO incorporates
RSLORA’s scaling factor and optimizes:



_⊤_
_a_ _[i]_ _t_ _[b][i]_ _t_ _,_ (69)

_∥a_ _[i]_ _t_ _[∥]_ [2] _[∥][b]_ _t_ _[i][∥]_ [2]



where _a_ _[i]_ _t_ [and] _[b][i]_ _t_ [are] [the] _[i]_ [-th] [rank-one] [components] [of] [the] [low-]
rank matrices, and _Dt_ is a diagonal matrix containing the
scaling factors based on the norms of these components. Here,
_λ_ is a trainable scalar that controls the upper bound on the
norm of the update as:



_λ_ �� _W_ ��
_∥AtDtBt∥_ 2 = �� _r_ �2



�����




- _a_ _[i]_ _t_ _[b][i]_ _t_


_i_ =0



����



2



_,_ (77)
_F_



where _∇A_ _[∗]_ _t_ _[,][ ∇][B]_ _t_ _[∗]_ are optimized gradients of _At, Bt_,
_sAt∇Bt_ _[∗]_ [+] _[s][∇][A][t][B]_ _t_ _[∗]_ [represents] [the] [optimized] [indirect] [update.]



_r_




_α_
���� ~~_√_~~ _r_ ( _At∇Bt_ _[∗]_ [+] _[ ∇][A]_ _t_ _[∗][B][t]_ [)] _[ −∇]_ _W_ [�] _t_



_≤_ _λ_ _W_ (70)
�������2 _[.]_
�����2



arg min
_∇A_ _[∗]_ _t_ _[,][∇][B]_ _t_ _[∗]_



The bounded adaptation prevents the adapted model from
diverging from the pretrained model.
Hao et al. [70] also utilize inductive derivation for _At, Bt_
to analyze the optimization dynamics of LoRA. Specifically,
assume ���� _ti_ =0 _[∇]_ _W_ [�] _i_ ��� _F_ _[≤]_ _[L]_ [(constant] _[L]_ [is] [defined] [as] [an]
upper bound) for every training step _t_, which implies that the
model stays within a finite Euclidean ball. In this case, by
induction:



_∂D_
= ~~_√_~~ [2] _[α]_ _Bt_ _[⊤]_ [(] _[sA][t][∇][B]_ _t_ _[∗]_ [+] _[ s][∇][A]_ _t_ _[∗][B][t]_ _[−∇]_ _W_ [�] _t_ ) = 0 _,_ (78)
_∂∇A_ _[∗]_ _t_ _r_

_∂D_
= ~~_√_~~ [2] _[α]_ _sA_ _[⊤]_ _t_ [(] _[sA][t][∇][B]_ _t_ _[∗]_ [+] _[ s][∇][A]_ _t_ _[∗][B][t]_ _[−∇]_ _W_ [�] _t_ ) = 0 _._ (79)
_∂∇Bt_ _[∗]_ _r_



2
Denoting _D_ = _sAt∇Bt_ + _s∇AtBt −∇W_ - _t_
��� ���



Denoting _D_ = _sAt∇Bt_ + _s∇AtBt −∇W_ - _t_ [we] [derive]

_F_ [,]
the following optimality conditions:




_[α]_ _Bt_ = _η_ _[α]_

_r_ _[f][A]_ [(] _[t]_ [))] _[A]_ [0] _[,]_ _r_



_At_ = ( _I_ + _η_ _[α]_



0 _[f][B]_ [(] _[t]_ [)] _[,]_ (71)
_r_ _[A][⊤]_



Assuming _At, Bt_ maintain full rank during training such
that _A_ _[⊤]_ _t_ _[A][t]_ [and] _[B][t][B]_ _t_ _[⊤]_ [are] [invertible,] [we] [derive] _[∇][B][∗]_ [:]



where _fA_ ( _t_ ) and _fB_ ( _t_ ) are defined by induction as:



_t−_ 1

- _∇Wf_ [�] _B_ _[⊤]_ [(] _[i]_ [)] _[,]_ (72)

_i_ =0



_√_
_r_
_∇Bt_ _[∗]_ [=]



_fA_ ( _t_ ) = _−η_ _[α]_

_r_



_fA_ ( _t_ ) = _−η_ _[α]_



_r_ _[f]_ _A_ _[ ⊤]_ [(] _[i]_ [))] _[∇]_ _W._ [�] (73)



_∇Bt_ _[∗]_ [=] _t_ _[A][t]_ [)] _[−]_ [1] _[A]_ _t_ _[⊤][∇]_ _W_ [�] _t −_ ( _A_ _[⊤]_ _t_ _[A][t]_ [)] _[−]_ [1] _[A]_ _t_ _[⊤][∇][A]_ _t_ _[∗][B][t][.]_

_α_ [(] _[A][⊤]_
(80)
Substituting Eq. (80) into Eq. (78) and solving the resulting
equation yields the expression for _∇A_ _[∗]_ _t_ [:]



_√_
_r_
_∇A_ _[∗]_ _t_ [=]



_WtBt_ _[⊤]_ [(] _[B][t][B]_ _t_ _[⊤]_ [)] _[−]_ [1][ +] _[ A][t][M][t][,]_ (81)
_α_ _[∇]_ [�]



_fB_ ( _t_ ) = _−_



_t−_ 1




�( _I_ + _η_ _[α]_

_r_

_i_ =0



The adapter’s computation at step _t_ can be expressed as:



∆ _W_ = _γrAtBt_ = _η_ _[α]_ [2]




_[α]_ _r_ [2][2] _[A]_ [0] _[A]_ 0 _[⊤][f][A]_ [(] _[t]_ [)+] _[η]_ [2] _[α]_ _r_ [3][3]



∆ _W_ = _γrAtBt_ = _η_ _r_ [2] _[A]_ [0] _[A]_ 0 _[⊤][f][A]_ [(] _[t]_ [)+] _[η]_ [2] _r_ [3] _[f][B]_ [(] _[t]_ [)] _[A]_ [0] _[A]_ 0 _[⊤][f][A]_ [(] _[t]_ [)] _[.]_

(74)
Hao et al. further establish the upper bound at every step:



_r_ _[L]_ [2][)] _[t]_ [)]
_∥fA_ ( _t_ ) _∥_ 2 _≤_ _[ηγ][r][L]_ [2] 1 [(1] _−_ _[ −]_ _η_ [2][(] _γ_ _[η]_ _r_ [2][2] _L_ _[γ]_ [2][2] _,_ (75)

where _γr_ = _αr_ [.] [This] [bound] [reveals] [that] [the] [second] [term]

in Eq. (74) becomes negligible when _ηγr_ _≪_ _L_, since this
condition ensures lim _t→∞_ _ηγr ∥fA_ ( _t_ ) _∥≪_ 1. Consequently:

∆ _W_ = _γrAtBt_ _≈_ _γrA_ 0 _B_ [˜] _t_ =: _ηγr_ [2] _[A]_ [0] _[A][⊤]_ 0 _[f]_ [˜] _[B]_ [(] _[t]_ [)] _[,]_ (76)

where we can define _f_ [˜] _B_ ( _t_ ) =: _f_ [˜] _B_ ( _t−_ 1) _−∇W_ [�] _t_ = [�] _i_ _[t]_ =0 _[∇]_ _W_ [�] _i_ .
Substituting this into Eq (76), we can obtain the expression
presented in Eq (3), which implies that LoRA adapters function as gradient compressors under small learning rates.
Building upon this insight, Hao et al. propose **FLORA** [70],
which employs a random low-rank projection matrix _A_ _[⊤]_ _∈_
R _[r][×][m]_ to compress the gradients of a pretrained weight of
size _m_ _×_ _n_ . The method efficiently computes and stores
optimizer states using the compressed gradient, subsequently
decompressing the optimizer’s updates through _A_, enabling
an intuitive update alignment. GALORE [122] proposes a
similar framework where the projection matrix is obtained



where _Mt_ _∈_ R _[r][×][r]_ is an arbitrary matrix. Substituting Eq. (81)
into Eq. (80) we have:

_√_
_r_
_∇Bt_ _[∗]_ [=] _t_ _[A][t]_ [)] _[−]_ [1] _[A]_ _t_ _[⊤][∇]_ _W_ [�] _t_ [ _I−Bt_ _[⊤]_ [(] _[B][t][B]_ _t_ _[⊤]_ [)] _[−]_ [1] _[B][t]_ []] _[−][B][t][M][t][,]_

_α_ [(] _[A][⊤]_
(82)
The final solutions to the objective of LORA-PRO are shown
in Eqs. (81)-(82). To utilize these solutions, LoRA-Pro alters
the gradients of _A_ and _B_, effectively aligning the indirect
updates from LORA to the direct updates from full-finetuning
(LORA-PRO only utilizes the values and gradients of low-rank
matrices to compute the aligned gradients since _∇W_ [�] _tBt_ _[⊤]_ =
_∇At_ and _A_ _[⊤]_ _t_ _[∇]_ _W_ [�] _t_ = _∇Bt_ ).
To obtain the solution for the arbitrary matrix _M_, LORAPRO further consider the following optimization objective:

arg min _M_ _[∥∇][A]_ _t_ _[∗]_ _[−∇][A][t][∥]_ _F_ [2] [+] _[ ∥∇][B]_ _t_ _[∗]_ _[−∇][B][t][∥]_ _F_ [2] _[,]_ (83)


which can be optimized by solving the Sylvester equation:

_MtBtBt_ _[⊤]_ [+] _[ A]_ _t_ _[⊤][A][t][M][t]_ [=] _[ −]_ _α_ _[r]_ [2] _[A]_ _t_ _[⊤][∇][A][t]_ [(] _[B][t][B]_ _t_ _[⊤]_ [)] _[−]_ [1] _[,]_ (84)

which has a unique solution provided that _BtBt_ _[⊤]_ [and] _[ −][A]_ _t_ _[⊤][A][t]_
do not have any shared eigenvalues.
Integrating LORA with intermediate nonlinear functions is
also a prevalent line of research [72]–[75]. Si et al. [123]


JOURNAL OF L [A] TEX CLASS FILES, VOL. 18, NO. 9, SEPTEMBER 2020 10































Fig. 4. Illustration of initialization adjustment based LORA variants.



argue that the linear coupling mechanism in LoRA restricts
its capacity to represent arbitrary rank-r matrices; therefore,
introducing an intermediate _r × r_ matrix or nonlinearity function between _A_ and _B_ serves as a viable solution for a closer
alignment with the learning capability of full fine-tuning. Dong
et al. [72] assert that methodologies such as **MOSLORA** [92]
and **FLORA** (Si et al.) [71], which incorporate an intermediate
_r ×_ _r_ matrix, preserve the linearity of LoRA and consequently
restrict the exploration of broader parameter spaces.
**LODA(+)** [75] integrates LoRA with a multi-layer nonlinear activation structure to relax the low-rank linear constraint.
Following the convention of PEFT methods, we denote the
effective weight update induced by LoDA+ as ∆ _W_, defined
implicitly through its action on the input:
_α_ _[α]_



of the other to vanish initially. For example, if _B_ 0 = 0, then
_∇A_ 0 = 0, preventing updates to _At_ until _Bt_ = 0.
This gradient suppression results in significantly slower
convergence compared to full fine-tuning, particularly when
using small learning rates. As discussed in Section II-A3,
LORA does not reduce the overall computational complexity
of training relative to full fine-tuning. Consequently, the slower
convergence can result in substantially more FLOPs to achieve
comparable performance. As shown in Figure 4, to address this
limitation, while also aiming to improve performance, several
advanced initialization strategies have been proposed.
_1)_ _Data-independent Init Methods:_ Typically, the initialization scheme of LORA is defined as follows: (1) the weight
matrix _A_ is initialized using either a Gaussian distribution
(reported in the original paper) or a Kaiming uniform distribution ( adopted in the official [implementation](https://github.com/microsoft/LoRA/blob/c4593f060e6a368d7bb5af5273b8e42810cdef90/loralib/layers.py/#L124) and the [PEFT](https://github.com/huggingface/peft/blob/47313792ddea21decbf0cad195cb880e7a487864/src/peft/tuners/lora/layer.py/#L260)
[library), while (2) the weight matrix](https://github.com/huggingface/peft/blob/47313792ddea21decbf0cad195cb880e7a487864/src/peft/tuners/lora/layer.py/#L260) _B_ is initialized with zeros.
Formally, when employing a Kaiming uniform distribution, the
initialization can be expressed as:




   _A_ 0 _∼U_ _−_ ~~_√_~~ [1] _,_ + ~~_√_~~ [1]
_m_ _m_




_,_ _B_ 0 = **0** _r×n._ (88)



_α_

[:=] _[α]_
_r_ _[X]_ [∆] _[W]_ _r_




       - _f_ 1( _XAB_ )�) _,_ (85)
_r_ [(] _[XAB]_ [ +] _[ f]_ [2]



The original paper does not explore the potential differences
between initializing matrix _A_ with zeros versus initializing
matrix _B_ with zeros. Intuitively, one might assume these two
initialization schemes exhibit similar performance. However,
Hayou et al. [77] verify that under Kaiming init [124] or
Lecun init [125], initializing matrix _B_ with zeros yields better
performance and robustness to the learning rate.
Shiwei et al. [76] further explore a scheme where both
matrices _A_ and _B_ are randomly initialized (referred to as
**NZLORA** in this paper). Given hyperparamters _γA_ and _γB_,
NZLORA can be formally expressed as:



where _f_ 1( _·_ ) and _f_ 2( _·_ ) are parameterized nonlinear transformations (e.g., small linear layers with LeakyReLU activations).
As illustrated in Figure 1 of the original paper, _f_ 1 comprises
two _r × r_ matrices interleaved with three LeakyReLU functions, while _f_ 2 consists of a single LeakyReLU function. ∆ _W_
in LODA+ does not correspond to a fixed low-rank matrix
but rather an input-dependent mapping, and thus cannot be
explicitly materialized as a standalone weight matrix. (The
original paper did not specify the use of scaling for LODA+;
therefore, scaling is omitted here.)
Similar to LODA+, **AURORA** enhances LORA with an
adaptive nonlinear layer (ANL) that combines both fixed and
learnable nonlinear components. Formally, the effective weight
update in Aurora can be expressed as:




   _A_ 0 _∼U_ _−_ ~~_√_~~ _[γ][A]_ _,_ + ~~_√_~~ _[γ][A]_
_m_ _m_




- _,_ _B_ 0 _∼U_ _−_ ~~_√_~~ _[γ][B]_ _,_ + ~~_√_~~ _[γ][B]_
_m_ _m_




_._



_fANL_ ( _M_ ) = tanh(tanh( _M_ )) + _Vs · S_ ( _M_ ) _,_ (86)
_α_ _[α]_



_α_

[:=] _[α]_
_r_ _[X]_ [∆] _[W]_ _r_



(87)
_r_ _[f][ANL]_ [(] _[XA]_ [)] _[B,]_



(89)
NZLORA accelerates convergence by addressing the small
gradient issue of vanilla LORA, making it more robust to
sub-optimal learning rates. A common challenge with nonzero initialization schemes is training instability. To mitigate
this, existing methods typically adjust pretrained weights by
subtracting the low-rank adapter’s initial values—a process we
term pretrained weights manipulation. However, this approach
has a key limitation: since the pretrained weights must be
modified again during inference, storing only the tuned lowrank adapters becomes infeasible. NZLORA demonstrates that
with carefully calibrated initialization variances (controlled by
_γA_ and _γB_ ), pretrained weights manipulation can be safely
omitted without compromising final fine-tuning performance.
The strategic initialization of low-rank adapters using pretrained weight statistics has become one of the dominant
paradigms in data-independent initialization schemes. This
methodology enables precise fine-tuning of targeted feature
subspaces within pretrained weights.
**PISSA** [26] laid the foundation for initialization from
statistics of pretrained weights. PISSA initializes the adapter
components using SVD of a pretrained weight matrix as:
_W_     - = _UW_     - _[S]_ _W_ [�] _[V]_ _W_     - _[⊤][,]_ (90)



where the first term in the ANL function _fANL_ ( _·_ ) represents a
fixed nonlinear mapping implemented via the tanh activation
function, and the second term introduces a learnable nonlinear
mapping based on B-spline basis functions. Here, _C_ _∈_ R _[r][×][r]_ is
an intermediate square matrix, _S_ ( _·_ ) is the spline basis function
and _Vs_ _∈_ R _[r]_ is the spline weight vector.


_D._ _Initialization_ _Adjustment_ _Based_ LORA _Variants_


In the standard LORA implementation, the gradients of _A_
and _B_ depend on each other’s magnitudes (i.e., as indicated
by Eq (2), initializing one matrix to zero causes the gradient


JOURNAL OF L [A] TEX CLASS FILES, VOL. 18, NO. 9, SEPTEMBER 2020 11



_A_ 0 = _UW_     - [[:] _[,]_ [ :] _[ r]_ []] _[S]_ _W_     - [1] _[/]_ [2][[:] _[ r,]_ [ :] _[ r]_ []] _[,]_ (91)

_B_ 0 = _SW_     - [1] _[/]_ [2][[:] _[ r,]_ [ :] _[ r]_ []] _[V]_ _W_     - _[⊤]_ [[:] _[ r,]_ [ :]] _[.]_ (92)


Effectively capturing the most principal features of the original weight matrix according to the ECKART-YOUNG THEOREM [126], [127]. This inspired a series of subsequent
works [69], [79]–[81], [128].
In contrast to this principal-component approach,
**MILORA** [78] exploits the minor components:


_A_ 0 = _UW_    - [[:] _[,][ −][r]_ [:]] _[S]_ _W_    - [1] _[/]_ [2][[] _[−][r]_ [:] _[,][ −][r]_ [:]] _[,]_ (93)

_B_ 0 = _SW_    - [1] _[/]_ [2][[] _[−][r]_ [:] _[,][ −][r]_ [:]] _[V]_ _W_    - _[⊤]_ [[:] _[,][ −][r]_ [:]] _[.]_ (94)


This preserves the primary knowledge in frozen weights while
adaptively learning from the less dominant features.
**OLORA** [129] uses QR decomposition for initialization as:


_W_   - = _QR, A_ 0 = _Q_ [: _,_ : _r_ ] _, B_ 0 = _R_ [: _r,_ :] _,_ (95)


where _Q_ _∈_ R _[m][×][m]_ is orthonormal and _R_ _∈_ R _[m][×][n]_ is upper
triangular. This method achieves orthonormal initialization
with computational efficiency.
Building upon these foundations, **SORSA** [81] enhances
orthonormal preservation through a regularization scheme. The
method modifies PISSA’s initialization while enforcing strict
orthonormality constraints:


_A_ 0 = _UW_  - [[:] _[,]_ [ :] _[ r]_ []] _[, B]_ [0] [=] _[ V]_ _W_  - _[⊤]_ [[:] _[ r,]_ [ :]] _[, D]_ [0] [=] _[ S]_ _W_ [�][[] _[r]_ [:] _[, r]_ [:]] _[,]_ (96)

_Wt_ = _W_ [�] + ∆ _Wt_ = _W_ [�] + _AtDtBt,_ (97)



Assuming the gradient matrix _∇W_ [�] is invertible and 2 _r_ _<_
min( _m, n_ ), multiplying _A_ 0 _A_ _[⊤]_ 0 [or] _[B]_ 0 _[⊤][B]_ [0] [by] [an] [invertible] [ma-]
trix does not alter its rank. Therefore, the maximum possible
rank of _P_ ( _A_ 0 _, B_ 0 _, ∇W_ [�] ) is 2 _r_ . In essence, LORA-GA seeks
to construct the optimal rank-2 _r_ approximation of the gradient
matrix _∇W_ [�] via _P_ ( _A_ 0 _, B_ 0 _, ∇W_ [�] 0).
The solution of Eq. (99) can be derived from the truncated
SVD of the pretrained weight gradient matrix as follows:

_∇W_ [�] 0 = _U∇W_ �0 _[S]_ _∇W_ [�] 0 _[V]_ _∇_ _[⊤]_ _W_ [�] 0 _[,]_ (100)

_A_ 0 = _U∇W_ �0 [[:] _[,]_ [ :] _[ r]_ []] _[,]_ _B_ 0 = _V∇_ _[⊤]_ _W_ [�] 0 [[] _[r]_ [ + 1 : 2] _[r,]_ [ :]] _[.]_ (101)


Following Eqs. (100)–(101), before the formal training
phase, LORA-GA efficiently computes and offloads the gradients of the pretrained weights layer by layer, resembling the
fused gradient approach proposed in LOMO [130] without
performing optimization steps.
To further align with the scaling factor introduced by
RSLORA [65] which we discussed in Section II-C, LORAGA incorporates the following scaling mechanism:




_[√]_ 4
_m_
~~_√_~~ _V_ _[⊤]_
_γ_ _∇W_ [�] 0 [[] _[r]_ [ + 1 : 2] _[r,]_ [ :]] _[,]_



_A_ 0 =




_[√]_ 4
_m_
~~_√_~~ _γ_ _U∇W_ �0 [[:] _[,]_ [ :] _[ r]_ []] _[,]_ _B_ 0 =



(102)



_L_ reg := �� _A⊤t_ _[A][t]_ _[−]_ _[I]_ ��2



2 _F_ [+] �� _BtBt⊤_ _[−]_ _[I]_ ��2



(98)
_F_ _[,]_



where _γ_ denotes a hyperparameter introduced by LORA-GA
to control the scaling.
**LORA-ONE** [82] identifies several purported misconceptions in LORA-GA and proposes modifications to its SVDbased feature selection and scaling mechanisms. The authors contend that under LORA’s standard zero-initialization
scheme, as shown in Eq. (88), the weight matrix _B_ - after the
first training step—naturally resides in the top- _r_ subspace of
the right singular matrix of the gradient matrix. Furthermore,
they argue that the subsequent training dynamics of _B_ remain
confined to this invariant subspace, while matrix _A_ aligns with
the top- _r_ subspace of the left singular matrix of the gradient
matrix under certain requirements.
Based on this premise, LORA-ONE asserts that initializing
_B_ with _V_ _[⊤]_ [:] [2] _[r,]_ [ :]] [results] [in] [suboptimal] [alignment,]
_∇W_ [�] 0 [[] _[r]_ [ + 1]
trapping the optimization in an undesirable subspace. Instead,
they claim _B_ should align with _V_ _[⊤]_ _[r,]_ [ :]][.] [However,] [since]
_∇W_ [�] 0 [[:]
this observation hinges on LORA’s default zero-initialization
scheme, its applicability to LORA-GA - which employs a
different initialization strategy - remains questionable.
Moreover, the indirect update to pretrained after the first
gradient descent step of LORA-GA is given by:
~~_√_~~ _α_ _A_ 1 _B_ 1 _−_ ~~_√_~~ _[α]_ _A_ 0 _B_ 0 = ~~_√_~~ _[α]_  - _−_ _η∇W_ [�] 0 _B_ 0 _[⊤][B]_ [0]
_r_ _r_ _r_



where _L_ _[reg]_ represents the orthonormal regulation loss. This
approach maintains the benefits of pretrained features while
ensuring stable optimization through orthonormal constraints.
_2)_ _Gradient-driven_ _Init_ _Methods:_ As shown in Section II-A2, the optimization dynamics of LORA adapters are
closely tied to the corresponding gradients of the pretrained
weights. Motivated by this insight, multiple gradient-driven
methods are proposed to enhance performance.
**LORA-GA** [27] introduces a gradient-based initialization
strategy for low-rank adapters by effectively leveraging precomputed gradients. The central idea of LORA-GA lies in
its optimization objective, which explicitly minimizes the discrepancy between the weight updates at the initial training step
induced by LORA and those obtained through full fine-tuning
with an arbitrary scaling factor _ζ_ . Formally, this objective can
be expressed as the following minimization problem:




- _−_ _η∇W_ [�] 0 _B_ 0 _[⊤][B]_ [0]



According to Eq. (103), the optimal 2 _r_ -approximation of
the initial gradient descent step’s update direction can be
achieved when the second-order _η_ [2] term is negligible. This
approximation, however, imposes an inherent constraint on the
learning rate selection using LORA-GA.
Building upon these observations, LORA-ONE introduces
the following initialization:

_−∇W_ [�] 0 = _U∇W_ �0 _[S]_ _∇W_ [�] 0 _[V]_ _∇_ _[⊤]_ _W_ [�] 0 _[,]_ _S∇W_ - _[←]_ _[S]_ _∇W_ [�] _[/σ]_ [1] _[,]_ (104)



(103)

_−_ _ηA_ 0 _A_ _[⊤]_ 0 _[∇]_ _W_ [�] 0 + _η_ [2] _∇WB_ [�] 0 _[⊤][A]_ 0 _[⊤][∇]_ _W_ [�] 0� _._



arg min
_A_ 0 _,B_ 0



2
_P_ ( _A_ 0 _, B_ 0 _, ∇W_ �0) _−_ _ζ∇W_ [�] 0 (99)
��� ��� _F_ _[,]_



where the projection operator _P_ ( _A_ 0 _, B_ 0 _, ∇W_ [�] 0) _≡_
_A_ 0 _A_ _[⊤]_ 0 _[∇]_ _W_ [�] 0 + _∇W_ [�] 0 _B_ 0 _[⊤][B]_ [0] represents the approximate
gradient of _W_ as illustrated in Eq. (4). Under the assumption

[�]
of a single step of stochastic gradient descent (SGD) with a
learning rate _η_, the objective in Eq. (99) directly minimizes the
difference between the updates of LoRA and full fine-tuning
at the initial training step.


JOURNAL OF L [A] TEX CLASS FILES, VOL. 18, NO. 9, SEPTEMBER 2020 12



1
_A_ 0 = ~~_√_~~ _γ U∇W_ �0 [[:] _[,]_ [ :] _[ r]_ []] _[S]_ _∇_ [1] _[/]_ _W_ [�][2] 0 [[:] _[ r,]_ [ :] _[ r]_ []] _[,]_ (105)

1
_B_ 0 = ~~_√_~~ _γ S∇_ [1] _[/]_ _W_ [�][2] 0 [[:] _[ r,]_ [ :] _[ r]_ []] _[V]_ _∇_ _[⊤]_ _W_ [�] 0 [[:] _[ r,]_ [ :]] _[,]_ (106)


where _γ_ is a hyperparameter analogous to LORA-GA’s scaling factor and _σ_ 1 is the largest singular value of _−∇W_ [�] 0.
Remarkably, LoRA-One achieves recovery of the one-step
gradient updates for pretrained weights—with negligible error—while eliminating the need for explicit weight manipulation discussed in Section II-D1. **LORA-SB** [131] similarly
initializes _A_ 0 and _B_ 0 using the top- _r_ left and right singular
vectors respectively, while introducing _D_ _∈_ R _[r][×][r]_ initialized
with the corresponding singular values. During training, while
maintaining the same forward pass formulation as Eq. (97),
LORA-SB keeps _A_ 0 and _B_ 0 frozen and only updates _Dt_ .
**GORA** [62] observes that the compression form shown in
Eq. (3) is not the optimal solution given an initialized _A_ 0. The
best solution is given by:

_A_ _[†]_ 0 [= (] _[A]_ 0 _[⊤][A]_ [0][)] _[−]_ [1] _[A]_ 0 _[⊤][,]_ _A_ 0 _B_ 0 = _−A_ 0 _A_ _[†]_ 0 _[∇]_ _W_ [�] 0 _≈−∇W_ [�] 0 _,_
(107)
where _A_ _[†]_ is the Moore-Penrose inverse of the matrix _A_ .
Furthermore, GORA finds that the expected Frobenius norm
of _∇W_ [�] 0 is _[√]_ _mn_, while that of _AB_ is _[√]_ _rn_ under a zeromean unit-variance distribution. Following these observations,
GORA initializes the low-rank weights by:



specifically selected for their relevance to the model’s world
knowledge representation. Mathematically, after obtaining the
covariance matrix, CORDA initializes the corresponding lowrank weights using the minor components of a weighted
covariance matrix through the following transformation:

_A_ 0 = ( _C_ _[−]_ [1] _UCW_  - [)[:] _[,][ −][r]_ [:]] _[S]_ _C_ _[−]_ _W_ [�][1] _[/]_ [2][[] _[−][r]_ [:] _[,][ −][r]_ [:]] _[,]_ (112)

_B_ 0 = _SC_ _[−]_ _W_ [�][1] _[/]_ [2][[] _[−][r]_ [:] _[,][ −][r]_ [:]] _[V]_ _C_ _[⊤]_ _W_ [�][[] _[−][r]_ [:] _[,]_ [ :]] _[.]_ (113)


In _instruction-previewed adaptation_, the primary objective is
to maximize alignment with the downstream task, prioritizing
task-specific performance. For this purpose, CORDA computes
the covariance matrices using a subset of the training dataset
and initializes the low-rank weights as:

_A_ 0 = ( _C_ _[−]_ [1] _UCW_    - [)[:] _[,]_ [ :] _[ r]_ []] _[S]_ _C_ _[−]_ _W_ [�][1] _[/]_ [2][[:] _[ r,]_ [ :] _[ r]_ []] _[,]_ (114)

_B_ 0 = _SC_ _[−]_ _W_ [�][1] _[/]_ [2][[:] _[ r,]_ [ :] _[ r]_ []] _[V]_ _C_ _[⊤]_ _W_ [�][[:] _[ r,]_ [ :]] _[.]_ (115)


As demonstrated in Section II-D, LORA faces the challenge
of vanishing gradients during the initial training phases. To
mitigate this issue, Paischer et al. [64] proposed **EVA** ( _Ex-_
_plained_ _Variance_ _Adaptation_ ), which utilizes principal components derived from the activation covariance matrix _X_ _[⊤]_ _X_
to properly initialize the weights of the matrix _A_ . The primary
objective of EVA is to maximize the expected gradient signal
of the matrix _B_ during the initial training stages. Formally,
this objective can be expressed as:




   _A_ 0 _∼U_ _−_ ~~_√_~~ [1] _,_ + ~~_√_~~ [1]
_m_ _m_




_,_ _B_ 0 = _−_ _[γ][√][m]_



_A_ 0max _A_ _[⊤]_ 0 [=] _[I]_ [ E] - _∥∇B_ 0 _∥_ [2] _F_ - = _A_ 0max _A_ _[⊤]_ 0 [=] _[I]_ [ E] ���� _A⊤_ 0 _[∇]_ _W_ [�] ���2 _F_




_._ (116)



_α_
~~_√_~~ _A_ 0 _B_ 0 _≈−_ _[γα][√][rmn]_
_r_ _α_ ~~_[√]_~~ _rmn_



_α_ _A_ _[†]_ 0 _[∇]_ _W_ [�] 0 _,_ (108)



_W_ 0 _≈−γ∇W_ [�] 0 _,_ (109)
_α_ ~~_[√]_~~ _rmn_ _[∇]_ [�]



Consider the LORA forward pass in a simple linear model
where the input _x ∈_ R [1] _[×][m]_ and output _y_ ˆ _∈_ R [1] _[×][n]_ :


_y_ ˆ = _x_ ( _W_ [�] + _AB_ ) _,_ _∇B_ 0 = _A_ _[⊤]_ 0 _[x][⊤][∇][y,]_ [ˆ] (117)


where _∇y_ ˆ represents the gradient of the predicted label _y_ ˆ under
the loss function _L_ (ˆ _y, y_ ). The expected squared Frobenius
norm of the gradient of _B_ 0 can then be derived as:

_∥∇B_ 0 _∥_ [2] _F_ [= Tr(] _[∇][B]_ 0 _[⊤][∇][B]_ [0][) = Tr(] _[∇][y]_ [ˆ] _[∇][y]_ [ˆ] _[⊤][xA]_ [0] _[A]_ 0 _[⊤][x][⊤]_ [)]

= _∇y_ ˆ _∇y_ ˆ _[⊤]_ _·_ Tr( _A_ _[⊤]_ 0 _[x][⊤][xA]_ [0][)] _[.]_

        - ���
Scaler

(118)
EVA makes the key assumption that the gradient of _y_ ˆ
is statistically independent of the input (i.e., _∇y_ ˆ _⊥_ _x_ ),
the gradient _∇y_ ˆ depends solely on _W_ [�] since _A_ 0 _B_ 0 = 0.
Consequently, the expected covariance between the input and
the gradient of _y_ ˆ becomes:


E �( _x −_ E[ _x_ ]) _[⊤]_ ( _∇y_ ˆ _−_ E[ _∇y_ ˆ])� = **0** _m×n._ (119)


This leads to EVA’s fundamental conclusion that the expected initial gradient magnitude of _B_ 0 is directly proportional
to the trace of the activation matrix projected by _A_ 0:

E     - _∥∇B_ 0 _∥_ [2] _F_     - _∝_ Tr( _A_ _[⊤]_ 0 [E]     - _x_ _[⊤]_ _x_     - _A_ 0) _._ (120)


Therefore, the objective in Eq. 116 can be rewritten as:

max  - _∥∇B_ 0 _∥_ [2] _F_  - = max 0 [E]  - _x_ _[⊤]_ _x_  - _A_ 0) _._ (121)
_A_ 0 _A_ _[⊤]_ 0 [=] _[I]_ [ E] _A_ 0 _A_ _[⊤]_ 0 [=] _[I]_ [ Tr(] _[A][⊤]_



where _γ_ is a hyperparameter of GORA that controls the scaling
of initialization. With a proper _γ_, a lower initial loss and faster
convergence speed can be achieved by GORA.
_3)_ _Activation-aware_ _Init_ _Methods:_ Let _X_ _∈_ R _[bs][×][m]_ denote
the input activations of a pretrained weight matrix _W_ _∈_

[�]
R _[m][×][n]_, where _b_ is the batch size, _s_ is the padded sequence
length. The unnormalized covariance matrix _C_ = _X_ _[⊤]_ _X_
captures the second-order statistics of the inputs. To analyze
how _W_ interacts with these input statistics, CORDA performs

[�]
SVD on the matrix _CW_ [�] = _X_ _[⊤]_ _XW_ [�], which combines the
data distribution _C_ with the learned features _W_ . Formally, the

[�]
decomposition can be expressed as follows:


_C_ = _X_ _[⊤]_ _X,_ _CW_ [�] = _UCW_    - _[S]_ _CW_ [�] _[V]_ _C_ _[⊤]_ _W_ [�] _[,]_ (110)
_W_  - = _C_ _[−]_ [1] _CW_ [�] = ( _C_ _[−]_ [1] _UCW_  - [)] _[S]_ _CW_ [�] _[V]_ _C_ _[⊤]_ _W_ [�] _[.]_ (111)


This decomposition reveals task-relevant directions in the input
space that are amplified or suppressed by _W_ .
Leveraging this decomposition, **CORDA** [84] proposes two
activation-based initialization schemes, namely _knowledge-_
_preserved_ _adaptation_ and _instruction-previewed_ _adaptation_ .
The key principle behind _knowledge-preserved_ _adaptation_
is to retain the pretrained model’s world knowledge as much
as possible while adapting it to downstream tasks by altering
minor directions. To operationalize this concept, CORDA
employs the following methodology: First, it computes covariance matrices using question-answering datasets that are


JOURNAL OF L [A] TEX CLASS FILES, VOL. 18, NO. 9, SEPTEMBER 2020 13



(c) Expert (b) Router (a) Loss


















|𝐵#<br>&|𝐵|&$⋯𝐵 &%<br>&|
|---|---|---|
|𝐵&#|𝐴|𝐴|


















|𝐵#<br>#<br>𝐴#<br>#|Col2|𝐵|$<br>#⋯<br>$<br>#|𝐵%<br>#|Col6|
|---|---|---|---|---|---|
|𝐴##<br>𝐵#||𝐴<br>|𝐴<br>|𝐴#<br>|𝐴#<br>|





















Fig. 5. Illustration of mixture of experts Integration based LORA variants.


This goal is equivalent to maximizing the variance of the
down-projected activation _X_ 0 _A_ 0 and maximizing the explained variance in a rank- _r_ approximation of the activation
_X_ 0. The solution can be derived from the truncated SVD:

_C_ = _X_ _[⊤]_ _X_ = _UCSCVC_ _[⊤]_ (122)

_A_ 0 = _Uc_ [: _,_ : _r_ ] _SC_ _∈_ R _[m][×][r]_ _,_ _B_ 0 = **0** _r×n,_ (123)


where _UC_ contains the eigenvectors and _SC_ contains the
eigenvalues of _C_ . For computational efficiency, EVA computes
the covariance matrix _X_ _[⊤]_ _X_ using a subset of training data
and employs incremental SVD [132] with truncation [133] to
minimize memory and time overheads during initialization.
The final initialization of _A_ 0 follows Eqs. (122)–(123).


_E._ _Mixture-of-Experts_ _Integration_ _Based_ LORA _Variants_

By replacing standard LoRA layers with MoE modules
composed of multiple LoRA experts, Mixture-of-Experts integration based LORA variants aim to enhance model capacity
and adaptability. Formally, the behavior of these variants is
generally characterized by a routed combination of LORA
expert outputs. The adaptation form can be defined as:



where _N_ is the number of experts, I( _·_ ) is the indicator function
denoting whether expert _i_ is selected for token _x_, and the two
summation terms represent the actual fraction of tokens routed
to expert _i_ and the average predicted probability for expert _i_,
respectively.
Recent variants have introduced innovations across three
primary dimensions to this framework: modifications to the
training objective (Loss), enhancements to the expert selection
process (Router), and reconfigurations of the architectural
design (Structure).
_1)_ _Loss_ _Modification_ _Methods:_ While the standard regularization term _Lreg_ primarily focuses on load balancing to
ensure equitable expert usage, it remains agnostic to the actual
features learned by the experts. Consequently, this metricdriven constraint is insufficient for addressing the unique
semantic challenges arising during fine-tuning, such as the
tendency for experts to converge on identical representations
or the overwriting of general world knowledge. To overcome
these limitations, recent works have designed specialized auxiliary losses that go beyond simple routing statistics to actively
shape expert specialization and diversity.
A key challenge in MoE training is random routing, where
the gating network fails to develop strong preferences, causing
different experts to converge on similar feature representations.
This expert redundancy negates the capacity benefits of the
MoE architecture. To address this, **MOELORA** [85] incorporates a contrastive learning objective into the loss function.
The motivation is to force experts to learn distinct features
by maximizing the semantic distance between their outputs.
Specifically, it treats the outputs processed by the same expert
as positive pairs and those from different experts as negative
pairs. The expert contrastive loss _Lreg_ is defined as:

_Lreg_ = _−_   - log   - exp( _q · k_ + _/τ_ ) (127)

_k∈{k_ + _,k−}_ [exp(] _[q][ ·][ k/τ]_ [)] _[,]_


where _q_ is the query output, _k_ + represents outputs from the
same expert, _k−_ represents outputs from other experts, and _τ_ is
the temperature. This auxiliary loss encourages high diversity
among experts, ensuring that the expanded parameter space is
effectively utilized for distinct feature processing.
While MOELORA focuses on general expert diversity,
other approaches leverage loss functions to enforce specific
functional roles, particularly to mitigate ”catastrophic forgetting.” Standard fine-tuning often overwrites the model’s pretrained world knowledge while learning downstream tasks.
**LORAMOE** [86] addresses this by introducing a localized
balancing constraint to separate experts into two groups: those
preserving world knowledge and those adapting to new tasks.
It utilizes an importance matrix _Q_ and a coefficient matrix _I_
that rewards alignment between expert types and sample types:



∆ _W_ = _γr ·_



_N_

- _ωi_ ( _x_ ) _·_ ( _BiAi_ ) _,_ (124)


_i_ =1



where _x_ is an input vector (hidden state of a token for LLMs),
_N_ is the number of experts, and _ωi_ ( _x_ ) is the routing weight
for expert _i_ determined by a gating network _g_ ( _x_ ). Here, the
foundational router activates only the top _k_ experts based on
the gating scores:




   _gi_ ( _x_ ) if _i ∈_ TopK( _g_ ( _x_ ))

_ωi_ ( _x_ ) = (125)

0 otherwise



The optimization objective typically combines the primary
task loss _Ltask_ with a regularization loss _Lreg_ to regulate
expert behavior. In the standard setting, _Lreg_ typically serves
as a load-balancing term to ensure even expert utilization. For
a given batch of input tokens _B_, this regularization loss is
usually defined as the scaled dot-product between the expert
selection frequency and the average gating probability:



_In,m_ =




1 + _δ_ if Type _e_ ( _n_ ) = Type _s_ ( _m_ ) (128)
1 _−_ _δ_ otherwise




   
- _gi_ ( _x_ )


_x∈B_

(126)




1
_|B|_





I( _i ∈_ TopK( _g_ ( _x_ )))

_x∈B_








1

_·_

_|B|_




_·_



_,_



_Lreg_ = _N_



_N_



_i_ =1







The regularization loss is calculated based on the dispersion
of the weighted importance matrix _Z_ = _I_ _◦_ _Q_ :

_Lreg_ = _[σ]_ [2][(] _[Z]_ [)] (129)

_µ_ ( _Z_ ) _[.]_


JOURNAL OF L [A] TEX CLASS FILES, VOL. 18, NO. 9, SEPTEMBER 2020 14



By maximizing the variance of _Z_, LORAMOE effectively
disentangles task-specific adaptation from general knowledge
retention, thereby solving the forgetting problem through
guided expert specialization.
_2)_ _Router_ _Modification_ _Methods:_ The routing mechanism
determines how inputs are distributed among experts. Standard
approaches often rely on implicit, token-level routing, where
different tokens within the same sequence might be sent to
different experts based on latent features. This can lead to
fragmented context and interference between heterogeneous
tasks. To address these limitations, **MOA** [87] diverges from
the standard paradigm by adopting a sequence-level routing
strategy guided by explicit domain metadata. Instead of relying
on unsupervised token-wise learning, the model employs a
regularization loss to penalize deviations from ground-truth
domain labels. This supervision enforces precise, consistent
data-to-expert assignments across all layer-wise routers, effectively mitigating task interference by prioritizing the sequence’s domain identity over local token statistics.
Focusing on efficiency, **ADAMOLE** [88] challenges the
static allocation of experts in Top- _k_ methods. Motivated by
the observation that tokens vary in complexity, it introduces a
dynamic, context-sensitive routing strategy. Instead of a fixed
_k_, it employs an adaptive threshold _τ_ ( _x_ ) derived from the
input features. An expert is activated only if its gating score
exceeds this threshold:


_ωi_ ( _x_ ) = _gi_ ( _x_ ) _·_ I( _gi_ ( _x_ ) _> τ_ ( _x_ )) _,_ (130)

where _τ_ ( _x_ ) = _τ_ max _· σ_ ( _Wτ_ _x_ + _bτ_ ) _._ (131)


This mechanism allows the model to dynamically adjust the
number of active experts based on the specific requirements
of the input complexity.
_3)_ _Expert_ _Modification_ _Methods:_ Beyond loss functions
and routing, significant research focuses on structurally optimizing how LoRA experts are constructed, initialized, and
arranged within the network.
**MOLA** [89] is motivated by the understanding that different
Transformer layers process features at varying levels of abstraction. Consequently, a uniform number of experts across
all layers is suboptimal. MOLA structurally alters the MoE
configuration by varying the number of experts _Nl_ specific
to each layer _l_ . By adopting architectures such as Diamond
or Inverted-Triangle patterns for expert allocation, MOLA
optimizes expert redundancy where it is most needed.
Another structural challenge is bridging the performance
gap between LoRA-based methods and full fine-tuning.
**GOAT** [90] addresses this by structurally aligning the initialization of experts with the singular value decomposition (SVD)
of the pre-trained weights. Each LoRA expert is initialized
using disjoint segments of the singular vectors _U_ and _V_ :



In the realm of structural efficiency, **HYDRA-LORA** [91]
addresses the parameter redundancy inherent in standard MoE
designs where ( _Bi, Ai_ ) pairs are fully independent. Diverging
from the symmetric expert structure, it proposes an asymmetric
architecture consisting of a single shared _A_ and multiple
_B_ . The shared projection matrix _A_ captures general features
across all inputs, while the set of distinct matrices _{Bi}_ serves
as the experts. A dynamic router _g_ ( _x_ ) computes input-sensitive
weights to combine these heads, resulting in the update:







_y_ = _Wx_ + _s_

[�]




- _N_

 - _ωi_ ( _x_ ) _Bi_


_i_ =1



_Ax._ (133)



This design significantly reduces parameter count while maintaining the token-level adaptability of the router.
Conversely, **MOSLORA** [92] modifies the internal structure
of the LoRA module itself to introduce mixture capabilities
without an external router.


III. OVERVIEW OF LORAFACTORY


_A._ _Core_ _Implementations_ _of_ _LoRA_ _in_ _LoRAFactory_


LoRAFactory follows a modular inheritance hierarchy
with LinearWithLoRA as the base class, enabling efficient implementation of LORA variants through strategic
method overriding. The LinearWithLoRA class extends
torch.nn.Linear class and provides the foundations
of LoRA’s mechanism. The core forward computation of
LinearWithLoRA is detailed below:

_x_ out = _xW_ - [+] _[ x]_ [∆] _[W]_ [=][ linear][(] _[x]_ [in] _[,]_ [ �] _W_ _[⊤]_ ) (134)

+ _s ·_ linear�linear(dropout( _x_ in) _, A_ _[⊤]_ ) _, B_ _[⊤]_ [�] _,_


where linear and dropout are functions provided by
PyTorch. Key methods of LinearWithLoRA are:


_•_ forward: Orchestrates the forward pass as a linear layer.
Conditionally applies low-rank adaptations (LoRA)—
disabled either by the DisableLoRA context manager
or when LoRA weights are inaccessible.

_•_ _lora_forward: Computes the low-rank adaptation
as shown in the fused forward pass of the low-rank
adaptation part in Eq. (134).

_•_ init_lora_weights: Initializes the low-rank
weights.

_•_ compute_lora_weight: Computes the effective
LoRA weight ∆ _W_ .

A simple LoRAConfig data class is defined alongside,
covering the following key configurations:


_•_ in_features: int: The input dimension.

_•_ out_features: int: The output dimension.

_•_ bias: bool: Whether a bias term is needed.

_•_ lora_rank: int: The rank of the low-rank adapter.

_•_ lora_scaler: float: The scaling coefficient of the
low-rank adapter (defaultly used as _α_ ).

_•_ lora_dropout: float: The dropout rate of the input of the low-rank adapter.

_•_ weight_a_init_method: str: The name of the
initialization method for the matrix _A_ (e.g., kaiming,
representing the kaiming uniform distribution).




- 1
_i_ _Vi_ _[T]_ _[.]_ (132)
_s_ [Σ][1] _[/]_ [2]



_Bi_ =




- 1
_s_ _[U][i]_ [Σ] _i_ [1] _[/]_ [2] _,_ _Ai_ =



Combined with a theoretically derived scaling factor _s_, this
structural initialization ensures that the optimization trajectory
of the MoE-LoRA model closely mimics that of full-rank finetuning.


JOURNAL OF L [A] TEX CLASS FILES, VOL. 18, NO. 9, SEPTEMBER 2020 15




_•_ weight_b_init_method: str: The name of the
initialization method for the matrix _B_ .

_•_ run_lora_in_fp32: bool: Whether run low-rank
computation under the FP32 precision, while keeping the
pretrained weight with original precision.

_•_ quant: bool: Whether quantize the pretrained weight.

The class of QLORA extends LinearWithLoRA by
quantizing the layer’s pretrained weights to lower precision (e.g., NF4). This implementation is highly flexible: it returns the output of LinearWithLoRA when
LoRAConfig.quant is False; otherwise, it performs
computation by de-quantizing the quantized weights. Hence,
the LinearWithQLoRA is further inherited by classes of
LoRA variant methods for easy quantization.


_B._ _Implementations_ _of_ _LoRA_ _Variants_ _in_ _LoRAFactory_


Variants such as DORA cannot directly use the forward pass
of LinearWithLoRA; for example, DORA requires merging
the low-rank weights into pretrained weights and using the
weights with altered magnitudes for forward computation,
making the fused computation impossible. For example, the
forward pass of LinearWithDoRA can be expressed as:


_x_ out = linear( _xin,_ self._apply_dora() _[⊤]_ ) _,_ (135)


where self._apply_dora() follows Eq. (68).
Variants such as AURORA necessitate forward passes of
low-rank adaptation that differ from vanilla LORA. For example, as shown in Eq. (86), AURORA introduces a non-linear
function _fANL_ into the forward pass, the forward pass of
AURORA can be correspondingly expressed as:


_x_ ANL = self._ANL(linear(dropout( _xin_ ) _, A_ _[⊤]_ )) (136)

_x_ ∆ _W_ = _s ·_ linear( _x_ ANL _, B_ _[⊤]_ ) _,_ (137)


where self._ANL() is a method performing _fANL_ .
Variants such as PISSA, relying on pretrained weights to
initialize low-rank weights, are implemented by modifying the
init_lora_weights method. In contrast, variants such
as LORA-GA, which utilize gradients or activations for initialization, require deactivating the init_lora_weights
method and executing a variant-specific re-initialization function after computing and storing the gradients or activations.
Sharing-based variants share low-rank weights across modules; the low-rank weights of these variants cannot be directly initialized. For this reason, a variant-specific function
prepare_shared_lora_weights is required to identify
all sets of modules that share low-rank weights and initialize the corresponding shared weights. After all sharing sets
and shared weights are prepared, a variant-specific function
update_shared_weights_to_layer is required to distribute the shared weights.


_C._ _Working_ _Mechanism_ _of_ _LoRAFactory_


All LoRA-related hyperparameters within LoRAFactory are
parsed via an argument parser and stored in a namespace
variable, args. Following model initialization, both the model
and args are passed to the setup_lora function. This



function identifies all targeted modules in the model designated for adaptation, and invokes the switch_to_lora
function. The latter determines the targeted LoRA variant
for adaptation and replaces all specified linear modules in
the model with corresponding adaptation-class linear modules. Throughout this process, any exceptional cases are
automatically managed by these functions. LoRAFactory is
natively compatible with modern training strategies, including
DeepSpeed ZeRO 3. The model with adapted modules can
be trained using custom trainers, such as the Hugging Face
Transformers Trainer, or it may employ the toolkits provided
within the framework.


IV. EMPIRICAL EVALUATION USING LORAFACTORY


We present a systematic evaluation of 20 representative
LORA variants, which have been published in top-tier venues
such as NeurIPS, ICLR, and ICML, within a unified framework implemented in our codebase, **LoRAFactory** . Our
benchmark spans three domains: natural language understanding (NLU), natural language generation (NLG), and image
classification (IC). A key challenge in comparing LORA
variants lies in their sensitivity to hyperparameter choices.
While vanilla LORA is known to be highly sensitive to
the learning rate [99], [105], the sensitivity profiles of its
variants remain largely uncharacterized. To address this, we
conduct a comprehensive sensitivity analysis using Llama-3.18B-Base as a testbed, varying batch size, LORA dropout rate,
training data volume, and learning rate. Our results indicate
that learning rate sensitivity is the most salient differentiator,
with optimal ranges varying substantially across methods.
Consequently, we fix all hyperparameters except the learning
rate in the main experiments.
**Experimental** **Protocol.** For NLU, we fine-tune RoBERTaBase [30] on all tasks of the GLUE benchmark [31]. For
NLG, we evaluate mathematical reasoning and code generation
using Llama-3.1-8B-Base [37]. For IC, we train CLIP-ViTB/16 [134] on seven image classification datasets: StanfordCars [135], DTD [136], EuroSAT [137], GTSRB [138], RESISC45 [139], SUN397 [140], and SVHN [141]. Given space
limitations and consistent trends observed across domains, we
present visualized NLG results in the main text, while full
numerical results, including those of NLU and IC, are provided
in Appendix C.
**Default** **Configuration.** All experiments use rank _r_ = 8,
scaling coefficient _α_ = 16, and no LORA dropout (except
for variants like DENSELORA, where larger _r_ and _α_ are used
to maintain comparable trainable parameter counts; see Appendix). We employ the AdamW optimizer [10] with a cosine
learning rate schedule. All runs use a fixed random seed; we
observe that qualitative trends are robust to initialization.


_A._ _Computational_ _and_ _Memory_ _Overhead_ _Analysis_


Figure 8 compares the training time and peak GPU memory usage of LORA variants on Llama-3.1-8B-Base under a
defaultly identical hardware and software conditions (single
NVIDIA H200 GPU, BF16 precision, sequence length 1024,


JOURNAL OF L [A] TEX CLASS FILES, VOL. 18, NO. 9, SEPTEMBER 2020 16



(a) Training Data Volume


75

70

65

60


0
100k 200k 300k 395k


(c) LoRA Dropout Rate


75

70

65

60


0



(b) Batch Size


16 32 64 128 256


(d) Learning Rate


|Col1|Col2|Col3|Col4|
|---|---|---|---|
|||||
|||||
|||||



Fig. 6. Performance of LoRA and selected variants with altering distinct hyperparameters.



batch size 1, no activation checkpointing). Variants with negligible overhead (e.g., LORA+) are omitted for clarity. Vanilla
LORA achieves the lowest overhead (4h 42m, 30,067 MB),
serving as an efficiency baseline. DORA incurs the highest
memory cost (52,847 MB, +75%) due to explicit materialization of low-rank matrices during forward propagation,
a cost that can be mitigated via activation checkpointing.
LORAMOE is the slowest (36h 31m, +676.95%) owing to
its expert-routing mechanism. ADALORA and RANDLORA
exhibit increased runtime due to dynamic rank allocation or
full-rank computations. These results underscore a fundamental trade-off: architectural enhancements often come at the
expense of computational and memory efficiency ( **Finding 1** ).


_B._ _Hyperparameter_ _Sensitivity_ _Analysis_

We fine-tune Llama-3.1-8B-Base on MetaMathQA [142]
and evaluate on GSM8K [143], using a base configuration
of 100k samples, batch size 64, 0% dropout, and learning rate
5e-5. In each ablation, only one hyperparameter is varied.
_1)_ _Training_ _Data_ _Volume_ _and_ _Batch_ _Size:_ As shown in
Figure 6(a), performance generally improves with data volume. Vanilla LORA increases from 70.13 to 74.60 as data
grows from 100k to 395k. However, variants like LORAGA and MOSLORA saturate earlier. Performance remains
roughly stable across batch sizes 16–64 ( **Finding** **2** ), but
degrades significantly at larger sizes due to fewer optimization
steps. Vanilla LORA drops from 72.71 to 65.28 at batch size
256, whereas LORA-GA maintains robustness, attributable to
its gradient-magnitude-enhanced initialization scheme, which
reduces reliance on frequent updates. Notably, inter-method
performance gaps narrow with more update steps, with a
smaller batch size or larger training data volume, suggesting
that moderate-scale dataset volumes and update steps are more
discriminative for evaluation ( **Finding** **3** ).
_2)_ _LoRA_ _Dropout_ _Rate:_ Most variants are insensitive to
dropout ( **Finding** **4** ), but LORA-GA suffers severe degradation (from 72.02 to 51.33). This stems from a mismatch



between its initialization (computed without initialized lowrank weights) and training dynamics (with initialized low-rank
weights and dropout), which alters input statistics. To ensure
fair comparison, we disable dropout in all main experiments.
_3)_ _Learning_ _Rate:_ Figure 6(d) reveals pronounced and
method-specific learning rate sensitivity ( **Finding** **5** ), with
narrow and non-overlapping optimal ranges. This necessitates
extensive learning rate sweeps to find out the near-optimal
performance of each method we tested, as detailed next.


_C._ _Learning_ _Rate_ _Sweep_ _Results_ _on_ _NLG_

_1)_ _Task_ _Settings:_ We evaluate mathematical reasoning by
fine-tuning on 100k samples from MetaMathQA [142] and
testing on GSM8K [143]. For code generation, we train on
100k samples from CodeFeedback [144] and evaluate on
HumanEval [145]. To mitigate variance from HumanEval’s
small size (163 samples), we average over eight evaluation
runs. We sweep eight learning rates (1e-6 to 1e-3) while fixing
other settings with the default configurations.
_2)_ _Results_ _and_ _Discussion:_ As shown in Figure 7, performance typically rises with learning rate until an optimum,
beyond which it declines. Several variants (e.g., ADALORA)
converge slower than vanilla LORA, likely due to additional regularization, for example, orthogonality constraints in
ADALORA or coupling with pretrained weights (e.g., HIRA,
which dampens gradient signals.
Notably, many variants outperform vanilla LORA at low
learning rates. On GSM8K at 1e-6, LORA-GA (64.06) surpasses vanilla LORA (52.82) by over 11 points. However, this
advantage vanishes at higher rates: the best variant (LORA+,
75.59 at 1e-4) exceeds LORA (75.51 at 1e-4) by only
0.08 points. On HumanEval, only RANDLORA and RASA
marginally surpass LORA. At 1e-6, most methods fail to
achieve meaningful code generation performance, indicating
that stronger update signals are essential for this task.
Surprisingly, LORA exhibits higher performance ceilings
than its most evaluated variants on both tasks, a trend also


JOURNAL OF L [A] TEX CLASS FILES, VOL. 18, NO. 9, SEPTEMBER 2020 17




|Col1|Col2|Col3|Col4|Col5|Col6|Col7|Col8|Col9|
|---|---|---|---|---|---|---|---|---|
|||||||LoRA<br>RaSA<br>DenseLoRA<br>|ReLoR<br>AdaLo<br>MeLoR<br>|A<br>RA<br>A|


|Col1|Col2|Col3|Col4|Col5|Col6|Col7|Col8|Col9|
|---|---|---|---|---|---|---|---|---|
|||||||LoRA<br>|GOAT<br>||



40



70


60


70


60


50


50


40


30


20


10


40


20





(d) Mixture-of-Experts-GSM8k









70


60


70


60


50


50


40


30





20


|Col1|Col2|Col3|Col4|Col5|Col6|Col7|Col8|Col9|
|---|---|---|---|---|---|---|---|---|
|||||||LoRA<br>RaSA<br>|HiRA<br>AdaLo<br>|RA<br>|



0
1e-6 1e-5 2e-5 5e-5 1e-4 2e-4 5e-4 1e-3







1e-6 1e-5 2e-5 5e-5 1e-4 2e-4 5e-4 1e-3



Fig. 7. Performance comparison of LoRA and its variants on GSM8K (accuracy) and HumanEval (pass@1) across a range of learning rates.



40h


15h


12h


10h


8h


6h




















|Col1|Col2|Col3|Col4|RandLoR|A|
|---|---|---|---|---|---|
||||~~LoKr~~<br>LoRAMoE||LoHa|
||DoRA|Aurora|RandLoRA(U=1024)|||
|||~~AdaLoRA~~||||
||||DoRA<br>DeLoRA<br>HiRA|||
||LoRA|RaSA<br><br>MELoRA|DenseLoRA<br>Loran|~~Params (Mi~~<br>21<br>22|~~ lions)~~<br>.6<br>.2|
|||LoRA<br>MoSLoRA||22<br>23|.8<br>.4|



20GB 30GB 40GB 60GB 90GB


Fig. 8. Computational and memory overhead of LORA variants. _†_ dentes
with activation checkpoint, and _U_ is a hyperparameter of RANDLORA.


observed in NLU and IC experiments ( **Key** **Finding** ). This
phenomenon arises from the _small-gradient_ _issue_ in vanilla
LORA combined with improper hyperparameter configurations such as small learning rates or scaling factor, limited
update steps, its parameter updates are not sufficient, hindering
optimization. In contrast, variants like LORA-GA produce
initial gradients _∼_ 100 _×_ larger, enabling effective learning in
certain suboptimal hyperparameter regimes. However, when
a proper set of hyperparameter configurations is adopted,



compensating for vanilla LORA’s inherent small gradients,
thereby neutralizing the relative advantage of these variants.
Our findings suggest that prior studies, which often evaluate
the performance using a fixed hyperparameter configuration,
may have underestimated the performance of the most important baseline: LORA. Performance gains frequently disappear
under comprehensive hyperparameter sweeps, underscoring
the necessity of broad hyperparameter exploration for fair and
robust evaluation of LORA methods.


V. CONCLUSION

In this work, we conduct a unified study of LORA and
its variants. We organize all methods into four categories,
establishing a fine-grained and structured taxonomy based on
their principal operational axes. Further, we unify them under
a review framework of low-rank update dynamics, illuminating
their connections. Empirically, we introduce LoRAFactory, a
modular and extensible codebase that implements 50+ LORA
variants. Through extensive large-scale experiments, several
key findings emerge. These results underscore the robust
performance of the fundamental baseline, LORA, and emphasize the critical role of hyperparameter tuning, specifically
the calibration of the learning rate, in ensuring equitable
benchmarking within LORA research. By releasing all code
and configurations, we hope this work provides a foundation
for more rigorous and transparent evaluation.


JOURNAL OF L [A] TEX CLASS FILES, VOL. 18, NO. 9, SEPTEMBER 2020 18



REFERENCES


[1] Z. Liang, Y. Xu, Y. Hong, P. Shang, Q. Wang, Q. Fu, and K. Liu, “A
survey of multimodel large language models,” in _Proceedings_ _of_ _the_
_3rd_ _International_ _Conference_ _on_ _Computer,_ _Artificial_ _Intelligence_ _and_
_Control_ _Engineering_, 2024, pp. 405–409.

[2] Z. Li, X. Wu, H. Du, F. Liu, H. Nghiem, and G. Shi, “A survey of
state of the art large vision language models: Alignment, benchmark,
evaluations and challenges,” _arXiv_ _preprint_ _arXiv:2501.02189_, 2025.

[3] W. X. Zhao, K. Zhou, J. Li, T. Tang, X. Wang, Y. Hou, Y. Min,
B. Zhang, J. Zhang, Z. Dong _et_ _al._, “A survey of large language
models,” _arXiv_ _preprint_ _arXiv:2303.18223_, vol. 1, no. 2, 2023.

[4] P. Gao, J. Han, R. Zhang, Z. Lin, S. Geng, A. Zhou, W. Zhang, P. Lu,
C. He, X. Yue _et_ _al._, “Llama-adapter v2: Parameter-efficient visual
instruction model,” _arXiv_ _preprint_ _arXiv:2304.15010_, 2023.

[5] X. Liu, K. Ji, Y. Fu, W. L. Tam, Z. Du, Z. Yang, and J. Tang, “P-tuning
v2: Prompt tuning can be comparable to fine-tuning universally across
scales and tasks,” _arXiv_ _preprint_ _arXiv:2110.07602_, 2021.

[6] E. B. Zaken, S. Ravfogel, and Y. Goldberg, “Bitfit: Simple parameterefficient fine-tuning for transformer-based masked language-models,”
_arXiv_ _preprint_ _arXiv:2106.10199_, 2021.

[7] R. Karimi Mahabadi, J. Henderson, and S. Ruder, “Compacter: Efficient low-rank hypercomplex adapter layers,” _Advances_ _in_ _neural_
_information_ _processing_ _systems_, vol. 34, pp. 1022–1035, 2021.

[8] E. J. Hu, Y. Shen, P. Wallis, Z. Allen-Zhu, Y. Li, S. Wang, L. Wang,
W. Chen _et al._, “Lora: Low-rank adaptation of large language models.”
_ICLR_, vol. 1, no. 2, p. 3, 2022.

[9] D. P. Kingma and J. Ba, “Adam: A method for stochastic optimization,”
_arXiv_ _preprint_ _arXiv:1412.6980_, 2014.

[10] I. Loshchilov and F. Hutter, “Decoupled weight decay regularization,”
_arXiv_ _preprint_ _arXiv:1711.05101_, 2017.

[11] S. Rajbhandari, J. Rasley, O. Ruwase, and Y. He, “Zero: Memory
optimizations toward training trillion parameter models,” in _SC20:_ _In-_
_ternational Conference for High Performance Computing, Networking,_
_Storage_ _and_ _Analysis_ . IEEE, 2020, pp. 1–16.

[12] Y. Zhao, A. Gu, R. Varma, L. Luo, C.-C. Huang, M. Xu, L. Wright,
H. Shojanazeri _et_ _al._, “Pytorch fsdp: experiences on scaling fully
sharded data parallel,” _arXiv_ _preprint_ _arXiv:2304.11277_, 2023.

[13] W. Su, Y. Tang, Q. Ai, J. Yan, C. Wang, H. Wang, Z. Ye, Y. Zhou, and
Y. Liu, “Parametric retrieval augmented generation,” in _Proceedings_
_of_ _the_ _48th_ _International_ _ACM_ _SIGIR_ _Conference_ _on_ _Research_ _and_
_Development_ _in_ _Information_ _Retrieval_, 2025, pp. 1240–1250.

[14] A. Zweiger, J. Pari, H. Guo, E. Aky¨urek, Y. Kim, and P. Agrawal, “Selfadapting language models,” _arXiv_ _preprint_ _arXiv:2506.10943_, 2025.

[15] Y. Wei, Y. Miao, D. Zhou, and D. Hu, “Moka: Multimodal low-rank
adaptation for mllms,” _arXiv_ _preprint_ _arXiv:2506.05191_, 2025.

[16] H. Wang, Y. Ye, B. Li, Y. Nie, J. Lu, J. Tang, Y. Wang, and C. Huang,
“Vision as lora,” _arXiv_ _preprint_ _arXiv:2503.20680_, 2025.

[17] S. Babakniya, A. R. Elkordy, Y. H. Ezzeldin, Q. Liu, K.-B. Song, M. ElKhamy, and S. Avestimehr, “Slora: Federated parameter efficient finetuning of language models,” _arXiv_ _preprint_ _arXiv:2308.06522_, 2023.

[18] J. Qi, Z. Luan, S. Huang, C. Fung, H. Yang, and D. Qian, “Fdlora:
Personalized federated learning of large language model via dual lora
tuning,” _arXiv_ _preprint_ _arXiv:2406.07925_, 2024.

[19] T. Dettmers, A. Pagnoni, A. Holtzman, and L. Zettlemoyer, “Qlora:
Efficient finetuning of quantized llms,” _Advances in neural information_
_processing_ _systems_, vol. 36, pp. 10 088–10 115, 2023.

[20] Y. Li, Y. Yu, C. Liang, P. He, N. Karampatziakis, W. Chen, and
T. Zhao, “Loftq: Lora-fine-tuning-aware quantization for large language
models,” _arXiv_ _preprint_ _arXiv:2310.08659_, 2023.

[21] V. Lialin, N. Shivagunde, S. Muckatira, and A. Rumshisky, “Relora:
High-rank training through low-rank updates,” _URL_ _https://arxiv._
_org/abs/2307.05695_, 2023.

[22] Q. Zhang, M. Chen, A. Bukharin, N. Karampatziakis, P. He _et_ _al._,
“Adalora: Adaptive budget allocation for parameter-efficient finetuning,” _arXiv_ _preprint_ _arXiv:2303.10512_, 2023.

[23] P. Albert, F. Z. Zhang, H. Saratchandran, C. Rodriguez-Opazo, A. v. d.
Hengel, and E. Abbasnejad, “Randlora: Full-rank parameter-efficient
fine-tuning of large models,” _arXiv_ _preprint_ _arXiv:2502.00987_, 2025.

[24] S. Hayou, N. Ghosh, and B. Yu, “Lora+: Efficient low rank adaptation
of large models,” _arXiv_ _preprint_ _arXiv:2402.12354_, 2024.

[25] Z. Wang, J. Liang, R. He, Z. Wang, and T. Tan, “Lora-pro: Are low-rank
adapters properly optimized?” in _International Conference on Learning_
_Representations_, 2025.




[26] F. Meng, Z. Wang, and M. Zhang, “Pissa: Principal singular values and
singular vectors adaptation of large language models,” in _Advances_ _in_
_Neural_ _Information_ _Processing_ _Systems_, vol. 37, 2024, pp. 121 038–
121 072.

[27] S. Wang, L. Yu, and J. Li, “Lora-ga: Low-rank adaptation with gradient
approximation,” _Advances_ _in_ _Neural_ _Information_ _Processing_ _Systems_,
vol. 37, pp. 54 905–54 931, 2024.

[28] W. Feng, C. Hao, Y. Zhang, Y. Han, and H. Wang, “Mixture-ofloras: An efficient multitask tuning method for large language models,”
in _Proceedings_ _of_ _the_ _2024_ _Joint_ _International_ _Conference_ _on_ _Com-_
_putational_ _Linguistics,_ _Language_ _Resources_ _and_ _Evaluation_ _(LREC-_
_COLING_ _2024)_, 2024, pp. 11 371–11 380.

[29] S. Mangrulkar, S. Gugger, L. Debut, Y. Belkada, S. Paul, B. Bossan,
and M. Tietz, “PEFT: State-of-the-art parameter-efficient fine-tuning
methods,” [https://github.com/huggingface/peft,](https://github.com/huggingface/peft) 2022.

[30] Y. Liu, M. Ott, N. Goyal, J. Du, M. Joshi, D. Chen, O. Levy, M. Lewis,
L. Zettlemoyer, and V. Stoyanov, “Roberta: A robustly optimized bert
pretraining approach,” _arXiv_ _preprint_ _arXiv:1907.11692_, 2019.

[31] A. Wang, A. Singh, J. Michael, F. Hill, O. Levy, and S. R. Bowman,
“Glue: A multi-task benchmark and analysis platform for natural
language understanding,” _arXiv_ _preprint_ _arXiv:1804.07461_, 2018.

[32] A. Radford, J. Wu, R. Child, D. Luan, D. Amodei, I. Sutskever _et_ _al._,
“Language models are unsupervised multitask learners,” _OpenAI_ _blog_,
vol. 1, no. 8, p. 9, 2019.

[33] J. Novikova, O. Duˇsek, and V. Rieser, “The e2e dataset: New challenges
for end-to-end generation,” _arXiv_ _preprint_ _arXiv:1706.09254_, 2017.

[34] T. Brown, B. Mann, N. Ryder, M. Subbiah, J. D. Kaplan, P. Dhariwal,
A. Neelakantan, P. Shyam, G. Sastry, A. Askell _et al._, “Language models are few-shot learners,” _Advances_ _in_ _neural_ _information_ _processing_
_systems_, vol. 33, pp. 1877–1901, 2020.

[35] V. Zhong, C. Xiong, and R. Socher, “Seq2sql: Generating structured
queries from natural language using reinforcement learning,” _arXiv_
_preprint_ _arXiv:1709.00103_, 2017.

[36] B. Gliwa, I. Mochol, M. Biesek, and A. Wawer, “Samsum corpus:
A human-annotated dialogue dataset for abstractive summarization,”
_arXiv_ _preprint_ _arXiv:1911.12237_, 2019.

[37] A. Dubey, A. Jauhri, A. Pandey, A. Kadian, A. Al-Dahle, A. Letman,
A. Mathur, A. Schelten, A. Yang, A. Fan _et_ _al._, “The llama 3 herd of
models,” _arXiv_ _e-prints_, pp. arXiv–2407, 2024.

[38] A. Yang, A. Li, B. Yang, B. Zhang, B. Hui, B. Zheng, B. Yu, C. Gao,
C. Huang, C. Lv _et_ _al._, “Qwen3 technical report,” _arXiv_ _preprint_
_arXiv:2505.09388_, 2025.

[39] X. Meng, D. Dai, W. Luo, Z. Yang, S. Wu, X. Wang, P. Wang, Q. Dong,
L. Chen, and Z. Sui, “Periodiclora: Breaking the low-rank bottleneck
in lora optimization,” _arXiv_ _preprint_ _arXiv:2402.16141_, 2024.

[40] W. Xia, C. Qin, and E. Hazan, “Chain of lora: Efficient finetuning of language models via residual learning,” _arXiv_ _preprint_
_arXiv:2401.04151_, 2024.

[41] Y. Zhang, H. Zhu, A. Liu, H. Yu, P. Koniusz, and I. King, “Less is
more: Extreme gradient boost rank-1 adaption for efficient finetuning
of llms,” _arXiv_ _preprint_ _arXiv:2410.19694_, 2024.

[42] P. Ren, C. Shi, S. Wu, M. Zhang, Z. Ren, M. de Rijke, Z. Chen,
and J. Pei, “Melora: Mini-ensemble low-rank adapters for parameterefficient fine-tuning,” _arXiv_ _preprint_ _arXiv:2402.17263_, 2024.

[43] N. Hyeon-Woo, M. Ye-Bin, and T.-H. Oh, “Fedpara: Low-rank
hadamard product for communication-efficient federated learning,”
_arXiv_ _preprint_ _arXiv:2108.06098_, 2021.

[44] S.-Y. Yeh, Y.-G. Hsieh, Z. Gao, B. B. Yang, G. Oh, and Y. Gong,
“Navigating text-to-image customization: From lycoris fine-tuning to
model evaluation,” in _The_ _Twelfth_ _International_ _Conference_ _on_ _Learn-_
_ing_ _Representations_, 2023.

[45] Q. Huang, T. Ko, Z. Zhuang, L. Tang, and Y. Zhang, “Hira: Parameterefficient hadamard high-rank adaptation for large language models,”
_Advancing Adaptation Techniques for Personalised Dialogue and Con-_
_versational_ _AI_, p. 124, 2024.

[46] T. Jiang, S. Huang, S. Luo, Z. Zhang, H. Huang, F. Wei _et_ _al._, “Mora:
High-rank updating for parameter-efficient fine-tuning,” _arXiv_ _preprint_
_arXiv:2405.12130_, 2024.

[47] Y. Song, J. Zhao, I. G. Harris, and S. A. Jyothi, “Sharelora: Parameter
efficient and robust large language model fine-tuning via shared lowrank adaptation,” _arXiv_ _preprint_ _arXiv:2406.10785_, 2024.

[48] D. J. Kopiczko, T. Blankevoort, and Y. M. Asano, “Vera: Vector-based
random matrix adaptation,” _arXiv_ _preprint_ _arXiv:2310.11454_, 2023.

[49] Z. He, Z. Tu, X. Wang, X. Chen, Z. Wang, J. Xu, T. Liang, W. Jiao,
Z. Zhang, and R. Wang, “Rasa: Rank-sharing low-rank adaptation,”
_arXiv_ _preprint_ _arXiv:2503.12576_, 2025.


JOURNAL OF L [A] TEX CLASS FILES, VOL. 18, NO. 9, SEPTEMBER 2020 19




[50] L. Mu, X. Wang, L. Ni, Y. Li, Z. Wu, P. Jin, and Y. Zhang, “Denselora:
Dense low-rank adaptation of large language models,” _arXiv_ _preprint_
_arXiv:2505.23808_, 2025.

[51] S. Wang, B. Xue, J. Ye, J. Jiang, L. Chen, L. Kong, and C. Wu,
“Prolora: Partial rotation empowers more parameter-efficient lora,”
_arXiv_ _preprint_ _arXiv:2402.16902_, 2024.

[52] Y. Zhou, R. Li, C. Zhou, F. Yang, and A. Pan, “Bslora: Enhancing the
parameter efficiency of lora with intra-layer and inter-layer sharing,”
in _Forty-second_ _International_ _Conference_ _on_ _Machine_ _Learning_ .

[53] A. Renduchintala, T. Konuk, and O. Kuchaiev, “Tied-lora: Enhancing parameter efficiency of lora with weight tying,” _arXiv_ _preprint_
_arXiv:2311.09578_, 2023.

[54] Y. Li, S. Han, and S. Ji, “Vb-lora: Extreme parameter efficient finetuning with vector banks,” _Advances in Neural Information Processing_
_Systems_, vol. 37, pp. 16 724–16 751, 2024.

[55] M. Li, P. Ye, J. Ye, H. He, and T. Chen, “E²lora: Efficient and
effective low-rank adaptation with entropy-guided adaptive sharing,”
in _International_ _Conference_ _on_ _Learning_ _Representations_, 2026.

[56] Y. Hu, Y. Xie, T. Wang, M. Chen, and Z. Pan, “Structure-aware
low-rank adaptation for parameter-efficient fine-tuning,” _Mathematics_,
vol. 11, no. 20, p. 4317, 2023.

[57] N. Ding, X. Lv, Q. Wang, Y. Chen, B. Zhou, Z. Liu, and M. Sun,
“Sparse low-rank adaptation of pre-trained language models,” _arXiv_
_preprint_ _arXiv:2311.11696_, 2023.

[58] R. Zhang, R. Qiang, S. A. Somayajula, and P. Xie, “Autolora: Automatically tuning matrix ranks in low-rank adaptation based on meta
learning,” _arXiv_ _preprint_ _arXiv:2403.09113_, 2024.

[59] F. Zhang, L. Li, J. Chen, Z. Jiang, B. Wang, and Y. Qian, “Increlora:
Incremental parameter allocation method for parameter-efficient finetuning,” _arXiv_ _preprint_ _arXiv:2308.12043_, 2023.

[60] Z. Liu, J. Lyn, W. Zhu, X. Tian, and Y. Graham, “Alora: Allocating lowrank adaptation for fine-tuning large language models,” _arXiv_ _preprint_
_arXiv:2403.16187_, 2024.

[61] R. Qiang, R. Zhang, and P. Xie, “Bilora: A bi-level optimization
framework for overfitting-resilient low-rank adaptation of large pretrained models,” _arXiv_ _preprint_ _arXiv:2403.13037_, 2024.

[62] H. He, P. Ye, Y. Ren, Y. Yuan, L. Zhou, S. Ju, and L. Chen, “Gora:
Gradient-driven adaptive low rank adaptation,” in _The_ _Thirty-ninth_
_Annual_ _Conference_ _on_ _Neural_ _Information_ _Processing_ _Systems_, 2025.

[63] J. Ye, H. He, M. Li, F. Han, T. Chen, and P. Ye, “Gradient intrinsic
dimensionality alignment: Narrowing the gap between low-rank adaptation and full fine-tuning,” in _International_ _Conference_ _on_ _Learning_
_Representations_, 2026.

[64] F. Paischer, L. Hauzenberger, T. Schmied, B. Alkin, M. P. Deisenroth,
and S. Hochreiter, “Parameter efficient fine-tuning via explained variance adaptation,” _arXiv_ _preprint_ _arXiv:2410.07170_, 2024.

[65] D. Kalajdzievski, “A rank stabilization scaling factor for fine-tuning
with lora,” _arXiv_ _preprint_ _arXiv:2312.03732_, 2023.

[66] F. Zhang and M. Pilanci, “Riemannian preconditioned lora for finetuning foundation models,” _arXiv_ _preprint_ _arXiv:2402.02347_, 2024.

[67] S.-Y. Liu, C.-Y. Wang, H. Yin, P. Molchanov, Y.-C. F. Wang, K.-T.
Cheng, and M.-H. Chen, “Dora: Weight-decomposed low-rank adaptation,” in _Forty-first_ _International_ _Conference_ _on_ _Machine_ _Learning_,
2024.

[68] M. Bini, L. Girrbach, and Z. Akata, “Delora: Decoupling angles and
strength in low-rank adaptation,” _arXiv_ _preprint_ _arXiv:2503.18225_,
2025.

[69] J. Han, S. Zhang, and K. Zhang, “Dual decomposition of weights and
singular value low rank adaptation,” _arXiv_ _preprint_ _arXiv:2505.14367_,
2025.

[70] Y. Hao, Y. Cao, and L. Mou, “Flora: Low-rank adapters are secretly
gradient compressors,” _arXiv_ _preprint_ _arXiv:2402.03293_, 2024.

[71] C. Si, X. Wang, X. Yang, Z. Xu, Q. Li, J. Dai, Y. Qiao, X. Yang, and
W. Shen, “Flora: Low-rank core space for n-dimension,” _arXiv preprint_
_arXiv:2405.14739_, vol. 10, 2024.

[72] H. Dong, W. Zhu, G. Song, and L. Wang, “Aurora: Breaking lowrank bottleneck of lora with nonlinear mapping,” _arXiv_ _preprint_
_arXiv:2505.18738_, 2025.

[73] Y. Ji, H. Saratchandran, C. Gordon, Z. Zhang, and S. Lucey, “Efficient learning with sine-activated low-rank matrices,” _arXiv_ _preprint_
_arXiv:2403.19243_, 2024.

[74] Y. Li, L. Song, and H. Hou, “Loran: Improved low-rank adaptation
by a non-linear transformation,” in _Findings_ _of_ _the_ _Association_ _for_
_Computational_ _Linguistics:_ _EMNLP_ _2024_, 2024, pp. 3134–3143.

[75] J. Liu, T. Koike-Akino, P. Wang, M. Brand, K. Parsons, and Y. Wang,
“Loda: Low-dimensional adaptation of large language models,” in



_Enhancing_ _LLM_ _Performance:_ _Efficacy,_ _Fine-Tuning,_ _and_ _Inference_
_Techniques_ . Springer, 2025, pp. 67–81.

[76] S. Li, X. Luo, X. Tang, H. Wang, H. Chen, Y. Li, R. Li _et al._, “Beyond
zero initialization: Investigating the impact of non-zero initialization on
lora fine-tuning dynamics,” in _Forty-second_ _International_ _Conference_
_on_ _Machine_ _Learning_ .

[77] S. Hayou, N. Ghosh, and B. Yu, “The impact of initialization on
lora finetuning dynamics,” _Advances in Neural Information Processing_
_Systems_, vol. 37, pp. 117 015–117 040, 2024.

[78] H. Wang, Y. Li, S. Wang _et_ _al._, “Milora: Harnessing minor singular
components for parameter-efficient llm finetuning,” in _Proceedings_
_of_ _the_ _2025_ _Conference_ _of_ _the_ _Nations_ _of_ _the_ _Americas_ _Chapter_
_of_ _the_ _Association_ _for_ _Computational_ _Linguistics:_ _Human_ _Language_
_Technologies_ _(Volume_ _1:_ _Long_ _Papers)_, 2025, pp. 4823–4836.

[79] C. Lin, L. Li, D. Li, J. Zou, W. Xue, and Y. Guo, “Nora: Nested lowrank adaptation for efficient fine-tuning large models,” _arXiv_ _preprint_
_arXiv:2408.10280_, 2024.

[80] C. Guo, Y. Wu, and Y. Chang, “Nlora: Nystr _\_ ” om-initiated
low-rank adaptation for large language models,” _arXiv_ _preprint_
_arXiv:2502.14482_, 2025.

[81] Y. Cao and Z. Song, “Sorsa: Singular values and orthonormal regularized singular vectors adaptation of large language models,” _arXiv_
_preprint_ _arXiv:2409.00055_, 2024.

[82] Y. Zhang, F. Liu, and Y. Chen, “Lora-one: One-step full gradient could
suffice for fine-tuning large language models, provably and efficiently,”
_arXiv_ _preprint_ _arXiv:2502.01235_, 2025.

[83] C. Si, Z. Shi, S. Zhang, X. Yang, H. Pfister, and W. Shen, “Taskspecific directions: Definition, exploration, and utilization in parameter
efficient fine-tuning,” _arXiv_ _preprint_ _arXiv:2409.01035_, 2024.

[84] Y. Yang, X. Li, Z. Zhou, S. Song, J. Wu _et al._, “Corda: Context-oriented
decomposition adaptation of large language models for task-aware
parameter-efficient fine-tuning,” in _Advances_ _in_ _Neural_ _Information_
_Processing_ _Systems_, vol. 37, 2024, pp. 71 768–71 791.

[85] T. Luo, J. Lei, F. Lei, W. Liu, S. He, J. Zhao, and K. Liu,
“Moelora: Contrastive learning guided mixture of experts on parameterefficient fine-tuning for large language models,” _arXiv_ _preprint_
_arXiv:2402.12851_, 2024.

[86] S. Dou, E. Zhou, Y. Liu, S. Gao, J. Zhao, W. Shen, Y. Zhou, Z. Xi,
X. Wang, X. Fan _et_ _al._, “Loramoe: Alleviate world knowledge forgetting in large language models via moe-style plugin,” _arXiv_ _preprint_
_arXiv:2312.09979_, 2023.

[87] W. Feng, C. Hao, Y. Zhang, Y. Han, and H. Wang, “Mixture-of-loras:
An efficient multitask tuning for large language models,” _arXiv preprint_
_arXiv:2403.03432_, 2024.

[88] Z. Liu and J. Luo, “Adamole: Fine-tuning large language models
with adaptive mixture of low-rank adaptation experts,” _arXiv_ _preprint_
_arXiv:2405.00361_, 2024.

[89] C. Gao, K. Chen, J. Rao, B. Sun, R. Liu, D. Peng, Y. Zhang, X. Guo,
J. Yang, and V. Subrahmanian, “Higher layers need more lora experts,”
_arXiv_ _preprint_ _arXiv:2402.08562_, 2024.

[90] C. Fan, Z. Lu, S. Liu, C. Gu, X. Qu, W. Wei, and Y. Cheng, “Make lora
great again: Boosting lora with adaptive singular values and mixtureof-experts optimization alignment,” _arXiv_ _preprint_ _arXiv:2502.16894_,
2025.

[91] C. Tian, Z. Shi, Z. Guo, L. Li, and C.-Z. Xu, “Hydralora: An
asymmetric lora architecture for efficient fine-tuning,” _Advances_ _in_
_Neural Information Processing Systems_, vol. 37, pp. 9565–9584, 2024.

[92] T. Wu, J. Wang, Z. Zhao, and N. Wong, “Mixture-of-subspaces in lowrank adaptation,” _arXiv_ _preprint_ _arXiv:2406.11909_, 2024.

[93] Y. Wang, Y. Lin, X. Zeng, and G. Zhang, “Multilora: Democratizing
lora for better multi-task learning,” _arXiv_ _preprint_ _arXiv:2311.11501_,
2023.

[94] Y. Zhu, N. Wichers, C.-C. Lin, X. Wang, T. Chen, L. Shu, H. Lu, C. Liu,
L. Luo, J. Chen _et_ _al._, “Sira: Sparse mixture of low rank adaptation,”
_arXiv_ _preprint_ _arXiv:2311.09179_, 2023.

[95] A. Agiza, M. Neseem, and S. Reda, “Mtlora: Low-rank adaptation
approach for efficient multi-task learning,” in _Proceedings_ _of_ _the_
_IEEE/CVF_ _conference_ _on_ _computer_ _vision_ _and_ _pattern_ _recognition_,
2024, pp. 16 196–16 205.

[96] Y. Yang, P.-T. Jiang, Q. Hou, H. Zhang, J. Chen, and B. Li, “Multi-task
dense prediction via mixture of low-rank experts,” in _Proceedings_ _of_
_the_ _IEEE/CVF_ _conference_ _on_ _computer_ _vision_ _and_ _pattern_ _recognition_,
2024, pp. 27 927–27 937.

[97] S. Chen, Z. Jie, and L. Ma, “Llava-mole: Sparse mixture of lora experts
for mitigating data conflicts in instruction finetuning mllms,” _arXiv_
_preprint_ _arXiv:2401.16160_, 2024.


JOURNAL OF L [A] TEX CLASS FILES, VOL. 18, NO. 9, SEPTEMBER 2020 20




[98] C. Li, H. Farkhoor, R. Liu, and J. Yosinski, “Measuring the intrinsic
dimension of objective landscapes,” _arXiv_ _preprint_ _arXiv:1804.08838_,
2018.

[99] D. Biderman, J. Portes, J. J. G. Ortiz, M. Paul, P. Greengard, C. Jennings, D. King, S. Havens, V. Chiley, J. Frankle _et_ _al._, “Lora learns
less and forgets less,” _arXiv_ _preprint_ _arXiv:2405.09673_, 2024.

[100] R. Shuttleworth, J. Andreas, A. Torralba, and P. Sharma, “Lora
vs full fine-tuning: An illusion of equivalence,” _arXiv_ _preprint_
_arXiv:2410.21228_, 2024.

[101] L. Zhang, L. Zhang, S. Shi, X. Chu, and B. Li, “Lora-fa: Memoryefficient low-rank adaptation for large language models fine-tuning,”
_arXiv_ _preprint_ _arXiv:2308.03303_, 2023.

[102] J. Zhu, K. Greenewald, K. Nadjahi, H. S. D. O. Borde, R. B. Gabrielsson, L. Choshen, M. Ghassemi, M. Yurochkin, and J. Solomon, “Asymmetry in low-rank adapters of foundation models,” _arXiv_ _preprint_
_arXiv:2402.16842_, 2024.

[103] S. Ghosh, C. K. R. Evuru, S. Kumar, D. Aneja, Z. Jin, R. Duraiswami,
D. Manocha _et_ _al._, “A closer look at the limitations of instruction
tuning,” _arXiv_ _preprint_ _arXiv:2402.05119_, 2024.

[104] M. McCloskey and N. J. Cohen, “Catastrophic interference in connectionist networks: The sequential learning problem,” in _Psychology_ _of_
_learning_ _and_ _motivation_ . Elsevier, 1989, vol. 24, pp. 109–165.

[105] J. Schulman and T. M. Lab, “Lora without regret,” _Thinking_ _Machines_
_Lab:_ _Connectionism_, 2025, https://thinkingmachines.ai/blog/lora/.

[106] N. Shazeer and M. Stern, “Adafactor: Adaptive learning rates with
sublinear memory cost,” in _International_ _Conference_ _on_ _Machine_
_Learning_ . PMLR, 2018, pp. 4596–4604.

[107] J. Ren, S. Rajbhandari, R. Y. Aminabadi, O. Ruwase, S. Yang,
M. Zhang, D. Li, and Y. He, “ _{_ Zero-offload _}_ : Democratizing _{_ billionscale _}_ model training,” in _2021_ _USENIX_ _Annual_ _Technical_ _Conference_
_(USENIX_ _ATC_ _21)_, 2021, pp. 551–564.

[108] M. Frank, P. Wolfe _et_ _al._, “An algorithm for quadratic programming,”
_Naval_ _research_ _logistics_ _quarterly_, vol. 3, no. 1-2, pp. 95–110, 1956.

[109] T. Chen and C. Guestrin, “Xgboost: A scalable tree boosting system,”
in _Proceedings_ _of_ _the_ _22nd_ _acm_ _sigkdd_ _international_ _conference_ _on_
_knowledge_ _discovery_ _and_ _data_ _mining_, 2016, pp. 785–794.

[110] A. Edalati, M. Tahaei, I. Kobyzev, V. P. Nia, J. J. Clark, and M. Rezagholizadeh, “Krona: Parameter-efficient tuning with kronecker adapter,”
in _Enhancing_ _LLM_ _Performance:_ _Efficacy,_ _Fine-Tuning,_ _and_ _Inference_
_Techniques_ . Springer, 2025, pp. 49–65.

[111] M. Dehghani, S. Gouws, O. Vinyals, J. Uszkoreit, and Ł. Kaiser,
“Universal transformers,” _arXiv_ _preprint_ _arXiv:1807.03819_, 2018.

[112] S. Takase and S. Kiyono, “Lessons on parameter sharing across layers
in transformers,” _arXiv_ _preprint_ _arXiv:2104.06022_, 2021.

[113] K. Lu, A. Grover, P. Abbeel, and I. Mordatch, “Frozen pretrained
transformers as universal computation engines,” in _Proceedings_ _of_ _the_
_AAAI_ _conference_ _on_ _artificial_ _intelligence_, vol. 36, no. 7, 2022, pp.
7628–7636.

[114] M. Schrimpf, I. A. Blank, G. Tuckute, C. Kauf, E. A. Hosseini,
N. Kanwisher, J. B. Tenenbaum, and E. Fedorenko, “The neural
architecture of language: Integrative modeling converges on predictive
processing,” _Proceedings_ _of_ _the_ _National_ _Academy_ _of_ _Sciences_, vol.
118, no. 45, p. e2105646118, 2021.

[115] J. Frankle, D. J. Schwab, and A. S. Morcos, “Training batchnorm and
only batchnorm: On the expressive power of random features in cnns,”
_arXiv_ _preprint_ _arXiv:2003.00152_, 2020.

[116] S. Lin, P. Lyu, D. Liu, T. Tang, X. Liang, A. Song, and X. Chang, “Mlp
can be a good transformer learner,” in _Proceedings_ _of_ _the_ _IEEE/CVF_
_Conference_ _on_ _Computer_ _Vision_ _and_ _Pattern_ _Recognition_, 2024, pp.
19 489–19 498.

[117] Y. Mao, K. Huang, C. Guan, G. Bao, F. Mo, and J. Xu, “Dora: Enhancing parameter-efficient fine-tuning with dynamic rank distribution,”
_arXiv_ _preprint_ _arXiv:2405.17357_, 2024.

[118] N. Ding, X. Lv, Q. Wang, Y. Chen, B. Zhou, Z. Liu, and M. Sun,
“Sparse low-rank adaptation of pre-trained language models,” _arXiv_
_preprint_ _arXiv:2311.11696_, 2023.

[119] H. Rajabzadeh, M. Valipour, T. Zhu, M. Tahaei, H. J. Kwon, A. Ghodsi,
B. Chen, and M. Rezagholizadeh, “Qdylora: Quantized dynamic lowrank adaptation for efficient large language model tuning,” _arXiv_
_preprint_ _arXiv:2402.10462_, 2024.

[120] B. Mishra and R. Sepulchre, “Riemannian preconditioning,” _SIAM_
_Journal_ _on_ _Optimization_, vol. 26, no. 1, pp. 635–660, 2016.

[121] M. Bini, K. Roth, Z. Akata, and A. Khoreva, “Ether: Efficient finetuning of large-scale models with hyperplane reflections,” _arXiv_ _preprint_
_arXiv:2405.20271_, 2024.




[122] J. Zhao, Z. Zhang, B. Chen, Z. Wang, A. Anandkumar, and Y. Tian,
“Galore: Memory-efficient llm training by gradient low-rank projection,” _arXiv_ _preprint_ _arXiv:2403.03507_, 2024.

[123] C. Si, X. Yang, and W. Shen, “See further for parameter efficient finetuning by standing on the shoulders of decomposition,” _arXiv_ _preprint_
_arXiv:2407.05417_, 2024.

[124] K. He, X. Zhang, S. Ren, and J. Sun, “Deep residual learning for image
recognition,” in _Proceedings of the IEEE conference on computer vision_
_and_ _pattern_ _recognition_, 2016, pp. 770–778.

[125] G. Montavon, G. Orr, and K.-R. M¨uller, _Neural_ _networks:_ _tricks_ _of_ _the_
_trade_ . springer, 2012, vol. 7700.

[126] C. Eckart and G. Young, “The approximation of one matrix by another
of lower rank,” _Psychometrika_, vol. 1, no. 3, pp. 211–218, 1936.

[127] L. Mirsky, “Symmetric gauge functions and unitarily invariant norms,”
_The_ _quarterly_ _journal_ _of_ _mathematics_, vol. 11, no. 1, pp. 50–59, 1960.

[128] S. Azizi, S. Kundu, and M. Pedram, “Lamda: Large model fine-tuning
via spectrally decomposed low-dimensional adaptation,” _arXiv preprint_
_arXiv:2406.12832_, 2024.

[129] K. B¨uy¨ukaky¨uz, “Olora: Orthonormal low-rank adaptation of large
language models,” _arXiv_ _preprint_ _arXiv:2406.01775_, 2024.

[130] K. Lv, Y. Yang, T. Liu, Q. Gao, Q. Guo, and X. Qiu, “Full parameter
fine-tuning for large language models with limited resources,” _arXiv_
_preprint_ _arXiv:2306.09782_, 2023.

[131] K. Ponkshe, R. Singhal, E. Gorbunov, A. Tumanov, S. Horvath, and
P. Vepakomma, “Initialization using update approximation is a silver
bullet for extremely efficient low-rank fine-tuning,” _arXiv_ _preprint_
_arXiv:2411.19557_, 2024.

[132] D. A. Ross, J. Lim, R.-S. Lin, and M.-H. Yang, “Incremental learning
for robust visual tracking,” _International_ _journal_ _of_ _computer_ _vision_,
vol. 77, no. 1, pp. 125–141, 2008.

[133] N. Halko, P.-G. Martinsson, and J. A. Tropp, “Finding structure
with randomness: Probabilistic algorithms for constructing approximate
matrix decompositions,” _SIAM_ _review_, vol. 53, no. 2, pp. 217–288,
2011.

[134] A. Radford, J. W. Kim, C. Hallacy, A. Ramesh, G. Goh, S. Agarwal,
G. Sastry, A. Askell, P. Mishkin, J. Clark _et_ _al._, “Learning transferable
visual models from natural language supervision,” in _International_
_conference_ _on_ _machine_ _learning_ . PmLR, 2021, pp. 8748–8763.

[135] J. Krause, M. Stark, J. Deng, and L. Fei-Fei, “3d object representations
for fine-grained categorization,” in _Proceedings_ _of_ _the_ _IEEE_ _interna-_
_tional_ _conference_ _on_ _computer_ _vision_ _workshops_, 2013, pp. 554–561.

[136] M. Cimpoi, S. Maji, I. Kokkinos, S. Mohamed, and A. Vedaldi, “Describing textures in the wild,” in _Proceedings_ _of_ _the_ _IEEE_ _conference_
_on_ _computer_ _vision_ _and_ _pattern_ _recognition_, 2014, pp. 3606–3613.

[137] P. Helber, B. Bischke, A. Dengel, and D. Borth, “Eurosat: A novel
dataset and deep learning benchmark for land use and land cover
classification,” _IEEE_ _Journal_ _of_ _Selected_ _Topics_ _in_ _Applied_ _Earth_
_Observations and Remote Sensing_, vol. 12, no. 7, pp. 2217–2226, 2019.

[138] S. Houben, J. Stallkamp, J. Salmen, M. Schlipsing, and C. Igel,
“Detection of traffic signs in real-world images: The german traffic
sign detection benchmark,” in _The_ _2013_ _international_ _joint_ _conference_
_on_ _neural_ _networks_ _(IJCNN)_ . Ieee, 2013, pp. 1–8.

[139] G. Cheng, J. Han, and X. Lu, “Remote sensing image scene classification: Benchmark and state of the art,” _Proceedings_ _of_ _the_ _IEEE_, vol.
105, no. 10, pp. 1865–1883, 2017.

[140] J. Xiao, J. Hays, K. A. Ehinger, A. Oliva, and A. Torralba, “Sun
database: Large-scale scene recognition from abbey to zoo,” in _2010_
_IEEE_ _computer_ _society_ _conference_ _on_ _computer_ _vision_ _and_ _pattern_
_recognition_ . IEEE, 2010, pp. 3485–3492.

[141] Y. Netzer, T. Wang, A. Coates, A. Bissacco, B. Wu, A. Y. Ng _et_ _al._,
“Reading digits in natural images with unsupervised feature learning,”
in _NIPS workshop on deep learning and unsupervised feature learning_,
vol. 2011, no. 2. Granada, 2011, p. 4.

[142] L. Yu, W. Jiang, H. Shi, J. Yu, Z. Liu, Y. Zhang, J. T. Kwok, Z. Li,
A. Weller, and W. Liu, “Metamath: Bootstrap your own mathematical
questions for large language models,” _arXiv preprint arXiv:2309.12284_,
2023.

[143] K. Cobbe, V. Kosaraju, M. Bavarian, M. Chen, H. Jun, L. Kaiser,
M. Plappert, J. Tworek, J. Hilton, R. Nakano _et_ _al._, “Training verifiers
to solve math word problems,” _arXiv preprint arXiv:2110.14168_, 2021.

[144] T. Zheng, G. Zhang, T. Shen, X. Liu, B. Y. Lin, J. Fu, W. Chen,
and X. Yue, “Opencodeinterpreter: Integrating code generation with
execution and refinement,” _arXiv_ _preprint_ _arXiv:2402.14658_, 2024.

[145] M. Chen, J. Tworek, H. Jun _et_ _al._, “Evaluating large language models
trained on code,” 2021.


JOURNAL OF L [A] TEX CLASS FILES, VOL. 18, NO. 9, SEPTEMBER 2020 21


[146] Z. Han, C. Gao, J. Liu, J. Zhang, and S. Q. Zhang, “Parameter-efficient
fine-tuning for large models: A comprehensive survey,” _arXiv_ _preprint_
_arXiv:2403.14608_, 2024.

[147] L. Wang, S. Chen, L. Jiang, S. Pan, R. Cai, S. Yang, and F. Yang,
“Parameter-efficient fine-tuning in large models: A survey of methodologies,” _arXiv_ _preprint_ _arXiv:2410.19878_, 2024.

[148] L. Xu, H. Xie, S.-Z. J. Qin, X. Tao, and F. L. Wang, “Parameterefficient fine-tuning methods for pretrained language models: A critical
review and assessment,” _arXiv_ _preprint_ _arXiv:2312.12148_, 2023.

[149] Y. Mao, Y. Ge, Y. Fan, W. Xu, Y. Mi, Z. Hu, and Y. Gao, “A survey on
lora of large language models,” _Frontiers of Computer Science_, vol. 19,
no. 7, p. 197605, 2025.

[150] M. Yang, J. Chen, Y. Zhang, J. Liu, J. Zhang, Q. Ma, H. Verma,
Q. Zhang, M. Zhou, I. King _et al._, “Low-rank adaptation for foundation
models: A comprehensive review,” _arXiv_ _preprint_ _arXiv:2501.00365_,
2024.

[151] N. Houlsby, A. Giurgiu, S. Jastrzebski, B. Morrone, Q. De Laroussilhe,
A. Gesmundo, M. Attariyan, and S. Gelly, “Parameter-efficient transfer
learning for nlp,” in _International_ _conference_ _on_ _machine_ _learning_ .
PMLR, 2019, pp. 2790–2799.

[152] P. He, X. Liu, J. Gao, and W. Chen, “Deberta: Decoding-enhanced bert
with disentangled attention,” _arXiv_ _preprint_ _arXiv:2006.03654_, 2020.

[153] B. Zi, X. Qi, L. Wang, J. Wang, K.-F. Wong, and L. Zhang, “Delta-lora:
Fine-tuning high-rank parameters with the delta of low-rank matrices,”
_arXiv_ _preprint_ _arXiv:2309.02411_, 2023.

[154] C. Raffel, N. Shazeer, A. Roberts, K. Lee, S. Narang, M. Matena,
Y. Zhou, W. Li, and P. J. Liu, “Exploring the limits of transfer learning
with a unified text-to-text transformer,” _Journal_ _of_ _machine_ _learning_
_research_, vol. 21, no. 140, pp. 1–67, 2020.

[155] H. Touvron, L. Martin, K. Stone, P. Albert, A. Almahairi, Y. Babaei,
N. Bashlykov, S. Batra, P. Bhargava, S. Bhosale _et_ _al._, “Llama
2: Open foundation and fine-tuned chat models,” _arXiv_ _preprint_
_arXiv:2307.09288_, 2023.

[156] H. Touvron, T. Lavril, G. Izacard, X. Martinet, M.-A. Lachaux,
T. Lacroix, B. Rozi`ere, N. Goyal, E. Hambro, F. Azhar _et_ _al._, “Llama:
Open and efficient foundation language models,” _arXiv_ _preprint_
_arXiv:2302.13971_, 2023.

[157] G. Team, T. Mesnard, C. Hardin, R. Dadashi, S. Bhupatiraju, S. Pathak,
L. Sifre, M. Rivi`ere, M. S. Kale, J. Love _et_ _al._, “Gemma: Open
models based on gemini research and technology,” _arXiv_ _preprint_
_arXiv:2403.08295_, 2024.

[158] G. Team, M. Riviere, S. Pathak, P. G. Sessa, C. Hardin, S. Bhupatiraju,
L. Hussenot, T. Mesnard, B. Shahriari, A. Ram´e _et_ _al._, “Gemma
2: Improving open language models at a practical size, 2024,” _URL_
_https://arxiv._ _org/abs/2408.00118_, vol. 1, no. 3, 2024.

[159] G. Team, A. Kamath, J. Ferret, S. Pathak, N. Vieillard, R. Merhej,
S. Perrin, T. Matejovicova, A. Ram´e, M. Rivi`ere _et_ _al._, “Gemma 3
technical report,” _arXiv_ _preprint_ _arXiv:2503.19786_, 2025.

[160] A. Dosovitskiy, L. Beyer, A. Kolesnikov, D. Weissenborn, X. Zhai,
T. Unterthiner, M. Dehghani, M. Minderer, G. Heigold, S. Gelly _et al._,
“An image is worth 16x16 words: Transformers for image recognition
at scale,” _arXiv_ _preprint_ _arXiv:2010.11929_, 2020.


JOURNAL OF L [A] TEX CLASS FILES, VOL. 18, NO. 9, SEPTEMBER 2020 22



APPENDIX


_A._ _Related_ _Works_


_1)_ _Survey of PEFT and LoRA:_ Despite considerable survey
attention on PEFT, its most influential method, LoRA, and
its proliferating variants receive superficial coverage. Existing
surveys treat LoRA as a minor component within broader
PEFT taxonomies, offering only cursory lists or brief summaries. For example, Han et al. [146] include a short section on
“Reparameterized PEFT” without detailed analysis or mathematical formulations. Wang et al. [147] catalog over 10 LoRAinspired methods but provide merely enumerative descriptions
lacking systematic categorization. Xu et al. [148] list 11 LoRA
variants with formulations but do not analyze their underlying
mechanisms or comparative advantages. Mao et al. [149] and
Yang et al. [150] conduct comprehensive surveys yet still
offer lists with brief explanations rather than deeper insights.
In summary, while acknowledging LoRA’s popularity, these
surveys lack a principled and in-depth examination. This gap
motivates our work: a dedicated, systematic, and analytical
survey tracing the evolution of LoRA variants, dissecting their
innovations, and evaluating their trade-offs.
_2)_ _Evaluation_ _of_ _LoRA_ _and_ _its_ _Variants:_ Evaluating LoRA
and its variants is complex. The original LoRA paper [8]
benchmarks LoRA against PEFT methods including BitFit [6]
and adapter tuning [151] on models like RoBERTa [30],
DeBERTa [152], GPT-2 [32], and GPT-3-175B [34]. Several
follow-up studies [22], [61], [153] adhere to similar pipelines
to demonstrate advantages over vanilla LoRA. However, the
NLU evaluation pipeline for vanilla LoRA requires intensive
hyperparameter grid searches, hindering large-scale comparisons. Its NLG pipeline uses outdated models like GPT-2/GPT3 on tasks such as WikiSQL [35] and MNLI [31], which are
not representative of current frontier models like the Llama3
series [37] or modern NLG scenarios. Recent LoRA variants
are also evaluated on vision tasks alongside NLU and NLG.
For NLU, the GLUE benchmark with models like RoBERTa,
DeBERTa, and T5 [154] is common, with RoBERTa being
the most frequent choice. For NLG, LLMs such as the Llama
series [37], [155], [156] and Gemma series [157]–[159] are
evaluated on commonsense reasoning, chat, mathematical reasoning, and code generation. For vision, ViT [160] and CLIPViT are commonly tested on image classification tasks. Considering this, our comprehensive evaluation tests RoBERTaBase on GLUE for NLU, Llama-3.1-8B-Base on mathematical
reasoning and code generation for NLG, and CLIP-ViT-16/B
on seven image classification tasks for vision performance.


_B._ _Notations_


This section delineates the notations utilized throughout this
paper. Unless otherwise indicated, all notations conform to the
definitions presented in Table I.


_C._ _Additional_ _Experimental_ _Results_


Due to space constraints within the main body of the paper,
this section presents supplementary experimental results of
significance.



_1)_ _Computational_ _and_ _Memory_ _Overhead_ _Analysis:_ Table II presents the numerical training time and peak memory
usage of some variants implemented in LoRAFactory (variants
such as LORA+, which do not affect the efficiency of LORA,
are not presented in this table). To ensure intrinsic efficiency is
measured without masking effects from external optimizations,
experiments were conducted on a single NVIDIA H200 GPU
using the Llama-3.1-8B-Base model (BF16 mixed precision,
sequence length 1024, batch size 1) without parallelism, CPU
offloading, or activation checkpointing.
Vanilla LORA serves as the foundational baseline, achieving the lowest memory footprint (30,067 MB) and the fastest
training time (4h 42m). In contrast, DORA exhibits the highest
memory consumption (52,847 MB, +75%), primarily because
methods like DORA, HIRA, and LOHA explicitly materialize
low-rank matrices ( _A_ and _B_ ) and their product during the
forward pass. Vanilla LoRA avoids this by fusing computation
of low-rank weights, a benefit that persists unless activation
checkpointing is applied. As the router in each LORAMOE
module introduces additional trainable parameters, we compare the computational and memory overhead of LORAMOE
with two settings: 8 total experts and 2 activated experts per
module; 6 total experts and 2 activated experts per module,
each expert with a rank of 1. Therefore, the prior setting has
an identical overall rank of 8 with LORA, but it introduces
significantly more trainable parameters. The latter setting has
a comparable number of trainable parameters with LORA but
a smaller overall rank. Both settings of LORAMOE require
significantly longer training durations compared to LORA
due to the mixture-of-experts architecture, which introduces
significant overhead through learnable token routers. While
MOSLORA, RASA, and MELORA maintain memory profiles similar to vanilla LoRA with moderate speed tradeoffs, methods like ADALORA and RANDLORA suffer from
prolonged training times due to dynamic rank allocation or
high-rank computation strategies (The official implementation
of RANDLORA adopts full-rank computation, which leads
to high computational cost. We limit the upper bound of
the dimension of random bases of RANDLORA to 1024,
denoted as RANDLORA _U_ =1024). These results highlight the
inherent tension between expressiveness and efficiency in
LoRA extensions.
_2)_ _Learning_ _Rate_ _Sweep_ _Results_ _on_ _NLU_ _Tasks:_ **Exper-**
**imental** **settings.** We fine-tune RoBERTa-base to evaluate
LoRA and its variants on the full GLUE benchmark. We
follow standard evaluation metrics for each GLUE sub-task:
accuracy for SST-2, MNLI, MRPC, QNLI, and RTE; Pearson
correlation for STS-B; F1 for QQP; and Matthews Correlation
Coefficient for CoLA. We employ a linear learning rate decay
schedule with a warm-up ratio of 0.03. Seven learning rates
are tested for all methods, including: [1e-6, 1e-5, 5e-5, 1e-4,
5e-4, 1e-3, 5e-3].
All experimental settings remain consistent across runs. The
batch size is 32, weight decay is disabled, and the maximum
sequence length is 256 for all GLUE sub-tasks. Both the
base model and all LoRA modules operate in FP32 precision
without mixed-precision training. Each training run consists of
10 epochs, with the test performance recorded at the end of


JOURNAL OF L [A] TEX CLASS FILES, VOL. 18, NO. 9, SEPTEMBER 2020 23


TABLE I
LIST OF NOTATIONS


**Symbol** **Description**


_W_ _∈_ R _[m][×][n]_ Weight matrix of a linear layer.
_W_ - _∈_ R _[m][×][n]_ pretrained weight of _W_ .
∆ _W_ Update applied to the weight _W_ during fine-tuning.
_A ∈_ R _[m][×][r]_, _B_ _∈_ R _[r][×][n]_ Trainable low-rank matrices in the standard LoRA decomposition.
_r_ Rank hyperparameter of LoRA and its most variants, with _r_ _≪_ min( _m, n_ ).
_α_ Scaling hyperparameter of LoRA and its most variants.
_γr_ Scaling factor of LoRA, _γr_ _→_ 0 as _r_ _→∞_ .
_η_ Learning rate used for parameter updates.
_∇W_ [�] Gradient of the pretrained weight _W_ .

[�]
_∇A_, _∇B_ Gradients of the low-rank matrices _A_ and _B_ .
_Wt_ Weight matrix of a linear layer at fine-tuning step _t_ ( _Wt_ = _W_ [�] + ∆ _Wt_ ).
_At_, _Bt_ Values of the low-rank matrices _A_ and _B_ at fine-tuning step _t_ .
_A_ 0, _B_ 0 Initial values of the low-rank matrices _A_ and _B_ .
SVD( _M_ ) Singular Value Decomposition of matrix _M_ .
Tr( _M_ ) Trace of matrix _M_ .
_U, S, V_ Matrices from the SVD of a matrix, i.e., _M_ = _USV_ _[⊤]_ .
_⊙_ Hadamard (element-wise) product of two matrices.
_⊗_ Kronecker product of two matrices.

 - Block-diagonal matrix constructor.

[ _M_ 1 _|M_ 2 _. . . |Mn_ ] Matrix concatenation operator.
_R_ ( _M_ ) Rank of matrix _M_ .
_∥· ∥F_ Frobenius norm of a matrix.
_L_ task Primary task-specific loss function (e.g., cross-entropy).
_L_ reg Auxiliary regularization loss (e.g., for orthogonality in AdaLoRA).
LoRAFactory A unified, modular codebase developed in this work for benchmarking LoRA variants.
LLMs Large Language Models
NLU Natural Language Understanding.
NLG Natural Language Generation.
IC Image Classification.
PEFT Parameter-Efficient Fine-Tuning.
MoE Mixture of Experts.


TABLE II
COMPUTATIONAL AND MEMORY USAGE OF LORA VARIANTS. _†_ DENOTES THE USE OF ACTIVATION CHECKPOINTING.


**Method** **#Params** **Time** **Memory**


LORA [8] 20.97M 4h42min 30067MB
LORA _[†]_ [8] 20.97M 6h22min 20873MB
DORA [67] 22.35M 9h19min 52847MB
DORA _[†]_ [67] 22.35M 12h17min 21729MB
DELORA [68] 20.97M 9h16min 39343MB
ADALORA [22] 20.97M 12h10min 30447MB
HIRA [45] 20.97M 8h10min 39669MB
RASA [49] 20.98M 6h14min 30381MB
DENSELORA [50] 23.99M 7h16min 37751MB
RANDLORA [23] 23.30M 39h31min 81645MB
RANDLORA _U_ =1024 [23] 23.30M 13h24min 41187MB
MELORA [42] 20.97M 6h49min 30847MB
LORAMOE _e_ =8 [86] 30.93M 36h31min 46425MB
LORAMOE _e_ =6 [86] 23.20M 27h57min 45937MB
MOSLORA [92] 20.99M 5h50min 30085MB
AURORA [72] 21.00M 12h32min 30549MB
LOHA [43] 20.97M 35h28min 92851MB
LOKR [44] 20.86M 35h53min 56151MB
LORAN [74] 20.97M 6h28min 45747MB


JOURNAL OF L [A] TEX CLASS FILES, VOL. 18, NO. 9, SEPTEMBER 2020 24



|(b|) Optimization|Process Adjust|ment|Col5|Col6|Col7|
|---|---|---|---|---|---|---|
||||||||
||||||||
||||||||
|||||Lo<br>~~De~~|RA<br>~~LoRA~~<br>LoRA<br>~~RsLo~~|+<br>~~RA~~|
|||||Do|RA<br>||


|(d|) Mixture-of-E|xperts|Col4|Col5|Col6|Col7|
|---|---|---|---|---|---|---|
||||||||
||||||||
|||||LoRA|MoSLo|RA|


LoRAMoE



70


60


50


40


70


60


50


40


|(a|) Initialization|Adjustment|Col4|Col5|Col6|Col7|
|---|---|---|---|---|---|---|
||||||||
||||||||
||||||||
|||||Lo<br>Pi<br>EV|RA<br>SSA<br>A<br>LoRA-<br>LoRA-<br>NZLoR|GA<br>One<br>A|



|(c|) Rank Adjustm|ent|Col4|Col5|Col6|Col7|
|---|---|---|---|---|---|---|
||||||||
||||||||
|||||LoRA<br>~~RaSA~~<br>DenseL|oRA<br>MeLoR<br>~~ReLoR~~<br>AdaLo|A<br>~~A~~<br>RA|


RandLoRA







GOAT



HiRA



70


60


50


40


70


60


50


40



30
1e-6 1e-5 5e-5 1e-4 5e-4 1e-3



1e-6 1e-5 5e-5 1e-4 5e-4 1e-3



Fig. 9. Performance comparison of various LoRA variants on the GLUE benchmark across different learning rates. Results are grouped by method category
as illustrated in Section II. All plots share the same y-axis (averaged numerical score) and x-axis (learning rate).



each epoch; the best test result across all 10 epochs is reported.
**Experimental** **results.** Figure 9 shows the average evaluation results on the 9 subsets of the GLUE benchmark. For
the detailed numerical results of each subset, please refer to
Table IV- X.
The average performance of LORA attains a relatively modest value of 55.23 at the lowest learning rate examined, with
performance progressively increasing to 79.66 as the learning
rate rises to 1e-4. Among all tested variants, only RASA
significantly exceeds LoRA in peak performance, achieving
81.37 at the learning rate of 5e-4.
All initialization-based LORA variants significantly enhance gradient flow at small learning rates (e.g., 1e-5), leading
to improved performance in such configurations. Similarly,
MELORA incorporates a block-diagonal structure, which also
amplifies the gradient magnitude in LORA. However, these
enhancements come at a cost: the improved gradient properties
hinder convergence at higher learning rates, preventing these
methods from reaching or surpassing the peak performance
achievable with standard LORA under such settings. Simultaneously, LORA+ implements a learning rate decoupling
strategy for the low-rank matrices _A_ and _B_ within low-rank
adapters. For LORA+, it is recommended that the learning
rate for matrix _B_ be set to 16 times that of matrix _A_ . This
approach effectively applies a higher learning rate to matrix
_B_ compared to standard LoRA under an equivalent base
learning rate, which governs matrix _A_ and other trainable
parameters. In practice, while these variants perform well
with smaller learning rates, their effectiveness diminishes,
occasionally sharply, when larger learning rates are employed.
In contrast, the auxiliary loss in ADALORA, the weight
decomposition strategies in DORA and DELORA, and the



Hadamard product operation between low-rank and pretrained
weights in HIRA significantly impede convergence at small
learning rates. For instance, HIRA achieves only 53.19 at a
learning rate of 1e-5, which is 16.6 points lower than LORA
under the same setting. As a result, these methods require
learning rates that are about 10 to 1000 times larger than
those used by LoRA to achieve comparable performance. It
should be noted that LORA itself typically employs learning
rates 10 to 100 times higher than those commonly used in full
fine-tuning. Notably, most of these methods do not explicitly
state in their original papers that they require such elevated
learning rates. This observation highlights the importance of
carefully selecting learning rates when applying these methods
in practice, as their optimal values may differ significantly
from those used in standard fine-tuning approaches.


For Mixture-of-Experts integration based LoRA Variants,
both LORAMOE and GOAT fail to surpass the performance
of LoRA on most learning rates we tested, while requiring
substantially more training and inference time. One possible
reason is that under similar trainable parameter budgets, the inherently sparse structure of MoE-based methods can limit their
overall performance. As a non-traditional mixture-of-experts
approach, MOSLORA introduces a small intermediate matrix
to the low-rank adapter, demonstrating greater stability with
respect to learning rate selection than LORA. Our experiments
on NLG and IC also validate this observation.


_3)_ _Learning_ _Rate_ _Sweep_ _Results_ _on_ _IC_ _Tasks:_ **Experimen-**
**tal** **settings** For image classification tasks, we fine-tune CLIPViT-16/B on seven benchmark datasets: Stanford-Cars [135],
DTD [136], EuroSAT [137], GTSRB [138], RESISC45 [139],
SUN397 [140], and SVHN [141]. Each method’s classification


JOURNAL OF L [A] TEX CLASS FILES, VOL. 18, NO. 9, SEPTEMBER 2020 25



80


70


60


50


40


30


80


70


60


50


40





80


70


60


50


40





80


60











40


20



30

|(c|) Rank Ad|justment|Col4|Col5|Col6|Col7|Col8|Col9|Col10|
|---|---|---|---|---|---|---|---|---|---|
|||||||||||
|||||||||||
|||||||||||
|||||||Lo<br>Ad|RA<br>aLoRA|DenseLo<br>RandLo|RA<br>A|
|||||||Hi<br>Ra|RA<br>SA|ReLoRA<br>MeLoRA||

1e-6 1e-5 2e-5 5e-5 1e-4 2e-4 5e-4 1e-3 2e-3


|(d|) Mixture|-of-Exper|ts|Col5|Col6|Col7|Col8|Col9|Col10|
|---|---|---|---|---|---|---|---|---|---|
|||||||||||
|||||||||||
|||||||L<br>|oRA<br>|GOAT<br>||
||||||||~~oSLoRA~~|~~LoRA~~|~~oE~~|



1e-6 1e-5 2e-5 5e-5 1e-4 2e-4 5e-4 1e-3 2e-3



Fig. 10. Performance comparison of LoRA variants on seven image classification tasks across different learning rates. All plots share the same y-axis
(accuracy) and x-axis (learning rate).



accuracy is evaluated on the corresponding test set of each
task. Experiments are repeated with ten distinct learning rates:

[1e-6, 1e-5, 2e-5, 5e-5, 1e-4, 2e-4, 5e-4, 1e-3, 2e-3, 5e-3].
Other experimental settings, including the optimizer (and its
configurations), learning rate scheduler (and its configurations), and batch size, remain identical to those used in our
NLG experiments and are held constant across all runs.


**Experimental** **results** Figure 10 shows the average evaluation results on the 7 subsets of the IC tasks, with LORA and
its variants exhibiting a gradual performance improvement as
the learning rate increases, consistent with the trends observed
in our NLU and NLG experiments; for the results of each
subset, please refer to Table XI- XIX. For LORA, average
performance rises steadily from 54.22 at a learning rate of 1e6 to 90.75 at 5e-4. In contrast to our experiments on natural
language understanding and generation, LORA and its variants
demonstrate greater robustness to variations in learning rates
on the information classification tasks examined. Specifically,
LORA achieves a performance of 90.03 at a learning rate
of 2e-4, with performance remaining approximately stable
when the learning rate is slightly reduced to 1e-4 or increased
to 5e-4. Most experimental results are similar to those of
our experiments on NLU and NLG: variants with enhanced
gradient flow (including LORA+, which sets the learning rate
of matrix _B_ 16 times the base learning rate) show advantages
over vanilla LORA at small learning rates, and the advantages
diminish gradually as LORA approaches its peak performance;
ADALORA, HIRA, and DELORA show clear disadvantages
over other methods at small learning rates for their constraints
on the optimization process.



_4)_ _Additional_ _Experimental_ _Settings:_ For LORA variants
evaluated in our experiments, we adopt the following variantspecific hyperparameters (we adopt the recommended settings
if possible):


_•_ LORA-GA: The number of gradient estimation steps is
set to 64; the hyperparameter _γ_ is set to 16.

_•_ NZLORA: Both hyperparameters _γA_ and _γB_ are set to
16.

_•_ PISSA: The number of fast SVD decomposition iterations PISSA is set to 64.

_•_ LORA-ONE: The number of gradient estimation steps is
set to 64; the hyperparameter _γ_ is set to 128.

_•_ EVA: The number of the activation estimation steps is
set to 64; the convergence threshold of the incremental
SVD is set to 0.9.

_•_ DELORA: The hyperparamter _λ_ is set to 8. The initialization schemes for _A_ and _B_ are both the Kaiming uniform
distribution.

_•_ LORA+: The ratio of learning rates used for _B_ and _A_ is
set to 16.

_•_ MELORA: The number of diagonal blocks is set to 2,
resulting in a overall rank of 16 for each adapter.

_•_ RELORA: The low-rank weights are merged and reinitialized 3-5 times during each training process; the
number of re-warmup steps after each _merge-and-reinit_
process is set to 10.

_•_ ADALORA: The hyperparamter _ti_ is set to 100 while _tf_
is set to 900. The initial rank is set to 12, and the final
effective rank is set to 8.

_•_ RANDLORA: The rank of low-rank bases is set to
32, ensuring a comparable trainable parameter count to


JOURNAL OF L [A] TEX CLASS FILES, VOL. 18, NO. 9, SEPTEMBER 2020 26



LORA; the upper bound of the dimension of all lowrank bases is set to 1024, resulting in a maximum rank
of 1024.

_•_ RASA: The shared rank _k_ is set to 1, resulting in an
overall rank of _r −_ 1 + _L_ for each adapter.

_•_ DENSELORA: The rank of each adapter is set to 24 _·_ _r_ =
192, where _r_ is the rank used for vanilla LORA. The
hyperparameter _α_ is therefore set to 48 _· r_ = 384. This
setting results in a comparable trainable parameter count
to LORA but with a much higher overall rank.

_•_ LORAMOE and GOAT: The number of experts is set to
8, each expert with a rank of 1, resulting in a total rank
of 8; the number of activated experts for each token is
set to 2.

_•_ HIRA: No extra hyperparameters.

_•_ MOSLORA: No extra hyperparameters.

_•_ RSLORA: No extra hyperparameters.

_•_ DORA: No extra hyperparameters.


_5)_ _Learning Rate Sweep Results on High-rank Settings:_ To
systematically investigate the high-rank performance of LORA
and its variants, we select one representative variant from each
major category of LoRA extensions and evaluate their behavior
under a high-rank setting. Specifically, we benchmark four
variants: LORA-GA, RSLORA, MELORA, and LORAMOE,
against vanilla LORA. All experimental configurations are
kept identical to those used in our main NLG experiments,
except that the LoRA rank is uniformly set to 128 across all
methods. As noted in Section II, it is common practice to set
the scaling hyperparameter _α_ to twice the LORA rank. To
isolate and assess the impact of this convention, particularly
in contrast to variants like RSLORA, which inherently adjust
scaling, we also evaluate vanilla LORA with _α_ = 256 (i.e., 2
× 128) as a controlled baseline.


The experimental results under the high-rank setting are
summarized in Table III. On GSM8K, Vanilla LORA achieves
the best performance among all evaluated methods, reaching
76 _._ 57 (an improvement of +1 _._ 07 over LORA with _r_ = 8)
with a learning rate of 1e-4 and _α_ = 256. Notably, LORA
with _α_ = 16 also attains a competitive accuracy of 76 _._ 12
on GSM8K when using a relatively high learning rate of
5e-4. This suggests that, in our experimental setup, a larger
learning rate can partially compensate for the effect of a
small fixed _α_ . These trends differ from those reported in
Figure S3 of Biderman et al. [99], which may be due to
differences in learning-rate tuning or task selection across studies. Furthermore, the empirical findings from Kalajdzievski et
al. [65] indicate that the gradient norm of LORA tends to
collapse as the rank increases. Our results demonstrate that
this issue can be mitigated through several strategies: applying
the rank-stabilizing scaling of RSLORA; setting _α_ = 2 _r_ as
empirical studies suggested; adopting LORA variants with
enhanced gradient flow such as LORA-GA, or using a larger
learning rate. On HumanEval, Vanilla LORA ( _α_ = 256) and
LORA-GA both achieve peak performance of 51 _._ 30, which is
3 _._ 28 points higher than the peak performance of LORA with
_r_ = 8, at learning rates of 1e-4 and 5e-4, respectively. The
substantial improvements on both GSM8k and HumanEval



highlight the effectiveness of increasing LORA’s rank when
training settings are appropriately configured.


JOURNAL OF L [A] TEX CLASS FILES, VOL. 18, NO. 9, SEPTEMBER 2020 27


TABLE III
PERFORMANCE OF LORA AND ITS VARIANTS UNDER A HIGH-RANK SETTING ACROSS LEARNING RATES ON GSM8K AND HUMANEVAL. WE USE _†_ AND

_‡_ TO DENOTE LORA WITH _α_ = 256 AND _α_ = 16, RESPECTIVELY.


**Method** **GSM8K** **HumanEval**


**1e-5** **2e-5** **5e-5** **1e-4** **2e-4** **5e-4** **1e-5** **2e-5** **5e-5** **1e-4** **2e-4** **5e-4**


LoRA _[†]_ 72.02 72.40 74.98 76.57 74.30 1.29 46.88 46.80 48.70 51.30 51.07 41.31
LoRA _[‡]_ 61.87 66.49 72.86 71.65 73.01 76.12 40.02 41.84 43.90 46.11 47.09 48.63
LoRA-GA 70.66 72.48 75.74 75.82 74.60 71.42 41.16 46.49 51.30 50.99 51.07 48.48
RsLoRA 68.34 71.72 74.91 75.66 74.75 1.52 44.51 45.66 50.00 51.14 51.60 46.27
MELoRA 71.42 72.02 74.60 72.63 69.90 57.32 48.09 48.78 50.53 48.40 43.14 32.70


TABLE IV
PERFORMANCE COMPARISON ON THE GLUE BENCHMARK WITH A LEARNING RATE OF 1E-6.


Method SST-2 CoLA MNLI MRPC QNLI QQP RTE STS-B WNLI AVG


LoRA 89.45 0.00 78.69 66.38 82.70 79.43 47.65 13.37 39.44 55.23


**Rank** **Adjustment** **Based** **LoRA** **Variants**
HiRA 49.08 0.96 32.74 65.83 49.13 0.00 47.65 2.71 39.44 31.95
RaSA 88.76 0.00 76.95 66.38 80.59 78.64 48.38 6.20 40.85 54.08
AdaLoRA 49.08 0.00 32.77 65.71 48.92 0.00 47.65 2.64 39.44 31.66
MELoRA 92.55 0.00 84.10 66.38 88.82 83.33 50.54 78.53 39.44 64.85
DenseLoRA 91.51 0.00 81.29 66.38 86.02 81.30 48.74 0.00 36.62 54.58
RandLoRA 84.29 0.00 71.93 66.38 80.08 78.10 47.65 11.85 39.44 53.30
ReLoRA 89.22 0.00 77.47 66.38 81.85 82.31 48.38 15.48 40.85 55.77


**Optimization** **Process** **Adjustment** **Based** **LoRA** **Variants**
DoRA 89.56 0.00 78.70 66.38 82.93 79.48 47.65 13.88 39.44 55.34
RsLoRA 91.97 0.00 81.83 66.38 86.14 81.24 49.10 6.17 38.03 55.65
LoRA+ 93.23 0.00 84.64 66.38 89.76 84.04 49.10 81.13 49.30 66.40
DeLoRA 50.92 0.00 66.85 66.38 63.18 77.35 48.74 9.24 40.85 47.05


**Initialization** **Adjustment** **Based** **LoRA** **Variants**
EVA 91.63 0.00 81.57 66.38 86.75 80.95 49.46 20.34 38.03 57.23
PiSSA 90.94 0.00 82.01 66.38 85.68 81.48 49.10 18.05 38.03 56.85
LoRAGA 92.55 0.00 84.51 66.38 89.97 83.61 53.79 80.34 38.03 65.46
LoRA-One 89.11 0.00 78.18 66.38 83.29 78.60 47.29 9.15 56.34 56.48
NZLoRA 90.94 0.00 82.04 66.38 86.56 81.27 49.46 9.38 38.03 56.01


**Mixture-of-Experts** **Integration** **Based** **Variants**
GOAT 87.16 0.00 76.17 66.38 69.73 78.49 52.35 5.34 49.30 53.88
MoSLoRA 88.42 0.00 77.32 66.38 81.48 78.62 48.38 6.26 40.85 54.19
LoRAMoE 91.86 0.00 82.82 66.38 87.20 82.02 49.46 22.07 38.03 57.76


JOURNAL OF L [A] TEX CLASS FILES, VOL. 18, NO. 9, SEPTEMBER 2020 28


TABLE V
PERFORMANCE COMPARISON ON THE GLUE BENCHMARK WITH A LEARNING RATE OF 1E-5.


Method SST-2 CoLA MNLI MRPC QNLI QQP RTE STS-B WNLI AVG


LoRA 93.35 32.91 85.59 66.38 90.47 84.91 49.10 82.88 42.25 69.76


**Rank** **Adjustment** **Based** **LoRA** **Variants**
HiRA 86.12 0.00 76.76 66.26 79.62 78.65 47.65 4.22 39.44 53.19
RaSA 93.23 0.00 85.28 66.38 90.24 84.48 49.82 81.12 40.85 65.71
AdaLoRA 90.37 0.00 82.29 66.38 85.97 81.31 47.65 5.69 39.44 55.46
MELoRA 94.38 53.18 86.70 84.08 91.97 86.57 68.95 88.87 39.44 77.13
DenseLoRA 94.04 50.99 86.15 66.38 91.70 85.59 49.46 86.41 50.70 73.49
RandLoRA 92.66 0.00 84.88 66.38 89.12 84.03 51.99 80.68 39.44 65.46
ReLoRA 93.46 52.74 85.09 66.38 89.89 87.23 49.46 83.39 50.70 73.15


**Optimization** **Process** **Adjustment** **Based** **LoRA** **Variants**
DoRA 93.23 32.03 85.73 66.38 90.60 84.90 49.10 82.89 43.66 69.84
RsLoRA 94.27 48.15 86.51 68.58 91.45 85.96 54.15 86.16 47.89 73.68
LoRA+ 94.38 56.06 87.31 84.81 92.44 87.58 71.12 89.53 42.25 78.39
DeLoRA 91.86 0.00 84.66 66.38 89.08 83.22 49.10 76.11 40.85 64.58


**Initialization** **Adjustment** **Based** **LoRA** **Variants**
EVA 94.38 51.11 86.06 75.96 91.83 85.57 61.01 86.38 43.66 75.11
PiSSA 93.12 50.70 86.42 73.03 91.51 86.23 58.48 86.68 47.89 74.90
LoRAGA 94.61 54.87 87.09 85.72 92.44 86.97 69.68 88.30 36.62 77.37
LoRA-One 93.23 35.74 85.79 66.38 90.68 84.91 48.01 82.91 56.34 71.55
NZLoRA 93.58 50.87 86.42 67.85 91.55 85.76 60.29 85.52 45.07 74.10


**Mixture-of-Experts** **Integration** **Based** **Variants**
GOAT 93.12 0.00 85.64 66.38 90.41 85.33 51.26 81.28 49.30 66.97
MoSLoRA 93.35 18.30 85.58 66.38 90.62 84.73 49.10 81.44 38.03 67.50
LoRAMoE 93.35 48.07 85.63 69.49 92.02 86.06 66.06 88.75 36.62 74.01


TABLE VI
PERFORMANCE COMPARISON ON THE GLUE BENCHMARK WITH A LEARNING RATE OF 5E-5.


Method SST-2 CoLA MNLI MRPC QNLI QQP RTE STS-B WNLI AVG


LoRA 94.38 55.25 87.67 85.60 92.35 87.37 67.51 89.37 49.30 78.76


**Rank** **Adjustment** **Based** **LoRA** **Variants**
HiRA 92.09 0.00 84.36 66.38 88.93 83.58 48.38 47.79 40.85 61.37
RaSA 93.92 54.32 87.76 84.38 92.44 87.15 66.79 89.48 46.48 78.08
AdaLoRA 93.23 40.03 86.11 66.38 90.45 85.12 47.65 82.10 39.44 70.06
MELoRA 93.46 56.25 85.89 84.93 91.19 86.67 75.81 90.57 29.58 77.15
DenseLoRA 94.38 58.05 87.81 86.70 92.61 87.88 69.68 90.30 49.30 79.63
RandLoRA 92.89 48.94 87.09 81.70 92.27 86.82 62.45 86.94 35.21 74.92
ReLoRA 94.61 55.08 87.07 85.17 92.06 89.48 70.04 88.62 56.34 79.83


**Optimization** **Process** **Adjustment** **Based** **LoRA** **Variants**
DoRA 94.38 52.44 87.73 85.36 92.39 87.37 68.23 89.42 49.30 78.51
RsLoRA 94.61 54.98 87.67 85.72 92.73 88.07 72.92 90.39 46.48 79.29
LoRA+ 94.95 60.57 87.28 86.52 92.39 87.89 74.73 90.82 25.35 77.83
DeLoRA 93.92 52.37 86.57 83.53 91.59 86.14 59.57 84.65 45.07 75.93


**Initialization** **Adjustment** **Based** **LoRA** **Variants**
EVA 94.04 56.02 87.42 85.23 92.42 87.46 72.92 90.53 33.80 77.76
PiSSA 93.92 57.29 87.38 86.21 92.08 87.75 70.40 89.73 39.44 78.24
LoRAGA 93.35 59.07 87.34 86.33 92.73 87.27 76.17 90.29 33.80 78.48
LoRA-One 94.15 55.79 87.77 84.62 92.71 87.35 70.76 89.28 59.15 80.18
NZLoRA 94.27 56.58 87.07 85.85 92.40 87.74 74.01 89.95 30.99 77.65


**Mixture-of-Experts** **Integration** **Based** **Variants**
GOAT 94.04 55.23 86.83 83.71 92.46 87.43 56.68 88.91 53.52 77.65
MoSLoRA 94.27 53.82 87.47 85.17 92.20 87.24 70.04 89.12 46.48 78.42
LoRAMoE 93.00 53.91 85.55 85.72 91.72 86.02 70.76 90.37 25.35 75.82


JOURNAL OF L [A] TEX CLASS FILES, VOL. 18, NO. 9, SEPTEMBER 2020 29


TABLE VII
PERFORMANCE COMPARISON ON THE GLUE BENCHMARK WITH A LEARNING RATE OF 1E-4.


Method SST-2 CoLA MNLI MRPC QNLI QQP RTE STS-B WNLI AVG


LoRA 94.27 55.99 87.70 86.58 92.75 88.17 73.29 90.29 47.89 79.66


**Rank** **Adjustment** **Based** **LoRA** **Variants**
HiRA 93.23 0.00 85.72 66.38 90.64 85.14 49.82 80.68 39.44 65.67
RaSA 93.81 57.27 87.74 85.60 92.42 87.83 73.29 90.11 49.30 79.71
AdaLoRA 93.81 49.69 87.27 66.38 92.14 86.68 49.82 86.94 39.44 72.46
MELoRA 92.43 53.38 85.11 84.38 91.13 85.22 69.68 90.24 56.34 78.66
DenseLoRA 93.81 59.57 87.47 87.00 92.78 88.64 75.45 90.59 47.89 80.36
RandLoRA 93.81 51.71 87.35 85.23 92.46 87.70 68.95 88.83 35.21 76.81
ReLoRA 94.72 58.35 87.67 87.19 92.69 87.50 71.12 89.88 56.34 80.61


**Optimization** **Process** **Adjustment** **Based** **LoRA** **Variants**
DoRA 94.15 56.29 87.63 86.39 92.58 88.13 72.56 90.33 45.07 79.24
RsLoRA 94.27 57.78 87.25 85.30 92.46 88.27 73.65 91.04 38.03 78.67
LoRA+ 93.58 61.82 86.56 86.58 92.40 86.01 52.71 90.87 40.85 76.82
DeLoRA 94.38 52.42 87.11 85.30 92.29 86.95 66.79 87.13 43.66 77.34


**Initialization** **Adjustment** **Based** **LoRA** **Variants**
EVA 94.15 58.81 87.51 85.48 92.29 88.18 75.09 90.75 25.35 77.51
PiSSA 93.92 59.81 87.24 86.70 92.37 88.10 76.90 90.27 28.17 78.16
LoRAGA 92.55 57.54 86.16 85.66 91.70 86.77 72.56 90.25 56.34 79.95
LoRA-One 94.38 55.51 87.89 85.42 92.86 87.91 74.37 90.17 52.11 80.07
NZLoRA 94.04 59.05 87.27 86.15 91.93 87.77 72.20 90.20 25.35 77.11


**Mixture-of-Experts** **Integration** **Based** **Variants**
GOAT 94.04 53.64 86.99 85.72 92.10 87.25 69.31 89.56 47.89 78.50
MoSLoRA 94.95 55.49 87.62 86.82 92.67 87.88 72.56 90.22 47.89 79.57
LoRAMoE 91.97 56.25 32.74 84.26 90.24 0.00 71.84 90.39 23.94 60.18


TABLE VIII
PERFORMANCE COMPARISON ON THE GLUE BENCHMARK WITH A LEARNING RATE OF 5E-4.


Method SST-2 CoLA MNLI MRPC QNLI QQP RTE STS-B WNLI AVG


LoRA 93.23 61.58 87.12 86.15 92.23 0.00 78.34 91.00 28.17 68.65


**Rank** **Adjustment** **Based** **LoRA** **Variants**
HiRA 94.04 55.47 87.15 84.81 92.58 87.79 64.98 87.77 40.85 77.27
RaSA 94.04 60.32 87.11 86.94 92.42 88.50 75.81 90.88 56.34 81.37
AdaLoRA 93.35 58.06 87.25 87.19 92.76 88.26 70.76 90.31 36.62 78.29
MELoRA 50.92 0.00 32.74 66.38 50.63 0.00 52.71 0.00 56.34 34.26
DenseLoRA 93.35 60.82 31.82 87.37 92.08 0.00 52.71 91.01 28.17 59.70
RandLoRA 94.15 57.53 86.82 87.00 92.35 88.15 75.81 90.53 22.54 77.21
ReLoRA 93.58 55.48 84.49 86.09 91.83 86.83 52.71 91.05 56.34 77.60


**Optimization** **Process** **Adjustment** **Based** **LoRA** **Variants**
DoRA 93.58 62.35 86.56 87.25 92.42 85.52 76.53 90.94 28.17 78.15
RsLoRA 50.92 60.58 32.74 84.81 50.63 0.00 72.92 90.85 56.34 55.53
LoRA+ 50.92 0.00 32.74 66.38 49.37 0.00 52.71 10.57 56.34 35.45
DeLoRA 94.27 59.05 87.50 86.64 92.42 87.97 72.20 89.81 28.17 77.56


**Initialization** **Adjustment** **Based** **LoRA** **Variants**
EVA 92.66 59.05 86.81 84.81 91.63 0.00 52.71 90.72 56.34 68.30
PiSSA 50.92 0.00 32.74 83.89 50.63 0.00 52.71 89.49 56.34 46.30
LoRAGA 50.92 0.00 31.82 66.38 49.37 0.00 47.29 5.15 56.34 34.14
LoRA-One 93.69 62.07 86.95 87.37 92.01 0.00 78.34 90.65 29.58 68.96
NZLoRA 50.92 0.00 32.74 85.42 50.63 0.00 52.71 89.66 56.34 46.49


**Mixture-of-Experts** **Integration** **Based** **Variants**
GOAT 50.92 0.00 32.74 85.17 49.37 0.00 52.71 89.29 30.99 43.47
MoSLoRA 93.23 59.56 87.00 85.36 92.12 88.29 76.53 90.72 35.21 78.67
LoRAMoE 50.92 0.00 32.74 66.38 49.37 0.00 52.71 1.29 43.66 33.01


JOURNAL OF L [A] TEX CLASS FILES, VOL. 18, NO. 9, SEPTEMBER 2020 30


TABLE IX
PERFORMANCE COMPARISON ON THE GLUE BENCHMARK WITH A LEARNING RATE OF 1E-3.


Method SST-2 CoLA MNLI MRPC QNLI QQP RTE STS-B WNLI AVG


LoRA 50.92 0.00 32.74 86.33 49.37 0.00 52.71 89.35 30.99 43.60


**Rank** **Adjustment** **Based** **LoRA** **Variants**
HiRA 93.69 57.27 86.89 86.94 92.23 88.52 72.92 89.76 47.89 79.57
RaSA 93.00 0.00 87.27 86.46 92.25 0.00 77.98 90.90 28.17 61.78
AdaLoRA 93.81 61.57 87.33 86.76 92.12 88.27 76.53 90.53 40.85 79.75
MELoRA 50.92 0.00 31.82 66.38 49.37 0.00 52.71 0.00 43.66 32.55
DenseLoRA 50.92 0.00 32.74 66.38 50.63 0.00 52.71 0.00 56.34 34.18
RandLoRA 93.58 56.50 86.59 87.37 91.19 87.13 77.98 90.65 25.35 77.37
ReLoRA 50.92 15.54 35.45 66.38 50.63 38.72 52.71 88.51 56.34 50.58


**Optimization** **Process** **Adjustment** **Based** **LoRA** **Variants**
DoRA 50.92 58.83 32.74 66.38 50.63 0.00 52.71 89.39 32.39 48.22
RsLoRA 50.92 0.00 35.45 66.38 49.37 0.00 52.71 89.94 56.34 44.57
LoRA+ 50.92 0.00 32.74 66.38 49.37 0.00 52.71 13.26 56.34 35.75
DeLoRA 93.81 61.09 87.72 86.58 92.50 88.23 68.95 89.74 30.99 77.73


**Initialization** **Adjustment** **Based** **LoRA** **Variants**
EVA 50.92 0.00 35.45 66.38 49.37 0.00 52.71 89.70 56.34 44.54
PiSSA 50.92 0.00 32.74 66.38 50.63 0.00 52.71 7.96 56.34 35.30
LoRAGA 50.92 0.00 31.82 66.38 49.37 0.00 47.29 0.00 56.34 33.20
LoRA-One 50.92 0.00 32.74 85.91 49.37 0.00 52.71 90.79 38.03 44.50
NZLoRA 50.92 0.00 32.74 66.38 50.63 0.00 47.29 88.46 56.34 43.64


**Mixture-of-Experts** **Integration** **Based** **Variants**
GOAT 50.92 0.00 32.74 66.38 49.37 0.00 52.71 2.65 56.34 34.57
MoSLoRA 94.04 60.07 87.32 86.39 92.33 87.76 52.71 89.55 53.52 78.19
LoRAMoE 50.92 0.00 32.74 66.38 49.37 0.00 52.71 0.40 43.66 32.91


TABLE X
PERFORMANCE COMPARISON ON THE GLUE BENCHMARK WITH A LEARNING RATE OF 5E-3.


Method SST-2 CoLA MNLI MRPC QNLI QQP RTE STS-B WNLI AVG


LoRA 50.92 0.00 32.74 66.38 49.37 0.00 52.71 0.00 56.34 34.18


**Rank** **Adjustment** **Based** **LoRA** **Variants**
HiRA 90.37 59.12 32.74 86.82 49.37 0.00 79.78 90.69 23.94 56.98
RaSA 50.92 0.00 32.74 66.38 50.63 0.00 52.71 0.00 43.66 32.73
AdaLoRA 50.92 60.08 32.74 86.03 50.63 0.00 52.71 0.00 54.93 42.99
MELoRA 50.92 0.00 32.74 66.38 49.37 0.00 52.71 0.10 56.34 34.28
DenseLoRA 50.92 0.00 31.82 66.38 49.37 0.00 52.71 0.23 56.34 34.20
RandLoRA 50.92 0.00 31.82 66.38 50.63 0.00 52.71 0.00 56.34 33.21
ReLoRA 50.92 62.40 35.45 66.38 50.63 38.72 52.71 2.52 56.34 46.23


**Optimization** **Process** **Adjustment** **Based** **LoRA** **Variants**
DoRA 50.92 0.00 32.74 66.38 49.37 0.00 52.71 0.00 43.66 32.82
RsLoRA 50.92 0.00 32.74 66.38 49.37 0.00 52.71 0.34 43.66 32.90
LoRA+ 50.92 0.00 32.74 66.38 49.37 0.00 52.71 1.23 43.66 33.00
DeLoRA 94.15 0.00 87.07 66.38 92.63 88.24 47.29 0.00 56.34 58.71


**Initialization** **Adjustment** **Based** **LoRA** **Variants**
EVA 50.92 0.00 32.74 66.38 49.37 0.00 52.71 0.00 56.34 34.18
PiSSA 50.92 0.00 32.74 66.38 49.37 0.00 52.71 0.00 43.66 32.62
LoRAGA 50.92 0.00 32.74 66.38 49.37 0.00 52.71 2.97 43.66 33.19
LoRA-One 50.92 0.00 35.45 66.38 49.37 0.00 52.71 2.89 43.66 33.49
NZLoRA 50.92 0.00 32.74 66.38 49.37 0.00 52.71 0.98 43.66 32.97


**Mixture-of-Experts** **Integration** **Based** **Variants**
GOAT 50.92 0.00 35.45 66.38 49.37 0.00 52.71 1.60 43.66 33.34
MoSLoRA 50.92 0.00 32.74 66.38 49.37 0.00 52.71 0.00 56.34 34.27
LoRAMoE 50.92 0.00 32.74 66.38 50.63 0.00 52.71 0.80 56.34 34.50


JOURNAL OF L [A] TEX CLASS FILES, VOL. 18, NO. 9, SEPTEMBER 2020 31


TABLE XI
PERFORMANCE ON THE SEVEN IMAGE CLASSIFICATION TASKS WITH A LEARNING RATE OF 1E-6.


Method Cars DTD EuroSAT GTSRB RESISIC45 SUN397 SVHN AVG


LoRA 65.58 47.39 73.69 44.00 65.16 65.30 62.01 54.22


**Rank** **Adjustment** **Based** **LoRA** **Variants**
HiRA 63.96 42.87 40.74 69.00 56.71 62.76 13.91 40.23
RaSA 65.25 46.54 66.72 36.00 63.32 64.87 53.01 51.44
AdaLoRA 63.89 42.87 40.44 69.00 56.63 62.75 13.75 40.15
MELoRA 71.60 63.30 96.93 39.59 86.27 69.90 92.75 74.33
DenseLoRA 66.24 50.00 79.13 69.00 67.52 66.65 71.05 57.33
RandLoRA 66.70 49.95 84.31 1.18 69.03 65.79 74.47 58.78
ReLoRA 65.44 46.60 70.44 0.39 63.98 64.91 55.38 52.45


**Optimization** **Process** **Adjustment** **Based** **LoRA** **Variants**
DoRA 65.64 47.93 74.94 48.00 65.51 65.46 63.82 54.83
RsLoRA 67.35 52.13 87.39 3.06 70.87 67.30 79.54 61.09
LoRA+ 74.31 70.64 97.39 63.65 89.30 71.83 94.48 80.23
DeLoRA 64.92 44.79 59.07 37.00 60.94 63.73 36.37 47.17


**Initialization** **Adjustment** **Based** **LoRA** **Variants**
EVA 69.53 58.35 94.89 22.64 81.17 68.71 89.02 69.19
PiSSA 67.83 53.94 92.19 8.84 75.33 67.89 83.42 64.21
LoRA-GA 73.50 68.03 97.26 53.33 88.35 70.83 93.73 77.86
LoRA-One 18.70 46.65 61.65 2.47 51.97 62.66 63.39 43.93
NZLoRA 68.69 55.59 94.20 12.73 78.22 67.90 85.57 66.13


**Mixture-of-Experts** **Integration** **Based** **Variants**
GOAT 63.11 44.04 60.04 44.00 59.46 61.94 52.57 48.80
MoSLoRA 65.27 45.80 64.28 36.00 62.59 64.62 50.50 50.49
LoRAMoE 69.37 55.21 94.93 16.94 79.05 67.89 89.07 67.49


TABLE XII
PERFORMANCE ON THE SEVEN IMAGE CLASSIFICATION TASKS WITH A LEARNING RATE OF 1E-5.


Method Cars DTD EuroSAT GTSRB RESISIC45 SUN397 SVHN AVG


LoRA 71.79 66.28 96.93 40.40 86.37 70.59 93.38 75.11


**Rank** **Adjustment** **Based** **LoRA** **Variants**
HiRA 64.35 43.35 44.81 58.00 57.89 63.04 19.40 41.92
RaSA 70.73 63.03 96.22 29.46 84.56 69.89 92.29 72.31
AdaLoRA 64.64 45.32 50.83 44.00 60.33 63.88 47.41 47.55
MELoRA 80.74 75.05 98.35 96.85 94.75 76.16 96.29 88.31
DenseLoRA 74.38 71.76 97.28 63.28 89.25 71.82 94.12 80.27
RandLoRA 74.06 67.82 97.61 60.03 88.87 70.84 94.01 79.03
ReLoRA 70.39 62.34 96.13 29.06 84.41 69.71 92.38 72.06


**Optimization** **Process** **Adjustment** **Based** **LoRA** **Variants**
DoRA 72.18 66.44 97.06 42.59 86.81 70.73 93.48 75.61
RsLoRA 75.60 71.70 97.80 74.34 90.59 72.59 94.89 82.50
LoRA+ 83.32 77.66 98.50 98.17 95.22 77.56 96.91 89.62
DeLoRA 68.09 54.89 93.37 11.46 76.54 67.37 84.50 65.17


**Initialization** **Adjustment** **Based** **LoRA** **Variants**
EVA 78.51 74.79 98.06 91.71 92.56 73.97 95.72 86.47
PiSSA 75.36 69.52 97.83 76.98 91.03 72.72 95.06 82.64
LoRA-GA 82.33 75.53 98.52 96.96 94.70 76.01 96.49 88.65
LoRA-One 70.50 67.39 96.11 39.07 85.84 70.28 92.41 74.51
NZLoRA 77.70 72.82 98.26 85.82 92.25 73.36 95.55 85.11


**Mixture-of-Experts** **Integration** **Based** **Variants**
GOAT 71.40 66.65 96.48 48.87 87.49 69.36 92.91 76.17
MoSLoRA 70.69 63.09 96.09 30.37 84.48 69.92 92.36 72.43
LoRAMoE 78.72 72.02 98.15 91.92 92.70 74.26 95.62 86.20


JOURNAL OF L [A] TEX CLASS FILES, VOL. 18, NO. 9, SEPTEMBER 2020 32


TABLE XIII
PERFORMANCE ON THE SEVEN IMAGE CLASSIFICATION TASKS WITH A LEARNING RATE OF 2E-5.


Method Cars DTD EuroSAT GTSRB RESISIC45 SUN397 SVHN AVG


LoRA 75.29 71.44 97.63 71.57 90.41 72.43 94.90 81.95


**Rank** **Adjustment** **Based** **LoRA** **Variants**
HiRA 64.83 44.68 53.80 40.00 60.19 63.69 35.93 46.22
RaSA 73.91 69.31 97.33 59.29 88.97 71.71 94.26 79.25
AdaLoRA 66.14 51.06 77.07 50.00 67.76 67.46 75.92 57.99
MELoRA 82.35 76.44 98.57 98.25 95.59 77.12 96.83 89.31
DenseLoRA 77.84 73.56 98.04 83.28 91.81 74.21 95.39 84.88
RandLoRA 77.50 73.62 98.20 83.22 91.75 72.79 95.31 84.63
ReLoRA 73.45 69.41 97.33 59.98 88.49 71.26 94.19 79.16


**Optimization** **Process** **Adjustment** **Based** **LoRA** **Variants**
DoRA 75.59 71.81 97.80 73.37 90.56 72.61 94.98 82.39
RsLoRA 78.97 74.26 98.13 89.09 92.79 74.92 95.91 86.30
LoRA+ 85.95 79.68 98.76 98.77 95.71 78.45 97.28 90.66
DeLoRA 69.73 60.16 95.83 27.21 83.00 68.54 90.98 70.78


**Initialization** **Adjustment** **Based** **LoRA** **Variants**
EVA 81.05 76.17 98.37 96.75 94.30 75.43 96.34 88.34
PiSSA 77.95 71.17 98.30 89.37 92.90 74.52 95.91 85.73
LoRA-GA 84.17 77.13 98.52 98.34 95.63 76.89 96.85 89.65
LoRA-One 73.39 72.77 97.26 63.67 89.56 72.01 94.29 80.42
NZLoRA 80.13 74.47 98.41 95.42 94.11 75.48 96.17 87.74


**Mixture-of-Experts** **Integration** **Based** **Variants**
GOAT 76.48 72.34 97.54 78.95 91.30 72.21 6.70 70.79
MoSLoRA 74.05 70.05 97.19 63.17 89.27 71.81 94.25 79.97
LoRAMoE 79.42 74.26 98.20 95.86 94.29 75.75 96.01 87.68


TABLE XIV
PERFORMANCE ON THE IMAGE CLASSIFICATION TASKS WITH A LEARNING RATE OF 5E-5.


Method Cars DTD EuroSAT GTSRB RESISIC45 SUN397 SVHN AVG


LoRA 80.08 74.52 98.07 92.15 93.49 75.68 96.15 87.16


**Rank** **Adjustment** **Based** **LoRA** **Variants**
HiRA 65.89 50.64 77.04 53.00 67.22 66.16 70.83 56.90
RaSA 78.72 74.63 98.09 87.57 92.68 74.82 95.83 86.05
AdaLoRA 69.39 64.47 95.00 17.81 82.87 69.22 91.61 70.05
MELoRA 83.16 77.13 98.80 98.71 96.11 76.52 97.15 89.65
DenseLoRA 81.63 74.79 98.41 95.61 94.19 76.57 96.32 88.22
RandLoRA 81.61 75.74 98.54 95.99 94.48 75.71 96.40 88.35
ReLoRA 78.10 74.68 98.04 86.92 92.19 73.98 95.63 85.65


**Optimization** **Process** **Adjustment** **Based** **LoRA** **Variants**
DoRA 80.25 74.68 98.11 92.80 93.48 75.87 96.19 87.34
RsLoRA 82.08 75.74 98.35 97.11 94.81 77.10 96.62 88.83
LoRA+ 87.30 79.04 98.70 98.90 96.41 78.11 97.36 90.83
DeLoRA 73.24 68.51 97.15 62.95 88.73 70.76 93.85 79.31


**Initialization** **Adjustment** **Based** **LoRA** **Variants**
EVA 82.42 77.55 98.44 98.59 95.37 76.50 96.77 89.38
PiSSA 81.22 74.20 98.57 96.92 94.84 76.57 96.63 88.42
LoRA-GA 85.93 77.87 98.61 98.96 95.81 77.28 97.02 90.21
LoRA-One 78.46 75.43 98.11 91.14 92.89 75.11 95.89 86.72
NZLoRA 82.55 76.60 98.61 98.60 95.71 77.39 96.87 89.48


**Mixture-of-Experts** **Integration** **Based** **Variants**
GOAT 81.06 75.37 98.06 94.53 93.97 75.59 96.00 87.80
MoSLoRA 79.06 74.36 98.04 89.83 92.79 75.22 95.85 86.45
LoRAMoE 80.11 73.30 98.43 95.50 94.63 75.94 95.68 87.66


JOURNAL OF L [A] TEX CLASS FILES, VOL. 18, NO. 9, SEPTEMBER 2020 33


TABLE XV
PERFORMANCE ON SEVEN IMAGE CLASSIFICATION TASKS WITH A LEARNING RATE OF 1E-4.


Method Cars DTD EuroSAT GTSRB RESISIC45 SUN397 SVHN AVG


LoRA 82.22 75.85 98.41 97.08 94.67 77.18 96.58 88.86


**Rank** **Adjustment** **Based** **LoRA** **Variants**
HiRA 68.08 56.06 89.80 5.91 76.21 68.12 85.80 64.28
RaSA 81.52 76.01 98.26 96.36 94.11 76.79 96.36 88.49
AdaLoRA 73.29 74.31 97.06 58.87 88.51 71.76 94.21 79.72
MELoRA 82.66 74.84 98.57 98.68 95.59 74.59 96.98 88.84
DenseLoRA 83.80 77.18 98.43 97.87 95.22 77.37 96.75 89.52
RandLoRA 83.04 76.81 98.65 98.37 95.51 77.08 96.85 89.47
ReLoRA 81.18 76.44 98.30 95.56 93.92 76.04 96.31 88.25


**Optimization** **Process** **Adjustment** **Based** **LoRA** **Variants**
DoRA 82.20 76.01 98.41 97.22 94.70 77.27 96.64 88.92
RsLoRA 83.78 78.40 98.63 98.85 95.51 77.85 96.98 90.00
LoRA+ 87.40 72.71 98.70 98.84 95.54 76.61 96.91 89.53
DeLoRA 76.53 72.77 97.94 83.49 91.68 72.78 95.22 84.34


**Initialization** **Adjustment** **Based** **LoRA** **Variants**
EVA 83.99 77.45 98.33 98.74 95.79 77.07 97.07 89.78
PiSSA 83.34 77.66 98.67 98.27 95.63 77.10 97.00 89.67
LoRA-GA 85.04 75.74 98.61 98.80 95.57 76.49 96.94 89.60
LoRA-One 81.30 76.38 98.43 97.01 94.38 76.82 96.41 88.68
NZLoRA 84.77 78.72 98.72 99.07 96.00 78.20 97.09 90.37


**Mixture-of-Experts** **Integration** **Based** **Variants**
GOAT 82.43 75.59 98.26 96.53 95.03 76.82 96.25 88.70
MoSLoRA 81.81 76.01 98.35 96.56 94.32 76.75 96.39 88.60
LoRAMoE 77.85 72.23 97.26 89.53 92.06 73.31 91.88 84.87


TABLE XVI
PERFORMANCE ON THE SEVEN IMAGE CLASSIFICATION TASKS WITH A LEARNING RATE OF 2E-4.


Method Cars DTD EuroSAT GTSRB RESISIC45 SUN397 SVHN AVG


LoRA 84.07 78.62 98.57 98.50 95.52 77.90 97.02 90.03


**Rank** **Adjustment** **Based** **LoRA** **Variants**
HiRA 70.87 66.06 95.69 24.93 84.62 69.76 92.49 72.06
RaSA 83.17 77.50 98.50 98.11 95.29 77.63 96.73 89.56
AdaLoRA 78.12 75.05 97.65 86.07 91.94 74.75 95.72 85.61
MELoRA 79.34 70.00 98.37 98.14 94.14 69.75 96.12 86.55
DenseLoRA 85.75 78.40 98.70 98.45 95.90 78.35 97.08 90.38
RandLoRA 85.24 78.19 98.61 99.15 96.25 78.03 97.05 90.36
ReLoRA 82.84 78.46 98.44 97.80 94.98 77.06 96.78 89.48


**Optimization** **Process** **Adjustment** **Based** **LoRA** **Variants**
DoRA 84.12 77.77 98.65 98.76 95.59 77.88 97.06 89.98
RsLoRA 85.92 78.88 98.63 99.19 96.14 78.02 97.30 90.58
LoRA+ 1.12 4.84 70.54 23.14 10.21 3.15 19.59 18.94
DeLoRA 79.69 74.47 98.37 94.96 93.52 74.80 95.95 87.39


**Initialization** **Adjustment** **Based** **LoRA** **Variants**
EVA 83.92 76.22 98.56 98.53 95.81 76.63 96.98 89.52
PiSSA 85.09 78.30 98.83 98.69 95.73 77.22 97.07 90.13
LoRA-GA 82.74 71.44 98.43 98.72 94.81 73.43 96.96 88.08
LoRA-One 83.11 78.83 98.61 98.48 95.29 77.64 96.90 89.84
NZLoRA 85.66 77.98 98.80 98.82 96.22 77.52 97.36 90.34


**Mixture-of-Experts** **Integration** **Based** **Variants**
GOAT 83.46 77.45 98.56 97.18 95.32 77.39 96.62 89.43
MoSLoRA 83.34 77.39 98.46 98.12 95.46 77.75 96.86 89.63
LoRAMoE 1.41 9.26 56.19 20.92 16.17 1.43 19.59 17.85


JOURNAL OF L [A] TEX CLASS FILES, VOL. 18, NO. 9, SEPTEMBER 2020 34


TABLE XVII
PERFORMANCE ON THE SEVEN IMAGE CLASSIFICATION TASKS WITH A LEARNING RATE OF 5E-4.


Method Cars DTD EuroSAT GTSRB RESISIC45 SUN397 SVHN AVG


LoRA 86.78 78.62 98.74 98.93 96.27 78.68 97.20 90.75


**Rank** **Adjustment** **Based** **LoRA** **Variants**
HiRA 76.46 73.88 97.65 78.80 90.60 73.19 94.86 83.63
RaSA 86.36 78.62 98.59 98.94 96.05 78.68 97.16 90.63
AdaLoRA 81.77 76.86 98.48 96.99 94.16 77.08 96.53 88.84
MELoRA 2.46 11.06 74.24 39.00 38.25 6.01 20.44 27.35
DenseLoRA 87.10 78.72 98.83 99.17 96.32 79.01 97.41 90.94
RandLoRA 86.38 77.93 98.70 99.22 96.25 77.79 97.41 90.53
ReLoRA 85.59 79.31 98.67 98.49 95.90 77.82 97.07 90.41


**Optimization** **Process** **Adjustment** **Based** **LoRA** **Variants**
DoRA 86.72 78.94 98.61 99.06 96.05 78.82 97.27 90.78
RsLoRA 87.19 76.28 98.72 98.90 96.24 77.68 97.25 90.32
LoRA+ 1.11 3.24 33.13 9.90 9.44 1.23 19.72 11.11
DeLoRA 82.03 76.76 98.59 98.08 95.40 76.87 96.65 89.20


**Initialization** **Adjustment** **Based** **LoRA** **Variants**
EVA 83.17 73.62 98.41 98.40 95.62 75.15 97.13 88.79
PiSSA 85.10 73.67 98.48 98.77 95.56 75.53 97.15 89.18
LoRA-GA 77.12 60.53 97.52 98.20 93.17 65.33 96.44 84.04
LoRA-One 86.66 79.63 98.59 99.14 96.38 78.54 97.33 90.90
NZLoRA 83.92 71.54 98.57 98.74 95.54 73.31 96.83 88.35


**Mixture-of-Experts** **Integration** **Based** **Variants**
GOAT 84.33 77.23 98.28 96.30 94.86 76.38 28.61 79.43
MoSLoRA 85.23 78.56 98.63 98.75 96.06 78.31 97.10 90.38
LoRAMoE 87.00 4.41 59.41 6.98 11.98 1.02 19.59 14.89


TABLE XVIII
PERFORMANCE ON THE SEVEN IMAGE CLASSIFICATION TASKS WITH A LEARNING RATE OF 1E-3.


Method Cars DTD EuroSAT GTSRB RESISIC45 SUN397 SVHN AVG


LoRA 87.41 77.07 98.74 99.03 96.19 77.71 97.27 90.49


**Rank** **Adjustment** **Based** **LoRA** **Variants**
HiRA 80.94 75.64 98.24 93.79 93.33 75.85 96.05 87.69
RaSA 87.71 77.93 98.69 98.92 96.35 78.35 97.30 90.75
AdaLoRA 83.73 78.51 98.46 98.11 95.14 77.86 96.77 89.80
MELoRA 1.79 11.76 72.09 27.47 33.59 2.69 31.39 25.83
DenseLoRA 88.15 80.21 98.74 98.92 96.41 78.65 97.26 91.19
RandLoRA 86.03 74.57 98.70 99.30 96.14 75.84 97.39 89.71
ReLoRA 85.66 77.34 98.61 98.82 95.84 76.62 97.08 90.00


**Optimization** **Process** **Adjustment** **Based** **LoRA** **Variants**
DoRA 88.07 77.71 98.69 98.92 96.43 77.73 97.35 90.70
RsLoRA 86.46 72.29 98.57 98.50 95.57 75.52 96.52 89.06
LoRA+ 99.00 3.35 37.30 11.03 8.14 30.00 19.59 11.53
DeLoRA 83.83 78.03 98.65 98.73 95.92 77.34 97.07 89.94


**Initialization** **Adjustment** **Based** **LoRA** **Variants**
EVA 83.97 66.76 98.22 98.15 94.86 74.21 96.88 87.58
PiSSA 83.40 67.61 98.41 98.38 94.73 71.77 96.75 87.29
LoRA-GA 58.91 44.95 96.57 95.15 89.60 48.79 95.29 75.61
LoRA-One 87.53 77.29 98.69 98.52 96.38 78.03 97.19 90.52
NZLoRA 77.13 59.47 97.46 97.97 92.94 65.55 95.33 83.69


**Mixture-of-Experts** **Integration** **Based** **Variants**
GOAT 1.06 6.28 69.50 11.47 8.84 67.34 32.97 28.21
MoSLoRA 86.94 78.72 98.63 98.92 95.95 78.50 97.34 90.71
LoRAMoE 92.00 4.31 19.02 13.71 6.51 38.00 19.59 9.21


JOURNAL OF L [A] TEX CLASS FILES, VOL. 18, NO. 9, SEPTEMBER 2020 35


TABLE XIX
PERFORMANCE ON THE SEVEN IMAGE CLASSIFICATION TASKS WITH A LEARNING RATE OF 2E-3.


Method Cars DTD EuroSAT GTSRB RESISIC45 SUN397 SVHN AVG


LoRA 86.01 69.95 98.59 98.53 95.22 75.09 96.20 88.51


**Rank** **Adjustment** **Based** **LoRA** **Variants**
HiRA 83.16 77.07 98.39 97.46 94.71 77.35 96.70 89.26
RaSA 87.36 74.89 98.57 98.80 96.16 77.75 97.30 90.12
AdaLoRA 85.05 78.35 98.80 98.65 95.70 78.44 96.90 90.27
MELoRA 1.58 8.62 61.13 24.15 17.40 1.26 22.17 19.47
DenseLoRA 55.00 3.14 98.70 98.74 5.54 72.00 19.59 32.43
RandLoRA 82.37 67.82 98.28 99.18 95.06 70.66 97.03 87.20
ReLoRA 82.30 69.26 97.98 98.32 94.44 71.15 96.27 87.10


**Optimization** **Process** **Adjustment** **Based** **LoRA** **Variants**
DoRA 86.66 70.43 98.48 98.93 94.98 75.32 96.70 88.79
RsLoRA 1.83 5.32 56.26 22.32 14.03 65.00 32.10 18.93
LoRA+ 66.00 2.13 35.69 7.95 2.24 25.00 19.59 9.79
DeLoRA 85.00 78.78 98.70 98.76 95.86 78.06 97.19 90.34


**Initialization** **Adjustment** **Based** **LoRA** **Variants**
EVA 80.00 57.39 97.28 94.82 92.90 70.24 94.23 83.84
PiSSA 77.99 54.68 96.91 96.72 92.60 64.44 94.33 82.52
LoRA-GA 2.72 13.72 83.43 49.11 50.32 4.59 53.62 36.79
LoRA-One 86.47 71.65 98.30 98.48 95.32 75.50 95.95 88.81
NZLoRA 2.50 12.02 67.85 41.00 41.37 4.29 46.39 30.77


**Mixture-of-Experts** **Integration** **Based** **Variants**
GOAT 83.00 3.30 40.72 9.94 3.98 31.00 19.63 11.24
MoSLoRA 87.20 77.93 98.70 99.11 96.33 78.68 97.15 90.73
LoRAMoE 88.00 2.39 25.39 7.18 5.35 38.00 19.55 8.73


TABLE XX
PERFORMANCE ON IMAGE CLASSIFICATION TASKS WITH A LEARNING RATE OF 5E-3.


Method Cars DTD EuroSAT GTSRB RESISIC45 SUN397 SVHN AVG


LoRA 1.24 4.57 50.63 14.43 6.06 79.00 19.59 13.90


**Rank** **Adjustment** **Based** **LoRA** **Variants**
HiRA 85.45 79.10 98.67 98.73 96.19 78.78 97.28 90.60
RaSA 72.00 4.73 27.61 11.58 20.67 2.27 19.60 12.45
AdaLoRA 85.60 79.15 98.63 98.67 96.06 78.31 97.04 90.49
MELoRA 1.31 8.35 49.65 12.95 13.06 1.10 28.53 16.42
DenseLoRA 92.00 4.79 45.63 11.80 7.98 73.00 19.59 13.06
RandLoRA 70.51 51.65 97.19 98.50 91.35 55.24 95.77 80.03
ReLoRA 1.09 4.04 44.91 6.91 7.95 1.74 19.59 12.32


**Optimization** **Process** **Adjustment** **Based** **LoRA** **Variants**
DoRA 86.00 2.55 50.76 14.82 7.13 1.90 19.59 13.94
RsLoRA 72.00 5.80 31.15 10.93 13.44 34.00 22.60 12.14
LoRA+ 81.00 2.13 11.30 48.00 2.24 30.00 19.59 5.26
DeLoRA 86.25 79.36 98.78 98.60 96.13 78.51 97.36 90.71


**Initialization** **Adjustment** **Based** **LoRA** **Variants**
EVA 91.00 4.10 41.96 10.97 19.57 1.26 19.62 14.06
PiSSA 1.14 5.21 49.93 19.82 7.49 1.21 38.00 17.54
LoRA-GA 1.82 10.96 59.17 25.63 16.32 1.48 35.63 21.57
LoRA-One 67.00 5.59 48.48 5.98 8.43 72.00 27.11 13.85
NZLoRA 95.00 5.48 57.37 13.08 11.60 69.00 33.16 17.48


**Mixture-of-Experts** **Integration** **Based** **Variants**
GOAT 88.00 2.45 24.76 6.12 3.46 30.00 19.59 8.22
MoSLoRA 95.00 6.54 57.85 15.85 9.44 74.00 32.67 17.72
LoRAMoE 88.00 2.93 23.35 9.91 4.19 27.00 19.59 8.73


JOURNAL OF L [A] TEX CLASS FILES, VOL. 18, NO. 9, SEPTEMBER 2020 36


TABLE XXI
PERFORMANCE ON GSM8K.


Method 1e-6 1e-5 2e-5 5e-5 1e-4 2e-4 5e-4 1e-3


LoRA 52.84 64.37 66.94 70.13 73.16 72.86 75.51 72.10


**Rank** **Adjustment** **Based** **LoRA** **Variants**
HiRA 6.44 7.44 30.02 49.73 54.81 62.09 66.49 72.10
RaSA 48.98 61.87 63.84 68.92 71.04 72.48 73.31 74.30
AdaLoRA 5.84 34.65 49.32 59.51 61.49 65.58 70.35 71.72
MELoRA 62.55 71.72 72.02 70.36 64.52 57.01 1.74 2.05
DenseLoRA 50.19 63.76 67.85 68.84 72.86 72.33 74.22 74.75
RandLoRA 46.32 64.75 68.92 74.22 74.53 75.59 71.27 65.43
ReLoRA 55.04 65.81 69.6 71.87 71.65 67.17 41.93 1.52


**Optimization** **Process** **Adjustment** **Based** **LoRA** **Variants**
DoRA 54.69 64.67 67.25 71.80 73.09 74.15 74.53 72.25
RsLoRA 54.51 65.73 69.45 71.87 73.92 74.68 69.75 67.55
LoRA+ 60.12 70.28 72.02 74.68 75.59 72.25 64.67 1.59
DeLoRA 30.86 39.68 42.34 49.22 66.57 70.20 70.74 72.02


**Initialization** **Adjustment** **Based** **LoRA** **Variants**
EVA 60.12 69.67 71.87 71.49 73.09 73.84 74.30 71.65
PiSSA 57.39 69.14 71.27 72.18 72.86 72.71 71.11 64.67
LoRA-GA 64.06 70.36 70.51 72.02 71.95 67.63 64.22 48.45
LoRA-One 52.39 64.59 67.70 70.28 72.18 73.01 74.68 71.27
NZLoRA 53.68 63.76 67.63 71.87 73.31 71.27 70.81 64.22


**Mixture-of-Experts** **Integration** **Based** **Variants**
GOAT 48.98 67.25 67.63 68.84 71.65 71.27 52.39 2.12
MoSLoRA 48.52 63.31 66.03 69.37 69.98 72.71 74.00 74.68
LoRAMoE 46.32 67.93 69.83 69.22 59.97 34.60 1.67 1.52


TABLE XXII
PERFORMANCE ON HUMANEVAL.


Method 1e-6 1e-5 2e-5 5e-5 1e-4 2e-4 5e-4 1e-3


LoRA 9.30 41.31 41.46 44.82 45.27 48.09 48.17 42.07


**Rank** **Adjustment** **Based** **LoRA** **Variants**
HiRA 0.00 3.20 4.04 11.05 23.09 39.18 43.67 45.12
RaSA 6.48 40.47 43.67 42.91 46.04 47.71 49.31 49.31
AdaLoRA 0.08 4.19 7.24 26.52 39.25 41.62 45.73 44.74
MELoRA 18.14 45.81 45.88 42.45 35.59 26.45 0.00 0.00
DenseLoRA 7.77 38.41 42.61 45.05 45.20 46.19 48.02 46.72
RandLoRA 7.16 29.73 33.99 44.51 48.63 50.30 47.79 44.89
ReLoRA 44.21 44.97 47.03 42.07 30.26 10.44 1.07 0.00


**Optimization** **Process** **Adjustment** **Based** **LoRA** **Variants**
DoRA 9.07 42.99 42.91 46.34 46.72 46.57 47.18 44.74
RsLoRA 12.73 43.67 42.53 45.66 47.56 47.94 44.13 40.02
LoRA+ 28.28 47.64 46.57 46.04 46.19 44.36 37.35 0.00
DeLoRA 4.88 7.01 10.21 23.02 37.65 44.21 45.50 44.59


**Initialization** **Adjustment** **Based** **LoRA** **Variants**
EVA 15.55 39.63 46.42 46.49 45.43 45.20 45.96 44.89
PiSSA 7.01 28.51 26.14 45.20 45.66 47.41 41.54 35.37
LoRA-GA 37.04 44.59 44.28 45.96 46.65 43.75 39.41 30.72
LoRA-One 11.66 42.91 44.28 45.35 43.83 45.43 47.79 46.11
NZLoRA 7.16 24.70 36.74 45.81 46.80 47.64 46.27 39.10


**Mixture-of-Experts** **Integration** **Based** **Variants**
GOAT 5.49 42.53 43.83 45.58 46.19 45.05 0.00 0.00
MoSLoRA 5.79 43.06 44.97 46.04 45.27 47.79 46.49 46.80
LoRAMoE 9.91 45.05 43.05 43.45 37.20 0.00 0.00 0.00


