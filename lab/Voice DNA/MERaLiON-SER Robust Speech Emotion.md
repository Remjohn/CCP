## **MERaLiON-SER: Robust Speech Emotion** **Recognition Model for English and SEA Languages**

**MERaLiON Team**
Institute for Infocomm Research (I [2] R), A*STAR, Singapore
Corresponding Author: Hardik B. Sailor
```
              sailorhb@a-star.edu.sg

```

**Abstract**


We present **MERaLiON-SER** [1], a robust speech emotion recognition model designed for English and Southeast Asian languages. The model is trained using a
hybrid objective combining weighted categorical cross-entropy and Concordance
Correlation Coefficient (CCC) losses for joint discrete and dimensional emotion
modelling. This dual approach enables the model to capture both the distinct
categories of emotion (like ’happy’ or ’angry’) and the fine-grained, such as arousal
(intensity), valence (positivity/negativity), and dominance (sense of control), leading to a more comprehensive and robust representation of human affect. Extensive
evaluations across multilingual Singaporean languages (English, Chinese, Malay,
and Tamil ) and other public benchmarks show that MERaLiON-SER consistently
surpasses both open-source speech encoders and large Audio-LLMs. These results
underscore the importance of specialised speech-only models for accurate paralinguistic understanding and cross-lingual generalisation. Furthermore, the proposed
framework provides a foundation for integrating emotion-aware perception into
future _agentic audio systems_, enabling more empathetic and contextually adaptive
multimodal reasoning.


**1** **Introduction**


Human speech is a rich medium not only for semantic communication, but also for conveying
emotional and paralinguistic information such as affective states, intention, and interpersonal stance.
Recognising emotions from speech has become a foundational task in affective computing and humanmachine interaction: accurate speech emotion recognition (SER) enables applications ranging from
virtual assistants that adapt to user mood, to mental-health monitoring, to empathetic conversational
agents in service and robotics domains.


Yet despite impressive progress in speech processing and representation learning, SER remains
significantly more challenging than many seemingly “solved" tasks in speech and language. First,
emotional expression in speech is inherently ambiguous and subjective: different listeners often
disagree on the label of a given utterance, mixed emotions may co-occur, and prosodic cues can vary
wildly across speakers, languages and cultures. For example, work on annotation ambiguity shows
that labelling disagreements among raters are common and that collapsing those disagreements into a
single “majority” label may discard useful signal.


Second, SER suffers from annotation scarcity and imbalance: many datasets are small, acted rather
than spontaneous, and heavily biased toward a handful of well-studied languages (e.g., English).
Under-resourced languages or code-mixed scenarios (typical in multilingual regions) are far less
represented.


1Huggingface model and demo is available here: https://huggingface.co/MERaLiON/MERaLiON-SER-v1


Third, cross-domain and cross-corpus transfers remain problematic: models trained on one dataset
(speakers, recording conditions, culture) often degrade drastically when applied to a different domain.
Domain shifts include language, speaker demographics, recording channel or environment noise.


Fourth, although large self-supervised and multimodal models (e.g., speech encoders or audiolanguage models) provide powerful acoustic and semantic representations, they often prioritize
linguistic content (ASR or transcription) over paralinguistic cues [Chen et al., 2025]. As a result, even
state-of-the-art audio-LLMs may under-perform when tasked with fine-grained emotion reasoning in
multilingual or culturally diverse scenarios.


In multilingual and culturally diverse regions (such as Southeast Asia), emotional expression can
be shaped by language mixing, prosodic variation, and code-switching. These phenomena demand
models that capture both linguistic and paralinguistic signals, adapt across languages and speakers,
and remain robust to annotation and domain shift.


In this work, we present **MERaLiON-SER**, a robust, parameter-efficient speech emotion recognition
model tailored for English and Southeast Asian languages. As the model was developed under the
MERaLiON project, it is accordingly designated as MERaLiON-SER. Unlike general audio-language
models, which are optimised primarily for speech-to-text or audio-text tasks, MERaLiON-SER
emphasises paralinguistic specialisation for learning emotion intent directly from speech, independent
of transcription. Our experiments show strong generalisation across Singaporean multilingual codemixed speech, Southeast Asian languages, and public benchmark datasets. This design positions
MERaLiON-SER as a key building block towards emotionally intelligent, multilingual and agentic
audio systems.


**2** **Model description**


