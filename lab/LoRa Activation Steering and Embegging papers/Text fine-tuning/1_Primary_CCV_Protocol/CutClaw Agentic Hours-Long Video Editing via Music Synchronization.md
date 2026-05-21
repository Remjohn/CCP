## **CutClaw: Agentic Hours-Long Video Editing via** **Music Synchronization**

Shifang Zhao [1] _[,]_ [2], Yihan Hu [2], Ying Shan [3], Yunchao Wei [1] _[†]_, and Xiaodong Cun [2] _[†]_





1 Beijing Jiaotong University
2 GVC Lab, Great Bay University
3 ARC Lab, Tencent

```
https://github.com/GVCLab/CutClaw

```
















**Fig. 1:** We present an automated music-driven video editing system that transforms
hours-long footage into high-quality short videos based on user instructions and given
music rhythm, so that the resulting video demonstrates precise music synchronization,
faithful instruction following, and visually appealing aesthetics.


**Abstract.** Editing the video content with audio alignment forms a digital human-made art in current social media. However, the time-consuming
and repetitive nature of manual video editing has long been a challenge
for filmmakers and professional content creators alike. In this paper, we
introduce CutClaw, an autonomous multi-agent framework designed to
edit hours-long raw footage into meaningful short videos that leverages
the capabilities of multiple Multimodal Language Models (MLLMs) as
an agent system. It produces videos with synchronized music, followed by
instructions, and a visually appealing appearance. In detail, our approach
begins by employing a hierarchical multimodal decomposition that captures both fine-grained details and global structures across visual and


_†_ Corresponding authors.


2 Zhao et al.


audio footage. Then, to ensure narrative consistency, a Playwriter Agent
orchestrates the whole storytelling flow and structures the long-term narrative, anchoring visual scenes to musical shifts. Finally, to construct a
short edited video, Editor and Reviewer Agents collaboratively optimize
the final cut via selecting fine-grained visual content based on rigorous aesthetic and semantic criteria. We conduct detailed experiments
to demonstrate that CutClaw significantly outperforms state-of-the-art
baselines in generating high-quality, rhythm-aligned videos. The code is
available at: `[https://github.com/GVCLab/CutClaw](https://github.com/GVCLab/CutClaw)` .


**1** **Introduction**


Videos are inherently multimodal, weaving together visual and auditory streams.
Consequently, Audio-driven video editing [4] represents the most transformative
stage of storytelling, fusing sight and sound into organic harmony. Moving beyond simple temporal concatenation, cinematic editing is inherently a complex
multimodal alignment problem. In practice, distilling hours of untrimmed video
into a concise output requires traversing a massive search space to retrieve sparse,
salient segments that simultaneously advance the global storyline and strictly
adhere to local auditory dynamics. Balancing the dual constraints of maintaining global narrative coherence and ensuring fine-grained visual-audio harmony
renders professional editing a highly labor-intensive process that is heavily dependent on human aesthetic intuition.
Despite recent progress, existing automated video editing frameworks typically neglect the critical role of audio, falling into three suboptimal paradigms.
_e.g_ ., Template-based methods [1,3,5] force clips into rigid, predefined temporal
slots and overlay background music; lacking audio-visual synchronization and semantic awareness, they yield repetitive outputs devoid of narrative progression.
Highlight detection methods [26] optimize for local visual salience but are audioagnostic, treating clips in isolation and failing to construct a globally coherent
narrative. Text-based approaches [12] prioritize linguistic semantics by aligning
visuals with transcripts, yet neglect the underlying musical structure, disrupting
both kinetic rhythm and affective energy. Consequently, these methods optimize audio, video, and text instruction independently, struggling to achieve the
holistic multimodal alignment required to satisfy the dual constraint of global
storytelling and fine-grained visual-audio harmony.
To build a system capable of practical audio-visual storytelling entails three
fundamental technical challenges. _(i)_ _Context_ _Length_ _Limitation._ The dense visual information required for fine-grained understanding across hours-long raw
footage physically surpasses the context window length of current MLLMs (Multimodal Language Models) [9,17]. _(ii)_ _Context-Grounded_ _Storytelling._ Crafting a
cohesive visual story requires reconciling external user instructions with the intrinsic semantics of the raw video and audio. It is highly challenging to synthesize


4 In this work, “editing” and “cutting” are used interchangeably to denote the temporal
selection and assembly of raw video segments.


CutClaw: Agentic Hours-Long Video Editing via Music Synchronization 3


a narrative logic that strictly executes creative intent without decoupling from
the native context and subjects of the source materials. _(iii) Fine-Grained Cross-_
_Modal Alignment._ Achieving organic visual-audio harmony demands fine-grained
temporal grounding to synchronize musical shifts with a holistic understanding
of visual plot, aesthetics, and emotion.
To address these challenges, we introduce _CutClaw_, an autonomous MLLMpowered multi-agent framework that mimics a professional post-production workflow through a collaborative, coarse-to-fine hierarchy. To overcome the context
length limitation, a _Bottom-Up_ _Multimodal_ _Footage_ _Deconstruction_ module abstracts both raw video and audio into structured semantic units of visual scenes
and musical sections, enabling both narrative comprehension and fine-grained
analysis. To achieve context-grounded storytelling, a _Playwriter_ agent acts as a
global planner. Using the musical structure as an invariant temporal anchor, it
aligns user instructions with the abstracted scenes to synthesize a narrative that
executes creative intent while respecting the source material’s intrinsic plot. Finally, to achieve fine-grained cross-modal alignment, _Editor_ agent and _Reviewer_
agent collaboratively perform top-down hierarchical visual grounding. Guided by
the summarized script, the _Editor_ localizes precise segments, and the _Reviewer_
enforces a multi-criteria validity gate to rigorously evaluate plot relevance, visual
aesthetics, and instruction following, thereby guaranteeing organic audio-visual
harmony.
Our key contributions are summarized as:


**–** We tackle the novel task of audio-driven video editing, formally modeling
it as a joint optimization problem that simultaneously satisfies instructiondriven storytelling and fine-grained rhythmic harmony.

**–** We introduce **CutClaw**, an MLLM-powered multi-agent framework that
tackles the computationally intractable search space of hours-long footage. It
integrates _bottom-up_ _multimodal_ _deconstruction_ with a collaborative agentic
workflow, where a _Playwriter_ orchestrates music-anchored narrative planning, while _Editor_ and _Reviewer_ agents collaboratively execute precise segment selection.

**–** Extensive experiments and user studies demonstrate that CutClaw significantly outperforms state-of-the-art baselines in visual quality, instruction
following, and rhythmic harmony.


**2** **Related** **Work**


**AI-assisted** **Video** **Editing.** Video editing has evolved from optimizationbased heuristics to data-driven frameworks. Early pioneering works, such as
Write-A-Video [24] and ESA [7], formulated editing as an energy minimization
problem to align shots with themed cues. Recent generative methods [8,18] have
shifted towards constructing visual sequences driven by high-level instructions
or subtitle narratives [12]. However, these methods are fundamentally limited to
assembling pre-segmented clips, rely on explicit scripts for narrative structure,
and critically neglect the rhythmic guidance of the music modality. In contrast,


4 Zhao et al.


CutClaw directly processes raw, untrimmed footage without manual scripts, formulating editing as a hierarchical narrative construction that simultaneously
guarantees semantic storytelling and fine-grained audio-visual harmony.

**Video** **Temporal** **Grounding** **and** **Highlight** **Detection.** Video Temporal
Grounding(VTG) and Highlight Detection serve as fundamental prerequisites
for editing by determining where to cut within raw footage. VTG aims to
localize specific segments based on natural language queries; conventional approaches [10,15] rely on pretrained feature encoders, while recent methods [25]
leverage MLLMs to enhance instruction understanding. Similarly, Highlight Detection has evolved from using visual saliency scores [23,27,29] to incorporating
textual prompts [22, 26] for better alignment with user preferences. However,
both streams of research face significant limitations in professional editing contexts: they struggle to effectively model the long-term context of raw footage
and lack precise control over the duration of retrieved results. Consequently,
these methods are ill-suited for high-precision audio-visual synchronization tasks,
where visual cuts must rigorously align with musical beats and rhythmic patterns. To bridge this gap, we take a step to deal with hours-long video footage
with both textual and musical input.

