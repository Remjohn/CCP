## **from Visual Dynamics**

**Xiangbo Gao** [1], **Mingyang Wu** [1], **Siyuan Yang** [1], **Jiongze Yu** [1], **Pardis Taghavi** [1], **Fangzhou Lin** [1], **Zhengzhong Tu** [1] _[,]_ [2]


1Texas A&M University 2Visko Platform


**Abstract.** While recent generative video models have achieved remarkable visual realism and are being
explored as world models, true physical simulation requires mastering both space and time. Current
models can produce visually smooth kinematics, yet they lack a reliable internal motion pulse to
ground these motions in a consistent, real-world time scale. This temporal ambiguity stems from the
common practice of indiscriminately training on videos with vastly different real-world speeds, forcing
them into standardized frame rates. This leads to what we term _chronometric_ _hallucination_ : generated
sequences exhibit ambiguous, unstable, and uncontrollable physical motion speeds. To address this,
we propose Visual Chronometer, a predictor that recovers the Physical Frames Per Second (PhyFPS)
directly from the visual dynamics of an input video. Trained via controlled temporal resampling,
our method estimates the true temporal scale implied by the motion itself, bypassing unreliable
metadata. To systematically quantify this issue, we establish two benchmarks, `PhyFPS-Bench-Real`
and `PhyFPS-Bench-Gen` . Our evaluations reveal a harsh reality: state-of-the-art video generators suffer
from severe PhyFPS misalignment and temporal instability. Finally, we demonstrate that applying
PhyFPS corrections significantly improves the human-perceived naturalness of AI-generated videos.


_“Not_ _only_ _do_ _we_ _measure_ _the_ _movement_ _by_ _the_ _time,_ _but_ _also_ _the_ _time_ _by_ _the_ _movement,_
_because_ _they_ _define_ _each_ _other.”_     - Aristotle, _Physics_


**Project Homepage:** `[https://xiangbogaobarry.github.io/Visual_Chronometer/](https://xiangbogaobarry.github.io/Visual_Chronometer/)`

**Date:** March 30, 2026

**Contact:** Xiangbo Gao [(xiangbogaobarry@gmail.com),](mailto:xiangbogaobarry@gmail.com) Zhengzhong Tu [(tzz@tamu.edu)](mailto:tzz@tamu.edu)

### **1 Introduction**


While modern generative video models excel at spatial realism—producing photorealistic textures, complex
geometry, and coherent layouts [1, 2, 3, 4, 5, 6]—an increasing number aspire to go further and act as physical
world models [7, 8]. However, faithfully simulating the physical world requires an intricate mastery of both
space and time; physical motion is governed by a strict relationship between spatial displacement and elapsed
time, yet today’s video generation pipelines often lack a stable pulse of motion to track this. Consequently,
while modern generators can produce visually fluid kinematics, these motions are rarely grounded in a
consistent, real-world time scale.

Much of this temporal ambiguity stems from the agnostic treatment of time during the training of modern video
models [9]. Internet-scale video datasets are mixtures of varying capture and editing regimes, encompassing
standard-rate footage, extreme slow-motion, and accelerated time-lapses. During training, models are typically
blind to these inherent physical speeds; a time-lapse and a slow-motion video might be fed into the network
identically. This lack of time-scale awareness severs the correspondence between a discrete frame step and the
real-world time elapsed. As a result, models learn to generate plausible frame-to-frame transitions, but the
underlying physical speed of the generated motion becomes ambiguous, unstable, and impossible to explicitly
control. We refer to this prevalent failure mode as **Chronometric Hallucination** (see Figure 1).
Aristotle once observed that “ _not_ _only_ _do_ _we_ _measure_ _the_ _movement_ _by_ _the_ _time,_ _but_ _also_ _the_ _time_ _by_ _the_
_movement,_ _because_ _they_ _define_ _each_ _other._ ” Operationalizing this ancient principle, we introduce **Visual**
**Chronometer**, a predictor designed to alleviate chronometric hallucination by recovering this intrinsic motion


**Figure 1** **Visualization of Chronometric Hallucination.** Current video generators sometimes fail to ground their outputs in a
consistent physical time scale, even when no speed-manipulating keywords (e.g., “slow motion”) are prompted. **(a)** A
hummingbird hawk-moth is rendered in extreme slow-motion, despite its naturally high wing-beat frequency. **(b)** A
person falls onto a bed at a velocity significantly slower than standard gravity. These instances illustrate **Chronometric**
**Hallucination** : a prevalent failure mode where generated motions exhibit an ambiguous, unstable, and uncontrollable
physical time scale.


pulse, formalized as **Physical Frames Per Second (PhyFPS)**, directly from visual dynamics. We distinguish the
inherent PhyFPS from the nominal metadata (meta FPS) by defining PhyFPS as the true frame rate that
aligns with the real-world passage of time. Through controlled temporal resampling, we supervise the model
to learn these motion-grounded dynamics, bypassing the often unreliable metadata.

We evaluate Visual Chronometer across multiple dimensions. First, to validate the accuracy of our method,
we introduce `PhyFPS-Bench-Real`, comprising real-world videos where the true PhyFPS often diverges from
the meta FPS due to complex speed variations. Second, we establish `PhyFPS-Bench-Gen` to systematically
audit state-of-the-art video generators along three complementary axes: (i) the alignment between meta FPS
and actual PhyFPS, (ii) intra-video stability (the consistency of PhyFPS across sliding windows within a
single clip), and (iii) inter-video stability across different outputs from the same model configuration.
Our extensive measurements reveal a harsh reality: even strong generators exhibit substantial PhyFPS
misalignment, alongside significant intra- and inter-video temporal jitter. Without a grounded physical time
scale, these models fail to provide the reliable simulation necessary for true world modeling. Furthermore,
we demonstrate that applying PhyFPS-guided post-corrections to generated videos substantially improves
human-perceived naturalness, as validated by our user study. Finally, we evaluate strong Vision-Language
Models (VLMs) as potential PhyFPS judges, finding them vastly unreliable for this specialized task, thereby
underscoring the necessity of our dedicated Visual Chronometer. Our contributions are summarized as follows:

 - We identify and define the phenomenon of **chronometric hallucination** in modern video generators, and
formalize **Physical Frames Per Second (PhyFPS)** as a temporal scale distinct from nominal meta FPS.

 - We propose **Visual Chronometer**, a robust predictor that recovers PhyFPS directly from raw frames by
learning motion-grounded dynamics through controlled temporal resampling.

 - We introduce `PhyFPS-Bench-Gen` to audit state-of-the-art generators, revealing severe time-scale misalignment in modern video generators. We further show that PhyFPS-guided post-correction significantly
enhances human-perceived temporal naturalness.

 - Through `PhyFPS-Bench-Real`, we demonstrate our model’s precision in predicting Physical FPS. Our
analysis also reveals that the state-of-the-art VLMs are unreliable temporal judges, underscoring the
necessity of a dedicated Visual Chronometer.

### **2 Related Works**


**2.1** **Video Generation and the Quest for World Models**


