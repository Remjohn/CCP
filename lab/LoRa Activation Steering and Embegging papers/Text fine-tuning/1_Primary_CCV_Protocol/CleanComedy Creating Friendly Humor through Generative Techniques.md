## **CleanComedy: Creating Friendly Humor through Generative Techniques**

**Dmitry Vikhorev** **[1]** **, Daria Galimzianova** **[1,2]** **, Svetlana Gorovaia** **[1]** **,**
**Elizaveta Zhemchuzhina** **[1]**, **Ivan P. Yamshchikov** **[3]**

1LEYA Lab, HSE University, 2MTS AI, 3CAIRO, THWS



**Abstract**


Humor generation is a challenging task in
natural language processing due to limited
resources and the quality of existing datasets.
Available humor language resources often suffer
from toxicity and duplication, limiting their
effectiveness for training robust models. This
paper proposes CleanComedy, a specialized,
partially annotated toxicity-filtered corpus of
English and Russian jokes collected from
various sources. We study the effectiveness of
our data filtering approach through a survey on
humor and toxicity levels in various joke groups.
In addition, we study advances in computer
humor generation by comparing jokes written
by humans with various groups of generative
jokes, including our baseline models trained on
the CleanComedy datasets.


**1** **Introduction**


Computational humor is a significant area of
research within natural language processing. The
humor analysis is complex due to its reliance on
contextual dependencies. Despite this challenge,
computational humor offers possibilities for
improving human-computer interaction.
Previous works in this field (Chen and Soo,
2018; Yang et al., 2015; Mihalcea and Strapparava,
2005) have laid the baseline in humor recognition.
Recent research has focused on developing humor
generation solutions based on LLMs (Jentzsch and
Kersting, 2023; Amin and Burghardt, 2020).
In this study, we collect, filter and prepare humor
datasets in English and Russian languages. In order
to further enhance the utility of the datasets, we
collect human humor scores for 1,000 Russian
and 1,000 English jokes. We publish individual
annotations for every joke without aggregating
scores provided by multiple annotators.
The datasets are publicly available on GitHub [1],
facilitating access for the research community.


