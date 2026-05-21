## **ROLL**

2025-10-16

### **Attention Illuminates LLM Reasoning: The Preplan-and-Anchor** **Rhythm Enables Fine-Grained Policy Optimization**


**Yang Li** [12] **, Zhichen Dong** [12] **, Yuhan Sun** [1] **, Weixun Wang** [2] **, Shaopan Xiong** [2] **, Yijia Luo** [2] **,**
**Jiashun Liu** [2] **, Han Lu** [12] **, Jiamang Wang** [2] **, Wenbo Su** [2] _[∗]_ **, Bo Zheng** [2] **, Junchi Yan** [1] _[∗]_

1Shanghai Jiao Tong University 2Alibaba Group

### **Abstract**


The reasoning pattern of Large language models (LLMs) remains opaque, and Reinforcement
learning (RL) typically applies uniform credit across an entire generation, blurring the distinction
between pivotal and routine steps. **This work positions attention as a privileged substrate that**
**renders the internal logic of LLMs legible, not merely as a byproduct of computation, but as a**
**mechanistic blueprint of reasoning itself.** We first distinguish attention heads between locally and
globally focused information processing and reveal that locally focused heads produce a sawtooth
pattern near the diagonal indicating phrasal chunks, while globally focused heads expose tokens
that exert broad downstream influence over future tokens. We formalize these with two metrics: 1)
Windowed Average Attention Distance, which measures the extent of backward attention within a
clipped window; 2) Future Attention Influence, which quantifies a token’s global importance as the
average attention it receives from subsequent tokens. Taken together, these signals reveal a recurring
preplan-and-anchor mechanism, where the model first performs a long-range contextual reference
to generate an introductory token, which is immediately followed by or coincides with a semantic
anchor token that organizes subsequent reasoning. Leveraging these insights, we introduce three
novel RL strategies that dynamically perform targeted credit assignment to critical nodes (preplan
tokens, anchor tokens, and their temporal coupling) and show consistent performance gains across
various reasoning tasks. **By aligning optimization with the model’s intrinsic reasoning rhythm,**
**we aim to transform opaque optimization into an actionable structure-aware process, hoping to**
**offer a potential step toward more transparent and effective optimization of LLM reasoning.**







𝑖









𝛾!"#$%": More Credit for **Tokens of Semantic GroupsIntroductory**



𝑗

Local Attention Pattern










|This model finally finds more hidden patterns|Col2|
|---|---|
|**_This_**<br>_model_|_hidden patterns_|







𝑖



𝑗

Global Attention Pattern



𝛾!&"#'%": More Credit for **for Subsequent ReasoningAnchor Tokens**


𝛾!$#(')*+,: More Credit for **Influence of Semantic GroupsReallocated Semantic**



Focus More on Critical Nodes

of the Reasoning Path



Figure 1: **Attention dynamics uncover reasoning patterns:** Local heads exhibit a near-diagonal, sawtooth
pattern that forms phrasal chunks, while global heads highlight tokens with strong downstream influence.
Their coupling reveals a preplan-and-anchor rhythm: at chunk onsets, preplan tokens set up the next
reasoning step, followed (or coinciding) by anchor tokens that are persistently revisited by future tokens
to guide downstream reasoning. **Reasoning rhythm enhances RL:** Leveraging detected preplan and
anchor tokens, our RL method amplifies their token-level credit accordingly, focusing learning on the
critical nodes that drive more effective reasoning.


_∗_
Correspondence authors. Junchi Yan: `yanjunchi@sjtu.edu.cn` ; Wenbo Su: `vincent.swb@taobao.com`


1


**1** **Introduction**


Large Language Models (LLMs) have achieved remarkable success on complex reasoning, propelled by
training algorithms that elicit explicit step-by-step thought. A prominent paradigm is Reinforcement
Learning with Verifiable Rewards (RLVR) (Lambert et al., 2024), where a model’s outputs are optimized
with RL objectives guided by automated correctness checks. This setup encourages models to produce
intermediate reasoning tokens before issuing a final answer, giving rise to Large Reasoning Models
(LRMs) that excel on challenging problems in mathematics (Hendrycks et al., 2021; Cobbe et al., 2021b;
Shao et al., 2024; Yang et al., 2024), coding (Chen et al., 2021; Jimenez et al., 2023; Hui et al., 2024), and
agentic decision making (Liu et al., 2023; Yao et al., 2024).


Despite impressive performance, LLMs remain largely opaque: there still lacks a clear understanding of
how LLMs structure their reasoning process internally, when and how they retrieve and bind information.
Consequently, optimization strategies often treat an entire generation as a uniform target. In the popular
RL settings, sequence-level rewards are typically spread across all tokens (Shao et al., 2024; Yu et al.,
2025), blurring the distinction between pivotal moments that shape downstream reasoning and routine
steps that merely elaborate local structure. This mismatch between how models appear to reason and
how we optimize them limits data efficiency, interpretability, and the reliability of performance gains on
challenging reasoning tasks. This paper seeks to bridge this gap by first showing an intrinsic reasoning
rhythm through the lens of attention dynamics and subsequently introducing fine-grained RL strategies
that enhance credit assignment to the tokens where the model appears to plan and anchor its reasoning.


Our analysis takes two complementary views of attention: a local (backward) perspective that measures
how strongly a token depends on nearby versus distant context, and a global (forward) perspective
that measures a token’s downstream influence on subsequent tokens. Specifically, we classify attention
heads as either locally or globally focused based on their average attention span, which we define as
the attention-weighted mean positional distance of their attention connections. Aggregating patterns
within each class reveals two robust regularities as shown in Fig. 1. First, locally focused heads exhibit a
sawtooth motif near the diagonal that tracks phrasal or semantic chunks. Within a chunk (e.g., habitual
expressions), attention stays highly localized, while the onset of a new chunk pulls attention back to
earlier context. Second, globally focused heads highlight a small set of anchor tokens that exert broad
downstream influence. These tokens are revisited by many subsequent positions and act as semantic
pivots that steer the unfolding reasoning.


We distill these regularities into two model-internal metrics computed from the attention map of an
auxiliary forward pass. The **Windowed Average Attention Distance (WAAD, Def. 4.1)** measures how
far a token looks back within a clipped window, emphasizing whether the model must reach beyond
immediate neighbors to resolve ambiguity. Visualizing the WAAD sequence reveals a clear alternation
between peaks and valleys, aligned with chunk boundaries. The **Future** **Attention** **Influence** **(FAI,**
**Def. 4.1)** quantifies a token’s global importance by measuring the average attention it receives from later
tokens. Visualizing the FAI sequence reveals differences and fluctuations in token influence, where highinfluence tokens essentially correspond to key logical waypoints, such as pivotal definitions, intermediate
results, or decision points. **The joint dynamics of the metrics** reveal a consistent two-beat preplan-andanchor pattern. As the model approaches a semantic boundary, WAAD spikes as it consults longer-range
context to draft an introductory token. This spike is often followed by, or coincides with, the emission
of an anchor token with high FAI that organizes downstream inference. Additionally, WAAD spikes
typically maintain high token entropies. The model reaches further back when nearby cues are insufficient
to disambiguate the next step (e.g., when the preceding words do not naturally license the next token).
Conversely, locally dominated tokens tend to have lower entropy, reflecting stereotyped continuations.


Building on the insights, we propose fine-grained policy optimization strategies that align credit assignment with the model’s intrinsic reasoning patterns. Rather than applying uniform advantages across a
trajectory, we offer a process-aware alternative by leveraging internal, attention-based signals to differentially reinforce the steps the model itself treats as structurally decisive, as shown in Fig. 1: (1) emphasizing
introductory tokens at chunk onsets (WAAD peaks) to establish the local scaffold for subsequent steps; (2)
amplifying anchor tokens (high FAI) to articulate and preserve core semantic commitments that organize
downstream inference, accelerating the propagation of verifiable signals to key decision points; and (3)
when an anchor is locally dominated, reallocate part of its credit to the associated introductory token,
promoting coherent chunk-level credit assignment rather than overfitting a single position.


**Our contributions include:** (1) We introduce attention dynamics as a principled lens for uncovering
intrinsic reasoning structure in LLMs and empirically reveal the so-called preplan-and-anchor rhythm.
We formalize this pattern through two novel metrics and analyze their joint behavior to characterize local
phrasal processing and global contextual anchoring. (2) Building on these insights, we introduce three
structure-aware reinforcement learning strategies that dynamically reweight token-level advantages to
emphasize critical reasoning nodes, specifically, introductory preplan tokens, semantic anchor tokensand


2


their temporal coupling. (3) We demonstrate consistent and significant empirical gains across various
reasoning benchmarks, validating our effectiveness and efficiency while maintaining compatibility with
existing RLVR workflows.


**2** **Related Work**


**Reinforcement Learning for LLMs.** Reinforcement learning (RL) is central to LLM post-training, popularized by RLHF for instruction following and preference alignment (Christiano et al., 2017; Ziegler
et al., 2019; Ouyang et al., 2022; Schulman et al., 2022; Bai et al., 2022a). Two strands dominate: online
policy-gradient methods with on-policy rollouts (Schulman et al., 2017; Shao et al., 2024; Williams, 1992)
and offline preference optimization without on-policy sampling (Rafailov et al., 2023; Meng et al., 2024;
Ethayarajh et al., 2024). Reinforcement Learning from AI Feedback (RLAiF) extends this by using LLMs
to generate feedback for alignment (Bai et al., 2022b; Sun et al., 2023; Lee et al., 2023; Guo et al., 2024).
Outcome-based **RL with verifiable rewards (RLVR)** (Shao et al., 2024; Lambert et al., 2025) has driven
recent advances through deterministic rule-based rewards (Xin et al., 2024; Wang et al., 2024), with
large-scale systems demonstrating that correctness-guided RL elicits extended reasoning (Lambert et al.,
2024; OpenAI, 2024; Guo et al., 2025; Team et al., 2025; Yang et al., 2025a). A growing ecosystem studies
data aggregation, policy updates, and scalable training infrastructure (Yu et al., 2025; Yue et al., 2025;
Zheng et al., 2025; Liu et al., 2025).


