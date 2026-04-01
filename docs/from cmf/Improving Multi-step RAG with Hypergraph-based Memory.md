Preprint

## IMPROVING MULTI-STEP RAG WITH HYPERGRAPH- BASED MEMORY FOR LONG-CONTEXT COMPLEX RE### LATIONAL MODELING


**Chulun Zhou** [1] _[∗]_ **,** **Chunkang Zhang** _[∗]_ **,** **Guoxin Yu,** **Fandong Meng** [2] **,** **Jie Zhou** [2] **,**
**Wai Lam** [1] _[†]_ **,** **Mo Yu** [2] _[†]_

The Chinese University of Hong Kong [1], WeChat AI [2]
_{_ clzhou,wlam _}_ @se.cuhk.edu.hk, zkang5051@gmail.com
moyumyu@global.tencent.com


ABSTRACT


Multi-step retrieval-augmented generation (RAG) has become a widely adopted
strategy for enhancing large language models (LLMs) on tasks that demand global
comprehension and intensive reasoning. Many RAG systems incorporate a working memory module to consolidate retrieved information. However, existing memory designs function primarily as passive storage that accumulates isolated facts
for the purpose of condensing the lengthy inputs and generating new sub-queries
through deduction. This static nature overlooks the crucial high-order correlations
among primitive facts, the compositions of which can often provide stronger guidance for subsequent steps. Therefore, their representational strength and impact on
multi-step reasoning and knowledge evolution are limited, resulting in fragmented
reasoning and weak global sense-making capacity in extended contexts.
We introduce HGMEM, a hypergraph-based memory mechanism that extends the
concept of memory beyond simple storage into a dynamic, expressive structure for
complex reasoning and global understanding. In our approach, memory is represented as a hypergraph whose hyperedges correspond to distinct memory units, enabling the progressive formation of higher-order interactions within memory. This
mechanism connects facts and thoughts around the focal problem, evolving into
an integrated and situated knowledge structure that provides strong propositions
for deeper reasoning in subsequent steps. We evaluate HGMEM on several challenging datasets designed for global sense-making. Extensive experiments and
in-depth analyses show that our method consistently improves multi-step RAG
and substantially outperforms strong baseline systems across diverse tasks. [1]


1 INTRODUCTION


Single-step retrieval-augmented generation (RAG) often proves insufficient for resolving complex
queries within long contexts (Trivedi et al., 2023; Shao et al., 2023; Cheng et al., 2025), motivating the shift toward multi-step RAG methods that iteratively interleave retrieval with reasoning. To
effectively capture dependencies across steps and condense the lengthy processing history, many approaches incorporate working memory mechanisms inspired by human cognition (Lee et al., 2024;
Zhong et al., 2024). However, current memory-enhanced multi-step RAG methods still face challenges in complex relational modeling, especially for resolving global sense-making tasks over long
contexts.


During multi-step RAG execution, a straightforward implementation of working memory mechanism is to let a large language model (LLM) summarize the interaction history into a plaintext
description of current problem-solving state. This strategy has been widely adopted since early studies (Li et al., 2023; Trivedi et al., 2023) as well as in commercial systems (Jones, 2025; Shen & Yang,
2025). Nonetheless, such unstructured memory mechanisms cannot be manipulated with sufficient


