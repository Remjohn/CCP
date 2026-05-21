## **Activation Steering for Accent-Neutralized Zero-Shot Text-To-Speech**

_Mu Yang, John H. L. Hansen_


Center for Robust Speech Systems (CRSS), University of Texas at Dallas, USA

mu.yang@utdallas.edu, john.hansen@utdallas.edu



**Abstract**


Zero-shot Text-to-Speech (TTS) models can generate speech
that captures both the voice timbre and accent of a reference
speaker. However, disentangling these attributes remains challenging, as the output often inherits both the accent and timbre from the reference. In this study, we introduce a novel,
post-hoc, and training-free approach to neutralize accent while
preserving the speaker’s original timbre, utilizing inferencetime activation steering. We first extract layer-specific “steering vectors” offline, which are derived from the internal activation differences within the TTS model between accented and
native speech. During inference, the steering vectors are applied to guide the model to produce accent-neutralized, timbrepreserving speech. Empirical results demonstrate that the proposed steering vectors effectively mitigate the output accent and
exhibit strong generalizability to unseen accented speakers, offering a practical solution for accent-free voice cloning. [1]

**Index Terms** : Text-To-Speech, activation steering, accent neutralization, accent conversion


**1.** **Introduction**


Zero-shot Text-To-Speech (TTS) Synthesis is the task of generating speech for a target text using a reference speech utterance
(and sometimes optionally, the text transcript of the reference
speech) of an arbitrary speaker. The generated speech is expected to have the voice characteristics of the reference speaker
(e.g., timbre, prosody, accent, emotion, etc.). Recent advances
on generative models have enabled significant improvements
on zero-shot TTS. These include the use of Diffusion Models

[1, 2, 3, 4, 5], Autoregressive Large Language Models (LLM)

[6, 7, 8], and hybrid approaches that combine both LLM and
Diffusion strategies [9, 10, 11, 12, 13].
However, disentangling the control over different voice
characteristics remains a challenge. For example, when using
an accented reference speech, the generated speech often inherits both the accent and timbre from the reference. In this work,
we focus on accent-neutralized zero-shot TTS, which aims to
generate speech with the timbre of the reference speaker but
without the speaker’s accent. This is a practical problem for
accent-free voice cloning, which can be useful for various applications, such as creating training targets for Accent Conversion
(AC) models [14, 15], providing second-language (L2) learners with personalized accent-neutralized speech feedback for
computer-aided pronunciation training [16], etc.
Our solution is based on activation steering, a technique
that modifies the internal activations of a neural network during inference to control specific model behaviors. In generative


