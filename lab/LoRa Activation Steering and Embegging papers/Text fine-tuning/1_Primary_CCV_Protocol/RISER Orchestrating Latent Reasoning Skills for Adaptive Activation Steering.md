## **RISER: Orchestrating Latent Reasoning Skills for Adaptive** **Activation Steering**

**Wencheng** **Ye** **Xiaoyang** **Yuan** **Yi** **Bin** **Hengyu** **Jin**
Tongji University Tongji University Tongji University Tongji University


**Liang** **Peng** **Pengpeng** **Zeng** **Heng** **Tao** **Shen**
Tencent Tongji University Tongji University



**Abstract**


Recent work on domain-specific reasoning
with large language models (LLMs) often
relies on training-intensive approaches that
require parameter updates. While activation steering has emerged as a parameterefficient alternative, existing methods apply static, manual interventions that fail
to adapt to the dynamic nature of complex reasoning. To address this limitation, we propose **RISER** ( **R** outer-based
**I** ntervention for **S** teerable **E** nhancement of
**R** easoning), a plug-and-play intervention
framework that adaptively steers LLM reasoning in activation space. RISER constructs a library of reusable reasoning vectors and employs a lightweight Router to
dynamically compose them for each input.
The Router is optimized via reinforcement
learning under task-level rewards, activating latent cognitive primitives in an emergent and compositional manner. Across
seven diverse benchmarks, RISER yields
3.4–6.5% average zero-shot accuracy improvements over the base model while surpassing CoT-style reasoning with 2–3×
higher token efficiency and robust accuracy gains. Further analysis shows that
RISER autonomously combines multiple
vectors into interpretable, precise control
strategies, pointing toward more controllable and efficient LLM reasoning. Code
can be found in: `[RISER](https://github.com/gooogleshanghai/RISER-Orchestrating-Latent-Reasoning-Skills-for-Adaptive-Activation-Steering)` .


**1** **Introduction**


Large Language Models (LLMs) (Touvron
et al., 2023; Brown et al., 2020) exhibit
strong general reasoning abilities (Ahn et al.,
2024; Wei et al., 2022a; Shi et al., 2024),
yet they often perform inconsistently on specialized downstream tasks requiring domain
knowledge, disciplined reasoning patterns, and
the coordinated use of multiple cognitive
skills (Wang et al., 2025b; Li et al., 2025;





































Figure 1: Conceptual comparison between Standard Inference and the RISER framework. RISER
(bottom) uses a learned Router to dynamically inject composed vectors, analogous to an explicit
executive-control mechanism.


Chang et al., 2024). In practice, we seek
to strengthen such reasoning without expensive retraining or relying solely on indirect
prompting strategies, motivating mechanisms
that can directly modulate the model’s internal computation during inference.


Existing approaches face fundamental limitations. Training-based methods such as Supervised Fine-Tuning (SFT) and Reinforcement Learning (RL) require invasive parameter updates (Shenfeld et al., 2025; Huan
et al., 2025), leading to issues such as catastrophic forgetting (Li et al., 2024; Ding and
Wang, 2025) or substantial computational
overhead (Liao et al., 2025). Meanwhile,
training-free prompting (Wang et al., 2025a)
suffers from signal attenuation during forward
propagation (Wu et al., 2025). Activation
steering offers a promising alternative by directly modifying internal activations without
changing model weights, but existing methods predominantly use a _single_ steering vector with _fixed_ intervention strength (Venhoff
et al., 2025b; Hø jer et al., 2025; Jin et al.,
2025). Such static, one-dimensional control


limits their expressiveness and fails to capture
the rich, multi-faceted structure of reasoning
embedded in large models.
Decades of cognitive neuroscience research
suggest a more flexible architecture: human
cognition emerges from **modular** functional
regions (Kanwisher et al., 1999; Anderson,
2010) coordinated by the **Prefrontal** **Cor-**
**tex** **(PFC)** through dynamic routing of control signals (Miller and Cohen, 2001). This
perspective suggests a different blueprint, and
highlights two key elements absent in current
activation steering methods: a set of diverse
reasoning primitives and a controller capable
of selecting and composing them adaptively.
Inspired by this, we ask: _Can_ _we_ _build_ _a_
_PFC-like_ _controller_ _that_ _adaptively_ _awakens,_
_routes,_ _and_ _composes_ _latent_ _cognitive_ _capabili-_
_ties_ _through_ _activation-level_ _interventions_ _dur-_
_ing_ _inference?_
Furthermore, recent advances in Representation Engineering (Tan et al., 2024; Postmus and Abreu, 2024; Alain and Bengio, 2016)
show that LLMs’ activation spaces contain
interpretable, semantically meaningful directions to capture attributes, skills, and latent
reasoning patterns (Lee et al., 2025b; Marks
and Tegmark, 2023; Cyberey and Evans, 2025;
Zhang et al., 2025a; Rimsky et al., 2024).
These directions can be disentangled, composed, and manipulated to alter model behavior (Fartale et al., 2025). Such findings
support the hypothesis that complex reasoning may be decomposable into multiple linear subspaces, each corresponding to a distinct cognitive capability. If true, then static
single-vector steering is fundamentally misaligned with the structure of the model: what
is needed is dynamic, compositional, and taskaware control.
Therefore, we propose a dynamic activation steering approach, termed **RISER**
( **R** outer-based **I** ntervention for **S** teerable
**E** nhancement of **R** easoning), which enables
adaptive and compositional control of the
model’s internal reasoning process. RISER
treats distinct activation patterns as reusable
reasoning directions (which we call cognitive
primitives). We first extract reasoning vectors that encode core cognitive functions to
form a reusable capability library. Then, we
introduce a lightweight Router module act


ing as a reasoning controller. Given an input query, the Router dynamically selects relevant vectors, determines optimal intervention strengths, and injects the combined representation into the model’s forward pass (see
Figure 1). We use RL to directly optimize
the routing policy, effectively externalizing
the model’s implicit logic into explicit, interpretable control decisions.

Our experiments across seven diverse reasoning benchmarks demonstrate RISER’s effectiveness. It yields 3.4%–6.5% absolute zeroshot accuracy improvements while maintaining inference efficiency close to standard inference. Further analysis reveals that the RLtrained Router autonomously composes multiple primitives in meaningful ways, offering
transparent insight into which cognitive capabilities are invoked and how they synergize for
a given task. We summarize our primary contributions as follows:

- We propose RISER, a plug-and-play activation intervention framework that keeps
LLM parameters frozen while a lightweight
Router dynamically selects and composes
cognitive primitives, enabling precise and
task-adaptive reasoning control.

- We develop a rigorous pipeline for eliciting
high-quality reasoning vectors, incorporating LLM-Judge filtering and clustering to
construct an orthogonal and disentangled library of cognitive primitives with verified
steering effects.

- Extensive evaluation on seven benchmarks
shows that we establish a new state-of-theart for activation steering, closing the gap
between inference-time control and heavy
fine-tuning while offering interpretable insights into latent skill composition.


**2** **Related** **Work**


**2.1** **Activation** **Steering**


The study of linear representations has evolved
from passive probing (Alain and Bengio, 2016;
Belinkov, 2022) to activation steering (Turner
et al., 2023; Bartoszcze et al., 2025; Wang
et al., 2025c), which enables active intervention on high-level concepts. Effective methods for concept vector extraction include Contrastive Activation Addition (CAA) (Rimsky
et al., 2024) and SAEs (Cunningham et al.,


**Offline Stage B:**
**Router Training**



**Input Query**

A company purchased equipment for $50,000
with a 10-year useful life and $5,000 salvage
value. Using straight-line depreciation, what is
the annual depreciation expense?



























Figure 2: An overview of the RISER framework, illustrating the process of offline extraction of reasoning
vectors and offline training of the Router, followed by online inference where the pre-trained Router
dynamically selects and combines vectors to intervene in the LLM’s activation, guiding the final output.



2023). More recently, this paradigm has been
extended to cognitive processes and reasoning, as it has been demonstrated that a reasoning vector extracted from one task can
be applied to improve accuracy on another,
thus confirming that reasoning capabilities are
transferable (Hø jer et al., 2025; Wang et al.,
2025a; Venhoff et al., 2025a; Zbeeb et al.,
2025; Valentino et al., 2025). However, they
typically apply a single, fixed vector with a
manually-tuned strength for all inputs, failing
to adapt to the specific demands of each task.
While some work has introduced limited dynamics through gated activation (Jin et al.,
2025) or strength calculation for single vectors (Zhang et al., 2025a), they do not address
the challenge of composing multiple capabilities with adaptive intervention strengths and
rely on supervised objectives for training.


**2.2** **Conditional** **Computation** **and**
**Modular** **Networks**


Modular networks can be categorized into
two main granularities: intra-model and intermodel. A prominent intra-model approach
is the Mixture-of-Experts (MoE) architecture (Shazeer et al., 2017; Fedus et al., 2022)
that activates a small subset of experts for
each input. At a coarser, inter-model granularity, researchers have explored task allocation



among multiple independent LLMs (Zhang
et al., 2025b; Piskala et al., 2024). RISER
applies the dynamic routing philosophy to a
single, frozen LLM at the representation layer,
offering greater flexibility and controllability.


**3** **The** **RISER** **Framework**


**3.1** **Overall** **Architecture**


