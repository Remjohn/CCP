## **Enhancing Speech Emotion Recognition with Graph-Based Multimodal** **Fusion and Prosodic Features for the Speech Emotion Recognition in** **Naturalistic Conditions Challenge at Interspeech 2025**

_Alef Iury Ferreira_ [1] _, Lucas Rafael Gris_ [1] _, Alexandre Ferro Filho_ [1] _, Lucas_ _Olives_ _[´]_ [1] _, Daniel Ribeiro_ [1] _,_
_Luiz Fernando_ [1] _, Fernanda Lustosa_ [2] _, Rodrigo Tanaka_ [3] _, Frederico Oliveira_ [4] _, Arlindo Galv˜ao Filho_ [1]


1Federal University of Goi´as, Brazil
2Federal University of Rio Grande do Norte, Brazil
3Aeronautics Institute of Technology, Brazil
4Federal University of Mato Grosso, Brazil

alef ~~i~~ ury ~~c~~ .c@discente.ufg.br, lucas.gris@discente.ufg.br, fred.santos.oliveira@gmail.com



**Abstract**


Training SER models in natural, spontaneous speech is especially challenging due to the subtle expression of emotions and
the unpredictable nature of real-world audio. In this paper, we
present a robust system for the INTERSPEECH 2025 Speech
Emotion Recognition in Naturalistic Conditions Challenge, focusing on categorical emotion recognition. Our method combines state-of-the-art audio models with text features enriched
by prosodic and spectral cues. In particular, we investigate the
effectiveness of Fundamental Frequency (F0) quantization and
the use of a pretrained audio tagging model. We also employ an
ensemble model to improve robustness. On the official test set,
our system achieved a Macro F1-score of 39.79% (42.20% on
validation). Our results underscore the potential of these methods, and analysis of fusion techniques confirmed the effectiveness of Graph Attention Networks. Our source code is publicly
available. [1] .
**Index Terms** : speech emotion recognition, speech representations


**1.** **Introduction**


Speech emotion recognition (SER) is a critical component of affective computing and human–computer interaction [1]. Early
SER relied on hand-crafted features but struggled with realworld generalization [2]. Several factors contribute to these
limitations, including individual variability in emotional expression and the subjective nature of emotion labeling [3]. To address these challenges, recent advances in deep learning and
self-supervised learning (SSL) have transformed the field by
leveraging large-scale unlabeled speech data to learn robust and
transferable representations, significantly enhancing SER performance [4]. However, challenges remain when processing
natural speech because emotions are expressed subtly and in
a spontaneous way [5].
Recent work has shown that multi-task learning can improve SER performance by jointly addressing related tasks such
as speech-to-text recognition and emotion classification [6].
Other studies have introduced domain-specific pretext tasks
that use audiovisual cues to learn better emotional representations [7]. In the Odyssey 2024 Speech Emotion Recognition
Challenge [8], several studies adopted a multimodal approach
by combining audio and text inputs, achieving significantly bet

1https://github.com/alefiury/
InterSpeech-SER-2025



ter performance compared to audio-only methods. In this context, the integration of SSL models in a multimodal context has
emerged as a promising approach in the field.
In this paper, we present a system for the INTERSPEECH
2025 Speech Emotion Recognition in the Naturalistic Conditions Challenge. The challenge consists of two tracks: categorical emotion recognition and emotional attribute prediction. This study focuses on categorical emotion recognition.
Our approach builds on recent advances by combining state-ofthe-art audio models, including Wav2Vec2 [9], HuBERT [10],
WavLM [11], Whisper [12], and XEUS [13], alongside a text
encoder based on RoBERTa [14]. The feature set is enriched by
adding prosodic features like Fundamental Frequency (F0) and
spectral features such as Mel-Spectrograms. We also use Sequential Feature Resampling (SeqAug) [15] for data augmentation and a majority voting ensemble to improve overall performance. We tested several configurations of the system and
combined various approaches in a final ensemble model.
Extensive experiments and ablation studies confirm that
our bimodal and multimodal fusion techniques significantly
improve performance. Our results align with recent research

