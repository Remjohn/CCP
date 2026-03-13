## **How Controllable Are Large Language Models?** **A Unified Evaluation across Behavioral Granularities**

**Ziwen Xu** **[1,2]** [*] **,** **Kewei Xu** **[1]** [*] **,** **Haoming Xu** **[1]** **,** **Haiwen Hong** **[2]** **,** **Longtao Huang** **[2]** **,** **Hui Xue** **[2]** **,**
**Ningyu Zhang** [1], **Yongliang Shen** [1], **Guozhou Zheng** [1], **Huajun Chen** [1], **Shumin Deng** [3][†]

1Zhejiang University, 2Alibaba Group
3National University of Singapore, NUS-NCS Joint Lab, Singapore



**Abstract**


Large Language Models (LLMs) are increasingly deployed in socially sensitive domains,
yet their unpredictable behaviors, ranging from
misaligned intent to inconsistent personality,
pose significant risks. We introduce SteerEval,
a hierarchical benchmark for evaluating LLM
controllability across three domains: language
features, sentiment, and personality. Each domain is structured into three specification levels: L1 ( _what_ to express), L2 ( _how_ to express),
and L3 ( _how to instantiate_ ), connecting highlevel behavioral intent to concrete textual output. Using SteerEval, we systematically evaluate contemporary steering methods, revealing
that control often degrades at finer-grained levels. Our benchmark offers a principled and
interpretable framework for safe and controllable LLM behavior, serving as a foundation
for future research.


**1** **Introduction**


Large language models (LLMs) have shown impressive performance across a broad spectrum of
tasks, from dialogue and summarization to reasoning and creative generation (Zhao et al., 2023).
These advances have accelerated the deployment
of LLMs in socially sensitive domains such as education, healthcare, and decision support, where
model outputs can directly shape human behavior and well-being. However, alongside their impressive abilities, LLMs can exhibit unpredictable
or undesirable behaviors, including misalignment
with user intent, unintended shifts in sentiment, and
inconsistent personality expression. Such failures
pose tangible risks in real-world settings, making
reliable behavioral control not just desirable, but
essential (Anwar et al., 2024; Sharkey et al., 2025).
Controlling LLM behavior in human-facing applications involves two complementary dimensions:


  - Equal Contribution.

  - Corresponding Author.



Figure 1: Behavioral control targets can be organized
by granularity. For example, the target of _autonomy_
progresses from a high-level objective (Level 1), to a
constrained manner of expression (Level 2), and finally
to a directly checkable surface realization (Level 3).


_content_ (what the model expresses) and _granular-_
_ity_ (the level of specificity in its expression). This
distinction can be informed by Marr’s three levels
of analysis (Marr, 1982): at a high level, communication requires determining the intended message
(analogous to content), formulating a coherent plan
to convey it (analogous to intermediate specification), and producing concrete realizations (analogous to fine-grained instantiation). Similarly, effective model steering requires interpretable control
over both _what_ the model communicates and _how_
_precisely_ it is expressed, from abstract intent to
concrete textual realization.


Motivated by this analogy, we introduce a hierarchical benchmark, **SteerEval**, designed for systematically evaluating LLM steerability. We automatically synthesize the data with hierarchical concepts
and manually verify it to ensure quality. SteerEval
organizes behavioral control along two complementary axes. First, control targets are grouped into
three domains: language features, sentiment, and
personality. Second, each domain is structured hi


**Core Target: Dependency → Autonomy**

Dependency **Autonomy**

Exhibit personality.









Exhibit autonomy **.**














erarchically into three specification levels: **Level 1**
**(Computational level:** **what to express)**, **Level 2**
**(Algorithmic level:** **how to express it)**, and **Level**
**3** **(Implementational** **level:** **how** **to** **instantiate**
**it)** . For example, as shown in Figure 1, in the
personality domain, Level 1 defines the affective
polarity (autonomy or dependency), Level 2 constrains the tone or framing used to convey it, and
Level 3 enforces concrete lexical realizations. This
hierarchical organization provides a principled and
interpretable scaffold that links high-level behavioral intent to concrete textual outputs, facilitating
systematic evaluation of steering methods.
Using SteerEval, we conduct a comprehensive
evaluation of contemporary LLM steering methods
across domains and specification levels. Our analysis reveals nuanced patterns: while some methods
maintain reliable control at coarse-grained levels,
their performance often degrades as constraints become more fine-grained and behaviorally precise.
By framing model steering as a problem of _hier-_
_archical behavioral control_, SteerEval provides a
rigorous, interpretable, and actionable benchmark
for guiding the development of LLMs that are predictable, controllable, and socially safe.


**2** **Preliminary**


**2.1** **Steering Task**


Without steering, the model generates _y_ ˆ = _M_ ( _x_ ).
A steering method conditions on _g_ to construct an
inference-time intervention _Ig_, producing


_y_ ˆsteered = _Ig_ ( _M, x_ ) _,_ (1)


In this work, _Ig_ takes one of two forms: (i)
**prompt-based** steering, which prepends a concept
prompt _pg_ to the input, yielding _M_ ( _pg∥x_ ); or (ii)
**activation-based** steering, which modifies intermediate activations during the forward propagation
using a concept-specific vector.
Steering is evaluated by whether _y_ ˆsteered better
expresses the target concept _g_ while preserving general response quality, including instruction following and fluency. All interventions and evaluations
are implemented using the open-source framework
EASYEDIT2 (Xu et al., 2025).


**2.2** **Existing Benchmark**


Prior steering benchmarks are narrow in scope, targeting specific behaviors (Zou et al., 2023; Im and
Li, 2025) or tasks (Makelov, 2024), such as personality (Perez et al., 2023), sentiment (Han et al.,



2024; Farooq et al., 2025), or safety (Siu et al.,
2025; Han et al., 2025; Wang et al., 2025). Heterogeneous concept definitions and data formats make
cross-method comparison difficult.
AXBENCH (Wu et al., 2025b) partially addresses this issue by standardizing evaluation
across steering methods, but its concepts are derived from sparse autoencoders (SAEs) feature
descriptions (Lieberum et al., 2024) rather than
explicit behavioral definitions, lack domain or
granularity structure, and do not provide concepttargeted preference pairs for training. Moreover,
its evaluation prompts are sampled from AlpacaEval (Dubois et al., 2024), rather than being tailored to specific concepts.
We address these limitations with **SteerEval**,
a **hierarchical** **concept** **benchmark** equipped
with a scalable automated data synthesis pipeline.
SteerEval covers multiple behavioral domains and
organizes each domain into three specification levels, and provides **concept-targeted** **preference**
**data** and **concept-aligned** **evaluation** **sets**, enabling systematic and fair evaluation of controllability across domains and levels of granularity.


**2.3** **Hierarchical Control in Cognition**


Effective behavioral control relies on hierarchical
organization and goal-directed regulation. Marr’s
three levels of analysis (Marr, 1982) distinguishes
between computational goals, algorithmic representations, and physical implementation, highlighting
how behavior emerges from interacting layers of
abstraction. Complementarily, theories of cognitive
control (Botvinick and Braver, 2015; Badre, 2025)
describe mechanisms that select and regulate actions across these layers, enabling flexible behavior
from abstract intentions to concrete execution.
Motivated by these principles, our benchmark
organizes steering targets across coarse-grained behavioral domains and finer-grained L1 _∼_ L3 specification levels, providing a principled framework
for analyzing how steering signals interact with the
model’s internal hierarchy.


**3** **Hierarchical Steering Benchmark**


**3.1** **Design Principles**


We design a benchmark to probe the boundaries
of concept steering by testing the same core target
under progressively stricter granularity constraints.
Inspired by Marr’s three level of analysis (Marr,
1982), we organize steering targets with a three

