Preprint.

## **Graph of Skills: Dependency-Aware Structural Retrieval** **for Massive Agent Skills**


**Dawei** **Liu** **[1]** _[†]_ **Zongxia** **Li** **[2]** _[†]_ **Hongyang** **Du** **[3]** **Xiyang** **Wu** **[2]** **Shihang** **Gui** **[3]**
**Yongbei** **Kuang** [4] **Lichao** **Sun** [5]

1University of Pennelvenia 2University of Maryland 3Brown University
4Carnegie Melon University 5Lehigh University
```
 liudawei@seas.upenn.edu zli12321@umd.edu lis221@lehigh.edu

```

[�](https://github.com/davidliuk/graph-of-skills) **Github:** `[https://github.com/davidliuk/graph-of-skills](https://github.com/davidliuk/graph-of-skills)`


**Abstract**


Skill usage has become a core component of modern agent systems and
can substantially improve agents’ ability to complete complex tasks. In
real-world settings, where agents must monitor and interact with numerous
personal applications, web browsers, and other environment interfaces, skill
libraries can scale to thousands of reusable skills. Scaling to larger skill sets
introduces two key challenges. First, loading the full skill set saturates the
context window, driving up token costs, hallucination, and latency. In this
paper, we present **Graph** **of** **Skills** **(GoS)**, an inference-time structural
retrieval layer for large skill libraries. GoS constructs an executable skill
graph offline from skill packages, then at inference time retrieves a bounded,
dependency-aware skill bundle through hybrid semantic–lexical seeding,
reverse-weighted Personalized PageRank, and context-budgeted hydration.
On SkillsBench and ALFWorld, GoS improves average reward by 43 _._ 6% over
the vanilla full skill-loading baseline while reducing input tokens by 37 _._ 8%,
and generalizes across three model families: Claude Sonnet, GPT-5.2 Codex,
and MiniMax. Additional ablation studies across skill libraries ranging from
200 to 2,000 skills further demonstrate that GoS consistently outperforms
both vanilla skills loading and simple vector retrieval in balancing reward,
token efficiency, and runtime.


**1** **Introduction**


Large Language Model (LLM) agents solve complex technical tasks by invoking external
tools, APIs, and reusable skills (Schick et al., 2023; Mialon et al., 2023). As these tools and
skills grow from dozens of tools to thousands or even tens of thousands of candidates (Patil
et al., 2023; Li et al., 2023; Xu et al., 2023; Qin et al., 2024), the core challenge shifts from
deciding _whether_ to use a skill to retrieving the most relevant set of skills that is sufficient
for a task. Shi et al. (2025) already shows that skill retrieval itself is now a major bottleneck
in realistic tool ecosystems.


Two common strategies are widely used for handling large skill libraries. **Vanilla**
**Skills** (Agent Skills, 2026) prepends the entire skill set to the context window. This can work
for small toolsets, but it scales poorly: token cost grows linearly with library size, and critical
domain constraints become easy for the model to overlook inside an overloaded context
(Liu et al., 2024a). An alternative is **vector-based** **retrieval** (Lewis et al., 2020; Wang
et al., 2023), which improves efficiency by retrieving semantically similar skills. However,
semantic proximity does not imply executable sufficiency. In many engineering tasks, the
top semantic match is a high-level solver, while the actual solution also requires a lower-level
parser, converter, setup utility, or domain-specific preprocessor that is semantically weak
but functionally necessary (Qin et al., 2024; Patel et al., 2025; Patil et al., 2023) (Figure 1).


_†_ Core Contribution.


1


Preprint.



























































Figure 1: Conceptual comparison between flat skill loading, vector retrieval, and Graph
of Skills (GoS). **Vanilla** **Skills** prepends the full skill library to the prompt, so relevant
constraints and prerequisite skills become buried in an overloaded context. **Vector** **Skills**
improves efficiency by returning semantically similar skills, but it can still miss a functionally
required prerequisite outside the retrieved set, creating the prerequisite gap. **Graph** **of**
**Skills** starts from hybrid semantic-lexical seeds and then performs structure-aware retrieval
to recover prerequisite skills and assemble a compact execution bundle.


We present **Graph** **of** **Skills** (GoS), an inference-time structural retrieval layer for large local
skill libraries to combat limitations of the previous two approaches. GoS constructs a directed
multi-relational graph over local skill packages, where nodes are executable skills and edges
encode prerequisite and workflow structure. At query time, GoS uses semantic and lexical
signals only to identify a small seed set, then applies reverse-weighted Personalized PageRank
(PPR) (Haveliwala, 2002; Yang et al., 2024) to recover additional skills that are structurally
important for execution. The result is a bounded skill bundle that is both relevant and closer
to dependency-complete than isolated top- _k_ retrieval. This problem setting is complementary
to repository-scale skill infrastructures such as SkillNet and AgentSkillOS (Liang et al., 2026;
Li et al., 2026a).


Those works focus on creating, organizing, evaluating, and orchestrating large skill ecosystems.
GoS targets a critical downstream question: if a large local skill library already exists,
how should an agent retrieve the smallest and most relevant executable subset that is
sufficient for the current task? Rather than exposing only keyword or vector search over
repository metadata, GoS parses each `skill` `specification` into executable fields such
as I/O schemas, tooling, script entrypoints, and stable source paths, constructs typed
dependency and workflow edges, and retrieves a bounded bundle through graph diffusion
plus reranking.


Our contributions are as follows: (1) We introduce GoS, an agentic skill usage pipeline
that combines offline graph construction with inference-time structural retrieval to improve
skill selection accuracy while reducing input token consumption. (2) We evaluate GoS on
the 1,000-skill SkillsBench setting and find that, compared to the full skill-loading baseline,
GoS improves average reward by 43.6% and reduces input tokens by 37.8% across two
benchmarks and three model families. Additional ablation studies confirm that this pattern
holds consistently across skill library sizes ranging from 200 to 2,000 skills.


**2** **Related** **Work**


**Tool** **Use,** **Tool** **Discovery,** **and** **Tool** **Retrieval** **for** **Agents.** Early research on toolaugmented language models focuses on relatively small, fixed toolsets, where the primary


2


Preprint.


challenge is deciding _when_ to invoke a tool and formatting the call correctly (Schick et al.,
2023; Mialon et al., 2023). As tool sets grow from dozens of tools to thousands (Patil
et al., 2023; Li et al., 2023; Xu et al., 2023; Qin et al., 2024) and context windows continue
to expand (Singh et al., 2026; Li et al., 2026c; Comanici et al., 2025), the problem shifts
toward _tool_ _discovery_ and _tool_ _retrieval_ . Systems and benchmarks such as Gorilla Patil
et al. (2023), API-Bank Li et al. (2023), ToolBench-style evaluations Xu et al. (2023), and
ToolLLM Qin et al. (2024) show that large tool universes require scalable retrieval over
API descriptions and tool documentation. ToolNet (Liu et al., 2024b) introduces graph
structure into large-scale tool access, with the objective to connect models to broad tool
ecosystems rather than recover dependency-complete local executable bundles. However, Shi
et al. (2025) shows that tool retrieval is itself a difficult modeling problem and that generic
dense retrievers are often poorly aligned with real tool-use needs (Shi et al., 2025).


**Skill** **Repositories,** **Ecosystems,** **and** **Benchmarks.** Recent systems increasingly treat
agent skills as reusable assets rather than ad hoc prompts (Agent Skills, 2026; Liang et al.,
2026; Li et al., 2026a). SkillNet (Liang et al., 2026) is a repository-scale skill library in this
space, supporting skill creation from heterogeneous sources, multi-dimensional evaluation,
ontology construction, and relational analysis over large skill collections. AgentSkillOS (Li
et al., 2026a) similarly advocates for an ecosystem-level approach, emphasizing that massive
skill libraries must be systematically categorized for efficient retrieval and dynamically
chained together to execute complex, multi-step tasks. SkillsBench (Li et al., 2026b) shows
that curated external skills can improve agent performance, while also exposing that simply
having many skills available does not guarantee reliable and safe use. Other systems and
registries such as SkillsMP, ClawHub, and LangSkills similarly support packaging, discovery,
and search over large skill collections (SkillsMP, 2026; OpenClaw, 2026; Li et al., 2025;
LabRAI, 2026). These skill repository platforms lower the cost of packaging, publishing,
browsing, and searching large skill collections, but their primary interface remains entry-level
search or distribution over individual skills or bundles.


**Graph-Based** **Retrieval** **and** **Relational** **Memory.** Graph-structured retrieval has
recently improved knowledge access in document, memory, and tool-use settings, but its role
differs substantially across these regimes. GraphRAG (Edge et al., 2024) uses graph structure
to support query-focused synthesis over document collections, HippoRAG (Jiménez Gutiérrez
et al., 2024) models long-term memory as an associative graph for improved retrieval, and
adjacent agent systems such as ControlLLM (Liu et al., 2023) and ToolNet (Liu et al., 2024b)
incorporate graph structure over tools rather than treating tools as a flat list. However, these
lines of work do not directly study retrieval over large local skill repositories. GraphRAG-style
systems target knowledge synthesis, memory access, or relational QA; tool-graph methods
focus primarily on graph-guided tool planning and navigation during reasoning. By contrast,
our setting requires an _upstream_ retrieval layer that selects a small executable bundle _before_
generation begins. To our knowledge, prior work has not focused on graph-based retrieval
for agent skills under this objective: recovering a dependency-complete executable bundle
under a tight context budget, rather than merely retrieving one relevant item.


**3** **Methodology**


GoS is an inference-time retrieval layer for large local skill libraries. It constructs a typed
graph offline from local skill packages and, at query time, returns a compact execution bundle
that is relevant to the task and more likely than flat retrieval to include the prerequisites
required for successful execution.


**3.1** **Problem** **Setup**


Let _C_ = _{d_ 1 _, . . ., dm}_ denote a local corpus of skill packages. Each package contains a
primary specification document together with optional scripts, references, and auxiliary
assets. GoS converts _C_ into a typed directed graph


_G_ = ( _V, E, w, ϕ_ ) _,_


3


Preprint.



















Figure 2: Overview of Graph of Skills (GoS). **Left:** offline indexing converts local skill
packages into normalized skill records and typed edges. Dependency edges are induced from
I/O compatibility, while workflow, semantic, and alternative relations are added through
sparse validation. **Center:** the typed directed skill graph is the retrieval substrate; edge
labels denote dependency, workflow, semantic, and alternative relations. **Right:** online
retrieval maps a task query to a compact query schema, forms merged seeds from semantic
and lexical retrieval, applies reverse-aware Personalized PageRank, and returns a budgeted
execution bundle after reranking and hydration.


where each node _v_ _∈_ _V_ is a normalized executable skill record, each edge _e ∈_ _E_ connects two
skills, _w_ ( _e_ ) _>_ 0 is an edge weight, and _ϕ_ ( _e_ ) _∈R_ assigns an edge type from the relation set


_R_ = _{_ dep _,_ wf _,_ sem _,_ alt _}._


Given a task query _q_ and a context budget _τ_, the retrieval problem is to return a bundle
_B_ ( _q_ ) _⊆_ _V_ that is simultaneously relevant, execution-complete when possible, and compact.
We view this as a budgeted selection problem,



I[ _u ∈_ _B ∧_ _v_ _∈_ _B_ ] s.t. cost( _B_ ) _≤_ _τ,_ (1)

( _u,v_ ) _∈E_ dep



max
_B⊆V_




- rel( _v, q_ ) + _β_ 

_v∈B_ ( _u,v_ ) _∈_







where the first term favors query relevance, the second rewards dependency-complete bundles,
and cost( _B_ ) measures the prompt budget consumed by the hydrated bundle. Equation (1)
is not solved exactly. Instead, GoS approximates this objective through three stages: hybrid
seed retrieval, reverse-aware graph diffusion, and budgeted reranking plus hydration.


**3.2** **Offline** **Graph** **Construction**


**Skill** **Normalization.** Each skill package is parsed into a normalized skill record containing a canonical name, capability summary, I/O fields, domain tags, tooling, entrypoints,
compatibility notes, and a stable local source path. This normalization step is primarily
deterministic: the system extracts executable fields whenever possible and uses a lightweight
LLM pass only to recover retrieval-critical semantic fields when package documentation is
incomplete. The goal is to convert each local skill into a retrieval unit that an agent can
directly consume at inference time.


**Typed** **Relation** **Induction.** GoS uses four edge types. _Dependency_ edges represent
executable prerequisites and form the primary structural relation in the graph. A dependency
edge _vi_ _→_ _vj_ is added when the outputs produced by _vi_ are compatible with inputs required
by _vj_, so that _vi_ can plausibly provide an artifact consumed by _vj_ . _Workflow_ edges capture
common multi-step pipelines, _semantic_ edges connect near-duplicate or topically adjacent
skills, and _alternative_ edges link interchangeable strategies for the same subproblem.


4


Preprint.


Rather than performing unconstrained all-pairs relation inference, GoS constructs nondependency edges through sparse validation. For each node, it first forms a small candidate
pool using lexical similarity, semantic neighbors, and I/O-based expansion. Relation validation is then applied only inside this pool. This keeps graph construction tractable while
ensuring that the resulting graph remains anchored in executable structure rather than
metadata proximity alone.


**3.3** **Online** **Structural** **Retrieval**


**Query** **Representation** **and** **Hybrid** **Seeding.** Dense retrieval (Karpukhin et al., 2020) is
often effective at finding the visible top-level skill but weak at recovering semantically subtle
prerequisites. Lexical retrieval in the probabilistic ranking tradition (Robertson et al., 2009)
is robust for concrete artifacts and filenames, but brittle under paraphrase. GoS therefore
combines the two signals at the seeding stage.


At retrieval time, the raw query is mapped to a lightweight retrieval schema containing the
task goal, salient operations, referenced artifacts, and normalized keywords. This schema
can be produced by an optional LLM rewrite, following the general intuition of rewrite-thenretrieve pipelines (Ma et al., 2023); when rewriting is unavailable or disabled, GoS falls back
to deterministic lexical normalization. GoS then computes a semantic seed score _s_ [sem] _i_ ( _q_ ) and
a lexical seed score _s_ [lex] _i_ [(] _[q]_ [)] [for] [each] [candidate] [skill] _[v][i]_ [,] [and] [merges] [them] [as]

_zi_ ( _q_ ) = _η s_ [sem] _i_ ( _q_ ) + (1 _−_ _η_ ) _s_ [lex] _i_ [(] _[q]_ [)] _[,]_ (2)


where _η_ _∈_ [0 _,_ 1] controls the semantic–lexical tradeoff. The initial seed distribution is obtained
by normalizing the merged scores over the candidate pool,


_zi_ ( _q_ )
**p** _i_ =              
_j_ _[z][j]_ [(] _[q]_ [)] _[.]_


**Reverse-Aware** **Typed** **Diffusion.** Let _Ar_ denote the weighted adjacency matrix for
relation type _r_ _∈R_ . To let retrieval move from a matched high-level skill toward likely
prerequisites, GoS uses both forward and reverse transitions. For each relation type, we
define a row-normalized forward operator _Tr_ _[→]_ and a row-normalized reverse operator _Tr_ _[←]_
obtained from _Ar_ and _A_ _[⊤]_ _r_ [,] [respectively.] [GoS] [then] [forms] [the] [unified] [transition] [operator]







_,_ (3)



_T_ = RowNorm



��



_λr_ ( _Tr_ _[→]_ + _γrTr_ _[←]_ [)]
_r∈R_



where _λr_ _≥_ 0 and [�] _r_ _[λ][r]_ [= 1] [weight] [relation] [types,] [and] _[γ][r]_ _[≥]_ [0] [controls] [how] [strongly] [reverse]

traversal is allowed for each type.


The core retrieval step is a reverse-aware Personalized PageRank-style diffusion over this
operator (Page et al., 1999; Jeh & Widom, 2003; Yang et al., 2024):


**s** [(] _[ℓ]_ [+1)] = _α_ **p** + (1 _−_ _α_ ) _T_ _[⊤]_ **s** [(] _[ℓ]_ [)] _,_ (4)


where _α_ _∈_ (0 _,_ 1) is the restart parameter. Relative to flat top- _k_ retrieval, relevance is
not assigned only to individually matched skills; it is propagated across a local executable
neighborhood. In particular, once a high-level solver is retrieved as a seed, upstream parser,
setup, or preprocessing skills can still accumulate score through reverse dependency paths
even when they are not themselves strong semantic matches to the original query.


**Budgeted** **Reranking** **and** **Hydration.** The diffusion score alone is insufficient, because
the final output must be compact and directly usable by an agent. GoS therefore reranks
candidate skills by combining graph score with field-level query evidence:


_ρi_ ( _q_ ) = **s** _[⋆]_ _i_ [+] _[ µ m][i]_ [(] _[q]_ [)] _[,]_ (5)

where **s** _[⋆]_ _i_ [is] [the] [converged] [diffusion] [score,] _[m][i]_ [(] _[q]_ [)] [aggregates] [direct] [matches] [between] [the] [query]
and skill fields such as name, capability summary, artifacts, and entrypoints, and _µ_ controls
how much local grounding is preserved after graph expansion.


5


Preprint.


Candidates are then hydrated in descending order of _ρi_ ( _q_ ) under both per-skill and global
context budgets. Here, _hydration_ denotes materializing a selected skill into an agentconsumable payload that includes a stable source path together with concise capability text
and the most relevant execution notes. The final output is therefore a bounded execution
bundle designed to maximize executable coverage within the prompt budget.


**4** **Experiments**


We evaluate whether graph-structured retrieval improves agent performance and efficiency
relative to flat full-library access and non-graph semantic retrieval.


**4.1** **Experimental** **Setup**


We evaluate GoS on two benchmarks using the full released task sets. **SkillsBench** (Li et al.,
2026b) contains a diverse set of real-world technical tasks across 11 domains, paired with
curated Skills: structured packages of procedural knowledge (instructions, code templates,
resources) that augment LLM agents at inference time. The task domains span complex
technical work such as macroeconomic detrending, power-grid feasibility analysis, 3D scan
analysis, financial modeling, and seismic phase picking. **ALFWorld** (Shridhar et al., 2020b)
is an interactive simulator that aligns text descriptions and commands with a physically
embodied robotic environment, built by combining TextWorld (Côté et al., 2018), an engine
for interactive text-based games and the ALFRED dataset (Shridhar et al., 2020a). Its
tasks involve multi-step household activities such as navigating rooms, finding objects, and
manipulating them. In the LLM agent literature, ALFWorld is widely used in its text-only
mode as a benchmark for sequential decision making, where an agent receives textual room
descriptions and must issue a chain of commands to accomplish a goal (Yao et al., 2023;
Shinn et al., 2023). We evaluate on the full 140-episode split.


**Baselines.** We compare GoS against two baselines. _Vanilla_ _Skills_ exposes the entire skill
library directly to the agent, maximizing recall but providing no retrieval-time compression.
On ALFWorld, this follows the official Agent Skills format and reference repository (Agent
Skills, 2026). _Vector_ _Skills_ retrieves a bounded set of skills using semantic similarity over the
same embedding model used by GoS, namely `openai/text-embedding-3-large` (OpenAI,
2024) (3072 dimensions). It isolates the effect of graph structure from the general benefit of
retrieval-time compression. _GoS_ uses the same base embedding model as _Vector_ _Skills_ but
replaces flat nearest-neighbor retrieval with structure-aware retrieval over the skill graph. In
the experiments reported here, we disable the optional query-rewrite module and use the
raw task instruction as the retrieval query. The critical comparison is therefore between flat
semantic retrieval and dependency-aware structural retrieval under the same backbone and
embedding setup.


**Models and Evaluation.** All experiments are conducted with Claude Sonnet 4.5 (Anthropic,
2025), MiniMax M2.7 (MiniMax, 2026), and GPT-5.2 Codex (OpenAI, 2025). Each model–
method setting is run twice, and we report the mean across runs. We report average reward
across tasks as the primary evaluation metric. For ALFWorld, rewards are binary, so average
reward is equivalent to success rate. We additionally report average total token usage and
agent-only runtime; runtime is measured from agent start to agent finish and excludes
environment setup.


**Evaluation** **Protocol.** We use the full benchmark task sets and apply the same retry policy
across the main and sensitivity experiments. If environment construction fails, we rebuild
and rerun the task up to two additional times; tasks that still fail after these retries are
excluded as unresolved infrastructure failures rather than counted as model failures. For
agent timeouts, we distinguish between substantive execution failures and startup failures:
if the agent has already been executing for a long time and then times out, we record
reward 0 and keep the run in the aggregate; if the timeout occurs before a meaningful run is
established, we rerun the trial. This protocol is applied to the full SkillsBench evaluation,
the full 140-episode ALFWorld evaluation, and the library-size sensitivity study.


6


Preprint.


Table 1: **R** denotes average reward (%), **T** denotes tokens, and **S** denotes runtime ( **s** ) ( _↑_
indicates larger values are better, and _↓_ denotes smaller values are better). Results are
means over two runs per setting. For ALFWorld, average reward equals success rate. The
top-performing results are highlighted in **bold**, and the second-best are underlined.


SkillsBench ALFWorld


Model Method R _↑_ T _↓_ S _↓_ R _↑_ T _↓_ S _↓_


Vanilla Skills 25.0 967,791 465.8 89.3 1,524,401 53.2
Claude Sonnet 4.5 Vector Skills 19.3 894,640 **357.3** 93.6 28,407 **37.8**
+ GoS **31.0** **860,315** 364.9 **97.9** **27,215** 49.2


Vanilla Skills 17.2 942,113 580.7 47.1 2,184,823 88.6
MiniMax M2.7 Vector Skills 10.4 **852,881** 552.9 50.7 66,109 73.4
+ GoS **18.7** 867,452 **502.5** **54.3** **65,227** **68.8**


Vanilla Skills 27.4 3,187,749 **686.8** 89.3 1,435,614 83.3
GPT-5.2 Codex Vector Skills 21.5 **1,243,648** 773.0 92.9 **34,436** **57.0**
+ GoS **34.4** 1,379,773 715.6 **93.6** 46,462 64.7


**4.2** **Main** **Results**


We present the main results in Table 1. Across all six model–benchmark blocks, GoS attains
the highest average reward. Relative to _Vanilla_ _Skills_, it reduces average token usage in all
six blocks and reduces agent runtime in five of the six. Relative to _Vector_ _Skills_, it improves
reward in every block while keeping the token budget in the same compressed regime.


**Naive** **semantic** **retrieval** **struggles** **on** **long-horizon** **tasks.** Many tasks in SkillsBench
are long-horizon and require combining relevant skills with prerequisite utilities, such as
environment setup, data preprocessing, or output formatting. These skills may not be
lexically salient in the task description. Vector Skills, which retrieves based solely on
embedding similarity to the query, often misses these indirect but essential dependencies,
leading to incomplete skill sets and lower task completion rates. This pattern is most visible
on SkillsBench. Under Claude Sonnet 4.5, _Vector_ _Skills_ drops from 25.0 to 19.3 average
reward relative to _Vanilla_ _Skills_ ; under MiniMax M2.7, it drops from 17.2 to 10.4; and under
GPT-5.2 Codex, it drops from 27.4 to 21.5. In contrast, GoS improves over both baselines in
all three SkillsBench blocks while still using substantially fewer tokens than flat prompting.
These results are consistent with the hypothesis that long-horizon tasks are sensitive not
only to topical relevance, but also to whether the retrieved bundle contains the prerequisite
helpers needed to complete the full execution path.


**GoS** **achieves** **the** **strongest** **overall** **tradeoff** **on** **ALFWorld.** The ALFWorld results
show that the same advantage transfers to a sequential embodied environment. Under Claude
Sonnet 4.5, GoS reaches 97.9% average success, compared with 93.6% for _Vector_ _Skills_ and
89.3% for _Vanilla_ _Skills_, while reducing average total tokens from 1,524,401 to 27,215 relative
to flat prompting. Under MiniMax M2.7, GoS again gives the strongest overall tradeoff,
improving reward from 47.1% under _Vanilla_ _Skills_ and 50.7% under _Vector_ _Skills_ to 54.3%,
while also achieving the lowest token usage and runtime in that block. Under GPT-5.2
Codex, GoS and _Vector_ _Skills_ are close on reward (93.6% vs. 92.9%), but GoS still remains
clearly more efficient than _Vanilla_ _Skills_ . Taken together, these results suggest that the
benefit of structure-aware retrieval is not limited to technical code-execution tasks.


**GoS** **offers** **the** **best** **efficiency–performance** **tradeoff.** _Vanilla_ _Skills_ preserves maximal recall, but its cost grows rapidly with library size and leaves the agent to search an
unstructured skill set at inference time. _Vector_ _Skills_ reduces token cost, but its retrieved
set is often incomplete, because semantically nearby skills are not always jointly sufficient.
GoS improves reward over _Vector_ _Skills_ by 10.97 points on SkillsBench and 2.87 points on
ALFWorld while remaining far more efficient than _Vanilla_ _Skills_ (Table 1). The results are
averaged over two runs per setting. We interpret them as a consistent empirical pattern
rather than a formal significance claim.


7


Preprint.


Figure 3: Sensitivity to library size on full SkillsBench under GPT-5.2 Codex. Left: compact
summary table for Vanilla Skills, Vector Skills, and GoS. Right: reward and input-token
trends as the skill repository grows from 200 to 2,000 skills. GoS preserves the strongest
reward once the library becomes moderately large, while both retrieval-based methods
substantially weaken the growth of prompt cost relative to flat exposure.



N Method R _↑_ T _↓_ S _↓_


200 Vanilla Skills **32.5** 1.85 **701.6**
Vector Skills 21.2 **1.06** 833.8
+ GoS 32.1 1.36 731.2

500 Vanilla Skills 26.0 1.93 **756.8**
Vector Skills 20.7 **1.10** 849.5
+ GoS **31.4** **1.16** 890.3

1000 Vanilla Skills 27.4 3.19 **686.8**
Vector Skills 21.5 **1.24** 773.0
+ GoS **34.4** 1.38 715.6

2000 Vanilla Skills 26.7 5.84 **733.5**
Vector Skills 23.8 **1.11** 799.8
+ GoS **31.3** 1.14 788.0


**N** : library size, **R** : reward, **T** : input tokens (M), **S** :
runtime (s).


**4.3** **Qualitative** **Analysis**



35


30


25


20


6


4


2


0
200 500 1000 2000


Skill library size



We inspect trajectory-level evidence to study how retrieval quality changes the downstream
execution path, not just the final score. Appendix F provides a broader case set; here we
focus on one representative example that isolates the main mechanism behind GoS.


**Pedestrian** **Traffic** **Counting.** `pedestrian-traffic-counting` requires a short but
complete visual pipeline: extracting frames, counting pedestrians reliably, and formatting
the output in the expected structure. In this case, GoS retrieved a compact bundle centered on `gemini-count-in-video`, `video-frame-extraction`, and `openai-vision`, and
achieved the highest score (0 _._ 417). _Vanilla_ _Skills_ eventually opened related helpers, including
`gemini-count-in-video`, `video-frame-extraction`, and `object_counter`, but reached
only 0 _._ 267, suggesting that broad library access can recover relevant tools while still leaving
the agent with a noisier search problem. _Vector_ _Skills_ scored only 0 _._ 041: it retrieved some
relevant context, but not a bundle that the agent could convert into a workable end-to-end
plan. The qualitative lesson is that GoS does not help merely by retrieving topically similar
skills. It helps by exposing a bundle that is already close to the executable decomposition
of the task, so the agent can commit earlier to a verifier-aligned plan rather than spending
budget on additional search and assembly.


**5** **Ablation** **Study**


We conduct an additional ablation study to evaluate the impact of the skill library size on
GoS, _Vanilla_ _Skills_, and _Vector_ _Skills_, alongside the effects of the lexical merge and reranker
components on GoS performance.


**5.1** **Sensitivity** **to** **Skill** **Library** **Size**


We run an additional full-SkillsBench study with GPT-5.2 Codex while varying the library
size from 200 to 500, 1,000, and 2,000 skills. We report average reward, average input
tokens, and agent-only runtime under the same retry and exclusion rules used in the main
experiments in Table 2.


**Prompt** **cost** **grows** **rapidly** **for** **all** **skill** **exposure.** The strongest trend is on input
tokens. As the library grows from 500 to 2,000 skills, _Vanilla_ _Skills_ rises from 1.93M to


8


Preprint.


5.84M average input tokens, roughly a 3 _×_ increase. Over the same range, _Vector_ _Skills_ stays
near 1.10M–1.24M tokens and GoS stays near 1.14M–1.38M tokens. This result shows that
simple retrieval substantially weakens the coupling between repository size and prompt size,
while GoS does so without giving up reward.


**GoS** **maintains** **a** **reward** **advantage** **at** **all** **tested** **scales.** At 200 skills, _Vanilla_ _Skills_
is still slightly ahead of GoS (32.5 vs. 32.1). Once the library becomes moderately large,
GoS outperforms both baselines at every tested scale: 31.4 vs. 26.0 / 20.7 at 500 skills,
34.4 vs. 27.4 / 21.5 at 1,000 skills, and 31.3 vs. 26.7 / 23.8 at 2,000 skills (GoS / Vanilla
Skills / Vector Skills). The margin is largest at 1,000 skills and remains substantial at 2,000,
indicating that increasing library size does not weaken the benefit of dependency-aware
retrieval.


**The** **extra** **retrieval** **step** **adds** **modest** **runtime** **for** **GPT-5.2** **Codex,** **but** **does**
**not** **change** **the** **main** **scaling** **conclusion.** Both retrieval-based methods are slower
than _Vanilla_ _Skills_ in agent-only runtime for GPT at most scales, reflecting the overhead
of searching before execution. However, this reduced runtime is unique to GPT-5.2 Codex,
likely due to caching mechanisms for fixed skill libraries within the black-box model, where
Claude and MiniMax have longer runtime when using _Vanilla_ _Skills_ than GoS and _Vector_
_Skills_ (Table 1). In contrast, the Claude model lacks this optimization, making the _Vanilla_
_Skills_ approach significantly slower than retrieval methods. Furthermore, the results suggest
that the primary system bottleneck is not graph traversal or vector search, but rather the
overhead of exposing an increasingly large, flat library directly to the model.


**5.2** **Component** **Analysis** **of** **the** **GoS** **Retrieval** **Pipeline**



We next evaluate the contribution of two key
retrieval components in the GoS pipeline: Method R _↑_ T _↓_ S _↓_
graph propagation and lexical reranking. Full GoS **34.4** 1.38 715.6
These ablations were run under the main w/o graph propagation 29.3 0.89 766.2
SkillsBench configuration — GPT-5.2 Codex w/o lexical + rerank 26.7 1.01 747.7
across skill libraries of increasing size (200,
500, 1,000, and 2,000 skills). In the first Table 2: Component ablation on full Skillsablation, we remove graph propagation, dis- Bench with GPT-5.2 Codex and the 1,000-skill
abling the system’s ability to expand beyond library. **R** : average reward (%), **T** : average
seed skills to structurally related prerequi- total tokens (M), **S** : agent-only runtime (s).
sites. In the second, we remove lexical retrieval and reranking, forcing the system to rely solely on the semantic retriever before graph
expansion.


**Graph** **propagation** **and** **lexical** **reranking** **are** **important** **components** **for** **GoS’**
**success.** Removing graph propagation reduces average token usage from 1.38M to 0.89M,
but it also lowers average reward from 34.4 to 29.3 ( _↓_ 5 _._ 1). Removing lexical retrieval and
reranking lowers average token usage from 1.38M to 1.01M. It lowers average reward from
34.4 to 26.7 ( _↓_ 7 _._ 7). The larger degradation in the second ablation suggests that better
seed quality is especially important on SkillsBench: if the initial retrieved skills are weak,
graph expansion has less useful structure from which to recover missing prerequisites. These
results show that hybrid semantic–lexical retrieval improves entry-point quality, and graph
propagation then converts those stronger seeds into a more execution-complete bundle.


**6** **Conclusion**


Skill retrieval is a critical bottleneck for agents operating over massive skill libraries. Unlike
approaches that retrieve only semantically relevant skills, GoS recovers a small, jointly
sufficient set of skills by capturing not just the target skill but also the parsers, preprocessors,
and dependencies needed for successful execution. GoS is complementary to, but distinct
from, broader skill management systems such as SkillNet and AgentSkillOS (Liang et al.,
2026; Li et al., 2026a). Our results demonstrate that GoS consistently outperforms both
vanilla skills loading and simple vector retrieval, improving execution reward while reducing


9



Method R _↑_ T _↓_ S _↓_



Full GoS **34.4** 1.38 715.6
w/o graph propagation 29.3 0.89 766.2
w/o lexical + rerank 26.7 1.01 747.7



Table 2: Component ablation on full SkillsBench with GPT-5.2 Codex and the 1,000-skill
library. **R** : average reward (%), **T** : average
total tokens (M), **S** : agent-only runtime (s).


Preprint.


token consumption. This advantage holds across two benchmarks, three model families, and
skill libraries of varying sizes.


**Limitations and Future Work.** GoS still depends on the quality of its offline graph. Poorly
documented skills, ambiguous I/O schemas, or missing execution metadata can degrade edge
quality and downstream retrieval. In addition, the current graph system is mostly static:
it does not yet refine graph structure from repeated execution traces, verifier outcomes, or
user feedback. Future work can focus on including online edge-weight adaptation, graph
updates from successful trajectories, stronger reranking over candidate bundles, and broader
evaluation on multimodal and interactive agent settings.


**Reproducibility** **Statement**


The paper and appendix specify the core components needed to reproduce the proposed
method: parser-first skill normalization, optional LLM-based semantic field completion,
typed edge construction, hybrid semantic–lexical seeding, reverse-aware graph diffusion,
reranking, and budgeted hydration. We also document the evaluation protocol, including
benchmark settings, run structure, reward definitions, token accounting, agent-only runtime
measurement, and the treatment of unresolved infrastructure failures.


Because the submission package is size-constrained, we do not include the full codebase and
experiment assets with the anonymous submission. We plan to release the implementation,
experiment configurations, prompt templates, agent-environment instructions, and resultprocessing scripts in the camera-ready release. The public release will also include the
benchmark configuration files and task-generation assets needed to reproduce the SkillsBench
and ALFWorld experiments reported in the paper.


Exact numerical replication may still vary because the experiments depend on black-box LLM
APIs and external inference providers whose behavior can change over time. To reduce this
variance, we use fixed prompts and configurations, repeated runs under the same protocol,
and a clear separation between infrastructure failures and substantive model failures. We
therefore expect the main comparative trends and qualitative conclusions to be reproducible
even when exact per-run metrics vary modestly.


**References**


Agent Skills. Agent skills, 2026. URL `[https://github.com/agentskills/agentskills](https://github.com/agentskills/agentskills)` .
Specification and documentation repository, accessed 2026-04-01.


Anthropic. Claude sonnet 4.5, 2025. URL `[https://www.anthropic.com/news/](https://www.anthropic.com/news/claude-sonnet-4-5)`
`[claude-sonnet-4-5](https://www.anthropic.com/news/claude-sonnet-4-5)` . Official release page, accessed 2026-04-01.


Gheorghe Comanici, Eric Bieber, Mike Schaekermann, Ice Pasupat, Noveen Sachdeva, Inderjit
Dhillon, Marcel Blistein, Ori Ram, Dan Zhang, Evan Rosen, et al. Gemini 2.5: Pushing
the frontier with advanced reasoning, multimodality, long context, and next generation
agentic capabilities. _arXiv_ _preprint_ _arXiv:2507.06261_, 2025.


Marc-Alexandre Côté, Akos Kádár, Xingdi Yuan, Ben Kybartas, Tavian Barnes, Emery Fine,
James Moore, Matthew Hausknecht, Layla El Asri, Mahmoud Adada, et al. Textworld: A
learning environment for text-based games. In _Workshop_ _on_ _Computer_ _Games_, pp. 41–75.
Springer, 2018.


Darren Edge, Ha Trinh, Newman Cheng, Joshua Bradley, Alex Chao, Apurva Mody, Steven
Truitt, and Jonathan Larson. From local to global: A graph rag approach to query-focused
summarization. _arXiv_ _preprint_ _arXiv:2404.16130_, 2024.


Taher H. Haveliwala. Topic-sensitive pagerank. In _Proceedings_ _of_ _the_ _11th_ _International_
_Conference_ _on_ _World_ _Wide_ _Web_, WWW ’02, pp. 517–526, New York, NY, USA, 2002.
Association for Computing Machinery. ISBN 1581134495. doi: 10.1145/511446.511513.
URL `[https://doi.org/10.1145/511446.511513](https://doi.org/10.1145/511446.511513)` .


10


Preprint.


Glen Jeh and Jennifer Widom. Scaling personalized web search. In _Proceedings_ _of_ _the_ _12th_
_international_ _conference_ _on_ _World_ _Wide_ _Web_, pp. 271–279, 2003.


Bernal Jiménez Gutiérrez, Yiheng Shu, Yu Gu, Michihiro Yasunaga, and Yu Su. Hipporag:
Neurobiologically inspired long-term memory for large language models. _arXiv_ _preprint_
_arXiv:2405.14831_, 2024.


Vladimir Karpukhin, Barlas Oguz, Sewon Min, Patrick Lewis, Ledell Wu, Sergey Edunov,
Danqi Chen, and Wen-tau Yih. Dense passage retrieval for open-domain question answering. In _Proceedings_ _of_ _the_ _2020_ _Conference_ _on_ _Empirical_ _Methods_ _in_ _Natural_ _Language_
_Processing_ _(EMNLP)_, pp. 6769–6781, Online, 2020. Association for Computational Linguistics. doi: 10.18653/v1/2020.emnlp-main.550. URL `[https://aclanthology.org/2020.](https://aclanthology.org/2020.emnlp-main.550/)`
`[emnlp-main.550/](https://aclanthology.org/2020.emnlp-main.550/)` .


LabRAI. Langskills, 2026. URL `[https://github.com/LabRAI/LangSkills](https://github.com/LabRAI/LangSkills)` . GitHub repository, accessed 2026-04-01.


Patrick Lewis, Ethan Perez, Aleksandra Piktus, Fabio Petroni, Vladimir Karpukhin, Naman
Goyal, Heinrich Küttler, Mike Lewis, Wen-tau Yih, Tim Rocktäschel, et al. Retrievalaugmented generation for knowledge-intensive nlp tasks. In _Advances in Neural Information_
_Processing_ _Systems_, volume 33, pp. 9459–9474, 2020.


Hao Li, Chunjiang Mu, Jianhao Chen, Siyue Ren, Zhiyao Cui, Yiqun Zhang, Lei Bai, and
Shuyue Hu. Organizing, orchestrating, and benchmarking agent skills at ecosystem scale.
_arXiv_ _preprint_ _arXiv:2603.02176_, 2026a.


Minghao Li, Yingxiu Zhao, Bowen Yu, Feifan Song, Hangyu Li, Haiyang Yu, Zhoujun Li,
Fei Huang, and Yongbin Li. Api-bank: A comprehensive benchmark for tool-augmented
llms. _arXiv_ _preprint_ _arXiv:2304.08244_, 2023.


Xiangyi Li, Wenbo Chen, Yimin Liu, Shenghan Zheng, Xiaokun Chen, Yifeng He, Yubo
Li, Bingran You, Haotian Shen, Jiankai Sun, Shuyi Wang, Qunhong Zeng, Di Wang,
Xuandong Zhao, Yuanli Wang, Roey Ben Chaim, Zonglin Di, Yipeng Gao, Junwei He,
Yizhuo He, Liqiang Jing, Luyang Kong, Xin Lan, Jiachen Li, Songlin Li, Yijiang Li,
Yueqian Lin, Xinyi Liu, Xuanqing Liu, Haoran Lyu, Ze Ma, Bowei Wang, Runhui Wang,
Tianyu Wang, Wengao Ye, Yue Zhang, Hanwen Xing, Yiqi Xue, Steven Dillmann, and
Han-chung Lee. Skillsbench: Benchmarking how well agent skills work across diverse
tasks. _arXiv_ _preprint_ _arXiv:2602.12670_, 2026b. doi: 10.48550/arXiv.2602.12670. URL
`[https://arxiv.org/abs/2602.12670](https://arxiv.org/abs/2602.12670)` .


Zongxia Li, Wenhao Yu, Chengsong Huang, Rui Liu, Zhenwen Liang, Fuxiao Liu, Jingxi Che,
Dian Yu, Jordan Boyd-Graber, Haitao Mi, et al. Self-rewarding vision-language model via
reasoning decomposition. _arXiv_ _preprint_ _arXiv:2508.19652_, 2025.


Zongxia Li, Hongyang Du, Chengsong Huang, Xiyang Wu, Lantao Yu, Yicheng He, Jing Xie,
Xiaomin Wu, Zhichao Liu, Jiarui Zhang, et al. Mm-zero: Self-evolving multi-model vision
language models from zero data. _arXiv_ _preprint_ _arXiv:2603.09206_, 2026c.


Yuan Liang, Ruobin Zhong, Haoming Xu, Chen Jiang, Yi Zhong, Runnan Fang, Jia-Chen
Gu, Shumin Deng, Yunzhi Yao, Mengru Wang, Shuofei Qiao, Xin Xu, Tongtong Wu, Kun
Wang, Yang Liu, Zhen Bi, Jungang Lou, Yuchen Eleanor Jiang, Hangcheng Zhu, Gang Yu,
Haiwen Hong, Longtao Huang, Hui Xue, Chenxi Wang, Yijun Wang, Zifei Shan, Xi Chen,
Zhaopeng Tu, Feiyu Xiong, Xin Xie, Peng Zhang, Zhengke Gui, Lei Liang, Jun Zhou,
Chiyu Wu, Jin Shang, Yu Gong, Junyu Lin, Changliang Xu, Hongjie Deng, Wen Zhang,
Keyan Ding, Qiang Zhang, Fei Huang, Ningyu Zhang, Jeff Z. Pan, Guilin Qi, Haofen
Wang, and Huajun Chen. Skillnet: Create, evaluate, and connect ai skills. _arXiv_ _preprint_
_arXiv:2603.04448_, 2026.


Nelson F. Liu, Kevin Lin, John Hewitt, Ashwin Paranjape, Michele Bevilacqua, Fabio
Petroni, and Percy Liang. Lost in the middle: How language models use long contexts.
_Transactions_ _of_ _the_ _Association_ _for_ _Computational_ _Linguistics_, 12:157–173, 2024a. doi:
10.1162/tacl_a_00638. URL `[https://aclanthology.org/2024.tacl-1.9/](https://aclanthology.org/2024.tacl-1.9/)` .


11


Preprint.


Xukun Liu, Zhiyuan Peng, Xiaoyuan Yi, Xing Xie, Lirong Xiang, Yuchen Liu, and Dongkuan
Xu. Toolnet: Connecting large language models with massive tools via tool graph. _arXiv_
_preprint_ _arXiv:2403.00839_, 2024b.


Zhaoyang Liu, Zeqiang Lai, Zhangwei Gao, Erfei Cui, Ziheng Li, Xizhou Zhu, Lewei Lu,
Qifeng Chen, Yu Qiao, Jifeng Dai, and Wenhai Wang. Controlllm: Augment language
models with tools by searching on graphs. _arXiv_ _preprint_ _arXiv:2310.17796_, 2023.


Xinbei Ma, Yeyun Gong, Pengcheng He, Hai Zhao, and Nan Duan. Query rewriting in
retrieval-augmented large language models. In _Proceedings_ _of_ _the_ _2023_ _Conference_ _on_
_Empirical_ _Methods_ _in_ _Natural_ _Language_ _Processing_, pp. 5303–5315, Singapore, 2023.
Association for Computational Linguistics. doi: 10.18653/v1/2023.emnlp-main.322. URL
`[https://aclanthology.org/2023.emnlp-main.322/](https://aclanthology.org/2023.emnlp-main.322/)` .


Grégoire Mialon, Roberto Dessì, Maria Lomeli, Christoforos Nalmpantis, Ram Pasunuru,
Roberta Raileanu, Baptiste Rozière, Timo Schick, Jane Dwivedi-Yu, Asli Celikyilmaz,
et al. Augmented language models: a survey. _Transactions_ _on_ _Machine_ _Learning_ _Research_,
2023.


MiniMax. Minimax m2.7, 2026. URL `[https://www.minimax.io/news/minimax-m27-en](https://www.minimax.io/news/minimax-m27-en)` .
Official release page, accessed 2026-04-01.


OpenAI. text-embedding-3-large, 2024. URL `[https://developers.openai.com/api/docs/](https://developers.openai.com/api/docs/models/text-embedding-3-large)`
`[models/text-embedding-3-large](https://developers.openai.com/api/docs/models/text-embedding-3-large)` . Official model documentation, accessed 2026-04-01.


OpenAI. Gpt-5.2-codex, 2025. URL `[https://developers.openai.com/api/docs/models/](https://developers.openai.com/api/docs/models/gpt-5.2-codex)`
`[gpt-5.2-codex](https://developers.openai.com/api/docs/models/gpt-5.2-codex)` . Official model documentation, accessed 2026-04-01.


OpenClaw. Clawhub registry, 2026. URL `[https://openclawdoc.com/docs/skills/](https://openclawdoc.com/docs/skills/clawhub/)`
`[clawhub/](https://openclawdoc.com/docs/skills/clawhub/)` . Documentation page, accessed 2026-04-01.


Lawrence Page, Sergey Brin, Rajeev Motwani, and Terry Winograd. The pagerank citation
ranking: Bringing order to the web. Technical report, Stanford InfoLab, 1999.


Bhrij Patel, Davide Belli, Amir Jalalirad, Maximilian Arnold, Aleksandr Ermovol, and Bence
Major. Dynamic tool dependency retrieval for efficient function calling. _arXiv_ _preprint_
_arXiv:2512.17052_, 2025.


Shishir G. Patil, Tianjun Zhang, Xin Wang, and Joseph E. Gonzalez. Gorilla: Large language
model connected with massive apis. _arXiv_ _preprint_ _arXiv:2305.15334_, 2023.


Yujia Qin, Shihao Liang, Yining Ye, Kunlun Zhu, Lan Yan, Yaxi Lu, Yankai Lin, Xin
Cong, Xiangru Tang, Bill Qian, Sihan Zhao, Lauren Hong, Runchu Tian, Ruobing Xie, Jie
Zhou, Mark Gerstein, Dahai Li, Zhiyuan Liu, and Maosong Sun. Toolllm: Facilitating
large language models to master 16000+ real-world apis. In _International_ _Conference_ _on_
_Learning_ _Representations_, 2024.


Stephen Robertson, Hugo Zaragoza, et al. The probabilistic relevance framework: Bm25
and beyond. _Foundations_ _and_ _Trends®_ _in_ _Information_ _Retrieval_, 3(4):333–389, 2009.


Timo Schick, Jane Dwivedi-Yu, Roberto Dessì, Roberta Raileanu, Maria Lomeli, Luke
Zettlemoyer, Nicola Cancedda, and Thomas Scialom. Toolformer: Language models can
teach themselves to use tools. _Advances_ _in_ _Neural_ _Information_ _Processing_ _Systems_, 36,
2023.


Zhengliang Shi, Yuhan Wang, Lingyong Yan, Pengjie Ren, Shuaiqiang Wang, Dawei Yin,
and Zhaochun Ren. Retrieval models aren’t tool-savvy: Benchmarking tool retrieval for
large language models. _arXiv_ _preprint_ _arXiv:2503.01763_, 2025.


Noah Shinn, Federico Cassano, Edward Berman, Ashwin Gopinath, Karthik Narasimhan,
and Shunyu Yao. Reflexion: Language agents with verbal reinforcement learning. _arXiv_
_preprint_ _arXiv:2303.11366_, 2023.


12


Preprint.


Mohit Shridhar, Jesse Thomason, Daniel Gordon, Yonatan Bisk, Winson Han, Roozbeh
Mottaghi, Luke Zettlemoyer, and Dieter Fox. Alfred: A benchmark for interpreting
grounded instructions for everyday tasks. In _Proceedings_ _of_ _the_ _IEEE/CVF_ _conference_ _on_
_computer_ _vision_ _and_ _pattern_ _recognition_, pp. 10740–10749, 2020a.


Mohit Shridhar, Xingdi Yuan, Marc-Alexandre Côté, Yonatan Bisk, Adam Trischler, and
Matthew Hausknecht. Alfworld: Aligning text and embodied environments for interactive
learning. _arXiv_ _preprint_ _arXiv:2010.03768_, 2020b.


Aaditya Singh, Adam Fry, Adam Perelman, Adam Tart, Adi Ganesh, Ahmed El-Kishky,
Aidan McLaughlin, Aiden Low, AJ Ostrow, Akhila Ananthram, et al. Openai gpt-5 system
card. _arXiv_ _preprint_ _arXiv:2601.03267_, 2026.


SkillsMP. Skillsmp, 2026. URL `[https://skillsmp.com/](https://skillsmp.com/)` . Agent Skills Marketplace, accessed
2026-04-01.


Guanzhi Wang, Yuqi Xie, Yunfan Jiang, Ajay Mandlekar, Chaowei Xiao, Yuke Zhu, Linxi
Fan, and Anima Anandkumar. Voyager: An open-ended embodied agent with large
language models. _arXiv_ _preprint_ _arXiv:2305.16291_, 2023.


Qiantong Xu, Fenglu Hong, Bo Li, Changran Hu, Zhengyu Chen, and Jian Zhang. On
the tool manipulation capability of open-source large language models. _arXiv_ _preprint_
_arXiv:2305.16504_, 2023.


Mingji Yang, Hanzhi Wang, Zhewei Wei, Sibo Wang, and Ji-Rong Wen. Efficient algorithms
for personalized pagerank computation: A survey. _IEEE_ _Transactions_ _on_ _Knowledge_ _and_
_Data_ _Engineering_, 36(9):4582–4602, 2024. doi: 10.1109/TKDE.2024.3376000.


Shunyu Yao, Jeffrey Zhao, Dian Yu, Nan Du, Izhak Shafran, Karthik Narasimhan, and
Yuan Cao. React: Synergizing reasoning and acting in language models. In _International_
_Conference_ _on_ _Learning_ _Representations_, 2023.


13


Preprint.


**A** **Appendix** **Overview**


To make the supplementary material easier to navigate, we briefly summarize the organization
of the appendix before presenting the detailed evidence. The appendix is designed to
complement the main paper along four axes: implementation fidelity, prompt/interface
design, retrieval mechanics, and trajectory-grounded empirical analysis.


Table 3: Appendix roadmap. The table summarizes the role of each supplementary section
and how it complements the main paper.


**B** **Implementation** **Details**


This appendix summarizes the implementation decisions behind GoS and clarifies how the
abstract pipeline in the main text is instantiated in code. The purpose is not to enumerate
every engineering detail, but to expose the concrete design choices that determine graph
quality, retrieval behavior, and the final agent-facing bundle.


Table 4: GoS implementation summary. The table highlights the main design choices that
determine graph construction, retrieval, and agent-facing hydration.





14


Preprint.


Table 5: Normalized node fields used at retrieval time. The table lists the fields retained in
each skill node and their retrieval role in GoS.











Table 6: Relation types and reverse weights in reverse-aware graph diffusion. The table
shows how each edge type contributes to backward structural propagation during retrieval.

















15


Preprint.


**Implementation** **Substrate.** GoS is implemented on top of a graph-backed retrieval
substrate for workspace management, vector indexing, and graph storage, while replacing
document-centric assumptions with skill-specific parsing, relation induction, and agentoriented hydration. Concretely, the system maintains an HNSW vector index over skill
representations together with a typed directed graph whose vertices are normalized skills and
whose edges carry relation labels, directional semantics, and scalar weights. This yields a
retrieval substrate in which semantic proximity and structural connectivity can be combined
inside a single inference-time pipeline rather than treated as disjoint retrieval regimes.


**Parser-First** **Skill** **Normalization.** Each local skill package is first parsed deterministically from its primary `SKILL.md` file and nearby package structure. The parser extracts the
canonical name and description from YAML frontmatter, collects explicit input and output
fields, recovers domain tags, tooling, example tasks, compatibility notes, and allowed tools
from both frontmatter and markdown sections, and resolves script entrypoints by scanning
the local `scripts/` directory when present. It also materializes a stable local source path
and a rendered snippet used later for retrieval and hydration. This parser-first design keeps
node construction anchored in executable package structure rather than relying entirely on
free-form semantic extraction.


**LLM-Assisted** **Semantic** **Completion.** When package documentation is incomplete,
GoS optionally performs a lightweight LLM pass over the full markdown body to recover
retrieval-critical semantic fields, including capability summaries, inputs, outputs, domain
tags, tooling, and example tasks. Importantly, this stage is constrained to normalize a single
skill node and is not used to emit graph relations directly. In other words, the LLM here
serves as a high-precision semantic completion module for node attributes rather than as an
unconstrained graph-construction oracle. The inferred fields are then merged back with the
deterministic parse, with the implementation favoring completed semantic fields only when
they improve the retrieval representation.


**Typed** **Node** **Representation.** After normalization, each skill is serialized into a node
record that stores both structured lists and compact textual views. Besides canonical
descriptive fields, the node retains raw skill content, rendered snippets, script entrypoints,
and a stable `Source:` path. This dual representation is operationally important: the graph
and vector index operate over normalized fields, whereas the final agent-facing bundle requires
concise but directly usable payloads that can be opened inside the execution environment
without path reconstruction.


**Directed** **Typed** **Relation** **Induction.** The GoS graph is a typed directed graph rather
than an undirected similarity graph. Dependency edges are induced deterministically by
matching producer outputs against consumer inputs in both directions for each candidate
pair. An edge _u →_ _v_ therefore has explicit executable semantics: _u_ can plausibly provide an
artifact consumed by _v_ . Because I/O compatibility is asymmetric in general, this dependency
structure cannot be reduced to undirected similarity without losing the notion of prerequisite
direction.


Non-dependency relations, namely _workflow_, _semantic_, and _alternative_, are added through
sparse LLM validation rather than dense all-pairs inference. For each node, GoS first
forms a bounded candidate pool by combining lexical overlap, semantic neighbors from the
vector index, and I/O-based candidate expansion. The LLM is then asked only to validate
high-confidence relations inside this restricted pool. This two-stage design keeps graph
construction tractable and biases the resulting graph toward precision rather than density.


**Hybrid** **Seeding** **at** **Query** **Time.** At retrieval time, GoS does not rely on vector search
alone. The system first optionally rewrites the raw task request into a compact query schema
containing the goal, operations, artifacts, constraints, and high-value keywords. Semantic
seeding is then obtained from nearest-neighbor search in embedding space, while lexical
seeding is computed from token overlap over normalized node fields such as name, capability,
I/O descriptors, tooling, example tasks, entrypoints, and snippets. These candidate pools
are merged and reranked before graph diffusion, so the graph is seeded by a hybrid entry


16


Preprint.


set rather than by a single retriever. In practice, this detail matters because the quality of
the initial seeds strongly influences whether later graph expansion can recover the correct
prerequisite chain.


**Reverse-Aware** **Structural** **Diffusion.** Retrieval over the graph uses a Personalized
PageRank-style diffusion operator constructed from the directed typed edges. The implementation first inserts forward transition mass along each stored edge, and then injects
type-specific reverse transitions so that relevance can flow back from a matched high-level
skill toward likely prerequisites. The reverse coefficients are largest for dependency edges
and smaller for workflow, semantic, and alternative links, reflecting the fact that reverse
traversal is most justified when recovering executable prerequisites. Operationally, this means
the graph remains directed, but retrieval is explicitly reverse-aware. GoS therefore does
not collapse the graph into an undirected graph; instead, it performs controlled backward
propagation during scoring.


**Reranking** **and** **Budgeted** **Hydration.** The stationary graph score is not exposed to the
agent directly. After diffusion, GoS reranks candidate skills by combining graph relevance
with field-level query evidence, then hydrates only the top skills into an agent-facing bundle
under both per-skill and global context budgets. Each hydrated payload includes a concise
skill rendering, relevant execution notes, and the original local source path. The retrieval
output therefore functions as a bounded execution context rather than a generic search-result
list. This final budgeted hydration step is essential for preserving the efficiency advantage
over flat all-skills loading while still presenting enough structure for downstream execution.


**Section** **Summary.** From an implementation perspective, GoS is best understood as a
hybrid graph-construction and retrieval system: deterministic parsing and I/O matching
provide a reliable executable backbone; optional LLM semantic completion improves node
quality when documentation is incomplete; sparse LLM relation validation adds higher-order
inter-skill structure; and reverse-aware graph diffusion converts a small hybrid seed set
into a compact, more execution-complete bundle. These implementation choices are what
instantiate the central claim of the paper that structural retrieval should recover not only
relevant skills, but also the prerequisite context needed to use them effectively.


**C** **Prompt** **and** **Interface** **Examples**


**Layered** **Prompt** **Design.** GoS uses two prompt layers with deliberately separated
responsibilities. The first layer operates _inside_ the indexing and retrieval stack, where
LLMs are used only for constrained normalization, optional query rewriting, and sparse
relation validation. The second layer operates at the _agent_ _interface_, where the environment
prompt tells the downstream agent when to call retrieval, how to interpret the returned
bundle, and how strongly to prefer reuse over open-ended exploration. This separation
is methodologically important. Graph-side prompts determine what semantic structure
enters the retrieval substrate, whereas agent-side prompts determine whether that retrieved
structure is converted into a verifier-aligned execution plan.


**Presentation** **Goal.** This section is not intended to enumerate full prompt templates.
Instead, it exposes the narrow prompt fragments and interface rules that are most important
for understanding the method. From a reviewer perspective, the key point is that GoS does
not rely on unconstrained prompt engineering. The internal prompts are used to normalize
or validate bounded objects, and the external interface is used to constrain downstream
behavior once retrieval has occurred. Together, these prompts form an interface contract
between offline graph construction and online execution.


**Internal** **Prompt** **A:** **Skill** **Semantic** **Completion.** The semantic-completion prompt
is intentionally narrow. It asks the model to normalize exactly one skill document and
extract only retrieval-critical fields. In the implementation, the prompt explicitly preserves
the canonical `name` and `description` when present, emphasizes high precision, and requires
the returned `edges` list to be empty. This design reflects a conservative use of LLMs: the


17


Preprint.


Table 7: Representative prompt and interface components in GoS. The table highlights the
small set of prompt contracts that shape graph construction and downstream agent behavior.













model is allowed to fill semantic gaps in node attributes, but not to invent graph structure.
Operationally, this improves the quality of node representations used for indexing while
avoiding a common failure mode in LLM-built graphs, namely relation over-generation. The
prompt is therefore best understood as a constrained semantic completion module, not as a
latent graph generator.


**Internal** **Prompt** **B:** **Relation** **Validation.** The relation-validation prompt is invoked
only after GoS has formed a small candidate pool using lexical overlap, semantic neighbors,
and I/O-based expansion. The prompt defines four edge types: _dependency_, _workflow_,
_semantic_, and _alternative_ . It also explicitly instructs the model to prefer sparse, highprecision edges, to emit nothing when uncertain, and to preserve exact skill names in the
`source` and `target` fields. This makes the prompt function more like a relation verifier than
a free-form graph generator. In practice, this design is important because it limits graph
density and preserves the typed semantics later used during reverse-aware diffusion.


18


Preprint.


This excerpt illustrates the central design principle of the internal extraction prompt: GoS
uses the LLM as a constrained semantic normalizer, not as an unconstrained graph author.
For the appendix, the important point is not merely that an LLM appears in the pipeline,
but that the allowable output space is sharply restricted to node-local semantic completion.


**Internal** **Prompt** **C:** **Query** **Rewrite.** The optional query-rewrite prompt maps a raw
task request to a compact retrieval schema with fields such as `goal`, `operations`, `artifacts`,
`constraints`, and `keywords` . The prompt explicitly instructs the model not to invent
benchmark-specific labels and to leave unclear fields empty. This is consistent with the
retrieval objective in GoS: rewriting is used only to expose retrieval-critical technical terms
such as file formats, APIs, protocols, and concrete operations. It is not intended to change the
task itself. When rewriting is disabled or unavailable, the system falls back to deterministic
lexical normalization, so query rewriting is a retrieval enhancement rather than a mandatory
dependency. In other words, the prompt improves lexical and semantic coverage at the seed
stage, but it is not allowed to redefine the problem.


**Agent** **Interface** **Prompt.** In the SkillsBench GoS environment, the agent is instructed
to begin with a targeted retrieval query built from the task goal, artifact or format, operation
or API, and verifier-critical constraints. The interface then forces the agent to read the
retrieval status before continuing. A `NO_SKILL_HIT` response means the agent must explicitly
acknowledge that no relevant skill was found and proceed without claiming skill use. A
`SKILL_HIT` response means the returned bundle should be treated as a narrowing device:
the agent is told to use the returned local source paths, inspect scripts before implementing
from scratch, and prioritize the shortest path to verifier pass. This interface design matters
because the main quality difference is often not whether some relevant skill exists somewhere
in the library, but whether the agent receives a compact, execution-ready bundle early enough
to affect the trajectory. In that sense, the interface prompt is part of the method rather than
a presentation detail.







This second excerpt shows that the agent-facing interface is itself part of the method. It
does not merely expose a search command. It constrains when retrieval is called, how the
returned bundle is interpreted, and how aggressively the downstream agent is allowed to
branch away from authoritative local implementations. The resulting effect is to make
retrieval operational rather than decorative: the bundle is meant to narrow the search space
immediately, not merely provide optional background context.


**Section** **Summary.** Taken together, these examples show that prompt design in GoS is not
generic scaffolding. The internal prompts constrain how semantic structure enters the graph;
the external interface constrains how retrieved structure enters the agent’s working context.
The two layers therefore form an interface contract between offline graph construction and
online agent execution. This contract is especially important in our setting because many


19


Preprint.





**Algorithm** **1:** Offline graph construction for GoS


failures are not pure retrieval misses, but retrieval-hit trajectories in which the agent still
drifts unless the interface strongly biases it toward verifier-minimal reuse. The appendix
evidence should therefore be read as support for a broader methodological claim: in graphaugmented agent systems, retrieval quality depends not only on what is indexed, but also on
how the retrieved structure is exposed and behaviorally enforced downstream.


**D** **Core** **Retrieval** **Pseudocode**


**Presentation Goal.** For completeness, we provide pseudocode for the two main algorithmic
stages of GoS: offline graph construction and online structural retrieval. The presentation is
intentionally close to the implementation, but abstracted enough to foreground the method
rather than the surrounding engineering details.


**Implementation** **Correspondence.** Algorithm 1 corresponds to the parser-first normalization and relation-induction logic in the GoS implementation. Algorithm 2 corresponds to
the retrieval path and the reverse-aware Personalized PageRank utilities. In practice, these
stages additionally include engineering details such as workspace bootstrapping, embeddingdimension checks, source-path rewriting for containerized environments, and context clipping
under hard character budgets. We omit those details from the pseudocode because they
are not conceptually central, but they are nevertheless important for stable end-to-end
deployment.


**E** **Error** **Analysis**


**Error** **Taxonomy.** We distinguish retrieval-side errors from downstream execution failures,
since these correspond to different limits of the overall system. A retrieval method can
fail because it never surfaces the correct skill, because it retrieves an incomplete bundle
that omits critical prerequisites, or because it produces a broadly adequate bundle that is
subsequently misused by the downstream agent. Treating these failure modes separately is
important for attributing gains correctly: GoS is designed to improve retrieval completeness,
but it cannot by itself eliminate planning or execution failures once a bundle has already
been provided. Across our trajectories, several of the most informative failures are not simple


20


Preprint.





**Algorithm** **2:** Online graph-based skill retrieval


Table 8: Primary error modes in GoS-style retrieval experiments. The table separates
retrieval failures, downstream execution failures, and infrastructure issues.















retrieval misses, but long-horizon search failures in which the correct general tool family is
present and the agent still does not converge to a verifier-passing implementation.


**Retrieval** **Misses.** A retrieval miss occurs when the correct skill exists in the repository
but is not surfaced at all. In this regime, the agent is forced onto a generic from-scratch
path, so any downstream failure should be attributed primarily to the retriever rather
than to execution drift. Misses typically arise when the query language does not overlap strongly with the skill description, when the task is phrased around a downstream
objective but the critical skill is an upstream parser or setup utility, or when semantic
retrieval overweights topical similarity relative to executable relevance. A representative
example is `dapt-intrusion-detection` . In the failed GoS-style trajectory, the agent issued
`graphskills-query` but did not recover `pcap-analysis`, instead receiving an irrelevant
bundle that included items such as `dc-power-flow` and `dialogue-graph` . By contrast, the
stronger baseline trajectory opened `pcap-analysis` and reused its tested helper code. The


21


Preprint.


resulting difference in behavior is characteristic of a true retrieval miss: once the relevant
analysis skill is absent, the task degrades into from-scratch implementation and fails the
verifier.


**Partial** **Retrieval.** Partial retrieval is more subtle and often more important. Here,
the retrieved bundle contains an obviously relevant high-level skill, but omits one or more
prerequisite helpers needed for successful completion. In our setting, these missing items are
often parsers, format converters, preprocessing utilities, setup routines, or constraint-carrying
reference skills. This is precisely the regime in which graph-aware retrieval is intended to
help: once a high-level skill is matched as a seed, reverse-aware propagation can recover
supporting skills that are weak semantic matches to the raw query but strong structural
neighbors in the skill graph. `earthquake-phase-association` illustrates the boundary
of this idea. In the stronger all-skills trajectory, the agent assembled a coherent seismic
stack including `gamma-phase-associator`, `obspy-data-api`, `seisbench-model-api`, and
`seismic-picker-selection`, and the task passed. In the corresponding GoS case, the
graph retrieval did bring in a partially relevant seismic bundle, but the resulting context
was still less complete, and the task failed with reward 0 _._ 0. This suggests that structural
retrieval helps only when the recovered neighborhood is sufficiently complete to support the
downstream pipeline, not merely when one or two domain-relevant skills are present.


**Good** **Retrieval,** **Bad** **Execution.** Some failures occur even when the retrieved bundle
is broadly adequate. In these cases, the agent may still over-generalize the task, ignore
a retrieved authoritative interface, implement unnecessary functionality, or fail to align
with the verifier. These episodes matter because they bound what can be credited to
retrieval alone. They also motivate the conservative agent-facing instructions used in our
environments, which emphasize verifier-minimal solutions, direct use of returned local source
paths, and avoidance of unnecessary branching. `energy-market-pricing` is a representative example: both all-skills and GoS had access to the relevant economic-dispatch /
power-flow skill family and both eventually passed, but the all-skills trajectory required
substantially more agent time before converging. This is not a retrieval miss; it is a difference in how efficiently a broadly adequate bundle is converted into a verifier-passing plan.
Conversely, `adaptive-cruise-control` shows the opposite failure mode: the retrieved bundle included clearly relevant control skills such as `pid-controller`, `mpc-horizon-tuning`,
`vehicle-dynamics`, and `simulation-metrics`, yet the run still finished with reward 0 _._ 0. In
that case the failure is better described as long-horizon execution drift or verifier mismatch
rather than poor retrieval.


A related example is `dialogue-parser` . Multiple conditions had access to relevant task
structure, yet only the strongest GoS trajectory converted that context into a full pass,
while other conditions remained at partial reward. This again indicates that the dominant
bottleneck was not the absence of any relevant skill at all, but how effectively the agent
translated the available skill context into the exact output expected by the verifier.


**Infrastructure** **Failures.** Finally, a subset of observed failures are not retrieval failures at
all, but infrastructure failures such as environment build issues, setup crashes, or startup
timeouts before a substantive episode begins. These cases are methodologically important
but conceptually distinct: they should be tracked for experiment hygiene and rerun logic,
yet they should not be interpreted as evidence against the quality of the retrieval method
or the underlying model. Representative examples include Docker / BuildKit failures such
as `layer` `does` `not` `exist` on `dapt-intrusion-detection`, missing compiler toolchains for
`obspy` -dependent tasks, and logging failures that leave some trials with incomplete session
traces or null token fields. These episodes matter operationally because they require reruns
and infrastructure fixes, but they are not evidence about the retrieval quality of GoS, vector
retrieval, or all-skills. For this reason, we treat them as experiment-hygiene issues and
exclude them from method-quality interpretation whenever possible.


22


Preprint.


**F** **Qualitative** **Analysis**


**Section** **Framing.** We next examine a set of trajectory-grounded qualitative cases and
compare the concrete skill evidence that actually entered the agent’s working context in each
condition. Table 9 reports the skills that materially shaped each run: for GoS and Vector
Skills, these are the skills surfaced by the retrieval call and then used downstream, while for
_Vanilla_ _Skills_ they are the skills the agent explicitly opened from the mounted library. This
keeps the comparison grounded in executed trajectories rather than hypothetical retrieval
quality.


Across the cases below, we focus on a single question: does the method expose a compact,
execution-ready bundle early enough to change the trajectory? The main qualitative difference
is often not whether a relevant skill exists somewhere in the repository, but whether the
agent receives the right subset in a form that can be operationalized under the task budget.


**Case** **Study** **1:** **Pedestrian** **Traffic** **Counting.** The clearest intermediate case in
our trajectories is `pedestrian-traffic-counting` . The task requires frame extraction, reliable pedestrian counting, and structured output generation. GoS surfaced a
compact visual pipeline centered on `gemini-count-in-video`, `video-frame-extraction`,
and `openai-vision`, and achieved the strongest outcome among the three conditions
(0 _._ 417). The _Vanilla_ _Skills_ baseline did eventually open relevant helpers, including
`gemini-count-in-video`, `video-frame-extraction`, and `object_counter`, but reached
only a partial score (0 _._ 267). The _Vector_ _Skills_ run performed worst (0 _._ 041): although it
issued the retrieval call, the retrieved context was not converted into a workable plan. This
example is useful because it is not a pure pass/fail contrast. _Vanilla_ _Skills_ does locate
relevant functionality, but GoS exposes a smaller and more coherent bundle that appears
easier to operationalize within the available task budget.


**Case** **Study** **2:** **Flood** **Risk** **Analysis.** The `flood-risk-analysis` task illustrates a
different regime: both GoS and _Vanilla_ _Skills_ succeed, but GoS exposes the required
chain with much less search friction. In this task the correct workflow is not generic timeseries analysis; it is specifically the combination of `usgs-data-download` for measurements,
`nws-flood-thresholds` for stage cutoffs, and `flood-detection` for aggregation and comparison. GoS surfaced exactly this bundle and passed with reward 1 _._ 0. The _Vanilla_ _Skills_
baseline also passed with reward 1 _._ 0, but only after the agent explicitly searched through the
large mounted library and opened the same family of skills. _Vector_ _Skills_, by contrast, issued
the retrieval command but never translated retrieval into a usable flood-analysis bundle,
and the run failed with reward 0 _._ 0. This case is useful because it does not primarily show a
reward gap between GoS and _Vanilla_ _Skills_ ; instead, it shows that when the right execution
chain exists in the repository, GoS mainly helps by making that chain explicit earlier in the
trajectory.


**Case** **Study** **3:** **Travel** **Planning.** The `travel-planning` task is informative precisely because all three conditions surfaced clearly relevant travel skills. In the GoS run, the retrieved
context centered on `search-cities`, `search-accommodations`, `search-attractions`,
`search-driving-distance`, and `search-restaurants`, which is very close to the intended
tool chain for the task. The _Vanilla_ _Skills_ baseline likewise opened essentially the same
family of skills after searching through the library. _Vector_ _Skills_ also surfaced and used
this same cluster of `search-*` skills, and that run passed the verifier with reward 1 _._ 0. This
example sharpens the qualitative claim of the paper. The advantage of GoS is not that flat
semantic retrieval can never recover the correct skill family; rather, it is that GoS more
reliably exposes a compact and coherent bundle early in the episode. When _Vector_ _Skills_
does succeed, as it does here, its behavior becomes qualitatively much closer to GoS than to
a clean retrieval miss.


**Case** **Study** **4:** **Network** **Intrusion** **Detection.** A clean GoS-positive example is
`dapt-intrusion-detection` . In this case, GoS surfaced `pcap-analysis` together with
adjacent analysis helpers such as `pcap-triage-tshark` and `threat-detection`, and the
task passed. By contrast, the corresponding vector condition retrieved unrelated automation

23


Preprint.


oriented skills rather than a usable PCAP analysis bundle, while the all-skills condition
still failed despite full library access. This case is a useful counterpart to the retrieval-miss
pattern discussed in the Error Analysis section: once retrieval surfaces the right analysis
bundle, the task becomes a reuse problem rather than a from-scratch reverse-engineering
problem.


**Case** **Study** **5:** **Dialogue** **Parsing.** The `dialogue-parser` examples show a strong
gradient across methods. GoS converted the task into a full pass while exposing a compact
bundle centered on `dialogue_graph`, together with structural helpers such as `obj-exporter`,
`browser-testing`, and parser-oriented support. _Vanilla_ _Skills_ eventually improved once it
explicitly opened `dialogue_graph`, and _Vector_ _Skills_ also reached a substantial partial score,
but neither condition showed the same level of structured completeness as the strongest
GoS trajectory. This case illustrates a pattern that appears repeatedly: once the right
latent-representation skill is surfaced early, the rest of the pipeline becomes much easier for
the agent to operationalize.


**Case** **Study** **6:** **Earthquake** **Phase** **Association.** `earthquake-phase-association`
is a useful negative case for GoS because it shows that structural retrieval
does not help automatically when the recovered neighborhood is still incomplete.
In the strongest all-skills trajectory, the agent assembled a seismic processing
stack including `gamma-phase-associator`, `obspy-data-api`, `obspy-datacenter-client`,
`seisbench-model-api`, and `seismic-picker-selection`, and the task passed. The corresponding GoS case surfaced only a weaker subset, centered on `gamma-phase-associator`,
`seisbench-model-api`, and `seismic-picker-selection`, with an irrelevant distraction skill
mixed into the bundle, and the task failed. This is exactly the kind of case that is easy to
miss if one looks only at whether some domain-relevant skill was retrieved. The qualitative
difference is that the all-skills trajectory assembled a more execution-complete stack, while
the GoS trajectory remained one step short of the required pipeline.


**Case** **Study** **7:** **Energy** **Market** **Pricing.** A final useful case is `energy-market-pricing`,
where all-skills and GoS both passed but with very different trajectory quality. The all-skills
condition explicitly used `dc-power-flow` and `economic-dispatch`, while GoS surfaced a
broader but still coherent optimization bundle including `dc-power-flow`, `power-flow-data`,
`locational-marginal-prices`, and `casadi-ipopt-nlp` . Both runs eventually passed the
verifier, but the trajectory quality differed sharply: GoS converted the retrieved bundle into
a solution with substantially less agent-side search. This is one of the clearest examples
in which the main value of GoS is not higher reward, but a shorter path from retrieval to
execution.


**Case** **Study** **8:** **3D** **Scan** **Calculation.** The `3d-scan-calc` task serves as a useful
control because all three conditions can succeed when they recover the same latent geometry
bottleneck. GoS exposed `mesh-analysis` together with adjacent geometric helpers, directly
matching the preprocessing structure of the task. _Vanilla_ _Skills_ also reached a passing
solution once the agent opened `mesh-analysis`, but the surrounding library context was
notably noisier. _Vector_ _Skills_ likewise passed when it surfaced `mesh-analysis` together
with geometry-oriented companions such as `obj-exporter`, `pymatgen`, and `threejs` . The
qualitative lesson is therefore not that GoS is uniquely capable of solving the task; rather,
when all methods recover a geometry-centered bundle, all can succeed, and the remaining
difference is how directly that bundle is exposed.


**Case** **Study** **9:** **Adaptive** **Cruise** **Control.** `adaptive-cruise-control` is a useful
failure case because all three conditions surfaced highly plausible control-related skills
and still failed. GoS exposed `imc-tuning-rules`, `pid-controller`, `safety-interlocks`,
and `vehicle-dynamics`, while _Vector_ _Skills_ surfaced an even more explicit control bundle including `pid-controller`, `mpc-horizon-tuning`, `integral-action-design`,
`simulation-metrics`, and `vehicle-dynamics` . The _Vanilla_ _Skills_ condition also had access
to a broad control-oriented context, yet none of the three settings converged to a passing
solution. This case is important precisely because it is not a retrieval miss. It shows that once


24


Preprint.


the task requires a long control-design and verifier-alignment chain, even a qualitatively good
skill bundle may not be enough; the dominant bottleneck shifts from retrieval to execution
discipline.


**Case** **Study** **10:** **Economic** **Detrending** **and** **Correlation.** The
`econ-detrending-correlation` task offers a complementary success case. GoS surfaced `timeseries-detrending` and converted the task into a full pass, while the all-skills
condition failed to assemble a comparably coherent detrending-centered bundle. _Vector_ _Skills_
also reached a full pass, but with a noisier retrieved context whose skills were only weakly
connected to the intended econometric workflow. This case is useful in two ways. First, it
shows another task where surfacing the right latent preprocessing step, here detrending
rather than raw correlation, materially changes the result. Second, it reinforces the lesson
from `travel-planning` : vector retrieval can still succeed, but its successful episodes do not
always arise from a bundle that is as semantically crisp or structurally interpretable as the
one surfaced by GoS.


**Takeaway.** Across all ten qualitative cases in this appendix, the main pattern is not
simply that GoS retrieves skills with better topical overlap. Rather, GoS more often
exposes a bundle that is already close to the executable decomposition of the task.
The `pedestrian-traffic-counting` example shows a genuine middle case in which
_Vanilla_ _Skills_ finds relevant tools but still underperforms the tighter GoS bundle. The
`flood-risk-analysis` example shows that when the correct chain is available to multiple
methods, GoS mainly reduces search friction and makes the intended execution path explicit
earlier. The `travel-planning`, `3d-scan-calc`, and `econ-detrending-correlation` examples show that _Vector_ _Skills_ can also succeed when it recovers the right family of skills, but
these successes are most convincing when the retrieved bundle becomes qualitatively similar
to what GoS surfaces directly. The `dialogue-parser` and `dapt-intrusion-detection`
cases show how GoS can convert that structural advantage into clearer downstream wins.
By contrast, `earthquake-phase-association` shows a real boundary condition in which
GoS still falls short of an execution-complete bundle, while `energy-market-pricing` and
`adaptive-cruise-control` show that even with broadly adequate retrieval, trajectory efficiency and verifier alignment remain separate bottlenecks. Taken together, these cases
support the core claim of the paper: structural retrieval helps not only by improving relevance,
but by presenting agents with a more execution-ready context.


25


Preprint.


Table 9: Trajectory-grounded skill evidence from executed qualitative cases. Useful denotes
skills that were clearly operationalized downstream; Noisy denotes retrieved or opened items
that were tangential or not visibly used.

















































26


