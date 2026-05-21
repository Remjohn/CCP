## **Steering Conversational Large Language Models for Long Emotional** **Support Conversations**

**Navid Madani** **and** **Sougata Saha** **and** **Rohini Srihari**
Computer Science and Engineering - University at Buffalo
Buffalo, NY, 14260
{smadani, sougatas, rohini}@buffalo.edu


**Abstract**


In this study, we address the challenge of enabling large language models (LLMs) to consistently adhere to emotional support strategies
in extended conversations. We focus on the
steerability of the Llama-2 and Llama-3 suite
of models, examining their ability to maintain
these strategies throughout interactions. To assess this, we introduce the Strategy Relevant
Attention (SRA) metric, which quantifies the
model’s adherence to the prompted strategy
through attention maps. To facilitate our study,
we create a strategy-conditioned synthetic conversational dataset derived from the ESConv
dataset. We also propose various baselines
informed by our proposed SRA metric to address the challenge and propose a fine-tuned
model that significantly enhances the steerability of the base model in following the strategy
throughout the conversation. The code and data
are publicly available on our GitHub. [1]


**1** **Introduction**



In the rapidly evolving domain of conversational
AI, the creation of emotionally intelligent conversational agents is becoming increasingly important
as it opens up new possibilities for more natural
and helpful interactions between humans and machines. Central to this transformative journey is the
challenge of empowering large language models
(LLMs) not only to partake in natural dialogues
but also to adeptly navigate and influence the conversation flow using expert strategies derived from
psychology and emotional support literature.
This paper delves into the critical aspect of integrating emotional support strategies into conversational LLMs, a domain that remains largely uncharted yet holds significant promise for a range
of applications, from mental health support to customer service.