As depicted in Figure 2, RISER follows a simple offline-online split. Offline, we assume access to a compact library of reasoning vectors
_{_ **v** _i}_ _[K]_ _i_ =1 [,] [each] [representing] [a] [reusable] [cogni-]
tive primitive. Given this library, we train a
lightweight Router that learns to map internal states to compositions of these primitives
(Section 3.3). In Section 4, we describe one
concrete, data-driven instantiation process. In
the online inference phase, the prepared components are used to intervene minimally but
effectively in the LLM’s forward computation.
As an input query is processed up to a predetermined intermediate layer _l_, we read the
hidden state of the last token, **h** _l_, and feed it
into the Router, which infers the immediate
cognitive demands and outputs a composite
reasoning vector by selecting and weighting a
small subset of primitives. The resulting vector is injected back into the model to the activation at layer _l_, and maintained as a sustained


cognitive priming during decoding.


**3.2** **Router** **as** **a** **Dynamic** **Controller**


The Router is a lightweight network that reads
the model’s current hidden state and outputs
an intervention in activation space. It receives
the hidden state of the last token at the target
layer _l_, denoted by **h** _l_ _∈_ R _[d]_, which serves as a
natural proxy for the task’s current reasoning
demands. From this state, the Router produces two parallel outputs over the _K_ primitives at a sequence-level: a selection mask **w** _∈_
_{_ 0 _,_ 1 _}_ _[K]_ and a strength vector _**α**_ _∈_ [0 _, α_ max] _[K]_ .
In practice, the selection head first outputs
a probability vector **p** _∈_ [0 _,_ 1] _[K]_ via a Sigmoid activation, which is thresholded at inference time to obtain the binary mask **w** that
specifies which capabilities to activate. During training, we apply the Gumbel-Sigmoid
relaxation (Jang et al., 2017). In parallel,
the strength head predicts _**α**_, which specifies
_how_ _strongly_ to move along each selected direction. This dual-head design decouples the
discrete choice of primitives from continuous
intensity modulation, encouraging sparse yet
flexible control. The final composite vector for
injection is synthesized via a weighted summation over the primitive library:



**Supervised** **Warm-Up.** To avoid a coldstart regime, we first train the Router on a curated dataset derived from the vector library.
For each training instance, we use grid search
over the library to identify an intervention configuration ( **w** _[∗]_ _,_ _**α**_ _[∗]_ ) that successfully elicits the
correct reasoning generation, establishing a robust baseline policy that knows which primitives tend to be useful in which contexts.
**Reinforcement** **Learning** **Refinement.**
To move beyond the limitations of this static
dataset and adapt to unseen task variations,
we then fine-tune the Router with Group Relative Policy Optimization (GRPO) (Shao et al.,
2024). In this stage, the Router is free to explore the space of primitive compositions. We
use an accuracy-based reward



_ri_ =




1 _,_ if the answer is correct _,_
(3)
0 _,_ otherwise _,_



which directly encourages policies that increase end-task accuracy. To ensure that interventions remain conservative and stable, we
additionally impose a KL regularizer which at
each decoding step _t_ computes


_L_ KL = E _t_ - _D_ KL� _π_ routed( _· | x, y<t_ ) _∥_ _π_ base( _· | x, y<t_ )� [�] _,_

(4)
where _π_ routed and _π_ base denote the output
distributions of the routed and base models.
This regularizer discourages vector injections
that induce large deviations from the base
model’s behavior while still allowing beneficial
changes, enabling the Router to learn primitive compositions without destabilizing the
underlying model.


**4** **Vector** **Elicitation** **Pipeline**


As effectiveness of the Router depends on the
quality of the underlying primitives, we construct a concrete, data-driven vector elicitation pipeline. We first generate a broad candidate set of activation pairs following Contrastive Activation Additions. For a diverse
range of reasoning tasks, we design paired
prompts: a _positive_ prompt to elicit rigorous reasoning and a _negative_ prompt to suppress it. To mitigate noise, we integrate
a quality-aware filtering mechanism using an
LLM Judge (Claude-3.5-Sonnet (Anthropic,
2024)) which evaluates the generated reasoning traces with strict inclusion criteria: only



**v** inject =



_K_


_wi · αi ·_ **v** _i,_ (1)

_i_ =1



where _wi_ and _αi_ are the _i_ -th elements of **w** and
_**α**_, respectively, and **v** _i_ is the _i_ -th reasoning
primitive. This vector is then injected into
the LLM’s forward pass via an element-wise
addition to the last-token activation at layer _l_ :


**h** _[′]_ _l_ = **h** _l_ + **v** inject _,_ (2)


where **h** _l_ is the original hidden activation and
**h** _[′]_ _l_ is the resulting steered activation. The
model subsequently resumes its computation
from layer _l_ +1 onward using **h** _[′]_ _l_, so that the
remaining layers perform their usual processing under a slightly reoriented internal state
toward the desired reasoning trajectory.


**3.3** **Router** **Optimization**


Given the Router’s role, we optimize it directly
from task-level feedback, enabling it to learn
when and how to combine primitives to best
serve downstream objectives.


Figure 3: Latent space visualization of extracted
vectors. We project the high-dimensional difference vectors onto a 2D plane using PCA. The
visualization reveals naturally forming clusters,
demonstrating that the extracted reasoning vectors
possess strong semantic separability within the activation space.


sample pairs where the positive generation
achieves proficient reasoning and the negative
one clearly lacks reasoning are retained.
After filtering, we investigate the structure
of the difference vectors ( **h** [+] _−_ **h** _[−]_ ) to build a
compact set of representative reasoning directions. Our goal is to construct a small, interpretable, and practically controllable library
suitable for downstream routing. To this end,
we perform PCA visualization to examine the
coarse geometry of the activation manifold. As
shown in Figure 3, the projections consistently
exhibit several recurring high-density regions.
Rather than adopting a large number of
clusters, we select major clusters that appear stably across random initializations and
that jointly cover the dominant reasoning
patterns observed in data (numerical reasoning, logical inference, ethical alignment, reading comprehension, scientific analysis, and
domain-specific knowledge), maintaining a
compact and human-understandable control
space. Guided by the observation that the
first six principal components account for over
85% of the total variance in the extracted vectors, we set the cluster count _K_ = 6 and apply K-Means clustering to formally separate
the difference vectors. Let _Si_ denote the set
of sample indices assigned to the _i_ -th cluster.
The reasoning vector **v** _i_ _∈_ R _[d]_ for primitive _i_ is
defined as the centroid:



1
**v** _i_ =
_|Si|_





( **h** [+] _j_ _[−]_ **[h]** _j_ _[−]_ [)] _[,]_ (5)
_j∈Si_



Figure 4: Reasoning vector library similarity
heatmap. The low off-diagonal values confirm that
the extracted vectors represent distinct and separable cognitive functions.


ative activations at layer _l_ for the _j_ -th pair.
We apply L2 normalization ( **v** _i_ _←_ **v** _i/∥_ **v** _i∥_ 2)
to ensure consistent intervention magnitudes.
The resulting library shows that the vectors are nearly orthogonal, with an average
pairwise cosine similarity _<_ 0 _._ 1 (Figure 4),
indicating that the selected directions represent distinct and minimally overlapping cognitive behaviors. Furthermore, as shown in
Figure 5, static steering experiments validate
their functional efficacy: applying them can
yield accuracy improvements on corresponding datasets. These findings confirm that our
compact, engineering-driven extraction yields
a set of effective and independently controllable reasoning modules.


**5** **Experiments**


**5.1** **Experimental** **Setup**


We employ the Qwen2.5 family (7B-Instruct,
14B-Instruct, 32B-Instruct) (Qwen et al.,
2025) and Llama-3-8B-Instruct (Grattafiori
et al., 2024) as base models and, following
prior work (Chen et al., 2025), respectively
select layers 20, 25, 40 and 13 as default
layers for vector elicitation and intervention.
We threshold gating selection probabilities at
0 _._ 7, set the maximum intervention strength to
_α_ max = 2 _._ 0 and implement the Router as a
lightweight, bottleneck-style Multi-Layer Perceptron (MLP) with approximately 5 million
parameters ( _<_ 0 _._ 1% of base model), distinguishing our approach from simple linear classifiers while introducing negligible latency.
**Datasets.** The Vector Elicitation data consist of 500 problems randomly selected from
MMLU (Hendrycks et al., 2021b), each paired



where **h** [+] _j_ [and] **[ h]** _j_ _[−]_ [denote the positive and neg-]


Table 1: Performance Comparison on Qwen2.5 Family and Llama-3 Models. We report accuracy (%)
and improvements (∆) over the baseline. **Best** and Second best results are labeled.


