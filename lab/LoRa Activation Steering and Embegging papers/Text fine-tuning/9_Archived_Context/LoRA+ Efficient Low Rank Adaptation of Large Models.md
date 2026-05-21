## **LoRA+: Efficient Low Rank Adaptation of Large Models**

**Soufiane Hayou** [* 1] **Nikhil Ghosh** [* 2] **Bin Yu** [2]



**Abstract**


In this paper, we show that Low Rank Adaptation
(LoRA) as originally introduced in (Hu et al.,
2021) leads to suboptimal finetuning of models
with large width (embedding dimension). This
is due to the fact that adapter matrices _A_ and
_B_ in LoRA are updated with the same learning
rate. Using scaling arguments for large width
networks, we demonstrate that using the same
learning rate for _A_ and _B_ does not allow
efficient feature learning. We then show that this
suboptimality of LoRA can be corrected simply
by setting different learning rates for the LoRA
adapter matrices _A_ and _B_ with a well-chosen
fixed ratio. We call this proposed algorithm
LoRA+. In our extensive experiments, LoRA+
improves performance (1% _−_ 2% improvements)
and finetuning speed (up to _∼_ 2X SpeedUp), at
the same computational cost as LoRA.


**1. Introduction**


State-of-the-art (SOTA) deep learning models all share
a common characteristic: they all have an extremely
large number of parameters (10’s if not 100’s of billions
parameters). Currently, only a few industry labs can
pretrain large language models due to their high training
cost. However, many pretrained models are accessible
either through an API (GPT4, (OpenAI, 2023)) or through
open-source platforms (Llama, (Touvron et al., 2023)).
Most practitioners are interested in using such models
for specific tasks and want to _adapt_ these models to a
new, generally smaller task. This procedure is known as
_finetuning_, where one adjusts the weights of the pretrained
model to improve performance on the new task. However,
due to the size of SOTA models, adapting to down-stream
tasks with full finetuning (finetuning all model parameters)


*Equal contribution 1Simons Institute, UC Berkeley
2Department of Statistics, UC Berkeley. Correspondence
to: Soufiane Hayou <hayou@berkeley.edu>, Nikhil Ghosh
<nikhil_ghosh@berkeley.edu>.


_Proceedings_ _of_ _the_ _41_ _[st]_ _International_ _Conference_ _on_ _Machine_
_Learning_, Vienna, Austria. PMLR 235, 2024. Copyright 2024
by the author(s).



is computationally infeasible as it requires modifying the
weights of the pretrained models using gradient methods
which is a costly process. Besides, a model that has already
learned generally useful representations during pretraining
would not require in-principle significant adaptation of all
parameters. With this intuition, researchers have proposed
a variety of resource-efficient finetuning methods which
typically freeze the pretrained weights and tune only a
small set of newly inserted parameters. Such methods
include prompt tuning (Lester et al., 2021) where a “soft
prompt" is learned and appended to the input, the adapters
method (Houlsby et al., 2019) where lightweight “adapter"
layers are inserted and trained, and ( _IA_ ) [3] (Liu et al.,
2022) where activation vectors are modified with learned
scalings. Another resource-efficient method is known as
_Low_ _Rank_ _Adaptation_ (Hu et al., 2021), or simply LoRA.
In LoRA finetuning, only a low rank matrix, called an
_adapter_, that is added to the pretrained weights is trainable.
The training can be done with any optimizer and in practice
a common choice is Adam (Kingma and Ba, 2014). Since
the trained adapter is low-rank, this effectively reduces the
number of trainable parameters in the fine-tuning process,
significantly decreasing the training cost. On many tasks
such as instruction finetuning, LoRA has been shown
to achieve comparable or better performance compared
with full-finetuning (Wang et al., 2023; Liu et al., 2023),
although on complicated, long form generation tasks, it is
not always as performant. The impressive performance and
the computational savings of LoRA have contributed to it
becoming an industry standard finetuning method.


Efficient use of LoRA requires a careful choice of
hyperparameters: the rank and the learning rate. While
some theoretical guidelines on the choice of the rank in
LoRA exist in the literature (see e.g. Zeng and Lee (2023)),
there are no principled guidelines on how to set the learning
rate, apart from common choices of order 1 _e_ -4.


**Related** **Work.** Dettmers et al. (2023) introduced a
quantized version of LoRA (or QLoRA), which further
reduces computation costs by quantizing pretrained
weights down to as few as four bits. Using QLoRA enables
fine-tuning Llama-65b (Touvron et al., 2023), on a single
consumer GPU while achieving competitive performance
with full-finetuning. To further improve LoRA training
with quantization, Li et al. (2023) introduced a new



1


**Effcient Low Rank Adaptation**



_Figure 1._ The key difference between standard LoRA and
LoRA+ is in how learning rates are set (the matrices _GA_ and
_GB_ are ‘effective’ gradients from AdamW) With standard LoRA,
the learning rate is the same for _A_ and _B_, which provably leads
to suboptimal learning when embedding dimension is large. In
LoRA+, we set the learning rate of _B_ to be _λ×_ that of _A_, where
_λ ≫_ 1 is fixed. We later provide guidelines on how to set _λ_ .


method called LoftQ for computing a better initialization
for quantized training. Additional variations of LoRA
have been proposed such as VeRA (Kopiczko et al., 2023)
which freezes random weight tied adapters and learns
vector scalings of the internal adapter activations. This
achieves a further reduction in the number of trainable
parameters while achieving comparable performance to
LoRA on several NLP finetuning tasks. However, to the
best of our knowledge, there is no principled guidance for
setting LoRA learning rate which is the focus of our work.


**Contributions.** We provide guidelines for setting the
learning rate through a theory of scaling for neural
networks. There is a significant number of works on the
scaling of neural networks from the infinite width/depth
perspective. The approach is simple: take the width/depth
of a neural network to infinity, [1] understand how the
limit depends on the choice of the hyperparameters
in the training process such as the learning rate and
initialization variance, then derive principled choices for
these hyperparameters to achieve some desired goal (e.g.
improve feature learning). Examples of the infinite-width
limit include works on initialization schemes such as (He
et al., 2016; Yang, 2019), or more holistically network
parametrizations such as (Yang and Hu, 2021) where the
authors introduced _µ_ P, a neural network parameterization
ensuring feature learning in the infinite-width limit,
offering precise scaling rules for architecture and learning
rates to maximize feature learning. Examples for the
depth limit include initialization strategies (Schoenholz


1Depending on the model, one might want to scale width
with fixed depth and vice-versa, or both at the same time. See
Appendix A.1 for more details.



et al., 2017a; He et al., 2023; Hayou et al., 2019), block
scaling (see e.g. (Hayou et al., 2021; Hayou, 2023; Noci
et al., 2023)), depth parametrizations (Yang et al., 2023;
Bordelon et al., 2023) etc. Here we propose to use the
same strategy to derive scaling rules for the learning rate in
LoRA for finetuning. More precisely, we study the infinitewidth limit of LoRA finetuning dynamics and show that
standard LoRA setup is suboptimal. We correct this by
introducing a new method called LoRA+ that improves
feature learning in low rank adaptation in the this limit.
The key innovation in LoRA+ is setting different learning
rates for _A_ and _B_ modules (LoRA modules) as explained in
Figure 1. Our theory is validated with extensive empirical
results with different language of models and tasks.


**2. Setup and Definitions**



where _x_ _∈_ R _[d]_ is the input, _L_ _≥_ 1 is the network depth,
( _Fl_ ) _l∈_ [ _L_ ] are mappings that define the layers, _Wl_ _∈_ R _[n][×][n]_

are the hidden weights, where _n_ is the network _width_, and
_Win, Wout_ are input and output embedding weights.


Model (1) is _pretrained_ on some dataset _D_ to perform some
specified task (e.g. next token prediction). Once the model
is pretrained, one can finetune it to improve performance
on some downstream task. To achieve this with relatively
small devices (limited GPUs), resource-efficient finetuning
methods like LoRA significantly reduce the computational
cost by considering low rank weight matrices instead of full
rank finetuning (or simply full finetuning).


**Definition 1** (Low Rank Adapters (LoRA) from (Hu et al.,
2021)) **.** _For_ _any_ _weight_ _matrix_ _W_ _∈_ R _[n]_ [1] _[×][n]_ [2] _in_ _the_
_pretrained_ _model,_ _we_ _constrain_ _its_ _update_ _in_ _the_ _fine-_
_tuning_ _process_ _by_ _representing_ _the_ _latter_ _with_ _a_ _low-rank_
_decomposition_ _W_ = _W_ _[∗]_ + _[α]_ _r_ _[BA][.]_ _[Here,]_ _[only]_ _[the]_ _[weight]_

_matrices B_ _∈_ R _[n]_ [1] _[×][r]_ _, A_ _∈_ R _[r][×][n]_ [2] _are trainable._ _The rank_
_r_ _≪_ min( _n_ 1 _, n_ 2) _and α ∈_ R _are tunable constants._


**Scaling of Neural Networks.** It is well known that as the
width _n_ grows, the network initialization scheme and the
learning should be adapted to avoid numerical instabilities
and ensure efficient learning. For instance, the variance
of the initialization weights (in hidden layers) should
scale 1 _/n_ to prevent arbitrarily large pre-activations as we
increase model width _n_ (e.g. He init (He et al., 2016)).
To derive such scaling rules, a principled approach consist



Our methodology in this paper is model agnostic and
applies to general neural network models. Let us consider
a neural network of the form

 _Yin_ ( _x_ ) = _Winx,_



_Yin_ ( _x_ ) = _Winx,_
_Yl_ ( _x_ ) = _Fl_ ( _Wl, Yl−_ 1( _x_ )) _,_ _l ∈_ [ _L_ ] _,_ (1)
_Yout_ ( _x_ ) = _WoutYL_ ( _x_ ) _,_







2


**Effcient Low Rank Adaptation**



of analyzing statistical properties of key quantities in the
model (e.g. pre-activations) as _n_ grows and then adjust the
initialization, the learning rate, and the architecture itself
to achieve desirable properties in the limit _n →∞_ (Hayou
et al., 2019; Schoenholz et al., 2017b; Yang, 2019; Yang
and Littwin, 2023). This approach is used in this paper to
study feature learning dynamics with LoRA in the infinitewidth limit. This will allow us to derive scaling rules for the
learning rates of LoRA modules. For more details about the
theory of scaling of neural networks, see Appendix A.1.


**Notation.** Hereafter, we use the following notation to
describe the asymptotic behaviour as the width _n_ grows.
Given sequences _cn_ _∈_ R and _dn_ _∈_ R [+], we write _cn_ =
_O_ ( _dn_ ), resp. _cn_ = Ω( _dn_ ), to refer to _cn_ _<_ _κdn_, resp.
_cn_ _> κdn_, for some constant _κ >_ 0. We write _cn_ = Θ( _dn_ )
if both _cn_ = _O_ ( _dn_ ) and _cn_ = Ω( _dn_ ) are satisfied. For
vector sequences _cn_ = ( _c_ _[i]_ _n_ [)][1] _[≤][i][≤][k]_ _[∈]_ [R] _[k]_ [(for some] _[ k]_ _[>]_ [ 0][),]
we write _cn_ = _O_ ( _dn_ ) when _c_ _[i]_ _n_ [=] _[O]_ [(] _[d][i]_ _n_ [)] [for] [all] _[i]_ _[∈]_ [[] _[k]_ []][,]
and same holds for other asymptotic notations. Finally,
when the sequence _cn_ is a vector of random variables,
convergence is understood to be convergence in second
moment ( _L_ 2 norm).


**3. An Intuitive Analysis of LoRA**


Our intuition is simple: the matrices _A_ and _B_ have
“transposed” shapes and one would naturally ask whether
the learning rate should be set differently for the two
matrices. In practice, most SOTA models have large width
(embedding dimension). Thus, it makes sense to study the
training dynamics when the width goes to infinity.


**3.1. LoRA with a Toy Model**


Consider the following linear model


_f_ ( _x_ ) = ( _W_ _[∗]_ + _ba_ _[⊤]_ ) _x,_ (2)


where _W_ _[∗]_ _∈_ R [1] _[×][n]_ are the pretrained weights, _b_ _∈_ R _, a_ _∈_
R _[n]_ are LoRA weights, [2] _x_ _∈_ R _[n]_ is the model input.
This setup corresponds to _n_ 1 = 1 _, n_ 2 = _n, r_ = 1 in
Definition 1. We assume that the weights _W_ _[∗]_ are fixed
(from pretraining). The goal is to minimize the loss _L_ ( _θ_ ) =
12 [(] _[f]_ [(] _[x]_ [)] _[−][y]_ [)][2][ where] _[ θ]_ [= (] _[a, b]_ [)][ and][ (] _[x, y]_ [)][ is an input-output]
datapoint. [3] We assume that _x_ = Θ _n_ (1) which means that
input coordinates remain of the same order as we increase
width. In the following, we analyze the behaviour of the
finetuning dynamics as model width _n_ grows.


2Here, we consider _n_ 2 = 1 to simplify the analysis. All the
conclusions remain essentially valid when _n_ 2 = _n_ 1 = _n_ .
3For simplicity, we assume that the finetuning dataset consists
of a single sample. Our analysis is readily generalizable to
multiple samples.



**Initialization.** We consider a Gaussian initialization of
the weights as follows: _ai_ _∼N_ (0 _, σa_ [2][)][,] _[b]_ _[∼N]_ [(0] _[, σ]_ _b_ [2][)][.][4]

