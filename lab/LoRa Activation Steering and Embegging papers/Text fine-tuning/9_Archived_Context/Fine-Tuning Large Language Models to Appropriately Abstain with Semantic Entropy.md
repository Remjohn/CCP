## **Fine-Tuning Large Language Models to Appropriately** **Abstain with Semantic Entropy**

**Benedict Aaron Tjandra** [1] _[∗]_ **Muhammed Razzak** [1] _[∗]_ **Jannik Kossen** [1] _[∗]_


**Kunal Handa** [1] **Yarin Gal** [1]


1 OATML, Department of Computer Science, University of Oxford


**Abstract**


Large Language Models (LLMs) are known to hallucinate, whereby they generate
plausible but inaccurate text. This phenomenon poses significant risks in critical
applications, such as medicine or law, necessitating robust hallucination mitigation
strategies. While recent works have proposed fine-tuning methods to teach LLMs
to abstain from answering questions beyond their knowledge or capabilities, these
methods rely on the existence of ground-truth labels or are limited to short-form
responses. To address these limitations, we propose fine-tuning using semantic
entropy, an uncertainty measure derived from introspection into the model which
does not require external labels. We demonstrate that our approach matches or
outperforms models fine-tuned using prior work and achieves strong performance
for both short and long-form generations on a range of datasets.


**1** **Introduction**


Large language models (LLMs) have made significant progress in natural language processing, achieving remarkable performance across a wide range of tasks (OpenAI, 2024; Meta, 2024; Google, 2024).
Models, like GPT-4, Llama 3, and Gemini, have demonstrated capabilities that rival or surpass human
performance in a range of domains and are increasingly deployed in the real world for various applications (Yang et al., 2023a). However, despite these advancements in performance, LLMs remain far
from flawless, particularly when it comes to handling tasks that fall outside their scope of knowledge
or reasoning abilities (Ji et al., 2023a; Huang et al., 2023), where they tend to exhibit _hallucinations_ .


Hallucinations, in the context of LLMs, refer to instances where models generate content that, while
appearing plausible, is factually inaccurate, contradicts previously established world knowledge, or
does not make logical sense (Zhang et al., 2023). These hallucinations, while harmless in low-stakes
applications, can have severe consequences when LLMs are deployed in safety-critical domains such
as healthcare or legal services, where the generation of erroneous information could be costly or lead
to real-world harm (Han et al., 2024; Weiser, 2023). As a result, mitigating hallucinations is crucial
to ensuring the safety, trustworthiness, and overall reliability of LLMs (Rawte et al., 2023).


Various strategies have been proposed to mitigate hallucinations (Ji et al., 2023a; Tonmoy et al., 2024).
Retrieval Augmented Generation (RAG) approaches attempt to ground LLM outputs by incorporating
external knowledge sources (Lewis et al., 2021; Shuster et al., 2021; Ji et al., 2023b), anchoring
responses in verified facts. Other techniques involve modifying the inference process to encourage
more cautious generation (Shi et al., 2023; Chuang et al., 2024) or focus on post-hoc detection,
where hallucinations are flagged after generation through methods such as confidence or uncertainty
estimation (Kadavath et al., 2022; Azaria and Mitchell, 2023; Kuhn et al., 2023; Farquhar et al., 2024).


An approach that has gained attention due to its simplicity and effectiveness involves fine-tuning
LLMs to abstain from answering questions that are outside the scope of their knowledge or


_∗_ Equal Contribution. Correspondence to aaron_tjandra@yahoo.com.


Preprint. Under review.


capabilities (Wen et al., 2024). To do this, an LLM is fine-tuned on a dataset that consists of examples
of questions that the LLM should abstain from answering and, conversely, examples of questions
that the LLM should willingly answer. Several recent works (Yang et al., 2023b; Cheng et al., 2024;
Wolfe et al., 2024) teach the LLM to abstain from answering questions it answered incorrectly. These
approaches, however, require access to ground-truth labels, which in many cases can be difficult or
costly to obtain. Additionally, since ground-truth labels come from external sources, there is evidence
that they are potentially noisy and hence not the most appropriate teaching signal Kossen et al. (2024).
To avoid being dependent on ground-truth labels, Zhang et al. (2024) explored an uncertainty-based
fine-tuning approach, R-Tuning-U, where they first approximate an LLM’s uncertainty (as measured
by entropy) in answering a question and subsequently training the LLM to abstain from answering
questions it is uncertain. R-Tuning-U, however, is sensitive to the lexical and syntactical variations
of generations, limiting its application to settings where the LLM is instructed to generate short-form
responses consisting of not more than a few words, hindering its usefulness.


In this work, we propose to leverage semantic entropy (Kuhn et al., 2023; Farquhar et al., 2024) to
overcome these limitations. Semantic entropy improves over R-Tuning-U by computing entropy over
the semantic space that model generations occupy, rather than over raw token sequences. As semantic
entropy evaluates the entropy over the semantic meaning of the generations, it is robust to lexical
and syntactical variations of generations. This results in a better indicator of hallucinations in both
short-form and long-form generation settings (Kuhn et al., 2023; Farquhar et al., 2024). By fine-tuning
models to abstain from answering questions it is uncertain about using semantic entropy, we provide
an approach to reduce the model’s hallucinations, without relying on ground-truth labels or being
restricted to the short-form response setting. This allows for a more flexible and reliable abstention
across a wide range of tasks and domains, providing a powerful tool for reducing hallucinations.


We evaluate our method across several benchmarks and introduce a new metric called accuracyengagement distance (AED), which quantifies model hallucinations more comprehensively by taking
into account its _accuracy_ and _engagement_, the number of questions it chooses to answer willingly.
Using this metric, we show that models fine-tuned with semantic entropy significantly outperform
R-Tuning and R-Tuning-U, existing approaches where the former is label-dependent and the latter
is label-independent. Compared to R-Tuning and R-Tuning-U (Zhang et al., 2024), our method
achieves up to 30.1% reduction in hallucination rates for long-form generations and up to 8.7% for
short-form generations. Our method opens up new avenues to fine-tune models on both short-form
and long-form generations without relying on ground-truth labels, making it easily scalable.


**Contributions.** In summary, the key contributions of this paper are:


    - We demonstrate that models fine-tuned using semantic entropy (Section 5) match or outperform models fine-tuned using prior work, under both long-form (Long-QA) and short-form
(Short-QA) answering settings (Section 6).


    - We introduce the _accuracy-engagement distance (AED)_, a novel evaluation metric, that more
holistically quantifies the extent of a model’s hallucination by taking into account both the
_accuracy_ and _engagement_ of a model (Section 4).


**2** **Related Work**


There is a significant body of work in the literature that studies why hallucination occurs and how
to prevent them. We redirect the reader to recent surveys (Ji et al., 2023a; Huang et al., 2023;
Rawte et al., 2023; Chakraborty et al., 2024) for a comprehensive overview of hallucinations. For
conciseness, we focus on previous work that are most pertinent to ours.


**Uncertainty Estimation in LLMs.** A variety of works have proposed uncertainty measures to detect
hallucinations in LLM generations. Grey-box methods rely on token likelihoods and multiple samples
to a prompt to measure LLM uncertainty (Kadavath et al., 2022; Kuhn et al., 2023; Farquhar et al.,
2024; Zhang et al., 2024). White-box methods assume access to the internals of an LLM (weights
and activations) and train models on the activations during generation to probe into the uncertainty of
LLMs (Ahdritz et al., 2024; Kossen et al., 2024; Liu et al., 2024).


**Abstention Fine-Tuning.** There is a range of proposed methods to fine-tune LLMs to abstain from
answering questions beyond their capabilities (Wen et al., 2024). Wolfe et al. (2024) looked into
using QA datasets with unanswerable questions and fine-tuned LLMs to abstain from answering


2