Modern video generative models, spanning large-scale diffusion and autoregressive architectures, have achieved
unprecedented perceptual quality and semantic coherence [10, 1, 2, 11, 12, 13, 14, 15, 6, 16]. To capture
dynamics, these systems employ sophisticated temporal modeling mechanisms, such as 3D spatiotemporal
operators [17, 18], causal attention blocks [7, 10], and temporal latent spaces [19, 20]. As these architectures


2


scale, they are increasingly framed as “world models” capable of simulating physical environments [21, 22, 23,
24, 25]. However, while prior works focus heavily on optimizing frame-to-frame kinematic smoothness and
spatial layout, the actual physical time scale of the depicted motion is rarely encoded or supervised [26, 27];
instead, models rely entirely on the nominal frame rate (meta FPS) provided by the dataset container. Because
these advanced generative mechanisms do not explicitly ground their temporal learning in real-world physics,
they remain highly vulnerable to chronometric hallucination—producing motions that look perceptually
smooth but lack a consistent physical speed. We argue that one cannot fix a physical flaw without first being
able to measure it. Thus, we complement these generative advancements by developing the first dedicated tool
to audit this structural blind spot. By explicitly defining and predicting the intrinsic Physical FPS (PhyFPS),
we provide the necessary metric and benchmark to evaluate time-scale calibration in world models.


**2.2** **Visual Perception of Time and Dynamics**


Our methodology draws inspiration from a long-standing line of computer vision research aimed at understanding time and speed from visual cues. Early efforts in this domain focused on domain-specific heuristics, such
as detecting slow-motion replays in sports broadcasts [28, 29, 30]. More recently, self-supervised approaches
like SpeedNet [31] demonstrated that neural networks can discriminate between normal-rate and artificially
sped-up clips. In a parallel vein, research on the “arrow of time” explores whether models can recognize
the forward or backward directionality of video playback [32, 33]. Furthermore, semantic hyperlapse and
time-remapping techniques actively manipulate temporal sampling to summarize videos [34, 35, 36, 37, 38, 39],
proving that visual dynamics naturally dictate the perceived flow of time. However, these existing perception
models typically frame time as a binary classification problem (e.g., faster vs. slower, forward vs. backward).
They do not aim to recover a high-precision physical metric. In contrast, **Visual Chronometer** frames time-scale
perception as an absolute continuous regression problem, directly predicting PhyFPS from frame sequences to
audit generative models without relying on corrupted metadata.


**2.3** **Benchmarking Temporal and Physical Fidelity**


Evaluating video generation has traditionally been dominated by perceptual quality and semantic fidelity
metrics. Standard protocols rely on frame-level similarity (PSNR [40], SSIM [41], LPIPS [42]), no-reference
perceptual quality predictors for user-generated and variable-frame-rate videos such as RAPIQUE [43] and
FAVER [44], and distribution-level feature matching, most notably the Fréchet Video Distance (FVD) [45].
Recognizing the limitations of monolithic metrics, recent comprehensive suites like VBench [46, 47, 48]
and WorldScore [49] have introduced multi-dimensional evaluations, including physics-adjacent axes such
as temporal consistency and action alignment. Nevertheless, these benchmarks primarily evaluate whether
the motion “looks natural” rather than measuring the exact temporal speed governing the scene. Time-scale
fidelity—specifically, whether a video strictly adheres to a stable physical frame rate throughout its duration—
remains entirely unmeasured. Our introduced benchmarks, `PhyFPS-Bench-Real` and `PhyFPS-Bench-Gen`,
fill this critical void. By shifting the evaluation paradigm from perceptual smoothness to chronometric
measurement, we provide the first quantitative audit of intra-video and inter-video time-scale stability in
generative world models.

### **3 Data Preparation**


**3.1** **Data Collection**


To train **Visual** **Chronometer** to accurately predict the **Physical** **Frames** **Per** **Second** **(PhyFPS)**, we require
a training dataset with verified, ground-truth temporal labels. A model trained on data suffering from
chronometric hallucination inherently cannot serve as a reliable temporal measurement tool. Therefore, we
curate a dataset exclusively from video sources where the nominal metadata frame rate perfectly aligns with
the real-world physical sampling rate (i.e., meta FPS = PhyFPS), strictly excluding videos with ambiguous
post-hoc time-scale editing. We aggregate our high-fidelity source data from the following categories:

- **High-Frame-Rate Academic Datasets:** We utilize high-speed benchmarks, including Adobe240 [50] and
BVI-VFI [51] (up to 120 Hz), typically used for precise temporal analysis and frame interpolation.


3


videos from high-frequency source data (240 FPS) to simulate real-world camera
mechanics: Sharp Capture, Motion Blur, and Rolling Shutter.



Rates.




 - **Raw Broadcast Sequences:** Uncompressed 4K YUV footage from UVG [52] (50/120 FPS) is included; its
raw pipeline minimizes the risk of hidden temporal remapping.

 - **Sensor-Synchronized** **Autonomous** **Data:** Datasets from NVIDIA and Honda [53] provide cross-sensor
alignment (Camera/LiDAR/IMU), where strict synchronization guarantees physical time-scale integrity.

 - **Physics-Grounded** **Human** **Motion:** Human-centric sequences [54] are incorporated to leverage motion
captured specifically for biomechanical and dynamic realism.

 - **Verified In-House Data:** We supplement the public datasets with an internal collection captured under
strictly controlled settings with verified frame-rate metadata.


**3.2** **Data Preprocessing and Augmentation**


To force the model to learn intrinsic visual dynamics rather than relying on semantic content priors, we
expand our training distribution by synthetically generating a diverse array of PhyFPS variants from the
source videos. We first temporally upsample all source videos to a high-frequency base rate of 240 FPS using
a state-of-the-art frame interpolation model (RIFE) [55].

Let this high-rate video be _I_ _[H]_ at a frequency _FH_ = 240 FPS. For a target lower frame rate _FL_, we define the
downsampling ratio as _N_ = _FH_ _/FL_ . We then synthesize low-rate videos ( _I_ _[L]_ ) using three distinct strategies
(illustrated in Fig. 2), each designed to model specific real-world camera mechanics:


**(1) Sharp Capture (Fast Shutter):** To simulate cameras operating with a very fast shutter speed (which minimizes
motion blur), we uniformly subsample the high-rate sequence by setting _Ik_ _[L]_ [=] _[ I]_ _⌊_ _[H]_ _kN_ _⌋_ [,] [where] _[I]_ _k_ _[L]_ [denotes] [the]
_k_ -th frame of the synthesized low-rate video and _⌊kN_ _⌋_ is the corresponding discrete frame index in the
high-rate source. This isolates pure spatial displacement over time, preserving sharp object boundaries but
often resulting in the naturally aliased motion (stutter) typically seen in sports or action footage.


**(2) Motion Blur (Variable Exposure):** Real-world cameras integrate light over an exposure window, resulting in
motion blur that provides strong visual cues about object velocity. To mimic this exposure integration, we
synthesize each low-rate frame by averaging a temporal window of high-rate frames: _Ik_ _[L]_ [=] _M_ 1 - _Mi_ =0 _−_ 1 _[I]_ _⌊_ _[H]_ _kN_ _⌋_ + _i_ [,]
where _M_ is the exposure window length. We simulate long, medium, and short effective exposures by setting
_M_ _∈{N, N/_ 2 _, N/_ 4 _}_ .