**Agents** **for** **Video** **Generation** **and** **Editing.** The advent of MLLMs has
catalyzed the use of multi-agent collaborations in the video domain [13, 32].
Recent frameworks employ agents for various settings, ranging from generative
role-playing in ViMax [11] to non-linear editing in EditDuet [21] and targeted
video trimming [30]. However, these systems face critical bottlenecks in scalability and precision. They are constrained by context windows when processing
hours-long footage and fail to achieve audio-visual synchronization due to coarse
LLM planning. CutClaw overcomes these limitations by pairing a Hierarchical
Decomposition strategy for long-context processing with Audio-Anchor Alignment for precise multi-modal synchronization.


**3** **Method**


**3.1** **Problem** **Formulation**


Given raw video footage, a target music track, and a text instruction as multimodal inputs, we formulate video editing as an agent-driven segment extraction
and assembly problem. By leveraging multiple specialized models and agents,
our framework extracts and synchronizes relevant clips to ensure the final output strictly follows the narrative instruction while achieving organic audio-visual
harmony.
Formally, given raw video footage _V_, the background music track _M_, and the
user instructions _I_, the target edited video is recomposed by a trimed timeline
_E_ = ( _c_ 1 _, . . ., cN_ ), which consists of a sequence of clips and each clip _ci_ = ( _t_ [in] _i_ _[, t]_ _i_ [out] )
represents a continuous segment extracted from the original video footage _V_ . We


CutClaw: Agentic Hours-Long Video Editing via Music Synchronization 5


**Fig. 2:** _**The**_ _**whole**_ _**workflow**_ _**of**_ _**the**_ _**CutClaw.**_ The multi-modal footage is first **De-**
**constructed**, and then, the shot plan is generated by the **Playwriter**, scene retrieval
and editing by the **Editor**, and quality validation by the **Reviewer** .


optimize a timeline _E_ _[∗]_ to maximize a joint objective function:



\ lab el
_{_



e
_q:j_ oint ___ - b _j}_ \begi _n_ {


m
_spl_ it} \ _ma t_ h c _al_ {E}^* _=_ \ _a_



(1)



where _Q_ vis ( _Visual_ _Quality_ ) ensures aesthetic appeal and protagonist prominence; _Q_ narr ( _Narrative_ _Flow_ ) enforces coherent storytelling between adjacent
clips; _Q_ cond ( _Semantic Alignment_ ) measures the fidelity of selected content to the
instructions _I_ ; and _Q_ sync ( _Rhythmic_ _Alignment_ ) encourages visual cuts to synchronize with musical beats in _M_ . Instead of brute-force searching, we approximate the solution via a _hierarchical_ _search_ _space_ _analysis_ _and_ _pruning_ _strategy_ .
As shown in Fig. 2, we first discretize the high-dimensional footage into structured semantic (Sec. 3.2), effectively reducing the solution space. Subsequently,
the _Playwriter_ (Sec. 3.3) leverages audio-visual correlations to constrain the
search scope to localized candidate pools, enabling the _Editor_ (Sec. 3.4) and _Re-_
_viewer_ (Sec. 3.5) to perform efficient fine-grained retrieval and rigorous rejection
sampling to finalize the timeline _E_ _[∗]_ .


**3.2** **Bottom-Up** **Multimodal** **Footage** **Deconstruction**


The raw footage _V_ and background music _M_ are continuous, high-dimensional
streams, making direct timeline optimization computationally intractable. To
address this, we perform a bottom-up deconstruction to discretize these inputs
into structured semantic units, establishing a finite, searchable candidate space
for the subsequent hierarchical planning.


|Zhao et al.|Col2|Col3|Col4|Col5|Col6|Col7|
|---|---|---|---|---|---|---|
||||||||
|||Raw V|ideo Footage|ideo Footage|||







Showcase the
Joker's signature
traits    ....



Section-Level Structure














































































