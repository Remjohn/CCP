## **LoRA vs Full Fine-tuning: An Illusion of Equivalence**

**Reece Shuttleworth** **Jacob Andreas** **Antonio Torralba** **Pratyusha Sharma**
MIT CSAIL
```
        {rshuttle, jda, torralba, pratyusha}@mit.edu

```

**Abstract**


Fine-tuning is a crucial paradigm for adapting pre-trained large language models
to downstream tasks. Recently, methods like Low-Rank Adaptation (LoRA) have
been shown to effectively fine-tune LLMs with an extreme reduction in trainable
parameters. But, _are_ _their_ _learned_ _solutions_ _really_ _equivalent?_ We study how
LoRA and full-finetuning change pre-trained models by analyzing the model’s
weight matrices through the lens of their spectral properties. We find that LoRA and
full fine-tuning yield weight matrices whose singular value decompositions exhibit
very different structure: weight matrices trained with LoRA have new, high-ranking
singular vectors, which we call _intruder dimensions_, while those trained with full
fine-tuning do not. Further, we extend the finding that LoRA forgets less than full
fine-tuning and find its forgetting is vastly localized to the intruder dimension –
by causally intervening on the intruder dimensions by changing their associated
singular values post-fine-tuning, we show that they cause forgetting. Moreover,
scaling them down significantly improves modeling of the pre-training distribution
with a minimal drop in downstream task performance. Given this, we should expect
accumulating intruder dimensions to be harmful and lead to more forgetting. This
will be amplified during continual learning because of sequentially fine-tuning,
and we show that LoRA models do accumulate intruder dimensions here tend to
perform worse in this setting, emphasizing the practicality of our findings.


**1** **Introduction**



Adapting large, pre-trained models to downstream tasks via fine-tuning is a computationand data-efficient way to create domain-specific
models for a variety of tasks. The simplest approach is to fine-tune all parameters of the pretrained model on downstream task data [Devlin
et al., 2019, Ouyang et al., 2022]. However, as
pre-trained models grow larger, full fine-tuning
becomes increasingly challenging and expensive. Recently, parameter-efficient fine-tuning
(PEFT) methods, especially low-rank adaptation
(LoRA; Hu et al., 2021), have been shown to
enable fine-tuning with only a fraction of the
trainable parameters. **While LoRA can match**
**full** **fine-tuning** **performance,** **are** **the** **solu-**
**tions learned by the two methods similar?**



Figure 1: **LoRA and full fine-tuning update the pa-**
**rameter space differently.** Similarity matricies of preand post-fine-tuning singular vectors for LLaMA2-7B
that characterize the spectral differences introduced during fine-tuning. Full fine-tuning retains most of the
pre-training structure, while LoRA has a diagonal shift.
Color shows cosine similarity.



While full fine-tuning treats every parameter as
trainable, LoRA treats the learned update to a weight matrix as the product of two low-rank matrices

[Hu et al., 2021]. While this parameterization is empirically effective, a principled explanation of


39th Conference on Neural Information Processing Systems (NeurIPS 2025).


Figure 2: **Characterizing structural differences between solutions learnt by LoRA & Full Fine-tuning.** **a)**
We measure the changes to the SVD of the pre-trained weights made during fine-tuning. We observe _intruder_
_dimensions_ introduced by LoRA in top ranking singular vectors but not by full fine-tuning. **b)** Comparing a
matrix fine-tuned with full fine-tuning or LoRA. **c)** The intruder dimension shows near-zero absolute cosine
similarity with all pre-trained singular vectors, in contrast to other singular vectors of the finetuned matrix.


the mechanism by which it matches the full fine-tuning performance has remained elusive. One
explanation is offered by the _intrinsic dimension hypothesis_ [Li et al., 2018, Aghajanyan et al., 2021],
which posits that the update learned via fine-tuning has a low intrinsic rank, suggesting that LoRA
might recover an approximately equivalent solution to full fine-tuning. However, prior work has
observed differences in the ability of LoRA and full fine-tuning to independently change the angle
and magnitude with which a neuron transforms its input [Liu et al., 2024]. Moreover, other work
has also observed that LoRA has difficulty matching the performance of full fine-tuning on difficult
tasks like code generation [Biderman et al., 2024, Zhuo et al., 2024] and long-form text generation

[Ivison et al., 2023]. Therefore, it is unclear if these findings indicate a limit in LoRA’s ability to fit
to a specific downstream task, or if these methods learn inherently different solutions.


In this paper, we show that full fine-tuning and LoRA learn different solutions with characteristic
differences in their spectral properties (as shown in Fig. 1 for LLaMA2-7B [Touvron et al., 2023b])
and that these spectral differences are causally related to different model behaviors. We observe:


1. **LoRA and full fine-tuning produce structurally different parameter updates, characterized**
**by the existence of** _**intruder dimensions**_ **in weight matrices tuned by LoRA** . Intruder dimensions
are singular vectors with large associated singular values that are very dissimilar to the singular
vectors in the pre-trained weight matrix. In contrast, fully fine-tuned models remain spectrally similar
to the pre-trained model and do not contain intruder dimensions.


2. **LoRA forgets less than full fine-tuning...but not always.** We extend the findings of Biderman
et al. [2024] that LoRA forgets less to the case _even_ when there is equal fine-tuning performance
between LoRA and full fine-tuning, showing that a difference in fit is not simply the cause of this
finding but rather is inherent to these methods. However, this is not always the case: despite nearly
identical fine-tuning task accuracies, we show that different selections of LoRA alpha and learning
rate lead to starkly different generalization behaviors, even leading to LoRA forgetting more than full
fine-tuning. We also find that models with the best generalization for each of these hyperparameter
settings have the fewest intruder dimensions.


3. **Intruder** **dimensions** **cause** **forgetting** **of** **the** **pre-training** **distribution.** Scaling down the
associated singular values of high-ranking intruder dimensions leads to a large drop in loss on the
pre-training distribution (forgetting) but only a minimal drop in test performance. The drop in
forgetting we observe when scaling down singular vectors is unique to intruder dimensions and
indicates that they interfere with the pre-trained language modeling ability of these models. Given
this finding, we should expect accumulating intruder dimensions to be harmful and lead to more
forgetting. To amplify this accumulation and examine its effect, we fine-tune in a continual learning


2


setting (sequentially fine-tuning on many tasks) and show that LoRA models do indeed tend to forget
more on previously learned tasks in this setting, providing additional support for our findings.


**2** **Background & Related Work**


**Methods for fine-tuning.** Pre-trained language models offer a foundation for downstream applications, eliminating the need to train from scratch [Ouyang et al., 2022, Devlin et al., 2019]. Full
fine-tuning, in which every parameter of a pre-trained model is updated, is commonly used [Devlin
et al., 2019, Liu et al., 2019]. Low Rank Adaptation (LoRA; Hu et al., 2021), which represents
the update to the weights as a product of two low-rank matrices, reduces computation and memory
requirements relative to full fine-tuning. Past work has shown that LoRA matches full fine-tuning
performance for tasks like sequence classification [Hu et al., 2021], instruction tuning [Dettmers
et al., 2023, Ghosh et al., 2024], and chat [Dettmers et al., 2023]. Other work has shown a gap in
performance on harder tasks like code generation [Biderman et al., 2024, Zhuo et al., 2024]. We
focus our investigation on both cases to ensure our findings generalize to all use cases.

**LoRA, formally.** Given a pre-trained weight matrix _W_ 0 _∈_ R _[m][×][n]_, full fine-tuning treats the learned
matrix update as ∆ _W_ _∈_ R _[m][×][n]_ . Instead, LoRA decomposes ∆ _W_ into a product of two matrices such
that ∆ _W_ = _BA_, where _B_ _∈_ R _[m][×][r]_, _A ∈_ R _[r][×][n]_, and where the rank _r_ is generally _r_ _≪_ _min_ ( _m, n_ ).
During prediction,

_Y_ = _WtunedX_ = ( _W_ 0 + _[α]_ _[.]_

_r_ _[BA]_ [)] _[X]_


_B_ is initialized to zero, and _A_ sampled from an isotropic Gaussian. All parameters in _B_ and _A_ are
trained. From this we can see that while full fine-tuning has _mn_ trainable parameters per weight
matrix, LoRA only has _mr_ + _rn_ . See Appendix E for derivation of LoRA adapter gradients.


**LoRA Variants.** Many variations of LoRA exist. Methods improve LoRA’s performance or memoryefficiency by initializing with the principal [Meng et al., 2024] or minor [Wang et al., 2024] components of the underlying weight matrix, training with quantization [Dettmers et al., 2023], adaptively
allocating different ranks [Zhang et al., 2023], or sequentially training multiple LoRAs [Xia et al.,
2024]. Other methods propose similar but alternative architectures [Liu et al., 2024, Kopiczko et al.,
2024, Koohpayegani et al., 2024]. Other work has also proposed low rank manipulations to the
activations instead of the weights [Wu et al., 2024]. Although the primary focus of our study is on
the original LoRA setup [Hu et al., 2021], we also study a few LoRA variants (Appendix O). While
we leave a rigorous analysis of all possible variants to future work, our preliminary experiments show
that our findings generalize to several variants. Additionally, we also demonstrate the robustness of
our findings across a range of LoRA hyperparameter settings (Appendices A.4, M, N).


**Analysis of Solutions.** The intrinsic dimension measure [Li et al., 2018] was used by Aghajanyan
et al. [2021] to argue that the fine-tuning update for a pre-trained LLM has low intrinsic rank,
explaining why only a small number of trainable parameters are necessary to reach 90% of full
fine-tuning performance. This finding motivated Hu et al. [2021] to hypothesize that LoRA works
because solutions of low intrinsic rank exist. But to our knowledge, no past work has compared
the rank (or other properties of weight matrices) between LoRA and full-fine tuning on tasks where
they are matched in performance. While Liu et al. [2024] showed that LoRA has difficulty changing
directional and magnitude components of a neuron independently, it is unclear if this difference is
due to an inability of LoRA to fit as well as full fine-tuning to the adaptation task.


**Relation to Biderman et al. [2024].** Recent work comparing LoRA to full fine-tuning has found
that LoRA forgets less when fine-tuned on math and code [Biderman et al., 2024] and more closely
resembles the pre-trained model [Ghosh et al., 2024]. We extend the findings of Biderman et al.

[2024] to the case when there is equal fine-tuning performance between LoRA and full fine-tuning,
showing that a difference in fit to the fine-tuning task is not simply the cause of this finding but rather
is inherent to these methods.

**Singular Value Decomposition.** The SVD decomposes a matrix _M_ _∈_ R _[m][×][n]_ such that _M_ = _U_ Σ _V_ _[T]_,
where _U_ _∈_ R _[m][×][m]_ and _V_ _∈_ R _[n][×][n]_ have orthonormal columns representing the singular vectors of
_M_ and Σ _∈_ R _[m][×][n]_ is a diagonal matrix containing the singular values of _M_ . _U_ and _V_ _[T]_ represent
rotations that matrix _M_ performs, while Σ represents scaling along those axes. Singular vectors,
ordered by singular values, reveal a matrix’s most important axes of transformation.


3


**3** **Structural Differences**


Inspired by Sharma et al. [2024]’s finding that
the singular value decomposition (SVD, Klema
and Laub, 1980) can be used to selectively prune
singular vectors to improve model performance,
this paper adopts the SVD of neural network parameters as a lens for understanding the changes
that fine-tuning makes to pre-trained weights.
Understanding how these dimensions change
can give us insight into how a particular finetuning method changes the pre-trained model.
In particular, we study how well singular vectors in weight matrices fine-tuned with LoRA
or full fine-tuning map to singular vectors in the
pre-trained weights (using cosine similarity).



Figure 3: **LoRA and full fine-tuning learn distinct**
**structural solutions.** LoRA introduces _intruder dimen-_
_sions_ (represented by outlined columns).



Visually, we observe in Fig. 2(b) that LoRA and full fine-tuning’s singular vectors have very different
similarities to the pre-trained singular vectors: singular vectors of models fine-tuned with LoRA
appear to have, on average, much lower cosine similarity to pre-trained singular vectors in comparison
to full fine-tuning. Interestingly, in LoRA fine-tuned models, we also observe the presence of high
ranking singular vectors with very low cosine similarity to any pre-trained singular vector. [1] In
Fig. 2(c), we show the difference between these vectors with low cosine similarity to the pre-trained
singular vectors and normal singular vectors from the fine-tuned weights. This “new” dimension can
be seen in Fig. 2(b) as the lone red dot in the bottom left corner. We name these “new” dimensions
_intruder dimensions_, which we define formally as follows:

**Definition** **3.1.** A singular vector _yj_ from the fine-tuned weight matrix _Wtuned_ is an **intruder**
**dimension** if and only if max _i_ ( _cos_ ( _yj, xi_ )) _<_ _ϵ_, where _ϵ_ is a similarity threshold and _xi_ are the
singular vectors of _W_ 0.



Examples of intruder dimensions may be seen
in Fig. 3. Here, we plot the similarity matrix
between the top 10 singular vectors (ranked by
singular value) in the pre-trained and fine-tuned
matrices. While full fine-tuning appears to have
a clear one-to-one mapping, LoRA appears to
have its mapping shifted by “blank” columns
(outlined in magenta): these are intruder dimensions, with low cosine similarity to every pretrained singular vector. A zoomed out version of
this plot can be seen in Fig. 1, in which we see
an off diagonal shift due to intruder dimensions.



**Require:** Pre-trained weights _W_ 0, fine-tuned
weights _W_ t, cosine similarity threshold _ϵ_, #
of fine-tuned singular vectors to examine _k_ .
1: [ _U_ 0 _,_ Σ0 _, V_ 0 _[⊤]_ []] _[ ←]_ [SVD][(] _[W]_ [0][)]
2: [ _Ut,_ Σ _t, Vt_ _[⊤]_ []] _[ ←]_ [SVD][(] _[W]_ [tuned][)]
3: n_intruders _←_ 0
4: _n ←_ # of pre-trained singular vectors
5: **for** _j_ _←_ 1 **to** _k_ **do**
6: **if** _∀i ≤_ _n_ : cos� _U_ 0[ _i_ ] _,_ _Ut_ [ _j_ ]� _< ϵ_ **then**
7: n_intruders _←_ n_intruders + 1
8: **end if**
9: **end for**
10: **return** n_intruders



**Algorithm 1** Finding intruder dimensions.



It is important to note that in the case of full
fine-tuning, the singular vectors that map to a 8: **end if**
pre-trained singular vector with high cosine sim- 9: **end for**
ilarity also have similar singular values. From 10: **return** n_intruders
these initial measurements, it appears that LoRA
and full fine-tuning have structural differences in the changes they make to the pre-trained weights:
while full fine-tuning appears to make small changes to the existing singular vectors and singular
values, LoRA introduces new singular vectors that have a large contribution to the norm of the
updated parameter matrix.


**Our Models.** We study LLaMA2-7B [Touvron et al., 2023b] and RoBERTa-base [Liu et al., 2019].
RoBERTa-base is a pre-trained encoder-only language model and we fine-tune it on six different
sequence classification tasks. See Appendix B.3 for fine-tuning details. LLaMA2-7B is a pre-trained
decoder-only language model, and we study it when fine-tuned on either code or math. These
checkpoints are provided by Biderman et al. [2024]. We also study LLaMA-7B [Touvron et al.,


1Recall that in high dimensions, a vector can have low cosine similarity to a set of orthogonal vectors that
span a space; see Appendix D for discussion.


4


(a) LLaMA-7B fine-tuned
on Alpaca.



(b) LLaMA2-7B fine-tuned on
MetaMathQA.



(c) LLaMA2-7B fine-tuned on
Magicoder-Evol-Instruct.



(d) Number of intruder dimensions in RoBERTa models fine-tuned on 6 different tasks.


Figure 4: **LoRA has intruder dimensions,** **whereas full fine-tuning does not.** Here, we set _k_ = 10 and
measure the impact of _ϵ_ on the number of intruder dimensions measured. LoRA introduces many intruder
dimensions in the top 10 ranked singular vectors, while full fine-tuning does not. Numbers are reported are the
sums across the entire model.


Figure 5: **Evolution of an intruder dimension across training steps.** _(Left)_ Intruder dimensions, and their
rank, in a LoRA fine-tuned weight matrix during fine-tuning. _(Middle)_ Their associated singular values, which
shows that the singular value associated with the intruder dimension increases. _(Right)_ Test accuracy across
training steps.


2023a] models fine-tuned on instruction following. See Appendix K for more details about these
models. Importantly, these LLaMA models span math, code, and chat, which are considerably harder
than sequence classification tasks. This ensures wide coverage of LoRA use cases.


**Our Method.** To calculate the number of intruder dimensions in a specific weight matrix, we use
Algorithm. 1. In it, we first compute the SVD of both the pre-trained and resulting LoRA and full
fine-tuned weights. Then, for each of the top _k_ highest-ranking singular vectors, we measure its
maximum cosine similarity with all of the pre-trained singular vectors. If this maximum cosine
similarity is less than some threshold _ϵ_, we classify this singular vector as an intruder dimension.
Note that both _k_, the number of fine-tuned singular vectors to examine, and _ϵ_, the cosine similarity
threshold, are hyperparameters; we verify the robustness of our findings for a wide range of _ϵ_ and
_k_ values in Fig. 4 and Fig. 15 respectively. To determine the number of intruder dimensions in a
specific model, we run this algorithm for each weight matrix in the model and sum the total.


**LoRA** **fine-tuned** **models** **contain** **high-ranking** **intruder** **dimensions** **while** **fully** **fine-tuned**
**models do not.** To characterize the differences in fine-tuning methods, we first evaluate the differences
in the total number of intruder dimensions in the top 10 highest-ranking singular vectors ( _k_ = 10). We
repeat this procedure for a range of _ϵ_ values, our cosine similarity threshold. The results are presented
in Fig. 4. For LLaMA2-7B, we find that models trained with LoRA contain intruder dimensions for
ranks at least as high as _r_ _≤_ 256. For RoBERTa, we consistently observe intruder dimensions for
rank _r_ _≤_ 16, even for low values of _ϵ_ . Interestingly, we observe that fully fine-tuned models, for
all model sizes, almost _never_ contain intruder dimensions in their top 10 singular vectors, even for
epsilon values of about 0.6 to 0.9. This means that full fine-tuning makes smaller changes to the same


5


set of high contribution pre-trained singular vectors, rather than introducing new singular vectors
like LoRA. Importantly, the number of intruder dimensions appears to drop as rank increases past a
certain threshold, suggesting that the low-rank nature, as well as the update rule of LoRA, induces
them to occur. This is underscored by the _r_ = 2048 case of LLaMA2-7B fine-tuned on math (Fig 4b),
which does not have intruder dimensions and instead has a very similar curve to full fine-tuning. As
rank increases past a threshold and LoRA begins to resemble a high rank update, intruder dimensions
begin to disappear.


**LoRA variants have intruder dimensions.** We examine 4 other LoRA variants to ensure that our
findings do not only apply to vanilla LoRA. We examine AdaLoRA [Zhang et al., 2023], LoRA+

[Hayou et al., 2024], PiSSA [Meng et al., 2024], and VeRA [Kopiczko et al., 2024]. In all of these
cases, we find intruder dimensions with similar characteristics to vanilla LoRA (see Fig. 23). This
shows our findings hold to other variants. For more discussion about these methods, see Appendix O.


**Intruder dimensions are distributed across both high and low singular values.** We examine
the extent to which intruder dimensions exist throughout the entire weight matrix and how they are
distributed. To do this, we hold _ϵ_ fixed and measure the number of intruder dimensions while varying
the proportion of the fine-tuned singular vectors that we examine (Appendix I, Fig. 15). Here, we can
see that LoRA consistently has more intruder dimensions than full fine-tuning, regardless of what
fraction of the singular values we examine. See Appendix I for more discussion.


**Intruder dimensions increase in magnitude and change in direction as fine-tuning progresses.**
To further understand how a particular intruder dimension is introduced during fine-tuning with
LoRA, we measure the maximum cosine similarity between the top individual fine-tuned singular
vectors and all the pre-trained singular vectors across many intermediate steps in the fine-tuning
process, as seen in Fig. 5 ( _left_ ). In parallel, we track changes in their associated singular values
as seen in Fig. 5 ( _middle_ ). As is evident from the graphs, intruder dimensions appear to gradually
increase their “rank" ( _left_ ) as their singular value is increased ( _middle_ ) while simultaneously changing
in direction too as training progresses.


**Additional empirical observations.** **1.** We find that the random seed used by LoRA to initialize
its adapters plays no role in the resulting structure (see Appendix N). **2.** We observe that the total
number of intruder dimensions increases linearly with respect to the size of the fine-tuning dataset up
to a certain point before saturating (Appendix J). **3.** We study the effective rank of these fine-tuning
updates (Appendix H). However, we find that this measure does not suffice to explain the behavioral
differences we observe in LoRA and full fine-tuning. Also, it is important to note that even if it had,
its global nature would prevent the precise examinations we conduct in future sections, like in Fig. 8.


**Experimental and theoretical justification for why intruder dimensions occur.** It is important
to note that intruder dimensions are an empirical observation of LoRA. We find that a variety of
factors play a role in the introduction of intruder dimensions. In the next section, we present results
that suggest that learning rate and LoRA’s _α_ contribute to intruder dimensions. In the appendix, we
present findings that suggest that tuning the B matrix only leads to fewer intruder dimensions (A.5),
and demonstrate how the addition of orthogonal vectors to the pre-trained weight matrix models the
introduction of intruder dimensions well (A.2).


**4** **Model Differences:** **Forgetting and Out-of-Distribution Generalization**


**LoRA forgets less.** We measure the change in out of distribution performance (forgetting) induced by
fine-tuning. For LLaMA2-7B, we follow Biderman et al. [2024] and measure forgetting as the average
score on Hellaswag [Zellers et al., 2019], WinoGrande [Sakaguchi et al., 2021], Arc-Challenge [Clark
et al., 2018]. For RoBERTa-base, we measure its “pseudo-loss”, which is analogous to language
modelling loss for encoder-only models, as described by Salazar et al. [2020] on a sample of its
pre-training dataset (as described by Liu et al. [2019]). Going forward, we refer to these values
as “forgetting” and report them in Fig. 6. We observe that across all tasks, full fine-tuning forgets
more of its pre-training language modeling ability in comparison to LoRA. Importantly, all our
RoBERTa-base models fine-tune to equivalent accuracy on the downstream task (Table 2). This
extends the finding that LoRA forgets less [Biderman et al., 2024] to the case where LoRA and full
fine-tuning have equal fit, showing that LoRA forgetting less is not simply a function of it underfitting
the fine-tuning task in comparison to full fine-tuning (like in Biderman et al. [2024]), but rather a
characteristic of LoRA itself.


6


(a) LLaMA2-7B. (b) RoBERTa-base.


Figure 6: **LoRA forgets less, even with same fit to fine-tuning task.** For LLaMA2-7B, forgetting is measured
on unrelated tasks, as described in Biderman et al. [2024]. For RoBERTa, Pseudo loss on a sample of its
pre-training distribution measured as described by Salazar et al. [2020]. In both, LoRA forgets less than full
fine-tuning.


Figure 7: **As training progresses, models with growing amount of intruder dimensions continue to forget**
**more, despite non-increasing test performance.** We also measure a strong correlation( _ρ_ = 0.971, p-value
_≪_ 0 _._ 001) between number of intruder dimensions and pre-training pseudo loss. Bigger learning rates lead to
more intruder dimensions and forgetting.


**LoRA** _α_ **impacts** **generalization** **and** **intruder** **dimensions.** For our experiments, we use the
commonly used _α_ = 2 _r_ [Biderman et al., 2024] as well as _α_ = 8 [Hu et al., 2021]. For both settings
of _α_, models obtain equivalent performance on the target task (Tables 1 & 2). However, when _α_ = 8,
all ranks of LoRA—even very large ones—exhibit intruder dimensions (Fig. 19a), have a much
smaller effective rank than when _α_ = 2 _r_ (Appendix H), and have much worse generalization (more
forgetting, Fig. 20). Models trained with _α_ = 2 _r_ have fewer intruder dimensions and generalize
better. This provides additional evidence highlighting the importance of using _α_ = 2 _r_ [Kalajdzievski,
2023, Biderman et al., 2024], particularly for higher ranks of LoRA.


**An increase in intruder dimensions leads to an increase in forgetting.** We do a learning rate sweep
for RoBERTa-base with LoRA _r_ = 8 on MNLI to observe its impact. Across epochs, we measure
the number of intruder dimensions, test accuracy, and forgetting (pre-training loss). We report the
results of these models and our baseline full fine-tuning model in Fig. 7. We observe that _across_
and _within_ training runs, as the number of intruder dimensions increase, forgetting (meaning worse
generalization) also increases. Test accuracy has no such relation. Separately, we see that for large
learning rates with many intruder dimensions, LoRA models _forget more_ than full fine-tuning. This
shows that while LoRA in general does forget less than full fine-tuning, it is not a guarantee.


