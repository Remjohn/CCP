## **Fragile Knowledge, Robust Instruction-Following: The** **Width Pruning Dichotomy in Llama-3.2**

**Pere** **Martra** _peremartra@uadla.com_
_Universidad_ _Internacional_ _Menéndez_ _Pelayo_ _(UIMP)_


**Abstract**


Structured width pruning of GLU-MLP layers in Llama-3.2 models, guided by the Maximum Absolute Weight (MAW) criterion, reveals a systematic dichotomy in how reducing the
expansion ratio affects different model capabilities. While performance on tasks relying on
parametric knowledge (e.g., MMLU, GSM8K) and perplexity metrics degrades predictably
with decreasing expansion ratios, instruction-following capabilities improve substantially
(+46% to +75% in IFEval for Llama-3.2-1B and 3B models), and multi-step reasoning
remains robust (MUSR). This pattern, observed consistently across both evaluated model
sizes, challenges the prevailing assumption in compression research that pruning induces
uniform degradation. To investigate this, we evaluated seven expansion ratio configurations using comprehensive benchmark suites that assess factual knowledge, mathematical
reasoning, language comprehension, instruction-following, and truthfulness. Our analysis
identifies the expansion ratio as a critical architectural parameter that selectively modulates cognitive capabilities, rather than merely serving as a compression metric. While prior
work has implicitly suggested this dichotomy in published results, we provide a systematic
characterization of this selective preservation phenomenon. Notably, we document a robust
inverse correlation ( _r_ = _−_ 0 _._ 864, _p_ = 0 _._ 012 in Llama-3B) between factual knowledge capacity
(MMLU) and truthfulness metrics (TruthfulQA-MC2): as knowledge degrades monotonically, the model’s ability to discriminate misconceptions improves consistently. This finding connects two previously distinct research areas—knowledge degradation under pruning
and truthfulness improvement—demonstrating that MAW-guided width pruning acts as a
selective filter, reducing parametric knowledge while preserving or enhancing behavioral
alignment.


**1** **Introduction**


This study investigates the impact of structured width pruning on GLU-MLP layers Guo et al. (2024), using
Llama-3.2 models as case studies. We analyze how the expansion ratio—a key architectural parameter—
serves not only as a compression mechanism but also as an intervention that selectively modulates cognitive
capabilities Sharma et al. (2023).


Building on a prior empirical observation Martra (2024a) that identified a 140% expansion ratio as a
performance equilibrium point, this work provides the first systematic characterization of the underlying
mechanisms. We document two core findings: (1) a "Capability Dichotomy," where MAW pruning degrades parametrized knowledge while preserving or improving instruction-following, and (2) a "Truthfulness
Paradox"—an inverse correlation ( _r_ = _−_ 0 _._ 864) between factual knowledge and misconception discrimination.


Section 1.1 motivates the need for efficient models, Section 1.2 contextualizes width pruning within LLM
optimization techniques, Section 1.3 details our contributions, and Section 1.4 previews key results.


**1.1** **Motivation:** **The** **Need** **for** **Efficient** **Models**


Large language models have demonstrated unprecedented capabilities across a wide range of tasks Zhao
et al. (2025), but their increasing size incurs significant computational and energy costs during both training


1


and inference. Models with tens or hundreds of billions of parameters require specialized infrastructure and
consume substantial resources, which limits their accessibility and sustainability Muralidharan et al. (2024).


Reducing the computational footprint of LLMs is no longer merely an academic goal but a practical necessity
to democratize access, enable deployment on resource-constrained devices (e.g., edge devices), and ensure
long-term economic and environmental viability. This urgent need for efficiency has spurred research into
techniques for improving the efficiency of large language model-based solutions Sun et al. (2024).


Among these techniques, structured pruning—the systematic removal of neural components—has emerged
as a particularly promising approach, traditionally viewed as a compression method Muralidharan et al.
(2024); Xia et al. (2024). However, applying width pruning to GLU layers introduces a fundamental architectural question: Does capacity reduction uniformly degrade all cognitive functions, or can it induce
selective changes?. In this study, we use pruning not only as a compression tool but also as an analytical
lens to explore this question, systematically examining how variations in the expansion ratio reshape the
model’s capability profile.


**1.2** **Width** **Pruning** **in** **the** **Context** **of** **LLM** **Optimization**


Structured pruning is one of several strategies employed by the research community for model optimization.
It complements two other primary approaches: quantization, which reduces the numerical precision of model
weights (e.g., from 16-bit to 4-bit representation), and knowledge distillation, which trains a smaller "student"
model to replicate the behavior of a larger "teacher" model Muralidharan et al. (2024).


Unlike quantization and distillation—methods that operate at the representation and training levels,
respectively—structured pruning directly modifies the model’s architecture by removing entire components.
This approach permanently reduces the parameter count Sun et al. (2024); Xia et al. (2024), enabling both
the elimination of inherent structural redundancies in pre-trained models and the adaptation of generalpurpose models to task-specific deployments. By prioritizing the most relevant capabilities for a given use
case, pruning can optimize models for efficiency without sacrificing critical functionality Reda et al. (2025).


Structured pruning techniques are broadly categorized into depth pruning (removing entire layers) and width
pruning (reducing layer dimensions) Kim et al. (2024); Muralidharan et al. (2024). While depth pruning
represents an aggressive and coarse-grained intervention, width pruning offers finer-grained control, enabling
precise, "surgical" modifications to the model’s behavior at the neuronal level Sharma et al. (2023); Wei
et al. (2024). This study focuses on the systematic application of width pruning to adjust the intermediate
dimension of MLP layers, thereby altering the expansion ratio—a fundamental yet understudied architectural
parameter whose impact on model capabilities remains poorly understood.


**1.3** **Contributions**


This work presents a systematic analysis of the impact of width pruning on GLU architectures, using Llama3.2-1B and 3B models as case studies. Specifically, we examine how variations in the expansion ratio
differentially affect cognitive capabilities in language models. Our main contributions are as follows:


  - **Dichotomy** **of** **capabilities** **under** **the** **MAW** **criterion:** We demonstrate that width pruning
guided by the Maximum Absolute Weight (MAW) criterion affects different task types in fundamentally distinct ways. While capabilities reliant on parametrized knowledge—such as performance
on MMLU, GSM8K, and perplexity—degrade predictably with reductions in the expansion ratio
Muralidharan et al. (2024), instruction-following metrics (IFEval) improve significantly (+46% to
+75%; see Appendix A). This reveals a systematic trade-off between factual memory and behavioral
adherence. Notably, this pattern is consistent across both 1B and 3B models and is specific to the
MAW criterion. Alternative pruning methods, such as Variance of Weights (VOW) and Product of
Norms (PON), do not exhibit this behavior and instead result in catastrophic performance collapse
(see Appendix D).


  - **Truthfulness** **paradox:** We document a robust inverse correlation ( _r_ = _−_ 0 _._ 864 in Llama-3B)
between factual knowledge capacity (MMLU) and truthfulness metrics (TruthfulQA-MC2). This


2


focus on truthfulness—often measured by TruthfulQA—is an active area of research (see section
4.3). This relationship suggests that MAW-guided width pruning selectively reduces the model’s
reliance on memorized misconceptions (see Section 4.3), with direct implications for applications
where minimizing misinformation is prioritized over encyclopedic knowledge retention.


  - **Efficiency** **trade-offs** **by** **inference** **mode:** We quantify the efficiency trade-offs of pruning, which
consistently reduces energy consumption by up to 23% (J/token) but introduces end-to-end latency
penalties that depend on the operational context Gholami & Omar (2023); Muralidharan et al.
(2024). In single-request configurations (B1), we observe latency increases of up to +18%, whereas
batch processing (B8) shows resilient throughput. These findings indicate that pruned configurations
are better optimized for high-concurrency workloads than for interactive applications.


Additionally, we complement this analysis with a detailed characterization of the carbon footprint (see
Appendix C) and an evaluation of instruct-tuned models (see Appendix B). In these evaluations, an expansion
ratio of 2 _._ 4 _×_ emerges as an equilibrium point, balancing competitive capabilities across both model sizes.


**1.4** **Results** **Preview**


Our experiments demonstrate that MAW-guided width pruning in GLU-MLP layers is more than a uniform
compression technique; it is an intervention that selectively reshapes the model’s cognitive capabilities Hou
et al. (2025); Sharma et al. (2023); Wei et al. (2024). The results reveal a systematic dichotomy: while performance on tasks dependent on parameterized factual knowledge—such as MMLU and GSM8K—degrades
predictably as the expansion ratio decreases, instruction-following metrics improve substantially. Specifically,
IFEval scores increase by +46% in Llama-3.2-1B (expansion ratio 2 _._ 4 _×_, 40% pruning) and up to +75% in
Llama-3.2-3B (expansion ratio 1 _._ 6 _×_, 40% pruning) (see Appendix A).


This selective modification is further exemplified by a "truthfulness paradox": we observe a robust inverse
correlation ( _r_ = _−_ 0 _._ 864 in Llama-3B) between factual knowledge (MMLU) and truthfulness (TruthfulQAMC2). This suggests that MAW pruning selectively attenuates reliance on memorized misconceptions while
simultaneously degrading general knowledge retention.


This finding significantly contrasts with the work of Li et al. Li et al. (2025), who report a simultaneous
degradation of MMLU and TruthfulQA when functionally suppressing the ’truthfulness neurons’. This
suggests that our structural pruning (width pruning) modulates truthfulness mechanisms in a fundamentally
different way than functional interventions.


Additionally, our analysis uncovers a critical efficiency trade-off that depends on the inference mode Gholami
& Omar (2023); Muralidharan et al. (2024). Pruning consistently reduces energy consumption (J/token)
but incurs significant end-to-end latency penalties in single-request configurations (B1). However, these
latency costs are substantially mitigated in batch processing scenarios (B8), suggesting that the architectural
bottleneck affecting single-stream generation does not constrain parallel processing capacity.


