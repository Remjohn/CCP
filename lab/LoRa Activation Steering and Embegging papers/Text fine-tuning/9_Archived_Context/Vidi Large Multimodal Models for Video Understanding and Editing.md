# **Vidi: Large Multimodal Models for Video** **Understanding and Editing**

Intelligent Editing Team [∗], Intelligent Creation, ByteDance Inc.
San Jose/Seattle, US
```
         https://bytedance.github.io/vidi-website/

### **Abstract**

```

Humans naturally share information with those they are connected to, and video has become one of the
dominant mediums for communication and expression on the Internet. To support the creation of highquality large-scale video content, a modern pipeline requires a comprehensive understanding of both the
raw input materials ( _e.g._, the unedited footage captured by cameras) and the editing components ( _e.g._,
visual effects). In video editing scenarios, models must process multiple modalities ( _e.g._, vision, audio, text)
with strong background knowledge and handle flexible input lengths ( _e.g._, hour-long raw videos), which
poses significant challenges for traditional models. In this report, we introduce Vidi, a family of Large
Multimodal Models (LMMs) for a wide range of video understand editing scenarios. The first release focuses
on temporal retrieval, _i.e._, identifying the time ranges within the input videos corresponding to a given text
query, which plays a critical role in intelligent editing. The model is capable of processing hour-long videos
with strong temporal understanding capability, _e.g._, retrieve time ranges for certain queries. To support a
comprehensive evaluation in real-world scenarios, we also present the VUE-TR benchmark, which introduces
five key advancements: 1) **Video** **duration** : spans from 20 seconds to over an hour, which is significantly
longer than existing temporal/moment retrieval datasets. 2) **Audio** **support** : includes audio-based queries
for temporal retrieval. 3) **Query format** : accommodates three different query lengths/formats, _i.e._, keyword,
phrase, and sentence. 4) **Annotation** **quality** : all ground-truth time ranges are manually annotated with
high accuracy. 5) **Evaluation metric** : a refined IoU metric designed to support evaluation over multiple time
ranges. Remarkably, Vidi significantly outperforms leading proprietary models, _e.g._, GPT-4o and Gemini,
on the temporal retrieval task, indicating its superiority in video editing scenarios.
#### **Vidi-1.5 Vidi Gemini-2.0-Flash Gemini-2.5-Pro-0325 GPT-4o**



60


50


40


30


20


10


0





















**Ultra-Short**

**<1 min**



**Short**
**1-10 mins**



**Medium**
**10-30 mins**



**Long**
**30-60 mins**



**Ultra-long**

**>60 mins**



Figure 1: Temporal retrieval accuracy of different models on the proposed VUE-TR benchmark.


∗A detailed contributor list can be found in Section 10.


1


### **1 Introduction**

Video has become one of the most dominant mediums for sharing information on the Internet. However,
for most users, video creation remains a complex and time-consuming process, especially on mobile devices
where precise editing is challenging. Among all editing stages, the most laborious step is often identifying
the desired segments with long, unedited footage. Beyond trimming, users frequently struggle with video
composition tasks, such as selecting appropriate music, transitions, effects, animations, filters, stickers, and
fonts, which require both technical skill and artistic judgment. Moreover, creative editing actions beyond
composition are increasingly important in modern video production but are even harder to achieve without
expert tools or AI assistance, _e.g._, generating thumbnails, cover art or stylized scenes. _We_ _aim_ _to_ _build_ _the_
_next_ _generation_ _of_ _video_ _creation_ _systems_ _powered_ _by_ _advanced_ _video_ _understanding_ _and_ _editing_ _capabilities,_
_enabling_ _users_ _to_ _complete_ _complex_ _editing_ _workflows_ _automatically_ _and_ _effortlessly._
In this release, we present Vidi, a large multimodal model for video understanding and editing ( **VUE** )
with a particular focus on the temporal retrieval ( **TR** ) task. Vidi takes text, vision, and audio as input
modalities and retrieves the most relevant time ranges corresponding to a natural language query. A key
strength of our model lies in its ability to handle hour-long input videos, significantly surpassing the duration
constraints of existing academic temporal/moment retrieval datasets [6, 12, 9, 14, 7], which typically cap at
around 150 seconds.
To support comprehensive evaluation in realistic settings, we introduce a manually annotated benchmark
(abbreviated VUE-TR) for temporal retrieval. VUE-TR consists of videos ranging from approximately 20
seconds to over 1 hour, categorized into five groups: ultra-short ( _<_ 1 min), short (1 _−_ 10 mins), medium
(10 _−_ 30 mins), long (30 _−_ 60 mins) and ultra-long ( _>_ 1 hour). Each video is paired with queries of varying
formats and lengths ( _i.e._, keyword, phrase, and sentence) to reflect the diversity of the user search intent.
Critically, queries may require visual, audio, or both modalities for accurate localization. This aligns closely
with real-world scenarios, where audio plays an essential role in video comprehension, particularly in domains
such as TV shows, broadcasts, and musical performances. As illustrated in Figure 2, we present an example
of an hour-long video with three queries, covering different formats and modalities. Remarkably, Vidi-7B
significantly surpasses leading Large Multimodal Models (LMMs), such as Gemini and GPT-4o, highlighting
its effectiveness in handling complex multimodal temporal retrieval tasks. Building upon this success, Vidi1.5-9B achieves further performance gains through an enhanced LLM backbone, an upgraded visual encoder,
an adaptive token compression strategy, and the incorporation of additional high-quality training data.


**00:07:45** **00:15:31** **00:25:26** **00:49:16** **01:01:44**


**Query (Vision, keyword): A horse**
**Time Range: 00:15:17 – 00:15:48**


**Query (Audio, phrase): fall asleep on bike**
**Time Rages: 00:07:44 – 00:07:47**


**Query (Vision+Audio, sentence): During a virtual meeting, a man**
**recounts a memory during a time when he ate testicles of different**
**animals which he found to be too big and described it as horrendous.**
**Time Ranges: 00:49:06 – 00:49:28**


Figure 2: Examples of temporal retrieval queries and their corresponding time ranges from the
proposed VUE-TR benchmark. The duration of the example video is 3 _,_ 871 seconds ( _i.e._, 01:04:31).
Each query is presented in one of three formats ( _i.e._, keyword, phrase, sentence) with visual or
audio information. Facial regions in the video frames are blurred to protect privacy.


2


### **2 General Overview**

Figure 3 illustrates the model architecture of Vidi. For LLM training, we adopt the decomposed attention
mechanism proposed by Kuo _et_ _al._ [13], which reduces the computational complexity over multimodal tokens
_N_ from _O_ ( _N_ [2] ) to _O_ ( _N_ ) without sacrificing performance on downstream multimodal tasks. This efficient
attention design enables training and inference in extremely long videos, which are otherwise infeasible for
standard transformer-based models [28]. All videos are uniformly sampled at 1 frames per second (fps) for
visual input and 16 _,_ 000 Hz for audio, ensuring that the model can localize and understand content with
second-level precision.


Text Output

0:14:11-0:14:18, 0:14:56-0:15:00

#### LLM + Decomposed Attention


Audio Adapter Vision Adapter


Audio Visual Tokenizer


“Street scene with cars”



Audio Input





Text Input



Figure 3: An overview of the Vidi architecture. Raw visual and audio inputs are first process by
pretrained modality-specific encoders to extract token sequences. A multimodal adapter is applied
to both the visual and audio branches to compress the token sequences and project them into the
input space of the pretrained LLM [11, 25]. Notably, the LLM operates using the decomposed
attention [13] to enable efficient and scalable modeling over long, densely sampled multimodal
sequences.


Training of Vidi is carried out in two main stages to ensure strong multimodal temporal retrieval:


  - **Multimodal Alignment** : This stage focuses on aligning vision and audio data with the corresponding
text descriptions and timestamps. We first train the vision and audio adapters using visual and audio
captioning data, while keeping the rest of the model frozen. Then the LLM and adapters are jointly
trained on synthetic video/audio data with ground-truth time ranges, allowing the model to learn
multimodal-to-temporal grounding. Finally, the model is fine-tuned using real videos, with supervision
from paired ( _i.e._, timestamp and caption/ASR) data to narrow the domain gap between synthetic and
in-the-wild content.


  - **Application** **Post-training** : To support diverse application scenarios, we further fine-tune the model