|(1) Shot Stru<br>Shot 0|Col2|Col3|Col4|Col5|cture Parsing<br>Shot 5|Col7|Col8|Col9|
|---|---|---|---|---|---|---|---|---|
|Shot  1<br>Subtitles<br>`01:40:27,830 -> 01:40:32,010`<br>**`[Jim Gordon]`** `The doctor says`<br>`you're in agonizing pain, but`<br>`you won't accept medication. `<br>`01:40:27,830 --> 01:40:32,010`<br>**`[Jim Gordon]`** `That you're`<br>`refusing to accept skin`<br>`grafts.`<br>`01:40:38,150 --> 01:40:42,430`<br>**`[Harvey Dent]`** `Remember that`<br>`name you all had for me when I`<br>`was at Internal Affairs?`<br> <br>...<br>Shot 4<br>Environment:<br>`Location: Hospital Bed`<br>`Time: Daylight`<br>Character:<br>`ID 1: Person in Foreground`<br>Cinematography:<br>`Shot: Close-up, Static`<br>`Composition: Over-the-shoulder,`<br>`Eye-level`<br>Narrative:<br> <br>Environment:<br>`Location: Hospital Room`<br>`Time: Daylight`<br>Character:<br>`ID 1: Patient in Bed`<br>Cinematography:<br>`Shot: Medium Shot, Static`<br>`Composition: Centered composition`<br>`with the character, Eye-level`<br>Narrative:<br>|Shot  1<br>Subtitles<br>`01:40:27,830 -> 01:40:32,010`<br>**`[Jim Gordon]`** `The doctor says`<br>`you're in agonizing pain, but`<br>`you won't accept medication. `<br>`01:40:27,830 --> 01:40:32,010`<br>**`[Jim Gordon]`** `That you're`<br>`refusing to accept skin`<br>`grafts.`<br>`01:40:38,150 --> 01:40:42,430`<br>**`[Harvey Dent]`** `Remember that`<br>`name you all had for me when I`<br>`was at Internal Affairs?`<br> <br>...<br>Shot 4<br>Environment:<br>`Location: Hospital Bed`<br>`Time: Daylight`<br>Character:<br>`ID 1: Person in Foreground`<br>Cinematography:<br>`Shot: Close-up, Static`<br>`Composition: Over-the-shoulder,`<br>`Eye-level`<br>Narrative:<br> <br>Environment:<br>`Location: Hospital Room`<br>`Time: Daylight`<br>Character:<br>`ID 1: Patient in Bed`<br>Cinematography:<br>`Shot: Medium Shot, Static`<br>`Composition: Centered composition`<br>`with the character, Eye-level`<br>Narrative:<br>|Shot  1<br>Subtitles<br>`01:40:27,830 -> 01:40:32,010`<br>**`[Jim Gordon]`** `The doctor says`<br>`you're in agonizing pain, but`<br>`you won't accept medication. `<br>`01:40:27,830 --> 01:40:32,010`<br>**`[Jim Gordon]`** `That you're`<br>`refusing to accept skin`<br>`grafts.`<br>`01:40:38,150 --> 01:40:42,430`<br>**`[Harvey Dent]`** `Remember that`<br>`name you all had for me when I`<br>`was at Internal Affairs?`<br> <br>...<br>Shot 4<br>Environment:<br>`Location: Hospital Bed`<br>`Time: Daylight`<br>Character:<br>`ID 1: Person in Foreground`<br>Cinematography:<br>`Shot: Close-up, Static`<br>`Composition: Over-the-shoulder,`<br>`Eye-level`<br>Narrative:<br> <br>Environment:<br>`Location: Hospital Room`<br>`Time: Daylight`<br>Character:<br>`ID 1: Patient in Bed`<br>Cinematography:<br>`Shot: Medium Shot, Static`<br>`Composition: Centered composition`<br>`with the character, Eye-level`<br>Narrative:<br>|Shot  1<br>Subtitles<br>`01:40:27,830 -> 01:40:32,010`<br>**`[Jim Gordon]`** `The doctor says`<br>`you're in agonizing pain, but`<br>`you won't accept medication. `<br>`01:40:27,830 --> 01:40:32,010`<br>**`[Jim Gordon]`** `That you're`<br>`refusing to accept skin`<br>`grafts.`<br>`01:40:38,150 --> 01:40:42,430`<br>**`[Harvey Dent]`** `Remember that`<br>`name you all had for me when I`<br>`was at Internal Affairs?`<br> <br>...<br>Shot 4<br>Environment:<br>`Location: Hospital Bed`<br>`Time: Daylight`<br>Character:<br>`ID 1: Person in Foreground`<br>Cinematography:<br>`Shot: Close-up, Static`<br>`Composition: Over-the-shoulder,`<br>`Eye-level`<br>Narrative:<br> <br>Environment:<br>`Location: Hospital Room`<br>`Time: Daylight`<br>Character:<br>`ID 1: Patient in Bed`<br>Cinematography:<br>`Shot: Medium Shot, Static`<br>`Composition: Centered composition`<br>`with the character, Eye-level`<br>Narrative:<br>|Shot  1<br>Subtitles<br>`01:40:27,830 -> 01:40:32,010`<br>**`[Jim Gordon]`** `The doctor says`<br>`you're in agonizing pain, but`<br>`you won't accept medication. `<br>`01:40:27,830 --> 01:40:32,010`<br>**`[Jim Gordon]`** `That you're`<br>`refusing to accept skin`<br>`grafts.`<br>`01:40:38,150 --> 01:40:42,430`<br>**`[Harvey Dent]`** `Remember that`<br>`name you all had for me when I`<br>`was at Internal Affairs?`<br> <br>...<br>Shot 4<br>Environment:<br>`Location: Hospital Bed`<br>`Time: Daylight`<br>Character:<br>`ID 1: Person in Foreground`<br>Cinematography:<br>`Shot: Close-up, Static`<br>`Composition: Over-the-shoulder,`<br>`Eye-level`<br>Narrative:<br> <br>Environment:<br>`Location: Hospital Room`<br>`Time: Daylight`<br>Character:<br>`ID 1: Patient in Bed`<br>Cinematography:<br>`Shot: Medium Shot, Static`<br>`Composition: Centered composition`<br>`with the character, Eye-level`<br>Narrative:<br>|Shot  1<br>Subtitles<br>`01:40:27,830 -> 01:40:32,010`<br>**`[Jim Gordon]`** `The doctor says`<br>`you're in agonizing pain, but`<br>`you won't accept medication. `<br>`01:40:27,830 --> 01:40:32,010`<br>**`[Jim Gordon]`** `That you're`<br>`refusing to accept skin`<br>`grafts.`<br>`01:40:38,150 --> 01:40:42,430`<br>**`[Harvey Dent]`** `Remember that`<br>`name you all had for me when I`<br>`was at Internal Affairs?`<br> <br>...<br>Shot 4<br>Environment:<br>`Location: Hospital Bed`<br>`Time: Daylight`<br>Character:<br>`ID 1: Person in Foreground`<br>Cinematography:<br>`Shot: Close-up, Static`<br>`Composition: Over-the-shoulder,`<br>`Eye-level`<br>Narrative:<br> <br>Environment:<br>`Location: Hospital Room`<br>`Time: Daylight`<br>Character:<br>`ID 1: Patient in Bed`<br>Cinematography:<br>`Shot: Medium Shot, Static`<br>`Composition: Centered composition`<br>`with the character, Eye-level`<br>Narrative:<br>|Shot  1<br>Subtitles<br>`01:40:27,830 -> 01:40:32,010`<br>**`[Jim Gordon]`** `The doctor says`<br>`you're in agonizing pain, but`<br>`you won't accept medication. `<br>`01:40:27,830 --> 01:40:32,010`<br>**`[Jim Gordon]`** `That you're`<br>`refusing to accept skin`<br>`grafts.`<br>`01:40:38,150 --> 01:40:42,430`<br>**`[Harvey Dent]`** `Remember that`<br>`name you all had for me when I`<br>`was at Internal Affairs?`<br> <br>...<br>Shot 4<br>Environment:<br>`Location: Hospital Bed`<br>`Time: Daylight`<br>Character:<br>`ID 1: Person in Foreground`<br>Cinematography:<br>`Shot: Close-up, Static`<br>`Composition: Over-the-shoulder,`<br>`Eye-level`<br>Narrative:<br> <br>Environment:<br>`Location: Hospital Room`<br>`Time: Daylight`<br>Character:<br>`ID 1: Patient in Bed`<br>Cinematography:<br>`Shot: Medium Shot, Static`<br>`Composition: Centered composition`<br>`with the character, Eye-level`<br>Narrative:<br>|Shot  1<br>Subtitles<br>`01:40:27,830 -> 01:40:32,010`<br>**`[Jim Gordon]`** `The doctor says`<br>`you're in agonizing pain, but`<br>`you won't accept medication. `<br>`01:40:27,830 --> 01:40:32,010`<br>**`[Jim Gordon]`** `That you're`<br>`refusing to accept skin`<br>`grafts.`<br>`01:40:38,150 --> 01:40:42,430`<br>**`[Harvey Dent]`** `Remember that`<br>`name you all had for me when I`<br>`was at Internal Affairs?`<br> <br>...<br>Shot 4<br>Environment:<br>`Location: Hospital Bed`<br>`Time: Daylight`<br>Character:<br>`ID 1: Person in Foreground`<br>Cinematography:<br>`Shot: Close-up, Static`<br>`Composition: Over-the-shoulder,`<br>`Eye-level`<br>Narrative:<br> <br>Environment:<br>`Location: Hospital Room`<br>`Time: Daylight`<br>Character:<br>`ID 1: Patient in Bed`<br>Cinematography:<br>`Shot: Medium Shot, Static`<br>`Composition: Centered composition`<br>`with the character, Eye-level`<br>Narrative:<br>|Shot  1<br>Subtitles<br>`01:40:27,830 -> 01:40:32,010`<br>**`[Jim Gordon]`** `The doctor says`<br>`you're in agonizing pain, but`<br>`you won't accept medication. `<br>`01:40:27,830 --> 01:40:32,010`<br>**`[Jim Gordon]`** `That you're`<br>`refusing to accept skin`<br>`grafts.`<br>`01:40:38,150 --> 01:40:42,430`<br>**`[Harvey Dent]`** `Remember that`<br>`name you all had for me when I`<br>`was at Internal Affairs?`<br> <br>...<br>Shot 4<br>Environment:<br>`Location: Hospital Bed`<br>`Time: Daylight`<br>Character:<br>`ID 1: Person in Foreground`<br>Cinematography:<br>`Shot: Close-up, Static`<br>`Composition: Over-the-shoulder,`<br>`Eye-level`<br>Narrative:<br> <br>Environment:<br>`Location: Hospital Room`<br>`Time: Daylight`<br>Character:<br>`ID 1: Patient in Bed`<br>Cinematography:<br>`Shot: Medium Shot, Static`<br>`Composition: Centered composition`<br>`with the character, Eye-level`<br>Narrative:<br>|
|`Action: Lying`<br>`Emotion: Serious`<br>`Context: To esta`<br>`presence and ser`<br>`a key character`|`, Somber`<br>`  blish the`<br>`  ious demean`<br>`   in a formal`|`   or of`|`Action:`<br>`Emotion`<br>`Context`<br>`charact`<br>`interna`|` Speaking`<br>`: Somber, Intense`<br>`: To capture the`<br>`er's emotional respon`<br>`l conflict during a s`|` Speaking`<br>`: Somber, Intense`<br>`: To capture the`<br>`er's emotional respon`<br>`l conflict during a s`|`  se and`<br>`    rious`|`01:40:52,570`<br>**`[Harvey Dent`**<br>`01:41:05,130`<br>|<br>**` ]`** `Say it. Say it!`<br>` --> 01:41:07,310`<br>|
|<br>`setting.`|<br>`setting.`|<br>`setting.`|<br>`conversation.`|<br>`conversation.`|<br>`conversation.`|<br>`conversation.`|<br>**`[Jim Gordon]`** `Two-Face, Harvey`<br>`Two-Face.`|<br>**`[Jim Gordon]`** `Two-Face, Harvey`<br>`Two-Face.`|
|(2) Semantic Scene Aggregation|(2) Semantic Scene Aggregation|(2) Semantic Scene Aggregation|(2) Semantic Scene Aggregation|(2) Semantic Scene Aggregation|(2) Semantic Scene Aggregation|(2) Semantic Scene Aggregation|(2) Semantic Scene Aggregation|(2) Semantic Scene Aggregation|
|⭐` 5/5 (Class: Content, Usable)`<br>Visual Score:<br>Character:<br>Narrative:<br>Emotion:<br>Cinematography:<br>Scene-level Caption<br>Narrative-Coherent<br>Narrative-Coherent<br>Narrative-Coherent<br>Identity-Aware<br>Identity-Aware<br>Identity-Aware<br>Production-Oriented<br>Production-Oriented<br>Production-Oriented<br>Scene 0<br>`Close-up of face to Reveal of disfigurement .`<br>`Harvey Dent (Subject), Jim Gordon (Interactor).`<br>`         Harvey Dent lies in a hospital bed, his face bandaged and`<br>`his body in agony, refusing skin grafts and medication. Jim Gordon`<br>`visits him, expressing sorrow for Rachel's death and confronting`<br>`Dent about his transformation ....`<br>`Somber (Start), Tense (Dialogue), Tragic (Climax)`|⭐` 5/5 (Class: Content, Usable)`<br>Visual Score:<br>Character:<br>Narrative:<br>Emotion:<br>Cinematography:<br>Scene-level Caption<br>Narrative-Coherent<br>Narrative-Coherent<br>Narrative-Coherent<br>Identity-Aware<br>Identity-Aware<br>Identity-Aware<br>Production-Oriented<br>Production-Oriented<br>Production-Oriented<br>Scene 0<br>`Close-up of face to Reveal of disfigurement .`<br>`Harvey Dent (Subject), Jim Gordon (Interactor).`<br>`         Harvey Dent lies in a hospital bed, his face bandaged and`<br>`his body in agony, refusing skin grafts and medication. Jim Gordon`<br>`visits him, expressing sorrow for Rachel's death and confronting`<br>`Dent about his transformation ....`<br>`Somber (Start), Tense (Dialogue), Tragic (Climax)`|⭐` 5/5 (Class: Content, Usable)`<br>Visual Score:<br>Character:<br>Narrative:<br>Emotion:<br>Cinematography:<br>Scene-level Caption<br>Narrative-Coherent<br>Narrative-Coherent<br>Narrative-Coherent<br>Identity-Aware<br>Identity-Aware<br>Identity-Aware<br>Production-Oriented<br>Production-Oriented<br>Production-Oriented<br>Scene 0<br>`Close-up of face to Reveal of disfigurement .`<br>`Harvey Dent (Subject), Jim Gordon (Interactor).`<br>`         Harvey Dent lies in a hospital bed, his face bandaged and`<br>`his body in agony, refusing skin grafts and medication. Jim Gordon`<br>`visits him, expressing sorrow for Rachel's death and confronting`<br>`Dent about his transformation ....`<br>`Somber (Start), Tense (Dialogue), Tragic (Climax)`|⭐` 5/5 (Class: Content, Usable)`<br>Visual Score:<br>Character:<br>Narrative:<br>Emotion:<br>Cinematography:<br>Scene-level Caption<br>Narrative-Coherent<br>Narrative-Coherent<br>Narrative-Coherent<br>Identity-Aware<br>Identity-Aware<br>Identity-Aware<br>Production-Oriented<br>Production-Oriented<br>Production-Oriented<br>Scene 0<br>`Close-up of face to Reveal of disfigurement .`<br>`Harvey Dent (Subject), Jim Gordon (Interactor).`<br>`         Harvey Dent lies in a hospital bed, his face bandaged and`<br>`his body in agony, refusing skin grafts and medication. Jim Gordon`<br>`visits him, expressing sorrow for Rachel's death and confronting`<br>`Dent about his transformation ....`<br>`Somber (Start), Tense (Dialogue), Tragic (Climax)`|⭐` 5/5 (Class: Content, Usable)`<br>Visual Score:<br>Character:<br>Narrative:<br>Emotion:<br>Cinematography:<br>Scene-level Caption<br>Narrative-Coherent<br>Narrative-Coherent<br>Narrative-Coherent<br>Identity-Aware<br>Identity-Aware<br>Identity-Aware<br>Production-Oriented<br>Production-Oriented<br>Production-Oriented<br>Scene 0<br>`Close-up of face to Reveal of disfigurement .`<br>`Harvey Dent (Subject), Jim Gordon (Interactor).`<br>`         Harvey Dent lies in a hospital bed, his face bandaged and`<br>`his body in agony, refusing skin grafts and medication. Jim Gordon`<br>`visits him, expressing sorrow for Rachel's death and confronting`<br>`Dent about his transformation ....`<br>`Somber (Start), Tense (Dialogue), Tragic (Climax)`|⭐` 5/5 (Class: Content, Usable)`<br>Visual Score:<br>Character:<br>Narrative:<br>Emotion:<br>Cinematography:<br>Scene-level Caption<br>Narrative-Coherent<br>Narrative-Coherent<br>Narrative-Coherent<br>Identity-Aware<br>Identity-Aware<br>Identity-Aware<br>Production-Oriented<br>Production-Oriented<br>Production-Oriented<br>Scene 0<br>`Close-up of face to Reveal of disfigurement .`<br>`Harvey Dent (Subject), Jim Gordon (Interactor).`<br>`         Harvey Dent lies in a hospital bed, his face bandaged and`<br>`his body in agony, refusing skin grafts and medication. Jim Gordon`<br>`visits him, expressing sorrow for Rachel's death and confronting`<br>`Dent about his transformation ....`<br>`Somber (Start), Tense (Dialogue), Tragic (Climax)`|⭐` 5/5 (Class: Content, Usable)`<br>Visual Score:<br>Character:<br>Narrative:<br>Emotion:<br>Cinematography:<br>Scene-level Caption<br>Narrative-Coherent<br>Narrative-Coherent<br>Narrative-Coherent<br>Identity-Aware<br>Identity-Aware<br>Identity-Aware<br>Production-Oriented<br>Production-Oriented<br>Production-Oriented<br>Scene 0<br>`Close-up of face to Reveal of disfigurement .`<br>`Harvey Dent (Subject), Jim Gordon (Interactor).`<br>`         Harvey Dent lies in a hospital bed, his face bandaged and`<br>`his body in agony, refusing skin grafts and medication. Jim Gordon`<br>`visits him, expressing sorrow for Rachel's death and confronting`<br>`Dent about his transformation ....`<br>`Somber (Start), Tense (Dialogue), Tragic (Climax)`|⭐` 5/5 (Class: Content, Usable)`<br>Visual Score:<br>Character:<br>Narrative:<br>Emotion:<br>Cinematography:<br>Scene-level Caption<br>Narrative-Coherent<br>Narrative-Coherent<br>Narrative-Coherent<br>Identity-Aware<br>Identity-Aware<br>Identity-Aware<br>Production-Oriented<br>Production-Oriented<br>Production-Oriented<br>Scene 0<br>`Close-up of face to Reveal of disfigurement .`<br>`Harvey Dent (Subject), Jim Gordon (Interactor).`<br>`         Harvey Dent lies in a hospital bed, his face bandaged and`<br>`his body in agony, refusing skin grafts and medication. Jim Gordon`<br>`visits him, expressing sorrow for Rachel's death and confronting`<br>`Dent about his transformation ....`<br>`Somber (Start), Tense (Dialogue), Tragic (Climax)`|⭐` 5/5 (Class: Content, Usable)`<br>Visual Score:<br>Character:<br>Narrative:<br>Emotion:<br>Cinematography:<br>Scene-level Caption<br>Narrative-Coherent<br>Narrative-Coherent<br>Narrative-Coherent<br>Identity-Aware<br>Identity-Aware<br>Identity-Aware<br>Production-Oriented<br>Production-Oriented<br>Production-Oriented<br>Scene 0<br>`Close-up of face to Reveal of disfigurement .`<br>`Harvey Dent (Subject), Jim Gordon (Interactor).`<br>`         Harvey Dent lies in a hospital bed, his face bandaged and`<br>`his body in agony, refusing skin grafts and medication. Jim Gordon`<br>`visits him, expressing sorrow for Rachel's death and confronting`<br>`Dent about his transformation ....`<br>`Somber (Start), Tense (Dialogue), Tragic (Climax)`|