**Intruder dimensions strongly correlate with forgetting.** When we measure the Spearman correlation between the number of intruder dimensions with forgetting in Fig. 7, we find an extremely strong
fit( _ρ_ = 0 _._ 971, p-value _≪_ 0 _._ 001). When measuring the same for our LLaMA2-7B models across
training epochs (Fig. 11), we still find a strong and still statistically significant relationship ( _ρ_ = 0 _._ 59,
p-value = 0 _._ 0006). In contrast, when measuring the correlation between intruder dimensions and test
accuracy, we find no statistically significant relationship: for RoBERTa, we measure _ρ_ = _−_ 0 _._ 3381 &
p-value = 0 _._ 218. For LLaMA2-7B, we measure _ρ_ = _−_ 0 _._ 3178 & p-value = 0 _._ 0869. See Appendix F
for more information. These results suggest that intruder dimensions are clearly linked with forgetting
but _are not necessary for performance._ We examine this claim and whether this relationship is causal
in the next section.


7


(a) LLaMA2-7B
on code with r=16.



(b) LLaMA2-7B
on math with r=16.



(c) RoBERTa-base
on MNLI with r=8.



(d) RoBERTa-base
on QQP with r=8.



Figure 8: **Scaling down intruder dimensions in fine-tuned models reduces forgetting but not performance.**
We scale the top intruder dimension in each matrix such that _W_ = _W_ 0 +∆ _W_ +( _λ_ _−_ 1) _uiσivi_ _[T]_ [.] [Lines represent]
forgetting (red) and learning (green). Dotted lines represent pre-trained baselines. **Axis Labels:** Green: Test
Accuracy (%). Red: Pre-training Loss (Forgetting).


**5** **Intruder Dimensions Cause Forgetting**


Previously, we observed that the number of intruder dimensions correlates strongly with forgetting.
_Do intruder dimensions cause this forgetting?_


**Scaling the magnitude of intruder dimensions.** To test if intruder dimensions _cause_ increased
forgetting, we must intervene on intruder dimensions and see the impact. We do this by finding the
highest ranked (by singular value) intruder dimension in each weight matrix and scale its contribution
such that the new weight matrix is _W_ = _W_ 0 + ∆ _W_ + ( _λ −_ 1) _uiσivi_ _[T]_ [, where] _[ i]_ [ is the index of the]
top intruder dimension ( _λ_ = 0 is removal and _λ_ = 1 is no change). We sweep _λ_ _[′]_ _s_ between 0 and 1,
scale the intruder dimensions, and measure test accuracy and pre-training loss. For a comparison
baseline, we select the neighbor of the intruder dimension to separately scale. See Fig. 8 for results
(and Figs. 12& 13 for full results.)


**Scaling down intruder dimensions reduces forgetting** . In Fig. 8, we show that when we scale down
the top intruder dimension of each weight matrix, we measure a significant reduction in forgetting
(pre-training loss) while incurring a minimal drop in test accuracy. For all examples in Fig. 8, we
observe that when using _λ_ = 0 _._ 7 or 0 _._ 9, there is almost no impact on fine-tuning performance, while
there is a large percentage drop in forgetting (See Tables 3&4). In one example for LLaMA2-7B
fine-tuned on MetaMath with LoRA _r_ = 256, we observe that scaling the top intruder dimension in
each matrix with _λ_ = 0 _._ 3 leads to a 0.1% drop in test accuracy and a 33.3% drop in the forgetting
induced by fine-tuning. In another for RoBERTa-base fine-tuned on QQP, using _λ_ = 0 _._ 7 leads to
equivalent in test accuracy and a 33.2% reduction in the forgetting induced by fine-tuning. In certain
scenarios, we even see test accuracy _improve_ along with a drop in forgetting. If we instead increase
their contribution ( _λ_ _>_ 1), we observe more forgetting. Across the board, scaling down intruder
dimensions seems to have little impact on test accuracy but a major impact on forgetting. This
pattern is exclusive to intruder dimensions (Fig. 12): if we instead intervene on pre-trained singular
vectors that have a similar singular value to the intruder dimension (ensuring similar contributions to
matrix) and scale their magnitude down, we see that forgetting goes up. These results indicate that
the forgetting observed in LoRA is caused by intruder dimensions interfering with the pre-trained
language modeling capabilities. Moreover, the scale (singular value) of these intruder dimensions is
not essential for the fine-tuning task performance. See Appendix G for further discussion.


**Continual Learning Setup.** To examine a practical example of how accumulating intruder dimensions, which cause forgetting, may impact performance, we study continual learning, since it requires
learning and remembering across a range of tasks. To do this, we train RoBERTa sequentially on
multiple tasks and measure performance as new tasks are learned. We use the same training recipe
and datasets as before but now sequentially in the following dataset order: MNLI, QQP, SST-2,
SIQA, WinoGrande, FEVER. After training on a certain dataset in the sequence, we merge the LoRA
weights into the model and reinitialize the LoRA adapter before training on the next task. After
training on a specific task, we test on all tasks by, for each task, separately retraining its classification
head before testing on its test set. Results are shown in Fig. 9a.


**Accumulating intruder dimensions hurts LoRA models during continual learning.** In Fig. 9a,
initially both LoRA and full fine-tuning train to equal performance (MNLI), which is consistent with


8


(a) Continual learning results.



(b) Similarity matrices for LoRA r=8 during continual learning.


(c) Similarity matrices for full fine-tuning during continual learning.



Figure 9: **Full fine-tuning is better than LoRA at continual learning because of accumulating intruder**
**dimensions.** When sequentially training on six tasks, full fine-tuning retains performance better than LoRA. in
Fig. 9a, horizontal dotted line indicates baseline pre-trained performance. Vertical solid line indicates when a
specific dataset is fine-tuned on. Gray region represents performance before the model has been trained on that
task. See Appendix L, Fig. 17 for more. In Figs. 9b&9c, we see that LoRA accumulates intruder dimensions
across tasks and contributes to its degrading performance, whereas full fine-tuning does not.


our previous observations. However, we observe that all ranks of LoRA degrade much more rapidly
than full fine-tuning. Low ranks of LoRA, which have the most intruder dimensions, degrade the
most. We attribute this divergence from earlier results—where LoRA appeared to forget less—to the
accumulation of intruder dimensions during continual learning, which drive forgetting. To show this,
we visualize how intruders are added across tasks in Fig. 9b. Here, we see that each task adds its own
intruder dimensions leading to a large amount of intruder dimensions upon the completion of the
six task continual learning experiment. In contrast, in Fig. 9c, we see that full fine-tuning retains the
pre-trained structure well justifying why full fine-tuning forgets less during continual learning.


**Implications and prescriptions in fine-tuning.** These findings suggest several implications and
prescriptions during LoRA fine-tuning. We have shown that intruder dimensions drive forgetting, and
therefore should be avoided when possible. Interestingly, this presents a data free model evaluation
method to examine which model is most overfit to the fine-tuning task (forgotten the most): given
two equally performing models on downstream test sets, you should select the one with fewer
intruder dimensions. Intruder dimensions appear to be a necessary part of fine-tuning, but they can
be mitigated. Further, these results show the danger of using LoRA during continual learning and
justifies using many different adapters without combining them, like advocated in Sheng et al. [2024].


**6** **Conclusion**


This paper describes the finding that LoRA and full fine-tuning update different parts of the parameter
space resulting in distinct spectral properties: LoRA often introduces intruder dimensions—highranking singular vectors dissimilar to those in pre-trained weights. These structural differences persist
across a series of ablations. Next, we find that models with fewer intruder dimensions exhibit better
out-of-distribution generalization and forget less of the pretraining distribution. Last, we show that
intruder dimensions _cause_ increased forgetting: We show that reducing the magnitude of high ranking
intruder dimensions leads to minimal changes in test performance but a large drop in pretraining
loss. We show that this is particularly relevant during continual training: even though LoRA forgets
less than full fine-tuning after training on one task, sequentially training leads to an accumulation of
intruder dimensions that causes more forgetting than full-finetuning.


9


**Acknowledgements**


We would like to thank Jacob Portes and Dan Biderman for corresponding with us and releasing
their LLaMA-2 7B checkpoints for us to use. This enabled us to study a more comprehensive range
of models. We would also like to thank Leshem Chosen, Lucas Hennigen, Han Guo, Vighnesh
Subramaniam, Valerio Pepe, and the entire Language & Intelligence lab for their helpful feedback
on this work. This research was supported in part by the National Science Foundation under grant
IIS-2238240.


**References**


Armen Aghajanyan, Sonal Gupta, and Luke Zettlemoyer. Intrinsic Dimensionality Explains the
Effectiveness of Language Model Fine-Tuning. In _Proceedings of the 59th Annual Meeting of the_
_Association for Computational Linguistics and the 11th International Joint Conference on Natural_
_Language Processing (Volume 1: Long Papers)_ . Association for Computational Linguistics, August
2021. URL `[https://aclanthology.org/2021.acl-long.568](https://aclanthology.org/2021.acl-long.568)` .


Loubna Ben Allal, Niklas Muennighoff, Logesh Kumar Umapathi, Ben Lipkin, and Leandro von
Werra. A framework for the evaluation of code generation models. `[https://github.com/](https://github.com/bigcode-project/bigcode-evaluation-harness)`
`[bigcode-project/bigcode-evaluation-harness](https://github.com/bigcode-project/bigcode-evaluation-harness)`, 2022.


Dan Biderman, Jose Gonzalez Ortiz, Jacob Portes, Mansheej Paul, Philip Greengard, Connor Jennings, Daniel King, Sam Havens, Vitaliy Chiley, Jonathan Frankle, Cody Blakeney, and John P.
Cunningham. LoRA Learns Less and Forgets Less. Transactions on Machine Learning Research,
2024. URL `[https://arxiv.org/abs/2405.09673](https://arxiv.org/abs/2405.09673)` .


Mark Chen, Jerry Tworek, Heewoo Jun, Qiming Yuan, Henrique Ponde de Oliveira Pinto, Jared
Kaplan, Harri Edwards, Yuri Burda, Nicholas Joseph, Greg Brockman, Alex Ray, Raul Puri,
Gretchen Krueger, Michael Petrov, Heidy Khlaaf, Girish Sastry, Pamela Mishkin, Brooke Chan,
Scott Gray, Nick Ryder, Mikhail Pavlov, Alethea Power, Lukasz Kaiser, Mohammad Bavarian,
Clemens Winter, Philippe Tillet, Felipe Petroski Such, Dave Cummings, Matthias Plappert, Fotios
Chantzis, Elizabeth Barnes, Ariel Herbert-Voss, William Hebgen Guss, Alex Nichol, Alex Paino,
Nikolas Tezak, Jie Tang, Igor Babuschkin, Suchir Balaji, Shantanu Jain, William Saunders,
Christopher Hesse, Andrew N. Carr, Jan Leike, Josh Achiam, Vedant Misra, Evan Morikawa,
Alec Radford, Matthew Knight, Miles Brundage, Mira Murati, Katie Mayer, Peter Welinder, Bob
McGrew, Dario Amodei, Sam McCandlish, Ilya Sutskever, and Wojciech Zaremba. Evaluating
large language models trained on code, 2021. URL `[https://arxiv.org/abs/2107.03374](https://arxiv.org/abs/2107.03374)` .


Peter Clark, Isaac Cowhey, Oren Etzioni, Tushar Khot, Ashish Sabharwal, Carissa Schoenick, and
Oyvind Tafjord. Think you have solved question answering? try arc, the ai2 reasoning challenge,
2018. URL `[https://arxiv.org/abs/1803.05457](https://arxiv.org/abs/1803.05457)` .


Karl Cobbe, Vineet Kosaraju, Mohammad Bavarian, Mark Chen, Heewoo Jun, Lukasz Kaiser,
Matthias Plappert, Jerry Tworek, Jacob Hilton, Reiichiro Nakano, Christopher Hesse, and John
Schulman. Training verifiers to solve math word problems, 2021. URL `[https://arxiv.org/](https://arxiv.org/abs/2110.14168)`
`[abs/2110.14168](https://arxiv.org/abs/2110.14168)` .


Tim Dettmers, Artidoro Pagnoni, Ari Holtzman, and Luke Zettlemoyer. QLoRA: Efficient Finetuning
of Quantized LLMs. In _Advances in Neural Information Processing Systems_, 2023.


Jacob Devlin, Ming-Wei Chang, Kenton Lee, and Kristina Toutanova. BERT: Pre-training of Deep
Bidirectional Transformers for Language Understanding. In _Proceedings of the 2019 Conference_
_of the North American Chapter of the Association for Computational Linguistics_ . Association for
Computational Linguistics, June 2019. URL `[https://aclanthology.org/N19-1423](https://aclanthology.org/N19-1423)` .


