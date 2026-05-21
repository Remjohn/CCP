## ALLoRA: Adaptive Learning Rate Mitigates LoRA Fatal Flaws



**Hai** **Huang**
Google
1600 Amphitheatre Parkway
Mountain View, California
```
haih@google.com

```


**Randall** **Balestriero**
Department of Computer Science
Brown University
```
  rbalestr@brown.edu

```

Abstract



Low-Rank Adaptation (LoRA) is the bread and butter of Large Language
Model (LLM) finetuning. LoRA learns an additive low-rank perturbation,
_**AB**_, of a pretrained matrix parameter _**W**_ to align the model to a new
task or dataset with _**W**_ + _**AB**_ . We identify three core limitations to LoRA
for finetuning–a setting that employs limited amount of data and training
steps. First, LoRA employs Dropout to prevent overfitting. We prove that
Dropout is only suitable for long training episodes but fails to converge
to a reliable regularizer for short training episodes. Second, LoRA’s initialization of _**B**_ at 0 creates a slow training dynamic between _**A**_ and _**B**_ .
That dynamic is also exacerbated by Dropout that further slows the escape from 0 for _**B**_ which is particularly harmful for short training episodes.
Third, the scaling factor multiplying each LoRA additive perturbation creates “short-sighted” interactions between the LoRA modules of different
layers. Motivated by principled analysis of those limitations, we find an
elegant solution: a Dropout-free, scaling-free, LoRA with Adaptive Learning rate–coined ALLoRA. By scaling the per sample and per parameter
gradients with a coefficient inversely proportional to parameters’ _ℓ_ 2 norm,
ALLoRA alleviates those three limitations. As a by-product, ALLoRA removes two hyper-parameters from LoRA: the scaling factor and the dropout
rate. Empirical results show that ALLoRA admits better accuracy than
LoRA on various settings, including against recent LoRA variants such
as Weight-Decomposed Low-Rank Adaptation (DoRA). Ablation studies
show our solution is the optimal in a family of weight-dependent / outputdependent approaches on various LLMs including the latest Llama3.


1 Introduction


Large Language Models (LLMs) (Hoffmann et al., 2022; Touvron et al., 2023; Jiang et al.,
2023) are Deep Neural Networks (DNNs)–commonly built from Transformer with selfattention–built for sequence processing, e.g., Natural Language Processing (NLP). LLMs
have radically changed the way we approach NLP (Chowdhary, 2020) by removing the need
for handcrafted feature engineering such as bags of words (Zhang et al., 2010). Instead, current solutions directly operate on the input data–or a lossless compression known as tokens
(Shibata et al., 1999). Because we now have access to humongous amount of text data, the
standard training pipeline for LLMs take the following form. First, the LLM is _pretrained_
on a large text corpus through next-token prediction. That autoregressive pretext-task
enables the LLM to learn the underlying dynamic of the language. Commonly, RLHF is
also employed after pretraining to make the model’s behavior shift from autoregressive to
agentic. Then, the LLM is _fine-tuned_ on a more specific downstream task or dataset. That
fine-tuning is user-specific and plays a fundamental role in making LLMs practically useful
but relies on much more limited datasets, as we formalize below.


1


_**Premise:**_ _The_ _training_ _regime_ _involved_ _in_ _pretraining_ _and_ _fine-tuning_ _are_ _drastically_
_different._ _The_ _former_ _employs_ _limitless_ _data_ _and_ _abundant_ _training_ _steps_ _while_ _the_
_latter_ _employs_ _limited_ _data_ _and_ _few_ _training_ _steps._


That premise is now widely accepted upon as the latest state-of-the-art LLM solutions stem
from the numerous open-source industry groups such as Meta’s Llama (Dubey et al., 2024),
Google’s Gemma (Team et al., 2024), Apple’s OpenELM (Mehta et al., 2024), or Cohere’s
Aya. Hence, as LLM practitioners, most of the attention is now turning into deriving
fine-tuning strategies that meet the very particular needs of fine-tuning LLMs.


To tackle that paradigm shift introduced by the pretraining-finetuning strategy, specialized
methods have been developed, such as the eponymous Low-Rank Adaption (LoRA). LoRA
has fueled countless deployment of LLMs–as it took a gigantic leap in accommodating for
the fine-tuning regime. In short, LoRA proposes to fine-tune a LLM by learning an additive
low-rank matrix perturbation to some of the LLM’s internal parameter matrices. Core
to its design, LoRA leverages (i) Dropout (Srivastava et al., 2014) as a mean to prevent
overfitting to the fine-tuning task, and (ii) zero-initialization to ensure that training starts
from the LLM’s pretrained mapping, and (iii) a scaling factor that rescales the LoRA’s
matrix factorization. While the impact of LoRA is ubiquitous, we nonetheless believe that
LoRA could be further improved based on three observations.


_**LoRA’s**_ _**three**_ _**fatal**_ _**flaws**_ _**for**_ _**finetuning:**_ _First,_ _**Dropout**_ _–a stochastic regularizer–_
_whose_ _benefits_ _quickly_ _vanish_ _when_ _considering_ _fine-tuning,_ _and_ _can_ _in_ _fact_ _introduce_
_detrimental_ _additional_ _variance_ _to_ _the_ _training._ _Second,_ _the_ _**zero-initialization**_ _which_
_is_ _difficult_ _to_ _escape_ _from_ _due_ _to_ _Dropout’s_ _implicit_ _regularization._ _Third,_ _the_ _**scaling**_
_**parameter**_ _that_ _introduces_ _nonlinear_ _interactions_ _between_ _LoRA_ _modules_ _of_ _different_
_layers._


While each of those three design choices are well-motivated when considering long training,
e.g., pretraining, it becomes harder to prove their benefits when considering fine-tuning
that only employs a minimal amount of training steps. That is why, after carefully bringing
to light and studying the above flaws of LoRA–in the context of fine-tuning–in section 3,
we will propose a novel variation of LoRA that we coin **ALLoRA** for **A** daptive **L** earning
rate **LoRA** (section 4). ALLoRA proposes to remove the Dropout regularizer and the
scaling factor while adding an adaptive learning rate for the low-rank matrices entries. As
depicted in listing 1, the implementation is straightforward with theoretical and practical
benefits. First, by removing the Dropout regularization and the scaling factor, ALLoRA
is simpler to employ as it no longer requires cross-validation of those parameters. Second,
we demonstrate how ALLoRA improves performances over LoRA and alternatives such as
DoRA. In short, our adaptive learning rate strategy is able to prevent over-fitting, learn
competitive solutions, and converge more quickly than alternatives–all while employing less
hyper-parameters.


We summarize our contributions below:


1. We identify three inefficiencies (sections 3.1 to 3.3) in the current LoRA design
making it unfit for short training, i.e., finetuning, that we empirically validate in
section 3.4.


2. We propose a novel adaptive learning rate variation of LoRA–coined ALLoRA–free
of two of the original LoRA’s complicated designs: the Dropout regularizer and the
scaling factor (section 4).


3. We empirically validate the benefits of ALLoRA over numerous datasets and model
architectures including the latest Llama3 family (sections 4.4 and 4.5). We obtain
that despite ALLoRA employing less hyperparameters than LoRA, it is able to
outperform its counter part and recent variants such as DoRA consistently.


2


The full codebase to reproduce figures and tables is publicly available [1] along side the finetuned models’ weights [2] .


2 Related Works


LoRA is a type of _Parameter_ _Efficient_ _Fine_ _Tuning_ (PEFT) designed to reduce the cost
of finetuning, especially with LLMs. As LLMs typically have large number of parameters–
in the scale of billions–one can not afford to finetune all those parameters on a particular
downstream task or dataset. Existing PEFT can be divided into three categories, namely
_Adapter-based_ _Methods_, _Prompt-based_ _Methods_, and _LoRA_ .


Adapter-based methods (Houlsby et al., 2019; He et al., 2022; Karimi Mahabadi et al.,
2021a;b) introduce additional trainable modules, _a.k.a._ the _adapters_, into the original backbone whose weights are frozen during the finetuning. In Houlsby et al. (2019), linear modules
were added in sequence to the existing layer, while in He et al. (2022), they were added in
parallel to the existing layer for the sake of better performance.


Prompt-based methods (Lester et al., 2021; Razdaibiedina et al., 2023; Wang et al., 2023)
introduce soft tokens as trainable parameters and prepend them to the prompt. This category is the least intrusive as the finetuning can be done by only prompting the LLMs.
However, prompt-based methods are in general sensitive to initialization and their overall
effectiveness is affected.


LoRA (Hu et al., 2021) uses low-rank matrices to simulate weight changes of the pretrained
weights. Since low-rank matrices can be merged back to original weights, LoRA does not
incur any additional cost at inference, which is a significant advantage over the other two
categories. Many variants were proposed lately. For example, in Zhang et al. (2023), SVD
decomposition was employed to determine significance of singular values, and less important
ones are pruned. Hyeon-Woo et al. (2022) applies low-rank Hadamard product to federated
learning. Qiu et al. (2023) and Liu et al. (2024b) adopt orthogonal factorization and applied
to diffusion models. Renduchintala et al. (2023) introduces weight tying and realizes more
savings on number of parameters. A unified LoRA family was introduced for Stable diffusion
in Yeh et al. (2024). Different combinations of LoRA are chosen for different tasks in Ponti
et al. (2022). A scaling vectors is learnt to adjust a pair of frozen random matrices shared
across layers in Kopiczko et al. (2023).