**Dataset** **/** **Category** **Base** **Model** **CoT-Prompting** **Self-Consistency** **CoT** **CAA** **CAST** **SAS** **FR-Ponder** **Our** **Method** **(RISER)**


**Qwen2.5-7B-Instruct**
MATH 46.8 51.5 52.1 47.1 49.8 48.3 49.2 **53.3(+6.5)**
GSM8K 79.8 **85.3** 85.2 82.9 84.6 83.8 84.4 85.2(+5.4)

_Average_ _(Math/Logic)_ 63.3 68.4 68.7 65.0 67.2 66.1 66.8 **69.3(+6.0)**


GPQA 31.0 31.2 33.2 31.9 33.7 32.6 33.0 **36.8(+5.8)**
MMLU-Pro (in-dist.) 44.1 44.0 44.2 46.2 47.5 46.9 47.7 **50.3(+6.2)**
ARC-C 63.7 63.3 64.4 63.3 65.3 64.1 65.8 **67.2(+3.5)**
_Average_ _(General)_ 46.3 46.2 47.3 47.1 48.8 47.9 48.8 **51.4(+5.1)**


Ethics 48.6 49.3 48.7 **53.2** 52.4 51.0 50.2 52.1(+3.5)
TruthfulQA 56.4 58.9 58.9 59.6 59.4 59.1 59.0 **59.8(+3.4)**
_Average_ _(Moral)_ 52.5 54.1 53.8 **56.4** 55.9 55.1 54.6 56.0(+3.5)


**Qwen2.5-14B-Instruct**
MATH 55.6 58.9 60.4 56.4 59.0 57.4 58.2 **61.8(+6.2)**
GSM8K 86.5 90.5 89.7 88.6 90.1 89.2 90.0 **90.8(+4.3)**
_Average_ _(Math/Logic)_ 71.1 74.7 75.1 72.5 74.6 73.3 74.1 **76.3(+5.2)**


GPQA 32.8 33.6 34.5 33.7 35.9 34.2 35.3 **38.0(+5.2)**
MMLU-Pro (in-dist.) 51.2 50.9 51.8 54.0 55.1 54.7 55.6 **57.2(+6.0)**
ARC-C 67.3 67.6 68.2 67.1 69.4 67.9 70.0 **71.6(+4.3)**
_Average_ _(General)_ 50.4 50.7 51.5 51.6 53.5 52.3 53.6 **55.6(+5.2)**


Ethics 64.3 66.1 65.2 **68.5** 67.7 66.3 66.9 67.9(+3.6)

TruthfulQA 58.4 60.6 61.5 61.3 61.8 61.4 61.0 **62.1(+3.7)**
_Average_ _(Moral)_ 61.4 63.4 63.4 64.9 64.8 63.9 64.0 **65.0(+3.6)**


**Qwen2.5-32B-Instruct**
MATH 57.7 60.8 61.9 58.8 60.9 59.6 60.4 **63.2(+5.5)**
GSM8K 90.9 93.2 93.5 91.9 93.0 92.6 92.7 **93.9(+3.0)**
_Average_ _(Math/Logic)_ 74.3 77.0 77.7 75.4 77.0 76.1 76.6 **78.6(+4.3)**


GPQA 48.0 48.5 49.9 48.9 50.3 49.2 50.0 **52.7(+4.7)**
MMLU-Pro (in-dist.) 55.1 55.6 56.5 57.4 58.4 58.0 58.9 **60.7(+5.6)**
ARC-C 70.4 70.1 71.4 70.9 72.5 71.6 73.0 **74.7(+4.3)**
_Average_ _(General)_ 57.8 58.1 59.3 59.1 60.4 59.6 60.6 **62.7(+4.9)**


Ethics 77.9 78.8 78.2 81.0 **81.4** 79.7 79.9 **81.4(+3.5)**
TruthfulQA 60.2 62.1 62.3 62.8 **64.0** 62.4 62.5 63.5(+3.3)

_Average_ _(Moral)_ 69.1 70.5 70.3 71.9 **72.7** 71.1 71.2 72.5(+3.4)


**Llama-3-8B-Instruct**
MATH 30.9 33.6 34.1 32.8 33.2 32.4 34.2 **35.4(+4.5)**
GSM8K 84.5 88.2 87.3 88.5 88.7 88.0 88.9 **89.1(+4.6)**
GPQA 25.8 26.3 30.2 25.6 27.4 26.0 27.9 **30.9(+5.1)**
TruthfulQA 44.0 45.2 47.5 48.2 **48.7** 47.3 47.8 48.4(+4.4)


ation Datasets include benchmarks chosen to
cover diverse reasoning types including math/logic reasoning (GSM8K (Cobbe et al., 2021),
MATH (Hendrycks et al., 2021c)), general
reasoning (GPQA (Rein et al., 2023), ARCC (Clark et al., 2018), MMLU-Pro) and ethics
and factual alignment (Ethics (Hendrycks
et al., 2021a), TruthfulQA (Lin et al., 2022)).



Figure 5: Static steering validation. The performance sensitivity to steering strength ( _α_ ) confirms
that the extracted vectors effectively modulate specific reasoning behaviors.


with positive and negative guiding prompts;
During Router Training, the SFT phase uses
an automated pipeline to extract and annotate
200 samples from MMLU, while the RL phase
employs MMLU-Pro (Wang et al., 2025d) as
the resource for reinforcement learning refinement. We split MMLU-Pro into 70% training
tasks for RL and 30% held-out tasks for evaluation, with no question overlap. The Evalu


**Baselines.** We compare against a set of
baselines to quantify improvements: zero-shot
base model; Chain-of-Thought (CoT) prompting (Wei et al., 2022b); Self-Consistency
CoT (Wang et al., 2023) (with 5 samples and
majority voting); CAA (static vector intervention with the best performance under different multipliers) (Rimsky et al., 2024); CAST
(conditional activation steering) (Lee et al.,
2025a); SAS (using sparse autoencoders for
vector elicitation) (Bayat et al., 2025) and FRPonder (He and Tang, 2025) (using a controller to regulate reasoning depth by selecting
steering vectors).


Table 2: Comprehensive ablation studies on key
framework components and design choices. We report accuracy (%) on representative datasets.


**Category** **Model** **Variant** **/** **Setting** **MATH** **GPQA** **TruthfulQA**


**Our** **Method** **(Full** **RISER** **@** **L20)** 53.3 36.8 59.8
_Direct_ _GRPO_ _(full-model_ _RL_ _fine-tuning)_ 47.6 34.6 58.6


[w/o] [RL] [Refinement] [(SFT-only)] 49.4 31.2 54.6
_Training_ _Ablation_ [-]

            - w/o Composition (Top-1 Only) 51.6 33.5 60.2


            - Early Layer (L5) 48.5 31.5 55.0

            - Middle Layer (L19) 52.1 35.5 59.5

_Layer_ _Sensitivity_

            - Middle Layer (L21) 51.8 34.6 59.6

            - Late Layer (L28) 49.0 32.0 56.1


**Ablation** **Settings.** To dissect component contributions, we evaluate several variants: **Direct** **GRPO** **Fine-tuning** (GRPO
algorithm on the backbone model under an
equivalent computational budget); **SFT-only**
**Router** (Router trained only in the supervised phase without RL refinement); **Top-1**
**Vector** **Only** (select only the single higheststrength reasoning vector, disabling vector
composition); and **Layer** **Sensitivity** **Anal-**
**ysis** (interventions applied at layers adjacent
to the default layer as well as at earlier layer
5 and later layer 28 to assess sensitivity to intervention depth).
**Evaluation** **Metrics.** We report primary
task accuracy and token efficiency measured
by the total number of tokens generated.
**Implementation** **Details:** For the SFT
phase, we fine-tune the Router for 3 epochs
with a learning rate of 5 _×_ 10 _[−]_ [6] . For RL phase
we adopt a learning rate of 2 _×_ 10 _[−]_ [6], a batch
size of 128, a maximum context length of 8192
tokens during 2 epochs.


**5.2** **Results**


Table 1 presents the comprehensive results on
models, where RISER exhibits consistent performance gains across different model families.
Focusing on the primary Qwen family, our
method (RISER) achieves the highest average
accuracy in the challenging **General Reason-**
**ing** category, significantly outperforming all
other methods. In **Math/Logic** **Reasoning**,
our method also outperforms the strong SelfConsistency CoT baseline. This demonstrates
the framework’s strong generalization and its
ability to handle complex, multi-disciplinary
tasks by dynamically composing capabilities.
By learning to compose latent reasoning primitives only on one dataset, the Router acquires
a transferable control strategy that generalizes
across heterogeneous reasoning benchmarks.
We quantitatively analyze token efficiency



on MATH and GPQA. Regarding efficiency,
RISER requires only 1392 and 3056 tokens
on MATH and GPQA, respectively, compared
to 4033 and 6195 for CoT, realizing a 2–3×
gain. While CoT generates reasoning-helpful
external text, RISER mobilizes latent circuits
for higher computational utilization, bypassing the need for verbose textual scaffolding to
guide the trajectory.
We compare our framework against static
intervention CAA and other steering methods.
The results clearly show the value of dynamic
control. In the two categories requiring flexible, compositional reasoning (Math/Logic and
General Reasoning), our dynamic Router significantly outperforms the static CAA baseline. Interestingly, in the Moral Alignment
category, the static CAA or conditionally dynamic CAST baseline achieves the highest
score, slightly edging out our method. This is
likely because these tasks are highly uniform in
their cognitive demands, and a strong, static
application of the Ethical Alignment vector is
highly effective. However, RISER still delivers substantial alignment improvements over
all non-steering baselines.
The Router strategy heatmap in Figure 6
also provides a cognitive map which intuitively
demonstrates the explicit policy learned by
the Router. On one hand, it learns a highly
logical and specialized mapping: MATH and
GSM8K tasks are strongly associated with
the Numerical Calculation vector, while Ethics
and TruthfulQA tasks correspond to the Ethical Alignment vector. On the other hand,
when faced with complex cross-domain tasks
(GPQA), the Router learns to autonomously
compose multiple cognitive primitives. This
provides direct evidence that the RL refinement phase externalized the LLM’s implicit,
synergistic strategies for complex problemsolving into an analyzable model.


**5.3** **Ablation** **Studies**


We performed ablation studies on Qwen2.57B-Instruct (Table 2) to isolate the contributions of key components.
**Comparison** **with** **Direct** **Fine-tuning:**
A core question is whether the performance
gains come from our RISER framework or simply from the RL training itself. To answer this,
we compare RISER against the Direct GRPO


Math


GSM8K


GPQA


MMLU-Pro