1Audio demo: [https://accentsteer.github.io/](https://accentsteer.github.io/)



models, it has been used to erase specific concepts in Diffusionbased image generation [17], detoxify and shift the sentiment of
LLM responses [18], alter the persona traits of LLMs [19], and
more [20, 21]. The efficacy of this approach demonstrates that
high-level semantic concepts can be represented as _linear_ _di-_
_rections_ in the activation space, and that steering the activations
along these directions can effectively control the corresponding concepts in the model responses. In this work, we ask the
following research question: since the internal activations of a
zero-shot TTS model contain information about multiple voice
characteristics, can we steer the activations to neutralize the reference speaker’s accent while preserving the timbre?

To this end, inspired by Persona Vectors [19], we propose a
_post-hoc and training-free_ approach. Specifically, as shown in
Figure 1, we first extract “steering vectors” offline. We feed the
TTS model with accented and neutral reference utterances respectively to produce the same target texts. The layer-wise differences between the averages of activations of the two conditions are considered as steering vectors, which we hypothesize
capture the direction that steers neutral representations towards
accented representations (and vice versa) in the activation space
of the TTS model. Then, during inference, the steering vectors are applied to corresponding layers to guide the model to
produce accent-neutralized, timbre-preserving speech. We conduct steering experiments on Qwen3-TTS [6], a state-of-the-art
LLM-based zero-shot TTS model. Empirical results show that
this simple steering approach can effectively mitigate the accent
in the output speech, while maintaining the reference speaker’s
timbre to a large extent, as measured by the speaker embedding
similarity. In addition, the steering vectors show strong generalizability to unseen accented speakers, whose utterances are not
used for steering vector extraction, suggesting that the steering
vectors capture a general direction for accent neutralization in
the activation space of the TTS model.


**2.** **Related Work**


Several prior works have explored activation steering to enhance the controllability of zero-shot TTS. Suni et. al. [22]
proposed a method to fit prosody and style vectors, which are
used to manipulate the embedding space of reference utterances. Counterfactual Activation Editing [23] uses external
classifiers and regressors to edit the internal representations of
the TTS model to achieve post-hoc prosody and mispronunciation control. EmoShift [24] builds lightweight activation steering layers on top of the output embeddings for emotion-aware
TTS. TruS [25] adopts a similar steering vectors extraction
method for inference-time speaker unlearning in a Diffusionbased TTS model. Our work is related to EmoSteer [26], which
pre-extracts emotion steering vectors for a Diffusion-based TTS


Ref. Text




















|Col1|Col2|Col3|...|Steering Vectors|
|---|---|---|---|---|
||||||
|||**TT**<br>❄<br>Transformer|**S Model**<br>...<br>Transformer|**S Model**<br>...<br>Transformer|
|Transformer|Transformer|Transformer|Transformer|Transformer|
|Transformer|||||



Figure 1: _The proposed activation steering framework for accent-neutralized zero-shot TTS. (a) Steering vectors are extracted offline_
_from_ _the_ _activation_ _differences_ _between_ _accented_ _and_ _neutral_ _speech,_ _and_ _(b)_ _applied_ _during_ _inference_ _to_ _guide_ _the_ _model_ _towards_
_accent-neutralized output while preserving timbre._ _In this paper, we experiment with single-layer steering, i.e., only one layer is steered_
_while other layers are left unchanged._ _The figure illustrates the general framework that multiple layers can be steered simultaneously._



model and relies on an external emotion classifier to select topk steering tokens, and thus requires multiple inference passes
to apply the steering vectors. In contrast, our method does not
require any external classifiers and applies the steering vectors
in a single autoregressive decoding pass, which is more efficient
and practical for real-time applications.


**3.** **Method**


**3.1.** **The Qwen3-TTS Model**


We extract steering vectors from the activations of Qwen3-TTS

[6], a state-of-the-art LLM-based zero-shot TTS model. It uses
a 12.5 Hz multi-codebook speech tokenizer with 1 semantic
stream and 15 acoustic streams derived from Residual Vector Quantization (RVQ) [27]. The Qwen3-TTS model consists
of a Qwen3-LLM-based backbone (28-layer Transformer) and
a lightweight Multi-Token Prediction (MTP) module (5-layer
Transformer) on top of the backbone. The backbone takes as input the aggregated codebook features from the speech tokenizer
and predicts the semantic token, and the MTP module then predicts the remaining acoustic tokens. In this work, we focus on
the activations from the backbone LLM, as it accounts for the
majority of the model parameters and is responsible for learning
the shared representations across different voice characteristics.


**3.2.** **Steering Vector Extraction**


For zero-shot TTS, Qwen3-TTS takes as input a reference
speech and its corresponding text transcript, and the target text
to be synthesized. To compute the steering vectors, we use
ARCTIC [28] and L2-ARCTIC [29] to curate an extraction
dataset with contrastive accent conditions. ARCTIC provides
US American English speech (considered as accent-neutral)
from 4 native speakers, while L2-ARCTIC provides accented
English speech for the same set of sentences in ARCTIC, where
each accented version is spoken by 4 L2 speakers. We randomly
sample two disjoint sets of _K_ sentences, one as the target texts
and one as the reference texts. For each of the target texts, we
pair it with one reference text and aggregate the corresponding
speech from the 4 native speakers and 4 accented speakers, creating the (target text, reference text, reference speech) triplets as
the TTS inputs. As shown in Figure. 1, we feed the triplets into
the TTS model to generate accented and neutral speech. For
each generated speech, we record layer-wise activations (each



Transformer layer’s output) within the backbone LLM, averaged over the generated tokens. Then the steering vectors are
computed as the difference between the mean activations of the
accented condition and the neutral condition:



_Nn_

- **a** [(] _l,i_ _[neutral]_ [)] (1)

_i_ =1



1
**v** _l_ = _Na_




- _Na_ **a** [(] _l,i_ _[accented]_ [)] _−_ _N_ 1 _n_

_i_ =1



where **v** _l_ _∈_ R _[d]_ is the steering vector for layer _l_ with the size of
hidden dimension _d_, **a** [(] _l,i_ _[accented]_ [)] and **a** [(] _l,i_ _[neutral]_ [)] are the averaged
activations of the _i_ -th generated sample at layer _l_, for the accented and neutral conditions, respectively, and _Na_ and _Nn_ are
the number of samples in each condition. We only keep track
of the activations of generated tokens, while the activations of
prompt tokens (i.e., reference speech and text) are excluded.
Since accent is coupled with speaker identity (i.e., the same
speaker always speaks with the same accent), the steering vectors may capture not only the accent but also the speaker information. To break the entanglement and encourage the steering vectors to capture more accent-specific information, during
steering vectors extraction, we apply on-the-fly data augmentations on reference speech waveforms to introduce perturbations
that modify the speaker’s voice [30, 31]. These perturbations
involve 3 sequential random transformations: 1) scaling all formant frequencies within an utterance by a random factor; 2)
scaling the fundamental frequency (F0) by a random factor; and
3) applying a random frequency-shaping equalizer. As these
scaling and frequency-shaping operations are uniformly applied
across the utterance, they primarily modify the speaker’s voice
while having minimal impact on the spoken content or accent.
For each sample, a random variable _γ_ is drawn from the uniform distribution _U_ (0 _,_ 1). Perturbations are applied if _γ_ _>_ 0 _._ 3;
otherwise, the original waveforms are used. We show the effect
of the data augmentation in ablation study (Section. 5.3).