More recently, Liu et al. (2024a) proposes decomposing the weights into directional and
magnitude components to boost accuracy. Hayou et al. (2024a) studies the optimal initialization of the low-rank matrices, and a follow-up work (Hayou et al., 2024b) proposes to
apply different learning rate to different low-rank matrices. Superficially this is similar to
one of our idea to adapt learning rate, though our idea is inspired by a principled study of
dropout (Srivastava et al., 2014).


More broadly, Zhao et al. (2024) applies the low-rank concept to compute low-rank gradients
directly. Jang et al. (2024) provides a study on the existence and convergence of LoRA
solutions. And Zhang & Pilanci (2024) is a study of the potential ill conditioned low-rank
matrices.


3 A Critical Analysis Of LoRA for Finetuning


PEFT is the main bridge between large pretrained LLMs and specialized practical use-cases.
Hence, PEFT research is extremely active which led to numerous variations of LoRA being
developed. Our theoretical study builds on the seminal version formalized below, other
LoRA variants will be compared in our experimental sections 4.4 and 4.5.

**Definition** **1.** (Low Rank Adapters (LoRA) from Hu et al. (2021)). For any weight matrix
_**W**_ _∈_ R _[n]_ [1] _[×][n]_ [2] in the pretrained model, we constrain its update in the finetuning process by
representing the latter with a low-rank decomposition _**W**_ [˜] = _**W**_ + _[α]_ _r_ _**[BA]**_ [.] [Here,] [only] [the]


1 `[http://github.com/rbalestr-lab/allora](http://github.com/rbalestr-lab/allora)`
2 `[http://bit.ly/allora-weights](http://bit.ly/allora-weights)`


3


weight matrices _**B**_ _∈_ R _[n]_ [1] _[×][r]_, _**A**_ _∈_ R _[r][×][n]_ [2] are trainable. The rank _r_ _≪_ min( _n_ 1 _, n_ 2) and _α ∈_ R
are tunable constants.


Despite LoRA’s simplicity, very little attention was put on its core premises within a finetuning context, i.e., with limited amount of training steps. We propose here a principled
and critical study of LoRA, culminating with our finding of three core flaws of LoRA for
short training (sections 3.1 to 3.3). The following section 4 will investigate our solution,
ALLoRA.


3.1 First Flaw: A Stochastic Regularization that Will not Converge


LoRA’s regularization comes from Dropout (Srivastava et al., 2014), i.e., applying a multiplicative random binary mask at the bottleneck of the matrix factorization. The use of
Dropout would seem justified since Wager et al. (2013) showed in the linear regime that
Dropout acts as a variant of _ℓ_ 2 regularization on normalized design matrix (inputs), a result
also found in the previous study of Wang & Manning (2013). However, those theoretical results deal with _expectations_, i.e., infinite training time. Similarly, previous empirical studies
of Dropout showed great regularization benefits, but all those studies only considered full
training, i.e., long training episodes that ultimately converge to their expectation. We argue that those beneficial findings _do_ _not_ _hold_ _during_ _fine-tuning_ _which_ _only_ _employs_ _limited_
_training_ _steps_ .


To understand the impact of Dropout in terms of regularization, we will consider a few
variations of models and study the discrepancy between the _expected_ benefit of Dropout with
its _empirical_ realisations. We will conduct validation on real dataset and LLMs to support
our theory throughout the section, and in particular in section 3.4. Also, we consider here
and in section 3.2 _α/r_ to be 1 without loss of generality, none of our results are impacted
by that constant scaling factor.


**Linear** **model** **with** **full** **training.** Let’s first consider the original setting of a linear model
with Dropout applied to its predictions. That is, we consider the following Ordinary Least
Squares (OLS) setting _∥_ _**Y**_ _−_ ( _**XW**_ ) _⊙_ _**V**_ _∥_ [2] _F_ [,] [with] _**[Y]**_ _[∈]_ [R] _[N]_ _[×][C][,]_ _**[ X]**_ _[∈]_ [R] _[N]_ _[×][D][,]_ _**[ W]**_ _[∈]_ [R] _[D][×][C]_ [and]
the random realization of dropout matrix _**V**_ _∈{_ 0 _,_ _p_ [1] _[}][N]_ _[×][C]_ [.] [We] [note] [that] [such] [parametriza-]

tion of Dropout is commonly employed in the literature to ensure that its expectation is
equal to 1, and it is also PyTorch’s official implementation. We have the following property
that has motivated the use of Dropout through more than a decade by now:

E - _∥_ _**Y**_ _−_ ( _**XW**_ ) _⊙_ _**V**_ _∥_ [2] _F_ 
= _∥_ _**Y**_ _∥_ [2] _F_ [+][ E]  - _−_ 2 _Tr_  - _**Y**_  - _**V**_ _[⊤]_ _⊙_ ( _**XW**_ ) _[⊤]_ [��] + _Tr_ �� _**V**_ _[⊤]_ _⊙_ ( _**XW**_ ) _[⊤]_ [�] (( _**XW**_ ) _⊙_ _**V**_ )��



= _∥_ _**Y**_ _∥_ [2] _F_ _[−]_ [2] _[Tr]_ - _**Y**_ ( _**XW**_ ) _[⊤]_ [�] + _Tr_ �( _**XW**_ ) _[⊤]_ ( _**XW**_ )� +




- 1 - _Tr_ �( _**XW**_ ) _[⊤]_ ( _**XW**_ )� _,_
_λ_ _[−]_ [1]



which is solved for _**W**_ = _p_ ( _**X**_ _[⊤]_ _**X**_ ) _[−]_ [1] _**Y**_ _[⊤]_ _**X**_ . We note that we decomposed the loss into the
terms that happen in the original (Dropout-free) setting, in blue, and the Dropout induces
terms in orange. Comparing that with the usual Tikhonov regularization that produces
_**W**_ = ( _**X**_ _[⊤]_ _**X**_ + _λ_ _**I**_ ) _[−]_ [1] _**Y**_ _[⊤]_ _**X**_ we see then whenever the eigenvalues of _**X**_ _[⊤]_ _**X**_ are all identical
to a positive constant _c_ (e.g. when _**X**_ is whitened), _**W**_ = _c_ + _cλ_ [(] _**[X]**_ _[⊤]_ _**[X]**_ [)] _[−]_ [1] _**[Y]**_ _[⊤]_ _**[X]**_ [hence]
recovering the dropout solution. Assuming _c_ = 1 without loss of generality, we obtain that
applying Dropout with rate _p_ = 1+1 _λ_ [is equivalent to applying Tikhonov regularization with]
rate _λ_ . As a result, we see that if training for long enough, Dropout can efficiently replace
explicit forms of regularization such as weight decay. While the above results recovers
known theoretical analysis of Dropout–showing its benefits as an implicit regularizer–those
derivations only emerge from taking expectation of the loss, i.e., considering infinite training
steps. For us, the question thus turns into the following: _what_ _are_ _the_ _benefits_ _of_ _Dropout_
_as_ _a_ _LoRA_ _regularizer_ _for_ _very_ _short_ _training_ _regime_ _such_ _as_ _finetuning?_


**LoRA** **with** **Dropout** **fails** **to** **converge.** Let’s denote the LoRA linear finetuning setting
as follows

_L_ ≜ _∥_ _**Y**_ _−_ _**X**_ _LoRA_ _**A**_ _,_ _**B**_ ( _**W**_ ) _∥_ [2] _F_ [=] _[ ∥]_ _**[Y]**_ _[−]_ _**[XW]**_ _[−]_ [((] _**[XA]**_ [)] _[ ⊙]_ _**[V]**_ [ )] _**[B]**_ _[∥]_ [2] _F_ _[.]_ (1)


4


Figure 1: We depict the absolute difference ( **y-axis** ) between the empirical and expected finetuning
LoRA loss with varying Dropout rates ( **rows** ) on different datasets ( **columns** ) as a function of the
number of Dropout realisation ( **x-axis** ). We observe that regardless of the dataset and Dropout
probability, the empirical error is a poor estimate of the true expected loss even after hundreds of
averaged realisations. Hence, **finetuning** **with** **Dropout** **produces** **a** **large** **amount** **of** **random**
**noise** **that** **go** **well** **beyond** **its** **regularization** **benefit** **which** **only** **emerges** **after** **a** **large**
**number** **of** **steps** . That finding is also confirmed by the LLM experiment in fig. 5.


In the above setting, we can slightly modify the above analysis to obtain the following result



E [ _L_ ]= _∥_ _**Y**_ _−_ _**XW**_ _∥_ [2] _F_ _[−]_ [2] _[Tr]_ �( _**Y**_ _−_ _**XW**_ ) _[⊤]_ ( _**XAB**_ )�+ _∥_ _**XAB**_ _∥_ [2] _F_ [+] [1] _[ −]_ _[λ]_

_λ_



_R_

- _∥_ _**X**_ ( _**A**_ ) _.,r_ ( _**B**_ ) _r,.∥_ [2] _F_ _[,]_

_r_ =1



where we recall that _λ_ [1] _[−]_ [1] _[ >]_ [ 0] _[,][ ∀][λ][ ∈]_ [(0] _[,]_ [ 1).] [As] [for] [the] [full] [training] [setting,] [we] [decomposed]

the loss into the terms that happen in the original (Dropout-free) setting, in blue, and
the Dropout induces terms in orange. Before diving into the impact of Dropout in terms
of regularization, it is interesting to understand how many samples or training steps are
needed for the empirical estimate to converge to the above expectation. We propose that
analysis in fig. 1. We clearly see that even for small Dropout value 0 _._ 05, the convergence is
quite slow on the various settings we explored.


