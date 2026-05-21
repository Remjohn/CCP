#### **1 Introduction**

Driven by recent advancements in OS-level assistants, AI agents are rapidly evolving from conversational interfaces into integrated file-system coworkers. However, seamless human-AI collaboration requires transcending
the execution of isolated commands. As users exhibit profound variability in their workflows, organizational
habits, and execution styles, adapting to these distinct preferences is essential for agents to continuously align
with long-term user behavior. Effective personalization thus requires grounding in two complementary signals
from the file system (Lewis et al., 2020; Park et al., 2023): _behavioral_ _traces_, the sequence of operations a user
performs such as reading, creating, and reorganizing files, and _content_ _deltas_, the incremental outputs a user
actually produces and edits, which carry far stronger personal signatures than externally sourced materials
like downloaded references and pre-existing templates. By inferring stable preferences from these file-level
signals rather than transient dialogue, agents can achieve the reliable adaptation necessary for practical,
everyday coworking.


Despite its importance, personalized behavioral adaptation is severely hindered by bottlenecks in data,
evaluation, and methodology. First, regarding _data_, collecting real-world, multimodal, and long-trajectory
file-system data is prohibitively difficult (Xie et al., 2024; Mu et al., 2025). Strict privacy constraints and the
absence of scalable collection strategies limit the capture of diverse user preferences. Second, for _evaluation_,


1


**Figure 1** **Overview of the FileGram Project.** FileGram introduces a personalized AI coworker natively integrated into the
user file system. By consolidating cross-session activities and file outputs into long-term behavioral memory, the agent
infers intent and proactively synchronizes workspaces, establishing a new paradigm for real-world interactive coworking.


as shown in Table 1, existing benchmarks (Wu et al., 2024a; Hu et al., 2025) heavily prioritize conversational
recall or isolated GUI success rates (Zhou et al., 2024; Deng et al., 2023; Mialon et al., 2024), overlooking
memory-centric, personalized behavior understanding tasks. Finally, in terms of _methodology_, mainstream
memory architectures (Chhikara et al., 2025; Rasmussen et al., 2025; Li et al., 2025) remain fundamentally
interaction-centric. By relying on top-down dialogue summaries, they lack the bottom-up architecture required
to distill procedural behavior patterns from continuous file-system operations (Zeng et al., 2024). Documentcentric methods (Mathew et al., 2021; Ma et al., 2024; Han et al., 2025) treat files as fixed knowledge artifacts,
agnostic to _who_ produced them, and recent edit-based preference learning (Gao et al., 2024) remains limited
to single-turn generation. FileGram generalizes these insights to the file-system scale, jointly modeling
atomic actions and content deltas across long-horizon, multimodal trajectories.


To address these bottlenecks, we propose **FileGram**, a unified framework designed to ground agent memory
and personalization in file-system behavioral traces. This framework tackles the challenges through three core
components. First, to overcome data scarcity, **FileGramEngine** simulates multimodal file-system behavioral
traces across realistic scenarios to enable scalable data generation. Second, for robust evaluation, **FileGramBench**
serves as the first benchmark dedicated to memory-centric personalization tasks based on file-system operations.
It provides four distinct evaluation tracks and 16 attributes spanning procedural, semantic, and episodic
memory capabilities. Finally, to advance methodology, **FileGramOS** introduces the first bottom-up architecture
that constructs user profiles directly from atomic actions and content deltas rather than relying on top-down
dialogue summaries. Together, these components establish a comprehensive foundation to evaluate and
develop the next generation of memory-centric personalized AI coworkers.


Extensive experiments on FileGramBench reveal that existing memory systems struggle with file-system
personalization: context-based and narrative-first baselines top out at 48–50% accuracy, while multimodal
methods fare even worse at 44.7%. Our FileGramOS achieves 59.6% by preserving atomic actions and
content deltas in a bottom-up architecture. Further analysis exposes a clear capability hierarchy, where current
methods show partial competence in behavioral understanding but fail at shift attribution and multimodal
grounding. Through FileGram, we aim to provide the essential data, evaluation, and structural foundation
to drive the development of truly adaptive AI coworkers.


2


**Table 1** Comparison of FileGramBench with representative benchmarks. Only FileGramBench jointly provides
multimodal content, persistent memory, and file-system behavioral traces with controlled profiles. **Columns** : MS =
multi-session; MM = multimodal; UP = user profile; Me = explicit memory component; FR = fact retrieval; Re =
reasoning; KM = knowledge management; Pe = personalization.


**Data** **Evaluation**


**Benchmark** **Type** **#QA** **MS** **MM** **UP** **Me** **FR** **Re** **KM** **Pe**


DuLeMon (Xu et al., 2022) Conv.     - ✓ ✗ ✓ ✓ ✓ ✗ ✗ ✓
DialogBench (Ou et al., 2024) Conv. 9.8K ✓ ✗ ✗ ✓ ✓ ✗ ✗ ✗
MemoryBank (Zhong et al., 2024) Conv. 194 ✓ ✗ ✓ ✓ ✓ ✗ ✓ ✓
LongMemEval (Wu et al., 2024a) Conv. 500 ✓ ✗ ✓ ✓ ✓ ✓ ✓ ✗
MemAgentBench (Hu et al., 2025) Conv. 146 ✓ ✗ ✗ ✓ ✓ ✗ ✓ ✗
MMDU (Liu et al., 2024) Conv. 1.6K ✗ ✓ ✗ ✓ ✓ ✗ ✗ ✗
LoCoMo (Maharana et al., 2024) Conv. 7.5K ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓
MMRC (Xue et al., 2025) Conv. 28.7K ✓ ✓ ✗ ✓ ✓ ✓ ✓ ✗
Mem-Gallery (Bei et al., 2026) Conv. 1.7K ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✗


OSWorld (Xie et al., 2024) GUI 369 ✗ ✓ ✗ ✗ ✗ ✗ ✗ ✗
OfficeBench (Wang et al., 2024) GUI 300 ✗ ✓ ✗ ✗ ✗ ✗ ✗ ✗
MEMTRACK (Deshpande et al., 2025) Agent 47 ✓ ✗ ✗ ✓ ✓ ✓ ✗ ✗
AgencyBench (Li et al., 2026) Agent 138 ✓ ✗ ✗ ✓ ✓ ✗ ✓ ✗
Evo-Memory (Wei et al., 2025) Agent     - ✓ ✗ ✗ ✓ ✓ ✓ ✓ ✗
MemoryArena (He et al., 2026) Agent 766 ✓ ✗ ✗ ✓ ✓ ✓ ✓ ✗


**FileGramBench** ( **Ours** ) **File** **4.6K** ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓

#### **2 Related Work**


**Benchmarks for Agents and Memory.** Prior benchmarks evaluate memory through two dominant paradigms:
conversational recall and environmental task execution, as shown in Table 1. Conversational datasets focus
heavily on static semantic retrieval over extended text dialogues (Wu et al., 2024a; Maharana et al., 2024),
inherently stripping away the procedural context of real workflows. Conversely, execution-driven benchmarks
situate agents in realistic operating systems or web interfaces but treat memory as a latent variable implicitly
measured by objective task success (Zhou et al., 2024; Xie et al., 2024). While recent trajectory-aware
benchmarks (Zhao et al., 2026; He et al., 2026) evaluate memory strictly for universal reasoning and generic
fact retention, FileGramBench shifts this paradigm toward personalization. It provides the first controllable
suite to evaluate how effectively agents infer and predict user-specific behaviors directly from longitudinal
file-system traces.


**Memory System and Personalization for Agents.** Existing architectures predominantly extract explicit facts
and relational structures from conversational histories (Packer et al., 2023; Chhikara et al., 2025; Rasmussen
et al., 2025), remaining fundamentally disconnected from the user’s operational environment. While recent
advancements in multimodal perception (Lu et al., 2026; Lin et al., 2025) and trajectory tracking (Li et al.,
2025; Fang et al., 2025) capture temporal dynamics, they typically model these dimensions in isolation or
within highly constrained, simulation-based environments such as online shopping or social media (Wang
et al., 2025b; Jin et al., 2025). Crucially, no existing framework utilizes granular file-system activities to
jointly sustain the procedural, semantic, and episodic memory required for continuous coworking adaptation.
FileGramOS bridges this gap by directly encoding atomic file-system actions and content deltas into a
unified, three-channel memory framework for robust behavioral pattern extraction.

#### **3 FileGramEngine: Behavioral Data Generation**


In this section, we introduce FileGramEngine, the data-generation component of FileGram for synthesizing
realistic file-system behavioral traces conditioned on specific user profiles and tasks. We illustrate our task
formulation in Section 3.1, followed by the data engine in Section 3.2, which simulates controlled, long-term


3


**Figure 2** **Data generation pipeline.** FileGramEngine generates one trajectory per profile–task pair. Agents execute in
profile-isolated workspaces for each task; raw tool traces are filtered and canonicalized to retain real action signals
while removing simulation artifacts, and outputs are materialized as standardized behavioral traces with aligned
text/document/visual views for cross-modal evaluation.


**Table 2** Six behavioral dimensions with L/M/R tiers used for profile construction in FileGramEngine.


**Dim** **Name** **Left (L)** **Middle (M)** **Right (R)**


A Consumption Pattern Sequential deep reading Targeted search-first Breadth-first browsing
B Production Style Comprehensive & detailed Balanced Minimal & concise
C Organization Preference Deeply nested (3+ levels) Adaptive (1–2 levels) Flat (root only)
D Iteration Strategy Incremental small edits Balanced refinement Bulk rewrite
E Curation Selective (active cleanup) Pragmatic (moderate cleanup) Preservative (accumulative)
F Cross-Modal Behavior Visual-heavy (charts, figures) Balanced (tables) Text-only


trajectories, translating raw tool usage into typed atomic actions paired with rich file-level artifacts, such as
_content_ _deltas_ —the precise record of what changed in each file, comprising full snapshots for newly created
files and patch diffs for edits—and final agent outputs.


**3.1** **Profile & Task Formulation**


**Profile Design.** To systematically model user variance, our schema defines 19 fine-grained attributes per profile
as detailed in Section C.1 of Appendix, combining basic semantic identity fields ( _e.g._, role and language)
with six core behavioral dimensions shown in Table 2. These dimensions capture recurring user patterns
across distinct workflows: _Consumption_ _Pattern_ (A), _Production_ _Style_ (B), _Organization_ _Preference_ (C),
_Iteration_ _Strategy_ (D), _Curation_ (E), and _Cross-Modal_ _Behavior_ (F). We discretize each dimension into three
distinct tiers - L/M/R, to capture a realistic spectrum of behavioral styles, ranging from minimalist and
rapid execution to exhaustive and structured iteration, thus providing a controlled basis for the benchmark
attributes in FileGramBench. To ensure this control mechanism yields realistic behaviors, we let human
verifiers validate that the generated traces clearly reflect the profile specifications. Building on this validated
schema, we instantiate 20 diverse profiles with varying L/M/R combinations. We calibrate evaluation difficulty
by pairing profiles at two granularities: we test subtle behavioral shifts by differing in 1–2 dimensions, and
macro-level distinctions through pairs differing over 5 dimensions.


4


**Task Design.** We derive task design directly from the six profile dimensions: each task is constructed to elicit
trace-observable behavioral signals (Krathwohl, 2002). Tasks are organized into six types— _Understand_, _Create_,
_Organize_, _Synthesize_, _Iterate_, and _Maintain_ —ranging from focused single-dimension probes to compositional
multi-dimension settings. In total, we curate 32 tasks (16 text-centric, 16 multimodal), each initialized with
a pre-populated workspace curated from real personal file collections in HippoCamp (Yang et al., 2026),
collectively comprising 615 diverse input files spanning videos, audio, images, spreadsheets, presentations, and
PDFs. Details are in Section C.2.