Finally, our study identifies an expansion ratio of 2 _._ 4 _×_ as an optimal balance point for the evaluated models,
effectively reconciling the competing objectives of capability preservation and efficiency.


**2** **Background** **&** **Related** **Work**


This section establishes the technical foundations for our study. Section 2.1 describes the Gated Linear Unit
(GLU) architecture, a core component of our pruning methodology. Section 2.2 positions our work within
the broader context of structured pruning research.


**2.1** **GLU** **Architecture**


Gated Linear Unit (GLU) layers represent an evolution of the standard Feed-Forward Network (FFN) layers
in transformer models. While a vanilla FFN applies a simple transformation of the form _h_ = _σ_ ( _xW_ 1) _W_ 2,


3


GLU introduces a gating mechanism that modulates information flow through element-wise multiplication
Shazeer (2020).


]


Figure 1: GLU (Gated Linear Unit) architecture within the MLP block of Llama-3.2-1B. The diagram shows
the input flow from `post_attention_layernom`, the parallel `up_proj` and `gate_proj` projections, the SiLU
activation function ( `act_fn` ), the element-wise multiplication (gating), and the final `down_proj` contraction.


As illustrated in Figure 1, the transformation in a GLU layer is defined as:


_h_ = ( _xW_ up _⊙_ SiLU( _xW_ gate)) _W_ down (1)


where:


  - _x ∈_ R _[d]_ [model] is the post-attention input


  - _W_ up _, W_ gate _∈_ R _[d]_ [model] _[×][d]_ [ff] are the parallel expansion projections


  - _W_ down _∈_ R _[d]_ [ff] _[×][d]_ [model] is the contraction projection


  - _⊙_ denotes the element-wise (Hadamard) product


  - SiLU( _x_ ) = _x · σ_ ( _x_ ) is the Sigmoid Linear Unit activation function


The expansion ratio is defined as _r_ = _d_ ff _/d_ model and determines the MLP layer capacity. For Llama-3.2-1B,
_d_ model = 2048 and _d_ ff = 8192, resulting in _r_ = 4 _._ 0 _×_ . For Llama-3.2-3B, _d_ model = 3072 and _d_ ff = 8192, giving
_r_ _≈_ 2 _._ 67 _×_ .


A fundamental characteristic of GLU for structured pruning is that _W_ up and _W_ gate must maintain identical
dimensions due to the gating mechanism Guo et al. (2024). This means that any reduction in _d_ ff must be


4


applied in a paired manner to both projections simultaneously, removing the same neurons in both layers.
This paired pruning constraint is essential to maintain the architectural coherence of the pruned model Guo
et al. (2024).


**2.2** **Related** **Work**


Structured pruning has been explored through various strategies to reduce the size of LLMs while preserving
their performance. These techniques can be broadly classified into two categories: width pruning, which
reduces the dimensionality of layers, and depth pruning, which removes entire layers.


**Width Pruning in LLMs.** Several recent studies address structured pruning at the neuron or channel level.
**SliceGPT** Ashkboos et al. (2024) employs principal component analysis on activation matrices to identify
neurons for removal through channel-wise pruning, applying transformations at the full block level. However,
this activation-based approach exhibits high sensitivity to the calibration data used. **AMP** Mugnaini et al.
(2025) introduces a method that prunes attention heads and MLP neurons simultaneously by projecting
input data onto weights, assessing structural importance through activation magnitudes. Although flexible,
AMP does not systematically explore the effects of varying expansion ratios in MLP layers. As noted
in comprehensive surveys (e.g., Zhao et al., 2025) Zhao et al. (2025), width pruning remains relatively
underexplored compared to techniques like quantization or knowledge distillation, particularly in the context
of systematic architectural analysis.


**Depth** **Pruning.** Unlike width pruning, the literature on depth pruning (removal of entire transformer
blocks) presents conflicting results. Some works, such as Kim et al. Kim et al. (2024), advocate for this
technique, arguing that it can achieve "comparable or superior" performance to width pruning. However,
more recent research, such as Wang et al. Wang et al. (2025), demonstrates that removing even a few layers
severely degrades test-time scaling, causing a "catastrophic collapse" in long-chain reasoning benchmarks—a
structural damage that proves irrecoverable through fine-tuning. Our width pruning approach offers more
granular control compared to this drastic measure, enabling more gradual and selective degradation.


**GLU-Specific** **Pruning.** Prior work that systematically analyzes the impact of expansion ratios in GLU
architectures is limited. A previous exploratory study Martra (2024a) identified a 140% expansion ratio as
an empirical equilibrium point for performance in Llama-3.2 models. However, that work did not provide
a systematic characterization of the underlying mechanisms or the selective impact on different cognitive
capabilities. To our knowledge, no study has framed the expansion ratio as an intervention to selectively
modulate cognitive functions. This gap—moving from empirical observation to systematic characterization—
motivates our approach: we demonstrate that width pruning in GLU-MLP layers does not simply constitute
uniform compression but rather an intervention that selectively modifies different cognitive capabilities, with
the expansion ratio emerging as a critical metric for determining pruning effectiveness.


**3** **Methodology**


This section describes the methodological approach used to systematically prune Llama-3.2 models and
evaluate the impact of varying GLU expansion ratios on model performance and capabilities.


**3.1** **Width** **Pruning** **in** **GLU** **Architectures**


Width pruning reduces the intermediate dimension of MLP layers in transformers, directly modifying the
architectural parameter known as the expansion ratio. In architectures based on Gated Linear Units (GLU),
each MLP layer contains three linear projections: gate_proj, up_proj, and down_proj Shazeer (2020).


The first two process the input in parallel (with an output dimension of intermediate_dim), where gate_proj
applies a sigmoid activation that modulates the output of up_proj before projecting back to the hidden
dimension through down_proj. The expansion ratio is defined as intermediate_dim _/_ hidden_dim and determines the expansion capacity of these layers.


5


Width pruning in GLU requires **paired pruning** : neurons removed from gate_proj must exactly correspond
to those removed from up_proj to maintain the coherence of the gating mechanism Guo et al. (2024).


**Neuron** **Selection:** **MAW** To determine which neurons to prune, we conducted a preliminary evaluation
comparing three importance metrics: Maximum Absolute Weight (MAW), Vector-based Output Weighting (VOW), and Product of Norms (PON) (see Appendix D). The VOW and PON methods resulted in
catastrophic performance degradation immediately after pruning.


The MAW method calculates the importance of each neuron as the maximum absolute value of its incoming
weights. This calculation accounts for the parallel operation of the up_proj and gate_proj layers.


The formula used to calculate the importance score (importance_scores) of each candidate neuron, combining
the weight values from the two paired layers, is as follows:


**Step** **1:** **Calculation** **of** **the** **Maximum** **Absolute** **Weight** **for** **each** **expansion** **layer**


gate_max_abs = max( _W_ gate _,_ axis = 1) + _|_ min( _W_ gate _,_ axis = 1) _|_


up_max_abs = max( _W_ up _,_ axis = 1) + _|_ min( _W_ up _,_ axis = 1) _|_


**Step** **2:** **Calculation** **of** **the** **Combined** **Importance** **Score**


importance_scores = gate_max_abs + up_max_abs


The neurons with the lowest importance scores, as determined by this formula, are selected for removal from
the model.


The selection of MAW as the importance method is justified by preliminary results documented in Appendix D. Alternative methods—VOW (Variance of Weights) and PON (Product of Norms)—resulted in
catastrophic performance collapse: at 10% pruning in Llama-3.2-1B, VOW increased WikiText perplexity
by +337% and Lambada by +9 _,_ 207%, while PON reached +527% and +35 _,_ 440%, respectively. By contrast,
MAW maintained moderate increases of +51% and +259%, confirming its superiority for GLU architectures
(see Appendix D).


The pruning implementation was carried out using the **optipfair** library (v0.2.0) Martra (2024b), a specialized tool for structured pruning in GLU architectures that automatically handles paired pruning and ensures
dimensional consistency Guo et al. (2024). The configuration applied uniform pruning across all model layers
while preserving the attention architecture. All operations were performed using bfloat16 precision.


**3.2** **Experimental** **configuration**


We evaluated two models from the Llama-3.2 family AI (2024) in their base version (not instruct):


  - Llama-3.2-1B: hidden_size = 2048, intermediate_size = 8192, baseline expansion ratio of 4 _._ 0 _×_


  - Llama-3.2-3B: hidden_size = 3072, intermediate_size = 8192, baseline expansion ratio of 2 _._ 67 _×_


This selection enables us to analyze how pruning affects models with different baseline expansion ratios and
parameter scales.


For each model, we evaluated seven pruning configurations, ranging from the unpruned baseline (0%) to
aggressive pruning (60%). Since the models have different baseline expansion ratios, the same pruning
percentage results in different final expansion ratios. Table 1 presents the complete mapping:


6


Table 1: Pruning confgurations and resulting expansion ratios for Llama-3.2-1B and 3B models.

**Expansion** **1B** **Pruning** **3B** **Pruning** **Inter.** **Dim** **Inter.** **Dim**
**Ratio** **(%)** **(%)** **(1B)** **(3B)**


4.0x 0% (baseline)         - 8192         3.6x 10%         - 7373         3.2x 20%         - 6554         2.8x 30%         - 5735         2.67x        - 0% (baseline)        - 8192
2.4x 40% 10% 4916 7373
2.13x        - 20%        - 6554
2.0x 50%         - 4096         1.87x        - 30%        - 5735
1.6x 60% 40% 3277 4916
1.33x        - 50%        - 4096
1.07x        - 60%        - 3277