**3.3.** **Inference-Time Steering for Accent Neutralization**


During inference, we apply the steering vectors to the corresponding layers of the backbone LLM to guide the model towards accent-neutralized output. Specifically, at each decoding
step _t_, we modify the activations of layer _l_ as follows:


**a** _[t]_ _l_ _[←]_     - **a** _[t]_ _l_ _[−]_ _[α][ ·]_ **[ v]** _l_     - _·_ _||_ **a** _[t]_ _l_ _[||]_ [2] (2)
_||_ **a** _[t]_ _l_ _[−]_ _[α][ ·]_ **[ v]** _[l][||]_ [2]


Table 1: _Evaluation results on L2-ARCTIC and speechocean762. The steering vectors are extracted using the samples from L2-ARCTIC,_
_and applied to both L2-ARCTIC and speechocean762 for evaluation._ _EN_ ~~_U_~~ _S (US American English) and EN_ ~~_C_~~ _N (Mandarin Chinese_
_English) denote the reference speech accents; ISR denotes Inference Success Rate; AMR-CN and AMR-US denotes Accent Match Rate_
_with EN_ ~~_C_~~ _N and EN_ ~~_U_~~ _S accent target, respectively._ _See Section._ _4 for more details on the evaluation metrics._ _Steering strength α is_
_set to 1.0 for all the steered models in the table._


**Evaluation** **Steering** **Prompt** **ISR** _↑_ **AMR-CN** _↓_ **AMR-US** _↑_ **WER** _↓_
**ID** **Model** **Spk Sim** _↑_ **UTMOS** _↑_
**Dataset** **Setting** **Accent** **(%)** **(%)** **(%)** **(%)**


1 EN US 100.00 0.00 100.00 0.87 3.34 1.04

Unsteered
2 EN ~~C~~ N 98.46 82.14 0.00 **0.85** **3.31** 3.98
Qwen3-TTS 0.6B

3 Steer layer 15 EN ~~C~~ N **98.68** **1.78** **97.33** **0.73** **3.18** **2.64**
4 L2-ARCTIC Steer layer 10 EN ~~C~~ N 96.04 4.35 94.74 0.72 3.10 3.18


5 EN US 100.00 0.00 100.00 0.87 3.38 0.97

Unsteered
6 EN ~~C~~ N **99.56** 83.89 1.10 **0.84** **3.33** 3.4
Qwen3-TTS 1.7B

7 Steer layer 15 EN ~~C~~ N **99.56** **9.49** **88.74** **0.76** **3.32** **2.24**
8 Steer layer 10 EN ~~C~~ N 99.34 18.14 79.87 **0.76** 3.22 2.63


9 Unsteered EN ~~C~~ N **97.00** **3.09** 0.00 **0.78** 2.73 56.41
speechocean762 Qwen3-TTS 1.7B

10 Steer layer 15 EN ~~C~~ N **92.00** **3.26** **48.91** **0.74** **3.01** **32.43**
11 Steer layer 10 EN ~~C~~ N 86.00 6.98 48.84 **0.74** 2.93 32.85



where **a** _[t]_ _l_ _[∈]_ [R] _[d]_ [is] [the] [activation] [at] [layer] _[l]_ [and] [decoding] [step]
_t_, and _α_ is a hyperparameter that controls the steering strength.
Note that the steering vectors indicate the direction that pushes
the activations of neutral speech towards those of accented
speech in the representation space. When the inference reference samples are accented, subtracting the steering vectors enables the negation of such “accent directions”, which steers the
accent activations towards neutral activations and thus mitigates
the accent in the generated speech. The normalization term is
applied to maintain the original activation norm. We empirically find that the normalization better preserves speaker timbre. Similar to the steering vectors extraction stage, the steering
vectors are only applied to the generated tokens, while the activations of the prompt tokens are not modified. In this study, we
experiment with single-layer steering, where only one layer is
steered while other layers are left unchanged.