With LoRA, we generally want to initialize the product _ba_ _[⊤]_

to be 0 so that finetuning starts from the pretrained model.
This implies at least one of the weights _a_ and _b_ is initialized
to 0. If both are initialized to 0, it is trivial that no learning
occurs in this case since this is a saddle point. Thus, we
should initialize one of the parameters _a_ and _b_ to be nonzero and the other to be zero. If we choose a non-zero
initialization for _a_, then following standard initialization
schemes (e.g., He Init (He et al., 2016), LeCun Init (LeCun
et al., 2002)), one should set _σa_ [2] [=] [Θ(] _[n][−]_ [1][)][ to ensure] _[ a][⊤][x]_
does not explode with width. This is justified by the Central
Limit Theorem (CLT). [5] On the other hand, if we choose
a non-zero initialization for _b_, one should make sure that
_σb_ [2] [= Θ(1)][.] [This leaves us with two possible schemes:]

  - Init[1]: _σb_ [2] [= 0] _[, σ]_ _a_ [2] [= Θ(] _[n][−]_ [1][)][.]


  - Init[2]: _σb_ [2] [= Θ(1)] _[, σ]_ _a_ [2] [= 0][.]


Our analysis will only consider these two initialization
schemes for LoRA modules, although the results should
in-principle hold for other schemes, providing that stability
(as discussed above) is satisfied.


**Learning rate.** WLOG, we can simplify the analysis by
assuming that _W_ _[∗]_ = 0. This can be achieved by setting
_y_ ˜ = _y −_ _W_ _[∗]_ _x_ . The gradients are given by



The update in model output is driven by the three terms
( _δt_ _[i]_ [)] _i∈{_ 1 _,_ 2 _,_ 3 _}_ [.] The first two terms represent “linear”
contributions to the update, i.e. change in model output
driven by fixing _b_ and updating _a_ and vice-versa. These
terms are order one in _η_ . The third term _δt_ [3] [represents] [a]
multiplicative update, compounding the updates in _a_ and _b_,
and is an order two term in _η_ . As _n_ grows, a desirable
property is that ∆ _ft_ = Θ(1). Intuitively, this means


4The Gaussian distribution can be replaced by any other
distribution with finite variance.
5Technically, the CLT only ensures the almost sure
convergence, the _L_ 2 convergence follows from the Dominated
Convergence Theorem. We omit these technical details in this
paper.



_∂L_



_∂a_ [=] _[ b]_ [(] _[f]_ [(] _[x]_ [)] _[ −]_ _[y]_ [)] _[x.]_



_∂L_ _[∂][L]_

_∂b_ [=] _[ a][⊤][x]_ [(] _[f]_ [(] _[x]_ [)] _[ −]_ _[y]_ [)] _[,]_ _∂a_



We use subscript _t_ to denote the finetuning step. Let _Ut_ =
( _ft_ ( _x_ ) _−_ _y_ ). At step _t_ with learning rate _η_ _>_ 0, we have



_def_
∆ _ft_ = _ft_ ( _x_ ) _−_ _ft−_ 1( _x_ ) = _−ηb_ [2] _t−_ 1 _[U][t][−]_ [1] _[∥][x][∥]_ [2]

              - ��              _δt_ [1]

_−_ _η_ ( _a_ _[⊤]_ _t−_ 1 _[x]_ [)][2] _[U][t][−]_ [1] + _η_ [2] _Ut_ [2] _−_ 1 _[b][t][−]_ [1][(] _[a]_ _t_ _[⊤]_ _−_ 1 _[x]_ [)] _[∥][x][∥]_ [2]

  - ��  -  - ��  _δt_ [2] _δt_ [3]



+ _η_ [2] _Ut_ [2] _−_ 1 _[b][t][−]_ [1][(] _[a]_ _t_ _[⊤]_ _−_ 1 _[x]_ [)] _[∥][x][∥]_ [2] _._

 - ��  _δt_ [3]



_._



3


**Effcient Low Rank Adaptation**



that as we scale the width, feature updates do not ‘suffer’
from this scaling (see Appendix A.1 for more details). An
example of a scenario where feature learning is affected
by scaling is the lazy training regime (Jacot et al., 2018),
where feature updates are of order Θ( _n_ _[−]_ [1] _[/]_ [2] ) which implies
that no feature learning occurs in the limit _n_ _→∞_ . The
condition ∆ _ft_ = Θ(1) also implies that the update does
not explode with width, which is also a desirable property.


Having ∆ _ft_ = Θ(1) satisfied implies that at least one of
the three terms ( _δt_ _[i]_ [)] _i∈{_ 1 _,_ 2 _,_ 3 _}_ [is][ Θ(1)][.] [Ideally, we want both]
_δt_ [1] [and] _[ δ]_ _t_ [2] [to be][ Θ(1)][ because otherwise it means that either]
_a_ or _b_ is not efficiently updated. For instance, if _δt_ [1] [=] _[ o]_ [(1)][,]
it means that as _n_ _→∞_, the model acts as if _a_ is fixed
and only _b_ is trained. Similar conclusions hold when _δt_ [2] [=]

_o_ (1). Having both _δt_ [1] [and] _[δ]_ _t_ [2] [being] [Θ(1)] [in] [width] [means]
that both _a_ and _b_ parameter updates significantly contribute
to the change in _ft_ ( _x_ ), and we say that feature learning with
LoRA is _efficient_ when this is the case, i.e. _δi_ _[t]_ [=] [Θ(1)][ for]
_i_ _∈{_ 1 _,_ 2 _}_ and all _t_ _>_ 1. We will formalize this definition
of efficiency in the next section. The reader might wonder
why we do not require that _δt_ [3] [be] [Θ(1)][.] [We] [will] [see] [that]
when both _δt_ [1] [and] _[ δ]_ _t_ [2] [are][ Θ(1)][, the term] _[ δ]_ _t_ [3] [is also][ Θ(1)][.]


**Efficiency** **Analysis.** Let us assume that we train the
model with gradient descent with learning rate _η_ = Θ( _n_ _[c]_ )
for some _c_ _∈_ R, and suppose that we initialize the model
with Init[1]. Sine the training dynamics are mainly
matrix vector products, sum of vectors/scalars etc (see
(Yang et al., 2022)), [6] it is easy to see that any quantity
in the training dynamics should be of order _n_ _[γ]_ for some
_γ_ _∈_ R. For any quantity _v_ in the training dynamics, we
write _v_ = Θ( _n_ _[γ]_ [[] _[v]_ []] ). When _v_ is a vector, we use the same
notation when all entries of _v_ are Θ( _n_ _[γ]_ [[] _[v]_ []] ). The _γ_ notation
is formally defined in Appendix A.


Starting from initialization, we have _f_ 0( _x_ ) = 0. LoRA
finetuning is efficient when _δt_ [1] [=] [Θ(1)][ and] _[ δ]_ _t_ [2] [=] [Θ(1)][ for]
all _t >_ 1, [7] and _ft_ ( _x_ ) = Θ(1) for _t >_ 1. This translate to

 _c_ + 2 _γ_ [ _bt−_ 1] + 1 = 0 ( _δt_ [1] [= Θ(1))]



rate should scale as _η_ = Θ( _n_ _[−]_ [1] _[/]_ [2] ) in order to achieve
efficient feature learning. At initialization, _b_ 0 = 0 and
_a_ _[⊤]_ 0 _[x]_ [=] [Θ(1)] [(by] [Central] [Limit] [Theorem).] Through
an inductive argument, for _t_ _>_ 0, _bt_ will be of order
Θ( _n_ _[−]_ [1] _[/]_ [2] ) and _a_ _[⊤]_ _t_ _[x]_ [ will be of order][ Θ(1)][, yielding] _[ f][t]_ [(] _[x]_ [) =]
Θ( _n_ _[−]_ [1] _[/]_ [2] ). Indeed, at each iteration the update to _bt_ will be
of order Θ( _ηya_ _[⊤]_ _t−_ 1 _[x]_ [)] [=] [Θ(] _[n][−]_ [1] _[/]_ [2][)] [and] [the] [updates] [to] _[a][t]_
are of order Θ( _ηbt−_ 1 _yx_ ) = Θ( _n_ _[−]_ [1] ). As _ft_ = Θ( _n_ _[−]_ [1] _[/]_ [2] ),
this yields a contradiction towards learning Θ(1) features.


This shows that we cannot have both _δt_ [1] [and] _[ δ]_ _t_ [2] [to be][ Θ(1)]
with this parametrization (also true with Init[2]). We
formalize this result in the next proposition and refer the
reader to Appendix A for further technical details.


**Proposition 1** (Inefficiency of LoRA fine-tuning) **.** _Assume_
_that_ _LoRA_ _weights_ _are_ _initialized_ _with_ _Init[1]_ _or_
_Init[2] and trained with gradient descent with learning_
_rate η_ = Θ( _n_ _[c]_ ) _for some c_ _∈_ R _._ _Then,_ _it is impossible to_
_have δt_ _[i]_ [= Θ(1)] _[ for][ i][ ∈{]_ [1] _[,]_ [ 2] _[}][ for any][ t >]_ [ 0] _[, and therefore,]_
_fine-tuning with LoRA in this setup is inefficient._



_ca_ + 2 _γ_ [ _bt−_ 1] + 1 = 0 ( _δt_ [1] [= Θ(1))]
_cb_ + 2 _γ_ [ _a_ _[⊤]_ _t−_ 1 _[x]_ [] = 0] ( _δt_ [2] [= Θ(1))]
_γ_ [ _bt−_ 1] + _γ_ [ _a_ _[⊤]_ _t−_ 1 _[x]_ [] = 0] ( _ft−_ 1( _x_ ) = Θ(1))



_c_ + 2 _γ_ [ _bt−_ 1] + 1 = 0 ( _δt_ [1] [= Θ(1))]
_c_ + 2 _γ_ [ _a_ _[⊤]_ _t−_ 1 _[x]_ [] = 0] ( _δt_ [2] [= Θ(1))]
_γ_ [ _bt−_ 1] + _γ_ [ _a_ _[⊤]_ _t−_ 1 _[x]_ [] = 0] ( _ft−_ 1( _x_ ) = Θ(1))



In conclusion, efficiency cannot be achieved with this
parametrization of the learning rate. This suggests
that standard LoRA finetuning as currently used by
practitioners is suboptimal, especially when model width
is large, which is a property that is largely satsified
in practice ( _n_ _≈_ 700 for GPT2 and _n_ _≈_ 4000 for
LLama). This analysis suggests that _we are missing crucial_
_hyperparameters_ in the standard LoRA setup. Indeed, we
show that by decoupling the learning rate for _a_ and _b_, we
can have _δt_ _[i]_ [=] [Θ(1)] [for] _[i]_ _[∈{]_ [1] _[,]_ [ 2] _[,]_ [ 3] _[}]_ [.] [We] [write] _[η][a][, η][b]_ [to]
denote the learning rates. The analysis conducted above
remains morally the same with the only difference being in
the learning rates. Let _ηa_ = Θ( _n_ _[c][a]_ ) and _ηb_ = Θ( _n_ _[c][b]_ ),
and assume that weights are initialized with Init[1].
A similar analysis to the one conducted above show that
having _ft_ ( _x_ ) = Θ(1) and _δt_ _[i]_ [=] [Θ(1)] [for] _[i]_ _[∈{]_ [1] _[,]_ [ 2] _[}]_ [and]
_t >_ 0 implies that for all _t >_ 1

 _ca_ + 2 _γ_ [ _bt−_ 1] + 1 = 0 ( _δt_ [1] [= Θ(1))]











Solving this equation yields _c_ = _−_ 1 _/_ 2, i.e. the learning


6A crucial assumption for this to hold is also to have that for
any matrix/vector product in the training dynamics, the product
dimension (the dimension along which the matrix/vector product
is calculated) is Θ( _n_ _[α]_ ) for some _α_ _>_ 0. For instance, in the
case of Transformers, this is satisfied since the MLP embedding
dimension is generally _k × n_ . However, this condition would be
violated if for instance one considers MLP embedding dimension
_kn_ log( _n_ ). Such non-standard scaling choices require a particular
treatment, but the conclusions remain the same.
7Here we use the _t_ _>_ 1 instead of _t_ _>_ 0 because at _t_ _≤_ 1, at
least one the terms _δ_ 1 [1] [or] _[ δ]_ 1 [2] [will be zero.]



which, after simple calculations, implies that _ca_ + _cb_ = _−_ 1.
This is only a necessary condition. In the next result, taking
also some elements of stability into consideration, we fully
characterize the choice of _ηa_ and _ηb_ to ensure efficient
LoRA fine-tuning.


**Proposition** **2** (Efficient Fine-Tuning with LoRA) **.** _In_ _the_
_case of model_ (2) _,_ _with ηa_ = Θ( _n_ _[−]_ [1] ) _and ηb_ = Θ(1) _,_ _we_
_have for all t >_ 1 _, i ∈{_ 1 _,_ 2 _,_ 3 _}, δt_ _[i]_ [= Θ(1)] _[.]_


We refer the reader to Appendix A for more details on the
proof of Proposition 2. In conclusion, scaling the learning



4


**Effcient Low Rank Adaptation**