*Equal contribution. _†_ : Co-corresponding authors.
[1We release our code at https://github.com/Encyclomen/HGMem](https://github.com/Encyclomen/HGMem)


1


Preprint


accuracy across steps and often lose the ability to back-trace references to retrieved texts. Consequently, recent research has shifted toward structured or semi-structured working memory, typically
with predefined schemas such as relational tables (Lu et al., 2023), knowledge graphs (Oguz et al.,
2022; Xu et al., 2025), or event-centric bullet points (Wang et al., 2025).


However, existing memory mechanisms often treat memory as static storage that continually accumulates meaningful but primitive facts. This view overlooks the evolving nature of human working
memory, which incrementally incorporates higher-order correlations from previously memorized
content. This capacity is particularly crucial for resolving global sense-making tasks that involve
complex relational modeling over long contexts. In such scenarios, the required knowledge for tackling a query is often composed of complex structures that extend beyond predefined schemas, and
reasoning over long lists of primitive facts is both inefficient and prone to confusion with mixed or
irrelevant information. Current memory mechanisms in multi-step RAG systems lack these abilities,
preventing memory from effectively guiding LLMs’ interaction with external data sources. These
limitations highlight the need for a working memory with stronger representational capacity.


In this paper, we propose a hypergraph-based memory mechanism (HGMEM) for multi-step RAG
systems, which enables memory to evolve into more expressive structures that support complex
relational modeling to enhance LLMs’ understanding over long contexts. Hypergraphs, as a generalization of graphs, are particularly well-suited for this purpose (Feng et al., 2019). In our design,
memory is structured as a hypergraph composed of hyperedges, each treated as a distinct memory
point that represents a specific perspective of the memorized information. Initially, these memory
points encode low-order primitive facts. As the LLM interacts with external environments, higherorder correlations among memory points gradually emerge and are progressively integrated into the
memory through update, insertion, and merging operations. At each step before response generation,
the LLM examines the current memory and generates subqueries, enabling adaptive memory-based
evidence retrieval for both focused local investigation and broad global exploration.


This rich and structured memory facilitates broader contextual awareness and stronger reasoning in
real-world applications by offering several advantages. First, it maintains an **integrated** **body** **of**
**knowledge** around the focal problem by synthesizing primitive evidence and intermediate thoughts,
typically going _beyond_ _predefined_ _schemas_ and providing a _global_ _perspective_ over the evidence.
Second, it offers **structured** **and** **accurate** **guidance** for the LLM’s sustained interactions in two
ways: (1) enabling subsequent reasoning to start from representational propositions rather than from
a long list of disparate primitive facts; and (2) leveraging the topological structure of hypergraph to
guide subquery generation and evidence retrieval in a more accurate manner.


We conduct extensive experiments on several challenging tasks involving global sense-making questions within long contexts. The results show that our HGMEM achieves significant improvements
over competitive RAG baselines, confirming the advantages.


2 RELATED WORK


2.1 WORKING MEMORY MECHANISMS FOR MULTI-STEP RAG


Starting from ReAct (Yao et al., 2023), many multi-step RAG systems have incorporated reflections
to integrate available information for subsequent decisions. These reflections can be regarded as a
simple form of memory. With the development of structured indexing for RAG, working memory
also borrows this idea. Prevailing studies (Li et al., 2023; 2025a; Shen & Yang, 2025; Chhikara et al.,
2025; Xu et al., 2025) save agent behavior, such as task decomposing, execution tracking, and result
verification, to manage task context more effectively, representing a step toward explicit working
memory for complex multi-agent coordination. This idea also matured in chain-of-thought (CoT)
and multi-round RAG, where working memory is represented as iteratively updated records of reasoning steps or retrieved evidence. For example, IRCOT (Trivedi et al., 2023) and ComoRAG (Wang
et al., 2025) employ a dynamic memory workspace to iteratively consolidate past knowledge or steps
and incorporate new evidence, supporting scalable and iterative reasoning across multiple steps.


Some studies take a step further to adopt a graph-structured working memory to enhance multi-step
RAG (Liu et al., 2024; Li et al., 2025a). ERA-CoT (Liu et al., 2024) aids LLMs in understanding
context through a series of pre-defined reasoning substeps performing entity-relationship analysis.


2


Preprint


KnowTrace (Li et al., 2025a) equips LLMs with a graph-based working memory to trace relevant
knowledge through multi-step RAG execution. However, the working memories of these graphenhanced work do not effectively support modeling high-order correlations among multiple entities/relationships as each edge in their graphs can intrinsically describe at most binary relationships.
By contrast, due to the high-order nature of hypergraph structure, our HGMEM naturally enables
its working memory to evolve into more expressive forms capable of flexibly modeling high-order
_n_ -ary ( _n >_ 2) relations. This advantage helps to fully unleash the reasoning capability of LLMs for
multi-step RAG, especially crucial for resolving global sense-making questions that require complex
reasoning and deep understanding over long contexts.


2.2 RAG WITH STRUCTURED KNOWLEDGE INDEX


There is a long line of work that studies managing extended corpora through structured knowledge
indexing to enhance RAG. Though different from our focus on working memory mechanism, these
work can be viewed as building structured (and static) long-term memory before actually tackling
user queries, thus are relevant. Specifically, tree-structured methods, such as RAPTOR (Sarthi et al.,
2024), T-RAG (Fatehkia et al., 2024), and TreeRAG (Tao et al., 2025), organize text chunks or entity
hierarchies, enabling multi-level or bidirectional retrieval to enhance context integration. Another
line of research focuses on building graph-structured index to flexibly represent knowledge for enhancing RAG systems (Xu et al., 2024a; Edge et al., 2024; Guo et al., 2024; Li et al., 2025b). For
example, GraphRAG (Edge et al., 2024) and LightRAG (Guo et al., 2024) build entity graphs and
community-level summaries, or leverage graph-enhanced indexing for dual-level retrieval, leading
to improvements in global reasoning, retrieval efficiency, and response diversity. CAM (Li et al.,
2025b) proposes a constructivist agentic memory that flexibly assimilates and accommodates input
texts within a hierarchical graph. Hyper-RAG (Feng et al., 2025), HypergraphRAG (Luo et al.,
2025) and PropRAG (Wang, 2025) adopt hypergraph to build their structured knowledge index and
design retrieval/search algorithms for query resolving. In addition, there are also a range of other
memory mechanisms, essentially structured knowledge index, that simulate long contexts or dialog
histories as long-term memory to improve RAG systems. According to the form of memory representation, they can be basically classified as contextual memory (Chen et al., 2023; Gutierrez et al.,
2024; Lee et al., 2024; Li et al., 2024b; Guti´errez et al., 2025) and parametric memory (Qian et al.,
2025).


However, these existing studies merely leverage their structured index (or memory) as static storage,
which are typically constructed during an offline indexing stage before actually responding to user
queries.


3 METHODOLOGY


We introduce HGMEM, the hypergraph-based memory mechanism designed to facilitate better contextual awareness and reasoning in multi-step RAG settings with structured data sources, especially
for long-context tasks that require complex global sense-making.


3.1 PROBLEM FORMULATION


In this work, we consider the kind of tasks for LLMs to resolve a query based on a given document.
Besides the plain texts, we assume that the document has been preprocessed into a graph through
an offline graph-building stage, where entities and relationships are extracted from the document
passage.Formally, let us denote the document as _D_ segmented into a set of small manageable text
chunks _{d_ 1 _, d_ 2 _, ..., d|D|}_, and the derived graph as _G_ composed of nodes _VG_ and edges _EG_ corresponding to the extracted entities and relationships, respectively. Each node _v ∈VG_ or edge _e ∈EG_
is associated with the source text chunks in which its embodied entity/relationship appears, which
is recorded during the offline graph construction. Meanwhile, the nodes, edges, and text chunks are
embedded into high-dimensional vectors for vector-based retrieval. For resolving the query, LLMs
have access to both the document and its derived graph as structured data sources.


3


Preprint


Figure 1: ( _i_ ) The RAG system at its _t_ -th interaction step. ①: The LLM adaptively generates a set
of subqueries _Q_ [(] _[t]_ [)] for either local investigation or global exploration (see Section 3.4). ②: _Q_ [(] _[t]_ [)] are
used to retrieve information from _D_ and _G_ . ③: _VQ_ ( _t_ ), _E_ ( _VQ_ ( _t_ )) and _D_ ( _VQ_ ( _t_ )) are obtained through
graph-based indexing and vector-based matching. ④: The LLM evolves current memory _M_ [(] _[t]_ [)] into
_M_ [(] _[t]_ [+1)] using Equation 2. ( _ii_ ) The structure of our proposed hypergraph-based memory that evolves
through update, insertion and merging operations.


3.2 MULTI-STEP RAG SYSTEM WITH MEMORY


When dealing with tasks requiring a comprehensive understanding, especially over the long context, RAG systems usually resort to multi-step approaches with an underlying memory mechanism,
where retrieval operations are interleaved with intermediate reasoning to support broader contextual
awareness.


Given a target query _q_ ˆ, the LLM iteratively interacts with _D_ and _G_ while managing a memory _M_ to
store relevant information for ultimately resolving ˆ _q_ . During each interaction step _t_, the LLM judges
whether the content of the current memory has been sufficient with respect to the target query.
If the memory is deemed sufficient, it immediately produces a response. Otherwise, it analyzes
current memory and generates several subqueries _Q_ [(] _[t]_ [)] that aim at fetching more information from
the external environment to enrich the memory. The prompts for generating subqueries are given in
Appendix E.


Let _RV_ ( _Q_ ) define the entity retrieval operation fetching the most relevant nodes to a query set _Q_
from a candidate node set _V_ using vector-based matching:



_RV_ ( _Q_ ) = 

_q∈Q_



argmax _nv_ (sim( **h** _q,_ **h** _v_ )) _,_ (1)
_v ∈V_



where _nv_ is the number of retrieved entities per query, **h** _q_ is the vector representation of _q_, **h** _v_ is the
vector representation of _v_, and sim( _·, ·_ ) is the cosine similarity function.


As illustrated in Figure 1 ( _i_ ), at the _t_ -th step, if the LLM proceeds to generate subqueries _Q_ [(] _[t]_ [)] based
on current memory _M_ [(] _[t]_ [)] maintained until the previous step, it retrieves a set of the most relevant
entities _VQ_ ( _t_ ) = _RVG_ ( _Q_ [(] _[t]_ [)] ) from _VG_ . Then, via graph-based indexing, the relationships and text
chunks associated with the entities in _VQ_ ( _t_ ) are also obtained, represented as _E_ ( _VQ_ ( _t_ )) and _D_ ( _VQ_ ( _t_ )),
respectively. [2] Subsequently, the LLM analyzes and consolidates this retrieved information into the


2We also use vector-based filtering to keep at most _ne_ relationships and _nd_ text chunks.


4


Preprint


memory, evolving memory into _M_ [(] _[t]_ [+1)], which can be formalized as


_M_ [(] _[t]_ [+1)] _←_ LLM( _M_ [(] _[t]_ [)] _, VQ_ ( _t_ ) _, E_ ( _VQ_ ( _t_ )) _, D_ ( _VQ_ ( _t_ ))) _._ (2)


Note that, at the initial step ( _t_ = 0), we treat the target query _q_ ˆ as a special subquery belonging to
_Q_ [(0)], _i.e. Q_ [(0)] = _{q_ ˆ _}_ . Further details about the memory storage, subquery generation and the dynamics of memory evolving will be elaborated in Section 3.3, Section 3.4 and Section 3.5, respectively.


3.3 HYPERGRAPH-BASED MEMORY STORAGE


When the LLM interacts with the document _D_ and the graph _G_, it continuously consolidates relevant
information into the memory storage _M_, which is modeled as a hypergraph:


_M_ = ( _VM,_ _E_ [˜] _M_ ) _,_ (3)


where _VM_ = _{v_ 1 _, v_ 2 _, ...}_ is the vertex set and _E_ [˜] _M_ = _{e_ ˜1 _,_ ˜ _e_ 2 _, ...}_ is the hyperedge set. It should
be noted that the vertices in _VM_ are actually equivalent to those nodes in _VG_, both embodying
identified entities. Particularly, _VM_ is a subset of _VG_ . In our implementation, we ensure that each
vertex _vi ∈VM_ must also exist in _G_ . [3] Formally, every vertex _vi ∈VM_ is represented as

_vi_ = (Ω _[ent]_ _vi_ _[,][ D][v]_ _i_ [)] _[,]_ (4)

where Ω _[ent]_ _vi_ stands for the information of its embodied entity, including name and description, and
_Dvi_ denotes the set of text chunks associated with this vertex _vi_ . Similarly, every hyperedge ˜ _ej ∈EM_
is represented as
_e_ ˜ _j_ = (Ω _[rel]_ _e_ ˜ _j_ _[,][ V][e]_ [˜] _j_ [)] _[,]_ (5)

where Ω _[rel]_ _e_ ˜ _j_ [characterizes the description of the embodied relationship and] _[ V][e]_ [˜] _j_ [is the set of involved]
vertices subordinate to this hyperedge _e_ ˜ _j_ . Particularly, the hyperedges can be treated as separate
memory points, each of which corresponds to a certain aspect of the entire information stored in
current memory, as shown in Figure 1 ( _ii_ ). Unlike those binary edges _EG_ that connect at most two
nodes in the external graph, a hyperedge can connect an arbitrary number (two or more) of vertices.
In this way, our hypergraph-based memory is capable of flexibly modeling high-order correlation
among multiple vertices ( _n_ _≥_ 2). As a result, the whole memory as a hypergraph can effectively
support complex relational modeling, ensuring strong expressiveness to enhance LLMs’ reasoning.


3.4 ADAPTIVE MEMORY-BASED EVIDENCE RETRIEVAL


As described in Section 3.2, at each step _t_ of our RAG workflow, with respect to the target query, the
LLM determines whether to immediately produce a response or proceed to acquire more information
from the external documents _D_ and graph _G_ . If current memory _M_ [(] _[t]_ [)] = ( _VM_ [(] _[t]_ [)] _[,]_ _[E]_ [˜] _M_ [(] _[t]_ [)][)] [is] [deemed]
insufficient, the LLM first analyzes _M_ [(] _[t]_ [)] and generates several subqueries _Q_ [(] _[t]_ [)] indicating what to
further explore. Specifically, we design an adaptive memory-based evidence retrieval strategy for
either local investigation or global exploration with _Q_ [(] _[t]_ [)] :


(i) Local Investigation: When the LLM plans to more deeply investigate some specific memory
points, its generated subqueries are utilized to trigger local evidence retrieval over _G_ . Concretely, suppose a _q ∈Q_ [(] _[t]_ [)] especially targets at inspecting _e_ ˜ _j ∈_ _E_ [˜] _M_ [(] _[t]_ [)][, the nodes corresponding]
to the vertices _Ve_ ˜ _j_ subordinate to _e_ ˜ _j_ are used as anchor nodes on _G_ . Thereafter, using the operation defined by Equation 1, entity retrieval is conducted within the neighborhood of these
anchors, which is formalized as


_Vq_ = _RN_ ( _Vej_ ˜ )( _q_ ) _,_ (6)


        _N_ ( _Ve_ ˜ _j_ ) = ( _NM_ ( _t_ )( _v_ ) _∪NG_ ( _v_ )) _,_

_v∈Vej_ ˜


where _NM_ ( _t_ )( _v_ ) represents the neighboring vertices of _v_ over _M_ [(] _[t]_ [)] and _NG_ ( _v_ ) represents the
neighboring nodes of _v_ over _G_ .


3If any vertex does not exist in _VG_, we forcibly insert it, along with its associated relationships, into _G_ .


5


Preprint

















Figure 2: An illustration of memory evolving dynamics. Each point is equivalent to a hyperedge in
the hypergraph. _M_ [(] _[t]_ [)] evolves into _M_ [(] _[t]_ [+1)] through update, insertion and merging operations.


(ii) Global Exploration: When there are unexplored aspects transcending the scope of current
memory, the LLM resorts to generating subqueries for exploring broader information from the
external documents and graph, not pertinent to any existing memory point. For a _q ∈Q_ [(] _[t]_ [)], the
process of entity retrieval can be written as
_Vq_ = _RC_ ( _M_ ( _t_ ))( _q_ ) _,_ (7)

_C_ ( _M_ [(] _[t]_ [)] ) = _VG_ _−VM_ ( _t_ ) _,_

where _C_ ( _M_ [(] _[t]_ [)] ) represents the available scope comprised of all nodes except those already
existing in the current memory.


Then, as in Section 3.2, the associated relationships _E_ ( _Vq_ ) and text chunks _D_ ( _Vq_ ) are obtained via
graph-based indexing. Finally, following Equation 2, the LLM evolves its current memory _M_ [(] _[t]_ [)]

into _M_ [(] _[t]_ [+1)] . Under such a strategy, the RAG system is able to adaptively combine both local
investigation and global exploration for more flexible information retrieval during interaction with
external data sources.


3.5 DYNAMIC OF MEMORY EVOLVING


Once a set of subqueries have been generated at the _t_ -th step, following Equation 2, the LLM analyzes the retrieved information and consolidates useful content into the current memory _M_ [(] _[t]_ [)],
resulting in the evolved memory _M_ [(] _[t]_ [+1)] . As shown in Figure 1 ( _ii_ ), on the basis of hypergraphbased memory storage, the dynamic of memory evolving in our proposed HGMEM involves the
following three types of operations:


- _**Update**_ . According to the retrieved information, if there are certain existing memory points whose
descriptions should be modified, the update operation will revise the descriptions of corresponding
hyperedges without changing their subordinate entities.

- _**Insertion**_ . The insertion operation should be evoked when some content of the retrieved information is suitable to be inserted as additional memory points into the current memory, which creates
new hyperedges in the hypergraph.

- _**Merging**_ . After insertion and update, the LLM inspects current memory and selectively merges
existing memory points that are more suitable to constitute a single semantically/logically cohesive unit. With respect to the target query _q_ ˆ, suppose the memory points _e_ ˜ _i_ =(Ω _[rel]_ _e_ ˜ _i_ _[,][ V][e]_ [˜] _i_ [)] [and]
_e_ ˜ _j_ =(Ω _[rel]_ _e_ ˜ _j_ _[,][ V][e]_ [˜] _j_ [)] [are] [to] [be] [merged] [into] [a] [high-order] [memory] [point] _[e]_ [˜] _[k]_ [=][(Ω] _[rel]_ _e_ ˜ _k_ _[,][ V][e]_ [˜] _k_ [)][,] [its] [description]
and subordinate vertices are acquired as

Ω _[rel]_ _e_ ˜ _k_ _[←]_ [LLM(Ω] _[rel]_ _e_ ˜ _i_ _[,]_ [ Ω] _[rel]_ _e_ ˜ _j_ _[,]_ [ ˆ] _[q]_ [)] (8)

_Ve_ ˜ _k_ = _Ve_ ˜ _i_ _∪Ve_ ˜ _j_ _._

Then, the newly merged memory point is added into the hyperedge set _E_ [˜] _M_ ( _t_ ) of the current memory _M_ [(] _[t]_ [)] . This merging operation over the hypergraph-based memory builds higher-order correlations among multiple existing memory points, facilitating the resolution of queries that require
complex relational modeling with disparate facts.


In this way, besides continuously accumulating primitive facts during the LLM’s interactions with
external data sources, the memory also gradually evolves into more sophisticated forms, capturing higher-order correlations for complex relational modeling. Figure 2 gives a concrete example
illustrating the dynamics of memory evolving.


6


Preprint


3.6 MEMORY-ENHANCED RESPONSE GENERATION


When the LLM exceeds its maximum interaction steps or the content in current memory
_M_ [(] _[t]_ [)] = ( _VM_ [(] _[t]_ [)] _[,]_ _[E]_ [˜] _M_ [(] _[t]_ [)][)] [has] [been] [deemed] [sufficient,] [a] [response] [is] [immediately] [produced] [according] [to]
the information stored in current memory. Concretely, besides the descriptions of all memory points
( _i.e._ _E_ [˜] _M_ [(] _[t]_ [)][), the text chunks associated with all the entities] _[ V]_ _M_ [(] _[t]_ [)] [in current memory are also provided]
to the LLM for producing the final response.


4 EXPERIMENTAL SETTINGS


4.1 DATASETS


We choose generative sense-making question answering (QA) (Edge et al., 2024; Guo et al., 2024)
and long narrative understanding (Li et al., 2024a; Xu et al., 2024b; Yu et al., 2025; Kocisk´y et al.,
2018; Karpinska et al., 2024; Yen et al., 2025; Zhou et al., 2025) as our evaluation tasks. For generative sense-making QA, similar to the setups used in previous works (Edge et al., 2024; Guo et al.,
2024), we retain a portion of long documents with more than 100k tokens from **Longbench V2** (Bai
et al., 2025). From each retained document, we use GPT-4o to generate several global sense-making
queries that satisfy the following requirements: 1) The queries should target the overall understanding of the whole provided documents, instead of only concentrating on several specific phrases or
sentence pieces. 2) The queries should require high-level understandings and global reasoning over
disparate evidence scattered across the whole paragraph. For long narrative understanding, we use
three public benchmarks including **NarrativeQA** (Kocisk´y et al., 2018), **NoCha** (Karpinska et al.,
2024) and **Prelude** (Yu et al., 2025). Both tasks require global comprehension and complex sensemaking over disparate evidence across long contexts. Details about the usage and statistics of data
used in our experiments are given in Appendix A.