on task-specific data, including temporal retrieval and video/image VQA. The temporal retrieval training data mirror the structure of the VUE-TR benchmark, with queries in three formats ( _i.e._, keyword,
phrase, sentence), requiring information from vision, audio, or both. This stage enhances the model’s
ability to handle real-word usage patterns where query types vary significantly.


Depending on the intended use case, we train different versions of Vidi, with custom training recipes, _e.g._, a
temporal retrieval expert model, and a more generic VQA model (to be included in future releases). During
inference, Vidi is capable of running on a single 80G GPU without quantization, and efficiently process videos
exceeding 2 hours in length, making it practical for real-world deployment in long-form video editing and
retrieval tasks.


3


### **3 Model Architecture**

Unlike generic video understanding tasks that rely on sparse or uniform sampling of a fixed number of frames,
temporal retrieval requires models to localize relevant segments with second-level precision, necessitating
dense sampling, typically at 1 fps. Under this fixed sampling rate, the multimodal inputs ( _e.g._, vision,
audio, and text) can vary significantly in length, ranging from ultra-short of just a few seconds to ultra-long
exceeding an hour. Furthermore, our proposed VUE-TR benchmark emphasizes realistic retrieval conditions
by requiring models to process both visual and audio modalities when localizing queries. To address challenges
in handling videos with varying length and multimodal inputs at scale, we adopt the Decomposed Attention
( **D-Attn** ) [13] architecture in Vidi. D-Attn offers exceptional computational efficiency while maintaining
strong multimodal capabilities. It also facilitates seamless integration of visual, audio, and textual streams,
making it well suited for temporal retrieval in long-form, real-world videos.
As shown in Figure 3, the visual and audio inputs are first encoded into token sequences using pretrained visual and audio encoders, respectively. The resulting multimodal embeddings are projected with
corresponding adapter layers. Together with the text query embeddings, they are fed into a D-Attn LLM,
which localizes the text query within the input video.

As illustrated in Figure 4, D-Attn is an architectural adaptation of modern pretrained LLMs,
#### where causal self-attention within an LLM is To

equivalently decomposed into visual-to-visual self
v v v v v v v T T T T T

attention (V2V Self-Attn), textual-to-textual self
v

attention (T2T Self-Attn), and textual-to-visual

v

cross-attention (T2V Cross-Attn). With this de
v

v

T2V Cross-Attn to enhance multimodal perfor
v

mance and computational efficiency, while preserv
v

ing the capabilities of the pretrained LLM.

T

From a computational point of view, a diagonal variant of V2V Self-Attn is proposed to retain T

T2V T2T

performance while reducing the complexity from T

Cross-Attn Self-Attn

_O_ ( _N_ [2] ) to _O_ ( _N_ ) for the visual tokens _N_, shown in T
Figure 4. This lightweight design is particularly

T

well suited for densely sampled, ultra-long videos,
where _N_ might be extremely large. For example,
if each frame consists of 400 tokens, a one-hour

Figure 4: Decomposed Attention [13] equiva
video would have 1.44M tokens. Such input length

lently decomposes causal self-attention in an LLM

is challenging for conventional fully self-attention

into three components: visual-to-visual (V2V),

mechanisms.
In terms of multimodal alignment, Kuo _et_ textual-to-textual (T2T), and textual-to-visual
_al._ [13] identify a critical issue: positional bias (T2V) attentions.
between text and visual tokens can hinder the
model’s ability to establish comprehensive understanding of multimodal contents. To address this, a debiased
positional encoding strategy is proposed to remove positional encodings from T2V Cross-Attn, eliminating
the undesirable bias. This approach yields consistent improvements across a wide range of downstream
tasks. By integrating both diagonal V2V Self-Attn and debiased positional encodings in T2V Cross-Attn,
the resulting D-Attn LLM can process multimodal tokens longer than the pretrained LLM’s original context
length. Please refer to Kuo _et_ _al._ [13] for more details.
To effectively address the challenge of varying-length video input, we modify the _α_ -weighting strategy used
in the D-Attn framework. This adjustment is designed to balance the contributions of textual and multimodal
information. In particular, video lengths (and thus token counts) can vary significantly in the context of
temporal retrieval. In D-Attn, Kuo _et_ _al._ [13] analytically derive how self-attention can be equivalently
decomposed into a weighted sum of T2T Self-Attn and T2V Cross-Attn. Given a text token _t_ and a sequence


#### To



v v v v v v v T T T T T



v
v

v
v
v

v
v

T

T

T

T

T



None



T2V
Cross-Attn



T2T
Self-Attn



Figure 4: Decomposed Attention [13] equivalently decomposes causal self-attention in an LLM
into three components: visual-to-visual (V2V),
textual-to-textual (T2T), and textual-to-visual
(T2V) attentions.



4


of concatenated visual and textual tokens [ _V, T_ ], the attention from _t_ to [ _V, T_ ] can be formulated as


`Attn` ( _t,_ [ _V, T_ ]) = _αV_ `XA` ( _t, V_ ) + _αT_ `SA` ( _t, T_ ) _,_ (1)


where _αV_ = `Sigmoid` ( _SV_ _−_ _ST_ ), _αT_ = `Sigmoid` ( _ST_ _−_ _SV_ ) = 1 _−_ _αV_ . _V_ = [ _v_ 1 _, v_ 2 _, · · ·_ _, vN_ ] and _T_ =

[ _t_ 1 _, t_ 2 _, · · ·_ _, tM_ ] represent a sequence of visual and text tokens, respectively. _SV_ and _ST_ are defined as the
logarithmic sum of the exponential of the dot product between _t_ and _V_, and between _t_ and _T_, respectively.



_SV_ = log




- _N_ 
 - _e_ _**[q]**_ _[t][·]_ _**[k]**_ _[vn]_


_n_



, and _ST_ = log




- _M_ 
 - _e_ _**[q]**_ _[t][·]_ _**[k]**_ _[tm]_


_m_



_,_ (2)



where _N_ is the number of visual tokens and _M_ is the number of text tokens. In the temporal retrieval
task, this formulation leads to an imbalance: while the length of the text query _M_ typically stays within
a small range, the count of visual tokens _N_ can vary dramatically due to differences in the duration of the
video. As a result, _SV_ tends to be significantly larger for longer videos, which in turn biases _αV_ towards 1
and _αT_ towards 0. This causes the model to overemphasize visual input while neglecting the textual query,
potentially degrading performance. To mitigate this issue, we simplify the formulation in Vidi by fixing
the weighting coefficients, _i.e._, _αV_ = _αT_ = 1. This ensures a balanced contribution from both modalities,
regardless of the input video length.
The D-Attn framework can be trivially generalized to accommodate audio inputs. Given audio tokens
_A_ = [ _a_ 1 _, a_ 2 _, · · ·_ _, aP_ ], the attention of a text token _t_ to the combined multimodal sequence [ _V, A, T_ ] can be
similarly derived as


`Attn` ( _t,_ [ _V, A, T_ ]) = _αV_ `XA` ( _t, V_ ) + _αA_ `XA` ( _t, A_ ) + _αT_ `SA` ( _t, T_ ) (3)

_≃_ `XA` ( _t, V_ ) + `XA` ( _t, A_ ) + `SA` ( _t, T_ ) _,_ (4)


where we set _α_ -weightings _αV_ = _αA_ = _αT_ = 1. In practice, we observe that this fixed-weight decomposition
significantly improves training stability, accelerates convergence, and yields better performance than both
the original _α_ -adaptive formulation and fully self-attention.

### **4 Multimodal Alignment**


To align the multimodal inputs (vision and audio) with the corresponding timestamps and text in either the
inputs or outputs, we adopt a three-stage training strategy: 1) adapter training, 2) synthetic data training,
and 3) real video training.


**4.1** **Adapter** **Training**


In this stage, we train the adapters from scratch while keeping the weight of the vision/audio encoders and the
LLM fixed. Each adapter contains a convolution layer for compressing the raw visual or audio tokens, followed
by an MLP that maps the compressed representations into the LLM-compatible input space. We leverage
the strong publicly available pretrained models for all other components: SigLIP series [35, 27] for vision,
Whisper [22] for audio, and Mistral [11]/Gemma [25] for the language model backbone. The adapters are
trained on approximately 1 million image and audio caption data, allowing them to learn semantic grounding
across modalities while maintaining alignment with the LLM.


**4.2** **Synthetic** **Data** **Training**


