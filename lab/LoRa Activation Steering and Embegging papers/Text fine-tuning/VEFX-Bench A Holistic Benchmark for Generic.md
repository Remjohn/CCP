**Xiangbo Gao** [1] _[,]_ [2], **Sicong Jiang** [3], **Bangya Liu** [3], **Xinghao Chen** [1], **Minglai Yang** [3], **Siyuan Yang** [1], **Mingyang Wu** [1], **Jiongze**
**Yu** [1], **Qi Zheng** [2], **Haozhi Wang** [2], **Jiayi Zhang**, **Jie Yang** [2], **Zihan Wang** [3], **Qing Yin** [2], **Zhengzhong Tu** [1] _[,]_ [2]


1Texas A&M University 2Visko Platform 3Abaka AI


**Abstract.** As AI-assisted video creation becomes increasingly practical, instruction-guided video editing
has become essential for refining generated or captured footage to meet professional requirements.
Yet the field still lacks both a large-scale human-annotated dataset with complete editing examples
and a standardized evaluator for comparing editing systems. Existing resources are limited by small
scale, missing edited outputs, or the absence of human quality labels, while current evaluation often
relies on expensive manual inspection or generic vision-language model judges that are not specialized
for editing quality. We introduce `VEFX-Dataset`, a human-annotated dataset containing 5,049 video
editing examples across 9 major editing categories and 32 subcategories, each labeled along three
decoupled dimensions: Instruction Following, Rendering Quality, and Edit Exclusivity. Building
on `VEFX-Dataset`, we propose `VEFX-Reward`, a reward model designed specifically for video editing
quality assessment. `VEFX-Reward` jointly processes the source video, the editing instruction, and the
edited video, and predicts per-dimension quality scores via ordinal regression. We further release
`VEFX-Bench`, a benchmark of 300 curated video-prompt pairs for standardized comparison of editing
systems. Experiments show that `VEFX-Reward` aligns more strongly with human judgments than
generic VLM judges and prior reward models on both standard IQA/VQA metrics and group-wise
preference evaluation. Using `VEFX-Reward` as an evaluator, we benchmark representative commercial
and open-source video editing systems, revealing a gap between visual plausibility, instruction following,
and edit locality in current models.


**Project Homepage:** `[https://xiangbogaobarry.github.io/VEFX-Bench/](https://xiangbogaobarry.github.io/VEFX-Bench/)`

**Date:** April 20, 2026

**Contact:** Xiangbo Gao [(xiangbogaobarry@gmail.com),](mailto:xiangbogaobarry@gmail.com) Zhengzhong Tu

#### **1 Introduction**


The landscape of AI-assisted video creation is advancing rapidly. Recent video generation systems have shown
impressive progress in producing photorealistic clips from natural-language prompts [1–9]. In professional
production workflows, however, a prompt-generated video rarely satisfies the desired result in a single pass; it
typically undergoes multiple rounds of targeted refinement, such as moving objects, adjusting camera motion,
or adding visual effects, before it can be used. As a result, instruction-guided video editing [1, 10, 11], where
a user specifies a natural-language instruction to modify an existing video, has therefore become an essential
component of AI-assisted filmmaking.


Despite rapid progress, the evaluation of video editing and visual effects (VFX) remains fundamentally
unresolved. Unlike generic video generation, video editing must answer at least three distinct questions: Did
the model execute the requested edit? Is the edited video visually coherent and temporally plausible? Did it
preserve content that should have remained unchanged? These requirements expose two major bottlenecks.
First, the field lacks large-scale human-annotated resources that contain complete editing triplets—the source
video, the editing instruction, and the edited result—along with fine-grained quality labels. Second, evaluation
still relies heavily on costly manual inspection or generic vision-language model (VLM) judges that are not
designed for video-editing-specific assessment. The absence of a dedicated automatic evaluator makes both
systematic benchmarking and preference-based optimization difficult.


**VEFX-Dataset**
Step1: Data Collection & Preprocessing



**VEFX-Reward**



Multi-source Data Collection



Data Filtering Final High-Quality Dataset (1419 Videos)



























N-Pairs Video Editing



…


…













Step2: Editing Pair Data Generation

















**output-1** **output-2** **output-3**



Tools-A



Tools-B Tools-C













1419 Raw



9 major tasks

34 subtasks





**org-video**


**org-video**



…



Videos Text Prompt Generation





**output-1** **output-2** **output-3**



**Figure 1** **Overview of our framework.** We construct `VEFX-Dataset`, a human-annotated dataset with 5,049 video editing
examples across 9 categories and 32 subcategories, scored along three decoupled dimensions: Instruction Following
(IF), Rendering Quality (RQ), and Edit Exclusivity (EE). We train `VEFX-Reward`, a dedicated reward model for video
editing quality assessment that takes the original video, editing instruction, and edited video as input and predicts
per-dimension quality scores. We further release `VEFX-Bench`, a benchmark of 300 curated video-prompt pairs for
standardized comparison of editing systems.


Existing resources address only parts of this problem. Benchmarks like EditBoard [12], FiVE-Bench [13], and
IVE-Bench [14] provide instructions without edited outputs; OpenVE [15] offers scale but relies heavily on
automated generation and filtering rather than human annotation; VE-Bench [16] included edited videos
and human scores but reduced quality to a single scalar and are built on older editing systems. On the
reward-model side, prior work focuses on image editing or video generation quality rather than video editing
itself [17, 18]. As a result, there is a pressing need for a benchmark and evaluator that jointly capture
instruction faithfulness, rendering quality, and preservation of unedited content.


To address these gaps, we introduce `VEFX-Dataset`, `VEFX-Reward`, and `VEFX-Bench` . `VEFX-Dataset` contains
5,049 human-annotated video editing examples spanning 9 major categories and 32 fine-grained subcategories.
Each example contains a source video, an editing instruction, and an edited result produced by a diverse
mixture of commercial systems, open-source models, and agentic editing pipelines. Trained annotators score
each example along three decoupled dimensions: Instruction Following (IF), Rendering Quality (RQ), and Edit
Exclusivity (EE). This design is central to the benchmark: an edit may be semantically wrong but visually
clean, or visually strong while unnecessarily modifying non-target content. Building on `VEFX-Dataset`, we
train `VEFX-Reward`, a reward model that takes the source video, the editing instruction, and the edited video
as input and predicts per-dimension quality scores via ordinal regression. We further release `VEFX-Bench`,
a standardized benchmark of 300 curated video-prompt pairs for systematic model comparison, and use
`VEFX-Reward` to evaluate representative commercial and open-source editing systems under the same multidimensional protocol. Our contributions are summarized as follows:


- We construct `VEFX-Dataset`, a human-annotated dataset of 5,049 video editing examples across 9 main
categories and 32 subcategories, generated by a diverse mixture of commercial, open-source, and agentic
editing systems. Each example is scored on a 4-point rubric along three decoupled dimensions: IF, RQ,
and EE. We further release `VEFX-Bench`, a standardized benchmark of 300 curated video-prompt pairs for
comparing editing systems.


- We propose `VEFX-Reward`, the first dedicated reward model for video editing quality assessment. `VEFX-Reward`
jointly reasons over the source video, the editing instruction, and the edited result, and predicts multidimensional quality scores with an ordinal regression objective.


- We conduct comprehensive experiments showing that `VEFX-Reward` aligns more strongly with human
judgments than generic VLM judges and prior reward-model baselines on both standard IQA/VQA
metrics and group-wise preference evaluation. We further apply `VEFX-Reward` to benchmark representative


2


commercial and open-source video editing systems, exposing task-dependent strengths and persistent
weaknesses in instruction following and edit locality.

#### **2 Related Work**


**2.1** **Instruction-Guided Video Editing**


Instruction-guided video editing aims to modify a video according to natural-language instructions while
preserving unrelated content. Early methods extended image editing pipelines to the temporal domain,
typically by introducing temporal attention or consistency modules on top of text-to-image diffusion models

[19, 20]. More recent approaches adopt video-native diffusion or flow-matching architectures. Representative
research models include VACE [10], UniVideo [11], and the broader Wan family [1, 21]. Alongside them,
commercial systems such as Kling Omni, Grok Imagine, Luma Ray2, and the commercial Wan 2.6 service
variant have reached practical quality levels [7, 8, 21, 22]. The resulting ecosystem is highly heterogeneous,
with different systems excelling on different editing types, which makes standardized evaluation increasingly
important.


**2.2** **Video Editing Quality Evaluation**


Evaluating video editing quality is intrinsically multi-faceted. Conventional metrics such as CLIP score, SSIM,
and LPIPS capture only narrow aspects of the problem and do not directly measure instruction fidelity,
temporal consistency, or unintended edits [23, 24]. VBench and VBench++ provide broad evaluation suites
for video generation, but they are not designed for editing, where the source and edited videos must be
considered jointly [25, 26]. Several editing-oriented resources have been introduced more recently. `EditBoard`

[12] and `FiVE` [13] provide useful task-oriented protocols, but at limited scope or scale. `OpenVE-3M` [15]
provides scale without human quality annotation. `IVE-Bench` [14] includes source videos and instructions with
a multi-dimensional protocol, but no edited results. `VE-Bench` [16] includes edited videos and human scores,
but reduces quality to a single scalar MOS. In contrast, `VEFX-Dataset` provides large-scale human-annotated
video editing examples with decoupled quality labels tailored specifically to the editing setting.


**2.3** **Reward Models for Visual Generation**


The success of RLHF in language modeling has motivated analogous efforts in visual generation. For image
generation, reward models such as ImageReward, HPS, and PickScore learn to approximate human preference
signals from large-scale annotations [27–29]. This line of work has extended to image editing: EditReward
trains a multi-dimensional reward model for instruction-guided image editing and demonstrates value for both
evaluation and data curation [17]. In the video domain, VideoScore, VideoReward, DenseDPO, WorldScore,
and Pulse model human preferences or preference-driven alignment primarily for video generation [18, 30–33].
VE-Bench also includes a video editing assessor, but it predicts only a single scalar score and is tied to an
earlier benchmark setting [16]. These methods do not explicitly reason over the relationship between the
source video and the edited result. `VEFX-Reward` addresses this gap by jointly processing the original video,
the editing instruction, and the edited result, and by predicting multi-dimensional quality scores tailored to
video editing.

### 3 VEFX-Dataset and VEFX-Bench


We present `VEFX-Dataset`, a human-annotated dataset for video editing quality evaluation, and `VEFX-Bench`,
a standardized benchmark for systematic model comparison. `VEFX-Dataset` contains 5,049 editing examples—
4,200 for training and 849 for testing—covering 9 major categories and 32 subcategories, each annotated along
three decoupled quality dimensions: Instruction Following (IF), Rendering Quality (RQ), and Edit Exclusivity
(EE). `VEFX-Bench` contains 300 curated (raw video, editing prompt) pairs for evaluating and comparing video
editing models under a standardized protocol. This section describes the data collection process, annotation
protocol, reliability check, and key dataset statistics.


3