We used the expansion ratio as the primary independent variable to facilitate cross-model comparisons, as
it directly represents the architectural capacity of MLP layers regardless of the model’s base size Shazeer
(2020).


The pruned models were evaluated on a suite of 13 benchmarks covering diverse cognitive aspects of language
models Muralidharan et al. (2024):


Table 2: Benchmark suite employed for evaluation across cognitive categories.


**Category** **Benchmark** **Shots** **Metric** **Description**


Knowledge MMLU 5 Accuracy Multidisciplinary knowledge
ARC-Challenge 0 Accuracy Scientific reasoning


Math GSM8K 5 Exact Match Math problems with CoT
Reasoning MUSR 0 Acc-Norm Multi-step reasoning


Language HellaSwag 0 Acc-Norm Sentence completion
Understanding WinoGrande 0 Accuracy Ambiguity resolution
PIQA 0 Accuracy Physical reasoning
BoolQ 0 Accuracy Boolean questions


Language WikiText 0 Perplexity Continuous text perplexity
Modeling Lambada 0 Perplexity Last word prediction


Truthfulness TruthfulQA-MC1 0 Accuracy Truthfulness (single correct)
TruthfulQA-MC2 0 Accuracy Truthfulness (multi-correct)


Instruction IFEval 0 Strict Acc Instruction adherence
Following


To quantify efficiency trade-offs (Contribution 3), we evaluated inference in two operational scenarios:


  - **Single-Request** **(batch_size** = 1 **):** Simulating interactive applications, we measured end-to-end
latency (time to complete generation) and energy consumption (Joules/token).


  - **Batch** **Processing** **(batch_size** = 8 **):** Simulating high-concurrency workloads, we measured
throughput and energy consumption (Joules/token).


These measurements were performed using **CodeCarbon** Courty et al. (2025) on a set of representative
benchmarks:


7


  - HellaSwag (20 tokens, short generation)


  - MMLU (50 tokens, knowledge responses)


  - IFEval (150 tokens, instruction following)


These benchmarks were configured to ensure diversity in generation lengths and task types Muralidharan
et al. (2024); Xia et al. (2024).


All evaluations were conducted using the **EleutherAI** **LM** **Evaluation** **Harness** (v0.4.9.1) Sutawika et al.
(2024), a widely adopted framework that ensures reproducibility and comparability with other works. The
prompts and few-shot configurations adhered to the framework’s standard implementations.


Experiments were run on Google Colab with NVIDIA L4 GPUs (24GB VRAM). Inference employed
torch.bfloat16 precision with the device_map="auto" loading strategy to optimize memory usage. The
total evaluation time per model was approximately 5-6 hours, encompassing all benchmarks and pruning
configurations.


**3.3** **Reproducibility**


To ensure full reproducibility of our experiments, all pipeline components are publicly available and fully
documented:


  - **Software** **and** **configurations:** We utilized **OptIFAIR** v0.2.0 Martra (2024b) for structural pruning and lm-evaluation-harness v0.4.9.1 Sutawika et al. (2024) for evaluations. All pruning configurations, including the MAW method, applied percentages, and calibration seeds, are documented in the
project’s public repository. The benchmark evaluations adhered to the default harness configurations
without modifications to the prompts.


  - **Data** **and** **checkpoints:** The baseline models were sourced directly from HuggingFace Hub
(meta-llama/Llama-3.2-1B and meta-llama/Llama-3.2-3B) AI (2024). Complete results in JSON
format, including comprehensive experimental metadata, are accessible in the project repository.


  - **Source** **code:** The entire codebase to reproduce the pruning process, evaluations, and all analyses
is available on GitHub: `[https://github.com/peremartra/llama-glu-expansion-pruning](https://github.com/peremartra/llama-glu-expansion-pruning)` . The
repository contains documented notebooks for each experimental phase and scripts to regenerate all
figures presented in the paper.


**4** **Results**


This section presents the empirical findings from applying our MAW-based width pruning methodology (3)
to the Llama-3.2-1B and 3B models. We analyze the impact of reducing the GLU expansion ratio using a
comprehensive suite of capacity and efficiency benchmarks Muralidharan et al. (2024).


The results validate our hypothesis of selective capacity degradation. We demonstrate that pruning does not
induce uniform degradation but rather a set of complex and systematic trade-offs between different cognitive
functions and operational efficiency metrics (see Section 4.3).


**4.1** **Overall** **Performance** **Landcape**


We evaluated seven expansion ratio configurations across two Llama-3.2 models (1B and 3B parameters)
using 13 benchmarks covering factual knowledge, mathematical and algorithmic reasoning, language understanding, truthfulness, and instruction-following. The results reveal markedly heterogeneous degradation
patterns across different types of cognitive tasks. Table 3 presents a summary of the most representative
benchmarks at key expansion ratios: baseline, the 2 _._ 4 _×_ ratio (identified as the equilibrium point in both
models), and the most aggressive ratio evaluated. The following subsections systematically characterize three
main findings:


8


  - A dichotomy between fragile and robust capabilities (see Section 4.2)


  - An inverse correlation between knowledge and truthfulness (see Section 4.3)


  - Trade-offs between energy efficiency and inference latency (see Section 4.4)


Complete results for all expansion ratios and benchmarks are available in Appendix A.


Table 3: Performance Summary at Key Expansion Ratios. Values in bold indicate performance improvements
relative to baseline.


**Llama-3.2-1B** **Llama-3.2-3B**
**Benchmark** **Category** **4.0×** **2.4×** **1.6×** **2.67×** **2.4×** **1.07×**


MMLU (Knowledge) 0.311 0.269 0.255 0.561 0.433 0.259
GSM8K (Math Reasoning) 0.064 0.009 0.007 0.264 0.135 0.011
IFEval (Instruction Following) 0.104 **0.152** **0.137** 0.094 **0.131** **0.133**
MUSR (Algorithmic Reasoning) 0.340 **0.429** **0.409** 0.364 **0.373** 0.360
TruthfulQA-MC2 (Truthfulness) 0.377 **0.430** **0.466** 0.392 0.377 **0.457**


Complete results for all 7 expansion ratios and 13 benchmarks are provided in Appendix A.


**4.2** **The** **Capability** **Dicothomy**


The analysis of performance trajectories across expansion ratios reveals markedly contrasting patterns between different benchmarks. While some metrics show predictable and monotonic collapse with expansion
ratio reduction, others exhibit unexpected behaviors: initial improvement followed by gradual degradation,
or even sustained improvement across multiple pruning levels Hou et al. (2025). Figures 2 and 3 illustrate
these contrasting patterns for six representative benchmarks in Llama-3.2-1B and Llama-3.2-3B, respectively.
These patterns reveal a systematic dichotomy that remains consistent between both model sizes under the
MAW (Maximum Absolute Weight) neuron selection method.


Figure 2: Llama-3.2-1B Benchmarks. Panel A (Fragile Capabilities) shows the predictable collapse of
knowledge-dependent tasks (GSM8K, Lambada, WikiText) as expansion ratio decreases. Panel B (Robust
Capabilities) reveals the contrasting improvement of algorithmic and instruction-following tasks (IFEval,
MUSR, TruthfulQA-MC2). Performance is normalized to baseline (4.0×) = 100%. The X-axis represents
expansion ratios from 4.0× to 1.6×; the Y-axis shows normalized performance.


9


]


Figure 3: Llama-3.2-3B Benchmarks. Panel A (Fragile Capabilities) demonstrates monotonic degradation of
knowledge-dependent tasks (GSM8K, Lambada, WikiText) across expansion ratios 2.67× to 1.07×. Panel B
(Robust Capabilities) exhibits non-monotonic improvement in instruction-following (IFEval reaching 174.4%
of baseline) and consistent gains in truthfulness (TruthfulQA-MC2). Performance is normalized to baseline
(2.67×) = 100%. This pattern replicates the dichotomy observed in Llama-1B.


These diverging patterns reveal two distinct categories of cognitive capabilities. **Fragile** **capabilities** (Panel
A in both figures) include tasks that critically depend on parameterized knowledge stored in the model’s
weights Sharma et al. (2023). Mathematical reasoning (GSM8K) illustrates this behavior in a particularly
dramatic way: in Llama-1B, accuracy collapses to 49 _._ 9% of baseline at an expansion ratio of 3 _._ 6 _×_ (after the
first 10% reduction), dropping precipitously to 14 _._ 3% at 2 _._ 4 _×_ and stabilizing around 10 _._ 7% at 1 _._ 6 _×_ . Llama3B exhibits a similar trajectory: 51 _._ 2% of baseline at 2 _._ 4 _×_, collapsing to just 4 _._ 0% at the most aggressive
ratio (1 _._ 07 _×_ ). Perplexity metrics show even more severe collapses: Lambada degrades exponentially in both
models, with WikiText demonstrating greater relative resilience but eventually converging toward the same
fate at extreme ratios Muralidharan et al. (2024) (see Appendix A).


In marked contrast, **robust** **capabilities** (Panel B) encompass tasks that require algorithmic processing
or behavioral adherence rather than factual knowledge retrieval. Instruction-following (IFEval) improves
with moderate pruning in both models (see Appendix A), reaching peaks of 175 _._ 0% of baseline in Llama-1B
(expansion ratio 2 _._ 8 _×_ ) and 174 _._ 4% in Llama-3B (expansion ratio 1 _._ 6 _×_ ). Notably, even at more aggressive
pruning levels, IFEval remains significantly above baseline: 132 _._ 2% in Llama-1B (1 _._ 6 _×_ ) and 141 _._ 1% in
Llama-3B (1 _._ 07 _×_ ). Algorithmic reasoning (MUSR) shows differentiated patterns between models: Llama1B reaches its maximum of 126 _._ 1% of baseline at an expansion ratio of 2 _._ 4 _×_, while Llama-3B stays close to
baseline with only moderate variations. TruthfulQA-MC2 exhibits gradual and sustained improvement in
both models, reaching 123 _._ 6% of baseline in Llama-1B (1 _._ 6 _×_ ) and 116 _._ 7% in Llama-3B (1 _._ 07 _×_ ), a pattern
explored in detail in Section 4.3.


