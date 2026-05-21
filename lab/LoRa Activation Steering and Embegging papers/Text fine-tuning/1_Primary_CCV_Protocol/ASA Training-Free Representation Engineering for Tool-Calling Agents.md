## **ASA: Training-Free Representation Engineering for Tool-Calling** **Agents**

**Youjin** **Wang** [1 *] **Run** **Zhou** [1 *] **Rong** **Fu** [2] **Shuaishuai** **Cao** [3] **Hongwei** **Zeng** [4] **Jiaxuan** **Lu** [5]

**Sicheng** **Fan** [6] **Jiaqiao** **Zhao** [7] **Liangming** **Pan** [8]



**Abstract**


Adapting LLM agents to domain-specific tool
calling remains notably brittle under evolving
interfaces. Prompt and schema engineering is
easy to deploy but often fragile under distribution shift and strict parsers, while continual parameter-efficient fine-tuning improves
reliability at the cost of training, maintenance, and potential forgetting. We identify
a critical Lazy Agent failure mode where tool
necessity is nearly perfectly decodable from
mid-layer activations, yet the model remains
conservative in entering tool mode, revealing
a representation-behavior gap. We propose
**Activation** **Steering** **Adapter** **(ASA)**, a
training-free, inference-time controller that
performs a single-shot mid-layer intervention and targets tool domains via a routerconditioned mixture of steering vectors with
a probe-guided signed gate to amplify true intent while suppressing spurious triggers. On
MTU-Bench with Qwen2.5-1.5B, ASA improves strict tool-use F1 from 0.18 to 0.50
while reducing the false positive rate from
0.15 to 0.05, using only about 20KB of
portable assets and no weight updates.


**1.** **Introduction**


Large pretrained models demonstrate strong capabilities across a wide range of tasks, yet their efficient
adaptation to specialized domains remains an open
and practical challenge. In real-world deployments,
the set of available tools, API signatures, and in

*Equal contribution 1Renmin University of China
2University of Macau 3Central South University
4University of the Chinese Academy of Sciences 5Shanghai
AI Laboratory [6] Fudan University [7] Central South University [8] Peking University. Correspondence to: Liangming
Pan <liangming.pan@pku.edu.cn>.


_Preprint._ _February_ _10,_ _2026._



teraction protocols changes frequently, and schemas
continuously accumulate constraints, often leading to
distribution shifts and breakdowns in output formats
when a general model is applied to a concrete environment (Xi et al., 2025; Qin et al., 2023; Patil et al.,
2024; Schick et al., 2023). The central engineering
question is how to adapt a general model to evolving domain toolsets in a way that preserves its broad
competencies while remaining stable and controllable
in production (Hu et al., 2022; Dettmers et al., 2023;
Prottasha et al., 2025). In this paper, we use _tool-_
_calling_ _domain_ _adaptation_ to denote robust _tool_ _se-_
_lection_ _and_ _tool-mode_ _triggering_ under _schema_ _shift_,
i.e., when available tools, API signatures, and interaction protocols evolve over time.This is especially difficult because tool calling is a discrete, parser-defined
mode switch, so small distribution shifts can flip execution even when the underlying intent representation
is preserved; moreover, the cost of updating prompts
or adapters grows linearly with the number of domains
and API versions, becoming prohibitive at scale.


Existing solutions follow two main directions. One direction operates on the input side by using prompts
and schema constraints to steer tool invocation; this
approach is easy to deploy but it consumes context capacity and is fragile under wording or context perturbations (Yao et al., 2022; Qin et al., 2023). The other
direction adapts model parameters via parameterefficient fine-tuning methods such as LoRA and its
quantized variants; such methods improve in-domain
invocation success and format compliance but impose
recurring costs for training, deployment, and regression testing as domains and interfaces proliferate, and
they risk degrading general capabilities over time (Hu
et al., 2022; Dettmers et al., 2023; Tang et al., 2023;
Prottasha et al., 2025; Lu et al., 2025).


When these approaches are deployed in dynamic or adversarial settings, three issues frequently arise. First,
prompt and schema methods are brittle and sensitive
to small changes in wording or context (Qin et al.,
2023). Second, frequent fine-tuning is unsustainable



1


**ASA:** **Training-Free** **Representation** **Engineering** **for** **Tool-Calling** **Agents**


_Figure_ _1._ Overview of tool-calling domain adaptation methods under rapidly evolving tool sets and interaction protocols,
and our inference-time probe-gated activation control.



at scale because the operational burden and risk of
forgetting increase with the number of domains and
interface versions (Hu et al., 2022; Dettmers et al.,
2023; Prottasha et al., 2025). Third, there is a conceptual mismatch in treating tool invocation as mere
knowledge or format injection rather than as a control
problem that requires a reliable switch in the model’s
execution mode. Empirically, we uncover a paradox
that we term ’Lazy Agent failure mode’: linear probes
on mid-layer activations can predict tool necessity with
near-perfect accuracy ( _>_ 99% AUC), yet the model’s
overt generation fails to trigger tools in over 80 percent
of these cases. This reveals a persistent _representation–_
_behavior_ _gap_, characterizing a state where the agent
’knows’ what to do but lacks the activation impulse
to break the generation threshold. Meanwhile, naive
activation injection can also amplify spurious triggers
due to downstream nonlinearities and adversarial constraints. This reveals a key bottleneck at the behaviorcontrol layer (Zou et al., 2023; Turner et al., 2024;
Wehner et al., 2025; Bartoszcze et al., 2025). This
Lazy Agent failure mode characterizes a specific breakdown where tool-use intent is cleanly encoded within
the representation space, but fails to cross the discrete
decision threshold required for execution. Such a gap
renders the model’s tool-calling capabilities brittle, as
the latent "intent" and final "action" are effectively decoupled under strict parsing constraints. To resolve
this, we argue that the agent requires more than just
static guidance; it needs an inference-time control layer
capable of bridging the representation-behavior gap.



Motivated by these observations, we propose a twolevel, inference-time control paradigm that requires no
weight updates. The approach models domain adaptation for agent-style tool-calling as a combination
of representation-level intent alignment and decisionlevel boundary calibration (Zou et al., 2023; Turner
et al., 2024; Wehner et al., 2025). At the representation level we introduce ASA, a compact adapter
that models intent geometry using a shared base vector plus a small set of domain offset experts combined by a lightweight router. At the decision level,
instead of logit-level biasing, we use a _probe-guided_
_signed_ _gate_ that conditionally _opens_ (injects) or _in-_
_verts_ (suppresses) the steering direction, thereby calibrating the discrete tool-mode transition under strict
tool-call parsing and adversarial phrasing (Lee et al.,
2024; Rahn et al., 2024). On the MTU-Bench benchmark, ASA provides strong intent-aligned control with
negligible storage and no training, yielding consistent
improvements in strict F1 (balancing missed calls and
false triggers) while largely preserving output format
and argument compliance. Together, these findings
suggest a practical middle ground that is more robust
than prompt-only approaches and considerably lighterweight than continual fine-tuning.


This positions tool calling as a form of _complex_ _struc-_
_tural_ _behavior_ _control_, which is precisely where existing RepE-style steering is under-explored and where
ASA is designed to operate. Our main contributions
are threefold. First, we identify a _representation–_
_behavior_ _gap_ in tool-calling adaptation: tool intent is



2


**ASA:** **Training-Free** **Representation** **Engineering** **for** **Tool-Calling** **Agents**



nearly perfectly linearly decodable from mid-layer activations, yet strict tool-mode triggering remains conservative, causing missed calls and false triggers. Second, we propose ASA, a training-free, inference-time
activation controller that performs a _single-shot_ midlayer intervention using a router-conditioned _mixture-_
_of-vectors_ and a probe-guided _signed_ _gate_ ; the gate
acts as a context-aware safety valve, enabling bidirectional control with one strength knob _α_ and optimizing strict F1 (Recall–FPR). Third, we introduce a
strictly isolated MTU-Bench protocol with deterministic triggering and post-trigger validity checks (format/tool/args), and show consistent strict-F1 gains
across prompt baselines, LoRA references, and model
scales (0.5B/1.5B/8B),with only KB-level portable assets, under strict production constraints.


**2.** **Related** **Work**


**2.1.** **LLM** **agents** **and** **tool-calling**


LLM agent and tool-calling research integrates external tools into the reasoning/decision loop so models can query, compute, and interact with environments. Most approaches operate at the I/O interface through structured prompting, exemplars/templates, or output normalization and work well in relatively controlled settings. ReAct interleaves reasoning and actions but is prompt-fragile under wording or context shifts (Yao et al., 2022). Reflexion
uses self-reflective memory but relies on stable traces
and protocol assumptions (Shinn et al., 2023). Skillaccumulating agents such as Voyager compose procedures yet often bind to a specific interface, limiting
cross-domain/protocol transfer (Wang et al., 2023).
Output-side supervision or normalization (e.g., Toolformer and parsability-focused methods) improves reliability, but typically requires re-training or strong
constraints when schemas evolve or prompts become
adversarial (Schick et al., 2023; Johnson et al., 2025;
Dang et al., 2025). Overall, prior work strengthens external workflows but offers limited mechanisms for internally stable, transferable execution-mode switching;
we instead study internal control via mid-layer intent
routing with lightweight gated calibration to robustly
trigger tools without weight updates.


**2.2.** **Parameter-efficient** **fine-tuning** **and**
**domain** **adaptation**


Parameter-efficient fine-tuning (PEFT) adapts pretrained models to new domains with minimal additional parameters and computation. Representative
PEFT variants include prompt-based methods such as
Prefix-Tuning (Li & Liang, 2021), sparse parameter



