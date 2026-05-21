## **BOTTLEHUMOR: Self-Informed Humor Explanation using the Information** **Bottleneck Principle**

**EunJeong Hwang** [1] _[,]_ [2] **, Peter West** [1] **, and Vered Shwartz** [1] _[,]_ [2]

1 University of British Columbia 2 Vector Institute for AI
{ejhwang,pwest,vshwartz}@cs.ubc.ca



**Abstract**


Humor is prevalent in online communications
and it often relies on more than one modality
(e.g., cartoons and memes). Interpreting humor
in multimodal settings requires drawing on diverse types of knowledge, including metaphorical, sociocultural, and commonsense knowledge. However, identifying the most useful
knowledge remains an open question. We introduce BOTTLEHUMOR, a method inspired by
the information bottleneck principle that elicits relevant world knowledge from vision and
language models which is iteratively refined
for generating an explanation of the humor
in an unsupervised manner. Our experiments
on three datasets confirm the advantage of our
method over a range of baselines. Our method
can further be adapted in the future for additional tasks that can benefit from eliciting and
conditioning on relevant world knowledge and
open new research avenues in this direction.


**1** **Introduction**


Humor is an effective communication tool (Stauffer, 1999; Wanzer et al., 2010; Vartabedian, 1993;
Kasulis, 1989) that can manifest in various forms,
including puns, exaggerated facial expressions, absurd behaviors, and incongruities (Shaw, 2010). It
is shaped by multiple factors such as culture, social interactions, societal phenomena, and personal
imagination (Warren and Mcgraw, 2015; Warren
et al., 2020).
In particular, humor is prevalent in online communications (McCulloch, 2020), often spanning
multiple modalities (e.g., cartoons and memes;
Shifman, 2013). Interpreting humor across modalities requires “reading between the lines”, connecting textual and visual elements to grasp the meaning (Warren et al., 2020). For example, in Fig. 1,
connecting the tooth fairy depicted in the image
carrying a plunger to the caption, “In this economy, it’s good to have an extra trade”, creates the



Figure 1: Humor understanding requires understanding
world knowledge. BOTTLEHUMOR aims to reduce redundancy in existing inputs (e.g. image descriptions)
while increasing relevance to candidate explanations.


humorous interpretation that in this state of the
economy, even the imaginary fairy needs a side job
as a plumber.
Several datasets for multimodal humor understanding tasks were proposed, where models are
tasked with generating free-text humor explanations for an image and a caption (Hwang and
Shwartz, 2023; Hessel et al., 2023; Nandy et al.,
2024; Hu et al., 2024b). However, they are often
overlooked in vision-and-language models (VLMs)
evaluations, possibly due to the subjective nature
of humor and the challenges in evaluating free-text
explanations. With that said, VLMs have demonstrated remarkable visual reasoning capabilities on
datasets requiring scientific knowledge (Lu et al.,
2022), commonsense knowledge (Schwenk et al.,
2022), and spatial reasoning (Liu et al., 2023) and
there is a prominent line of work on enhancing multimodal reasoning (Zhang et al., 2024; Mitra et al.,
2024; Mondal et al., 2024; Hu et al., 2024a).
In this paper, we introduce BOTTLEHUMOR, a



**Redundancy**










method inspired by the information bottleneck (IB)
principle. BOTTLEHUMOR leverages VLMs to
generate and iteratively refine implications and explanations from an image and text, selecting those
most relevant for explaining the humor in the image
and maximizing information gain. As an off-theshelf method, it is applicable to any VLM.

We evaluate BOTTLEHUMOR on three multimodal humor explanation datasets: MemeCap
(Hwang and Shwartz, 2023), NewYorker (Hessel
et al., 2023), and YesBut (Nandy et al., 2024).
Prior work relied on reference-based automatic
metrics that overlook lexical variability and the
open-endedness of explanations and costly human
evaluation. Leveraging the strong text understanding capabilities of LLMs, we propose new automatic evaluation metrics that resemble precision
and recall, and better correlate with human judgments. BOTTLEHUMOR improves _F_ 1 by up to 8.2,
4.3, and 2.8 points on MemeCap, NewYorker, and
YesBut, respectively, compared to zero-shot baselines and outperforms existing self-refine methods
that merely iterate on and refine the explanation
without generating intermediate implications. Our
results highlight the importance of incorporating
implications, paving the way for future research on
incorporating diverse world knowledge in complex
reasoning tasks. [1]


**2** **Related Work**


**Multimodal** **Humor** **Understanding.** Earlier
works on humor understanding primarily focus on
detection in images and videos (Chandrasekaran
et al., 2016; Castro et al., 2019; Patro et al., 2021).
Recent work shifted to generative tasks, typically
explaining humor in an image (Hwang and Shwartz,
2023; Hessel et al., 2023; Nandy et al., 2024) or
video (Hyun et al., 2024; Hasan et al., 2019). Understanding and explanation generation remain underexplored due to the complexity of the task and
free-text evaluation. The V-Flute dataset (Saakyan
et al., 2024) addresses this by re-casting this as
predicting whether an image containing humorous
elements or visual metaphors _entails_ a given description, while providing justification. We focus
on the generative version of this task, proposing a
method to enhance humor explanation and a framework for automatic evaluation.


