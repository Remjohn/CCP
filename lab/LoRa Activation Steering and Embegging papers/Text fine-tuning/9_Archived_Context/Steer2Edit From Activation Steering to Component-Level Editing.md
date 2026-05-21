### **Steer2Edit: From Activation Steering to Component-Level Editing**

**Chung-En Sun** [1] **Ge Yan** [* 1] **Zimo Wang** [* 2] **Tsui-Wei Weng** [2]



**Abstract**


Steering methods influence Large Language
Model behavior by identifying semantic directions in hidden representations, and are typically realized through inference-time activation
interventions that apply a fixed, global modification to the model’s internal states. While
effective, such interventions often induce unfavorable attribute–utility trade-offs under strong
control, as they ignore the fact that many behaviors are governed by a small and heterogeneous subset of model components. To alleviate the trade-offs, we propose **STEER2EDIT**, a
theoretically grounded, training-free framework
that transforms steering vectors from inferencetime control signals into diagnostic signals for
component-level rank-1 weight editing. Instead
of uniformly injecting a steering direction during generation, **STEER2EDIT** selectively redistributes behavioral influence across individual
attention heads and MLP neurons, yielding interpretable edits that preserve the standard forward pass and remain compatible with optimized
parallel inference. Across multiple tasks including safety alignment, truthfulness promotion,
and reasoning efficiency, **STEER2EDIT** consistently achieves more favorable attribute–utility
trade-offs: at matched downstream performance, it improves safety by up to 17.2%, increases truthfulness by 9.8%, and reduces reasoning length by 12.2% on average. Overall,
**STEER2EDIT** provides a principled bridge between representation steering and weight editing
by translating steering signals into _interpretable_,
_training-free_ parameter updates. Our code is
available at: [https://github.com/Trustworthy-ML-](https://github.com/Trustworthy-ML-Lab/Steer2Edit)
[Lab/Steer2Edit](https://github.com/Trustworthy-ML-Lab/Steer2Edit)


1Department of Computer Science and Engineering, UC San
Diego [2] Halıcıoglu˘ Data Science Institute, UC San Diego. Correspondence to: Chung-En Sun _<_ cesun@ucsd.edu _>_, Tsui-Wei
Weng _<_ lweng@ucsd.edu _>_ .


_Preprint._



**1. Introduction**


Large Language Models (LLMs) have demonstrated strong
capabilities across a wide range of tasks, including multistep reasoning (Guo et al., 2025), code generation (Chen,
2021), and planning (Yao et al., 2023). As these models
are increasingly deployed in real-world settings, there is
growing interest in _controlling_ specific model behaviors
without retraining or fully fine-tuning the model.


A prominent line of recent work addresses this goal through
_representation_ _steering_ (Zou et al., 2023a; Turner et al.,
2023; Arditi et al., 2024; Yan et al., 2025; Li et al., 2025).
These methods identify a _steering_ _vector_ in the model’s
hidden representation space that correlates with a target
attribute, and then intervene at inference time by adding
this vector to intermediate activations. Compared to full
fine-tuning, steering-based methods offer a lightweight way
to adapt a model to different behaviors.


Despite their flexibility, activation-space steering methods
suffer from two fundamental limitations. _First_, steering
applies a _global_ modification to the hidden representation.
While such interventions can induce the target behavior,
they treat all tokens and internal components uniformly, regardless of how the behavior is realized within the model.
Empirical and mechanistic studies show that many behaviors
are governed by a small and heterogeneous subset of model
components (Olsson et al., 2022; Meng et al., 2022; Zhao
et al., 2025; Zhou et al., 2024; Chu et al., 2025), typically
involving specific attention heads or MLP neurons, while
most components are only weakly related or unrelated to the
target attribute. By ignoring this internal structure, global
steering can interfere with unrelated semantic features, resulting in unfavorable trade-offs between the controlled
attribute and downstream performance.


_Second_, activation-space steering relies on inference-time
modification of intermediate activations. This departs from
the standard forward pass assumed by modern optimized
inference and training systems, which typically require fixed
computation graphs. As a result, activation-level interventions complicate integration with standard deployment, parallel inference, and fine-tuning pipelines. While this limitation can in principle be mitigated with additional system
engineering, activation steering remains an inference-time
control mechanism whose effects are tied to the decoding



1


**Steer2Edit:** **From Activation Steering to Component-Level Editing**



process, rather than being encoded in the model parameters.


These limitations motivate a different perspective: instead
of treating steering vectors as control signals to be directly
injected into the forward pass, can we reinterpret them as
_diagnostic signals_ that reveal how a target behavior is distributed across model components? If so, can this information be used to selectively modify the components that
genuinely govern the behavior, while avoiding unnecessary
interference that degrades utility?


To answer these questions, we introduce **STEER2EDIT**, a
theoretically grounded framework that converts steering vectors into _component-level weight edits_ . In **STEER2EDIT**,
a steering vector is treated as a diagnostic signal that reveals which attention heads and MLP neurons align with
a target behavior, and to what extent. Guided by this signal, the method applies coordinated rank-1 updates to individual components, selectively amplifying or suppressing
their contributions along the steering direction, rather than
inducing a global activation shift. By redistributing behavioral influence at the component level, **STEER2EDIT**
enables more precise behavioral control and more favorable attribute–utility trade-offs, while yielding interpretable
component-level edits. The resulting procedure is closedform, requires no fine-tuning or iterative optimization, and
produces a standalone edited model that operates under the
standard forward pass and remains compatible with existing
training and optimized parallel inference pipelines.


**Contributions.**

 - We propose **STEER2EDIT**, the first theoretically
grounded framework that translates steering vectors into
component-level rank-1 weight edits, requiring no finetuning and admitting a closed-form, single-step solution.


 - We show that **STEER2EDIT** consistently achieves a
superior attribute–performance trade-off compared to
activation-level steering across diverse behavioral control
settings: when matched for downstream performance, it
improves safety by **17.2%**, truthfulness by **9.8%**, and, in
the efficient reasoning setting, reduces reasoning length
by **12.2%** on average.


 - We show that **STEER2EDIT** produces a standalone
edited model that preserves the original architecture,
while offering fine-grained interpretability into which
components govern specific behaviors and how these
behaviors are distributed across the network.


**2. Preliminary**


In this section, we fix notation for the Transformer residual stream, define the steering vectors used throughout,
and specify the editable weight components used in later
**STEER2EDIT** analysis.



**Transformer residual-stream updates.** We consider a
pre-normalization Transformer, where the residual stream
is updated at layer _ℓ_ according to
_rℓ_ [attn] = _rℓ_ [mlp] _−_ 1 [+] _[ δ]_ _ℓ_ [attn] _,_ _δℓ_ [attn] := Attn�LayerNorm( _rℓ_ [mlp] _−_ 1 [)] - _,_

_rℓ_ [mlp] = _rℓ_ [attn] + _δℓ_ [mlp] _,_ _δℓ_ [mlp] := MLP�LayerNorm( _rℓ_ [attn][)] - _._

Both _δℓ_ [attn] and _δℓ_ [mlp] lie in the same residual-stream space R _[d]_ .


**Steering vector.** Steering vectors are commonly used in
activation steering, where a semantic direction in hidden representations is added to the residual stream at inference time
to control model behavior. Such vectors can be constructed
in various ways. For simplicity, we adopt a mean-difference
construction in this work, while noting that **STEER2EDIT**
is agnostic to how the steering vector is obtained.


Let _X_ denote a set of prompts. For each prompt _x_ _∈X_,
the model generates a completion _y_, which is classified as
exhibiting or not exhibiting the target attribute, yielding _Y_ pos
and _Y_ neg.


At token position _t_ of _y_, let _δℓ_ _[b]_ [(] _[y, t]_ [)] _[ ∈]_ [R] _[d]_ [,] _[ b][ ∈{]_ [attn] _[,]_ [ mlp] _[}][,]_
denote the output of the corresponding block at layer _ℓ_
before it is written into the residual stream. Aggregating
over token positions _Ty_ and averaging over generations, we
define



The steering vector at layer _ℓ_ and block _b_ is given by the
mean difference
~~_b_~~ ~~_b_~~
_vℓ_ _[b]_ [=] _[ δ]_ _ℓ,_ pos _[−]_ _[δ]_ _ℓ,_ neg _[∈]_ [R] _[d][.]_ (1)


**Editable** **weight** **components** **and** **notation.** We focus
on linear weight components whose outputs produce the
block activations from which the steering vectors in Eq.(1)
are extracted. Specifically, for each layer _ℓ_ and block type
_b_ _∈{_ attn _,_ mlp _}_, we consider linear maps whose outputs
contribute to the block output _δℓ_ _[b]_ _[before]_ [ it is written into the]
residual stream.


Concretely, these editable components include: (i) the output projection ( _o_ ~~_p_~~ _roj_ ) of an individual attention head in the
attention block, and (ii) the down-projection ( _down_ ~~_p_~~ _roj_ )
associated with a single neuron in the MLP block. We
denote any such component generically by
_Wi_ _∈_ R _[d]_ [out] _[×][d]_ [in] _,_ _d_ out = _d,_
where the index _i_ implicitly identifies a specific layer _ℓ_,
block type _b_, and component within that block.


For an input activation _hi_ _∈_ R _[d]_ [in] to component _Wi_, the
component output _Wihi_ lies in the same residual-stream
space R _[d]_ as the corresponding steering vector _vℓ_ _[b]_ [.] [Accord-]
ingly, in the subsequent analysis we associate each editable
component _Wi_ with the steering vector extracted from the
same layer and block, and write this vector simply as _vi_ .



~~_b_~~ 1
_δℓ,a_ [=]
_|Ya|_






_y∈Ya_




- _δℓ_ _[b]_ [(] _[y, t]_ [)] _[,]_ _a ∈{_ pos _,_ neg _}._

_t∈Ty_



1
_|Ty|_



2


**Steer2Edit:** **From Activation Steering to Component-Level Editing**





























_Figure 1._ Overview of STEER2EDIT. STEER2EDIT converts the steering signal into component-level rank-1 weight edits. For each
component, the edit ∆ _Wi_ = _λiuiki_ _[⊤]_ [is] [constructed] [by] [aligning] [the] [output] [direction] _[u][i]_ [with] [the] [steering] [vector,] [choosing] [an] [input]
direction _ki_ that triggers the edit only on relevant inputs, and allocating the magnitude _λi_ under a global budget. The resulting edits are
training-free, architecture-preserving, and interpretable.



**3. Steer2Edit**


In this section, we introduce **STEER2EDIT**, a principled
framework for component-level weight editing based on
given steering vectors. We parameterize each edit as a rank-1
update and derive its form by decomposing the problem into
three parts: (i) identifying the output-space direction that
preserves semantic invariance, (ii) the input-space direction
that aligns the edit with the component’s intrinsic semantic
contribution, and (iii) the scalar magnitude that allocates
edit strength under a global regularization budget.


**3.1. Assumption and Setting**


For each editable component _Wi_ _∈_ R _[d]_ [out] _[×][d]_ [in], we assume
the existence of a steering vector _vi_ _∈_ R _[d]_ [out] extracted from
the same representation space into which _Wi_ writes (e.g.,
the hidden state after an attention or MLP block). Thus,
the output dimension of _Wi_ matches that of _vi_, and both lie
in a common semantic space. Note that **STEER2EDIT** is
agnostic to how _vi_ is obtained.


Our goal is to modify each component _Wi_ so that the resulting update ∆ _Wi_ alters the model’s behavior along the
semantic direction represented by _vi_ . Because the steering
signal specifies a single direction in representation space,
we model each edit as a rank-1 perturbation, which is the
minimal modification that can inject a directional effect into
a linear map. Accordingly, we parameterize the edit as

∆ _Wi_ = _λi uiki_ _[⊤][,]_

where _ui_ _∈_ R _[d]_ [out] is an output-space direction, _ki_ _∈_ R _[d]_ [in] is
an input-space direction, and _λi_ _∈_ R is a scalar magnitude
controlling the strength of the edit.



Given an input activation _hi_, let _oi_ := _Wihi_ _∈_ R _[d]_ [out] denote
the original output of component _Wi_ . After applying the
rank-1 edit ∆ _Wi_ = _λiuiki_ _[⊤]_ [,] [the] [edited] [output] [is] _[o]_ [˜] _[i]_ [:=]
( _Wi_ + ∆ _Wi_ ) _hi_ = _oi_ + ∆ _oi,_ where the induced output shift
is
∆ _oi_ := ∆ _Wihi_ = _λi ui_ ( _ki_ _[⊤][h][i]_ [)] _[.]_ (2)


The three quantities ( _ui, ki, λi_ ) play distinct roles in the
edit. The output-space direction _ui_ specifies the semantic
direction affected by the edit, the input-space direction _ki_
determines which inputs activate the edit through the inner
product _ki_ _[⊤][h][i]_ [,] [and] [the] [scalar] [magnitude] _[λ][i]_ [controls] [how]
strongly each component is modified.


We derive these quantities in a sequential order. We first
determine _ui_, then _ki_, and finally solve for _{λi}_ _[n]_ _i_ =1 [,] [the]
per-component edit magnitudes. As shown in the following
sections, this ordering is without loss of generality: the
optimal choice of _ui_ depends only on the steering vector _vi_ ;
the choice of _ki_ depends on _ui_ and local properties of the
component _Wi_ ; and once the geometric directions are fixed,
the magnitudes _{λi}_ can be optimized independently.


Hence, we derive the three components of the edit in the
following order:


1. the output-space direction _ui_ in Section 3.2;


2. the input-space direction _ki_ in Section 3.3;


3. the scalar magnitude _λi_ in Section 3.4.


Throughout the following derivations, we identify only the
directions of _ui_ and _ki_ ; their scale and sign are absorbed
into the scalar coefficients _λi_, which are determined in the
last step.



3


**Steer2Edit:** **From Activation Steering to Component-Level Editing**



**3.2. Step 1:** **Solving for the Output-space Direction** _ui_


The vector _ui_ determines the _direction_ of the output shift
∆ _oi_ . Because the steering signal specifies a single semantic
direction _vi_, we require that the edit modifies the component’s output _only_ along this direction and introduces no
change in any orthogonal subspace.


Formally, recall that ∆ _oi_ = ∆ _Wihi._ Semantic invariance
requires that, for any input _hi_, the output shift ∆ _oi_ has zero
projection onto any direction orthogonal to _vi_ :

_z_ _[⊤]_ ∆ _oi_ = _z_ _[⊤]_ ∆ _Wihi_ = 0 _∀_ _hi,_ _∀_ _z_ _⊥_ _vi._ (3)


This constraint directly restricts the output-space direction
_ui_ of the edit. The following theorem formalizes this restriction.


**Theorem 3.1** (Output-space direction under semantic invariance) **.** _Let vi_ = 0 _, and let_ ∆ _Wi_ = _λi uiki_ _[⊤]_ _[be a rank-1 edit]_
_with_ ∆ _Wi_ = 0 _._ _If for all hi_ _and all z_ _⊥_ _vi_ _we have_

_z_ _[⊤]_ ∆ _Wihi_ = 0 _,_


_then the output-space direction ui_ _must be collinear with vi,_
_i.e.,_
_ui_ _∈_ span _{vi}._


We defer the proof to Appendix A.1. Theorem 3.1 shows
that enforcing semantic invariance in Eq.(3) uniquely constrains the output-space direction: any valid rank-1 update
must lie entirely along the steering direction _vi_ . Importantly,
this result is independent of both the input-space direction
_ki_ and the scalar magnitude _λi_ . This separation justifies
solving for _ui_ first in our derivation.


We therefore adopt the canonical normalized choice

_vi_
_ui_ = _v_ ˆ _i_ := _∥vi∥_ 2 _,_


with the sign and scale absorbed later into the magnitude _λi_ .


**3.3. Step 2:** **Solving for the Input-space Direction** _ki_


Having solved the output-space direction _ui_ = _v_ ˆ _i_ in Section 3.2, we now determine the input-space direction _ki_ for
each editable component _Wi_ . As before, we solve for the
_direction_ of _ki_ ; its sign and scale are absorbed into the scalar
magnitude _λi_ .


**Intuition.** As shown in Eq. (2), the input-space direction
_ki_ determines which input activations _hi_ trigger the edit
through the inner product _ki_ _[⊤][h][i]_ [.] [To identify a suitable] _[ k][i]_ [,]
we note that a well-trained component _Wi_ already encodes
which inputs are relevant for contributing to the semantic
direction _vi_, and the edit ∆ _Wi_ should mirror this existing
input-dependent pattern.


To formalize this intuition, we define the _semantic alignment_
_score_ of component _Wi_ for an input _hi_ as

_si_ ( _hi_ ) := _vi_ _[⊤][o][i]_ [=] _[ v]_ _i_ _[⊤][W][i][h][i][,]_



where _oi_ := _Wihi_, which measures how strongly the original component output aligns with the target semantic direction _vi_ for a given input _hi_ . Intuitively, if _si_ ( _hi_ ) is small
across inputs, this indicates that the component is generally
unrelated to the semantic direction _vi_, and the edit should
be small for all inputs similarly. If, for some components,
_si_ ( _hi_ ) is large for certain inputs, the edit should be large on
those same inputs.


Hence, we choose _ki_ so that the induced change in the
semantic alignment score, ∆ _si_ ( _hi_ ) := _vi_ _[⊤]_ [∆] _[W][i][h][i][,]_ [ occurs]
on the same inputs for which _si_ ( _hi_ ) is large. To formalize
this idea, we maximize the ”absolute” Pearson correlation
between ∆ _si_ ( _hi_ ) and _si_ ( _hi_ ), as we do not care about the
sign or overall scale at this stage. The following theorem
provides the solution.


**Theorem** **3.2** (Input-space direction matching semantic
alignment variation) **.** _Fix_ _a_ _component_ _Wi_ _and_ _set_ _ui_ =
_v_ ˆ _i._ _Assume_ _Wi_ _[⊤][v][i]_ [=] [0] _[and]_ [Var(] _[s][i]_ [(] _[h][i]_ [))] _[>]_ [0] _[,]_ _[where]_
_si_ ( _hi_ ) := _vi_ _[⊤][W][i][h][i][.]_ _[Consider choosing an input-direction]_
_ki_ = 0 _so_ _that_ _the_ _induced_ _semantic_ _alignment_ _shift_
∆ _si_ ( _hi_ ) := _vi_ _[⊤]_ [∆] _[W][i][h][i][ exhibits maximal co-variation with]_
_the component’s intrinsic semantic alignment score si_ ( _hi_ ) _._
_Formally, consider the objective_



max
_ki_ =0




     -     - [�]
Pearson ∆ _si_ ( _hi_ ) _,_ _si_ ( _hi_ ) _._
��� ��



_Then there exists a maximizer ki that is collinear with Wi_ _[⊤][v][i][,]_
_i.e.,_
_ki_ _∈_ span _{Wi_ _[⊤][v][i][}][.]_


We defer the proof to Appendix A.2. Theorem 3.2 shows
that the input-space direction _ki_ should align with the component’s intrinsic input sensitivity _Wi_ _[⊤][v][i]_ [.] [We] [therefore]
adopt the normalized choice

_k_ ˆ _i_ := _∥WWi_ _[⊤]_ _i_ _[⊤][v][v][i][i][∥]_ [2] _._

This choice is further empirically validated in Appendix E.


**3.4. Step 3:** **Solving for the Edit Magnitudes** _**λ**_


With the edit directions _ui_ and _ki_ fixed, we now determine
the magnitudes _{λi}_, which control how strongly each component is reinforced or suppressed. Intuitively, the magnitude assigned to each component should reflect how that
component contributes to the direction _vi on average across_
_inputs_ : components that consistently align with _vi_ should be
reinforced, components that consistently oppose it should
be suppressed, and components with weak alignment should
receive little or no edit.


Note that this role is fundamentally different from that of
the input-space direction _ki_, which captures how the component’s semantic alignment score _si_ ( _hi_ ) _varies across inputs_,
whereas the magnitudes _λi_ depend only on the component’s
_overall, input-averaged_ semantic alignment.



4


**Steer2Edit:** **From Activation Steering to Component-Level Editing**



To formalize this allocation of editing strength, we now
introduce an importance weighting for each component and
derive _λi_ via a global regularized optimization.


**Importance** **weighting.** Recall that the _semantic_ _align-_
_ment_ _score_ _si_ ( _hi_ ) := _vi_ _[⊤][W][i][h][i]_ [measures] [how] [strongly]
component _Wi_ contributes to the semantic direction _vi_
for a given input _hi_ . Since the magnitudes _λi_ are intended to capture a component’s _overall_ semantic contribution, we measure this contribution by the expectation of
the semantic alignment score over the input distribution:
E[ _si_ ( _hi_ )] = E[ _vi_ _[⊤][W][i][h][i]_ []][.] [However, the typical output mag-]
nitude of _Wihi_ can vary substantially across layers, making
raw values not directly comparable between components.
To place components on a common footing, we make the
following changes: (i) remove the arbitrary scale of the
semantic direction by using ˆ _vi_ = _vi/∥vi∥_ 2, and (ii) normalize by the output norm of the mean activation _µi_ = E[ _hi_ ],
yielding

E[ _si_ ( _hi_ )] _vi_ _[⊤][W][i][µ][i]_
_gi_ = _∥vi∥_ 2 _∥Wiµi∥_ 2 = _∥vi∥_ 2 _∥Wiµi∥_ 2 = cos( _vi, Wiµi_ ) _,_


which we refer to as the _component importance score_ . The
sign of _gi_ indicates whether the component aligns or opposes
the semantic direction, while _|gi|_ measures the strength of
this tendency. This normalization choice is empirically
validated in Appendix E.


**Elastic-Net objective.** The component importance score
_gi_ indicates whether component _Wi_ should be reinforced or
suppressed, and with what strength. A natural objective is
therefore to maximize total alignment _**g**_ _[⊤]_ _**λ**_ = [�] _i_ _[n]_ =1 _[g][i][λ][i][.]_
However, this objective is unbounded, and effective weight
editing should remain lightweight by modifying only a small
number of relevant components while keeping edit magnitudes controlled.


We address both considerations with an Elastic-Net regularization, combining an _ℓ_ 1 term to promote sparsity and an _ℓ_ 2
term to limit overall edit size:



_the sparsity and overall strength of the edit._ _Formally, let_
_**g**_ = ( _g_ 1 _, . . ., gn_ ) _and consider_




    _**λ**_ max _∈_ R _[n]_ _**[g]**_ _[⊤]_ _**[λ]**_ _[−][ρ]_ _α∥_ _**λ**_ _∥_ 1 + [1] _[ −]_ 2 _[α]_ _∥_ _**λ**_ _∥_ [2] 2




_, ρ >_ 0 _,_ _α ∈_ [0 _,_ 1) _._



_The unique edit magnitude assigned to component i is_

[0)]
_λ_ _[∗]_ _i_ [= sign(] _[g][i]_ [) ][max(] _[|][g][i][| −]_ _[ρα,]_ _._

_ρ_ (1 _−_ _α_ )


We defer the proof to Appendix A.3. Theorem 3.3 yields a
closed-form soft-thresholding rule for allocating edit magnitudes _λi_ according to the alignment scores _gi_ under a global
Elastic-Net budget. Substituting _λ_ _[∗]_ _i_ [, together with] _[ u][i]_ [=] _[v]_ [ˆ] _[i]_
and _ki_ = _k_ [ˆ] _i_, gives the unified weight-editing update below.


**3.5. Summary:** **Unified Weight Editing Rule**


Each editable component _Wi_ receives the rank-1 update


[0)]
∆ _Wi_ = sign( _gi_ ) [max(] _[|][g][i][| −]_ _[ρα,]_ _v_ ˆ _i_ _k_ [ˆ] _i_ _[⊤][,]_

_ρ_ (1 _−_ _α_ )




    max _**g**_ _[⊤]_ _**λ**_ _−_ _ρ_ _α∥_ _**λ**_ _∥_ 1 + [1] _[ −]_ _[α]_ _∥_ _**λ**_ _∥_ [2] 2
_**λ**_ 2




_,_



where _ρ >_ 0 controls the global edit budget and _α ∈_ [0 _,_ 1)
trades off _ℓ_ 1 sparsity and _ℓ_ 2 smoothness. Ablation results
in Appendix E confirm the importance of both the _ℓ_ 1 and _ℓ_ 2
regularization terms.


**Theorem 3.3** (Edit magnitude allocation under regularization) **.** _For each component Wi, let gi_ = cos( _vi, Wiµi_ ) _de-_
_note the component importance score, with the convention_
_that gi_ := 0 _if Wiµi_ = 0 _._


_Consider_ _the_ _problem_ _of_ _assigning_ _edit_ _magnitudes_ _{λi}_
_to_ _maximize_ _total_ _signed_ _alignment_ _as_ _measured_ _by_ _the_
_component importance scores {gi}, while controlling both_



where

_v_ ˆ _i_ := _∥vvii∥_ 2 _,_ _k_ ˆ _i_ = _∥WWi_ _[⊤]_ _i_ _[⊤][v][v][i][i][∥]_ [2] _,_ _gi_ = cos( _vi,_ _Wiµi_ ) _._


Each update is:


 - **Directionally selective:** it modifies only the projection
along the semantic direction _vi_ ;

 - **Input-selective:** it determines which inputs should trigger the edit based on the component’s intrinsic semantic
behavior;

 - **Budget-aware:** its magnitude _λ_ _[∗]_ _i_ [is determined by the]
component importance score _gi_ under an Elastic-Net
regularizer.


Thus, **STEER2EDIT** yields a component-level weight editing framework that jointly captures _what_ semantic direction
to modify, _when_ the edit should be activated by the input,
and _how strongly_ each component should be adjusted.


**4. Experiments**


This section evaluates whether **STEER2EDIT** achieves a
superior _attribute–utility trade-off_ compared to inferencetime activation steering. We consider three representative
behavioral control settings: (i) safety alignment against
jailbreak attacks, (ii) truthfulness promotion, and (iii) reasoning efficiency control. Across all settings, we compare
**STEER2EDIT** against the standard activation-steering baseline and report trade-offs between the target attribute and
downstream utility.


**4.1. Implementation of Steer2Edit and Baseline**


We describe how the activation-steering and **STEER2EDIT**
are instantiated, and how editing hyperparameters are selected.



5


**Steer2Edit:** **From Activation Steering to Component-Level Editing**



**Activation Steering (Baseline).** Given a layer-wise steering vector _vℓ_, the hidden representation is modified as
_hℓ_ _←_ _hℓ_ + _γvℓ_, where _γ_ _≥_ 0 denotes the steering strength.
We extract steering vectors separately for attention and MLP
blocks at each layer, _{vℓ_ [attn] _, vℓ_ [mlp] _}_ _[L]_ _ℓ_ =1 [,] [and] [add] [the] [vector]
after each block during inference. We sweep _γ_ to trace
attribute–utility trade-off curves. Task-specific steering vector construction is deferred to Appendix B.


**Steer2Edit.** Following Section 3, we apply rank-1 edits to linear components that write directly into the residual stream. For attention, we edit each head’s output projection _Wo_ _∈_ R _[d]_ [model] _[×][d]_ [head] . For MLPs, we edit individual
down-projection neurons by treating each column _w_ down _,j_
of _W_ down _∈_ R _[d]_ [model] _[×][d]_ [ff] as an independent component.


Edit magnitudes are determined by an Elastic-Net objective
with sparsity parameter _α_ and global budgets _ρ_ attn and _ρ_ mlp
for attention heads and MLP neurons, respectively. For each
model and behavior setting, hyperparameters ( _ρ_ attn _, ρ_ mlp _, α_ )
are selected via a small grid search on a held-out validation set, ranking configurations by the target attribute metric. Unless otherwise noted, results correspond to the bestperforming or top-ranked configurations. Full search details
are provided in Appendix C.


**4.2. Evaluation for Behavioral Control**


We consider three evaluation settings that examine behavioral control along distinct dimensions: safety alignment,
truthfulness, and reasoning efficiency. In each setting, the
_target_ _attribute_ is measured using task-specific metrics,
while _downstream utility_ is evaluated on task-oriented benchmarks that are unrelated to the controlled behavior.


For each use case, we visualize the trade-off between the
target attribute and downstream utility. A method achieves
a superior trade-off if it improves the target attribute while
maintaining higher utility. Our experiments are designed to
test whether **STEER2EDIT** can consistently achieve such
favorable trade-offs relative to activation steering.


4.2.1. SAFETY ALIGNMENT AGAINST JAILBREAK
ATTACKS


**Goal.** We evaluate whether **STEER2EDIT** can strengthen
refusal behavior under strong jailbreak attacks while preserving helpfulness on benign tasks.


**Models and evaluation.** We evaluate safety alignment on
**LLaMA-2-7B-Chat** and **Mistral-7B-Instruct-v0.2** . Safety
is measured using **ADVBench**, which consists of harmful
user queries designed to elicit unsafe behavior. Each query is
transformed into a jailbreak prompt using either **GCG** (Zou
et al., 2023b), a classical gradient-based attack, or **ADV-**
**LLM** (Sun et al., 2025a), a substantially stronger attack that



_Figure 3._ Signed **STEER2EDIT** edit coefficients _λ_ for safety alignment. Positive (red) coefficients reinforce safety-aligned components, while negative (blue) coefficients suppress safety-opposing
ones. Edits are highly sparse and concentrated in a small subset of
attention heads, predominantly in later layers.


trains an LLM to generate adversarial suffixes. We report the
**refusal rate**, defined as the proportion of model responses
that are refusals, averaged across both attack types.


Downstream utility is evaluated on **GSM8K**, **CodeMMLU**,
and **CommonsenseQA**, measuring utility on grade-school
math reasoning, programming, and commonsense multiplechoice questions. Utility is reported as the mean accuracy
across all three benchmarks.


**Results.** Figure 2 illustrates the safety–utility relationship.
Each star corresponds to one of the top-10 most safetyaligned **STEER2EDIT** configurations. While steeringvector baselines trace a clear safety–utility trade-off as intervention strength increases, **STEER2EDIT** identifies configurations that lie beyond this trade-off frontier, occupying
the top-right region of the plot and achieving higher refusal
rates without sacrificing downstream utility.


**Component-level analysis.** Because **STEER2EDIT** applies edits at the level of individual components, the resulting weight updates are directly interpretable and reveal
which components mediate the target behavior.



90


80


70


60


50



Safety Alignment - Utility Trade-off

LLaMA-2-7B-Chat Mistral-7B-Instruct-v0.2


80


70


60


50


40



20 25 30 35
Average Utility (Accuracy)



20 30 40 50
Average Utility (Accuracy)



_Figure_ _2._ Safety–utility trade-off on **LLaMA-2-7B-Chat** and
**Mistral-7B-Instruct-v0.2** . Each point corresponds to a different
intervention strength. **STEER2EDIT** consistently attains higher
refusal rates at comparable or higher utility, while strong steeringvector interventions incur substantial utility degradation.



6


**Steer2Edit:** **From Activation Steering to Component-Level Editing**



Figure 3 shows the signed edit coefficients _λ_ for the bestperforming safety-aligned configuration. Each cell corresponds to the strength of a rank-1 update applied to a specific
component: positive values reinforce components aligned
with refusal behavior, while negative values suppress components that oppose safety.


Across both models, non-zero _λ_ values are highly sparse and
concentrated in a small number of attention heads, predominantly in later layers. MLP neurons receive near-zero coefficients with only a few isolated exceptions. These results
indicate that effective safety control is achieved through
selective amplification and suppression of a small set of
attention heads.


4.2.2. TRUTHFULNESS PROMOTION


**Goal.** We evaluate whether **STEER2EDIT** increases the
model’s preference for truthful answers while preserving
performance on unrelated downstream tasks.


**Models and evaluation.** We evaluate on **Gemma-2-2B-**
**IT** and **LLaMA-3-8B-Instruct** using **TruthfulQA** . For
each prompt, we measure whether the model assigns higher
probability to the truthful answer than to a plausible but false
alternative, and report truthful preference accuracy. Downstream utility is again measured on GSM8K, CodeMMLU,
and CommonsenseQA.


**Results.** Figure 4 shows the truthfulness–utility relationship. While activation steering traces a clear trade-off
in which stronger interventions rapidly degrade utility,
**STEER2EDIT** achieves substantial truthfulness gains without incurring much utility loss.


**Component-level analysis.** Figure 5 visualizes the edit
coefficients _λ_ of the best-performing truthfulness-aligned
configuration. Across both models, truthfulness control
is sparse and predominantly mediated by attention heads,
with non-zero edits concentrated in a limited number of
layers. In contrast to safety alignment, truthfulness edits are distributed across both early and late layers. Notably, in **Gemma-2-2B-IT**, edits are dominated by negative coefficients, suggesting that truthfulness gains arise
primarily from suppressing hallucination-promoting components rather than reinforcing truth-aligned ones. Overall,
these patterns indicate that truthfulness can rely on markedly
different internal circuits across models, while remaining
amenable to selective, component-level intervention.


4.2.3. EFFICIENT REASONING


**Goal.** We evaluate whether **STEER2EDIT** can shorten reasoning traces while preserving answer accuracy, improving
inference efficiency for Large Reasoning Models (LRMs).



_Figure 5._ Signed **STEER2EDIT** edit coefficients _λ_ for truthfulness
promotion. Positive values reinforce truthfulness-aligned components, while negative values suppress components associated with
hallucinated behavior.


**Models** **and** **datasets.** We evaluate on **Qwen3-4B-**
**Thinking-2507** and **OpenMath-Nemotron-7B** using
GSM8K, MATH-500, GPQA, and CodeMMLU. Downstream utility is measured as mean accuracy across all
datasets, while reasoning efficiency is measured by the number of generated reasoning tokens.


**Results.** Figure 6 shows the accuracy–efficiency relationship. Across both models, activation steering reduces reasoning length only at the cost of substantial accuracy degradation. In contrast, **STEER2EDIT** significantly shortens
reasoning traces while maintaining comparable accuracy.


**Component-level analysis.** Figure 7 visualizes the edit
coefficients _λ_ for the best-performing efficiency-oriented
configuration and reveals a qualitatively different pattern
from safety and truthfulness. Reasoning efficiency is predominantly mediated by MLP components, with dense, distributed edits spanning many neurons, while attention heads
play a comparatively minor role. The most effective configurations correspond to larger _ρ_ mlp and smaller _α_, indicating
that reducing reasoning length requires coordinated, distributed modifications to internal computation rather than
sparse interventions on a small set of components. Together,
these results suggest that reasoning efficiency is governed



58

57

56

55

54

53

52

51



20 40
Average Utility (Accuracy)



Truthfulness Alignment - Utility Trade-off

Gemma-2-2B-IT LLaMA-3-8B-Instruct


52


50


48


46


44


42



40 50 60
Average Utility (Accuracy)



40



_Figure 4._ Truthfulness–utility trade-off on **Gemma-2-2B-IT** and
**LLaMA-3-8B-Instruct** . **STEER2EDIT** improves truthfulness at a
higher downstream utility than activation steering.



7


**Steer2Edit:** **From Activation Steering to Component-Level Editing**



Reasoning Efficiency - Accuracy Trade-off

Qwen3-4B-Thinking-2507 OpenMath-Nemotron-7B



Qwen3-4B-Thinking-2507



3600

3800

4000

4200

4400

4600

4800

5000



3000


3500


4000


4500


5000


5500



60 70 80 90
Average Accuracy (Higher Better)



40 50 60 70
Average Accuracy (Higher Better)



_Figure 6._ Accuracy–efficiency trade-off on **Qwen3-4B-Thinking-**
**2507** and **OpenMath-Nemotron-7B** . The y-axis measures reasoning length (lower is better). **STEER2EDIT** achieves a more
favorable accuracy–efficiency trade-off than activation steering.



_Figure 7._ Signed **STEER2EDIT** edit coefficients _λ_ for reasoning
efficiency control. Positive values reinforce components associated with shorter reasoning traces, while negative values suppress
components that promote longer chains of thought.


by broad MLP-based computation patterns, in sharp contrast
to the sparse, attention-dominated circuits underlying safety
and truthfulness.


**4.3. Additional Experiments.**


For completeness, we report (i) _per-dataset trade-off curves_,
(ii) _design-choice ablations over_ ( _u, k, λ_ ), (iii) a _component-_
_wise budget sensitivity analysis_ that isolates the effects of
_ρ_ attn and _ρ_ mlp at fixed _α_, and (iv) comparisons with _training-_
_based baselines_ (full fine-tuning and rank-1 LoRA) in Appendix D, Appendix E, Appendix F, and Appendix G. .


**5. Related Works**


**Steering** **and** **controlling** **LLM** **behavior.** A growing
body of work studies behavioral control in LLMs via interventions on internal representations. Representation engineering methods (Zou et al., 2023a; Turner et al., 2023;
Arditi et al., 2024; Yan et al., 2025; Li et al., 2025) extract semantic directions from contrastive examples and
apply inference-time activation interventions to modulate
attributes such as safety or reasoning behavior. These approaches are training-free, but rely on global, inference


time modifications. In parallel, Concept Bottleneck Models
(Sun et al., 2025b; 2024; Bidusa & Markovitch, 2025; Tan
et al., 2023; Ludan et al., 2023) introduce explicit concept
variables and architectural constraints to enable structured,
human-interpretable control. Together, these lines of work
demonstrate that LLM behavior can be influenced through
manipulation of internal representations.


In contrast, **STEER2EDIT** translates steering signals into
_component-level_ edits that operate at the level of individual
components. By redistributing behavioral influence across
attention heads and MLP neurons, **STEER2EDIT** enables
more favorable attribute–utility trade-offs, while providing fine-grained interpretability and preserving the standard
model architecture.


**LLM** **weight** **editing.** Another line of work focuses on
modifying model parameters to induce persistent behavioral
changes without full retraining. Representative approaches
include meta-editors such as MEND (Mitchell et al., 2021)
and KnowledgeEditor (De Cao et al., 2021), mechanistic editors such as ROME (Meng et al., 2022) and MEMIT (Meng
et al., 2023), neuron-level interventions (Dai et al., 2022),
and semi-parametric methods such as SERAC (Mitchell
et al., 2022). More recent work applies targeted weight
edits to specific components for behavior control, including
ThinkEdit (Sun et al., 2025c) for mitigating overly short
reasoning traces and DRefA (Chu et al., 2025) for safety.
These methods are largely empirical and do not provide a
unified framework for allocating and justifying edits across
components.


**STEER2EDIT** complements this literature by providing a
general, theoretically grounded, and training-free framework that systematically converts steering directions into
component-wise weight updates.


**6. Conclusion**


We introduced **STEER2EDIT**, a principled framework that
translates steering signals into component-level weight edits
via a closed-form solution. By shifting behavioral control
from inference-time activation intervention to parameter
updates, **STEER2EDIT** achieves more favorable behavior–
utility trade-offs while preserving the standard model architecture. Beyond empirical gains, the method offers finegrained interpretability, revealing how safety, truthfulness,
and reasoning efficiency are distributed across attention
heads and MLP components. These results show that steering vectors can serve as effective diagnostic signals for
systematic weight editing, providing a practical and theoretically grounded alternative to activation-level control.



8


**Steer2Edit:** **From Activation Steering to Component-Level Editing**



**Broader Impact**


This paper presents work whose goal is to advance the field
of machine learning by enabling efficient, interpretable, and
training-free model editing at the level of individual components. In positive applications, STEER2EDIT may help
practitioners correct or reduce undesirable behaviors (e.g.,
unsafe responses or hallucinations) and better understand
which internal components support a given behavior, which
can improve transparency and facilitate auditing. At the
same time, weight-editing methods are inherently dual-use:
the same capability can be applied to remove safeguards,
amplify biases, or otherwise manipulate model behavior for
harmful purposes, and edited models may be redistributed
without clear provenance. To mitigate these risks, we emphasize that edits should be evaluated across diverse safety and
capability tests, that releases should include clear documentation of intended use and limitations, and that responsible
access controls may be appropriate for edits that materially
alter safety-critical behaviors. Overall, we believe the primary societal consequence of this work is enabling more
controllable and inspectable models, with corresponding
responsibility to prevent and detect misuse.


**References**


Arditi, A., Obeso, O., Syed, A., Paleka, D., Panickssery, N.,
Gurnee, W., and Nanda, N. Refusal in language models
is mediated by a single direction. _NeurIPS_, 2024.


Bidusa, O. R. and Markovitch, S. Concept layers: Enhancing interpretability and intervenability via llm conceptualization. _arXiv preprint arXiv:2502.13632_, 2025.


Chen, M. Evaluating large language models trained on code.
_arXiv preprint arXiv:2107.03374_, 2021.


Chu, K. L., Sun, C.-E., and Weng, T.-W. How to make
llms safer? detecting and editing key heads in llms. In
_NeurIPS Lock-LLM Workshop_, 2025.


Dai, D., Dong, L., Hao, Y., Sui, Z., Chang, B., and Wei, F.
Knowledge neurons in pretrained transformers. In _ACL_,
2022.


De Cao, N., Aziz, W., and Titov, I. Editing factual knowledge in language models. _arXiv_ _preprint_
_arXiv:2104.08164_, 2021.


Guo, D., Yang, D., Zhang, H., Song, J., Zhang, R., Xu, R.,
Zhu, Q., Ma, S., Wang, P., Bi, X., et al. Deepseek-r1: Incentivizing reasoning capability in llms via reinforcement
learning. _arXiv preprint arXiv:2501.12948_, 2025.


Li, Y., Sun, C.-E., and Weng, T.-W. Effective skill unlearning through intervention and abstention. _NAACL_, 2025.



Ludan, J. M., Lyu, Q., Yang, Y., Dugan, L., Yatskar, M.,
and Callison-Burch, C. Interpretable-by-design text classification with iteratively generated concept bottleneck.
_arXiv preprint_, 2023.


Meng, K., Bau, D., Andonian, A., and Belinkov, Y. Locating
and editing factual associations in gpt. _NeurIPS_, 2022.


Meng, K., Sharma, A. S., Andonian, A., Belinkov, Y., and
Bau, D. Mass-editing memory in a transformer. _ICLR_,
2023.


Mitchell, E., Lin, C., Bosselut, A., Finn, C., and Manning, C. D. Fast model editing at scale. _arXiv preprint_
_arXiv:2110.11309_, 2021.


Mitchell, E., Lin, C., Bosselut, A., Manning, C. D., and
Finn, C. Memory-based model editing at scale. In _ICML_,
2022.


Olsson, C., Elhage, N., Nanda, N., Joseph, N., DasSarma,
N., Henighan, T., Mann, B., Askell, A., Bai, Y., Chen,
A., et al. In-context learning and induction heads. _arXiv_
_preprint arXiv:2209.11895_, 2022.


Sun, C.-E., Oikarinen, T., and Weng, T.-W. Crafting large
language models for enhanced interpretability. In _ICML_
_2024 Workshop on Mechanistic Interpretability_, 2024.


Sun, C.-E., Liu, X., Yang, W., Weng, T.-W., Cheng, H., San,
A., Galley, M., and Gao, J. Iterative self-tuning llms for
enhanced jailbreaking capabilities. In _NAACL_, 2025a.


Sun, C.-E., Oikarinen, T., Ustun, B., and Weng, T.-W. Concept bottleneck large language models. In _ICLR_, 2025b.


Sun, C.-E., Yan, G., and Weng, T.-W. Thinkedit: Interpretable weight editing to mitigate overly short thinking
in reasoning models. _EMNLP_, 2025c.


Tan, Z., Cheng, L., Wang, S., Bo, Y., Li, J., and Liu, H.
Interpreting pretrained language models via concept bottlenecks. _arXiv preprint_, 2023.


Turner, A. M., Thiergart, L., Leech, G., Udell, D., Vazquez,
J. J., Mini, U., and MacDiarmid, M. Steering language models with activation engineering. _arXiv preprint_
_arXiv:2308.10248_, 2023.


Yan, G., Sun, C.-E., et al. Reflctrl: Controlling llm reflection via representation engineering. _arXiv_ _preprint_
_arXiv:2512.13979_, 2025.


Yao, S., Zhao, J., Yu, D., Du, N., Shafran, I., Narasimhan,
K., and Cao, Y. React: Synergizing reasoning and acting
in language models, 2023.


Zhao, Y., Zhang, W., Xie, Y., Goyal, A., Kawaguchi, K.,
and Shieh, M. Understanding and enhancing safety mechanisms of llms via safety-specific neuron. In _ICLR_, 2025.



9


**Steer2Edit:** **From Activation Steering to Component-Level Editing**


Zhou, Z., Yu, H., Zhang, X., Xu, R., Huang, F., Wang, K.,
Liu, Y., Fang, J., and Li, Y. On the role of attention
heads in large language model safety. _arXiv_ _preprint_
_arXiv:2410.13708_, 2024.


Zou, A., Phan, L., Chen, S., Campbell, J., Guo, P., Ren, R.,
Pan, A., Yin, X., Mazeika, M., Dombrowski, A., Goel,
S., Li, N., Byun, M. J., Wang, Z., Mallen, A., Basart, S.,
Koyejo, S., Song, D., Fredrikson, M., Kolter, J. Z., and
Hendrycks, D. Representation engineering: A top-down
approach to AI transparency. _CoRR_, 2023a.


Zou, A., Wang, Z., Carlini, N., Nasr, M., Kolter, J. Z.,
and Fredrikson, M. Universal and transferable adversarial attacks on aligned language models. _arXiv preprint_
_arXiv:2307.15043_, 2023b.


10


**Steer2Edit:** **From Activation Steering to Component-Level Editing**

### **Table of Contents**


**A** **Proofs for STEER2EDIT** **11**


A.1 Proof of Theorem 3.1 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 11


A.2 Proof of Theorem 3.2 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 12


A.3 Proof of Theorem 3.3 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 13


**B** **Steering Vector Construction** **15**


**C** **Hyperparameter Search Procedure** **16**


**D** **Per-Dataset Trade-off Analysis** **17**


D.1 Safety Alignment: Attack- and Dataset-Specific Trade-offs . . . . . . . . . . . . . . . . . . . . . . . . . 17


D.2 Truthfulness: Dataset-Specific Utility Trade-offs . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 17


D.3 Efficient Reasoning: Dataset-Level Accuracy–Length Trade-offs . . . . . . . . . . . . . . . . . . . . . . 17


**E** **Ablation Study of STEER2EDIT:** **Empirical Justification of Formal Design Choices** **20**


E.1 Unified Performance Summary . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 20


E.2 Detailed Per-Setting Results . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 21


**F** **Component-Wise Budget Sensitivity Analysis** **23**


F.1 Safety Alignment: Sensitivity to Attention Budget . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 23


F.2 Truthfulness: Sensitivity Dominated by Attention . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 23


F.3 Efficient Reasoning: Sensitivity Dominated by MLP Budget . . . . . . . . . . . . . . . . . . . . . . . . 24


**G** **Additional Baselines:** **Comparing STEER2EDIT with Training-Based Methods** **25**


G.1 Safety Alignment . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 25


G.2 Truthfulness . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 25


G.3 Efficient Reasoning . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 26


**A. Proofs for STEER2EDIT**


**A.1. Proof of Theorem 3.1**


**Theorem A.1** (Output-space direction under semantic invariance) **.** _Let vi_ = 0 _, and let_ ∆ _Wi_ = _λi uiki_ _[⊤]_ _[be a rank-1 edit]_
_with_ ∆ _Wi_ = 0 _._ _If for all hi_ _and all z_ _⊥_ _vi_ _we have_


_z_ _[⊤]_ ∆ _Wihi_ = 0 _,_


_then the output-space direction ui_ _must be collinear with vi, i.e.,_


_ui_ _∈_ span _{vi}._


_Proof._ Substituting ∆ _Wi_ = _λi uiki_ _[⊤]_ [,]
_z_ _[⊤]_ ∆ _Wihi_ = _λi_ ( _z_ _[⊤]_ _ui_ ) ( _ki_ _[⊤][h][i]_ [)] _[.]_

Because ∆ _Wi_ = 0, we have _ki_ = 0, and therefore there exists some _hi_ such that _ki_ _[⊤][h][i]_ [= 0][.] [For the expression above to]
vanish for all such _hi_, we must have _z_ _[⊤]_ _ui_ = 0 for every vector _z_ orthogonal to _vi_ . The only vectors satisfying this condition
are those proportional to _vi_ . Hence _ui_ _∈_ span _{vi}_ .


11


**Steer2Edit:** **From Activation Steering to Component-Level Editing**


**A.2. Proof of Theorem 3.2**


**Theorem A.2** (Input-space direction matching semantic alignment variation) **.** _Fix a component Wi and set ui_ = _v_ ˆ _i._ _Assume_
_Wi_ _[⊤][v][i]_ [=] [0] _[and]_ [Var(] _[s][i]_ [(] _[h][i]_ [))] _[>]_ [0] _[,]_ _[where]_ _[s][i]_ [(] _[h][i]_ [)] [:=] _[v]_ _i_ _[⊤][W][i][h][i][.]_ _[Consider]_ _[choosing]_ _[an]_ _[input-direction]_ _[k][i]_ [=] [0] _[so]_ _[that]_ _[the]_
_induced_ _semantic_ _alignment_ _shift_ ∆ _si_ ( _hi_ ) := _vi_ _[⊤]_ [∆] _[W][i][h][i]_ _[exhibits]_ _[maximal]_ _[co-variation]_ _[with]_ _[the]_ _[component’s]_ _[intrinsic]_
_semantic alignment score si_ ( _hi_ ) _._ _Formally, consider the objective_



max
_ki_ =0




     -     - [�]
Pearson ∆ _si_ ( _hi_ ) _,_ _si_ ( _hi_ ) _._
��� ��



_Then there exists a maximizer ki_ _that is collinear with Wi_ _[⊤][v][i][, i.e.,]_

_ki_ _∈_ span _{Wi_ _[⊤][v][i][}][.]_


_Proof._ Recall that _si_ ( _hi_ ) := _vi_ _[⊤][W][i][h][i]_ [and][ ∆] _[s][i]_ [(] _[h][i]_ [) :=] _[ v]_ _i_ _[⊤]_ [∆] _[W][i][h][i][.]_ [ Using][ ∆] _[W][i]_ [=] _[ λ][i][v]_ [ˆ] _[i][k]_ _i_ _[⊤]_ [, we have]

∆ _si_ ( _hi_ ) = _λi∥vi∥_ 2 ( _ki_ _[⊤][h][i]_ [)] _[.]_


Pearson correlation is invariant to additive shifts in either argument, so it is unchanged if we center the inputs. Let
_h_ ˜ _i_ = _hi −_ _µi_ with _µi_ = E[ _hi_ ], and define

∆� _si_ ( _hi_ ) := ∆ _si_ ( _h_ [˜] _i_ ) _,_ _s_ ˜ _i_ ( _hi_ ) := _si_ ( _h_ [˜] _i_ ) _._


Denote the covariance matrix by
Σ _i_ := E[ _h_ [˜] _ih_ [˜] _[⊤]_ _i_ []] _[.]_


**Step 1:** **covariance.** We have

∆� _si_ ( _hi_ ) = _λi∥vi∥_ 2 ( _ki_ _[⊤][h]_ [˜] _[i]_ [)] _[,]_ _s_ ˜ _i_ ( _hi_ ) = _vi_ _[⊤][W][i][h]_ [˜] _[i][.]_


Hence


Cov(∆ [�] _si,_ ˜ _si_ ) = E[∆ [�] _si_ ( _hi_ ) ˜ _si_ ( _hi_ )]

= _λi∥vi∥_ 2 E[( _ki_ _[⊤][h]_ [˜] _[i]_ [)(] _[v]_ _i_ _[⊤][W][i][h]_ [˜] _[i]_ [)]]

= _λi∥vi∥_ 2 _ki_ _[⊤]_ [E][[˜] _[h][i][h]_ [˜] _[⊤]_ _i_ []] _[ W]_ _i_ _[ ⊤][v][i]_

= _λi∥vi∥_ 2 _ki_ _[⊤]_ [Σ] _[i][W][ ⊤]_ _i_ _[v][i][.]_


**Step 2:** **variances.** Similarly,
Var(∆ [�] _si_ ) = E[∆ [�] _si_ ( _hi_ ) [2] ] = _λ_ [2] _i_ _[∥][v][i][∥]_ 2 [2] _[k]_ _i_ _[⊤]_ [Σ] _[i][k][i][,]_

and
Var(˜ _si_ ) = E[˜ _si_ ( _hi_ ) [2] ] = _vi_ _[⊤][W][i]_ [Σ] _[i][W][ ⊤]_ _i_ _[v][i][.]_


**Step 3:** **Pearson correlation.** The Pearson correlation between the induced and intrinsic semantic signals is

Pearson(∆ [�] _si,_ ˜ _si_ ) =                - Cov(∆ [�] _si,_ ˜ _si_ ) _._
Var(∆ [�] _si_ ) �Var(˜ _si_ )


Substituting the expressions above gives

_λi∥vi∥_ 2 _ki_ _[⊤]_ [Σ] _[i][W][ ⊤]_ _i_ _[v][i]_
Pearson(∆ [�] _si,_ ˜ _si_ ) =             -             _λ_ [2] _i_ _[∥][v][i][∥]_ 2 [2] _[k]_ _i_ _[⊤]_ [Σ] _[i][k][i]_ _vi_ _[⊤][W][i]_ [Σ] _[i][W][ ⊤]_ _i_ _[v][i]_

sign( _λi_ ) _ki_ _[⊤]_ [Σ] _[i][W][ ⊤]_ _i_ _[v][i]_
= _._

           - _ki_ _[⊤]_ [Σ] _[i][k][i]_ ~~�~~ _vi_ _[⊤][W][i]_ [Σ] _[i][W][ ⊤]_ _i_ _[v][i]_


The denominator’s second factor is independent of _ki_, and sign( _λi_ ) is irrelevant when maximizing absolute correlation.
Thus maximizing _|_ Pearson(∆ [�] _si,_ ˜ _si_ ) _|_ over _ki_ = 0 reduces to maximizing

_|ki_ _[⊤]_ [Σ] _[i][W][ ⊤]_ _i_ _[v][i][|]_
_._ (1)

           - _ki_ _[⊤]_ [Σ] _[i][k][i]_


12


**Steer2Edit:** **From Activation Steering to Component-Level Editing**


**Step 4:** **Cauchy–Schwarz in the** Σ _i_ **-inner product.** Define the Σ _i_ -inner product:


_⟨a, b⟩_ Σ _i_ := _a_ _[⊤]_ Σ _ib,_ _∥a∥_ Σ _i_ :=                      - _a_ _[⊤]_ Σ _ia._


Then (1) becomes
_|⟨ki, Wi_ _[⊤][v][i][⟩]_ [Σ] _i_ _[|]_
_._
_∥ki∥_ Σ _i_


By Cauchy–Schwarz,
_|⟨ki, Wi_ _[⊤][v][i][⟩]_ [Σ] _i_ _[| ≤∥][k][i][∥]_ [Σ] _i_ _[∥][W][ ⊤]_ _i_ _[v][i][∥]_ [Σ] _i_ _[.]_

Equality is attained by choosing _ki_ _∝_ _Wi_ _[⊤][v][i]_ [.] [Therefore, there exists an optimizer] _[ k][i]_ _[∈]_ [span] _[{][W]_ _i_ _[ ⊤][v][i][}]_ [.]


**A.3. Proof of Theorem 3.3**


**Theorem A.3** (Edit magnitude allocation under regularization) **.** _For each component Wi, let gi_ = cos( _vi, Wiµi_ ) _denote the_
_component importance score, with the convention that gi_ := 0 _if Wiµi_ = 0 _._


_Consider the problem of assigning edit magnitudes {λi} to maximize total signed alignment as measured by the component_
_importance scores {gi}, while controlling both the sparsity and overall strength of the edit._ _Formally, let_ _**g**_ = ( _g_ 1 _, . . ., gn_ )
_and consider_




    _**λ**_ max _∈_ R _[n]_ _**[g]**_ _[⊤]_ _**[λ]**_ _[ −]_ _[ρ]_ _α∥_ _**λ**_ _∥_ 1 + [1] _[ −]_ 2 _[α]_



2 _∥_ _**λ**_ _∥_ [2] 2




_, ρ >_ 0 _,_ _α ∈_ [0 _,_ 1) _._



_The unique edit magnitude assigned to component i is_


[0)]
_λ_ _[∗]_ _i_ [= sign(] _[g][i]_ [) ][max(] _[|][g][i][| −]_ _[ρα,]_ _._

_ρ_ (1 _−_ _α_ )


_Proof._ For component _i_, define the one-dimensional objective




     _J_ ( _λi_ ) = _giλi −_ _ρ_ _α|λi|_ + [1] _[ −]_ 2 _[α]_ _λ_ [2] _i_




     _J_ ( _λi_ ) = _giλi −_ _ρ_ _α|λi|_ + [1] _[ −]_ _[α]_




_._



A scalar value _λ_ _[∗]_ _i_ [maximizes] _[ J]_ [iff]
0 _∈_ _∂J_ ( _λ_ _[∗]_ _i_ [)] _[,]_


where the subgradient is needed only at _λi_ = 0 due to the nondifferentiability of _|λi|_ . We analyze the three regions _λi_ _>_ 0,
_λi_ _<_ 0, and _λi_ = 0.


**Case 1:** _λi_ _>_ 0 **.** Here _|λi|_ = _λi_, so




     _J_ ( _λi_ ) = _giλi −_ _ρ_ _αλi_ + [1] _[ −]_ 2 _[α]_ _λ_ [2] _i_




_._



Differentiating gives
_dJ_
= _gi −_ _ρα −_ _ρ_ (1 _−_ _α_ ) _λi._
_dλi_



Setting this to zero yields



_λi_ = _[g][i][ −]_ _[ρα]_

_ρ_ (1 _−_ _α_ ) _[,]_



which is valid only when the positivity assumption holds, i.e. _gi_ _> ρα_ .


**Case 2:** _λi_ _<_ 0 **.** Here _|λi|_ = _−λi_, so


_J_ ( _λi_ ) = _giλi_ + _ραλi −_ _[ρ]_ [(1] _[ −]_ _[α]_ [)] _λ_ [2] _i_ _[.]_

2


Differentiating,
_dJ_
= _gi_ + _ρα −_ _ρ_ (1 _−_ _α_ ) _λi._
_dλi_


13


**Steer2Edit:** **From Activation Steering to Component-Level Editing**



Setting this to zero gives


which is valid only when _gi_ _< −ρα_ .



_λi_ = _[g][i]_ [ +] _[ ρα]_

_ρ_ (1 _−_ _α_ ) _[,]_



**Case 3:** _λi_ = 0 **.** At zero, the subdifferential of _|λi|_ is _∂|λi|_ = [ _−_ 1 _,_ 1]. The optimality condition


0 _∈_ _gi −_ _ρα s,_ _s ∈_ [ _−_ 1 _,_ 1] _,_


is feasible iff _|gi| ≤_ _ρα_ . Thus _λ_ _[∗]_ _i_ [= 0][ whenever the alignment is too small to exceed the threshold.]


Combining all three cases gives the soft-threshold rule



_gi −_ _ρα_
_gi_ _> ρα,_
_ρ_ (1 _−_ _α_ ) _[,]_



_λ_ _[∗]_ _i_ [=]








0 _,_ _|gi| ≤_ _ρα,_


_gi_ + _ρα_
_gi_ _< −ρα._
_ρ_ (1 _−_ _α_ ) _[,]_







Equivalently,




[0)]
_λ_ _[∗]_ _i_ [= sign(] _[g][i]_ [) ][max(] _[|][g][i][| −]_ _[ρα,]_ _._

_ρ_ (1 _−_ _α_ )


14


**Steer2Edit:** **From Activation Steering to Component-Level Editing**


**B. Steering Vector Construction**


This appendix describes the procedures used to construct steering vectors for each behavioral control setting. Across all
experiments, steering vectors are computed using the same general mean-difference formulation and are shared verbatim
between activation steering and **STEER2EDIT** . Only the definition of positive and negative response sets differs by task.


**General** **formulation.** For a given model, layer _ℓ_, and block type (attention or MLP), we collect the block output
activations for a set of responses. Let _P_ and _N_ denote the positive and negative response sets associated with a target
behavior. For each response, we average the block outputs over all response tokens. The steering vector is then defined as
the difference between the mean activations:


_vℓ_ = E _x∈P_ [ _hℓ_ ( _x_ )] _−_ E _x∈N_ [ _hℓ_ ( _x_ )] _._


This procedure is applied independently to the attention and MLP blocks at each layer, yielding _{vℓ_ [attn] _, vℓ_ [mlp] _}_ _[L]_ _ℓ_ =1 [.]


**Safety alignment.** For safety alignment, we construct steering vectors using the ADVBench dataset. The positive set _P_
consists of refusal responses to harmful prompts, while the negative set _N_ consists of standard helpful responses to benign
questions sampled from Alpaca dataset. Steering vectors are computed from model-generated responses.


**Truthfulness.** For truthfulness promotion, we use the TruthfulQA dataset. We split the dataset into a probing set and an
evaluation set. Model responses on the probing set are labeled as _truthful_ or _hallucinated_ using **QwQ-32B** as an external
judge. The positive set _P_ consists of truthful responses, and the negative set _N_ consists of hallucinated responses.


**efficient Reasoning.** For reasoning efficiency control, we use the GSM8K training set. We measure the length of each
model-generated reasoning trace and select the top 5% shortest and top 5% longest responses. The positive set _P_ consists
of short reasoning traces, and the negative set _N_ consists of long reasoning traces. The resulting steering vectors capture
directions associated with shorter internal reasoning processes.


All steering vectors are computed once per model and per behavioral control setting. During evaluation, the same steering
vectors are applied across all test sets, reflecting a practical deployment scenario in which vectors are not optimized for any
specific evaluation benchmark.


15


**Steer2Edit:** **From Activation Steering to Component-Level Editing**


**C. Hyperparameter Search Procedure**


**STEER2EDIT** introduces three scalar hyperparameters: the attention editing budget _ρ_ attn, the MLP editing budget _ρ_ mlp, and
the Elastic-Net sparsity parameter _α_ . These parameters control how edit magnitude is allocated across model components
and how sparsely edits are distributed. Hyperparameters are selected using a lightweight two-stage grid search on held-out
data.


**Step 1:** **Coarse grid search**


We first perform a coarse-grained grid search over a shared range that is identical across all models and behavioral control
settings:


_ρ_ attn _∈{_ 0 _._ 1 _,_ 0 _._ 3 _,_ 0 _._ 5 _,_ 0 _._ 7 _,_ 0 _._ 9 _},_ _ρ_ mlp _∈{_ 0 _._ 1 _,_ 0 _._ 3 _,_ 0 _._ 5 _,_ 0 _._ 7 _,_ 0 _._ 9 _},_ _α ∈{_ 0 _._ 1 _,_ 0 _._ 3 _,_ 0 _._ 5 _,_ 0 _._ 7 _,_ 0 _._ 9 _}._


The goal of this step is to identify the approximate operating regime (e.g., attention-dominated versus MLP-dominated edits,
sparse versus distributed allocation), rather than to finely optimize performance.


Each configuration is first subjected to a lightweight sanity check using 20 short, simple prompts. If the edited model
exhibits degenerate behavior (e.g., repetitive output, failure to respond, or nonsensical generations), the configuration is
immediately discarded. This allows unstable settings to be filtered at negligible cost.


**Step 2:** **Refined grid search**


Based on the results of the coarse search, we define a refined but still small grid for each (model, setting) pair. The refined
grids narrow the range and reduce the step size around regions that exhibit meaningful improvements in the target attribute
while preserving normal model behavior.


In several settings, we observe that edits to either attention or MLP components have negligible impact on the target behavior.
In these cases, the corresponding component is not edited at all, and no budget is assigned to that component during the
refined search.


**Final search ranges**


Table 1 summarizes the refined hyperparameter ranges used in each behavioral control setting. All reported results in the
main paper, including the best-performing configuration and the top-10 configurations shown in trade-off plots, are selected
exclusively from these ranges.


**Setting / Model** _**ρ**_ attn _**ρ**_ mlp _**α**_


_Safety Alignment_
LLaMA-2-7B-Chat [0 _._ 16 _,_ 0 _._ 24] (step = 0.02) [0 _._ 35 _,_ 0 _._ 55] (step = 0.05) [0 _._ 70 _,_ 0 _._ 90] (step = 0.05)
Mistral-7B-Instruct-v0.2 [0 _._ 42 _,_ 0 _._ 50] (step = 0.02) [0 _._ 40 _,_ 0 _._ 60] (step = 0.05) [0 _._ 65 _,_ 0 _._ 85] (step = 0.05)


_Truthfulness_
Gemma-2-2B-IT [0 _._ 30 _,_ 0 _._ 50] (step = 0.05) _negligible_ [0 _._ 75 _,_ 0 _._ 95] (step = 0.05)
LLaMA-3-8B-Instruct [0 _._ 10 _,_ 0 _._ 14] (step = 0.01) [0 _._ 30 _,_ 0 _._ 50] (step = 0.05) [0 _._ 30 _,_ 0 _._ 70] (step = 0.10)


_Efficient Reasoning_
Qwen3-4B-Thinking-2507 _negligible_ [0 _._ 65 _,_ 0 _._ 80] (step = 0.05) [0 _._ 05 _,_ 0 _._ 20] (step = 0.05)
OpenMath-Nemotron-7B [0 _._ 20 _,_ 0 _._ 30] (step = 0.05) [0 _._ 80 _,_ 0 _._ 90] (step = 0.05) [0 _._ 10 _,_ 0 _._ 20] (step = 0.05)


_Table 1._ Refined hyperparameter search ranges for **STEER2EDIT** . “Negligible” indicates that edits to the corresponding component were
found to have insufficient effect during coarse search and are therefore not applied in the refined search.


**Efficiency and reporting**


Hyperparameter search for **STEER2EDIT** is computationally lightweight. Each configuration requires only a single closedform application of rank-1 weight edits, followed by evaluation on a held-out small validation set. In practice, the full
two-stage search completes within minutes per model, and does not involve gradient-based optimization. All evaluations are
performed on held-out data that is disjoint from steering vector extraction. No additional tuning is performed on test sets.


16


**Steer2Edit:** **From Activation Steering to Component-Level Editing**


**D. Per-Dataset Trade-off Analysis**


In Section 4.2, we summarize each behavioral control setting using aggregated downstream utility metrics to provide a
concise comparison across methods. In this appendix, we present _per-dataset trade-off curves_ that expose finer-grained
behavior across individual evaluation benchmarks. These results demonstrate that the superior attribute–utility trade-offs
achieved by **STEER2EDIT** are consistent across datasets.


**D.1. Safety Alignment:** **Attack- and Dataset-Specific Trade-offs**


For safety alignment, we evaluate two jailbreak attack methods (GCG and ADV-LLM) and three downstream utility
benchmarks (CommonsenseQA, Code-MMLU, and GSM8K), resulting in six distinct safety–utility trade-off settings per
model.


Figure 8 reports refusal rate versus downstream utility separately for each attack–dataset pair on **LLaMA-2-7B-Chat** and
**Mistral-7B-Instruct-v0.2** . Across most settings, **STEER2EDIT** identifies configurations that achieve higher refusal rates at
comparable or higher utility than inference-time activation steering.


For **LLaMA-2-7B-Chat**, **STEER2EDIT** consistently dominates the steering baseline under both GCG and ADV-LLM
attacks across all downstream datasets. For **Mistral-7B-Instruct-v0.2**, performance depends on the attack strength: under
the weaker GCG attack, **STEER2EDIT** is occasionally slightly worse than activation steering at comparable utility, whereas
under the substantially stronger ADV-LLM attack, **STEER2EDIT** achieves markedly higher refusal rates while preserving
downstream accuracy.


Notably, the advantage of **STEER2EDIT** becomes more pronounced as the attack strength increases. While activation
steering requires aggressive intervention that sharply degrades utility under ADV-LLM, weight-level edits derived by
**STEER2EDIT** maintain stable benign-task performance while substantially improving robustness to strong jailbreaks.


**D.2. Truthfulness:** **Dataset-Specific Utility Trade-offs**


For truthfulness promotion, downstream utility is evaluated independently on CommonsenseQA, Code-MMLU, and GSM8K.
Figure 9 shows truthfulness versus utility accuracy for **Gemma-2-2B-IT** and **LLaMA-3-8B-Instruct** on each benchmark.


Across all datasets, activation steering exhibits a pronounced trade-off in which increasing truthfulness rapidly degrades task
performance. In contrast, **STEER2EDIT** consistently attains higher truthfulness at substantially higher utility, with edited
configurations occupying regions of the trade-off space that is unattainable by steering alone.


These per-dataset results demonstrate that the truthfulness gains of **STEER2EDIT** generalizes across reasoning-heavy and
knowledge-oriented benchmarks.


**D.3. Efficient Reasoning:** **Dataset-Level Accuracy–Length Trade-offs**


For efficient reasoning control, we report dataset-specific trade-offs between answer accuracy and reasoning length on
GSM8K, MATH-500, GPQA, and Code-MMLU for **Qwen3-4B-Thinking-2507** and **OpenMath-Nemotron-7B** .


Figure 10 shows that activation steering reduces reasoning length primarily by sacrificing accuracy, with the severity of this
trade-off varying substantially across datasets. In contrast, **STEER2EDIT** consistently identifies configurations that shorten
reasoning traces while preserving accuracy, including on challenging benchmarks such as GPQA and MATH-500.


Notably, these improvements generalize beyond GSM8K, despite the steering direction being extracted from GSM8K,
indicating that **STEER2EDIT** captures a transferable mechanism for reasoning efficiency control.


17


**Steer2Edit:** **From Activation Steering to Component-Level Editing**


Safety Alignment Utility Trade-off

LLaMA-2-7B-Chat



CommonsenseQA


95


90


85


80


75


70


65
30 35 40 45 50 55


90



GSM8K


95


90


85


80


75


70


65
16 18 20 22 24


90


80


70


60


50


40


30


16 18 20 22 24


GSM8K


90


85


80


75


70


65


60

10 20 30 40


80


70


60


50


40


30


20


10


10 20 30 40
Utility Accuracy



80


70


60


50


40


30


90


85


80


75


70


65


60


80


70


60


50


40


30


20


10



30 35 40 45 50 55


CommonsenseQA


30 40 50 60


30 40 50 60
Utility Accuracy



Code-MMLU


95


90


85


80


75


70


65
15.0 17.5 20.0 22.5 25.0 27.5 30.0


90


80


70


60


50


40


30


15.0 17.5 20.0 22.5 25.0 27.5 30.0


Mistral-7B-Instruct-v0.2


Code-MMLU


90


85


80


75


70


65


60

20 30 40 50


80


70


60


50


40


30


20


10


20 30 40 50
Utility Accuracy



_Figure 8._ Per-dataset safety–utility trade-offs under GCG and ADV-LLM attacks. Each column corresponds to a downstream utility
dataset (CommonsenseQA, Code-MMLU, GSM8K), and each row corresponds to an attack method. **STEER2EDIT** consistently achieves
higher refusal rates at comparable or higher utility than activation steering across all settings.


18


**Steer2Edit:** **From Activation Steering to Component-Level Editing**



Truthfulness Alignment Utility Trade-off



CommonsenseQA


58


57


56


55


54


53


52


51
10 20 30 40 50 60 70


52



58


57


56


55


54


53


52


51
15 20 25 30 35 40

LLaMA-3-8B-Instruct


52


50


48


46


44


42



Gemma-2-2B-IT



Code-MMLU



GSM8K


58


57


56


55


54


53


52


51
10 20 30 40 50


52


50


48


46


44


42



50


48


46


44


42


40



40 45 50 55 60 65 70
Utility Accuracy



20 30 40 50
Utility Accuracy



50 55 60 65 70 75
Utility Accuracy



40



40



_Figure 9._ Per-dataset truthfulness–utility trade-offs on CommonsenseQA, Code-MMLU, and GSM8K for Gemma-2-2B-IT and LLaMA3-8B-Instruct. **STEER2EDIT** improves truthfulness while preserving higher downstream utility across all datasets.


Reasoning Efficiency - Accuracy Trade-off

Qwen3-4B-Thinking-2507



10 15 20 25 30 35
Average Accuracy



Code-MMLU


65 70 75 80 85 90 95



GPQA


30 40 50 60 70



3200

3400

3600

3800

4000

4200

4400

4600

4800



GSM8K


80.0 82.5 85.0 87.5 90.0 92.5


40 50 60 70 80 90
Average Accuracy



3000


4000


5000


6000


3000


3200


3400


3600


3800


4000



MATH-500


50 60 70 80 90 100


60 70 80 90
Average Accuracy



5000


6000


7000


8000


9000


5000

5500

6000

6500

7000

7500

8000

8500

9000



OpenMath-Nemotron-7B


4500


4750


5000


5250


5500


5750


6000



50 60 70 80
Average Accuracy



6250



1000


1100


1200


1300


1400


1500


1400


1600


1800


2000


2200


2400



_Figure 10._ Per-dataset accuracy–reasoning-length trade-offs on GSM8K, MATH-500, GPQA, and Code-MMLU for Qwen3-4B-Thinking2507 and OpenMath-Nemotron-7B. **STEER2EDIT** reduces reasoning length while maintaining accuracy across all datasets.


19


**Steer2Edit:** **From Activation Steering to Component-Level Editing**


**E. Ablation Study of STEER2EDIT:** **Empirical Justification of Formal Design Choices**


In this section, we validate the design choices of **STEER2EDIT** through a systematic ablation study. We decompose the
rank-1 weight update, ∆ _Wi_ = _λiuiki_ _[⊤]_ [, and independently modify its three core components:] [the] **[ Input Direction]** [ (] _[k]_ [), the]
**Importance Score** ( _g_ ), and the **Edit Magnitude** ( _λ_ ), while holding the others constant.


This study aims to determine whether the performance of **STEER2EDIT** arises from its specific geometric and statistical formulations—such as using cosine similarity for scoring or Elastic-Net for sparsity—rather than generic weight modifications.
Table 2 defines the five ablation variants tested and the specific hypothesis each one investigates.


_Table 2._ **Ablation Definitions.** We categorize variants by the component they modify: Input Direction ( _k_ ), Importance Score ( _g_ ), or
Magnitude ( _λ_ ).


**Ablation Category** **Variant** **Definition and Hypothesis Tested**

**Input** _k_ _k_ mean Sets _ki_ _←_ _µi_, where _µi_ = E[ _hi_ ]. Tests if data statistics alone suffice without
directional sensitivity.
_k_ svd Sets _ki_ _←_ **v** 1, where **v** 1 is the top right singular vector of _Wi_ . Tests if intrinsic
weight directions suffice.

**Score** _g_ _g_ dot Sets _gi_ _←_ _v_ ˆ _i_ _[⊤]_ [(] _[W][i][µ][i]_ [)][ (unnormalized dot product), removing the normalization by]
_∥Wiµi∥_ 2. Tests the effect of component-output normalization.


**Magnitude** _λ_ _ℓ_ 0 Selects top- _K_ components (hard threshold) matching Elastic-Net sparsity. Tests if
sparsity alone explains gains.
_ℓ_ 2 Uses Elastic-Net with _α_ = 0 (Ridge regularization), resulting in dense edits. Tests
if dense edits can preserve utility.


**E.1. Unified Performance Summary**


To facilitate a high-level comparison, Table 3 aggregates the results across all three behavioral settings: Safety Alignment,
Truthfulness, and Efficient Reasoning.


We normalize the attribute scores to a common [0 _,_ 1] scale. For **Safety** and **Truthfulness**, we use the raw percentage divided by 100. For **Efficient** **Reasoning**, where lower length is better, we define the efficiency score as
min(1 _, L_ **STEER2EDIT** _/L_ Ablation). **STEER2EDIT** consistently achieves the highest combined **Attribute** _×_ **Utility** score,
demonstrating that precise input alignment, normalized scoring, and sparse regularization are all critical for optimal
performance.


_Table 3._ **Unified Performance Summary.** Results are averaged across 6 models (2 per setting). **STEER2EDIT** achieves the best global
trade-off between targeting the attribute and maintaining downstream utility.


**Normalized Attribute Score** _↑_ **Normalized Utility Score** _↑_ **Overall Average** _↑_
**Category** **Variant** **Attr** _×_ **Util**
Safety Truth Effic. Safety Truth Effic. **Attribute** **Utility**


**Full Method** **Steer2Edit** 0.807 **0.550** **1.000** 0.341 0.536 0.755 **0.786** 0.544 **0.427**


**Input** _k_ _k_ mean **0.827** 0.531 0.926 0.279 0.350 0.589 0.761 0.406 0.309
_k_ svd 0.536 0.474 0.757 **0.400** **0.572** **0.805** 0.589 **0.592** 0.349


**Score** _g_ _g_ dot 0.102 0.509 0.628 0.047 0.232 0.003 0.413 0.094 0.039

**Magnitude** _λ_ _ℓ_ 0 0.506 0.546 0.767 0.321 0.423 0.596 0.606 0.447 0.271
_ℓ_ 2 0.000 0.580 0.472 0.032 0.226 0.394 0.350 0.217 0.076


**Key Insights:** **Normalization and Sparsity.** Two critical design principles emerge from these aggregated results. First,
**Score** **Normalization** **is** **paramount** **for** **stability.** The catastrophic failure of the unnormalized _g_ dot variant (Overall
Score: 0.039) reveals that raw activation magnitudes vary drastically across model layers. Without the cosine-similarity
normalization used in **STEER2EDIT**, the editing process becomes dominated by high-norm layers, destabilizing the model
regardless of the target attribute. Second, **Sparsity is essential for utility preservation.** The dense _ℓ_ 2 baseline struggles to
maintain downstream performance (Utility: 0.217), confirming that precise, sparse interventions are required to disentangle


20


**Steer2Edit:** **From Activation Steering to Component-Level Editing**


specific behaviors without overwriting the model’s general knowledge base.


**E.2. Detailed Per-Setting Results**


The following subsections analyze the impact of each component across our three behavioral settings. We find that while
different tasks exhibit unique sensitivities, the failures of the ablation baselines consistently point to the necessity of
**STEER2EDIT** ’s three-pillared approach: precise directional alignment, normalized scoring, and sparse editing.


**Safety Alignment:** **Selective vs.** **Uniform Triggering.** Table 4 highlights the risks of uniformly triggered edits. The
_k_ mean baseline, which activates edits based on the global mean activation E[ _x_ ], achieves high safety (e.g., 92.20% refusal on
ADV-LLM) but substantially reduces utility (21.75% vs. 28.00% for **STEER2EDIT** ). This indicates that activating edits
in a largely input-agnostic manner leads to significant degradation on benign downstream tasks. Conversely, the dense _ℓ_ 2
baseline results in near-total model failure (0.05% safety), suggesting that safety-related behavior is mediated by localized
components and is disrupted by dense parameter modifications. **STEER2EDIT** avoids these failure modes by combining
input-selective activation with sparse, component-level edits.


_Table 4._ **Safety Alignment Ablations (Detailed).** Metrics are Average Safety (Refusal Rate) and Average Utility (Accuracy).


**Avg** **Avg** **Safety (Refusal Rate)** **Utility (Accuracy)**
**Model** **Variant** **S** _×_ **U**
**Safety** **Util** GCG ADV-LLM CommonsenseQA Code-MMLU GSM8K





|Steer2Edit 24.68 88.15 28.00 95.10 81.20 45.01 20.06 18.93<br>k 19.12 87.90 21.75 83.60 92.20 30.14 19.57 15.53<br>Llama2- mean<br>k 22.82 66.35 34.39 90.80 41.90 50.77 30.49 21.90<br>7B-Chat svd<br>g 0.69 15.35 4.49 23.30 7.40 6.45 5.37 1.65<br>dot<br>ℓ 0 7.66 41.25 18.58 36.40 46.10 27.26 25.43 3.05<br>ℓ 2 0.00 0.05 6.33 0.10 0.00 3.60 14.88 0.52|95.10 81.20|45.01 20.06 18.93|
|---|---|---|
|Llama2-<br>7B-Chat<br>Steer2Edit<br>**24.68**<br>**88.15**<br>28.00<br>**95.10**<br>81.20<br>45.01<br>20.06<br>18.93<br>_k_mean<br>19.12<br>87.90<br>21.75<br>83.60<br>**92.20**<br>30.14<br>19.57<br>15.53<br>_k_svd<br>22.82<br>66.35<br>**34.39**<br>90.80<br>41.90<br>**50.77**<br>**30.49**<br>**21.90**<br>_g_dot<br>0.69<br>15.35<br>4.49<br>23.30<br>7.40<br>6.45<br>5.37<br>1.65<br>_ℓ_0<br>7.66<br>41.25<br>18.58<br>36.40<br>46.10<br>27.26<br>25.43<br>3.05<br>_ℓ_2<br>0.00<br>0.05<br>6.33<br>0.10<br>0.00<br>3.60<br>14.88<br>0.52|83.60<br>**92.20**<br>90.80<br>41.90|30.14<br>19.57<br>15.53<br>**50.77**<br>**30.49**<br>**21.90**|
|Llama2-<br>7B-Chat<br>Steer2Edit<br>**24.68**<br>**88.15**<br>28.00<br>**95.10**<br>81.20<br>45.01<br>20.06<br>18.93<br>_k_mean<br>19.12<br>87.90<br>21.75<br>83.60<br>**92.20**<br>30.14<br>19.57<br>15.53<br>_k_svd<br>22.82<br>66.35<br>**34.39**<br>90.80<br>41.90<br>**50.77**<br>**30.49**<br>**21.90**<br>_g_dot<br>0.69<br>15.35<br>4.49<br>23.30<br>7.40<br>6.45<br>5.37<br>1.65<br>_ℓ_0<br>7.66<br>41.25<br>18.58<br>36.40<br>46.10<br>27.26<br>25.43<br>3.05<br>_ℓ_2<br>0.00<br>0.05<br>6.33<br>0.10<br>0.00<br>3.60<br>14.88<br>0.52|23.30<br>7.40|6.45<br>5.37<br>1.65|


|Steer2Edit 29.38 73.15 40.16 75.20 71.10 57.00 50.37 13.10<br>k 26.33 77.45 34.00 71.60 83.30 54.24 45.55 2.22<br>Mistral-7B mean<br>k 18.59 40.85 45.51 68.80 12.90 53.61 51.95 30.98<br>-Instruct svd<br>g 0.25 5.05 4.96 0.90 9.20 5.43 9.45 0.01<br>dot<br>ℓ 0 27.29 59.85 45.60 77.20 42.50 55.96 48.35 32.48<br>ℓ 2 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00|75.20 71.10|57.00 50.37 13.10|
|---|---|---|
|Mistral-7B<br>-Instruct<br>Steer2Edit<br>**29.38**<br>73.15<br>40.16<br>75.20<br>71.10<br>**57.00**<br>50.37<br>13.10<br>_k_mean<br>26.33<br>**77.45**<br>34.00<br>71.60<br>**83.30**<br>54.24<br>45.55<br>2.22<br>_k_svd<br>18.59<br>40.85<br>45.51<br>68.80<br>12.90<br>53.61<br>**51.95**<br>30.98<br>_g_dot<br>0.25<br>5.05<br>4.96<br>0.90<br>9.20<br>5.43<br>9.45<br>0.01<br>_ℓ_0<br>27.29<br>59.85<br>**45.60**<br>**77.20**<br>42.50<br>55.96<br>48.35<br>**32.48**<br>_ℓ_2<br>0.00<br>0.00<br>0.00<br>0.00<br>0.00<br>0.00<br>0.00<br>0.00|71.60<br>**83.30**<br>68.80<br>12.90|54.24<br>45.55<br>2.22<br>53.61<br>**51.95**<br>30.98|
|Mistral-7B<br>-Instruct<br>Steer2Edit<br>**29.38**<br>73.15<br>40.16<br>75.20<br>71.10<br>**57.00**<br>50.37<br>13.10<br>_k_mean<br>26.33<br>**77.45**<br>34.00<br>71.60<br>**83.30**<br>54.24<br>45.55<br>2.22<br>_k_svd<br>18.59<br>40.85<br>45.51<br>68.80<br>12.90<br>53.61<br>**51.95**<br>30.98<br>_g_dot<br>0.25<br>5.05<br>4.96<br>0.90<br>9.20<br>5.43<br>9.45<br>0.01<br>_ℓ_0<br>27.29<br>59.85<br>**45.60**<br>**77.20**<br>42.50<br>55.96<br>48.35<br>**32.48**<br>_ℓ_2<br>0.00<br>0.00<br>0.00<br>0.00<br>0.00<br>0.00<br>0.00<br>0.00|0.90<br>9.20|5.43<br>9.45<br>0.01|
|Mistral-7B<br>-Instruct<br>Steer2Edit<br>**29.38**<br>73.15<br>40.16<br>75.20<br>71.10<br>**57.00**<br>50.37<br>13.10<br>_k_mean<br>26.33<br>**77.45**<br>34.00<br>71.60<br>**83.30**<br>54.24<br>45.55<br>2.22<br>_k_svd<br>18.59<br>40.85<br>45.51<br>68.80<br>12.90<br>53.61<br>**51.95**<br>30.98<br>_g_dot<br>0.25<br>5.05<br>4.96<br>0.90<br>9.20<br>5.43<br>9.45<br>0.01<br>_ℓ_0<br>27.29<br>59.85<br>**45.60**<br>**77.20**<br>42.50<br>55.96<br>48.35<br>**32.48**<br>_ℓ_2<br>0.00<br>0.00<br>0.00<br>0.00<br>0.00<br>0.00<br>0.00<br>0.00|**77.20**<br>42.50<br>0.00<br>0.00|55.96<br>48.35<br>**32.48**<br>0.00<br>0.00<br>0.00|


21


**Steer2Edit:** **From Activation Steering to Component-Level Editing**


**Truthfulness:** **The Critical Role of Sparsity.** Table 5 provides strong evidence for the necessity of sparse editing ( _ℓ_ 0
regularization). The dense _ℓ_ 2 variant, which modifies all parameters in the target block, causes catastrophic utility collapse
(0.00% on Llama3-8B), demonstrating that dense edits severely disrupt the model’s general capabilities. Additionally,
we observe an informative trade-off with _k_ svd: while it preserves high utility (65.11% on Llama3), it fails to significantly
improve truthfulness (39.61%). This suggests that aligning edits with the model’s intrinsic dominant activation patterns is
insufficient to induce a shift toward truthful behavior. Only **STEER2EDIT** balances these objectives: it uses _k_ to selectively
activate edits on semantically relevant inputs, while _ℓ_ 0 sparsity restricts the intervention to a small set of behaviorally
relevant neurons.


_Table 5._ **Truthfulness Ablations (Detailed).** Metrics are Average Truthfulness (TruthfulQA Accuracy) and Average Utility (Accuracy).






|Model Method T × U Avg Avg Attribute Utility (Accuracy) Truth Util TruthfulQA CommonsenseQA Code-MMLU GSM8K|Attribute TruthfulQA|Utility (Accuracy) CommonsenseQA Code-MMLU GSM8K|
|---|---|---|
|Gemma2<br>2B-IT<br>Steer2Edit<br>25.30<br>56.97<br>44.41<br>56.97<br>**69.00**<br>37.07<br>27.16<br>_k_mean<br>24.93<br>55.75<br>44.71<br>55.75<br>68.59<br>38.29<br>27.24<br>_k_svd<br>**27.26**<br>55.26<br>**49.33**<br>55.26<br>68.12<br>**39.39**<br>**40.48**<br>_g_dot<br>1.16<br>**58.68**<br>1.98<br>**58.68**<br>2.83<br>2.20<br>0.90<br>_ℓ_0<br>15.33<br>57.95<br>26.46<br>57.95<br>58.29<br>16.04<br>5.06<br>_ℓ_2<br>26.15<br>57.95<br>45.12<br>57.95<br>63.62<br>36.95<br>34.78|56.97|**69.00**<br>37.07<br>27.16|
|Gemma2<br>2B-IT<br>Steer2Edit<br>25.30<br>56.97<br>44.41<br>56.97<br>**69.00**<br>37.07<br>27.16<br>_k_mean<br>24.93<br>55.75<br>44.71<br>55.75<br>68.59<br>38.29<br>27.24<br>_k_svd<br>**27.26**<br>55.26<br>**49.33**<br>55.26<br>68.12<br>**39.39**<br>**40.48**<br>_g_dot<br>1.16<br>**58.68**<br>1.98<br>**58.68**<br>2.83<br>2.20<br>0.90<br>_ℓ_0<br>15.33<br>57.95<br>26.46<br>57.95<br>58.29<br>16.04<br>5.06<br>_ℓ_2<br>26.15<br>57.95<br>45.12<br>57.95<br>63.62<br>36.95<br>34.78|55.75<br>55.26|68.59<br>38.29<br>27.24<br>68.12<br>**39.39**<br>**40.48**|
|Gemma2<br>2B-IT<br>Steer2Edit<br>25.30<br>56.97<br>44.41<br>56.97<br>**69.00**<br>37.07<br>27.16<br>_k_mean<br>24.93<br>55.75<br>44.71<br>55.75<br>68.59<br>38.29<br>27.24<br>_k_svd<br>**27.26**<br>55.26<br>**49.33**<br>55.26<br>68.12<br>**39.39**<br>**40.48**<br>_g_dot<br>1.16<br>**58.68**<br>1.98<br>**58.68**<br>2.83<br>2.20<br>0.90<br>_ℓ_0<br>15.33<br>57.95<br>26.46<br>57.95<br>58.29<br>16.04<br>5.06<br>_ℓ_2<br>26.15<br>57.95<br>45.12<br>57.95<br>63.62<br>36.95<br>34.78|**58.68**|2.83<br>2.20<br>0.90|


|Steer2Edit 33.27 53.06 62.71 53.06 66.86 52.74 68.54<br>k 12.74 50.37 25.29 50.37 39.67 25.61 10.60<br>Llama3 mean<br>k 25.79 39.61 65.11 39.61 71.30 51.71 72.32<br>8B-Instruct svd<br>g 19.11 43.03 44.42 43.03 26.94 41.77 64.56<br>dot<br>ℓ 0 29.87 51.34 58.18 51.34 64.14 47.13 63.26<br>ℓ 2 0.00 57.95 0.00 57.95 0.00 0.00 0.00|53.06|66.86 52.74 68.54|
|---|---|---|
|Llama3<br>8B-Instruct<br>Steer2Edit<br>**33.27**<br>53.06<br>62.71<br>53.06<br>66.86<br>**52.74**<br>68.54<br>_k_mean<br>12.74<br>50.37<br>25.29<br>50.37<br>39.67<br>25.61<br>10.60<br>_k_svd<br>25.79<br>39.61<br>**65.11**<br>39.61<br>**71.30**<br>51.71<br>**72.32**<br>_g_dot<br>19.11<br>43.03<br>44.42<br>43.03<br>26.94<br>41.77<br>64.56<br>_ℓ_0<br>29.87<br>51.34<br>58.18<br>51.34<br>64.14<br>47.13<br>63.26<br>_ℓ_2<br>0.00<br>**57.95**<br>0.00<br>**57.95**<br>0.00<br>0.00<br>0.00|50.37<br>39.61|39.67<br>25.61<br>10.60<br>**71.30**<br>51.71<br>**72.32**|
|Llama3<br>8B-Instruct<br>Steer2Edit<br>**33.27**<br>53.06<br>62.71<br>53.06<br>66.86<br>**52.74**<br>68.54<br>_k_mean<br>12.74<br>50.37<br>25.29<br>50.37<br>39.67<br>25.61<br>10.60<br>_k_svd<br>25.79<br>39.61<br>**65.11**<br>39.61<br>**71.30**<br>51.71<br>**72.32**<br>_g_dot<br>19.11<br>43.03<br>44.42<br>43.03<br>26.94<br>41.77<br>64.56<br>_ℓ_0<br>29.87<br>51.34<br>58.18<br>51.34<br>64.14<br>47.13<br>63.26<br>_ℓ_2<br>0.00<br>**57.95**<br>0.00<br>**57.95**<br>0.00<br>0.00<br>0.00|43.03|26.94<br>41.77<br>64.56|
|Llama3<br>8B-Instruct<br>Steer2Edit<br>**33.27**<br>53.06<br>62.71<br>53.06<br>66.86<br>**52.74**<br>68.54<br>_k_mean<br>12.74<br>50.37<br>25.29<br>50.37<br>39.67<br>25.61<br>10.60<br>_k_svd<br>25.79<br>39.61<br>**65.11**<br>39.61<br>**71.30**<br>51.71<br>**72.32**<br>_g_dot<br>19.11<br>43.03<br>44.42<br>43.03<br>26.94<br>41.77<br>64.56<br>_ℓ_0<br>29.87<br>51.34<br>58.18<br>51.34<br>64.14<br>47.13<br>63.26<br>_ℓ_2<br>0.00<br>**57.95**<br>0.00<br>**57.95**<br>0.00<br>0.00<br>0.00|51.34<br>**57.95**|64.14<br>47.13<br>63.26<br>0.00<br>0.00<br>0.00|



**Efficient Reasoning:** **Stability via Normalization.** Table 6 highlights the critical role of score normalization for stable
reasoning control. The _g_ dot variant, which uses the raw dot product, fails pathologically: it reduces the reasoning length to
just 21 tokens (Qwen3-4B) while collapsing utility to near zero (0.13%). This behavior arises because activation norms vary
substantially across layers; without the cosine normalization used in **STEER2EDIT**, edit magnitudes become dominated by
high-norm layers, leading to severe disruption of model behavior. Conversely, the _k_ svd baseline increases reasoning length
(5351 vs. 3467 for **STEER2EDIT** ), indicating that activating edits along the model’s intrinsic dominant activation patterns
is insufficient for improving efficiency. Together, these results show that effective reasoning-length control requires both
normalized importance scoring and task-specific edit activation, as implemented in **STEER2EDIT** .


_Table 6._ **Efficient Reasoning Ablations (Detailed).** Metrics are Reasoning Length (Lower is Better) and Utility (Higher is Better). The **U**
**/ L** metric represents efficiency (Utility _/_ Length _×_ 100).





|Model Variant U / L Avg Avg Reasoning Length (Lower is Better) Utility (Higher is Better) Len Util MATH-500 GPQA Code-MMLU GSM8K MATH-500 GPQA Code-MMLU GSM8K|Reasoning Length (Lower is Better) MATH-500 GPQA Code-MMLU GSM8K|Utility (Higher is Better) MATH-500 GPQA Code-MMLU GSM8K|
|---|---|---|
|Qwen3<br>4B-Thinking<br>Steer2Edit<br>**2.28**<br>3467<br>78.95<br>4136<br>5299<br>3433<br>1000<br>92.2<br>44.4<br>87.6<br>91.5<br>_k_mean<br>1.56<br>3266<br>51.05<br>3188<br>2728<br>6129<br>1018<br>53.2<br>10.3<br>78.1<br>62.7<br>_k_svd<br>1.64<br>5351<br>**87.99**<br>6389<br>8780<br>4622<br>1613<br>**96.9**<br>**67.5**<br>**93.9**<br>**93.6**<br>_g_dot<br>0.62<br>**21**<br>0.13<br>**23**<br>**33**<br>**10**<br>**18**<br>0.3<br>0.0<br>0.0<br>0.2<br>_ℓ_0<br>0.73<br>6506<br>47.61<br>8646<br>5202<br>4698<br>7477<br>44.7<br>36.0<br>65.7<br>44.1<br>_ℓ_2<br>0.08<br>22476<br>17.63<br>32223<br>18987<br>6420<br>32274<br>3.0<br>15.2<br>50.4<br>2.0|4136<br>5299<br>3433<br>1000|92.2<br>44.4<br>87.6<br>91.5|
|Qwen3<br>4B-Thinking<br>Steer2Edit<br>**2.28**<br>3467<br>78.95<br>4136<br>5299<br>3433<br>1000<br>92.2<br>44.4<br>87.6<br>91.5<br>_k_mean<br>1.56<br>3266<br>51.05<br>3188<br>2728<br>6129<br>1018<br>53.2<br>10.3<br>78.1<br>62.7<br>_k_svd<br>1.64<br>5351<br>**87.99**<br>6389<br>8780<br>4622<br>1613<br>**96.9**<br>**67.5**<br>**93.9**<br>**93.6**<br>_g_dot<br>0.62<br>**21**<br>0.13<br>**23**<br>**33**<br>**10**<br>**18**<br>0.3<br>0.0<br>0.0<br>0.2<br>_ℓ_0<br>0.73<br>6506<br>47.61<br>8646<br>5202<br>4698<br>7477<br>44.7<br>36.0<br>65.7<br>44.1<br>_ℓ_2<br>0.08<br>22476<br>17.63<br>32223<br>18987<br>6420<br>32274<br>3.0<br>15.2<br>50.4<br>2.0|3188<br>2728<br>6129<br>1018<br>6389<br>8780<br>4622<br>1613|53.2<br>10.3<br>78.1<br>62.7<br>**96.9**<br>**67.5**<br>**93.9**<br>**93.6**|
|Qwen3<br>4B-Thinking<br>Steer2Edit<br>**2.28**<br>3467<br>78.95<br>4136<br>5299<br>3433<br>1000<br>92.2<br>44.4<br>87.6<br>91.5<br>_k_mean<br>1.56<br>3266<br>51.05<br>3188<br>2728<br>6129<br>1018<br>53.2<br>10.3<br>78.1<br>62.7<br>_k_svd<br>1.64<br>5351<br>**87.99**<br>6389<br>8780<br>4622<br>1613<br>**96.9**<br>**67.5**<br>**93.9**<br>**93.6**<br>_g_dot<br>0.62<br>**21**<br>0.13<br>**23**<br>**33**<br>**10**<br>**18**<br>0.3<br>0.0<br>0.0<br>0.2<br>_ℓ_0<br>0.73<br>6506<br>47.61<br>8646<br>5202<br>4698<br>7477<br>44.7<br>36.0<br>65.7<br>44.1<br>_ℓ_2<br>0.08<br>22476<br>17.63<br>32223<br>18987<br>6420<br>32274<br>3.0<br>15.2<br>50.4<br>2.0|**23**<br>**33**<br>**10**<br>**18**|0.3<br>0.0<br>0.0<br>0.2|


|Steer2Edit 1.62 4445 72.12 3405 7821 5038 1515 94.4 30.1 75.8 88.1<br>OpenMath- kmean 1.28 5216 66.69 3838 8814 6522 1691 92.5 25.8 66.7 81.9<br>ksvd 1.42 5131 73.01 4188 8880 4985 2472 93.9 32.8 75.6 89.7<br>Nemotron-7B<br>gdot 0.00 17338 0.52 18380 16628 17163 17182 0.9 0.0 0.6 0.6<br>ℓ0 1.64 4356 71.60 3422 7971 4503 1528 94.5 29.6 73.4 88.9<br>ℓ2 1.09 5633 61.23 2911 12686 5160 1773 89.5 17.7 66.1 71.7|3405 7821 5038 1515|94.4 30.1 75.8 88.1|
|---|---|---|
|OpenMath-<br>Nemotron-7B<br>Steer2Edit<br>1.62<br>4445<br>72.12<br>3405<br>**7821**<br>5038<br>**1515**<br>94.4<br>30.1<br>**75.8**<br>88.1<br>_k_mean<br>1.28<br>5216<br>66.69<br>3838<br>8814<br>6522<br>1691<br>92.5<br>25.8<br>66.7<br>81.9<br>_k_svd<br>1.42<br>5131<br>**73.01**<br>4188<br>8880<br>4985<br>2472<br>93.9<br>**32.8**<br>75.6<br>**89.7**<br>_g_dot<br>0.00<br>17338<br>0.52<br>18380<br>16628<br>17163<br>17182<br>0.9<br>0.0<br>0.6<br>0.6<br>_ℓ_0<br>**1.64**<br>**4356**<br>71.60<br>3422<br>7971<br>**4503**<br>1528<br>**94.5**<br>29.6<br>73.4<br>88.9<br>_ℓ_2<br>1.09<br>5633<br>61.23<br>**2911**<br>12686<br>5160<br>1773<br>89.5<br>17.7<br>66.1<br>71.7|3838<br>8814<br>6522<br>1691<br>4188<br>8880<br>4985<br>2472|92.5<br>25.8<br>66.7<br>81.9<br>93.9<br>**32.8**<br>75.6<br>**89.7**|
|OpenMath-<br>Nemotron-7B<br>Steer2Edit<br>1.62<br>4445<br>72.12<br>3405<br>**7821**<br>5038<br>**1515**<br>94.4<br>30.1<br>**75.8**<br>88.1<br>_k_mean<br>1.28<br>5216<br>66.69<br>3838<br>8814<br>6522<br>1691<br>92.5<br>25.8<br>66.7<br>81.9<br>_k_svd<br>1.42<br>5131<br>**73.01**<br>4188<br>8880<br>4985<br>2472<br>93.9<br>**32.8**<br>75.6<br>**89.7**<br>_g_dot<br>0.00<br>17338<br>0.52<br>18380<br>16628<br>17163<br>17182<br>0.9<br>0.0<br>0.6<br>0.6<br>_ℓ_0<br>**1.64**<br>**4356**<br>71.60<br>3422<br>7971<br>**4503**<br>1528<br>**94.5**<br>29.6<br>73.4<br>88.9<br>_ℓ_2<br>1.09<br>5633<br>61.23<br>**2911**<br>12686<br>5160<br>1773<br>89.5<br>17.7<br>66.1<br>71.7|18380<br>16628<br>17163<br>17182|0.9<br>0.0<br>0.6<br>0.6|
|OpenMath-<br>Nemotron-7B<br>Steer2Edit<br>1.62<br>4445<br>72.12<br>3405<br>**7821**<br>5038<br>**1515**<br>94.4<br>30.1<br>**75.8**<br>88.1<br>_k_mean<br>1.28<br>5216<br>66.69<br>3838<br>8814<br>6522<br>1691<br>92.5<br>25.8<br>66.7<br>81.9<br>_k_svd<br>1.42<br>5131<br>**73.01**<br>4188<br>8880<br>4985<br>2472<br>93.9<br>**32.8**<br>75.6<br>**89.7**<br>_g_dot<br>0.00<br>17338<br>0.52<br>18380<br>16628<br>17163<br>17182<br>0.9<br>0.0<br>0.6<br>0.6<br>_ℓ_0<br>**1.64**<br>**4356**<br>71.60<br>3422<br>7971<br>**4503**<br>1528<br>**94.5**<br>29.6<br>73.4<br>88.9<br>_ℓ_2<br>1.09<br>5633<br>61.23<br>**2911**<br>12686<br>5160<br>1773<br>89.5<br>17.7<br>66.1<br>71.7|3422<br>7971<br>**4503**<br>1528<br>**2911**<br>12686<br>5160<br>1773|**94.5**<br>29.6<br>73.4<br>88.9<br>89.5<br>17.7<br>66.1<br>71.7|


22


**Steer2Edit:** **From Activation Steering to Component-Level Editing**


**F. Component-Wise Budget Sensitivity Analysis**


In the main paper, we show that the best-performing **STEER2EDIT** configurations exhibit a consistent component-level
structure: safety and truthfulness control rely on sparse edits to attention heads, whereas reasoning efficiency is primarily
governed by distributed MLP neuron edits.


To further validate that this structural separation is intrinsic to the underlying mechanisms, we conduct a controlled
_component-wise budget sensitivity analysis_ . In this study, we fix the sparsity parameter _α_ and vary the regularization budget
of one component class at a time, while disabling edits to the other class by sending its budget to infinity ( _ρ →∞_ ). This
isolates how changes in attention and MLP budgets individually influence the attribute–utility trade-off.


**F.1. Safety Alignment:** **Sensitivity to Attention Budget**


Figure 11 illustrates how the safety–utility trade-off responds to changes in the attention and MLP budgets when considered
in isolation. Increasing the attention budget _ρ_ attn produces substantial gains in refusal rate at moderate utility cost, closely
matching the best joint configurations reported in the main paper. In contrast, varying the MLP budget _ρ_ mlp leads to markedly
weaker safety improvements and often degrades utility more rapidly.


This asymmetric sensitivity indicates that safety alignment is primarily mediated by a small number of attention heads. The
result is consistent with the sparsity patterns observed in Figure 3, where non-zero edit coefficients are concentrated in
late-layer attention components, with minimal contribution from MLP neurons.



80


60


40


20



Component Ablation: Safety vs. Utility

LLaMA-2-7B-Chat Mistral-7B-Instruct-v0.2

80


70


60





50


40


30


20


10


0


|Col1|Col2|Col3|Col4|Col5|
|---|---|---|---|---|
|||||~~=~~ 0.7<br>~~=~~ 0.7|
||||||
||||||
||||||


|Col1|Col2|Col3|Col4|Col5|Col6|Col7|Col8|
|---|---|---|---|---|---|---|---|
|||||||||
|||||||||
||||||||<br>|
||||||||~~=~~<br>~~= 0.~~|
|||||||||
|||||||||
|||||||||
|||||||||



0 10 20 30 40 50
Average Utility (Accuracy)





0





0 10 20 30





_Figure 11._ **Component-wise budget sensitivity for safety alignment.** We fix the sparsity parameter _α_ and vary the attention regularization
budget _ρ_ attn while disabling MLP edits by taking _ρ_ mlp _→∞_, and vice versa. Improvements in refusal rate are primarily driven by changes
in the attention budget, whereas varying the MLP budget yields limited safety gains and earlier utility degradation.


**F.2. Truthfulness:** **Sensitivity Dominated by Attention**


Figure 12 reports the component-wise budget sensitivity for truthfulness promotion. Across both evaluated models,
increasing the attention budget consistently yields larger improvements in truthful preference accuracy than increasing the
MLP budget under the same sparsity constraint. MLP-only edits fail to recover the trade-off frontier achieved by attention
edits.


These findings align with the component-level edit distributions shown in Figure 5, which reveal that truthfulness control
is achieved through sparse, localized attention interventions. Notably, several models exhibit predominantly negative edit
coefficients, suggesting that suppressing hallucination-promoting attention heads is more effective than broadly modifying
MLP computation.


23


**Steer2Edit:** **From Activation Steering to Component-Level Editing**


Component Ablation: Truthfulness vs. Utility

Gemma-2-2B-IT LLaMA-3-8B-Instruct



60


58


56


54





60.0


57.5


55.0


52.5


50.0


47.5


45.0


42.5


40.0





52


50


48






|Col1|Col2|Col3|Col4|Col5|Col6|Col7|
|---|---|---|---|---|---|---|
||||||||
||||||||
|||||||= 0|
|0.<br> .1|1|||||<br>=|
||||||||


|Col1|Col2|Col3|Col4|Col5|Col6|Col7|Col8|
|---|---|---|---|---|---|---|---|
|.1||||||||
|||||||||
|||||||||
|||||||||
|||||||~~= 0~~|~~ .1~~|
||||||||=<br>=|



0 10 20 30 40 50



0 10 20 30 40 50 60 70
Average Utility (Accuracy)





_Figure_ _12._ **Component-wise** **budget** **sensitivity** **for** **truthfulness** **control.** Truthfulness improvements are strongly sensitive to the
attention budget _ρ_ attn, while varying the MLP budget _ρ_ mlp in isolation results in substantially smaller gains at comparable downstream
utility.


**F.3. Efficient Reasoning:** **Sensitivity Dominated by MLP Budget**


Figure 13 shows that reasoning efficiency exhibits a qualitatively different sensitivity pattern. Increasing the MLP budget
_ρ_ mlp leads to a smooth and substantial reduction in reasoning length while preserving accuracy. In contrast, varying the
attention budget _ρ_ attn in isolation produces only marginal efficiency improvements, even at large budgets.


This behavior mirrors the dense MLP edit patterns observed in Figure 7 and confirms that efficient reasoning control requires
coordinated, distributed modifications to MLP neurons across layers. Unlike safety and truthfulness, which are governed by
localized attention-based circuits, reasoning efficiency emerges from broad MLP-based computation.



Reasoning Efficiency - Accuracy Trade-off

Qwen3-4B-Thinking-2507 OpenMath-Nemotron-7B



3000


3500


4000


4500


5000


5500









4400


4500


4600


4700


4800


4900


5000


5100








|Col1|Col2|Col3|Col4|Col5|Col6|Col7|
|---|---|---|---|---|---|---|
|=|0.6||||||
|||||||= 1.2|
||||||||
|||||||<br>= 1|
||||||=|.6|


|Col1|Col2|Col3|Col4|Col5|Col6|Col7|Col8|Col9|Col10|Col11|
|---|---|---|---|---|---|---|---|---|---|---|
||||||||||||
||= 0.7||||||||||
||||~~= 1~~.2|~~= 1~~.2|||||||
||||||||||||
||~~= 0.2~~||||||||||
||~~= 0.2~~|||~~=~~|~~ .8~~||||||
||||||||||||
||||||||||||
||||||||||||
||||||||||||



60 65 70 75 80 85 90



70 71 72 73 74 75 76
Average Accuracy (Higher Better)





_Figure 13._ **Component-wise budget sensitivity for reasoning efficiency.** Reductions in reasoning length are strongly influenced by the
MLP budget _ρ_ mlp, while varying the attention budget _ρ_ attn yields only minor efficiency gains. This indicates that efficient reasoning is
governed by distributed MLP computation rather than sparse attention circuits.


**Summary.** Across all behavioral control settings, this component-wise budget sensitivity analysis establishes a clear correspondence between the component class whose budget most strongly influences the trade-off frontier and the components
receiving non-zero edits in the best-performing **STEER2EDIT** configurations. Safety and truthfulness are attentiondominated, whereas reasoning efficiency is MLP-dominated, providing further evidence that **STEER2EDIT** uncovers
genuine, setting-dependent circuit structure rather than artifacts of hyperparameter tuning.


24


**Steer2Edit:** **From Activation Steering to Component-Level Editing**


**G. Additional Baselines:** **Comparing STEER2EDIT with Training-Based Methods**


We compare STEER2EDIT against training-based adaptation methods that directly optimize model parameters toward a
target behavior. Specifically, we consider **full-parameter fine-tuning** and **rank-1 LoRA fine-tuning** as additional baselines.


**Setup and comparison protocol.** For each control setting (safety, truthfulness, and efficient reasoning), we fine-tune
models on the _same probing dataset used to extract steering vectors_ . Training uses the _positive set_ (i.e., examples that exhibit
the target attribute), so the model is explicitly optimized to imitate the desired behavior. We evaluate the resulting models
using the same attribute and downstream utility metrics as in the main experiments and report trade-off curves alongside
activation steering and STEER2EDIT. The **full** fine-tuning baseline updates all model parameters. The **rank-1** baseline
applies LoRA adapters with rank _r_ = 1, inserted into the standard attention projections (q ~~p~~ roj, k ~~p~~ roj, v ~~p~~ roj,

- ~~p~~ roj) and MLP projections (gate proj, up ~~p~~ roj, down ~~p~~ roj), while keeping the backbone weights frozen. All
baselines are trained with standard supervised objectives and comparable training budgets.


**G.1. Safety Alignment**


Figure 14 shows the safety–utility trade-off for models fine-tuned on the safety probing positive set. Full fine-tuning
increases refusal rates but often does so by globally shifting the model’s response distribution, leading to over-refusal on
benign queries and sharp drops in downstream utility, particularly for Mistral. Rank-1 LoRA produces minimal changes,
indicating limited capacity to induce reliable safety behavior under this supervision.



90


80


70


60


50



Safety Alignment - Utility Trade-off

LLaMA-2-7B-Chat Mistral-7B-Instruct-v0.2


90


80


70


60


50


40


30



20 25 30 35
Average Utility (Accuracy)



10 20 30 40 50
Average Utility (Accuracy)



Original
Steering Vector



Steer2Edit (Ours)
full parameter finetune



rank1 finetune



_Figure 14._ **Safety–utility trade-off with training-based baselines.** Full fine-tuning improves refusal rates but frequently collapses utility
due to over-refusal, especially in the low-data regime. Rank-1 LoRA has negligible effect. These trends indicate that training-based
optimization on small positive sets induces coarse, global behavioral shifts rather than selective safety control.


**G.2. Truthfulness**


Figure 15 reports the truthfulness–utility trade-off for models fine-tuned on the truthfulness probing positive set. Full
fine-tuning yields modest improvements in TruthfulQA accuracy, but these gains are typically accompanied by noticeable
degradation in downstream utility, suggesting broad shifts in the model’s answer distribution rather than selective promotion
of truthfulness. Rank-1 LoRA again exhibits little effect.


25


58


56


54


52


50



**Steer2Edit:** **From Activation Steering to Component-Level Editing**


Truthfulness - Utility Trade-off

Gemma-2 LLaMA-3-8B


52


50


48


46


44


42



35 40 45 50 55 60 65
Average Utility (Accuracy)



10 20 30 40 50
Average Utility (Accuracy)



40



Original
Steering Vector



Steer2Edit (Ours)
full parameter finetune



rank1 finetune



_Figure_ _15._ **Truthfulness–utility** **trade-off** **with** **training-based** **baselines.** Fine-tuning on the positive set improves TruthfulQA
performance but often incurs utility loss, reflecting over-regularization of response behavior. Rank-1 LoRA provides insufficient
adaptation capacity to meaningfully alter truthfulness.


**G.3. Efficient Reasoning**


Figure 16 presents the reasoning efficiency–accuracy trade-off for models fine-tuned on the efficient-reasoning probing
positive set. Full fine-tuning can encourage shorter generations, but the resulting reductions in reasoning length are generally
comparable to activation steering and do not consistently surpass it. Rank-1 LoRA again produces minimal changes,
indicating limited capacity to meaningfully influence reasoning behavior under this supervision.



3000


3500


4000


4500


5000


5500



60 70 80 90
Average Accuracy (Higher Better)



Reasoning Efficiency - Accuracy Trade-off

Qwen3-4B-Thinking-2507 OpenMath-Nemotron-7B

3600


3800


4000


4200


4400


4600


4800


5000



40 50 60 70
Average Accuracy (Higher Better)



Original
Steering Vector



Steer2Edit (Ours)
full parameter finetune



rank1 finetune



_Figure 16._ **Reasoning efficiency–accuracy trade-off with training-based baselines.** Full fine-tuning reduces reasoning length but
largely matches the trade-off achieved by activation steering, without clear advantages. Rank-1 LoRA has little effect.


**Summary.** Across all three control settings, fine-tuning on the probing dataset can move models toward the target attribute,
but typically does so by inducing broad distributional shifts that trace a trade-off curve similar to activation steering. These
limitations are most evident in the low-data regime considered here, where the probing sets are intentionally small and
narrowly targeted. Rank-1 LoRA consistently exhibits weak effects across all settings. In contrast, STEER2EDIT achieves
more favorable trade-offs while remaining training-free and component-interpretable, highlighting the benefit of converting
steering diagnostics into targeted weight edits rather than optimizing behavior through global parameter updates.


26


**Steer2Edit:** **From Activation Steering to Component-Level Editing**


27