those questions. Similarly, Brahman et al. (2024) developed a taxonomy for different abstention
scenarios and, using prompting techniques, constructed a synthetic dataset to capture each abstention
scenario. They then used this dataset to fine-tune models and measured their abstention rate in each
abstention scenario. Yang et al. (2023b) and Cheng et al. (2024) sampled multiple responses to each
question and leveraged the accuracy rate to fine-tune LLMs to abstain from questions whose accuracy
rate is below a certain threshold. Zhang et al. (2024) proposed R-Tuning and R-Tuning-U to fine-tune
LLMs under the Short-QA answering setting. In R-Tuning, models are instructed to generate single
responses to a set of questions, and are fine-tuned to abstain from questions it answered incorrectly.
In R-Tuning-U, multiple responses are sampled per question and the entropy of those responses is
used to measure the uncertainty of an LLM to each question. The model is then fine-tuned to abstain
on the top-50% most uncertain questions while keeping their original responses for the other half.


**3** **Background:** **Label-Free Uncertainty Estimation in LLMs**


In this section, we familiarise the reader with R-Tuning-U and semantic entropy, two uncertainty quantifying methods for LLMs that we use to determine the set of questions an LLM should abstain from.


**R-Tuning-U.** R-Tuning-U (Zhang et al., 2024) uses an approximation of the _classical_ conditional
entropy given a particular question _q_ to measure an LLM’s uncertainty. Let _G_ be the set of possible
generations, where **s** _∈_ _G_ denotes a sequence of tokens with _si_ representing the _i_ -th token in the
sequence, and let **q** be the sequence of tokens obtained by tokenising our prompt _q_ . Using the
conditional probability distribution _pθ_ that we can obtain from an LLM, the probability of some
token sequence **s** occurring given **q** is



_pθ_ ( **s** _|_ **q** ) =



_|_ **s** _|_

- _pθ_ ( _si_ _|_ **s** _<i,_ **q** ) _,_ (1)


_i_ =1



where **s** _<i_ = ( _s_ 1 _, ..., si−_ 1). The classical conditional entropy over generations is formally defined as


_E_ ( **q** ) = _−_         - _pθ_ ( **s** _|_ **q** ) log _pθ_ ( **s** _|_ **q** ) _._ (2)


**s** _∈G_


However, since the size of _G_ may be extremely large, the above equation is intractable to compute
exactly. R-Tuning-U arrives at a discrete approximation of Equation (2) by sampling _M_ generations
and subsequently measuring the empirical probability of the occurrence of each generation. If we
let _U_ to be the set of unique generations obtained from _S_, our list of sampled generations, and _c_ ( _u_ )
to be the number of times _u ∈_ _U_ occurs in _S_, then R-Tuning-U approximates the classical entropy by




- - _c_ ( _u_ )
log
_M_




_._ (3)



_E_ ( **q** ) _≈−_ 

_u∈U_




- _c_ ( _u_ )

_M_



**Semantic Entropy.** The key drawback of R-Tuning-U is that it disregards the semantic meaning of
the generations and is sensitive to lexical and syntactical variations. A model that generates “The
capital of France is Paris” and “Paris is France’s capital” when prompted twice in response to the
question “What is France’s capital?” is not uncertain in any meaningful sense (Kuhn et al., 2023).
R-Tuning-U, however, will assign a non-zero uncertainty as the generations are different strings.


Semantic entropy improves over R-Tuning-U by taking into account the semantic meaning of
generations. Instead of computing the entropy of the generations, it computes the entropy of _semantic_
_equivalence classes_ that the generations occupy, where a semantic equivalence class _C_ is defined
to be the set of generations that share the same particular meaning. More concretely, letting _C_ to
be the set of all semantic equivalence classes, for any semantic equivalence class _C_ _∈C_, we have
_∀_ **s** _,_ **s** _[′]_ _∈_ _C_ : _R_ ( **s** _,_ **s** _[′]_ ), where _R_ ( _·, ·_ ) is a _semantic equivalence relation_ that holds if and only if two
generations have the same semantic meaning. Formally, the semantic entropy is defined as


_SE_ ( **q** ) = _−_         - _pθ_ ( _C_ _|_ **q** ) log _pθ_ ( _C_ _|_ **q** ) _,_ (4)


_C∈C_


3


where _pθ_ ( _C_ _|_ **q** ) is the probability of a semantic equivalence class _C_ occurring given **q** :




- _pθ_ ( **s** _|_ **q** ) = 

**s** _∈C_ **s** _∈C_



_pθ_ ( _C_ _|_ **q** ) = 


**s** _∈C_



_|_ **s** _|_

- _pθ_ ( _si_ _|_ **s** _<i,_ **q** ) _._ (5)


_i_ =1



However, just as calculating classical entropy is intractable, calculating semantic entropy is equally
intractable. Similar to R-Tuning-U, we can approximate the (discrete) semantic entropy by sampling
_M_ generations in response to _q_ and using the number of generations in each semantic equivalence
class (Farquhar et al., 2024) to approximate _pθ_ ( _C_ _|_ **q** ). Letting _C_ 1 _, . . ., Cm_ to be the semantic equivalence classes that we can extract from our sampled list of generations _S_, the discrete approximation
of semantic entropy is given by



_m_



_i_ =1




- - _|Ci|_
log
_M_




_._ (6)



_SE_ ( **q** ) _≈−_



_m_

- _pθ_ ( _Ci_ _|_ **q** ) log _pθ_ ( _Ci_ _|_ **q** ) _≈−_


_i_ =1




- _|Ci|_
_M_



To compute the above equation in practice, we need to first operationalise the semantic equivalence
relation _R_ ( _·, ·_ ). In this work, we follow Kuhn et al. (2023)’s approach to implement _R_ ( _·, ·_ ) using
the concept of question-dependent bi-directional entailment. More specifically, we deem that two
generations **s** and **s** _[′]_ are semantically equivalent if an entailment model says they logically entail one
another within the context of the question. We then use _R_ ( _·, ·_ ) to cluster _S_ into semantic equivalence
classes, where each class consists of responses that share the same semantic meaning. Given these
equivalence classes, we estimate the probability _pθ_ ( _Ci_ ) of each class _Ci_ by dividing the number of
responses in class _Ci_ by the total number of responses _M_ . The semantic entropy for a question _q_
then follows via Equation (6). More details concerning the entailment model, semantic clustering,
and semantic entropy calculation can be found in Appendix A.3.


**4** **Accuracy-Engagement Distance**


Several works (Zhang et al., 2024; Feng et al., 2024) suggest using the accuracy over the set of
willingly answered questions to measure the extent of hallucination of a model. Though a natural
idea, we argue that this metric is not a holistic measure of model performance as it does not penalise
the model from wrongly abstaining from a question. To illustrate, consider a model _A_ 1 that willingly
answers all questions on a dataset of 2500 questions and attains an accuracy of 70%. Suppose that
fine-tuning _A_ 1 yields a model _A_ 2 that willingly answers 10 questions and attains an accuracy of 70%.
If we use accuracy to compare _A_ 1 and _A_ 2, then we would deem them as equivalent as they have the
same accuracies. However, from a helpfulness point of view, this is misleading as _A_ 2 is clearly _worse_
than _A_ 1 as it avoids answering a substantial number of questions that _A_ 1 previously got correct.


We can see that _A_ 2 has a **low engagement** as it abstains from answering a large number of questions.
Ideally, our metric should **penalise low engagement and low accuracy** and reward **high engagement**
**and high accuracy** . Adapting Tian et al. (2023)’s method to compare the truthfulness of biography
generations, we propose to evaluate fine-tuned models using a novel evaluation metric, the _Accuracy-_
_Engagement Distance_, that takes into account both the accuracy and engagement of a model.