**Analyses of LLM Reasoning.** A complementary literature analyzes how LLMs represent and execute
reasoning (Wang et al., 2023; Ma et al., 2023; Dong et al., 2025; Yang et al., 2025b). Step-level edits suggest
surface CoT redundancy (Wang et al., 2022; Madaan & Yazdanbakhsh, 2022; Wang & Zhou, 2024; Chen
et al., 2024; Han et al., 2025; Wolf et al., 2025). White-box studies identify components that propagate
information, such as iteration and receiver heads (Cabannes et al., 2024; Ren et al., 2024; Bertolazzi et al.,
2025), critical subsets of attention heads (Geva et al., 2023; Mohebbi et al., 2023; Zheng et al., 2024),
steerable planning/backtracking directions (Venhoff et al., 2025; Turner et al., 2024), and deduction
circuits (Dutta et al., 2024; Ameisen et al., 2025; Lindsey et al., 2025). Additional phenomena include
attention sinks on initial tokens (Xiao et al., 2023; Gu et al., 2025; OpenAI et al., 2025; Barbero et al., 2025)
and anchor sentences that guide downstream inference (Bogdan et al., 2025; Men et al., 2024). These
accounts, however, are often descriptive and rarely yield process-aware training recipes.


Within RLVR, analyses indicate that gains are driven by the emergence and macro-structure of explicit
reasoning rather than answer correctness and the micro-content (Gandhi et al., 2025; Li et al., 2025). Other
work targets critical tokens as decision points for exploration (Vassoyan et al., 2025; Lin et al., 2024) and
emphasizes high-entropy _forking_ tokens that govern divergent paths (Wang et al., 2025b;a; Cheng et al.,
2025; Cui et al., 2025). Our approach differs by deriving model-internal signals from attention dynamics.
We identify a recurring preplan-and-anchor rhythm, link key metrics to model-internal signals, and use
these signals to perform targeted credit assignment within standard RL frameworks.


**3** **Preliminaries**


**3.1** **Self-Attention Mechanism in Decoder-Only LLMs**


Given the sampled question **q** _∼_ _Q_, a decoder-only LLM policy _πθ_ autoregressively generates an output
sequence **o**, with **o** _t_ as the _t_ -th token in **o** :


_T_
### pθ ( o | q ) = ∏ pθ ( ot | q, o <t ). (1)

_t_ =1


Within each Transformer layer _l_ and head _h_ _∈{_ 1, . . ., _H}_, multi-head self-attention computes headspecific attention maps:


                      
**S** [(] _[l]_ [,] _[h]_ [)] = **[Q]** [(] _[l]_ [,] _[h]_ ~~_√_~~ [)] **[K]** [(] _[l]_ [,] _[h]_ [)] _[⊤]_ + **M**, **A** [(] _[l]_ [,] _[h]_ [)] = softmax **S** [(] _[l]_ [,] _[h]_ [)][�], **O** [(] _[l]_ [,] _[h]_ [)] = **A** [(] _[l]_ [,] _[h]_ [)] **V** [(] _[l]_ [,] _[h]_ [)], (2)

_dk_

                  and aggregates heads via MHA( **X** ) = Concat _h_ _[H]_ =1 **[O]** [(] _[l]_ [,] _[h]_ [)][�] **WO** [(] _[l]_ [)][.] [Causal masking enforces autoregressive]
dependence with

�0, _s ≤_ _t_,
### M t, s = − ∞, s > t, ⇒ A [(] t, [l] s [,] [h] [)] = 0 for s > t, s ∑ ≤t A [(] t, [l] s [,] [h] [)] = 1. (3)

Thus, each attention map **A** [(] _[l]_ [,] _[h]_ [)] _∈_ **R** _[T][×][T]_ is lower-triangular and row-stochastic, providing head-specific
weights over past positions that we analyze.


3


**3.2** **Reinforcement Learning with Verifiable Rewards**


RL optimized the LLM policy to maximize the cumulative rewards _r_ received from the verifier:

max _θ_ _J_ ( _θ_ ) := **Eq** _∼Q_, **o** _∼πθ_ ( _·|_ **q** )[ _r_ ( **o** )]. (4)


Policy gradient methods (Williams, 1992) are a standard approach for solving this optimization problem,
with Proximal Policy Optimization (PPO) (Schulman et al., 2017) as the de facto standard for stable,
sample-efficient fine-tuning. PPO updates on data from a frozen old policy _πold_, applies importance
sampling to correct distribution shift, and optimizes a clipped surrogate objective to constrain divergence
between the new and old policies:



1
_J_ PPO( _θ_ ) = **Eq** _∼Q_, **o** _∼πθ_ ( _·|_ **q** ) _|_ **o** _|_



_|_ **o** _|_
### ∑ min

_t_ =1




- _πθ_ ( _ot|_ **q**, **o** _<t_ ) [clip] - _πθ_ ( _ot|_ **q**, **o** _<t_ ) [1] _[−][ϵ]_ [,] [1][+] _[ϵ]_ - _At_
_πθ_ old ( _ot|_ **q**, **o** _<t_ ) _[A][t]_ [,] _πθ_ old ( _ot|_ **q**, **o** _<t_ ) [,]







(5)



where _At_ is the advantage at step _t_, typically estimated via Generalized Advantage Estimation (GAE) (Schulman et al., 2015), and _ϵ_ is a clipping hyperparameter for stabilizing updates.


Group Relative Policy Optimization (GRPO) (Shao et al., 2024) eliminates the value function (critic)
and instead estimates the advantage by normalizing rewards within a group of sampled responses for
the same prompt. Specifically, for a prompt **q** with _G_ responses and associated rewards _{ri}i_ _[G]_ =1 [,] [the]
group-normalized advantage is given by:

_A_ ˆ _i_, _t_ = _[r][i]_ _[−]_ [mean][(] _[{][r][i][}]_ _i_ _[G]_ =1 [)] . (6)

std( _{ri}i_ _[G]_ =1 [)]


By emphasizing the differences among candidate outputs for the same prompt, it effectively preserves the
reliability of the gradient signal, even in sparse reward settings. In addition to this modified advantage
estimation, GRPO adds a KL penalty term to the clipped objective in Eq. 5.


**4** **Dissecting Attention Dynamics to Expose the Reasoning Rhythm**


This section dissects attention dynamics to uncover an intrinsic rhythm in model reasoning and grounds
each claim with **inline empirical validations** . More experimental details can be found in Appendix A.1.


**4.1** **Head Grouping by Span and the Emergent Local/Global Patterns**


To uncover characteristic reasoning patterns, we analyze attention maps from two complementary
directions, i.e., forward (the reach of a token’s downstream influence into distant later steps) and
backward (the extent to which a token’s generation is dominated by the immediately preceding context).
Together, these perspectives correspond to local and global views of the reasoning structure.


We analyze attention dynamics using Qwen3-4B-Base (Yang et al., 2025a) on math prompts from the
GSM8K dataset (Cobbe et al., 2021b) with temperature _T_ =0.7. Using the non-SFT model avoids confounds
from supervised instructions and provides a clean starting point for zero-RL training. For each prompt,
we obtain attention maps via a single forward pass over the concatenated prompt-response sequence;
unless otherwise noted, all token-level metrics are computed on rows corresponding to response tokens.


Let **A** [(] _[l]_ [,] _[h]_ [)] _∈_ **R** _[N][×][N]_ denote the causal attention map for layer _l_ and head _h_ over the full sequence of length

_N_, with **A** [(] _t_, _[l]_ _s_ [,] _[h]_ [)] the attention from position _t_ to _s_ _≤_ _t_ . Since the attention is causal and row-stochastic

(∑ _[t]_ _s_ =1 **[A]** _t_ [(], _[l]_ _s_ [,] _[h]_ [)] = 1 for each _t_ ), we can interpret each row as a probability distribution over past positions.
To characterize the effective receptive span of a head, we define its attention-weighted mean backward
distance over the generated response positions _R_ as:



1
_d_ [(] _[l]_ [,] _[h]_ [)] =
### |R| t [∑] ∈R



_t_
### ∑ A [(] t, [l] s [,] [h] [)] ( t − s ), (7)

_s_ =1



Since the inner sum is a convex combination of distances ( _t −_ _s_ ), _d_ [(] _[l]_ [,] _[h]_ [)] is precisely the average distance that
head ( _l_, _h_ ) looks back when generating tokens in the response. Consequently, heads with smaller _d_ [(] _[l]_ [,] _[h]_ [)]
indicate a strong focus toward recent context (i.e., attention concentrated near the diagonal), reflecting
local focus, whereas large values signify frequent long-range dependencies (i.e., attention reaching far into
the past), characteristic of global focus. We sort all heads by _d_ [(] _[l]_ [,] _[h]_ [)] and designate the lowest and highest


4


Figure 2: Visualization and quantification of local and global attention patterns on a math reasoning case.
Left: a local-focused attention map highlights near-diagonal sawtooth patterns, and a global-focused map
highlights vertical stripes indicative of broader attention. Right: the corresponding token-level metrics,
including FAI (Def. 4.1) for receiver and global heads, WAAD (Def. 4.1), and token entropy, with key
points correlating with each other.


quantiles (e.g., bottom/top 30%) as the local-focused set _H_ loc and global-focused set _H_ glob, respectively.
We then aggregate attention within each group:


1 1
### A ¯ [loc] = ∑ A [(] [l] [,] [h] [)], A ¯ [glob] = ∑ A [(] [l] [,] [h] [)] . (8)
_|H_ loc _|_ ( _l_, _h_ ) _∈H_ loc _|H_ glob _|_ ( _l_, _h_ ) _∈H_ glob


Fig. 2 visualizes **A** [¯] [loc] and **A** [¯] [glob], revealing two complementary patterns summarized below.


**Local Attention Pattern:** **Near-Diagonal Sawtooth Indicating Local Phrasal Chunks.** The local-focused
aggregate map **A** [¯] [loc] exhibits a characteristic sawtooth along the diagonal that tracks phrasal or semantic
chunks. Within a semantic or phrasal chunk (e.g., “by the way”), attention remains tightly local, while at
the onset of a new chunk, attention abruptly reaches further back, followed by locally dominated tokens.


To operationalize this local structure, we introduce a windowed distance to measure how far a token
looks back within a clipped window, emphasizing whether the model must reach beyond immediate
neighbors to resolve ambiguity. We introduce a time window to downweight absolute positional artifacts
since tokens of different positions handle different preceding attention ranges.





Low WAAD values indicate tight local continuation within a chunk (valleys), while spikes represent longrange consultation at chunk boundaries (peaks). The WAAD sequence in Fig. 2 reveals clear peak-valley
alternation aligned with chunk boundaries: a chunk onset typically exhibits a peak (it must retrieve earlier
context to form semantics), followed by a sharp drop as subsequent tokens rely on immediate neighbors.
Mechanistically, local heads enact habit-driven micro-syntax, where once a chunk is initiated, subsequent
tokens are locally licensed with low uncertainty, reflecting collocational continuations internalized during
pretraining. Hesitation concentrates at chunk boundaries, where the model consults longer-range context.


**Global Attention Pattern:** **Sparse Anchors with Broad Influence to Downstream Tokens.** The global

5