rates as _ηa_ = Θ( _n_ _[−]_ [1] ) and _ηb_ = Θ(1) ensures stability
(∆ _ft_ = Θ(1)) and efficiency of LoRA finetuning ( _δt_ _[i]_ [=]
Θ(1) for _i_ _∈{_ 1 _,_ 2 _}_ and _t_ _>_ 1) in the infinite-width limit.
In practice, this means that the learning rate for _b_ should
be generally much larger than that of _a_ . This remains true
even if _b_ _∈_ R _[r]_ for general _r_ . We will later see that this
scaling is valid for general neural network models.



2.0


1.5


1.0


0.5


0.30


0.25


0.20



1.0e+01

2.2e+00

4.6e-01

1.0e-01

2.2e-02

4.6e-03

1.0e-03

2.2e-04


1.0e+01

2.2e+00

4.6e-01

1.0e-01

2.2e-02

4.6e-03

1.0e-03

2.2e-04


0.22


0.20


0.18









A



2.0


1.5


1.0


0.5


0.24


0.22


0.20


0.18







A


|Col1|> )|Col3|Col4|
|---|---|---|---|
|<br>|<br>|<br>|<br>|
|<br>~~B ~~<br>Test (<br>B ><br>Train (<br>B <br> <br>|~~A~~<br><br>A)<br>=<br>A)<br><br><br><br>0.18|~~t~~<br>~~[180, 200]~~||
|<br>~~B ~~<br>Test (<br>B ><br>Train (<br>B <br> <br>|~~A~~<br><br>A)<br>=<br>A)<br><br><br><br>0.18|||
|~~Test (~~<br>B|A~~)~~<br>1<br>0.17||0|
|||80<br>20|80<br>20|
|||||



25 50 75 100 125 150 175 200
t


_Figure 2._ ( **Top** ) Train/Test accuracy of toy model Equation (3)
averaged over 3 random seeds. Orange dashed line represents the
line _ηA_ = _ηB_, and red dots represents all values of ( _ηA, ηB_ ) for
which _d_ min( _ηA, ηB_ ) := _L_ ( _ηA,ηB_ ) _/L_ _[∗]_ _−_ 1 _≤_ 1%, where _L_ _[∗]_ is
the best loss. ( **Bottom** ) Train/Test curves for two sets of learning
rates: the optimal choice ( _ηA_ _[∗]_ _[, η]_ _B_ _[∗]_ [)] [=] [(2] _[.]_ [78] _[,]_ [ 1] _[.]_ [29e] _[−]_ [4)][ overall at]
_t_ = 200 in terms of test loss (Blue) and the optimal choice when
_ηA_ = _ηB_ which is given by ( _ηA, ηB_ ) = (2 _._ 15e _−_ 2 _,_ 2 _._ 15e _−_ 2)
(Orange). All values are averaged oevr three runs and confidence
interval are shown (shaded).


**3.2. Verifying the Results on a Toy Model**


The previous analysis considers a simple linear model.
To assess the validity of the scaling rules in a non-linear
setting, we consider a neural network model given by


_f_ ( _x_ ) = _Woutϕ_ ( _BAϕ_ ( _Winx_ )) _,_ (3)

where _Win_ _∈_ R _[n][×][d]_ _, Wout_ _∈_ R [1] _[×][n]_ _, A_ _∈_ R _[r][×][n]_ _, B_ _∈_
R _[n][×][r]_ are the weights, and _ϕ_ is the ReLU function. The
model is trained on a synthetic dataset generated with _X_ _∼_
_N_ (0 _, Id_ ) _,_ _Y_ = sin( _d_ _[−]_ [1][ �] _[d]_ _i_ =1 _[X][i]_ [)][.] [See] [Appendix] [C] [for]
more details.



Only the weight matrices _A, B_ are trained ( _Win, Wout_ are
fixed). We use _d_ = 5 _, n_ = 100 _, r_ = 4, train data size
1000 and a test data size 100. [8] The train/test loss for
varying _ηA_ and _ηB_ is reported in Figure 2 at the early
stages of the training ( _t_ = 10) and after convergence
(we observed convergence around _t_ _≈_ 200 for reasonable
choices of learning rates). The red ’+’ signs represents
learning rates ( _ηA, ηB_ ) for which the loss is within 1%
range from the best loss and dashed line represents the case
where the learning rates are set equal. We observe that
both the best train and test losses are consistently achieved
by a combination of learning rates where _ηb_ _≫_ _ηa_, which
validates our analysis in the previous section. Notice also
that optimal learning rates ( _ηA, ηB_ ) are generally close to
the edge of stability, a well-known behaviour in training
dynamics of deep networks (Cohen et al., 2021).


**4. Stability and Feature Learning with LoRA**
**in the Infinite Width Limit**


In this section, we extend the analysis above to general
neural architectures with LoRA layers. We show that the
conclusions from the analysis on the linear model hold for
general neural architectures: 1) using the same learning
rate for both _A_ and _B_ leads to suboptimal feature learning
when model width is large, and 2) this problem can be fixed
by setting different learning rates for _A_ and _B_ .


Since our aim in this paper is primarily methodological, the
theoretical results in this section are of a physics level of
rigor, omitting technical assumptions that would otherwise
make the analysis rigorous but unnecessarily complicated.
In all the results, LoRA rank _r_ is considered fixed and
finetuning dynamics are analyzed in the limit of infinitewidth. This setup fairly represents practical scenarios
where _r_ _≪_ _n_ and _r_ is generally small.


**Notation.** The LoRA weights are initialized with _Aij_ _∼_
_N_ (0 _, σA_ [2] [)] _[, B][ij]_ _[∼N]_ [(0] _[, σ]_ _B_ [2] [)] [for] [some] _[σ][A][, σ][B]_ _[≥]_ [0][.][9] [Here]
also, we assume that either _σB_ [2] [=] [0] [and] _[σ]_ _A_ [2] [=] [Θ(] _[n][−]_ [1][)]
(Init[1]), or _σB_ [2] [=] [Θ(1)] [and] _[σ]_ _A_ [2] [=] [0] [(][Init[2]][).]
Given a LoRA layer in the model, Z denotes the input
to that layer and _Z_ [¯] the output after adding the pretrained
weights. More precisely, we write _Z_ [¯] = _W_ _[∗]_ Z + _[α]_ _r_ _[BA]_ [ Z][.]


Our main analysis relies on a careful estimation of the
magnitude of several quantities including _LoRA_ _features_ .
Let us first give a formal definition.


**Definition** **2** (LoRA Features) **.** _Given_ _a_ _general_ _neural_
_architecture_ _and_ _a_ _LoRA_ _layer_ _(Definition_ _1),_ _we_ _define_
_LoRA features_ ( _ZA, ZB_ ) _as ZA_ = _AZ and ZB_ = _BZA_ =


8See Appendix C for more details about the experimental
setup.
9In (Hu et al., 2021), _B_ is initialized to 0, which corresponds
to setting _σB_ = 0.



5


**Effcient Low Rank Adaptation**



_BAZ ._ _At_ _fine-tuning_ _step_ _t,_ _we_ _use_ _the_ _superscript_ _t_
_to_ _denote_ _the_ _value_ _of_ _LoRA_ _features_ _ZA_ _[t]_ _[, Z]_ _B_ _[t]_ _[,]_ _[and]_ _[the]_
_subscript t to denote the weights At, Bt._


LoRA layers are 2-layers linear networks with a
“bottleneck” in the middle (since generally _r_ _≪_ _n_ ). This
bottleneck shape might induce some numerical challenges
in training stability and efficiency (Definition 3 and
Definition 5).


**Finetuning Dataset.** To simplify the analysis, we assume
that the finetuning dataset comprises a single sample
( _x, y_ ), [10] and the goal is to minimize the loss _L_ ( _**θ**_ _,_ ( _x, y_ ))
computed with the underlying model where the adjusted
weights are given by _W_ _[∗]_ + _BA_ for all LoRA layers
(here _**θ**_ = _{A, B,_ for all LoRA layers in the model _}_ ). At
training step _t_, and for any LoRA layer in the model, Z _[t]_

is the input to the LoRA layer, computed with data input
_x_ . Similarly, we write _dZ_ [¯] _[t]_ to denote the gradient of the
loss function with respect to the layer output features _Z_ [¯]
evaluated at data point ( _x, y_ ).


The notion of stability of LoRA as discussed in Section 3
can be generalized to any neural network model as follows.


**Definition** **3** (Stability) **.** _We_ _say_ _that_ _LoRA_ _finetuning_ _is_
_stable if for all LoRA layers in the model, and all training_
_steps t, we have Z, ZA, ZB_ = _O_ (1) _as n goes to infinity._


Stability implies that no quantity in the network explodes
as width grows, a desirable property as we scale the
model. [11] Naturally, in order to ensure stability, one has
to scale hyperparameters (initialization, learning rate) as
_n_ grows. Scaling rules for initialization are fairly easy to
infer and were already discussed in Section 3 where we
obtained two plausible initialization schemes (Init[1]
and Init[2]). More importantly, if we arbitrarily scale
the learning rate with width, we might end up with
suboptimal learning as width grows even if the finetuning is
stable. This is the case for instance when we aggressively
downscale the learning rate with width, or inadequately
parameterize the network (e.g. Neural Tangent Kernel
parametrization which leads to the kernel regime in the
infinite width limit, (Jacot et al., 2018)). To take this into
account, we define a notion of feature learning with LoRA.


**Definition 4** (Stable Feature Learning with LoRA) **.** _We say_


10This assumption on the finetuning dataset is for simplification
purposes only. All our analysis can be re-written with ‘batched’
gradients and the conclusions remain the same. However, some
additonal assumptions are required to make the analysis rigorous.
11It is possible to define stability as Z _, ZB_ = _O_ (1) and exclude
_ZA_ from the condition. This would allow scenarios where for
instance the entries of _A_ explode with width but their magnitude
is compensated with a smaller magnitude of _B_ . This system has
one degree of freedom because of the homogeneity of the product
_BA_, and by imposing that _ZA_ = _O_ (1), we avoid having such
scenarios.



where _u ⊗_ _v_ denotes the outer product _uv_ _[⊤]_ of vectors _u_, _v_,
and the weights are updated as follows


_At_ = _At−_ 1 _−_ _ηAgA_ _[t][−]_ [1] _,_ _Bt_ = _Bt−_ 1 _−_ _ηBgB_ _[t][−]_ [1] _,_


where _gA, gB_ are processed gradients (e.g. normalized
gradients with momentum as in AdamW etc). Hereafter,
we assume that the gradients are processed in a way that
makes their entries Θ(1). This is generally satisfied in
practice (with Adam for instance) and has been considered
in (Yang and Littwin, 2023) to derive the _µ_ -parametrization
for general gradient processing functions.


Unlike the linear model in Section 3, LoRA feature updates
are not only driven by the change in the _A, B_ weights, but
also Z _, dZ_ [¯] which are updated as we finetune the model
(assuming there are multiple LoRA layers). To isolate the
contribution of individual LoRA layers to feature learning,


12When taking the infinite width limit, we assume that
pretraining parameterization is _µ_ P. This is just a technicality for
the infinite-width limit and does not have any implications on
practical scenarios where the width is finite. The most important
implications of this assumption is that in the pretrained network
(before introducing LoRA layers), we have Z = Θ(1) _,_ _Z_ [¯] =
Θ(1), which holds for a general input-output pair ( _x, y_ ).



_that LoRA finetuning induces stable feature learning if it is_
_stable (Definition 3), and for all LoRA layers and finetuning_

_def_
_step t, we have_ ∆ _ZB_ _[t]_ = _ZB_ _[t]_ [+1] _−_ _ZB_ _[t]_ [= Θ(1)] _[.]_


A similar definition of feature learning was introduced in
(Yang and Littwin, 2023) for pretraining. This definition
ensures that the network is not ‘stuck’ in a kernel regime
where feature updates are of order _O_ ( _n_ _[−][ϵ]_ ) in the infinitewidth limit for some _ϵ_ _>_ 0, which implies that no feature
learning occurs in the limit. The authors introduced the
_µ_ -parameterization (or maximal update parametrization), a
specific network parameterization (initialization + learning
rate scaling), that ensures that feature updates are Θ(1).
Note that here we added stability in the definition, but in
principle, one could define feature learning with Ω instead
of Θ. The latter covers unstable scenarios (e.g. when
∆ _ZB_ _[t]_ [=] [Θ(] _[n]_ [)] [due] [to] [improper] [scaling] [of] [initialization]
and learning rate), so we omit it here and focus on stable
feature learning. Also, notice that we only consider
finetuning dynamics and not the pretraining dynamics.
However, since our analysis depends on weights _W_ _[∗]_ from
pretraining, we assume that pretraining parameterization
ensures stability and feature learning as width grows (see
Appendix A for more details). [12]


At finetuning step _t_, the gradients are given by



_∂Lt_



_r_ _[d][Z]_ [ ¯] _[t][−]_ [1] _[ ⊗]_ _[A][t][−]_ [1][Z] _[t][−]_ [1]



_∂Lt_

_[α]_
_∂B_ [=] _r_



_∂Lt_



_t−_ 1 _[d][Z]_ [ ¯] _[t][−]_ [1] _[ ⊗]_ [Z] _[t][−]_ [1] _[,]_
_r_ _[B][⊤]_



_∂∂ALt_ [=] _[ dZ]_ _A_ _[t][−]_ [1] _⊗_ Z _[t][−]_ [1] = _[α]_ _r_



6


**Effcient Low Rank Adaptation**