**Behavioral Perturbation.** To prevent the generation of unrealistically static personas, we introduce deliberate
_behavioral_ _perturbation_ . Specifically, for each profile, five trajectories are forced to undergo a localized shift in
a task-relevant dimension by a single tier defined in Table 2. This injection of controlled noise serves a dual
purpose: first, it mirrors the natural behavioral fluctuations of real-world users, preventing memory systems
from exploiting overly consistent, shortcut-style heuristics. Second, these perturbed trajectories establish a
critical foundation for FileGramBench, explicitly powering Track 3 to evaluate a system’s robustness and
its capacity for persona drift detection.


**3.2** **Data Engine and Composition**


**FileGramEngine.** To synthesize the behavioral trajectories, the FileGramEngine pairs each profile with
every task, yielding 640 unique execution combinations as illustrated in Figure 2. Because the tasks inherently
alter the file system by creating, editing, and reorganizing files, we make sure each execution occurs within
an isolated, sandboxed workspace to strictly prevent behavioral cross-contamination. Within each sandbox,
a tool-using agent (Anthropic, 2025) prompted with the assigned persona and executes the task through a
continuous think–act–observe loop (Yao et al., 2022). Crucially, the engine organizes these interactions at
two distinct levels: raw shell commands and tool calls are abstracted into typed, atomic actions, while each
event is systematically paired with its corresponding content delta, capturing full snapshots for new files
and precise patch diffs for edits. Finally, a post-execution filter examines artificial simulation traces, such
as LLM thought processes and intermediate error logs, ensuring the resulting trajectories contain only pure,
behaviorally meaningful file operations.


**Dataset Composition.** The pipeline produces 640 behavioral trajectories, comprising 20,028 atomic actions
and approximately 2.5K agent-generated files. By interleaving structured procedural logs with fine-grained
content deltas, each trajectory provides a highly granular chronological record that collaboratively serves as the
empirical foundation for FileGramBench. To further enrich modality diversity for cross-modal evaluation,
we develop a decomposition pipeline that segments text-based outputs into semantically coherent sections
and renders them across diverse target modalities. This expansion yields over 10K multimodal files spanning
PDFs, slide presentations, images, audio narrations, and other formats (Figure 3). Together, these trajectories
and their multimodal derivatives constitute the foundational corpus for FileGramBench evaluations.

#### **4 FileGramBench: Evaluation Framework**


FileGramBench comprises 4.6K memory-targeted QA pairs across nine sub-tasks organized into four
tracks (Figure 4), covering procedural, semantic, and episodic memory channels. The benchmark spans both
simulated behavioral trajectories and real-world human screen recordings, with ground truth derived from
predefined user profiles to ensure objective evaluation.


**4.1** **Automatic QA Generation**


FileGramBench converts behavioral trajectories from FileGramEngine into structured evaluation items
through a template-based pipeline.


**MCQ Construction.** Answer options are constructed from predefined profile attributes in the templates, with
distractors drawn from fine-grained profile pairs differing in only 1–2 dimensions to ensure genuine behavioral
discrimination. Trajectory sequence fragments serve as both evidence context and, in some sub-tasks, answer
candidates. GPT-4.1 generates the natural-language questions given the options and context.


5


|A<br>F<br>Name: Aisha<br>Role: Executive<br>Assistant E|Col2|Col3|Col4|Col5|Col6|Col7|
|---|---|---|---|---|---|---|
|Name: Aisha<br>Role: Executive<br>Assistant<br>E<br>F<br>A<br>|Name: Aisha<br>Role: Executive<br>Assistant<br>E<br>F<br>A<br>|Name: Aisha<br>Role: Executive<br>Assistant<br>E<br>F<br>A<br>|Name: Aisha<br>Role: Executive<br>Assistant<br>E<br>F<br>A<br>||||
|Name: Aisha<br>Role: Executive<br>Assistant<br>E<br>F<br>A<br>|Name: Aisha<br>Role: Executive<br>Assistant<br>E<br>F<br>A<br>|Name: Aisha<br>Role: Executive<br>Assistant<br>E<br>F<br>A<br>|Name: Aisha<br>Role: Executive<br>Assistant<br>E<br>F<br>A<br>||||
|Name: Aisha<br>Role: Executive<br>Assistant<br>E<br>F<br>A<br>|Name: Aisha<br>Role: Executive<br>Assistant<br>E<br>F<br>A<br>|Name: Aisha<br>Role: Executive<br>Assistant<br>E<br>F<br>A<br>|Name: Aisha<br>Role: Executive<br>Assistant<br>E<br>F<br>A<br>|Name: Aisha<br>Role: Executive<br>Assistant<br>E<br>F<br>A<br>|Name: Aisha<br>Role: Executive<br>Assistant<br>E<br>F<br>A<br>|Name: Aisha<br>Role: Executive<br>Assistant<br>E<br>F<br>A<br>|
||||<br><br>|<br><br>|<br><br>|<br><br>|
||||<br><br>|<br><br>|<br><br>|<br><br>|
||||<br><br>|<br><br>|<br><br>|<br><br>|









**Figure 3** **Data distribution.** 20 profiles _×_ 32 tasks yield 640 trajectories comprising _∼_ 10K output files and 20,028 atomic
actions.


**Open-endedConstruction.** Ground-truth answers are derived
from profile templates. We define per-attribute rubrics and
use an LLM judge to score each response on a Likert 1–5
scale.


**Real-world Annotation.** Beyond simulated trajectories, we
also collect real-world screen recordings. We first convert
simulated trajectories into GUI-level operation sequences
as behavioral guidance videos. Human participants then
receive the task description, behavioral profile, and this
guidance video, and perform the task while their screen is
recorded. This pipeline ensures controllable data collection
while grounding evaluation in authentic user behavior.


**4.2** **QA Taxonomy**


**Track 1:** **Understanding.** Given _N_ trajectories from one user,
recover that user’s behavioral profile. _Attribute_ _Recognition_

**Figure 4** **FileGramQA distribution.** 4.6K questions

(326 MCQs, 3-choice): identify the L/M/R tier on a specified

by track (inner) and sub-task (outer).

behavioral dimension or infer semantic attributes (role, tone,
language); _Behavioral_ _Fingerprint_ (560 MCQs, 4-choice):
given a single anonymous trajectory, match it to one of four
candidate profiles; _Profile_ _Reconstruction_ (free-form): produce a structured assessment across all six behavioral
dimensions through 19 user attributes.


**Track 2:** **Reasoning.** Pattern-level inference and disentanglement under ambiguity. _Behavioral_ _Inference_ (560
MCQs, 4-choice): given 31 trajectories with one task held out, predict behavior on the unseen task; _Trace_
_Disentanglement_ (1,134 MCQs, 2–4 choices): given interleaved event streams from two users on the same task,
identify the primary behavioral difference.


**Track 3:** **Detection.** Per-session memory under behavioral drift. Using the perturbation design from Section 3.1,
5 of 32 trajectories per profile shift one dimension by one tier. _Anomaly_ _Detection_ (815 MCQs, 5–6 choices):
given trajectories mixed with one impostor from a similar profile, identify the impostor session; _Shift_ _Analysis_
(288 MCQs, 3–6 choices): given baseline and one perturbed trajectory, identify which dimension shifted and
in which direction.


6


|T2: REASONING|Col2|Col3|Col4|
|---|---|---|---|
|Behavioral Inference<br>Which behavioral prediction is most<br>consistent with how user would<br>approach an iterate task (T-19) ?<br>Trajectories (T-01 … T-<br>32) with T-19 held out<br>(A) Search -> single pass...<br>(B) Search -> moderate edits...<br>(C)✓Quick scan -> structured<br>details -> nested dir...<br>Gap|Behavioral Inference<br>Which behavioral prediction is most<br>consistent with how user would<br>approach an iterate task (T-19) ?<br>Trajectories (T-01 … T-<br>32) with T-19 held out<br>(A) Search -> single pass...<br>(B) Search -> moderate edits...<br>(C)✓Quick scan -> structured<br>details -> nested dir...<br>Gap|Trace Disentanglement<br>Interleaved event streams from<br>User A and B on the same task:<br>User A x T-05⊕User B x T-05<br>Two users performed the same<br>task. What is the primary<br>behavioral difference?<br>(A) Diff language, not behavior...<br>(B) No significant difference...<br>(C)✓One scans files broadly<br>while the other search-first...|Trace Disentanglement<br>Interleaved event streams from<br>User A and B on the same task:<br>User A x T-05⊕User B x T-05<br>Two users performed the same<br>task. What is the primary<br>behavioral difference?<br>(A) Diff language, not behavior...<br>(B) No significant difference...<br>(C)✓One scans files broadly<br>while the other search-first...|
|Behavioral Inference<br>Which behavioral prediction is most<br>consistent with how user would<br>approach an iterate task (T-19) ?<br>Trajectories (T-01 … T-<br>32) with T-19 held out<br>(A) Search -> single pass...<br>(B) Search -> moderate edits...<br>(C)✓Quick scan -> structured<br>details -> nested dir...<br>Gap|(A) Search -> single pass...<br>(B) Search -> moderate edits...<br>(C)✓Quick scan -> structured<br>details -> nested dir...|(A) Search -> single pass...<br>(B) Search -> moderate edits...<br>(C)✓Quick scan -> structured<br>details -> nested dir...|<br>(B) No significant difference...<br>(C)✓One scans files broadly<br>while the other search-first...|
































|T1: UNDERSTANDING|Col2|Col3|
|---|---|---|
|trace<br>Based on the behavioral<br>trajectories provided,<br>which description best<br>matches this user’s<br>Consumption Pattern?<br>x32<br>32 Trajectories<br>(T-01 … T-32)<br>From User X<br>(A) Breadth-first<br>scanner...<br>(B) Sequential deep<br>reader...<br>(C)✓Targeted<br>searcher...<br>Attribute Recognition|Behavioral Fingerprint<br>Single trace<br>T-14<br>Single<br>Trajectory<br>From<br>Anonymous User<br>Which user profile<br>description best<br>matches the<br>observed behavior?<br>(A) search -> targeted<br>-> deep dirs...<br>(B)✓read -> multi-<br>level -> deeply nested<br>(C) search -> nested<br>dirs…|Profile Reconstruction<br>trace<br>x32<br>32<br>Trajectories<br>(T-01 … T-32)<br>From User X<br>Write a comprehensive<br>profile of this user<br>covering 6 dimensions:<br>(reference provided)<br>‘User A’<br>✓Sequential deep<br>reader (T-01, T-03)<br>✓Detailed output (T-<br>05),<br>✓Nested dirs (T-07)…<br>Likert scale:|




























|T3: DETECTION|Col2|
|---|---|
|Anomaly Detection<br>User A x {T-03, T-14, T-22,<br>T-23, T-27}; User B x T-14<br>Six trajectories, five are<br>from the same user, one is<br>animpostor. What is it?<br>(A) Film & Animation (T-22)<br>(B)✓Version Mgmt. (T-14)<br>(C) Photo & Album (T-23)<br>(D) Student Portfolio (T-27)|Shift Analysis<br>User 1 x {T-08, T-10, T-25,<br>T-30, T-22, T-26 (pert.)}<br>Which character best analyze<br>the behavioral change?<br>(A) Text -> Visuals<br>(B) Passive -> Cleanup<br>(C) Flat -> Deep dirs.<br>(D)✓Scan -> Targeted|



**Figure 5** **QA examples from FileGramBench.** Representative questions from the four tracks, including both MCQ and
open-ended formats.


**Track 4:** **Multimodal Grounding.** Extend evaluation to vision-centric setting with rendered documents and
real-world screen recordings. _File_ _Grounding_ (550 MCQs): answer the same behavioral questions as Tracks 1–3,
but with file outputs presented as rendered PDFs and images instead of raw text; _Visual_ _Grounding_ (100,
free-form, real-world): given the first half of a real participant’s screen recording, predict subsequent file
operations and behavioral patterns.


**Channel-wise Grouping.** We map each sub-task to one of three channels: _procedural_ for operation-level patterns,
_semantic_ for content-level understanding, and _episodic_ for temporal consistency and drift detection across
session.


**4.3** **Evaluation Protocol**