focused aggregate map **A** [¯] [glob] disproportionately highlights a sparse set of tokens that receive sustained
attention from many future positions. These tokens function as semantic anchors that are repeatedly
revisited and steer unfolding reasoning to a stable frame. We quantify a token’s downstream importance
by averaging the attention it receives from future positions within a controlled horizon.





High FAI surfaces tokens with broad downstream reach (anchor tokens). As shown in Fig. 2, visualizing
FAI over a response reveals differences and fluctuations in token influence, where high-influence tokens
essentially correspond to key logical waypoints (e.g., pivotal definitions, intermediate results, or decision
points). We also observe a growing density of high-FAI tokens as the trajectory approaches the final
answer region, consistent with the need to consolidate prior reasoning.


**Do Perturbations at High-FAI Tokens More Effectively Alter Subsequent Reasoning?** At a chosen
position _i_ _[∗]_, we take the predictive distribution _pθ_ ( _· |_ **o** _<i∗_ ), select the top- _k_ candidates _Vk_ ( _i_ _[∗]_ ) (i.e., highestlogit tokens), and for each _v ∈Vk_ ( _i_ _[∗]_ ) we force _oi∗_ = _v_ and roll out continuations under greedy decoding.
We then compare each counterfactual trajectory **o** ˜ _>_ _[v]_ _i_ _[∗]_ [with the original] **[ o]** _[>][i][∗]_ [using Jaccard overlap over]
content words, with _S_ ( _·_ ) denotes the content token set of a reasoning trajectory:



Jaccard ( **o** _>i∗_, ˜ **o** _>_ _[v]_ _i_ _[∗]_ [) =]




- 
- _S_ ( **o** _>i∗_ ) _∩S_ ( **o** ˜ _v>i_ _[∗]_ [)] 
- - . (11)

- _S_ ( **o** _>i∗_ ) _∪S_ ( **o** ˜ _v>i_ _[∗]_ [)] 


We conduct this analysis on 70 randomly sampled math
problems. We conduct rollout simulations on high-FAI positions and low-FAI positions for comparison. As shown in
Table 1, across problems and rollout horizons, perturbations
at high-FAI positions yield substantially lower Jaccard similarity, with 87.14% of trials showing greater deviation than at
low-FAI positions. This indicates that FAI-identified anchors
causally organize downstream inference: changing them reshapes the global plan and cadence of reasoning, whereas
interventions at locally dominated positions primarily affect
surface form without redirecting the overall trajectory.



Table 1: Jaccard similarity of rollouts
for top- and bottom- _k_ ranked by FAI.
Pr(Top _<_ Bottom) denotes the percentage
of trials where top- _k_ similarity is lower.


Top- _k_ Bottom- _k_


Mean Jaccard similarity 0.534 0.631
Pr(Top _<_ Bottom) 87.14%



Fig. 3 and the corresponding results in Appendix B.1 show examples comparing the effects of perturbing
high-FAI versus low-FAI positions. Replacing high-FAI tokens (even with semantically similar alternatives) frequently induces substantial shifts in the model’s downstream reasoning logic, such as altering
the problem-solving strategy or even changing the overall correctness, as reflected by the low Jaccard
similarity. In contrast, perturbations at low-FAI positions typically affect only local phrasing while
preserving the global reasoning structure, even yielding near-identical continuations. The results show
that FAI reflects a reasoning-anchoring capacity that causally governs the model’s planning and execution
rhythm, rather than merely reflecting surface-level linguistic variation.


**4.2** **Joint Dynamics:** **A Recurring Preplan-and-Anchor Mechanism**


Single-metric evaluations of reasoning often provide an incomplete picture. In practice, key internal
signals are closely coupled. This section explores the joint dynamics of internal metrics while also
connecting to readily observable indicators. A multidimensional analysis of these signals uncovers three
robust empirical couplings, converging on a recurring preplan-and-anchor mechanism that underlies
and organizes the model’s reasoning behavior.


**Coupling** **Pattern** **1:** **WAAD** **Peaks** **Maintain** **Higher** **Token** **Entropies.** Token-level entropy _Ht_ =

_−_ ∑ _v pθ_ ( _v |_ **q**, **o** _<t_ ) log _pθ_ ( _v | ·_ ) reflects predictive uncertainty and drives reasoning exploration (Wang
et al., 2025b). As shown in Fig. 2, spikes in WAAD _t_ correspond to tokens with higher _Ht_ . When immediate
local cues dominate, next-token prediction is confident (low _Ht_ ) and attention remains near-diagonal (low
WAAD _t_ ), which is consistent with habit-driven micro-syntax learned in pretraining (e.g., after “by the”,
“way” follows naturally). In contrast, at semantic junctures where the local context underdetermines


6


Figure 3: An example comparing the effects of perturbing high-FAI versus low-FAI positions and
continuing the rollout of the subsequent reasoning trajectory. Perturbing a high-FAI position typically
leads to a clear shift in the overall reasoning logic, whereas replacing a low-FAI token more frequently
just alters local phrasing, leaving the downstream reasoning trajectory essentially unchanged.


the next step, the model exhibits higher uncertainty (high _Ht_ ) and reaches further back to retrieve
disambiguating information (high WAAD _t_ ). In this sense, high-entropy tokens and WAAD peaks can
be two sides of the same coin: local ambiguity triggers long-range consultation. Conversely, locally
dominated tokens tend to have lower entropy, reflecting stereotyped continuations that can be decided
from local context alone.


**Coupling Pattern 2:** **Receiver Heads and Global-Focused Heads Surface Shared Anchors.** Bogdan
et al. (2025) has identified receiver heads, i.e., attention heads whose inbound attention distribution is
highly selective and thus diagnostic of tokens that attract strong attention from future positions (e.g., via
column-wise kurtosis). We compare those heads with our global-focused set _H_ glob, and find that the
token-level downstream influence computed from either set is highly concordant. Aggregating attention
over receiver heads or over _H_ glob yields strongly correlated FAI profiles across tokens, as shown in Fig. 2,
indicating that span-based and kurtosis-based filtering arrive at the same conclusions and mutually
corroborate one another.


**Coupling Pattern 3: FAI Peaks Follow or Coincide with WAAD Peaks.** As highlighted in Fig. 2, high-FAI
tokens typically occur at or just after WAAD peaks, reflecting a two-beat process: (i) _Preplan_ : As the
model approaches a semantic boundary, a WAAD peak signals long-range context retrieval to generate
an introductory token that prepares the forthcoming concept or step. (ii) _Anchor_ : At the same position
or immediately later, the model emits a token with high FAI, repeatedly attended by future positions
to guide and stabilize subsequent reasoning. When the model delivers a key logical point, it may have
already planned it in advance; however, to preserve fluency and conventional phrasing, it often first
produces an introductory token to open the chunk and only then emits the key anchor token. From a
local perspective, such anchor tokens can be dominated by immediately preceding tokens, leaving little
room for exploration at the anchor position itself. This motivates joint consideration of both the anchor
and its introductory token during optimization.


**Quantitative** **Analysis.** To quantify the significance of the three couplings, we randomly sample 70
questions and analyze linkages between metrics. For each coupling, we compute the observed statistic
(e.g., average entropy at WAAD peaks, co-occurrence rates of FAI and receiver-head peaks, alignment
between WAAD and FAI peaks) and compare it against the expectation under random situations in which
the positions of the first metric’s peaks are shuffled. Table 2 shows that all couplings exhibit substantial
lifts over random chance (ranging from +42.47% to +171.49%), validating these joint dynamics.


7


Table 2: Quantitative Analysis of Linkages Between Key Metrics. Random baselines are illustrative
estimates based on the probability of this value occurring under completely random conditions. Lift quantifies the strength of the correlation beyond random chance, calculated by (Observed - Random)/Random.


**Metric Correlation** **Random** **Observed** **Lift**


Average Entropy of the WAAD Peaks 0.2386 0.3608 +51.97%
FAI Peak of Receiver & Global Heads Co-occurrence 22.41% 60.84% +171.49%
FAI Peak Follows/Coincides with WAAD Peak 36.87% 52.53% +42.47%


**5** **Fine-Grained Policy Optimization Driven by Attention Signals**


Conventional sequence-level RLVR distributes credit uniformly across tokens, overlooking the internal
reasoning organization that indicates positions (preplans and anchors) are structurally decisive. We
instead align token-level credit with the model’s intrinsic reasoning rhythm by rescaling the per-token
advantage in on-policy RL using data-dependent weights derived from attention dynamics.


**5.1** **Attention Calculation in the RL Framework**


**The Vanilla RL Framework.** In reinforcement learning (RL) for large language models (LLMs), the core
objective is to optimize a policy that maximizes expected task-specific rewards, such as correctness in
mathematical reasoning, while maintaining alignment with the original language distribution. Under
PPO framework, which also generalizes to GRPO and similar on-policy methods, training proceeds
through an iterative loop of inference, reward evaluation, and policy update. We implement our methods
on top of the ROLL framework (Wang et al., 2025c).


In our setup, two reasoning model instances are maintained: (1) `actor` ~~`i`~~ `nfer` : deployed with `vLLM`
for high-throughput, low-latency inference; (2) `actor` ~~`t`~~ `rain` : implemented in `Megatron` for efficient
large-scale training with model parallelism. At each iteration, `actor` ~~`i`~~ `nfer` (initialized from the latest
`actor` `train` weights) generates a batch of responses to input prompts. These responses are evaluated
by a reward model or an execution-based verifier, producing scalar rewards per sequence. The promptresponse-reward tuples constitute the RL experience data. This data is then fed to `actor` ~~`t`~~ `rain`, which
computes policy gradients using the clipped objective to ensure stable updates. After each training
update, the updated weights of `actor` ~~`t`~~ `rain` are synchronized to `actor` `infer`, closing the loop.


**Implementation** **of** **Attention** **Mechanisms** **in** **RL.** Modern distributed training frameworks and inference engines for LLM like `vLLM` and `Megatron` typically employ flash attention (Dao et al., 2022) for
computational efficiency, which discards full attention matrices during execution to reduce memory
overhead. Consequently, the complete attention maps are not available for analysis in either `actor` ~~`i`~~ `nfer`
or `actor` `train` . To address this, we introduce a dedicated auxiliary model, `actor` ~~`a`~~ `ttn`, implemented
with a standard Transformer. This model retains full attention weights during the forward pass, enabling
us to compute internal metrics based on attention dynamics.


