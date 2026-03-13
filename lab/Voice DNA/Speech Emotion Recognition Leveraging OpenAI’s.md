## Speech Emotion Recognition Leveraging OpenAI’s Whisper Representations and Attentive Pooling Methods

Ali Shendabadi [1], Parnia Izadirad [1], Mostafa Salehi [1*],
Mahmoud Bijankhan [2]


1Faculty of Intelligent Systems Engineering, University of Tehran,
N.Kargar, Tehran, Iran.
2Faculty of Literature and Humanities, University of Tehran, Enghelab,
Tehran, Iran.


*Corresponding author(s). E-mail(s): mostafa ~~s~~ alehi@ut.ac.ir;
Contributing authors: alishendabadi@ut.ac.ir; parniaizadirad@ut.ac.ir;

mbjkhan@ut.ac.ir;


**Abstract**


Speech Emotion Recognition (SER) research has faced limitations due to the
lack of standard and sufficiently large datasets. Recent studies have leveraged
pre-trained models to extract features for downstream tasks such as SER. This
work explores the capabilities of Whisper, a pre-trained ASR system, in speech
emotion recognition by proposing two attention-based pooling methods, Multihead Attentive Average Pooling and QKV Pooling, designed to efficiently reduce
the dimensionality of Whisper representations while preserving emotional features. We experiment on English and Persian, using the IEMOCAP and ShEMO
datasets respectively, with Whisper Tiny and Small. Our multi-head QKV architecture achieves state-of-the-art results on the ShEMO dataset, with a 2.47%
improvement in unweighted accuracy. We further compare the performance of
different Whisper encoder layers and find that intermediate layers often perform
better for SER on the Persian dataset, providing a lightweight and efficient alternative to much larger models such as HuBERT X-Large. Our findings highlight
the potential of Whisper as a representation extractor for SER and demonstrate
the effectiveness of attention-based pooling for dimension reduction.


**Keywords:** Speech Emotion Recognition, Whisper, Attentive Pooling, Attention
Mechanism


1


### **1 Introduction**

In recent years, human-computer interaction has entered a new phase. AI assistants such as ChatGPT have become an everyday tool for humans, raising the need
for machines to better understand humans and their needs. A significant factor in
achieving this is the capability of these systems to correctly detect human emotions
Nimmagadda et al. (2022). In spoken interactions, emotions are conveyed through the
tone of the utterance; more specifically, the manner in which the words are spoken and
their semantic meaning. The task of Speech Emotion Recognition (SER) is to detect
the emotions in an utterance using features extracted from the speech signal. An SER
system that better comprehends human emotions enables more appropriate responses
to users and helps anticipate their needs.






























|Multi-Head QKV Pooling<br>V<br>WV<br>Add and Norm<br>K<br>WK<br>Global Mean q Vector Wq|Col2|Col3|Col4|Col5|Col6|Col7|Col8|Col9|Col10|Col11|
|---|---|---|---|---|---|---|---|---|---|---|
|V<br>K<br>WK<br>WV<br>Wq<br>Global Mean<br>Add and Norm<br>**Multi-Head QKV Pooling**<br>q Vector|V<br>K<br>WK<br>WV<br>Wq<br>Global Mean<br>Add and Norm<br>**Multi-Head QKV Pooling**<br>q Vector|V<br>K<br>WK<br>WV<br>Wq<br>Global Mean<br>Add and Norm<br>**Multi-Head QKV Pooling**<br>q Vector|V<br>K<br>WK<br>WV<br>Wq<br>Global Mean<br>Add and Norm<br>**Multi-Head QKV Pooling**<br>q Vector|V<br>K<br>WK<br>WV<br>Wq<br>Global Mean<br>Add and Norm<br>**Multi-Head QKV Pooling**<br>q Vector|V<br>K<br>WK<br>WV<br>Wq<br>Global Mean<br>Add and Norm<br>**Multi-Head QKV Pooling**<br>q Vector|V<br>K<br>WK<br>WV<br>Wq<br>Global Mean<br>Add and Norm<br>**Multi-Head QKV Pooling**<br>q Vector|V<br>K<br>WK<br>WV<br>Wq<br>Global Mean<br>Add and Norm<br>**Multi-Head QKV Pooling**<br>q Vector|V<br>K<br>WK<br>WV<br>Wq<br>Global Mean<br>Add and Norm<br>**Multi-Head QKV Pooling**<br>q Vector|||
|V<br>K<br>WK<br>WV<br>Wq<br>Global Mean<br>Add and Norm<br>**Multi-Head QKV Pooling**<br>q Vector|V<br>K<br>WK<br>WV<br>Wq<br>Global Mean<br>Add and Norm<br>**Multi-Head QKV Pooling**<br>q Vector||||||||||
|V<br>K<br>WK<br>WV<br>Wq<br>Global Mean<br>Add and Norm<br>**Multi-Head QKV Pooling**<br>q Vector|||WV||||||||
|V<br>K<br>WK<br>WV<br>Wq<br>Global Mean<br>Add and Norm<br>**Multi-Head QKV Pooling**<br>q Vector|||||||||||
|V<br>K<br>WK<br>WV<br>Wq<br>Global Mean<br>Add and Norm<br>**Multi-Head QKV Pooling**<br>q Vector|Gl||||||||||
|V<br>K<br>WK<br>WV<br>Wq<br>Global Mean<br>Add and Norm<br>**Multi-Head QKV Pooling**<br>q Vector|Gl|ob|ob|ob|ob|ob|ob|ob|ob|ob|
||||||||||||
||||||||||||
||||||||||||


|Whisper processor<br>Whisper encoder<br>projector layer<br>Model Representation|Col2|Col3|Col4|Col5|Col6|Col7|
|---|---|---|---|---|---|---|
|Whisper processor<br>Whisper encoder<br>projector layer<br>**Model Representation**|||||||
|Whisper processor<br>Whisper encoder<br>projector layer<br>**Model Representation**|||||||
|Whisper processor<br>Whisper encoder<br>projector layer<br>**Model Representation**|||||||
|Whisper processor<br>Whisper encoder<br>projector layer<br>**Model Representation**|||||||



**Fig.** **1** : Demonstration of the Multi-head Attentive Average Pooling and Multi-head
QKV Pooling pipeline for SER. After extracting speech representations using Whisper
encoders, a multi-head pooling method is applied to reduce the dimensionality of the
representation matrix. The stacked rectangles represent attention heads. The outputs
from all attention heads are concatenated and subsequently projected through a weight
matrix _W_ _[o]_, producing a final 256-dimensional vector that serves as the input to the
classifier.


In recent studies, pre-trained models have been adapted for extracting features
as opposed to traditional features such as MFCC. These studies have achieved stateof-the-art results by fine-tuning pre-trained models on an SER corpus. Some other
studies treat the pre-trained model as an upstream model for feature extraction by


2