The proposed architecture employs the Whisper-Medium encoder as the foundational backbone for
multilingual acoustic feature extraction. Building upon this encoder, a custom downstream network
is introduced, comprising attention-based pooling layers followed by modified Emphasized Channel
Attention, Propagation and Aggregation in Time Delay Neural Network (ECAPA-TDNN) modules to
capture both temporal dynamics and speaker-invariant paralinguistic features [Desplanques et al.,
2020]. Compared to the original ECAPA-TDNN model, we replaced all BatchNorm layers with
GroupNorm layers. The model adopts a multi-head output design to jointly address categorical and
dimensional emotion recognition tasks. Specifically, the categorical head branch includes a softmax
layer for seven discrete emotions, while the dimensional head branch includes a sigmoid layer to
estimate three continuous dimension scores. **This model supports seven emotion classes, namely,**
**Neutral,** **Happy,** **Sad,** **Angry,** **Surprised,** **Fearful,** **Disgusted** **and** **three** **dimensional** **emotion**
**scores for arousal, valence, dominance.** This joint learning approach facilitates fine-grained and
segmental prosody rich representation of emotional expressions.


To mitigate overfitting and computational overhead during training, the Whisper encoder parameters
are kept frozen, while Low-Rank Adaptation (LoRA) adapters are integrated into the attention layers
(key, query, and value). This training approach enable efficient task-specific fine-tuning [Hu et al.,
2022]. Furthermore, to capture emotional cues at multiple temporal resolutions, we introduce novel
multiscale and hierarchical attention pooling techniques that enable the model to effectively combine
short and long-term emotion cues. The overall block diagram of the model is shown in Figure 1. The
downstream model includes ECAPA-TDNN pooling layers, and task-specific output heads.


Overall, the model is designed with an emphasis on parameter-efficient multilingual affective modeling and temporal abstraction, enabling the extraction of expressive emotional representations without
extensive retraining or large-scale parameter updates. This design philosophy balances computational
efficiency, generalization capability, and cross-lingual transferability, making the model suitable for
scalable deployment in diverse speech-based affective computing applications


**3** **Training Details**


**3.1** **Loss Functions**


The overall objective combined categorical and dimensional emotion losses. The categorical branch
optimized a weighted cross-entropy loss with label smoothing = 0.1, while the dimensional branch


2


Categorical labels Dimensional scores











Figure 1: Block diagram of proposed model


employed the Concordance Correlation Coefficient (CCC) loss. The total loss was a weighted sum of
these components with coefficients _λ_ cat = 1 _._ 0 and _λ_ dim = 0 _._ 5.


The loss function was a weighted sum of the following components:


**Weighted Cross-Entropy Loss (CE)** for the categorical emotion classification:



_L_ CE = _−_



_C_

- _wi · yi_ log( ˆ _yi_ ) _,_ (1)


_i_ =1



where _C_ is the number of emotion classes, _yi_ is the ground truth for the _i_ -th class, _y_ ˆ _i_ is the predicted
probability, and _wi_ is the weight assigned to the _i_ -th class to handle class imbalance.


**Concordance Correlation Coefficient (CCC) Loss** for the dimensional emotion regression:


2 _·_ cov( _y,_ ˆ _y_ )
_L_ CCC = 1 _−_ var( _y_ ) + var(ˆ _y_ ) + ( _µy −_ _µy_ ˆ) [2] _[,]_ (2)


where _y_ and _y_ ˆ are the true and predicted dimensional values, respectively, _µy_ and _µy_ ˆ are the means of
the true and predicted values, and cov( _y,_ ˆ _y_ ) and var( _y_ ), var(ˆ _y_ ) are the covariance and variance terms.


The combined loss function is a weighted sum of the above components:


_L_ = _λ_ cat _L_ CE + _λ_ dim _L_ CCC _,_ (3)


where _λ_ cat and _λ_ dim are the scaling coefficients for the categorical and dimensional, respectively.


**3.2** **Training Configuration**


Optimization was carried out using two parameter groups: a low learning rate for the frozen backbone
with LoRA adapters (learning rate=5e-5, weight decay = 4e-5) and a higher rate for the downstream
network (learning rate=6e-4, weight decay = 8e-5). A cosine annealing scheduler with a 0.08 warmup ratio was employed to gradually adjust the learning rate during training. To improve model
generalization, label smoothing with an _ϵ_ of 0.1 was employed during training. The model was
trained for 15 epochs with a batch size of 32 on single node with 8 Nvidia H100 GPUs. We used
development set categorical loss as early stopping criteria.


3


During training, extensive data augmentations were applied to ensure robustness to environmental and
speaker variations. MixUp was performed with a probability of 0.5 and mixing coefficient _α_ = 0 _._ 3