To support large-scale training for temporal alignment, we propose a synthetic video generation pipeline
based on captioned video and audio datasets with ground-truth timestamps. As shown in Figure 5, we begin
by randomly sampling a group of candidate samples from large-scale caption corpora, _i.e._, approximately 25
million images and 400 thousand audio clips. Each image is expanded into a synthetic video segment using a
sliding window approach with randomized parameters such as window size, starting corner, sliding direction,
and sliding speed. This mimics camera movement or visual variation over time. Similarly, audio clips are
segmented and spliced in random order to create synthetic audio tracks. The resulting synthetic inputs are


5


Synthetic Long Audio


Figure 5: An overview of the synthetic training data generation pipeline. Visual and audio segments
can be duplicated at multiple timestamps to simulate real videos.


arbitrarily long and composed of diverse multimodal segments. Since each segment originates from a known
captioned sample, we can automatically generate large-scale (timestamp, caption) pairs as supervision. Since
images do not match audio, the training input contains only one active modality (vision or audio), while the
other is padded with empty tokens.
We train the model on two complementary objectives: 1) caption prediction: given a timestamp range,
predict the corresponding caption; 2) timestamp localization: given a caption, predict the matching timestamp range. These dual tasks help the model develop a deep understanding of both visual/audio content
and the temporal axis. After training on synthetic data, the model achieves over 80% accuracy on a synthetic evaluation set with multi-minute sequences, indicating strong alignment capability and robust temporal
grounding.


**4.3** **Real** **Video** **Training**


To bridge the gap between synthetic videos and real-world videos, we further train the model on a large
corpus of 1 million long videos, each annotated with dense supervision in the form of pairs (timestamp,
caption) and (timestamp, subtitle). As shown in Figure 6, each long video is first segmented into short
clips (typically 5 _−_ 30 _s_ ) using a combination of scene boundary detection [16] and subtitle punctuation cues

[8]. This process yields approximately 3 _−_ 500 segments per video, depending on the density and duration
of the content. After that, dense captions are generated with state-of-the-art LMMs [3, 37], resulting in
fine-grained semantic coverage. Original subtitles are reprocessed into sentence-level units using punctuationbased splitting, enhancing their suitability for timestamped supervision. This pipeline produces more than 30
million paired training samples (timestamp, caption) and (timestamp, subtitle). The training input consists
of raw video files containing both visual and audio tracks.
We design four training objectives to fully leverage aligned supervision.


  - Caption prediction: given a timestamp range, predict the corresponding dense caption.


  - Subtitle prediction: given a timestamp range, predict the associated sentence-level subtitle.


  - Caption-based localization: given a caption, predict the matching timestamp range.


  - Subtitle-based localization: given a sentence-level subtitle, predict the corresponding timestamp range.


These tasks not only reinforce the model’s ability to align textual descriptions with multimodal signals, but
also help it adapt to complex video/audio in real-world distributions.


6


Caption: The man waves the
Belgian flag to start a race, a
line of race cars drives past him
on a race track.


LMM



Caption: The video shows a thrilling
moment in a Formula E race, with
multiple cars navigating a turn on the
track, showcasing the intensity and
speed of the competition.



LMM LMM LMM



Caption: A thrilling race car drive
on a track, showcasing the driver's
perspective as they navigate
through the course.



Caption: The video captures a
celebratory moment on a podium
where race car drivers and teams
are raising their trophies and waving
flags, signifying their victory in the 6
Hours of Spa-Francorchamps race.



……



……



……



00:00:05 – 00:00:13 00:01:52 – 00:02:04 00:08:22 – 00:08:34 00:12:00 – 00:12:07



00:01:52 – 00:02:04



00:08:22 – 00:08:34



Scene Boundary Detection


Figure 6: An overview of the proposed real video training data generation pipeline. Long videos
are first segmented into short clips using scene boundary detection and subtitle punctuation. Then,
existing LMMs are used to generate dense, timestamp-aligned captions for each clip, resulting in
high-quality supervision for real-world temporal grounding tasks.

### **5 Application Post-training**


To support the temporal retrieval task, we build an annotation pipeline to generate user-like search queries
and ground-truth timestamps to guide the training phase. As shown in Figure 7, we take advantage of the
video clip split in Section 4.3 with dense captions to generate user-style queries and timestamp ranges.


**Dense** **Captions.** Similar to [30], we generate structural captions to maintain the consistency of text-clip
and cover the details in each video clip. Specifically, each caption contains six aspects: 1) subjects of the
video, 2) actions of the subjects, 3) scene environment where the action takes place and all visual text overlay
on-screen, including logos, subtitles, signs, or other writings, 4) visual style or special effects including video
effects, animation, style, composition, and lighting, 5) camera parameters including camera motion, angles,
and focal length, 6) background knowledge for common sense reasoning such as famous landmarks, celebrities,
or historical events.


**Query** **and** **Timestamp** **Pairs.** To generate high-quality query–timestamp pairs for long videos, we use
chain-of-thought (CoT) [32] prompting of LLM. We first combine detailed dense captions and subtitles with
timestamps from all video segments to provide a comprehensive textual representation of the video’s content.
The aggregated text is sent to a pretrained LLM. The LLM is used to generate a concise summary to capture
the key events and themes with the guidance from the CoT prompting to comprehend the context of the
video. In this way, CoT prompting enables the model to perform intermediate reasoning, leading to a more
accurate and coherent understanding of video content.
To improve format diversity and better simulate real-word scenarios, we generate queries in three levels
of granularity:


  - **keyword** : concise terms representing objects, concepts or entities, such as “love”, “coffee making
process”, and “washing machine”.


  - **phrase** : short descriptions capturing actions or states, like “a man riding a bike”, “person in deep
thought”, and “enjoying a swim in the pool”.


7


  - **sentence** : complete sentence(s) describing detailed events or scenes, _e.g._, “The majestic presence of a
volcano surrounded by lush vegetation and shrouded in clouds”.


**Post-processing** **and** **Filtering.** We design a rule-based post-processing step to enhance the quality of
generated queries and the corresponding time ranges, formed by the following stages. 1. Merging adjacent
time ranges: for each query, we combine consecutive time segments or those separated by small gaps ( _e.g._,
0 _._ 5 seconds), provided the query appearing in captions or subtitles. 2. Filtering out low-confidence queries:
queries with confidence scores below 0 _._ 9 are discarded to ensure reliability. 3. Excluding overly general
queries: queries associated with more than 10 timestamps are considered too general. We remove such
cases that frequently appear throughout the video. 4. Eliminating machine-style queries: queries exhibiting
templated or unnatural phrasing, such as “The video concludes...” or “In the closing moments,” will be
filtered out to ensure quality. After that, the generated queries and the corresponding time ranges are sent
to human annotators to perform the final stage verification and modification.



Final Time Range: 00:08:29 – 00:08:32


Final Query (Sentence): cars are
allowed to spin tires in the pit lane.


Human Annotator


Initial Time Range: 00:08:22 – 00:08:34
Initial Query: During the race, in the pit
lane, cars are allowed to spin all four
tires, showcasing a specific regulation
or adaptability in racing scenarios.



Final Time Range: 00:10:46 – 00:10:49


Final Query (Phrase): Kamui Kobayashi
wins for Toyota


Human Annotator


Initial Time Range: 00:10:45 – 00:10:55
Initial Query: Kamui Kobayashi wins for
Toyota



Final Time Range: 00:11:51 – 00:11:52,
00:12:07 – 00:12:12
Final Query (Keyword): podium
celebration


Human Annotator


Initial Time Range: 00:12:00 – 00:12:07
Initial Query: podium celebration















00:08:22 – 00:08:34 00:10:45 – 00:10:55
00:12:00 – 00:12:07


Figure 7: An illustration of post-training data generation pipeline for temporal retrieval. Queries
of varying formats (keywords, phrases, and sentences) are constructed and paired with timestamp
annotations from real videos.


**Two-Round** **Human** **Annotation.** Although involving a filtering process, generated queries and the
corresponding time ranges still contain ambiguity of phrasing and misaligned timestamps. To obtain highquality annotations, we further design a comprehensive human-in-the-loop refinement process. Annotators
begin by examining each query for clarity and relevance. If a query is ambiguous or unrealistic, it is required
to be rewritten to reflect the video content accurately. After that, the annotators review the entire video
to identify precise time segments corresponding to the refined queries. In addition, another annotator is
required to review the annotations independently. Discrepancies identified during this phase will be resolved
through discussion or by consulting a senior annotator.
It is worth mentioning that each query is annotated based on its reliance on visual and/or auditory information. Annotators assign one of the following modality tags to each query: vision, audio, or vision+audio.


  - **Vision** . The query can be accurately identified purely on the basis of visual content. Audio information
