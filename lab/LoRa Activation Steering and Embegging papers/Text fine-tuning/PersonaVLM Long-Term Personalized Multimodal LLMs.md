#### **PersonaVLM: Long-Term Personalized Multimodal LLMs**

Chang Nie [1] Chaoyou Fu [1][*] Yifan Zhang [2] Haihua Yang [2][†] Caifeng Shan [1]


1Nanjing University 2ByteDance


changnie@smail.nju.edu.cn, bradyfu24@gmail.com



**Abstract**


_Multimodal Large Language Models (MLLMs) serve as daily_
_assistants for millions._ _However, their ability to generate re-_
_sponses aligned with individual preferences remains limited._
_Prior approaches enable only static, single-turn personaliza-_
_tion through input augmentation or output alignment, and_
_thus fail to capture users’ evolving preferences and person-_
_ality_ _over_ _time_ _(see_ _Fig._ _1)._ _In_ _this_ _paper,_ _we_ _introduce_
_**PersonaVLM**_ _, an innovative personalized multimodal agent_
_framework designed for long-term personalization._ _It trans-_
_forms a general-purpose MLLM into a personalized assistant_
_by integrating three key capabilities:_ _(a)_ _**Remembering**_ _:_ _It_
_proactively_ _extracts_ _and_ _summarizes_ _chronological_ _multi-_
_modal memories from interactions, consolidating them into_
_a personalized database._ _(b)_ _**Reasoning**_ _:_ _It conducts multi-_
_turn reasoning by retrieving and integrating relevant memo-_
_ries from the database._ _(c)_ _**Response Alignment**_ _:_ _It infers_
_the user’s evolving personality throughout long-term inter-_
_actions to ensure outputs remain aligned with their unique_
_characteristics._ _For evaluation, we establish_ _**Persona-MME**_ _,_
_a comprehensive benchmark comprising over 2,000 curated_
_interaction cases, designed to assess long-term MLLM per-_
_sonalization across seven key aspects and 14 fine-grained_
_tasks._ _Extensive experiments validate our method’s effective-_
_ness, improving the baseline by 22.4% (Persona-MME) and_
_9.8% (PERSONAMEM) under a 128k context, while outper-_
_forming GPT-4o by 5.2% and 2.0%,_ _respectively._ _Project_
_page:_ _[https://PersonaVLM.github.io.](https://PersonaVLM.github.io)_


**1. Introduction**


Multimodal Large Language Models (MLLMs) are increasingly integrated into the daily lives of millions of
users [1, 46], serving as assistants, creative partners, and
companions [19, 44, 47]. As their adoption grows, user
expectations are shifting from general-purpose problemsolving towards personalized and empathetic long-term ex

*Corresponding author.
†Project leader.



periences [20, 42]. This shift poses a critical question: _**How**_
_**can we evolve a general MLLM into a truly personalized**_
_**assistant**_ _**that**_ _**accurately**_ _**infers**_ _**user**_ _**intent,**_ _**dynamically**_
_**aligns its behavior with individual preferences and person-**_
_**ality, and persistently remembers user-specific multimodal**_
_**information over time?**_ Addressing this question not only
enhances user satisfaction and trust but also unlocks the
significant value of MLLMs in domains like recommendation [38], healthcare [3], and education [48], to name a few.

Even advanced proprietary models exhibit limited capabilities in generating responses that cater to a user’s unique
preferences and characteristics [6, 14, 50]. This challenge
stems from two primary factors: on the model side, they
are predominantly optimized within fixed windows and a
one-size-fits-all paradigm [21]; on the user side, an individual’s preferences and personality are inherently diverse and
dynamic, continuously evolving throughout ongoing interactions [14]. As illustrated in Fig. 1, a user initially expresses a
preference for _Sprite_ but subsequently shifts to _Coca-Cola_ to
mitigate anxiety in a multimodal interaction. When the user
later expresses stress, a retrieval-augmented response fails
to capture this shift, resulting in a misaligned recommendation. Furthermore, a generic aligned response may feel
overly extraverted, failing to accommodate the introverted
and neurotic user whose personality traits are often revealed
subtly across many unrelated dialogues.

The root of these failures is that current personalization
strategies are designed for static interactions. Specifically,
input augmentation-based MLLMs like Yo’LLaVA [28] and
RAP [11] specialize in recognizing user-specific concepts,
but lack mechanisms to manage or update these memories, consequently failing to capture preference shifts from
_Sprite_ to _Coca-Cola_ . Similarly, alignment techniques such
as ALIGNXPERT [21] and Personality-Activation Search
(PAS) [52] presuppose static user traits, preventing them
from adapting to a user’s introversion revealed contextually
over time. Therefore, we identify two foundational pillars for
effective long-term personalization: (i) _**Personalized Mem-**_
_**ory Architecture**_ . The ability to proactively construct and
manage a dynamic, user-centric multimodal database. (ii)
_**Memory Utilization and Response Alignment**_ . The capacity


Figure 1. Illustration of PersonaVLM’s three core capabilities for long-term personalization. PersonaVLM proactively remembers user
preference shifts, performs multi-turn reasoning with retrieval, and generates responses aligned with the user’s personality. In contrast,
existing personalization strategies, such as input augmentation and output alignment, will result in poor recommendations based on outdated
memories and replies that are misaligned with the user’s personality.



to effectively utilize this database, employing reasoning and
retrieval to generate responses that are deeply aligned with
the user’s unique and evolving characteristics.
Building on these pillars, we propose **PersonaVLM**, an
innovative agent framework for long-term personalized interaction. First, we design a memory architecture that integrates a user personality profile and four distinct memory
types ( _core_ for foundational attributes, _semantic_ for facts,
_procedural_ for habits, and _episodic_ for events) to store and
manage user information. Second, building upon this architecture, a two-stage collaborative process transforms a
general MLLM into a personalized assistant: (1) Response
stage: Given the user’s multimodal input and context, PersonaVLM autonomously performs multi-step reasoning and
memory retrieval to generate a response aligned with the
user’s personality. (2) Update stage: The model infers and
updates the user’s latent traits, quantified as Big Five scores [1],
through a momentum-based Personality Evolving Mechanism (PEM). Concurrently, it proactively extracts and summarizes key knowledge from the dialogue, updating the four
memory types for future use. This integrated design endows
PersonaVLM with the three key capabilities shown in Fig. 1.
Alongside the design of the framework, we address the
scarcity of suitable training data by developing a synthesis
pipeline to generate a large-scale personalized, multimodal
interactive dataset, comprising over 30 _k_ interactions across
500 unique personas. This self-contained dataset enables
effective training while ensuring PersonaVLM can operate
locally, thereby eliminating data privacy concerns. Furthermore, recognizing that existing benchmarks [24] are often
static and text-centric, we establish **Persona-MME**, a comprehensive benchmark designed to evaluate the long-term,
multi-faceted, and multimodal personalization of MLLMs.


1We represent user personality using the Big Five traits [35]: Openness, Conscientiousness, Extraversion, Agreeableness, and Neuroticism
(OCEAN), with each trait scored from 1 to 5.



In summary, our contributions are fourfold:

- We propose PersonaVLM, an innovative agent framework
that achieves long-term personalization for MLLMs by integrating three core capabilities: proactive _**R**_ _emembering_,
multi-step _**R**_ _easoning_, and _**R**_ _esponse Alignment_ .

- We introduce a personalized memory architecture featuring two key components: the PEM for dynamic alignment
and a multi-type memory database comprising core, procedural, semantic, and episodic memories.

- We establish Persona-MME, a comprehensive benchmark
designed to evaluate the long-term and multi-faceted personalization capabilities of MLLMs, and use it to benchmark over 10 leading proprietary and open-source models.

- We conduct extensive experiments to validate the effectiveness of PersonaVLM. Under a 128 _k_ context, PersonaVLM
achieves improvements of 22.4% on Persona-MME and
9.8% on PERSONAMEM [14]. Notably, it surpasses GPT4o on these benchmarks and in open-ended evaluations.


**2. Related Work**


The recent surge in LLM development has catalyzed
the emergence of powerful MLLMs like GPT-4o [12],
LLaVA [23], and the Qwen series [5, 45], showcasing exceptional capabilities in various general-domain tasks [47].
However, to evolve into a true personal assistant, a model
must transcend the “one-size-fits-all” paradigm and tailor responses to individual user knowledge and preferences [24, 49]. Existing efforts to address this challenge can
be categorized into three primary streams: adaptation-based,
augmentation-based, and alignment-based personalization.


**Adaptation-based** **Personalization.** Adaptation-based
methods operate at the model level, encoding user-specific
knowledge directly into trainable parameters through finetuning. Some works, for instance, employ parameterefficient fine-tuning (PEFT) to adapt LLMs for individ

Figure 2. Overview of the PersonaVLM Framework. It leverages a personalized memory architecture and operates in two collaborative
stages to achieve long-term personalization. In the Response Stage (blue arrows), it processes multimodal input, retrieves from personalized
memory, and generates a personality-aligned response. Subsequently, in the Update Stage (pink arrows), the framework analyzes the
completed interaction to extract key memories and update the user’s evolving personality profile [1] .



ual users or groups [37, 53]. This principle extends to
the multimodal domain, where personalized MLLMs like
MyVLM [2] and Yo’LLaVA [28] utilize learnable embeddings and soft prompts, respectively, to represent userspecific visual concepts. Such adaptation enables the model
to transition from recognizing “a generic dog” to recognizing
“the user’s pet dog.” However, their reliance on fine-tuning
for each new user concept renders these methods less scalable and unable to capture the evolution of user preferences.


**Augmentation-based** **Personalization.** In contrast to
model-level adaptation, augmentation-based approaches operate at the input level by equipping models with an external database to retain and retrieve user-specific memories [39, 41]. This paradigm is pivotal for transcending the
limitations of fixed context windows in lifelong dialogues [7].
Related approaches [11, 29] extend personalization to the
multimodal domain. They first employ open-vocabulary
object detectors [25] to crop predefined visual concepts
from images, which are then used for subsequent matching and retrieval. A key advantage of these methods is their
training-free nature [2], allowing them to accommodate new
user concepts at inference time. However, they are limited
by a manually predefined database and lack mechanisms to
proactively manage and update knowledge from dynamic
interactions. Moreover, while general-purpose memory architectures like A-Mem [43] and Memory OS [22] employ


2Following the specific terminology from [32], this denotes that new
user concepts can be accommodated at inference time without requiring
continual fine-tuning.



more sophisticated agentic frameworks, their utility in our
context is severely constrained. Their primary focus on textonly data limits their applicability to truly multimodal inputs,
and their reliance on proprietary models creates barriers for
open research and raises significant privacy concerns.


**Alignment-based Personalization.** While standard LLM
alignment, such as Reinforcement Learning from Human
Feedback (RLHF) [30], enforces a universal, “one-size-fitsall” behavioral standard, it inherently fails to accommodate
diverse user preferences and communication styles. As
shown in Fig. 1 (right), an overly enthusiastic response, while
generally helpful, might be inappropriate for an introverted
user experiencing anxiety. Personalized alignment directly
tackles this limitation by redefining the optimization objective from a universal standard to a user-specific one [24].
For example, Li et al. [21] incorporate user features into the
input and use methods such as Direct Preference Optimization (DPO) [34] to align model responses with predefined
user values. Another strategy, PAS [52], trains user-specific
“probes” to guide personalization at inference time. While
this approach enables inference-time adaptation, it is fundamentally limited. Its reliance on per-user training poses
significant scalability challenges; moreover, the static nature
of these probes means the alignment can become outdated
as the user’s personality evolves over long-term interactions.


Departing from prior works that address siloed aspects
of personalization for MLLMs, such as static memory or
fixed alignment, we introduce PersonaVLM: a unified agent
framework designed for dynamic, long-term interaction.


**3. Methods**


**3.1. PersonaVLM Framework**


The overall architecture of the PersonaVLM agent is illustrated in Fig. 2. It is built upon a personalized memory
architecture and operates through two collaborative stages of
**Response** and **Update** to enable long-term personalization.


**Personalized Memory Architecture.** This architecture is
designed to construct and maintain a comprehensive, longterm user profile, storing two primary categories of information. First, it maintains a user personality profile ( _P_ ), which
provides a quantitative representation of the user’s personality as a vector of scores for the Big Five dimensions [3]

(Openness, Conscientiousness, Extraversion, Agreeableness,
and Neuroticism). Second, it features a multi-type memory database ( _M_ ) that captures a wide range of user-related
knowledge. This timeline-based, agentic system supports
flexible CRUD (create, read, update, delete) operations and
is structured into four distinct memory types:

- **Core** **Memory:** Stores the user’s fundamental attributes (e.g., human and persona blocks), inspired by
MemGPT [31], and is dynamically updated to reflect their
most current profile.

- **Semantic Memory:** Distills event-independent, abstract
knowledge by extracting key entities, relationships, and
multimodal concepts.

- **Episodic Memory:** Organizes raw dialogues into atomic,
time-stamped events, each including a summary, dialogue
turns, and keywords for efficient retrieval.

- **Procedural Memory:** Records user-centric plans, goals,
and recurring behaviors or habits.
Regarding their storage and persistence, while episodic and
semantic memories are stored chronologically, core and procedural memories, along with the personality profile, retain
only their latest versions to ensure relevance. Our design
overcomes the limitations of existing systems, making our
memory architecture: (a) Self-contained, avoiding proprietary model dependencies; (b) Explicitly personalized, prioritizing user-centric knowledge; and (c) Multimodal support,
enabling a more holistic user understanding. For details on
our memory architecture, refer to Appendix A.


**Response Stage.** The objective of this stage is to generate
an aligned response by performing multi-step reasoning and
timeline-based retrieval. Formally, this process at turn _m_
can be formulated as:


_Rm_ = _R_ ( _Qm, Cm, Mm−_ 1) _,_ (1)


where _Rm_ is the personalized response. This response
is conditioned on three inputs: the current user query
_Qm_ = ( _Tm, Im, tm_ ), consisting of a text instruction _Tm_,


3Representing user personality via the Big Five traits is a prevalent
approach in LLM alignment [52], rooted in psychological theories [16, 35].



an optional image _Im_, and a timestamp _tm_ ; the dialogue
context [4] _Cm_ = _{_ ( _Qi, Ri_ ) _|_ 0 _< i < m_ and _|ti −_ _tm| ≤_ _ts}_ ;
and the state of the personalized memory database _Mm−_ 1.
As depicted in the left panel of Fig. 2, the implementation
of Eq. (1) is structured as a multi-step interaction between
the PersonaVLM agent and its memory system. In the initial
step, the model is prompted with the user’s instruction, context, and a consolidated profile (comprising the user’s core
memory and personality). The model then outputs a detailed
reasoning process and an `action` result. If the model determines that the current information is insufficient, it outputs
retrieval conditions within a predefined template, including
the `time period` and `keywords` for searching. The agent
then executes the retrieval process by first isolating memories within the inferred `time period` and then performing
a parallel search across semantic, episodic, and procedural memory types. The top- _k_ results from each type are
collected and fed back to the model to initiate the next reasoning step. This iterative process continues for multiple
rounds until the model outputs the final response _Rm_ .
Two key insights drive the design of this stage. First,
user queries are often highly context-dependent and contain
anaphora (e.g., “that thing we just talked about”), which
renders direct semantic retrieval imprecise. In contrast, a
multi-turn, agentic retrieval process typically yields more
precise and efficient results [15, 26]. Second, while some
memory mechanisms [22, 40] may leverage query rewriting [27] to improve retrieval accuracy, they overlook crucial
temporal cues (e.g., “this morning”). Our design addresses
these gaps by enabling the model to determine not just _what_
to retrieve, but also _if_ retrieval is necessary and from _when_ .


**Update Stage.** This stage, which executes automatically
during idle periods after a response is generated, primarily
involves two parts: evolving the user’s personality profile
and proactively updating the memories. This process at turn
_m_ can be represented as:


( _Pm, Mm_ ) = _U_ ( _Qm, Rm, Mm−_ 1) _._ (2)


Specifically, the user’s personality profile, _Pm_, is updated
via our proposed **Personality Evolving Mechanism (PEM)** .
The PEM maintains a long-term personality profile as a vector **p** _∈_ R [5], corresponding to the Big Five dimensions [52].
At each turn _m_, the PEM first infers a temporary set of
personality scores from the user’s latest query, _Qm_ . These
scores are normalized to form a turn-specific personality
vector, **p** _[′]_ _m_ [.] Subsequently, the long-term profile vector
is updated using an exponential moving average (EMA):
**p** _m_ _←_ _λ_ _·_ **p** _m−_ 1 + (1 _−_ _λ_ ) _·_ **p** _[′]_ _m_ [,] [where] _[λ]_ _[∈]_ [[0] _[,]_ [ 1]] [is] [a]
dynamic smoothing factor. To ensure high adaptability in


4We treat the recent conversation history (within a _ts_ = 60 minute
threshold) as short-term memory, and user inactivity beyond this threshold
initiates a new session.


**(a) Data Synthesis Pipeline**



**(b) Persona-MME Overview**



**(c) Samples and Tasks Distribution**



Figure 3. Overview of our data synthesis pipeline and Persona-MME. (a) The pipeline first constructs rich user personas and then simulates
long-term, dynamic conversations, generating both the dialogue and intermediate memories. (b) Persona-MME provides a comprehensive
evaluation of personalization by assessing 14 fine-grained capabilities. (c) Statistics for Persona-MME, which includes two context length
configurations (32 _k_ and 128 _k_ ) and contains over 2,000 _in-situ_ [6] cases.



early conversations while promoting stability over time, we
employ a cosine decay schedule for _λ_ . It starts with a low
value (allowing rapid adaptation to initial user interactions)
and gradually increases, making the profile more stable and
less susceptible to minor fluctuations. Finally, the updated
numerical vector **p** _m_ is converted back into a descriptive
textual summary, _Pm_, for use in the Response Stage.
Second, we selectively extract and update the four memory types, each with tailored logic. Semantic memory is
updated after each turn, where key information such as user
preferences, multimodal concepts, and explicit memorization requests is extracted and stored with timestamps and
keywords. In contrast, core and procedural memory are updated at the end of each session; the agent analyzes the entire
session’s dialogue to perform automated CRUD operations
and keep these memories current. Finally, episodic memory
is constructed by segmenting dialogues into distinct topics,
with each entry containing a summary, relevant keywords,
and the specific dialogue turns involved. See Appendix B.1
for the complete implementation pipeline.


**3.2. Training of PersonaVLM**


We adopt Qwen2.5-VL-7B [5] as the backbone model for
PersonaVLM and train it using a two-stage process.


**Stage** **1:** **Supervised** **Fine-Tuning** **(SFT).** We perform
SFT on a curated synthetic dataset of 78 _k_ samples to equip
the model with foundational memory management and multiturn reasoning skills. The training data is synthesized via a
pipeline introduced in the next section and comprises two
primary types: (a) examples for memory mechanisms, including personality inference and the four types of memory



CRUD operations; and (b) QA pairs containing complete,
multi-step reasoning trajectories constructed offline. After
SFT, the model is capable of generating well-formed reasoning and retrieval actions, providing a strong cold-start
initialization for the subsequent stage.


**Stage 2:** **Reinforcement Learning (RL).** This stage aims
to further enhance the model’s multi-turn reasoning capability. We employ Group Relative Policy Optimization
(GRPO) [10], an improved PPO algorithm, to train the policy
model _πθ_ . During generation, we enforce a strictly structured output format: the model must first output its reasoning
process within <think></think> tags, followed by either retrieval conditions in <retrieve></retrieve>
tags or the final response in <answer></answer> tags.
For each training sample _{Q,_ _R}_, where _Q_ is the user input

[�]
and _R_ is the preferred response, a group of multi-turn trajec
[�]
tories _{τ_ 1 _, . . ., τG}_ is sampled from the policy model. The
reward for the _i_ -th trajectory _τi_ is calculated as:


_ri_ = _f_ acc( _R_ [�] _, Rτi_ ) _· f_ cons( _Q, Rτi_ ) + 0 _._ 5 _· f_ format( _Rτi_ ) _,_ (3)


where _f_ acc, _f_ cons, and _f_ format are reward functions for accuracy, logical consistency between reasoning and the final
answer, and format adherence, respectively. We use Qwen330B-A3B [45] as an _LLM-as-a-Judge_ to compute _f_ acc and
_f_ cons via zero-shot prompting. Following [10], the advantage
for each trajectory is computed by standardizing its reward
within the sampled group. During training, we cap the maximum number of retrieval attempts at three per trajectory,
and the loss is computed exclusively on the generated tokens.
Further details on the training data and implementation are
provided in Appendix B.2.


**4. Dataset and Persona-MME Construction**


To enable both the implementation and evaluation of longterm dynamic personalization, we make two key contributions. First, to address the scarcity of high-quality training data, we construct a large-scale multimodal interaction
dataset via a dedicated synthesis pipeline. Second, we establish Persona-MME, a comprehensive benchmark for evaluating personalization in multimodal settings. This dual
effort is necessitated by existing datasets [21, 28], which are
typically static, single-turn, or lack multimodal support.


**Dataset Synthesis Pipeline.** As illustrated in Fig. 3 (a), we
design a synthesis pipeline to generate training data at _scale_ .
The process commences by sampling base personas from
PersonaHub [9], which are then enriched with randomly assigned personality traits. This enrichment step generates a
detailed role description and an initial user profile, forming
the initial Core Memory. We employ Seed1.6-thinking [5] to
generate conversations guided by a structured flow. This process is governed by several key principles: (1) **Long-term**
**Dynamics** : Dialogues extend over hundreds of turns to simulate interactions spanning weeks or months. To capture this
longitudinal evolution, we probabilistically induce dynamic
shifts in user preferences, topics, and personality traits. (2)
**Multimodality and Scenario Diversity** : Over 15% of dialogues incorporate multimodal elements. The interactions
span a wide range of real-world scenarios, from professional
tasks to casual conversations. (3) **Structured Supervision** :
The generation process is guided to produce not only the
conversational dialogue but also the intermediate reasoning,
retrieval, and memorization steps. This explicit structure
provides rich supervisory signals for training the PersonaVLM framework. Further details on the data distribution
and validation process are provided in Appendix C.


**Persona-MME: Evaluating Long-Term Personalization**
**of MLLMs.** Existing benchmarks focus on siloed aspects
of personalization. For instance, PERSONAMEM [14] evaluates a model’s ability to track a user’s evolving profile,
ALIGNX-test [21] is centered on static alignment, and others like Yo’LLaVA [11, 28] assess user-specific concept
understanding. However, none provide a holistic evaluation
across the critical dimensions of dynamic personalization.
To fill this void, we introduce Persona-MME, a comprehensive benchmark comprising over 2,000 _in-situ_ [6] cases
derived from 200 diverse personas. As depicted in Fig. 3
(b), Persona-MME is structured around seven core dimensions: **Memory, Intent, Preference, Behavior, Relation-**
**ship, Growth, and Alignment** . Together, these dimensions


5Seed1.6-thinking is a commercial model with performance comparable
to GPT-4o, selected for its balance of capability and cost-effectiveness.
6Queries are posed from the user’s first-person perspective at a specific
point in the conversational history, simulating a realistic interaction [14].



|GPT-4o LlaMA 3.1-8B InternVL3-8B Qwen2.5-VL-7B PersonaVLM (ours)|Col2|Col3|Col4|Col5|Col6|Col7|Col8|Col9|
|---|---|---|---|---|---|---|---|---|
|<br> <br>0.0<br>0.1<br>0.2<br>0.3<br>0.4<br>0.5<br>0.6<br>0.7<br>0.8<br>0.9<br>Accuracy|||||||||
|<br> <br>0.0<br>0.1<br>0.2<br>0.3<br>0.4<br>0.5<br>0.6<br>0.7<br>0.8<br>0.9<br>Accuracy|||||||||
|<br> <br>0.0<br>0.1<br>0.2<br>0.3<br>0.4<br>0.5<br>0.6<br>0.7<br>0.8<br>0.9<br>Accuracy|||||||||
|<br> <br>0.0<br>0.1<br>0.2<br>0.3<br>0.4<br>0.5<br>0.6<br>0.7<br>0.8<br>0.9<br>Accuracy|||||||||
|<br> <br>0.0<br>0.1<br>0.2<br>0.3<br>0.4<br>0.5<br>0.6<br>0.7<br>0.8<br>0.9<br>Accuracy|||||||||
|<br> <br>0.0<br>0.1<br>0.2<br>0.3<br>0.4<br>0.5<br>0.6<br>0.7<br>0.8<br>0.9<br>Accuracy|||||||||
|<br> <br>0.0<br>0.1<br>0.2<br>0.3<br>0.4<br>0.5<br>0.6<br>0.7<br>0.8<br>0.9<br>Accuracy|||||||||
|<br> <br>0.0<br>0.1<br>0.2<br>0.3<br>0.4<br>0.5<br>0.6<br>0.7<br>0.8<br>0.9<br>Accuracy|||||||||
|<br> <br>0.0<br>0.1<br>0.2<br>0.3<br>0.4<br>0.5<br>0.6<br>0.7<br>0.8<br>0.9<br>Accuracy|<br>||<br>|<br>|<br>||<br>||


Figure 4. Quantitative evaluation across seven tasks on the PERSONAMEM (32 _k_ ) benchmark.


encompass 14 fine-grained tasks, which are detailed in Table 5 in the Appendix. To accommodate different context
lengths, we provide two evaluation configurations: a 32 _k_ context version for dialogues under 100 turns and a 128 _k_ context version for longer interactions, each containing cases
from 100 distinct personas. Each test case comprises (1) a
multiple-choice question assessing the model’s personalized
memory and understanding, and (2) an optional personality
test evaluating its alignment. This multi-faceted structure
enables Persona-MME to evaluate an MLLM’s long-term
personalization capabilities across diverse personas. Further
details and statistics are provided in Appendix D.


**5. Experiments**


In this section, we present a series of quantitative and qualitative experiments designed to validate our PersonaVLM
framework. The evaluation in the main paper is structured
to answer the following research questions (RQs):

- **RQ1:** How effectively does PersonaVLM perform in personalized user understanding and memory recall?

- **RQ2:** Can PersonaVLM achieve effective alignment by
capturing a user’s evolving personality traits over time?

- **RQ3:** How well does PersonaVLM perform in personalized open-ended generation?

For comprehensive evaluations of Persona-MME, ablation
studies about memory components, and further discussions,
please refer to Appendices D, E, and F, respectively.


**5.1. Personalized Understanding Evaluation**


To evaluate personalized understanding (RQ1), we conduct
experiments on two benchmarks: our Persona-MME and
PERSONAMEM [14]. The latter includes seven task types
specifically designed to assess a model’s ability to track
dynamic user preferences over the long term. We evaluate
all models under two long-context settings (32 _k_ and 128 _k_
tokens), with detailed results reported in Table 1 and Fig. 4.
For comparison, we benchmark against several powerful
models, including the proprietary GPT-4o [12] and strong
open-source models such as Qwen2.5-VL-7B [5], LLaVAOneVision-1.5-8B [4], and InternVL3-8B/38B [51]. See


Table 1. Evaluation on the Persona-MME and PERSONAMEM benchmarks, tested at context lengths of 32 _k_ and 128 _k_ . We report accuracy
(%) for Persona-MME (overall and across six aspects) and PERSONAMEM. The comparison includes two settings: full-context (“Full”)
and retrieval-augmented generation (“RAG”). Best results are shown in **bold** . The GPT-4o results on PERSONAMEM are from [14].


|Persona-MME<br>Context Model PERSONAMEM<br>Memory Intent Preference Behavior Relationship Growth Overall|Col2|Col3|Col4|Col5|
|---|---|---|---|---|
|**Context**<br>**Model**<br>**Persona-MME**<br>**PERSONAMEM**<br>Memory<br>Intent<br>Preference<br>Behavior<br>Relationship<br>Growth<br>Overall|**Context**<br>**Model**<br>**Persona-MME**<br>**PERSONAMEM**<br>Memory<br>Intent<br>Preference<br>Behavior<br>Relationship<br>Growth<br>Overall|**Context**<br>**Model**<br>**Persona-MME**<br>**PERSONAMEM**<br>Memory<br>Intent<br>Preference<br>Behavior<br>Relationship<br>Growth<br>Overall|Overall|Overall|
|GPT-4o<br>**86.99**<br>**83.87**<br>**63.12**<br>57.14<br>71.30<br>73.87<br>**72.35**<br>39.20<br>32_k_-Full<br>Qwen2.5-VL-7B<br>66.13<br>66.85<br>59.75<br>59.24<br>68.45<br>70.69<br>64.84<br>43.63<br>InternVL3-8B<br>56.45<br>76.24<br>57.20<br>54.35<br>69.05<br>74.14<br>64.04<br>52.97<br>InternVL3-38B<br>66.67<br>85.64<br>66.53<br>59.78<br>72.02<br>77.59<br>71.04<br>**57.93**<br>OneVision-1.5-8B<br>74.19<br>74.59<br>60.59<br>53.26<br>72.62<br>74.14<br>67.76<br>52.80<br>Qwen2.5-VL-7B<br>65.05<br>68.51<br>50.42<br>57.61<br>60.71<br>68.39<br>61.20<br>45.67<br>32_k_-RAG<br>PersonaVLMSFT<br>67.20<br>70.17<br>49.58<br>57.07<br>70.24<br>80.46<br>64.84+3_._64<br>52.12+6_._45<br>PersonaVLMRL<br>69.89<br>76.80<br>58.05<br>**69.02**<br>**73.21**<br>**86.78**<br>71.48+10_._28<br>56.53+10_._86|GPT-4o<br>**86.99**<br>**83.87**<br>**63.12**<br>57.14<br>71.30<br>73.87<br>**72.35**<br>39.20<br>32_k_-Full<br>Qwen2.5-VL-7B<br>66.13<br>66.85<br>59.75<br>59.24<br>68.45<br>70.69<br>64.84<br>43.63<br>InternVL3-8B<br>56.45<br>76.24<br>57.20<br>54.35<br>69.05<br>74.14<br>64.04<br>52.97<br>InternVL3-38B<br>66.67<br>85.64<br>66.53<br>59.78<br>72.02<br>77.59<br>71.04<br>**57.93**<br>OneVision-1.5-8B<br>74.19<br>74.59<br>60.59<br>53.26<br>72.62<br>74.14<br>67.76<br>52.80<br>Qwen2.5-VL-7B<br>65.05<br>68.51<br>50.42<br>57.61<br>60.71<br>68.39<br>61.20<br>45.67<br>32_k_-RAG<br>PersonaVLMSFT<br>67.20<br>70.17<br>49.58<br>57.07<br>70.24<br>80.46<br>64.84+3_._64<br>52.12+6_._45<br>PersonaVLMRL<br>69.89<br>76.80<br>58.05<br>**69.02**<br>**73.21**<br>**86.78**<br>71.48+10_._28<br>56.53+10_._86|**86.99**<br>**83.87**<br>**63.12**<br>57.14<br>71.30<br>73.87|**72.35**|39.20|
|GPT-4o<br>**86.99**<br>**83.87**<br>**63.12**<br>57.14<br>71.30<br>73.87<br>**72.35**<br>39.20<br>32_k_-Full<br>Qwen2.5-VL-7B<br>66.13<br>66.85<br>59.75<br>59.24<br>68.45<br>70.69<br>64.84<br>43.63<br>InternVL3-8B<br>56.45<br>76.24<br>57.20<br>54.35<br>69.05<br>74.14<br>64.04<br>52.97<br>InternVL3-38B<br>66.67<br>85.64<br>66.53<br>59.78<br>72.02<br>77.59<br>71.04<br>**57.93**<br>OneVision-1.5-8B<br>74.19<br>74.59<br>60.59<br>53.26<br>72.62<br>74.14<br>67.76<br>52.80<br>Qwen2.5-VL-7B<br>65.05<br>68.51<br>50.42<br>57.61<br>60.71<br>68.39<br>61.20<br>45.67<br>32_k_-RAG<br>PersonaVLMSFT<br>67.20<br>70.17<br>49.58<br>57.07<br>70.24<br>80.46<br>64.84+3_._64<br>52.12+6_._45<br>PersonaVLMRL<br>69.89<br>76.80<br>58.05<br>**69.02**<br>**73.21**<br>**86.78**<br>71.48+10_._28<br>56.53+10_._86|GPT-4o<br>**86.99**<br>**83.87**<br>**63.12**<br>57.14<br>71.30<br>73.87<br>**72.35**<br>39.20<br>32_k_-Full<br>Qwen2.5-VL-7B<br>66.13<br>66.85<br>59.75<br>59.24<br>68.45<br>70.69<br>64.84<br>43.63<br>InternVL3-8B<br>56.45<br>76.24<br>57.20<br>54.35<br>69.05<br>74.14<br>64.04<br>52.97<br>InternVL3-38B<br>66.67<br>85.64<br>66.53<br>59.78<br>72.02<br>77.59<br>71.04<br>**57.93**<br>OneVision-1.5-8B<br>74.19<br>74.59<br>60.59<br>53.26<br>72.62<br>74.14<br>67.76<br>52.80<br>Qwen2.5-VL-7B<br>65.05<br>68.51<br>50.42<br>57.61<br>60.71<br>68.39<br>61.20<br>45.67<br>32_k_-RAG<br>PersonaVLMSFT<br>67.20<br>70.17<br>49.58<br>57.07<br>70.24<br>80.46<br>64.84+3_._64<br>52.12+6_._45<br>PersonaVLMRL<br>69.89<br>76.80<br>58.05<br>**69.02**<br>**73.21**<br>**86.78**<br>71.48+10_._28<br>56.53+10_._86|66.13<br>66.85<br>59.75<br>59.24<br>68.45<br>70.69<br>56.45<br>76.24<br>57.20<br>54.35<br>69.05<br>74.14<br>66.67<br>85.64<br>66.53<br>59.78<br>72.02<br>77.59<br>74.19<br>74.59<br>60.59<br>53.26<br>72.62<br>74.14|64.84<br>64.04<br>71.04<br>67.76|43.63<br>52.97<br>**57.93**<br>52.80|
|GPT-4o<br>**86.99**<br>**83.87**<br>**63.12**<br>57.14<br>71.30<br>73.87<br>**72.35**<br>39.20<br>32_k_-Full<br>Qwen2.5-VL-7B<br>66.13<br>66.85<br>59.75<br>59.24<br>68.45<br>70.69<br>64.84<br>43.63<br>InternVL3-8B<br>56.45<br>76.24<br>57.20<br>54.35<br>69.05<br>74.14<br>64.04<br>52.97<br>InternVL3-38B<br>66.67<br>85.64<br>66.53<br>59.78<br>72.02<br>77.59<br>71.04<br>**57.93**<br>OneVision-1.5-8B<br>74.19<br>74.59<br>60.59<br>53.26<br>72.62<br>74.14<br>67.76<br>52.80<br>Qwen2.5-VL-7B<br>65.05<br>68.51<br>50.42<br>57.61<br>60.71<br>68.39<br>61.20<br>45.67<br>32_k_-RAG<br>PersonaVLMSFT<br>67.20<br>70.17<br>49.58<br>57.07<br>70.24<br>80.46<br>64.84+3_._64<br>52.12+6_._45<br>PersonaVLMRL<br>69.89<br>76.80<br>58.05<br>**69.02**<br>**73.21**<br>**86.78**<br>71.48+10_._28<br>56.53+10_._86|Qwen2.5-VL-7B<br>PersonaVLMSFT<br>PersonaVLMRL|65.05<br>68.51<br>50.42<br>57.61<br>60.71<br>68.39<br>67.20<br>70.17<br>49.58<br>57.07<br>70.24<br>80.46<br>69.89<br>76.80<br>58.05<br>**69.02**<br>**73.21**<br>**86.78**|61.20<br>64.84+3_._64<br>71.48+10_._28|45.67<br>52.12+6_._45<br>56.53+10_._86|
|GPT-4o<br>**84.44**<br>75.63<br>59.12<br>55.65<br>65.98<br>76.64<br>69.23<br>45.32<br>128_k_-Full<br>Qwen2.5-VL-7B<br>50.60<br>54.73<br>52.41<br>54.30<br>55.83<br>60.90<br>54.48<br>3.08<br>InternVL3-8B<br>57.23<br>68.92<br>53.48<br>54.97<br>69.17<br>76.69<br>62.43<br>36.62<br>InternVL3-38B<br>67.47<br>71.62<br>**64.71**<br>58.94<br>65.00<br>76.69<br>67.18<br>46.56<br>OneVision-1.5-8B<br>52.44<br>54.79<br>58.15<br>45.33<br>65.25<br>67.18<br>56.66<br>14.28<br>Qwen2.5-VL-7B<br>56.63<br>63.51<br>50.27<br>55.63<br>61.67<br>70.68<br>59.01<br>37.88<br>128_k_-RAG<br>PersonaVLMSFT<br>67.47<br>75.68<br>59.36<br>51.66<br>71.67<br>81.95<br>67.18+8_._17<br>43.60+5_._72<br>PersonaVLMRL<br>69.28<br>**77.70**<br>61.50<br>**60.26**<br>**75.00**<br>**87.97**<br>**71.05**+12_._04<br>**47.28**+9_._4|GPT-4o<br>**84.44**<br>75.63<br>59.12<br>55.65<br>65.98<br>76.64<br>69.23<br>45.32<br>128_k_-Full<br>Qwen2.5-VL-7B<br>50.60<br>54.73<br>52.41<br>54.30<br>55.83<br>60.90<br>54.48<br>3.08<br>InternVL3-8B<br>57.23<br>68.92<br>53.48<br>54.97<br>69.17<br>76.69<br>62.43<br>36.62<br>InternVL3-38B<br>67.47<br>71.62<br>**64.71**<br>58.94<br>65.00<br>76.69<br>67.18<br>46.56<br>OneVision-1.5-8B<br>52.44<br>54.79<br>58.15<br>45.33<br>65.25<br>67.18<br>56.66<br>14.28<br>Qwen2.5-VL-7B<br>56.63<br>63.51<br>50.27<br>55.63<br>61.67<br>70.68<br>59.01<br>37.88<br>128_k_-RAG<br>PersonaVLMSFT<br>67.47<br>75.68<br>59.36<br>51.66<br>71.67<br>81.95<br>67.18+8_._17<br>43.60+5_._72<br>PersonaVLMRL<br>69.28<br>**77.70**<br>61.50<br>**60.26**<br>**75.00**<br>**87.97**<br>**71.05**+12_._04<br>**47.28**+9_._4|GPT-4o<br>**84.44**<br>75.63<br>59.12<br>55.65<br>65.98<br>76.64<br>69.23<br>45.32<br>128_k_-Full<br>Qwen2.5-VL-7B<br>50.60<br>54.73<br>52.41<br>54.30<br>55.83<br>60.90<br>54.48<br>3.08<br>InternVL3-8B<br>57.23<br>68.92<br>53.48<br>54.97<br>69.17<br>76.69<br>62.43<br>36.62<br>InternVL3-38B<br>67.47<br>71.62<br>**64.71**<br>58.94<br>65.00<br>76.69<br>67.18<br>46.56<br>OneVision-1.5-8B<br>52.44<br>54.79<br>58.15<br>45.33<br>65.25<br>67.18<br>56.66<br>14.28<br>Qwen2.5-VL-7B<br>56.63<br>63.51<br>50.27<br>55.63<br>61.67<br>70.68<br>59.01<br>37.88<br>128_k_-RAG<br>PersonaVLMSFT<br>67.47<br>75.68<br>59.36<br>51.66<br>71.67<br>81.95<br>67.18+8_._17<br>43.60+5_._72<br>PersonaVLMRL<br>69.28<br>**77.70**<br>61.50<br>**60.26**<br>**75.00**<br>**87.97**<br>**71.05**+12_._04<br>**47.28**+9_._4|GPT-4o<br>**84.44**<br>75.63<br>59.12<br>55.65<br>65.98<br>76.64<br>69.23<br>45.32<br>128_k_-Full<br>Qwen2.5-VL-7B<br>50.60<br>54.73<br>52.41<br>54.30<br>55.83<br>60.90<br>54.48<br>3.08<br>InternVL3-8B<br>57.23<br>68.92<br>53.48<br>54.97<br>69.17<br>76.69<br>62.43<br>36.62<br>InternVL3-38B<br>67.47<br>71.62<br>**64.71**<br>58.94<br>65.00<br>76.69<br>67.18<br>46.56<br>OneVision-1.5-8B<br>52.44<br>54.79<br>58.15<br>45.33<br>65.25<br>67.18<br>56.66<br>14.28<br>Qwen2.5-VL-7B<br>56.63<br>63.51<br>50.27<br>55.63<br>61.67<br>70.68<br>59.01<br>37.88<br>128_k_-RAG<br>PersonaVLMSFT<br>67.47<br>75.68<br>59.36<br>51.66<br>71.67<br>81.95<br>67.18+8_._17<br>43.60+5_._72<br>PersonaVLMRL<br>69.28<br>**77.70**<br>61.50<br>**60.26**<br>**75.00**<br>**87.97**<br>**71.05**+12_._04<br>**47.28**+9_._4|GPT-4o<br>**84.44**<br>75.63<br>59.12<br>55.65<br>65.98<br>76.64<br>69.23<br>45.32<br>128_k_-Full<br>Qwen2.5-VL-7B<br>50.60<br>54.73<br>52.41<br>54.30<br>55.83<br>60.90<br>54.48<br>3.08<br>InternVL3-8B<br>57.23<br>68.92<br>53.48<br>54.97<br>69.17<br>76.69<br>62.43<br>36.62<br>InternVL3-38B<br>67.47<br>71.62<br>**64.71**<br>58.94<br>65.00<br>76.69<br>67.18<br>46.56<br>OneVision-1.5-8B<br>52.44<br>54.79<br>58.15<br>45.33<br>65.25<br>67.18<br>56.66<br>14.28<br>Qwen2.5-VL-7B<br>56.63<br>63.51<br>50.27<br>55.63<br>61.67<br>70.68<br>59.01<br>37.88<br>128_k_-RAG<br>PersonaVLMSFT<br>67.47<br>75.68<br>59.36<br>51.66<br>71.67<br>81.95<br>67.18+8_._17<br>43.60+5_._72<br>PersonaVLMRL<br>69.28<br>**77.70**<br>61.50<br>**60.26**<br>**75.00**<br>**87.97**<br>**71.05**+12_._04<br>**47.28**+9_._4|
|GPT-4o<br>**84.44**<br>75.63<br>59.12<br>55.65<br>65.98<br>76.64<br>69.23<br>45.32<br>128_k_-Full<br>Qwen2.5-VL-7B<br>50.60<br>54.73<br>52.41<br>54.30<br>55.83<br>60.90<br>54.48<br>3.08<br>InternVL3-8B<br>57.23<br>68.92<br>53.48<br>54.97<br>69.17<br>76.69<br>62.43<br>36.62<br>InternVL3-38B<br>67.47<br>71.62<br>**64.71**<br>58.94<br>65.00<br>76.69<br>67.18<br>46.56<br>OneVision-1.5-8B<br>52.44<br>54.79<br>58.15<br>45.33<br>65.25<br>67.18<br>56.66<br>14.28<br>Qwen2.5-VL-7B<br>56.63<br>63.51<br>50.27<br>55.63<br>61.67<br>70.68<br>59.01<br>37.88<br>128_k_-RAG<br>PersonaVLMSFT<br>67.47<br>75.68<br>59.36<br>51.66<br>71.67<br>81.95<br>67.18+8_._17<br>43.60+5_._72<br>PersonaVLMRL<br>69.28<br>**77.70**<br>61.50<br>**60.26**<br>**75.00**<br>**87.97**<br>**71.05**+12_._04<br>**47.28**+9_._4|GPT-4o<br>**84.44**<br>75.63<br>59.12<br>55.65<br>65.98<br>76.64<br>69.23<br>45.32<br>128_k_-Full<br>Qwen2.5-VL-7B<br>50.60<br>54.73<br>52.41<br>54.30<br>55.83<br>60.90<br>54.48<br>3.08<br>InternVL3-8B<br>57.23<br>68.92<br>53.48<br>54.97<br>69.17<br>76.69<br>62.43<br>36.62<br>InternVL3-38B<br>67.47<br>71.62<br>**64.71**<br>58.94<br>65.00<br>76.69<br>67.18<br>46.56<br>OneVision-1.5-8B<br>52.44<br>54.79<br>58.15<br>45.33<br>65.25<br>67.18<br>56.66<br>14.28<br>Qwen2.5-VL-7B<br>56.63<br>63.51<br>50.27<br>55.63<br>61.67<br>70.68<br>59.01<br>37.88<br>128_k_-RAG<br>PersonaVLMSFT<br>67.47<br>75.68<br>59.36<br>51.66<br>71.67<br>81.95<br>67.18+8_._17<br>43.60+5_._72<br>PersonaVLMRL<br>69.28<br>**77.70**<br>61.50<br>**60.26**<br>**75.00**<br>**87.97**<br>**71.05**+12_._04<br>**47.28**+9_._4|50.60<br>54.73<br>52.41<br>54.30<br>55.83<br>60.90<br>57.23<br>68.92<br>53.48<br>54.97<br>69.17<br>76.69<br>67.47<br>71.62<br>**64.71**<br>58.94<br>65.00<br>76.69<br>52.44<br>54.79<br>58.15<br>45.33<br>65.25<br>67.18|54.48<br>62.43<br>67.18<br>56.66|3.08<br>36.62<br>46.56<br>14.28|
|GPT-4o<br>**84.44**<br>75.63<br>59.12<br>55.65<br>65.98<br>76.64<br>69.23<br>45.32<br>128_k_-Full<br>Qwen2.5-VL-7B<br>50.60<br>54.73<br>52.41<br>54.30<br>55.83<br>60.90<br>54.48<br>3.08<br>InternVL3-8B<br>57.23<br>68.92<br>53.48<br>54.97<br>69.17<br>76.69<br>62.43<br>36.62<br>InternVL3-38B<br>67.47<br>71.62<br>**64.71**<br>58.94<br>65.00<br>76.69<br>67.18<br>46.56<br>OneVision-1.5-8B<br>52.44<br>54.79<br>58.15<br>45.33<br>65.25<br>67.18<br>56.66<br>14.28<br>Qwen2.5-VL-7B<br>56.63<br>63.51<br>50.27<br>55.63<br>61.67<br>70.68<br>59.01<br>37.88<br>128_k_-RAG<br>PersonaVLMSFT<br>67.47<br>75.68<br>59.36<br>51.66<br>71.67<br>81.95<br>67.18+8_._17<br>43.60+5_._72<br>PersonaVLMRL<br>69.28<br>**77.70**<br>61.50<br>**60.26**<br>**75.00**<br>**87.97**<br>**71.05**+12_._04<br>**47.28**+9_._4|Qwen2.5-VL-7B<br>PersonaVLMSFT<br>PersonaVLMRL|56.63<br>63.51<br>50.27<br>55.63<br>61.67<br>70.68<br>67.47<br>75.68<br>59.36<br>51.66<br>71.67<br>81.95<br>69.28<br>**77.70**<br>61.50<br>**60.26**<br>**75.00**<br>**87.97**|59.01<br>67.18+8_._17<br>**71.05**+12_._04|37.88<br>43.60+5_._72<br>**47.28**+9_._4|



Wins Ties Loses



5.0% 16.0%



2.5%

5.0%


7.5%8.5%



PersonaVLM vs. Qwen2.5-VL-7B


PersonaVLM vs. InternVL3-8B


PersonaVLM vs. GPT-4o



92.5%


84.0%


79.0%


|Persona-MME P-SOUPS<br>Model<br>32k 128k Expertise Informativeness Style Overall|Col2|Col3|
|---|---|---|
|Qwen2.5-VL-7B<br>InternVL3-8B<br>InternVL3-38B<br>Qwen3-30B-A3B|69.91<br>52.27<br>55.75<br>55.56<br>64.60<br>63.01<br>80.09<br>83.06|39.00<br>49.34<br>23.00<br>37.11<br>47.16<br>51.81<br>26.16<br>41.71<br>**52.80**<br>53.30<br>32.83<br>46.32<br>51.67<br>**54.60**<br>35.16<br>47.14|



Figure 5. Qualitative comparison on open-ended generation, evaluated by Gemini-2.5-Pro. The evaluation assesses both the factual
accuracy and the personality alignment of the responses.


Appendix Fig. 10 for more comparisons with leading models.

Compared to strong open-source models of a similar size,
such as InternVL3-8B and LLaVA-OneVision-1.5-8B (provided with full context), PersonaVLM shows improvements
of 8.62% and 14.39% on Persona-MME in the 128 _k_ setting, respectively. While the personalization capabilities
of these open-source models appear to improve with scale,
PersonaVLM still outperforms the much larger InternVL338B by 3.87% on Persona-MME (128 _k_ ). We also evaluate
Qwen2.5-VL-7B augmented with a straightforward RAG
setup, which retrieves the top five most relevant messages
following the approach of [14]. Interestingly, the results
show that RAG can be detrimental in short-context scenarios—degrading performance on preference understanding
tasks by as much as 9.33%—while providing a substantial
boost of 4.53% in long-context settings. Additionally, as
shown in Table 1, the two-stage training process demonstrates clear effectiveness, yielding an average improvement
of 5.35% on Persona-MME.

When benchmarked against the proprietary GPT-4o, our



Table 2. Evaluation of personalized alignment on the PersonaMME and P-SOUPS benchmarks.


_baseline with different strategies_

|Self-Critic<br>Few-Shot|59.73 57.66<br>- -|39.67 49.33 23.67 37.50<br>42.16 48.66 28.33 39.67|
|---|---|---|
|PersonaVLM (ours)|**89.16**<br>**92.22**|51.16<br>53.65<br>**44.00**<br>**49.60**|



method achieves competitive results on Persona-MME and
demonstrates notable improvements of 17.3% and 2.0% on
the 32 _k_ and 128 _k_ configurations of PERSONAMEM, respectively. Furthermore, while PersonaVLM’s performance
in memory recall lags behind that of GPT-4o with full context—a finding consistent with [18]—it demonstrates a significant advantage elsewhere. In particular, in Growth Modeling and Behavioral Awareness, PersonaVLM outperforms
GPT-4o by over 10%.


**5.2. Personalized Alignment Evaluation**


For RQ2, we conduct experiments on two benchmarks:
the Alignment sub-task within Persona-MME and the PSOUPS [13], which comprise 812 and 1,800 test cases, respectively. The former assesses a model’s ability to determine if a response aligns with a user’s personality inferred
from the conversational context. The latter evaluates personality alignment with a given user profile across three
dimensions: Expertise, Informativeness, and Style.
We quantitatively compare PersonaVLM against several
powerful open-source models, including InternVL3-8B/38B


**Relevant Historical Context** **Current Turn**



**User :** Thinking about that little train set from a while back... what color was the main
part of the engine? (2024-10-02 20:31) **Failed visual recall**



**Failed visual recall**



**Qwen2.5-VL :** The main part of the train set engine? Remember that rusty red.



old childhood thing… she’d lose herself
in it for hours... (2024-09-15 11:33)


**User :** My friend Bob
really enjoys playing
the guitar on Sunday
afternoons... (202510-12 16:22 ~~)~~


Low: Agreeableness, Extraversion
Moderately High: Neuroticism



**GPT-4o :** The main engine color was primarily green—a grounding hue amidst the rustic
rail chaos, perfect for stitching vintage texture into threads woven with nostalgia.

**PersonaVLM :** That engine’s a deep, moody green—like the kind of hue that’d hum
with your sister’s train set nostalgia and the Labyrinth’s gothic velvet vibes...



**PersonaVLM :** Your conscientious mind and pattern - seeking instinct? Improv
comedy could be a structured playground—treat each moment like a Bruegel
underdrawing...Worth a try… if you frame it as a controlled experiment...



**User :**



Weekend vibes are back—gotta see what he’s up to! Bet it’s
something fun! (2025-10-19 15:04 Sunday)



**Qwen2.5-VL :** The image shows a person taking a selfie with two black dogs. The
person appears to be making a playful gesture with their hand, and...



**Lacks personalization**



**GPT-4o :** It looks like there's a lot of joy and energy this weekend, surrounded by the
company of some adorable dogs. Spending time with pets can be a great way to relax..
**PersonaVLM :** Ohhh, that guitar + Sunday afternoon energy with Bob? Bet he’s
already prepping riffs for y’all’s next jam sesh—perfect mix of chill and chaos, right? �✨



**User :** I'm thinking of trying improv comedy. Given my personality, what's your take?
(2024-09-25 16:40)
**Qwen2.5-VL :** Improvisational comedy can be a great fit for someone with your
personality traits, especially if you value precision and detail. Here are... **Generic**
**GPT-4o :** Improv comedy could be a fascinating outlet for you—it’s about embracing
spontaneity and relinquishing control, which contrasts with ...



**Generic**



**Overly formulaic, tonally misaligned**



Figure 6. Qualitative comparison on open-ended generation tasks. Case studies demonstrate PersonaVLM’s superior capabilities in memory
recall, context integration, and personality alignment compared to the baseline and GPT-4o.



and Qwen3-30B-A3B [45], with the latter being noted for its
strong language capabilities. We also evaluate the baseline
model augmented with different strategies, such as SelfCritic and few-shot prompting [50]. As shown in Table 2,
PersonaVLM consistently outperforms existing models on
both benchmarks. Notably, it leads the next-best model by
9.16% on Persona-MME and 2.46% on P-SOUPS, representing a _>_ 12% gain over the baseline. Interestingly, languagecentric models (e.g., Qwen3-30B-A3B) exhibit stronger
alignment than multimodal counterparts like InternVL3-38B,
with a 20% margin on Persona-MME (128 _k_ ). These outcomes underscore PersonaVLM’s capacity for robust personality alignment.


**5.3. Qualitative Evaluation**


To address RQ3 on open-ended generation, we conduct an
automated evaluation using 200 questions randomly sampled
from Persona-MME. We benchmark PersonaVLM against
InternVL3-8B, Qwen2.5-VL-7B, and GPT-4o, employing
Gemini-2.5-Pro [8] as an automated judge. Responses are assessed on two criteria: Accuracy and Personality Alignment,
with PersonaVLM’s performance in pairwise comparisons
classified as a “win,” “tie,” or “loss.” The evaluation prompt
is provided in Fig. 23. As illustrated in Fig. 5, PersonaVLM
achieves a substantially higher win rate than its peers. Particularly striking is its head-to-head performance against



GPT-4o, where PersonaVLM secures a 79% win rate versus
a 16% loss rate. This is further corroborated by qualitative case studies in Fig. 6, which showcase PersonaVLM’s
ability to perform accurate visual recall, integrate contextual memory, and maintain long-term personality alignment.
In contrast, other models exhibit critical failures, such as
memory hallucinations or tonally misaligned responses that
ignore user-specific memories. These findings validate the
generative capabilities of PersonaVLM for long-term personalization.


**6. CONCLUSION**


This paper introduces PersonaVLM, a novel agent framework that enables long-term, dynamic personalization for
MLLMs by integrating three core capabilities: Remembering, Reasoning, and Response Alignment. To support rigorous evaluation, we further propose Persona-MME, a comprehensive benchmark for personalized multimodal understanding. Experiments show that PersonaVLM significantly
enhances a model’s personalization capabilities and consistently outperforms strong counterparts, including both
proprietary GPT-4o and leading open-source alternatives.
Our work provides a new paradigm for developing truly
user-centric AI assistants, and future work will extend these
capabilities toward a fully immersive multimodal experience.


**References**


[1] Josh Achiam, Steven Adler, Sandhini Agarwal, Lama Ahmad,
Ilge Akkaya, Florencia Leoni Aleman, Diogo Almeida, Janko
Altenschmidt, Sam Altman, Shyamal Anadkat, et al. Gpt-4
technical report. _arXiv:2303.08774_, 2023.

[2] Yuval Alaluf, Elad Richardson, Sergey Tulyakov, Kfir Aberman, and Daniel Cohen-Or. Myvlm: Personalizing vlms for
user-specific queries. In _ECCV_, 2024.

[3] Rawan AlSaad, Alaa Abd-Alrazaq, Sabri Boughorbel, Arfan
Ahmed, Max-Antoine Renault, Rafat Damseh, and Javaid
Sheikh. Multimodal large language models in health care: applications, challenges, and future outlook. _Journal of medical_
_Internet research_, 2024.

[4] Xiang An, Yin Xie, Kaicheng Yang, Wenkang Zhang,
Xiuwei Zhao, Zheng Cheng, Yirui Wang, Songcen Xu,
Changrui Chen, Chunsheng Wu, et al. Llava-onevision-1.5:
Fully open framework for democratized multimodal training.
_arXiv:2509.23661_, 2025.

[5] Shuai Bai, Keqin Chen, Xuejing Liu, Jialin Wang, Wenbin
Ge, Sibo Song, Kai Dang, Peng Wang, Shijie Wang, Jun Tang,
et al. Qwen2. 5-vl technical report. _arXiv:2502.13923_, 2025.

[6] Jin Chen, Zheng Liu, Xu Huang, Chenwang Wu, Qi Liu,
Gangwei Jiang, Yuanhao Pu, Yuxuan Lei, Xiaolong Chen,
Xingmei Wang, et al. When large language models meet
personalization: Perspectives of challenges and opportunities.
_World Wide Web_, 2024.

[7] Prateek Chhikara, Dev Khant, Saket Aryan, Taranjeet Singh,
and Deshraj Yadav. Mem0: Building production-ready ai
agents with scalable long-term memory. _arXiv:2504.19413_,
2025.

[8] Gheorghe Comanici, Eric Bieber, Mike Schaekermann, Ice
Pasupat, Noveen Sachdeva, Inderjit Dhillon, Marcel Blistein, Ori Ram, Dan Zhang, Evan Rosen, et al. Gemini 2.5:
Pushing the frontier with advanced reasoning, multimodality, long context, and next generation agentic capabilities.
_arXiv:2507.06261_, 2025.

[9] Tao Ge, Xin Chan, Xiaoyang Wang, Dian Yu, Haitao Mi, and
Dong Yu. Scaling synthetic data creation with 1,000,000,000
personas. _arXiv:2406.20094_, 2024.

[10] Daya Guo, Dejian Yang, Haowei Zhang, Junxiao Song,
Ruoyu Zhang, Runxin Xu, Qihao Zhu, Shirong Ma, Peiyi
Wang, Xiao Bi, et al. Deepseek-r1: Incentivizing reasoning capability in llms via reinforcement learning. _arXiv:2501.12948_,
2025.

[11] Haoran Hao, Jiaming Han, Changsheng Li, Yu-Feng Li, and
Xiangyu Yue. Rap: Retrieval-augmented personalization for
multimodal large language models. In _CVPR_, 2025.

[12] Aaron Hurst, Adam Lerer, Adam P Goucher, Adam Perelman, Aditya Ramesh, Aidan Clark, AJ Ostrow, Akila Welihinda, Alan Hayes, Alec Radford, et al. Gpt-4o system card.
_arXiv:2410.21276_, 2024.

[13] Joel Jang, Seungone Kim, Bill Yuchen Lin, Yizhong Wang,
Jack Hessel, Luke Zettlemoyer, Hannaneh Hajishirzi, Yejin
Choi, and Prithviraj Ammanabrolu. Personalized soups: Personalized large language model alignment via post-hoc parameter merging. _arXiv:2310.11564_, 2023.




[14] Bowen Jiang, Zhuoqun Hao, Young-Min Cho, Bryan Li, Yuan
Yuan, Sihao Chen, Lyle Ungar, Camillo J Taylor, and Dan
Roth. Know me, respond to me: Benchmarking llms for
dynamic user profiling and personalized responses at scale.
_arXiv:2504.14225_, 2025.

[15] Bowen Jin, Hansi Zeng, Zhenrui Yue, Jinsung Yoon, Sercan
Arik, Dong Wang, Hamed Zamani, and Jiawei Han. Searchr1: Training llms to reason and leverage search engines with
reinforcement learning. _arXiv:2503.09516_, 2025.

[16] Oliver P John, Sanjay Srivastava, et al. The big-five trait taxonomy: History, measurement, and theoretical perspectives.
1999.

[17] Jeff Johnson, Matthijs Douze, and Hervé Jégou. Billion-scale
similarity search with gpus. _IEEE Transactions on Big Data_,
2019.

[18] Jiazheng Kang, Mingming Ji, Zhe Zhao, and Ting Bai. Memory os of ai agent. 2025.

[19] Chunyuan Li, Zhe Gan, Zhengyuan Yang, Jianwei Yang, Linjie Li, Lijuan Wang, Jianfeng Gao, et al. Multimodal foundation models: From specialists to general-purpose assistants.
_Foundations and Trends® in Computer Graphics and Vision_,
2024.

[20] Hao Li, Chenghao Yang, An Zhang, Yang Deng, Xiang Wang,
and Tat-Seng Chua. Hello again! llm-powered personalized
agent for long-term dialogue. _arXiv:2406.05925_, 2024.

[21] Jia-Nan Li, Jian Guan, Songhao Wu, Wei Wu, and Rui Yan.
From 1,000,000 users to every user: Scaling up personalized
preference for user-level alignment. _arXiv:2503.15463_, 2025.

[22] Zhiyu Li, Shichao Song, Chenyang Xi, Hanyu Wang, Chen
Tang, Simin Niu, Ding Chen, Jiawei Yang, Chunyu Li,
Qingchen Yu, et al. Memos: A memory os for ai system.
_arXiv:2507.03724_, 2025.

[23] Haotian Liu, Chunyuan Li, Qingyang Wu, and Yong Jae Lee.
Visual instruction tuning. In _NeurIPS_, 2023.

[24] Jiahong Liu, Zexuan Qiu, Zhongyang Li, Quanyu Dai,
Wenhao Yu, Jieming Zhu, Minda Hu, Menglin Yang, TatSeng Chua, and Irwin King. A survey of personalized
large language models: Progress and future directions.
_arXiv:2502.11528_, 2025.

[25] Shilong Liu, Zhaoyang Zeng, Tianhe Ren, Feng Li, Hao
Zhang, Jie Yang, Qing Jiang, Chunyuan Li, Jianwei Yang,
Hang Su, et al. Grounding dino: Marrying dino with grounded
pre-training for open-set object detection. In _ECCV_, 2024.

[26] Lin Long, Yichen He, Wentao Ye, Yiyuan Pan, Yuan Lin,
Hang Li, Junbo Zhao, and Wei Li. Seeing, listening, remembering, and reasoning: A multimodal agent with long-term
memory. _arXiv:2508.09736_, 2025.

[27] Xinbei Ma, Yeyun Gong, Pengcheng He, Hai Zhao, and Nan
Duan. Query rewriting in retrieval-augmented large language
models. In _EMNLP_, 2023.

[28] Thao Nguyen, Haotian Liu, Yuheng Li, Mu Cai, Utkarsh Ojha,
and Yong Jae Lee. Yo’llava: Your personalized language and
vision assistant. In _NeurIPS_, 2024.

[29] Yeongtak Oh, Jisoo Mok, Dohyun Chung, Juhyeon Shin,
Sangha Park, Johan Barthelemy, and Sungroh Yoon. Repic:
Reinforced post-training for personalizing multi-modal language models. _arXiv:2506.18369_, 2025.


[30] Long Ouyang, Jeffrey Wu, Xu Jiang, Diogo Almeida, Carroll Wainwright, Pamela Mishkin, Chong Zhang, Sandhini
Agarwal, Katarina Slama, Alex Ray, et al. Training language models to follow instructions with human feedback. In
_NeurIPS_, 2022.

[31] Charles Packer, Vivian Fang, Shishir_G Patil, Kevin Lin,
Sarah Wooders, and Joseph_E Gonzalez. Memgpt: Towards
llms as operating systems. _arXiv:2310.08560_, 2023.

[32] Renjie Pi, Jianshu Zhang, Tianyang Han, Jipeng Zhang, Rui
Pan, and Tong Zhang. Personalized visual instruction tuning.
_arXiv:2410.07113_, 2024.

[33] Alec Radford, Jong Wook Kim, Chris Hallacy, Aditya
Ramesh, Gabriel Goh, Sandhini Agarwal, Girish Sastry,
Amanda Askell, Pamela Mishkin, Jack Clark, et al. Learning
transferable visual models from natural language supervision.
In _ICML_, 2021.

[34] Rafael Rafailov, Archit Sharma, Eric Mitchell, Christopher D
Manning, Stefano Ermon, and Chelsea Finn. Direct preference optimization: Your language model is secretly a reward
model. In _NeurIPS_, 2023.

[35] Sonia Roccas, Lilach Sagiv, Shalom H Schwartz, and Ariel
Knafo. The big five personality factors and personal values.
_Personality and social psychology bulletin_, 2002.

[36] John Schulman, Filip Wolski, Prafulla Dhariwal, Alec Radford, and Oleg Klimov. Proximal policy optimization algorithms. _arXiv:1707.06347_, 2017.

[37] Zhaoxuan Tan, Qingkai Zeng, Yijun Tian, Zheyuan Liu,
Bing Yin, and Meng Jiang. Democratizing large language models via personalized parameter-efficient fine-tuning.
_arXiv:2402.04401_, 2024.

[38] Qi Wang, Jindong Li, Shiqi Wang, Qianli Xing, Runliang Niu,
He Kong, Rui Li, Guodong Long, Yi Chang, and Chengqi
Zhang. Towards next-generation llm-based recommender
systems: A survey and beyond. _arXiv:2410.19744_, 2024.

[39] Weizhi Wang, Li Dong, Hao Cheng, Xiaodong Liu, Xifeng
Yan, Jianfeng Gao, and Furu Wei. Augmenting language
models with long-term memory. In _NeurIPS_, 2023.

[40] Yu Wang and Xi Chen. Mirix: Multi-agent memory system
for llm-based agents. _arXiv:2507.07957_, 2025.

[41] Jiale Wei, Xiang Ying, Tao Gao, Fangyi Bao, Felix Tao,
and Jingbo Shang. Ai-native memory 2.0: Second me.
_arXiv:2503.08102_, 2025.

[42] Junda Wu, Hanjia Lyu, Yu Xia, Zhehao Zhang, Joe Barrow,
Ishita Kumar, Mehrnoosh Mirtaheri, Hongjie Chen, Ryan A
Rossi, Franck Dernoncourt, et al. Personalized multimodal
large language models: A survey. _arXiv:2412.02142_, 2024.

[43] Wujiang Xu, Kai Mei, Hang Gao, Juntao Tan, Zujie Liang,
and Yongfeng Zhang. A-mem: Agentic memory for llm
agents. _arXiv:2502.12110_, 2025.

[44] Zhenyu Xu, Hailin Xu, Zhouyang Lu, Yingying Zhao, Rui
Zhu, Yujiang Wang, Mingzhi Dong, Yuhu Chang, Qin Lv,
Robert P Dick, et al. Can large language models be good companions? an llm-based eyewear system with conversational
common ground. In _IMWUT_, 2024.

[45] An Yang, Anfeng Li, Baosong Yang, Beichen Zhang, Binyuan
Hui, Bo Zheng, Bowen Yu, Chang Gao, Chengen Huang,
Chenxu Lv, et al. Qwen3 technical report. _arXiv:2505.09388_,
2025.




[46] Yuan Yao, Tianyu Yu, Ao Zhang, Chongyi Wang, Junbo Cui,
Hongji Zhu, Tianchi Cai, Haoyu Li, Weilin Zhao, Zhihui
He, et al. Minicpm-v: A gpt-4v level mllm on your phone.
_arXiv:2408.01800_, 2024.

[47] Shukang Yin, Chaoyou Fu, Sirui Zhao, Ke Li, Xing Sun,
Tong Xu, and Enhong Chen. A survey on multimodal large
language models. _National Science Review_, 2024.

[48] Jifan Yu, Zheyuan Zhang, Daniel Zhang-li, Shangqing Tu,
Zhanxin Hao, Rui Miao Li, Haoxuan Li, Yuanchun Wang,
Hanming Li, Linlu Gong, et al. From mooc to maic: Reshaping online teaching and learning through llm-driven agents.
_arXiv:2409.03512_, 2024.

[49] Zhehao Zhang, Ryan A Rossi, Branislav Kveton, Yijia Shao,
Diyi Yang, Hamed Zamani, Franck Dernoncourt, Joe Barrow, Tong Yu, Sungchul Kim, et al. Personalization of large
language models: A survey. _arXiv:2411.00027_, 2024.

[50] Siyan Zhao, Mingyi Hong, Yang Liu, Devamanyu Hazarika, and Kaixiang Lin. Do llms recognize your preferences? evaluating personalized preference following in llms.
_arXiv:2502.09597_, 2025.

[51] Jinguo Zhu, Weiyun Wang, Zhe Chen, Zhaoyang Liu, Shenglong Ye, Lixin Gu, Hao Tian, Yuchen Duan, Weijie Su,
Jie Shao, et al. Internvl3: Exploring advanced training
and test-time recipes for open-source multimodal models.
_arXiv:2504.10479_, 2025.

[52] Minjun Zhu, Yixuan Weng, Linyi Yang, and Yue Zhang. Personality alignment of large language models. In _ICLR_, 2025.

[53] Yuchen Zhuang, Haotian Sun, Yue Yu, Rushi Qiang, Qifan
Wang, Chao Zhang, and Bo Dai. Hydra: Model factorization
framework for black-box llm personalization. In _NeurIPS_,
2024.


#### **PersonaVLM: Long-Term Personalized Multimodal LLMs** Supplementary Material



This supplementary material provides comprehensive details
to complement the main paper, organized as follows:


- **Appendix A** elaborates on our proposed memory architecture, detailing each memory component—including its
storage, retrieval, and update processes.

- **Appendix B** outlines the training and implementation details of PersonaVLM framework.

- **Appendix C** presents a detailed analysis of our synthesized
dataset, covering its distribution and the validation process.

- **Appendix** **D** offers a comprehensive breakdown of
Persona-MME, including its task taxonomy, detailed statistical analysis, and full evaluation results.

- **Appendix E** presents additional experimental details, including ablation studies and the full set of prompts used
in our framework.

- **Appendix F** offers further efficiency analysis and limitations of PersonaVLM.


**A. Details of the PersonaVLM Memory Archi-**
**tecture**


As introduced in Section 3, the PersonaVLM memory architecture comprises two components: a User Personality
Profile ( _P_ ) and a Multi-Type Memory Database ( _M_ ). This
section provides a detailed exposition of how these memories
are stored, updated, and retrieved.


**A.1. Memory Storage**


**User Personality Profile (** _P_ **).** We quantitatively represent
the user’s personality as a five-dimensional vector, **p** _∈_ R [5],
where each element corresponds to a Big Five trait and is a
floating-point value between 1 and 5. This profile is dynamically updated after each interaction turn _m_ . Specifically,
at the end of a turn, the model infers a personality vector,
**p** _[′]_ _m_ _[∈]_ [R][5][, where each component is an integer score from]
1 to 5 based on the user’s current input and context. The
persistent personality profile **p** is then updated using an Exponential Moving Average (EMA): **p** _←_ _λm_ **p** +(1 _−λm_ ) **p** _[′]_ _m_
where the smoothing factor _λm_ is dynamically adjusted to be
more sensitive in early interactions and stabilize over time:
_λm_ = 0 _._ 7 _−_ 0 _._ 2 _·_ cos - min(50 _m,_ 50) _π_ - _._ To ensure stability,

this update is applied selectively. The process is skipped
if the inferred personality vector **p** _[′]_ _m_ [consists solely of the]
neutral score (3), a condition that typically arises in nonpersonalized or neutral contexts. During the response generation stage, the personality profile _P_ is provided to the
model via structured prompting.



**Core** **Memory.** Core memory stores the user’s foundational and high-priority attributes and is included in every
interaction turn. It is divided into two sub-components [31]:

- **Human:** Factual user attributes, such as age, gender, preferences, and interests, with the user’s name as a mandatory
field. This information provides PersonaVLM with a foundational understanding of the user’s background.

- **Persona:** The user’s identity, roles (e.g., “a meticulous
researcher”), and explicit requirements for the model’s
interaction style, tone, and behavior.


**Semantic Memory.** Semantic memory [40] archives timeless, multimodal knowledge that is either explicitly provided
by the user or autonomously inferred by the model. This
knowledge is categorized as follows:

- **Explicit Directives:** Direct commands from the user to
remember specific information, which can be textual or
visual. For example, a user might provide an image and
say, “Remember the boy in this picture.”

- **Core** **Facts:** Stable, factual information about the user
disclosed during conversation, such as their profession,
significant life events, or specific requirements for the
agent’s behavior.

- **Preferences & Habits:** User preferences for entities, visual styles, or activities, which can be either explicitly
stated or implicitly revealed through behavior patterns.

- **Visual Concepts:** User-specific visual concepts that arise
in multimodal dialogues, such as friends, pets, or personal
items. These are stored as a key-value pair linking a textual description to an image crop, formatted as “simple
description <image>”.
Beyond these predefined categories, the agent autonomously
determines at the end of each turn whether new semantic
knowledge warrants storage. If so, it generates a structured
output containing the reasoning process, memory content,
and a set of keywords for future retrieval.


**Episodic Memory.** Episodic memory archives both summaries and raw data from past conversations. For each multiturn dialogue session, the model segments the conversation
by topic. Each resulting topic-based episode contains three
key elements: (a) a concise summary, (b) a set of keywords,
and (c) the indices of the dialogue turns constituting that
episode. To ensure no details are lost, the original dialogue
data is never deleted; the episodic memory serves as a structured layer for organizing and retrieving this raw data.


**Procedural** **Memory.** Procedural memory tracks user
goals and identifies recurring behaviors or habits by stor

Distribution of SFT Data



Distribution of RL Data













**Algorithm 1** Operational Pipeline of PersonaVLM


**Input:** User query _Qm_ = ( _Tm, Im, tm_ ), personality profile
_Pm−_ 1, memory database _Mm−_ 1, max reasoning steps
_N_, model _πθ_, session threshold _ts_ .
1: **if** _tm −_ _tm−_ 1 _≥_ _ts_ **then**
2: Update Core, Procedural, and Episodic Memory
based on the last session.

3: **end if**
4: _Cm_ _←{_ ( _Qi, Ri_ ) _|_ 0 _< i < m_ and _|ti −_ _tm| ≤_ _ts}_
5: **for** _n_ = 1 to _N_ **do**
6: _Sn_ _←_ _πθ_ ( _Qm, Cm, Pm−_ 1)
7: `action` _,_ `args` _←_ Parse( _Sn_ )

8: **if** `action` = `retrieve` **then**
9: (keywords, time period) _←_ `args`
10: _M_ retrieved _←_ Retrieve( _Mm−_ 1
keywords, time period)
11: _Cm_ _←Cm ∪M_ retrieved
12: **else if** `action` = `answer` **then**

13: _Rm_ _←_ `args`
14: **break**
15: **end if**
16: **end for**
17: Infer turn-specific personality **p** _[′]_ _m_ [from] _[ Q][m]_ [and update]
long-term profile **p** _m_ .
18: Convert **p** _m_ to textual summary _Pm_ .

19: Extract and update Semantic Memory based on the current turn ( _Qm, Rm_ ).
**Output:** Final response _Rm_, updated state ( _Pm, Mm_ ).


mirrors the text-based semantic search, creating a unified
retrieval mechanism across modalities.


**A.3. Memory Management**


Our memory management policies distinguish between raw
conversational history and structured memory [43]. While
the complete interaction history is retained for low-level
access, the structured memories are managed according to
the following policies. Semantic and Episodic memory are
treated as purely additive; new entries detailing facts, concepts, or events are appended without modifying or deleting
existing ones, thereby preserving an immutable historical
record. In contrast, Core and Procedural memory maintain
a single, canonical version of the user’s profile and habits.
These memories are mutable and undergo CRUD operations
at the end of each session to ensure they accurately reflect
the user’s most current state.


**B. Implementation Details of PersonaVLM**


**B.1. Implementation Process**


The end-to-end operational pipeline of PersonaVLM is detailed in Algorithm 1. In our offline implementation, a new

















Figure 7. Data composition for the training of PersonaVLM


ing procedural events from conversations. It primarily stores
two types of information:

- **Long-term Goals:** Ongoing projects, plans, or objectives
that the user is working towards.

- **Habits & Routines:** Repetitive behaviors or workflows
that are automatically identified from user interactions.
Similar to Core Memory, this information is stored as keyvalue pairs, and only the latest version is retained.


**A.2. Memory Retrieval**


Memory retrieval is a critical step within the Response
Stage, initiated when PersonaVLM determines that external knowledge is necessary to fulfill a user’s request. The
process begins by generating a retrieval query encapsulated
within <retrieve></retrieve> tags. This specifies
a `time period` and `keywords` to guide the search. The
time period is defined by start and end timestamps in a
“ `YYYY` _−_ `MM` _−_ `DDHH` : `MM` ” format.


**Textual** **Memory** **Retrieval.** For text-based memories
(i.e., procedural, semantic, and episodic), we employ a
parallel multi-source retrieval strategy. First, all textual memories are encoded into dense vectors using the
all-MiniLM-L6-v2 sentence transformer [7] . Given a user
query, we perform a similarity search against the memory
database. The top- _k_ most relevant memories are retrieved
from each category, where _k_ is empirically set to 2, 4, and
2 for procedural, semantic, and episodic memories, respectively, unless otherwise specified. This entire process is
accelerated by leveraging Facebook AI Similarity Search
(FAISS) [17] for efficient indexing and retrieval.


**Visual Concept Retrieval.** This process is automatically
triggered when the user’s input contains an image. First,
we employ an off-the-shelf object detector, Grounding
DINO [25], to extract salient objects from the input image. We then compute the cosine similarity between the
CLIP [33] embeddings of these detected objects and the
visual concepts stored in semantic memory. This process


7https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2


Table 3. The hyperparameters used in SFT and RL training.


**Training stage**
**Hyperparameter**
**SFT** **RL**
Batch Size 64 72
Learning Rate 2e-5 2e-6
LR Scheduler cosine cosine
Total Steps 1200 400
Max Pixels 230400 230400
Max Length 16384 16384
Warmup Ratio 0.03 0.05
deepspeed zero3 zero3
Number of Samples in a Group  - 6
Num Iterations  - 1
Repetition Penalty  - 1.05


user session is initiated if the time elapsed since the last
interaction, _tm −_ _tm−_ 1, exceeds a predefined threshold _ts_
(e.g., 60 minutes). At the start of a new session, a memory
consolidation process is triggered to update the user’s longterm Core and Procedural memories based on the previous
session.


**B.2. Training Details**


**Training** **Data** **Composition.** The composition of our
training data for the SFT and RL stages is detailed in Fig. 7.
The SFT dataset comprises a total of 78 _k_ samples. This
dataset is constructed using the synthesis pipeline illustrated
in Fig. 3 (a) and is further augmented with 6 _k_ user-related
concept samples based on [11]. The SFT data is primarily
split between question-answering (QA) pairs for reasoning
(43.6%) and memory-related samples (56.4%). The memoryrelated category is further subdivided into a personality inference task (10.3%) and examples for the four memory types
(46.1%). In contrast, the RL dataset consists of 5.6 _k_ samples,
categorized into three types: open-ended QA with verifiable
answers (21.0%), multiple-choice questions (55.6%), and
binary-choice questions (23.4%).


**Implementation** **Details.** We implement our training
pipeline based on the repositories Qwen-VL [8] and ms-swift [9] .
The hyperparameter settings for both the SFT and RL stages
are detailed in Table 3. All experiments were conducted on
a server equipped with 8 NVIDIA H800 GPUs. The entire
two-stage training process completes in approximately 8
hours, comprising 2 hours for SFT and 6 hours for RL.


**Group Relative Policy Optimization.** GRPO [10] is an
advancement over PPO [36] that refines policy optimization


8https://github.com/QwenLM/Qwen3-VL
9https://github.com/modelscope/ms-swift




              -              clip( _ri_ _[t]_ [(] _[θ]_ [)] _[,]_ [ 1] _[ −]_ _[ϵ,]_ [ 1 +] _[ ϵ]_ [)] _[A]_ [ �] _i_ _[t]_ _−_ _β_ DKL( _πθ ∥_ _π_ ref) _._


(4)


where _ri_ _[t]_ [(] _[θ]_ [) =] _ππθθ_ old( _τ_ ( _τi,ti,t|τ|τi,<ti,<t_ )) [is the probability ratio,] _[ π]_ [ref][ is a]
reference policy, and _β_ is a hyperparameter that controls the
strength of the KL regularization. Detailed training settings
are provided in Table 3.


**Optimization** **Strategies.** To improve the effectiveness
and robustness of our retrieval mechanism, we implement
several optimization strategies.
First, to mitigate retrieval redundancy within a single reasoning trajectory, the model is encouraged to use diverse
query conditions (i.e., keywords and time periods). We
enforce this by implementing a deduplication filter that prevents any single memory entry from being retrieved more
than once per trajectory.
Second, we employ a dynamic top- _k_ strategy during training to better prepare the model for varied information scenarios. Specifically, while we use fixed top- _k_ values at inference
(2 for episodic and 4 for semantic memories), these values
are randomized during training, sampled uniformly from the
ranges [2, 5] and [3, 6], respectively. This approach acts as a
form of data augmentation, training the model to be robust
to both sparse and dense information retrieval contexts.


**C. Data Curation Details.**


**Data Distribution.** We synthesize a large-scale, long-term
multimodal dialogue dataset by sampling 700 unique personas from PersonaHub [9], allocating 500 for training and
200 for testing. The detailed distribution of the synthesized
data is visualized in Fig. 8 and the top-right panel of Fig. 3.
Training dialogues consist of 20 to 100 turns, spanning a
simulated timeframe of up to one month. In contrast, test
dialogues are designed to be more challenging, featuring



by replacing the critic model with a relative evaluation mechanism. Instead of learning an absolute value function, GRPO
estimates advantages by comparing the quality of multiple
trajectories sampled within a group. For each training sample _{Q,_ _R}_, where _Q_ is the user input and _R_ is the preferred

[�] [�]
response, the policy model _πθ_ rollouts a group of multi-turn
trajectories _{τ_ 1 _, . . ., τG}_ . The reward for each trajectory _τi_
is calculated using Eq. (3). Based on these rewards, we then
compute the normalized advantage _A_ [�] _[t]_ _i_ [for each token by nor-]
malizing them across the sampled group. The optimization
objective is:



_L_ GRPO( _θ_ ) = E( _Q,_ - _R_ ) _∼D,{τi}_ _[G]_ _i_ =1 _[∼][π][θ]_ old [(] _[·|Q]_ [)]




 [1]

_G_



_G_




_i_ =1



_|τi|_





- min - _ri_ _[t]_ [(] _[θ]_ [)][ �] _[A][t]_ _i_ _[,]_

_t_ =1



1
_|τi|_


rule-based checks that validate data integrity, including the
chronological consistency of timestamps and the completeness of episodic dialogues. Concurrently, a model-based selfcorrection mechanism verifies the safety and coherence of
the generated content. Second, the automatically filtered data
undergoes a human review. In this final step, human reviewers are tasked with identifying and removing any remaining
erroneous, nonsensical, or repetitive dialogues, ensuring the
final dataset is of high fidelity.


**D. Persona-MME: Details and Statistics**


**Task Taxonomy.** We provide the definitions for evaluated
tasks in Table 5 and present illustrative examples in Fig. 9.


**Data** **Statistics** **and** **Distribution.** Persona-MME is designed to evaluate long-term personalization across seven
key aspects, encompassing a total of 14 fine-grained tasks
and comprising **2,034** _in-situ_ test cases. It is important to
note that a single test scenario may simultaneously assess
multiple capabilities. Fig. 11 illustrates the distribution of
these tasks. The benchmark consists of 13 primary tasks
(from Visual Detail Recall to Generalizing to New Scenarios), which are distributed relatively evenly. The 14th task,
personality alignment, is not a standalone category but is
evaluated concurrently within 406 of the primary task cases.
The diversity of our evaluation set is a core design principle. We constructed **200** unique personas, each with a
distinct fictional background, and crafted dialogues that span
a broad spectrum of topics and scenarios to ensure comprehensive testing. The resulting topical breadth is visualized in
Figure 12, which presents a word cloud of the most prominent keywords from the evaluation dialogues.
Further statistical analysis of Persona-MME is presented
in Table 6. On average, each _in-situ_ test case is grounded in
a conversational history of **142.9 turns**, of which **15.87%**
are multimodal. The average length of a test question is
**22.7 words**, while the average answer length is **3.05 words** .
A significant portion of questions, **34.02%**, require visual
information from the context to be answered correctly.


**Comprehensive Evaluation.** We present a comprehensive
evaluation of over ten leading models on the 128 _k_ configuration of Persona-MME, with detailed results provided in
Table 4 and Fig. 10. The evaluation spans a range of proprietary models (e.g., GPT-4o, GPT-5, Gemini-2.5-Flash,
Claude-3.7-Sonnet) and open-source alternatives (e.g., the
Qwen series, InternVL3-8B/38B, OneVision-1.5-8B). Our
key findings are as follows:

- **Proprietary vs.** **Open-Source Gap:** Proprietary models
exhibit significantly better overall personalization capabilities than their open-source counterparts.

- **Challenges** **for** **Smaller** **and** **Multimodal** **Models:**
Smaller open-source multimodal models, such as



60

50

40

30

20

10

0



|Col1|Col2|Col3|Col4|Col5|Col6|Col7|Col8|Col9|Col10|
|---|---|---|---|---|---|---|---|---|---|
|||||||||||
|||||||||||
|||||||||||
|||||||||||
|||||||||||
|||||||||||


Dialogue Turns



35


30


25


20


15


10


5



Figure 8. Distribution of the 500 long-term conversation samples
in the training data.


longer conversations in two settings: 20–100 turns (for a
32 _k_ context window) and 100–500 turns (for a 128 _k_ context
window), with a simulated duration of up to three months.
This designed discrepancy between training and testing data
allows for a rigorous evaluation of our memory architecture’s
long-term capabilities.
It is important to note a distinction in how the dialogue
data is utilized: the full, synthesized multi-turn dialogues
serve as the database for retrieval, while the QA pairs used
for model training feature re-generated answers. This is
because the original answers have access to the complete
dialogue history, whereas the training target must be an
answer generated solely based on the current query and the
retrieved memory content.


**Multimodal** **Memory** **Formatting.** To support multimodal knowledge, visual concepts in semantic memory are
stored in a structured format: “Memory Content (Image Object: <class_name>)”. During the memory update process,
Grounding DINO [25] is used to crop the corresponding
object from the image. This cropped image patch is then
paired with a simple textual description forming the input
format for the model, i.e., “simple description <image>”.
Crucially, the system distinguishes between concrete visual objects and abstract preferences. For instance, if a user
states, “I like this style of picture,” the system stores a textual
fact, such as “User likes [style description],” rather than the
raw image or its constituent objects. Also, episodic memory retains the original multimodal dialogue turns, including
both text and full images, to preserve memory integrity.


**Data Validation.** To ensure the accuracy, safety, and overall quality of our synthesized dataset, we employ a twostage filtering process. First, we perform automated filtering
using both rule-based checks and model-based validation.
During data synthesis, the generation model outputs structured metadata, such as timestamps and dialogue turn indices for episodic topics. We leverage this metadata to apply


Recognition











**Interest**
**Evolution**

**Analysis**













Figure 9. Illustrative in-situ cases for the 14 task categories in Persona-MME, organized into the seven core personalization aspects.


Table 4. Comprehensive evaluation on the 128 _k_ configuration of Persona-MME. We compare PersonaVLM with proprietary and opensource models across 14 tasks: Visual Detail Recall (VDR), Semantic Information Recall (SIR), Explicit Intent Inference (EII), Implicit
Intent Recognition (IIR), Latest Preference Recognition (LPR), Interest Evolution Analysis (IEA), Implicit Preference Recommendation
(IPR), Behavioral Pattern Recognition (BPR), Long-term Goal Tracking (LGT), Relationship Recognition (RR), Relationship Dynamics
Comprehension (RDC), Tiered Explanation Delivery (TED), Generalizing to New Scenarios (GNS), and Personality Alignment (PA).

|Model|Memory Intent Preference Behavior Relationship Growth Alignment<br>Overall<br>VDR SIR EII IIR LPR IEA IPR BPR LGT RR RDC TED GNS PA|Col3|Col4|Col5|Col6|Col7|Col8|Col9|
|---|---|---|---|---|---|---|---|---|
|Random|25.00<br>25.00|25.00<br>25.00|25.00<br>25.00<br>25.00|25.00<br>25.00|25.00<br>25.00|25.00<br>25.00|50.00|32.11|



_Proprietary models_
GPT-4o-mini 54.39 89.74 78.46 64.81 64.58 59.68 61.22 68.33 45.31 54.17 71.43 73.33 75.81 65.14 66.44
GPT-4o 73.68 92.31 86.15 62.96 62.50 54.84 61.22 61.67 50.0 56.25 75.51 73.33 79.03 78.87 71.90
GPT-5 85.71 **98.72** **93.85** 67.92 **74.47** **70.97** 65.31 **76.67** **70.97** **85.11** **81.63** 76.19 75.81 **92.25** **82.95**
Gemini-2.5-Flash **88.06** 92.55 88.00 73.44 67.86 47.89 50.00 62.5 58.33 72.22 77.19 75.00 80.00 80.90 74.90
Claude-3.7-Sonnet 51.47 91.11 80.26 **76.19** 60.38 61.43 61.54 61.97 38.24 64.81 66.67 66.67 70.42 80.65 70.40


_Open-source models_


|Qwen2.5-VL-7B<br>InternVL3-8B<br>InternVL3-38B<br>Qwen3-VL-8B<br>Qwen3-30B-A3B<br>OneVision-1.5-8B|52.11 49.47<br>29.58 77.89<br>38.03 89.47<br>63.38 84.21<br>29.58 85.26<br>42.86 59.57|52.44 57.58<br>74.39 62.12<br>78.05 63.64<br>76.83 68.18<br>82.93 75.76<br>59.26 49.23|52.63 48.65 57.14<br>59.65 54.05 46.43<br>68.42 64.86 60.71<br>61.4 58.11 67.86<br>70.18 63.51 64.29<br>62.5 46.58 69.09|55.84 52.7<br>66.23 43.24<br>72.73 44.59<br>67.53 40.54<br>63.64 44.59<br>48.68 41.89|50.88 60.32<br>61.40 76.19<br>57.89 71.43<br>82.46 76.19<br>68.42 77.78<br>73.21 58.06|56.9 64.0<br>75.86 77.33<br>70.69 81.33<br>79.31 88.00<br>82.76 86.67<br>64.91 68.92|55.0<br>54.17<br>63.06<br>71.39<br>81.39<br>53.93|54.62<br>60.08<br>66.01<br>70.75<br>72.65<br>55.88|
|---|---|---|---|---|---|---|---|---|
|PersonaVLM (ours)|50.70<br>83.16|81.71<br>72.73|59.65<br>54.05<br>**73.21**|58.44<br>62.16|75.44<br>74.60|**82.76**<br>**92.00**|92.22|77.08|



Qwen2.5-VL-7B, InternVL3-8B, and OneVision-1.5-8B,
particularly struggle with personality alignment, with their
performance often being comparable to a random baseline.



In contrast, large language-centric models like Qwen330B-A3B can achieve superior overall scores, outperforming even larger multimodal models like InternVL3-38B,


80


60


40


20

















0

|82.95|Col2|Col3|Col4|Col5|Col6|Col7|Col8|Col9|Col10|Col11|Col12|Col13|Col14|Col15|Col16|Col17|Col18|Col19|Col20|Col21|Col22|Col23|Col24|Col25|Col26|Col27|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|82.95<br>|||||||||||||||||||||||||||
|||~~77.08~~<br>74.90<br>72.65<br>71.90<br>70.75<br>70.40<br>66.44<br>66.01<br>60.08<br>|~~77.08~~<br>74.90<br>72.65<br>71.90<br>70.75<br>70.40<br>66.44<br>66.01<br>60.08<br>|~~77.08~~<br>74.90<br>72.65<br>71.90<br>70.75<br>70.40<br>66.44<br>66.01<br>60.08<br>|~~77.08~~<br>74.90<br>72.65<br>71.90<br>70.75<br>70.40<br>66.44<br>66.01<br>60.08<br>|~~77.08~~<br>74.90<br>72.65<br>71.90<br>70.75<br>70.40<br>66.44<br>66.01<br>60.08<br>|~~77.08~~<br>74.90<br>72.65<br>71.90<br>70.75<br>70.40<br>66.44<br>66.01<br>60.08<br>|~~77.08~~<br>74.90<br>72.65<br>71.90<br>70.75<br>70.40<br>66.44<br>66.01<br>60.08<br>|~~77.08~~<br>74.90<br>72.65<br>71.90<br>70.75<br>70.40<br>66.44<br>66.01<br>60.08<br>|~~77.08~~<br>74.90<br>72.65<br>71.90<br>70.75<br>70.40<br>66.44<br>66.01<br>60.08<br>|~~77.08~~<br>74.90<br>72.65<br>71.90<br>70.75<br>70.40<br>66.44<br>66.01<br>60.08<br>|~~77.08~~<br>74.90<br>72.65<br>71.90<br>70.75<br>70.40<br>66.44<br>66.01<br>60.08<br>|~~77.08~~<br>74.90<br>72.65<br>71.90<br>70.75<br>70.40<br>66.44<br>66.01<br>60.08<br>|~~77.08~~<br>74.90<br>72.65<br>71.90<br>70.75<br>70.40<br>66.44<br>66.01<br>60.08<br>|~~77.08~~<br>74.90<br>72.65<br>71.90<br>70.75<br>70.40<br>66.44<br>66.01<br>60.08<br>|~~77.08~~<br>74.90<br>72.65<br>71.90<br>70.75<br>70.40<br>66.44<br>66.01<br>60.08<br>|~~77.08~~<br>74.90<br>72.65<br>71.90<br>70.75<br>70.40<br>66.44<br>66.01<br>60.08<br>|~~77.08~~<br>74.90<br>72.65<br>71.90<br>70.75<br>70.40<br>66.44<br>66.01<br>60.08<br>|~~77.08~~<br>74.90<br>72.65<br>71.90<br>70.75<br>70.40<br>66.44<br>66.01<br>60.08<br>|~~77.08~~<br>74.90<br>72.65<br>71.90<br>70.75<br>70.40<br>66.44<br>66.01<br>60.08<br>|~~77.08~~<br>74.90<br>72.65<br>71.90<br>70.75<br>70.40<br>66.44<br>66.01<br>60.08<br>|~~77.08~~<br>74.90<br>72.65<br>71.90<br>70.75<br>70.40<br>66.44<br>66.01<br>60.08<br>|~~77.08~~<br>74.90<br>72.65<br>71.90<br>70.75<br>70.40<br>66.44<br>66.01<br>60.08<br>|~~77.08~~<br>74.90<br>72.65<br>71.90<br>70.75<br>70.40<br>66.44<br>66.01<br>60.08<br>|~~77.08~~<br>74.90<br>72.65<br>71.90<br>70.75<br>70.40<br>66.44<br>66.01<br>60.08<br>|~~77.08~~<br>74.90<br>72.65<br>71.90<br>70.75<br>70.40<br>66.44<br>66.01<br>60.08<br>|
|||~~77.08~~<br>74.90<br>72.65<br>71.90<br>70.75<br>70.40<br>66.44<br>66.01<br>60.08<br>|||||||||||||||||||||||||
|||~~77.08~~<br>74.90<br>72.65<br>71.90<br>70.75<br>70.40<br>66.44<br>66.01<br>60.08<br>|||||||||||||||||||||||||
|||~~77.08~~<br>74.90<br>72.65<br>71.90<br>70.75<br>70.40<br>66.44<br>66.01<br>60.08<br>|||||||||||||||||||||||||
|||~~77.08~~<br>74.90<br>72.65<br>71.90<br>70.75<br>70.40<br>66.44<br>66.01<br>60.08<br>|||||||||||||||||||||||||
|||||||||||||||||||||55.88<br>54.62|55.88<br>54.62|55.88<br>54.62|55.88<br>54.62|55.88<br>54.62|55.88<br>54.62|55.88<br>54.62|
|||||||||||||||||||||55.88<br>54.62|||||||
|||||||||||||||||||||||||32.11|32.11|32.11|
|||||||||||||||||||||||||32.11|||
||||<br>||||||||||||||||||||||||



Figure 10. Overall performance on Persona-MME (128 _k_ ), ranking PersonaVLM against various proprietary and open-source models.



20%


18%


16%


14%


12%


10%


8%


6%


4%


2%


0%






































|Col1|Col2|Col3|Col4|Col5|Col6|Col7|Col8|Col9|Col10|Col11|Col12|Col13|Col14|Col15|Col16|Col17|Conte<br>32k|Col19|Col20|xt Lengt|Col22|Col23|h<br>128k|Col25|Col26|Col27|Col28|Col29|Col30|Col31|Col32|Col33|Col34|Col35|Col36|Col37|Col38|Col39|Col40|Col41|Col42|Col43|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|||||||||||||||||||||||||||||||||||||||226|226|226|180|180|
|||||||||||||||||||||||||||||||||||||||226|226||||
||||||||||||||||||||||||||||||||||||||||||||
||||||||||||||||||||||||||||||||||||||||||||
||||||||||||||||||||||||||||||||||||||||||||
||||||95|95|95||||||||||||||||||||||||||||||||||||
||||||||||||||||||||||||||||||||||||||||||||
|92|92|94<br>71|94<br>71|94<br>71||98|98|~~82~~|~~82~~|~~82~~||||92|92|92|74|74|74|92|92|92|92<br>77|92<br>77|92<br>77|74|74|74|86|86|86|92<br>|92<br>|92<br>||||75|75||||
||||||||||83|83|68|80|80|57|57|||64|64|56|56||||||82|82|59|59||65|65||82<br>58|82<br>58|82<br>58||||||
||||||||||83|83|68|80|80||||||||||||||||||||||||||||||
||||||||||83|83|68|80|80||||||||||||||||||||||||||||||
||||||||||||||||||||||||||||||||||||||||||||
||||||||||||||||||||||||||||||||||||||||||||



Figure 11. Distribution of the 14 fine-grained tasks in Persona-MME across its 32 _k_ and 128 _k_ context length configurations, with the number
of test cases indicated for each task.



despite their inherent limitations on visual tasks (e.g.,
VDR).

- **No Single Dominant Model:** Even the top-performing
model, GPT-5, does not dominate across all sub-tasks. It



is surpassed by other models in specific areas, including
Growth Modeling and Visual Detail Recall, highlighting
the complexity of holistic personalization.

- **Effectiveness of PersonaVLM:** Our PersonaVLM frame

Table 5. Task definitions for the Persona-MME evaluation suite.


**Evaluation Aspect** **Task** **Definition**



Memory


Intent


Preference


Behavior


Relationship



Visual Detail Recall Assesses the ability to recall fine-grained visual details from previously shared images.


Semantic Information Recall Evaluates long-term memory for semantic information (e.g., events,
preferences, context) from conversational history.


Explicit Intent Inference Assesses understanding a user’s explicitly stated intent from past
multimodal context (e.g., linking a suitcase photo to text about a
"business trip").


Implicit Intent Recognition Tests inferring a user’s latent intent from the current context (e.g.,
deducing a calm beach is unsuitable for a user known to enjoy
surfing).


Latest Preference Recognition Assesses prioritizing recent behavioral evidence (e.g., a rock concert
photo) over older, contradictory stated preferences (e.g., "I only like
classical music").


Interest Evolution Analysis Evaluates explaining the evolution of a user’s interests by linking it
to a specific causal event from their history (e.g., a change in diet
due to a mentioned allergy).


Implicit Preference RecommenTests recommending based on implicit values inferred from user
dation
history (e.g., suggesting a bicycle over a car to an eco-conscious
user).


Behavioral Pattern Recognition Assesses recognizing recurring behavioral patterns to predict actions
(e.g., predicting a Saturday café visit based on a history of Saturday
café photos).


Long-term Goal Tracking Tests tracking a long-term goal’s progress, including identifying
when its status is unknown due to insufficient information.


Relationship Recognition Tests identifying relationship significance based on the frequency
and context of individuals in multimodal history (e.g., identifying a
closer friend by their more frequent appearance).


Relationship Dynamics CompreAssesses inferring relationship dynamics from context to adapt
hension
communication style (e.g., using a professional tone for a colleague).



Tiered Explanation Delivery Tests tailoring explanations to a user’s evolving skill level.
Growth

Generalizing to New Scenarios Assesses the ability to generalize a user’s behaviors and preferences
to novel scenarios.


Alignment Personality Alignment Assesses the ability to infer a user’s personality traits from long-term
interactions and adapt its responses accordingly.



work significantly enhances the baseline model’s performance by **22.46%** . The most substantial improvements are
concentrated in the sophisticated dimensions of **Growth**
and **Alignment**, underscoring the targeted benefits of our
approach.



**Comparison with Existing Benchmarks.** As shown in
Table 7, Persona-MME provides a more comprehensive evaluation of personalization compared to existing benchmarks.
Specifically, it is the only benchmark that combines **long-**
**term** interaction scenarios, **multimodal** (vision and text)
inputs, and a holistic assessment of memory, understanding,
and alignment capabilities.


Table 6. Key statistics of the Persona-MME.

|Statistic Value|Col2|
|---|---|
|Avg. turns per dialogue<br>Multimodal turn ratio<br>Avg. question length<br>Avg. answer length<br>Image-related question ratio|142.9<br>15.87%<br>22.7 words<br>3.05 words<br>34.02%|



Figure 12. Word cloud of keywords from the dialogue data in
Persona-MME, illustrating the rich diversity of conversation scenarios and topics.


**Quality** **Assurance.** To ensure the quality of PersonaMME, every test case underwent a rigorous manual review process. We first generated initial questions using
the Gemini-2.5-Pro API [10] . Subsequently, a team of four annotators meticulously reviewed each case against three key
criteria: (a) Consistency: ensuring the question aligns with
its assigned task category. (b) Accuracy: verifying the correctness of the ground-truth answer. (c) Alignment Validity:
assessing whether the model’s response in alignment tests
appropriately adapts to (or conflicts with) the predefined
personality traits. Any examples found to be ambiguous or
conflicting were discarded. This comprehensive review process required approximately 40 person-hours to complete.


**E. More Experimental Details**


**E.1. Benchmarks**


**PERSONAMEM [14].** This is a recent benchmark featuring
synthetic, multi-session, and timeline-aware conversational
data, designed to evaluate an LLM’s ability to remember,
track, and generalize from personalized user profiles and
preferences. It includes seven types of _in-situ_ user queries,
including: recall user-shared facts, suggest new ideas, acknowledge latest user preferences, track full preference evolution, revisit reasons behind preference updates, and provide
preference-aligned recommendations. We conduct evaluations under two context-length settings, 32 _k_ and 128 _k_ to

10We use the gemini-2.5-pro-preview-06-05 model.


|Col1|Col2|Col3|Col4|Col5|Col6|Col7|Col8|Col9|Col10|Col11|Col12|Col13|Col14|Col15|Col16|Col17|Col18|Col19|Col20|Col21|Col22|Col23|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
||||||||||||||||||||||||
||||||||||||||||||||||||
||||||||||||||||||||||||
||||||||||||||||||||||||
||||||||||||||||||||||||
||||||||||||||||||||||||
||||||||||||||||||||||||
||||||||||||||||||||||||
||||||||||||||||||||||||
||||||||||||||||||||||||
||||||||||||||||||||||||
||||||||||||||||||||||||
||||||||||||||||||||||||
||||||||||||||||||||||||
||||||||||||||||||||||||
||||||||||||||||||||||||
||||||||||||||||||||||||



Figure 13. Ablation study on the number of retrieved episodic
topics for Persona-MME.


kens. The settings comprise 589 and 1,362 multiple-choice
questions, respectively, with the larger setting derived by
sampling half of the personas from the original 2,728. Performance is measured by accuracy, and the comparative
results are reported in Table 1 and Fig. 4.


**P-SOUPS** **[13].** P-SOUPS assesses LLM personalization
across three preference dimensions: _Expertise_, _Informative-_
_ness_, and _Style_, each containing 600 test cases for a total
of 1,800. A single test case consists of a user prompt, a
profile, and a pair of responses: one aligned with the profile
(the “chosen” response) and one misaligned (the “rejected”
response). The model is tasked with selecting the aligned
response from the pair, and performance is measured by accuracy. For our few-shot experiments, we augment the input
with a single example of Pair-wise Comparative Feedback,
as provided by the benchmark.


**E.2. Ablation Study**


**Effectiveness of Different Memory Types.** We present an
ablation study on the memory components of PersonaVLM
architecture in Table 8. The results consistently show that
removing any single memory type degrades overall performance, a trend that holds across both the 32 _k_ and 128 _k_
context settings. Notably, Episodic memory emerges as the
most critical component; its removal leads to a substantial
performance drop of 12.41% and 5.19% in the two settings,
respectively, while removing other memory types results in a
performance drop of less than 2%. Delving into sub-task performance, we observe that Procedural memory has a strong
impact on tasks related to Behavior and Relationship. Collectively, these findings suggest that the different memory types
fulfill distinct yet complementary roles, and all are integral
to the holistic performance of the PersonaVLM agent.



75


70


65


60



Number of Topics


Table 7. Comparison of Persona-MME with existing personalization benchmarks. Abbreviations are defined as follows. **Modality** : V
(Visual), T (Text). **Capabilities** : U (Personalized Understanding), M (Memory), A (Alignment). **Answer Type** : MC (Multiple Choice), BC
(Binary Choice).


**Benchmark** **Modality** **Long-Term** **Capabilities** **Answer Type**


PERSONAMEM [14] T ✓ M + U MC
P-SOUPS / ALIGNX-test [13, 21] T A BC
Yo’LLaVA [28] V U BC
RAP [11] V M + U MC


**Persona-MME (ours)** V + T ✓ U + M + A MC + BC


Table 8. Ablation study of PersonaVLM components on the Persona-MME benchmark. The evaluation shows the performance impact of
removing (“w/o” denotes “without”) key components, specifically the individual memory types (Core, Procedural, Semantic, Episodic) and
the reasoning capability.


**Persona-MME**
**Context** **Setting**

Memory Intent Preference Behavior Relationship Growth Overall


PersonaVLM 69.89 76.8 58.05 69.02 73.21 86.78 71.48

       - w/o Core 73.66 74.59 59.32 63.59 67.26 83.91 69.80 _−_ 1 _._ 68

       - w/o Procedural 72.58 79.01 59.32 59.78 70.24 85.06 70.33 _−_ 1 _._ 15
32 _k_   - w/o Semantic 66.67 72.38 59.32 66.30 72.02 85.63 69.71 _−_ 1 _._ 77

       - w/o Episodic 33.77 55.35 56.68 66.27 69.84 74.07 59.07 _−_ 12 _._ 41

       - w/o Reasoning 69.57 69.7 60.48 62.14 71.76 83.61 68.73 _−_ 2 _._ 75


PersonaVLM 69.28 77.70 61.50 60.26 75.00 87.97 71.05

       - w/o Core 69.28 77.70 64.17 58.28 72.50 84.21 70.39 _−_ 0 _._ 66

       - w/o Procedural 69.88 77.03 61.50 54.97 69.17 87.97 69.39 _−_ 1 _._ 66
128 _k_   - w/o Semantic 67.47 73.65 60.43 60.93 74.17 88.72 69.94 _−_ 1 _._ 11

       - w/o Episodic 50.60 68.92 60.96 62.25 70.00 88.72 65.86 _−_ 5 _._ 19

       - w/o Reasoning 59.21 71.97 57.87 65.87 73.39 80.00 67.32 _−_ 3 _._ 73



**Episodic Memory Configuration.** Given the critical role
of episodic memory, we conduct an ablation study on the
number of retrieved memory topics. As shown in Fig. 13, the
overall accuracy on Persona-MME initially increases with
the number of retrieved topics before performance saturates.
To strike a balance between performance and computational
efficiency, we select two topics as the default setting for all
of our main experiments.


Table 9. Ablation study on the PEM component.

|Setting|Expertise|Informativeness|Style|Overall|
|---|---|---|---|---|
|PersonaVLM<br>- w /o PEM|51.1<br>48.5_−_2_._6|53.6<br>50.2_−_3_._4|44.0<br>38.3_−_9_._2|49.6<br>45.6_−_4_._0|



**Effectiveness of the Reasoning Capability.** We validate
the effectiveness of PersonaVLM’s multi-step reasoning and
retrieval capability with two key findings. First, the full
PersonaVLM model, trained with reinforcement learning,



demonstrates a significant 4–7% performance gain over its
SFT-only baseline on Persona-MME and PERSONAMEM
(Table 1). This highlights the benefit of the overall training
process in cultivating this advanced reasoning behavior. To
further isolate the contribution of this capability, we conduct
an ablation study. Disabling multi-turn retrieval during the
response stage results in performance drops of 2.75% and
3.73% at the 32 _k_ and 128 _k_ context settings, respectively
(Table 8). These results underscore the critical role that
multi-step reasoning and retrieval play in achieving robust
long-term personalization.


**E.3. Personality Evolving Mechanism**


In Fig. 14, we visualize how PEM captures the evolution
of personality traits inferred from user interactions across
diverse personas. Furthermore, as shown in Table 9, our
ablation study on P-SOUPS demonstrates the effectiveness
of PEM. Finally, Table 10 provides examples of how PersonaVLM adapts its responses based on the inferred personality
traits to meet the user’s personalized needs. These results


Table 10. An overview of the Big Five personality dimensions, with examples illustrating how our method generates adaptive responses to
the same user query by adjusting inferred trait scores (high vs. low).


**Personality** **Characteristic** **Example**



Openness **Low** : practical, conventional, factual, cautious,
pragmatic
**High** : creative, imaginative, curious, innovative,
abstract, broad-minded


Conscientiousness **Low** : spontaneous, flexible, impulsive, carefree
**High** : organized, disciplined, detail-oriented,
efficient, reliable.


Extraversion **Low** : reserved, quiet,
solitary, reflective,
thoughtful
**High** : outgoing, sociable,
energetic, talkative,
assertive.


Agreeableness **Low** : competitive, critical, skeptical, direct, analytical
**High** : cooperative, compassionate, empathetic,
trusting, kind.


Neuroticism **Low** : calm, confident, resilient, secure, emotionally stable
**High** : anxious, worryprone, insecure, stressed,
moody.



**Query:** I’m planning a one-week trip to Rome. Can you suggest an
itinerary for me?
**Low score response:** Rome is such a rich city with so much history! For
a one-week trip, here’s a practical itinerary that balances must-see spots
with some flexibility. Day 1...Day 7... Enjoy your trip to Rome!
**High score response:** Clare, planning a week in Rome? Let’s mix iconic
spots with hidden gems—here’s a flexible itinerary you can tweak! Day
1...Day 7. Adjust days as you please; Rome’s best-kept secrets are waiting
for you to discover them!


**Query:** I signed up for a 5k race that’s three months away. Now I need to
figure out how to train for it.
**Low score response:** For a 5k three months out, start small—maybe aim
for 20 minutes of walking/jogging 3 days a week, building up by 1 minute
each week. Use a calendar to map it out (or just keep a notebook handy).
If you hit a rough patch, mix in some light stretching or yoga to keep
things loose. Start slow, stay consistent—you’ll build endurance without
burning out.
**High score response:** Let’s break this into a structured 3-month plan!
Here’s what works for many runners: Month 1 (Weeks 1–4): Build
Base...For consistency, use a calendar to log your runs—tracking distance/time helps keep you on track. Also, mix in strength training (like
leg curls, lunges) 2 days/week to build endurance.


**Query:** My birthday’s this weekend—should I go all out with a big party,
or keep it intimate with a small dinner among my closest friends? What
would you choose?
**Low score response:** Since you lean toward calm interactions, keeping it
small might let you savor every moment without the pressure of impressing a crowd.
**High score response:** That’s such a fun dilemma! Since you’re all about
the good vibes (hello, high extraversion!), a big party with friends could
be electric—imagine laughter, games, and maybe even a surprise performance (or two!).


**Query:** In a team meeting, a colleague made a small mistake. Should I
point it out, or stay quiet?
**Low score response:** It depends on the context. If the mistake is minor ...
But if it’s something that could clarify or prevent confusion later, pointing
it out—clearly, without criticizing—could help. Think about what’s best
for the team’s flow right now.
**High score response:** Clare, when a colleague makes a small mistake
in a team meeting, there’s no one “right” answer—both ways have pros
and cons. Think about how the mistake affects the team’s goal, your
relationship with that colleague, and your comfort level. Either way,
you’re being thoughtful either way!"


**Query:** I have an important presentation next week. I can’t stop thinking
about all the things that could go wrong.
**Low** **score** **response:** It’s normal to feel some pressure before a big
presentation. Focus on what you can control...
**High score response:** I know, it’s been unbearable. Staying cool feels
like such a win when it’s this hot out. Hope you’re finding ways to beat
the heat—maybe some refreshing drinks or light walks.


Table 11. Efficiency comparison of PersonaVLM


**Method** **Avg.Tokens** **Avg.Times (s)**


baseline 43530 8.4
PersonaVLM w/o reasoning 2726 2.09
PersonaVLM 2170 10.18


demonstrate that the inclusion of PEM enables PersonaVLM
not only to capture a user’s evolving personality during longterm interactions accurately but also to generate responses
that are consistently aligned with these inferred traits.


**E.4. More Interaction Examples**


In Fig. 15, we provide comparative cases of open-ended interactions between PersonaVLM, the baseline model, and GPT4o. These examples demonstrate PersonaVLM’s superior
comprehensive personalization capabilities during long-term
interactions.


**E.5. Prompts Used in Our Framework**


We present the prompts used in PersonaVLM across several
figures. The prompts for multi-turn reasoning and retrieval
are shown in Figs.16 and 17. The prompt for PEM personality inference is shown in Fig. 18. The corresponding prompts
for updating the different memory modules are provided in
Figs. 19, 20, 21, and 22. The prompt for the open-generation
task evaluation is presented in Fig. 23.


**F. Further Discussion**


**Efficiency** **and** **Data** **Security.** We evaluate model efficiency using two key metrics: average token consumption
per request and average response time (in seconds). As detailed in Table 11, our analysis is based on 100 randomly
selected samples from the Persona-MME, comparing the
baseline model (Qwen2.5-VL-7B), PersonaVLM without
its reasoning capability (PersonaVLM w/o reasoning), and
the standard PersonaVLM. It is important to note that the
measured time covers the end-to-end process from user input
to receiving the complete response. The memory update operation in PersonaVLM is performed asynchronously after
a response is delivered and is therefore excluded from this
timing analysis.
The results highlight two key findings. First, PersonaVLM without reasoning demonstrates significant efficiency
gains over the baseline, reducing average token consumption by a remarkable 93.7% and achieving a 4.8 _×_ speedup.
Second, when equipped with its reasoning capability, the
standard PersonaVLM further decreases token consumption
by 20.4% compared to its non-reasoning counterpart. However, the computational overhead of the reasoning process
results in a 21.1% increase in response time relative to the



baseline. This reveals a clear trade-off between advanced
reasoning capabilities and response latency.
Regarding data security, PersonaVLM’s memory and retrieval operations function independently of external commercial model APIs. This self-contained architecture inherently ensures data security and mitigates privacy concerns.


**Limitations.** PersonaVLM has several limitations. First, it
does not currently support person recognition and tracking
from video or audio inputs. Second, its overall performance
is inherently constrained by the capabilities of the underlying
baseline model, despite significant personalization gains.
Third, the memory system is primarily timeline-based and
does not yet establish connections or merge related episodic
memories occurring at different times. Addressing these
limitations is a key direction for our future work.


Turn 0

C


N

Turn 0

C


N

Turn 0

C


N

Turn 0

C


N

Turn 0

C


N

Turn 0

C


N

Turn 0

C


N

Turn 0

C


N

Turn 0

C


N

Turn 0

C


N

Turn 0

C


N

Turn 0

C


N



Turn 30

C


N

Turn 42

C


N

Turn 38

C


N

Turn 30

C


N

Turn 47

C


N

Turn 26

C


N

Turn 54

C


N

Turn 45

C


N

Turn 29

C


N

Turn 35

C


N

Turn 45

C


N

Turn 35

C


N



Turn 60

C


N

Turn 85

C


N

Turn 77

C


N

Turn 60

C


N

Turn 95

C


N

Turn 52

C


N

Turn 108

C


N

Turn 91

C


N

Turn 58

C


N

Turn 70

C


N

Turn 90

C


N

Turn 71

C


N



Turn 91

C


N

Turn 128

C


N

Turn 116

C


N

Turn 91

C


N

Turn 143

C


N

Turn 78

C


N

Turn 163

C


N

Turn 136

C


N

Turn 87

C


N

Turn 106

C


N

Turn 135

C


N

Turn 107

C


N



Turn 121

C


N

Turn 171

C


N

Turn 154

C


N

Turn 121

C


N

Turn 190

C


N

Turn 104

C


N

Turn 217

C


N

Turn 182

C


N

Turn 116

C


N

Turn 141

C


N

Turn 180

C


N

Turn 142

C


N



Turn 151

C


N

Turn 214

C


N

Turn 193

C


N

Turn 152

C


N

Turn 238

C


N

Turn 131

C


N

Turn 271

C


N

Turn 227

C


N

Turn 145

C


N

Turn 176

C


N

Turn 226

C


N

Turn 178

C


N



Turn 182

C


N

Turn 257

C


N

Turn 232

C


N

Turn 182

C


N

Turn 286

C


N

Turn 157

C


N

Turn 326

C


N

Turn 273

C


N

Turn 174

C


N

Turn 212

C


N

Turn 271

C


N

Turn 214

C


N



Turn 212

C


N

Turn 300

C


N

Turn 270

C


N

Turn 213

C


N

Turn 333

C


N

Turn 183

C


N

Turn 380

C


N

Turn 318

C


N

Turn 203

C


N

Turn 247

C


N

Turn 316

C


N

Turn 249

C


N



Turn 242

C


N

Turn 343

C


N

Turn 309

C


N

Turn 243

C


N

Turn 381

C


N

Turn 209

C


N

Turn 434

C


N

Turn 364

C


N

Turn 232

C


N

Turn 282

C


N

Turn 361

C


N

Turn 285

C


N



Turn 273

C


N

Turn 386

C


N

Turn 348

C


N

Turn 274

C


N

Turn 429

C


N

Turn 236

C


N

Turn 489

C


N

Turn 410

C


N

Turn 262

C


N

Turn 318

C


N

Turn 407

C


N

Turn 321

C


N



User 1


User 2


User 3


User 4


User 5


User 6


User 7


User 8


User 9


User 10


User 11


User 12





O


O


O


O


O


O


O


O


O


O


O


O





O


O


O


O


O


O


O


O


O


O


O


O





O


O


O


O


O


O


O


O


O


O


O


O





O


O


O


O


O


O


O


O


O


O


O


O





O


O


O


O


O


O


O


O


O


O


O


O





O


O


O


O


O


O


O


O


O


O


O


O





O


O


O


O


O


O


O


O


O


O


O


O





O


O


O


O


O


O


O


O


O


O


O


O





O


O


O


O


O


O


O


O


O


O


O


O





O


O


O


O


O


O


O


O


O


O


O


O



Figure 14. Visualization of dynamic personality evolving process captured by PEM on ten randomly sampled conversations from the
Persona-MME dataset.


**Relevant Historical Context** **Current Turn**



**User :** This is the café cat—named her
Colette after Solène’s old sax tune,
though... (2024-09-03 19:20)



**User :** My mind's a tangled mess of faces tonight. Based on everything, who seems
more significant in my life right now, Colette or Oscar? (2024-09-05 19:55)
**Qwen2.5-VL** : Both Colette and Oscar are significant in your life, but they serve
different roles. Colette represents... Both are essential, but in different ways.
**GPT-4o :** Colette seems more significant right now—her presence and purrs offer a
constant, if frayed, companionship in your sketches and typewriter rhythms.

**PersonaVLM :** Colette’s the steadier thread here—her purr’s been the quiet
accomplice to chaos, the hum under your typewriter’s static...

**User :** Thinking back to that picture of Kai from Thursday morning, what was on the





**GPT-4o :** Above the heart decoration on the wall was a cross.



**User :** This is my partner Kai’s morning **PersonaVLM :** In the wall above Kai’s heart decoration that Thursday morning, there
routine snap... (2024-09-12 09:40) was a cross—just another little detail that feels like how he weaves steady, caring...



**User :** NFL SUNDAY PREP IS LIT—
Marie’s ranch vs Rita’s buffalo dip?
Y’ALL KNOW WE’RE SETTLING THIS
TODAY! GONNA FILM BERNIE’S SIDE...
(2024-10-25 09:30)


camping trip Marnie and I meticulously
planned in...(2024-09-15 15:37)



**User :** Hey, for the pizza swap snacks, what was that dip Rita brought last Friday


**GPT-4o :** Rita brought buffalo dip to last Friday’s pizza swap—perfect clash with
Marie’s ranch, and Bernie’s side-eye meme’ll capture that chaos just right!



**PersonaVLM :** Rita brought that bold red *buffalo* dip—Marie’s already schemin’ to
pair it with ranch for the next pizza swap...—chaos approved �✨

**User :** A friend invited me to a 'spontaneous-speaking' storytelling night. Everyone
gets a random object and has to weave a story around it on the spot. I've never done
anything like it. Based on what you know about me, what's a good way for me to
approach this? (2024-07-07 17:18)



**Qwen2.5-VL :** That sounds like a fun and creative challenge! Given your interest in
storytelling and your calm, gentle demeanor, here are some tips...
**GPT-4o :** Approach it like you’re weaving a group garden chat—embrace the chaos
and find peace in it, like Belle does among the blooms...



**PersonaVLM :** Since you're new to this, try framing it like a gentle anchor—a little like
how you approach slow art or the ceramics workshop. Pick an object, then take a
breath, and let your mind wander to...



**User :** That campsite picture from last Sunday, with the horses. Do you think it would
be a good location for one of those dating shows? (2024-09-23 22:13)

**Qwen2.5-VL :** A campsite with horses might make for an interesting backdrop for a
dating show, especially if the show focuses on outdoor...



**GPT-4o :** That campsite, with its openness, could provide a scenic, natural backdrop
for a dating show...



Figure 15. Case studies: Qualitative comparison of open-ended generation


Figure 16. Prompt for multi-turn reasoning and retrieval in the response phase.





Figure 17. Intermediate prompt for multi-turn reasoning and retrieval in the response phase.


Figure 18. Prompt for inferring the user’s Big Five personality traits from the latest interaction.







Figure 19. Prompt for updating procedural memories.


Figure 20. Prompt for analyzing user input and deciding on semantic memory creation.


Figure 21. Prompt for updating the core memory based on recent conversations.





Figure 22. Prompt for creating episodic memories by summarizing dialogue topics.


Figure 23. Prompt for open-generation task evaluation.