[1https://github.com/gorovuha/CleanComedy](https://github.com/gorovuha/CleanComedy)



Following, we fine-tune and align an LLM on
the prepared data, generate new humor samples
and ask human annotators to evaluate them. The
model undergoes two training stages: **Supervised**
**Fine-Tuning** and **Alignment** to learn the humor
style and subsequently pick up what “funniness”
is. We use the scores obtained from the human
annotators during the alignment stage.
The human judgments are then obtained for
results of the two-stage fine-tuning presented in this
research. They show that this training technique
might give rise to lightweight humorous models
and encourage responsible and effective generative
AI. Although one could cherry pick some fun
and interesting jokes, generative humor generally
remains an open research problem.
This paper presents a detailed account of our
methodology for dataset collection, filtering, and
annotation, as well as provides the settings and
results of the experiments with LLM fine-tuned on
our dataset in comparison with existing models.


**2** **Related work**


Computational humor research has seen significant
advancements in recent years. One of the primary
challenges in this field is capturing the details and
contextual dependencies that make humor effective
and enjoyable.
Works in computational humor (Mihalcea and
Strapparava, 2005; Yang et al., 2015; Chen and Soo,
2018), lay the groundwork by exploring the field
of humor recognition. They introduce linguistic
features, which are essential in distinguishing
humorous content from non-humorous text.
Humor often involves a delicate balance of
positive and negative emotions, the work (Meaney
et al., 2021) explores the dual nature of humor and
offense, highlighting the importance of sentiment
analysis in humor research.



1


**2.1** **Data**


The evolution of computational humor research
has produced a variety of popular datasets, which
serve as the foundational data sources for training
humor recognition and generation models. Table
1 provides an overview of the most commonly
referenced datasets. **16k One-Liners** (Mihalcea and
Strapparava, 2005; Weller and Seppi, 2019; Chen
and Soo, 2018) consists of 16,000 English oneliner jokes sourced from various online collections
and 16,000 non-humorous sentences from news
titles, proverbs, British National Corpus, and Open
Mind Common Sense collection. **Pun of the Day**
(Yang et al., 2015) is a collection of puns gathered
from the popular website "Pun of the Day."Each
entry is user-submitted and typically reviewed by
website moderators before inclusion. **Short Jokes**
2 consists of 231,657 brief jokes extracted from
various joke websites and social media platforms.
**SemEval 2021 Task 7: HaHackathon, Detecting**
**and Rating Humor and Offense** (Meaney et al.,
2021) contains 4,932 jokes, mostly from _twitter_ .
**Knowledge** **Amalgam:** **Generating** **Jokes** **and**
**Quotes** **Together** (Chippada and Saha, 2018)
introduces 96,910 jokes, which was sourced from
CrowdTruth and Subreddits, and then deduplicated.
It also includes quotes and tweets from different
sources. **The** **Naughtyformer:** **A** **Transformer**
**Understands Offensive Humor** (Tang et al., 2022)
introduces 92,153 jokes divided into three different
categories: Clean Jokes, Dark Jokes, and Dirty
Jokes. It also includes news texts as negative
samples. **Humor Detection: A Transformer Gets**
**the Last Laugh** (Weller and Seppi, 2019) contains
14,946 jokes scrapped from Reddit. It also includes
the _Short Jokes_ and _Pun of the Day_ datasets listed
above.
For the Russian language, there are fewer public
datasets with jokes (V. et al., 2017). The most
suitable is **FUN** **dataset** (Blinov et al., 2019),
collected from Russian social media and humor
resources. It contains different types of jokes, such
as one-liners, multi-turn jokes, and short sketches.
There is a manual binary annotation of about 2,000
instances.
These datasets are broadly used in solving
computational humor tasks yet they share two major
problems that hinder their usage for training of
generative humor models:

1. **Toxicity** : Many jokes in these datasets contain


[2https://github.com/amoudgl/short-jokes-dataset](https://github.com/amoudgl/short-jokes-dataset)



offensive content, including sexist, racist, or
otherwise discriminatory jokes. This does not
only raise ethical concerns but also impacts the
generalisation capacity of the humor models
trained on such data.
2. **Redundancy** : There is a high number of
duplicate jokes, both explicit when the same
exact words are used, and implicit when
the same joke is paraphrased multiple times.
Training models on duplicate data can lead to
overfitting.


**2.2** **LLMs**


There has been several recent attempts to explore
humor abilities of LLMs.
The study by the authors of (Jentzsch and
Kersting, 2023) explores the abilities of ChatGPT
3.5 in both creating and comprehending humor.
Their findings indicate that the model struggles
with the generation and interpretation of jokes. For
instance, ChatGPT 3.5 produces only a limited set
of unique jokes, which appear to be hard-coded.
The paper (Mirowski et al., 2024) studies the
LLM as creative writing assistants for comedians
and conclude that the models can be deployed
successfully in this quality with certain restrictions,
such as contextual alignment.

Sunkara et al. (2024) introduced an adaptive
humor generation model that personalizes content
based on user feedback, demonstrating improved
engagement through tailored humor.

Zhang et al. (2024) emphasized the importance
of multimodal context in humor generation,
integrating visual and textual data to capture
nuanced humor elements.

Li et al. (2024) proposed a novel approach using
contrastive learning with humor-contextualized
embeddings, resulting in more contextually
appropriate and diverse humorous text generation.

D’Silva (2024) explored augmenting LLMs with
humor theories to understand puns, highlighting
the challenges LLMs face in grasping linguistic
nuances and the potential of theoretical frameworks
to improve comprehension.

Wu et al. (2024) conducted a comparative
study on the role of cultural context in humor
generation, revealing significant differences in
humor perception between Western and Eastern
cultures and underscoring the necessity for
culturally aware humor models.



2


**3** **Dataset Curation**


In this section, we describe the methodology
employed in collecting and processing our dataset,
which includes humor content in both English and
Russian languages. The approach to dataset curation
is guided by the goal to create a resource that is not
only large and varied but also devoid of offensive
content and redundancies that could potentially bias
or undermine the performance of language models
trained on it.


**3.1** **Data Processing**


Firstly, we collect all the data mentioned in Section
2.1, see Table 1 for a quick overview. Then we
united it into one large collection and removed
exact duplicates, ignoring punctuation and case.
Every step of the further filtering process removes
bad samples. We do not paraphrase the jokes in
order to preserve the intricate semantics of humor.
The initial preprocessing of English data involves
the removal of examples that contain all symbols
except Latin characters and punctuation marks. It
helps get rid of bad examples comprising emojis,
links and also, for example, corrupted jokes from
Reddit containing _[deleted]_ or _[removed]_ words
(these words indicate that a part of the joke was
deleted before it was collected). We also noticed
that excessively short or long entries have a large
amount of noise (for example, repetitions, unfunny
utterances), so the next step was to keep examples
only between 50 and 150 characters, see Table 3
in Appendix.
For both English and Russian, we utilised
unbiased toxicity classifier Detoxify (Hanu and
Unitary team, 2020) for extracting toxic jokes
as this model is capable of detecting different
types of toxicity like threats, obscenity, insults, and
identity-based hate. As the authors of the classifier
mention, words associated with swearing, insults
or profanity are likely to be classified as toxic,
regardless of the tone or the intent. According to our
goal, which is to collect an ethical humor dataset,
we removed all the jokes that were supposed to
be toxic. Due to lower representation of Russian
in multilingual models, we employ ruBERTConv
Toxic Classifier [3], a transformer model tailored for
the Russian language (Kuratov and Arkhipov, 2019;
Dementieva et al., 2021), to improve the accuracy
of toxicity recognition .


[3https://huggingface.co/IlyaGusev/rubertconv_](https://huggingface.co/IlyaGusev/rubertconv_toxic_clf)
[toxic_clf](https://huggingface.co/IlyaGusev/rubertconv_toxic_clf)



To identify and remove duplicate jokes, we
utilize Sentence-BERT (SBERT) pretrained model
**all-mpnet-base-v2** (Reimers and Gurevych, 2019,
2020). This framework allows us to compute
text embeddings and then compare their cosine
similarity and find sentences with similar semantics
(Farouk, 2019). The goal is to remove jokes with
the same meaning expressed in different words or
jokes where some parts are presented in a different
order (see Table **??** in the Appendix). As we collect
English jokes from various sources, there is a large
number of duplicate instances. We consider two
entries as duplicates if the cosine between their
embeddings is higher than 0.7 for English and
higher than 0.9 for Russian.


After that, rigorous manual analysis of the
dataset shows that a large part of jokes
contains metaphorical insults. To make the
resulting data cleaner we label jokes with zeroshot classifier **DeBERTa-v3-large-mnli-fever-anli-**
**ling-wanli** (Laurer et al., 2024). The set of labels
this time is _politics,_ _neutral,_ _offending,_ _alcohol,_
_drugs,_ _racist_ . Thus, we removed all instances
labeled as political, racist, and insulting content
(see Table **??** in the Appendix) to avoid unethical
expressions.


A thorough analysis of the remaining jokes
reveals a significant number of texts on sensitive
topics. Therefore, we utilize topic modeling to
understand our large corpus better. Our objective
is to have topics that are specific enough (e.g.,
separating soft drinks from alcohol) but not
overly fragmented (e.g., having 100 classes about
animals would be uninteresting). **BERTopic**, a topic
modeling technique that leverages transformers
and c-TF-IDF (Grootendorst, 2022), is used to
create clusters with easily interpretable topics while
keeping important words in the topic descriptions.
The visual representation of these clusters can be
found in Appendix 4, 5.


Cluster modeling allows us to thoroughly analyze
the collected dataset in terms of diversity and
content distribution. We remove sensitive jokes
that belong to the clusters about _religion, funerals,_
_bathrooms, officers, pregnancy, nations, disabilities,_
_and divorce_ ensuring ethical and useful dataset.


The final remaining dataset, after the full set of
filters has been applied, contains 44k English jokes
and 40k Russian jokes. The comprehensive filtering
pipeline can be found in Figures 1 and 2.



3


Name Description Jokes Non-jokes


English


16k One-Liners Humorous samples from daily joke websites 16,000 16,000
Short Jokes Short jokes scraped from various joke 231,657 0
websites with lengths ranging from 10 to
200 characters



SemEval 2021 Task 7:
HaHackathon, Detecting and
Rating Humor and Offense

Knowledge Amalgam:
Generating Jokes and Quotes
Together

The Naughtyformer: A
Transformer Understands
Offensive Humor

Humor Detection: A
Transformer Gets the Last
Laugh



80% jokes from twitter and 20% jokes from 4,932 3,068
Short Jokes dataset



Multiple sources were combined and
deduplicated (the two sources for jokes are
CrowdTruth and Subreddits)



96,910 173,633



Scrapped from Reddit and includes different 92,153 10,710
types of humour


The original part is scraped from Reddit 14,946 0



Pun of the Day Puns from Pun of the Day website 2,423 2,423
CleanComedy English Ethical filtered jokes with 2-scale score 44,481 0
CleanComedy English Gold Ethical filtered jokes with human humor 1,000 0
5-scale score


Russian


Stierlitz One-liners from social media 46,608 46,608
FUN Russian jokes from social media and online 156,605 156,605
collections

CleanComedy Russian Ethical filtered jokes with 2-scale score 40,926 0
CleanComedy Russian Gold Ethical filtered jokes with human humour 1,000 0
5-scale score


Table 1: Comparison of Humor Datasets



**3.2** **Dataset Annotation**


Datasets for both languages include manual human
annotation of 1,000 samples for each language. We
call this subset of the data **CleanComedy** **Gold** .
Volunteers have been asked to rate a joke on a scale
from 1 to 5 depending on how funny they believe the
joke is. The instruction for the annotation included
the following points:

  - Rate how funny a joke is on a five-point scale,
where 1 is not funny and 5 is very funny.

  - Do you find the text of the joke vulnerable or
inappropriate?
Each joke has been rated by five different
annotators. The scores were collected through
**Telegram** bot by crowd sourcing. The annotators
volunteered their time, dedicating a maximum of
one hour. For each instance we calculated the



mean score for five annotators, which is used in
CleanComedy Gold datasets as human humor score,
see Figure 3. We also publish individual scores
to facilitate further research on personalization of
generative humor.
With the consent of the annotators we also
publish their anonymized data, such as age, gender
(female, male and other), education level (secondary
vocational, bachelor’s degree, specialist degree,
master’s degree, PhD) and the language fluency
level for both languages (from A1 to C2 + native).


**4** **Models**


In our experiments, we fine-tune a pre-trained
version of a multilingual large language model
[meta-llama/Llama-3.1-8B. We utilize the pre-train](https://huggingface.co/meta-llama/Llama-3.1-8B)
version of the model because we believe that in



4


Figure 1: Topic modelling for CleanComedy English.


Figure 2: Topic modelling for CleanComedy Russian.



this setting the influence of our dataset on the
final result increases, while using the instruction
[model meta-llama/Llama-3.1-8B-Instruct increases](https://huggingface.co/meta-llama/Llama-3.1-8B-Instruct)
the dependence on both the model itself and the
prompt selected for it.
Our prompt for fine-tuning models looks like
this:


<|begin_of_text|>
<|reserved_special_token_{i}|>
{text}


where <|begin_of_text|> is the start of text
token, <|reserved_special_token_{i}|> is the
language token (i=0 for English and i=1 for Russian
language), and {text} is a joke text.
For fine-tuning the model, we use LoRA (Hu
et al., 2021). Instead of updating all the weights in
every layer, we only train low-rank approximations
(with a rank of 4) for all layers except for the
classification and embedding layers, which we train
fully.
We fine-tune the model in two stages: **Supervised**
**Fine-Tuning** and **LLM** **Alignment** . At the first
[stage, we train meta-llama/Llama-3.1-8B to imitate](https://huggingface.co/meta-llama/Llama-3.1-8B)
the jokes of our large datasets. At the second stage,
we additionally train the model obtained at the
previous stage to generate funny examples from our
small annotated dataset and not generate unfunny
ones. At both stages, optimization is performed
using the Adam algorithm, coupled with a cosine
learning rate scheduler. The batch size per these
two stages is equal to 64.


**4.1** **Supervised Fine-Tuning**


At this stage, we train [meta-llama/Llama-3.1-8B](https://huggingface.co/meta-llama/Llama-3.1-8B)
using the datasets described in Data processing



subsection.
The model’s training employs the standard
language modeling loss function. A fine-tuning
phase takes 2 epochs using a maximum learning
rate of 1e-05.


**4.2** **LLM Alignment**


At this stage, we additionally train the model
obtained at the previous stage using the
CleanComedy Gold dataset. We calculate the level
of humor in a joke by averaging the annotators’
ratings in this one. Since these average ratings are
between 1 and 5, we apply a linear transformation
to map the scores to a 0-to-1 scale to get soft labels
for sequence classification task.
The model is trained using binary cross-entropy
as the loss function for binary classification tasks
inspired by **DPO** (Rafailov et al., 2024) and **SimPO**
(Meng et al., 2024). Our method differs from
these methods by using soft positive/negative labels
instead of requiring a dataset of chosen-rejected
answer pairs:


_t_ = ( _s −_ 1) _/_ 4 _,_


_loss_ = _−_ - ( _t_ log( _p_ ) + (1 _−_ _t_ ) log(1 _−_ _p_ )) _,_


( _t,p_ ) _∈B_


where _s_ [4] is an average humor score of a joke from
the annotated dataset and _p_ is probability of the
same joke according to the language model that is
trained.
A fine-tuning phase takes 5 epochs using a
maximum learning rate of 4e-07.


4The range of _s_ varies from 1 to 5, so _t_ falls between
0 and 1 and can be interpreted as the target probability for
classification task using soft labels.



5


Figure 3: Average scores for **CleanComedy Gold** datasets in English (in the left picture) and Russian (in the right
picture). The average score of 5 annotators was computed for each joke.



**5** **Results**


For both languages, we sample 100 examples from
each of the following six groups:


1. **LLaMA** **3.1** **8B** **(Supervised** **Fine-Tuned).**
See Supervised Fine-Tuning section for
training details.
2. **LLaMA 3.1 8B (Supervised Fine-Tuned +**
**Aligned).** See LLM Alignment section for
training details.
3. **LLaMA 3.1 8B (Instruct).** We use following
prompts for two languages.


**System prompt:**
_You are a comedian with a lot of experience._
_Your income level and future career depend_
_on_ _the_ _level_ _of_ _humor_ _in_ _jokes._ _Since_ _your_
_audience is educated, it’s best to avoid using_
_well-known jokes._


**User prompt:**
_Write a funny short joke for your performance._
_I_ _only_ _need_ _the_ _text of_ _this_ _joke_ _and_ _nothing_
_else._


4. **GPT-4o.** Since we don’t have access to the
GPT-4o API, we use the **default** **system**
**prompt** and generate all 100 jokes of the
class at one time, using the following prompt:



**User prompt:**
_Hi! Imagine that you are a comedian with a_
_lot of experience. Write 100 funny short jokes_
_for your performance. Your income level and_
_future career depend on them._


5. **Unfiltered** **Dataset.** In order to understand
how the levels of humor and toxicity in the
dataset are changed after toxicity filters, we
also take 100 samples from the dataset without
toxicity filters.
6. **Clean** **Dataset.** In order to understand how
large language models are able to learn
humor from humorous data, we also take 100
samples from the dataset as some reference
for comparing humor scores.
We employ ancestral sampling with a
temperature of 0.5 for all generated examples,
except for the **LLaMA** **3.1** **8B** **(Instruct)** model
for English, where we use a temperature of 0.9 to
mitigate its tendency towards generating absolutely
identical texts at lower temperatures. Additionally,
for the **LLaMA** **3.1** **8B** **(Instruct)** generations,
we remove semantic duplicates using the SBERT
model in the same manner as during the dataset
deduplication stage, applying the same cutoff
threshold for identifying duplicates [5] .
Each of the 600 sampled examples was evaluated
by 3 individuals, following a process similar to
that described in Dataset Annotation subsection.
In this case, in addition to rating each joke, the
evaluators were also asked to assess its level of


5We do this for two languages.



6


Model Humor score ↑ Toxicity percentage ↓


English


LLaMA 3.1 8B (Supervised Fine-Tuned) 2 _._ 11 _±_ 1 _._ 2 13 _._ 38
LLaMA 3.1 8B (Supervised Fine-Tuned + Aligned) 2 _._ 02 _±_ 1 _._ 08 15 _._ 38
LLaMA 3.1 8B (Instruct) 2 _._ 65 _±_ 1 _._ 23 **3.97**
GPT-4o **3.02** _±_ 1 _._ 3 9 _._ 27
Unfiltered Dataset 2 _._ 72 _±_ 1 _._ 42 26 _._ 09
Clean Dataset 2 _._ 96 _±_ 1 _._ 36 11 _._ 41


Russian


LLaMA 3.1 8B (Supervised Fine-Tuned) 1 _._ 68 _±_ 1 _._ 09 4 _._ 01
LLaMA 3.1 8B (Supervised Fine-Tuned + Aligned) 1 _._ 74 _±_ 1 _._ 06 **3.3**
LLaMA 3.1 8B (Instruct) 2 _._ 07 _±_ 1 _._ 27 4 _._ 26
GPT-4o 2 _._ 38 _±_ 1 _._ 23 4 _._ 67
Unfiltered Dataset 2 _._ 77 _±_ 1 _._ 4 20 _._ 93
Clean Dataset **2.84** _±_ 1 _._ 44 11 _._ 37


Table 2: Comparison of average metrics for different groups of jokes. Standard deviations are also calculated for
the humor scores. Each group includes 100 examples, with each example rated by at least 3 people. The toxicity
percentage ranges from 0 to 100, while the humor score ranges from 1 to 5.



toxicity or inappropriateness [6] . The average ratings
for each group can be found in Table 2. For both
English and Russian, the toxicity percentage in
our clean datasets is half that of the originally
collected data, demonstrating the effectiveness of
the aforementioned filtering process. The data on
the demographics of the annotators can be found in
Figures 7, 8, 9 and 10.
The evaluation of humor generation models
reveals interesting trends across different setups
for both English and Russian datasets.
For English, among the models, GPT-4o achieves
the highest humor score, closely followed by the
Clean Dataset of human-created jokes. The LLaMA
3.1 8B (Instruct) model also performs well, with a
humor score, but significantly lags behind GPT-4o.
Models fine-tuned on the CleanComedy dataset,
such as Supervised Fine-Tuned and Aligned, show
lower humor scores, reflecting the challenges in
adapting LLMs to humor tasks using limited or
filtered data. In terms of toxicity, the LLaMA
3.1 8B (Instruct) achieves the lowest percentage,
significantly outperforming both the unfiltered
dataset and the clean dataset.
Similar trends are observed in Russian, where
Clean Dataset achieves the highest humor score,
followed by GPT-4o. The LLaMA 3.1 8B (Instruct)
model scores slightly lower than its English


6We ask: "Do you find this text vulnerable or
inappropriate?"An annotator can answer "yes"or "no".



counterpart, suggesting room for improvement in
handling humor in Russian. Fine-tuned models for
Russian also show lower humor scores. The Aligned
model, however, demonstrates the lowest toxicity
percentage, indicating that filtering and alignment
processes are particularly effective in producing
clean content for Russian.
The age histograms in Figure 7 show the majority
of our annotators are aged 20-30, which skews the
humor perception toward this age group. It is also
important to point out that there was almost no
native speakers of English among our volunteers
(Figure 10), which has significantly influenced the
humor scores obtained for the English jokes. We
theorize that the English jokes generated by our
models were rated higher than Russian due to this
linguistic bias. The humor scores for the Russian
generative jokes are lower for the models trained
on the filtered data because they could have been
deemed more boring for the annotators, as the
humor scores are lower for the jokes with lower
toxicity percentage.


**6** **Conclusion**


In this research, we share the insights we gained
while experimenting with prompting and finetuning models for humor generation.
This paper presents CleanComedy, a novel and
ethically curated dataset for humor generation
and evaluation in English and Russian. Through



7


rigorous data filtering and annotation processes, we
address the common challenges in datasets, such
as toxicity and redundancy. By fine-tuning a LLM
with this dataset, we demonstrated its capability
to generate contextually appropriate and ethically
aligned humor.
The results provided by the annotators of
our experiments underscore the importance of
alignment techniques in improving the quality and
relevance of generated humor. While our models
perform well within the scope of the dataset,
challenges remain in generating humor that adapts
different languages and cultures.
This study contributes to the field by
introducing methodologies that prioritize ethical
considerations while advancing computational
humor research. However, humor’s subjective and
cultural nature requires ongoing attention to ensure
AI-generated content remains inclusive, engaging,
and responsible.


**Limitations**


The English dataset faces challenges related to the
quality and diversity of humor instances. While
significant efforts are made to remove offensive
and inappropriate content from the datasets, the
filtering processes may not be ideal. Enhanced
filtering techniques and ongoing monitoring are
essential to mitigate this risk. Moreover, future
research should focus on developing more advanced
generative techniques to enhance the coherence and
creativity of the outputs.
When training language models, we have only
experimented with PEFT methods. Judging by the
quality of the resulted generations, the models
would benefit greatly from full fine-tuning. Another
limitation of this study is the size of the dataset
which comprised only _∼_ 40k samples for each
language. It seems obvious that collecting a
bigger and higher quality humor dataset could
further advance humor generation. For example,
transcribing popular humor shows seems to be an
interesting idea for humor data collection.
Humor is inherently connected to cultural and
contextual details, which can be challenging for
language models to understand and generate. The
models we trained for English and Russian show
different types of jokes, thus, they might not
perform well across other cultural contexts and
languages, rising the need for culturally adaptive
humor generation techniques.



**Ethical Statement**


The ethical risks that the computational humor
research carries are discussed in this section ensure
responsible development of AI technologies.
Computational humor systems may mimic biases
present in training data. Despite multiple stage
filtering process and mitigation strategies to prevent
the spread of stereotypes and discriminatory
content, generated humorous texts still can
sometimes result in offensive or harmful content.
There is a risk that computational humor
systems could be misused for malicious purposes,
such as cyberbullying, harassment, or spreading
misinformation, thus, we claim that our systems are
not intended for ant malicious applications.
The rise of computational humor may impact on
human writing and entertainment. It is essential to
consider societal impacts and strive for a balance
that supports human creativity while leveraging
technological advancements.


**Acknowledgments**


We would like to express our gratitude to the
volunteer crowdworkers who dedicated their time
and effort to evaluate our generative models.


**References**


Miriam Amin and Manuel Burghardt. 2020. [A](https://aclanthology.org/2020.latechclfl-1.4)
survey on approaches [to](https://aclanthology.org/2020.latechclfl-1.4) computational humor
[generation.](https://aclanthology.org/2020.latechclfl-1.4) In _Proceedings of the 4th Joint SIGHUM_
_Workshop on Computational Linguistics for Cultural_
_Heritage, Social Sciences, Humanities and Literature_,
pages 29–41, Online. International Committee on
Computational Linguistics.


Vladislav Blinov, Valeria Bolotova-Baranova, and Pavel
Braslavski. 2019. [Large dataset and language model](https://doi.org/10.18653/v1/P19-1394)
fun-tuning for [humor](https://doi.org/10.18653/v1/P19-1394) recognition. In _Proceedings_
_of_ _the_ _57th_ _Annual_ _Meeting_ _of_ _the_ _Association_
_for_ _Computational_ _Linguistics_, pages 4027–4032,
Florence, Italy. Association for Computational
Linguistics.


Peng-Yu Chen and Von-Wun Soo. 2018. [Humor](https://doi.org/10.18653/v1/N18-2018)
[recognition using deep learning.](https://doi.org/10.18653/v1/N18-2018) In _Proceedings of_
_the 2018 Conference of the North American Chapter_
_of_ _the_ _Association_ _for_ _Computational_ _Linguistics:_
_Human_ _Language_ _Technologies,_ _Volume_ _2_ _(Short_
_Papers)_, pages 113–117, New Orleans, Louisiana.
Association for Computational Linguistics.


Bhargav Chippada and Shubajit Saha. 2018. [Knowledge](https://arxiv.org/abs/1806.04387)
amalgam: Generating [jokes](https://arxiv.org/abs/1806.04387) and quotes together.
_Preprint_, arXiv:1806.04387.



8


Daryna Dementieva, Daniil Moskovskiy, Varvara
Logacheva, David Dale, Olga Kozlova, Nikita
Semenov, and Alexander Panchenko. 2021. [Methods](https://arxiv.org/abs/2105.09052)
for detoxification of [texts](https://arxiv.org/abs/2105.09052) for the russian language.
_Preprint_, arXiv:2105.09052.


Rohan D’Silva. 2024. _Augmenting_ _[Large](https://hammer.purdue.edu/articles/thesis/Augmenting_Large_Language_Models_with_Humor_Theory_To_Understand_Puns/25674792)_ _Language_
_Models_ _with_ _Humor_ _[Theory](https://hammer.purdue.edu/articles/thesis/Augmenting_Large_Language_Models_with_Humor_Theory_To_Understand_Puns/25674792)_ _to_ _Understand_ _Puns_ .
Ph.D. thesis, Purdue University.


Mamdouh Farouk. 2019. Measuring sentences
[similarity: A survey.](https://doi.org/10.17485/ijst/2019/v12i25/143977) _Indian Journal of Science and_
_Technology_, 12(25):1–11.


Maarten Grootendorst. 2022. Bertopic: Neural topic
modeling with a class-based tf-idf procedure. _arXiv_
_preprint arXiv:2203.05794_ .


Laura Hanu and Unitary team. 2020. Detoxify. Github.
https://github.com/unitaryai/detoxify.


Edward J. Hu, Yelong Shen, Phillip Wallis, Zeyuan
Allen-Zhu, Yuanzhi Li, Shean Wang, Lu Wang, and
Weizhu Chen. 2021. [Lora: Low-rank adaptation of](https://arxiv.org/abs/2106.09685)
[large language models.](https://arxiv.org/abs/2106.09685) _Preprint_, arXiv:2106.09685.


Sophie Jentzsch and Kristian Kersting. 2023. [ChatGPT](https://doi.org/10.18653/v1/2023.wassa-1.29)
[is fun, but it is not funny! humor is still challenging](https://doi.org/10.18653/v1/2023.wassa-1.29)
large [language](https://doi.org/10.18653/v1/2023.wassa-1.29) models. In _Proceedings_ _of_ _the_
_13th_ _Workshop_ _on_ _Computational_ _Approaches_ _to_
_Subjectivity,_ _Sentiment,_ _&_ _Social_ _Media_ _Analysis_,
pages 325–340, Toronto, Canada. Association for
Computational Linguistics.


Yuri Kuratov and Mikhail Arkhipov. 2019. [Adaptation](https://arxiv.org/abs/1905.07213)
of deep bidirectional [multilingual](https://arxiv.org/abs/1905.07213) transformers for
[russian language.](https://arxiv.org/abs/1905.07213) _Preprint_, arXiv:1905.07213.


Moritz Laurer, Wouter Van Atteveldt, Andreu Casas,
and Kasper Welbers. 2024. Less annotating, more
classifying: Addressing the data scarcity issue of
supervised machine learning with deep transfer
learning and bert-nli. _Political Analysis_, 32(1):84–
100.


Wei Li et al. 2024. [A novel approach to humorous text](https://arxiv.org/abs/2410.10370)
[generation: Using contrastive learning with humor-](https://arxiv.org/abs/2410.10370)
[contextualized embeddings.](https://arxiv.org/abs/2410.10370) _ArXiv_ .


J. A. Meaney, Steven Wilson, Luis Chiruzzo, Adam
Lopez, and Walid Magdy. 2021. [SemEval 2021 task 7:](https://doi.org/10.18653/v1/2021.semeval-1.9)
[HaHackathon, detecting and rating humor and offense.](https://doi.org/10.18653/v1/2021.semeval-1.9)
In _Proceedings of the 15th International Workshop on_
_Semantic Evaluation (SemEval-2021)_, pages 105–119,
Online. Association for Computational Linguistics.


Yu Meng, Mengzhou Xia, and Danqi Chen. 2024. [Simpo:](https://arxiv.org/abs/2405.14734)
[Simple preference optimization with a reference-free](https://arxiv.org/abs/2405.14734)
[reward.](https://arxiv.org/abs/2405.14734) _Preprint_, arXiv:2405.14734.


Rada Mihalcea and Carlo Strapparava. 2005. [Making](https://aclanthology.org/H05-1067)
[computers laugh: Investigations in automatic humor](https://aclanthology.org/H05-1067)
[recognition.](https://aclanthology.org/H05-1067) In _Proceedings_ _of_ _Human_ _Language_
_Technology Conference and Conference on Empirical_
_Methods_ _in_ _Natural_ _Language_ _Processing_, pages
531–538, Vancouver, British Columbia, Canada.
Association for Computational Linguistics.



Piotr Mirowski, Juliette Love, Kory Mathewson, and
Shakir Mohamed. 2024. A robot walks into a bar:
Can language models serve as creativity supporttools
for comedy? an evaluation of llms’ humour alignment
with comedians. In _The 2024 ACM Conference on_
_Fairness,_ _Accountability,_ _and_ _Transparency_, pages
1622–1636.


Rafael Rafailov, Archit Sharma, Eric Mitchell, Stefano
Ermon, Christopher D. Manning, and Chelsea
Finn. 2024. Direct preference [optimization:](https://arxiv.org/abs/2305.18290) Your
[language model is secretly a reward model.](https://arxiv.org/abs/2305.18290) _Preprint_,
arXiv:2305.18290.


Nils Reimers and Iryna Gurevych. 2019. [Sentence-](https://arxiv.org/abs/1908.10084)
bert: Sentence [embeddings](https://arxiv.org/abs/1908.10084) using siamese bert[networks.](https://arxiv.org/abs/1908.10084) In _Proceedings of the 2019 Conference on_
_Empirical Methods in Natural Language Processing_ .
Association for Computational Linguistics.


Nils Reimers and Iryna Gurevych. 2020. [Making](http://arxiv.org/abs/2004.09813)
monolingual sentence [embeddings](http://arxiv.org/abs/2004.09813) multilingual
using [knowledge](http://arxiv.org/abs/2004.09813) distillation. _arXiv_ _preprint_
_arXiv:2004.09813_ .


Pradeep Sunkara et al. 2024. [Adaptive](https://arxiv.org/abs/2405.07280) humor
generation: Enhancing [personalization](https://arxiv.org/abs/2405.07280) with user
[feedback.](https://arxiv.org/abs/2405.07280) _ArXiv_ .


Leonard Tang, Alexander Cai, Steve Li, and Jason Wang.
2022. [The naughtyformer: A transformer understands](https://arxiv.org/abs/2211.14369)
[offensive humor.](https://arxiv.org/abs/2211.14369) _Preprint_, arXiv:2211.14369.


Bolotova V. V., Blinov V. A., Mishchenko K. I.,
and Braslavski P. I. 2017. Which ir [model](https://www.dialog-21.ru/media/3905/bolotovavvetal.pdf) has
a better sense of [humor?](https://www.dialog-21.ru/media/3905/bolotovavvetal.pdf) search over a large
[collection](https://www.dialog-21.ru/media/3905/bolotovavvetal.pdf) of jokes. In _Computational_ _Linguistics_
_and_ _Intellectual_ _Technologies:_ _Proceedings_ _of_ _the_
_International Conference “Dialogue 2017”_, Moscow,
Russia. Russian State University For The Humanities.


Orion Weller and Kevin Seppi. 2019. [Humor detection:](https://arxiv.org/abs/1909.00252)
A transformer [gets](https://arxiv.org/abs/1909.00252) the last laugh. _Preprint_,
arXiv:1909.00252.


Yuhan Wu et al. 2024. [The role of cultural context in](https://ceur-ws.org/Vol-3740/paper-183.pdf)
[humor generation: A comparative study of western](https://ceur-ws.org/Vol-3740/paper-183.pdf)
and eastern [humor](https://ceur-ws.org/Vol-3740/paper-183.pdf) models. In _CEUR_ _Workshop_
_Proceedings_ .


Diyi Yang, Alon Lavie, Chris Dyer, and Eduard
Hovy. 2015. [Humor recognition and humor anchor](https://doi.org/10.18653/v1/D15-1284)
[extraction.](https://doi.org/10.18653/v1/D15-1284) In _Proceedings of the 2015 Conference on_
_Empirical Methods in Natural Language Processing_,
pages 2367–2376, Lisbon, Portugal. Association for
Computational Linguistics.


Wei Zhang et al. 2024. [Improving humor in language](https://arxiv.org/abs/2405.20956)
[models through multimodal context.](https://arxiv.org/abs/2405.20956) _ArXiv_ .



9


**A** **Appendix**


Text Drawback
well.... [https://imgur.com/gallery/2CmdahS] links
(https://imgur.com/gallery/2CmdahS)

`占占占人占占占人占占点占点占点占占` . . . `占占` not latin characters
```
     占
```

A veteran walks into a bar. 12 people in the bar [removed]

[removed]

Chinas president is so bad beacuse.... [Deleted] [deleted]
lock lock me, i dare you. not a joke (excessively
short)
Test post Test not a joke (excessively
short)
meat meat meat meat meat meat meat meat meat meat repetition (excessively
meat meat meat meat meat meat meat meat meat meat long)
meat meat meat meat meat meat meat meat meat meat
meat meat meat meat meat meat meat meat meat meat
meat meat meat meat meat meat meat meat meat meat
meat meat meat meat meat meat meat meat meat meat
meat meat meat meat meat meat meat meat meat meat
meat meat meat



Mars is Earth’s second moon Mars is Earth’s second
moon Mars is Earth’s second moon Mars is Earth’s
second moon Mars is Earth’s second moon... (and so
on)



repetition (excessively
long)



Table 3: Different types of noise before initial preprocessing of the English data. All the provided examples were
removed after initial preprocessing that includes the removal of corrupted characters and excessively short or long
examples (shorter than 30 or longer than 150 characters).


10


Joke ruBERT
Conversatinal
Toxicity
Classifer



Multilingual
Detoxify



Если бы я была принцессой, то моим замком был
бы ликеро-водочный завод. _(If I were a princess, my_
_castle would be a distillery.)_



0 0.01



Где твоя грудь? Ты ее спугнул. _(Where_ _are_ _your_ 1 0.83
_breasts? You scared them away.)_



Мы не будем больше встречаться... Что, тараканы
в твоей голове проголосовали против меня? _(We_
_won’t_ _be_ _dating_ _anymore..._ _What,_ _the_ _bugs_ _in_ _your_
_head voted against me?)_



0 0.73



Table 4: Different toxicity classifiers results for CleanComedy Russian, 1 – for toxic, 0 – neutral, for ruBERTConv
we considered jokes with score more than 0.1 to be inappropriate.


Duplicate Cosine
English
what’s a rock group with four guys that don’t sing? mount rushmore
What rock group has four guys who can’t sing? Mount Rushmore. 0.922
who’s an all male rock group that doesn’t sing? mount rushmore . 0.8857
what do you call a rock group with no bassist, drummer, singer or guitarist? 0.741
Mount Rushmore

Q: What do you call a male quartet? A: Three men and a tenor. 0.528
Russian
а зачем в низу эскалатора бабулька в будке сидит? - она там педали крутит.
_(Why is grandma sitting in a booth at the bottom of the escalator? - She’s pedalling there.)_
А знаете, зачем в метро внизу эскалатора бабулька в будке? Она там педали 0.928
крутит. _(Do you know why there is a granny in a booth in the subway at the_
_bottom of the escalator? She’s pedalling there.)_



Привет, как дела? Вот все тебе надо знать.
_(Hi, how are you? You gotta know everything, don’t you?)_

- Привет! Как дела? - Порадовать тебя нечем. - Как? Неужели всё хорошо?
_(Hello!_ _How_ _are_ _you?_ _-_ _I_ _can’t_ _please_ _you_ _with_ _anything._ _-_ _How_ _come?_ _Is_
_everything really good?)_


Table 5: Cosine similarity between duplicates


11



0.9033


Joke Label
English
Romeo: Your cheeks are like petals. Juliet: Really? Romeo: Yes, bicycle neutral
pedals.

What would one call a movie about meth addictions? Need for speed. drugs
what do you call ghosts that haunt liquor stores? spirits alcohol
What do Syrian refugees eat for breakfast? Syrial! racist
Bought my epileptic girlfriend a strobe light for her birthday. She will offending
have a fit when she sees it.

Why can’t you have Christmas dinner in the EU? Because there is no politics
turkey.

Russian
Иногда я выпиваю стакан воды, просто для того что бы удивить свою alcohol
печень. _(Sometimes I drink a glass of water, just to surprise my liver.)_




 - Знаешь, я целый месяц ходила на фитнес!... - И сколько сбросила? 12 тысяч!!!... _(- You know, I went to fitness for a whole month!... - And_
_how much did you lose? - 12 hundred!!!...)_

Лучше было бы, если бы народные избранники отвечали не за свои
предвыборные слова, а за свои послевыборные дела. _(It would be better_
_if the people’s representatives were responsible not for their pre-election_
_words, but for their post-election deeds.)_



neutral


politics



99 процентов моей подготовки к экзамену это курение с грустным drugs
лицом. _(99 of my exam preparation involves smoking with a sad face.)_



Бомжи вышли на демонстрацию против новых технологий. По их словам, в коробке из-под плоского телевизора вообще жить невозможно.
_(Homeless people demonstrated against new technologies. According to_
_them, it is generally impossible to live in a flat-screen TV box.)_

Американский турист ходит с гидом по Лондону. — Все тут у вас
такое маленькое, зажатое, — говорит он. — Это здание, например,
было бы в Америке раз в десять выше. — О, конечно, сэр! Это-же
психиатрическая клиника. _(An_ _American_ _tourist_ _walks_ _with_ _a_ _guide_
_around London._ _“Everything_ _here is_ _so_ _small_ _and_ _cramped,”_ _he says._
_“This building, for example, would be ten times taller in America.” - Oh,_
_of course, sir! This is a psychiatric clinic.)_


Table 6: Sentiment analysis


12



offending


racist


Joke Cluster name
English
Idea:A Transformers movie that can transform into a movie
much better movie.



’Why did voldermort used Twitter instead of
Facebook? Because he only had followers. Not
friends.



facebook



What did the Jewish man say to himself on a hot day? jews
I should be used to being in an oven by now.

What kind of bee can’t be understood? A mumble bee
bee !

what do you call a dead bee?a was bee
What happens to someone who gets attacked by bees? bee
They get bee’d up

I just tried coffee for the first time... To be honest, it coffee
wasn’t my cup of tea...

What do you call a cat in love? Romeow cat
Russian
Вся жизнь — футбол, а ты в ней — сборная России. футбол _(football)_
_(All_ _life_ _is_ _football,_ _and_ _in_ _it_ _you_ _are_ _the_ _Russian_
_national team.)_



Доктор, помогите мне. У меня проблема. Я часто
ошибаюсь в людях. Я не доктор. _(Doctor, help me._
_I_ _have_ _a_ _problem._ _I_ _often_ _make_ _mistakes_ _in_ _people._
_I’m not a doctor.)_

Поймал мужик золотую рыбку хочу машину и
завод. Рыбка: хорошо но в кредит или по лизингу?
Старик: так выбирай на подсолнечном или сливочном? _(A man caught a goldfish and tells it that_
_he wants a car and a factory. Goldfish: okay, do you_
_want to loan or to lease it? Old man: so choose oil or_
_fat?)_

Я не понимаю фразу: Устал, как собака. Моя
собака спит, ест и гуляет. Я бы сам от такой жизни
не отказался. _(I don’t understand the phrase: Tired_
_like a dog. My dog sleeps, eats and walks. I myself_
_would not refuse such a life.)_

В компании со мной обычно смеются не над шуткой, а над тем, как я смеюсь над шуткой. _(People_
_with me usually laugh not at the joke, but at the way_
_I laugh at the joke.)_



доктор _(doctor)_


рыба _(fish)_


собака _(dog)_


юмор _(humour)_



Table 7: Sentiment analysis


13


Figure 4: Topic modeling for CleanComedy English.


Figure 5: Topic modeling for CleanComedy English.


14


Figure 6: Number of jokes rated by one person for English (in the left picture) and Russian (in the right picture).
Only annotators with at least one score are taken into account.


Figure 7: Age of annotators for English (in the left picture) and Russian (in the right picture). Only annotators with
at least one score are taken into account.


Figure 8: Gender of annotators for English (in the left picture) and Russian (in the right picture). Only annotators
with at least one score are taken into account.


15


Figure 9: Education level of annotators for English (in the left picture) and Russian (in the right picture). Only
annotators with at least one score are taken into account.


Figure 10: Language level of annotators. Only annotators with at least one evaluation point are taken into account.


16