Consider a fine-tuned model that answers _Q_ questions willingly. Among these _Q_ questions, the model
answers _I_ questions incorrectly and _C_ questions correctly. We can conceptualise our fine-tuned
model as occupying a single point in R [2] whose coordinates are ( _I, C_ ). An ideal model, that has
the highest accuracy and engagement, answers all questions correctly and is represented by the
point (0, _|D|_ ) in this space, where _|D|_ is the total number of questions in a particular dataset. The
Accuracy-Engagement Distance (AED) is the normalised Euclidean distance between the point
representing the fine-tuned model and the ideal model:



AED =




_I_ [2] + ( _|D| −_ _C_ ) [2]

_._
2 _· |D|_ [2]



The AED ranges from 0 to 1 and is maximised when the model answers every question correctly ( **max**
**accuracy, max engagement** ) and is minimised when the model answers every question incorrectly
( **min accuracy,** **max engagement** ). If we now compare _A_ 1 and _A_ 2 using AED, we can see that
_A_ 1 achieves an AED of 0.30 while _A_ 2 achieves an AED of 0.71, penalising _A_ 2’s low engagement.


4


**5** **Abstention Fine-Tuning using Semantic Entropy**


In this section, we introduce a fine-tuning strategy that leverages semantic entropy to enable model
abstention in uncertain scenarios.


**Overview.** The key idea is to determine which questions to abstain from and to willingly answer based
on the semantic entropy of a model’s responses. Questions with high semantic entropy, indicating a
high likelihood of a hallucination being generated, should be abstained from answering, while those
with low semantic entropy should be answered with the model’s standard response.


**Dataset Construction.** For each question in the training dataset, we generate a **standard response**
using a low-temperature setting ( _T_ = 0 _._ 1) to encourage a deterministic output. Additionally, we
generate _M_ = 10 responses by sampling at a high temperature ( _T_ = 1 _._ 0) to capture the model’s
variability under more stochastic conditions.


The high-temperature responses are used to compute the semantic entropy as described in Section 3.
Computing the semantic entropy of each question _q_ results in a set of ( _q, SE_ ( _q_ )) pairs where _SE_ ( _q_ )
represents the semantic entropy of _q_ ’s responses. With the computed semantic entropy for each
question, we partition the dataset into two subsets based on a user-defined uncertainty threshold _τ_ :


    - **High-entropy set** _H_ **:** This set contains questions where _SE_ ( _q_ ) _> τ_, indicating a high level
of uncertainty in the model’s responses. For these questions, we modify the ground-truth
label to an abstention phrase: _"I don’t know the answer."_

    - **Low-entropy** **set** _L_ **:** This set includes questions with _SE_ ( _q_ ) _≤_ _τ_, where the model is
relatively confident. Here, the ground-truth label is set to be the model’s standard response.


**Fine-Tuning Procedure.** Once the dataset is partitioned, we fine-tune the model using _H_ and _L_ .
We employ supervised fine-tuning with cross-entropy loss, where the model is trained to predict the
next token in the concatenated input sequence (prompt + question + adjusted label). The model is
encouraged to generate the standard response for questions in _L_, while abstaining for those in _H_ .


Formally, given an answering setting prompt, i.e. Long-QA or Short-QA, tokenised questions **q**, and
their corresponding tokenised ground-truth labels **y** [(] _[q]_ [)] (either the standard response or abstention
phrase), the model learns to minimise the following fine-tuning objective during training:



_LCE_ ( _pθ_ ) = _−_ 

_q∈Q_



_|_ **y** [(] _[q]_ [)] _|_

- log _pθ_ ( _yt_ [(] _[q]_ [)] _|_ prompt _,_ **q** _,_ **y** _t_ [(] _−_ _[q]_ [)] 1 [)] _[,]_ (7)

_t_ =1



where _Q_ denotes the set of questions in the training set and _pθ_ ( _·_ _|_ prompt _,_ **q** _,_ **y** _t_ [(] _−_ _[q]_ [)] 1 [)][ is the model’s]
predicted next-token probability distribution given the answering setting prompt, question, and the
first _t −_ 1 tokens of the modified ground-truth label.


**6** **Experiments**


We evaluate our abstention fine-tuning approach LLAMA-3-8B-INSTRUCT (Meta, 2024) across four
datasets and two answering settings: 1) Long-QA, where we instruct the LLM to generate free-form
sentence-length generations and 2) Short-QA, where we instruct the LLM to generate short-form
answers. Our prompts for each answering setting can be found in Appendix A.1.


**Datasets.** We evaluate across four datasets: TriviaQA Joshi et al. (2017), BioASQ Tsatsaronis et al.
(2015), NQ Kwiatkowski et al. (2019), and SQuAD Rajpurkar et al. (2016). We randomly select
2500 QA pairs from the validation split of each dataset and designate 2000 data points for training
and 500 data points for in-distribution validation. We adopt a closed-book setting for our experiments
and remove additional context that is present in TriviaQA and SQuAD. For each question, we use
the model’s standard response and the question’s ground-truth label to assign an accuracy score to
that question (Appendix A.2). As described in Section 5, the high-temperature responses are used to
calculate the semantic entropy of each question. We compute semantic entropy with two entailment
models resulting in two variants of semantic entropy: Semantic Entropy with DeBERTa entailment
(SE (DeBERTa)) and Semantic Entropy with Llama-3-70B-Instruct entailment (SE (Llama)). Further
implementation details can be found in Appendix A.3. In addition to semantic entropy, we use the hightemperature responses to compute the entropy for R-Tuning-U via a direct application of Equation (2).


5


**Fine-Tuning.** Our experiments involve fine-tuning a model on a training dataset and evaluating the
fine-tuned model on the in-distribution validation split and out-of-distribution datasets that exclude
the training set. For experiments concerning an uncertainty metric, i.e. R-Tuning-U, SE (DeBERTa),
and SE (Llama), each fine-tuning run is associated with a threshold _τ_, where we partition the training
set into the high-entropy set and the low-entropy set. We then fine-tune the model via the method
described in Section 5. For R-Tuning, we assign the set of incorrect questions to _H_ and the set of
correct questions to _L_ and equivalently replace the ground-truth labels of _H_ with the abstention
phrase and _L_ with the standard response of the model. Due to resource constraints, we use LoRA (Hu
et al., 2021) to perform supervised fine-tuning. In addition to single dataset experiments, i.e. training
on one dataset and evaluating on another dataset, we also conduct experiments where we train on
multiple datasets – specifically by combining the training splits of TriviaQA, BioASQ, and NQ. We
denote this setting as “Mult” in subsequent sections. In “Mult”, the validation set is the combined
validation sets of TrivaQA, BioASQ, and NQ, and the out-of-distribution set consists of SQuAD.
Hyperparameter details can be found in Appendix A.4.


**Model Selection and Evaluation.** We conduct two forms of evaluation: 1) Best-Threshold Evaluation and 2) All-Threshold Evaluation. In **Best-Threshold Evaluation**, we conduct experiments
with R-Tuning with 3 random seeds and report the mean and standard deviation of the AED on
the in-distribution validation set and out-of-distribution datasets. For each of R-Tuning-U, SE
(DeBERTa), and SE (Llama), we first train a different model on 9 equally-spaced thresholds, ranging
from 0.25 and 2.25, and select the threshold _τ_ that achieves the lowest AED on the in-distribution
validation set. We conduct experiments with that threshold using 3 random seeds and report the mean
and standard deviation AED on the in-distribution validation set and out-of-distribution datasets.
This captures a realistic scenario where an in-distribution validation set is used to pick the threshold _τ_
that leads to the lowest AED and subsequently evaluating how well this fine-tuned model generalises
on out-of-distribution settings.


In **All-Threshold Evaluation**, we evaluate each fine-tuned model trained at each of the 9 thresholds
in our _single-dataset_ _experiments_, recording the number of incorrect and correct questions each
fine-tuned model gets on out-of-distribution datasets. To inspect the formation of any overall trends,
we aggregate the number of incorrect and correct questions to build an “adaptation” plot, where
each point represents the average incorrect and correct responses a fine-tuned model gets on an
out-of-distribution dataset when trained at a specific threshold. For both types of evaluation, we
perform greedy inference ( _T_ = 0).