[16, 8, 17], offering valuable insights for the advancement of
multimodal emotion recognition. Additionally, we also investigate the F0 quantization for prosodic modeling and the
use of Consistent Ensemble Distillation (CED) [18] for MelSpectrogram processing. The remainder of this paper is structured as follows: Section 2 reviews related work and Section
3 outlines the proposed system. Section 4 details the experimental setup, while Section 5 presents and discusses the results.
Finally, Section 6 concludes the paper.


**2.** **Related Work**


Recent research has improved SER performance through multimodal fusion, self-supervised learning (SSL), and deep learning architectures. The Odyssey 2024 Challenge demonstrated
the advantages of combining speech and text, with top systems
leveraging ensemble SSL models, attention-based fusion, and
class imbalance mitigation [8, 16].
Other architectures based on hierarchical cross-attention
models (HCAM) [19] and Multimodal Dual Attention Transformers (MDAT) [17] improve feature interaction. HCAM
applies bidirectional gated recurrent units (GRUs) with selfattention and cross-modal attention to refine multimodal embeddings, whereas MDAT employs a transformer-based dualattention mechanism, incorporating both graph attention and


Figure 1: _Overview of the proposed system architecture for multimodal emotion recognition._



co-attention layers to enhance cross-modal dependencies.


Originally introduced for graph-structured data [20], Graph
Attention Networks (GATs) dynamically assign attention
weights to different nodes, allowing for adaptive feature importance estimation. In [17], the MDAT integrates graph attention
and co-attention mechanisms to enhance multimodal fusion in
cross-language SER. Their model applies graph attention layers to dynamically learn dependencies between speech and text
embeddings, refining modality-specific features while capturing cross-modal interactions. Additionally, they introduced a
transformer encoder layer for high-level feature representation,
further improving emotion classification accuracy across multiple languages. Their findings highlight the robustness of graphbased fusion, demonstrating superior generalization compared
to conventional multimodal approaches. Our work extends this
investigation by evaluating the effectiveness of GATs for multimodal SER in spontaneous speech settings.


**3.** **Proposed System**


Figure 1 illustrates our system. The hidden states of the last
layer _L_ of the text encoder are denoted by _ZT_ _[L]_ [(] _[j]_ [)][ for positions]
_j_ = 1 _, . . ., N_ and from the speech encoder by _ZS_ _[L]_ [(] _[t]_ [)][ for frames]
_t_ = 1 _, . . ., T_ . After fusion, modality-specific representations
are maintained as _ZF,T_ ( _j_ ) (text) and _ZF,S_ ( _t_ ) (speech). We further integrate discretized F0 embeddings _ZF_ 0( _k_ ) (with _k_ indexing the F0 sequence) and spectral features _ZSpec_ from the CED
model. Our approach was built based on four main stages:


1. **Unimodal** **Speech** **Model** **Selection** : We compare several
SSL-based audio encoders to identify the most robust unimodal backbone.

2. **Bimodal Fusion with Text** : We incorporate text representations from a pretrained text encoder to leverage content-based
features. We also evaluate various fusion strategies.

3. **Prosodic** **and** **Spectral** **Feature** **Integration** : We augment
the fused embeddings with discretized F0 embeddings and
spectral information through the CED).

4. **Additional** **Strategies** : We investigate some additional
strategies in order to enhance the model robustness such as
data augmentation and the use of SwiGLU [21] activation in
the MLP module.



**3.1.** **Unimodal Speech Model Selection**


We began by comparing five popular open-source SSL speech
models: Wav2vec2 Large [2], Whisper Large V3 [3], WavLM
Large [4], HuBERT Large [5] and XEUS [6] . All models except XEUS
were initialized using Hugging Face checkpoints, while XEUS
was initialized with the ESPNet Toolkit [22].
For prototyping efficiency, we pre-extracted features from
the last hidden layer of each SSL model. This allowed us to
rapidly iterate and compare their performances on the filtered
validation set (with ‘X’ and ‘O’ labels removed). The model
yielding the highest macro F1-score on this unimodal configuration was selected as the audio backbone for subsequent multimodal experiments.