To better understand those trends, we propose a first simple bound on “how far off” is the
expectation to the empirical estimator as a function of the number of realisations, or, steps.
The detailed derivations as provided in appendix A.We obtain



_N_

- _∥_ _**Y**_ _−_ _**XW**_ _−_ (( _**XA**_ ) _⊙_ _**V**_ _n_ ) _**B**_ _∥_ [2] _F_ _[−]_ [E] - _∥_ _**Y**_ _−_ _**XW**_ _−_ (( _**XA**_ ) _⊙_ _**V**_ ) _**B**_ _∥_ [2] _F_ 
_n_ =1 �����







E



1

_N_
������



_≤_ _[Std]_ - _∥_ _**Y**_ _−_ _**XW**_ _−_ ~~_√_~~ (( _**XA**_ ) _⊙_ _**V**_ ) _**B**_ _∥_ [2] _F_ 


~~_√_~~



_._
_N_



As a result, the benefit of _N_, in our case the number of training steps, only appears for
large _N_ as depicted in fig. 1. This is particularly true as training progresses where the value
of the standard deviation of the error ( _Std_ - _∥_ _**Y**_ _−_ ( _**XW**_ ) _⊙_ _**V**_ _∥_ [2] _F_ �) may increase under the
Dropout. While this could be dataset and model specific, we illustrate the distribution of
that random variable during training in fig. 2. We look at the standard deviation of the
gradients as a function of Dropout realisation in a simple MLP with MNIST classification
task as training progresses and observe that the distribution becomes more and more heavytailed as training progresses, indicating that some mini-batch may receive highly noisy loss
and gradient updates, hence making it hard to recover during short finetuning settings.


5


Figure 2: Depiction of the distribution of standard deviation of gradients ( **y-axis** ) w.r.t. the
second layer of a MLP trained for MNIST ( **left** ) and CIFAR10 ( **right** ) classification, equipped
with Dropout. At each training epoch ( **x-axis** ), we consider a single mini-batch and compute
the gradients under numerous Dropout realisation. For each entry in the matrix of gradients,
we compute the standard deviation and report the distribution over entries. We clearly see that
**while** **the** **average** **variance** **of** **the** **gradient** **decreases** **slightly** **during** **training,** **the** **tail**
**significantly** **increases,** **leading** **to** **unstable** **training** **in** **finetuning** **regimes** .


3.2 Second Flaw: Zero Initialization and Unfair Regularization


The second flaw we uncover comes from the zero initialization of _**B**_ . As we will see, that is
a limitation regardless of employing Dropout or not, but Dropout exacerbates it.


**Zero** **initialization** **implies** **imbalanced** **training** **dynamics.** A peculiarity of LoRA
compared to most other deep learning framework lies in its asymmetric initialization. While
_**A**_ is initialized with random entries, _**B**_ is initialized at 0. This initialization is intuitive when
looking at the output of LoRA being 0 at first, i.e., one starts from the original model and
then moves away from that if needed for the finetuning task. However, this seemingly
reasonable initialization creates a strong imbalance in the training dynamic of _**A**_ and _**B**_ .
To see that, we can extend our derivation to obtain the derivative of the expected loss as


              - 1 _−_ _λ_              _∇_ _**A**_ E [ _L_ ] = _−_ _**X**_ _[⊤]_ ( _**Y**_ _−_ _**XW**_ ) _**B**_ _[⊤]_ + _**X**_ _[⊤]_ _**XA**_ diag( _∥_ _**B**_ 1 _,_ : _∥_ [2] 2 _[, . . .,][ ∥]_ _**[B]**_ _[r,]_ [:] _[∥]_ [2] 2 [) +] _**[ BB]**_ _[⊤]_ _,_
_λ_

_∇_ _**B**_ E [ _L_ ] = _−_ _**A**_ _[⊤]_ _**X**_ _[⊤]_ ( _**Y**_ _−_ _**XW**_ )


    -     + _**A**_ _[⊤]_ _**X**_ _[⊤]_ _**XA**_ + [1] _[ −]_ _[λ]_ diag( _∥_ ( _**XA**_ )1 _,_ : _∥_ [2] 2 _[, . . .,][ ∥]_ [(] _**[XA]**_ [)] _[r,]_ [:] _[∥]_ [2] 2 [)] _**B**_ _,_

_λ_


hence the effective gradient norm for _**A**_ is 0 during the first few steps because of _**B**_ being 0,
while the gradient norm for _**B**_ will be high _∥_ _**A**_ _[⊤]_ _**X**_ _[⊤]_ ( _**Y**_ _−_ _**XW**_ ) _∥_ [2] _F_ _[≫]_ [0–regardless] [of] [the]
Dropout rate employed. While such issue only concerns the first few training steps, it is
clear that it will be detrimental in a finetuning regime where the total number of training
steps is limited. We note that if _**A**_ is zero-initialized instead of _**B**_, our entire argument still
holds as the same slow training dynamic appears albeit with respect to _**A**_ instead of _**B**_ .
Our findings support the conclusion of Hayou et al. (2024b) that demonstrated how _**A**_ and
_**B**_ should receive different learning rates to improve LoRA’s performances.


**Dropout** **further** **slows** **down** **the** **escape** **from** 0 **.** An additional issue arises when using
Dropout. In that setting, the escape of _**B**_ from 0, which is needed for _**A**_ to also learn and
for the LoRA module to be effective, will be further slowed down. To better characterize
that effect, let’s study the close-form regularization impact of Dropout using the expected
loss derived in section 3.1. As per the full training regime, we see that Dropout acts as a
regularization on _**A**_ and _**B**_ based on their alignment with _**X**_ . In fact, taking derivative with


6


Figure 3: Depiction of the norm of _**A**_ ( **left** ), the norm of _**B**_ ( **middle** ) and training loss ( **right** ) for
a MNIST LoRA finetuning experiment. We see that as training progresses ( **x-axis** ) as the impact
of increased Dropout probability ( **colors** ) has a **disproportionate** **regularization** **impact** **on** _**B**_
**while** **barely** **impacting** **the** **norm** **of** _**A**_ **,** **indicating** **an** **asymmetry** **in** **Dropout’s** **implicit**
**regularization** **that** **makes** **LoRA** **slow** **to** **train** .


respect to the loss, we see that the orange contributing term’s gradient is given by



_∇_ _**A**_


_∇_ _**B**_




- 1 - - _r_ _∥_ _**X**_ ( _**A**_ ): _,i_ ( _**B**_ ) _i,_ : _∥_ [2] _F_ [=] - 1 - _**X**_ _[⊤]_ _**XA**_ diag( _∥_ _**B**_ 1 _,_ : _∥_ [2] 2 _[, . . .,][ ∥]_ _**[B]**_ _[r,]_ [:] _[∥]_ 2 [2][)] _[,]_
_λ_ _[−]_ [1] _λ_ _[−]_ [1]

_i_ =1

- 1 - - _r_ _∥_ _**X**_ ( _**A**_ ): _,i_ ( _**B**_ ) _i,_ : _∥_ [2] _F_ [=] - 1 - diag( _∥_ ( _**XA**_ )1 _,_ : _∥_ [2] 2 _[, . . .,][ ∥]_ [(] _**[XA]**_ [)] _[r,]_ [:] _[∥]_ 2 [2][)] _**[B]**_ _[.]_
_λ_ _[−]_ [1] _λ_ _[−]_ [1]

_i_ =1



Hence, Dropout with LoRA regularizes the matrices _**A**_ and _**B**_ using a weight decay type of
regularization but weighted by the squared _ℓ_ 2 norm of the rows of _**B**_ and the squared _ℓ_ 2 norm
of the columns of _**XA**_, respectively. Those findings bring to light an unfair regularization
impact of Dropout with LoRA. At initialization, i.e., when _**B**_ = 0, the strength of the
regularizer on _**A**_ will be null. Yet, the strength of the regularizer on _**B**_ is large as it is
equal to the norm of _**XA**_ which, even at initialization, will be largely greater than 0. This
is concerning since not only _**B**_ starts from a zero-norm initialization opposed to _**A**_, but
also its regularization is stronger than that of _**A**_ . We depict that dynamic in a practical
scenario in fig. 3. We observe that the impact of Dropout’s regularization, as measured
by varying the value of _λ_, is minimal on the training dynamic of _**A**_, only altering the final
norm by about 30%, while the impact of Dropout’s regularization on _**B**_ is drastic, producing
solutions with norms varying by more than 500%.


3.3 Third Flaw: Ripple Effect Of Scaling Factor


The third and last flaw we investigate deals with the scaling factor. While section 3.1 and
section 3.2 considered it to be 1 without loss of generality, we now use back the value from
definition 1, i.e., using _η_ = _[α]_ _r_ [as] [the] _[Scaling]_ _[Factor]_ [.]

The scaling factor plays an important role to match _||_ _**BA**_ _||_ to a comparable level with
_||_ _**W**_ _||_ . Despite its effectiveness, the scaling factor creates a ripple effect across layers of a
LLM and may make finetuning unstable. Hu et al. (2021) discussed the importance of the
scaling factor and suggest to tune it carefully to prevent _**BA**_ from overwhelming _**W**_ . From a
different perspective, Houlsby et al. (2019) empirically showed the scale of the initialization
of _**BA**_ can negatively impact validation accuracy. Later, Hayou et al. (2024a) argued that
for the best performance, either _**A**_ or _**B**_ must be initialized at 0.