**4.** **Experimental Setup**


**Datasets** We use ARCTIC and L2-ARCTIC for steering vector extraction. We focus on neutralizing the Mandarin Chineseaccented English. Speech and transcripts from the 4 Chinese-L1
speakers in L2-ARCTIC and the 4 native speakers in ARCTIC
are used for steering vector extraction. For each speaker, we
hold out 10% of the utterances as the evaluation set, and we
sample from the remaining utterances to extract steering vectors. As an out-of-distribution evaluation to test the generalizability of the steering vectors, we use speechocean762 [32],
which features 250 Mandarin Chinese-L1 speakers (adults and
children) with diverse English proficiency levels. We randomly
sample 100 utterances from the adult group of the test set, which
are paired with another 100 different text transcripts in speechocean762 as the target texts for TTS inference.

**Steering** **Vector** **Extraction** **and** **Steering** **Setting** We experiment with two sizes of pre-trained Qwen3-TTS models,
0.6B and 1.7B parameters. Both models have 28 Transformer layers in the backbone LLM. For each model, we extract steering vectors from the following layer indices (zeroindexed): 1 _,_ 5 _,_ 10 _,_ 15 _,_ 20 _,_ 25 _,_ 27. We use 4,000 ARCTIC plus
L2-ARCTIC samples for steering vector extraction (i.e. _Na_ +
_Nn_ = 4000 in Equation 3.2). During inference, we experiment



with two steering strengths _α_ : 1.0 and 2.0.
**Evaluation** **Metrics** We evaluate the generated speech on the
following metrics: 1) **Inference** **Success** **Rate** **(ISR)** : the percentage of samples where the TTS model successfully generates speech without errors, measuring the TTS model’s stability under steering [2] ; 2) **Accent** **Match** **Rate** **(AMR)** : the percentage of samples where the generated speech is classified as
having a specific accent (e.g. EN ~~C~~ N or EN ~~U~~ S) by an external pre-trained accent classifier [31] [3] ; 3) **Spk** **Sim** : the cosine
similarity between speaker embeddings of the generated speech
and the reference speech, where the speaker embeddings are
extracted using a pre-trained speaker encoder model [4] ; 4) **UT-**
**MOS** : the overall natrualness Mean of Opinion (MOS) score
predicted by UTMOSv2 [33]; 5) **Word** **Error** **Rate** **(WER)** :
we use Whisper-turbo [34] to transcribe the generated speech
and compute WER against the target text.


**5.** **Results**


**5.1.** **In-Domain and Cross-Domain Steering**


Table. 1 shows the evaluation results on L2-ARCTIC and speechocean762. The unsteered models (Rows 1 and 2, 5 and 6)
show high AMR following the prompt accent, meaning that the
generated speech inherits the accent from the reference speech.
For both the 0.6B and 1.7B models, when the prompt utterances
have accent, activation steering significantly reduces AMR-CN
and increases AMR-US, indicating effective accent neutralization. However, we also observe a drop on speaker similarity,
suggesting a trade-off between accent neutralization and timbre
preservation. For the 1.7B model, the Spk Sim drop (0.84 to
0.76 ) is less than the 0.6B model (Rows 6 and 7 vs. Rows 2
and 3). After listening to the speech generated with steering,
we find that in some cases, there are some local pitch shifts and