4.2 IMPLEMENTATION DETAILS


**Offline Graph Construction.** For all the datasets used in our experiments, we first segment every
document into text chunks of 200 tokens with 50 overlapping tokens between adjacent chunks.
Then, GPT-4o is utilized to preprocess each of the chunkized documents into a graph using the
open-sourced tool provided by LightRAG (Guo et al., 2024). After building the graph, we adopt
_bge-m3_ (Chen et al., 2024) as the embedding model to convert all the entities, relationships and text
chunks into vector representations managed by _nano vector database_ .


**System** **Deployment** **and** **Configuration.** Our RAG system is comprised of the backbone LLM
and the hypergraph-based memory. We choose GPT-4o and Qwen2.5-32B-Instruct as the representatives of advanced closed-source and open-source LLMs, respectively. During experiments,
GPT-4o is accessed through the official API while Qwen2.5-32B-Instruct is locally deployed with
VLLM (Kwon et al., 2023). For the configuration of LLM inference, we set the temperature to
0.8 and the maximum number of output tokens to 2,048. As for the hypergraph-based memory, we
employ the _hypergraph-db_ package to maintain and manage the hypergraph at runtime. The vector representations of the nodes, hyperedges and associated text chunks in the hypergraph are also
generated by _bge-m3_ embedding model.


4.3 BASELINES AND EVALUATION METRICS


In our experiments, we compare our proposed HGMEM to two types of baseline methods, _i.e._ traditional RAG and multi-step RAG, which utilize plain texts and/or graph-structured data sources.
Among these methods, DeepRAG (Guan et al., 2025) and ComoRAG (Wang et al., 2025) are
equipped with a working memory, while the others are not. The details of these comparison methods
can be found in Appendix B. To ensure fair comparison, all baselines operate on a similar number
of retrieved passages. In the case of single-step RAG, this means retrieving the same average number of text chunks as our HGMEM. For multi-step RAG methods, we approximate comparability
by constraining them to rewrite the same maximum number of subqueries and perform the same
maximum number of steps, while requiring retrieval of the same average number of chunks per step.


7


Preprint


Table 1: The overall experimental results on four benchmarks. The second column “ **Working**
**Memory** ” distinguishes whether the corresponding method is equipped with a working memory
that enhances LLMs during RAG execution. The best scores in each dataset are **bolded** . HGMEM
consistently outperforms other comparison methods across all datasets.


**Type** **Working** **Method** **Longbench** **NarrativeQA** **NoCha** **Prelude**

**Memory** **Comprehensiveness** **Diversity** **Acc (%)** **Acc (%)** **Acc (%)**


_GPT-4o_



Traditional RAG



× NaiveRAG 61.62 64.20 52.00 67.46 60.00
× GraphRAG 60.39 64.02 53.00 70.63 59.26
× LightRAG 61.55 63.37 44.00 71.43 61.48
× HippoRAG v2 58.92 61.27 34.00 72.22 54.81



✓ DeepRAG 63.62 65.98 45.00 67.46 56.30
Multi-step RAG ✓ ComoRAG 62.18 65.82 54.00 63.49 54.07
Ours ✓ HGMEM **65.73** **69.74** **55.00** **73.81** **62.96**


_Qwen2.5-32B-Instruct_



Traditional RAG



× NaiveRAG 61.41 62.25 37.00 64.29 52.59
× GraphRAG 60.78 62.16 44.00 62.70 50.37
× LightRAG 60.82 62.73 40.00 59.52 60.74
× HippoRAG v2 56.66 60.80 33.00 68.25 51.85