[1https://github.com/navidmdn/ESConv-SRA](https://github.com/navidmdn/ESConv-SRA)



Figure 1: A sample continuation of a conversation using
**"Provide Different Perspectives"** strategy, given by
three different prompt templates sorted by the SRA metric increasing from bottom to top using Llama-70b-chat
model. The model output using the prompt template
with higher SRA adheres better to the given strategy.


The advent of the Emotional Support Conversations dataset (ESConv) (Liu et al., 2021) has
marked a significant milestone, providing a rich
resource for researchers to delve into and enhance
emotional support dialogue systems. Despite this
advancement, there remains a notable gap in the
state-of-the-art evaluation methods for such systems. Researchers have tried to build and improve



1


systems that either align closely with the gold standard responses in the dataset (responses from Amazon MTurk workers certified as emotional supporters) or focus on enhancing the model’s ability to
plan subsequent strategies. However, the predominant metric for comparison in these works remains
the alignment with these gold standard responses.
We argue that this approach may not be the most
effective for several reasons. First, in the realm of
emotional support, there is often no single ’correct’
strategy for continuing a conversation. Second,
even when a model bases its response on a specific
strategy, there are numerous potential high-quality
responses that could be equally effective.

In our research, we adopt a different perspective,
reevaluating the core problem in the context of recent advancements. With the advent of Large Language Models (LLMs), generating natural and fluent text has become less of a challenge. Our focus,
therefore, shifts to a more nuanced aspect: the degree to which we can effectively guide these LLMs
to adhere to specific emotional support strategies
during extended conversations, and importantly,
**how** **we** **can** **evaluate** **and** **quantify** **their** **pro-**
**ficiency** **in** **following** **these** **strategies** . This approach acknowledges the proficiency of LLMs in
text generation while emphasizing the critical need
for strategic control and direction in prolonged interactive scenarios. The challenge extends beyond
merely directing the conversation, delving into the
realm of assessing and quantifying the model’s adherence to the predefined emotional support strategies. Below are the main contributions of our work:


**Introducing Strategy Relevant Attention (SRA):**
**Measuring** **Strategy** **Adherence** **in** **Conversa-**
**tional** **AI** **Through** **Attention** **Lens** We introduce a novel proxy metric termed _Strategy Relevant_
_Attention (SRA)_, designed to quantitatively assess
the extent to which a model aligns its attention with
the strategic directives provided in prompts. This
metric facilitates the comparative analysis of different models in terms of their efficacy in guiding
model adherence to predefined strategies. Furthermore, SRA aids in the development of prompts that
enhance the model’s ability to maintain strategic
consistency throughout prolonged conversations.
Through rigorous evaluation, encompassing both
automated and human assessments, we establish
a significant correlation between a model’s adherence to strategy and its SRA score, highlighting
the utility of SRA in evaluating a model’s strategy



following capability.


**Release** **of** **an** **Extended** **ESConv** **Dataset** As
a practical contribution to the field, we release an
extensive synthetic dataset. This dataset, an extension of the existing ESConv dataset, features
multiple strategy continuations. It serves as a valuable resource for further research and development
in building steerable emotional support agents suitable for long conversations.


**A Steerable Emotional Support Model** In addition, we fine-tune Llama2-7B-chat and Llama38B-instruct models under multiple strategic conditions to improve its steerability throughout extended conversations. Our results demonstrate that
the fine-tuned models exhibit significantly better
steerability in long conversations compared to the
base models. This improvement is also consistent
with our finding that the fine-tuned models achieve
a higher SRA metric.


**2** **Related Work**


**2.1** **Emotional Support Conversation Systems**


The landscape of Emotional Support (ES) systems
has undergone significant evolution, shaped largely
by the nature and complexity of datasets available
for research. Early ES datasets predominantly consisted of single-turn conversations ((Medeiros and
Bosse, 2018), (Sharma et al., 2020)), leading to a
research focus primarily on developing Emotional
Support Conversation (ESC) systems for these
simplified, single-interaction scenarios ((Sharma
et al., 2021), (Hosseini and Caragea, 2021)).This
approach, while foundational, did not fully encapsulate the dynamic and multi-faceted nature of realworld emotional support interactions. The release
of the first multi-turn ESC dataset, ESConv (Liu
et al., 2021), marked a pivotal shift in this domain.
This dataset opened up new avenues for exploring
data-driven approaches in multi-turn ESC systems.
(Peng et al., 2022a) introduced an innovative
hierarchical graph network, aiming to effectively
utilize both the global emotion cause and the local
user intention in emotional support conversations.
Moving away from relying on a single strategy
for response generation, (Tu et al., 2022) incorporated commonsense knowledge and a mix of response strategies into the framework of emotional
support conversation. (Cheng et al., 2022) put forward the concept of look-ahead strategy planning,
a method designed to select strategies that could



2


yield the best long-term effects in emotional support dialogue. In a further advancement, (Peng
et al., 2022b) explored the selection of appropriate
strategies based on the feedback from the conversation seeker. More recently (Zhao et al., 2023)
addressed the challenge of performing a smooth
transition in an utterance level based on semantics, emotions and strategies embedded in each
utterance. More closely related to our research,
(Zheng et al., 2023b) introduced a synthetic dataset
with richer annotations and experimented with fine
tuning llama models for this task using parameter
efficient methods and showed that it outperforms
previous work.


**2.2** **Large Language Models’ Behavior in**
**Long-Context Scenarios**


The interaction of large language models (LLMs)
with long-context scenarios has been a subject of
considerable research interest and is particularly
relevant to this work. (Krishna et al., 2022) observed that in moderately-sized Transformer language models, the quality of neural generation
tends to deteriorate when dealing with long contexts. In a study focused on long-context models,
(Sun et al., 2021) reported that while extended contexts do enhance the prediction accuracy for a limited set of tokens, the overall improvement remains
marginal. Further exploring this domain, (Qin et al.,
2022) conducted an analysis on the performance
of efficient Transformers across a range of longcontext downstream NLP tasks. Their findings
reveal a recency bias in long-context Transformers, indicating that these models do not effectively
leverage long-range context. In a recent study (Liu
et al., 2023) revealed "lost in the middle" effect
in SOTA LLM models which indicates that these
models can overlook the tokens in the middle of the
input. As a subsequent study, researchers showed
that instruction fine-tuned versions of these models still overlook the middle and tail of the input
prompt, but this happens less than pre-trained models (Wu et al., 2023).


**2.3** **Steering Language Models**


The ability to steer language models (LMs) towards
desired behaviors has become increasingly important, particularly for applications requiring alignment with human preferences or specific conversational strategies. Recent research has explored various methods for achieving this steerability, ranging
from fine-tuning and prompt engineering to more



direct manipulation of model activations. (Turner
et al., 2023) introduces a lightweight method for
model control that directly modifies the activations
of LMs during inference. (Alves et al., 2023) explores the potential of steering LMs in the domain
of machine translation. By leveraging both finetuning and in-context learning, this work demonstrates how LMs can be guided to adhere to specific linguistic or stylistic preferences. More relevant to our work, Dong et al. (2023) proposes a
novel approach for steering language models using
attribute-conditioned supervised fine-tuning (SFT).
By conditioning models on desired attributes during the training process. Our approach, inspired by
this work and our proposed attention-based adherence signal (SRA) tries to tackle this steerability
challenge in the domain of emotional support conversations.


**3** **Preliminaries**


**3.1** **ESConv Dataset**


Our research leverages the Emotional Support Conversation dataset, ESConv (Liu et al., 2021), which
is notably characterized by its inclusion of long conversations, averaging 30 turns per dialogue. This
aspect is of paramount importance to our work,
as our analysis specifically targets the dynamics
of extended dialogues in emotional support contexts. In these interactions, individuals seeking
support (seekers) engage with others (supporters)
who assist them in navigating through challenging emotional states. The supporters’ responsibilities encompass recognizing the seekers’ problems,
providing consolation, and suggesting actionable
solutions to address their concerns according to a
predefined strategy. Appendix A.1 summarizes the
statistics of this dataset and it’s key features.


**3.2** **Transformers and Auto Regressive**
**Language Models**


Given a sequence of input embeddings _{em}_ _[L]_ _m_ =1 [in]
_R_ _[d]_, where _L_ is the length of the input sequence, a
transformer language model with _M_ layers and _H_
attention heads processes each embedding _em_ . At
each layer, the model transforms the embeddings
into their corresponding query, key, and value vectors in _R_ _[d/H]_ as shown in equation 1:



3


_qm_ = _W_ _[q]_ _em,_

_km_ = _W_ _[k]_ _em,_

_vm_ = _W_ _[v]_ _em,_ (1)


where _W_ _[q]_ _, W_ _[k]_ _, W_ _[v]_ _∈_ _R_ _[d/H][×][d]_ are learnable
matrices. We will then use these vectors to calculate attention weights over previous tokens (equation 2) where _h_ is the corresponding attention head.



_lmn_ _[h]_ [=]




_⟨qm_ _[h]_ _[, k]_ _n_ _[h][⟩][,]_ if _m ≥_ _n,_
(2)
_−∞,_ otherwise _,_



We will then apply a scaled softmax normalization to calculate the final attention weights _a_ _[h]_ _m,n_ [as]
in equation 3


exp        - _lm,n_ _[h]_ _[/]_ ~~�~~ _d/H_        _a_ _[h]_ _m,n_ [=]    - _Li_ =1 [exp]    - _lm,i_ _[h]_ _[/]_ ~~�~~ _d/H_    - (3)


The attention weights will be used to calculate
the final output embedding _o_ _[h]_ _m,n_ [at position] _[ m]_ [ for]
head _h_ (equation 4)



To test this hypothesis, **we introduce the metric**
**"Strategy Relevant Attention (SRA)".** **This met-**
**ric is designed to measure the degree to which**
**the tokens generated by the model are focused**
**on** **the** **strategy-relevant** **tokens** **present** **in** **the**
**input** . The core objective is to build a prompting
template that consistently maintain attention on the
strategic aspects of the dialogue over time. By
quantifying the model’s adherence to the prompted
strategy, this metric serves as a critical tool in assessing the effectiveness of different models in following strategic directions throughout the conversation.


**4.1** **Strategy Relevant Attention**


Informed by the concept of attention mechanisms,
we hypothesise that the level of attention paid to
strategy-centric tokens could be a pivotal factor in
determining the model’s proficiency in adhering
to the set strategy, although this remains to be empirically validated. To quantify this assumption,
we aggregate the attention weights of the strategy
relevant tokens over all heads and all layers for the
generated response tokens.
Let’s assume that the strategy relevant tokens
span from token _Sb_ to _Se_ and the response tokens
generated by the model span from token _L_ + 1 to
token _L_ + _R_ where _R_ is the length of the response
tokens. We can define the attention weight matrix
as _A_ _∈_ _R_ _[M]_ _[×][H][×][R][×][L]_ ( _M_ being number of attention layers and _H_ being the number of attention
heads) in which each element represents the attention of a response token over a prompt token in a
specific head and layer of the LLM following the
equation 3. Equation 5 formulates Strategy Relevant Attention ( _SRA_ ) as the aggregate attention of
response tokens on the strategy relevant tokens.




_o_ _[h]_ _m,n_ [=]


**4** **Methodology**



_L_


_a_ [(] _m,n_ _[h]_ [)] _[v]_ _n_ [(] _[h]_ [)] (4)
_n_ =1



When we attempted to force the model to follow
specific strategies using a standard prompt, we noticed a trend: as the conversation extended, the
model’s responses became increasingly indifferent
to the system prompt, particularly to the prompted
strategy. Specifically, the model began to generate
very general responses, regardless of what the specified strategy was. This tendency to drift towards
generic responses irrespective of the strategy input
suggests a diminishing sensitivity to the strategic
nuances as the dialogue progresses.
Inspired by prior research investigating the impact of token positioning within prompts (Liu et al.,
2023), (Wu et al., 2023), we formulated a hypothesis concerning the behavior of large language models in extended dialogues. We hypothesize that as
the context length increases, the model’s attention
to tokens related to the prompted strategy decreases.
This diminishing focus could result in a drift towards less specific and more generalized responses
as the conversation progresses.



For the baseline, we adhered to the standard prompt
template as proposed by the Llama model developers (Touvron et al., 2023). This involves incorporating the strategy into the system message of the



_H_


_Am,h,r,l,_

_h_ =1



1
_SRA_ _[agg]_ _r,l_ [=]
_MH_



_M_



_m_ =1



_SRA_ ¯ _[agg]_ _r,l_ _[∈]_ [R]


(5)



_Se_



_l_ = _Sb_



1
_SRA_ =
_|Se −_ _Sb| × R_


**4.2** **Prompting Baselines**



_R_



_r_ =1



4


Figure 2: Left: average accuracy of the strategy following for each model with respect to the turn of the conversation,
Right: average SRA of the responses with respect to the turn of the conversation



|Model|Accuracy|Log-SRA|
|---|---|---|
|llama3-8b-instruct_standard<br>llama3-8b-instruct_c5hf<br>llama3-8b-instruct_c3hf<br>llama3-8b-instruct_c5hl<br>llama3-8b-instruct_c3hl<br>llama3-8b-instruct_c1hf<br>llama3-8b-instruct_c1hl|0.594<br>0.658<br>0.711<br>0.736<br>0.798<br>0.811<br>0.821|-6.916<br>-6.607<br>-6.337<br>-6.711<br>-6.549<br>**-5.758**<br>-6.082|
|llama3-8b-instruct_ours|**0.940**|-5.760|
|llama2-7b-chat_standard<br>llama2-7b-chat_c5hf<br>llama2-7b-chat_c5hl<br>llama2-7b-chat_c3hf<br>llama2-7b-chat_c3hl<br>llama2-7b-chat_c1hl<br>llama2-7b-chat_c1hf|0.144<br>0.178<br>0.202<br>0.294<br>0.295<br>0.715<br>0.765|-7.294<br>-6.802<br>-6.781<br>-6.394<br>-6.504<br>-6.164<br>**-6.112**|
|llama2-7b-chat_ours|**0.933**|-6.126|


Table 1: Log-SRA and strategy following accuracy of
our proposed models versus the baselines. For our models we use the standard prompting template.


input prompt, followed by the conversation history
up to the last message from the emotional support
seeker. In contrast, we also design 6 other prompt
templates as described in figure 3. These variations
include maintaining only 1, 3, or 5 of the most
recent messages in the user/assistant message section of the prompt and relocating the remainder of
the conversation history to either the beginning or
the end of the system message resulting in _c1_hf,_
_c1_hl, c3_hf, c3_hl, c5_hf, c5_hl_ templates. This alteration aims to test the impact of prompt structure
on the model’s attention to strategy guidelines in
extended dialogues. To create a follow-up response
in the conversation using a particular strategy, we



incorporate the _situation_ from the original ESConv
dataset (it is a short summary of the emotional
challenge the help seeker is dealing with), _strat-_
_egy_ which is the strategy that the help seeker is
supposed to follow in the next utterance, _strategy_
_description_ which is the definition of the strategy [2],
and all utterances into the prompt template. We
then feed the resulting sequence into the model and
generate the next utterance.


Figure 3: Six experimental prompt templates to measure
SRA with respect to the position of strategy guidelines
inside the prompt.


**4.3** **Extended ESConv Dataset**


The ESConv dataset initially categorizes the supporter’s conversational strategies, identifying eight
types, such as questioning, reflecting feelings, and
providing suggestions. However, our study seeks
to explore the intricacies of emotional support with
a more granular approach. Taking inspiration from
the study by (Zheng et al., 2023b) which developed


2full list of strategies and their definitions can be found in
appendix A.2



5


|Number of dialogs|1,297|
|---|---|
|Number of strategy conditioned<br>continuations|41,822|
|min conversation history length|5|
|max conversation history length|23|
|avg conversation history length|11.76|
|train/test/validation split|1147 / 100 / 50 conversations|
|train/test/validation examples|36,923 / 3,292 / 1,607|


Table 2: Statistics of our proposed extended ESconv
dataset


a more detailed method for categorizing support
strategies, we have decided to use this advanced
classification in our study. We’ve detailed each
strategy along with a description of the strategy
and more details about this dataset in appendix
A.2. Using these new categories, **we** **expanded**
**the ESConv dataset into several variations for**
**just one turn conditioned on multiple strategies** .
We picked a random conversation from the dataset
and split it at a random point between the 5th and
23th turn. We chose these points to make sure we
continued the conversation in the most appropriate spots. For instance, it wouldn’t make sense
to start _Collaborative Planning_ when someone is
just saying goodbye, or to use _Reflective Statement_
when just greeting. We always split the conversation after the person seeking help has spoken,
allowing the model to take over as the supporter.
Then, with a specific model and a prompting template, **we** **carried** **the** **conversation** **forward** **by**
**one turn** using some of the 15 support strategies
(Zheng et al., 2023b) mentioned. This creates various strategy conditioned single-turn continuations
of the conversations. However, we couldn’t try
out every single combination because of computing constraints. We hold out 100 conversations for
testing different hypothesises. Table 2 shows the
statistics of our proposed extended dataset.


**4.4** **Training a Steerable Model**


Informed by our proposed SRA metric, we selected the prompting baseline with the highest SRA
(c1_hf) and used llama2-13b-chat model to generate the Extended ESConv dataset, as discussed in
4.3. We fine-tuned _Llama2-7b-chat_ and _Llama3-_
_8b-instruct_ models using the LoRA method (Hu
et al., 2021), focusing exclusively on the last utterance’s strategy-conditioned continuations within
the standard prompting setup. This approach enables the model to prioritize the system prompt
while generating new utterances. Our objective
is to enhance the model’s attention to the system



prompt, thereby increasing its steerability in this
setup. We fine-tuned the model on a single A100
GPU, utilizing the default training configurations
of base models with a cumulative batch size of
64 and a cosine learning rate schedule with hard
restarts for 5 epochs. We mask the conversation
history for loss calculation and only measure the
negative log-likelihood on the last utterance. Also,
followed by the convention set by the LoRA paper
we used alpha of 256 twice the size of rank 128 for
the adaptors.


**4.5** **Strategy Classifier**


We utilize the same dataset provided in 4.4 to train
a RoBERTa-large sequence classifier, designed to
categorize the strategy employed in a single response. The model is trained on pairs of response
and prompted strategy from our best performing
prompting baseline. Note that this is a weakly labeled dataset as the responses might not well follow
the prompted strategy. Based on human annotation
on a held-out dataset of 1000 utterance samples
from our test set, the trained classifier achieves an
accuracy of 93.6%. More details on the performance of this model and it’s error analysis can be
found in appendix E. This classifier is trained to
automatically assess the strategy adherence of different models. The model is trained for 5 epochs
using a batch size of 128 on a single A100 GPU.
We also perform an extensive qualitative and quantitative analysis on the predictability of different
model responses in appendix D.


**5** **Experimental Setup and Results**


As discussed in 4.3, we hold out 100 conversations
for experiments and tests. We perform the experiments discussed in this section on these 100 conversations which haven’t been seen by our fine-tuned
models during training. For generating responses
we set the decoding strategy to sampling with _top_p_
of 0.9 and _temperature_ of 0.7 for all of the models.


**5.1** **How does SRA correlate with strategy**
**adherence?**


In this section, we aim to test our hypothesis regarding the correlation between the SRA metric
and the steerability of the model in strategy adherence. Specifically, **we hypothesize that the SRA**
**metric** **quantifies** **the** **extent** **to** **which** **a** **model,**
**identical in parameters to another, allocates at-**
**tention to strategy-specific tokens, thereby indi-**
**cating its proficiency in adhering to the intended**



6


Figure 4: Correlation of the SRA metric with the accuracy of the strategy following for llama2-7b-chat finetuned model vs. baselines. Y-axis is in logarithmic
scale.


**strategy.** We follow the approach outlined in section 4.3, use llama2-7b-chat and extend the test
set conversations using all of the prompting baselines. Note that for our fine-tuned model we also
use the standard prompt template. To test this hypothesis, we utilize the strategy classifier trained
in 4.5 to evaluate the strategies employed in the
generated responses by each model. We compare
our fine-tuned model against the baseline prompts
given the same model size (llama2-7b-chat). Subsequently, we measure how closely the accuracy of
strategy adherence correlates with the SRA metric.
Figure 4 illustrates the results. We observe that
the SRA metric has a Pearson correlation of 0.94
with the correctness of the strategies followed by
the models, indicating a significant correlation. We
also perform the same experiment using llama3-8binstruct and observed the same strong correlation
between strategy adherence and SRA of 0.8.


**5.2** **How does steerability of the model change**
**in depth of the conversations?**


We use the strategy classifier in 4.5 to compare
the accuracy of the strategy adherence of our proposed models versus the baselines. We compare
our fine-tuned llama3-8b-instruct and llama2-7bchat with baselines explained in section 4.2 over
both SRA metric and strategy adherence accuracy.
Note again that for fine-tuned models we use the
standard prompting. We summarize the results in
table 1. Our fine-tuned models consistently outperforms the baselines with an **improvement** **of**
**78.9% over the llama-2 base model and 37.6%**
over llama-3 base model in strategy adherence ac


curacy and gains significantly more SRA after finetuning. It is also worth mentioning that llama38b-instruct model is significantly improved over
llama2-7b-chat in steerability as it outperforms it
by 45%.
Figure 2 illustrates the amount of SRA and average accuracy of the strategy following with respect
to the turn of the conversation for llama2-7b-chat
and it’s corresponding baselines. We also provide
the results for the same set of experiments over
llama3-8b-instruct in appendix F. We observe that
the baseline prompts informed by our SRA metric
are able to maintain a high SRA and strategy adherence as we go deeper into the conversation and
our proposed model outperforms the baselines and
maintains a robust SRA and adherence throughout
the conversation. Also the _c1_hf_ prompt achieves
the most stable strategy following behavior compared to the other baselines. More importantly, we
observe that our fine-tuned model, despite maintaining the same prompting template as the standard
baseline, significantly achieves higher SRA and
strategy following accuracy during the conversation.


**5.3** **Does better strategy following deteriorate**
**conversationality of the model?**


To this end, we found out that we can improve
strategy adherence or steerability of the model by
designing more efficient prompts or fine-tuning the
model with synthetic data to enforce the model to
attend more to the strategy directions. However,
**it is important to evaluate other dimensions of**
**performance and make sure that the resulting**
**models are not less coherent, natural and con-**
**sistent.** Note that since we are forcing the models
to blindly follow different strategies at different
stages of the conversation, we can’t simply compare the helpfulness of two model responses as the
helpfulness is not the relevant metric here since the
followed strategy might not be optimal. Therefore,
aside from the strategy following capability we try
to measure coherence, naturalness and the quality
of the responses.


**5.3.1** **Model based evaluation results**


We compare our fine-tuned model’s responses with
it’s initial base model before fine-tuning. We generate 500 random strategy-conditioned utterances
following the same approach as section 4.3 from
the held out 100 conversations using llama2-7bchat, llama3-8b-instruct and their fine-tuned varia


7


Win(%) Tie(%) Lose(%)
Llama2-7b-chat
**74.12** 18.63 7.25
(ours vs standard)

Llama3-8b-instruct
**50.78** 35.29 13.92
(ours vs standard)


Table 3: Head to head comparison of our fine-tuned
models with their base models.


tions using standard prompting. We use gpt-4o
as the judge LLM. The prompt template along
with some examples are shown in appendix C. We
also mitigate possible positional bias discussed in
(Zheng et al., 2023a) and alternate between model
responses and call it a tie in case of mismatched
judges. Table 3 shows the wining rate of our proposed llama-2 and llama-3 fine-tuned models versus the initial models. Both of our llama-2 and
llama-3 models significantly win over baselines.
This highlights that our approach not only enhances
the strategy adherence of the base models, but also
maintains consistency, coherence and quality.


**5.3.2** **Human evaluation results**


In addition to model based analyses, we also ask human annotators to score how good different models
adhere to strategies while staying coherent, consistent and natural. We generate responses to a
given conversation history using two distinct models picked among _c1_hf_, _c3_hf_, _standard_ and our
fine-tuned version with standard prompting and
use llama2-7b-chat as the assistant. Same as section 5.3.1, we generate 150 head to head strategyconditioned continuation comparisons. We then
compute the SRA for both responses, which serves
as a preliminary quantitative measure of strategic
alignment. Subsequently, two human annotators
are tasked with evaluating the responses, assigning
scores based on the perceived effectiveness of each
response in following the outlined strategy and being coherent, consistent and natural. Finally, we
measure the Pearson correlation between the human score and the difference between SRA metrics
of the two responses. Details of the annotation task
are explained in appendix B. As depicted in figure
5, we observe a high Pearson correlation of 0.80
and 0.82 between the each of the annotators’ scores
and the difference in SRA for the two responses
with Krippendorff’s Alpha agreement of 0.91 between the annotators. This result, highlights the
effectiveness of our proposed SRA metric in measuring the adherence of the models to the prompted



strategy. We also observe a 79.41% win-rate of our
fine-tuned model versus other baselines.


Figure 5: y-axis shows the normalized score of the
annotators for each annotation task and x-axis shows
the normalized log of difference between responses in
the annotation task.


**6** **Conclusion**


In this study, we addressed the challenges that large
language models (LLMs) face when engaging in
long-form conversational setups, specifically focusing on maintaining consistent strategy adherence
in emotional support conversations. We introduced
the Strategy-Relevant Attention (SRA) metric to
monitor how effectively models attend to strategic
directives throughout interactions. Our findings
show that the Llama-2 and Llama-3 models struggle to consistently follow the intended strategies,
particularly as conversations progress.

Leveraging the insights from the SRA metric,
we explored various prompting techniques to enhance strategy adherence and constructed a synthetic, strategy-conditioned extension of the ESConv dataset. Our fine-tuned models, trained on
this extended dataset, demonstrated significant improvements in steerability or strategy adherence
compared to baseline models.

Furthermore, through model-based and human
evaluations, we validated that our fine-tuned models not only excel in maintaining strategic focus
but also preserve key conversational qualities such
as naturalness, relevance, consistency, and coherence. These results highlight the potential of our
approach in steering LLMs more effectively in emotionally supportive dialogues and set the stage for
future work in refining long-horizon conversational
planning.



8


**7** **Limitations**


While our research on the Strategy-Relevant Attention (SRA) metric demonstrates significant advancements in conversational AI, it is not without
limitations. Firstly, the generalizability of SRA
across diverse LLM architectures and configurations remains to be fully explored. Additionally,
the effectiveness of SRA in scenarios beyond emotional support conversations, especially in more
complex or nuanced interactions, requires further
investigation. Also, in this work we only focus on
the ability of these models for following strategy.
Although this is an important skill in a conversational agent, but we do not study the helpfulness
or effectiveness of different strategies at different
stages of the conversation and leave it to the future
work.


**8** **Ethical Considerations**


Given that the LLMs are designed to engage in emotionally sensitive conversations, it is crucial to ensure user privacy and confidentiality. All data used
for training and evaluation should be anonymized,
with personal identifiers removed. This is mitigated
by the authors of the ESConv dataset and since we
are extending the same dataset, we do not encounter
such challenges. Also, since the model engages
with users seeking emotional support, it must be
carefully designed to avoid causing harm. It is
essential to ensure that the model’s responses are
empathetic, supportive, and non-triggering. Continuous monitoring, human-in-the-loop oversight, and
the inclusion of mental health professionals in the
evaluation process are necessary to maintain the
emotional safety of users. This work only focuses
on strategy adherence and does not consider the
planning aspect of the emotional support task. It
is also important that the users interacting with the
model be made aware that they are engaging with
an AI system rather than a human. Clear communication about the system’s capabilities, limitations,
and the nature of the support it can provide is essential. Informed consent should be obtained, ensuring
users understand the model’s role, data usage policies, and the scope of emotional support it offers.


**References**


Duarte M. Alves, Nuno M. Guerreiro, Joao Alves, José P.
Pombal, Ricardo Rei, Jos’e G. C. de Souza, Pierre
Colombo, and André Martins. 2023. [Steering large](https://api.semanticscholar.org/CorpusID:264405904)



[language models for machine translation with finetun-](https://api.semanticscholar.org/CorpusID:264405904)
[ing and in-context learning.](https://api.semanticscholar.org/CorpusID:264405904) _ArXiv_, abs/2310.13448.


Yi Cheng, Wenge Liu, Wenjie Li, Jiashuo Wang, Ruihui
Zhao, Bang Liu, Xiaodan Liang, and Yefeng Zheng.
2022. [Improving multi-turn emotional support dia-](https://api.semanticscholar.org/CorpusID:252780132)
[logue generation with lookahead strategy planning.](https://api.semanticscholar.org/CorpusID:252780132)
In _Conference on Empirical Methods in Natural Lan-_
_guage Processing_ .


Yi Dong, Zhilin Wang, Makesh Narsimhan Sreedhar,
Xianchao Wu, and Oleksii Kuchaiev. 2023. [Steerlm:](https://api.semanticscholar.org/CorpusID:263830508)
[Attribute conditioned sft as an (user-steerable) alter-](https://api.semanticscholar.org/CorpusID:263830508)
[native to rlhf.](https://api.semanticscholar.org/CorpusID:263830508) _ArXiv_, abs/2310.05344.


Abhimanyu Dubey, Abhinav Jauhri, Abhinav Pandey,
Abhishek Kadian, Ahmad Al-Dahle, Aiesha Letman,
Akhil Mathur, Alan Schelten, Amy Yang, Angela
Fan, Anirudh Goyal, Anthony Hartshorn, Aobo Yang,
Archi Mitra, Archie Sravankumar, Artem Korenev,
Arthur Hinsvark, Arun Rao, Aston Zhang, Aurelien
Rodriguez, Austen Gregerson, Ava Spataru, Baptiste Roziere, Bethany Biron, Binh Tang, Bobbie
Chern, Charlotte Caucheteux, Chaya Nayak, Chloe
Bi, Chris Marra, Chris McConnell, Christian Keller,
Christophe Touret, Chunyang Wu, Corinne Wong,
Cristian Canton Ferrer, Cyrus Nikolaidis, Damien Allonsius, Daniel Song, Danielle Pintz, Danny Livshits,
David Esiobu, Dhruv Choudhary, Dhruv Mahajan,
Diego Garcia-Olano, Diego Perino, Dieuwke Hupkes,
Egor Lakomkin, Ehab AlBadawy, Elina Lobanova,
Emily Dinan, Eric Michael Smith, Filip Radenovic,
Frank Zhang, Gabriel Synnaeve, Gabrielle Lee, Georgia Lewis Anderson, Graeme Nail, Gregoire Mialon, Guan Pang, Guillem Cucurell, Hailey Nguyen,
Hannah Korevaar, Hu Xu, Hugo Touvron, Iliyan
Zarov, Imanol Arrieta Ibarra, Isabel Kloumann, Ishan
Misra, Ivan Evtimov, Jade Copet, Jaewon Lee, Jan
Geffert, Jana Vranes, Jason Park, Jay Mahadeokar,
Jeet Shah, Jelmer van der Linde, Jennifer Billock,
Jenny Hong, Jenya Lee, Jeremy Fu, Jianfeng Chi,
Jianyu Huang, Jiawen Liu, Jie Wang, Jiecao Yu,
Joanna Bitton, Joe Spisak, Jongsoo Park, Joseph
Rocca, Joshua Johnstun, Joshua Saxe, Junteng Jia,
Kalyan Vasuden Alwala, Kartikeya Upasani, Kate
Plawiak, Ke Li, Kenneth Heafield, Kevin Stone,
Khalid El-Arini, Krithika Iyer, Kshitiz Malik, Kuenley Chiu, Kunal Bhalla, Lauren Rantala-Yeary, Laurens van der Maaten, Lawrence Chen, Liang Tan, Liz
Jenkins, Louis Martin, Lovish Madaan, Lubo Malo,
Lukas Blecher, Lukas Landzaat, Luke de Oliveira,
Madeline Muzzi, Mahesh Pasupuleti, Mannat Singh,
Manohar Paluri, Marcin Kardas, Mathew Oldham,
Mathieu Rita, Maya Pavlova, Melanie Kambadur,
Mike Lewis, Min Si, Mitesh Kumar Singh, Mona
Hassan, Naman Goyal, Narjes Torabi, Nikolay Bashlykov, Nikolay Bogoychev, Niladri Chatterji, Olivier
Duchenne, Onur Çelebi, Patrick Alrassy, Pengchuan
Zhang, Pengwei Li, Petar Vasic, Peter Weng, Prajjwal Bhargava, Pratik Dubal, Praveen Krishnan,
Punit Singh Koura, Puxin Xu, Qing He, Qingxiao
Dong, Ragavan Srinivasan, Raj Ganapathy, Ramon
Calderer, Ricardo Silveira Cabral, Robert Stojnic,
Roberta Raileanu, Rohit Girdhar, Rohit Patel, Romain Sauvestre, Ronnie Polidoro, Roshan Sumbaly,



9


Ross Taylor, Ruan Silva, Rui Hou, Rui Wang, Saghar
Hosseini, Sahana Chennabasappa, Sanjay Singh,
Sean Bell, Seohyun Sonia Kim, Sergey Edunov,
Shaoliang Nie, Sharan Narang, Sharath Raparthy,
Sheng Shen, Shengye Wan, Shruti Bhosale, Shun
Zhang, Simon Vandenhende, Soumya Batra, Spencer
Whitman, Sten Sootla, Stephane Collot, Suchin Gururangan, Sydney Borodinsky, Tamar Herman, Tara
Fowler, Tarek Sheasha, Thomas Georgiou, Thomas
Scialom, Tobias Speckbacher, Todor Mihaylov, Tong
Xiao, Ujjwal Karn, Vedanuj Goswami, Vibhor
Gupta, Vignesh Ramanathan, Viktor Kerkez, Vincent
Gonguet, Virginie Do, Vish Vogeti, Vladan Petrovic, Weiwei Chu, Wenhan Xiong, Wenyin Fu, Whitney Meers, Xavier Martinet, Xiaodong Wang, Xiaoqing Ellen Tan, Xinfeng Xie, Xuchao Jia, Xuewei
Wang, Yaelle Goldschlag, Yashesh Gaur, Yasmine
Babaei, Yi Wen, Yiwen Song, Yuchen Zhang, Yue
Li, Yuning Mao, Zacharie Delpierre Coudert, Zheng
Yan, Zhengxing Chen, Zoe Papakipos, Aaditya Singh,
Aaron Grattafiori, Abha Jain, Adam Kelsey, Adam
Shajnfeld, Adithya Gangidi, Adolfo Victoria, Ahuva
Goldstand, Ajay Menon, Ajay Sharma, Alex Boesenberg, Alex Vaughan, Alexei Baevski, Allie Feinstein,
Amanda Kallet, Amit Sangani, Anam Yunus, Andrei Lupu, Andres Alvarado, Andrew Caples, Andrew Gu, Andrew Ho, Andrew Poulton, Andrew
Ryan, Ankit Ramchandani, Annie Franco, Aparajita Saraf, Arkabandhu Chowdhury, Ashley Gabriel,
Ashwin Bharambe, Assaf Eisenman, Azadeh Yazdan, Beau James, Ben Maurer, Benjamin Leonhardi,
Bernie Huang, Beth Loyd, Beto De Paola, Bhargavi
Paranjape, Bing Liu, Bo Wu, Boyu Ni, Braden Hancock, Bram Wasti, Brandon Spence, Brani Stojkovic,
Brian Gamido, Britt Montalvo, Carl Parker, Carly
Burton, Catalina Mejia, Changhan Wang, Changkyu
Kim, Chao Zhou, Chester Hu, Ching-Hsiang Chu,
Chris Cai, Chris Tindal, Christoph Feichtenhofer, Damon Civin, Dana Beaty, Daniel Kreymer, Daniel Li,
Danny Wyatt, David Adkins, David Xu, Davide Testuggine, Delia David, Devi Parikh, Diana Liskovich,
Didem Foss, Dingkang Wang, Duc Le, Dustin Holland, Edward Dowling, Eissa Jamil, Elaine Montgomery, Eleonora Presani, Emily Hahn, Emily Wood,
Erik Brinkman, Esteban Arcaute, Evan Dunbar, Evan
Smothers, Fei Sun, Felix Kreuk, Feng Tian, Firat
Ozgenel, Francesco Caggioni, Francisco Guzmán,
Frank Kanayet, Frank Seide, Gabriela Medina Florez, Gabriella Schwarz, Gada Badeer, Georgia Swee,
Gil Halpern, Govind Thattai, Grant Herman, Grigory
Sizov, Guangyi, Zhang, Guna Lakshminarayanan,
Hamid Shojanazeri, Han Zou, Hannah Wang, Hanwen Zha, Haroun Habeeb, Harrison Rudolph, Helen Suk, Henry Aspegren, Hunter Goldman, Ibrahim
Damlaj, Igor Molybog, Igor Tufanov, Irina-Elena
Veliche, Itai Gat, Jake Weissman, James Geboski,
James Kohli, Japhet Asher, Jean-Baptiste Gaya,
Jeff Marcus, Jeff Tang, Jennifer Chan, Jenny Zhen,
Jeremy Reizenstein, Jeremy Teboul, Jessica Zhong,
Jian Jin, Jingyi Yang, Joe Cummings, Jon Carvill,
Jon Shepard, Jonathan McPhie, Jonathan Torres,
Josh Ginsburg, Junjie Wang, Kai Wu, Kam Hou
U, Karan Saxena, Karthik Prasad, Kartikay Khandelwal, Katayoun Zand, Kathy Matosich, Kaushik



Veeraraghavan, Kelly Michelena, Keqian Li, Kun
Huang, Kunal Chawla, Kushal Lakhotia, Kyle Huang,
Lailin Chen, Lakshya Garg, Lavender A, Leandro
Silva, Lee Bell, Lei Zhang, Liangpeng Guo, Licheng
Yu, Liron Moshkovich, Luca Wehrstedt, Madian
Khabsa, Manav Avalani, Manish Bhatt, Maria Tsimpoukelli, Martynas Mankus, Matan Hasson, Matthew
Lennie, Matthias Reso, Maxim Groshev, Maxim
Naumov, Maya Lathi, Meghan Keneally, Michael L.
Seltzer, Michal Valko, Michelle Restrepo, Mihir
Patel, Mik Vyatskov, Mikayel Samvelyan, Mike
Clark, Mike Macey, Mike Wang, Miquel Jubert Hermoso, Mo Metanat, Mohammad Rastegari, Munish Bansal, Nandhini Santhanam, Natascha Parks,
Natasha White, Navyata Bawa, Nayan Singhal, Nick
Egebo, Nicolas Usunier, Nikolay Pavlovich Laptev,
Ning Dong, Ning Zhang, Norman Cheng, Oleg
Chernoguz, Olivia Hart, Omkar Salpekar, Ozlem
Kalinli, Parkin Kent, Parth Parekh, Paul Saab, Pavan Balaji, Pedro Rittner, Philip Bontrager, Pierre
Roux, Piotr Dollar, Polina Zvyagina, Prashant Ratanchandani, Pritish Yuvraj, Qian Liang, Rachad Alao,
Rachel Rodriguez, Rafi Ayub, Raghotham Murthy,
Raghu Nayani, Rahul Mitra, Raymond Li, Rebekkah
Hogan, Robin Battey, Rocky Wang, Rohan Maheswari, Russ Howes, Ruty Rinott, Sai Jayesh Bondu,
Samyak Datta, Sara Chugh, Sara Hunt, Sargun
Dhillon, Sasha Sidorov, Satadru Pan, Saurabh Verma,
Seiji Yamamoto, Sharadh Ramaswamy, Shaun Lindsay, Shaun Lindsay, Sheng Feng, Shenghao Lin,
Shengxin Cindy Zha, Shiva Shankar, Shuqiang
Zhang, Shuqiang Zhang, Sinong Wang, Sneha Agarwal, Soji Sajuyigbe, Soumith Chintala, Stephanie
Max, Stephen Chen, Steve Kehoe, Steve Satterfield,
Sudarshan Govindaprasad, Sumit Gupta, Sungmin
Cho, Sunny Virk, Suraj Subramanian, Sy Choudhury,
Sydney Goldman, Tal Remez, Tamar Glaser, Tamara
Best, Thilo Kohler, Thomas Robinson, Tianhe Li,
Tianjun Zhang, Tim Matthews, Timothy Chou, Tzook
Shaked, Varun Vontimitta, Victoria Ajayi, Victoria
Montanez, Vijai Mohan, Vinay Satish Kumar, Vishal
Mangla, Vítor Albiero, Vlad Ionescu, Vlad Poenaru,
Vlad Tiberiu Mihailescu, Vladimir Ivanov, Wei Li,
Wenchen Wang, Wenwen Jiang, Wes Bouaziz, Will
Constable, Xiaocheng Tang, Xiaofang Wang, Xiaojian Wu, Xiaolan Wang, Xide Xia, Xilun Wu, Xinbo
Gao, Yanjun Chen, Ye Hu, Ye Jia, Ye Qi, Yenda Li,
Yilin Zhang, Ying Zhang, Yossi Adi, Youngjin Nam,
Yu, Wang, Yuchen Hao, Yundi Qian, Yuzi He, Zach
Rait, Zachary DeVito, Zef Rosnbrick, Zhaoduo Wen,
Zhenyu Yang, and Zhiwei Zhao. 2024. [The llama 3](https://arxiv.org/abs/2407.21783)
[herd of models.](https://arxiv.org/abs/2407.21783) _Preprint_, arXiv:2407.21783.


Mahshid Hosseini and Cornelia Caragea. 2021. [It takes](https://api.semanticscholar.org/CorpusID:233238086)
two to empathize: [One to seek and one to provide.](https://api.semanticscholar.org/CorpusID:233238086) In
_AAAI Conference on Artificial Intelligence_ .


J. Edward Hu, Yelong Shen, Phillip Wallis, Zeyuan
Allen-Zhu, Yuanzhi Li, Shean Wang, and Weizhu
Chen. 2021. Lora: Low-rank [adaptation](https://api.semanticscholar.org/CorpusID:235458009) of large
[language models.](https://api.semanticscholar.org/CorpusID:235458009) _ArXiv_, abs/2106.09685.


Kalpesh Krishna, Yapei Chang, John Wieting, and Mohit Iyyer. 2022. Rankgen: [Improving text generation](https://api.semanticscholar.org/CorpusID:248887396)
[with large ranking models.](https://api.semanticscholar.org/CorpusID:248887396) _ArXiv_, abs/2205.09726.



10


Nelson F. Liu, Kevin Lin, John Hewitt, Ashwin Paranjape, Michele Bevilacqua, Fabio Petroni, and Percy
Liang. 2023. Lost in the [middle:](https://api.semanticscholar.org/CorpusID:259360665) How language
[models use long contexts.](https://api.semanticscholar.org/CorpusID:259360665) _ArXiv_, abs/2307.03172.


Siyang Liu, Chujie Zheng, Orianna Demasi, Sahand
Sabour, Yu Li, Zhou Yu, Yong Jiang, and Minlie
Huang. 2021. Towards [emotional](https://api.semanticscholar.org/CorpusID:235294326) support dialog
[systems.](https://api.semanticscholar.org/CorpusID:235294326) _ArXiv_, abs/2106.01144.


Lenin Medeiros and Tibor Bosse. 2018. [Using crowd-](https://api.semanticscholar.org/CorpusID:49397755)
sourcing for the [development](https://api.semanticscholar.org/CorpusID:49397755) of online emotional
[support agents.](https://api.semanticscholar.org/CorpusID:49397755) In _Practical Applications of Agents_
_and Multi-Agent Systems_ .


Wei Peng, Yue Hu, Luxi Xing, Yuqiang Xie, Yajing Sun,
and Yunpeng Li. 2022a. [Control globally, understand](https://api.semanticscholar.org/CorpusID:248406141)
locally: [A global-to-local hierarchical graph network](https://api.semanticscholar.org/CorpusID:248406141)
[for emotional support conversation.](https://api.semanticscholar.org/CorpusID:248406141) In _International_
_Joint Conference on Artificial Intelligence_ .


Wei Peng, Ziyuan Qin, Yue Hu, Yuqiang Xie, and Yunpeng Li. 2022b. Fado: [Feedback-aware double con-](https://api.semanticscholar.org/CorpusID:253244287)
[trolling network for emotional support conversation.](https://api.semanticscholar.org/CorpusID:253244287)
_Knowl. Based Syst._, 264:110340.


Guanghui Qin, Yukun Feng, and Benjamin Van Durme.
2022. [The nlp task effectiveness of long-range trans-](https://api.semanticscholar.org/CorpusID:246867127)
[formers.](https://api.semanticscholar.org/CorpusID:246867127) _ArXiv_, abs/2202.07856.


Nils Reimers and Iryna Gurevych. 2019. [Sentence-bert:](https://api.semanticscholar.org/CorpusID:201646309)
[Sentence embeddings using siamese bert-networks.](https://api.semanticscholar.org/CorpusID:201646309)
In _Conference on Empirical Methods in Natural Lan-_
_guage Processing_ .


Ashish Sharma, Inna Wanyin Lin, Adam S. Miner,
David C. Atkins, and Tim Althoff. 2021. [Towards](https://api.semanticscholar.org/CorpusID:231639313)
[facilitating empathic conversations in online mental](https://api.semanticscholar.org/CorpusID:231639313)
health support: [A reinforcement learning approach.](https://api.semanticscholar.org/CorpusID:231639313)
_Proceedings of the Web Conference 2021_ .


Ashish Sharma, Adam S. Miner, David C. Atkins, and
Tim Althoff. 2020. [A computational approach to un-](https://api.semanticscholar.org/CorpusID:221761251)
[derstanding empathy expressed in text-based mental](https://api.semanticscholar.org/CorpusID:221761251)
[health support.](https://api.semanticscholar.org/CorpusID:221761251) _ArXiv_, abs/2009.08441.


Simeng Sun, Kalpesh Krishna, Andrew MattarellaMicke, and Mohit Iyyer. 2021. Do [long-range](https://api.semanticscholar.org/CorpusID:237572264)
language models [actually](https://api.semanticscholar.org/CorpusID:237572264) use long-range context?
_ArXiv_, abs/2109.09115.


Hugo Touvron, Louis Martin, Kevin R. Stone, Peter
Albert, Amjad Almahairi, Yasmine Babaei, Nikolay Bashlykov, Soumya Batra, Prajjwal Bhargava,
Shruti Bhosale, Daniel M. Bikel, Lukas Blecher, Cristian Cantón Ferrer, Moya Chen, Guillem Cucurull,
David Esiobu, Jude Fernandes, Jeremy Fu, Wenyin
Fu, Brian Fuller, Cynthia Gao, Vedanuj Goswami,
Naman Goyal, Anthony S. Hartshorn, Saghar Hosseini, Rui Hou, Hakan Inan, Marcin Kardas, Viktor
Kerkez, Madian Khabsa, Isabel M. Kloumann, A. V.
Korenev, Punit Singh Koura, Marie-Anne Lachaux,
Thibaut Lavril, Jenya Lee, Diana Liskovich, Yinghai
Lu, Yuning Mao, Xavier Martinet, Todor Mihaylov,
Pushkar Mishra, Igor Molybog, Yixin Nie, Andrew
Poulton, Jeremy Reizenstein, Rashi Rungta, Kalyan



Saladi, Alan Schelten, Ruan Silva, Eric Michael
Smith, R. Subramanian, Xia Tan, Binh Tang, Ross
Taylor, Adina Williams, Jian Xiang Kuan, Puxin
Xu, Zhengxu Yan, Iliyan Zarov, Yuchen Zhang, Angela Fan, Melanie Kambadur, Sharan Narang, Aurelien Rodriguez, Robert Stojnic, Sergey Edunov, and
Thomas Scialom. 2023. Llama 2: [Open foundation](https://api.semanticscholar.org/CorpusID:259950998)
[and fine-tuned chat models.](https://api.semanticscholar.org/CorpusID:259950998) _ArXiv_, abs/2307.09288.


Quan Tu, Yanran Li, Jianwei Cui, Bin Wang, Jiaxin
Wen, and Rui Yan. 2022. Misc: [A mixed strategy-](https://api.semanticscholar.org/CorpusID:247748640)
[aware model integrating comet for emotional support](https://api.semanticscholar.org/CorpusID:247748640)
[conversation.](https://api.semanticscholar.org/CorpusID:247748640) _ArXiv_, abs/2203.13560.


Alexander Matt Turner, Lisa Thiergart, David S.
Udell, Gavin Leech, Ulisse Mini, and Monte Stuart MacDiarmid. 2023. [Activation addition:](https://api.semanticscholar.org/CorpusID:261049449) Steering language models without optimization. _ArXiv_,
abs/2308.10248.


Xuansheng Wu, Wenlin Yao, Jianshu Chen, Xiaoman
Pan, Xiaoyang Wang, Ninghao Liu, and Dong Yu.
2023. [From language modeling to instruction follow-](https://api.semanticscholar.org/CorpusID:263334329)
ing: [Understanding the behavior shift in llms after](https://api.semanticscholar.org/CorpusID:263334329)
[instruction tuning.](https://api.semanticscholar.org/CorpusID:263334329) _ArXiv_, abs/2310.00492.


Weixiang Zhao, Yanyan Zhao, Shilong Wang, and Bing
Qin. 2023. Transesc: [Smoothing emotional support](https://api.semanticscholar.org/CorpusID:258547321)
conversation via [turn-level](https://api.semanticscholar.org/CorpusID:258547321) state transition. In _An-_
_nual Meeting of the Association for Computational_
_Linguistics_ .


Lianmin Zheng, Wei-Lin Chiang, Ying Sheng, Siyuan
Zhuang, Zhanghao Wu, Yonghao Zhuang, Zi Lin,
Zhuohan Li, Dacheng Li, Eric P. Xing, Haotong
Zhang, Joseph Gonzalez, and Ion Stoica. 2023a.
[Judging llm-as-a-judge with mt-bench and chatbot](https://api.semanticscholar.org/CorpusID:259129398)
[arena.](https://api.semanticscholar.org/CorpusID:259129398) _ArXiv_, abs/2306.05685.


Zhonghua Zheng, Lizi Liao, Yang Deng, and Liqiang
Nie. 2023b. [Building emotional support chatbots in](https://api.semanticscholar.org/CorpusID:261065100)
[the era of llms.](https://api.semanticscholar.org/CorpusID:261065100) _ArXiv_, abs/2308.11584.


**A** **Datasets**


**A.1** **ESConv Dataset Statistics**


Table 4 summarizes some of the key statistics of
the ESConv dataset.

|Category|Total|
|---|---|
|# dialogues<br># utterances<br>avg. length of dialogues<br># strategies|1,053<br>31,410<br>29.8<br>8|



Table 4: Some of the key statistics of the original ESConv dataset



11


**A.2** **Extended ESConv Dataset Statistics**


To create the extended version of the dataset for
training our proposed models, we chose the most
effective prompting template (c1_hf) for strategy
following and generated continuations by randomly
selecting a strategy. To be more specific, we cut
the conversations after "help seeker’s" turn at some
point between 5th and 23th turn of the conversation
for 7b and 13b llama models and somewhere between 5th and 19th turn for 70b model. Afterwards,
we randomly pick strategies with probability of
30% and prompt the model to get the response.
We then postprocess the responses by removing
the indicators of the strategy or any unwanted textual span such as "Here is a response:". Table 5
summarizes the statistics of this dataset.


**A.2.1** **Strategies and their definitions**


In tables 7 and 8 we provide all of the 15 strategies
that we use to extend the dataset along with some
examples of how they might be used. Both strategy
and description will directly be used inside of the
prompt.


**B** **Annotation Task Details**


Figure 6 shows a sample annotation task. Two of
the authors of the paper perform the annotation
task. We simply instruct the annotators with the
following paragraph before starting the annotation:

On the top of each task you
will see a strategy along with it’s
definition. Afterwards you will be
given a conversation between an emotional
supporter (counselor) and a person who
is seeking help. The conversation is
cut at a random spot with help seeker
uttering the last turn. Then you will
see two continuations of the conversation
using the proposed strategy. Your task
is to choose the continuation that best
follows the strategy while maintaining
consistency and coherence with respect
to the conversation history and remains
natural and conversational. You have 8
options for scoring +4 meaning the right
continuation is extremely preferred over
the left continuation and vice versa.
If none of the responses satisfy the
requirement or both of them are perfectly
following the strategy and are consistent
and coherent, choose 0 but if one of them


12



is slightly better lean your score towards
that answer accordingly.


**C** **Model Based Evaluation**


We use the prompt template shown in figure 7.
More specifically, we ask the model to act as an impartial judge and compare the strategy adherence of
the two models while taking into account the consistency, coherence, quality and the response being
natural. The general judging template is adopted
from MT-Bench (Zheng et al., 2023a) paper.
We incorporate conversation histories of two different models, the intended strategy instructions
and the responses by both models into the judge
prompt. We also alternate between the position of
the both models’ responses in the judge prompt and
call the judge twice to make sure we avoid positional bias. The judge will then have to first reason
about which model is potentially better and then
choose either one of them or call it a tie.
Figure 9 illustrates an examples where our proposed llama3-8b-instruct model outperforms the
base model and figure 8 shows an example where
our model loses to the base model because of lack
of natural flow in the response.


**D** **Predictability of the Strategy from the**
**Response**


This section explores the assumption that the effectiveness of a model in following a given strategy
can be quantified by assessing how predictable the
strategy is, given the generated utterance. We hypothesize that there is a direct correlation between
the predictability of the strategy and the model’s
adherence to it. **Although predictability of the re-**
**sponses does not necessarily indicate the adher-**
**ence to the specific strategy, it perfectly assess**
**the ability of different methods in distinguish-**
**ing between strategies when generating the re-**
**sponse.**
To formalize this concept, we utilize Bayes’
rule, a fundamental theorem in probability theory.
Bayes’ rule describes the probability of an event
based on prior knowledge of conditions related
to the event. In our context, it is used to relate
the probability of a strategy _S_ given a generated
response _R_, to the probability of generating a response given a strategy. The rule is formulated
as:


_P_ ( _S|R_ ) = _[P]_ [(] _[R][|][S]_ [)] _[ ×][ P]_ [(] _[S]_ [)] (6)

_P_ ( _R_ )


|model name|number of conversations|number of continuations|min/max turn|
|---|---|---|---|
|llama-7b-chat<br>llama-13b-chat<br>llama-70b-chat|1,297<br>1,297<br>1,297|41,994<br>41,822<br>24,760|5/23<br>5/23<br>5/19|


Table 5: statistics of the extended dialogue dataset


Figure 6: A sample annotation task



Here, _P_ ( _S|R_ ) represents the posterior probability, indicating the likelihood of the strategy _S_ given
the observation of the response _R_ . _P_ ( _R|S_ ) is the
likelihood of generating the response _R_ when following the strategy _S_ . _P_ ( _S_ ) and _P_ ( _R_ ) are the
prior probabilities of the strategy and the response,
respectively.
A high posterior probability, _P_ ( _S|R_ ), suggests
that the response _R_ strongly indicates the use of
strategy _S_, implying effective adherence by the
model to the strategy. Conversely, a low value
indicates weaker adherence to the strategy.


**D.1** **Measuring predictability based on lexical**
**features**


Our first proposal is a baseline model using Bag of
Words Logistic Regression over N-grams to identify lexical differences between different templates’
responses. This model is selected for its simplicity
and interpretability. It allows us to easily understand which words or phrases significantly contribute to the distinctiveness of the responses. The
model is defined as:







_P_ ( _S|R_ ) = _σ_




- _N_

 
_ωi · xi_ + _b_

_i_ =1



(7)



weights assigned to each n-gram, _xi_ are the ngram features extracted from the response, and _b_
is the bias term. We remove English stop words
and words that appear in more than 90% of the responses and then build 2-gram and 3-gram feature
vectors to train the logistic regression model.


**D.2** **Measuring predictability based on**
**semantic features**


To complement the first model and capture deeper
semantic features, we also employ a Sentence Bert
model (Reimers and Gurevych, 2019) for sequence
classification. To be specific, we use _all-mpnet-_
_base-v2_ model which stands on top of the leader
board for the best quality of sentence encodings
over 14 tasks in different domains [3] . This model
provides us with the capability to discern intricate
semantic patterns that might be overlooked by the
simpler lexical predictor. We first employ the Sentence Bert model according to equation 8 where
_R_ is the sequence of response tokens and retrieve
an aggregate embedding for the whole response
(in case of mpnet model we use, it will be a normalized average of the embeddings of all tokens in
the sequence). Afterwards, same as what we did
with the lexical predictor, we feed the encoding to


[3https://www.sbert.net/docs/pretrained_models.html](https://www.sbert.net/docs/pretrained_models.html)



where _σ_ is the sigmoid function, _ωi_ are the



13


Figure 7: The prompt template used for comparison of two model responses using gpt-4o



a logistic regression model to predict the strategy
class.


_X_ = Normalize (Mean(SBERT( _R_ ))) _,_ (8)







_P_ ( _S|R_ ) = _σ_




- _N_

 
_ωi · xi_ + _b_

_i_ =1



_,_ (9)



show a qualitative analysis of the lexical predictor
trained on the responses of the llama2-13b model
using _c1_hf_ prompt template. After training the
logistic regression model on training portion of the
responses using bag-of-words features, we report
top-5 features with highest coefficient in table 9.
According to this analysis, not only the responses
are distinguishable, but also highest coefficients
are corresponding to relevant phrases that can explain the strategy class. For instance, in the **Col-**
**laborative Planning** class, top coefficients contain
phrases such as "work together" and "brainstorm
strategies".


**E** **Classifier Error Analysis**

|Strategy|Precision|Recall|F1-Score|Support|
|---|---|---|---|---|
|Affrmation|0.99|1.00|0.99|74|
|Avoid Judgment and Criticism|0.75|0.92|0.83|62|
|Chit Chat|0.91|1.00|0.95|63|
|Clarifcation|0.98|0.82|0.90|57|
|Collaborative Planning|0.96|0.99|0.97|75|
|Emotional Validation|0.98|0.97|0.98|65|
|Normalize Experiences|0.91|0.98|0.95|54|
|Offer Hope|0.97|0.94|0.95|63|
|Promote Self-Care Practices|0.97|1.00|0.99|72|
|Provide Different Perspectives|0.96|0.96|0.96|67|
|Refective Statements|0.90|0.91|0.91|81|
|Reframe Negative Thoughts|0.99|0.92|0.95|76|
|Share Information|0.95|0.91|0.93|67|
|Stress Management|0.98|0.88|0.93|60|
|Suggest Options|0.93|0.88|0.90|64|



Table 6: Precision, Recall, F1-Score, and Support for
Each Strategy


For evaluating the performance of the classifier,



**D.3** **Predictability results**


We measure the predictability of response strategy
in the responses provided by all of the baselines
on the held out test set using llama-2 suit of models. We randomly split each collection to 80/20
portions of training and test and train both mentioned models using 4-fold cross validation and
report the prediction accuracies on the test set. We
observe that the predictability of the responses in
one collection is highly correlated with SRA of the
responses in that collection.
Figure 10 show the accuracy of the predictors
trained on each of the extended data collections corresponding to different baseline models using bag
of word embeddings and sentence bert embeddings
of responses and a logistic regression classifier.
By qualitatively analyzing the coefficients of the
logistic regression model trained on lexical features, we observe that not only the responses given
by the high SRA prompts are predictable (distinguishable) but also the high coefficient n-grams are
completely relevant to the class of the strategy. We



14


Figure 8: An example where gpt-4o judges the base model to give a better response that both aligns with the strategy
and is more natural, coherent and consistent


15


Figure 9: An example where gpt-4o judges the our model to give a better response that both aligns with the strategy
and is more natural, coherent and consistent


16


Figure 10: Comparison of the predictability of the strategy of different prompt responses across different model
sizes. We report accuracy of prediction using two predictors one operating on lexical features of response and
the other one on semantic features of the response.


we use the held out 100 conversations. We randomly break conversations the same way we outlined in section 4.3 and randomly pick our finetuned llama2-7b-chat and llama3-8b-instruct models to continue the conversation using a random
strategy. Then we collect 1000 responses. Afterwards, we apply our classifier on the responses and
measure the inferred strategy given the response.
The authors of the paper are asked to verify if the
inferred class of strategy is used in the response
generated by the model. The exact annotation instruction is as follows:
_Given the response bellow, verify if the response_
_uses the mentioned strategy._ _If the response uses_
_multiple strategies, only verify it’s correctness if the_
_strategy forms the main argument in the response._
the classifier achieves 93.6% accuracy on this
task. Table 6 shows the detailed performance on different classes. It can be observed that the classifier
mostly struggles in _Avoid Judgment and Criticism_
class.


**F** **Steerability analysis of Llama-3 models**


We fix the same experimental setup as in section

5.2 for llama3-8b-instruct and measure the average
accuracy and SRA of the model responses in depth
of the conversation. Although llama-3 models go
through a more extensive phase of steerability training (Dubey et al., 2024), we still observe the lack
of adherence to the prompted strategy for these
models and therefore a huge gap between the performance of the base llama3-8b-instruct model and
our fine-tuned counter part in following the strategy.
Figure 11 demonstrates the accuracy and SRA of
the responses by different llama3-8b based models
in depth of the conversation.



17


|strategy|description|
|---|---|
|Affrmation|This involves acknowledging and positively reinforcing an individual’s strengths,<br>feelings, or actions. Examples: ’You’ve shown incredible resilience in facing<br>these challenges.’ ’I admire your dedication to improving your situation.’ ’Your<br>ability to stay hopeful in tough times is truly commendable.’|
|Clarifcation|This entails asking questions or restating what was said to ensure clear under-<br>standing of the person’s feelings or situation. Examples: ’Could you explain<br>a bit more about what you mean by that?’ ’So, what you’re saying is that you<br>feel overwhelmed by the workload?’ ’I want to make sure I understand; you’re<br>feeling anxious about the upcoming event, right?’|
|Collaborative Plan-<br>ning|This involves working together to develop strategies or plans to address specifc<br>issues or challenges. Examples: ’Let’s brainstorm some strategies that could<br>help you manage this stress.’ ’We can work together to come up with a plan that<br>feels comfortable for you.’ ’How about we outline some steps you can take to<br>approach this problem?’|
|Emotional Valida-<br>tion|This strategy involves acknowledging and accepting the person’s emotions as<br>legitimate and important. Examples: ’It’s completely normal to feel sad in<br>a situation like this.’ ’Your feelings of frustration in this case are absolutely<br>understandable.’ ’I hear you, and it makes sense that you would feel anxious<br>about this.’|
|Normalize Experi-<br>ences|This approach helps the person understand that their experiences or feelings<br>are common and not something to be ashamed of. Examples: ’Many people go<br>through similar challenges, and it’s okay to feel this way.’ ’Feeling overwhelmed<br>in such situations is a common reaction.’ ’It’s normal to have ups and downs in<br>response to life’s stresses.’|
|Offer Hope|This involves providing reassurance that things can improve and that there is<br>hope for a better future. Examples: ’I’m confdent that you’ll fnd a way through<br>this challenge.’ ’Things might be tough now, but there is always a possibility for<br>change and growth.’ ’I believe in your ability to overcome these obstacles.’|
|Promote Self-Care<br>Practices|Encouraging the person to engage in activities that promote physical, emotional,<br>and mental well-being. Examples: ’Have you considered setting aside some time<br>for relaxation or a hobby you enjoy?’ ’Taking care of your health is important,<br>maybe try some exercise or meditation.’ ’Remember to take breaks and do things<br>that make you feel good.’|
|Provide<br>Different<br>Perspectives|Offering new viewpoints or ways of thinking about a situation to help broaden<br>understanding and possibly reduce distress. Examples: ’Have you considered<br>looking at the situation from this angle?’ ’Sometimes, stepping back and viewing<br>things differently can be helpful.’ ’What if we think about the potential positive<br>outcomes of this scenario?’|



Table 7: Strategy 1 to 8 along with their descriptions


18


|strategy|description|
|---|---|
|Avoid<br>Judgment<br>and Criticism|This strategy focuses on providing support without expressing negative judg-<br>ments or criticisms of the person’s thoughts, feelings, or actions. Examples:<br>’It’s understandable that you felt that way in that situation.’ ’Everyone makes<br>mistakes, and it’s okay to be imperfect.’ ’Your feelings are valid, and it’s okay<br>to express them.’|
|Refective<br>State-<br>ments|Mirroring back what the person has said to show understanding and empathy.<br>Examples: ’It sounds like you’re feeling really overwhelmed by your workload.’<br>’You seem to be saying that this situation has made you feel anxious.’ ’I hear<br>that you’re fnding it hard to cope with these changes.’|
|Reframe Negative<br>Thoughts|Helping to shift negative or unhelpful thought patterns into more positive or<br>realistic ones. Examples: ’Instead of thinking of it as a failure, could we see it<br>as a learning opportunity?’ ’What if we try to focus on what you can control in<br>this situation?’ ’Let’s look for the strengths you’ve shown in dealing with this.’|
|Share Information|Providing factual information or resources that might be helpful in understanding<br>or coping with a situation. Examples: ’I read an article about coping strategies<br>that might be useful for you.’ ’There are some great books that offer insights<br>into managing these feelings.’ ’I can share some websites that provide helpful<br>tips on stress management.’|
|Stress Management|Offering techniques or suggestions to help reduce or manage stress. Examples:<br>’Have you tried deep breathing or mindfulness exercises to manage stress?’ ’Cre-<br>ating a regular routine can sometimes help in reducing stress levels.’ ’Exercise<br>can be a great way to relieve stress and improve mood.’|
|Suggest Options|Presenting various possibilities or alternatives that the person might consider in<br>their situation. Examples: ’One option might be to talk to someone you trust<br>about what you’re going through.’ ’Have you thought about joining a support<br>group for this issue?’ ’Maybe trying a new approach to this problem could yield<br>different results.’|
|Chit Chat|Engaging in light, casual conversation to build rapport and provide a sense of<br>normalcy and comfort. Examples: ’How’s your day going so far?’ ’Did you see<br>that funny movie that came out recently?’ ’I love this weather we’re having. Do<br>you enjoy outdoor activities?’|



Table 8: Strategy 9 to 15 along with their descriptions


19


|Strategy|Top 5 N-grams|
|---|---|
|Affrmation|truly commendable, takes lot, shown incredi-<br>ble, strength resilience, resilience facing|
|Avoid Judgment and Criticism|important remember, okay feel, remember<br>everyone, completely understandable, under-<br>standable feeling|
|Chit Chat|day going, oh gosh, outdoor activities, oh<br>goodness, hey day|
|Clarifcation|tell mean, clarify saying, tell bit, clarify feel-<br>ing, feeling overwhelmed|
|Collaborative Planning|work together, together come, let work, come<br>plan, brainstorm strategies|
|Emotional Validation|completely understandable, valid important,<br>normal feel, completely normal, absolutely<br>valid|
|Normalize Experiences|many people, okay feel, completely normal,<br>important remember, normal feel|
|Offer Hope|better future, hope better, want know, believe<br>ability, fnd way|
|Promote Self-Care Practices|aside time, setting aside time, considered set-<br>ting, hobby enjoy, time relaxation|
|Provide Different Perspectives|instead focusing, different perspective, consid-<br>ered looking, situation different, additionally<br>might|
|Refective Statements|sounds like, like feeling, understandable feel-<br>ing, feeling really, tell feeling|
|Reframe Negative Thoughts|instead focusing, try reframe, let try, reframe<br>opportunity, let focus|
|Share Information|resources available, additionally many, online<br>resources, many resources, might helpful|
|Stress Management|deep breathing, manage stress, regular routine,<br>techniques help, stress levels|
|Suggest Options|option could, one option, additionally might,<br>another option, option might|


Table 9: Top 5 3-gram and 2-gram features for strategy classification in lexical predictor


20


Figure 11: Left: average accuracy of the strategy following for each model with respect to the turn of the conversation,
Right: average SRA of the responses with respect to the turn of the conversation


21