[Zhang et al., 2018]. Additional augmentations include additive noise drawn from the MUSAN
corpora [Snyder et al., 2015] and speed perturbations with factors of 0.9 and 1.1, respectively.


**4** **Datasets**


**4.1** **Training datasets**


The MERLION-SER was trained using a combination of proprietary labeled, pseudo-labeled, and
open-source datasets that allows usage in commercial model building.


**4.1.1** **SG training dataset**


Two training datasets were used in this model that include SG languages: the SG-ECMT train set and
the SGTV dataset.


**SG-ECMT Train Set** : The SG-ECMT train set consists of speech data in English, Malay, Chinese,
and Tamil, the four major languages spoken in Singapore. This data is derived from our proprietary
unlabeled raw speech corpora, containing 10–30 seconds segments across the following seven emotion
categories: neutral, angry, disgusted, fearful, happy, sad, and surprised.


The raw data was processed and filtered following the pipeline described in [Wang et al., 2025a].
Specifically, emotion labels were estimated every 4 seconds with a 2 seconds overlap using the
emotion2vec pipeline [Ma et al., 2024b], which classifies speech into nine categories: the seven target
emotions listed above, plus _other_ and _unknown_ .


To ensure high-quality labeling, we retained only the segments where both the emotion2vec+ seed
and emotion2vec+ base models produced identical predictions among the six target emotions (angry,
disgusted, fearful, happy, sad, surprised). Speech segments without consistent emotion predictions
were labeled as neutral. Speech samples were then selected based on the number of emotional
segment occurrences to ensure reliable emotion representation within each utterance [Wang et al.,
2025b].


The resulting SG-ECMT dataset comprises 27,458, 14,212, 14,370, and 10,169 samples for the
English, Chinese, Malay, and Tamil training sets, respectively. This pseudo-labeled dataset was
subsequently used to generate a second set of pseudo labels using our MERaLiON-SER model in a
two-pass labeling process.


**SGTV Dataset:** The SGTV dataset is an internally created, human-labeled emotional speech dataset.
This data consists of approximately 117,000 speech samples (about 120 hours) collected from
Singaporean TV shows and movies. Data primarily include English, Mandarin Chinese and codemixed utterances between the two languages. Emotion labels were manually annotated by trained
human annotators and include the seven categories from the SG-ECMT train set.


**4.1.2** **Open source training set**


We trained the model using publicly available open-source datasets. This includes CREMA-D [Cao
et al., 2014], M3ED [Huang et al., 2021], ESD [Zhou and Zhou, 2018], and MELD [Poria et al.,
2019].


**4.2** **Evaluation dataset**


The model’s performance was rigorously evaluated on both manually validated Singapore language
sets and public multilingual benchmarks.


**4.2.1** **Manually curated SG evaluation set**


We curated the SG-ECMT evaluation set following the same procedure as the SG-ECMT train set. It
consists of 1,880 speech samples, each ranging from 10–30 seconds in duration. Initially, we selected
80 samples per emotion category per language for English, Chinese, Malay, and Tamil.


4


Subsequently, three native-speaking human validaters for each language manually reviewed and
corrected the automatically generated emotion labels. Then a majority-vote scheme was applied to
finalize the labels.


In total, the resulting evaluation sets comprise 466, 466, 479, and 469 samples for English, Chinese,
Malay, and Tamil, respectively.


**4.2.2** **Public evaluation set**


We also used popular public datasets for English, Chinese, and Indonesia. For English, we used
MSP-podcast test1 [Busso et al., 2017], IEMOCAP five test folds [Busso et al., 2008], and MELD.
We also included M3ED for Chinese and IndoWaveSentiment for Indonesia.


**5** **Evaluation setup**


For evaluation, we averaged the predictions from the top four model checkpoints, selected based
on the lowest categorical loss on the development set, to ensure robust and stable performance. We
benchmarked our proposed model against both open-source and closed-source systems covering a
range of architectures and modalities.


**Open-source Speech-only Models:** We included three variants of **emotion2vec** - _Large_, _Base_, and
_Seed_ that differ in model capacity and pretraining data. These models represent strong speech-only
baselines for emotion recognition.


**Open-source Audio LLMs:** To compare with recent large-scale multimodal speech models optimized for Southeast Asian (SEA) languages, we evaluated **MERaLiON-10B** [He et al., 2024]
and **SeaLLMs-Audio-7B** [Liu et al., 2025]. Both models incorporate speech-text alignment during
finetuning and demonstrate strong cross-lingual generalization.