is not necessary to retrieve the segments.


8


  - **Audio** . The query depends solely on the auditory information. Visual cues are not necessary to
identify the video segment.


  - **Vision+Audio** . The query relies on visual and auditory information for accurate interpretation and
localization within the video.


This categorization strategy helps researchers evaluate the capabilities of the models with a more detailed
analysis.

### **6 Evaluation Benchmark**


We introduce VUE-TR, a new evaluation benchmark specifically designed to advance temporal retrieval
in real-world scenarios. VUE-TR addresses five critical aspects often overlooked in prior academic benchmarks [6, 12, 9, 14, 7]: **video** **duration**, **audio** **support**, **query** **format**, **annotation** **quality**, and **metric**
**design** . To ensure high-quality supervision, all annotations are manually curated using a robust annotation
pipeline described in Section 5, which yields significantly more accurate and consistent labels than existing
benchmarks.

|Ultra-short Short Medium Long Ultra-long<br>Duration Category Total<br>< 1 min 1 −10 mins 10 −30 mins 30 −60 mins > 60 mins|Col2|Col3|
|---|---|---|
|# Videos<br># Queries<br>Video Hours|63<br>150<br>150<br>50<br>15<br>183<br>439<br>427<br>396<br>153<br>0.81<br>11.71<br>43.71<br>34.17<br>17.48|428<br>1,598<br>107.87|



Table 1: Duration distribution of videos in the proposed VUE-TR evaluation benchmark. The
dataset covers a wide range of video lengths, from ultra-short clips ( _<_ 1 minute) to ultra-long
videos ( _>_ 1 hour), enabling comprehensive evaluation of temporal retrieval models across diverse
real-world scenarios.



**Query Modality**



**Query Format**















Vision Audio Vision+Audio





Figure 8: The distribution of query modality and format in the VUE-TR benchmark. This diverse
distribution reflects real-world retrieval scenarios and enables fine-grained analysis of model performance across input types.


**6.1** **Data** **Statistics**


VUE-TR is built using publicly available videos, and the annotations are made accessible to foster open
research. As presented in Table 1 and Figure 8, the benchmark consists of 1 _,_ 598 queries across 428 videos,
spanning over 107 hours. It supports attribute-based slicing for fine-grained performance analysis as follows.


9


  - **Video** **Duration.** Unlike prior datasets limited to short clips, the video length varies from 20 seconds
to more than 1 hour, covering the full spectrum of durations encountered in real-world scenarios. To
facilitate duration-wise evaluation, we categorize videos into five balanced buckets: ultra-short ( _<_ 1
min), short (1 _−_ 10 mins), medium (10 _−_ 30 mins), long (30 _−_ 60 mins) and ultra-long ( _>_ 60 mins). It
enables systematic analysis of model performance as the video length increases, which is a key challenge
for temporal retrieval that prior work failed to capture.


  - **Query** **Modality.** While most large vision-language models (LVLMs) operate on vision and text
alone, VUE-TR explicitly integrates audio as a core input modality. As shown in Figure 8 (left), 47%
of the queries involve both visual and audio signals, 35% are vision-only, and 18% are audio-only. This
breakdown enables a comprehensive evaluation of multimodal capabilities.


  - **Query** **Format.** VUE-TR is the first temporal retrieval benchmark to incorporate multiple query
formats, reflecting the diversity of user intent in real-word search scenarios. The three formats, ranging
from keywords to free form sentences, are carefully balanced, as shown in Figure 8 (right). Then the
model can be evaluated to handle queries of varying linguistic complexity.


**6.2** **Evaluation** **Metric**


To support evaluation of generic temporal retrieval involving multiple timestamp ranges, we re-define **IoU**
(Intersection over Union), **precision**, and **recall** along the time axis. As illustrated in Figure 9, the IoU is
computed based on the intersection and the union between the predicted time intervals and ground-truth.


**Prediction**


**Ground-truth**


**Intersection**


**Union**


Figure 9: Definition of intersection and union for temporal retrieval. Both prediction and groundtruth annotations may contain multiple timestamp ranges. The IoU for each sample is computed
as [�] _I_ ( _TP, TG_ ) _/_ [�] _U_ ( _TP, TG_ ).



For each sample, we compute precision _P_, recall _R_ and IoU as the core evaluation metrics. According to
the definition in Equation (5), a perfect prediction would be exactly the same as the ground-truth timestamp
ranges, _i.e._, _P_ = _R_ = IoU = 1. To capture performance across varying levels of overlap, we sweep thresholds
in the range [0 _,_ 1] to generate accuracy-threshold curves. We then compute the area under curve (AUC)
for each metric, denoted as _P_ [¯], _R_ [¯], IoU,¯ which serve as the final evaluation scores. Although AUC provides
a comprehensive summary, the user experience in real-world applications often depends on performance as
specific thresholds, _e.g._, IoU@0.5. Therefore, we also report accuracy-threshold curves (see Figure 10) to
facilitate a more detailed analysis, while treating AUC as the primary metric for evaluation.
 _P_ =                                           - _I_ ( _TP, TG_ ) _/_                                           - _TP,_



_P_ = - _I_ ( _TP, TG_ ) _/_ - _TP,_

_R_ = - _I_ ( _TP, TG_ ) _/_ - _TG,_



(5)



IoU = - _I_ ( _TP, TG_ ) _/_ - _U_ ( _TP, TG_ ) _,_



where _I_ ( _·, ·_ ) and _U_ ( _·, ·_ ) denote the interaction and union function between predicted timestamps _TP_ and
ground-truth _TG_, respectively. The summation is taken over all overlapping time intervals between prediction
and ground-truth.


10


### **7 Experiment**

**7.1** **Implementation** **Details**


**Adapter** **Synthetic** **&** **Real** **Videos** **Post** **Training**


lr adapter 1e-3 5e-6 5e-6

lr llm frozen 2e-6 2e-6

mm encoders frozen frozen frozen

video duration 10-600 secs 10-1800 secs 10-1800 secs

weight decay 0.0 0.0 0.0

optimizer AdamW [20] AdamW [20] AdamW [20]

optimizer _β_ 1 default (0.9) default default

optimizer _β_ 2 default (0.999) default default

optimizer _ϵ_ default (1e-8) default default

training steps 2k 10k 1 epoch

lr scheduler cosine cosine cosine

total batch size 128 128 128

dtype bfloat16 bfloat16 bfloat16

deepspeed stage 2 stage 3 stage 3

gradient ckpt off on on


Table 2: Training configurations and hyper-parameters used across different training stages for Vidi.


