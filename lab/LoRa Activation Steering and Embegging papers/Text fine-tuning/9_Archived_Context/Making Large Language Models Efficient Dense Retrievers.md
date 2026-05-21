## **Making Large Language Models Efficient Dense Retrievers**

**Yibin Lei** **[1]** [*] **, Shwai He** **[2]** _[∗]_ **, Ang Li** **[2]** **, Andrew Yates** **[3]**

1University of Amsterdam 2University of Maryland, College Park
3Johns Hopkins University, HLTCOE
y.lei@uva.nl, {shwaihe, angliece}@umd.edu, andrew.yates@jhu.edu


|Col1|Full mo<br>MLP pr<br>Attentio<br>Block p|del<br>uned<br>n pruned<br>runed|Col4|Col5|Col6|Col7|Col8|Col9|
|---|---|---|---|---|---|---|---|---|
||||EffiR-|6M-4.3B|~~Effi~~|~~R-8M-5.7B~~|RepLLa|RepLLa|
||||||||||
||||||EffiR-8B-5.4B||||
|||EffiR-3.4B|EffiR-3.4B|EffiR-3.4B|EffiR-3.4B|EffiR-3.4B|EffiR-3.4B|EffiR-3.4B|
||EffiR-24M-|EffiR-20<br>2.9B|M-3.6B|||EffiR-1|~~EffiR-8A-6.~~<br>6A-6.4B|~~EffiR-8A-6.~~<br>6A-6.4B|
|Q|Q|WEN-4B<br>EffiR-16B-3.6B|||||||
||||||||||



500 600 700 800 900 1000
Inference Speed ( s/sample)



**Abstract**


Recent work has shown that directly fine-tuning
large language models (LLMs) for dense retrieval yields strong performance, but their substantial parameter counts make them computationally inefficient. While prior studies have
revealed significant layer redundancy in LLMs
for generative tasks, it remains unclear whether
similar redundancy exists when these models
are adapted for retrieval tasks, which require
encoding entire sequences into fixed representations rather than generating tokens iteratively.
To this end, we conduct a comprehensive analysis of layer redundancy in LLM-based dense
retrievers. We find that, in contrast to generative settings, MLP layers are substantially
more prunable, while attention layers remain
critical for semantic aggregation. Building on
this insight, we propose EffiR, a framework
for developing efficient retrievers that performs
large-scale MLP compression through a coarseto-fine strategy (coarse-grained depth reduction followed by fine-grained width reduction),
combined with retrieval-specific fine-tuning.
Across diverse BEIR datasets and LLM backbones, EffiR achieves substantial reductions in
model size and inference cost while preserving
the performance of full-size models. [1]


**1** **Introduction**


Dense retrieval models (Karpukhin et al., 2020;
Xiong et al., 2021; Hofstätter et al., 2021; Izacard et al., 2022; Ma et al., 2024) map queries and
documents into a shared dense vector space, enabling efficient similarity-based search. Compared
to traditional sparse methods like BM25 (Robertson et al., 1995), dense retrievers offer stronger
semantic matching capabilities and have shown superior performance across a variety of information
retrieval benchmarks (Bajaj et al., 2018; Thakur
et al., 2021; Muennighoff et al., 2023).


