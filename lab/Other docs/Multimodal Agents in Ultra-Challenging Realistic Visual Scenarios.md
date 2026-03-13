## **AGENTVISTA: Evaluating Multimodal Agents in Ultra-Challenging** **Realistic Visual Scenarios**

**Zhaochen Su** [1] **Jincheng Gao** [1] **Hangyu Guo** [1] **Zhenhua Liu** [1] **Lueyang Zhang** [1] **Xinyu Geng** [1]

**Shijue Huang** [1] **Peng Xia** [2] **Guanyu Jiang** [3] **Cheng Wang** [4] **Yue Zhang** [1] **Yi R. (May) Fung** [1] **Junxian He** [1]

**Website:** [agentvista-bench.github.io](https://agentvista-bench.github.io/)   - [github.com/hkust-nlp/AgentVista](https://github.com/hkust-nlp/AgentVista)



**Abstract**


Real-world multimodal agents solve multi-step
workflows grounded in visual evidence. For example, an agent can troubleshoot a device by linking
a wiring photo to a schematic and validating the
fix with online documentation, or plan a trip by
interpreting a transit map and checking schedules
under routing constraints. However, existing multimodal benchmarks mainly evaluate single-turn
visual reasoning or specific tool skills, and they
do not fully capture the realism, visual subtlety,
and long-horizon tool use that practical agents require. We introduce AGENTVISTA, a benchmark
for generalist multimodal agents that spans 25 subdomains across 7 categories, pairing realistic and
detail-rich visual scenarios with natural hybrid
tool use. Tasks require long-horizon tool interactions across modalities, including web search,
image search, page navigation, and code-based
operations for both image processing and general programming. Comprehensive evaluation of
state-of-the-art models exposes significant gaps
in their ability to carry out long-horizon multimodal tool use. Even the best model in our evaluation, GEMINI-3-PRO with tools, achieves only
27.3% overall accuracy, and hard instances can require more than 25 tool-calling turns. We expect
AGENTVISTA to accelerate the development of
more capable and reliable multimodal agents for
realistic and ultra-challenging problem solving.


**1. Introduction**


Humans seamlessly integrate multi-sensory information to
tackle complex real-world problems (Stein, 2012). With the


1Hong Kong University of Science and Technology 2University
of North Carolina at Chapel Hill [3] Zhejiang University [4] National
University of Singapore. Correspondence to: Zhaochen Su
_<_ zsubf@connect.ust.hk _>_, Yi R. (May) Fung _<_ yrfung@ust.hk _>_,
Junxian He _<_ junxianh@cse.ust.hk _>_ .


_Preprint._ _March 3, 2026._



_Figure 1._ A representative AGENTVISTA task grounded in a real
home-renovation scenario. The agent needs to match flooring
styles across images, verify the target room, retrieve product specifications, and compute final cost via interleaved tool use.


rapid evolution of AI agents (Wang et al., 2024a; Comanici
et al., 2025; OpenAI, 2025f; Team et al., 2026), developing
visual agentic intelligence becomes essential. For instance,
an agent is expected to assist in shopping by scanning shelf
products and retrieving nutritional information to satisfy
user health constraints, or support troubleshooting by linking malfunction photos with schematic diagrams to diagnose
specific faults. However, a major challenge in developing
such multimodal agents is the absence of a benchmark based
on realistic scenarios that covers the diversity and complexity of long-horizon tool interactions across different modalities, which limits reliable evaluation of agent capabilities in
open domains (Xie et al., 2024; Li et al., 2025a).


Traditional multimodal benchmarks (Antol et al., 2015; Hudson & Manning, 2019; Yue et al., 2024a; Wang et al., 2024b;
Scale AI, 2025) focus on assessing visual perception and
complex reasoning capabilities. Recently, a growing number of benchmarks have emerged to evaluate multimodal
agentic behaviors (Ma et al., 2024; Li et al., 2025b; Ashraf
et al., 2025; Guo et al., 2025; Tao et al., 2025; Geng et al.,
2025). However, these evaluations typically present two
main gaps: ❶ **Capability-Specific Evaluation** : They typically emphasize particular capabilities, focusing on skills
such as visual manipulation (Wang et al., 2025; Lai et al.,
2025), web browsing (Li et al., 2025c; Tao et al., 2025),
or code generation (Yang et al., 2024). This narrow focus















1


**AgentVista**





































_Figure 2._ Sampled AGENTVISTA examples from each domain. Each query is grounded in complex, real-world visual scenes and is
designed to elicit agentic tool use with multi-step reasoning toward a unique, verifiable answer.



makes it difficult to evaluate generalist agents that must
combine multiple skills and remain reliable in long-horizon
workflows. ❷ **Trade-off between Realism and Difficulty** :
Practical agent tasks are difficult because they combine
cluttered visual evidence with long-horizon tool use under
constraints. Yet many benchmarks increase difficulty by
simplifying the visual state or by relying on tool patterns
that deviate from everyday workflows, which can shift the
bottleneck away from realistic grounding and interaction.
For example, VisualToolBench pre-processes the input images to facilitate specific visual operations (Guo et al., 2025).
While this design is effective for evaluating visual manipulation, it also shifts the problem from reasoning over natural
visual states to operating on curated inputs.


To address these gaps, we introduce AGENTVISTA, a benchmark designed to evaluate generalist multimodal agents on
diverse, realistic, and challenging tasks. AGENTVISTA contains 209 tasks spanning 25 sub-domains across 7 categories,
including commerce, geography, society, technology, entertainment, culture, and academics, and grounds each query
in detail-rich visual states such as daily photos, screenshots,



_Table 1._ Comparison with representative multimodal agent benchmarks. Operation abbreviations: **VO.** (Visual Operations), **VS.**
(Visual Search), **TS.** (Text Search), and **CE.** (Code Execution).
Tool categories are based on the tools and signals used in these
benchmarks. “# Turns” reports the average number of tool-calling
turns by GPT-5, used as a proxy for task complexity.

|BENCHMARK|MULTI<br>VO. VS. TS. CE. # Turns<br>IMAGE|
|---|---|
|TIR-BENCH<br>AGENT-X<br>MMSEARCH-PLUS<br>BROWSECOMP-VL<br>VISUALTOOLBENCH|✓<br>✗<br>✗<br>✓<br>✓<br>2.92<br>✓<br>✗<br>✓<br>✓<br>✓<br>3.4<br>✗<br>✓<br>✓<br>✗<br>✓<br>4.6<br>✗<br>✓<br>✓<br>✓<br>✗<br>4.3<br>✓<br>✗<br>✓<br>✓<br>✗<br>4.46|
|AGENTVISTA (Ours)|✓<br>✓<br>✓<br>✓<br>✓<br>12.67|



and technical diagrams, with both single-image and multiimage inputs. Each query is manually authored to reflect
authentic user intent and is subjected to strict quality control, where every instance is carefully reviewed to ensure
mandatory visual dependence and a unique, verifiable answer. Every task requires long-horizon interaction with
interleaved tools, where the agent repeatedly grounds visual
cues, retrieves external information, and verifies intermedi


2


**AgentVista**



ate decisions. Table 1 summarizes the key differences between AGENTVISTA and representative agentic multimodal
benchmarks. Figure 1 shows a representative example from
AGENTVISTA motivated by a real home renovation need:
the agent need to match flooring styles across scenes, verify
the target room with image-based checks, retrieve product
specifications online, and compute a deterministic final cost
from the room size and packaging information.


AGENTVISTA is evaluated in a controlled yet practical setting, we adopt four widely used tools that cover the core
interaction patterns of real-world multimodal agents, including web search, image search, page navigation, and
code-based operations for both image processing and general programming. Our experiments on representative opensource and commercial MLLMs show that AGENTVISTA
remains far from being solved, leaving substantial room for
improvement. Even the best performance in our evaluation,
GEMINI-3-PRO, achieves only 27.3% overall accuracy. Further error analysis shows that many failures start with visual
misidentification and then lead to wrong retrieval and unreliable tool use over many steps. To facilitate future research,
we will release both the AGENTVISTA benchmark and a
lightweight yet general agent framework to facilitate reproducible evaluation and accelerate progress on long-horizon
multimodal tool use.


**2. The AGENTVISTA**


**2.1. Overview of AGENTVISTA**


We introduce AGENTVISTA, a benchmark for evaluating generalist multimodal agents on realistic and ultrachallenging tasks. AGENTVISTA focuses on realistic user requests that are still hard in practice and require long-horizon
tool use grounded in visual evidence. AGENTVISTA contains 209 tasks spanning 25 sub-domains across 7 categories:
Technology, Commerce, Geography, Entertainment, Society, Academics, and Culture. The domain distribution and
dataset composition are summarized in Table 2 and Figure 4.
As shown in Figure 2, tasks are built from authentic user
needs and require multi-step reasoning with tool use. For
example, an agent may need to read key constraints from a
photo or screenshot, retrieve missing details from external
resources, and then combine multiple pieces of evidence
to produce the final answer. This includes diagnosing a
hardware issue by matching visible components to technical documentation, selecting a product that satisfies allergy
and nutrition constraints by comparing labels with online
specifications, and planning a route under time and transit
limits by reading schedules from images and verifying them
with web search. To enable robust and scalable evaluation,
each instance is paired with a clear and deterministic ground
truth answer, typically a short phrase or a numeric value.



_Table 2._ Summary statistics of the AGENTVISTA benchmark.


**STATISTIC** **NUMBER**


Total queries 209
Total images 308
Primary categories 7
Secondary categories 25


Average query length 401.4
Average answer length 40.8


Image distribution

   - Single-image queries 151 (72.2%)

   - Multi-image queries 58 (27.8%)


**2.2. Data Construction**


2.2.1. CORE DESIGN PRINCIPLES

We design AGENTVISTA based on three principles:


- **Vision-centric** **tasks** **with** **realistic** **images.** Each task
requires obtaining the key evidence from the visual input. The images are real and contain visual details to
support visual understanding, such as small but important
cues, multiple related objects, or subtle differences across
views. The query avoids stating the key information in
text and avoids questions that can be answered by a keyword search. These constraints ensure that solving the
task relies on understanding and comparison of visual
details, rather than on textual shortcuts.


- **Natural interleaved hybrid tool use.** Each task requires
using different tool types together, and the interaction
must include interleaved tool calls across at least two
tool categories. The intended solution should mix visual
tools and text-based tools, such as using image search or
image processing to gather visual evidence, then using
web search or page navigation to retrieve needed facts,
and finally combining the evidence to reach the answer.
Tool use must follow natural and real-world workflows.
Each tool call should be necessary for solving the task,
rather than added only to make the interaction longer. To
keep tasks realistic and challenging, we favor instances
that require grounding tool outputs in the visual input
under explicit constraints.


- **Easy to verify and stable over time.** Following recent
evaluation protocols (Li et al., 2025c; Wei et al., 2025),
each task has a concise target answer in a fixed format,
such as a number, an entity name, or a short description.
This design makes the evaluation process simple and accurate, similar to math tasks. Additionally, we address
the issue of information changing over time. Annotators
verify facts against reliable sources. When necessary, we
include specific time constraints in the question to ensure
the ground truth remains valid.



3


**AgentVista**







**300,000+**


















|Col1|Stage 1 Agent-Centric Filter|Col3|Finalization Filter Stage 2|Col5|Execution Filtering Stage 3|Col7|Quality Assurance Stage 4|Col9|
|---|---|---|---|---|---|---|---|---|
|**os**|_Remove Low-Quality_<br>_Images_<br>_Generate Task Queries_<br>_Human Screen for_<br>_Complexity_<br>**Agent-Centric Filter**||**Finalization Filter**<br>Construction &<br>Annotation||**Execution Filtering**<br>Hybrid-Action<br>Validation<br>_Long-Horizon Test_<br>_Tool Necessity_||**Quality Assurance**<br>_Two-Round  Review_<br>_Reproduce Tool Results_<br>_Finalize  Tasks_|**Final**<br>**AgentVista**<br>**Dataset**<br>**209Ultra-**<br>**Challenging Task**|
|**os**|**Initial Candidate**<br>**Selection**|**Initial Candidate**<br>**Selection**|**Challenging Task**<br>**Creation**|**Challenging Task**<br>**Creation**|**Execute & Test**|**Execute & Test**|**Verify & Approve**|**Verify & Approve**|



_Figure 3._ Overview of the AGENTVISTA dataset construction pipeline, consisting of agent-centric filtering, expert finalization, execution
filtering, and two-round verification to produce realistic and ultra-challenging multimodal agent tasks.







_Figure 4._ The categorization of AGENTVISTA. The benchmark
spans 7 major categories and 25 sub-domains, covering a broad
range of realistic and challenging multimodal agent scenarios. Category abbreviations: **COMM.** (Commerce), **GEOG.** (Geography),
**ENT.** (Entertainment), **TECH.** (Technology), **SOC.** (Society),
**ACAD.** (Academics), and **CULT.** (Culture).


2.2.2. DATASET CREATION PIPELINE


We build AGENTVISTA from 300k+ real images and real
user needs collected from public model arenas, annotatorcaptured daily scenarios, and private community forums,
with details in Appendix A.2. The dataset construction
pipeline is shown in Figure 3.


**Stage** **1:** **Agent-centric** **filtering.** We start with modelassisted mining and filtering to identify candidate initial
states that reflect realistic daily workflows. We first use
CLAUDE-OPUS-4 to filter the raw image pool by removing
cases with limited visual information or weak agentic potential, such as pure OCR screenshots, single-object landmark
photos, and images that can be solved without meaningful
visual reasoning. We provide CLAUDE-OPUS-4 with our
tool schema and ask it to propose an initial task query that
is compatible with the available tools and has a verifiable
answer format. The proposed query serves as a candidate
starting point for downstream curation. We then apply human screening to retain only images with sufficiently rich



visual evidence and queries that support a natural task formulation with hybrid tool use. To avoid simple cases, we
prioritize candidates with non-trivial constraints and keep
only those that naturally require multi-step reasoning rather
than a single direct lookup.


**Stage** **2:** **Expert** **finalization.** We recruit and train expert annotators on the project scope, taxonomy, and quality
requirements, and ask them to finalize each candidate produced in Stage 1. Starting from the image and the initial
query, annotators rewrite the query into a realistic user request while keeping it self-contained and vision-centric.
Realism is enforced by preserving the original visual state
and intent, and by expressing constraints in the way users
typically specify them, such as time, budget, compatibility,
and safety requirements. To make tasks ultra-challenging
in a natural way, annotators select cases where the answer
depends on fine-grained visual cues and cannot be obtained
by a single direct lookup. They ensure that solving the
task requires combining visual evidence with information
gathered from tools, and that the process includes necessary
interleaving across tool types. Annotators then produce a
deterministic target answer and record the key evidence and
tool steps used to obtain it, which enables later checking.


**Stage 3:** **Execution filtering.** We validate each instance
by executing the candidate task in our tool environment and
checking that the annotated answer is supported by reproducible tool outputs. During this process, we run GEMINI-3FLASH in the same tool environment to screen for tool-use
diversity, and we retain only tasks that require interleaved
calls across at least two categories. Furthermore, we run
GEMINI-2.5-PRO with tool access disabled and remove
samples that can be solved from the prompt alone.


**Stage** **4:** **Two-round** **verification.** Finally, we conduct
two rounds of verification. The first round removes instances
with insufficient visual evidence, weak visual dependency,
or questionable answer validity. In the second round, a
separate group re-checks each instance by following the evidence and tool steps recorded by annotators, and confirms
that the final answer is supported by the visual cues and the
tool outputs. Instances with unclear evidence, unstable an


4


**AgentVista**



swers, or unrealistic workflows are removed. The remaining
instances form the final AGENTVISTA benchmark.


**Filtering statistics.** We begin with 300k+ candidate images. Stage 1 uses model-assisted filtering and human
screening to select 568 potential initial states, 0.19% of
the raw pool. Stage 2 expert finalization yields 315 tasks
after rewriting the initial queries into realistic user requests
and adding deterministic target answers. Stage 3 execution
filtering retains 241 tasks by validating reproducible tool
outputs, enforcing interleaved calls across at least two tool
categories, and removing tasks solvable when tool access is
disabled. Stage 4 two-round verification selects the final 209
tasks by re-checking visual evidence, recorded tool steps,
and answer validity. On average, constructing a single instance takes about 4 hours, and expert annotators take about
30 minutes to solve an instance.


2.2.3. TOOL ENVIRONMENT


AGENTVISTA supports a compact set of tools that cover
common multimodal agent workflows. Models can call
web search to retrieve web pages, visit to open and
navigate a page, and image ~~s~~ earch to locate images
when a query requires external visual references. We also
provide code ~~i~~ nterpreter, which supports both programming and image processing. It enables arithmetic and
parsing, structured extraction, and operations such as cropping, resizing, measuring, and comparing visual regions
when needed. All tools are exposed with detailed descriptions and structured inputs and outputs, so the model can
decide when to call a tool and how to use the returned results.
Detailed tool definitions are provided in Appendix B.1.


**3. Experiments**


**3.1. Experimental Setup**


**Models.** We evaluate a broad set of frontier multimodal models that are commonly used as generalist
agents. Specifically, we test GPT-4.1 (OpenAI, 2025c),
O3, O4-MINI (OpenAI, 2025a), GPT-5 (OpenAI, 2025b),
GPT-5.1 (OpenAI, 2025d), GPT-5.2 (OpenAI, 2025e),
GEMINI-3-FLASH (Google DeepMind, 2025a), GEMINI3-PRO (Google DeepMind, 2025b), GROK-4 (xAI, 2025),
CLAUDE-SONNET-4 (Anthropic, 2025b), CLAUDE-OPUS4.1 (Anthropic, 2025a), CLAUDE-SONNET-4.5 (Anthropic,
2025c), and QWEN3-VL-235B-A22B (Bai et al., 2025).


**Evaluation Setup.** For all experiments, we use a temperature of 0.6 and cap the tool interaction budget at 30 turns for
every model. Since AGENTVISTA provides concise target
answers in deterministic formats, evaluation reduces to verifying the final answer. We use GPT-4.1 as a fixed judge
model to assess whether a model’s final response matches
the annotated ground truth under the required format. We
report accuracy as the evaluation metric.



**3.2. Main Results**

We report the overall performance in Table 3. We make the
below three observations.


**AGENTVISTA** **is** **ultra-challenging.** The results show
that AGENTVISTA remains difficult for current multimodal
agents. Even the best-performing model, GEMINI-3-PRO,
achieves 27.27% overall accuracy, indicating substantial
headroom. Performance is also low for a large portion of
models: 4 out of 14 models score below 15% overall accuracy. These results suggest that agents still have significant
room for improvement in complex long-horizon settings that
require multi-step tool use grounded in real visual evidence.
The average number of turns further reflects this difficulty.
For example, GPT-5.2 uses 13.85 turns on average, and 5
out of 14 models exceed 10 turns on average, indicating that
many tasks require extended multi-step interactions rather
than a short tool sequence. We also observe a sizable gap
between the open-source model QWEN3-VL-235B and the
closed-source models, suggesting substantial room for opensource multimodal agents. We report additional open-source
baselines in Appendix B.2. We further analyze common
failure patterns in Section 4.3.


**Domain strengths differ across model families.** Performance varies noticeably across categories, revealing complementary strengths among model series. The GPT-5 family
shows strong coverage on practical categories, with GPT5.2 performing best on TECHNOLOGY and tying for the
best score on ENTERTAINMENT, while GPT-5 and GPT-5.1
lead COMMERCE. The Gemini series is strongest overall:
GEMINI-3-PRO achieves the highest overall accuracy, leads
GEOGRAPHY, and performs competitively on SOCIETY and
CULTURE. Claude models are comparatively stronger on
categories that emphasize careful reading and constraint following, with their best results appearing in TECHNOLOGY
and GEOGRAPHY. Overall, these results suggest that current
agents do not yet provide uniform competence across domains, and improving broad, consistent performance across
realistic long-horizon tasks remains an open challenge.


**Multi-image inputs are not uniformly harder than single**
**image inputs.** For nearly all evaluated models, accuracy
with multi-image inputs is higher than with single-image
inputs. The gain is especially large for GEMINI-3-PRO,
which improves from 23.68% under single-image input to
36.84% under multi-image input. This pattern matches how
our multi-image instances are constructed. Additional views
often provide complementary evidence, reduce ambiguity,
and reveal details that are missing in a single shot, which
can make grounding and downstream retrieval more reliable.
While multi-image inputs still require cross-image alignment, the results suggest that the main bottleneck remains
long-horizon tool use and constraint tracking, rather than
the presence of multiple images itself.



5


**AgentVista**


_Table_ _3._ Main results on our proposed AGENTVISTA. Domain abbreviations: **COMM.** (Commerce), **GEOG.** (Geography), **ENT.**
(Entertainment), **TECH.** (Technology), **SOC.** (Society), **ACAD.** (Academics), and **CULT.** (Culture). Input mode abbreviations: **SINGLE.**
(Single-image input) and **MULTI.** (Multi-image input). The best-performing model in each category is **in-bold**, and the second best is


|underlined. Overall, GEMINI-3-PRO achieves the highest accuracy among all evaluated models. All values are accuracies in %.|Col2|Col3|Col4|
|---|---|---|---|
|**MODEL**<br>**BY CATEGORY**<br>**BY INPUT MODE**<br>**SUMMARY**<br>**COMM.**<br>**GEOG.**<br>**ENT.**<br>**TECH.**<br>**SOC.**<br>**ACAD.**<br>**CULT.**<br>**SINGLE.**<br>**MULTI.**<br>**OVERALL**<br>**# TURNS**|**MODEL**<br>**BY CATEGORY**<br>**BY INPUT MODE**<br>**SUMMARY**<br>**COMM.**<br>**GEOG.**<br>**ENT.**<br>**TECH.**<br>**SOC.**<br>**ACAD.**<br>**CULT.**<br>**SINGLE.**<br>**MULTI.**<br>**OVERALL**<br>**# TURNS**|**MODEL**<br>**BY CATEGORY**<br>**BY INPUT MODE**<br>**SUMMARY**<br>**COMM.**<br>**GEOG.**<br>**ENT.**<br>**TECH.**<br>**SOC.**<br>**ACAD.**<br>**CULT.**<br>**SINGLE.**<br>**MULTI.**<br>**OVERALL**<br>**# TURNS**|**MODEL**<br>**BY CATEGORY**<br>**BY INPUT MODE**<br>**SUMMARY**<br>**COMM.**<br>**GEOG.**<br>**ENT.**<br>**TECH.**<br>**SOC.**<br>**ACAD.**<br>**CULT.**<br>**SINGLE.**<br>**MULTI.**<br>**OVERALL**<br>**# TURNS**|
|QWEN3-VL-235B<br>GPT-4.1<br>O3<br>O4-MINI<br>GPT-5<br>GPT-5.1<br>GPT-5.2<br>GROK-4<br>CLAUDE-SONNET-4<br>CLAUDE-OPUS-4<br>CLAUDE-OPUS-4.1<br>CLAUDE-SONNET-4.5<br>GEMINI-3-FLASH<br>GEMINI-3-PRO|7.14<br>7.69<br>7.69<br>26.47<br>16.00<br>20.00<br>13.33<br>16.67<br>15.38<br>10.26<br>29.41<br>20.00<br>20.00<br>13.33<br>21.43<br>15.38<br>7.69<br>23.53<br>**40.00**<br>26.67<br>13.33<br>2.38<br>10.26<br>2.56<br>8.82<br>8.00<br>13.33<br>0.00<br>**23.81**<br>23.08<br>12.82<br>35.29<br>28.00<br>26.67<br>26.67<br>**23.81**<br>12.82<br>15.38<br>26.47<br>24.00<br>**40.00**<br>**40.00**<br>21.43<br>17.95<br>**20.51**<br>**38.24**<br>24.00<br>33.33<br>20.00<br>11.90<br>23.08<br>7.69<br>20.59<br>28.00<br>0.00<br>0.00<br>9.52<br>15.38<br>2.56<br>29.41<br>16.00<br>20.00<br>6.67<br>19.05<br>12.82<br>5.13<br>26.47<br>20.00<br>20.00<br>6.67<br>11.90<br>23.08<br>10.26<br>29.41<br>16.00<br>26.67<br>13.33<br>11.90<br>23.08<br>7.69<br>26.47<br>24.00<br>20.00<br>13.33<br>16.67<br>17.95<br>10.26<br>29.41<br>28.00<br>**40.00**<br>20.00<br>16.67<br>**28.21**<br>**20.51**<br>32.35<br>32.00<br>**40.00**<br>**40.00**|11.84<br>15.79<br>15.13<br>24.56<br>17.76<br>26.32<br>6.58<br>5.26<br>**24.34**<br>24.56<br>19.74<br>31.58<br>23.03<br>28.07<br>13.82<br>17.54<br>11.18<br>21.05<br>11.84<br>26.32<br>16.45<br>22.81<br>17.11<br>19.30<br>18.42<br>28.07<br>23.68<br>**36.84**|12.92<br>2.34<br>17.70<br>1.74<br>20.10<br>13.18<br>6.22<br>1.89<br>24.40<br>12.67<br>22.97<br>17.14<br>24.40<br>13.85<br>14.83<br>16.44<br>13.88<br>5.37<br>15.79<br>6.89<br>18.18<br>7.28<br>17.70<br>9.99<br>21.05<br>7.78<br>**27.27**<br>6.67|



Web Search Code Interpreter Visit Image Search










|Col1|11.8%|18.7%|18.2%|11.5%|5.5%|Col7|11.1%|13.0%|11.0%|
|---|---|---|---|---|---|---|---|---|---|
|10.3%|10.3%|10.3%|10.3%|10.3%|10.3%|10.3%|10.3%|10.3%|10.3%|
|10.3%|65.5% <br>|65.5% <br>|65.5% <br>|67.3%<br>|20.2%|19.8%|38.1%|34.5%|44.3%|
|5.8%|5.8%|5.8%|5.8%|5.8%|5.8%|5.8%|5.8%|5.8%|5.8%|
|76.1%<br>|76.1%<br>|55.2%|51.4%|51.4%|51.4%|51.4%|51.4%|51.4%|51.4%|
|76.1%<br>|76.1%<br>|55.2%|51.4%|51.4%|69.4%|69.4%|69.4%|69.4%|69.4%|
|76.1%<br>|76.1%<br>|55.2%|51.4%|51.4%|69.4%|66.2%|66.2%|66.2%|66.2%|
|76.1%<br>|76.1%<br>|55.2%|51.4%|51.4%|69.4%|66.2%|49.5%|50.8%|50.8%|
|76.1%<br>|76.1%<br>|55.2%|51.4%|51.4%|69.4%|66.2%|49.5%|50.8%|43.1%|
|76.1%<br>|76.1%<br>|55.2%|26.1%|26.1%|26.1%|26.1%|26.1%|26.1%|26.1%|
|76.1%<br>|76.1%<br>|23.7%|23.7%|23.7%|23.7%|23.7%|23.7%|23.7%|23.7%|
|76.1%<br>|20.5%|20.5%|20.5%|20.5%|20.5%|20.5%|20.5%|20.5%|20.5%|
|76.1%<br>|20.5%|20.5%|20.5%|17.4%|17.4%|17.4%|17.4%|17.4%|17.4%|



_Figure 5._ Tool-use distribution across models. GPT models rely
more on the code interpreter, while Gemini and Claude models use
web search most frequently.


**4. Further Analysis**

**4.1. Tool Distribution Analysis**

In this section, we analyze the distribution of tool calls
across models. As shown in Figure 5, the GPT-5 series
relies most heavily on the code interpreter. We further break
down code interpreter calls by operation type in Figure 6.
The results suggest that these models more often perform
image-centric operations during problem solving, such as
zooming in, cropping, resizing, measuring regions, and
carrying out structured extraction or calculations. Across
the inspected models, _crop_ is the most frequent operation,
indicating that many trajectories depend on localized visual
grounding before proceeding to retrieval or computation.
Second, the GEMINI and CLAUDE series call web search
most often, indicating a stronger preference for retrievaldriven workflows. Across all models, image search is used



less frequently than the other tools. In the next tool ablation
study, we quantify how each tool contributes to performance
and how accuracy changes when a tool is removed.


**4.2. Tool Ablation Study**


In this section, we ablate tool access to quantify how each
tool modality contributes to performance.
**Experimental** **setup.** We evaluate three settings with
prompts lightly adapted to reflect the available capabilities, while keeping the evaluation protocol and inference
hyperparameters fixed. ❶ **Vision** **only** : the agent has access only to a visual manipulation environment, enabling
image processing operations for inspection and transformation, but no external retrieval. ❷ **Search** **only** : the agent
can retrieve external evidence through both image-based
and text-based search, and can read retrieved webpages, but
cannot perform tool-based visual manipulation or programmatic verification. ❸ **No** **tool** : the agent relies purely on
direct generation without any tool assistance.


**Key findings.** Figure 7 shows that using the full tool suite
yields the best performance for both models, confirming
that AGENTVISTA rewards hybrid workflows that combine
visual manipulation and retrieval. For GEMINI-3-PRO, the
full tool setting reaches 27.27% accuracy, higher than the
vision-only setting at 20.10% and the no-tool setting at
18.18%. For CLAUDE-SONNET-4.5, the full tool setting
achieves 17.70%, slightly above the vision-only setting at
17.22%, while the search-only and no-tool settings both
drop to 13.40%. We also find that the role of retrieval differs
across models. For GEMINI-3-PRO, the search-only setting
reaches 26.32%, close to the full tool setting. This suggests
that its strong visual perception enables it to extract reliable
cues from images and benefit primarily from retrieval and
page navigation, while visual manipulation mainly supports
inspection and verification. In contrast, CLAUDE-SONNET


6


Grok-4



Gemini-3-Pro



GPT-5.2



**AgentVista**


Claude-Sonnet-4.5





































crop
calculation



loading display
editing



visualization
others



contrast
rotate



resize
brightness



_Figure 6._ Image manipulation operation distribution of code interpreter calls across four multimodal models. Tool usages are automatically
categorized into image-editing and analysis-related types. Across models, _crop_ is the most frequent operation, suggesting that many
interactions rely on localized visual grounding before further reasoning.



30


25


20


15


10


5


0



Gemini-3-Pro Claude-Sonnet-4.5















_Figure 7._ Tool ablation on GEMINI-3-PRO and CLAUDE-SONNET4.5. Both models perform best with the full tool suite, highlighting
the importance of combining visual manipulation and retrieval.


4.5 relies more on visual manipulation than retrieval, since
the vision-only setting remains close to the full tool setting,
whereas the search-only setting degrades substantially.


**4.3. Error Analysis**

To understand the main bottlenecks on AGENTVISTA, we
analyze failures from four representative models. For each
incorrect case, we assign an error label, including tool execution failure, visual misidentification, knowledge hallucination, calculation error, instruction misinterpretation, and
others. The labels are generated by GEMINI-3-FLASH based
on the model trajectories, and the distributions are shown
in Figure 8. Detailed definitions for each error type are
provided in Appendix C. Figure 8 shows a clear trend that
visual misidentification is the main failure mode across all
models. This aligns with the design of AGENTVISTA, where
tasks are grounded in realistic and cluttered visual states
and often depend on small but critical details. From bad
cases, we find that frontier agents can often zoom in to the
relevant region, but they still fail when the image is blurry
or the key cue is visually subtle. Knowledge hallucination
is the second most common error type, which also matches



_Table 4._ Test-time scaling results under different sampling budgets
_K_ on GEMINI-3-FLASH. We report Random1@ _K_ as a lower
bound, Best-of- _K_ (BoN@ _K_ ) selected by a reward model, and
Pass@ _K_ as an upper bound. All values are accuracies in %.


**SETTING** _K_ =1 _K_ =2 _K_ =4 _K_ =8 _K_ =16


**RANDOM1@** _K_ 21.05 19.11 18.23 17.09 18.05
**BON@** _K_ 21.05 24.88 26.32 28.23 30.62
**PASS@** _K_ 21.05 26.07 34.22 42.59 51.67


our benchmark design. Many tasks require applying diverse
world knowledge to long-horizon tool interactions, and current models still struggle to resolve long-tail facts reliably
even with web search. We include representative good and
bad cases with detailed explanations in Appendix D. Overall,
these results suggest that AGENTVISTA can expose practical
weaknesses in both fine-grained visual understanding and
knowledge-grounded reasoning under realistic tool use.


**4.4. Test Time Scaling**


To study whether additional sampling at test time can improve performance on AGENTVISTA, we evaluate test-time
scaling on GEMINI-3-FLASH. We generate _K_ independent
solutions per instance and use GEMINI-3-FLASH as the
reward model to select a final answer when selection is required. We follow the same evaluation protocol as in prior
experiments. Table 4 reports three settings: RANDOM1@ _K_,
which randomly selects one of the _K_ samples as a lower
bound, Best-of- _K_ (BON@ _K_ ), which selects the highestscoring sample under the reward model, and PASS@ _K_,
which measures whether at least one of the _K_ samples is
correct as an upper bound.


**Key** **findings.** Table 4 shows that test-time scaling consistently improves performance. Under BON, accuracy increases from 21.05% at _K_ =1 to 30.62% at _K_ =16. The
upper bound rises even more, with PASS@ _K_ increasing



7


Grok-4



Gemini-3-Pro



GPT-5.2



**AgentVista**


Claude-Sonnet-4.5











































tool execution failure
visual misidentification



knowledge hallucination
calculation error



instruction misinterpretation
others



_Figure 8._ Error category distribution on AGENTVISTA across four multimodal models. Error types are automatically labeled by GEMINI3-FLASH based on model trajectories. Across all models, _visual misidentification_ is the dominant failure mode, indicating that many
errors originate from incorrect grounding on fine-grained visual evidence.



from 21.05% at _K_ =1 to 51.67% at _K_ =16. In contrast,
RANDOM1@ _K_ remains low and does not improve with
larger _K_, indicating that gains mainly come from better
selection rather than sampling alone. Despite these improvements, scaling alone is not sufficient to solve AGENTVISTA.
Even at _K_ =16, BON reaches only 30.62%, while Pass@16
is 51.67%. This gap indicates substantial room for reinforcement learning or other optimization methods that can better
close the gap between selection and the achievable upper
bound, and more broadly highlights the need for stronger
long-horizon tool use and more reliable visual grounding.


**5. Related Work**


**5.1. Multimodal Agents and Tool Use**


Recent years have witnessed rapid progress in large multimodal models that combine visual perception with languagebased reasoning (Peng et al., 2023; Liu et al., 2023; Zhu
et al., 2023; Li et al., 2023). A key step toward practical multimodal agents is to couple these models with tools
so they can inspect visual evidence, verify intermediate
hypotheses, and refine solutions over multiple steps. OpenAI o3 and o4-mini follow this direction by manipulating
user-provided images during reasoning through operations
such as cropping, zooming, and rotation, and coordinating
these visual operations with other tools when needed (OpenAI, 2025f). This paradigm has inspired open systems that
study tool-driven multimodal reasoning and long-horizon
interaction (Su et al., 2025a;b). Recent work also explores
stronger training signals for repeated grounding, such as
reinforcement learning for interleaved perception and reasoning (Zheng et al., 2025), and extends multimodal agents
with web and code tools for mixed tool use in realistic settings (Hong et al., 2025; Geng et al., 2025). Despite this
progress, there is still no benchmark that evaluates generalist multimodal agents on realistic, ultra-challenging tasks.
AGENTVISTA fills this gap by focusing on long-horizon,



interleaved tool use grounded in real visual inputs.


**5.2. Multimodal Agent Benchmarks**


Early multimodal benchmarks mainly evaluate perception
and visual reasoning in static question answering, where
models respond from a fixed image and text context without interaction (Antol et al., 2015; Hudson & Manning,
2019; Lu et al., 2023; Yue et al., 2024b; Wang et al., 2024b).
While useful, they do not test whether an agent can choose
actions, call tools, and verify intermediate results. Recent
agent benchmarks add tool use, including multi-step planning (Ma et al., 2024), web browsing and search (Li et al.,
2025c; Tao et al., 2025), and tool-assisted visual reasoning
and active perception (Wu & Xie, 2024; Lai et al., 2025;
Li et al., 2025b; Ashraf et al., 2025). More recent works
further move toward interleaved tool settings, but the visual evidence is often relatively clean or lightweight, which
makes perception less demanding, and the resulting tool
trajectories tend to be shorter and less diverse (Guo et al.,
2025; Hong et al., 2025; Chen et al., 2026). AGENTVISTA
addresses this gap by emphasizing realistic visual inputs
and long-horizon workflows that require repeated visual
checking and interleaved use of multiple tool types.


**6. Conclusion**


We introduce AGENTVISTA, a benchmark for evaluating generalist multimodal agents on realistic, ultrachallenging tasks that require long-horizon, interleaved tool
use grounded in visual evidence. AGENTVISTA contains
209 tasks spanning 25 sub-domains across 7 categories,
with strict quality control to ensure vision-centric queries
and unique, verifiable answers. Experiments across frontier
models show that AGENTVISTA is far from solved: even
the best-performing model, GEMINI-3-PRO, reaches only
27.3% overall accuracy. The benchmark also elicits long interaction trajectories, with models such as GPT-5.2 averaging 13.85 tool turns per task, indicating substantial complex


8


**AgentVista**



ity beyond short tool chains. Further analysis highlights visual grounding and long-horizon tool use as key bottlenecks
for current multimodal agents. We hope AGENTVISTA
provides a practical benchmark for tracking progress and
motivates the development of multimodal agents that can
solve complex, multi-step real-world tasks more reliably.


**Impact Statement**


This work introduces AGENTVISTA, a benchmark for
evaluating generalist multimodal agents on realistic, ultrachallenging tasks that require long-horizon tool use
grounded in real visual inputs. By using concise, verifiable
answers and a controlled tool environment, AGENTVISTA
enables reproducible comparisons and helps identify key
bottlenecks in visual grounding, constraint tracking, and tool
reliability. Improved multimodal agents could benefit practical applications such as shopping assistance, travel planning,
and troubleshooting from user photos, where agents must
combine visual evidence with online information and computation. At the same time, stronger agents may increase
risks of privacy leakage from user-provided images and
overconfident but incorrect outputs in real deployments. We
mitigate these concerns by filtering and rewriting tasks to
avoid personal identifiers when applicable, and by emphasizing short answers that encourage checkable evaluation
rather than persuasive free-form text.


Benchmark construction can also reflect biases from source
data and annotator decisions, which may affect coverage
across domains and scenarios. We hope AGENTVISTA supports future work on more robust and responsible multimodal agents by providing a shared evaluation target for
realistic, long-horizon tool use.


**References**


Anthropic. Introducing Claude Opus 4.1: State-of-the-Art
High-Performance Multimodal AI. [https://www.](https://www.anthropic.com/news/claude-opus-4-1)
[anthropic.com/news/claude-opus-4-1,](https://www.anthropic.com/news/claude-opus-4-1)
2025a.


Anthropic. Introducing claude 4: Sonnet 4 and
opus 4. [https://www.anthropic.com/news/](https://www.anthropic.com/news/claude-4)
[claude-4, 2025b.](https://www.anthropic.com/news/claude-4)


Anthropic. Introducing claude sonnet 4.5. [https://www.](https://www.anthropic.com/news/claude-sonnet-4-5)
[anthropic.com/news/claude-sonnet-4-5,](https://www.anthropic.com/news/claude-sonnet-4-5)
2025c.


Antol, S., Agrawal, A., Lu, J., Mitchell, M., Batra, D.,
Zitnick, C. L., and Parikh, D. Vqa: Visual question
answering. In _Proceedings_ _of_ _the_ _IEEE_ _International_
_Conference on Computer Vision_, December 2015.


Ashraf, T., Saqib, A., Ghani, H., AlMahri, M., Li, Y., Ahsan,



N., Nawaz, U., Lahoud, J., Cholakkal, H., Shah, M., et al.
Agent-x: Evaluating deep multimodal reasoning in visioncentric agentic tasks. _arXiv preprint arXiv:2505.24876_,
2025.


Bai, S., Cai, Y., Chen, R., Chen, K., Chen, X., Cheng,
Z., Deng, L., et al. Qwen3-VL technical report. _arXiv_
_preprint_ _arXiv:2511.21631_, 2025. URL [https://](https://arxiv.org/abs/2511.21631)
[arxiv.org/abs/2511.21631.](https://arxiv.org/abs/2511.21631)


Chen, J., Shen, X., Zheng, L., Shao, Z., Cui, H., Du, C.,
Gong, L., Gu, F., Hao, X., He, W., He, J., Hu, Y., Huang,
B., Li, S., Li, Q., Luo, J., Liu, Z., Liu, X., Mao, N., Mu,
L., Pan, X., Qu, Z., Ren, C., Rao, X., Sun, H., Wang,
Q., Wang, S., Wang, Z., Wang, W., Wen, L., Zhan, J.,
Yang, H., Yang, S., Yang, J., Yu, P., Zhang, H., Zhang,
B., Zhou, C., Zhou, Z., Zhou, S., Xie, S., Zhu, Y., Ma, H.,
Wei, T., Zhou, P., and Chen, W. Mindwatcher: Toward
smarter multimodal tool-integrated reasoning, 2026. URL
[https://arxiv.org/abs/2512.23412.](https://arxiv.org/abs/2512.23412)


Chou, C., Dunlap, L., Mashita, K., Mandal, K., Darrell, T.,
Stoica, I., Gonzalez, J. E., and Chiang, W.-L. Visionarena:
230k real world user-vlm conversations with preference
labels. In _Proceedings of the Computer Vision and Pattern_
_Recognition Conference_, pp. 3877–3887, 2025.


Comanici, G., Bieber, E., Schaekermann, M., Pasupat, I.,
Sachdeva, N., Dhillon, I., Blistein, M., Ram, O., Zhang,
D., Rosen, E., et al. Gemini 2.5: Pushing the frontier
with advanced reasoning, multimodality, long context,
and next generation agentic capabilities. _arXiv preprint_
_arXiv:2507.06261_, 2025.


Geng, X., Xia, P., Zhang, Z., Wang, X., Wang, Q., Ding, R.,
Wang, C., Wu, J., Zhao, Y., Li, K., et al. Webwatcher:
Breaking new frontier of vision-language deep research
agent. _arXiv preprint arXiv:2508.05748_, 2025.


Google DeepMind. Gemini 3 flash: frontier intelligence built for speed. [https://blog.google/](https://blog.google/products/gemini/gemini-3-flash/)
[products/gemini/gemini-3-flash/, 2025a.](https://blog.google/products/gemini/gemini-3-flash/)


Google DeepMind. A new era of intelligence with gemini
[3. https://blog.google/products/gemini/](https://blog.google/products/gemini/gemini-3/)
[gemini-3/, 2025b.](https://blog.google/products/gemini/gemini-3/)


Guo, X., Tyagi, U., Gosai, A., Vergara, P., Park, J., Montoya, E. G. H., Zhang, C. B. C., Hu, B., He, Y., Liu, B.,
et al. Beyond seeing: Evaluating multimodal llms on toolenabled image perception, transformation, and reasoning.
_arXiv preprint arXiv:2510.12712_, 2025.


Hong, J., Zhao, C., Zhu, C., Lu, W., Xu, G., and Yu, X.
Deepeyesv2: Toward agentic multimodal model. _arXiv_
_preprint arXiv:2511.05271_, 2025.



9


**AgentVista**



Hudson, D. A. and Manning, C. D. Gqa: A new dataset for
real-world visual reasoning and compositional question
answering. In _Proceedings of the IEEE/CVF Conference_
_on Computer Vision and Pattern Recognition_, June 2019.


Lai, X., Li, J., Li, W., Liu, T., Li, T., and Zhao, H. Mini-o3:
Scaling up reasoning patterns and interaction turns for
visual search. _arXiv preprint arXiv:2509.07969_, 2025.


Li, J., Li, D., Savarese, S., and Hoi, S. Blip-2: Bootstrapping
language-image pre-training with frozen image encoders
and large language models. In _International conference_
_on machine learning_, pp. 19730–19742. PMLR, 2023.


Li, J., Zhao, W., Zhao, J., Zeng, W., Wu, H., Wang, X.,
Ge, R., Cao, Y., Huang, Y., Liu, W., et al. The tool
decathlon: Benchmarking language agents for diverse,
realistic, and long-horizon task execution. _arXiv preprint_
_arXiv:2510.25726_, 2025a.


Li, M., Zhong, J., Zhao, S., Zhang, H., Lin, S., Lai, Y.,
Chen, W., Psounis, K., and Zhang, K. Tir-bench: A comprehensive benchmark for agentic thinking-with-images
reasoning. _arXiv preprint arXiv:2511.01833_, 2025b.


Li, S., Bu, X., Wang, W., Liu, J., Dong, J., He, H., Lu, H.,
Zhang, H., Jing, C., Li, Z., Li, C., Tian, J., Zhang, C.,
Peng, T., He, Y., Gu, J., Zhang, Y., Yang, J., Zhang, G.,
Huang, W., Zhou, W., Zhang, Z., Ding, R., and Wen,
S. Mm-browsecomp: A comprehensive benchmark for
multimodal browsing agents, 2025c. [URL https://](https://arxiv.org/abs/2508.13186)
[arxiv.org/abs/2508.13186.](https://arxiv.org/abs/2508.13186)


Liu, H., Li, C., Wu, Q., and Lee, Y. J. Visual instruction tuning. _Advances in neural information processing systems_,
36:34892–34916, 2023.


Lu, P., Bansal, H., Xia, T., Liu, J., Li, C., Hajishirzi,
H., Cheng, H., Chang, K.-W., Galley, M., and Gao,
J. Mathvista: Evaluating mathematical reasoning of
foundation models in visual contexts. _arXiv_ _preprint_
_arXiv:2310.02255_, 2023.


Lu, Y., Jiang, D., Chen, W., Wang, W. Y., Choi, Y., and Lin,
B. Y. Wildvision: Evaluating vision-language models in
the wild with human preferences. _Advances_ _in_ _Neural_
_Information Processing Systems_, 37:48224–48255, 2024.


Ma, Z., Huang, W., Zhang, J., Gupta, T., and Krishna, R.
m & m’s: A benchmark to evaluate tool-use for m ultistep m ulti-modal tasks. In _European_ _Conference_ _on_
_Computer Vision_, pp. 18–34. Springer, 2024.


OpenAI. Introducing openai o3 and o4mini. [https://openai.com/index/](https://openai.com/index/introducing-o3-and-o4-mini/)
[introducing-o3-and-o4-mini/, 2025a.](https://openai.com/index/introducing-o3-and-o4-mini/)



OpenAI. Introducing gpt-5. [https://openai.com/](https://openai.com/index/introducing-gpt-5/)
[index/introducing-gpt-5/, 2025b.](https://openai.com/index/introducing-gpt-5/)


OpenAI. Gpt-4.1: Enhanced coding and instruction following. [https://openai.com/index/gpt-4-1/,](https://openai.com/index/gpt-4-1/)
2025c. Released April 14, 2025.


OpenAI. Gpt-5.1: A smarter, more conversational chatgpt. [https://openai.com/index/gpt-5-1/,](https://openai.com/index/gpt-5-1/)
2025d.


OpenAI. Introducing gpt-5.2. [https://openai.com/](https://openai.com/index/introducing-gpt-5-2/)
[index/introducing-gpt-5-2/, 2025e.](https://openai.com/index/introducing-gpt-5-2/)


OpenAI. OpenAI o3 and o4-mini system card. System card,
OpenAI, April 2025f. [URL https://cdn.openai.](https://cdn.openai.com/papers/o3-o4-mini-system-card.pdf)
[com/papers/o3-o4-mini-system-card.pdf.](https://cdn.openai.com/papers/o3-o4-mini-system-card.pdf)
Released April 16, 2025.


Peng, Z., Wang, W., Dong, L., Hao, Y., Huang, S., Ma,
S., and Wei, F. Kosmos-2: Grounding multimodal
large language models to the world. _arXiv_ _preprint_
_arXiv:2306.14824_, 2023.


Scale AI. Vista: Visual–language understanding leaderboard. [https://scale.com/leaderboard/](https://scale.com/leaderboard/visual_language_understanding)
[visual_language_understanding, 2025.](https://scale.com/leaderboard/visual_language_understanding)


Stein, B. E. _The new handbook of multisensory processing_ .
Mit Press, 2012.


Su, Z., Li, L., Song, M., Hao, Y., Yang, Z., Zhang, J., Chen,
G., Gu, J., Li, J., Qu, X., et al. Openthinkimg: Learning to
think with images via visual tool reinforcement learning.
_arXiv preprint arXiv:2505.08617_, 2025a.


Su, Z., Xia, P., Guo, H., Liu, Z., Ma, Y., Qu, X., Liu, J., Li,
Y., Zeng, K., Yang, Z., et al. Thinking with images for
multimodal reasoning: Foundations, methods, and future
frontiers. _arXiv preprint arXiv:2506.23918_, 2025b.


Tao, X., Teng, Y., Su, X., Fu, X., Wu, J., Tao, C., Liu, Z., Bai,
H., Liu, R., and Kong, L. Mmsearch-plus: Benchmarking
provenance-aware search for multimodal browsing agents.
_arXiv preprint arXiv:2508.21475_, 2025.


Team, K., Bai, T., Bai, Y., Bao, Y., Cai, S., Cao, Y., Charles,
Y., Che, H., Chen, C., Chen, G., et al. Kimi k2. 5: Visual
agentic intelligence. _arXiv preprint arXiv:2602.02276_,
2026.


Wang, L., Ma, C., Feng, X., Zhang, Z., Yang, H., Zhang, J.,
Chen, Z., Tang, J., Chen, X., Lin, Y., et al. A survey on
large language model based autonomous agents. _Frontiers_
_of Computer Science_, 18(6):186345, 2024a.


Wang, W., Ding, L., Zeng, M., Zhou, X., Shen, L., Luo, Y.,
Yu, W., and Tao, D. Divide, conquer and combine: A



10


**AgentVista**



training-free framework for high-resolution image perception in multimodal large language models. In _Proceed-_
_ings_ _of_ _the_ _AAAI_ _Conference_ _on_ _Artificial_ _Intelligence_,
volume 39, pp. 7907–7915, 2025.


Wang, Z., Xia, M., He, L., Chen, H., Liu, Y., Zhu, R., Liang,
K., Wu, X., Liu, H., Malladi, S., et al. Charxiv: Charting
gaps in realistic chart understanding in multimodal llms.
_Advances in Neural Information Processing Systems_, 37:
113569–113697, 2024b.


Wei, J., Sun, Z., Papay, S., McKinney, S., Han, J., Fulford,
I., Chung, H. W., Passos, A. T., Fedus, W., and Glaese,
A. Browsecomp: A simple yet challenging benchmark
for browsing agents. _arXiv preprint arXiv:2504.12516_,
2025.


Wu, P. and Xie, S. V*: Guided visual search as a core
mechanism in multimodal llms. In _Proceedings_ _of_ _the_
_IEEE/CVF Conference on Computer Vision and Pattern_
_Recognition_, pp. 13084–13094, 2024.


xAI. Grok-4. [https://x.ai/news/grok-4, 2025.](https://x.ai/news/grok-4)


Xie, T., Zhang, D., Chen, J., Li, X., Zhao, S., Cao, R., Hua,
T. J., Cheng, Z., Shin, D., Lei, F., et al. Osworld: Benchmarking multimodal agents for open-ended tasks in real
computer environments. _Advances in Neural Information_
_Processing Systems_, 37:52040–52094, 2024.


Yang, J., Jimenez, C. E., Zhang, A. L., Lieret, K., Yang,
J., Wu, X., Press, O., Muennighoff, N., Synnaeve, G.,
Narasimhan, K. R., Yang, D., Wang, S. I., and Press,
O. Swe-bench multimodal: Do ai systems generalize
to visual software domains?, 2024. URL [https://](https://arxiv.org/abs/2410.03859)
[arxiv.org/abs/2410.03859.](https://arxiv.org/abs/2410.03859)


Yue, X., Ni, Y., Zhang, K., Zheng, T., Liu, R., Zhang, G.,
Stevens, S., Jiang, D., Ren, W., Sun, Y., Wei, C., Yu, B.,
Yuan, R., Sun, R., Yin, M., Zheng, B., Yang, Z., Liu, Y.,
Huang, W., Sun, H., Su, Y., and Chen, W. Mmmu: A
massive multi-discipline multimodal understanding and
reasoning benchmark for expert agi. In _Proceedings of the_
_IEEE/CVF Conference on Computer Vision and Pattern_
_Recognition_, pp. 9556–9567, June 2024a.


Yue, X., Ni, Y., Zhang, K., Zheng, T., Liu, R., Zhang, G.,
Stevens, S., Jiang, D., Ren, W., Sun, Y., et al. Mmmu: A
massive multi-discipline multimodal understanding and
reasoning benchmark for expert agi. In _Proceedings of the_
_IEEE/CVF Conference on Computer Vision and Pattern_
_Recognition_, pp. 9556–9567, 2024b.


Zheng, Z., Yang, M., Hong, J., Zhao, C., Xu, G., Yang, L.,
Shen, C., and Yu, X. Deepeyes: Incentivizing” thinking
with images” via reinforcement learning. _arXiv preprint_
_arXiv:2505.14362_, 2025.



Zhu, D., Chen, J., Shen, X., Li, X., and Elhoseiny, M.
Minigpt-4: Enhancing vision-language understanding
with advanced large language models. _arXiv_ _preprint_
_arXiv:2304.10592_, 2023.



11


**AgentVista**


**A. AGENTVISTA Details**


**A.1. Dataset Taxonomy of AGENTVISTA**


AGENTVISTA covers seven major categories: (1) **Technology**, which includes hardware troubleshooting, engineering
analysis, and system configuration grounded in real photos, screenshots, and diagrams; (2) **Commerce**, which includes
product selection, pricing and budget calculation, and finance-related reasoning under practical constraints; (3) **Geography**,
which includes route planning, map interpretation, location identification, and spatial calculations; (4) **Entertainment**, which
includes sports analytics, media and hobby curation, and game-related reasoning; (5) **Society**, which includes everyday tasks
such as health and culinary decisions, home maintenance, manual assembly troubleshooting, and plant care; (6) **Academics**,
which includes mathematical computation, scientific identification, and data analysis; and (7) **Culture**, which includes
cultural knowledge, history-related understanding, and artifact appraisal grounded in visual evidence.


**A.2. Data Sources**


All AGENTVISTA instances are grounded in real images and real user needs. Across all sources, we apply a unified set of
criteria. We retain only images with sufficient visual detail to support non-trivial reasoning, and we exclude cases where the
solution can be obtained by directly searching the query text or by retrieving the same image and question from the public
web. We curate candidates from three channels.


**Public user-submitted arenas.** We collect image-based user submissions from public vision-language model arenas,
including VisionArena and WildVision (Chou et al., 2025; Lu et al., 2024). This source provides 284.4K images with
diverse real-world scenes. We first apply an automated filter using CLAUDE-OPUS-4.1 to remove images with limited
visual information and cases that do not fit agentic problem settings. The filter also proposes a candidate task query that
reflects the plausible action space. The prompt is shown in Appendix B.3.1. Human annotators then select high-quality
candidates for downstream curation.


**Annotator-captured real-life scenarios.** We also include tasks collected by annotators from real daily situations, together
with the original photos or screenshots that motivated the request. This channel naturally captures practical constraints,
such as cluttered scenes, partial evidence, and ambiguous context, which are common in real deployments. We treat these
instances as first-party user needs and keep their intent while ensuring the final task remains self-contained.


**Private community forums.** We also curate candidates from community help-seeking forums. We collect posts that
include visually informative images and reflect realistic user goals. Since these posts often contain lengthy discussions and
personal details, we rewrite each case into a standalone task while preserving the original intent and removing identifying
information. We apply stricter screening to ensure clarity and consistency with our benchmark standards.


**B. Experimental Details**


**B.1. Tool Definition**


AGENTVISTA is evaluated in a controlled tool environment with a compact set of commonly used tools for multimodal agent
workflows. Models can invoke these tools appropriately within the <tool ~~c~~ all>...</tool ~~c~~ all> block during
interaction. In detail, our tools are defined as follows.





12


**AgentVista**







13


**AgentVista**


**B.2. Analysis of open-source model results.**


_Table 5._ Results of representative open-source models on AGENTVISTA by category. Domain abbreviations: **COMM.** (Commerce),
**GEOG.** (Geography), **ENT.** (Entertainment), **TECH.** (Technology), **SOC.** (Society), **ACAD.** (Academics), and **CULT.** (Culture). The
best-performing model in each category is **in-bold**, and the second best is underlined. All values are accuracies in %.


**MODEL** **COMM.** **GEOG.** **ENT.** **TECH.** **SOC.** **ACAD.** **CULT.** **OVERALL**


QWEN3-VL-235B 7.14 7.69 **7.69** **26.47** 16.00 **20.00** 13.33 **12.92**
DEEPEYES-V2-7B **9.52** **10.26** 2.56 14.71 **24.00** 6.67 **20.00** 11.48
WEBWATCHER-32B 0.00 **10.26** 0.00 23.53 **24.00** **20.00** 0.00 10.05


Table 5 reports results for three representative open-source multimodal models. In particular, DEEPEYES-V2-7B (Hong
et al., 2025) and WEBWATCHER-32B (Geng et al., 2025) are tool-using open-source agents that can interact with external
tools to support multi-step problem solving, while QWEN3-VL-235B serves as a strong open-source multimodal backbone.
Overall, these open-source baselines remain far from solving AGENTVISTA, i.e., their overall accuracy ranges from 10.05%
to 12.92%, substantially lower than the best-performing model GEMINI-3-PRO at 27.3%. This gap further reflects the
ultra-challenging nature of AGENTVISTA and highlights the large room for improving open-source multimodal agents.


**B.3. Prompts**


B.3.1. PROMPTS FOR DATA CONSTRUCTION





14


**AgentVista**





B.3.2. THE PROMPT FOR EVALUATION







**C. Error type definitions.**


In Section 4.3, we report the error distributions of representative models on AGENTVISTA. Here we define the error types
used in our taxonomy.


**Tool** **execution** **failure.** This category captures cases where the agent follows a plan, but fails due to issues in tool
interaction. Typical examples include empty tool outputs, invalid requests, and failures to open or parse retrieved content.
These errors suggest that robust tool use and self-checking are important for completing long-horizon workflows.


**Visual misidentification.** This category includes errors caused by incorrect visual understanding, such as reading the
wrong text on a label, confusing similar components, missing a small indicator, or miscounting objects. Because visual


15


**AgentVista**


evidence often determines what to search for and how to apply constraints, a single perception mistake can cause later steps
to follow an incorrect direction.


**Knowledge** **hallucination.** This category refers to cases where the agent outputs facts that are not supported by the
provided images or retrieved sources. Common patterns include inventing details that look plausible, relying on generic rules
of thumb, or asserting standards that do not match the evidence in the current instance. These failures indicate insufficient
grounding in the multimodal context.


**Calculation error.** This category covers mistakes in arithmetic or multi-step aggregation, such as wrong unit conversions,
incorrect date computations, or errors when combining multiple retrieved values. These cases often arise after several steps,
when the agent must keep intermediate numbers consistent while continuing to use tools.


**Instruction misinterpretation.** This category includes failures to follow the user request or constraints, such as ignoring a
time window, missing a required format, applying the wrong condition, or answering a related but different question. Even
when perception and retrieval are correct, misunderstanding the intent can still lead to an incorrect final answer.


**Others.** This category groups remaining failures that do not fit the above types or that involve multiple types without a
clear primary cause. Examples include incomplete final answers, premature termination, inconsistent outputs across steps,
or cases where the model produces an answer that cannot be checked against the required format. We use this bucket to keep
the taxonomy simple while still accounting for long-tail error patterns.


**D. Case Study**


In this section, we present representative trajectories to illustrate both successful and failed behaviors on AGENTVISTA. We
first show a good-case example that demonstrates effective long-horizon, interleaved tool use. We then provide one bad-case
example for each error type, highlighting how different failure modes arise and how they derail the overall workflow.


**D.1. Good Case Examples**


**Traj** **#1:** **Sneaker** **Authentication.** This task involved verifying the authenticity of luxury sneakers based on visual
evidence. Through a sequence of seven tool invocations, the model conducted a systematic examination of specific features.
It utilized Image Search to contrast tongue and size tags with authentic references, identifying an anomalous ”A8513”
sticker. Subsequent validation via Web Search confirmed this as a counterfeit indicator, leading to the correct classification.


**Traj #2:** **Strongest German Beer Analysis.** Identifying the strongest beer required distinguishing specific brands within
a cluttered image. The model synergized the Code Interpreter for visual refinement with Web Search for factual retrieval.
This approach enabled the precise filtering of lower-alcohol options, resulting in the accurate identification of a tie between
Steam Brew German Red and Perlenbacher Strong.


**Traj #1:** **Sneaker Authentication (GEMINI-3-PRO; success; 7 tool calls)**


**Task.** Acting as a luxury sneaker authenticator, search for authentic craftsmanship images for comparison. Decide whether the
shoes are **Real** or **Fake**, and give at least two visual reasons.

_Input images._


**Ground truth.** Counterfeit. Key cues include Widow’s Peak Error, Poor Tongue Font & Stitching, Misaligned 3M Stripes.


16


**AgentVista**


**Tool trajectory (condensed).**
**Step 1.** _web search_
Query: Dior B30 black sneaker authentic vs fake guide
**Evidence.** Retrieved legit-check guides that highlight tongue tag font, stitching, and interior label formats as key checks.

**Step 2.** _image search_
Query: authentic Dior B30 black sneaker tongue tag
**Evidence.** Collected reference images for tongue tag layout and font.


**Step 3.** _image search_
Query: authentic Dior B30 sneaker inside size tag label
**Evidence.** Collected reference images for inside label formats and placement.


**Step 4.** _web search_
Query: Dior B30 authentic inner size code format
**Evidence.** Guides report authentic style identifiers follow a structured style-ID pattern, rather than generic sticker-like codes.

**Step 5.** _image search_
Query: fake Dior B30 size sticker A8513
**Evidence.** Collected examples where generic interior stickers are associated with replicas.


**Final decision.** **Fake.**
**Reasons.**

- The interior sticker code format is inconsistent with authentic labeling patterns shown in retrieved references.


- The tongue tag font and stitching do not match the authentic reference images. ✓


**Traj #2:** **Strongest German Beer Analysis (GEMINI-3-PRO; success; 7 tool calls)**


**Task.** From the beers shown in the photo, consider only German-brewed beers with ABV _>_ 5%. Which **brand** has the highest
**total alcohol per can**, accounting for both ABV and can volume?

_Input image._


17


**AgentVista**


**Ground truth.** **Steam Brew German Red** and **Perlenbacher Strong** (tie).


**Tool trajectory (condensed).**
**Step 1.** _code interpreter_
**Evidence.** Zoomed and cropped the photo to read brand names and the ABV/volume information on the cans.


**Step 2.** _web search_
Query: Perlenbacher Strong ABV Steam Brew German Red ABV
**Evidence.** Retrieved product pages confirming both beers are **7.9% ABV** .

**Step 3.** _code interpreter_
**Evidence.** Cropped individual cans to verify they are German-brewed and to confirm can capacity (standard tall can).


**Step 4.** _web search_
Query: Steam Brew German Red volume 500ml
**Evidence.** Confirmed the can size used for calculation is **500 ml** .

**Step 5.** _image search_
**Evidence.** Attempted to identify other cans/variants; no higher-ABV German-brewed option was found among the eligible beers.

**Step 6.** _web search_
Query: Steam Brew German Red ABV exact Perlenbacher Strong ABV
**Evidence.** Cross-checked ABV values and resolved remaining ambiguity.


**Final decision.** **Tie:** **Steam Brew German Red and Perlenbacher Strong.**
**Reason.** Both are German-brewed, exceed 5% ABV, and have the same alcohol per can: 0 _._ 079 _×_ 500 ml = 39 _._ 5 ml. ✓


18


**AgentVista**


**D.2. Bad Case Examples**


**Traj #3:** **Karst Jigsaw Puzzle.** _**Tool execution failure**_ **.** **Task.** Reconstruct a 6 _×_ 6 jigsaw puzzle from an input image
and locate the missing piece position. **Failure.** The model attempted to segment puzzle pieces with code-based image
processing, but the segmentation failed and extracted only 24 segments instead of the expected 35. Without a complete set
of pieces, the model could not form a valid grid and the reconstruction became infeasible. **Classification Rationale.** The
core issue is a breakdown in tool-based image processing, which blocks the workflow even though the high-level plan is
reasonable.


**Traj #4:** **Authors United Window Display.** _**Visual misidentification**_ **.** **Task.** Identify the author shown in a window
display from the provided image. **Failure.** The visible author is Donna Tartt, but the model failed to identify her. Although
it performed cropping, it still did not extract the correct visual cue and produced an incorrect identification. **Classification**
**Rationale.** The decisive evidence is in the image, and the failure comes from incorrect visual recognition rather than
retrieval or reasoning.


**Traj #5:** **Target Arena Identification.** _**Visual misidentification**_ **.** **Task.** Identify the correct university basketball facility
shown in the image. **Failure.** The model misread an unclear floor logo and anchored on the wrong university, then reinforced
the mistake using generic features such as roof trusses. It concluded the venue was St. Thomas AARC, while the correct
answer is UNC. **Classification Rationale.** The initial mistake is a wrong visual anchor, and later steps follow that incorrect
anchor.


**Traj** **#6:** **Pilea** **Root** **Diagnosis.** _**Knowledge**_ _**hallucination**_ **.** **Task.** Diagnose the hard mass on Pilea roots from the
image. **Failure.** The correct interpretation is calloused residue from root rot, but the model claimed it was a “nursery
plug” or fungal material and described visual properties that are not supported by the image. The final diagnosis followed
a made-up interpretation aligned with retrieval results rather than the provided evidence. **Classification Rationale.** The
model introduces unsupported facts and forces the image to fit a preconceived explanation.


**Traj #7:** **Studio Swing Prop Design.** _**Instruction misinterpretation**_ **.** **Task.** Design a stationary photo prop that visually
looks like a suspended swing. **Failure.** The model proposed a design where the seat is visibly supported by a horizontal bar,
which removes the hanging illusion and violates the core constraint of the request. **Classification Rationale.** The model
fails to follow the key constraint and answers a different problem than the one asked.


**Traj #3:** **Karst Jigsaw Puzzle (GEMINI-3-PRO; failed; 3 tool calls)**


**Task.** The first image shows a 6 _×_ 6 jigsaw puzzle (one piece missing) made from a karst-landform photo. The second image is a
local reference landscape photo. Reconstruct the puzzle and report the coordinate of the missing piece. Coordinates are defined
on the reconstructed grid: top-left is (1 _,_ 1), top-right is (1 _,_ 6), and bottom-right is (6 _,_ 6).

_Input images._


**Ground truth.** (3 _,_ 1)


**Tool trajectory (condensed).**
**Step 1.** _code interpreter_
**Goal.** Segment the puzzle into individual pieces and assign each piece to a grid cell.
**Outcome.** The segmentation merges adjacent pieces and fails to recover all pieces.


19


**AgentVista**


**Step 2.** _code interpreter_
**Goal.** Improve segmentation with morphological operations and contour filtering.
**Outcome.** Still under-segments the puzzle and extracts only **24** regions, instead of the expected **35** pieces (or 36 slots).


**Step 3.** _code interpreter_
**Goal.** Crop and visualize the extracted pieces for downstream matching.
**Outcome.** Visualization confirms missing segments; reconstruction cannot proceed.


**Failure point.** **Step 2 (segmentation).** The model cannot reliably separate touching pieces, so it fails to obtain a complete set of
puzzle pieces. Without correct piece extraction, subsequent grid reconstruction and missing-cell identification are not feasible.


**Final outcome.** The model fails to reconstruct the 6 _×_ 6 layout and cannot determine the missing coordinate. ✗


20


**AgentVista**


**Traj #4:** **Authors United Window Display (GEMINI-3-PRO; failed; 13 tool calls)**


**Task.** This photo shows a bookstore window display supporting “Authors United,” featuring photos of authors who have appeared
at the bookstore. Among the authors whose photos are clearly visible in the display, identify the author whose work stayed on
_The New York Times_ Bestseller List for the most total weeks during the years when “Authors United” was most active. Report the
author, the work, and the total weeks.

_Input image._


**Ground truth.** Donna Tartt; _The Goldfinch_ ; 39 weeks.


**Tool trajectory (condensed).**
**Step 1.** _web search_
**Goal.** Identify the bookstore and locate a source describing the window display.
**Outcome.** Finds a relevant local article about the display.
**Step 2.** _visit_
**Goal.** Read the article and recover the set of authors shown in the display.
**Outcome.** The page provides context but does not yield a complete, reliable list of the visible authors.
**Step 3.** _code interpreter_
**Goal.** Extract author names from the image via OCR.
**Outcome.** OCR is noisy and incomplete; text cues are not recovered reliably.
**Step 4.** _code interpreter_
**Goal.** Crop the window display into smaller regions to identify individual authors.
**Outcome.** Produces multiple crops, but faces and cover details remain ambiguous at this resolution.


**Steps 5–9.** _image search / web search / visit_
**Goal.** Identify cropped portraits and posters (e.g., “READ” poster) via reverse search and related pages.
**Outcome.** Reverse search does not return actionable matches; the model cannot reliably map crops to specific authors.


21


**AgentVista**


**Steps 10–13.** _web search_
**Goal.** Estimate the correct answer by comparing bestseller-list durations among guessed candidates.
**Outcome.** The model anchors on the wrong author set and proceeds with an incorrect comparison.


**Failure point.** **Step 4 (visual identification).** Even after cropping, the model fails to correctly identify the clearly visible author
(Donna Tartt) from the display. This incorrect visual grounding leads to downstream searches and bestseller comparisons over
the wrong candidate set, culminating in an incorrect final answer.


**Final answer.** Anthony Doerr; _All the Light We Cannot See_ ; _∼_ 84 weeks. ✗


**Traj #5:** **Target Arena Identification (GEMINI-3-PRO; failed; 11 tool calls)**


**Task.** A colleague referenced this venue only as “Target Arena A.” Identify exactly which university facility is shown so the
correct team metadata (e.g., seating capacity, fan distribution) can be linked in a database.

_Input image._


**Ground truth.** UNC


**Tool trajectory (condensed).**
**Step 1.** _code interpreter_
**Goal.** Inspect the full scene and locate the most informative identifiers (court logo, scoreboard, signage).
**Outcome.** The model focuses on the floor logo and plans to use it for identification.
**Step 2.** _code interpreter_
**Goal.** Crop the court logo and scoreboard region for downstream search.
**Outcome.** Produces a small, low-detail logo crop (insufficient for reliable matching).


**Step 3.** _image search (reverse)_
**Goal.** Identify the venue or team via reverse search on the cropped logo.
**Outcome.** No matches returned.
**Step 4.** _code interpreter_
**Goal.** Re-crop the logo with more context.
**Outcome.** The crop remains ambiguous and visually distorted.


**Step 5.** _image search (reverse)_
**Goal.** Retry reverse search with the updated crop.
**Outcome.** Still no matches.


22


**AgentVista**


**Step 6.** _web search_
**Goal.** Use structural cues (exposed truss ceiling, running track/balcony) to narrow candidates.
**Outcome.** Returns generic lists; does not provide a grounded identification.
**Step 7.** _code interpreter_
**Goal.** Enhance contrast/sharpness of the logo crop to clarify the mascot shape.
**Outcome.** Enhancement does not resolve the mascot identity.


**Step 8.** _image search (reverse)_
**Goal.** Reverse search the enhanced crop.
**Outcome.** No matches.
**Step 9.** _image search (text)_
**Goal.** Pivot to a guessed candidate (University of St. Thomas AARC) based on weak visual similarity.
**Outcome.** Retrieves reference images for comparison.
**Step 10.** _image search (text)_
**Goal.** Expand references (Schoenecker Arena / AARC interiors) and match architecture.
**Outcome.** The model over-weights generic ceiling/track similarities.
**Step 11.** _image search (text)_
**Goal.** Final confirmation via additional reference images.
**Outcome.** Commits to the incorrect university.


**Failure point.** **Step 9 (incorrect anchoring).** After failing to identify the floor logo, the model switches to architecture-based
matching and prematurely anchors on St. Thomas. The remaining steps reinforce this guess using generic similarities (trusses,
ducts, balcony/track) rather than a definitive visual identifier from the query image, leading to an incorrect final answer.


**Final answer.** University of St. Thomas (Minnesota) ✗


**Traj #6:** **Pilea Root Diagnosis (GEMINI-3-PRO; failed; 6 tool calls)**


**Task.** A Pilea was overwatered two months ago and later stabilized. During repotting, a large white mass is found at the root
base; it is hard and crusty (does not burst when poked). Based on the images and history, identify the substance and decide
whether pesticides are needed.

_Input images._


**Ground truth.** No pesticide needed. The mass is calloused / crustified root-rot residue from the prior overwatering incident.


**Tool trajectory (condensed).**
**Step 1.** _web search_
**Goal.** Identify common causes of a hard white mass near Pilea roots.
**Outcome.** Results skew toward unrelated “white spots” / mineral topics (mostly leaf-focused).
**Step 2.** _web search_
**Goal.** Broaden to generic houseplant root “white lump” explanations.
**Outcome.** Mixed hypotheses (mineral buildup, mold/fungus) without matching the specific context.
**Step 3.** _image search_


23


**AgentVista**


**Goal.** Look up nursery-plug examples as an alternative explanation.
**Outcome.** Retrieves plug images that encourage an external “plug/mesh” hypothesis.
**Step 4.** _web search_
**Goal.** Explore other possibilities (e.g., slime mold / residue) from search cues.
**Outcome.** Finds generic statements that crusty residue can occur, but without strong alignment to an underground root-base
mass.
**Step 5.** _web search_
**Goal.** Re-search with Pilea-specific phrasing to confirm the plug/mesh theory.
**Outcome.** Surfacing discussions about “root mesh / death plugs” further reinforces the plug narrative.
**Step 6.** _web search_
**Goal.** Finalize between plug/mesh vs. plant-tissue explanation.
**Outcome.** Commits to “nursery plug + dried fungus” as the main explanation.


**Failure point.** **Step 3 (incorrect hypothesis shift).** After early searches returned noisy, non-root-specific results, the model
pivots to an external “nursery plug / mesh” explanation based on loosely similar reference images. This guess then becomes the
anchor and is reinforced by subsequent searches, while the overwatering history and root-location cue (consistent with healed
root damage) are underweighted.


**Final answer.** A nursery plug (“death plug”) encrusted/colonized by dried saprophytic fungus; no pesticides. ✗


**Traj #7:** **Swing Prop Construction (GEMINI-3-PRO; direct response)**


**Task.** Build a swing prop for a children’s photography studio that _looks_ like a rope-hung swing but is completely stationary and
safe. The seat must appear connected to the top beam (no “floating” look). Only basic woodworking tools are available.

_Input image._


**Ground truth.** Bolt the seat to the frame using vertical wooden posts, then wrap thick hemp rope around the posts to hide the
wood and create the hanging illusion.


**Model response (condensed).**
**Step 1 (direct).**

- **Interpretation.** The model treats the prop as a bench-like structure supported by a visible horizontal stretcher bar, rather than
creating a concealed rigid support that still looks rope-hung.


- **Proposed design.** Build a rigid A-frame, add a horizontal stretcher across the legs, mount the seat on the stretcher, and add
decorative (non-load-bearing) ropes from top beam to seat to mimic a swing.


**Failure point.** **Constraint miss (visual illusion).** The proposed stretcher-bar support remains visually apparent and undermines
the requirement that the seat should look convincingly hung from the top beam. It does not use hidden vertical supports wrapped
in rope, which is the key trick in the ground-truth solution.


**Final answer.** Build a stationary bench supported by a horizontal bar, then add taut decorative ropes to imitate a swing. ✗


24