Leo Gao, Jonathan Tow, Baber Abbasi, Stella Biderman, Sid Black, Anthony DiPofi, Charles Foster,
Laurence Golding, Jeffrey Hsu, Alain Le Noac’h, Haonan Li, Kyle McDonell, Niklas Muennighoff,
Chris Ociepa, Jason Phang, Laria Reynolds, Hailey Schoelkopf, Aviya Skowron, Lintang Sutawika,
Eric Tang, Anish Thite, Ben Wang, Kevin Wang, and Andy Zou. The language model evaluation
harness, 07 2024. URL `[https://zenodo.org/records/12608602](https://zenodo.org/records/12608602)` .


10


Sreyan Ghosh, Chandra Kiran Reddy Evuru, Sonal Kumar, Ramaneswaran S, Deepali Aneja, Zeyu
Jin, Ramani Duraiswami, and Dinesh Manocha. A Closer Look at the Limitations of Instruction
Tuning. In _Proceedings of the 41st International Conference on Machine Learning_ . International
Conference on Machine Learning, 2024. URL `[https://arxiv.org/abs/2402.05119](https://arxiv.org/abs/2402.05119)` .


Aaron Gokaslan and Vanya Cohen. OpenWebText Corpus. `[http://Skylion007.github.io/](http://Skylion007.github.io/OpenWebTextCorpus)`
`[OpenWebTextCorpus](http://Skylion007.github.io/OpenWebTextCorpus)`, 2019.


Felix Hamborg, Norman Meuschke, Corinna Breitinger, and Bela Gipp. news-please: A Generic
News Crawler and Extractor. In _Proceedings of the 15th International Symposium of Information_
_Science_, pages 218–223, March 2017. doi: 10.5281/zenodo.4120316.


Yongchang Hao, Yanshuai Cao, and Lili Mou. Flora: Low-Rank Adapters Are Secretly Gradient Compressors. In _Proceedings of the 41st International Conference on Machine Learning_ . International
Conference on Machine Learning, 2024. URL `[https://arxiv.org/abs/2402.03293](https://arxiv.org/abs/2402.03293)` .


Soufiane Hayou, Nikhil Ghosh, and Bin Yu. LoRA+: Efficient Low Rank Adaptation of Large
Models, 2024. URL `[https://arxiv.org/abs/2402.12354](https://arxiv.org/abs/2402.12354)` .


Edward J. Hu, Yelong Shen, Phillip Wallis, Zeyuan Allen-Zhu, Yuanzhi Li, Shean Wang, Lu Wang,
and Weizhu Chen. LoRA: Low-Rank Adaptation of Large Language Models. International
Conference on Learning Representations, 2021.


Hamish Ivison, Yizhong Wang, Valentina Pyatkin, Nathan Lambert, Matthew Peters, Pradeep Dasigi,
Joel Jang, David Wadden, Noah A. Smith, Iz Beltagy, and Hannaneh Hajishirzi. Camels in a
Changing Climate: Enhancing LM Adaptation with Tulu 2, 2023. URL `[https://arxiv.org/](https://arxiv.org/abs/2311.10702)`
`[abs/2311.10702](https://arxiv.org/abs/2311.10702)` .


Damjan Kalajdzievski. A Rank Stabilization Scaling Factor for Fine-Tuning with LoRA, 2023. URL
`[https://arxiv.org/abs/2312.03732](https://arxiv.org/abs/2312.03732)` .


Diederik P. Kingma and Jimmy Ba. Adam: A method for stochastic optimization, 2017. URL
`[https://arxiv.org/abs/1412.6980](https://arxiv.org/abs/1412.6980)` .


V. Klema and A. Laub. The singular value decomposition: Its computation and some applications.
_IEEE Transactions on Automatic Control_, 25(2):164–176, 1980. doi: 10.1109/TAC.1980.1102314.


Soroush Abbasi Koohpayegani, KL Navaneet, Parsa Nooralinejad, Soheil Kolouri, and Hamed
Pirsiavash. NOLA: Compressing LoRA using Linear Combination of Random Basis. International
Conference on Learning Representations, 2024. URL `[https://arxiv.org/abs/2310.02556](https://arxiv.org/abs/2310.02556)` .


Dawid J. Kopiczko, Tijmen Blankevoort, and Yuki M. Asano. VeRA: Vector-based Random Matrix
Adaptation. International Conference on Learning Representations, 2024. URL `[https://arxiv.](https://arxiv.org/abs/2310.11454)`
`[org/abs/2310.11454](https://arxiv.org/abs/2310.11454)` .


Chunyuan Li, Heerad Farkhoor, Rosanne Liu, and Jason Yosinski. Measuring the Intrinsic Dimension
of Objective Landscapes. International Conference on Learning Representations, 2018. URL
`[https://arxiv.org/abs/1804.08838](https://arxiv.org/abs/1804.08838)` .


Raymond Li, Loubna Ben Allal, Yangtian Zi, Niklas Muennighoff, Denis Kocetkov, Chenghao Mou,
Marc Marone, Christopher Akiki, Jia Li, Jenny Chim, Qian Liu, Evgenii Zheltonozhskii, Terry Yue
Zhuo, Thomas Wang, Olivier Dehaene, Mishig Davaadorj, Joel Lamy-Poirier, João Monteiro,
Oleh Shliazhko, Nicolas Gontier, Nicholas Meade, Armel Zebaze, Ming-Ho Yee, Logesh Kumar
Umapathi, Jian Zhu, Benjamin Lipkin, Muhtasham Oblokulov, Zhiruo Wang, Rudra Murthy, Jason
Stillerman, Siva Sankalp Patel, Dmitry Abulkhanov, Marco Zocca, Manan Dey, Zhihan Zhang,
Nour Fahmy, Urvashi Bhattacharyya, Wenhao Yu, Swayam Singh, Sasha Luccioni, Paulo Villegas,
Maxim Kunakov, Fedor Zhdanov, Manuel Romero, Tony Lee, Nadav Timor, Jennifer Ding, Claire
Schlesinger, Hailey Schoelkopf, Jan Ebert, Tri Dao, Mayank Mishra, Alex Gu, Jennifer Robinson,
Carolyn Jane Anderson, Brendan Dolan-Gavitt, Danish Contractor, Siva Reddy, Daniel Fried,
Dzmitry Bahdanau, Yacine Jernite, Carlos Muñoz Ferrandis, Sean Hughes, Thomas Wolf, Arjun
Guha, Leandro von Werra, and Harm de Vries. Starcoder: may the source be with you!, 2023.
URL `[https://arxiv.org/abs/2305.06161](https://arxiv.org/abs/2305.06161)` .


11


Shih-Yang Liu, Chien-Yi Wang, Hongxu Yin, Pavlo Molchanov, Yu-Chiang Frank Wang, Kwang-Ting
Cheng, and Min-Hung Chen. DoRA: Weight-Decomposed Low-Rank Adaptation. In _Proceedings_
_of the 41st International Conference on Machine Learning_ . International Conference on Machine
Learning, 2024. URL `[https://arxiv.org/abs/2402.09353](https://arxiv.org/abs/2402.09353)` .


Yinhan Liu, Myle Ott, Naman Goyal, Jingfei Du, Mandar Joshi, Danqi Chen, Omer Levy, Mike Lewis,
Luke Zettlemoyer, and Veselin Stoyanov. RoBERTa: A Robustly Optimized BERT Pretraining
Approach, 2019. URL `[https://arxiv.org/abs/1907.11692](https://arxiv.org/abs/1907.11692)` .


Sourab Mangrulkar, Sylvain Gugger, Lysandre Debut, Younes Belkada, Sayak Paul, and Benjamin
Bossan. PEFT: State-of-the-art Parameter-Efficient Fine-Tuning methods. `[https://github.](https://github.com/huggingface/peft)`
`[com/huggingface/peft](https://github.com/huggingface/peft)`, 2022.


Fanxu Meng, Zhaohui Wang, and Muhan Zhang. PiSSA: Principal Singular Values and Singular
Vectors Adaptation of Large Language Models, 2024. URL `[https://arxiv.org/abs/2404.](https://arxiv.org/abs/2404.02948)`
`[02948](https://arxiv.org/abs/2404.02948)` .


Long Ouyang, Jeffrey Wu, Xu Jiang, Diogo Almeida, Carroll Wainwright, Pamela Mishkin, Chong
Zhang, Sandhini Agarwal, Katarina Slama, Alex Ray, John Schulman, Jacob Hilton, Fraser Kelton,
Luke Miller, Maddie Simens, Amanda Askell, Peter Welinder, Paul F Christiano, Jan Leike, and
Ryan Lowe. Training language models to follow instructions with human feedback. In _Advances_
_in Neural Information Processing Systems_, volume 35, 2022.


Keiran Paster, Marco Dos Santos, Zhangir Azerbayev, and Jimmy Ba. Openwebmath: An open dataset
of high-quality mathematical web text, 2023. URL `[https://arxiv.org/abs/2310.06786](https://arxiv.org/abs/2310.06786)` .


Olivier Roy and Martin Vetterli. The effective rank: A measure of effective dimensionality. In _2007_
_15th European Signal Processing Conference_, pages 606–610, 2007.


Keisuke Sakaguchi, Ronan Le Bras, Chandra Bhagavatula, and Yejin Choi. WinoGrande: an
adversarial winograd schema challenge at scale. _Commun. ACM_, 64(9):99–106, August 2021.
ISSN 0001-0782. doi: 10.1145/3474381. URL `[https://doi.org/10.1145/3474381](https://doi.org/10.1145/3474381)` .


Julian Salazar, Davis Liang, Toan Q. Nguyen, and Katrin Kirchhoff. Masked Language Model Scoring.
In _Proceedings_ _of_ _the_ _58th_ _Annual_ _Meeting_ _of_ _the_ _Association_ _for_ _Computational_ _Linguistics_ .
Association for Computational Linguistics, 2020. doi: 10.18653/v1/2020.acl-main.240. URL
`[http://dx.doi.org/10.18653/v1/2020.acl-main.240](http://dx.doi.org/10.18653/v1/2020.acl-main.240)` .


Maarten Sap, Hannah Rashkin, Derek Chen, Ronan Le Bras, and Yejin Choi. Social IQa: Commonsense Reasoning about Social Interactions. In Kentaro Inui, Jing Jiang, Vincent Ng, and Xiaojun
Wan, editors, _Proceedings of the 2019 Conference on Empirical Methods in Natural Language_
_Processing and the 9th International Joint Conference on Natural Language Processing (EMNLP-_
_IJCNLP)_, pages 4463–4473, Hong Kong, China, November 2019. Association for Computational
Linguistics. doi: 10.18653/v1/D19-1454. URL `[https://aclanthology.org/D19-1454](https://aclanthology.org/D19-1454)` .


Pratyusha Sharma, Jordan T. Ash, and Dipendra Misra. The Truth is in There: Improving Reasoning in
Language Models with Layer-Selective Rank Reduction. In _The Twelfth International Conference_
_on Learning Representations_, 2024. URL `[https://openreview.net/forum?id=ozX92bu8VA](https://openreview.net/forum?id=ozX92bu8VA)` .


Ying Sheng, Shiyi Cao, Dacheng Li, Coleman Hooper, Nicholas Lee, Shuo Yang, Christopher Chou,
Banghua Zhu, Lianmin Zheng, Kurt Keutzer, Joseph E. Gonzalez, and Ion Stoica. S-lora: Serving
thousands of concurrent lora adapters, 2024. URL `[https://arxiv.org/abs/2311.03285](https://arxiv.org/abs/2311.03285)` .


Richard Socher, Alex Perelygin, Jean Wu, Jason Chuang, Christopher D. Manning, Andrew Ng,
and Christopher Potts. Recursive Deep Models for Semantic Compositionality Over a Sentiment
Treebank. In David Yarowsky, Timothy Baldwin, Anna Korhonen, Karen Livescu, and Steven
Bethard, editors, _Proceedings_ _of_ _the_ _2013_ _Conference_ _on_ _Empirical_ _Methods_ _in_ _Natural_ _Lan-_
_guage Processing_, pages 1631–1642, Seattle, Washington, USA, October 2013. Association for
Computational Linguistics. URL `[https://aclanthology.org/D13-1170](https://aclanthology.org/D13-1170)` .


Rohan Taori, Ishaan Gulrajani, Tianyi Zhang, Yann Dubois, Xuechen Li, Carlos Guestrin, Percy
Liang, and Tatsunori B. Hashimoto. Stanford Alpaca: An Instruction-following LLaMA model.
`[https://github.com/tatsu-lab/stanford_alpaca](https://github.com/tatsu-lab/stanford_alpaca)`, 2023.


12