we assume that only a _single LoRA layer is trainable_ and all
other LoRA layers are frozen. [13] . In this setting, considering
the only trainable LoRA layer in the model, the layer input
Z is fixed and does not change with _t_, while _dZ_ [¯] changes
with step _t_ (because _Z_ [¯] _[t]_ = ( _W_ _[∗]_ + _[α]_ _r_ _[B][t][A][t]_ [)][Z)][.] [After step] _[ t]_ [,]

_ZB_ is updated as follows



∆ _ZB_ _[t]_ [=] _[ B][t][−]_ [1][∆] _[Z]_ _A_ _[t]_

    - ��     _δt_ [1]



+ ∆ _BtZA_ _[t][−]_ [1]

 - ��  _δt_ [2]



+ ∆ _Bt_ ∆ _ZA_ _[t]_

 - ��  _δt_ [3]



As discussed in Section 3, the terms _δt_ [1] _[, δ]_ _t_ [2] [represent]
the ‘linear’ feature updates that we obtain if we fix one
weight matrix and only train the other, while _δt_ [3] [represents]
the ‘multiplicative’ feature update which captures the
compounded update due to updating both _A_ and _B_ .


**Analysis** **of** **the** **Role** **of** _A_ **and** _B_ **.** As discussed above,
we want to ensure that _δt_ [1] [=] [Θ(1)] [and] _[δ]_ _t_ [2] [=] [Θ(1)] [which]
means that both weight matrices contribute to the update in
_ZB_ . To further explain why this is a desirable property, let
us analyze how changes in matrices _A_ and _B_ affect LoRA
feature _ZB_ = _BA_ Z.


Let ( _B_ : _,i_ )1 _≤i≤r_ denote the columns of _B_ . We can express
_ZB_ as _ZB_ = [�] _i_ _[r]_ =1 [(] _[A]_ [Z][)] _[i][B]_ [:] _[,i]_ [,] [where] [(] _[A]_ [Z][)] _[i]_ [is] [the] _[i][th]_

coordinate of _A_ Z. This decomposition suggests that the
_direction_ of _ZB_ is a weighted sum of the columns of _B_,
and _A_ modulates the _weights_ . With this, we can also write

   _δt_ [1] [=][ �] _i_ _[r]_ =1 [(∆] _[A][t]_ [Z][)] _[i]_ [(] _[B]_ [:] _[,i]_ [)] _[t][−]_ [1]
_δt_ [2] [=][ �] _i_ _[r]_ =1 [(] _[A][t][−]_ [1][Z][)] _[i]_ [(∆] _[B]_ [:] _[,i]_ [)] _[t][−]_ [1] _[,]_


where ( _B_ : _,i_ ) _t_ refers to the columns of _B_ at time step _t_ .
Having both _δt_ [1] [and] _[ δ]_ _t_ [2] [of order][ Θ(1)][ means that both] _[ A]_ [ and]
_B_ are ‘sufficiently’ updated to induce a change in weights
( _A_ Z) _i_ and directions _B_ : _,i_ . If one of the matrices _A, B_ is
not efficiently updated, we might end up with suboptimal
finetuning, leading to either non updated directions _B_
or direction weights ( _At−_ 1 _Z_ ). For instance, assuming
that the model is initialized with Init[2], and that _B_
is not efficiently updated, the direction of _ZB_ will be
mostly determined by the vector (sub)space of dimension
_r_ generated by the columns of _B_ at initialization. This
analysis leads to the following definition of efficient
learning with LoRA.

**Definition** **5** (Efficient Learning) **.** _We_ _say_ _that_ _LoRA_ _fine-_
_tuning_ _is_ _efficient_ _if_ _it_ _is_ _stable_ _(Definition_ _3),_ _and_ _for_ _all_
_LoRA layers in the model, all steps t_ _>_ 1 _, and i{_ 1 _,_ 2 _}, we_
_have δt_ _[i]_ [= Θ(1)] _[.]_


Note that it is possible to achieve stable feature learning
(Definition 4) without necessarily having efficient learning.


13This is equivalent to having only a single LoRA layer in the
model since LoRA layers are initialized to zero. In this way, we
can quantify feature learning induced by the LoRA layer as we
finetune the model.



This is the case when for instance _B_ is not updated (fixed
to a non-zero init with Init[2]) and only _A_ is updated,
which corresponds to simply setting _ηB_ = 0. This is a
trivial case, but other non-trivial cases of inefficiency are
common in practice, such as the use of the same learning
rate for _A_ and _B_ which is a standard practice. In the next
theorem, we characterize the optimal scaling of learning
rates _ηA_ and _ηB_, a conclusion similar to that of Section 3.

**Theorem** **1** (Efficient LoRA (Informal)) **.** _Assume_ _that_
_weight_ _matrices_ _A_ _and_ _B_ _are_ _trained_ _with_ _Adam_ _with_
_respective learning rates ηA and ηB._ _Then, it is impossible_
_to_ _achieve_ _efficiency_ _with_ _ηA_ = _ηB._ _However,_ _LoRA_
_Finetuning is efficient with ηA_ = Θ( _n_ _[−]_ [1] ) _and ηB_ = Θ(1) _._


The result of Theorem 1 suggests that efficiency can only
be achieved with _ηB/ηA_ = Θ( _n_ ). In practice, this
translates to setting _ηB_ _≫_ _ηA_, but does not provide a
precise ratio _ηB/ηA_ to be fixed while tuning the learning
rate (the constant in ‘Θ’ is generally intractable), unless
we tune both _ηB_ and _ηA_ which is not efficient from
a computational perspective as it becomes a 2D tuning
problem. It is therefore natural to set a fixed ratio _ηB/ηA_
and tune only _ηA_ (or _ηB_ ), which would effectively reduce
the tuning process to a 1D grid search, achieving the same
computational cost of standard LoRA where the learning
rate is the same for _A_ and _B_ . We call this method LoRA+.



In the next section, through extensive empirical
evaluations, we first validate our theoretical result
and show that optimal pairs ( _ηA, ηB_ ) (in terms of test
accuracy) generally satisfy _ηB_ _≫_ _ηA_ . We then investigate
the optimal ratio _λ_ for LoRA+ and suggest a default
ratio that was empirically found to generally improve
performance compared to standard LoRA. Although the
conclusions of Theorem 1 and Proposition 2 are similar,
the proof techniques are different. In Proposition 2, the
linear model is trained with gradient descent, while in
Theorem 1, the training algorithm is Adam-type in the
sense that it normalizes the gradients before updating the
weights. The formal statement of Theorem 1 requires an
additional assumption on the alignment of the processed
gradients _gA_ with LoRA input Z. This technical detail is
introduced and discussed in Appendix A.


**5. Experiments with Language Models**


We report our empirical results using LoRA to finetune a
set of language models on different benchmarks. Details
about the experimental setup and more empirical results
are provided in Appendix C. We also identify a default
value for the ratio _λ_ = _ηB/ηA_ that generally improves





7


**Effcient Low Rank Adaptation**



SST2


A



94

93

92

91

90



QQP


A



89


88


87


86



4.0e-03

2.0e-03

1.0e-03

5.0e-04

2.0e-04

1.0e-04



MNLI


A



86


84


82


80



QNLI


A



92


90


88


86



_Figure 3._ Test accuracy of Roberta-base finetuning for 3 epochs on MNLI, QQP, QNLI, and 10 epochs on SST2, with sequence length
_T_ = 128 and half precision (FP16). LoRA hyperparameters are set to _α_ = _r_ = 8. All values are averaged over 3 random seeds
(we do not show confidence intervals for better visualizations, but fluctuations are of order 0 _._ 1%, see Figure 7 for instance). For better
visualization, when accuracy is lower than a fixed threshold, we set it to threshold. Values shown in red are: 1) the best accuracy (overall)
and 2) the accuracy for a set of learning rates where _ηB_ and _ηA_ are close in order of magnitude ( _ηB/ηA_ _∈_ [1 _,_ 1 _._ 25]).



performance as compared to standard LoRA. The code
for our experiments is available at [https://github.](https://github.com/nikhil-ghosh-berkeley/loraplus)
[com/nikhil-ghosh-berkeley/loraplus.](https://github.com/nikhil-ghosh-berkeley/loraplus)


**5.1. GLUE tasks with GPT-2 and RoBERTa**


The GLUE benchmark (General Language Understanding
Evaluation) consists of several language tasks that evaluate
the understanding capabilities of langugage models (Wang
et al., 2018). Using LoRA, we finetune Roberta-base from
the RoBERTa family (Liu et al., 2019) and GPT-2 (Radford
et al., 2019) on MNLI, QQP, SST2, and QNLI tasks (Other
tasks are smaller and generally require an already finetuned
model e.g. on MNLI as starting checkpoint) with varying
learning rates ( _ηA, ηB_ ) to identify the optimal combination.
Empirical details are provided in Appendix C.


**Roberta-base.** Figure 3 shows the results of Robertabase finetuning with _α_ = _r_ = 8, trained with half precision
(FP16). We observe that test accuracy is consistently
maximal for some set of learning rates satisfying _ηB_ _≫_
_ηA_, outperforming the standard practice where _ηA_ and _ηB_
are usually set equal. Interestingly, the gap between the
optimal choice of learning rates overall and the optimal
choice when _ηA_ _≈_ _ηB_ is more pronounced for ‘harder’
tasks like MNLI and QQP, as compared to SST2 and QNLI.
This is probably due to the fact that harder tasks require
more efficient feature learning. It is also worth mentioning
that in our experiments, given limited computational
resources, we use sequence length _T_ = 128 and finetune
for only 3 epochs for MNLI and QQP, so it is expected that
we obtain test accuracies lower that those reported in (Hu
et al., 2021) where the authores finetune Roberta-base with
_T_ = 512 sequence length (for MNLI) and more epochs (30
for MNLI). In Appendix C, we provide additional results
with Test/Train accuracy/loss.



**GPT-2.** Figure 4 shows the results of finetuning GPT2 with LoRA on MNLI and QQP (other tasks and full
precision training are provided in Appendix C). Similar
to the conclusions from Roberta-base, we observe that
maximal test accuracies are achieved with some ( _ηA, ηB_ )
satisfying _ηB_ _≫_ _ηA_ . Further GPT-2 results with different
tasks are provided in Appendix C. Here also, we observed
that the harder the task, the larger the gap between model
performance when _ηB_ _≫_ _ηA_ and when _ηA_ _≈_ _ηB_ .



_Figure 4._ Test accuracy of GPT-2 after finetuning for 3 epochs on
MNLI, QQP, with FP16 precision. LoRA hyperparameters are
set to _α_ = _r_ = 8. Both train/test accuracy are consistently
maximal for some choice of learning rates where _ηB_ _≫_ _ηA_ . See
Appendix C for more numerical results with GPT2.


**5.2. Llama**


To further validate our theoretical findings, we finetune
the Llama-7b model (Touvron et al., 2023) on the MNLI
dataset and flan-v2 dataset (Longpre et al., 2023) using
LoRA. Each trial is averaged over two seeds.


**Flan-v2.** We examine LoRA training of Llama on the
instruction finetuning dataset flan-v2 (Longpre et al.,
2023). To make the experiments computationally feasible,
we train for one epoch on a size 100 _,_ 000 subset of the
flan-v2 dataset. We record the test accuracy of the best
checkpoint every 500 steps. The LoRA hyperparameters



4.0e-03

2.0e-03

1.0e-03

5.0e-04

2.0e-04

1.0e-04



MNLI


A



80


78



QQP


A



88

87

86

85

84



8


**Effcient Low Rank Adaptation**



|Col1|GPT2|Col3|Col4|
|---|---|---|---|
||~~Roberta~~|||
|||||
|||||
|||||
|||||


MNLI QQP SST2 QNLI



are set to _α_ = 16 and _r_ = 64. The adapters are added to
every linear layer (excluding embedding layers) and we use
a constant learning rate schedule. The full training details
are in Appendix C.



10


8


6


4


2



4.0e-04

2.0e-04

1.0e-04

5.0e-05

1.0e-05

5.0e-06

1.0e-06





2.0e-03

1.0e-03

5.0e-04

4.0e-04

2.0e-04

1.0e-04

5.0e-05

1.0e-05







90.0


89.5


89.0


88.5


88.0


87.5


87.0


86.5


86.0





44


42


40


38


36

















A



A



_Figure 5._ Left: MMLU accuracy of Llama-7b trained for one
epoch on a 100k subset of flan-v2. Right: Test accuracy of the best
checkpoint of Llama-7b trained on MNLI for one epoch. Values
are averaged over two seeds.


We evaluate the final model on the MMLU benchmark
(Hendrycks et al., 2020). The results in Figure 5 show that
for this benchmark taking _ηB_ _≫_ _ηA_ is advantageous and
results in a roughly 1.3% gain compared with the optimal
_ηB_ = _ηA_ . In Appendix C we show that the same effect
holds also when using Init[1].


**MNLI.** The right panel of Fig 5 shows the results of
finetuning Llama-7b with LoRA on MNLI, with _α_ = 16,
_r_ = 8. We train using half precision and constant learning
rate schedule, with a sequence length _T_ = 128. Since
MNLI is relatively easy for Llama, we finetune for only
one epoch, which is sufficient for the model to reach its
peak test accuracy. In Figure 5, _ηB_ = _ηA_ is nearly optimal
for all _ηB_ _≥_ _ηA_ . This is consistent with the intuition
that efficient feature learning is not required for easy
tasks and that having _ηB/ηA_ _≫_ 1 does not significantly
enhance performance. Additionally, the magnitude of
stable learning rates for Llama is much smaller than for
GPT-2 and RoBERTa on MNLI further supporting that
Llama requires less adaptation. Analogous plots for the
train and test loss are shown in Fig 19 in Appendix C.


**5.3. How to set LoRA+ Ratio?**


Naturally, the optimal ratio _λ_ depends on the architecture
and the finetuning task via the constants in ‘Θ’
(Theorem 1). This is a limitation of these asymptotic
results since they do not offer any insights on how
the constants are affected by the task and the neural
architecture. Figure 6 show the distribution of the ratio
_ηB/ηA_ for the top 4 runs in terms of test accuracy
for different pairs of (model, task). This is the same
experimental setup of Figure 3 and Figure 4. The optimal
ratio is model and task sensitive and shows significant



_Figure 6._ Distribution of the ratio _ηB/ηA_ for the top 4 learning
rate for each pair (model, task). The 4 learning rates are selected
using the test loss at the end of finetuning (i.e. top 4 learning
rates ( _ηB, ηA_ ) in terms of test loss). The distribution shows the
interquartile range ( 25% _−_ 75% quantiles) and the median.


variance. Our additional experiments in Appendix C
show that it is also sensitive to initialization (Init[1]
vs Init[2]). With Init[2], we found that generally
setting a ratio of _λ_ = _ηB/ηA_ _≈_ 2 [4] improves performance
for Roberta (Figure 7). However, with Init[1], we
found that the optimal ratio is smaller and is of order 2 [2] -2 [3]

(see Appendix C). For LLama experiments, it seems that a
ratio of order 2 [1] -2 [2] is optimal..



0.850

0.825

0.800

0.775

0.750





|Col1|Col2|Col3|Col4|Col5|Col6|
|---|---|---|---|---|---|
||2|X Sp|eed|Up|Up|
|||||||
||<br><br>|||~~4~~<br>|~~4~~<br>|
||<br><br>||<br>|<br>|<br>|
||~~Optimal (~~<br>A~~,~~<br><br>Optimal (<br>A,<br>|B~~) wit~~<br>B) with|<br>B <br> <br>B =|~~ 2~~<br>A<br><br>A|~~ 2~~<br>A<br><br>A|
|0<br>5000 10<br> t accuracy o<br>  etups: (**LoR**<br> ned using a g<br>** sion and**|000 15000 20000 25000 30000 35000<br>Step<br>f Roberta-base fnetuned on the <br>**A+**)_ ηB_ = 24_ηA_ and (**Standard**) <br>  rid search.<br>**  Limitations**|000 15000 20000 25000 30000 35000<br>Step<br>f Roberta-base fnetuned on the <br>**A+**)_ ηB_ = 24_ηA_ and (**Standard**) <br>  rid search.<br>**  Limitations**|000 15000 20000 25000 30000 35000<br>Step<br>f Roberta-base fnetuned on the <br>**A+**)_ ηB_ = 24_ηA_ and (**Standard**) <br>  rid search.<br>**  Limitations**|000 15000 20000 25000 30000 35000<br>Step<br>f Roberta-base fnetuned on the <br>**A+**)_ ηB_ = 24_ηA_ and (**Standard**) <br>  rid search.<br>**  Limitations**|000 15000 20000 25000 30000 35000<br>Step<br>f Roberta-base fnetuned on the <br>**A+**)_ ηB_ = 24_ηA_ and (**Standard**) <br>  rid search.<br>**  Limitations**|