**3.2.** **Bimodal Fusion with Text Encoder**


After selecting the best-performing audio encoder, we incorporated a text modality to provide content-based features. We
used RoBERTa Large [7] as the text encoder, with transcriptions obtained with the state-of-the-art Canary ASR model [23].
To ensure consistency, we relied solely on Canary-generated
transcriptions, bypassing the dataset’s original annotations.
RoBERTa embeddings were pre-extracted for efficiency.
Following, we explored multiple fusion strategies for integrating speech and text representations. A simple concatenation approach was first tested, where mean-pooled features
from both modalities were combined and passed through an
MLP classifier. Next, we evaluated early fusion via a singlelayer Transformer encoder, refining each modality’s representation before applying mean pooling and classification [24].
Additionally, we implemented Hierarchical Cross Attention
(HCAM) [19], where bidirectional GRUs with self-attention
refine SSL-based features before cross-attention layers enable
inter-modal communication. Unlike [19], we applied an attentive pooling strategy before classification.


2https://huggingface.co/facebook/
wav2vec2-large
3https://huggingface.co/openai/
whisper-large-v3
4https://huggingface.co/microsoft/wavlm-large
5https://huggingface.co/facebook/
hubert-large-ll60k
6https://huggingface.co/espnet/xeus
7https://huggingface.co/FacebookAI/
roberta-large


Finally, we examined the Multimodal Dual Attention
Transformer (MDAT) [17], which integrates graph attention
modules [20] and cross-attention mechanisms. MDAT utilizes
two Transformer encoders for further refinement, differing from
our early fusion setup by employing eight multihead attention
heads, which yielded better performance in preliminary experiments.


**3.3.** **Prosodic and Spectral Feature Integration**


This work incorporates a prosodic modality derived from the
F0, as previous work has shown that it is closely linked to
speech emotion [25]. We adopt a quantization-based approach,
inspired by [26], to model F0 contours. Raw F0, extracted using
the RMVPE [27] model, is mel-scaled and quantized into 256
bins, with an additional padding index. These bins are mapped
to learnable 256-dimensional embeddings, projected to 512 dimensions, and mean-pooled in the time dimension. This representation is concatenated with speech and text embeddings, improving the model context. To assess the efficacy of this quantized F0 embedding strategy, we conduct a comparative analysis against a baseline approach employing a 1D Convolutional
Neural Network (CNN). This baseline CNN directly processes
the raw F0 signal, utilizing a kernel size of 3, a stride of 1, and
256 channels. The CNN output is processed by a batch normalization layer followed by a ReLU activation function, and a linear projection layer that maps the output to a 512-dimensional
space. Finally, mean-pooling is applied across the time dimension to generate a fixed-length representation. This comparison
can be seen in Table 3.
For spectral refinement, we extract Mel filterbanks via
Kaldi-compatible torchaudio functions and process them
with _Consistent Ensemble Distillation (CED)_ [18]. CED distills
knowledge from large teacher models into lightweight yet highperformance student models. We employ the ‘CED-Small’ variant (22M parameters), balancing computational efficiency and
performance. The extracted spectral features are fine-tuned and
concatenated with the fused embeddings before being passed to
the MLP classifier, enriching the multimodal representation.


**3.4.** **SwiGLU Based MLP**


To further improve performance, we investigated the effect of
replacing the standard ReLU activation with a SwiGLU in the
MLP module. Inspired by [28], we replaced the default MLP
structure; consisting of a linear layer, ReLU activation, dropout,
and a final classification layer with a SwiGLU-based module.
The SwiGLU submodule comprises two linear layers and a
Swish [29] activation, followed by a final linear layer. Our empirical results demonstrate that this modification yields a slight
yet consistent performance improvement.


**4.** **Experimental Setup**