**Fig. 3:** _**Left:**_ _**Video**_ _**Shots**_ _**Aggregation.**_ We first perform shot detection on the
entire video and conduct a caption for a detailed understanding. Then, we use an LLM
to aggregate similar content for a scene-level description. _**Right:**_ _**The**_ _**workflow**_ _**of**_
_**Playwriter.**_ Playwriter generate the whole storyline according to the input, and gives
the detailed shot plan of each specific shot of music.


**Video** **Shots** **Aggregation:** **From** **Shot** **to** **Scene** Effective editing requires
both fine-grained and coarse-grained narrative comprehension. To reconcile these
granularity requirements within the context window limits of MLLMs [2], we propose a hierarchical aggregation strategy (Fig. 3 Left). Specifically, we discretize
the footage _V_ into atomic _shots_ _S_ defined as fundamental visual units bounded
by camera cuts, which are subsequently aggregated into _scenes_ _Z_ forming contiguous, spatio-temporally coherent shot sequences.
_Shot_ _Parsing_ _and_ _Scene_ _Aggregation._ To instantiate this hierarchy, we first obtain the atomic shots _S_ using boundary detection [6]. For each shot _si_, we extract
semantic attributes _A_ ( _si_ ) covering cinematography, character dynamics, and environment via an MLLM [2]. To group these individual shots into the defined
scenes, we compute a transition similarity Sim( _si, si_ +1) = _**α**_ _[⊤]_ **v** _i,i_ +1 between
adjacent shots. Here, **v** _i,i_ +1 denotes the attribute-wise similarity vector derived
from the LLM [20] features, and _**α**_ represents the weight vector balancing the
importance of different attributes. A scene boundary is induced whenever this
similarity score drops below a predefined threshold _τ_, effectively partitioning the
continuous footage into discrete, meaningful narrative blocks.
_Character-Aware_ _Grounding._ To ensure narrative consistency involving recurring protagonists, we implement a identity injection. We first analyze the dialogue to infer character identities _H_ (names and roles). These identities are
injected as textual conditioning into the MLLM [28] during scene analysis. This
grounds the generated descriptive summary _D_ ( _zj_ ) in specific personas (e.g., replacing “a man” with “Joker”), facilitating reliable cross-scene character tracking.