updates like BitFit (Zaken et al., 2022), and low-rank
adaptation approaches such as LoRA and QLoRA,
which use low-rank updates to reduce fine-tuning costs
(Hu et al., 2022; Dettmers et al., 2023). Tool-use
datasets such as ToolAlpaca further show that PEFT
can increase in-domain invocation success and format
compliance (Tang et al., 2023). However, PEFT is
training-driven: as domains and interfaces proliferate
and change, training, deployment, regression testing,
and rollouts scale roughly linearly, with risks of forgetting and version drift. ReFT constrains updates to lowdimensional subspaces to improve stability, but still requires training and thus struggles under rapid protocol
churn (Wu et al., 2024). Other approaches (e.g., SKTuning) assume stable semantic anchors, which may
not hold when alignment targets evolving function-call
schemas (Prottasha et al., 2024). In contrast, we perform inference-time domain alignment via a switchable
two-level control mechanism that leaves base weights
untouched, reducing long-term maintenance burden.


**2.3.** **Representation** **engineering** **and** **activation**
**steering**


Representation engineering and activation steering
guide behavior by intervening on intermediate activations, enabling switchable and often interpretable control without retraining. Prior work shows that concepts/intentions can be detected and injected along
activation directions to steer outputs (Zou et al.,
2023; Turner et al., 2024). Yet most studies focus on single concepts or narrow tasks, and rarely
model multi-domain geometry with shared bases plus
domain-specific offsets. Further, representation-level
interventions may not translate to end-to-end behavioral change under strong constraints or adversarial
prompts, since downstream nonlinearities can attenuate injected signals. Taxonomies and systematization efforts improve selectivity and interpretability (Wehner et al., 2025; Bartoszcze et al., 2025), while
conditional control methods refine intervention precision (Lee et al., 2024; Rahn et al., 2024). Most
RepE work targets semantic attributes, whereas agent
tool calling is a parser-defined _discrete_ _mode_ _switch_
with strict executability constraints. Evidence on
RepE for such multi-tool, schema-constrained _tool-_
_mode_ _switching_ is limited; ASA addresses this by
domain-structured directions with confidence gating.


**3.** **Methodology**


This section presents ASA, an inference-time mechanism designed to control whether a pretrained language model enters a tool-invocation execution mode.



3


**ASA:** **Training-Free** **Representation** **Engineering** **for** **Tool-Calling** **Agents**


_Figure_ _2._ **ASA** **overview.** We extract the last-token hidden state at layer _L_ during the pre-fill pass, route the input to
a domain _d_ [ˆ], estimate tool intent probability _p_, construct MoV = _v_ ˆ _d_ [+] _[ βv]_ [global][,] [and] [inject] [∆] _[h]_ [=] [Gate(] _[h]_ [)] _[ ·][ α][ ·]_ [ MoV] [once.]
No further interventions are applied during incremental decoding.



_Table_ _1._ H1 results at _L_ 18: tool intent is nearly perfectly
linearly readable.


Model Layer AUC (Tool-Necessary vs. Non-Tool) Shuffle AUC


Qwen2.5-0.5B-Instruct 18 0.9994 0.4982 [0.4891, 0.5076]
Qwen2.5-1.5B-Instruct 18 0.9996 [0.9987, 1.0000] 0.4966 [0.4884, 0.5053]
Qwen2.5-8B-Instruct 18 0.9989 0.4975 [0.4879, 0.5068]


_Table_ _2._ H3 results: cross-domain interference matrix (normalized diagonal).


Code Math Search Translation


Code 1.00 0.17 0.37 0.42
Math 0.17 1.00 0.29 0.11
Search 0.37 0.29 1.00 0.03
Translation 0.42 0.11 0.03 1.00


ASA is motivated by diagnostic observations about
how tool-use intent is represented and causally expressed in intermediate activations. The method
achieves reversible, low-cost control via a single hiddenstate perturbation applied at a selected intermediate
layer, while leaving backbone parameters unchanged.


**3.1.** **Problem** **definition**


We consider an autoregressive model that maps an
instruction _x_ to an output token sequence _y_ =
( _y_ 1 _, . . ., yT_ ). At generation step _t_, the model produces
logits

_zt_ ( _x, y<t_ ) _∈_ R _[|][V][ |]_ _,_ (1)



_Table_ _3._ H2 results (Qwen2.5-1.5B-Instruct, _L_ 18): injecting the intent direction changes tool-trigger evidence.


_α_ Direction ∆Logit (mean) ∆Prob (mean) _p_ -value (+ _v_ / _−v_ vs. rand)


0.25 + _v_ +0.2077 +1.38% 2 _._ 51 _×_ 10 _[−]_ [36]

0.25 _−v_ -0.2230 -1.41% 1 _._ 89 _×_ 10 _[−]_ [37]

0.25 random -0.0037 +0.11% 

1.00 + _v_ +0.8359 +5.47% 7 _._ 10 _×_ 10 _[−]_ [43]

1.00 _−v_ -0.9414 -5.46% 3 _._ 26 _×_ 10 _[−]_ [44]

1.00 random -0.0459 -0.22% 

where _V_ denotes the vocabulary, and corresponding
probabilities _pt_ = softmax( _zt_ ). Here and below a deterministic parser defines a binary behavioral event


_T_ ( _x_ ) _∈{_ 0 _,_ 1 _},_ (2)


where _T_ ( _x_ ) = 1 if and only if the generated sequence is
interpreted as a valid tool invocation by the parser (for
example by containing a function-call scaffold whose
syntax and arguments are parseable). The operational
objective is to design a compact, portable controller
that, for any input _x_, can increase the probability of
producing a correct tool call when a tool is necessary
while suppressing spurious calls when it is not, without
modifying the model parameters _θ_ .


**3.2.** **Notation** **and** **measurement** **primitives**


Extract the Pre-LN residual-stream representation at
a chosen layer _L_ and at the final non-padding prompt



4


**ASA:** **Training-Free** **Representation** **Engineering** **for** **Tool-Calling** **Agents**



token:

_hL_ ( _x_ ) _∈_ R _[D]_ _,_ (3)


where _D_ is the residual dimension. In experiments we
also standardize each coordinate of _hL_ using trainingset statistics; formally,


( )
_h_ ˜ _L_ ( _x_ ) = Std _hL_ ( _x_ ) = _[h][L]_ [(] _[x]_ [)] _[ −]_ _[µ]_ [train] _,_ (4)

_σ_ train


where _µ_ train and _σ_ train denote per-dimension mean
and standard deviation computed on the router/probe
training partition.


For evaluation of causal influence we measure the mean
change in logits for a set of trigger tokens _S_ . Given an
intervention that maps _hL_ _�→_ _h_ _[′]_ _L_ [,] [define]

[ ]
∆Logit = E _t∈S_ _zt_ [trigger] ( _h_ _[′]_ _L_ [)] _[ −]_ _[z]_ _t_ [trigger] ( _hL_ ) _,_ (5)


where _zt_ [trigger] denotes the logit(s) associated with tokens considered evidence of tool invocation and the
expectation averages over the trigger positions.


**3.3.** **Empirical** **diagnostics** **(motivation**
**summary)**


Three empirical findings justify the ASA design. First,
a lightweight linear classifier trained on _hL_ ( _x_ ) reliably separates samples requiring tool invocation from
those that do not, demonstrating that tool intent is linearly readable in mid-layer activations. Second, a direction derived from class-conditional means produces
a measurable causal effect on early tool-trigger logits
(Eq. (5)), far surpassing norm-matched random perturbations. Third, when intent directions are estimated
separately per domain, the resulting vectors display
partial domain-specific geometry, which implies that
routing to domain-aware directions can reduce crossdomain interference.


**3.4.** **ASA** **architecture** **and** **operations**


ASA composes three lightweight components: a compact set of steering vectors, a multi-class router, and
per-domain intent probes. At inference time ASA performs a single-shot, signed injection into _hL_ ( _x_ ) followed by normal forward propagation. Below we formalize each component and the intervention rule.


3.4.1. Steering vector construction


Using a disjoint calibration split, compute classconditional means in the layer- _L_ hidden space:

[ ]
_µ_ pos = E _hL_ ( _x_ ) _| y_ _[⋆]_ ( _x_ ) = 1 _,_ (6)

[ ]
_µ_ neg = E _hL_ ( _x_ ) _| y_ _[⋆]_ ( _x_ ) = 0 _,_ (7)



where _y_ _[⋆]_ ( _x_ ) is an oracle binary label indicating
whether a tool call is necessary. The global intent vector is defined as


_v_ global = _µ_ pos _−_ _µ_ neg _,_ (8)


where _v_ global _∈_ R _[D]_ points from the non-tool mean
toward the tool-necessary mean. Per-domain vectors
_vd_ are built analogously by restricting expectations to
samples in domain _d_ . After construction, normalize
each vector:

_v_
_v_ ˆ = (9)
_∥v∥_ _[,]_


where _∥· ∥_ denotes the Euclidean norm and _v_ ˆ denotes
the unit-normalized direction used at inference.


3.4.2. Router and probe definitions


A lightweight router maps standardized representations to a domain label. Concretely,



where _W_ [r] _∈_ R _[|D|×][D]_ and _b_ [r] are router parameters estimated on the router training split.


Each domain has a linear probe that outputs an intent
score. For domain _d_ [ˆ],


( )
_p_ ( _x_ ) = _qψ_ [( ˆ] _[d]_ [)][(] _[h][L]_ [(] _[x]_ [))] [=] _[σ]_ _wd_ _[⊤]_ ˆ _[h][L]_ [(] _[x]_ [) +] _[ b]_ [ ˆ] _d_ _,_ (11)