This dichotomy, consistent across both model sizes, suggests that width pruning guided by the MAW importance criterion selectively modifies different functional components of the model. Fragile capabilities appear
to critically depend on neurons that the MAW criterion prioritizes for elimination, as evidenced by their
monotonic degradation as the expansion ratio decreases. Robust capabilities, by contrast, seem to depend
more on processing patterns distributed across the entire transformer architecture, where dimensionality
reduction in MLP layers can even act as a form of regularization that improves generalization by reducing
overfitting to spurious patterns memorized during pre-training Sharma et al. (2023). This interpretation
is supported by the particularly pronounced behavior of IFEval, whose improvement suggests that strict
instruction adherence benefits from the elimination of spurious correlations in MLP layers.


10


**4.3** **The** **Truthfulness** **Paradox**


Among the patterns observed in robust capabilities, the behavior of TruthfulQA-MC2 presents a notable
particularity: while metrics for factual knowledge degrade with pruning, truthfulness consistently improves
(see Appendix A). This inverse relationship constitutes a systematic pattern observed across both evaluated
models.


]


Figure 4: The Truthfulness Paradox. Divergent trajectories of factual knowledge (MMLU, blue dashed
lines) and truthfulness (TruthfulQA-MC2, orange solid lines) across expansion ratios. Panel A shows Llama3.2-1B; Panel B shows Llama-3.2-3B. As the expansion ratio decreases, factual knowledge degrades while
truthfulness improves, revealing a systematic inverse relationship.


Figure 4 illustrates this inverse relationship through divergent trajectories: while MMLU performance degrades monotonically (blue dashed lines), TruthfulQA-MC2 scores improve consistently (orange solid lines)
across all evaluated expansion ratios. In Llama-1B (Panel A), MMLU accuracy declines from 0 _._ 311 (baseline) to 0 _._ 255 (1 _._ 6 _×_, _−_ 17 _._ 9%), while TruthfulQA-MC2 accuracy improves from 0 _._ 377 to 0 _._ 466 (+23 _._ 6%).
In Llama-3B (Panel B), the divergent pattern is even more pronounced: MMLU accuracy collapses from
0 _._ 561 (baseline) to 0 _._ 259 (1 _._ 07 _×_, _−_ 53 _._ 8%), while TruthfulQA-MC2 accuracy improves from 0 _._ 392 to 0 _._ 457
(+16 _._ 7%). Correlation analysis quantifies this inverse relationship: Pearson _r_ = _−_ 0 _._ 676 ( _p_ = 0 _._ 096) for
Llama-1B, _r_ = _−_ 0 _._ 864 ( _p_ = 0 _._ 012) for Llama-3B, and _r_ = _−_ 0 _._ 627 ( _p_ = 0 _._ 016) for both models combined.


MAW-based width pruning results in an observable trade-off: a degradation of factual knowledge (MMLU)
is accompanied by an improvement in the model’s ability to avoid common misconceptions (TruthfulQAMC2). This consistent pattern across both models suggests that neuron selection through the Maximum
Absolute Weight (MAW) criterion differentially affects the types of knowledge stored in the MLP layers
Fu et al. (2025). TruthfulQA-MC2 specifically evaluates the model’s ability to distinguish between true
statements and plausible misconceptions that are common in human populations. The improvement in this
metric indicates that the MAW criterion, by prioritizing the retention of neurons with higher absolute weight
magnitudes, may selectively preserve information relevant to discriminating truth from misconceptions, while
removing neurons associated with general factual knowledge responses (see Appendix A).


This trade-off has practical implications for selecting both pruning methods and expansion ratio configurations based on application requirements. In contexts where minimizing incorrect responses is prioritized
over comprehensive factual knowledge, the MAW approach with moderately reduced expansion ratios may
be preferable. A complete characterization of this balance between different cognitive capabilities informs
the analysis of optimal configurations, which we further develop in Section 5.


**4.4** **Efficiency** **Trade-offs:** **Single-Request** **vs.** **Batch** **Processing**


MAW-based width pruning yields energy efficiency improvements Gholami & Omar (2023) that vary significantly depending on the inference mode. In a **Single-Request** configuration (batch_size = 1), Llama-1B


11


reduces energy consumption from 0 _._ 268 J/token (baseline, 4 _._ 0 _×_ ) to 0 _._ 222 J/token at 2 _._ 4 _×_ ( _−_ 17 _._ 2%) and
to 0 _._ 206 J/token at 1 _._ 6 _×_ ( _−_ 23 _._ 1%), as measured using MMLU as a representative benchmark for longgeneration tasks. However, this improvement comes at the cost of increased end-to.end latency in aggressive
pruning configurations. Although latency exhibits variability across intermediate expansion ratios, the general trend in aggressive configurations shows an increase: it reaches 929 ms at 2 _._ 4 _×_ (+12 _._ 7% compared
to baseline) and 970 ms at 1 _._ 6 _×_ (+17 _._ 7%), highlighting a trade-off between energy efficiency and response
latency (see Appendix C).


Figure 5 illustrates this trade-off and demonstrates that the deployment context critically determines its
practical relevance. In a **Batch** **Processing** configuration (batch_size = 8), energy efficiency improves
dramatically: Llama-1B consumes only 0 _._ 055 J/token at baseline (79 _._ 5% lower than single-request) and
0 _._ 048 J/token at 2 _._ 4 _×_ (78 _._ 3% lower than single-request).


Pruning benefits both configurations, but the absolute difference between inference modes persists: the
pruned model at 2 _._ 4 _×_ consumes 0 _._ 222 J/token in single-request mode versus 0 _._ 048 J/token in batch
processing—a 4 _._ 6 _×_ difference. Llama-3B follows similar patterns, with comparable advantages in batch
processing.


Figure 5: Efficiency Trade-offs - Single-Request vs Batch Processing. Panel A (Llama-3.2-1B) and Panel
B (Llama-3.2-3B) display the relationship between end-to-end latency (red lines), single-request energy consumption (blue dashed lines), and batch processing energy consumption (blue solid lines) across expansion
ratios. Latency increases with pruning intensity in both models. Single-request energy decreases across expansion ratios, while batch processing energy remains consistently lower than single-request configurations
at all expansion ratios. The left Y-axis shows latency in milliseconds; the right Y-axis shows energy consumption in joules per token.


This pattern suggests that pruned configurations are better optimized for batch processing workloads
(see Section 4.4; see Appendix C) than for interactive, single-request applications. In high-concurrency
scenarios—where multiple requests are processed simultaneously—the fixed cost of prompt processing is
amortized across parallel generations, effectively diluting the impact of increased individual end-to-end latency on overall system throughput.


**5** **Discussions**


This section interprets the empirical findings presented in Section 4. We begin by analyzing the theoretical
implications of the capacity dichotomy (Section 5.1) and the truthfulness paradox (Section 5.2), then derive
practical consequences for deployment (Section 5.3), and finally contextualize the work by addressing its
limitations (Section 5.4) and future directions (Section 5.5).


12


**5.1** **Interpretation** **of** **the** **Capacity** **Dichotomy**


The systematic dichotomy between fragile capabilities (e.g., GSM8K, MMLU, perplexity) and robust capabilities (e.g., IFEval, MUSR, TruthfulQA-MC2), as observed in Section 4.2, remains consistent across both
Llama-3.2-1B and Llama-3.2-3B. This consistency suggests that the dichotomy is not an artifact specific to
a single model but rather a reproducible architectural pattern. We propose that the absolute magnitude
of weights—the criterion employed by the MAW method—reflects distinct computational roles within the
GLU-MLP layers: neurons with high-weight magnitudes may be associated with algorithmic processing and
adherence to instructional structures (e.g., IFEval, MUSR) (see Section 4.2), whereas neurons with lowerweight magnitudes primarily contribute to the storage and retrieval of parameterized factual knowledge (e.g.,
MMLU, GSM8K).


This interpretation is supported by the differential severity of performance degradation: while GSM8K accuracy collapses drastically ( _−_ 85 _._ 7% in Llama-1B and _−_ 48 _._ 8% in Llama-3B at a 2 _._ 4 _×_ expansion ratio),
instruction-following metrics exhibit substantial improvements (+46 _._ 5% and +39 _._ 1%, respectively) (see Appendix A).


Our finding that static MAW pruning improves instruction-following performance aligns with the work of
Hou et al. Hou et al. (2025), who also aim to enhance instruction-following through pruning. However,
their approach relies on a dynamic method based on instruction activations, which contrasts with our static,
weight-based strategy.


The specificity of the neuron selection method is critical to achieving this behavior. A preliminary evaluation comparing MAW with alternative pruning methods (VOW and PON) revealed that the latter lead
to catastrophic performance collapse: at a 10% pruning ratio in Llama-3.2-1B, VOW increased WikiText
perplexity by +337% and Lambada by +9 _,_ 207%, while PON resulted in increases of +527% and +35 _,_ 440%,
respectively (Appendix D). By contrast, MAW produced more moderate increases of +51% and +259%.
This empirical evidence confirms that the importance criterion fundamentally determines which cognitive
capabilities are preserved during pruning.


Additionally, recent activation-based width pruning methods—such as SliceGPT Ashkboos et al. (2024),
which applies PCA to activation covariance matrices, and AMP Mugnaini et al. (2025), which uses projected
activation magnitude—do not report similar dichotomies. Instead, these methods focus on minimizing
uniform performance degradation across tasks. This divergence suggests that the observed dichotomy is
specific to the MAW criterion and not a general property of width pruning in GLU architectures.