Figure 2: Example cases from the three domains Personality, Sentiment, and Language Features across the
L1 _∼_ L3 hierarchies. Taking Language Features as an example, the core steering goal is to increase redundancy.
At _Level 1 (L1)_, the model is guided to express the general intent “Increase redundancy”, shifting from “Concise
phrasing” to “Elaborative repetition”. At _Level 2 (L2)_, the steering specifies a strategy for realization, moving from a
“Single expression” to a “Rephrased restatement”. At _Level 3 (L3)_, atomic, verifiable markers are enforced, requiring
the inclusion of “(i.e.,”. These examples illustrate how each level progressively constrains model outputs from
abstract intent to concrete surface evidence. Further details are provided in §3.



level hierarchy that separates inter-domain from
intra-domain specification. We synthesize multidomain data with an automated pipeline, mitigate
concept leakage through question rewriting, and ensure preference reliability using paired samples and
a two-stage quality-control process that combines
automated filtering with manual review.


**3.2** **Granularity Hierarchy Design**


Steering is often evaluated against a single “target
concept,” yet real-world control objectives vary
in granularity, from high-level intent to concrete
surface constraints. Crucially, success at a coarse
level does not guarantee success at finer levels.

We posit that this disparity arises because behavioral concepts occupy different depths within
a model’s internal hierarchy. Personality reflects
higher-level, enduring dispositional priors; sentiment captures intermediate, context-dependent affective tendencies; and language features shape
lower-level surface realizations. Moreover, each
domain contains its own internal gradations, forming a hierarchy of increasingly specific attributes.

Guided by this view, we construct our benchmark across three domains, i.e., personality, senti


ment, and language features, and organize each concept into a three-level granularity hierarchy. This
design allows us to systematically probe where
steering methods remain robust and where they begin to break down. Figure 2 shows representative
instances across domains and levels.


**Level** **1** **(L1)** **Computational** **Level.** L1 specifies **what to express** by defining high-level steering intent without constraining surface realization.
This level permits diverse outputs and tests whether
a method reliably biases behavior toward the intended direction. As shown in Figure 2, L1 objectives include autonomy (Personality), high enthusiasm (Sentiment), or increased redundancy (Language Features), shifting outputs along the target
dimension without prescribing realization.


**Level** **2** **(L2)** **Algorithmic** **Level.** L2 specifies
**how to express the intent** by specifying realization strategy while preserving L1’s objective, testing whether steering controls manner of expression rather than only target direction. Figure 2
shows representative L2 cases. In Personality, the
L2 objective is “Express autonomy through selfdirected choice”, shifting from “defer to others” to


“decisions are self-made”. In Sentiment, the L2
objective is “Use celebratory emphasis”, moving
from “neutral praise” to “energized praise”. In Language Features, L2 focuses on “Immediate paraphrase”, transitioning from “single expression” to
“rephrased restatement”.


**Level** **3** **(L3)** **Implementational** **Level.** L3 defines **how to instantiate the expression** by turning L2 strategy into atomic, verifiable surface
constraints, imposng the finest-grained control requirements. Figure 2 illustrates representative L3
cases. In Personality, the L3 objective is “Use
self-authored to instantiate autonomy”, where
the original output contains “no self-authored”
and the steered output “includes self-authored”.
In Sentiment, the L3 objective is “Use hooray to
express enthusiasm”, shifting from “no hooray”
to “includes hooray”. In Language Features, the
L3 objective is “Use (i.e., to instantiate immediate paraphrase”, moving from “no (i.e.,” to
“includes (i.e.,”. While these constraints provide
unambiguous evidence of realization, they may interfere with instruction following, making L3 the
most strictest setting.
Overall, L1 _→_ L3 progresses from intention, to
strategy, to verifiable evidence, enabling a more diagnostic evaluation of steering robustness, as summarized in Table 1.


Level Frequency Abstraction Description


L1 High Highest What to express
L2 Medium Moderate How to express it
L3 Low Lowest How to instantiate it


Table 1: Relationship between granularity levels, their
typical occurrence frequency in natural text, and abstraction. Finer-grained targets are less frequent and
less abstract, but more directly verifiable.


**3.3** **Automated Data Synthesis Pipeline**


We construct the benchmark via a fully automated,
multi-stage synthesis pipeline (Figure 3). It comprises three stages:


**Hierarchical** **Concept** **Synthesis.** As Step 1
in Figure 3 illustrates, users provide or randomly sample a domain_name. Conditioned on
this identifier, an LLM generates a bounded
domain_description that defines the domain
scope and delineates neighboring domains, which
is used as a global constraint for subsequent generations (Appendix D.1). Given the domain_name,
domain_description, and a target data quantity,



we then synthesize a three-level concept hierarchy
(L1 _∼_ L3) with explicit granularity separation and
concrete L3 constraints (Appendix D.2); formal
definitions of granularity levels are in Section 3.2.


**Question Generation and Refine.** As Step 2 in
Figure 3 shows, for each concept we generate a
diverse set of concept-conditioned questions with a
fixed train/test split, together with an anchor question and its reference (positive, negative) answers to
calibrate style and difficulty (Appendix D.3). To reduce artifacts where question phrasing cues the target concept, we then rewrite each question by pivoting it toward a related-but-distinct concept while
preserving the domain context (Appendix D.4).


**Paired** **Answer** **Generation.** As Step 3 in Figure 3 shows, we generate a contrastive answer
pair for each rewritten question: a matching
answer that satisfies the target concept and a
not_matching answer that exhibits the opposite
behavior. The pair is constrained to be minimally
edited at the lexical level to maximize structural
overlap and isolate concept-bearing differences
(Appendix D.5).


**3.4** **Quality Assurance**


To ensure data quality, we implemented a two-stage
quality assurance framework combining automated
validation with structured manual review.
**Stage 1:** **Automated Validation.** This stage focuses on format and size consistency during data
generation. Since large language models may not
satisfy all constraints in a single pass, multiple
candidate outputs are generated per task. These
candidates undergo automated format and integrity
checks, after which the validated subset is truncated in sequence to match the target size, ensuring
standardized data structures and accurate scaling.
**Stage** **2:** **Manual** **Group** **Review.** This stage
ensures semantic fidelity and label accuracy. Professional NLP annotators are assigned by domain
and granularity, following a standardized workflow:
guideline familiarization, calibration on a random
_∼_ 20% subset, dual independent verification with
consensus, and collective resolution of flagged issues. This process reduces subjectivity, improves
consistency, and ensures high-quality domain, granularity, and preference annotations. **All data are**
**vetted** **for** **privacy** **and** **security** **by** **an** **internal**
**review** **committee** . And we released the dataset
under the **MIT License** .


Figure 3: Automated data synthesis pipeline.







Figure 4: The hierarchical structure and sample distribution of our dataset.


**3.5** **Dataset Statistics**


The dataset was constructed via the automated
synthesis pipeline described above and manually validated for quality. It is a paired preference dataset structured around 3 primary domains: Personality, Sentiment, and Language
Features. Reflecting the Marr-inspired hierarchy,
each domain is organized into three granularity levels (Level 1, Level 2, Level 3), with each level
comprising 8 independent concepts. For each concept, the dataset provides 70 training, 30 test, and
5 validation samples. Each sample consists of
a question paired with a matching and a nonmatching answer. In total, the core benchmark
contains 7 _,_ 560 samples. The detailed distribution
across domains and granularity levels is provided
in Figure 4. Additionally, a specialized domain focused on Reasoning Patterns was independently
constructed to test logic-specific steering; details
for this domain are available in Appendix B.


**3.6** **Fields and Usage Specifications**


As shown in Figure 7 at Appebdix A, the domain
and domain_description define the broader data
category and its explanatory scope. Under
this hierarchy, the concept, concept_id, and



concept_description fields characterize the specific relevant concepts and their descriptions pertaining to that domain. The question field serves
as the specific probe designed to elicit this concept. Finally, for steering purposes, matching
and not_matching correspond to responses that
strictly adhere to or deviate from the target
concept, respectively.


**4** **Experiments**


**4.1** **Experiment Settings**


**Models** **and** **Steering** **Methods.** We evaluate
on Gemma-2-9B-Instruct (Team, 2024a), Qwen2.5-7B-Instruct (Team, 2024c), and Llama-3.1-8BInstruct (Team, 2024b). For prompt-based baselines, we use 0-shot Prompt (Wu et al., 2025b)
and 3-shot Prompt. For activation-based steering
baselines, we include PCA, DiffMean (Marks and
Tegmark, 2023), and RePS (Wu et al., 2025c). We
also report Vanilla (no steering). Detailed hyperparameter are provided in Appendix B.


**Evaluation.** All methods are tested in an openended generation setting. Methods that do not require a steering factor, namely Vanilla, Prompt (0shot), are evaluated directly on the test set. In the
Prompt (3-shot) setting, 3 preference pairs are randomly sampled from the training set as in-context
demonstrations. For PCA, DiffMean, and RePS,
the steering factor is searched on the validation set
to find the optimal scaling value, which is then applied for generation and evaluation on the test set.
For each steering concept, we use gpt-4.1-mini
to score model responses on a 5-point scale in
_{_ 0 _,_ 1 _,_ 2 _,_ 3 _,_ 4 _}_ along three dimensions: (i) a **Con-**
**cept Score** measuring how accurately the output
conveys the intended concept, (ii) an **Instruction**
**Score** measuring how well it follows the instruc

**Language Features** **Personality** **Sentiment**
**Method**

L1 L2 L3 L1 L2 L3 L1 L2 L3


CS HM CS HM CS HM CS HM CS HM CS HM CS HM CS HM CS HM


**Gemma-2-9b-Instruct**
Vanilla 1.16 1.38 0.95 1.14 0.14 0.15 0.45 0.58 0.79 1.01 0.05 0.06 1.40 1.61 1.18 1.40 0.00 0.00

PCA 1.94 1.85 1.45 1.51 0.13 0.15 1.33 1.48 1.51 1.20 0.05 0.06 1.86 2.01 1.68 1.75 0.00 0.00
DiffMean **3.12** **2.98** 2.70 2.78 0.14 0.14 **3.16** **3.10** 3.17 3.10 0.05 0.05 2.79 2.92 2.83 2.68 0.07 0.08
RePS 2.87 2.82 2.36 2.16 2.07 2.00 3.15 3.04 **3.63** **3.48** 2.34 2.12 **3.27** 3.21 2.75 2.53 1.65 1.64


**Qwen-2.5-7b-Instruct**
Vanilla 0.75 0.93 0.68 0.81 0.10 0.11 0.39 0.52 0.73 0.95 0.06 0.07 0.86 1.05 0.83 1.01 0.00 0.00

PCA 1.82 1.95 1.35 1.55 0.08 0.09 1.62 1.70 1.18 1.28 0.07 0.07 1.37 1.38 1.13 1.29 0.03 0.03
DiffMean 2.80 2.76 2.50 2.54 0.30 0.33 **2.77** 2.78 3.00 3.07 0.07 0.07 2.44 2.54 2.25 2.49 0.01 0.01
RePS **3.11** **2.90** 2.72 2.60 1.43 1.22 2.70 2.70 3.05 3.16 0.82 0.71 **2.93** 2.76 2.48 2.46 1.25 1.11


**Llama-3.1-8B-Instruct**
Vanilla 0.81 0.99 0.75 0.89 0.12 0.13 0.38 0.52 0.75 0.95 0.05 0.06 1.09 1.31 0.91 1.05 0.01 0.01
Prompt (0-shot) 2.61 2.74 3.01 3.14 1.89 2.10 2.07 2.46 2.92 3.14 3.00 3.36 3.12 3.34 2.93 3.09 2.38 2.69
Prompt (3-shot) **3.01** **3.20** **3.41** **3.53** **2.86** **3.15** 2.88 **3.25** 3.38 **3.55** **3.16** **3.44** **3.21** **3.54** **3.26** **3.42** **2.71** **3.04**
PCA 2.31 2.06 1.72 1.63 0.30 0.31 1.34 1.27 1.30 1.44 0.06 0.06 1.26 1.39 1.80 1.78 0.03 0.03
DiffMean 2.79 2.83 2.89 3.00 0.41 0.39 2.51 2.58 2.87 2.99 0.07 0.08 2.64 2.62 2.43 2.51 0.00 0.00


Table 2: Performance across domains, granularity levels, and metrics. Each domain includes three granularity levels
L1 to L3. We report Concept Score (CS) on a 0–4 scale and Harmonic Mean (HM) on the same scale. HM is
the harmonic mean of Concept Score, Instruction Score, and Fluency Score. **Best** and second-best results are
highlighted within each model block.



tion, and (iii) a **Fluency Score** measuring linguistic
quality, coherence, and readability; we additionally
report an aggregate score given by the **harmonic**
**mean (HM)** of these three scores to downweight
low performance in any single dimension.


**4.2** **Main Results**


We present main results in Table 2, subsequently
with overall, level-wise, and domain-wise analysis.


**Overall** **comparison.** **Prompt-based** **steering**
**outperforms** **activation-based** **steering** **overall.**
We evaluate overall performance by computing the
harmonic mean (HM) averaged over _all domains_
and _all levels_ . On Gemma-2-9B-Instruct, Prompt
(0/3-shot) achieves HM=3.10/3.12, substantially
higher than activation-based methods (PCA 1.11,
DiffMean 1.98, RePS 2.56) and Vanilla (0.81); consistent conclusions are observed on Qwen-2.5-7BInstruct and Llama-3.1-8B-Instruct as well. Moreover, few-shot further improves prompting. Within
activation-based methods, **RePS, which directly**
**trains a steering vector from data, is consistently**
**stronger than the training-free baselines PCA**
**and DiffMean**, but still trails prompting overall, in
line with prior findings (Wu et al., 2025c).



**Level-wise analysis.** Averaged across domains,
**activation-based** **steering** **is** **highly** **sensitive**
**to** **concept** **granularity** . On Gemma-2-9BInstruct, the harmonic mean (HM) for activationbased methods (PCA/DiffMean/RePS) drops from
1.67/2.76/2.94 at L1 to 0.05/0.07/1.72 at L3. As
the target specification becomes finer (L1 _→_ L3),
performance degrades sharply, consistent with the
intuition that finer levels require deeper processing in Marr’s hierarchy. In contrast, **prompt-based**
**steering is strong and stable** across all levels, with
HM staying around 3.0 from L1 to L3. We observe
similar trends on Qwen-2.5-7B-Instruct and Llama3.1-8B-Instruct. Notably, **activation-based meth-**
**ods can match or even outperform prompting at**
**the coarsest level (L1)**, contrasting with prior findings (Wang et al., 2025). However, they fall behind
substantially at L2 and L3, and the gap widens as
granularity increases, which also helps explain why
prompt-based steering often dominates activationbased steering on AXBENCH (Wu et al., 2025b).


**Domain-wise analysis.** In the level-averaged results, **prompt-based steering remains strong and**
**stable** across all three models, with HM consistently around 3.0. In contrast, **activation-based**
**steering exhibits clear domain dependence** . Using RePS as an example, averaged over the three


(a) Few-Shot Analysis (b) Steering Strength


Figure 5: Experimental results in terms of few-shot analysis and steering strength.



models, it attains the highest HM on personality
at approximately 2.43, followed by sentiment at
approximately 2.37, and language features at approximately 2.25. Overall, these trends support
our hypothesis that personality, sentiment, and language features in our benchmark can be interpreted
through Marr’s three levels of analysis: different domains impose different steering demands,
and activation-based interventions transfer less uniformly across domains than prompting.


**5** **Analysis**


**5.1** **Scaling with In-Context Shots**


We study how the number of in-context demonstrations affects prompt-based steering. Figure 5a
shows trends from 0-shot to 16-shot for representative concept–domain pairs, covering coarsegrained (L1/L2) and fine-grained (L3) targets. For
L1/L2, a few demonstrations often yield most of
the gains and then saturate, consistent with fewshot prompting helping the model infer the intended task and disambiguate underspecified instructions (Brown et al., 2020; Min et al., 2022).
For L3, adding more shots is typically less helpful
and can even hurt, plausibly because extra examples introduce idiosyncratic surface cues that increase shortcut matching or interfere with alreadytight constraints (Min et al., 2022). This coarse-tofine difference is also broadly compatible with hierarchical accounts of cognition (Botvinick, 2008;
Miller et al., 2017).


**5.2** **Scaling with the Steering Strength**


We study how the _steering factor_ affects activationbased steering. Figure 5b reports Concept, Instruction, Fluency, and Harmonic Mean for RePS and
DiffMean on Qwen-2.5-7B-Instruct across multiple factor settings, covering L1 _∼_ L3 concepts in
both Language Features and Personality.



Overall, increasing the steering factor tends to
improve Concept Score, but beyond a certain range
it can noticeably reduce Instruction following and
Fluency, leading to a peak in Harmonic Mean at
moderate strengths. This reflects a **trade-off** between **concept enforcement** and **general capabil-**
**ity retention**, consistent with prior findings (Tigges
et al., 2023; Zou et al., 2023; Durmus et al., 2024;
Taimeskhanov et al., 2026). Further, the effect
is clearest for L1. Coarse-grained targets often
yield cleaner and more consistent steering directions, and scaling the steering factor provides an
additional degree of freedom to strengthen concept
transfer (Mikolov et al., 2013; Pennington et al.,
2014), which can outperform prompting when wellcalibrated. For L2/L3, trends are less consistent
and gains are smaller, indicating that the activationbased methods we evaluate do not reliably deliver
fine-grained control under stronger specification
constraints.


**5.3** **Case Study**


Figure 6 shows a representative concept instantiated at three granularity levels and the corresponding model outputs under different steering methods. The examples illustrate that our levels capture
different control requirements, and that steering
behavior changes systematically with granularity.


**L1 is typically easy to steer without harming gen-**
**eral quality.** At **L1**, the target is coarse-grained
concept guidance. As shown in Figure 6, steering can often be applied smoothly across prompts,
enhancing concept expression while largely preserving instruction following and fluency. This
aligns with prior evidence that inference-time interventions can control high-level output properties
such as topic and sentiment while preserving performance on off-target tasks (Turner et al., 2023).


### Target ： Be enthusiastic



















Figure 6: Detailed Case Study.



**L2 exposes a trade-off between concept realiza-**
**tion and general capabilities.** At **L2**, the target
constrains the _manner_ of expression. The cases in
Figure 6 reveal a recurring tension between concept guidance and instruction following. Some retain strong instruction following and fluent answers
but fail to realize the concept in the specified way,
whereas others achieve the desired style only by
sacrificing instruction adherence or fluency, similar
to observations by Li et al. (2023).


**L3 remains difficult even when sacrificing gen-**
**eral** **capabilities.** At **L3**, the target becomes a
token-level constraint that is directly checkable.
Figure 6 shows that most steering methods struggle
to satisfy this fine-grained requirement. Notably,
even when steering is strengthened and general capabilities degrade, the concept score often remains
low, suggesting that atomic constraint satisfaction
is substantially harder than L1 _∼_ L2 steering.


**6** **Related Work**


Steering includes many techniques, two common
ones are **prompt-based** steering, which uses carefully designed instructions or examples to guide
generation (Perez et al., 2023; Han et al., 2024;
Wu et al., 2025b), and **activation-based** steering, which intervenes on hidden activations using
learned concept directions (Rimsky et al., 2024;
Pres et al., 2024; Arditi et al., 2025; Han et al.,
2025; Bartoszcze et al., 2025; Zhu et al., 2025;
Zhang et al., 2025; Bayat et al., 2025; Chen et al.,
2025b; Wu et al., 2025a; Sun et al., 2025; Sheng



et al., 2025; Bigelow et al., 2025; Zhang et al.,
2026; Xu et al., 2026; Sarfati et al., 2026; Park
et al., 2026; Beaglehole et al., 2026). For activationbased steering, _training-free_ methods such as PCA
and DiffMean (Marks and Tegmark, 2023) estimate directions from representation statistics, while
_training-based_ methods (Wu et al., 2024; Cao et al.,
2024) such as RePS (Wu et al., 2025c) learn directions with a preference-style objective.


However, these methods are often evaluated on
**limited behaviors or small task sets**, such as sentiment, safety, and personas (Han et al., 2024; Farooq
et al., 2025; Tak et al., 2025; Siu et al., 2025; Han
et al., 2025; Wang et al., 2025; Arditi et al., 2025;
Sangayya Hiremath et al., 2026). AXBENCH
improves cross-method comparability, but its concepts are derived from Sparse Autoencoder (SAE)
features (Bricken et al., 2023; Templeton et al.,
2024; Gao et al., 2024; Huben et al., 2024; Shu
et al., 2025), which are often fine-grained and not
organized by domain or granularity. Moreover,
its evaluation prompts are sampled rather than designed to test specific concepts (Wu et al., 2025b).
STEER-BENCH (Chen et al., 2025a) studies intrinsic model steerability, rather than providing a
benchmark for comparing steering methods. Overall, whether model behavior can be controlled _sys-_
_tematically,_ _predictably,_ _and_ _in_ _a_ _hierarchically_
_structured way_ remains open; answering it requires
a **hierarchical steering benchmark** that enables
evaluation across concept levels and analysis of
how steering affects levels of model behavior.


**7** **Conclusion**


We introduce _SteerEval_, a hierarchical benchmark
for evaluating LLM steering across behavioral domains and levels of concept granularity using highquality synthetic preference data. Our results show
that steering performance degrades in a systematic and predictable manner as control objectives
become deeper and more tightly specified, revealing clear boundaries and failure modes of existing methods. By making these limits explicit,
SteerEval provides a principled foundation for developing more reliable, robust and interpretable
approaches to behavioral control in LLMs.


**Limitations**


Despite our best efforts, some aspects remain beyond the scope of this paper.
_Coverage of concepts and domains._ We instantiate our hierarchy in a limited set of settings (e.g.,
Language Features and Personality). While the
pipeline is extensible, we do not cover multi-turn dialogue, tool use, long-context interaction, or safetycritical domains; extending to these settings is left
to future work.
_Experimental_ _setting._ We study single-turn
prompts and single-concept control. We do not
test multi-turn dialogue, composition of multiple
concepts, or sequential/iterative steering, which are
common in real use.
_Method tuning._ Steering results depend on extraction choices (layer, data pairing) and coefficient
selection. While we sweep strengths, we do not
claim optimal tuning for every concept, especially
at L2/L3.
_LLM-as-a-judge._ We rely on LLM-based evaluation for Concept/Instruction/Fluency. Such judges
can be biased and sensitive to prompting, and may
over/under-credit fine-grained compliance. Scores
should be read as approximate signals rather than
definitive ground truth.


**Ethics Statement**


Our benchmark characterizes controllability boundaries of LLMs across domains and granularity levels; however, its extensible pipeline implies misuse risk, so we recommend safety monitoring and
capability-retention checks in deployment. We do
not collect or include personal data in our benchmark. Overall, we do not anticipate significant
ethical or societal impacts from this work.



**References**


Usman Anwar, Abulhair Saparov, Javier Rando, Daniel
Paleka, Miles Turpin, Peter Hase, Ekdeep Singh
Lubana, Erik Jenner, Stephen Casper, Oliver Sourbut,
Benjamin L. Edelman, Zhaowei Zhang, Mario Günther, Anton Korinek, José Hernández-Orallo, Lewis
Hammond, Eric J. Bigelow, Alexander Pan, Lauro
Langosco, Tomasz Korbak, Heidi Zhang, Ruiqi
Zhong, Seán Ó hÉigeartaigh, Gabriel Recchia, Giulio
Corsi, Alan Chan, Markus Anderljung, Lilian Edwards, Yoshua Bengio, Danqi Chen, Samuel Albanie,
Tegan Maharaj, Jakob N. Foerster, Florian Tramèr,
He He, Atoosa Kasirzadeh, Yejin Choi, and David
Krueger. 2024. Foundational [challenges](https://doi.org/10.48550/ARXIV.2404.09932) in assur[ing alignment and safety of large language models.](https://doi.org/10.48550/ARXIV.2404.09932)
_CoRR_, abs/2404.09932.


Andy Arditi, Owain Evans, and Jack Lindsey.
2025. Persona vectors: Monitoring and controlling character traits in language models.
_http://arxiv.org/abs/2507.21509_ .


David Badre. 2025. [Cognitive control.](https://doi.org/10.1146/annurev-psych-022024-103901) _Annual Review_
_of Psychology_, 76(Volume 76, 2025):167–195.


Lukasz Bartoszcze, Sarthak Munshi, Bryan Sukidi, Jennifer Yen, Zejia Yang, David Williams-King, Linh
Le, Kosi Asuzu, and Carsten Maple. 2025. [Represen-](https://doi.org/10.48550/ARXIV.2502.17601)
[tation engineering for large-language models: Survey](https://doi.org/10.48550/ARXIV.2502.17601)
[and research challenges.](https://doi.org/10.48550/ARXIV.2502.17601) _CoRR_, abs/2502.17601.


Reza Bayat, Ali Rahimi-Kalahroudi, Mohammad
Pezeshki, Sarath Chandar, and Pascal Vincent. 2025.
[Steering large language model activations in sparse](https://doi.org/10.48550/ARXIV.2503.00177)
[spaces.](https://doi.org/10.48550/ARXIV.2503.00177) _CoRR_, abs/2503.00177.


Daniel Beaglehole, Adityanarayanan Radhakrishnan,
Enric Boix-Adsera, and Mikhail Belkin. 2026. Toward universal steering and monitoring of ai models.
_Science_, 391(6787):787–792.


Eric J. Bigelow, Daniel Wurgaft, YingQiao Wang,
Noah D. Goodman, Tomer D. Ullman, Hidenori
Tanaka, and Ekdeep Singh Lubana. 2025. [Belief](https://doi.org/10.48550/ARXIV.2511.00617)
[dynamics reveal the dual nature of in-context learn-](https://doi.org/10.48550/ARXIV.2511.00617)
[ing and activation steering.](https://doi.org/10.48550/ARXIV.2511.00617) _CoRR_, abs/2511.00617.


Matthew Botvinick and Todd Braver. 2015. [Motivation](https://doi.org/10.1146/annurev-psych-010814-015044)
and cognitive control: [From behavior to neural mech-](https://doi.org/10.1146/annurev-psych-010814-015044)
[anism.](https://doi.org/10.1146/annurev-psych-010814-015044) _Annual Review of Psychology_, 66(Volume 66,
2015):83–113.


Matthew M Botvinick. 2008. Hierarchical models of
behavior and prefrontal function. _Trends in cognitive_
_sciences_, 12(5):201–208.


Trenton Bricken, Adly Templeton, Joshua Batson,
Brian Chen, Adam Jermyn, Tom Conerly, Nick
Turner, Cem Anil, Carson Denison, Amanda Askell,
Robert Lasenby, Yifan Wu, Shauna Kravec, Nicholas
Schiefer, Tim Maxwell, Nicholas Joseph, Zac
Hatfield-Dodds, Alex Tamkin, Karina Nguyen,
Brayden McLean, Josiah E Burke, Tristan Hume,
Shan Carter, Tom Henighan, and Christopher


Olah. 2023. Towards monosemanticity: Decomposing language models with dictionary learning.
_Transformer_ _Circuits_ _Thread_ . Https://transformercircuits.pub/2023/monosemanticfeatures/index.html.


Tom B. Brown, Benjamin Mann, Nick Ryder, Melanie
Subbiah, Jared Kaplan, Prafulla Dhariwal, Arvind
Neelakantan, Pranav Shyam, Girish Sastry, Amanda
Askell, Sandhini Agarwal, Ariel Herbert-Voss,
Gretchen Krueger, Tom Henighan, Rewon Child,
Aditya Ramesh, Daniel M. Ziegler, Jeffrey Wu,
Clemens Winter, Christopher Hesse, Mark Chen, Eric
Sigler, Mateusz Litwin, Scott Gray, Benjamin Chess,
Jack Clark, Christopher Berner, Sam McCandlish,
Alec Radford, Ilya Sutskever, and Dario Amodei.
2020. [Language models are few-shot learners.](https://proceedings.neurips.cc/paper/2020/hash/1457c0d6bfcb4967418bfb8ac142f64a-Abstract.html) In _Ad-_
_vances in Neural Information Processing Systems 33:_
_Annual Conference on Neural Information Process-_
_ing_ _Systems_ _2020,_ _NeurIPS_ _2020,_ _December_ _6-12,_
_2020, virtual_ .


Yuanpu Cao, Tianrong Zhang, Bochuan Cao, Ziyi Yin,
Lu Lin, Fenglong Ma, and Jinghui Chen. 2024. [Per-](http://papers.nips.cc/paper_files/paper/2024/hash/58cbe393b4254da8966780a40d023c0b-Abstract-Conference.html)
[sonalized steering of large language models:](http://papers.nips.cc/paper_files/paper/2024/hash/58cbe393b4254da8966780a40d023c0b-Abstract-Conference.html) Versa[tile steering vectors through bi-directional preference](http://papers.nips.cc/paper_files/paper/2024/hash/58cbe393b4254da8966780a40d023c0b-Abstract-Conference.html)
[optimization.](http://papers.nips.cc/paper_files/paper/2024/hash/58cbe393b4254da8966780a40d023c0b-Abstract-Conference.html) In _Advances_ _in_ _Neural_ _Information_
_Processing Systems 38:_ _Annual Conference on Neu-_
_ral Information Processing Systems 2024, NeurIPS_
_2024,_ _Vancouver,_ _BC,_ _Canada,_ _December_ _10_ _-_ _15,_
_2024_ .


Kai Chen, Zihao He, Taiwei Shi, and Kristina Lerman.
2025a. Steer-bench: A benchmark for evaluating the
steerability of large language models. _arXiv preprint_
_arXiv:2505.20645_ .


Runjin Chen, Zhenyu Zhang, Junyuan Hong, Souvik
Kundu, and Zhangyang Wang. 2025b. [SEAL: steer-](https://doi.org/10.48550/ARXIV.2504.07986)
[able reasoning calibration of large language models](https://doi.org/10.48550/ARXIV.2504.07986)
[for free.](https://doi.org/10.48550/ARXIV.2504.07986) _CoRR_, abs/2504.07986.


Yann Dubois, Balázs Galambosi, Percy Liang, and Tatsunori B. Hashimoto. 2024. [Length-controlled](https://doi.org/10.48550/ARXIV.2404.04475) alpacaeval: [A simple way to debias automatic evalua-](https://doi.org/10.48550/ARXIV.2404.04475)
[tors.](https://doi.org/10.48550/ARXIV.2404.04475) _CoRR_, abs/2404.04475.


Esin Durmus, Alex Tamkin, Jack Clark, Jerry Wei,
Jonathan Marcus, Joshua Batson, Kunal Handa,
Liane Lovitt, Meg Tong, Miles McCain, Kunal
Handa, Liane Lovitt, Meg Tong, Miles McCain,
Oliver Rausch, Saffron Huang, Sam Bowman, Stuart Ritchie, Tom Henighan, and Deep Ganguli. 2024.
[Evaluating feature steering:](https://anthropic.com/research/evaluating-feature-steering) A case study in mitigat[ing social biases.](https://anthropic.com/research/evaluating-feature-steering)


Misbah Farooq, Varuna De Silva, Rahul Rahulamathavan, and Xiyu Shi. 2025. [Sentiment steering in large](https://doi.org/10.1109/DSP65409.2025.11075111)
[language models via activation vector manipulation.](https://doi.org/10.1109/DSP65409.2025.11075111)
In _DSP_, pages 1–5. IEEE.


Leo Gao, Tom Dupré la Tour, Henk Tillman, Gabriel
Goh, Rajan Troll, Alec Radford, Ilya Sutskever, Jan
Leike, and Jeffrey Wu. 2024. [Scaling and evaluating](https://doi.org/10.48550/ARXIV.2406.04093)
[sparse autoencoders.](https://doi.org/10.48550/ARXIV.2406.04093) _CoRR_, abs/2406.04093.



Chi Han, Jialiang Xu, Manling Li, Yi Fung, Chenkai
Sun, Nan Jiang, Tarek F. Abdelzaher, and Heng Ji.
2024. [Word embeddings are steers for language mod-](https://doi.org/10.18653/V1/2024.ACL-LONG.864)
[els.](https://doi.org/10.18653/V1/2024.ACL-LONG.864) In _Proceedings of the 62nd Annual Meeting of_
_the Association for Computational Linguistics (Vol-_
_ume 1:_ _Long Papers), ACL 2024, Bangkok, Thailand,_
_August 11-16,_ _2024_, pages 16410–16430. Association for Computational Linguistics.


Peixuan Han, Cheng Qian, Xiusi Chen, Yuji Zhang,
Denghui Zhang, and Heng Ji. 2025. [Internal](https://doi.org/10.48550/ARXIV.2502.01042) activation as the polar star for steering unsafe LLM
[behavior.](https://doi.org/10.48550/ARXIV.2502.01042) _CoRR_, abs/2502.01042.


Robert Huben, Hoagy Cunningham, Logan Riggs,
Aidan Ewart, and Lee Sharkey. 2024. [Sparse autoen-](https://openreview.net/forum?id=F76bwRSLeK)
[coders find highly interpretable features in language](https://openreview.net/forum?id=F76bwRSLeK)
[models.](https://openreview.net/forum?id=F76bwRSLeK) In _The_ _Twelfth_ _International_ _Conference_
_on_ _Learning_ _Representations,_ _ICLR_ _2024,_ _Vienna,_
_Austria, May 7-11, 2024_ . OpenReview.net.


Shawn Im and Yixuan Li. 2025. A [unified](https://doi.org/10.48550/ARXIV.2502.02716) under[standing and evaluation of steering methods.](https://doi.org/10.48550/ARXIV.2502.02716) _CoRR_,
abs/2502.02716.


Kenneth Li, Oam Patel, Fernanda B. Viégas, Hanspeter
Pfister, and Martin Wattenberg. 2023. [Inference-time](http://papers.nips.cc/paper_files/paper/2023/hash/81b8390039b7302c909cb769f8b6cd93-Abstract-Conference.html)
intervention: [Eliciting truthful answers from a lan-](http://papers.nips.cc/paper_files/paper/2023/hash/81b8390039b7302c909cb769f8b6cd93-Abstract-Conference.html)
guage model. In _Advances_ _in_ _Neural_ _Information_
_Processing Systems 36:_ _Annual Conference on Neu-_
_ral Information Processing Systems 2023, NeurIPS_
_2023,_ _New_ _Orleans,_ _LA,_ _USA,_ _December_ _10_ _-_ _16,_
_2023_ .


Tom Lieberum, Senthooran Rajamanoharan, Arthur
Conmy, Lewis Smith, Nicolas Sonnerat, Vikrant
Varma, János Kramár, Anca D. Dragan, Rohin Shah,
and Neel Nanda. 2024. [Gemma scope:](https://doi.org/10.48550/ARXIV.2408.05147) Open sparse
autoencoders [everywhere](https://doi.org/10.48550/ARXIV.2408.05147) all at once on gemma 2.
_CoRR_, abs/2408.05147.


Aleksandar Makelov. 2024. Sparse autoencoders match
supervised features for model steering on the ioi
task. In _ICML 2024 Workshop on Mechanistic Inter-_
_pretability_ .


Samuel Marks and Max Tegmark. 2023. [The geometry](https://doi.org/10.48550/ARXIV.2310.06824)
of truth: [Emergent linear structure in large language](https://doi.org/10.48550/ARXIV.2310.06824)
[model representations of true/false datasets.](https://doi.org/10.48550/ARXIV.2310.06824) _CoRR_,
abs/2310.06824.


David Marr. 1982. _Vision:_ _A computational investiga-_
_tion into the human representation and processing of_
_visual information_ . MIT press.


Tomás Mikolov, Wen-tau Yih, and Geoffrey Zweig.
2013. Linguistic [regularities](https://aclanthology.org/N13-1090/) in continuous space
[word representations.](https://aclanthology.org/N13-1090/) In _Human Language Technolo-_
_gies:_ _Conference of the North American Chapter of_
_the Association of Computational Linguistics,_ _Pro-_
_ceedings, June 9-14, 2013, Westin Peachtree Plaza_
_Hotel, Atlanta, Georgia, USA_, pages 746–751. The
Association for Computational Linguistics.


George A Miller, Galanter Eugene, and Karl H Pribram.
2017. Plans and the structure of behaviour. In _Sys-_
_tems research for behavioral science_, pages 369–382.
Routledge.


Sewon Min, Xinxi Lyu, Ari Holtzman, Mikel Artetxe,
Mike Lewis, Hannaneh Hajishirzi, and Luke Zettlemoyer. 2022. [Rethinking the role of demonstrations:](https://doi.org/10.18653/V1/2022.EMNLP-MAIN.759)
[What makes in-context learning work?](https://doi.org/10.18653/V1/2022.EMNLP-MAIN.759) In _Proceed-_
_ings of the 2022 Conference on Empirical Methods_
_in Natural Language Processing, EMNLP 2022, Abu_
_Dhabi, United Arab Emirates, December 7-11, 2022_,
pages 11048–11064. Association for Computational
Linguistics.


Kiho Park, Todd Nief, Yo Joong Choe, and Victor Veitch.
2026. [The information geometry of softmax:](https://arxiv.org/abs/2602.15293) Prob[ing and steering.](https://arxiv.org/abs/2602.15293) _Preprint_, arXiv:2602.15293.


Jeffrey Pennington, Richard Socher, and Christopher D.
Manning. 2014. Glove: Global [vectors](https://doi.org/10.3115/V1/D14-1162) for word
[representation.](https://doi.org/10.3115/V1/D14-1162) In _Proceedings of the 2014 Confer-_
_ence on Empirical Methods in Natural Language Pro-_
_cessing, EMNLP 2014, October 25-29, 2014, Doha,_
_Qatar, A meeting of SIGDAT, a Special Interest Group_
_of the ACL_, pages 1532–1543. ACL.


Ethan Perez, Sam Ringer, Kamile Lukosiute, Karina
Nguyen, Edwin Chen, Scott Heiner, Craig Pettit,
Catherine Olsson, Sandipan Kundu, Saurav Kadavath, Andy Jones, Anna Chen, Benjamin Mann,
Brian Israel, Bryan Seethor, Cameron McKinnon,
Christopher Olah, Da Yan, Daniela Amodei, Dario
Amodei, Dawn Drain, Dustin Li, Eli Tran-Johnson,
Guro Khundadze, Jackson Kernion, James Landis,
Jamie Kerr, Jared Mueller, Jeeyoon Hyun, Joshua
Landau, Kamal Ndousse, Landon Goldberg, Liane
Lovitt, Martin Lucas, Michael Sellitto, Miranda
Zhang, Neerav Kingsland, Nelson Elhage, Nicholas
Joseph, Noemí Mercado, Nova DasSarma, Oliver
Rausch, Robin Larson, Sam McCandlish, Scott Johnston, Shauna Kravec, Sheer El Showk, Tamera Lanham, Timothy Telleen-Lawton, Tom Brown, Tom
Henighan, Tristan Hume, Yuntao Bai, Zac HatfieldDodds, Jack Clark, Samuel R. Bowman, Amanda
Askell, Roger B. Grosse, Danny Hernandez, Deep
Ganguli, Evan Hubinger, Nicholas Schiefer, and
Jared Kaplan. 2023. Discovering [language](https://doi.org/10.18653/V1/2023.FINDINGS-ACL.847) model
[behaviors with model-written evaluations.](https://doi.org/10.18653/V1/2023.FINDINGS-ACL.847) In _Find-_
_ings of the Association for Computational Linguis-_
_tics:_ _ACL 2023, Toronto, Canada, July 9-14, 2023_,
pages 13387–13434. Association for Computational
Linguistics.


Itamar Pres, Laura Ruis, Ekdeep Singh Lubana, and
David Krueger. 2024. Towards [reliable](https://doi.org/10.48550/ARXIV.2410.17245) evaluation
of behavior steering interventions in llms. _CoRR_,
abs/2410.17245.


Nina Rimsky, Nick Gabrieli, Julian Schulz, Meg Tong,
Evan Hubinger, and Alexander Matt Turner. 2024.
[Steering llama 2 via contrastive activation addition.](https://doi.org/10.18653/V1/2024.ACL-LONG.828)
In _Proceedings_ _of_ _the_ _62nd_ _Annual_ _Meeting_ _of_ _the_
_Association for Computational Linguistics (Volume 1:_
_Long Papers), ACL 2024, Bangkok, Thailand, August_



_11-16,_ _2024_, pages 15504–15522. Association for
Computational Linguistics.


Basavaraj Sangayya Hiremath, Marco Polignano, Marco
Levantesi, Giovanni Semeraro, Ernesto William
De Luca, and Amos Poznanski. 2026. [State-wise](https://doi.org/10.1016/j.neunet.2026.108708)
linear modulation [(slim):](https://doi.org/10.1016/j.neunet.2026.108708) A novel approach for
steering large [language](https://doi.org/10.1016/j.neunet.2026.108708) models. _Neural_ _Networks_,
199:108708.


Raphaël Sarfati, Eric Bigelow, Daniel Wurgaft, Jack
Merullo, Atticus Geiger, Owen Lewis, Tom McGrath,
and Ekdeep Singh Lubana. 2026. [The shape of be-](https://arxiv.org/abs/2602.02315)
liefs: [Geometry, dynamics, and interventions along](https://arxiv.org/abs/2602.02315)
[representation manifolds of language models’ poste-](https://arxiv.org/abs/2602.02315)
[riors.](https://arxiv.org/abs/2602.02315) _Preprint_, arXiv:2602.02315.


Lee Sharkey, Bilal Chughtai, Joshua Batson, Jack Lindsey, Jeff Wu, Lucius Bushnaq, Nicholas GoldowskyDill, Stefan Heimersheim, Alejandro Ortega, Joseph
Bloom, et al. 2025. Open problems in mechanistic
interpretability. _arXiv preprint arXiv:2501.16496_ .


Leheng Sheng, Changshuo Shen, Weixiang Zhao, Junfeng Fang, Xiaohao Liu, Zhenkai Liang, Xiang Wang,
An Zhang, and Tat-Seng Chua. 2025. [Alphasteer:](https://doi.org/10.48550/ARXIV.2506.07022)
[Learning refusal steering with principled null-space](https://doi.org/10.48550/ARXIV.2506.07022)
[constraint.](https://doi.org/10.48550/ARXIV.2506.07022) _CoRR_, abs/2506.07022.


Dong Shu, Xuansheng Wu, Haiyan Zhao, Daking Rai,
Ziyu Yao, Ninghao Liu, and Mengnan Du. 2025. [A](https://aclanthology.org/2025.findings-emnlp.89/)
[survey on sparse autoencoders:](https://aclanthology.org/2025.findings-emnlp.89/) Interpreting the inter[nal mechanisms of large language models.](https://aclanthology.org/2025.findings-emnlp.89/) In _Find-_
_ings of the Association for Computational Linguistics:_
_EMNLP 2025, Suzhou, China, November 4-9, 2025_,
pages 1690–1712. Association for Computational
Linguistics.


Vincent Siu, Nicholas Crispino, David Park, Nathan W.
Henry, Zhun Wang, Yang Liu, Dawn Song, and Chenguang Wang. 2025. [Steeringsafety:](https://arxiv.org/abs/2509.13450) A systematic
[safety evaluation framework of representation steer-](https://arxiv.org/abs/2509.13450)
[ing in llms.](https://arxiv.org/abs/2509.13450)


Jiuding Sun, Sidharth Baskaran, Zhengxuan Wu,
Michael Sklar, Christopher Potts, and Atticus Geiger.
2025. Hypersteer: [Activation steering at scale with](https://doi.org/10.48550/ARXIV.2506.03292)
[hypernetworks.](https://doi.org/10.48550/ARXIV.2506.03292) _CoRR_, abs/2506.03292.


Magamed Taimeskhanov, Samuel Vaiter, and Damien
Garreau. 2026. Towards [understanding](https://arxiv.org/abs/2602.02712) steering
[strength.](https://arxiv.org/abs/2602.02712) _Preprint_, arXiv:2602.02712.


Ala N. Tak, Amin Banayeeanzade, Anahita Bolourani,
Mina Kian, Robin Jia, and Jonathan Gratch. 2025.
[Mechanistic interpretability of emotion inference in](https://aclanthology.org/2025.findings-acl.679/)
large [language](https://aclanthology.org/2025.findings-acl.679/) models. In _Findings_ _of_ _the_ _Associ-_
_ation for Computational Linguistics, ACL 2025, Vi-_
_enna, Austria, July 27 - August 1, 2025_, pages 13090–
13120. Association for Computational Linguistics.


Gemma Team. 2024a. Gemma: [Open](https://doi.org/10.48550/ARXIV.2403.08295) models
based on gemini [research](https://doi.org/10.48550/ARXIV.2403.08295) and technology. _CoRR_,
abs/2403.08295.


Llama Team. 2024b. The llama 3 [herd](https://doi.org/10.48550/ARXIV.2407.21783) of models.
_CoRR_, abs/2407.21783.


Qwen Team. 2024c. Qwen2.5: [A party of foundation](https://qwenlm.github.io/blog/qwen2.5/)
[models.](https://qwenlm.github.io/blog/qwen2.5/)


Adly Templeton, Tom Conerly, Jonathan Marcus, Jack
Lindsey, Trenton Bricken, Brian Chen, Adam Pearce,
Craig Citro, Emmanuel Ameisen, Andy Jones, Hoagy
Cunningham, Nicholas L Turner, Callum McDougall,
Monte MacDiarmid, C. Daniel Freeman, Theodore R.
Sumers, Edward Rees, Joshua Batson, Adam Jermyn,
Shan Carter, Chris Olah, and Tom Henighan. 2024.
Scaling [monosemanticity:](https://transformer-circuits.pub/2024/scaling-monosemanticity/index.html) Extracting interpretable
[features from claude 3 sonnet.](https://transformer-circuits.pub/2024/scaling-monosemanticity/index.html) _Transformer Circuits_
_Thread_ .


Curt Tigges, Curt Tigges, Oskar Hollinsworth, Curt
Tigges, Atticus Geiger, Atticus Geiger, Oskar
Hollinsworth, Neel Nanda, Neel Nanda, Atticus
Geiger, and Neel Nanda. 2023. Linear representations of sentiment [in](https://doi.org/10.48550/arxiv.2310.15154) large language models.
_http://arxiv.org/abs/2310.15154_ .


Alexander Matt Turner, Lisa Thiergart, David Udell,
Gavin Leech, Ulisse Mini, and Monte MacDiarmid.
2023. Activation addition: [Steering language models](https://doi.org/10.48550/ARXIV.2308.10248)
[without optimization.](https://doi.org/10.48550/ARXIV.2308.10248) _CoRR_, abs/2308.10248.


Mengru Wang, Ziwen Xu, Shengyu Mao, Shumin Deng,
Zhaopeng Tu, Huajun Chen, and Ningyu Zhang.
2025. [Beyond prompt engineering:](https://aclanthology.org/2025.acl-long.1139/) Robust behavior
[control in llms via steering target atoms.](https://aclanthology.org/2025.acl-long.1139/) In _Proceed-_
_ings of the 63rd Annual Meeting of the Association_
_for Computational Linguistics (Volume 1:_ _Long Pa-_
_pers), ACL 2025, Vienna, Austria, July 27 - August 1,_
_2025_, pages 23381–23399. Association for Computational Linguistics.


Lyucheng Wu, Mengru Wang, Ziwen Xu, Tri Cao, Nay
Oo, Bryan Hooi, and Shumin Deng. 2025a. [Au-](https://doi.org/10.18653/V1/2025.EMNLP-MAIN.41)
[tomating steering for safe multimodal large language](https://doi.org/10.18653/V1/2025.EMNLP-MAIN.41)
[models.](https://doi.org/10.18653/V1/2025.EMNLP-MAIN.41) In _Proceedings of the 2025 Conference on_
_Empirical Methods in Natural Language Processing,_
_EMNLP 2025, Suzhou, China, November 4-9, 2025_,
pages 792–814. Association for Computational Linguistics.


Zhengxuan Wu, Aryaman Arora, Atticus Geiger, Zheng
Wang, Jing Huang, Dan Jurafsky, Christopher D.
Manning, and Christopher Potts. 2025b. [Axbench:](https://openreview.net/forum?id=K2CckZjNy0)
Steering llms? even [simple](https://openreview.net/forum?id=K2CckZjNy0) baselines outperform
[sparse autoencoders.](https://openreview.net/forum?id=K2CckZjNy0) In _Forty-second International_
_Conference on Machine Learning, ICML 2025, Van-_
_couver,_ _BC,_ _Canada,_ _July_ _13-19,_ _2025_ . OpenReview.net.


Zhengxuan Wu, Aryaman Arora, Zheng Wang, Atticus
Geiger, Dan Jurafsky, Christopher D. Manning, and
Christopher Potts. 2024. Reft: [Representation fine-](http://papers.nips.cc/paper_files/paper/2024/hash/75008a0fba53bf13b0bb3b7bff986e0e-Abstract-Conference.html)
[tuning for language models.](http://papers.nips.cc/paper_files/paper/2024/hash/75008a0fba53bf13b0bb3b7bff986e0e-Abstract-Conference.html) In _Advances in Neural_
_Information Processing Systems 38:_ _Annual Confer-_
_ence on Neural Information Processing Systems 2024,_
_NeurIPS 2024, Vancouver, BC, Canada, December_
_10 - 15, 2024_ .


Zhengxuan Wu, Qinan Yu, Aryaman Arora, Christopher D. Manning, and Christopher Potts. 2025c. [Im-](https://doi.org/10.48550/ARXIV.2505.20809)



[proved representation steering for language models.](https://doi.org/10.48550/ARXIV.2505.20809)
_CoRR_, abs/2505.20809.


Ziwen Xu, Shuxun Wang, Kewei Xu, Haoming
Xu, Mengru Wang, Xinle Deng, Yunzhi Yao,
Guozhou Zheng, Huajun Chen, and Ningyu Zhang.
2025. Easyedit2: An [easy-to-use](https://doi.org/10.48550/ARXIV.2504.15133) steering framework for editing [large](https://doi.org/10.48550/ARXIV.2504.15133) language models. _CoRR_,
abs/2504.15133.


Ziwen Xu, Chenyan Wu, Hengyu Sun, Haiwen Hong,
Mengru Wang, Yunzhi Yao, Longtao Huang, Hui
Xue, Shumin Deng, Zhixuan Chu, Huajun Chen, and
Ningyu Zhang. 2026. [Why steering works:](https://arxiv.org/abs/2602.02343) Toward a
[unified view of language model parameter dynamics.](https://arxiv.org/abs/2602.02343)
_Preprint_, arXiv:2602.02343.


Hengyuan Zhang, Zhihao Zhang, Mingyang Wang, Zunhai Su, Yiwei Wang, Qianli Wang, Shuzhou Yuan,
Ercong Nie, Xufeng Duan, Qibo Xue, Zeping Yu,
Chenming Shang, Xiao Liang, Jing Xiong, Hui Shen,
Chaofan Tao, Zhengwu Liu, Senjie Jin, Zhiheng Xi,
Dongdong Zhang, Sophia Ananiadou, Tao Gui, Ruobing Xie, Hayden Kwok-Hay So, Hinrich Schütze,
Xuanjing Huang, Qi Zhang, and Ngai Wong. 2026.
Locate, steer, and [improve:](https://doi.org/10.48550/ARXIV.2601.14004) A practical survey of
[actionable mechanistic interpretability in large lan-](https://doi.org/10.48550/ARXIV.2601.14004)
[guage models.](https://doi.org/10.48550/ARXIV.2601.14004) _CoRR_, abs/2601.14004.


Jinghao Zhang, Yuting Liu, Wenjie Wang, Qiang Liu,
Shu Wu, Liang Wang, and Tat-Seng Chua. 2025. [Per-](https://aclanthology.org/2025.acl-long.353/)
[sonalized text generation with contrastive activation](https://aclanthology.org/2025.acl-long.353/)
[steering.](https://aclanthology.org/2025.acl-long.353/) In _Proceedings of the 63rd Annual Meet-_
_ing of the Association for Computational Linguistics_
_(Volume 1:_ _Long Papers), ACL 2025, Vienna, Austria,_
_July 27 - August 1, 2025_, pages 7128–7141. Association for Computational Linguistics.


Wayne Xin Zhao, Kun Zhou, Junyi Li, Tianyi Tang,
Xiaolei Wang, Yupeng Hou, Yingqian Min, Beichen Zhang, Junjie Zhang, Zican Dong, Yifan Du,
Chen Yang, Yushuo Chen, Zhipeng Chen, Jinhao
Jiang, Ruiyang Ren, Yifan Li, Xinyu Tang, Zikang
Liu, Peiyu Liu, Jian-Yun Nie, and Ji-Rong Wen.
2023. A survey of large language models. _CoRR_,
abs/2303.18223.


Minjun Zhu, Yixuan Weng, Linyi Yang, and Yue Zhang.
2025. [Personality alignment of large language mod-](https://openreview.net/forum?id=0DZEs8NpUH)
[els.](https://openreview.net/forum?id=0DZEs8NpUH) In _The Thirteenth International Conference on_
_Learning_ _Representations,_ _ICLR_ _2025,_ _Singapore,_
_April 24-28, 2025_ . OpenReview.net.


Andy Zou, Long Phan, Sarah Li Chen, James Campbell,
Phillip Guo, Richard Ren, Alexander Pan, Xuwang
Yin, Mantas Mazeika, Ann-Kathrin Dombrowski,
Shashwat Goel, Nathaniel Li, Michael J. Byun, Zifan
Wang, Alex Mallen, Steven Basart, Sanmi Koyejo,
Dawn Song, Matt Fredrikson, J. Zico Kolter, and
Dan Hendrycks. 2023. [Representation engineering:](https://doi.org/10.48550/ARXIV.2310.01405)
A top-down [approach](https://doi.org/10.48550/ARXIV.2310.01405) to AI transparency. _CoRR_,
abs/2310.01405.


**A** **Dataset Case**


This section presents representative dataset cases
to illustrate the structure and annotation of our data.
Figure 7 shows the field specifications of a data
entry, including domain and concept definitions,
the probing question, and contrastive responses
used for model steering.


**B** **Detailed Experimental Setup**


Following prior work (Wu et al., 2025b; Wang
et al., 2025; Bigelow et al., 2025), we apply steering at a single mid-to-late layer: the 20th, 14th, and
12th layers for Gemma-2-9B-Instruct, Qwen-2.57B-Instruct, and Llama-3.1-8B-Instruct, respectively. For PCA, DiffMean, and RePS, we search
for the optimal steering factor for each concept on
the validation set when applying the steering vector; detailed values are reported in Table 3, 4, 5,
6. And other hyperparameters are consistent with
AxBench and RePS. All experiments are conducted
using three NVIDIA A800 GPUs over the course
of one week.


**C** **Detailed Experiment Results**


Detailed experimental results for all domain across
three granularity levels (L1–L3) can be found in
Table 7, 8, 9, 10. We report the Concept Score
(CS), Instruction Score (IS), Fluency Score (FS),
and their Harmonic Mean (HM). All metrics are
evaluated on a 0–4 scale.


**D** **Automatic Data Synthesis Prompt**


**D.1** **Domain Specification Prompt**


We use the following hint template to expand domain keywords into explicit, bounded, specific domain descriptions, serving as global constraints for
subsequent data synthesis.











**D.2** **Granularity-Level Concept Synthesis**
**Prompt**


We use the following hint template to synthesize a
three-level concept hierarchy (L1-L3) with a specified domain description and a specified amount of
synthesis data.


Figure 7: Field specifications of the data entry. The domain and concept fields define the hierarchical subject
matter, which is probed by the question. Matching and not_matching serve as contrastive responses for model
steering.


**Gemma-2-9B-it** **Qwen-2.5-7B-it** **Llama-3.1-8B-it**
**Concept**

**PCA** **DiffMean** **RePS** **PCA** **DiffMean** **RePS** **PCA** **DiffMean** **RePS**


**L1_1** 3 4 10 4 4 3 4 3 7
**L2_1** 4 7 20 5 6 5 4 5 8
**L3_1** 1 1 22 1 1 8 1 1 8


**L1_2** 2 7 22 8 7 8 6 3 8
**L2_2** 4 6 10 1 8 8 1 3 3
**L3_2** 1 1 14 1 1 7 1 1 7


**L1_3** 6 7 16 8 4 6 7 7 8
**L2_3** 5 8 16 7 8 3 6 6 5
**L3_3** 1 1 10 1 1 4 1 1 3


**L1_4** 3 7 10 1 8 3 2 5 3
**L2_4** 8 4 10 1 4 4 2 3 6
**L3_4** 5 3 16 3 7 1 6 1 1


**L1_5** 6 6 14 5 5 3 5 5 5
**L2_5** 6 3 24 6 7 5 7 7 3
**L3_5** 1 1 18 1 1 3 6 6 3


**L1_6** 5 6 12 4 5 3 5 1 6
**L2_6** 7 5 12 4 3 2 6 3 5
**L3_6** 1 1 14 1 8 7 1 1 5


**L1_7** 8 8 14 5 5 3 7 4 8
**L2_7** 4 4 14 2 7 2 5 5 2
**L3_7** 1 5 10 1 4 3 1 6 1


**L1_8** 6 3 12 3 6 4 5 4 5
**L2_8** 5 6 10 5 5 4 6 5 3
**L3_8** 1 1 12 1 1 1 1 1 1


Table 3: Steering factors in the **Language Features** domain when applying steering vectors across all concepts and
models.


**Gemma-2-9B-it** **Qwen-2.5-7B-it** **Llama-3.1-8B-it**
**Concept**

**PCA** **DiffMean** **RePS** **PCA** **DiffMean** **RePS** **PCA** **DiffMean** **RePS**


**L1_1** 1 6 18 1 6 3 3 3 8
**L2_1** 1 4 10 1 5 3 4 3 4
**L3_1** 1 1 16 1 1 8 1 1 7


**L1_2** 4 5 12 1 5 2 5 4 2
**L2_2** 7 4 10 5 4 6 8 4 5
**L3_2** 1 1 18 1 1 8 1 1 1


**L1_3** 6 3 10 5 5 5 4 4 4
**L2_3** 5 3 10 4 6 2 4 4 5
**L3_3** 1 1 14 1 1 8 1 1 6


**L1_4** 4 7 18 5 6 4 1 3 6
**L2_4** 3 4 10 5 5 3 4 3 4
**L3_4** 1 1 10 1 1 1 1 1 1


**L1_5** 5 4 14 6 5 2 4 4 2
**L2_5** 4 5 12 6 5 3 4 5 6
**L3_5** 1 1 20 1 1 1 1 1 1


**L1_6** 1 4 10 6 4 1 5 4 4
**L2_6** 5 3 12 5 4 4 3 3 5
**L3_6** 1 1 16 1 1 1 1 1 1


**L1_7** 4 5 10 7 7 6 4 4 8
**L2_7** 5 7 12 8 4 5 3 3 3
**L3_7** 1 1 16 1 1 7 1 1 6


**L1_8** 3 6 10 3 6 2 3 5 6
**L2_8** 7 5 10 1 6 2 1 4 5
**L3_8** 1 5 12 1 3 1 4 2 1


Table 4: Steering factors in the **Personality** domain when applying steering vectors across all concepts and models.


**Gemma-2-9B-it** **Qwen-2.5-7B-it** **Llama-3.1-8B-it**
**Concept**

**PCA** **DiffMean** **RePS** **PCA** **DiffMean** **RePS** **PCA** **DiffMean** **RePS**


**L1_1** 7 8 10 7 6 6 5 6 1
**L2_1** 5 8 18 4 8 5 3 1 1
**L3_1** 1 1 10 8 1 1 1 1 1


**L1_2** 1 6 12 4 6 5 4 5 4
**L2_2** 4 5 10 7 3 3 4 3 3
**L3_2** 1 1 10 4 1 2 3 1 1


**L1_3** 6 7 16 6 5 2 7 2 4
**L2_3** 8 7 18 8 2 3 8 1 4
**L3_3** 1 1 14 1 1 1 1 1 8


**L1_4** 1 6 10 5 6 1 1 3 1
**L2_4** 5 1 12 6 7 4 5 2 2
**L3_4** 1 1 10 1 1 1 1 1 1


**L1_5** 4 8 16 8 8 2 5 4 1
**L2_5** 3 1 10 4 1 3 3 2 1
**L3_5** 1 1 14 1 1 6 1 1 1


**L1_6** 3 2 12 7 4 5 1 3 3
**L2_6** 4 7 12 3 7 2 4 6 3
**L3_6** 1 5 10 1 8 1 1 7 1


**L1_7** 2 1 12 8 8 6 3 3 3
**L2_7** 6 1 12 8 8 1 5 6 7
**L3_7** 1 1 18 1 1 3 1 1 1


**L1_8** 7 5 10 7 7 6 3 8 5
**L2_8** 5 6 14 6 7 1 1 6 3
**L3_8** 1 1 16 8 8 1 1 8 3


Table 5: Steering factors in the **Reasoning Patterns** domain when applying steering vectors across all concepts and
models.


**Gemma-2-9B-it** **Qwen-2.5-7B-it** **Llama-3.1-8B-it**
**Concept**

**PCA** **DiffMean** **RePS** **PCA** **DiffMean** **RePS** **PCA** **DiffMean** **RePS**


**L1_1** 1 8 12 2 8 3 7 8 8
**L2_1** 8 8 10 8 7 2 7 7 4
**L3_1** 1 6 10 1 1 1 1 1 1


**L1_2** 1 8 12 5 8 6 3 7 3
**L2_2** 5 5 14 1 8 8 8 8 4
**L3_2** 1 8 18 1 1 5 1 8 4


**L1_3** 7 6 10 3 6 3 4 3 5
**L2_3** 5 4 18 2 4 2 6 2 7
**L3_3** 1 1 12 1 1 1 1 1 1


**L1_4** 3 3 16 6 5 3 1 4 3
**L2_4** 4 5 12 1 4 3 3 2 7
**L3_4** 1 1 14 1 1 6 1 1 3


**L1_5** 4 7 16 4 2 6 1 8 4
**L2_5** 3 3 14 5 3 1 5 2 2
**L3_5** 1 1 10 5 1 4 1 2 1


**L1_6** 8 4 10 8 2 3 6 5 7
**L2_6** 7 7 14 5 3 4 5 3 7
**L3_6** 1 1 10 1 1 1 1 1 1


**L1_7** 8 8 14 5 3 3 2 4 4
**L2_7** 5 6 16 8 6 4 4 3 7
**L3_7** 1 8 24 1 7 6 1 1 1


**L1_8** 1 5 14 1 8 4 1 5 6
**L2_8** 4 4 22 1 3 2 6 5 5
**L3_8** 1 1 16 1 1 6 1 1 1


Table 6: Steering factors in the **Sentiment** domain when applying steering vectors across all concepts and models.








L1 L2 L3
**Method**


CS IS FS HM CS IS FS HM CS IS FS HM


Table 7: Detailed experimental results for the **Language Features** domain across three granularity levels (L1–L3).
We report the Concept Score (CS), Instruction Score (IS), Fluency Score (FS), and their Harmonic Mean (HM). All
metrics are evaluated on a 0–4 scale.


L1 L2 L3
**Method**


CS IS FS HM CS IS FS HM CS IS FS HM


Table 8: Detailed experimental results for the **Personality** domain across three granularity levels (L1–L3). We
report the Concept Score (CS), Instruction Score (IS), Fluency Score (FS), and their Harmonic Mean (HM). All
metrics are evaluated on a 0–4 scale.






L1 L2 L3
**Method**


CS IS FS HM CS IS FS HM CS IS FS HM


RePS 2.52 3.67 3.37 2.69 1.98 3.58 3.07 1.90 1.10 3.71 2.92 1.13


DiffMean 1.73 3.87 3.43 1.93 1.46 3.82 3.48 1.73 0.25 3.92 3.53 0.26
RePS 1.74 3.07 3.23 1.84 1.42 3.31 2.95 1.42 0.34 3.39 3.09 0.18


DiffMean 1.22 3.88 3.52 1.50 1.05 3.83 3.56 1.25 0.15 3.88 3.39 0.16
RePS 2.00 3.84 3.60 2.19 1.95 3.85 3.43 1.97 0.48 3.82 3.27 0.48


Table 9: Detailed experimental results for the **Reasoning Patterns** domain across three granularity levels (L1–L3).
We report the Concept Score (CS), Instruction Score (IS), Fluency Score (FS), and their Harmonic Mean (HM). All
metrics are evaluated on a 0–4 scale.


L1 L2 L3
**Method**


CS IS FS HM CS IS FS HM CS IS FS HM


**Gemma-2-9b-Instruct**
Vanilla 1.40 3.74 3.67 1.61 1.17 3.85 3.77 1.40 0.00 3.77 3.70 0.00

PCA 1.86 3.42 3.67 2.01 1.68 3.37 3.65 1.75 0.00 3.75 3.63 0.00
DiffMean 2.79 3.67 3.72 2.92 2.83 3.42 3.57 2.68 0.07 3.81 3.65 0.08
RePS **3.27** 3.41 3.73 3.21 2.75 3.15 3.46 2.53 1.65 3.55 3.07 1.64


PCA 1.37 3.58 3.62 1.38 1.13 3.80 3.68 1.29 0.03 3.86 3.73 0.03
DiffMean 2.44 3.70 3.56 2.54 2.25 3.85 3.62 2.49 0.01 3.86 3.68 0.02
RePS **2.93** 2.97 3.50 2.76 2.48 3.23 3.53 2.46 1.25 3.16 2.99 1.11


DiffMean 2.64 3.63 3.60 2.62 2.43 3.72 3.57 2.51 0.00 3.84 3.68 0.00
RePS 2.85 3.44 3.40 2.78 2.85 3.48 3.35 2.73 0.72 3.96 3.59 0.78


Table 10: Detailed experimental results for the **Sentiment** domain across three granularity levels (L1–L3). We
report the Concept Score (CS), Instruction Score (IS), Fluency Score (FS), and their Harmonic Mean (HM). All
metrics are evaluated on a 0–4 scale.


**D.3** **Question Set Generation Prompt**


We use the following hint template to generate a
diverse set of questions related to the concepts.
These are then divided into a training set of 70
questions and a test set of 30 questions.




**D.4** **Question Refinement Prompt**


We use the following prompts to restate the question, reducing lexical or semantic cues that directly
reveal the target concept.








**D.5** **Minimum Difference Comparison**
**Answer Pair Generation Prompt**


We use the following hint template to generate comparison answer pairs with the greatest structural
overlap and the least lexical-level difference, thus
highlighting conceptual differences.








**E** **Evaluation Prompt**


**E.1** **Concept Evalution Prompt**


We use the following hint template to evaluate the
relevance to the target concept


**E.2** **Instruction Evalution Prompt**


We use the following hint template to evaluate the
model’s ability to follow instructions


**E.3** **Fluency Evalution Prompt**


We use the following hint template to evaluate the
fluency of the response generated by the model