ARC-Challenge


Ethics


TruthfulQA



Router Strategy Heatmap: Task-Specific Vector Analysis



1.4


1.2


1.0


0.8


0.6


0.4


0.2


0.0


|1.|42|0.|63|0.|09|0.|28|0.|53|0.|18|
|---|---|---|---|---|---|---|---|---|---|---|---|
|||||||||||||
|||||||||||||
|~~1.~~|~~7~~|~~0.~~|~~8~~|~~0.~~|~~6~~|~~0.~~|~~1~~|~~0.~~|~~1~~|~~0.~~|~~5~~|
|~~0.~~|~~35~~|~~0.~~|~~70~~|~~0.~~|~~11~~|~~0.~~|~~65~~|~~1.~~|~~24~~|~~0.~~|~~72~~|
|||||||||||||
|||||||||||||
|~~0.~~|~~3~~|~~0.~~|~~8~~|~~0.~~|~~6~~|~~0.~~|~~3~~|~~1.~~|~~9~~|~~0.~~|~~0~~|
|~~0.~~|~~0~~|~~1.~~|~~5~~|~~0.~~|~~3~~|~~0.~~|~~2~~|~~0.~~|~~2~~|~~0.~~|~~5~~|
|||||||||||||
|~~0.~~|~~11~~|~~0.~~|~~5~~|~~1.~~|~~7~~|~~0.~~|~~3~~|~~0.~~|~~8~~|~~0.~~|~~6~~|
|||||||||||||
|||||||||||||
|~~0.~~|~~6~~|~~0.~~|~~0~~|~~1.~~|~~2~~|~~0.~~|~~8~~|~~0.~~|~~5~~|~~0.~~|~~3~~|



Reasoning Vectors

Figure 6: This heatmap shows the average strength
assigned by the Router for each reasoning vector
across different benchmarks and exhibits both logical specialization and complex composition.


baseline. RISER consistently outperforms the
GRPO baseline in average accuracy across all
three categories, which indicates that applying
the same computational budget to train an external, dynamic reasoning controller is a more
effective approach and validates its generalization advantage.
**Impact** **of** **RL** **Training:** The SFT-only
Router significantly underperforms the full
model, especially on complex benchmarks like
GPQA and TruthfulQA, confirming that RL
refinement is crucial for discovering synergistic vector compositions.
**Necessity** **of** **Composition:** Restricting
the Router to a single vector (Top-1 Vector
Only) hurts performance on multi-disciplinary
tasks, validating the critical role of vector
orchestration. Conversely, on the homogeneous TruthfulQA, the Top-1 variant achieves
a marginal gain, indicating that our framework
correctly adapts to favor focused, single-vector
interventions for monolithic tasks.
**Layer** **Optimality:** Finally, Layer Sensitivity analysis identifies the middle layers as
the optimal intervention site, showing robustness in adjacent layers but significant degradation at the model’s input and output layers.
This observation confirms the hypothesis that
reasoning processes crystallize within the middle layers, acting as a critical bridge between
the initial input processing in early layers and
the final linguistic realization in later layers.


**5.4** **Extensibility**


To investigate extensibility, we extend RISER
to a different domain and introduce an additional primitive targeting code synthesis. Following the same vector elicitation and routing pipeline, we expand the Router’s output



space to seven dimensions and perform a brief
SFT phase on 200 examples, updating only the
Router. On HumanEval (Chen et al., 2021),
the frozen base model achieves 56.3% pass@1,
while static CAA improves performance to
57.2%. The extended Router over seven primitives further boosts accuracy to 59.9% and
does not significantly affect performance on
the original reasoning benchmarks, indicating
that newly added primitives can be integrated
in a non-interfering manner.


**5.5** **Transferability** **Across** **Models**


We further examine whether RISER can be
reused beyond the backbone on which it is
derived and evaluate cross-model transfer by
directly applying a trained RISER configuration to a different target model. Within the
same model family, transferring RISER across
parameter scales remains effective, suggesting
that both the learned vector library and the
Router’s composition strategy align reasonably well across scales. In contrast, transferring across different model families provides
no benefit, indicating that the primitive directions and routing policy are tightly coupled to model-specific representation geometry and activation statistics. These results indicate that transfer is promising when the underlying activation manifolds are sufficiently
aligned, but not across heterogeneous architectures. Full analysis are in Appendix C.


Table 3: Cross-Model Transferability on MATH.
Off-diagonal entries show transfer results.

|Target Model (Inference)|Source Router (Trained on)|
|---|---|
|**Target Model (Inference)**|**Qwen-7B**<br>**Qwen-14B**<br>**Qwen-32B**<br>**Llama-3-8B**|
|**Qwen2.5-7B**<br>**Qwen2.5-14B**<br>**Qwen2.5-32B**|**53.3**<br>51.7 (+4.9)<br>52.1 (+5.3)<br>46.5 (-0.3)<br>58.1 (+2.5)<br>**61.8**<br>60.4 (+4.8)<br>55.8 (+0.2)<br>59.8 (+2.1)<br>60.6 (+2.9)<br>**63.2**<br>57.5 (-0.2)|
|**Llama-3-8B**|30.5 (-0.4)<br>31.1 (+0.2)<br>30.8 (-0.1)<br>**35.4**|



**6** **Conclusion**


RISER demonstrates that LLM reasoning can
be effectively enhanced by orchestrating latent activations, offering a computationally efficient alternative to weight modification or
verbose prompting. By learning explicit, RLoptimized policy, our framework achieves significant performance gains while validating
the existence of steerable cognitive primitives
within frozen models. This approach shifts the
focus from surface-level text generation to internal state management, establishing a viable


path toward more controllable and resourceefficient AI systems.


**7** **Limitations**


Our framework, while effective, is constrained
by its reliance on reactivating latent capabilities, making its performance bounded by the
quality of the base model’s pre-training. The
construction of a capability library with a fixed
number of clusters further reflects an engineering trade-off: it stabilizes control but may
reduce semantic granularity, potentially oversimplifying the underlying activation manifold
for highly nuanced tasks. Moreover, the extracted vectors predominantly capture broad
domain-level reasoning patterns due to the
natural clustering structure of the model’s activation space. Future work can focus on disentangling these into finer-grained, domainagnostic atomic skills, automating the discovery of such primitives, and exploring hierarchical routing mechanisms to achieve more precise control over complex reasoning chains. Finally, as RISER operates by modifying internal activations, careless application without
proper constraints could lead to unintended
behavioral shifts. In this work, we restrict our
analysis to controlled benchmark settings, and
future deployment-oriented use would require
additional safety and alignment evaluation.


**References**