These observations carry direct implications for the design of pruning strategies. Importance criteria are
not interchangeable; different methods selectively impact distinct cognitive capabilities of the model. While
activation-based approaches prioritize preserving uniform performance, MAW introduces a selective trade-off
that may be advantageous in applications where instructional adherence and truthfulness take precedence
over the exhaustiveness of factual knowledge.


**5.2** **Interpretation** **of** **the** **Truthfulness** **Paradox**


The inverse correlation between factual knowledge (MMLU) and truthfulness (TruthfulQA-MC2), as documented in Section 4.3, suggests a selective mechanism for information elimination. We propose that the misconceptions evaluated in TruthfulQA-MC2—incorrect yet plausible claims common in human populations—
may be preferentially stored in neurons with low absolute weight magnitudes. These are precisely the
neurons that the MAW criterion prioritizes for elimination. The sustained and monotonic improvement
in TruthfulQA-MC2 performance across all evaluated expansion ratios (from 0 _._ 377 to 0 _._ 466 in Llama-1B,
+23 _._ 6%) contrasts with the relative stability of TruthfulQA-MC1 (from 0 _._ 234 to 0 _._ 238, +1 _._ 6%). This suggests that pruning does not uniformly increase the model’s caution but specifically reduces its tendency to
select plausible yet incorrect answers when multiple alternatives are presented.


This pattern aligns with the hypothesis that MAW pruning preserves high-confidence knowledge (associated
with high-magnitude neurons) while eliminating spurious or less consolidated misconceptions (associated with
low-magnitude neurons). The severity of MMLU degradation ( _−_ 53 _._ 8% in Llama-3B at an expansion ratio of


13


1 _._ 07 _×_ ) concurrent with TruthfulQA-MC2 improvement (+16 _._ 7%) confirms that this trade-off is not marginal
but fundamental: MAW pruning does not make the model "smarter" or "more truthful" in an analytical sense.
Instead, it reduces the model’s reliance on memorized knowledge Muralidharan et al. (2024). By eliminating
low-magnitude neurons associated with stored information—whether correct or misconceptions—the model
has reduced access to memorized answers. This, in turn, decreases the likelihood of reproducing common
falsehoods alongside correct factual knowledge.


This dynamic presents an explicit trade-off for model design: in applications where encyclopedic comprehensiveness is critical, MAW pruning is detrimental. However, in domains where the priority is to minimize
the generation of plausible misinformation and reduce the model’s tendency to "hallucinate" incorrect facts,
this technique emerges as a valuable intervention.


**5.3** **Practical** **Implications:** **Balancing** **Capabilities** **and** **Efficiency**


Energy efficiency improves consistently up to an expansion ratio of 2 _._ 4 _×_, but this improvement comes with
critical trade-offs that depend on the inference mode Gholami & Omar (2023). In a **single-request** configuration (batch_size = 1), Llama-1B reduces energy consumption by 17 _._ 2% (from 0 _._ 268 to 0 _._ 222 J/token)
but increases end-to-end latency by 12 _._ 7% (from 824 ms to 929 ms). In contrast, **batch** **processing**
(batch_size = 8) offers substantially superior efficiency (0 _._ 048 J/token, approximately 4 _._ 6 _×_ better than
single-request mode) with throughput resilience. These results suggest distinct optimization profiles for
different deployment scenarios (see Section 4.4).


It is worth noting that the end-to.end latency analysis reveals non-monotonic behavior at intermediate
expansion ratios (a decrease between 3 _._ 6 _×_ and 3 _._ 2 _×_, followed by a sustained increase), possibly due to
hardware optimizations or cache memory effects. However, this pattern does not invalidate the general
trend of increasing latency in more aggressive pruning configurations.


The 2 _._ 4 _×_ expansion ratio emerges as an equilibrium point for balancing capabilities in the two evaluated
models. However, this convergence should be interpreted cautiously: with only two model sizes (1B and 3B),
we cannot claim that 2 _._ 4 _×_ is universally optimal for the entire Llama family or for GLU architectures in
general. Notably, achieving a 2 _._ 4 _×_ ratio requires substantially different pruning percentages in each model:
40% in Llama-1B (from a baseline of 4 _._ 0 _×_ ) versus only 10% in Llama-3B (from a baseline of 2 _._ 67 _×_ ). This
indicates that the equilibrium expansion ratio is not a function of the pruning percentage but rather a
property of the resulting architectural ratio.


At this ratio, both models retain robust algorithmic capabilities (IFEval: +46 _._ 5% and +39 _._ 1%, respectively) (see Appendix A) while maintaining factual knowledge at levels acceptable for many applications
(MMLU: 86 _._ 4% and 77 _._ 3% of baseline). However, mathematical reasoning capabilities exhibit severe degradation (GSM8K: 14 _._ 3% in Llama-1B, 51 _._ 2% in Llama-3B). This reveals a scale effect where larger models
demonstrate greater absolute fragility but also greater relative resilience in fragile tasks.


It is critical to recognize that the 2 _._ 4 _×_ ratio constitutes an equilibrium only under specific application priorities. For applications that prioritize the exhaustiveness of factual knowledge (e.g., MMLU, GSM8K) over
instructional adherence, higher expansion ratios—or even the unpruned baseline—would be more appropriate. The "optimal point" fundamentally depends on the application’s objectives Reda et al. (2025).


The practical guidelines derived from these results emphasize the importance of deployment context:


  - **Batch** **processing** **workloads** (e.g., offline generation, document analysis) can leverage 2 _._ 4 _×_ or
more aggressive configurations to maximize energy efficiency (see Appendix C).


  - **Instruction-following** **oriented** **applications** with modest encyclopedic knowledge requirements
may find the 2 _._ 4 _×_ ratio to be an optimal balance between improved behavioral adherence and
acceptable knowledge degradation (see Appendix A).


Unlike previous work on width pruning, such as **SliceGPT** and **AMP** —which does not report systematic
exploration of optimal expansion ratios or deployment-specific trade-offs—our approach reveals that the


14


optimal architectural ratio depends critically on both the neuron selection method and the specific use case
Mugnaini et al. (2025); Reda et al. (2025).


**5.4** **Limitations**


This study has several methodological and scope limitations that must be considered when interpreting the
results. First, our analysis is limited to two model sizes within the Llama-3.2 family (1B and 3B parameters),
both of which fall within the small model range. As a result, our conclusions about width pruning behavior
using the MAW method cannot be extrapolated to larger models (7B, 13B, 70B+), where the distribution
of capabilities and resilience to pruning may differ significantly.


Second, we exclusively evaluate GLU architectures as implemented in Llama-3.2. The observed capacity
dichotomy and the 2 _._ 4 _×_ equilibrium point may not generalize to other architectural families (e.g., Mistral,
Qwen, Gemma) or to MLP variants without gating mechanisms Guo et al. (2024); Shazeer (2020).


Third, we employ only the MAW (Maximum Absolute Weight) method for neuron selection, having empirically validated its superiority over VOW and PON. However, we do not explore other potentially relevant
criteria—such as gradient-based importance, second-order methods, or more sophisticated importance scoring techniques—that could reveal different trade-offs Ai et al. (2025). It is critical to emphasize that our
main findings, particularly the dichotomy between fragile and robust capabilities and the truthfulness paradox, are specific to the MAW criterion. As demonstrated in our preliminary experiments (Appendix D),
alternative methods like VOW or PON lead to catastrophic performance collapse even at minimal pruning
levels. Therefore, these patterns should not be generalized to width pruning as a whole, but specifically to
width pruning using MAW selection.


The experimental scope also presents additional limitations. The main results (Section 4) focus on base
models without instruction tuning, with analysis of instruct models deferred to Appendix B. Since instruction
tuning substantially alters the distribution of knowledge in the weights, we cannot confirm that the observed
patterns persist in models fine-tuned for instruction following. Furthermore, we do not explore post-pruning
recovery strategies through additional fine-tuning, which could potentially mitigate the degradation of fragile
capabilities such as GSM8K Muralidharan et al. (2024). We also do not conduct controlled comparisons
with alternative compression techniques—such as quantization (reducing numerical precision) or knowledge
distillation (transferring to smaller architectures)—which might offer different trade-offs between efficiency
and capabilities. Finally, we apply uniform pruning across all model layers and do not investigate whether
layer-selective pruning (preserving specific early or late layers) or non-uniform pruning could improve the
balance of capabilities Sharma et al. (2023).


These limitations do not invalidate the reported findings but do define their scope. The qualitative patterns
observed—the dichotomy between fragile and robust capabilities Wei et al. (2024), the truthfulness paradox
(inverse correlation between MMLU and TruthfulQA), and the trade-off between energy efficiency and endto-end latency—are robust within the evaluated context (small Llama-3.2 models, MAW method, base
configuration). However, they may generalize to broader contexts only with further empirical validation.
In contrast, the specific equilibrium point at a 2 _._ 4 _×_ expansion ratio is the most context-dependent finding:
consistently observed in only two model sizes (1B and 3B), each with different architectural baselines (4 _._ 0 _×_
and 2 _._ 67 _×_ ). Its transferability to larger models or distinct architectural families remains uncertain and
requires specific investigation.


**5.5** **Future** **Work**


The findings of this study, together with the limitations identified in Section 5.4, open multiple avenues for
future research. The most immediate direction involves extending the analysis to larger models within the
Llama family (7B, 13B, 70B) and other GLU-based architectures (e.g., Mistral, Qwen). This extension aims
to determine whether the qualitative patterns observed persist:


  - The dichotomy between fragile capabilities (parameterized factual knowledge) and robust capabilities
(algorithmic processing and instruction-following),


15


  - The truthfulness paradox, where a reduction in factual knowledge correlates with an improvement