**(3) Synthetic Rolling Shutter** Fast-moving objects captured by modern CMOS sensors frequently exhibit rolling
shutter distortions [56] because sensor rows or columns are read sequentially rather than instantaneously. We
simulate this intra-frame temporal distortion by partitioning the target frame’s spatial dimension (e.g., width
_W_ ) into progressive bands. A pixel at column _x_ is sampled from the high-rate sequence at a progressively
shifted time index: _⌊kN_ _⌋_ + _⌊M_ _· x/W_ _⌋_ . By varying the readout duration _M_ _∈{N, N/_ 2 _, N/_ 4 _}_, we ensure the
predictor is robust to these common spatiotemporal artifacts.


**Final Dataset Composition.** As summarized in Fig. 3, alongside these synthetically augmented variants, we
retain the original source videos at their native capture rates to preserve raw sensor statistics. e generate
training data across 18 Physical Frame Rates, yielding a comprehensive dataset of 465,535 video clips,
uniformly standardized to a length of 128 frames to ensure balanced representation across different time scales.


4


### **4 Visual Chronometer**

**4.1** **Model Architecture**


**Backbone and Regression Head.** We adopt VideoVAE+ [20] as the foundational video encoder to extract
compact spatiotemporal latent representations. Given an input clip of _T_ frames **V** = _{It}_ _[T]_ _t_ =1 [,] [the] [backbone]
produces a sequence of latent tokens **Z** = Enc( **V** ).

Instead of relying on conventional spatial pooling, we attach a lightweight, attention-based prediction head to
aggregate temporal features into a clip-level representation. Specifically, we project the latent tokens into a
hidden dimension and introduce a learnable query embedding that cross-attends to the token sequence. This
query-based pooling mechanism effectively decouples the regression head from the input frame count, enabling
**Visual Chronometer** to process videos of arbitrary lengths. Finally, a Multi-Layer Perceptron (MLP) maps
the aggregated feature vector to a single scalar _s_ ˆ _∈_ R, which represents the predicted logarithmic frame rate,
log(PhyFPS). We predict the logarithmic value rather than the absolute frequency to stabilize optimization
across an exponentially wide range of time scales and to penalize relative, rather than absolute, errors.


**4.2** **Training Objective**


Let the ground-truth PhyFPS be _y_, with its log-space target defined as _s_ = log _y_ . The model outputs the
prediction _s_ ˆ = log ˆ _y_ . We optimize the model using a Mean Squared Error (MSE) in the logarithmic space:



_L_ log = [1]

_n_



_n_

- (log _yi −_ _s_ ˆ _i_ ) [2] _,_ (1)


_i_ =1



where _n_ is the batch size. Because the target PhyFPS values in our dataset are strictly positive ( _yi_ _≥_ 2), the
logarithmic transformation is intrinsically well-defined. Therefore, we deliberately omit the standard offset
term (+1) typically found in traditional Mean Squared Logarithmic Error (MSLE) formulations, allowing the
loss to strictly reflect the true proportional scaling of time.


**4.3** **Model Training Details**


To train the Visual Chronometer, we extract clips from the dataset using a sliding window. During training,
clips are sampled with a maximum temporal footprint of _T_ = 32 frames. To ensure robust performance
across different deployment scenarios, we train two variants of the model targeting different operational
regimes. The **VC-Wide** model is trained to predict across 18 distinct frame rates spanning from extreme
slow-motion to high-speed capture: PhyFPS _∈{_ 2 _,_ 5 _,_ 10 _,_ 12 _,_ 15 _,_ 18 _,_ 20 _,_ 24 _,_ 25 _,_ 30 _,_ 35 _,_ 40 _,_ 45 _,_ 50 _,_ 60 _,_ 90 _,_ 120 _,_ 240 _}_ .
The **VC-Common** model focuses specifically on the most prevalent consumer and web video formats, narrowing
the output space to PhyFPS _∈{_ 12 _,_ 15 _,_ 18 _,_ 20 _,_ 24 _,_ 25 _,_ 30 _,_ 35 _,_ 40 _,_ 45 _,_ 50 _,_ 60 _}_ .

Both models are trained end-to-end, fine-tuning the VideoVAE+ backbone jointly with the attention-based
prediction head. Optimization is performed using the Adam optimizer with a learning rate of 1 _×_ 10 _[−]_ [5] for
125,000 iterations. We execute the training on a single computing node equipped with four NVIDIA RTX
A6000 GPUs, utilizing a global batch size of 32.

### **5 Experiments**


In this section, we conduct three sets of experiments to validate the **Visual Chronometer** and demonstrate its
utility in addressing chronometric hallucination, as well as enabling physics-grounded data preprocessing and
video post-processing. First, we introduce `PhyFPS-Bench-Gen` to audit existing open- and closed-source video
generative models by measuring their Meta-vs-PhyFPS alignment and temporal stability. Second, we build
`PhyFPS-Bench-Real` to evaluate the prediction accuracy of our model against reliable ground-truth labels.
Third, we compare our specialized predictor against strong Vision-Language Models (VLMs), demonstrating
that general-purpose foundation models are not yet capable of reliable PhyFPS prediction.


5


**5.1** **Auditing Generative World Models**


`PhyFPS-Bench-Gen` **.** We introduce `PhyFPS-Bench-Gen`, a benchmark designed to quantitatively audit the timescale alignment of video generative models using our Visual Chronometer. We evaluate a diverse spectrum of
leading generators. For open-source models, we assess the Wan series [1] (Wan2.1-1.3B, Wan2.1-14B, Wan2.25B, Wan2.2-14B), the LTX series [11, 2] (LTX-Video, LTX-2), the CogVideoX series [12] (CogVideoX-2B,
CogVideoX-5B), HunyuanVideo [14], and the autoregressive model InfinityStar [57]. For closed-source models,
we evaluate Veo-3.1-Fast [58], Sora-2 [59], Grok-Imagine-T2V [60], Kling-o3 [61], Seedance-1.0-Lite [62], and
Seedance-1.5-Pro [62].


**Benchmark Prompts.** To ensure robust evaluation, we design 100 text-to-video prompts covering diverse
content and motion patterns, strictly avoiding explicit speed-manipulation keywords (e.g., `slow` `motion`,
`time-lapse`, `speed` `up` ). To guarantee that PhyFPS is observable, every prompt mandates at least one clearly
dynamic instance, excluding purely static scenes. Prompt diversity is balanced across five axes: (i) **primary**
**entity** (human, animal, vehicle, and nature), (ii) **motion type** (articulated, rigid-body, fluid, and multi-agent),
(iii) **camera behavior** (static, pan, and tracking), (iv) **environmental effects** (rain, fire, and wind), and (v)
**scene context** (indoor, urban, and nature). All models operate under default settings, extracting the nominal
saved FPS ( _F_ meta) from official documentation or output metadata, where _F_ meta _,c_ denotes the container FPS
of the source video corresponding to clip _c_ .