where _σ_ ( _·_ ) is the sigmoid function, and _wd_ ˆ _, b_ ˆ _d_ are fitted
on domain-specific training data. Here _p_ ( _x_ ) estimates
the probability that a tool invocation is appropriate.


3.4.3. Mixture-of-vectors (MoV) composition


Given the router prediction _d_ [ˆ] and the normalized vectors, ASA composes a direction using a domain expert
plus a global offset:


MoV( _hL_ ( _x_ )) = _v_ ˆ _d_ ˆ + _β_ ˆ _v_ global _,_ (12)


where _β_ _≥_ 0 controls the strength of the global intent contribution and both _v_ ˆ _d_ ˆ and _v_ ˆglobal are unitnormalized as in Eq. (9). This modular design lets
ASA scale to new domains by simply adding a new
expert vector _v_ new (and updating the router), without
retraining the backbone, effectively enabling a plugand-play library of domain skills.


3.4.4. Confidence gating and signed injection


To avoid ambiguous injections near decision boundaries, map the probe probability to a ternary control



(
_d_ ˆ = arg max _W_ [r][ ˜] _hL_ ( _x_ ) + _b_ [r][)]
_d∈D_ dom [softmax]



(10)
_d_ _[,]_



5


**ASA:** **Training-Free** **Representation** **Engineering** **for** **Tool-Calling** **Agents**



signal:




+1 _,_ _p_ ( _x_ ) _> τ,_



**Algorithm** **1** ASA single-shot inference (equationreferenced)


**Require:** Frozen model _fθ_, router parameters
( _W_ [r] _, b_ [r] ), per-domain probes _{wd, bd}_, steering
vectors _{v_ ˆglobal _,_ ˆ _vd}_, intervention layer _L_, strength
_α_, global weight _β_, confidence threshold _τ_
1: Run the initial pre-fill forward pass and extract
the last-token hidden state _hL_ ( _x_ ) from the Pre-LN
residual stream.
2: Standardize the representation: compute _h_ [˜] _L_ ( _x_ ) =
Std( _hL_ ( _x_ )) as in Eq. (4).
3: Predict domain label _d_ [ˆ] using the router: _d_ ˆ _←_
arg max _d_ softmax( _W_ [r] _h_ [˜] _L_ ( _x_ ) + _b_ [r] ) _d_ . See Eq. (10).
4: Compute intent probability _p_ ( _x_ ) from the domain
probe: _p_ ( _x_ ) _←_ _σ_ ( _wd_ _[⊤]_ ˆ _[h][L]_ [(] _[x]_ [) +] _[ b]_ [ ˆ] _d_ [).] [See] [Eq.] [(][11][).]
5: Form the routed steering direction MoV( _hL_ ( _x_ )) _←_
_v_ ˆ _d_ ˆ + _β_ ˆ _v_ global as in Eq. (12).
6: Evaluate the ternary gate Gate( _hL_ ( _x_ )) according
to Eq. (13) using threshold _τ_ .
7: Apply the single-shot signed injection:


_h_ _[′]_ _L_ [(] _[x]_ [)] _[←]_ _[h][L]_ [(] _[x]_ [) + Gate(] _[h][L]_ [(] _[x]_ [))] _[ ·][ α][ ·]_ [ MoV(] _[h][L]_ [(] _[x]_ [))] _[,]_


which implements Eq. (14).
8: Continue the forward pass from layer _L_ using
_h_ _[′]_ _L_ [(] _[x]_ [)] [and] [decode] [autoregressively] [(no] [further] [in-]
jections).
9: **return** generated sequence _y_ .


main, evaluates intent via the appropriate probe, composes the steering direction using Eq. (12), computes
the ternary gate in Eq. (13), applies the signed injection in Eq. (14) if warranted, and then resumes the
normal forward computation. The process leaves the
base model parameters untouched and restricts interventions to a single temporal point.


**4.** **Experiments**


In this section, we evaluate ASA for tool-calling domain adaptation, focusing on its effectiveness under
a strict experimental protocol, its controllability enabled by context-aware probe-guided gating, and its
robustness across different model scales. We benchmark against prompt-only variants and a parameterupdate baseline (LoRA) to clarify where ASA sits on
the robustness–efficiency spectrum. All experiments
are conducted on strictly isolated calibration, training, validation, and held-out test splits to prevent data
leakage and to directly measure whether steering can
bridge the representation and behavior gap.Additional
visualizations are provided in Appendix E.



Gate( _hL_ ( _x_ )) =












_−_ 1 _,_ _p_ ( _x_ ) _<_ 1 _−_ _τ,_



(13)



0 _,_ otherwise _,_



where _τ_ _∈_ (0 _._ 5 _,_ 1) is a fixed confidence threshold selected on validation data.


The single-shot intervention applied at layer _L_ is


_h_ _[′]_ _L_ [(] _[x]_ [)] [=] _[h][L]_ [(] _[x]_ [)+Gate(] _[h][L]_ [(] _[x]_ [))] _[·]_ _[α]_ _[·]_ [MoV(] _[h][L]_ [(] _[x]_ [))] _[,]_ [(14)]


where _α ≥_ 0 scales the perturbation magnitude. When
probe is confident that a tool is required the controller
adds the composed steering vector; when the probe
is confident that no tool is needed the controller subtracts the vector; otherwise no modification is made.
The injection occurs only once during the pre-fill pass
and is not repeated at subsequent decoding steps.


**3.5.** **Data** **hygiene** **and** **deployment** **constraints**


To prevent leakage between calibration and evaluation,
ASA uses disjoint data partitions. The calibration
corpus is reserved solely for steering-vector estimation
and is never used to train routers or probes. Router
and probe fitting, hyperparameter selection including
_τ_ and _α_, and final reporting are performed on separate
training/validation/test splits drawn from the benchmark partition. Standardization statistics in Eq. (4)
are computed on the router/probe training split and
applied at inference time.


The ASA asset footprint consists only of the small set
of unit vectors _{v_ ˆ _d} ∪{v_ ˆglobal _}_ and linear predictors
_W_ [r] _, b_ [r] _, {wd, bd}_, making the controller portable and inexpensive to store and transmit.


**3.6.** **Causal** **check** **and** **evaluation** **diagnostics**


As a validation of causal efficacy, one computes the
change in trigger logits under sign-symmetric injections and compares this to random-direction controls
using Eq. (5). Sign-consistent ∆Logit values confirm
that the constructed directions influence early trigger
evidence. Behavior-level metrics such as strict trigger
recall, false positive rate, and post-trigger executability are reported under a deterministic decoding protocol to minimize stochastic variability.


**3.7.** **Inference** **summary**


At runtime the controller is executed as a single,
lightweight forward hook at layer _L_ . The hook standardizes the last-token residual _hL_ ( _x_ ), predicts a do


6


**ASA:** **Training-Free** **Representation** **Engineering** **for** **Tool-Calling** **Agents**


_Table 4._ LLaMA (8B,L=23) neighborhood adaptation (main results). We report triggering Precision/Recall/F1, Accuracy,
and FPR for each domain. **ASA** **(Ours)** reports the best operating point per domain by F1 (from the _α_ sweep).


**Method** **Metric** **Code** **Math** **Search** **Translation** **ALL**



Prompt-only


Baseline



Precision (P) 0.8723 0.6857 0.8584 0.9382 0.8627

Recall (R) 0.2854 0.3528 0.2629 0.9989 0.4988

F1-Score 0.4218 0.4639 0.3957 0.9687 0.6238

Accuracy (Acc.) 0.6358 0.6189 0.6287 0.9658 0.7159

FPR 0.0389 0.1428 0.0367 0.0859 0.0829


Precision (P) 0.8574 0.6368 0.8337 0.9234 0.8407

Recall (R) 0.2508 0.2919 0.2089 0.9988 0.4378

F1-Score 0.3879 0.4008 0.3339 0.9608 0.5759

Accuracy (Acc.) 0.6049 0.5629 0.5839 0.9589 0.6779

FPR 0.0419 0.1669 0.0419 0.0839 0.0839



**4.1.** **Experimental** **Setup** **and** **Metrics**


**Benchmark** **construction.** We evaluate on a 1,600sample multi-domain benchmark spanning Math,
Code, Search, and Translation. Samples are
constructed from public instruction-following and QA
datasets (e.g., Alpaca (Stanford, 2023) and Natural
Questions (Kwiatkowski et al., 2019)). We apply
domain-specific filtering rules to form Tool-Necessary
and Non-Tool pairs, validate tool labels via explicit
_<functioncall>_ markers, and randomly subsample
1,600 instances for evaluation (an engineering choice;
the construction procedure scales to larger corpora).
Detailed training and inference configurations of the
LoRA baseline are provided in Appendix C.4.


**Strict** **protocol** **and** **metrics.** We count a tool call
as _triggered_ iff the output contains _<functioncall>_ .
We report triggering Precision/Recall/F1, Accuracy,
and FPR (Non-Tool trigger rate), plus Success Precision _P_ succ conditioned on triggering: JSON-valid (AST
fallback), schema-consistent (whitelist), and argumentvalid (present, non-empty, format-compliant).We select _L_ by a probe sweep (best val AUC; Fig. 3), tune
_α_ by best val F1 (test sweep in Table 5), and tune _τ_
on val (grid _{_ 0 _._ 50 _,_ 0 _._ 55 _,_ 0 _._ 60 _,_ 0 _._ 65 _,_ 0 _._ 70 _}_ ) then fix it on
test. Routers/probes use only train; vectors use only
CAL.


**4.2.** **Main** **Results** **on** **Two** **Models**


We report results on two instruction-tuned LLMs:
LLaMA (8B) and Qwen2.5-1.5B. Table 4 summarizes