**Structural** **Audio** **Parsing** To maximize Rhythmic Alignment ( _Q_ sync), we
convert the continuous music waveform _M_ into a discrete grid of potential


CutClaw: Agentic Hours-Long Video Editing via Music Synchronization 7


cut points. We employ a hierarchical strategy that bridges micro-level rhythm
(beats) with macro-level musical form (sections), providing the Playwriter with
rigid temporal anchors.


_Hierarchical_ _Keypoint_ _Detection._ We first extract perceptually salient _Sound_
_Keypoints_ _K_ on a discrete time axis _T_ [4]. We identify three types of candidates:
(i) Downbeats _K_ db (bar-level accents); (ii) Pitch Changes _K_ pc (melodic transitions); and (iii) Spectral Energy Changes _K_ se (timbral transitions). We form a
unified candidate pool _K_ 0 = _K_ db _∪K_ pc _∪K_ se and apply temporal filtering _Φ_ ( _·_ )
(e.g., peak de-duplication) to obtain robust boundaries _K_ = _Φ_ ( _K_ 0).


_Structure-Guided Refinement._ To organize these keypoints, we use an MLLM [28]
to partition the track into coarse structural units _U_ = _{uj}_ _[M]_ _j_ =1 [(e.g.,] [verse,]
chorus). Within each unit _uj_, we score the contained keypoints _t_ _∈K ∩_ _uj_ to
retain only the most significant boundaries. The significance score is computed
as a weighted sum of cue intensities:


\mat _h_ r m _[{]_ **s** c _o_ r _e_ }(t) **=** _\_ b o ldsymbo _l_ _{_ \beta _}_ ^ _{_ \top } _\_,\ _[m]_ _a_ (2)


where int _∗_ ( _t_ ) denotes the intensity of each respective type at time _t_, and _**β**_ is the
weight vector. Finally, we generate structure-aligned captions, describing local
rhythm, emotion, and energy to guide the visual matching.


**3.3** **Playwriter:** **Music-Anchored** **Script** **Synthesis**


Given the decomposed semantic scenes _Z_ and structural audio units _U_, Playwriter [9] utilizes the musical structure _U_ as the invariant temporal anchor for
storytelling(Fig. 3 Right). By strictly grounding the visual narrative progression
onto this auditory skeleton, the Playwriter enforces Rhythmic Alignment ( _Q_ sync)
while optimizing for Instruction Fidelity ( _Q_ cond) and Narrative Flow ( _Q_ narr). It
utilizes structural scene allocation and keypoint-aligned shot planning to map
the video scenes _Z_ onto the musical structure _U_, generating a shot plan subject
to strictly formalized execution rules to guarantee validity:


1. _Disjoint_ _Resource_ _Allocation_ _(Non-Overlap):_ To prevent temporal redundancy, the Playwriter strictly partitions the scene _Z_ . Let _Zuj_ _⊂Z_ denote
the subset of scenes allocated to the _j_ -th musical unit. For any two distinct
units _uj, uk_ _∈U_, we enforce: _Zuj_ _∩Zuk_ = _∅._ This exclusive assignment
ensures that no source material is reused across different narrative blocks,
logically satisfying the global non-overlap constraint by construction.
2. _Structural_ _Temporal_ _Anchoring_ _(Music_ _Duration):_ To enforce the duration
constraint, the generated shot plan _Pj_ for each unit _uj_ inherits the fixed temporal topology of the audio. The total planned duration is strictly anchored
to the audio interval length: [�] _p∈Pj_ [Duration][(] _[p]_ [)] _[ ≡|][u][j][|][.]_


Below, we give the details workflow.


8 Zhao et al.


**Structural** **Scene** **Allocation** The first stage constructs a global mapping
between musical structural units and visual scenes. Let _U_ = _{uj}_ _[M]_ _j_ =1 [denote] [the]
set of musical units derived in Sec. 3.2. The agent generates a structure proposal
_P_ that assigns a subset of candidate scenes _Zuj_ _⊂Z_ to each unit _uj_ .
The allocation is formulated as a conditional generation task:


_\_ m _a_ thcal _{Z} __ _{ u_ _ _j_ (3)


where _Φ_ macro represents the LLM-based [9] planning function conditioned on the
user instruction _I_ . To satisfy the hard temporal constraints, we enforce a strict
disjoint set requirement:


_\_ _m ath_ c _al_ _{_ } __{_ (4)


If the generated proposal violates this condition (i.e., a scene is reused across
different musical sections), the system rejects _P_ and triggers a regeneration with
negative constraints.


**Keypoint-Aligned** **Shot** **Planning** The second stage refines the allocation
into a sequence of executable specifications. For each unit _uj_, let _{k_ 1 _, . . ., kL}_
be the set of fine-grained musical segments contained within its temporal scope.
The agent generates a shot plan consisting of specifications _{p_ 1 _, . . ., pL}_ .
Critically, rather than outputting final timestamps, each specification _pi_ =
( _τi, z_ id _, di_ ) serves as a _retrieval_ _constraint_ for the subsequent editing phase:


_τi_ **:** The target duration constraint derived directly from the audio segment _ki_,
ensuring rhythmic synchronization ( _Q_ sync).
_z_ id **:** The source scene index selected from _Zuj_, which restricts the retrieval search
space to the allocated narrative block.
_di_ **:** A semantic visual description (e.g., specific plot or emotion) that guides the
content matching within scene _z_ id.


This hierarchical binding transforms the global optimization problem into a
series of local retrieval tasks. By explicitly binding the _i_ -th shot to a specific
scene _z_ id, the Playwriter effectively prunes the search space for the downstream
Editor, ensuring that the final clip selection is conducted successfully.


**3.4** **Editor:** **Top-Down** **Hierarchical** **Visual** **Grounding**


Operating within the structural shot plan constrained by the Playwriter, the
Editor performs fine-grained temporal grounding to determine the precise continuous coordinates of the final timeline _E_ _[∗]_ . We instantiate the Editor as a
ReAct [31] agent designed to iteratively maximize the local energy terms of the
joint objective function (Eq. 1), specifically targeting Visual Quality ( _Q_ vis).


CutClaw: Agentic Hours-Long Video Editing via Music Synchronization 9



pool through a hypothesis
main actions:

**Action 1: Semantic Neigh-** **Fig. 4:** _**Editor**_ _**and**_ _**Reviewer**_ are used to perform
**borhood** **Retrieval.** This segment selection and validation. SNR stands for Seaction initializes the local mantic Neighborhood Retrieval, and FGST stands
search space _Ωi_ by retrieving for Fine-Grained Shot Trimming.
all shots belonging to the assigned scene _z_ id. To address potential content scarcity
or segmentation noise in the visual candidate, we incorporate an Adaptive Expansion mechanism. If the primary search space _Ωi_ = _{s_ _|_ _s_ _∈_ _z_ id _}_ fails to
yield a high-confidence candidate, the Editor expands the scope to the semantic
neighborhood:


_\_ [O] _[ m][e]_ _[g a]_ _['][ _][ i]_ [ = \Omega] [_i] _[ \]_ [c] _[u][p]_ (5)


This fallback strategy prevents retrieval dead-ends by aggregating shots from
adjacent structural units, ensuring the agent maintains a sufficient material pool
for optimization.

**Action** **2:** **Fine-Grained** **Shot** **Trimming.** To maximize the objective terms
_Q_ vis and _Q_ sync, the Editor employs a VLM-driven analysis tool to perform dense
temporal grounding within the candidate shots. For a candidate shot _s_ _∈_ _Ωi_,
the agent seeks a sub-segment _ci_ _⊂_ _s_ that maximizes a weighted local score:


_c_ [_] [i^* = ] a _r g_ \max } _ _{ c_ \subs _e t_ s, (6)
_\mathop_ _{\_


Here, _S_ aes represents the aesthetic score (contributing to _Q_ vis), and _R_ prot denotes
the _Protagonist_ _Presence_ _Ratio_ (contributing to _Q_ cond), where _α_ and _β_ are the
respective balancing weights. The presence ratio is computed by cross-referencing
frame content with the character identity set _H_ established in Sec. 3.2. If the
current segment yields a suboptimal score, the agent heuristically shifts the
temporal window based on VLM feedback until a high-fidelity clip is secured.

**Action** **3:** **Commit.** The Editor submits the trimmed candidate _ci_ to the Reviewer (Sec. 3.5). Upon receiving an approval signal, the clip is rendered and
committed to the final timeline _E_ _[∗]_ . Otherwise, the Editor triggers a backtracking mechanism to explore alternative intervals within _Ωi_ .











































**Fig. 4:** _**Editor**_ _**and**_ _**Reviewer**_ are used to perform
segment selection and validation. SNR stands for Semantic Neighborhood Retrieval, and FGST stands
for Fine-Grained Shot Trimming.


10 Zhao et al.


**3.5** **Reviewer:** **Multi-Criteria** **Validity** **Gate**


To ensure the final timeline _E_ _[∗]_ adheres to both narrative intent and structural
constraints, we introduce the Reviewer to operate as a discriminatory gate. As
shown in Fig. 4, this module audits every candidate clip _ci_ proposed by the
Editor through a rigorous rejection sampling mechanism. The reviewer checks
the consistency of the edited video from the following aspects:
**Semantic Identity Verification.** To enforce narrative consistency ( _Q_ cond), the
Reviewer validates that the visual subject strictly aligns with the target identity defined in _H_ . By computing a _Protagonist_ _Presence_ _Ratio_ via hierarchical
MLLM [2] sampling, we filter out false positives where the character is merely
a background extra, occluded, or unrecognizable. This ensures that the protagonist remains the primary visual focus throughout the sequence, distinguishing
the main characters from crowd elements.
**Temporal** **and** **Structural** **Integrity.** To maintain the topological validity of
the timeline, we enforce hard constraints on sequencing. The Reviewer verifies
_Non-Overlap_ ( _∩Eprev_ = _∅_ ) to prevent content duplication and checks _Duration_
_Fidelity_ to ensure the visual cut points align precisely with the rhythmic grid
of the music track _M_ . Any violation of these constraints triggers an immediate
rejection to preserve the global structure.
**Perceptual** **Quality** **Assurance.** To maximize aesthetic appeal ( _Q_ vis), the
module audits low-level visual saliency. It rejects shots exhibiting significant
quality degradation, ensuring that every committed segment meets broadcastlevel viewing standards. Upon detection of any violation, the Reviewer returns
structured feedback, prompting the Editor to backtrack and explore alternative
intervals within the semantic neighborhood.
If the candidate clip does not meet the requirements, the Reviewer will notify
the editor to select the relevant scene around the current one. By reviewing each
candidate clip in the optimized timeline, we obtain the final edited video.


**4** **Experiment**


**4.1** **Evaluation** **and** **Implementation**


**Benchmark.** To rigorously evaluate our framework, we establish a diverse benchmark specifically designed for agentic video editing tasks. Our dataset comprises
10 distinct source pairs, collected from 5 feature-length films and 5 long-duration
VLOGs, with raw footage lengths ranging from 1 to 3 hours. This collection accumulates to approximately 24 hours of total footage, ensuring a robust assessment
across both professionally cinematographed content and unscripted, naturalistic
recordings. The corresponding auditory inputs consist of 10 segmented music
tracks spanning a wide spectrum of genres, including Pop, Jazz, OST, Rock,
and R&B with target edit durations varying from 20 seconds to one minute.
To test the system’s semantic adaptability, we formulate two distinct instruction categories: _(1)Character-Centric_ _Instructions_, which constrain the edit to
focus exclusively on a single protagonist, thereby challenging the agent’s ability


CutClaw: Agentic Hours-Long Video Editing via Music Synchronization 11


to maintain identity consistency; and _(2)Narrative-Centric_ _Instructions_, which
demand the inclusion of multiple characters or complex interactions to convey a
cohesive visual story. In total, this benchmark yields 20 unique evaluation cases
(10 pairs _×_ 2 instruction types), covering a broad range of visual styles and
narrative requirements.
**Metrics.** We evaluate our framework via automated quantitative analysis and a
subjective user study. In the automated regime, _Visual_ _Quality_ and _Instruction_
_Follow_ are scored by GPT-5.2 [16] based on aesthetic integrity and semantic
alignment, respectively. Conversely, given the high temporal precision required
for audio-visual alignment, which remains challenging for MLLMs, _AV_ _Harmony_
is quantified via detecting the minimum temporal offset _∆t_ between audio onsets (downbeats, pitch) and video scenes, strictly rewarding alignments within a
perceptual threshold (e.g., _∆t ≤_ 0 _._ 1 _s_ ). The user study mirrors these three metrics to capture human perceptual preference and exclusively evaluates a fourth
dimension, _Human-Likeness_, which benchmarks the naturalness of the model’s
editing pacing and logic against professional human editors.
**Baselines.** We benchmark our framework against three representative methods covering different editing paradigms. NarratoAI [12] serves as a baseline for
subtitle-driven editing; it is a mainstream open-source framework that processes
full-video subtitles to generate clips based on textual instructions. Note that
NarratoAI is inapplicable to VLOG scenarios due to the scarcity of speech and
subtitles in such footage. UVCOM [26] and Time-R1 [25] represent state-of-theart approaches in moment retrieval and temporal grounding, respectively. Since
both models typically handle fixed-length short videos, we adapt them for longform footage by first segmenting the source video, then selecting the top-5 clips
with the highest confidence. Finally, we trim the selected segments to match the
target duration, discarding excess frames.
**Implementation Details.** For the core agentic framework, we employ MiniMaxM2.1 [14] to power the Editor and Reviewer agents, while Gemini3-Pro [9]
serves as the Playwriter. In the preprocessing stage, we utilize PySceneDetect [6]
for shot boundary detection and Whisper-v3-turbo [19] for Automatic Speech
Recognition (ASR) to extract subtitles. For multimodal understanding, Qwen3VL-30B-A3B [2] and Qwen3-Omni-30B-A3B [28] are deployed for visual and
music captioning, respectively. To optimize computational efficiency during inference, video footage is downsampled to a short-side resolution of 360p at a
frame rate of 2 FPS.


**4.2** **Main** **Results**


As presented in Tab. 1, CutClaw achieves superior performance across all quantitative metrics. Validating our coarse-to-fine editing strategy, our method consistently surpasses the strongest baselines in Visual Quality. Furthermore, CutClaw
leads the Instruction Follow metric, particularly excelling in object-oriented instruction, which demonstrates its precise visual content localization capabilities.
Finally, its dominant performance in AV Harmony confirms that the resulting
cuts are rigorously and rhythmically aligned with the input music. Fig. 6 shows


|2<br>Instruction<br>Input|Zhao et al.<br>“A montage of Rose's evolution on the Titanic: from trapped aristocrat to free spirit. Key shots:<br>despair at the ship's rail, joyous dancing in 3rd class, defiant spitting, and survival in freezing<br>water. Focus on her red hair, ocean backdrop, and the transition from tight corsets to loose<br>clothing.”|
|---|---|
|Input<br>Music|Input VIdeo Footage|


Iter 0 Get Shot Plan






```
Shot IDX: 1
Time Duration: 5.2s
Content: This is the discovery of the "Ghost" or Gravitational Anomaly. Cooper is in his daughter Murph's
bedroom, observing how the dust floating in the air is settling in a specific, non-random pattern on the floor

```









```
(Time_Range=[00:19:18 - 00:19:26])

```



```
Result Analysis show:
- [00:19:18 – 00:19:20] (2.0s):
 - Visual Composition: [Hard Cut] Close-up. Dark kitchen setting with minimal lighting through blinds. Slight motion blur observed.
 - Semantic Analysis: High tension (Intensity: Medium). The shot functions primarily to establish emotional distress.
 - Quality Assessment: Score 3 (Consistent low lighting).
- [00:19:20 – 00:19:23] (3.0s):
 - Visual Composition: [Hard Cut] Medium shot containing two subjects (older man, young girl). Environment features hanging lamp and appliances.

```



```
(Time_Range=[00:19:46 - 00:20:07])

```



```
Result Analysis show:

```


























**Fig. 5:** _**A**_ _**sample**_ _**execution**_ _**of**_ _**a**_ _**single-shot**_ _**cutting**_, utilizing footage from
movie “Interstellar” and the music “Moon.” Actions performed by the Playwright,
Editor, and Reviewer are color-coded in blue, yellow, and green, respectively. The

orange background traces the execution path leading to the final clip selection.


the qualitative comparison against baseline methods. When considering the overall edited quality, baseline methods exhibit rigid segment selection, completely
failing to align with the musical structure. While NarratoAI loosely follows user
instructions at the cost of severe visual degradation, UVCOM and Time-R1
maintain visual quality but lack logical narrative connections across shots. Additional video results are available in the supplementary material. To further


CutClaw: Agentic Hours-Long Video Editing via Music Synchronization 13





|Nostalgic|Col2|Playful|Joyful|Intense|Melancholic|Col7|Urgent|Hopeful|Tender|Col11|
|---|---|---|---|---|---|---|---|---|---|---|
||||||||||||
||||||||||||
||||||||||||
||||||||||||
||||||||||||
||||||||||||
||||||||||||
||||||||||||


Narrative-driven Instruction:


_“A deconstruction of the Hollywood Ending, using the song’s cynical yet tender lyrics to juxtapose the idealized ‘Epilogue’ sequence with_
_the gritty reality of the couple’s arguments and separation, illustrating that while they were each other's muse, real life—like the song_
_suggests—is far more complicated than a movie script.”_








|Tender|Col2|Col3|Dreamy|Col5|Col6|Col7|Resigned|Explosive|Col10|Col11|Col12|
|---|---|---|---|---|---|---|---|---|---|---|---|
|Tender|Tender|Tender||||||||||
|Tender|Tender|Tender||||||||||
|Tender|Tender|||||||||||
|Tender|Tender|||||||||||
|Tender||||||||||||
|Tender||||||||||||
|Tender||||||||||||
|Tender||||||||||||



**Fig. 6:** _**Qualitative**_ _**comparison**_ _**between**_ _**CutClaw**_ _**and**_ _**baseline**_ _**methods.**_ The
two cases utilize full-length footage from the films “Paprika” and “La La Land”, paired
with the musical tracks “Luv(sic) Pt.2” and “Norman F**king Rockwell”, respectively.
Shot boundary detection is performed using PySceneDetect [6].


illustrate our method, we provide an execution sample in Fig. 5, detailing the
collaborative workflow among the Playwriter, Editor, and Reviewer agents.


**Ablation** **Study** To validate the effectiveness of individual components within
CutClaw, we conducted an ablation study by systematically removing the Editor,



**Table** **1:** _**Comparision**_ . We report the
performance scores across three metrics: Visual Quality, Instruction Follow
(Obj/Nar), and AV Harmony.


**Method** **Visual** **Quality** **Instruction** **Follow** **AV** **Harmony**

Film Vlog Avg. Obj Nar Avg. Film Vlog Avg.


NarratoAI 75.7  - 75.7 56.0 72.0 64.0 84.9  - 84.9
UVCOM 71.2 73.6 72.4 60.8 64.5 62.6 78.9 79.7 79.3
Time-R1 73.3 72.6 72.9 51.9 71.0 61.5 77.0 75.8 76.4


**CutClaw** **79.2** **76.0** **77.6** **66.6** **73.4** **70.0** **85.7** **87.3** **86.5**



**Table** **2:** _**Ablation**_ _**Study**_ . We report the
performance impact of ablating the Editor,
Reviewer, or Audio Context across three
metrics.


**Method** **Visual** **Quality** **Instruction** **Follow** **AV** **Harmony**

Film Vlog Avg. Obj Nar Avg. Film Vlog Avg.


w/o Audio 77.3 73.8 75.5 63.4 **74.3** 68.9 78.0 76.5 77.2
w/o Editor 78.6 75.4 77.0 59.7 71.5 65.6 84.8 86.0 85.4
w/o Reviewer 78.1 74.0 76.0 **66.6** 72.9 69.8 85.1 **89.4** **87.2**


**CutClaw** **79.2** **76.0** **77.6** **66.6** 73.4 **70.0** **85.7** 87.3 86.5


14 Zhao et al.


**Table** **3:** _**User**_ _**Study**_ _**Results**_ . We report the percentage of user votes across four
metrics: Visual Quality, Instruction Following, Audio-Visual Harmony, and HumanLikeness. For each metric, we break down performance by instruction type (Narrative/Object) and video type (Film/Vlog). Avg. denotes the average score. Our method
outperforms baselines across all categories. - Note that NarratoAI cannot deal with
the VLOG as it does not have dense subtitles.


**Method** **Visual** **Quality** **Instruction** **Follow** **Audio-Visual** **Harmony** **Human-Like**

Nar Obj Film Vlog Avg Nar Obj Film Vlog Avg Nar Obj Film Vlog Avg Nar Obj Film Vlog Avg


NarratoAI* 11.6% 11.2% 27.3% - 11.4% 14.8% 10.8% 28.7% - 12.8% 11.2% 12.4% 25.3% - 11.8% 12.0% 8.4% 23.3% - 10.2%
UVCOM 18.0% 16.8% 7.3% 23.6% 17.4% 18.8% 13.2% 7.3% 22.0% 16.0% 17.2% 13.2% 6.0% 22.8% 15.2% 18.8% 15.6% 9.3% 23.6% 17.2%
Time-R1 25.2% 17.6% 18.0% 22.4% 21.4% 22.4% 19.6% 16.7% 24.0% 21.0% 23.2% 16.8% 17.3% 18.4% 20.0% 24.8% 22.8% 16.7% 25.6% 23.8%


**CutClaw** **45.2%** **54.4%** **47.3%** **54.0%** **49.8%** **44.0%** **56.4%** **47.3%** **53.6%** **50.2%** **48.4%** **57.6%** **51.3%** **57.6%** **53.0%** **44.4%** **53.2%** **50.7%** **50.4%** **48.8%**


Reviewer, and Audio Context, with results detailed in Tab. 2. We first observe
that replacing the Audio’s beat-aware analysis with fixed-length segmentation
causes AV Harmony to drop significantly from 86.5 to 77.2, confirming its necessity for rhythmic alignment. Similarly, removing the Reviewer leads to a decline
in Visual Quality from 77.6 to 76.0, as the system loses the feedback loop required
to refine low-quality candidates and transition mismatches. Finally, substituting
the Editor with a random clip selector degrades performance across both Visual
Quality and Instruction Following, reducing the average score from 70.0 to 65.6.
This demonstrates that the Editor’s hierarchical structuring is foundational for
preserving narrative coherence and semantic accuracy.


**User** **Study** To complement the objective metrics, we conducted a user preference study to assess the subjective quality of the generated videos. We recruit 25
participants to evaluate the results. The questionnaire consists of 80 evaluation
items, asking participants to vote for the best method across four dimensions: Visual Quality, Instruction Follow, Audio-Visual Harmony, and Human-Likeness.
In total, we collected 2,000 user opinions, providing a statistically robust basis
for our analysis. As illustrated in Tab. 3, CutClaw outperforms all baselines by
a significant margin across all categories. Specifically, our method receive 49.8%
of the votes for Visual Quality and 53.0% for Audio-Visual Harmony, which is
more than double the votes received by the second-best method, Time-R1 (21.4%
and 20.0%, respectively). Notably, in the Human-Like metric, CutClaw secured
48.8% of user preference, highlighting its ability to mimic professional human
editing logic better than existing automated solutions. These results align consistently with our quantitative findings, confirming the superiority of our approach
in real-world viewer evaluations.


**4.3** **Limitation**


Our framework still faces limitations. First, while we ensure strong narrative
flow, the system lacks advanced visual hooks, such as generated visual effects
or specific monologue highlights that are crucial for engaging content. Future
iterations could integrate generative video models to synthesize these expressive
elements. Second, the multi-stage pipeline processing extensive raw footage results in high inference latency. Optimizing the pipeline for speed or employing


CutClaw: Agentic Hours-Long Video Editing via Music Synchronization 15


coarse-to-fine processing strategies to enable real-time feedback remains a key
direction for future research.


**5** **Conclusion**


We presented CutClaw, an autonomous multi-agent framework designed to automate the complex task of professional video editing from hours-long raw footage.
By addressing the critical challenges of processing long contexts and achieving
precise audio-visual consistency, our approach bridges the gap between simple
clip assembly and instruction-aligned, music-driven storytelling. The core innovation of our framework lies in its hierarchical decomposition strategy, which transforms continuous high-dimensional data into structured semantic units. This
structure allows our specialized agents to collaborate effectively: the Playwriter
anchors the narrative to musical structure, the Editor performs fine-grained visual grounding, and the Reviewer enforces rigorous aesthetic and continuity constraints. Our extensive experimental results demonstrate that CutClaw significantly outperforms state-of-the-art baselines across key metrics, including Visual
Quality, Instruction Following, and AV Harmony.


**Acknowledgements**


This work was financially supported in part by the National Natural Science
Foundation of China (Project No. 62506064) and Guangdong Provincial Regional
Joint Fund (Project No. 2024A1515110052). The computational resources are
supported by SongShan Lake HPC Center (SSL-HPC) in Great Bay University.


**References**


1. Adobe: Adobe premiere pro (2026), `[https : / / www . adobe . com / products /](https://www.adobe.com/products/premiere.html)`
```
  premiere.html
```

2. Bai, S., Cai, Y., Chen, R., Chen, K., Chen, X., Cheng, Z., Deng, L., Ding, W.,
Gao, C., Ge, C., et al.: Qwen3-vl technical report. arXiv preprint arXiv:2511.21631
(2025)
3. Blackmagic Design: Davinci resolve 20 (2026), `[https://www.blackmagicdesign.](https://www.blackmagicdesign.com/products/davinciresolve)`
```
  com/products/davinciresolve
```

4. Böck, S., Korzeniowski, F., Schlüter, J., Krebs, F., Widmer, G.: madmom: a new
Python Audio and Music Signal Processing Library. In: Proceedings of the 24th
ACM International Conference on Multimedia. pp. 1174–1178. Amsterdam, The
Netherlands (10 2016). `[https://doi.org/10.1145/2964284.2973795](https://doi.org/10.1145/2964284.2973795)`
5. ByteDance: Capcut (2026), `[https://www.capcut.com/](https://www.capcut.com/)`
6. Castellano, B., collaborators: Pyscenedetect (2025), `[https://github.com/](https://github.com/Breakthrough/PySceneDetect)`
```
  Breakthrough/PySceneDetect
```

7. Chen, Y., Wang, W., Zheng, T., Wen, X., Yang, H., Zhang, Y.: Esa: Energybased shot assembly optimization for automatic video editing. arXiv preprint
arXiv:2511.02505 (2025)


16 Zhao et al.


8. Cheng, D., Zhan, H., Zhao, X., Liu, G., Li, Z., Xie, J., Song, Z., Feng, W., Peng,
B.: Text-to-edit: Controllable end-to-end video ad creation via multimodal llms.
arXiv preprint arXiv:2501.05884 (2025)
9. Google: Gemini3 (2025), `[https://deepmind.google/models/gemini/](https://deepmind.google/models/gemini/)`
10. Guo, Y., Liu, J., Li, M., Liu, Q., Chen, X., Tang, X.: Trace: Temporal grounding
video llm via causal event modeling. arXiv preprint arXiv:2410.05643 (2024)
11. HKUDS: Vimax: Agentic video generation (2025), `[https://github.com/HKUDS/](https://github.com/HKUDS/ViMax)`
```
  ViMax
```

12. linyqh: Narratoai (2025), `[https://github.com/linyqh/NarratoAI](https://github.com/linyqh/NarratoAI)`
13. Liu, C., Wu, H., Zhong, Y., Zhang, X., Wang, Y., Xie, W.: Intelligent grimmopen-ended visual storytelling via latent diffusion models. In: Proceedings of the
IEEE/CVF Conference on Computer Vision and Pattern Recognition. pp. 6190–
6200 (2024)
14. MiniMax AI: Minimax-m2.1: a sota model for real-world dev & agents. (2025),

```
  https://github.com/MiniMax-AI/MiniMax-M2.1
```

15. Mu, F., Mo, S., Li, Y.: Snag: Scalable and accurate video grounding. In: Proceedings of the IEEE/CVF conference on computer vision and pattern recognition. pp.
18930–18940 (2024)
16. OpenAI: Gpt-5.2 (2025), `[https://openai.com/index/introducing-gpt-5-2/](https://openai.com/index/introducing-gpt-5-2/)`
17. OpenAI: Chatgpt (2026), `[https://chatgpt.com/](https://chatgpt.com/)`
18. Pardo, A., Wang, J.H., Ghanem, B., Sivic, J., Russell, B., Heilbron, F.C.: Generative timelines for instructed visual assembly. arXiv preprint arXiv:2411.12293
(2024)
19. Radford, A., Kim, J.W., Xu, T., Brockman, G., McLeavey, C., Sutskever, I.: Robust
speech recognition via large-scale weak supervision. In: International conference on
machine learning. pp. 28492–28518. PMLR (2023)
20. Reimers, N., Gurevych, I.: Making monolingual sentence embeddings multilingual
using knowledge distillation. In: Proceedings of the 2020 Conference on Empirical
Methods in Natural Language Processing. Association for Computational Linguistics (11 2020), `[https://arxiv.org/abs/2004.09813](https://arxiv.org/abs/2004.09813)`
21. Sandoval-Castaneda, M., Russell, B., Sivic, J., Shakhnarovich, G., Caba Heilbron,
F.: Editduet: A multi-agent system for video non-linear editing. In: Proceedings
of the Special Interest Group on Computer Graphics and Interactive Techniques
Conference Conference Papers. pp. 1–11 (2025)
22. Sun, H., Zhou, M., Chen, W., Xie, W.: Tr-detr: Task-reciprocal transformer for
joint moment retrieval and highlight detection. In: Proceedings of the AAAI Conference on Artificial Intelligence. vol. 38, pp. 4998–5007 (2024)
23. Sun, M., Farhadi, A., Seitz, S.: Ranking domain-specific highlights by analyzing
edited videos. In: European conference on computer vision. pp. 787–802. Springer
(2014)
24. Wang, M., Yang, G.W., Hu, S.M., Yau, S.T., Shamir, A., et al.: Write-a-video:
computational video montage from themed text. ACM Trans. Graph. **38** (6), 177–
1 (2019)
25. Wang, Y., Wang, Z., Xu, B., Du, Y., Lin, K., Xiao, Z., Yue, Z., Ju, J., Zhang, L.,
Yang, D., et al.: Time-r1: Post-training large vision language model for temporal
video grounding. arXiv preprint arXiv:2503.13377 (2025)
26. Xiao, Y., Luo, Z., Liu, Y., Ma, Y., Bian, H., Ji, Y., Yang, Y., Li, X.: Bridging the
gap: A unified video comprehension framework for moment retrieval and highlight
detection. In: Proceedings of the IEEE/CVF conference on computer vision and
pattern recognition. pp. 18709–18719 (2024)


CutClaw: Agentic Hours-Long Video Editing via Music Synchronization 17


27. Xiong, B., Kalantidis, Y., Ghadiyaram, D., Grauman, K.: Less is more: Learning highlight detection from video duration. In: Proceedings of the IEEE/CVF
conference on computer vision and pattern recognition. pp. 1258–1267 (2019)
28. Xu, J., Guo, Z., Hu, H., Chu, Y., Wang, X., He, J., Wang, Y., Shi, X., He, T., Zhu,
X., et al.: Qwen3-omni technical report. arXiv preprint arXiv:2509.17765 (2025)
29. Xu, M., Wang, H., Ni, B., Zhu, R., Sun, Z., Wang, C.: Cross-category video highlight detection via set-based learning. In: Proceedings of the IEEE/CVF International Conference on Computer Vision. pp. 7970–7979 (2021)
30. Yang, L., Chen, Z., Li, X., Jia, P., Long, L., Yang, J.: Agent-based video trimming.
arXiv preprint arXiv:2412.09513 (2024)
31. Yao, S., Zhao, J., Yu, D., Du, N., Shafran, I., Narasimhan, K.R., Cao, Y.: React:
Synergizing reasoning and acting in language models. In: The eleventh international
conference on learning representations (2022)
32. Zhu, Z., Lin, K.Q., Shou, M.Z.: Paper2video: Automatic video generation from
scientific papers. arXiv preprint arXiv:2510.05096 (2025)


