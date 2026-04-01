[VIDEO-REASON.COM](https://video-reason.com)

## **A Very Big Video Reasoning Suite**


**Maijunxian Wang** [* 1] **Ruisi Wang** [* 2] **Juyi Lin** [* 3] **Ran Ji** [* 4] **Thadd¨aus Wiedemer** [5] **Qingying Gao** [6]
**Dezhi Luo** [7] **Yaoyao Qian** [3] **Lianyu Huang** [8] **Zelong Hong** [9] **Jiahui Ge** [8] **Qianli Ma** [10] **Hang He** [11]
**Yifan Zhou** [10] **Lingzi Guo** [12] **Lantao Mei** [12] **Jiachen Li** [13] **Hanwen Xing** [8] **Tianqi Zhao** [14]
**Fengyuan Yu** [2] **Weihang Xiao** [15] **Yizheng Jiao** [16] **Jianheng Hou** [8] **Danyang Zhang** [17]
**Pengcheng Xu** [18] **Boyang Zhong** [19] **Zehong Zhao** [4] **Gaoyun Fang** [20] **John Kitaoka** [21] **Yile Xu** [22]
**Hua Xu** [23] **Kenton Blacutt** [24] **Tin Nguyen** [25] **Siyuan Song** [13] **Haoran Sun** [6] **Shaoyue Wen** [20]
**Linyang He** [26] **Runming Wang** [6] **Yanzhi Wang** [3] **Mengyue Yang** [27] **Ziqiao Ma** [7] **Rapha¨el Milli`ere** [28]
**Freda Shi** [29] **Nuno Vasconcelos** [4] **Daniel Khashabi** [6] **Alan Yuille** [6] **Yilun Du** [30] **Ziming Liu** [12]
**Bo Li** [2] **Dahua Lin** [31] **Ziwei Liu** [2] **Vikash Kumar** [32] **Yijiang Li** [4] **Lei Yang** [31]
**Zhongang Cai** [2 †] **Hokin Deng** [32 †]


1 University of California, Berkeley 2 Nanyang Technological University 3 Northeastern University 4 University of
California, San Diego [5] University of T¨ubingen [6] Johns Hopkins University [7] University of Michigan [8] University of
Southern California [9] Washington University in St. Louis [10] Shanghai Jiao Tong University [11] East China Normal
University [12] Stanford University [13] University of Texas at Austin [14] University of California, Los Angeles [15] Cornell
University [16] University of North Carolina at Chapel Hill [17] San Jose State University [18] University of California,
Irvine [19] Technical University of Munich [20] Imperial College London [21] University of Wisconsin–Madison [22] University
of Edinburgh [23] Hong Kong University of Science and Technology [24] New York University [25] Auburn
University [26] Columbia University [27] University of Bristol [28] University of Oxford [29] University of
Waterloo [30] Harvard [31] The Chinese University of Hong Kong [32] Carnegie Mellon University [*] Equal contribution.

   - Correspondence to: Hokin Deng _<_ hokind@andrew.cmu.edu _>_, Zhongang Cai _<_ caiz0023@e.ntu.edu.sg _>_ .


**Figure 1** Overview of VBVR. Left: the grid shows representative tasks spanning our cognitive architecture,
which are color-coded according to their underlying capability: **Spatiality**, **Transformation**, **Knowledge**,
**Abstraction**, and **Perception** . At the center of the grids, we visualize the scale comparison between VBVR
(2.015M samples) and nine other datasets combined (12.8K samples): the sizes of the circles are drawn to
scale. Top-right: scaling behavior on in-domain and out-of-domain evaluations. Bottom-right: benchmark
performance across five cognitive capabilities.







**Abstraction**







1


[VIDEO-REASON.COM](https://video-reason.com) _A Very Big Video Reasoning Suite_


ABSTRACT


Rapid progress in video models has largely focused on visual quality, leaving their reasoning capabilities underexplored. Video reasoning grounds intelligence in spatiotemporally consistent visual
environments that go beyond what text can naturally capture, enabling intuitive reasoning over
spatiotemporal structure, such as continuity, interaction, and causality. However, systematically
studying video reasoning and its scaling behavior is hindered by the lack of large-scale video
reasoning training data. To address this gap, we introduce the **Very Big Video Reasoning (VBVR)**
**Dataset**, an unprecedentedly large-scale resource spanning _200_ curated reasoning tasks following a
principled taxonomy, and over _one million_ video clips—approximately _three orders of magnitude_
larger than existing datasets. We further present **VBVR-Bench**, a verifiable evaluation framework
that moves beyond model-based judging by incorporating rule-based, human-aligned scorers, enabling reproducible and interpretable diagnosis of video reasoning capabilities. Leveraging the
VBVR suite, we conduct one of the first large-scale **scaling studies** of video reasoning and observe
early signs of emergent generalization to unseen reasoning tasks. Together, VBVR lays a foundation
for the next stage of research in generalizable video reasoning. The data, benchmark tool kit, and
models are released publicly at **[video-reason.com](https://video-reason.com)** .


**1. Introduction**


Ground-breaking progress has been achieved in large language models, whose reasoning abilities now
generalize across challenging tasks such as coding, mathematics, and scientific discovery (Mitchell, 2025;
Rapaport, 2026). However, such capabilities remain largely confined to text-based scenarios. Meanwhile,
recent advances in video generation models have predominantly emphasized visual realism, with comparatively
limited focus on reasoning capabilities. Yet video models hold the potential to support a new paradigm of
reasoning (Wiedemer et al., 2025), grounded in spatiotemporally consistent visual environments where spatial
structure, physical dynamics, and long-range causality are naturally encoded. This makes video frames an
ideal substrate for studying reasoning grounded in the physical world. Despite this promise and growing
interest in video reasoning, the community still lacks several critical components required for systematic
progress: (1) a large-scale and diverse **dataset** to enable meaningful investigation of scaling and generalization,
(2) an **evaluation toolkit** built on verifiable and reproducible principles, and (3) an initial **scaling study** that
examines emergent capabilities in video reasoning models. In this work, we address all three challenges by
introducing the **Very Big Video Reasoning (VBVR)** suite.


First, we introduce **VBVR-Dataset**, a large-scale and diverse training source designed to facilitate systematic
study of video reasoning. We adopt a principled approach, grounding our task taxonomy in well-established
theories of human cognitive architecture (Newell & Simon, 1972; Anderson, 2007). Specifically, we organize core visual reasoning capabilities into five pillars: _abstraction_, _knowledge_, _spatiality_, _perception_, and
_transformation_ . The dataset is the result of a community-oriented, collaborative effort involving over 50
researchers and engineers from diverse disciplines worldwide, ensuring broad coverage and strong domain
expertise across 200 tasks to date. Contributors are given full freedom to design the core task semantics and
reasoning procedures, allowing for maximal diversity, while a unified, overarching task template is applied as
a standardized wrapper for input and output specification. This separation ensures consistency for automated
scaling without constraining task creativity. All tasks undergo expert human inspection to ensure quality and
correctness before being processed by our automated, cloud-based pipeline, which generates large volumes of
randomized training examples in a distributed manner. In total, VBVR-Dataset contains 2,015,000 images
and 1,007,500 video clips, making it approximately 1,000 _×_ larger than existing alternatives. Importantly, the
pipeline is immediately compatible with newly added tasks and supports scalable generation of additional
examples per task, enabling continuous expansion in both dataset breadth and scale.


Second, **VBVR-Bench** provides a systematic, reproducible, and explainable evaluation framework for video
reasoning models. While VLM-as-a-judge paradigms have been widely adopted for evaluating video generation
models (Peng et al., 2025), we explicitly enforce the use of verifiable, rule-based scorers to ensure that


2


[VIDEO-REASON.COM](https://video-reason.com) _A Very Big Video Reasoning Suite_


**Table 1** Comparison of VBVR-Dataset with existing video reasoning benchmarks. VBVR-Dataset surpasses
all prior benchmarks by multiple orders of magnitude across every dimension and is, to our knowledge, the
first to provide large-scale training data for video reasoning.


Dataset #Task #Images #Videos #Train #Test


Video-Zero-Shot (Wiedemer et al., 2025) 69 1,578 0 0 2,128
V-ReasonBench (Luo et al., 2025c) 13 652 0 0 326
MMGR (Cai et al., 2025) 10 1,323 530 0 1,853
VideoThinkBench (Tong et al., 2025) 24 8,298 0 0 4,149
TiViBench (Chen et al., 2025) 24 595 0 0 595
VR-Bench (Yang et al., 2025a) 5 0 7,920 6,336 1,538
MME-CoF (Guo et al., 2025) 12 120 0 0 120
Gen-ViRe (Liu et al., 2025) 24 117 0 0 72
Ruler-Bench (He et al., 2025) 40 101 0 0 622


**VBVR-Dataset** **200** **2,015,000** **1,007,500** **1,000,000** **7,500**


**Table 2** Foundational faculties of a human mind. One-sentence definitions are provided. The comprehensive
set of philosophical justifications and empirical supports for each faculty are available in Sec. A.


**Faculty** **Definition**


**Abstraction** To find rules from observations and use rules to deduce results.
**Knowledge** Propositional truth statements one could utter, either learned or gifted since birth.
**Perception** Immediate access to sense datum, no further justification could be provided, i.e. ”Here is one hand”
**Spatiality** The intuition of the basic properties of our world, such as three-dimensionality and Euclidean-ness.
**Transformation** To simulate spatial-temporal continuities with internal models in one’s mind


evaluation outcomes are clearly defined and fully reproducible. To validate that these task-specific scorers
faithfully reflect model capabilities, we conduct human preference alignment experiments, observing strong
agreement between automated scores and human judgments, with a Spearman’s correlation coefficient of
_ρ >_ 0 _._ 9. Leveraging VBVR-Bench, we benchmark leading proprietary models: Veo 3.1 (Google DeepMind,
2026), Sora 2 (OpenAI, 2025), Kling 2.6 (Kuaishou Technology, 2025), and Runway Gen-4 (Runway Research,
2025), alongside representative open-source models, including Wan-2.2 (WanTeam, 2025), CogVideoX1.5 (Yang et al., 2024), HuanyuanVideo (Kong et al., 2024), and LTX-2 (HaCohen et al., 2026). We reveal a
substantial gap in video reasoning capabilities across systems; the strongest model still falls short of human
performance by a large margin. Moreover, we use VBVR to analyze how different cognitive capabilities
co-develop across models, revealing non-trivial dependencies and trade-offs between reasoning skills.


Third, with a large-scale dataset and a reliable evaluation benchmark in place, we conduct an in-depth
investigation of scaling effects in video generation models. Using Wan-2.2 as the base model, we observe
concurrent performance improvements on both in-domain (ID) and out-of-domain (OOD) tasks as training
scale increases, indicating the gradual emergence of generalization capabilities. Beyond these gains, our
analysis yields several key insights. First, performance on both ID and OOD tasks eventually plateaus as data
scale increases, leaving a persistent gap between model and human performance that cannot be bridged by data
scaling alone. This suggests fundamental limitations in current video generation architectures when applied
to video reasoning. Second, although OOD performance improves substantially with scale, a consistent gap
remains between ID and OOD settings; narrowing this gap appears essential for robust, in-the-wild video
reasoning and generation. Finally, qualitative analyses reveal emergent behaviors in instruction following,
controlled editing, and semantic understanding with increased model scale, while also exposing important
limitations that motivate future research.


In summary, we present the VBVR suite, centered on an unprecedentedly large-scale and continually growing
dataset for video reasoning, **VBVR-Dataset**, together with a verifiable, human-aligned evaluation toolkit,
**VBVR-Bench** . Leveraging this suite, we conduct one of the first systematic scaling studies of video reasoning
models and uncover early, encouraging evidence of emergent generalization. We believe VBVR provides a
foundational infrastructure for future research toward generalizable video reasoning.


3


[VIDEO-REASON.COM](https://video-reason.com) _A Very Big Video Reasoning Suite_


**2. Related Works**


Since the inauguration of diffusion models and transformer-based scaling (Ho et al., 2020; Peebles & Xie,
2023), video generation models are rapidly proliferating, with closed models such as Sora, MovieGen, and Veo,
and open-source ones like CogVideoX, HunyuanVideo, and Wan (OpenAI, 2025; Polyak et al., 2024; Google
DeepMind, 2026; Yang et al., 2024; Kong et al., 2024; WanTeam, 2025). But many models are optimized for
creative production rather than explicit relational, causal, or counterfactual reasoning (Peebles & Xie, 2023;
Yang et al., 2024; Zheng et al., 2024).


Recent research increasingly investigates video generation not only as a content-creation tool, but as a reasoning
substrate (Tong et al., 2025; Guo et al., 2025; Liu et al., 2025; Wiedemer et al., 2025). A recent study has tested
Veo-3 and shown early evidence that the model exhibits nontrivial zero-shot perceptual and manipulation
behaviors and can solve simple tasks without task-specific training (Wiedemer et al., 2025). Later works now
span generation-as-reasoning paradigms (Tong et al., 2025), multi-step Chain-of-Frame diagnosis (Guo et al.,
2025; Liu et al., 2025), TI2V answer suites (Luo et al., 2025c; Chen et al., 2025), among others (He et al.,
2025; Yang et al., 2025a; Cai et al., 2025).


Despite sharper measurement, much of the ecosystem remains evaluation-heavy: standardized, large-scale
training splits and controlled ablation protocols are missing, making it difficult to run reproducible scaling
studies that directly optimize for reasoning correctness. This motivates datasets that are designed not only
to test video reasoning, but to support training for reasoning at scale under consistent domain coverage and
reliable supervision signals.


**3. Dataset**


In this section, we describe the cognitive architecture underlying our systematic task design (Sec. 3.1), present
the key statistics of VBVR-Dataset (Sec. 3.2), and detail the data generation pipeline (Sec. 3.3).


**3.1. Cognitive Architecture**


Aristotle treated cognition as an organized hierarchy of _dunameis_, cognitive faculties, ascending from _aisthesisˆ_,
perception, through _phantasia_, imagination, and _mnem¯_ _e¯_, memory, to _nousˆ_, understanding, culminating in the
extraction of _katholou_, knowledge, from _empeiria_, experience (Aristotle, 1984g;b). Kant further argued the
mind structures experience through _a priori_ intuitions and categories, aggregating by _Einbildungskraft_ (Kant,
1781). Synthesizing from two millennia of philosophical inquiry and recent cognitive and neural sciences, we
organize VBVR around five foundational cognitive faculties. **Perception** refers to the extraction of structured
representations from sensory input, what Aristotle called receiving “form without matter”, where, for example,
we test edge detection, color, and shape perception, discrimination (Aristotle, 1984g; Hubel & Wiesel,
1962; DiCarlo et al., 2012). **Transformation** is the manipulation and synthesis of mental representations,
corresponding to Aristotle’s _phantasia_ and Kant’s _Einbildungskraft_, where we use cases like mental rotation to
test (Shepard & Metzler, 1971; Zacks, 2008). **Spatiality** is the representation of places and their geometric
relationships in our world. Kant identified space as an _a priori_ form of intuition prerequisite to perception
itself, and we use cases like navigation to probe this ability (Kant, 1781; O’Keefe & Dostrovsky, 1971; Hafting
et al., 2005). **Abstraction** is the distillation of generalizable knowledge from particular experiences, Aristotle’s
_katholou_ extracted by _nousˆ_, Kant’s transcendental ideas generated by _Vernunft_, and we use cases like Raven’s
Matrices to test (Aristotle, 1984b; Kant, 1781; Carey, 2009; Badre & Nee, 2018). **Knowledge**, as Aristotle
has referred, is the _telos_ of human life. Through the faculties of our mind, humans accumulate and refine
knowledge over time. This knowledge may be intrinsic, that is, foundational or core knowledge we are born
with, or learned (Aristotle, 1984c;b;d;e; Spelke, 2000; Li et al., 2025). To operationalize these faculties in a
video-based reasoning setting, VBVR implements each category as a family of parameterized task generators.
Representative task instances for each faculty are illustrated in Fig. 2. Full philosophical grounding and
neuroscientific evidence for each faculty appear in Sec. A.


4


[VIDEO-REASON.COM](https://video-reason.com) _A Very Big Video Reasoning Suite_


**Figure** **2** Sample task instances generated from the VBVR parameterized task suite, organized by five
cognitive faculties. Each sequence illustrates the structured reasoning process required to reach a valid solution.
Tasks are implemented as deterministic generators supporting scalable instance variation while preserving
visual clarity and video dependency. Each row corresponds to a faculty defined in Section 3.1: abstract
cognitive constructs are instantiated as executable, verifiable video-based reasoning tasks.


**3.2. Data Statistics**


Table 1 compares VBVR-Dataset with existing video reasoning benchmarks. VBVR-Dataset surpasses prior
work by _multiple orders of magnitude_ across all key dimensions. Notably, most existing video reasoning
benchmarks provide few or no video samples (often lacking training data altogether), which has been a major
bottleneck for studying scaling. In total, VBVR-Dataset comprises 200 tasks: 150 tasks will be publicly
released, while the remaining 50 tasks are reserved as a hidden set for future leaderboard evaluation to preserve
benchmark integrity.


5


in Sec. 3.1. Rather than relying on implicit or post-hoc task definitions, VBVR explicitly constrains the task
space through a unified set of quality standards.


All task proposals are evaluated against six criteria: **(1)** **Information** **sufficiency**, requiring all necessary
reasoning cues to be present in the first frame and the prompt; **(2)** **Deterministic** **solvability**, ensuring a
unique and verifiable success criterion; **(3) Video dependency**, such that the task cannot be solved from a
single static image but through a process; **(4) Visual clarity**, ensuring all visual elements are distinguishable
with unambiguous layouts; **(5)** **Parametric** **diversity**, supporting the generation of at least 10,000 nontrivial instances; **(6) Technical feasibility**, avoiding unsolvable or pathological configurations under standard
rendering pipelines.


Task proposals are submitted by internal contributors and the open-source community. Each proposal specifies
the reasoning objective, expected input–output structure, and parameter space. Proposals undergo a design
review process conducted by designated reviewers, who assess cognitive validity, verifiability, and scalability.
Through this rigorous review process, slightly more than **200 task designs** have already been approved from
over 500 initial proposals. Only approved tasks proceed to implementation.


_**3.3.2. Task-Specific Generator Implementation**_


The second stage implements approved designs as executable generators. Each approved task design is
implemented as a task-specific parameterized generator. For example, a grid navigation generator produces
diverse task instances by specifying different grid sizes, obstacle placements, and start/end positions. For each
configuration, it algorithmically computes the solution and generates both the task and ground-truth outputs.
To ensure consistency across tasks, VBVR offers a standardized generator template that defines interfaces,
output formats, and validation hooks.


Each generator deterministically produces a four-component output: (1) first ~~f~~ rame.png (initial state),


6


[VIDEO-REASON.COM](https://video-reason.com) _A Very Big Video Reasoning Suite_


**Table 3** Benchmarking results on **VBVR-Bench** . Overall In-Domain (ID) and Out-of-Domain (OOD) scores
are reported alongside category-wise performance. Higher is better. **Bold** : best in group; underline: second
best.

|Col1|Col2|Col3|In-Domain by Category|Col5|Out-of-Domain by Category|
|---|---|---|---|---|---|
|**Models**|**Overall**|**Avg.**|**Abst.**<br>**Know.**<br>**Perc.**<br>**Spat.**<br>**Trans.**|**Avg.**|**Abst.**<br>**Know.**<br>**Perc.**<br>**Spat.**<br>**Trans.**|
|**Human**|0.974|0.960|0.919<br>0.956<br>1.00<br>0.95<br>1.00|0.988|1.00<br>1.00<br>0.990<br>1.00<br>0.970|
|**Open-source Models**<br>CogVideoX1.5-5B-I2V (Yang et al., 2024)<br>HunyuanVideo-I2V (Kong et al., 2024)<br>Wan2.2-I2V-A14B (WanTeam, 2025)<br>LTX-2 (HaCohen et al., 2026)|0.273<br>0.273<br>**0.371**<br>0.313|0.283<br>0.280<br>**0.412**<br>0.329|0.241<br>0.328<br>0.257<br>0.328<br>0.305<br>0.207<br>0.357<br>0.293<br>0.280<br>0.316<br>**0.430**<br>**0.382**<br>**0.415**<br>**0.404**<br>**0.419**<br>0.316<br>0.362<br>0.326<br>0.340<br>0.306|0.262<br>0.265<br>**0.329**<br>0.297|0.281<br>0.235<br>0.250<br>**0.254**<br>0.282<br>0.175<br>**0.369**<br>0.290<br>0.253<br>0.250<br>**0.405**<br>0.308<br>**0.343**<br>0.236<br>0.307<br>0.244<br>0.337<br>0.317<br>0.231<br>**0.311**|
|**Proprietary Models**<br>Runway Gen-4 Turbo (Runway Research, 2025)<br>0.403<br>0.392<br>0.396<br>0.409<br>0.429<br>0.341<br>0.363<br>0.414<br>0.515<br>0.429<br>0.419<br>0.327<br>0.373<br>Sora 2 (OpenAI, 2025)<br>**0.546**<br>**0.569**<br>0.602<br>0.477<br>**0.581**<br>**0.572**<br>**0.597**<br>**0.523**<br>0.546<br>**0.472**<br>**0.525**<br>**0.462**<br>**0.546**<br>Kling 2.6 (Kuaishou Technology, 2025)<br>0.369<br>0.408<br>0.465<br>0.323<br>0.375<br>0.347<br>0.519<br>0.330<br>0.528<br>0.135<br>0.272<br>0.356<br>0.359<br>Veo 3.1 (Google DeepMind, 2026)<br>0.480<br>0.531<br>**0.611**<br>**0.503**<br>0.520<br>0.444<br>0.510<br>0.429<br>**0.577**<br>0.277<br>0.420<br>0.441<br>0.404|**Proprietary Models**<br>Runway Gen-4 Turbo (Runway Research, 2025)<br>0.403<br>0.392<br>0.396<br>0.409<br>0.429<br>0.341<br>0.363<br>0.414<br>0.515<br>0.429<br>0.419<br>0.327<br>0.373<br>Sora 2 (OpenAI, 2025)<br>**0.546**<br>**0.569**<br>0.602<br>0.477<br>**0.581**<br>**0.572**<br>**0.597**<br>**0.523**<br>0.546<br>**0.472**<br>**0.525**<br>**0.462**<br>**0.546**<br>Kling 2.6 (Kuaishou Technology, 2025)<br>0.369<br>0.408<br>0.465<br>0.323<br>0.375<br>0.347<br>0.519<br>0.330<br>0.528<br>0.135<br>0.272<br>0.356<br>0.359<br>Veo 3.1 (Google DeepMind, 2026)<br>0.480<br>0.531<br>**0.611**<br>**0.503**<br>0.520<br>0.444<br>0.510<br>0.429<br>**0.577**<br>0.277<br>0.420<br>0.441<br>0.404|**Proprietary Models**<br>Runway Gen-4 Turbo (Runway Research, 2025)<br>0.403<br>0.392<br>0.396<br>0.409<br>0.429<br>0.341<br>0.363<br>0.414<br>0.515<br>0.429<br>0.419<br>0.327<br>0.373<br>Sora 2 (OpenAI, 2025)<br>**0.546**<br>**0.569**<br>0.602<br>0.477<br>**0.581**<br>**0.572**<br>**0.597**<br>**0.523**<br>0.546<br>**0.472**<br>**0.525**<br>**0.462**<br>**0.546**<br>Kling 2.6 (Kuaishou Technology, 2025)<br>0.369<br>0.408<br>0.465<br>0.323<br>0.375<br>0.347<br>0.519<br>0.330<br>0.528<br>0.135<br>0.272<br>0.356<br>0.359<br>Veo 3.1 (Google DeepMind, 2026)<br>0.480<br>0.531<br>**0.611**<br>**0.503**<br>0.520<br>0.444<br>0.510<br>0.429<br>**0.577**<br>0.277<br>0.420<br>0.441<br>0.404|**Proprietary Models**<br>Runway Gen-4 Turbo (Runway Research, 2025)<br>0.403<br>0.392<br>0.396<br>0.409<br>0.429<br>0.341<br>0.363<br>0.414<br>0.515<br>0.429<br>0.419<br>0.327<br>0.373<br>Sora 2 (OpenAI, 2025)<br>**0.546**<br>**0.569**<br>0.602<br>0.477<br>**0.581**<br>**0.572**<br>**0.597**<br>**0.523**<br>0.546<br>**0.472**<br>**0.525**<br>**0.462**<br>**0.546**<br>Kling 2.6 (Kuaishou Technology, 2025)<br>0.369<br>0.408<br>0.465<br>0.323<br>0.375<br>0.347<br>0.519<br>0.330<br>0.528<br>0.135<br>0.272<br>0.356<br>0.359<br>Veo 3.1 (Google DeepMind, 2026)<br>0.480<br>0.531<br>**0.611**<br>**0.503**<br>0.520<br>0.444<br>0.510<br>0.429<br>**0.577**<br>0.277<br>0.420<br>0.441<br>0.404|**Proprietary Models**<br>Runway Gen-4 Turbo (Runway Research, 2025)<br>0.403<br>0.392<br>0.396<br>0.409<br>0.429<br>0.341<br>0.363<br>0.414<br>0.515<br>0.429<br>0.419<br>0.327<br>0.373<br>Sora 2 (OpenAI, 2025)<br>**0.546**<br>**0.569**<br>0.602<br>0.477<br>**0.581**<br>**0.572**<br>**0.597**<br>**0.523**<br>0.546<br>**0.472**<br>**0.525**<br>**0.462**<br>**0.546**<br>Kling 2.6 (Kuaishou Technology, 2025)<br>0.369<br>0.408<br>0.465<br>0.323<br>0.375<br>0.347<br>0.519<br>0.330<br>0.528<br>0.135<br>0.272<br>0.356<br>0.359<br>Veo 3.1 (Google DeepMind, 2026)<br>0.480<br>0.531<br>**0.611**<br>**0.503**<br>0.520<br>0.444<br>0.510<br>0.429<br>**0.577**<br>0.277<br>0.420<br>0.441<br>0.404|**Proprietary Models**<br>Runway Gen-4 Turbo (Runway Research, 2025)<br>0.403<br>0.392<br>0.396<br>0.409<br>0.429<br>0.341<br>0.363<br>0.414<br>0.515<br>0.429<br>0.419<br>0.327<br>0.373<br>Sora 2 (OpenAI, 2025)<br>**0.546**<br>**0.569**<br>0.602<br>0.477<br>**0.581**<br>**0.572**<br>**0.597**<br>**0.523**<br>0.546<br>**0.472**<br>**0.525**<br>**0.462**<br>**0.546**<br>Kling 2.6 (Kuaishou Technology, 2025)<br>0.369<br>0.408<br>0.465<br>0.323<br>0.375<br>0.347<br>0.519<br>0.330<br>0.528<br>0.135<br>0.272<br>0.356<br>0.359<br>Veo 3.1 (Google DeepMind, 2026)<br>0.480<br>0.531<br>**0.611**<br>**0.503**<br>0.520<br>0.444<br>0.510<br>0.429<br>**0.577**<br>0.277<br>0.420<br>0.441<br>0.404|
|**Data Scaling Strong Baseline**<br>VBVR-Wan2.2<br>**0.685**<br>**0.760**<br>**0.724**<br>**0.750**<br>**0.782**<br>**0.745**<br>**0.833**<br>**0.610**<br>**0.768**<br>**0.572**<br>**0.547**<br>**0.618**<br>**0.615**|**Data Scaling Strong Baseline**<br>VBVR-Wan2.2<br>**0.685**<br>**0.760**<br>**0.724**<br>**0.750**<br>**0.782**<br>**0.745**<br>**0.833**<br>**0.610**<br>**0.768**<br>**0.572**<br>**0.547**<br>**0.618**<br>**0.615**|**Data Scaling Strong Baseline**<br>VBVR-Wan2.2<br>**0.685**<br>**0.760**<br>**0.724**<br>**0.750**<br>**0.782**<br>**0.745**<br>**0.833**<br>**0.610**<br>**0.768**<br>**0.572**<br>**0.547**<br>**0.618**<br>**0.615**|**Data Scaling Strong Baseline**<br>VBVR-Wan2.2<br>**0.685**<br>**0.760**<br>**0.724**<br>**0.750**<br>**0.782**<br>**0.745**<br>**0.833**<br>**0.610**<br>**0.768**<br>**0.572**<br>**0.547**<br>**0.618**<br>**0.615**|**Data Scaling Strong Baseline**<br>VBVR-Wan2.2<br>**0.685**<br>**0.760**<br>**0.724**<br>**0.750**<br>**0.782**<br>**0.745**<br>**0.833**<br>**0.610**<br>**0.768**<br>**0.572**<br>**0.547**<br>**0.618**<br>**0.615**|**Data Scaling Strong Baseline**<br>VBVR-Wan2.2<br>**0.685**<br>**0.760**<br>**0.724**<br>**0.750**<br>**0.782**<br>**0.745**<br>**0.833**<br>**0.610**<br>**0.768**<br>**0.572**<br>**0.547**<br>**0.618**<br>**0.615**|



(2) prompt.txt (task instruction), (3) final ~~f~~ rame.png (target state), and (4) ground ~~t~~ ruth.mp4
(complete solution trajectory). Components (1) and (2) constitute model inputs; components (3) and (4)
provide verifiable supervision—complete reasoning paths that enable learning “how” to reason, not just “what”
the answer is.


Task diversity is achieved through structured parameter spaces defined per generator. Parameters vary across
task-relevant dimensions, including object count, spatial configuration, structural complexity, and difficulty
level. Generators employ stratified sampling to ensure balanced coverage within each task’s parameter space.
Before deployment, all generators undergo code review to verify scalability, visual quality, edge-case handling,
and reproducibility under fixed random seeds. Only generators that satisfy these requirements are admitted to
large-scale production.


_**3.3.3. Large-Scale Generation and Control**_


The final stage executes validated generators at scale within a distributed generation framework. VBVR
generates one million training samples across 100 training tasks (10,000 per task) and 7500 test samples across
150 test tasks (50 per task). Training and test splits are constructed using disjoint random seed ranges to prevent
data leakage. Quality control is fully automated during generation. Each sample is validated for the existence
of a solution, visual compliance, and boundary constraints. Failed generations trigger automatic retries;
persistent failures are logged for further generator refinement. System-level monitoring tracks generation
statistics and validation failure rates across tasks. From the 150 approved task designs, we organize 100 tasks
for training and 100 tasks for testing, with a carefully designed dual-split strategy to assess both in-distribution
robustness and out-of-distribution generalization in Sec. 4.1.


The parameterized infrastructure supports continuous expansion: standardized generator templates enable
community contributors to develop new tasks while automated validation ensures consistent quality. This
positions VBVR as a living benchmark that evolves with the field’s understanding of video reasoning.
Implementation details and generator specifications are provided in Sec. B.


**4. Benchmark**


In this section, we introduce the evaluation toolkit (Sec. 4.1) and assess its validity through alignment with
human preferences (Sec. 4.2). We subsequently report the performance of leading video generation models
(Sec. 4.3) and investigate the correlations among their reasoning capabilities (Sec. 4.4).


7


[VIDEO-REASON.COM](https://video-reason.com) _A Very Big Video Reasoning Suite_


**4.1. Evaluation Kit**


To systematically assess model reasoning capabilities, VBVR-Bench employs a dual-split evaluation strategy
across 100 diverse tasks. The first split contains 50 tasks that overlap with the training categories but differ
in unseen parameter configurations and sample instances, providing a test of _in-domain generalization_ . The
second split includes the remaining 50 tasks, which are entirely novel and are designed to measure _out-of-_
_domain_ _generalization_ . It tests whether models can solve reasoning challenges without prior exposure to
similar structures, and thus whether they acquire transferable reasoning primitives rather than relying on
task-specific memorization. Each task consists of five test samples, enabling statistically robust evaluation
across diverse reasoning scenarios.


A key feature of VBVR-Bench is its fully **rule-based evaluation framework**, which is feasible because most
test tasks have a unique, verifiable correct answer, allowing interpretable evaluation based on spatial position,
color, object identity, path, or logical outcome. Moreover, geometric, physical, or deductive constraints are
also considered in the scoring rubrics. Each of the 100 test tasks is paired with a dedicated evaluation rule,
with scores on multiple aspects to compute a weighted, comprehensive score. Sub-criteria include spatial
accuracy, trajectory correctness, temporal consistency, and logical validity.


For example, in the Task G-45: Key Door Matching (More examples are included in Sec. D), a green dot agent
must first locate a color-specified key and then navigate to the matching door within a grid maze. Performance
is scored across four weighted dimensions: target identification accuracy (30%), path validity (30%), path
efficiency (20%), and animation quality (20%). Target identification verifies that the agent selects the correct
key and door without confusing colors, path validity ensures the agent follows allowed paths without wall
collisions, path efficiency compares the actual trajectory to the optimal BFS path, and animation quality checks
smooth frame-by-frame movement and precise object alignment. A full score indicates perfection in all four
dimensions (correct key and door selection, near-optimal pathing, and precise spatial and temporal alignment).


Overall, VBVR-Bench provides:


  - **Reproducibility** **and** **Determinism** . The evaluation is fully deterministic and avoids the stochastic
variability or hallucinations associated with LLM-based judgments.

  - **Granular Verifiability** . Each task is decomposed into interpretable vectors, allowing precise measurement of spatial, temporal, and logical correctness, even at the pixel or object-property level.

  - **Transparent Diagnosis** . By explicitly encoding reasoning constraints, the benchmark ranks models _and_
reveals systematic trade-offs, capability gaps, trade-offs, and cross-domain performance trends.


**4.2. Human Preference Alignment Analysis**


To assess alignment between VBVR-Bench and human perception, we conduct a large-scale human preference
study and compare model win ratios derived from human judgments with those computed from VBVR-Bench’s
automatic metrics. Specifically, human win ratios are obtained from pairwise preference annotations, where a
model is considered to win if it is preferred over another model for the same prompt. In contrast, VBVR-Bench
win ratios are computed by ranking models by their per-sample automatic scores and counting how often each
model outperforms others. As shown in Fig. 4, the two sets of win ratios exhibit strong positive correlations
across models, indicating that VBVR-Bench provides reliable and human-aligned performance estimates.
Details of the study are provided in the Sec. C.2.


**4.3. Leading Model Performances**


Table 3 shows performance across model families. Most open-source baselines cluster between 0.27 and 0.31
overall, indicating limited capability in complex video reasoning, while Wan2.2-I2V-A14B is the strongest
open-source baseline at 0.371. Proprietary models perform better overall, led by Sora 2 (0.546) and Veo 3.1
(0.480), particularly in Abstraction and Transformation categories.


Fine-tuning Wan2.2-I2V-A14B on VBVR-Dataset yields VBVR-Wan2.2, which achieves a new state of the art
with an overall score of 0.685, representing an 84.6% relative improvement over its base model. VBVR-Wan2.2


8


[VIDEO-REASON.COM](https://video-reason.com) _A Very Big Video Reasoning Suite_


**Figure 4** Human alignment analysis for VBVR-Bench. Our experiments show that VBVR-Bench evaluations
in all splits closely match human perceptions. In each plot, a dot represents the human preference win ratio
(horizontal axis) and VBVR-Bench evaluation win ratio (vertical axis) for a particular video generation model.
We linearly fit a straight line to visualize the correlation, and calculate the Spearman’s correlation coefficient
( _ρ_ ) for each dimension.


attains the best performance across all evaluated categories, with especially strong results in Spatiality and
Perception, suggesting that large-scale reasoning-oriented data substantially enhances integrated world-model
reasoning capabilities.


Notably, despite these gains, a considerable gap to human performance remains. This highlights the persistent
challenges of long-horizon temporal reasoning and robust symbolic manipulation in video generation. We
further analyze how performance evolves with increasing training data under a fixed architecture, and how
in-domain and out-of-domain generalization behaviors differ, in Sec. 5.


We also analyze the stability and consistency of model behavior using domain-wise score distributions that
reveal performance variability and rating noise across domains (see Sec. C.3.2).


**4.4. Capability Correlation**


**Figure 5** Residualized capability correlation among five faculties across 9 models (Pearson _ρ_ ). We regress
out a model-level general factor (overall strength) to highlight _structural_ dependencies and inter-relations.


We further study _capability dependency_ among the five cognitive faculties, asking whether strengths in one
capability tend to co-occur with strengths in another across models. A naive correlation is often dominated by


9


[VIDEO-REASON.COM](https://video-reason.com) _A Very Big Video Reasoning Suite_


overall model strength (i.e., stronger models score higher on _all_ categories). To isolate _structural_ dependencies,
we compute category-level mean scores per model and regress out a model-level _general factor_ (overall mean
score) before measuring Pearson correlations on the residuals. See Sec. C.3.1 for more implementation details.


Figure 5 reveals non-trivial structures underlying the cognitive faculties. We observe a strong positive
coupling between **Knowledge** and **Spatiality** ( _ρ_ = 0 _._ 461). This result is particularly interesting given the
past neuroscience studies which suggest human brains use hippocampal place cells and grid cells to support
concept learning. One seminal study suggests patients with bilateral hippocampal damage were impaired at
learning both spatial and non-spatial configural associations in a deterministic feedback task, showing only
partial, inflexible residual learning, supporting a domain-general hippocampal role in binding and configural
learning (Kumaran et al., 2007). The follow-up study shows a hippocampus–ventromedial prefrontal cortex
circuit supports the emergence of conceptual knowledge that guides choices, and the hippocampus is uniquely
required to transfer that knowledge to a perceptually novel setting (Kumaran et al., 2009). Edward Tolman
in last century hypothesizes that our spatial map of the physical world could be transferred to be used as a
**cognitive map**, which is a mental representation, not only used for spatial navigation, but conceptual space
construction, and general knowledge learning (Tolman, 1948; Yang et al., 2025b). Converging evidence from
neuroscience and AI are coming into places to suggest the deep inter-relatedness between cognitive spatial
intrinsics and knowledge acquisition (Baram et al., 2024; Whittington et al., 2025; Xiao et al., 2025).


In contrast, **Knowledge** correlates strongly negatively with **Perception** ( _ρ_ = _−_ 0 _._ 757). One very interesting
debate in cognitive science is whether we should count core knowledge, which are knowledge that we are born
with, as actually perception (Bai et al., 2025). Namely, instead of understanding intuitive physics or object
permanence as a kind of knowledge, we should actually consider them as a kind of perception, which are
actually supported by our perceptual neural circuits, such as medial temporal lobe, rather than our learning and
memory circuits, such as hippocampus (Hassabis & Maguire, 2009; Martin & Barense, 2023)


**Abstraction** shows a strong negative correlation with **Transformation** ( _ρ_ = _−_ 0 _._ 641) and a moderate one with
**Spatiality** ( _ρ_ = _−_ 0 _._ 481), and do not show any signs of positive correlations with any other cognitive faculties.
This result is consistent with our understanding with the modularity of abstraction faculty in our brain, namely
prefrontal cortex (Vaidya & Badre, 2022; Passingham & Lau, 2023; Bein & Niv, 2025; Li et al., 2026)


Moreover, **Perception** trades off with **Spatiality** ( _ρ_ = _−_ 0 _._ 565) but is nearly uncorrelated with both **Ab-**
**straction** ( _ρ_ = _−_ 0 _._ 043) and **Transformation** ( _ρ_ = 0 _._ 057). **Transformation** is also nearly uncorrelated
with **Spatiality** ( _ρ_ = _−_ 0 _._ 050). Overall, VBVR-Bench not only ranks models but also enables interpretable
diagnosis of how capabilities co-develop or decouple across systems.


**5. VBVR-Wan2.2 Analysis**


We further investigate VBVR-Wan2.2 to gain insights into scaling video reasoning. We first describe the
experimental settings (Sec. 5.1), followed by an analysis of the scaling behavior (Sec. 5.2), comprehensive
qualitative evaluations (Sec. 5.3), and performance on general video benchmarks (Sec. 5.4).


**5.1. Experiment settings**


We conduct all experiments on Wan2.2-I2V-A14B without architectural modifications, as the goal of VBVRWan2.2 is to **investigate data scaling behavior** and provide a **strong baseline model** for the video reasoning
research community. Leveraging the VBVR-Dataset, which to our knowledge constitutes one of the largest
video reasoning datasets to date, enables a systematic investigation of scaling behaviors in video-based
reasoning under a fixed model architecture. For training, we adopt a learning rate of 1e-4 and train for one
epoch in each experiment. We employ LoRA adaptation on the DiT backbone, and applying LoRA to the
modules q, k, v, o, ffn.0, ffn.2 with a lora rank of 32.


10


[VIDEO-REASON.COM](https://video-reason.com) _A Very Big Video Reasoning Suite_


**Table 4** Performance by Data Scale (0K–500K). **Bold** : best per column; underline: second best.


**In-Domain by Category** **Out-of-Domain by Category**


**Models** **Overall** **Avg.** **Abst.** **Know.** **Perc.** **Spat.** **Trans.** **Avg.** **Abst.** **Know.** **Perc.** **Spat.** **Trans.**


**0K** 0.371 0.412 0.430 0.382 0.415 0.404 0.419 0.329 0.405 0.308 0.343 0.236 0.307
**50K** 0.549 0.576 0.527 0.584 0.537 0.642 0.654 0.522 0.596 0.584 0.507 0.482 0.490
**100K** 0.623 0.701 0.622 0.680 0.777 0.719 0.759 0.545 0.622 0.524 0.533 0.557 0.517
**200K** **0.689** 0.767 0.739 0.709 0.791 **0.799** 0.825 **0.611** 0.748 **0.621** 0.545 **0.659** 0.599
**300K** 0.682 0.763 0.733 0.713 **0.795** 0.776 0.827 0.601 0.732 0.596 0.542 0.628 0.600
**400K** 0.682 **0.771** **0.744** 0.744 0.793 0.753 **0.848** 0.593 0.742 0.592 0.532 0.605 0.588
**500K** 0.685 0.760 0.724 **0.750** 0.782 0.745 0.833 0.610 **0.768** 0.572 **0.547** 0.618 **0.615**


**5.2. Scaling Curve**


To systematically investigate data scaling behavior, we progressively increase the training data size from 0K
samples (the original Wan2.2 base model) to 500K samples (VBVR-Wan2.2), and report the corresponding
performance changes in Tab. 4.


First, training VBVR-Wan2.2 shows clear but **saturating gains from data scaling** . In-domain (ID) performance improves substantially with increased training data, rising from 0.412 at initialization to about 0.771 at
400K samples, after which gains plateau and slightly fluctuate. The failure to approach perfect accuracy, even
within familiar distributions, suggests that current video generation architectures exhibit fundamental representational and optimization bottlenecks. In particular, these tasks require the simultaneous satisfaction of logical
constraints and long-term temporal consistency, while the stochastic nature of video generation introduces
cumulative rendering noise and temporal drift. Importantly, this saturation regime makes VBVR-Dataset a
valuable testbed for researchers to investigate architectural advances, such as explicit state tracking, structured
reasoning modules, or self-correction mechanisms, under controlled and scalable evaluation settings.


Second, examining **generalization to out-of-domain (OOD) tasks** highlights critical insights. Both ID and
OOD performance improve with more data, ID from 0.412 to 0.760, and OOD from 0.329 to 0.610. This
indicates that **scaling data enhances transferable reasoning capabilities** beyond memorized patterns. Our
qualitative analysis in Sec. 5.3 further illustrates how the model benefits from increased training data and
generalizes to out-of-domain tasks, providing interpretable insights into improvements in temporal consistency,
logical reasoning, and task transferability. However, a persistent 15% generalization gap remains, suggesting
that **increasing data within fixed task distributions is insufficient for robust systematic generalization** .
With our data factory, we plan to continuously introduce **new task families and richer compositional regimes**
in future releases, enabling broader coverage of reasoning patterns and better closing the ID–OOD gap.


**5.3. Qualitative Analysis**


We qualitatively compare Wan2.2-I2V-A14B (base model), VBVR-Wan2.2, and the strongest proprietary
baseline in our study, Sora 2. A recurring pattern is that, after VBVR training, VBVR-Wan2.2 can match
or even surpass Sora 2 on a broad set of tasks that require _verifiable_ manipulations under stable scenes.
This motivates our central takeaway: **controllability** **before** **reasoning** . If a model freely rewrites the
scene (background/layout/object identity) during generation, intermediate states become unreliable and any
“reasoning action” (delete/move/mark) is no longer verifiable. In practice, the base model(Wan2.2-I2V-A14B)
often fails in precisely this way: it may not preserve target identity or stable layouts, thereby breaking the
prerequisite for manipulation-based reasoning.


To make qualitative comparisons direct and reproducible, we select examples as **same-task, same-sample**
**comparisons** whenever multiple models are shown on the same case. Importantly, the representative cases
in Fig. 6 are **out-of-domain (OOD) task families held out from training**, so improvements reflect transfer to
novel task structures rather than memorization.


**Controllable** **execution** **under** **constraints** **(VBVR-Wan2.2** **vs** **Sora** **2).** Panel A highlights that VBVR
training primarily improves _constraint-following, tool-like execution_ under stable scenes. On O-5 Task, Sora
2 introduces extra, unnecessary operations: after deleting the target symbol, it further merges/re-layouts the
remaining symbols, violating the intended minimal-edit constraint from the task. In contrast, VBVR-Wan2.2


11


[VIDEO-REASON.COM](https://video-reason.com) _A Very Big Video Reasoning Suite_


**Figure 6** Qualitative overview on held-out OOD task families. Panel A presents same-task, same-sample
comparisons between VBVR-Wan2.2 and Sora 2 on three controllable-execution tasks: O-5 (delete the marked
symbol with minimal unintended changes), O-6 (apply a 2D geometric rotation under the target cue), and
O-30 (rearrange a bookshelf by moving an object into the designated slot), with checkmarks/crosses indicating
task success/failure. Panel B shows VBVR-Wan2.2-only emergent behaviors on O-49 (complete a symmetric
pattern with a consistent self-chosen policy) and O-11 (“rationalizing”: modifying intermediate elements to
fit an internally assumed transformation narrative). Panel C reports honest boundaries of VBVR-Wan2.2 on
G-47 (long-horizon key–door navigation, with possible agent duplication/flickering) and O-21 (blueprint
gap filling, where the video can be correct yet procedurally unfaithful).















exhibits an emergent “do exactly what is asked” capability, deleting the marked symbol _without_ additional
changes. On O-6 Task, Sora 2 may fail to maintain scene control and to distinguish the target region from the
object to be manipulated, leading to a degenerate outcome where the box and object rotate together. In contrast,
VBVR-Wan2.2 correctly separates the target cue from the manipulated object and performs a pivot-based
rotation that aligns with the task requirement, suggesting emergent geometric manipulation skills beyond the
training task families. On O-30, VBVR-Wan2.2 successfully performs the required constrained relocation
(moving a book into the designated slot). Notably, Sora 2 can fail by producing auxiliary markings/lines
without executing the actual object manipulation, illustrating that even strong proprietary models may break
down when success requires precise, constraint-following control rather than generic scene editing.


**Emergent strategies and multi-step behavior (VBVR-Wan2.2).** Beyond controlled, tool-like execution,
we observe emergent _strategy-level_ regularities and multi-step behaviors on OOD task families. On O-49,
VBVR-Wan2.2 often produces a rule-consistent completion of the missing half while exhibiting a distinctive,
_self-chosen_ completion policy: across samples, the completion typically appears as a smooth, coherent “fade-in”
fill rather than discrete cell-by-cell edits. This consistency suggests that the model is not merely matching static
templates, but is transferring controllable execution primitives and organizing them into a stable policy under a


12


[VIDEO-REASON.COM](https://video-reason.com) _A Very Big Video Reasoning Suite_


new task structure. On O-11, we sometimes observe behaviors resembling “understand _→_ act _→_ adjust”. In
addition to applying the intended two-step transformation to the queried shape (first change color, then move
it), VBVR-Wan2.2 may modify intermediate elements (e.g., shifting a misaligned reference shape toward the
arrow cue; arrows are manually overlaid for visualization), effectively _rationalizing_ an internally assumed
transformation narrative. While such interventions may conflict with the ground-truth reasoning trace and
still yield imperfect final answers, they provide a qualitative signal that the model is maintaining scene-level
coherence and executing multi-step plans rather than producing one-shot, uncontrolled scene rewrites.


**Limitations and failure modes (VBVR-Wan2.2).** Despite improved scene controllability, several challenging
regimes remain. We observe _process unfaithfulness_ in tasks with explicit procedural ground truth. On O-21
( _construction blueprint_ ), the gold procedure scans candidate pieces one-by-one, previews each candidate at
the gap, marks incorrect candidates with a cross, and stops when the correct candidate is found and placed.
The generated video can mimic a plausible-looking trial-and-error process without faithfully reflecting the
true decision mechanism (“correct answer, wrong method”), highlighting the need for stronger process-level
supervision and evaluation. Finally, long-horizon control can break down in interactive tasks. On G-47,
compared to the base model that may move doors/keys directly, VBVR-Wan2.2 better distinguishes the agent
from scene entities and exhibits the correct high-level subgoal structure (fetch key _→_ reach door). However,
it can still suffer from control failures such as agent duplication/flickering when traversing a coherent path,
indicating that maintaining identity and stable dynamics over long horizons remains an open problem.


In summary, these qualitative insights reinforce a fundamental shift in evaluating video intelligence: **con-**
**trollability** **is** **the** **bedrock** **of** **verifiable** **reasoning.** Our results demonstrate that VBVR training moves
beyond generic video synthesis, instilling a ’controllability-first’ execution logic that generalizes even to
novel, out-of-domain task structures. While VBVR-Wan2.2 shows a nascent ability to coordinate multi-step
strategies, the remaining gap in process faithfulness and long-term identity stability highlights the next frontier.
Achieving true video reasoning will require not just larger scale, but a move toward models that can maintain
rigorous causal and physical constraints over extended temporal horizons.


**5.4. General Performance on VBench++**


**Table 5** Comprehensive evaluation results on VBench-I2V.


Total I2V Quality Video-Text Video-Image Video-Image Subject Background Motion Dynamic Aesthetic Imaging
Model
Score Score Score Camera Motion Subject Consist. Backgr. Consist. Consistency Consistency Smoothness Degree Quality Quality
Wan2.2-I2V-A14B 0.8816 0.9582 0.8050 0.5444 0.9752 0.9903 0.9468 0.9672 0.9832 0.5285 0.6153 0.7036
VBVR-Wan2.2 0.8835 0.9678 0.7992 0.6592 0.9804 0.9921 0.9547 0.9722 0.9852 0.4106 0.6153 0.7080


To evaluate the performance of VBVR-Wan2.2 in real-world video generation scenarios, we benchmarked
it against the Wan2.2-I2V-A14B base model using the VBench-I2V suite. As shown in the Tab. 5, After
LoRA training on VBVR-Dataset, the model maintains a high level of performance across all core metrics,
demonstrating that VBVR-Wan2.2 does not undermine the fundamental generative capabilities of the base
model. Notably, we observed a significant increase in Video-Text Camera Motion Consistency (rising from
0.5444 to 0.6592), accompanied by a decrease in Dynamic Degree. These quantitative results align closely
with our qualitative findings. That is, the model exhibits a more precise understanding of motion dynamics,
effectively discerning which regions require temporal change and which should remain preserved. This balance
results in videos that are both more stable and better aligned with the provided motion prompts.


**6. Conclusion**


In this work, we present VBVR-Dataset, the first large-scale and diverse training dataset designed for video
reasoning, along with VBVR-Bench, a comprehensive evaluation toolkit for verifiable and reproducible
assessment. Through systematic scaling studies, we demonstrate that increasing model scale leads to early
signs of emergent generalization in video reasoning.


13


[VIDEO-REASON.COM](https://video-reason.com) _A Very Big Video Reasoning Suite_


**References**


Allison, H. E. _Kant’s Transcendental Idealism:_ _An Interpretation and Defense_ . Yale University Press, New
Haven, revised and enlarged edition, 2004.


Andersen, R. A., Snyder, L. H., Bradley, D. C., and Xing, J. Multimodal representation of space in the posterior
parietal cortex and its use in planning movements. _Annual Review of Neuroscience_, 20:303–330, 1997. doi:
10.1146/annurev.neuro.20.1.303.


Anderson, J. R. _Rules of the Mind_ . Lawrence Erlbaum Associates, Hillsdale, NJ, 1993.


Anderson, J. R. _How Can the Human Mind Occur in the Physical Universe?_ Oxford University Press, 2007.


Anderson, J. R. _Language, memory, and thought_ . Psychology Press, 2013.


Anderson, J. R. and Lebiere, C. _The Atomic Components of Thought_ . Lawrence Erlbaum Associates, Mahwah,
NJ, 1998.


Aristotle. On memory. In Barnes, J. (ed.), _The Complete Works of Aristotle:_ _The Revised Oxford Translation_,
volume 1, pp. 714–720. Princeton University Press, 1984a.


Aristotle. Metaphysics. In Barnes, J. (ed.), _The Complete Works of Aristotle:_ _The Revised Oxford Translation_,
volume 2, pp. 1552–1728. Princeton University Press, 1984b.


Aristotle. _Physics_, volume 1. Princeton University Press, 1984c.


Aristotle. _Posterior Analytics_, volume 1. Princeton University Press, 1984d.


Aristotle. Prior analytics. In Barnes, J. (ed.), _The Complete Works of Aristotle: The Revised Oxford Translation_,
volume 1 of _Bollingen Series_ . Princeton University Press, Princeton, NJ, 1984e.


Aristotle. Sense and sensibilia. In Barnes, J. (ed.), _The Complete Works of Aristotle:_ _The Revised Oxford_
_Translation_, volume 1, pp. 693–713. Princeton University Press, 1984f.


Aristotle. On the soul. In Barnes, J. (ed.), _The Complete Works of Aristotle:_ _The Revised Oxford Translation_,
volume 1, pp. 641–692. Princeton University Press, 1984g.


Badre, D. and Nee, D. E. Frontal cortex and the hierarchical control of behavior. _Trends in Cognitive Sciences_,
22(2):170–188, 2018.


Bai, D., Hafri, A., Izard, V., Firestone, C., and Strickland, B. “core perception”: Re-imagining precocious
reasoning as sophisticated perceiving. _Behavioral and Brain Sciences_, pp. 1–75, 2025.


Baillargeon, R., Spelke, E. S., and Wasserman, S. Object permanence in five-month-old infants. _Cognition_, 20
(3):191–208, 1985.


Baker, N., Lu, H., Erlikhman, G., and Kellman, P. J. Deep convolutional networks do not classify based on
global object shape. _PLoS Computational Biology_, 14(12):e1006613, 2018. doi: 10.1371/journal.pcbi.
1006613.


Banino, A., Barry, C., Uria, B., Blundell, C., Lillicrap, T., Mirowski, P., Pritzel, A., Chadwick, M. J., Degris,
T., Modayil, J., Wayne, G., Soyer, H., Viola, F., Zhang, B., Goroshin, R., Rabinowitz, N., Pascanu, R.,
Beattie, C., Petersen, S., Sadik, A., Gaffney, S., King, H., Kavukcuoglu, K., Hassabis, D., Hadsell, R., and
Kumaran, D. Vector-based navigation using grid-like representations in artificial agents. _Nature_, 557(7705):
429–433, 2018. doi: 10.1038/s41586-018-0102-6.


Bao, P., She, L., McGill, M., Bhattacharyya, R., and Tsao, D. Y. A map of object space in primate inferotemporal cortex. _Nature_, 583:103–108, 2020. doi: 10.1038/s41586-020-2350-5.


14


[VIDEO-REASON.COM](https://video-reason.com) _A Very Big Video Reasoning Suite_


Baram, A., Nili, H., Barreiros, I., Samborska, V., Behrens, T. E., and Garvert, M. M. An abstract relational
map emerges in the human medial prefrontal cortex with consolidation. _bioRxiv_, pp. 2024–10, 2024.


Behrens, T. E. J., Muller, T. H., Whittington, J. C. R., Mark, S., Baram, A. B., Stachenfeld, K. L., and
Kurth-Nelson, Z. What is a cognitive map? Organizing knowledge for flexible behavior. _Neuron_, 100(2):
490–509, 2018. doi: 10.1016/j.neuron.2018.10.002.


Bein, O. and Niv, Y. Schemas, reinforcement learning and the medial prefrontal cortex. _Nature_ _Reviews_
_Neuroscience_, 26(3):141–157, 2025.


Bengio, Y., Courville, A., and Vincent, P. Representation learning: A review and new perspectives. _IEEE_
_Transactions on Pattern Analysis and Machine Intelligence_, 35(8):1798–1828, 2013.


Bertolero, M. A., Yeo, B. T. T., and D’Esposito, M. The modular and integrative functional architecture of
the human brain. _Proceedings of the National Academy of Sciences_, 112(49):E6798–E6807, 2015. doi:
10.1073/pnas.1510619112.


Bonhoeffer, T. and Grinvald, A. Iso-orientation domains in cat visual cortex are arranged in pinwheel-like
patterns. _Nature_, 353:429–431, 1991.


Bowman, C. R. and Zeithamova, D. Abstract memory representations in the ventromedial prefrontal cortex
and hippocampus support concept generalization. _Journal of Neuroscience_, 38(10):2605–2614, 2018.


Brincat, S. L., Siegel, M., von Nicolai, C., and Miller, E. K. Gradual progression from sensory to task-related
processing in cerebral cortex. _Proceedings of the National Academy of Sciences_, 115(30):E7202–E7211,
2018.


Burgess, P. W., Dumontheil, I., and Gilbert, S. J. The gateway hypothesis of rostral prefrontal cortex (area 10)
function. _Trends in Cognitive Sciences_, 11(7):290–298, 2007.


Cai, Z., Qiu, H., Ma, T., Zhao, H., Zhou, G., Huang, K.-H., Kordjamshidi, P., Zhang, M., Xiao, W., Gu, J.,
Peng, N., and Hu, J. MMGR: Multi-modal generative reasoning. _arXiv preprint arXiv:2512.14691_, 2025.
[URL https://arxiv.org/abs/2512.14691.](https://arxiv.org/abs/2512.14691)


Calvert, G. A. Crossmodal processing in the human brain: Insights from functional neuroimaging studies.
_Cerebral Cortex_, 11(12):1110–1123, 2001.


Carey, S. _The Origin of Concepts_ . Oxford Series in Cognitive Development. Oxford University Press, New
York, 2009.


Carey, S. Pr´ecis of The Origin of Concepts. _Behavioral and Brain Sciences_, 34(3):113–124, 2011.


Carey, S. and Spelke, E. Science and core knowledge. _Philosophy of Science_, 63(4):515–533, 1996.


Chakladar, D. D. Cortex level connectivity between act-r modules during eeg-based n-back task. _Cognitive_
_Neurodynamics_, 18(6):4033–4045, December 2024. doi: 10.1007/s11571-024-10177-y.


Chen, H. H., Lan, D., Shu, W.-J., Liu, Q., Wang, Z., Chen, S., Cheng, W., Chen, K., Zhang, H., Zhang, Z., Guo,
R., Cheng, Y., and Chen, Y.-C. Tivibench: Benchmarking think-in-video reasoning for video generative
models. _arXiv preprint arXiv:2511.13704_, 2025. [URL https://arxiv.org/abs/2511.13704.](https://arxiv.org/abs/2511.13704)


Christoff, K., Keramatian, K., Gordon, A. M., Smith, R., and Madler, B.¨ Prefrontal organization of cognitive
control according to levels of abstraction. _Brain Research_, 1286:94–105, 2009.


Colby, C. L. and Goldberg, M. E. Space and attention in parietal cortex. _Annual Review of Neuroscience_, 22:
319–349, 1999. doi: 10.1146/annurev.neuro.22.1.319.


d’anthropologie de Paris, S. _Bulletins de la Soci´et´e d’anthropologie de Paris_ . Masson., 1898.


15


[VIDEO-REASON.COM](https://video-reason.com) _A Very Big Video Reasoning Suite_


DiCarlo, J. J., Zoccolan, D., and Rust, N. C. How does the brain solve visual object recognition? _Neuron_, 73
(3):415–434, 2012.


Friston, K. The free-energy principle: A unified brain theory? _Nature Reviews Neuroscience_, 11:127–138,
2010. doi: 10.1038/nrn2787.


Geirhos, R., Narayanappa, K., Mitzkus, B., Thieringer, T., Bethge, M., Wichmann, F. A., and Brendel, W.
Partial success in closing the gap between human and machine vision. _Advances in Neural Information_
_Processing Systems_, 34:23885–23899, 2021.


Gentner, D. Structure-mapping: A theoretical framework for analogy. _Cognitive Science_, 7(2):155–170, 1983.


Gentner, D. and Hoyos, C. Analogy and abstraction. _Topics in Cognitive Science_, 9(3):672–693, 2017. doi:
10.1111/tops.12278.


Ghazanfar, A. A. and Schroeder, C. E. Is neocortex essentially multisensory? _Trends in Cognitive Sciences_,
10(6):278–285, 2006. doi: 10.1016/j.tics.2006.04.008.


Gibson, J. The ecological approach to visual perception: classic edition, 2014.


Gilboa, A. and Marlatte, H. Neurobiology of schemas and schema-mediated memory. _Trends in Cognitive_
_Sciences_, 21(8):618–631, 2017.


Goodale, M. A. and Milner, A. D. Separate visual pathways for perception and action. _Trends in Neurosciences_,
15(1):20–25, 1992. doi: 10.1016/0166-2236(92)90344-8.


Google DeepMind. Veo 3.1. Technical report, Google DeepMind, 2026. [URL https://blog.google/](https://blog.google/innovation-and-ai/technology/ai/veo-3-1-ingredients-to-video/)
[innovation-and-ai/technology/ai/veo-3-1-ingredients-to-video/.](https://blog.google/innovation-and-ai/technology/ai/veo-3-1-ingredients-to-video/) Released
January 13, 2026.


Greco, A., Moser, J., Preissl, H., and Siegel, M. Predictive learning shapes the representational geometry of
the human brain. _Nature communications_, 15(1):9670, 2024.


Guo, Z., Chen, X., Zhang, R., An, R., Qi, Y., Jiang, D., Li, X., Zhang, M., Li, H., and Heng, P.-A. Are video
models ready as zero-shot reasoners? an empirical study with the MME-CoF benchmark. _arXiv preprint_
_arXiv:2510.26802_, 2025. [URL https://arxiv.org/abs/2510.26802.](https://arxiv.org/abs/2510.26802)


Guyer, P. _Kant and the Claims of Knowledge_ . Cambridge University Press, Cambridge, 1987.


HaCohen, Y., Brazowski, B., Chiprut, N., Bitterman, Y., Kvochko, A., Berkowitz, A., Shalem, D., Lifschitz,
D., Moshe, D., Porat, E., Richardson, E., Shiran, G., Chachy, I., Chetboun, J., Finkelson, M., Kupchick, M.,
Zabari, N., Guetta, N., Kotler, N., Bibi, O., Gordon, O., Panet, P., Benita, R., Armon, S., Kulikov, V., Inger,
Y., Shiftan, Y., Melumian, Z., and Farbman, Z. Ltx-2: Efficient joint audio-visual foundation model, 2026.
[URL https://arxiv.org/abs/2601.03233.](https://arxiv.org/abs/2601.03233) Submitted 6 Jan 2026.


Hafting, T., Fyhn, M., Molden, S., Moser, M.-B., and Moser, E. I. Microstructure of a spatial map in the
entorhinal cortex. _Nature_, 436(7052):801–806, 2005. doi: 10.1038/nature03721.


Hassabis, D. and Maguire, E. A. The construction system of the brain. _Philosophical Transactions of the_
_Royal Society B: Biological Sciences_, 364(1521):1263–1271, 2009.


He, X., Fan, Z., Li, H., Zhuo, F., Xu, H., Cheng, S., Weng, D., Liu, H., Ye, C., and Wu, B. RULER-bench: Probing rule-based reasoning abilities of next-level video generation models for vision foundation intelligence.
_arXiv preprint arXiv:2512.02622_, 2025. [URL https://arxiv.org/abs/2512.02622.](https://arxiv.org/abs/2512.02622)


Hegarty, M., Montello, D. R., Richardson, A. E., Ishikawa, T., and Lovelace, K. Spatial abilities at different
scales: Individual differences in aptitude-test performance and spatial-layout learning. _Intelligence_, 34(2):
151–176, 2006. doi: 10.1016/j.intell.2005.09.005.


16


[VIDEO-REASON.COM](https://video-reason.com) _A Very Big Video Reasoning Suite_


Helie, S. and Sun, R.´ Creative problem solving: A CLARION theory. In _2010 International Joint Conference_
_on Neural Networks (IJCNN)_, pp. 1460–1466, Barcelona, Spain, 2010. IEEE. doi: 10.1109/IJCNN.2010.
5596891. [URL https://doi.org/10.1109/IJCNN.2010.5596891.](https://doi.org/10.1109/IJCNN.2010.5596891)


Helmholtz, H. v. _Treatise on physiological optics, 3 vols._ Optical Society of America, 1924.


Ho, J., Jain, A., and Abbeel, P. Denoising diffusion probabilistic models. In _Advances in Neural Information_
_Processing Systems (NeurIPS)_, volume 33, pp. 6840–6851, 2020.


Holyoak, K. J. Analogy and relational reasoning. In Holyoak, K. J. and Morrison, R. G. (eds.), _The Oxford_
_Handbook of Thinking and Reasoning_, pp. 234–259. Oxford University Press, 2012.


Holyoak, K. J., Gentner, D., and Kokinov, B. N. Introduction: The place of analogy in cognition. In Gentner,
D., Holyoak, K. J., and Kokinov, B. N. (eds.), _The Analogical Mind:_ _Perspectives from Cognitive Science_,
pp. 1–19. MIT Press, 2001.


Hubel, D. H. and Wiesel, T. N. Receptive fields, binocular interaction and functional architecture in the cat’s
visual cortex. _The Journal of Physiology_, 160:106–154, 1962.


Hubel, D. H. and Wiesel, T. N. Receptive fields and functional architecture of monkey striate cortex. _The_
_Journal of Physiology_, 195(1):215–243, 1968.


Hubel, D. H. and Wiesel, T. N. Ferrier lecture: Functional architecture of macaque monkey visual cortex.
_Proceedings of the Royal Society of London. Series B, Biological Sciences_, 198(1130):1–59, 1977.


Kant, I. _Critique of Pure Reason_ . Cambridge University Press, Cambridge, 1781. The Cambridge Edition of
the Works of Immanuel Kant.


Kanwisher, N. Functional specificity in the human brain: A window into the functional architecture of the
mind. _Proceedings of the National Academy of Sciences_, 107(25):11163–11170, 2010. doi: 10.1073/pnas.
1005062107.


Kanwisher, N., McDermott, J., and Chun, M. M. The fusiform face area: A module in human extrastriate
cortex specialized for face perception. _Journal of Neuroscience_, 17(11):4302–4311, 1997. doi: 10.1523/
JNEUROSCI.17-11-04302.1997.


Kazemian, A., Elmoznino, E., and Bonner, M. F. Convolutional architectures are cortex-aligned de novo.
_Nature Machine Intelligence_, 2025. doi: 10.1038/s42256-025-01142-3.


Keil, F. C. _Concepts, kinds, and cognitive development_ . mit Press, 1992.


Keller, G. B. and Mrsic-Flogel, T. D. Predictive processing: A canonical cortical computation. _Neuron_, 100
(2):424–435, 2018. doi: 10.1016/j.neuron.2018.10.003.


Kersten, D., Mamassian, P., and Yuille, A. Object perception as bayesian inference. _Annual_ _Review_ _of_
_Psychology_, 55:271–304, 2004. doi: 10.1146/annurev.psych.55.090902.142005.


Kong, W., Tian, Q., Zhang, Z., Min, R., Dai, Z., Zhou, J., Xiong, J., Li, X., Wu, B., Zhang, J., et al. HunyuanVideo: A systematic framework for large video generative models. _arXiv preprint arXiv:2412.03603_,
2024.


Kosslyn, S. M. _Image and Mind_ . Harvard University Press, Cambridge, MA, 1980.


Kosslyn, S. M. _Image and brain:_ _The resolution of the imagery debate_ . MIT press, 1996.


Kriegeskorte, N. Deep neural networks: A new framework for modeling biological vision and brain information
processing. _Annual Review of Vision Science_, 1:417–446, 2015.


17


[VIDEO-REASON.COM](https://video-reason.com) _A Very Big Video Reasoning Suite_


Kuaishou Technology. Kling AI launches video 2.6 model with “simultaneous audio-visual generation”
capability, redefining AI video creation workflow. Press Release, December 2025. Model released
December 3, 2025. Press release published December 5, 2025.


Kumaran, D., Hassabis, D., Spiers, H. J., Vann, S. D., Vargha-Khadem, F., and Maguire, E. A. Impaired spatial
and non-spatial configural learning in patients with hippocampal pathology. _Neuropsychologia_, 45(12):
2699–2711, 2007.


Kumaran, D., Summerfield, J. J., Hassabis, D., and Maguire, E. A. Tracking the emergence of conceptual
knowledge during human decision making. _Neuron_, 63(6):889–901, 2009.


Kording, K. P., Beierholm, U., Ma, W. J., Quartz, S., Tenenbaum, J. B., and Shams, L.¨ Causal inference in
multisensory perception. _PLoS ONE_, 2(9):e943, 2007. doi: 10.1371/journal.pone.0000943.


Laird, J. E., Rosenbloom, P. S., and Newell, A. Soar: An architecture for general intelligence. _Artificial_
_Intelligence_, 33(1):1–64, 1987. doi: 10.1016/0004-3702(87)90050-6. [URL https://doi.org/10.](https://doi.org/10.1016/0004-3702(87)90050-6)
[1016/0004-3702(87)90050-6.](https://doi.org/10.1016/0004-3702(87)90050-6)


Langley, P., Laird, J. E., and Rogers, S. Cognitive architectures: Research issues and challenges. _Cognitive_
_Systems Research_, 10(2):141–160, 2009. doi: 10.1016/j.cogsys.2006.07.004. [URL https://doi.org/](https://doi.org/10.1016/j.cogsys.2006.07.004)
[10.1016/j.cogsys.2006.07.004.](https://doi.org/10.1016/j.cogsys.2006.07.004)


LeCun, Y., Bengio, Y., and Hinton, G. Deep learning. _Nature_, 521(7553):436–444, 2015.


Li, H., Chrysanthidis, N., Brincat, S. L., Rose, J., and Miller, E. K. Neural subspace reorganization reflects
value-based decision making. _bioRxiv_, pp. 2026–02, 2026.


Li, Y., Gao, Q., Zhao, T., Wang, B., Sun, H., Lyu, H., Hawkins, R. D., Vasconcelos, N., Golan, T., Luo,
D., and Deng, H. Core knowledge deficits in multi-modal language models. 2025. URL [https:](https://arxiv.org/abs/2410.10855)
[//arxiv.org/abs/2410.10855.](https://arxiv.org/abs/2410.10855)


Liu, X., Xu, Z., Li, M., Wang, K., Lee, Y. J., and Shang, Y. Can world simulators reason? Gen-ViRe: A
generative visual reasoning benchmark. _arXiv preprint arXiv:2511.13853_, 2025. [URL https://arxiv.](https://arxiv.org/abs/2511.13853)
[org/abs/2511.13853.](https://arxiv.org/abs/2511.13853)


Longuenesse, B. _Kant and the Capacity to Judge:_ _Sensibility and Discursivity in the Transcendental Analytic_
_of the Critique of Pure Reason_ . Princeton University Press, Princeton, 1998.


Luo, D., Li, Y., and Deng, H. The philosophical foundations of growing ai like a child. _arXiv_ _preprint_
_arXiv:2502.10742_, 2025a.


Luo, D., Wang, M., Wang, B., Zhao, T., Li, Y., and Deng, H. Machine psychophysics: Cognitive control in
vision-language models. _arXiv preprint arXiv:2505.18969_, 2025b.


Luo, Y., Zhao, X., Lin, B., Zhu, L., Tang, L., Liu, Y., Chen, Y.-C., Qian, S., Wang, X., and You, Y. Vreasonbench: Toward unified reasoning benchmark suite for video generation models. _arXiv_ _preprint_
_arXiv:2511.16668_, 2025c. [URL https://arxiv.org/abs/2511.16668.](https://arxiv.org/abs/2511.16668)


Ma, W. J., Beck, J. M., Latham, P. E., and Pouget, A. Bayesian inference with probabilistic population codes.
_Nature Neuroscience_, 9:1432–1438, 2006. doi: 10.1038/nn1790.


Marr, D. _Vision:_ _A Computational Investigation into the Human Representation and Processing of Visual_
_Information_ . W.H. Freeman, San Francisco, 1982.


Martin, C. B. and Barense, M. D. Perception and memory in the ventral visual stream and medial temporal
lobe. _Annual review of vision science_, 9(1):409–434, 2023.


18


[VIDEO-REASON.COM](https://video-reason.com) _A Very Big Video Reasoning Suite_


McClelland, J. L., McNaughton, B. L., and Lampinen, A. K. Integration of new information in memory:
New insights from a complementary learning systems perspective. _Philosophical Transactions of the Royal_
_Society B_, 375(1799):20190637, 2020.


McCorduck, P. _Machines_ _Who_ _Think:_ _A_ _Personal_ _Inquiry_ _into_ _the_ _History_ _and_ _Prospects_ _of_ _Artificial_
_Intelligence_ . A K Peters/CRC Press, 2 edition, 2004. ISBN 9781568812052. doi: 10.1201/9780429258985.


Milner, A. D. and Goodale, M. A. Two visual systems re-viewed. _Neuropsychologia_, 46(3):774–785, 2008.


Mitchell, M. Artificial intelligence learns to reason, 2025.


Moser, E. I. and Moser, M.-B. Grid cells and cortical representation. _Nature_ _Reviews_ _Neuroscience_, 15:
466–481, 2014. doi: 10.1038/nrn3766.


Newell, A. You can’t play 20 questions with nature and win: Projective comments on the papers of this
symposium. In Chase, W. G. (ed.), _Visual Information Processing_, pp. 283–308. Academic Press, New
York, NY, 1973. ISBN 9780121701505. doi: 10.1016/B978-0-12-170150-5.50012-3. [URL https://](https://linkinghub.elsevier.com/retrieve/pii/B9780121701505500123)
[linkinghub.elsevier.com/retrieve/pii/B9780121701505500123.](https://linkinghub.elsevier.com/retrieve/pii/B9780121701505500123) Proceedings of the
Eighth Annual Carnegie Symposium on Cognition, Carnegie-Mellon University, Pittsburgh, Pennsylvania,
May 19, 1972.


Newell, A. and Simon, H. A. The logic theory machine – a complex information processing system. _IRE_
_Transactions on Information Theory_, 2(3):61–79, 1956.


Newell, A. and Simon, H. A. _Human Problem Solving_ . Prentice-Hall, Englewood Cliffs, NJ, 1972. ISBN
0134454030.


Newell, A., Shaw, J. C., and Simon, H. A. Report on a general problem solving program. In _IFIP congress_,
volume 256, pp. 1959. Pittsburgh, PA, 1959.


Nobel Prize Committee. The Nobel prize in physiology or medicine 2014. [https://www.nobelprize.](https://www.nobelprize.org/prizes/medicine/2014/summary/)
[org/prizes/medicine/2014/summary/, 2014.](https://www.nobelprize.org/prizes/medicine/2014/summary/) Awarded to John O’Keefe, May-Britt Moser and
Edvard I. Moser.


O’Keefe, J. and Dostrovsky, J. The hippocampus as a spatial map: Preliminary evidence from unit activity in
the freely-moving rat. _Brain Research_, 34(1):171–175, 1971. doi: 10.1016/0006-8993(71)90358-1.


Olshausen, B. A. and Field, D. J. Emergence of simple-cell receptive field properties by learning a sparse code
for natural images. _Nature_, 381:607–609, 1996.


OpenAI. Sora: Openai’s text-to-video model. [https://openai.com/index/sora-is-here, 2025.](https://openai.com/index/sora-is-here)
publicly released September 2025.


Palmeri, T. J., Love, B. C., and Turner, B. M. Model-based cognitive neuroscience. _Journal of Mathematical_
_Psychology_, 76(Pt B):59–64, February 2017. doi: 10.1016/j.jmp.2016.10.010.


Papadopoulos, A., Sforazzini, F., Egan, G., and Jamadar, S. Functional subdivisions within the human
intraparietal sulcus are involved in visuospatial transformation in a non-context-dependent manner. _Human_
_brain mapping_, 39(1):354–368, 2018.


Passingham, R. E. and Lau, H. Do we understand the prefrontal cortex? _Brain Structure and Function_, 228(5):
1095–1105, 2023.


Peebles, W. and Xie, S. Scalable diffusion models with transformers. In _Proceedings_ _of_ _the_ _IEEE/CVF_
_International Conference on Computer Vision (ICCV)_, pp. 4195–4205, 2023.


Peng, W., Wang, G., Yang, T., Li, C., Xu, X., He, H., and Zhang, K. SVBench: Evaluation of video generation
models on social reasoning. _arXiv preprint arXiv:2512.21507_, 2025.


19


[VIDEO-REASON.COM](https://video-reason.com) _A Very Big Video Reasoning Suite_


Petersen, S. E. and Sporns, O. Brain networks and cognitive architectures. _Neuron_, 88(1):207–219, Oct 2015.
doi: 10.1016/j.neuron.2015.09.027.


Plato. _Theaetetus_, volume 12. Harvard University Press, Cambridge, MA, 1921. Loeb Classical Library.
Original work published ca. 369 BCE.


Polyak, A., Zohar, A., Brown, A., Tjandra, A., Sinha, A., Lee, A., Vyas, A., Shi, B., Ma, C., Chuang, C., et al.
MovieGen: A cast of media foundation models. _arXiv preprint arXiv:2410.13720_, 2024.


Quian Quiroga, R., Boscaglia, M., Jonas, J., Rey, H. G., Yan, X., Maillard, L., Colnat-Coulbois, S., Koessler,
L., and Rossion, B. Single neuron responses underlying face recognition in the human midfusiform
face-selective cortex. _Nature Communications_, 14(1):5661, 2023.


Ramnani, N. and Owen, A. M. Anterior prefrontal cortex: Insights into function from anatomy and neuroimaging. _Nature Reviews Neuroscience_, 5(3):184–194, 2004.


Rao, R. P. N. and Ballard, D. H. Predictive coding in the visual cortex: A functional interpretation of some
extra-classical receptive-field effects. _Nature Neuroscience_, 2(1):79–87, 1999. doi: 10.1038/4580.


Rapaport, W. J. Has ai succeeded? 2026.


Renero, A. Nous and aisthesis:¯ Two cognitive faculties in aristotle. _Methexis´_, 26(1):103–120, 2013. doi:
10.1163/24680974-90000616.


Runway Research. Introducing runway gen-4: Next-generation ai models for media generation and
world consistency. Runway Research, March 2025. URL [https://runwayml.com/research/](https://runwayml.com/research/introducing-runway-gen-4)
[introducing-runway-gen-4.](https://runwayml.com/research/introducing-runway-gen-4) Accessed January 27, 2026.


Russell, S. J. and Norvig, P. _Artificial Intelligence:_ _A Modern Approach_ . Pearson, Hoboken, 4th edition, 2021.
ISBN 9780134610993.


Shams, L. and Beierholm, U. R. Causal inference in perception. _Trends in Cognitive Sciences_, 14(9):425–432,
2010.


Shepard, R. N. and Metzler, J. Mental rotation of three-dimensional objects. _Science_, 171(3972):701–703,
1971. doi: 10.1126/science.171.3972.701.


Shields, C. _Aristotle:_ _De Anima_ . Oxford University Press, 2016.


Spelke, E. S. Core knowledge. _American Psychologist_, 55(11):1233–1243, 2000. doi: 10.1037/0003-066X.55.
11.1233.


Spelke, E. S. and Kinzler, K. D. Core knowledge. _Developmental_ _Science_, 10(1):89–96, 2007. doi:
10.1111/j.1467-7687.2007.00569.x.


Sporns, O., Tononi, G., and Kotter, R.¨ The human connectome: A structural description of the human brain.
_PLoS Computational Biology_, 1(4):e42, 2005. doi: 10.1371/journal.pcbi.0010042.


Stein, B. E. and Stanford, T. R. Multisensory integration: Current issues from the perspective of the single
neuron. _Nature Reviews Neuroscience_, 9:255–266, 2008. doi: 10.1038/nrn2331.


Swanson, L. R. The predictive processing paradigm has roots in kant. _Frontiers in Systems Neuroscience_, 10:
79, 2016. doi: 10.3389/fnsys.2016.00079.


Tanaka, K. Inferotemporal cortex and object vision. _Annual Review of Neuroscience_, 19:109–139, 1996.


Tolman, E. C. Cognitive maps in rats and men. _Psychological Review_, 55(4):189–208, 1948. doi: 10.1037/
h0061626.


20


[VIDEO-REASON.COM](https://video-reason.com) _A Very Big Video Reasoning Suite_


Tomov, M. S., Yagati, S., Kumar, A., Yang, W., and Gershman, S. J. Discovery of hierarchical representations
for efficient planning. _PLoS Computational Biology_, 16(4):e1007594, 2020.


Tong, J., Mou, Y., Li, H., Li, M., Yang, Y., Zhang, M., Chen, Q., et al. Thinking with video: Video generation
as a promising multimodal reasoning paradigm. _arXiv preprint arXiv:2511.04570_, 2025.


Treisman, A. M. and Gelade, G. A feature-integration theory of attention. _Cognitive_ _Psychology_, 12(1):
97–136, 1980.


Tsao, D. Y., Freiwald, W. A., Tootell, R. B. H., and Livingstone, M. S. A cortical region consisting entirely of
face-selective cells. _Science_, 311(5761):670–674, 2006. doi: 10.1126/science.1119983.


Tse, D., Takeuchi, T., Kakeyama, M., Kajii, Y., Okuno, H., Tohyama, C., Bito, H., and Morris, R. G. M.
Schema-dependent gene activation and memory encoding in neocortex. _Science_, 333(6044):891–895, 2011.


Vaidya, A. R. and Badre, D. Abstract task representations for inference and control. _Trends_ _in_ _cognitive_
_sciences_, 26(6):484–498, 2022.


von Helmholtz, H. _Handbuch der physiologischen Optik_ . L. Voss, Leipzig, 1867.


WanTeam. Wan: Open and advanced large-scale video generative models. _arXiv preprint arXiv:2503.20314_,
2025. [URL https://arxiv.org/abs/2503.20314.](https://arxiv.org/abs/2503.20314)


Wedin, M. V. _Mind and Imagination in Aristotle_ . Yale University Press, New Haven, 1988.


Wernicke, C. _Der aphasische Symptomencomplex:_ _Eine psychologische Studie auf anatomischer Basis_ . Max
Cohn und Weigert, Breslau, 1874. English translation: The Symptom Complex of Aphasia.


Whitehead, A. N. and Russell, B. _Principia mathematica_, volume 2. The University Press, 1927.


Whittington, J. C., Dorrell, W., Behrens, T. E., Ganguli, S., and El-Gaby, M. A tale of two algorithms:
Structured slots explain prefrontal sequence memory and are unified with hippocampal cognitive maps.
_Neuron_, 113(2):321–333, 2025.


Whittington, J. C. R., Muller, T. H., Mark, S., Chen, G., Barry, C., Burgess, N., and Behrens, T. E. J.
The Tolman-Eichenbaum machine: Unifying space and relational memory through generalization in the
hippocampal formation. _Cell_, 183(5):1249–1263, 2020. doi: 10.1016/j.cell.2020.10.024.


Wiedemer, T., Li, Y., Vicol, P., Gu, S. S., Matarese, N., Swersky, K., Kim, B., Jaini, P., and Geirhos,
R. Video models are zero-shot learners and reasoners. _arXiv_ _preprint_ _arXiv:2509.20328_, 2025. URL
[https://arxiv.org/abs/2509.20328.](https://arxiv.org/abs/2509.20328)


Xiao, Z., Wang, X., Zhang, J., Ou, J., He, L., Qu, Y., Hu, X., Behrens, T. E., and Liu, Y. Human hippocampal
ripples align new experiences with a grid-like schema. _Neuron_, 113(21):3661–3672, 2025.


Yamakawa, H. The whole brain architecture approach: Accelerating the development of artificial general intelligence by referring to the brain. _Neural_ _Networks_, 144:478–495, 2021. doi: 10.1016/
j.neunet.2021.09.004. URL [https://www.sciencedirect.com/science/article/pii/](https://www.sciencedirect.com/science/article/pii/S0893608021003543)
[S0893608021003543.](https://www.sciencedirect.com/science/article/pii/S0893608021003543)


Yamins, D. L. K., Hong, H., Cadieu, C. F., Solomon, E. A., Seibert, D., and DiCarlo, J. J. Performanceoptimized hierarchical models predict neural responses in higher visual cortex. _Proceedings of the National_
_Academy of Sciences_, 111(23):8619–8624, 2014.


Yang, C., Wan, H., Peng, Y., Cheng, X., Yu, Z., Zhang, J., Yu, J., Yu, X., Zheng, X., Zhou, D., and Wu, C.
Reasoning via video: The first evaluation of video models’ reasoning abilities through maze-solving tasks.
_arXiv preprint arXiv:2511.15065_, 2025a. [URL https://arxiv.org/abs/2511.15065.](https://arxiv.org/abs/2511.15065)


21


[VIDEO-REASON.COM](https://video-reason.com) _A Very Big Video Reasoning Suite_


Yang, J., Yang, S., Gupta, A. W., Han, R., Fei-Fei, L., and Xie, S. Thinking in space: How multimodal large
language models see, remember, and recall spaces. In _Proceedings of the Computer Vision and Pattern_
_Recognition Conference_, pp. 10632–10643, 2025b.


Yang, Z., Teng, J., Zheng, W., Ding, M., Huang, S., Xu, J., Yang, Y., Hong, W., Zhang, X., Feng, G., et al.
CogVideoX: Text-to-video diffusion models with an expert transformer. _arXiv preprint arXiv:2408.06072_,
2024.


Zacks, J. M. Neuroimaging studies of mental rotation: A meta-analysis and review. _Journal of Cognitive_
_Neuroscience_, 20(1):1–19, 2008.


Zheng, Z., Peng, X., Yang, T., Shen, C., Li, S., Liu, H., Zhou, Y., Li, T., and You, Y. Open-SORA:
Democratizing efficient video production for all. _arXiv preprint arXiv:2412.20404_, 2024.


22


[VIDEO-REASON.COM](https://video-reason.com) _A Very Big Video Reasoning Suite_


**A. Details of Cognitive Architecture**


Does intelligence have a structure? Such discussion could date back to Aristotle, where cognition is treated
not as a flat “inner theater”, i.e. in his mentor (Plato 1921, _Theaetetus_ 189e–190a), but as an organization of
_dunameis_, in other words, cognitive faculties. Knowing begins with _aisthesisˆ_, perception, where the senses
receive the form of external things without their matter, i.e. seeing “redness,” not absorbing the red object
(Aristotle 1984f;g, _De Anima_ 2.1, 412a19–23; 2.12, 424a17–24). The perceived then gets filtered through
_koine aist¯_ _hesis_ _[ˆ]_, in other words, common sense, where our judgments are supplied by core knowledge born
with us, such as spatiality, intuitive physics, and logic thoughts (Carey & Spelke 1996; Carey 2009; Luo et al.
2025a; Li et al. 2025; Aristotle 1984g, _De Anima_ 3.1, 425a27–b11). _Phantasia_ serves as the substrate that
preserves, recombines, organizes and transforms the perceptual _empeiria_, experiences, and stores them into
_mnem¯_ _e¯_, memory (Aristotle 1984a;g, _De Anima_ 3.3, 427b14–428a9, _On Memory_, 449b3–453b11). Above
_empeiria_ and _mnem¯_ _e¯_ lies the _nousˆ_, the uniquely human faculty of understanding and abstraction, and from
_empeiria_, _nousˆ_ extracts _katholou_, universals, an arc that Aritsole foregrounds as he traces from _aisthesisˆ_,
_phantasia_, _empeiria_, _mnem¯_ _e¯_ to _nousˆ_ . Essentially, the path to _katholou_, for Aristole, is the path to knowledge
and intelligent human behaviors, and therefore such is the flow of Aristotle’s cognitive architecture (Aristotle,
1984b, _Metaphysics_ 1.1, 980a21–27).


German Idealism is another undertaking where human thinkers try to theorize the structure of our cognition
and mind. Kant posits that the mind does not simply mirror the but actively structures the world that we
perceive as it’s (Kant 1781, _CPR_, A19–A24/B33–B38; A30–A33/B45–B49). He holds that raw sensory input
can only become meaningful when organized by the mind’s built-in frameworks – _sinnlichkeit_, a priori forms
of intuition, i.e. space and time, and _verstand_, categories of understanding, which include understanding of
numbers, of quality, modality, of causality, and of relations (Kant 1781, _CPR_, A50–A51/B74–B75; A80/B106).
Between _sinnlichkeit_ and _verstand_ lies _einbildungskraft_, where structured perceptual mental content would be
sent to for transformation and synthesis. Kant gives particular descriptions of such transformation of mental
content: _sinnlichkeit_ first organizes the spatiotemporal shape of representations, ordering raw data as a unified
intuition in space and time, and _einbildungskraft_ brings together intuitions so that they can be combined, and
finally _verstand_ recognizes the unified data by subsuming it under a category (Kant 1781, _CPR_, A98–A110).
At the apex lies _vernunft_, which offers the ultimate abstraction of mental representations, and generate ideas
such as the soul, the self as a whole, the world, the universe as a totality, and God (Allison 2004; Longuenesse
1998; Guyer 1987; Kant 1781, _CPR_, A327/B384; A642/B670; A249–A252).


Modern discussions on cognitive architecture usually combine with research in artificial intelligence and
cognitive neuroscience. At the Dartmouth Workshop in 1956, where the term ”artificial intelligence” is
coined, Herbert Simon and Alan Newell has presented Logical Theorist, a computer program which they
had claimed to be the “the first artificial intelligence program” (Newell & Simon, 1956; McCorduck, 2004).
While Logical Theorist is narrow and could only prove 38 of the first 52 theorems in Russell’s philosophy
textbook, it sparks the first AI boom where people try to build principled computer programs that would
produce human-like intelligent behaviors (Whitehead & Russell, 1927; Russell & Norvig, 2021). The General
Problem Solver has shown that human reasoning could be simulated using symbolic production systems,
establishing a computational account of problem solving, while critiques argue such is only a subset of what
human intelligence could do (Newell et al., 1959; Newell & Simon, 1972; Newell, 1973). Full-scale cognitive
architecture models soon have flourished, including ACT-R, SOAR, and CLARION models (Anderson, 2013;
Laird et al., 1987; Anderson & Lebiere, 1998; Anderson, 1993; 2007; Langley et al., 2009; Helie´ & Sun,
2010).


As techniques in neuroscience have developed, a dialogue has emerged between cognitive architectures
and brain architectures (Petersen & Sporns, 2015). Human brain is interestingly modular, with cognitive
functions specifically implemented in particular physical anatomical locations, yet these specialized regions
communicate constantly to orchestrate cognition (d’anthropologie de Paris, 1898; Wernicke, 1874; Kanwisher,
2010). Recently, cognitive neuroscientists hope to map out the structural and functional connectivity between
brain areas as to understand the architectural organization underlying cognition (Sporns et al., 2005; Bertolero
et al., 2015). Explicit combinations of the cognitive architecture approaches and connectomics approaches have


23


[VIDEO-REASON.COM](https://video-reason.com) _A Very Big Video Reasoning Suite_


been carried out in research in recent years and yielded validations of some of the hypothesized architectural
claims about human cognition in the human brain (Palmeri et al., 2017; Yamakawa, 2021; Chakladar, 2024).


Sitting on the shoulder of philosophy giants and combining works from cognitive architecture modeling and
neuroscience, we have consolidated a cognitive architecture made of **perception**, **transformation**, **spatiality**,
**abstraction**, and **knowledge** .


**A.1. Perception**


Perception is the the extraction of form without matter (Aristotle, 1984g, _De_ _Anima_ 2.12, 424a17–24).
Helmholtz calls this as ”unconscious inference” (von Helmholtz, 1867; Helmholtz, 1924). The visual system
exemplifies perception’s hierarchical architecture. V1 neurons function as oriented edge detectors organized
into columnar structures reflecting natural image statistics (Hubel & Wiesel, 1962; 1968; Bonhoeffer &
Grinvald, 1991; Hubel & Wiesel, 1977; Olshausen & Field, 1996). Beyond V1, the ventral and dorsal
streams achieve progressively invariant object recognition (Milner & Goodale, 2008; Goodale & Milner, 1992;
DiCarlo et al., 2012; Tanaka, 1996), with category-selective regions like the fusiform face area emerging in
inferotemporal cortex (Kanwisher et al., 1997; Tsao et al., 2006; Quian Quiroga et al., 2023), where cells
collectively map a low-dimensional ”object space” (Bao et al., 2020). Just as Kant has hypothesized (Swanson,
2016), the brain generates predictions about sensory input and computes prediction errors, with representational
geometry shaped by environmental regularities (Rao & Ballard, 1999; Friston, 2010; Keller & Mrsic-Flogel,
2018; Greco et al., 2024; Kersten et al., 2004; Ma et al., 2006). Multimodal integration binds signals across
modalities through causal inference in regions like superior temporal cortex (Ghazanfar & Schroeder, 2006;
Stein & Stanford, 2008; Calvert, 2001; Kording et al.¨, 2007; Shams & Beierholm, 2010). Marr’s tri-level
framework connects biological and artificial vision (Marr, 1982): CNNs exhibit cortex-aligned representations,
though they lack robust higher-level processing found in biological systems (Yamins et al., 2014; Kriegeskorte,
2015; Kazemian et al., 2025; Baker et al., 2018; Geirhos et al., 2021). Gibson’s ecological approach reminds
us that perception ultimately serves action through affordances (Gibson, 2014)—connecting to Aristotle’s view
that _aisthesisˆ_ serves the organism’s engagement with its environment. Perception constitutes the entry point of
human cognitive architecture, a thesis from Marr and Gibson to modern deep learning (Gibson, 2014; Marr,
1982; Yamins et al., 2014; Kriegeskorte, 2015; Kazemian et al., 2025; Baker et al., 2018; Geirhos et al., 2021).


**A.2. Transformation**


Transformation refers to the cognitive faculty that manipulates, recombines, and synthesizes mental representations, corresponding to Aristotle’s _phantasia_ and Kant’s _Einbildungskraft_ . Aristotle insists that “whenever one
contemplates, one necessarily at the same time contemplates in images,” positioning _phantasia_ not as passive
storage but as active transformation of _empeiria_ into material suitable for _nousˆ_ (Aristotle 1984g, _De Anima_
3.7, 431a16–17; Wedin 1988). Kant systematizes this through his three syntheses, apprehension gathering the
sensory manifold, reproduction in imagination holding representations together, and recognition subsuming
the unified manifold under categories, with _Einbildungskraft_ functioning productively to generate experiential
structure by binding intuitions according to _Verstand_ (Kant 1781, _CPR_, A98–A110; Longuenesse 1998; Allison
2004). Modern cognitive science operationalizes these insights: scientists have demonstrated that mental
rotation operates analogically on quasi-spatial representations, proposing that mental images are constructed in
a “visual buffer” for manipulation (Shepard & Metzler, 1971; Kosslyn, 1980; 1996). Another work has showed
that focused attention binds preattentively registered features into coherent objects, a process that breaks down
with parietal lesions, echoing Kant’s synthesis of apprehension (Kant 1781, _CPR_, A98–A110; Treisman &
Gelade, 1980). Neuroscience suggests the posterior parietal cortex, particularly the intraparietal sulcus, as
the substrate for transformation (Zacks, 2008; Papadopoulos et al., 2018), while cognitive architectures like
ACT-R formalize this through an imaginal module with parietal correlates (Anderson, 2007). Transformation
thus occupies the crucial intermediate position both Aristotle and Kant recognized: between raw _aisthesisˆ_ or
_Sinnlichkeit_ and the higher operations of _noˆus_ or _Vernunft_ .


24


[VIDEO-REASON.COM](https://video-reason.com) _A Very Big Video Reasoning Suite_


**A.3. Spatiality**


For Kant, space constitutes an _a priori_ form of _sinnlichkeit_ —a transcendental precondition for perception
itself, not something derived from experience (Kant 1781, _CPR_, A22–A24/B37–B40). This insight finds
support in developmental psychology identifying spatiality as a core knowledge system: infants possess
domain-specific machinery for representing places and their geometric relationships, with deep phylogenetic
roots observable across species and cultures (Spelke & Kinzler, 2007; Spelke, 2000). Tolman first proposed
that animals construct internal “cognitive maps” enabling flexible navigation beyond simple stimulus-response
associations (Tolman, 1948). The neural substrates were later revealed: _place cells_ in the hippocampus fire
at specific locations (O’Keefe & Dostrovsky, 1971), while _grid cells_ in the entorhinal cortex provide metric
coordinates through hexagonal firing patterns (Hafting et al., 2005), which are discoveries recognized by the
2014 Nobel Prize as “a positioning system in the brain” (Moser & Moser, 2014; Nobel Prize Committee, 2014).
The posterior parietal cortex complements this system by organizing sensory coordinates into motor-relevant
reference frames (Colby & Goldberg, 1999; Andersen et al., 1997). Beyond representation, humans perform
spatial operations such as mental rotation, where reaction times increase linearly with angular disparity
(Shepard & Metzler, 1971; Hegarty et al., 2006). Computational models that are grid-cell-inspired have been
proposed, but human-level performances remain challenging (Banino et al., 2018; Whittington et al., 2020;
Behrens et al., 2018). Spatiality serves as a fundamental function, a prerequisite for perception, scaffold for
memory, and substrate for reasoning in human cognitive architecture.


**A.4. Abstraction**


Abstraction represents the apex of our cognitive architecture, where embodied experiences are distilled into
generalizable knowledge. For Aristotle, _nousˆ_ extracts _katholou_, universals, from accumulated _empeiria_
through selective attention to essential features x(Aristotle, 1984b, _Metaphysics_ 1.1, 980a21–27; Renero, 2013;
Aristotle, 1984g, _De Anima_ 3.4–8; Shields, 2016). Kant’s _Vernunft_ similarly generates transcendental ideas
extending beyond the categories of _Verstand_, though exceeding the boundaries of possible experience (Kant,
1781, _CPR_, A327/B384; A642/B670; Allison, 2004; Guyer, 1987). Contemporary accounts elaborate these
mechanisms: one developmental psychology work demonstrates that abstract concepts emerge through Quinian
Bootstrapping, producing representational systems with greater expressive power than core cognition, with
concepts possessing causally deep “cores” (Carey, 2009; Carey, 2011; Carey, 2009; Keil, 1992). Gentner’s
structure-mapping theory shows how analogical reasoning maps relational patterns across domains, with
systematicity determining preferred mappings and enabling children to extract relational abstractions (Gentner,
1983; Gentner & Hoyos, 2017; Holyoak, 2012; Gentner, 1983; Gentner & Hoyos, 2017; Holyoak et al., 2001).
Neuroscience reveals abstraction’s hierarchical implementation: the lateral PFC exhibits a rostral-to-caudal
gradient whereby anterior regions process increasingly abstract information, with rostral PFC serving as a
“gateway” for internally-generated thought (Badre & Nee, 2018; Christoff et al., 2009; Badre & Nee, 2018;

Brincat et al., 2018; Burgess et al., 2007; Ramnani & Owen, 2004). Memory systems contribute through
schema-guided consolidation, with hippocampus and vmPFC maintaining abstract prototype representations
that support generalization (Bowman & Zeithamova, 2018; Gilboa & Marlatte, 2017; Tse et al., 2011;
McClelland et al., 2020). Hierarchical abstraction might underly deep learning’s layered representations and
cognitive architectures’ multiple processing levels (LeCun et al., 2015; Bengio et al., 2013; Anderson, 2007;
Laird et al., 1987; Tomov et al., 2020; Luo et al., 2025b). Abstraction integrates the outputs of perception,
transformation, and spatiality to achieve the _katholou_, knowledge, that Aristotle recognized as the _telos_ of
intelligent behavior (Aristotle, 1984d, _Posterior Analytics_ 2.19, 100a3–100b5).


**A.5. Knowledge**


Aristotle opens the _Metaphysics_ with the claim that “all human beings by nature desire to know” (Aristotle,
1984b, _Metaphysics_ 980a21), and devotes the closing chapter of the _Posterior Analytics_ to explaining how they
do so. Knowledge begins in _aisthesisˆ_, sense perception, which deposits _mnemˆ_ _eˆ_, memory; repeated memories
of the same kind consolidate into _empeiria_, experience; and from experience _nousˆ_ abstracts the universal
first principles that ground _epistemˆ_ _eˆ_, demonstrative knowledge (Aristotle, 1984d, _Posterior Analytics_ II.19,


25


[VIDEO-REASON.COM](https://video-reason.com) _A Very Big Video Reasoning Suite_


99b15–100b17). The progression is neither purely empirical nor purely rational: perception furnishes the
material, but it is the active intellect that grasps the universal in the particular, “as when a rout has occurred
in battle, first one soldier makes a stand, then another, until the original formation is restored” (Aristotle,
1984d, _Posterior Analytics_ 100a12–13). For Aristotle, then, human cognition is structured from the outset by
capacities that go beyond the sensory given, _nousˆ_ does not learn first principles from experience so much as
recognize them through it.


Kant radicalizes this insight. Whereas Aristotle allows that universals are latent in perception and extracted
by intellect, Kant argues that the mind actively constitutes the very form of experience. “Thoughts without
content are empty; intuitions without concepts are blind” (Kant, 1781, _CPR_ A51/B75): knowledge requires
both sensible _Anschauungen_ delivered by receptivity and the _Kategorien_ of _Verstand_ imposed by spontaneity.
The categories, substance, causality, unity, plurality, and the res, are not abstracted from experience but are
its _a priori_ conditions of possibility (Kant, 1781, _CPR_ A80/B106; Longuenesse, 1998). The transcendental
deduction establishes that these concepts must apply to any object of experience whatsoever, because it is
only through their application that the manifold of intuition is synthesized into coherent representation (Kant,
1781, _CPR_ B129–B169; Allison, 2004). Knowledge, for Kant, is thus never a passive reception but an active
structuring: the mind brings to experience the very framework within which experience becomes intelligible.


Contemporary developmental psychology has furnished striking empirical support for this rationalist inheritance. Research on core knowledge demonstrates that human infants possess, from the earliest months of
life, a set of domain-specific representational systems that structure cognition prior to and independently of
explicit instruction (Spelke & Kinzler, 2007). These representations are abstract, often amodal, and operate
according to principles that go well beyond what associative learning from perceptual statistics could deliver
(Baillargeon et al., 1985). Carey’s account of conceptual change further shows that later, explicit knowledge is
constructed not _ex nihilo_ but through the enrichment, combination, and bootstrapping of these core systems, a
process she terms Quinian bootstrapping (Carey, 2009).


**Figure 7** Distribution of 150 visual reasoning tasks across five cognitive faculties in the VBVR-Dataset.















**Table 6** Complete Cognitive Taxonomy of VBVR-Dataset (150 Visual Reasoning Tasks)


**Task ID** **Cognitive Category** **Description**


**ABSTRACTION (33)**
G-7 Abstraction Return objects to correct bin by category
G-26 Abstraction Maintain object identity across different objects
G-29 Abstraction Find extreme values in chart (with data labels)
G-37 Abstraction Identify random symmetry patterns
G-38 Abstraction Identify shape symmetry patterns
G-41 Abstraction Grid highest cost path finding
G-44 Abstraction Breadth-first search traversal
G-49 Abstraction Complete missing contour segments
G-51 Abstraction Predict next color in sequence
G-131 Abstraction Select next figure in increasing size sequence
G-133 Abstraction Select next figure in decreasing size sequence
G-134 Abstraction Select next figure in large-small alternating sequence
G-135 Abstraction Select next figure in small-large alternating sequence
G-193 Abstraction Draw next sized shape in pattern
O-7 Abstraction Shape color change operations
O-8 Abstraction Shape rotation operations


26



_Continued on next page_


[VIDEO-REASON.COM](https://video-reason.com) _A Very Big Video Reasoning Suite_


_Table 6 — continued from previous page_


**Task ID** **Cognitive Category** **Description**


O-9 Abstraction Shape scaling operations
O-10 Abstraction Shape outline fill operations
O-11 Abstraction Shape color then move (compound operation)
O-12 Abstraction Shape color then scale (compound operation)
O-13 Abstraction Shape outline then move (compound operation)
O-14 Abstraction Shape scale then outline (compound operation)
O-21 Abstraction Construction blueprint interpretation
O-29 Abstraction Ball color clustering and merging
O-30 Abstraction Bookshelf organization task
O-37 Abstraction Light sequence pattern recognition
O-43 Abstraction Object subtraction (quantity reasoning)
O-45 Abstraction Sequence completion task
O-47 Abstraction Sliding puzzle solving
O-49 Abstraction Symmetry completion task
O-54 Abstraction Control panel symbol manipulation
O-56 Abstraction Raven’s Progressive Matrices reasoning
O-66 Abstraction Animal color sorting task


**KNOWLEDGE (23)**
G-27 Knowledge Read chart data and semantic comprehension
G-30 Knowledge Find extreme values in chart (without data labels)
G-35 Knowledge Hit target after bounce
G-48 Knowledge Multiple bounces prediction
G-160 Knowledge Circle largest numerical value
G-162 Knowledge Locate twelve o’clock arrows
G-163 Knowledge Identify digits 1 and 9
G-200 Knowledge Circle maximum value in set
G-217 Knowledge Circle central dot
G-247 Knowledge Identify Chinese character
G-273 Knowledge High density liquid behavior
O-3 Knowledge Symbol reordering operations
O-15 Knowledge Ball bounces at given time
O-18 Knowledge Glass refraction
O-19 Knowledge Mirror reflection
O-23 Knowledge Domino chain branch path prediction
O-24 Knowledge Domino chain gap analysis
O-34 Knowledge Dot-to-dot connection task
O-52 Knowledge Traffic light state reasoning
O-53 Knowledge Clock reading and time reasoning
O-62 Knowledge Gravity physics simulation
O-75 Knowledge Communicating vessels (fluid dynamics)
O-87 Knowledge Fluid diffusion reasoning


**PERCEPTION (45)**
G-3 Perception Stable sort objects maintaining order
G-4 Perception Identify and distinguish different objects
G-5 Perception Multi-object placement to specified positions
G-9 Perception Identify objects in specified region
G-19 Perception Sort objects by specified rule
G-22 Perception Attention shift to same object
G-39 Perception Attention shift to different object
G-43 Perception Understand scene structure and spatial layout
G-54 Perception Connecting matching colors
G-132 Perception Find fragment for gap filling
G-136 Perception Locate point in overlapping area
G-137 Perception Identify figure in overlapping area
G-138 Perception Spot unique non-repeated color
G-141 Perception Identify polygon with most sides
G-143 Perception Select box with most dots
G-146 Perception Circle all squares from mixed shapes
G-147 Perception Identify unique figure in uniform set
G-158 Perception Identify all hollow points
G-161 Perception Mark second largest shape
G-165 Perception Mark tangent point after motion
G-166 Perception Highlight horizontal lines
G-167 Perception Select longest polygon side
G-168 Perception Identify rectangle nearest to square
G-169 Perception Locate intersection of line segments
G-174 Perception Arrange circles by circumference
G-189 Perception Draw midpoint perpendicular line
G-195 Perception Select nearest 2:1 rectangle
G-198 Perception Mark right-angled triangles
G-199 Perception Locate line intersections
G-202 Perception Mark wave peaks


_Continued on next page_


27


[VIDEO-REASON.COM](https://video-reason.com) _A Very Big Video Reasoning Suite_


_Table 6 — continued from previous page_


**Task ID** **Cognitive Category** **Description**


G-206 Perception Identify pentagons
G-212 Perception Find incorrect arrow direction
G-218 Perception Identify largest angle in triangle
G-222 Perception Mark tangent point of circles
G-223 Perception Highlight horizontal lines
G-248 Perception Mark asymmetrical shape
G-250 Perception Color triple intersection red
O-1 Perception Color mixing (additive)
O-2 Perception Pigment color mixing (subtractive)
O-16 Perception Color addition operations
O-17 Perception Color subtraction operations
O-31 Perception Ball eating mechanics
O-33 Perception Counting objects accurately
O-38 Perception Identify majority color in set
O-65 Perception Animal size sorting


**SPATIALITY (20)**
G-12 Spatiality Grid navigation to obtain reward
G-13 Spatiality Grid number sequence navigation
G-14 Spatiality Grid color sequence navigation
G-15 Spatiality Grid navigation avoiding obstacles
G-16 Spatiality Grid navigation going through blocks
G-17 Spatiality Grid navigation avoiding red blocks
G-18 Spatiality Grid shortest path finding
G-31 Spatiality Directed graph navigation
G-32 Spatiality Undirected graph navigation
G-33 Spatiality Visual Jenga game
G-45 Spatiality Key-door matching puzzle
G-46 Spatiality Find keys and open doors
G-47 Spatiality Multiple keys for one door puzzle
G-140 Spatiality Locate topmost unobscured figure
G-219 Spatiality Select leftmost shape
G-221 Spatiality Outline innermost square
O-25 Spatiality LEGO construction assembly
O-39 Spatiality Maze navigation and solving
O-55 Spatiality Rotation operations
O-83 Spatiality Planar warp verification


**TRANSFORMATION (29)**
G-1 Transformation Predict object trajectory
G-2 Transformation Reorder objects by rule
G-6 Transformation Resize object
G-8 Transformation Track object movement
G-11 Transformation Handle object reappearance after disappearance
G-21 Transformation Multiple occlusions (vertical)
G-24 Transformation Separate objects (no rotation)
G-25 Transformation Separate rotating objects
G-34 Transformation Object packing optimization
G-36 Transformation Multiple occlusions (horizontal)
G-40 Transformation Combined rotating objects
G-50 Transformation Suppress spurious edges
G-194 Transformation Construct concentric ring
G-240 Transformation Add borders to unbordered shapes
O-4 Transformation Symbol substitution operations
O-5 Transformation Symbol deletion operations
O-6 Transformation 2D geometric transformation
O-22 Transformation Construction stack (gravity balance)
O-27 Transformation Move 2 objects to 2 targets
O-32 Transformation Rolling ball physics
O-36 Transformation Grid shift operations
O-44 Transformation Rotation puzzle
O-46 Transformation Shape sorter classification
O-58 Transformation Symbol delete operations
O-59 Transformation Symbol insert operations
O-60 Transformation Symbol substitute operations
O-61 Transformation Symbol edit operations
O-64 Transformation Animal matching task
O-85 Transformation 2D object rotation


28


[VIDEO-REASON.COM](https://video-reason.com) _A Very Big Video Reasoning Suite_


**B. Data Curation**


This appendix provides a comprehensive account of the data curation pipeline that underlies the VBVR-Bench.
We detail the five-stage process from task design to benchmark construction, the quality assurance mechanisms,
and the infrastructure that enables large-scale data generation.


**B.1. Overview of Data Curation Pipeline**


The VBVR-Bench is built through a systematic five-stage pipeline that transforms cognitive task concepts into
a standardized evaluation framework.


**Pipeline Flow** . The data curation pipeline consists of five sequential stages. **Stage 1:** **Task Design** We begin
by designing cognitive reasoning tasks grounded in cognitive science principles. Starting from over 300 task
candidates, we employ a dual-review process to select tasks that meet six quality criteria. This stage produces
two distinct task sets: 100 training tasks and 100 testing tasks with an overlapping of 50 tasks. **Stage 2:** **Task**
**Implementation** Each training task is implemented as a parameterized generator capable of producing diverse
samples. These generators form the our data spring, VBVR-DataFactory, a set of modular synthesis engines.
All generators inherit from a standardized BaseGenerator template and are managed as independent
repositories within a GitHub Organization. Implementation undergoes rigorous quality control by dedicated
reviewers who verify scalability, code quality, and adherence to file specifications. **Stage 3:** **Large-Scale**
**Distributed** **Generation** . The VBVR-DataFactory infrastructure orchestrates parallel generation of one
million training samples (10,000 per task) stored privately on AWS S3. Simultaneously, we generate 500 fresh
test cases (5 per task) from the Test task set. Each sample comprises an initial frame, task prompt, ground-truth
solution, and reference video. **Stage 4:** **Model Evaluation** . We employ VBVR-EvalKit to evaluate eight
state-of-the-art image-to-video (I2V) models on the 500 test cases, producing 4,000 generated videos. Human
annotators assess each video across three reasoning-specific dimensions: Task Completion, Reasoning Logic,
and Visual Quality, each scored on a 1-5 scale. **Stage 5:** **Benchmark Construction and Model Training** .
The evaluation data is integrated into a standardized benchmark dataset. We train the VBVR-Wan on the one
million training samples, demonstrating that explicit reasoning supervision significantly improves performance
on reasoning-intensive tasks.


_**B.1.1. Key Statistics**_


Table 7 summarizes the scale and coverage of the VBVR benchmark:


**Table 7** Data Construction Statistics


**Component** **Scale** **Description**


Task Candidates 300+ Initial task pool
Training Tasks 100 Generate training data
Test Tasks 100 50 In-Domain + 50 Out-of-Distribution
Training Samples 1,000,000 100 tasks × 10,000 samples per task
Test Cases 7,500 150 tasks × 50 samples per task
Cognitive Categories 5 Systematic coverage
Evaluated Models 8 State-of-the-art I2V models, 4 open-source, 4 commercial
Generated Videos 4,000 8 models × 500 cases
Evaluation Records 4,000 Task Completion/Reasoning Logic/Visual Quality annotations
Development Team 75 53 OSS coders + 7 full-time employees + 5 QC reviewers
Code Repositories 300+ Github Organization


_**B.1.2. Design Principles**_


The pipeline is guided by the following core design principles: **1.** **Dual Generalization Testing** . The InDomain/OOD split enables evaluation of both in-task generalization (seen task types with unseen samples)
and cross-task generalization (unseen task types). **2.** **Reasoning-First Paradigm** . Unlike benchmarks that
primarily assess generation quality, VBVR emphasizes reasoning correctness through TC, RL, and VQ metrics
that capture task completion, logical consistency, and visual fidelity. **3.** **Industrial-Scale Quality Assurance**
We employ a dual-review mechanism: peer review for task design (by five task designers) and dedicated


29


[VIDEO-REASON.COM](https://video-reason.com) _A Very Big Video Reasoning Suite_


quality control for implementation (by more than two specialized reviewers). Six quality criteria ensure
tasks are well-specified, visually clear, and scalable. **4.** **Extensible Infrastructure** . The modular generator
architecture and comprehensive evaluation toolkit facilitate easy extension with new tasks and models. **5.**
**Cognitive Inspiration** . Our task design began with a loose cognitive taxonomy inspired by cognitive science
literature. However, rather than rigidly adhering to a fixed theoretical framework, we adopted a task-driven
design philosophy: we prioritized designing intellectually meaningful reasoning tasks first, then organized
them into our categories. **6.** **Diversity Focus** . This approach contrasts with top-down frameworks that first
define strict categories, then fill them with tasks. Our bottom-up approach ensured that each task possesses
genuine reasoning value, and maximizing our diversity, rather than forcing tasks to fit narrow pre-determined
boxes.


_**B.1.3. Task Selection and Filtering**_


**Initial Pool** We designed over 300 task candidates through iterative brainstorming sessions. Each designer
independently proposed tasks, which were then collectively discussed and refined.


**Selection Criteria (Six Standards)** Tasks were evaluated against six criteria during peer review:


1. **Information Sufficiency** : The first frame must contain all information necessary for reasoning, without
requiring external context.


✓ Pass Example: G-15 (Grid Avoid Obstacles) — the first frame shows start point, end point, and all
obstacles.
_×_ Fail Example: Tasks where the goal object is initially occluded or requires additional verbal
explanation.


2. **Deterministic Solution** : Tasks should have a clear, unique solution (or explicitly defined criteria for
multiple valid solutions, e.g., “shortest path”).


✓ Pass Example: G-18 (Grid Shortest Path) — the optimal path is unambiguous.

_×_ Fail Example: Open-ended tasks with ambiguous success conditions.


3. **Video-Based Reasoning** : Tasks must be suitable for video generation models, encompassing diverse
reasoning types (temporal dynamics, static recognition, logical inference).


✓ Pass Example: O-23 (Domino Chain) — requires temporal causality reasoning.


! Note: Unlike some benchmarks, we do NOT exclude static recognition tasks; we include both
dynamic and static reasoning.


4. **Visual Clarity** : Objects must be distinguishable, text/numbers legible, and layouts uncluttered to avoid
perceptual ambiguity.


5. **Parametric** **Diversity** **(Scalability)** : The parameter space must be large enough to generate 10,000
non-trivial, distinct samples per task.


6. **Technical Feasibility** : Tasks must be implementable with our rendering pipeline (PIL-based), output
standard file formats, and avoid edge cases (e.g., initial occlusions, boundary overflow).


**Rejection Cases** Here are some of the tasks were excluded:


  - **A. Multi-Step Logic Chains**


**–** Example: Logic Gate Circuits

**–** Reason: Reasoning chains too long to clearly visualize in video format.


  - **B. Complex Physics Requiring Precise Numerical Solutions**


30


[VIDEO-REASON.COM](https://video-reason.com) _A Very Big Video Reasoning Suite_


**–** Example: Elastic Collisions with friction coefficients

**–** Reason: Continuous parameters yield no deterministic solution (tiny parameter variations lead to
drastically different trajectories); I2V models cannot precisely simulate physics.


  - **C. Excessively Difficult Tasks**


**–** Example: Sudoku

**–** Reason: High difficulty even for humans; unsuitable for video format (better suited for static
reasoning); evaluation criteria too strict (any single cell error constitutes failure).


_**B.1.4. Peer Review Process**_


All task designs underwent a structured peer review by the five task designers, with each designer evaluating
others’ proposals using a standardized checklist derived from the six quality criteria; tasks typically progressed
through 2–3 rounds of iterative refinement based on this feedback, during which common issues were identified,
including **ambiguous success conditions**, **insufficient visual clarity**, **parameter spaces too small to support**
**10k samples**, and **unintentional edge cases** (e.g., objects overlapping at initialization). A task advanced to
implementation (Stage 2) only after receiving consensus approval from at least three reviewers. This process
ensured that every task in VBVR meets rigorous cognitive and technical standards, forming a solid foundation
for the subsequent implementation and evaluation stages.


**B.2. Details of Task Implementation**


This section details the implementation of the 200 tasks as parameterized generators. We describe the
standardized architecture, code management infrastructure, parameterization strategies, visual rendering
pipeline, and dedicated quality control procedures.


_**B.2.1. Generator Architecture and Standardization**_


**BaseGenerator Template** All task generators inherit from a standardized BaseGenerator abstract base
class, ensuring consistent interfaces and output formats. The template defines:


1. **Required Methods** :


     - ~~i~~ nit ~~(~~ self, seed, params): Initialize generator with random seed and task-specific
parameters.

     - generate ~~s~~ ample(self) -> Sample: Generate a single task instance.

     - validate ~~s~~ ample(self, sample) -> bool: Verify sample meets quality criteria.

     - save ~~s~~ ample(self, sample, output ~~d~~ ir): Save sample to standardized file structure.


2. **Standard Output Format** : Each sample is saved as a directory containing:


     - first ~~f~~ rame.png: Initial state image (required)

     - prompt.txt: Task instruction in natural language (required)

     - final ~~f~~ rame.png or goal.txt: Target state or goal description

     - ground ~~t~~ ruth.mp4: Reference solution video demonstrating the correct reasoning process


3. **Configuration Management** : Generators expose configurable parameters through a config.yaml
file specifying:


     - Parameter ranges (e.g., grid size: 5-10, number of objects: 3-8)

     - Difficulty levels (easy/medium/hard)

     - Visual settings (resolution: 512×512, frame rate: 24 fps)


31


[VIDEO-REASON.COM](https://video-reason.com) _A Very Big Video Reasoning Suite_


**Design Rationale** . The BaseGenerator template serves three core purposes: **Consistency**, by providing
uniform interfaces that simplify integration with VBVR-DataFactory for batch generation; **Quality Assurance**,
through the validate ~~s~~ ample() method, which enforces critical checks such as ensuring no object
occlusions and that valid solutions exist; and **Extensibility**, enabling new tasks to be added by implementing
the abstract methods while leveraging shared utility functions.


_**B.2.2. Code Management Infrastructure**_


All task generators are managed as independent repositories within a GitHub Organization, an architecture that provides clear organizational and operational advantages: each repository follows a strict
Naming Convention of _{_ Type _}_ - _{_ ID _}_ ~~_{_~~ task ~~n~~ ame _}_ ~~d~~ ata-generator (e.g., G-3 ~~s~~ table ~~s~~ ort ~~-~~
data-generator and O-15 ~~b~~ all bounces ~~g~~ iven ~~t~~ ime ~~d~~ ata-generator), where Type denotes
G, which are contributed by commercial enterprises, or O, which are contributed by OSS developers, and ID
is a unique numeric identifier; this structure enables Independent Versioning, as each task maintains its own
commit history, tags, and release cycles, and supports Modular Updates, ensuring that bug fixes or parameter
adjustments to one task do not affect others.


All generators share the core/ directory structure through Git submodules or package dependencies, ensuring
consistent utility functions while allowing each task to evolve independently. This design yields several
version control benefits: 1. Traceability, as each sample records the exact generator version (git commit
hash) used for generation; 2. Reproducibility, enabling researchers to check out specific generator versions to
reproduce sample generation; and 3. Collaboration, allowing multiple team members to work on different
tasks simultaneously without merge conflicts.


**Figure 8** This is a typical example of data samples in our dataset. The model receives a prompt and a first
image, and is asked to generate a video that solves the prompt. Final image and ground truth videos are
provided as references in data samples.







_**B.2.3. Parameterization Strategy for Diversity**_


To generate 10,000 distinct, non-trivial samples per task, we employ systematic parameterization strategies:


**Example 1:** **G-15 (Grid Avoid Obstacles)**


Parameters:

 - grid_size: [5, 6, 7, 8, 9, 10] # 6 options

 - num_obstacles: [3, 4, 5, ..., 15] # 13 options

 - start_position: grid-dependent # ˜grid_size² options

 - end_position: grid-dependent # ˜grid_size² options

 - obstacle_layout: random_valid # ˜10ˆ6 variations


Estimated unique samples: - 10ˆ9

Sampling strategy: Constrained random sampling ensuring solvability


**Example 2:** **O-56 (Raven’s Progressive Matrices)**


Parameters:

 - pattern_type: [size_progression, rotation, color_change,

shape_replacement, combination] # 5 types

 - num_objects: [1, 2, 3, ..., n] # n options

 - object_shapes: [circle, square, triangle, ...] # 8 shapes


32


[VIDEO-REASON.COM](https://video-reason.com) _A Very Big Video Reasoning Suite_


 - progression_complexity: [simple, compound] # 2 levels

 - visual_style: [minimal, decorated] # 2 styles


Estimated unique samples: - 10ˆ5

Sampling strategy: Balanced distribution across pattern types


**Example 3:** **G-3 (Stable Sort)**


Parameters:

 - num_shape_types: [2, 3, 4] # 3 options

 - shapes_per_type: [2, 3, 4] # 3 options

 - color_palette: [vibrant, pastel, ...] # 5 palettes

 - initial_layout: random_permutation # n! permutations

 - shape_geometry: [geometric, organic] # 2 styles


Estimated unique samples: - 10ˆ6

Sampling strategy: Uniform sampling across difficulty levels


Diversity is enforced through four complementary mechanisms: stratified sampling, which divides the
parameter space into strata (e.g., difficulty levels) and samples proportionally from each; constraint satisfaction,
which ensures that all generated samples are valid (e.g., mazes admit solutions and puzzles are solvable);
duplicate detection, which tracks parameter combinations via hash functions to prevent exact duplicates; and
visual variety, which randomizes visual attributes such as colors, sizes, and positions beyond the core reasoning
parameters.


Each generated sample undergoes automatic validation, including a solvability check to verify that a groundtruth solution exists (e.g., via A* search for navigation tasks), a visual clarity check to ensure that objects do
not overlap excessively and that text remains legible with a minimum font size, and a parameter bounds check
to confirm that all parameters fall within their specified ranges.


_**B.2.4. Visual Rendering Pipeline**_


All visuals adhere to fixed specifications: a resolution of 512 _×_ 512 pixels, 24-bit RGB color depth (8 bits per
channel), a frame rate of 24 fps for ground-truth videos, and H.264 as the video codec.


**B.3. Large-Scale Distributed Generation of Training Data**


The VBVR-DataFactory component orchestrates the parallel generation of one million training samples using
the 300+ generators in our data spring. It provides a complete, production-grade serverless system for cloud
infrastructure, generation workflow, data organization, and quality assurance, enabling efficient, reliable, and
cost-effective large-scale data production.


All generated samples are stored on Amazon Web Services (AWS) Simple Storage Service (S3). S3 is chosen
for its ability to scale to petabyte-level data with automatic capacity management, its high durability through
redundant storage across multiple availability zones, and its fine-grained access control through IAM policies.
Training data are kept in private buckets with server-side encryption to prevent public exposure and test-set
contamination. In addition, S3’s tiered storage model makes long-term archival cost-effective.


To efficiently generate one million samples, VBVR-DataFactory employs distributed serverless processing
via AWS Lambda. The system distributes tasks across up to 990 concurrent Lambda function instances, each
configured with 3 GB memory and a 15-minute execution timeout. Generation tasks are queued in Amazon
SQS and automatically trigger Lambda invocations, eliminating the need for manual cluster management.
Within each task, samples are produced in configurable batches of 25–100 to balance memory usage and
processing efficiency. A typical one-million-sample generation completes in approximately 2–4 hours with the
full fleet of 990 concurrent workers, at a total cost of roughly $800–1200 per run (primarily Lambda compute


33


[VIDEO-REASON.COM](https://video-reason.com) _A Very Big Video Reasoning Suite_


and S3 storage). Fault tolerance is built in through SQS’s automatic retry mechanism with configurable
visibility timeouts, a Dead Letter Queue (DLQ) for failed messages after one retry attempt, and CloudWatch
metrics for real-time monitoring of task success rates and processing durations.


The end-to-end generation pipeline begins with configuration and planning, where generators, sample counts,
random seeds, and output formats are defined. Tasks are submitted to the SQS queue as Pydantic-validated
JSON messages, each specifying the generator type, number of samples, starting index for global sample
numbering, random seed, and output format (individual files or compressed tar archives). Lambda functions
receive these messages, execute the corresponding generator subprocess, validate and rename outputs with zeropadded global indices, upload results to S3 with structured prefixes, and emit success metrics to CloudWatch.
Failed tasks automatically move to the DLQ for manual inspection and resubmission after debugging.


On a per-task basis (100 samples, typical batch size), sample generation requires approximately 15 minutes,
with generation speed varying significantly by task complexity—simple geometric tasks average 1–3 seconds
per sample, while complex graph or physics tasks require 9–15 seconds per sample. File organization and
S3 upload add 1–2 minutes depending on file sizes, and Lambda cold starts contribute an additional 5–10
seconds for the first invocation. Each task therefore completes in roughly 15–20 minutes on a Lambda
instance, enabling the entire one-million-sample corpus to be produced in 2–4 hours with 990 parallel workers.
For efficient access during training, VBVR-DataFactory maintains a hierarchical S3 structure organized by
generator and task, with each sample directory containing standardized files (first ~~f~~ rame.png, prompt.txt, and
optionally final ~~f~~ rame.png and ground ~~t~~ ruth.mp4). This organization allows training pipelines to locate, filter,
and stream data efficiently at scale through S3’s prefix-based listing and parallel download capabilities.


Quality assurance is integrated throughout generation. Every sample is validated by the generator’s internal
checks before being saved, ensuring solvability, visual clarity, and file integrity. The system continuously
monitors task success rates, processing durations, and samples uploaded through CloudWatch metrics, with
alarms configured to detect anomalies such as high failure rates or DLQ accumulation. Sample diversity is
enforced through unique per-task random seeds that increment deterministically across batches, preventing
duplicate generation. The DLQ captures and preserves failed tasks for post-mortem analysis, enabling
systematic debugging of generator issues and infrastructure failures. Across typical production runs, task
validation failures occur in fewer than 1 percent of cases, primarily due to edge-case parameter combinations
that are caught by Pydantic schema validation before reaching the generator. Infrastructure-related failures
(timeouts, out-of-memory errors) occur in approximately 0.1–0.5 percent of tasks and are resolved through
DLQ resubmission after adjusting batch sizes or addressing generator bugs.


All training samples are stored in private S3 buckets with server-side encryption (SSE-S3), versioning disabled
to reduce costs, and IAM role-based access control restricted to authorized Lambda functions and training
pipelines. Full S3 access logging is enabled for audit trails. The data contain no personally identifiable
information, as all samples are fully synthetic and procedurally generated. Together, these design choices
demonstrate that, with proper serverless engineering, million-scale, high-quality data generation is achievable,
reliable, and cost-effective. The resulting one million samples form the training foundation for VBVR-Wan
and future video reasoning systems.


34


[VIDEO-REASON.COM](https://video-reason.com) _A Very Big Video Reasoning Suite_


**C. VBVR-Bench Details**


**C.1. Model Inference Infrastructure**


VBVR-Bench is an end-to-end evaluation framework that integrates large-scale model inference (or API-based
invocation for proprietary models) with a rule-based evaluation engine over a standardized 100-task video
reasoning benchmark. At the model level, VBVR-Bench provides a unified VideoGenerator abstraction
that encapsulates 29 video generation systems, including closed-source models such as Google Veo, OpenAI
Sora, and Runway Gen-4, as well as open-source and research models such as CogVideoX, Wan2.2, LTX-2,
and HunyuanVideo. This abstraction ensures that all models are executed through an identical pipeline,
eliminating confounding factors introduced by model-specific inference logic. It supports batch execution
at scale, incorporates caching mechanisms to avoid redundant generations, and is fully reusable, allowing
interrupted evaluations to continue without loss of progress.


_**C.1.1. Model Selection and Configuration**_


For the VBVR benchmark, we evaluate eight state-of-the-art image-to-video (I2V) models representing diverse
architectures and capabilities:


**Table 8** Evaluated Models


**Model** **Developer** **Architecture** **Parameters** **Key Features**


CogVideoX1.5-5B-I2V Tsinghua University / Zhipu AI Transformer-based diffusion model 5 billion Strong text-image alignment
Wan2.2-I2V-A14B Wanx AI Latent diffusion with attention mechanisms 14 billion High-fidelity temporal consistency
LTX-2 Lightricks Efficient transformer architecture _∼_ 3 billion Fast inference
HunyuanVideo-I2V Tencent Hunyuan Multi-stage diffusion with spatial-temporal attention _∼_ 7 billion Strong on complex scenes
Veo Google DeepMind Proprietary (closed-source) Unknown (large-scale) Strong physics understanding
Sora OpenAI Proprietary (closed-source, rumored diffusion transformer) Unknown (likely _>_ 10B) Temporal coherence, realistic physics
Runway Gen-3 Runway ML Proprietary (closed-source) Unknown Creative generation, text adherence
Kling 2.6 Kuaishou Technology Proprietary (closed-source, likely diffusion-based) Unknown Fast inference


The models included in the benchmark are chosen to reflect the breadth and maturity of the current imageto-video landscape. The set intentionally mixes open-source and closed-source systems, ensuring that both
academic and industrial approaches are represented. It spans a wide range of architectural paradigms, capturing
fundamentally different design philosophies in video generation. The selected models cover a broad scale
spectrum, from approximately 3B parameters to 14B+ and beyond, enabling analysis of how reasoning
capability correlates with model size. All included systems represent state-of-the-art performance as of late
2025 and early 2026, ensuring that the benchmark reflects the current frontier of the field.


To ensure fair and controlled comparison, all generated videos follow the resolution of their corresponding
ground-truth videos, which include both square and rectangular aspect ratios. For open-source models that
support custom input resolutions, we specify the resolution to match the ground truth. For closed-source
models with fixed resolution constraints (e.g., Sora 2 only supports 1280×720 or 720×1280), we pad the
first-frame image with a background color and automatically detect and remove the padding during evaluation.
Frame rates range from 15–24 fps depending on model requirements. For API-based models, we adopt the
default or provider-recommended generation settings, while for open-source models we use the configurations
reported in their original papers. This standardization removes confounding factors arising from resolution
or tuning differences, ensuring that observed performance differences reflect reasoning ability rather than
generation format.


**C.2. Details of Human Preference Analysis**


_**C.2.1. Data Preparation**_


To mitigate potential biases in pairwise comparisons, we adopt two complementar scoring schemes: **relative**
**scoring** based on pairwise preference judgments, and **absolute** **scoring** based on independent per-video
ratings. In cases where the absolute scores clearly indicate that one video is superior but the corresponding
relative annotation contradicts this assessment, the final decision is revised in favor of the absolute judgment.
For each sample consisting of a text prompt and an initial image pair _pi_, we generate videos using nine


35


[VIDEO-REASON.COM](https://video-reason.com) _A Very Big Video Reasoning Suite_


video generation models _M_ = _{M_ 1 _, M_ 2 _, M_ 3 _, M_ 4 _, M_ 5 _, M_ 6 _, M_ 7 _, M_ 8 _, M_ 9 _}_, producing a set of outputs _Gi_ =
_{Vi,_ 1 _, Vi,_ 2 _, Vi,_ 3 _, Vi,_ 4 _, Vi,_ 5 _, Vi,_ 6 _, Vi,_ 7 _, Vi,_ 8 _, Vi,_ 9 _}_ .

For relative evaluation, all pairwise combinations are constructed within each group, resulting in �92� = 36
unique video pairs per sample. For absolute evaluation, the dataset contains 500 distinct prompt–image pairs
_pi_ . Each pair is processed by all nine models, yielding a total of 500 × 9 = 4,500 single-video annotation
instances.


Each video is presented together with its corresponding text prompt and task-specific evaluation documents.
To reduce annotation noise, every video is independently annotated five times. All samples are randomly
shuffled before assigned to annotators.


_**C.2.2. Human annotation**_


Annotators are between 20 and 35 years old and possess basic domain knowledge relevant to the tasks. All
annotators undergo standardized training to ensure consistent interpretation of evaluation criteria.


For relative scoring, annotators are shown two videos generated from the same prompt and are asked to select
which one better completes the task and aligns with the given prompt overall, with ties allowed.


For absolute scoring, annotators rate each video along three dimensions using a 5-point Likert scale, where
higher scores indicate better performance. **Task Completion (TC)** assessing whether the task goal is achieved;
**Reasoning Logic (RL)**, assessing the correctness of the reasoning process; and **Visual Quality (VQ)**, assessing
visual clarity, temporal coherence, and rendering fidelity.


_**C.2.3. Win Ratio Calculation**_


From relative human annotations, we compute a win ratio for each model. In each comparison, the preferred
model receives a score of 1 and the other 0; in the case of a tie, both receive 0.5. Win ratios are aggregated
across all pairwise comparisons for each evaluation split.


From absolute annotations, we average the scores of the TC, RL and VQ dimensions to obtain a final score per
sample. These absolute scores are used for cross-verification of pairwise results and for resolving contradictory
annotations between the two scoring schemes.


Finally, we compare the win ratios derived from relative human annotations (with cross-verification using
absolute scores) with the win ratios computed from VBVR-Bench ’s automatic evaluation metrics, and measure
the correlation between the two across models.


**C.3. Detailed Analysis Protocols and Additional Results**


_**C.3.1. Residualized Capability Correlation**_


This section details the computation behind Fig. 5 in the main paper. Our goal is to quantify _capability_
_dependency_ between cognitive categories while avoiding trivial correlations induced by overall model strength.


**Category scores.** Let _m_ index models and _c_ index categories (five total). For each model _m_ and category _c_,
we compute a category-level score by averaging the per-sample Overall ratings:


_Sm,c_ = mean�Overall� over all evaluated samples with Category = _c_ for model _m._


**General factor.** We define a model-level general factor as the overall mean score across all samples:


_Gm_ = mean�Overall� over all evaluated samples for model _m._


**Residualization.** For each category _c_, we regress _Sm,c_ on _Gm_ across models:


_Sm,c_ = _ac_ + _bcGm_ + _ϵm,c,_


and retain the residuals _ϵm,c_ as the _strength beyond overall model quality_ .


36


[VIDEO-REASON.COM](https://video-reason.com) _A Very Big Video Reasoning Suite_


**Capability dependency matrix.** For each pair of categories ( _c_ 1 _, c_ 2), we compute Pearson correlation across
models using residuals:
_Rc_ 1 _,c_ 2 = corr ( _{ϵm,c_ 1 _}m, {ϵm,c_ 2 _}m_ ) _._


The resulting 5 _×_ 5 matrix _R_ is visualized as a heatmap (main paper, Fig. 5).


**Implementation** **notes.** We use the benchmark table and compute (i) _Sm,c_, (ii) _Gm_, (iii) residuals by
ordinary least squares, and (iv) Pearson correlations on residuals. We also report Spearman _ρ_ in auxiliary
analysis to confirm robustness to monotonic transformations.


_**C.3.2. Domain-wise Score Distributions (Boxplots)**_


To complement mean performance summaries, we report domain-wise score distributions across models
using boxplots: **task-level** distributions, where each point corresponds to a task mean score within a domain
(capturing cross-task variability).


**Figure 9** Domain-wise score distributions across 9 models (red dashed line separates baselines and VBVRWan2.2).


Task-Level Boxplot: Model Performance by Domain (9 Models: Open-source | Closed-source | Ours)



CogV Hunyuan LTX Wan Kling Runway Veo Sora VBVR
Model


37



CogV Hunyuan LTX Wan Kling Runway Veo Sora VBVR
Model



Abstraction

(23 tasks)



Perception

(30 tasks)



Transformation

(20 tasks)



5


4


3


2


1



CogV Hunyuan LTX Wan Kling Runway Veo Sora VBVR
Model



Knowledge

(14 tasks)


CogV Hunyuan LTX Wan Kling Runway Veo Sora VBVR
Model



Spatiality
(13 tasks)


CogV Hunyuan LTX Wan Kling Runway Veo Sora VBVR
Model


[VIDEO-REASON.COM](https://video-reason.com) _A Very Big Video Reasoning Suite_


**D. Selected Tasks and Rubrics**


This appendix includes a curated set of tasks that require multi-step planning and/or multiple interacting
constraints. For each task, we show the initial and final frames, followed by the evaluation rubric used to score
model outputs.


**Stable Sort (Task G-3)** Rearrange objects by grouping them by shape type and sorting each group by size
while preserving all attributes, testing multi-constraint spatial reasoning, attribute fidelity, and rule following.


**(a)** First **(b)** 1st Progression **(c)** 2nd Progression **(d)** Final


**Figure 10** Stable Sort


**Example Prompt** “The scene contains two types of shapes, each type has three shapes of different sizes
arranged randomly. Keep all shapes unchanged in appearance (type, size, and color). Only rearrange their
positions: first group the shapes by type, then within each group, sort the shapes from smallest to largest (left
to right), and arrange all shapes in a single horizontal line from left to right.”
_Human Annotation Scoring (1–5):_


  - **5 (Perfect).** Correct grouping; correct within-group ascending size order (left to right); horizontal
alignment; attributes preserved (type/size/color); reasonable spacing, no overlaps.


  - **4 (Near-perfect).** Correct grouping and ordering with one minor imperfection (e.g., small color deviation
(hue shift within _±_ 10%), small size deviation (within _±_ 5%), slight vertical misalignment, or mildly
uneven spacing) while the intended layout remains clear.


  - **3 (Partially correct).** Grouping is correct but ordering is wrong in at least one group; _or_ grouping and
ordering are correct but attribute changes are noticeable (e.g., color shift _>_ 10%, size change _>_ 5%, or
mild deformation while still recognizable).


  - **2 (Multiple errors).** Incorrect grouping and/or incorrect ordering, and/or missing/extra objects.


  - **1 (Failure).** Objective not achieved (no intended grouping/ordering) and/or severe object
modification/loss.


_Evaluation dimensions (suggested weights):_


  - **Classification accuracy (30%).** Correctly identify the two shape types; group identical shapes; include
all 6 objects.


  - **Ordering correctness (30%).** Ascending size order within each group; coherent left-to-right
organization.


  - **Object fidelity (30%).** Preserve shape type, size, and color; maintain clear contours/edges.


  - **Layout accuracy (10%).** Horizontal alignment and reasonable spacing.


38


[VIDEO-REASON.COM](https://video-reason.com) _A Very Big Video Reasoning Suite_


**Grid Avoid Obstacles (Task G-15)** Navigate a 10 _×_ 10 grid from start to goal using only 4-neighbor moves
without entering obstacle cells, testing shortest-path planning under hard constraints.


**(a)** First **(b)** 1st Progression **(c)** 2nd Progression **(d)** Final


**Figure 11** Grid Avoid Obstacles

**Example Prompt** : “The scene shows a 10x10 grid with a blue start square (containing a yellow circular
agent), a red end square, and multiple black X marks indicating obstacles. Starting from the blue start square,
the agent can move to adjacent cells (up, down, left, right) each step. The goal is to move the agent to the red
end square along the shortest path without entering any cells marked with black X obstacles.”
_Human Annotation Scoring (1–5):_


  - **5 (Perfect).** Reaches the goal; avoids all obstacles; uses a shortest (or tied-shortest) obstacle-avoiding
path; movement is legal (4-neighbor, within-grid) and agent appearance is preserved.


  - **4 (Near-perfect).** Reaches the goal and avoids all obstacles; only a minor imperfection (e.g., _≤_ 2 extra
steps vs. optimal, slight appearance drift, or minor legal-motion jitter).


  - **3 (Partially correct).** Clear attempt but with a notable issue (e.g., enters exactly one obstacle cell once,

_>_ 2 extra steps, stops short of the goal, or an occasional illegal/diagonal tendency).


  - **2 (Mostly incorrect).** Multiple violations (e.g., enters 2–3 obstacle cells) and/or out-of-grid motion
and/or highly inefficient/random routing and/or fails to reach the goal.


  - **1 (Failure).** No meaningful progress or unrelated output; frequent obstacle crossings ( _≥_ 4) or the grid is
corrupted.


_Evaluation dimensions (suggested weights):_


  - **Obstacle avoidance (40%).** Zero obstacle entries; respects non-traversable constraint.


  - **Path optimality (30%).** Shortest path length under obstacle constraints.


  - **Motion-rule compliance (20%).** 4-neighbor steps, within-grid, continuous trajectory.


  - **Task completion (10%).** Reaches the goal with a coherent start→goal trajectory.


39


[VIDEO-REASON.COM](https://video-reason.com) _A Very Big Video Reasoning Suite_


**Grid Go Through Block (Task G-16)** Plan a near-shortest 4-neighbor route that visits all marked target
cells (in blue) before reaching the goal (in red) in a 10 _×_ 10 grid, testing multi-goal route optimization under
movement constraints.


**(a)** First **(b)** 1st Progression **(c)** 2nd Progression **(d)** Final


**Figure 12** Grid Go Through Block

**Example Prompt** :“The scene shows a 10x10 grid with a green start square (containing an orange circular
agent), a red end square, and multiple blue rectangular blocks. Starting from the green start square, the agent
can move to adjacent cells (up, down, left, right) each step. The goal is to move the agent to the red end square
along the shortest path that passes through all blue blocks (the agent must visit every blue block before
reaching the red end square).”
_Human Annotation Scoring (1–5):_


  - **5 (Perfect).** Starts at the start cell and ends at the goal; visits all targets; uses a globally shortest route
under the visit-all constraint; motion is legal (4-neighbor, within-grid) and agent appearance is preserved.


  - **4 (Near-perfect).** Reaches the goal and visits all targets; only small imperfections (e.g., _≤_ 3 extra steps,
minor appearance drift, or slight presentation issues while the realized path remains grid-orthogonal).


  - **3 (Partially correct).** Clear attempt but with a notable issue (e.g., misses exactly one target, _>_ 3 extra
steps, stops before the goal, or an occasional illegal move).


  - **2 (Mostly incorrect).** Misses two or more targets and/or fails to reach the goal, and/or frequent
illegal/out-of-grid motion, and/or highly inefficient/random routing.


  - **1 (Failure).** No meaningful progress; ignores targets or output is unrelated / grid is broken.


_Evaluation dimensions (suggested weights):_


  - **Target coverage (40%).** All targets visited; none missing; targets remain visible.


  - **Route optimality (30%).** Near-global shortest route under the visit-all constraint (target order matters).


  - **Task completion (20%).** Full start→(all targets)→end sequence completed.


  - **Motion legality (10%).** 4-neighbor steps only; stays within grid; coherent step-by-step movement.


40


[VIDEO-REASON.COM](https://video-reason.com) _A Very Big Video Reasoning Suite_


**Directed** **Graph** **Navigation** **(Task** **G-31)** Navigate from the start node to the goal node by traversing
only along directed edges (respecting arrow direction) with a minimum-hop path, testing goal-directed graph
planning under directionality constraints.


**(a)** First **(b)** 1st Progression **(c)** 2nd Progression **(d)** Final


**Figure 13** Directed Graph Navigation

**Prompt** :“The scene shows a network of nodes connected by directed edges (edges with arrows indicating
direction) with a green starting node, a red ending node, and a blue triangular agent positioned at the green
starting node. The agent can only move along edges in the direction they point (from the source node to the
target node, cannot move backwards), moving from one node to an adjacent node each step. Move the blue
triangular agent from the green starting node to the red ending node along the path with the minimum number
of steps.”
_Human Annotation Scoring (1–5):_


  - **5 (Perfect).** Reaches the goal; uses a minimum-hop path; strictly follows arrow directions and moves
only along existing edges; motion is continuous and the graph is preserved.


  - **4 (Near-perfect).** Reaches the goal with correct direction/edge-following behavior; only minor
presentation issues while path length remains shortest.


  - **3 (Partially correct).** Reaches the goal but with a notable issue (e.g., +1–2 extra hops, a single direction
violation, or slight deviation from drawn edges).


  - **2 (Mostly incorrect).** Severe issues: _≥_ 3 extra hops, multiple direction violations, “flying”/cutting
across space, reaches the wrong node, or alters graph structure.


  - **1 (Failure).** Does not reach the goal, behavior is random/invalid (ignores arrows), or the graph is
corrupted.


_Evaluation dimensions (suggested weights):_


  - **Shortest-path correctness (40%).** Minimum-hop path length.


  - **Direction compliance (35%).** No reverse traversals; respects arrow orientation.


  - **Motion legality (15%).** Moves along existing edges, one edge per step; no teleportation.


  - **Graph fidelity (10%).** Nodes/edges/arrows remain unchanged.


41


[VIDEO-REASON.COM](https://video-reason.com) _A Very Big Video Reasoning Suite_


**Key Door Matching (Task G-45)** In a maze, first collect the prompt-specified colored key and then reach
the matching door via legal corridor moves near shortest, testing instruction grounding, sequencing, and
constrained navigation.


**(a)** First **(b)** 1st Progression **(c)** 2nd Progression **(d)** Final


**Figure 14** Key Door Matching

**Prompt** :“The scene shows a maze with a green circular agent, colored diamond-shaped keys, and colored
hollow rectangular doors. Find the Blue key and then navigate to the matching Blue door, showing the
complete movement process step by step.”
_Human Annotation Scoring (1–5):_


  - **5 (Perfect).** Reaches the correct target-colored key, then reaches the matching door (correct order); path
is legal and continuous; path length is near-optimal (e.g., _≤_ 120% of BFS shortest for start _→_ key _→_ door);
key disappears when reached; full trajectory is shown.


  - **4 (Near-perfect).** Correct key and door in correct order; minor issues only (e.g., slightly longer path
_∼_ 120%–150%, small jitter/backtracking, or a 1–2 frame delay in key disappearance).


  - **3 (Partially correct).** Finds the correct key but makes a major mistake (e.g., goes to wrong door,
completes only one stage, noticeably inefficient path _∼_ 150%–200%, or 1–2 minor wall violations).


  - **2 (Mostly incorrect).** Wrong key color and/or wrong order (door before key), and/or multiple wall
crossings, and/or extremely inefficient path ( _>_ 200%), or stops at irrelevant locations.


  - **1 (Failure).** Agent barely moves or moves randomly; ignores maze constraints; incorrect key/door colors;
or agent behavior is abnormal.


_Evaluation dimensions (suggested weights):_


  - **Target identification (30%).** Correctly identify the prompt-specified key and matching door; do not
confuse with other colors.


  - **Path validity (30%).** Follow allowed corridors only, avoid wall collisions, and maintain step-by-step
movement.


  - **Path efficiency (20%).** Actual path length relative to the BFS-optimal path; _≤_ 110% = excellent,
110–130% = acceptable, _>_ 200% = poor.


  - **Animation quality (20%).** Smooth frame-by-frame movement; agent centers align with key and door;
key pickup effect visible.


42