**PhyFPS Estimation and Metrics.** For all audits on generated videos, we employ the **VC-Common** predictor. For
each video _v_ _∈{_ 1 _, . . ., V }_, we extract _Cv_ overlapping clips of _T_ =32 frames with stride _s_ =4. Let _f_ [ˆ] _v,c_ denote
the predicted PhyFPS for clip _c_ . The video-level PhyFPS ( _f_ [¯] _v_ ) and the overall model-level PhyFPS ( _F_ [ˆ] ) are
computed as:



_V_

- _f_ ¯ _v._ (2)


_v_ =1



1
_f_ ¯ _v_ =
_Cv_




- _Cv_ _f_ ˆ _v,c,_ _F_ ˆ = 1

_V_
_c_ =1



We evaluate each generator along three critical dimensions. **(1) Meta-vs-PhyFPS Alignment** measures how well
the nominal container rate _F_ meta matches the predicted intrinsic speed. We report both the **Avg.** **Error (FPS)**
and the **Pct.** **Error (%)** :



�� _f_ ˆ _v,c −_ _F_ meta _,c_ ��

- - _._ (3)

_F_ meta _,c_



_V_



_v_ =1



1
_Cv_



Avg. Error = [1]

_V_



_V_



_v_ =1



1
_Cv_



_Cv_



_c_ =1



_f_ ˆ _v,c −_ _F_ meta _,c_ _,_ Pct. Error = [100]
��� ��� _V_



_f_ ˆ _v,c −_ _F_ meta _,c_ _,_ Pct. Error = [100]
��� ���



_Cv_



_c_ =1



**(2) Inter-video Consistency** and **(3) Intra-video Consistency** evaluate temporal stability across different prompts
and within a single continuous video, respectively. Both utilize the coefficient of variation (CV):



Inter CV = Std� _{f_ [¯] _v}_ _[V]_ _v_ =1�



_V_



Std _{fv}v_ =1 _,_ Intra CV = [1]

Mean� _{f_ [¯] _v}_ _[V]_ _v_ =1� _V_




   -    
- _V_ Std _{f_ [ˆ] _v,c}_ _[C]_ _c_ =1 _[v]_ _._ (4)

    -    
_v_ =1 Mean _{f_ [ˆ] _v,c}_ _[C]_ _c_ =1 _[v]_



**Audit Results.** Table 1 details the results of the `PhyFPS-Bench-Gen` audit. We observe a pervasive Metavs-PhyFPS mismatch across the majority of generators; despite outputs being stored at a fixed nominal
meta FPS, the intrinsic visual speeds vary wildly. Notably, the Wan series models exhibit a relatively high
adherence to their suggested meta FPS, achieving comparatively low average and percentage errors. To
evaluate temporal consistency, we measure Inter CV and Intra CV, which represent the fluctuation of PhyFPS
across different generated videos and the stability of PhyFPS across different time segments within a single
video, respectively. The LTX-Video and LTX-2 models demonstrate strong performance on these stability
metrics. This suggests their temporal representations are internally consistent, and the high absolute errors
may primarily stem from inaccurate meta FPS metadata rather than structural chronometric hallucination.
For instance, LTX-Video’s outputs might simply need their meta FPS adjusted from 24 to around 46.5 to
achieve high time-scale fidelity.

Overall, closed-source models slightly outperform open-source counterparts in terms of absolute accuracy,
maintaining average errors below 14 FPS and percentage errors under 60%. This indicates that commercial
models may employ more carefully designed strategies for selecting meta FPS. However, despite these


6


**Table 1** **Quantitative Audit of Generative Models.** `PhyFPS-Bench-Gen` results evaluating time-scale fidelity. Blue and red
shaded cells indicate the best and second-best performance within each group (open vs. closed source).


Model Meta FPS PhyFPS Avg. Error _↓_ Pct. Error(%) _↓_ Intra CV _↓_ Inter CV _↓_


_Open-sourced_ _Models_


CogVideoX-2B 24 33.64 12.46 52 0.11 0.46
CogVideoX-5B 24 38.26 17.96 75 0.12 0.52
HunyuanVideo 24 35.89 13.82 58 0.12 0.36
Wan2.1-T2V-1.3B 24 26.28 7.54 31 0.11 0.38
Wan2.1-T2V-14B 24 32.37 10.87 45 0.14 0.36
Wan2.2-T2V-A14B 24 31.52 10.74 45 0.12 0.38
Wan2.2-TI2V-5B 24 32.81 11.63 48 0.15 0.38
InfinityStar (5s) 16 34.41 18.46 115 0.11 0.38
InfinityStar (10s) 16 36.15 20.19 126 0.16 0.36
LTX-Video 24 46.52 23.67 99 0.10 0.33
LTX-2 25 39.77 15.70 63 0.13 0.34


_Closed-sourced_ _Models_


Seedance-1.0-Lite 24 28.60 8.31 35 0.15 0.37

Veo-3.1-Fast 24 35.83 13.62 57 0.17 0.33


advantages in global alignment, the Intra and Inter CV scores of closed-source models are not significantly
better than those of open-source models. This reveals that even heavily optimized, industry-scale generators
still struggle with PhyFPS stability. It appears researchers predominantly prioritize visual fidelity and
kinematic smoothness, inadvertently neglecting strict physical time-scale adherence. This lack of reliable
temporal grounding poses a significant challenge for leveraging current video generative models as accurate
world models. Finally, we observe a consistent trend where the predicted PhyFPS is generally higher than the
assigned Meta FPS across almost all videos. According to the Visual Chronometer, most generated videos
should be played back at a higher meta FPS, or directly at their intrinsic PhyFPS. This finding aligns with the
widely recognized phenomenon that current generative models tend to produce “slow but smooth” videos [9].


**User Study:** **Perceptual Validation via Video Post-processing.** To demonstrate the practical utility of our method
and confirm that mathematical PhyFPS accuracy translates to improved human perception, we conduct a
user study treating the predictor as a post-processing tool. Using **VC-Common**, we predict the clip-level
PhyFPS for generated videos. We then present users with three variants of the same sequence. The first
variant is the **Original** video, representing the untouched output directly from the generative model. The
second variant, **Pred**, serves as a globally corrected version; here, we uniformly re-time the entire video to
match its average predicted PhyFPS. The third variant, **Pred Dyn**, applies a dynamic local correction, where
each distinct temporal segment within the video is independently re-timed based on its specific, clip-level
PhyFPS prediction.

We collected 1,490 pairwise comparisons from
over 15 participants. Utilizing the Bradley–Terry
model [63], we estimated the relative preference
strength for each variant, computing 90% confidence intervals via bootstrapping (Figure 4). The results reveal that both post-processed variants significantly outperform the hallucinated original outputs
(19.0%). Interestingly, the global correction (Pred, **Figure 4** **Human Perceptual Preference on Temporal Natural-**
44.2%) is preferred over the dynamic local correc- **ness.** Bradley-Terry scores comparing the original genertion (Pred Dyn, 36.9%). We hypothesize that while ated videos against our post-processed variants. Both the
dynamic correction perfectly aligns local clips to global average correction ( **Pred** ) and dynamic local correc
tion ( **Pred Dyn** ) are strongly preferred over the hallucinated

their intrinsic PhyFPS, varying the playback frame

original outputs, with 90% confidence intervals indicating

rate within a single short sequence may introduce

statistical significance.