Specifically, after `actor` `infer` completes generation of a response (which involves hundreds to thousands
of forward steps during autoregressive decoding), we concatenate the original prompt and the generated
response into a single sequence and perform one additional forward pass through `actor` ~~`a`~~ `ttn` . During
this pass, we sample attention maps from five evenly spaced layers within the middle third of the network
(i.e., from layers _⌊L_ /3 _⌋_ to _⌊_ 2 _L_ /3 _⌋_, where _L_ is the total number of layers) to serve as representative
snapshots of the model’s internal attention behavior. The model typically requires thousands of forward
passes for token-by-token generation, whereas we obtain attention maps with just a single additional
forward pass over the generated response (together with the prompt), introducing little additional latency
with parallel computation. After each policy update of `actor` ~~`t`~~ `rain`, its parameters are synchronized to
both `actor` ~~`i`~~ `nfer` and `actor` ~~`a`~~ `ttn` to ensure consistency across inference, training, and attention analysis.


**5.2** **Targeted Credit Assignment to Critical Nodes in Reasoning**


For the specific advantage scaling designs in RL, without loss of generality, we illustrate with the vanilla
PPO objective and introduce a shaped advantage:







1
_J_ ( _θ_ ) = **Eq** _∼Q_, **o** _∼πθ_ ( _·|_ **q** ) _|_ **o** _|_



_|_ **o** _|_
### ∑ min

_t_ =1




- _πθ_ ( **o** _t|_ **q**, **o** _<t_ ) [clip] - _πθ_ ( **o** _t|_ **q**, **o** _<t_ ) [1] _[−][ϵ]_ [,] [1][+] _[ϵ]_ - _Atγt_
_πθ_ old ( **o** _t|_ **q**, **o** _<t_ ) _[A][t][γ][t]_ [,] _πθ_ old ( **o** _t|_ **q**, **o** _<t_ ) [,]



(12)
where _γt_ is the scaling coefficient. Our variants amplify the advantages of tokens identified by the
model’s internal reasoning patterns, thereby improving the efficiency of RL. We instantiate _γt_ with three


8


strategies that correspond to the local preplan signal, the global anchor signal, and their joint coupling.


**(1)** **Local-chunk** **credit:** **select** **preplan** **tokens** **via** **distance** **drops,** **motivated** **by** **the** **local** **attention**
**pattern (Sec. 4.1).** For the tokens within each response, we detect preplan tokens by the WAAD variations
between consecutive positions and then select the top _q_ quantile tokens accordingly:


∆ _t_ = _|_ WAAD _t −_ WAAD _t_ +1 _|_ and _T_ loc = TopQ�∆ _t_, _q_ =0.4�, (13)


Here, large ∆ _t_ identifies the boundary tokens at a peak-valley transition of phrasal chunks. Since these
tokens initiate local scaffolds and guide subsequent reasoning, emphasizing these points strengthens the
locus of planning and encourages the policy to resolve long-range dependencies before committing. We
amplify advantages of tokens within _T_ loc by configuring the scaling coefficient:

_γt_ = 1 + ( _γ_ amp _−_ 1) **1** _{t ∈T_ loc _}_, (14)


where _γ_ amp = 1.5 denotes an amplification factor.


**(2) Global-anchor credit:** **select tokens with high future influence, motivated by the global attention**
**pattern (Sec. 4.1).** We score tokens by FAI and then select the top _q_ quantile tokens accordingly:


_T_ glob = TopQ�FAI, _q_ =0.4�, (15)


By amplifying anchors, it learns to articulate and preserve core semantic commitments that organize
downstream inference. Because these tokens largely determine subsequent reasoning, prioritizing
reinforcement (and, when applicable, penalties) at these positions propagates the verifiable signal to the
key points more quickly, enabling more targeted optimization. Thus, We amplify advantages of tokens
within _T_ glob by configuring the scaling coefficient:


_γt_ = 1 + ( _γ_ amp _−_ 1) **1** _{t ∈T_ glob _}_, (16)


where _γ_ amp = 1.5 denotes an amplification factor.


**(3) Coupled rhythm credit:** **combine preplans and anchors, and back-allocate credit from anchors to**
**their local precursors,** **motivated by the joint dynamic of local/global patterns (Sec. 4.2).** A locally
dominated anchor has limited freedom to optimize, so we back-allocate credit of high-FAI tokens across
the local semantic chunk, promoting coherent chunk-level scaffolding rather than overfitting to a single
position. We couple WAAD with FAI signal to reflect the two-beat rhythm and to share credit between
anchors and their preceding preplans. The key idea is: identify high-influence anchors, test whether they
are locally dominated, and, if so, diffuse a fraction of their credit backward to the preplan token that
prepares the anchor.


With the anchor candidate set _T_ glob, the WAAD variations ∆ _t_, and given thresholds _τ_ waad and _τ_ ∆, we say
an anchor _t_ is locally dominated by its immediate past _k_ tokens if


WAAD _t_ _≤_ _τ_ waad and max _[≥]_ _[τ]_ [∆][.] (17)
_u∈{t−k_,..., _t−_ 1 _}_ [∆] _[u]_


We denote _t ∈D_ when _t_ is a high-influence token with low WAAD, locally licensed preceded by a recent
WAAD peak. Then, we redistribute a fraction _α_ _∈_ [0, 1] of the amplification bonus _γ_ amp _−_ 1 from each
locally dominated anchor to its associated introductory token _I_ ( _D_ ) = _{_ intro( _s_ ) : _s ∈D}_ :


_γt_ = 1 + ( _γ_ amp _−_ 1) **1** _{t ∈T_ glob _\ D}_ + (1 _−α_ )( _γ_ amp _−_ 1) **1** _{t ∈D}_ + _α_ ( _γ_ amp _−_ 1) **1** _{t ∈I_ ( _D_ ) _}_, (18)


where _γ_ amp = 1.5 denotes an amplification factor.


**5.3** **Experimental Evaluation**


**5.3.1** **Experiment Settings**


**Benchmarks.** We test on relatively simple puzzles and question-answering (QA) benchmarks and
challenging mathematical reasoning datasets. (i) the _Countdown_ puzzle (Pan et al., 2025), where the goal is
to combine four given numbers using arithmetic operations to reach a target value; (ii) the _CrossThink-QA_
dataset (Akter et al., 2025), which aggregates multi-domain QA pairs from heterogeneous sources; and
(iii) five standard math reasoning benchmarks: AIME24, AIME25, AMC, MATH500 (Hendrycks et al.,
2021), and OlympiadBench (He et al., 2024).


**Baselines.** Our approach introduces a novel modulation of token-level advantages for RL. To isolate the
impact of this design, we implement our method on top of GRPO to directly assess the improvement.
In addition, we consider alternative token-level advantage enhancement strategies for comparison: (1)


9


Table 3: Results on the Countdown and QA datasets.
Bold denotes the best results per dataset.


**Method** **Countdown** **CrossThinkQA**


GRPO 52.6 48.0
+ random credit 55.0 47.8
+ high-entropy credit 57.7 48.0

down and Qwen3-8B-Base on QA.

|Col1|Col2|Col3|
|---|---|---|
||||



Figure 5: RL Performance curves of Qwen3-4B-Base and Qwen3-8B-Base models for math reasoning.


_Random_ : randomly select tokens for advantage amplification; (2) _Entropy_ : amplify advantages for tokens
with high predictive entropy to encourage exploration.


**Backbone Models and Implementation Details.** Experiments are conducted using the Qwen3-4B-Base
and Qwen3-8B-Base models. We use a maximum context length of 1024 for simple puzzles and QA, and
1024 or 8192 for math reasoning. The shorter context length is adopted as it yields a cleaner reasoning
process that aligns more closely with the analytical environment and is less confounded by long-range
dependencies that can dilute the effect of attention-based strategies. The curves are smoothed through
the exponential moving averages of the peak performance, emphasizing sustained improvements.


**Training details.** We use a training batch size of 512 and micro-batch size of 32, yielding 16 gradient steps
per batch, with learning rate 1 _×_ 10 _[−]_ [6] . The loss excludes both KL and entropy regularization. Decoding
temperature during training is _T_ =1.0. Our rhythm-aligned variants replace the per-token advantage
_At_ by _A_ [˜] _t_ = _γt_ _At_, where _γt_ is computed from attention maps captured in a single forward pass. Unless
noted, we set the WAAD window _W_ = 10, the FAI horizon _H_ _∈_ [10, 50], anchor selection by top-quantile
( _q_ =40%), neighborhood size _k_ _∈{_ 1, 2, 3 _}_ for back-allocation. All shaping signals are detached from
gradients and applied only to nonnegative advantages. The 4B models are trained on 8 GPUs, and the 8B
models are trained on 16 GPUs, running for 500 and 600 steps, respectively. More experimental details
for RL experiments can be found in Appendix A.2.


**5.3.2** **Results and Analyses**


**Results** **on** **Simple** **Logical** **Puzzles** **and** **QA.** Table 3 reports the final accuracy on the Countdown
and CrossThink-QA benchmarks. On Countdown, our _coupled rhythm credit_ strategy achieves 63.1%,
substantially outperforming GRPO (52.6%). Notably, both _local-chunk_ and _global-anchor_ credit schemes also
yield consistent gains, suggesting that structured credit propagation effectively guides policy learning. In
contrast, random or entropy-based token selection provides marginal or no improvement. On CrossThinkQA, where reasoning is more open-ended and less constrained by formal rules, all credit-aware variants
show consistent improvements over GRPO (48.0%). The best-performing variant, _coupled rhythm credit_,
reaches 50.1%, indicating that attention-based credit assignment can aid generalization in heterogeneous
QA. Fig. 4 shows the training curves on Countdown and QA tasks. Our variants converge faster and reach
higher plateaus than GRPO, with _coupled credit_ exhibiting the earliest improvement and highest scores.


**Results on Mathematical Reasoning.** Table 4 evaluates credit assignment strategies across mathematical
reasoning benchmarks and model scales. Our methods consistently outperform both the GRPO baseline
and naive alternatives (e.g., random or high-entropy credit). Notably, _coupled rhythm credit_ achieves the


10


Table 4: Results of math reasoning. AIME 24&25: avg@16; others: pass@1. Bold denotes the best results.


**Method** **AIME24** **AIME25** **AMC23** **MATH** **Olympiad** **Avg.**


_Qwen3-4B-Base with 1K Length_


GRPO 8.4 5.2 55.1 74.2 42.8 37.1
+ random credit 8.7 5.5 55.2 74.4 42.0 37.1
+ high-entropy credit 8.3 4.9 55.5 74.8 42.5 37.2


_Qwen3-8B-Base with 1K Length_


GRPO 9.3 7.3 59.1 77.1 44.2 39.4
+ random credit 8.9 8.1 60.1 77.4 43.3 39.6
+ high-entropy credit 8.7 7.7 60.4 78.0 45.6 40.1


_Qwen3-4B-Base with 8K Length_


GRPO 19.5 16.1 57.6 81.0 49.9 44.8
+ random credit 18.0 16.6 57.1 82.0 50.0 44.7
+ high-entropy credit 19.3 15.4 57.8 81.2 48.6 44.5