Table 1 compares `VEFX-Dataset` with existing video editing datasets along three properties that are particularly
important for reward modeling: whether the dataset includes edited outputs, whether the scores come from
human annotation, and whether quality is decomposed into multiple dimensions. These properties matter
because reward-model training requires actual edited results, reliable human supervision, and labels that
distinguish different failure modes. Several recent resources provide prompts without edited outputs [12–14];
others rely on automated filtering or judge models rather than trained annotators [13, 15]; and some collapse
editing quality into a single scalar. `VEFX-Dataset` is the only dataset in this comparison that satisfies all
three conditions simultaneously.


**Table 1** Comparison of `VEFX-Dataset` with existing video editing datasets. In the “#Cate” column, entries such as
“8/35” denote 8 major categories and 35 subcategories. “Human Ann.” indicates whether quality scores are provided
by human annotators. “Multi-Dim.” indicates whether the evaluation is decomposed into multiple quality dimensions.
“Editing Systems” summarizes the diversity of models used to generate edited videos.


Dataset #Videos #Pairs #Cate Edited Videos Human Ann. Multi-Dim. Editing Systems

`VE-Bench` [16] 169 1,170 6 ✓ ✓ ✗ 8 SD-based open-source (2024)
`EditBoard` [12]  -  - 4 ✗  -  -  `FiVE` [13] _∼_ 100 420 6 ✗  -  -  `OpenVE-3M` [15] 1M 3M 8 ✓ ✗ ✓ Open-source + agentic (2025)
`IVE-Bench` [14] 600  - 8/35 ✗  -  -  `VEFX-Dataset` (Ours) 1,988 5,049 9/32 ✓ ✓ ✓ 4 Commercial + Open + Agentic (2026)


**3.1** **Data Collection**


**Source** **videos.** We curate source videos from open-source video datasets including Open-Sora [34] and
OpenVid-1M [35], supplemented with privately collected footage for additional diversity. We filter the initial
pool for quality and usability, including sufficient resolution, duration, and temporal continuity, remove NSFW
content, and then sample across scene categories and content types. The final set contains 1,419 source videos
spanning 10 scene categories, summarized in Figure 3(c).


**Editing instructions.** We design instructions to cover 9 major editing
categories and 32 subcategories, illustrated in Figure 2. To improve
task-video compatibility, we use Gemini 3 Flash [36] to analyze video
content, assign suitable editing categories, and generate matched
prompts. Low-confidence assignments are discarded. This process
yields broad task coverage while keeping the editing instructions
grounded in the source content.



**Edited video generation.** For each (source video, instruction) pair, we
collect edited videos from a diverse mixture of commercial systems,
open-source models, and agentic editing pipelines. This diversity
is important because it exposes the benchmark to a broad range
of quality levels and failure modes rather than the behavior of a
single model family. Detailed model lists and pipeline descriptions
are provided in Section C.


**3.2** **Annotation Protocol**



**Figure 2** Task hierarchy of the 9 main
editing categories and 32 subcategories
in `VEFX-Dataset` .



Each editing example is evaluated on a 4-point scale along three decoupled dimensions.


**Instruction Following (IF).** IF measures whether the edit satisfies the semantic requirements of the instruction.
A score of 4 indicates that all requested edits are completed correctly, while a score of 1 indicates failure,
contradiction, or an edit that is largely unrelated to the instruction.


**Rendering Quality (RQ).** RQ evaluates visual quality, including clarity, naturalness, temporal stability, and the
absence of artifacts such as flickering, ghosting, blur, or distortion. This dimension is scored independently of
whether the instruction is followed.


4


**Table 2** Summary of the 4-point scoring rubric for each annotation dimension.


Score 4 Score 3 Score 2 Score 1

IF All requested edits com- Core edit completed with minor Partial execution with major se- Failure, contradiction,
pleted correctly deviation mantic deviation or unrelated edit

RQ Clear, stable, and artifact- Minor but noticeable degrada- Clear quality failure with recur- Severe visual breakfree tion rent artifacts down

EE No clear non-target One clear non-target change Two–three non-target changes or Global or widespread
change one large unintended change over-editing


**EditExclusivity(EE).** EE assesses whether the model changes only the intended target region without introducing
unnecessary modifications elsewhere. In our annotation guide, score 4 means that no clear non-target change
is introduced, score 3 corresponds to one localized non-target change, score 2 corresponds to two to three
clear non-target changes or one large unintended background change, and score 1 indicates widespread or
global over-editing.


A summary of the rubric is provided in Table 2, with the complete annotation guide in Section D. The key
principle of the protocol is that IF, RQ, and EE are scored independently. For example, if the instruction is
“turn the apple into a banana” but the model returns the unchanged video with excellent visual quality, the
correct labels are IF = 1, RQ = 4, and EE = 4. This decoupling prevents semantic success, visual fidelity,
and locality preservation from contaminating one another. All annotators complete a calibration phase with
detailed guidelines and reference examples before annotation begins.


**3.3** **Annotation Reliability**


To assess annotation reliability, we conduct a targeted cross-check study. We randomly sample 550 examples
from the dataset and re-annotate them with a double-annotation strategy using a new group of annotators
independent of the original raters. Since the labels lie on a four-point ordinal scale, we report two direct
agreement measures: exact agreement and within-1-point agreement.


Table 3 shows strong agreement under this cross- **Table 3** Inter-annotator agreement on the 550-sample crosscheck protocol. Within-1 agreement exceeds 91% check subset. Higher values indicate stronger agreement.
on all three dimensions, reaching 93.5% for IF, Metric IF RQ EE
97.2% for RQ, and 91.7% for EE, while exact agree
Exact Agreement (%) 75.2 87.2 72.2

ment remains high at 75.2%, 87.2%, and 72.2%,

Within-1 Agreement (%) 93.5 97.2 91.7

respectively. This pattern is intuitive: rendering
quality is the easiest dimension to align on, while instruction following and edit exclusivity involve more
borderline cases around partial success and acceptable non-target change. Although limited in scale, this
study provides a useful sanity check that the three-dimensional labels are stable enough for training and
evaluation. Additional details are provided in Section E.



**Table 3** Inter-annotator agreement on the 550-sample crosscheck subset. Higher values indicate stronger agreement.



Metric IF RQ EE

Exact Agreement (%) 75.2 87.2 72.2

Within-1 Agreement (%) 93.5 97.2 91.7



**3.4** **Dataset Statistics and Analysis**


We present several analyses of `VEFX-Dataset` to characterize the dataset and motivate its three-dimensional
design. Extended analysis is provided in Section F.


**Score distributions and score patterns.** Figure 3 shows that the three quality dimensions follow clearly different
distributions, which justifies decoupled evaluation. IF is the most polarized: 41.2% of samples receive score 1,
while 28.1% receive score 4, indicating that many edits either fail outright or satisfy the instruction well. RQ
is much more right-skewed, with 78.6% of samples receiving scores 3 or 4 and only 6.8% receiving score 1,
suggesting that visual plausibility is often easier to achieve than semantic correctness. EE is more balanced
across score levels. The common score-pattern panel reinforces this point: while (4 _,_ 4 _,_ 4) is the most frequent
triplet, several of the next most common patterns are cases such as (1 _,_ 4 _,_ 4) and (1 _,_ 4 _,_ 3), where the output
looks plausible but does not follow the instruction.


**Task difficulty across editing types.** The task-type heatmap reveals substantial variation in difficulty across
editing categories. Camera Angle Editing is the hardest category overall, with IF = 1.76 and an overall mean
of 2.46, while Quantity Editing is also challenging on IF at 2.09. By contrast, Style Editing reaches the
highest IF at 2.87, and Visual Effect Editing attains the highest overall mean at 2.93. RQ remains relatively


5


**Figure 3** Overview of dataset statistics for `VEFX-Dataset` . Panel (a) shows common IF–RQ–EE score patterns; (b)
reports pairwise dimension correlations; (c) summarizes video-category coverage; (d) shows the video-resolution
distribution; (e) reports mean scores by task type; and (f) shows score distributions across annotation dimensions.
Together they show that `VEFX-Dataset` spans diverse content and resolutions, exhibits heterogeneous task difficulty,
and captures clear variation in difficulty across editing tasks.


stable across task types, between 3.00 and 3.39, again suggesting that current systems are better at producing
visually plausible outputs than at satisfying complex instructions. EE varies more strongly, with Instance
Motion Editing reaching 3.06 while Creative Editing and Style Editing are lower at 2.22 and 2.23.


**Coverage and dimension independence.** Panels (c) and (d) show that `VEFX-Dataset` spans diverse scene types
and video formats rather than collapsing to a single narrow distribution. Large groups such as Nature,
People, and Street are well represented, while finer-grained content remains present in the long tail. The
resolution distribution is also broad: 1920 _×_ 1080 is the largest bucket at 36.8%, 3840 _×_ 2160 contributes 21.4%,
and portrait videos such as 1080 _×_ 1920 remain substantial at 14.6%. This coverage matters because editing
difficulty depends on both semantic content and visual format. To verify that IF, RQ, and EE capture distinct
aspects of editing quality, we further compute pairwise correlations over the full dataset. All correlations
remain weak: IF–RQ is 0.241, IF–EE is 0.195, and RQ–EE is 0.327. These low correlations support the
three-axis annotation design and indicate that a single scalar score would obscure important failure modes.

### 4 VEFX-Reward : Human-Aligned Video Editing Reward Model


We present the design and training of `VEFX-Reward`, a reward model that predicts human-aligned quality
scores for video editing results. Unlike existing reward models that target either image editing or video
generation, `VEFX-Reward` is specifically designed for the video editing setting, where quality assessment must
jointly consider the original video, the editing instruction, and the edited output.


**4.1** **Problem Formulation**


Given an original video _Vo_ = _{vo_ _[t]_ _[}][T]_ _t_ =1 [,] [an] [editing] [instruction] _[P]_ [,] [and] [the] [corresponding] [edited] [video] _[V][e]_ [=]
_{ve_ _[t][}][T]_ _t_ =1 [,] [our] [goal] [is] [to] [predict] [quality] [scores] [that] [align] [with] [human] [judgment] [along] [the] [three] [annotation]
dimensions defined in Section 3.2:

[ _s_ IF _, s_ RQ _, s_ EE] = _F_ ( _Vo, P, Ve_ ) _,_ (1)


6


where each score lies on the ordinal scale _{_ 1 _,_ 2 _,_ 3 _,_ 4 _}_ .


The three dimensions require different reasoning. Instruction Following evaluates the semantic execution of
the requested edit. Rendering Quality measures visual fidelity and temporal consistency. Edit Exclusivity
compares the original and edited videos to detect unintended modifications outside the target region. A single
holistic score would obscure these distinct failure modes, which motivates the multi-dimensional formulation
of `VEFX-Reward` .


**4.2** **Architecture**


`VEFX-Reward` is instantiated on the Qwen3-VL-Instruct family [37] at two scales, 4B and 32B, which correspond
to `VEFX-Reward-4B` and `VEFX-Reward-32B` in the experiments. In both variants, the model jointly processes
the original video, the edited video, and the editing instruction. This design allows the backbone to compare
the edited result against both the requested change and the source content, which is essential for assessing
semantic faithfulness, rendering quality, and unintended edits within one shared representation.


We introduce three learnable special tokens, `<|IF_reward|>`, `<|RQ_reward|>`, and `<|EE_reward|>`, to query
the three target dimensions. Their final hidden states are passed to a shared reward head, which produces
the ordinal logits used for prediction. This token-based design gives each dimension its own query while
preserving a single backbone for joint multimodal reasoning.