James Thorne, Andreas Vlachos, Christos Christodoulopoulos, and Arpit Mittal. FEVER: a Largescale Dataset for Fact Extraction and VERification. In Marilyn Walker, Heng Ji, and Amanda Stent,
editors, _Proceedings of the 2018 Conference of the North American Chapter of the Association_
_for Computational Linguistics:_ _Human Language Technologies, Volume 1 (Long Papers)_, pages
809–819, New Orleans, Louisiana, June 2018. Association for Computational Linguistics. doi:
10.18653/v1/N18-1074. URL `[https://aclanthology.org/N18-1074](https://aclanthology.org/N18-1074)` .


Hugo Touvron, Thibaut Lavril, Gautier Izacard, Xavier Martinet, Marie-Anne Lachaux, Timothée
Lacroix, Baptiste Rozière, Naman Goyal, Eric Hambro, Faisal Azhar, Aurelien Rodriguez, Armand
Joulin, Edouard Grave, and Guillaume Lample. LLaMA: Open and Efficient Foundation Language
Models, 2023a. URL `[https://arxiv.org/abs/2302.13971](https://arxiv.org/abs/2302.13971)` .


Hugo Touvron, Louis Martin, Kevin Stone, Peter Albert, Amjad Almahairi, Yasmine Babaei, Nikolay
Bashlykov, Soumya Batra, Prajjwal Bhargava, Shruti Bhosale, Dan Bikel, Lukas Blecher, Cristian Canton Ferrer, Moya Chen, Guillem Cucurull, David Esiobu, Jude Fernandes, Jeremy Fu,
Wenyin Fu, Brian Fuller, Cynthia Gao, Vedanuj Goswami, Naman Goyal, Anthony Hartshorn,
Saghar Hosseini, Rui Hou, Hakan Inan, Marcin Kardas, Viktor Kerkez, Madian Khabsa, Isabel
Kloumann, Artem Korenev, Punit Singh Koura, Marie-Anne Lachaux, Thibaut Lavril, Jenya Lee,
Diana Liskovich, Yinghai Lu, Yuning Mao, Xavier Martinet, Todor Mihaylov, Pushkar Mishra,
Igor Molybog, Yixin Nie, Andrew Poulton, Jeremy Reizenstein, Rashi Rungta, Kalyan Saladi,
Alan Schelten, Ruan Silva, Eric Michael Smith, Ranjan Subramanian, Xiaoqing Ellen Tan, Binh
Tang, Ross Taylor, Adina Williams, Jian Xiang Kuan, Puxin Xu, Zheng Yan, Iliyan Zarov, Yuchen
Zhang, Angela Fan, Melanie Kambadur, Sharan Narang, Aurelien Rodriguez, Robert Stojnic,
Sergey Edunov, and Thomas Scialom. Llama 2: Open Foundation and Fine-Tuned Chat Models,
2023b. URL `[https://arxiv.org/abs/2307.09288](https://arxiv.org/abs/2307.09288)` .


Trieu H. Trinh and Quoc V. Le. A Simple Method for Commonsense Reasoning, 2019. URL
`[https://arxiv.org/abs/1806.02847](https://arxiv.org/abs/1806.02847)` .


Alex Wang, Amanpreet Singh, Julian Michael, Felix Hill, Omer Levy, and Samuel R. Bowman.
GLUE: A Multi-Task Benchmark and Analysis Platform for Natural Language Understanding. In
_International Conference on Learning Representations_, 2019. URL `[https://openreview.net/](https://openreview.net/forum?id=rJ4km2R5t7)`
`[forum?id=rJ4km2R5t7](https://openreview.net/forum?id=rJ4km2R5t7)` .


Hanqing Wang, Yixia Li, Shuo Wang, Guanhua Chen, and Yun Chen. Milora: Harnessing minor
singular components for parameter-efficient llm finetuning, 2024. URL `[https://arxiv.org/](https://arxiv.org/abs/2406.09044)`
`[abs/2406.09044](https://arxiv.org/abs/2406.09044)` .


Yuxiang Wei, Zhe Wang, Jiawei Liu, Yifeng Ding, and Lingming Zhang. Magicoder: Empowering
Code Generation with OSS-Instruct. In _Proceedings_ _of_ _the_ _41st_ _International_ _Conference_ _on_
_Machine Learning_ . International Conference on Machine Learning, 2024. URL `[https://arxiv.](https://arxiv.org/abs/2312.02120)`
`[org/abs/2312.02120](https://arxiv.org/abs/2312.02120)` .


Adina Williams, Nikita Nangia, and Samuel Bowman. A Broad-Coverage Challenge Corpus for
Sentence Understanding through Inference. In Marilyn Walker, Heng Ji, and Amanda Stent,
editors, _Proceedings of the 2018 Conference of the North American Chapter of the Association_
_for Computational Linguistics:_ _Human Language Technologies, Volume 1 (Long Papers)_, pages
1112–1122, New Orleans, Louisiana, June 2018. Association for Computational Linguistics. doi:
10.18653/v1/N18-1101. URL `[https://aclanthology.org/N18-1101](https://aclanthology.org/N18-1101)` .


Zhengxuan Wu, Aryaman Arora, Zheng Wang, Atticus Geiger, Dan Jurafsky, Christopher D. Manning,
and Christopher Potts. ReFT: Representation Finetuning for Language Models, 2024. URL
`[https://arxiv.org/abs/2404.03592](https://arxiv.org/abs/2404.03592)` .


Wenhan Xia, Chengwei Qin, and Elad Hazan. Chain of LoRA: Efficient Fine-tuning of Language
Models via Residual Learning. In _Proceedings of the 41st International Conference on Machine_
_Learning_ . International Conference on Machine Learning, 2024. URL `[https://arxiv.org/](https://arxiv.org/abs/2401.04151)`
`[abs/2401.04151](https://arxiv.org/abs/2401.04151)` .


Longhui Yu, Weisen Jiang, Han Shi, Jincheng YU, Zhengying Liu, Yu Zhang, James Kwok, Zhenguo
Li, Adrian Weller, and Weiyang Liu. MetaMath: Bootstrap Your Own Mathematical Questions for
Large Language Models. In _The Twelfth International Conference on Learning Representations_,
2024. URL `[https://openreview.net/forum?id=N8N0hgNDRt](https://openreview.net/forum?id=N8N0hgNDRt)` .


13


Rowan Zellers, Ari Holtzman, Yonatan Bisk, Ali Farhadi, and Yejin Choi. Hellaswag: Can a machine
really finish your sentence?, 2019. URL `[https://arxiv.org/abs/1905.07830](https://arxiv.org/abs/1905.07830)` .


Qingru Zhang, Minshuo Chen, Alexander Bukharin, Pengcheng He, Yu Cheng, Weizhu Chen, and
Tuo Zhao. Adaptive Budget Allocation for Parameter-Efficient Fine-Tuning. In _The_ _Eleventh_
_International Conference on Learning Representations_, 2023. URL `[https://openreview.net/](https://openreview.net/forum?id=lq62uWRJjiY)`
`[forum?id=lq62uWRJjiY](https://openreview.net/forum?id=lq62uWRJjiY)` .


Jiacheng Zhu, Kristjan Greenewald, Kimia Nadjahi, Haitz Sáez de Ocáriz Borde, Rickard Brüel
Gabrielsson, Leshem Choshen, Marzyeh Ghassemi, Mikhail Yurochkin, and Justin Solomon.
Asymmetry in Low-Rank Adapters of Foundation Models. In _ICLR 2024 Workshop on Mathe-_
_matical and Empirical Understanding of Foundation Models_, 2024. URL `[https://openreview.](https://openreview.net/forum?id=PHrrbfrMEl)`
`[net/forum?id=PHrrbfrMEl](https://openreview.net/forum?id=PHrrbfrMEl)` .


Yukun Zhu, Ryan Kiros, Rich Zemel, Ruslan Salakhutdinov, Raquel Urtasun, Antonio Torralba, and
Sanja Fidler. Aligning Books and Movies: Towards Story-Like Visual Explanations by Watching
Movies and Reading Books. In _The IEEE International Conference on Computer Vision (ICCV)_,
December 2015.


Terry Yue Zhuo, Armel Zebaze, Nitchakarn Suppattarachai, Leandro von Werra, Harm de Vries,
Qian Liu, and Niklas Muennighoff. Astraios: Parameter-Efficient Instruction Tuning Code Large
Language Models, 2024. URL `[https://arxiv.org/abs/2401.00788](https://arxiv.org/abs/2401.00788)` .


14


**A** **Why do intruder dimensions exist & can we alleviate them?**


Here, we discuss possible causes of intruder dimensions.


**A.1** **What do intruder dimensions do?**


**Conjecture:** **Intruder dimensions, as high-ranking singular vectors, contribute significantly to**
**the norm and stability of the parameter matrix.** In contrast to pre-trained singular vectors that are
learned from large pre-training corpora, LoRA introduces intruder dimensions learned solely from
the smaller dataset of the fine-tuning task, which overpower the pre-trained vectors, as seen in the
experiments so far. This suggests that these intruder dimensions are very task specific. On the other
hand, full fine-tuning, while adapting just as effectively to the fine-tuning task, retains the spectral
properties of the pre-trained model effectively. Our experiments that scale down intruder dimensions
provide evidence for the claim that intruder dimensions are specialized to the fine-tuning task, since
we observe that increasing the norm of an intruder dimension (using _λ >_ 1) leads to little change in
adaptation task performance but leads to a significant increase in forgetting (pre-training loss).


**A.2** **Adding a random vector**


**Adding an random vector to a pre-trained matrix introduces an intruder dimension:** To help
provide intuition about how new singular vectors in the SVD can be added by LoRA, we examine
mathematical conditions that lead to their creation. Certainly, when comparing SVD( _W_ + _λvv_ _[T]_ )
and SVD( _W_ ), where _W_ are the pre-trained weights in R _[n][×][n]_, _v_ is a randomly sampled vector in R _[n]_,
and _λ_ is a scalar value greater than the largest singular value of _W_, we expect this update to create an
intruder dimension (as _v_ is nearly orthogonal to the existing singular vectors w.h.p.).


**A.3** **Differences in update rule**


As described in Appendix E, LoRA and full fine-tuning have characteristically different update rules,
even for the same training examples. We highlight that LoRA has gradients projected into a low-rank
space [Hao et al., 2024], leading to conditions similar to the toy example in section A.2 above.


**A.4** **Impact of learning rate on intruder dimensions.**


We study the impact learning rate has on intruder dimensions by sweeping a range of learning rates
while keeping all other hyperparameters fixed for LoRA _r_ = 8 and fine-tune on MNLI. Across
training epochs, we report the number of intruder dimensions, test accuracy, and pre-training loss
(Fig. 7). Across models, we see they have similar test accuracies after 5 epochs but very different
numbers of intruder dimensions. We note that small learning rates do not converge as fast as the ones
we tested and have difficulty reaching the maximum performance that larger learning rates are able to
reach. We see that as we increase learning rate, the number of intruder dimensions also increases
(left, Fig. 7). This illustrates a tradeoff in the selection of learning rate of LoRA: picking a larger
learning rate may lead to faster convergence and potentially better test accuracy with more intruder
dimensions and drift in overall language modeling performance, while smaller learning rates may
lead to less drift but potentially lower test accuracy.


Because of this experiment, one may dispute our findings with the claim that they are due to
our specific selection of hyperparameters. Therefore, we find it important to note that we adopt
hyperparameters from prior literature [Hu et al., 2021], default settings in common machine learning
libraries [2], and also study externally trained open-sourced models. This means that our findings are a
reflection of common practices and not due to a selection bias by us. Learning rates used by prior
work were likely determined based on a variety of factors like speed of convergence and best resulting
test accuracy and therefore selected large learning rates that still converge well but coincidentally
result in intruder dimensions.


15


Figure 10: **Impact of only tuning B on the number of intruder dimensions.** We randomly initialize
A such that it has singular values of 1, freeze it, and only train B. When we do this, we see a sharp
reduction in high ranking intruder dimensions in comparison to those in normal LoRA (reported in
Fig. 4d). Graphs for a specific dataset have the same range as Fig. 4d for easy comparison.


**A.5** **Matrix product parameterization of LoRA**


Multiplying matrices together amplifies their spectral differences (their singular values) and in most
cases leads to a lower effective rank. To test the impact of the product _BA_ on the introduction of
intruder dimensions, we randomly initialize _A_ such that all its singular values are 1 and freeze it. We
only tune _B_ and keep the rest of our fine-tuning recipe the same. Comparing this with vanilla LoRA is
fair because Zhu et al. [2024] found that tuning _B_ is more impactful and important for generalization
in comparison to _A_ and Hao et al. [2024] showed that only tuning _B_ effectively approximates LoRA.
As we can see in Fig. 10, we see a sharp drop in the number of high ranking intruder dimensions
when only tuning _B_ in comparison to the vanilla LoRA case where we train _A_ and _B_ separately, as
reported in Fig. 4. This suggests that the matrix product of LoRA is an important component in the
introduction of intruder dimensions because of how it amplifies the spectral differences of _B_ and _A_ .