freezing all layers and building a downstream model for predicting emotions based on
the representations produced by the pre-trained model.
In this study, we use Whisper Radford et al. (2022), a pre-trained ASR model, for
feature extraction by freezing the encoder layers. We then apply a Dimension Reduction Module (DRM) for pooling a single vector from the representation matrix. We
propose two attention-based pooling methods: Attentive Pooling and QKV Pooling.
In Attentive Pooling, we initially follow the experiment carried out in Nasersharif and
Namvarpour (2024), where each frame is given a weight to assess its importance for
predicting the emotion in an utterance. We further extend this approach by applying it in a multi-head manner. In QKV Pooling, the query is conditioned on the
global average pooled from the initial representation of the pre-trained model. Our
results indicate that an attention-based pooling method can enable a smaller model
to compete with the results of larger models.
The main contributions of this research are as follows:


- Proposing QKV Pooling, an attention-based pooling method that extracts a single
vector from a high-dimensional representation matrix while minimizing information
loss. Additionally, we adapt Attentive Pooling on Whisper. Our results show that
Whisper Small with QKV achieves performance comparable to Whisper Large V3 on
both IEMOCAP and ShEMO, demonstrating a consistent and promising trade-off
between cost and accuracy.

- Exploring the effectiveness of the Whisper encoder as a representation extractor for
SER in Persian, a lower-resource language.

- Analyzing the different layers of the Whisper encoder and comparing their ability
to create effective speech representations.