✓ DeepRAG 61.45 63.56 44.00 66.40 51.11
Multi-step RAG ✓ ComoRAG 60.74 61.28 44.00 57.60 50.37
Ours ✓ HGMEM **64.18** **66.51** **51.00** **70.63** **62.22**


For generative sense-making QA, we adopt the following two metrics to assess the qualities of
model responses: 1) **Comprehensiveness** measures how well the model response comprehensively
covers and addresses all aspects and necessary details with respect to the target query. 2) **Diversity**
indicates how rich and diverse the response is in providing various perspectives and insights related
to the query. We employ GPT-4o as the judge to evaluate the model responses according to the
grading criteria that gives scores ranging from 0 to 100 based on a two-step scoring scheme, as
detailed in Appendix F.


For long narrative understanding, including NarrativeQA, Nocha, and Prelude, we uniformly use
prediction accuracy (Acc) as the reported metric. Specifically, for NarrativeQA, prior studies (Bulian et al., 2022; Wang et al., 2024; Zhou et al., 2025) have shown that conventional token-level
metrics such as Exact Match and F1 score usually fail to reflect actual semantic equivalence between hypothesis and reference answer, especially for abstractive answers. Therefore, we also apply
GPT-4o for judging whether the LLM’s prediction fully entails the reference answer, producing a
binary True/False decision.


5 RESULTS AND ANALYSIS


5.1 OVERALL RESULTS


Table 1 reports the overall results across all evaluation tasks. Our HGMEM consistently outperforms
both single-step and multi-step RAG baselines on every dataset. Importantly, our HGMEM with
Qwen2.5-32B-Instruct matches or even outperforms baselines powered by the stronger GPT-4o,
underscoring its value in resource-efficient scenarios.


The baselines exhibit mixed performance patterns reflecting their respective representational
strengths. For instance, HippoRAG v2 relies on knowledge triples, which provide strong fact representation but limited coverage of events and plots. As a result, it performs well on NoCha but
falls behind NaiveRAG on NarrativeQA. In contrast, GraphRAG and LightRAG excel at building
global representations but are weaker at capturing fine-grained details, leading them to outperform
other baselines on Prelude and NarrativeQA. The two multi-step RAG methods, which mainly employ working memory to iteratively generate subqueries in a chaining fashion, struggle with sensemaking questions, where integrating higher-order relationships is essential.


In comparison, our HGMEM provides strong compositional representations that span from facts to
plots, equipping LLM reasoning with high-order correlations and integrated evidence. This enables
it to meet the diverse requirements posed by the evaluation tasks.


8


Preprint


Figure 3: Prediction accuracies at different steps using Qwen2.5-32B-Instruct on long narrative
understanding datasets.


Table 2: Ablation results using Qwen2.5-32B-Instruct. “ _w/._ GE Only” and “ _w/._ LI Only” stand for
subquery generation strategies with Global Exploration and Local Investigation, respectively. “ _w/o._
Update” and “ _w/o._ Merging” refer to HGMEM ablating update and merging operations during
memory evolving, respectively.


**Longbench** **NarrativeQA** **Nocha** **Prelude**
**Ablation Type** **Method**

**Comprehensiveness** **Diversity** **Acc (%)** **Acc (%)** **Acc (%)**


HGMEM **64.18** **66.51** **51.00** **70.63** **62.22**
Retrieval Strategy _w/._ _GE Only_ 59.25 61.67 47.00 68.25 59.26
_w/._ _LI Only_ 61.38 63.82 43.00 63.49 60.00


HGMEM **64.18** **66.51** **51.00** **70.63** **62.22**
Memory Evolution _w/o._ _Update_ 62.48 64.92 50.00 68.25 60.00
_w/o._ _Merging_ 61.76 61.80 43.00 61.11 57.78


5.2 PERFORMANCE AT DIFFERENT STEPS


During the execution of our multi-step RAG system, the memory progressively evolves and guides
the LLM to proceed with retrieval and reasoning. To inspect the effects of memory evolving over
multiple interaction steps, we force the LLM to generate responses at every step for a total of six
turns, even if it originally decides to terminate the iteration earlier. Figure 3 presents the performances at different steps using Qwen2.5-32B-Instruct on long narrative understanding tasks. Note
that _t_ =0 represents the initial step when the target query _q_ ˆ is used for retrieval. We can observe that
our HGMEM achieves its best performance at _t_ =3, mostly outperforming NaiveRAG and LightRAG
baselines across steps. More steps bring no further improvements at a higher cost.


5.3 ABLATION STUDIES


**Evidence** **Retrieval** **Strategy.** When the LLM determines to acquire more information from _D_
and _G_, our HGMEM adopts an adaptive memory-based evidence retrieval strategy for either focused
local investigation or broad global exploration (Section 3.4). To investigate the effects of such
strategy, in Table 2, we compare our strategy to the variants that involve only _Local_ _Investigation_
or _Global Exploration_, represented as “ _w/._ _LI Only_ ” and “ _w/._ _GE Only_ ”, respectively. The results
show that both “ _w/._ _LI Only_ ” and “ _w/._ _GE Only_ ” significantly underperforms the adaptive strategy
across all datasets, demonstrating the effectiveness and necessity of adaptively combining the two
modes of evidence retrieval.


**Effects** **of** **Update** **and** **Merging** **Operations.** The memory evolving in our HGMEM involves
update, insertion and merging operations, where merging is especially critical to building highorder correlations from primitive facts. Because insertion is indispensable, we just carry out ablation
experiments on all datasets using Qwen2.5-32B-Instruct to assess the effects of update and merging
operations, as shown in Table 2. Compared to the “HGMEM”, removing either operation leads
to a performance drop, while removing merging (“ _w/o._ _Merging_ ”) causes a substantially larger
degradation than removing update (“ _w/o._ _Update_ ”). It reflects the effectiveness of both operations,
especially highlighting the importance of high-order correlations built through merging operations.


9


Preprint


Table 3: Average number of entities per hyperedge ( _Avg_ - _Nv_ ) in final memory and prediction accuracy (Acc) for a subset of 120 sampled primitive and sense-making queries.


**NarrativeQA** **Nocha** **Prelude**
**Query Type** **Method**

_**Avg**_ **-** _Nv_ **Acc (%)** _**Avg**_ **-** _Nv_ **Acc (%)** _**Avg**_ **-** _Nv_ **Acc (%)**


HGMEM 3.35 70.00 3.78 60.00 3.85 55.00
Primitive
_w/o._ _Merging_ 3.32 70.00 3.42 65.00 3.73 60.00


HGMEM 7.07 40.00 7.97 70.00 5.25 60.00
Sense-making
_w/o._ _Merging_ 4.10 30.00 3.80 60.00 3.74 55.00


5.4 DISSECTING QUERY RESOLVING: PRIMITIVE VS. SENSE-MAKING


To better understand how our proposed HGMEM brings improvement to the evaluation tasks, we
conduct a targeted analysis across different query types. Specifically, we randomly sample 40
queries from each long narrative understanding dataset used in our experiments, yielding a total
of 120 queries. These are then manually categorized into two representative types:


 - _Primitive Query_ : Queries that primarily require locating directly associated chunks, which can
often be resolved with local evidence and focus on straightforward factual information.


 - _Sense-making_ _Query_ : Queries that require deeper comprehension by connecting and integrating multiple pieces of evidence, emphasizing the construction of higher-order relationships and
interpretation beyond surface retrieval.


We compare both prediction accuracy and the average number of entities per hyperedge ( _Avg_ - _Nv_ )
in memory before generating final responses. The latter serves as a quantitative indicator of relationship complexity. Table 3 shows that on _sense-making_ _queries_, our full “HGMEM” achieves
higher accuracy with considerably larger _Avg_ - _Nv_ than “HGMEM _w/o._ _Merging_ ”, demonstrating
that forming higher-order correlations enhances comprehension. In contrast, for primitive queries,
“HGMEM” yields comparable or slightly lower accuracy relative to “HGMEM _w/o._ _Merging_ ”. This
is likely because the full model still tends to associate additional pieces of relevant evidence (as
indicated by the slightly higher _Avg_ - _Nv_ ), even though the primitive evidence alone is sufficient to
answer straightforward queries, resulting in redundancy.


Notably, the _Avg_ - _Nv_ on sense-making queries consistently exceeds that on primitive queries, especially when merging is applied. Taken together, these results indicate that HGMEM improves
contextual understanding by constructing high-order correlations for complex relational reasoning,
rather than relying on shallow accumulation of surface facts.


6 CONCLUSION


In this work, we propose HGMEM, the hypergraph-based memory mechanism that aims at improving multi-step RAG by enabling the evolving of memory into more sophisticated forms for complex
relational modeling. In HGMEM, the memory is structured as a hypergraph composed of a set
of hyperedges as separate memory points. HGMEM allows the memory to progressively establish high-order correlations among previously accumulated primitive facts during the execution of
multi-step RAG systems, guiding LLMs to organize and connect thoughts for a focal problem. Extensive experiments and in-depth analysis validate the effectiveness of our method over strong RAG
baselines on challenging datasets featuring global sense-making questions over long context.


7 REPRODUCIBILITY STATEMENT


To ensure reproducibility, we introduce the usage and statistics of our used datasets in Section 4.1
and Appendix A. We also give the implementation details about the offline graph construction, system deployment and configuration in Section 4.2. Appendix D gives the prompts for updating,
inserting and merging memory points for memory evolving during multi-step RAG execution. Appendix E describes the procedures for subquery generation with detailed prompts. Appendix F gives
the evaluation prompts for scoring model responses in the generative sense-making QA task.


