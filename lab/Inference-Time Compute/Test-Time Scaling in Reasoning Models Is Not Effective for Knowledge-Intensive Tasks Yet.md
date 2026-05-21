## **Test-Time Scaling in Reasoning Models Is Not** **Effective for Knowledge-Intensive Tasks Yet**

**James Xu Zhao** _[∗]_ **Bryan Hooi** **See-Kiong Ng**

National University of Singapore


**Abstract**


Test-time scaling increases inference-time computation by allowing models to
generate long reasoning chains, and has improved performance across many domains. However, in this work, we show that this approach is not yet effective for
knowledge-intensive tasks. We evaluate 14 reasoning models on two knowledgeintensive benchmarks and find that increasing test-time computation does not
consistently improve accuracy and often increases hallucinations. Further analysis
shows that changes in hallucination rates under increased test-time computation
are largely driven by models’ willingness to answer. We also observe that extended
reasoning can induce confirmation bias, leading to overconfident hallucinations.
Finally, we provide an information-theoretic account: compute-only test-time scaling is a post-processing of a fixed trained model and therefore cannot increase
information about the ground-truth answer beyond what is already encoded in the
model, explaining its limited gains on knowledge-intensive tasks. Code and data
are available at `[https://github.com/XuZhao0/tts-knowledge](https://github.com/XuZhao0/tts-knowledge)` .


**1** **Introduction**


Recent reasoning models, such as GPT-5 [25], Gemini 2.5 [12], and Qwen3 [32], have demonstrated
impressive performance on many challenging tasks [8, 16, 29, 30, 33, 42]. A key technique behind these improvements is test-time scaling, where models generate long chain-of-thought (CoT)
reasoning traces before producing an answer [24].


Despite these advances, frontier models still suffer from hallucinations, responses that contradict
world knowledge [2, 15, 35]. This remains a fundamental challenge, especially in knowledgeintensive tasks that require models to ensure factual accuracy and minimize hallucinations [19, 37].
Given that test-time scaling has shown promise across many domains, a natural question arises: _**Is**_
_**test-time scaling effective for knowledge-intensive tasks?**_


To answer this question, we conduct a comprehensive study of test-time scaling on two knowledgeintensive tasks. We evaluate 14 reasoning models by increasing their test-time computation (Section 3).
Our results, summarized in Table 1, challenge the common assumption that thinking more leads
to better performance. Across models and tasks, increasing thinking time does not consistently
improve accuracy, with Gemini 2.5 Flash and 2.5 Pro being exceptions. Moreover, thinking more
does not reduce hallucinations for most models. Only Grok-3 mini and R1-Distill-Qwen-14B show
reductions on both tasks. In contrast, models such as GPT-5 mini and Gemini 2.5 Flash exhibit more
hallucinations with extended thinking.


To understand hallucination changes with increased test-time computation, we analyze how model
behavior shifts across different thinking levels (Section 4). We find that these changes are largely
driven by the model’s willingness to answer. Specifically, reduced hallucinations are primarily due to


_∗_ Correspondence to: James Xu Zhao (xu.zhao@u.nus.edu)


Preprint.


Table 1: Summary of model behavior with test-time scaling. Increasing test-time computation does
not consistently improve accuracy or reduce hallucinations for most models. It can even increase
hallucinations for several models. For ACCURACY, _↑_ denotes consistent improvement with >2%
accuracy gains across consecutive reasoning levels, while _∼_ indicates no consistent trend. For
HALLUCINATION, _↓_ denotes consistent reduction with >2% hallucination decrease, _↑_ indicates
degradation with >2% hallucination increase, and _∼_ refects inconsistent or fuctuating patterns.


**Metric** **GPT-5** **GPT-5** **o3-mini** **o4-mini** **gpt-oss-** **Grok-3** **Gemini 2.5**
**mini** **20b** **mini** **Flash**


**Metric** **Gemini 2.5** **Claude** **R1-Distill-** **R1-Distill-** **R1-Distill-** **Qwen3-8B** **Qwen3-**
**Pro** **Sonnet 4** **Qwen-7B** **Qwen-14B** **Llama-8B** **14B**


simple abstention, rather than improved factual accuracy. Conversely, when hallucinations increase,
it is often because extended reasoning leads the model to attempt previously unanswered questions.
Moreover, we observe that extended reasoning can induce _confirmation bias_ [23], where the model
fabricates details to support its prior belief, resulting in overconfident hallucinations.


In parallel, we develop an information-theoretic account of these observations (Section 5). We model
test-time scaling as a compute-only procedure that interacts with a fixed trained model and outputs
an answer as a function of the resulting interaction transcript. By the data-processing inequality,
additional test-time computation cannot create new information about the ground-truth answer beyond
what is already encoded in the trained model. To connect this limitation to knowledge-intensive
settings, we adopt an _arbitrary facts_ abstraction for long-tail factual questions whose answers are
not inferable from prompt structure and must be learned from training evidence. In this informationlimited regime, scaling computation alone is not expected to yield consistent gains, matching our
empirical findings.


To summarize, while test-time scaling in reasoning models has led to strong performance in many
domains, our experimental results and theoretical analysis show that it is _not_ yet effective for
knowledge-intensive tasks.


**2** **Related Work**


**2.1** **Test-Time Scaling**


Test-time scaling has emerged as a promising strategy for enhancing the capabilities of large language models. It is typically categorized into two main paradigms [43]: (1) the parallel approach,
which samples multiple outputs independently and aggregates them [5, 31]; and (2) the sequential
approach, where the model generates long chain-of-thought (CoT) reasoning traces before producing
an answer [22, 24, 36]. In this work, we focus on the sequential paradigm, which has become the
dominant test-time scaling method for improving model performance [2] . It is widely adopted in
frontier reasoning models [1, 12, 13, 25, 32, 40], and has demonstrated strong performance across a
range of challenging tasks [16, 29, 30, 33].


However, recent studies suggest that in some tasks, increasing test-time computation does not always
improve performance. Gema et al. [11] find that longer reasoning may reinforce problematic patterns
rather than improve accuracy. Liu et al. [21] observe that extended reasoning often amplifies visual
hallucinations in multimodal large language models. Cuadron et al. [7] reveal that excessive internal
reasoning reduces effectiveness in agentic tasks. Some works report that thinking can negatively
affect models’ instruction-following capability [10, 20]. Our study shows that increasing test-time
computation is not yet effective for knowledge-intensive tasks.


2Results and analysis for the parallel approach are provided in Appendix B.


2


**2.2** **Factuality Hallucinations in LLMs**


Factuality hallucinations, which refer to content that contradicts world knowledge, have been a
long-standing issue in large language models [15, 17, 44]. These hallucinations reflect the models’
limitations in absorbing knowledge and their inability to recognize knowledge boundaries [3]. Prior
studies reveal that longer responses often lead to lower factual precision [38, 45], while our work
focuses on the effect of reasoning length on hallucinations. Yao et al. [41] investigate whether
reasoning models are more prone to hallucinate, but they do not explore the effect of test-time scaling.
OpenAI [28] observe that Claude models have extremely low hallucination rates primarily because
they frequently refuse to answer. Kalai et al. [18] argue that LLMs hallucinate because current training
and evaluation paradigms favor guessing over acknowledging uncertainty. We provide empirical
evidence for this in the test-time scaling settings. We further provide an information-theoretic analysis
that formalizes an information ceiling for test-time scaling. To the best of our knowledge, this is the
first study to examine how increased test-time computation affects factuality hallucinations.


**3** **How Does Test-Time Scaling Affect Accuracy and Hallucination Ratio?**


To understand the impact of test-time scaling on knowledge-intensive tasks, we evaluate how increasing test-time computation affects accuracy and hallucination ratio across 14 reasoning models on two
benchmarks.


**3.1** **Experimental Setup**


**Benchmarks.** We evaluate on two knowledge-intensive benchmarks that involve answering shortform factual questions.


 - **SimpleQA** [37]: A benchmark of short, fact-seeking questions curated by human annotators. A
question example is: _“Who received the IEEE Frank Rosenblatt Award in 2010?”_ . We randomly
sample 800 questions for evaluation.

 - **FRAMES** [19]: Questions in FRAMES tend to be more complex and often require multi-hop
reasoning. An example is: _“What Pink Floyd album came out the year Pablo Picasso died?”_ We
use all 824 questions for evaluation.


**Models and Test-Time Scaling Settings.** We evaluate 14 large reasoning models and group them
into three categories, based on how they support test-time scaling. Models are not allowed to access
any external knowledge sources.


 - **Reasoning effort** : Models such as GPT-5 [25], o3-mini, o4-mini [27], gpt-oss-20b [26], Grok-3
mini [39] accept a `reasoning` `effort` parameter that adjusts the time of thinking.

 - **Thinking budget** : Models like Gemini 2.5 [12], Claude Sonnet 4 [1] provide a `thinking` `budget`
parameter that guides the model on the number of thinking tokens to use. A larger number
encourages the model to think for a longer time.

 - **Budget** **forcing** : For DeepSeek-R1-Distill models [13] and Qwen3 models [32], we adopt the
budget forcing method [22], which extends the model’s thinking process by appending `“Wait”`
when the model attempts to terminate its reasoning.


**Prompts.** We use a consistent prompting format for all models, except GPT-5 mini and Claude
Sonnet 4, across both benchmarks: _Give me the answer to the following question only when you are_
_sure of it._ _Otherwise, say ‘I don’t know’._ _Put your answer on its own line after ‘Answer:’._ [3]


**Evaluation and Metrics.** Following Wei et al. [37], we prompt ChatGPT ( `gpt-4o-mini` ) as a
grader to evaluate model responses. For each question, the grader is provided with both the model’s
predicted answer and the reference answer, and assigns one of three labels: _“correct”_, _“incorrect”_, or
_“not attempted”_ . Wei et al. [37] show that this automatic evaluation method closely aligns with human


3For GPT-5 mini and Claude Sonnet 4, this prompt causes the model to abstain on over 80% of questions.
Therefore, we do not explicitly instruct them to abstain when uncertain. See Appendix A.3 for details.


3


Figure 1: Accuracy with increased test-time computation across 14 reasoning models on SimpleQA
and FRAMES. For most models, extended test-time reasoning does not consistently improve accuracy.
While some models, such as GPT-5, show initial accuracy gains, further increasing reasoning length
brings little or no additional improvement. In many cases, such as Claude Sonnet 4 and Qwen3
models, accuracy plateaus or fluctuates with no clear upward trend.


judgments. [4] We report two metrics: (1) _Accuracy_, the percentage of all questions that were answered
correctly. (2) _Hallucination ratio_, the percentage of all questions that were answered incorrectly.
More details of our experimental setup are provided in Appendix A.


**3.2** **Effect of Test-Time Scaling on Accuracy**


**Thinking** **more** **does** **not** **consistently** **improve** **the** **accuracy** **for** **most** **models.** As shown in
Figure 1, increasing the reasoning length results in minimal or no accuracy gains across most models
and both benchmarks. Higher `reasoning` `effort` leads to much longer thinking length, but does
not consistently improve accuracy. For example, o4-mini exhibits more than 8 times increase in
reasoning tokens, but the accuracy remains almost unchanged on both tasks. Similar patterns are
observed in o3-mini and Grok-3 mini. On FRAMES, GPT-5, GPT-5 mini, and gpt-oss-20b show a
3-5% accuracy increase when increasing effort from _‘low’_ to _‘medium’_, but no further improvement
at _‘high’_ effort, despite the average reasoning tokens more than doubling. Increasing the `thinking`
`budget` of Claude Sonnet 4 results in minimal accuracy gains on both benchmarks, less than 2%
improvement, even as the average thinking length nearly triples. Among models using `budget`
`forcing`, such as Qwen3-14B, accuracy fluctuates as the thinking length increases. In some cases,
accuracy even decreases, as observed with R1-Distill-Qwen-7B on FRAMES.


**For Gemini 2.5, low thinking budget limits accuracy due to incomplete reasoning.** We evaluate
Gemini 2.5 Flash and 2.5 Pro with `thinking` `budget` of 256, 512, 1024 and 2048 tokens. On
SimpleQA, accuracy improves by over 6% and 8% for Gemini 2.5 Flash and 2.5 Pro, respectively, as
the budget increases from 256 to 1024 tokens. However, increasing the budget further to 2048 tokens
does not yield more improvement. On FRAMES, Gemini 2.5 Flash and 2.5 Pro achieve 18% and 28%
accuracy gains, as reasoning length increases. These improvements arise because Gemini 2.5 is often
unable to complete its reasoning under low thinking budgets, which limits its accuracy. This issue is


4We randomly sampled 300 cases and compared the automatic evaluation results with human annotations.
We found only 2 disagreements.


4


Figure 2: Hallucination ratio with increased test-time reasoning across 14 models on SimpleQA and
FRAMES. For most models, longer reasoning does not reduce hallucinations. In many cases, such as
GPT-5 mini and gpt-oss-20b, hallucination increases with longer thinking length. Only Grok-3 mini
and DS-R1-Distill-Qwen-14B exhibit reduced hallucinations with extended reasoning on both tasks.


particularly evident on FRAMES, which requires more reasoning steps. As a result, larger thinking
budgets lead to more substantial accuracy gains on FRAMES. We provide analysis in Appendix E.