**Closed-source** **Multimodal** **Models:** For completeness, we further compared our model with
two state-of-the-art proprietary systems: **GPT-4o-Audio** [Achiama et al., 2023] and **Gemini-2.5-**
**Flash** [Anil et al., 2025]—which are capable of joint reasoning across audio and text modalities.


**Prompt and Inference Configuration:** A uniform prompt was used for fair evaluation across all
LLM-based models:

```
    PROMPT = "Determine the speaker’s emotion in the given audio.
    Reply with a single label from: Neutral, Happy, Sad, Angry,
    Fearful, Disgusted, Surprised."

```

Table 1: Summary of baseline and comparison models used for evaluation.


**Model** **Type** **Parameters** **Availability** **License**


_Open-source Speech-only Models_
emotion2vec-large Speech-only Encoder 300M Open-source Not mentioned*
emotion2vec-base Speech-only Encoder 90M Open-source Not mentioned*
emotion2vec-seed Speech-only Encoder 90M Open-source Not mentioned*
MERaLiON-SER Speech-only Encoder 309M Open-source MIT


_Open-source Audio LLMs (SEA-optimized)_
MERaLiON-10B Audio LLM 10B Open-source MIT
SeaLLMs-Audio-7B Audio LLM 7B Open-source Not mentioned


_Closed-source Multimodal Models_
GPT-4o-Audio Multimodal LLM - Closed-source Paid API
Gemini-2.5-Flash Multimodal LLM - Closed-source Paid API

*All emotion2vec models include several datasets that restrict their commercial usage.


5


**6** **Results and Discussion**


In SER task, class imbalance is a persistent challenge, as certain emotions such as neutral or happy
typically dominate spontaneous datasets, while others like fear or disgust occur infrequently. Conventional performance metrics, such as weighted accuracy or traditional accuracy tend to be dominated
by these majority classes, often masking a model’s poor discrimination of minority emotions. To
provide a more balanced evaluation, researchers in the affective computing community commonly use
Unweighted Average Recall (UAR) also known as Balanced Accuracy as the principal metric. Unlike
weighted accuracy which aggregates correct predictions proportional to class distribution—UAR
offers a class-independent assessment that more accurately reflects a model’s generalization capability
across diverse emotional states.


We have evaluated MERaLiON-SER-v1 performance on evaluation set of SG-ECMT dataset. The
SG-ECMT dataset for Singapore languages contains fine-grained labels at every two seconds and
merged nearby segments to create a course level segments with maximum of 15 second duration. We
have also added performance of primary 4 classes in emotion literature: Neutral, Angry, Sad, and
Happy.


**6.1** **Evaluation on Singapore Languages**


Figure 2 presents the UAR across four Singapore languages—English, Chinese, Malay, and
Tamil—under both 7-class and 4-class emotion settings, evaluated using fine-grained 2-second
segments and merged segments ranging from 2–15 seconds.


Overall, **MERaLiON-SER-v1** achieves the highest average UAR across all configurations, outperforming both open-source speech encoders ( _emotion2vec-large,_ _base,_ _seed_ ) and multimodal
LLMs ( _GPT-4o-Audio,_ _Gemini-2.5-flash,_ _MERaLiON-2-10B,_ _SeaLLMs-Audio-7B_ ). Specifically,
MERaLiON-SER-v1 reaches 53.9% (7-class, 2s), 60.2% (7-class merged), 65.1% (4-class, 2s), and
70.0% (4-class merged), surpassing the best open-source speech encoder ( _emotion2vec-seed_ ) by +4.9,
+2.3, +7.1, and +4.3 absolute UAR points respectively.


**Speech-only vs.** **multimodal LLMs:** Among the speech-only models, the performance ranking
is consistent across all settings: **MERaLiON-SER-v1** _> emotion2vec-seed > emotion2vec-base ≈_
_emotion2vec-large_ . Audio-LLMs, though trained with large-scale data, lag behind specialized SER
models: MERaLiON-2-10B achieves mid-tier performance (43–60%), while SeaLLMs-Audio-7B
remains the lowest-performing system. Closed-source LLMs perform competitively with merged
segments but still underperform on fine-grained 7-class tasks, underscoring the need for task-specific
acoustic representation learning.


**Language-specific observations:** MERaLiON-SER-v1 dominates in English, Chinese, and Tamil,
while emotion2vec-seed slightly surpasses it for Malay. However, in case of primary 4-class evaluation, MERaLiON-SER-v1 achieves competitive performance as emotion2vec for Malay language.