We implement the released Vidi models using three core components: the visual encoder ( `google/siglip`
`-so400m-patch14-384` [35] for Vidi, and `google/siglip2-so400m-patch14-384` [27] for Vidi-1.5, the audio
encoder `openai/whisper-large-v3` [22], and the language model ( `mistralai/Mistral-7B-Instruct-v0.3`

[11] for Vidi, and `google/gemma-2-9b` [25] for Vidi-1.5). Unlike existing video LLMs that use a fixed number
of uniformly sampled frames, Vidi adopts modality-specific fixed sampling rates: 1 _._ 0 fps for video frames
and 16 _,_ 000 Hz for audio signals. It ensures sufficient coverage of fine-grained visual and auditory details
across varying video durations. After sampling, each image frame is independently encoded by SigLip to
convert it into a sequence of visual tokens. In parallel, the audio waveform is segmented into batches,
each independently encoded by Whisper, and then concatenated back into a sequence of audio tokens. The
complete set of training configurations and hyper-parameters for various stages is provided in Table 2.


**7.2** **Temporal** **Retrieval** **Results**


We compare our model with three state-of-the-art proprietary models including GPT-4o [10], Gemini-2.0Flash [1] and Gemini-2.5-Pro [1]. There models are chosen for their strong performance and broad modality
support, making them competitive baselines for real-world temporal retrieval.
Since GPT-4o API does not support audio, we extract frames at 1 fps and feed them as input images. To
adapt GPT-4o for temporal retrieval, we design a simple custom prompt with in-context examples, ensuring
that the output only contains frame index ranges. An example instruction is as follows:

```
   The input images are frames from a video. Output the frame indexes that correspond
   to the text query: "QUERY". Only output the index range, for example, 2-4, 6-8.

```

We observe that GPT-4o follows this prompt reliably, typically producing clean and parseable frame ranges,
which are then converted into time intervals for evaluation.


11


|Category Metric Vidi-1.5 Vidi Gemini-2.0-Flash† Gemini-2.5-Pro† GPT-4o‡|Col2|
|---|---|
|Ultra-Short (_<_ 1_m_)<br>¯_P_<br>¯_R_<br>¯<br>IoU<br>|70.7<br>64.5<br>**72.3**<br>58.8<br>53.6<br>76.2<br>**79.6**<br>65.4<br>69.2<br>42.1<br>**58.4**<br>54.6<br>49.2<br>42.6<br>32.5|
|Short (1_ −_10_m_)<br>¯_P_<br>¯_R_<br>¯<br>IoU<br>|**60.5**<br>57.4<br>51.7<br>43.3<br>30.0<br>**63.4**<br>55.8<br>50.6<br>41.7<br>26.5<br>**44.1**<br>40.5<br>31.6<br>22.7<br>15.6|
|Medium (10_ −_30_m_)<br>¯_P_<br>¯_R_<br>¯<br>IoU<br>|**53.8**<br>47.4<br>35.1<br>31.1<br>18.2<br>**54.0**<br>46.6<br>34.4<br>22.6<br>21.1<br>**38.1**<br>32.1<br>18.2<br>9.9<br>9.1|
|Long (30_ −_60_m_)<br>¯_P_<br>¯_R_<br>¯<br>IoU<br>|**47.8**<br>38.9<br>26.3<br>29.9<br>18.2<br>40.6<br>**44.9**<br>12.9<br>11.9<br>17.7<br>**30.5**<br>27.6<br>7.1<br>4.9<br>9.2|
|Ultra-Long (_>_ 60_m_)<br>¯_P_<br>¯_R_<br>¯<br>IoU|**46.1**<br>36.7<br>17.1<br>25.3<br>20.4<br>43.2<br>**46.7**<br>8.3<br>5.8<br>19.6<br>**32.3**<br>27.5<br>2.9<br>2.4<br>9.5|
|Keyword<br>¯_P_<br>¯_R_<br>¯<br>IoU<br>|**60.5**<br>54.4<br>50.3<br>47.9<br>37.4<br>**61.5**<br>57.4<br>33.0<br>33.4<br>26.4<br>**43.8**<br>39.4<br>21.9<br>17.4<br>18.3|
|Phrase<br>¯_P_<br>¯_R_<br>¯<br>IoU<br>|**53.1**<br>45.3<br>41.4<br>41.7<br>25.1<br>**50.2**<br>48.1<br>36.6<br>31.1<br>23.7<br>**36.8**<br>32.4<br>22.3<br>16.0<br>13.2|
|Sentence<br>¯_P_<br>¯_R_<br>¯<br>IoU|**52.9**<br>47.5<br>31.1<br>30.2<br>17.5<br>**53.1**<br>**52.3**<br>34.2<br>23.3<br>22.2<br>**38.5**<br>34.7<br>19.7<br>12.6<br>10.0|
|Audio<br>¯_P_<br>¯_R_<br>¯<br>IoU<br>|**38.1**<br>34.2<br>32.5<br>30.9<br>7.3<br>42.1<br>**43.8**<br>35.8<br>25.5<br>16.5<br>**27.0**<br>24.2<br>20.3<br>10.2<br>3.7|
|Vision<br>¯_P_<br>¯_R_<br>¯<br>IoU<br>|**70.0**<br>53.6<br>48.6<br>48.2<br>41.3<br>**66.9**<br>61.6<br>38.9<br>37.9<br>30.5<br>**49.7**<br>43.9<br>25.4<br>21.8<br>22.0|
|Vision+Audio<br>¯_P_<br>¯_R_<br>¯<br>IoU|**56.2**<br>51.2<br>37.2<br>33.9<br>21.2<br>**50.6**<br>49.0<br>30.9<br>23.4<br>22.0<br>**36.9**<br>33.4<br>18.4<br>12.1<br>11.1|
|Overall<br>¯_P_<br>¯_R_<br>¯<br>IoU|**55.3**<br>49.0<br>40.3<br>39.3<br>25.9<br>**54.8**<br>52.5<br>34.6<br>28.9<br>24.0<br>**39.6**<br>35.4<br>21.2<br>15.2<br>13.6|


Table 3: Performance of different models on the VUE-TR benchmark across various evaluation
attributes. _P_ [¯] and _R_ [¯] represent the AUC (Area Under Curve) values for precision and recall, respectively; while IoU¯ denotes the AUC of intersection-over-union between prediction and ground-truth
timestamp ranges, as defined in Section 6.2. GPT models are accessed via the Azure API, and
Gemini is accessed via internal Google API. _†_ Gemini models are evaluated by directly uploading
videos. To comply with the 100 MB upload limit, long videos are resized to a resolution of 256 pixels. Compared to Gemini-2.0-Flash, Gemini-2.5-Pro (0325) incurs higher latency and token cost for
reasoning and exhibits a higher content filtering rate, often resulting in empty outputs. _‡_ GPT-4o is
constrained by the Azure API’s 120-frame limit. For videos longer than 120 seconds, we uniformly
sample 120 frames.


12


Unlike GPT-4o, Gemini models [1] naturally support text, vision, and audio with extremely long context
length, making them ideal for long video understanding. Gemini can also take raw video files as input. We
evaluate two versions:


  - Gemini-2.5-Pro (0325): Offers strong reasoning and often outputs explicit Chain-of-Thought (CoT)
explanations. However, when not constrained by output formatting instructions, the responses can
be highly inconsistent and difficult to parse. In contrast, adding strict format requirements improves
consistency but leads to degraded performance. Therefore, we choose the simple prompt without
format requirement and parse the major possible formats for evaluation.


  - Gemini-2.0-Flash (stable): Provides a better output structure and lower rejection rates, making it
more reliable for batch evaluations. Although slightly less capable in reasoning than Gemini-2.5-Pro,
it balances performance and robustness well.


The prompt provided to Gemini models is:

```
   Answer with time ranges and do not output explanation. What are all the time ranges
   corresponding to the text query: "QUERY"?

```

However, Gemini-0325 frequently deviates from these instructions, returning time ranges in inconsistent
formats. We therefore implement careful parsing procedures to reliably extract time intervals for evaluation.
In Table 3, we report performance in multiple evaluation dimensions: video duration, query format, and
query modality. Remarkably, Vidi outperforms all baseline models in all categories for the primary metric
IoU.¯ In ultra-short videos, Gemini-2.0-Flash achieves the best precision, but its recall is significantly lower,
leading to a lower IoU.¯ Performance across different query formats is relatively consistent, though models
generally struggle more with longer and more descriptive queries. As expected, GPT-4o performs poorly in
audio-only queries due to lack of audio input support. Other models perform comparably across modalities,
but accuracy in audio-based queries is consistently lower than that on vision-based queries, highlighting the
challenge of audio-conditioned understanding.
As shown in Figure 10, we can still observe that Vidi consistently outperforms all competitors by a significant margin across the entire range of thresholds. This performance gap even widens at higher thresholds
( _e.g._, _≥_ 0 _._ 5), where other models degrade much more rapidly. It shows Vidi’s strength in fine-grained temporal precision, a critical capability for real-world video editing and retrieval tasks. By using more powerful
backbones and dynamic token compression, Vidi-1.5 gains considerable improvement over all the metrics.



1.0

0.9

0.8

0.7

0.6

0.5

0.4

0.3

0.2

0.1



1.0

0.9

0.8

0.7

0.6

0.5

0.4

0.3

0.2

0.1



1.0

0.9

0.8

0.7

0.6

0.5

0.4

0.3

0.2

0.1









0.0

|Col1|Col2|Col3|Col4|V|idi-1|.5 [5|5.32|%]|Col10|
|---|---|---|---|---|---|---|---|---|---|
|||||<br>V<br>|<br>idi [<br>|<br> 48.9<br>|<br> 6%]<br>|<br>||
|||||||||||
|||||~~G~~<br>|~~emi~~<br>|~~ni-2.~~<br>|~~0-Fla~~<br>|~~sh [4~~<br>|~~ 0.34%]~~<br>|
|||||||||||
|||||<br>|~~emi~~<br>~~PT-~~|~~i-2.~~<br>~~o [2~~|~~-Pr~~<br>~~ .94~~|~~ [39~~<br>~~ ]~~|~~ 31%]~~|
|||||||||||
|||||||||||
|||||||||||
|||||||||||


0.0 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1.0
Precision Threshold



0.0

|Col1|Col2|Col3|Col4|V|Col6|idi-1|.5 [5|4.78|%]|Col11|Col12|
|---|---|---|---|---|---|---|---|---|---|---|---|
|||||<br>V<br>|<br>V<br>|<br>idi [<br>|<br> 52.5<br>|<br> 1%]<br>|<br>|||
|||||||||||||
|||||<br>|<br>|~~emi~~<br>|~~ni-2.~~<br>|~~0-Fla~~<br>|~~sh [3~~<br>|~~ 4.58~~<br>|~~ %]~~<br>|
|||||||||||||
|||||<br>|<br>|~~emi~~<br>~~PT-~~|~~i-2.~~<br>~~o [2~~|~~-Pr~~<br>~~ .00~~|~~ [28~~<br>~~ ]~~|~~ 91%~~|~~ ]~~|
|||||||||||||
|||||||||||||
|||||||||||||
|||||||||||||


0.0 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1.0
Recall Threshold



0.0

|Col1|V|idi-|1.5 [3|9.63|%]|Col7|Col8|
|---|---|---|---|---|---|---|---|
||<br>V<br>|<br>idi [<br>|<br> 35.4<br>|<br> 3%]<br>|<br>|||
||<br>|~~em~~<br>|~~ni-2.~~<br>|~~0-Fla~~<br>|~~sh [~~<br>|~~ 1.23~~<br>|~~ %]~~<br>|
||<br>|~~em~~<br>~~PT-~~|~~ni-2~~<br>~~o [1~~|~~5-Pr~~<br>~~ 3.62~~|~~ [15~~<br>~~ ]~~|~~ 19%~~|~~ ]~~|
|||||||||
|||||||||
|||||||||
|||||||||


0.0 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1.0
IoU Threshold



Figure 10: Overall performance curves for temporal retrieval on the VUE-TR benchmark. We
report accuracy across varying thresholds for different models.

### **8 Related Work**


**Benchmarks.** Recent advancements in video question answering (VideoQA) have been sharped by benchmarks such as CinePile [23], Video-MME [5], MovieChat-1K [26], LVBench [31], and LongVideoBench [33].
To evaluate models on long-form videos, many of these benchmarks demonstrate strong performance with


13


only sparse frame sampling. They may not fully reflect a model’s video understanding capabilities. For example, LLaVA-OneVision [15] only employs as few as 32 uniformly sampled frames to achieve 66 _._ 3% accuracy
on Video-MME [5].
In contrast, temporal retrieval requires fine-grained understanding across the full temporal span of a video
instead of a few scattered glimpses. As such, temporal retrieval serves as a more rigorous benchmark for
evaluating a model’s true capability in video understanding. Charades-STA [6] and DiDeMo [9] focus mainly
on action grounding within short clips ( _∼_ 30 _s_ ). QVHighlights [14] and ActivityNet Captions [12] extend to
several minutes videos, covering event descriptions and subjectively defined highlights. Recently, LongVALE

[7] introduces multimodal audio-visual queries, but remains constrained to relatively short durations.
To address above limitations, our benchmark is designed to evaluate model performance in realistic,
large-scale video environments. In particular, we extend the video length to over one hour, and introduce a
video duration categorization into ultra-short, short, medium, long, and ultra-long segments. Furthermore,
we diversify the retrieval challenge by varying query format (keyword, phrase, sentence) and modality (visiononly, audio-only, vision+audio), enabling a more comprehensive understanding of model capabilities.


**Video** **LMMs.** Video understanding has made significant progress with the emergence of LMMs that
integrate visual and textual information. Models such as the InternLM-XComposer [36, 4, 37], QwenVL [2, 29, 3], and LLaVA [19, 33] series have introduced innovative architectures and training strategies.
InternLM-XComposer adopts a modular architecture that integrates interleaved text-image composition and
comprehension with rich multilingual knowledge. Qwen-VL and its successors introduce flexible multi-image
and box-conditioned input capabilities, supporting multilingual and multi-turn interaction for diverse visionlanguage tasks. The LLaVA series bridges visual perception with LLMs through a unified representation
space, and its recent extensions, such as LLaVA-NeXT, further support video and 3D input via interleaved
multimodal pretraining [17]. Although these models demonstrate impressive general-purpose reasoning, they
typically operate on a limited number of frames ( _e.g._, _≤_ 64), which restricts their effectiveness in long-form
temporal retrieval.


**Temporal** **Retrieval.** Early methods [14, 6, 9, 12] usually employ proposal-based strategies, where models
first generate candidate segments and then rank them based on their semantic relevance to the query. With
the emergence of video LMMs, recent research has shifted toward enhancing video-text alignment through
unified frameworks. For example, TimeChat [24] connects a time-aware frame encoder and a sliding video QFormer [18] to deal with temporal retrieval based on an instruction-tuning dataset. TimeSearch [21] proposes
a temporal spotlight grounding strategy to find key events and a temporal reflection mechanism to verify
time range predictions and guide the search direction. Ye _et_ _al._ [34] revisit the temporal search in long-form
videos by proposing a lightweight framework that reformulates temporal retrieval as a spatial search problem.
Although efficient, the above methods rely on sampling only 8 _∼_ 96 frames, which may be insufficient to
capture fine-grained temporal cues.
Despite these advancements, most existing methods still focus on short videos or rely on sparse frame
sampling, and primarily limited to vision-only inputs. These constraints hinder the evaluation of models’
full multimodal reasoning abilities, particularly in understanding and retrieving moments from long, complex
videos involving both visual and auditory modalities. In this work, we propose Vidi, a new approach that
jointly incorporates text, vision, and audio input from hour-long videos to retrieve the most relevant temporal
segments based on free-form natural language queries. Our setting pushes beyond existing benchmarks by
requiring fine-grained temporal understanding across extended multimodal content.

### **9 Conclusion**


We introduce Vidi, a large multi-modal model for real-world video understanding and editing (VUE). The
first release focuses on temporal retrieval (TR), which is a foundational step in video trimming and editing,
by localizing relevant segments from long videos given natural language queries. To support robust evaluation under realistic conditions, we propose VUE-TR, a new benchmark for practical video editing use cases.
VUE-TR introduces key improvements over prior datasets in terms of video duration, audio support, query
format, annotation quality, and metric design for multispan timestamp evaluation. Vidi leverages a unified
vision-audio-language architecture with modality-aware sampling and precise token alignment. In addition,


14


the Decomposed Attention mechanism allows the model to capture fine-grained temporal cues across diverse
modalities and scales seamlessly to long videos. As demonstrated in the VUE-TR benchmark, Vidi consistently outperforms leading proprietary models such as GPT-4o and Gemini. For future work, we plan to
extend Vidi to support a wider spectrum of video understanding tasks, including temporal VQA, spatiotemporal grounding, and high-level video understanding. Additionally, we aim to explore interactive editing
capabilities to further bridge the gap between large models and real-world VUE applications.


15


### **10 Contributors**

**Core** **Contributors** **-** **Research** **(alphabetical** **order)**
Chia-Wen Kuo, Dawei Du, Fan Chen, Guang Chen, Sijie Zhu, Xin Gu.


**Core** **Contributors** **-** **Infrastructure** **(alphabetical** **order)**
Celong Liu, Tong Jin.


**Research** **Leads**
Longyin Wen, Xiaohui Shen.


**Contributors** **(alphabetical** **order)**
Jiamin Yuan, Lingxi Zhang, Lu Guo, Lusha Li, Qingyu Chen, Rachel Deng, Stuart Siew, Wei Lu, Wen Zhong,
Xing Mei, Xueqiong Qu, Zhenfang Chen.

### **References**


[1] Rohan Anil, Sebastian Borgeaud, Yonghui Wu, Jean-Baptiste Alayrac, Jiahui Yu, Radu Soricut, Johan
Schalkwyk, Andrew M. Dai, Anja Hauth, Katie Millican, David Silver, Slav Petrov, Melvin Johnson, Ioannis Antonoglou, Julian Schrittwieser, Amelia Glaese, Jilin Chen, Emily Pitler, Timothy P.
Lillicrap, Angeliki Lazaridou, Orhan Firat, James Molloy, Michael Isard, Paul Ronald Barham, Tom
Hennigan, Benjamin Lee, Fabio Viola, Malcolm Reynolds, Yuanzhong Xu, Ryan Doherty, Eli Collins,
Clemens Meyer, Eliza Rutherford, Erica Moreira, Kareem Ayoub, Megha Goel, George Tucker, Enrique Piqueras, Maxim Krikun, Iain Barr, Nikolay Savinov, Ivo Danihelka, Becca Roelofs, Ana¨ıs White,
Anders Andreassen, Tamara von Glehn, Lakshman Yagati, Mehran Kazemi, Lucas Gonzalez, Misha
Khalman, Jakub Sygnowski, and et al. Gemini: A family of highly capable multimodal models. _CoRR_,
abs/2312.11805, 2023.


[2] Jinze Bai, Shuai Bai, Shusheng Yang, Shijie Wang, Sinan Tan, Peng Wang, Junyang Lin, Chang Zhou,
and Jingren Zhou. Qwen-vl: A frontier large vision-language model with versatile abilities. _CoRR_,
abs/2308.12966, 2023.


[3] Shuai Bai, Keqin Chen, Xuejing Liu, Jialin Wang, Wenbin Ge, Sibo Song, Kai Dang, Peng Wang, Shijie
Wang, Jun Tang, Humen Zhong, Yuanzhi Zhu, Ming-Hsuan Yang, Zhaohai Li, Jianqiang Wan, Pengfei
Wang, Wei Ding, Zheren Fu, Yiheng Xu, Jiabo Ye, Xi Zhang, Tianbao Xie, Zesen Cheng, Hang Zhang,
Zhibo Yang, Haiyang Xu, and Junyang Lin. Qwen2.5-vl technical report. _CoRR_, abs/2502.13923, 2025.


[4] Xiaoyi Dong, Pan Zhang, Yuhang Zang, Yuhang Cao, Bin Wang, Linke Ouyang, Xilin Wei, Songyang
Zhang, Haodong Duan, Maosong Cao, Wenwei Zhang, Yining Li, Hang Yan, Yang Gao, Xinyue
Zhang, Wei Li, Jingwen Li, Kai Chen, Conghui He, Xingcheng Zhang, Yu Qiao, Dahua Lin, and Jiaqi Wang. Internlm-xcomposer2: Mastering free-form text-image composition and comprehension in
vision-language large model. _CoRR_, abs/2401.16420, 2024.


[5] Chaoyou Fu, Yuhan Dai, Yondong Luo, Lei Li, Shuhuai Ren, Renrui Zhang, Zihan Wang, Chenyu Zhou,
Yunhang Shen, Mengdan Zhang, Peixian Chen, Yanwei Li, Shaohui Lin, Sirui Zhao, Ke Li, Tong Xu,
Xiawu Zheng, Enhong Chen, Rongrong Ji, and Xing Sun. Video-mme: The first-ever comprehensive
evaluation benchmark of multi-modal llms in video analysis. _CoRR_, abs/2405.21075, 2024.


[6] Jiyang Gao, Chen Sun, Zhenheng Yang, and Ram Nevatia. TALL: temporal activity localization via
language query. In _IEEE_ _International_ _Conference_ _on_ _Computer_ _Vision,_ _ICCV_ _2017,_ _Venice,_ _Italy,_
_October_ _22-29,_ _2017_, pages 5277–5285. IEEE Computer Society, 2017.


[7] Tiantian Geng, Jinrui Zhang, Qingni Wang, Teng Wang, Jinming Duan, and Feng Zheng. Longvale: Vision-audio-language-event benchmark towards time-aware omni-modal perception of long videos.
_CoRR_, abs/2411.19772, 2024.


16


[8] Oliver Guhr, Anne-Kathrin Schumann, Frank Bahrmann, and Hans-Joachim B¨ohme. Fullstop: Multilingual deep models for punctuation prediction. In _Proceedings_ _of_ _the_ _Swiss_ _Text_ _Analytics_ _Conference_
_2021,_ _Winterthur,_ _Switzerland,_ _June_ _14-16,_ _2021_ _(held_ _online_ _due_ _to_ _COVID19_ _pandemic)_, volume 2957
of _CEUR_ _Workshop_ _Proceedings_ . CEUR-WS.org, 2021.


[9] Lisa Anne Hendricks, Oliver Wang, Eli Shechtman, Josef Sivic, Trevor Darrell, and Bryan C. Russell.
Localizing moments in video with natural language. In _IEEE_ _International_ _Conference_ _on_ _Computer_
_Vision, ICCV 2017, Venice,_ _Italy,_ _October 22-29, 2017_, pages 5804–5813. IEEE Computer Society, 2017.


[10] Aaron Hurst, Adam Lerer, Adam P. Goucher, Adam Perelman, Aditya Ramesh, Aidan Clark, AJ Ostrow,
Akila Welihinda, Alan Hayes, Alec Radford, Aleksander Madry, Alex Baker-Whitcomb, and et al. Gpt-4o
system card. _CoRR_, abs/2410.21276, 2024.


[11] Albert Q. Jiang, Alexandre Sablayrolles, Arthur Mensch, Chris Bamford, Devendra Singh Chaplot,
Diego de Las Casas, Florian Bressand, Gianna Lengyel, Guillaume Lample, Lucile Saulnier, L´elio Renard
Lavaud, Marie-Anne Lachaux, Pierre Stock, Teven Le Scao, Thibaut Lavril, Thomas Wang, Timoth´ee
Lacroix, and William El Sayed. Mistral 7b. _CoRR_, abs/2310.06825, 2023.


[12] Ranjay Krishna, Kenji Hata, Frederic Ren, Li Fei-Fei, and Juan Carlos Niebles. Dense-captioning events
in videos. In _IEEE_ _International_ _Conference_ _on_ _Computer_ _Vision,_ _ICCV_ _2017,_ _Venice,_ _Italy,_ _October_
_22-29,_ _2017_, pages 706–715. IEEE Computer Society, 2017.


[13] Chia-Wen Kuo, Sijie Zhu, Fan Chen, Xiaohui Shen, and Longyin Wen. Rethinking homogeneity of vision
and text tokens in large vision-and-language models. _CoRR_, abs/2502.01906, 2025.


[14] Jie Lei, Tamara L. Berg, and Mohit Bansal. Detecting moments and highlights in videos via natural
language queries. In _Advances_ _in_ _Neural_ _Information_ _Processing_ _Systems_ _34:_ _Annual_ _Conference_ _on_
_Neural Information Processing Systems 2021, NeurIPS 2021, December 6-14, 2021, virtual_, pages 11846–
11858, 2021.


[15] Bo Li, Yuanhan Zhang, Dong Guo, Renrui Zhang, Feng Li, Hao Zhang, Kaichen Zhang, Yanwei Li,
Ziwei Liu, and Chunyuan Li. Llava-onevision: Easy visual task transfer. _CoRR_, abs/2408.03326, 2024.


[16] Congcong Li, Xinyao Wang, Dexiang Hong, Yufei Wang, Libo Zhang, Tiejian Luo, and Longyin Wen.
Structured context transformer for generic event boundary detection. _CoRR_, abs/2206.02985, 2022.


[17] Feng Li, Renrui Zhang, Hao Zhang, Yuanhan Zhang, Bo Li, Wei Li, Zejun Ma, and Chunyuan Li. Llavanext-interleave: Tackling multi-image, video, and 3d in large multimodal models. _CoRR_, abs/2407.07895,
2024.


[18] Junnan Li, Dongxu Li, Silvio Savarese, and Steven C. H. Hoi. BLIP-2: bootstrapping language-image
pre-training with frozen image encoders and large language models. In _International_ _Conference_ _on_
_Machine_ _Learning,_ _ICML_ _2023,_ _23-29_ _July_ _2023,_ _Honolulu,_ _Hawaii,_ _USA_, volume 202 of _Proceedings_ _of_
_Machine_ _Learning_ _Research_, pages 19730–19742. PMLR, 2023.


[19] Haotian Liu, Chunyuan Li, Qingyang Wu, and Yong Jae Lee. Visual instruction tuning. In _Advances_
_in_ _Neural_ _Information_ _Processing_ _Systems_ _36:_ _Annual_ _Conference_ _on_ _Neural_ _Information_ _Processing_
_Systems_ _2023,_ _NeurIPS_ _2023,_ _New_ _Orleans,_ _LA,_ _USA,_ _December_ _10_ _-_ _16,_ _2023_, 2023.


[20] Ilya Loshchilov and Frank Hutter. Decoupled weight decay regularization. In _7th_ _International_ _Confer-_
_ence on Learning Representations, ICLR 2019, New Orleans, LA, USA, May 6-9, 2019_ . OpenReview.net,
2019.


[21] Junwen Pan, Rui Zhang, Xin Wan, Yuan Zhang, Ming Lu, and Qi She. Timesearch: Hierarchical video
search with spotlight and reflection for human-like long video understanding. _CoRR_, abs/2504.01407,
2025.


17


[22] Alec Radford, Jong Wook Kim, Tao Xu, Greg Brockman, Christine McLeavey, and Ilya Sutskever.
Robust speech recognition via large-scale weak supervision. In _International_ _Conference_ _on_ _Machine_
_Learning,_ _ICML_ _2023,_ _23-29_ _July_ _2023,_ _Honolulu,_ _Hawaii,_ _USA_, volume 202 of _Proceedings_ _of_ _Machine_
_Learning_ _Research_, pages 28492–28518. PMLR, 2023.


[23] Ruchit Rawal, Khalid Saifullah, Ronen Basri, David Jacobs, Gowthami Somepalli, and Tom Goldstein.
Cinepile: A long video question answering dataset and benchmark. _CoRR_, abs/2405.08813, 2024.


[24] Shuhuai Ren, Linli Yao, Shicheng Li, Xu Sun, and Lu Hou. Timechat: A time-sensitive multimodal
large language model for long video understanding. In _IEEE/CVF_ _Conference_ _on_ _Computer_ _Vision_
_and_ _Pattern_ _Recognition,_ _CVPR_ _2024,_ _Seattle,_ _WA,_ _USA,_ _June_ _16-22,_ _2024_, pages 14313–14323. IEEE,
2024.


[25] Morgane Rivi`ere, Shreya Pathak, Pier Giuseppe Sessa, Cassidy Hardin, Surya Bhupatiraju, L´eonard
Hussenot, Thomas Mesnard, Bobak Shahriari, Alexandre Ram´e, and et al. Gemma 2: Improving open
language models at a practical size. _CoRR_, abs/2408.00118, 2024.


[26] Enxin Song, Wenhao Chai, Guanhong Wang, Yucheng Zhang, Haoyang Zhou, Feiyang Wu, Haozhe Chi,
Xun Guo, Tian Ye, Yanting Zhang, Yan Lu, Jenq-Neng Hwang, and Gaoang Wang. Moviechat: From
dense token to sparse memory for long video understanding. In _IEEE/CVF_ _Conference_ _on_ _Computer_
_Vision_ _and_ _Pattern_ _Recognition,_ _CVPR_ _2024,_ _Seattle,_ _WA,_ _USA,_ _June_ _16-22,_ _2024_, pages 18221–18232.
IEEE, 2024.


[27] Michael Tschannen, Alexey A. Gritsenko, Xiao Wang, Muhammad Ferjad Naeem, Ibrahim Alabdulmohsin, Nikhil Parthasarathy, Talfan Evans, Lucas Beyer, Ye Xia, Basil Mustafa, Olivier J. H´enaff,
Jeremiah Harmsen, Andreas Steiner, and Xiaohua Zhai. Siglip 2: Multilingual vision-language encoders
with improved semantic understanding, localization, and dense features. _CoRR_, abs/2502.14786, 2025.


[28] Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N. Gomez, Lukasz
Kaiser, and Illia Polosukhin. Attention is all you need. In _Advances_ _in_ _Neural_ _Information_ _Processing_
_Systems_ _30:_ _Annual_ _Conference_ _on_ _Neural_ _Information_ _Processing_ _Systems_ _2017,_ _December_ _4-9,_ _2017,_
_Long_ _Beach,_ _CA,_ _USA_, pages 5998–6008, 2017.


[29] Peng Wang, Shuai Bai, Sinan Tan, Shijie Wang, Zhihao Fan, Jinze Bai, Keqin Chen, Xuejing Liu, Jialin
Wang, Wenbin Ge, Yang Fan, Kai Dang, Mengfei Du, Xuancheng Ren, Rui Men, Dayiheng Liu, Chang
Zhou, Jingren Zhou, and Junyang Lin. Qwen2-vl: Enhancing vision-language model’s perception of the
world at any resolution. _CoRR_, abs/2409.12191, 2024.


[30] Qiuheng Wang, Yukai Shi, Jiarong Ou, Rui Chen, Ke Lin, Jiahao Wang, Boyuan Jiang, Haotian Yang,
Mingwu Zheng, Xin Tao, Fei Yang, Pengfei Wan, and Di Zhang. Koala-36m: A large-scale video dataset
improving consistency between fine-grained conditions and video content. _CoRR_, abs/2410.08260, 2024.


[31] Weihan Wang, Zehai He, Wenyi Hong, Yean Cheng, Xiaohan Zhang, Ji Qi, Shiyu Huang, Bin Xu, Yuxiao
Dong, Ming Ding, and Jie Tang. Lvbench: An extreme long video understanding benchmark. _CoRR_,
abs/2406.08035, 2024.


[32] Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten Bosma, Brian Ichter, Fei Xia, Ed H. Chi, Quoc V.
Le, and Denny Zhou. Chain-of-thought prompting elicits reasoning in large language models. In _Advances_
_in_ _Neural_ _Information_ _Processing_ _Systems_ _35:_ _Annual_ _Conference_ _on_ _Neural_ _Information_ _Processing_
_Systems_ _2022,_ _NeurIPS_ _2022,_ _New_ _Orleans,_ _LA,_ _USA,_ _November_ _28_ _-_ _December_ _9,_ _2022_, 2022.


[33] Haoning Wu, Dongxu Li, Bei Chen, and Junnan Li. Longvideobench: A benchmark for long-context
interleaved video-language understanding. In _Advances_ _in_ _Neural_ _Information_ _Processing_ _Systems_ _38:_
_Annual_ _Conference_ _on_ _Neural_ _Information_ _Processing_ _Systems_ _2024,_ _NeurIPS_ _2024,_ _Vancouver,_ _BC,_
_Canada,_ _December_ _10_ _-_ _15,_ _2024_, 2024.


[34] Jinhui Ye, Zihan Wang, Haosen Sun, Keshigeyan Chandrasegaran, Zane Durante, Cristobal Eyzaguirre,
Yonatan Bisk, Juan Carlos Niebles, Ehsan Adeli, Li Fei-Fei, Jiajun Wu, and Manling Li. Re-thinking
temporal search for long-form video understanding. _CoRR_, abs/2504.02259, 2025.


18


[35] Xiaohua Zhai, Basil Mustafa, Alexander Kolesnikov, and Lucas Beyer. Sigmoid loss for language image
pre-training. In _IEEE/CVF_ _International_ _Conference_ _on_ _Computer_ _Vision,_ _ICCV_ _2023,_ _Paris,_ _France,_
_October_ _1-6,_ _2023_, pages 11941–11952. IEEE, 2023.


[36] Pan Zhang, Xiaoyi Dong, Bin Wang, Yuhang Cao, Chao Xu, Linke Ouyang, Zhiyuan Zhao, Shuangrui Ding, Songyang Zhang, Haodong Duan, Wenwei Zhang, Hang Yan, Xinyue Zhang, Wei Li, Jingwen Li, Kai Chen, Conghui He, Xingcheng Zhang, Yu Qiao, Dahua Lin, and Jiaqi Wang. Internlmxcomposer: A vision-language large model for advanced text-image comprehension and composition.
_CoRR_, abs/2309.15112, 2023.


[37] Pan Zhang, Xiaoyi Dong, Yuhang Zang, Yuhang Cao, Rui Qian, Lin Chen, Qipeng Guo, Haodong Duan,
Bin Wang, Linke Ouyang, Songyang Zhang, Wenwei Zhang, Yining Li, Yang Gao, Peng Sun, Xinyue
Zhang, Wei Li, Jingwen Li, Wenhai Wang, Hang Yan, Conghui He, Xingcheng Zhang, Kai Chen, Jifeng
Dai, Yu Qiao, Dahua Lin, and Jiaqi Wang. Internlm-xcomposer-2.5: A versatile large vision language
model supporting long-contextual input and output. _CoRR_, abs/2407.03320, 2024.


19