In this section, we describe the experimental setup and the
dataset utilized in our experiments, along with the data augmentation technique applied.
All experiments were trained using a batch size of 8 and
a Weighted Cross-Entropy Loss function, where class weights
were determined by the inverse frequency of each class within
the training set, for 20 epochs, using a cosine learning rate
scheduler with warm-up of 500 steps. The learning rate was
bounded between a minimum of 5e-5 and a maximum of 1e-5.
Optimization was performed using the AdamW [30] optimizer,
configured with the following parameters: _ϵ_ = 1e-8, _β_ = [0.9,



0.98] and a weight decay of 1e-6. Additionally, norm-based
gradient clipping, with a threshold of 10, was employed to stabilize training.


**4.1.** **The MSP Dataset**


The dataset used in this study is the MSP-Podcast corpus, a
repository of spontaneous and emotionally diverse speech segments collected from various podcast recordings. Unlike traditional speech emotion recognition (SER) datasets, which often
consist of acted emotional expressions, this corpus captures natural interactions, providing greater variability and authenticity.


**4.2.** **Data Augmentation**


We enhance generalization and mitigate overfitting using SeqAug [15], a modality-agnostic sequential data augmentation
technique applicable to our pre-extracted speech and text features. SeqAug permutes randomly selected feature dimensions
temporally, resampling from a distribution while preserving sequence integrity. During training, we apply SeqAug independently to each modality with 50% probability, consistently using a beta distribution ( _α_ = 0 _._ 5) for permutation. Unlike the
original, our approach employs independent permutations per
feature dimension, rather than a shared permutation to force
the model to learn representations robust to temporal misalignments between features, simulating asynchrony between modalities and improving feature importance extraction.


**5.** **Results and Discussion**


In this section, we analyze the performance of our systems,
evaluating different aspects of feature extraction and fusion
strategies. We report results for unimodal speech models, bimodal fusion with text, prosodic and spectral feature integration. Finally, we present the performance of the ensemble system, which represents our best configuration.
Performance was measured using the following metrics:
Macro and Micro F1-score, Recall (R), and Precision (P). For
brevity, we did not report accuracy since Micro F1 and accuracy
yielded identical values.


Table 1: _Performance metrics for unimodal speech models. Best_
_results are in bold, and the second-best results are underlined._

|SSL Model|Macro F1|Micro F1|R|P|
|---|---|---|---|---|
|W2V2 Large|0.178|0.394|0.198|0.172|
|HuBERT Large|0.274|0.478|0.279|0.276|
|WavLM Large|0.313|0.482|0.333|0.316|
|Whisper Large V3|**0.366**|**0.524**|**0.391**|**0.366**|
|XEUS|0.323|0.512|0.334|0.323|



Table 1 shows unimodal speech model performance.
Wav2Vec2 and HuBERT underperformed, likely due to pretraining on read speech. WavLM, XEUS, and Whisper performed better, with Whisper achieving the highest Macro F1
(0.366) and Micro F1 (0.524), likely benefiting from pretraining on diverse, spontaneous, and noisy speech.
Table 3 presents results for bimodal fusion (incorporating RoBERTa Large text features), comparing multiple fusion
strategies. Bimodal fusion significantly outperformed unimodal
models. MDAT, integrating GATs, achieved the highest Macro
F1 (0.401), highlighting the effectiveness of graph-based multimodal fusion. Surprisingly, the simple fusion strategy outperformed more complex techniques like Transformer-based fu

Table 2: _Comparison_ _of_ _the_ _performance_ _of_ _the_ _individual_ _models_ _selected_ _to_ _build_ _the_ _ensemble_ _and_ _the_ _overall_ _performance_ _of_ _the_
_ensemble_ _system._ _Best_ _results_ _are_ _in_ _bold,_ _and_ _the_ _second-best_ _results_ _are_ _underlined._ _”Batch_ _Bal”_ _refers_ _to_ _the_ _usage_ _of_ _balaned_
_sampling as in [31], ”Focal” refers to the usage of Focal Loss [32]._