Although other models achieve higher accuracy, as discussed in Section 4, our study
emphasizes that an effective pooling method can enable a smaller pre-trained model
to achieve results comparable to models that are hundreds of times larger. We release
all the codes at [https://github.com/alishendabadi/AttentivePoolingWhisperSER.](https://github.com/alishendabadi/AttentivePoolingWhisperSER)

### **2 Related Works and Background**


Early SER systems relied on traditional machine learning methods such as Hidden Markov Models (HMMs), Gaussian Mixture Models (GMMs), Support Vector
Machines (SVMs), and Decision Trees Pepino et al. (2021). In these methods,
researchers employed hand-crafted acoustic features like MFCCs, Linear Predictive
Cepstral Coefficients (LPCCs), energy, pitch, and speaking rate. While capable,
these approaches faced fundamental limitations in capturing the complexity and
individuality of human emotion Jin et al. (2025).
More recent studies have explored deep learning approaches and achieved good
experimental results. Recurrent Neural Networks (RNNs) and Long Short-Term Memory (LSTM) networks have been used to learn high-level feature representations by
processing speech signals sequentially Gupta et al. (2022). In DialogueRNN Majumder
et al. (2019), AGHMN Jiao et al. (2020), and HiGRU Jiao et al. (2019), researchers


3


used Gated Recurrent Units (GRUs) to capture temporal dependencies and contextual relationships in emotional speech. In other studies Zhao et al. (2019); Zhang et al.
(2019); Dutt and Gader (2023), Convolutional Neural Networks (CNNs) and RNNs
were combined to model and extract frequency and temporal features from emotional
speech, respectively.
Despite achieving significant results, these models still faced several challenges.
CNNs suffered from an inability to capture long-term dependencies due to their fixed
window sizes. RNNs, on the other hand, were prone to issues such as gradient vanishing
or exploding problems when processing lengthy sequences, which limited their overall
understanding of emotions. Additionally, combining CNN and RNN structures often
increased model complexity. This could lead to higher computational costs, more timeconsuming training, and an increased risk of overfitting, especially on small datasets.
In response to the above issues researchers have used Transformer models for modeling SER task. These self-attention based models are better equipped to process
lengthy input sequences and capture their global dependencies.
An ongoing problem throughout SER research has been the lack of standard
datasets. The available datasets are usually small and unbalanced. For this reason,
researchers have adopted transfer learning in their work, where pre-trained models are
used to learn meaningful representations applicable to downstream tasks. Pre-trained
models like Wav2Vec, HuBERT, and Whisper have significantly impacted various
downstream speech processing tasks, including SER, by providing rich, contextualized
speech representations. For example, Jiao et al. Jiao et al. (2024) used HuBERT features and log Mel-spectrograms in MFHCA, an SER method based on a Multi-Spatial
Fusion module (MF) and a Hierarchical Cooperative Attention module (HCA), to
identify emotion-related regions and integrate features. HuBERT was also used for
feature representation in DSTM Jin et al. (2025), a Transformer-based network with
dynamic-static feature fusion, using a locally adaptive multi-head attention module
(DTM) for dynamic local features and a global static attention module (STM) for
global features.
Although MFHCA and DSTM have achieved benchmark results using Hubert xlarge representations, the large number of parameters in this model remains a challenge
in handling high time and space complexity utilizing it. More recent pre-trained models are more robust in speech recognition. With these models researchers were able to
lower the computation cost without sacrificing accuracy. For example Qu et al. Qu
et al. (2024) developed SER-Whisper, a framework that integrates a frozen Whisper
encoder with specialized transformer-based classification layers, achieving high accuracy on the RAVDESS Livingstone and Russo (2018) dataset. Similarly, Sankaran et
al. Sankaran et al. (2024) and Ma et al Ma et al. (2024) compared Whisper-based
representations with other pre-trained models such as Wav2vec 2.0, WavLM Chen
et al. (2022) and data2vec Baevski et al. (2022) showing that Whisper consistently
outperforms alternatives in both audio abuse detection and SER tasks.
Further efforts have focused on adapting Whisper for emotion-related applications.
Chou et al. Chou (2024) proposed Whisper-SER, which leverages Whisper Tiny with a
lightweight adapter for multi-label SER. Their approach employed a two-stage training
strategy with weighted losses to mitigate conflicts between ASR and SER objectives.


4


However, they noted that Whisper Tiny exhibited higher word error rates (WER)
on emotional speech datasets like MSP-PODCAST compared to neutral utterances.
Feng et al. Feng and Narayanan (2024) extended Whisper’s role to SER data curation
by generating transcriptions and utilizing encoder outputs as representations. They
also explored the use of large language models (LLMs), including LLaMa 2, Falcon,
and Flan-T5 XXL, for emotion annotation and data augmentation. Although LLMs
struggled in zero-shot emotion annotation, combining multiple models and incorporating limited human feedback substantially improved annotation quality and SER
performance.
To efficiently process the high-dimensional outputs of pre-trained speech models,
dimension reduction has emerged as a critical technique for mitigating computational
costs and overfitting risks. Nasersharif et al. Nasersharif and Namvarpour (2024) a
DRM, which integrates attentive average pooling, maxout activation, and linear layers to extract relevant features while reducing dimensionality. This approach enables
dynamic selection of informative blocks and feature fusion via attention mechanisms,
thereby enhancing SER performance.
A parallel body of work has examined Wav2vec 2.0 for SER, with particular focus
on leveraging intermediate transformer block outputs. Studies have shown that early
blocks encode acoustic features, while later ones capture linguistic information. Pepino
et al. Pepino et al. (2021) proposed combining multiple Wav2vec 2.0 layers through
trainable weights, achieving superior SER performance and providing insights into
the relative contributions of different layers. Nasersharif et al. Nasersharif and Namvarpour (2024) worked on IEMOCAP and ShEMO Mohamad Nezami et al. (2019)
and demonstrated that intermediate layers outperform both initial and final ones for
emotion recognition.

### **3 Methodology**


This section describes the three main elements in our study: 1. A pre-trained model
that creates a representation from an audio sample. 2. A pooling method based on an
attention mechanism that limits the loss of important information during dimension
reduction. 3. A classifier which predicts the most likely emotion.


**3.1** **Model** **Representation**


In this study, we use Whisper features for representing audio samples. Whisper has
shown state-of-the-art performance in many speech-related tasks, including SER. We
also selected this model because of its multilingual capabilities, as we experiment on
both English and Persian. Here, we give a brief review of Whisper and then explain
the feature extraction process in detail.


**3.1.1** **Whisper**


Whisper is a weakly supervised multilingual and multitask speech recognition model
pre-trained on 680,000 hours of labeled audio data. Whisper uses an encoder-decoder
Transformer architecture. First, audio inputs are re-sampled to 16,000 Hz and an


5


80-channel log-Mel spectrogram of the audio segments is computed and globally normalized. These spectrograms are then passed through two convolution layers. The
encoder Transformer blocks then process the output of those convolutional layers
using sinusoidal positional embeddings. Finally, the decoder part converts the representations to a sequence of tokens using learned positional embeddings and tied
input-output representations.
What differentiates Whisper from other ASR models is its multilingual capabilities.
Whisper is trained on a massive amount of data, including 117,000 hours covering
96 languages. Additionally, the diversity of speech data used for pre-training makes
Whisper a robust model for low resource languages.
Whisper consists of three main parts; 1. two convolution layers which extract high
level representation of mel-spectrograms created from raw audio by the Whisper processor. The mel-spectrograms are computed over 25 ms windows with a stride of
10 ms. 2. Encoder transformer blocks which process the spectrogram representations
after adding positional embeddings. The encoder blocks use self-attention to create
a sequence of encoder-hidden states. 3. Decoder transformer blocks that predict the
next token using learned positional embeddings. The predictions are conditioned on
the encoder-hidden states using cross-attention from encoder blocks in addition to
previously predicted tokens using self-attention. The encoder and decoder blocks have
the same width and number of layers.


**3.1.2** **Feature** **Extraction**


For feature extraction, we use the encoder part of Whisper without updating its parameters. Utterances are first passed through the Whisper processor, which truncates each
sample to 30 seconds and creates a log Mel-spectrogram from the raw audio. The
Mel-spectrogram is processed by two convolutional layers using the GELU activation
function. After the convolution layers, sinusoidal positional embeddings are added to
the output. These embeddings can provide the model with information about the
position of the audio features in the sequence.


_X_ = Processor( **x** ( _t_ )) _,_ _X_ _∈_ R [80] _[×]_ [3000] (1)


Finally, these enhanced representations are passed through the encoder Transformer blocks to process the final output. The final representation is a matrix of 1500
vectors with a dimension based on the model size. To achieve unified dimensionality
for all whisper sizes a fully connected projector layer is applied. This layer maps the
encoder output to a fixed model dimension and then normalizes each representation.
In our experiments we set _dmodel_ to 256 thus in all scenarios a representation matrix
R [1500] _[×]_ [256] will be obtained for classification.


_H_ = Projector(WhisperEncoder( _X_ )) _,_ _H_ _∈_ R [1500] _[×]_ [256] (2)


**3.2** **Attentive** **Pooling**


To make the Whisper representation ready for classification, we need to convert it
into a one-dimensional vector, which causes some information loss. We propose two


6


methods for this transformation: Multi-head Attentive Average Pooling and Multihead QKV Pooling. In our experiments, QKV pooling generally outperforms Attentive
Average Pooling, except for Weighted Accuracy on IEMOCAP. Both methods are
included in this section to maintain coherence and organization of the paper.


_a_ = Pooling( _H_ ) _,_ _a ∈_ R [256] (3)
In equation 2, _H_ is the final model representation that was generated for each
sample, and _a_ is the final vector that goes through the classifier after pooling.


**3.2.1** **Multi-head** **Attentive** **Average** **Pooling**


In average pooling, all frames of an utterance have equal weight and therefore equal
effect on the emotion prediction. However, in many cases, certain frames within
an utterance contain more informative features for predicting emotion than others.
To give appropriate weight to each frame, we adapt attentive statistics pooling, an
attention-based pooling approach first introduced in Okabe et al. (2018). This mechanism is incorporated to assign importance to different frames within an utterance
by integrating statistics pooling and the attention mechanism, creating a more robust
speaker embedding.
Previous works Nasersharif and Namvarpour (2024); Okabe et al. (2018); Nazari
et al. (2025) have achieved significant results by applying attentive statistics pooling
for classification. In this study, we extend this approach by integrating a multi-head
attention mechanism to improve the scaling accuracy. Specifically, each attention head
is associated with a separate small neural network trained to compute the weights for
each frame.
As in Okabe et al. (2018) and Nasersharif and Namvarpour (2024), we describe
our attention network as mapping a value vector to an output, multiplying all of its
elements by an attention weight.


_et_ = _f_ ( **h** _tW_ 1 _[attn]_ + **b** ) **w** 2 _[attn]_ + _k_ (4)
, in which _W_ 1 _∈_ R _[d][model][×][d][hidden]_ and **w** 2 _∈_ R _[dhidden]_ . _f_ ( _._ ) is the hyperbolic tangent
activation function, and its output is passed through a dropout layer to prevent overfitting. Attention weights are calculated by being passed through a softmax function.
Instead of performing a single attention function with _dhidden_ -dimensional value vectors and attention weights, it is computed on a set of queries packed together as a _V_
matrix and attention weights packed together in the **e** vector.


Average Pooling( **e** _, V_ ) = Softmax          - **e** _[T]_ [ �] _V_ (5)
The _V_ matrix is also formed by mapping each vector in the representation matrix
to a vector of size _dhidden_ . All these vectors are grouped to form a _V_ matrix of size
R [1500] _[×][d][hidden]_ .


_V_ = _HW_ _[V]_ _,_ _W_ _[V]_ _∈_ R _[d][model][×][d][hidden]_ (6)
The process described above is done 4 times in a 4-head manner using different
sets of _W_ _[V]_ . Output vectors from each head are concatenated together and mapped
back to _dmodel_ to form the pooled vector _a_ .


7


Head _i_ = Average Pooling( **e** _i, Vi_ ) Concat(Head1 _, . . .,_ Head _n_ ) _W_ _[out]_ (7a)

**a** = MultiHead(Head1 _, . . .,_ Head _n_ ) _,_ **a** _∈_ R _[d][model]_ (7b)


,where _W_ _[out]_ _∈_ R [(#] _[heads.d][hidden]_ [)] _[×][d][model]_ and maps the dimension of the pooled
vector to _dmodel_


**3.2.2** **Multi-head** **QKV** **Attention** **Pooling**


In this method, we integrate a multi-head QKV attention mechanism to our pooling
approach to reduce information loss during dimension reduction. In the QKV attention
mechanism proposed by Vaswani et al. Vaswani (2017), the scaled dot product of _Q_
and _K_ is used to generate attention weights for each vector, with _Q_ derived from
previously generated tokens. In our classification task, however, no prior outputs are
available. To address this, we follow the pooling approach used in CLIP Radford et al.
(2021), conditioning the query on the global average-pooled representation of the audio
sample.




            - **q** _K_ _T_
QKV Attention( **q** _, K, V_ ) = Softmax ~~_√_~~
_dk_




_V_ (8a)



1
_µ_ ( _H_ ) =
1500



1500


**h** _i,_ _µ ∈_ R [256] (8b)

_i_ =1



Head _i_ = QKV Att( _µ_ ( _H_ ) _Wi_ _[Q][, HW][ K]_ _i_ _[, HW][ V]_ _i_ [)] (8c)


**3.2.3** **Classifier**


Following dimension reduction, the resulting pooled vector ( _a_ ), which is 256dimensional, is passed to a classification layer. The classifier head is a fully connected
layer with randomly initialized weights that maps the vector to a lower-dimensional
output based on the number of emotions in the dataset. For example, in IEMOCAP, four emotion classes are used: anger, happiness, sadness, and neutral. Using the
Softmax activation function, the most likely emotion is predicted.


Emotion = Softmax(FC( _a_ )) _,_ Emotion _∈_ R [4] (9)

### **4 Experiment and results**


**4.1** **Datasets**


**ShEMO**, or the Sharif Emotional Speech Database, contains 3 hours and 25 minutes
of online radio plays consisting of 3,000 utterances from 87 native Persian speakers.


8


Each utterance is labeled with one of six emotions, including anger, fear, happiness,
sadness, surprise, and neutral, where anger and neutral account for 70 percent of the
utterances, sadness 15 percent, and happiness and surprise together make up less than
15 percent. Fear, as the smallest class, is disregarded in line with previous work. The
utterances were divided into 10 groups, where each group consisted of unique speakers.


**IEMOCAP**, or the Interactive Emotional Dyadic Motion Capture dataset, is a widely
used benchmark in SER. It contains approximately 12 hours of dyadic audiovisual data
from 10 actors (five male - female pairs) recorded over five sessions. In line with prior
work, we restricted our analysis to improvised utterances annotated with four emotional categories: anger, happiness (excited and happy merged), sadness, and neutral.
All other emotion labels were excluded, resulting in a dataset of 2,793 utterances. For
evaluation, we employed five-fold cross-validation, where in each fold one session was
held out for testing and the remaining four sessions were used for training. This established methodology ensures that our results are directly comparable to other studies
using the IEMOCAP dataset.


**4.2** **Experimental** **Setup**


The models are implemented using the PyTorch framework, with pre-trained Whisper weights imported from Hugging Face. Both IEMOCAP and ShEMO datasets are
randomly split into batches of size 16 during both the training and testing phases.
Based on the dataset partitioning, we perform five-fold and ten-fold cross-validation
for IEMOCAP and ShEMO, respectively.
The hyperparameters are selected through a trial-and-error approach. All models
are trained for 30 epochs. For ShEMO, both pooling methods use 6 heads, each with
a hidden size of 4. For IEMOCAP, the number of heads is set to 12, with each head
having a hidden size of 4. The AdamW optimizer is employed to optimize the trainable weights, as it demonstrated strong performance in Nasersharif and Namvarpour
(2024). A cosine scheduler is used to adjust the learning rate, which peaks at 10e _−_ 4
with 10% warmup steps.


**4.3** **Results** **on** **Pooling** **Methods**


To ensure comparability with previous research in the speech emotion recognition
domain, two accuracy metrics, namely Weighted Accuracy and Unweighted Accuracy,
are selected for evaluation.
Unweighted Accuracy is defined as the average recall achieved for each class,
providing a more balanced performance measure, particularly for datasets such as
ShEMO, where testing is conducted on an unbalanced set.
The proposed classification framework is trained and tested using two different
Whisper model sizes as the representation extractor. Specifically, we utilized Whisper
Tiny and Whisper Small to compare the classification results.
In Section 3.2, we proposed two attention-based pooling methods. Table 1 presents
their results in comparison to Global Mean Pooling, which serves as the baseline.


9


**Table** **1** : Performance comparison of Multi-head Attentive Average Pooling (Attentive) and Multi-head QKV Pooling (QKV). Mean Average Pooling (Mean) serves as
the baseline model. Whisper Tiny and Whisper Small encoders were evaluated on the
ShEMO and IEMOCAP datasets for all three pooling methods. **WA** is for Weighted
Accuracy and **UA** is for Unweighted Accuracy.


**Size** **Pooling** **ShEMO** **IEMOCAP**


WA UA WA UA


Mean 84.12 _±_ 3.60 73.66 _±_ 3.87 68.22 _±_ 2.09 68.53 _±_ 2.35
Tiny Attentive 84.71 _±_ 4.59 74.71 _±_ 4.74 68.55 _±_ 1.79 68.67 _±_ 1.89
QKV **84.81** _±_ 3.64 **75.14** _±_ 4.24 **69.37** _±_ 1.84 **69.38** _±_ 1.98


Mean 88.81 _±_ 3.26 82.41 _±_ 4.02 70.52 _±_ 1.73 70.61 _±_ 2.39
Small Attentive 88.94 _±_ 2.11 82.86 _±_ 4.88 **71.98** _±_ 1.75 72.64 _±_ 2.22
QKV **89.19** _±_ 2.65 **83.07** _±_ 4.99 71.82 _±_ 0.22 **72.96** _±_ 2.22


Predictably, the attention-based pooling methods outperform simple averaging.
This is due to the fact that emotion features are not distributed evenly in an audio
sample, with some frames carrying more salient emotional cues than others. Methods
that leverage attention address this variability in feature extraction, unlike traditional
pooling methods.
QKV pooling achieves the highest accuracy on both ShEMO and IEMOCAP
datasets and consistently maintains superior results across different model sizes. However, the lower layers of the QKV-based model exhibit reduced accuracy, indicating
that its performance gains are primarily derived from higher-level representations
(Section 4.6).


**4.4** **Model** **Size** **Factor**


As shown in Table 1, the results indicate that the framework achieves superior classification performance when using representations extracted from the larger Whisper
model. This was predictable because the Small model also produces a lower word
error rate than the Tiny model in Whisper’s main task, ASR, thus it generates better
representations from the input speech.
Performance comparison of Whisper Tiny and Whisper Small encoders for Multihead Attentive Average Pooling (AttW) and Multi-head QKV Pooling (QKV)
methods on ShEMO. The radar chart shows that Whisper Small consistently outperforms Whisper Tiny, with particularly notable improvements in categories with fewer
samples.
The significant improvement in Unweighted Accuracy for ShEMO, which is a more
unbalanced dataset compared to IEMOCAP, suggests that the improved performance
of the larger Whisper model can be attributed to its enhanced ability to classify
the less frequent categories more effectively. As illustrated in Figure 2, the accuracy
improvements for the happy and sad categories are more pronounced compared to


10


Sad_AttW



Whisper Small

Whisper Tiny



|Angry_AttW|Neutral_AttW|
|---|---|
|Neutral_QKV<br>0|Angry_QKV<br><br>20<br>40<br>60<br>80<br>10|


Sad_QKV



Happy_QKV





**Fig.** **2** : Performance comparison of Whisper Tiny and Whisper Small encoders for
Multi-head Attentive Average Pooling (AttW) and Multi-head QKV Pooling (QKV)
methods on ShEMO. The radar chart shows that Whisper Small consistently outperforms Whisper Tiny, with particularly notable improvements in categories with fewer
samples


those for neutral and angry. This trend is also evident when examining the confusion
matrices in Figure 3.



































Happy Neutral Sad Angery
Predicted


(b) Whisper Small



















































































0.8


0.6


0.4


0.2


0.0



















0.8


0.6


0.4


0.2


0.0



Happy Neutral Sad Angery
Predicted


(a) Whisper Tiny



**Fig.** **3** : Confusion matrices of classifying ShEMO using different sizes of Whisper for
representation extraction.


11


**Table** **2** : Comparison of our main results with prior work on ShEMO and IEMOCAP
datasets. The best results are highlighted in **bold** .


**Dataset** **Base** **Model** **WA** **UA**



ShEMO


IEMOCAP



Wav2vec 2.0 Large Nasersharif and Namvarpour (2024) 86.80 80.60
HuBERT Large Ma et al. (2024) 83.35 64.29
WavLM Large Ma et al. (2024) 87.13 71.72
Data2vec 2.0 Large Ma et al. (2024) 82.68 64.09
Whisper Large V3 Ma et al. (2024) **89.55** 80.23
**Whisper** **Small** **(Ours)** 89.19 **83.07**


Whisper Large V3 Ma et al. (2024) 72.86 73.54
HuBERT Large Ma et al. (2024) 63.10 63.87
WavLM Large Ma et al. (2024) 69.07 69.47
Data2vec 2.0 Large Ma et al. (2024) 56.23 57.30
HuBERT X-Large Jin et al. (2025) 70.65 71.46
HuBERT X-Large Jiao et al. (2024) **74.24** **74.57**
**Whisper** **Small** **(Ours)** 71.98 72.96



**4.5** **Cost-accuracy** **Trade-off**


Obtained results on both datasets are comparable with the latest state-of-the-art
(SOTA) research, as shown in Table 2. To the best of our knowledge, the highest results
obtained on ShEMO are reported in EmoBox Ma et al. (2024), with Nasersharif et al.
Nasersharif and Namvarpour (2024) reporting a slightly higher Unweighted Accuracy.
Our proposed multihead QKV pooling method, however, achieves the best Unweighted
Accuracy using a smaller model, highlighting its effectiveness in balancing performance
and efficiency.
Although our results do not reach SOTA performance on IEMOCAP compared to
other work, we argue that our model requires substantially less computational cost.
The lower accuracy compared to the SOTA models can be justified by the significantly higher efficiency and lighter architecture of our approach. It must be noted
that the HuBERT X-Large model used in prior studies to extract representations contains approximately ten times more parameters than Whisper Small. Consequently, it
requires significantly more computational resources in both training and inference.
Overall, our findings indicate that efficient pooling mechanisms such as QKV
pooling can effectively close the gap between smaller and larger pre-trained models.
However, as we compared Whisper Tiny and Whisper Small in the previous section,
we illustrated the effect of model size on emotion detection. Therefore, we encourage adopting attention-based pooling methods on larger models to achieve further
performance improvements.


**4.6** **Different** **Whisper** **Encoder** **Layers** **for** **Representations**


According to Pepino et al. Pepino et al. (2021), different layers of pre-trained models
capture different types of information during training. While the last encoder layer is
generally best for producing representations for the main pre-training task, the middle
layers often contain more useful information for tasks such as SER.


12


1.4


1.2


1.0


0.8


0.6


0.4


0.2


0.0


100


90


80


70


60


50


40


30



|Col1|Col2|Col3|Col4|Col5|Vali<br>Trai|dation Loss<br>ning Loss|
|---|---|---|---|---|---|---|
||||||||
||||||||
||||||||
||||||||
||||||||
||||||||


0 5 10 15 20 25 30
Epoch


(a) Loss curve for layer 8


Validation Accuracy

|Col1|Trainin|g Accuracy|Col4|Col5|Col6|Col7|
|---|---|---|---|---|---|---|
||||||||
||||||||
||||||||
||||||||
||||||||



0 5 10 15 20 25 30
Epoch


(c) Accuracy curve for layer 8



|Col1|Col2|Col3|Col4|Col5|Vali<br>Trai|dation Loss<br>ning Loss|
|---|---|---|---|---|---|---|
||||||||
||||||||
||||||||
||||||||
||||||||
||||||||


0 5 10 15 20 25 30
Epoch


(b) Loss curve for layer 12


Validation Accuracy

|Col1|Col2|Col3|Col4|Col5|Training|Accuracy|
|---|---|---|---|---|---|---|
||||||||
||||||||
||||||||
||||||||
||||||||



0 5 10 15 20 25 30
Epoch


(d) Accuracy curve for layer 12



1.4


1.2


1.0


0.8


0.6


0.4


0.2


0.0


100


90


80


70


60


50


40


30



**Fig.** **4** : Comparing learning speed using different layers of whisper encoder as representation in ShEMO


Whisper, the pre-trained model used in this study, was trained in a multitask
setting to perform tasks including ASR, voice activity detection (VAD), language
detection, and speech translation. It was not explicitly trained for emotion detection
in speech. Moreover, in the multilingual model, different encoder layers may have
acquired different types of information depending on the input language.
Previous work has applied Whisper for speech classification and SER Ma et al.
(2024); Sankaran et al. (2025), but the experiments were limited to the model representations of the final layer. To the best of our knowledge, this is the first work to
investigate the model representations of each layer in depth. We study and report the
performance of all four layers of Whisper Tiny and all twelve layers of Whisper Small.
Models utilizing the final layer of Whisper reached their maximum learning potential much faster but also tended to overfit earlier. In contrast, models based on
intermediate and lower layers required more epochs to achieve their full potential.


13


This observation, shown in Figure 4, held consistently across both the IEMOCAP and
ShEMO datasets.
According to Figure 5, for the IEMOCAP dataset, in most cases, using the output of the last Whisper encoder layer yields the best performance. However, for the
ShEMO dataset, using the middle layers as speech representations yields better results.
Complete experimental results are presented in Appendix A.



|Mean|Col2|
|---|---|
|~~Attentive~~<br>QKV|~~Attentive~~<br>QKV|


Layer 1 Layer 4 Layer 8 Layer 12
Layers


(b) IEMOCAP



80


70


60


50


40


30


20


10


0



|Mean|Col2|
|---|---|
|~~Attentive~~<br>QKV|~~Attentive~~<br>QKV|


Layer 1 Layer 4 Layer 8 Layer 12
Layers


(a) ShEMO



70


60


50


40


30


20


10


0



**Fig.** **5** : Performance comparison of Mean Average Pooling (Mean), Multi-head Attentive Average Pooling (Attentive) and Multi-head QKV Pooling (QKV) when using 4
different layers of Whisper Small Encoders.

### **5 Discussion and Future Work**


In the projection stage, a substantial dimensionality reduction occurs. For instance,
in the small model, 768-dimensional vectors are reduced to 256 dimensions through
a fully connected layer with randomly initialized weights. Later, in the classification
stage, the 256-dimensional vector is mapped to a 4-dimensional output, again through
a fully connected layer with randomly initialized weights. This introduces a large
number of trainable parameters, for example, in the small model 197,632 weights are
solely dedicated to dimensionality reduction. Such parameters not only require random
initialization and training but also demand larger datasets than those available in our
experiments, while increasing model overhead. Therefore, employing more creative
and efficient methods for dimensionality reduction could potentially lead to higher
accuracy and better model optimization.
One promising direction is the integration of an ASR system to generate transcriptions from speech, using text as an additional modality for emotion recognition.
Given that the Whisper decoder inherently maps speech representations to text and
benefits from pretrained weights, it may eliminate the need for an additional embedding model such as BERT. In other words, the decoder produces intermediate vector
representations that can directly be exploited for emotion classification, avoiding


14


the computationally expensive two-step process of first generating text and then
embedding it again with a separate language model.
Another line of exploration is multimodal Emotion Recognition. For example,
datasets such as IEMOCAP or MELD Poria et al. (2018) contain not only speech but
also visual data. Leveraging facial gestures as an auxiliary modality could improve
recognition performance.
In this study, we focused solely on using the output of individual Whisper encoder
layers as standalone speech representations and compared their performance. Since
some layers exhibited only marginal differences in performance, it suggests that each
layer encodes useful but slightly distinct information for emotion classification. Consequently, designing an attention-based mechanism that aggregates information across
all encoder layers into a unified representation matrix may yield better results. However, this would increase model complexity and require more powerful hardware (e.g.,
graphical processing units with higher VRAM).
Compared with competing approaches that rely on models such as HuBERT XLarge (1B parameters) or Wav2Vec 2.0 (300M parameters) for SER on datasets like
IEMOCAP or ShEMO, the Whisper-small model with an encoder of only 88M parameters represents a lightweight yet effective alternative. Even when performance is
comparable, the use of Whisper-small offers a more efficient and practical solution.
Furthermore, our findings on ShEMO suggest that intermediate encoder layers of Whisper yield better performance than the final layers. This indicates that
intermediate-layer representations can serve as effective speech embeddings while
reducing computational cost, as the final layers need not be activated. This further
enhances the efficiency and practicality of Whisper-based SER systems.

### **6 Conclusion**


In this work, we explore the research gap for achieving a pooling method that prevents
the loss of valuable information from a speech representation. We chose Whisper for
its state-of-the-art performance and multilingual abilities to generate representations
from audio samples. The multilingual abilities of Whisper also allow us to contribute
to SER in Persian, as a low-resource language, as well as English, enabling us to
compare our results globally and with more studies. We use ShEMO and IEMOCAP
for Persian and English, respectively. After attaining the audio representations using
Whisper encoders, we applied a pooling method based on an attention mechanism. The
first method, Multi-head Attentive Average Pooling, extends existing attentive statistics pooling by integrating a multi-head attention mechanism to assign importance
weights to different frames within an utterance, considering that some frames contain
more informative features for emotion prediction than others. The second method,
Multi-head QKV Attention Pooling, utilizes a multi-head QKV (Query, Key, Value)
attention mechanism for pooling, but since the classification task lacks prior generated tokens usually required for the Query (Q), the approach conditions the Query
on the globally average-pooled representation of the audio sample. Our experiments
show that QKV achieves SOTA results on the Shemo dataset for unweighted accuracy, which is significant in an unbalanced dataset such as Shemo. Also, compared to


15


the SOTA for IEMOCAP, our method consumes less computational cost and appears
to be a good trade-off between accuracy and cost.


16


### **References**

Baevski A, Hsu WN, Xu Q, et al (2022) Data2vec: A general framework for selfsupervised learning in speech, vision and language. In: International conference on
machine learning, PMLR, pp 1298–1312


Chen S, Wang C, Chen Z, et al (2022) Wavlm: Large-scale self-supervised pre-training
for full stack speech processing. IEEE Journal of Selected Topics in Signal Processing
16(6):1505–1518


Chou HC (2024) A tiny whisper-ser: Unifying automatic speech recognition and multilabel speech emotion recognition tasks. In: 2024 Asia Pacific Signal and Information
Processing Association Annual Summit and Conference (APSIPA ASC), IEEE, pp
1–6


Dutt A, Gader P (2023) Wavelet multiresolution analysis based speech emotion recognition system using 1d cnn lstm networks. IEEE/ACM Transactions on Audio,
Speech, and Language Processing 31:2043–2054


Feng T, Narayanan S (2024) Foundation model assisted automatic speech emotion
recognition: Transcribing, annotating, and augmenting. In: ICASSP 2024-2024 IEEE
International Conference on Acoustics, Speech and Signal Processing (ICASSP),
IEEE, pp 12116–12120


Gupta V, Juyal S, Hu YC (2022) Understanding human emotions through speech spectrograms using deep neural network. the Journal of Supercomputing 78(5):6944–
6973


Jiao W, Yang H, King I, et al (2019) Higru: Hierarchical gated recurrent units for
utterance-level emotion recognition. arXiv preprint arXiv:190404446


Jiao W, Lyu M, King I (2020) Real-time emotion recognition via attention gated
hierarchical memory network. In: Proceedings of the AAAI conference on artificial
intelligence, pp 8002–8009


Jiao X, Wang L, Yu Y (2024) Mfhca: Enhancing speech emotion recognition
via multi-spatial fusion and hierarchical cooperative attention. arXiv preprint
arXiv:240413509


Jin G, Xu Y, Kang H, et al (2025) Dstm: A transformer-based model with dynamicstatic feature fusion in speech emotion recognition. Computer Speech & Language
90:101733


Livingstone SR, Russo FA (2018) The ryerson audio-visual database of emotional
speech and song (ravdess): A dynamic, multimodal set of facial and vocal expressions
in north american english. PloS one 13(5):e0196391


17


Ma Z, Chen M, Zhang H, et al (2024) Emobox: Multilingual multi-corpus speech
emotion recognition toolkit and benchmark. arXiv preprint arXiv:240607162


Majumder N, Poria S, Hazarika D, et al (2019) Dialoguernn: An attentive rnn for
emotion detection in conversations. In: Proceedings of the AAAI conference on
artificial intelligence, pp 6818–6825


Mohamad Nezami O, Jamshid Lou P, Karami M (2019) Shemo: a large-scale validated
database for persian speech emotion detection. Language Resources and Evaluation
53(1):1–16


Nasersharif B, Namvarpour M (2024) Exploring the potential of wav2vec 2.0 for speech
emotion recognition using classifier combination and attention-based feature fusion.
The Journal of Supercomputing 80(16):23667–23688


Nazari R, Salehi M, Shoeibi A (2025) An explainable connectome convolutional transformer for multimodal autism spectrum disorder classification. International Journal
of Neural Systems 35(8):2550043–2550043


Nimmagadda R, Arora K, Martin MV (2022) Emotion recognition models for
companion robots. The Journal of Supercomputing 78(11):13710–13727


Okabe K, Koshinaka T, Shinoda K (2018) Attentive statistics pooling for deep speaker
embedding. arXiv preprint arXiv:180310963


Pepino L, Riera P, Ferrer L (2021) Emotion recognition from speech using wav2vec
2.0 embeddings. arXiv preprint arXiv:210403502


Poria S, Hazarika D, Majumder N, et al (2018) Meld: A multimodal multi-party
dataset for emotion recognition in conversations. arXiv preprint arXiv:181002508


Qu X, Sun Z, Feng S, et al (2024) Breaking the silence: Whisper-driven emotion
recognition in ai mental support models. In: 2024 IEEE Conference on Artificial
Intelligence (CAI), IEEE, pp 290–291


Radford A, Kim JW, Hallacy C, et al (2021) Learning transferable visual models
from natural language supervision. In: International conference on machine learning,
PmLR, pp 8748–8763


Radford A, Kim JW, Xu T, et al (2022) Robust speech recognition via large-scale
weak supervision. URL [https://arxiv.org/abs/2212.04356,](https://arxiv.org/abs/2212.04356) [arXiv:2212.04356](https://arxiv.org/abs/2212.04356)


Sankaran AN, Farahbakhsh R, Crespi N (2024) Towards cross-lingual audio
abuse detection in low-resource settings with few-shot learning. arXiv preprint
arXiv:241201408


Sankaran AN, Farahbakhsh R, Crespi N (2025) Towards cross-lingual audio abuse
detection in low-resource settings with few-shot learning. In: 31st International


18


Conference on Computational Linguistics


Vaswani A (2017) Attention is all you need. Advances in Neural Information Processing
Systems


Zhang S, Zhao X, Tian Q (2019) Spontaneous speech emotion recognition using
multiscale deep convolutional lstm. IEEE Transactions on Affective Computing
13(2):680–688


Zhao J, Mao X, Chen L (2019) Speech emotion recognition using deep 1d & 2d cnn
lstm networks. Biomedical signal processing and control 47:312–323


19


### **Appendix A Results on Whisper Encoder Layers**

In Tables 3 and 4, we have included the Weighted and Unweighted Accuracy of each
transformer layer in the Whisper model. We experimented with Whisper Tiny and
Whisper Large, with 4 and 12 transformer blocks, respectively.


**Table 3** : Performance comparison of different pooling methods and layers for Whisper
Tiny model configurations on IEMOCAP and ShEMO datasets.


**IEMOCAP** **ShEMO**


**Layer** **WA** **UA** **F1** **WA** **UA** **F1**


**Whisper** **Tiny** **+** **Mean** **Pooling**


1 54.62 _±_ 2.27 55.40 _±_ 2.37 54.06 _±_ 2.23 70.94 _±_ 5.25 50.47 _±_ 2.87 67.08 _±_ 6.15
2 60.85 _±_ 1.30 61.76 _±_ 1.54 60.08 _±_ 1.65 80.88 _±_ 4.20 66.94 _±_ 4.82 79.54 _±_ 4.72
3 66.44 _±_ 1.93 66.92 _±_ 2.62 66.11 _±_ 2.07 83.26 _±_ 4.00 71.74 _±_ 3.78 82.48 _±_ 4.27
4 68.22 _±_ 2.09 68.53 _±_ 2.35 67.98 _±_ 2.13 84.12 _±_ 3.60 73.66 _±_ 3.87 83.47 _±_ 3.77


**Whisper** **Tiny** **+** **Attentive** **Average** **Pooling**


1 58.42 _±_ 2.46 58.88 _±_ 2.80 57.72 _±_ 2.89 78.35 _±_ 4.13 60.22 _±_ 6.33 76.42 _±_ 4.46
2 64.83 _±_ 1.84 64.84 _±_ 2.83 64.25 _±_ 2.11 80.33 _±_ 3.72 64.73 _±_ 6.21 78.98 _±_ 4.10
3 66.67 _±_ 1.44 67.47 _±_ 1.86 66.42 _±_ 1.66 84.71 _±_ 4.59 74.71 _±_ 4.74 84.29 _±_ 4.53
4 68.57 _±_ 2.17 68.69 _±_ 2.18 68.50 _±_ 2.42 83.09 _±_ 3.56 73.51 _±_ 3.48 82.78 _±_ 3.65


**Whisper** **Tiny** **+** **QKV** **Pooling**


1 54.74 _±_ 2.22 56.43 _±_ 0.92 53.45 _±_ 2.65 73.95 _±_ 5.65 52.78 _±_ 4.72 70.24 _±_ 6.25
2 61.80 _±_ 1.60 62.51 _±_ 2.56 61.22 _±_ 1.97 79.89 _±_ 4.39 63.67 _±_ 6.01 78.06 _±_ 5.19
3 66.94 _±_ 1.41 67.88 _±_ 1.77 66.58 _±_ 1.79 84.81 _±_ 3.64 74.90 _±_ 4.48 84.26 _±_ 4.06
4 69.37 _±_ 1.84 69.38 _±_ 1.98 69.31 _±_ 1.91 83.32 _±_ 3.86 75.14 _±_ 4.24 82.97 _±_ 3.88


20


**Table 4** : Performance comparison of different pooling methods and layers for Whisper
Small model configurations on IEMOCAP and ShEMO datasets.


**IEMOCAP** **ShEMO**


**Layer** **WA** **UA** **F1** **WA** **UA** **F1**


**Whisper** **Small** **+** **Mean** **Pooling**


1 55.58 _±_ 1.30 55.54 _±_ 2.06 55.29 _±_ 1.37 73.20 _±_ 6.78 51.97 _±_ 6.86 69.41 _±_ 7.98
2 58.42 _±_ 1.64 59.90 _±_ 2.58 57.79 _±_ 1.86 77.15 _±_ 5.99 58.08 _±_ 4.33 74.57 _±_ 6.66
3 59.88 _±_ 1.64 59.94 _±_ 1.65 59.27 _±_ 2.21 79.54 _±_ 5.51 62.41 _±_ 7.58 77.35 _±_ 6.51
4 62.43 _±_ 1.81 63.43 _±_ 1.76 61.93 _±_ 2.27 82.53 _±_ 4.55 69.48 _±_ 4.44 81.43 _±_ 5.13
5 66.68 _±_ 1.26 67.48 _±_ 2.49 66.42 _±_ 1.18 85.20 _±_ 3.96 76.03 _±_ 4.16 84.71 _±_ 4.23
6 67.77 _±_ 1.65 67.42 _±_ 2.52 67.78 _±_ 1.69 85.89 _±_ 3.37 77.30 _±_ 3.32 85.65 _±_ 3.44
7 68.27 _±_ 1.48 67.95 _±_ 1.83 67.99 _±_ 1.70 88.19 _±_ 2.46 79.84 _±_ 4.58 87.84 _±_ 2.53
8 69.99 _±_ 1.26 70.24 _±_ 1.84 69.88 _±_ 1.26 88.81 _±_ 3.26 82.41 _±_ 4.02 88.59 _±_ 3.25
9 70.05 _±_ 1.79 70.16 _±_ 2.37 69.94 _±_ 1.95 87.41 _±_ 3.76 78.40 _±_ 7.80 87.15 _±_ 3.86
10 70.52 _±_ 1.73 70.61 _±_ 2.39 70.43 _±_ 1.76 87.07 _±_ 3.52 77.92 _±_ 7.15 86.64 _±_ 3.73
11 70.65 _±_ 1.35 70.66 _±_ 2.35 70.56 _±_ 1.45 86.65 _±_ 3.35 77.55 _±_ 5.86 86.22 _±_ 3.47
12 70.69 _±_ 1.58 70.78 _±_ 2.37 70.62 _±_ 1.05 87.61 _±_ 3.15 81.65 _±_ 5.71 87.56 _±_ 3.09


**Whisper** **Small** **+** **Attentive** **Average** **Pooling**


1 59.07 _±_ 2.73 60.47 _±_ 1.83 58.13 _±_ 3.44 73.15 _±_ 6.61 52.13 _±_ 5.49 69.62 _±_ 7.42
2 61.75 _±_ 1.49 62.54 _±_ 2.11 61.36 _±_ 1.64 77.55 _±_ 5.87 58.66 _±_ 5.28 74.71 _±_ 6.70
3 63.23 _±_ 1.51 64.32 _±_ 1.52 62.48 _±_ 2.26 80.69 _±_ 4.96 65.48 _±_ 4.18 78.87 _±_ 5.84
4 64.96 _±_ 1.48 65.03 _±_ 2.89 64.51 _±_ 1.57 83.18 _±_ 4.77 74.19 _±_ 3.58 82.80 _±_ 4.80
5 66.83 _±_ 0.87 67.70 _±_ 1.44 66.61 _±_ 0.82 85.19 _±_ 3.40 76.50 _±_ 4.61 84.84 _±_ 3.54
6 67.51 _±_ 2.22 67.46 _±_ 2.06 67.53 _±_ 2.53 85.98 _±_ 2.67 78.02 _±_ 5.47 85.75 _±_ 2.86
7 69.36 _±_ 2.09 70.81 _±_ 2.63 69.28 _±_ 2.14 88.31 _±_ 2.74 81.89 _±_ 3.18 88.12 _±_ 2.78
8 68.79 _±_ 1.97 68.70 _±_ 2.25 68.66 _±_ 1.94 88.94 _±_ 2.11 82.86 _±_ 4.88 88.79 _±_ 2.18
9 68.29 _±_ 2.26 68.79 _±_ 2.49 68.05 _±_ 2.23 88.63 _±_ 3.16 82.55 _±_ 5.21 88.44 _±_ 3.20
10 69.35 _±_ 2.43 69.68 _±_ 2.84 69.21 _±_ 2.45 87.02 _±_ 2.96 79.17 _±_ 5.44 86.59 _±_ 3.37
11 71.50 _±_ 3.09 71.11 _±_ 3.09 71.47 _±_ 3.14 88.19 _±_ 2.66 80.22 _±_ 6.32 88.02 _±_ 2.73
12 71.98 _±_ 1.75 72.64 _±_ 2.22 71.89 _±_ 1.64 86.71 _±_ 2.71 79.75 _±_ 3.60 86.44 _±_ 2.66


**Whisper** **Small** **+** **QKV** **Pooling**


1 55.85 _±_ 1.77 57.82 _±_ 2.13 54.81 _±_ 2.05 73.06 _±_ 6.32 50.59 _±_ 5.55 68.90 _±_ 6.77
2 58.15 _±_ 2.00 59.89 _±_ 2.89 57.61 _±_ 2.23 76.91 _±_ 6.11 57.21 _±_ 4.31 73.91 _±_ 7.07
3 60.37 _±_ 1.75 62.17 _±_ 2.64 59.72 _±_ 2.21 78.80 _±_ 5.89 61.67 _±_ 5.86 76.58 _±_ 7.21
4 62.86 _±_ 1.58 64.40 _±_ 1.92 62.52 _±_ 1.89 82.43 _±_ 5.26 68.67 _±_ 6.71 81.07 _±_ 5.98
5 66.31 _±_ 0.91 67.87 _±_ 2.19 65.84 _±_ 1.01 85.24 _±_ 4.34 75.83 _±_ 5.98 84.95 _±_ 4.43
6 67.90 _±_ 2.29 68.20 _±_ 2.86 67.90 _±_ 2.37 85.84 _±_ 3.80 78.17 _±_ 4.53 85.61 _±_ 3.93
7 69.46 _±_ 1.46 69.23 _±_ 2.23 69.30 _±_ 1.47 88.16 _±_ 2.88 81.78 _±_ 3.04 88.01 _±_ 2.83
8 70.15 _±_ 1.42 70.55 _±_ 2.06 69.95 _±_ 1.45 89.19 _±_ 2.65 83.07 _±_ 4.99 89.04 _±_ 2.62
9 70.66 _±_ 1.34 70.70 _±_ 1.70 70.67 _±_ 1.36 88.45 _±_ 3.47 82.75 _±_ 4.70 88.35 _±_ 3.47
10 71.83 _±_ 1.44 72.04 _±_ 1.19 71.74 _±_ 1.45 88.55 _±_ 3.29 82.85 _±_ 3.07 88.40 _±_ 3.27
11 71.79 _±_ 2.20 72.96 _±_ 2.22 71.50 _±_ 2.25 88.02 _±_ 3.13 78.76 _±_ 6.90 87.63 _±_ 3.32
12 71.04 _±_ 1.61 71.51 _±_ 1.93 70.96 _±_ 1.46 87.34 _±_ 2.43 81.44 _±_ 3.42 87.17 _±_ 2.38


21