**6.2** **Evaluation on Public Multilingual Datasets**


We further evaluated the models on five publicly available emotion datasets: three English corpora
( **MSP-Podcast**, **IEMOCAP**, **MELD** ), one Chinese corpus ( **M3ED** ), and one Indonesian corpus
( **IndoWaveSentiment** ). These datasets differ in style—acted vs. spontaneous speech, monologue vs.
dialogue, and high- vs. low-resource settings—allowing a robust test of cross-domain generalization.
The results are shown in Figure 3 for different models.


**Overall comparison:** Across all datasets, **MERaLiON-SER-v1** again delivers the highest UAR,
achieving 64–70% on English corpora and around 57–60% on Chinese and Indonesian data. The
emotion2vec has three variants and results shows that performance is not consistent across datasets
and hence there is no single emotion2vec model that is better across all datasets. The best open-source
baseline ( _emotion2vec-seed_ ) lags by 4–6% absolute UAR, while multimodal LLMs (e.g., GPT-4oAudio, Gemini-2.5-flash) trail by 8–12%. Despite having larger parameter counts, MERaLiON-2-10B
remains below MERaLiON-SER-v1, indicating that model scale does not substitute for paralinguistic
specialization.


6


80


60


40


20





0


|Col1|Col2|Col3|Col4|Col5|Col6|Col7|Col8|Col9|Col10|Col11|Col12|
|---|---|---|---|---|---|---|---|---|---|---|---|
|||||||||||||
|||||||||||||


|Col1|Col2|Col3|Col4|Col5|Col6|Col7|Col8|Col9|Col10|Col11|Col12|Col13|Col14|Col15|Col16|Col17|Col18|Col19|Col20|Col21|Col22|Col23|Col24|Col25|Col26|Col27|Col28|Col29|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
||||||||||||||||||||||||||||||
||||||||||||||||||||||||||||||



80


60


40


20





0

|English Chinese Malay Tamil 4-Class 2s|Col2|Col3|Col4|Col5|Col6|Col7|Col8|Col9|Col10|Col11|Col12|
|---|---|---|---|---|---|---|---|---|---|---|---|
|||||||||||||
|||||||||||||
|||||||||||||
|||||||||||||

English Chinese Malay Tamil Avg



|English Chinese Malay Tamil Avg 4-Class Merged Segments (2 15s)|Col2|Col3|Col4|Col5|Col6|Col7|Col8|Col9|Col10|Col11|Col12|Col13|Col14|Col15|Col16|Col17|Col18|Col19|Col20|Col21|Col22|Col23|Col24|Col25|Col26|Col27|Col28|Col29|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
||||||||||||||||||||||||||||||
||||||||||||||||||||||||||||||
||||||||||||||||||||||||||||||
||||||||||||||||||||||||||||||


English Chinese Malay Tamil Avg















**7** **Related Work**


**7.1** **Self-Supervised and Representation Learning for SER**


Recent years have seen major advances via self-supervised learning (SSL) based speech models (e.g.,
Wav2Vec 2.0, HuBERT, WavLM) that learn contextualised acoustic features from large unlabeled
corpora [Mohamed et al., 2022]. These representations improve downstream SER—especially when
fine-tuned with an emotion-specific dataset [Naini et al., 2024]. There are several benchmarks


7


that show the importance of speech SSL and large scale models like Whisper for speech emotion
recognition [Ma et al., 2024a], [Osman et al., 2024]. There are very limited attempts to create a large
scale speech emotion model that is open source and can perform well on different languages. One
notable attempt is emotion2vec where authors released open source models with different model sizes
and training configurations [Ma et al., 2024b]. Other open source model releases include models
specifically trained by single dataset that is MSP podcast [Feng et al., 2025].


**7.2** **Audio-Language Models and Emotion Reasoning**


The frontier of audio-text understanding has expanded significantly with the rise of audio large
language models (AudioLLM) and multimodal agents (e.g., GPT-4o-Audio, Gemini). Past efforts to
incorporate paralinguistic understanding into these models generally fall into three categories: (1)
fine-tuning on specific emotional datasets [Lin et al., 2024a, Kim et al., 2024, Kang et al., 2024, Wang
et al., 2024]„ (2) knowledge distillation from specialized emotion recognition systems [Lu et al., 2024,
2025, Wang et al., 2024], and (3) translating acoustic cues directly into text prompts Wu et al. [2025],
Lin et al. [2024b], Xu et al. [2024], Wu et al. [2024]. Crucially, however, these general-purpose
AudioLLM consistently prioritize speech semantics (transcription) over subtle paralinguistic cues
(such as emotion and other speaker traits). As a result, their capacity for fine-grained emotion
reasoning remains fundamentally limited. This persistent gap motivates the need for specialized SER
models built explicitly for deep emotional representation. In summary, while large pre-trained and
multimodal models offer broad applicability, specialized SER models continue to play a vital role in
capturing affective nuance.