**4.3** **Ordinal Regression Objective**


The bimodal distribution of IF scores (Section 3.4) and the ordinal nature of the 4-point scale motivate the
use of ordinal regression rather than standard L2 loss. We adopt ordinal regression [38], which models the
score as a sequence of ordered threshold decisions instead of an unconstrained scalar regression target.


For each dimension, the reward head predicts three ordered probabilities corresponding to whether the score
is greater than 1, 2, and 3. Training applies binary cross-entropy to these ordered threshold predictions under
the formulation:



_K−_ 1





- BCE� _σ_ ( _zd_ _[k]_ [)] _[,]_ **[1]** [[] _[y][d]_ _[> k]_ []] ��� _yd_ _≥_ _k_ - _,_ (2)

_k_ =1



_L_ = 

_d_



1
_K −_ 1



where the conditional constraint _yd_ _≥_ _k_ ensures that each threshold is trained only on relevant samples,
preserving the ordinal structure.


At inference, we convert these ordered probabilities into a continuous score on [1 _,_ 4] by taking their expected
value:



_s_ ˆ _d_ = 1 +



_K−_ 1




_P_ ( _Y_ _> k_ ) _._ (3)

_k_ =1



This soft prediction is used in all reported experiments.


**4.4** **Training Details**


**Data and video processing.** We train `VEFX-Reward` on the 4,200-example training split of `VEFX-Dataset` and
evaluate on the 849-example test split, with the split stratified across editing categories and pipelines. For
each example, we uniformly sample both the original and edited videos at 4 FPS and cap the frame resolution
at 399,360 pixels, approximately 632 _×_ 632, while preserving native aspect ratios through Qwen3-VL’s
dynamic-resolution mechanism. The two videos are sampled with aligned temporal indices to support direct
comparison, and the maximum sequence length is set to 32,768 tokens.


**Optimization.** We use a two-stage training schedule. In the first stage, lasting 1 epoch, we freeze all pretrained
parameters and train only the newly introduced reward tokens and reward head. In the second stage, lasting
49 epochs, we unfreeze and fine-tune the language backbone and visual-language merger together with the
reward head and reward tokens, while keeping the vision tower frozen. We optimize with AdamW using
learning rates of 1 _×_ 10 _[−]_ [5] for the language-side parameters and 5 _×_ 10 _[−]_ [5] for the reward tokens, cosine decay,
and a 15% warmup ratio. Training is performed in bf16 on 8 GPUs with an effective batch size of 8, and all
three reward dimensions are optimized jointly with equal loss weights.


7


#### **5 Experiments**

We conduct comprehensive experiments to evaluate `VEFX-Reward` as a video editing quality assessor. We
compare against generic VLM-as-judge baselines and prior reward models, analyze global agreement with
standard IQA/VQA metrics, and further test whether the learned scores preserve local human preferences
within directly comparable candidate sets.


**5.1** **Experimental Setup**


**Evaluation metrics.** Our primary evaluation follows standard IQA/VQA protocol. We report Spearman RankOrder Correlation Coefficient (SRCC), Kendall Rank-Order Correlation Coefficient (KRCC), Pearson Linear
Correlation Coefficient (PLCC), and Root Mean Squared Error (RMSE) in Section 5.2. SRCC and KRCC
are computed on raw predictions, while PLCC and RMSE are computed after the standard four-parameter
logistic calibration. We complement these global correlation metrics with a group-wise preference metric,
Pairwise Accuracy, in Section 5.3. Detailed metric definitions and the calibration protocol are provided in
Section H.1.


**Baselines.** We compare `VEFX-Reward` against three types of baselines:


- _VLM-as-a-Judge_ : Qwen3.5-397B, Qwen3.5-122B [37], Gemini-3.1-Pro, Gemini-3.1-Flash-Lite, Gemini-2.5Flash [36, 39], and Seed-2.0-Lite, Seed-1.6 [40]. Each model receives the source video, editing instruction,
and edited video, and is prompted to score editing quality on the same 1–4 rubric used in human annotation.


- _EditReward_ : an image editing reward model with two output heads, one aligned with instruction following
and one aligned with generic visual quality [17].


- _VE-Bench_ : a video editing reward model that predicts a single scalar quality score [16].


**Implementation details.** We instantiate `VEFX-Reward` at two scales, `VEFX-Reward-4B` and `VEFX-Reward-32B`,
using Qwen3-VL backbones at 4B and 32B with the same architecture and training objective. Both models
are trained on the 4,200-example training split and evaluated on the 849-example test split. We sample both
the original and edited videos at 4 FPS with a maximum frame resolution of 399,360 pixels while preserving
aspect ratio, and train in bf16 with an effective batch size of 8. For VLM-as-judge baselines, we use a shared
rubric-aligned prompt over the same source-video/instruction/edited-video triplet. In our evaluation, the
human overall score is defined as the arithmetic mean of IF, RQ, and EE. For `VEFX-Reward` and VLM-as-judge
baselines, the overall prediction is the mean of the three predicted dimension scores; for EditReward, it
is the mean of its two native heads; and for VE-Bench, it is the model’s native scalar output. Additional
implementation details are provided in Section B.


**5.2** **Results on Standard IQA/VQA Metrics**


Following standard IQA/VQA practice, we evaluate all methods with SRCC, KRCC, PLCC, and RMSE. The
Overall columns in Table 4 report agreement on the human overall score rather than a separate learned target.


**Overall results.** Both `VEFX-Reward` variants clearly outperform prior reward-model baselines on the human
overall score. `VEFX-Reward-32B` is strongest overall, achieving 0.780 SRCC, 0.616 KRCC, 0.790 PLCC, and
0.475 RMSE, while `VEFX-Reward-4B` follows closely at 0.760, 0.595, 0.771, and 0.493. The margin over prior
reward models is substantial: EditReward reaches 0.558 overall SRCC and 0.631 RMSE, whereas VE-Bench
drops further to 0.214 SRCC and 0.752 RMSE.


**Dimension-wise behavior.** The two `VEFX-Reward` scales show complementary strengths. `VEFX-Reward-32B` is
best on IF and EE, with the strongest rank correlation and calibration on both dimensions. `VEFX-Reward-4B`
is slightly stronger on RQ across all four standard metrics, which suggests that larger scale mainly helps
instruction faithfulness and edit exclusivity, while rendering-quality prediction is already close to saturation
at 4B scale. This is consistent with the dataset statistics in Section 3.4: RQ is both less ambiguous and more
concentrated than IF.


**Baseline comparison.** Strong VLM judges remain competitive on a few individual columns, but they do not


8


**Table 4** Results on standard IQA/VQA metrics. SRCC, KRCC, and PLCC are higher-is-better; RMSE is lower-is-better.
PLCC and RMSE are computed after logistic calibration. Overall denotes correlation on the human overall score,
defined as the mean of IF, RQ, and EE. For `VEFX-Reward` and VLM-as-judge baselines, the overall prediction is the
mean of the three predicted dimension scores; EditReward uses the mean of its two native heads, and VE-Bench uses
its native scalar overall score.


SRCC _↑_ KRCC _↑_ PLCC _↑_ RMSE _↓_
Method


IF RQ EE Overall IF RQ EE Overall IF RQ EE Overall IF RQ EE Overall


_VLM-as-a-Judge_


Seed-1.6 0.686 0.618 0.504 0.630 0.605 0.573 0.447 0.508 0.684 0.608 0.591 0.701 0.918 0.798 0.917 0.565


Seed-2.0-Lite 0.545 0.544 0.697 0.720 0.483 0.497 0.527 0.607 0.616 0.594 0.729 0.768 0.984 0.815 0.791 0.510


Qwen3.5-122B 0.379 0.563 0.658 0.631 0.327 0.523 0.573 0.520 0.378 0.663 0.601 0.685 1.165 0.752 0.893 0.578


Qwen3.5-397B 0.572 0.422 0.654 0.601 0.506 0.384 0.587 0.497 0.615 0.624 0.692 0.657 0.992 0.785 0.820 0.598

Gemini-3.1-Pro 0.731 0.518 0.681 0.752 0.559 0.459 0.584 0.608 **0.754** 0.510 0.644 0.726 0.826 0.864 0.788 0.546


Gemini-3.1-Flash-Lite 0.309 0.302 0.661 0.574 0.283 0.277 0.555 0.436 0.316 0.425 0.673 0.505 1.194 0.910 0.840 0.685


Gemini-2.5-Flash 0.256 0.217 0.581 0.383 0.236 0.195 0.544 0.296 0.256 0.491 0.569 0.478 1.216 0.875 0.934 0.697


_Previous_ _Reward_ _Models_


EditReward [17] 0.453 -0.211 - 0.558 0.342 -0.164 - 0.411 0.455 0.317 - 0.580 1.113 0.844 - 0.631


VE-Bench [16] - - - 0.214 - - - 0.150 - - - 0.238 - - - 0.752


_Ours_


**Figure 4** Predicted overall scores versus human overall scores for `VEFX-Reward-32B`, EditReward, and VE-Bench. Here
the human overall score is defined as the mean of IF, RQ, and EE. `VEFX-Reward-32B` exhibits a tight monotonic trend
that closely follows the human score axis, whereas EditReward shows a weaker and more nonlinear relationship, and
VE-Bench displays substantially larger dispersion with limited sensitivity to score differences. Additional scatter plots
are provided in Section H.1.


match the consistency of `VEFX-Reward` across dimensions and metrics. More importantly, the gap to previous
reward models is large and systematic. EditReward remains somewhat useful on IF, but its negative RQ
correlations indicate a clear mismatch between image-editing supervision and video-editing assessment; it
also has no dedicated EE head. VE-Bench predicts only a single scalar score and therefore cannot support
per-dimension analysis, while even its overall agreement remains weak. These results support the need for a
reward model that jointly reasons over the source video, the editing instruction, and the edited output.


**Scatter-plot analysis.** Figure 4 provides a qualitative comparison of the three reward models on the human
overall score. `VEFX-Reward-32B` shows a clear monotonic increase and a relatively tight concentration around
the fitted trend, indicating that its predictions preserve both ordering and score magnitude more faithfully.
EditReward still captures a coarse positive trend, but the response is more nonlinear and compressed. VEBench exhibits the weakest alignment, with much larger dispersion at nearly every human score level. This
visual evidence is fully consistent with the quantitative results in Table 4.


**5.3** **Group-wise Preference Evaluation**


Standard IQA/VQA metrics measure global correlation with human scores, but reward models are often used
in a more local setting: given several candidate edits for the same source video and instruction, the model


9


should prefer the better one. We therefore add a group-wise preference evaluation that measures whether a
reward model preserves human ordering within directly comparable candidate sets.


**Pairwise Accuracy.** Each ranking group _g_ contains all candidate edits that share the same raw video and
editing instruction; candidate edits may come from different editing systems, but comparisons are performed
only within the group and never across groups. We enumerate all candidate pairs in each group and compare
the predicted ordering with the ground-truth ordering. If the ground truth is tied, the pair is counted as
correct regardless of the prediction; if the prediction is tied but the ground truth is not, it receives a score of
0 _._ 5. The dataset-level Pairwise Accuracy is