10


Preprint


REFERENCES


Yushi Bai, Shangqing Tu, Jiajie Zhang, Hao Peng, Xiaozhi Wang, Xin Lv, Shulin Cao, Jiazheng
Xu, Lei Hou, Yuxiao Dong, Jie Tang, and Juanzi Li. Longbench v2: Towards deeper understanding and reasoning on realistic long-context multitasks. In _Proceedings_ _of_ _Association_ _for_
_Computational Linguistics_, pp. 3639–3664, 2025.


Jannis Bulian, Christian Buck, Wojciech Gajewski, Benjamin B¨orschinger, and Tal Schuster.
Tomayto, tomahto. beyond token-level answer equivalence for question answering evaluation.
_CoRR_, abs/2202.07654, 2022.


Howard Chen, Ramakanth Pasunuru, Jason Weston, and Asli Celikyilmaz. Walking down the memory maze: Beyond context limit through interactive reading. _CoRR_, abs/2310.05029, 2023.


Jianlv Chen, Shitao Xiao, Peitian Zhang, Kun Luo, Defu Lian, and Zheng Liu. BGE m3-embedding:
Multi-lingual, multi-functionality, multi-granularity text embeddings through self-knowledge distillation. _CoRR_, abs/2402.03216, 2024.


Mingyue Cheng, Yucong Luo, Jie Ouyang, Qi Liu, Huijie Liu, Li Li, Shuo Yu, Bohou Zhang,
Jiawei Cao, Jie Ma, Daoyu Wang, and Enhong Chen. A survey on knowledge-oriented retrievalaugmented generation. _CoRR_, abs/2503.10677, 2025.


Prateek Chhikara, Dev Khant, Saket Aryan, Taranjeet Singh, and Deshraj Yadav. Mem0: Building
production-ready AI agents with scalable long-term memory. _CoRR_, abs/2504.19413, 2025.


Darren Edge, Ha Trinh, Newman Cheng, Joshua Bradley, Alex Chao, Apurva Mody, Steven Truitt,
and Jonathan Larson. From local to global: A graph RAG approach to query-focused summarization. _CoRR_, abs/2404.16130, 2024.


Masoomali Fatehkia, Ji Kim Lucas, and Sanjay Chawla. T-RAG: lessons from the LLM trenches.
_CoRR_, abs/2402.07483, 2024.


Yifan Feng, Haoxuan You, Zizhao Zhang, Rongrong Ji, and Yue Gao. Hypergraph neural networks.
In _Proceedings of the AAAI Conference on Artificial Intelligence_, pp. 3558–3565, 2019.


Yifan Feng, Hao Hu, Xingliang Hou, Shiquan Liu, Shihui Ying, Shaoyi Du, Han Hu, and Yue
Gao. Hyper-rag: Combating LLM hallucinations using hypergraph-driven retrieval-augmented
generation. _CoRR_, abs/2504.08758, 2025.


Xinyan Guan, Jiali Zeng, Fandong Meng, Chunlei Xin, Yaojie Lu, Hongyu Lin, Xianpei Han,
Le Sun, and Jie Zhou. Deeprag: Thinking to retrieval step by step for large language models.
_CoRR_, abs/2502.01142, 2025.


Zirui Guo, Lianghao Xia, Yanhua Yu, Tu Ao, and Chao Huang. Lightrag: Simple and fast retrievalaugmented generation. _CoRR_, abs/2410.05779, 2024.


Bernal Jimenez Gutierrez, Yiheng Shu, Yu Gu, Michihiro Yasunaga, and Yu Su. Hipporag: Neurobiologically inspired long-term memory for large language models. In _Proceedings of Neural_
_Information Processing Systems_, 2024.


Bernal Jim´enez Guti´errez, Yiheng Shu, Weijian Qi, Sizhe Zhou, and Yu Su. From RAG to memory:
Non-parametric continual learning for large language models. _CoRR_, abs/2502.14802, 2025.


Nicola Jones. Openai’s’ deep research’tool: is it useful for scientists? _Nature_, 2025.


Marzena Karpinska, Katherine Thai, Kyle Lo, Tanya Goyal, and Mohit Iyyer. One thousand and
one pairs: A ”novel” challenge for long-context language models. In _Proceedings of EMNLP_, pp.
17048–17085, 2024.


Tom´as Kocisk´y, Jonathan Schwarz, Phil Blunsom, Chris Dyer, Karl Moritz Hermann, G´abor Melis,
and Edward Grefenstette. The narrativeqa reading comprehension challenge. _Transactions of the_
_Association for Computational Linguistics_, 6:317–328, 2018.


11


Preprint


Woosuk Kwon, Zhuohan Li, Siyuan Zhuang, Ying Sheng, Lianmin Zheng, Cody Hao Yu, Joseph
Gonzalez, Hao Zhang, and Ion Stoica. Efficient memory management for large language model
serving with pagedattention. In _Proceedings of the Symposium on Operating Systems Principles_,
pp. 611–626, 2023.


Kuang-Huei Lee, Xinyun Chen, Hiroki Furuta, John F. Canny, and Ian Fischer. A human-inspired
reading agent with gist memory of very long contexts. In _Proceedings of International Conference_
_on Machine Learning_, 2024.


Guohao Li, Hasan Hammoud, Hani Itani, Dmitrii Khizbullin, and Bernard Ghanem. CAMEL:
communicative agents for ”mind” exploration of large language model society. In _Proceedings of_
_Neural Information Processing Systems_, 2023.


Jiaqi Li, Mengmeng Wang, Zilong Zheng, and Muhan Zhang. Loogle: Can long-context language
models understand long contexts? In _Proceedings of Association for Computational Linguistics_,
pp. 16304–16333, 2024a.


Rui Li, Quanyu Dai, Zeyu Zhang, Xu Chen, Zhenhua Dong, and Ji-Rong Wen. Knowtrace: Bootstrapping iterative retrieval-augmented generation with structured knowledge tracing. _CoRR_,
abs/2505.20245, 2025a.


Rui Li, Zeyu Zhang, Xiaohe Bo, Zihang Tian, Xu Chen, Quanyu Dai, Zhenhua Dong, and Ruiming
Tang. CAM: A constructivist view of agentic memory for llm-based reading comprehension.
_CoRR_, abs/2510.05520, 2025b.


Shilong Li, Yancheng He, Hangyu Guo, Xingyuan Bu, Ge Bai, Jie Liu, Jiaheng Liu, Xingwei Qu,
Yangguang Li, Wanli Ouyang, Wenbo Su, and Bo Zheng. Graphreader: Building graph-based
agent to enhance long-context abilities of large language models. In _Findings of Empirical Meth-_
_ods in Natural Language Processing_, pp. 12758–12786, 2024b.


Yanming Liu, Xinyue Peng, Tianyu Du, Jianwei Yin, Weihao Liu, and Xuhong Zhang. Era-cot:
Improving chain-of-thought through entity relationship analysis. In _Proceedings_ _of_ _Association_
_for Computational Linguistics_, pp. 8780–8794, 2024.


Junru Lu, Siyu An, Mingbao Lin, Gabriele Pergola, Yulan He, Di Yin, Xing Sun, and Yunsheng
Wu. Memochat: Tuning llms to use memos for consistent long-range open-domain conversation.
_CoRR_, abs/2308.08239, 2023.


Haoran Luo, Haihong E, Guanting Chen, Yandan Zheng, Xiaobao Wu, Yikai Guo, Qika Lin,
Yu Feng, Ze-min Kuang, Meina Song, Yifan Zhu, and Luu Anh Tuan. Hypergraphrag:
Retrieval-augmented generation with hypergraph-structured knowledge representation. _CoRR_,
abs/2503.21322, 2025.


Barlas Oguz, Xilun Chen, Vladimir Karpukhin, Stan Peshterliev, Dmytro Okhonko, Michael Sejr
Schlichtkrull, Sonal Gupta, Yashar Mehdad, and Scott Yih. Unik-qa: Unified representations of
structured and unstructured knowledge for open-domain question answering. In _Findings of the_
_Association for Computational Linguistics:_ _NAACL_, pp. 1535–1546, 2022.


Hongjin Qian, Zheng Liu, Peitian Zhang, Kelong Mao, Defu Lian, Zhicheng Dou, and Tiejun
Huang. Memorag: Boosting long context processing with global memory-enhanced retrieval
augmentation. In _Proceedings of WWW 2025_, pp. 2366–2377, 2025.


Parth Sarthi, Salman Abdullah, Aditi Tuli, Shubh Khanna, Anna Goldie, and Christopher D. Manning. RAPTOR: recursive abstractive processing for tree-organized retrieval. In _Proceedings of_
_International Conference on Learning Representations_, 2024.


Zhihong Shao, Yeyun Gong, Yelong Shen, Minlie Huang, Nan Duan, and Weizhu Chen. Enhancing
retrieval-augmented large language models with iterative retrieval-generation synergy. In _Find-_
_ings of EMNLP_, pp. 9248–9274. Association for Computational Linguistics, 2023.


Minjie Shen and Qikai Yang. From mind to machine: The rise of manus AI as a fully autonomous
digital agent. _CoRR_, abs/2505.02024, 2025.


12


Preprint


Wenyu Tao, Xiaofen Xing, Yirong Chen, Linyi Huang, and Xiangmin Xu. Treerag: Unleashing the
power of hierarchical storage for enhanced knowledge retrieval in long documents. In _Findings_
_of the Association for Computational Linguistics_, pp. 356–371, 2025.