|Model|Macro F1|Micro F1|R|P|
|---|---|---|---|---|
|Whisper + RoBERTa + MDAT + F0 Quant + SwiGLU + Data Aug<br>Whisper + RoBERTa + HCAM + F0 Quant + CED Spectral<br>Whisper + RoBERTa + HCAM + F0 Quant + CED Spectral + Data Aug + Focal<br>XEUS + E5 [33] + Transformers + Batch Bal + Data Aug + Focal|0.411<br>0.367<br>0.384<br>0.335|0.567<br>0.496<br>0.547<br>0.505|0.420<br>0.431<br>0.397<br>0.353|**0.446**<br>0.385<br>0.386<br>0.337|
|Ensemble (Majority Voting)|**0.422**|**0.581**|**0.437**|0.414|



Table 3: _Performance of various fusion strategies, prosodic and_
_spectral feature integration. Best results within each section are_
_in bold, and the second-best results are underlined._


**Strategy/Feature** **Macro F1** **Micro F1** **R** **P**
**Fusion Strategies**
Simple 0.388 0.557 0.404 0.383
Transformers 0.364 0.448 0.362 0.377
HCAM 0.383 0.556 0.391 0.396
MDAT **0.401** **0.582** **0.393** **0.455**
**Prosody Integration**
+ F0 0.397 **0.587** 0.398 0.435
+ Quant. F0 0.407 0.572 0.410 0.425
+ Data Aug. 0.400 0.586 0.400 0.436
+ SwiGLU **0.411** 0.567 **0.420** **0.446**
**Spectral Integration (CED)**

+ Random 0.342 0.583 0.332 **0.464**
+ Pretrained 0.376 0.578 0.366 0.403
+ Data Aug. 0.393 0.568 0.395 0.409
+ SwiGLU **0.405** **0.586** **0.396** 0.435


sion and HCAM. This may be due to increased susceptibility
to overfitting with the more complex models, given the limited
dataset size.

Integrating pretrained CED spectral features with prosodic
features, data augmentation, and SwiGLU yielded a Macro F1
of 0.405, demonstrating the value of incorporating learned spectral representations in addition to the prosodic information. The
best-performing CED and F0 configurations performed similarly (0.405 vs. 0.411), suggesting both feature types contribute
valuable, complementary information. Notably, a model employing randomly initialized CED features performed significantly worse (Macro F1: 0.342), highlighting the importance
of pre-training, which performed better (Macro F1: 0.376). A
SwiGLU-based MLP consistently improved performance, particularly when used alongside SeqAug, indicating its effectiveness in capturing temporal relationships.

Our speech emotion recognition ensemble was built using
an exhaustive search algorithm, exploring various model combinations. This exploration encompassed 13 variations of the
top-performing configuration. These variations experimented
with different fusion methods, the inclusion of data augmentation, the addition of prosodic and spectral features, and the integration of the second-best performing unimodal model (XEUS)
and an alternative text encoder (E5 Large V2). We also tested
using focal loss and balanced sampling. While E5 demonstrated
strong performance on standard text benchmarks, initial testing
revealed its lower effectiveness compared to RoBERTa Large
in this specific emotion recognition task. Ensemble candidates,
always including our best individual model, using at least three
models at a time.

Predictions were combined via majority voting, with our
top model breaking ties. To prevent overfitting, ensembles were



evaluated on 100 randomly sampled, class-balanced subsets of
the validation data. The size of each subset equalled the smallest
class sample size. The final ensemble was selected based on the
highest mean macro-F1 score across these subsets.
As presented in Table 2 our final ensemble achieved a
Macro F1-score of 0.422, representing an improvement over
individual configurations, including the best-performing single
model (Whisper with a Macro F1 of 0.366) and the most effective fusion strategy (MDAT, with a Macro F1 of 0.401 and 0.411
with the usage of data augmentation and SwiGLU). This significant increase indicates that the combination of diverse model
variations, along with complementary prosodic and spectral features, effectively boosted the system’s robustness and its ability
to generalize across class imbalances and subtle emotional expressions in spontaneous speech.


**6.** **Conclusion**