perceptual inconsistencies or jitter. Conversely, applying a constant, averaged Physical Frame Rate (Pred) remains visually smoother and more natural to human
observers. Ultimately, these findings definitively highlight the value of physics-grounded post-processing.


7


**5.2** **Validating the Visual Chronometer**


To establish the reliability of our measurement tool, we evaluate its prediction accuracy on the `PhyFPS-Bench-Real`
test set (comprising 4,000 verified clips partitioned from our dataset). Crucially, to ensure that the Visual
Chronometer learns intrinsic physical time scales rather than overfitting to dataset-specific biases, we enforce
a strict cross-source split; the training, validation, and test sets are derived from entirely disjoint video sources.
Given the ground-truth PhyFPS _yi_ and predicted PhyFPS _y_ ˆ _i_ across _n_ test samples, we report the Mean
Absolute Error (MAE) and Mean Absolute Percentage Error (MAPE) to capture both absolute deviations
and proportional accuracy:



MAE = [1]

_n_



_n_





- _|yi −_ _y_ ˆ _i|,_ MAPE = [100]

_n_

_i_ =1



_n_



_n_



_i_ =1



_|yi −_ _y_ ˆ _i|_

_._ (5)
_yi_



Given the rapid advancements in Vision-Language Models (VLMs), it is tempting to deploy them as out-of-thebox evaluators for physical scene dynamics. To rigorously test this hypothesis, we establish a comprehensive
baseline using state-of-the-art VLMs, including Gemini-3.1-Pro [64], Gemini-3-Flash [64], Seed-1.6 and
Seed-1.6-Flash [62], as well as Qwen3.5+ and Qwen3.5-397B [65].



We evaluate these VLMs under two input paradigms
(prompt details in the Appendix). First, we use
a _Video-based_ approach. Because modern VLMs
typically subsample frames to manage context length,
this inherent preprocessing disrupts temporal spacing,
predictably degrading frame rate perception. To
bypass this architectural bottleneck, we introduce
an _Image-based_ paradigm, unrolling the video into
128 discrete images fed sequentially to preserve the
absolute frame count and temporal order.

The results (Table 2) show that our Visual Chronometers ( **VC-Common** and **VC-Wide** ) achieve exceptionally
low MAE and MAPE, with the narrower-range VCCommon predictably yielding the tightest margins.
Qualitatively, Figure 5 confirms our model’s ability
to continuously and accurately track physical time
scales across varying base rates.
Conversely, all tested VLMs fail catastrophically at
physical estimation for both video inputs and unrolled
image sequences. Many suffer from severe mode
collapse. For example, Seed-1.6-Flash degenerates to
predicting exactly 30 FPS for all inputs regardless of
the actual dynamics. These findings demonstrate that
general-purpose foundation models lack a grounded
internal motion pulse, reinforcing the necessity of our
specialized architecture.


**5.3** **Ablation Studies**



**Table** **2** **Predictor** **Accuracy** **&** **VLM** **Baseline** **Compar-**
**ison.** Evaluating the Visual Chronometer (Ours)
against state-of-the-art Vision-Language Models on
`PhyFPS-Bench-Real` . The average ground-truth PhyFPS
across the test set is 38.81. Blue and red shaded cells
indicate the best and second-best performance.


Model Avg Pred MAE _↓_ MAPE(%) _↓_


_Ours_


_Video-based_ _VLM_


Gemini-3.1-Pro 31.00 21.67 43
Gemini-3-Flash 26.60 23.40 47
Seed-1.6 29.60 20.40 41
Seed-1.6-Flash 30.00 20.00 40
Qwen3.5+ 4.46 45.54 91
Qwen3.5-397B 25.60 24.40 49


_Image-based_ _VLM_


Gemini-3.1-Pro 5.15 44.85 90
Gemini-3-Flash 1.77 48.23 96
Seed-1.6 6.35 43.65 87
Seed-1.6-Flash 30.00 20.00 40
Qwen3.5+ 3.48 46.52 93
Qwen3.5-397B 22.03 27.97 56



To validate our core design choices, we conduct ablation studies on the **VC-Common** model, evaluating the
impact of physics-grounded data augmentations and inference temporal context length.


**Impact of Temporal Augmentations.** To verify the necessity of our physics-grounded augmentations (Fast
Shutter, Motion Blur, and Synthetic Rolling Shutter), we train a naive baseline using only uniform temporal
subsampling. Evaluated on the in-the-wild conditions of `PhyFPS-Bench-Real` (Table 3), the baseline degrades
significantly, with MAE increasing from 3.46 to 5.12. Without simulating exposure integration or sequential
sensor readout during training, the naive model overfits to idealized spatial displacements and fails to
disentangle physical speed from realistic motion artifacts. This confirms our augmentations are critical for
learning robust, intrinsic visual dynamics.


8


**Table 3** **Ablation Study on Temporal Data Augmentations.** Evaluated on `PhyFPS-Bench-Real` using the VC-Common
configuration.


Augmentation Strategy Motion Blur Rolling Shutter MAE _↓_ MAPE (%) _↓_


Naive Baseline ✗ ✗ 5.12 13
+ Motion Blur ✓ ✗ 4.87 11
**VC-Common** ✓ ✓ **3.46** **9**


**Impact of Temporal Context Length.** Measuring physical speed computationally requires sufficient kinematic
history. We evaluate the robustness of **VC-Common** across varying inference window lengths (patch sizes)
_T_ _∈{_ 8 _,_ 16 _,_ 32 _,_ 64 _,_ 128 _}_ .
As illustrated in Figure 6, the base model (trained on max 32 frames) expectedly struggles with ultra-short
contexts ( _T_ = 8) due to insufficient visual evidence, optimizing at _T_ = 32 (MAE = 3 _._ 46). Notably, it
demonstrates strong length extrapolation, maintaining competitive accuracy at _T_ = 64 and 128. Post-training
the model on a maximum length of 128 frames further improves performance at _T_ = 64 without degrading
short-patch accuracy.

However, a critical bottleneck emerges: increasing the inference patch size to _T_ = 128 fails to outperform
_T_ = 64. This reveals an inherent trade-off in temporal modeling. While small patches lack sufficient receptive
fields, extremely large patches (e.g., _T_ = 128, spanning the entire benchmark video) restrict evaluation to
a single global inference pass. This loses the variance-reduction benefits of sliding-window ensembling and
strips the model of its ability to capture fine-grained PhyFPS fluctuations within a single shot. Consequently,
a mid-range patch size ( _T_ = 32 to 64) optimally balances kinematic context with local temporal granularity.

### **6 Discussion: Implications and Future Directions**


In this section, we contextualize our findings and explore future directions for temporal modeling in generative
video through a question-and-answer format.


9


**Figure 6** **Ablation on Inference Context Length (** _T_ **).** Evaluating the VC-Common model across different inference patch
sizes on `PhyFPS-Bench-Real` . We compare the base model (trained on max 32 frames) with a post-trained variant
(max 128 frames) to analyze the trade-off between temporal receptive field and sliding-window granularity.


**Q1: IsstrictalignmentbetweenPhyFPSandmetaFPSalwaysdesirable?** **Inotherwords, ischronometrichallucination**
**inherently problematic, given that intentional speed manipulation is a core creative tool in filmmaking?**