Employing a scaling argument, we showed that LoRA
finetuning as it is currently used in practice is not efficient.
We proposed a method, LoRA+, that resolves this issue by
setting different learning rates for LoRA adapter matrices.
Our analysis is supported by extensive empirical results
confirming the benefits of LoRA+ for both training speed
and performance. These benefits are more significant for
‘hard’ tasks such as MNLI for Roberta/GPT2 (compared to
SST2 for instance) and MMLU for LLama-7b (compared
to MNLI for instance). However, as we depicted in
Figure 7, a more refined estimation of the optimal ratio
_ηB/ηA_ should take into account task and model dependent,
and our analysis in this paper lacks this dimension. We
leave this for future work.



9


**Effcient Low Rank Adaptation**



**Acknowledgement**


We thank Amazon Web Services (AWS) for cloud credits
under an Amazon Research Award. We also gratefully
acknowledge partial support from NSF grants DMS2209975, 2015341, NSF grant 2023505 on Collaborative
Research: Foundations of Data Science Institute (FODSI),
the NSF and the Simons Foundation for the Collaboration
on the Theoretical Foundations of Deep Learning through
awards DMS-2031883 and 814639, and NSF grant
MC2378 to the Institute for Artificial CyberThreat
Intelligence and OperatioN (ACTION).


**Impact Statement**


This paper presents work whose goal is to advance the
field of Machine Learning, specifically, to speed up the
leading algorithm LoRA for fine-tuning pre-trained large
language models while improving performance of the finetuned models. The speed-up saves computation resources
when pre-trained large language models are customized for
particular down-stream tasks. There are many potential
societal consequences of our work, none which we feel
must be specifically highlighted here.


**References**


Blake Bordelon, Lorenzo Noci, Mufan Bill Li, Boris
Hanin, and Cengiz Pehlevan. Depthwise hyperparameter
transfer in residual networks: Dynamics and scaling
limit, 2023.


