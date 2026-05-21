## **ThinkBrake: Efficient Reasoning via Log-Probability Margin** **Guided Decoding**

**Sangjun Song** _[∗]_ **, Minjae Oh** _[∗]_ **, Seungkyu Lee** _[‡]_ **, Sungmin Jo** _[§]_ **, Yohan Jo** _[†]_

Graduate School of Data Science, Seoul National University
{ssangjun706, kosair, gyuu01, jsm0424, yohan.jo}@snu.ac.kr



**Abstract**


Large Reasoning Models (LRMs) allocate substantial inference-time compute to Chain-ofThought (CoT) reasoning, improving performance on mathematics, scientific QA, and
tool usage. However, this introduces _over-_
_thinking_ : LRMs often reach a correct intermediate solution, continue reasoning, and
overwrite it with an incorrect answer. We
first demonstrate that oracle stopping—where
we inject </think> at every sentence boundary and select the best stopping point in
hindsight—improves average accuracy by 8%
while reducing thinking tokens by 72%, exposing substantial overthinking. Motivated
by this finding, we propose THINKBRAKE,
which monitors the log-probability margin between the top continuation token and </think>
at sentence boundaries, stopping reasoning
when this margin narrows. THINKBRAKE requires no training and achieves favorable accuracy–efficiency trade-offs across math, scientific QA, and tool usage benchmarks, reducing thinking token usage by up to 30%.
Furthermore, we provide theoretical analysis
showing that THINKBRAKE is equivalent to
test-time realignment with a reward bonus for
the </think>. Code is available at [https:](https://github.com/holi-lab/ThinkBrake)
[//github.com/holi-lab/ThinkBrake.](https://github.com/holi-lab/ThinkBrake)


**1** **Introduction**


Recent progress in Large Reasoning Models
(LRMs) (OpenAI, 2024; Guo et al., 2025; Yang
et al., 2025) has demonstrated remarkable capabilities across various tasks such as mathematics, scientific QA, and tool usage. By allocating inferencetime computation through Chain-of-Thought (CoT)
reasoning (Wei et al., 2022), LRMs demonstrate behaviors like self-correction and iterative refinement,


_∗_ Equal contribution _†_ Corresponding author.

_‡_ Visiting intern from Department of Industrial Engineering,
Seoul National University.
_§_ Visiting intern from Department of Computer Science and
Engineering, Seoul National University.



actively improving performance with increased token usage (Chen et al., 2025; Xu et al., 2025).
However, this increased inference-time compute
raises practical concerns about _efficient reasoning_
(Feng et al., 2025), as longer trajectories introduce
higher latency and costs. More critically, it introduces _overthinking_ (Zhang et al., 2025a): LRMs
frequently reach a correct intermediate step, only
to continue deliberating and overwrite it with an
incorrect final output (see Figure 1, left panel).
We first conduct a preliminary oracle analysis
to validate that overthinking is a genuine problem
and that LRMs would benefit from early termination of reasoning. Leveraging the fact that recent
LRMs use special tokens <think> and </think>
to wrap reasoning (where </think> triggers answer generation), we inject </think> at every sentence boundary, forcing early termination at each
possible reasoning step (see §2). Across mathematical reasoning benchmarks (GSM8K, MATH500,
AIME2024, AIME2025) and tool usage (Berkeley
Function Calling Leaderboard; BFCL), this oracle
approach achieves an average accuracy gain of 8%
while reducing reasoning tokens by 72%. This gap
reveals substantial recoverable headroom: many
failures can be prevented simply by stopping at the
right moment (see Figure 1, right panel).
Motivated by this oracle analysis, we introduce
THINKBRAKE, a practical approach to early stopping. THINKBRAKE monitors the log-probability
margin between </think> and the current top token at sentence boundaries, stopping reasoning
when this margin narrows. THINKBRAKE is modelagnostic, requiring only an explicit reasoning format with </think>. While prior works have explored test-time methods for reasoning efficiency
(Li et al., 2025; Wang et al., 2025; Laaouach,
2025), they often rely on hand-crafted heuristics.
In contrast, we provide a theoretical foundation
for THINKBRAKE, showing it is equivalent to KLregularized test-time realignment that assigns a


How many values can be obtained from 2 ∙3 ∙4 ∙5 + 1 by inserting parentheses?



**<think>** Okay, let’s see… The addition ‘+’ is fixed
between 5 and 1… The possible ‘sum terms’ depend
only on the prefix product: (5 + 1), (4 ∙5 + 1),

(3 ∙4 ∙5 + 1), (2 ∙3 ∙4 ∙5 + 1)… This leads to exactly

**4 distinct values** : 144, 126, 122, 121… **Wait, I should**
**check all 14 permutations of Catalan 4… </think>**
**The answer is 14.**



**User**


**<think>** Okay, let’s see… The addition ‘+’ is fixed
between 5 and 1… The possible ‘sum terms’ depend
only on the prefix product: (5 + 1), (4 ∙5 + 1),

(3 ∙4 ∙5 + 1), (2 ∙3 ∙4 ∙5 + 1)… This leads to exactly

**4 distinct values** : 144, 126, 122, 121. **</think>**


**Stop Thinking!**

**The answer is 4.**



**LRMs**



Figure 1: An example of LRM overthinking (left). The LRM arrives at the correct solution of 4, but continues
reasoning after “Wait” and overwrites it with an incorrect answer of 14. Appropriate early termination via </think>
injection removes overthinking and leads to the correct answer (right).



reward bonus to </think>, pushing the LRM towards concise reasoning (see §3.2).
We evaluate THINKBRAKE on six LRMs across
four mathematical reasoning benchmarks (GSM8K,
MATH500, AIME2024, AIME2025), two additional reasoning benchmarks (GPQA-Diamond,
ARC-Challenge), and two tool usage benchmarks
(BFCL, Meta-Tool), demonstrating consistent efficiency gains with competitive accuracy (see §4).
We show that THINKBRAKE preserves accuracy
uniformly across problem difficulties, rather than
trading off performance on easy versus hard instances. Furthermore, THINKBRAKE-generated
trajectories can serve as training data for Direct Preference Optimization (DPO). This enables
LRMs to internalize concise reasoning without
inference-time intervention and achieve improved
efficiency with only a small amount of training data
(see §4.4). Our contributions are:


  - We identify and quantify overthinking in
LRMs via oracle </think> rollouts, quantifying recoverable headroom across mathematical reasoning and tool usage (see §2).


  - We introduce THINKBRAKE, a test-time inference method based on a log-margin criterion at sentence boundaries, with theoretical
grounding as KL-regularized test-time realignment assigning a reward bonus to </think>
(see §3).


  - We validate THINKBRAKE across six LRMs
and eight benchmarks spanning mathematical,
scientific, and tool-use reasoning, and show
its generated data enables efficient reasoning
via DPO (see §4).



**2** **Overthinking in LRMs**


To validate that overthinking is a genuine problem and quantify the potential gains from early
stopping, we analyze whether LRMs would have
answered correctly had reasoning been terminated
earlier. We conduct controlled rollouts with forced
termination by injecting </think> at every sentence boundary, causing the model to stop thinking and produce an answer. We mark a trajectory
as _recoverable_ if it contains a sentence boundary
where the model has reached the correct answer
but continues reasoning and eventually produces an
incorrect one. This yields an _oracle_ accuracy—the
achievable accuracy with hindsight knowledge of
the optimal stopping point (see Appendix B for an
example).
We use Qwen3-4B-Thinking (Yang et al., 2025)
as our base LRM and evaluate across mathematical reasoning (GSM8K (Cobbe et al., 2021),
MATH500 (Hendrycks et al., 2021), AIME2024,
AIME2025 (Art of Problem Solving, 2025)) and
tool usage (BFCL-v1 (Patil et al., 2025)). Detailed
experiment settings are in Appendix C.
In Figure 2, oracle stopping reduces error rate
to 6% on mathematical reasoning and 5% on tool
usage, improving over the baseline by 8% while
reducing thinking token usage by 54% on mathematics and 89% on tool usage. Remarkably, the
improvements are consistent across difficulty levels; even on the challenging AIME benchmarks,
oracle stopping recovers 61% of failures while cutting tokens by 44%. Notably, fewer than 5% of
errors are irrecoverable for most benchmarks, confirming that a substantial portion of failures stem
from overthinking rather than inability.


Base Oracle





20


15


10


5


0



25


20


15


10


5


0


|Col1|Col2|Col3|Col4|2.9|Col6|23.8|Col8|23.8|Col10|Col11|Col12|Col13|Col14|Col15|Col16|Col17|Col18|Col19|Col20|Col21|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|||||2|2||||||||||||||||
|||||2|||||||||||||||||
|||||||3.3|3.3||8|8|8||||||||||
|||||||1|1||11.<br>|11.<br>|11.<br>|9.5<br>.5|9.5<br>.5|9.5<br>.5|||9.5|9.5|||
||||||||||||||||||||||
||||||||||||||||||||||
|4.9<br>|4.9<br>|4.7<br>|4.7<br>||||||6.7|6.7||8|8||6.5<br>|6.5<br>|4.0||4.5|4.5|
|4.9<br>|4.9<br>|4.7<br>|4.7<br>||||||6.7|6.7|||||||||||
|4.9<br>|4.9<br>|4.7<br>|4.7<br>||||||||||||||||||
|||2.2||0.2|||||||||||1.5||||||


|×103|Col2|Col3|Col4|Col5|17|Col7|Col8|Col9|Col10|Col11|Col12|Col13|Col14|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
||||19294|19294|213|213|213|||||||
||||19294|19294|213|213||||||||
||||||67|67||17|17|||||
||0|0|||112|112||116|116|||||
||0|0||||||||||||
|8|636<br>|636<br>|44||||||2||9|1||
|8|636<br>|||||||||||||
|157<br>|487||25||||||107<br>|965<br>200<br>|119<br>62<br>|162<br>124<br>|160|



Figure 2: Oracle experiments via sentence-boundary </think> injection on mathematical reasoning (GSM8K,
MATH500, AIME2024, AIME2025) and tool usage (BFCL-v1). Optimal termination yields both improved error
rate (left) and reduced thinking token usage (right). See Table 12 for a tabular version.



**3** **THINKBRAKE**


**3.1** **Intuition and Definition**


We propose THINKBRAKE, a simple early termination method that injects the </think> when the
log-probability margin between the top-predicted
token and </think> becomes small. Formally, let
_πθ_ be our LRM, _x_ be the input, and _y<t_ be the
current reasoning chain. At each sentence boundary, let _yt_ _[⋆]_ [=] [arg max] _[y]_ _[π][θ]_ [(] _[y]_ _[|]_ _[x]_ [;] _[ y][<t]_ [)][ be the top-]
predicted token that is not </think>. We terminate
model thinking when:


_πθ_ ( _yt_ _[⋆]_ _[|][ x]_ [;] _[ y][<t]_ [)]
log (1)
_πθ_ (</think> _| x_ ; _y<t_ ) _[≤]_ _[τ,]_


where _τ_ is a hyperparameter that controls the stopping threshold. The intuition is that as productive
reasoning concludes, the probability margin between continuing and stopping narrows. While
THINKBRAKE considers only the top token, it naturally accounts for different levels of overall token
entropy, as we justify through the following exhaustive cases:


**Case** **1:** **Termination** **state.** The model
assigns the highest probability to </think>
( _pθ_ (</think>) _>_ _pθ_ ( _yt_ _[⋆]_ [)][),] [so] [termination occurs]
regardless of THINKBRAKE.


**Case 2:** **High-entropy state.** The model spreads
probability across many tokens, indicating genuine
uncertainty. Early stopping here risks premature
termination of productive reasoning, so we should
stop as conservatively as possible. Using _yt_ _[⋆]_ [as the]
reference is the most conservative choice, as it by
definition carries the largest probability.



**Case 3:** **Low-entropy state.** The model concentrates probability on one or a few tokens, indicating
high raw probability of _yt_ _[⋆]_ [.] [If] [</think>] [is] [com-]
parably probable, it too carries high probability–
meaning the model genuinely considers stopping
as an option and productive reasoning has ended.
Termination in this case is therefore natural.

For comparison, we also consider a linear
probability-gap variant (THINKBRAKE-p) that triggers when _pθ_ ( _yt_ _[⋆]_ [)] _[ −]_ _[p][θ]_ [(][</think>][)] _[≤]_ _[τ]_ [prob][.] [This]
variant proves significantly less effective (see
§4.2). Furthermore, we validate the dynamics of
THINKBRAKE with respect to entropy and compare its difference against THINKBRAKE-p in Appendix D.


**3.2** **Theoretical Analysis**


We theoretically ground THINKBRAKE by showing it is equivalent to a logit margin test, which
can be interpreted as test-time realignment via a
KL-regularized policy with a reward bonus for
</think>.


**Log-space** **margins** **equal** **logit** **margins.** We
first show that THINKBRAKE is equivalent to a
_logit margin_ test. For brevity, let _e_ := </think>
denote the stop token and _st_ := ( _x_ ; _y<t_ ) denote the
decoding state. Let _zθ_ ( _y_ _|_ _st_ ) be the pre-softmax
logit for token _y_ in the vocabulary _V_ at state _st_ .
With decoding temperature _T_ _>_ 0, the next-token
distribution is:


exp� _zθ_ ( _y_ _| st_ ) _/T_         _πθ_ ( _y_ _| st_ ) =  - _y_ _[′]_ [ exp]  - _zθ_ ( _y_ _[′]_ _| st_ ) _/T_  - _._ (2)


Taking the log-ratio between any two tokens cancels the normalization:



log _[π][θ]_ [(] _[a][ |][ s][t]_ [)]




_[π][θ]_ [(] _[a][ |][ s][t]_ [)] _[z][θ]_ [(] _[a][ |][ s][t]_ [)] _[ −]_ _[z][θ]_ [(] _[b][ |][ s][t]_ [)]

_πθ_ ( _b | st_ ) [=] _T_



_._ (3)
_T_



Let _yt_ _[⋆]_ := arg max _y∈V\{e} zθ_ ( _y_ _|_ _st_ ) be the best
continuation token (excluding _e_ ). The _log-space_
_stopping margin_ is

_t_ _[|][ s][t]_ [)] _t_ _[|][ s][t]_ [)] _[ −]_ _[z][θ]_ [(] _[e][ |][ s][t]_ [)]
_mt_ := log _[π][θ]_ [(] _[y][⋆]_ _[z][θ]_ [(] _[y][⋆]_ _._
_πθ_ ( _e | st_ ) [=] _T_

(4)


Therefore, THINKBRAKE is exactly a temperaturescaled _logit margin test_ between the best continuation token and </think>.


**THINKBRAKE** **as** **test-time** **realignment.** We
now formalize THINKBRAKE as optimizing a KLregularized policy that prefers emitting </think>.
Let _B_ denote the set of sentence boundary states
where THINKBRAKE may terminate. At a boundary state _st_ _∈_ _B_, consider the general KLregularized objective with hyperparameter _β_ _>_ 0:


_π_ ˜ _θ_ ( _· | st_ ) = arg _π_ max( _·|st_ ) [E] _[y][∼][π]_ [(] _[·|][s][t]_ [)][[] _[r]_ [(] _[s][t][, y]_ [)]]


_−_ _β_ KL( _π_ ( _· | st_ ) _∥πθ_ ( _· | st_ )) _._
(5)


The closed-form optimal policy is given by (Korbak et al., 2022; Rafailov et al., 2023):




         - _r_ ( _st, y_ )

_π_ ˜ _θ_ ( _y_ _| st_ ) = [1] _πθ_ ( _y_ _| st_ ) exp

_Zt_ _β_




_._ (6)



**Equivalence to the THINKBRAKE margin test.**
Under greedy decoding from the realigned policy
at _st_ _∈B_, it selects _e_ if and only if


_zθ_ ( _e | st_ ) + _τT_ _≥_ _zθ_ ( _yt_ _[⋆]_ _[|][ s][t]_ [)]

_t_ _[|][ s][t]_ [)] _[ −]_ _[z][θ]_ [(] _[e][ |][ s][t]_ [)]
_τ_ _≥_ _[z][θ]_ [(] _[y][⋆]_

_T_
_mt_ _≤_ _τ,_ (10)


where _mt_ is defined in Eq. (4). This is exactly
THINKBRAKE. For non-boundary states _st_ _∈B/_,
THINKBRAKE applies no realignment and decodes
from _πθ_ ( _· | st_ ) as usual.


**4** **Experiments**


**4.1** **Experimental Setup**


We evaluate several models for our main experiments: Qwen3-4B-Thinking, Qwen3-4B, Qwen314B, Qwen3-32B (Yang et al., 2025), DeepSeekR1-7B (Guo et al., 2025), and Phi-4-Reasoning
(Abdin et al., 2025). Qwen3-32B is a model posttrained with reinforcement learning (RL), while the
smaller Qwen models are trained via supervised
fine-tuning. DeepSeek-R1-7B is a Qwen2.5-based
model distilled from DeepSeek-R1-generated reasoning traces. Phi-4-Reasoning is derived from Phi4 through supervised fine-tuning on curated reasoning demonstrations. All models use default reasoning format with explicit <think> and </think>
delimiters.
We compare against NoWait (Wang et al., 2025),
which suppresses filler tokens like "wait" and
"hmm"; ThinkLess (Li et al., 2025), which forces
immediate </think> emission after <think>;
Dynasor-CoT (Fu et al., 2025), which extracts intermediate answers and applies early stopping based
on consistency; DEER (Yang et al., 2026), which
also interrupts mid-thinking and stops based on
entropy; and THINKBRAKE-p (§3.1). Details in
Appendix C.5.
We report both task accuracy and thinking token reduction. We measure _thinking tokens_ as tokens generated within the reasoning span (between
<think> and </think>). We report ∆Tok as the
percentage change in thinking tokens relative to
baseline decoding for the same model and benchmark. Detailed baseline methods, implementation
settings, and system prompts are provided in Appendix C.


**Selecting Hyperparameter** _τ_ **.** THINKBRAKE introduces a single hyperparameter, _τ_, which controls



We define the reward to make the KL-regularized
objective equivalent to THINKBRAKE’s logit margin test in Eq. (1).


_rτ_ ( _st, y_ ) := _τβ ·_ **1** [ _y_ = _e_ ] _._ (7)


Plugging Eq. (7) into Eq. (6) gives exp( _rτ_ _/β_ ) =
exp( _τ_ **1** [ _y_ = _e_ ]), so the realignment simply upweights </think> by a factor _e_ _[τ]_ .
We now show that setting _β_ = _T_ yields a direct
connection to logit margins. Since _πθ_ ( _·_ _|_ _st_ ) is a
softmax over logits, Eq. (6) with _β_ = _T_ is equivalent to _logit shaping_ . Define the shaped logit:


_z_ ˜ _θ,τ_ ( _y_ _| st_ ) := _zθ_ ( _y_ _| st_ ) + _rτ_ ( _st, y_ ) _,_ (8)


where _rτ_ ( _st, y_ ) = _τT_ _·_ **1** [ _y_ = _e_ ] under our choice
of _β_ = _T_ . Then the realigned policy becomes:


_π_ ˜ _θ,τ_ ( _y_ _| st_ ) = softmax(˜ _zθ,τ_ ( _y_ _| st_ ) _/T_ ) _._ (9)


Thus, at boundary states, the realigned policy is
exactly the base model with a constant bonus _τT_
added to the </think> logit.


GSM8K MATH500 AIME2024 AIME2025 GPQA-D ARC-C Avg.


Model Acc ∆Tok Acc ∆Tok Acc ∆Tok Acc ∆Tok Acc ∆Tok Acc ∆Tok Acc ∆Tok


Qwen3-4B-Thinking 95.1 - 95.3 - 77.1 - 76.2 - 64.1 - 94.3 - 83.7 + NoWait 94.2 -25.1% 96.4 -17.9% 66.7 -30.5% 66.7 -35.6% 68.2 -19.6% 92.7 14.6% 80.8 -19.0%
+ ThinkLess 92.6 -100% 56.4 -100% 3.3 -100% 3.3 -100% 50.0 -100% 94.2 -100% 50.0 -100%
+ DEER 95.1 -34.1% 94.4 -14.2% 63.3 -34.3% 60.0 -37.9% 68.2 -1.3% 92.8 -9.0% 79.0 -21.8%
+ Dynasor-CoT 95.2 -34.0% 87.2 -42.1% 63.3 -28.8% 53.3 -28.9% 62.6 -22.6% 94.5 -39.1% 76.0 -23.0%
+ THINKBRAKE-p 93.9 -37.3% 91.2 -57.9% 35.0 -72.6% 30.4 -76.0% 47.0 -67.5% 93.7 -31.7% 65.2 -57.2%
+ THINKBRAKE 94.8 -18.9% 96.6 -20.4% 67.2 -33.5% 62.8 -33.4% 62.6 -32.7% 94.0 -19.9% 79.7 -26.5%


Qwen3-4B 94.4 - 96.0 - 68.8 - 59.6 - 51.0 - 94.0 - 77.3 + NoWait 94.5 -40.4% 94.6 -31.4% 56.7 -16.6% 50.0 -27.1% 57.6 -26.6% 93.4 -14.4% 74.5 -26.1%
+ THINKBRAKE 94.5 -30.1% 95.4 -14.4% 64.6 -12.7% 60.4 -13.5% 55.6 -29.7% 93.9 -11.5% 77.4 -18.7%


Qwen3-14B 96.0 - 96.8 - 71.7 - 69.2 - 60.6 - 95.9 - 81.7 + NoWait 95.8 -29.4% 95.2 -25.1% 70.0 -19.8% 56.7 -16.6% 62.1 -20.5% 96.2 -8.1% 79.3 -19.9%
+ THINKBRAKE 95.0 -15.4% 96.9 -7.7% 77.9 -7.4% 65.8 -6.0% 61.1 -39.9% 95.2 -18.2% 82.0 -15.8%


Qwen3-32B 96.0 - 97.0 - 75.8 - 68.3 - 65.2 - 92.1 - 82.4 + NoWait 95.3 -23.6% 95.8 -20.6% 66.7 -12.0% 56.7 -10.6% 60.1 -12.4% 90.1 9.0% 77.5 -11.7%
+ THINKBRAKE 96.5 -9.1% 97.2 -1.4% 77.1 -6.2% 68.3 -4.3% 65.7 -19.9% 91.0 -8.0% 82.6 -8.2%


DeepSeek-R1-7B 92.7 - 93.8 - 49.5 - 37.6 - 48.0 - 67.7 - 64.9 + NoWait 90.6 -30.8% 91.2 -31.0% 40.0 -32.4% 26.7 -36.5% 43.4 -35.5% 64.6 -12.6% 59.4 -29.8%
+ THINKBRAKE 92.4 -25.0% 92.0 -23.2% 45.2 -25.0% 33.2 -20.3% 45.5 -51.2% 70.7 -35.3% 63.2 -30.0%


Phi-4-Reasoning 91.7 - 71.1 - 67.5 - 63.7 - 62.6 - 80.0 - 72.8 + NoWait 92.1 -2.4% 70.8 -17.7% 63.3 -9.4% 53.3 -8.6% 63.1 -19.1% 77.6 -7.0% 70.0 -10.7%
+ THINKBRAKE 91.7 -25.6% 70.4 -17.2% 73.3 -6.4% 53.3 -5.2% 67.7 -1.1% 80.0 -25.3% 72.7 -13.5%


Table 1: Math and science results on GSM8K, MATH500, AIME2024, AIME2025, GPQA-D, and ARC-C. We
report accuracy and ∆Tok (thinking token reduction vs. the base decoding) for each model. For AIME2024
and AIME2025, which contain only 30 questions, we report results over 32 runs and also report the variance
and confidence intervals. For brevity we only show the baseline method for the Qwen3-4B-Thinking model. A
comprehensive result table including baseline methods is in Appendix E.



40


30


20


10


0



Baseline 0.1 0.25 1.0 2.5 10.0 25.0
Threshold



100


80


60


40


20


0



Figure 3: _τ_ search from error rate and thinking token
usage for THINKBRAKE on Qwen3-4B-Thinking.


how aggressively we terminate reasoning at sentence boundaries. Increasing _τ_ encourages earlier
emission of </think>, yielding fewer thinking tokens, but overly large values can truncate useful
reasoning and degrade accuracy. To choose a default threshold without per-benchmark tuning, we
perform a lightweight sweep over _τ_ on a small validation split. Concretely, we evaluate Qwen3-4BThinking across a grid of _τ_ values on a subset of the



DAPO17K (Yu et al., 2025) dataset and record both
error rate and thinking token reduction compared
to baseline decoding.

Figure 3 shows that at _τ_ =0 _._ 1, THINKBRAKE
achieves both reduced error rate and substantial
token reduction compared to baseline. Beyond
this point, error rate increases and token usage decreases smoothly as _τ_ increases further. Notably,
while error rate is lowest at _τ_ =0 _._ 1, it remains competitive for _τ_ values up to 1.0, demonstrating robustness to the choice of threshold. We therefore
select _τ_ =0 _._ 1 and apply it to all Qwen3 model sizes
and all benchmarks. Our results show that this
threshold generalizes well out-of-distribution from
mathematical reasoning to other tasks. Similarly,
we select optimal _τ_ values for DeepSeek-R1-7B
( _τ_ =0 _._ 1) and Phi-4-Reasoning ( _τ_ =2 _._ 5) using the
same procedure (see Appendix C.6 for details).


**4.2** **Main Results**


**Math** **&** **Science** **Reasoning.** We evaluate on
four math benchmarks: GSM8K (Cobbe et al.,
2021), MATH500 (Hendrycks et al., 2021),
AIME2024, AIME2025 (Art of Problem Solving,


BFCL-v1 BFCL-v2 Meta-Tool


Model Parallel Multi-Parallel Parallel Multi-Parallel Single Multiple Avg.


Acc ∆Tok Acc ∆Tok Acc ∆Tok Acc ∆Tok Acc ∆Tok Acc ∆Tok Acc ∆Tok


Qwen3-4B-Thinking 93.5 - 90.5 - 87.5 - 79.2 - 69.7 - 85.5 - 84.3 + NoWait 88.5 -44.4% 88.5 -53.5% 81.3 -50.7% 75.0 -66.5% 68.9 0.1% 84.7 -11.2% 81.2 -37.7%
+ ThinkLess 79.5 -100% 83.0 -100% 37.5 -100% 45.8 -100% 67.4 -100% 86.5 -100% 66.6 -100%
+ THINKBRAKE-p 78.0 -26.9% 42.5 -33.4% 62.5 -28.5% 29.2 -43.8% 70.8 -25.8% 86.7 -12.7% 61.6 -28.5%
+ THINKBRAKE 95.5 -26.8% 90.5 -28.2% 87.5 -32.3% 87.5 -18.9% 72.4 -20.6% 86.3 -9.0% 86.6 -22.6%


Qwen3-4B 90.0 - 83.0 - 81.2 - 70.8 - 74.3 - 90.5 - 81.6 + NoWait 88.0 -13.5% 84.0 1.2% 75.0 -5.1% 75.0 -11.1% 72.5 -3.1% 90.5 -8.4% 80.8 -6.7%
+ THINKBRAKE 89.5 -16.5% 83.5 -12.0% 62.5 -21.1% 75.0 -10.2% 72.7 -1.4% 91.1 -3.0% 79.0 -10.7%


Qwen3-14B 92.0 - 83.5 - 62.5 - 70.8 - 63.3 - 84.9 - 76.2 + NoWait 90.0 -16.3% 84.0 1.8% 62.5 -30.1% 62.5 -10.9% 61.2 -2.4% 84.5 -5.8% 74.1 -10.6%
+ THINKBRAKE 93.0 -21.2% 85.0 -14.2% 62.5 -25.4% 62.5 -7.6% 66.3 -1.6% 85.7 -4.5% 75.8 -12.4%


Qwen3-32B 93.0 - 85.0 - 68.8 - 70.8 - 64.8 - 84.3 - 77.8 + NoWait 91.0 -13.0% 82.5 -5.0% 68.8 -3.9% 62.5 -14.3% 63.8 3.6% 83.9 1.3% 75.4 -5.2%
+ THINKBRAKE 91.0 -14.3% 90.0 -7.3% 68.8 -4.6% 58.0 -13.3% 64.4 -1.5% 85.5 -1.1% 76.3 -7.0%


DeepSeek-R1-7B 52.5 - 38.0 - 43.8 - 29.2 - 63.2 - 80.3 - 51.2 + NoWait 62.0 -4.0% 42.5 -6.9% 50.0 -8.9% 20.8 11.0% 64.9 0.6% 73.2 -19.3% 52.2 -4.6%
+ THINKBRAKE 42.0 -14.6% 37.0 -11.6% 43.8 -19.9% 16.7 -6.0% 63.4 -7.4% 76.3 -26.3% 46.5 -14.3%


Phi-4-Reasoning 87.5 - 77.5 - 81.2 - 58.3 - 77.7 - 90.5 - 78.8 + NoWait 81.0 -1.3% 75.5 -13.2% 81.2 -6.4% 58.3 -11.9% 76.6 -8.5% 90.9 -15.4% 77.2 -9.5%
+ THINKBRAKE 84.5 2.7% 77.5 -6.4% 75.0 4.6% 70.8 -4.9% 77.2 -2.5% 90.3 -5.4% 79.2 -2.0%


Table 2: Results on BFCL-v1, BFCL-v2, and Meta-Tool benchmarks. Simple and Multiple scenarios in BFCL
are omitted for brevity. We report accuracy and ∆Tok (token reduction) for parallel and multi-parallel scenarios
in BFCL, and single and multiple selection scenarios in Meta-Tool. A comprehensive result table including all
baseline methods is in Appendix E.



2025). We also consider a scientific reasoning
benchmark and a general reasoning benchmark:
GPQA-D (Rein et al., 2024), ARC-Challenge
(Clark et al., 2018). For AIME benchmarks, we
provide 32 run results with confidence intervals for
Qwen3-4B-Thinking and DeepSeek-R1-7B (see
Appendix E).

Table 1 shows that THINKBRAKE consistently achieves strong accuracy-efficiency tradeoffs across all models and difficulties. On easier
benchmarks (GSM8K, MATH500), THINKBRAKE
reduces tokens by 10–30% while maintaining
or improving accuracy. On challenging AIME
benchmarks, THINKBRAKE maintains competitive performance with substantial token savings—notably improving accuracy for Qwen3-14B
and Phi-4-Reasoning on AIME2024, suggesting
THINKBRAKE prevents overthinking.

In contrast, baseline methods show various limitations. ThinkLess (which removes all thinking)
causes catastrophic drops on hard math: _∼_ 40%
drop on MATH500 and _∼_ 73% drop on AIME2024
for Qwen3-4B-Thinking, highlighting the need for
reasoning in such tasks. NoWait degrades less
severely but still drops notably on challenging
AIME compared to THINKBRAKE. Dynasor-CoT



shows high performance degradation on benchmarks like AIME; while it often reduces more tokens, this comes at the cost of substantially larger
performance degradation. DEER shows competitive performance but still degrades on benchmarks
like AIME compared to THINKBRAKE.

An apparent pattern across model scales is that
larger models require less aggressive stopping.
Average token reduction decreases from 26.5%
(Qwen3-4B-Thinking) to 15.8% (14B) to 8.2%
(32B). To verify this trend of diminishing gains as
model size scales, we further evaluate on a larger
model: Qwen3-Next-80B. Surprisingly, we observe a substantial 22.3% token reduction, breaking
the apparent trend. We therefore attribute the diminishing reductions from 4B to 32B not to model
size, but to reasoning trace length, as larger models
tend to produce shorter traces, leaving less redundant thinking to prune. The 80B model, despite
being the largest, generates longer traces than the
32B model and correspondingly yields greater reductions. See Appendix E for a further analysis.


**Tool Usage.** We evaluate on BFCL non-live (v1),
live (v2) (Patil et al., 2025) and Meta-Tool (Huang
et al., 2024). Tool usage results show different pat

terns, as ThinkLess—which failed catastrophically
on math—performs reasonably on some simpler
tool usage scenarios, suggesting function calling
benefits less from extended reasoning than mathematical domains.
However, on challenging scenarios, baseline
heuristics can degrade performance. On BFCLv2 with Qwen3-4B-Thinking, ThinkLess suffers
catastrophic drops on parallel tasks ( _∼_ 50% drop)
and multi-parallel tasks ( _∼_ 33% drop). NoWait
shows modest degradation with a _∼_ 7% drop on
parallel and _∼_ 5% drop on multi-parallel. In contrast, THINKBRAKE maintains robust performance
across all scenarios. On BFCL-v2, THINKBRAKE
matches baseline accuracy on parallel tasks with
32.3% token reduction, and notably improves multiparallel performance by _∼_ 8%. This demonstrates
that THINKBRAKE’s adaptive stopping criterion
successfully prevents overthinking on complex
tool usage scenarios where simpler heuristics fail.
These results show that THINKBRAKE generalizes
effectively beyond mathematical and scientific reasoning to tool usage tasks.


**Logarithmic** **Margin** **Design.** As discussed in
§3.1, we compare THINKBRAKE with its linear
probability-gap variant THINKBRAKE-p: _pθ_ ( _yt_ _[⋆]_ [)] _[−]_
_pθ_ (</think>) _≤_ _τ_ prob. Tables 1 and 2 show
that THINKBRAKE-p exhibits substantial accuracy drops on challenging tasks like AIME–
achieving only 30–35% on AIME compared to
THINKBRAKE’s 62–67%—while performing comparably on easier tasks like GSM8K with Qwen34B-Thinking.
This is likely because the log-ratio formulation
requires the absolute probabilities of both _yt_ _[⋆]_ [and]
</think> to be sufficiently large to trigger termination. When both probabilities are low, a small logmargin is harder to achieve—the two must be far
more similar in relative terms than when both are
high. As a result, THINKBRAKE terminates model
thinking conservatively when the model is uncertain, and primarily when it is confident (see Appendix D). In contrast, raw probability differences
lack this adaptive property, causing premature termination during uncertain reasoning states and
leading to significant accuracy degradation on challenging tasks. These results validate that the logspace formulation is essential for THINKBRAKE’s
robustness on hard reasoning tasks.


**Premature** **Exiting** **and** **Spurious** **Reasoning.**
While THINKBRAKE largely preserves baseline



Benchmark Oracle THINKBRAKE


AIME2024 11,261 12,830
AIME2025 11,618 14,197


Table 3: Average tokens for Oracle and THINKBRAKE
on Qwen3-4B-Thinking. THINKBRAKE exits later than
the oracle for both AIME2024 and AIME2025.


accuracy, we observe slight performance degradation on highly complex benchmarks (e.g., AIME,
GPQA-D) for specific models such as Qwen34B-Thinking and DeepSeek-R1-7B. To determine
whether this stems from premature termination, a
vulnerability in confidence-based early-exit methods, we compare THINKBRAKE’s stopping points
against an oracle setting. As shown in Table 3,
THINKBRAKE consistently generates more tokens
than the oracle before exiting, indicating that it does
not suffer from premature termination in practice,
and is using sufficient reasoning budgets.
Consequently, we attribute these accuracy drops
not to insufficient reasoning, but to _spurious rea-_
_soning_ . Because harder benchmarks naturally elicit
longer reasoning traces, they pose a greater risk
for the model to engage in flawed or contradictory logic _after_ successfully solving the problem,
but only before THINKBRAKE triggers termination.
This explains why the observed degradation is primarily concentrated in benchmarks characterized
by extended reasoning lengths. We provide further results and a qualitative example of spurious
reasoning in Appendix E.


**4.3** **Ablation Studies**


**Hyperparameter** **Sensitivity.** We further analyze THINKBRAKE across test sets with various thresholds ( _τ_ _∈{_ 0 _._ 1 _,_ 0 _._ 25 _,_ 1 _._ 0 _,_ 2 _._ 5 _,_ 10 _}_ ) for
Qwen3-4B-Thinking. Figure 4 shows that accuracy
remains stable until very high thresholds ( _τ_ _≥_ 10),
while token reduction increases monotonically with
_τ_ . Although a single threshold works reasonably
well across various tasks within model families,
optimal thresholds vary by task difficulty. Easier tasks like MATH500 and tool usages maintain
accuracy with higher _τ_, while challenging GPQAD shows sensitivity to increasing _τ_, suggesting
we can use more aggressive _τ_ for easier tasks to
maximize token reduction. As a practical rule of
thumb, _τ_ = 0 _._ 1 works well across almost all modelbenchmark pairs; for new settings, one can increase
_τ_ for easier tasks to maximize token efficiency or
maintain a low _τ_ for harder ones to preserve accuracy. See Appendix E for full results.


100


80


60


40


20


0


|5.3% 96.6% 5.9%|Col2|Col3|Col4|5.6% 4.6% .2%|Col6|Col7|Col8|Col9|%|Col11|Col12|Col13|Col14|Col15|Col16|Col17|Col18|Col19|Col20|Col21|Col22|Col23|Col24|Col25|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|9<br><br>9<br>|9<br><br>9<br>|9<br><br>9<br>|9<br><br>9<br>|%<br><br>9<br>9<br>92|%<br><br>9<br>9<br>92|%<br><br>9<br>9<br>92|%<br><br>9<br>9<br>92|%<br><br>9<br>9<br>92|82.5%<br>85.0<br>82.7%<br>|82.5%<br>85.0<br>82.7%<br>|82.5%<br>85.0<br>82.7%<br>|82.5%<br>85.0<br>82.7%<br>|82.5%<br>85.0<br>82.7%<br>|5.0%<br>77.0%<br><br>76.6%<br>82.0%<br><br>81.8%<br>81.5%|5.0%<br>77.0%<br><br>76.6%<br>82.0%<br><br>81.8%<br>81.5%|5.0%<br>77.0%<br><br>76.6%<br>82.0%<br><br>81.8%<br>81.5%|5.0%<br>77.0%<br><br>76.6%<br>82.0%<br><br>81.8%<br>81.5%|5.0%<br>77.0%<br><br>76.6%<br>82.0%<br><br>81.8%<br>81.5%|5.0%<br>77.0%<br><br>76.6%<br>82.0%<br><br>81.8%<br>81.5%|5.0%<br>77.0%<br><br>76.6%<br>82.0%<br><br>81.8%<br>81.5%|76.9%<br>77.5%<br>76.9%|76.9%<br>77.5%<br>76.9%|76.9%<br>77.5%<br>76.9%|76.9%<br>77.5%<br>76.9%|
|9<br><br>9<br>|||||||||||||||||||||||||
|||||||64.1<br>62.6%<br>57.6%<br>|64.1<br>62.6%<br>57.6%<br>|64.1<br>62.6%<br>57.6%<br>|60.1%<br>61.6%<br>.5%|60.1%<br>61.6%<br>.5%|60.1%<br>61.6%<br>.5%||||||7<br>|7<br>|||||||
||||||||||||52||||||||||||||
||||||||||||||||||||||||||
||||||||||||||||||||||||||


|×10 3|Col2|Col3|Col4|8455|Col6|Col7|Col8|Col9|Col10|Col11|Col12|Col13|Col14|Col15|Col16|Col17|Col18|Col19|Col20|Col21|Col22|Col23|Col24|Col25|Col26|Col27|Col28|Col29|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|||||8|8|8|8|8|8|8|||||||||||||||||||
|||||8|8|8|8||||||||||||||||||||||
|6360|6360|6360|6360||||||5991<br>728<br>|5991<br>728<br>|71|71|71|71|71|71|71||||||||||||
|||4910<br>4760<br>|4910<br>4760<br>|4328<br>3916|4328<br>3916|4328<br>3916|4328<br>3916|||5<br>|53<br>4864<br>602|53<br>4864<br>602|53<br>4864<br>602|53<br>4864<br>602|53<br>4864<br>602|53<br>4864<br>602|53<br>4864<br>602||||||||||||
|||4910<br>4760<br>|4910<br>4760<br>|4328<br>3916|4328<br>3916|4328<br>3916|4328<br>3916|||5<br>|||||||||||||||||||
||||||||||||||||||||||||||||||
|||||||2462|2462||||||1697<br>1376<br>1364<br><br>3|1697<br>1376<br>1364<br><br>3|1697<br>1376<br>1364<br><br>3|1697<br>1376<br>1364<br><br>3|1697<br>1376<br>1364<br><br>3|1743<br>1436<br>1427<br>1332<br><br>1304<br>1219|1743<br>1436<br>1427<br>1332<br><br>1304<br>1219|1743<br>1436<br>1427<br>1332<br><br>1304<br>1219|1743<br>1436<br>1427<br>1332<br><br>1304<br>1219|1743<br>1436<br>1427<br>1332<br><br>1304<br>1219|1743<br>1436<br>1427<br>1332<br><br>1304<br>1219|1743<br>1436<br>1427<br>1332<br><br>1304<br>1219|1423<br>1390<br>1223|1423<br>1390<br>1223|1423<br>1390<br>1223|1423<br>1390<br>1223|
|||||||2462|2462||||||||||||||||||||||
||||||||||||||||||||||||||||||
||||||||||||||||||||||||||||||



MATH500 GPQA-D BFCL-V2 META-TOOL



Baseline = 0.1 = 0.25 = 1.0 = 2.5 = 10.0


8


6


4


2



0
MATH500 GPQA-D BFCL-V2 META-TOOL



Figure 4: Hyperparameter sensitivity for Qwen3-4B-Thinking over MATH500, GPQA-D and tool usages. Accuracy
remains robust except for extreme case _τ_ = 10 (left). Token reduction increases with _τ_ (right).



100


80


60


40


20


0



|Col1|Col2|Col3|Col4|Col5|Col6|Col7|Col8|Col9|Col10|Col11|
|---|---|---|---|---|---|---|---|---|---|---|
|||||||||Think<br>Base<br>|Brake<br>||
|||||||||~~robl~~|~~m Co~~|~~ unt~~|
||||||||||||
||||||||||||
||||||||||||


1 2 3 4 5 6 7 8 9 10
Difficulty



1200


1000


800


600


400


200


0



Figure 5: Accuracy by difficulty on Omni-MATH.
THINKBRAKE maintains uniform performance across
all levels. Grey bars show problem counts.


**Performance Across Problem Difficulties.** We
investigate whether THINKBRAKE trades performance between easy and hard problems, using the
Omni-MATH dataset (Gao et al., 2024), which
provides difficulty labels from 1 to 10. Figure 5
shows THINKBRAKE maintains or improves accuracy uniformly across all difficulty levels without any trade-off. Notably, THINKBRAKE shows
greater improvements on harder problems, suggesting that overthinking is more prevalent in challenging questions. We hypothesize that LRMs, uncertain about harder problems, continue generating
spurious verification steps even after reaching a
correct answer. This validates that efficiency gains
come from preventing overthinking rather than sacrificing performance on hard problems. To further
quantify how often early stopping changes correctness, we compute prediction transition matrices
before and after THINKBRAKE (see Appendix E).
Across models, most examples remain unchanged
(correct→correct or incorrect→incorrect), indicating THINKBRAKE primarily reduces computation
without substantial accuracy trade-offs.



Benchmark Base DPO ∆Tok


GSM8K 95.1 95.2 -23.6%
MATH500 95.3 96.7 -27.7%
AIME2024 77.1 80.7 -8.8%
AIME2025 76.2 76.0 -9.5%
GPQA-D 64.1 61.5 -16.2%
ARC-C 94.3 93.8 -20.8%


BFCL-v1 88.3 88.0 -16.6%
BFCL-v2 82.5 83.6 -10.5%
Meta-Tool 75.0 76.1 -23.9%


Table 4: Benchmark results for Qwen3-4B-Thinking
trained with DPO on THINKBRAKE-generated data.


**4.4** **Training from THINKBRAKE Data**


Since THINKBRAKE generates concise trajectories
that maintain or improve accuracy, we investigate
whether this data can be used to train LRMs for
efficient reasoning. We apply Direct Preference Optimization (DPO; Rafailov et al., 2023) to Qwen34B-Thinking, treating THINKBRAKE trajectories
as preferred and baseline trajectories as rejected.
We construct 1.3K preference pairs from OmniMATH problems. The training is highly efficient
as it requires only 20 minutes on 2 _×_ H200 GPUs
(see Appendix C.3 for details).

Table 4 shows that DPO training successfully
transfers THINKBRAKE’s efficiency to the LRM.
Despite training only on mathematical reasoning,
the model achieves 9–28% thinking token reduction across all benchmarks while maintaining accuracy. Notably, improvements transfer to harder
math problems (AIME), and to entirely out-ofdomain tasks including GPQA-D, ARC-C, and tool
usage. This demonstrates that the model learns general concise reasoning patterns rather than memorizing task-specific solutions, enabling efficient
training of LRMs with minimal data and compute.


**5** **Related Work**


**5.1** **Concise Reasoning**


As LRMs often generate excessive tokens, recent
work has studied efficient reasoning methods.


**Test-Time** **Methods.** Several training-free approaches have been proposed, including sampling
answers at each step using consistency as an earlystop signal (Mao et al., 2025; Liu and Wang, 2025;
Wan et al., 2025), employing external verifiers
(Jiang et al., 2025), or leveraging model representations via probing (Fu et al., 2025) and signals
like confidence (Yang et al., 2026) and entropy
(Laaouach, 2025). Other heuristics include suppressing reflection tokens (e.g., “Wait”, “Hmm”)
(Wang et al., 2025) or skipping explicit reasoning
entirely (Li et al., 2025). While effective in some
cases, these methods typically rely on hand-crafted
rules or require additional computational overhead
from multiple rollouts or external models.


**Training** **Methods.** An alternative approach
trains models to produce concise traces directly.
Kang et al. (2025) compress long CoT and condition models to generate shorter reasoning, while
subsequent work (Fang et al., 2025; Song and
Zheng, 2025; Fatemi et al., 2025; Aggarwal and
Welleck, 2025) presents RL frameworks for concise reasoning. However, these require significant
computational resources and can potentially destabilize general model performance.


**5.2** **Logit-Based Test-Time Realignment**


A complementary literature explores test-time realignment without retraining by applying logitspace shifts to the base model. Unlike heuristic test-time methods, these approaches implement principled objectives—such as RLHF alignment—directly at decoding time via logit manipulation. One line of work constructs such shifts using
signals from aligned and base models (Mitchell
et al., 2024; Liu et al., 2024a), with controllable
strength at decoding time (Liu et al., 2024b), while
related logit interventions can elicit specific abilities like reasoning (Zhang et al., 2025b). Another line leverages decoding-time steering for
user-specific objectives, including modular rewards
(Huang et al., 2025) or expert combinations (Liu
et al., 2021). Overall, these logit-based methods provide a theoretically grounded and flexible mechanism for test-time behavior control.



THINKBRAKE falls within this framework: we implement a KL-regularized realignment objective
that assigns a reward bonus to </think>, enabling
principled concise reasoning.


**6** **Conclusion**


We study overthinking in Large Reasoning Models across mathematical reasoning, scientific QA,
and tool usage. Oracle experiments reveal that
LRMs often reach correct intermediate solutions
but fail to terminate, leaving substantial headroom
for improved accuracy and efficiency. We introduce THINKBRAKE, a training-free decoding rule
that triggers </think> based on log-probability
margins at sentence boundaries. THINKBRAKE
achieves favorable accuracy-efficiency trade-offs
across multiple model families and benchmarks, is
theoretically grounded as KL-regularized test-time
realignment, and can train more efficient models
via preference optimization.


**Limitations**


THINKBRAKE comes with several limitations.
First, THINKBRAKE requires explicit reasoning
delimiters (<think> and </think>) and access to
model logits, which may not be available in models with hidden chain-of-thought or black-box API
settings. Second, the method introduces a hyperparameter _τ_ that, while robust across a range of
values, may require tuning in some settings. Finally, THINKBRAKE uses a local stopping criterion
based on probability margins and does not explicitly reason about global answer correctness, which
may lead to early termination when the model is
confidently wrong.


**Acknowledgements**


This work was supported by the National Research Foundation of Korea (NRF) grant (RS2024-00333484) and by the Institute of Information & Communications Technology Planning &
Evaluation (IITP) grant (RS-2025-02215122, Development and Demonstration of Lightweight AI
Model for Smart Homes), all funded by the Korean government (MSIT). This research was also
supported by the Korea Institute of Science and
Technology Information (KISTI) in 2026 (No.
(KISTI)K26L3M1C1), aimed at developing KONI
(KISTI Open Neural Intelligence), a large language
model specialized in science and technology.


**References**


Marah Abdin, Sahaj Agarwal, Ahmed Awadallah,
Vidhisha Balachandran, Harkirat Behl, Lingjiao
Chen, Gustavo de Rosa, Suriya Gunasekar, Mojan Javaheripi, Neel Joshi, and 1 others. 2025.
Phi-4-reasoning technical report. _arXiv_ _preprint_
_arXiv:2504.21318_ .


Pranjal Aggarwal and Sean Welleck. 2025. L1: [Con-](https://openreview.net/forum?id=4jdIxXBNve)
[trolling how long a reasoning model thinks with re-](https://openreview.net/forum?id=4jdIxXBNve)
[inforcement learning.](https://openreview.net/forum?id=4jdIxXBNve) In _Second Conference on Lan-_
_guage Modeling_ .


Art of Problem Solving. 2025. AIME [problems](https://artofproblemsolving.com/wiki/index.php/AIME_Problems_and_Solutions) and
[solutions.](https://artofproblemsolving.com/wiki/index.php/AIME_Problems_and_Solutions) Accessed: 2026-1-02.


Qiguang Chen, Libo Qin, Jinhao Liu, Dengyun Peng,
Jiannan Guan, Peng Wang, Mengkang Hu, Yuhang
Zhou, Te Gao, and Wanxiang Che. 2025. [Towards](https://arxiv.org/pdf/2503.09567)
reasoning era: A survey of long chain-of-thought
[for reasoning large language models.](https://arxiv.org/pdf/2503.09567) _arXiv preprint_
_arXiv:2503.09567_ .


Peter Clark, Isaac Cowhey, Oren Etzioni, Tushar Khot,
Ashish Sabharwal, Carissa Schoenick, and Oyvind
Tafjord. 2018. Think you have solved question
answering? try arc, the ai2 reasoning challenge.
_Preprint_, arXiv:1803.05457.


Karl Cobbe, Vineet Kosaraju, Mohammad Bavarian,
Mark Chen, Heewoo Jun, Lukasz Kaiser, Matthias
Plappert, Jerry Tworek, Jacob Hilton, Reiichiro
Nakano, and 1 others. 2021. Training verifiers
to solve math word problems. _arXiv_ _preprint_
_arXiv:2110.14168_ .


Gongfan Fang, Xinyin Ma, and Xinchao Wang. 2025.

Thinkless: [LLM learns when to think.](https://openreview.net/forum?id=ariVQf0KZx) In _The Thirty-_
_ninth Annual Conference on Neural Information Pro-_
_cessing Systems_ .


Mehdi Fatemi, Banafsheh Rafiee, Mingjie Tang, and
Kartik Talamadupula. 2025. Concise reasoning via [reinforcement](https://arxiv.org/pdf/2504.05185) learning. _arXiv_ _preprint_
_arXiv:2504.05185_ .


Sicheng Feng, Gongfan Fang, Xinyin Ma, and Xinchao
Wang. 2025. [Efficient reasoning models:](https://openreview.net/forum?id=sySqlxj8EB) A survey.
_Transactions on Machine Learning Research_ .


Yichao Fu, Junda Chen, Yonghao Zhuang, Zheyu Fu,
Ion Stoica, and Hao Zhang. 2025. [Reasoning without](https://openreview.net/forum?id=wpK4IMJfdX)
self-doubt: [More efficient chain-of-thought through](https://openreview.net/forum?id=wpK4IMJfdX)
[certainty probing.](https://openreview.net/forum?id=wpK4IMJfdX) In _ICLR 2025 Workshop on Foun-_
_dation Models in the Wild_ .


Bofei Gao, Feifan Song, Zhe Yang, Zefan Cai, Yibo
Miao, Qingxiu Dong, Lei Li, Chenghao Ma, Liang
Chen, Runxin Xu, and 1 others. 2024. Omnimath: A universal olympiad level mathematic benchmark for large language models. _arXiv_ _preprint_
_arXiv:2410.07985_ .


Daya Guo, Dejian Yang, Haowei Zhang, Junxiao
Song, Ruoyu Zhang, Runxin Xu, Qihao Zhu, Shirong Ma, Peiyi Wang, Xiao Bi, and 1 others. 2025.



Deepseek-r1: [Incentivizing reasoning capability in](https://arxiv.org/pdf/2501.12948)
llms via [reinforcement](https://arxiv.org/pdf/2501.12948) learning. _arXiv_ _preprint_
_arXiv:2501.12948_ .


Dan Hendrycks, Collin Burns, Saurav Kadavath, Akul
Arora, Steven Basart, Eric Tang, Dawn Song, and
Jacob Steinhardt. 2021. Measuring [mathematical](https://openreview.net/forum?id=7Bywt2mQsCe)
[problem solving with the MATH dataset.](https://openreview.net/forum?id=7Bywt2mQsCe) In _Thirty-_
_fifth Conference on Neural Information Processing_
_Systems Datasets and Benchmarks Track (Round 2)_ .


Edward J Hu, yelong shen, Phillip Wallis, Zeyuan AllenZhu, Yuanzhi Li, Shean Wang, Lu Wang, and Weizhu
Chen. 2022. LoRA: Low-rank [adaptation](https://openreview.net/forum?id=nZeVKeeFYf9) of large
[language](https://openreview.net/forum?id=nZeVKeeFYf9) models. In _International_ _Conference_ _on_
_Learning Representations_ .


James Y. Huang, Sailik Sengupta, Daniele Bonadiman,
Yi-An Lai, Arshit Gupta, Nikolaos Pappas, Saab Mansour, Katrin Kirchhoff, and Dan Roth. 2025. [DeAL:](https://doi.org/10.18653/v1/2025.acl-long.1274)
[Decoding-time alignment for large language models.](https://doi.org/10.18653/v1/2025.acl-long.1274)
In _Proceedings_ _of_ _the_ _63rd_ _Annual_ _Meeting_ _of_ _the_
_Association for Computational Linguistics (Volume 1:_
_Long Papers)_, pages 26280–26300, Vienna, Austria.
Association for Computational Linguistics.


Yue Huang, Jiawen Shi, Yuan Li, Chenrui Fan, Siyuan
Wu, Qihui Zhang, Yixin Liu, Pan Zhou, Yao Wan,
Neil Zhenqiang Gong, and Lichao Sun. 2024. [Meta-](https://openreview.net/forum?id=R0c2qtalgG)
[tool benchmark for large language models:](https://openreview.net/forum?id=R0c2qtalgG) Deciding
[whether to use tools and which to use.](https://openreview.net/forum?id=R0c2qtalgG) In _The Twelfth_
_International_ _Conference_ _on_ _Learning_ _Representa-_
_tions_ .


Guochao Jiang, Guofeng Quan, Zepeng Ding, Ziqin
Luo, Dixuan Wang, and Zheng Hu. 2025. [Flashthink:](https://arxiv.org/pdf/2505.13949)
[An early exit method for efficient reasoning.](https://arxiv.org/pdf/2505.13949) _arXiv_
_preprint arXiv:2505.13949_ .


Yu Kang, Xianghui Sun, Liangyu Chen, and Wei Zou.
2025. C3ot: Generating [shorter](https://arxiv.org/pdf/2412.11664) chain-of-thought
[without compromising effectiveness.](https://arxiv.org/pdf/2412.11664) In _Proceedings_
_of the AAAI Conference on Artificial Intelligence_ .


Tomasz Korbak, Hady Elsahar, Germán Kruszewski,
and Marc Dymetman. 2022. [On reinforcement learn-](https://arxiv.org/pdf/2206.00761)
ing and distribution [matching](https://arxiv.org/pdf/2206.00761) for fine-tuning language models with no catastrophic forgetting. _Ad-_
_vances_ _in_ _Neural_ _Information_ _Processing_ _Systems_,
35:16203–16220.


Yassir Laaouach. 2025. HALT-cot: [Model-agnostic](https://openreview.net/pdf?id=CX5c7C1CZa)
early stopping for [chain-of-thought](https://openreview.net/pdf?id=CX5c7C1CZa) reasoning via
answer entropy. In _4th_ _Muslims_ _in_ _ML_ _Workshop_
_co-located with ICML 2025_ .


Gengyang Li, Yifeng Gao, Yuming Li, and Yunfang Wu.
2025. Thinkless: [A training-free inference-efficient](https://arxiv.org/pdf/2505.15684)
method for reducing [reasoning](https://arxiv.org/pdf/2505.15684) redundancy. _arXiv_
_preprint arXiv:2505.15684_ .


Alisa Liu, Xiaochuang Han, Yizhong Wang, Yulia
Tsvetkov, Yejin Choi, and Noah A. Smith. 2024a.
[Tuning language models by proxy.](https://openreview.net/forum?id=dribhnhm1i) In _First Confer-_
_ence on Language Modeling_ .


Alisa Liu, Maarten Sap, Ximing Lu, Swabha
Swayamdipta, Chandra Bhagavatula, Noah A. Smith,
and Yejin Choi. 2021. [DExperts: Decoding-time con-](https://doi.org/10.18653/v1/2021.acl-long.522)
[trolled text generation with experts and anti-experts.](https://doi.org/10.18653/v1/2021.acl-long.522)
In _Proceedings_ _of_ _the_ _59th_ _Annual_ _Meeting_ _of_ _the_
_Association_ _for_ _Computational_ _Linguistics_ _and_ _the_
_11th International Joint Conference on Natural Lan-_
_guage Processing (Volume 1:_ _Long Papers)_, pages
6691–6706, Online. Association for Computational
Linguistics.


Tianlin Liu, Shangmin Guo, Leonardo Bianco, Daniele
Calandriello, Quentin Berthet, Felipe Llinares-López,
Jessica Hoffmann, Lucas Dixon, Michal Valko, and
Mathieu Blondel. 2024b. [Decoding-time](https://openreview.net/forum?id=n8g6WMxt09) realign[ment of language models.](https://openreview.net/forum?id=n8g6WMxt09) In _Forty-first International_
_Conference on Machine Learning_ .


Xin Liu and Lu Wang. 2025. [Answer convergence as](https://doi.org/10.18653/v1/2025.emnlp-main.904)
[a signal for early stopping in reasoning.](https://doi.org/10.18653/v1/2025.emnlp-main.904) In _Proceed-_
_ings of the 2025 Conference on Empirical Methods in_
_Natural Language Processing_, pages 17907–17918,
Suzhou, China. Association for Computational Linguistics.


Minjia Mao, Bowen Yin, Yu Zhu, and Xiao Fang. 2025.

[Early stopping chain-of-thoughts in large language](https://arxiv.org/pdf/2509.14004)
[models.](https://arxiv.org/pdf/2509.14004) _arXiv preprint arXiv:2509.14004_ .


Eric Mitchell, Rafael Rafailov, Archit Sharma, Chelsea
Finn, and Christopher D Manning. 2024. An emulator for fine-tuning [large](https://openreview.net/forum?id=Eo7kv0sllr) language models using
[small language models.](https://openreview.net/forum?id=Eo7kv0sllr) In _The Twelfth International_
_Conference on Learning Representations_ .


OpenAI. 2024. [Learning to reason with llms.](https://openai.com/index/learning-to-reason-with-llms) Associated Press (AP).


Shishir G Patil, Huanzhi Mao, Fanjia Yan, Charlie Cheng-Jie Ji, Vishnu Suresh, Ion Stoica, and
Joseph E. Gonzalez. 2025. The [berkeley](https://openreview.net/forum?id=2GmDdhBdDk) function
[calling leaderboard (BFCL): From tool use to agentic](https://openreview.net/forum?id=2GmDdhBdDk)
[evaluation of large language models.](https://openreview.net/forum?id=2GmDdhBdDk) In _Forty-second_
_International Conference on Machine Learning_ .


Rafael Rafailov, Archit Sharma, Eric Mitchell, Christopher D Manning, Stefano Ermon, and Chelsea Finn.
2023. [Direct preference optimization:](https://arxiv.org/pdf/2305.18290) Your language
[model is secretly a reward model.](https://arxiv.org/pdf/2305.18290) _Advances in neural_
_information processing systems_, 36:53728–53741.


David Rein, Betty Li Hou, Asa Cooper Stickland, Jackson Petty, Richard Yuanzhe Pang, Julien Dirani, Julian Michael, and Samuel R. Bowman. 2024. [GPQA:](https://openreview.net/forum?id=Ti67584b98)
[A graduate-level google-proof q&a benchmark.](https://openreview.net/forum?id=Ti67584b98) In
_First Conference on Language Modeling_ .


Mingyang Song and Mao Zheng. 2025. Walk [before](https://arxiv.org/pdf/2505.21178)
you run! concise llm [reasoning](https://arxiv.org/pdf/2505.21178) via reinforcement
[learning.](https://arxiv.org/pdf/2505.21178) _arXiv preprint arXiv:2505.21178_ .


Guangya Wan, Yuqi Wu, Jie Chen, and Sheng Li. 2025.

[Reasoning aware self-consistency:](https://doi.org/10.18653/v1/2025.naacl-long.184) Leveraging reasoning paths for [efficient](https://doi.org/10.18653/v1/2025.naacl-long.184) LLM sampling. In _Pro-_
_ceedings_ _of_ _the_ _2025_ _Conference_ _of_ _the_ _Nations_ _of_



_the_ _Americas_ _Chapter_ _of_ _the_ _Association_ _for_ _Com-_
_putational Linguistics:_ _Human Language Technolo-_
_gies_ _(Volume_ _1:_ _Long_ _Papers)_, pages 3613–3635,
Albuquerque, New Mexico. Association for Computational Linguistics.


Chenlong Wang, Yuanning Feng, Dongping Chen,
Zhaoyang Chu, Ranjay Krishna, and Tianyi Zhou.
2025. Wait, we don’t need to “wait”! removing
thinking tokens [improves](https://doi.org/10.18653/v1/2025.findings-emnlp.394) reasoning efficiency. In
_Findings of the Association for Computational Lin-_
_guistics:_ _EMNLP 2025_, pages 7459–7482, Suzhou,
China. Association for Computational Linguistics.


Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten
Bosma, brian ichter, Fei Xia, Ed H. Chi, Quoc V Le,
and Denny Zhou. 2022. Chain of [thought](https://openreview.net/forum?id=_VjQlMeSB_J) prompting elicits reasoning in large language models. In
_Advances in Neural Information Processing Systems_ .


Fengli Xu, Qianyue Hao, Zefang Zong, Jingwei Wang,
Yunke Zhang, Jingyi Wang, Xiaochong Lan, Jiahui
Gong, Tianjian Ouyang, Fanjin Meng, and 1 others.
2025. Towards large [reasoning](https://arxiv.org/pdf/2501.09686) models: A survey
[of reinforced reasoning with large language models.](https://arxiv.org/pdf/2501.09686)
_arXiv preprint arXiv:2501.09686_ .


An Yang, Anfeng Li, Baosong Yang, Beichen Zhang,
Binyuan Hui, Bo Zheng, Bowen Yu, Chang
Gao, Chengen Huang, Chenxu Lv, and 1 others.
2025. Qwen3 [technical](https://arxiv.org/pdf/2505.09388) report. _arXiv_ _preprint_
_arXiv:2505.09388_ .


Chenxu Yang, Qingyi Si, Yongjie Duan, Zheliang Zhu,
Chenyu Zhu, Qiaowei Li, Minghui Chen, Zheng Lin,
and Weiping Wang. 2026. Dynamic [early](https://openreview.net/forum?id=NpU7ZXafRi) exit in
[reasoning models.](https://openreview.net/forum?id=NpU7ZXafRi) In _The Fourteenth International_
_Conference on Learning Representations_ .


Qiying Yu, Zheng Zhang, Ruofei Zhu, Yufeng Yuan, Xiaochen Zuo, YuYue, Weinan Dai, Tiantian Fan, Gaohong Liu, Juncai Liu, LingJun Liu, Xin Liu, Haibin
Lin, Zhiqi Lin, Bole Ma, Guangming Sheng, Yuxuan
Tong, Chi Zhang, Mofan Zhang, and 17 others. 2025.
[DAPO: An open-source LLM reinforcement learning](https://openreview.net/forum?id=2a36EMSSTp)
[system at scale.](https://openreview.net/forum?id=2a36EMSSTp) In _The Thirty-ninth Annual Confer-_
_ence on Neural Information Processing Systems_ .


Xuechen Zhang, Zijian Huang, Chenshun Ni, Ziyang
Xiong, Jiasi Chen, and Samet Oymak. 2025a. [Mak-](https://openreview.net/forum?id=tZBhvKaLUJ)
[ing small language models efficient reasoners:](https://openreview.net/forum?id=tZBhvKaLUJ) Inter[vention, supervision, reinforcement.](https://openreview.net/forum?id=tZBhvKaLUJ) In _ICML 2025_
_Workshop on Long-Context Foundation Models_ .


Yunxiang Zhang, Muhammad Khalifa, Lechen Zhang,
Xin Liu, Ayoung Lee, Xinliang Frederick Zhang,
Farima Fatahi Bayat, and Lu Wang. 2025b. [Logit](https://arxiv.org/pdf/2510.09354)
[arithmetic elicits long reasoning capabilities without](https://arxiv.org/pdf/2510.09354)
[training.](https://arxiv.org/pdf/2510.09354) _arXiv preprint arXiv:2510.09354_ .


**A** **Usage of Large Language Models**


Large language models were used for literature
search, coding assistance, and proofreading only.
They were not used for ideation, results, or analysis;
all contributions and conclusions are the authors’.


**B** **Example of Overthinking**


Tables 10 and 11 present a BFCL example and the
corresponding LRM response. Green highlights
mark points at which terminating would yield a
correct answer, whereas red highlights indicate an
incorrect one. Notably, the model’s reasoning turns
red after a certain point, illustrating overthinking.


**C** **Experiment Details**


We use NVIDIA H200 GPU for all inference and
training, with a fixed seed of 42.


**C.1** **Model Details**


The official Huggingface names for the models we
used are as follows in Table 5.


**Our Name** **Hf Model Id**


Qwen3-4B-Thinking Qwen/Qwen3-4B-Thinking
-2507
Qwen3-4B Qwen/Qwen3-4B
Qwen3-14B Qwen/Qwen3-14B
Qwen3-32B Qwen/Qwen3-32B
DeepSeek-R1-7B deepseek-ai/DeepSeekR1-Distill-Qwen-7B
Phi-4-Reasoning microsoft/Phi-4-reasoning
Qwen3-Next-80B Qwen/Qwen3-Next-80B
-A3B-Thinking


Table 5: Model names and Huggingface identifiers.


**C.2** **Inference Details**


For all inference tasks, we use the following hyperparameters following the official guidelines for
each model (Yang et al., 2025; Abdin et al., 2025;
Guo et al., 2025). For Qwen3-4B-Thinking, we extend the reasoning budget to 32k for AIME benchmarks only.


**C.3** **Training on THINKBRAKE**


This section describes the experimental details for
§4. To curate a training dataset, we sampled _∼_ 1.3K
examples from Omni-MATH, with the preferred responses generated using THINKBRAKE and dispreferred responses generated without THINKBRAKE.
We applied the following filtering criteria: (1) when
both methods produce correct answers, we only include examples where the baseline token length



**Parameter** **DeepSeek** **Qwen3** **Phi-4**


THINKBRAKE- _τ_ 0.1 0.1 2.5


_Sampling Parameters_


Temperature 0.6 0.6 0.8
Top-p 1 0.95 0.95
Top-k    - 20 50


_Token Budgets_


Reasoning Budget 16384 16384 16384
Answer Budget 4096 4096 4096


Table 6: Inference hyperparameters for different models.


exceeds the THINKBRAKE token length, demonstrating efficiency gains; (2) when THINKBRAKE
produces correct answers but the baseline fails, we
include all such examples; (3) all other cases are
excluded from the training set. This curation process ensures that our training data emphasizes both
correctness improvements and computational efficiency.
We performed Direct Preference Optimization
(DPO; Rafailov et al., 2023) using the hyperparameters listed in Table 7. Training was conducted with
LoRA (Hu et al., 2022) for parameter-efficient finetuning in around 20 minutes of wall-clock time.


**Hyperparameter** **Value**


Learning Rate 2 _×_ 10 _[−]_ [5]

Batch Size (per device) 8
Gradient Accumulation Steps 4
Effective Batch Size 64
Number of GPUs 2 _×_ H200
Training Epochs 10
LoRA Rank ( _r_ ) 32
LoRA Alpha ( _α_ ) 32
Training Samples 1,348


Table 7: Training hyperparameters for DPO.


**C.4** **System Prompts**


Following the official guides (Abdin et al., 2025;
Guo et al., 2025; Yang et al., 2025) we use the
following prompts in Figures 9, 10, 11 and 12 for
our experiments.


**C.5** **Baseline Methods**


This section describes the details on the baseline
methods:


**NoWait** (Wang et al., 2025): removes delay/filler
tokens (e.g., “wait”, “hmm”) during decoding to
stop overthinking and allow for earlier termination.
We use the following list in Table 8 for NoWait.


**Keywords**


wait, hmm, hmmm, but, however, check, verify, alternatively


Table 8: Keyword list for NoWait.


**ThinkLess** (Li et al., 2025): forces immediate termination by emitting </think> right after the initial <think>, minimizing the thinking process to
two special tokens: <think></think>.


**Dynasor-CoT** (Fu et al., 2025): injects probing
prompts at regular intervals to extract intermediate
answers, terminating reasoning early if those answers demonstrate consistency across consecutive
steps.


**DEER** (Yang et al., 2026): monitors the model’s
reasoning for linguistic transition markers (e.g.,
‘Wait’, ‘Alternatively’), temporarily interrupts the
process at these points to induce a trial answer,
and evaluates the model’s internal probability confidence in that answer—exiting to output it if the
confidence threshold is met, or discarding it and
resuming the chain of thought if it is not.


**C.6** **Hyperparameter Selection**


Figures 6 and 7 show the hyperparameter search
for additional models.


DeepSeek-R1-7B



|Log Mar<br>ln(P)|gin (High P)<br>0.288 <|Col3|Col4|Col5|
|---|---|---|---|---|
|||||P(Top)|
||P(Top) = 0.2<br>P(</thin<br> gin (Low P)<br>|P(Top) = 0.2<br>P(</thin<br> gin (Low P)<br>|P(Top) = 0.2<br>P(</thin<br> gin (Low P)<br>|P(Top) = 0.2<br>P(</thin<br> gin (Low P)<br>|
||P(Top) = 0.2<br>P(</thin<br> gin (Low P)<br>|P(</thin|k>) = 0.3|k>) = 0.3|
|Log Mar<br>|Log Mar<br>|Log Mar<br>|Log Mar<br>|Log Mar<br>|
|~~ln(P)~~|nk>) = 0.1<br>~~ 0.693 >~~|nk>) = 0.1<br>~~ 0.693 >~~|||
|P(</thi|P(</thi|P(</thi|P(</thi|P(</thi|
||Raw Gap = 0.1|Raw Gap = 0.1|||
||Raw Gap = 0.1|Raw Gap = 0.1|Raw Gap = 0.1|Raw Gap = 0.1|
||Raw Gap = 0.1|Raw Gap = 0.1|||
|~~0~~|~~0~~|~~0~~|~~0~~|~~0~~|


Figure 8: Log-probability plot with two illustrative
cases, ∆P1 and ∆P2. Here, ∆P1 denotes a scenario
where the most likely token has high probability (0.4),
and ∆P2 denotes a scenario where the most likely token
has lower probability (0.2), while the raw gap is the
same (i.e., ∆P1 = ∆P2).


**Entropy** **State.** Table 9 shows the ratio of
</think> in the top 20 tokens and median entropy
for the log-probability setting (THINKBRAKE)
and the raw-probability variant (THINKBRAKE-p).
THINKBRAKE terminates almost exclusively in



40


30


20


10


0



Phi-4-Reasoning


Baseline 0.1 0.25 1.0 2.5 10.0 25.0
Threshold



100


80


60


40


20


0



Figure 7: _τ_ search from error rate and thinking token
usage for THINKBRAKE on Phi-4-Reasoning.


**D** **Why Log-Space Margins Are Robust**


As shown in Tables 14, 15 and §4.2, linear probability gaps are insufficient for THINKBRAKE. A
meaningful log-probability gap only arises when
both competing probabilities are relatively high
(see Figure 8), indicating that the model is genuinely confident at that step. If we used a linear probability gap, both ∆P1 and ∆P2 would
trigger early termination; in contrast, using a logprobability gap triggers only for ∆P1—where both
the top token and </think> have high probabilities—signaling confidence in stopping the reasoning.


Logarithm Sensitivity: Log Prob Margin vs Raw Probability Gap

0





1


2


3





60


50


40


30


20


10


0



Baseline 0.1 0.25 1.0 2.5 10.0 25.0
Threshold



100


80


60


40


20


0



Figure 6: _τ_ search from error rate and thinking token
usage for THINKBRAKE on DeepSeek-R1-7B.


low-entropy states and only when </think> ranks
within the top 20 tokens, while the raw-probability
variant (THINKBRAKE-p) frequently triggers in
high-entropy states even when </think> is not in
the top 20, confirming that the log design is robust
precisely where the raw-probability design is more
sensitive.


Category Method Ratio in Top-20 Median Entropy


THINKBRAKE 99.9% 0.018
Math
THINKBRAKE-p 66.6% 0.264


THINKBRAKE 100.0% 0.036
Science
THINKBRAKE-p 65.3% 0.458


Table 9: Entropy and top-20 ratio results on Qwen3-4BThinking across math and science benchmarks.


**E** **Extensive Results**


In this section, we provide extensive results across
all benchmarks, models, and hyperparameter combinations.


**Token Count.** Table 13 shows the average token
count per base model and benchmark. We consistently observe that difficult tasks such as AIME and
GPQA-D require larger token budgets.


**Full** **Tables.** Tables 14 and 15 present extensive results from the experiments in §4. Specifically, Table 14 shows the full results including
all baseline methods across all models. Table 15
shows the complete results for BFCL-v1, BFCLv2 (including Simple and Multiple function categories), and Meta-Tool benchmarks. We observe
that THINKBRAKE achieves a better performancetoken reduction tradeoff overall. Furthermore, Table 16 reports the variances and 95% confidence
intervals (CIs) for accuracy and token counts on the
AIME benchmarks, computed over 32 independent
runs. Notably, THINKBRAKE’s token consumption
falls entirely below the baseline’s CI, confirming
a statistically meaningful reduction in reasoning
length.


**Token** **Reduction** **and** **Model** **Size.** Table 17
shows that larger models tend to produce shorter
reasoning traces and there is less redundant thinking to prune. Qwen3-Next-80B, despite being
larger, produces substantially longer traces than
Qwen3-32B, and correspondingly yields larger token reductions. We suggest that token reduction
rate depends on the reasoning trace length rather
than model size.



**Premature** **Exiting** **and** **Spurious** **Reasoning.**
To investigate the performance degradation associated with THINKBRAKE, we analyzed the perproblem token counts of THINKBRAKE versus an
oracle setting on the highly challenging AIME
benchmarks. Table 18 reveals that among the 16
instances where THINKBRAKE failed but the oracle succeeded, THINKBRAKE exited prior to the
oracle in only 2 cases. This indicates that premature termination is not the primary reason for
incorrect answers. Instead, errors appear to stem
from subsequent spurious reasoning that misleads
the LRMs. A detailed example is shown in Table 19, where the model successfully solves the
problem but then engages in flawed reasoning before THINKBRAKE finally terminates generation.
We hypothesize that highly verbose models, such as
Qwen3-4B-Thinking (which produces the longest
average reasoning traces), are especially vulnerable
to this type of reasoning degradation.


_τ_ **Ablation.** Figures 13, 14, 15, and 16 show
extensive results across various threshold values
_τ_ _∈{_ 0 _._ 1 _,_ 0 _._ 25 _,_ 1 _._ 0 _,_ 2 _._ 5 _}_ . The first two figures display token reduction percentage compared to the
base model, while the latter two show accuracy
comparison across various _τ_ values. We observe
that larger _τ_ values result in greater token reduction, and accuracy is maintained across various _τ_
settings.


**Transition** **Matrix.** Figure 17 shows the transition matrices for all models (aggregated across
all benchmarks), illustrating model behavior before and after applying THINKBRAKE. The matrices show high values along the diagonal (top-left
and bottom-right), indicating that THINKBRAKE
preserves accuracy without introducing significant
changes to correct or incorrect predictions.


**Question**


Find the area and perimeter of a circle with a radius of 5 and also find the circumference of a circle
with diameter of 10.


**Prompt**


system:
# Tools
You may call one or more functions to assist with the user query.
You are provided with function signatures within <tools> XML tags:
<tools>
{ "name": "circle.calculate_circumference",
"description": "Calculate the circumference of a circle based on the diameter.",
"parameters": {
"type": "dict",
"properties": {
"diameter": { "type": "integer", "description": "The diameter of the circle." }
},
"required": ["diameter"]
}
},
{ "name": "circle.calculate_area",
"description": "Calculate the area of a circle based on the radius.",
"parameters": {
"type": "dict",
"properties": {
"radius": { "type": "integer", "description": "The radius of the circle." }
},
"required": ["radius"]
}
},
{ "name": "rectangle.calculate_perimeter",
"description": "Calculate the perimeter of a rectangle based on the length and breadth.",
"parameters": {
"type": "dict",
"properties": {
"length": { "type": "integer", "description": "The length of the rectangle." },
"breadth": { "type": "integer", "description": "The breadth of the rectangle." }
},
"required": ["length", "breadth"]
}
}
</tools>
For each function call, return a json object with function name and arguments within <tool_call>
XML tags:
<tool_call>
{ "name": <function-name>, "arguments": <args-json-object> }
</tool_call>
user: The above geometry question.


Table 10: Full question and prompt.


<think>

Okay, let’s tackle this problem. The user wants the area and perimeter of a circle with radius 5, and the
circumference of a circle with diameter 10.
First, I need to check which tools are available.
There’s circle.calculate_area which takes radius, and rectangle.calculate_perimeter but wait, the user is
asking for the perimeter of a circle? Wait, no.
Wait, the problem says "area and perimeter of a circle".
Wait, circles don’t have perimeters; they have circumferences.

Maybe the user made a mistake here.
Let me read again.
The user says: "Find the area and perimeter of a circle with a radius of 5 and also find the circumference
of a circle with diameter of 10."
Hmm, perimeter for a circle is called circumference.
So maybe the user is confused.
But according to the tools provided, there’s circle.calculate_circumference (for diameter),
circle.calculate_area (for radius), and rectangle.calculate_perimeter (for length and breadth).
Wait, the user is asking for perimeter of a circle.

But the tools don’t have a circle perimeter function.
Wait, the rectangle function is for perimeter of a rectangle, which is different.

So maybe the user intended to say circumference for the circle’s perimeter.

...
Because perimeter is a term for 2D shapes, but for circles it’s circumference.
Assuming that the user wants:

- Area of radius 5 circle: call calculate_area with radius=5.

- Circumference of radius 5 circle (which they called perimeter): but since the tool requires diameter, we
can compute diameter as 10 (since radius is 5), so call calculate_circumference with diameter=10.

- Also, circumference with diameter 10: call calculate_circumference with diameter=10.

...
So three tool calls? Or is the perimeter part a mistake and the user just meant circumference?
Wait, the rectangle.calculate_perimeter is for rectangles, so that’s not relevant here.
The user is talking about circles, so we ignore the rectangle tool.
So, the correct tool calls are:
1. circle.calculate_area(radius=5)

2. circle.calculate_circumference(diameter=10)
3. circle.calculate_circumference(diameter=10)
But in reality, the user is asking for two separate values: perimeter (which is circumference) for radius 5
(diameter 10) and circumference for diameter 10.
So they are the same calculation, but the user is asking for it twice.

...

- For the perimeter of radius 5 circle: since perimeter of a circle is circumference, which is calculated via
diameter.
So diameter is .


Table 11: Qwen3-4B thinking trajectory.


Figure 9: Prompt template for Qwen3 on mathematical
reasoning tasks. Similar to DeepSeek, the model provides reasoning within think tags before the final boxed
answer.



Figure 11: Prompt template for DeepSeek on mathematical reasoning tasks. The model is instructed to provide
step-by-step reasoning within think tags, followed by
the final answer in boxed notation.





Figure 10: Prompt template for Qwen3 on general
multiple-choice reasoning tasks. The model is instructed
to format its final answer as a single choice letter.





Figure 12: Prompt template for Phi-4-Reasoning with
comprehensive system instructions. The model is
guided to use a systematic thinking process with explicit thought and solution sections.


**(a) Math** GSM8K MATH500 AIME2024 AIME2025 Avg.


Method Acc ∆Tok Acc ∆Tok Acc ∆Tok Acc ∆Tok Acc ∆Tok


Base 95.1  - 95.3  - 77.1  - 76.2  - 86.0  Oracle 97.8 -69.1% 99.8 -60.0% 86.7 -41.6% 93.3 -45.5% 94.4 -54.1%


_Avg._ _Base Token_ _1,578_ _6,360_ _19,294_ _21,317_ _12,137_


**(b) Tool** simple multiple parallel multi-parallel Avg.


Method Acc ∆Tok Acc ∆Tok Acc ∆Tok Acc ∆Tok Acc ∆Tok


Base 88.2  - 90.5  - 93.5  - 90.5  - 90.7  Oracle 91.5 -81.3% 98.5 -93.6% 96.0 -89.7% 95.5 -90.1% 95.4 -88.7%


_Avg._ _Base Token_ _1,155_ _985_ _1,200_ _1,621_ _1,240_


Table 12: Accuracy (%) and ∆Tok (token reduction, %) on Math and Tool benchmarks. The results represent
performance under oracle </think> stopping compared to the base Qwen3-4B-Thinking model.


Model GSM8K MATH500 AIME 2024 AIME 2025 GPQA-D ARC-C


Qwen3-4B-Thinking 1,578 6,360 19,294 21,317 8,455 1,178
Qwen3-4B 2,407 5,250 13,000 15,163 7,497 798
Qwen3-14B 1,912 4,938 12,807 14,198 7,379 621
Qwen3-32B 1,794 4,650 12,278 13,727 6,626 726
DeepSeek-R1-7B 1,674 4,062 12,146 12,476 7,097 770
Phi-4-Reasoning 1,332 2,664 9,616 10,599 7,896 1,360
Qwen3-Next-80B 1,169 4,547 15,538 16,976 8,025 807


BFCL-v1 BFCL-v2 Meta-Tool


Model Simple Multiple Parallel Multi-Par. Simple Multiple Parallel Multi-Par. Single Multiple


Qwen3-4B-Thinking 1,072 965 1,199 1,621 1,094 1,832 1,473 2,397 1,946 1,336
Qwen3-4B 607 744 844 1,046 653 1,426 837 1,555 1,069 856
Qwen3-14B 545 725 834 975 612 1,372 944 1,470 1,091 873
Qwen3-32B 553 750 826 991 617 1,342 725 1,572 1,048 857
DeepSeek-R1-7B 669 959 815 1,152 743 1,702 816 1,623 1,144 1,187
Phi-4-Reasoning 1,259 1,480 1,574 2,050 1,641 2,582 1,692 2,607 2,104 1,966


Table 13: Average token counts for base models across all datasets and models.


GSM8K MATH500 AIME2024 AIME2025 GPQA-D ARC-C Avg.


Model Acc ∆Tok Acc ∆Tok Acc ∆Tok Acc ∆Tok Acc ∆Tok Acc ∆Tok Acc ∆Tok


Qwen3-4B-Thinking 95.1 - 95.3 - 77.1 - 76.2 - 64.1 - 94.3 - 83.7 + NoWait 94.2 -25.1% 96.4 -17.9% 66.7 -30.5% 66.7 -35.6% 68.2 -19.6% 92.7 14.6% 80.8 -19.0%
+ ThinkLess 92.6 -100% 56.4 -100% 3.3 -100% 3.3 -100% 50.0 -100% 94.2 -100% 50.0 -100%
+ DEER 95.1 -34.1% 94.4 -14.2% 63.3 -34.3% 60.0 -37.9% 68.2 -1.3% 92.8 -9.0% 79.0 -21.8%
+ Dynasor-CoT 95.2 -34.0% 87.2 -42.1% 63.3 -28.8% 53.3 -28.9% 62.6 -22.6% 94.5 -39.1% 76.0 -23.0%
+ THINKBRAKE-p 93.9 -37.3% 91.2 -57.9% 35.0 -72.6% 30.4 -76.0% 47.0 -67.5% 93.7 -31.7% 65.2 -57.2%
+ THINKBRAKE 94.8 -18.9% 96.6 -20.4% 67.2 -33.5% 62.8 -33.4% 62.6 -32.7% 94.0 -19.9% 79.7 -26.5%


Qwen3-4B 94.4 - 96.0 - 68.8 - 59.6 - 51.0 - 94.0 - 77.3 + NoWait 94.5 -40.4% 94.6 -31.4% 56.7 -16.6% 50.0 -27.1% 57.6 -26.6% 93.4 -14.4% 74.5 -26.1%
+ ThinkLess 91.0 -100% 85.4 -100% 23.3 -100% 23.3 -100% 46.0 -100% 89.3 -100% 59.7 -100%
+ THINKBRAKE-p 92.8 -40.2% 88.6 -51.3% 29.2 -64.5% 25.0 -67.8% 47.5 -54.2% 93.4 -15.0% 62.8 -48.8%
+ THINKBRAKE 94.5 -30.1% 95.4 -14.4% 64.6 -12.7% 60.4 -13.5% 55.6 -29.7% 93.9 -11.5% 77.4 -18.7%


Qwen3-14B 96.0 - 96.8 - 71.7 - 69.2 - 60.6 - 95.9 - 81.7 + NoWait 95.8 -29.4% 95.2 -25.1% 70.0 -19.8% 56.7 -16.6% 62.1 -20.5% 96.2 -8.1% 79.3 -19.9%
+ ThinkLess 93.4 -100% 86.8 -100% 23.3 -100% 30.0 -100% 49.5 -100% 94.3 -100% 62.9 -100%
+ THINKBRAKE-p 95.1 -31.6% 89.0 -49.8% 38.8 -68% 26.2 -72% 57.6 -66.4% 94.7 -17.9% 66.9 -51%
+ THINKBRAKE 95.0 -15.4% 96.9 -7.7% 77.9 -7.4% 65.8 -6.0% 61.1 -39.9% 95.2 -18.2% 82.0 -15.8%


Qwen3-32B 96.0 - 97.0 - 75.8 - 68.3 - 65.2 - 92.1 - 82.4 + NoWait 95.3 -23.6% 95.8 -20.6% 66.7 -12.0% 56.7 -10.6% 60.1 -12.4% 90.1 9.0% 77.5 -11.7%
+ ThinkLess 93.3 -100% 87.6 -100% 23.3 -100% 20.0 -100% 54.5 -100% 95.1 -100% 62.3 -100%
+ THINKBRAKE-p 94.8 -23.0% 89.6 -39.4% 39.2 -61.5% 26.7 -66.4% 53.5 -51.0% 92.2 -11.7% 66.0 -42.2%
+ THINKBRAKE 96.5 -9.1% 97.2 -1.4% 77.1 -6.2% 68.3 -4.3% 65.7 -19.9% 91.0 -8.0% 82.6 -8.2%


DeepSeek-R1-7B 92.7 - 93.8 - 49.5 - 37.6 - 48.0 - 67.7 - 64.9 + NoWait 90.6 -30.8% 91.2 -31.0% 40.0 -32.4% 26.7 -36.5% 43.4 -35.5% 64.6 -12.6% 59.4 -29.8%
+ ThinkLess 85.9 -100% 78.4 -100% 16.7 -100% 20.0 -100% 30.3 -100% 50.4 -100% 47.0 -100%
+ DEER 89.0 -60.5% 87.2 -44.5% 50.0 -28.2% 33.3 -9.8% 43.9 -16.7% 73.9 -10.6% 62.9 -28.3%
+ Dynasor-CoT 61.3 -87.8% 64.2 -47.2% 33.4 -31.8% 33.4 -26.4% 32.3 -71.2% 77.8 -53.6% 50.4 -53.0%
+ THINKBRAKE-p 87.8 -54.9% 81.4 -60.6% 25.4 -71.4% 22.9 -73.5% 36.4 -76.8% 67.2 -31.0% 53.5 -61.4%
+ THINKBRAKE 92.4 -25.0% 92.0 -23.2% 45.2 -25.0% 33.2 -20.3% 45.5 -51.5% 70.7 -35.3% 63.2 -30.0%


Phi-4-Reasoning 91.7 - 71.1 - 67.5 - 63.7 - 62.6 - 80.0 - 72.8 + NoWait 92.1 -2.4% 70.8 -17.7% 63.3 -9.4% 53.3 -8.6% 63.1 -19.1% 77.6 -7.0% 70.0 -10.7%
+ ThinkLess 92.6 -100% 66.4 -100% 36.7 -100% 23.3 -100% 54.0 -100% 82.7 -100% 59.3 -100%
+ THINKBRAKE-p 91.3 -42.5% 68.8 -50.4% 39.6 -63.1% 29.2 -66.6% 59.1 -62.8% 84.2 -49.2% 62.0 -55.8%
+ THINKBRAKE 91.7 -25.6% 70.4 -17.2% 73.3 -6.4% 53.3 -5.2% 67.7 -1.1% 80.0 -25.3% 72.7 -13.5%


Qwen3-Next-80B 96.7 - 98.2 - 90.0 - 80.0 - 76.3 - 96.8 - 89.7 + THINKBRAKE 96.5 -24.3% 99.2 -21.6% 86.7 -24.3% 73.3 -16.7% 72.7 -25.6% 97.0 -21.8% 87.6 -22.3%


Table 14: Math and science results on GSM8K, MATH500, AIME24, AIME25, GPQA-D, and ARC-C. We report
accuracy and ∆Tok (thinking token reduction vs. the Base decoding) for each model. This table presents the full
comparison including all baseline methods for all models.


BFCL-v1 BFCL-v2 Meta-Tool


Model Simple Multi Parallel Multi-Par. Simple Multi Parallel Multi-Par. Single Multiple Avg.


Acc ∆Tok Acc ∆Tok Acc ∆Tok Acc ∆Tok Acc ∆Tok Acc ∆Tok Acc ∆Tok Acc ∆Tok Acc ∆Tok Acc ∆Tok Acc ∆Tok


Qwen3-4B-Thinking 88.2 - 90.5 - 93.5 - 90.5 - 79.8 - 83.4 - 87.5 - 79.2 - 69.7 - 85.5 - 84.8 + NoWait 83.6 -33.1% 88.0 -11.5% 88.5 -44.4% 88.5 -53.5% 75.6 -29.9% 80.3 -16.5% 81.3 -50.7% 75.0 -66.5% 68.9 0.1% 84.7 -11.2% 81.4 -31.7%
+ ThinkLess 86.2 -8.1% 93.0 -2.2% 79.5 -100.0% 83.0 -100.0% 81.0 -5.9% 82.9 -4.1% 37.5 -100.0% 45.8 -100.0% 67.4 -100.0% 86.5 -100.0% 74.3 -62.0%
+ THINKBRAKE-p 88.0 -40.0% 90.5 -16.7% 78.0 -26.9% 42.5 -33.4% 79.5 -34.8% 81.7 -20.4% 62.5 -28.5% 29.2 -43.8% 70.8 -25.8% 86.7 -12.7% 70.9 -28.3%
+ THINKBRAKE 87.3 -32.9% 90.0 -12.4% 95.5 -26.8% 90.5 -28.2% 82.2 -29.9% 82.9 -16.7% 87.5 -32.3% 87.5 -18.9% 72.4 -20.6% 86.3 -9.0% 86.2 -22.8%


Qwen3-4B 88.2 - 92.0 - 90.0 - 83.0 - 80.2 - 81.0 - 81.2 - 70.8 - 74.3 - 90.5 - 83.1 + NoWait 88.2 -16.3% 90.5 -1.5% 88.0 -13.5% 84.0 1.2% 78.3 -9.6% 80.0 -5.8% 75.0 -5.1% 75.0 -11.1% 72.5 -3.1% 90.5 -8.4% 82.2 -7.3%
+ ThinkLess 86.4 -100.0% 89.5 -100.0% 87.5 -100.0% 83.5 -100.0% 71.3 -100.0% 76.4 -100.0% 56.2 -100.0% 62.5 -100.0% 69.1 -100.0% 92.2 -100.0% 77.5 -100.0%
+ THINKBRAKE-p 87.3 -13.5% 93.0 -4.6% 90.5 -14.8% 84.0 -4.8% 80.2 -6.9% 81.8 -3.5% 75.0 -15.1% 75.0 -12.7% 73.5 -1.5% 90.3 -2.9% 83.1 -8.0%
+ THINKBRAKE 87.8 -12.5% 92.5 -5.2% 89.5 -16.5% 83.5 -12.0% 79.1 -9.0% 81.2 -2.9% 62.5 -21.1% 75.0 -10.2% 72.7 -1.4% 91.1 -3.0% 81.5 -9.4%


Qwen3-14B 87.8 - 93.0 - 92.0 - 83.5 - 80.6 - 81.1 - 62.5 - 70.8 - 63.3 - 84.9 - 80.0 + NoWait 87.1 -7.5% 92.0 -0.6% 90.0 -16.3% 84.0 1.8% 77.9 -7.0% 79.8 -4.9% 62.5 -30.1% 62.5 -10.9% 61.2 -2.4% 84.5 -5.8% 78.2 -8.4%
+ ThinkLess 88.4 -100.0% 87.5 -100.0% 90.0 -100.0% 87.0 -100.0% 74.4 -100.0% 77.9 -100.0% 56.2 -100.0% 50.0 -100.0% 69.7 -100.0% 83.5 -100.0% 76.5 -100.0%
+ THINKBRAKE-p 88.4 -9.4% 92.5 -2.2% 91.5 -23.5% 86.0 -16.0% 77.9 -10.1% 80.7 -5.3% 68.8 -29.9% 50.0 -14.6% 64.6 -2.1% 85.9 -4.8% 78.6 -11.8%
+ THINKBRAKE 87.8 -9.5% 92.0 -4.1% 93.0 -21.2% 85.0 -14.2% 78.3 -7.7% 79.7 -5.2% 62.5 -25.4% 62.5 -7.6% 66.3 -1.6% 85.7 -4.5% 79.3 -10.1%


Qwen3-32B 88.0 - 90.0 - 93.0 - 85.0 - 83.7 - 80.7 - 68.8 - 70.8 - 64.8 - 84.3 - 80.9 + NoWait 87.3 -7.8% 88.0 -4.0% 91.0 -13.0% 82.5 -5.0% 80.6 -6.2% 79.0 -1.6% 68.8 -3.9% 62.5 -14.3% 63.8 3.6% 83.9 1.3% 78.7 -5.1%
+ ThinkLess 89.1 -100.0% 87.5 -100.0% 91.5 -100.0% 88.0 -100.0% 77.1 -100.0% 81.3 -100.0% 68.8 -100.0% 58.3 -100.0% 72.3 -100.0% 82.7 -100.0% 79.7 -100.0%
+ THINKBRAKE-p 89.1 -0.5% 91.5 -3.2% 92.0 -12.3% 84.5 -7.1% 80.2 -6.2% 80.8 -0.7% 75.0 -9.1% 66.7 -15.6% 64.4 -1.6% 85.1 -3.3% 80.9 -6.0%
+ THINKBRAKE 88.9 -5.4% 91.0 -3.7% 91.0 -14.3% 90.0 -7.3% 79.8 -7.8% 81.5 -2.2% 68.8 -4.6% 58.0 -13.3% 64.4 -1.5% 85.5 -1.1% 79.9 -6.1%


DeepSeek-R1-7B 57.8 - 61.0 - 52.5 - 38.0 - 54.7 - 41.7 - 43.8 - 29.2 - 63.2 - 80.3 - 52.2 + NoWait 63.3 -2.2% 65.5 0.7% 62.0 -4.0% 42.5 -6.9% 57.8 -2.0% 39.6 -3.2% 50.0 -8.9% 20.8 11.0% 64.9 0.6% 73.2 -19.3% 54.0 -3.4%
+ ThinkLess 9.6 -100.0% 23.5 -100.0% 5.0 -100.0% 5.0 -100.0% 24.0 -100.0% 20.1 -100.0% 0.0 -100.0% 4.2 -100.0% 57.4 -100.0% 88.3 -100.0% 23.7 -100.0%
+ THINKBRAKE-p 48.4 -9.7% 50.0 -9.1% 39.0 -12.1% 28.5 -11.6% 46.5 -8.3% 35.8 -7.7% 37.5 -5.8% 20.8 -5.2% 65.0 -9.3% 79.5 -26.3% 45.1 -10.5%
+ THINKBRAKE 45.3 -11.4% 50.5 -9.6% 42.0 -14.6% 37.0 -11.6% 46.1 -10.8% 35.8 -8.8% 43.8 -19.9% 16.7 -6.0% 63.4 -7.4% 76.3 -26.3% 45.7 -12.6%


Phi-4-Reasoning 82.7 - 88.0 - 87.5 - 77.5 - 70.9 - 72.6 - 81.2 - 58.3 - 77.7 - 90.5 - 78.7 + NoWait 79.1 -6.8% 83.0 -11.1% 81.0 -1.3% 75.5 -13.2% 70.5 -16.7% 67.5 -12.5% 81.2 -6.4% 58.3 -11.9% 76.6 -8.5% 90.9 -15.4% 76.4 -10.4%
+ ThinkLess 65.8 -100.0% 72.5 -100.0% 73.5 -100.0% 68.5 -100.0% 56.2 -100.0% 66.3 -100.0% 87.5 -100.0% 50.0 -100.0% 76.3 -100.0% 90.5 -100.0% 70.7 -100.0%
+ THINKBRAKE-p 80.4 -30.0% 85.5 -22.0% 88.5 -37.8% 80.0 -39.1% 62.8 -36.2% 62.8 -26.4% 87.5 -42.8% 50.0 -28.7% 75.2 -36.1% 91.3 -43.8% 76.4 -34.3%
+ THINKBRAKE 81.6 0.9% 87.5 -4.2% 84.5 2.7% 77.5 -6.4% 69.4 -8.1% 72.2 -1.9% 75.0 4.6% 70.8 -4.9% 77.2 -2.5% 90.3 -5.4% 78.6 -2.5%


Table 15: Results on BFCL-v1, BFCL-v2, and Meta-Tool benchmarks. We report accuracy and ∆Tok for all
subcategories (Simple, Multiple, Parallel, Multi-Parallel for BFCL; Single, Multiple for Meta-Tool) across all
methods.


Model Metric Statistics AIME2024 AIME2025


Baseline THINKBRAKE Baseline THINKBRAKE


Variance 18.2 20.2 23.7 43.1
Accuracy
95% CI [76.2, 79.2] [65.6, 68.7] [74.5, 77.8] [60.5, 65.1]
Qwen3-4B-Thinking

Variance 78,749,681 33,023,520 74,600,230 37,478,663
Tokens
95% CI [18,870, 19,994] [12,605, 13,333] [20,725, 21,819] [13,727, 14,502]


Variance 44.5 33.5 22.4 30.5
Accuracy
95% CI [47.2, 51.8] [43.4, 47.4] [36.0, 39.2] [31.3, 35.1]
DeepSeek-R1-7B

Variance 27,202,081 17,728,953 28,471,392 19,546,656
Tokens
95% CI [10,420, 11,081] [7,885, 8,418] [10,872, 11,548] [8,173, 8,733]


Table 16: Variance and 95% confidence intervals (CI) of accuracy and token count.


Model Qwen3-4B-Thinking Qwen3-4B Qwen3-14B Qwen3-32B Qwen3-Next-80B


Avg. Base Token 9,695 7,352 6,976 6,634 7,844
∆Tok -22.6% -10.7% -12.4% -7.0% -22.3%


Table 17: Token reduction rate of THINKBRAKE. We report ∆Tok (thinking token reduction vs. the Base decoding)
for Qwen3 Family.


Benchmark Problem ID Oracle THINKBRAKE ∆Tok



AIME2024


AIME2025



1 5,734 21,555 +15,821
13 4,962 11,244 +6,282
18 3,948 21,967 +18,019
20 15,969 21,394 +5,425
25 6,778 22,777 +15,999
27 4,396 14,965 +10,569
29 17,396 10,685 -6,711


9 20,393 10,190 -10,203
10 7,660 13,672 +6,012
12 6,369 21,539 +15,170
13 6,528 21,690 +15,162
19 2,730 12,770 +10,040
25 8,097 21,605 +13,508
27 11,175 22,880 +11,705
28 6,490 22,424 +15,934
29 4,391 21,641 +17,250



Table 18: Token comparison (Oracle vs. THINKBRAKE) on AIME2024 and AIME2025 for Qwen3-4B-Thinking.


<think>
...

But wait, in the problem, they say "the circumcircle of triangle DEF intersects BD, AE, AF at G, H,
J". Wait, BD: B to D, D is midpoint of BC, so BD is a median? Wait, no, median from B should go
to midpoint of AC, but here D is midpoint of BC, so BD is not a median, it’s a segment from vertex B
to midpoint of side BC? Wait, that’s just half of side BC! Wait, hold on, that can’t be. Wait, maybe I
misread the problem. Wait, let’s check again: "D, E, and F be the midpoints of sides BC, AC, and
AB, respectively." So yes: D _∈_ BC, midpoint; E _∈_ AC, midpoint; F _∈_ AB, midpoint.
// Oracle Stopping point


Then "the circumcircle of triangle DEF intersects BD, AE, and AF at points G, H, J, respectively."
Wait, BD: B is a vertex, D is midpoint of BC, so BD is the segment from B to D, which is half of BC?
// Spurious Reasoning begins
...
Yes! This makes perfect sense now. The nine-point circle passes through the three feet of the altitudes
and the three midpoints of the sides, so each side of the triangle intersects the nine-point circle at
exactly two points: the midpoint of the side and the foot of the altitude from the opposite vertex.
// False Confidence, ThinkBrake stopping leads to wrong answer
...

I can’t believe I didn’t remember that the nine-point circle passes through the feet of the altitudes
earlier—
// Correction after continued Reasoning


Table 19: Spurious reasoning example from AIME2025-19. The model initially reaches a correct interpretation
(oracle stopping point), but continues spurious reasoning, leading THINKBRAKE to terminate at a false-confidence
state.


Qwen3-4B-Thinking


60


50


40


30


20


10


0

|Col1|Col2|Col3|Col4|Col5|Col6|Col7|Col8|Col9|Col10|Col11|Col12|Col13|Col14|Col15|Col16|Col17|Col18|Col19|Col20|Col21|Col22|Col23|Col24|Col25|Col26|Col27|Col28|Col29|Col30|Col31|Col32|Col33|Col34|Col35|Col36|Col37|Col38|Col39|Col40|Col41|Col42|Col43|Col44|%|Col46|Col47|Col48|Col49|Col50|Col51|Col52|Col53|Col54|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|||||||||||||||||||||||||||||||||||||||.2%|.2%|.2%|.2%|.2%|.2%|7.4|7.4|7.4|7.4|7.4|7.4|||||
|||||||||||||||||||||||||||||||||||||||7.9%<br>55|7.9%<br>55|7.9%<br>55|7.9%<br>55|7.9%<br>55|7.9%<br>55|50.7%<br>5|50.7%<br>5|50.7%<br>5|50.7%<br>5|50.7%<br>5|50.7%<br>5|||||
|||||||||||||||||||||||||||||||||||||||7.9%<br>55|7.9%<br>55|7.9%<br>55|7.9%<br>55|7.9%<br>55|7.9%<br>55|50.7%<br>5|50.7%<br>5|||||||||
|||||||||||||||||||||||||||||||||||||||7.9%<br>55|7.9%<br>55|||||||||||||||
||||||||||6.5%<br>42.5%|6.5%<br>42.5%|6.5%<br>42.5%|6.5%<br>42.5%|6.5%<br>42.5%|6.5%<br>42.5%||||||3%<br>6.3%|3%<br>6.3%|3%<br>6.3%|3%<br>6.3%|3%<br>6.3%|3%<br>6.3%|||||||8%<br>7.5%|8%<br>7.5%|8%<br>7.5%|8%<br>7.5%|8%<br>7.5%|8%<br>7.5%|4|4||7.5%<br>41.6%|7.5%<br>41.6%|7.5%<br>41.6%|||||||38.4%|38.4%|38.4%|38.4%|
||||||||||6.5%<br>42.5%|6.5%<br>42.5%|6.5%<br>42.5%|6.5%<br>42.5%|6.5%<br>42.5%|6.5%<br>42.5%||||||3%<br>6.3%|3%<br>6.3%|3%<br>6.3%|3%<br>6.3%|3%<br>6.3%|3%<br>6.3%|||||||8%<br>7.5%|8%<br>7.5%|8%<br>7.5%|8%<br>7.5%|8%<br>7.5%|8%<br>7.5%|4||||||||||||||||
||||||||||6.5%<br>42.5%|6.5%<br>42.5%||||||||||||||||||||||||||||||||||||||||||||
||||29.1%<br><br>32.2<br>.0%<br>29.3%|29.1%<br><br>32.2<br>.0%<br>29.3%|29.1%<br><br>32.2<br>.0%<br>29.3%|29.1%<br><br>32.2<br>.0%<br>29.3%|29.1%<br><br>32.2<br>.0%<br>29.3%|29.1%<br><br>32.2<br>.0%<br>29.3%|3|3|||||31.5%<br>33.0<br>%<br>6%|31.5%<br>33.0<br>%<br>6%|31.5%<br>33.0<br>%<br>6%|31.5%<br>33.0<br>%<br>6%|31.5%<br>33.0<br>%<br>6%|34.<br>3|34.<br>3|34.<br>3|34.<br>3|34.<br>3|34.<br>3|||||||34.<br><br><br>%|34.<br><br><br>%|34.<br><br><br>%|34.<br><br><br>%|34.<br><br><br>%|34.<br><br><br>%||||3|3|||||%<br>2%|%<br>2%|%<br>2%|32.0%|32.0%|32.0%|32.0%|
||||29.1%<br><br>32.2<br>.0%<br>29.3%|29.1%<br><br>32.2<br>.0%<br>29.3%|29.1%<br><br>32.2<br>.0%<br>29.3%|29.1%<br><br>32.2<br>.0%<br>29.3%|29.1%<br><br>32.2<br>.0%<br>29.3%|29.1%<br><br>32.2<br>.0%<br>29.3%|3|||||||||||||||||||||||||||||||||||||||||||||
||||29.1%<br><br>32.2<br>.0%<br>29.3%|29.1%<br><br>32.2<br>.0%<br>29.3%|29.1%<br><br>32.2<br>.0%<br>29.3%|29.1%<br><br>32.2<br>.0%<br>29.3%|29.1%<br><br>32.2<br>.0%<br>29.3%|||||||||||||||||||||||||||||||||||||||||||||||
|21.7%<br>22.5|21.7%<br>22.5|21.7%<br>22.5|25|25||||||||19.9%<br>9.2%|19.9%<br>9.2%|19.9%<br>9.2%|23.5<br>24.|23.5<br>24.|23.5<br>24.||||||.6%<br>.2%|.6%<br>.2%|.6%<br>.2%|8.9%<br><br>9.6%<br>8.4%<br>20.2%|8.9%<br><br>9.6%<br>8.4%<br>20.2%|8.9%<br><br>9.6%<br>8.4%<br>20.2%|8.9%<br><br>9.6%<br>8.4%<br>20.2%|8.9%<br><br>9.6%<br>8.4%<br>20.2%|8.9%<br><br>9.6%<br>8.4%<br>20.2%|21.5%<br>23.2|21.5%<br>23.2|21.5%<br>23.2|21.5%<br>23.2||||||||||||22.8<br>25|22.8<br>25|22.8<br>25|||||
||||||||||||||||||||||||17<br>1|17<br>1|17<br>1|1|1||1<br>|1<br>|1<br>|||||||||||||||||||||||
|0.0%||||||0.0%||||||0.0%|||||0.0%||||||0.0%||||||0.0%||||||0.0%||||||0.0%||||||0.0%|||||||

GSM8K GPQA-D ARC-C BFCL-V1 META-TOOL BFCL-V2 AIME2024 AIME2025 MATH500


Qwen3-4B


60


50


40


30


20


10


0

|Col1|Col2|Col3|Col4|Col5|Col6|Col7|Col8|Col9|Col10|Col11|Col12|Col13|Col14|Col15|Col16|Col17|Col18|Col19|Col20|Col21|Col22|Col23|Col24|Col25|Col26|Col27|Col28|Col29|Col30|Col31|Col32|Col33|Col34|Col35|Col36|Col37|Col38|Col39|Col40|Col41|Col42|Col43|Col44|Col45|Col46|Col47|Col48|Col49|Col50|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|||||||||||||||||||||||||||||||||||||||||||||||||||
||||%<br>%|%<br>%|%<br>%|%<br>%|%<br>%|%<br>%|%|%|%|%|%|%||||||||||||||||||||||||||||||||||||
|30.1%<br>30.0%|30.1%<br>30.0%|30.1%<br>30.0%|29.7%<br><br>8.0%<br>33.0<br>34.3|29.7%<br><br>8.0%<br>33.0<br>34.3|29.7%<br><br>8.0%<br>33.0<br>34.3|29.7%<br><br>8.0%<br>33.0<br>34.3|29.7%<br><br>8.0%<br>33.0<br>34.3|29.7%<br><br>8.0%<br>33.0<br>34.3|32.0%<br>32.9|32.0%<br>32.9|32.0%<br>32.9|32.0%<br>32.9|32.0%<br>32.9|32.0%<br>32.9||||||||||||||||||||||||||||||||||||
|30.1%<br>30.0%|30.1%<br>30.0%|30.1%<br>30.0%|29.7%<br><br>8.0%<br>33.0<br>34.3|||||||||||||||||||||||||||||||||||||||||||||||
||||||||||||||||%<br>%|%<br>%|%<br>%|%<br>%|%<br>%|%<br>7%|%<br>7%|%<br>7%|%<br>7%||||||3%|3%|3%|3%|3%|%<br><br>.3%<br>19.4%<br>21.7%|%<br><br>.3%<br>19.4%<br>21.7%|%<br><br>.3%<br>19.4%<br>21.7%|%<br><br>.3%<br>19.4%<br>21.7%|%<br><br>.3%<br>19.4%<br>21.7%|%<br><br>.3%<br>19.4%<br>21.7%|%<br><br>8%<br>5%|%<br><br>8%<br>5%|%<br><br>8%<br>5%|%<br><br>8%<br>5%|%<br><br>8%<br>5%|%<br><br>8%<br>5%|7.9%<br>20.2%|7.9%<br>20.2%|7.9%<br>20.2%|7.9%<br>20.2%|
|||||||||||||||||||||||||||||||||||||||||||||||||||
|||||||||||||||||||||||||||||||||||||||||||||||||||
|||||||||||||11.5%<br>12.5%|11.5%<br>12.5%|11.5%<br>12.5%|11.9%<br><br>12.7<br>13.7<br>14.0|11.9%<br><br>12.7<br>13.7<br>14.0|11.9%<br><br>12.7<br>13.7<br>14.0|11.9%<br><br>12.7<br>13.7<br>14.0|11.9%<br><br>12.7<br>13.7<br>14.0|13.3<br>14.|13.3<br>14.|13.3<br>14.|13.3<br>14.||||||12.7%<br><br>15.<br>%<br>%|12.7%<br><br>15.<br>%<br>%|12.7%<br><br>15.<br>%<br>%|12.7%<br><br>15.<br>%<br>%|12.7%<br><br>15.<br>%<br>%||||13.5<br>1|13.5<br>1|13.5<br>1|14.4<br><br>15<br>8.6%<br>14.|14.4<br><br>15<br>8.6%<br>14.|14.4<br><br>15<br>8.6%<br>14.|14.4<br><br>15<br>8.6%<br>14.|14.4<br><br>15<br>8.6%<br>14.|14.4<br><br>15<br>8.6%<br>14.|1|1|||
|||||||||||||11.5%<br>12.5%|11.5%<br>12.5%|11.5%<br>12.5%|11.9%<br><br>12.7<br>13.7<br>14.0|11.9%<br><br>12.7<br>13.7<br>14.0|11.9%<br><br>12.7<br>13.7<br>14.0|11.9%<br><br>12.7<br>13.7<br>14.0|11.9%<br><br>12.7<br>13.7<br>14.0|13.3<br>14.|13.3<br>14.|13.3<br>14.|13.3<br>14.||||||12.7%<br><br>15.<br>%<br>%|12.7%<br><br>15.<br>%<br>%|12.7%<br><br>15.<br>%<br>%|12.7%<br><br>15.<br>%<br>%|12.7%<br><br>15.<br>%<br>%||||13.5<br>1|13.5<br>1|13.5<br>1|14.4<br><br>15<br>8.6%<br>14.|14.4<br><br>15<br>8.6%<br>14.|14.4<br><br>15<br>8.6%<br>14.|14.4<br><br>15<br>8.6%<br>14.|14.4<br><br>15<br>8.6%<br>14.|14.4<br><br>15<br>8.6%<br>14.|1||||
|||||||||||||11.5%<br>12.5%|11.5%<br>12.5%|||||||||||||||||||||||||||||||||||||
|0.0%||||||0.0%||||||0.0%|||||0.0%||||||0.0%<br>1.9%<br>1.5%|0.0%<br>3.8%<br><br>3.7<br>2.2%<br>2.5%|0.0%<br>3.8%<br><br>3.7<br>2.2%<br>2.5%|0.0%<br>3.8%<br><br>3.7<br>2.2%<br>2.5%|0.0%<br>3.8%<br><br>3.7<br>2.2%<br>2.5%|0.0%<br>3.8%<br><br>3.7<br>2.2%<br>2.5%|0.0%<br><br>4.9<br>5.9|0.0%<br><br>4.9<br>5.9|0.0%<br><br>4.9<br>5.9||||||0.0%||||||0.0%|||||||
|0.0%||||||0.0%||||||0.0%|||||0.0%||||||0.0%<br>1.9%<br>1.5%|0.0%<br>3.8%<br><br>3.7<br>2.2%<br>2.5%|0.0%<br>3.8%<br><br>3.7<br>2.2%<br>2.5%|0.0%<br>3.8%<br><br>3.7<br>2.2%<br>2.5%|0.0%<br>3.8%<br><br>3.7<br>2.2%<br>2.5%|0.0%<br>3.8%<br><br>3.7<br>2.2%<br>2.5%|0.0%<br><br>4.9<br>5.9|0.0%<br><br>4.9<br>5.9|0.0%<br><br>4.9<br>5.9||||||0.0%|||||||||||||
|0.0%||||||0.0%||||||0.0%|||||0.0%||||||0.0%<br>1.9%<br>1.5%|||||||||||||||||||||||||||

GSM8K GPQA-D ARC-C BFCL-V1 META-TOOL BFCL-V2 AIME2024 AIME2025 MATH500


Qwen3-14B


60


50


40


30


20


10


0

|Col1|Col2|Col3|Col4|Col5|Col6|Col7|Col8|Col9|8%|Col11|Col12|Col13|Col14|Col15|Col16|Col17|Col18|Col19|Col20|Col21|Col22|Col23|Col24|Col25|Col26|Col27|Col28|Col29|Col30|Col31|Col32|Col33|Col34|Col35|Col36|Col37|Col38|Col39|Col40|Col41|Col42|Col43|Col44|Col45|Col46|Col47|Col48|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
||||||||||6.9%<br>54.|6.9%<br>54.|6.9%<br>54.|6.9%<br>54.|6.9%<br>54.|6.9%<br>54.||||||||||||||||||||||||||||||||||
||||||||||6.9%<br>54.|6.9%<br>54.||||||||||||||||||||||||||||||||||||||
||||39.9%<br>41.2%|39.9%<br>41.2%|39.9%<br>41.2%|39.9%<br>41.2%|39.9%<br>41.2%|39.9%<br>41.2%|4|4||||||||||||||||||||||||||||||||||||||
||||39.9%<br>41.2%|39.9%<br>41.2%|39.9%<br>41.2%|39.9%<br>41.2%|39.9%<br>41.2%|39.9%<br>41.2%|4|||||||||||||||||||||||||||||||||||||||
|||||||||||||||||||||||||||||||||||||||||||||||||
|%<br>%|%<br>%|%<br>%|8.0%<br>22.3%|8.0%<br>22.3%|8.0%<br>22.3%|8.0%<br>22.3%||||||8.2%<br>7.9%|8.2%<br>7.9%|8.2%<br>7.9%|21.4%<br>20.6%|21.4%<br>20.6%|21.4%<br>20.6%|21.4%<br>20.6%|21.4%<br>20.6%|%<br>7.6%|%<br>7.6%|%<br>7.6%|%<br>7.6%|%<br>7.6%|%<br>7.6%|||||||||||||||||||||||
|15.4<br>15.|15.4<br>15.|15.4<br>15.|1|1||||||||1<br>1|1<br>1|1<br>1|||12.1%<br>13.2|12.1%<br>13.2|12.1%<br>13.2|%<br><br><br>15.3<br>1|%<br><br><br>15.3<br>1|%<br><br><br>15.3<br>1|%<br><br><br>15.3<br>1|%<br><br><br>15.3<br>1|%<br><br><br>15.3<br>1|.7%<br><br>6.5%<br>%<br>%|.7%<br><br>6.5%<br>%<br>%|.7%<br><br>6.5%<br>%<br>%|7.4%<br><br>7.8%<br>7.6%<br>8.7%|7.4%<br><br>7.8%<br>7.6%<br>8.7%|7.4%<br><br>7.8%<br>7.6%<br>8.7%|7.4%<br><br>7.8%<br>7.6%<br>8.7%|7.4%<br><br>7.8%<br>7.6%<br>8.7%|7.4%<br><br>7.8%<br>7.6%<br>8.7%|6.0%<br><br>7.1%<br>10.4%<br>8%|6.0%<br><br>7.1%<br>10.4%<br>8%|6.0%<br><br>7.1%<br>10.4%<br>8%|6.0%<br><br>7.1%<br>10.4%<br>8%|7.7%<br><br>8.1%<br>10.2%<br>3%|7.7%<br><br>8.1%<br>10.2%<br>3%|7.7%<br><br>8.1%<br>10.2%<br>3%|7.7%<br><br>8.1%<br>10.2%<br>3%|7.7%<br><br>8.1%<br>10.2%<br>3%|7.4%<br>9.2%|7.4%<br>9.2%|7.4%<br>9.2%|7.4%<br>9.2%|
|15.4<br>15.|15.4<br>15.|15.4<br>15.|1|||||||||||||||||||||||||||||||||||||||||||||
|15.4<br>15.||||||||||||||||||||||||||||||||||||||||||||||||
|15.4<br>15.||||||||||||||||||||||||||||||||||||||||||||||||
|0.0%||||||0.0%||||||0.0%|||||0.0%||||||0.0%<br>2.4<br>2.6|0.0%<br>2.4<br>2.6|0.0%<br>2.4<br>2.6|0.0%<br>5<br><br><br>3.1<br>3.3|0.0%<br>5<br><br><br>3.1<br>3.3|0.0%<br>5<br><br><br>3.1<br>3.3||||0.0%|||||0.0%<br><br>3.||||0.0%<br>4.|||||||
|0.0%||||||0.0%||||||0.0%|||||0.0%||||||0.0%<br>2.4<br>2.6|||||||||||||||||||||||||

GSM8K GPQA-D ARC-C BFCL-V1 META-TOOL BFCL-V2 AIME2024 AIME2025 MATH500


Baseline = 0.1 = 0.25 = 1.0 = 2.5


Figure 13: Token reduction across various threshold values _τ_ for Qwen3-4B, Qwen3-4B-Thinking, and Qwen3-14B.


Qwen3-32B


60


50


40


30


20


10


0

|Col1|Col2|Col3|Col4|Col5|Col6|Col7|Col8|Col9|Col10|Col11|Col12|Col13|Col14|Col15|Col16|Col17|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
||||||||||||||||||
||||||||||||||||||
|||||||30.9%|30.9%|30.9%|30.9%||||||||
||19.9%<br>22.5<br>%<br>18.5%|19.9%<br>22.5<br>%<br>18.5%|19.9%<br>22.5<br>%<br>18.5%|19.9%<br>22.5<br>%<br>18.5%|19.9%<br>22.5<br>%<br>18.5%|20.6%|20.6%||||6%|||6%|||
||19.9%<br>22.5<br>%<br>18.5%|19.9%<br>22.5<br>%<br>18.5%|19.9%<br>22.5<br>%<br>18.5%|19.9%<br>22.5<br>%<br>18.5%|||||||||||||
|.0%<br>9.1%<br>10.8%|12.9<br>||.0%||||||.0%<br>8.0%<br>8.3%|.0%<br>7.4%<br><br>7.5%<br>9.2%<br>11.8%|.0%<br>0.1%<br><br>.0%<br>10.5%<br>14.|.0%<br>3.0%<br><br>1.8%<br>1.3%<br>2.7%|.0%<br>6.2%<br><br>6.6%<br>2.4%<br>2.9%|.0%<br>4.3%<br><br>5.5%<br>10.5%<br>14.|.0%<br>1.4%<br><br>3.2%<br>10.7%<br>6.0%|6.6%<br>6.9%|

GSM8K GPQA-D ARC-C BFCL-V1 META-TOOL BFCL-V2 AIME2024 AIME2025 MATH500


60


50


40


30


20


10


0

|% 7|Col2|Col3|Col4|Col5|Col6|Col7|Col8|Col9|Col10|Col11|7|DeepSeek-R1-7B|Col14|Col15|Col16|Col17|Col18|Col19|Col20|Col21|Col22|Col23|Col24|Col25|Col26|Col27|Col28|Col29|Col30|Col31|Col32|Col33|Col34|Col35|Col36|Col37|Col38|Col39|Col40|Col41|Col42|Col43|Col44|Col45|Col46|Col47|Col48|Col49|Col50|Col51|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|.5%<br>6.2%<br>62.8%|.5%<br>6.2%<br>62.8%|.5%<br>6.2%<br>62.8%|.5%<br>6.2%<br>62.8%|.5%<br>6.2%<br>62.8%|.5%<br>6.2%<br>62.8%|.5%<br>6.2%<br>62.8%|.5%<br>6.2%<br>62.8%|.5%<br>6.2%<br>62.8%|.5%<br>6.2%<br>62.8%|.5%<br>6.2%<br>62.8%|||||||||||||||||||||||||||||||||||||||||
|.5%<br>6.2%<br>62.8%|.5%<br>6.2%<br>62.8%|.5%<br>6.2%<br>62.8%|.5%<br>6.2%<br>62.8%|.5%<br>6.2%<br>62.8%|.5%<br>6.2%<br>62.8%|.5%<br>6.2%<br>62.8%|.5%<br>6.2%<br>62.8%|.5%<br>6.2%<br>62.8%|.5%<br>6.2%<br>62.8%||||||||||||||||||||||||||||||||||||||||||
||||55<br>5<br>%|55<br>5<br>%|55<br>5<br>%|55<br>5<br>%|55<br>5<br>%|55<br>5<br>%|||||||||||||||||||||||||||5.6%|5.6%|5.6%|5.6%|5.6%|5.6%|48.8%|48.8%|48.8%|48.8%|48.8%|48.8%|||||
||||55<br>5<br>%|55<br>5<br>%|55<br>5<br>%|55<br>5<br>%|||||||||||||||||||||||||||||||||||||||||||||
||||6%<br>42.2|6%<br>42.2|6%<br>42.2|6%<br>42.2|||||||||.6%|.6%|.6%|.6%|.6%||||||||||||||||6.2%<br>4|6.2%<br>4|6.2%<br>4|6.2%<br>4|6.2%<br>4|6.2%<br>4|%|%|||||6.8%|6.8%|6.8%|6.8%|
||||6%<br>42.2|6%<br>42.2|6%<br>42.2|6%<br>42.2|||||||||.6%|.6%|.6%|.6%|.6%||||||||||||||||6.2%<br>4|6.2%<br>4|||||||||||||||
||||6%<br>42.2|6%<br>42.2|||||||||||||||||||||||||||||||||||||||||||||||
|7.4%<br>29.9%|7.4%<br>29.9%|7.4%<br>29.9%|34.|34.||||||||30.3%<br>27.8%|30.3%<br>27.8%|30.3%<br>27.8%|30.0%<br>35|30.0%<br>35|30.0%<br>35|30.0%<br>35|30.0%<br>35|||||||||||6.6%<br>29.8%|6.6%<br>29.8%|6.6%<br>29.8%|6.6%<br>29.8%|6.6%<br>29.8%|3|3||6.6%<br>.4%|6.6%<br>.4%|6.6%<br>.4%|32.2|32.2|||||.9%<br>3|.9%<br>3|.9%<br>3|.9%<br>3|
|7.4%<br>29.9%|7.4%<br>29.9%|7.4%<br>29.9%|34.||||||||||||||||||||||||||||||||||||||||||||||||
|7.4%<br>29.9%|7.4%<br>29.9%|7.4%<br>29.9%|34.||||||||||||||||||||||||||||||||||||||||||||||||
|2|2||||||||||||||||%<br>|%<br>|%<br>|9%<br><br>.5%<br>%<br>.7%|9%<br><br>.5%<br>%<br>.7%|9%<br><br>.5%<br>%<br>.7%|9%<br><br>.5%<br>%<br>.7%|9%<br><br>.5%<br>%<br>.7%|9%<br><br>.5%<br>%<br>.7%|17.2%<br>20.2%|17.2%<br>20.2%|17.2%<br>20.2%|17.2%<br>20.2%|2<br>%|2<br>%|2<br>%|2<br>%|||||2<br>25|2<br>25|2<br>25||||18.3%<br>18.9%|18.3%<br>18.9%|18.3%<br>18.9%|25|25|||
|2|||||||||||||||||||||||||||||||||||||||||||||||||||
||||||||||||||||||11.6<br>11.5|11.6<br>11.5|11.6<br>11.5|13.<br><br>1<br>12.5<br>14|13.<br><br>1<br>12.5<br>14|13.<br><br>1<br>12.5<br>14|13.<br><br>1<br>12.5<br>14|13.<br><br>1<br>12.5<br>14|13.<br><br>1<br>12.5<br>14||||.9%<br>.9%|9.4%<br>10.9|9.4%<br>10.9|9.4%<br>10.9|||||||||||||||||||
|0.0%||||||0.0%||||||0.0%|||||0.0%||||||0.0%||||||0.0%<br>8<br>|||0.0%||||||0.0%||||||0.0%|||||||

GSM8K GPQA-D ARC-C BFCL-V1 META-TOOL BFCL-V2 AIME2024 AIME2025 MATH500


Phi-4-Reasoning


60


50


40


30


20


10


0

|Col1|Col2|Col3|Col4|Col5|Col6|Col7|Col8|Col9|Col10|Col11|Col12|Col13|Col14|Col15|Col16|Col17|Col18|Col19|Col20|Col21|Col22|Col23|Col24|Col25|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
||||||||||||||||||||||||||
||||||||||||||||||||||||||
||||6%|6%|6%|6%|6%||||3%|3%|3%||||||||||||
|5.9%<br>.3%|5.9%<br>.3%|5.9%<br>.3%|21.2%<br>25.|21.2%<br>25.|21.2%<br>25.|21.2%<br>25.|21.2%<br>25.|18.1%<br>18.6%|18.1%<br>18.6%|18.1%<br>18.6%|22.2%<br>25.|22.2%<br>25.|22.2%<br>25.|||||5%|5%|5%|%<br>17.2%|%<br>17.2%|%<br>17.2%|%<br>17.2%|
|5.9%<br>.3%|5.9%<br>.3%|5.9%<br>.3%|21.2%<br>25.|21.2%<br>25.|||||||||||||||||||||
|1<br>1|1<br>1|1<br>1||||.5%|.5%|%|||||||||%<br>4%|13.<br>%<br>%|13.<br>%<br>%|13.<br>%<br>%|12.4<br>|12.4<br>|||
|1<br>1|1<br>1|1<br>1||||.5%|.5%|%|||||||||%<br>4%|13.<br>%<br>%|||||||
|0.0%||||||0.0%<br>4.0%<br>|0.0%<br>4.0%<br>|0.0%<br><br>4.6<br>1.1%|||||0.0%<br>.4%<br>.7%|0.0%<br>0.1%<br><br>0.8%<br>1.1%<br>1.4%|0.0%<br>0.5%<br><br>-0.3%<br>2.3%<br>3.4%|0.0%<br>1.7%<br><br>3.5<br>1.5%<br>2.7%|0.0%<br>9%<br><br>2.8%<br>5.8<br>6.|0.0%<br><br>0.3%<br>5.2||6.|||||
|0.0%||||||0.0%<br>4.0%<br>|||||||||||||||||||

GSM8K GPQA-D ARC-C BFCL-V1 META-TOOL BFCL-V2 AIME2024 AIME2025 MATH500


Baseline = 0.1 = 0.25 = 1.0 = 2.5


Figure 14: Token reduction across various threshold values _τ_ for Qwen3-32B, DeepSeek-R1-7B, and Phi-4Reasoning.


Qwen3-4B-Thinking


100


80


60


40


20


0

|% % %|Col2|Col3|Col4|% 9% % 9% % %|Col6|Col7|Col8|Col9|Col10|Col11|9% 6% %|Col13|Col14|Col15|Col16|Col17|Col18|Col19|Col20|Col21|Col22|Col23|Col24|Col25|Col26|Col27|Col28|Col29|Col30|Col31|% % %|Col33|Col34|Col35|Col36|Col37|Col38|% % %|Col40|Col41|Col42|Col43|Col44|Col45|Col46|Col47|Col48|Col49|Col50|Col51|Col52|Col53|Col54|Col55|Col56|Col57|Col58|Col59|Col60|Col61|Col62|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|5.1<br>4.7<br>.7|5.1<br>4.7<br>.7|5.1<br>4.7<br>.7|5.1<br>4.7<br>.7|5.3<br>5.9<br><br>5.<br>.2<br>4.6|5.3<br>5.9<br><br>5.<br>.2<br>4.6|5.3<br>5.9<br><br>5.<br>.2<br>4.6|5.3<br>5.9<br><br>5.<br>.2<br>4.6|5.3<br>5.9<br><br>5.<br>.2<br>4.6|5.3<br>5.9<br><br>5.<br>.2<br>4.6|5.3<br>5.9<br><br>5.<br>.2<br>4.6|5.6<br>4.6|5.6<br>4.6|5.6<br>4.6|5.6<br>4.6|5.6<br>4.6|5.6<br>4.6|5.6<br>4.6||||||||||||||4.3<br>.7%<br>.0|4.3<br>.7%<br>.0|4.3<br>.7%<br>.0|4.3<br>.7%<br>.0|4.3<br>.7%<br>.0|4.3<br>.7%<br>.0|4.3<br>.7%<br>.0|%<br>8%<br><br><br>.1<br>.7%|%<br>8%<br><br><br>.1<br>.7%|%<br>8%<br><br><br>.1<br>.7%|%<br>8%<br><br><br>.1<br>.7%|%<br>8%<br><br><br>.1<br>.7%|%<br>8%<br><br><br>.1<br>.7%|%<br>8%<br><br><br>.1<br>.7%|%<br>%|%<br>%|%<br>%|%<br>%|%<br>%|%<br>%||||||||||||
|9<br>9<br>9|9<br>9<br>9|9<br>9<br>9|9<br>9<br>9|9<br>9<br><br><br>94<br>9|9<br>9<br><br><br>94<br>9|9<br>9<br><br><br>94<br>9|9<br>9<br><br><br>94<br>9|9<br>9<br><br><br>94<br>9|9<br>9<br><br><br>94<br>9|9<br>9<br><br><br>94<br>9|7.2%<br><br>9<br>9|7.2%<br><br>9<br>9|7.2%<br><br>9<br>9|7.2%<br><br>9<br>9|7.2%<br><br>9<br>9|7.2%<br><br>9<br>9|7.2%<br><br>9<br>9|6.2%|6.2%|6.2%|6.2%|6.2%|6.2%||||||||9<br>93<br>9|9<br>93<br>9|9<br>93<br>9|9<br>93<br>9|9<br>93<br>9|9<br>93<br>9|9<br>93<br>9|90.7<br>90.<br><br>88.0<br>94<br>93|90.7<br>90.<br><br>88.0<br>94<br>93|90.7<br>90.<br><br>88.0<br>94<br>93|90.7<br>90.<br><br>88.0<br>94<br>93|90.7<br>90.<br><br>88.0<br>94<br>93|90.7<br>90.<br><br>88.0<br>94<br>93|90.7<br>90.<br><br>88.0<br>94<br>93|82.5%<br>85.0%<br><br>82.7%<br>88.1<br>88.8|82.5%<br>85.0%<br><br>82.7%<br>88.1<br>88.8|82.5%<br>85.0%<br><br>82.7%<br>88.1<br>88.8|82.5%<br>85.0%<br><br>82.7%<br>88.1<br>88.8|82.5%<br>85.0%<br><br>82.7%<br>88.1<br>88.8|82.5%<br>85.0%<br><br>82.7%<br>88.1<br>88.8|.0%<br>7.0%<br><br>.6%<br>82.0%<br>81.8%|.0%<br>7.0%<br><br>.6%<br>82.0%<br>81.8%|.0%<br>7.0%<br><br>.6%<br>82.0%<br>81.8%|.0%<br>7.0%<br><br>.6%<br>82.0%<br>81.8%|.0%<br>7.0%<br><br>.6%<br>82.0%<br>81.8%|.0%<br>7.0%<br><br>.6%<br>82.0%<br>81.8%|.0%<br>7.0%<br><br>.6%<br>82.0%<br>81.8%|6.9%<br>7.5%|6.9%<br>7.5%|6.9%<br>7.5%|6.9%<br>7.5%|
|9<br>9<br>9||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
|9<br>9<br>9||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
|9<br>9<br>9||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
|||||||||||||||7<br>63.7%<br>63.7%|7<br>63.7%<br>63.7%|7<br>63.7%<br>63.7%|7<br>63.7%<br>63.7%|7<br>59.2%<br><br>7.1%<br>5.0%<br>5.4%|7<br>59.2%<br><br>7.1%<br>5.0%<br>5.4%|7<br>59.2%<br><br>7.1%<br>5.0%<br>5.4%|7<br>59.2%<br><br>7.1%<br>5.0%<br>5.4%|7<br>59.2%<br><br>7.1%<br>5.0%<br>5.4%|7<br>59.2%<br><br>7.1%<br>5.0%<br>5.4%|64.1%<br>60.6%<br><br>57.6%<br>%<br>%|64.1%<br>60.6%<br><br>57.6%<br>%<br>%|64.1%<br>60.6%<br><br>57.6%<br>%<br>%|64.1%<br>60.6%<br><br>57.6%<br>%<br>%|64.1%<br>60.6%<br><br>57.6%<br>%<br>%|64.1%<br>60.6%<br><br>57.6%<br>%<br>%|64.1%<br>60.6%<br><br>57.6%<br>%<br>%|60.1%<br>61.6%|60.1%<br>61.6%|60.1%<br>61.6%|60.1%<br>61.6%||||||||||||||||||||75<br>7<br>7|75<br>7<br>7|75<br>7<br>7|75<br>7<br>7|7<br>7|7<br>7|7<br>7|7<br>7|
|||||||||||||||7<br>63.7%<br>63.7%||||||||||||||||||||||||||||||||||||||||||||||||
|||||||||||||||||||5<br>5|5<br>5|5<br>5||||50.4<br>48.3|50.4<br>48.3|50.4<br>48.3|50.4<br>48.3|||||||||||||||||||||||||||||||||||
|||||||||||||||||||5<br>5|5<br>5|5<br>5||||50.4<br>48.3||||||||||||||||||||||||||||||||||||||
|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||

GSM8K MATH500 AIME24 AIME25 GPQA-D ARC-C BFCL-V1 BFCL-V2 META-TOOL


Qwen3-4B


100


80


60


40


20


0

|% % %|Col2|Col3|Col4|0% % % % % %|Col6|Col7|Col8|Col9|Col10|Col11|% % 0%|Col13|Col14|Col15|Col16|Col17|Col18|Col19|Col20|Col21|Col22|Col23|Col24|Col25|Col26|Col27|Col28|Col29|Col30|Col31|% % %|Col33|Col34|Col35|Col36|Col37|Col38|% % %|Col40|Col41|Col42|Col43|Col44|Col45|Col46|Col47|Col48|Col49|Col50|Col51|Col52|Col53|Col54|Col55|Col56|Col57|Col58|Col59|Col60|Col61|Col62|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|4.4<br>4.5<br>.4|4.4<br>4.5<br>.4|4.4<br>4.5<br>.4|4.4<br>4.5<br>.4|6.0<br>5.4<br><br>5.6<br>4.3<br>.2|6.0<br>5.4<br><br>5.6<br>4.3<br>.2|6.0<br>5.4<br><br>5.6<br>4.3<br>.2|6.0<br>5.4<br><br>5.6<br>4.3<br>.2|6.0<br>5.4<br><br>5.6<br>4.3<br>.2|6.0<br>5.4<br><br>5.6<br>4.3<br>.2|6.0<br>5.4<br><br>5.6<br>4.3<br>.2|5.4<br>6.0|5.4<br>6.0|5.4<br>6.0|5.4<br>6.0|5.4<br>6.0|5.4<br>6.0|5.4<br>6.0||||||||||||||.0<br>.9<br>.9|.0<br>.9<br>.9|.0<br>.9<br>.9|.0<br>.9<br>.9|.0<br>.9<br>.9|.0<br>.9<br>.9|.0<br>.9<br>.9|%<br>%<br><br><br>.1<br>.9|%<br>%<br><br><br>.1<br>.9|%<br>%<br><br><br>.1<br>.9|%<br>%<br><br><br>.1<br>.9|%<br>%<br><br><br>.1<br>.9|%<br>%<br><br><br>.1<br>.9|%<br>%<br><br><br>.1<br>.9|%<br>%|%<br>%|%<br>%|%<br>%|%<br>%|%<br>%||||||||||||
|9<br>9<br>9|9<br>9<br>9|9<br>9<br>9|9<br>9<br>9|9<br>9<br><br><br>9<br>94|9<br>9<br><br><br>9<br>94|9<br>9<br><br><br>9<br>94|9<br>9<br><br><br>9<br>94|9<br>9<br><br><br>9<br>94|9<br>9<br><br><br>9<br>94|9<br>9<br><br><br>9<br>94|%<br><br><br>9<br>9|%<br><br><br>9<br>9|%<br><br><br>9<br>9|%<br><br><br>9<br>9|%<br><br><br>9<br>9|%<br><br><br>9<br>9|%<br><br><br>9<br>9|%|%|%|%|%|%||||||||94<br>93<br>9|94<br>93<br>9|94<br>93<br>9|94<br>93<br>9|94<br>93<br>9|94<br>93<br>9|94<br>93<br>9|88.3<br>88.2<br><br>87.4%<br>94<br>93|88.3<br>88.2<br><br>87.4%<br>94<br>93|88.3<br>88.2<br><br>87.4%<br>94<br>93|88.3<br>88.2<br><br>87.4%<br>94<br>93|88.3<br>88.2<br><br>87.4%<br>94<br>93|88.3<br>88.2<br><br>87.4%<br>94<br>93|88.3<br>88.2<br><br>87.4%<br>94<br>93|80.7%<br>80.5%<br><br>80.0%<br>88.5<br>88.8|80.7%<br>80.5%<br><br>80.0%<br>88.5<br>88.8|80.7%<br>80.5%<br><br>80.0%<br>88.5<br>88.8|80.7%<br>80.5%<br><br>80.0%<br>88.5<br>88.8|80.7%<br>80.5%<br><br>80.0%<br>88.5<br>88.8|80.7%<br>80.5%<br><br>80.0%<br>88.5<br>88.8|79.7%<br>78.8%<br><br>78.2%<br>81.3%<br>80.2%|79.7%<br>78.8%<br><br>78.2%<br>81.3%<br>80.2%|79.7%<br>78.8%<br><br>78.2%<br>81.3%<br>80.2%|79.7%<br>78.8%<br><br>78.2%<br>81.3%<br>80.2%|79.7%<br>78.8%<br><br>78.2%<br>81.3%<br>80.2%|79.7%<br>78.8%<br><br>78.2%<br>81.3%<br>80.2%|79.7%<br>78.8%<br><br>78.2%<br>81.3%<br>80.2%|79.8%<br>78.6%|79.8%<br>78.6%|79.8%<br>78.6%|79.8%<br>78.6%|
|9<br>9<br>9||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
|9<br>9<br>9||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
|||||||||||||||68.8<br>64.6%<br>66.7%|68.8<br>64.6%<br>66.7%|68.8<br>64.6%<br>66.7%|68.8<br>64.6%<br>66.7%|59.6%<br>60.4%<br><br>5.8%<br>66.7%<br>70.0|59.6%<br>60.4%<br><br>5.8%<br>66.7%<br>70.0|59.6%<br>60.4%<br><br>5.8%<br>66.7%<br>70.0|59.6%<br>60.4%<br><br>5.8%<br>66.7%<br>70.0|59.6%<br>60.4%<br><br>5.8%<br>66.7%<br>70.0|59.6%<br>60.4%<br><br>5.8%<br>66.7%<br>70.0|0%<br>5.6%<br><br>%<br>56.7%<br>.3%|0%<br>5.6%<br><br>%<br>56.7%<br>.3%|0%<br>5.6%<br><br>%<br>56.7%<br>.3%|0%<br>5.6%<br><br>%<br>56.7%<br>.3%|0%<br>5.6%<br><br>%<br>56.7%<br>.3%|0%<br>5.6%<br><br>%<br>56.7%<br>.3%|0%<br>5.6%<br><br>%<br>56.7%<br>.3%|5%<br>59.1%|5%<br>59.1%|5%<br>59.1%|5%<br>59.1%||||||||||||||||||||||||||||
|||||||||||||||68.8<br>64.6%<br>66.7%||||||||||||||||||||||||||||||||||||||||||||||||
|||||||||||||||||||||||||51.<br>5<br><br>50.<br><br>53|51.<br>5<br><br>50.<br><br>53|51.<br>5<br><br>50.<br><br>53|51.<br>5<br><br>50.<br><br>53|51.<br>5<br><br>50.<br><br>53|51.<br>5<br><br>50.<br><br>53|51.<br>5<br><br>50.<br><br>53|51.|51.||||||||||||||||||||||||||||||
|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||

GSM8K MATH500 AIME24 AIME25 GPQA-D ARC-C BFCL-V1 BFCL-V2 META-TOOL


Qwen3-14B


100


80


60


40


20


0

|6.0 5.0 5.3|Col2|Col3|Col4|5.1 5.5 96.8 96.9 96.9|Col6|Col7|Col8|Col9|Col10|Col11|6.4 96.8|Col13|Col14|Col15|Col16|Col17|Col18|Col19|Col20|Col21|Col22|Col23|Col24|Col25|Col26|Col27|Col28|Col29|Col30|Col31|5.9 5.2 4.8|Col33|Col34|Col35|Col36|Col37|Col38|5.5 5.0 % % %|Col40|Col41|Col42|Col43|Col44|Col45|% %|Col47|Col48|Col49|Col50|Col51|Col52|Col53|Col54|Col55|Col56|Col57|Col58|Col59|Col60|Col61|Col62|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|9<br>9<br>9|9<br>9<br>9|9<br>9<br>9|9<br>9<br>9|9<br>9|9<br>9|9<br>9|9<br>9|9<br>9|9<br>9|9<br>9|.7%<br>77.9%<br><br>75.8%<br>9<br>|.7%<br>77.9%<br><br>75.8%<br>9<br>|.7%<br>77.9%<br><br>75.8%<br>9<br>|.7%<br>77.9%<br><br>75.8%<br>9<br>|.7%<br>77.9%<br><br>75.8%<br>9<br>|.7%<br>77.9%<br><br>75.8%<br>9<br>|.7%<br>77.9%<br><br>75.8%<br>9<br>|2%<br><br><br>%<br>76.7%<br>83.3%|2%<br><br><br>%<br>76.7%<br>83.3%|2%<br><br><br>%<br>76.7%<br>83.3%|2%<br><br><br>%<br>76.7%<br>83.3%|2%<br><br><br>%<br>76.7%<br>83.3%|2%<br><br><br>%<br>76.7%<br>83.3%|%<br>0%|%<br>0%|%<br>0%|%<br>0%|%<br>0%|%<br>0%|%<br>0%|9<br>9<br>9|9<br>9<br>9|9<br>9<br>9|9<br>9<br>9|9<br>9<br>9|9<br>9<br>9|9<br>9<br>9|88.7<br>89.0<br><br>88.0<br>9<br>9|88.7<br>89.0<br><br>88.0<br>9<br>9|88.7<br>89.0<br><br>88.0<br>9<br>9|88.7<br>89.0<br><br>88.0<br>9<br>9|88.7<br>89.0<br><br>88.0<br>9<br>9|88.7<br>89.0<br><br>88.0<br>9<br>9|88.7<br>89.0<br><br>88.0<br>9<br>9|80.6%<br>78.9%<br><br>78.1%<br>88.8<br>88.5|80.6%<br>78.9%<br><br>78.1%<br>88.8<br>88.5|80.6%<br>78.9%<br><br>78.1%<br>88.8<br>88.5|80.6%<br>78.9%<br><br>78.1%<br>88.8<br>88.5|80.6%<br>78.9%<br><br>78.1%<br>88.8<br>88.5|80.6%<br>78.9%<br><br>78.1%<br>88.8<br>88.5|5%<br>2.8%<br><br>.6%<br>79.0%<br>79.1%|5%<br>2.8%<br><br>.6%<br>79.0%<br>79.1%|5%<br>2.8%<br><br>.6%<br>79.0%<br>79.1%|5%<br>2.8%<br><br>.6%<br>79.0%<br>79.1%|5%<br>2.8%<br><br>.6%<br>79.0%<br>79.1%|5%<br>2.8%<br><br>.6%<br>79.0%<br>79.1%|5%<br>2.8%<br><br>.6%<br>79.0%<br>79.1%|.1%<br>.4%|.1%<br>.4%|.1%<br>.4%|.1%<br>.4%|
|9<br>9<br>9||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
|9<br>9<br>9||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
|9<br>9<br>9||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
|||||||||||||||71|71|||||69.<br>65.8%<br>67.9|69.<br>65.8%<br>67.9|69.<br>65.8%<br>67.9|69.<br>65.8%<br>67.9|60.6%<br>61.1%<br><br>7.6%<br>66.7<br>70.|60.6%<br>61.1%<br><br>7.6%<br>66.7<br>70.|60.6%<br>61.1%<br><br>7.6%<br>66.7<br>70.|60.6%<br>61.1%<br><br>7.6%<br>66.7<br>70.|60.6%<br>61.1%<br><br>7.6%<br>66.7<br>70.|60.6%<br>61.1%<br><br>7.6%<br>66.7<br>70.|60.6%<br>61.1%<br><br>7.6%<br>66.7<br>70.|6.6%<br>57.1%|6.6%<br>57.1%|6.6%<br>57.1%|6.6%<br>57.1%||||||||||||||||||||70.<br>7<br>71|70.<br>7<br>71|70.<br>7<br>71|70.<br>7<br>71|71<br>72|71<br>72|71<br>72|71<br>72|
|||||||||||||||71||||||||6||||||||||||||||||||||||||||||||||||||||
||||||||||||||||||||||||||||||||5<br>|5<br>|5<br>|5<br>||||||||||||||||||||||||||||
|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||

GSM8K MATH500 AIME24 AIME25 GPQA-D ARC-C BFCL-V1 BFCL-V2 META-TOOL


Baseline t=0.1 t=0.25 t=1.0 t=2.5


Figure 15: Accuracy comparison across various threshold values _τ_ for Qwen3-4B-Thinking, Qwen3-4B, and
Qwen3-14B.


Qwen3-32B


100


80


60


40


20


0

|% % %|Col2|Col3|Col4|% % % 5% % %|Col6|Col7|Col8|Col9|Col10|Col11|5% 8% 4%|Col13|Col14|Col15|Col16|Col17|Col18|Col19|Col20|Col21|Col22|Col23|Col24|Col25|Col26|Col27|Col28|Col29|Col30|Col31|Col32|Col33|Col34|Col35|Col36|Col37|Col38|Col39|Col40|Col41|Col42|Col43|Col44|Col45|Col46|Col47|Col48|Col49|Col50|Col51|Col52|Col53|Col54|Col55|Col56|Col57|Col58|Col59|Col60|Col61|Col62|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|96.0<br>96.5<br>96.2|96.0<br>96.5<br>96.2|96.0<br>96.5<br>96.2|96.0<br>96.5<br>96.2|97.0<br>97.2<br><br>97.<br>96.1<br>96.1|97.0<br>97.2<br><br>97.<br>96.1<br>96.1|97.0<br>97.2<br><br>97.<br>96.1<br>96.1|97.0<br>97.2<br><br>97.<br>96.1<br>96.1|97.0<br>97.2<br><br>97.<br>96.1<br>96.1|97.0<br>97.2<br><br>97.<br>96.1<br>96.1|97.0<br>97.2<br><br>97.<br>96.1<br>96.1|97.8<br>97.4|97.8<br>97.4|97.8<br>97.4|97.8<br>97.4|97.8<br>97.4|97.8<br>97.4|97.8<br>97.4||||||||||||||2.1%<br>.0%<br>.9%|2.1%<br>.0%<br>.9%|2.1%<br>.0%<br>.9%|2.1%<br>.0%<br>.9%|2.1%<br>.0%<br>.9%|2.1%<br>.0%<br>.9%|2.1%<br>.0%<br>.9%|7%<br>.8%<br><br>9%<br>2.4%<br>.3%|7%<br>.8%<br><br>9%<br>2.4%<br>.3%|7%<br>.8%<br><br>9%<br>2.4%<br>.3%|7%<br>.8%<br><br>9%<br>2.4%<br>.3%|7%<br>.8%<br><br>9%<br>2.4%<br>.3%|7%<br>.8%<br><br>9%<br>2.4%<br>.3%|7%<br>.8%<br><br>9%<br>2.4%<br>.3%|8%<br>0%|8%<br>0%|8%<br>0%|8%<br>0%|8%<br>0%|8%<br>0%||||||||||||
|||||||||||||||75.8%<br>77.1%<br>78.3%|75.8%<br>77.1%<br>78.3%|75.8%<br>77.1%<br>78.3%|75.8%<br>77.1%<br>78.3%|%<br>%<br><br>77.9%<br>83.3%|%<br>%<br><br>77.9%<br>83.3%|%<br>%<br><br>77.9%<br>83.3%|%<br>%<br><br>77.9%<br>83.3%|%<br>%<br><br>77.9%<br>83.3%|%<br>%<br><br>77.9%<br>83.3%|7%<br>76.7%|7%<br>76.7%|7%<br>76.7%|7%<br>76.7%|7%<br>76.7%|7%<br>76.7%|7%<br>76.7%|9<br>91<br>9<br>|9<br>91<br>9<br>|9<br>91<br>9<br>|9<br>91<br>9<br>|9<br>91<br>9<br>|9<br>91<br>9<br>|9<br>91<br>9<br>|88.<br>89<br><br>87.<br>9<br>90|88.<br>89<br><br>87.<br>9<br>90|88.<br>89<br><br>87.<br>9<br>90|88.<br>89<br><br>87.<br>9<br>90|88.<br>89<br><br>87.<br>9<br>90|88.<br>89<br><br>87.<br>9<br>90|88.<br>89<br><br>87.<br>9<br>90|81.0%<br>80.6%<br><br>80.2%<br>88.<br>89.|81.0%<br>80.6%<br><br>80.2%<br>88.<br>89.|81.0%<br>80.6%<br><br>80.2%<br>88.<br>89.|81.0%<br>80.6%<br><br>80.2%<br>88.<br>89.|81.0%<br>80.6%<br><br>80.2%<br>88.<br>89.|81.0%<br>80.6%<br><br>80.2%<br>88.<br>89.|3%<br>.4%<br><br>.9%<br>81.1%<br>80.1%|3%<br>.4%<br><br>.9%<br>81.1%<br>80.1%|3%<br>.4%<br><br>.9%<br>81.1%<br>80.1%|3%<br>.4%<br><br>.9%<br>81.1%<br>80.1%|3%<br>.4%<br><br>.9%<br>81.1%<br>80.1%|3%<br>.4%<br><br>.9%<br>81.1%<br>80.1%|3%<br>.4%<br><br>.9%<br>81.1%<br>80.1%|9%<br>0%|9%<br>0%|9%<br>0%|9%<br>0%|
|||||||||||||||75.8%<br>77.1%<br>78.3%|75.8%<br>77.1%<br>78.3%|75.8%<br>77.1%<br>78.3%|75.8%<br>77.1%<br>78.3%|%<br>%<br><br>77.9%<br>83.3%|%<br>%<br><br>77.9%<br>83.3%|%<br>%<br><br>77.9%<br>83.3%|%<br>%<br><br>77.9%<br>83.3%|%<br>%<br><br>77.9%<br>83.3%|%<br>%<br><br>77.9%<br>83.3%|7%<br>76.7%|7%<br>76.7%|7%<br>76.7%|7%<br>76.7%|7%<br>76.7%|7%<br>76.7%|7%<br>76.7%|9<br>91<br>9<br>|9<br>91<br>9<br>|9<br>91<br>9<br>|9<br>91<br>9<br>||||||||||||||||||||||||||||
|||||||||||||||75.8%<br>77.1%<br>78.3%|75.8%<br>77.1%<br>78.3%|75.8%<br>77.1%<br>78.3%|75.8%<br>77.1%<br>78.3%|%<br>%<br><br>77.9%<br>83.3%||||||||||||||||||||||||||||||||||||||||||||
|||||||||||||||||||||68.3<br>68.3<br>63.7%|68.3<br>68.3<br>63.7%|68.3<br>68.3<br>63.7%|68.3<br>68.3<br>63.7%|65.2%<br>65.7%<br><br>62.6%<br>69.|65.2%<br>65.7%<br><br>62.6%<br>69.|65.2%<br>65.7%<br><br>62.6%<br>69.|65.2%<br>65.7%<br><br>62.6%<br>69.|65.2%<br>65.7%<br><br>62.6%<br>69.|65.2%<br>65.7%<br><br>62.6%<br>69.|65.2%<br>65.7%<br><br>62.6%<br>69.|65.7%<br>62.1%|65.7%<br>62.1%|65.7%<br>62.1%|65.7%<br>62.1%||||||||||||||||||||71.<br>71<br>71|71.<br>71<br>71|71.<br>71<br>71|71.<br>71<br>71|70.<br>71.|70.<br>71.|70.<br>71.|70.<br>71.|
|||||||||||||||||||||68.3<br>68.3<br>63.7%||||||||||||||||||||||||||||||||||||||||||
|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||

GSM8K MATH500 AIME24 AIME25 GPQA-D ARC-C BFCL-V1 BFCL-V2 META-TOOL


DeepSeek-R1-7B


100


80


60


40


20


0

|% % %|Col2|Col3|Col4|8% % % % %|Col6|Col7|Col8|Col9|Col10|Col11|% % %|Col13|Col14|Col15|Col16|Col17|Col18|Col19|Col20|Col21|Col22|Col23|Col24|Col25|Col26|Col27|Col28|Col29|Col30|Col31|Col32|Col33|Col34|Col35|Col36|Col37|Col38|Col39|Col40|Col41|Col42|Col43|Col44|Col45|Col46|Col47|Col48|Col49|Col50|Col51|Col52|Col53|Col54|Col55|Col56|Col57|Col58|Col59|Col60|Col61|Col62|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|.7<br>5<br>|.7<br>5<br>|.7<br>5<br>|.7<br>5<br>|.8<br>0<br><br>.2<br>0<br>%|.8<br>0<br><br>.2<br>0<br>%|.8<br>0<br><br>.2<br>0<br>%|.8<br>0<br><br>.2<br>0<br>%|.8<br>0<br><br>.2<br>0<br>%|.8<br>0<br><br>.2<br>0<br>%|.8<br>0<br><br>.2<br>0<br>%|0%<br>%|0%<br>%|0%<br>%|0%<br>%|0%<br>%|0%<br>%|0%<br>%|||||||||||||||||||||||||||||||||||||||||||||
|92<br>92.<br>91.|92<br>92.<br>91.|92<br>92.<br>91.|92<br>92.<br>91.|93<br>92.<br><br>93<br>92.<br>89.8|93<br>92.<br><br>93<br>92.<br>89.8|93<br>92.<br><br>93<br>92.<br>89.8|93<br>92.<br><br>93<br>92.<br>89.8|93<br>92.<br><br>93<br>92.<br>89.8|93<br>92.<br><br>93<br>92.<br>89.8|93<br>92.<br><br>93<br>92.<br>89.8|91.<br>90.6|91.<br>90.6|91.<br>90.6|91.<br>90.6|91.<br>90.6|91.<br>90.6|91.<br>90.6||||||||||||||%<br>%|%<br>%|%<br>%|%<br>%|%<br>%|%<br>%|%<br>%|%<br>%|%<br>%|%<br>%|%<br>%|%<br>%|%<br>%|%<br>%|||||||%<br><br>|%<br><br>|%<br><br>|%<br><br>|%<br><br>|%<br><br>|%<br><br>|%|%|%|%|
|92<br>92.<br>91.||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
|||||||||||||||%|%|%|%||||||||||||||67.7%<br>70.7<br>70.<br>%|67.7%<br>70.7<br>70.<br>%|67.7%<br>70.7<br>70.<br>%|67.7%<br>70.7<br>70.<br>%|67.7%<br>70.7<br>70.<br>%|67.7%<br>70.7<br>70.<br>%|67.7%<br>70.7<br>70.<br>%|.0%<br><br>68.3<br>68.9|.0%<br><br>68.3<br>68.9|.0%<br><br>68.3<br>68.9|.0%<br><br>68.3<br>68.9|.0%<br><br>68.3<br>68.9|.0%<br><br>68.3<br>68.9|.0%<br><br>68.3<br>68.9|||||||68.9<br>67.7%<br>69.4|68.9<br>67.7%<br>69.4|68.9<br>67.7%<br>69.4|68.9<br>67.7%<br>69.4|68.9<br>67.7%<br>69.4|68.9<br>67.7%<br>69.4|68.9<br>67.7%<br>69.4|68.0%<br>69.7|68.0%<br>69.7|68.0%<br>69.7|68.0%<br>69.7|
|||||||||||||||%|%|%|%||||||||||||||67.7%<br>70.7<br>70.<br>%|67.7%<br>70.7<br>70.<br>%|67.7%<br>70.7<br>70.<br>%|67.7%<br>70.7<br>70.<br>%||||||||||||||||||||||||||||
|||||||||||||||49.5<br>45.2%<br>45.8%|49.5<br>45.2%<br>45.8%|49.5<br>45.2%<br>45.8%|49.5<br>45.2%<br>45.8%|.6%<br>%<br><br><br>0.0%<br>0.2%|.6%<br>%<br><br><br>0.0%<br>0.2%|.6%<br>%<br><br><br>0.0%<br>0.2%|.6%<br>%<br><br><br>0.0%<br>0.2%|.6%<br>%<br><br><br>0.0%<br>0.2%|.6%<br>%<br><br><br>0.0%<br>0.2%|48.0%<br>45.5%<br><br>43.4%<br>|48.0%<br>45.5%<br><br>43.4%<br>|48.0%<br>45.5%<br><br>43.4%<br>|48.0%<br>45.5%<br><br>43.4%<br>|48.0%<br>45.5%<br><br>43.4%<br>|48.0%<br>45.5%<br><br>43.4%<br>|48.0%<br>45.5%<br><br>43.4%<br>|48.5<br>46.0%|48.5<br>46.0%|48.5<br>46.0%|48.5<br>46.0%|||||||54<br>44.2%<br>40.9%|54<br>44.2%<br>40.9%|54<br>44.2%<br>40.9%|54<br>44.2%<br>40.9%|44.0%<br>.5%<br><br>0.0%<br>42.4%<br>3%|44.0%<br>.5%<br><br>0.0%<br>42.4%<br>3%|44.0%<br>.5%<br><br>0.0%<br>42.4%<br>3%|44.0%<br>.5%<br><br>0.0%<br>42.4%<br>3%|44.0%<br>.5%<br><br>0.0%<br>42.4%<br>3%|44.0%<br>.5%<br><br>0.0%<br>42.4%<br>3%|.5%<br>.1%|.5%<br>.1%|.5%<br>.1%|.5%<br>.1%||||||||
|||||||||||||||49.5<br>45.2%<br>45.8%|49.5<br>45.2%<br>45.8%|49.5<br>45.2%<br>45.8%|49.5<br>45.2%<br>45.8%|.6%<br>%<br><br><br>0.0%<br>0.2%|.6%<br>%<br><br><br>0.0%<br>0.2%|.6%<br>%<br><br><br>0.0%<br>0.2%|.6%<br>%<br><br><br>0.0%<br>0.2%|.6%<br>%<br><br><br>0.0%<br>0.2%|.6%<br>%<br><br><br>0.0%<br>0.2%|48.0%<br>45.5%<br><br>43.4%<br>|48.0%<br>45.5%<br><br>43.4%<br>|48.0%<br>45.5%<br><br>43.4%<br>|48.0%<br>45.5%<br><br>43.4%<br>|48.0%<br>45.5%<br><br>43.4%<br>|48.0%<br>45.5%<br><br>43.4%<br>|48.0%<br>45.5%<br><br>43.4%<br>|48.5<br>46.0%|48.5<br>46.0%|48.5<br>46.0%|48.5<br>46.0%|||||||54<br>44.2%<br>40.9%|||||||||||||||||||||
|||||||||||||||||||37<br>33.2<br>32.1<br>4<br>4|37<br>33.2<br>32.1<br>4<br>4|37<br>33.2<br>32.1<br>4<br>4|37<br>33.2<br>32.1<br>4<br>4|37<br>33.2<br>32.1<br>4<br>4|37<br>33.2<br>32.1<br>4<br>4|30.0%<br>31.7%|30.0%<br>31.7%|30.0%<br>31.7%|30.0%<br>31.7%|||||||||||||||||||36.|36.||37<br>|37<br>|37<br>37|37<br>37|37<br>37|37<br>37||||||||
|||||||||||||||||||37<br>33.2<br>32.1<br>4<br>4|37<br>33.2<br>32.1<br>4<br>4|37<br>33.2<br>32.1<br>4<br>4||||||||||||||||||||||||||||||||||||||||||
|||||||||||||||||||37<br>33.2<br>32.1<br>4<br>4|37<br>33.2<br>32.1<br>4<br>4|37<br>33.2<br>32.1<br>4<br>4||||||||||||||||||||||||||||||||||||||||||
|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||

GSM8K MATH500 AIME24 AIME25 GPQA-D ARC-C BFCL-V1 BFCL-V2 META-TOOL


Phi-4-Reasoning


100


80


60


40


20


0

|7% 1% 7%|Col2|Col3|Col4|7% 7% 7%|Col6|Col7|Col8|Col9|Col10|Col11|Col12|Col13|Col14|Col15|Col16|Col17|Col18|Col19|Col20|Col21|Col22|Col23|Col24|Col25|Col26|Col27|Col28|Col29|Col30|Col31|Col32|Col33|Col34|Col35|Col36|Col37|Col38|Col39|Col40|Col41|Col42|Col43|Col44|Col45|Col46|Col47|Col48|Col49|Col50|Col51|Col52|Col53|Col54|Col55|Col56|Col57|Col58|Col59|Col60|Col61|Col62|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|91.7<br>91.1<br>91.|91.7<br>91.1<br>91.|91.7<br>91.1<br>91.|91.7<br>91.1<br>91.|%<br>%<br><br><br>91.7<br>91.7|%<br>%<br><br><br>91.7<br>91.7|%<br>%<br><br><br>91.7<br>91.7|%<br>%<br><br><br>91.7<br>91.7|%<br>%<br><br><br>91.7<br>91.7|%<br>%<br><br><br>91.7<br>91.7|%<br>%<br><br><br>91.7<br>91.7|3%<br><br><br>%<br>%|3%<br><br><br>%<br>%|3%<br><br><br>%<br>%|3%<br><br><br>%<br>%|3%<br><br><br>%<br>%|3%<br><br><br>%<br>%|3%<br><br><br>%<br>%|%<br>3%|%<br>3%|%<br>3%|%<br>3%|%<br>3%|%<br>3%||||||||80.0%<br>80.2%<br><br>8.8%|80.0%<br>80.2%<br><br>8.8%|80.0%<br>80.2%<br><br>8.8%|80.0%<br>80.2%<br><br>8.8%|80.0%<br>80.2%<br><br>8.8%|80.0%<br>80.2%<br><br>8.8%|80.0%<br>80.2%<br><br>8.8%|83.6%<br>83.7%<br><br>82.8%<br>81.3%<br>80.0%|83.6%<br>83.7%<br><br>82.8%<br>81.3%<br>80.0%|83.6%<br>83.7%<br><br>82.8%<br>81.3%<br>80.0%|83.6%<br>83.7%<br><br>82.8%<br>81.3%<br>80.0%|83.6%<br>83.7%<br><br>82.8%<br>81.3%<br>80.0%|83.6%<br>83.7%<br><br>82.8%<br>81.3%<br>80.0%|83.6%<br>83.7%<br><br>82.8%<br>81.3%<br>80.0%|%<br>9%<br><br>%<br>84.0%<br>82.4%|%<br>9%<br><br>%<br>84.0%<br>82.4%|%<br>9%<br><br>%<br>84.0%<br>82.4%|%<br>9%<br><br>%<br>84.0%<br>82.4%|%<br>9%<br><br>%<br>84.0%<br>82.4%|%<br>9%<br><br>%<br>84.0%<br>82.4%|82.0%<br>82.2%<br><br>81.5%<br>%<br>%|82.0%<br>82.2%<br><br>81.5%<br>%<br>%|82.0%<br>82.2%<br><br>81.5%<br>%<br>%|82.0%<br>82.2%<br><br>81.5%<br>%<br>%|82.0%<br>82.2%<br><br>81.5%<br>%<br>%|82.0%<br>82.2%<br><br>81.5%<br>%<br>%|82.0%<br>82.2%<br><br>81.5%<br>%<br>%|81.7%<br>81.6%|81.7%<br>81.6%|81.7%<br>81.6%|81.7%<br>81.6%|
|91.7<br>91.1<br>91.||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
||||||||71.1<br>71.4<br>69.8|71.1<br>71.4<br>69.8|71.1<br>71.4<br>69.8|71.1<br>71.4<br>69.8|67.5%<br>73.<br><br>69.2%<br>71.1<br>70.4|67.5%<br>73.<br><br>69.2%<br>71.1<br>70.4|67.5%<br>73.<br><br>69.2%<br>71.1<br>70.4|67.5%<br>73.<br><br>69.2%<br>71.1<br>70.4|67.5%<br>73.<br><br>69.2%<br>71.1<br>70.4|67.5%<br>73.<br><br>69.2%<br>71.1<br>70.4|67.5%<br>73.<br><br>69.2%<br>71.1<br>70.4|63.7%<br>6.7%<br><br>7.5%<br>70.4<br>73.|63.7%<br>6.7%<br><br>7.5%<br>70.4<br>73.|63.7%<br>6.7%<br><br>7.5%<br>70.4<br>73.|63.7%<br>6.7%<br><br>7.5%<br>70.4<br>73.|63.7%<br>6.7%<br><br>7.5%<br>70.4<br>73.|63.7%<br>6.7%<br><br>7.5%<br>70.4<br>73.|62.6%<br>60.6%<br><br>69.7<br>60.0%<br>3%|62.6%<br>60.6%<br><br>69.7<br>60.0%<br>3%|62.6%<br>60.6%<br><br>69.7<br>60.0%<br>3%|62.6%<br>60.6%<br><br>69.7<br>60.0%<br>3%|62.6%<br>60.6%<br><br>69.7<br>60.0%<br>3%|62.6%<br>60.6%<br><br>69.7<br>60.0%<br>3%|62.6%<br>60.6%<br><br>69.7<br>60.0%<br>3%|66.2%<br>67.7%|66.2%<br>67.7%|66.2%<br>67.7%|66.2%<br>67.7%|||||||||||||72.1<br>72.<br>72.|72.1<br>72.<br>72.|72.1<br>72.<br>72.|72.1<br>72.<br>72.|71.9<br>71.7|71.9<br>71.7|71.9<br>71.7|71.9<br>71.7||||||||
||||||||71.1<br>71.4<br>69.8|||||||||||||||||||||||||||||||||||||||||||||||||||||||
|||||||||||||||||||||||5<br>|5<br>|||53.|53.|||||||||||||||||||||||||||||||||||
|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||

GSM8K MATH500 AIME24 AIME25 GPQA-D ARC-C BFCL-V1 BFCL-V2 META-TOOL


Baseline t=0.1 t=0.25 t=1.0 t=2.5


Figure 16: Accuracy comparison across various threshold values _τ_ for Qwen3-32B, DeepSeek-R1-7B, and Phi-4Reasoning.


Qwen3-4B-Thinking-2507




|60|57 20|2|
|---|---|---|
|~~(83.~~<br>1<br>|~~6%)~~<br><br>~~(2.~~<br>5<br><br>7<br>|~~%)~~<br>8<br>|
|~~(2.~~|~~%)~~<br><br>~~(10.~~|~~9%)~~|


|60|84 16|9|
|---|---|---|
|~~(84.~~<br>1<br>|~~0%)~~<br><br>~~(2.~~<br>9<br><br>8<br>|~~%)~~<br>0<br>|
|~~(2.~~|~~%)~~<br><br>~~(11.~~|~~2%)~~|


|59|61 23|9|
|---|---|---|
|~~(82.~~<br>2<br>|~~3%)~~<br><br>~~(3.~~<br>7<br><br>8<br>|~~%)~~<br>5<br>|
|~~(3.~~|~~%)~~<br><br>~~(11.~~|~~1%)~~|



Baseline

Qwen3-32B

|59|00 29|0|
|---|---|---|
|~~(81.~~<br>2<br>|~~5%)~~<br><br>~~(4.~~<br>2<br><br>7<br>|~~%)~~<br>0<br>|
|~~(4.~~|~~%)~~<br><br>~~(10.~~|~~5%)~~|



Baseline







Qwen3-4B


Baseline







Qwen3-14B


Baseline






|39|60 67|6|
|---|---|---|
|~~(54.~~<br>8<br>|~~7%)~~<br><br>~~(9.~~<br>6<br><br>17<br>|~~%)~~<br>10<br>|
|~~(12.~~|~~4%)~~<br><br>~~(23.~~|~~6%)~~|


|54|17 41|3|
|---|---|---|
|~~(74.~~<br>4<br>|~~8%)~~<br><br>~~(5.~~<br>6<br><br>10<br>|~~%)~~<br>06<br>|
|~~(5.~~|~~%)~~<br><br>~~(13.~~|~~9%)~~|



Baseline



DeepSeek-R1-Distill-Qwen-7B



phi-4-reasoning









Baseline



Figure 17: Transition matrices showing prediction transitions before and after applying THINKBRAKE for all
models, aggregated across all benchmarks. High diagonal values indicate preserved accuracy.