**Two-stage pipeline and leakage control.** (1) **Ingest** : each method processes raw trajectories (atomic actions +
content deltas) using its own memory pipeline. Methods requiring an LLM during ingestion use the same
backbone (Gemini 2.5-Flash (Comanici et al., 2025)), isolating memory design as the independent variable.
(2) **Answer** : Gemini 2.5-Flash answers MCQs using only the retrieved memory. To prevent leakage, models
never access ground-truth profiles, dimension definitions, or perturbation tags; ingestion is restricted to raw
trajectories and content deltas.

#### **5 FileGramOS: Bottom-Up Memory Framework**


FileGramOS is a bottom-up, action-aware memory framework designed for file-centric user behavior. Rather
than prematurely summarizing trajectories into free-form narratives, it builds structured memory from raw
event traces through three stages: per-trajectory encoding that processes distinct behavioral and semantic
streams into an atomic _Engram_, cross-engram consolidation that routes these units into three specialized
memory channels, and a lightweight retrieval stage that composes answers from the consolidated clues. Figure 6
summarizes the overall pipeline.


**5.1** **Stage 1:** **Per-Trajectory Encoding**


The first stage transforms raw, noisy inputs (action sequences and file content/diffs) into a structured atomic
memory unit called an **Engram** . While a raw trajectory is simply a chronological event sequence, an Engram
distills it into a compact, multi-faceted representation that jointly captures procedural statistics, semantic
content, and episodic structure. To capture the multifaceted nature of user behavior, the data flows through
three parallel extraction pipelines:


**Procedural Extraction.** This pipeline isolates the mechanics of user actions. It begins with _Action_ _Counting_
(e.g., tracking reads, edits, writes), followed by _Computation_ to derive higher-level metrics such as browse


7


|File Ingestion<br>…<br>Chunk 1 Chunk 2 Chunk n<br>Embedding<br>Text Embeddings|Col2|Col3|
|---|---|---|
|Text Embed<br>|Text Embed<br>|Style: <summary><br>|
|Text Embed<br>|Text Embed<br>|Detail: <summary>|
|Text Embed<br>|||















**Figure 6** **FileGramOS architecture.** Three-stage pipeline: (1) per-trajectory encoding of traces via parallel extraction
streams into an Engram; (2) cross-engram consolidation routing data into procedural, semantic, and episodic channels,
including an LLM verifier for _variation_ _vs._ _outlier_ ; and (3) query-adaptive retrieval.


ratios and average output lengths. Finally, _Vectorization_ compresses over 50 behavioral features into a dense
17-dimensional fingerprint **f** _j_ _∈_ R [17] .


**Semantic Parsing.** This stream extracts meaning from the content itself. Multimodal file snapshots (documents,
videos) and edit diffs are passed through a vision-language model to generate structural captions and a
behavioral descriptor that summarizes the user’s style, formatting preferences, and detail level.


**Action Merge.** Simultaneously, the raw event timeline undergoes boundary detection to segment continuous
traces into discrete, logical episodes (e.g., “Document survey” _→_ “Report creation”).


These three streams converge to instantiate an _Engram_ for a specific profile and task. Each Engram explicitly
stores a **Procedural Unit** (the vectorized fingerprint), a **Semantic Unit** (file metadata and behavioral descriptor),
and an **Episodic Unit** (segmented trace episodes).


**5.2** **Stage 2:** **Cross-Engram Consolidation**


Once _N_ Engrams are generated across multiple sessions, the **Engram Consolidator** unpacks and routes their
components into a unified **MemoryStore** divided into three complementary channels:


**Procedural Channel.** This channel establishes stable behavioral traits by aggregating the 17-D fingerprints
( **f** 1 _. . ._ **f** _N_ ) from the Engrams’ Procedural Units. It computes cross-trace statistics (mean, median, standard
deviation, min, max) for each feature. These aggregated statistics form stable _Procedural_ _Clues_, allowing the
system to confidently categorize behaviors like “Deeply nested organization” or “Incremental iteration.”


**Semantic Channel.** Taking the behavioral descriptors and file metadata from the Semantic Units, this channel
handles content ingestion and embedding. Text data is divided into chunks and embedded to group similar
content. An LLM then performs a cross-session summary, merging distinct styles and detail preferences into
unified _Semantic_ _Clues_ .


8


**Episodic Channel.** This channel maintains temporal fidelity and detects behavioral drift using the Episodic
Units. Trajectories are clustered into behavioral modes based on sequence similarity. To detect anomalies,
session fingerprints are z-score normalized and evaluated by their distance to the cluster centroid:

_zk_ [(] _[j]_ [)] = _[f]_ _k_ [ (] _σ_ _[j]_ _k_ [)] + _− ϵµk_ _[,]_ _δj_ = _∥_ **z** _j_ _−_ **z** ¯ _∥_ 2 _,_ _y_ ˆ _j_ = I[ _δj_ _> µδ_ + _τσδ_ ] _,_ (1)


with _τ_ =1 _._ 5. Since numeric outliers in file-centric tasks are often intentional, flagged sessions are passed to an
LLM-based **Anomaly Judge** :


_rj_ = LLM( _ψj_ ) _∈{_ variation _,_ outlier _,_ uncertain _}._ (2)


This explicitly disambiguates task-dependent _variations_ from genuine behavioral _shifts_, outputting contextual
_Episodic_ _Clues_ .


**5.3** **Stage 3:** **Query-Adaptive Retrieval**


By maintaining three distinct channels, FileGramOS defers the final interpretation of the memory until
query time. Given a user query, the system performs **Keyword Extraction** to identify the target dimension,
e.g., “File Organization”. It then adaptively retrieves the pre-computed clues from the MemoryStore—pulling
structural habits from the Procedural Clues, stylistic preferences from Semantic Clues, and flagged deviations
from Episodic Clues—and routes them to a final LLM generation step to compose a grounded, evidence-backed
answer.

#### **6 Experiments**


**6.1** **Setup**


**Data and Input.** We evaluate 640 trajectories from FileGramEngine under three settings. The _Text_ setting
uses original Markdown agent outputs. The _Multimodal_ setting renders outputs as PDFs and images. The
_Real-World_ setting replaces simulated traces with human screen recordings. Behavioral event logs remain
identical across the first two settings, and we utilize Gemini 2.5-Flash as the shared video captioner across the
three settings.


**Methods.** We evaluate FileGramOS against 12 methods using Gemini 2.5-Flash (Comanici et al., 2025)
as the shared QA backbone. The baselines fall into three distinct groups: (1) context methods including
Full Context, Naive RAG, and VisRAG (Yu et al., 2025), (2) text interaction memory methods spanning
Mem0 (Chhikara et al., 2025), Zep (Rasmussen et al., 2025), MemOS (Li et al., 2025), EverMemOS (Hu et al.,
2026), and SimpleMem (Liu et al., 2026), and (3) multimodal memory methods featuring MMA (Lu et al.,
2026) and MemU (NevaMind-AI, 2025).


**6.2** **Results Analysis**


**Bottom-up Structure Surpasses Narrative Summarization.** Among memory-targeted methods, FileGramOS
scores 59.6%, significantly outperforming the strongest narrative baseline EverMemOS at 49.9%. The core
advantage lies in abstraction timing. Narrative-first methods like Mem0, Zep, MemOS, SimpleMem, and
EverMemOS summarize trajectories during ingestion. This prematurely erases key behavioral discriminators
like action counts, directory depth, and edit granularity. The result is systematic flattening where distinct
profiles receive identical generic descriptors, like “structured”, “methodical”, and “comprehensive”, despite
differing operations. In contrast, as shown in Figure 7, FileGramOS prevents this by preserving distributional
statistics at ingest time and deferring semantic abstraction until query time.


**Track and Channel Overview.** Track 1 and 2 are partially solvable, while Track 3 exposes a clear detection-vsexplanation gap. Specifically, (1) AnomDet evaluates cross-session summarization: methods that aggregate
behavioral norms across trajectories, such as EverMemOS and FileGramOS, achieve over 70% accuracy,
whereas flat memory systems like Mem0 and SimpleMem remain near random at 21–26%; (2) ShiftAna


9


**Table 3** **Main results on FileGramBench.** All scores are accuracy (%) scaled 0–100. _[†]_ Open-ended sub-tasks are scored by
LLM judge (Likert 1–5, rescaled). _[‡]_ Multimodal memory with native non-text ingestion. Sub-task and token definitions
are detailed below the table.













|Tokens T1: Understanding T2: Reasoning T3: Detection T4: MM Channel<br>Method Avg<br>Attr Behav Prof Behav Trace Anom Shift File Vis<br>In. Out. Proc Sem Epi<br>Rec FP Rec† Inf Dis Det Ana Grd Grd†|Tokens|Col3|Col4|Col5|Col6|Channel|Col8|
|---|---|---|---|---|---|---|---|
|**Method**<br>**Tokens**<br>**T1: Understanding T2: Reasoning T3: Detection**<br>**T4: MM**<br>**Channel**<br>**Avg**<br>**In.**<br>**Out.**<br>**Attr**<br>**Rec**<br>**Behav**<br>**FP**<br>**Prof**<br>**Rec**_†_<br>**Behav**<br>**Inf**<br>**Trace**<br>**Dis**<br>**Anom**<br>**Det**<br>**Shift**<br>**Ana**<br>**File**<br>**Grd**<br>**Vis**<br>**Grd**_†_ **Proc Sem**<br>**Epi**|**In.**<br>**Out.**|**In.**<br>**Out.**|**In.**<br>**Out.**|**In.**<br>**Out.**|**In.**<br>**Out.**|**Proc Sem**<br>**Epi**|**Proc Sem**<br>**Epi**|
|No Context|—<br>—|36.2<br>25.7<br>–|17.4<br>36.9|19.0<br>20.5|23.8<br>–|25.7 38.2 19.7|25.4|
|Full Context<br>Naive RAG<br>Eager Summ.<br>VisRAG (Yu et al., 2025)_‡_|625.2K 45.9K <br>625.2K<br>3.9K <br>625.2K<br>3.7K <br>609.8K 10.0K|40.5<br>31.1<br>50.0<br> 48.2<br>27.7<br>46.8<br> 45.1<br>29.6<br>55.6<br> **53.4**<br>33.2<br>56.3|30.6<br>80.5<br>26.4<br>64.1<br>39.3<br>65.9<br>32.9<br>72.8|36.8<br>37.8<br>38.4<br>20.1<br>59.7<br>36.1<br>64.5<br>35.4|42.5<br>7.0<br>35.1<br>5.5<br>44.0<br>6.5<br>45.3<br>7.0|50.7 43.0 37.3 <br>42.0 49.3 29.7 <br>49.8 49.3 48.4 <br>51.2 **55.2** 54.7|48.0<br> 40.5<br> 49.5<br> 51.9|
|Full Context<br>Naive RAG<br>Eager Summ.<br>VisRAG (Yu et al., 2025)_‡_|625.2K 45.9K <br>625.2K<br>3.9K <br>625.2K<br>3.7K <br>609.8K 10.0K|40.5<br>31.1<br>50.0<br> 48.2<br>27.7<br>46.8<br> 45.1<br>29.6<br>55.6<br> **53.4**<br>33.2<br>56.3|30.6<br>80.5<br>26.4<br>64.1<br>39.3<br>65.9<br>32.9<br>72.8|36.8<br>37.8<br>38.4<br>20.1<br>59.7<br>36.1<br>64.5<br>35.4|42.5<br>7.0<br>35.1<br>5.5<br>44.0<br>6.5<br>45.3<br>7.0|50.7 43.0 37.3 <br>42.0 49.3 29.7 <br>49.8 49.3 48.4 <br>51.2 **55.2** 54.7||
|Mem0 (Chhikara et al., 2025)<br>Zep (Rasmussen et al., 2025)<br>MemOS (Li et al., 2025)<br>SimpleMem (Liu et al., 2026)<br>EverMemOS (Hu et al., 2026) <br>MemU (NevaMind-AI, 2025)_‡_<br>MMA (Lu et al., 2026)_‡_|119.9K<br>3.0K <br>219.1K<br>3.8K <br>302.3K<br>4.2K <br>9.3K<br>3.5K <br> 1098.9K 8.4K <br>293.6K<br>7.9K <br>331.8K<br>4.5K|44.2<br>26.4<br>48.1<br> 43.6<br>28.4<br>50.4<br> 44.2<br>24.8<br>52.0<br> 43.6<br>20.2<br>56.6<br> 48.8<br>30.2<br>**57.7**<br> 47.9<br>27.3<br>50.4<br> 51.2<br>29.8<br>51.8|21.4<br>50.4<br>27.4<br>61.0<br>23.0<br>57.3<br>28.2<br>47.5<br>39.3<br>62.2<br>30.4<br>65.7<br>28.9<br>57.4|23.8<br>28.5<br>37.5<br>28.1<br>26.3<br>28.1<br>21.8<br>28.5<br>**71.4**<br>**38.9**<br>46.0<br>33.0<br>57.5<br>32.6|29.5<br>4.0<br>35.4<br>5.0<br>32.0<br>4.5<br>29.0<br>4.5<br>44.5<br>7.5<br>39.8<br>6.0<br>41.3<br>5.5|33.4 47.8 26.0 <br>41.3 44.6 33.0 <br>37.2 47.2 27.2 <br>33.3 47.2 26.2 <br>48.7 50.8 55.9 <br>44.9 49.3 39.8 <br>42.8 51.6 53.1|33.2<br> 40.2<br> 36.2<br> 32.9<br> 49.9<br> 44.4<br> 44.7|
|FileGramOS|109.7K<br>4.3K|50.6<br>**35.2**<br>54.2|**42.1**<br>**80.9**|70.2<br>37.8|**55.8**<br>**8.5**|**60.1** 54.6 **58.9 **|**59.6**|