2We find that when steering with larger _α_ and in rare cases, even for
the unsteered baseline, the TTS model may get stuck in the decoding
loop due to the absence of a stop token. We consider such cases as failed
inference. Measuring the ISR is important to understand the relation
between activation steering and the TTS model’s stability.
3AMR-CN and AMR-US do not sum to 1 because the classifier was
trained on ARCTIC plus L2-ARCTIC, including 7 accents in total.
[4https://github.com/resemble-ai/Resemblyzer](https://github.com/resemble-ai/Resemblyzer)


100


80


60


40


20



|ISR (%)|Col2|
|---|---|
|ISR (%)||
|||
|||
|||
|||
|||


1 5 10 15 20 25 27
Steering Layer Index



80


60


40


20


0



|AMR-US (%)|Col2|
|---|---|
|AMR-US (%)||
|||
|||
|||
|||
|||


1 5 10 15 20 25 27
Steering Layer Index



0.85


0.80


0.75


0.70


0.65


0.60



|SPK-SIM|Col2|
|---|---|
|||
|||
|||
|||
|||


1 5 10 15 20 25 27
Steering Layer Index



3.3

3.2

3.1

3.0

2.9

2.8

2.7



|WER (%)|Col2|
|---|---|
|WER (%)||
|||
|||
|||
|||
|||


1 5 10 15 20 25 27
Steering Layer Index



|AMR-CN (%)|Col2|
|---|---|
|AMR-CN (%)||
|||
|||
|||
|||


1 5 10 15 20 25 27
Steering Layer Index



100


80


60


40


20


0



|UTMOS|Col2|
|---|---|
|||
|||
|||
|||
|||
|||


1 5 10 15 20 25 27
Steering Layer Index



4.5


4.0


3.5


3.0


2.5


2.0



0.6B, = 1.0 0.6B, = 2.0 0.6B, unsteered 1.7B, = 1.0 1.7B, = 2.0 1.7B, unsteered


Figure 2: _Layerwise single-layer steering analyses on L2-ARCTIC. Layers are zero-indexed (layer 1 means the 2nd layer)._ _Solid and_
_dashed lines represent the results of steering with different models and steering strengths. Dotted lines represent the unsteered baseline._



Table 2: _Ablation_ _study:_ _impact_ _of_ _the_ _number_ _of_ _samples_
_and data augmentation for steering vectors extraction (Section._
_3.2)._ _The steering vectors are extracted from the 1.7B model’s_
_layer_ _15._ _The_ _evaluation_ _is_ _conducted_ _on_ _L2-ARCTIC_ _with_
_EN_ ~~_C_~~ _N prompt accent._ _Steering strength α is set to 1.0._


**ISR** _↑_ **AMR-US** _↑_ **WER** _↓_
**# Samples** **Augmentation** **Spk Sim** _↑_ **UTMOS** _↑_
**(%)** **(%)** **(%)**


w/ aug. 99.56 88.74 **0.76** **3.32** **2.24**
4000
w/o aug. **100.00** **93.41** 0.75 3.27 2.49


w/ aug. 99.56 87.42 **0.77** **3.32** 2.42
1000
w/o aug. **99.78** **93.61** 0.74 3.27 **2.24**


w/ aug. **100.00** 93.19 **0.73** **3.28** **2.14**
40
w/o aug. **100.00** **95.60** 0.70 3.27 2.46


prosody changes that may contribute to the accent neutralization. [5] Nevertheless, overall, the speaker identity is still largely
preserved. UTMOS is also improved or maintained after steering. This indicates the high natraulness of the generated speech
under steering. The WER improvement may be attributed to
the reduced accent (and potentially mispronunciations), making the generated speech more intelligible [36]. The steering
vectors also show strong generalizability to unseen accented
speakers in speechocean762, as evidenced by the significant improvement of AMR-US compared to the unsteered condition.
Noteblely, WER is significantly reduced after steering (56.41%
to 32.43%, Rows 9 and 10). This may be due to the fact that
speechocean762 speakers have much more diverse proficiency
levels, and the speech recordings contain more pronunciation
errors and disfluencies than the L2-ARCTIC speakers, making
the zero-shot voice cloning more challenging and produces less
natural and intelligible speech. The proposed steering vectors
may provide a mitigation solution for such challenging cases.


**5.2.** **Layerwise Steering Analyses**


We analyze the steering effect across layers. Figure. 2 shows
the 6 metrics when steering these layers with different models
and steering strengths. When _α_ = 1 _._ 0, from the AMR-CN,
AMR-US and Spk Sim curves, we can see that in general, steering the middle layers (15 and 20) provides the most balanced
trade-off between accent neutralization and timbre preservation,
while steering the early layers and top layers has a weaker effect
on accent neutralization but stronger timbre preservation. This


5Another reason of the Spk Sim drop may be due to the speaker encoder model’s sensitivity to accent changes. Prior works on Emotional
Voice Conversion [35] showed that speaker embeddings could be distant even for the same speaker with different emotions. We hypothesize
that this may also be the case for accent changes.



echos the findings in Persona Vectors [19] which showed that
steering middle layers has a stronger effect on persona traits
expression. When increasing to _α_ = 2 _._ 0, although the overall AMR-CN reduction is larger, Spk Sim also drops significantly. This suggests a negative effect of over-steering the “accent vectors”: it aggressively deviates the representations far
from the reference speaker’s original activation space, causing
drastic speaker identity change.
The UTMOS and WER curves show that steering middle
layers (especially layer 15) also leads to better naturalness and
intelligibility, even matching or surpassing the unsteered baseline, while steering early layers and top layers could cause
naturalness and intelligibility degradation. Particularly, when
_α_ = 2 _._ 0, steering early layers causes significant ISR drops, suggesting that the early layers are more sensitive to over-steering
and more likely to cause inference failure. In addition, the 1.7B
model shows better stability (steerability) than the 0.6B model,
as evidenced by the higher ISR under the same steering settings.


**5.3.** **Ablation Study on Steering Vectors Extraction**


In this section, we investigate the impact of the number of samples and data augmentation for steering vector extraction (Section. 3.2). We experiment with three different numbers of samples: 40, 1000, and 4000. For each setting, we compare the
steering vectors extracted with and without data augmentation.
The results are shown in Table. 2. We find that the data augmentation effectively improves Spk Sim. This suggests that the
proposed data augmentation can help break the entanglement
between accent and speaker identity, and encourage the steering
vectors to capture more accent-specific information. In terms of
the number of needed samples for steering vector extraction, it
seems that 1000 samples are sufficient to achieve a decent balance between accent neutralization and timbre preservation.


**6.** **Conclusion**


In this work, we introduce a novel, simple yet effective activation steering method for accent-neutralized zero-shot TTS. We
extract layer-wise steering vectors based on the activation differences between accented and neutral speech. During inference, these vectors guide the model toward generating accentneutralized speech while preserving the speaker’s timbre. Experimental results on Qwen3-TTS demonstrate that the proposed steering vectors effectively reduce accents in the synthesized speech while largely retaining the speaker’s timbre. Furthermore, the steering vectors exhibit strong generalizability to
unseen accented speakers, indicating that they capture a universal direction for accent neutralization within the activation
space of the TTS model.


**7.** **Generative AI Use Disclosure**


Generative AI tools were only used for polishing and editing
of the manuscript. We did not use any generative AI tools for
designing the technical method, conducting experiments, or analyzing the results.


**8.** **References**


[1] Y. Chen, Z. Niu, Z. Ma, K. Deng, C. Wang, J. JianZhao, K. Yu,
and X. Chen, “F5-tts: A fairytaler that fakes fluent and faithful
speech with flow matching,” in _Proceedings_ _of_ _the_ _63rd_ _Annual_
_Meeting of the Association for Computational Linguistics (Volume_
_1:_ _Long Papers)_, 2025, pp. 6255–6271.

[2] S. E. Eskimez, X. Wang, M. Thakker, C. Li, C.-H. Tsai, Z. Xiao,
H. Yang, Z. Zhu, M. Tang, X. Tan _et al._, “E2 tts: Embarrassingly
easy fully non-autoregressive zero-shot tts,” in _2024 IEEE spoken_
_language technology workshop (SLT)_ . IEEE, 2024, pp. 682–689.

[3] Z. Ju, Y. Wang, K. Shen, X. Tan, D. Xin, D. Yang, Y. Liu, Y. Leng,
K. Song, S. Tang, Z. Wu, T. Qin, X.-Y. Li, W. Ye, S. Zhang,
J. Bian, L. He, J. Li, and S. Zhao, “Naturalspeech 3: zero-shot
speech synthesis with factorized codec and diffusion models,” ser.
ICML’24. JMLR.org, 2024.

[4] S. Kim, K. Shih, J. F. Santos, E. Bakhturina, M. Desta, R. Valle,
S. Yoon, B. Catanzaro _et_ _al._, “P-flow: A fast and data-efficient
zero-shot tts through speech prompting,” _Advances in Neural In-_
_formation Processing Systems_, vol. 36, pp. 74 213–74 228, 2023.

[5] H. Zhu, W. Kang, Z. Yao, L. Guo, F. Kuang, Z. Li, W. Zhuang,
L. Lin, and D. Povey, “Zipvoice: Fast and high-quality zero-shot
text-to-speech with flow matching,” _Proc. ASRU_, 2025.

[6] H. Hu, X. Zhu, T. He, D. Guo, B. Zhang, X. Wang, Z. Guo,
Z. Jiang, H. Hao, Z. Guo _et_ _al._, “Qwen3-tts technical report,”
_arXiv preprint arXiv:2601.15621_, 2026.

[7] X. Wang, M. Jiang, Z. Ma, Z. Zhang, S. Liu, L. Li, Z. Liang,
Q. Zheng, R. Wang, X. Feng _et_ _al._, “Spark-tts: An efficient llmbased text-to-speech model with single-stream decoupled speech
tokens,” _arXiv preprint arXiv:2503.01710_, 2025.

[8] Z. Ye, X. Zhu, C.-M. Chan, X. Wang, X. Tan, J. Lei, Y. Peng,
H. Liu, Y. Jin, Z. Dai _et_ _al._, “Llasa: Scaling train-time and
inference-time compute for llama-based speech synthesis,” _arXiv_
_preprint arXiv:2502.04128_, 2025.

[9] Z. Du, Q. Chen, S. Zhang, K. Hu, H. Lu, Y. Yang, H. Hu,
S. Zheng, Y. Gu, Z. Ma _et_ _al._, “Cosyvoice: A scalable multilingual zero-shot text-to-speech synthesizer based on supervised
semantic tokens,” _arXiv preprint arXiv:2407.05407_, 2024.

[10] Z. Du, Y. Wang, Q. Chen, X. Shi, X. Lv, T. Zhao, Z. Gao,
Y. Yang, C. Gao, H. Wang _et al._, “Cosyvoice 2: Scalable streaming speech synthesis with large language models,” _arXiv preprint_
_arXiv:2412.10117_, 2024.

[11] H.-H. Guo, Y. Hu, F.-Y. Shen, X. Tang, Y.-C. Wu, F.-L. Xie, and
K. Xie, “Fireredtts-1s: An upgraded streamable foundation textto-speech system,” _arXiv preprint arXiv:2503.20499_, 2025.

[12] S. Zhou, Y. Zhou, Y. He, X. Zhou, J. Wang, W. Deng, and
J. Shu, “Indextts2: A breakthrough in emotionally expressive
and duration-controlled auto-regressive zero-shot text-to-speech,”
_arXiv preprint arXiv:2506.21619_, 2025.

[13] X. Zhang, X. Zhang, K. Peng, Z. Tang, V. Manohar, Y. Liu,
J. Hwang, D. Li, Y. Wang, J. Chan _et_ _al._, “Vevo: Controllable
zero-shot voice imitation with self-supervised disentanglement,”
in _The_ _Thirteenth_ _International_ _Conference_ _on_ _Learning_ _Repre-_
_sentations_, 2025.

[14] Y. Halychanskyi, C. Churchwell, Y. Wen, and V. Kindratenko,
“Fac-facodec: Controllable zero-shot foreign accent conversion
with factorized speech codec,” _arXiv preprint arXiv:2510.10785_,
2025.

[15] W. Quamer, A. Das, J. Levis, E. Chukharev-Hudilainen, and
R. Gutierrez-Osuna, “Zero-Shot Foreign Accent Conversion without a Native Reference,” in _Interspeech_ _2022_, 2022, pp. 4920–
4924.




[16] K. Hirschi, O. Kang, M. Yang, J. H. Hansen, and K. Beloin, “Artificial intelligence-generated feedback for second language intelligibility: an exploratory intervention study on effects and perceptions,” _Language Learning_, vol. 75, no. S1, pp. 204–241, 2025.


[17] T. Gaintseva, A.-M. Oncescu, C. Ma, Z. Liu, M. Benning,
G. Slabaugh, J. Deng, and I. Elezi, “CASteer: Cross-attention
steering for controllable concept erasure,” in _The_ _Fourteenth_ _In-_
_ternational Conference on Learning Representations_, 2026. [Online]. Available: [https://openreview.net/forum?id=6D5Odqol1B](https://openreview.net/forum?id=6D5Odqol1B)


[18] A. M. Turner, L. Thiergart, G. Leech, D. Udell, J. J. Vazquez,
U. Mini, and M. MacDiarmid, “Steering language models with
activation engineering,” _arXiv preprint arXiv:2308.10248_, 2023.


[19] R. Chen, A. Arditi, H. Sleight, O. Evans, and J. Lindsey, “Persona
vectors: Monitoring and controlling character traits in language
models,” _arXiv preprint arXiv:2507.21509_, 2025.


[20] K. Li, O. Patel, F. Vi´egas, H. Pfister, and M. Wattenberg,
“Inference-time intervention: Eliciting truthful answers from a
language model,” _Advances_ _in_ _Neural_ _Information_ _Processing_
_Systems_, vol. 36, pp. 41 451–41 530, 2023.


[21] P. Rodriguez, A. Blaas, M. Klein, L. Zappella, N. Apostoloff,
marco cuturi, and X. Suau, “Controlling language and diffusion
models by transporting activations,” in _The_ _Thirteenth_ _Interna-_
_tional_ _Conference_ _on_ _Learning_ _Representations_, 2025. [Online].
Available: [https://openreview.net/forum?id=l2zFn6TIQi](https://openreview.net/forum?id=l2zFn6TIQi)

[22] A. Suni, S. Le Maguer, S. Kakouros, T. T¨or¨o, and J. Simko, “Style [ˇ]
and Prosody control for Zero-shot Speech Synthesis,” in _13th edi-_
_tion of the Speech Synthesis Workshop_, 2025, pp. 28–34.


[23] K. Lee, A. Stitsyuk, G. Jho, I. Hwang, and J. Choi, “Counterfactual Activation Editing for Post-hoc Prosody and Mispronunciation Correction in TTS Models,” in _Interspeech_ _2025_, 2025, pp.
434–438.


[24] L. Zhou, H. Jiang, J. Li, T. Wang, and H. Li, “Emoshift:
Lightweight activation steering for enhanced emotion-aware
speech synthesis,” _arXiv preprint arXiv:2601.22873_, 2026.


[25] M. Lee, E. Shin, and J. Lee, “Erasing your voice before it’s heard:
Training-free speaker unlearning for zero-shot text-to-speech,”
_arXiv preprint arXiv:2601.20481_, 2026.


[26] T. Xie, S. Yang, C. Li, D. Yu, and L. Liu, “Emosteer-tts: Finegrained and training-free emotion-controllable text-to-speech via
activation steering,” _arXiv preprint arXiv:2508.03543_, 2025.


[27] A. D´efossez, L. Mazar´e, M. Orsini, A. Royer, P. P´erez, H. J´egou,
E. Grave, and N. Zeghidour, “Moshi: a speech-text foundation
model for real-time dialogue,” _arXiv preprint arXiv:2410.00037_,
2024.


[28] J. Kominek and A. W. Black, “The cmu arctic speech databases,”
in _Fifth ISCA workshop on speech synthesis_, 2004.


[29] G. Zhao, S. Sonsaat, A. Silpachai _et al._, “L2-arctic: A non-native
english speech corpus.” in _Proc. Interspeech_, 2018.


[30] K. Qian, Y. Zhang, H. Gao, J. Ni, C.-I. Lai, D. Cox, M. HasegawaJohnson, and S. Chang, “Contentvec: An improved selfsupervised speech representation by disentangling speakers,” in
_International_ _conference_ _on_ _machine_ _learning_ . PMLR, 2022,
pp. 18 003–18 017.


[31] M. Yang, R. C. M. C. Shekar, O. Kang, and J. H. L. Hansen,
“What Can an Accent Identifier Learn? Probing Phonetic and
Prosodic Information in a Wav2vec2-based Accent Identification
Model,” in _Interspeech 2023_, 2023, pp. 1923–1927.


[32] J. Zhang, Z. Zhang, Y. Wang, Z. Yan, Q. Song, Y. Huang, K. Li,
D. Povey, and Y. Wang, “speechocean762: An open-source nonnative english speech corpus for pronunciation assessment,” in
_Proc. Interspeech 2021_, 2021.


[33] K. Baba, W. Nakata, Y. Saito, and H. Saruwatari, “The t05 system
for the VoiceMOS Challenge 2024: Transfer learning from deep
image classifier to naturalness MOS prediction of high-quality
synthetic speech,” in _IEEE_ _Spoken_ _Language_ _Technology_ _Work-_
_shop (SLT)_, 2024, pp. 818–824.


[34] A. Radford, J. W. Kim, T. Xu, G. Brockman, C. McLeavey, and
I. Sutskever, “Robust speech recognition via large-scale weak
supervision,” in _International_ _conference_ _on_ _machine_ _learning_ .
PMLR, 2023, pp. 28 492–28 518.


[35] Z. Du, J. Lu, K. Zhou, L. Kaushik, and B. Sisman, “Converting
Anyone’s Voice: End-to-End Expressive Voice Conversion with
A Conditional Diffusion Model,” in _The_ _Speaker_ _and_ _Language_
_Recognition Workshop (Odyssey 2024)_, 2024, pp. 172–179.


[36] M. Yang, K. Hirschi, S. D. Looney, O. Kang, and J. H. Hansen,
“Improving Mispronunciation Detection with Wav2vec2-based
Momentum Pseudo-Labeling for Accentedness and Intelligibility
Assessment,” in _Interspeech 2022_, 2022, pp. 4481–4485.