Jeremy Cohen, Simran Kaur, Yuanzhi Li, J Zico Kolter,
and Ameet Talwalkar. Gradient descent on neural
networks typically occurs at the edge of stability. In
_International_ _Conference_ _on_ _Learning_ _Representations_,
2021. URL [https://openreview.net/forum?](https://openreview.net/forum?id=jh-rTtvkGeM)
[id=jh-rTtvkGeM.](https://openreview.net/forum?id=jh-rTtvkGeM)


Tim Dettmers, Artidoro Pagnoni, Ari Holtzman, and Luke
Zettlemoyer. Qlora: Efficient finetuning of quantized
llms. _arXiv preprint arXiv:2305.14314_, 2023.


Soufiane Hayou. On the infinite-depth limit of finite-width
neural networks. _Transactions_ _on_ _Machine_ _Learning_
_Research_, 2023. ISSN 2835-8856. URL [https://](https://openreview.net/forum?id=RbLsYz1Az9)
[openreview.net/forum?id=RbLsYz1Az9.](https://openreview.net/forum?id=RbLsYz1Az9)


Soufiane Hayou, Arnaud Doucet, and Judith Rousseau.
On the impact of the activation function on deep
neural networks training. In Kamalika Chaudhuri
and Ruslan Salakhutdinov, editors, _Proceedings_ _of_ _the_
_36th_ _International_ _Conference_ _on_ _Machine_ _Learning_,
volume 97 of _Proceedings_ _of_ _Machine_ _Learning_
_Research_, pages 2672–2680. PMLR, 09–15 Jun 2019.



URL [https://proceedings.mlr.press/](https://proceedings.mlr.press/v97/hayou19a.html)
[v97/hayou19a.html.](https://proceedings.mlr.press/v97/hayou19a.html)


Soufiane Hayou, Eugenio Clerico, Bobby He, George
Deligiannidis, Arnaud Doucet, and Judith Rousseau.
Stable resnet. In Arindam Banerjee and Kenji Fukumizu,
editors, _Proceedings_ _of_ _The_ _24th_ _International_
_Conference_ _on_ _Artificial_ _Intelligence_ _and_ _Statistics_,
volume 130 of _Proceedings_ _of_ _Machine_ _Learning_
_Research_, pages 1324–1332. PMLR, 13–15 Apr 2021.
URL [https://proceedings.mlr.press/](https://proceedings.mlr.press/v130/hayou21a.html)
[v130/hayou21a.html.](https://proceedings.mlr.press/v130/hayou21a.html)


Bobby He, James Martens, Guodong Zhang, Aleksandar
Botev, Andrew Brock, Samuel L Smith, and Yee Whye
Teh. Deep transformers without shortcuts: Modifying
self-attention for faithful signal propagation, 2023.


Kaiming He, Xiangyu Zhang, Shaoqing Ren, and Jian
Sun. Deep residual learning for image recognition. In
_Proceedings of the IEEE conference on computer vision_
_and pattern recognition_, pages 770–778, 2016.


Dan Hendrycks, Collin Burns, Steven Basart, Andy Zou,
Mantas Mazeika, Dawn Song, and Jacob Steinhardt.
Measuring massive multitask language understanding.
_arXiv preprint arXiv:2009.03300_, 2020.


Jordan Hoffmann, Sebastian Borgeaud, Arthur Mensch,
Elena Buchatskaya, Trevor Cai, Eliza Rutherford, Diego
de Las Casas, Lisa Anne Hendricks, Johannes Welbl,
Aidan Clark, Tom Hennigan, Eric Noland, Katie
Millican, George van den Driessche, Bogdan Damoc,
Aurelia Guy, Simon Osindero, Karen Simonyan, Erich
Elsen, Jack W. Rae, Oriol Vinyals, and Laurent Sifre.
Training compute-optimal large language models, 2022.


Neil Houlsby, Andrei Giurgiu, Stanislaw Jastrzebski,
Bruna Morrone, Quentin De Laroussilhe, Andrea
Gesmundo, Mona Attariyan, and Sylvain Gelly.
Parameter-efficient transfer learning for nlp. In
_International_ _Conference_ _on_ _Machine_ _Learning_, pages
2790–2799. PMLR, 2019.


Edward J. Hu, Yelong Shen, Phillip Wallis, Zeyuan AllenZhu, Yuanzhi Li, Shean Wang, Lu Wang, and Weizhu
Chen. Lora: Low-rank adaptation of large language
models. _arXiv preprint arXiv:2106.09685_, 2021.


Arthur Jacot, Franck Gabriel, and Clément Hongler.
Neural tangent kernel: Convergence and generalization
in neural networks. _Advances_ _in_ _neural_ _information_
_processing systems_, 31, 2018.


Diederik P Kingma and Jimmy Ba. Adam: A
method for stochastic optimization. _arXiv_ _preprint_
_arXiv:1412.6980_, 2014.



10


**Effcient Low Rank Adaptation**



Dawid Jan Kopiczko, Tijmen Blankevoort, and
Yuki Markus Asano. Vera: Vector-based random
matrix adaptation. _arXiv_ _preprint_ _arXiv:2310.11454_,
2023.


Yann LeCun, Léon Bottou, Genevieve B Orr, and KlausRobert Müller. Efficient backprop. In _Neural networks:_
_Tricks of the trade_, pages 9–50. Springer, 2002.


Brian Lester, Rami Al-Rfou, and Noah Constant. The
power of scale for parameter-efficient prompt tuning.
_arXiv preprint arXiv:2104.08691_, 2021.


Yixiao Li, Yifan Yu, Chen Liang, Pengcheng He, Nikos
Karampatziakis, Weizhu Chen, and Tuo Zhao. Loftq:
Lora-fine-tuning-aware quantization for large language
models. _arXiv preprint arXiv:2310.08659_, 2023.


Haokun Liu, Derek Tam, Mohammed Muqeeth, Jay Mohta,
Tenghao Huang, Mohit Bansal, and Colin A Raffel.
Few-shot parameter-efficient fine-tuning is better and
cheaper than in-context learning. _Advances_ _in_ _Neural_
_Information Processing Systems_, 35:1950–1965, 2022.


Haotian Liu, Chunyuan Li, Yuheng Li, and Yong Jae Lee.
Improved baselines with visual instruction tuning. _arXiv_
_preprint arXiv:2310.03744_, 2023.


Yinhan Liu, Myle Ott, Naman Goyal, Jingfei Du, Mandar
Joshi, Danqi Chen, Omer Levy, Mike Lewis, Luke
Zettlemoyer, and Veselin Stoyanov. Roberta: A robustly
optimized bert pretraining approach, 2019.


Shayne Longpre, Le Hou, Tu Vu, Albert Webson,
Hyung Won Chung, Yi Tay, Denny Zhou, Quoc V Le,
Barret Zoph, Jason Wei, et al. The flan collection:
Designing data and methods for effective instruction
tuning. _arXiv preprint arXiv:2301.13688_, 2023.


Lorenzo Noci, Chuning Li, Mufan Bill Li, Bobby He,
Thomas Hofmann, Chris Maddison, and Daniel M. Roy.
The shaped transformer: Attention models in the infinite
depth-and-width limit, 2023.


OpenAI. Gpt-4 technical report. _arXiv_ _preprint_
_arXiv:2303.08774_, 2023.


Alec Radford, Jeffrey Wu, Rewon Child, David Luan,
Dario Amodei, Ilya Sutskever, et al. Language models
are unsupervised multitask learners. _OpenAI blog_, 1(8):
9, 2019.


Samuel S. Schoenholz, Justin Gilmer, Surya Ganguli, and
Jascha Sohl-Dickstein. Deep information propagation,
2017a.


S.S. Schoenholz, J. Gilmer, S. Ganguli, and J. SohlDickstein. Deep information propagation. In



_International_ _Conference_ _on_ _Learning_ _Representations_,
2017b.


Hugo Touvron, Louis Martin, Kevin Stone, Peter Albert,
Amjad Almahairi, Yasmine Babaei, Nikolay Bashlykov,
Soumya Batra, Prajjwal Bhargava, Shruti Bhosale, Dan
Bikel, Lukas Blecher, Cristian Canton Ferrer, Moya
Chen, Guillem Cucurull, David Esiobu, Jude Fernandes,
Jeremy Fu, Wenyin Fu, Brian Fuller, Cynthia Gao,
Vedanuj Goswami, Naman Goyal, Anthony Hartshorn,
Saghar Hosseini, Rui Hou, Hakan Inan, Marcin Kardas,
Viktor Kerkez, Madian Khabsa, Isabel Kloumann,
Artem Korenev, Punit Singh Koura, Marie-Anne
Lachaux, Thibaut Lavril, Jenya Lee, Diana Liskovich,
Yinghai Lu, Yuning Mao, Xavier Martinet, Todor
Mihaylov, Pushkar Mishra, Igor Molybog, Yixin Nie,
Andrew Poulton, Jeremy Reizenstein, Rashi Rungta,
Kalyan Saladi, Alan Schelten, Ruan Silva, Eric Michael
Smith, Ranjan Subramanian, Xiaoqing Ellen Tan,
Binh Tang, Ross Taylor, Adina Williams, Jian Xiang
Kuan, Puxin Xu, Zheng Yan, Iliyan Zarov, Yuchen
Zhang, Angela Fan, Melanie Kambadur, Sharan Narang,
Aurelien Rodriguez, Robert Stojnic, Sergey Edunov, and
Thomas Scialom. Llama 2: Open foundation and finetuned chat models. _arXiv_ _preprint_ _arXiv:2307.09288_,
2023.


Alex Wang, Amanpreet Singh, Julian Michael, Felix Hill,
Omer Levy, and Samuel R. Bowman. Glue: A multi-task
benchmark and analysis platform for natural language
understanding, 2018.


Yizhong Wang, Hamish Ivison, Pradeep Dasigi, Jack
Hessel, Tushar Khot, Khyathi Raghavi Chandu, David
Wadden, Kelsey MacMillan, Noah A Smith, Iz Beltagy,
et al. How far can camels go? exploring the state of
instruction tuning on open resources. _arXiv_ _preprint_
_arXiv:2306.04751_, 2023.


G. Yang. Scaling limits of wide neural networks with
weight sharing: Gaussian process behavior, gradient
independence, and neural tangent kernel derivation.
_arXiv preprint arXiv:1902.04760_, 2019.


Greg Yang and Edward J Hu. Tensor programs iv:
Feature learning in infinite-width neural networks. In
_International_ _Conference_ _on_ _Machine_ _Learning_, pages
11727–11737. PMLR, 2021.


Greg Yang and Etai Littwin. Tensor programs ivb:
Adaptive optimization in the infinite-width limit. _arXiv_
_preprint arXiv:2308.01814_, 2023.


Greg Yang, Edward J Hu, Igor Babuschkin, Szymon
Sidor, Xiaodong Liu, David Farhi, Nick Ryder,
Jakub Pachocki, Weizhu Chen, and Jianfeng Gao.
Tensor programs v: Tuning large neural networks



11


**Effcient Low Rank Adaptation**


via zero-shot hyperparameter transfer. _arXiv_ _preprint_
_arXiv:2203.03466_, 2022.


Greg Yang, Dingli Yu, Chen Zhu, and Soufiane Hayou.
Tensor programs vi: Feature learning in infinite-depth
neural networks. _arXiv_ _preprint_ _arXiv:2310.02244_,
2023.


Liu Yang, Steve Hanneke, and Jaime Carbonell. A theory
of transfer learning with applications to active learning.
_Machine learning_, 90:161–189, 2013.


Yuchen Zeng and Kangwook Lee. The expressive power of
low-rank adaptation. _arXiv_ _preprint_ _arXiv:2310.17513_,
2023.


12


**Effcient Low Rank Adaptation**


**A. Proofs**


In this section, we provide proofs for Proposition 1, Proposition 2, Theorem 1, and some technical details used in the
proofs.


**A.1. Scaling of Neural Networks**


Scaling refers to the process of increasing the size of one of the ingredients in the model to improve performance (see e.g.
(Hoffmann et al., 2022)). This includes model capacity which can be increased via width (embedding dimension) or depth
(number of layers) or both, compute (training data), number of training steps etc. In this paper, we are interested in scaling
model capacity via the width _n_ . This is motivated by the fact that most state-of-the-art language and vision models have
large width.


It is well known that as the width _n_ grows, the network initialization scheme and the learning should be adapted to avoid
numerical instabilities and ensure efficient learning. For instance, the initialization variance should scale 1 _/n_ to prevent
arbitrarily large pre-activations as we increase model width _n_ (e.g. He init (He et al., 2016)). To derive such scaling rules,
a principled approach consist of analyzing statistical properties of key quantities in the model (e.g. pre-activations) as _n_
grows and then adjust the initialization, the learning rate, and the architecture itself to achieve desirable properties in the
limit _n →∞_ (Hayou et al., 2019; Schoenholz et al., 2017b; Yang, 2019).


In this context, (Yang et al., 2022) introduces the Maximal Update Parameterization (or _µ_ P), a set of scaling rules for the
initialization scheme, the learning rate, and the network architecture that ensure stability and maximal feature learning in
the infinite width limit. Stability is defined by _Yl_ _[i]_ [= Θ(1)][ for all] _[ l]_ [ and] _[ i]_ [ where the asymptotic notation ‘][Θ(] _[.]_ [)][’ is with respect]
to width _n_ (see next paragraph for a formal definition), and feature learning is defined by ∆ _Yl_ = Θ(1), where ∆ refers
to the feature update after taking a gradient step. _µ_ P guarantees that these two conditions are satisfied at any training step
_t_ . Roughly speaking, _µ_ P specifies that hidden weights should be initialized with Θ( _n_ _[−]_ [1] _[/]_ [2] ) random weights, and weight
updates should be of order Θ( _n_ _[−]_ [1] ). Input weights should be initialized Θ(1) and the weights update should be Θ(1) as
well. While the output weights should be initialized Θ( _n_ _[−]_ [1] ) and updated with Θ( _n_ _[−]_ [1] ). These rules ensure both stability
and feature learning in the infinite-width limit, in contrast to standard parameterization (exploding features if the learning
rate is well tuned), and kernel parameterizations (e.g. Neural Tangent Kernel parameterization where ∆ _Yl_ = Θ( _n_ _[−]_ [1] _[/]_ [2] ),
i.e. no feature learning in the limit).


**A.2. The Gamma Function (** _γ_ [ _._ ] **)**


In the theory of scaling of neural networks, one usually tracks the asymptotic behaviour of key quantities as we scale some
model ingredient. For instance, if we scale the width, we are interested in quantifying how certain quantities in the network
behave as width _n_ grows large and the asymptotic notation becomes natural in this case. This is a standard approach for
(principled) model scaling and it has so far been used to derive scaling rules for initialization (Schoenholz et al., 2017b),
activation function (Hayou et al., 2019), network parametrization (Yang et al., 2023), amongst other things.


With Init[1] and Init[2], the weights are initialized with Θ( _n_ _[−][β]_ ) for some _β_ _≥_ 0. Assuming that the learning rates
also scale polynomially with _n_, it is straightforward that preactivations, gradients, and weight updates are all asymptotically
polynomial in _n_ . It is therefore natural to introduce the Gamma function, and we write _v_ = Θ( _γ_ [ _v_ ]) to capture this
polynomial behaviour. Now, let us introduce some elementary operations with the Gamma function.


**Multiplication.** Given two real-valued variables _v, v_ _[′]_, we have _γ_ [ _v × v_ _[′]_ ] = _γ_ [ _v_ ] + _γ_ [ _v_ _[′]_ ].


**Addition.** Given two real-valued variables _v, v_ _[′]_, we generally have _γ_ [ _v_ + _v_ _[′]_ ] = max( _γ_ [ _v_ ] _, γ_ [ _v_ _[′]_ ]). The only case where
this is violated is when _v_ _[′]_ = _−v_ . This is generally a zero probability event if _v_ and _v_ _[′]_ are random variables that are not
perfectly correlated, which is the case in most situations where we make use of this formula (see the proofs below).


**A.3. Proof of Proposition 1**


**Proposition 1.** [Inefficiency of LoRA fine-tuning] _Assume that LoRA weights are initialized with Init[1] or Init[2]_
_and trained with gradient descent with learning rate η_ = Θ( _n_ _[c]_ ) _for some c ∈_ R _._ _Then, it is impossible to have δt_ _[i]_ [= Θ(1)]
_for all i for any t >_ 0 _, and therefore, fine-tuning with LoRA in this setup is inefficient._


13


**Effcient Low Rank Adaptation**



_Proof._ Assume that the model is initialized with Init[1]. Since the training dynamics are mainly simple linear algebra
operation (matrix vector products, sum of vectors/scalars etc), it is easy to see that any vector/scaler in the training dynamics
has a magnitude of order _n_ _[γ]_ for some _γ_ _∈_ R (for more details, see the Tensor Programs framework, e.g. (Yang, 2019)).
For any quantity _v_ in the training dynamics, we write _v_ = Θ( _n_ _[γ]_ [[] _[v]_ []] ). When _v_ is a vector, we use the same notation when
all entries of _v_ are Θ( _n_ _[γ]_ [[] _[v]_ []] ). Efficiency is defined by having _δi_ _[t]_ [=] [Θ(1)][ for] _[ i]_ _[∈{]_ [1] _[,]_ [ 2] _[}]_ [ and] _[ t]_ _[>]_ [1][.] [Note that this implies]
_ft_ ( _x_ ) = Θ(1) for all _t_ _>_ 1. Let _t_ _>_ 1 and assume that learning with LoRA is efficient. We will show that this leads to a
contradiction. Efficiency requires that _δt_ _[i]_ [= Θ(1)][ for all] _[ t, i][ ∈{]_ [1] _[,]_ [ 2] _[}]_ [.] [Using the elementary formulas from Appendix][ A.2][,]
this implies that for all _t_
 _γ_ [ _η_ ] + 2 _γ_ [ _bt−_ 1] + 1 = 0



_γ_ [ _η_ ] + 2 _γ_ [ _bt−_ 1] + 1 = 0
_γ_ [ _η_ ] + 2 _γ_ [ _a_ _[⊤]_ _t−_ 1 _[x]_ [] = 0]
_γ_ [ _bt−_ 1] + _γ_ [ _a_ _[⊤]_ _t−_ 1 _[x]_ [] = 0] _[.]_







Solving this equation yields _γ_ [ _η_ ] = _−_ 1 _/_ 2, i.e. LoRA finetuning can be efficient only if the learning rate scales as _η_ =
Θ( _n_ _[−]_ [1] _[/]_ [2] ). Let us now show that this yields a contradiction. From the gradient updates and the elementary operations from
Appendix A.2, we have the following recursive formulas


          _γ_ [ _bt_ ] = max( _γ_ [ _bt−_ 1] _, −_ 1 _/_ 2 + _γ_ [ _a_ _[⊤]_ _t−_ 1 _[x]_ [])]
_γ_ [ _a_ _[⊤]_ _t_ _[x]_ [] = max(] _[γ]_ [[] _[a]_ _t_ _[⊤]_ _−_ 1 _[x]_ []] _[,]_ [ 1] _[/]_ [2 +] _[ γ]_ [[] _[b][t][−]_ [1][])]

Starting from _t_ = 1, with Init[1] we have _γ_ [ _b_ 1] = _γ_ [ _η_ ( _a_ _[⊤]_ 0 _[x]_ [)] _[y]_ [] =] _[ −]_ [1] _[/]_ [2][ and] _[ γ]_ [[] _[a]_ 1 _[⊤][x]_ [] =] _[ γ]_ [[] _[a]_ 0 _[⊤][x]_ [] = 0][, we have] _[ γ]_ [[] _[b]_ [2][] =] _[ −]_ [1] _[/]_ [2]
and _γ_ [ _a_ _[⊤]_ 2 _[x]_ []] [=] [0][.] [Trivially, this holds for any] _[ t]_ [.] [However, this implies that] _[ γ]_ [[] _[f][t]_ []] [=] _[γ]_ [[] _[b][t]_ [] +] _[ γ]_ [[] _[a][⊤]_ _t_ _[x]_ []] [=] _[−]_ [1] _[/]_ [2][ which means]
that ∆ _ft_ cannot be Θ(1). With Init[2], we have _γ_ [ _b_ 1] = _γ_ [ _b_ 0] = 0 and _γ_ [ _a_ _[⊤]_ 1 []] [=] _[γ]_ [[] _[ηb]_ [0] _[y][∥][x][∥]_ [2][]] [=] _[−]_ [1] _[/]_ [2 + 1] [=] [1] _[/]_ [2][.] [From]
the recursive formula we get _γ_ [ _b_ 2] = 0 and _γ_ [ _a_ _[⊤]_ 2 _[x]_ []] [=] [1] _[/]_ [2][ which remains true for all] _[ t]_ [.] [In this case we have] _[ γ]_ [[] _[f][t]_ []] [=] [1] _[/]_ [2]
which contradicts ∆ _ft_ = Θ(1).


In both cases, this contradicts our assumption, and therefore efficiency cannot be achieved in this setup.


**A.4. Proof of Proposition 2**


**Proposition 2.** [Efficient Fine-Tuning with LoRA] _In the case of Toy model Equation_ (2) _,_ _with ηa_ = Θ( _n_ _[−]_ [1] ) _and ηb_ =
Θ(1) _, we have for all t >_ 1 _, ∈{_ 1 _,_ 2 _,_ 3 _}, δt_ _[i]_ [= Θ(1)] _[.]_



_Proof._ The proof is similar in flavor to that of Proposition 1. In this case, the set of equations that should be satisfied so
that _δt_ _[i]_ [= Θ(1)][ are given by]
 _γ_ [ _ηa_ ] + 2 _γ_ [ _bt−_ 1] + 1 = 0



_γ_ [ _ηa_ ] + 2 _γ_ [ _bt−_ 1] + 1 = 0
_γ_ [ _ηb_ ] + 2 _γ_ [ _a_ _[⊤]_ _t−_ 1 _[x]_ [] = 0]
_γ_ [ _ηa_ ] + _γ_ [ _ηb_ ] + _γ_ [ _bt−_ 1] + _γ_ [ _a_ _[⊤]_ _t−_ 1 _[x]_ [] + 1 = 0] _[,]_







where we have used the elementary formulas from Appendix A.2. Simple calculations yield _γ_ [ _ηa_ ] + _γ_ [ _ηb_ ] = _−_ 1. Using
the gradient update expression with the elementary addition from Appendix A.2, the recursive formulas controlling _γ_ [ _bt_ ]
and _γ_ [ _a_ _[⊤]_ _t_ _[x]_ []][ are given by]

         _γ_ [ _bt_ ] = max( _γ_ [ _bt−_ 1] _, γ_ [ _ηb_ ] + _γ_ [ _a_ _[⊤]_ _t−_ 1 _[x]_ [])]
_γ_ [ _a_ _[⊤]_ _t_ _[x]_ [] = max(] _[γ]_ [[] _[a]_ _t_ _[⊤]_ _−_ 1 _[x]_ []] _[, γ]_ [[] _[η][a]_ [] +] _[ γ]_ [[] _[b][t][−]_ [1][] + 1)] _[.]_


Starting from _t_ = 1, with Init[1], we have _γ_ [ _b_ 1] = _γ_ [ _ηb_ ( _a_ _[⊤]_ 0 _[x]_ [)] _[y]_ []] [=] _[γ]_ [[] _[η][b]_ []] [and] _[γ]_ [[] _[a][⊤]_ 1 _[x]_ []] [=] _[γ]_ [[] _[a][⊤]_ 0 _[x]_ []] [=] [0][.] [Therefore]
_γ_ [ _b_ 2] = max( _γ_ [ _ηb_ ] _, γ_ [ _ηb_ ] + 0) = _γ_ [ _ηb_ ], and _γ_ [ _a_ _[⊤]_ 2 _[x]_ []] [=] [max(0] _[, γ]_ [[] _[η][a]_ [] +] _[ γ]_ [[] _[η][b]_ [] + 1)] [=] [max(0] _[,]_ [ 0)] [=] [0][.] [By induction, this]
holds for all _t_ _≥_ 1. With Init[2], we have _γ_ [ _b_ 1] = _γ_ [ _b_ 0] = 0, and _γ_ [ _a_ _[⊤]_ 1 _[x]_ []] [=] _[γ]_ [[] _[−][η][a][b]_ [2] 0 _[y][∥][x][∥]_ [2][]] [=] _[γ]_ [[] _[η][a]_ [] + 1][.] [At] [step]
_t_ = 2, we have _γ_ [ _b_ 2] = max(0 _, γ_ [ _ηb_ ] + _γ_ [ _ηa_ ] + 1) = 0 and _γ_ [ _a_ _[⊤]_ 2 _[x]_ []] [=] [max(] _[γ]_ [[] _[η][a]_ [] + 1] _[, γ]_ [[] _[η][a]_ [] + 0 + 1)] [=] _[γ]_ [[] _[η][a]_ [] + 1][, and]
this holds for all _t_ by induction. In both cases, to ensure that _γ_ [ _ft_ ] = _γ_ [ _bt_ ] + _γ_ [ _a_ _[⊤]_ _t_ _[x]_ []] [=] [0][, we have to set] _[ γ]_ [[] _[η][b]_ []] [=] [0][ and]
_γ_ [ _ηa_ ] = _−_ 1 (straightforward from the equation _γ_ [ _ηb_ ] + _γ_ [ _ηa_ ] = _−_ 1). In conclusion, setting _ηa_ = Θ( _n_ _[−]_ [1] ) and _ηb_ = Θ(1)
ensures efficient fine-tuning with LoRA.


14


**Effcient Low Rank Adaptation**


**A.5. Proof of Theorem 1**


In this section, we give a non-rigorous but intuitive proof of Theorem 1. The proof relies on the following assumption on
the processed gradient _gA_ .

**Assumption 1.** _With the same setup of Section 4, at training step t, we have gA_ _[t]_ _[Z]_ [ = Θ(] _[n]_ [)] _[.]_


To see why Assumption 1 is sound in practice, let us study the product _gA_ _[t]_ [Z][ in the simple case of Adam with no momentum,]
a.k.a SignSGD which is given by




   - _∂L_
_gA_ = sign
_∂A_




_,_



where the sign function is applied element-wise. At training step _t_, we have



_∂Lt_



_t−_ 1 _[d][Z]_ [ ¯] _[t][−]_ [1] _[ ⊗]_ [Z] _[,]_
_r_ _[B][⊤]_



_∂Lt_

_[α]_
_∂A_ [=] _r_



Let _S_ _[t]_ = _[α]_ _r_ _[B]_ _t_ _[⊤]_ _−_ 1 _[d][Z]_ [ ¯] _[t][−]_ [1][.] [Therefore we have]

_gA_ = sign( _S_ _[t]_ _⊗_ Z) = (sign( _Si_ _[t]_ [Z] ~~_j_~~ [))][1] _[≤][i,j][≤][n][.]_


However, note that we also have
sign( _Si_ _[t]_ [Z] _j_ [) =][ sign][(] _[S]_ _i_ _[t]_ [)][sign][(][Z] ~~_j_~~ [)] _[,]_


and as a result
_gA_ _[t]_ [=][ sign][(] _[S][t]_ [)] _[ ⊗]_ [sign][(][Z][)] _[.]_


Hence, we obtain
_gA_ _[t]_ [Z][ = (][sign][(][Z][)] _[⊤]_ [Z][)][sign][(] _[S][t]_ [) = Θ(] _[n]_ [)] _[,]_

where we used the fact that sign(Z) _[⊤]_ Z = Θ( _n_ ).


This intuition should in-principle hold for the general variant of Adam with momentum as long as the gradient processing
function (a notion introduced in (Yang et al., 2013)) roughly preserves the sign(Z) direction. This reasoning can be made
rigorous for general gradient processing function using the Tensor Program framework and taking the infinite-width limit
where the components of _gA,_ Z _, dZ_ [¯] all become iid. However this necessitates an intricate treatment of several quantities in
the process, which we believe is an unnecessary complication and does not serve the main purpose of this paper.


Let us now give a proof for the main claim.


**Theorem 1.** _Assume that weight matrices A and B_ _are trained with Adam with respective learning rates ηA_ _and ηB_ _and_
_that Assumption 1 is satisifed with the Adam gradient processing function._ _Then, it is impossible to achieve efficiency with_
_ηA_ = _ηB._ _However, LoRA Finetuning is efficient with ηA_ = Θ( _n_ _[−]_ [1] ) _and ηB_ = Θ(1) _._



_Proof._ With the same setup of Section 4, at step _t_, we have

 _δt_ [1] [=] _[ B][t][−]_ [1][∆] _[Z]_ _A_ _[t]_



_δt_ [1] [=] _[ B][t][−]_ [1][∆] _[Z]_ _A_ _[t]_ [=] _[ −][η][A][B][t][−]_ [1] _[g]_ _A_ _[t][−]_ [1] Z
_δt_ [2] [= ∆] _[B][t][Z]_ _A_ _[t][−]_ [1] = _−ηBgB_ _[t][−]_ [1] _At−_ 1Z
_δt_ [3] [= ∆] _[B][t]_ [∆] _[Z]_ _A_ _[t]_ [=] _[ η][A][η][B][g]_ _B_ _[t][−]_ [1] _gA_ _[t][−]_ [1] Z







The key observation here is that _gA_ _[t][−]_ [1] Z has entries of order Θ( _n_ ) as predicted and justified in Assumption 1. Having
_δt_ _[i]_ [= Θ(1)][ for] _[ i][ ∈{]_ [1] _[,]_ [ 2] _[}]_ [ and] _[ Z]_ _B_ _[t]_ [= Θ(1)][ for] _[ t >]_ [ 1][ translate to]
 _γ_ [ _ηA_ ] + _γ_ [ _Bt−_ 1] + 1 = 0



_γ_ [ _ηA_ ] + _γ_ [ _Bt−_ 1] + 1 = 0
_γ_ [ _ηB_ ] + _γ_ [ _At−_ 1Z] = 0
_γ_ [ _Bt−_ 1] + _γ_ [ _At−_ 1Z] = 0 _,_







15


which implies that _γ_ [ _ηA_ ] + _γ_ [ _ηB_ ] = _−_ 1.


With the gradient updates, we have


which implies that



**Effcient Low Rank Adaptation**


_Bt_ = _Bt−_ 1 _−_ _ηBgB_ _[t][−]_ [1]
_At_ Z = _At−_ 1Z _−_ _ηAgA_ _[t][−]_ [1] Z


_γ_ [ _Bt_ ] = max( _γ_ [ _Bt−_ 1] _, γ_ [ _ηB_ ])


_γ_ [ _At_ Z] = max( _γ_ [ _At−_ 1Z] _, γ_ [ _ηA_ ] + 1) _,_



Now assume that the model is initialized with Init[1]. We have _γ_ [ _B_ 1] = _γ_ [ _ηB_ ] and therefore for all _t_, we have
_γ_ [ _Bt_ ] = _γ_ [ _ηB_ ]. We also have _γ_ [ _A_ 1Z] = _γ_ [ _A_ 0Z] = 0 (because _A_ 1 = _A_ 0, and we use the Central Limit Theorem to
conclude). Hence, if we choose the same learning rate for _A_ and _B_, given by _η_, we obtain _γ_ [ _η_ ] = _−_ 1 _/_ 2, and therefore
_γ_ [ _ZA_ _[t][−]_ [1] ] = _γ_ [ _At−_ 1Z] = 1 _/_ 2 which violates the stability condition. A similar behaviour occurs with Init[2]. Hence,
efficiency is not possible in this case. However, if we set _γ_ [ _ηB_ ] = 0 and _γ_ [ _ηA_ ] = _−_ 1, we get that _γ_ [ _Bt_ ] = 0 _, γ_ [ _At_ Z] = 0,
and _δt_ _[i]_ [= Θ(1)][ for all] _[ i][ ∈{]_ [1] _[,]_ [ 2] _[,]_ [ 3] _[}]_ [ and] _[ t][ ≥]_ [1][.] [The same result holds with][ Init[2]][.]


**B. Efficiency from a Loss Perspective.**


Consider the same setup of Section 4. At step _t_, the loss changes as follows


∆ _L_ = _L_ (( _BA_ ) _t_ ) _−L_ (( _BA_ ) _t−_ 1)

_≈⟨dZ_ [¯] _[t][−]_ [1] _⊗_ Z _,_ ( _BA_ ) _t −_ ( _BA_ ) _t−_ 1 _⟩F_
= _⟨dZ_ [¯] _[t][−]_ [1] _,_ ∆ _ZB_ _[t]_ _[⟩][,]_

where _⟨., .⟩F_ is the Frobenius inner product in R _[n][×][n]_, and _⟨., .⟩_ is the euclidean product in R _[n]_ . Since the direction of the
feature updates are significantly correlated with _dZ_ [¯] _[t][−]_ [1], it should be expected that having _δt_ _[i]_ [=] [Θ(1)] [for] [all] _[i]_ [results] [in]
more efficient loss reduction.


**C. Additional Experiments**


This section complements the empirical results reported in the main text. We provide the details of our experimental setup,
and show the acc/loss heatmaps for several configurations.


**C.1. Empirical Details**


C.1.1. TOY EXAMPLE


In Figure 2, we trained a simple MLP with LoRA layers to verify the results of the analysis in Section 3. Here we provide
the empirical details for these experiments.


**Model.** We consider a simple MLP given by


_f_ ( _x_ ) = _Woutϕ_ ( _BAϕ_ ( _Winx_ )) _,_


where _Win_ _∈_ R _[n][×][d]_ _, Wout_ _∈_ R [1] _[×][n]_ _, A_ _∈_ R _[r][×][n]_ _, B_ _∈_ R _[n][×][r]_ are the weights, and _ϕ_ is the ReLU activation function. Here,
we used _d_ = 5, _n_ = 100, and _r_ = 4.


**Dataset.** Synthetic dataset generated by _X_ _∼N_ (0 _, Id_ ) _, Y_ = sin( _d_ _[−]_ [1][ �] _[d]_ _i_ =1 _[X][i]_ [)] [with] _[d]_ [=] [5][.] [The] [number] [of] [training]
examples is _Ntrain_ = 1000, and the number of test examples is _Ntest_ = 100.


**Training.** We train the model with gradient descent for a range for values of ( _ηA, ηB_ ). The weights are initialized as
follows: _Win_ _∼N_ (0 _,_ 1 _._ ) _, Wout_ _∼N_ (0 _,_ 1 _/n_ ) _, A ∼N_ (0 _,_ 1 _/n_ ) _, B_ _∼N_ (0 _,_ 1 _._ ). Only the weight matrices _A, B_ are trained
and _Win, Wout_ are fixed to their initial value.


16


**Effcient Low Rank Adaptation**


C.1.2. GLUE TASKS WITH GPT2/ROBERTA


For our experiments with GPT2/Roberta-base models, finetuned on GLUE tasks, we use the following setup:


**Tasks.** MNLI, QQP, SST2, QNLI


**Models.** GPT2, Roberta-base


**Training Alg.** AdamW with _β_ 1 = 0 _._ 9 _, β_ 2 = 0 _._ 99 _, ϵ_ = 1e-8, linear schedule, no warmup.


**Learning rate grid.** _ηA_ _∈{_ 4e-3, 2e-3, 1e-3, 5e-4, 2e-4, 1e-4 _}_, _ηB_ _∈{_ 8e-4, 4e-4, 2e-4, 1e-4, 5e-5, 2e-5, 1e-5 _}_ .


**Targert Modules for LoRA.** For Roberta-base, we add LoRA layers to ‘query’ and ‘value’ weights. For GPT2, we add
LoRA layers to ‘c_attn, c_proj, c_fc’.


**Other Hyperparameters.** Sequence length _T_ = 128, train batch size _bs_ = 32, number of train epochs _E_ = 3 ( _E_ = 10
for SST2), number of random seeds _s_ = 3.


**GPUs.** Nvidia V100, Nvidia A10.


C.1.3. LLAMA MNLI


For our experiments using the Llama-7b model, finetuned on MNLI, we use following setup


**Training Alg.** AdamW with _β_ 1 = 0 _._ 9, _β_ 2 = 0 _._ 999, _ϵ_ = 1e-6, constant schedule.


**Learning rate grid.** _ηA_ _∈{_ 1e-6, 5e-6, 1e-5, 2.5e-5, 5e-5, 1e-4 _}_, _ηB_ _∈{_ 1e-6, 5e-6, 1e-5, 2.5e-5, 5e-5, 1e-4 _}_, _ηB_ _≥_ _ηA_


**LoRA Hyperparameters.** LoRA rank _r_ = 8, _α_ = 16, and dropout 0 _._ 1. LoRA target modules ‘q_proj, k_proj, v_proj,
o_proj, up_proj, down_proj, gate_proj’.


**Other Hyperparameters.** Sequence length _T_ = 128, train batch size _bs_ = 32, number of train epochs _E_ = 1, number
of random seeds _s_ = 2 for _ηA_ = _ηB_ and _ηA, ηB_ near test optimal, _s_ = 1 otherwise. Precision FP16.


**GPUs.** Nvidia V100.


C.1.4. LLAMA FLAN-V2


For our experiments using the Llama-7b model, finetuned on a size 100k random subset flan-v2, we use following setup


**Training Alg.** AdamW with _β_ 1 = 0 _._ 9, _β_ 2 = 0 _._ 999, _ϵ_ = 1e-6, constant schedule.


**Learning rate grid.** _ηA_ _∈{_ 1e-6, 5e-6, 1e-5, 2.5e-5, 5e-5, 1e-4 _}_, _ηB_ _∈{_ 1e-6, 5e-6, 1e-5, 2.5e-5, 5e-5, 1e-4 _}_, _ηB_ _≥_ _ηA_


**LoRA Hyperparameters.** LoRA rank _r_ = 64, _α_ = 16, and dropout 0 _._ 1. LoRA target modules ‘q_proj, k_proj, v_proj,
o_proj, up_proj, down_proj, gate_proj’.


**Other** **Hyperparameters.** Sequence length _T_ source = 1536, _T_ target = 512, train batch size _bs_ = 16, number of epochs
_E_ = 1, number of random seeds _s_ = 2 for _ηA_ = _ηB_ and _ηA, ηB_ near test optimal, _s_ = 1 otherwise. Precision BF16.


**MMLU Evaluation.** We evaluate average accuracy on MMLU using 5-shot prompting.


**GPUs.** Nvidia A10.


17


**Effcient Low Rank Adaptation**


**C.2. Results of Roberta-base Finetuning on all Tasks**


Figure 3 showed finetuning test accuracy for Roberta-base. To complement these results, we show here the test/train
accuracy for all tasks.



SST2


A



0.94


0.93


0.92


0.91


0.90


0.98


0.96


0.94


0.92


0.90



QQP


A



0.89


0.88


0.87


0.86


0.92


0.90


0.88


0.86



4.0e-03

2.0e-03

1.0e-03

5.0e-04

2.0e-04

1.0e-04


4.0e-03

2.0e-03

1.0e-03

5.0e-04

2.0e-04

1.0e-04



MNLI


A



0.86


0.84


0.82


0.80

0.90

0.88

0.86

0.84

0.82

0.80



QNLI


A



0.92


0.90


0.88


0.86


0.94

0.92

0.90

0.88

0.86



_Figure 8._ GLUE/Roberta-base: same as Figure 3 with test/train accuracy.


Interestingly, the optimal choice of learning rates for test accuracy differs from that of the train accuracy, although the
difference is small. This can be due to mild overfitting occuring during finetuning (the optimal choice of learning rates
( _ηA, ηB_ ) for train accuracy probably lead to a some overfitting).


**C.3. Results of GPT2 Finetuning on all Tasks**


Figure 4 showed finetuning results for GPT2 on MNLI and QQP. To complement these results, we show here the test/train
accuracy for all tasks.



4.0e-03

2.0e-03

1.0e-03

5.0e-04

2.0e-04

1.0e-04


4.0e-03

2.0e-03

1.0e-03

5.0e-04

2.0e-04

1.0e-04



MNLI


A



0.81

0.80

0.79

0.78

0.77


0.875

0.850

0.825

0.800

0.775



SST2


A



0.915

0.910

0.905

0.900

0.895


0.98


0.96


0.94


0.92


0.90



QNLI


A



0.87

0.86

0.85

0.84

0.83


0.925

0.900

0.875

0.850

0.825



QQP


A



0.88

0.87

0.86

0.85

0.84


0.94

0.92

0.90

0.88

0.86



_Figure 9._ GLUE/GPT2: same setup as Figure 4 with additional tasks


18


**Effcient Low Rank Adaptation**



**C.4. GLUE Tasks with Full Precision**


MNLI



A



SST2



QNLI





4.0e-03

2.0e-03

1.0e-03

5.0e-04

2.0e-04

1.0e-04


4.0e-03

2.0e-03

1.0e-03

5.0e-04

2.0e-04

1.0e-04


4.0e-03

2.0e-03

1.0e-03

5.0e-04

2.0e-04

1.0e-04


4.0e-03

2.0e-03

1.0e-03

5.0e-04

2.0e-04

1.0e-04



0.89


0.88


0.87


0.86


0.92


0.90


0.88


0.86





QQP


A





A



0.86


0.85


0.84


0.83


0.90


0.88


0.86


0.84


0.82





















0.94


0.93


0.92


0.91


0.96


0.94


0.92





A



_Figure 10._ GLUE/Roberta-base: same as Figure 3 with full precision training instead of FP16.



MNLI



QQP



SST2



QNLI















































0.81


0.80


0.79


0.78


0.875

0.850

0.825

0.800





0.88


0.87


0.86


0.85


0.94


0.92


0.90


0.88


0.86





0.915


0.910


0.905


0.900


0.98


0.96


0.94


0.92





0.92


0.91


0.90


0.89


0.88


0.94


0.92


0.90


0.88


0.875

0.850

0.825

0.800

0.775

0.750


0.90


0.85


0.80


0.75

















A



A



A



A



_Figure 11._ GLUE/GPT2: same setup as Figure 9 with full precision training


19


**Effcient Low Rank Adaptation**



**C.5. GLUE Tasks Test/Train Loss**


MNLI

4.0e-03



A



QQP


A



0.32


0.30


0.28


0.300

0.275

0.250

0.225

0.200



QNLI


A



SST2





2.0e-03

1.0e-03

5.0e-04

2.0e-04

1.0e-04


4.0e-03

2.0e-03

1.0e-03

5.0e-04

2.0e-04

1.0e-04



A



0.500

0.475

0.450

0.425

0.400


0.50


0.45


0.40


0.35


0.30







0.40


0.35


0.30


0.25


0.4


0.3


0.2


0.1







_Figure 12._ GLUE/Roberta-base: same setup as Figure 3 with 100 _×_ Test/Train loss instead of accuracy



0.40


0.35


0.30


0.25


0.40

0.35

0.30

0.25

0.20

0.15


0.40


0.38


0.36


0.34


0.32


0.40

0.35

0.30

0.25

0.20

0.15



QNLI


A



4.0e-03

2.0e-03

1.0e-03

5.0e-04

2.0e-04

1.0e-04


4.0e-03

2.0e-03

1.0e-03

5.0e-04

2.0e-04

1.0e-04



MNLI


A



0.54


0.52


0.50


0.48

0.55

0.50

0.45

0.40

0.35

0.30



QQP


A



0.34


0.32


0.30


0.30


0.25


0.20


0.15



SST2



A







0.36

0.34

0.32

0.30

0.28


0.25


0.20


0.15


0.10


0.05





_Figure 13._ GLUE/GPT2: same setup as Figure 9 with 100 _×_ Test/Train loss instead of accuracy


20


**Effcient Low Rank Adaptation**


**C.6. GLUE Tasks with Different LoRA Ranks**



QNLI





SST2



4.0e-03

2.0e-03

1.0e-03

5.0e-04

2.0e-04

1.0e-04


4.0e-03

2.0e-03

1.0e-03

5.0e-04

2.0e-04

1.0e-04



MNLI



























0.86


0.85


0.84


0.83


0.82


0.88


0.86


0.84


0.82





0.94


0.93


0.92


0.91


0.96


0.94


0.92





0.91

0.90

0.89

0.88

0.87

0.94


0.92


0.90


0.88


0.86







A



A



A



_Figure 14._ GLUE/Roberta-base: same setup as Figure 3 with _r_ = 4



SST2



QNLI



4.0e-03

2.0e-03

1.0e-03

5.0e-04

2.0e-04

1.0e-04


4.0e-03

2.0e-03

1.0e-03

5.0e-04

2.0e-04

1.0e-04























0.940

0.935

0.930

0.925

0.920


0.96


0.94


0.92





0.92


0.91


0.90


0.89


0.88


0.94


0.92


0.90


0.88





A



A



_Figure 15._ GLUE/Roberta-base: same setup as Figure 3 with _r_ = 16



SST2



QNLI



4.0e-03

2.0e-03

1.0e-03

5.0e-04

2.0e-04

1.0e-04


4.0e-03

2.0e-03

1.0e-03

5.0e-04

2.0e-04

1.0e-04



















0.925

0.920

0.915

0.910

0.905

0.900


0.96


0.94


0.92





0.875

0.870

0.865

0.860

0.855

0.850


0.92

0.90

0.88

0.86

0.84







A



A



_Figure 16._ GLUE/GPT2: same setup as Figure 11 with _r_ = 4


21


**Effcient Low Rank Adaptation**



MNLI - Init[1]



MNLI - Init[2]



4.1e-02

1.0e-02

5.1e-03

2.6e-03

1.3e-03

6.4e-04

3.2e-04

3.1e-04



4.1e-02

1.0e-02

5.1e-03

2.6e-03

1.3e-03

6.4e-04

3.2e-04

3.1e-04





86


85


84


83


82


81





86


85


84


83


82


81



_Figure 17._ Roberta-base with Init[1] and Init[2], finetuning on MNLI for 10 epochs (similar to Figure 3 but with more epochs).


**C.7. Experiments with Init[1]**


We also run some experiments using Init[1] as initialization scheme. We noticed that the optimal ratio _λ_ is this case
is generally smaller than the optimal ratio with Init[2]. Figure 17 shows the optimal learning rates ( _ηA, ηB_ ) obtained
with Init[1] and Init[2]. The optimal ratio _λ_ = _ηB/ηA_ is generally smaller with Init[1].


22


**Effcient Low Rank Adaptation**


**C.8. Llama Flan-v2 MMLU Acc/Train Loss**







2.0e-03

1.0e-03

5.0e-04

4.0e-04

2.0e-04

1.0e-04

5.0e-05

1.0e-05







44


42


40


38


36


34


32


30





95


90


85


80


75


70


65















A



A



(a) MMLU evaluation accuracy and train loss of Llama-7b trained on flan-v2 100k in the same
setting as Figure 5 left panel (using Init[2]). Interestingly, even in one epoch the model
can overfit. We were unable to find _ηB_ _>_ _ηA_ that was optimal for train loss, however it could
be the case that the grid was not fine enough or that overfitting does not require much “feature
learning" and _ηB/ηA_ _≈_ 1 is optimal for minimizing train loss (see the main text for more
discussion).


(b) MMLU evaluation accuracy and train loss of Llama-7b trained on flan-v2 100k in the
same setting as Figure 5 left panel except using Init[1]. Interestingly, the optimal MMLU
accuracy is 0.6% higher than using Init[2] and the optimal ratio _ηB/ηA_ is twice as large.
The training loss is also near optimal only using a large ratio _ηB/ηA_ .


_Figure 18._ Llama-7b on flan-v2 training with different initializations.


23


**Effcient Low Rank Adaptation**



**C.9. Llama MNLI Test/Train Loss**


4.0e-04

2.0e-04

1.0e-04

5.0e-05

1.0e-05

5.0e-06

1.0e-06







80


70


60


50


40


30


20


10







40


38


36


34


32


30


28















A



A



_Figure 19._ Train and test loss of Llama-7b finetuned on MNLI in the same setting as Figure 5 right panel.


24