domain-wise triggering performance on LLaMA. For
each domain, ASA reports the best operating point
selected by F1 from the _α_ sweep, and we specially
highlight our results. Table 5 further reports a full _α_
sweep on Qwen2.5-1.5B under the same strict protocol,
together with prompt variants and PEFT baselines,
to situate ASA on the robustness–efficiency spectrum.
ASA consistently improves the trigger-quality tradeoff over both Prompt-only and Baseline across the two
evaluated models (Tables 4, 5). On LLaMA, gains concentrate on domains that are not already saturated,
while false triggers remain controlled; Translation
is near ceiling on this split and thus exhibits limited
headroom. On Qwen2.5-1.5B, prompt-only baselines
either under-trigger (e.g., the system-free setting collapses tool calling) or trade higher recall for substantially more false alarms, underscoring the brittleness
of prompt engineering under strict interfaces. In contrast, ASA improves triggering behavior across a broad
range of steering strengths without inducing structural
collapse: post-trigger validity remains stable, indicating that activation injection primarily modulates the
decision to enter tool mode rather than corrupting formatting or argument construction. This is enabled
by **probe-guided** **dynamic** **gating**, which conditionally opens or suppresses steering based on the current
context, allowing ASA to mitigate the typical recall–
hallucination trade-off.


**Comparison** **across** **adaptation** **paradigms.** Under the same strict protocol (Table 5), prompting
mainly shifts surface instructions and tends to move
along a recall–false-trigger frontier without reliably



7


**ASA:** **Training-Free** **Representation** **Engineering** **for** **Tool-Calling** **Agents**


_Table_ _5._ Results on the MTU-Bench test set (Qwen2.5-1.5B, _L_ =18). ASA (Ours) applies probe-guided dynamic gating
for all _α_ ; we report **F1** as primary metric . Here _Trig._ _Prec._ denotes precision of the tool-mode triggering decision, while
post-trigger validity (Format/ **Exec.** **Prec.** /Args) measures executability conditional on triggering, where **Exec.** **Prec.** is
defined as the ratio of samples with both valid format and tool name to the total triggered samples.


Triggering Post-trigger validity Cost Rel. vs. baseline
_α_ Method Branch

Trig. Prec. Rec. **F1** Acc. FPR Format **Exec.** **Prec.** Args Storage Train ∆ **F1** ∆Prec ∆FPR


**Prompt** **variants**
Prompt: no_system 0.0000 0.0000 0.0000   - 0.0000   -   -   - 0 No -100.00% -100.00% -100.00%
Prompt: few_shot_system 0.4348 0.2083 0.2817   - 0.2708 0.8200 0.3826 0.8000 0 No +54.95% -1.18% +85.73%


**PEFT** **baselines**
LoRA (Rank-16) (Hu et al., 2022) 0.5600 0.5833 0.5714   - 0.4583 0.6500 0.2240 0.6300 _∼_ 19MB Yes +214.30% +27.27% +214.33%
LoRA (Rank-8) (Hu et al., 2022) 0.4800 0.4500 0.4643   - 0.5200 0.5800 0.1920 0.5600 _∼_ 10MB Yes +155.39% +9.09% +256.65%


Prefix-Tuning (Li & Liang, 2021) 0.6174 0.2041 0.3029   - 0.1074 0.8111 0.4405 0.8425 _∼_ 15MB Yes +48.76% +4.63% -4.58%
BitFit (Zaken et al., 2022) 0.5873 0.1702 0.2564   - 0.1343 0.7432 0.4323 0.8146 _∼_ 8MB Yes +58.98% +8.49% -8.93%
Q-LoRA (Dettmers et al., 2023) 0.7328 0.3154 0.4696   - 0.1193 0.8432 0.4898 0.8922 _∼_ 18MB Yes +79.86% +23.35% -14.21%


**Vector** **injection**
Baseline (zero_shot_system) 0.4400 0.1146 0.1818 0.4844 0.1458 1.0000 0.4000 0.9900 0 No   -   -   0.5 ASA (Ours) steer 0.4615 0.1250 0.1967 0.4896 0.1458 0.9700 0.4231 0.9600 _∼_ 20KB No +8.20% +4.89% +0.00%
1.0 ASA (Ours) steer 0.5937 0.1979 0.2969 0.5312 0.1354 0.9400 0.5625 0.9300 _∼_ 20KB No +63.31% +34.93% -7.13%
2.0 ASA (Ours) steer 0.7805 0.3333 0.4672 0.6198 0.0937 0.8900 0.7073 0.8800 _∼_ 20KB No +156.99% +77.39% -35.73%
3.0 ASA (Ours) steer 0.7778 0.3646 0.4965 0.6302 0.1042 0.8600 0.6667 0.8500 _∼_ 20KB No +173.10% +76.77% -28.53%
**4.0** **ASA** **(Ours)** steer **0.8718** **0.3542** **0.5037** **0.6510** **0.0521** 0.8800 **0.6923** 0.8700 _∼_ 20KB No **+177.06%** **+98.14%** **-64.27%**



closing the representation–behavior gap. PEFT baselines such as LoRA can attain strong triggering metrics
by updating model weights, but incur non-trivial training/storage overhead and often amplify false triggers;
lighter PEFT variants typically preserve post-trigger
validity but struggle to recover recall, while quantized
variants remain training-dependent. ASA instead offers a _training-free_ operating knob with low overhead,
achieving competitive triggering behavior while maintaining executability, suggesting its primary effect is
targeted control of tool-mode entry rather than improving format compliance alone.


**Scaling** **behavior.** Across model scales, the optimal
intervention depth shifts with capacity (e.g., L18 _→_
L21), consistent with layer-depth drift under scaling.
More importantly, ASA transfers when the base model
already possesses tool-calling capability and thus has
a latent circuit to amplify; it cannot “create” tool-use
behavior from scratch. See Appendix E (Table 14) for
the full scaling summary.


**4.3.** **Ablation** **Study**


We ablate ASA at _α_ = 4 _._ 0 to confirm Table 6 gains are
from structured control (not incidental perturbations).
**ASA** **(full)** gives the best balance. Removing the
probe-guided gate (No gate) makes injection unconditional and blows up false triggers (FPR = 0 _._ 5000),
showing the gate is the key safety valve on Non-Tool
inputs. A norm-matched Random direction does not
help, ruling out a pure “perturbation energy” effect.
Composition matters: Global only is strong but less
selective, while Domain only is often insufficient to reliably enter tool mode. Mismatch hurts schema consis


_Table_ _6._ Ablation study on test set (Qwen2.5-1.5B, Layer
18, _α_ = 4 _._ 0). **Oracle** **Router** uses the ground-truth domain label for domain-vector selection (ideal router with
100% domain accuracy).


Mode Prec. Rec. FPR Tool acc.


Baseline 0.4400 0.1146 0.1458 0.9600
ASA (full) 0.8718 0.3542 0.0521 0.7436
Oracle Router 0.9714 0.3542 0.0104 0.8000
Global only 0.8261 0.3958 0.0833 0.6957
Domain only 0.3636 0.1250 0.2188 0.7576
No gate 0.4217 0.3646 0.5000 0.7229
Random 0.5556 0.1042 0.0833 0.9444
Mismatch 0.7885 0.4271 0.1146 0.6346


tency, reflected by lower tool-name accuracy. Oracle
Router (ground-truth domains) further reduces FPR
to 0 _._ 0104, indicating routing headroom. **We** **also** **re-**
**port** **the** **same** **ablation** **pattern** **on** **LLAMA** **in**
**Appendix** **F,** **again** **highlighting** **the** **necessity** **of**
**gating.** LoRA adapters are trained via standard supervised fine-tuning on the same CAL split; full training and generation details are in Appendix C.4.


**5.** **Conclusion**


ASA provides a training-free, inference-time control
layer for tool-calling domain adaptation, bridging the
representation–behavior gap where tool intent is decodable but fails to trigger under strict interfaces. On
MTU-Bench, single-shot routed steering with probeguided gating boosts strict tool-use F1 (higher recall,
lower FPR) while preserving output validity.



8


**ASA:** **Training-Free** **Representation** **Engineering** **for** **Tool-Calling** **Agents**



**Impact** **Statement**


This paper presents work on activation steering for
tool-calling domain adaptation. The goal is to advance machine learning by improving controllability of
large language model agents. Our approach enables
reliable tool-calling across domains without parameter
updates, potentially reducing deployment costs and
improving AI safety through better behavioral control. However, the ability to bidirectionally control
tool invocation raises dual use concerns, as adversarial actors might exploit similar mechanisms to suppress safety critical tool calls or evade monitoring systems. We urge researchers to investigate safeguards
against unauthorized activation steering. Societal consequences include more robust AI assistants but also
potential misuse of steering techniques for deceptive
behavior.


**References**


Bartoszcze, L., Munshi, S., Sukidi, B., Yen, J., Yang,
Z., Williams-King, D., Le, L., Asuzu, K., and Maple,
C. Representation engineering for large-language
models: Survey and research challenges. _arXiv_
_preprint_ _arXiv:2502.17601_, 2025.


Dang, H., Liu, T., Wu, Z., Yang, J., Jiang, H., Yang,
T., Chen, P., Wang, Z., Wang, H., Li, H., et al.
Improving large language models function calling
and interpretability via guided-structured templates.
In _Proceedings_ _of_ _the_ _2025_ _Conference_ _on_ _Empirical_
_Methods in Natural Language Processing_, pp. 24437–
24453, 2025.


Dettmers, T., Pagnoni, A., Holtzman, A., and Zettlemoyer, L. Qlora: Efficient finetuning of quantized
llms. _arXiv_ _preprint_ _arXiv:2305.14314_, 2023. doi:
10.48550/arXiv.2305.14314.