**B** **Implementation Details**


**B.1** **Evaluation details**


We follow the precedence of Biderman et al. [2024] when evaluating LLaMA2-7B: When fine-tuned
on code, we evaluate on HumanEval [Chen et al., 2021] using the bigcode-eval-harness [Ben Allal
et al., 2022]. When fine-tuned on math, we evaluate on GSM8K [Cobbe et al., 2021] using the
lm-eval-harness [Gao et al., 2024]. On both, we evaluate task forgetting by evaluating on Hellaswag,
WinoGrande, and Arc-Challenge using the lm-eval-harness [Gao et al., 2024].


We measure language modeling loss for all our LLaMA2-7B models on a random sample of its
pre-training data distribution, according to Touvron et al. [2023b]. We measure “pseudo-loss” for all
our fine-tuned RoBERTa models on a random sample of the four datasets that RoBERTa used for
pre-training(OpenWebText [Gokaslan and Cohen, 2019], CCNews [Hamborg et al., 2017], Stories

[Trinh and Le, 2019], and bookcorpus [Zhu et al., 2015]) and weigh them proportionally to their
contribution as described by Liu et al. [2019].


**B.2** **Compute Resources**


All experiments were run on an internal, shared 8xA100-SXM4-80GB machine. All RoBERTa-base
fine-tuning runs required a single A100 GPU. All evaluations and analyses also required a single A100
GPU. Many experiments were run sequentially due to need to share these computing resources. Due
to these constraints, instead of fine-tuning our own LLaMA2-7B models, we use publicly released
fine-tuned models. For more information on these models, see Section K. Each RoBERTa-base
fine-tune run takes at most 6 hours on a single GPU. Evaluating an arbitrary LLaMA2-7B model for
both test accuracy and forgetting takes about 45 minutes on a single GPU.


**B.3** **RoBERTa fine-tuning details**


We generally follow the procedure used by Hu et al. [2021]. For all models, we use a linear learning
rate schedule with 0.06 linear warmup ratio and train for a maximum of 5 epochs with batch size 16.


2PEFT, the most popular LoRA library, use learning rates _≥_ 1e-3 in their tutorials and states “With LoRA-like
methods, you can afford to use a higher batch size and learning rate." [Mangrulkar et al., 2022].


16


We use the Adam optimizer [Kingma and Ba, 2017] with no weight decay and a maximum sequence
length of 512. We fine-tune all linear layers besides the embedding matrix. For full fine-tuning,
we use a learning rate of 1e-5. For LoRA, we set _α_ = 2 _r_, and train for all ranks in {1, 2, 4, 8,
16, 64}. We hold the “total learning rate of LoRA", which is _α ∗_ _η_, fixed as we sweep rank such
that this product always equals 2.4e-3. We fine-tune these models to equivalent accuracy on their
downstream task. We fine-tune on six sequence classification tasks: sentiment analysis [Socher et al.,
2013], entailment [Williams et al., 2018], duplicate identification [Wang et al., 2019], fact verification

[Thorne et al., 2018], and common sense reasoning [Sap et al., 2019, Sakaguchi et al., 2021].


**C** **Model Accuracies**


We report the accuracies that our RoBERTa models achieve in Table 1 and Table 2. Our main results
are based on the models in Table 2.

|Model Type|MNLI SST-2 QQP WinoGrande SIQA FEVER|
|---|---|
|RoBERTa-base<br>Full<br>r=1<br>r=2<br>r=4<br>r=8<br>r=16<br>r=64|0.8745<br>0.9438<br>0.9152<br>0.6582<br>0.6499<br>0.6892<br>0.8647<br>0.9358<br>0.9045<br>0.6251<br>0.672<br>0.6712<br>0.8604<br>0.9415<br>0.9058<br>0.6172<br>0.6581<br>0.6673<br>0.8607<br>0.9369<br>0.9079<br>0.6472<br>0.6505<br>0.6694<br>0.8648<br>0.9438<br>0.9108<br>0.6417<br>0.6586<br>0.6582<br>0.8604<br>0.9427<br>0.9095<br>0.6235<br>0.6853<br>0.663<br>0.8671<br>0.9484<br>0.9117<br>0.6614<br>0.6638<br>0.6601|



Table 1: Model accuracies on their given downstream task after fine-tuning for _α_ = 8.

|Model Type|MNLI SST-2 QQP WinoGrande SIQA FEVER|
|---|---|
|RoBERTa-base<br>Full<br>r=1<br>r=2<br>r=4<br>r=8<br>r=16<br>r=64|0.8745<br>0.9438<br>0.9152<br>0.6582<br>0.6499<br>0.6892<br>0.8677<br>0.9415<br>0.9042<br>0.6275<br>0.6418<br>0.687<br>0.869<br>0.945<br>0.9054<br>0.6551<br>0.6438<br>0.6822<br>0.8698<br>0.9472<br>0.9089<br>0.6361<br>0.6602<br>0.6827<br>0.8704<br>0.9472<br>0.9093<br>0.6346<br>0.6607<br>0.6928<br>0.8739<br>0.9461<br>0.9093<br>0.6417<br>0.6571<br>0.6924<br>0.8719<br>0.9472<br>0.9061<br>0.6212<br>0.6167<br>0.6864|



Table 2: Model accuracies on their given downstream task after fine-tuning for _α_ = 2 _r_ . Our main
results are based on these models.


**D** **Cosine Similarity with Orthogonal Vectors that Span a Space**


Here we demonstrate why it is possible for a vector to have low cosine similarity with every orthogonal
vector that collectively span a space if the dimensionality of the vectors is high.


**Minimizing the Maximum Cosine Similarity.** Lets take _Z_ = min _cos_ ( _v, xi_ ), where _v_ is an
_v∈_ R _[n]_ [ max] _i_

arbitrary vector and each vector _xi_, which we collectively call _X_, make up an orthonormal basis that
span the space. _Z_ can be small in a high dimensional space.


**2-D case.** Assume _X_ = _I_ without loss of generality. It is trivial to see that _Z_ = ~~_√_~~ 1

2 [, and is when]



_v_ = - ~~_√_~~ 1




 2 .



~~_√_~~ 1
2




[=]        - ~~_√_~~ 1
3 [when] _[ v]_




 3 .



**3-D case.** Assume _X_ = _I_ without loss of generality. _Z_ = ~~_√_~~ 1



~~_√_~~ 1
3



~~_√_~~ 1
3



**N-D case.** In the N-D case, we can see, via induction, that _Z_ = ~~_√_~~ 1 .
_n_


As we can see here, if _n_ is large, the value of _Z_ will be low, even though we are doing the cosine
similarity of a vector with respect to a set of orthonormal vectors that span a space.


17


**E** **Derivation of LoRA Adapter’s Gradients**


Our calculations were derived independently but follow a similar line to that of Hao et al. [2024].


**Derivation for Full Fine-tuning.** Full fine-tuning is structured such that


_Y_ = _WtunedX_ = ( _W_ 0 + ∆ _W_ ) _X,_


where _X_ _∈_ R _[n][×][b]_ are the inputs, _Y_ _∈_ R _[m][×][b]_ are the outputs, _W_ 0 _∈_ R _[m][×][n]_ are the pre-trained weights,
and ∆ _W_ _∈_ R _[m][×][n]_ is the fine-tuning update. Accordingly, _∂_ ∆ _∂LW_ [=] _∂Y_ _[∂L]_ _[X]_ _[T]_ [, and the update is]

∆ _Wn_ = ∆ _Wn−_ 1 _−_ _η_ _[∂L]_ _n_ _[,]_

_∂Y_ _n_ _[X]_ _[T]_


where _η_ is the learning rate.


**Derivation for LoRA.** LoRA is structured such that

_Y_ = _WtunedX_ = ( _W_ 0 + _[α]_

_r_ _[BA]_ [)] _[X,]_



where _X_ _∈_ R _[n][×][b]_ are the inputs, _Y_ _∈_ R _[m][×][b]_ are the outputs, _W_ 0 _∈_ R _[m][×][n]_ are the pre-trained weights,
_B_ _∈_ R _[m][×][r]_ is initialized to zero, _A_ _∈_ R _[r][×][n]_ is randomly initialized, and _α_ is a hyperparameter.
Accordingly, _[∂L]_ [=] _[α]_ _∂L_ _[X]_ _[T][ A][T]_ [and] _[∂L]_ [=] _[α]_ _[B][T]_ _[∂L]_ _[X]_ _[T]_ [ .] [Therefore, their respective updates are]




_[α]_ _r_ _∂Y∂L_ _[X]_ _[T][ A][T]_ [and] _∂A_ _[∂L]_




_[α]_ _[∂L]_

_r_ _[B][T]_ _∂Y_




_[∂L]_ _[α]_

_∂B_ [=] _r_




_[∂L]_ _[α]_

_∂A_ [=] _r_



_∂Y_ _[∂L]_ _[X]_ _[T]_ [ .] [Therefore, their respective updates are]



_∂L_

_Bn_ = _Bn−_ 1 _−_ _η_ _[α]_

_r_ _∂Y_ _[X]_ _[T][ A][T]_



and


where _η_ is the learning rate.




_[α]_ _[∂L]_

_r_ _[B][T]_ _∂Y_



_An_ = _An−_ 1 _−_ _η_ _[α]_



_∂Y_ _[X]_ _[T][,]_



**Differences in First Step.** During the very first step of training, given identical examples both full
fine-tuning and LoRA have the same _X_ and _Y_ for each layer since _B_ is initialized to zero. After the
first step, full fine-tuning has a update matrix equal to


∆ _Wfull_ = _−η_ _[∂L]_

_∂Y_ _[X]_ _[T][ .]_


In contrast, LoRA has an update matrix equal to



∆ _Wlora_ = ( _[α]_




_[α]_

_r_ [)(] _[B]_ [0] _[ −]_ _[η ][α]_ _r_




_[α]_ _∂L_ 0 [)(] _[A]_ [0] _[−]_ _[η]_ _[α]_

_r_ _∂Y_ _[X]_ _[T][ A][T]_ _r_




_[α]_ _r_ _[B]_ 0 _[T]_ _∂Y∂L_ _[X]_ _[T]_ [ )] _[.]_



Since _B_ 0 = 0,



∆ _Wlora_ = ( _[α]_




_[α]_ _[α]_

_r_ [)(] _[−][η]_ _r_




_[α]_ _∂L_ 0 [)(] _[A]_ [0][)] _[.]_

_r_ _∂Y_ _[X]_ _[T][ A][T]_



From this, we can see that the gradient steps are clearly different, even with the same training
examples.


**F** **Intruder Dimensions Correlate with Forgetting**


**F.1** **For RoBERTa**


As mentioned in the main text, when measuring the Spearman correlation between the number of
intruder dimensions and forgetting in Fig. 7 we find an extremely strong fit, with _ρ_ = 0 _._ 971 and
p-value _≪_ 0 _._ 001. This shows us that intruder dimensions strongly correlate with forgetting. In
contrast, when we correlate intruder dimensions with performance, we find no such correlation: for
RoBERTa, we measure _ρ_ = _−_ 0 _._ 3381 with p-value = 0 _._ 218.


18


Figure 11: **For LLaMA2-7B, intruder dimensions correlate with forgetting.** Top row: MetaMath.
Bottom row: Magicoder. We display intruder dimensions vs test accuracy and intruder dimensions vs
forgetting.


**F.2** **LLaMA2-7B**


When measuring the Spearman correlation between number of intruder dimensions and forgetting for
our LLaMA2-7B models across training epochs (Fig. 11 ( _middle_ )), we find a statistically significant
relationship with _ρ_ = 0 _._ 59 and p-value = 0 _._ 0006. When correlating intruder dimensions and test
accuracy (Fig. 11 ( _left_ )), we instead measure _ρ_ = _−_ 0 _._ 3178 with p-value = 0 _._ 0869. Again, we see
that intruder dimensions correlates with forgetting.


**G** **Intruder Dimensions Cause Forgetting (Scaling Experiments)**


**G.1** **Performance Differences When Scaling Down Intruder Dimensions**


**G.1.1** **RoBERTa**