**8** **Limitations and Future Work**


MERaLiON-SER demonstrates strong multilingual generalization and outperforms large multimodal
models on speech emotion recognition task. Here, we highlight few limitations as well. First, the
model was trained on pseudo-labeled data for certain languages, which despite careful filtering may
introduce label noise and bias. We conducted human-verified annotation task for evaluation set only.
Our future work is to enhance this by adding small amount of manually labeled dataset for languages
that does not have training dataset. Second, this model provides seven emotion classes and hence can
not be used for other categories such as contempt or for cases where complex emotional contexts
is required such as sarcasm detection. However, dimensional scores make it possible to give more
generalised emotion representation space.


Beyond these limitations, a promising research direction lies in integrating MERaLiON-SER within
agentic frameworks, where emotion understanding can guide reasoning, dialogue planning, and empathetic response generation. Since existing Audio-LLMs are often limited in affective reasoning due
to text-dominant alignment, a hybrid system where MERaLiON-SER acts as an emotional perception
module could provide emotionally grounded signals to autonomous agents or conversational systems.
Such extension would pave the way for next-generation empathetic Audio-LLMs and agentic AI
systems capable of reasoning not only about emotions but also through them.


**9** **Conclusions**


We released MERaLiON-SER, a robust speech emotion recognition model developed for English
and Southeast Asian languages. In both regional (Singapore) and public multilingual benchmarks,
MERaLiON-SER achieves superior and consistent performance across languages, emotion granularity, and segment durations. The results emphasize that, despite advances in multimodal LLMs,
speech-only encoders with targeted paralinguistic learning remain essential for fine-grained affective
reasoning and cross-lingual robustness.


**Acknowledgments and Disclosure of Funding**