Hu, E. J., Shen, Y., Wallis, P., Allen-Zhu, Z., Li, Y.,
Wang, S., Wang, L., Chen, W., et al. Lora: Lowrank adaptation of large language models. _ICLR_, 1
(2):3, 2022.


Johnson, R. T., Pain, M. D., and West, J. D. Natural language tools: A natural language approach to
tool calling in large language agents. _arXiv_ _preprint_
_arXiv:2510.14453_, 2025.


Kwiatkowski, T., Palomaki, J., Redfield, O., Collins,
M., Parikh, A., Alberti, C., Epstein, D., Polosukhin,
I., Devlin, J., Lee, K., et al. Natural questions: a
benchmark for question answering research. _Trans-_
_actions_ _of_ _the_ _Association_ _for_ _Computational_ _Lin-_
_guistics_, 7:453–466, 2019.



Lee, B. W., Padhi, I., Ramamurthy, K. N., Miehling,
E., Dognin, P., Nagireddy, M., and Dhurandhar,
A. Programming refusal with conditional activation
steering. _arXiv_ _preprint_ _arXiv:2409.05907_, 2024.


Li, X. L. and Liang, P. Prefix-tuning: Optimizing
continuous prompts for generation. _arXiv_ _preprint_
_arXiv:2101.00190_, 2021.


Lu, W., Luu, R. K., and Buehler, M. J. Fine-tuning
large language models for domain adaptation: Exploration of training strategies, scaling, model merging and synergistic capabilities. _npj_ _Computational_
_Materials_, 11(1):84, 2025.


Patil, S. G., Zhang, T., Wang, X., and Gonzalez, J. E.
Gorilla: Large language model connected with massive apis. _Advances_ _in_ _Neural_ _Information_ _Process-_
_ing_ _Systems_, 37:126544–126565, 2024.


Prottasha, N. J., Mahmud, A., Sobuj, M. S. I.,
Bhat, P., Kowsher, M., Yousefi, N., and Garibay,
O. O. Parameter-efficient fine-tuning of large language models using semantic knowledge tuning. _Sci-_
_entific_ _Reports_, 14(1):30667, 2024.


Prottasha, N. J., Chowdhury, U. R., Mohanto, S.,
Nuzhat, T., Sami, A. A., Ali, M. S., Sobuj, M.
S. I., Raman, H., Kowsher, M., and Garibay, O. O.
Peft a2z: Parameter-efficient fine-tuning survey for
large language and vision models. _arXiv_ _preprint_
_arXiv:2504.14117_, 2025.


Qin, Y., Liang, S., Ye, Y., Zhu, K., Yan, L., Lu, Y.,
Lin, Y., Cong, X., Tang, X., Qian, B., et al. Toolllm:
Facilitating large language models to master 16000+
real-world apis. _arXiv_ _preprint_ _arXiv:2307.16789_,
2023.


Rahn, N., D’Oro, P., and Bellemare, M. G. Controlling
large language model agents with entropic activation
steering. _arXiv_ _preprint_ _arXiv:2406.00244_, 2024.


Schick, T., Dwivedi-Yu, J., Dessì, R., Raileanu, R.,
Lomeli, M., Hambro, E., Zettlemoyer, L., Cancedda,
N., and Scialom, T. Toolformer: Language models can teach themselves to use tools. _Advances_ _in_
_Neural_ _Information_ _Processing_ _Systems_, 36:68539–
68551, 2023.


Shinn, N., Cassano, F., Gopinath, A., Narasimhan, K.,
and Yao, S. Reflexion: language agents with verbal
reinforcement learning. In _Advances_ _in_ _Neural_ _In-_
_formation_ _Processing_ _Systems_ _36_ _(NeurIPS_ _2023)_,
2023.


Stanford, C. Alpaca: a strong, replicable instructionfollowing model, 2023.



9


**ASA:** **Training-Free** **Representation** **Engineering** **for** **Tool-Calling** **Agents**


Tang, Q., Deng, Z., Lin, H., Han, X., Liang, Q., Cao,
B., and Sun, L. Toolalpaca: Generalized tool learning for language models with 3000 simulated cases.
_arXiv_ _preprint_ _arXiv:2306.05301_, 2023.


Turner, A. M., Thiergart, L., Leech, G., Udell, D.,
Mini, U., and MacDiarmid, M. Activation addition: Steering language models without optimization. 2024.


Wang, G., Xie, Y., Jiang, Y., Mandlekar, A., Xiao,
C., Zhu, Y., Fan, L., and Anandkumar, A. Voyager:
An open-ended embodied agent with large language
models, 2023. 2023.


Wehner, J., Abdelnabi, S., Tan, D., Krueger, D.,
and Fritz, M. Taxonomy, opportunities, and challenges of representation engineering for large language models. _arXiv_ _preprint_ _arXiv:2502.19649_,
2025.


Wu, Z., Arora, A., Wang, Z., Geiger, A., Jurafsky,
D., Manning, C. D., and Potts, C. Reft: Representation finetuning for language models. In _Ad-_
_vances in Neural Information Processing Systems 38_
_(NeurIPS_ _2024)_, 2024.


Xi, Z., Chen, W., Guo, X., He, W., Ding, Y., Hong,
B., Zhang, M., Wang, J., Jin, S., Zhou, E., et al.
The rise and potential of large language model based
agents: A survey. _Science_ _China_ _Information_ _Sci-_
_ences_, 68(2):121101, 2025.


Yao, S., Zhao, J., Yu, D., Du, N., Shafran, I.,
Narasimhan, K. R., and Cao, Y. React: Synergizing reasoning and acting in language models. In _The_
_eleventh_ _international_ _conference_ _on_ _learning_ _repre-_
_sentations_, 2022.


Zaken, E. B., Goldberg, Y., and Ravfogel, S.
Bitfit: Simple parameter-efficient fine-tuning for
transformer-based masked language-models. In _Pro-_
_ceedings_ _of_ _the_ _60th_ _Annual_ _Meeting_ _of_ _the_ _Asso-_
_ciation_ _for_ _Computational_ _Linguistics_ _(Volume_ _2:_
_Short_ _Papers)_, pp. 1–9, 2022.


Zou, A., Phan, L., Chen, S., Campbell, J., Guo, P.,
Ren, R., Pan, A., Yin, X., Mazeika, M., Dombrowski, A.-K., et al. Representation engineering:
A top-down approach to ai transparency. _arXiv_
_preprint_ _arXiv:2310.01405_, 2023.


10


**ASA:** **Training-Free** **Representation** **Engineering** **for** **Tool-Calling** **Agents**


**A.** **Appendix** **Overview**


This appendix complements the main paper with four components. Appendix B explains why intent may be
strongly decodable in representation space yet fail to reliably manifest as tool-entry behavior under strict interface
constraints. Appendix C specifies datasets, splits, models, decoding, interventions, and metric definitions for
faithful replication. Appendix D defines deterministic trigger and validation rules so that the behavioral event
_T_ ( _x_ ) is auditable. Appendix E provides additional results referenced but not expanded in the main text, including
cross-model probe decodability, logit-lens causality tables, cross-domain interference matrices, prompt baselines,
scaling summaries, and efficiency comparisons.


**B.** **Theoretical** **Analysis:** **From** **Representation** **to** **Behavior**


**B.1.** **Problem** **setup** **and** **the** **representation–behavior** **gap**


We study tool calling as an _auditable_ _discrete_ _event_ under strict interface constraints. Given an instruction _x_,
the agent produces a string output. A deterministic parser maps the output to a binary event _T_ ( _x_ ) _∈{_ 0 _,_ 1 _}_ that
indicates whether tool mode is entered. Importantly, the parser defines a _hard_ _boundary_ (e.g., the appearance of
_<functioncall>_ and a valid payload), so small changes in decoding can flip _T_ ( _x_ ) discontinuously.


Many LLMs encode tool intent in hidden states: a linear probe on a mid-layer residual stream can separate
Tool-Necessary vs Non-Tool with near-perfect AUC (see Appendix E, Table 10). However, a high-AUC intent
signal does _not_ imply reliable tool-entry behavior, because behavior requires the model to emit a very specific
string pattern and schema-compliant JSON under decoding constraints.


**B.2.** **Why** **strong** **intent** **decodability** **may** **not** **translate** **into** **tool** **entry**


We highlight three failure mechanisms.


**(i)** **Discrete** **parser** **boundary** **and** **early-token** **competition.** Tool entry often depends on _very_ _early_
generation decisions that determine whether the model commits to _<functioncall>_ . Even if later-layer representations encode intent, the output may remain in natural language if the early-token logit competition is not
sufficiently biased. This motivates _mid-layer_ _causal_ _control_ that affects the early distribution over trigger tokens,
rather than post-hoc formatting.


**(ii)** **Interface** **constraints** **amplify** **small** **formatting** **errors.** A model can be “toolish” but still fail strict
validators: invalid JSON, wrong tool name (schema mismatch), or missing/empty arguments are all treated as
failures in deployment. Therefore, any method must improve not only trigger rate but also _post-trigger_ _validity_ .


**(iii)** **Prompt/schema** **fragility** **under** **protocol** **evolution.** Prompt constraints are implemented at the
input level; they can be brittle under distribution shifts, context budget changes, and evolving tool schemas.
Demonstrations may increase recall but often increase false triggering on Non-Tool inputs, yielding a poor
precision–FPR trade-off (Appendix E, Table 13).


**B.3.** **Implication** **for** **method** **design**


The analysis motivates the design of a representation-level controller that is _selective_ to avoid spurious triggers through probe-guided gating and _domain-structured_ to reduce cross-domain interference (see Appendix E,
Table 12). The need for selectivity is informed by findings on trigger token competition (Appendix E, Table 11).