**7** **Results and Discussion**


This section presents and discusses our results for Best-Threshold and All-Threshold Evaluation.


**Models Fine-Tuned on Semantic Entropy Have Lower AEDs.** Figure 1 and Figure 2 presents
results for Best-Threshold Evaluation. Figure 1 shows in-distribution experiments where we
average results across different seeds, while Figure 2 shows out-of-distribution experiments where
we average results across different seeds _and_ further averaging experiments that share the same
out-of-distribution dataset. A granular breakdown of our out-of-distribution experiments can be
found in Appendix A.6. We further aggregate the means of all datasets and present the overall
average for each setting in Table 1. From Figure 1 and Figure 2, fine-tuning on semantic entropy,
under both Long-QA and Short-QA answering settings and on in-distribution and out-of-distribution
evaluations, yields models with AEDs that are typically equal or lower than models fine-tuned
with R-Tuning and R-Tuning-U. We also see that fine-tuning on semantic entropy computed with
a stronger entailment model (SE (Llama)) largely led to models with lower AEDs. Moreover, from


Table 1: SE (Llama) and SE (DeBERTa) achieves the lowest overall average Accuracy-Engagement
Distances for both Long-QA and Short-QA. **Bold** indicates lowest.


**Setting** **SE (Llama)** (ours) **SE (DeBERTa)** (ours) **R-Tuning** **R-Tuning-U** **Original Model**


Long-QA: In-Distribution **0.364** 0.411 0.399 0.521 0.380
Short-QA: In-Distribution 0.428 **0.427** 0.469 0.438 0.467
Long-QA: Out-of-Distribution **0.406** 0.432 0.438 0.541 0.425
Short-QA: Out-of-Distribution **0.473** 0.482 0.508 0.485 0.525


6


0.6


0.5


0.4


0.3


0.2


0.7


0.6


0.5


0.4


0.3


0.2
































































