**A:** Dynamic retiming—such as deliberate slow-motion or time-lapse—is undeniably a vital creative tool. We
do not argue that every generated video must strictly adhere to a 1 _×_ physical time scale (i.e., PhyFPS =
meta FPS). Rather, the fundamental issue with chronometric hallucination lies in the absence of **controllability** .
Currently, models hallucinate time scales arbitrarily; a user prompting for a “person walking” might implicitly
receive a sequence operating at 0 _._ 5 _×_ or 2 _×_ physical speed without any explicit instruction. While variable
speeds are essential for specific creative scenarios, the ability to stably generate a grounded, default 1 _×_ speed
is a prerequisite for true controllability. If generative video models are to evolve into reliable world models,
they must possess a stable internal pulse. Only by first mastering baseline physical reality can a model
faithfully execute deliberate _N_ _×_ speed manipulations upon request.


**Q2:** **How can future video generation pipelines resolve chronometric hallucination?**

**A:** To resolve this issue, future pipelines should treat time as an active, controllable condition. First, at the
data curation level, training datasets should be rigorously relabeled with their true intrinsic PhyFPS. Our
Visual Chronometer can serve as an automated, large-scale annotator to explicitly filter or condition the
input distribution. Second, at the architectural level, models require temporal conditioning mechanisms that
force the network to explicitly comprehend and disentangle the true pulse of varying physical frame rates
during training. Finally, from an optimization standpoint, the Visual Chronometer has the potential to act
as a specialized reward model. By providing direct, physics-grounded supervision signals during preference
alignment (e.g., via RLHF or DPO), it can guide generative models to strictly adhere to desired temporal
dynamics and structurally eliminate chronometric hallucination.

### **7 Conclusion**


In this work, we identify and formalize the phenomenon of **chronometric** **hallucination** in modern video
generative models, where a reliance on arbitrary metadata containers leads to ambiguous and uncontrollable
physical speeds. To address this issue, we propose the **Visual Chronometer**, a robust predictor trained via
physics-grounded temporal resampling that accurately recovers the intrinsic Physical Frames Per Second
(PhyFPS) directly from visual dynamics. Through our comprehensive benchmarks, `PhyFPS-Bench-Gen` and
`PhyFPS-Bench-Real`, we reveal a stark reality: state-of-the-art generators and vision-language models currently
struggle to maintain a consistent internal pulse of motion. Nevertheless, by demonstrating that PhyFPS-guided
dynamic retiming significantly improves the human-perceived temporal naturalness of AI-generated videos,
we offer an immediate, practical mitigation. Ultimately, we hope this work inspires future generative world
models to transition from passive metadata reliance to active, physics-grounded temporal conditioning.


10


### **References**


[1] T. Wan, A. Wang, B. Ai, B. Wen, C. Mao, C.-W. Xie, D. Chen, F. Yu, H. Zhao, J. Yang _et_ _al._, “Wan: Open and
advanced large-scale video generative models,” _arXiv_ _preprint_ _arXiv:2503.20314_, 2025.


[2] Y. HaCohen, B. Brazowski, N. Chiprut, Y. Bitterman, A. Kvochko, A. Berkowitz, D. Shalem, D. Lifschitz,
D. Moshe, E. Porat _et_ _al._, “Ltx-2: Efficient joint audio-visual foundation model,” _arXiv_ _preprint_ _arXiv:2601.03233_,
2026.


[3] Z. Jiang, Z. Han, C. Mao, J. Zhang, Y. Pan, and Y. Liu, “Vace: All-in-one video creation and editing,” _arXiv_
_preprint_ _arXiv:2503.07598_, 2025.


[4] R. Burgert, C. Herrmann, F. Cole, M. S. Ryoo, N. Wadhwa, A. Voynov, and N. Ruiz, “Motionv2v: Editing motion
in a video,” _arXiv_ _preprint_ _arXiv:2511.20640_, 2025.


[5] X. Gao, R. Li, X. Chen, Y. Wu, S. Feng, Q. Yin, and Z. Tu, “Pisco: Precise video instance insertion with sparse
control,” _arXiv_ _preprint_ _arXiv:2602.08277_, 2026.


[6] M. Wu, A. Mishra, S. Dey, S. Xing, N. Ravipati, H. Wu, B. Li, and Z. Tu, “Consid-gen: View-consistent and
identity-preserving image-to-video generation,” _arXiv_ _preprint_ _arXiv:2602.10113_, 2026.


[7] A. Ali, J. Bai, M. Bala, Y. Balaji, A. Blakeman, T. Cai, J. Cao, T. Cao, E. Cha, Y.-W. Chao _et_ _al._, “World
simulation with video foundation models for physical ai,” _arXiv_ _preprint_ _arXiv:2511.00062_, 2025.


[8] R. Team, Z. Gao, Q. Wang, Y. Zeng, J. Zhu, K. L. Cheng, Y. Li, H. Wang, Y. Xu, S. Ma _et_ _al._, “Advancing
open-source world models,” _arXiv_ _preprint_ _arXiv:2601.20540_, 2026.


[9] Z. Wu, A. Kag, I. Skorokhodov, W. Menapace, A. Mirzaei, I. Gilitschenski, S. Tulyakov, and A. Siarohin, “Densedpo:
Fine-grained temporal preference optimization for video diffusion models,” _arXiv_ _preprint_ _arXiv:2506.03517_, 2025.