**C.** **Experimental** **Protocol** **for** **Reproducibility**


**C.1.** **Datasets** **and** **splits**


We evaluate tool-mode triggering on the REST test set under a strict parser. We compute intervention directions
using a calibration set (CAL) that is disjoint from test. For the MoV vector construction, we use the MOV dataset
(320 samples) to estimate mean differences between Tool-Necessary and Non-Tool hidden states.


11


**ASA:** **Training-Free** **Representation** **Engineering** **for** **Tool-Calling** **Agents**


_Table_ _7._ ASA configuration and evaluation protocol.


**Item** **Setting**


Training paradigm Training-free (statistics only)
Vector construction MOV (320 samples), _µ_ pos _−_ _µ_ neg
Stored parameters _∼_ 20 KB (steering vectors + probe weights)
Inference overhead Single vector addition
Compute resource Single RTX 4090 ( _<_ 24GB VRAM)
Prompt template _GLOBAL_SYSTEM_PROMPT_
Prompt structure Strict System/User/Assistant alignment
Test isolation Test set excluded from all statistics/training
Parser Deterministic _parse_functioncall_
Parsing logic _<functioncall>_ tag + JSON / _ast.literal_eval_ fallback
Decoding Greedy ( _do_sample=False_ )
Max new tokens 128
Padding side Left
Random seed 42 (others within _±_ 3%)


_Table_ _8._ Deterministic trigger and validation rules used in this paper.


Component Rule


Tool-mode entry Trigger iff _<functioncall>_ appears anywhere in the output
Syntactic validity Payload inside tags is JSON-parseable (AST fallback allowed)
Schema consistency _name_ must belong to the domain-specific whitelist
Argument integrity _arguments_ exists, non-empty, and format-compliant


**C.2.** **Models** **and** **decoding**


We primarily use Qwen2.5-1.5B-Instruct; we additionally report generalization to Qwen2.5-8B-Instruct and (optionally) a LLAMA-family backbone. Decoding uses greedy generation (do_sample=False) to minimize variance
in _T_ ( _x_ ) and make parser outcomes deterministic.


**C.3.** **Intervention** **definition**


Let _hℓ_ ( _x_ ) denote the residual-stream representation at a selected depth _ℓ_ (selected by a probe sweep; Figure 3).
ASA injects an intent-aligned direction _v_ scaled by _α_, optionally composed from a global component and a
domain expert component. A probe-guided gate determines whether to apply + _v_, apply _−v_ (suppress), or do
nothing.


**C.4.** **Metrics**


We report trigger-level Precision/Recall/F1/FPR, and post-trigger validity (format/tool-name/args accuracy)
under strict validators. Success metrics summarize executability after parsing and schema checks.


This table pins down the methods operational definition, preventing hidden degrees of freedom. Two protocol
elements are particularly load-bearing. First, test isolation ensures directions are computed only from CAL/MOV,
avoiding optimistic bias from leaking evaluation patterns into steering statistics. Second, deterministic parsing
plus greedy decoding makes _T_ ( _x_ ) stable: improvements cannot be explained by sampling variance or ambiguous
scoring. Together, these constraints ensure reported gains correspond to genuine improvements in controllable
tool entry and executability under a deployment-like interface.


**D.** **Deterministic** **Parsing** **and** **Validation** **Rules**


We define a strict, deterministic evaluator so that tool calling is auditable. Tool-mode entry is triggered iff
_<functioncall>_ appears anywhere in the output. After triggering, we validate payload parseability and schema
compliance.


12


**ASA:** **Training-Free** **Representation** **Engineering** **for** **Tool-Calling** **Agents**


_Table_ _9._ Intervention sites and limitations relevant to behavior control under strict tool-mode parsing.


Method Intervention site Form Key limitation


Prompt / schema Input _X_ do( _X_ := _X_ _[′]_ ) Fragile; may suppress tools via overconstraint
Hidden injection Mid-layer _Hℓ_ _[⋆]_ _Hℓ_ _[⋆]_ := _Hℓ_ _[⋆]_ + ∆ _h_ Can raise recall but often raises FPR without gating
ASA (MoV + gate) Mid-layer _Hℓ_ _[⋆]_ Conditional ∆ _h_ ( _x_ ) Depends on intent evidence / routing accuracy
PEFT (LoRA/SFT) Parameters _θ_ _θ_ := _θ_ + ∆ _θ_ Costly retraining; maintenance under
churn


_Table_ _10._ Cross-model probe AUC at a fixed mid layer (Layer 18) (tool intent vs Non-Tool).


Model Layer AUC p-value


Qwen2.5-0.5B-Instruct L18 0.9994 _<_ 0 _._ 001
Qwen2.5-1.5B-Instruct L18 0.9996 _<_ 0 _._ 001
Qwen2.5-8B-Instruct L18 0.9989 _<_ 0 _._ 001


_Table_ _11._ Logit-Lens intervention on Qwen2.5-1.5B at Layer 18 (target token: _<functioncall>_ ). Reported p-values
compare + _v_ vs random.


_α_ Mode ∆Logit (mean) ∆Prob (mean) p-value


0.25 Plus (+ _v_ ) +0.2077 +1.38% 2 _._ 51 _×_ 10 _[−]_ [36]

0.25 Minus ( _−v_ ) -0.2230 -1.41% 0.25 Random -0.0037 +0.11% 

1.0 Plus (+ _v_ ) +0.8359 +5.47% 7 _._ 10 _×_ 10 _[−]_ [43]

1.0 Minus ( _−v_ ) -0.9414 -5.46% 1.0 Random -0.0459 -0.22% 

These rules separate two post-trigger failure modes: wrong tool selection (schema mismatch) and non-executable
calls (e.g., missing, empty, or invalid arguments). This decomposition is essential for interpreting recall/FPR
trade-offs: while a method may increase trigger frequency, it can simultaneously degrade executability. Under
these validators, such degradation is penalized in success precision, even if trigger-level recall improves. Consequently, performance gains under this protocol more closely reflect true deployment value than do relaxed
evaluations that accept tool-like natural language.


**E.** **Additional** **Results** **and** **Visualizations**


The control locus determines reliability under a discrete parser boundary. Prompt methods intervene at _X_
and are sensitive to phrasing and context budget; they can improve apparent compliance by suppressing tool
entry, reducing recall. Unconditional hidden injections move the logit competition but are not selective, often
increasing both recall and FPR. ASA adds selectivity via probe-guided gating and domain-structured directions,
targeting a better recall–FPR Pareto point. PEFT can be strong but is operationally expensive under API churn,
motivating training-free steering.


Near-saturated AUC across scales shows tool intent is linearly accessible in mid-layer representations and is
largely scale-invariant. However, high AUC should not be conflated with correct tool calls: behavior requires
emitting a strict pattern and schema-valid JSON. This gap motivates using the probe as a _controller_ (gating
signal) rather than assuming intent decodability implies reliable tool entry.


This is a causal signature: increasing _α_ along + _v_ raises the trigger-token logit/probability, while _−v_ suppresses it,
and random directions do not replicate the effect. Therefore _v_ is intent-aligned rather than an “energy injection”
artifact. Crucially, this evidence addresses _steerability_ but not _selectivity_ : without gating, the same causal push
can spuriously trigger on Non-Tool inputs, inflating FPRhence the need for probe-guided conditional control.


13


**ASA:** **Training-Free** **Representation** **Engineering** **for** **Tool-Calling** **Agents**


_Table_ _12._ Cross-domain interference matrix (cosine similarity) between domain intent vectors.


Domain Code Math Search Translation


Code 1.00 0.17 0.37 0.42
Math 0.17 1.00 0.29 0.11
Search 0.37 0.29 1.00 0.03
Translation 0.42 0.11 0.03 1.00


_Table_ _13._ Prompt baselines without ASA vector injection.


Variant Recall (Tool=1) FPR (Tool=0) Note


Zero-shot System 0.1146 0.1458 Prompt-only baseline under strict triggering
Few-shot System 0.2083 0.2708 Higher recall but substantially higher false
triggers
No System 0.0000 0.0000 Tool mode collapses without system specification


_Table_ _14._ Scaling summary across model sizes.


Model Status Best config Observed behavior Conclusion


0.5B Fail - Recall= 0, FPR= 0 Steering cannot create tool
ability if missing
1.5B Success L18, _α_ = 4 _._ 0 Recall _↑_, FPR _↓_ Sweet spot: rich semantics
and controllability
8B Success L21, _α_ = 3 _._ 0 F1: 0.38 _→_ 0.64 Layer drift; gains after retuning


_Table_ _15._ Qwen2.5-8B-Instruct: baseline vs ASA at Layer 21, _α_ = 3 _._ 0.


Metric Baseline ASA (steer) ∆


Precision 0.5179 0.8500 +0.3321
Recall 0.3021 0.5132 +0.2111
F1 0.3816 0.6400 +0.2584
Accuracy 0.5104 0.7083 +0.1979
FPR 0.2812 0.0625 -0.2187


Diagonal dominance indicates domain directions are distinct, supporting a modular representation of tool intent.
Very low similarities (e.g., Search vs Translation) imply near-orthogonal subspaces; a single global direction would
inject irrelevant components, likely causing wrong tool names or malformed arguments. Moderate overlaps
suggest partial shared structure but not enough to justify a one-size-fits-all direction. This motivates MoV
routing: selecting domain experts reduces cross-domain leakage and should improve post-trigger schema validity.


Prompting alone struggles under strict parsing. Few-shot increases recall but also increases FPR, indicating
pattern-overgeneralization: the model learns tool-like behavior that leaks into Non-Tool contexts. No-system
collapse shows the system message is part of the interface contract; without it, the model fails to enter tool mode
at all. This supports the claim that input-level methods are brittle under protocol evolution and distribution
shifts.