To illustrate the ripple effect, we adopt a multi-linear model which is a simplified version of
the toy model in Hayou et al. (2024b).


_fl_ ( _**x**_ ) = _**W**_ _lfl−_ 1( _**x**_ ) _,_ _l ∈_ [ _L_ ] (2)


where _L ≥_ 1 is the number of layers. Applying LoRA at each layer gives


_fl_ ( _**x**_ ) = ( _**W**_ _l_ + _η_ _**B**_ _l_ _**A**_ _l_ ) _fl−_ 1( _**x**_ )


7


Figure 4: Test set performance gap ( **y-axis** ) between the close-form Dropout regularization
and its empirical estimate as a function of training steps ( **x-axis** ). We observe that **the**
**benefit** **of** **Dropout** **as** **a** **regularizer** **falls** **short** **for** **finetuning** **(small** **number**
**of** **training** **steps)** **compared** **to** **pretraining** **regimes** **(large** **number** **of** **trainign**
**steps)** .


Expanding the equation, we have _fL_ ( _**x**_ ) = ( _**W**_ _L_ + _η_ _**B**_ _L_ _**A**_ _L_ ) _..._ ( _**W**_ 1 + _η_ _**B**_ 1 _**A**_ 1) _**x**_ . Let _||·||M_ be
a matrix norm induced by a vector norm _||·||v_ . Applying Cauchy-Schwartz and the triangle
inequality, we have


_||fL_ ( _**x**_ ) _|| ≤||fL_ ( _**x**_ ) _||v_ = _||_ ( _**W**_ _L_ + _η_ _**B**_ _L_ _**A**_ _L_ ) _..._ ( _**W**_ 1 + _η_ _**B**_ 1 _**A**_ 1) _||M_ _· ||_ _**x**_ _||v_
_≤_ ( _||_ _**W**_ _L||_ + _η||_ _**B**_ _L_ _**A**_ _L||_ ) _..._ ( _||_ _**W**_ 1 _||_ + _η||_ _**B**_ 1 _**A**_ 1 _||_ ) _||_ _**x**_ _||_



= _C_ (1 + _η_ _[||]_ _**[B]**_ _[L]_ _**[A]**_ _[L][||]_



_||_ _**W**_ 1 _||_ [)] _[||]_ _**[x]**_ _[||]_




_**[B]**_ _[L]_ _**[A]**_ _[L][||]_ _[||]_ _**[B]**_ [1] _**[A]**_ [1] _[||]_