_T1_ - **AttrRec** : Attribute Recognition (326, 3-choice); **BehavFP** : Behavioral Fingerprint (560, 4-choice); **ProfRec** : Profile Reconstruction (320, free-form).
_T2_ - **BehavInf** : Behavioral Inference (560, 4-choice); **TraceDis** : Trace Disentanglement (1,134, 2–4 choices).
_T3_ - **AnomDet** : Anomaly Detection (815, 5–6 choices); **ShiftAna** : Shift Analysis (288, 3–6 choices).
_T4_ - **FileGrd** : File Grounding (550, mixed); **VisGrd** : Visual Grounding (100, free-form). Text methods use a shared text parser; VisRAG and _[‡]_ methods use
native multimodal input.

_Channel_ - **Proc** : procedural; **Sem** : semantic; **Epi** : episodic. _Tokens_ - **In.** : total stored memory per profile (avg. over 20 profiles); **Out.** : retrieved context per
query (avg.).


examines trace perturbations along a single behavioral dimension entangled with normal cross-task variance.
While existing models can detect overall deviations, they fail to attribute these changes to specific dimensions
or directions. In contrast, FileGramOS surpasses baselines by leveraging channel-wise procedural cues, while
the semantic track remains more competitive: VisRAG and EverMemOS rival FileGramOS by effectively
capturing formatting and content information. These results demonstrate that fine-grained operational
micro-structure serves as the decisive signal for file-system personalization, whereas semantic understanding
can often be approximated through conventional retrieval or summarization strategies.


**Context Baselines vs. Memory-targeted Methods.** The naive Full Context approach outperforms dedicated
memory pipelines by simply concatenating raw events. This strategy proves that preserving complete evidence
occasionally outweighs semantic abstraction. The TraceDis task clearly demonstrates this advantage, as Full
Context achieves a score similar to FileGramOS by directly comparing complete action chains. Meanwhile,
narrative methods fall far behind because their summaries discard critical sequential diversity signals. However,
raw concatenation fails on tasks demanding cross-session comparison. Full Context drops significantly below
FileGramOS in these scenarios, because detecting outliers across 32 trajectories strictly requires structured
aggregation. Beyond text methods, vision-augmented retrieval provides a distinct alternative. VisRAG
dominates the Semantic channel by leveraging page-image retrieval to capture layout cues. However, it still
lacks the behavioral abstraction required for procedural tasks, causing a substantial performance drop in
those areas.


**Multimodal Memory Methods.** Multimodal memory systems like MMA and MemU fail to outperform the
strongest text-only baselines. While mechanisms like confidence-scored retrieval and VLM captioning assist
with specific anomaly detection tasks or non-text ingestion, they do not yield stronger overall behavioral
discrimination. FileGramOS surpasses these methods by a wide margin, proving that simply handling
multimodal inputs is insufficient. The critical factor remains how behavioral evidence is structured and
preserved. Furthermore, rendered page images are inherently blind to operation-level statistics such as file
counts, output lengths, and edit frequencies, as well as file-system structures like directory depth and naming
conventions. This limitation causes all vision-based methods to fail on these dimensions even when they


10


CASE A: Procedural Case B: Multimodal





**（** 1 **）** Need comparing
multimodal artifacts



T-01 : Two users performed the same task ...
Which pair best describes how the two users differ?



A . reading strategy (sequential vs targeted)... output
detail (comprehensive vs minimal)...