Scaling separates _capability_ from _control_ . On 0.5B, the model does not implement tool calling robustly, so
steering cannot induce correct tool mode. On 1.5B, mid-layer intervention yields higher recall with lower FPR,
indicating intent is both readable and behaviorally pliable. On 8B, the optimal depth shifts deeper, consistent
with semantic decision boundaries moving with scale; re-selecting _ℓ_ is essential for transfer.


Both precision and recall improve while FPR drops sharply, indicating selective control rather than indiscriminate
triggering. The FPR reduction implies the gate (and/or better depth alignment) suppresses spurious tool-mode


14


**ASA:** **Training-Free** **Representation** **Engineering** **for** **Tool-Calling** **Agents**


_Table_ _16._ Storage/parameter footprint comparison.


Method Stored artifacts Footprint


ASA (vectors + router) _{v_ global _, v_ domain _}_ + lightweight router _∼_ 20 KB
LoRA (rank-16, REST train) LoRA adapters (rank-16) _∼_ 19 MB


_Figure_ _3._ Layer-wise probe sweep used to select the intervention depth.


MOV Calibration Set: L18 Hidden Space PCA Projection



0.06


0.04


0.02


0.00


-0.02


-0.04


-0.06



Effect of Logit-Lens Steering on Function-Call Probability





20


15


10


5


0


5



|Col1|Col2|Col3|Col4|Col5|Col6|code<br>math<br>search|
|---|---|---|---|---|---|---|
|||||||translation<br>Non-tool<br>~~Tool~~|
|||||||Global vector|
||||||||
||||||||
||||vglobal||||
||||||||
||||||||
||0|5<br>||1|1|0|


PC1









|p|< 0.00+1 vv sd. iCreocnttriooln (|Tar|get)|Col5|Col6|Col7|
|---|---|---|---|---|---|---|
|~~(B~~|~~onferroni corrected)~~<br> <br> direction|~~onferroni corrected)~~<br> <br> direction|<br> n (Control)||~~0.~~|~~55~~<br>~~**~~|
||||0.0<br>|0.0<br>|28<br>***||
||~~0.~~<br>0.0|~~0.~~<br>0.0|~~14~~<br>01<br>-0.<br>~~***~~|~~14~~<br>01<br>-0.<br>~~***~~|001<br>~~-0.~~|~~02~~|
||-0.|-0.|014<br>|014<br>|Increased<br>probability||
||||-0.|-0.|029||
||||||||
||||||~~-0.~~|~~55~~|


Steering Coefficient











_Figure_ _4._ Combined geometry and causal diagnostic at the selected layer.


entry on Non-Tool inputs. Meanwhile recall gains show Tool-Necessary inputs are pushed across the strict
trigger boundary. The combined effect yields a strong F1 improvement and validates transfer at scale after
depth re-tuning.


The KB-vs-MB footprint gap is decisive under API/tool churn. ASA stores only a few directions and a lightweight
controller, making versioning and redeployment cheap. LoRA introduces persistent adapter weights and typically requires retraining/revalidation when schemas change, increasing maintenance cost. Thus, ASA targets
a deployment regime where meaningful behavioral gains are achieved with minimal storage and no gradient
updates.


**Discussion of Figure 3.** Figure 3 defines the depth selection criterion: we choose _ℓ_ where validation separability
peaks (or forms a stable plateau), indicating a well-formed intent boundary. Intervening too early can be “presemantic” and unstable; intervening too late can reduce controllability because downstream transformations are
constrained by decoding dynamics. Fixing _ℓ_ based on validation prevents test overfitting and ensures steering
results reflect a principled depth choice rather than post-hoc tuning.


**Discussion** **of** **Figure** **4.** In Figure 4, the geometry component supports a structured representation where Tool


15


**ASA:** **Training-Free** **Representation** **Engineering** **for** **Tool-Calling** **Agents**


Active Steering Performance Across Domains



1.0


0.8


0.6


0.4


0.2


0.0



(a) F1 Score vs Steering Strength

|Domain|Col2|Col3|Col4|Col5|Col6|Col7|Col8|Col9|Col10|Col11|Col12|Col13|Col14|Col15|Col16|Col17|Col18|Col19|Col20|Col21|Col22|Col23|Col24|Col25|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|ALL<br>Math<br>~~Code~~|ALL<br>Math<br>~~Code~~|ALL<br>Math<br>~~Code~~|||||||||||||||||||||||
|Sear<br>|Sear<br>|Sear<br>|ch<br>||||||||||||||||||||||
|Tran|Tran|Tran|la|la|la|la|la|la|la|la|la|la|la||||||||||||
||||||||||||||||||||||||||
||||||||||||||||||||||||||
||||||||||||||||||||||||||
||||||||||||||||||||||||||



0 1.0 2.0 3.0 4.0 5.0
Steering Strength ( )



1.0


0.8


0.6


0.4


0.2


0.0



(b) Recall vs Steering Strength


0 1.0 2.0 3.0 4.0 5.0
Steering Strength ( )



_Figure_ _5._ Active steering performance on REST: domain-wise trends versus intervention strength _α_ .



(a) F1 Score





1.0


0.9


0.8


0.7


0.6


0.5


0.4


0.3







1.0


0.9


0.8


0.7


0.6


0.5


0.4


0.3


0.2






|Col1|Col2|Col3|Col4|Col5|Col6|Col7|Col8|
|---|---|---|---|---|---|---|---|
|||||||||
|||||||||
|||||||||
|||||||||
||||||Code|Translati|on|
||||||Math<br>Search|ALL||


|Col1|Col2|Col3|(b) Recall|Col5|Col6|Col7|Col8|
|---|---|---|---|---|---|---|---|
|||||||||
|||||||||
|||||||||
|||||||||
|||||||||
|||||||||
||||||Code|Translati|on|
||||||Math<br>~~Search~~|ALL||



0 1 2 3 4 5
Steering Strength ( )



0 1 2 3 4 5
Steering Strength ( )



_Figure_ _6._ REST: F1/Recall curves across domains under different steering strengths _α_ .


vs Non-Tool (and often domains) occupy separable regions; this motivates domain-structured experts rather than
a single global direction. The causal component shows direction-specific control (aligned vs anti-aligned effects)
and rejects the “random energy” explanation. Together, Figure 4 justifies two key design choices: intent-aligned
vectors exist and are causally meaningful, but selectivity is still required to avoid spurious triggers.


**Discussion** **of** **Figure** **5.** Figure 5 visualizes the operating-point movement induced by _α_ . Low _α_ is insufficient
to consistently reorder early decoding decisions, limiting recall improvements. Moderate _α_ increases the chance
that Tool-Necessary inputs cross the strict trigger boundary, improving recall/F1. Overly large _α_ can dominate
downstream computation, increasing spurious triggers or schema instability; this is exactly where probe-guided
gating is necessary to preserve precision and control FPR.


**Discussion** **of** **Figure** **6.** The curves in Figure 6 reveal domain-dependent sensitivity to _α_ . Some domains
saturate recall quickly (strong intrinsic tool prior), while others require larger _α_ but risk higher FPR or posttrigger errors. This heterogeneity in Figure 6 argues against a single global setting and supports routing + gating:
the intervention should be conditioned on domain and intent confidence to reach each domains best operating
region.


**Discussion** **of** **Figure** **7.** Reporting the best per-domain operating point in Figure 7 prevents aggregate metrics
from hiding domain regressions. The selected _α_ also indicates “control difficulty”: domains requiring larger _α_
likely have weaker natural trigger evidence under strict parsing. This supports the need for conditional control:
rather than brute-force amplification, gating can preserve precision while still enabling recall gains where needed.


**Discussion** **of** **Figure** **8.** The heatmap in Figure 8 makes the global trade-off explicit: recall often rises with _α_


16


|Col1|Col2|Col3|Col4|Col5|Col6|Col7|Col8|Col9|Col10|Col11|Col12|Col13|Col14|Col15|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
||||||||||||||||
|+48%<br>~~( =5)~~|+48%<br>~~( =5)~~|+48%<br>~~( =5)~~|+48%<br>~~( =5)~~|+48%<br>~~( =5)~~||+83%<br>( =2)|+83%<br>( =2)|+83%<br>( =2)|+83%<br>( =2)||||||
||||||||||||||||
||||||||||||||||
||||||||||||||||
||||||||||||||||
||||||||||||||||


Code Math Search Trans. ALL


_Figure_ _7._ REST: F1 improvement at the best operating point per domain (annotated with the selected _α_ ).



Precision


Recall


F1


Accuracy



Global (ALL Domains) Performance

|0.84 0.84 0.88 0.92 0.90 0.91<br>0.44 0.49 0.53 0.60 0.69 0.72<br>0.58 0.62 0.66 0.73 0.78 0.80<br>0.68 0.70 0.73 0.78 0.81 0.82|Col2|Col3|Col4|Col5|Col6|Col7|
|---|---|---|---|---|---|---|
||||||||



_Figure_ _8._ REST (ALL domains): global metrics as a function of _α_ .



1.0


0.9


0.8


0.7


0.6


0.5


0.4



up to a point, but precision can degrade if FPR increases. Therefore, “bigger _α_ ” is not optimal; the best region
is where recall gains do not trigger a disproportionate increase in spurious tool-mode entries. This emphasizes
why we report both recall and FPR and tune _α_ on validation rather than maximizing trigger frequency.


**F.** **Ablation** **Studies**