Harsh Trivedi, Niranjan Balasubramanian, Tushar Khot, and Ashish Sabharwal. Interleaving retrieval with chain-of-thought reasoning for knowledge-intensive multi-step questions. In _Pro-_
_ceedings of the Association for Computational Linguistics_, pp. 10014–10037, 2023.


Jingjin Wang. Proprag: Guiding retrieval with beam search over proposition paths. _CoRR_,
abs/2504.18070, 2025.


Juyuan Wang, Rongchen Zhao, Wei Wei, Yufeng Wang, Mo Yu, Jie Zhou, Jin Xu, and Liyan Xu.
Comorag: A cognitive-inspired memory-organized RAG for stateful long narrative reasoning.
_CoRR_, abs/2508.10419, 2025.


Yang Wang, Alberto Garcia Hernandez, Roman Kyslyi, and Nicholas Kersting. Evaluating quality of answers for retrieval-augmented generation: A strong LLM is all you need. _CoRR_,
abs/2406.18064, 2024.


Liyan Xu, Jiangnan Li, Mo Yu, and Jie Zhou. Fine-grained modeling of narrative context: A coherence perspective via retrospective questions. In _Proceedings of the Association for Computational_
_Linguistics_, pp. 5822–5838, 2024a.


Wujiang Xu, Zujie Liang, Kai Mei, Hang Gao, Juntao Tan, and Yongfeng Zhang. A-MEM: agentic
memory for LLM agents. _CoRR_, abs/2502.12110, 2025.


Zhe Xu, Jiasheng Ye, Xiangyang Liu, Tianxiang Sun, Xiaoran Liu, Qipeng Guo, Linlin Li, Qun Liu,
Xuanjing Huang, and Xipeng Qiu. Detectiveqa: Evaluating long-context reasoning on detective
novels. _CoRR_, abs/2409.02465, 2024b.


Shunyu Yao, Jeffrey Zhao, Dian Yu, Nan Du, Izhak Shafran, Karthik R. Narasimhan, and Yuan Cao.
React: Synergizing reasoning and acting in language models. In _Proceedings_ _of_ _International_
_Conference on Learning Representations_, 2023.


Howard Yen, Tianyu Gao, Minmin Hou, Ke Ding, Daniel Fleischer, Peter Izsak, Moshe Wasserblat,
and Danqi Chen. HELMET: how to evaluate long-context models effectively and thoroughly. In
_The Thirteenth International Conference on Learning Representations_, 2025.


Mo Yu, Tsz Ting Chung, Chulun Zhou, Tong Li, Rui Lu, Jiangnan Li, Liyan Xu, Haoshu Lu, Ning
Zhang, Jing Li, and Jie Zhou. PRELUDE: A benchmark designed to require global comprehension and reasoning over long contexts. _CoRR_, abs/2508.09848, 2025.


Wanjun Zhong, Lianghong Guo, Qiqi Gao, He Ye, and Yanlin Wang. Memorybank: Enhancing large
language models with long-term memory. In _Proceedings_ _of_ _the_ _AAAI_ _Conference_ _on_ _Artificial_
_Intelligence_, pp. 19724–19731, 2024.


Chulun Zhou, Qiujing Wang, Mo Yu, Xiaoqian Yue, Rui Lu, Jiangnan Li, Yifan Zhou, Shunchi
Zhang, Jie Zhou, and Wai Lam. The essence of contextual understanding in theory of mind: A
study on question answering with story characters. In _Proceedings of the Association for Compu-_
_tational Linguistics_, pp. 22612–22631, 2025.


13


Preprint


Table 4: Statistics of data used in our experiments. #Documents, Avg. #Tokens and #Queries
represent the number of documents, average tokens per document and the total number of queries,
respectively.


**Longbench (Financial)** **Longbench (Governmental)** **Longbench (Legal)** **NarrativeQA** **Nocha** **Prelude**


#Documents 20 22 7 10 4 5
Avg. #Tokens 266k 256k 194k 218k 139k 280k
#Queries 100 98 55 100 126 135


A DATASET STATISTICS


**Generative Sense-making QA.** We retain a portion of long documents with more than 100k tokens from **Longbench** **V2** (Bai et al., 2025), which was originally comprised of six major task
categories designed to assess the ability of LLMs to handle long-context problems. In our experiments, we select three domains of documents from the category of single-document QA, including
_Financial_, _Governmental_ and _Legal_ .


**Long Narrative Understanding.** We use the following public benchmarks:


- **NarrativeQA** (Kocisk´y et al., 2018): It is one of the most widely used benchmarks for story
question answering. Because of its question construction strategy over high-level book summaries,
the task places greater emphasis on synthesis and inference beyond local texts. In contrast, many
other existing long-context QA tasks can often be solved with only local evidence, as shown by
studies in (Yu et al., 2025). For evaluation, we randomly sample 10 long books exceeding 100k
tokens, together with their associated queries, from the complete benchmark.


- **NoCha** (Karpinska et al., 2024): The task involves discriminating minimally different pairs of
true and false claims about English fictional books. Although the format may appear different
from sense-making questions, NoCha is explicitly designed to require constructing a global understanding of the book in relation to the focal statement. Since the official test set is hidden, we
conduct experiments using only the publicly released subset.


- **Prelude** (Yu et al., 2025): This benchmark assesses LLMs’ global comprehension and deep reasoning by requiring them to determine whether a character’s prequel story is consistent with the
original book. Most instances of this task demand integrating multiple pieces of evidence or even
forming a holistic impression of the character’s storyline. In our experiments, we use all English
books included in Prelude for evaluation.


Table 4 gives the detailed statistics about the data used in our experiments, including the number of
documents, average tokens per document and the total number of queries. Generative sense-making
QA task involves documents from Longbench V2 benchmark in _Financial_, _Government_ and _Legal_
domains. Long narrative understanding task uses NarrativeQA, Nocha and Prelude benchmarks.


B COMPARISON BASELINES


In our experiments, we compare our methods to traditional RAG and Multi-step RAG methods.
Traditional RAG includes:


 - **NaiveRAG** just uses the target query to retrieve a set of text chunks from the document for
dealing with queries.


 - **GraphRAG** (Edge et al., 2024) constructs knowledge graph from plain-text documents and build
a hierarchy of communities of closely related entities before using an LLM to make responses.


 - **LightRAG** (Guo et al., 2024) also builds a graph structure and employs a dual-level retrieval
strategy from both low-level and high-level evidence discovery.


 - **HippoRAG v2** (Guti´errez et al., 2025) creates a knowledge graph and adopts the Personalized
PageRank algorithm with dense-sparse integration of passages into the graph search process for
resolving queries.


14


Preprint


Figure 4: The prompt for updating and inserting memory points during memory evolving in HGMEM.


Figure 5: The prompt for merging memory points during memory evolving in HGMEM.


15


Preprint


Table 5: Statistics of the cost of online multi-step RAG execution in our HGMEM and other baselines with working memory. _Avg_ -Token is the average count of tokens processed by LLMs per question, while _Avg_ -Time stands for the average inference latency per question.


**NarrativeQA** **Nocha** **Prelude**
**Method**

_**Avg**_ **-Token** _**Avg**_ **-Time** _**Avg**_ **-Token** _**Avg**_ **-Time** _**Avg**_ **-Token** _**Avg**_ **-Time**


HGMEM 4436.43 15.84 5252.73 18.76 5421.74 19.36
_w/o._ _Merging_ 4154.02 14.84 4750.32 16.97 4897.81 17.49


DeepRAG 3904.18 13.94 4724.07 16.87 4514.66 16.12
ComoRAG 5083.26 18.15 5503.98 19.66 7827.56 27.96


Multi-step RAG includes:


 - **DeepRAG** (Guan et al., 2025) conducts multi-step reasoning as a Markov Decision Process by
iteratively decomposing queries.


 - **ComoRAG** (Wang et al., 2025) undergoes multi-step interactions with external data sources
with a dynamic memory workspace, iteratively generateing probing queries and integrating the
retrieved evidence into a global memory pool.


C COST COMPARISON


We conduct a cost comparison between our HGMem and other baselines with working memory in
terms of token consumption and inference latency. Note that the cost of online multi-step RAG
execution is the real concern for fair comparison because the offline graph construction is just for
building query-agnostic indexing structure. With this focus, we measure the average token consumption and inference latency of HGMEM, ComoRAG and DeepRAG in Table 5. From the statistics,
we can observe that the cost of our HGMem is basically of the same level with those of DeepRAG
and ComoRAG while consistently achieving better performance. We can also see that the merging operation, which is the core operation for forming high-order correlation in our HGMem, just
introduces minor computational overhead.


D PROMPTS FOR MEMORY EVOLVING


Section 3.5 describes the dynamics of memory evolving in HGMEM, which consists of update,
insertion and merging operations. The prompts for these three types of operations are given in
Figure 4 and Figure 5.


E PROMPTS FOR SUBQUERY GENERATION


During our multi-step RAG execution, the LLM needs to generate subqueries for acquiring information from external data sources. First, it raises relevant concerns that either target at specific
memory points or aim at probing useful information outside current memory. Then, the LLM generates corresponding subqueries according to the raised concerns. The prompts for raising concerns
and generating subqueries are given in Figure 6 and Figure 7, respectively.


F EVALUATION PROMPTS FOR GENERATIVE SENSE-MAKING QA