✓ B.C. ...output detail (comprehensive vs minimalorganization (nested vs flat)...

D. reading strategy (sequential vs targeted).



✓ B.C.









**（** 3 **）** Cross-event
reasoning



**（** 2 **）** Cross-Format Output
Gap



























































**Figure** **7** **Qualitative** **comparison.** _Left:_ A BehavFP question where FileGramOS’s three-channel architecture—
procedural statistics, semantic narration, and episodic clustering—jointly recover the correct profile, while baselines
each miss different signals. _Right:_ A TraceDis question involving multimodal artifacts, where cross-format output gaps
and parsing losses cause widespread failures.


succeed on formatting cues, as illustrated in Figure 7.


**Multimodal and real-world gap.** When transitioning to the Multimodal setting where outputs become PDFs
or images, text-only methods fall toward baseline levels. While MemU mitigates this decline through
VLM captioning, FileGramOS demonstrates the highest resilience because its procedural channel relies on
modality-invariant event logs. Moving to the Real-World setting widens this performance gap even further.
Specifically, accuracy on human screen recordings drops to single digits across all evaluated methods. This
sharp decline reveals a substantial distance between structured trace analysis and actual video-level behavioral
understanding. The primary reason for this struggle is that simulated trajectories provide clean action logs,
whereas real-world recordings introduce noise, variable pacing, and unstructured visual input. Consequently,
this unexplored sim-to-real gap alongside persistent difficulties in shift attribution and open-ended profile
reconstruction defines concrete research frontiers for future memory-centric personalized systems.

#### **7 Conclusion**


In this paper, we present the unified FileGram framework, encompassing FileGramEngine for trajectory
generation, FileGramBench for diagnostic evaluation, and FileGramOS as a bottom-up reference method,
to make file-system behavioral personalization measurable and reproducible. Using this framework, we
conduct extensive evaluations, highlighting significant challenges within this domain. Shared workspace
content provides weak personalization signals compared to operation-level traces, meaning early narrative
summarization inadvertently flattens distinct user behaviors. Furthermore, shift attribution remains a critical
bottleneck because systems can easily detect anomalies but consistently fail to explain the exact nature and
direction of those behavioral changes. Together, we hope the framework, along with the exposed challenges,
will pave the way for developing personalized memory-centric file-system agents.


11


#### **References**

Anthropic. System Card: Claude Haiku 4.5. [https://www-cdn.anthropic.com/](https://www-cdn.anthropic.com/7aad69bf12627d42234e01ee7c36305dc2f6a970.pdf)
[7aad69bf12627d42234e01ee7c36305dc2f6a970.pdf,](https://www-cdn.anthropic.com/7aad69bf12627d42234e01ee7c36305dc2f6a970.pdf) October 2025. Accessed 2026.


Yuanchen Bei, Tianxin Wei, Xuying Ning, Yanjun Zhao, Zhining Liu, Xiao Lin, Yada Zhu, Hendrik Hamann, Jingrui
He, and Hanghang Tong. Mem-gallery: Benchmarking multimodal long-term conversational memory for mllm
agents. _arXiv_ _preprint_ _arXiv:2601.03515_, 2026.


Prateek Chhikara, Dev Khant, Saket Aryan, Taranjeet Singh, and Deshraj Yadav. Mem0: Building production-ready
ai agents with scalable long-term memory. _arXiv_ _preprint_ _arXiv:2504.19413_, 2025.


Gheorghe Comanici, Eric Bieber, Mike Schaekermann, Ice Pasupat, Noveen Sachdeva, Inderjit Dhillon, Marcel Blistein,
Ori Ram, Dan Zhang, Evan Rosen, et al. Gemini 2.5: Pushing the frontier with advanced reasoning, multimodality,
long context, and next generation agentic capabilities. _arXiv_ _preprint_ _arXiv:2507.06261_, 2025.


Xiang Deng, Yu Gu, Boyuan Zheng, Shijie Chen, Sam Stevens, Boshi Wang, Huan Sun, and Yu Su. Mind2web:
Towards a generalist agent for the web. _Advances_ _in_ _Neural_ _Information_ _Processing_ _Systems_, 36:28091–28114, 2023.


Darshan Deshpande, Varun Gangal, Hersh Mehta, Anand Kannappan, Rebecca Qian, and Peng Wang. Memtrack:
Evaluating long-term memory and state tracking in multi-platform dynamic agent environments. _arXiv_ _preprint_
_arXiv:2510.01353_, 2025.


Runnan Fang, Yuan Liang, Xiaobin Wang, Jialong Wu, Shuofei Qiao, Pengjun Xie, Fei Huang, Huajun Chen, and
Ningyu Zhang. Memp: Exploring agent procedural memory. _arXiv_ _preprint_ _arXiv:2508.06433_, 2025.


Ge Gao, Alexey Taymanov, Eduardo Salinas, Paul Mineiro, and Dipendra Misra. Aligning llm agents by learning
latent preference from user edits, 2024. [https://arxiv.org/abs/2404.15269.](https://arxiv.org/abs/2404.15269)


Bernal Jiménez Gutiérrez, Yiheng Shu, Yu Gu, Michihiro Yasunaga, and Yu Su. Hipporag: Neurobiologically inspired
long-term memory for large language models, 2025. [https://arxiv.org/abs/2405.14831.](https://arxiv.org/abs/2405.14831)


Siwei Han, Peng Xia, Ruiyi Zhang, Tong Sun, Yun Li, Hongtu Zhu, and Huaxiu Yao. Mdocagent: A multi-modal
multi-agent framework for document understanding, 2025. [https://arxiv.org/abs/2503.13964.](https://arxiv.org/abs/2503.13964)


Zexue He, Yu Wang, Churan Zhi, Yuanzhe Hu, Tzu-Ping Chen, Lang Yin, Ze Chen, Tong Arthur Wu, Siru Ouyang,
Zihan Wang, et al. Memoryarena: Benchmarking agent memory in interdependent multi-session agentic tasks. _arXiv_
_preprint_ _arXiv:2602.16313_, 2026.


Chuanrui Hu, Xingze Gao, Zuyi Zhou, Dannong Xu, Yi Bai, Xintong Li, Hui Zhang, Tong Li, Chong Zhang, Lidong
Bing, et al. Evermemos: A self-organizing memory operating system for structured long-horizon reasoning. _arXiv_
_preprint_ _arXiv:2601.02163_, 2026.


Yuanzhe Hu, Yu Wang, and Julian McAuley. Evaluating memory in llm agents via incremental multi-turn interactions.
_arXiv_ _preprint_ _arXiv:2507.05257_, 2025.


Bingrui Jin, Kunyao Lan, and Mengyue Wu. Twice: An llm agent framework for simulating personalized user tweeting
behavior with long-term temporal features. _arXiv_ _preprint_ _arXiv:2602.22222_, 2025.


David R Krathwohl. A revision of bloom’s taxonomy: An overview. _Theory_ _into_ _practice_, 41(4):212–218, 2002.


Patrick Lewis, Ethan Perez, Aleksandra Piktus, Fabio Petroni, Vladimir Karpukhin, Naman Goyal, Heinrich Küttler,
Mike Lewis, Wen-tau Yih, Tim Rocktäschel, et al. Retrieval-augmented generation for knowledge-intensive nlp tasks.
_Advances_ _in_ _neural_ _information_ _processing_ _systems_, 33:9459–9474, 2020.


Keyu Li, Junhao Shi, Yang Xiao, Mohan Jiang, Jie Sun, Yunze Wu, Shijie Xia, Xiaojie Cai, Tianze Xu, Weiye Si, et al.
Agencybench: Benchmarking the frontiers of autonomous agents in 1m-token real-world contexts. _arXiv_ _preprint_
_arXiv:2601.11044_, 2026.


Zhiyu Li, Chenyang Xi, Chunyu Li, Ding Chen, Boyu Chen, Shichao Song, Simin Niu, Hanyu Wang, Jiawei Yang,
Chen Tang, et al. Memos: A memory os for ai system. _arXiv_ _preprint_ _arXiv:2507.03724_, 2025.


Yueqian Lin, Qinsi Wang, Hancheng Ye, Yuzhe Fu, Hai Li, Yiran Chen, et al. Hippomm: Hippocampal-inspired
multimodal memory for long audiovisual event understanding. _arXiv_ _preprint_ _arXiv:2504.10739_, 2025.


Jiaqi Liu, Yaofeng Su, Peng Xia, Siwei Han, Zeyu Zheng, Cihang Xie, Mingyu Ding, and Huaxiu Yao. Simplemem:
Efficient lifelong memory for llm agents. _arXiv_ _preprint_ _arXiv:2601.02553_, 2026.


12


Ziyu Liu, Tao Chu, Yuhang Zang, Xilin Wei, Xiaoyi Dong, Pan Zhang, Zijian Liang, Yuanjun Xiong, Yu Qiao, Dahua
Lin, et al. Mmdu: A multi-turn multi-image dialog understanding benchmark and instruction-tuning dataset for
lvlms. _Advances_ _in_ _Neural_ _Information_ _Processing_ _Systems_, 37:8698–8733, 2024.


Lin Long, Yichen He, Wentao Ye, Yiyuan Pan, Yuan Lin, Hang Li, Junbo Zhao, and Wei Li. Seeing, listening,
remembering, and reasoning: A multimodal agent with long-term memory. _arXiv_ _preprint_ _arXiv:2508.09736_, 2025.


Yihao Lu, Wanru Cheng, Zeyu Zhang, and Hao Tang. Mma: Multimodal memory agent. _arXiv_ _preprint_
_arXiv:2602.16493_, 2026.


Yubo Ma, Yuhang Zang, Liangyu Chen, Meiqi Chen, Yizhu Jiao, Xinze Li, Xinyuan Lu, Ziyu Liu, Yan Ma, Xiaoyi
Dong, Pan Zhang, Liangming Pan, Yu-Gang Jiang, Jiaqi Wang, Yixin Cao, and Aixin Sun. Mmlongbench-doc:
Benchmarking long-context document understanding with visualizations, 2024. [https://arxiv.org/abs/2407.01523.](https://arxiv.org/abs/2407.01523)


Adyasha Maharana, Dong-Ho Lee, Sergey Tulyakov, Mohit Bansal, Francesco Barbieri, and Yuwei Fang. Evaluating
very long-term conversational memory of llm agents. In _Proceedings_ _of_ _the_ _62nd_ _Annual_ _Meeting_ _of_ _the_ _Association_
_for_ _Computational_ _Linguistics_ _(Volume_ _1:_ _Long_ _Papers)_, pages 13851–13870, 2024.


Minesh Mathew, Dimosthenis Karatzas, and C. V. Jawahar. Docvqa: A dataset for vqa on document images, 2021.

[https://arxiv.org/abs/2007.00398.](https://arxiv.org/abs/2007.00398)


Grégoire Mialon, Clémentine Fourrier, Thomas Wolf, Yann LeCun, and Thomas Scialom. GAIA: a benchmark for
general AI assistants, 2024. [https://openreview.net/forum?id=fibxvahvs3.](https://openreview.net/forum?id=fibxvahvs3)


Jian Mu, Chaoyun Zhang, Chiming Ni, Lu Wang, Bo Qiao, Kartik Mathur, Qianhui Wu, Yuhang Xie, Xiaojun Ma,
Mengyu Zhou, Si Qin, Liqun Li, Yu Kang, Minghua Ma, Qingwei Lin, Saravan Rajmohan, and Dongmei Zhang. Gui360 _[◦]_ : A comprehensive dataset and benchmark for computer-using agents, 2025. [https://arxiv.org/abs/2511.04307.](https://arxiv.org/abs/2511.04307)


NevaMind-AI. Memu: Memory-augmented understanding. [https://github.com/NevaMind-AI/memU,](https://github.com/NevaMind-AI/memU) 2025. Accessed:
2026-03-05.


Jiao Ou, Junda Lu, Che Liu, Yihong Tang, Fuzheng Zhang, Di Zhang, and Kun Gai. Dialogbench: Evaluating
llms as human-like dialogue systems. In _Proceedings_ _of_ _the_ _2024_ _Conference_ _of_ _the_ _North_ _American_ _Chapter_ _of_
_the_ _Association_ _for_ _Computational_ _Linguistics:_ _Human_ _Language_ _Technologies_ _(Volume_ _1:_ _Long_ _Papers)_, pages
6137–6170, 2024.


Charles Packer, Vivian Fang, Shishir_G Patil, Kevin Lin, Sarah Wooders, and Joseph_E Gonzalez. Memgpt: towards
llms as operating systems. 2023.


Joon Sung Park, Joseph O’Brien, Carrie Jun Cai, Meredith Ringel Morris, Percy Liang, and Michael S Bernstein.
Generative agents: Interactive simulacra of human behavior. In _Proceedings_ _of_ _the_ _36th_ _annual_ _acm_ _symposium_ _on_
_user_ _interface_ _software_ _and_ _technology_, pages 1–22, 2023.


Preston Rasmussen, Pavlo Paliychuk, Travis Beauvais, Jack Ryan, and Daniel Chalef. Zep: a temporal knowledge
graph architecture for agent memory. _arXiv_ _preprint_ _arXiv:2501.13956_, 2025.


Xubin Ren, Lingrui Xu, Long Xia, Shuaiqiang Wang, Dawei Yin, and Chao Huang. Videorag: Retrieval-augmented
generation with extreme long-context videos, 2025. [https://arxiv.org/abs/2502.01549.](https://arxiv.org/abs/2502.01549)


Piaohong Wang, Motong Tian, Jiaxian Li, Yuan Liang, Yuqing Wang, Qianben Chen, Tiannan Wang, Zhicong Lu,
Jiawei Ma, Yuchen Eleanor Jiang, and Wangchunshu Zhou. O-mem: Omni memory system for personalized, long
horizon, self-evolving agents, 2025a. [https://arxiv.org/abs/2511.13593.](https://arxiv.org/abs/2511.13593)


Qiuchen Wang, Shihang Wang, Yu Zeng, Qiang Zhang, Fanrui Zhang, Zhuoning Guo, Bosi Zhang, Wenxuan Huang, Lin
Chen, Zehui Chen, Pengjun Xie, and Ruixue Ding. Vimrag: Navigating massive visual context in retrieval-augmented
generation via multimodal memory graph, 2026. [https://arxiv.org/abs/2602.12735.](https://arxiv.org/abs/2602.12735)


Zilong Wang, Yuedong Cui, Li Zhong, Zimin Zhang, Da Yin, Bill Yuchen Lin, and Jingbo Shang. Officebench:
Benchmarking language agents across multiple applications for office automation. _arXiv_ _preprint_ _arXiv:2407.19056_,
2024.


Ziyi Wang, Yuxuan Lu, Yimeng Zhang, Jing Huang, and Dakuo Wang. Customer-r1: Personalized simulation of
human behaviors via rl-based llm agent in online shopping. _arXiv_ _preprint_ _arXiv:2510.07230_, 2025b.


Tianxin Wei, Noveen Sachdeva, Benjamin Coleman, Zhankui He, Yuanchen Bei, Xuying Ning, Mengting Ai, Yunzhe
Li, Jingrui He, Ed H Chi, et al. Evo-memory: Benchmarking llm agent test-time learning with self-evolving memory.
_arXiv_ _preprint_ _arXiv:2511.20857_, 2025.


13


Siwei Wen, Zhangcheng Wang, Xingjian Zhang, Lei Huang, and Wenjun Wu. Eventmemagent: Hierarchical event-centric
memory for online video understanding with adaptive tool use. _arXiv_ _preprint_ _arXiv:2602.15329_, 2026.


Rebecca Westhäußer, Frederik Berenz, Wolfgang Minker, and Sebastian Zepf. Caim: Development and evaluation of a
cognitive ai memory framework for long-term interaction with intelligent agents, 2025. [https://arxiv.org/abs/2505.](https://arxiv.org/abs/2505.13044)
[13044.](https://arxiv.org/abs/2505.13044)


Di Wu, Hongwei Wang, Wenhao Yu, Yuwei Zhang, Kai-Wei Chang, and Dong Yu. Longmemeval: Benchmarking chat
assistants on long-term interactive memory. _arXiv_ _preprint_ _arXiv:2410.10813_, 2024a.


Zhiyong Wu, Chengcheng Han, Zichen Ding, Zhenmin Weng, Zhoumianze Liu, Shunyu Yao, Tao Yu, and Lingpeng Kong.
Os-copilot: Towards generalist computer agents with self-improvement, 2024b. [https://arxiv.org/abs/2402.07456.](https://arxiv.org/abs/2402.07456)


Tianbao Xie, Danyang Zhang, Jixuan Chen, Xiaochuan Li, Siheng Zhao, Ruisheng Cao, Toh J Hua, Zhoujun Cheng,
Dongchan Shin, Fangyu Lei, et al. Osworld: Benchmarking multimodal agents for open-ended tasks in real computer
environments. _Advances_ _in_ _Neural_ _Information_ _Processing_ _Systems_, 37:52040–52094, 2024.


Wujiang Xu, Zujie Liang, Kai Mei, Hang Gao, Juntao Tan, and Yongfeng Zhang. A-mem: Agentic memory for llm
agents. _arXiv_ _preprint_ _arXiv:2502.12110_, 2025.


Xinchao Xu, Zhibin Gou, Wenquan Wu, Zheng-Yu Niu, Hua Wu, Haifeng Wang, and Shihang Wang. Long time no
see! open-domain conversation with long-term persona memory. In _Findings_ _of_ _the_ _Association_ _for_ _Computational_
_Linguistics:_ _ACL_ _2022_, pages 2639–2650, 2022.


Haochen Xue, Feilong Tang, Ming Hu, Yexin Liu, Qidong Huang, Yulong Li, Chengzhi Liu, Zhongxing Xu, Chong
Zhang, Chun-Mei Feng, et al. Mmrc: A large-scale benchmark for understanding multimodal large language model in
real-world conversation. In _Proceedings_ _of_ _the_ _63rd_ _Annual_ _Meeting_ _of_ _the_ _Association_ _for_ _Computational_ _Linguistics_
_(Volume_ _1:_ _Long_ _Papers)_, pages 22477–22503, 2025.


Zhe Yang, Shulin Tian, Kairui Hu, Shuai Liu, Hoang-Nhat Nguyen, Yichi Zhang, Zujin Guo, Mengying Yu, Zinan
Zhang, Jingkang Yang, Chen Change Loy, and Ziwei Liu. Hippocamp: Benchmarking contextual agents on personal
computers, 2026.


Shunyu Yao, Jeffrey Zhao, Dian Yu, Nan Du, Izhak Shafran, Karthik R Narasimhan, and Yuan Cao. React: Synergizing
reasoning and acting in language models. In _The_ _eleventh_ _international_ _conference_ _on_ _learning_ _representations_, 2022.


Shi Yu, Chaoyue Tang, Bokai Xu, Junbo Cui, Junhao Ran, Yukun Yan, Zhenghao Liu, Shuo Wang, Xu Han, Zhiyuan
Liu, and Maosong Sun. Visrag: Vision-based retrieval-augmented generation on multi-modality documents, 2025.
[https://arxiv.org/abs/2410.10594.](https://arxiv.org/abs/2410.10594)


Aohan Zeng, Mingdao Liu, Rui Lu, Bowen Wang, Xiao Liu, Yuxiao Dong, and Jie Tang. Agenttuning: Enabling
generalized agent abilities for llms. In _Findings_ _of_ _the_ _Association_ _for_ _Computational_ _Linguistics:_ _ACL_ _2024_, pages
3053–3077, 2024.


Yujie Zhao, Boqin Yuan, Junbo Huang, Haocheng Yuan, Zhongming Yu, Haozhou Xu, Lanxiang Hu, Abhilash
Shankarampeta, Zimeng Huang, Wentao Ni, et al. Ama-bench: Evaluating long-horizon memory for agentic
applications. _arXiv_ _preprint_ _arXiv:2602.22769_, 2026.


Wanjun Zhong, Lianghong Guo, Qiqi Gao, He Ye, and Yanlin Wang. Memorybank: Enhancing large language
models with long-term memory. In _Proceedings_ _of_ _the_ _AAAI_ _conference_ _on_ _artificial_ _intelligence_, volume 38, pages
19724–19731, 2024.


Shuyan Zhou, Frank F. Xu, Hao Zhu, Xuhui Zhou, Robert Lo, Abishek Sridhar, Xianyi Cheng, Tianyue Ou, Yonatan
Bisk, Daniel Fried, Uri Alon, and Graham Neubig. Webarena: A realistic web environment for building autonomous
agents, 2024. [https://arxiv.org/abs/2307.13854.](https://arxiv.org/abs/2307.13854)


14


## **Appendix**

This supplementary material is organized into five parts. Section A extends the related work. Section B details
the FileGramOS architecture and pipeline. Section C describes benchmark construction and data. Section D
presents extended experiments and analysis. Section E addresses deployment, ethics, and reproducibility.

#### **A Extended Related Work**


**A.1** **Memory Framework Comparison**


Beyond the benchmark-level comparison in the main paper, we position FileGramOS within the broader
landscape of memory architectures in Table 4.


**Dialogue-based** **and** **flat-store** **systems.** First-generation memory frameworks—MemGPT (Packer et al.,
2023), Mem0 (Chhikara et al., 2025), SimpleMem (Liu et al., 2026)—extract semantic facts from dialogue
and store them in flat or hierarchical key–value stores. While effective for conversational recall, they lack
procedural modeling and cannot ingest non-textual behavioral evidence. Graph-based extensions such as
HippoRAG (Gutiérrez et al., 2025), Zep (Rasmussen et al., 2025), and A-MEM (Xu et al., 2025) introduce
relational structure via knowledge graphs and personalized retrieval, yet remain anchored to dialogue as the
sole input modality.


**Multimodal and video memory.** Recent systems broaden the input space beyond text. MMA (Lu et al., 2026)
and MemU (NevaMind-AI, 2025) incorporate vision-language perception; VideoRAG (Ren et al., 2025),
HippoMM (Lin et al., 2025), M3-Agent (Long et al., 2025), and EventMemAgent (Wen et al., 2026) process
video or audio streams. Among these, only EventMemAgent partially models procedural behavior through
event-level annotations, and none ingests file-system traces.


**Trajectory-aware and hierarchical designs.** MemOS (Li et al., 2025) and EverMemOS (Hu et al., 2026) improve
temporal organization through hierarchical consolidation, while Memp (Fang et al., 2025) is the first to model
procedural memory from agent trajectories—but it covers neither semantic nor episodic channels. Across
all families, no existing system jointly covers procedural, semantic, and episodic channels from file-system
evidence.


**Structured-profile and ontology-driven memory.** CAIM (Westhäußer et al., 2025) organizes user knowledge
through an ontology-driven tagging scheme, mapping each interaction to a domain taxonomy before storage;
this top-down design contrasts with FileGramOS’s bottom-up approach, where behavioral dimensions
emerge from trace statistics rather than a pre-defined ontology. O-Mem (Wang et al., 2025a) introduces a
multi-store persona memory with separate working, short-term, and long-term stores—an architecture that
parallels FileGramOS’s three-channel separation but operates on dialogue turns rather than file-system
actions. More broadly, surveys on agent memory taxonomies advocate distinct procedural, episodic, and
semantic substrates—a classification that directly motivates FileGramOS’s channel design. Knowledge-graph
(KG) based approaches (Rasmussen et al., 2025; Xu et al., 2025) structure memories as entity–relation triples,
enabling traversal-based retrieval; FileGramOS’s procedural channel serves a related role through aggregate
statistics (17-D fingerprints), trading graph flexibility for deterministic reproducibility and higher retrieval
efficiency.

#### **B System Architecture and Implementation**


**B.1** **Behavioral Signal Schema**


Each trajectory is composed of typed _atomic_ _actions_ paired with their corresponding _content_ _deltas_, stored as
a timestamped sequence in events.json. Table 5 catalogues all 22 raw event types: 12 atomic actions retained
after cleaning and 10 simulation metadata types that are stripped (74.3% of all raw events). In addition, three
per-event fields—message_id, model_provider, and model_name—are removed from all retained events,
as they leak which LLM engine generated the trajectory rather than reflecting user behavior.


15


**Table 4** **Memory framework comparison.** FileGramOS is the first system to ingest file-system behavioral traces and
jointly model procedural, semantic, and episodic channels; all prior systems operate on dialogue or video. Src.:
primary input source; MM: multimodal support; Str.: storage structure—Flat, Graph, or Hierarchical; Cons.: temporal
consolidation.


**Memory Channel**
**System** **Src.** **MM** **Str.** **Cons.**

**Proc.** **Sem.** **Epi.**


MemGPT (Packer et al., 2023) Dialogue ✗ Hier. ✗ ✓ _◦_ ✓
Mem0 (Chhikara et al., 2025) Dialogue ✗ Flat/Graph ✗ ✓ ✗ ✓
Zep (Rasmussen et al., 2025) Dialogue ✗ Graph ✗ ✓ ✓ ✓
A-MEM (Xu et al., 2025) Dialogue ✗ Graph ✗ ✓ ✓ ✓
HippoRAG (Gutiérrez et al., 2025) Dialogue ✗ Graph ✗ ✓ ✗ ✓
SimpleMem (Liu et al., 2026) Dialogue ✗ Hier. ✗ ✓ ✓ ✓
MemU (NevaMind-AI, 2025) Multimodal ✓ Hier. ✗ ✓ _◦_ ✗
MMA (Lu et al., 2026) Multimodal ✓ Flat ✗ ✓ _◦_ ✗
VideoRAG (Ren et al., 2025) Video ✓ Graph ✗ ✓ ✓ ✓
VimRAG (Wang et al., 2026) Multimodal ✓ Graph ✗ ✗ ✓ _◦_
HippoMM (Lin et al., 2025) Audio+Video ✓ Hier. ✗ ✓ ✓ ✓
M3-Agent (Long et al., 2025) Audio+Video ✓ Graph ✗ ✓ ✓ ✓
EventMemAgent (Wen et al., 2026) Video ✓ Hier. _◦_ ✓ ✓ ✓
Memp (Fang et al., 2025) Trajectory ✗ Hier. ✓ ✗ ✗ ✓
MemOS (Li et al., 2025) Dialogue ✗ Hier. _◦_ ✓ _◦_ ✓
EverMemOS (Hu et al., 2026) Dialogue ✗ Hier. ✗ ✓ ✓ ✓


**FileGramOS (Ours)** **File Sys.** ✓ **Hier.** ✓ ✓ ✓ ✓


**Table 5** **Event types in raw trajectories.** The upper block lists the 12 atomic action types retained after cleaning with
their total counts across 640 trajectories. The lower block lists the 10 simulation metadata types removed, which
account for 74.3% of all raw events.


**Retained:** **Atomic Actions**


**Event Type** **Count** **Category** **Key Fields**


file_read 4,541 Read path, type, depth, view_count, view_range, length, revisit_ms
file_browse 1,649 Read dir_path, files_listed, depth
file_search 294 Read search_type, query, files_matched, files_opened
file_write 3,024 Write path, type, operation, length, before/after_hash, media_ref
file_edit 1,057 Write path, tool, lines_added/deleted/modified, diff, before/after_hash
dir_create 944 Org. dir_path, depth, sibling_count
file_copy 211 Org. src_path, dest_path, is_backup
file_move 130 Org. old_path, new_path, dest_depth
file_delete 92 Org. path, file_age_ms, was_temporary
file_rename 83 Org. old_path, new_path, naming_pattern
cross_file_ref 4,094 Flow src_file, target_file, ref_type, interval_ms
context_switch 3,909 Flow from_file, to_file, trigger, switch_count

**Subtotal** **20,028**


**Removed:** **Simulation Metadata**


tool_call 15,301 Sim. Raw tool invocation log
llm_response 13,096 Sim. LLM token counts, latency, stop reason
iteration_start 13,096 Sim. Agent loop iteration begin marker
iteration_end 13,096 Sim. Agent loop iteration end marker
fs_snapshot 1,280 Sim. Directory tree snapshot at session boundaries
session_start 640 Sim. Session bookkeeping
session_end 640 Sim. Session totals
error_encounter 233 Sim. Infrastructure errors
error_response 215 Sim. Automatic retry of tool failures
compaction_triggered 214 Sim. Context window compression

**Subtotal** **57,811**


16


**B.2** **Procedural Fingerprint Specification**


The procedural fingerprint **f** _j_ _∈_ R [17] compresses each trajectory’s behavioral events into a fixed-length vector
spanning all six profile dimensions. Table 6 enumerates the 17 features with their computation rules and
source event types.


**Table 6** **Procedural fingerprint specification.** All 17 features are computed deterministically from cleaned atomic actions,
grouped by the six behavioral dimensions. Source event types follow Table 5.


**Group** **Key** **Source Events** **Computation** **Interpretation**

search_ratio file_search, file_read, file_browse _|_ read _|_ + _|_ browse _|_ search _||_ + _|_ search _|_ Targeted search vs. sequential browsing
reading_strategy browse_ratio file_browse, file_read, file_search _|_ read _|_ + _|_ browse _|_ browse _|_ + _|_ _|_ search _|_ Directory-level exploration

revisit_ratio file_read _|{e_ :view_count _|_ read _|_ _>_ 1 _}|_ Re-reading previously viewed files


avg_output_length file_write: create mean(content_length) Average verbosity of created files
output_detail files_created file_write: create _|_ creates _|_ Number of output files produced
total_output_chars file_write: create          - content_length Total production volume


dirs_created dir_create _|_ dir_create _|_ Active directory structuring
directory_style max_dir_depth dir_create max(depth) Deepest nesting level
files_moved file_move _|_ file_move _|_ Reorganization via relocation


total_edits file_edit _|_ file_edit _|_ Post-creation modification frequency
edit_strategy avg_lines_changed file_edit mean(added + deleted) Average edit magnitude
small_edit_ratio file_edit _|{e_ :∆ _|_ linesedits _<|_ 10 _}|_ Fraction of incremental refinements


total_deletes file_delete _|_ file_delete _|_ Curation aggressiveness
version_strategy delete_to_create file_delete, file_write _||_ createsdeletes _||_ Curation vs. accumulation


structured_files file_write: create _|{e_ : ext _∈S}|_ Structured formats: csv, json, xlsx, etc.
cross_modal md_table_rows file_write: create - _|_ /ˆ|.*|/gm _|_ Inline tabular content in Markdown
image_files file_write: create _|{e_ : ext _∈I}|_ Visual content: png, jpg, svg, gif


**Normalization and consolidation.** During cross-engram consolidation (Stage 2), per-trajectory fingerprints
_{_ **f** 1 _, . . .,_ **f** _N_ _}_ are z-score normalized per dimension: _zk_ [(] _[j]_ [)] = ( _fk_ [(] _[j]_ [)] _−_ _µk_ ) _/_ ( _σk_ + _ϵ_ ), where _µk_ and _σk_ are computed
across all _N_ trajectories. The procedural channel then stores cross-trace statistics—mean, median, standard
deviation, min, and max—for each of the 17 features, providing a compact yet informative summary of the
profile’s behavioral tendencies.


**Design rationale.** The 17 features are chosen to cover all six behavioral dimensions with at least two features
each, use only deterministic counting-based computations that require no LLM calls and produce perfectly
reproducible outputs, and remain interpretable with a clear behavioral reading per feature. We experimented
with higher-dimensional feature sets of up to 50 raw statistics and found that the 17-feature subset retains
discriminative power while enabling efficient z-score normalization and deviation detection.


**B.3** **Semantic Channel Details**


The semantic channel captures _what_ the user produces and _how_ they produce it, complementing the procedural
channel’s quantitative statistics with content-level understanding.


**Per-trajectory extraction.** Each Engram’s Semantic Unit stores _file_ _metadata_ —detected language, file type
distribution, naming conventions, and representative filenames—alongside a _behavioral_ _descriptor_ generated
by a VLM from multimodal file snapshots and edit diffs, summarizing the user’s style, formatting, and detail
level. Created-file content and edit-chain diffs are split into 800-character chunks, embedded via Cohere
embed-english-v3.0 at 1024-D; up to 50 chunks per profile are retained, prioritizing non-deviant trajectories.


**Cross-session consolidation.** Stage 2 merges all Semantic Units into a unified profile: aggregated language and
naming statistics form the _static_ _content_ ; an LLM cross-session summary produces unified _Semantic_ _Clues_
such as “produces verbose Markdown reports with structured headers and inline tables”; the embedded chunks
are indexed for query-adaptive retrieval at Stage 3.


17


**Table 7** **Dimension derivation.** Each row is an OS-agent use case; each column is a behavioral dimension. Cells indicate
the specific capability the dimension enables for that use case.


**A: Consump.** **B: Product.** **C: Organiz.** **D: Iteration** **E: Curation** **F: Cross-M.**


**UC1:** **Proactive** Predict next read Predict format Pre-create dirs - Predict cleanup Predict chart need

**UC2:** **Defaults** Set read mode Set length & tone Set folder depth Set edit granularity - Set output modality

**UC3:** **Smart Org.** - - Maintain hierarchy - Predict retention 
**UC4:** **Recovery** Reconstruct reads Reconstruct drafts Navigate folders Reconstruct edits - 
**UC5:** **Continuity** Consistent reading Consistent style Consistent structure Consistent editing Consistent curation Consistent modality

**UC6:** **Conflict** Detect read drift Detect style change Detect reorganiz. Detect edit shift Detect curation chg. 
**UC7:** **Delegation** Read as user Write as user Organize as user Edit as user Curate as user Use user modalities


**B.4** **Episodic Segmentation and Boundary Detection**


The episodic channel partitions each trajectory into 2–5 semantically coherent _episodes_ —e.g., “document
survey” followed by “report drafting”—and clusters them across trajectories to surface recurrent themes.


**Per-trajectory segmentation.** Two LLM calls per trajectory. First, _boundary_ _detection_ : the event timeline
is rendered as a compact string of _∼_ 50 chars per event, and an LLM identifies 2–5 focus-shift boundaries,
validated, deduplicated, and capped at 4. Trajectories with fewer than 3 events or invalid outputs fall
back to a single episode; segments with fewer than 3 events merge with the preceding one. Second, _episode_
_summarization_ : for each segment, the LLM generates a title, a third-person narrative of 3–8 sentences, and a
one-sentence summary.


**Cross-trajectory** **clustering.** During consolidation, episode summaries are embedded with Cohere embedenglish-v3.0 at 1024-D and grouped via agglomerative clustering with average linkage, cosine similarity, and
a threshold of 0.6, surfacing recurrent themes across sessions. Separately, trajectories are clustered by their
17-D fingerprints using Euclidean distance with at most 3 clusters to capture distinct behavioral modes such
as read-heavy vs. production-heavy sessions. We chose LLM-based segmentation over sliding-window phase
detection, which is too coarse to distinguish different episodes within the same phase, and over HMMs, which
require labeled transition data unavailable for our task set; non-determinism is mitigated by strict validation
and single-episode fallback.


**B.5** **Query-Adaptive Retrieval Details**


Given a query _q_, the retriever concatenates three blocks in fixed order: _Procedural_ _Patterns_ —the full L/M/R
dimension summary and aggregate statistics, always included; _Semantic_ _Content_ —static metadata plus the
top-5 content chunks by cosine similarity to _q_ via Cohere embed-english-v3.0; and _Episodic_ _Consistency_ behavioral clusters, anomalous sessions, and the top-5 episode narratives by cosine similarity to _q_ . Content
previews are truncated to 800 characters and filenames to 40 characters, as determined by the sensitivity study
in Section D.2. The three channels are concatenated as Markdown sections with no cross-channel re-ranking;
ablation experiments confirm all three contribute complementary signal.

#### **C Benchmark Construction and Data**


**C.1** **Profile Design and Instantiation**


**Dimension derivation.** We derive the six behavioral dimensions from seven OS-agent use cases—Proactive
Assistance, Personalized Defaults, Smart Organization, Context Recovery, Behavioral Continuity, Conflict
Detection, and Delegation Quality—by asking _what_ _behavioral_ _aspect_ _must_ _the_ _agent_ _understand_ for each,
then grouping the resulting needs into orthogonal dimensions. Table 7 shows the complete mapping.


**Attribute schema.** Table 8 lists all 19 attributes: 3 identity and 16 behavioral, organized under dimensions
A–F with L/M/R tiers. Profile Reconstruction evaluates all 16 behavioral attributes per profile, yielding
20 _×_ 16 = 320 items.


18


**Table 8** **Profile attribute schema.** Three identity attributes define the user; 16 behavioral attributes span dimensions
A–F, each discretized into L/M/R tiers. version_strategy is shared by dimensions C and D. Profile Reconstruction
evaluates all 16 behavioral attributes per profile, yielding 20 _×_ 16 = 320 scored items.


**Attribute** **Dim.** **L** **M** **R**

#### name — Free-form display name role — Professional role language — Primary output language reading_strategy A Sequential deep Search-first Breadth-first thoroughness A Exhaustive Selective Minimal tone B Formal, academic Professional Casual output_detail B Comprehensive Balanced Concise output_structure B Highly structured Moderate Free-form documentation B Extensive Moderate Minimal directory_style C Nested, 3+ levels Adaptive, 1–2 Flat, root only naming C Systematic Semi-structured Ad-hoc version_strategy C,D Explicit v1/v2 Backup copies In-place overwrite edit_strategy D Incremental edits Balanced Bulk rewrite error_handling D Cautious, backup Selective backup Direct, no backup revision_depth D Multi-pass Two-pass Single-pass working_style E Phased, methodical Pragmatic Burst-mode cleanup_policy E Aggressive cleanup Periodic archival Never delete cross_modal F Visual-heavy Balanced Text-only output_modality F Multi-format Dual-format Single-format


**Table 9** **Profile instances.** L/M/R tier assignments across dimensions A–F for all 20 profiles. Each tier appears in at
least 5 profiles per dimension to prevent evaluation bias.

|ID Name Role A B C D E F|ID Name Role A B C D E F|
|---|---|
|p1<br>Chen Wei<br>Research Analyst<br>L<br>L<br>L<br>L<br>L<br>M<br>p2<br>Liu Jing<br>Policy Analyst<br>L<br>L<br>R<br>R<br>L<br>M<br>p3<br>Sam Taylor<br>Ops Manager<br>M<br>R<br>R<br>R<br>M<br>R<br>p4<br>Nakamura Yuki Finance Consultant<br>M<br>L<br>M<br>L<br>R<br>L<br>p5<br>Maria Santos<br>Marketing Coord.<br>R<br>M<br>M<br>M<br>R<br>M<br>p6<br>Alex Kim<br>Event Planner<br>R<br>M<br>L<br>R<br>M<br>R<br>p7<br>Zhang Meilin<br>Curriculum Designer<br>L<br>M<br>M<br>M<br>M<br>L<br>p8<br>Jordan Rivera<br>Technical Writer<br>R<br>R<br>M<br>L<br>R<br>R<br>p9<br>Li Hao<br>UX Researcher<br>M<br>M<br>L<br>M<br>L<br>L<br>p10<br>Emily Okafor<br>Quality Auditor<br>L<br>R<br>R<br>R<br>R<br>M|p11<br>Priya Sharma<br>Supply Chain Ana.<br>M<br>L<br>L<br>L<br>L<br>R<br>p12<br>Wang Fang<br>Journalism Editor<br>R<br>L<br>R<br>L<br>M M<br>p13<br>Zhao Ming<br>Landscape Arch.<br>L<br>M<br>L<br>M<br>L<br>L<br>p14<br>Daniel Osei<br>Compliance Ofcer<br>M<br>R<br>L<br>L<br>M<br>R<br>p15<br>Sophie Laurent<br>Project Manager<br>R<br>L<br>M<br>M<br>R<br>M<br>p16<br>Marcus Chen<br>Data Analyst<br>M<br>M<br>R<br>M<br>L<br>R<br>p17<br>Chen Wenjing<br>Museum Curator<br>L<br>L<br>L<br>L<br>M<br>L<br>p18<br>Aisha Johnson<br>Executive Assistant<br>R<br>R<br>R<br>R<br>L<br>M<br>p19<br>Lin Xiaoyu<br>Social Media Mgr.<br>M<br>M<br>R<br>M<br>M<br>R<br>p20<br>Tom O’Brien<br>Building Inspector<br>L<br>R<br>M<br>R<br>R<br>L|



**Profile instances.** Table 9 presents L/M/R assignments for all 20 profiles. Each tier appears in at least 5
profiles per dimension, preventing evaluation bias.


19


**C.2** **Task Pool and File Type Statistics**


We design 32 tasks spanning 6 types—16 text-centric and 16 multimodal with audio, image, or video inputs.
Table 10 provides the full task pool.


**Task representativeness.** Our six task types—Understand, Organize, Create, Synthesize, Iterate, Maintain—
subsume the core desktop activities in OSWorld (Xie et al., 2024), OfficeBench (Wang et al., 2024), and
OS-Copilot (Wu et al., 2024b), while adding curation and cross-modal dimensions absent from existing
benchmarks. Code development, real-time collaboration, and system administration are not covered, which
we note as a limitation in Section E.2.


**Table 10** **Task pool overview.** 32 tasks across 6 types with their activated dimensions and input file composition. A
dimension is listed when _≥_ 70% of profiles show non-trivial signal; parenthesized dimensions indicate 30–69% partial
activation. MM marks multimodal tasks.


**Task** **Type** **MM** **Description** **Dims** **In** **Input File Types**


T-01 Understand ✗ Investment analyst work overview summary A, B, E, F 26 .md(7), .pdf(6), .eml(5), .txt(5), .png(2), .csv(1)
T-02 Understand ✓ Legal case materials review and timeline A, B, E, F 24 .eml(6), .pdf(5), .docx(5), .txt(3), .png(2), .xlsx(1), .ics(1), .mp3(1)
T-03 Create ✗ Personal knowledge base creation B, (C), (E) 0 _empty_ _workspace_
T-04 Create ✗ Meeting minutes and follow-up document cre- B, (E) 0 _empty_ _workspace_
ation

T-05 Organize ✗ Messy folder cleanup and reorganization A, B, C, E, F 30 .eml(8), .png(4), .md(4), .txt(4), .pdf(4), .jpg(2), .ics(2), .csv(1), .docx(1)
T-06 Synthesize ✗ Multi-source synthesis research report A, B, E, F 21 .pdf(8), .eml(6), .txt(3), .md(3), .docx(1)
T-07 Synthesize ✓ Diary and notes synthesis into personal profile A, B, E, F 22 .eml(5), .txt(5), .png(4), .mp3(3), .ics(2), .xlsx(1), .pdf(1), .docx(1)
T-08 Create ✗ Quarterly work summary report creation A, B, E, F 18 .md(7), .eml(6), .txt(3), .docx(1), .csv(1)
T-09 Iterate ✗ Report revision and condensation B, D, (A), (E) 1 .md(1)
T-10 Maintain ✗ Knowledge base content update and mainte- A, B, D, E, F, (C) 5 .md(5)
nance

T-11 Iterate ✗ Multi-file error detection and correction A, B, D, E, F 7 .md(7)
T-12 Iterate ✗ Document format standardization A, B, D, E, F 16 .txt(7), .md(5), .pdf(2), .png(1), .eml(1)
T-13 Iterate ✗ Review feedback integration and revision A, B, D, E, F, (C) 4 .md(4)
T-14 Organize ✗ Version management and archiving A, B, C, E, F, (D) 10 .md(9), .csv(1)
T-15 Synthesize ✗ Conflicting reports analysis and reconciliation A, B, E, F 5 .md(3), .csv(2)
T-16 Understand ✓ Time-constrained priority triage A, E, B, F 22 .md(9), .eml(4), .pdf(3), .mp3(2), .png(2), .csv(1), .txt(1)
T-17 Understand ✗ File system health check and diagnostics A, B, E, F 24 .eml(6), .pdf(5), .docx(5), .txt(3), .png(2), .xlsx(1), .ics(1), .mp3(1)
T-18 Maintain ✗ Legal knowledge base three-round incremental A, B, C, D, E, F 16 .md(8), .pdf(4), .mp3(1), .docx(1), .eml(1), .png(1)
update

T-19 Iterate ✓ Document audience adaptation A, B, D, E, F 16 .docx(5), .pdf(3), .mp3(3), .eml(3), .md(2)
T-20 Create ✗ Weekly report management system setup B, E, (C) 0 _empty_ _workspace_
T-21 Organize ✓ File system cleanup and deduplication C, A, D 30 .png(18), .mp3(5), .jpg(5), .tmp(1), .bak(1)
T-22 Understand ✓ Film collection catalog and review A, F, B 24 .mp4(13), .gif(6), .jpg(2), .pptx(1), .pdf(1), .docx(1)
T-23 Organize ✓ Travel photo album organization C, F, A 40 .jpg(17), .jpeg(16), .png(7)
T-24 Synthesize ✓ Earnings call cross-modal analysis A, B, F 19 .mp3(8), .pdf(8), .md(3)
T-25 Understand ✓ Legal multimedia evidence review A, F, B 25 .mp4(5), .docx(5), .png(4), .pdf(4), .mp3(4), .eml(3)
T-26 Organize ✓ Personal digital asset archiving C, A, F 35 .png(12), .jpg(6), .mp3(5), .mp4(4), .txt(2), .mkv(2), .eml(2), .md(1), .csv(1)
T-27 Create ✓ Student portfolio compilation B, F, C 25 .pdf(13), .png(6), .mp4(2), .eml(2), .jpeg(1), .ics(1)
T-28 Synthesize ✓ Pet care archive synthesis A, B, F 18 .png(7), .eml(6), .mp3(3), .pdf(1), .ics(1)
T-29 Organize ✓ Company registration PDF database C, D, A 30 .pdf(28), .xlsx(2)
T-30 Iterate ✓ Voice memo organization and archiving D, F, A 17 .mp3(13), .txt(2), .md(2)
T-31 Create ✓ Nature scenery video collection curation B, F, C 24 .mp4(14), .jpeg(9), .jpg(1)
T-32 Maintain ✓ Cross-modal archive consistency check D, A, F 24 .png(8), .mp3(4), .mp4(3), .eml(3), .docx(3), .pdf(2), .txt(1)


**Total** **578**


**C.3** **Evaluation Pipeline**


**QA generation.** For MCQ tracks, all distractors must share at least 3 dimensions with the target to ensure
non-trivial difficulty; GPT-4.1 converts structured templates into natural-language phrasing. For open-ended
Profile Reconstruction, an LLM judge scores each attribute on a 1–5 Likert scale—from incorrect identification **1**
to correct tier with specific evidence **5** —with randomized attribute order and calibration examples.


**Cross-backbone trace validation.** To verify that behavioral signal is genuine rather than a generation-model
artifact, we feed the same FileGramOS memory context to three QA backbones while fixing the judge
to Gemini 2.5-Flash. As shown in Table 11, all backbones achieve _>_ 80% accuracy with _<_ 2.0 pp variance,
confirming the signal is model-agnostic.


20


**Table 11** **Cross-backbone trace validation.** Per-attribute reconstruction accuracy (%) across three QA backbones, all
receiving the same FileGramOS memory context. Inter-backbone variance stays below 2.0 pp, confirming modelagnostic signal.


**QA Backbone** **Proc.** **Sem.** **Avg.**


Gemini 2.5-Flash 84.4 80.0 82.8
GPT-4.1 82.5 78.3 80.9
Claude Sonnet 4 83.8 80.0 82.2

#### **D Extended Experiments and Analysis**


**D.1** **Baseline Implementation Details**


All 12 baselines share the same QA backbone—Gemini 2.5-Flash—and receive identical cleaned event logs
and output files per profile. Table 12 summarizes each method’s category, memory mechanism, and key
configuration. All systems use their published default settings; no per-baseline hyperparameter sweeps are
performed. For systems not originally designed for file-system traces, such as Mem0 and Zep, each trajectory
is mapped to a conversation turn containing the full event log.


**Table 12** **Baseline implementation summary.** All 12 baselines plus FileGramOS share Gemini 2.5-Flash as QA backbone
and receive identical cleaned event logs and output files per profile.


**Method** **Category** **Memory Mechanism** **Key Config**


No Context Context None Lower bound
Full Context Context Full concatenation 625.2K tok avg
Naive RAG Context Chunk embed + top-5 retrieval 512-tok chunks, overlap 64
VisRAG Context ColPali vision embed + top-5 Page images + text fallback


Eager Summ. Text Per-trajectory LLM summary Concatenated summaries
Mem0 Text Flat key–value store Official SDK defaults
Zep Text Graph-based knowledge graph Graph + semantic search
MemOS Text Hierarchical tier pipeline Working/short/long-term
SimpleMem Text Compact keyword + semantic 9.3K tok avg
EverMemOS Text Temporal consolidation + hierarchy 1098.9K tok avg


MMA Multimodal Confidence-scored retrieval Text + visual ingestion
MemU Multimodal VLM captioning + dual store PDF/image captioning


FileGramOS Ours 3-channel structured extraction _τ_ =1 _._ 5, 109.7K tok avg


**D.2** **Ablation Studies**


**Memory channel removal.** We evaluate FileGramOS with each channel removed in turn, carefully decoupling
shared representations to ensure clean isolation. Table 13 reports the results.


The procedural channel is the dominant contributor: removing it causes the largest drop of _−_ 11.1 pp, with
Trace Disentanglement degrading most severely from 80.9 to 53.1. Removing the semantic or episodic channel
produces smaller but meaningful drops of _−_ 5.5 pp and _−_ 4.2 pp respectively, and each channel’s removal
most strongly degrades its own question type, validating that the three channels capture genuinely distinct
behavioral signals.


**Parameter sensitivity.** We vary retrieval-time truncation and context presentation parameters; ingest-time
variations all produce identical accuracy and are omitted. Table 14 reports the results.


21


**Table 13** **Channel ablation.** First row: absolute accuracy (%); ablation rows: per-cell ∆ relative to the full model. The
procedural channel contributes the largest overall drop; all three channels carry distinct, complementary signal.



**T1:** **Underst.** **T2:** **Reason.** **T3:** **Detect.** **Channel**
**Variant** **Avg**
Attr Behav Behav Trace Anom Shift

Proc Sem Epi

Rec FP Inf Dis Det Ana



Behav Trace

Inf Dis



Anom Shift
Proc Sem Epi
Det Ana



FileGramOS **50.6** **35.2** **42.1** **80.9** **70.2** **37.8** **60.1** **55.0** **58.9** **59.6**


**Table 14** **Parameter sensitivity.** Per-track accuracy (%) on Tracks 1–3. ∆: relative to the 300-char default for retriever
rows, and to the 800-char optimum for context rows. Ingest-time parameters have zero effect and are omitted.


**Configuration** **T1** **T2** **T3** **Avg** ∆


_Retriever_ _display_ _length_
300 chars (default) 46.0 70.7 48.7 53.5                500 chars 46.7 70.0 49.3 53.8 +0.3
800 chars **48.0** 71.3 49.3 **54.5** + **1.0**
1000 chars 46.7 72.0 49.3 54.3 +0.8


_Context_ _presentation_
Preview 200 _→_ 400 chars 47.3 72.0 **50.7** 55.2 +0.7
Files/task 3 _→_ 5 46.0 **72.7** 49.7 54.5 _±_ 0.0
Files/task 3 _→_ 2 42.7 71.3 50.0 53.5 _−_ 1.0
+ Edit chain diffs 44.0 69.3 49.7 53.2 _−_ 1.3

_−_ Content previews 43.3 71.3 47.3 52.3 _−_ 2.2


Track 2 is near-invariant across all configurations, as Trace Disentanglement relies on procedural statistics
alone. Track 1 is content-sensitive: display at 800 characters yields the best trade-off, while removing content
previews degrades it by _−_ 4.7 pp. This confirms that procedural features suffice for reasoning, while compact
semantic grounding is necessary for attribute inference and change-point detection.

#### **E Discussion and Resources**


**E.1** **Deployment and System Integration**


Although evaluated on synthetic traces, FileGramOS is designed for deployment atop real OS-level file-system
monitors.


**Event collection.** Native APIs—FSEvents on macOS, inotify/fanotify on Linux, ReadDirectoryChangesW
on Windows—report file creation, modification, deletion, and renaming in real time with negligible overhead.
FileGramOS’s 12 event types map directly to these notifications. Read-related events such as file_read and
file_browse additionally require application-level hooks or access-time tracking.


**Integration architecture.** A production deployment chains three components: a lightweight _event_ _collector_
daemon that filters OS events into a local append-only log; a periodic _Engram_ _encoder_ that runs Stage 1
extraction; and an on-demand _memory_ _consolidator_ _+_ _retriever_ that updates the three-channel store and
assembles query-relevant context. All processing is local by default.


**Current limitations.** Key open challenges include interleaved multi-application event streams, duplicate or
out-of-order events from cloud-synced file systems, and per-directory privacy opt-in/opt-out controls.


22


**E.2** **Ethical Considerations**


**Synthetic data and bias.** All traces are generated by Claude Haiku 4.5 rather than collected from real users,
eliminating direct privacy concerns but introducing potential model-inherent biases. We mitigate this through
20 profiles spanning diverse roles, languages, and behavioral configurations, validated by human verifiers.
Nonetheless, synthetic traces cannot capture the full complexity of real-world file-system interaction.


**Privacy.** File-system traces reveal sensitive patterns—working hours, task priorities, organizational habits—
even when synthetically generated. Real-world deployment requires informed consent, data minimization, right
to deletion, and access control. FileGramOS partially addresses minimization by design: the procedural
channel stores only 17-D aggregate fingerprints and the semantic channel stores descriptors rather than file
contents; however, the episodic channel retains temporal patterns that could be re-identified.


**Limitations.** All trajectories originate from a single LLM, which may impose stylistic uniformity absent in real
multi-user settings. Behavioral shifts are single-tier perturbations, whereas real drift is often gradual and
multi-dimensional. The 32 tasks exclude code development, real-time collaboration, and system administration.
With 20 profiles and 640 trajectories the benchmark operates at moderate scale; the sharp accuracy drop in
the Real-World setting confirms that sim-to-real transfer remains an open challenge.


**Intended use.** FileGramBench is a research benchmark for memory and personalization systems, released
under a research-use license. It is not intended for surveillance, employee monitoring, or profiling individuals
without explicit consent.


23