This work presented a multimodal system for speech emotion
recognition in naturalistic conditions, leveraging SSL-based
speech models, a text encoder, and prosodic and spectral features. Our evaluation of unimodal models demonstrated the
strong performance of Whisper and XEUS, highlighting their
robustness for SER in spontaneous speech.
Among fusion strategies, the Multimodal Dual Attention
Transformer (MDAT) achieved the best results, confirming the
effectiveness of graph-based attention. Additionally, the integration of quantized F0 embeddings significantly improved
Macro F1, reinforcing the importance of prosodic cues. Our final ensemble model reached a Macro F1-score of 0.422, demonstrating the advantages of combining multiple modalities and
advanced fusion techniques.
In future work, we plan to explore additional fusion strategies to further enhance cross-modal interactions and capture
nuanced emotional expressions. We also aim to refine our
data augmentation and ensemble selection methods, investigating end-to-end training frameworks that may reduce computational overhead while improving model interpretability and
generalization. Furthermore, validating our approach on larger,
more diverse datasets and incorporating domain adaptation
techniques will be critical to ensuring robustness across different speech contexts and application scenarios.


**7.** **Acknowledgements**


This work has been fully/partially funded by the project Research and Development of Algorithms for Construction of Digital Human Technological Components supported by Advanced
Knowledge Center in Immersive Technologies (AKCIT), with
financial resources from the PPI IoT/Manufatura 4.0 / PPI HardwareBR of the MCTI grant number 057/2023, signed with EMBRAPII/. We also thank the Artificial Intelligence Lab at Recod.ai, the Institute of Computing, University of Campinas.


**8.** **References**


[1] R. W. Picard, “Affective computing mit press,” _Cambridge, Mas-_
_sachsusetts_, p. 2, 1997.

[2] C. Busso, M. Bulut, C.-C. Lee, A. Kazemzadeh, E. Mower,
S. Kim, J. N. Chang, S. Lee, and S. S. Narayanan, “Iemocap:
Interactive emotional dyadic motion capture database,” _Language_
_resources and evaluation_, vol. 42, pp. 335–359, 2008.

[3] H.-C. Chou and C.-C. Lee, “Every rating matters: Joint learning
of subjective labels and individual annotators for speech emotion
classification,” in _ICASSP_ _2019_ _-_ _2019_ _IEEE_ _International_ _Con-_
_ference_ _on_ _Acoustics,_ _Speech_ _and_ _Signal_ _Processing_ _(ICASSP)_,
2019, pp. 5886–5890.

[4] E. Morais, R. Hoory, W. Zhu, I. Gat, M. Damasceno, and
H. Aronowitz, “Speech emotion recognition using self-supervised
features,” in _ICASSP_ _2022-2022_ _IEEE_ _International_ _Conference_
_on_ _Acoustics,_ _Speech_ _and_ _Signal_ _Processing_ _(ICASSP)_ . IEEE,
2022, pp. 6922–6926.

[5] R. Chakraborty, M. Pandharipande, and S. K. Kopparapu, _Analyz-_
_ing emotion in spontaneous speech_ . Springer, 2017.

[6] X. Cai, J. Yuan, R. Zheng, L. Huang, and K. Church, “Speech
emotion recognition with multi-task learning,” in _Interspeech_
_2021_, 2021, pp. 4508–4512.

[7] L. Goncalves and C. Busso, “Improving speech emotion recognition using self-supervised learning with domain-specific audiovisual tasks,” in _Interspeech 2022_, 2022, pp. 1168–1172.

[8] L. Goncalves, A. N. Salman, A. R. Naini, L. M. Velazquez,
T. Thebaud, L. P. Garcia, N. Dehak, B. Sisman, and C. Busso,
“Odyssey 2024-speech emotion recognition challenge: Dataset,
baseline framework, and results,” _Development_, vol. 10, no. 9,290,
pp. 4–54, 2024.