_||_ _**W**_ _L||_ [)] _[...]_ [(1 +] _[ η]_ _||_ _**W**_ 1 _||_



_≤_ _C_ (1 + _η_ ¯ _m_ ) _[L]_ _||_ _**x**_ _||_ = Θ((1 + _η_ ) _[L]_ )



_||_ _**B**_ _l_ _**A**_ _l||_
_l∈L_ _||_ _**W**_ _||_



where _C_ = _||_ _**W**_ _L||...||_ _**W**_ 1 _||_ is a constant, and _m_ ¯ = _L_ 1 


where _C_ = _||_ _**W**_ _L||...||_ _**W**_ 1 _||_ is a constant, and _m_ ¯ = _L_ - _l∈L_ _||_ _**W**_ _l_ _Ll||_ [is] [also] [a] [constant] [in] [a]

single forward pass. Notice that all the inequalities are tight.


**Proposition** **1.** (Ripple Effect) In the worst case, a constant scaling factor _η_ may cause
the final output of a single forward pass of a LoRA finetuned model to grow exponentially
_w.r.t._ the number of layers in the model.


We also note that proposition 1 is especially limiting for LLMs that most commonly resort
to increased depth rather than increased width to scale up their capacity (Hestness et al.,
2017).


3.4 Empirical validation of the harmful impact of Dropout for short

fine-tuning


Because we were able to derive the expectation in close-form, we can now perform LoRA
fine-tuning on the expected loss to see how the idealised performance varies. To that end,
we propose a simple experiment with a 3-layer MLP on MNIST. We pretrain the model on
a subset of 4096 training set images, and then perform LoRA fine-tunining on another set
of 512 training images. We measure the gap in the test loss when training on the idealized
(expected) loss and on the empirical loss on the test set throughout finetuning in fig. 4. We
clearly observe that not only the gap consistently increases with the Dropout rate, but also
that the gap culminates after a few hundred training steps and then slowly goes down. In
short, the detrimental impact of Dropout is maximum during short finetuning episodes.


8


Figure 5: **Left** : LoRA with varying Dropout rates: **High** **value** **of** **Dropout** **provides** **the**
**strongest** **performance** **after** **long** **fine-tuning** **and** **the** **weakest** **performance** **after** **short**
**fine-tuning** . Each line is an average of 3 runs. X-axis is epochs, and Y-axis is accuracy. **Right** :
ALLoRA escapes from 0 rapidly, and then tapers off into a measured move. The starting phase
matches that of LoRA with a much higher learning rate. LoRA with a lower learning rate can reach
the same level of _L_ [2] norm but much slower. This finding echoes fig. 1 that showed how Dropout’s
induced noise does not converge until long training is employed.


Moving to LLMs, we also confirm that simplified model’s intuition with LLM experiments
below. We run experiments with **Qwen2-0.5B** on **Bias** **in** **Bios**, a classification task to
predict the job of an employee given the job description, for various dropout rates and up
to 10 epochs. We note that 10 epochs is already a large number of finetuning iterations for
practical scenarios. It shows that large dropout rates successfully avoid overfitting, but at
the cost of lower accuracy at lower number of epochs, while no dropout sees higher accuracy
at lower number of epochs, but will overfit at later epochs. See fig. 5 Left and table 5.


Having concluded our brief tour of LoRA’s possible shortcomings when it comes to finetuning LLMs in a few shots, we now propose to study our attempt at improving LoRA
through a novel parametrization.


4 ALLoRA: Escaping LoRA’s Flaws for Fine-Tuning


4.1 Deconstructing LoRA


Section 3 summarized three flaws of LoRA, which we show can be addressed by a single
solution: ALLoRA.


First we establish the underlying links among dropout, scaling factor, and learning rate.
Consider the LoRA finetuning of a single layer as in eq. (2), _f_ ( _**x**_ ) = ( _**W**_ + _η_ _**BA**_ ) _**x**_ . Following
Hayou et al. (2024b) and without loss of generality, we can simplify the model by assuming
_**W**_ = 0, which is equivalent to defining _**y**_ ˜ = _**y**_ _−_ _**W x**_, and rewriting the loss function by _**y**_ ˜.
Also assuming _η_ = 1, we have _f_ ( _**x**_ ) = _**BAx**_ . The goal is to minimize loss _L_ whose gradient
is _g_ = _∂_ ( _∂_ _**BA**_ _L_ ) [.] _[f]_ [(] _**[x]**_ [)] _[ ∈]_ [R] _[n]_ [1] [is] [a] [column] [vector.] [Expanding] [it] [per] [row] [gives]


( _f_ ( _**x**_ )) _i_ = ( _**BA**_ ) _i,_ : _**x**_ _,_ _i ∈_ [ _n_ 1] (3)



The effect of dropping out ( _f_ ( _**x**_ )) _i_ for a given _i_ is equivalent to applying a per-row scaling
factor _ηi_ = 0 to ( _**BA**_ ) _i,_ :. Note that this is true only for ( _**BA**_ ) _i,_ :, the effect on ( _**BA**_ ) _j,_ : _, j_ = _i_
is slightly different. Since _[dη][·]_ _dx_ _[f]_ [(] _[x]_ [)] = _η_ _[df]_ _x_ [(] _[x]_ [)], _ηi_ = 0 is implicitly applied to the _i_ -th row of the

gradient _gi_ = ( _∂_ ( _∂_ _**BA**_ _L_ ) [)] _[i,]_ [:][,] [which] [is] [again] [a] [scaling] [factor] [applied] [to] [the] [learning] [rate] _[l]_ [.]


The observation reveals that both scaling factor and dropout are adaptions on LoRA output
_f_ ( _x_ ), and both have effects on gradient. We are inspired to formalize a general framework
that subsumes both, within which we can use a principled approach to systematically discover novel solutions.

**Definition** **2.** (Adaptive Learning) Consider a single layer linear model _f_ ( _**x**_ ) = _**BAx**_ with
gradient _g_ ( _**x**_ ) = _[∂]_ _∂_ _[L]_ ( [(] _**BA**_ _[f]_ [(] _**[x]**_ ) [))] [.] [Let] _[Output]_ _[Adaptor]_ [be] [a] [function] _[f][o]_ [:] [R] _[n]_ [1] _[→]_ [R] _[n]_ [1][,] _[Gradient]_




_[·]_ _dx_ _[f]_ [(] _[x]_ [)] = _η_ _[df]_ _x_ [(] _[x]_ [)]



The observation reveals that both scaling factor and dropout are adaptions on LoRA output
_f_ ( _x_ ), and both have effects on gradient. We are inspired to formalize a general framework
that subsumes both, within which we can use a principled approach to systematically discover novel solutions.

**Definition** **2.** (Adaptive Learning) Consider a single layer linear model _f_ ( _**x**_ ) = _**BAx**_ with
gradient _g_ ( _**x**_ ) = _[∂][L]_ [(] _[f]_ [(] _**[x]**_ [))] [.] [Let] _[Output]_ _[Adaptor]_ [be] [a] [function] _[f][o]_ [:] [R] _[n]_ [1] _[→]_ [R] _[n]_ [1][,] _[Gradient]_



9


_Adaptor_ be a function _fg_ : R _[n]_ [1] _[×][n]_ [2] _→_ R _[n]_ [1] _[×][n]_ [2] . Define adapted output _f_ [˜] and adapted
gradient _g_ ˜ by

           - _f_ ˜ = _fo ◦_ _f_
(4)
_g_ ˜ = _fg ◦_ _g_

Adaptive learning is to use the adapted _f_ [˜] and _g_ ˜ in place of _f_ and _g_ respectively in the
learning process.


Let _I_ : _x_ _�→_ _x_ be the identity function. Then a natural corollary is that all learning is
adaptive learning (when _fo_ = _I_ and _fg_ = _I_ ). Note that _L_ is a function of _f_ ( _**x**_ ), hence

_g_ ( _**x**_ ) = _∂∂_ (( _L◦_ _**BA**_ _f_ )) [.] [Use] _[f]_ [˜] [in] [place] [of] _[f]_ [defines] [a] [naturally] [adapted] [gradient] _[g]_ [˜] [=] _∂∂_ (( _L◦_ _**BA**_ _f_ [˜] )) [=]

_∂_ ( _∂L◦_ ( _**BA**_ _fo◦_ ) _f_ ) [.] [When] [it’s] [clear] [from] [the] [context,] [we] [omit] _[g]_ [˜] [if] [it’s] [naturally] [defined] [by] [a] [non-]

trivial _f_ [˜] .


4.2 ALLoRA: Less Hyper-Parameters and More Stability for Finetuning


Under the Adaptive Learning framework, scaling factor is define by _fo_ = _κ_ : _x �→_ _ηx_ .

           - _f_ ˜ = _κ ◦_ _f_ = _ηf_
(5)
_g_ ˜ = _κ ◦_ _f_ = _ηg_


One idea to reduce the ripple effect while keeping the positive effect of scaling factor is to
force _fo_ = _I_, while keeping _g_ ˜ intact, which is to use a larger learning rate _η · l_ . Nonetheless,
a fixed learning rate cannot simultaneously achieve both fast escape from 0 and, once away
from 0, measured discovery of optimal direction. We think an adaptive learning rate that
is inversely proportional to _||_ ( _**BA**_ ) _i,_ : _||_ is a good candidate to realize our idea. We use the
function 1 _/_ ~~�~~ _||_ ( _**BA**_ ) _i,_ : _||_ + 1 _/η_ [2] which reaches maximum _η_ at _||_ ( _**BA**_ ) _i,_ : _||_ = 0 and then tapers
down when _||_ ( _**BA**_ ) _i,_ : _||_ increases (fig. 6).


Formally, ALLoRA is defined by

       - _f_ ˜ = _I_ _◦_ _f_
_g_ ˜ _i_ = 1 _/_            - _||_ ( _**BA**_ ) _i,_ : _||_ + 1 _/η_ [2] _· gi,_ _i ∈_ [ _n_ 1]


where _η_ is a hyperparameter. Note that this does not introduce a new hyperparameter. We
split learning rate into a constant base learning rate _lb_ and _η_, and the effective learning rate
is _η · lb_ .


One more implementation detail is the backward pass computes, in addition to the gradients
of _**A**_ and _**B**_, also the gradient of the input from layer below, and propagate which back to
the layer below. We only modify the gradients of _**A**_ and _**B**_, but not that of the input. This
helps further restrict the changes within each layer and reduce ripple effect.


To quickly verify our idea, we add probing code to trace the _L_ [2] norm of row vectors of _**BA**_ .
As shown in fig. 5 Right, adaptive learning rate escapes from 0 rapidly, the speed matches
with LoRA with a learning rate that is _η · lb_ . Then it finds an approriate level and enters
measured discovery of optimal directions. LoRA with a learning rate lower than _η · lb_ can
reach the same level, but at a much slower pace. The experiment is with **Snowflake** **Arctic**
**XS** and **Rotten** **Tomatoes** .


Note that ALLoRA multiplies different scaling factors to different rows of _**BA**_ ’s gradient
stochastically (because _**A**_ is stochastically initialized and _**BA**_ is stochastically learnt). Intuitively it is a generalization of Dropout which multiplies binary factors (0 or 1 _−_ 1 _p_ [) to different]
rows stochastically. We hypothesize that ALLoRA may recover some regularisation effect
of Dropout and invite researchers to find a theoretical proof.


4.3 A Family of Adaptive Solutions


We adopt a principled approach to explore other reasonable designs that fall into the adaptive learning framework defined by definition 2.


10


Table 1: Accuracy comparison of various LoRA ranks on **Qwen2-0.5B** and **Emotion** . LoRA’s
and DoRA’s learning rate _l_ = 1 _e −_ 4, ALLoRA’s base learning rate is _lb_ = 1 _e −_ 4, and _η_ = 1. Each
cell is an average over 5 runs.


Method _r_ = 4 _r_ = 8 _r_ = 16 _r_ = 32 _r_ = 64


LoRA 33.09 34.01 35.19 35.59 38.13
DoRA 33.34 34.14 35.50 36.81 38.07
ALLoRA **33.45** **34.80** **35.61** **37.18** **38.27**


First notice that in ( _f_ ( _**x**_ )) _i_ = ( _**BA**_ ) _i,_ : _**x**_, ( _f_ ( _**x**_ )) _i_ and ( _**BA**_ ) _i,_ : define each other. So instead of
adapt the learning by ( _**BA**_ ) _i,_ :, we can also adapt it by ( _f_ ( _**x**_ )) _i_, which is _Output-Dependent_,
or ALLoRA-OD, defined by

       - _f_ ˜ = _I_ _◦_ _f_
_g_ ˜ _i_ = 1 _/_ ~~�~~ _|_ ( _f_ ( _**x**_ )) _i|_ + 1 _/η_ [2] _· gi,_ _i ∈_ [ _n_ 1]


Note that ( _f_ ( _**x**_ )) _i_ is a scalar, hence we use its absolute value. Qualitatively, ALLoRA-OD
subjects to the stochastic noise in _**x**_ because ( _f_ ( _**x**_ )) _i_ = ( _**BA**_ ) _i,_ : _**x**_ . According to Smith et al.
(2021), this type of stochastic noise is an implicit regularization. Our conjecture is that it
may drag down the accuracy just as dropout does, and therefore ALLoRA-OD may not be
as good as ALLoRA.


Given the link between learning rate and scaling factor, we may achieve similar effect by
switching from adaptive learning rate to _Adaptive_ _Scaling_ _Factor_, or ASF-LoRA, defined by


_f_ ˜ _i_ = 1 _/_ ~~�~~ _|_ ( _f_ ( _**x**_ )) _i|_ + 1 _/η_ [2] _· fi,_ _i ∈_ [ _n_ 1]


Note that _g_ ˜ is naturally defined by using _f_ [˜] in place of _f_ . The potential downside is that it
introduces ripple effect across layers, which may blur accuracy. And our conjecture is again
ASF-LoRA may not be as good as ALLoRA.


One more caveat of ASF-LoRA is that we cannot merge _**BA**_ back to _**W**_ as we need to apply
_fo_ to the LoRA output.


4.4 Empirical Validation: Perception Tasks


Our first set of experiments gauges the performance of ALLoRA on perception tasks. Mainstream LLMs nowadays are mostly pretrained by next token prediction, which is good for
generative tasks, but may not be a good fit for perception tasks such as Natural Language
Understanding (NLU) and Sentiment Analysis (SA). In fact, we observe subpar accuracy
when finetuning popular open-weight models for NLU and SA tasks (see table 6). We hope
to show that ALLoRA may help boost the accuracy for perception tasks.


For our experiments, we pick three midsized LLMs: **Qwen2-0.5B**, **Snowflake-Artic-L**,
and **OpenELM-450M**, and four NLU and SA datasets: **Bias** **in** **Bios**, **Emotion**, **Rotten**
**Tomatoes**, and **Yelp** **Review** . To demonstrate the stability of ALLoRA, we run the
experiments with various _η_ [2] _∈{_ 1 _,_ 2 _,_ 4 _}_ with a fixed baselin _√_ e learning rate _lb_ = 1 _e_ _−_ 4. To be
fair for LoRA, we run LoRA at learning rate _l ∈{_ 1 _e −_ 4 _,_ 2 _e −_ 4 _,_ 2 _e −_ 4 _}_, respectively. We

finetune for 2 epochs. Each experiment is run 5 times and we report average final accuracy.
Table 2 Left shows the accuracy gap between ALLoRA and LoRA, where positive numbers
indicate ALLoRA has better accuracy. The result shows that ALLoRA in general admits
better accuracy over plain LoRA. Average improvement over all cases is 0 _._ 3%.


In the experiment, the dropout rate for ALLoRA is 0 _._ 0 and that for LoRA is 0 _._ 05. We
also run ALLoRA+D, the version of ALLoRA with **D** ropout, also at dropout rate 0 _._ 05.
Table 2 Right shows that there is no evident difference between ALLoRA and ALLoRA+D,
matching our theoretical result from section 3.1.

Since _η_ originates from _[α]_ _r_ [in] [definition] [1,] [we] [also] [run] [at] [various] [LoRA] [ranks] _[r]_ [,] [and] [the]

results show that ALLoRA’s advantage is consistent across different _r_ (table 1).


11


Table 2: Accuracy gap between ALLoRA and LoRA. Each cell is an average of 5 runs. **Left** :
ALLoRA admits better accuracy than that of LoRA. **Right** : ALLoRA+D, the version with 0 _._ 05
dropout rate, admits comparable accuracy than that of ALLoRA.


Table 3: Accuracy comparison of LLaMA 7B, LLaMA2 7B, and LLaMA3 8B between ALLoRA
and DoRA on eight commonsense reasoning datasets. DoRA results are taken from Liu et al.
(2024a). ALLoRA+D is the version of ALLoRA with 0 _._ 05 dropout rate.


Model # Params
Method BoolQ PIQA SIQA HSwag WGrande ARC-e ARC-c OBQA Avg.
LoRA Rank %



LLaMA-7B
16


LLaMA-7B
32


LLaMA2-7B
16


LLaMA2-7B
32


LLaMA3-8B
16


LLaMA3-8B
32



DoRA 0.43 70.0 82.6 79.7 83.2 80.6 80.6 65.4 77.6 77.5
ALLoRA+D (ours) 0.41 69.4 82.7 78.3 84.8 80.0 80.9 65.7 79.2 **77.6**
ALLoRA (ours) 0.41 69.2 80.8 78.5 83.9 81.1 80.8 65.2 78.2 77.2


DoRA 0.84 69.7 83.4 78.6 87.2 81.0 81.9 66.2 79.2 78.4
ALLoRA+D (ours) 0.83 70.0 82.3 78.1 84.6 82.2 81.0 67.9 81.0 **78.4**
ALLoRA (ours) 0.83 70.2 82.6 78.6 83.8 81.1 81.0 66.3 82.6 78.3


DoRA 0.43 72.0 83.1 79.9 89.1 83.0 84.5 71.0 81.2 80.5
ALLoRA+D (ours) 0.41 71.7 83.7 79.5 91.4 82.4 84.3 69.2 81.2 80.4
ALLoRA (ours) 0.41 72.4 83.9 80.0 90.8 83.0 84.7 71.3 80.2 **80.8**


DoRA 0.84 71.8 83.7 76.0 89.1 82.6 83.7 68.2 82.4 79.7
ALLoRA+D (ours) 0.83 72.2 83.1 79.6 91.2 84.5 84.5 71.0 80.0 80.8
ALLoRA (ours) 0.83 72.3 83.8 79.3 91.4 83.0 85.0 71.2 82.2 **81.0**


DoRA 0.35 74.5 88.8 80.3 95.5 84.7 90.1 79.1 87.2 85.0
ALLoRA+D (ours) 0.35 75.2 88.9 80.8 95.6 84.7 90.2 80.6 85.8 85.2
ALLoRA (ours) 0.35 74.5 89.1 80.4 95.5 85.8 90.7 80.3 86.0 **85.3**


DoRA 0.71 74.6 89.3 79.9 95.5 85.6 90.5 80.4 85.8 85.2
ALLoRA+D (ours) 0.70 74.5 88.9 81.8 95.9 86.3 90.4 80.5 87.6 **85.8**
ALLoRA (ours) 0.70 75.1 88.7 81.8 95.8 85.4 91.0 81.1 86.6 85.7



4.5 Empirical Validation: Commonsense Reasoning


We also compare ALLoRA with DoRA (Liu et al. (2024a)), a recent LoRA variant that
demonstrated superb performance over a range of PEFT methods. Since DoRA results are
universally better than other PEFT methods, we only compare ALLoRA to DoRA. We
run experiments on **LLaMA-7B**, **LLaMA2-7B**, and **LLaMA3-8B** on 8 **Commonsense**
tasks. Following DoRA’s setup, for each model, we run both ALLoRA and ALLoRA+D with
LoRA rank _r_ _∈{_ 16 _,_ 32 _}_ and for 3 epochs. Table 3 shows that for all cases, either ALLoRA
or ALLoRA+D has the best average accuracy. On average, ALLoRA and ALLoRA+D each
boosted accuracy by 0 _._ 3% over DoRA.


Note that we run experiments with various _η_ [2] _∈{_ 1 _,_ 2 _,_ 4 _}_ and report the best accuracy, this
follows DoRA’s practices to run with various learning rate _l_ _∈{_ 1 _e −_ 4 _,_ 2 _e −_ 4 _}_ and report
the best.


In table 3 we also report the number of trainable parameters as a percentage of the number of
pretrained parameters. Since ALLoRA does not introduce additional trainable parameters,
its trainable parameters are slightly lower than that of DoRA.


12


Table 4: Accuracy gap between ALLoRA and other adaptive approaches. Each cell is an average
of 5 runs. **Top** **left** : ALLoRA admits better accuracy than that of ALLoRA-OD, where learning
rate is LoRA **O** utput- **D** ependent. **Top** **right** : ALLoRA admits better accuracy than that of ASFLoRA, where an **A** daptive **S** cale **F** actor is applied to LoRA output. **Bottom** **left** : ALLoRA
admits better accuracy than that of LoRA with a fixed scaling factor. **Bottom** **right** : Adaptive
scale factor is not better than a fixed scale factor.


5 Ablation Study


Using the same setup in section 4.4, we run experiments with ALLoRA-OD, the outputdependent variant, and ASF-LoRA, the adaptive scaling factor variant. We also run LoRA
with comparable fixed scaling factors to form an objective baseline for ASF-LoRA.


5.1 ALLoRA-OD


Table 4 Top Left shows the accuracy gap between ALLoRA and ALLoRA-OD. A positive
number indicates that ALLoRA has better accuracy. Overall speaking, ALLoRA has better
accuracy than ALLoRA-OD. But the difference is moderate, as average improvement over
all cases is 0 _._ 4%.


The result matches our conjecture that stochastic noise experienced by ALLoRA-OD might
have dragged down accuracy at early epochs.


5.2 ASF-LoRA and LoRA with Fixed Scaling Factor


Since a scaling factor on output is implicitly also a scaling factor on gradient, we use the
same _η_ when comparing between ALLoRA and ASF-LoRA, i.e., the gradient adaptor _fg_ in
ALLoRA and the output adaptor _fo_ in ASF-LoRA use the same _η_ .


Table 4 Top Right shows the accuracy gap between ALLoRA and ASF-LoRA. A positive
number indicates that ALLoRA has better accuracy. ALLoRA has a significant advantage over ASF-LoRA as average improvement over all cases is 1 _._ 1%. Since we know that
ALLoRA-OD is only slightly worse than ALLoRA, the evidence leans toward that Adaptive
Learning Rate is in general a better solution family than Adaptive Scaling Factor.



_√_

_[α]_

_r_ _[∈{]_ [1] _[,]_



We also run LoRA at comparable fixed scaling factors _[α]_



We also run LoRA at comparable fixed scaling factors _r_ _[∈{]_ [1] _[,]_ 2 _,_ 2 _}_ . The results, as shown

in table 4 Bottom, show that



13


   - ASF-LoRA is not a competitive method, as over half of cases see ASF-LoRA’s accuracy significantly lower than LoRA with a comparable fixed scaling factor (positive
numbers in table 4 Bottom Right).


   - ALLoRA is significantly better than LoRA with a comparable fixed scaling factor,
as average improvement over all cases is 0 _._ 9%.


6 Conclusion and Future Work


This paper identifies three major flaws of LoRA, namely dropout, zero-initialization, and
scaling factor. We conducted principled analysis and proved that dropout is not a musthave in the finetuning regime. After uncovering the hidden connection between dropout,
scaling factor, and learning rate, we proposed a unified adaptive learning framework to
address them all: ALLoRA. Empirical results show that ALLoRA admits better accuracy
than plain LoRA over multiple backbones, datasets, and learning rates; and better accuracy
than recent successful LoRA variants such as DoRA. Ablation study shows that ALLoRA
is the optimal in a family of adaptive methods.


We list a few interesting research directions and invite researchers to explore the frontier
opened-up by our research:


   - The adaptive learning framework introduced by this paper is generic and may find
broad applications beyond LoRA. Other use cases such as pretraining may not have
the constraints that the weight matrix must be initialized at 0. But they may have
other types of constraints, which may be solved by adaptive learning with a different
adaptor function.


   - Within the LoRA use case, we only examine one particular adaptor function, there
could be other adaptor functions that have superior performance.


   - We only provide empirical evidence that ALLoRA admits better accuracy and hypothesize that ALLoRA is implicitly a regularization. Theoretical guarantee is
needed, especially for the convoluted case where the base model has multiple layers.


   - Starting from 0 weights may avoid the lottery ticket hypothesis (Frankle & Carbin
(2019)), for good or bad, where adaptive learning rate can be a handy tool.


References


KR Chowdhary. Natural language processing. _Fundamentals_ _of_ _artificial_ _intelligence_, pp.
603–649, 2020.


Abhimanyu Dubey, Abhinav Jauhri, Abhinav Pandey, Abhishek Kadian, Ahmad Al-Dahle,
Aiesha Letman, Akhil Mathur, Alan Schelten, Amy Yang, Angela Fan, et al. The llama
3 herd of models. _arXiv_ _preprint_ _arXiv:2407.21783_, 2024.


Jonathan Frankle and Michael Carbin. The lottery ticket hypothesis: Finding sparse, trainable neural networks. In _International_ _Conference_ _on_ _Learning_ _Representations_, 2019.


Soufiane Hayou, Nikhil Ghosh, and Bin Yu. The impact of initialization on lora finetuning
dynamics. _arXiv_ _preprint_ _arXiv:2406.08447_, 2024a.


Soufiane Hayou, Nikhil Ghosh, and Bin Yu. Lora+: Efficient low rank adaptation of large
models. _arXiv_ _preprint_ _arXiv:2402.12354_, 2024b.


Junxian He, Chunting Zhou, Xuezhe Ma, Taylor Berg-Kirkpatrick, and Graham Neubig. Towards a unified view of parameter-efficient transfer learning. In _International_ _Conference_
_on_ _Learning_ _Representations_, 2022.


Joel Hestness, Sharan Narang, Newsha Ardalani, Gregory Diamos, Heewoo Jun, Hassan
Kianinejad, Md Mostofa Ali Patwary, Yang Yang, and Yanqi Zhou. Deep learning scaling
is predictable, empirically. _arXiv_ _preprint_ _arXiv:1712.00409_, 2017.


14


Jordan Hoffmann, Sebastian Borgeaud, Arthur Mensch, Elena Buchatskaya, Trevor Cai,
Eliza Rutherford, Diego de Las Casas, Lisa Anne Hendricks, Johannes Welbl, Aidan Clark,
et al. Training compute-optimal large language models. _arXiv_ _preprint_ _arXiv:2203.15556_,
2022.


Neil Houlsby, Andrei Giurgiu, Stanislaw Jastrzebski, Bruna Morrone, Quentin De Laroussilhe, Andrea Gesmundo, Mona Attariyan, and Sylvain Gelly. Parameter-efficient transfer
learning for nlp. In _International_ _conference_ _on_ _machine_ _learning_, pp. 2790–2799. PMLR,
2019.


Edward J. Hu, Yelong Shen, Phillip Wallis, Zeyuan AllenZhu, Yuanzhi Li, Shean Wang,
Lu Wang, and Weizhu Chen. Lora: Low-rank adaptation of large language models. _arXiv_
_preprint_ _arXiv:2106.09685_, 2021.


Nam Hyeon-Woo, Moon Ye-Bin, and Tae-Hyun Oh. Fedpara: Low-rank hadamard product
for communication-efficient federated learning. In _ICLR_ Hyeon-Woo et al. (2022).


Uijeong Jang, Jason D Lee, and Ernest K Ryu. Lora training in the ntk regime has no
spurious local minima. _arXiv_ _preprint_ _arXiv:2402.11867_, 2024.


Albert Q Jiang, Alexandre Sablayrolles, Arthur Mensch, Chris Bamford, Devendra Singh
Chaplot, Diego de las Casas, Florian Bressand, Gianna Lengyel, Guillaume Lample, Lucile
Saulnier, et al. Mistral 7b. _arXiv_ _preprint_ _arXiv:2310.06825_, 2023.


Rabeeh Karimi Mahabadi, James Henderson, and Sebastian Ruder. Compacter: Efficient
low-rank hypercomplex adapter layers. In M. Ranzato, A. Beygelzimer, Y. Dauphin,
P.S. Liang, and J. Wortman Vaughan (eds.), _Advances_ _in_ _Neural_ _Information_ _Processing_
_Systems_, volume 34, pp. 1022–1035. Curran Associates, Inc., 2021a.


Rabeeh Karimi Mahabadi, Sebastian Ruder, Mostafa Dehghani, and James Henderson.
Parameter-efficient multi-task fine-tuning for transformers via shared hypernetworks. In
_Annual_ _Meeting_ _of_ _the_ _Association_ _for_ _Computational_ _Linguistics_, 2021b.


Dawid Jan Kopiczko, Tijmen Blankevoort, and Yuki Markus Asano. Vera: Vector-based
random matrix adaptation. _CoRR_, abs/2310.11454, 2023.


Brian Lester, Rami Al-Rfou, and Noah Constant. The power of scale for parameter-efficient
prompt tuning. In Lester et al. (2021), pp. 3045–3059.


Shih-Yang Liu, Chien-Yi Wang, Hongxu Yin, Pavlo Molchanov, Yu-Chiang Frank Wang,
Kwang-Ting Cheng, and Min-Hung Chen. Dora: Weight-decomposed low-rank adaptation. _arXiv_ _preprint_ _arXiv:2402.09353_, 2024a.


Weiyang Liu, Zeju Qiu, Yao Feng, Yuliang Xiu, Yuxuan Xue, Longhui Yu, Haiwen Feng,
Zhen Liu, Juyeon Heo, Songyou Peng, Yandong Wen, Michael J. Black, Adrian Weller, and
Bernhard Sch¨olkopf. Parameter-efficient orthogonal finetuning via butterfly factorization.
In _ICLR_ Liu et al. (2024b).


Sachin Mehta, Mohammad Hossein Sekhavat, Qingqing Cao, Maxwell Horton, Yanzi Jin,
Chenfan Sun, Iman Mirzadeh, Mahyar Najibi, Dmitry Belenko, Peter Zatloukal, and Mohammad Rastegari. OpenELM: An Efficient Language Model Family with Open Training
and Inference Framework. _arXiv.org_, April 2024. URL `[https://arxiv.org/abs/2404.](https://arxiv.org/abs/2404.14619v1)`
`[14619v1](https://arxiv.org/abs/2404.14619v1)` .


Edoardo M Ponti, Alessandro Sordoni, Yoshua Bengio, and Siva Reddy. Combining modular
skills in multitask learning. _arXiv_ _preprint_ _arXiv:2202.13914_, 2022.


Zeju Qiu, Weiyang Liu, Haiwen Feng, Yuxuan Xue, Yao Feng, Zhen Liu, Dan Zhang, Adrian
Weller, and Bernhard Sch¨olkopf. Controlling text-to-image diffusion by orthogonal finetuning. In Qiu et al. (2023).


15


Anastasia Razdaibiedina, Yuning Mao, Madian Khabsa, Mike Lewis, Rui Hou, Jimmy Ba,
and Amjad Almahairi. Residual prompt tuning: improving prompt tuning with residual
reparameterization. In Razdaibiedina et al. (2023), pp. 6740–6757. ISBN 978-1-95942962-3.


Adithya Renduchintala, Tugrul Konuk, and Oleksii Kuchaiev. Tied-lora: Enhacing parameter efficiency of lora with weight tying. _CoRR_, abs/2311.09578, 2023.


Yusuxke Shibata, Takuya Kida, Shuichi Fukamachi, Masayuki Takeda, Ayumi Shinohara,
Takeshi Shinohara, and Setsuo Arikawa. Byte pair encoding: A text compression scheme
that accelerates pattern matching. 1999.


Samuel L Smith, Benoit Dherin, David GT Barrett, and Soham De. On the origin of implicit
regularization in stochastic gradient descent. _arXiv_ _preprint_ _arXiv:2101.12176_, 2021.


Nitish Srivastava, Geoffrey Hinton, Alex Krizhevsky, Ilya Sutskever, and Ruslan Salakhutdinov. Dropout: A simple way to prevent neural networks from overfitting. _Journal_ _of_
_machine_ _learning_ _research_, 15(1):1929–1958, 2014.


Gemma Team, Thomas Mesnard, Cassidy Hardin, Robert Dadashi, Surya Bhupatiraju,
Shreya Pathak, Laurent Sifre, Morgane Rivi`ere, Mihir Sanjay Kale, Juliette Love,
et al. Gemma: Open models based on gemini research and technology. _arXiv_ _preprint_
_arXiv:2403.08295_, 2024.


Hugo Touvron, Louis Martin, Kevin Stone, Peter Albert, Amjad Almahairi, Yasmine Babaei,
Nikolay Bashlykov, Soumya Batra, Prajjwal Bhargava, Shruti Bhosale, et al. Llama 2:
Open foundation and fine-tuned chat models. _arXiv_ _preprint_ _arXiv:2307.09288_, 2023.


Stefan Wager, Sida Wang, and Percy Liang. Dropout training as adaptive regularization. In
Christopher J. C. Burges, L´eon Bottou, Zoubin Ghahramani, and Kilian Q. Weinberger
(eds.), _NIPS_, pp. 351–359, 2013.


Sida Wang and Christopher Manning. Fast dropout training. In _Proceedings_ _of_ _the_ _30th_
_International_ _Conference_ _on_ _Machine_ _Learning_, pp. 118–126, 2013.


Yaqing Wang, Jialin Wu, Tanmaya Dabral, Jiageng Zhang, Geoff Brown, Chun-Ta Lu,
Frederick Liu, Yi Liang, Bo Pang, Michael Bendersky, et al. Non-intrusive adaptation:
Input-centric parameter-efficient fine-tuning for versatile multimodal modeling. _arXiv_
_preprint_ _arXiv:2310.12100_, 2023.


Shih-Ying Yeh, Yu-Guan Hsieh, Zhidong Gao, Bernard B. W. Yang, Giyeong Oh, and
Yanmin Gong. Navigating text-to-image customization: From lycoris fine-tuning to model
evaluation. In _ICLR_ Yeh et al. (2024).


Fangzhao Zhang and Mert Pilanci. Riemannian preconditioned lora for fine-tuning foundation models. _arXiv_ _preprint_ _arXiv:2402.02347_, 2024.


Qingru Zhang, Minshuo Chen, Alexander Bukharin, Pengcheng He, Yu Cheng, Weizhu
Chen, and Tuo Zhao. Adaptive budget allocation for parameter-efficient fine-tuning. In
_ICLR_ Zhang et al. (2023).


Yin Zhang, Rong Jin, and Zhi-Hua Zhou. Understanding bag-of-words model: a statistical
framework. _International_ _journal_ _of_ _machine_ _learning_ _and_ _cybernetics_, 1:43–52, 2010.


Jiawei Zhao, Zhenyu Zhang, Beidi Chen, Zhangyang Wang, Anima Anandkumar, and Yuandong Tian. Galore: Memory-efficient llm training by gradient low-rank projection. _arXiv_
_preprint_ _arXiv:2403.03507_, 2024.


16


Table 5: Reprise of fig. 5 Left depicting that the epoch at which the LoRA fine-tuned model
reaches the best accuracy increases with the Dropout rate, i.e., the larger the probability to drop
dimensions, the more regularization is applied and the better the final performance–but only after
very long fine-tuning.


dropout 0.0 0.05 0.1 0.2 0.4


Acc. at epoch=3 77.92 77.96 77.68 77.44 77.22
Acc. at epoch=10 78.00 79.95 80.50 80.77 80.65
Max acc. 79.81 80.27 80.54 80.78 80.65
Epoch of max acc. 6 8 8 9 10


A Proof of upper bound


_Proof._ To simplify the derivations, we will denote _**Y**_ _−_ _**XW**_ _−_ (( _**XA**_ ) _⊙_ _**V**_ _n_ ) _**B**_ by _**Z**_ _n_ .



_N_

- _∥_ _**Z**_ _n∥_ [2] _F_ _[−]_ [E] - _∥_ _**Z**_ _∥_ [2] _F_ �����

_n_ =1 






E


=E



1

_N_
������








~~�~~
��

- 1

_N_







_∥_ _**Z**_ _n∥_ [2] _F_ _[−]_ [E][ [] _[∥]_ _**[Z]**_ _[∥]_ _F_ [2] []]
_n_ =1



2 []








_N_





~~�~~

 
 
_≤_ �E

 



1

_N_







_N_




_∥_ _**Z**_ _n∥_ [2] _F_ _[−]_ [E][ [] _[∥]_ _**[Z]**_ _[∥]_ _F_ [2] []]
_n_ =1



�2 []












~~�~~

 
 
=�E

 



1

_N_







_N_

- _∥_ _**Z**_ _n∥_ [2] _F_

_n_ =1



�2 []

 _−_ E [ _∥_ _**Z**_ _∥_ [2] _F_ []][2]








~~�~~

 
 
=� [1]

_N_ [2]


~~�~~

 
 
=� [1]

_N_ [2]




~~�~~



- [1]
_N_ [2]


~~�~~



- [1]
_N_ [2]



_N_




_N_ [E][ [] _[∥]_ _**[Z]**_ _[∥]_ _F_ [2] []][2]





E [ _∥_ _**Z**_ _n∥_ [4] _F_ []] _[ −]_ [1]

_N_

_n_ =1



_N_



_n_ =1




E [ _∥_ _**Z**_ _n∥_ [4] _F_ []] _[ −]_ [E][ [] _[∥]_ _**[Z]**_ _[∥]_ _F_ [2] []][2][�]




 - 1

= _F_ []]

_N_ _[V ar]_ [ [] _[∥]_ _**[Z]**_ _[∥]_ [2]



= _[Std]_ ~~_√_~~ - _∥_ _**Z**_ _∥_ [2] _F_ 


~~_√_~~



_N_



B Finetuning Accuracy At Various Dropout Rates


Table 5 contains accuracy of various dropout rates at different number of epochs.


C Adaptive Function


Figure 6 is an adaptive function that provides output value when _|x|_ = 0, and then tapers
down when _|x| >_ 0.


17


Figure 6: Adaptive function 1 _/_        - _|x|_ + 1 _/η_ [2] for _η_ [2] = 1 _,_ 2 _,_ 4.


Table 6: Accuracy comparison of various models, datasets, and learning rates between
ALLoRA and plain LoRA. ALLoRA+D is the version of ALLoRA with 0 _._ 05 dropout rate.
LoRA’s learning rate is _η_ _×_ 1 _e_ _−_ 4, ALLoRA’s and ALLoRA+D’s base learning rate is 1 _e_ _−_ 4.
Each cell is an average over 5 runs.


Qwen2-0.5B Snowflake-Artic-L OpenELM-450M
Learning Rate Method
b-in-b emotion rotten emotion rotten yelp emotion rotten yelp



_η_ [2] = 1 _._ 0
_lb_ = 1 _e −_ 4


_η_ [2] = 2 _._ 0
_lb_ = 1 _e −_ 4


_η_ [2] = 4 _._ 0
_lb_ = 1 _e −_ 4



LoRA 70.81 35.59 53.19 87.06 77.71 63.61 84.98 87.95 71.41
ALLoRA+D (ours) 71.29 37.18 53.64 86.93 **78.29** 63.55 **86.07** **88.20** 71.32
ALLoRA (ours) **71.53** **37.35** **54.33** 86.98 78.19 63.52 86.04 88.11 71.36


LoRA 73.70 37.76 54.32 88.30 79.34 64.26 90.01 88.74 71.62
ALLoRA+D (ours) 73.77 **38.52** 54.67 88.23 **79.44** 64.24 **90.01** 88.95 71.63
ALLoRA (ours) **73.99** 38.09 **55.37** **88.52** 79.16 **64.33** 89.93 **89.04** **71.68**


LoRA 75.60 38.68 54.90 88.95 80.04 64.76 91.33 89.55 71.79
ALLoRA+D (ours) **75.72** 39.00 **55.83** **89.08** **80.24** 64.61 91.27 **89.61** **71.83**
ALLoRA (ours) 75.52 **39.47** 55.68 88.91 **80.24** **64.76** **91.43** 89.47 71.82



D Perception Tasks


Table 6 shows the accuracy data of all of our experiments on perception tasks. Each cell is
an average of 5 runs. ALLoRA is universally better than LoRA in terms of accuracy.


E Ablation


Table 7 shows the accuracy data of all of our ablation study on perception tasks. Each cell
is an average of 5 runs. ALLoRA is universally better than the rest in the family.


18


Table 7: Accuracy comparison of various models, datasets, and learning rates between ALLoRA and other adaptive approaches. for adaptive learning rate approaches, i.e., ALLoRA
and ALLoRA-OD, base learning rate is 1 _e_ _−_ 4. For adaptive scaling factor, i.e., ASF-LoRA,
learning rate is fixed at 1 _e −_ 4, an adaptive scaling factor 1 _/_ ~~�~~ _|x|_ + 1 _/η_ [2] is applied. For
LoRA, a fixed scaling factor _η_ is applied, and learning rate is fixed at 1 _e −_ 4. Each cell is
an average over 5 runs.


Qwen2-0.5B Snowflake-Artic-L OpenELM-450M
_η_ [2] Method
emotion rotten emotion rotten emotion rotten



1 _._ 0


2 _._ 0


4 _._ 0



ALLoRA (ours) **37.35** **54.33** 86.98 **78.19** 86.04 **88.11**
ALLoRA-OD 36.91 52.31 87.24 77.47 86.31 88.11
ASF-LoRA 36.40 53.43 87.30 78.03 83.44 87.58
LoRA _×η_ 35.59 53.19 87.06 77.71 84.98 87.95


ALLoRA (ours) 38.09 **55.37** **88.52** **79.16** **89.93** **89.04**
ALLoRA-OD 38.15 53.55 88.22 79.16 89.86 89.02
ASF-LoRA 37.20 54.17 87.74 78.18 86.26 88.22
LoRA _×η_ 36.61 54.47 87.62 78.72 88.77 88.39


ALLoRA (ours) **39.47** **55.68** 88.91 **80.24** **91.43** **89.47**
ALLoRA-OD 38.67 54.95 88.97 80.21 91.27 89.38
ASF-LoRA 38.45 54.41 87.97 79.23 89.64 88.80
LoRA _×η_ 37.63 53.70 88.49 79.31 90.25 89.08


19


F Code


1 `class` `ALLoRA(torch.autograd.Function):`

2 `rsq_scale` `=` `1.` `/` `4.` `#` `1` `/` `\eta^2`


3

4 `@staticmethod`

5 `def` `forward(ctx,` `input_x,` `weight_A,` `weight_B):`

6 `output` `=` `input_x` `@` `weight_A.t()` `@` `weight_B.t()`

7 `norms` `=` `torch.norm(weight_B` `@` `weight_A,` `dim =1)`

8 `ctx. save_for_backward (input_x,` `weight_A,` `weight_B,` `norms)`

9 `return` `output`


10

11 `@staticmethod`

12 `def` `backward(ctx,` `grad_output):`

13 `input_x,` `weight_A,` `weight_B,` `norms` `=` `ctx. saved_tensors`

14 `accelerate` `=` `1.` `/` `torch.sqrt(norms` `+` `LinearLayer2 .rsq_scale)`

15 `grad_input` `=` `grad_output` `@` `weight_B` `@` `weight_A`

16 `temp` `=` `grad_output.mul(accelerate)` `@` `weight_B`

17 `temp` `=` `torch.transpose(temp,` `1,` `2)`

18 `grad_weight_A` `=` `temp` `@` `input_x`

19 `temp` `=` `grad_output.mul(accelerate).transpose (1,` `2)`

20 `grad_weight_B` `=` `temp` `@` `(input_x` `@` `weight_A.t())`

21 `return` `grad_input,` `grad_weight_A,` `grad_weight_B`


Listing 1: ALLoRA Code


20