in misconception discrimination, and


  - The systematic trade-off between energy efficiency and end-to-end latency, depending on the inference mode.


Additionally, it is essential to determine whether an analogous architectural equilibrium point—though not
necessarily at 2 _._ 4 _×_ —exists in larger-scale models, balancing these competing tensions. Such findings would
provide insights into the generality of our observations. The code repository accompanying this study
includes a configurable pipeline designed to facilitate this extension, requiring only the specification of the
target model and desired pruning ratios.


**Exploration** **of** **Alternative** **Importance** **Scoring** **Methods**


Investigating alternative importance scoring methods—particularly hybrid criteria that combine weight magnitude with activation statistics—could clarify whether the observed capability dichotomy is specific to the
MAW method Ai et al. (2025) or a more fundamental property of width pruning in GLU architectures. This
research direction also raises a broader hypothesis for future exploration: width pruning could serve not
only as a compression technique but also as a tool for functional specialization and behavior modification in
zero-shot settings Sharma et al. (2023).


We propose that the importance criterion acts as a control mechanism for this specialization. By designing
custom criteria (e.g., activation-based), it may be possible to selectively shape the model’s capability profile
Sharma et al. (2023), enhancing specific domains or mitigating biases.


**Impact** **of** **MAW** **Pruning** **on** **Instruction-Tuned** **Models**


Further research should also examine how MAW pruning affects models that have undergone instruction
tuning Hou et al. (2025). Our preliminary analysis (Appendix B) reveals a counterintuitive finding: although
the Llama-1B-Instruct model experiences a drop in IFEval performance from 36 _._ 41% to 14 _._ 6% after 40%
pruning (an apparent degradation of _−_ 59 _._ 9%), this final performance level converges to that of the pruned
base model in the same configuration (15 _._ 16%).


This suggests that MAW pruning does not degrade the model’s fundamental instruction-following capabilities. Instead, it selectively eliminates the specific improvements introduced by fine-tuning—the gains from
10 _._ 35% to 36 _._ 41% that instruction tuning had added to the base model. The most parsimonious interpretation
is that instruction tuning stores its modifications in neurons with low absolute weight magnitudes—precisely
those that MAW prioritizes for elimination—while base capabilities reside in high-magnitude neurons.


**6** **conclusion**


This study presents a systematic analysis of the impact of width pruning on GLU-MLP layers in Llama-3.2
models, specifically examining how variations in the expansion ratio affect different cognitive capabilities.
Despite being a fundamental architectural parameter, the expansion ratio has received limited empirical
attention in the structured pruning literature Zhu et al. (2024). Our results demonstrate that width pruning
guided by the Maximum Absolute Weight (MAW) criterion does not merely serve as uniform compression.
Instead, it acts as a selective intervention that modifies distinct model functions, revealing systematic tradeoffs between cognitive capabilities and operational efficiency metrics. These findings suggest that width
pruning, through the deliberate design of importance criteria, could be employed as a tool for selective
behavioral modification rather than simple compression Sharma et al. (2023)—a direction we propose to
explore in future work (Section 5.5).


**Capability** **dichotomy.** The central finding of this study is the existence of a reproducible dichotomy
between fragile and robust capabilities Wei et al. (2024). While tasks reliant on parametric knowledge—such
as MMLU, GSM8K, and perplexity—degrade predictably with reductions in the expansion ratio Muralidharan et al. (2024) (see Section 4.2), instruction-following metrics exhibit significant improvements (IFEval:
+46 _._ 5% in Llama-1B and +39 _._ 1% in Llama-3B at an expansion ratio of 2 _._ 4 _×_ for each model) (Appendix


16


A). This reveals a systematic trade-off between factual memory and behavioral adherence. This pattern
remains consistent across both evaluated models (1B and 3B parameters), suggesting that it is not an artifact specific to a single model size but rather a reproducible architectural phenomenon. Critically, this
dichotomy is specific to the MAW criterion. As demonstrated in our preliminary experiments, alternative
pruning methods—such as VOW and PON—result in catastrophic performance collapse even at minimal
pruning levels.


**Truthfulness** **paradox.** We document a robust inverse correlation ( _r_ = _−_ 0 _._ 864, _p_ = 0 _._ 012 in Llama3B) between factual knowledge (MMLU) and truthfulness (TruthfulQA-MC2) (Section 4.3). While MMLU
degrades monotonically with expansion ratio reduction, TruthfulQA-MC2 improves consistently (+23 _._ 6% in
Llama-1B, +16 _._ 7% in Llama-3B in the most aggressive configurations) (see Appendix A). This relationship
suggests that MAW selectively reduces the model’s reliance on memorized misconceptions, presenting an
explicit trade-off: in applications where minimizing plausible misinformation is prioritized over encyclopedic
comprehensiveness, MAW width pruning emerges as a beneficial intervention; in contexts where factual
knowledge retrieval is critical, it proves detrimental Muralidharan et al. (2024).


**Efficiency** **trade-offs** **depend** **on** **the** **inference** **mode.** Pruning reduces energy consumption by
up to 23% (J/token) but increases end-to-end latency by up to 17 _._ 58% in single-request configurations
(batch_size = 1). Batch processing (batch_size = 8) achieves 4 _._ 6 _×_ superior energy efficiency with stable
throughput (see Section 4.4).


A 2 _._ 4 _×_ expansion ratio emerges as an equilibrium point in the two evaluated models, balancing algorithmic
capability improvements (+46% and +39% in IFEval) (Appendix A) with controlled factual knowledge
degradation (86 _._ 4% and 77 _._ 3% of baseline MMLU) Muralidharan et al. (2024). However, it is critical to
recognize that this "optimal point" depends fundamentally on application priorities Reda et al. (2025): for
systems prioritizing knowledge exhaustiveness over instructional adherence, higher expansion ratios—or even
the unpruned baseline—would be more appropriate.


In summary, this work establishes that the expansion ratio in GLU-MLP layers is not merely a compression
hyperparameter but an architectural variable that determines systematic trade-offs between different types of
cognitive capabilities. The selection of the optimal ratio depends critically on the importance criterion used
(MAW vs. alternatives) Ai et al. (2025), the deployment context (batch vs. single-request), and application
priorities (instructional adherence vs. factual knowledge).


The pruned models and complete code to reproduce all experiments are on GitHub: `[https://github.com/](https://github.com/peremartra/llama-glu-expansion-pruning)`
`[peremartra/llama-glu-expansion-pruning](https://github.com/peremartra/llama-glu-expansion-pruning)` .


**References**


Mengting Ai, Tianxin Wei, Sirui Chen, and Jingrui He. NIRVANA: Structured pruning reimagined
for large language models compression, September 2025. URL `[http://arxiv.org/abs/2509.14230](http://arxiv.org/abs/2509.14230)` .
arXiv:2509.14230 [cs].


Meta AI. llama-models/models/llama3_2/MODEL_card.md at main - meta-llama/llama-models, 2024.
URL `[https://github.com/meta-llama/llama-models/blob/main/models/llama3_2/MODEL_CARD.md](https://github.com/meta-llama/llama-models/blob/main/models/llama3_2/MODEL_CARD.md)` .


Saleh Ashkboos, Maximilian L. Croci, Marcelo Gennari do Nascimento, Torsten Hoefler, and James Hensman. SliceGPT: Compress Large Language Models by Deleting Rows and Columns, February 2024. URL
`[http://arxiv.org/abs/2401.15024](http://arxiv.org/abs/2401.15024)` . arXiv: 2401.15024.


Benoît Courty, Victor Schmidt, Goyal-Kamal, inimaz, MarionCoutarel, Luis Blanche, Boris Feld, Jérémy
Lecourt, LiamConnell, Amine Saboni, SabAmine, supatomic, Patrick LLORET, Mathilde Léval, Alexis
Cruveiller, ouminasara, Franklin Zhao, Christian Bauer, Aditya Joshi, Jerry Laruba Festus, Alexis Bogroff,
Niko Laskaris, Hugues de Lavoreille, Alexandre Phiev, Edoardo Abati, Douglas Blank, rosekelly6400,
and Ziyao Wang. mlco2/codecarbon: v3.0.8, October 2025. URL `[https://zenodo.org/doi/10.5281/](https://zenodo.org/doi/10.5281/zenodo.4658424)`
`[zenodo.4658424](https://zenodo.org/doi/10.5281/zenodo.4658424)` .


17


Yao Fu, Runchao Li, Xianxuan Long, Haotian Yu, Xiaotian Han, Yu Yin, and Pan Li. Pruning Weights
but Not Truth: Safeguarding Truthfulness While Pruning LLMs, September 2025. URL `[https://arxiv.](https://arxiv.org/abs/2509.00096v2)`
`[org/abs/2509.00096v2](https://arxiv.org/abs/2509.00096v2)` .


Sia Gholami and Marwan Omar. Can pruning make Large Language Models more efficient?, October 2023.
URL `[http://arxiv.org/abs/2310.04573](http://arxiv.org/abs/2310.04573)` . arXiv:2310.04573 [cs].


Zhiyu Guo, Hidetaka Kamigaito, and Taro Wanatnabe. Dependency-Aware Semi-Structured Sparsity of
GLU Variants in Large Language Models, October 2024. URL `[http://arxiv.org/abs/2405.01943](http://arxiv.org/abs/2405.01943)` .
arXiv:2405.01943 [cs].


Bairu Hou, Qibin Chen, Jianyu Wang, Guoli Yin, Chong Wang, Nan Du, Ruoming Pang, Shiyu Chang, and
Tao Lei. Instruction-Following Pruning for Large Language Models, June 2025. URL `[http://arxiv.org/](http://arxiv.org/abs/2501.02086)`
`[abs/2501.02086](http://arxiv.org/abs/2501.02086)` . arXiv:2501.02086 [cs].