[10] J. Liu, J. Han, B. Yan, H. Wu, F. Zhu, X. Wang, Y. Jiang, B. Peng, and Z. Yuan, “Infinitystar: Unified spacetime
autoregressive modeling for visual generation,” 2025. [Online]. Available: [https://arxiv.org/abs/2511.04675](https://arxiv.org/abs/2511.04675)


[11] Y. HaCohen, N. Chiprut, B. Brazowski, D. Shalem, D. Moshe, E. Richardson, E. Levin, G. Shiran, N. Zabari,
O. Gordon _et_ _al._, “Ltx-video: Realtime video latent diffusion,” _arXiv_ _preprint_ _arXiv:2501.00103_, 2024.


[12] Z. Yang, J. Teng, W. Zheng, M. Ding, S. Huang, J. Xu, Y. Yang, W. Hong, X. Zhang, G. Feng _et_ _al._, “Cogvideox:
Text-to-video diffusion models with an expert transformer,” _arXiv_ _preprint_ _arXiv:2408.06072_, 2024.


[13] W. Hong, M. Ding, W. Zheng, X. Liu, and J. Tang, “Cogvideo: Large-scale pretraining for text-to-video generation
via transformers,” _arXiv_ _preprint_ _arXiv:2205.15868_, 2022.


[14] W. Kong, Q. Tian, Z. Zhang, R. Min, Z. Dai, J. Zhou, J. Xiong, X. Li, B. Wu, J. Zhang _et_ _al._, “Hunyuanvideo: A
systematic framework for large video generative models,” _arXiv_ _preprint_ _arXiv:2412.03603_, 2024.


[15] M. Elmoghany, L. Zhao, X. Shen, S. Mukherjee, Y. Zhou, G. Wu, V. D. Lai, S. Yoon, R. Rossi, A. Rashwan _et_ _al._,
“Infinitystory: Unlimited video generation with world consistency and character-aware shot transitions,” _arXiv_
_preprint_ _arXiv:2603.03646_, 2026.


[16] J. Yu, X. Gao, P. Verlani, A. Gadde, Y. Wang, B. Adsumilli, and Z. Tu, “Sparkvsr: Interactive video superresolution via sparse keyframe propagation,” _arXiv_ _preprint_ _arXiv:2603.16864_, 2026.


[17] D. Tran, L. Bourdev, R. Fergus, L. Torresani, and M. Paluri, “Learning spatiotemporal features with 3d
convolutional networks,” in _Proceedings_ _of_ _the_ _IEEE_ _international_ _conference_ _on_ _computer_ _vision_, 2015, pp.
4489–4497.


[18] A. Vaswani, N. Shazeer, N. Parmar, J. Uszkoreit, L. Jones, A. N. Gomez, Ł. Kaiser, and I. Polosukhin, “Attention
is all you need,” _Advances_ _in_ _neural_ _information_ _processing_ _systems_, vol. 30, 2017.


[19] Z. Tong, Y. Song, J. Wang, and L. Wang, “Videomae: Masked autoencoders are data-efficient learners for
self-supervised video pre-training,” _Advances_ _in_ _neural_ _information_ _processing_ _systems_, vol. 35, pp. 10 078–10 093,
2022.


[20] Y. Xing, Y. Fei, Y. He, J. Chen, J. Xie, X. Chi, and Q. Chen, “Large motion video autoencoding with cross-modal
video vae,” _arXiv_ _preprint_ _arXiv:2412.17805_, 2024.


[21] B. Kang, Y. Yue, R. Lu, Z. Lin, Y. Zhao, K. Wang, G. Huang, and J. Feng, “How far is video generation from
world model: A physical law perspective,” _arXiv_ _preprint_ _arXiv:2411.02385_, 2024.


[22] Y. Qin, Z. Shi, J. Yu, X. Wang, E. Zhou, L. Li, Z. Yin, X. Liu, L. Sheng, J. Shao _et_ _al._, “Worldsimbench: Towards
video generation models as world simulators,” _arXiv_ _preprint_ _arXiv:2410.18072_, 2024.


[23] J. Ding, Y. Zhang, Y. Shang, Y. Zhang, Z. Zong, J. Feng, Y. Yuan, H. Su, N. Li, N. Sukiennik _et al._, “Understanding
world or predicting future? a comprehensive survey of world models,” _ACM_ _Computing_ _Surveys_, vol. 58, no. 3, pp.
1–38, 2025.


11


[24] L. Wang, Z. Chen, Y. Du, D. Yan, W. Ge, G. Shen, X. Xu, L. Wu, M. Chen, T. Xu _et_ _al._, “A mechanistic view on
video generation as world models: State and dynamics,” _arXiv_ _preprint_ _arXiv:2601.17067_, 2026.


[25] Y. Wang, S. Xing, C. Can, R. Li, H. Hua, K. Tian, Z. Mo, X. Gao, K. Wu, S. Zhou _et_ _al._, “Generative ai for
autonomous driving: Frontiers and opportunities,” _arXiv_ _preprint_ _arXiv:2505.08854_, 2025.


[26] Y. Yuan, X. Wang, T. Wickremasinghe, Z. Nadir, B. Ma, and S. H. Chan, “Newtongen: Physics-consistent and
controllable text-to-video generation via neural newtonian dynamics,” _arXiv_ _preprint_ _arXiv:2509.21309_, 2025.


[27] Z. Gao, J. Mao, H.-X. Yu, H. Lou, E. Y.-T. Jia, J. Barbic, J. Wu, and Y. Wang, “Seeing the wind from a falling
leaf,” _arXiv_ _preprint_ _arXiv:2512.00762_, 2025.


[28] L. Wang, X. Liu, S. Lin, G. Xu, and H.-Y. Shum, “Generic slow-motion replay detection in sports video,” in _2004_
_International_ _Conference_ _on_ _Image_ _Processing,_ _2004._ _ICIP’04._, vol. 3. IEEE, 2004, pp. 1585–1588.


[29] C.-M. Chen and L.-H. Chen, “A novel method for slow motion replay detection in broadcast basketball video,”
_Multimedia_ _Tools_ _and_ _Applications_, vol. 74, no. 21, pp. 9573–9593, 2015.


[30] V. Kiani and H. R. Pourreza, “An effective slow-motion detection approach for compressed soccer videos,”
_International_ _Scholarly_ _Research_ _Notices_, vol. 2012, no. 1, p. 959508, 2012.


[31] S. Benaim, A. Ephrat, O. Lang, I. Mosseri, W. T. Freeman, M. Rubinstein, M. Irani, and T. Dekel, “Speednet:
Learning the speediness in videos,” in _Proceedings_ _of_ _the_ _IEEE/CVF_ _conference_ _on_ _computer_ _vision_ _and_ _pattern_
_recognition_, 2020, pp. 9922–9931.


[32] L. C. Pickup, Z. Pan, D. Wei, Y. Shih, C. Zhang, A. Zisserman, B. Scholkopf, and W. T. Freeman, “Seeing the
arrow of time,” in _Proceedings_ _of_ _the_ _IEEE_ _Conference_ _on_ _Computer_ _Vision_ _and_ _Pattern_ _Recognition_, 2014, pp.
2035–2042.


[33] D. Wei, J. J. Lim, A. Zisserman, and W. T. Freeman, “Learning and using the arrow of time,” in _Proceedings_ _of_
_the_ _IEEE_ _conference_ _on_ _computer_ _vision_ _and_ _pattern_ _recognition_, 2018, pp. 8052–8060.


[34] E. P. Bennett and L. McMillan, “Computational time-lapse video,” in _ACM_ _SIGGRAPH_ _2007_ _papers_, 2007, pp.
102–es.


[35] N. Petrovic, N. Jojic, and T. S. Huang, “Adaptive video fast forward,” _Multimedia_ _Tools_ _and_ _Applications_, vol. 26,
no. 3, pp. 327–344, 2005.


[36] F. Zhou, S. Bing Kang, and M. F. Cohen, “Time-mapping using space-time saliency,” in _proceedings_ _of_ _the_ _IEEE_
_Conference_ _on_ _Computer_ _Vision_ _and_ _Pattern_ _Recognition_, 2014, pp. 3358–3365.


[37] S. Lan, R. Panda, Q. Zhu, and A. K. Roy-Chowdhury, “Ffnet: Video fast-forwarding via reinforcement learning,”
in _Proceedings_ _of_ _the_ _IEEE_ _Conference_ _on_ _Computer_ _Vision_ _and_ _Pattern_ _Recognition_, 2018, pp. 6771–6780.


[38] M. Silva, W. Ramos, J. Ferreira, F. Chamone, M. Campos, and E. R. Nascimento, “A weighted sparse sampling
and smoothing frame transition approach for semantic fast-forward first-person videos,” in _Proceedings_ _of_ _the_
_IEEE_ _Conference_ _on_ _Computer_ _Vision_ _and_ _Pattern_ _Recognition_, 2018, pp. 2383–2392.


[39] M. M. da Silva, “Semantic hyperlapse: a sparse coding based and multi-importance approach for first-person
videos,” 2019.


[40] B. Jähne, _Digital_ _image_ _processing_ . Springer, 2005.


[41] Z. Wang, A. C. Bovik, H. R. Sheikh, and E. P. Simoncelli, “Image quality assessment: from error visibility to
structural similarity,” _IEEE_ _transactions_ _on_ _image_ _processing_, vol. 13, no. 4, pp. 600–612, 2004.


[42] R. Zhang, P. Isola, A. A. Efros, E. Shechtman, and O. Wang, “The unreasonable effectiveness of deep features as
a perceptual metric,” in _Proceedings_ _of_ _the_ _IEEE_ _conference_ _on_ _computer_ _vision_ _and_ _pattern_ _recognition_, 2018, pp.
586–595.


[43] Z. Tu, X. Yu, Y. Wang, N. Birkbeck, B. Adsumilli, and A. C. Bovik, “Rapique: Rapid and accurate video quality
prediction of user generated content,” _IEEE_ _Open_ _Journal_ _of_ _Signal_ _Processing_, vol. 2, pp. 425–440, 2021.


[44] Q. Zheng, Z. Tu, P. C. Madhusudana, X. Zeng, A. C. Bovik, and Y. Fan, “Faver: Blind quality prediction of
variable frame rate videos,” _Signal_ _Processing:_ _Image_ _Communication_, vol. 122, p. 117101, 2024.


[45] I. Skorokhodov, S. Tulyakov, and M. Elhoseiny, “Stylegan-v: A continuous video generator with the price, image
quality and perks of stylegan2,” in _Proceedings_ _of_ _the_ _IEEE/CVF_ _conference_ _on_ _computer_ _vision_ _and_ _pattern_
_recognition_, 2022, pp. 3626–3636.


[46] Z. Huang, Y. He, J. Yu, F. Zhang, C. Si, Y. Jiang, Y. Zhang, T. Wu, Q. Jin, N. Chanpaisit _et_ _al._, “Vbench:
Comprehensive benchmark suite for video generative models,” in _Proceedings_ _of_ _the_ _IEEE/CVF_ _Conference_ _on_
_Computer_ _Vision_ _and_ _Pattern_ _Recognition_, 2024, pp. 21 807–21 818.


12


[47] D. Zheng, Z. Huang, H. Liu, K. Zou, Y. He, F. Zhang, L. Gu, Y. Zhang, J. He, W.-S. Zheng _et_ _al._, “Vbench-2.0:
Advancing video generation benchmark suite for intrinsic faithfulness,” _arXiv_ _preprint_ _arXiv:2503.21755_, 2025.


[48] Z. Huang, F. Zhang, X. Xu, Y. He, J. Yu, Z. Dong, Q. Ma, N. Chanpaisit, C. Si, Y. Jiang _et_ _al._, “Vbench++:
Comprehensive and versatile benchmark suite for video generative models,” _IEEE_ _Transactions_ _on_ _Pattern_
_Analysis_ _and_ _Machine_ _Intelligence_, 2025.


[49] H. Duan, H.-X. Yu, S. Chen, L. Fei-Fei, and J. Wu, “Worldscore: A unified evaluation benchmark for world
generation,” in _Proceedings_ _of_ _the_ _IEEE/CVF_ _International_ _Conference_ _on_ _Computer_ _Vision_, 2025, pp. 27 713–
27 724.


[50] S. Su, M. Delbracio, J. Wang, G. Sapiro, W. Heidrich, and O. Wang, “Deep video deblurring for hand-held
cameras,” in _Proceedings_ _of_ _the_ _IEEE_ _conference_ _on_ _computer_ _vision_ _and_ _pattern_ _recognition_, 2017, pp. 1279–1288.


[51] D. Danier, F. Zhang, and D. R. Bull, “Bvi-vfi: A video quality database for video frame interpolation,” _IEEE_
_Transactions_ _on_ _Image_ _Processing_, vol. 32, pp. 6004–6019, 2023.


[52] A. Mercat, M. Viitanen, and J. Vanne, “Uvg dataset: 50/120fps 4k sequences for video codec analysis and
development,” in _Proceedings_ _of_ _the_ _11th_ _ACM_ _multimedia_ _systems_ _conference_, 2020, pp. 297–302.


[53] V. Ramanishka, Y.-T. Chen, T. Misu, and K. Saenko, “Toward driving scene understanding: A dataset for learning
driver behavior and causal reasoning,” in _Proceedings_ _of_ _the_ _IEEE_ _Conference_ _on_ _Computer_ _Vision_ _and_ _Pattern_
_Recognition_, 2018, pp. 7699–7707.


[54] D. Mehta, H. Rhodin, D. Casas, P. Fua, O. Sotnychenko, W. Xu, and C. Theobalt, “Monocular 3d human pose
estimation in the wild using improved cnn supervision,” in _2017_ _international_ _conference_ _on_ _3D_ _vision_ _(3DV)_ .
IEEE, 2017, pp. 506–516.


[55] Z. Huang, T. Zhang, W. Heng, B. Shi, and S. Zhou, “Real-time intermediate flow estimation for video frame
interpolation,” in _Proceedings_ _of_ _the_ _European_ _Conference_ _on_ _Computer_ _Vision_ _(ECCV)_, 2022.


[56] C.-K. Liang, Y.-C. Peng, and H. Chen, “Rolling shutter distortion correction,” in _Visual_ _Communications_ _and_
_Image_ _Processing_ _2005_, vol. 5960. SPIE, 2005, pp. 1315–1322.


[57] J. Liu, J. Han, B. Yan, H. Wu, F. Zhu, X. Wang, Y. Jiang, B. Peng, and Z. Yuan, “Infinitystar: Unified spacetime
autoregressive modeling for visual generation,” _arXiv_ _preprint_ _arXiv:2511.04675_, 2025.


[58] DeepMind, “Veo 3 technical report,” DeepMind, Technical Report, 2025, accessed: 2026-02-18. [Online]. Available:

[https://storage.googleapis.com/deepmind-media/veo/Veo-3-Tech-Report.pdf](https://storage.googleapis.com/deepmind-media/veo/Veo-3-Tech-Report.pdf)


[59] OpenAI, “Sora: Creating video from text,” 2024.


[60] xAI, “Grok Imagine - ai image & video generation by xai,” 2026.


[61] Kling AI, “Kling AI Omni / VIDEO O1 creative interface,” 2025.


[62] ByteDance Seed Team, “ByteDance Seed: Models and research,” [https://seed.bytedance.com/,](https://seed.bytedance.com/) 2025, accessed:
2026-02-27.


[63] R. A. Bradley and M. E. Terry, “Rank analysis of incomplete block designs: I. the method of paired comparisons,”
_Biometrika_, vol. 39, no. 3/4, pp. 324–345, 1952.


[64] Google DeepMind, “Gemini 3.1 - deepmind ai model,” 2025.


[65] A. Yang, A. Li, B. Yang, B. Zhang, B. Hui, B. Zheng, B. Yu, C. Gao, C. Huang, C. Lv _et_ _al._, “Qwen3 technical
report,” _arXiv_ _preprint_ _arXiv:2505.09388_, 2025.


13