|Col1|Col2|Col3|Col4|Col5|Col6|Col7|Col8|Col9|Col10|0.654|Col12|Col13|Col14|Col15|Col16|Col17|0.5|Col19|Col20|Col21|Col22|Col23|Col24|0.629<br>84 0.588|Col26|Col27|Col28|Col29|Col30|Col31|Col32|Col33|Col34|Col35|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|||||||||||||0.4|0.4|0.4|0.4|0.4|0.543<br>0.555<br>81<br>0.556|0.543<br>0.555<br>81<br>0.556|0.543<br>0.555<br>81<br>0.556|0.543<br>0.555<br>81<br>0.556|0.543<br>0.555<br>81<br>0.556|0.543<br>0.555<br>81<br>0.556|||||||||0.506|0.506|0.506|0.506|
||||0.438<br>~~0.3~~|0.438<br>~~0.3~~|0.438<br>~~0.3~~|0.438<br>~~0.3~~|0.438<br>~~0.3~~|0.438<br>~~0.3~~|0.438<br>~~0.3~~|~~77~~||0.418<br>0.44<br>|0.418<br>0.44<br>|0.418<br>0.44<br>|0.418<br>0.44<br>||||0.426|0.426|||||||0.421<br>~~0.3~~|0.421<br>~~0.3~~|0.421<br>~~0.3~~|0.421<br>~~0.3~~|~~57~~||||
||||0.353<br>96<br>~~0.261~~<br>0.202|0.353<br>96<br>~~0.261~~<br>0.202|0.353<br>96<br>~~0.261~~<br>0.202|0.353<br>96<br>~~0.261~~<br>0.202|0.353<br>96<br>~~0.261~~<br>0.202|||||0.354|0.354||||||||||||||0.319|0.319|||||0.328|0.328|
||||0.353<br>96<br>~~0.261~~<br>0.202||||||||||||||||||||||||||||||||
||Tr|iviaQ<br>|iviaQ<br>|A||||B|ioAS|ioAS|Q||||Sh|NQ<br>ort-|NQ<br>ort-|QA||||S|QuA|QuA|D|0.708||||Mult|Mult||||
||Tr|iviaQ<br>||||||||~~0.5~~|~~0.5~~|~~0.5~~|~~0.5~~|~~0.5~~|~~0.5~~|~~0.5~~|0.593<br>0.595<br>~~51~~<br>0.6<br>|0.593<br>0.595<br>~~51~~<br>0.6<br>|0.593<br>0.595<br>~~51~~<br>0.6<br>|0.593<br>0.595<br>~~51~~<br>0.6<br>|0.593<br>0.595<br>~~51~~<br>0.6<br>|0.593<br>0.595<br>~~51~~<br>0.6<br>|0.593<br>0.595<br>~~51~~<br>0.6<br>|46<br>0.613|46<br>0.613||||||||||
||Tr|iviaQ<br>||||||||~~0.5~~|~~0.5~~|~~0.5~~|~~0.5~~|~~0.5~~|~~0.5~~|~~0.5~~|0.593<br>0.595<br>~~51~~<br>0.6<br>|0.593<br>0.595<br>~~51~~<br>0.6<br>|0.593<br>0.595<br>~~51~~<br>0.6<br>|0.593<br>0.595<br>~~51~~<br>0.6<br>|0.593<br>0.595<br>~~51~~<br>0.6<br>|0.593<br>0.595<br>~~51~~<br>0.6<br>|||||||||||||
||Tr|iviaQ<br>||||||||0.518<br>0.509<br>|0.518<br>0.509<br>|0.518<br>0.509<br>|0.518<br>0.509<br>|0.518<br>0.509<br>|0.518<br>0.509<br>|0.518<br>0.509<br>|0.522<br>0.562|0.522<br>0.562|0.522<br>0.562|0.522<br>0.562|||||||0.|0.|0.|0.|42|42|42|42|
||Tr|iviaQ<br>|0.397<br>0.395<br><br>0.4|0.397<br>0.395<br><br>0.4|0.397<br>0.395<br><br>0.4|0.397<br>0.395<br><br>0.4|0.397<br>0.395<br><br>0.4|0.397<br>0.395<br><br>0.4|0.397<br>0.395<br><br>0.4|14<br>0.399<br>0.412|14<br>0.399<br>0.412|14<br>0.399<br>0.412|14<br>0.399<br>0.412||||||||||||||~~0.381~~<br>~~0.385~~<br>|~~0.381~~<br>~~0.385~~<br>|~~0.381~~<br>~~0.385~~<br>|~~0.381~~<br>~~0.385~~<br>|0.394<br>0.405|0.394<br>0.405|0.394<br>0.405|0.394<br>0.405|
||Tr|iviaQ<br>|~~15~~|~~15~~|~~15~~|~~15~~|||||||||||||||||||||||||||||
||Tr|iviaQ<br>|~~15~~|~~15~~|~~15~~|~~15~~|||||||||||||||||||||||||||||
||Tr|||0.261<br>0.25|0.261<br>0.25|0.261<br>0.25|||||||||||||||||||||||||||||
||||||||||||||||||||||||||||||||||||
||Tr<br>SE|iviaQ<br> (Lla|iviaQ<br> (Lla|A<br> ma|) (ou|) (ou|)|B|ioAS<br>S|ioAS<br>S|Q<br>E (D|eBE|eBE|a) (o|urs)|NQ<br>|NQ<br>||R-|R-|ning|S|QuA|QuA|D<br>R-|Tuni|Tuni|U||Mult<br>|Mult<br>|Origi|nal|nal|
||||||||||||||||||||||||||||||||||||
||||||||||||||||||||||||||||||||||||





0.6


0.5


0.4


0.3


0.2


0.7


0.6


0.5


0.4


0.3


0.2






















































































|Col1|Col2|Col3|Col4|Col5|Col6|Col7|Col8|Col9|Col10|0.612|Col12|Col13|Col14|Col15|Col16|Col17|0.552|Col19|Col20|Col21|Col22|Col23|Col24|0.631<br>0.588<br>0.583 0.5|Col26|Col27|Col28|Col29|Col30|Col31|0.656<br>56 0.583|Col33|Col34|Col35|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
||||~~0.372~~<br>0.3|~~0.372~~<br>0.3|~~0.372~~<br>0.3|~~0.372~~<br>0.3|~~0.372~~<br>0.3|~~0.372~~<br>0.3|~~0.372~~<br>0.3|89||0.428<br>0.44<br>0.4|0.428<br>0.44<br>0.4|0.428<br>0.44<br>0.4|0.428<br>0.44<br>0.4|0.428<br>0.44<br>0.4|0.538<br><br>43<br>0.<br>0.519<br>0.448|0.538<br><br>43<br>0.<br>0.519<br>0.448|0.538<br><br>43<br>0.<br>0.519<br>0.448|0.538<br><br>43<br>0.<br>0.519<br>0.448|0.538<br><br>43<br>0.<br>0.519<br>0.448|0.538<br><br>43<br>0.<br>0.519<br>0.448|0.538<br><br>43<br>0.<br>0.519<br>0.448|43|||0.532|0.532|||||||
||||~~0.372~~<br>0.3|~~0.372~~<br>0.3|~~0.372~~<br>0.3|~~0.372~~<br>0.3|~~0.372~~<br>0.3|~~0.372~~<br>0.3|~~0.372~~<br>0.3|89||0.428<br>0.44<br>0.4|0.428<br>0.44<br>0.4||||||||||||||||||||||
||||0.318<br><br>0.286|0.318<br><br>0.286|0.318<br><br>0.286|0.318<br><br>0.286|0.318<br><br>0.286|||||0.318|0.318||||||||||||||||||||||
||||~~58~~||0.192|0.192|||||||||||||||||||||||||||||
||Tr|iviaQ|iviaQ|A||||B|ioAS|ioAS|Q||||Sh|NQ<br>ort-|NQ<br>ort-|QA||||S|QuA|QuA|D|0.702||||Mult|Mult||0.702||
||Tr|iviaQ|||||||||||||||0.618<br>0.631<br>0.6|0.618<br>0.631<br>0.6|0.618<br>0.631<br>0.6|0.618<br>0.631<br>0.6|0.618<br>0.631<br>0.6|0.618<br>0.631<br>0.6|0.618<br>0.631<br>0.6|17<br>0.629|17<br>0.629||0.612<br>0.626<br>0.6|0.612<br>0.626<br>0.6|0.612<br>0.626<br>0.6|0.612<br>0.626<br>0.6|17<br>0.609|17<br>0.609|||
||Tr|iviaQ||||||||0.514<br>0.52<br>0.5|0.514<br>0.52<br>0.5|0.514<br>0.52<br>0.5|0.514<br>0.52<br>0.5|0.514<br>0.52<br>0.5|0.514<br>0.52<br>0.5|0.514<br>0.52<br>0.5|48<br>0.529<br>~~0.574~~|48<br>0.529<br>~~0.574~~|48<br>0.529<br>~~0.574~~|48<br>0.529<br>~~0.574~~|||||||||||||||
||Tr|iviaQ||||||||0.514<br>0.52<br>0.5|0.514<br>0.52<br>0.5|0.514<br>0.52<br>0.5|0.514<br>0.52<br>0.5|0.514<br>0.52<br>0.5|0.514<br>0.52<br>0.5|0.514<br>0.52<br>0.5|48<br>0.529<br>~~0.574~~|48<br>0.529<br>~~0.574~~|||||||||||||||||
||Tr|iviaQ|~~0.371~~<br>~~0.382~~<br>~~0.4~~|~~0.371~~<br>~~0.382~~<br>~~0.4~~|~~0.371~~<br>~~0.382~~<br>~~0.4~~|~~0.371~~<br>~~0.382~~<br>~~0.4~~|~~0.371~~<br>~~0.382~~<br>~~0.4~~|~~0.371~~<br>~~0.382~~<br>~~0.4~~|~~0.371~~<br>~~0.382~~<br>~~0.4~~|~~48~~<br>0.402<br>0.392|~~48~~<br>0.402<br>0.392|~~48~~<br>0.402<br>0.392|~~48~~<br>0.402<br>0.392||||||||||||||||||||||
||Tr|iviaQ|~~0.371~~<br>~~0.382~~<br>~~0.4~~|~~0.371~~<br>~~0.382~~<br>~~0.4~~|~~0.371~~<br>~~0.382~~<br>~~0.4~~|~~0.371~~<br>~~0.382~~<br>~~0.4~~|~~0.371~~<br>~~0.382~~<br>~~0.4~~|~~0.371~~<br>~~0.382~~<br>~~0.4~~|||||||||||||||||||||||||||
||Tr|iviaQ|09|09|09|09|||||||||||||||||||||||||||||
||Tr|||0.258<br>0.253|0.258<br>0.253|0.258<br>0.253|||||||||||||||||||||||||||||
||||||||||||||||||||||||||||||||||||
||Tr<br>SE|iviaQ<br> (Lla|iviaQ<br> (Lla|A<br> ma|) (ou|) (ou|)|B|ioAS<br>S|ioAS<br>S|Q<br>E (D|eBE|eBE|a) (o|urs)|NQ<br>|NQ<br>||R-|R-|ning|S|QuA|QuA|D<br>R-|Tuni|Tuni|U||Mult<br>|Mult<br>|Origi|nal|nal|
||||||||||||||||||||||||||||||||||||
||||||||||||||||||||||||||||||||||||



Figure 2: Our method, SE (Llama), matches or outperforms R-Tuning and R-Tuning-U for Long-QA
and Short-QA in out-of-distribution experiments. Mean Accuracy-Engagement Distances (AEDs) are
shown on top of each bar. Standard deviations are shown as error bars. The lower the AED, the better.


Table 1, we observe that, in aggregate, fine-tuning on R-Tuning and R-Tuning-U leads to models
that often are _worse_ than the original model. In contrast, fine-tuning on SE (Llama) yields models
that **significantly outperform** existing methods and the original model. Notably, if we compare
SE (Llama) with R-Tuning and R-Tuning-U, we obtain up to 30.1% and 8.7% reduction in AEDs
for in-distribution experiments for Long-QA and Short-QA respectively. For out-of-distribution
experiments, we obtain reductions up to 25.0% and 6.9% for Long-QA and Short-QA.


7


800


700


600


500


400


300


200


100


0



0 50 100 150 200
No. Incorrect



0 100 200 300 400
No. Incorrect



0 100 200 300 400
No. Incorrect



350


300


250


200


150


100


50


0



600


500


400


300


200


100


0



0 50 100 150 200 250 300 350
No. Incorrect



500


400


300


200


100


0



SE (Llama) SE (DeBERTa) R-Tuning R-Tuning-U


Figure 3: SE (Llama) forms a frontier over other methods in the Long-QA Adaptation Plot. Each
point represents a fine-tuned model trained at a specific threshold.


**Fine-Tuning with Semantic Entropy Is a Pareto Improvement For Long-QA.** We present the
Long-QA adaptation plot in Figure 3 as a result of All-Threshold Evaluation. Here, we observe
that **models** **fine-tuned** **with** **SE** **(Llama)** **form** **a** **frontier** **over** **models** **fine-tuned** **using** **other**
**methods** . Since the AED is the Euclidean distance from an ideal model that has maximum accuracy
and engagement (the top left corner of the adaptation plot), then it follows that **models fine-tuned**
**with SE (Llama) attains lower AEDs no matter the uncertainty threshold on out-of-distribution**
**settings** **for** **Long-QA** . This further underscores the effectiveness of semantic entropy as an
abstention fine-tuning method. It is difficult, however, to discern an overall trend in the Short-QA
adaptation plot, which we show at Appendix A.5, where it seems that no method forms a frontier
above another. This may be because there are lesser lexical and syntactical variances in Short-QA
than in Long-QA, which leads to weaker methods such as SE (DeBERTa) and R-Tuning Entropy
performing equivalently as SE (Llama) at numerous thresholds.


**Takeaways.** We can see models fine-tuned with semantic entropy, in most cases, outperform models
fine-tuned with R-Tuning and R-Tuning-U, which indicates that semantic entropy is a clearer signal
to reduce hallucinations than a model’s correctness on a question and classical entropy. This is
because semantic entropy is a more delineative statistic of a model’s uncertainty than both R-Tuning
and R-Tuning-U, which facilitates model learning and generalisation. Our findings represent an
advancement in fine-tuning methodologies for both Long-QA and Short-QA answering settings,
opening new avenues for reducing hallucinations for both short-form and long-form generations
without the reliance on exhaustively labeled datasets.


**Limitations.** We note that in some instances of our single dataset experiments, the original model
still attains lower AEDs than the fine-tuning approaches we have explored in our experiments. Due to
resource constraints, we suspect that this is due to the relatively low LoRA rank _r_ = 8 employed
during training and the relatively small number of data points (2000) that we have used to train our
models. Indeed, despite convergence on the training set, we observe that our fine-tuned models cannot
exactly fit the training set. Future work could include full fine-tuning and to scale up our experiments
to include more training points. We would also like to improve the reliability of our adaptation plots
by repeating each threshold experiment multiple times.


**8** **Conclusion**


In this work, we proposed using semantic entropy to fine-tune LLMs to abstain from answering
questions beyond their capabilities. Under our proposed evaluation metric, the Accuracy-Engagement
Distance which accounts for both the accuracy and engagement of a model, we demonstrated that
models fine-tuned on semantic entropy matched or outperformed models fine-tuned via existing
methods that relied on ground-truth labels or classical entropy.


Other than scaling up our experiments as discussed previously, future work may entail experimenting
with other open-source LLMs to see if our conclusions have a generalising effect. Furthermore,
future work can adapt our work to apply to longer generations, i.e. paragraphs or biographies.
Finally, given the success of using semantic entropy to reduce hallucinations and recent evidence


8


that the model may be computing semantic entropy internally (Kossen et al., 2024), future work
can also explore using semantic entropy as a fine-tuning method to calibrate models and comparing
its viability with previous works (Zhang et al., 2024; Kadavath et al., 2022).


**Acknowledgments.** The authors thank Neil Band and members of the OATML group for insightful
discussions throughout the development of this paper.


**References**


G. Ahdritz, T. Qin, N. Vyas, B. Barak, and B. L. Edelman. Distinguishing the knowable from the
unknowable with language models, 2024. URL `[https://arxiv.org/abs/2402.03563](https://arxiv.org/abs/2402.03563)` .

A. Azaria and T. Mitchell. The internal state of an llm knows when it’s lying, 2023. URL `[https:](https://arxiv.org/abs/2304.13734)`
`[//arxiv.org/abs/2304.13734](https://arxiv.org/abs/2304.13734)` .


F. Brahman, S. Kumar, V. Balachandran, P. Dasigi, V. Pyatkin, A. Ravichander, S. Wiegreffe, N. Dziri,
K. Chandu, J. Hessel, Y. Tsvetkov, N. A. Smith, Y. Choi, and H. Hajishirzi. The art of saying no:
Contextual noncompliance in language models, 2024. URL `[https://arxiv.org/abs/2407.](https://arxiv.org/abs/2407.12043)`
`[12043](https://arxiv.org/abs/2407.12043)` .


N. Chakraborty, M. Ornik, and K. Driggs-Campbell. Hallucination detection in foundation models
for decision-making: A flexible definition and review of the state of the art, 2024. URL `[https:](https://arxiv.org/abs/2403.16527)`
`[//arxiv.org/abs/2403.16527](https://arxiv.org/abs/2403.16527)` .

Q. Cheng, T. Sun, X. Liu, W. Zhang, Z. Yin, S. Li, L. Li, Z. He, K. Chen, and X. Qiu. Can ai
assistants know what they don’t know?, 2024. URL `[https://arxiv.org/abs/2401.13275](https://arxiv.org/abs/2401.13275)` .

Y.-S. Chuang, Y. Xie, H. Luo, Y. Kim, J. Glass, and P. He. Dola: Decoding by contrasting layers
improves factuality in large language models, 2024. URL `[https://arxiv.org/abs/2309.](https://arxiv.org/abs/2309.03883)`
`[03883](https://arxiv.org/abs/2309.03883)` .

S. Farquhar, J. Kossen, L. Kuhn, and Y. Gal. Detecting hallucinations in large language models
using semantic entropy. _Nature_, 630(8017):625–630, Jun 2024. ISSN 1476-4687. doi: 10.1038/
s41586-024-07421-0. URL `[https://doi.org/10.1038/s41586-024-07421-0](https://doi.org/10.1038/s41586-024-07421-0)` .

S. Feng, W. Shi, Y. Wang, W. Ding, V. Balachandran, and Y. Tsvetkov. Don’t hallucinate, abstain:
Identifying llm knowledge gaps via multi-llm collaboration, 2024. URL `[https://arxiv.org/](https://arxiv.org/abs/2402.00367)`
`[abs/2402.00367](https://arxiv.org/abs/2402.00367)` .

Google. Gemini: A family of highly capable multimodal models, 2024. URL `[https://arxiv.](https://arxiv.org/abs/2312.11805)`
`[org/abs/2312.11805](https://arxiv.org/abs/2312.11805)` .


T. Han, A. Kumar, C. Agarwal, and H. Lakkaraju. Medsafetybench: Evaluating and improving the
medical safety of large language models, 2024. URL `[https://arxiv.org/abs/2403.03744](https://arxiv.org/abs/2403.03744)` .


P. He, X. Liu, J. Gao, and W. Chen. Deberta: Decoding-enhanced bert with disentangled attention,
2021. URL `[https://arxiv.org/abs/2006.03654](https://arxiv.org/abs/2006.03654)` .


E. J. Hu, Y. Shen, P. Wallis, Z. Allen-Zhu, Y. Li, S. Wang, L. Wang, and W. Chen. Lora: Low-rank
adaptation of large language models, 2021. URL `[https://arxiv.org/abs/2106.09685](https://arxiv.org/abs/2106.09685)` .

L. Huang, W. Yu, W. Ma, W. Zhong, Z. Feng, H. Wang, Q. Chen, W. Peng, X. Feng, B. Qin, and
T. Liu. A survey on hallucination in large language models: Principles, taxonomy, challenges, and
open questions, 2023. URL `[https://arxiv.org/abs/2311.05232](https://arxiv.org/abs/2311.05232)` .


Z. Ji, N. Lee, R. Frieske, T. Yu, D. Su, Y. Xu, E. Ishii, Y. J. Bang, A. Madotto, and P. Fung. Survey of
hallucination in natural language generation. _ACM Computing Surveys_, 55(12):1–38, Mar. 2023a.
ISSN 1557-7341. doi: 10.1145/3571730. URL `[http://dx.doi.org/10.1145/3571730](http://dx.doi.org/10.1145/3571730)` .

Z. Ji, Z. Liu, N. Lee, T. Yu, B. Wilie, M. Zeng, and P. Fung. Rho ( _ρ_ ): Reducing hallucination in
open-domain dialogues with knowledge grounding, 2023b. URL `[https://arxiv.org/abs/](https://arxiv.org/abs/2212.01588)`
`[2212.01588](https://arxiv.org/abs/2212.01588)` .

M. Joshi, E. Choi, D. S. Weld, and L. Zettlemoyer. Triviaqa: A large scale distantly supervised
challenge dataset for reading comprehension, 2017. URL `[https://arxiv.org/abs/1705.](https://arxiv.org/abs/1705.03551)`
`[03551](https://arxiv.org/abs/1705.03551)` .


S. Kadavath, T. Conerly, A. Askell, T. Henighan, D. Drain, E. Perez, N. Schiefer, Z. Hatfield-Dodds,
N. DasSarma, E. Tran-Johnson, S. Johnston, S. El-Showk, A. Jones, N. Elhage, T. Hume, A. Chen,


9


Y. Bai, S. Bowman, S. Fort, D. Ganguli, D. Hernandez, J. Jacobson, J. Kernion, S. Kravec,
L. Lovitt, K. Ndousse, C. Olsson, S. Ringer, D. Amodei, T. Brown, J. Clark, N. Joseph, B. Mann,
S. McCandlish, C. Olah, and J. Kaplan. Language models (mostly) know what they know, 2022.
URL `[https://arxiv.org/abs/2207.05221](https://arxiv.org/abs/2207.05221)` .

J. Kossen, J. Han, M. Razzak, L. Schut, S. Malik, and Y. Gal. Semantic entropy probes: Robust and
cheap hallucination detection in llms, 2024. URL `[https://arxiv.org/abs/2406.15927](https://arxiv.org/abs/2406.15927)` .

L. Kuhn, Y. Gal, and S. Farquhar. Semantic uncertainty: Linguistic invariances for uncertainty
estimation in natural language generation, 2023. URL `[https://arxiv.org/abs/2302.09664](https://arxiv.org/abs/2302.09664)` .


T. Kwiatkowski, J. Palomaki, O. Redfield, M. Collins, A. Parikh, C. Alberti, D. Epstein, I. Polosukhin,
J. Devlin, K. Lee, K. Toutanova, L. Jones, M. Kelcey, M.-W. Chang, A. M. Dai, J. Uszkoreit, Q. Le,
and S. Petrov. Natural questions: A benchmark for question answering research. _Transactions_
_of the Association for Computational Linguistics_, 7:452–466, 2019. doi: 10.1162/tacl_a_00276.
URL `[https://aclanthology.org/Q19-1026](https://aclanthology.org/Q19-1026)` .

P. Lewis, E. Perez, A. Piktus, F. Petroni, V. Karpukhin, N. Goyal, H. Küttler, M. Lewis, W. tau Yih,
T. Rocktäschel, S. Riedel, and D. Kiela. Retrieval-augmented generation for knowledge-intensive
nlp tasks, 2021. URL `[https://arxiv.org/abs/2005.11401](https://arxiv.org/abs/2005.11401)` .

L. Liu, Y. Pan, X. Li, and G. Chen. Uncertainty estimation and quantification for llms: A simple
supervised approach, 2024. URL `[https://arxiv.org/abs/2404.15993](https://arxiv.org/abs/2404.15993)` .

I. Loshchilov and F. Hutter. Decoupled weight decay regularization, 2019. URL `[https://arxiv.](https://arxiv.org/abs/1711.05101)`
`[org/abs/1711.05101](https://arxiv.org/abs/1711.05101)` .

Meta. The llama 3 herd of models, 2024. URL `[https://arxiv.org/abs/2407.21783](https://arxiv.org/abs/2407.21783)` .

OpenAI. Gpt-4 technical report, 2024. URL `[https://arxiv.org/abs/2303.08774](https://arxiv.org/abs/2303.08774)` .

P. Rajpurkar, J. Zhang, K. Lopyrev, and P. Liang. Squad: 100,000+ questions for machine comprehension of text, 2016. URL `[https://arxiv.org/abs/1606.05250](https://arxiv.org/abs/1606.05250)` .

V. Rawte, S. Chakraborty, A. Pathak, A. Sarkar, S. M. T. I. Tonmoy, A. Chadha, A. P. Sheth,
and A. Das. The troubling emergence of hallucination in large language models – an extensive
definition, quantification, and prescriptive remediations, 2023. URL `[https://arxiv.org/abs/](https://arxiv.org/abs/2310.04988)`
`[2310.04988](https://arxiv.org/abs/2310.04988)` .

W. Shi, X. Han, M. Lewis, Y. Tsvetkov, L. Zettlemoyer, and S. W. tau Yih. Trusting your evidence:
Hallucinate less with context-aware decoding, 2023. URL `[https://arxiv.org/abs/2305.](https://arxiv.org/abs/2305.14739)`
`[14739](https://arxiv.org/abs/2305.14739)` .

K. Shuster, S. Poff, M. Chen, D. Kiela, and J. Weston. Retrieval augmentation reduces hallucination
in conversation, 2021. URL `[https://arxiv.org/abs/2104.07567](https://arxiv.org/abs/2104.07567)` .


K. Tian, E. Mitchell, H. Yao, C. D. Manning, and C. Finn. Fine-tuning language models for factuality,
2023. URL `[https://arxiv.org/abs/2311.08401](https://arxiv.org/abs/2311.08401)` .

S. M. T. I. Tonmoy, S. M. M. Zaman, V. Jain, A. Rani, V. Rawte, A. Chadha, and A. Das. A
comprehensive survey of hallucination mitigation techniques in large language models, 2024. URL
`[https://arxiv.org/abs/2401.01313](https://arxiv.org/abs/2401.01313)` .

G. Tsatsaronis, G. Balikas, P. Malakasiotis, I. Partalas, M. Zschunke, M. R. Alvers, D. Weissenborn,
A. Krithara, S. Petridis, D. Polychronopoulos, Y. Almirantis, J. Pavlopoulos, N. Baskiotis, P. Gallinari, T. Artiéres, A.-C. N. Ngomo, N. Heino, E. Gaussier, L. Barrio-Alvers, M. Schroeder,
I. Androutsopoulos, and G. Paliouras. An overview of the BIOASQ large-scale biomedical
semantic indexing and question answering competition. _BMC Bioinformatics_, 16(1):138, Apr.
2015.

B. Weiser. Lawyer who used ChatGPT faces penalty for made up citations. _The New York Times_,
June 2023.

B. Wen, J. Yao, S. Feng, C. Xu, Y. Tsvetkov, B. Howe, and L. L. Wang. Know your limits: A survey
of abstention in large language models, 2024. URL `[https://arxiv.org/abs/2407.18418](https://arxiv.org/abs/2407.18418)` .

R. Wolfe, I. Slaughter, B. Han, B. Wen, Y. Yang, L. Rosenblatt, B. Herman, E. Brown, Z. Qu,
N. Weber, and B. Howe. Laboratory-scale ai: Open-weight models are competitive with chatgpt
even in low-resource settings. In _The 2024 ACM Conference on Fairness,_ _Accountability,_ _and_
_Transparency_, volume 35, page 1199–1210. ACM, June 2024. doi: 10.1145/3630106.3658966.
URL `[http://dx.doi.org/10.1145/3630106.3658966](http://dx.doi.org/10.1145/3630106.3658966)` .


10


J. Yang, H. Jin, R. Tang, X. Han, Q. Feng, H. Jiang, B. Yin, and X. Hu. Harnessing the power of llms in
practice: A survey on chatgpt and beyond, 2023a. URL `[https://arxiv.org/abs/2304.13712](https://arxiv.org/abs/2304.13712)` .


Y. Yang, E. Chern, X. Qiu, G. Neubig, and P. Liu. Alignment for honesty, 2023b. URL `[https:](https://arxiv.org/abs/2312.07000)`
`[//arxiv.org/abs/2312.07000](https://arxiv.org/abs/2312.07000)` .


H. Zhang, S. Diao, Y. Lin, Y. R. Fung, Q. Lian, X. Wang, Y. Chen, H. Ji, and T. Zhang. R-tuning:
Instructing large language models to say ‘i don’t know’, 2024. URL `[https://arxiv.org/abs/](https://arxiv.org/abs/2311.09677)`
`[2311.09677](https://arxiv.org/abs/2311.09677)` .


Y. Zhang, Y. Li, L. Cui, D. Cai, L. Liu, T. Fu, X. Huang, E. Zhao, Y. Zhang, Y. Chen, L. Wang, A. T.
Luu, W. Bi, F. Shi, and S. Shi. Siren’s song in the ai ocean: A survey on hallucination in large
language models, 2023. URL `[https://arxiv.org/abs/2309.01219](https://arxiv.org/abs/2309.01219)` .


**A** **Appendix / supplemental material**


**A.1** **Answering Setting Prompts**


**A.1.1** **Long-QA Answering Setting**


In the Long-QA setting, we instruct models to generate free-form, sentence-length responses using
the following prompt:





Figure 4: Long-QA Free-form Prompt.


**A.1.2** **Short-QA Answering Setting**


In the Short-QA setting, we use the following prompt to instruct the model to generate short-form
responses not more than a few words:


11


Figure 5: Prompt for Short-QA.


**A.2** **Accuracy Evaluation**


Given a standard response of our model to a question _q_, and the ground-truth label for that question,
we use LLAMA-3-8B-INSTRUCT and the following prompt to assess the accuracy of the standard
response:





Figure 6: Prompt template for accuracy evaluation.


**A.3** **Semantic Entropy Implementation**


The non-trivial part of computing the semantic entropy lies in computing the semantic equivalence
relation _R_ ( _·, ·_ ) that is true if two generations share the same semantic meaning (Section 3). While
there are potentially many choices to implement _R_ ( _·, ·_ ), in this work, we follow Kuhn et al. (2023) in
using the idea of bi-directional entailment to determine semantic equivalence. Here, we treat two
generations **s** and **s** _[′]_ to be semantically equivalent if and only if **s** logically entails **s** _[′]_ and vice versa.
For example, ‘The capital of France is Paris’ and ‘Paris is the capital of France’ share the same
meaning as they logically entail each other. However, as we are supplied with a question, we must
constrain our entailment to hold within the context of the question. For example, the generations
‘Paris’ and ‘The capital of France is Paris’ on their own do not entail one another as the former only
declares ‘Paris’, without stating that it is the capital of France. However, if the generations were
produced with respect to the question ‘What is the capital of France?’, then within the context of the
question, both generations entail one another.


12


As described in Section 6, we assign two variants of semantic entropy to each question, SE (DeBERTa)
and SE (Llama), each using different language models to perform entailment. The first of these uses
DeBERTa-NLI, which follows Kuhn et al. (2023)’s proposal, and the second of these uses Llama3-70B-Instruct, which is inspired from Farquhar et al. (2024)’s findings that LLMs can perform
entailment well.


**A.3.1** **Entailment using DeBERTa-NLI**


DeBERTa-NLI (He et al., 2021) is a language model based on the transformer encoder-decoder
architecture that is fine-tuned on the task of natural language inference (NLI). In NLI, we are given
a ‘premise’ and a ‘hypothesis’, and the task is to classify whether the hypothesis logically follows
from the premise (entailment), logically contradicts the premise (contradiction), or is logically
undetermined given the premise (neutral). To use DeBERTa-NLI to see whether two generations **s**
and **s** _[′]_ entail one another given the question, we first concatenate the question to each **s** and **s** _[′]_ and
then concatenate both concatenations together using a special token. DeBERTa-NLI then classifies
this concatenation as ‘entailment’, ‘contradiction’, or ‘neutral’. We next do this for the other direction
and only deem that **s** and **s** _[′]_ are semantically equivalent if DeBERTa-NLI says ‘entailment’ for both
directions.


**A.3.2** **Entailment using Llama-3-70B-Instruct**


Llama-3-70B-Instruct is the 70 Billion-parameter variant of Llama-3-8B-Instruct. Leveraging Llama3-70B-Instruct’s ability to follow instructions and to perform NLP tasks through in-context learning,
we used a 5-shot ICL prompt to do question-dependent (uni-directional) NLI (Appendix A.3.2).
Equivalently to the above, we only deem two generations **s** and **s** _[′]_ as semantically equivalent if
Llama-3-70B-Instruct produces ‘entailment’ for both directions.





13


Figure 7: Uni-directional entailment ICL prompt.


Having shown how to implement the semantic equivalence relation _R_ via one of the two methods above, we can now cluster the high-temperature responses into semantic equivalence classes
_C_ 1 _, . . ., Cm_ . The discrete semantic entropy then follows via direct calculation of Equation (6). We
show a concrete implementation of semantic clustering and the subsequent calculation of discrete
semantic entropy in Code Block 1.


1 `from` `collections` `import` `Counter`


2 `def` `semantic_entropy (question,` `high_temp_generations ):`


3 `next_id` `=` `0`


4 `assignment` `=` `[-1]` `*` `len` `( high_temp_generations )`


5 `for` `i,` `s1` `in` `enumerate` `( high_temp_generations ):`


6 `if` `assignment` `!=` `-1:`


7 `continue`


8 `#` `If` `s1` `has` `not` `been` `assigned` `an` `id,` `assign` `it` `next_id.`


9 `assignment[i]` `=` `next_id`


10 `for` `j,` `s2` `in` `enumerate` `( high_temp_generations [i` `+` `1:]):`


11 `if` `is_semantically_equivalent (question,` `s1,` `s2):`


12 `assignment[j]` `=` `assignment[i]`


13 `next_id` `+=` `1`


14


14 `freq_list` `=` `list` `(Counter(assignment.values ()))`


15 `semantic_entropy` `=` `scipy.stats.entropy(freq_list)`


16 `return` `semantic_entropy`


Code Block 1: `Python` code to compute discrete semantic entropy.


**A.4** **Hyperparameter Details**


All of our experiments under both answering settings use a global hyperparameter configuration.
We found that a learning rate of 3 _×_ 10 _[−]_ [5], a batch size of 48, and training for 7 epochs under a
cosine annealing schedule with a cycle of 0.2 yields decent convergence on the training set and the
in-distribution validation set. We employed the AdamW optimiser (Loshchilov and Hutter, 2019) for
all experiments and used LoRA with _r_ = 8 on the query and value projection matrices.


**A.5** **Short-QA Out-of-Distribution Adaptation Plot**


We present the Short-QA adaptation plot in Figure 8. As we can see, the effect is less pronounced
than that of the Long-QA adaptation plot and it is harder to discern an overall trend.



0 100 200 300 400
No. Incorrect



400


350


300


250


200


150


100


50


0



0 100 200 300 400 500 600
No. Incorrect



0 100 200 300 400 500
No. Incorrect



250


200


150


100


50


0



700


600


500


400


300


200


100



0 50 100 150 200 250
No. Incorrect



600


500


400


300


200


100


0



SE (Llama) SE (DeBERTa) R-Tuning R-Tuning-U


Figure 8: Short-QA Out-of-Distribution Adaptation Plot. Each point represents a fine-tuned model
trained at a specific threshold.


**A.6** **Granular Breakdown of Experiments**


Table 2 shows a granular breakdown of our experiments for Best-Threshold Evaluation. Here, the
**Setting** column denotes how the model is trained and evaluated. For example, “Long-QA: TriviaQA

_◦_ TriviaQA” means that the model is trained under Long-QA, on the training split of TriviaQA, and
evaluated on the in-distribution validation split of TriviaQA. “Short-QA: BioASQ _◦_ SQuAD” means
that the model is trained on the training split of BioASQ and evaluated on all SQuAD data points
under the Short-QA answering setting.


15


Table 2: Granular Breakdown of Experiments: Long-QA and Short-QA mean _±_ standard deviation
Accuracy-Engagement Distances for each fine-tuning method, the lower the better. Green indicates
lowest, blue indicates second-lowest.


**Setting** **R-Tuning** **R-Tuning-U** **SE (DeBERTa)** (ours) **SE (Llama)** (ours) **Original Model**


16