The computational work for this article was fully performed on resources of the National Supercomputing Centre (NSCC), Singapore (https://www.nscc.sg). We acknowledge Frank and his team
from Asiastar International Consultancy Pte Ltd, who were engaged as an external consultancy to
perform human annotations for the speech emotion annotation task. We also thank student intern


8


Arjun Srinivas to help for data and automated emotion labeling work. This research is supported by
the National Research Foundation, Singapore under its National Large Language Models Funding
Initiative. Any opinions, findings, conclusions, or recommendations expressed in this material are
those of the author(s) and do not reflect the views of the National Research Foundation, Singapore.


**References**


J. Achiama, S. Adler, S. Agarwal, L. Ahmad, I. Akkaya, F. L. Aleman, D. Almeida, J. Altenschmidt,
S. Altman, S. Anadkat, and et al. GPT-4 technical report. _arXiv preprint arXiv:2303.08774_, 2023.


R. Anil, S. Borgeaud, J.-B. Alayrac, J. Yu, R. Soricut, J. Schalkwyk, A. M. Dai, A. Hauth, K. Millican,
D. Silver, and et al. Gemini: A family of highly capable multimodal models. _arXiv_ _preprint_
_arXiv:2312.11805_, 2025.


C. Busso, M. Bulut, C.-C. Lee, E. Kazemzadeh, E. M. Provost, S. Kim, J. N. Chang, S. Lee, and
S. S. Narayanan. IEMOCAP: interactive emotional dyadic motion capture database. _Language_
_Resources and Evaluation_, 42:335–359, 2008.


C. Busso, M. Al-Hames, and Z. Liu. MSP-Podcast: A large-scale corpus for research on affective
computing in the wild. _IEEE Transactions on Affective Computing_, 8(4):455–469, 2017.


H. Cao, D. G. Cooper, M. K. Keutmann, R. C. Gur, A. Nenkova, and R. Verma. CREMA-D: Crowdsourced emotional multimodal actors dataset. _IEEE Transactions on Affective Computing_, 5(4):
377–390, 2014.


J. Chen, Z. Guo, J. Chun, P. Wang, A. Perrault, and M. Elsner. Do Audio LLMs Really LISTEN,
or Just Transcribe? Measuring Lexical vs. Acoustic Emotion Cues Reliance. _arXiv_ _preprint_
_arXiv:2510.10444_, 2025.


B. Desplanques, J. Thienpondt, and K. Demuynck. ECAPA-TDNN: Emphasized channel attention,
propagation and aggregation in tdnn based speaker verification. In _Proc._ _Interspeech_, pages
3830–3834, 2020.


T. Feng, J. Lee, A. Xu, Y. Lee, T. Lertpetchpun, X. Shi, H. Wang, T. Thebaud, L. Moro-Velazquez,
D. Byrd, et al. Vox-profile: A speech foundation model benchmark for characterizing diverse
speaker and speech traits. _arXiv preprint arXiv:2505.14648_, 2025.


Y. He, Z. Liu, S. Sun, B. Wang, W. Zhang, X. Zou, N. F. Chen, and A. T. Aw. MERaLiON-AudioLLM:
Technical report. _arXiv preprint arXiv:2412.09818_, 2024.


E. J. Hu, Y. Shen, P. Wallis, Z. Allen-Zhu, Y. Li, S. Wang, L. Wang, W. Chen, et al. LoRA: Low-rank
adaptation of large language models. _ICLR_, 1(2):3, 2022.


Z. Huang, H. Yang, M. Yan, and Q. Yang. M3ED: A multi-modal multi-turn multi-level multilabel emotional dialogue dataset. In _Proceedings of the 29th ACM International Conference on_
_Multimedia (MM ’21)_, 2021.


W. Kang, J. Jia, C. Wu, W. Zhou, E. Lakomkin, Y. Gaur, L. Sari, S. Kim, K. Li, J. Mahadeokar,
et al. Frozen large language models can perceive paralinguistic aspects of speech. _arXiv preprint_
_arXiv:2410.01162_, 2024.


H. Kim, S. Seo, K. Jeong, O. Kwon, S. Kim, J. Kim, J. Lee, E. Song, M. Oh, J.-W. Ha, S. Yoon,
and K. M. Yoo. Paralinguistics-aware speech-empowered large language models for natural
conversation. In _The Thirty-eighth Annual Conference on Neural Information Processing Systems_
_(NeurIPS)_, 2024.


G.-T. Lin, C.-H. Chiang, and H.-Y. Lee. Advancing large language models to capture varied speaking
styles and respond properly in spoken conversations. _arXiv preprint arXiv:2402.12786_, 2024a.


W.-C. Lin, S. Ghaffarzadegan, L. Bondi, A. Kumar, S. Das, and H.-H. Wu. CLAP4Emo: ChatGPTAssisted Speech Emotion Retrieval with Natural Language Supervision. In _IEEE International_
_Conference on Acoustics, Speech and Signal Processing (ICASSP)_, pages 11791–11795, 2024b.


9


C. Liu, M. Aljunied, G. Chen, H. P. Chan, W. Xu, Y. Rong, and W. Zhang. SeaLLMs-Audio:
Large Audio-Language Models for Southeast Asia. `[https://github.com/DAMO-NLP-SG/](https://github.com/DAMO-NLP-SG/SeaLLMs-Audio)`
`[SeaLLMs-Audio](https://github.com/DAMO-NLP-SG/SeaLLMs-Audio)`, 2025.


K.-H. Lu, Z. Chen, S.-W. Fu, H. Huang, B. Ginsburg, Y.-C. Wang, and H.-y. Lee. DeSTA: Enhancing
speech language models through descriptive speech-text alignment. In _Interspeech_, pages 4159–
4163, 2024. doi: 10.21437/Interspeech.2024-457.


K.-H. Lu, Z. Chen, S.-W. Fu, C.-H. H. Yang, J. Balam, B. Ginsburg, Y.-C. Wang, and H.-y. Lee.
DeSTA2: Developing instruction-following speech language model without speech instructiontuning data. In _IEEE_ _International_ _Conference_ _on_ _Acoustics,_ _Speech_ _and_ _Signal_ _Processing_
_(ICASSP)_, 2025.


Z. Ma, M. Chen, H. Zhang, Z. Zheng, W. Chen, X. Li, J. Ye, X. Chen, and T. Hain. EmoBox:
Multilingual Multi-corpus Speech Emotion Recognition Toolkit and Benchmark. In _Interspeech_
_2024_, pages 1580–1584, 2024a.


Z. Ma, Z. Zheng, J. Ye, J. Li, Z. Gao, S. Zhang, and X. Chen. emotion2vec: Self-supervised
pre-training for speech emotion representation. In _Findings of the Association for Computational_
_Linguistics (ACL)_, 2024b.


A. Mohamed, H.-y. Lee, L. Borgholt, J. D. Havtorn, J. Edin, C. Igel, K. Kirchhoff, S.-W. Li,
K. Livescu, L. Maaløe, T. N. Sainath, and S. Watanabe. Self-supervised speech representation
learning: A review. _IEEE Journal of Selected Topics in Signal Processing_, 16(6):1179–1210, 2022.


A. R. Naini, M. A. Kohler, E. Richerson, D. Robinson, and C. Busso. Generalization of selfsupervised learning-based representations for cross-domain speech emotion recognition. In _2024_
_IEEE_ _International_ _Conference_ _on_ _Acoustics,_ _Speech_ _and_ _Signal_ _Processing_ _(ICASSP)_, pages
12031–12035, 2024.


M. Osman, D. Z. Kaplan, and T. Nadeem. SER Evals: In-domain and Out-of-domain benchmarking
for speech emotion recognition. In _Interspeech 2024_, pages 1395–1399, 2024. doi: 10.21437/
Interspeech.2024-2440.


S. Poria, D. Hazarika, N. Majumder, G. Naik, E. Cambria, and R. Mihalcea. MELD: A multimodal
multi-party dataset for emotion recognition in conversations. In _Proceedings of the 57th Annual_
_Meeting of the Association for Computation al Linguistics (ACL)_, 2019.


D. Snyder, G. Chen, and D. Povey. MUSAN: A Music, Speech, and Noise Corpus. _arXiv preprint_
_arXiv:1510.08484_, 2015.


C. Wang, M. Liao, Z. Huang, J. Wu, C. Zong, and J. Zhang. BLSP-Emo: Towards empathetic large
speech-language models. _Proceedings of the 2024 Conference on Empirical Methods in Natural_
_Language Processing (EMNLP)_, 2024.


Q. Wang, H. B. Sailor, T. Liu, and A. T. Aw. Contextual paralinguistic data creation for multi-modal
speech-llm: Data condensation and spoken QA generation. In _Proc. Interspeech_, 2025a.


Q. Wang, H. B. Sailor, T. Liu, W. Zhang, M. Huzaifah, N. Lertcheva, S. Sun, N. F. Chen, J. Wu, and
A. Aw. Benchmarking contextual and paralinguistic reasoning in speech-llms: A case study with
in-the-wild data. In _Findings of EMNLP 2025_, 2025b.


H. Wu, H.-C. Chou, K.-W. Chang, L. Goncalves, J. Du, J.-S. R. Jang, C.-C. Lee, and H.-Y. Lee.
Empower typed descriptions by large language models for speech emotion recognition. In _Asia_
_Pacific Signal and Information Processing Association Annual Summit and Conference (APSIPA_
_ASC)_, pages 1–6. IEEE, 2024.


Z. Wu, Z. Gong, L. Ai, P. Shi, K. Donbekci, and J. Hirschberg. Beyond silent letters: Amplifying
LLMs in emotion recognition with vocal nuances. In _Findings of the Association for Computational_
_Linguistics:_ _NAACL 2025_, pages 2202–2218, 2025.


Y. Xu, H. Chen, J. Yu, Q. Huang, Z. Wu, S.-X. Zhang, G. Li, Y. Luo, and R. Gu. SECap: Speech
emotion captioning with large language model. In _Proceedings of the AAAI Conference on Artificial_
_Intelligence_, volume 38, pages 19323–19331, 2024.


10


H. Zhang, M. Cisse, Y. N. Dauphin, and D. Lopez-Paz. Mixup: Beyond empirical risk minimization.
_ICLR_, 2018.


Y. Zhou and L. Zhou. Emotional speech dataset (ESD) for voice conversion. In _Interspeech_, pages
2793–2797, 2018.


**10** **MERaLiON Team (alphabetical order)**


Aw Ai Ti, Chen Fang Yih Nancy, Chiu Ying Lay, Ding Yang, He Yingxu, Jiang Ridong, Li Jingtao,
Liao Jingyi, Liu Zhuohan, Lu Yanfeng, Ma Yi, Manas Gupta, Muhammad Huzaifah Bin Md Shahrin,
Nabilah Binte Md Johan, Nattadaporn Lertcheva, Pan Chunlei, Pham Minh Duc, Sailor Hardik
Bhupendra, Siti Maryam Binte Ahmad Subaidi, Siti Umairah Binte Mohammad Salleh, Sun Shuo,
Tarun Kumar Vangani, Wang Qiongqiong, Won Cheng Yi Lewis, Wong Heng Meng Jeremy, Wu
Jinyang, Zhang Huayun, Zhang Longyin, Zou Xunlong


11