1Our code and data are available at:
[https://github.com/eujhwang/bottle-humor](https://github.com/eujhwang/bottle-humor)



**Iterative LLM-based Reasoning.** Many methods elicit knowledge from the LLM for intermediate reasoning steps. Shwartz et al. (2020) elicited
clarification questions and answers, then incorporated these in the input. Modern Few-shot prompting removed the need for supervision for these explanations (Marasovic et al., 2022; Wiegreffe et al.,
2022). One popular approach is Chain-of-Thought
(CoT; Wei et al., 2022). CoT steers LLMs to generate intermediate reasoning steps towards the final answer, improving multi-step arithmetic, commonsense, and symbolic reasoning tasks. Relevant
successor approaches include self-refine (Madaan
et al., 2023) which prompts LLMs to iteratively improve their answers with self-generated feedback.
Eliciting knowledge from LLMs to improve predictions has been used for opinion understanding
(Hwang et al., 2024; Hoyle et al., 2023), factuality (Akyürek et al., 2024), and consistency (Liang
et al., 2024).

CoT has been adapted to the vision and language
setting (Zhang et al., 2024) by adding external
knowledge (Mondal et al., 2024), extracting a scene
graph (Mitra et al., 2024), or using visual sketches
as intermediate reasoning steps (Hu et al., 2024a).
Most existing works focus on benchmarks such as
ScienceQA (Lu et al., 2022) and visual commonsense reasoning (Schwenk et al., 2022), with (a)
definitive/objective answers; and (b) simple evaluation metrics (e.g., ScienceQA is multiple-choice).
We focus on multimodal explanation generation
tasks in which the answers are open-ended and nuanced. As in CoT, we elicit intermediate reasoning
steps from the models, but propose a novel method
using the information bottleneck principle to guide
generation and selection of useful knowledge for a
correct explanation.


**Information** **Bottleneck** **Principle.** The Information Bottleneck principle (IB; Tishby et al.,
1999), based on information theory, extracts relevant information from an input while minimizing
redundancy (Sec. 3.1). It has been applied to a wide
range of tasks (Ben-Shaul et al., 2023), including
representation learning (Wu et al., 2020; Lee et al.,
2021), deep learning (Saxe et al., 2018; Kawaguchi
et al., 2023), summarization (West et al., 2019; Ju
et al., 2021; Li et al., 2021), speech recognition
(Hecht et al., 2009), and multimodal learning (Mai
et al., 2023; Fang et al., 2024). Most prior works apply the IB principle during training to learn useful
feature representations, with the exception of West


et al. (2019); Ju et al. (2021), who use IB for unsupervised summarization. In this work, we extend
the IB principle to multimodal humor understanding to identify relevant LLM world knowledge.


**3** **BOTTLEHUMOR**


Given a humoristic image along with an accompanying text ( _caption_ ), our goal is to generate a
descriptive explanation of the humor. For example,
in Figure 2, a fairy woman with a plunger looking
at a boy can be humorously explained as “The humor comes from a fairy with a plunger, taking a
side job because of a tough economy” (from the
NewYorker dataset; Hessel et al., 2023).
We propose BOTTLEHUMOR (Figure 2), a multihop reasoning method inspired by the IB principle
(Sec. 3.1). We integrate the visual and textual components to generate implications (Sec. 3.2). We
then select the most useful implications by employing the IB principle (Sec. 3.3), and add them to the
input to generate candidate explanations (Sec. 3.4).
This iterative process alternates between refining
implications and explanations.


**3.1** **The Information Bottleneck Principle**


We use the Information Bottleneck principle (IB;
Tishby et al., 1999) to select useful implications in
BOTTLEHUMOR. IB aims to extract the most relevant information from a given input variable while
minimizing redundancy. Specifically, IB seeks to
compress the input source _S_ into a representation
_S_ ˆ while retaining the information most relevant to
predicting the target _Y_ . This objective is formulated as minimizing the following equation:


_I_ ( _S,_ _S_ [ˆ] ) _−_ _αI_ ( _S, Y_ [ˆ] )


where _I_ denotes mutual information, and _α_ is a parameter to balance compression term _I_ ( _S,_ _S_ [ˆ] ) with
relevance term _I_ ( _S, Y_ [ˆ] ).


**3.2** **Eliciting Multi-Hop Implications**


First, we generate a set of natural language implications of the input. The goal of this step is to
discover connections across different objects, concepts, and situations described in the input.


**Image Descriptions.** As a first step, we provide
the image _I_ to a VLM to generate a detailed _image_
_description D_, focusing on the scene and objects
while ignoring the humoristic meaning behind the
image. We limit the description to a maximum of
five sentences.



**Implications.** Using these descriptions, the VLM
elicits _implications_ : commonsense knowledge, social norms, and possible connections for the objects
in the description _D_ and the caption _C_ . Implications generated at hop _h_ are denoted as _P_ _[h]_ =
_{p_ _[h]_ 1 _[, p][h]_ 2 _[, . . ., p][h]_ _j_ _[}]_ [.]
In the first hop, the implications are derived from
the image _I_, its caption _C_, and a subset of two image descriptions _D_, selected via a sliding window
to balance efficiency (i.e., input length and cost)
and coverage. From the second hop onward, we
provide the VLM with _candidate explanations_ (see
below) and one of the previously selected top- _k_
implications (Sec. 3.3).
When the number of generated implications exceeds 15, we cluster them using sentence embeddings and select the implications closest to each
cluster’s centroid. This step reduces redundancy
while preserving diversity.


**Candidate Explanations.** To guide implication
selection for generating the correct output, we provide the image _I_ and caption _C_ to the VLM to
generate a set of _candidate_ _explanations_ at each
hop: _R_ _[h]_ = _{r_ 1 _[h][, r]_ 2 _[h][, . . ., r]_ _k_ _[h][}]_ [.] [One candidate expla-]
nation acts as an initial hypothesis, refined iteratively when additional information (implications)
becomes available. In the first hop, we generate
candidate explanations by providing the VLM with
the image _I_, caption _C_, and descriptions _D_ . From
the second hop onward, we condition—in addition
to the previous inputs—on each of the _k_ implications selected in the previous hop (§3.3) to generate
_k_ candidate explanations. The prompts used for
generating image descriptions, implications, and
candidate explanations are in Appendix F.


**3.3** **Selecting and Refining Useful Implications**


We aim to select the top _k_ most useful implications
at each hop, which should add meaningful information beyond the image and caption while providing
relevant context for generating a target response.
These requirements lend themselves to the two core
IB components: compression and relevance.


**Compression.** The compression term is used to
ensure that new implications provide additional
information beyond what is already known. We
measure the redundancy of each implication generated in the current hop _h_, _{Pj_ _[h][}]_ _j_ _[J]_ =1 [with the inputs]
_X_ _[h]_ = _{C, D, P_ _[h][−]_ [1] _}_, which include the image,
caption, and implications generated at previous
hops (when applicable). We can think of this as


the caption, image description, implications from
previous hops, and the target implication:


_I_ ˆ( _Pj_ _[h][, Y]_ [ ) = min] _i_ _|_ _Z_ [ˆ] _j_ _[h]_ [))]
_i∈I_ [(CE(] _[R][h][−]_ [1]


Cross-entropy values tend to be lower for short
candidate explanations, leading to abnormally low
scores for low-quality responses. To address this,
we introduce a length penalty to adjust for deviations from the average response length. Responses
significantly shorter or longer than the average receive a larger penalty. We incorporate a scaling
factor _β_, defined as the ratio of the average crossentropy to the average length. The length penalty
is then formulated as:


_CE_ ¯
_LPi_ = _β · |Li −_ _L_ [¯] _|,_ _β_ =

_L_ ¯















where _α_ is a hyperparameter that controls the tradeoff between the compression and relevance terms.
In our experiments, we set _α_ = 0 _._ 7, based on our
empirical observation. A detailed analysis of the
effect of varying _α_ is provided in Appendix E.
We use the implications in each hop to refine
the candidate explanations in the next hop and vice
versa. To avoid excessive calculation during the
implication refinement step, we keep the number
of candidate explanations to a maximum of three
based on the cross entropy scores computed using all existing inputs. These inputs, denoted as
_Z_ ˆ _j_ _[h]_ [=] _[{][C, D, P]_ _j_ _[ h][, R]_ _i_ _[h][−]_ [1] _}_, include caption, image
descriptions, current hop implications, and previous hop candidate explanations. We then select
top- _k_ candidate explanations ( _k_ = 3) in current


hop candidate explanations _Ri_ _[h]_ [that minimize the]
cross-entropy:

_R_ top- _[h]_ _k_ [= arg] _[ min]_ _i∈I,|I|_ = _k_ [CE(] _[R]_ _i_ _[h]_ _[|]_ _[Z]_ [ˆ] _j_ _[h]_ [)] (2)


In our experiments, we set the number of hops _H_
to 2 and the number of reasoning chains _k_ to 3.


**3.4** **Generating Final Answer**


After _H_ iterations of refinement, we generate the
final answer. As for candidate explanation generation in earlier hops, we provide the VLM with the
image _I_, its caption _C_, the _k_ implications selected
in the previous hop (Eq. 1), and the _k_ candidate
answers selected in the previous hop (Eq. 2), instructing it to generate a response.
We used Sentence Transformer [2] for all sentence
embeddings. The prompts for generating multi-hop
implications and explanations are in Appendix F.


**4** **Experimental Setup**


**4.1** **Datasets**


We evaluate BOTTLEHUMOR on three multimodal
humor datasets (see examples in Appendix A):


**MemeCap (Hwang and Shwartz, 2023).** Each
instance includes a meme paired with a title (social
media post to which the meme was attached). The
task is to generate a brief explanation, compared
against multiple reference explanations. The task
requires interpreting visual metaphors in relation to
the text, where models can benefit from reasoning
about background knowledge.


**New Yorker Cartoon (Hessel et al., 2023).** We
focus on the explanation generation task: given a
New Yorker cartoon and its caption, generate an
explanation for why the caption is funny given the
cartoon, requiring an understanding of the scene,
caption, and commonsense and world knowledge.


**YesBut (Nandy et al., 2024).** Each instance contains an image with two parts captioned “yes” and
“but”. The task is to explain why the image is funny
or satirical.
Since our method is unsupervised, we use the
test set portions of these datasets. Due to resource
and cost constraints, we don’t evaluate our method
on the full test sets. Instead, from each dataset,
we randomly sample 100 test instances. We repeat the process three times using different random
seeds to obtain three test splits and report average
performance and standard deviation.


2BAAI/bge-large-en-v1.5



**4.2** **Models**


We test our method with two closed-source and two
open-source VLMs.


**GPT-4o** **(Hurst** **et** **al.,** **2024)** is an advanced,
closed-source multimodal model processing text,
audio, images, and video and generating text, audio, and images. It matches GPT-4’s performance
in English text tasks with improved vision understanding.


**Gemini (Team** **et al., 2023)** is a closed-source
multimodal model from Google, available in multiple variants optimized for different tasks. We use
Gemini 1.5 Flash for evaluation and Gemini 1.5
Flash-8B for experiments, a smaller, faster variant
with comparable performance.


**Qwen2** **(Yang** **et** **al.,** **2024)** is an open-source
multimodal model built on a vision transformer
with strong visual reasoning. We use the
Qwen2-VL-7B-Instruct model, competitive with
GPT-4o on several benchmarks.


**Phi** **(Abdin** **et** **al.,** **2024)** is a lightweight,
open-source 4.2B-parameter multimodal model,
trained on synthetic and web data. We use
Phi-3.5-Vision-Instruct, optimized for precise instruction adherence.


**4.3** **Baselines**


We compare our method to four prompting-based
baselines: [3] zero-shot (ZS), Chain-of-Thought
(COT) prompting, and self-refinement with (SR)
and without (SR-NOC) a critic.
ZS generates a final explanation directly from
the image and caption using VLM. COT follows
a similar setup but instructs the model to produce
intermediate reasoning chains (Wei et al., 2022).
Additionally, we implement SR, a multimodal variant of self-refinement (Madaan et al., 2023), where
a _generator_ produces a response, and a _critic_ evaluates it based on predefined criteria. The critic’s
feedback helps refine the output iteratively [4] . Evaluation criteria include correctness, soundness, completeness, faithfulness, and clarity (details in Appendix H). SR-NOC functions identically to SR
but without a _critic model_, refining candidate explanations without feedback. This also serves as an
ablation of the implications from BOTTLEHUMOR.
Prompts for baselines are in Appendix H.


3Temperature set to 0.8 for all baselines.
4Refinement steps set to 2 for fair comparison.


**4.4** **Evaluation Metrics**


While human evaluation is often the most reliable
option for open-ended tasks like ours (Hwang and
Shwartz, 2023), it is costly at scale. LLM-based
evaluations (e.g., with Gemini 1.5 Flash) offer
a more affordable alternative but are not always
reliable (Ye et al., 2024). Prior research in fact
verification has found that modern closed-source
LLMs excel at fact checking when the complex
facts are decomposed into simpler, atomic facts
and verified individually (Gunjal and Durrett, 2024;
Samir et al., 2024). Inspired by this approach, we
propose LLM-based precision and recall scores.
For recall, we decompose the reference _ref_ into
atomic facts: _{y_ 1 _, y_ 2 _, ..., yn}_ and check whether
each appears in the predicted response _pred_ .



Recall = [1]

_n_



_n_

- 1 - _LLM_ ( _yi, pred_ ) = Yes�


_i_ =1



where _n_ is the number of atomic facts in _ref_ .
Precision follows the same process in reverse,
decomposing _pred_ into a list of atomic facts:
_{x_ 1 _, x_ 2 _, ..., xm}_ and verifying their presence in
_ref_ :



Precision = [1]

_m_



_m_

- 1 - _LLM_ ( _xi, ref_ ) = Yes�


_i_ =1



where _m_ is the number of atomic facts in _pred_ .
Both decomposition and verification use GeminiFlash-1.5 with a temperature of 0.2.
In preliminary experiments, we observed that
human references tend to omit obvious visual details, whereas model-generated answers are often
more complete, referencing visual information. To
prevent penalizing the models for these facts, we incorporate literal image descriptions (Sec 3) into the
reference by decomposing them and adding them
to the atomic facts for fairer evaluation. Based
on the precision and recall scores, we report the
macro- _F_ 1 score.
To assess the reliability of our metrics, we conducted a human evaluation on 130 random samples
across all models and datasets via CloudResearch
(details in Appendix D). Human annotators determined whether each atomic sentence appeared in
the corresponding text (e.g., reference). The average agreement between the LLM-based evaluator
and two human annotators was 77.1% ( _κ_ = 54 _._ 1),
similar to the agreement between the two annotators: 75.4% ( _κ_ = 50 _._ 8), indicating considerable



Figure 3: An example analysis of the explanations of ZS
and BOTTLEHUMOR for a New Yorker Cartoon, using
SentenceSHAP. Implications are sorted according to
their SentenceSHAP score from most to least important.


alignment with human judgment. Prompts are in
Appendix G.


**5** **Results**


We present the comparison of BOTTLEHUMOR to
the baselines (§5.1), look into the contribution of
each individual component in our method (§5.2),
justify the IB framework (§5.3), and present an
error analysis of our method’s predictions (§5.3).


**5.1** **Comparison to the Baselines**


Table 1 presents the overall experimental results.
Compared to the best of ZS and COT, BOTTLEHUMOR improves an average of 4.2, 1.6, and 2.1
_F_ 1 points on the MemeCap, NewYorker, and YesBut datasets, respectively, across models. Among
all models, GPT-4o performs best, averaging 3.4
F1 point improvement across datasets. BOTTLEHUMOR significantly boosts recall while maintaining comparable precision. This suggests that our
method effectively integrates external knowledge
to generate more comprehensive final explanations,
with a slight precision drop due to potential noise.
ZS performs reasonably well, likely due to these
strong VLMs trained on similar tasks. However,


**MemeCap** **NewYorker** **YesBut** **Avg.**
**Model** **Method** **P** **R** **F1** **P** **R** **F1** **P** **R** **F1** **F1**







Table 1: Precision, Recall, and F1 scores of models and baselines on three multimodal humor benchmarks.



**Model** **Input** **MC** **NY** **YB**


Imp 47.61 _._ 3 53.30 _._ 3 54.95 _._ 3
**GPT4o** Cand 50.01 _._ 9 56.52 _._ 7 59.73 _._ 1
**Ours** **51.5** 0 _._ 3 **58.2** 0 _._ 5 **60.5** 2 _._ 5


Imp 32.50 _._ 8 36.80 _._ 2 39.05 _._ 1
**Flash1.5** Cand 32.83 _._ 2 **37.7** 1 _._ 1 **43.7** 2 _._ 7
**Ours** **32.9** 2 _._ 2 36.71 _._ 3 43.14 _._ 7


Imp 36.22 _._ 1 **29.2** 0 _._ 9 **36.2** 1 _._ 2
**Qwen2** Cand **37.0** 1 _._ 0 **29.2** 0 _._ 9 33.50 _._ 7
**Ours** 36.21 _._ 2 28.10 _._ 2 33.51 _._ 2


Imp 23.24 _._ 0 23.21 _._ 4 26.24 _._ 2
**Phi** Cand **27.3** 2 _._ 2 23.10 _._ 8 28.14 _._ 9
**Ours** 25.23 _._ 0 **23.6** 0 _._ 4 **29.7** 1 _._ 1


Table 2: F1 score comparison of using a single refined
input: implications (Imp) or candidate explanations
(Cand) vs. using both.


COT causes a substantial performance drop. We
observe that COT’s reasoning often leads the model
to produce more generic explanations and lose focus on explaining the humor.


The self-refine baselines perform similarly to
ZS, with SR slightly outperforming SR-NOC. This
suggests that merely refining the output without
adding new information might not be beneficial
for these tasks. Furthermore, incorrect feedback
from SR could even negatively impact the performance. In contrast, BOTTLEHUMOR outperforms
both self-refinement baselines, improving an average of 2.8, 2.0, and 3.3 _F_ 1 points on the MemeCap,
NewYorker, and YesBut datasets, respectively; sup


porting our hypothesis that humor understanding
requires additional world knowledge, which BOT
TLEHUMOR can successfully integrate into the reasoning process.


**5.2** **Contribution of Individual Components**


Since our method introduces several modifications
to the standard prompting approach, we assess the
contribution of each individual component to the
final performance. We conduct ablation tests and
employ an explainability technique to point to the
features that the model relies on most.


**Ablation** **study.** Table 2 presents an ablation
study where only a single input is provided after
refining implications and candidate explanations.
GPT-4o and Phi perform better with both inputs,
suggesting they effectively integrate relevant information from both to generate improved explanations. In contrast, Flash-1.5 and Qwen2 models
rely more on the candidate explanations, which
contain more readily-useful information than the
implications, indicating these models are less proficient at ignoring noisy or irrelevant implications.


**Feature importance.** To further pinpoint the contribution of individual implications to the final
explanations, we turn to interpretability methods.
We adapt TokenSHAP (Horovicz and Goldshmidt,

2024), which estimates the importance of individual tokens to the model’s prediction using Monte


Carlo Shapley value estimation, to a sentence-level
variation that we refer to as SentenceSHAP (see
Appendix B for details). This approach visualizes
each sentence’s contribution to the final explanation, as shown in Figure 3. The explanation from
ZS misses the humor in the long CVS receipt that
the officer is holding as a badge of honor, while
BOTTLEHUMOR is directly informed by the top
implication.


**5.3** **Assessment of the IB Framework**


**IB** **component** **analysis.** We focus on GPT4o,
the best performing model across all datasets, and
analyze the contribution of each IB component in
our method through ablation tests. We evaluate four
implication selection approaches (iterative refinement; Sec. 3.3): (1) _Random_, where implications
are selected randomly; (2) _Cosine_, which selects
implications with the lowest cosine similarity to
the previous inputs; (3) _CE_, which selects implications that yield the lowest cross-entropy value
when we condition on them to generate the candidate explanations; and (4) _Cosine+CE_, our method
presented in Sec. 3.3 that combines cosine similarity and cross-entropy based on the IB principle.
We conduct the analysis on 100 random instances
from each dataset. Figure 4 shows that _Cosine+CE_
method outperforms the _Cosine_ and _CE_ baselines,
improving _F_ 1 score by 4.8 and 2.3 points, respectively, confirming the importance of balancing reducing redundancy with increasing the signal.


**Quality of intermediate explanations.** To analyze whether the candidate explanations improve
across iterations, we randomly sample 50 examples
from each dataset and their outputs generated by
GPT-4o and Flash1.5. Since each iteration generates three candidate explanations, we report the
highest _F_ 1 score among them, and the corresponding precision and recall values in Table 3. For
GPT-4o, _F_ 1 scores consistently improve across iterations, primarily driven by recall, which increases
by an average of 11.4 points at _h_ 2 compared to the
initial hop. Precision also improves significantly at
_h_ 1, averaging an 8.0 point gain across datasets, then
stabilizes. A similar trend is observed in Flash1.58B, a considerably smaller model, except for the
MemeCap, where _F_ 1 scores peak at _h_ 1 but decrease
by 2.5 points at _h_ 2. While precision remains similar at the final hop compared to _h_ 1, recall drops by
2.4 points, suggesting smaller models are more susceptible to noisy information as iterations progress.



Figure 4: Performance of GPT4o on different IB components.


**GPT4o** **Flash1.5**
**h0** **h1** **h2** **h0** **h1** **h2**


**MC** P 88.5 **92.7** **92.7** 81.0 92.2 **92.3**
R 35.6 47.0 **48.5** 21.0 **35.0** 32.6
_F_ 1 50.8 62.4 **63.6** 33.3 **50.7** 48.2


**NY** P 79.6 **86.5** 84.7 72.2 **83.5** **83.5**
R 50.6 57.9 **62.8** 22.9 33.4 **34.7**
_F_ 1 61.9 69.4 **72.1** 34.8 47.7 **49.0**


**YB** P 67.2 **82.3** 82.0 81.0 92.2 **92.3**
R 48.2 56.2 **57.6** 26.2 36.8 **38.1**
_F_ 1 56.2 66.8 **67.6** 39.6 52.6 **54.0**


Table 3: Precision, Recall, and _F_ 1 scores on intermediate explanations across hops. h stands for hop. In
our experiments, hop _h_ = 0 corresponds to _k_ = 0 (no
implications), _h_ = 1 allows up to _k_ = 3 implications,
and _h_ = 2 allows up to _k_ = 6 implications.


**Error analysis.** We manually analyzed 40 randomly sampled explanations across different models where implications negatively impacted performance. The two most common errors are: dilution
of focus (81.2%) and introducing irrelevant information (18.7%). Dilution of focus occurs when implications repeat the same concept multiple times
or include overly generalized statements that override more specific details. Irrelevant information,
such as common phrases unrelated to the humor
can also distort the explanation. See Appendix C
for examples analyzed using SentenceSHAP.


**6** **Conclusions**


We introduced BOTTLEHUMOR, an unsupervised
method inspired by the information bottleneck principle that addresses humor explanation tasks by
eliciting relevant knowledge from VLMs and iteratively refining the explanation. Our experiments
show that BOTTLEHUMOR outperforms a range of
baselines on three datasets, underscoring the importance of incorporating relevant world knowledge
in humor understanding. Our analysis offers insights into the impact of individual components in


our method, and justifies the use of the IB principle. We further propose an LLM-based evaluation
framework and an adaptation of an interpretability
technique. While we tested our contributions in
the context of humor interpretation, future work
can adapt them to any task that can benefit from
eliciting and reasoning on world knowledge.


**Limitations**


**Subjective nature of humor understanding.** Individuals may interpret humor differently based on
their personal background knowledge. While we
find that the reference in the data is likely the most
representative interpretation of the humor in the
image and caption, other interpretations can also
be valid, which are not captured in our scores.


**Evaluation** **of** **explanations.** Humor explanations are often nuanced and subtle. While breaking
down the explanation into atomic sentences helps
the model verify the accuracy and relevance of each
claim, it may overlook the nuanced meaning that
emerges when all the sentences are combined.


**Trade-off** **between** **interpretability** **and** **effi-**
**ciency.** Our method emphasizes interpretable,
step-by-step controllable reasoning for the humor
explanation tasks, but this comes with increased
resource cost. While the computational cost can be
managed by limiting the number of implications or
image descriptions, the increased cost remains an
inherent trade-off for incorporating interpretable
reasoning steps. In contrast, less interpretable
or controllable approaches may offer greater efficiency. Each call typically involves _≤_ 500 input
tokens and _≤_ 128 output tokens, with up to 20 calls
per sample. For 100 samples, this results in an estimated total cost of up to $4–5 USD using GPT-4o
and up to $1 USD using Gemini-Flash-1.5-8B.


**Ethics Statement**


**Data.** All datasets used in our work, MemeCap,
NewYorker, and YesBut, are publicly available.
The datasets include images, accompanying texts,
and humor interpretations collected from humans
and may contain offensive content to some people.


**Models.** The LLMs and VLMs we used for the
experiments are trained on a large-scale web corpora and some of them utilize human feedback.
Given their training sources, they could potentially
generate content (i.e., descriptions, implications,
and explanations) that exhibit societal biases.



**Data Collection.** We use CloudResearch to collect judgments about model-generated explanations
in order to validate our proposed automatic evaluation method. To ensure the quality of evaluation,
we required that workers were located in Englishspeaking countries (e.g. US, UK, Canada, Australia, and New Zealand), and had an acceptance
rate of at least 93% on 1,000 prior annotations. We
paid $0.20 for the evaluation task, which means
that annotators were compensated with an average
hourly wage of $13, which is comparable to the US
minimum wage. We did not use any personal information from annotators. We obtained ethics approval from our institution’s research ethics board
prior to running the study.


**Acknowledgements**


This work was funded, in part, by the Vector Institute for AI, Canada CIFAR AI Chairs program,
Accelerate Foundation Models Research Program
Award from Microsoft, an NSERC discovery grant,
and a research gift from AI2. We thank Jack Hessel, Benyamin Movassagh, Sahithya Ravi, Aditya
Chinchure, and Vasile Negrescu for insightful discussions and feedback.


**References**


Marah Abdin, Jyoti Aneja, Hany Awadalla, Ahmed
Awadallah, Ammar Ahmad Awan, Nguyen Bach,
Amit Bahree, Arash Bakhtiari, Jianmin Bao, Harkirat
Behl, Alon Benhaim, Misha Bilenko, Johan Bjorck,
Sébastien Bubeck, Martin Cai, Qin Cai, Vishrav
Chaudhary, Dong Chen, Dongdong Chen, Weizhu
Chen, Yen-Chun Chen, Yi-Ling Chen, Hao Cheng,
Parul Chopra, Xiyang Dai, Matthew Dixon, Ronen Eldan, Victor Fragoso, Jianfeng Gao, Mei Gao,
Min Gao, Amit Garg, Allie Del Giorno, Abhishek
Goswami, Suriya Gunasekar, Emman Haider, Junheng Hao, Russell J. Hewett, Wenxiang Hu, Jamie
Huynh, Dan Iter, Sam Ade Jacobs, Mojan Javaheripi,
Xin Jin, Nikos Karampatziakis, Piero Kauffmann,
Mahoud Khademi, Dongwoo Kim, Young Jin Kim,
Lev Kurilenko, James R. Lee, Yin Tat Lee, Yuanzhi
Li, Yunsheng Li, Chen Liang, Lars Liden, Xihui
Lin, Zeqi Lin, Ce Liu, Liyuan Liu, Mengchen Liu,
Weishung Liu, Xiaodong Liu, Chong Luo, Piyush
Madan, Ali Mahmoudzadeh, David Majercak, Matt
Mazzola, Caio César Teodoro Mendes, Arindam Mitra, Hardik Modi, Anh Nguyen, Brandon Norick,
Barun Patra, Daniel Perez-Becker, Thomas Portet,
Reid Pryzant, Heyang Qin, Marko Radmilac, Liliang
Ren, Gustavo de Rosa, Corby Rosset, Sambudha Roy,
Olatunji Ruwase, Olli Saarikivi, Amin Saied, Adil
Salim, Michael Santacroce, Shital Shah, Ning Shang,
Hiteshi Sharma, Yelong Shen, Swadheen Shukla, Xia
Song, Masahiro Tanaka, Andrea Tupini, Praneetha


Vaddamanu, Chunyu Wang, Guanhua Wang, Lijuan
Wang, Shuohang Wang, Xin Wang, Yu Wang, Rachel
Ward, Wen Wen, Philipp Witte, Haiping Wu, Xiaoxia
Wu, Michael Wyatt, Bin Xiao, Can Xu, Jiahang Xu,
Weijian Xu, Jilong Xue, Sonali Yadav, Fan Yang,
Jianwei Yang, Yifan Yang, Ziyi Yang, Donghan Yu,
Lu Yuan, Chenruidong Zhang, Cyril Zhang, Jianwen
Zhang, Li Lyna Zhang, Yi Zhang, Yue Zhang, Yunan
Zhang, and Xiren Zhou. 2024. [Phi-3 technical report:](https://arxiv.org/abs/2404.14219)
A highly capable [language](https://arxiv.org/abs/2404.14219) model locally on your
[phone.](https://arxiv.org/abs/2404.14219) _Preprint_, arXiv:2404.14219.


Afra Feyza Akyürek, Ekin Akyürek, Leshem Choshen,
Derry Wijaya, and Jacob Andreas. 2024. [Deductive](https://doi.org/10.18653/v1/2024.findings-acl.584)
[closure training of language models for coherence,](https://doi.org/10.18653/v1/2024.findings-acl.584)
[accuracy, and updatability.](https://doi.org/10.18653/v1/2024.findings-acl.584) In _Findings of the Asso-_
_ciation_ _for_ _Computational_ _Linguistics:_ _ACL_ _2024_,
pages 9802–9818, Bangkok, Thailand. Association
for Computational Linguistics.


Ido Ben-Shaul, Ravid Shwartz-Ziv, Tomer Galanti, Shai
Dekel, and Yann LeCun. 2023. Reverse engineering self-supervised learning. In _Proceedings of the_
_37th International Conference on Neural Information_
_Processing Systems_, NIPS ’23, Red Hook, NY, USA.
Curran Associates Inc.


Santiago Castro, Devamanyu Hazarika, Verónica PérezRosas, Roger Zimmermann, Rada Mihalcea, and Soujanya Poria. 2019. [Towards multimodal sarcasm de-](https://doi.org/10.18653/v1/P19-1455)
[tection (an _Obviously_ perfect paper).](https://doi.org/10.18653/v1/P19-1455) In _Proceed-_
_ings of the 57th Annual Meeting of the Association for_
_Computational_ _Linguistics_, pages 4619–4629, Florence, Italy. Association for Computational Linguistics.


Arjun Chandrasekaran, Ashwin K. Vijayakumar, Stanislaw Antol, Mohit Bansal, Dhruv Batra, C. Lawrence
Zitnick, and Devi Parikh. 2016. We are humor beings: Understanding and predicting visual humor. In
_Proceedings of the IEEE Conference on Computer_
_Vision and Pattern Recognition (CVPR)_ .


Yingying Fang, Shuang Wu, Sheng Zhang, Chaoyan
Huang, Tieyong Zeng, Xiaodan Xing, Simon Walsh,
and Guang Yang. 2024. [Dynamic multimodal infor-](https://doi.org/10.1109/WACV57701.2024.00752)
mation bottleneck for [multimodality](https://doi.org/10.1109/WACV57701.2024.00752) classification.
In _WACV_, pages 7681–7691.


Anisha Gunjal and Greg Durrett. 2024. [Molecular facts:](https://doi.org/10.18653/v1/2024.findings-emnlp.215)
[Desiderata for decontextualization in LLM fact veri-](https://doi.org/10.18653/v1/2024.findings-emnlp.215)
[fication.](https://doi.org/10.18653/v1/2024.findings-emnlp.215) In _Findings of the Association for Computa-_
_tional Linguistics:_ _EMNLP 2024_, pages 3751–3768,
Miami, Florida, USA. Association for Computational
Linguistics.


Md Kamrul Hasan, Wasifur Rahman, AmirAli
Bagher Zadeh, Jianyuan Zhong, Md Iftekhar Tanveer,
Louis-Philippe Morency, and Mohammed (Ehsan)
Hoque. 2019. [UR-FUNNY: A multimodal language](https://doi.org/10.18653/v1/D19-1211)
[dataset for understanding humor.](https://doi.org/10.18653/v1/D19-1211) In _Proceedings of_
_the 2019 Conference on Empirical Methods in Natu-_
_ral Language Processing and the 9th International_
_Joint Conference on Natural Language Processing_
_(EMNLP-IJCNLP)_, pages 2046–2056, Hong Kong,
China. Association for Computational Linguistics.



Ron M. Hecht, Elad Noor, and Naftali Tishby. 2009.

[Speaker recognition by gaussian information bottle-](https://doi.org/10.21437/Interspeech.2009-387)
[neck.](https://doi.org/10.21437/Interspeech.2009-387) In _Interspeech 2009_, pages 1567–1570.


Jack Hessel, Ana Marasovic, Jena D. Hwang, Lillian
Lee, Jeff Da, Rowan Zellers, Robert Mankoff, and
Yejin Choi. 2023. Do androids [laugh](https://doi.org/10.18653/v1/2023.acl-long.41) at electric
sheep? humor [“understanding”](https://doi.org/10.18653/v1/2023.acl-long.41) benchmarks from
[the new yorker caption contest.](https://doi.org/10.18653/v1/2023.acl-long.41) In _Proceedings of the_
_61st Annual Meeting of the Association for Compu-_
_tational Linguistics (Volume 1:_ _Long Papers)_, pages
688–714, Toronto, Canada. Association for Computational Linguistics.


Miriam Horovicz and Roni Goldshmidt. 2024. [To-](https://doi.org/10.18653/v1/2024.nlp4science-1.1)
[kenSHAP: Interpreting large language models with](https://doi.org/10.18653/v1/2024.nlp4science-1.1)
Monte Carlo [shapley](https://doi.org/10.18653/v1/2024.nlp4science-1.1) value estimation. In _Pro-_
_ceedings_ _of_ _the_ _1st_ _Workshop_ _on_ _NLP_ _for_ _Science_
_(NLP4Science)_, pages 1–8, Miami, FL, USA. Association for Computational Linguistics.


Alexander Hoyle, Rupak Sarkar, Pranav Goel, and
Philip Resnik. 2023. Natural [language](https://doi.org/10.18653/v1/2023.emnlp-main.815) decompositions of implicit [content](https://doi.org/10.18653/v1/2023.emnlp-main.815) enable better text repre[sentations.](https://doi.org/10.18653/v1/2023.emnlp-main.815) In _Proceedings of the 2023 Conference_
_on Empirical Methods in Natural Language Process-_
_ing_, pages 13188–13214, Singapore. Association for
Computational Linguistics.


Yushi Hu, Weijia Shi, Xingyu Fu, Dan Roth, Mari Ostendorf, Luke Zettlemoyer, Noah A. Smith, and Ranjay Krishna. 2024a. [Visual sketchpad:](https://openreview.net/forum?id=GNSMl1P5VR) Sketching as
a visual chain of thought for multimodal language
[models.](https://openreview.net/forum?id=GNSMl1P5VR) In _The Thirty-eighth Annual Conference on_
_Neural Information Processing Systems_ .


Zhe Hu, Tuo Liang, Jing Li, Yiren Lu, Yunlai Zhou, Yiran Qiao, Jing Ma, and Yu Yin. 2024b. [Cracking the](https://openreview.net/forum?id=bCMpdaQCNW)
code of juxtaposition: [Can AI models understand the](https://openreview.net/forum?id=bCMpdaQCNW)
[humorous contradictions.](https://openreview.net/forum?id=bCMpdaQCNW) In _The Thirty-eighth An-_
_nual Conference on Neural Information Processing_
_Systems_ .


Aaron Hurst, Adam Lerer, Adam P Goucher, Adam
Perelman, Aditya Ramesh, Aidan Clark, AJ Ostrow, Akila Welihinda, Alan Hayes, Alec Radford,
et al. 2024. Gpt-4o system card. _arXiv_ _preprint_
_arXiv:2410.21276_ .


EunJeong Hwang and Vered Shwartz. 2023. [MemeCap:](https://doi.org/10.18653/v1/2023.emnlp-main.89)
A dataset for captioning and interpreting memes.
In _Proceedings_ _of_ _the_ _2023_ _Conference_ _on_ _Empir-_
_ical Methods in Natural Language Processing_, pages
1433–1445, Singapore. Association for Computational Linguistics.


EunJeong Hwang, Vered Shwartz, Dan Gutfreund, and
Veronika Thost. 2024. [A graph per persona:](https://aclanthology.org/2024.findings-acl.115/) Reasoning about subjective [natural](https://aclanthology.org/2024.findings-acl.115/) language descriptions.
In _Findings_ _of_ _the_ _Association_ _for_ _Computational_
_Linguistics ACL 2024_, pages 1928–1942.


Lee Hyun, Kim Sung-Bin, Seungju Han, Youngjae Yu,
and Tae-Hyun Oh. 2024. Smile: [Multimodal dataset](https://doi.org/10.18653/v1/2024.findings-naacl.73)
for understanding [laughter](https://doi.org/10.18653/v1/2024.findings-naacl.73) in video with language
[models.](https://doi.org/10.18653/v1/2024.findings-naacl.73) In _NAACL-HLT_ _(Findings)_, pages 1149–
1167.


Jiaxin Ju, Ming Liu, Huan Yee Koh, Yuan Jin, Lan Du,
and Shirui Pan. 2021. [Leveraging information bot-](https://doi.org/10.18653/v1/2021.findings-emnlp.345)
tleneck for scientific [document](https://doi.org/10.18653/v1/2021.findings-emnlp.345) summarization. In
_Findings of the Association for Computational Lin-_
_guistics:_ _EMNLP_ _2021_, pages 4091–4098, Punta
Cana, Dominican Republic. Association for Computational Linguistics.


Thomas P. Kasulis. 1989. [Introduction.](http://www.jstor.org/stable/1399446) _Philosophy_
_East and West_, 39(3):239–241.


Kenji Kawaguchi, Zhun Deng, Xu Ji, and Jiaoyang
Huang. 2023. How does information bottleneck help
deep learning? In _International Conference on Ma-_
_chine Learning (ICML)_ .


Kuang-Huei Lee, Anurag Arnab, Sergio Guadarrama,
John Canny, and Ian Fischer. 2021. [Compressive](https://openreview.net/forum?id=ZYX1ff6H0Bs)
[visual representations.](https://openreview.net/forum?id=ZYX1ff6H0Bs) In _Advances in Neural Infor-_
_mation Processing Systems_ .


Haoran Li, Arash Einolghozati, Srinivasan Iyer, Bhargavi Paranjape, Yashar Mehdad, Sonal Gupta, and
Marjan Ghazvininejad. 2021. EASE: [Extractive-](https://doi.org/10.18653/v1/2021.newsum-1.10)
[abstractive summarization end-to-end using the infor-](https://doi.org/10.18653/v1/2021.newsum-1.10)
[mation bottleneck principle.](https://doi.org/10.18653/v1/2021.newsum-1.10) In _Proceedings of the_
_Third Workshop on New Frontiers in Summarization_,
pages 85–95, Online and in Dominican Republic.
Association for Computational Linguistics.


Xun Liang, Shichao Song, Zifan Zheng, Hanyu Wang,
Qingchen Yu, Xunkai Li, Rong-Hua Li, Feiyu Xiong,
and Zhiyu Li. 2024. Internal [consistency](https://doi.org/10.48550/arXiv.2407.14507) and self[feedback in large language models:](https://doi.org/10.48550/arXiv.2407.14507) A survey. _CoRR_,
abs/2407.14507.


Fangyu Liu, Guy Edward Toh Emerson, and Nigel Collier. 2023. Visual spatial reasoning. _Transactions of_
_the Association for Computational Linguistics_ .


Pan Lu, Swaroop Mishra, Tony Xia, Liang Qiu, KaiWei Chang, Song-Chun Zhu, Oyvind Tafjord, Peter
Clark, and Ashwin Kalyan. 2022. Learn to explain:
Multimodal reasoning via thought chains for science
question answering. In _The 36th Conference on Neu-_
_ral Information Processing Systems (NeurIPS)_ .


Aman Madaan, Niket Tandon, Prakhar Gupta, Skyler
Hallinan, Luyu Gao, Sarah Wiegreffe, Uri Alon,
Nouha Dziri, Shrimai Prabhumoye, Yiming Yang,
Shashank Gupta, Bodhisattwa Prasad Majumder,
Katherine Hermann, Sean Welleck, Amir Yazdanbakhsh, and Peter Clark. 2023. [Self-refine:](https://openreview.net/forum?id=S37hOerQLB) Itera[tive refinement with self-feedback.](https://openreview.net/forum?id=S37hOerQLB) In _Thirty-seventh_
_Conference on Neural Information Processing Sys-_
_tems_ .


Sijie Mai, Ying Zeng, and Haifeng Hu. 2023. [Mul-](https://doi.org/10.1109/tmm.2022.3171679)
[timodal information bottleneck:](https://doi.org/10.1109/tmm.2022.3171679) Learning minimal
[sufficient unimodal and multimodal representations.](https://doi.org/10.1109/tmm.2022.3171679)
_IEEE Transactions on Multimedia_, 25:4121–4134.


Ana Marasovic, Iz Beltagy, Doug Downey, and Matthew
Peters. 2022. [Few-shot self-rationalization with nat-](https://doi.org/10.18653/v1/2022.findings-naacl.31)
[ural language prompts.](https://doi.org/10.18653/v1/2022.findings-naacl.31) In _Findings of the Associa-_
_tion_ _for_ _Computational_ _Linguistics:_ _NAACL_ _2022_,



pages 410–424, Seattle, United States. Association
for Computational Linguistics.


Gretchen McCulloch. 2020. _Because internet:_ _Under-_
_standing the new rules of language_ . Penguin.


Chancharik Mitra, Brandon Huang, Trevor Darrell, and
Roei Herzig. 2024. Compositional chain of thought
prompting for large multimodal models. In _Proceed-_
_ings of the IEEE/CVF Conference on Computer Vi-_
_sion and Pattern Recognition (CVPR)_ .


Debjyoti Mondal, Suraj Modi, Subhadarshi Panda, Rituraj Singh, and Godawari Sudhakar Rao. 2024. [Kam-](https://arxiv.org/abs/2401.12863)
cot: Knowledge [augmented](https://arxiv.org/abs/2401.12863) multimodal chain-of[thoughts reasoning.](https://arxiv.org/abs/2401.12863) _Preprint_, arXiv:2401.12863.


Abhilash Nandy, Yash Agarwal, Ashish Patwa, Millon Madhur Das, Aman Bansal, Ankit Raj, Pawan
Goyal, and Niloy Ganguly. 2024. [***YesBut***:](https://doi.org/10.18653/v1/2024.emnlp-main.937) A
[high-quality annotated multimodal dataset for eval-](https://doi.org/10.18653/v1/2024.emnlp-main.937)
uating satire [comprehension](https://doi.org/10.18653/v1/2024.emnlp-main.937) capability of vision[language models.](https://doi.org/10.18653/v1/2024.emnlp-main.937) In _Proceedings of the 2024 Confer-_
_ence on Empirical Methods in Natural Language Pro-_
_cessing_, pages 16878–16895, Miami, Florida, USA.
Association for Computational Linguistics.


Badri N. Patro, Mayank Lunayach, Deepankar Srivastava, Sarvesh Sarvesh, Hunar Singh, and Vinay P.
Namboodiri. 2021. [Multimodal humor dataset:](https://doi.org/10.1109/WACV48630.2021.00062) Predicting laughter [tracks](https://doi.org/10.1109/WACV48630.2021.00062) for sitcoms. In _2021_ _IEEE_
_Winter Conference on Applications of Computer Vi-_
_sion (WACV)_, pages 576–585.


Arkadiy Saakyan, Shreyas Kulkarni, Tuhin Chakrabarty,
and Smaranda Muresan. 2024. [Understanding figura-](https://arxiv.org/abs/2405.01474)
[tive meaning through explainable visual entailment.](https://arxiv.org/abs/2405.01474)
_Preprint_, arXiv:2405.01474.


Farhan Samir, Chan Young Park, Anjalie Field, Vered
Shwartz, and Yulia Tsvetkov. 2024. [Locating](https://doi.org/10.18653/v1/2024.emnlp-main.384) in[formation gaps and narrative inconsistencies across](https://doi.org/10.18653/v1/2024.emnlp-main.384)
languages: [A case study of LGBT people portrayals](https://doi.org/10.18653/v1/2024.emnlp-main.384)
[on Wikipedia.](https://doi.org/10.18653/v1/2024.emnlp-main.384) In _Proceedings of the 2024 Confer-_
_ence_ _on_ _Empirical_ _Methods_ _in_ _Natural_ _Language_
_Processing_, pages 6747–6762, Miami, Florida, USA.
Association for Computational Linguistics.


Andrew Michael Saxe, Yamini Bansal, Joel Dapello,
Madhu Advani, Artemy Kolchinsky, Brendan Daniel
Tracey, and David Daniel Cox. 2018. [On the infor-](https://openreview.net/forum?id=ry_WPG-A-)
[mation bottleneck theory of deep learning.](https://openreview.net/forum?id=ry_WPG-A-) In _Inter-_
_national Conference on Learning Representations_ .


Dustin Schwenk, Apoorv Khandelwal, Christopher
Clark, Kenneth Marino, and Roozbeh Mottaghi. 2022.
_A-OKVQA:_ _A_ _[Benchmark](https://doi.org/10.1007/978-3-031-20074-8_9)_ _for_ _Visual_ _Question_ _An-_
_[swering Using World Knowledge](https://doi.org/10.1007/978-3-031-20074-8_9)_, pages 146–162.


Joshua Shaw. 2010. [Philosophy of humor.](https://doi.org/10.1111/j.1747-9991.2009.00281.x) _Philosophy_
_Compass_, 5(2):112–126.


Limor Shifman. 2013. _Memes in digital culture_ . MIT
press.


Vered Shwartz, Peter West, Ronan Le Bras, Chandra
Bhagavatula, and Yejin Choi. 2020. [Unsupervised](https://doi.org/10.18653/v1/2020.emnlp-main.373)
[commonsense question answering with self-talk.](https://doi.org/10.18653/v1/2020.emnlp-main.373) In
_Proceedings_ _of_ _the_ _2020_ _Conference_ _on_ _Empirical_
_Methods in Natural Language Processing (EMNLP)_,
pages 4615–4629, Online. Association for Computational Linguistics.


David Stauffer. 1999. Let the good times roll: Building
a fun culture. _Harvard Management Update_ .


Gemini Team, Rohan Anil, Sebastian Borgeaud, JeanBaptiste Alayrac, Jiahui Yu, Radu Soricut, Johan
Schalkwyk, Andrew M Dai, Anja Hauth, Katie
Millican, et al. 2023. Gemini: a family of
highly capable multimodal models. _arXiv preprint_
_arXiv:2312.11805_ .


Naftali Tishby, Fernando C. Pereira, and William Bialek.
1999. [The information bottleneck method.](https://arxiv.org/abs/physics/0004057) In _Proc._
_of the 37-th Annual Allerton Conference on Commu-_
_nication, Control and Computing_, pages 368–377.


Laurel Klinger Vartabedian, Robert A.; Vartabedian.
1993. _The Annual Meeting of the Speech Communi-_
_cation Association_ .


Melissa Wanzer, Ann Frymier, and Jeffrey Irwin. 2010.

[An explanation of the relationship between instructor](https://doi.org/10.1080/03634520903367238)
[humor and student learning:](https://doi.org/10.1080/03634520903367238) Instructional humor pro[cessing theory.](https://doi.org/10.1080/03634520903367238) _Communication Education - COM-_
_MUN EDUC_, 59:1–18.


Caleb Warren, Adam Barsky, and A Peter Mcgraw. 2020.

[What makes things funny?](https://api.semanticscholar.org/CorpusID:229343265) an integrative review of
[the antecedents of laughter and amusement.](https://api.semanticscholar.org/CorpusID:229343265) _Person-_
_ality and Social Psychology Review_, 25:41 – 65.


Caleb Warren and A. Peter Mcgraw. 2015. [Opinion:](https://doi.org/10.1073/pnas.1503836112)
What makes [things](https://doi.org/10.1073/pnas.1503836112) humorous. _Proceedings_ _of_ _the_
_National Academy of Sciences_, 112:7105–7106.


Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten
Bosma, brian ichter, Fei Xia, Ed Chi, Quoc V Le,
and Denny Zhou. 2022. [Chain-of-thought prompt-](https://proceedings.neurips.cc/paper_files/paper/2022/file/9d5609613524ecf4f15af0f7b31abca4-Paper-Conference.pdf)
ing elicits reasoning in large language models. In
_Advances in Neural Information Processing Systems_,
volume 35, pages 24824–24837. Curran Associates,
Inc.


Peter West, Ari Holtzman, Jan Buys, and Yejin Choi.
2019. BottleSum: [Unsupervised and self-supervised](https://doi.org/10.18653/v1/D19-1389)
[sentence summarization using the information bottle-](https://doi.org/10.18653/v1/D19-1389)
[neck principle.](https://doi.org/10.18653/v1/D19-1389) In _Proceedings of the 2019 Confer-_
_ence on Empirical Methods in Natural Language Pro-_
_cessing and the 9th International Joint Conference_
_on Natural Language Processing (EMNLP-IJCNLP)_,
pages 3752–3761, Hong Kong, China. Association
for Computational Linguistics.


Sarah Wiegreffe, Jack Hessel, Swabha Swayamdipta,
Mark Riedl, and Yejin Choi. 2022. [Reframing](https://doi.org/10.18653/v1/2022.naacl-main.47)
[human-AI collaboration for generating free-text ex-](https://doi.org/10.18653/v1/2022.naacl-main.47)
[planations.](https://doi.org/10.18653/v1/2022.naacl-main.47) In _Proceedings of the 2022 Conference_
_of_ _the_ _North_ _American_ _Chapter_ _of_ _the_ _Association_
_for_ _Computational_ _Linguistics:_ _Human_ _Language_



_Technologies_, pages 632–658, Seattle, United States.
Association for Computational Linguistics.


Tailin Wu, Hongyu Ren, Pan Li, and Jure Leskovec.
2020. [Graph information bottleneck.](https://proceedings.neurips.cc/paper_files/paper/2020/file/ebc2aa04e75e3caabda543a1317160c0-Paper.pdf) In _Advances in_
_Neural Information Processing Systems_, volume 33,
pages 20437–20448. Curran Associates, Inc.


An Yang, Baosong Yang, Binyuan Hui, Bo Zheng,
Bowen Yu, Chang Zhou, Chengpeng Li, Chengyuan
Li, Dayiheng Liu, Fei Huang, Guanting Dong, Haoran Wei, Huan Lin, Jialong Tang, Jialin Wang,
Jian Yang, Jianhong Tu, Jianwei Zhang, Jianxin
Ma, Jianxin Yang, Jin Xu, Jingren Zhou, Jinze Bai,
Jinzheng He, Junyang Lin, Kai Dang, Keming Lu, Keqin Chen, Kexin Yang, Mei Li, Mingfeng Xue, Na Ni,
Pei Zhang, Peng Wang, Ru Peng, Rui Men, Ruize
Gao, Runji Lin, Shijie Wang, Shuai Bai, Sinan Tan,
Tianhang Zhu, Tianhao Li, Tianyu Liu, Wenbin Ge,
Xiaodong Deng, Xiaohuan Zhou, Xingzhang Ren,
Xinyu Zhang, Xipin Wei, Xuancheng Ren, Xuejing
Liu, Yang Fan, Yang Yao, Yichang Zhang, Yu Wan,
Yunfei Chu, Yuqiong Liu, Zeyu Cui, Zhenru Zhang,
Zhifang Guo, and Zhihao Fan. 2024. [Qwen2 techni-](https://arxiv.org/abs/2407.10671)
[cal report.](https://arxiv.org/abs/2407.10671) _Preprint_, arXiv:2407.10671.


Jiayi Ye, Yanbo Wang, Yue Huang, Dongping Chen,
Qihui Zhang, Nuno Moniz, Tian Gao, Werner Geyer,
Chao Huang, Pin-Yu Chen, Nitesh V Chawla, and
Xiangliang Zhang. 2024. Justice or prejudice? quantifying biases in llm-as-a-judge. _arXiv_ _preprint_
_arXiv:2410.02736_ .


Zhuosheng Zhang, Aston Zhang, Mu Li, hai zhao,
George Karypis, and Alex Smola. 2024. [Multi-](https://openreview.net/forum?id=y1pPWFVfvR)
[modal chain-of-thought reasoning in language mod-](https://openreview.net/forum?id=y1pPWFVfvR)
[els.](https://openreview.net/forum?id=y1pPWFVfvR) _Transactions on Machine Learning Research_ .


**A** **Dataset Examples**


Figure 5 illustrates example data instances from
MemeCap, NewYorker, and YesBut.


**B** **SentenceSHAP**


In this section, we introduce SentenceSHAP, an
adaptation of TokenSHAP (Horovicz and Goldshmidt, 2024). While TokenSHAP calculates the importance of individual tokens, SentenceSHAP estimates the importance of individual sentences in the
input prompt. The importance score is calculated
using Monte Carlo Shapley Estimation, following
the same principles as TokenSHAP.
Given an input prompt _X_ = _{x_ 1 _, x_ 2 _, . . ., xn}_,
where _xi_ represents a sentence, we generate all
possible combinations of _X_ by excluding each sentence _xi_ (i.e., _X_ _−{xi}_ ). Let _Z_ represent the set
of all combinations where each _xi_ is removed. To
estimate Shapley values efficiently, we randomly


Figure 5: Dataset Examples on MemeCap, NewYorker, and YesBut.



sample from _Z_ with a specified sampling ratio, resulting in a subset _Zs_ = _{X_ 1 _, X_ 2 _, . . ., Xs}_, where
each _Xi_ = _X_ _−{xi}_ .


Next, we generate a base response _r_ 0 using a
VLM (or LLM) with the original prompt _X_, and a
set of responses _Rs_ = _{r_ 1 _, r_ 2 _, . . ., rs}_, each generated by a prompt from one of the sampled combinations in _Zs_ .


We then compute the cosine similarity between the base response _r_ 0 and each response in _Rs_ using Sentence Transformer
(BAAI/bge-large-en-v1.5). The average similarity between combinations with and without _xi_ is
computed, and the difference between these averages gives the Shapley value for sentence _xi_ . This
is expressed as:


_ϕ_ ( _xi_ ) =



**C** **Error Analysis Based on**
**SentenceSHAP**


Figure 6 presents two examples of negative impacts from implications: dilution of focus and the
introduction of irrelevant information.


**D** **Details on human anntations**


We present the annotation interface on
CloudResearch used for human evaluation
to validate our evaluation metric in Figure 7. Refer
to Sec. 6 for details on annotator selection criteria
and compensation.


**E** **Effect of** _α_ **on explanation quality.**


To understand the role of the hyperparameter _α_ in
Eq. (1), we conducted an ablation study evaluating
F1 scores from GPT-4o across all three datasets
(100 samples each), using a fixed random seed. As
shown in Table 4, performance varies with different
_α_ values. When _α_ = 0 _._ 0, the model prioritizes relevance alone; when _α_ = 1 _._ 0, it focuses exclusively
on compression. Across datasets, the best performance tends to occur near _α_ = 0 _._ 7, indicating that
a balanced trade-off between compression and relevance yields the most informative and accurate
intermediate explanations.



1

_s_



_s_


(cos( _r_ 0 _, rj_ _| xi_ ) _−_ cos( _r_ 0 _, rj_ _| ¬xi_ ))

_j_ =1



where _ϕ_ ( _xi_ ) represents the Shapley value for sentence _xi_, cos( _r_ 0 _, rj_ _|_ _xi_ ) is the cosine similarity
between the base response and the response that
includes sentence _xi_, cos( _r_ 0 _, rj_ _|_ _¬xi_ ) is the cosine similarity between the base response and the
response that excludes sentence _xi_, and _s_ is the
number of sampled combinations in _Zs_ .


|Col1|Reference: The image is ironical, as having breakfast in bed is a luxury.<br>However, eating while in bed leads to food crumbs, making the bed<br>dirty, along with the need to clean the bed afterwards.|
|---|---|
||**Base:**… On the left, we see an elegant woman confidently striding<br>through an airport, presumably embarking on her journey with her<br>luggage at her side. The right side reveals the disappointing reality of<br>her situation: she is sprawled face down on the floor, appearing<br>exhausted and defeated. The expectation set by the confident woman<br>is humorously subverted by the reality of airport delays, a common<br>travel mishap, resonating with anyone who has experienced similar<br>frustrations. The caption adds a layer of irony to the situation, as it<br>acknowledges that while the journey is underway, it has not gone as<br>planned, a sentiment familiar to anyone who has faced travel delays. …|
|**Implications:**|**Implications:**|
|The 'BUT' panel shows a man lying on the ground near his luggage, which<br>contrasts with the initial impression of a positive outcome. (1.8)|The 'BUT' panel shows a man lying on the ground near his luggage, which<br>contrasts with the initial impression of a positive outcome. (1.8)|
|The 'BUT' panel shows a man lying on the ground near his luggage, which<br>contrasts with the initial impression of a positive outcome. (1.8)|**Ours:**The humor in the image arises from the stark contrast between<br>the woman's confident appearance and the unfortunate reality of the<br>flight delay, coupled with the casual acknowledgment in the caption<br>"Yes, But" which suggests thatdespite the optimistic beginning, the<br>situation has taken a comically negative turn. This plays on the universal<br>experience of travel delays and the frustration they often cause, making<br>the situation both relatable and exaggeratedly humorous.|
|The contrast between the organized, cheerful woman and the chaotic,<br>defeated man underscores the often unpredictable and humorous<br>misfortunes that can occur during travel. (1.3)|The contrast between the organized, cheerful woman and the chaotic,<br>defeated man underscores the often unpredictable and humorous<br>misfortunes that can occur during travel. (1.3)|
|The image uses this scenario to point out the discrepancy between one's<br>expectations upon departure and the reality of potential delays, a universal<br>experience for travelers. (0.6)|The image uses this scenario to point out the discrepancy between one's<br>expectations upon departure and the reality of potential delays, a universal<br>experience for travelers. (0.6)|


**Error: Irrelevant information**







**Caption** : from London to the Bay


**Reference** :

  - Meme poster is trying to convey a joke about how old MC
Hammer fans are now.

  - Meme poster makes a pun about Hammer time about a
grandma.


**Base** : The meme poster is humorously depicting an elderly
woman as a cool, hip figure akin to a rap icon.


**Ours** : The meme poster is humorously reimagining Vanilla
Ice's "Ice Ice Baby" with a grandmotherly twist.





Figure 6: Examples of negative impact from implications from Phi (top) and GPT4o (bottom).



**Dataset** **0** _**.**_ **0** **0** _**.**_ **3** **0** _**.**_ **7** **1** _**.**_ **0**


MEMECAP 46.7 51.5 51.5 48.2
NEWYORKER 57.5 57.6 57.7 57.1
YESBUT 58.1 56.2 59.0 55.0


Table 4: Ablation study for the hyperparameter _α_ used
in Eq. (1).


**F** **Generation Prompts for Selection and**
**Refinement**


Figures 8, 9, and 10 show the prompts used for generating image descriptions, seed implications (1st
hop), and non-seed implications (2nd hop onward).
Figure 11 displays the prompt used to generate candidate and final explanations. Image descriptions



are used for candidate explanations when existing
data is insufficient but are not used for final explanations. For calculating Cross Entropy values (used
as a relevance term), we use the prompt in Figure
11, substituting the image with image descriptions,
as LLM is used to calculate the cross entropies.


**G** **Evaluation Prompts**


Figures 12 and 13 present the prompts used to calculate recall and precision scores in our LLM-based
evaluation, respectively.


**H** **Prompts for Baselines**


Figure 14 presents the prompt used for the ZS, CoT,
and SR Generator methods. While the format remains largely the same, we adjust it based on the


baseline being tested (e.g., CoT requires generating
intermediate reasoning, so we add extra instructions for that). Figure 15 shows the prompt used
in the SR critic model. The critic’s criteria include:
(1) _correctness_, measuring whether the explanation
directly addresses why the caption is humorous in
relation to the image and its caption; (2) _sound-_
_ness_, evaluating whether the explanation provides
a well-reasoned interpretation of the humor; (3)
_completeness_, ensuring all important aspects in the
caption and image contributing to the humor are
considered; (4) _faithfulness_, verifying that the explanation is factually consistency with the image
and caption; and (5) _clarity_, ensuring the explanation is clear, concise, and free from unnecessary
ambiguity.


Prompt for Image Descriptions


Describe the image by focusing on the noun phrases that highlight the actions, expressions, and interactions of the main
visible objects, facial expressions, and people.


Here are some guidelines when generating image descriptions:

- Provide specific and detailed references to the objects, their actions, and expressions. Avoid using pronouns in the
description.

- Do not include trivial details such as artist signatures, autographs, copyright marks, or any unrelated background
information.

- Focus only on elements that directly contribute to the meaning, context, or main action of the scene.

- If you are unsure about any object, action, or expression, do not make guesses or generate made-up elements.

- Write each sentence on a new line.

- Limit the description to a maximum of 5 sentences, with each focusing on a distinct and relevant aspect that directly
contribute to the meaning, context, or main action of the scene.


Here are some examples of desired output: 
[Description] (example of newyorker cartoon image):
Through a window, two women with surprised expressions gaze at a snowman with human arms.


[Description] (example of newyorker cartoon image):
A man and a woman are in a room with a regular looking bookshelf and regular sized books on the wall.
In the middle of the room the man is pointing to text written on a giant open book which covers the entire floor.
He is talking while the woman with worried expression watches from the doorway.


[Description] (example of meme):
The left side shows a woman angrily pointing with a distressed expression, yelling “You said memes would work!”.
The right side shows a white cat sitting at a table with a plate of food in front of it, looking indifferent or smug with the
text above the cat reads, “I said good memes would work”.


[Description] (example of yesbut image):
The left side shows a hand holding a blue plane ticket marked with a price of “$50”, featuring an airplane icon and a
barcode, indicating it’s a flight ticket.
The right side shows a hand holding a smartphone displaying a taxi app, showing a route map labeled “Airport” and a
price of “$65”.



Proceed to generate the description.

[Description]:


Figure 8: A prompt used to generate image descriptions.


Prompt for Seed Implications


You are provided with the following inputs:

- [Image]: An image (e.g. meme, new yorker cartoon, yes-but image)

- [Caption]: A caption written by a human.

- [Descriptions]: Literal descriptions that detail the image.


### Your Task:

[ One-sentence description of the ultimate goal of your task. Customize based on the task. ]
Infer implicit meanings, cultural references, commonsense knowledge, social norms, or contrasts that connect the
caption to the described objects, concepts, situations, or facial expressions.


### Guidelines:

- If you are unsure about any details in the caption, description, or implication, refer to the original image for
clarification.

- Identify connections between the objects, actions, or concepts described in the inputs.

- Explore possible interpretations, contrasts, or relationships that arise naturally from the scene, while staying grounded
in the provided details.

- Avoid repeating or rephrasing existing implications. Ensure each new implication introduces fresh insights or
perspectives.

- Each implication should be concise (one sentence) and avoid being overly generic or vague.

- Be specific in making connections, ensuring they align with the details provided in the caption and descriptions.

- Generate up to 3 meaningful implications.


### Example Outputs:
#### Example 1 (example of newyorker cartoon image):

[Caption]: “This is the most advanced case of Surrealism I’ve seen.”

[Descriptions]: A body in three parts is on an exam table in a doctor’s office with the body’s arms crossed as though
annoyed.

[Connections]:
1. The dismembered body is illogical and impossible, much like Surrealist art, which often explores the absurd.
2. The body’s angry posture adds a human emotion to an otherwise bizarre scenario, highlighting the strange contrast.


#### Example 2 (example of newyorker cartoon image):

[Caption]: “He has a summer job as a scarecrow.”

[Descriptions]: A snowman with human arms stands in a field.

[Connections]:
1. The snowman, an emblem of winter, represents something out of place in a summer setting, much like a scarecrow’s
seasonal function.
2. The human arms on the snowman suggest that the role of a scarecrow is being played by something unexpected and
seasonal.


#### Example 3 (example of yesbut image):

[Caption]: “The left side shows a hand holding a blue plane ticket marked with a price of ‘$50’.”

[Descriptions]: The screen on the right side shows a route map labeled “Airport” and a price of ‘$65’.

[Connections]:
1. The discrepancy between the ticket price and the taxi fare highlights the often-overlooked costs of travel beyond just
booking a flight.
2. The image shows the hidden costs of air travel, with the extra fare representing the added complexity of budgeting for
transportation.


#### Example 4 (example of meme):

[Caption]: “You said memes would work!”

[Descriptions]: A cat smirks with the text “I said good memes would work.”

[Connections]:
1. The woman’s frustration reflects a common tendency to blame concepts (memes) instead of the quality of execution,
as implied by the cat’s response.
2. The contrast between the angry human and the smug cat highlights how people often misinterpret success as simple,
rather than a matter of quality.


### Now, proceed to generate output:

[Caption]: [ Caption ]


[Descriptions]:

[ Descriptions ]


[Connections]:


Figure 9: A prompt used to generate seed implications.


Prompt for Non-Seed Implications (2nd hop onward)


You are provided with the following inputs:

- [Image]: An image (e.g. meme, new yorker cartoon, yes-but image)

- [Caption]: A caption written by a human.

- [Descriptions]: Literal descriptions that detail the image.

- [Implication]: A previously generated implication that suggests a possible connection between the objects or concepts
in the caption and description.


### Your Task:

[ One-sentence description of the ultimate goal of your task. Customize based on the task. ]
Infer implicit meanings across the objects, concepts, situations, or facial expressions found in the caption, description,
and implication. Focus on identifying relevant commonsense knowledge, social norms, or underlying connections.


### Guidelines:

- If you are unsure about any details in the caption, description, or implication, refer to the original image for
clarification.

- Identify potential connections between the objects, actions, or concepts described in the inputs.

- Explore interpretations, contrasts, or relationships that naturally arise from the scene while remaining grounded in the
inputs.

- Avoid repeating or rephrasing existing implications. Ensure each new implication provides fresh insights or
perspectives.

- Each implication should be concise (one sentence) and avoid overly generic or vague statements.

- Be specific in the connections you make, ensuring they align closely with the details provided.

- Generate up to 3 meaningful implications that expand on the implicit meaning of the scene.


### Example Outputs:
#### Example 1 (example of newyorker cartoon image):

[Caption]: "This is the most advanced case of Surrealism I’ve seen."

[Descriptions]: A body in three parts is on an exam table in a doctor’s office with the body’s arms crossed as though
annoyed.

[Implication]: Surrealism is an art style that emphasizes strange, impossible, or unsettling scenes.

[Connections]:
1. A body in three parts creates an unsettling juxtaposition with the clinical setting, which aligns with Surrealist themes.
2. The body’s crossed arms add humor by assigning human emotion to an impossible scenario, reflecting Surrealist
absurdity.
...

[ We used sample examples from the prompt for generating seed implications (see Figure 9),
following the above format, which includes [Implication]:. ]



### Proceed to Generate Output:

[Caption]: [ Caption ]


[Descriptions]:

[ Descriptions ]


[Implication]:

[ Implication ]


[Connections]:


Figure 10: A prompt used to generate non-seed implications.


Prompt for Candidate and Final Explanations


You are provided with the following inputs:

- **[Image]:** A New Yorker cartoon image.

- **[Caption]:** A caption written by a human to accompany the image.

- **[Image Descriptions]:** Literal descriptions of the visual elements in the image.

- **[Implications]:** Possible connections or relationships between objects, concepts, or the caption and the image.

- **[Candidate Answers]:** Example answers generated in a previous step to provide guidance and context.


### Your Task:
Generate **one concise, specific explanation** that clearly captures why the caption is funny in the context of the
image. Your explanation must provide detailed justification and address how the humor arises from the interplay of the
caption, image, and associated norms or expectations.


### Guidelines for Generating Your Explanation:
1. **Clarity and Specificity:**

- Avoid generic or ambiguous phrases.

- Provide specific details that connect the roles, contexts, or expectations associated with the elements in the image and
its caption.


2. **Explain the Humor:**

- Clearly connect the humor to the caption, image, and any cultural, social, or situational norms being subverted or
referenced.

- Highlight why the combination of these elements creates an unexpected or amusing contrast.


3. **Prioritize Clarity Over Brevity:**

- Justify the humor by explaining all important components clearly and in detail.

- Aim to keep your response concise and under 150 words while ensuring no critical details are omitted.


4. **Use Additional Inputs Effectively:**

- **[Image Descriptions]:** Provide a foundation for understanding the visual elements."

- **[Implications]:** Assist in understanding relationships and connections but do not allow them to dominate or
significantly alter the central idea.

- **[Candidate Answers]:** Adapt your reasoning by leveraging strengths or improving upon weaknesses in the
candidate answers.


Now, proceed to generate your response based on the provided inputs.


### Inputs:

[Caption]: [ Caption ]


[Descriptions]:

[ Top-K Implications ]


[Implications]:

[ Top-K Implications ]


[Candidate Anwers]:

[ Top-K Candidate Explanations ]


[Output]:


Figure 11: A prompt used to generate candidate and final explanations.


Prompt for Evaluating Recall Score


Your task is to assess whether [Sentence1] is conveyed in [Sentence2]. [Sentence2] may consist of multiple sentences.


Here are the evaluation guidelines:
1. Mark ’Yes’ if [Sentence1] is conveyed in [Sentence2].
2. Mark ’No’ if [Sentence2] does not convey the information in [Sentence1].


Proceed to evaluate.


[Sentence1]: [ One Atomic Sentence from Decomposed Reference Explanation ]


[Sentence2]: [ Predicted Explanation ]


[Output]:


Figure 12: Prompt for evaluating recall score.


Prompt for Evaluating Precision Score


Your task is to assess whether [Sentence1] is inferable from [Sentence2]. [Sentence2] may consist of multiple sentences.


Here are the evaluation guidelines:
1. Mark "Yes" if [Sentence1] can be inferred from [Sentence2] - whether explicitly stated, implicitly conveyed,
reworded, or serving as supporting information.
2. Mark ’No’ if [Sentence1] is absent from [Sentence2], cannot be inferred, or contradicts it.


Proceed to evaluate.


[Sentence1]: [ One Atomic Sentence from Decomposed Predicted Explanation ]


[Sentence2]: [ Reference Explanation ]


[Output]:


Figure 13: Prompt for evaluating precision score.


Prompt for Baselines


You are provided with the following inputs:

  - **[Image]:** A New Yorker cartoon image.

  - **[Caption]:** A caption written by a human to accompany the image.

[ if Self-Refine with Critic is True: ]

  - **[Feedback for Candidate Answer]:** Feedback that points out some weakness in the current candidate responses.

[ if Self-Refine is True: ]

  - **[Candidate Answers]:** Example answers generated in a previous step to provide guidance and context.


### Your Task:
Generate **one concise, specific explanation** that clearly captures why the caption is funny in the context of the
image. Your explanation must provide detailed justification and address how the humor arises from the interplay of the
caption, image, and associated norms or expectations.


### Guidelines for Generating Your Explanation:
1. **Clarity and Specificity:**

  - Avoid generic or ambiguous phrases.

  - Provide specific details that connect the roles, contexts, or expectations associated with the elements in the image and
its caption.


2. **Explain the Humor:**

  - Clearly connect the humor to the caption, image, and any cultural, social, or situational norms being subverted or
referenced.

  - Highlight why the combination of these elements creates an unexpected or amusing contrast.


3. **Prioritize Clarity Over Brevity:**

  - Justify the humor by explaining all important components clearly and in detail.

  - Aim to keep your response concise and under 150 words while ensuring no critical details are omitted.


[ if Self-Refine is True: ]
4. **Use Additional Inputs Effectively:**

  - **[Candidate Answers]:** Adapt your reasoning by leveraging strengths or improving upon weaknesses in candidate
answers.

[ if Self-Refine with Critic is True: ]

  - **[Feedback for Candidate Answer]:** Feedback that points out some weaknesses in the current candidate responses.


[ if CoT is True: ]
Begin by analyzing the image and the given context, and explain your reasoning briefly before generating your final
response.


Here is an example format of the output:
{{
"Reasoning": "...",
"Explanation": "..."
}}


Now, proceed to generate your response based on the provided inputs.


### Inputs:

[Caption]: [ Caption ]


[Candidate Answers]: [ Candidate Explanations ]


[[Feedback for Candidate Answer]:]: [ Feedback for Candidate Explanations ]


[Output]:


Figure 14: A prompt used for baseline methods, with conditions added based on the specific baseline being
experimented with.


Prompt for Self-Refine Critic


[ Customize goal text here: ]
MemeCap: You will be given a meme along with its caption, and a candidate response that describes what meme poster
is trying to convey.
NewYorker: You will be given an image along with its caption, and a candidate response that explains why the caption
is funny for the given image.
YesBut: You will be given an image and a candidate response that describes why the image is funny or satirical.


Your task is to criticize the candidate response based on the following evaluation criteria:

- Correctness: Does the explanation directly address why the caption is funny, considering both the image and its
caption?

- Soundness: Does the explanation provide a meaningful and well-reasoned interpretation of the humor?

- Completeness: Does the explanation address all relevant aspects of the caption and image (e.g., visual details, text) that
contribute to the humor?

- Faithfulness: Is the explanation factually consistent with the details in the image and caption?

- Clarity: Is the explanation clear, concise, and free from unnecessary ambiguity?


Proceed to criticize the candidate response ideally using less than 5 sentences:


[Caption]: [ caption ]


[Candidate Response]:

[ Candidate Response ]


[Output]:


Figure 15: A prompt used in SR critic model.