Janice Ahn, Rishu Verma, Renze Lou, Di Liu, Rui
Zhang, and Wenpeng Yin. 2024. [Large language](https://doi.org/10.18653/v1/2024.eacl-srw.17)
models for [mathematical](https://doi.org/10.18653/v1/2024.eacl-srw.17) reasoning: Progresses
and [challenges.](https://doi.org/10.18653/v1/2024.eacl-srw.17) In _Proceedings_ _of_ _the_ _18th_ _Con-_
_ference_ _of_ _the_ _European_ _Chapter_ _of_ _the_ _Associa-_
_tion for Computational_ _Linguistics:_ _Student Re-_
_search_ _Workshop_, pages 225–237, St. Julian’s,
Malta. Association for Computational Linguistics.


Guillaume Alain and Yoshua Bengio. 2016. Understanding intermediate layers using linear classifier probes. _arXiv_ _preprint_ _arXiv:1610.01644_ .


Michael L. Anderson. 2010. Neural reuse: A fundamental organizational principle of the brain. _Be-_
_havioral_ _and_ _Brain_ _Sciences_, 33(4):245–66; discussion 266–313.


Anthropic. 2024. Model card [addendum:](https://assets.anthropic.com/m/1cd9d098ac3e6467/original/Claude-3-Model-Card-October-Addendum.pdf) Claude
3.5 haiku and [upgraded](https://assets.anthropic.com/m/1cd9d098ac3e6467/original/Claude-3-Model-Card-October-Addendum.pdf) claude 3.5 sonnet.


Lukasz Bartoszcze, Sarthak Munshi, Bryan Sukidi,
Jennifer Yen, Zejia Yang, David Williams-King,
Linh Le, Kosi Asuzu, and Carsten Maple. 2025.



Representation engineering for large-language
models: Survey and research challenges.


Reza Bayat, Ali Rahimi-Kalahroudi, Mohammad
Pezeshki, Sarath Chandar, and Pascal Vincent.
2025. Steering large [language](https://arxiv.org/abs/2503.00177) model activations
in [sparse](https://arxiv.org/abs/2503.00177) spaces. _Preprint_, arXiv:2503.00177.


Yonatan Belinkov. 2022. Probing [classifiers:](https://doi.org/10.1162/coli_a_00422)
Promises, [shortcomings,](https://doi.org/10.1162/coli_a_00422) and advances. _Com-_
_putational_ _Linguistics_, 48(1):207–219.


Tom Brown, Benjamin Mann, Nick Ryder, Melanie
Subbiah, Jared D Kaplan, Prafulla Dhariwal,
Arvind Neelakantan, Pranav Shyam, Girish Sastry, Amanda Askell, and 1 others. 2020. Language models are few-shot learners. _Advances in_
_neural_ _information_ _processing_ _systems_, 33:1877–
1901.


Yupeng Chang, Xu Wang, Jindong Wang, Yuan
Wu, Linyi Yang, Kaijie Zhu, Hao Chen, Xiaoyuan Yi, Cunxiang Wang, Yidong Wang, Wei
Ye, Yue Zhang, Yi Chang, Philip S. Yu, Qiang
Yang, and Xing Xie. 2024. A [survey](https://doi.org/10.1145/3641289) on evaluation of large [language](https://doi.org/10.1145/3641289) models. _ACM_ _Trans._
_Intell._ _Syst._ _Technol._, 15(3).


Mark Chen, Jerry Tworek, Heewoo Jun, Qiming Yuan, Henrique Ponde de Oliveira Pinto,
Jared Kaplan, Harri Edwards, Yuri Burda,
Nicholas Joseph, Greg Brockman, Alex Ray,
Raul Puri, Gretchen Krueger, Michael Petrov,
Heidy Khlaaf, Girish Sastry, Pamela Mishkin,
Brooke Chan, Scott Gray, and 39 others. 2021.
Evaluating large [language](https://arxiv.org/abs/2107.03374) models trained on
[code.](https://arxiv.org/abs/2107.03374) _Preprint_, arXiv:2107.03374.


Runjin Chen, Andy Arditi, Henry Sleight, Owain
Evans, and Jack Lindsey. 2025. [Persona vectors:](https://arxiv.org/abs/2507.21509)
Monitoring and [controlling](https://arxiv.org/abs/2507.21509) character traits in
[language](https://arxiv.org/abs/2507.21509) models. _Preprint_, arXiv:2507.21509.


Peter Clark, Isaac Cowhey, Oren Etzioni, Tushar
Khot, and Oyvind Tafjord. 2018. Think you
have solved question answering? try arc, the
ai2 reasoning challenge.


Karl Cobbe, Vineet Kosaraju, Mohammad Bavarian, Jacob Hilton, Reiichiro Nakano, Christopher Hesse, and John Schulman. 2021. Training
verifiers to solve math word problems.


Hoagy Cunningham, Aidan Ewart, Logan Riggs
Smith, Robert Huben, and Lee Sharkey.
2023. Sparse [autoencoders](https://api.semanticscholar.org/CorpusID:261934663) find highly interpretable features [in](https://api.semanticscholar.org/CorpusID:261934663) language models. _ArXiv_,
abs/2309.08600.


Hannah Cyberey and David Evans. 2025. [Steer-](https://openreview.net/forum?id=dVqZBagXF3)
ing the censorship: [Uncovering](https://openreview.net/forum?id=dVqZBagXF3) representation
vectors for LLM [”thought”](https://openreview.net/forum?id=dVqZBagXF3) control. In _Second_
_Conference_ _on_ _Language_ _Modeling_ .


Fei Ding and Baiqiao Wang. 2025. [Improved](https://api.semanticscholar.org/CorpusID:279306288) supervised fine-tuning [for](https://api.semanticscholar.org/CorpusID:279306288) large language models to mitigate [catastrophic](https://api.semanticscholar.org/CorpusID:279306288) forgetting. _ArXiv_,
abs/2506.09428.


Harshwardhan Fartale, Ashish Kattamuri, Rahul
Raja, Arpita Vats, Ishita Prasad, and Akshata Kishore Moharir. 2025. [Disentangling](https://arxiv.org/abs/2510.03366)
recall and reasoning [in](https://arxiv.org/abs/2510.03366) transformer models
through layer-wise [attention](https://arxiv.org/abs/2510.03366) and activation
[analysis.](https://arxiv.org/abs/2510.03366) _Preprint_, arXiv:2510.03366.


William Fedus, Barret Zoph, and Noam Shazeer.
2022. Switch transformers: Scaling to trillion
parameter models with simple and efficient sparsity. _Journal_ _of_ _Machine_ _Learning_ _Research_,
23(120):1–39.


Aaron Grattafiori, Abhimanyu Dubey, Abhinav
Jauhri, Abhinav Pandey, Abhishek Kadian, Ahmad Al-Dahle, Aiesha Letman, Akhil Mathur,
Alan Schelten, Alex Vaughan, Amy Yang, Angela Fan, Anirudh Goyal, Anthony Hartshorn,
Aobo Yang, Archi Mitra, Archie Sravankumar,
Artem Korenev, Arthur Hinsvark, and 542 others. 2024. [The llama 3 herd of models.](https://arxiv.org/abs/2407.21783) _Preprint_,
arXiv:2407.21783.


Yixin He and Lumingyuan Tang. 2025. [Learning](https://arxiv.org/abs/2509.24238)
to ponder: Adaptive [reasoning](https://arxiv.org/abs/2509.24238) in latent space.
_Preprint_, arXiv:2509.24238.


Dan Hendrycks, Collin Burns, Steven Basart, Andrew Critch, Jerry Li, Dawn Song, and Jacob Steinhardt. 2021a. Aligning ai with shared
human values. _Proceedings_ _of_ _the_ _Interna-_
_tional_ _Conference_ _on_ _Learning_ _Representations_
_(ICLR)_ .


Dan Hendrycks, Collin Burns, Steven Basart,
Andy Zou, Mantas Mazeika, Dawn Song, and
Jacob Steinhardt. 2021b. [Measuring](https://arxiv.org/abs/2009.03300) massive
multitask [language](https://arxiv.org/abs/2009.03300) understanding. _Preprint_,
arXiv:2009.03300.


Dan Hendrycks, Collin Burns, Saurav Kadavath,
Akul Arora, Steven Basart, Eric Tang, Dawn
Song, and Jacob Steinhardt. 2021c. [Measuring](https://datasets-benchmarks-proceedings.neurips.cc/paper_files/paper/2021/file/be83ab3ecd0db773eb2dc1b0a17836a1-Paper-round2.pdf)
mathematical problem solving with the math
[dataset.](https://datasets-benchmarks-proceedings.neurips.cc/paper_files/paper/2021/file/be83ab3ecd0db773eb2dc1b0a17836a1-Paper-round2.pdf) In _Proceedings_ _of_ _the_ _Neural_ _Informa-_
_tion_ _Processing_ _Systems_ _Track_ _on_ _Datasets_ _and_
_Benchmarks_, volume 1.


Bertram Hø jer, Oliver Jarvis, and Stefan Heinrich.
2025. [Improving reasoning performance in large](https://proceedings.iclr.cc/paper_files/paper/2025/file/6e73c39cc428c7d264d9820319f31e79-Paper-Conference.pdf)
language models via [representation](https://proceedings.iclr.cc/paper_files/paper/2025/file/6e73c39cc428c7d264d9820319f31e79-Paper-Conference.pdf) engineering.
In _International_ _Conference_ _on_ _Representation_
_Learning_, volume 2025, pages 44746–44763.


Maggie Huan, Yuetai Li, Tuney Zheng, Xiaoyu Xu,
Seungone Kim, Minxin Du, Radha Poovendran,
Graham Neubig, and Xiang Yue. 2025. [Does](https://arxiv.org/abs/2507.00432)
math reasoning [improve](https://arxiv.org/abs/2507.00432) general llm capabilities? understanding [transferability](https://arxiv.org/abs/2507.00432) of llm rea[soning.](https://arxiv.org/abs/2507.00432) _Preprint_, arXiv:2507.00432.



Eric Jang, Shixiang Gu, and Ben Poole. 2017.

Categorical [reparameterization](https://openreview.net/forum?id=rkE3y85ee) with gumbel[softmax.](https://openreview.net/forum?id=rkE3y85ee) In _5th_ _International_ _Conference_ _on_
_Learning_ _Representations,_ _ICLR_ _2017,_ _Toulon,_
_France,_ _April_ _24-26,_ _2017,_ _Conference_ _Track_
_Proceedings_ . OpenReview.net.


Haoran Jin, Meng Li, Xiting Wang, Zhihao Xu,
Minlie Huang, Yantao Jia, and Defu Lian. 2025.
[Internal value alignment in large language mod-](https://doi.org/10.18653/v1/2025.acl-long.1326)
els through controlled value vector activation.
In _Proceedings_ _of_ _the_ _63rd_ _Annual_ _Meeting_ _of_
_the_ _Association_ _for_ _Computational_ _Linguistics_
_(Volume_ _1:_ _Long_ _Papers)_, pages 27347–27371,
Vienna, Austria. Association for Computational
Linguistics.


Nancy Kanwisher, Josh Mcdermott, and Marvin M. Chun. 1999. The fusiform face area:
A module in human extrastriate cortex specialized for face perception. _The_ _Journal_ _of_ _Neuro-_
_science_, 17(11).


Bruce W. Lee, Inkit Padhi, Karthikeyan Natesan Ramamurthy, Erik Miehling, Pierre Dognin,
Manish Nagireddy, and Amit Dhurandhar.
2025a. Programming [refusal](https://arxiv.org/abs/2409.05907) with conditional
[activation](https://arxiv.org/abs/2409.05907) steering. _Preprint_, arXiv:2409.05907.


Sunbowen Lee, Qingyu Yin, Chak Tou Leong,
Jialiang Zhang, Yicheng Gong, and Xiaoyu
Shen. 2025b. Probing the [difficulty](https://arxiv.org/abs/2510.05969) perception
mechanism of [large](https://arxiv.org/abs/2510.05969) language models. _Preprint_,
arXiv:2510.05969.


Hongyu Li, Liang Ding, Meng Fang, and Dacheng
Tao. 2024. Revisiting [catastrophic](https://doi.org/10.18653/v1/2024.findings-emnlp.249) forgetting
in large [language](https://doi.org/10.18653/v1/2024.findings-emnlp.249) model tuning. In _Findings_
_of_ _the_ _Association_ _for_ _Computational_ _Linguis-_
_tics:_ _EMNLP_ _2024_, pages 4297–4308, Miami,
Florida, USA. Association for Computational
Linguistics.


Zhong-Zhi Li, Duzhen Zhang, Ming-Liang Zhang,
Jiaxin Zhang, Zengyan Liu, Yuxuan Yao, Haotian Xu, Junhao Zheng, Pei-Jie Wang, Xiuyi
Chen, Yingying Zhang, Fei Yin, Jiahua Dong,
Zhiwei Li, Bao-Long Bi, Ling-Rui Mei, Junfeng
Fang, Xiao Liang, Zhijiang Guo, and 2 others.
2025. From system 1 to [system](https://arxiv.org/abs/2502.17419) 2: A survey
of reasoning [large](https://arxiv.org/abs/2502.17419) language models. _Preprint_,
arXiv:2502.17419.


Mengqi Liao, Xiangyu Xi, Ruinian Chen, Jia
Leng, Yangen Hu, Ke Zeng, Shuai Liu, and
Huaiyu Wan. 2025. Enhancing [efficiency](https://arxiv.org/abs/2505.18573) and
exploration in [reinforcement](https://arxiv.org/abs/2505.18573) learning for llms.
_Preprint_, arXiv:2505.18573.


Stephanie Lin, Jacob Hilton, and Owain Evans.
2022. TruthfulQA: [Measuring](https://doi.org/10.18653/v1/2022.acl-long.229) how models
mimic [human](https://doi.org/10.18653/v1/2022.acl-long.229) falsehoods. In _Proceedings_ _of_
_the_ _60th_ _Annual_ _Meeting_ _of_ _the_ _Association_ _for_
_Computational Linguistics (Volume 1:_ _Long Pa-_
_pers)_, pages 3214–3252, Dublin, Ireland. Association for Computational Linguistics.


Samuel Marks and Max Tegmark. 2023. [The](https://api.semanticscholar.org/CorpusID:263831277) geometry of truth: [Emergent](https://api.semanticscholar.org/CorpusID:263831277) linear structure in
large language model [representations](https://api.semanticscholar.org/CorpusID:263831277) of true/false [datasets.](https://api.semanticscholar.org/CorpusID:263831277) _ArXiv_, abs/2310.06824.


Earl K. Miller and Jonathan D. Cohen. 2001. [An](https://doi.org/10.1146/annurev.neuro.24.1.167)
integrative theory of [prefrontal](https://doi.org/10.1146/annurev.neuro.24.1.167) cortex function.
_Annual_ _Review_ _of_ _Neuroscience_, 24(Volume 24,
2001):167–202.


Deepak Babu Piskala, Vijay Raajaa, Sachin
Mishra, and Bruno Bozza. 2024. [Optiroute](https://doi.org/10.5120/ijca2024924172) dynamic llm routing and selection based on user
preferences: Balancing performance, cost, and
[ethics.](https://doi.org/10.5120/ijca2024924172) _International_ _Journal_ _of_ _Computer_ _Ap-_
_plications_, 186(51):1–7.


Joris Postmus and Steven Abreu. 2024. [Steering](https://openreview.net/forum?id=gyAnAq16HC)
large language models using conceptors: Improving addition-based activation engineering.
In _MINT:_ _Foundation_ _Model_ _Interventions_ .


Qwen, :, An Yang, Baosong Yang, Beichen Zhang,
Binyuan Hui, Bo Zheng, Bowen Yu, Chengyuan
Li, Dayiheng Liu, Fei Huang, Haoran Wei, Huan
Lin, Jian Yang, Jianhong Tu, Jianwei Zhang,
Jianxin Yang, Jiaxi Yang, Jingren Zhou, and
25 others. 2025. Qwen2.5 [technical](https://arxiv.org/abs/2412.15115) report.
_Preprint_, arXiv:2412.15115.


David Rein, Betty Li Hou, Asa Cooper Stickland,
Jackson Petty, Richard Yuanzhe Pang, Julien
Dirani, Julian Michael, and Samuel R. Bowman.
2023. Gpqa: A [graduate-level](https://api.semanticscholar.org/CorpusID:265295009) google-proof q&a
[benchmark.](https://api.semanticscholar.org/CorpusID:265295009) _ArXiv_, abs/2311.12022.


Nina Rimsky, Nick Gabrieli, Julian Schulz, Meg
Tong, Evan Hubinger, and Alexander Turner.
2024. Steering llama 2 [via](https://doi.org/10.18653/v1/2024.acl-long.828) contrastive activation [addition.](https://doi.org/10.18653/v1/2024.acl-long.828) In _Proceedings_ _of_ _the_ _62nd_
_Annual_ _Meeting_ _of_ _the_ _Association_ _for_ _Compu-_
_tational_ _Linguistics_ _(Volume_ _1:_ _Long_ _Papers)_,
pages 15504–15522, Bangkok, Thailand. Association for Computational Linguistics.


Zhihong Shao, Peiyi Wang, Qihao Zhu, Runxin
Xu, Junxiao Song, Xiao Bi, Haowei Zhang,
Mingchuan Zhang, YK Li, Yang Wu, and 1 others. 2024. Deepseekmath: Pushing the limits of
mathematical reasoning in open language models. _arXiv_ _preprint_ _arXiv:2402.03300_ .


Noam Shazeer, Azalia Mirhoseini, Krzysztof
Maziarz, Andy Davis, Quoc Le, Geoffrey Hinton, and Jeff Dean. 2017. [Outrageously](https://doi.org/10.48550/arXiv.1701.06538) large
neural networks: The [sparsely-gated](https://doi.org/10.48550/arXiv.1701.06538) mixture[of-experts](https://doi.org/10.48550/arXiv.1701.06538) layer.


Idan Shenfeld, Jyothish Pari, and Pulkit Agrawal.
2025. Rl’s razor: Why online reinforcement learning forgets less. _arXiv_ _preprint_
_arXiv:2509.04259_ .


Wenhao Shi, Zhiqiang Hu, Yi Bin, Junhua Liu,
Yang Yang, See Kiong Ng, Lidong Bing, and



Roy Ka-Wei Lee. 2024. Math-llava: Bootstrapping mathematical reasoning for multimodal
large language models. In _Findings_ _of_ _the_ _Asso-_
_ciation_ _for_ _Computational_ _Linguistics:_ _EMNLP_
_2024_, pages 4663–4680.


Mirac Suzgun, Nathan Scales, Nathanael Sch¨arli,
Sebastian Gehrmann, Yi Tay, Hyung Won
Chung, Aakanksha Chowdhery, Quoc V. Le,
Ed H. Chi, Denny Zhou, and Jason Wei.
2022. Challenging [big-bench](https://arxiv.org/abs/2210.09261) tasks and whether
chain-of-thought can solve them. _Preprint_,
arXiv:2210.09261.


Daniel Tan, David Chanin, Aengus Lynch, Brooks
Paige, Dimitrios Kanoulas, Adri`a GarrigaAlonso, and Robert Kirk. 2024. [Analysing](https://proceedings.neurips.cc/paper_files/paper/2024/file/fb3ad59a84799bfb8d700e56d19c231b-Paper-Conference.pdf) the
[generalisation and reliability of steering vectors.](https://proceedings.neurips.cc/paper_files/paper/2024/file/fb3ad59a84799bfb8d700e56d19c231b-Paper-Conference.pdf)
In _Advances_ _in_ _Neural_ _Information_ _Processing_
_Systems_, volume 37, pages 139179–139212. Curran Associates, Inc.


Hugo Touvron, Thibaut Lavril, Gautier Izacard,
Xavier Martinet, Marie-Anne Lachaux, Timoth´ee Lacroix, Baptiste Rozi`ere, Naman Goyal,
Eric Hambro, Faisal Azhar, and 1 others. 2023.
Llama: Open and efficient foundation language
models. _arXiv_ _preprint_ _arXiv:2302.13971_ .


Alexander Matt Turner, Lisa Thiergart, Gavin
Leech, David Udell, Juan J. Vazquez, Ulisse
Mini, and Monte Macdiarmid. 2023. Steering
language models with activation engineering.


Marco Valentino, Geonhee Kim, Dhairya Dalal,
Zhixue Zhao, and Andr´e Freitas. 2025. Mitigating content effects on reasoning in language
models through fine-grained activation steering.
_arXiv_ _preprint_ _arXiv:2505.12189_ .


Constantin Venhoff, Iv´an Arcuschin, Philip Torr,
Arthur Conmy, and Neel Nanda. 2025a. Base
models know how to reason, thinking models
learn when. _arXiv_ _preprint_ _arXiv:2510.07364_ .


Constantin Venhoff, Iv´an Arcuschin, Philip Torr,
Arthur Conmy, and Neel Nanda. 2025b. [Under-](https://openreview.net/forum?id=OwhVWNOBcz)
standing reasoning in [thinking](https://openreview.net/forum?id=OwhVWNOBcz) language models
via [steering](https://openreview.net/forum?id=OwhVWNOBcz) vectors. In _Workshop_ _on_ _Reasoning_
_and_ _Planning_ _for_ _Large_ _Language_ _Models_ .


Mengru Wang, Ziwen Xu, Shengyu Mao, Shumin
Deng, Zhaopeng Tu, Huajun Chen, and Ningyu
Zhang. 2025a. [Beyond prompt engineering:](https://doi.org/10.18653/v1/2025.acl-long.1139) Robust behavior control [in](https://doi.org/10.18653/v1/2025.acl-long.1139) LLMs via steering target [atoms.](https://doi.org/10.18653/v1/2025.acl-long.1139) In _Proceedings_ _of_ _the_ _63rd_ _Annual_
_Meeting_ _of_ _the_ _Association_ _for_ _Computational_
_Linguistics_ _(Volume_ _1:_ _Long_ _Papers)_, pages
23381–23399, Vienna, Austria. Association for
Computational Linguistics.


Ruonan Wang, Runxi Wang, Yunwen Shen,
Chengfeng Wu, Qinglin Zhou, and Rohitash
Chandra. 2025b. Evaluation of llms for mathematical problem solving. _arXiv_ _preprint_
_arXiv:2506.00309_ .


Xin Wang, Haoyang Li, Zeyang Zhang, Haibo
Chen, and Wenwu Zhu. 2025c. [Modular](https://doi.org/10.48550/ARXIV.2504.20020) machine learning: An [indispensable](https://doi.org/10.48550/ARXIV.2504.20020) path towards
new-generation [large](https://doi.org/10.48550/ARXIV.2504.20020) language models. _CoRR_,
abs/2504.20020.


Xuezhi Wang, Jason Wei, Dale Schuurmans,
Quoc V. Le, Ed H. Chi, Sharan Narang,
Aakanksha Chowdhery, and Denny Zhou. 2023.
Self-consistency [improves](https://openreview.net/forum?id=1PL1NIMMrw) chain of thought reasoning in [language](https://openreview.net/forum?id=1PL1NIMMrw) models. In _The_ _Eleventh_
_International Conference on Learning Represen-_
_tations,_ _ICLR_ _2023,_ _Kigali,_ _Rwanda,_ _May_ _1-5,_
_2023_ . OpenReview.net.


Yubo Wang, Xueguang Ma, Ge Zhang, Yuansheng Ni, Abhranil Chandra, Shiguang Guo,
Weiming Ren, Aaran Arulraj, Xuan He, Ziyan
Jiang, Tianle Li, Max Ku, Kai Wang, Alex
Zhuang, Rongqi Fan, Xiang Yue, and Wenhu
Chen. 2025d. Mmlu-pro: a more robust and
challenging multi-task language understanding
benchmark. In _Proceedings_ _of_ _the_ _38th_ _Interna-_
_tional_ _Conference_ _on_ _Neural_ _Information_ _Pro-_
_cessing_ _Systems_, NeurIPS ’24, Red Hook, NY,
USA. Curran Associates Inc.


Jason Wei, Yi Tay, Rishi Bommasani, Colin Raffel, Barret Zoph, Sebastian Borgeaud, Dani Yogatama, Maarten Bosma, Denny Zhou, Donald
Metzler, and 1 others. 2022a. Emergent abilities of large language models. _arXiv_ _preprint_
_arXiv:2206.07682_ .


Jason Wei, Xuezhi Wang, Dale Schuurmans,
Maarten Bosma, brian ichter, Fei Xia, Ed Chi,
Quoc V Le, and Denny Zhou. 2022b. [Chain-](https://proceedings.neurips.cc/paper_files/paper/2022/file/9d5609613524ecf4f15af0f7b31abca4-Paper-Conference.pdf)
of-thought prompting [elicits](https://proceedings.neurips.cc/paper_files/paper/2022/file/9d5609613524ecf4f15af0f7b31abca4-Paper-Conference.pdf) reasoning in large
[language](https://proceedings.neurips.cc/paper_files/paper/2022/file/9d5609613524ecf4f15af0f7b31abca4-Paper-Conference.pdf) models. In _Advances_ _in_ _Neural_ _In-_
_formation_ _Processing_ _Systems_, volume 35, pages
24824–24837. Curran Associates, Inc.


Yuyang Wu, Yifei Wang, Ziyu Ye, Tianqi Du, Stefanie Jegelka, and Yisen Wang. 2025. [When](https://arxiv.org/abs/2502.07266)
more is less: [Understanding](https://arxiv.org/abs/2502.07266) chain-of-thought
length in llms. _Preprint_, arXiv:2502.07266.


Mohammad Zbeeb, Hasan Abed Al Kader Hammoud, and Bernard Ghanem. 2025. [Rea-](https://arxiv.org/abs/2509.01363)
soning vectors: [Transferring](https://arxiv.org/abs/2509.01363) chain-of-thought
capabilities via task arithmetic. _Preprint_,
arXiv:2509.01363.


Hanyu Zhang, Xiting Wang, Chengao Li, Xiang
Ao, and Qing He. 2025a. [Controlling](https://doi.org/10.1609/aaai.v39i24.34778) large language models through concept activation vec[tors.](https://doi.org/10.1609/aaai.v39i24.34778) _Proceedings_ _of_ _the_ _AAAI_ _Conference_ _on_
_Artificial_ _Intelligence_, 39(24):25851–25859.


Yi-Kai Zhang, De-Chuan Zhan, and Han-Jia Ye.
2025b. Capability [instruction](https://doi.org/10.1609/aaai.v39i24.34790) tuning. _Proceed-_
_ings_ _of_ _the_ _AAAI_ _Conference_ _on_ _Artificial_ _Intel-_
_ligence_, 39:25958–25966.



Figure 7: All baselines choose incorrectly, while
RISER selects the correct answer and grounds its
explanation in the rise of modern capitalism.


**A** **Case** **Study**


Figure 7 presents a qualitative comparison
where RISER successfully navigates conceptual traps. While the base model, CoT
prompting, and even stronger frontier models
are lured into selecting Bureaucracy by misleading lexical cues despite generating superficially coherent rationales, RISER correctly
identifies that Capitalism aligns with Weber’s
theory. Analysis of the routing weights reveals that RISER selectively amplifies logical
reasoning and domain knowledge primitives
while suppressing irrelevant directions, effectively steering the model’s focus.


**B** **Transferability** **Across** **Domains**


We further evaluated RISER directly on the
Big-Bench Hard (BBH) benchmark (Suzgun
et al., 2022) without any additional finetuning. Despite the significant distribution
shift moving from knowledge-centric exams to
pure symbolic tasks, RISER outperformed the
base model by 2.8%. Crucially, the Router
autonomously adapted its strategy by prioritizing general-purpose primitives, specifically
Logical Reasoning and Reading Comprehension. This transferability suggests that these
primitives capture content-agnostic cognitive
mechanisms akin to fluid intelligence and the
system successfully identifies that the underlying computational demand remains constant
even when the surface-level domain changes,
verifying that RISER orchestrates genuine,
transferable mental skills.










**C** **Transferability** **Across** **Models**


To delineate the generalization boundaries of
the RISER framework, we systematically investigate the transferability of learned Routers
across distinct model families and varying parameter scales in Table 3. Specifically, we apply a Router trained on a source model directly to a target model without any additional tuning. This experiment aims to determine whether the learned cognitive compositions capture universal reasoning patterns or
remain specific to the internal representation
space of the source architecture.


**C.1** **Cross-Architecture**
**Transferability**


We first evaluate Router transferability between distinct model families, specifically exchanging Routers between Qwen2.5-7B and
Llama-3-8B. Empirical results demonstrate
negligible generalization, with performance regressing to near-random or baseline levels.
This failure suggests that the learned reasoning vectors and routing policies are inextricably coupled to the specific manifold of
each model family. We attribute this incompatibility to three primary factors. First,
stochastic pre-training induces manifold misalignment, where semantically similar concepts acquire arbitrary geometric orientations
in high-dimensional space, precluding natural isometry between families without explicit
alignment. Second, variations in pre-training
corpora and tokenizers yield divergent activation statistics, causing source vectors to
map onto low-density or undefined regions in
the target manifold. Third, architectural inductive biases—arising from structural differences such as Grouped-Query Attention versus Multi-Head Attention—fundamentally reshape the activation landscape geometry, rendering direct vector transplantation mathematically invalid.


**C.2** **Intra-Family** **Transferability:**
**Scale** **Invariance**


Conversely, transferring Routers within the
same model family (e.g., across the Qwen2.5
series) yields substantial efficacy, indicating a
shared semantic alignment across scales. We
observe two distinct phenomena based on the
direction of transfer.



**Large-to-Small** **Transfer** **(Inference-**
**Time** **Distillation).** Transferring a Router
from a larger model (e.g., 32B) to a smaller
one (e.g., 7B) results in significant accuracy
gains of up to **+5%** . We posit that the Router
derived from the larger model encapsulates
more precise and robust cognitive strategies.
Deploying this advanced policy on a smaller
model functions as a form of inference-time
distillation, effectively guiding the smaller
model to navigate complex reasoning pathways that it fails to autonomously discover
due to limited capacity.


**Small-to-Large** **Transfer** **(Feature** **Con-**
**sistency).** Transferring from smaller to
larger models also confers meaningful improvements, typically enhancing accuracy by **+2–**
**3%** . This finding demonstrates scalable feature consistency, implying that the fundamental cognitive directions identified in smaller
parameter regimes remain preserved and refined in larger models. Consequently, the
lightweight Router maintains its steering effectiveness even as the backbone capacity increases, highlighting the hierarchical stability
of the learned representations within the same
lineage.


**D** **Implementation** **&** **Training**
**Details**


**D.1** **Hyperparameters**


In Table 4, we list the training configuration
and used hyperparameters during our experiment. Full framework code will be released
once accepted. Experiment is conducted on
RTX5090 GPU. We report accuracy for each
benchmark and average performance across
task groups and results are computed from
random seeds (average performance on 3 runs)
and report absolute accuracy and relative improvements over baselines.


**D.2** **Datasets** **Configuration**


Our training pipeline consists of three distinct
phases, each utilizing a specific data strategy
to ensure the robustness and capabilities of the
RISER framework.


**Phase** **1:** **Reasoning** **Vector** **Elicita-**
**tion** **Data.** To construct a comprehensive
library of cognitive primitives, we require a
dataset that covers a broad spectrum of rea

Table 4: Hyperparameters and implementation details for RISER training.


**Hyperparameter** **Value**


_Model_ _Architecture_ _&_ _Optimization_ _Strategy_
Advantage Estimator GRPO
Base LLM Trainable False
Router Trainable True


_Training_ _Configuration_
SFT Learning Rate 5 _×_ 10 _[−]_ [6]

SFT Epochs 3
RL Learning Rate 2 _×_ 10 _[−]_ [6]

Total RL Epochs 2
Global Batch Size 128
Max Context Length 8192
Data Shuffling True


_Reward_ _&_ _KL_ _Divergence_
Reward Type Accuracy (0/1)
KL Loss Coefficient 0.001
KL Loss Type Low Variance KL


_Rollout_ _&_ _Generation_
Temperature 1.5
Top-k -1 (Disabled)
Do Sample True
Number of Rollouts ( _N_ ) 8
Max Batched Tokens 8192


_Infrastructure_ _&_ _Parallelism_
Tensor Parallel Size 4
GPUs per Node 4
Number of Nodes 1


soning types. We constructed the elicitation dataset by performing **random** **sam-**
**pling** of 500 examples from the **MMLU**
benchmark (Hendrycks et al., 2021b). Given
MMLU’s inherent breadth across diverse subjects, ranging from elementary mathematics
to professional law, this random sampling
strategy ensures that the extracted vectors
cover a diverse spectrum of cognitive reasoning
patterns without introducing domain-specific
bias.

For each question, we generated several
paired activation states using the _Positive_ and
_Negative_ prompts (see Appendix G). To ensure quality, we applied the LLM-Judge filtering mechanism described in Section 4, retaining only pairs that exhibit a significant gap
in reasoning rigor, paving the path for further
experiments.


**Phase** **2:** **Router** **SFT** **Data** **(Oracle** **La-**
**bel** **Synthesis).** For the supervised warmup, we utilized a separate set of 200 MMLU



samples (non-overlapping with the elicitation
set). To synthesize the ground-truth ”Oracle
Labels” for training the Router, we employed
a **constrained** **grid** **search** mechanism. For
each query, we first ranked the primitives
based on their individual efficacy and preselected the **top-2** candidates. Within this reduced subspace, we performed a fine-grained
grid search over the intervention strength _α_,
discretizing the value with a step size of **0.1**
(ranging from 0 to _α_ max). The configuration ( **w** _[∗]_ _,_ _**α**_ _[∗]_ ) that elicited the correct response
with the highest confidence was selected as
the supervisory target. This approach efficiently provides high-quality initialization for
the Router without the computational cost of
an exhaustive search over the entire combinatorial space.


**Phase** **3:** **RL** **Refinement** **Data.** To further optimize the Router for complex composition and generalization, we employed
the **MMLU-Pro** benchmark. MMLU-Pro
presents a significantly harder challenge with
distractor options and complex reasoning
chains, providing a steeper gradient for reinforcement learning compared to standard
MMLU. We randomly split the dataset into
a Training Set (70%) for the GRPO algorithm
and a Held-out Set (30%) for validation. Importantly, we strictly ensured **no** **question**
**overlap** between the RL training set and the
final evaluation benchmarks (Table 1) to prevent data leakage and ensure fair evaluation.


**E** **RISER** **Inference** **Procedure**


Algorithm 1 provides pseudocode for our inference pipeline: we invoke the Router once after the prompt prefill to compute an injection
vector _v_ inject, and then reuse the same _v_ inject
as an additive intervention at layer _l_ for the
last-token activation at every decoding step.


**F** **Sensitivity** **Analysis** **of** **Cluster**
**Count** **(** _K_ **)**


We fixed the size of the cognitive primitive library at _K_ = 6 based on the observation that
the first six principal components account for
over 85% of the variance in the extracted difference vectors. To empirically validate this
choice and assess the sensitivity of RISER to
the granularity of the primitive library, we
conducted an ablation study with varying clus

**Algorithm** **1** RISER inference


**Require:** Frozen LLM _fθ_ ( _L_ layers), Router
_gϕ_, primitives _V_ = _{vi}_ _[K]_ _i_ =1 [,] [layer] [index] _[l]_ [,]
threshold _τ_, _α_ max, prompt tokens _x_, max
steps _T_
**Ensure:** Generated tokens _y_

1: **Prefill** **(compute** _v_ **inject** **once)** :

2: _hl_ _←_ ForwardToLayer( _fθ, x, l_ ) _▷_
last-token state at layer _l_

3: ( _p, α_ ) _←_ _gϕ_ ( _hl_ ) _▷p ∈_ [0 _,_ 1] _[K]_ _,_ _α ∈_ R _[K]_

4: **for** _i_ = 1 to _K_ **do**

5: _wi_ _←_ I[ _pi_ _> τ_ ]

6: _αi_ _←_ clip( _αi,_ 0 _, α_ max)

7: **end** **for**

8: _v_ inject _←_ [�] _[K]_ _i_ =1 _[w][i][ α][i][ v][i]_
9: **Decoding** **(reuse** **the** **same** _v_ **inject** **at**
**every** **step)** :

10: _y_ _←_ [ ]

11: **for** _t_ = 1 to _T_ **do**



12: _h_ [(] _l_ _[t]_ [)] _←_ ForwardToLayer( _fθ, x∥y, l_ )



13: _h_ ˜ [(] _l_ _[t]_ [)] _←_ _h_ [(] _l_ _[t]_ [)] + _v_ inject
14: logits [(] _[t]_ [)] _←_
ContinueFromLayer( _fθ,_ _h_ [˜][(] _l_ _[t]_ [)] _[, l]_ [)]



15: _yt_ _←_ DecodeToken(logits [(] _[t]_ [)] )



16: _y_ _←_ _y∥_ [ _yt_ ]

17: **if** _yt_ is EOS **then**

18: **break**

19: **end** **if**

20: **end** **for**

21: **return** _y_


ter counts _K_ _∈{_ 4 _,_ 6 _,_ 8 _,_ 12 _}_ . We evaluated
these variants on Qwen2.5-7B-Instruct using
three benchmarks that require distinct reasoning capabilities: GSM8K (Math), GPQA
(General/Scientific), and TruthfulQA (Safety/Alignment). All other hyperparameters
were held constant.


**Primitives** **(** _K_ **)** **Variance** **Explanation** **(PCA)** **GSM8K** **GPQA** **TruthfulQA** **Avg.**


_K_ = 4 72.4% 83.1 33.5 56.2 57.6
_K_ = 6 **(Ours)** **86.1%** **85.2** **36.8** 59.8 **60.6**
_K_ = 8 89.3% 85.0 36.4 **60.1** 60.5
_K_ = 12 93.5% 84.6 35.9 59.5 60.0

Table 5: **Sensitivity** **Analysis** **of** **Cluster**
**Count** **(** _K_ **).** We report the percentage of variance
explained by the top- _K_ principal components and
the zero-shot accuracy across three representative
benchmarks. _K_ = 6 strikes the optimal balance
between performance and model complexity.


The results, summarized in Table 5, demonstrate that _K_ = 6 is not merely an arbitrary
choice but a local optimum for performance.



**Under-clustering** **(** _K_ = 4 **):** Reducing
the number of primitives leads to a noticeable performance drop ( _−_ 3 _._ 0% average accuracy compared to _K_ = 6). With only 72.4% of
the variance explained, distinct cognitive functions (e.g., _Numerical_ _Calculation_ and _Logical_
_Reasoning_ ) are forced to merge into coarser
centroids. This _semantic_ _collision_ reduces the
precision of the steering vectors, preventing
the Router from isolating the specific capability required for specialized tasks like GSM8K.
**Over-clustering** **(** _K_ = 8 _,_ 12 **):** Increasing
_K_ beyond 6 yields diminishing returns. While
the explained variance increases to 93.5% at
_K_ = 12, the downstream accuracy plateaus
or slightly degrades. We attribute this to two
factors:
(1) _Redundancy_ : Higher _K_ values introduce
collinear vectors that represent fine-grained
nuances rather than distinct skills, reducing
the orthogonality of the library.
(2) _Optimization_ _Difficulty_ : A larger action
space complicates the RL exploration process.
The Router struggles to distinguish between
redundant vectors given the sparse reward signal, leading to less stable policies.
Consequently, _K_ = 6 provides the most
robust trade-off, ensuring sufficient semantic
coverage to handle diverse tasks while maintaining a compact and orthogonal action space
for efficient Router learning.


**G** **Prompt** **for** **Reasoning** **Quality**
**Isolation**


To extract reasoning vectors that encode cognitive rigor rather than mere verbosity, we employ a Reasoning Fidelity Contrast strategy.
The goal is to isolate the difference between
**verified** **execution** and **plausible** **genera-**
**tion**, ensuring the extracted vector promotes
efficiency by substituting internal computation for external token generation.


**G.1** **Vector** **Elicitation** **Prompts**


**G.2** **LLM** **Judge** **Filtering** **Criteria**


We employ an LLM Judge to ensure the vector subtraction captures the quality gap. The
judge filters for pairs where the positive response is logically sound (Score _>_ 80) and
the negative response lacks actual reasoning
depth (Score _<_ 20), while maintaining structural similarity.






