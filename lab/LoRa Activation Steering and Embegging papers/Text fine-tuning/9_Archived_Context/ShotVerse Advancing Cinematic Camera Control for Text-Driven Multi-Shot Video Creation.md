## **ShotVerse : Advancing Cinematic Camera Control for** **Text-Driven Multi-Shot Video Creation**

**Songlin Yang** [1] _[,]_ [2] _[,][†][,][∗]_ **, Zhe Wang** [1] _[,]_ [2] _[,][†]_ **, Xuyi Yang** [1] _[,]_ [2] _[,][†]_ **,**
**Songchun Zhang** [1] **, Xianghao Kong** [1] **, Taiyi Wu** [2] **, Xiaotong Zhao** [2] **, Ran Zhang** [2] **,**
**Alan Zhao** [2] **, Anyi Rao** [1] _[,][‡]_

1MMLab@HKUST, The Hong Kong University of Science and Technology
2Tencent Video AI Center, PCG, Tencent
```
          syangds@connect.ust.hk, anyirao@ust.hk
```

[Project Page](https://shotverse.github.io)


Shot 1 Shot 2



































**“low-angle” + “medium close-up” + “slight backward jitter”**



**“close-up” + “static”**









**“close-up” + “side-view angle” + “static with slight jitter”**



**“medium shot” + “leftward movement”**



Figure 1: **Cinematic, Camera-Controlled, Multi-Shot Video Creation via our** _**ShotVerse**_ **Frame-**
**work.** (i) _Multi-Shot Data Foundation_ : We curate _**ShotVerse-Bench**_ dataset from high-production
cinema and propose a novel calibration pipeline that aligns disjoint shot trajectories into a unified
global coordinate system. (ii) _“Plan-then-Control” Framework_ : A VLM-based Planner automates the
plotting of explicit, unified, cinematic trajectories from prompts, which serve as precise guidance for
the Controller to synthesize content. (iii) _Superior Performance_ : Examples demonstrate high-fidelity
and great camera-controlled generation across diverse genres. The inset 3D plots visualize the plotted
explicit trajectories.


**Abstract**


Text-driven video generation has democratized film creation, but camera control in
cinematic multi-shot scenarios remains a significant block. Implicit textual prompts
lack precision, while explicit trajectory conditioning imposes prohibitive manual
overhead and often triggers execution failures in current models. To overcome
this bottleneck, we propose a data-centric paradigm shift, positing that aligned
_(Caption,_ _Trajectory,_ _Video)_ triplets form an inherent joint distribution that can
connect automated plotting and precise execution. Guided by this insight, we
present _**ShotVerse**_, a “Plan-then-Control” framework that decouples generation
into two collaborative agents: a VLM (Vision-Language Model)-based Planner that


_∗_ Project leader

_†_ Equal contribution

_‡_ Corresponding author


Preprint.


leverages spatial priors to obtain cinematic, globally aligned trajectories from text,
and a Controller that renders these trajectories into multi-shot video content via a
camera adapter. Central to our approach is the construction of a data foundation: we
design an automated multi-shot camera calibration pipeline aligns disjoint singleshot trajectories into a unified global coordinate system. This facilitates the curation
of _**ShotVerse-Bench**_, a high-fidelity cinematic dataset with a three-track evaluation
protocol that serves as the bedrock for our framework. Extensive experiments
demonstrate that _**ShotVerse**_ effectively bridges the gap between unreliable textual
control and labor-intensive manual plotting, achieving superior cinematic aesthetics
and generating multi-shot videos that are both camera-accurate and cross-shot
consistent.


**1** **Introduction**


Text-driven video generation models [47] have democratized film creation, empowering users to act
as **directors** who synthesize cinematic clips from natural language. However, as the field progresses
toward multi-shot video generation, while users can now easily dictate _“what to see”_, the role of the
**cinematographer** —executing the precise _“how to shoot”_ via cinematic camera control—remains
a significant bottleneck [34]. Existing methods either struggle to accurately follow textual camera
conditions (e.g., “pan left”, “zoom in”) [41, 49, 58] or fail to ensure that cameras in a multi-shot
setting share a unified coordinate system [3, 23, 24] and that their combination conforms to cinematic
patterns [54, 25]. A straightforward solution to these issues is to guide the video model with explicit,
unified, and cinematic camera trajectories.


While this solution effectively grounds the camera motion, it introduces a new bottleneck, as plotting
and executing a cinematic multi-shot trajectory is non-trivial. First, manually plotting [56] cinematic
trajectories imposes a prohibitive design burden. Users must meticulously synchronize camera poses
in a unified global coordinate system with narrative flow, a labor-intensive process that demands
strong spatial reasoning and intrinsic aesthetic guidance. Second, a critical execution gap remains:
the state-of-the-art camera-controlled video models tend to treat such complex cinematic trajectories
as out-of-distribution conditions, leading to failure generation (see results in Fig. 3).


To tackle this bottleneck, we argue that this task demands a paradigm shift, rethinking from a
data-centric perspective. The aligned triplets of _(Caption, Trajectory, Video)_ naturally form a joint
distribution, and viewing the task through this lens offers two critical advantages: (i) _Automating_
_Cinematic Plotting_ : By modeling the conditional probability P( _Trajectory_ | _Caption_ ), we can leverage
the spatial priors of pre-trained vision-language models [10, 5, 13] (VLM) to directly infer camera
trajectories from text, bypassing the burden of manual plotting. (ii) _Enabling Aligned-Yet-Decoupled_
_Training_ : The _(Caption, Trajectory, Video)_ triplets are inherently aligned, which allows decoupled
optimization—optimizing P( _Trajectory_ | _Caption_ ) for plotting and P( _Video_ | _Caption_, _Trajectory_ ) for
generation, independently. This strategy avoids the instability of joint training while ensuring that the
plotted trajectories remain compatible with the generator’s execution domain.


Based on these insights, we propose _**ShotVerse**_, a “Plan-then-Control” framework, which receives
user prompts with camera description, maps them to explicit trajectories via a Planner, and utilizes a
Controller to generate multi-shot videos based on these trajectories and the prompts. Specifically,
_**ShotVerse**_ consists of two agents aligned by the shared data distribution: (i) _Planner_ : A VLM
fine-tuned to map high-level textual descriptions into explicit camera trajectories. It leverages the
learned joint distribution to predict explicit camera trajectories that respect cinematic patterns. (ii)
_Controller_ : Built upon a holistic multi-shot video backbone [41], it receives the explicit trajectories
and utilizes a lightweight camera adapter to render high-fidelity cinematic content. We specifically
adopt the holistic paradigm to bypass the complex inductive biases required for multi-shot consistency
in auto-regressive methods [58, 16], allowing us to focus purely on camera control mechanism.


Crucially, the validity of our data-centric hypothesis rests on the quality of the data itself. To address
the scarcity of aligned multi-shot data, we collect raw footage from high-production videos and
propose an automated camera calibration pipeline that aligns disjoint single-shot trajectories into a
unified global coordinate system. Paired with hierarchical captions, this constitutes _**ShotVerse-Bench**_,
which serves as both a high-fidelity training foundation and a rigorous evaluation benchmark. By
introducing a three-track evaluation protocol, this benchmark enables the comprehensive measurement


2


of cinematic planning, execution fidelity, and multi-shot consistency. As shown in Fig. 1, extensive
experiments demonstrate that our framework leverages the Planner for superior cinematic plotting
and enables the Controller to generate multi-shot videos that are both camera-accurate and cross-shot
consistent.


_**Distinctions and Contributions.**_ (i) In contrast to full-stack filmmaking frameworks [55, 53] based
on multi-agent systems [14, 36], _**ShotVerse**_ only focuses on the core component of explicit cinematic
camera control. Our method bridges high-level narrative intent with precise geometry via two
specialized agents: a Planner that plots script-driven, unified 3D trajectories, and a Controller that
injects these professional-grade camera patterns into multi-shot foundation models. (ii) Unlike
generic camera trajectory generation [59] and control [3, 23], we emphasize the automated synthesis
and execution of explicit cinematic trajectories, enabling models to manifest nuanced cinematography
beyond basic camera motion templates. (iii) We are the first to address explicit cinematic camera
control specifically for holistic multi-shot generation models, ensuring cross-shot coherence within a
unified global coordinate system. (iv) We provide an automated multi-shot camera calibration pipeline
to facilitate scalable data annotation and empower future research in multi-shot video synthesis.


**2** **Related Work**


_**Multi-Shot**_ _**Video**_ _**Creation.**_ Cascaded approaches [66, 55, 61, 48, 12, 64] struggle to maintain
consistency in the temporal gaps. To address this, memory-based methods [58, 25] formulate
generation as iterative shot synthesis conditioned on explicit memory, yet they face challenges with
error accumulation. Consequently, the field has shifted toward holistic generation, which fine-tunes
single-shot baselines (e.g., Wan [47]) to model the entire sequence jointly [22, 55, 8, 28, 49, 30].


_**Camera Trajectory Datasets.**_ MVImgNet [57], RealEstate10K [65], and DL3-DV-10K [37] primarily
capture basic paths in static environments, lacking cinematic narratives. While CCD [29] and
E.T. [11] introduce human-centric tracking, and GenDoP [59] focuses on cinematic moves, they
remain confined to single-shot settings without global spatial coherence. _In contrast, our_ _**ShotVerse-**_
_**Bench**_ _dataset uniquely provides multi-shot sequences calibrated into a unified coordinate system,_
_serving as the first dataset for learning cross-shot spatial logic and cinematic consistency._


_**Camera Trajectory Generation.**_ Early approaches relied on optimization [6, 38, 17, 40] or heuristic
constraints [7, 15, 27]. Recent generative methods often depend on explicit 3D priors: CCD [29]
and E.T. [11] require character motion inputs, Director3D [35] relies on object-centric data, and
GenDoP [59] necessitates RGBD information. _Unlike_ _these_ _methods_ _that_ _demand_ _complex_ _pre-_
_construction, we leverage the inherent alignment in our dataset, and utilize the strong semantic-spatial_
_priors of VLMs to automate cinematic plotting._


_**Camera Control for Text-Driven Video Generation.**_ Early approaches [23, 52, 21] encode camera
extrinsics into pre-trained models. Subsequent works enhance geometric fidelity by using 3D
priors [1, 2, 63]. However, they lack the capability to model multi-shot storytelling. Recent research
has expanded into synchronized multi-camera generation [4, 3, 32, 24], aiming for 3D-consistent
scene modeling across different viewpoints. However, these methods ignore orchestrating cinematic
cuts between distinct shots. The relevant work, ShotDirector [54], pioneers shot transitions in
single-shot video generation models by combining camera conditioning with editing-pattern-aware
prompting. However, its trajectory patterns are largely constrained to fixed-point shooting or specific
editing templates. _In contrast, we propose a more cinematic dataset, systematically unify planning_
_and controlling, and specifically target a holistic multi-shot video model._


**3** **Methodology:** _**ShotVerse**_


We propose _**ShotVerse**_ (Fig. 2) to decouple the multi-shot camera control task into planning and
controlling phases, which bridges the gap between unreliable textual camera control and laborintensive manual plotting. Guided by our data-centric perspective that aligned triplets of _(Caption,_
_Trajectory,_ _Video)_ form a joint distribution, this “Plan-then-Control” framework is presented as
follows: First, Sec. 3.1 details the Planner, which models the conditional probability P( _Trajectory_ |
_Caption_ ) to synthesize cinematic, globally unified trajectories from hierarchical textual descriptions.
Second, Sec. 3.2 presents the Controller, modeling P( _Video_ | _Caption_, _Trajectory_ ) to render these


3


|Hierarchical Prompt Construction<br>Global Shot 1Trajectory Shot 2 Trajectory<br>Prompt Prompt Query Prompt Query<br>Text Tokenizer & Embedding Layer|Col2|Col3|Col4|Col5|Col6|Col7|
|---|---|---|---|---|---|---|
|**Hierarchical Prompt Construction**<br>Global<br>Prompt<br>Shot 1<br>Prompt<br>Shot 2<br>Prompt<br>**Trajectory**<br>**Query**<br>**Trajectory**<br>**Query**<br>Text Tokenizer & Embedding Layer|**Hierarchical Prompt Construction**<br>Global<br>Prompt<br>Shot 1<br>Prompt<br>Shot 2<br>Prompt<br>**Trajectory**<br>**Query**<br>**Trajectory**<br>**Query**<br>Text Tokenizer & Embedding Layer|**Hierarchical Prompt Construction**<br>Global<br>Prompt<br>Shot 1<br>Prompt<br>Shot 2<br>Prompt<br>**Trajectory**<br>**Query**<br>**Trajectory**<br>**Query**<br>Text Tokenizer & Embedding Layer|||||
||||||||
|Vision-Language Model** + LoRA**<br>**Context-Aware**<br>**Encoding**|Vision-Language Model** + LoRA**<br>**Context-Aware**<br>**Encoding**|Vision-Language Model** + LoRA**<br>**Context-Aware**<br>**Encoding**|Vision-Language Model** + LoRA**<br>**Context-Aware**<br>**Encoding**|Vision-Language Model** + LoRA**<br>**Context-Aware**<br>**Encoding**|Vision-Language Model** + LoRA**<br>**Context-Aware**<br>**Encoding**|Vision-Language Model** + LoRA**<br>**Context-Aware**<br>**Encoding**|




















|ntroller: Trajectory Injection|Col2|Col3|Col4|Col5|Col6|
|---|---|---|---|---|---|
|Encoder<br>Text Encode<br>**Semantic Content w**<br>**Textural Camera Desc**<br>**ot Camera**<br>**ectories**|Encoder<br>Text Encode<br>**Semantic Content w**<br>**Textural Camera Desc**<br>**ot Camera**<br>**ectories**|Encoder<br>Text Encode<br>**Semantic Content w**<br>**Textural Camera Desc**<br>**ot Camera**<br>**ectories**|Encoder<br>Text Encode<br>**Semantic Content w**<br>**Textural Camera Desc**<br>**ot Camera**<br>**ectories**|Encoder<br>Text Encode<br>**Semantic Content w**<br>**Textural Camera Desc**<br>**ot Camera**<br>**ectories**|Encoder<br>Text Encode<br>**Semantic Content w**<br>**Textural Camera Desc**<br>**ot Camera**<br>**ectories**|
|Self-Attention<br>|Layer Norm||Cross-Attention||Layer Norm|
|DiT<br>Blocks<br>**+LoRA**<br> Noise<br>3D VAE<br>Decoder|DiT<br>Blocks<br>**+LoRA**<br> Noise<br>3D VAE<br>Decoder|DiT<br>Blocks<br>**+LoRA**<br> Noise<br>3D VAE<br>Decoder|DiT<br>Blocks<br>**+LoRA**<br> Noise<br>3D VAE<br>Decoder|DiT<br>Blocks<br>**+LoRA**<br> Noise<br>3D VAE<br>Decoder|DiT<br>Blocks<br>**+LoRA**<br> Noise<br>3D VAE<br>Decoder|
|** Rotary Positional Embedding**<br>**Width**<br>**Shot**<br>∙𝑭𝒔𝒉𝒐𝒕<br>∙𝑭𝒇𝒓𝒂𝒎𝒆<br>∙𝑭𝒉<br>∙𝑭𝒘<br> okens<br> ore)<br>Latent To<br> (After|** Rotary Positional Embedding**<br>**Width**<br>**Shot**<br>∙𝑭𝒔𝒉𝒐𝒕<br>∙𝑭𝒇𝒓𝒂𝒎𝒆<br>∙𝑭𝒉<br>∙𝑭𝒘<br> okens<br> ore)<br>Latent To<br> (After|** Rotary Positional Embedding**<br>**Width**<br>**Shot**<br>∙𝑭𝒔𝒉𝒐𝒕<br>∙𝑭𝒇𝒓𝒂𝒎𝒆<br>∙𝑭𝒉<br>∙𝑭𝒘<br> okens<br> ore)<br>Latent To<br> (After|** Rotary Positional Embedding**<br>**Width**<br>**Shot**<br>∙𝑭𝒔𝒉𝒐𝒕<br>∙𝑭𝒇𝒓𝒂𝒎𝒆<br>∙𝑭𝒉<br>∙𝑭𝒘<br> okens<br> ore)<br>Latent To<br> (After|** Rotary Positional Embedding**<br>**Width**<br>**Shot**<br>∙𝑭𝒔𝒉𝒐𝒕<br>∙𝑭𝒇𝒓𝒂𝒎𝒆<br>∙𝑭𝒉<br>∙𝑭𝒘<br> okens<br> ore)<br>Latent To<br> (After|** Rotary Positional Embedding**<br>**Width**<br>**Shot**<br>∙𝑭𝒔𝒉𝒐𝒕<br>∙𝑭𝒇𝒓𝒂𝒎𝒆<br>∙𝑭𝒉<br>∙𝑭𝒘<br> okens<br> ore)<br>Latent To<br> (After|



Figure 2: **Method Overview.** (i) _Dataset Curation_ . We construct the _**ShotVerse-Bench**_ by aligning
multi-shot trajectories into a unified global coordinate system via camera calibration, paired with
hierarchical global and per-shot captions. (ii) _Trajectory Plotting_ : The Planner utilizes a VLM to
process the hierarchical prompt interleaved with learnable trajectory query tokens. These inputs are
encoded into context-aware embeddings and transformed into explicit camera poses via a Trajectory
Decoder and a Pose De-Tokenizer. (iii) _Trajectory Injection_ : The Controller synthesizes high-fidelity
videos using a holistic DiT backbone. It precisely follows the trajectories via a Camera Adapter and
a 4D Rotary Positional Embedding strategy.


plotted trajectories into multi-shot videos using a holistic Diffusion Transformer (DiT) [44, 41]
backbone.


**3.1** **Planner:** **Shot-Aware Cinematic Trajectory Plotting**


_**Motivation.**_ To achieve automated and cinematic trajectory generation, we must address critical
limitations in existing paradigms. First, workflows [11, 29, 35] relying on pre-construction (e.g., 3D
scene layout or character proxies) inherently lack the potential for scalability and automation. Second,
while data-driven methods offer flexibility, previous works (e.g., GenDoP [59]) typically utilize
shallow text encoders, which fail to capture the deep spatial reasoning required for complex multi-shot
narratives. Large Vision-Language Models (e.g., Qwen3-VL [5]) offer a promising solution to bridge
this semantic-geometric gap due to their rich spatial priors [9]. However, a fundamental challenge
remains: directly tasking a VLM to predict variable-length, long-horizon trajectory sequences is
structurally inefficient and prone to model degeneration.


_**Overview.**_ To reconcile these challenges, we propose a shot-aware cinematic trajectory Planner. As
shown in Fig. 2, we first construct a hierarchical prompt, and then adopt a VLM to encode these inputs
to extract context-aware “camera codes”. A trajectory decoder is adopted to expand these codes into
variable-length trajectory tokens. Finally, a pose de-tokenizer de-tokenizes them into explicit camera
poses. The Planner is trained end-to-end to maximize the log-likelihood of the ground-truth tokens.


_**Task**_ _**Formulation**_ _**and**_ _**Trajectory**_ _**(De-)Tokenization.**_ We formulate planning as generating a
sequence of _K_ camera trajectories _S_ = _{S_ [(] _[k]_ [)] _}_ _[K]_ _k_ =1 [, where each shot] _[ S]_ [(] _[k]_ [)] [=] _[ {]_ **[P]** [(] _t_ _[k]_ [)] _}_ _[L]_ _t_ =1 _[k]_ [consists of]
_Lk_ poses defined in a unified global coordinate system. Each pose **P** [(] _t_ _[k]_ [)] _∈_ _SE_ (3) is represented using
a 12D continuous vector [ **t** _t,_ **r** _t_ ] where translation **t** _t_ _∈_ R [3] and rotation **r** _t_ _∈_ R [9] . We implement a
reversible tokenization pipeline where continuous camera parameters are normalized and discretized
into integer bins. Conversely, the de-tokenizer maps generated tokens back to continuous values via
bin centers, applying inverse scaling to recover the explicit trajectory in the unified global coordinate
system.


4


_**Hierarchical**_ _**Prompt**_ _**Construction.**_ To avoid semantic confusion between shots, we design a
structured input sequence **I** _in_ that interleaves semantic context with learnable query placeholders as:











Tok( _X_ [ (] _shot_ _[k]_ [)] [)] _[ ⊕]_ [[] `[<TRAJ>]` 1 [(] _[k]_ [)] _[, . . .,]_ `[ <TRAJ>]` _M_ [(] _[k]_ [)][]]  _,_ (1)

        - ��        Query Tokens for Shot _k_



**I** _in_ = Tok( _Xglobal_ ) _⊕_



_K_



_k_ =1



where _⊕_ denotes concatenation, and Tok( _·_ ) denotes text tokenizer. The input _Xtext_ is decomposed
into a global prompt _Xglobal_ and a sequence of per-shot prompts _{Xshot_ [(1)] _[, . . .,][ X]_ _shot_ [ (] _[K]_ [)] _[}]_ [.] [We append a]
fixed number of learnable trajectory query tokens, denoted as _{_ `<TRAJ>` [(] _m_ _[k]_ [)] _[}][M]_ _m_ =1 [, immediately after]
each shot’s textual description. These tokens serve as “slots” for the VLM to fill with shot-specific
camera plans.


_**Context-Aware**_ _**Encoding.**_ Since shallow text encoders [46] lack spatial reasoning, we leverage
the VLM backbone to perform a “mental simulation” of camera movement. Facilitated by the
self-attention mechanism, the hidden states of the trajectory query tokens aggregate information
from the global context, previous shots (causal dependency), and the specific instruction for the
current shot. Specifically, we employ the VLM backbone Φ( _·_ ) to encode the entire sequence **I** _in_, and
extract the final-layer hidden states corresponding to the query tokens of each shot _k_ as camera codes,
denoted as **H** [(] _plan_ _[k]_ [)] _[∈]_ [R] _[M]_ _[×][D]_ [vlm][, where] _[ D]_ [vlm][ is the hidden dimension of the VLM.]


_**Trajectory Decoder.**_ The VLM produces a fixed number ( _M_ ) of camera codes for each shot, whereas
the actual camera trajectory requires a variable-length sequence of pose tokens. To enable joint
temporal modeling across shots, we concatenate all shot-level codes with learnable separator tokens
`<SEP>` as:

              -               **H** _plan_ = **H** [(1)] _plan_ [;] `[ <SEP>]` [;] **[ H]** [(2)] _plan_ [;] `[ <SEP>]` [;] _[ . . .]_ [ ;] `[ <SEP>]` [;] **[ H]** [(] _plan_ _[K]_ [)] _._ (2)


The concatenated sequence **H** _plan_ serves as a prefix to a lightweight auto-regressive Transformer [60]
decoder, which models the probability _P_ ( **S** _traj|_ **H** _plan_ ). Since the VLM hidden dimension may differ
from the decoder embedding dimension, we project **H** plan to the decoder embedding space via a linear
layer to match the decoder embedding dimension _D_ . At decoding step _j_, the input is formulated as:


**X** _j_ = PosEmbed ([ **H** _plan_ ; _V_ [ _y_ 0: _j−_ 1]) _∈_ R [(][length][(] **[H]** _[plan]_ [)+] _[j]_ [)] _[×][D]_ _,_ (3)


where _V_ is a learnable codebook and _y_ 0: _j−_ 1 are previously generated trajectory token IDs. The
decoder applies stacked causal self-attention layers to predict the next token _yj_ via a linear projection
layer, enabling temporal modeling both within and across shots for cinematic continuity. This process
ultimately generates a trajectory token sequence **S** [ˆ] _traj_ = _{y_ ˆ _j}_ _[N]_ _j_ =1 [+2][, where] _[ N]_ [is the variable trajectory]
sequence length, with two special tokens for beginning and ending.


_**Training Objective.**_ We optimize the VLM parameters (via LoRA [26]) and the Decoder using:


_Lplan_ = CrossEntropy( **S** _traj,_ **S** [ˆ] _traj_ ) + _λ∥_ **H** _plan∥_ [2] 2 _[,]_ (4)


where the second term applies L2 regularization to the latent code **H** _plan_ to prevent overfitting and
ensure representation compactness.


**3.2** **Controller:** **Cinematic Camera Control for Text-Driven Multi-Shot Video Generation**


_**Motivation.**_ While the Planner provides precise geometric instructions, executing them poses a
significant challenge: complex multi-shot cinematic trajectories (e.g., rapid cuts, variable-speed
tracking) represent unseen patterns for pre-trained video models. Consequently, fine-tuning is
essential to bridge this domain gap. However, naive fine-tuning often degrades visual quality or fails
to capture the sharp temporal boundaries of cuts.


_**Overview.**_ To address these challenges, we propose a trajectory-conditioned Controller. We employ
the holistic multi-shot HoloCine [41] foundation model for video synthesis. To advance its camera
control, we employ a lightweight fine-tuning strategy (via LoRA) to adapt the model to new control
signals and patterns. Our architecture adaptation is designed with two guiding principles: (i) a
“simple-yet-effective” injection mechanism via a Camera Encoder that enforces geometric adherence
without disrupting pre-trained priors; and (ii) a shot-aware structural bias via 4D Rotary Positional
Embedding that explicitly informs the model of hierarchical boundaries. Finally, we optimize the
controller using a Flow Matching objective.


5


_**Camera**_ _**Encoder.**_ We implement a direct feature injection mechanism [3] to guide the camera
trajectory understanding of the model. Specifically, for each frame _t_, the extrinsic matrix **E** _t_ _∈_ R [3] _[×]_ [4]
is first flattened and projected to match the video token channels _d_ via a learnable Camera Encoder
_Ec_ (instantiated as a Fully Connected Layer), **c** _cam_ = _Ec_ (Flatten( **E** _t_ )) _∈_ R _[d]_ . To achieve fine-grained
control, this encoder is inserted into each transformer block. We directly add the camera embedding to
the intermediate visual features. Specifically, let **F** _norm_ denote the features after layer normalization
and adaptive modulation. The input features, **F** _attnin_, for the self-attention layer are computed as:
**F** _attnin_ = **F** _norm_ + **c** _cam_ . By injecting the trajectory signal **c** _cam_ right before the self-attention
layer, we explicitly condition the temporal modeling process on the target camera pose, ensuring the
generated motion dynamics align with the camera condition. While direct injection proves effective
in video-to-video settings [3] with synthetic data, applying it to text-driven generation risks texture
distribution drift. We resolve this via our data-centric foundation: by training on the real-world
_**ShotVerse-Bench**_ dataset, we ensure the model aligns camera control with natural cinematic textures.


_**4D Rotary Positional Embedding.**_ Standard video generation models typically utilize 3D positional
embeddings (i.e., frame, height, width). However, multi-shot videos possess a hierarchical temporal
structure (i.e., video _→_ shot _→_ frame). To explicitly inform the model about shot boundaries and
enforce intra-shot consistency, we propose a 4D Rotary Positional Embedding (4D RoPE) strategy.
As detailed in **Appendix Algorithm 1**, the process operates in three streamlined steps: (i) _Dimension_
_Allocation._ We partition the attention head dimension into four subspaces: _Fshot, Fframe, Fh, Fw,_ .
We allocate a larger proportion to spatial dimensions ( _Fh, Fw_ ) to preserve visual fidelity, while
reserving sufficient capacity in _Fshot_ and _Fframe_ for hierarchical temporal modeling. (ii) _Frequency_
_Pre-Computation._ Independent rotary frequency banks are pre-calculated for each dimension following the standard RoPE formulation. This creates orthogonal positional bases for height, width,
shot index, and frame index. (iii) _Dynamic Assembly._ During the forward pass, we dynamically map
each video frame to its corresponding shot index _s_ and global frame index _t_ . The final embedding is
assembled by concatenating the frequency components from all subspaces. Crucially, this mechanism
ensures that all frames within the same shot share a unified shot embedding, explicitly enforcing
intra-shot consistency while time handles fine-grained temporal dynamics.


_**Training Objective.**_ Following the HoloCine training protocol, we employ the Flow Matching [39]
objective. Given a clean video latent **v** 0 and a Gaussian noise sample **v** 1 _∼N_ ( **0** _,_ **I** ), we interpolate
between them to obtain **v** _σ_ = (1 _−_ _σ_ ) **v** 0 + _σ_ **v** 1 at noise level _σ_ _∈_ [0 _,_ 1]. The model _vθ_ is trained to
predict the velocity field **u** = **v** 1 _−_ **v** 0. The training objective is formulated as follows:


_Lcontrol_ = E _σ,_ **v** 0 _,_ **v** 1            - _∥vθ_ ( **v** _σ, σ,_ **c** _text,_ **c** _cam_ ) _−_ ( **v** 1 _−_ **v** 0) _∥_ [2] 2� _,_ (5)
where **c** _text_ represents the textual embeddings extracted by the text encoder, and **c** _cam_ denotes the
explicit camera condition embeddings.


**4** **Dataset and Benchmark:** _**ShotVerse-Bench**_


**4.1** **Dataset Curation**


_**Dataset Overview.**_ A core challenge in camera-controlled multi-shot cinematic video generation is
the lack of data that aligns semantic descriptions with globally unified camera trajectory annotations.
To address this, we construct a dataset, _**ShotVerse-Bench**_, featuring hierarchical captions and unified
multi-shot trajectories (Tab. 1). We collect 20,500 clips from high-production cinema, ensuring that
the content adheres to professional cinematic standards and cinematography principles, which covers
a broad and balanced taxonomy of camera control.


_**Multi-Shot**_ _**Camera**_ _**Calibration.**_ To align disjoint single-shot trajectories into a unified global
coordinate system, we propose a four-step calibration pipeline, as detailed in **Appendix Algorithm**
**2** . (i) _Dynamic_ _Foreground_ _Removal._ To address the dynamic objects, we employ SAM [45] to
mask foregrounds, retaining static background regions for robust pose estimation. (ii) _Single-Shot_
_Local Reconstruction._ We then independently reconstruct each shot _s_ using PI3 [51] on the static
background, producing a locally consistent trajectory within a shot-specific local frame. (iii) _Joint_
_Keyframe Global Reconstruction._ We sample keyframes across disjoint shots and reconstruct them
jointly via PI3. This yields a unified static scene and global poses, naturally defining a global
coordinate system for the entire multi-shot sequence. (iv) _Anchor-Based_ _Trajectory_ _Alignment._
To unify trajectories, we identify an anchor frame for each shot present in both local and global


6


Table 1: **Comparisons of Camera Trajectory Datasets.** _**ShotVerse-Bench**_ is the first large-scale
dataset that provides multi-shot cinematic camera trajectories together with rich, multi-level caption
annotations.


Caption Annotation Statistics
Dataset Traj Type Domain

Traj Scene Intent #Vocab #Sample #Frame


MVImgNet [57] _×_ _×_ _×_  - Object/Scene-Centric Captured 22K 6.5M
RealEstate10k [65] _×_ _×_ _×_  - Object/Scene-Centric Youtube 79K 11M
DL3DV-10K [37] _×_ _×_ _×_  - Object/Scene-Centric Captured 10K **51M**
CCD [29] ✓ _×_ _×_ 48 Tracking Synthetic 25K 4.5M
E.T. [11] ✓ _×_ _×_ 1790 Tracking Film **115K** 11M
GenDoP [59] ✓ ✓ ✓ 8698 Free-Moving Film 29K 11M
ShotVerse-Bench (Ours) ✓ ✓ ✓ **19819** Free-Moving& **Multi-Shot** Film/ **TV** / **Documentary** 20.5K 12M


reconstructions, yielding dual pose references. We estimate a similarity transformation to align the
local frame to the global system, resolving scale ambiguity by comparing the relative displacements
of the shot’s start and end keyframes.


_**Training and Test.**_ To construct multi-shot training data from the single-shot clips, we assemble
multi-shot sequences of 249 frames. We select 2,750 representative single-shot clips and group them
into 1,100 multi-shot scenes, each containing 2, 3, or 4 shots following a 6:3:1 ratio. After removing
embedded subtitles and standardizing resolution to 843 _×_ 480, we allocate 1,000 scenes for training
and 100 for testing with no scene overlap.


**4.2** **Evaluation Benchmark:** **A Three-Track Protocol**


Our target task is _text-driven cinematic multi-shot video creation with explicit, globally unified camera_
_control_, which requires models to jointly solve trajectory planning and faithful execution. To our
knowledge, this task has not been systematically evaluated by prior benchmarks; therefore, we
introduce a three-track protocol for comprehensive evaluation at both component and system levels,
by separately measuring (A) text-to-trajectory planning, (B) trajectory-to-video execution fidelity,
and (C) end-to-end text-to-video generation quality.


_**Track A: Text-to-Trajectory.**_ This track evaluates the Planner’s ability to translate narrative intent
into explicit camera trajectories. (i) _Input/Output_ : Hierarchical prompts _→_ Globally aligned camera
sequences. (ii) _Alignment_ _Metrics_ : We adopt _F1-Score_ for discrete motion tag alignment and
_CLaTr-CLIP_ [59] for soft semantic alignment.


_**Track B: Trajectory-to-Video.**_ This track assesses the Controller’s execution fidelity given groundtruth trajectories. (i) _Input/Output_ : Trajectories + Prompts _→_ Multi-shot video. (ii) _Control Accuracy_ :
We use PI3 [51] to extract poses from generated videos and compute _Transition Error_ and _Rota-_
_tion Error_ against ground truth. (iii) _Coordinate Alignment_ : We further introduce the _Coordinate_
_Alignment Score_ (CAS), which selects cross-shot frame pairs with the highest field-of-view overlap
and measures their visual consistency via DINOv2 [43] similarity—if the coordinate system is well
unified, frames with higher geometric overlap are expected to exhibit higher visual similarity.


_**Track C: Text-to-Video.**_ This track measures the end-to-end performance of integrated planning and
execution. (i) _Input/Output_ : Hierarchical prompts _→_ Multi-shot video. (ii) _Semantic Consistency_ :
We assess _Global and_ _Shot-level_ _Consistency_ via pairwise ViCLIP [50] embeddings. (iii) _Visual_
_Quality_ : We report _Aesthetic Quality_ (LAION predictor [33]), _Shot Transition Accuracy_ for temporal
cut precision, and _FVD_ for temporal coherence. (iv) _Cinematic Planning Quality_ : We conduct VLMbased (Gemini 3 Pro[19]) and user studies across four dimensions: _Motion Type Appropriateness_,
_Motion Duration Appropriateness_, _Subject Emphasis & Saliency_, and _Cinematic Pacing_ .


**4.3** **Baseline Selection**


We compare _ShotVerse_ against: (i) _Trajectory_ _Planners_ _(Track_ _A):_ We compare with representative camera trajectory generation methods, including CCD [29], E.T. [11], Director3D [35], and
GenDoP [59]. Among them, GenDoP serves as the strongest autoregressive trajectory generation
baseline. For multi-shot evaluation, these methods are applied under the same hierarchical prompt
setting for fair comparison. (ii) _Camera-Controlled Baselines (Track B):_ We evaluate state-of-the-art
single-shot control models, including CameraCtrl [23], MotionCtrl [52], and ReCamMaster [3]. To


7


Shot 1 Shot 2







CameraCtrl


MotionCtrl


ReCamMaster


HoloCine


MultiShot

Master


Sora2


VEO3


Kling3.0


Seedance2.0


ShotVerse

(Ours)


Figure 3: **Comparisons with the State-of-the-Art Baseline Methods.** Early camera-controlled
text-driven generation models (e.g., CameraCtrl, MotionCtrl) struggle to handle complex cinematic
camera trajectories. ReCamMaster executes the trajectory but drifts away from the subject in Shot
1. HoloCine, MultiShotMaster, Sora2, VEO3, and Kling3.0, and Seedance2.0 fail to execute the
complex “orbit” command, remaining nearly static. These failures demonstrate that for text-driven
models, scaling up caption density is insufficient to achieve precise control without explicit geometric
guidance.


adapt them for multi-shot evaluation, we apply these models shot-by-shot and concatenate the results
using our proposed calibration pipeline for alignment. (iii) _Multi-Shot_ _Video_ _Models_ _(Track_ _C):_
(iii-a) _Open-Source Models_ : We compare against HoloCine [41] and MultiShotMaster [49]. (iii-b)
_Closed-Source Models_ : We include leading closed-source models, which are Sora2 [42], VEO3 [20],
Kling3.0 [31], and Seedance2.0 [18]. As these models rely on implicit textual control, we provide
them with our hierarchical prompts to evaluate their zero-shot cinematic understanding.


**5** **Experiments**


**5.1** **Implementation Details**


The Planner integrates a Qwen3-VL-2B backbone with an OPT-based decoder (12 layers), utilizing
LoRA ( _r_ = 32) and discrete tokenization ( _B_ = 256) for trajectory synthesis. Inference employs
Nucleus sampling ( _τ_ = 0 _._ 9 _, p_ = 0 _._ 95). The Controller adapts HoloCine via rank-128 LoRA and a
fully-connected camera encoder. Following the Wan 2.2 protocol [47], we employ a critical two-stage
training strategy: the camera encoder is optimized only during the high-noise stage (0 _._ 875 _≤_ _σ_ _≤_ 1)


8


Table 2: **Track** **A:** **Quantitative** **Evaluation** **of** **Text-**
**Trajectory Alignment.**


**Method** **Dataset** DataDoP [59] ShotVerse-Bench

F1-Score _↑_ CLaTr-CLIP _↑_ F1-Score _↑_ CLaTr-CLIP _↑_


CCD [29] Pre-Trained 0.315 4.247 0.323 7.032
E.T. [11] Pre-Trained 0.319 0.000 0.289 2.462
Director3D [35] Pre-Trained 0.126 0.000 0.162 1.237
GenDoP [59] Pre-Trained 0.399 32.408 0.326 23.089
GenDoP [59] ShotVerse-Bench 0.268 24.132 0.343 33.875
ShotVerse (Ours) ShotVerse-Bench **0.418** **34.907** **0.422** **35.016**



Table 3: **Track B: Quantitative Evalu-**
**ation of Camera Control.** All methods
receive ground-truth trajectories.


Method Trans. Error _↓_ Rotation Error _↓_ CAS _↑_


MotionCtrl [52] 0.0900 2.56 0.329
CameraCtrl [23] 0.0571 1.28 0.343
ReCamMaster [3] 0.0589 1.12 0.408
ShotVerse (Ours) **0.0163** **0.73** **0.500**



Table 4: **Track** **C:** **Quantitative** **Evaluation**
**of Multi-Shot Quality.** Without shot-splitting,
shot metrics cannot be calculated for some baselines.


Method Sem.(Global)Consist. _↑_ Sem.(Shot)Consist. _↑_ AestheticQuality _↑_ Shot Trans.Accuracy _↑_ FVD _↓_


HoloCine [41] 0.297 0.254 4.981 0.645 407.54
MultiShotMaster [49] 0.279 0.247 5.210 0.927 440.78
Sora2 [42] 0.297  - 5.344  - 372.13
VEO3 [20] 0.282 - 5.441 - 941.50
Kling3.0 [31] 0.288  - 5.167  - 719.44
Seedance2.0 [18] 0.285  - 5.381  - 605.17
ShotVerse (Ours) **0.299** **0.255** **5.465** **0.933** **281.71**



Table 5: **Track** **C:** **Quantitative** **Evaluation** **of**
**Cinematic Quality.**


Method AppropriatenessMotion Type _↑_ AppropriatenessMotion Duration _↑_ Subject Emphasis& Saliency _↑_ CinematicPacing _↑_


HoloCine [41] 4.324 4.281 3.997 3.208
VEO3 [20] 4.402 4.189 4.252 3.288
VLM-Based Sora2 [42] 4.371 4.258 3.892 3.236
Kling3.0 [31] 4.302 4.153 3.872 3.108
Seedance2.0 [18] 4.402 4.279 4.328 3.279
ShotVerse (Ours) **4.447** **4.304** **4.426** **3.384**


HoloCine [41] 2.555 2.615 2.585 2.545
VEO3 [20] 3.564 3.892 3.649 3.561
User Study Sora2 [42] 3.665 3.645 3.865 3.625
Kling3.0 [31] 3.702 3.572 3.598 3.539
Seedance2.0 [18] 3.987 3.820 3.703 3.974
ShotVerse (Ours) **4.105** **4.060** **4.240** **4.055**



to anchor coarse motion, while the low-noise stage refines details via LoRA only. Optimization uses
AdamW (learning rate = 10 _[−]_ [4] ) on 96 NVIDIA H20 GPUs with FSDP [62].


**5.2** **Benchmark Results**


Results follow the three-track protocol (Sec.4.2), focusing on alignment, control, and cinematic
quality. Recognizing that numerical trajectory metrics often fail to reflect the actual cinematographic
experience, we emphasize the evaluation of rendered video outputs. We employ a dual-pronged
assessment strategy combining VLM-based scoring (Gemini 3 Pro[19]) with diverse human user
studies.


_**Track**_ _**A:**_ _**Text-to-Trajectory.**_ Tab. 2 compares our Planner against CCD [29], E.T. [11], Director3D [35], and GenDoP [59]. CCD, E.T., and Director3D underperform significantly, indicating
that existing trajectory generation methods struggle with complex, especially multi-shot, narrative
prompts. GenDoP, the strongest baseline, achieves competitive results on its native DataDoP benchmark but suffers a notable domain gap when re-trained on _ShotVerse-Bench_ . Our VLM-driven Planner
achieves the best results on both benchmarks, demonstrating stronger cross-domain generalization
from the vision-language backbone.


_**Track B: Trajectory-to-Video.**_ Tab. 3 compares camera control fidelity given ground-truth trajectories.
Single-shot baselines MotionCtrl [52] and CameraCtrl [23] exhibit high trajectory errors due to
the lack of cross-shot coordination. ReCamMaster [3] reduces rotation error but still suffers from
coordinate misalignment across shots. Our Controller achieves the lowest errors on both translation
and rotation, and the highest CAS, suggesting stronger cross-shot consistency under our CAS proxy.


_**Track C: Text-to-Video.**_ Tab. 4, Tab. 5, and Fig. 3 report end-to-end results. Our method achieves
the lowest FVD and highest Aesthetic Quality (5.465), outperforming both open-source and commercial baselines. Notably, commercial models achieve competitive aesthetics but suffer from
significantly higher FVD, indicating poor temporal fidelity without explicit trajectory guidance. For
Shot Transition Accuracy, HoloCine (0.645) reflects the limitation of standard 3D positional encoding,
MultiShotMaster (0.927) benefits from improved positional encoding, and our 4D RoPE further
raises the score to 0.933 by explicitly modeling shot indices. For cinematic quality (Tab. 5), both
VLM-based and user study evaluations confirm our method leads across all four dimensions, with
particularly strong gains in Subject Emphasis & Saliency and Cinematic Pacing.


**5.3** **Ablation Study**


_**Planner.**_ To analyze the contribution of the trajectory Planner, we conduct three structural ablations
(Tab. 6). (i) _VLM_ _encoder_ _provides_ _strong_ _spatial_ _priors_ : Replacing the VLM backbone with
the original shallow encoder adopted in GenDoP (i.e., _w/o_ _VLM_ _encoder_ ) leads to consistent


9


|(a) Ablation Study of Camera Encoder<br>w/o<br>Camera<br>Encoder<br>(HoloCine)<br>with<br>Camera<br>Encoder<br>(Ours)|(d) Ablation Study of Camera Calibration<br>w/o<br>Camera<br>Calibration<br>with<br>Camera<br>Calibration<br>(Ours)|
|---|---|
|**(b) Ablation Study of Camera Encoder Training Strategy**<br>with only<br>High-Noise<br>(Ours)<br>with<br>High-Noise<br>& Low-Noise|**(e) Ablation Study of Dataset**<br>Synthetic<br>Dataset<br>ShotVerse-<br>Bench<br>(Ours)|
|**(c) Ablation Study of Positional Embedding**<br>4D RoPE<br>(Ours)<br>3D RoPE<br>**Shot 1**<br>**Shot 2**|**(c) Ablation Study of Positional Embedding**<br>4D RoPE<br>(Ours)<br>3D RoPE<br>**Shot 1**<br>**Shot 2**|


Figure 4: **Qualitative Ablation Study.** (a) Camera encoder is vital for viewpoint grounding; without
it, the model fails to maintain subject orientation ( _e.g._, frontal faces). (b) High-noise pose injection
already establishes the global motion scaffold, while adding low-noise injection yields marginal
gains. (c) 4D RoPE ensures better shot-cutting stability over 3D RoPE. (d) Without calibration,
the camera/trajectory is not globally aligned across shots, causing inaccurate subject tracking. (e)
Training on synthetic triplets further makes both the character and the environment look synthetic,
and the domain gap to real videos degrades visual quality and temporal stability.


Table 6: **Quantitative Evaluation of Ablation Study (Planner).**


degradation in both F1-Score and CLaTr-CLIP (Tab. 6). VLM semantic-spatial priors are vital
for multi-shot camera semantics; omitting them compromises the Planner’s narrative alignment
and degrades trajectory-text consistency. (ii) _Dedicated trajectory decoder is necessary_ : Directly
adopting the VLM’s native decoder to autoregressively generate trajectory tokens significantly
degrades performance. Our shot-aware Transformer decoder avoids the structural inefficiency of
naive language modeling, ensuring stable long-horizon prediction through explicit temporal modeling.
(iii) _Query tokens enable shot-aware planning_ : Removing the learnable trajectory query tokens (i.e.,
_w/o Query Tokens_ ) and directly feeding the VLM encoder outputs to the decoder reduces F1-Score
and CLaTr-CLIP. Query tokens act as structured “planning slots” to disentangle per-shot reasoning;
without them, shared representations entangle semantics with geometry, compromising shot-specific
control and alignment.


_**Controller.**_ ShotVerse’s gains come from (i) Controller-specific designs and (ii) curated data, instead
of the video foundation model. (i-a) _Camera encoder is necessary for controllability_ : Fig. 4 (a) shows
that without the camera encoder (i.e., HoloCine), the model follows the intended motion pattern less
reliably, whereas adding the encoder yields clearer, more stable camera behavior. (i-b) _High-noise-_
_only injection is sufficient_ : Fig. 4 (b) and Tab. 7 indicate that adding an additional low-noise encoder
slightly trades off perceptual quality, implying early (high-noise) pose injection already establishes
the global motion scaffold. (i-c) _4D RoPE captures shot hierarchy_ : Replacing 4D RoPE with 3D
RoPE significantly degrades Shot Transition Accuracy from 0.933 to 0.429 (Tab. 7), demonstrating
that the explicit shot axis is critical for respecting shot boundaries. The ablation also changes the
behavior around shot boundaries (Fig. 4 (c)) and shifts the consistency/semantics trade-off, supporting
that 4D RoPE helps preserve intra-shot coherence while respecting multi-shot structure. (ii-d) _Unified_
_camera calibration is necessary_ : Removing global calibration reduces inter-shot consistency and
aesthetics (Fig. 4 (d)), supporting that unified coordinates are important for geometrically consistent
pose conditioning across cuts. (ii-e) _Synthetic supervision hurts film-like rendering_ : Aesthetics drops
noticeably and semantics slightly weakens (Tab. 7), suggesting real cinematic triplets provide crucial
cues beyond what synthetic triplets capture (Fig. 4 (e)).


10


Table 7: **Quantitative Evaluation of Ablation Study (Controller).**


Method Trans. Error _↓_ Rotation Error _↓_ Shot Trans. Acc. _↑_ Sem. Consist. (Global) _↑_ Sem. Consist. (Shot) _↑_ Aesthetic Quality _↑_


w/o Cam. Enc. (HoloCine) 0.0609 1.27 0.645 0.297 0.254 4.981
w/ Low&High Noise Enc. 0.0189 0.74 0.930 0.296 0.250 5.321
w/ 3D RoPE 0.0323 1.04 0.429 0.290 0.251 5.413
w/ Synthetic Data 0.0509 1.35 0.705 0.292 0.253 4.833
w/o Camera Calibration 0.0165 0.79 0.931 0.296 0.251 5.136
ShotVerse (Ours) **0.0163** **0.73** **0.933** **0.299** **0.255** **5.465**


**6** **Conclusions**


In this work, we have pioneered a data-centric shift in the landscape of cinematic, multi-shot video
generation. By introducing _**ShotVerse**_, we bridge the long-standing gap between high-level narrative
intent and low-level geometric precision, moving beyond simple video synthesis toward professional
cinematographic orchestration. Our “Plan-then-Control” framework demonstrates that the complex
spatial logic required for multi-shot storytelling can be effectively decoupled into a VLM-driven
cognitive plotting phase and a geometry-aware rendering phase. Central to this breakthrough is the
curation of _**ShotVerse-Bench**_ . By establishing a novel calibration pipeline that unifies disjoint shot
trajectories into a global coordinate system, we provide the community with the first high-fidelity
dataset capable of teaching AI the “grammar of film”. Our extensive evaluation, conducted via a
rigorous three-track protocol, confirms that _**ShotVerse**_ not only achieves state-of-the-art technical
accuracy but also manifests a profound implicit understanding of cinematic pacing and visual salience.


_**Limitations and Future Work.**_ Beyond establishing state-of-the-art performance, our comprehensive
error analysis yields three critical insights. (i) _Semantic-Geometric_ _Synergy:_ We uncover a vital
synergy in shot-reverse-shot scenarios where textual priors effectively compensate for calibration
noise. However, minor drifts in long-context recurring views persist, signaling that achieving pixelperfect scene persistence remains an open challenge. (ii) _Holistic Controllability vs._ _Scalability:_
Our work focuses solely on advancing camera controllability in multi-shot video within the **same**
scene. We validate that the holistic paradigm’s “God-view” controllability is currently optimal for
scene-level cinematic planning. Yet, its inherent duration limits and rigid cut points necessitate
future work on extending this precision to multi-scene, infinite-length generation. (iii) _Asymmetric_
_Generalization:_ While the model adapts surprisingly well to atmospheric shots, it struggles with
high-density crowd dynamics.


**References**


[1] Sherwin Bahmani, Ivan Skorokhodov, Guocheng Qian, Aliaksandr Siarohin, Willi Menapace,
Andrea Tagliasacchi, David B Lindell, and Sergey Tulyakov. Ac3d: Analyzing and improving
3d camera control in video diffusion transformers. _arXiv preprint arXiv:2411.18673_, 2024.


[2] Sherwin Bahmani, Ivan Skorokhodov, Aliaksandr Siarohin, Willi Menapace, Guocheng Qian,
Michael Vasilkovsky, Hsin-Ying Lee, Chaoyang Wang, Jiaxu Zou, Andrea Tagliasacchi, et al.
Vd3d: Taming large video diffusion transformers for 3d camera control. _arXiv_ _preprint_
_arXiv:2407.12781_, 2024.


[3] Jianhong Bai, Menghan Xia, Xiao Fu, Xintao Wang, Lianrui Mu, Jinwen Cao, Zuozhu Liu,
Haoji Hu, Xiang Bai, Pengfei Wan, et al. Recammaster: Camera-controlled generative rendering
from a single video. _arXiv preprint arXiv:2503.11647_, 2025.


[4] Jianhong Bai, Menghan Xia, Xintao Wang, Ziyang Yuan, Zuozhu Liu, Haoji Hu, Pengfei Wan,
and Di ZHANG. Syncammaster: Synchronizing multi-camera video generation from diverse
viewpoints. In _The Thirteenth International Conference on Learning Representations_, 2025.


[5] Shuai Bai, Yuxuan Cai, Ruizhe Chen, Keqin Chen, Xionghui Chen, Zesen Cheng, Lianghao
Deng, Wei Ding, Chang Gao, Chunjiang Ge, Wenbin Ge, Zhifang Guo, Qidong Huang, Jie
Huang, Fei Huang, Binyuan Hui, Shutong Jiang, Zhaohai Li, Mingsheng Li, Mei Li, Kaixin
Li, Zicheng Lin, Junyang Lin, Xuejing Liu, Jiawei Liu, Chenglong Liu, Yang Liu, Dayiheng
Liu, Shixuan Liu, Dunjie Lu, Ruilin Luo, Chenxu Lv, Rui Men, Lingchen Meng, Xuancheng
Ren, Xingzhang Ren, Sibo Song, Yuchong Sun, Jun Tang, Jianhong Tu, Jianqiang Wan, Peng


11


Wang, Pengfei Wang, Qiuyue Wang, Yuxuan Wang, Tianbao Xie, Yiheng Xu, Haiyang Xu, Jin
Xu, Zhibo Yang, Mingkun Yang, Jianxin Yang, An Yang, Bowen Yu, Fei Zhang, Hang Zhang,
Xi Zhang, Bo Zheng, Humen Zhong, Jingren Zhou, Fan Zhou, Jing Zhou, Yuanzhi Zhu, and
Ke Zhu. Qwen3-vl technical report. _arXiv preprint arXiv:2511.21631_, 2025.


[6] James F. Blinn. Where am i? what am I looking at? [cinematography]. _IEEE_ _Computer_
_Graphics and Applications_, 8(4):76–81, 1988.


[7] Rogerio Bonatti, Wenshan Wang, Cherie Ho, Aayush Ahuja, Mirko Gschwindt, Efe Camci,
Erdal Kayacan, Sanjiban Choudhury, and Sebastian A. Scherer. Autonomous aerial cinematography in unstructured environments with learned artistic decision-making. _J. Field Robotics_, 37
(4):606–641, 2020.


[8] Shengqu Cai, Ceyuan Yang, Lvmin Zhang, Yuwei Guo, Junfei Xiao, Ziyan Yang, Yinghao Xu,
Zhenheng Yang, Alan L. Yuille, Leonidas J. Guibas, Maneesh Agrawala, Lu Jiang, and Gordon
Wetzstein. Mixture of contexts for long video generation. _ArXiv_, abs/2508.21058, 2025. URL
`[https://api.semanticscholar.org/CorpusID:280950315](https://api.semanticscholar.org/CorpusID:280950315)` .


[9] Zhongang Cai, Ruisi Wang, Chenyang Gu, Fanyi Pu, Junxiang Xu, Yubo Wang, Wanqi Yin,
Zhitao Yang, Chen Wei, Qingping Sun, et al. Scaling spatial intelligence with multimodal
foundation models. _arXiv preprint arXiv:2511.13719_, 2025.


[10] An-Chieh Cheng, Hongxu Yin, Yang Fu, Qiushan Guo, Ruihan Yang, Jan Kautz, Xiaolong
Wang, and Sifei Liu. Spatialrgpt: Grounded spatial reasoning in vision-language models.
_Advances in Neural Information Processing Systems_, 37:135062–135093, 2024.


[11] Robin Courant, Nicolas Dufour, Xi Wang, Marc Christie, and Vicky Kalogeiton. E.T. the
exceptional trajectories: Text-to-camera-trajectory generation with character awareness. In
_ECCV_ _(4)_, volume 15062 of _Lecture_ _Notes_ _in_ _Computer_ _Science_, pages 464–480. Springer,
2024.


[12] Zahra Dehghanian, Morteza Abolghasemi, Hamid Beigy, and Hamid R. Rabiee. Cinelog: A
training free approach for cinematic long video generation, 2025. URL `[https://arxiv.org/](https://arxiv.org/abs/2512.12209)`
`[abs/2512.12209](https://arxiv.org/abs/2512.12209)` .


[13] Nianchen Deng, Lixin Gu, Shenglong Ye, Yinan He, Zhe Chen, Songze Li, Haomin Wang,
Xingguang Wei, Tianshuo Yang, Min Dou, et al. Internspatial: A comprehensive dataset for
spatial reasoning in vision-language models. _arXiv preprint arXiv:2506.18385_, 2025.


[14] Ali Dorri, Salil S Kanhere, and Raja Jurdak. Multi-agent systems: A survey. _Ieee Access_, 6:
28573–28593, 2018.


[15] Steven Mark Drucker, Tinsley A. Galyean, and David Zeltzer. CINEMA: A system for procedural camera movements. In _SI3D_, pages 67–70. ACM, 1992.


[16] Xiao Fu, Shitao Tang, Min Shi, Xian Liu, Jinwei Gu, Ming-Yu Liu, Dahua Lin, and Chen-Hsuan
Lin. Plenoptic video generation, 2026. URL `[https://arxiv.org/abs/2601.05239](https://arxiv.org/abs/2601.05239)` .


[17] Quentin Galvane, Marc Christie, Christophe Lino, and Rémi Ronfard. Camera-on-rails: automated computation of constrained camera paths. In _MIG_, pages 151–157. ACM, 2015.


[18] Yu Gao, Haoyuan Guo, Tuyen Hoang, Weilin Huang, Lu Jiang, Fangyuan Kong, Huixia Li,
Jiashi Li, Liang Li, Xiaojie Li, et al. Seedance 1.0: Exploring the boundaries of video generation
models. _arXiv preprint arXiv:2506.09113_, 2025.


[19] Gemini Team, Google. Gemini 3 pro. 2026. URL `[https://gemini.google.com/app](https://gemini.google.com/app)` .


[20] Google Deepmind. Veo3 video model. `[https://deepmind.google/models/veo/](https://deepmind.google/models/veo/)`, 2025.


[21] Yuwei Guo, Ceyuan Yang, Anyi Rao, Zhengyang Liang, Yaohui Wang, Yu Qiao, Maneesh
Agrawala, Dahua Lin, and Bo Dai. Animatediff: Animate your personalized text-to-image
diffusion models without specific tuning. _arXiv preprint arXiv:2307.04725_, 2023.


12


[22] Yuwei Guo, Ceyuan Yang, Ziyan Yang, Zhibei Ma, Zhijie Lin, Zhenheng Yang, Dahua Lin,
and Lu Jiang. Long context tuning for video generation. _ArXiv_, abs/2503.10589, 2025. URL
`[https://api.semanticscholar.org/CorpusID:276961453](https://api.semanticscholar.org/CorpusID:276961453)` .


[23] Hao He, Yinghao Xu, Yuwei Guo, Gordon Wetzstein, Bo Dai, Hongsheng Li, and Ceyuan
Yang. Cameractrl: Enabling camera control for text-to-video generation. _arXiv_ _preprint_
_arXiv:2404.02101_, 2024.


[24] Hao He, Ceyuan Yang, Shanchuan Lin, Yinghao Xu, Meng Wei, Liangke Gui, Qi Zhao, Gordon
Wetzstein, Lu Jiang, and Hongsheng Li. Cameractrl ii: Dynamic scene exploration via cameracontrolled video diffusion models. _arXiv preprint arXiv:2503.10592_, 2025.


[25] Jingwen He, Hongbo Liu, Jiajun Li, Ziqi Huang, Yu Qiao, Wanli Ouyang, and Ziwei Liu.
Cut2next: Generating next shot via in-context tuning. _arXiv preprint arXiv:2508.08244_, 2025.


[26] Edward J Hu, Yelong Shen, Phillip Wallis, Zeyuan Allen-Zhu, Yuanzhi Li, Shean Wang,
Lu Wang, Weizhu Chen, et al. Lora: Low-rank adaptation of large language models. _ICLR_, 1
(2):3, 2022.


[27] Chong Huang, Chuan-En Lin, Zhenyu Yang, Yan Kong, Peng Chen, Xin Yang, and Kwang-Ting
Cheng. Learning to film from professional human motion videos. In _CVPR_, pages 4244–4253.
Computer Vision Foundation / IEEE, 2019.


[28] Weinan Jia, Yuning Lu, Mengqi Huang, Hualiang Wang, Binyuan Huang, Nan Chen, Mu Liu,
Jidong Jiang, and Zhendong Mao. Moga: Mixture-of-groups attention for end-to-end long video
generation, 2025. URL `[https://arxiv.org/abs/2510.18692](https://arxiv.org/abs/2510.18692)` .


[29] Hongda Jiang, Xi Wang, Marc Christie, Libin Liu, and Baoquan Chen. Cinematographic camera
diffusion model. _Comput. Graph. Forum_, 43(2):i–iii, 2024.


[30] Ozgur Kara, Krishna Kumar Singh, Feng Liu, Duygu Ceylan, James M Rehg, and Tobias Hinz.
Shotadapter: Text-to-multi-shot video generation with diffusion models. In _Proceedings of the_
_Computer Vision and Pattern Recognition Conference_, pages 28405–28415, 2025.


[31] Kuaishou. Kling video model. `[https://kling.kuaishou.com](https://kling.kuaishou.com)`, 2025.


[32] Zhengfei Kuang, Shengqu Cai, Hao He, Yinghao Xu, Hongsheng Li, Leonidas Guibas, and
Gordon Wetzstein. Collaborative video diffusion: Consistent multi-video generation with
camera control. _arXiv preprint arXiv:2405.17414_, 2024.


[33] LAION-AI. aesthetic-predictor. `[https://github.com/LAION-AI/aesthetic-predictor](https://github.com/LAION-AI/aesthetic-predictor)`,
2022. GitHub repository.


[34] Xiaozhe Li, Kai Wu, Siyi Yang, YiZhan Qu, Guohua Zhang, Zhiyu Chen, Jiayao Li, Jiangchuan
Mu, Xiaobin Hu, Wen Fang, et al. Can video generation replace cinematographers? research on
the cinematic language of generated video. _arXiv preprint arXiv:2412.12223_, 2024.


[35] Xinyang Li, Zhangyu Lai, Linning Xu, Yansong Qu, Liujuan Cao, Shengchuan Zhang, Bo Dai,
and Rongrong Ji. Director3d: Real-world camera trajectory and 3d scene generation from text.
In _NeurIPS_, 2024.


[36] Zhengyang Liang, Daoan Zhang, Huichi Zhou, Rui Huang, Bobo Li, Yuechen Zhang,
Shengqiong Wu, Xiaohan Wang, Jiebo Luo, Lizi Liao, et al. Univa: Universal video agent
towards open-source next-generation video generalist. _arXiv preprint arXiv:2511.08521_, 2025.


[37] Lu Ling, Yichen Sheng, Zhi Tu, Wentian Zhao, Cheng Xin, Kun Wan, Lantao Yu, Qianyu Guo,
Zixun Yu, Yawen Lu, Xuanmao Li, Xingpeng Sun, Rohan Ashok, Aniruddha Mukherjee, Hao
Kang, Xiangrui Kong, Gang Hua, Tianyi Zhang, Bedrich Benes, and Aniket Bera. DL3DV-10K:
A large-scale scene dataset for deep learning-based 3d vision. In _CVPR_, pages 22160–22169.
IEEE, 2024.


[38] Christophe Lino and Marc Christie. Intuitive and efficient camera control with the toric space.
_ACM Trans. Graph._, 34(4):82:1–82:12, 2015.


13


[39] Yaron Lipman, Ricky T. Q. Chen, Heli Ben-Hamu, Maximilian Nickel, and Matt Le. Flow
matching for generative modeling. _ArXiv_, abs/2210.02747, 2022. URL `[https://api.](https://api.semanticscholar.org/CorpusID:252734897)`
`[semanticscholar.org/CorpusID:252734897](https://api.semanticscholar.org/CorpusID:252734897)` .


[40] Xinyi Liu, Tianyi Zhang, Matthew Johnson-Roberson, and Weiming Zhi. Splatraj: Camera
trajectory generation with semantic gaussian splatting. _CoRR_, abs/2410.06014, 2024.


[41] Yihao Meng, Hao Ouyang, Yue Yu, Qiuyu Wang, Wen Wang, Ka Leong Cheng, Hanlin Wang,
Yixuan Li, Cheng Chen, Yanhong Zeng, Yujun Shen, and Huamin Qu. Holocine: Holistic
generation of cinematic multi-shot long video narratives. _arXiv preprint arXiv:2510.20822_,
2025.


[42] OpenAI. Sora2 video model. `[https://openai.com/research/sora-2](https://openai.com/research/sora-2)`, 2025.


[43] Maxime Oquab, Timothée Darcet, Théo Moutakanni, Huy Vo, Marc Szafraniec, Vasil Khalidov,
Pierre Fernandez, Daniel Haziza, Francisco Massa, Alaaeldin El-Nouby, et al. Dinov2: Learning
robust visual features without supervision. _arXiv preprint arXiv:2304.07193_, 2023.


[44] William S. Peebles and Saining Xie. Scalable diffusion models with transformers. _Proceedings_
_of_ _the_ _IEEE/CVF_ _International_ _Conference_ _on_ _Computer_ _Vision_ _(ICCV)_, pages 4172–4182,
2023. URL `[https://api.semanticscholar.org/CorpusID:254854389](https://api.semanticscholar.org/CorpusID:254854389)` .


[45] Nikhila Ravi, Valentin Gabeur, Yuan-Ting Hu, Ronghang Hu, Chaitanya Ryali, Tengyu Ma,
Haitham Khedr, Roman Rädle, Chloe Rolland, Laura Gustafson, Eric Mintun, Junting Pan,
Kalyan Vasudev Alwala, Nicolas Carion, Chao-Yuan Wu, Ross Girshick, Piotr Dollár, and
Christoph Feichtenhofer. Sam 2: Segment anything in images and videos. _arXiv_ _preprint_
_arXiv:2408.00714_, 2024. URL `[https://arxiv.org/abs/2408.00714](https://arxiv.org/abs/2408.00714)` .


[46] Robin Rombach, Andreas Blattmann, Dominik Lorenz, Patrick Esser, and Björn Ommer. Highresolution image synthesis with latent diffusion models. In _Proceedings_ _of_ _the_ _IEEE/CVF_
_conference on computer vision and pattern recognition_, pages 10684–10695, 2022.


[47] Team Wan, Ang Wang, Baole Ai, Bin Wen, Chaojie Mao, Chen-Wei Xie, Di Chen, Feiwu Yu,
Haiming Zhao, Jianxiao Yang, Jianyuan Zeng, Jiayu Wang, Jingfeng Zhang, Jingren Zhou,
Jinkai Wang, Jixuan Chen, Kai Zhu, Kang Zhao, Keyu Yan, Lianghua Huang, Mengyang Feng,
Ningyi Zhang, Pandeng Li, Pingyu Wu, Ruihang Chu, Ruili Feng, Shiwei Zhang, Siyang Sun,
Tao Fang, Tianxing Wang, Tianyi Gui, Tingyu Weng, Tong Shen, Wei Lin, Wei Wang, Wei
Wang, Wenmeng Zhou, Wente Wang, Wenting Shen, Wenyuan Yu, Xianzhong Shi, Xiaoming
Huang, Xin Xu, Yan Kou, Yangyu Lv, Yifei Li, Yijing Liu, Yiming Wang, Yingya Zhang,
Yitong Huang, Yong Li, You Wu, Yu Liu, Yulin Pan, Yun Zheng, Yuntao Hong, Yupeng Shi,
Yutong Feng, Zeyinzi Jiang, Zhen Han, Zhi-Fan Wu, and Ziyu Liu. Wan: Open and advanced
large-scale video generative models. _arXiv preprint arXiv:2503.20314_, 2025.


[48] Qinghe Wang, Yawen Luo, Xiaoyu Shi, Xu Jia, Huchuan Lu, Tianfan Xue, Xintao Wang,
Pengfei Wan, Di Zhang, and Kun Gai. Cinemaster: A 3d-aware and controllable framework for
cinematic text-to-video generation. In _Proceedings of the Special Interest Group on Computer_
_Graphics and Interactive Techniques Conference Conference Papers_, pages 1–10, 2025.


[49] Qinghe Wang, Xiaoyu Shi, Baolu Li, Weikang Bian, Quande Liu, Huchuan Lu, Xintao Wang,
Pengfei Wan, Kun Gai, and Xu Jia. Multishotmaster: A controllable multi-shot video generation
framework. _arXiv preprint arXiv:2512.03041_, 2025.


[50] Yi Wang, Yinan He, Yizhuo Li, Kunchang Li, Jiashuo Yu, Xin Ma, Xinhao Li, Guo Chen,
Xinyuan Chen, Yaohui Wang, et al. Internvid: A large-scale video-text dataset for multimodal understanding and generation. In _The Twelfth International Conference on Learning_
_Representations_, 2023.


[51] Yifan Wang, Jianjun Zhou, Haoyi Zhu, Wenzheng Chang, Yang Zhou, Zizun Li, Junyi Chen,
Jiangmiao Pang, Chunhua Shen, and Tong He. pi3: Permutation-equivariant visual geometry
learning. _arXiv preprint arXiv:2507.13347_, 2025.


[52] Zhouxia Wang, Ziyang Yuan, Xintao Wang, Yaowei Li, Tianshui Chen, Menghan Xia, Ping
Luo, and Ying Shan. Motionctrl: A unified and flexible motion controller for video generation.
In _ACM SIGGRAPH 2024 Conference Papers_, pages 1–11, 2024.


14


[53] Weijia Wu, Zeyu Zhu, and Mike Zheng Shou. Automated movie generation via multi-agent cot
planning, 2025. URL `[https://arxiv.org/abs/2503.07314](https://arxiv.org/abs/2503.07314)` .


[54] Xiaoxue Wu, Xinyuan Chen, Yaohui Wang, and Yu Qiao. Shotdirector: Directorially
controllable multi-shot video generation with cinematographic transitions. _arXiv_ _preprint_
_arXiv:2512.10286_, 2025.


[55] Junfei Xiao, Ceyuan Yang, Lvmin Zhang, Shengqu Cai, Yang Zhao, Yuwei Guo, Gordon
Wetzstein, Maneesh Agrawala, Alan Yuille, and Lu Jiang. Captain cinema: Towards short
movie generation. _arXiv preprint arXiv:2507.18634_, 2025.


[56] Jinbo Xing, Long Mai, Cusuh Ham, Jiahui Huang, Aniruddha Mahapatra, Chi-Wing Fu,
Tien-Tsin Wong, and Feng Liu. Motioncanvas: Cinematic shot design with controllable imageto-video generation. In _Proceedings of the Special Interest Group on Computer Graphics and_
_Interactive Techniques Conference Conference Papers_, pages 1–11, 2025.


[57] Xianggang Yu, Mutian Xu, Yidan Zhang, Haolin Liu, Chongjie Ye, Yushuang Wu, Zizheng
Yan, Chenming Zhu, Zhangyang Xiong, Tianyou Liang, Guanying Chen, Shuguang Cui, and
Xiaoguang Han. Mvimgnet: A large-scale dataset of multi-view images. In _CVPR_, pages
9150–9161. IEEE, 2023.


[58] Kaiwen Zhang, Liming Jiang, Angtian Wang, Jacob Zhiyuan Fang, Tiancheng Zhi, Qing Yan,
Hao Kang, Xin Lu, and Xingang Pan. Storymem: Multi-shot long video storytelling with
memory. _arXiv preprint arXiv:2512.19539_, 2025.


[59] Mengchen Zhang, Tong Wu, Jing Tan, Ziwei Liu, Gordon Wetzstein, and Dahua Lin. Gendop:
Auto-regressive camera trajectory generation as a director of photography. _arXiv_ _preprint_
_arXiv:2504.07083_, 2025.


[60] Susan Zhang, Stephen Roller, Naman Goyal, Mikel Artetxe, Moya Chen, Shuohui Chen,
Christopher Dewan, Mona T. Diab, Xian Li, Xi Victoria Lin, Todor Mihaylov, Myle Ott, Sam
Shleifer, Kurt Shuster, Daniel Simig, Punit Singh Koura, Anjali Sridhar, Tianlu Wang, and Luke
Zettlemoyer. OPT: open pre-trained transformer language models. _CoRR_, abs/2205.01068,
2022.


[61] Yuang Zhang, Junqi Cheng, Haoyu Zhao, Jiaxi Gu, Fangyuan Zou, Zenghui Lu, and Peng Shu.
Shouldershot: Generating over-the-shoulder dialogue videos. _arXiv preprint arXiv:2508.07597_,
2025.


[62] Yanli Zhao, Andrew Gu, Rohan Varma, Liang Luo, Chien-Chin Huang, Min Xu, Less Wright,
Hamid Shojanazeri, Myle Ott, Sam Shleifer, Alban Desmaison, Can Balioglu, Pritam Damania,
Bernard Nguyen, Geeta Chauhan, Yuchen Hao, Ajit Mathews, and Shen Li. Pytorch fsdp:
Experiences on scaling fully sharded data parallel, 2023. URL `[https://arxiv.org/abs/](https://arxiv.org/abs/2304.11277)`
`[2304.11277](https://arxiv.org/abs/2304.11277)` .


[63] Guangcong Zheng, Teng Li, Rui Jiang, Yehao Lu, Tao Wu, and Xi Li. Cami2v: Cameracontrolled image-to-video diffusion model. _arXiv preprint arXiv:2410.15957_, 2024.


[64] Mingzhe Zheng, Yongqi Xu, Haojian Huang, Xuran Ma, Yexin Liu, Wenjie Shu, Yatian
Pang, Feilong Tang, Qifeng Chen, Harry Yang, and Ser-Nam Lim. Videogen-of-thought:
Step-by-step generating multi-shot video with minimal manual intervention, 2025. URL
`[https://arxiv.org/abs/2412.02259](https://arxiv.org/abs/2412.02259)` .


[65] Tinghui Zhou, Richard Tucker, John Flynn, Graham Fyffe, and Noah Snavely. Stereo magnification: learning view synthesis using multiplane images. _ACM Trans. Graph._, 37(4):65,
2018.


[66] Yupeng Zhou, Daquan Zhou, Ming-Ming Cheng, Jiashi Feng, and Qibin Hou. Storydiffusion:
Consistent self-attention for long-range image and video generation. _NeurIPS_, abs/2405.01434,
2024. URL `[https://api.semanticscholar.org/CorpusID:269502120](https://api.semanticscholar.org/CorpusID:269502120)` .


15


**Algorithm 1** 4D Rotary Positional Embedding (4D RoPE)

**Require:** Input latent tensor **X** _∈_ R _[B][×][T][ ×][H]_ _[′][×][W][ ′][×][d]_ ; shot boundaries _S_ = _{s_ 0 _, s_ 1 _, . . ., sN_ _}_ ; base
frequency _θ_ .
**Ensure:** Positionally encoded tensor **X** _[′]_ .

1: **// (i) Dimension Allocation**
2: _dh_ _←⌊d/_ 3 _⌋,_ _dw_ _←⌊d/_ 3 _⌋_
3: _dshot_ _←⌊_ ( _d −_ _dh −_ _dw_ ) _/_ 2 _⌋_
4: _dframe_ _←⌊_ ( _d −_ _dh −_ _dw_ ) _/_ 2 _⌋_
5: **// (ii) Frequency Pre-Computation**
6: **for** _dim ∈{shot, frame, height, width}_ **do**
7: Generate frequencies: **Θ** _dim_ _←{θ_ _[−]_ [2] _[k/d][dim]_ _| k_ _∈_ [0 _, ddim/_ 2) _}_
8: Pre-compute **F** _dim_ : **f** ( _m_ ) = _e_ _[j][·][m][·]_ **[Θ]** _[dim]_

9: **end for**
10: **// (iii) Dynamic Assembly During Forward Pass**
11: **I** _h_ _←_ Range(0 _, H_ _[′]_ ) _,_ **I** _w_ _←_ Range(0 _, W_ _[′]_ )
12: **I** _shot_ _←_ SearchSorted( _S,_ Range(0 _, T_ )) {Map frame _t_ to shot index}
13: **I** _frame_ _←_ Range(0 _, T_ )
14: **E** _shot_ _←_ Gather( **F** _shot,_ **I** _shot_ )
15: **E** _frame_ _←_ Gather( **F** _frame,_ **I** _frame_ )
16: **E** _h_ _←_ Gather( **F** _height,_ **I** _h_ )
17: **E** _w_ _←_ Gather( **F** _width,_ **I** _w_ )
18: **F** 4 _D_ _←_ Concat( **E** _shot,_ **E** _frame,_ **E** _h,_ **E** _w_ )
19: **X** _[′]_ _←_ **X** _·_ **F** 4 _D_ {Element-wise complex multiplication}
20: **return** Real( **X** _[′]_ )


**A** **Appendix**


This appendix includes the two algorithms referenced in the main paper: Algorithm 1 for 4D Rotary
Positional Embedding and Algorithm 2 for multi-shot camera calibration.


16


**Algorithm 2** Multi-Shot Camera Calibration


**Require:** Multi-shot video _V_ with _N_ shots _{S_ 1 _, S_ 2 _, . . ., SN_ _}_ ; pre-trained SAM2 model _Mseg_ ;
pose-informed 3D reconstruction model _MP I_ 3.
**Ensure:** Unified global camera trajectories _{Tglobal_ _[s]_ _[}]_ _s_ _[N]_ =1 [.]
1: **// (i) Dynamic Foreground Removal**
2: **for** each frame _It_ in _V_ **do**
3: Get dynamic mask **M** _t_ _←Mseg_ ( _It_ )
4: Extract static background _It_ _[static]_ _←_ _It ⊙_ (1 _−_ **M** _t_ )
5: **end for**
6: **// (ii) Single-Shot Local Reconstruction**
7: **for** each shot _s ∈{_ 1 _, . . ., N_ _}_ **do**
8: Input intra-shot frames _{It_ _[static]_ _}t∈s_ to _MP I_ 3
9: Estimate local trajectory _Tlocal_ _[s]_ [=] _[ {]_ **[P]** _local,t_ _[s]_ _[}]_ _t_ _[L]_ =1 _[s]_
10: **end for**
11: **// (iii) Joint Keyframe Global Reconstruction**
12: **for** each shot _s ∈{_ 1 _, . . ., N_ _}_ in the same scene **do**
13: Sample keyframes _Ks_ from static frames of shot _Ss_
14: **end for**
15: _K ←_ [�] _[N]_ _s_ =1 _[K][s]_
16: Input _K_ to _MP I_ 3 for joint reconstruction
17: Obtain global poses _{_ **P** _global,k_ _| k_ _∈K}_, defining the world frame _W_
18: **// (iv) Anchor-Based Trajectory Alignment**
19: **for** each shot _s ∈{_ 1 _, . . ., N_ _}_ **do**
20: Identify anchor frames _As_ = _{k_ _| k_ _∈Ks}_
21: Select first anchor _kstart_ and last anchor _kend_ from _As_
22: _dlocal_ _←∥_ trans( **P** _[s]_ _local,kend_ [)] _[ −]_ [trans][(] **[P]** _local,k_ _[s]_ _start_ [)] _[∥]_ [2]
23: _dglobal_ _←∥_ trans( **P** _global,kend_ ) _−_ trans( **P** _global,kstart_ ) _∥_ 2
24: _σs_ _←_ _dglobal/_ max( _dlocal, ϵ_ )
25: **M** _s_ _←_ arg min **T** - _k∈As_ _[∥]_ **[P]** _[global,k][ −]_ **[T]** _[ ·]_ **[ P]** _local,k_ _[s]_ _[∥]_ _F_ [2]

26: _Tglobal_ _[s]_ _[←{]_ **[M]** _[s][ ·]_ **[ P]** _local,t_ _[s]_ _[|]_ **[ P]** _local,t_ _[s]_ _[∈T]_ _local_ _[s]_ _[}]_
27: **end for**
28: **return** Unified trajectories _{Tglobal_ _[s]_ _[}]_ _s_ _[N]_ =1


17