Full ASA shifts the operating point substantially: precision and recall both rise while FPR drops, yielding a
large F1 gainevidence of selective control rather than increased trigger frequency alone. The **no_gate** ablation
isolates the gates safety role: recall rises but FPR explodes, a characteristic failure mode of unconditional amplification. The **random** direction control does not improve F1, ruling out a generic perturbation-energy explanation.
Composition matters: **global_only** boosts recall but retains higher FPR; **domain_only** underperforms and
increases FPR, consistent with insufficient shared intent evidence. Finally, **no_router** achieves extremely low


17


**ASA:** **Training-Free** **Representation** **Engineering** **for** **Tool-Calling** **Agents**


_Table 17._ Ablation study on the ALL domain. Precision/Recall/F1/Accuracy/FPR are computed for tool-mode triggering
under the strict protocol.


Ablation Mode Strategy Precision Recall F1-Score Accuracy FPR


full baseline 0.440 0.115 0.182 0.484 0.146
full steer 0.872 0.354 0.504 0.651 0.052
no_router baseline 0.440 0.115 0.182 0.484 0.146
no_router steer 0.971 0.354 0.519 0.672 0.010
global_only baseline 0.440 0.115 0.182 0.484 0.146
global_only steer 0.826 0.396 0.535 0.656 0.083
domain_only baseline 0.440 0.115 0.182 0.484 0.146
domain_only steer 0.364 0.125 0.186 0.453 0.219
no_gate baseline 0.440 0.115 0.182 0.484 0.146
no_gate steer 0.422 0.365 0.391 0.432 0.500
random baseline 0.440 0.115 0.182 0.484 0.146
random steer 0.556 0.104 0.175 0.510 0.083
mismatch baseline 0.440 0.115 0.182 0.484 0.146
mismatch steer 0.788 0.427 0.554 0.656 0.115


_Table_ _18._ Post-trigger validity under the steer strategy. Component accuracies are computed conditional on triggering.


Ablation Mode Call Count Format Acc Tool Name Acc Args Acc Success Recall Success Precision


full 39 0.949 0.744 0.949 0.281 0.692
no_router 35 0.943 0.800 0.943 0.281 0.771
global_only 46 0.978 0.696 0.978 0.323 0.674
domain_only 33 0.970 0.758 0.970 0.115 0.333
no_gate 83 0.976 0.723 0.976 0.292 0.337
random 18 1.000 0.944 1.000 0.094 0.500
mismatch 52 0.962 0.635 0.962 0.333 0.615


FPR while preserving recall, implying routing errors are a bottleneck and improving routing is a high-leverage
path forward.


Most variants maintain high format/args accuracy, suggesting the intervention primarily affects _whether_ the
model enters tool mode rather than causing systematic JSON collapse. Tool-name accuracy is the most sensitive
dimension: routing/direction mismatch increases schema errors. **no_gate** triggers far more often but has very
low success precision, demonstrating the deployment failure mode of over-triggering. **no_router** improves success precision, reinforcing that routing errors translate directly into wrong tool names/arguments and represent
a key bottleneck for further improvements.


18


**ASA:** **Training-Free** **Representation** **Engineering** **for** **Tool-Calling** **Agents**


Performance Analysis Across Different Network Layers (Best at Layer 23)



1.0


0.9


0.8


0.7


0.6


0.5



(a) Accuracy Performance

|Col1|Col2|Col3|Col4|Col5|La<br>Val:|Col7|yer 2<br>0.99|3<br>85|Col10|
|---|---|---|---|---|---|---|---|---|---|
|||||||||||
|||||||||||
|||||||||||
|||||||||||
|||||||||||
|||||||||||
|||||||||||
|||||||||||
|||||||||||
|||||||||||
|||||||||||
|||||||||||
|||||||||||
|||||||||||
|||||||||~~Validation~~<br>~~Test~~||
|||||||||||
|||||||||~~Best Val:~~|~~ .9985~~|
|||||||||<br>~~Best Test:~~|<br>~~ 0.9992~~|
|||||||||||



Layer Index



1.0


0.9


0.8


0.7


0.6


0.5



(b) AUC Performance

|Col1|Col2|Col3|Col4|Col5|Laye<br>Val: 0.|r 23<br>9996|Col8|
|---|---|---|---|---|---|---|---|
|||||||||
|||||||||
|||||||||
|||||||||
|||||||||
|||||||||
|||||||||
|||||||||
|||||||||
|||||||||
|||||||||
|||||||||
|||||||||
|||||||||
|||||||~~Validation~~<br>~~Test~~||
|||||||||
|||||||~~Best Val:~~|~~ .9996~~|
|||||||<br>~~Best Test:~~|<br>~~ 0.9998~~|
|||||||||



Layer Index



_Figure_ _9._ LLAMA: layer-wise probe decodability sweep over 32 layers.


A clear peak/plateau indicates tool intent becomes linearly accessible at certain depths, but the optimal layer
can differ from Qwen due to architectural/training differences. This figure justifies re-running layer selection
per backbone; reusing Qwens _ℓ_ blindly can be suboptimal. Conceptually, it supports the claim that intent
decodability is common while the depth at which it is most actionable is model-dependent.


19


**ASA:** **Training-Free** **Representation** **Engineering** **for** **Tool-Calling** **Agents**


_Table_ _19._ Injection instances (baseline text vs injected function-call text) with strict validity scores.


Index Domain Baseline (excerpt) Injected text (exact) Fmt Tool Args Task


1 math _(baseline...)_ “To calculate ...” _<functioncall>{"name":"calculator","arguments":{"expression":"3_ 1.0 1.0 1.0 1.0
_+_ _4_ _+_ _3"}}</functioncall><|im_end|>_


7 search _<functioncall>..._ _<functioncall>{"name":"web_search","arguments":{"query":"images_ 1.0 1.0 1.0 1.0
_sustainable_ _living_ _5"}}</functioncall>_
_<functioncall>{"name":"web_search","arguments":{"query":"images_
_recycling_ _5"}}</functioncall><|im_end|>_


18 math _(baseline...)_ “Discounted Price...” _<functioncall>{"name":"calculator","arguments":{"expression":"$200_ 1.0 1.0 1.0 1.0

_*_ _(1_ _-_ _0.2)"}}</functioncall><|im_end|>_


23 math _(baseline...)_ “Discounted Price...” _<functioncall>{"name":"calculator","arguments":{"expression":"$200_ 1.0 1.0 1.0 1.0

_*_ _(1_ _-_ _0.2)"}}</functioncall><|im_end|>_


24 code _(baseline...)_ “def calculate...” <functioncall>{"name":"python_interpreter","arguments":{"code":"import1.0 1.0 1.0 1.0
numpy as np\\nnp.min([10,
20, 30])                        - np.max([10, 20,
30])"}}</functioncall><|im_end|>


**Analysis** **of** **Table** **19.** This table clarifies what “strict post-trigger validity” means in practice. Case 7 is especially
diagnostic: the baseline already looks tool-like but lacks consistent closing tags, which can fail strict validators; the
injected version repairs the delimiter structure while preserving semantic intent, yielding perfect format/tool/args scores.
Across cases, the injected outputs are fully schema-formed _<functioncall>_ blocks, which is necessary for deployment
executability under Appendix D.


**G.** **Injection** **Examples** **(Baseline** **vs** **Injected)**


20


**ASA:** **Training-Free** **Representation** **Engineering** **for** **Tool-Calling** **Agents**


_Table_ _20._ Raw injection JSON records (verbatim) used for Appendix G.


[

{

"index": 1,
"domain": "math",
"instruction": "Okay, here they are. I took Math with a grade of A...",
"baseline_text": "To calculate your total GPA...",
"injected_text": "<functioncall>{\"name\": \"calculator\", \"arguments\": {\"expression\": \"3 + 4 + 3\"}}</functioncall><|
im_end|>",
"format_score": 1.0, "tool_name_score": 1.0, "args_score": 1.0, "task_score": 1.0
},
{

"index": 7,
"domain": "search",
"instruction": "I need images related to \"sustainable living\"...",
"baseline_text": "<functioncall>{\"name\": \"web_search\"...",
"injected_text": "<functioncall>{\"name\": \"web_search\", \"arguments\": {\"query\": \"images sustainable living 5\"}}</
functioncall>\n<functioncall>{\"name\": \"web_search\", \"arguments\": {\"query\": \"images recycling 5\"}}<|im_end|>",
"format_score": 1.0, "tool_name_score": 1.0, "args_score": 1.0, "task_score": 1.0
},


{
"index": 18,
"domain": "math",
"instruction": "I saw a dress that I liked...",
"baseline_text": "To calculate the discounted price...",
"injected_text": "<functioncall>{\"name\": \"calculator\", \"arguments\": {\"expression\": \"$200   - (1   - 0.2)\"}}</functioncall
><|im_end|>",
"format_score": 1.0, "tool_name_score": 1.0, "args_score": 1.0, "task_score": 1.0
},
{

"index": 24,
"domain": "code",
"instruction": "I have an array of numerical entities...",
"baseline_text": "To calculate the range...",
"injected_text": "<functioncall>{\"name\": \"python_interpreter\", \"arguments\": {\"code\": \"import numpy as np\\nnp.min([10,
20, 30])      - np.max([10, 20, 30])\"}}</functioncall><|im_end|>",
"format_score": 1.0, "tool_name_score": 1.0, "args_score": 1.0, "task_score": 1.0
}
]


**Analysis** **of** **Table** **20.** This verbatim record ensures the injection examples are auditable and reproducible. Notably,
the injected texts enforce complete tag closure and schema-complete JSON payloads with _name_ and _arguments_ . Under
the deterministic rules in Table 8, these surface-form constraints are necessary: even semantically correct intentions can
fail deployment if the emitted string is not strictly executable.


21