Figure 6: Peak perfo ~~r~~ mance m ~~o~~ ving avera ~~g~~ es of
Top- _k_ versus Bottom- _k_ credit assignment.



credit by different Top-k ratios.



strongest gains across all settings, with the most pronounced improvements on challenging tasks for
Qwen3-8B (e.g., +5.0pt on AIME25, +6.3pt on AMC23). These gains are robust across sequence lengths:
with an extended 8K context, where base GRPO already benefits from longer reasoning traces, it still
delivers consistent improvements (e.g., +4.3pt on AIME25). The curves in Fig. 5 further corroborate these
findings, showing faster convergence and higher final performance for rhythm-aware credit strategies.


**Ablation:** **Top-** _k_ **versus Bottom-** _k_ **.** For proposed metrics, we experiment with reallocating additional
credit to tokens ranked in the bottom 40% according to these metrics. Fig. 6 and Table 5 show that
reinforcing credit on such low-scoring tokens (i.e., those locally dominated or exhibiting minimal global
influence) leads to degraded performance. RL training becomes ineffective, and the peak evaluation
metrics show no improvement on mathematical reasoning. In contrast, preferentially assigning credit to
top- _k_ tokens yields clear improvements. This contrast underscores the validity of our metric in identifying
decisive positions.


**Ablation:** **Top-** _k_ **ratios.** Fig. 7 shows the performance curves of our _coupled rhythm credit_ with different
top- _k_ ratios,, evaluated on multiple mathematical benchmarks using Qwen3-8B-Base. Table 5 shows
the quantitative results. The results confirm that allocating credit exclusively to the top 40% of tokens
(i.e., _k_ = 0.4) yields the strongest overall performance, achieving the highest scores across all datasets
and a peak average of 43.2. Both smaller ( _k_ = 0.2) and larger ( _k ≥_ 0.6) ratios lead to performance drops,
indicating that reinforcing too few or too many tokens dilutes the signal for critical reasoning positions.


11


Table 5: Quantitative ablation results for Top-k vs. Bottom-k credit reallocation and different top-k ratios.


Method AIME24 AIME25 AMC23 MATH500 Olympiad Avg


GRPO (Baseline) 9.3 7.3 59.1 77.1 44.2 39.4


Coupled (Top-20%) 10.1 11.3 58.7 78.0 45.1 40.6
Coupled (Top-60%) 9.0 9.9 59.2 77.7 45.0 40.2
Coupled (Top-80%) 10.5 10.6 58.6 78.1 45.8 40.7
Coupled (Top-100%) 8.1 8.6 60.1 77.5 44.8 39.8


**6** **Conclusion**


We show that analyzing attention dynamics provides a powerful new lens for understanding and
directing LLM reasoning and post-training designs. By analyzing local and global attention, we uncover
a recurring preplan-and-anchor rhythm in LLM reasoning: long-range consultation precedes anchor
tokens that organize downstream inference. We formalize this with two metrics, WAAD and FAI, that
identify preplan and anchor tokens. Using these signals, we design a targeted RL credit assignment
that amplifies rewards on critical nodes: it emphasizes preplan tokens at chunk onsets, amplifies anchor
tokens, and reallocates credit from locally dominant anchors to their corresponding preplan tokens. The
method is plug-and-play with standard RLVR, and yields consistent empirical gains across reasoning
benchmarks compared with uniform credit assignment. More broadly, attention both explains intrinsic
model behaviors and prescribes targeted interventions, opening a path to more transparent, interpretable,
and effective policy optimization of reasoning models.


**Acknowledgment**


This work was in part supported by NSFC 92370201 and Alibaba Group.


12


**References**


Syeda Nahida Akter, Shrimai Prabhumoye, Matvei Novikov, Seungju Han, Ying Lin, Evelina Bakhturina,
Eric Nyberg, Yejin Choi, Mostofa Patwary, Mohammad Shoeybi, et al. Nemotron-crossthink: Scaling
self-learning beyond math reasoning. _arXiv preprint arXiv:2504.13941_, 2025.


Emmanuel Ameisen, Jack Lindsey, Adam Pearce, Wes Gurnee, Nicholas L. Turner, Brian Chen, Craig
Citro, David Abrahams, Shan Carter, Basil Hosmer, Jonathan Marcus, Michael Sklar, Adly Templeton,
Trenton Bricken, Callum McDougall, Hoagy Cunningham, Thomas Henighan, Adam Jermyn, Andy
Jones, Andrew Persic, Zhenyi Qi, T. Ben Thompson, Sam Zimmerman, Kelley Rivoire, Thomas Conerly,
Chris Olah, and Joshua Batson. Circuit tracing: Revealing computational graphs in language models.
_Transformer Circuits Thread_, 2025. URL `[https://transformer-circuits.pub/2025/attribution-gra](https://transformer-circuits.pub/2025/attribution-graphs/methods.html)`
`[phs/methods.html](https://transformer-circuits.pub/2025/attribution-graphs/methods.html)` .


Yuntao Bai, Andy Jones, Kamal Ndousse, Amanda Askell, Anna Chen, Nova DasSarma, Dawn Drain,
Stanislav Fort, Deep Ganguli, Tom Henighan, et al. Training a helpful and harmless assistant with
reinforcement learning from human feedback. _arXiv preprint arXiv:2204.05862_, 2022a.


Yuntao Bai, Saurav Kadavath, Sandipan Kundu, Amanda Askell, Jackson Kernion, Andy Jones, Anna
Chen, Anna Goldie, Azalia Mirhoseini, Cameron McKinnon, Carol Chen, Catherine Olsson, Christopher
Olah, Danny Hernandez, Dawn Drain, Deep Ganguli, Dustin Li, Eli Tran-Johnson, Ethan Perez,
Jamie Kerr, Jared Mueller, Jeffrey Ladish, Joshua Landau, Kamal Ndousse, Kamile Lukosuite, Liane
Lovitt, Michael Sellitto, Nelson Elhage, Nicholas Schiefer, Noemi Mercado, Nova DasSarma, Robert
Lasenby, Robin Larson, Sam Ringer, Scott Johnston, Shauna Kravec, Sheer El Showk, Stanislav Fort,
Tamera Lanham, Timothy Telleen-Lawton, Tom Conerly, Tom Henighan, Tristan Hume, Samuel R.
Bowman, Zac Hatfield-Dodds, Ben Mann, Dario Amodei, Nicholas Joseph, Sam McCandlish, Tom
Brown, and Jared Kaplan. Constitutional ai: Harmlessness from ai feedback, 2022b. URL `[https:](https://arxiv.org/abs/2212.08073)`
`[//arxiv.org/abs/2212.08073](https://arxiv.org/abs/2212.08073)` .


Federico Barbero, lvaro Arroyo, Xiangming Gu, Christos Perivolaropoulos, Michael Bronstein, Petar
Velikovi, and Razvan Pascanu. Why do llms attend to the first token?, 2025. URL `[https://arxiv.org/](https://arxiv.org/abs/2504.02732)`
`[abs/2504.02732](https://arxiv.org/abs/2504.02732)` .


Leonardo Bertolazzi, Philipp Mondorf, Barbara Plank, and Raffaella Bernardi. The validation gap: A
mechanistic analysis of how language models compute arithmetic but fail to validate it, 2025. URL
`[https://arxiv.org/abs/2502.11771](https://arxiv.org/abs/2502.11771)` .


Paul C Bogdan, Uzay Macar, Neel Nanda, and Arthur Conmy. Thought anchors: Which llm reasoning
steps matter? _arXiv preprint arXiv:2506.19143_, 2025.


Vivien Cabannes, Charles Arnal, Wassim Bouaziz, Xingyu Yang, Francois Charton, and Julia Kempe.
Iteration head: A mechanistic study of chain-of-thought. _Advances in Neural Information Processing_
_Systems_, 37:109101–109122, 2024.


Mark Chen, Jerry Tworek, Heewoo Jun, Qiming Yuan, Henrique Ponde De Oliveira Pinto, Jared Kaplan,
Harri Edwards, Yuri Burda, Nicholas Joseph, Greg Brockman, et al. Evaluating large language models
trained on code. _arXiv preprint arXiv:2107.03374_, 2021.


Qiguang Chen, Libo Qin, Jiaqi Wang, Jinxuan Zhou, and Wanxiang Che. Unlocking the capabilities of
thought: A reasoning boundary framework to quantify and optimize chain-of-thought, 2024. URL
`[https://arxiv.org/abs/2410.05695](https://arxiv.org/abs/2410.05695)` .


Daixuan Cheng, Shaohan Huang, Xuekai Zhu, Bo Dai, Wayne Xin Zhao, Zhenliang Zhang, and Furu Wei.
Reasoning with exploration: An entropy perspective. _arXiv preprint arXiv:2506.14758_, 2025.


Paul F Christiano, Jan Leike, Tom Brown, Miljan Martic, Shane Legg, and Dario Amodei. Deep reinforcement learning from human preferences. _Advances in neural information processing systems_, 30,
2017.


Karl Cobbe, Vineet Kosaraju, Mohammad Bavarian, Mark Chen, Heewoo Jun, Lukasz Kaiser, Matthias
Plappert, Jerry Tworek, Jacob Hilton, Reiichiro Nakano, Christopher Hesse, and John Schulman.
Training verifiers to solve math word problems. _arXiv preprint arXiv:2110.14168_, 2021a.


Karl Cobbe, Vineet Kosaraju, Mohammad Bavarian, Mark Chen, Heewoo Jun, Lukasz Kaiser, Matthias
Plappert, Jerry Tworek, Jacob Hilton, Reiichiro Nakano, et al. Training verifiers to solve math word
problems. _arXiv preprint arXiv:2110.14168_, 2021b.


13


Ganqu Cui, Yuchen Zhang, Jiacheng Chen, Lifan Yuan, Zhi Wang, Yuxin Zuo, Haozhan Li, Yuchen Fan,
Huayu Chen, Weize Chen, Zhiyuan Liu, Hao Peng, Lei Bai, Wanli Ouyang, Yu Cheng, Bowen Zhou,
and Ning Ding. The entropy mechanism of reinforcement learning for reasoning language models,
2025. URL `[https://arxiv.org/abs/2505.22617](https://arxiv.org/abs/2505.22617)` .


Tri Dao, Dan Fu, Stefano Ermon, Atri Rudra, and Christopher Re.´ Flashattention: Fast and memoryefficient exact attention with io-awareness. _Advances in neural information processing systems_, 35:16344–
16359, 2022.