[9] A. Baevski, Y. Zhou, A. Mohamed, and M. Auli, “wav2vec
2.0: A framework for self-supervised learning of speech representations,” _Advances_ _in_ _neural_ _information_ _processing_ _systems_,
vol. 33, pp. 12 449–12 460, 2020.

[10] W.-N. Hsu, B. Bolte, Y.-H. H. Tsai, K. Lakhotia, R. Salakhutdinov, and A. Mohamed, “Hubert: Self-supervised speech representation learning by masked prediction of hidden units,” _IEEE/ACM_
_transactions on audio, speech, and language processing_, vol. 29,
pp. 3451–3460, 2021.

[11] S. Chen, C. Wang, Z. Chen, Y. Wu, S. Liu, Z. Chen, J. Li,
N. Kanda, T. Yoshioka, X. Xiao _et al._, “Wavlm: Large-scale selfsupervised pre-training for full stack speech processing,” _IEEE_
_Journal_ _of_ _Selected_ _Topics_ _in_ _Signal_ _Processing_, vol. 16, no. 6,
pp. 1505–1518, 2022.

[12] A. Radford, J. W. Kim, T. Xu, G. Brockman, C. McLeavey, and
I. Sutskever, “Robust speech recognition via large-scale weak
supervision,” in _International_ _conference_ _on_ _machine_ _learning_ .
PMLR, 2023, pp. 28 492–28 518.

[13] W. Chen, W. Zhang, Y. Peng, X. Li, J. Tian, J. Shi, X. Chang,
S. Maiti, K. Livescu, and S. Watanabe, “Towards robust speech
representation learning for thousands of languages,” in _Proceed-_
_ings_ _of_ _the_ _2024_ _Conference_ _on_ _Empirical_ _Methods_ _in_ _Natural_
_Language Processing_, 2024, pp. 10 205–10 224.

[14] L. Zhuang, L. Wayne, S. Ya, and Z. Jun, “A robustly optimized
BERT pre-training approach with post-training,” in _Proceedings_
_of_ _the_ _20th_ _Chinese_ _National_ _Conference_ _on_ _Computational_
_Linguistics_, S. Li, M. Sun, Y. Liu, H. Wu, K. Liu, W. Che,
S. He, and G. Rao, Eds. Huhhot, China: Chinese Information
Processing Society of China, Aug. 2021, pp. 1218–1227.

[Online]. Available: https://aclanthology.org/2021.ccl-1.108/

[15] E. Georgiou and A. Potamianos, “Seqaug: Sequential feature resampling as a modality agnostic augmentation method,” _arXiv_
_preprint arXiv:2305.01954_, 2023.

[16] M. Chen, H. Zhang, Y. Li, J. Luo, W. Wu, Z. Ma, P. Bell, C. Lai,
J. D. Reiss, L. Wang, P. C. Woodland, X. Chen, H. Phan, and
T. Hain, “1st place solution to odyssey emotion recognition challenge task1: Tackling class imbalance problem,” in _The_ _Speaker_
_and_ _Language_ _Recognition_ _Workshop_ _(Odyssey_ _2024)_, 2024, pp.
260–265.




[17] S. A. M. Zaidi, S. Latif, and J. Qadir, “Enhancing cross-language
multimodal emotion recognition with dual attention transformers,” _IEEE Open Journal of the Computer Society_, 2024.


[18] H. Dinkel, Y. Wang, Z. Yan, J. Zhang, and Y. Wang, “Ced: Consistent ensemble distillation for audio tagging,” in _ICASSP_ _2024_

_- 2024 IEEE International Conference on Acoustics,_ _Speech_ _and_
_Signal Processing (ICASSP)_, 2024, pp. 291–295.


[19] S. Dutta and S. Ganapathy, “Hcam–hierarchical cross attention model for multi-modal emotion recognition,” _arXiv preprint_
_arXiv:2304.06910_, 2023.