We report our findings for RoBERTa models fine-tuned on MNLI, QQP, and FEVER in Table 3.
Remember that we scale down using the equation _W_ = _W_ 0 + ∆ _W_ + ( _λ −_ 1) _uiσivi_ _[T]_ [.] [Here, we see]
that scaling down intruder dimensions leads to a sharp drop in forgetting (pre-training loss) and a
much smaller drop in test accuracy. Scaling down an intruder dimension by two ( _λ_ = 0 _._ 5) results
always leads to less than a two percent drop in test accuracy but double digit percentage drops in
forgetting. One particularly compelling example, as shown in Fig. 8d, shows how scaling down
the top intruder dimensions with _λ_ = 0 _._ 7 when fine-tuning on QQP and using LoRA r=8 result in
essentially no (0.0%) drop in adaptation performance but a large (-33.2%) drop in forgetting. Our
findings of the impact of scaling down intruder dimensions hold across three datasets and both LoRA
r=1 and r=8, which were the two ranks that we found to have many intruder dimensions. Note that
this experiment is meaningless if a model has no intruder dimensions, since no singular vectors will
be removed.


**G.1.2** **LLaMA2-7B**


Our finding that scaling down intruder dimensions leads to less forgetting but similar test accuracy
holds to LLaMA2-7B. One particularly interesting example is for LLaMA2-7B fine-tuned on MetaMath with _r_ = 256: when scaling the top intruder dimensions down with _λ_ = 0 _._ 5, we see a large
drop (-25.2%) in forgetting and an _increase_ (+1.8%) in test accuracy.


19


|LoRA<br>Task<br>Rank|λ = 0.1<br>TA PTL|λ = 0.3<br>TA PTL|λ = 0.5<br>TA PTL|λ = 0.7<br>TA PTL|λ = 0.9<br>TA PTL|
|---|---|---|---|---|---|
|MNLI<br>r=1<br>r=8|-18.7<br>-13.3<br>-5.1<br>-24.7|-8.3<br>-14.5<br>-1.9<br>-23.1|-2.7<br>-13.7<br>-0.6<br>-19.8|-0.6<br>-11.0<br>-0.2<br>-14.5|0.0<br>-5.1<br>0.0<br>-5.9|
|QQP<br>r=1<br>r=8|-8.6<br>-35.5<br>-3.3<br>-52.0|-4.4<br>-35.8<br>-1.6<br>-50.6|-1.6<br>-34.1<br>-0.6<br>-45.0|-0.4<br>-28.9<br>-0.0<br>-33.2|0.1<br>-14.6<br>0.1<br>-13.0|
|FEVER<br>r=1<br>r=8|-11.1<br>-10.3<br>-5.6<br>-14.6|-4.2<br>-11.8<br>-1.0<br>-15.3|-0.4<br>-11.1<br>0.7<br>-13.4|0.6<br>-8.7<br>1.3<br>-9.7|0.6<br>-3.8<br>0.6<br>-4.0|


Table 3: **Impact of scaling RoBERTa-base’s intruder dimensions on test accuracy (TA) and pre**
**training loss (PTL).** Numbers reported are the percent change in test accuracy and percent reduction
in forgetting induced by fine-tuning. **Scaling down intruder dimensions leads to less forgetting.**
On RoBERTa. PTPL is Pre-training loss and TA is test accuracy. Both are reported as percent change
with respect to the unchanged fine-tuned model. Scaling down intruder dimensions has large impact
on forgetting but little impact on test accuracy.

|LoRA<br>Dataset<br>Rank|λ = 0.3<br>TA PTL|λ = 0.5<br>TA PTL|λ = 0.7<br>TA PTL|λ = 0.9<br>TA PTL|
|---|---|---|---|---|
|MetaMath<br>r=16<br>r=64<br>r=256|-15.0<br>-46.5<br>-5.8<br>-29.1<br>-0.1<br>-33.3|-6.6<br>-40.4<br>-4.4<br>-22.3<br>1.8<br>-25.2|-2.7<br>-28.2<br>0.3<br>-14.2<br>0.5<br>-15.5|0.0<br>-10.5<br>0.3<br>-4.9<br>-0.8<br>-5.2|
|Magicoder<br>r=16<br>r=64<br>r=256|-1.6<br>-37.5<br>-5.0<br>-12.7<br>-4.3<br>-12.8|-0.6<br>-24.4<br>-3.3<br>-8.3<br>-1.3<br>-10.2|-0.1<br>-13.2<br>0.3<br>-4.3<br>-0.9<br>-7.0|0.1<br>-4.1<br>2.2<br>-1.4<br>-1.6<br>-2.8|



Table 4: **Impact of scaling LLaMA2-7B’s intruder dimensions on test accuracy (TA) and pre**
**training loss (PTL).** Numbers reported are the percent change in test accuracy and percent reduction
in forgetting induced by fine-tuning.


**G.2** **Intruder Dimensions Cause Worse OOD Performance**


As we discussed in section 5 of the main text, for LoRA models with main intruder dimensions ( _r_ = 1
and _r_ = 8 in our experiments) we measure the impact of intruder dimensions by identifying and
scaling the top intruder dimension in every weight matrix such that _W_ = _W_ 0 +∆ _W_ +( _λ−_ 1) _uiσivi_ _[T]_ [,]
where _i_ is the index of the top intruder dimension (note that _λ_ = 0 is removal, _λ_ = 1 is no change,
and _λ_ = 2 doubles the intruder dimension). For our RoBERTa models fine-tuned on MNLI, QQP,
and FEVER, we use _λ ∈{_ 0 _,_ 0 _._ 25 _,_ 0 _._ 5 _,_ 0 _._ 75 _,_ 1 _._ 0 _,_ 1 _._ 5 _,_ 2 _._ 0 _}_ and for each measure the test accuracy and
pre-training loss. For a comparison baseline, we select the neighbor of the intruder dimension to
separately scale.


We report these results in Fig. 12a (MNLI), Fig. 12b (QQP), and Fig. 12c (FEVER). We find that
when scaling down intruder dimensions ( _λ <_ 1), we observe a clear and significant drop in forgetting
(pre-training loss) but a negligible drop in test accuracy (adaptation). When we instead scale up
intruder dimensions ( _λ >_ 1), we observe that forgetting increases significantly. We observe that when
scaling up top intruder dimensions by 50% ( _λ_ = 1 _._ 5), adaptation performance remains relatively
flat with a large increase in forgetting, providing further evidence that intruder dimensions are task
specific. These trends hold across all 6 models we study (3 datasets with two different LoRA ranks).


In contrast, when we scale a neighboring (pre-trained) singular vector of intruder dimensions instead,
we observe starkly different behaviors. When scaling down ( _λ <_ 1) these pre-trained singular vectors,
we observe we see that forgetting sharply increases and adaptation performance drops more sharply
than when scaling intruders instead. When scaling up ( _λ >_ 1) these pre-trained singular vectors, we
observe similar drops in forgetting and adaptation performance. This is likely because pre-trained
singular vectors are well tuned for language modeling, and therefore any change to them will have
negative downstream impacts on performance. This shows that are observations are not due to
the robustness of the model to scaling down specific singular vectors, but rather the difference in
contribution to model performance of intruder dimensions vs. pre-trained singular vectors.


Here, we clarify some possible points of confusion. We only scale the top intruder dimension in each
weight matrix, if and only if an intruder exists in that matrix, so even when _λ_ = 0 we do not recover


20


(a) RoBERTa-base fine-tuned on MNLI. (b) RoBERTa-base fine-tuned on QQP.


(c) RoBERTa-base fine-tuned on FEVER.


Figure 12: **Scaling RoBERTa-base’s intruder dimensions.** We scale the top intruder dimension
in each matrix by _λ_, a multiplicative constant, such that _W_ = _W_ 0 + ∆ _W_ + ( _λ −_ 1) _uiσivi_ _[T]_ [.] [Using]
_λ <_ 1 leads to a large drop in pre-training loss while only slightly impacting the test accuracy. For
Figs. 12a, 12b, and 12c, we also scale the intruder dimension’s neighbor, which is a pre-trained
singular vector. Changing these vectors negatively impacts both pre-training loss and test accuracy.


the pre-trained model because not all weight matrices have intruder dimensions and it is possible
for multiple intruder dimensions to exist in a weight matrix if LoRA _r_ _>_ 1. Furthermore, intruder
dimensions are not perfectly orthogonal to the pre-trained singular vectors. Due to the orthogonality
constraint imposed by the SVD, all singular vectors will be changed slightly in the matrix, so that
even when we remove the intruder dimension, the resulting matrix will be slightly different. These
reasons are why when _λ_ = 0 our LoRA _r_ = 1 models do not return to baseline performance.


These findings hold to LLaMA2-7B: in Fig 13, we see that scaling down intruder dimensions leads to
much less forgetting but similar test accuracy.


21


Figure 13: **Scaling down LLaMA2-7B’s intruder dimensions leads to less forgetting and nearly**
**equivalent test accuracy.**


**H** **The Effective Rank of the Update Matrix Depends on Alpha**


Kalajdzievski [2023] found that LoRA can have gradient collapse when rank is high if alpha is not set
properly. Biderman et al. [2024] found that setting _α_ = 2 _r_ is very important for the performance of
high rank LoRA. In this section, we provide additional evidence of the importance of setting _α_ = 2 _r_
and show that if _α_ is held fixed, high rank LoRA converges to low rank solutions. To do this, for
both _α_ = 2 _r_ and _α_ = 8, we measure the effective rank [Roy and Vetterli, 2007] of the weight matrix
updates for different LoRA ranks. Effective rank is a measure of the information density of a matrix
and can be thought of as an estimation of the rank needed to capture the information held in the
weight matrix. It is computed using the singular values of a matrix and we expect the LoRA rank to
be the upper bound on what the effective rank can be: LoRA _r_ = 8 should have an effective rank
update of at most 8. We present the effective rank measurements in Fig. 14. In this plot, we find that
when _α_ = 2 _r_ (Fig. 14a), LoRA _r_ = 64 and _r_ = 768 have much higher effective rank than _r_ = 8
and _r_ 16, with _r_ = 768 appearing to always have effective rank above 100. In stark contrast, we see
that when _α_ = 8 (Fig. 14b), high ranks of LoRA have much lower effective ranks, frequently even
converging to the effective rank of much lower rank updates (like _r_ = 8 and _r_ = 16). For example,
LoRA _r_ = 768 has an effective rank that is consistently below 50 when _α_ = 8. We note that full
fine-tuning has an effective rank update of above 400 consistently. These plots suggest that when
_α_ is kept fixed when scaling LoRA rank, the solutions are uable to take advantage of their higher
expressability and instead _converge to low rank solutions_ .


22


(a) Effective Rank of the LoRA update when _α_ = 2 _r_ . (b) Effective Rank of the LoRA update when _α_ = 8.


Figure 14: Effective rank of LoRA update matrices (∆ _W_ ) for RoBERTa fine-tuned on MNLI. We
observe that when _α_ = 2 _r_, higher ranks of LoRA ( _r_ = 64 _,_ 768) have much higher effective rank
than the same ranks of LoRA but instead with _α_ = 8. Building on Kalajdzievski [2023], Biderman
et al. [2024], this suggests that _α_ = 2 _r_ is necessary for high ranks of LoRA to utilize their expressive
capacity. Note: full fine-tuning consistently has updates with effective rank above 400.


**I** **Impact of Matrix Percentage on Number of Intruder Dimensions**


In this section, we examine the extent to which intruder dimensions exist throughout the entire weight
matrix and how they are distributed. As described in the main text, we hold _ϵ_ fixed as _ϵ_ = 0 _._ 5 and
measure the number of intruder dimensions while varying the proportion of the fine-tuned singular
vectors that we examine (this means varying our _k_ parameter in Algorithm 1). Here, we can see that
LoRA consistently has more intruder dimensions than full fine-tuning, regardless of what fraction of
the singular values we examine. The only caveat to this is that, for some datasets, full fine-tuning
passes LoRA _r_ = 1 when examining the last 20% of the fine-tuned singular vectors. This is likely
due to the limited expressivity of rank 1 updates and is interesting because it suggests that in this case,
full fine-tuning may be changing lower-ranking singular vectors more than LoRA. One interesting
contradiction to our findings is in Fig. 15d, which shows that full fine-tuning and LoRA appear
to have very similar distributions of intruder dimensions within their matrix when fine-tuned on
code. This is likely due to the large domain shift from natural language to coding tasks (Biderman
et al. [2024] also make this observation of a large domain shift required for models fine-tuned on
Magicoder [Wei et al., 2024]).


23


(a) Impact of the number of singular vectors in the fine-tuned matrix we examine, _k_, on the number of intruder
dimensions for RoBERTa models fine-tuned on 6 different tasks. Here, we set _ϵ_ = 0 _._ 5.



(b) LLaMA-7B fine-tuned on
Alpaca.



(c) LLaMA2-7B fine-tuned on
MetaMathQA.



(d) LLaMA2-7B fine-tuned on
Magicoder-Evol-Instruct.