For the evaluation of generative sense-making QA, we leverage GPT-4o as an evaluator to assess the
quality of model responses. Given the target query and the source paragraph from which the query
originated, the GPT-4o evaluator first indicates the level of comprehensiveness/diversity and then
gives a final score within the value range of the corresponding level. Detailed prompts for such LLMas-a-Judge evaluation. Figure 8 and Figure 9 give the prompts for scoring the comprehensiveness
and diversity, respectively.


16


Preprint


You are an intelligent assistant responsible for dealing with the [Main Query] by making appropriate operations as specified.
With respect to the [Main Query], you have consolidated some memory points in your [Memory] describing what you have already known regarding the [Main Query].
Each memory point can be seen as a specific aspect relevant to the [Main Query], providing necessary details or insights from its perspective.


-GoalYour task is to analyze the [Main Query] and [Memory], then determine whether current [Memory] has been sufficient to comprehensively resolve the [Main Query].
If not sufficient, you need to indicate what you want to further investigate.


-ProceduresStep 1.
Make appropriate judgement following the logic branches below.
Case 1: If the [Memory] has been sufficient to completely resolve the [Main Query], output <None> in [Concerns].
Case 2: If the [Memory] is not sufficient, determine current situation should be attributed to which of the following subcases.
Case 2.1: There are some specific memory points which you want to further investigate more details about.
Case 2.2: There are unexplored aspects that go beyond the scope of current [Memory] (i.e. not related to any of the existing memory points).


Step 2.
Output as **Example of Anticipated Output Format**.
Specifically, give your judgement in [Judgement] using corresponding case index (1, 2.1 or 2.2).
Then, generate several concerns that aim at exploring details or aspects not addressed by current [Memory] to better resolve the [Main Query]
When case 2.1, generate up to {num_concerns} concerns, each of which targets at a specific memory point. For each concern, specify the index of its corresponding memory
point.
When case 2.2, generate up to {num_concerns} concerns that probe meaningful information not yet covered by current [Memory]
###########-Example of Anticipated Output Format for Case 1-###########

[Judgement]: 1

[Concerns]: <None>


###########-Example of Anticipated Output Format for Case 2.1-###########

[Judgement]: 2.1

[Concerns]:
0{tuple_delimiter}your_concern_1{record_delimiter}
2{tuple_delimiter}your_concern_2{record_delimiter}
2{tuple_delimiter}your_concern_3{record_delimiter}
{completion_delimiter}


###########-Example of Anticipated Output Format for Case 2.2-###########

[Judgement]: 2.2

[Concerns]:
your_concern_1{record_delimiter}
your_concern_2{record_delimiter}
your_concern_3{record_delimiter}
{completion_delimiter}


######################-Real Data-######################

[Main Query]: {query}


[Memory]:
{memory}
######################

     - Note that:
(1) Your concern should be concise and suggest what further details or aspect you subsequently will seek for.
(2) Only output the judgement, concerns, and the indices of corresponding memory points without any other content.
(3) If current [Memory] has covered most relevant perspectives, generate fewer concerns to avoid redundancy.
(4) Your generated concerns should be separated by "{record_delimiter}".


######################
Output:


Figure 6: The prompt for raising concerns either targeting at specific memory points or probing
useful information outside the current memory.


You are an assistant responsible for dealing with the [Main Query].
Although you have had some relevant information in your [Memory], your current [Memory] is still not sufficient to comprehensively
resolve the [Main Query] due to the concern given in [Concern].
Therefore, you need to generate a subquery that aims at either retrieving more evidences or investigating unexplored aspects in

[Subquery] to better deal with the [Main Query] ultimately.


[Previous Subqueries] records a series of previous subqueries that have been raised before.


###########-Anticipated Output Format-###########

[Subquery]: xxx


######################-Real Data-######################

[Main Query]: {query}


[Memory]:
{memory}


[Concern]:
{concern}


[Previous Subqueries]:
{history_subqueries}


######################

      - Note that:
(1) Your generated subquery should be concise and address the concerns in your [Concern].
(2) You should avoid generating a subquery that is overly similar to any one of the [Previous Subqueries] or [Main Query].
(3) Only output your subquery without any other redundant content such as markup strings.
######################
Output:


Figure 7: The prompt for generating subqueries based on previously raised concerns.


17


Preprint


Given a [Paragraph] and a [Question], you will evaluate the quality of the [Response] in terms of Comprehensiveness.


######################-Real Case-######################

[Paragraph]:{paragraph}

[Question]: {question}

[Response]:{response}


######################-Evaluation Criteria-######################
Comprehensiveness measures whether the [Response] comprehensively covers all key aspects in the [Paragraph] with respect to the

[Question].
Level  | score range | description
Level 1 | 0-20  | The response is extremely one-sided, leaving out key parts or important aspects of the question.
Level 2 | 20-40 | The response has some content, but it misses many important aspects of the question and is not comprehensive enough.
Level 3 | 40-60 | The response is moderately comprehensive, covering the main aspects of the question, but there are still some omissions.
Level 4 | 60-80 | The response is comprehensive, covering most aspects of the question, with few omissions.
Level 5 | 80-100 | The response is extremely comprehensive, covering almost all aspects of the question no omissions, enabling the reader to
gain a complete and thorough understanding.
Evaluate the [Response] using the criteria listed above, give a level of comprehensiveness in [Level] based on the description of the indicator,
then give a score in [Score] based on the corresponding value range, and finally explain in [Explanation].


Note that:
(1) You should reference to the [Paragraph] and avoid misinterpreting any content of [Paragraph] as part of the [Response].
(2) Avoid excessively concerning very specific details. When the response mentions an aspect without providing very specific details, you
should consider this aspect as validly covered, as long as the omitted detail is not crucial to particularly mention with respect to the

[Question] in the whole scope of the response.
(3) If [Response] contains extra content not directly included in the [Paragraph], as long as the extra content is correct, do not consider the
extra content as defects for giving final evaluation.
(4) You should conform to the -Anticipated Output Format- and give your evaluation results in [Your Evaluation].
######################-Anticipated Output Format-######################

[Level]: A level ranging from 1 to 5 # This should be a single number, not a range.

[Score]: A value ranging from 0 to 100 # This should be a single number satisfying the ranging constraint of the corresponding [Level], not a
range.

[Explanation]: xxx

[Your Evaluation]:


Figure 8: The prompt for evaluating the comprehensiveness of a model response.


Given a [Paragraph] and a [Question], you will evaluate the quality of the [Response] in terms of Diversity.


######################-Real Case-######################

[Paragraph]: {paragraph}

[Question]: {question}

[Response]: {response}


######################-Evaluation Criteria-######################
Diversity measures how varied and rich is the response in offering different perspectives and insights related to the question.
Level  | score range | description
Level 1 | 0-20  | The response is extremely narrow and repetitive, providing only a single perspective or insight without exploring alternative
viewpoints or additional information.
Level 2 | 20-40 | The response offers a few different perspectives but remains largely superficial. It may touch on alternative viewpoints but
does not elaborate or provide substantial insights.
Level 3 | 40-60 | The response moderately presents several perspectives with moderate depth. It begins to integrate different viewpoints and
insights but may still miss some important angles or lack thorough exploration.
Level 4 | 60-80 | The response is rich in perspectives and insights. It basically explores multiple viewpoints and provides substantial
evidence and examples to support each angle.
Level 5 | 80-100 | The response is exceptionally varied and rich in perspectives and insights. It offers a comprehensive exploration of the
question, addressing multiple angles with depth and originality.
Evaluate the [Response] using the criteria listed above, give a level of comprehensiveness in [Level] based on the description of the indicator,
then give a score in [Score] based on the corresponding value range, and finally explain in [Explanation].


Note that:
(1) You should reference to the [Paragraph] and avoid misinterpreting any content of [Paragraph] as part of the [Response].
(2) If [Response] contains extra content not directly included in the [Paragraph], as long as the extra content is correct, do not consider the
extra content as defects for giving final evaluation.
(3) You should conform to the -Anticipated Output Format- and give your evaluation results in [Your Evaluation]
######################-Anticipated Output Format-######################

[Level]: A level ranging from 1 to 5 # This should be a single number, not a range.

[Score]: A value ranging from 0 to 100 # This should be a single number satisfying the ranging constraint of the corresponding [Level], not a
range.

[Explanation]: xxx

[Your Evaluation]:


Figure 9: The prompt for evaluating the diversity of a model response.


G CASE STUDY


As shown in Table 6, we present two representative cases highlighting HGMem’s distinct reasoning
advantages over LightRAG from the perspective of forming high-order correlations and the strategy
of adaptive memory-based evidence retrieval during memory evolving.


The first case is from NarrativeQA, where the question requires inferring the underlying cause of Xodar’s enslavement—a relation not explicitly stated in the original text. LightRAG just makes incorrect surface-level predictions based on the retrieved content. While DeepRAG stores the knowledge
in the memory, it does not form high-order correlation and fails to predict correctly. In contrast,


18


Preprint


HGMem progressively evolves its memory and establishes high-order correlations from primitive
evidences accumulated from past interactions, uncovering that Xodar’s punishment originates from
his defeat by Carter.


The second case is from Nocha, where the query mixes factual and misleading details. The LLM
raises a subquery about the source of the name ‘White Sands’. Using the strategy of local investigation, it particularly conducts in-depth inspection about the related memory point (Point 1) in current
memory and verifies that there is no clear evidence showing the name was given by Anne. However,
LightRAG mistakenly recognizes that the name ‘White Sands’ was given by Anne and DeepRAG
doesn’t qualify the correctness of ‘White Sands’.