Zhichen Dong, Zhanhui Zhou, Zhixuan Liu, Chao Yang, and Chaochao Lu. Emergent response planning
in llms, 2025. URL `[https://arxiv.org/abs/2502.06258](https://arxiv.org/abs/2502.06258)` .


Subhabrata Dutta, Joykirat Singh, Soumen Chakrabarti, and Tanmoy Chakraborty. How to think stepby-step: A mechanistic understanding of chain-of-thought reasoning. _arXiv preprint arXiv:2402.18312_,
2024.


Kawin Ethayarajh, Winnie Xu, Niklas Muennighoff, Dan Jurafsky, and Douwe Kiela. Kto: Model
alignment as prospect theoretic optimization. _arXiv preprint arXiv:2402.01306_, 2024.


Kanishk Gandhi, Ayush Chakravarthy, Anikait Singh, Nathan Lile, and Noah D Goodman. Cognitive
behaviors that enable self-improving reasoners, or, four habits of highly effective stars. _arXiv preprint_
_arXiv:2503.01307_, 2025.


Mor Geva, Jasmijn Bastings, Katja Filippova, and Amir Globerson. Dissecting recall of factual associations
in auto-regressive language models, 2023. URL `[https://arxiv.org/abs/2304.14767](https://arxiv.org/abs/2304.14767)` .


Xiangming Gu, Tianyu Pang, Chao Du, Qian Liu, Fengzhuo Zhang, Cunxiao Du, Ye Wang, and Min
Lin. When attention sink emerges in language models: An empirical view, 2025. URL `[https:](https://arxiv.org/abs/2410.10781)`
`[//arxiv.org/abs/2410.10781](https://arxiv.org/abs/2410.10781)` .


Daya Guo, Dejian Yang, Haowei Zhang, Junxiao Song, Ruoyu Zhang, Runxin Xu, Qihao Zhu, Shirong Ma,
Peiyi Wang, Xiao Bi, et al. Deepseek-r1: Incentivizing reasoning capability in llms via reinforcement
learning. _arXiv preprint arXiv:2501.12948_, 2025.


Shangmin Guo, Biao Zhang, Tianlin Liu, Tianqi Liu, Misha Khalman, Felipe Llinares, Alexandre Rame,
Thomas Mesnard, Yao Zhao, Bilal Piot, Johan Ferret, and Mathieu Blondel. Direct language model
alignment from online ai feedback, 2024. URL `[https://arxiv.org/abs/2402.04792](https://arxiv.org/abs/2402.04792)` .


Tingxu Han, Zhenting Wang, Chunrong Fang, Shiyu Zhao, Shiqing Ma, and Zhenyu Chen. Token-budgetaware llm reasoning, 2025. URL `[https://arxiv.org/abs/2412.18547](https://arxiv.org/abs/2412.18547)` .


Chaoqun He, Renjie Luo, Yuzhuo Bai, Shengding Hu, Zhen Leng Thai, Junhao Shen, Jinyi Hu, Xu Han,
Yujie Huang, Yuxiang Zhang, et al. Olympiadbench: A challenging benchmark for promoting agi with
olympiad-level bilingual multimodal scientific problems. _arXiv preprint arXiv:2402.14008_, 2024.


Dan Hendrycks, Collin Burns, Saurav Kadavath, Akul Arora, Steven Basart, Eric Tang, Dawn Song, and
Jacob Steinhardt. Measuring mathematical problem solving with the math dataset. _arXiv_ _preprint_
_arXiv:2103.03874_, 2021.


Binyuan Hui, Jian Yang, Zeyu Cui, Jiaxi Yang, Dayiheng Liu, Lei Zhang, Tianyu Liu, Jiajun Zhang, Bowen
Yu, Keming Lu, et al. Qwen2. 5-coder technical report. _arXiv preprint arXiv:2409.12186_, 2024.


Carlos E Jimenez, John Yang, Alexander Wettig, Shunyu Yao, Kexin Pei, Ofir Press, and Karthik
Narasimhan. Swe-bench: Can language models resolve real-world github issues? _arXiv_ _preprint_
_arXiv:2310.06770_, 2023.


Nathan Lambert, Jacob Morrison, Valentina Pyatkin, Shengyi Huang, Hamish Ivison, Faeze Brahman,
Lester James V Miranda, Alisa Liu, Nouha Dziri, Shane Lyu, et al. Tulu 3: Pushing frontiers in open
language model post-training. _arXiv preprint arXiv:2411.15124_, 2024.


Nathan Lambert, Jacob Morrison, Valentina Pyatkin, Shengyi Huang, Hamish Ivison, Faeze Brahman,
Lester James V. Miranda, Alisa Liu, Nouha Dziri, Shane Lyu, Yuling Gu, Saumya Malik, Victoria Graf,
Jena D. Hwang, Jiangjiang Yang, Ronan Le Bras, Oyvind Tafjord, Chris Wilhelm, Luca Soldaini, Noah A.
Smith, Yizhong Wang, Pradeep Dasigi, and Hannaneh Hajishirzi. Tulu 3: Pushing frontiers in open
language model post-training, 2025. URL `[https://arxiv.org/abs/2411.15124](https://arxiv.org/abs/2411.15124)` .


Harrison Lee, Samrat Phatale, Hassan Mansoor, Thomas Mesnard, Johan Ferret, Kellie Lu, Colton Bishop,
Ethan Hall, Victor Carbune, Abhinav Rastogi, et al. Rlaif vs. rlhf: Scaling reinforcement learning from
human feedback with ai feedback. _arXiv preprint arXiv:2309.00267_, 2023.


14


Dacheng Li, Shiyi Cao, Tyler Griggs, Shu Liu, Xiangxi Mo, Eric Tang, Sumanth Hegde, Kourosh
Hakhamaneshi, Shishir G Patil, Matei Zaharia, et al. Llms can easily learn to reason from demonstrations structure, not content, is what matters! _arXiv preprint arXiv:2502.07374_, 2025.


Jia Li, Edward Beeching, Lewis Tunstall, Ben Lipkin, Roman Soletskyi, Shengyi Huang, Kashif Rasul,
Longhui Yu, Albert Q Jiang, Ziju Shen, et al. Numinamath: The largest public dataset in ai4maths with
860k pairs of competition math problems and solutions. _Hugging Face repository_, 13(9):9, 2024.


Zicheng Lin, Tian Liang, Jiahao Xu, Qiuzhi Lin, Xing Wang, Ruilin Luo, Chufan Shi, Siheng Li, Yujiu
Yang, and Zhaopeng Tu. Critical tokens matter: Token-level contrastive estimation enhances llm’s
reasoning capability. _arXiv preprint arXiv:2411.19943_, 2024.


Jack Lindsey, Wes Gurnee, Emmanuel Ameisen, Brian Chen, Adam Pearce, Nicholas L. Turner, Craig
Citro, David Abrahams, Shan Carter, Basil Hosmer, Jonathan Marcus, Michael Sklar, Adly Templeton,
Trenton Bricken, Callum McDougall, Hoagy Cunningham, Thomas Henighan, Adam Jermyn, Andy
Jones, Andrew Persic, Zhenyi Qi, T. Ben Thompson, Sam Zimmerman, Kelley Rivoire, Thomas Conerly,
Chris Olah, and Joshua Batson. On the biology of a large language model. _Transformer Circuits Thread_,
2025. URL `[https://transformer-circuits.pub/2025/attribution-graphs/biology.html](https://transformer-circuits.pub/2025/attribution-graphs/biology.html)` .


Xiao Liu, Hao Yu, Hanchen Zhang, Yifan Xu, Xuanyu Lei, Hanyu Lai, Yu Gu, Hangliang Ding, Kaiwen
Men, Kejuan Yang, et al. Agentbench: Evaluating llms as agents. _arXiv preprint arXiv:2308.03688_, 2023.


Zihe Liu, Jiashun Liu, Yancheng He, Weixun Wang, Jiaheng Liu, Ling Pan, Xinyu Hu, Shaopan Xiong,
Ju Huang, Jian Hu, et al. Part i: Tricks or traps? a deep dive into rl for llm reasoning. _arXiv preprint_
_arXiv:2508.08221_, 2025.


Yingwei Ma, Yue Liu, Yue Yu, Yuanliang Zhang, Yu Jiang, Changjian Wang, and Shanshan Li. At which
training stage does code data help llms reasoning?, 2023. URL `[https://arxiv.org/abs/2309.16298](https://arxiv.org/abs/2309.16298)` .


Aman Madaan and Amir Yazdanbakhsh. Text and patterns: For effective chain of thought, it takes two to
tango. _arXiv preprint arXiv:2209.07686_, 2022.


Tianyi Men, Pengfei Cao, Zhuoran Jin, Yubo Chen, Kang Liu, and Jun Zhao. Unlocking the future:
Exploring look-ahead planning mechanistic interpretability in large language models, 2024. URL
`[https://arxiv.org/abs/2406.16033](https://arxiv.org/abs/2406.16033)` .


Yu Meng, Mengzhou Xia, and Danqi Chen. Simpo: Simple preference optimization with a reference-free
reward. _Advances in Neural Information Processing Systems_, 37:124198–124235, 2024.


Hosein Mohebbi, Willem Zuidema, Grzegorz Chrupaa, and Afra Alishahi. Quantifying context mixing in
transformers, 2023. URL `[https://arxiv.org/abs/2301.12971](https://arxiv.org/abs/2301.12971)` .


OpenAI. Learning to reason with llms, 2024. URL `[https://openai.com/index/learning-to-reaso](https://openai.com/index/learning-to-reason-with-llms/)`
`[n-with-llms/](https://openai.com/index/learning-to-reason-with-llms/)` .