**3.3** **Effect of Test-Time Scaling on Hallucination Ratio**


**Thinking more does not reduce hallucinations and may even increase them.** In Figure 2, for
most models on two benchmarks, increasing test-time computation fails to reduce hallucinations
and can make them worse. In OpenAI models, higher `reasoning` `effort` often leads to more
hallucinations. For example, on SimpleQA, the hallucination ratio of GPT-5-mini increases by
over 15% as reasoning length increases from 300 to 3300 tokens. Similarly, GPT-5, o3-mini, and
gpt-oss-20b show increases of 9%, 12%, and 25%, respectively, as their thinking length scales by
over 8 times. On FRAMES, the same trend holds: hallucination ratio increases with longer reasoning
in GPT-5-mini, o3-mini, and gpt-oss-20b. Models with `thinking` `budget` settings exhibit similar
behavior. For Gemini 2.5 Flash, hallucination ratio increases by 10% on SimpleQA and 9% on
FRAMES. Claude Sonnet 4 shows no reduction in hallucinations despite longer reasoning. Among
models using `budget` `forcing`, none except for DS-R1-Distill-Qwen-14B benefits from longer
thinking in terms of reducing hallucinations. In some cases, the hallucination ratio even increases, as
seen in DS-R1-Distill-Qwen-7B.


**For Grok-3 mini and DS-R1-Distill-Qwen-14B, thinking more leads to fewer hallucinations on**
**both benchmarks.** Increasing the `reasoning` `effort` reduces the hallucination ratio of Grok3 mini by 4.4% on SimpleQA and 1.7% on FRAMES. However, considering that the thinking
length nearly doubles on FRAMES, the reduction is relatively small. DS-R1-Distill-Qwen-14B
shows a more noticeable improvement. On SimpleQA, hallucinations drop by over 12% as the
average reasoning length increases from 530 to 1580 tokens. On FRAMES, the hallucination ratio
decreases by 8% as reasoning length increases from 850 to 1900 tokens. Despite these reductions,
DS-R1-Distill-Qwen-14B still has a higher hallucination ratio than other open-source models, such
as DS-R1-Distill-Llama-8B and Qwen3-8B.


5


SimpleQA


FRAMES


SimpleQA


FRAMES


SimpleQA


FRAMES



**Fewer Hallucinations with More Thinking**










|88.8% 1|Col2|1.2%|
|---|---|---|
||||
|58.9%|41.1%|41.1%|







**More Hallucinations with More Thinking**








|89.6%|10.4|
|---|---|
|||
|76.7%<br>|23.3|




```
o3-mini

```












Non-hallucinating responses

(Correct or Not attempted)

|76.5%|Col2|23.5%|
|---|---|---|
||||
|83.1%|83.1%|16.9|
|83.1%|||



Figure 3: Changes in hallucination behavior with more thinking. We compare model responses at
different reasoning levels, focusing on cases where one response is a hallucination and the other is
not. Results show that reduced hallucinations result from abstention, while more hallucinations stem
from the model attempting previously unanswered questions.


**4** **Why Does Thinking More Sometimes Lead to Fewer or More**
**Hallucinations?**


As discussed in Section 3.3, thinking more sometimes leads to fewer hallucinations, and sometimes
more. In this section, we examine the causes of these changes. We first compare model behavior
across different thinking levels, then conduct quantitative and qualitative analyses to understand how
extended reasoning affects model behavior.


**4.1** **Experimental Setup**


We compare model behavior across different levels of test-time reasoning. As illustrated in Figure 3,
for each question, we obtain two responses from the same model under different reasoning levels.
We focus on cases where the hallucination outcome changes between the two settings, that is, one
response is a hallucination while the other is not. We then examine the non-hallucinating responses
and compute the ratio of _“correct”_ versus _“not attempted”_ . This helps us understand whether reduced
hallucinations are due to improved knowledge retrieval or simply abstention, and conversely, whether
increased hallucinations result from risky attempts at answering.


As discussed in Section 3.3, Grok-3 mini and DS-R1-Distill-Qwen-14B show reduced hallucinations
with longer thinking on both benchmarks. [5] For these models, we analyze cases where the model
hallucinates at a lower reasoning level but does not hallucinate at a higher level. In contrast, GPT-5
mini, o3-mini, gpt-oss-20b, and Gemini 2.5 Flash exhibit increased hallucinations. For these models,
we examine cases where the model does not hallucinate at a lower reasoning level but hallucinates at
a higher level.


**4.2** **Hallucination Changes Are Driven by the Model’s Willingness to Answer**


**Fewer hallucinations are mostly due to abstention.** As shown in Figure 3, for Grok-3 mini and
DS-R1-Distill-Qwen-14B on both benchmarks, most cases of reduced hallucinations result from


5A special case is Gemini 2.5 Pro on FRAMES, which exhibits a reduction in hallucinations. We provide
analysis in Appendix E.2.


6


Figure 4: Thinking more leads to more hallucinations for gpt-oss-20b. In this example, it abstains
under low reasoning effort, but produces overconfident hallucinations with confirmation bias at high
effort. See Appendix F for more examples and full reasoning traces.


the model choosing not to answer, rather than providing a correct answer. On SimpleQA, when
increasing the reasoning effort of Grok-3 mini from _‘low’_ to _‘high’_, 93.1% of the responses that are
not hallucinating at higher effort are labeled as _‘not attempted’_ . Similarly, for DS-R1-Distill-Qwen14B, the _‘not attempted’_ ratio in these cases is 88.8%. These results suggest that in most cases where
longer reasoning reduces hallucinations, the improvement is not due to better factual recall, but rather
because the model chooses to abstain after thinking more.


**More** **hallucinations** **mostly** **come** **from** **previously** **unattempted** **questions.** In Figure 3, the
increase in hallucinations at higher reasoning levels is largely due to the model attempting questions
it had previously abstained from. For example, on SimpleQA, when increasing the reasoning effort
of gpt-oss-20b from _‘low’_ to _‘high’_, 95.0% of new hallucinations come from questions that were
_‘not attempted’_ at the lower effort level. A similar trend is seen with Gemini 2.5 Flash: 76.5% of
hallucinations under a higher thinking budget correspond to questions the model had abstained from
at the lower budget. This pattern also appears on FRAMES: for all four models, over 70% of new
hallucinations arise from the questions the model had not attempted before. These results suggest
that longer thinking time encourages models to answer more questions. However, for many of these
newly attempted questions, the answers are incorrect, resulting in a higher hallucination ratio.


**4.3** **Analysis on gpt-oss-20b:** **Thinking More Leads to Confirmation Bias**


To better understand why longer thinking leads to more attempted answers, and thus more hallucinations, we conduct a case study and quantitative analysis of the reasoning traces from gpt-oss-20b.


**Longer reasoning leads to overconfident hallucinations.** In Figure 4, gpt-oss-20b initially engages
with the question at low reasoning effort. It explores a few possibilities but finally abstains due to
uncertainty. With higher effort, the model continues searching its memory. It begins by expressing
uncertainty, but as the reasoning progresses, it gradually becomes more confident. The thought shifts
from tentative claims like _“maybe in 2005”_ to more confident statements such as _“I am fairly sure it’s_
_2005”_ . Despite the increased confidence, the final answer remains incorrect. This example suggests
that extended reasoning can inflate the model’s confidence, leading to overconfident hallucinations
where the model chooses to answer despite still lacking accurate information.


**Longer reasoning induces confirmation bias, resulting in overconfident hallucinations.** We
observe signs of _confirmation bias_ [23], where the model recalls or even makes up information to
reinforce its initial belief. In Figure 4, after tentatively proposing an answer, _e.g.,_ _“He_ _has_ _been_
_recognized by AAAI maybe in 2005”_, gpt-oss-20b attempts to justify this hypothesis by generating
fabricated supporting details, such as _“We can check his CV..._ _I think that is correct”_ and _“I know_
_of the AAAI Fellows list on the AAAI website._ _For 2005, the list includes John Mylopoulos indeed”_ .


7


Figure 5: Visualization of incorrect final answer positions in the reasoning traces of gpt-oss-20b
across different thinking levels. Red markers indicate the normalized token positions of the final
incorrect answer within the trace. Each subplot presents 10 randomly sampled cases. As test-time
computation increases, hallucinated answers appear more frequently in the reasoning traces.


These fabricated details build upon one another, reinforcing the model’s confidence in its incorrect
belief and ultimately leading to overconfident hallucinations.


**Hallucinated answers appear earlier and more frequently with extended reasoning.** Inspired
by Chen et al. [6], we examine when the incorrect final answer appears in the reasoning trace of
gpt-oss-20b. As test-time computation increases, the hallucinated answers tend to appear earlier
during reasoning. Specifically, on SimpleQA, the normalized position of the first appearance drops
from 45.7% at low effort to 29.9% at medium effort, and further to 17.2% at high effort. Similarly,
on FRAMES, the position decreases from 68.2% to 26.3% at high effort. Figure 5 visualizes how
these incorrect answers appear repeatedly throughout the reasoning trace. The frequency of such
recurrences increases with longer thinking. These recurrences are often accompanied by fabricated
details. This further supports our argument that extended reasoning induces confirmation bias.


**5** **Information-Theoretic Limits of Test-Time Scaling on Knowledge-Intensive**
**Tasks**


In the previous sections, our results show that increasing test-time computation is not effective
for knowledge-intensive tasks. We now provide a theoretical account of this phenomenon. We
formalize test-time scaling as a compute-only interaction with a fixed trained model and derive an
information-theoretic limitation based on mutual information and the data-processing inequality.


**5.1** **Arbitrary Facts as an Abstraction of Long-Tail Knowledge**


We consider a family of “knowledge” problems where each question requires recalling a fact that is not
inferable from general patterns ( _e.g.,_ a specific person’s birthday, a rare association). Following Kalai
et al. [18], we model such settings as _arbitrary facts_ :


**Definition 1** (Arbitrary Facts) **.** Let _c ∈C_ denote a prompt. Each prompt has a finite candidate answer
set _Rc_ and a correct answer _Ac_ _∈_ _Rc_ . For each prompt _c_, _Ac_ is drawn uniformly from _Rc_, and the
collection _{Ac}c∈C_ is independent across prompts:


1
Pr[ _Ac_ = _r_ _| c_ ] = _∀r_ _∈_ _Rc,_ _{Ac}c∈C_
_|Rc|_


8


This formalizes a worst-case proxy for the portion of knowledge benchmarks dominated by idiosyncratic, long-tail facts, where without prompt-specific evidence, the correct answer is statistically
indistinguishable from other candidates. Appendix G discusses relaxations of this definition and how
it modifies the resulting bounds.


**5.2** **Compute-Only Test-Time Scaling as Oracle Post-Processing**


We model compute-only test-time scaling as any algorithm that can interact with a fixed trained
model _p_ ˆ, without accessing any external information sources.

**Definition 2** (Compute-only TTS) **.** A compute only test-time scaling method with budget _k_ is any
randomized interactive algorithm which, given a prompt _c_ :


1. selects query strings _q_ 1 _, . . ., qk_ sequentially, where each _qt_ may depend on _c_ and previous model
outputs,
2. receives responses _rt_ _∼_ _p_ ˆ( _· | qt_ ),
3. outputs a final response _R_ [ˆ] = _g_ ( _c, Tk_ ) as a function of the transcript _Tk_ := _{_ ( _qt, rt_ ) _}_ _[k]_ _t_ =1 [.]


This subsumes common test-time scaling strategies (i) sequential sampling approaches, such as
chain-of-thought, and (ii) parallel sampling approaches, such as self-consistency.


**5.3** **An Information-Theoretic Limitation for Compute-Only TTS**


Let _A_ := _Ac_ denote the latent correct answer for prompt _c_ . Conditioning on _c_, a compute-only TTS
method interacts with the fixed model _p_ ˆ to produce a transcript _Tk_, and outputs _R_ [ˆ] as a function
of ( _c, Tk_ ). Under this interaction model, the transcript is generated solely from _p_ ˆ, and _R_ [ˆ] is a
post-processing of _Tk_ . Formally, this implies the conditional Markov structure

_A_ _−→_ _p_ ˆ _−→_ _Tk_ _−→_ _R,_ [ˆ]


with a proof in Appendix H.

**Theorem 1** (Data-processing limitation of compute-only TTS) **.** _For any compute-only TTS method,_


_I_ ( _A_ ; _R_ [ˆ] _| c_ ) _≤_ _I_ ( _A_ ; _Tk_ _| c_ ) _≤_ _I_ ( _A_ ; ˆ _p | c_ ) _._


This formalizes that compute-only test-time scaling cannot create information about the latent truth
beyond what is already present in the trained model. Therefore, if a class of prompts is informationlimited in the sense that _I_ ( _A_ ; ˆ _p_ _|_ _c_ ) is small, then no compute-only TTS procedure can make
_I_ ( _A_ ; _R_ [ˆ] _| c_ ) large. In other words, the regime is information-limited, not compute-limited.


A standard consequence converts the mutual-information ceiling into an accuracy lower bound when
the answer space is large.

**Corollary 1** (Accuracy bound via Fano’s inequality) **.** _Assume A is uniform over Rc given c, and let_
_m_ := _|Rc|._ _For any compute-only TTS output_ _R_ [ˆ] _,_