PairAcc =




- _G_ _g_ =1 ( _i,j_ ) _∈Pg_ [Acc] _[ij]_

_,_ (4)

 - _G_
_g_ =1 _[|P][g][|]_



where Acc _ij_ = 1 if the predicted order matches the human order. Unlike the global IQA/VQA metrics above,
Pairwise Accuracy depends only on relative ordering within each candidate group and is therefore insensitive
to score-scale mismatch across models.


**Table 5** Group-wise preference evaluation using Pairwise Accuracy. Overall denotes performance on the human overall
score, defined as the mean of IF, RQ, and EE.


Model IF RQ EE Overall

EditReward [17] 0.8283 0.5629 0.5317 0.7919
VE-Bench [16] 0.7351 0.8127 0.7143 0.6651


**Preference results.** Both `VEFX-Reward` variants substantially outperform previous reward models on groupwise preference consistency. `VEFX-Reward-32B` achieves the best overall Pairwise Accuracy at 0.872, while
`VEFX-Reward-4B` remains close at 0.863, indicating that most relative preference signal is already captured
at 4B scale. EditReward remains somewhat competitive on IF because one of its heads is naturally aligned
with instruction following, but it performs poorly on RQ and EE because it is an image editing reward
model without video-native temporal reasoning or a dedicated EE concept. VE-Bench shows moderate
ordering ability, but its single-score design limits fine-grained candidate comparison. Together, these results
confirm that `VEFX-Reward` is not only better aligned with human scores globally, but also more reliable for
within-group candidate selection.


**5.4** **Validation of Key Design Choices**


We keep the ablation study intentionally lightweight, since the main contribution of this work is the benchmark
and the reward-model formulation rather than a complex architectural recipe. The goal of this section is to
verify that the final configuration is supported by controlled development experiments.


**Table 6** Summary of key design-choice validations for `VEFX-Reward` .


Study Compared settings Selected choice Observation

Loss function REG / CLS / ORD ORD Best alignment with human labels
Temporal sampling 1 / 2 / 4 / 8 FPS 4 FPS Best balance of motion and redundancy
Spatial resolution 154K / 400K / 450K / 920K px _∼_ 400K px Best trade-off between detail and efficiency


**Analysis.** Ordinal regression is consistently the strongest choice in development, which is well aligned with
the ordered 1–4 label space. For video preprocessing, 4 FPS provides the best trade-off between temporal
coverage and redundant frames. Spatially, around 400K pixels per frame is the most effective operating point:
lower resolution removes subtle local editing cues, while higher resolution increases computation without
yielding clear gains. These trends support the default configuration used in the final `VEFX-Reward` models.

#### **6 Benchmarking Existing Video Editing Models**


Beyond baseline comparison, `VEFX-Bench` also enables a systematic evaluation of existing video editing models
with our learned evaluator. We score 10 representative models using `VEFX-Reward-32B` on the same 1–4 scale


10


as `VEFX-Dataset`, including the commercial systems Kling o3 omni [41], Kling o1 [42], Runway Gen-4.5 [43],
Seedance 2.0 [44], Grok Imagine [45], Luma ray 3 [46], Wan 2.6 [47], and Luma ray 2 [48], as well as the
open-source systems UniVideo [11] and VACE [10]. In this section, all reported metrics are computed from
soft expected predictions for IF, RQ, and EE. We report _Overall_ _(Mean)_ as the arithmetic mean of the three
dimensions, and use _Overall_ _(GeoAgg)_ as the primary ranking metric.


Following prior work on multiplicative multi-attribute aggregation, we define _Overall_ _(GeoAgg)_ as a weighted
geometric aggregate to reduce full compensability across dimensions and to penalize weak instruction following
more strongly [49, 50]. For each evaluated sample _i_ from model _m_, we first normalize the predicted scores to

[0 _,_ 1]:



_im,i_ = _[IF][m,i][ −]_ [1]




_[ −]_ [1]

_,_ _em,i_ = _[EE][m,i][ −]_ [1]
3 3




_[ −]_ [1]

_,_ _rm,i_ = _[RQ][m,i][ −]_ [1]
3 3



_._ (5)
3



We then compute the sample-level aggregate and average it over the evaluated set Ω _m_ :



1
Overall (GeoAgg) _m_ = _|_ Ω _m|_






_i∈_ Ω _m_



�1 + 3 - _i_ _[α]_ _m,i_ _[r]_ _m,i_ _[β]_ _[e][γ]_ _m,i_ - _α_ + _β_ 1 + _γ_ [�] _._ (6)



In all experiments in this section, we set ( _α, β, γ_ ) = (2 _,_ 1 _,_ 1), so IF receives twice the weight of RQ and EE. We
compute GeoAgg before averaging because the geometric aggregate is nonlinear; applying it after averaging IF,
RQ, and EE would overestimate systems with high variance or unbalanced per-sample behavior. Compared
with an arithmetic mean, this multiplicative form is more sensitive to weak dimensions, which is desirable in
video editing evaluation because strong rendering quality or locality preservation should not fully offset poor
instruction following.


**Adjusting incomplete model coverage.** Some commercial systems impose inference constraints, resulting in
incomplete benchmark coverage for models such as Runway Gen-4.5 and Seedance 2.0. Rather than reporting
a naive mean over each observed subset, which can be biased when coverage correlates with item difficulty,
we treat incomplete coverage as a missing-data problem [51]. Our adjustment follows the standard inversepropensity weighting principle [52–54]. Let _Rm,i_ = 1 indicate that model _m_ has a valid evaluated output for
benchmark item _i_, and let **x** _i_ denote item-level covariates such as task type, prompt length, and constraint
count. We estimate the observation propensity _p_ ˆ _m,i_ = Pr( _Rm,i_ = 1 _| m,_ **x** _i_ ) and weight each observed score
by a clipped inverse-propensity weight _wm,i_ = 1 _/p_ ˆ _m,i_ . For each dimension _d_, we then fit a weighted linear
mixed-effects model
_ym,i,d_ = _µm,d_ + _ui_ + _ϵm,i,d,_ _ui_ _∼N_ (0 _, σu_ [2][)] _[,]_ (7)


where _ui_ captures item difficulty. The reported IF, RQ, and EE scores are coverage-adjusted model-level
estimates _µ_ ˆ _m,d_ under the assumption that coverage is explainable by observed item covariates. _Overall_ _(Mean)_
is computed from these adjusted dimension scores, while _Overall_ _(GeoAgg)_ is computed from soft per-sample
IF/RQ/EE predictions and then averaged as in Equation (6).


**Table 7** `VEFX-Reward-32B` -based evaluation of representative video editing systems using soft expected predictions.
IF, RQ, EE, and Overall (Mean) use coverage-adjusted estimates from inverse-propensity-weighted mixed-effects
estimation; Overall (GeoAgg) is averaged over sample-level GeoAgg scores. Higher is better on all columns. _[∗]_ denotes
adjusted results for models with incomplete benchmark coverage.


Model Overall (GeoAgg) Overall (Mean) IF RQ EE

_Commercial_
Kling o3 omni **3.057** **3.221** 3.033 **3.588** 3.043
Kling o1 2.985 3.183 **3.040** 3.534 2.976
Runway Gen-4.5 _[∗]_ 2.912 3.020 2.817 3.319 2.923
Seedance 2.0 _[∗]_ 2.766 3.107 2.811 3.421 3.088
Grok Imagine 2.723 3.109 2.606 3.346 **3.376**
Luma ray 3 2.717 2.936 2.702 3.403 2.705
Wan 2.6 2.146 2.592 2.012 3.317 2.446
Luma ray 2 1.804 1.977 2.038 2.532 1.363

_Open-source_

UniVideo [11] 2.516 2.883 2.294 3.266 3.091
VACE [10] 1.775 2.126 2.027 3.172 1.180


11


**Table analysis.** As shown in Table 7, Kling o3 omni ranks first under _Overall_ _(GeoAgg)_, followed by Kling
o1. Both models combine strong IF and RQ with competitive EE, so their rankings remain high under the
per-sample multiplicative aggregate. Runway Gen-4.5 ranks third by GeoAgg, reflecting balanced per-sample
behavior despite a lower adjusted mean. Seedance 2.0 improves after the corrected result merge and ranks
fourth by GeoAgg, with strong RQ and EE but still weaker IF than the top systems. Grok Imagine achieves
the strongest EE score and a high arithmetic mean, but its lower IF reduces its _Overall_ _(GeoAgg)_ .


Among the open-source systems, UniVideo is clearly stronger than VACE and remains competitive with
several commercial systems, especially on EE. Luma ray 3 and Wan 2.6 achieve strong RQ but are limited by
weaker IF or EE, while Luma ray 2 and VACE show the largest drops because of poor edit exclusivity. Overall,
the results suggest that modern systems often produce visually plausible videos, but reliable instruction
following and locality preservation still separate the strongest editing models from the rest.


Observed score distributions grouped and ordered by per-sample GeoAgg



4


3


2


1


4


3


2


1



4


3


2


1


4


3


2


1







4


3


2


1





Models

Kling o3 omni

Kling o1

Runway Gen-4.5

Grok

Luma ray 3



Seedance

Wan 2.6

Luma ray 2

UniVideo

VACE



**Figure 5** Observed soft-score `VEFX-Reward-32B` distributions for the benchmarked video editing systems across _Overall_
_(GeoAgg)_, _Overall_ _(Mean)_, IF, RQ, and EE. Models are grouped by availability and ordered by per-sample _Overall_
_(GeoAgg)_ .


**Figure analysis.** Figure 5 complements the adjusted table with the distribution of observed per-item scores.
The top commercial systems have high medians but still show substantial prompt-level variance, indicating
that no model is uniformly reliable across editing tasks. RQ is generally higher and more concentrated than
IF, suggesting that visual plausibility is easier to achieve than instruction-faithful editing. EE provides the
clearest separation: Grok Imagine, UniVideo, Kling o3 omni, and Seedance 2.0 maintain relatively strong
locality, whereas VACE and Luma ray 2 concentrate near the bottom of the scale. The gap between _Overall_
_(Mean)_ and _Overall_ _(GeoAgg)_ is most visible for models with unbalanced dimensions, illustrating why a
shortfall-sensitive aggregate is useful for benchmark ranking.


**Task-wise analysis.** Figure 6 shows that the strongest systems are not uniformly strong across all editing types.
Kling o3 omni and Kling o1 maintain broad coverage with clear advantages on quantity, attribute, instance,
and visual-effect editing, while Runway Gen-4.5 and Seedance 2.0 are more balanced but slightly lower overall.
Grok Imagine has a distinctive profile: it is strong on style, instance, and visual-effect editing, but weaker on
camera-control tasks. The lower-scoring models show smaller and more compressed profiles, suggesting that
their failures are not limited to a single task type.


12


Overall (GeoAgg) Profiles by Editing Task



Kling o3 omni



Kling o1



Seedance 2.0



Runway Gen-4.5



Luma ray 3



Camera

Angle















Camera

Angle





Camera

Angle





Camera

Angle





Camera

Angle































































Creative Style


UniVideo



Creative Style


Grok Imagine



Creative Style


Wan 2.6



Creative Style


VACE



Creative Style