Figure 15: **Impact of** _k_ **, the number of fine-tuned singular vectors we examine, on the number**
**of** **intruder** **dimensions.** We see that models fine-tuned with LoRA tend to have more intruder
dimensions than full fine-tuning, regardless of the value of _k_ used.


**J** **Impact of Dataset Size On Intruder Dimensions**


**The** **total** **number** **of** **intruder** **dimensions** **increases** **proportionally** **to** **the** **size** **of** **the** **fine-**
**tuning dataset.** Using our training recipe (Appendix B.3), we fine-tuned models on data subsets
of varying sizes. We trained RoBERTa-base on MNLI using LoRA with rank 1 and 8 (cases where
we originally saw intruder dimensions) and measure the number of intruder dimensions along with
the impact of _ϵ_ and _k_ (Fig. 16). For _r_ = 8, as we train on more data, more intruder dimensions are
introduced. Interestingly, however, LoRA with rank 1 appears to converge to similar amounts of
intruder dimensions, regardless of the dataset size. This may be because of the limited expressivity of
models with _r_ = 1. This experiments suggest that with smaller datasets, fewer intruder dimensions
may be introduced by LoRA.


Figure 16: _(Left)_ Impact of cosine similarity threshold, _ϵ_, on the number of intruder dimensions for
LoRA models trained on different proportions of the MNLI dataset. _(Right)_ Impact of the number of
fine-tuned singular vectors we examine, _k_, on the number of intruder dimensions for LoRA models
trained on different proportions of the MNLI dataset. We see that training on a larger proportion of
the dataset increases the number of intruder dimensions in the model.


24


**K** **LLaMA/LLaMA-2 Instruction Tuned Models**


Our LLaMA-7B checkpoints were fine-tuned on the Alpaca [Taori et al., 2023] and consist of
two fully fine-tuned models, one LoRA model with rank 16, and one QLoRA [Dettmers et al.,
2023] model with rank 64. Our LLaMA2-7B checkpoints were fine-tuned on either code (IFT with
Magicoder-Evol-Instruct-110K [Wei et al., 2024] or CPT with StarCoder [Li et al., 2023]) or math
(IFT with MetaMathQA [Yu et al., 2024] or CPT with OpenWebMath [Paster et al., 2023]) and
consist of one fully fine-tuned model and 3-4 LoRA’ed models of different ranks for each dataset and
generously provided by Biderman et al. [2024]. In Fig. 4a, Full #1 refers to “PKU-Alignment/alpaca7b-reproduced" and Full #2 refers to “chavinlo/alpaca-native".

|Hugging Face Path|Base Model|IT Dataset|
|---|---|---|
|timdettmers/qlora-alpaca-7b|LLaMA-7b|Alpaca|
|tloen/alpaca-lora-7b|LLaMA-7b|Alpaca|
|PKU-Alignment/alpaca-7b-reproduced|LLaMA-7b|Alpaca|
|chavinlo/alpaca-native|LLaMA-7b|Alpaca|
|LoRA-TMLR-2024/magicoder-lora-rank-16-alpha-32|LLaMA2-7b|Magicoder|
|LoRA-TMLR-2024/magicoder-lora-rank-64-alpha-128|LLaMA2-7b|Magicoder|
|LoRA-TMLR-2024/magicoder-lora-rank-256-alpha-512|LLaMA2-7b|Magicoder|
|LoRA-TMLR-2024/magicoder-full-fnetuning-lr-5e-05|LLaMA2-7b|Magicoder|
|LoRA-TMLR-2024/metamath-lora-rank-16-alpha-32|LLaMA2-7b|MetaMath|
|LoRA-TMLR-2024/metamath-lora-rank-64-alpha-128|LLaMA2-7b|MetaMath|
|LoRA-TMLR-2024/metamath-lora-rank-256-alpha-512|LLaMA2-7b|MetaMath|
|LoRA-TMLR-2024/metamath-full-fnetuning-lr-1e-05|LLaMA2-7b|MetaMath|
|LoRA-TMLR-2024/starcoder-lora-rank-16-20B-tokens|LLaMA2-7b|StarCoder|
|LoRA-TMLR-2024/starcoder-lora-rank-64-20B-tokens|LLaMA2-7b|StarCoder|
|LoRA-TMLR-2024/starcoder-lora-rank-256-20B-tokens|LLaMA2-7b|StarCoder|
|LoRA-TMLR-2024/starcoder-full-fnetuning-lr-1e-05-20B-token|LLaMA2-7b|StarCoder|
|LoRA-TMLR-2024/openwebmath-lora-rank-16-20B-tokens|LLaMA2-7b|OpenWebMath|
|LoRA-TMLR-2024/openwebmath-lora-rank-64-20B-tokens|LLaMA2-7b|OpenWebMath|
|LoRA-TMLR-2024/openwebmath-lora-rank-256-20B-tokens|LLaMA2-7b|OpenWebMath|
|LoRA-TMLR-2024/openwebmath-full-fnetuning-lr-1e-05-20B-tokens|LLaMA2-7b|OpenWebMath|



Table 5: Hugging Face model paths for LLaMA-7b/LLaMA2-7b IT models.


**L** **Continual Learning**


**L.1** **Performance during continual learning**


As described in Section 4 in the main text, we train sequentially on 6 tasks and measure task
performance on all of these tasks across tasks trained on (continual learning). We report the full
graph of our findings in Fig. 17. In it, we find that when all our models are trained to similar accuracy,
lower ranks of LoRA, which coincide with more intruder dimensions, forget more of their previously
learned tasks than higher ranks of LoRA and full fine-tuning.


**L.2** **Similarity matrices during continual learning**


After each continual learning dataset we fine-tune on, we measure the similarity matrix between the
current model and the pre-trained model. In Fig. 18b, we observe that LoRA accumulates intruder
dimensions across fine-tuning datasets. In contrast, in Fig. 18a we observe that the pre-trained
structure of the model is retained well across fine-tuning datasets. These experiments suggest why
LoRA appears to degrade faster during continual learning.


25


Figure 17: Full plot of Fig. 9a. Continual Learning performance of RoBERTa for full fine-tuning and
LoRA. We sequentially train on six tasks, in order from left to right. Horizontal dotted line indicates
baseline pre-trained performance. Vertical solid line indicates when a specific dataset is fine-tuned on.
Gray region represents performance before the model has been trained on that task. We are interested
in the differences in accuracies of these methods both right after training (at the vertical black line)
and later (in the white region). We see that low ranks of LoRA forget previously learned tasks more.


(a) Continual learning similarity matrices for full fine-tuning.


(b) Continual learning similarity matrices for LoRA.


Figure 18: **LoRA accumulates intruder dimensions, while full fine-tuning does not.** The pretrained structure of the model degrades across tasks trained on.


26


**M** **Case Study:** **Setting Alpha=8 instead of Alpha=2r**


Our main experiments were conducted with _α_ = 2 _r_ . However, Hu et al. [2021] instead set _α_ = 8 for
RoBERTa-base. While not the recommended practice now, we explore what impact this selection has
on our findings. We report our key plots in Fig. 19a, 19b, 20, 21, & 14b. In Fig. 19a & 19b we see
that LoRA’d models with high rank have significantly more intruder dimensions in comparison to
when _α_ = 2 _r_ . Interestingly, whereas when _α_ = 2 _r_ LoRA models with ranks like 64 had no or very
few intruder dimensions (see Fig. 4), they now have numerous intruder dimensions. These differences
are corroborated by Fig. 14b, where we see that the learned solutions of LoRA have significantly
lower effective rank in comparison to when _α_ = 2 _r_ . For example, we see in Fig. 14b that when
LoRA has a rank of 768, the effective rank is never above 100. In contrast, we see in Fig. 14a that
with the same rank of 768, LoRA always has an effective rank above 768. This suggests that when
_α_ = 8, LoRA is converging to lower rank solutions than when _α_ = 2 _r_ . This supports the finding
that setting _α_ = 2 _r_ improves LoRA’s performance when a high rank is used [Biderman et al., 2024,
Kalajdzievski, 2023]. Behaviorally, we see in Fig. 21 that LoRA models with high rank have much
more forgetting on previously learned tasks in comparison to full fine-tuning and LoRA when _α_ = 2 _r_
is used ( _α_ = 2 _r_ results are in Fig. 17). Likewise, in Fig. 14b we see that when LoRA has high rank,
it has much more forgetting on the pre-trained distribution in comparison to LoRA when _α_ = 2 _r_ .


(a) Number of intruder dimensions in RoBERTa models fine-tuned on 6 different tasks. Here, we set _k_ = 10.
We use the same conditions as in Fig. 4d but instead now set _α_ = 8 instead of _α_ = 2 _r_ .


(b) Impact of the number of singular vectors in the fine-tuned matrix we examine, _k_, on the number of intruder
dimensions for RoBERTa models fine-tuned on 6 different tasks. Here, we set _ϵ_ = 0 _._ 5. We use the same
conditions as in Fig. 15a but instead now set _α_ = 8 instead of _α_ = 2 _r_ .


Figure 19: We find that when _α_ = 8 instead of _α_ = 2 _r_, our models have more intruder dimensions.
_(Top)_ Replication of Fig. 4d with _α_ = 8 instead of _α_ = 2 _r_ . _(Bottom)_ Replication of Fig. 15a with
_α_ = 8 instead of _α_ = 2 _r_ .


**N** **Impact of Random Seeds**


To ensure that random seed does not play a role in the number of intruder dimensions we observe
in a model, we sample 5 different seeds and fine-tune RoBERTa-base on MNLI using the same
methodology as in Fig. 4d. We find that the initialization has a negligible role on the number of
intruder dimensions. This shows that our findings are not dependent on the random initialization of
the LoRA modules.


**O** **LoRA Variants**


We focus significantly on the standard LoRA method proposed by Hu et al. [2021] in order to study it
in depth. However, many variants of LoRA have been proposed recently. AdaLoRA [Zhang et al.,
2023] adaptively allocates LoRA rank to different modules in order to ensure optimal allocation of
trainable parameters to certain modules. LoRA+ [Hayou et al., 2024] sets different learning rates
for the A and B modules in LoRA. PiSSA [Meng et al., 2024] initializes the A and B modules with


27


Figure 20: For _α_ = 8. RoBERTa’s performance on its pre-training data distribution after fine-tuning
on a particular task. We measure pseudo loss as described by Salazar et al. [2020]. We compare these
results to when _α_ = 2 _r_ (Fig. 6).


Figure 21: For _α_ = 8. RoBERTa’s performance on six datasets during continual learning. We
sequentially train on six tasks, in order from left to right. Horizontal dotted line indicates baseline
pre-trained performance. Vertical solid line indicates when a specific dataset is fine-tuned on. We
compare these results to when _α_ = 2 _r_ (Fig. 17).


the top ranking singular vectors of the pre-trained weights. VeRA [Kopiczko et al., 2024] models
LoRA as the product of two random matrices with trainable parameters doing elementwise operations
on the resulting vectors. These variants may have important impacts on the presence of intruder
dimensions. For example, PiSSA initializes with the singular vectors and therefore may have an
easier time changing them, possibly leading to more intruder dimensions. In contrast, LoRA+ in
effect lowers the learning rate, which we found to be important to introducing intruder dimensions,
and may therefore reduce the number of intruder dimensions.


In order to examine if intruder dimensions are still relevant for these methods, we rerun our MNLI
fine-tuning experiment with RoBERTa with each of these methods with default hyperparameters
that they provide. These results are supplied in Fig. 23. Interestingly, we see that all the variations
we examine have intruder dimensions. Some interesting observations include: LoRA+ and LoRA
_r_ = 1 appear to have nearly identical curves, suggesting they have very ismilar intruder dimension
characteristics. We again see that with higher ranks ( _r_ = 64) these LoRA variants tend to have very
few intruder dimensions. However, it does appear that methods that explicitly modify the singular
vectors, like PiSSA, have many intruder dimensions. This makes sense since they are explicitly
constructed to modify the singular vectors on the pre-trained model. These findings emphasize that


28


Figure 22: **Impact of Random Seeds on intruder dimensions.** We fine-tune RoBERTa-base across
5 random seeds and use our same methodology as in Fig. 4d. We find that the initialization has a
negligible role on the number of intruder dimensions. This shows that our findings are not dependent
on the random initialization of the LoRA modules.


Figure 23: **Measuring LoRA variants for intruder dimensions.** _k_ = 10. We compare variants
of LoRA to normal LoRA (blue) and full fine-tuning (black). We find that the LoRA variants we
examine still have intruder dimensions and shows that our findings are not just exclusive to normal
LoRA.


intruder dimensions are not just an observed phenomenom in normal LoRA and suggests to future
work the examination of LoRA variants.


29