*Equal contribution
[1Our code and models are available at https://github.](https://github.com/Yibin-Lei/EffiR)
[com/Yibin-Lei/EffiR.](https://github.com/Yibin-Lei/EffiR)



Figure 1: Effectiveness–efficiency trade-off in LLMbased dense retrievers. Each point shows a model’s
BEIR performance vs. inference speed. All models
are fine-tuned on MS MARCO. Marker types indicate
compression strategies. EffiR builds efficient models
based on Mistral-7B. For example, EffiR-20M-3.6B applies our EffiR method by dropping 20 MLP layers from
Mistral-7B, then fine-tuning the remaining 3.6B parameters. MLP-pruned models (green squares) consistently
lie near the Pareto frontier (dashed), showing strong
efficiency with minimal accuracy loss.


Large language models (LLMs) have recently
emerged as powerful backbones for dense retrieval, producing high-quality text embeddings
with strong generalization (Ma et al., 2024), multilingual capabilities (Li et al., 2024), and data
efficiency (Luo et al., 2024). They also reduce reliance on large-scale retrieval-oriented pretraining (Wang et al., 2024) and exhibit strong
instruction-following abilities (Sun et al., 2024b).
However, these benefits come with a significant
computational cost: these models typically rely on
large models with billions of parameters, making
them impractical for real-time deployment.


Recent research shows that LLMs exhibit considerable layer redundancy in _generative tasks_, where
attention layers are prunable while MLP layers remain critical, enabling the removal of a substantial
portion of layers with negligible degradation in performance (Gromov et al., 2024; He et al., 2024,
2025). However, despite these findings, dense



57


56


55


54


53


52


51









Mistral-7B



1


retrievers are still typically built by directly finetuning full LLM architectures without leveraging
layer redundancy (Wang et al., 2024; Ma et al.,
2024), limiting their efficiency and practicality.
Moreover, dense retrievers serve a fundamentally
different purpose from the pretraining objective of
LLMs: instead of predicting the next token iteratively, they aim to produce a single, semantically
meaningful representation for the entire input sequence. This distinction motivates examining: **(i)**
**Do the architectures of foundation models also**
**exhibit layer redundancy in retrieval tasks?** **(ii)**
**If so, how does this redundancy differ from that**
**of** **generative** **tasks?** **(iii)** **How** **can** **this** **redun-**
**dancy be exploited to develop more efficient re-**
**trieval models?**
To investigate these questions, we conduct a systematic analysis of layer redundancy across multiple LLM backbones, considering two settings: directly pruning off-the-shelf retrievers and pruning
followed by contrastive fine-tuning. We investigate
how model performance changes when different
layers are dropped, following layer-dropping techniques from prior work (He et al., 2024, 2025).
Interestingly, in contrast to findings in generative
settings, we find that MLP layers, often viewed as
repositories of factual knowledge (Zhu et al., 2020;
Meng et al., 2022), are more amenable to pruning
in retrieval models. Conversely, attention layers
exhibit less redundancy and cannot be removed
as aggressively as in generative models (He et al.,
2024; Siddiqui et al., 2024), as they play a crucial role in aggregating contextual information for
fine-grained semantic matching. Nonetheless, even
with the higher redundancy of MLP layers, aggressive coarse-grained layer dropping alone leads to
notable performance degradation beyond a certain
compression ratio.
Motivated by the above findings, and given the
substantial memory and computational overhead
of MLP layers in retrieval scenarios, where autoregressive decoding and key-value caching are not
applicable, we propose **Effi** cient **R** etriever ( **EffiR** ),
a framework that performs large-scale retrievaloriented MLP compression through a coarse-tofine-grained strategy, followed by retrieval-specific
fine-tuning. EffiR employs two complementary
compression stages: (i) _coarse-grained_ _depth_ _re-_
_duction_, which removes entire low-importance
MLP layers, and (ii) _fine-grained width reduction_,
which adaptively compresses the intermediate dimensions of the retained MLP layers. As shown



in Figure 1, MLP-pruned models (e.g., EffiR-16M4.3B) consistently lie on or near the Pareto frontier,
demonstrating that substantial MLP compression
can significantly improve efficiency with minimal
performance degradation for retrieval. Notably,
EffiR-3.4B, which applies our full coarse-to-fine
framework, achieves higher BEIR performance
than EffiR-20M-3.6B, which uses only coarsegrained layer dropping, despite having a smaller
parameter count. This illustrates the advantage
of combining coarse-grained depth reduction with
fine-grained width compression, allowing us to retain key representational capacity while reducing
redundancy more effectively than coarse methods
alone. Further experiments demonstrate that our
coarse-to-fine framework generalizes beyond Mistral and that EffiR is competitive with widely used
pruning methods while pruning only MLP layers
and providing substantial speedups through structural pruning.


**2** **Related Works**


**Dense** **Retrievers.** Early dense retrievers
fine-tuned pre-trained language models (e.g.,
BERT (Devlin et al., 2019)) directly for retrieval
tasks (Karpukhin et al., 2020; Izacard et al.,
2022; Lei et al., 2023), leading to a range of
methods that incorporate advanced techniques
like hard negative mining (Xiong et al., 2021;
Wang et al., 2022; Hofstätter et al., 2021). More
recently, LLMs have been adapted for dense
retrieval (Ma et al., 2024; Weller et al., 2025;
Wang et al., 2024), offering strong generalization,
multilingual abilities, and less reliance on domainspecific supervision. However, these benefits
come at the cost of significant computational
overhead. Prior work has explored improving
retrieval efficiency by reducing embedding
dimensionality (Kusupati et al., 2024; Lei et al.,
2025) or by accelerating similarity search using
approximate nearest neighbor techniques (Kumar
et al., 2024; Bruch et al., 2024), but the encoding
step, often the main computational bottleneck, has
received comparatively less attention. Beyond
reducing embedding dimensionality alone (as in
Matryoshka-style representations (Kusupati et al.,
2024)), more recent 2D Matryoshka approaches
train models that allow reducing both model layers
and embedding dimensions, enabling further
flexible effectiveness-efficiency trade-offs during
encoding (Zhuang et al., 2025; LI et al., 2025).



2


Recently, DRAMA (Ma et al., 2025) developed
small dense retrievers from LLMs through a
complex three-stage data augmentation pipeline
(producing over 50 million synthetic training
samples) combined with pruning across all model
components, including both attention and MLP
layers. In contrast, we discover that pruning MLP
layers alone is sufficient and use this insight to
construct a simple single-stage fine-tuning strategy
using only standard MSMARCO data.


**Redundancy** **in** **LLMs.** While increasing the
depth of large language models significantly enhances their capacity (OpenAI et al., 2024; Gemini,
2024), it also introduces considerable redundancy
across layers. Recent studies have addressed this
by identifying and removing less critical layers.
For example, Gromov et al. (2024) highlights the
limited utility of deeper layers and advocates for
dropping contiguous Transformer blocks. He et al.
(2024) further examines the internal architecture of
Transformer blocks and proposes fine-grained pruning strategies focused on attention layers, resulting
in more effective layer reduction. Despite these
advancements, existing work primarily focuses on
generative models (Jiang et al., 2023; Grattafiori
et al., 2024) that perform token-level generation.
In contrast, our work focuses on embedding models (Chen et al., 2024; Wang et al., 2022) that operate at the sequence level to produce fixed-length
representations, and holistically investigates how
redundancy manifests in this setting, offering new
insights beyond the generative paradigm.


**3** **How Retrieval Models are Different**


LLMs have shown promising performance in dense
retrieval due to their ability to learn effective embedding representations. However, despite sharing
the same underlying architectures, language modeling and dense retrieval serve distinct purposes. This
section delineates these differences to motivate a
distinct analysis of redundancy in dense retrievers.


**Training Objectives.** Dense retrievers and language models differ fundamentally in their training
objectives. Language models are typically optimized with token-level predictive losses. For instance, causal language models adopt an autoregressive objective:



where the model predicts each token _xt_ conditioned on its leftward context _x<t_ . In contrast,
dense retrievers are trained to produce semantically meaningful representations. A common approach is to optimize a _contrastive loss_ that brings
matched pairs (e.g., a query and its relevant document) closer while pushing apart mismatched pairs.
One widely used formulation is the InfoNCE loss:


exp(sim( _q, d_ [+] ) _/τ_ )
_L_ = _−_ log _,_
exp(sim( _q, d_ [+] ) _/τ_ ) + [�] _j_ _[N]_ =1 [exp(][sim][(] _[q, d]_ _j_ _[−]_ [)] _[/τ]_ [)]

(2)
where _q_ and _d_ [+] are the query and its corresponding
positive document, _d_ _[−]_ _j_ [are negative samples,] _[ τ]_ [is a]
temperature parameter, and sim() typically denotes
the similarity function between extracted representations, which is usually cosine similarity or inner
product. These embeddings are usually derived
from the model outputs using mean pooling or by
extracting the hidden state of the last token.


**Divergence** **in** **Inference** **Pattern.** The fundamental difference leads to distinct inference patterns. Specifically, generative models operate autoregressively, where local information from previously generated tokens is often sufficient to predict
the next token. In contrast, dense retrieval models
process the entire input sequence once and require
stronger global semantic aggregation to produce
fixed-length representations. This divergence suggests that attention layers, which aggregate information across tokens, and MLP layers, which perform intra-token transformations, may contribute
differently in the two modeling paradigms.
On the other hand, unlike generative models,
dense retrieval models obtain the representation in
a single forward pass without the autoregressive decoding process, thereby eliminating the additional
memory overhead (e.g., KV cache) associated with
sequential attention computations. Moreover, MLP
layers account for the majority of the parameters
(e.g., 77.8% in Mistral-7B (Jiang et al., 2023)), and
are computationally intensive due to their operations in high-dimensional spaces. This suggests focusing more heavily on the MLP layers to achieve
high compression rates and promote efficiency.


**Motivation.** Despite the functional differences
between generative and dense retrieval models,
mainstream dense retrievers are still typically
derived from general-purpose language models
through post-finetuning, without modifying the underlying architecture. However, these architectures



_L_ LM = _−_



_T_


log _P_ ( _xt_ _| x<t_ ) _,_ (1)

_t_ =1



3


|E5-Mistral<br>#Params|Full-Model<br>7.1B|Drop-8A Drop-16A<br>6.8B 6.4B|Drop-8B Drop-16B<br>5.4B 3.6B|Drop-8M Drop-16M<br>5.7B 4.3B|
|---|---|---|---|---|
|Arguana<br>Climate-FEVER<br>DBPedia<br>FEVER<br>FiQA<br>HotpotQA<br>NFCorpus<br>NQ<br>Quora<br>SCIDOCS<br>SciFact<br>TREC-COVID<br>Touche-2020|61.6<br>37.5<br>48.6<br>88.3<br>57.2<br>75.6<br>38.7<br>67.1<br>89.3<br>16.8<br>76.7<br>86.6<br>23.6|55.3<br>0.1<br>32.8<br>2.2<br>44.8<br>0.6<br>83.8<br>9.5<br>51.8<br>2.4<br>67.5<br>2.8<br>36.1<br>2.6<br>57.0<br>0.4<br>87.1<br>0.6<br>13.0<br>0.1<br>72.2<br>1.5<br>85.2<br>12.6<br>18.8<br>0.0|39.0<br>9.3<br>1.2<br>3.9<br>19.0<br>9.7<br>36.6<br>22.5<br>9.1<br>8.1<br>43.0<br>9.6<br>11.4<br>17.5<br>25.6<br>12.1<br>21.5<br>26.8<br>7.3<br>2.2<br>33.1<br>20.3<br>55.3<br>20.0<br>7.2<br>5.6|59.0<br>8.4<br>39.0<br>9.8<br>44.7<br>15.2<br>89.6<br>56.6<br>53.5<br>14.0<br>75.5<br>18.0<br>37.4<br>18.2<br>66.1<br>26.0<br>89.1<br>66.0<br>15.2<br>5.1<br>74.1<br>30.6<br>80.8<br>45.7<br>19.1<br>7.6|
|Average|59.1|54.3<br>2.7|23.8<br>12.9|57.2<br>24.7|


Table 1: Effectiveness (nDCG@10) and model sizes of E5-Mistral under different coarse-grained layer dropping
strategies. “Full-Model” denotes the unpruned model. “Drop- _k_ A”, “Drop- _k_ B”, and “Drop- _k_ M” indicate pruning
_k_ self-attention layers, transformer blocks, and MLP layers using our coarse-grained layer dropping method,
respectively. **No recovery training is applied.**



are originally pre-trained for generative tasks and
may introduce unnecessary complexity when applied to retrieval-based applications. This motivates us to examine whether general-purpose LLM
architectures are overparameterized for retrieval
and, if so, how their redundancy can be systematically leveraged to develop more efficient dense
retrievers.


**4** **Are LLM-based Retrievers Redundant?**


To examine redundancy in LLM-based dense retrievers, we apply the layer dropping method
from He et al. (2024) that focuses on removing
the whole redundant layers to improve efficiency at
scale. We study this by pruning three components
of LLMs: self-attention layers, MLP layers, and
full transformer blocks. While prior work on generative tasks (He et al., 2024; Siddiqui et al., 2024)
shows attention layers can often be pruned with
little impact, it’s unclear whether the same holds
for embedding-based models like dense retrievers.


**4.1** **Redundancy Analysis via Layer Dropping**


Transformer-based models are stacked by multiple
transformer blocks, each containing an attention
layer and an MLP layer. So a _L_ -layer model has 2 _L_
sub-layers and each sub-layer has a residual connection. For our analysis, we adopt a layer dropping strategy that removes sub-layers with minimal
contribution to embedding quality. This requires estimating the importance of each sub-layer. For the
_l_ -th sub-layer, we compute the importance scores:


_Sl_ = _M_ ( _xl, xl_ +1) _,_ _xl_ +1 = _xl_ + _Fl_ ( _xl_ ) _,_ (3)


where _Fl_ denotes the _l_ -th layer, and _M_ represents
the matching metric, e.g., _l_ 2-norm and cosine similarity. To assess the importance of the _l_ -th layer, we



compare the layer’s output _xl_ +1 with the input _xl_ .
If the input closely matches the full output, it indicates that the incremental contribution of _Fl_ ( _x_ ) is
minimal, suggesting that the layer can be removed
with limited impact on performance. Following
prior work showing the effectiveness of cosine similarity for identifying redundant layers (Gromov
et al., 2024; He et al., 2024), we adopt it as our importance metric, i.e., _M_ ( _x, y_ ) = 1 _−_ Cosine( _x, y_ ).
Given the distinct roles of attention and MLP
layers, where attention layers aggregate contextual
information across tokens, while MLP layers perform intra-token transformations, we treat them as
two separate groups during pruning. Specifically,
we retain only the most important layers within
each group. Let _S_ Attn and _S_ MLP denote the importance scores for the attention and MLP layers,
respectively. The selected sets of layers are defined
as:
_T_ Attn _←_ Argmax( _S_ Attn _, k_ Attn) _,_ (4)


_T_ MLP _←_ Argmax( _S_ MLP _, k_ MLP) _,_ (5)


where _k_ Attn and _k_ MLP denote the numbers of retained attention and MLP layers, respectively. The
sets of selected layers are represented by _T_ Attn and
_T_ MLP, corresponding to the retained attention and
MLP layers, respectively. The operator Argmax selects the top- _k_ most important layers in each group.


**4.2** **Setup**


**Pruning Setup.** Following He et al. (2024), we
compute importance scores for each layer using
256 validation samples from the C4 corpus (Raffel
et al., 2020), which is embedding and task-agnostic.
We then prune the least important modules per category and evaluate the resulting models on 13 BEIR
datasets (Thakur et al., 2021) using nDCG@10.



4


|Mistral-7B<br>#Params|Full-Model<br>7.1B|Drop-8A Drop-16A<br>6.8B 6.4B|Drop-8B Drop-16B Drop-Last16B<br>5.4B 3.6B 3.6B|Drop-8M Drop-16M Drop-20M Drop-24M<br>5.7B 4.3B 3.6B 2.9B|Drop-16M8A<br>4.0B|
|---|---|---|---|---|---|
|Arguana<br>Climate-FEVER<br>DBPedia<br>FEVER<br>FiQA<br>HotpotQA<br>NFCorpus<br>NQ<br>Quora<br>SCIDOCS<br>SciFact<br>TREC-COVID<br>Touche-2020|58.2<br>30.8<br>44.2<br>83.5<br>45.9<br>70.5<br>34.7<br>65.0<br>83.1<br>17.2<br>75.9<br>84.1<br>35.7|56.1<br>47.4<br>29.9<br>29.4<br>40.1<br>42.1<br>79.1<br>77.4<br>45.5<br>43.5<br>68.1<br>66.2<br>31.6<br>34.2<br>64.5<br>62.4<br>83.3<br>87.9<br>14.3<br>17.2<br>73.7<br>76.2<br>83.0<br>86.3<br>30.7<br>28.4|56.0<br>44.|<br>43.0<br>29.4<br>27.1<br>27.9<br>40.2<br>41.5<br>42.0<br>81.9<br>76.3<br>76.5<br>44.8<br>41.8<br>43.9<br>67.9<br>65.1<br>65.4<br>32.5<br>35.3<br>37.8<br>64.4<br>62.5<br>62.4<br>84.2<br>88.2<br>86.8<br>16.0<br>17.3<br>16.6<br>74.9<br>74.0<br>73.7<br>82.8<br>82.2<br>85.6<br>33.0<br>28.3<br>27.1|56.9<br>54.5<br>51.4<br>45.6<br>30.4<br>31.6<br>31.9<br>28.9<br>43.9<br>42.2<br>37.4<br>41.3<br>82.6<br>83.3<br>79.7<br>80.6<br>45.8<br>44.9<br>43.1<br>40.3<br>71.0<br>70.1<br>67.9<br>67.5<br>33.3<br>35.4<br>33.1<br>36.3<br>65.4<br>63.8<br>60.8<br>58.4<br>85.9<br>83.7<br>86.5<br>87.0<br>17.3<br>17.1<br>17.0<br>17.4<br>76.2<br>76.4<br>75.7<br>74.3<br>83.7<br>84.2<br>85.7<br>83.3<br>34.4<br>32.3<br>28.1<br>31.1|53.2<br>27.9<br>39.2<br>79.9<br>43.7<br>67.9<br>33.9<br>61.9<br>84.3<br>16.5<br>75.9<br>85.3<br>28.7|
|Average|56.1|53.8<br>53.7|54.5<br>52.6<br>53.0|55.9<br>55.3<br>53.7<br>53.2|53.7|


Table 2: Effectiveness (nDCG@10) and model sizes of Mistral-7B variants **trained** **using** **MS** **MARCO** after
coarse-grained layer dropping. We compare pruning of MLP layers (e.g., Drop-16M), attention layers (e.g., Drop16A), full transformer blocks (e.g., Drop-16B), and their combinations (e.g., Drop-16M8A). Drop-Last16B denotes
directly dropping the last 16 blocks. **Results for LLaMA3-8B, Qwen-2.5-1.5B, Qwen-2.5-3B, Qwen-2.5-7B, and**
**ModernBERT-base are provided in Appendices A.4.**



We also report parameter counts for each variant [2] .
We consider two settings: (i) directly pruning offthe-shelf retrievers and (ii) pruning base models
followed by contrastive fine-tuning.


**Dense** **Retriever** **Training** **Setup.** After compressing the base model, we fine-tune it for retrieval
tasks. Following prior work (Wang et al., 2024; Ma
et al., 2024), we append a special <eos> token to
each input text and use the hidden state of the final token as the text representation. We train all
dense retrievers using the InfoNCE loss defined in
Equation 2, with the temperature hyperparameter
set to 0.02, and additionally apply a distillation
loss. All models are trained on MSMARCO data
under identical settings to ensure fair comparison.
Detailed training configurations are provided in
Appendix A.2.


**4.3** **Layer Redundancy Results**


**4.3.1** **Pruning Off-the-Shelf Retrievers**


Table 1 presents the results of directly pruning the
off-the-shelf E5-Mistral model without any retraining. The results reveal several notable trends about
redundancy in LLM-based dense retrievers. Unlike in generation tasks, where attention layers are
typically more redundant, we find that pruning attention layers leads to a drastic collapse in performance, with dropping 16 attention layers nearly
zeroing out retrieval scores across several datasets.
This suggests that attention remains structurally vital for producing semantically rich embeddings.
However, pruning MLP layers leads to a more
graceful degradation: while performance drops are


2In the paper, we exclude the language modeling head
when reporting parameter counts, since text encoding does not
require it.



still noticeable, MLP-8 and MLP-16 retain moderate effectiveness on many datasets and yield significant parameter reductions. Interestingly, MLP
pruning outperforms block-level pruning despite
retaining less parameters (Drop-16M vs. Drop-8B),
suggesting that MLPs offer a more efficient compression axis for dense retrievers.


**4.3.2** **Pruning Followed by Fine-tuning**


To ensure a comprehensive examination, we also
investigate an alternative setup: pruning the base
model first, followed by contrastive fine-tuning.
The training settings are detailed in Section 4.2.

As shown in Table 2, MLP layers exhibit the
most redundancy. Dropping 16 MLP layers (EffiR16M) removes over 35% of parameters with minimal performance loss (55.3 vs. 56.1). However,
more aggressive pruning (EffiR-20M, EffiR-24M)
leads to sharper degradation, highlighting the limitations of depth-only compression and motivating
the width-aware, coarse-to-fine strategy used in
EffiR (Section 5.1).

In contrast, pruning attention layers results in
minimal parameter reduction but significant performance drops (e.g., EffiR-16A drops to 53.7
nDCG@10). Block-level pruning (EffiR-8B) falls
between these extremes: less efficient than targeted
MLP pruning and more stable than attention pruning, but lacking the precision of module-aware compression strategies.

These trends hold consistently across various
models, including LLaMA3-8B, Qwen-2.5-1.5B,
Qwen-2.5-3B, Qwen-2.5-7B and ModernBERTbase (see Appendices A.4), reinforcing our design principles for EffiR: (i) prioritize MLPs as the
primary compression dimension, and (ii) employ
adaptive width-aware self-slimming rather than



5


solely depth pruning to achieve superior efficiencyeffectiveness trade-offs.


**5** **EffiR: Efficient Retriever Training**


While results in Section 4 highlight the significant
redundancy of MLP layers, they also indicate the
limitations of depth-only pruning: removing too
many layers degrades retrieval effectiveness substantially. To overcome this trade-off, we introduce
EffiR (Efficient Retriever Training), a coarse-tofine compression framework designed to explores
redundancy from two complementary perspectives:
**depth** and **width** . Depth reduction (i.e., layer dropping) removes the whole redundant layers to improve efficiency at scale, while width reduction
adaptively compresses the remaining MLP layers
to further enhance compactness while maintaining
model performance.


**5.1** **Width Reduction via Self-Slimming**


In addition to the layer depth, the width of individual layers also contributes to the overall model size.
In particular, the majority of parameters arise from
MLP layers, which are formulated as:


MLP( _x_ ) = _W_ down (Act( _W_ gate _x_ ) _⊙_ _W_ up _x_ ) + _x,_ (6)


where _W_ gate _∈_ **R** _[n][×][d]_ and _W_ down _∈_ **R** _[d][×][n]_ are
the weight matrices of the MLP layer, and Act( _·_ )
denotes an activation function. For simplicity, we
omit the LayerNorm (LN) in the formulation.
The intermediate dimension _n_ is typically much
larger than the hidden size _d_ . For instance, Mistral7B employs an intermediate size of 14,336 in its
MLP layers, more than three times its hidden size
of 4096. While projecting the hidden states into
higher-dimensional spaces enhances the model’s
representational capacity, this architectural choice
substantially increases the parameter count: MLP
layers alone contribute to approximately 80% of
Mistral-7B’s total parameters.
To remedy this problem, we further propose selfslimming for width reduction across all MLP layers.
Specifically, we propose an importance indicator
trainable **z** _∈_ **R** _[n]_ at the intermediate neurons in an
MLP layer. With this indicator, an MLP layer is
reformulated:


MLP( _x_ ) = _W_ down (Relu( **z** ) _·_ Act( _W_ gate _x_ ) _⊙_ ( _W_ up _x_ ))+ _x._
(7)
Here, ReLU( **z** ) serves two purposes. First, it ensures that the importance scores are non-negative,
as negative values could lead to unintended cancellations. Second, it imposes a form of soft masking:



a neuron with ReLU( _zi_ ) _≈_ 0 contributes minimally to the output and is a candidate for pruning.
To ensure compatibility with the original MLP behavior, **z** is initialized as an all-ones vector, **1** _[n]_ .
We then adopt a training-oriented approach to
sparsify **z**, making it trainable only during the selfslimming phase. Specifically, the overall training
objective is defined as:


_L_ = _L_ InfoNCE + _λL_ norm _._ (8)


where _L_ norm is the _ℓ_ 0-norm over ReLU( **z** ), promoting sparsity in the active neurons, and _λ_ is the
corresponding regularization weight. The two loss
terms jointly steer the scaling factors to (i) improve
performance on the downstream retrieval task and
(ii) remain highly sparse.
However, since the _ℓ_ 0-norm is not differentiable
and cannot be optimized directly via gradient-based
methods, we use a sigmoid-based relaxation as a
differentiable surrogate [3] .
After only a few optimisation steps, the model
learns a _slim_ activation pattern in which far fewer
neurons are active. We then perform global pruning
by ranking all scaling factors in Relu( **z** ) across all
MLP layers and freezing the least important values
to 0 while setting the remaining ones to 1. The
resulting binary mask acts as a gating mechanism
for neuron activation. Next, we train this sparsified model with the _L_ InfoNCE objective, under the
normal dense retrieval training setting as described
in Section 4.2. After training, we permanently remove all intermediate dimensions of MLPs whose
corresponding scaling values are 0.


**6** **EffiR: Experimental Results**


In this section, we present comprehensive experiments demonstrating that EffiR enhances the efficiency of LLMs for dense retrieval without compromising retrieval performance.


**6.1** **Experimental Setup**


**Model.** We develop EffiR by applying our coarseto-fine framework to the Mistral-7B-v0.1 model.
In the first stage, we perform _coarse-grained MLP_
_layer_ _dropping_, removing 16 MLP layers identified as least important, following the pruning setup
described in Section 4.2. In the second stage, we
apply our fine-grained _self-slimming_ method to reduce the width of the remaining MLPs by 30%. We


3Details on the relaxation are provided in Appendix A.1.



6


|#Params<br>Query-Speedup<br>Doc-Speedup|RepLLaMA<br>6.6B<br>1.05×<br>0.98×|Mistral-7B* Llama-1B* Gemma-2B* QWEN-4B*<br>7.1B 1.2B 2.6B 3.6B<br>1.00× 6.71× 3.24× 2.22×<br>1.00× 6.91× 3.59× 2.18×|EffiR-8A EffiR-16A EffRi -16M EffiR-20M<br>6.8B 6.4B 4.3B 3.6B<br>1.08× 1.15× 1.64× 1.93×<br>1.08× 1.17× 1.55× 1.80×|EffiR<br>3.4B<br>1.97×<br>1.82×|
|---|---|---|---|---|
|Arguana<br>Climate-FEVER<br>DBPedia<br>FEVER<br>FiQA<br>HotpotQA<br>NFCorpus<br>NQ<br>Quora<br>SCIDOCS<br>SciFact<br>TREC-COVID<br>Touche-2020|48.6<br>31.0<br>43.7<br>83.4<br>45.8<br>68.5<br>37.8<br>62.4<br>86.8<br>18.1<br>75.6<br>84.7<br>30.5|58.2<br>49.7<br>57.5<br>48.6<br>30.8<br>26.4<br>37.7<br>23.4<br>44.2<br>38.2<br>37.7<br>43.1<br>83.5<br>81.8<br>78.3<br>80.2<br>45.9<br>37.8<br>40.6<br>40.1<br>70.5<br>65.2<br>65.7<br>65.0<br>34.7<br>32.3<br>33.7<br>35.6<br>65.0<br>57.8<br>58.7<br>60.4<br>83.1<br>82.4<br>77.7<br>83.3<br>17.2<br>17.0<br>15.4<br>14.3<br>75.9<br>70.4<br>72.4<br>73.7<br>84.1<br>81.7<br>76.9<br>83.0<br>35.7<br>29.3<br>28.3<br>29.1|56.1<br>47.4<br>54.5<br>51.4<br>29.9<br>29.4<br>31.6<br>31.9<br>40.1<br>42.1<br>42.2<br>37.4<br>79.1<br>77.4<br>83.3<br>79.7<br>45.5<br>43.5<br>44.9<br>43.1<br>68.1<br>66.2<br>70.1<br>67.9<br>31.6<br>34.2<br>35.4<br>33.1<br>64.5<br>62.4<br>63.8<br>60.8<br>87.9<br>84.6<br>83.7<br>86.5<br>17.2<br>17.7<br>17.1<br>17.0<br>76.2<br>72.4<br>76.4<br>75.7<br>86.3<br>84.0<br>84.2<br>85.7<br>32.3<br>30.7<br>28.4<br>28.1|52.8<br>30.4<br>43.0<br>82.0<br>42.8<br>67.6<br>35.9<br>60.8<br>83.3<br>17.4<br>75.1<br>83.3<br>31.7|
|Average|55.1|56.1<br>51.5<br>51.5<br>52.6|53.8<br>53.7<br>55.3<br>53.7|54.3|


Table 3: Retrieval performance (nDCG@10), model size, and inference speedup of EffiR and baselines on the
BEIR benchmark. EffiR denotes the model trained using the full coarse-to-fine framework. EffiR-16A and EffiR16M denote variants of EffiR that apply only coarse-grained pruning by dropping 16 attention and MLP layers,
respectively, prior to training. [*] Mistral-7B, Llama-1B, Gemma-2B, and QWEN-4B are trained with the same
retrieval supervision with no compression applied.



also examine the generalizability of EffiR under different ratios and across alternative LLM backbones
in Section 7.1.


**Evaluation.** In line with the evaluation in Section 4, we evaluate all models on the BEIR benchmark, using nDCG@10 as the metric. To assess
efficiency, we measure both the total parameter
count and **inference speedup relative to the full**
**Mistral-7B** **model** . Inference speedup is measured separately for query and document encoding using 1,000 randomly sampled inputs from the
NQ dataset, executed on a single H100 GPU using the HuggingFace Transformers library, with
torch.compile applied to the models.


**Baselines.** We compare EffiR against RepLLAMA (Ma et al., 2024), a strong LLMbased dense retriever trained on the MS MARCO
dataset (Bajaj et al., 2018), the same dataset used
to train our models. To isolate the effectiveness of
our training framework, we also evaluate a set of
small LLMs with similar release periods to Mistral7B, trained under identical setups. These include
LLaMA-3.2-1B (Grattafiori et al., 2024), Gemma2-2B (Team et al., 2024), and Qwen-1.5-4B (Bai
et al., 2023) models. All baselines are trained using
the identical configurations as described in Section 4.2. In addition, we report results for layer
dropping variants in which only coarse-grained
layer dropping is applied prior to training.


**6.2** **Main Results**


As shown in Table 3, EffiR achieves strong retrieval performance while significantly reducing
model size and inference cost. With an average
nDCG@10 of 54.3 across the BEIR benchmark, Ef


fiR closely matches the original Mistral-7B model
(56.1), despite using only ~48% of its parameters
and achieving a 1.97 _×_ query-side speedup. EffiR
also consistently outperforms similarly sized small
LLMs such as LLaMA-1B, Gemma-2B, and Qwen4B, though trained under the same retrieval supervision. This highlights the strength of our framework:
rather than relying on compact pretrained small
models with limited capacity, EffiR starts from a
larger model and applies retriever-aware compression that preserves capacity in critical components
while eliminating redundant computation.
In addition to outperforming general small
models, EffiR improves over intermediate coarsegrained pruned variants like EffiR-16M and EffiR20M, suggesting that our combined approach of
coarse-grained layer dropping followed by finegrained slimming is more effective than only using the coarse-grained method. This confirms the
importance of designing compression methods tailored to the retriever’s architectural priorities.


**7** **Analysis**


**7.1** **Width Reduction vs.** **Layer Dropping**


To analyze the impact of different compression
stages, we compare coarse-grained MLP layer dropping with the fine-grained self-slimming method
(Figure 3), starting from the same base: dropping
16 MLP layers from the Mistral model, a strong
initial trade-off.
From this point, we explore two paths: (1) dropping additional layers (EffiR-20M, EffiR-24M),
and (2) applying self-slimming to progressively
reduce MLP width by various sparsity ratios.
The trade-off is clear: further depth pruning re


7


0


8


16


24


32



Mistral


0 8 16 24
Layer Index



0


8


16


24


32



E5-Mistral


0 8 16 24
Layer Index



1.4

1.3

1.2

1.1

1.0

0.9

0.8

0.7

0.6



0 2 4 6 8 10 12 14
Layer Index





(a) MLP Layer Dropping Heat Maps



(b) Layer-wise hidden dimension counts after width
reduction under different reduction ratios.



Figure 2: Analyzing compression behavior across layers.



56.0

55.5

55.0

54.5

54.0

53.5

53.0


|arse-Grained Layer-Dropping<br>e-grained Self-Slimming|MLP-16|
|---|---|
|<br>~~20% sparsity~~<br>1|% sparsity|
|~~30% sparsity~~||
|~~MLP-20~~||
|~~4~~||


|Col1|Coarse-Grained Layer-Dropping|Col3|
|---|---|---|
||<br> <br>Fine-grained Self-Slimming|**MLP-16**|
|~~3~~|~~0% sparsity~~<br>20% sparsity||
||||
||||
|MLP|-20||
||||



3B 3.5B 4B 4.5B
#Params





54

53

52

51

50

49

48











Figure 3: Comparison of coarse-grained layer dropping
and fine-grained self-slimming, both starting from the
same 16-layer dropped base Mistral-7B model.


duces size but degrades performance, while selfslimming achieves a better efficiency-effectiveness
balance. For example, 30% self-slimming outperforms EffiR-20M with fewer parameters. Results
on Qwen2.5-7B (Figure 4) exhibit the same overall
pattern. These results support the two-stage design
of EffiR: use coarse-grained pruning to reduce redundant depth, then apply fine-grained width reduction for precise, quality-preserving compression.


**7.2** **Which Layers are More Redundant?**


**Layer Dropping.** We visualize the layer-wise redundancy of MLP using dropping-order heat maps
for both Mistral-7B and its retrieval-tuned variant
E5-Mistral, as shown in Figure 2a. Each cell indicates whether a layer is dropped (blue) or retained
(orange) during top- _k_ pruning. Notably, the redundancy patterns remain largely consistent after
retrieval fine-tuning: the E5-Mistral variant shows
similar trends to the base Mistral-7B model. Later
layers are generally more prunable than earlier
ones, highlighting a degree of overparameterization toward the top of the model.


**Self-Slimming** **Width-Reduction.** Figure 2b
presents the results of layer-wise hidden dimension counts under different overall sparsity ratios.
We observe a consistent trend: deeper layers tend



3.0B 3.5B 4.0B
#Params


Figure 4: Comparison of coarse-grained layer dropping
and fine-grained self-slimming, both starting from the
same 16-layer dropped base Qwen2.5-7B model.


to be sparser than shallower layers among the remaining layers. This aligns with our layer-dropping
results, where deeper layers are less important and
are pruned earlier.


**7.3** **Comparison with Pruning Methods**


Method Sparsity Order BEIR Avg.


Finetune-then-Prune 49.8
Wanda 50%
Prune-then-Finetune 54.1


Finetune-then-Prune 50.5
SparseGPT 50%
Prune-then-Finetune 54.7


EffiR 52% Prune-then-Finetune 54.3


Table 4: Comparison with sparsification-based pruning
methods. Note the sparsity of Wanda and SparseGPT
under prune-then-finetune is slightly higher than 50%
since the LoRA introduces additional parameters.


We compare EffiR with Wanda (Sun et al.,
2024a) and SparseGPT (Frantar and Alistarh,
2023), two widely used pruning methods that induce parameter sparsity in both attention and MLP
layers. To ensure a comprehensive comparison, we
evaluate them under both finetune-then-prune and
prune-then-finetune settings, using the same data
as EffiR. Specifically, we use their 2:4 structured
pruning veriants, which prunes at the block level
and can leverage optimized sparse matrix opera


8


tions to achieve real acceleration, achieving 1 _._ 24 _×_
speedup on LLaMA-7B as reported.
As shown in Table 4, under prune-then-finetune,
both Wanda and SparseGPT achieve performance
comparable to EffiR. However, their speedups rely
on sparse-matrix acceleration rather than structural
model changes, and the runtime improvement is
not linear with sparsity (e.g., 50% sparsity yields
only a 1.24 _×_ speedup for LLaMA-7B, as reported
in the Wanda paper). In contrast, EffiR performs
hard pruning that removes entire layers and reduces
hidden dimensions, which produces real reductions
in computation and achieves substantially higher
speedup. Moreover, sparse-matrix acceleration requires specialized kernels and hardware support
and still loads the full parameter set, offering no
memory savings. EffiR avoids these limitations,
making it more practical and deployment-friendly.


Method #Parameters BEIR Avg.


LlaMA2-7B 6.6B 55.7
Sheared-LLaMA2 2.6B 49.6


EffiR-20MLP 3.9B 53.0
_w/ −_ 30% 3.4B 52.5
_w/ −_ 50% 3.1B 49.8
EffiR-24MLP 3.4B 49.7
EffiR-28MLP 2.8B 43.4


Table 5: Comparison with the structural pruning method
Sheared-LLaMA on LLaMA2-7B. Dropping 20 MLP
layers is denoted as -20MLP; _w/_ _−_ 30% indicates reducing the width of the remaining MLP layers by 30%.
EffiR-20MLP _w/ −_ 50% achieves performance similar
to Sheared-LLaMA at comparable model size, despite
pruning only MLPs extremely aggressively (retaining
~19% of MLP parameters).


We further compare EffiR with another SOTA
structural pruning method ShearedLlama (Xia
et al., 2024), which is also used for developing
the Drama model (Ma et al., 2025). For the sake of
computation, we reuse the pruned LLaMA2 checkpoint released by the authors. We apply EffiR directly to the LLaMA2 model. Unlike EffiR, which
prunes only MLP layers, Sheared-LLaMA prunes
all parameters, giving it greater pruning flexibility.
As shown in Table 5, the two-stage design
of EffiR effectively mitigates the severe performance drop that occurs when applying layer dropping alone. At comparable scale, EffiR-20MLP
_w/ −_ 50% (3.1B) achieves performance similar to
Sheared-LLaMA (2.6B), despite restricting pruning to MLP layers only and using 10x less data for
pruning-specific training. Notably, EffiR-20MLP
_w/ −_ 50% retains just ~19% of the original MLP pa


rameters, directly highlighting that a large fraction
of MLP capacity is redundant for retrieval.
This comparison also underscores the value of
focusing on MLPs for retrieval. Sheared-LLaMA
uses a pruning pipeline that compresses both attention and MLPs, yet the gap to MLP-only pruning with EffiR is small. We also emphasize that
Sheared-LLaMA’s pruning pipeline requires 0.4
billion training tokens from diverse domains. In
contrast, EffiR achieves competitive performance
using fewer tokens (~0.03 billion). Thus, even if
Sheared-LLaMA is slightly smaller in total parameters, EffiR offers a simpler alternative that isolates
where the redundancy lies and recovers most of the
benefit at a lower pruning cost.


**7.3.1** **EffiR with Quantization**


We apply bitsandbytes NF4 quantization (with double quantization applied) (Dettmers et al., 2023) to
both the full Mistral model and the EffiR-pruned
models. The results in Table 6 show that quantization behaves similarly for both the unmodified
model and the EffiR-pruned model. In particular,
training with EffiR does not degrade quantization
performance, and in practice leads to substantial
size reductions with minimal loss in effectiveness.
This highlights the practical usefulness of EffiR as
a technique that can be combined with quantization
for even greater efficiency.


Method Precision Size BEIR Avg.


16bit 14.0 GB 56.1
Full-Mistral-Model
4bit 4.3 GB 56.0


16bit 11.4 GB 55.9
EffiR-Mistral-8MLP
4bit 3.7 GB 55.7


16bit 8.7 GB 55.3
EffiR-Mistral-16MLP
4bit 3.0 GB 55.3


Table 6: EffiR with quantization applied.


**8** **Conclusion**


In this work, we investigate the redundancy of
LLMs as retrievers and examine the traditional
pipeline for developing dense retrievers. Specifically, we reveal the parameter redundancy inherent in directly fine-tuning base models for retrieval
tasks. To address this, we propose EffiR, a twostage framework that compresses models in depth
and width, followed by fine-tuning for retrieval
tasks. EffiR offers a general framework for developing retrieval models and provides valuable
insights into efficient retriever design.



9


**Limitations**


We acknowledge the following limitations: (i)
English-centric evaluation: EffiR is evaluated primarily on standard English retrieval benchmarks.
Its effectiveness in multilingual or low-resource retrieval settings remains unexplored and may require
further adaptation. (ii) Inference cost: Although EffiR enables the development of efficient retrievers
that preserve performance while reducing model
size, the resulting EffiR models remain slower at
inference compared to smaller architectures such
as BERT-base.


**References**


Jinze Bai, Shuai Bai, Yunfei Chu, Zeyu Cui, Kai Dang,
and 1 others. 2023. Qwen [technical](https://arxiv.org/abs/2309.16609) report. _arXiv_
_preprint arXiv:2309.16609_ .


Payal Bajaj, Daniel Campos, Nick Craswell, Li Deng,
Jianfeng Gao, Xiaodong Liu, Rangan Majumder, Andrew McNamara, Bhaskar Mitra, Tri Nguyen, Mir
Rosenberg, Xia Song, Alina Stoica, Saurabh Tiwary,
and Tong Wang. 2018. Ms marco: [A human gener-](https://arxiv.org/abs/1611.09268)
[ated machine reading comprehension dataset.](https://arxiv.org/abs/1611.09268) _arXiv_
_preprint arXiv:1611.09268_ .


Sebastian Bruch, Franco Maria Nardini, Cosimo Rulli,
and Rossano Venturini. 2024. [Efficient inverted in-](https://doi.org/10.1145/3626772.3657769)
[dexes for approximate retrieval over learned sparse](https://doi.org/10.1145/3626772.3657769)
[representations.](https://doi.org/10.1145/3626772.3657769) In _Proceedings_ _of_ _the_ _47th_ _Inter-_
_national ACM SIGIR Conference on Research and_
_Development_ _in_ _Information_ _Retrieval_, SIGIR ’24,
page 152–162, New York, NY, USA. Association for
Computing Machinery.


Jianlyu Chen, Shitao Xiao, Peitian Zhang, Kun
Luo, Defu Lian, and Zheng Liu. 2024. [M3-](https://doi.org/10.18653/v1/2024.findings-acl.137)
embedding: [Multi-linguality,](https://doi.org/10.18653/v1/2024.findings-acl.137) multi-functionality,
multi-granularity text [embeddings](https://doi.org/10.18653/v1/2024.findings-acl.137) through selfknowledge distillation. In _Findings_ _of_ _the_ _Asso-_
_ciation_ _for_ _Computational_ _Linguistics:_ _ACL_ _2024_,
pages 2318–2335, Bangkok, Thailand. Association
for Computational Linguistics.


Tim Dettmers, Artidoro Pagnoni, Ari Holtzman, and
Luke Zettlemoyer. 2023. QLoRA: Efficient finetuning of quantized LLMs. In _Thirty-seventh_ _Confer-_
_ence on Neural Information Processing Systems_ .


Jacob Devlin, Ming-Wei Chang, Kenton Lee, and
Kristina Toutanova. 2019. BERT: [Pre-training](https://doi.org/10.18653/v1/N19-1423) of
[deep bidirectional transformers for language under-](https://doi.org/10.18653/v1/N19-1423)
[standing.](https://doi.org/10.18653/v1/N19-1423) In _Proceedings of the 2019 Conference of_
_the North American Chapter of the Association for_
_Computational Linguistics:_ _Human Language Tech-_
_nologies, Volume 1 (Long and Short Papers)_, pages
4171–4186, Minneapolis, Minnesota. Association for
Computational Linguistics.



Elias Frantar and Dan Alistarh. 2023. Sparsegpt: massive language models can be accurately pruned in
one-shot. ICML’23. JMLR.org.


Gemini. 2024. Gemini 1.5: [Unlocking](https://arxiv.org/abs/2403.05530) multimodal
[understanding across millions of tokens of context.](https://arxiv.org/abs/2403.05530)
_Preprint_, arXiv:2403.05530.


Aaron Grattafiori, Abhimanyu Dubey, Abhinav Jauhri,
Abhinav Pandey, Abhishek Kadian, and 1 others.
2024. [The llama 3 herd of models.](https://arxiv.org/abs/2407.21783) _arXiv preprint_
_arXiv:2407.21783_ .


Andrey Gromov, Kushal Tirumala, Hassan Shapourian,
Paolo Glorioso, and Daniel A. Roberts. 2024. [The](https://arxiv.org/abs/2403.17887)
unreasonable [ineffectiveness](https://arxiv.org/abs/2403.17887) of the deeper layers.
_Preprint_, arXiv:2403.17887.


Shwai He, Chaorui Deng, Ang Li, and Shen Yan. 2025.

[Understanding and harnessing sparsity in unified mul-](https://arxiv.org/abs/2512.02351)
[timodal models.](https://arxiv.org/abs/2512.02351) _arXiv preprint arXiv:2512.02351_ .


Shwai He, Guoheng Sun, Zheyu Shen, and Ang Li.
2024. [What matters in transformers?](https://arxiv.org/abs/2406.15786) not all attention
[is needed.](https://arxiv.org/abs/2406.15786) _Preprint_, arXiv:2406.15786.


Sebastian Hofstätter, Sheng-Chieh Lin, Jheng-Hong
Yang, Jimmy Lin, and Allan Hanbury. 2021. [Ef-](https://doi.org/10.1145/3404835.3462891)
ficiently teaching an [effective](https://doi.org/10.1145/3404835.3462891) dense retriever with
balanced topic [aware sampling.](https://doi.org/10.1145/3404835.3462891) In _Proceedings_ _of_
_the_ _44th_ _International_ _ACM_ _SIGIR_ _Conference_ _on_
_Research and Development in Information Retrieval_,
SIGIR ’21, page 113–122, New York, NY, USA. Association for Computing Machinery.


Gautier Izacard, Mathilde Caron, Lucas Hosseini, Sebastian Riedel, Piotr Bojanowski, Armand Joulin, and
Edouard Grave. 2022. [Unsupervised dense informa-](https://openreview.net/forum?id=jKN1pXi7b0)
[tion retrieval with contrastive learning.](https://openreview.net/forum?id=jKN1pXi7b0) _Transactions_
_on Machine Learning Research_ .


Albert Q. Jiang, Alexandre Sablayrolles, Arthur Mensch, Chris Bamford, Devendra Singh Chaplot, Diego
de las Casas, Florian Bressand, Gianna Lengyel, Guillaume Lample, Lucile Saulnier, Lélio Renard Lavaud,
Marie-Anne Lachaux, Pierre Stock, Teven Le Scao,
Thibaut Lavril, Thomas Wang, Timothée Lacroix,
and William El Sayed. 2023. [Mistral 7b.](https://arxiv.org/abs/2310.06825) _Preprint_,
arXiv:2310.06825.


Vladimir Karpukhin, Barlas Oguz, Sewon Min, Patrick
Lewis, Ledell Wu, Sergey Edunov, Danqi Chen, and
Wen-tau Yih. 2020. Dense passage retrieval for opendomain question answering. In _EMNLP_ .


Ramnath Kumar, Anshul Mittal, Nilesh Gupta, Aditya
Kusupati, Inderjit S Dhillon, and Prateek Jain. 2024.
[EHI: End-to-end learning of hierarchical index for](https://openreview.net/forum?id=GeLLOGsHV9)
[efficient dense retrieval.](https://openreview.net/forum?id=GeLLOGsHV9) _Transactions on Machine_
_Learning Research_ .


Aditya Kusupati, Gantavya Bhatt, Aniket Rege,
Matthew Wallingford, Aditya Sinha, Vivek Ramanujan, William Howard-Snyder, Kaifeng Chen,
Sham Kakade, Prateek Jain, and Ali Farhadi. 2024.
Matryoshka [representation](https://arxiv.org/abs/2205.13147) learning. _Preprint_,
arXiv:2205.13147.



10


Yibin Lei, Liang Ding, Yu Cao, Changtong Zan, Andrew Yates, and Dacheng Tao. 2023. [Unsupervised](https://aclanthology.org/2023.findings-acl.695/)
[dense retrieval with relevance-aware contrastive pre-](https://aclanthology.org/2023.findings-acl.695/)
[training.](https://aclanthology.org/2023.findings-acl.695/) In _Findings_ _of_ _the_ _Association_ _for_ _Com-_
_putational_ _Linguistics:_ _ACL_ _2023_ . Association for
Computational Linguistics.


Yibin Lei, Tao Shen, Yu Cao, and Andrew Yates. 2025.

[Enhancing lexicon-based text embeddings with large](https://aclanthology.org/2025.acl-long.930/)
[language](https://aclanthology.org/2025.acl-long.930/) models. In _Proceedings_ _of_ _the_ _63rd_ _An-_
_nual Meeting of the Association for Computational_
_Linguistics (Volume 1:_ _Long Papers)_, pages 18986–
19001, Vienna, Austria. Association for Computational Linguistics.


Chaofan Li, MingHao Qin, Shitao Xiao, Jianlyu Chen,
Kun Luo, Yingxia Shao, Defu Lian, and Zheng Liu.
2024. Making text [embedders](https://arxiv.org/abs/2409.15700) few-shot learners.
_Preprint_, arXiv:2409.15700.


Xianming LI, Zongxi Li, Jing Li, Haoran Xie, and Qing
Li. 2025. [ESE: Espresso sentence embeddings.](https://openreview.net/forum?id=plgLA2YBLH) In
_The Thirteenth International Conference on Learning_
_Representations_ .


Kun Luo, Minghao Qin, Zheng Liu, Shitao Xiao, Jun
Zhao, and Kang Liu. 2024. Large [language](https://doi.org/10.18653/v1/2024.emnlp-main.80) models as foundations for [next-gen](https://doi.org/10.18653/v1/2024.emnlp-main.80) dense retrieval: A
comprehensive [empirical](https://doi.org/10.18653/v1/2024.emnlp-main.80) assessment. In _Proceed-_
_ings of the 2024 Conference on Empirical Methods_
_in Natural Language Processing_, pages 1354–1365,
Miami, Florida, USA. Association for Computational
Linguistics.


Xueguang Ma, Xi Victoria Lin, Barlas Oguz, Jimmy
Lin, Wen-tau Yih, and Xilun Chen. 2025. [DRAMA:](https://aclanthology.org/2025.acl-long.1457/)
[Diverse augmentation from large language models](https://aclanthology.org/2025.acl-long.1457/)
to smaller [dense](https://aclanthology.org/2025.acl-long.1457/) retrievers. In _Proceedings_ _of_ _the_
_63rd Annual Meeting of the Association for Compu-_
_tational Linguistics (Volume 1:_ _Long Papers)_, pages
30170–30186, Vienna, Austria. Association for Computational Linguistics.


Xueguang Ma, Liang Wang, Nan Yang, Furu Wei, and
Jimmy Lin. 2024. [Fine-tuning llama for multi-stage](https://doi.org/10.1145/3626772.3657951)
text [retrieval.](https://doi.org/10.1145/3626772.3657951) In _Proceedings_ _of_ _the_ _47th_ _Interna-_
_tional ACM SIGIR Conference on Research and De-_
_velopment in Information Retrieval_, SIGIR ’24, page
2421–2425, New York, NY, USA. Association for
Computing Machinery.


Kevin Meng, David Bau, Alex Andonian, and Yonatan
Belinkov. 2022. Locating and editing factual associations in gpt. In _Proceedings of the 36th Interna-_
_tional Conference on Neural Information Processing_
_Systems_, NIPS ’22, Red Hook, NY, USA. Curran
Associates Inc.


Niklas Muennighoff, Nouamane Tazi, Loïc Magne, and
Nils Reimers. 2023. Mteb: [Massive text embedding](https://arxiv.org/abs/2210.07316)
[benchmark.](https://arxiv.org/abs/2210.07316) _Preprint_, arXiv:2210.07316.


OpenAI, Josh Achiam, Steven Adler, Sandhini Agarwal,
Lama Ahmad, Ilge Akkaya, Florencia Leoni Aleman, Diogo Almeida, Janko Altenschmidt, Sam Altman, Shyamal Anadkat, Red Avila, Igor Babuschkin,



Suchir Balaji, Valerie Balcom, Paul Baltescu, Haiming Bao, Mohammad Bavarian, Jeff Belgum, and
262 others. 2024. [Gpt-4 technical report.](https://arxiv.org/abs/2303.08774) _Preprint_,
arXiv:2303.08774.


Colin Raffel, Noam Shazeer, Adam Roberts, Katherine
Lee, Sharan Narang, Michael Matena, Yanqi Zhou,
Wei Li, and Peter J. Liu. 2020. Exploring the limits
of transfer learning with a unified text-to-text transformer. _J. Mach. Learn. Res._, 21(1).


Stephen E Robertson, Steve Walker, Susan Jones,
Micheline M Hancock-Beaulieu, Mike Gatford, and
1 others. 1995. Okapi at trec-3. _Nist Special Publica-_
_tion Sp_, 109:109.


Shoaib Ahmed Siddiqui, Xin Dong, Greg Heinrich,
Thomas Breuel, Jan Kautz, David Krueger, and Pavlo
Molchanov. 2024. [A deeper look at depth pruning](https://openreview.net/forum?id=9B7ayWclwN)
[of LLMs.](https://openreview.net/forum?id=9B7ayWclwN) In _ICML 2024 Workshop on Theoretical_
_Foundations of Foundation Models_ .


Mingjie Sun, Zhuang Liu, Anna Bair, and J Zico Kolter.
2024a. [A simple and effective pruning approach for](https://openreview.net/forum?id=PxoFut3dWW)
[large language models.](https://openreview.net/forum?id=PxoFut3dWW) In _The Twelfth International_
_Conference on Learning Representations_ .


Weiwei Sun, Zhengliang Shi, Wu Jiu Long, Lingyong
Yan, Xinyu Ma, Yiding Liu, Min Cao, Dawei Yin,
and Zhaochun Ren. 2024b. [MAIR: A massive bench-](https://doi.org/10.18653/v1/2024.emnlp-main.778)
[mark for evaluating instructed retrieval.](https://doi.org/10.18653/v1/2024.emnlp-main.778) In _Proceed-_
_ings of the 2024 Conference on Empirical Methods in_
_Natural Language Processing_, pages 14044–14067,
Miami, Florida, USA. Association for Computational
Linguistics.


Gemma Team, Morgane Riviere, Shreya Pathak,
Pier Giuseppe Sessa, Cassidy Hardin, and 1 others.
2024. Gemma 2: [Improving open language models](https://arxiv.org/abs/2408.00118)
[at a practical size.](https://arxiv.org/abs/2408.00118) _arXiv preprint arXiv:2408.00118_ .


Nandan Thakur, Nils Reimers, Andreas Sanii, and Iryna
Gurevych. 2021. Beir: A heterogeneous benchmark
for zero-shot evaluation of information retrieval models. In _NeurIPS_ .


Liang Wang, Nan Yang, Xiaolong Huang, Binxing Jiao, Linjun Yang, Daxin Jiang, Rangan Majumder, and Furu Wei. 2022. Text [embeddings](https://api.semanticscholar.org/CorpusID:254366618) by
weakly-supervised [contrastive](https://api.semanticscholar.org/CorpusID:254366618) pre-training. _ArXiv_,
abs/2212.03533.


Liang Wang, Nan Yang, Xiaolong Huang, Linjun Yang,
Rangan Majumder, and Furu Wei. 2024. [Improv-](https://aclanthology.org/2024.acl-long.642/)
[ing text embeddings with large language models.](https://aclanthology.org/2024.acl-long.642/) In
_Proceedings of the 62nd Annual Meeting of the As-_
_sociation for Computational Linguistics (Volume 1:_
_Long Papers)_, pages 11897–11916, Bangkok, Thailand. Association for Computational Linguistics.


Orion Weller, Benjamin Van Durme, Dawn Lawrie, Ashwin Paranjape, Yuhao Zhang, and Jack Hessel. 2025.
Promptriever: [Instruction-trained](https://openreview.net/forum?id=odvSjn416y) retrievers can be
[prompted like language models.](https://openreview.net/forum?id=odvSjn416y) In _The Thirteenth_
_International_ _Conference_ _on_ _Learning_ _Representa-_
_tions_ .



11


Mengzhou Xia, Tianyu Gao, Zhiyuan Zeng, and Danqi
Chen. 2024. Sheared LLaMA: Accelerating lan[guage model pre-training via structured pruning.](https://openreview.net/forum?id=09iOdaeOzp) In
_The_ _Twelfth_ _International_ _Conference_ _on_ _Learning_
_Representations_ .


Lee Xiong, Chenyan Wu, Ye Xiong, Jian Luan, Keith
Rogriguez, Luke Zettlemoyer, and Mingyang Sun.
2021. Approximate nearest neighbor negative contrastive learning for dense text retrieval. In _ICLR_ .


Chen Zhu, Ankit Singh Rawat, Manzil Zaheer, Srinadh
Bhojanapalli, Daliang Li, Felix Yu, and Sanjiv Kumar.
2020. [Modifying memories in transformer models.](https://arxiv.org/abs/2012.00363)
_Preprint_, arXiv:2012.00363.


Shengyao Zhuang, Shuai Wang, Fabio Zheng, Bevan
Koopman, and Guido Zuccon. 2025. [Starbucks-v2:](https://arxiv.org/abs/2410.13230)
Improved training for 2d matryoshka embeddings.
_arXiv preprint arXiv:2410.13230_ .



12


**A** **Appendix**


**A.1** **Sigmoid Surrogate for** _ℓ_ 0 **-norm**


To encourage sparsity during training without enforcing hard thresholding, we adopt a simple and
efficient sigmoid-based surrogate inspired by the
_ℓ_ 0-norm. Specifically, for a set of parameters _{xi}_,
the _ℓ_ 0-norm counts the number of non-zero entries:



_∥_ **x** _∥_ 0 =



_d_


**I** [ _xi_ = 0] _._

_i_ =1



This objective is discontinuous and therefore incompatible with standard gradient-based optimization. We therefore use a differentiable surrogate
based on the sigmoid of the parameter magnitude:



_R_ ˜( **x** ) =



_d_


_σ_ ( _β|xi|_ ) _,_

_i_ =1



where _σ_ ( _·_ ) denotes the sigmoid function and _β_ _>_ 0
controls the sharpness of the transition. Note that
_σ_ (0) = 0 _._ 5, so this surrogate is not a direct approximation of **I** [ _xi_ = 0]; rather, when minimized, it
softly encourages parameters to shrink toward zero
by assigning the lowest penalty to zero-valued entries and increasingly larger penalties to non-zero
magnitudes. Increasing _β_ sharpens the transition
around the origin (i.e., it more strongly separates
small from large magnitudes), but overly large values may harm gradient stability; in practice, we fix
_β_ = 5 _._ 0.


**A.2** **Training Configurations**


We train each model for one epoch using LoRA, applied to the v_proj, q_proj, k_proj, gate_proj,
down_proj, o_proj, up_proj layers, with a rank
of 32 and _α_ = 64. The learning rate is set to 1e4, and each sample consists of one positive and
seven negatives. We also include in-batch negatives and apply the KL-divergence loss to distill
ranking scores from the BGE-reranker. For the selfslimming setup, we fine-tune the scaling factors for
500 steps using full-parameter training and apply
a regularization weight _λ_ of 1e-8. Afterward, we
prune 30% of the intermediate dimensions in the
MLP layers based on their learned scaling factors,
removing the dimensions with the lowest values
across all layers.



**A.3** **BEIR Statisitcs**


We provide the detailed BEIR statistics in Table 7.


Dataset #Test #Corpus


Scifact 300 5,183
Arguana 1,406 8,674
Trec-Covid 50 171,332
FiQA-2018 648 57,638
DBPedia 400 4,635,922
NFCorpus 323 3,633
NQ 3,452 2,681,468
HotpotQA 7,405 5,233,329
Touche-2020 49 382,545
Quora 10,000 522,931
SCIDOCS 1,000 25,657
FEVER 6,666 5,416,568
Climate-FEVER 1,535 5,416,593


Table 7: Dataset Statistics


**A.4** **Additional Layer Dropping Results**


We present the results of coarse-grained layer dropping analysis on the LLaMA3-8B, Qwen-2.5-1.5B,
Qwen-2.5-3B, Qwen-2.5-7B, and ModernBERTbase in Tables 8, 9, 10, 11, and 12, with contrastive
learning applied. Similar to Mistral-7B, dropping
MLP layers results in a smaller performance degradation compared to pruning attention layers or entire transformer blocks across these models.


**A.5** **Results on Retrieval Latency**


We find that different EffiR variants and the original model, which have the same embedding dimension, achieve comparable retrieval latency: ~2.28
ms/query on the NFCorpus dataset using the Faiss
Flat index on a single core of the AMD EPYC 7763
CPU. This indicates that EffiR does not introduce
any retrieval-side overhead.


**A.6** **Results on Embedding Space Alignment**


We compute the embedding-space isotropy values
(based on average pairwise cosine similarity) for
both the original full model and EffiR-20MLP _w/_

_−_ 20% using 10,000 MS MARCO queries. The two
models obtain comparable isotropy scores (0.28 vs.
0.34), suggesting that EffiR largely preserves the
geometric structure of the embedding space.


**A.7** **Dropping-Order Heat Maps**


Figure 5 presents drop-order heat maps visualizing the layer-wise redundancy of attention layers
and Transformer blocks in both Mistral-7B and its
retrieval-tuned variant, E5-Mistral. As with MLP
layers, the later layers tend to be more redundant
and thus more prunable.



13


**A.8** **Why Attention is Critical:** **a Case Study**


We have shown that attention layers are more critical in embedding models than in generative models.
To further explore this, we examine how selectively
dropping MLP or attention layers impacts retrieval
performance.
As shown in Figure 6, models based on lasttoken embeddings (e.g., E5-Mistral (Wang et al.,
2024)) lose the ability to distinguish between positive and negative documents when attention layers
are dropped, whereas those with reduced MLP layers largely retain this capability. We hypothesize
this is because removing attention layers disrupts
the aggregation of contextual information, leading to degraded sequence representations. In contrast, pruning MLP layers preserves the information
flow from context tokens to the final token, thereby
maintaining retrieval effectiveness.
On the other hand, as shown in Figure 7, models using mean-pooling embeddings demonstrate
greater robustness to the removal of attention layers compared to those using last-token-based embeddings. This is likely because the mean-pooled
embedding still aggregates information from all
tokens in the sequence, effectively preserving contextual information.



14


|LLAMA3-8B|Full-Model|EffiR-8A EffiR-16A|EffiR-8B EffiR-16B|EffiR-8M EffiR-16M EffiR-20M EffiR-24M|EffiR-16M8A|
|---|---|---|---|---|---|
|Arguana<br>Climate-FEVER<br>DBPedia<br>FEVER<br>FiQA<br>HotpotQA<br>NFCorpus<br>NQ<br>Quora<br>SCIDOCS<br>SciFact<br>TREC-COVID<br>Touche-2020|48.6<br>31.0<br>43.7<br>83.4<br>45.8<br>68.5<br>37.8<br>62.4<br>86.8<br>18.1<br>75.6<br>84.7<br>30.5|46.5<br>40.2<br>29.1<br>26.5<br>43.0<br>35.0<br>81.7<br>79.1<br>41.9<br>34.9<br>67.5<br>58.5<br>33.8<br>32.0<br>63.9<br>58.1<br>86.5<br>85.9<br>15.8<br>12.7<br>73.3<br>69.0<br>81.1<br>78.9<br>30.3<br>25.4|50.4<br>37.5<br>30.5<br>27.3<br>38.9<br>34.2<br>80.9<br>78.4<br>40.6<br>32.1<br>66.9<br>61.2<br>31.1<br>28.1<br>62.1<br>56.5<br>87.9<br>85.9<br>14.8<br>12.3<br>73.2<br>69.0<br>79.7<br>76.3<br>29.5<br>24.4|51.5<br>52.9<br>42.1<br>42.1<br>29.4<br>28.9<br>29.6<br>21.1<br>43.9<br>43.1<br>43.8<br>33.6<br>83.2<br>83.3<br>84.5<br>68.1<br>42.4<br>41.4<br>39.1<br>31.5<br>70.5<br>68.6<br>67.3<br>57.5<br>35.4<br>34.9<br>35.5<br>30.9<br>63.8<br>62.4<br>61.7<br>49.4<br>87.0<br>87.1<br>86.7<br>83.7<br>17.6<br>15.8<br>16.4<br>15.3<br>74.5<br>72.8<br>73.5<br>64.7<br>82.1<br>83.1<br>81.2<br>75.5<br>32.6<br>31.4<br>31.6<br>26.3|44.5<br>28.8<br>39.1<br>81.2<br>39.1<br>65.3<br>35.1<br>61.0<br>86.8<br>15.8<br>73.8<br>82.9<br>26.6|
|Average|55.5|53.4<br>48.9|52.8<br>47.9|54.9<br>54.3<br>53.3<br>46.1|52.3|


Table 8: Effectiveness (nDCG@10) of LLAMA3-8B variants trained after coarse-grained layer dropping across
different architectural components. We compare pruning of MLP layers (e.g., EffiR-16M), attention layers (e.g.,
EffiR-16A), full transformer blocks (e.g., EffiR-16B), and their combinations (e.g., EffiR-16M8A).

|Qwen2.5-1.5B|Full-Model|EffiR-8A EffiR-16A|EffiR-8M EffiR-16M EffRi -20M|
|---|---|---|---|
|Arguana<br>Climate-FEVER<br>DBPedia<br>FEVER<br>FiQA<br>HotpotQA<br>NFCorpus<br>NQ<br>Quora<br>SCIDOCS<br>SciFact<br>TREC-COVID<br>Touche-2020|53.8<br>26.6<br>42.0<br>78.3<br>38.5<br>64.1<br>35.7<br>57.8<br>86.4<br>17.8<br>73.0<br>82.8<br>30.7|50.5<br>41.5<br>25.5<br>20.3<br>38.4<br>31.3<br>73.0<br>66.2<br>35.0<br>26.2<br>59.8<br>41.8<br>36.1<br>32.1<br>55.1<br>44.8<br>86.9<br>83.6<br>16.9<br>12.9<br>69.3<br>56.5<br>82.7<br>68.7<br>26.3<br>24.6|52.0<br>49.1<br>43.9<br>25.7<br>25.2<br>21.2<br>40.6<br>38.2<br>32.4<br>79.6<br>77.9<br>73.7<br>37.3<br>34.0<br>30.2<br>63.3<br>60.5<br>55.8<br>35.6<br>35.8<br>30.1<br>55.8<br>53.6<br>46.2<br>86.8<br>84.8<br>82.6<br>17.5<br>15.4<br>13.3<br>70.6<br>69.3<br>64.8<br>83.2<br>83.6<br>77.9<br>28.9<br>29.8<br>29.9|
|Average|52.9|50.4<br>42.3|52.1<br>50.6<br>46.3|



Table 9: Effectiveness (nDCG@10) of Qwen2.5-1.5B variants trained after coarse-grained layer dropping across
different architectural components.

|Qwen2.5-3B|Full-Model|EffiR-8A EffiR-16A|EffiR-8M EffiR-16M EffRi -20M|
|---|---|---|---|
|Arguana<br>Climate-FEVER<br>DBPedia<br>FEVER<br>FiQA<br>HotpotQA<br>NFCorpus<br>NQ<br>Quora<br>SCIDOCS<br>SciFact<br>TREC-COVID<br>Touche-2020|53.6<br>25.2<br>42.5<br>82.2<br>41.8<br>66.8<br>36.5<br>61.1<br>88.2<br>16.5<br>74.0<br>84.4<br>34.0|46.5<br>38.3<br>20.9<br>19.3<br>37.2<br>31.2<br>74.0<br>71.7<br>37.4<br>26.6<br>56.9<br>43.8<br>35.6<br>32.9<br>58.3<br>50.4<br>86.5<br>83.6<br>14.5<br>11.1<br>70.3<br>57.1<br>81.9<br>75.1<br>28.7<br>29.5|51.1<br>45.6<br>43.7<br>24.3<br>20.3<br>21.4<br>40.5<br>38.5<br>37.5<br>78.5<br>77.2<br>75.0<br>40.5<br>36.8<br>35.8<br>63.8<br>61.6<br>59.9<br>35.7<br>33.7<br>32.5<br>59.1<br>54.0<br>52.7<br>87.1<br>85.0<br>84.5<br>16.8<br>16.1<br>15.8<br>74.5<br>70.8<br>69.7<br>85.5<br>82.5<br>82.6<br>32.9<br>31.5<br>30.3|
|Average|54.4|49.9<br>43.9|53.1<br>50.3<br>49.3|



Table 10: Effectiveness (nDCG@10) of Qwen2.5-3B variants trained after coarse-grained layer dropping across
different architectural components.

|Qwen2.5-7B|Full-Model|EffiR-8A EffiR-16A|EffiR-8M EffiR-16M EffRi -20M|
|---|---|---|---|
|Arguana<br>Climate-FEVER<br>DBPedia<br>FEVER<br>FiQA<br>HotpotQA<br>NFCorpus<br>NQ<br>Quora<br>SCIDOCS<br>SciFact<br>TREC-COVID<br>Touche-2020|53.1<br>24.2<br>44.2<br>81.8<br>43.9<br>67.9<br>37.1<br>62.8<br>88.6<br>18.1<br>74.1<br>83.7<br>32.7|50.0<br>43.6<br>25.0<br>22.8<br>44.3<br>42.0<br>70.3<br>78.2<br>37.7<br>36.6<br>65.5<br>64.3<br>35.7<br>34.6<br>60.1<br>58.2<br>87.7<br>86.8<br>17.1<br>15.8<br>71.9<br>69.9<br>81.5<br>86.2<br>25.2<br>28.5|51.9<br>48.5<br>45.3<br>26.7<br>25.6<br>21.4<br>44.0<br>42.3<br>36.1<br>82.3<br>81.2<br>76.4<br>40.0<br>38.4<br>31.3<br>67.8<br>65.6<br>60.0<br>37.4<br>36.5<br>32.4<br>61.6<br>57.9<br>51.1<br>87.6<br>87.2<br>78.7<br>17.8<br>18.1<br>15.5<br>74.0<br>73.2<br>69.4<br>83.8<br>84.0<br>77.8<br>32.9<br>31.2<br>33.2|
|Average|54.8|51.7<br>51.3|54.4<br>53.1<br>48.4|



Table 11: Effectiveness (nDCG@10) of Qwen2.5-7B variants trained after coarse-grained layer dropping across
different architectural components.


15


|odernBERT-base|Full-Model|EffiR-8A EffiR-16A Effi|
|---|---|---|
|rguana<br>limate-FEVER<br>BPedia<br>EVER<br>iQA<br>otpotQA<br>FCorpus<br>Q<br>uora<br>CIDOCS<br>ciFact<br>REC-COVID<br>ouche-2020|51.6<br>20.1<br>26.0<br>66.4<br>28.5<br>47.7<br>24.5<br>44.2<br>79.9<br>12.4<br>58.6<br>77.8<br>26.7|44.7<br>0.1<br>8.7<br>0.0<br>12.0<br>0.0<br>52.0<br>0.0<br>11.5<br>0.2<br>23.7<br>0.0<br>22.3<br>0.6<br>35.7<br>0.0<br>69.6<br>0.0<br>2.3<br>0.0<br>48.0<br>0.0<br>67.1<br>0.0<br>25.8<br>0.0|
|verage|43.4|32.6<br>0.1|


Table 12: Effectiveness (nDCG@10) of ModernBERT-base variants trained after coarse-grained layer dropping
across different architectural components.



Mistral

0


8


16


24


32 0 8 16 24

Layer Index



Mistral

0


8


16


24


32 0 8 16 24

Layer Index



Mistral

0


8


16


24


32 0 8 16 24

Layer Index



0


8


16


24


32



E5-Mistral


0 8 16 24
Layer Index



0


8


16


24


32



E5-Mistral


0 8 16 24
Layer Index



0


8


16


24


32



E5-Mistral


0 8 16 24
Layer Index



(a) Block



(b) MLP



(c) Attention



Figure 5: **Dropping-order heat maps** for the base model (Mistral-7B) and its embedding variant (E5-Mistral).



1.0


0.8


0.6


0.4





16 18 20 22 24 26 28 30 32
Layer Index


(c) MLP Drop







**1.0**


**0.8**



1.0


0.9


0.8


0.7


0.6


0.5



16 18 20 22 24 26 28 30 32
Layer Index


(a) Baseline



16 18 20 22 24 26 28 30 32
Layer Index


(b) Attention Drop



Figure 6: Layer-wise query–document similarity for last-token-based retrieval in the original model (a) and
compressed models (b) and (c). The same query is paired with different documents, including a positive and a
negative example.



1.00


0.75


0.50


0.25


0.00



16 18 20 22 24 26 28 30 32
Layer Index


(a) Baseline



16 18 20 22 24 26 28 30 32
Layer Index


(b) Attention Drop



16 18 20 22 24 26 28 30 32
Layer Index


(c) MLP Drop





1.00


0.75


0.50


0.25


0.00





1.00


0.75


0.50


0.25


0.00





Figure 7: Layer-wise query–document similarity for mean-pooling-based retrieval in the original model (a) and
compressed models (b) and (c). The same query is paired with different documents, including a positive and a
negative example.


16