OpenAI, :, Sandhini Agarwal, Lama Ahmad, Jason Ai, Sam Altman, Andy Applebaum, Edwin Arbus,
Rahul K. Arora, Yu Bai, Bowen Baker, Haiming Bao, Boaz Barak, Ally Bennett, Tyler Bertao, Nivedita
Brett, Eugene Brevdo, Greg Brockman, Sebastien Bubeck, Che Chang, Kai Chen, Mark Chen, Enoch
Cheung, Aidan Clark, Dan Cook, Marat Dukhan, Casey Dvorak, Kevin Fives, Vlad Fomenko, Timur
Garipov, Kristian Georgiev, Mia Glaese, Tarun Gogineni, Adam Goucher, Lukas Gross, Katia Gil
Guzman, John Hallman, Jackie Hehir, Johannes Heidecke, Alec Helyar, Haitang Hu, Romain Huet,
Jacob Huh, Saachi Jain, Zach Johnson, Chris Koch, Irina Kofman, Dominik Kundel, Jason Kwon,
Volodymyr Kyrylov, Elaine Ya Le, Guillaume Leclerc, James Park Lennon, Scott Lessans, Mario
Lezcano-Casado, Yuanzhi Li, Zhuohan Li, Ji Lin, Jordan Liss, Lily, Liu, Jiancheng Liu, Kevin Lu, Chris
Lu, Zoran Martinovic, Lindsay McCallum, Josh McGrath, Scott McKinney, Aidan McLaughlin, Song
Mei, Steve Mostovoy, Tong Mu, Gideon Myles, Alexander Neitz, Alex Nichol, Jakub Pachocki, Alex
Paino, Dana Palmie, Ashley Pantuliano, Giambattista Parascandolo, Jongsoo Park, Leher Pathak,
Carolina Paz, Ludovic Peran, Dmitry Pimenov, Michelle Pokrass, Elizabeth Proehl, Huida Qiu, Gaby
Raila, Filippo Raso, Hongyu Ren, Kimmy Richardson, David Robinson, Bob Rotsted, Hadi Salman,
Suvansh Sanjeev, Max Schwarzer, D. Sculley, Harshit Sikchi, Kendal Simon, Karan Singhal, Yang Song,
Dane Stuckey, Zhiqing Sun, Philippe Tillet, Sam Toizer, Foivos Tsimpourlas, Nikhil Vyas, Eric Wallace,
Xin Wang, Miles Wang, Olivia Watkins, Kevin Weil, Amy Wendling, Kevin Whinnery, Cedric Whitney,
Hannah Wong, Lin Yang, Yu Yang, Michihiro Yasunaga, Kristen Ying, Wojciech Zaremba, Wenting
Zhan, Cyril Zhang, Brian Zhang, Eddie Zhang, and Shengjia Zhao. gpt-oss-120b & gpt-oss-20b model
card, 2025. URL `[https://arxiv.org/abs/2508.10925](https://arxiv.org/abs/2508.10925)` .


15


Long Ouyang, Jeffrey Wu, Xu Jiang, Diogo Almeida, Carroll Wainwright, Pamela Mishkin, Chong Zhang,
Sandhini Agarwal, Katarina Slama, Alex Ray, et al. Training language models to follow instructions
with human feedback. _Advances in neural information processing systems_, 35:27730–27744, 2022.


Jiayi Pan, Junjie Zhang, Xingyao Wang, Lifan Yuan, Hao Peng, and Alane Suhr. Tinyzero.
https://github.com/Jiayi-Pan/TinyZero, 2025. Accessed: 2025-01-24.


Rafael Rafailov, Archit Sharma, Eric Mitchell, Christopher D Manning, Stefano Ermon, and Chelsea Finn.
Direct preference optimization: Your language model is secretly a reward model. _Advances in neural_
_information processing systems_, 36:53728–53741, 2023.


Jie Ren, Qipeng Guo, Hang Yan, Dongrui Liu, Quanshi Zhang, Xipeng Qiu, and Dahua Lin. Identifying
semantic induction heads to understand in-context learning, 2024. URL `[https://arxiv.org/abs/24](https://arxiv.org/abs/2402.13055)`
`[02.13055](https://arxiv.org/abs/2402.13055)` .


John Schulman, Philipp Moritz, Sergey Levine, Michael Jordan, and Pieter Abbeel. High-dimensional
continuous control using generalized advantage estimation. _arXiv preprint arXiv:1506.02438_, 2015.


John Schulman, Filip Wolski, Prafulla Dhariwal, Alec Radford, and Oleg Klimov. Proximal policy
optimization algorithms. _arXiv preprint arXiv:1707.06347_, 2017.


John Schulman, Barret Zoph, Christina Kim, Jacob Hilton, Jacob Menick, Jiayi Weng, Juan Felipe Ceron
Uribe, Liam Fedus, Luke Metz, Michael Pokorny, et al. Chatgpt: Optimizing language models for
dialogue. _OpenAI blog_, 2(4), 2022.


Zhihong Shao, Peiyi Wang, Qihao Zhu, Runxin Xu, Junxiao Song, Xiao Bi, Haowei Zhang, Mingchuan
Zhang, YK Li, Yang Wu, et al. Deepseekmath: Pushing the limits of mathematical reasoning in open
language models. _arXiv preprint arXiv:2402.03300_, 2024.


Zhiqing Sun, Yikang Shen, Qinhong Zhou, Hongxin Zhang, Zhenfang Chen, David Cox, Yiming Yang,
and Chuang Gan. Principle-driven self-alignment of language models from scratch with minimal
human supervision. _Advances in Neural Information Processing Systems_, 36:2511–2565, 2023.


Kimi Team, Angang Du, Bofei Gao, Bowei Xing, Changjiu Jiang, Cheng Chen, Cheng Li, Chenjun Xiao,
Chenzhuang Du, Chonghua Liao, et al. Kimi k1. 5: Scaling reinforcement learning with llms. _arXiv_
_preprint arXiv:2501.12599_, 2025.


Alexander Matt Turner, Lisa Thiergart, Gavin Leech, David Udell, Juan J. Vazquez, Ulisse Mini, and
Monte MacDiarmid. Steering language models with activation engineering, 2024. URL `[https:](https://arxiv.org/abs/2308.10248)`
`[//arxiv.org/abs/2308.10248](https://arxiv.org/abs/2308.10248)` .


Jean Vassoyan, Nathanael Beau, and Roman Plaud.¨ Ignore the kl penalty! boosting exploration on critical
tokens to enhance rl fine-tuning. _arXiv preprint arXiv:2502.06533_, 2025.


Constantin Venhoff, Ivan´ Arcuschin, Philip Torr, Arthur Conmy, and Neel Nanda. Understanding
reasoning in thinking language models via steering vectors. _arXiv preprint arXiv:2506.18167_, 2025.


Boshi Wang, Sewon Min, Xiang Deng, Jiaming Shen, You Wu, Luke Zettlemoyer, and Huan Sun. Towards
understanding chain-of-thought prompting: An empirical study of what matters. _arXiv_ _preprint_
_arXiv:2212.10001_, 2022.


Boshi Wang, Sewon Min, Xiang Deng, Jiaming Shen, You Wu, Luke Zettlemoyer, and Huan Sun. Towards
understanding chain-of-thought prompting: An empirical study of what matters, 2023. URL `[https:](https://arxiv.org/abs/2212.10001)`
`[//arxiv.org/abs/2212.10001](https://arxiv.org/abs/2212.10001)` .


Jiawei Wang, Jiacai Liu, Yuqian Fu, Yingru Li, Xintao Wang, Yuan Lin, Yu Yue, Lin Zhang, Yang Wang,
and Ke Wang. Harnessing uncertainty: Entropy-modulated policy gradients for long-horizon llm
agents. _arXiv preprint arXiv:2509.09265_, 2025a.


Peiyi Wang, Lei Li, Zhihong Shao, R. X. Xu, Damai Dai, Yifei Li, Deli Chen, Y. Wu, and Zhifang
Sui. Math-shepherd: Verify and reinforce llms step-by-step without human annotations, 2024. URL
`[https://arxiv.org/abs/2312.08935](https://arxiv.org/abs/2312.08935)` .


Shenzhi Wang, Le Yu, Chang Gao, Chujie Zheng, Shixuan Liu, Rui Lu, Kai Dang, Xionghui Chen, Jianxin
Yang, Zhenru Zhang, et al. Beyond the 80/20 rule: High-entropy minority tokens drive effective
reinforcement learning for llm reasoning. _arXiv preprint arXiv:2506.01939_, 2025b.


Weixun Wang, Shaopan Xiong, Gengru Chen, Wei Gao, Sheng Guo, Yancheng He, Ju Huang, Jiaheng
Liu, Zhendong Li, Xiaoyang Li, et al. Reinforcement learning optimization for large-scale learning: An
efficient and user-friendly scaling library. _arXiv preprint arXiv:2506.06122_, 2025c.


16


Xuezhi Wang and Denny Zhou. Chain-of-thought reasoning without prompting. In A. Globerson,
L. Mackey, D. Belgrave, A. Fan, U. Paquet, J. Tomczak, and C. Zhang (eds.), _Advances_ _in_ _Neural_
_Information_ _Processing_ _Systems_, volume 37, pp. 66383–66409. Curran Associates, Inc., 2024. URL
```
 https://proceedings.neurips.cc/paper files/paper/2024/file/7a8e7fd295aa04eac4b470ae2
```

`[7f8785c-Paper-Conference.pdf](https://proceedings.neurips.cc/paper_files/paper/2024/file/7a8e7fd295aa04eac4b470ae27f8785c-Paper-Conference.pdf)` .


Ronald J Williams. Simple statistical gradient-following algorithms for connectionist reinforcement
learning. _Machine learning_, 8(3):229–256, 1992.


Yotam Wolf, Binyamin Rothberg, Dorin Shteyman, and Amnon Shashua. Compositional hardness of
code in large language models – a probabilistic perspective, 2025. URL `[https://arxiv.org/abs/2409](https://arxiv.org/abs/2409.18028)`
`[.18028](https://arxiv.org/abs/2409.18028)` .


Guangxuan Xiao, Yuandong Tian, Beidi Chen, Song Han, and Mike Lewis. Efficient streaming language
models with attention sinks. _arXiv preprint arXiv:2309.17453_, 2023.


Huajian Xin, Z. Z. Ren, Junxiao Song, Zhihong Shao, Wanjia Zhao, Haocheng Wang, Bo Liu, Liyue Zhang,
Xuan Lu, Qiushi Du, Wenjun Gao, Qihao Zhu, Dejian Yang, Zhibin Gou, Z. F. Wu, Fuli Luo, and Chong
Ruan. Deepseek-prover-v1.5: Harnessing proof assistant feedback for reinforcement learning and
monte-carlo tree search, 2024. URL `[https://arxiv.org/abs/2408.08152](https://arxiv.org/abs/2408.08152)` .


An Yang, Beichen Zhang, Binyuan Hui, Bofei Gao, Bowen Yu, Chengpeng Li, Dayiheng Liu, Jianhong Tu,
Jingren Zhou, Junyang Lin, et al. Qwen2. 5-math technical report: Toward mathematical expert model
via self-improvement. _arXiv preprint arXiv:2409.12122_, 2024.


An Yang, Anfeng Li, Baosong Yang, Beichen Zhang, Binyuan Hui, Bo Zheng, Bowen Yu, Chang Gao,
Chengen Huang, Chenxu Lv, et al. Qwen3 technical report. _arXiv preprint arXiv:2505.09388_, 2025a.


Sohee Yang, Elena Gribovskaya, Nora Kassner, Mor Geva, and Sebastian Riedel. Do large language
models latently perform multi-hop reasoning?, 2025b. URL `[https://arxiv.org/abs/2402.16837](https://arxiv.org/abs/2402.16837)` .