Luma ray 2



Camera

Angle















Camera

Angle





Camera

Angle





Camera

Angle





Camera

Angle































































Creative Style



Creative Style



Creative Style



Creative Style



Creative Style



**Figure 6** Task-wise _Overall_ _(GeoAgg)_ profiles of the benchmarked video editing systems. Each radar plot uses the same
radial scale, allowing the profile shape and absolute score level of each model to be compared across editing tasks.

#### **7 Conclusion**


We introduced `VEFX-Dataset`, a human-annotated dataset of 5,049 video editing examples with decoupled
labels for Instruction Following, Rendering Quality, and Edit Exclusivity, together with `VEFX-Reward` for
automated evaluation and `VEFX-Bench` for standardized model comparison. Across both standard IQA/VQA
metrics and group-wise preference evaluation, `VEFX-Reward` consistently outperforms generic VLM judges
and prior reward-model baselines, showing the value of task-specific reward modeling for video editing. Using
`VEFX-Reward` as a scalable evaluator, we further benchmark representative commercial and open-source editing
systems and analyze their behavior across editing tasks. This analysis shows that current systems often
achieve plausible rendering quality without reliably satisfying instructions or preserving non-target content,
reinforcing the need for multi-dimensional evaluation rather than a single holistic score. We hope these
resources provide a practical foundation for benchmarking, model selection, and reward-driven optimization
in video editing.


13


#### **References**


[1] T. Wan, A. Wang, B. Ai, B. Wen, C. Mao, C.-W. Xie, D. Chen, F. Yu, H. Zhao, J. Yang _et_ _al._, “Wan: Open and
advanced large-scale video generative models,” _arXiv_ _preprint_ _arXiv:2503.20314_, 2025.


[2] S. Chen, C. Ge, Y. Zhang, Y. Zhang, F. Zhu, H. Yang, H. Hao, H. Wu, Z. Lai, Y. Hu _et_ _al._, “Goku: Flow based
video generative foundation models,” in _Proceedings_ _of_ _the_ _Computer_ _Vision_ _and_ _Pattern_ _Recognition_ _Conference_,
2025, pp. 23 516–23 527.


[3] W. Kong, Q. Tian, Z. Zhang, R. Min, Z. Dai, J. Zhou, J. Xiong, X. Li, B. Wu, J. Zhang _et_ _al._, “Hunyuanvideo: A
systematic framework for large video generative models,” _arXiv_ _preprint_ _arXiv:2412.03603_, 2024.


[4] A. Polyak, A. Zohar, A. Brown, A. Tjandra, A. Sinha, A. Lee, A. Vyas, B. Shi, C.-Y. Ma, C.-Y. Chuang _et_ _al._,
“Movie gen: A cast of media foundation models,” _arXiv_ _preprint_ _arXiv:2410.13720_, 2024.


[5] OpenAI, “Sora: Creating video from text,” 2024.


[6] DeepMind, “Veo 3 technical report,” DeepMind, Technical Report, 2025, accessed: 2026-02-18. [Online]. Available:

[https://storage.googleapis.com/deepmind-media/veo/Veo-3-Tech-Report.pdf](https://storage.googleapis.com/deepmind-media/veo/Veo-3-Tech-Report.pdf)


[7] Kling AI, “Kling AI Omni / VIDEO O1 creative interface,” 2025.


[8] xAI, “Grok Imagine - ai image & video generation by xai,” 2026.


[9] M. Wu, A. Mishra, S. Dey, S. Xing, N. Ravipati, H. Wu, B. Li, and Z. Tu, “Consid-gen: View-consistent and
identity-preserving image-to-video generation,” _arXiv_ _preprint_ _arXiv:2602.10113_, 2026.


[10] Z. Jiang, Z. Han, C. Mao, J. Zhang, Y. Pan, and Y. Liu, “Vace: All-in-one video creation and editing,” _arXiv_
_preprint_ _arXiv:2503.07598_, 2025.


[11] C. Wei, Q. Liu, Z. Ye, Q. Wang, X. Wang, P. Wan, K. Gai, and W. Chen, “Univideo: Unified understanding,
generation, and editing for videos,” _arXiv_ _preprint_ _arXiv:2510.08377_, 2025.


[12] Y. Chen, P. Chen, X. Zhang, Y. Huang, and Q. Xie, “Editboard: Towards a comprehensive evaluation benchmark
for text-based video editing models,” in _Proceedings_ _of_ _the_ _AAAI_ _Conference_ _on_ _Artificial_ _Intelligence_, vol. 39,
no. 15, 2025, pp. 15 975–15 983.


[13] M. Li, C. Xie, Y. Wu, L. Zhang, and M. Wang, “Five: A fine-grained video editing benchmark for evaluating
emerging diffusion and rectified flow models,” _arXiv_ _preprint_ _arXiv:2503.13684_, 2025.


[14] Y. Chen, J. Zhang, T. Hu, Y. Zeng, Z. Xue, Q. He, C. Wang, Y. Liu, X. Hu, and S. Yan, “Ivebench: Modern
benchmark suite for instruction-guided video editing assessment,” _arXiv_ _preprint_ _arXiv:2510.11647_, 2025.


[15] H. He, J. Wang, J. Zhang, Z. Xue, X. Bu, Q. Yang, S. Wen, and L. Xie, “Openve-3m: A large-scale high-quality
dataset for instruction-guided video editing,” _arXiv_ _preprint_ _arXiv:2512.07826_, 2025.


[16] S. Sun, X. Liang, S. Fan, W. Gao, and W. Gao, “Ve-bench: Subjective-aligned benchmark suite for text-driven
video editing quality assessment,” _arXiv_ _preprint_ _arXiv:2408.11481_, 2024.


[17] K. Wu, S. Jiang, M. Ku, P. Nie, M. Liu, and W. Chen, “Editreward: A human-aligned reward model for
instruction-guided image editing,” _arXiv_ _preprint_ _arXiv:2509.26346_, 2025.


[18] J. Liu, G. Liu, J. Liang, Z. Yuan, X. Liu, M. Zheng, X. Wu, Q. Wang, M. Xia, X. Wang _et_ _al._, “Improving video
generation with human feedback,” _arXiv_ _preprint_ _arXiv:2501.13918_, 2025.


[19] Y. Guo, C. Yang, A. Rao, Z. Liang, Y. Wang, Y. Qiao, M. Agrawala, D. Lin, and B. Dai, “Animatediff: Animate
your personalized text-to-image diffusion models without specific tuning,” _arXiv_ _preprint_ _arXiv:2307.04725_, 2023.


[20] L. Yang, Z. Zhang, Y. Song, S. Hong, R. Xu, Y. Zhao, W. Zhang, B. Cui, and M.-H. Yang, “Diffusion models: A
comprehensive survey of methods and applications,” _ACM_ _computing_ _surveys_, vol. 56, no. 4, pp. 1–39, 2023.


[21] G. Cheng, X. Gao, L. Hu, S. Hu, M. Huang, C. Ji, J. Li, D. Meng, J. Qi, P. Qiao _et_ _al._, “Wan-animate: Unified
character animation and replacement with holistic replication,” _arXiv_ _preprint_ _arXiv:2509.14055_, 2025.


[22] Luma AI, “Luma ray2,” _[https:// lumalabs.ai/ ray2](https://lumalabs.ai/ray2)_, 2025.


[23] A. Radford, J. W. Kim, C. Hallacy, A. Ramesh, G. Goh, S. Agarwal, G. Sastry, A. Askell, P. Mishkin, J. Clark
_et_ _al._, “Learning transferable visual models from natural language supervision,” in _ICML_, 2021.


[24] R. Zhang, P. Isola, A. A. Efros, E. Shechtman, and O. Wang, “The unreasonable effectiveness of deep features as
a perceptual metric,” in _Proceedings_ _of_ _the_ _IEEE_ _conference_ _on_ _computer_ _vision_ _and_ _pattern_ _recognition_, 2018, pp.
586–595.


[25] Z. Huang, Y. He, J. Yu, F. Zhang, C. Si, Y. Jiang, Y. Zhang, T. Wu, Q. Jin, N. Chanpaisit _et_ _al._, “Vbench:
Comprehensive benchmark suite for video generative models,” in _Proceedings_ _of_ _the_ _IEEE/CVF_ _Conference_ _on_


14


_Computer_ _Vision_ _and_ _Pattern_ _Recognition_, 2024, pp. 21 807–21 818.


[26] Z. Huang, F. Zhang, X. Xu, Y. He, J. Yu, Z. Dong, Q. Ma, N. Chanpaisit, C. Si, Y. Jiang _et_ _al._, “Vbench++:
Comprehensive and versatile benchmark suite for video generative models,” _IEEE_ _Transactions_ _on_ _Pattern_
_Analysis_ _and_ _Machine_ _Intelligence_, 2025.


[27] J. Xu, X. Liu, Y. Wu, Y. Tong, Q. Li, M. Ding, J. Tang, and Y. Dong, “Imagereward: Learning and evaluating
human preferences for text-to-image generation,” _Advances_ _in_ _Neural_ _Information_ _Processing_ _Systems_, vol. 36, pp.
15 903–15 935, 2023.


[28] X. Wu, Y. Hao, K. Sun, Y. Chen, F. Zhu, R. Zhao, and H. Li, “Human preference score v2: A solid benchmark
for evaluating human preferences of text-to-image synthesis,” _arXiv_ _preprint_ _arXiv:2306.09341_, 2023.


[29] Y. Kirstain, A. Polyak, U. Singer, S. Matiana, J. Penna, and O. Levy, “Pick-a-pic: An open dataset of user
preferences for text-to-image generation,” _Advances_ _in_ _neural_ _information_ _processing_ _systems_, vol. 36, pp. 36 652–
36 663, 2023.


[30] X. He, D. Jiang, G. Zhang, M. Ku, A. Soni, S. Siu, H. Chen, A. Chandra, Z. Jiang, A. Arulraj _et_ _al._, “Videoscore:
Building automatic metrics to simulate fine-grained human feedback for video generation,” in _Proceedings_ _of_ _the_
_2024_ _Conference_ _on_ _Empirical_ _Methods_ _in_ _Natural_ _Language_ _Processing_, 2024, pp. 2105–2123.


[31] Z. Wu, A. Kag, I. Skorokhodov, W. Menapace, A. Mirzaei, I. Gilitschenski, S. Tulyakov, and A. Siarohin, “Densedpo:
Fine-grained temporal preference optimization for video diffusion models,” _arXiv_ _preprint_ _arXiv:2506.03517_, 2025.


[32] H. Duan, H.-X. Yu, S. Chen, L. Fei-Fei, and J. Wu, “Worldscore: A unified evaluation benchmark for world
generation,” in _Proceedings_ _of_ _the_ _IEEE/CVF_ _International_ _Conference_ _on_ _Computer_ _Vision_, 2025, pp. 27 713–
27 724.


[33] X. Gao, M. Wu, S. Yang, J. Yu, P. Taghavi, F. Lin, and Z. Tu, “The pulse of motion: Measuring physical frame
rate from visual dynamics,” _arXiv_ _preprint_ _arXiv:2603.14375_, 2026.


[34] Z. Zheng _et_ _al._, “Open-Sora: Democratizing efficient video production for all,” _arXiv_ _preprint_ _arXiv:2412.20404_,
2024.


[35] K. Nan _et_ _al._, “OpenVid-1M: A large-scale high-quality dataset for text-to-video generation,” _arXiv_ _preprint_
_arXiv:2407.02371_, 2024.


[36] Google DeepMind, “Gemini 3 Flash - deepmind ai model,” 2025.


[37] A. Yang, A. Li, B. Yang, B. Zhang, B. Hui, B. Zheng, B. Yu, C. Gao, C. Huang, C. Lv _et_ _al._, “Qwen3 technical
report,” _arXiv_ _preprint_ _arXiv:2505.09388_, 2025.


[38] U. Shaham, I. Zaidman, and J. Svirsky, “Deep ordinal regression using optimal transport loss and unimodal
output probabilities,” _arXiv_ _preprint_ _arXiv:2011.07607_, 2020.


[39] Google DeepMind, “Gemini 3.1 Pro - deepmind ai model,” 2025.


[40] ByteDance Seed Team, “ByteDance Seed: Models and research,” [https://seed.bytedance.com/,](https://seed.bytedance.com/) 2025, accessed:
2026-02-27.


[41] Kling AI, “Kling video 3.0 model user guide,” [https://kling.ai/quickstart/klingai-video-3-model-user-guide,](https://kling.ai/quickstart/klingai-video-3-model-user-guide) Feb.
2026, accessed: 2026-04-16.


[42] ——, “Kling video o1 user guide,” [https://kling.ai/quickstart/klingai-video-o1-user-guide,](https://kling.ai/quickstart/klingai-video-o1-user-guide) Dec. 2025, accessed:
2026-04-16.


[43] Runway, “Introducing runway gen-4.5: A new frontier for video generation,” [https://runwayml.com/research/](https://runwayml.com/research/introducing-runway-gen-4.5)
[introducing-runway-gen-4.5,](https://runwayml.com/research/introducing-runway-gen-4.5) Dec. 2025, accessed: 2026-04-16.


[44] ByteDance Seed Team, “Seedance 2.0 official launch,” [https://seed.bytedance.com/en/blog/](https://seed.bytedance.com/en/blog/official-launch-of-seedance-2-0)
[official-launch-of-seedance-2-0,](https://seed.bytedance.com/en/blog/official-launch-of-seedance-2-0) Feb. 2026, accessed: 2026-04-16.


[45] xAI, “Grok imagine api,” [https://x.ai/news/grok-imagine-api,](https://x.ai/news/grok-imagine-api) Jan. 2026, accessed: 2026-04-16.


[46] Luma AI, “Luma ai launches ray3,” [https://lumalabs.ai/news/ray3,](https://lumalabs.ai/news/ray3) Sep. 2025, accessed: 2026-04-16.


[47] Alibaba Cloud, “Alibaba unveils wan2.6 series enabling everyone to star in videos,” [https://www.alibabacloud.com/](https://www.alibabacloud.com/blog/alibaba-unveils-wan2-6-series-enabling-everyone-to-star-in-videos_602742)
[blog/alibaba-unveils-wan2-6-series-enabling-everyone-to-star-in-videos_602742,](https://www.alibabacloud.com/blog/alibaba-unveils-wan2-6-series-enabling-everyone-to-star-in-videos_602742) Dec. 2025, accessed: 2026-04-16.


[48] Luma AI, “Introducing ray2,” [https://lumalabs.ai/changelog/introducing-ray2,](https://lumalabs.ai/changelog/introducing-ray2) Jan. 2025, accessed: 2026-04-16.


[49] R. L. Keeney and H. Raiffa, _Decisions_ _with_ _Multiple_ _Objectives:_ _Preferences_ _and_ _Value_ _Tradeoffs_ . Cambridge
University Press, 1993.


[50] R. L. Keeney, “Multiplicative utility functions,” _Operations_ _Research_, vol. 22, no. 1, pp. 22–34, 1974.


15


[51] D. B. Rubin, “Inference and missing data,” _Biometrika_, vol. 63, no. 3, pp. 581–592, 1976.


[52] D. G. Horvitz and D. J. Thompson, “A generalization of sampling without replacement from a finite universe,”
_Journal_ _of_ _the_ _American_ _Statistical_ _Association_, vol. 47, no. 260, pp. 663–685, 1952.


[53] J. M. Robins, A. Rotnitzky, and L. P. Zhao, “Estimation of regression coefficients when some regressors are not
always observed,” _Journal_ _of_ _the_ _American_ _Statistical_ _Association_, vol. 89, no. 427, pp. 846–866, 1994.


[54] S. R. Seaman and I. R. White, “Review of inverse probability weighting for dealing with missing data,” _Statistical_
_Methods_ _in_ _Medical_ _Research_, vol. 22, no. 3, pp. 278–295, 2013.


[55] N. Ravi _et_ _al._, “SAM 2: Segment anything in images and videos,” _arXiv_ _preprint_ _arXiv:2408.00714_, 2024.


[56] C. Miao, Y. Feng, J. Zeng, Z. Gao, H. Liu, Y. Yan, D. Qi, X. Chen, B. Wang, and H. Zhao, “Rose: Remove
objects with side effects in videos,” _arXiv_ _preprint_ _arXiv:2508.18633_, 2025.


[57] X. Gao, R. Li, X. Chen, Y. Wu, S. Feng, Q. Yin, and Z. Tu, “Pisco: Precise video instance insertion with sparse
control,” _arXiv_ _preprint_ _arXiv:2602.08277_, 2026.


[58] Y. Xu, J. Zhang, Q. Zhang, and D. Tao, “ViTPose: Simple vision transformer baselines for human pose estimation,”
in _NeurIPS_, 2022.


[59] H. Lin, S. Chen, J. Liew, D. Y. Chen, Z. Li, G. Shi, J. Feng, and B. Kang, “Depth anything 3: Recovering the
visual space from any views,” _arXiv_ _preprint_ _arXiv:2511.10647_, 2025.


[60] J. He _et_ _al._, “ReCamMaster: Camera-controlled generative rendering from a single video,” _arXiv_ _preprint_
_arXiv:2501.12007_, 2025.


[61] T. Liu, Z. Chen, Z. Huang, S. Xu, S. Zhang, C. Ye, B. Li, Z. Cao, W. Li, H. Zhao _et_ _al._, “Light-x: Generative 4d
video rendering with camera and illumination control,” _arXiv_ _preprint_ _arXiv:2512.05115_, 2025.


16


## **Appendix**

### A Additional Training Details for VEFX-Reward

We provide the implementation details omitted from the main paper. `VEFX-Reward` is trained on the 4,200example training split of `VEFX-Dataset` and evaluated on the 849-example test split, with the split stratified
across editing categories and pipelines.


**Video Processing.** For each example, we uniformly sample both the original and edited videos at 4 FPS and
cap the frame resolution at 399,360 pixels, approximately 632 _×_ 632, while preserving aspect ratio through
Qwen3-VL’s dynamic-resolution mechanism. The two videos are sampled with aligned temporal indices to
support direct comparison. The maximum sequence length is 32,768 tokens.


**Optimization.** We use a two-stage training schedule. In the first stage, lasting 1 epoch, we freeze all pretrained
parameters and train only the newly introduced reward tokens and reward head. In the second stage, lasting
49 epochs, we unfreeze and fine-tune the language backbone and visual-language merger together with the
reward head and reward tokens, while keeping the vision tower frozen. We use AdamW with learning rates
of 1 _×_ 10 _[−]_ [5] for the language-side parameters and 5 _×_ 10 _[−]_ [5] for the reward tokens, cosine decay, and a 15%
warmup ratio. Training is performed in bf16 on 8 GPUs with an effective batch size of 8. The three reward
dimensions are optimized jointly with equal loss weights.

#### **B Additional Experimental Details**


**Model** **Variants.** We evaluate two `VEFX-Reward` variants, `VEFX-Reward-4B` and `VEFX-Reward-32B`, which
instantiate the same reward-model design on Qwen3-VL backbones at 4B and 32B scales.


**Evaluation Setup.** Both variants are evaluated on the same 849-example test split. For VLM-as-judge baselines,
we use a shared prompt that presents the original video, editing instruction, and edited video, and asks the
model to score IF, RQ, and EE according to the same 1–4 rubric used in human annotation. In the main
paper, the human overall score is defined as the arithmetic mean of the three human dimension scores. For
`VEFX-Reward` and VLM-as-judge baselines, the overall prediction is defined as the mean of the three predicted
dimension scores.


**External** **Reward** **Models.** EditReward and VE-Bench are evaluated through their native outputs. For
EditReward, the overall prediction is defined as the mean of its two native heads; for VE-Bench, the overall
prediction is its native scalar output. SRCC and KRCC are computed directly from raw predictions, while
PLCC and RMSE use the same logistic calibration protocol as in the main paper when applicable. Since
EditReward lacks a dedicated EE head and VE-Bench predicts only a single overall score, unavailable entries
are marked with –.

#### **C Editing Pipeline Details**


We describe the detailed procedures for each category of editing systems used in `VEFX-Dataset` .


**C.1** **Commercial Models**


For generic instruction-guided video editing, we directly submit (source video, instruction) pairs to four
commercial APIs: Grok Imagine [8], Kling Omni [7], Wan 2.6 [21], and Luma Ray2 [22]. These systems accept
free-form text instructions and produce edited videos end-to-end.


**C.2** **Open-Source Specialized Models**


**Instance Removal.** We first apply SAM 2 [55] to segment the target instance across all video frames, with
manual verification and correction of segmentation masks. The corrected masks are then fed to ROSE [56],


17


using the removal model retrained on the ROSE dataset with the PISCO [57] framework to support 720p
resolution and 121-frame sequences.


**Instance Insertion.** We use NanoBanana-Pro to perform the desired edit on a single reference frame, then
extract the newly inserted object via SAM 2 segmentation. The extracted single-frame instance serves as a
spatial control signal for PISCO, which propagates the insertion consistently across all video frames while
preserving the background.


**Instance Repositioning and Resizing.** The target instance is extracted using SAM 2 with manual correction.
A VLM (Gemini-2.0-Flash [36]) interprets the editing instruction and provides guidance for the required
spatial transformation (translation, scaling, rotation) of the segmented instance. Simultaneously, the PISCOfinetuned removal model inpaints the vacated region. Finally, PISCO-14B performs instance insertion using
the transformed instance as a spatial condition, composited onto the inpainted background video.


**Human Motion Editing.** We extract human pose keypoints using ViTPose [58] and modify them according
to Gemini-2.0-Flash’s interpretation of the editing instruction, with human-in-the-loop verification of pose
correctness. The modified pose sequence, together with additional control signals (Canny edges, depth maps
from Depth Anything V3 [59]), condition Wan-Animate to generate a new video from the original first frame.


**Camera** **Motion** **and** **Angle** **Editing.** Gemini-2.0-Flash maps the natural language instruction to predefined
camera trajectory parameters (pan, tilt, zoom, dolly, arc, etc.). ReCamMaster [60] and LightX [61] then
execute the specified camera transformation on the source video.


**Style, Creative, Visual Effect, and Attribute Editing.** For these categories, we apply NanoBanana-Pro to edit the
first frame according to the instruction, then use VACE [10] in first-frame-conditioned mode to propagate the
edit temporally across all frames. Additionally, for a subset of samples, we employ UniVideo [11] for direct
end-to-end text-conditioned video editing, similar to the commercial-model usage pattern.

#### **D Complete Annotation Guide**


This appendix provides the complete annotation guide used to train annotators for `VEFX-Dataset` . The guide
was provided in both English and Chinese; we present the English version here.


**D.1** **General Instructions**


Annotators are presented with an original video, an editing instruction, and one or more edited videos
produced by different models. For each edited video, annotators independently score three dimensions on a
4-point scale (1–4). The three dimensions must be scored independently: the score on one dimension must
not influence the score on another. When a result matches multiple descriptions, annotators should assign the
lowest applicable score. This rule is especially important when a video has both good aspects and one clear
failure that crosses the boundary to a lower level.


**D.2** **Dimension 1:** **Instruction Following (IF)**


This dimension evaluates whether the edited content accurately reflects the semantic requirements of the
instruction.

- **Score 4 — Complete and Correct Execution.** All requested edits are clearly completed, and no required
element is missing or incorrect. The target object, attribute, action, style, or camera change matches the
instruction without visible contradiction.


- **Score 3 — Mostly Correct Execution.** The core edit is completed, but one minor detail is wrong or missing.
Typical cases include correct target and edit type but slight mismatch in fine-grained attribute, appearance,
intensity, or local extent. The result should still be recognizably aligned with the instruction overall.


- **Score 2 — Partial Execution with Major Deviation.** The video shows some relationship to the instruction, but
the main requirement is only partially satisfied or is satisfied with a major semantic error. Typical cases


18


include editing the correct region but producing the wrong object or attribute, executing only one part of a
multi-step instruction, or mixing the requested edit with an obviously incorrect alternative.


- **Score 1 — Failure or Contradiction.** The instruction is not executed, the edit is largely unrelated, or the result
directly contradicts the instruction. Examples include no visible edit, editing the wrong target, or changing
the scene in the opposite direction from the requested operation.


**D.3** **Dimension 2:** **Rendering Quality (RQ)**


This dimension evaluates the visual quality of the edited video, including naturalness, clarity, physical
correctness of object movements, temporal consistency between frames, and the absence of artifacts.

- **Score** **4** **—** **High** **Visual** **Fidelity.** The video is clear, temporally stable, and visually natural throughout.
Artifacts are absent or only barely perceptible, object structure remains intact, and motion follows plausible
physical behavior.


- **Score 3 — Minor but Noticeable Degradation.** The video remains fully watchable, but there are visible quality
issues such as slight blur, local flicker, mild temporal inconsistency, or small artifact regions. These issues
are limited and do not damage the overall scene structure or object identity.


- **Score 2 — Clear Quality Failure.** Artifacts are obvious and recurrent, such as repeated flicker, deformation,
ghosting, severe blur, unstable boundaries, or unnatural motion. The content is still recognizable, but the
defects substantially reduce visual quality and viewing coherence.


- **Score 1 — Severe Visual Breakdown.** The result is visually unusable or close to unusable. Major regions are
corrupted, object identity collapses, temporal coherence is lost, or motion becomes physically implausible
to the point that the video no longer supports reliable evaluation of the intended edit.


**D.4** **Dimension 3:** **Edit Exclusivity (EE)**


This dimension evaluates whether the model executed only the specified operation without unnecessary
changes to unrelated areas. A non-target change is defined as any clearly visible modification to an object,
region, or background element that is not required by the instruction. When counting non-target changes,
multiple altered instances in different semantic regions should be counted separately.

- **Score** **4** **—** **Strict** **Preservation.** No clearly visible non-target change is introduced. All regions outside
the intended edit remain visually unchanged, except for imperceptible pixel-level differences or negligible
rendering noise.


- **Score 3 — One Clear Non-Target Change.** The intended target is edited, but exactly one additional non-target
object or semantic region is also clearly altered. The overall scene layout is still preserved, and the error
remains localized.


- **Score 2 — Two to Three Clear Non-Target Changes.** Two or three non-target objects or semantic regions are
clearly altered, or one large unintended background change affects a substantial part of the scene. The
result still resembles the original video, but over-editing is obvious.


- **Score 1 — Global or Widespread Over-Editing.** More than three non-target objects or semantic regions are
clearly altered, or the scene is globally rewritten. The result looks like a substantially different video rather
than a localized edit.


**D.5** **Dimension Decoupling Principle**


The three dimensions must be scored independently. Consider the following example:


**Instruction:** “Turn the apple into a banana.”


**Result:** The model completely fails and the apple remains unchanged.


- IF = 1 (complete failure to follow the instruction)


- RQ = score independently (if the video quality is excellent, this can still be 4)


19


- EE = score independently (if no unintended changes occurred, this can still be 4)


This principle ensures that each dimension captures a distinct aspect of editing quality.


**D.6** **Annotation Examples**


We provide all example cases from the annotation guide. Each figure shows the first frame of the original
video together with one or more edited results and their IF/RQ/EE scores. The scores are assigned from
the full video rather than from the displayed frame alone. These examples cover attribute editing, creative
editing, instance editing, visual effects, and style transfer, and illustrate how the same instruction can lead to
different score patterns across dimensions.


**Figure 7** Annotation example 1. The instruction asks to turn only the blue foreground pens into emerald green while
preserving transparency, reflections, highlights, the black pen, and the blurred background. Kling Omni receives
IF/RQ/EE = 4 _/_ 4 _/_ 4 because it executes the requested color change cleanly, keeps the plastic appearance realistic,
and leaves non-target content untouched. Grok Imagine receives 3 _/_ 4 _/_ 3 because the target edit is mostly correct and
visually clean, but the green conversion is less precise and some non-target regions are also affected, reducing both IF
and EE. Wan 2.6 receives 2 _/_ 3 _/_ 2 because the requested color transformation is incomplete, the result looks less stable
and less realistic, and unintended color changes spill into regions that should have remained unchanged.


**Figure 8** Annotation example 2. The instruction asks to replace the distant tropical islands and mountains with
glaciers and snow-covered peaks while leaving the rest of the scene intact. Grok Imagine and Kling Omni both receive
IF/RQ/EE = 4 _/_ 4 _/_ 4 because they fully carry out the requested background replacement, keep the water and boat-view
foreground natural, and introduce no obvious non-target distortions. Wan 2.6 receives 1 _/_ 4 _/_ 3 because it essentially fails
to perform the requested semantic edit: the original tropical background remains, so IF is 1. Its RQ is still 4 because
the video itself remains visually clean and artifact-free, which illustrates the intended decoupling between instruction
following and rendering quality. EE is 3 rather than 4 because, although the edit does not heavily corrupt the scene,
the output also does not faithfully realize the target modification.


20


**Figure 9** Annotation example 3. The instruction asks for a complete replacement of the white background with a
bustling construction-site interior, together with clean subject boundaries, stable depth, and relit foreground subjects.
All three edited results receive IF = 2 because they only partially satisfy the instruction: the construction-site
replacement is introduced, but the compositing and relighting are not fully convincing, so the overall request is only
partly achieved. Kling Omni receives the highest rendering score, RQ = 4, because its compositing is the cleanest and
most visually coherent over time. Grok Imagine and Wan 2.6 receive RQ = 3 because the inserted environment looks
less seamlessly integrated and shows weaker consistency. Grok Imagine and Kling Omni both receive EE = 4 because
the three people remain largely intact, whereas Wan 2.6 receives EE = 3 because the foreground subjects are altered
more noticeably during the edit.


**Figure 10** Annotation example 4. The instruction asks for a heavy snowfall effect with visible accumulation on the mossy
ground and bare branches. Grok Imagine receives IF/RQ/EE = 4 _/_ 4 _/_ 3 because it clearly adds snow and accumulation
with strong visual quality, but it also alters parts of the scene beyond the requested effect. Kling Omni receives 3 _/_ 4 _/_ 4
because the result is visually strong and preserves the scene structure well, but the snowfall effect is weaker than
requested, so the instruction is not fully satisfied. Wan 2.6 receives 4 _/_ 3 _/_ 3 because it does introduce the requested snow
effect, but the rendering is less realistic and less stable, and some non-target structure is also modified.


21


**Figure 11** Annotation example 5. The instruction asks to replace the shirt graphic with a detailed vintage red sports
car while keeping the rest of the person and scene unchanged. The edited result receives IF/RQ/EE = 3 _/_ 2 _/_ 4. IF is 3
because the shirt graphic is changed to a red car, so the main semantic request is met, but the inserted graphic is not
fully convincing as a detailed vintage illustration across the clip. RQ is 2 because the edited graphic shows noticeable
temporal instability and tracking inconsistency over time, even though the displayed frame looks acceptable. EE is 4
because the edit remains well localized to the shirt and does not introduce obvious unintended changes elsewhere in
the video.


**Figure 12** Annotation example 6. The instruction asks to convert the video into a cyberpunk style. The edited result
receives IF/RQ/EE = 4 _/_ 4 _/_ 3. IF is 4 because the neon lighting, color palette, wardrobe styling, and overall atmosphere
clearly match the requested cyberpunk aesthetic. RQ is 4 because the stylization is visually coherent and clean. EE is
reduced to 3 because the transformation also modifies unrelated details, including text, facial appearance, and other
local elements beyond the minimal style change needed to satisfy the instruction.

#### **E Inter-Annotator Agreement**


**E.1** **Cross-Check Procedure**


We randomly sample 550 examples from the annotated dataset and assign them to an independent group
of new annotators for re-annotation. The second group follows the same annotation protocol and training
procedure but has no access to the original annotations. This produces a double-annotation subset for a
focused consistency check.


22


**Figure 13** Annotation example 7. The instruction asks to replace the original black-rimmed glasses with gold-framed
aviator sunglasses while preserving the man’s facial features, expressions, head motion, reflections, and clean edges.
The edited result receives IF/RQ/EE = 3 _/_ 3 _/_ 2. IF is 3 because the target object is indeed changed into sunglasses, but
the replacement does not fully satisfy the requested appearance and realism. RQ is 3 because the local edit is usable
but not fully clean, with only moderate realism in the eyewear integration. EE is 2 because the edit also changes other
facial details, overall lighting, and background appearance, producing multiple unintended modifications outside the
requested eyewear replacement.


**E.2** **Agreement by Dimension**


Table 8 reports the agreement statistics used in the main paper.


**Table 8** Inter-annotator agreement on the 550-sample double-annotation subset.


Metric IF RQ EE

Exact Agreement (%) 75.2 87.2 72.2

Within-1 Agreement (%) 93.5 97.2 91.7


RQ achieves the strongest agreement, with 87.2% exact agreement and 97.2% within-1 agreement, indicating
that rendering quality is relatively stable across annotators. IF also shows strong consistency, with 75.2%
exact agreement and 93.5% within-1 agreement. EE remains the most challenging dimension, but still
reaches 72.2% exact agreement and 91.7% within-1 agreement, which suggests that judgments about nontarget changes are noisier yet still broadly consistent. Overall, these results support the reliability of the
three-dimensional annotation protocol while also reflecting the inherently subjective nature of fine-grained
video-editing assessment.

#### **F Extended Dataset Analysis**


We present additional analyses of `VEFX-Dataset` that complement the main text.


**F.1** **Task Type Difficulty Ranking**


Table 9 ranks the 9 task types by IF difficulty, and Figure 14 provides a finer-grained view across all 32
subcategories.


Camera Angle editing is the hardest task for IF, as it requires geometric and 3D scene reasoning that current
systems still handle poorly. Style Editing is the easiest for IF but has relatively low EE, reflecting the inherent
tension between global style transformation and strict locality preservation. Notably, RQ varies much less


23


**Table 9** Task type ranking by editing difficulty. Tasks are sorted by IF score in ascending order, so lower values indicate
harder semantic execution.


Task Type IF RQ EE _N_

Camera Angle 1.76 3.20 2.41 796

Instance Motion 2.00 3.39 3.06 450

Quantity 2.09 3.00 2.81 634

Camera Motion 2.31 3.28 2.69 383

Attribute 2.35 3.16 2.63 598

Creative 2.41 3.21 2.22 542

Instance 2.51 3.14 2.82 641

Visual Effect 2.58 3.32 2.89 520

Style 2.87 3.14 2.23 485


**Figure 14** Score breakdown across all 32 subcategories grouped by 9 main categories. Fine-grained subcategory variation
reveals which specific editing operations are most challenging.


across task types than IF or EE, which again suggests that current models find visual plausibility easier than
precise semantic execution.


**F.2** **Video Difficulty and Training Signal Quality**


Figure 15 shows the distribution of per-video difficulty, measured as the mean score across pipelines, against
cross-pipeline score variance. Videos with high score variance are especially valuable for reward-model learning
because they provide strong preference signals: different pipelines succeed or fail on the same input, enabling
the reward model to learn discriminative features rather than a dataset-wide average.


24


**Figure 15** Per-video difficulty (mean score) versus cross-pipeline score variance. High-variance videos provide especially
informative supervision for reward modeling.

#### **G Per-Category Detailed Results**


We provide finer-grained results for the six representative editing systems benchmarked in Section 6. Each
heatmap-style table reports the mean `VEFX-Reward-32B` score for one dimension at the level of the 9 main
editing categories, using the same model ordering as the main-text benchmark. To keep the focus on
comparative behavior rather than coverage statistics, we intentionally omit sample-count details here.


Across the 9 main categories, IF shows the largest variation and remains the main source of separation between
models. Grok Imagine and Kling Omni are strongest on many attribute, style, and instance-editing tasks,
while camera-angle and camera-motion edits remain difficult for nearly all systems. RQ is comparatively stable
across categories, indicating that visually plausible outputs are often easier to produce than semantically
correct ones. EE reveals the sharpest locality gap: Grok Imagine and UniVideo remain relatively strong on
localized edits, whereas VACE and Luma Ray2 degrade more visibly when preserving non-target regions
becomes difficult.



4


3


2


1



Camera Angle


Quantity


Attribute


Style


Camera Motion


Instance Motion


Instance


Visual Effect


Creative Edit



Per-Category Instruction Following Scores


|1.20|3.00|1.82|1.52|1.30|2.05|
|---|---|---|---|---|---|
|2.81|3.14|2.00|1.88|1.80|2.24|
|3.38|3.27|1.26|2.29|2.44|1.54|
|3.65|3.68|1.85|1.79|3.20|1.81|
|1.70|2.43|1.44|1.36|1.31|1.78|
|1.37|2.05|2.33|1.44|1.68|2.01|
|3.22|3.59|2.06|2.64|2.71|2.43|
|3.50|3.07|1.91|2.22|2.78|2.23|
|3.46|3.31|1.47|1.50|2.35|2.10|



**Figure 16** Heatmap table of per-category Instruction Following scores for the six benchmarked video editing systems.
Darker colors indicate higher `VEFX-Reward-32B` scores.


25


4


3


2


1



Camera Angle


Quantity


Attribute


Style


Camera Motion


Instance Motion


Instance


Visual Effect


Creative Edit



Per-Category Rendering Quality Scores


|3.47|3.73|3.53|3.00|3.27|3.37|
|---|---|---|---|---|---|
|3.19|3.45|3.37|2.94|3.25|2.94|
|3.62|3.82|3.47|3.10|3.43|2.92|
|3.76|3.68|3.44|2.58|3.25|2.88|
|2.90|3.86|3.33|2.55|3.14|3.31|
|3.21|3.33|3.33|3.00|3.26|3.04|
|3.44|3.82|3.47|3.00|3.14|3.15|
|3.38|3.47|3.45|2.78|3.50|3.00|
|3.85|3.85|3.60|3.00|3.08|3.12|



**Figure 17** Heatmap table of per-category Rendering Quality scores for the six benchmarked video editing systems.



4


3


2


1



Camera Angle


Quantity


Attribute


Style


Camera Motion


Instance Motion


Instance


Visual Effect


Creative Edit



Per-Category Edit Exclusivity Scores


|3.60|1.68|2.35|1.05|3.19|1.20|
|---|---|---|---|---|---|
|3.73|3.32|2.41|1.00|3.07|1.19|
|3.81|3.91|2.05|1.48|3.28|1.15|
|2.47|1.95|2.40|1.12|2.92|1.15|
|3.30|1.86|2.56|1.00|3.04|1.19|
|3.79|3.19|2.29|1.22|3.15|1.23|
|3.67|3.65|2.71|1.00|2.85|1.24|
|3.56|3.40|2.64|1.33|3.34|1.20|
|2.08|2.00|2.27|1.17|2.51|1.24|



**Figure 18** Heatmap table of per-category Edit Exclusivity scores for the six benchmarked video editing systems.

#### **H Additional Evaluation Details**


**H.1** **Definitions of Standard IQA/VQA Metrics**


In Section 5.2, we report four standard IQA/VQA-style metrics. We summarize their definitions here for
completeness.


**Spearman Rank-Order Correlation Coefficient (SRCC).** SRCC measures monotonic agreement between predicted
scores and human labels:

_i_ =1 _[d]_ _i_ [2]
SRCC = 1 _−_ [6][ �] _[n]_ (8)
_n_ ( _n_ [2] _−_ 1) _[,]_


where _di_ is the rank difference between the _i_ -th prediction and the corresponding human score.


**Kendall Rank-Order Correlation Coefficient (KRCC).** We use Kendall’s _τ_ -b to account for ties in the discrete 1–4


26


human scores:
_Nc −_ _Nd_
_τ_ =
�� _n_ ( _n−_ 1) �� _n_ (



(9)
2 _−_ 1) _−_ _T_ human� _[,]_



2 _−_ 1) _−_ _T_ pred�� _n_ ( _n_ 2 _−_ 1)



where _Nc_ and _Nd_ denote the numbers of concordant and discordant pairs, and _T_ pred and _T_ human denote the
numbers of tied pairs in the predicted and human rankings.


**Pearson Linear Correlation Coefficient (PLCC).** PLCC measures linear agreement after score calibration:


          - _n_
_i_ =1 [(] _[x][i][ −]_ _[x]_ [¯][)(] _[y][i][ −]_ _[y]_ [¯][)]
PLCC = �� ~~_n_~~ _[,]_ (10)
_i_ =1 [(] _[x][i][ −]_ _[x]_ [¯][)][2][ �] ~~_[n]_~~ _i_ =1 [(] _[y][i][ −]_ _[y]_ [¯][)][2]


where _xi_ is the calibrated model prediction and _yi_ is the human score.


**Root Mean Squared Error (RMSE).** RMSE measures the calibrated absolute deviation:



_n_
�( _xi −_ _yi_ ) [2] _._ (11)


_i_ =1



RMSE =




~~�~~



- [1]
_n_



**Logistic calibration.** Following common IQA/VQA protocol, we apply a four-parameter logistic mapping before
computing PLCC and RMSE:




+ _β_ 4 _,_ (12)



_q_ ( _x_ ) = _β_ 1




- 1 1
2 _[−]_ 1 + _e_ _[β]_ [2][(] _[x][−][β]_ [3][)]



where _x_ is the raw model score and _q_ ( _x_ ) is the calibrated score. The parameters _β_ 1 _, . . ., β_ 4 are fitted by
non-linear least squares on the evaluation set.


**Supplementary scatter plot.** Figure 19 directly compares `VEFX-Reward-4B` and `VEFX-Reward-32B` across IF,
RQ, EE, and Overall. Here Overall is defined as the mean of IF, RQ, and EE for both predictions and human
scores. The figure shows that scaling from 4B to 32B mainly improves IF, EE, and the overall score, where
the 32B predictions form visibly tighter trends around the human annotations. By contrast, RQ remains
relatively similar across scales, consistent with the main-text observation that rendering quality is already
easier to model than semantic faithfulness and edit locality.


**Figure 19** Side-by-side comparison between `VEFX-Reward-4B` and `VEFX-Reward-32B` across IF, RQ, EE, and Overall.


**H.2** **Additional Benchmark Visualizations**


We supplement Section 6 with two additional views of the six-model evaluation. The strip plot in Figure 20

shows the distribution of individual `VEFX-Reward-32B` scores, while the violin plot in Figure 21 emphasizes the


27


density shape for each model-dimension pair. These visualizations provide a more detailed view of score spread
and concentration, complementing the main-text box plot without repeating the same summary statistics.


Observed score distributions grouped and ordered by per-sample GeoAgg



4


3


2


1


4


3


2


1



4


3


2


1


4


3


2


1







4


3


2


1





Models

Kling o3 omni

Kling o1

Runway Gen-4.5

Seedance

Grok



Luma ray 3

Wan 2.6

Luma ray 2

UniVideo

VACE



**Figure 20** Strip plot of the six-model evaluation, showing individual `VEFX-Reward-32B` scores for IF, RQ, and EE.


Observed score distributions grouped and ordered by per-sample GeoAgg



4


3


2


1


4


3


2


1



4


3


2


1


4


3


2


1







4


3


2


1





Models

Kling o3 omni

Kling o1

Runway Gen-4.5

Seedance

Grok



Luma ray 3

Wan 2.6

Luma ray 2

UniVideo

VACE


|Kling o3 omni Kling o1 Runway Gen-4. Seedance Grok Luma ray 3 Wan 2.6 Luma ray 2 U Rendering Quality|ay 2 UniVideo VACE|
|---|---|
|<br> 5<br><br> <br> <br>Commercial<br>||
|<br> 5<br><br> <br> <br>Commercial<br>|<br>Open-source|



**Figure 21** Violin plot of the six-model evaluation, showing `VEFX-Reward-32B` score density for each model and dimension.


28


#### **I Ethical Considerations**

**Annotator welfare.** All annotators were compensated at fair market rates and were not exposed to harmful or
disturbing content. The annotation task involved evaluating video editing quality, which does not inherently
involve sensitive content. NSFW content was removed during the data curation stage.


**Potentialmisuse.** `VEFX-Reward` is designed to evaluate video editing quality. While the model could theoretically
be used to optimize for high-scoring edits that game specific metrics, the multi-dimensional scoring design
mitigates this risk by requiring simultaneous high performance across orthogonal dimensions. The ordinal
nature of the output, discrete scores 1–4, further limits the ability to exploit continuous optimization against
the reward model.


29