Together, these examples show that HGMem enables a deeper and more accurate contextual understanding beyond superficial text retrieval.


H A TOY EXAMPLE


To illustrate the core workflow of our method, we present a toy example in Figure 10. Given the
query “Why is Xodar given to Carter as a slave?”, the LLM first retrieves relevant evidence, converting it into a structured representation (corresponding to Point 0 in the figure). It then generates
sub-queries based on current memory to retrieve missing reasoning elements. In the subsequent
iteration, newly retrieved evidence is integrated into the memory storage through update, insertion
and merging operations, yielding a unified representation that includes high-order memory points
capturing complex relationships beyond surface content in original data sources. Finally, the LLM
leverages its evolved memory to produce an answer to the target query. This example illustrates how
the memory evolves during the multi-step RAG execution to iteratively refine its understanding and
support complex relational modeling.


19


Preprint


Table 6: Illustrative Cases on NarrativeQA and Nocha, where red and blue stand for the relevant
answer and its corresponding source, respectively































|Source|NarrativeQA|Nocha|
|---|---|---|
|**Question**|Why is Xodar given to Carter as a slave?|Answer TRUE if the statement is true, otherwise answer FALSE<br>[Statement]: Anne assigns romantic names to her surroundings, like<br>“Lake of Shining Waters” and “White Sands”.<br>[Question]: Based on the context provided, is the above statement<br>TRUE or FALSE?|
|**Golden Answer**|As his punishment for being defeated by Carter previously|False|
|**Relevent Chunks**|**1.** Xodar was brought from the adjoining room. Issus glared at him,<br>a baleful light in her hideous eyes. “And such as you are a Dator of<br>the First Born?” she squealed. “For the disgrace you have brought<br>upon the Immortal Race, you shall be degraded to a rank below<br>the lowest. No longer be you a Dator, but forevermore a slave of<br>slaves....”<br>**2.** ...|**1.** “Oh, I don’t like that name, either. I shall call it—let me<br>see—the Lake of Shining Waters. Yes, that is the right name for<br>it. I know because of the thrill. When I hit on a name that suits<br>exactly, it gives me a thrill. Do things ever give you a thrill?”<br>Matthew ruminated. ...”<br>**2.** said Anne dreamily. “Is it as nice as it sounds? Just when you<br>said ‘shore road’, I saw it in a picture in my mind, as quick as that!<br>And White Sands is a pretty name, too, but I don’t like it as well as<br>Avonlea. Avonlea is a lovely name. It just sounds like music. ...|
|**LightRAG Re-**<br>**trieval&Prediction**|**Prediction**:<br>Xodar is given to Carter as a slave due to his degradation by Issus<br>after falling from favor. Issus degrades Xodar to a rank below the<br>lowest and commands that he serve as a slave to Carter, who previ-<br>ously conquered Xodar in the prison on the Isle of Shador.|**Prediction**:<br>[Answer]: TRUE<br>[Explanation]: The statement is true based on the information pro-<br>vided in the data tables. In the Relationships table, there is a record<br>that indicates Anne of Green Gables gave the romantic name “Lake<br>of Shining Waters” to Barry’s Pond. Additionally, in the Sources<br>table, Anne expresses a preference for the name “Avonlea” over<br>“White Sands”, suggesting she has a fondness for romantic names.|
|**DeepRAG Re-**<br>**trieval&Prediction**|**Generated Subquery:**<br>**1.** What factors infuenced Issus’s decision to demote Xodar from a<br>Dator to a slave?<br>**2.**: What specifc orders or instructions did Issus give to ensure<br>Xodar was transferred to Carter as a slave?<br>**Memory**:<br>**1.** Xodar, originally a member of the First Born, was degraded to<br>a slave status by Issus due to his fall from favor. This demotion<br>signifes...<br>**2.** Issus, in a display of her absolute authority, degrades Xodar to<br>the lowest status of a slave, specifcally instructing him to serve<br>Carter. This act is designed to further demean Xodar and to test<br>Carter’s response.<br>**Prediction**:<br>Xodar is given to Carter as a slave because Issus seeks to degrade<br>and humiliate him. This act undermines Xodar’s former prestige<br>and weakens his infuence, while tying Carter’s treatment and suc-<br>cess to the actions of a once-respected fgure, likely intended to<br>provoke internal confict and dissatisfaction.|**Generated Subqueries:**<br>**1.** Is there evidence in the provided memory or data that Anne has<br>given romantic names to other locations besides Barry’s Pond?<br>**2.** Does the extended info suggest that Anne applies her romantic<br>naming to all her surroundings?<br>**Memory**:<br>**1.** Anne gives the romantic name ”Lake of Shining Waters” to<br>Barry’s Pond, indicating her imaginative and poetic nature towards<br>her surroundings.<br>**2.** Anne fnds Lover’s Lane picturesque and romantic, appreciating<br>its natural beauty and atmosphere for thoughtful refection. This<br>highlights her imaginative and poetic nature towards her surround-<br>ings.<br>**Prediction**:<br>[Answer]: TRUE<br>[Explanation]: The statement is true. There is a record that in-<br>dicates Anne of Green Gables gave the romantic name “Lake of<br>Shining Waters” to Barry’s Pond, indicating her imaginative and<br>poetic nature towards her surroundings.|
|**HGMEM Re-**<br>**trieval&Prediction**|**Generated Subquery:**<br>**1.** What specifc incident of Xodar was considered a disgrace to<br>the Immortal Race, leading directly to his punishment by Issus?<br>_(Global Exploration)_<br>**2.**: What role does Carter have in the decision to give Xodar to him<br>as a slave? _(Global Exploration)_<br>**3.**...<br>**Original Memory**:<br>**Point I**:<br>_Subordinate Entities_: Xodar, Issus, Cowardly injustice<br>_Description_: Xodar is punished by Issus as a form of cowardly<br>injustice for the disgrace he has brought upon the Immortal Race.<br>**Point II**:<br>_Subordinate Entities_: Xodar, Issus, Degradation<br>_Description_: Issus degrades Xodar to a rank below the lowest, Xo-<br>dar is no longer a Dator, but forever a slave of slaves, to fetch and<br>carry for the lower orders that serve in the gardens of Issus.<br>**Memory After Evolving** (Guided by Subquery 1):<br>**Point I** (_Merged_):<br>_Subordinate Entities_: Xodar, Issus, Cowardly injustice, Degradation<br>_Description_: Xodar’s degradation into a slave is a result of his<br>disgraceful defeat by John Carter, which brought shame to the<br>Immortal Race, leading Issus to punish him as a form of cowardly<br>injustice. This refects the societal judgment and loss of honor<br>within the Immortal Race’s culture.<br>**Prediction**:<br>Xodar is given to Carter as a slave due to his disgraceful defeat by<br>John Carter, which brought shame to the Immortal Race. Issus,<br>the goddess, punishes Xodar for his cowardice, degrading him to a<br>slave, and he is subsequently treated as such by Carter.|**Generated Subqueries:**<br>**1.**: Is there any evidence in “Anne of Green Gables” that suggests<br>Anne gave a romantic name to a place known as White Sands?<br>_(Local Investigation)_<br>**2.**: What’s the actual name of White Sands in the book “Anne of<br>Green Gables”? _(Local Investigation)_<br>**3.**...<br>**Original Memory**:<br>**Point I**:<br>_Subordinate Entities_: Diana, Barry’s pond, Lover’s lane, Gilbert,<br>Anne, White sands, Anne of Green Gables<br>_Description_: ... Anne has a habit of giving romantic names to her<br>surroundings, such as calling Barry’s Pond the “Lake of Shining<br>Waters”. While she does romanticize places, there is no specifc<br>mention of her assigning a romantic name to “White Sands”.<br>**Memory after Evolving** (Guided by Subquery 1):<br>**Point I** (_Updated_):<br>_Subordinate Entities_: Diana, Barry’s pond, Lover’s lane, Gilbert,<br>Anne, White sands, Anne of Green Gables<br>_Description_: ...Anne has a habit of giving romantic names to her<br>surroundings, such as calling Barry’s Pond the “Lake of Shining<br>Waters”. However, there is no specifc mention of her assigning a<br>romantic name to “White Sands”. White Sands is instead associated<br>with Gilbert and an educational opportunity offered to Anne by the<br>White Sands trustees.<br>**Prediction**:<br>[Answer]: FALSE<br>[Explanation]: According to the provided information, Anne does<br>give a romantic name to Barry’s Pond, referring to it as the “Lake<br>of Shining Waters”. However, there is no evidence in the memory<br>or data tables that Anne assigns a romantic name to “White Sands”.<br>Instead, White Sands is associated with Gilbert and an educational<br>opportunity for Anne, and it is mentioned as a geographical loca-<br>tion without any indication that Anne romanticizes it. Therefore,<br>the statement is false because it incorrectly includes “White Sands”<br>as one of the locations Anne romanticizes.|


20




Preprint



Retrieve Information

Memory Evolving

Generate Subquery



**Query** : Why is Xodar given to Carter as a slave?















**Response:** Xodar is given to John Carter as a slave by Issus to degrade him further after his defeat and humiliation.
Issus wants to punish Xodar by making him serve the very person who conquered him, marking a drastic change in
Xodar's status from a member of the First Born to a slave.


**Reference Answer:** As his punishment for being defeated by Carter previously


Figure 10: A toy example of HGMem workflow from the NarrativeQA dataset of GPT-4o


21