Bo-Kyeong Kim, Geonmin Kim, Tae-Ho Kim, Thibault Castells, Shinkook Choi, Junho Shin, and HyoungKyu Song. Shortened LLaMA: Depth Pruning for Large Language Models with Comparison of Retraining
Methods, June 2024. URL `[http://arxiv.org/abs/2402.02834](http://arxiv.org/abs/2402.02834)` . arXiv: 2402.02834.


Haohang Li, Yupeng Cao, Yangyang Yu, Jordan W. Suchow, and Zining Zhu. Truth Neurons, July 2025.
URL `[http://arxiv.org/abs/2505.12182](http://arxiv.org/abs/2505.12182)` . arXiv:2505.12182 [cs].


Pere Martra. Exploring GLU expansion ratios: Structured pruning in Llama-3.2 models, December 2024a.
URL `[https://osf.io/qgxea_v1/](https://osf.io/qgxea_v1/)` .


Pere Martra. optipfair: A Library for Structured Pruning and Bias Visualization of Large Language Models,
2024b. URL `[https://github.com/peremartra/optipfair](https://github.com/peremartra/optipfair)` . Versión 0.2.0, accedido 14 Noviembre 2025.


Leandro Giusti Mugnaini, Bruno Lopes Yamamoto, Lucas Lauton de Alcantara, Victor Zacarias, Edson
Bollis, Lucas Pellicer, Anna Helena Reali Costa, and Artur Jordao. Efficient LLMs with AMP: Attention
Heads and MLP Pruning, April 2025. URL `[http://arxiv.org/abs/2504.21174](http://arxiv.org/abs/2504.21174)` . arXiv: 2504.21174.


Saurav Muralidharan, Sharath Turuvekere Sreenivas, Raviraj Joshi, Marcin Chochowski, Mostofa Patwary,
Mohammad Shoeybi, Bryan Catanzaro, Jan Kautz, and Pavlo Molchanov. Compact Language Models
via Pruning and Knowledge Distillation, July 2024. URL `[http://arxiv.org/abs/2407.14679](http://arxiv.org/abs/2407.14679)` . arXiv:
2407.14679.


Waleed Reda, Abhinav Jangda, and Krishna Chintalapudi. How Many Parameters Does Your Task Really
Need? Task Specific Pruning with LLM-Sieve, October 2025. URL `[http://arxiv.org/abs/2505.18350](http://arxiv.org/abs/2505.18350)` .
arXiv:2505.18350 [cs].


Pratyusha Sharma, Jordan T Ash, and Dipendra Misra. THE TRUTH IS IN THERE: IMPROVING
REASONING IN LANGUAGE MODELS WITH LAYER-SELECTIVE RANK REDUCTION, 2023. URL
`[https://pratyushasharma.github.io/laser/](https://pratyushasharma.github.io/laser/)` .


Noam Shazeer. GLU Variants Improve Transformer, February 2020. URL `[http://arxiv.org/abs/2002.](http://arxiv.org/abs/2002.05202)`
`[05202](http://arxiv.org/abs/2002.05202)` . arXiv:2002.05202 [cs].


Mingjie Sun, Zhuang Liu, Anna Bair, and J. Zico Kolter. A Simple and Effective Pruning Approach for
Large Language Models, May 2024. URL `[http://arxiv.org/abs/2306.11695](http://arxiv.org/abs/2306.11695)` . arXiv: 2306.11695.


Lintang Sutawika, Hailey Schoelkopf, Leo Gao, Baber Abbasi, Stella Biderman, Jonathan Tow, ben fattori, Charles Lovering, farzanehnakhaee70, Jason Phang, Anish Thite, Fazz, Aflah, Niklas Muennighoff,
Thomas Wang, sdtblck, nopperl, gakada, tttyuntian, researcher2, Julen Etxaniz, Chris, Hanwool Albert Lee, Zdeněk Kasner, Khalid, LSinev, Jeffrey Hsu, Anjor Kanekar, KonradSzafer, and AndyZwei.
EleutherAI/lm-evaluation-harness: v0.4.3, July 2024. URL `[https://zenodo.org/doi/10.5281/zenodo.](https://zenodo.org/doi/10.5281/zenodo.12608602)`
`[12608602](https://zenodo.org/doi/10.5281/zenodo.12608602)` .


18


Keyu Wang, Tian Lyu, Guinan Su, Jonas Geiping, Lu Yin, Marco Canini, and Shiwei Liu. When Fewer
Layers Break More Chains: Layer Pruning Harms Test-Time Scaling in LLMs, October 2025. URL
`[http://arxiv.org/abs/2510.22228](http://arxiv.org/abs/2510.22228)` . arXiv: 2510.22228.


Boyi Wei, Kaixuan Huang, Yangsibo Huang, Tinghao Xie, Xiangyu Qi, Mengzhou Xia, Prateek Mittal,
Mengdi Wang, and Peter Henderson. Assessing the Brittleness of Safety Alignment via Pruning and
Low-Rank Modifications, October 2024. URL `[http://arxiv.org/abs/2402.05162](http://arxiv.org/abs/2402.05162)` . arXiv:2402.05162

[cs].


Mengzhou Xia, Tianyu Gao, Zhiyuan Zeng, and Danqi Chen. Sheared LLaMA: Accelerating Language
Model Pre-training via Structured Pruning, April 2024. URL `[http://arxiv.org/abs/2310.06694](http://arxiv.org/abs/2310.06694)` .
arXiv:2310.06694 [cs].


Wayne Xin Zhao, Kun Zhou, Junyi Li, Tianyi Tang, Xiaolei Wang, Yupeng Hou, Yingqian Min, Beichen
Zhang, Junjie Zhang, Zican Dong, Yifan Du, Chen Yang, Yushuo Chen, Zhipeng Chen, Jinhao Jiang,
Ruiyang Ren, Yifan Li, Xinyu Tang, Zikang Liu, Peiyu Liu, Jian-Yun Nie, and Ji-Rong Wen. A Survey of
Large Language Models, March 2025. URL `[http://arxiv.org/abs/2303.18223](http://arxiv.org/abs/2303.18223)` . arXiv:2303.18223 [cs].


Xunyu Zhu, Jian Li, Yong Liu, Can Ma, and Weiping Wang. A Survey on Model Compression for Large
Language Models, July 2024. URL `[http://arxiv.org/abs/2308.07633](http://arxiv.org/abs/2308.07633)` . arXiv: 2308.07633.


**A** **Complete** **Benchmark** **Results** **(Base** **Models)**


This appendix provides the complete results of the 13 benchmarks from the evaluation suite (described in
Table 2) for all expansion ratio configurations of the Llama-3.2-1B and Llama-3.2-3B base models.


**Metric** : All scores are Accuracy or Acc-Norm (higher is better), except WikiText and Lambada, which are
Perplexity (lower is better).


**Source** : Data is extracted from the project results files llama_1b_complete_results_latest.json and
llama_3b_complete_results_latest.json.


Table 4: Complete Benchmark Results vs. Expansion Ratio (Llama-3.2-1B).


**4.0x** **3.6x** **3.2x** **2.8x** **2.4x** **2.0x** **1.6x**
**Category** **Benchmark** **(Base)** **(10%)** **(20%)** **(30%)** **(40%)** **(50%)** **(60%)**


Knowledge MMLU 0.3111 0.2511 0.2661 0.2610 0.2689 0.2606 0.2554
ARC-Challenge 0.3626 0.3328 0.3080 0.2637 0.2509 0.2474 0.2398


Reasoning GSM8K 0.0637 0.0318 0.0212 0.0129 0.0091 0.0053 0.0068
MUSR 0.3399 0.3624 0.3638 0.3757 0.4286 0.3743 0.4087


Understanding HellaSwag 0.6363 0.5791 0.5076 0.4382 0.3737 0.3251 0.2909
WinoGrande 0.5991 0.6093 0.5935 0.5722 0.5706 0.5312 0.4870
PIQA 0.7454 0.7280 0.6757 0.6458 0.6115 0.5903 0.5637
BoolQ 0.6343 0.6260 0.6232 0.6260 0.6220 0.6141 0.5535


PPL WikiText 11.57 17.50 25.05 38.58 56.33 117.04 322.95
(Lower is better) Lambada 5.75 20.59 33.07 55.74 90.38 428.30 2941.08


Truthfulness TruthfulQA-MC1 0.2338 0.2460 0.2424 0.2448 0.2485 0.2460 0.2375
TruthfulQA-MC2 0.3772 0.4026 0.4153 0.4252 0.4298 0.4314 0.4661


Instructions IFEval 0.1035 0.1423 0.1275 0.1811 0.1516 0.1534 0.1368


19


Table 5: Complete Benchmark Results vs. Expansion Ratio (Llama-3.2-3B).


**2.67x** **2.4x** **2.13x** **1.87x** **1.6x** **1.33x** **1.07x**
**Category** **Benchmark** **(Base)** **(10%)** **(20%)** **(30%)** **(40%)** **(50%)** **(60%)**


Knowledge MMLU 0.5605 0.4333 0.2909 0.2307 0.2587 0.2555 0.2589
ARC-Challenge 0.4582 0.3959 0.3669 0.3123 0.2654 0.2381 0.2150


Reasoning GSM8K 0.2638 0.1350 0.0607 0.0273 0.0083 0.0068 0.0106
MUSR 0.3638 0.3730 0.3439 0.3373 0.3558 0.3545 0.3598


Understanding HellaSwag 0.7357 0.6853 0.6158 0.5232 0.4145 0.3399 0.2959
WinoGrande 0.6953 0.6748 0.6385 0.5927 0.5572 0.4886 0.4815
PIQA 0.7748 0.7508 0.7307 0.6812 0.6474 0.6045 0.5539
BoolQ 0.7294 0.5046 0.3972 0.4269 0.4208 0.5119 0.5034