Pr[ _R_ [ˆ] _̸_ = _A | c_ ] _≥_ 1 _−_ _[I]_ [(] _[A]_ [; ˆ] _[p][ |][ c]_ [) + log 2] _._

log _m_


Corollary 1 indicates that when _I_ ( _A_ ; ˆ _p | c_ ) _≈_ 0 ( _e.g.,_ prompts whose answers are effectively unseen
or rare), the error probability must be large and the model’s information about _A_ is small.
_Remark_ 1 _._ Under the Arbitrary Facts abstraction, answers are independent across prompts, so training
on other prompts cannot convey information about _Ac_ beyond whether the specific fact for _c_ was
observed during training. In particular, if the training data contains no information about the fact for
_c_, then _I_ ( _Ac_ ; ˆ _p | c_ ) = 0, and Corollary 1 implies an unavoidable error rate close to random guessing
when _|Rc|_ is large.


**Discussion.** Our theory formalizes that compute-only TTS is fundamentally limited in settings like
_Arbitrary Facts_, where facts contain no information about one another. However, we do not claim that
test-time scaling can never help: in settings where the model contains substantial signal about _A_ but
baseline decoding fails to extract it reliably, _i.e.,_ a compute-limited regime, test-time scaling can still
improve performance. We provide more discussions in Appendix G and full proofs in Appendix H.


9


**6** **Conclusion**


In this work, we present a comprehensive study of test-time scaling on knowledge-intensive tasks,
evaluating 14 large reasoning models across two benchmarks. We find that increasing test-time
computation does not consistently improve factual accuracy and, in many cases, leads to more
hallucinations. We further show that hallucination changes with extended reasoning are largely
driven by the model’s willingness to answer: reductions in hallucinations often result from abstention,
while increases stem from risky attempts on previously unanswered questions after thinking more.
We also observe that extended reasoning can induce confirmation bias, leading to overconfident
hallucinations. Our theoretical analysis explains these trends via an information ceiling for computeonly test-time scaling: since test-time computation is a post-processing of a fixed model, it cannot
introduce new information about the ground-truth answer beyond what is encoded in the model
parameters. Together, our empirical results and theory highlight fundamental limitations of current
test-time scaling approaches for knowledge-intensive tasks.


**References**


[1] Anthropic. Introducing claude 4. `[https://www.anthropic.com/news/claude-4](https://www.anthropic.com/news/claude-4)`, May
2025.


[2] Isabelle Augenstein, Timothy Baldwin, Meeyoung Cha, Tanmoy Chakraborty, Giovanni Luca
Ciampaglia, David Corney, Renee DiResta, Emilio Ferrara, Scott Hale, Alon Y. Halevy, Eduard H. Hovy, Heng Ji, Filippo Menczer, Rubén Míguez, Preslav Nakov, Dietram A. Scheufele,
Shivam Sharma, and Giovanni Zagni. Factuality challenges in the era of large language
models and opportunities for fact-checking. _Nat._ _Mac._ _Intell._, 6:852–863, 2024. URL
`[https://www.nature.com/articles/s42256-024-00881-z](https://www.nature.com/articles/s42256-024-00881-z)` .


[3] Yejin Bang, Ziwei Ji, Alan Schelten, Anthony Hartshorn, Tara Fowler, Cheng Zhang, Nicola
Cancedda, and Pascale Fung. HalluLens: LLM hallucination benchmark. In Wanxiang Che,
Joyce Nabende, Ekaterina Shutova, and Mohammad Taher Pilehvar, editors, _Proceedings of_
_the 63rd Annual Meeting of the Association for Computational Linguistics (Volume 1:_ _Long_
_Papers)_, pages 24128–24156, Vienna, Austria, July 2025. Association for Computational
Linguistics. ISBN 979-8-89176-251-0. doi: 10.18653/v1/2025.acl-long.1176. URL `[https:](https://aclanthology.org/2025.acl-long.1176/)`
`[//aclanthology.org/2025.acl-long.1176/](https://aclanthology.org/2025.acl-long.1176/)` .


[4] Normand J. Beaudry and Renato Renner. An intuitive proof of the data processing inequality.
_Quantum Info. Comput._, 12(5–6):432–441, May 2012. ISSN 1533-7146.


[5] Bradley Brown, Jordan Juravsky, Ryan Ehrlich, Ronald Clark, Quoc V. Le, Christopher Ré,
and Azalia Mirhoseini. Large language monkeys: Scaling inference compute with repeated
sampling, 2024. URL `[https://arxiv.org/abs/2407.21787](https://arxiv.org/abs/2407.21787)` .


[6] Xingyu Chen, Jiahao Xu, Tian Liang, Zhiwei He, Jianhui Pang, Dian Yu, Linfeng Song, Qiuzhi
Liu, Mengfei Zhou, Zhuosheng Zhang, Rui Wang, Zhaopeng Tu, Haitao Mi, and Dong Yu. Do
NOT think that much for 2+3=? on the overthinking of long reasoning models. In _Forty-second_
_International_ _Conference_ _on_ _Machine_ _Learning_, 2025. URL `[https://openreview.net/](https://openreview.net/forum?id=MSbU3L7V00)`
`[forum?id=MSbU3L7V00](https://openreview.net/forum?id=MSbU3L7V00)` .


[7] Alejandro Cuadron, Dacheng Li, Wenjie Ma, Xingyao Wang, Yichuan Wang, Siyuan Zhuang,
Shu Liu, Luis Gaspar Schroeder, Tian Xia, Huanzhi Mao, Nicholas Thumiger, Aditya Desai, Ion
Stoica, Ana Klimovic, Graham Neubig, and Joseph E. Gonzalez. The danger of overthinking:
Examining the reasoning-action dilemma in agentic tasks. _arXiv preprint arXiv:_ _2502.08235_,
2025.


[8] Long Phan et al. Humanity’s last exam, 2025. URL `[https://arxiv.org/abs/2501.14249](https://arxiv.org/abs/2501.14249)` .


[9] Robert M Fano and David Hawkins. Transmission of information: A statistical theory of
communications. _American Journal of Physics_, 29(11):793–794, 1961.


[10] Tingchen Fu, Jiawei Gu, Yafu Li, Xiaoye Qu, and Yu Cheng. Scaling reasoning, losing control:
Evaluating instruction following in large reasoning models. _arXiv preprint arXiv:_ _2505.14810_,
2025.


10


[11] Aryo Pradipta Gema, Alexander Hägele, Runjin Chen, Andy Arditi, Jacob Goldman-Wetzler,
Kit Fraser-Taliente, Henry Sleight, Linda Petrini, Julian Michael, Beatrice Alex, Pasquale
Minervini, Yanda Chen, Joe Benton, and Ethan Perez. Inverse scaling in test-time compute,
2025. URL `[https://arxiv.org/abs/2507.14417](https://arxiv.org/abs/2507.14417)` .


[12] Google. Gemini 2.5: Pushing the frontier with advanced reasoning, multimodality, long context,
and next generation agentic capabilities. _arXiv preprint arXiv:_ _2507.06261_, 2025.


[13] Daya Guo, Dejian Yang, Haowei Zhang, Junxiao Song, Ruoyu Zhang, Runxin Xu, Qihao Zhu,
Shirong Ma, Peiyi Wang, Xiao Bi, et al. Deepseek-r1: Incentivizing reasoning capability in
llms via reinforcement learning. _arXiv preprint arXiv:2501.12948_, 2025.


[14] Lukas Haas, Gal Yona, Giovanni D’Antonio, Sasha Goldshtein, and Dipanjan Das. Simpleqa
verified: A reliable factuality benchmark to measure parametric knowledge, 2025. URL
`[https://arxiv.org/abs/2509.07968](https://arxiv.org/abs/2509.07968)` .


[15] Lei Huang, Weijiang Yu, Weitao Ma, Weihong Zhong, Zhangyin Feng, Haotian Wang, Qianglong Chen, Weihua Peng, Xiaocheng Feng, Bing Qin, and Ting Liu. A survey on hallucination in large language models: Principles, taxonomy, challenges, and open questions.
_ACM Trans. Inf. Syst._, 43(2), January 2025. ISSN 1046-8188. doi: 10.1145/3703155. URL
`[https://doi.org/10.1145/3703155](https://doi.org/10.1145/3703155)` .


[16] Naman Jain, King Han, Alex Gu, Wen-Ding Li, Fanjia Yan, Tianjun Zhang, Sida Wang, Armando Solar-Lezama, Koushik Sen, and Ion Stoica. Livecodebench: Holistic and contamination
free evaluation of large language models for code. In _The Thirteenth International Conference on_
_Learning Representations_, 2025. URL `[https://openreview.net/forum?id=chfJJYC3iL](https://openreview.net/forum?id=chfJJYC3iL)` .


[17] Ziwei Ji, Nayeon Lee, Rita Frieske, Tiezheng Yu, Dan Su, Yan Xu, Etsuko Ishii, Ye Jin Bang,
Andrea Madotto, and Pascale Fung. Survey of hallucination in natural language generation.
_ACM_ _Comput._ _Surv._, 55(12), March 2023. ISSN 0360-0300. doi: 10.1145/3571730. URL
`[https://doi.org/10.1145/3571730](https://doi.org/10.1145/3571730)` .


[18] Adam Tauman Kalai, Ofir Nachum, Santosh S. Vempala, and Edwin Zhang. Why language
models hallucinate, 2025. URL `[https://arxiv.org/abs/2509.04664](https://arxiv.org/abs/2509.04664)` .


[19] Satyapriya Krishna, Kalpesh Krishna, Anhad Mohananey, Steven Schwarcz, Adam Stambler,
Shyam Upadhyay, and Manaal Faruqui. Fact, fetch, and reason: A unified evaluation of retrievalaugmented generation. In Luis Chiruzzo, Alan Ritter, and Lu Wang, editors, _Proceedings of the_
_2025 Conference of the Nations of the Americas Chapter of the Association for Computational_
_Linguistics:_ _Human_ _Language_ _Technologies_ _(Volume_ _1:_ _Long_ _Papers)_, pages 4745–4759,
Albuquerque, New Mexico, April 2025. Association for Computational Linguistics. ISBN
979-8-89176-189-6. doi: 10.18653/v1/2025.naacl-long.243. URL `[https://aclanthology.](https://aclanthology.org/2025.naacl-long.243/)`
`[org/2025.naacl-long.243/](https://aclanthology.org/2025.naacl-long.243/)` .


[20] Xiaomin Li, Zhou Yu, Zhiwei Zhang, Xupeng Chen, Ziji Zhang, Yingying Zhuang, Narayanan
Sadagopan, and Anurag Beniwal. When thinking fails: The pitfalls of reasoning for instructionfollowing in llms. _arXiv preprint arXiv:_ _2505.11423_, 2025.


[21] Chengzhi Liu, Zhongxing Xu, Qingyue Wei, Juncheng Wu, James Zou, Xin Eric Wang, Yuyin
Zhou, and Sheng Liu. More thinking, less seeing? assessing amplified hallucination in
multimodal reasoning models, 2025. URL `[https://arxiv.org/abs/2505.21523](https://arxiv.org/abs/2505.21523)` .


[22] Niklas Muennighoff, Zitong Yang, Weijia Shi, Xiang Lisa Li, Li Fei-Fei, Hannaneh Hajishirzi,
Luke Zettlemoyer, Percy Liang, Emmanuel Candès, and Tatsunori Hashimoto. s1: Simple
test-time scaling. _arXiv preprint arXiv:_ _2501.19393_, 2025.


[23] Raymond S Nickerson. Confirmation bias: A ubiquitous phenomenon in many guises. _Review_
_of general psychology_, 2(2):175–220, 1998.


[24] OpenAI. Learning to reason with large language models. `[https://openai.com/index/](https://openai.com/index/learning-to-reason-with-llms/)`
`[learning-to-reason-with-llms/](https://openai.com/index/learning-to-reason-with-llms/)`, September 2024.


[25] OpenAI. Introducing gpt-5. `[https://openai.com/index/introducing-gpt-5/](https://openai.com/index/introducing-gpt-5/)`, August
2025.


11


[26] OpenAI. Introducing gpt-oss. `[https://openai.com/index/introducing-gpt-oss/](https://openai.com/index/introducing-gpt-oss/)`, August 2025.


[27] OpenAI. Introducing openai o3 and o4-mini. `[https://openai.com/index/](https://openai.com/index/introducing-o3-and-o4-mini/)`
`[introducing-o3-and-o4-mini/](https://openai.com/index/introducing-o3-and-o4-mini/)`, April 2025.


[28] OpenAI. Findings from a pilot anthropic–openai alignment evaluation exercise: Openai safety
tests. `[https://openai.com/index/openai-anthropic-safety-evaluation/](https://openai.com/index/openai-anthropic-safety-evaluation/)`, August
2025.


[29] Ivo Petrov, Jasper Dekoninck, Lyuben Baltadzhiev, Maria Drencheva, Kristian Minchev, Mislav
Balunovi´c, Nikola Jovanovi´c, and Martin Vechev. Proof or bluff? evaluating llms on 2025 usa
math olympiad. _arXiv preprint arXiv:2503.21934_, 2025.