Shunyu Yao, Noah Shinn, Pedram Razavi, and Karthik Narasimhan. _τ_ -bench: A benchmark for toolagent-user interaction in real-world domains. _arXiv preprint arXiv:2406.12045_, 2024.


Qiying Yu, Zheng Zhang, Ruofei Zhu, Yufeng Yuan, Xiaochen Zuo, Yu Yue, Weinan Dai, Tiantian Fan,
Gaohong Liu, Lingjun Liu, et al. Dapo: An open-source llm reinforcement learning system at scale.
_arXiv preprint arXiv:2503.14476_, 2025.


Yu Yue, Yufeng Yuan, Qiying Yu, Xiaochen Zuo, Ruofei Zhu, Wenyuan Xu, Jiaze Chen, Chengyi Wang,
TianTian Fan, Zhengyin Du, et al. Vapo: Efficient and reliable reinforcement learning for advanced
reasoning tasks. _arXiv preprint arXiv:2504.05118_, 2025.


Chujie Zheng, Shixuan Liu, Mingze Li, Xiong-Hui Chen, Bowen Yu, Chang Gao, Kai Dang, Yuqiong Liu,
Rui Men, An Yang, Jingren Zhou, and Junyang Lin. Group sequence policy optimization, 2025. URL
`[https://arxiv.org/abs/2507.18071](https://arxiv.org/abs/2507.18071)` .


Zifan Zheng, Yezhaohui Wang, Yuxin Huang, Shichao Song, Mingchuan Yang, Bo Tang, Feiyu Xiong, and
Zhiyu Li. Attention heads of large language models: A survey. _arXiv preprint arXiv:2409.03752_, 2024.


Daniel M Ziegler, Nisan Stiennon, Jeffrey Wu, Tom B Brown, Alec Radford, Dario Amodei, Paul Christiano, and Geoffrey Irving. Fine-tuning language models from human preferences. _arXiv_ _preprint_
_arXiv:1909.08593_, 2019.


17


**Appendix**


**A** **Experimental Details**


**A.1** **Analysis in Sec. 4**


For experimental validation, we analyze attention dynamics using **Qwen3-4B-Base** (Yang et al., 2025a)
on prompts from the **GSM8K** dataset (Cobbe et al., 2021a), with sampling temperature _T_ = 0.7. Each
prompt is constructed by first providing the system instruction: `System:` `Please` `reason` `step` `by` `step,`
`and` `put` `your` `final` `answer` `within` _\_ `boxed` _{}_ `.` We then decompose the problem into a `Context` and a
`Question` field, as illustrated in Prompt A.1.


We first generate a response using standard autoregressive decoding. Once the full response is obtained,
we concatenate it with the original prompt and perform a _single_ _additional_ _forward_ _pass_ through the
model-using an eager attention implementation-to extract the full attention maps via the Hugging Face
`transformers` library. From this, we isolate the attention patterns corresponding to the response tokens
for analysis.


In computing the Windowed Attention Activation Density (WAAD), we set the temporal window size
to _W_ = 10, as we are primarily interested in local attention dependencies. For the Forward Attention
Influence (FAI) metric, we define the influence scope to span from each token position to the end of the
response.


Our analysis comprises two components: (i) For quantification analysis (e.g., Tables 1 and 2), we randomly
sample 70 GSM8K problems and examine the relationship between attention-based metrics across all
generated tokens; (ii) For qualitative analysis (e.g., Fig. 2), we select the problem with the shortest correct
response to facilitate clear and interpretable plots. The full prompt and model response for this example
are provided below:


The response for analysis is:





**Experimental** **Details** **of** **Table** **2.** Table 2 reports correlation analyses between the attention-based
metrics visualized in Fig. 2. The specific protocols for computing these correlations are as follows:


  - **Average** **Entropy** **of** **the** **WAAD** **Peaks:** We compute the average entropy at token positions
identified as WAAD peaks (reported as “observed”) and compare it against the average entropy
over all response tokens (reported as “random”). A higher observed value indicates that WAAD
peaks correspond to positions of significantly greater uncertainty.

  - **Receiver & Global FAI Peak Co-occurrence:** We measure the alignment between peaks identified
by receiver-head FAI (Bogdan et al., 2025) and those identified by global-head FAI. Specifically,
we report the fraction of receiver FAI peaks that overlap with global FAI peaks (reported as
“observed”). The “random” baseline denotes the expected overlap if receiver FAI peaks were
uniformly distributed across all response positions, i.e., the proportion of Global FAI peaks
among all tokens. An increase over this baseline signifies strong structural correspondence
between the two FAI variants.

  - **FAI Follows/Coincides with WAAD Peak:** We evaluate the extent to which FAI peaks coincide
with or immediately follow WAAD peaks. The “observed” value is the proportion of FAI


18


peaks satisfying this temporal condition relative to all FAI peaks. The “random” baseline is the
expectation by randomly shuffling FAI peak positions (preserving their count) and recomputing
the overlap. A higher observed value demonstrates non-random alignment between attention
activation density and forward influence.


**A.2** **RL Experiments in Sec. 5**


**Dataset.** For _Countdown_, we follow the data construction protocol of Pan et al. (2025) and use a test set
of 512 instances (each containing four input numbers), along with a training set of 20,000 samples. The
_CrossThink-QA_ dataset is sourced from Akter et al. (2025). For mathematical reasoning tasks, models are
trained on DAPO-Math-17K (Yu et al., 2025).


**Benchmark** **Details.** We evaluate our method across a spectrum of reasoning tasks, ranging from
relatively simple puzzles and general question-answering (QA) to challenging mathematical reasoning
benchmarks. Specifically, our evaluation suite includes:


- _Countdown_ (Pan et al., 2025): A symbolic reasoning puzzle in which the model is given four integers and
must construct a valid arithmetic expression using basic operations (+, _−_, _×_, _÷_ ) to reach a specified
target number. This task tests compositional planning and precise execution under constraints.

- _CrossThink-QA_ (Akter et al., 2025): A diverse, multi-domain QA dataset that aggregates questions from
heterogeneous sources (e.g., science, commonsense, and trivia), designed to assess general-purpose
reasoning and knowledge integration across domains.

- _Mathematical Reasoning Benchmarks_ : Five established datasets spanning a wide range of difficulty and
problem types:

**–** **AIME24** and **AIME25** : Collections of problems from the American Invitational Mathematics
Examination (2024 and 2025) [1], featuring non-routine problems requiring multi-step insight.

**–** **AMC** (Li et al., 2024): Problems from the American Mathematics Competitions, emphasizing
logical deduction and problem-solving under time constraints.

**–** **MATH500** (Hendrycks et al., 2021): A set of 500 challenging problems from the MATH dataset,
covering algebra, geometry, number theory, and combinatorics.

**–** **OlympiadBench** (He et al., 2024): A recent collection of international mathematical olympiad-level
problems, representing the frontier of machine reasoning in mathematics.


This diverse set of tasks enables us to assess both the generalizability and the depth of our method across
reasoning modalities and complexity levels.


**Plot Setup.** The performance curves are smoothed via an Exponential Moving Average (EMA): EMA _t_ =
_α ·_ max( _xt_, EMA _t−_ 1) + (1 _−_ _α_ ) _·_ EMA _t−_ 1, which reflects a running average of peak performance. When
the best performance is continually updated, the curve keeps rising; if performance stalls, the curve stays
flat. The curve’s endpoint therefore represents a relatively stable peak performance.


**B** **Supplementary Results**


**B.1** **Representative Perturbation Examples**


We present illustrative cases where token perturbations at high-FAI versus low-FAI positions lead to
qualitatively different reasoning behaviors. All examples use the same input prompt:


The original response by greedy decoding is:


1 `[https://maa.org/](https://maa.org/)`


19


We now perform perturbations at high-FAI positions, selecting other tokens from the top-k candidates
and rolling out continuations to observe how the subsequent reasoning trajectory changes.







In the example above, we observe a notable shift in the reasoning logic. Structurally, the response skips
the initial planning phase and jumps directly into computation, abandoning the original plan-then-solve
format. Moreover, the computational approach itself differs substantially. For instance, by framing the
problem in terms of sets of yogurts rather than per-unit cost. Despite these changes, the final answer
remains correct. Nevertheless, when compared to the original response, the content-word overlap at the
token level is only 0.383, indicating significant divergence in the reasoning trajectory. We observe that
sometimes the change to the token may appear minor, yet the model still frequently attends back to this
position internally. Thus, even when the surface semantics seem alike, it can exert a disproportionately
large influence on subsequent reasoning.


20


In this example, when we replace the token at the same position with the third-highest-probability
candidate, we observe that the model’s reasoning completely deviates from the correct path, leading to
an incorrect final answer. When compared to the original response, the content-word overlap at the token
level is only 0.255, indicating significant divergence in the reasoning trajectory.


Next, we examine the effects of perturbing low-FAI tokens by comparing the resulting reasoning trajectories after substitution. This allows us to assess how changes to less influential tokens impact the model’s
subsequent reasoning.







In this case, we observe a particularly interesting phenomenon: when replacing the token “over” in
“over 30 days” with “in”, the only change occurs at that specific position, and the subsequent reasoning
trajectory remains completely unchanged. The Jaccard similarity between the perturbed and original
outputs is 1.00, indicating identical content-word sets. This suggests that the choice of token at this
position is governed purely by local syntactic or stylistic preferences and exerts no influence on the global
reasoning process.


21


The example above exhibits the same pattern: the token replacement affects only the local phrasing, while
the overall reasoning logic remains essentially unchanged. The model follows the same solution strategy,
performs identical calculations, and arrives at the same final answer, confirming that such low-FAI tokens
typically serve a surface-level role without altering the core inference trajectory.


**B.2** **Visualization of FAI and WAAD Distributions on Tokens**


We visualize the token-level distributions of FAI and WAAD by directly outputting responses to randomly
sampled math problems from GSM8K, computing FAI and WAAD for each token, and encoding their
magnitudes via color intensity. As shown in Fig 8, tokens with high FAI typically retain intermediate
reasoning results, while tokens with high WAAD often mark the beginning of a new reasoning chunk
for the model. We also observe that punctuation tokens, such as commas, periods, and line breaks,
consistently attract elevated attention weights across multiple layers and heads. We hypothesize that this
phenomenon arises because punctuation marks appear periodically in the generated text and serve as
natural syntactic and semantic boundaries. The attention mechanism, being sensitive to such regular
structural cues, tends to form recurrent connections between these tokens. Thus, at these points, the
model consolidates contextual evidence from preceding tokens and redistributes summarized signals to
guide subsequent reasoning steps.


22


**Case 1**


**Case 2**


Figure 8: Visualization cases of the token-level distributions of FAI and WAAD.


23