PPL WikiText 9.26 11.88 15.86 23.35 42.18 74.83 162.47
(Lower is better) Lambada 3.95 6.11 8.16 14.72 51.02 240.72 5960.46


Truthfulness TruthfulQA-MC1 0.2497 0.2203 0.2387 0.2607 0.2448 0.2472 0.2387
TruthfulQA-MC2 0.3919 0.3767 0.4302 0.4390 0.4484 0.4391 0.4574


Instructions IFEval 0.0943 0.1312 0.1220 0.1534 0.1645 0.1627 0.1331


**B** **Analysis** **of** **Instruct-Tuned** **Models** **(Llama-3.2-1B-Instruct)**


The main analysis of this study (Section 4) focused on base models (pre-trained) to isolate the impact of width
pruning on the fundamental capabilities acquired during pre-training. However, to understand how MAW
pruning affects models that have been fine-tuned for instruction following, we conducted a complementary
evaluation using Llama-3.2-1B-Instruct. This analysis is based on a single instruct-tuned model; we did not
evaluate the 3B-Instruct model due to computational constraints.


The results reveal a critical finding: the "Capability Dichotomy" observed in base models does not replicate in
the evaluated instruct-tuned model. Specifically, instruction-following capability (IFEval), which improved
under moderate pruning in the base model (+3 _._ 3 percentage points from baseline to 1 _._ 6 _×_ ), experiences
severe degradation in the instruct-tuned model ( _−_ 22 _._ 7 percentage points) (Appendix B), converging toward
base model performance levels. In contrast, capabilities such as TruthfulQA-MC2 and MUSR remain robust
across both models, replicating the pattern observed in Section 4.3.


We observed that, under MAW pruning, the performance of the instruct-tuned model converges toward that
of the base model at low expansion ratios. Table B.1 compares the performance of Llama-3.2-1B (Base)
and Llama-3.2-1B-Instruct at equivalent expansion ratios, highlighting fragile capabilities (MMLU, GSM8K,
IFEval) alongside a robust capability (TruthfulQA-MC2) to illustrate this phenomenon.


Table 6: Performance Comparison: Base vs. Instruct at Equivalent Expansion Ratios.

**Exp.** **MMLU** **GSM8K** **IFEval** **TruthQA-MC2**
**Model** **Ratio** (Knowledge) (Reasoning) (Instruction) (Truthfulness)


Llama-1B (Base) 4.0x (0%) 0.311 0.064 0.104 0.377
Llama-1B-Instruct 4.0x (0%) 0.456 0.339 0.364 0.438


Llama-1B (Base) 2.4x (40%) 0.269 0.009 0.152 0.430
Llama-1B-Instruct 2.4x (40%) 0.261 0.016 0.146 0.437


Llama-1B (Base) 1.6x (60%) 0.255 0.007 0.137 0.466
Llama-1B-Instruct 1.6x (60%) 0.246 0.008 0.137 0.444


20


As shown in the table, while baseline models (4 _._ 0 _×_ ) exhibit significant performance gaps between the Base
and Instruct versions (e.g., +26 _._ 0 percentage points in IFEval, +27 _._ 5 percentage points in GSM8K), models
pruned at 2 _._ 4 _×_ and 1 _._ 6 _×_ converge to nearly identical values for fragile capabilities. At 1 _._ 6 _×_, IFEval reaches
exactly 0 _._ 137 in both models (mathematical convergence), GSM8K differs by only 0 _._ 1 percentage points, and
MMLU by 0 _._ 9 percentage points. Notably, TruthfulQA-MC2 does not show this convergence pattern and
remains stable across both models at all expansion ratios.


This convergence pattern suggests that the MAW criterion, which prioritizes absolute weight magnitudes,
eliminates neurons whose removal results in the loss of capabilities added during instruction tuning, while
preserving the base instruction-following capabilities inherent in the base model. The instruct-tuned model
does not fall below the base model’s IFEval performance (both converge to 13 _._ 7%), confirming that MAW
does not eliminate base instruction-following capabilities but only the improvements introduced during finetuning.


This reinforces the hypothesis presented in Section 5.5: the neural importance criterion acts as a control mechanism that determines which functional capabilities are preserved or removed. In the case of the evaluated
instruct-tuned model, MAW selectively eliminates both knowledge-intensive capabilities (MMLU, GSM8K)
Muralidharan et al. (2024) and alignment improvements (IFEval) introduced by fine-tuning, while consistently preserving robust capabilities (TruthfulQA-MC2, MUSR), in line with the behavior observed in base
models. These results are preliminary and specific to the MAW criterion as applied to Llama-3.2-1B-Instruct;
further evaluations with additional instruct-tuned models would be necessary to generalize these findings.


**C** **Complete** **Energy** **Efficiency** **Measurements**


Section 4.4 presents the energy efficiency trade-off analysis between inference modes (batch size 1 vs. 8).
Tables C.1 and C.2 provide the complete measurements for all evaluated expansion ratios in both models,
including energy consumption (J/token), end-to-end latency, and throughput Courty et al. (2025).


Table 7: Llama-3.2-1B Energy Efciency Metrics.

**Batch** **Size** **=** **1** **(Single** **Request)** **Batch** **Size** **=** **8** **(Batch)**


**Expansion** **Pruning** **Latency** **Throughput** **Throughput**
**Ratio** **(%)** **J/token** **(ms)** **(tok/s)** **J/token** **(tok/s)**


4.0x 0% 0.2767 877.30 50.90 0.0596 264.41
3.6x 10% 0.2763 1006.68 50.80 0.0696 262.95
3.2x 20% 0.2708 1123.24 51.15 0.0565 267.47
2.8x 30% 0.2529 1312.35 50.96 0.0618 265.49
2.4x 40% 0.2367 1320.89 50.80 0.0507 268.56 _[⋆]_

2.0x 50% 0.2313 1400.91 51.48 0.0473 275.04
1.6x 60% 0.2179 1396.79 51.33 0.0525 273.43


21


Table 8: Llama-3.2-3B Energy Efciency Metrics.

**Batch** **Size** **=** **1** **(Single** **Request)** **Batch** **Size** **=** **8** **(Batch)**


**Expansion** **Pruning** **Latency** **Throughput** **Throughput**
**Ratio** **(%)** **J/token** **(ms)** **(tok/s)** **J/token** **(tok/s)**


2.67x 0% 0.5970 1267.70 29.51 0.1262 153.63
2.40x 10% 0.5851 1790.98 29.45 0.1340 145.64
2.13x 20% 0.5689 1893.44 29.81 0.1206 155.75
1.87x 30% 0.5691 2053.14 29.81 0.1238 155.29
1.60x 40% 0.5407 2031.00 29.94 0.1099 161.17
1.33x 50% 0.5025 2066.31 30.16 0.1019 164.35
1.07x 60% 0.4691 2391.20 30.04 0.1115 162.91


**Notes:** J/token = joules per token (average energy per generated token); Latency = generation time
per prompt (milliseconds); Throughput = tokens generated per second. Metrics represent averages across
multiple benchmarks (HellaSwag, MMLU, IFEval) with three runs per configuration (seeds: 42, 123, 456).


**D** **Justification** **for** **the** **Selection** **of** **the** **Importance** **Criterion** **(MAW)**


The methodology of this study (Section 3) relies exclusively on the MAW (Maximum Absolute Weight) criterion for neuron selection during pruning. This decision is based on a preliminary evaluation conducted prior
to the main experiments (documented in the notebook 00_Neuron_Selection_Method_Comparison.ipynb
in the project repository), which compared MAW with two other weight-based importance methods: VOW
(Variance of Weights) and PON (Product of Norms).


The results of this preliminary evaluation demonstrated that alternative methods (VOW and PON) are
incompatible with gradual pruning in GLU architectures, leading to catastrophic performance collapse in
perplexity metrics. With only 10% pruning, VOW increased LAMBADA perplexity by +9 _,_ 207% (from
5 _._ 72 to 532 _._ 36), and PON by +35 _,_ 440% (from 5 _._ 72 to 2 _,_ 032 _._ 80), rendering systematic analysis of expansion
ratios unfeasible. In contrast, MAW was the only criterion that allowed controlled degradation (+259% in
LAMBADA, +51% in WikiText), enabling the gradual analysis reported in Sections 4 and 5.


Table 9: Catastrophic Collapse of Alternative Pruning Methods (10% Pruning, Llama-3.2-1B).


**Lambada** **(PPL)** **WikiText-2** **(PPL)**


**Selection** **Criteria** **Value** ∆ **vs.** **Base** **Value** ∆ **vs.** **Base**


Baseline (0%) 5.75 - 11.57 MAW (Maximum Absolute Weight) 20.59 +259% 17.45 +51%
VOW (Variance of Weights) 532.36 +9,207% 50.56 +337%
PON (Product of Norms) 2032.80 +35,440% 72.52 +527%


Source: Preliminary experiment documented in 00_Neuron_Selection_Method_Comparison.ipynb (project
repository). Evaluations conducted on full benchmarks.


As the data demonstrates, VOW and PON Ai et al. (2025) disrupt model coherence even at minimal
pruning levels, increasing LAMBADA perplexity by two and three orders of magnitude, respectively. This
catastrophic collapse precluded their use for gradual analysis of expansion ratios, which requires maintaining
basic model functionality across multiple pruning stages (10%, 20%, 30%, etc.).


22


The empirical superiority of MAW in preserving model stability under pruning justified its selection as the
only viable criterion for this study (see Table D.1). Consequently, all findings reported in this work—including
the Capability Dichotomy (Section 4.2), the Veracity Paradox (Section 4.3), and the energy efficiency analysis
(Section 4.4)—are specifically attributable to the nature of MAW-guided pruning. These findings should not
be generalized to width pruning as a general technique nor to other neuron selection criteria.


23