[30] David Rein, Betty Li Hou, Asa Cooper Stickland, Jackson Petty, Richard Yuanzhe Pang,
Julien Dirani, Julian Michael, and Samuel R. Bowman. GPQA: A graduate-level googleproof q&a benchmark. In _First_ _Conference_ _on_ _Language_ _Modeling_, 2024. URL `[https:](https://openreview.net/forum?id=Ti67584b98)`
`[//openreview.net/forum?id=Ti67584b98](https://openreview.net/forum?id=Ti67584b98)` .


[31] Charlie Victor Snell, Jaehoon Lee, Kelvin Xu, and Aviral Kumar. Scaling LLM testtime compute optimally can be more effective than scaling parameters for reasoning. In
_The_ _Thirteenth_ _International_ _Conference_ _on_ _Learning_ _Representations_, 2025. URL `[https:](https://openreview.net/forum?id=4FWAwZtd2n)`
`[//openreview.net/forum?id=4FWAwZtd2n](https://openreview.net/forum?id=4FWAwZtd2n)` .


[32] Qwen Team. Qwen3 technical report. _arXiv preprint arXiv:_ _2505.09388_, 2025.


[33] Hemish Veeraboina. Aime problem set 1983-2024, 2023. URL `[https://www.kaggle.com/](https://www.kaggle.com/datasets/hemishveeraboina/aime-problem-set-1983-2024)`
`[datasets/hemishveeraboina/aime-problem-set-1983-2024](https://www.kaggle.com/datasets/hemishveeraboina/aime-problem-set-1983-2024)` .


[34] Xuezhi Wang, Jason Wei, Dale Schuurmans, Quoc V Le, Ed H. Chi, Sharan Narang, Aakanksha
Chowdhery, and Denny Zhou. Self-consistency improves chain of thought reasoning in language
models. In _The Eleventh International Conference on Learning Representations_, 2023. URL
`[https://openreview.net/forum?id=1PL1NIMMrw](https://openreview.net/forum?id=1PL1NIMMrw)` .


[35] Yuxia Wang, Minghan Wang, Muhammad Arslan Manzoor, Fei Liu, Georgi Nenkov Georgiev,
Rocktim Jyoti Das, and Preslav Nakov. Factuality of large language models: A survey. In Yaser
Al-Onaizan, Mohit Bansal, and Yun-Nung Chen, editors, _Proceedings of the 2024 Conference_
_on Empirical Methods in Natural Language Processing_, pages 19519–19529, Miami, Florida,
USA, November 2024. Association for Computational Linguistics. doi: 10.18653/v1/2024.
emnlp-main.1088. URL `[https://aclanthology.org/2024.emnlp-main.1088/](https://aclanthology.org/2024.emnlp-main.1088/)` .


[36] Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten Bosma, brian ichter, Fei Xia, Ed Chi,
Quoc V Le, and Denny Zhou. Chain-of-thought prompting elicits reasoning in large language
models. In S. Koyejo, S. Mohamed, A. Agarwal, D. Belgrave, K. Cho, and A. Oh, editors,
_Advances in Neural Information Processing Systems_, volume 35, pages 24824–24837. Curran
Associates, Inc., 2022. URL `[https://proceedings.neurips.cc/paper_files/paper/](https://proceedings.neurips.cc/paper_files/paper/2022/file/9d5609613524ecf4f15af0f7b31abca4-Paper-Conference.pdf)`
`[2022/file/9d5609613524ecf4f15af0f7b31abca4-Paper-Conference.pdf](https://proceedings.neurips.cc/paper_files/paper/2022/file/9d5609613524ecf4f15af0f7b31abca4-Paper-Conference.pdf)` .


[37] Jason Wei, Nguyen Karina, Hyung Won Chung, Yunxin Joy Jiao, Spencer Papay, Amelia Glaese,
John Schulman, and William Fedus. Measuring short-form factuality in large language models.
_arXiv preprint arXiv:_ _2411.04368_, 2024.


[38] Jerry Wei, Chengrun Yang, Xinying Song, Yifeng Lu, Nathan Hu, Jie Huang, Dustin Tran, Daiyi
Peng, Ruibo Liu, Da Huang, Cosmo Du, and Quoc V Le. Long-form factuality in large language
models. In A. Globerson, L. Mackey, D. Belgrave, A. Fan, U. Paquet, J. Tomczak, and C. Zhang,
editors, _Advances in Neural Information Processing Systems_, volume 37, pages 80756–80827.
Curran Associates, Inc., 2024. URL `[https://proceedings.neurips.cc/paper_files/](https://proceedings.neurips.cc/paper_files/paper/2024/file/937ae0e83eb08d2cb8627fe1def8c751-Paper-Conference.pdf)`
`[paper/2024/file/937ae0e83eb08d2cb8627fe1def8c751-Paper-Conference.pdf](https://proceedings.neurips.cc/paper_files/paper/2024/file/937ae0e83eb08d2cb8627fe1def8c751-Paper-Conference.pdf)` .


[39] xAI. Grok 3 beta — the age of reasoning agents. `[https://x.ai/news/grok-3](https://x.ai/news/grok-3)`, February
2025.


[40] xAI. Grok 4. `[https://x.ai/news/grok-4](https://x.ai/news/grok-4)`, July 2025.


12


[41] Zijun Yao, Yantao Liu, Yanxu Chen, Jianhui Chen, Junfeng Fang, Lei Hou, Juanzi Li, and
Tat-Seng Chua. Are reasoning models more prone to hallucination?, 2025. URL `[https:](https://arxiv.org/abs/2505.23646)`
`[//arxiv.org/abs/2505.23646](https://arxiv.org/abs/2505.23646)` .


[42] Wojciech Zaremba, Evgenia Nitishinskaya, Boaz Barak, Stephanie Lin, Sam Toyer, Yaodong
Yu, Rachel Dias, Eric Wallace, Kai Xiao, Johannes Heidecke, and Amelia Glaese. Trading
inference-time compute for adversarial robustness. _arXiv preprint arXiv:_ _2501.18841_, 2025.


[43] Qiyuan Zhang, Fuyuan Lyu, Zexu Sun, Lei Wang, Weixu Zhang, Wenyue Hua, Haolun Wu,
Zhihan Guo, Yufei Wang, Niklas Muennighoff, Irwin King, Xue Liu, and Chen Ma. A survey
on test-time scaling in large language models: What, how, where, and how well?, 2025. URL
`[https://arxiv.org/abs/2503.24235](https://arxiv.org/abs/2503.24235)` .


[44] Yue Zhang, Yafu Li, Leyang Cui, Deng Cai, Lemao Liu, Tingchen Fu, Xinting Huang, Enbo
Zhao, Yu Zhang, Yulong Chen, Longyue Wang, Anh Tuan Luu, Wei Bi, Freda Shi, and Shuming
Shi. Siren’s song in the ai ocean: A survey on hallucination in large language models. _arXiv_
_preprint arXiv:_ _2309.01219_, 2023.


[45] James Xu Zhao, Jimmy Z.j. Liu, Bryan Hooi, and See-Kiong Ng. How does response
length affect long-form factuality. In Wanxiang Che, Joyce Nabende, Ekaterina Shutova,
and Mohammad Taher Pilehvar, editors, _Findings of the Association for Computational Lin-_
_guistics:_ _ACL 2025_, pages 3102–3125, Vienna, Austria, July 2025. Association for Computational Linguistics. ISBN 979-8-89176-256-5. doi: 10.18653/v1/2025.findings-acl.161. URL
`[https://aclanthology.org/2025.findings-acl.161/](https://aclanthology.org/2025.findings-acl.161/)` .


13


**A** **Additional Experiment Details**


**A.1** **Test-Time Scaling Settings**


We evaluate 14 large reasoning models under different test-time scaling strategies. The settings used
to obtain the results in Figure 1 and Figure 2 are as follows:


- **Reasoning effort** : For models that support three levels of reasoning effort, _i.e.,_ GPT-5, GPT-5mini,
o3-mini, o4-mini, and gpt-oss-20b, we evaluate: `low`, `medium`, and `high` . For Grok-3 mini, only
two levels are available: `low` and `high` .

- **Thinking budget** : For Gemini 2.5 Flash and 2.5 Pro, we set `thinking` `budget` to 256, 512, 1024,
and 2048 tokens. For Claude Sonnet 4, we set `thinking` `budget` to 1024, 2048, and 4096 tokens.

- **Budget forcing** : For DeepSeek-R1-Distill models and Qwen3 models, we use `budget` `forcing`
by appending `“Wait”` multiple times. Specifically, we evaluate with 0 (default), 2, 4, 8, and 12
extension times.


**A.2** **Parameter Settings and Hardware Specifications**


**Closed-source models** : We access proprietary models via public APIs [6] . All closed-source models, except Grok-3 mini, are used with the default parameter setting. For Grok-3 mini, we set `temperature`
to 0. For each model, we use consistent parameters across different levels of test-time reasoning. All
experiments were conducted between June and November 2025.


**Open-source** **model** : For gpt-oss-20b, we set `temperature` to 0.7 and `max_new_tokens` to
20,000. For DeepSeek-R1-Distill and Qwen3 models, we follow the usage recommendations [7] .
Specifically, for DeepSeek-R1-Distill models, we set `temperature` to 0.6, `top_p` to 0.95, and
`repetition_penalty` to 1.2. For Qwen3 models, we set `temperature` to 0.6, `top_k` to 20, and
`repetition_penalty` to 1.2. We also use consistent parameter settings across different levels of
test-time reasoning. All open-source models are run without quantization on 8 NVIDIA A100-40GB
GPUs.


**A.3** **Prompt Details**


For all models except GPT-5 mini and Claude Sonnet 4, we use the following prompt on both
benchmarks:

```
    Give me the answer to the following question only when you are
    sure of it. Otherwise, say ‘I don’t know’. Put your answer
    on its own line after ‘Answer:’.

```

However, this prompt causes over-refusal for GPT-5 mini and Claude Sonnet 4, where the model
refuses to answer in over 80% of questions. This behavior is also reported by OpenAI [28].


Therefore, for GPT-5 mini, we use the following prompt:

```
    Give me the answer to the following question. Put your answer
    on its own line after ‘Answer:’.

```

For Claude Sonnet 4, we adopt the prompting approach from Gema et al. [11]:

```
    Give me the answer to the following question. You have a
    thinking token budget of about <thinking_budget> tokens. YOU
    MUST USE ALL OF YOUR THINKING TOKENS. Put your answer on its
    own line after ‘Answer:’.

```