[20] P. Veliˇckovi´c, G. Cucurull, A. Casanova, A. Romero, P. Li`o, and
Y. Bengio, “Graph attention networks,” in _International_ _Confer-_
_ence on Learning Representations_, 2018.


[21] N. Shazeer, “Glu variants improve transformer,” _arXiv_ _preprint_
_arXiv:2002.05202_, 2020.


[22] S. Watanabe, T. Hori, S. Karita, T. Hayashi, J. Nishitoba, Y. Unno,
N. Enrique Yalta Soplin, J. Heymann, M. Wiesner, N. Chen,
A. Renduchintala, and T. Ochiai, “Espnet: End-to-end speech processing toolkit,” in _Proc. Interspeech_, 2018, pp. 2207–2211.

[23] K. C. Puvvada, P. Zelasko, [˙] H. Huang, O. Hrinchuk, N. R.
Koluguri, K. Dhawan, S. Majumdar, E. Rastorgueva, Z. Chen,
V. Lavrukhin, J. Balam, and B. Ginsburg, “Less is more: Accurate speech recognition & translation without web-scale data,” in
_Interspeech 2024_, 2024, pp. 3964–3968.


[24] M. Chen, H. Zhang, Y. Li, J. Luo, W. Wu, Z. Ma, P. Bell, C. Lai,
J. D. Reiss, L. Wang, P. C. Woodland, X. Chen, H. Phan, and
T. Hain, “1st place solution to odyssey emotion recognition challenge task1: Tackling class imbalance problem,” in _The_ _Speaker_
_and_ _Language_ _Recognition_ _Workshop_ _(Odyssey_ _2024)_, 2024, pp.
260–265.


[25] B. Stasiak and K. Rychlicki-Kicior, “Fundamental frequency extraction in speech emotion recognition,” in _Multimedia_ _Commu-_
_nications,_ _Services_ _and_ _Security_, A. Dziech and A. Czy˙zewski,
Eds. Berlin, Heidelberg: Springer Berlin Heidelberg, 2012, pp.
292–303.


[26] X. Wang, S. Takaki, and J. Yamagishi, “Autoregressive neural
f0 model for statistical parametric speech synthesis,” _IEEE/ACM_
_Transactions_ _on_ _Audio,_ _Speech,_ _and_ _Language_ _Processing_,
vol. 26, no. 8, pp. 1406–1419, 2018.


[27] H. Wei, X. Cao, T. Dan, and Y. Chen, “Rmvpe: A robust model
for vocal pitch estimation in polyphonic music,” in _Interspeech_
_2023_, 2023, pp. 5421–5425.


[28] I. Pacal, M. Alaftekin, and F. D. Zengul, “Enhancing skin cancer diagnosis using swin transformer with hybrid shifted windowbased multi-head self-attention and swiglu-based mlp,” _Journal of_
_Imaging Informatics in Medicine_, pp. 1–19, 2024.


[29] P. Ramachandran, B. Zoph, and Q. V. Le, “Searching
for activation functions,” 2018. [Online]. Available: https:
//openreview.net/forum?id=SkBYYyZRZ


[30] I. Loshchilov and F. Hutter, “Decoupled weight decay regularization,” in _International_ _Conference_ _on_ _Learn-_
_ing_ _Representations_, 2019. [Online]. Available: https:
//openreview.net/forum?id=Bkg6RiCqY7


[31] Q. Kong, Y. Cao, T. Iqbal, Y. Wang, W. Wang, and M. D. Plumbley, “Panns: Large-scale pretrained audio neural networks for
audio pattern recognition,” _IEEE/ACM_ _Transactions_ _on_ _Audio,_
_Speech, and Language Processing_, vol. 28, pp. 2880–2894, 2020.


[32] T.-Y. Lin, P. Goyal, R. Girshick, K. He, and P. Doll´ar, “Focal loss
for dense object detection,” in _2017_ _IEEE_ _International_ _Confer-_
_ence on Computer Vision (ICCV)_, 2017, pp. 2999–3007.


[33] L. Wang, N. Yang, X. Huang, L. Yang, R. Majumder, and F. Wei,
“Multilingual e5 text embeddings: A technical report,” _arXiv_
_preprint arXiv:2402.05672_, 2024.