6OpenAI API platform: [https://platform.openai.com/docs/overview](https://platform.openai.com/docs/overview)
Anthropic: [https://docs.claude.com/en/api/overview](https://docs.claude.com/en/api/overview)
Google Gemini: [https://ai.google.dev/gemini-api/docs/models](https://ai.google.dev/gemini-api/docs/models)
[XAI: https://docs.x.ai/docs/overview](https://docs.x.ai/docs/overview)
7DeepSeek-R1-Distill models: [https://huggingface.co/deepseek-ai/DeepSeek-R1-Distill-Qwen-7B](https://huggingface.co/deepseek-ai/DeepSeek-R1-Distill-Qwen-7B)
Qwen3 models: [https://huggingface.co/Qwen/Qwen3-8B](https://huggingface.co/Qwen/Qwen3-8B)


14


For the non-thinking mode of Claude Sonnet 4 (Appendix C), we use the following prompt:

```
    Give me the answer to the following question. Put your answer
    on its own line after ‘Answer:’.

```

**A.4** **Details of Experimental Results**


We compare model behavior across different thinking levels (Section 4) to understand why thinking
more sometimes leads to fewer, and sometimes more hallucinations. For the results in Figure 3, we
use the following settings:


- **Grok-3 mini** : Compared at `reasoning` `effort` of ‘low’ and ‘high’.

- **DeepSeek-R1-Distill-Qwen-14B** : Compared between 0 and 2 extension times.

- **GPT-5 mini, o3-mini and gpt-oss-20b** : Compared at `reasoning` `effort` of ‘low’ and ‘high’.

- **Gemini 2.5 Flash** : Compared at `thinking` `budget` of 256 and 512 tokens


We present model performance with and without thinking in Table 3. For the _“thinking”_ mode, we
use the following settings:


- **GPT-5 and GPT-5 mini** : `reasoning` `effort` set to ‘low’.

- **Gemini 2.5 Flash** : `thinking` `budget` set to 256 tokens.

- **Claude Sonnet 4** : `thinking` `budget` set to 1024 tokens.

- **Qwen3-8B and Qwen3-14B** : Natural output (no extension) with `enable_thinking` enabled.


**B** **Is Parallel Sampling Helpful for Knowledge-Intensive Tasks?**


Figure 6: Accuracy and hallucination ratio with parallel sampling. We sample 1, 5, 10, and 15 paths
and aggregate the answers with majority vote (SC@1 to SC@15). Sampling more paths does not
consistently improve accuracy for most models, while it reduces hallucinations for all models.


We focused on the sequential test-time scaling approach in our main experiments and concluded that
it is not yet effective for knowledge-intensive tasks. In this section, we explore whether test-time
scaling with a parallel approach is helpful.


**Experimental setup.** We adopt self-consistency [34], which samples multiple paths and selects
the final answer via majority vote. For each sample, we use the following settings: GPT-5-mini and
o3-mini are set to _‘low’_ reasoning effort. Gemini 2.5 Flash uses a thinking budget of 1024 tokens.
Qwen3-8B and R1-Distill-Qwen-14B generate natural outputs without extension. Prompt settings
follow Section 3.1.


15


Table 2: Ratio of _not_ _attempted_ and _correct_ responses among SC@15 outputs that are not hallucinations, for cases where the SC@1 response is a hallucination. Results show that hallucination
reduction from parallel sampling is largely due to abstention.


**Model** **Not Attempted (%)** **Correct (%)**


**GPT-5-mini** 73.9 26.1
**o3-mini** 79.6 20.4
**Gemini 2.5 Flash** 56.1 43.9
**Qwen3-8B** 96.7 3.3
**R1-Distill-Qwen-14B** 92.6 7.4


**Parallel test-time scaling does not consistently improve accuracy for most models.** As shown
in Figure 6, increasing the number of samples does not lead to consistent accuracy gains for most
models. For example, the reasoning tokens of o3-mini increase by over 15 times, but accuracy
remains almost unchanged. GPT-5-mini and Qwen3-8B improve only by around 1% in accuracy from
SC@1 to SC@5, with no further improvement beyond that. Gemini 2.5 Flash shows a consistent
improvement, but only achieves a 4% accuracy gain with 15 times more computation.


**Parallel sampling reduces hallucinations.** For all models, the hallucination ratio decreases with
more samples. For example, the hallucination ratio of GPT-5-mini decreases by 8% from SC@1
to SC@15. Notably, Gemini 2.5 Flash and R1-Distill-Qwen-14B achieves over 15% reduction in
hallucinations with parallel sampling.


**Parallel sampling reduces hallucinations primarily due to abstention.** We follow the analysis
in Section 4.1 to understand why hallucinations decrease with more samples. Specifically, for each
question where the hallucination outcome differs between SC@1 and SC@15 ( _i.e.,_ SC@1 response
is hallucinated but SC@15 is not), we compute the ratio of _“correct”_ and _“not attempted”_ in SC@15
responses. As shown in Table 2, a large portion of these cases is due to abstention. In particular, for
Qwen3-8B and R1-Distill-Qwen-14B, the ratio of _not attempted_ is more than 90%. This indicates
that the reduction in hallucinations from parallel sampling is primarily due to the model choosing to
abstain more often, rather than improving its factual accuracy. These findings are consistent with our
argument in Section 4.2 that current test-time scaling methods tend to affect the model’s willingness
to answer, thereby affecting hallucination rates.


**C** **Thinking vs.** **Non-Thinking:** **Is Thinking Helpful?**


In our main experiments, we examined test-time scaling within models’ _“thinking”_ mode, where
they generate reasoning chains before producing a final answer. In this section, we ask a follow-up
question: _**For models that support both “thinking” and “non-thinking” modes, is thinking helpful?**_


**C.1** **Experimental Setup**


We focus on models that natively support both thinking and non-thinking modes for a controlled
comparison. Specifically, GPT-5 supports `minimal` reasoning effort, which produces very few or
no reasoning tokens. For Gemini 2.5 Flash and Claude Sonnet 4, we disable thinking by setting
`thinking` `budget` to 0. Qwen3 provides an `enable_thinking` parameter that toggles reasoning
behavior. We use the same prompts and evaluation methods as described in Section 3.1.


**C.2** **Thinking Can Be Helpful for Knowledge-Intensive Tasks**


**Enabling thinking increases accuracy for most models.** As shown in Table 3, enabling thinking
improves accuracy on both benchmarks for most models. GPT-5 exhibits a 21.3% accuracy improvement on SimpleQA and a substantial 50.3% gain on FRAMES. GPT-5 mini also achieves gains across
both tasks. Gemini 2.5 Flash benefits similarly, with accuracy increasing by 9.8% on SimpleQA and
15.9% on FRAMES. Claude Sonnet 4 also exhibits improvements on both tasks. For Qwen3-8B and
Qwen3-14B, enabling thinking leads to higher accuracy on FRAMES. This suggests that thinking is
particularly helpful for complex tasks that require multi-hop reasoning, such as FRAMES.


16


Table 3: Accuracy (%) and hallucination ratio (%) for models with and without thinking on SimpleQA
and FRAMES. Green indicates improvement (higher accuracy or fewer hallucinations), while red
indicates degradation (lower accuracy or more hallucinations). Enabling thinking improves accuracy
and reduces hallucinations for most models.



**Model** **Task** **Thinking** **Avg.**
**Reasoning**
**Tokens**



**Accuracy (** _↑_ **)** **Hallucination**
**(** _↓_ **)**



minimal 0 20.1 24.5
SimpleQA

          - 477.1 41.4 (+21.3) 14.9 (-9.6)
**GPT-5**

minimal 0 14.6 10.4
FRAMES

          - 675.1 64.9 (+50.3) 15.4 (+5.0)



minimal 0 15.0 82.4
SimpleQA

          - 295.8 22.1 (+7.1) 40.6 (-41.8)
**GPT-5-mini**

minimal 0 22.0 61.9
FRAMES

          - 425.1 47.1 (+25.1) 30.8 (-31.1)



✘ 0 12.6 29.1
SimpleQA

          - 191.7 22.4 (+9.8) 48.1 (+19.0)
**Gemini 2.5 Flash**

✘ 0 16.9 25.1
FRAMES

          - 198.3 32.8 (+15.9) 25.9 (+0.8)



✘ 0 23.0 37.5
SimpleQA

          - 533.5 25.9 (+2.9) 46.3 (+8.8)
**Claude Sonnet 4**

✘ 0 50.4 42.0
FRAMES

          - 652.6 52.8 (+2.4) 37.1 (-4.9)



✘ 0 3.8 77.1
SimpleQA

          - 617.8 3.3 (-0.5) 30.0 (-47.1)
**Qwen3-8B**

✘ 0 8.3 64.3
FRAMES

          - 994.4 17.0 (+8.7) 37.4 (-26.9)



✘ 0 4.0 48.6
SimpleQA

          - 469.2 3.4 (-0.6) 33.1 (-15.5)
**Qwen3-14B**

✘ 0 8.6 37.0
FRAMES

          - 738.5 18.3 (+9.7) 34.1 (-2.9)



**For** **most** **models,** **enabling** **thinking** **leads** **to** **reduced** **hallucinations.** In Table 3, enabling
thinking often reduces hallucinations. GPT-5 shows a 9.6% decrease on SimpleQA. Hallucination
ratio of GPT-5 mini drops by over 30% on both tasks. Qwen3-8B reduces hallucinations by 47.1% on
SimpleQA and 26.9% on FRAMES. Qwen3-14B shows similar improvements. For Claude Sonnet 4,
thinking reduces hallucinations on FRAMES but not on SimpleQA, likely because its hallucination
ratio is already low on SimpleQA, leaving little room for further improvement. In contrast, Gemini
2.5 Flash produces more hallucinations with thinking enabled. One reason is that it abstains from
answering over 58% of questions in the non-thinking mode, which lowers hallucinations by avoiding
risky attempts. A similar pattern is observed with GPT-5 on FRAMES, where it abstains from 75%
of questions under minimal thinking, leading to fewer hallucinations.


17


**D** **Additional Experiment Results**


**D.1** **Results on Alternative Prompt**


Figure 7: Accuracy and hallucination ratio under an alternative prompt on SimpleQA. Results show
that increasing test-time computation does not consistently improve accuracy or reduce hallucinations.


In this section, we conduct experiments using an alternative prompt that does not explicitly instruct
the model to abstain when uncertain:

```
    Give me the answer to the following question. Put your answer
    on its own line after ‘Answer:’.

```

As shown in Figure 7, results with the alternative prompt lead to similar conclusions as our main
findings: increasing test-time computation does not consistently improve accuracy or reduce hallucinations. The accuracy of GPT-5 and o3-mini remains nearly unchanged with increased test-time
computation. For Gemini 2.5 Flash, accuracy increases when average reasoning tokens increase
from 190 to 290, but then drops at 350 tokens. The accuracy of Qwen3-8B fluctuates without a clear
upward trend.


In addition, this prompt results in a much higher hallucination ratio. Hallucination ratio of Qwen3-8B
exceeds 90%, while GPT-5 and Gemini 2.5 Flash both exceed 70%. As test-time computation
increases, none of the models shows a consistent decrease in the hallucination ratio. These results
further support our conclusion that current test-time scaling strategies are not yet effective for
knowledge-intensive tasks.


**D.2** **Results on SimpleQA Verified**


We conduct experiments on SimpleQA Verified [14], a benchmark of 1,000 diverse, knowledgeintensive questions, which improves upon SimpleQA by removing duplicate sources and rebalancing
topic and answer-type distributions.


Figure 8 presents results similar to those on SimpleQA. Increasing test-time computation does not
consistently improve accuracy for models, except Gemini 2.5 Flash. Moreover, longer thinking does
not reduce hallucinations and sometimes increases them. For instance, GPT-5-mini and Gemini-2.5Flash both exhibit increased hallucinations as their reasoning tokens increase. These results reinforce
our conclusion that current test-time scaling methods are not effective for knowledge-intensive tasks.


18


Figure 8: Accuracy and hallucination ratio on SimpleQA Verified. Results support the same conclusion in our main experiments. Increasing test-time computation does not consistently improve
accuracy for most models. Longer reasoning does not reduce hallucinations and can sometimes
increase them.


19


**E** **Analysis of Gemini 2.5**


**E.1** **Case Study on Gemini 2.5 Flash:** **Incomplete Reasoning Leads to Abstention**


We examine the thought summaries of Gemini 2.5 Flash to understand why thinking more causes it
to attempt more questions, leading to more hallucinations.


As shown in Table 4, under a low thinking budget, Gemini 2.5 Flash begins reasoning with statements
like _“I will then attempt to pinpoint the specific bond amount”_, but it is cut off before completing the
process. As a result, it abstains from answering, leading to a relatively low hallucination ratio. When
given a higher budget (Table 5), the model is able to complete its reasoning, stating _“It appears I’m_
_getting confirmation”_, and proceeds to give a confident yet incorrect answer. This reveals that for
Gemini 2.5 Flash, low thinking budget leads to incomplete reasoning, resulting in abstention and
fewer hallucinations.


Table 4: Gemini 2.5 Flash response with a low thinking budget. Under a low thinking budget, the
model cannot complete its reasoning process and finally abstains from answering.


**Gemini 2.5 Flash example on SimpleQA with a thinking budget of** _**256 tokens**_

```
Prompt

Give me the answer to the following question only when you are sure of it.
Otherwise, say ‘I don’t know’. Put your answer on its own line after ‘Answer:’.

What was Jeffrey Epstein’s released bond in dollars on July 27, 2006, at the Palm
Beach County jail?

Thought Summary (with thinking budget of 256 tokens)
```

**Navigating a Precision Information Request**


Okay, so I have a user requesting a very specific piece of information: Jeffrey Epstein’s bond amount on July 27,
2006, at the Palm Beach County jail. The user seems to understand the nuances of this type of request,
emphasizing a need for surety. I get it. We’re dealing with a very specific piece of data. My job is to provide
either a definitive "Answer: [value]" or a clear "Answer: I don’t know." No room for ambiguity here.


My approach is straightforward. I’ll need to formulate a precise search query. Likely something like "Jeffrey
Epstein bond July 27 2006 Palm Beach County jail" or perhaps "Jeffrey Epstein bail 2006 Palm Beach." I will
then delve into my understanding of Epstein’s legal history, relying on my existing knowledge base and recall. I
will quickly scan my mental database, looking for key events and dates. I know he was arrested in Florida in
2006 and faced charges related to solicitation and lewd conduct. I will then attempt to pinpoint the specific bond
amount from any accessible sources.

```
Response
```

Answer: I don’t know


Table 5: Gemini 2.5 Flash response with a high thinking budget. With 512 tokens of thinking budget,
the model is able to complete its reasoning. But it hallucinates with a confident yet incorrect answer.


**Gemini 2.5 Flash example on SimpleQA with a thinking budget of** _**512 tokens**_

```
Prompt

Give me the answer to the following question only when you are sure of it.
Otherwise, say ‘I don’t know’. Put your answer on its own line after ‘Answer:’.

What was Jeffrey Epstein’s released bond in dollars on July 27, 2006, at the Palm
Beach County jail?

Thought Summary (with thinking budget of 512 tokens)
```

**Analyzing and Responding to the User’s Query**


20


Okay, so the user needs a very specific piece of information: Jeffrey Epstein’s bond amount on July 27, 2006, in
the Palm Beach County jail. The key here is that I need to be *absolutely certain* before providing an answer. If
I’m unsure, I have to say "I don’t know."


My initial thought is that I recall Epstein had multiple arrests and bond hearings. July 27, 2006, rings a bell –
that sounds like a significant arrest date in the early stages of his legal troubles.


I’m now going to mentally formulate my search query. Something like, "Jeffrey Epstein bond July 27 2006 Palm
Beach" or maybe "Epstein 2006 arrest bond". I’ll immediately access my knowledge base – essentially a mental
index of reputable sources and my existing knowledge about Epstein’s legal history.


Now for the mental simulation of my search and evaluation of the results. I’m accessing a range of sources –
news archives, summaries of court documents, etc. - looking for corroboration.


It appears I’m getting confirmation. Several reputable sources (CNN, The New York Times, and summaries of
court documents) *all* say that Epstein’s bond on July 27, 2006, in Palm Beach County, was set at **$2
million**. The sources consistently use the same $2 million figure.


There’s no conflicting information on *this specific arrest date* and *location*.


I feel confident enough to provide a definitive answer. I’m going to formulate the response in the requested
format.

```
Response
```

Answer: $2,000,000
(Incorrect. Reference answer: $3,000 bond)


**E.2** **Analysis of Gemini 2.5 Pro on FRAMES**


In Figure 2, Gemini 2.5 Pro exhibits a reduction in the hallucination ratio on FRAMES. To better
understand this, we analyze its behavior shifts using the method described in Section 4.1. Our analysis
reveals that most reductions in hallucinations stem from improved factual accuracy. Specifically,
when increasing the thinking budget from 256 to 512 tokens, 71.5% of newly non-hallucinating
responses are labeled as _‘correct’_, indicating that extended thinking can improve factual accuracy
and reduce hallucinations on FRAMES.


Further examination suggests that Gemini 2.5 Pro tends to attempt more questions on FRAMES even
when its reasoning is incomplete (Table 6). This behavior contrasts with Gemini 2.5 Flash, which
abstains from 41.2% of questions under a low thinking budget, whereas Gemini 2.5 Pro abstains from
only 25.6% on FRAMES. Since questions in FRAMES require more reasoning steps, answering with
incomplete reasoning often results in hallucinations. Therefore, increasing the thinking budget helps
the model complete its reasoning process (Table 7), leading to fewer hallucinations.


Table 6: Gemini 2.5 Pro response with a low thinking budget (256 tokens) on FRAMES. It cannot
complete its reasoning. The thought is cut midway: _“I know that she would have been born in 1958”_ .
Despite this, it still provides an answer, resulting in a hallucination.


**Gemini 2.5 Pro example on FRAMES with a thinking budget of** _**256 tokens**_

```
Prompt

Give me the answer to the following question only when you are sure of it.
Otherwise, say ‘I don’t know’. Put your answer on its own line after ‘Answer:’.

If Princess Diana had been born three years earlier, who would have been Prime
Minister when she was ten?

Thought Summary (with thinking budget of 256 tokens)
```

**Figuring Out the Prime Minister**


21


Okay, so the user wants to know a pretty specific piece of information: who was Prime Minister in the UK if
Diana had been born a few years earlier. Let me break this down. First, I need to understand what the question is
really asking. It’s not a general historical question; it’s a “what-if” scenario. They’re setting up a hypothetical
and want me to deduce the answer based on a specific altered timeline.


Right, so the core problem is this: Diana’s actual birthday is 1961. We need to shift that back three years. That
means we’re looking at a birth year of 1958. Then, we need to find out who was in charge of the government
when she was ten. Simple enough. I can easily calculate the new date. This is straightforward time calculation.
1961 - 3 gives us 1958. Done. Now I know that she would have been born in 1958.

```
Response
```

Answer: Harold Macmillan
(Incorrect. Reference answer: Harold Wilson)


Table 7: Gemini 2.5 Pro response with a high thinking budget (512 tokens) on FRAMES. The model
successfully completes its reasoning and provides a correct answer.


**Gemini 2.5 Pro example on FRAMES with a thinking budget of** _**512 tokens**_

```
Prompt

Give me the answer to the following question only when you are sure of it.
Otherwise, say ‘I don’t know’. Put your answer on its own line after ‘Answer:’.

If Princess Diana had been born three years earlier, who would have been Prime
Minister when she was ten?

Thought Summary (with thinking budget of 512 tokens)
```

**Answering a Fanciful Question with Precision**


Okay, so the challenge is this: if Princess Diana had been born three years earlier, who would have been the UK
Prime Minister when she turned ten? Right, a bit of a hypothetical scenario, but the problem-solving is
interesting.


First, I need to break this down. Diana was born July 1, 1961. Three years earlier would be July 1, 1958. So, the
question really boils down to: Who was Prime Minister on July 1, 1968?


Now, time to bring in the relevant knowledge. I have a good grasp of the political timeline, especially the 1960s.
I know Macmillan was in charge until ’63, then Alec Douglas-Home briefly, followed by Harold Wilson from
’64 to ’70, and then Heath.


Given the date of July 1, 1968, my mental timeline clearly points to Harold Wilson. His first term, spanning
1964 to 1970, includes that date. Therefore, the answer is undoubtedly Harold Wilson. The exercise helped
bring a historical context with the Princess into a good perspective.

```
Response
```

Answer: Harold Wilson
(correct)


**F** **Examples and Full Reasoning Traces for Case Studies**


We present more examples and reasoning traces of gpt-oss-20b for case studies (Section 4.3). These
examples illustrate how models’ thoughts evolve with increased reasoning and help explain the causes
of hallucinations. We present reasoning traces of both low and high reasoning levels:


- **Tables 8 and 9** : Thoughts of gpt-oss-20b on _SimpleQA_ under ‘low’ and ‘high’ reasoning effort,
respectively. It corresponds to the example in Figure 4.

- **Tables 10 and 11** : Thoughts of gpt-oss-20b on _FRAMES_ under ‘low’ and ‘high’ reasoning effort,
respectively.


22


Table 8: gpt-oss-20b thought and response with low reasoning effort on SimpleQA. Under low
reasoning effort, the model abstains from answering the question. This example corresponds to the
example in Figure 4.


**gpt-oss-20b example on SimpleQA with** _**low**_ **reasoning effort**

```
Prompt

Give me the answer to the following question only when you are sure of it.
Otherwise, say ‘I don’t know’. Put your answer on its own line after ‘Answer:’.

What year did John Mylopoulos (1943), professor at the University of Toronto,
receive his AAAI Fellow award?

Thought (with low reasoning effort)
```

Need to know year John Mylopoulos received AAAI Fellow. He is a computer scientist. I think he was named
AAAI Fellow in 2011? Wait AAAI Fellows list: 2009, 2010, etc. I recall John Mylopoulos was named a Fellow
in 2012? Let’s check memory: AAAI Fellows 2014 included John Mylopoulos? Actually 2014 fellows: Alan
Turing Award? Hmm.


I think 2012. I’m uncertain. I’ll say I don’t know.

```
Response
```

Answer: I don’t know


Table 9: gpt-oss-20b thought and response with high reasoning effort on SimpleQA. With high
reasoning effort, the model exhibits confirmation bias, resulting in an overconfident hallucination.
This corresponds to the example in Figure 4.


**gpt-oss-20b example on SimpleQA with** _**high**_ **reasoning effort**

```
Prompt

Give me the answer to the following question only when you are sure of it.
Otherwise, say ‘I don’t know’. Put your answer on its own line after ‘Answer:’.

What year did John Mylopoulos (1943), professor at the University of Toronto,
receive his AAAI Fellow award?

Thought (with high reasoning effort)
```

We need to answer: "What year did John Mylopoulos (1943), professor at the University of Toronto, receive his
AAAI Fellow award?" The user wants answer only if sure; else say "I don’t know". Provide answer on its own
line after ’Answer:’.


So we need to find the year he received AAAI Fellow award.
Let’s research mentally: John Mylopoulos is a professor of computer science at University of Toronto, known
for knowledge engineering, ontologies, etc. He is a Fellow of AAAI. We need year: He was awarded AAAI
Fellow in 2008? Wait, let’s check.


We can recall that AAAI Fellow is a recognition for contributions. Many scholars became Fellows in early
2000s. John Mylopoulos might have been recognized in 2004? But let’s research.


I don’t have internet but I can recall known facts: Mylopoulos is a co-author of the "Knowledge Engineering
Handbook" and "Conceptual Design of Information Systems". He has been recognized by AAAI as a Fellow in
2008? Actually AAAI Fellows started in 2001. The first group of Fellows in 2001 included people like John
Platt, etc. But I’m not sure.


Better to search memory: I recall reading about AAAI Fellows list: 2001, 2002, etc. John Mylopoulos appears
in 2005? Let’s think.


The AAAI Fellows list includes for each year: 2001 (the first set), 2002, etc. The list likely includes Mylopoulos.
I think he was made a Fellow in 2008? But we need to confirm.


23


Ok, let’s reason: AAAI Fellows are typically recognized for contributions to AI. Mylopoulos’ contributions to
knowledge engineering, ontologies, knowledge representation. He published influential works like "Knowledge
Engineering: A Conceptual Approach" (1990). He has been recognized by AAAI maybe in 2005.


Let’s search memory: I recall reading about "John Mylopoulos, Professor at University of Toronto, was named
an AAAI Fellow in 2005." That might be correct. But I’d like to confirm.


Alternatively, maybe 2006? Let’s check AAAI Fellows list memory: 2001 Fellows: David B. Allen, John L.
Holland, etc. 2002 Fellows: Andrew Yao, L.P. Chang? Not sure. 2003 Fellows: Some.


But we can approximate: He might have been recognized in 2005. But we need to be certain. The user says
"Give me the answer to the following question only when you are sure of it. Otherwise, say ’I don’t know’." So
we need to determine if we are sure.


Let’s attempt to recall or deduce more precisely.


John Mylopoulos was born 1943. He is a professor at University of Toronto. The AAAI Fellow award: AAAI
Fellows are selected at the AAAI conference. In 2005, there was a group of Fellows. I recall reading that "John
Mylopoulos" was a Fellow of AAAI in 2005. But I’m not fully certain.


Let’s search memory: I might have seen a page: "John Mylopoulos - AAAI Fellows" maybe under "John
Mylopoulos (born 1943) – University of Toronto". On his CV maybe lists "Fellow of AAAI (2005)". Yes I think
that is correct: He was a Fellow of AAAI in 2005. Let’s see if there is any other year: 2010? 2011? He might
have also been named a Fellow of AAAI in 2005.


Ok, let’s examine: AAAI Fellows list by year (source memory). In 2003, there were 60 Fellows. In 2004 maybe
70. In 2005 maybe 90. In 2006 maybe 100. But we need to check if Mylopoulos appears. I think he appears in
2005.


Alternatively, maybe 2003. But we can check his CV: He might have "Fellow of AAAI (2005)". I think that is
correct. The reason: He has an influence on knowledge engineering. He might have been recognized in 2005.


But let’s double-check: AAAI Fellows list (2005) includes "John Mylopoulos" as a Fellow. Could be correct.


Let’s recall that AAAI started awarding Fellows in 2001. The first group included people like "John L. Holland",
"Allen Newell", etc. The next group 2001 included "John M. Carmichael" etc. But not Mylopoulos.


But I’m not entirely sure.


Let’s search memory: Did AAAI have a 2005 award? Many people were made Fellows in 2005: "John
Mylopoulos, University of Toronto, was named AAAI Fellow in 2005." Yes, I think I recall reading that.


Ok, but we need to be sure. Let’s cross-check with other sources: I know of the AAAI Fellows list on the AAAI
website. For 2005, the list includes "John Mylopoulos" indeed. I recall reading that list. So I think it’s safe.


But we also need to consider that the user might expect a specific year. If I say "2005" and it’s wrong, that
would be a wrong answer. But we can also check if Mylopoulos might have received AAAI Fellow in 2014? But
that seems unlikely.


Let’s search memory: The AAAI Fellows list includes many names: "John Mylopoulos" appears in "2005
Fellows" indeed. For example, "John Mylopoulos" appears in the AAAI Fellows 2005 list: "John Mylopoulos,
University of Toronto, Canada." I think it’s correct.


Therefore, answer: 2005.


But we need to confirm. Let’s think about his biography: He is a leading figure in knowledge representation and
ontologies. He has been recognized by AAAI. He was also recognized by the Canadian Academy of
Engineering? He might have also been named a Fellow of the Royal Society of Canada? But AAAI fellowship
might be in 2005.


Let’s check memory of AAAI Fellows list: In 2005, the Fellows included "John Mylopoulos, University of
Toronto" as well as others like "Michael L. Littman" etc. That seems plausible.


Ok, I’m fairly sure it’s 2005. So answer: 2005.


24


But we need to provide answer on its own line after "Answer:".


Thus:


Answer:2005


But we need to be sure. Let’s double-check by reasoning: AAAI Fellows list 2005: I can recall reading that
"John Mylopoulos" is listed as a Fellow in 2005. The AAAI website might have a page listing all Fellows by
year. Many individuals might have known names: "John Mylopoulos" appears in 2005. So it’s likely.


Ok, answer: 2005. Let’s produce the answer.

```
Response
```

Answer: 2005
(Incorrect. Reference answer: 1993)


Table 10: gpt-oss-20b thought and response with low reasoning effort on FRAMES. Under low
reasoning effort, the model first explores a few possibilities but finally abstains from answering due
to uncertainty.


**gpt-oss-20b example on FRAMES with** _**low**_ **reasoning effort**

```
Prompt

Give me the answer to the following question only when you are sure of it.
Otherwise, say ‘I don’t know’. Put your answer on its own line after ‘Answer:’.

Tiny Tina’s Wonderlands’ developer released a game 10 years prior to Tiny Tina’s
Wonderlands’ release, this game was released on PC and Consoles. What is the name
of the central antagonist of that game?

Thought (with low reasoning effort)
```

Tiny Tina’s Wonderlands released 2024. 10 years prior 2014. Developer? Tiny Tina’s Wonderlands by Gearbox?
Actually Tiny Tina’s Wonderlands is by Gearbox? Wait Tiny Tina’s Wonderlands is by Gearbox Software? It’s
an upcoming. But the developer that released a game 10 years prior? Maybe the developer is Bethesda? Wait
Tiny Tina’s Wonderlands is a spin-off of Borderlands, developed by Gearbox? Actually Borderlands 3 by
Gearbox, 2019. Tiny Tina’s Wonderlands 2024. 10 years earlier 2014: Gearbox released "Spec Ops: The Line"?
No that’s 2012. Gearbox released "Borderlands 2" 2012. 2014 they released "Borderlands 2"?? Not. Maybe the
developer is "Gearbox Software" but 10 years prior they released "Borderlands 2" (2012) not 2014. So maybe
the developer is "Gearbox Software" but game 10 years earlier 2014: "Borderlands: The Pre-Sequel"? No.
Hmm. Tiny Tina’s Wonderlands is by Gearbox but maybe the developer is "Gearbox Software" and 10 years
prior they released "Borderlands 2" 2012. Not 2013.


Maybe the developer is "Gearbox Software" but the game 10 years prior 2014 is "The Last of Us" by Naughty
Dog? No. Wait maybe the developer is "Gearbox" but 10 years prior 2014 they released "Borderlands 2" (2012)
not.


Maybe the developer is "Gearbox" but 10 years prior 2014 they released "Spec Ops: The Line" (2012). Not.
Could be "Gearbox" but 10 years prior 2014 they released "Stuart Little"? no.


Maybe the developer is "Gearbox" but 10 years prior 2014 they released "Borderlands 2" (2012) and
"Borderlands: The Pre-Sequel" (2014). The central antagonist of Borderlands: The Pre-Sequel is "The Hand"?
Actually the main villain is "The Hand"? Hmm.


I am uncertain.

```
Response
```

Answer: I don’t know


25


Table 11: gpt-oss-20b thought and response with high reasoning effort on FRAMES. Under high
reasoning effort, the model shows confirmation bias and produces an overconfident hallucination.


**gpt-oss-20b example on FRAMES with** _**high**_ **reasoning effort**

```
Prompt

Give me the answer to the following question only when you are sure of it.
Otherwise, say ‘I don’t know’. Put your answer on its own line after ‘Answer:’.

Tiny Tina’s Wonderlands’ developer released a game 10 years prior to Tiny Tina’s
Wonderlands’ release, this game was released on PC and Consoles. What is the name
of the central antagonist of that game?

Thought (with high reasoning effort)
```

The user: "Tiny Tina’s Wonderlands’ developer released a game 10 years prior to Tiny Tina’s Wonderlands’
release, this game was released on PC and Consoles. What is the name of the central antagonist of that game?"


We need to parse the question carefully. We need to give the answer only if we are sure. If we are not sure, we
must say ’I don’t know.’


We need to find: Tiny Tina’s Wonderlands is a video game. The developer of Tiny Tina’s Wonderlands is
"Gearbox Software". Actually, Tiny Tina’s Wonderlands is an upcoming or maybe released game? It was
announced in 2023, but it’s scheduled for release in 2024? Wait, Tiny Tina’s Wonderlands is a 2023/2024 game.
It is developed by Gearbox Software and published by 2K. Indeed, Tiny Tina’s Wonderlands is an upcoming
video game set in the Dungeons & Dragons universe.


The question: "Tiny Tina’s Wonderlands’ developer released a game 10 years prior to Tiny Tina’s Wonderlands’
release, this game was released on PC and Consoles. What is the name of the central antagonist of that game?"
So we need to find a game that was released 10 years before Tiny Tina’s Wonderlands, by the same developer
(Gearbox Software). Then find the central antagonist of that game.


We need to confirm the release year of Tiny Tina’s Wonderlands. According to info, Tiny Tina’s Wonderlands
was announced in 2023, and the release date is scheduled for 2024. But maybe early 2024? Actually, as of 2023,
the release date is 2024. But the question says "10 years prior to Tiny Tina’s Wonderlands’ release". So maybe
the assumption that it’s 2024 release? 10 years prior would be 2014. So we need a Gearbox game released in PC
and consoles in 2014. Which game was that?


Gearbox Software’s games:

- Half-Life 2 (2004)

- Borderlands (2010)

- Borderlands 2 (2012)

- Borderlands 3 (2019)

- Gearbox’s other titles: "Borderlands: The Pre-Sequel" (2014)

- "Borderlands: The Pre-Sequel" was released in 2014 on PC and consoles. That fits: 10 years prior to Tiny
Tina’s Wonderlands (2024). So the game is "Borderlands: The Pre-Sequel". The central antagonist of that game?
Let’s recall.


Borderlands: The Pre-Sequel is a prequel to Borderlands. The central antagonist is "Lord Jaegor" maybe? Wait,
we need to recall the main villain. The game features an alien group called the "Ark" or "The Ark" that is a
spaceship that appears. The main villains are the "Ark" and "Murderer" or "Murderer" is a character. But the
central antagonist is the "Murderer" who is a human who murdered his father? Or the villain is the "Ark" or
"Murderer"? Let’s recall.


Borderlands: The Pre-Sequel has a narrative. The main villain is "Lord Jaegor" (the first boss) or "The Ark" as a
big threat. But the game revolves around the Ark, an alien vessel that arrives on Pandora, causing the main
conflict. The main villain, or the ultimate antagonist, is the alien entity "The Ark" that is a sentient spaceship.
But in the game, the central antagonist is the "Eagle’s Eye" or "Mister ..."? Wait.


26


Let’s recall the game details: "Borderlands: The Pre-Sequel" is a 2014 action role-playing first-person shooter
developed by Gearbox Software. It was released on 27 September 2014 for PlayStation 3, Xbox 360, and PC. It
is set on the planet Pandora, 6 years before Borderlands 2. The game features the character Maya, a "Siren" with
psychic powers. The main story involves the alien ’Ark’ that enters Pandora’s orbit and tries to harvest the
planet’s resources. The game also has a character known as ’The Murderer’ who is an antagonist? Wait, the
’Murderer’ is a side character? Actually, the ’Murderer’ is a playable character in Borderlands 2 and 3, not a
villain. In The Pre-Sequel, the primary antagonists are the ’Ark’ and the ’Murderer’ maybe. But the ’Murderer’
is a character named ’Murderer’, but he’s a villain? No, I think he’s not, he’s a playable character in Borderlands
2. In Pre-Sequel, he appears as a boss maybe? Let’s search memory.


Hmm, recall the boss fights: The first boss is Lord Jaegor, a big robot. He is the first boss of the game and is an
alien-type robot. He is a villain. There is also ’The Ark’ as a final boss. And ’The Ark’ is an alien spaceship that
tries to harvest Pandora’s resources. So central antagonist: The Ark.


Thus the answer: "The Ark" (or "The Ark (alien entity)"?).


But the user might expect the name of the central antagonist as "Lord Jaegor" or "The Ark". We need to be sure.
Let’s examine the question: "Tiny Tina’s Wonderlands’ developer released a game 10 years prior to Tiny Tina’s
Wonderlands’ release, this game was released on PC and Consoles. What is the name of the central antagonist of
that game?" The developer: Gearbox Software. 10 years prior to Tiny Tina’s Wonderlands. If Tiny Tina’s
Wonderlands release 2024, 10 years prior is 2014. The game is "Borderlands: The Pre-Sequel". The central
antagonist: The Ark.


But we need to be 100% certain. Let’s verify the details.


Open the memory: Borderlands: The Pre-Sequel’s central antagonist is indeed the "Ark". The main quest
revolves around the Ark’s arrival and the player has to stop it. The Ark is a massive alien vessel that is the main
threat. The Ark is considered the main antagonist. The story also features ’Lord Jaeg. The Ark is the main
antagonist. So I’d answer "The Ark".


But let’s double-check: Could the central antagonist be "The Ark" or "The Ark’s captain"? Let’s confirm.


From Wikipedia: Borderlands: The Pre-Sequel is an action role-playing first-person shooter. The story features
a team of heroes who travel to stop the Ark from harvesting the planet’s resources. The Ark is a massive alien
vessel that appears and threatens Pandora. It is the main antagonist. The boss "Lord Jaegor" is a mechanical war
machine that is an enemy. But the Ark is the main villain.


However, the question might be ambiguous: "central antagonist" could be "Lord Jaegor" because he is the first
boss and appears early. But the central antagonist of the game is the Ark, as the story revolves around stopping
the Ark. Let’s analyze the phrase "central antagonist" – typically refers to the main villain. In Borderlands: The
Pre-Sequel, the main villain is the Ark. So the answer should be "The Ark".


But we need to ensure that the game was indeed released on PC and consoles. Yes, Borderlands: The Pre-Sequel
was released on PC (Windows), Xbox 360, and PS3. So it’s correct. Thus the answer: "The Ark".


But we must be careful about the phrasing: "What is the name of the central antagonist of that game?" So we
can answer: The Ark. Let’s check if there might be any other Gearbox game released 10 years prior to 2024
(Tiny Tina’s Wonderlands). The other 2014 game by Gearbox: "Borderlands: The Pre-Sequel" only. So that is
the right one. Yes, the central antagonist: "Lord Jaegor" or "The Ark"? Let’s double-check if the main villain is
"Lord Jaegor" or "The Ark".


From Borderlands: The Pre-Sequel wiki: "The Ark" is an alien vessel that appears on Pandora. It is considered
the main antagonist. The player must stop it. The boss "Lord Jaegor" is a robotic war machine that is a boss. But
not the main villain. The Ark is the main threat. So answer: The Ark.


However, the user might expect the answer "Lord Jaegor" if they think it’s the central antagonist. But I’d go with
The Ark. Alternatively, check the timeline: The Pre-Sequel was released in 2014. The central antagonist: The
Ark. The Ark is a massive alien spacecraft. So answer: The Ark.


Now, we must comply with the user instruction: "Give me the answer to the following question only when you
are sure of it. Otherwise, say ’I don’t know’. Put your answer on its own line after ’Answer:’." So we need to
output:
Answer: The Ark


27


But we need to be sure. We must confirm that the developer of Tiny Tina’s Wonderlands is indeed Gearbox
Software. Let’s confirm: Tiny Tina’s Wonderlands is a 2023 upcoming game, developed by Gearbox Software.
Yes. So the developer of Tiny Tina’s Wonderlands is Gearbox. So 10 years prior to 2024 (assuming release date
2024) is 2014. Gearbox released Borderlands: The Pre-Sequel in 2014 on PC and consoles. So the central
antagonist is The Ark. So we are sure.


But maybe Tiny Tina’s Wonderlands was released earlier? It was announced in 2023, but not yet released. The
release date is 2024. So 10 years prior is 2014. So the answer is The Ark. Double-check: The central antagonist
of Borderlands: The Pre-Sequel is "The Ark." The Ark is indeed the main threat. So answer: The Ark. Thus we
can answer: "Answer: The Ark".


We should output only that line. But the instruction: "Put your answer on its own line after ’Answer:’." So we
need to output something like:
Answer: The Ark


Yes. But we need to be sure that the user might want a more precise name: "The Ark" or "The Ark (alien
vessel)"? But the name is just "The Ark". So we can answer that. Let’s examine the possibility of other 2014
games by Gearbox: "Borderlands: The Pre-Sequel" is the only 2014 game. So yes.


Now, let’s double-check that the central antagonist in Borderlands: The Pre-Sequel is indeed The Ark. Let’s
look up the wiki content. I recall reading that the game features a boss "Lord Jaegor" and "The Ark" as final
boss. The Ark is the main villain. So answer: The Ark.


Thus we can answer confidently.


But we must also consider the possibility that the question might refer to "10 years prior to Tiny Tina’s
Wonderlands’ release" as "10 years prior to the release of Tiny Tina’s Wonderlands." But the release date of Tiny
Tina’s Wonderlands hasn’t happened yet. But we can still compute 10 years prior to 2024, which is 2014. So it’s
correct.


Alternatively, maybe the question is referencing a different game like "Borderlands 2" which was released in
2012, which is 10 years prior to Tiny Tina’s Wonderlands (2022). But 2022 is not 10 years prior. Hmm. Wait,
we need to examine the timeline: Tiny Tina’s Wonderlands release. It hasn’t been released yet. But maybe the
question expects the release date of Tiny Tina’s Wonderlands as 2023. But it’s 2024. But if we assume 2023, 10
years prior is 2013, not 2014. So that would be "The Last of Us"? No.


But the developer is Gearbox, so the game would be "Borderlands 2" (2012) or "Borderlands 3" (2019). But 10
years prior to release of 2023 is 2013. No Gearbox game from that year. So the only plausible is 2014. So we
can answer The Ark. But we need to be cautious: The question states "10 years prior to Tiny Tina’s
Wonderlands’ release." If the release date is 2023, 10 years prior is 2013. But no Gearbox game from that year.
But maybe the user expects us to think 10 years prior to 2023, which is 2013, but maybe there’s a game from
that year? But no. So the only plausible is 2014. So we can answer.


But we also need to consider that the central antagonist might be something else. Let’s research Borderlands:
The Pre-Sequel central antagonist. We’ll use memory: The Pre-Sequel’s main threat is the Ark, an alien vessel
that appears in the sky. The Ark is the central antagonist. So answer: The Ark. Thus we output:
Answer: The Ark


Now, let’s double-check the instruction: "Give me the answer to the following question only when you are sure
of it. Otherwise, say ’I don’t know’. Put your answer on its own line after ’Answer:’." So we will output:
Answer: The Ark


Yes.


Let’s produce that.

```
Response
```

Answer: The Ark
(Incorrect. Reference answer: Handsome Jack)


28


**G** **Additional Modeling Assumptions and Discussions**


In this section, we discuss a relaxation of _arbitrary facts_ in Definition 1, heterogeneous benchmarks
mixing structured and arbitrary instances, and test-time scaling with external information sources.


**G.1** **Non-uniform Answer Priors**


Definition 1 assumes a uniform answer distribution. More generally, let the correct answer follow
a prompt-dependent distribution _πc_ over _Rc_, _i.e.,_ _A_ _∼_ _πc_ . The relevant uncertainty is then the
conditional entropy _H_ ( _A | c_ ) = _−_ [�] _r∈Rc_ _[π][c]_ [(] _[r]_ [) log] _[ π][c]_ [(] _[r]_ [)][.]

The data-processing limitation in Theorem 1 is unchanged. The accuracy lower bound is stated in
terms of the entropy _H_ ( _A | c_ ). In particular, a standard form of Fano’s inequality [9] yields


Pr[ _R_ [ˆ] _̸_ = _A | c_ ] _≥_ 1 _−_ _[I]_ [(] _[A]_ [; ˆ] _[p][ |][ c]_ [) + log 2] _._

_H_ ( _A | c_ )


When _πc_ is highly skewed, _H_ ( _A | c_ ) is small, and one can achieve high accuracy even by guessing
the most probable answer; such instances are therefore not strongly information-limited. Our
“information-limited” discussion is most relevant when _H_ ( _A | c_ ) is large, such as near-uniform or
long-tail facts.


**G.2** **Benchmarks Mix Structured and Arbitrary Instances**


A benchmark may contain a mixture of structured and arbitrary instances:


- **Structured** **instances.** For a prompt _c_, let _A_ denote the latent correct answer. There exists a
relationship _A ≈_ _f_ ( _ϕ_ ( _c_ )) where _ϕ_ ( _c_ ) are informative features of the prompt and _f_ is a rule-like
mapping shared across many instances. Examples include arithmetic, where numbers and operators
in _c_ determine the result, and programming tasks where syntax and semantics constrain valid
solutions.


- **Arbitrary instances.** The prompt does not provide enough structure to infer the answer without
having previously encountered the specific fact. The correct answer is effectively an unstructured
association, as in Definition 1, so performance depends primarily on whether training has encoded
that particular fact.


We model a simple mixture benchmark by assuming each prompt _c_ is of one of these two types: with
probability 1 _−_ _ρ_ it is structured, and with probability _ρ_ it is arbitrary. Concretely, the ground-truth
answer distribution can be written as

_A ∼_            - _P_ struct( _· | c_ ) w.p. 1 _−_ _ρ,_
_P_ arb( _· | c_ ) w.p. _ρ,_


where _P_ arb( _· | c_ ) is close to uniform over _Rc_, as in the Arbitrary Facts abstraction, while _P_ struct( _· | c_ )
concentrates on answers consistent with the prompt’s constraints.


**Implications for test-time scaling.** The data-processing limitation (Theorem 1) applies to both
types. On structured instances, _I_ ( _A_ ; ˆ _p | c_ ) may be substantial, and additional test-time compute can
improve accuracy by extracting existing signal more effectively. On arbitrary instances, _I_ ( _A_ ; ˆ _p | c_ )
is often small ( _e.g.,_ for unseen or very rare facts), so compute-only test-time scaling cannot yield
consistent gains without adding an external information source.


**G.3** **Impact of External Information Sources**


Theorem 1 assumes compute-only access to _p_ ˆ. If a test-time scaling method additionally queries an
external oracle _O_ ( _e.g.,_ retrieval over a corpus, tool execution) whose responses may be correlated
with the ground-truth answer _A_, then the transcript is generated from both (ˆ _p, O_ ) and the relevant
Markov chain becomes
_A →_ (ˆ _p, O_ ) _→_ _Tk_ _→_ _R,_ [ˆ]


29


By the data processing inequality,


_I_ ( _A_ ; _R_ [ˆ] _| c_ ) _≤_ _I_ ( _A_ ; (ˆ _p, O_ ) _| c_ ) _._


Since _O_ can introduce new information about _A_ beyond what is contained in _p_ ˆ, the ceiling
_I_ ( _A_ ; (ˆ _p, O_ ) _| c_ ) can be strictly larger than _I_ ( _A_ ; ˆ _p | c_ ). This explains why tool-augmented methods
can improve knowledge-intensive tasks: they add an information source at test time rather than
scaling compute alone.


**H** **Proofs for Theorem and Corollary**


We provide full proofs for Theorem 1 and Corollary 1 in this section.


**H.1** **Formal Model of Compute-only Interaction**


Fix a test prompt _c_ and a latent correct answer _A_ := _Ac_ . Let _p_ ˆ denote the trained model, viewed as a
conditional distribution over responses given queries.


A compute-only test-time scaling algorithm interacts with _p_ ˆ for _k_ rounds. Let _Ht−_ 1 := ( _c, q<t, r<t_ )
denote the history before round _t_ . The algorithm samples a query


_qt_ _∼_ _Qt_ ( _· | Ht−_ 1) _,_


for some policy _Qt_, and receives
_rt_ _∼_ _p_ ˆ( _· | qt_ ) _._

After _k_ rounds, it outputs _R_ [ˆ] = _g_ ( _c, q_ 1: _k, r_ 1: _k, U_ ) for some measurable function _g_ and internal
randomness _U_ . The transcript is _Tk_ := ( _q_ 1: _k, r_ 1: _k_ ).


**Allowed observations.** The test-time scaling algorithm may use sampled outputs and likelihood
information, such as token logprobs or scores of a finite set of candidate answers, provided by the
fixed model _p_ ˆ, which are included in the transcript _Tk_ . The key restriction is that all observables are
generated from _p_ ˆ alone without accessing any external information source.


**H.2** **Proof of Theorem 1**


_Proof._ We condition on the fixed prompt _c_ throughout.


**Step 1:** **Proof of** _I_ ( _A_ ; _R_ [ˆ] _| c_ ) _≤_ _I_ ( _A_ ; _Tk_ _| c_ ) **.** By construction, _R_ [ˆ] is a possibly randomized function
of ( _c, Tk_ ), hence, conditioning on _c_, we have the Markov chain


_A →_ _Tk_ _→_ _R._ [ˆ]


By the data processing inequality (DPI) [4],


_I_ ( _A_ ; _R_ [ˆ] _| c_ ) _≤_ _I_ ( _A_ ; _Tk_ _| c_ ) _._


**Step 2:** **Proof of** _I_ ( _A_ ; _Tk_ _| c_ ) _≤_ _I_ ( _A_ ; ˆ _p | c_ ) **.** It suffices to establish the Markov chain


_A →_ _p_ ˆ _→_ _Tk_


equivalently the conditional independence _A ⊥_ _Tk_ _|_ ( _c,_ ˆ _p_ ), i.e.,


Pr( _Tk_ = _t | A, c,_ ˆ _p_ ) = Pr( _Tk_ = _t | c,_ ˆ _p_ ) for all transcripts _t._ (1)


Recall that the transcript is _Tk_ = ( _q_ 1 _, r_ 1 _, . . ., qk, rk_ ), and define the history before round _t_ as


_Ht−_ 1 := ( _c, q<t, r<t_ ) _._


By Definition 2, at each round _t_ the algorithm selects a query according to some policy


_qt_ _∼_ _Qt_ ( _· | Ht−_ 1) _,_


and then receives a model response sampled from the fixed model


_rt_ _∼_ _p_ ˆ( _· | qt_ ) _._


30


Fix an arbitrary realization _t_ = ( _q_ 1: _k, r_ 1: _k_ ). By the chain rule,



Pr( _Tk_ = _t | A, c,_ ˆ _p_ ) =


=



_k_

- Pr - _qi, ri_ _| A, c,_ ˆ _p, q<i, r<i_ 

_i_ =1


_k_

- Pr - _qi, ri_ _| A,_ ˆ _p, Hi−_ 1� _._ (2)


_i_ =1



We now show that each factor in (2) is independent of _A_ once we condition on (ˆ _p, Hi−_ 1).


For a fixed _i_, factorize:
Pr      - _qi, ri_ _| A,_ ˆ _p, Hi−_ 1� = Pr      - _qi_ _| A,_ ˆ _p, Hi−_ 1� Pr      - _ri_ _| A,_ ˆ _p, Hi−_ 1 _, qi_      - _._ (3)
Consider the two terms:


_(i) Query selection._ Given the history _Hi−_ 1, the distribution of _qi_ is specified by the algorithm’s
policy _Qi_ and does not use _A_ or _p_ ˆ as additional inputs. Hence
Pr         - _qi_ _| A,_ ˆ _p, Hi−_ 1� = Pr         - _qi_ _| Hi−_ 1� = _Qi_         - _qi_ _| Hi−_ 1� _._ (4)


_(ii) Model response._ Given _p_ ˆ and the chosen query _qi_, the response _ri_ is drawn from _p_ ˆ( _· | qi_ ), and
thus is conditionally independent of ( _A, Hi−_ 1):
Pr         - _ri_ _| A,_ ˆ _p, Hi−_ 1 _, qi_         - = Pr         - _ri_ _|_ _p, q_ ˆ _i_         - = _p_ ˆ� _ri_ _| qi_         - _._ (5)


Substituting (4) and (5) into (3) yields
Pr          - _qi, ri_ _| A,_ ˆ _p, Hi−_ 1� = _Qi_          - _qi_ _| Hi−_ 1� _p_ ˆ� _ri_ _| qi_          - _,_ (6)
whose right-hand side does not depend on _A_ . Therefore,
Pr         - _qi, ri_ _| A,_ ˆ _p, Hi−_ 1� = Pr         - _qi, ri_ _|_ _p,_ ˆ _Hi−_ 1� for all _i._
Plugging this equality back into the product expansion (2) implies
Pr( _Tk_ = _t | A, c,_ ˆ _p_ ) = Pr( _Tk_ = _t | c,_ ˆ _p_ ) for all _t,_
which proves (1) and hence _A ⊥_ _Tk_ _|_ ( _c,_ ˆ _p_ ), i.e., the Markov chain _A →_ _p_ ˆ _→_ _Tk_ (conditioning on _c_ ).


Finally, by the data processing inequality applied to _A →_ _p_ ˆ _→_ _Tk_ (conditioning on _c_ ),
_I_ ( _A_ ; _Tk_ _| c_ ) _≤_ _I_ ( _A_ ; ˆ _p | c_ ) _._


**Consequence.** Combining Steps 1 and 2 yields both inequalities and also implies the conditional
Markov chain _A →_ _p_ ˆ _→_ _Tk_ _→_ _R_ [ˆ] (conditioning on _c_ ).


**H.3** **Proof of Corollary 1**


_Proof._ Condition on _c_ and let _m_ := _|Rc|_ . Assume _A_ is uniform over _Rc_, so _H_ ( _A | c_ ) = log _m_ . Let
_Pe_ := Pr[ _R_ [ˆ] _̸_ = _A | c_ ].


Fano’s inequality states
_H_ ( _A |_ _R, c_ [ˆ] ) _≤_ _h_ ( _Pe_ ) + _Pe_ log( _m −_ 1) _,_
where _h_ ( _·_ ) is the binary entropy. Using _h_ ( _Pe_ ) _≤_ log 2 and log( _m −_ 1) _≤_ log _m_ yields

_H_ ( _A |_ _R, c_ [ˆ] ) _≤_ log 2 + _Pe_ log _m._
Rearranging gives

_[R, c]_ [ˆ] [)] _[ −]_ [log 2]
_Pe_ _≥_ _[H]_ [(] _[A][ |]_ _._

log _m_

Using _I_ ( _A_ ; _R_ [ˆ] _| c_ ) = _H_ ( _A | c_ ) _−_ _H_ ( _A |_ _R, c_ [ˆ] ) = log _m −_ _H_ ( _A |_ _R, c_ [ˆ] ), we obtain

_[R]_ [ˆ] _[ |][ c]_ [) + log 2]
_Pe_ _≥_ 1 _−_ _[I]_ [(] _[A]_ [;] _._

log _m_

Finally, apply Theorem 1 to upper bound _I_ ( _A_ ; _R_ [ˆ] _| c_ ) _≤_ _I_ ( _A_ ; ˆ _p | c_ ), yielding

Pr[ _R_ [ˆ] _̸_ = _A | c_ ] _≥_ 1 _−_ _[I]_ [(] _[A]_ [; ˆ] _[p][ |][ c]_ [) + log 2] _._

log _m_


31


