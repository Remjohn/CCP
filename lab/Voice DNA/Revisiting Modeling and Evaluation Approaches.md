# `國 立 清 華 大 學` `博 士 論 文`

## `重新探討語音情緒辨識的建模與評量方法：` `考慮標註者的主觀性與情緒的模糊性` Revisiting Modeling and Evaluation Approaches

#### 系所別：電機工程學系博士班 組別 : 系統 A 學號姓名： 104061701 周惶振 (Huang-Cheng Chou) 指導教授：李祈均 博士 (Prof. Chi-Chun Lee) `中 華 民 國 一一三 年 七 月`


#### `摘要`

```
 語音情緒辨識在過去二十年裡獲得了越來越多的關注。建立語音情緒識別系

統需要情緒數據庫，資料庫需要有人聲以及人類的情緒感受標記。研究人員們

會訓練群眾標記者或內部標記者，在收聽或觀看情緒錄像後，通過選擇預先定

義的情緒類別來描述和提供他們的情緒感知。然而，當研究人員們要求標記者

們從預定義的情緒中選擇情緒時，觀察到標記者之間出現分歧是很常見的。為

了處理這種標記者之間的分歧，大部分專家學者們將分歧視為雜訊，並使用標

籤聚合方法來獲得單一的共識情緒標記，作為訓練語音情緒識別系統的學習目

標。雖然這種通行做法將任務簡化為單一情緒標籤識別任務，但這個方法忽略

了人類情緒感知的自然行為。在本論文中，我們主張應重新檢視語音情感識別

語音情緒辨識中的建模與評估方法。本博士論文探討了構建語音情緒識別系統

的三個層面的新穎觀點。首先，我們接受情緒感受的主觀性，並考慮標記者的

所有情緒標記。傳統的方法只允許每位標記者對每個樣本給予一票情緒標記，

```

`但我們藉由考慮所有標記者的所有標記，利用現有的軟標籤方法` (soft-label) `重新`

```
計算標籤表示方式。此外，我們直接利用個別標記者的情緒標記來訓練個別標

記者的語音情緒識別系統，並聯合訓練個別標記者語音情緒識別系統和標準語

```

`音情緒識別系統` ( `使用共識標籤` ) `。在使用多數決所獲得的共識標籤當作最終情緒`

```
標籤進行測試時，個別標記者的建模方法提升了語音情緒辨識系統的性能。

 其次，我們重新思考了評估語音情緒辨識系統的方法以及語音情緒辨識任

務的制定和定義。我們主張在評估語音情緒辨識系統的性能時，不應該刪除任

```

I


```
何數據和情緒標記。此外，我們認為語音情緒辨識任務的定義可以包含情緒的

共現性（例如，悲傷和生氣）。因此，樣本的真實標籤不應該是單一情緒標

籤，而應該是包含更多情緒感知多樣性的分佈式標籤。我們提出了一種新的標

```

`籤聚合規則，稱為「全包容規則」` (all-inclusive rule) `，用於選擇訓練集和測試集`

```
的數據和其情緒標記。對四個公開英文情緒數據庫的結果表明，使用「全包容

規則」方法決定的訓練集所訓練的語音情緒辨識系統，在各種測試條件下，其

性能優於使用傳統方法，包括絕對多數決和相對多數決訓練的語音情緒辨識系

統。

 最後但同樣重要的是，我們受到心理學研究關於情緒共現性的發現啟發。我

們根據情緒資料庫訓練集中情緒標記來估計情緒共現性的頻率，並基於每種情

```

II


#### `致謝`

```
 我要向那些在我博士旅程中支持和指導我的人表達我真誠感謝。我的指導教

```

`授，李祈均博士，從大學專題開始指導我，從` 2014 `年到` 2024 `年，老師的專業知`

```
識、寶貴的見解和不懈的支持對這篇博士論文有著非常大的貢獻。祈均老師的

指導和支持讓我可以順利完成這篇博士論文以及旅程。

 我也向我的博士學位考試委員會的委員們，林嘉文教授、馬席彬教授、陳

柏琳教授、冀泰石教授，以及王新民博士，感謝各位委員們抽空參與，並提

供建設性的回饋與建議，以及投入時間審閱我的博士論文。也謝謝指導過我

```

`的` Carlos Busso `教授、李宏毅教授、劉奕汶教授、` Albert Ali Salah `教授、阮大成博`


`士，和` Alexander Visheratin `博士，他們不僅是合作者，還是我的指導員；有他們`

```
心研究而無財務之憂。

```

`我` `也` `感` `謝` ACII 2017 `和` `國` `際` `口` `語` `溝` `通` `學` `會` `獎` `勵` `（` INTERSPEECH 2022 `），`

```
讓 我 能 夠 在國 際 會 議 上 親 自 到 現 場 介 紹 我 們 的 研 究 ， 這 些 機 會 提 供

了 寶 貴 的 經 驗 和 新 的 視角 。 同 時 ， 能 夠 在 享 有 盛 譽 的 期 刊 上 發 表 我

```

`的研究成果，包括` APSIPA `《` Transactions on Signal and Information Processing `》`


`及` IEEE `《` Transactions on Affective Computing `》期刊，也是一個非常有價值的經`


`歷，也謝謝` ISCA Student Advisory Committee `，讓我可以成為委員，為國際會議`

```
貢獻，也讓我認識到非常多來自世界各地和各領域的專家和學者們。

 在此，我想向我的家人們、所有實驗室的夥伴們、朋友們（林維誠、陳思

```

`睿、` Seong-Gyun Leem `、` Lucas Goncalves `、吳姿瑩、` Ali N. Salman `、張凱為、林`


III


`羿成、吳海濱、任文澤、` Andrea Vidal `、許德丞、陳志杰和林旻萱）和人生中的`


`教練和老師們` ( `徐碩鴻老師、林靜枝老師、曹昱博士、張俊盛教授、徐桂平老`

```
師、吳德成教練、黃錫瑜教授、陳榮順老師、劉素貌教練、黃老師、蔡文祺老

```

`師、范光榮老師、楊硯茗教練、` Richard Lee `老闆、洪光燦教練、張炳煌教練和`


`王禮章老師` ) `表示感謝，感謝他們無微不至的支持和鼓勵。他們的耐心和理解讓`

```
這段旅程變得可承受且充實。感謝你們成為這段旅程的一部分。

```

IV


#### **Abstract**

Over the past twenty years, there has been a growing focus on speech emotion recog

nition (SER). To develop SER systems capable of identifying emotions in speech, re

searchers need to gather emotional databases for training purposes. This process in

volves training crowdsourced raters or in-house annotators to express their emotional


responses after experiencing emotional recordings by selecting from a set list of emo

tions. Nevertheless, it is common for raters to disagree on emotion selection from these


predefined categories. To address this issue, many researchers consider such disagree

ments noise and apply label aggregation techniques to produce a unified consensus la

bel, which serves as the target for training SER systems. While the common practice


Based on the findings of psychological studies, emotion perception is subjective.


Each individual could have varying responses to the same emotional stimulus. Ad

ditionally, boundaries of emotions in human perception are overlapped, blended, and


ambiguous. Those ambiguities of emotions and subjectivity of emotion perceptions in

spire us to revisit modeling and evaluation approaches in SER. This dissertation explores


novel perspectives on three main views of building SER systems. First, we embrace the


subjectivity of emotional perception and consider every emotional rating from annota

tors. Also, the conventional approach only allows each rater to provide one vote for


each sample. Still, we re-calculate label representation in the distributional format with


the existing soft-label method by considering all ratings from all raters. Moreover, we


V


directly utilize ratings of individual annotators to train SER systems and jointly train the


individual SER systems and the standard SER systems. The modeling of individual an

notators improves the performances of SER systems on the test sets with the consensus


labels obtained by the majority vote.


Secondly, we rethink the determination of methods to evaluate SER systems and the


formulation and definition of the SER task. We argue that we should not remove any


data and emotional ratings when assessing the performances of SER systems. Also,


we think the definition of SER task can have a co-occurrence of emotions (e.g., sad


and angry). Therefore, the ground truth of samples should not be the one-hot single


label, and it can be distributional to include more diversity of emotion perception. We


gether, using emotional ratings from the training data of emotion databases. This matrix


is then normalized, considering the frequency of each emotion class. We derive a pe

nalization matrix by subtracting the normalized matrix from an identity matrix. We aim


to apply penalties to SER systems during training when they predict rarely occurring


combinations of emotions. This penalization matrix is integrated into objective func

tions like cross-entropy loss. The findings from the largest English emotion database


indicate that using the penalization matrix enhances the performance of SER systems,


even under single-label testing conditions.


With the extensive results, we conclude that (1) we should involve the minority of


emotional ratings instead of removing them to build better-performance SER systems,


VI


(2) we should consider emotional ratings from more people instead of fewer people


during training SER systems to get better-performance SER systems; (3) we should al

low SER systems to predict multiple emotions to handle the possibility of co-occurring


emotions in the real-life scenarios. In future work, we plan to investigate training emo

tion recognition systems with multi-modalities (e.g., video, text, and audio) to process


signals to improve the performance of SER systems. Also, we are interested in the re

lationship between the number of training human-labeled data and the performances of


SER systems. Furthermore, we aim to understand the performance bias in the demo

graphic groups, such as gender, race, and age. Last but not least, we plan to build a


multi-lingual emotion recognition system.


VII


#### **Acknowledgements**

I am deeply grateful to everyone who has supported and guided me during my Ph.D.


journey. I extend special thanks to my advisor, Professor Chi-Chun Lee, who has been a


guiding force since my undergraduate years, from 2014 to 2024. Professor Lee’s exper

tise, invaluable insights, and unwavering support have been instrumental in completing


this doctoral dissertation. His guidance has played a crucial role in the successful con

clusion of my dissertation and my entire Ph.D. journey.


I am also profoundly grateful to the members of my dissertation committee, Pro

fessor Chia-Wen Lin, Professor Hsi-Pin Ma, Professor Berlin Chen, Professor Tai-Shih


Chi, and Dr. Hsin-Min Wang. Thank you all for taking the time to participate, provid

and the Association for Computational Linguistics and Chinese Language Processing


for the generous funding and resources provided during my research. With their finan

cial support, this work was possible. I acknowledge the scholarships I received from


the NOVATEK Fellowship and the National Science and Technology Council Ph.D.


Students Study Abroad Program, Google East Asia Student Travel Grants, The Rotary


Foundation Excellence Scholarship, and National Tsing Hua University Dean Ph.D.


Student Excellence Scholarship: These scholarships allowed me to concentrate fully on


my research without financial worry.


I am also thankful for the opportunities to present my work at international con

ferences, such as the ACII 2017 and International Speech Communication Association


VIII


Grants (INTERSPEECH 2022), which provided valuable feedback and new perspec

tives. Publishing my work in esteemed journals, including APSIPA Transactions on


Signal and Information Processing and IEEE Transactions on Affective Computing, has


also been an enriching experience.


I want to express my gratitude to my family, my lab-mates (BIICers), and friends


(Wei-Cheng Lin, Szu-Jui Chen, Seong-Gyun Leem, Lucas Goncalves, Tz-Ying Wu,


Ali N. Salman, Kai-Wei Chang, Yi-Cheng Lin, Haibin Wu, Wenze Ren, Andrea Vidal,


Te-Cheng Hsu, Jhih-Jie Chen, and Min-Hsuan Lin), and the coaches and teachers in


my life (Professor Shawn S. H. Hsu, Teacher Ching-Chin Lin, Dr. Yu Tsao, Professor


Jason S. Chang, Teacher Kuei-Ping Hsu, Coach Te-Cheng Wu, Professor Shi-Yu Huang,


IX


# **Contents**

**Abstract (Chinese)** **I**


**Acknowledgements (Chinese)** **III**


**1** **Introduction** **1**


1.1 Motivation . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 1


1.2 Background, Related Works, and Challenges . . . . . . . . . . . . . . . 4


1.2.1 Emotion Representations . . . . . . . . . . . . . . . . . . . . . 4


1.2.2 Emotion Recognition Systems using Multi-/Uni-modality . . . 4


1.2.3 Evaluation of SER Systems . . . . . . . . . . . . . . . . . . . 5


1.2.4 Label Prepossessing for Training SER Systems . . . . . . . . . 6


1.2.5 Co-occurrence of Emotions . . . . . . . . . . . . . . . . . . . 7


1.2.6 Disagreement between Raters on the Emotion Datasets . . . . . 8


1.3 Contributions . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 9


X


1.3.1 Every Rating Matters Considering the Subjectivity of Annotators 10


1.3.2 Novel Evaluation Method by an All-Inclusive Aggregation Rule 10


1.3.3 Training Loss Using Co-occurrence Frequency of Emotions . . 11


1.4 Outline of the Dissertation . . . . . . . . . . . . . . . . . . . . . . . . 11


**2** **Emotion Databases** **12**


2.1 IEMOCAP . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 12


2.2 IMPROV . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 13


2.3 CREMA-D . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 13


2.4 MSP-PODCAST . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 14


2.5 Standard Partition . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 15


3.2.1 Subjectivity of Emotion Perception . . . . . . . . . . . . . . . 18


3.2.2 Mixture of Annotators . . . . . . . . . . . . . . . . . . . . . . 18


3.2.3 Soft-label Training Method for SER Systems . . . . . . . . . . 19


3.3 Resource and Task Formulation . . . . . . . . . . . . . . . . . . . . . 19


3.4 Speech Emotion Classifier . . . . . . . . . . . . . . . . . . . . . . . . 20


3.4.1 Input Features . . . . . . . . . . . . . . . . . . . . . . . . . . . 20


3.4.2 Model Structure . . . . . . . . . . . . . . . . . . . . . . . . . 21


3.4.3 Training Labels . . . . . . . . . . . . . . . . . . . . . . . . . . 21


3.5 Proposed Method . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 22


3.5.1 Rater-Modeling . . . . . . . . . . . . . . . . . . . . . . . . . . 22


XI


3.5.2 Final Concatenation Layer . . . . . . . . . . . . . . . . . . . . 23


3.6 Experimental Setup . . . . . . . . . . . . . . . . . . . . . . . . . . . . 23


3.6.1 Foundational Component . . . . . . . . . . . . . . . . . . . . . 23


3.6.2 All Model Comparison . . . . . . . . . . . . . . . . . . . . . . 24


3.7 Other Training Details . . . . . . . . . . . . . . . . . . . . . . . . . . 25


3.8 Experimental Results and Analyses . . . . . . . . . . . . . . . . . . . . 26


3.9 Summary . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 27


**4** **Novel Evaluation Method by an All-Inclusive Aggregation Rule** **28**


4.1 Motivation and Background . . . . . . . . . . . . . . . . . . . . . . . 29


4.2 Previous Literature . . . . . . . . . . . . . . . . . . . . . . . . . . . . 31


4.4.1 Resource . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 35


4.4.2 Speech Emotion Classifier . . . . . . . . . . . . . . . . . . . . 35


4.4.3 Train/Test Set Defined by Aggregation Rules . . . . . . . . . . 37


4.4.4 Label Learning for SER . . . . . . . . . . . . . . . . . . . . . 37


4.4.5 Evaluation Metrics and Statistical Significance . . . . . . . . . 38


4.5 Experimental Results and Analyses . . . . . . . . . . . . . . . . . . . . 40


4.5.1 Comparison of Results with Prior SOTA Methods . . . . . . . . 41


4.5.2 Assessment with Full and Partial Test Data . . . . . . . . . . . 43


4.5.3 Evaluation on the Ambiguous Set . . . . . . . . . . . . . . . . 48


4.5.4 What is the most effective label learning method for SER? . . . 53


XII


4.6 Summary . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 55


**5** **Training Loss by Using Co-occurrence Frequency of Emotions** **58**


5.1 Motivation . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 59


5.2 Background and Related Works . . . . . . . . . . . . . . . . . . . . . 60


5.2.1 Contrastive Learning in Emotion Recognition . . . . . . . . . . 60


5.2.2 Label Learning in Emotion Recognition . . . . . . . . . . . . . 61


5.3 Proposed Method . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 63


5.3.1 Penalization Weights based on the Counts of Co-Existing Emo

tions . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 63


5.3.2 Label Processing to Train SER Systems . . . . . . . . . . . . . 64


5.4.5 Statistical Significance . . . . . . . . . . . . . . . . . . . . . . 68


5.5 Experimental Results and Analyses . . . . . . . . . . . . . . . . . . . . 68


5.5.1 Does incorporating the penalty loss ( _LP_ + _loss_ ) benefit SER Sys

tems? . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 68


5.5.2 Effect of Co-occurrence Matrix . . . . . . . . . . . . . . . . . 69


5.6 Summary . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 70


**6** **Conclusion** **71**


6.1 Discussion and Limitation . . . . . . . . . . . . . . . . . . . . . . . . 72


6.2 Future Works . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 73


**Bibliography** **75**


XIII


# **List of Figures**

1.1 The figure illustrates the trends of papers whose title includes speech


emotion recognition based on the Google Scholar website. The x-axis


means years; the y-axis is the number of papers. . . . . . . . . . . . . . 1


test set according to each aggregation method. MR contains the lowest


amount of data, and AR always includes the entire test set available in


the dataset. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 30


4.2 Averaged macro-F1 scores across 18 experiments (as shown in Table


4.7) involving different databases and label-learning strategies on var

ious evaluation sets generated by the three rules: _majority_ _rule_ (MR),


_plurality rule_ (PR), and _all-inclusive rule_ (AR). The notations _∗_, _†_, and


_⋆_ are used to indicate when a model achieves significantly better per

formance than models trained with _MRTrain_, _PRTrain_, and _ARTrain_,


respectively. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 45


XIV


4.3 Averaged macro-F1 scores across 18 experiments (detailed in Table 4.7)


with different databases and label-learning strategies on the varied eval

uation sets generated by the PR-MR and AR-PR rules. The notations _∗_,


_†_, and _⋆_ indicate significantly better performance compared to models


trained using the _MRTrain_, _PRTrain_, and _ARTrain_ sets, respectively. . . 47


4.4 The figure depicts the procedure of visualizing feature embeddings. . . 49


4.5 T-SNE visualizations using embeddings generated from models trained


with the MR _Train_ and AR _Train_ sets show the distribution of feature


embeddings. This analysis includes the following emotion pairs: anger

neutral, sadness-happiness, neutral-happiness, and anger-sadness. . . . . 50


label learning, hard-label learning, and soft-label learning strategies. All


models have been evaluated on the **AR-PR** test set, which includes sam

ples that do not achieve MR or PR consensus. Symbols _⊕_, _‡_, and _⋄_


denote instances where a model significantly outperforms those trained


using distributional, hard, and soft-label learning strategies, respectively. 55


5.1 Illustration of a process for generating the presented penalization ma

trix. The 8-class emotions involved include contempt (C), neutral (N),


sad (S), happy (H), fear (F), disgusted (D), angry (A), and surprised


(SU). The procedure in detail can be found in Section 5.3.1. . . . . . . . 63


XV


# **List of Tables**

1.1 Table summarizes the loss of data and emotion rating across the public


emotion databases. . . . . . . . . . . . . . . . . . . . . . . . . . . . . 6


2.1 Table overviews the defined standard partitions for the IEMOCAP and


3.2 Table summarizes the label distribution for each emotion class of the


models. Notice that each sample could have more than one emotional


rating. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 23


3.3 Table summarizes cross-validation details of the IEMOCAP, following


[1,2]. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 25


3.4 Table summarizes the results in unweighted average recall (UAR) of all


models evaluated on the IEMOCAP. . . . . . . . . . . . . . . . . . . . 26


4.1 Table is an overview of the number of utterances, emotion classes, and


data loss ratios in several prominent emotional datasets. Here, P indi

cates primary emotions, and S indicates secondary emotions. . . . . . . 32


XVI


4.2 Here is an overview of how label vectors are constructed for the _all-_


_inclusive_ _rule_ (AR) using three examples, each with five annotations,


in a four-class emotion classification task. The four emotions include


neutral (N), happy (H), angry (A), and sad (S). Label vectors are created


in the format: (N, H, A, S). We show three examples. For instance, (C1)


N,N,A,A,S demonstrates that the five emotional annotations for Case


(C1) selected two for neutral, two for angry, and one for sad. . . . . . . 34


4.3 Here is an overview of the data loss ratios introduced by the label ag

gregation method on the PODCAST development, test, and train sets. P


represents primary emotions, and S represents secondary emotions. . . . 36


ity rule” (PR). . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 41


4.6 Table illustrates the Kullback-Leibler divergence (KLD) when train

ing and testing with each aggregation method under each label-learning


strategy for each database. We highlight in bold the best performance


for each condition. We denote _∗_, _†_, and _⋆_ when a model has significantly


better performance than a model training with _MRTrain_, _PRTrain_, and


_ARTrain_, respectively. . . . . . . . . . . . . . . . . . . . . . . . . . . . 42


XVII


4.7 The table presents the macro-F1 scores achieved when models are trained


and tested using each aggregation method across various label-learning


strategies for each database. The highest performance for each condi

tion is highlighted in bold. Symbols such as _∗_, _†_, and _⋆_ are used to


indicate when a model significantly surpasses the performance of those


trained with MR _Train_, PR _Train_, and AR _Train_, respectively. . . . . . . . 43


4.8 The table shows averaged macro-F1 scores across 18 experiments listed


in Table 4.7 and Table 4.6 with different databases and label-learning


strategies on the different evaluation sets generated by three rules, _ma-_


_jority rule_ (MR), _plurality rule_ (PR), and _all-inclusive rule_ (AR). The _↓_


neutral-happiness (neu.-hap.), and anger-sadness (ang.-sad.). The high

est silhouette score for each pair is emphasized in bold. . . . . . . . . . 51


4.11 Analysis of the impact of additional data introduced through the AR


approach. The table outlines two strategies: the oversampling approach,


which leverages data augmentation, and the undersampling approach,


which involves randomly removing samples to achieve consistency in


the dataset. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 52


XVIII


4.12 The results for the undersampling strategy compare training sets con

sisting of either 20,000 samples, following the designated aggregation


rules, or 32,831 samples formed by randomly adding 12,831 samples


regardless of consensus. This table shows results in a macro-F1 score,


underscoring the advantages of using the _ARTrain_ set. . . . . . . . . . . 53


5.1 The table overviews the results on distributional-label, multi-hard-label,


and single-label tasks for the primary emotion classification task. The


mark _∗_ denotes that the outcomes for SER systems utilizing the pre

sented matrix have statistical significance compared to the baseline ( _α_ =


0; _β_ = 1). . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 69


XIX


# **Chapter 1** **Introduction**

Figure 1.1: The figure illustrates the trends of papers whose title includes speech emotion recognition based on the Google Scholar website. The x-axis means years; the
y-axis is the number of papers.


1


tion [5]. Moreover, SER is crucial for voice assistants as it enables them to generate


speech with appropriate emotions by predicting the emotional tone of users’ voices. I


also observe some startups contribute to building SER solutions to improve users’ ex

periences, such as HUME, BEHAVIORAL SIGNALS, UNIPHORE, and COGNOVI


LABS. Those companies provide emotion-aware solutions for their clients to under

stand users’ emotions and improve user experiences.


Additionally, SER needs interdisciplinary collaboration, such as studies of psychol

ogy, spoken language, and natural language understanding. Most researchers follow


psychological studies to design and collect emotional corpus. In common practice,


researchers provide pre-defined categorical emotions for raters to choose from after lis

Figure 1.2: The figure illustrates three main contributions to modeling and evaluation
approaches in SER systems.


2


of humans is high-dimensional, and boundaries of emotions among emotion perception


of humans are blended and overlap. The critical findings inspire and motivate me to re

visit standard SER systems’ whole modeling and evaluation methods. We have come up


with the following research questions to answer: (1) Should we remove those minority


emotional ratings? (2) Should we only let SER systems learn the emotional perception


of a few annotators? (3) Should SER systems only predict one single emotion for each


sample? Those questions could be split into two main factors, the subjectivity of emo

tion perception and ambiguity of emotions, contributing to the disagreement of emotion


perception among raters because of human bias, including gender [8], culture [9], and


age [10]. This dissertation dives into the whole process of modeling and evaluating SER


Figure 1.3: The figure illustrates the current trends of prior works on SER.


3


#### **1.2 Background, Related Works, and Challenges**

This section introduces an overview of the background and challenges of the prior


SER studies.

##### **1.2.1 Emotion Representations**


There are two main ways to represent emotion perception. One is a dimensional


attribute that assumes every attribute is independent of each other, like arousal [11] or


valence [12]. The other one is categorical emotions [6,7], such as anger or sadness. This


dissertation only focuses on categorical emotions since the perception of categorical


emotions is better perceived across cultures than dimensional attributions [13].


emotions from music. Consequently, different modalities lead to varying emotional


perceptions in humans.


Previous research has employed various modalities to develop emotion recognition


systems. For example, Goncalves et al. [14] utilized audio-visual data to build such


systems. Almedia et al. [15] focused on training systems to identify emotions from


facial expressions. Additionally, studies [16, 17] have successfully detected emotions


through music. This dissertation, however, is concerned solely with speech-based emo

tion recognition systems [18,19].


4


##### **1.2.3 Evaluation of SER Systems**

Many research studies on SER primarily focus on predicting a single emotion, using


methods like majority voting [1] or plurality rules [20] to derive a consensus label for


evaluating SER systems. This approach often discards emotional ratings with minority


opinions and data lacking a consensus label, resulting in a simpler test set. Conse

quently, SER system performance evaluations may only partially represent their true


capabilities due to excluding some data and emotional ratings. Figure 1.3 showcases


the trends in previous SER research, highlighting that many studies approach SER as a


single-label task with hard-label (one-hot encoding) targets. For instance, in Figure 1.3,


a sample from IEMOCAP was rated as frustration, frustration, anger, anger, and sad

Few studies treat Speech Emotion Recognition (SER) tasks as multi-label tasks, con

trary to other emotion recognition fields, which do. For example, in text emotion recog

nition [23, 24], image emotion classification [25], and audio-visual emotion recogni

tion [26,27], emotions are considered valid if they receive any vote. They use multi-hot


labels, as illustrated in Figure 1.3. A close study by [28] on facial expression recogni

tion calculated soft labels based on vote frequency for each emotion, converting these


into binary vectors (either multi-hot or single-hot) based on the threshold (1 _/_ ( _C_ _−_ 1),


where C is the number of emotion classes). However, this misses key information about


primary and secondary emotions. In label distribution learning [29], [30] used facial


expression databases to collect emotion intensity scores from multiple annotators, av

5


Table 1.1: Table summarizes the loss of data and emotion rating across the public emotion databases.


Label Aggregation Method Majority Rule Plurality Rule **Our Goal**


Emotion Database Data Rating Data Rating Data Rating


IMPROV (P) 9.18% 28.52% 4.63% 26.41% 0% 0%
CREMA-D 35.80% 52.96% 8.55% 40.57% 0% 0%
PODCAST (P) 44.81% 59.87% 19.85% 49.24% 0% 0%
IEMOCAP 31.37% 49.44% 25.32% 45.70% 0% 0%
IMPROV (S) 54.18% 76.91% 12.32% 56.70% 0% 0%
PODCAST (S) 92.01% 96.99% 33.72% 78.13% 0% 0%


Average 44.56% 60.78% 17.40% 49.46% 0% 0%


eraging these to normalize the distributional labels for system training and evaluation.


Similarly, [31] did this for text emotion recognition. However, these methods are chal

lenging to apply in SER due to the lack of emotional intensity scores, as SER databases


typically ask raters to select pre-defined emotions. This is possible because querying

##### **1.2.4 Label Prepossessing for Training SER Systems**


The most common approaches to obtain consensus labels are majority rule and plu

rality rule, whose definitions are introduced below. Table 1.1 summarizes the loss of


data and emotional ratings using two conventional label aggregation methods, majority


rule and plurality rule. We aim to try our best to retain all data and emotional ratings to


train the SER systems.


   - Majority Rule (MR): it selects one of the pre-defined emotion classes only if more


than half of the votes select that class.


   - Plurality Rule (PR): it selects a class if one emotional class obtains more votes


6


than others.


We argue that the two above conventional aggregation methods lose variations of


emotion perception and the number of data during SER systems, leading to the poor


ability to predict the samples that have co-occurrence of emotions. Therefore, we pro

pose two ways to model the variations of emotion perception. (1) The first is to model


individual raters’ SER systems since each person has a different sensitivity to various


emotions [34]. For instance, some raters are good at perceiving sad emotions; some can


easily sense happy emotions. (2) The second approach proposes a novel label aggre

gation rule, named the “all-inclusive” rule, incorporating all the labeled data with the


emotional ratings in the emotion databases.


son is more likely to feel simultaneously sad and neutral than both sad and happy. In


text emotion recognition, a study by [35] adapted a loss function initially proposed


by [36] to account for label correlation among raters, thereby quantifying dependency


between emotions. Additionally, research by [37] introduced a multi-label focal ob

jective function designed to enhance the differentiation between positive and negative


emotions to improve emotion recognition perceptivity in text systems. This approach,


however, overlooks the possibility of both negative and positive emotions occurring


together. Unlike the studies mentioned earlier, we directly examine the relationships


between co-existing categories of emotions based on their co-occurrence frequencies,


allowing for mixed emotional states such as happiness and anger. For instance, consider


7


a scenario where a girl was upset at her boyfriend for being over an hour late, but upon


his arrival, she saw he was holding her a present, her favorite dress. By conceptualiz

ing the co-occurrence frequency of emotions in a matrix and normalizing it to create a


penalty matrix, we can integrate this into existing objective functions like cross-entropy


to penalize models during training. The penalty matrix assigns greater loss values when


SER systems predict rare emotional co-occurrences, as indicated by the training set an

notations. Importantly, this approach allows for the recognition of both positive and


negative emotions happening concurrently.

##### **1.2.6 Disagreement between Raters on the Emotion Datasets**


or hate speech tagging [40,41], pose unique challenges due to their fundamentally sub

jective nature. Obtaining labels for these tasks is complex because they heavily de

pend on individual interpreters. Annotator disagreements can result from various fac

tors [42–44], such as diverse backgrounds leading to different interpretations, lack of


interest in providing accurate labels, emotional biases, and contextual differences [45].


These variances introduce substantial noise into the labeling process, particularly prob

lematic in crowd-sourced evaluations [46].


Annotation noise poses a major challenge, and various strategies have been devel

oped to lessen its effects. For speech emotion classification tasks, it’s important to


understand that while noise can lead to discrepancies in labels, it’s not the only cause


8


of disagreement. In line with the methodologies applied in the MSP-PODCAST cor

pus [39], efficient noise reduction approaches include excluding evaluators with persis

tently low agreement rates, pausing crowd-sourcing efforts when agreement falls below


a certain threshold, and employing in-house staff who can undergo specialized training


to enhance label consistency. Yet, it’s crucial to note that perceptual variations are not


merely noise; they can offer valuable insights that a speech emotion recognition system


should utilize.


This dissertation aims to demonstrate that traditional methods of label aggregation,


such as majority or plurality voting, often overlook the nuanced nature of subjective


perception and may not be suitable for speech emotion classification. We propose an


(2) Should we only let SER systems learn the emotional perception of a few an

notators?


(3) Should SER systems only predict one emotion for each sample?


This dissertation proposes three methods to improve the process for label prepro

cessing, evaluation of SER systems, and training of SER systems, respectively.


9


##### **1.3.1 Every Rating Matters Considering the Subjectivity of Anno-** **tators**

We first explore the inherent subjectivity of how each annotator perceives emotions


to improve the performances of SER systems. We aim to maximize the emotional rat

ings using the existing soft-label method introduced by [22] for training SER systems.


Additionally, we develop an individual SER model for each annotator based on their


respective ratings. To integrate all possible emotional data, we merged the embeddings


obtained from pre-trained SER models using the traditional hard-label and the existing


soft-label methods across five individual annotator SER systems for late-fusion. The


results indicate that the proposed framework improves performance when assessed on a


performance of SER systems, since determining consensus labels isn’t practical in real

world situations. Our ground truth is structured as a distribution reflecting the frequency


ratio of emotional votes for each emotion class. Like the study conducted by [22], we


believe that using a distributional similarity metric offers a more accurate assessment


of SER systems’ performance compared to accuracy-based metrics like the macro-F1


score, due to the subjective nature of SER. Distributional metrics better match how hu

mans perceive emotions [6, 7]. Nevertheless, since the SER field is more accustomed


to accuracy-based metrics, we also provide results using those. However, we’ve noticed


that transforming distributional labels into binary vectors for accuracy evaluation might


lead to losing some emotional ratings, which is different from our goal. Still, accuracy

10


based metrics give the community and reviewers a more precise understanding.

##### **1.3.3 Training Loss Using Co-occurrence Frequency of Emotions**


To model the connection between co-occurrence of emotions, we counted the counts


of co-occurrence of emotions based on labeled data in the train set of the emotion


database as a matrix and normalized the frequency matrix by the number of individ

ual emotion classes. Then, we use the unit matrix to subtract the normalized frequency


matrix as a penalization matrix. To penalize the SER systems during training when the


models predict rare co-occurrence of emotions, we integrate the designed penalization


matrix into the current common objective functions, e.g., cross-entropy. Considering


emotion databases (Chapter 2), and then introduce the three proposed methods: mod

eling the subjectivity of annotators (Chapter 3), a novel evaluation method (Chapter 4),


and a training loss that accounts for the co-occurrence of emotion classes (Chapter 5).


11


# **Chapter 2** **Emotion Databases**

The chapter discusses four public emotional databases leveraged in this dissertation.


here.


scripted and spontaneous dialogues, primarily focusing on romantic relationship sce

narios to evoke diverse emotions. Each session involved one male and one female


actor. To guarantee an expressive variation, performers utilized scripts to elicit dis

tinct feelings. The final recordings were segmented into 10,039 utterances. All ut

terances have human-typed transcripts. Raters watched segmented clips and selected


emotions from a predefined list of ten categories: neutral, happy, sad, angry, surprised,


fear, disgusted, frustrated, excited, and ”other.” Addressing issues related to results re

producibility, mentioned in prior research [48], we have provided meticulous details on


dataset splits in Section 2.5.2. Given the original dataset’s deficiency of standardized


split sets, our documentation aims to bridge that gap, ensuring greater consistency and


12


reproducibility. The IEMOCAP is used in Chapter 3 and Chapter 4.

#### **2.2 IMPROV**


The MSP-IMPROV dataset, also known as IMPROV [49], collects audio-visual


recordings, and 12 actors are English speakers. All dyadic interactions represent four


distinct emotional states: angry, happy, sad, and neutral. The sessions are thoroughly


segmented into 8,438 individual clips by humans, with each clip being assessed by a


minimum of five annotators using crowdsourcing methods. To maintain the high qual

ity of annotations, the dataset integrates a quality control technique outlined by [50],


aimed at identifying and excluding unreliable annotators.


to ensure clarity and maintain consistency in follow-up analyses. The IMPROV is only


used in Chapter 4.

#### **2.3 CREMA-D**


The CREMA-D dataset [51] collects high-fidelity audio-visual recordings from 91


professional actors, comprising forty-three women and forty-eight men. They were di

rected to deliver one of six unique emotions with the given scripts: angry, disgusted,


fearful, happy, sad, or neutral. A key highlight is the comprehensive labeling proce

dure; spanning over 7,442 segments, each segment was evaluated by more than two


thousand distinct crowdsourcing raters. All data were subjected to assessments from


13


no fewer than six annotators, who identified one of the six defined emotions for each


performance.


The perceptual annotation process operates within three contexts: voice- and face

only and audio-visual. Raters focus exclusively on listening to the segments’ audio in


the voice-only context. They watch the actors’ faces without audio input in the face

only context. Lastly, in the audio-visual context, annotators evaluate both the facial


expressions and the audio concurrently.


For this dissertation on SER, we specifically concentrate on the emotional labels


gathered from the voice-only scenario. Unlike numerous previous SER studies that


leveraged labels from the audio-visual context or omitted annotation specifics entirely,


compiled from licensed podcast resources. These recordings are initially split into utter

ances and subsequently labeled through a crowdsourcing website. The labeling protocol


encompasses primary (P) and secondary (S) methods. Raters choose from nine catego

rized emotions in the primary emotion: angry, sad, happy, surprised, fear, disgusted,


contempt, neutral, and ”other.” The secondary emotion broadens this scope to the pri

mary emotions, plus eight additional ones: amused, frustrated, depressed, concerned,


disappointed, excited, confused, and annoyed, making a total of 17 emotional cate

gories. At least five contributors meticulously annotate each utterance to ensure robust


and reliable annotations. Different dataset versions certify various utterance quantities


within the training, development, and complementary test groups (test1 and test2). The


14


MSP-PODCAST is used in Chapter 4 and Chapter 5.

#### **2.5 Standard Partition**


The preceding study [48] indicates that 80.77% of SER research papers produce irre

producible results with the widely recognized IEMOCAP dataset. The primary obstacle


to reproducibility is the absence of standardized data splits (e.g., training, development,


and test sets) within the database. Previous studies each defined their partitions; how

ever, they often withheld detailed partitioning methodologies or source code, compli

cating repeatability. Consequently, this dissertation aims to make SER more transparent


and reproducible for everyone. We establish and define standard partitions for four


ments.


the training set. This approach ensures an unbiased and robust assessment of the model’s


performance. For instance, in the IEMOCAP study, we summarize the data partitioning


approach in Table 2.1. Each session involves two speakers in interactive dialogues and


allows us to define five speaker-independent splits, referred to as Ses. 1 through Ses.


5. We perform a five-fold cross-validation, as detailed in Table 2.1, whereby every fold


Table 2.1: Table overviews the defined standard partitions for the IEMOCAP and the
**Ses.** means the session in the database.


Partition Training Set Development Set Test Set


1 Ses. 1,2,3 Ses. 4 Ses. 5
2 Ses. 2,3,4 Ses. 5 Ses. 1
3 Ses. 3,4,5 Ses. 1 Ses. 2
4 Ses. 1,4,5 Ses. 2 Ses. 3
5 Ses. 1,2,4 Ses. 3 Ses. 4


15


Table 2.2: Table overviews the defined standard partitions for the IMPROV and the **Ses.**
means the session in the database.


Partition Training Set Development Set Test Set


1 Ses. 1,2,3,4 Ses. 5 Ses. 6
2 Ses. 1,2,3,6 Ses. 4 Ses. 5
3 Ses. 1,2,5,6 Ses. 3 Ses. 4
4 Ses. 1,4,5,6 Ses. 2 Ses. 3
5 Ses. 3,4,5,6 Ses. 1 Ses. 2
6 Ses. 2,3,4,5 Ses. 6 Ses. 1


Table 2.3: Tables summarize the session in the CREMA-D emotion database. Notice
that the **M** and **F** mean the male and F, respectively.


Session Gender Speaker ID


1 7M;11F 1037-1054


2 12M;6F 1001-1018


3 13M;6F 1073-1091


4 9M;9F 1055-1072


5 15M;3F 1019-1036


tailed in Table 2.2. The splitting method provides the SER system with information on


interactions featuring various pairs of speakers and testing on completely new speaker


pairings. Consequently, this strategy systematically evaluates the model’s capacity to


generalize to various dyadic exchanges within the IMPROV dataset.

##### **2.5.3 Standard Partition of the CREMA-D**


The CREMA-D database is split into 5 subsets according to speaker IDs for the


speaker-independent context. Each subset comprises a unique blend of males and fe

males and specific speaker IDs, elaborated in Table 2.3. The partitioning strategy aligns


with the methodology employed for the IEMOCAP dataset discussed in section 2.5.1.


16


# **Chapter 3** **Every Rating Matters Considering** **Subjectivity of Annotators**

integrated learning of both general emotional insights and specific rater profiles yields


the highest accuracy in emotion recognition.

#### **3.1 Motivation**


Traditional SER systems [1,2] typically use the plurality rule or majority rule from


a group of raters as the learning targets, termed the hard label, to train emotion recog

nizers. However, factors like gender [8], culture [9], and age [10] significantly influ

ence emotion perception, leading to natural disagreement and ambiguity in annotations


[52,53]. Consequently, the hard label approach overlooks emotion perception’s diverse


annotations and subjective nuances. To address this limitation, researchers [2,22] have


17


proposed using soft labels—a distributional representation instead of a single definitive


label—to capture blended emotion perceptions better. While the soft labeling method


enhances flexibility in representing the variability of emotion perception, it still disre

gards the unique input of individual annotators because it creates the label distribution


by aggregating inputs from all annotators. Therefore, we first build individual-based


SER systems to model diverse and accurate subjectivity of emotion perception to im

prove aggregated emotion performance.

#### **3.2 Background and Related Works**


tinuous dimensional emotion tracking from audio and video sources. However, they still


consider the ratings of all raters at that same time, but our method directly models in

dividual raters’ emotion perception, which can preserve more subjectivity of emotion


perception.

##### **3.2.2 Mixture of Annotators**


Disagreement is present not just in emotion perception but also in various other


areas like medical image tagging. Yan et al. [56] suggested that discrepancies arise


because each annotator possesses unique medical domain knowledge. To address this,


18


they proposed a method involving multiple annotators, which takes into account all


available information by repeatedly using training data points until the models fully


grasp each annotator’s input. Their approach was found to be more effective than the


traditional method that uses majority voting to determine ground truth.

##### **3.2.3 Soft-label Training Method for SER Systems**


Steidl et al. [22] initially argued that using only a single emotion label as ground


truth in emotion recognition tasks might not be suitable due to the subjective nature of


emotion perception. They proposed using soft labels as ground truth based on count


data and utilized entropy loss as an evaluation criterion. However, they re-assigned


those trained with common soft labels and hard labels. Finally, Zhang [58] was the first


to demonstrate the advantages of using soft labels in cross-corpus SER, through their


proposed objective function.

#### **3.3 Resource and Task Formulation**


We employ the IEMOCAP database as referenced in section 2.1, encompassing


emotional ratings by 12 distinct raters across 10 categorical emotion classes. For consis

tency with previous research, we utilize the identical evaluation data wherein the entry


is tagged with a singular emotion state, determined by a majority vote from more than


19


three annotators. This study focuses on recognizing four primary emotion classes: sad,


neutral, happy, and angry. Following the practices in [1,2], we consolidate the happiness


and excitement categories into one: happiness. This aggregation includes 5,531 data


samples used in the emotion recognition evaluation; this approach aligns with the tradi

tional use of the IEMOCAP dataset as a benchmarking standard. The test set excludes


the data without consensus labels. The emotion class distributions of data samples are


sad: 19.60%, happy: 29.58%, neutral: 30.88%, and angry: 19.94%. Half of the raters


are also actors, while the other half consists of in-house raters. We selected only 5 out


of the 6 in-house raters (E1, E2, E4, E5, and E6) since these five provided annotations


for samples across all 5 sessions. Therefore, the proposed method only builds those 5


individual annotators.


feature set. This set includes 12-dimensional Mel-Frequency Cepstral Coefficients (MFCCs),


voice probability measures, zero-crossing rates, fundamental frequency (F0) values,


loudness metrics, and their respective first-order derivatives. Additionally, the second

order derivatives of both loudness and MFCCs are featured. The feature extraction pro

cess is carried out with a frame length of 60ms and a step size of 10ms. These features


are normalized for each speaker with z-score normalization and then downsampled by


averaging over sets of five consecutive frames.


20


##### **3.4.2 Model Structure**

Utilizing the framework [1], all models in this study are designed. This frame

work comprises an input layer, a bidirectional long short-term memory (LSTM) layer,


a fully connected layer, and an output layer. Mirsamadi et al. [1] investigated the var

ious attention mechanisms, and their proposed weighted pooling layer considering the


attention weights applied over the frame-level input features achieved the best perfor

mance when the input features extracted by the “Emobase.config” file in the OpenS

MILE toolkit. Therefore, all models used the same structure, and we denoted the model


as the **BLSTM-FC** .


label emotion as ground truth. To consider that emotion perception could be overlapped


and blended, Steidl et al. [22] first propose the soft labels to calculate the distributional


label based on the votes for each emotion class. Fayek et al. [57] integrated the inter

rater variability with soft-label to build SER systems. Also, Ando et al. [2] modified


the formulation of the calculation of soft labels by introducing _α_ to slightly change the


distribution of conventional soft labels as below.


_α_ + [�] _n_ _[R]_ _[v]_ _i_ _[n]_
_t_ ( _ci_ ) = _α × C_ + [�] _i_ _[C]_                 - _Rn_ _[v]_ _i_ _[n]_ _,_ (3.1)


where _ci_ means the _i−_ th emotion class, n represents the _n−_ rater, _vi_ _[n]_ [is] [the] [binary]


value to check whether _n−_ rater chooses _ci_ emotions, _C_ is how many categorical emo

21


tions and the _R_ represents the number of annotators for _t_ samples. In this dissertation,


we follow the study [2] to assign the _α_ value as 0 _._ 75, and _C_ is 4 since the number of


emotion classes is 4.

#### **3.5 Proposed Method**

##### **3.5.1 Rater-Modeling**


Due to the inherent subjectivity and unique individual differences, different people


may interpret the exact spoken phrase in varied ways. To enhance the SER systems, we


incorporate rater modeling. We categorize annotators into two groups: **Crowd** and **E** .


models. With soft labels, **Crowd** _S_ has over 3,185 more samples compared to **Crowd** _H_ .


Table 3.1: Table overviews the data samples used to train models.


**Model** **Total** **Multiple** **Single**


**Crowd** _H_ 5531 0 5531
**Crowd** _S_ 7774 3185 4589
**E1** 5954 44 5910
**E2** 7845 38 7807
**E4** 6429 212 6217
**E5** 422 3 419
**E6** 773 20 753


22


Table 3.2: Table summarizes the label distribution for each emotion class of the models.
Notice that each sample could have more than one emotional rating.


**Model** **Neutral** **Anger** **Sadness** **Happiness**


**CrowdH** 80.88% 19.94% 19.60% 29.58%
**CrowdS** 29.33% 17.77% 17.10% 35.79%
**E1** 8.49% 21.21% 20.64% 49.67%
**E2** 22.45% 26.58% 19.62% 31.35%
**E4** 52.88% 12.41% 10.95% 23.76%
**E5** 69.88% 15.29% 5.88% 8.94%
**E6** 26.73% 15.76% 14.22% 43.38%

##### **3.5.2 Final Concatenation Layer**


After successfully computing all model components, including the two Crowd mod

els and 5 E _N_ models, we froze their respective model weights. Then, we concatenate


the representation from the final layer before the softmax activation in each BLSTM-FC


presented in Fig. 3.1.


The foundational component is the BLSTM-FC model equipped with an attention


mechanism. This model architecture includes two fully connected (FC) layers with Rec

Figure 3.1: The figure illustrates the overall proposed model.


23


Figure 3.2: The figure illustrates the baselines and models for the ablation study.


tified Linear Unit (ReLU) activation functions, a BLSTM layer enhanced using atten

tion weights, and concludes with a fully-connected layer employing a softmax function.


Specifically, the model comprises 256 hidden units in the initial dense layer, 128 hidden


study. Subsequently, we evaluate and compare the performance outcomes for each com

ponent of the overall architecture, as detailed below.


   - **Baseline** **CROWD** _H_ : This model closely parallels the previous proposed, but it


utilizes a BLSTM-FC framework trained on hard labels in the study [1].


   - **Baseline CROWD** _S_ : This model employs soft label training, a method proposed


by the work [2], designed to utilize all labeled samples.


   - **Baseline** **CROWD** _HS_ : The model represents a fusion of Crowd _H_ and Crowd _S_ .


It combines all Crowd-relevant information by concatenating the representations


from Crowd _H_ and Crowd _S_ before feeding them into the final softmax layer.


24


   - **Proposed** **Rater** **Model,** **E** _N_ : Each of the E _N_ models is trained using soft label


learning based on the annotations made by individual raters.


   - **Proposed** **Fusion** **of** **E** _N_ : The model integrates all individual E _N_ components


(five separate annotators). It consolidates all rater-specific information by con

catenating the representations from each E _N_ before passing them through the final


softmax layer.


   - **Proposed Model** : As depicted in Figure 3.1, this model represents our ultimate


proposal and leverages all available Crowd and E _N_ information. It achieves this


by concatenating the representations from both Crowd _H_ and Crowd _S_ before feed

Early stopping criteria to minimize the loss value on the validation set are applied during


training across all configurations to prevent overfitting and ensure model effectiveness.


The optimizer utilized in this study is ADAMMAX [60].


Table 3.3: Table summarizes cross-validation details of the IEMOCAP, following [1,2].


**Fold** **Training Set** **Development Set** **Test Set**



**1** Ses. 1,2,3,4



**1** Ses. 1,2,3,4 Ses. 5

**2** Ses. 2,3,4,5 Ses. 1
**3** Ses. 3,4,5,1 Randomly 10% of training data Ses. 2
**4** Ses. 1,4,5,2 Ses. 3
**5** Ses. 1,2,4,3 Ses. 4



Randomly 10% of training data



25


Table 3.4: Table summarizes the results in unweighted average recall (UAR) of all
models evaluated on the IEMOCAP.


**Model** **Overall** **Neutral** **Angry** **Happy** **Sad**


**Crowd** _H_ **[1]** 0.5745 0.5571 0.6329 0.4502 0.6577
**Crowd** _S_ **[2]** 0.5712 0.4970 0.6298 0.6285 0.5314
**Crowd** _HS_ 0.5858 0.5966 0.5931 0.5363 0.6171
**E1** 0.5098 0.0804 0.6131 **0.7724** 0.5734
**E2** 0.5968 0.3878 0.6435 0.6425 0.6261
**E4** 0.4859 0.8129 0.4542 0.3820 0.2944
**E5** 0.3762 **0.8689** 0.4762 0.1121 0.0475
**E6** 0.4582 0.3685 0.4010 0.6039 0.4595
**EN** 0.6024 0.4964 0.6364 0.6148 0.6619


**Proposed** **0.6148** 0.5455 **0.6451** 0.6032 **0.6656**

#### **3.8 Experimental Results and Analyses**


Table 3.4 provides an overview of the results across various comparative models.


Our presented framework achieves the highest overall emotion classification perfor

which performs better with neutral and sad emotions. The complementary strengths


of Crowd _H_ and Crowd _S_ underscore the importance of their integration for advanced


emotion recognition results. Historically, happiness has been a challenging class to


identify [1, 2], and it benefits from soft-label learning, suggesting that happiness has a


more diffused presence within the acoustic spectrum than other emotions, such as anger


and sadness.


Furthermore, individual models tend to have low recognition rates, probably because


of the subjective perspectives of unique raters and the uneven distribution of emotion


classes within each annotator’s labeling. For instance, as Table 3.4 illustrates, the E1


model shows low recognition accuracy for the neutral state but reasonable performance


26


for recognizing happy emotion, while it is reverse for the E5 model. Examining the


emotion distribution in Table 3.2 reveals that this discrepancy is linked to the variety


and quantity of emotional data annotated by each rater. By integrating raters’ models


at the late-fusion level, E _N_ effectively taps into multiple complementary viewpoints,


enabling it to learn a well-rounded and nuanced understanding of emotion perception


from distinct individual perspectives.


Last but not least, by employing individual rater models, our proposed method can


expand the dataset used for building SER systems, compared to the traditional hard

label approach that limits the number of data in the train set to instances where con

sensus among raters is achieved. This allows for a more robust and comprehensive


racy. The framework achieves an impressive score of 61.48% on a task involving 4-class


emotion categorization. Although numerous studies have tackled the issue of annota

tor subjectivity, this pioneering approach explicitly combines consensus and individual


differences in emotion perception, leading to improved classification performance on a


benchmark dataset.


27


# **Chapter 4** **Novel Evaluation Method by an** **All-Inclusive Aggregation Rule**

We emphasize the need to account for all annotations and samples in the dataset, as


focusing only on performance metrics derived from a test set filtered by majority or plu

rality rules may skew the model’s performance evaluations. We specifically investigate


SER tasks and note that traditional aggregation rules result in data loss ratios between


4.63% and 92.01%, as shown in Table 4.1. Based on this insight, we introduce a ver

satile, all-inclusive rule, a label aggregation approach to appraise SER systems using


comprehensive test data. We differentiate the conventional single-label approach with


a multi-label methodology catering to the coexistence of various emotions. Training an


SER model with data chosen by the all-inclusive rule consistently achieves better macro

F1 scores when evaluated on the whole test set, including ambiguous, non-consensus


28


samples.

#### **4.1 Motivation and Background**


Given the inherently subjective nature of these tasks, models are often evaluated us

ing labels derived from human perceptual assessments, where multiple raters annotate


each data point. The common practice for processing these annotations and creating


training and testing sets relies on majority or plurality aggregation methods. These


methods ignore annotations that do not correspond with the consensus label. However,


co-existing emotions are frequently observed in everyday interactions [21], making it


challenging for a single label to represent a sample’s emotional perception fully. Ad

soft-label learning strategies to incorporate all samples [18, 57, 61–65]. Nonetheless,


test sets remain _simplified_, considering only sentences that meet MR or PR criteria,


thereby overlooking complex and ambiguous samples.


We propose a practical methodology that amalgamates all annotations gathered from


subjective evaluations for training and test sets, thereby enhancing the practical appli

cability of these systems. Although this approach is compatible with any domain re

quiring labels derived from perceptual assessments, our focus is on the SER task, where


co-occurring emotions are common in everyday interactions. Unlike traditional meth

ods that neglect non-consensus labels, we retain all data points in the training and test


sets. This strategy enables SER models to utilize comprehensive data during training


29


Figure 4.1: A diagram illustrating how much data and ratings are used in the final test


AR method, every data point is included in the test set, thus underlining the exhaustive


performance evaluation of SER systems. The main research questions driving the study


are as follows.


   - How is the performance of SER systems influenced by using different aggregation


methods for the training set annotations?


   - Does utilizing data from the all-inclusive rule in training an SER system enhance


performance on ambiguous emotions compared to data processed with majority


or plurality rules?


   - Which label learning strategy should be employed for training SER systems to


30


achieve optimal performance when tested on the entire data set?

#### **4.2 Previous Literature**

##### **4.2.1 Evaluation of SER Systems**


Evaluating SER systems on a complete test set is crucial. However, the common


approach involves discarding samples that lack consensus emotion labels. When gath

ering emotional annotations from multiple workers, significant disagreement often ex

ists among annotators [66–68], leading many studies to eliminate numerous data points


from the test set. For instance, the IEMOCAP and CREMA-D corpora use the major

category, ignoring secondary emotions in the recordings. In reality, emotional states


often co-exist (e.g., a person can be sad and angry) [21]. Therefore, consolidating mul

tiple annotations into a single class and discarding non-consensus data points does not


accurately capture whether SER system predictions reflect the complex emotional be

haviors observed in daily interactions. Although some studies have explored using a


”multiple-hot” vector to frame SER as a multi-label problem [23,27,77], this approach


does not discern dominant emotions. It treats all annotations equally valid, even if a


single annotator selected a class.


To our knowledge, Riera et al. [78] is the only study advocating for including all test


samples in evaluating SER systems rather than discarding non-consensus data. How

31


Table 4.1: Table is an overview of the number of utterances, emotion classes, and data
loss ratios in several prominent emotional datasets. Here, P indicates primary emotions,
and S indicates secondary emotions.


Label Aggregation MR PR AR


Database # Utterances Data Rating Data Rating Data Rating


IMPROV (P) 8438 9.18% 28.52% 4.63% 26.41% 0.00% 5.12%
CREMA-D 7442 35.80% 52.96% 8.55% 40.57% 0.00% 0.00%
PODCAST (P) 90978 44.81% 59.87% 19.85% 49.24% 0.00% 6.15%
IEMOCAP 10039 31.37% 49.44% 25.32% 45.70% 0.00% 3.10%
IMPROV (S) 8438 54.18% 76.91% 12.32% 56.70% 0.00% 4.23%
PODCAST (S) 90978 92.01% 96.99% 33.72% 78.13% 0.00% 1.64%


Average 44.56% 60.78% 17.40% 49.46% 0.00% 3.37%


ever, their study did not explore training SER systems with various label learning meth

ods. It involved relabeling some emotions (e.g., labeling excited as happy and surprised


as ”other”), which is a significant limitation. Unlike that study, this dissertation retains


ods.


valence and arousal. Furthermore, Yang et al. [80] utilized emotion shift as difficulty


scores to categorize samples as ”easy” or ”hard.” They trained text-based conversational


emotion recognition systems progressively, starting with easy samples and moving to


more challenging ones. Their findings show that curriculum learning boosts perfor

mance in emotion recognition within conversations, as incorporating harder samples


during training increases the training loss, thereby refining the system’s accuracy. Sim

ilar findings have been reported in recent research [81].


32


#### **4.3 Methodology**

We present a new aggregation methodology called the _all-inclusive_ _rule_ (AR), de

signed to facilitate the training and evaluation of SER systems using an exhaustive test


set. This includes data points lacking Majority Rule (MR) or Plurality Rule (PR) con

sensus. The definition, significance, and application of this rule are thoroughly ex

plained.

##### **4.3.1 Proposed All-inclusive Rule**


The All-Inclusive Rule (AR) is an aggregation methodology that retains all anno

tated samples within a dataset, regardless of vote frequencies. This method ensures data


An example is shown in Table 4.2 Case (C1), where the hard label could be (1,0,0,0) or


(0,0,1,0). AR produces the ground truth for the soft-label or distribution-label approach


by reflecting the vote distribution among emotional classes.


AR consistently utilizes the distributional ground truth when producing the test set,


irrespective of the chosen label-learning strategy, which is highlighted in the rightmost


column of Table 4.2. This comprehensive approach ensures every annotated data point


and all its annotations are integral to the test set. The all-inclusive rule enhances the


label descriptor, more accurately capturing the emotional nuances of data points by


integrating sentences that reflect ambiguous emotions into the test set.


33


Table 4.2: Here is an overview of how label vectors are constructed for the _all-inclusive_
_rule_ (AR) using three examples, each with five annotations, in a four-class emotion
classification task. The four emotions include neutral (N), happy (H), angry (A), and
sad (S). Label vectors are created in the format: (N, H, A, S). We show three examples.
For instance, (C1) N,N,A,A,S demonstrates that the five emotional annotations for Case
(C1) selected two for neutral, two for angry, and one for sad.


**Training Set** **Test Set**
**Case**
Hard-label Soft-label Distribution-label Label


(1,0,0,0)



(C1) N,N,A,A,S



OR


(0,0,1,0)



(0.4,0.0,0.4,0.2) (0.4,0.0,0.4,0.2) (0.4,0.0,0.4,0.2)



(C2) N,N,H,A,S (1,0,0,0) (0.4,0.2,0.2,0.2) (0.4,0.2,0.2,0.2) (0.4,0.2,0.2,0.2)


(C3) N,N,N,A,S (1,0,0,0) (0.6,0.0,0.2,0.2) (0.6,0.0,0.2,0.2) (0.6,0.0,0.2,0.2)

##### **4.3.2 Employing the All-Inclusive Rule for Test Set Construction**


In addition, our all-inclusive rule allows SER models to be tested on the entire test


set, including secondary emotions. Previous studies have often disregarded secondary


emotional annotations due to considerable data loss from standard aggregation methods


(up to 92.01% as noted in Table 4.1). As the AR method utilizes the fully annotated


test set, we can assess the SER model with secondary emotions, which have not been


examined before. Table 4.1 highlights the proportion of data loss introduced by dif

ferent aggregation methods across the four datasets used in this study for primary and


secondary emotions—utilization of MR and PR results in discarding up to 92.01% and


33.72% of the data, respectively. The most significant data loss occurs when classifying


secondary emotions in the MSP-Podcast corpus.


34


#### **4.4 Experimental Setup**

##### **4.4.1 Resource**

Four publicly available emotion databases, as detailed in Chapter 2, are utilized


in our research. The corpus version 1.10, containing 104,267 annotated utterances,


is employed. However, the “Test2” set is excluded, narrowing the dataset to 90,978


utterances, as shown in Table 4.1.

##### **4.4.2 Speech Emotion Classifier**


To assess the performance of various aggregation methods, we utilize the Wav2vec2.0


12 of the 24 transformer layers from the architecture, which preserves recognition per

formance while reducing the number of parameters [84]. Two hidden layers and a soft

max output layer are attached to this trimmed Wav2vec2.0 model. Each hidden layer


with the rectified linear unit (ReLU) activation function comprises 1,024 nodes. Im

plemented with average pooling per utterance, the outputs from the Wav2vec2.0 layers


feed into the classification layers. We apply a dropout function with ( p = 0.5 ) to the


first and second classification layers for regularization.


Our implementation is based on the HuggingFace library [86] and uses a pre-trained


”wav2vec2-large-robust” model. During fine-tuning, convolutional and transformer lay

ers of the Wav2vec2.0 model are frozen—a strategy that has shown better performance


35


Table 4.3: Here is an overview of the data loss ratios introduced by the label aggregation method on the PODCAST development, test, and train sets. P represents primary
emotions, and S represents secondary emotions.


Rule Set PODCAST (P) PODCAST (S)


Training 47.95% 88.63%
MR Development 47.90% 89.64%
Test 47.08% 90.90%


Training 18.76% 29.46%
PR Development 19.62% 28.90%
Test 17.14% 27.76%


Training 0.00% 0.00%
AR Development 0.00% 0.00%
Test 0.00% 0.00%


than fully fine-tuning all parameters [83]. We employ the Adam optimizer [87] and set


up a learning rate as 0 _._ 0001, structuring mini-batches from 32 utterances and training


the model over 100 epochs. The best recognition performance model is chosen from the


sessions. For IEMOCAP, IMPROV, and CREMA-D, a _K_ -fold cross-validation is ap

plied, where K means how many sessions. Each fold includes one session as the test


set, one as the development set, and the remaining is the training set. More details about


partitions are in Section 2.5


Table 4.1 reflects data loss ratios derived from each label aggregation method across


various databases. We evaluate data loss ratios in every partition (train, development,


test set). Observations indicate that data loss trends are relatively consistent across


all four datasets. Thus, Table 4.3 exemplifies these distributions specifically for the


PODCAST database, and the trends are similar in Table 4.1.


36


##### **4.4.3 Train/Test Set Defined by Aggregation Rules**

In this evaluation, the models are trained and tested using both matching and mis

matching aggregation rules. For both the training and development sets, ground truth


is established using MR, PR, and AR, denoted as _MRTrain_, _PRTrain_, and _ARTrain_,


respectively. The models are assessed on sets derived from MR, PR, and AR rules dur

ing testing. Additionally, two extra test conditions are defined, illustrated by the _donuts_


in Figure 4.1: PR-MR includes test samples accepted by PR but not by MR, whereas


AR-PR encompasses those accepted by AR but not by PR. The AR-PR condition is


the most ambiguous set, as it includes samples with non-consensus annotations. To


our knowledge, this study is the first to evaluate SER models using such non-consensus


annotations.


For hard-label learning, the ground truth is constructed with a one-hot encoding,


where the class receiving the highest number of votes from annotators is represented as


”1.0”. When utilizing the training set aggregated with AR, if there is no clear consen

sus, one of the top-voted emotions is randomly chosen as the ground-truth emotion. We


smooth the one-hot encoding ground truth vector using the smoothing strategy proposed


by Szegedy et al. [89] with a parameter set of 0.05. This method slightly adjusts prob

abilities for classes assigned initially a zero value. The SER systems are then trained


using the cross-entropy (CE) objective function.


For both soft-label learning and distribution-label learning, the ground-truth vector


reflects the distribution of annotator votes. This is achieved by dividing the vote count


37


for each class by the total number of votes for each data point. We also apply the label

smoothing strategy used in hard-label learning. Soft-label learning targets are optimized


using the CE loss function, while distribution-label learning uses the Kullback–Leibler


divergence (KLD) as the cost function.

##### **4.4.5 Evaluation Metrics and Statistical Significance**


**Hard-decision-based assessment**


This study employs macro-F1 scores to evaluate SER performance, which involves


calculating precision and recall rates. The MR, PR, and PR-MR test sets are structured


by selecting a single class, making them compatible with macro-F1 scoring. The class


how many emotion classes. This method is in line with those employed in previous


studies [78,90].


Consider an emotion recognition task that distinguishes between four emotions:


neutral, anger, sadness, and happiness. In one instance, five different reviewers each


gave their rating based on the sample, resulting in the following annotations: angry (A),


sad (S), sad (S), neutral (N), and angry (A). To determine the label distributions, we


categorize the data into (N, A, S, H) and get the proportions (0.2, 0.4, 0.4, 0.0).


The threshold is set to (1/4 = 0.25), so we convert the ground truth to (0,1,1,0). Dur

ing the inference, suppose we have predictions from three different models: (0.1, 0.45,


0.45, 0.0), (0.2, 0.35, 0.35, 0.1), and (0.45, 0.1, 0, 0.45). Applying the (0.25) threshold,


38


these outputs are converted into (0,1,1,0), (0,1,1,0), and (1,0,0,1), respectively. In this


example, the (0,1,1,0) and (0,1,1,0) fully match the ground truth.


**Distribution-based Assessment**


Following the approach proposed by Steidl et al. [22], where results are assessed


using an entropy-based metric, we employ the _Kullback-Leibler_ _divergence_ (KLD) to


determine the similarity between the model’s predicted distribution and the subjective


annotations. This method checks whether an SER model aligns with human emotional


perception. Unlike the macro-F1 evaluations, which binarize the model’s output for


single-label or multi-label tasks, we utilize the model’s probability distributions across


ities. Distribution-based assessments keep all data and maximum usage of emotional


ratings while evaluating the SER performances. Every assessment has different advan

tages and disadvantages, so both are presented in the paper. Table 4.4 outlines the ben

efits and limitations of using KLD versus traditional accuracy metrics (e.g., macro-F1,


micro-F1, and weighted-F1). Reporting both metrics offers complementary and more


detailed insights.


**Statistical Significance**


We assess the statistical significance of the results per each aggregation method uti

lized. For cross-validation experiments (IEMOCAP, CREMA-D, and IMPROV), the


39


Table 4.4: Comparison of distribution-based and hard-decision-based assessment metrics.








|Metric|Distribution-based assessment|Hard-decision-based assessment|
|---|---|---|
|Advantages|•<br>We can directly compare the models’ predictions to hu-<br>man perception without needing extra thresholding meth-<br>ods.<br>•<br>It is tuned to the overall shape and structure of the dis-<br>tributions, refecting both the accuracy and confdence of<br>the predictions.|•<br>The macro-F1 score has a defned range between 0 and 1,<br>facilitating straightforward interpretation and comparison<br>across various models and datasets.<br>•<br>By applying thresholds to the labels, we can mitigate the<br>infuence of noisy annotations from raters who were not<br>attentive.|
|Limitations|•<br>The performance differences between the baseline and<br>proposed models are diffcult to interpret because the<br>scale differences are minimal.<br>•<br>It lacks a fxed range, which makes it challenging to inter-<br>pret and compare absolute values across different datasets<br>or models.<br>•<br>It is susceptible to slight distribution variations, especially<br>when dealing with sparse or high-dimensional data.|•<br>All predictions and ground truth need to be binary (0 or<br>1)—this requirement can lead to information loss and re-<br>duced granularity, as it oversimplifes the distributional<br>nature of the ground truth.<br>•<br>It is challenging to assess model performance on less<br>common emotions, such as fear, due to limited available<br>data.|



models trained using _MRTrain_, _PRTrain_, and _ARTrain_ sets, respectively.

#### **4.5 Experimental Results and Analyses**


The experimental analysis begins by benchmarking our presented method against


state-of-the-art (SOTA) baselines, showcasing the advantages of the SER strategy uti

lized in this research (Section 4.5.1). Following that, we address the three research


questions outlined in Section 4.1 (Sections 4.5.2, 4.5.3, and 4.5.4).


40


##### **4.5.1 Comparison of Results with Prior SOTA Methods**

We assess the SER model’s performance against three existing SOTA benchmarks


using the IMPROV(P), CREMA-D, PODCAST(P), and IEMOCAP corpora. As dis

cussed by Li et al. [91], the first reference model establishes an end-to-end system that


converts speech into spectrograms and utilizes a self-attention mechanism to highlight


emotional elements within sentences. At its time of publication, this model set the SOTA


performance for identifying four primary emotions from the IEMOCAP database. The


second baseline is presented in the work by Pepino et al. [92], which leverages wav2vec


2.0 for extracting speech characteristics and combines them with hand-crafted features


from eGeMAPS [93], achieving top-tier classification outcomes on the IEMOCAP col

input.


Following previous research, the investigations treat SER as a single-label problem,


providing performance results under MR or PR test paradigms while training and eval

uating models across all primary emotion categories. Table 4.5 details the comparative


Table 4.5: Table shows the comparative evaluation between our proposed model and existing SOTA baselines for the IMPROV(P), CREMA-D, IEMOCAP, and PODCAST(P)
databases. The performance measurements are in the macro-F1 score, capturing the effectiveness of models by grouping labels in the test sets following the “majority rule”
(MR) or “plurality rule” (PR).


MR PR
Aggregation Method IMPROV(P) CREMA-D IEMOCAP PODCAST(P)

|MRT rain/PRT rain|Li et al. [91]<br>Pepino et al. [92]<br>Goncalves et al. [75]<br>The proposed|0.398 0.311 0.256<br>0.331 0.223 0.191<br>0.539 0.574 0.261<br>0.512 0.591 0.269|0.150<br>0.142<br>0.161<br>0.184|
|---|---|---|---|
|_ART rain_|The proposed|**0.562**<br>**0.585**<br>**0.279**|**0.166**|



41


Table 4.6: Table illustrates the Kullback-Leibler divergence (KLD) when training
and testing with each aggregation method under each label-learning strategy for each
database. We highlight in bold the best performance for each condition. We denote _∗_,

_†_, and _⋆_ when a model has significantly better performance than a model training with
_MRTrain_, _PRTrain_, and _ARTrain_, respectively.


Aggregation Hard-label learning Soft-label learning Distributional-label learning


Database (training) MR PR AR PR - MR AR - PR MR PR AR PR - MR AR - PR MR PR AR PR - MR AR - PR






|MRT rain<br>IMPROV(P) P RT rain<br>ART rain|0.235† 0.231† 0.229† 0.143 0.190<br>0.256 0.252 0.249 0.138 0.193<br>0.211∗† 0.208∗† 0.206∗† 0.139 0.180|0.175 0.172 0.171 0.108 0.150<br>0.172 0.169 0.169 0.117 0.162<br>0.182 0.180 0.178 0.115 0.157|0.232 0.233 0.236 0.271 0.285<br>0.240 0.242 0.244 0.289 0.286<br>0.237 0.238 0.241 0.277 0.283|
|---|---|---|---|
|CREMA-D<br>_MRT rain_<br>_P RT rain_<br>_ART rain_|0.078<br>0.091<br>0.094<br>0.122<br>0.129<br>**0.064**_∗_<br>**0.073**_∗_<br>**0.075**_∗_<br>0.094_∗_<br>0.099_∗_<br>0.068_∗_<br>0.075_∗_<br>0.076_∗_<br>**0.092**_∗_<br>**0.095**_∗_|**0.055**<br>0.058<br>0.059<br>0.066<br>0.066<br>0.058<br>0.057<br>0.057<br>0.056_∗_<br>0.059_∗_<br>0.058<br>**0.056**<br>**0.056**_∗_**0.053**_∗_<br>**0.055**_∗_|0.112<br>0.136<br>0.142<br>0.192<br>0.203<br>0.109<br>0.131<br>0.136<br>0.185<br>0.188_∗_<br>**0.103**_∗_**0.122**_∗†_ **0.126**_∗†_ **0.166**_∗†_ **0.178**_∗_|
|PODCAST (P)<br>_MRT rain_<br>_P RT rain_<br>_ART rain_|**0.150**<br>0.142<br>0.141<br>0.128<br>0.136<br>0.150<br>**0.137**<br>**0.135**<br>**0.112**_∗⋆_**0.125**_∗⋆_<br>0.170<br>0.153<br>0.150<br>0.123<br>0.134|**0.157**<br>**0.142**<br>**0.139**<br>0.114<br>0.125<br>0.164<br>0.144<br>0.140<br>**0.110**<br>**0.122**<br>0.172<br>0.151<br>0.146<br>0.113<br>0.125|0.203<br>0.219<br>0.223<br>0.248<br>**0.242**<br>0.203<br>0.218<br>0.222<br>0.244<br>0.243<br>**0.200**<br>**0.214**<br>**0.220**<br>**0.240**<br>0.245|
|IEMOCAP<br>_MRT rain_<br>_P RT rain_<br>_ART rain_|0.203<br>0.201<br>0.202<br>0.180<br>0.205<br>0.202<br>0.201<br>0.201<br>0.186<br>0.201<br>**0.185**<br>**0.183**_∗†_ **0.182**_∗†_ **0.159**_∗†_ **0.178**_∗†_|0.162<br>0.160<br>0.156<br>0.128<br>0.147<br>0.150_∗_<br>0.148_∗_0.145_∗_0.125<br>0.135_∗_<br>**0.143**_∗_<br>**0.141**_∗_**0.138**_∗_**0.120**<br>**0.130**_∗_|0.211<br>0.212<br>0.221<br>0.223<br>0.245<br>**0.204**<br>**0.206**<br>0.214<br>0.225<br>0.237<br>0.208<br>0.209<br>**0.214**<br>**0.217**<br>**0.227**_∗_|
|IMPROV (S)<br>_MRT rain_<br>_P RT rain_<br>_ART rain_|0.118<br>0.128<br>0.130<br>0.139<br>0.147<br>**0.103**_∗⋆_**0.103**_∗_<br>**0.104**_∗_<br>0.102_∗_<br>**0.109**_∗_<br>0.116<br>0.108_∗_<br>0.108_∗_<br>**0.099**_∗_<br>0.110_∗_|**0.090**_†⋆_0.088<br>0.089<br>0.087<br>0.094<br>0.103<br>0.089<br>0.088<br>0.074_∗_<br>0.082_∗_<br>0.100<br>**0.087**<br>**0.086**<br>**0.072**_∗_<br>**0.080**_∗_|**0.116**<br>0.158<br>0.163<br>0.205<br>0.196<br>0.119<br>0.150<br>0.155<br>0.184_∗_<br>0.190<br>0.120<br>**0.146**_∗_<br>**0.150**_∗_<br>**0.174**_∗_<br>**0.180**_∗_|
|PODCAST (S)<br>_MRT rain_<br>_P RT rain_<br>_ART rain_|0.085<br>0.098<br>0.102<br>0.100<br>0.113<br>**0.075**<br>**0.062**_∗_<br>**0.063**_∗_<br>**0.060**_∗_<br>0.067_∗_<br>0.084<br>0.064_∗_<br>0.064_∗_<br>0.061_∗_<br>**0.065**_∗_|**0.074**_†⋆_0.071<br>0.073<br>0.071<br>0.078<br>0.091<br>**0.060**_∗_**0.060**_∗_**0.056**_∗_<br>**0.058**_∗_<br>0.097<br>0.062_∗_0.061_∗_0.057_∗_<br>0.058_∗_|0.079<br>0.144<br>0.151<br>0.153<br>0.171<br>**0.067**<br>0.123_∗_<br>0.132_∗_<br>0.131_∗_<br>0.156_∗_<br>0.073<br>**0.117**_∗_<br>**0.126**_∗_<br>**0.124**_∗_<br>**0.149**_∗_|



references.


Specifically, on the IMPROV(P) corpus, our method achieves a macro-F1 score of


0.562 with AR _Train_, outstripping the result from Goncalves and Busso [75] which had


a score of 0.539. Nevertheless, training with PR _Train_ resulted in a lower macro-F1


score of 0.512 compared to 0.539. For the CREMA-D set, we report a result of 0.591


using the MR _Train_ set and 0.585 with the AR _Train_ scenario in a macro-F1 score, both


excelling beyond the SOTA score of 0.574. Moreover, our approach similarly outper

forms other SOTA methodologies [75,91,92] in both the IEMOCAP and PODCAST(P)


datasets.


42


##### **4.5.2 Assessment with Full and Partial Test Data**

Table 4.7 and Table 4.6 present the macro-F1 scores and KLD values for the dif

ferent combinations of aggregation methods and label-learning strategies, respectively.


These scores are derived from 18 experiments using various databases, where models


were trained with the _MRTrain_, _PRTrain_, or _ARTrain_ sets (6 databases × 3 learning


strategies). Figures 4.2 and 4.3 illustrate the average performance for each evaluation


set (MR, PR, AR, PR-MR, or AR-PR). A small-sample test of the hypothesis (matched


pairs) was conducted on these results. Table 4.8 summarizes the overall averaged results


from 18 experiments, and the bold numbers mean the better performance on each test


set. Based on the KLD metric, the SER system trained with the training set selected


PR _Train_ .


each database. The highest performance for each condition is highlighted in bold. Symbols such as _∗_, _†_, and _⋆_ are used to indicate when a model significantly surpasses the
performance of those trained with MR _Train_, PR _Train_, and AR _Train_, respectively.


Aggregation Hard-label learning Soft-label learning Distributional-label learning


Database (train/test set) MR PR AR PR - MR AR - PR MR PR AR PR - MR AR - PR MR PR AR PR - MR AR - PR





|MRT rain<br>IMPROV(P) PRT rain<br>ART rain|0.512† 0.507† 0.555† 0.300 0.516†<br>0.450 0.448 0.513 0.305 0.465<br>0.562∗† 0.555∗† 0.593∗† 0.335 0.498|0.595 0.587 0.613 0.346 0.530<br>0.600 0.593 0.623 0.341 0.531<br>0.576 0.569 0.602 0.339 0.518|0.612 0.604 0.599 0.401 0.440<br>0.601 0.596 0.590 0.359 0.436<br>0.602 0.594 0.600 0.340 0.441|
|---|---|---|---|
|CREMA-D<br>MR_T rain_<br>PR_T rain_<br>AR_T rain_|0.591<br>0.532<br>0.551<br>0.381<br>0.500<br>**0.600**<br>**0.545**<br>0.595_∗_<br>**0.390**<br>0.572_∗_<br>0.585<br>0.528<br>**0.607**_∗_<br>0.386<br>**0.593**_∗_|0.640<br>0.575<br>0.671<br>0.409<br>0.651<br>0.667<br>0.594<br>0.699_∗_<br>0.416<br>0.688<br>**0.673**<br>**0.615**_∗_<br>**0.710**_∗_<br>**0.444**<br>**0.706**_∗_|0.518_⋆_**0.474**_⋆_<br>0.411<br>**0.357**<br>0.368<br>**0.518**_⋆_0.473_⋆_<br>**0.419**<br>0.357<br>**0.374**<br>0.486<br>0.442<br>0.414<br>0.340<br>0.370|
|PODCAST (P)<br>MR_T rain_<br>PR_T rain_<br>AR_T rain_|0.214_⋆_<br>0.184_⋆_<br>0.303<br>0.143<br>0.300<br>**0.259**_∗⋆_**0.232**_∗⋆_**0.403**_∗⋆_**0.187**_∗⋆_**0.420**_∗⋆_<br>0.192<br>0.166<br>0.330_∗_<br>0.129<br>0.351_∗_|0.215<br>0.185<br>0.326<br>0.145<br>0.328<br>**0.241**_⋆_**0.207**_∗⋆_**0.397**_∗⋆_**0.160**_⋆_<br>**0.408**_∗⋆_<br>0.199<br>0.174<br>0.355_∗_<br>0.138<br>0.367_∗_|0.161<br>0.137<br>0.162<br>0.102<br>0.159<br>0.195_∗_0.166_∗_<br>0.192_∗_<br>0.126_∗_<br>0.184_∗_<br>**0.204**_∗_**0.175**_∗_<br>**0.200**_∗_<br>**0.139**_∗_<br>**0.192**_∗_|
|IEMOCAP<br>MR_T rain_<br>PR_T rain_<br>AR_T rain_|0.269<br>0.260<br>0.339<br>0.203<br>0.351<br>0.259<br>0.254<br>0.345<br>0.186<br>0.355<br>**0.279**<br>**0.268**<br>**0.365**<br>**0.238**_†_<br>**0.378**|0.346<br>0.343<br>0.412<br>0.257<br>0.426<br>0.369<br>0.359<br>0.433<br>**0.279**<br>0.453<br>**0.390**_∗_**0.383**_∗_<br>**0.464**_∗†_ 0.266<br>**0.479**_∗_|0.354<br>0.341<br>0.299<br>0.253<br>0.287<br>**0.377**<br>0.361<br>0.320<br>0.253<br>0.306<br>0.369<br>**0.361**<br>**0.325**_∗_<br>**0.265**<br>**0.317**|
|IMPROV (S)<br>MR_T rain_<br>PR_T rain_<br>AR_T rain_|0.424<br>0.254<br>0.229<br>0.234<br>0.245<br>**0.455**_⋆_<br>**0.340**_∗_<br>0.328_∗_<br>**0.318**_∗_<br>0.360_∗_<br>0.391<br>0.315_∗_<br>**0.337**_∗_<br>0.311_∗_<br>**0.365**_∗_|**0.451**<br>0.299<br>0.379<br>0.278<br>0.386<br>0.433<br>0.353_∗_<br>0.483_∗_<br>0.342_∗_<br>0.505_∗_<br>0.410<br>**0.360**_∗_<br>**0.491**_∗_<br>**0.343**_∗_<br>**0.522**_∗_|0.361<br>0.185<br>0.137<br>0.149<br>0.150<br>0.397<br>0.248_∗_<br>0.181_∗_<br>0.219_∗_<br>0.189_∗_<br>**0.431**_∗_**0.306**_∗†_ **0.216**_∗†_ **0.282**_∗†_ **0.227**_∗†_|
|PODCAST (S)<br>MR_T rain_<br>PR_T rain_<br>AR_T rain_|0.344<br>0.078<br>0.138<br>0.076<br>0.141<br>**0.392**_⋆_<br>0.113_∗_<br>0.327_∗_<br>0.111_∗_<br>0.328_∗_<br>0.283<br>**0.125**_∗_<br>**0.352**_∗†_ **0.124**_∗†_ **0.357**_∗†_|**0.389**_⋆_0.080<br>0.199<br>0.076<br>0.198<br>0.321<br>0.122_∗_<br>0.450_∗_<br>0.122_∗_<br>0.457_∗_<br>0.237<br>**0.139**_∗_<br>**0.457**_∗_<br>**0.142**_∗_<br>**0.466**_∗_|0.352<br>0.051<br>0.060<br>0.047<br>0.059<br>0.412<br>0.076_∗_<br>0.078_∗_<br>0.072_∗_<br>0.074_∗_<br>**0.425**<br>**0.078**_∗_<br>**0.091**_∗†_ **0.075**_∗_<br>**0.088**_∗†_|


43


Table 4.8: The table shows averaged macro-F1 scores across 18 experiments listed in
Table 4.7 and Table 4.6 with different databases and label-learning strategies on the different evaluation sets generated by three rules, _majority rule_ (MR), _plurality rule_ (PR),
and _all-inclusive rule_ (AR). The _↓_ means the lower values mean the higher performance;
the _↑_ is the opposite.


**Metric** **KLD** _↓_ **Macro-F1 Score** _↑_


**Train** _**\**_ **Test** **MR** **PR** **AR** **PR-MR** **AR-PR** **MR** **PR** **AR** **PR-MR** **AR-PR**


**MR** _T rain_ 0.1408 0.1491 0.1512 0.1488 0.1623 0.4082 0.3153 0.3546 0.2309 0.3353
**PR** _T rain_ 0.1406 0.1425 0.1433 0.1382 0.1507 **0.4192** 0.3378 0.4098 0.2524 0.3947
**AR** _T rain_ **0.1404** **0.1397** **0.1402** **0.1334** **0.1461** 0.4052 **0.3418** **0.4172** **0.2576** **0.4019**


and incomplete test data in a cross-corpus setting.


**Assessment on the Complete Test Set (AR)**


When evaluating using the AR approach with all annotated data in the test set, Fig

**Assessment of the Incomplete Test Sets (MR & PR)**


The single-label SER performance was assessed under the MR and PR test con

ditions. As detailed in Table 4.7, testing with the PR set consistently yielded lower


performance than testing with the MR set, as the MR set omits more ambiguous sam

ples. Similarly, performance in the PR-MR condition was generally worse than in the


PR conditions. These results highlight that including more ambiguous samples (lacking


majority consensus) in the test set—common in practical scenarios—can degrade SER


model performance. Therefore, using only PR or MR to define the test set might not ac

curately reflect the outcomes likely to be encountered in real-world deployments where


44


(a) Macro-F1 scores on MR set.


(b) Macro-F1 scores on PR set.


respectively.


Out of the 18 conditions analyzed, Table 4.7 indicates that when tested with the PR


set, training with the _ARTrain_ configuration resulted in the best performance in 11 out of


18 cases (approximately 61%), and 14 out of 18 cases (approximately 78%) when tested


with the AR set. Figure 4.2b presents statistically significant evidence that the average


macro-F1 scores for models trained with _ARTrain_ were superior to those trained with the


_PRTrain_ set. These findings suggest that using the AR approach for training aggregation


may enhance SER performance on samples with lower annotation agreement.


For tests evaluated on the MR condition, models trained with the _ARTrain_ set outper

formed others in only 7 out of 18 experiments (approximately 39%). Figure 4.2a shows


a decline in performance for the _ARTrain_ trained model compared to those trained with


45


either the _MRTrain_ or _PRTrain_ sets.


Including more complex samples in the training set ( _ARTrain_ ) appears to reduce ac

curacy for the most straightforward samples; however, this trade-off bolsters the model’s


resilience in real-world contexts where both ambiguous and unambiguous samples are


commonly encountered. This suggests that training SER systems with the _ARTrain_ set


could be more efficient for real-life applications, reflecting the genuine mix of sam

ple types in practical environments. Additionally, increased training samples with the


_PRTrain_ set displayed better performance than those trained with _MRTrain_, aligning


with findings reported by Chou et al. [18].


**Assessment in Cross-Corpus Scenarios**


corpus includes the additional emotions of surprise, fear, disgust, and contempt, along


with the emotions present in IMPROV (P). Given the emotional overlap, we can per

form this cross-corpus evaluation where a SER model trained with the PODCAST (P)


corpus aims to predict emotions within the IMPROV (P) corpus. Our approach involves


directly utilizing the models trained on the PODCAST (P) corpus and assessing their ef

ficacy on the IMPROV (P) set. We specifically focus on predictions for anger, sadness,


happiness, and the neutral state. We transform the distribution predictions into binary


labels by applying a threshold and then compute the results using the macro F1 score.


For instance, let’s consider a sample prediction for the IMPROV (P) dataset as: (an

gry, sad, happy, surprised, fear, disgusted, contempt, neutral) = (0.2, 0.2, 0.1, 0.1, 0.2,


46


Table 4.9: The table presents the cross-corpus macro-F1 scores for models trained using the 8-class MSP-PODCAST (P) dataset, applied to predict emotions in the 4-class
IMPROV (P) dataset.


Test Set MR PR AR PR-MR AR-PR


MR _T rain_ 0.445 0.441 0.520 0.271 0.506
PR _T rain_ 0.445 0.448 0.521 **0.295** 0.495
AR _T rain_ **0.458** **0.459** **0.523** 0.276 **0.520**


(a) Macro-F1 scores on PR-MR set.


sad, happy, neutral) = (0.2, 0.2, 0.1, 0.1). The next stage involves using the threshold


1 _/C_ =1/8 to convert predictions into a binary form: (1, 1, 0, 0). Assuming the ground


truth of the sample is: (anger, sadness, happiness, neutral) = (0.4, 0.4, 0.1, 0.1). Given


a threshold of 1/4 for the IMPROV (P) corpus, the binary conversion is (1, 1, 0, 0). In


this case, the prediction accuracy equates to 100%.


Table 4.9 presents the macro-F1 scores for cross-corpus testing, generated using the


MR, PR, AR, PR-MR, and AR-PR labels. The results indicate that using the AR _Train_


set for training yields superior performance on the MR, PR, AR, and AR-PR test sets.


This assessment also highlights the presented approach’s efficacy for cross-corpus eval

uations.


47


##### **4.5.3 Evaluation on the Ambiguous Set**

We address the second research question: **is** **the** **performance** **of** **an** **SER** **system**


**on** **ambiguous** **emotions** **enhanced** **when** **trained** **with** **data** **derived** **from** **the** **all-**


**inclusive rule as opposed to data obtained using the majority or plurality rules?**


**Performance on the** _AR −_ _PR_ **Condition**


We examine the results under the _AR −_ _PR_ test condition, which includes only the


samples from the AR dataset that are not part of the PR dataset. As detailed in Table


4.7, models trained with the _MRTrain_ set did not yield the best performances in 17 out


of 18 cases (approximately 94%) when evaluating this condition. In these evaluations,


predicting ambiguous emotions.


Additionally, Figure 4.3 reveals that models trained with the _ARTrain_ set achieve


significantly higher averaged macro-F1 scores compared to those taught with either the


_MRTrain_ set or the _PRTrain_ set on both _AR_ _−_ _PR_ and _PR_ _−_ _MR_ test conditions.


Therefore, we recommend employing the AR approach to select training data for SER


tasks.


**Analysis of the Feature Embeddings**


The goal is to display model embeddings trained with different sentence aggrega

tion methods, as illustrated in Figure 4.4. The investigation utilizes the PODCAST (P)


48


dataset, concentrating on anger, sadness, happiness, and neutral emotions for clearer


visual representation. Our focus is on test set segments with either high or low levels


of agreement—Cohen’s Kappa statistic [94] is used to define high and low agreement


groups. From the test samples, the top 2% showing high agreement is chosen: 21 sam

ples for ”sadness,” 33 for ”anger,” 97 for ”happiness,” and 139 for ”neutral,” as these


are assumed to represent speech with emotional solid consensus.


Additionally, we explore ambiguous cases by selecting the top 2% of test samples


with low agreement, meaning these samples largely lack clear consensus. We analyze


sentences containing a mix of two emotions along with their respective quantities in


brackets: anger-neutral (30), sadness-happiness (18), neutral-happiness (67), and anger

by models trained on the _ARTrain_ and _MRTrain_ sets. For conciseness, analogs for the


_PRTrain_, _AR −_ _PRTrain_, and _PR −_ _MRTrain_ sets are omitted. The T-SNE plots reflect


distinct separations between high-agreement emotions, with the two-emotion complex


Figure 4.4: The figure depicts the procedure of visualizing feature embeddings.


49


(a) anger-neutral,AR _Train_ (b) anger-neutral,MR _Train_


(g) anger-sadness,AR _Train_ (h) anger-sadness,MR _Train_


Figure 4.5: T-SNE visualizations using embeddings generated from models trained
with the MR _Train_ and AR _Train_ sets show the distribution of feature embeddings.
This analysis includes the following emotion pairs: anger-neutral, sadness-happiness,
neutral-happiness, and anger-sadness.


samples often appearing between pure emotions with high agreement.


Comparing embeddings from models trained on the _ARTrain_ versus _MRTrain_ sets,


50


Table 4.10: Silhouette scores for emotional clusters observed in the embeddings are
analyzed. The feature embedding analysis includes the following emotion pairs: angerneutral (ang.-neu.), sadness-happiness (sad.-hap.), neutral-happiness (neu.-hap.), and
anger-sadness (ang.-sad.). The highest silhouette score for each pair is emphasized in
bold.


Case ang.-neu. sad.-hap. neu.-hap. ang.-sad.


MR _T rain_ -0.0366 0.4085 0.0819 0.0819
PR _T rain_ 0.0502 0.3994 0.1291 0.0492
AR _T rain_ **0.0618** **0.4571** **0.1369** 0.1627
AR-PR _T rain_ -0.1371 0.1597 0.0166 0.2695
PR-MR _T rain_ -0.1379 0.17 0.0108 **0.4395**


it is apparent that the _ARTrain_ set offers superior separation between classes, as evi

denced by the centralized labels of emotions in the plots. Further validation comes from


the silhouette score [95], a metric assessing how healthy clusters are formed within the


embedding space (ranging from -1 for poor clustering to +1 for ideal clustering). We


silhouette score for ”anger-neutral,” ”sadness-happiness,” and ”neutral-happiness” clus

ters. Intriguingly, the model trained with _PR −_ _MRTrain_ had the top silhouette score


for the ”anger-sadness” cluster. Generally, models trained on datasets containing more


ambiguous samples are better able to cluster responses to complex emotion scenarios


than models trained solely on the _MRTrain_ engagement.


**Impact of Extra Data Incorporated by the AR Approach**


One advantage of using the _ARTrain_ set is the larger amount of data incorporated


in training, as it utilizes all available samples, unlike the _MRTrain_ or _PRTrain_ sets.


However, this extra data isn’t the only contributor to the effectiveness of this strategy.


51


We performed experiments comparing models trained on datasets of similar size using


both oversampling and undersampling strategies.


For the oversampling approach, we generated synthetic data following the method


proposed by Pappagari et al. [76]. The data generation continued until it matched the


quantity used in the _ARTrain_ set. Table 4.11 presents the results, with the “Real Data”


column indicating the number of data samples in the training set and the “Synthetic


Data” column showing how many utterances were generated as synthetic samples. Ta

ble 4.11 illustrates that the models trained with the _ARTrain_ set consistently outperform


both the ” _MRTrain_ + synthetic data” and ” _PRTrain_ + synthetic data” models, under

scoring the advantage of including additional samples from the _AR −_ _PRTrain_ set in


els under two conditions of uniform size across _MRTrain_, _PRTrain_, and _ARTrain_ . The


first condition included 20,000 randomly chosen training points under their respective


aggregation rules (MR, PR, or AR). The second condition added 12,831 random points


Table 4.11: Analysis of the impact of additional data introduced through the AR approach. The table outlines two strategies: the oversampling approach, which leverages
data augmentation, and the undersampling approach, which involves randomly removing samples to achieve consistency in the dataset.


Experiments Train Real Data Synthetic Data Reduce Data MR PR AR PR-MR AR-PR


MR _T rain_ 32,831 30,245 0 0.217 0.188 0.343 0.145 0.345
Oversampling PR _T rain_ 51,243 11,833 0 0.206 0.178 0.368 0.136 0.368
AR _T rain_ 63,076 0 0 **0.234** **0.211** **0.398** **0.172** **0.407**


MR _T rain_ 32,831 0 0 **0.237** **0.207** 0.366 0.164 0.372
Undersampling PR _T rain_ 32,831 0 18,412 0.214 0.186 0.380 0.142 0.388
AR _T rain_ 32,831 0 30,245 0.227 0.201 **0.387** **0.164** **0.399**


52


to result in 32,831 total samples. These extra points, picked randomly from the rest


of the training set, do not meet consensus criteria. Since not all 32,831 samples have


consensus for MR and PR rules, a soft-label learning strategy was applied. Table 4.12


lists the macro-F1 scores for both conditions, revealing that adding more samples is


consistently beneficial. Notably, the _ARTrain_ models frequently achieved the highest


performance in both conditions (20,000 and 32,831 samples). These findings suggest


that the AR method boosts the performance of SER models by including ambiguous


data, with its benefits extending beyond simply enlarging the training set.

##### **4.5.4 What is the most effective label learning method for SER?**


soft-label learning outperforms hard-label learning. Table 4.7 shows that SER systems


using soft-label learning surpassed those using hard-label learning in 17 out of 18 cases


(around 94%). This finding is consistent with prior studies, which have demonstrated


Table 4.12: The results for the undersampling strategy compare training sets consisting
of either 20,000 samples, following the designated aggregation rules, or 32,831 samples
formed by randomly adding 12,831 samples regardless of consensus. This table shows
results in a macro-F1 score, underscoring the advantages of using the _ARTrain_ set.


Train Set # MR PR AR PR-MR AR-PR


20,000 0.303 0.320 0.317 0.334 0.309
MR _T rain_ 32,831 **0.333** **0.350** **0.349** **0.362** **0.345**


20,000 0.336 0.375 0.377 0.404 0.382
PR _T rain_ 32,831 **0.350** **0.391** **0.394** **0.424** **0.404**


20,000 0.353 0.400 0.402 0.438 0.408
AR _T rain_ 32,831 **0.367** **0.415** **0.418** **0.454** **0.430**


53


(a) Training with MR.


(b) Training with PR.


on the entire test set and aggregated by the AR strategy for each database. We use the
symbols _⊕_, _‡_, and _⋄_ to indicate when a model significantly outperforms those trained
with distributional, soft, and hard-label learning strategies, respectively.


that representing emotions with soft-encoding and employing the CE loss function is a


more effective label learning strategy for training SER models [2,55,57,61,65].


Additionally, Figure 4.7 provides an overview of the macro-F1 scores for each


database, comparing three different label learning methods. We focus solely on the


_AR −_ _PR_ test set for more precise interpretation, as these samples are the most emo

tionally ambiguous. Figures 4.7a (training with MR), 4.7b (training with PL), and 4.7c


(training with AR) demonstrate that the soft-label learning strategy is the most appro

priate method among the existing learning approaches for training SER systems to rec

54


(a) Training with MR.


(b) Training with PR.


tively.


ognize mixed emotions from the ambiguous samples within the _AR −_ _PR_ set.

#### **4.6 Summary**


This paper examined speaker-independent categorical SER systems’ performance


using an all-inclusive test set, where no data was excluded, and our aggregation rule


was applied. Compared to traditional label aggregation methods like the majority rule


and plurality rule, the all-inclusive rule allows for the retention of all annotated data and


emotional ratings, thereby making it possible to train and evaluate SER systems that are


55


tailored to real-world scenarios. The initial examination revealed that adhering to the


majority or plurality rule excludes a notable portion of the annotated test samples, result

ing in a poor representation of expected SER performance in realistic scenarios. In real

world applications, the classifier must recognize emotions in all sentences, regardless of


consensus. Experiments with the comprehensive test set demonstrated that employing


the all-inclusive aggregation rule to define the ground truth yields more reliable SER


performance by incorporating more speech samples with low-agreement annotations.


Our findings also indicated a decline in SER model performance as more ambiguous


samples were included in the test set, highlighting the significance of using the com

plete test set. Additionally, we found that training exclusively with high-agreement data


test sets.


application of the all-inclusive rule to encompass other subjective tasks. Its effective

ness could mainly be assessed in areas like _text-to-speech_ (TTS) and textless _speech-to-_


_speech translation_ (S2ST) systems. For instance, Zhou et al. [96] introduced a system


that synthesizes human voices with mixed emotions; however, the limited range of emo

tions indicates the potential for enhancing emotion embedding. By employing the all

inclusive rule, which utilizes the entire dataset, it is anticipated that more authentic and


varied emotional expressions will be achieved in TTS systems, surpassing current ap

proaches. Moreover, despite its critical role in natural human interaction, present S2ST


systems still need to incorporate emotional information [97, 98]. Acknowledging the


significance of emotions in effective communication, integrating the all-inclusive rule


56


into S2ST systems is believed to significantly enhance their realism in speech conver

sion.


57


# **Chapter 5** **Training Loss by Using Co-occurrence** **Frequency of Emotions**

predict multiple emotional categories. This approach, though, typically neglects the


relationships among different emotions during the training process, treating them in

dependently. This study investigates the interconnected nature of emotional categories


and how these relationships impact the training of SER models. Specifically, the co

occurrence frequencies of emotions are assessed based on perceptual evaluations within


the training data. This information creates a matrix that assigns penalties according


to class dependencies, enforcing harsher penalties for errors between more dissimilar


emotions. This matrix combines three established label learning techniques using the


modified loss function. Subsequently, SER models are developed using both the newly


integrated penalization matrix and the traditional cost functions typically utilized. The


58


newly introduced penalization matrix significantly improves the macro F1-score on the


PODCAST dataset, showing increases of 17.12%, 12.79%, and 25.8% for hard-label,


multi-label, and distribution-label learning methods, respectively.

#### **5.1 Motivation**


SER is crucial for enhancing human-centered computer interactions. Emotional


labels for training SER systems are generally obtained from perceptual evaluations.


Nonetheless, subjectivity in emotion perception leads to interpreting the same speech,


and often the same speech differently [6, 68]. Conventionally, SER studies handle the


variability in emotional annotations as noise, using label aggregation methods to pro

sidering the commonness of emotion co-occurrence in emotional ratings can create bet

ter SER systems.


Examining simultaneous emotions that appear in everyday life [21], Xu et al. [105]


capitalized on the prevalence of concurrent emotions in perceptual assessments to forge


initial linkages within their presented graph-based DNN. Meanwhile, the work [22]


leveraged frequent emotional misclassifications by evaluators to evaluate an SER sys

tem’s performance. Furthermore, some research works have utilized the soft-label


method to capture secondary emotions present in voice [57,61,64]. This body of work


highlights the importance of accounting for feedback from all evaluators in perceptual


evaluations, even when there is variation from agreed-upon labels.


59


This research explores how incorporating emotional co-occurrence data can improve


the training process of a SER system. It involves creating a co-occurrence frequency


matrix that captures the relationships between different emotions as determined by per

ceptual evaluations. This matrix is subsequently converted into a penalization matrix,


which adjusts the loss functions by assigning greater penalties for predicting combi

nations of emotions that seldom occur together. Our approach folds the penalization


matrix into existing cost functions as a ”penalty loss,” thereby increasing the loss value


if the model forecasts emotions with low co-occurrence frequencies. For instance, since


anger and contempt are seldom co-selected in perceptual evaluations, predicting these


two emotions jointly will incur a higher penalty than predicting commonly co-occurring


at maximizing inter-class distance while minimizing intra-class distances. Their find

ings demonstrate the advantages of this approach. Additionally, Zhao [107] introduced


a nearest neighbor contrastive learning technique to emphasize distinctions between


various emotions by leveraging local neighborhood information, which subsequently


boosted SER system performance under cross-corpus testing conditions. Different from


the previously mentioned studies, the frequency of co-occurrence of emotions in the


training set is used by us to model the relationship between emotion classes.


60


##### **5.2.2 Label Learning in Emotion Recognition**

This work explores the application of co-occurrence frequencies of emotional classes


derived from perceptual evaluations to enhance the training process of an SER system. It


examines related methods such as distribution-, hard-, multi-label learning, and emotion


classification. To illustrate, we use a 4-class emotion classification task that includes an

gry (A), neutral (N), happy (H), and sad (S) emotions. In this scenario, five annotators


independently assess a sentence, each assigning one label. For a single sample, an ex

ample set of labels might look like this: ”S, N, S, N, S.”


**Emotion Recognition using Hard-label Learning**


work [18] built each annotator individually to capture the subjective nature of percep

tual evaluations. These approaches permit the inclusion of sentences in the training


dataset even when annotators have differing emotional perceptions. Contrary to sys

tems trained with hard-label learning—which predict a single emotion per utterance and


assume that emotions are independent—these advanced techniques consider emotional


co-occurrence. My findings reveal that adopting the ”penalty loss” method improves


performance.


61


**Emotion Recognition using Multi-label Learning**


Multi-label learning empowers emotion classifiers to detect several emotions in a


single data instance, generating multiple hard vectors that may highlight more than one


emotion. For example, the emotions identified could be represented as (1, 0, 1, 0).


Prominent examples of this approach in emotion recognition are found in studies like


[27, 77, 108]. Although multi-label learning facilitates recording various emotions, it


assumes these emotions manifest independently. This traditional methodology also fails


to signify the relative importance of emotions, such as discerning primary emotions


from secondary ones. In the research, we utilize the approach described by the work


[104], applying multi-label learning to display enhancements in SER systems through


between the actual and predicted distributions. A couple of notable applications of


distribution-label learning to SER include the studies by [90] and [109]. Chou et al.


[90] tailored distribution-label learning by translating emotional ratings into distribution


labels, and we adopted a similar method to train the model. The KLD is typically used


as the loss function in traditional distribution-label learning. Our research examines the


impact of introducing a ”penalty loss” on the accuracy of classification results.


62


Figure 5.1: Illustration of a process for generating the presented penalization matrix.
The 8-class emotions involved include contempt (C), neutral (N), sad (S), happy (H),
fear (F), disgusted (D), angry (A), and surprised (SU). The procedure in detail can be
found in Section 5.3.1.

#### **5.3 Proposed Method**

##### **5.3.1 Penalization Weights based on the Counts of Co-Existing Emo-** **tions**


occurrences, _neutral_ was chosen 14,337 times. Consequently, the entries at positions


(”S”, ”N”) and (”N”, ”S”) are populated with 14,337, respectively.


In phase 2, we create a matrix indicating the probability of co-existing emotions


by dividing each element by the total count of instances marked with the corresponding


emotion in each column. Take the second column labeled ”S” from Fig. 5.1 (b) as an ex

ample—the co-occurrence frequencies of _anger_ with other emotions are 6,331, 18,456,


12,767, 3,613, 6,807, 9,260, 3,835, and 5,796. By dividing each of these frequencies by


the total occurrences of _sad_ (6,331), we obtain co-occurrence probabilities: 0.34, 1.00,


0.37, 0.25, 0.52, 0.77, 0.27, and 0.41. As an example, the co-existing possibility of


disgust and sad (0.37) is greater than that of sad and contempt (0.25). This normalized


63


matrix is termed the co-existing weight matrix (Figure 5.1 (c)), which is asymmetric


owing to the normalization performed column-wise.


In phase 3, the co-occurrence weight matrix converts into a ”penalization matrix.”


This conversion is essential as it penalizes the SER models for forecasting rare emo

tion combinations. The conversion process is simple: Each element in the co-existing


emotion weight matrix is subtracted from one, resulting in the penalization matrix (Fig

ure 5.1 (d)). Employing the method causes an increase in the training loss if the model


predicts infrequent combinations of emotions.

##### **5.3.2 Label Processing to Train SER Systems** **5.3.3 Loss Functions Integrated by the Proposed Penalization Ma-** **trix**


The technique of integrating a penalization matrix into loss functions is proposed.


This method requires the definition of _N × K_ matrices for both the model’s predictions


( _Y_ _[P]_ ) and the actual labels ( _Y_ _[T]_ ). Here, _C_ signifies the number of emotional categories,


while _N_ denotes the number of samples under consideration. The variation in each row


of _Y_ _[T]_ depends on the label learning approach in use, whether it is distribution-, multi-,


or hard-label learning. Afterwards, the loss value matrix ( _L_ _∈_ _R_ _[N]_ _[×][C]_ ) is determined


64


using the following approach:


_L_ = _floss_ ( _Y_ _[T]_ _, Y_ _[P]_ ) (5.1)


The loss function, represented by ( _floss_ ), could be the cross-entropy (CE). The el

ements of ( L ) are calculated as ( _floss_ ( _Y_ _[T]_ _ij, Y_ _[P]_ _ij_ ) ), where ( _j_ _∈_ 1 _, . . ., K_ ) and


( _i_ _∈_ 1 _, . . ., N_ ), to estimate the categorical emotion loss for each utterance. Sub

sequently, the proposed matrix has been incorporated into Equation 5.1. The matrix


introduced, denoted as ( _P_ ), belongs to ( _R_ _[K][×][K]_ ) (refer to Fig. 5.1). The integration of


the loss function is achieved through the penalization matrix, represented by ( _LP_ + _loss_


), as follows:


(5.2)





_LP_ + _BCE_ = _−_





(

_i_ =1



_i_ =1



_z_ =1



_N_




_j_ =1


_C_




_j_ =1



_C_
�( _Pjz · Yij_ _[T]_ _[·]_ [ log(] _[Y]_ _ij_ _[P]_ [)] (5.4)

_z_ =1



+ _Pjz ·_ (1 _−_ _Yij_ _[T]_ [)] _[ ·]_ [ log(1] _[ −]_ _[Y]_ _ij_ _[P]_ [)))] _[,]_



_C_




_LP_ + _KLD_ =



_N_




(

_i_ =1



_j_ =1




- _C_ _Pjz · Yij_ _[T]_ _[·]_ [ log(] _[Y]_ _ij_ _[T]_ )) _._ (5.5)

_z_ =1 _Yij_ _[P]_



In training, the initial loss is modified by the proposed loss, resulting in the total loss


as described by Equation 5.6. In this equation, _α_ _∈_ _R_ and _β_ are assigned a value of


65


either 1 or 0.


_LP_ _[loss]_ = _βLloss_ + _α · LP_ + _loss._ (5.6)

#### **5.4 Experimental Setup**

##### **5.4.1 Resource**


We evaluate the proposed method using the Podcast corpus [39], using version 1.9 in


this ongoing collection effort. The training set consists of 55,283 speech utterances, the


development set includes 9,546, and the test set comprises 16,570 utterances—primary


was assessed across multiple publicly accessible emotional datasets. This analysis iden

tified the wav2vec feature set, introduced by the study [111], as one of the most ro

bust techniques for feature extraction. Consequently, the models incorporate the 512

dimensional wav2vec feature as input. To prepare the data for training, we standardized


all features using z-normalization, which was calculated according to the mean and


standard deviation from the training dataset.

##### **5.4.3 SER Models and Other Details**


We adopted the chunk-level SER models proposed by [112] as the primary model.


This approach systematically processes sentences of varied lengths by converting them


66


into a specified number of uniformly sized chunks through overlapping adjustments.


Based on the paper’s suggestions, we utilized LSTM as the feature encoder at the chunk


level, along with the RNN-AttenVec model for chunk-level attention [112]. This com

bination allows us to capture emotion-related information at different levels. For further


details on the network architecture, see Lin and Busso [112]. Model parameters adhered


to those in Chou et al. [19]. Based on previous studies, for the output layer, we used


softmax activation for CE [99,101,103] and KLD [19,29], with sigmoid activation for


BCE [104, 113]. We used Adam optimizer and set the learning rate to 0 _._ 0001; we set


the batch size to 128. Then, we train all models with the epochs of 25. Finally, we


saved the best-performing model according to their minimum loss on the development


learning, I used macro-, micro-, and weighted-F1 scores, unweighted average recall, and


unweighted average precision. In the case of multi-label and distribution-label learning,


I employ measures similar to those referenced in the study by [113]: ranking and ham

ming loss, coverage error, alongside macro F1. Moreover, micro- and weighted-F1


scores are integrated to estimate multi-label tasks specifically. For a performance as

sessment of multi-label and distribution-label methods, binarization of predictions is


necessary. For multi-label learning, predictions’ probabilities are changed into ”multi

hot” binary vectors using a threshold of 0.5, following [104, 113]’s methodology. For


distribution-label learning, a threshold is fixed at 1/convertingion of probability predic

tions into binary vectors, in line with Chou et al. [19].


67


##### **5.4.5 Statistical Significance**

The methodology from Lin and Busso [112] is employed, where the original test


set is divided at random into 30 smaller subsets of roughly equal size. The average


results for all metrics are then reported. A two-tailed t-test is utilized to conduct the


statistical significance test, evaluating the difference between the proposed approach


and the baseline models. A result is considered statistically significant if the _p_ -value is


less than 0.05.

#### **5.5 Experimental Results and Analyses**


the loss _L_ (with _β_ = 1) was accounted for in the experiments as opposed to excluding


it ( _β_ = 0). The _α_ column states the value assigned to the PL loss weight. Specifically,


the top-performing values for each loss function are emphasized in bold.

##### 5.5.1 Does incorporating the penalty loss ( LP + loss ) benefit SER Sys- **tems?**


Table 5.1 reveals that models utilizing the proposed penalty loss ( _LP_ + _loss_ ) typically


achieve the best outcomes across different label learning strategies. For example, when


the results are evaluated on the single-emotion utterances, the model with _LP_ + _loss_ where


68


Table 5.1: The table overviews the results on distributional-label, multi-hard-label, and
single-label tasks for the primary emotion classification task. The mark _∗_ denotes that
the outcomes for SER systems utilizing the presented matrix have statistical significance
compared to the baseline ( _α_ = 0; _β_ = 1).


**Single-label Task**





|fLoss|β α Unweighted Average Recall ↑Unweighted Average Precision ↑Macro F1 ↑Micro F1 ↑Weighted F1 ↑|
|---|---|
|**CE**|**1 0**<br>0.144<br>0.133<br>0.111<br>0.424<br>0.318|
|**CE**|**1 0.5**<br>**0.156***<br>**0.137***<br>0.129*<br>**0.425**<br>**0.347**<br>**1 1**<br>0.155*<br>0.136<br>**0.130***<br>0.408<br>0.346<br>**0 1**<br>0.154*<br>0.136<br>0.128*<br>0.396<br>0.341|


**Muli-label Task**







|fLoss|β α Hamming Loss ↓ Ranking Loss ↓ Coverage Error↓ Macro F1 ↑Micro F1 ↑Weighted F1 ↑|
|---|---|
|**BCE**|**1 0**<br>0.304<br>0.603<br>6.899<br>0.219<br>0.466<br>0.352|
|**BCE**|**1 0.5**<br>0.303<br>0.608<br>6.928<br>0.215<br>0.462<br>0.348<br>**1 1**<br>**0.303**<br>**0.587**<br>**6.837**<br>0.235<br>**0.482**<br>0.370<br>**0 1**<br>0.305<br>0.597<br>6.871<br>**0.247***<br>0.477<br>**0.378**|


**Distribution-label Task**








|fLoss|β α Hamming Loss ↓ Ranking Loss ↓ Coverage Error↓ Macro F1 ↑Micro F1 ↑Weighted F1 ↑|
|---|---|
|**KLD**|**1 0**<br>**0.294**<br>0.511<br>6.279<br>0.283<br>0.522<br>0.431|
|**KLD**|**1 0.5**<br>0.308<br>**0.507**<br>6.220<br>0.322*<br>**0.533**<br>0.471*<br>**1 1**<br>0.315<br>0.509<br>**6.214**<br>0.330*<br>0.532<br>0.475*<br>**0 1**<br>0.337<br>0.530<br>6.284<br>**0.356***<br>0.526<br>**0.496***|



a remarkable 25.8% relative enhancement over the baseline and surpasses SOTA results


documented by the work [19] (31.6% maF1). This suggests that the presented penalty


loss ( _LP_ + _loss_ ) significantly improves model accuracy in primary emotion classification


tasks. Furthermore, the results exhibit that aggregating the primary loss _Lloss_ with the


presented loss _LP_ + _loss_ tends to boost overall effectiveness.

##### **5.5.2 Effect of Co-occurrence Matrix**


The aim is to determine if the proposed methodology effectively allows systems to


capture the intended co-existing emotions matrix accurately. This is evaluated by mea

suring the distance between the co-existing emotions matrices derived from the learn

69


ing targets in the training set and those obtained from model predictions, utilizing the


Frobenius norm as the distance metric. The focus is on models that use either _LP_ + _loss_


( _α_ = 1; _β_ = 0) or _Lloss_ ( _α_ = 0; _β_ = 1). When _LP_ + _loss_ is implemented, a decrease in


the distance was observed from 4.27 to 4.00 using the multi-label approach and from


4.13 to 3.39 using the distribution-label approach. This reduction signifies that the co

existing emotion matrix, as the proposed penalization method predicted, is more closely


aligned with the target co-occurrence matrix.

#### **5.6 Summary**


This dissertation utilized co-existing emotion counts to create a penalization weight


tion classification tasks.


70


# **Chapter 6** **Conclusion**

This dissertation introduces three proposed methods to optimize the pipeline for


ambiguous utterances with complex emotional perceptions. Adding these minority rat

ings also boosts the performance of SER systems on comprehensive test sets that mirror


real-world conditions. Further analyses reveal that standard approaches, which neglect


these minority ratings, show reduced capabilities in clustering samples with dual emo

tions. Therefore, including the minority of emotional ratings is essential to account for


the subjectivity inherent in emotion perception.


**(2) Should we only let the SER systems learn the emotional perceptions of a few**


**people?** The findings of this dissertation indicate that allowing SER systems to learn


emotion perception from a larger group can enhance recognition capabilities through


the proposed all-inclusive rule or individual-rater modeling method. This not only im

71


proves the performance of SER systems but also offers a unique opportunity for per

sonal growth. By incorporating emotional ratings from a broader range of people, each


person’s unique sensitivity and emotional background can contribute valuable insights.


This should inspire and motivate researchers, developers, and practitioners in the field


of SER to continue their work and strive for excellence.


**(3) Should SER systems only predict one emotion per speech?** To address real

world conditions that involve the simultaneous occurrence of various emotion classes,


SER systems need training to predict multiple emotions simultaneously. This disserta

tion convincingly illustrates that multi-label SER systems can achieve superior perfor

mance on test sets featuring a single consensus label determined by the plurality rule


emotion.


other factors need consideration. For instance, the effect of various inputs, such as hand

crafted features or raw audio signals, on prediction outcomes should have been ana

lyzed. Additionally, the relationships between layer embeddings and label spaces should


be explored. Visualizing these relationships could provide fascinating insights. Further

more, all the suggested methods are designed for traditional SER emotion databases,


while the latest dataset [115] includes intensity scores for each categorical emotion.


Using this type of emotion database might mean our methods must be optimized for


training and evaluating SER systems. It would be intriguing to see if our methods could


be adapted for samples with intensity scores.


Furthermore, the proposed comprehensive rule recommends incorporating all data


72


into the emotion dataset. However, an examination of how the dataset size impacts SER


system performance was not conducted. This omission stems from the fact that the


largest existing emotion dataset comprises merely around 200,000 utterances, signifi

cantly less than databases used in other speech tasks such as Automatic Speech Recog

nition (ASR). Additionally, extensive experiments under cross-domain conditions were


not undertaken, and only a single experiment was performed. It is essential to note that


cross-domain experiments are crucial for real-world application of SER systems.


In conclusion, this dissertation recommends utilizing the original emotion classi

fications within the database. A pertinent question that arises is how many emotion


classes are sufficient to accurately capture emotional perception in real-world scenarios.


posed methods during inference. In future studies, the first benchmark for SER will be


proposed based on the partitions defined in this dissertation, allowing for a standard

ized evaluation of models and easy comparison of performances across different SER


models. The intention is to examine performance disparities caused by natural biases


in emotional perceptions, including gender, race, and ethnicity. Additionally, the im

pact of missing modality on SER system performance will be explored, considering


that real-world conditions might lead to signal loss. Noisy label learning, such as facial


expression recognition [116], is worth investigating to check whether it can be useful


in improving SER systems. Multilingual SER systems will be developed in at least ten


languages due to slight variations in emotion perception across languages, which might


73


offer complementary information to enhance overall system performance. Finally, per

sonalized SER systems will be constructed based on speaker or user profiles to improve


user experience in real-world applications, recognizing that each individual could have


unique emotional responses.


74


# **Bibliography**


[1] S. Mirsamadi, E. Barsoum, and C. Zhang, “Automatic speech emotion recogni

tion using recurrent neural networks with local attention,” in _2017 IEEE Interna-_


_tional Conference on Acoustics, Speech and Signal Processing (ICASSP)_, 2017,


pp. 2227–2231.


_of_ _the_ _40th_ _International_ _Conference_ _on_ _Machine_ _Learning_, ser. Proceedings of


Machine Learning Research, A. Krause, E. Brunskill, K. Cho, B. Engelhardt,


S. Sabato, and J. Scarlett, Eds., vol. 202. PMLR, 23–29 Jul 2023, pp. 28 492–


28 518. [Online]. Available: [https://proceedings.mlr.press/v202/radford23a.html](https://proceedings.mlr.press/v202/radford23a.html)


[4] S. Communication, L. Barrault, Y.-A. Chung, M. C. Meglioli, D. Dale, N. Dong,


M. Duppenthaler, P.-A. Duquenne, B. Ellis, H. Elsahar, J. Haaheim, J. Hoffman,


M.-J. Hwang, H. Inaguma, C. Klaiber, I. Kulikov, P. Li, D. Licht, J. Maillard,


R. Mavlyutov, A. Rakotoarison, K. R. Sadagopan, A. Ramakrishnan, T. Tran,


G. Wenzek, Y. Yang, E. Ye, I. Evtimov, P. Fernandez, C. Gao, P. Hansanti,


75


E. Kalbassi, A. Kallet, A. Kozhevnikov, G. M. Gonzalez, R. S. Roman,


C. Touret, C. Wong, C. Wood, B. Yu, P. Andrews, C. Balioglu, P.-J. Chen, M. R.


Costa-juss`a, M. Elbayad, H. Gong, F. Guzm´an, K. Heffernan, S. Jain, J. Kao,


A. Lee, X. Ma, A. Mourachko, B. Peloquin, J. Pino, S. Popuri, C. Ropers,


S. Saleem, H. Schwenk, A. Sun, P. Tomasello, C. Wang, J. Wang, S. Wang,


and M. Williamson, “Seamless: Multilingual Expressive and Streaming Speech


Translation,” 2023. [Online]. Available: [https://arxiv.org/abs/2312.05187](https://arxiv.org/abs/2312.05187)


[5] L. F. Parra-Gallego and J. R. Orozco-Arroyave, “Classification of emotions and


evaluation of customer satisfaction from speech in real world acoustic environ

ments,” _Digital_ _Signal_ _Processing_, vol. 120, p. 103286, 2022. [Online]. Avail

_in_ _Cognitive_ _Sciences_, vol. 25, no. 2, pp. 124–136, 2021. [Online]. Available:


[https://www.sciencedirect.com/science/article/pii/S136466132030276X](https://www.sciencedirect.com/science/article/pii/S136466132030276X)


[8] J. A. Hall and D. Matsumoto, “Gender differences in judgments of


multiple emotions from facial expressions,” _Emotion_ _(Washington,_ _D.C.)_,


vol. 4, no. 2, p. 201—206, June 2004. [Online]. Available: [https:](https://doi.org/10.1037/1528-3542.4.2.201)


[//doi.org/10.1037/1528-3542.4.2.201](https://doi.org/10.1037/1528-3542.4.2.201)


[9] D. Matsumoto, “American-Japanese Cultural Differences in the Recognition


of Universal Facial Expressions,” _Journal_ _of_ _Cross-Cultural_ _Psychology_,


76


vol. 23, no. 1, pp. 72–84, 1992. [Online]. Available: [https://doi.org/10.1177/](https://doi.org/10.1177/0022022192231005)


[0022022192231005](https://doi.org/10.1177/0022022192231005)


[10] A. Suzuki, T. Hoshino, K. Shigemasu, and M. Kawamura, “Decline or


improvement?: Age-related differences in facial expression recognition,”


_Biological_ _Psychology_, vol. 74, no. 1, pp. 75–84, 2007. [Online]. Available:


[https://www.sciencedirect.com/science/article/pii/S0301051106001669](https://www.sciencedirect.com/science/article/pii/S0301051106001669)


[11] J. A. Russell, “Core affect and the psychological construction of emotion,”


_Psychological_ _review_, vol. 110, no. 1, p. 145—172, January 2003. [Online].


Available: [https://doi.org/10.1037/0033-295x.110.1.145](https://doi.org/10.1037/0033-295x.110.1.145)


cultures,” _Nature human behaviour_, vol. 3, no. 4, pp. 369–382, 2019.


[14] L. Goncalves and C. Busso, “AuxFormer: Robust Approach to Audiovisual Emo

tion Recognition,” in _ICASSP_ _2022_ _-_ _2022_ _IEEE_ _International_ _Conference_ _on_


_Acoustics, Speech and Signal Processing (ICASSP)_, 2022, pp. 7357–7361.


[15] J. Almeida, L. Vilac¸a, I. N. Teixeira, and P. Viana, “Emotion Identification


in Movies through Facial Expression Recognition,” _Applied_ _Sciences_, vol. 11,


[no. 15, 2021. [Online]. Available: https://www.mdpi.com/2076-3417/11/15/6827](https://www.mdpi.com/2076-3417/11/15/6827)


[16] J. S. G´omez-Ca˜n´on, E. Cano, Y.-H. Yang, P. Herrera, and E. Gomez, “Let’s


agree to disagree: Consensus Entropy Active Learning for Personalized Music


77


Emotion Recognition,” in _Proceedings_ _of_ _the_ _22nd_ _International_ _Society_ _for_


_Music_ _Information_ _Retrieval_ _Conference_ . ISMIR, Oct. 2021, pp. 237–245.


[Online]. Available: [https://doi.org/10.5281/zenodo.5624399](https://doi.org/10.5281/zenodo.5624399)


[17] J. S. G´omez-Ca˜n´on, E. Cano, T. Eerola, P. Herrera, X. Hu, Y.-H. Yang, and


E. G´omez, “Music Emotion Recognition: Toward new, robust standards in per

sonalized and context-sensitive applications,” _IEEE Signal Processing Magazine_,


vol. 38, no. 6, pp. 106–114, 2021.


[18] H.-C. Chou and C.-C. Lee, “Every Rating Matters: Joint Learning of Subjective


Labels and Individual Annotators for Speech Emotion Classification,” in _ICASSP_


[20] S. Parthasarathy and C. Busso, “Semi-Supervised Speech Emotion Recognition


With Ladder Networks,” _IEEE/ACM_ _Transactions_ _on_ _Audio,_ _Speech,_ _and_ _Lan-_


_guage Processing_, vol. 28, pp. 2697–2709, 2020.


[21] K. Vansteelandt, I. Van Mechelen, and J. B. Nezlek, “The co-occurrence


of emotions in daily life: A multilevel approach,” _Journal_ _of_ _Research_


_in_ _Personality_, vol. 39, no. 3, pp. 325–335, 2005. [Online]. Available:


[https://www.sciencedirect.com/science/article/pii/S0092656604000431](https://www.sciencedirect.com/science/article/pii/S0092656604000431)


[22] S. Steidl, M. Levit, A. Batliner, E. Noth, and H. Niemann, “”Of all things the


measure is man” automatic classification of emotions and inter-labeler consis

tency [speech-based emotion recognition],” in _Proceedings. (ICASSP ’05). IEEE_


78


_International_ _Conference_ _on_ _Acoustics,_ _Speech,_ _and_ _Signal_ _Processing,_ _2005._,


vol. 1, 2005, pp. I/317–I/320 Vol. 1.


[23] D. Zhang, X. Ju, J. Li, S. Li, Q. Zhu, and G. Zhou, “Multi-modal Multi-label


Emotion Detection with Modality and Label Dependence,” in _Proceedings_ _of_


_the_ _2020_ _Conference_ _on_ _Empirical_ _Methods_ _in_ _Natural_ _Language_ _Processing_


_(EMNLP)_, B. Webber, T. Cohn, Y. He, and Y. Liu, Eds. Online: Association


for Computational Linguistics, Nov. 2020, pp. 3584–3593. [Online]. Available:


[https://aclanthology.org/2020.emnlp-main.291](https://aclanthology.org/2020.emnlp-main.291)


[24] X. Kang, X. Shi, Y. Wu, and F. Ren, “Active Learning With Complementary


[26] X. Ju, D. Zhang, J. Li, and G. Zhou, “Transformer-based Label Set Generation


for Multi-modal Multi-label Emotion Detection,” in _Proceedings_ _of_ _the_ _28th_


_ACM_ _International_ _Conference_ _on_ _Multimedia_, ser. MM ’20. New York,


NY, USA: Association for Computing Machinery, 2020, p. 512–520. [Online].


Available: [https://doi.org/10.1145/3394171.3413577](https://doi.org/10.1145/3394171.3413577)


[27] D. Zhang, X. Ju, W. Zhang, J. Li, S. Li, Q. Zhu, and G. Zhou, “Multi-modal


Multi-label Emotion Recognition with Heterogeneous Hierarchical Message


Passing,” _Proceedings_ _of_ _the_ _AAAI_ _Conference_ _on_ _Artificial_ _Intelligence_,


vol. 35, no. 16, pp. 14 338–14 346, May 2021. [Online]. Available:


[https://ojs.aaai.org/index.php/AAAI/article/view/17686](https://ojs.aaai.org/index.php/AAAI/article/view/17686)


79


[28] S. Li and W. Deng, “Blended Emotion in-the-Wild: Multi-label Facial


Expression Recognition Using Crowdsourced Annotations and Deep Locality


Feature Learning,” _Int._ _J._ _Comput._ _Vision_, vol. 127, no. 6–7, p. 884–906, jun


2019. [Online]. Available: [https://doi.org/10.1007/s11263-018-1131-1](https://doi.org/10.1007/s11263-018-1131-1)


[29] X. Geng, “Label Distribution Learning,” _IEEE_ _Transactions_ _on Knowledge_ _and_


_Data Engineering_, vol. 28, no. 7, pp. 1734–1748, 2016.


[30] Y. Zhou, H. Xue, and X. Geng, “Emotion Distribution Recognition from


Facial Expressions,” in _Proceedings_ _of_ _the_ _23rd_ _ACM_ _International_ _Conference_


_on_ _Multimedia_, ser. MM ’15. New York, NY, USA: Association for


[32] G. N. Yannakakis, R. Cowie, and C. Busso, “The ordinal nature of emotions,” in


_2017_ _Seventh_ _International_ _Conference_ _on_ _Affective_ _Computing_ _and_ _Intelligent_


_Interaction (ACII)_, 2017, pp. 248–255.


[33] ——, “The Ordinal Nature of Emotions: An Emerging Approach,” _IEEE Trans-_


_actions on Affective Computing_, vol. 12, no. 1, pp. 16–35, 2021.


[34] R. A. Martin, G. E. Berry, T. Dobranski, M. Horne, and P. G. Dodgson, “Emotion


Perception Threshold: Individual Differences in Emotional Sensitivity,” _Journal_


_of Research in Personality_, vol. 30, no. 2, pp. 290–305, 1996. [Online]. Available:


[https://www.sciencedirect.com/science/article/pii/S0092656696900197](https://www.sciencedirect.com/science/article/pii/S0092656696900197)


80


[35] H. Alhuzali and S. Ananiadou, “SpanEmo: Casting Multi-label Emotion


Classification as Span-prediction,” in _Proceedings_ _of_ _the_ _16th_ _Conference_ _of_


_the_ _European_ _Chapter_ _of_ _the_ _Association_ _for_ _Computational_ _Linguistics:_ _Main_


_Volume_, P. Merlo, J. Tiedemann, and R. Tsarfaty, Eds. Online: Association


for Computational Linguistics, Apr. 2021, pp. 1573–1584. [Online]. Available:


[https://aclanthology.org/2021.eacl-main.135](https://aclanthology.org/2021.eacl-main.135)


[36] C.-K. Yeh, W.-C. Wu, W.-J. Ko, and Y.-C. F. Wang, “Learning Deep Latent


Space for Multi-Label Classification,” _Proceedings_ _of_ _the_ _AAAI_ _Conference_


_on_ _Artificial_ _Intelligence_, vol. 31, no. 1, Feb. 2017. [Online]. Available:


[https://ojs.aaai.org/index.php/AAAI/article/view/10769](https://ojs.aaai.org/index.php/AAAI/article/view/10769)


_(LREC’14)_, N. Calzolari, K. Choukri, T. Declerck, H. Loftsson, B. Maegaard,


J. Mariani, A. Moreno, J. Odijk, and S. Piperidis, Eds. Reykjavik, Iceland:


European Language Resources Association (ELRA), May 2014, pp. 859–


866. [Online]. Available: [http://www.lrec-conf.org/proceedings/lrec2014/pdf/](http://www.lrec-conf.org/proceedings/lrec2014/pdf/497_Paper.pdf)


497 ~~P~~ [aper.pdf](http://www.lrec-conf.org/proceedings/lrec2014/pdf/497_Paper.pdf)


[39] R. Lotfian and C. Busso, “Building Naturalistic Emotionally Balanced Speech


Corpus by Retrieving Emotional Speech from Existing Podcast Recordings,”


_IEEE Transactions on Affective Computing_, vol. 10, no. 4, pp. 471–483, 2019.


81


[40] Z. Waseem, “Are You a Racist or Am I Seeing Things? Annotator Influence


on Hate Speech Detection on Twitter,” in _Proceedings_ _of_ _the_ _First_ _Workshop_


_on_ _NLP_ _and_ _Computational_ _Social_ _Science_, D. Bamman, A. S. Do˘gru¨oz,


J. Eisenstein, D. Hovy, D. Jurgens, B. O’Connor, A. Oh, O. Tsur, and S. Volkova,


Eds. Austin, Texas: Association for Computational Linguistics, Nov. 2016, pp.


138–142. [Online]. Available: [https://aclanthology.org/W16-5618](https://aclanthology.org/W16-5618)


[41] A. M. Davani, M. D´ıaz, and V. Prabhakaran, “Dealing with Disagreements:


Looking Beyond the Majority Vote in Subjective Annotations,” _Transactions_ _of_


_the_ _Association_ _for_ _Computational_ _Linguistics_, vol. 10, pp. 92–110, 01 2022.


[Online]. Available: [https://doi.org/10.1162/tacl](https://doi.org/10.1162/tacl_a_00449) ~~a~~ ~~0~~ 0449


[43] M. Sandri, E. Leonardelli, S. Tonelli, and E. Jezek, “Why Don’t You Do


It Right? Analysing Annotators’ Disagreement in Subjective Tasks,” in


_Proceedings of the 17th Conference of the European Chapter of the Association_


_for Computational Linguistics_, A. Vlachos and I. Augenstein, Eds. Dubrovnik,


Croatia: Association for Computational Linguistics, May 2023, pp. 2428–2441.


[Online]. Available: [https://aclanthology.org/2023.eacl-main.178](https://aclanthology.org/2023.eacl-main.178)


[44] S. Oluyemi, B. Neuendorf, J. Plepi, L. Flek, J. Schl¨otterer, and C. Welch,


“Corpus Considerations for Annotator Modeling and Scaling,” in _Proceedings_


_of_ _the_ _2024_ _Conference_ _of_ _the_ _North_ _American_ _Chapter_ _of_ _the_ _Association_ _for_


_Computational_ _Linguistics:_ _Human_ _Language_ _Technologies_ _(Volume_ _1:_ _Long_


82


_Papers)_, K. Duh, H. Gomez, and S. Bethard, Eds. Mexico City, Mexico:


Association for Computational Linguistics, Jun. 2024, pp. 1029–1040. [Online].


Available: [https://aclanthology.org/2024.naacl-long.59](https://aclanthology.org/2024.naacl-long.59)


[45] L. Martinez-Lucas, A. Salman, S.-G. Leem, S. G. Upadhyay, C.-C. Lee, and


C. Busso, “Analyzing the Effect of Affective Priming on Emotional Annotations,”


in _2023 11th International Conference on Affective Computing and Intelligent In-_


_teraction (ACII)_, 2023, pp. 1–8.


[46] C. Hube, B. Fetahu, and U. Gadiraju, “Understanding and Mitigating Worker


Biases in the Crowdsourced Collection of Subjective Judgments,” in _Proceedings_


[48] N. Antoniou, A. Katsamanis, T. Giannakopoulos, and S. Narayanan, “Designing


and Evaluating Speech Emotion Recognition Systems: A Reality Check Case


Study with IEMOCAP,” in _ICASSP 2023 - 2023 IEEE International Conference_


_on Acoustics, Speech and Signal Processing (ICASSP)_, 2023, pp. 1–5.


[49] C. Busso, S. Parthasarathy, A. Burmania, M. AbdelWahab, N. Sadoughi, and


E. M. Provost, “MSP-IMPROV: An Acted Corpus of Dyadic Interactions to


Study Emotion Perception,” _IEEE_ _Transactions_ _on_ _Affective_ _Computing_, vol. 8,


no. 1, pp. 67–80, 2017.


83


[50] A. Burmania, S. Parthasarathy, and C. Busso, “Increasing the Reliability of


Crowdsourcing Evaluations Using Online Quality Assessment,” _IEEE_ _Transac-_


_tions on Affective Computing_, vol. 7, no. 4, pp. 374–388, 2016.


[51] H. Cao, D. G. Cooper, M. K. Keutmann, R. C. Gur, A. Nenkova, and R. Verma,


“CREMA-D: Crowd-Sourced Emotional Multimodal Actors Dataset,” _IEEE_


_Transactions on Affective Computing_, vol. 5, no. 4, pp. 377–390, 2014.


[52] E. Mower, A. Metallinou, C.-C. Lee, A. Kazemzadeh, C. Busso, S. Lee, and


S. Narayanan, “Interpreting ambiguous emotional expressions,” in _2009 3rd In-_


_ternational_ _Conference_ _on_ _Affective_ _Computing_ _and_ _Intelligent_ _Interaction_ _and_


_and Intelligent Interaction (ACII)_, 2015, pp. 553–559.


[55] J. Han, Z. Zhang, M. Schmitt, M. Pantic, and B. Schuller, “From Hard


to Soft: Towards more Human-like Emotion Recognition by Modelling


the Perception Uncertainty,” in _Proceedings_ _of_ _the_ _25th_ _ACM_ _International_


_Conference_ _on_ _Multimedia_, ser. MM ’17. New York, NY, USA: Association


for Computing Machinery, 2017, p. 890–897. [Online]. Available: [https:](https://doi.org/10.1145/3123266.3123383)


[//doi.org/10.1145/3123266.3123383](https://doi.org/10.1145/3123266.3123383)


[56] Y. Yan, R. Rosales, G. Fung, M. Schmidt, G. Hermosillo, L. Bogoni, L. Moy,


and J. Dy, “Modeling annotator expertise: Learning when everybody knows a


bit of something,” in _Proceedings_ _of_ _the_ _Thirteenth_ _International_ _Conference_


84


_on_ _Artificial_ _Intelligence_ _and_ _Statistics_, ser. Proceedings of Machine Learning


Research, Y. W. Teh and M. Titterington, Eds., vol. 9. Chia Laguna Resort,


Sardinia, Italy: PMLR, 13–15 May 2010, pp. 932–939. [Online]. Available:


[https://proceedings.mlr.press/v9/yan10a.html](https://proceedings.mlr.press/v9/yan10a.html)


[57] H. Fayek, M. Lech, and L. Cavedon, “Modeling subjectiveness in emotion recog

nition with deep neural networks: Ensembles vs soft labels,” in _2016_ _Interna-_


_tional Joint Conference on Neural Networks (IJCNN)_, 2016, pp. 566–570.


[58] B. Zhang, Y. Kong, G. Essl, and E. M. Provost, “f-similarity preservation


loss for soft labels: A demonstration on cross-corpus speech emotion


[https://doi.org/10.1145/1873951.1874246](https://doi.org/10.1145/1873951.1874246)


[60] D. Kingma and J. Ba, “Adam: A Method for Stochastic Optimization,” in _Inter-_


_national Conference on Learning Representations (ICLR)_, San Diega, CA, USA,


2015.


[61] R. Lotfian and C. Busso, “Formulating emotion perception as a probabilis

tic model with application to categorical emotion classification,” in _2017_ _Sev-_


_enth International Conference on Affective Computing and Intelligent Interaction_


_(ACII)_, 2017, pp. 415–420.


85


[62] Y. Kim and J. Kim, “Human-Like Emotion Recognition: Multi-Label Learning


from Noisy Labeled Audio-Visual Expressive Speech,” in _2018_ _IEEE_ _Interna-_


_tional Conference on Acoustics, Speech and Signal Processing (ICASSP)_, 2018,


pp. 5104–5108.


[63] A. Ando, R. Masumura, H. Kamiyama, S. Kobashikawa, and Y. Aono, “Speech


Emotion Recognition Based on Multi-Label Emotion Existence Model,” in _Proc._


_Interspeech 2019_, 2019, pp. 2818–2822.


[64] K. Sridhar, W.-C. Lin, and C. Busso, “Generative Approach Using Soft-Labels to


Learn Uncertainty in Predicting Emotional Attributes,” in _2021 9th International_


1–8.


[66] L. Devillers, L. Vidrascu, and L. Lamel, “Challenges in real-life emotion


annotation and machine learning based detection,” _Neural_ _Networks_, vol. 18,


no. 4, pp. 407–422, 2005, emotion and Brain. [Online]. Available:


[https://www.sciencedirect.com/science/article/pii/S0893608005000407](https://www.sciencedirect.com/science/article/pii/S0893608005000407)


[67] E. Mower, M. J. Mataric, and S. Narayanan, “Human Perception of Audio-Visual


Synthetic Character Emotion Expression in the Presence of Ambiguous and Con

flicting Information,” _IEEE Transactions on Multimedia_, vol. 11, no. 5, pp. 843–


855, 2009.


86


[68] V. Sethu, E. M. Provost, J. Epps, C. Busso, N. Cummins, and S. Narayanan, “The


ambiguous world of emotion representation,” _ArXiv e-prints (arXiv:1909.00360)_,


pp. 1–19, May 2019.


[69] C. Busso and S. S. Narayanan, “Scripted dialogs versus improvisation: lessons


learned about emotional elicitation techniques from the IEMOCAP database,” in


_Proc. Interspeech 2008_, 2008, pp. 1670–1673.


[70] H. M. Fayek, M. Lech, and L. Cavedon, “Evaluating deep learning architectures


for Speech Emotion Recognition,” _Neural_ _Networks_, vol. 92, pp. 60–68, 2017,


advances in Cognitive Engineering Using Neural Networks. [Online]. Available:


[72] S. Mekruksavanich, A. Jitpattanakul, and N. Hnoohom, “Negative Emotion


Recognition using Deep Learning for Thai Language,” in _2020_ _Joint_ _Interna-_


_tional_ _Conference_ _on_ _Digital_ _Arts,_ _Media_ _and_ _Technology_ _with_ _ECTI_ _Northern_


_Section_ _Conference_ _on_ _Electrical,_ _Electronics,_ _Computer_ _and_ _Telecommunica-_


_tions Engineering (ECTI DAMT & NCON)_, 2020, pp. 71–74.


[73] B. Mocanu, R. Tapu, and T. Zaharia, “Utterance Level Feature Aggregation


with Deep Metric Learning for Speech Emotion Recognition,” _Sensors_, vol. 21,


[no. 12, 2021. [Online]. Available: https://www.mdpi.com/1424-8220/21/12/4233](https://www.mdpi.com/1424-8220/21/12/4233)


[74] M. Neumann and N. T. Vu, “Improving Speech Emotion Recognition with Un

supervised Representation Learning on Unlabeled Speech,” in _ICASSP_ _2019_ _-_


87


_2019_ _IEEE_ _International_ _Conference_ _on_ _Acoustics,_ _Speech_ _and_ _Signal_ _Process-_


_ing (ICASSP)_, 2019, pp. 7390–7394.


[75] L. Goncalves and C. Busso, “Improving Speech Emotion Recognition Using


Self-Supervised Learning with Domain-Specific Audiovisual Tasks,” in _Proc. In-_


_terspeech 2022_, 2022, pp. 1168–1172.


[76] R. Pappagari, J. Villalba, P. Zelasko, L. Moro-Velazquez, and N. Dehak, “Copy- [˙]


paste: An augmentation method for speech emotion recognition,” in _ICASSP_


_2021_ _-_ _2021_ _IEEE_ _International_ _Conference_ _on_ _Acoustics,_ _Speech_ _and_ _Signal_


_Processing (ICASSP)_, 2021, pp. 6324–6328.


wards a Comprehensive Evaluation of Speech Emotion Recognition Systems,” in


_Workshop_ _on_ _Speech,_ _Music_ _and_ _Mind_ _(SMM_ _2019)_, Graz, Austria, September


2019, pp. 11–15.


[79] R. Lotfian and C. Busso, “Curriculum Learning for Speech Emotion Recognition


From Crowdsourced Labels,” _IEEE/ACM_ _Transactions_ _on_ _Audio,_ _Speech,_ _and_


_Language Processing_, vol. 27, no. 4, pp. 815–826, 2019.


[80] L. Yang, Y. Shen, Y. Mao, and L. Cai, “Hybrid Curriculum Learning for Emotion


Recognition in Conversation,” _Proceedings of the AAAI Conference on Artificial_


_Intelligence_, vol. 36, no. 10, pp. 11 595–11 603, Jun. 2022. [Online]. Available:


[https://ojs.aaai.org/index.php/AAAI/article/view/21413](https://ojs.aaai.org/index.php/AAAI/article/view/21413)


88


[81] J. Li, X. Wang, Y. Liu, and Z. Zeng, “ERNetCL: A novel emotion recognition


network in textual conversation based on curriculum learning strategy,”


_Knowledge-Based_ _Systems_, vol. 286, p. 111434, 2024. [Online]. Available:


[https://www.sciencedirect.com/science/article/pii/S0950705124000698](https://www.sciencedirect.com/science/article/pii/S0950705124000698)


[82] A. Baevski, Y. Zhou, A. Mohamed, and M. Auli, “wav2vec 2.0: A Framework


for Self-Supervised Learning of Speech Representations,” in _Advances_ _in_


_Neural Information Processing Systems_, H. Larochelle, M. Ranzato, R. Hadsell,


M. Balcan, and H. Lin, Eds., vol. 33. Curran Associates, Inc., 2020, pp.


12 449–12 460. [Online]. Available: [https://proceedings.neurips.cc/paper](https://proceedings.neurips.cc/paper_files/paper/2020/file/92d1e1eb1cd6f9fba3227870bb6d7f07-Paper.pdf) ~~f~~ iles/


[paper/2020/file/92d1e1eb1cd6f9fba3227870bb6d7f07-Paper.pdf](https://proceedings.neurips.cc/paper_files/paper/2020/file/92d1e1eb1cd6f9fba3227870bb6d7f07-Paper.pdf)


[84] J. Wagner, A. Triantafyllopoulos, H. Wierstorf, M. Schmitt, F. Burkhardt, F. Ey

ben, and B. W. Schuller, “Dawn of the Transformer Era in Speech Emotion


Recognition: Closing the Valence Gap,” _IEEE_ _Transactions_ _on_ _Pattern_ _Analy-_


_sis and Machine Intelligence_, vol. 45, no. 9, pp. 10 745–10 759, 2023.


[85] W.-N. Hsu, A. Sriram, A. Baevski, T. Likhomanenko, Q. Xu, V. Pratap, J. Kahn,


A. Lee, R. Collobert, G. Synnaeve, and M. Auli, “Robust wav2vec 2.0: Analyz

ing Domain Shift in Self-Supervised Pre-Training,” in _Proc._ _Interspeech_ _2021_,


2021, pp. 721–725.


89


[86] T. Wolf, L. Debut, V. Sanh, J. Chaumond, C. Delangue, A. Moi, P. Cistac,


T. Rault, R. Louf, M. Funtowicz, J. Davison, S. Shleifer, P. von Platen, C. Ma,


Y. Jernite, J. Plu, C. Xu, T. Le Scao, S. Gugger, M. Drame, and Q. L. amd


A.M. Rush, “HuggingFace’s transformers: State-of-the-art natural language pro

cessing,” _ArXiv e-prints (arXiv:1910.03771v5)_, pp. 1–8, October 2019.


[87] D. Kingma and J. Ba, “Adam: A method for stochastic optimization,” in _Inter-_


_national_ _Conference_ _on_ _Learning_ _Representations_, San Diego, CA, USA, May


2015, pp. 1–13.


[88] A. Paszke, S. Gross, F. Massa, A. Lerer, J. Bradbury, G. Chanan, T. Killeen,


_ference on Computer Vision and Pattern Recognition (CVPR)_, June 2016.


[90] H.-C. Chou, C.-C. Lee, and C. Busso, “Exploiting Co-occurrence Frequency of


Emotions in Perceptual Evaluations To Train A Speech Emotion Classifier,” in


_Proc. Interspeech 2022_, 2022, pp. 161–165.


[91] Y. Li, T. Zhao, and T. Kawahara, “Improved End-to-End Speech Emotion Recog

nition Using Self Attention Mechanism and Multitask Learning,” in _Proc. Inter-_


_speech 2019_, 2019, pp. 2803–2807.


[92] L. Pepino, P. Riera, and L. Ferrer, “Emotion Recognition from Speech Using


wav2vec 2.0 Embeddings,” in _Proc. Interspeech 2021_, 2021, pp. 3400–3404.


90


[93] F. Eyben, K. R. Scherer, B. W. Schuller, J. Sundberg, E. Andr´e, C. Busso, L. Y.


Devillers, J. Epps, P. Laukka, S. S. Narayanan, and K. P. Truong, “The Geneva


Minimalistic Acoustic Parameter Set (GeMAPS) for Voice Research and Affec

tive Computing,” _IEEE_ _Transactions_ _on_ _Affective_ _Computing_, vol. 7, no. 2, pp.


190–202, 2016.


[94] J. Cohen, “A coefficient of agreement for nominal scales,” _Educational and psy-_


_chological measurement_, vol. 20, no. 1, pp. 37–46, 1960.


[95] P. J. Rousseeuw, “Silhouettes: A graphical aid to the interpretation and


validation of cluster analysis,” _Journal_ _of_ _Computational_ _and_ _Applied_


Y. Adi, J. Pino, J. Gu, and W.-N. Hsu, “Textless Speech-to-Speech Translation


on Real Data,” in _Proceedings_ _of_ _the_ _2022_ _Conference_ _of_ _the_ _North_ _American_


_Chapter_ _of_ _the_ _Association_ _for_ _Computational_ _Linguistics:_ _Human_ _Language_


_Technologies_, M. Carpuat, M.-C. de Marneffe, and I. V. Meza Ruiz, Eds.


Seattle, United States: Association for Computational Linguistics, Jul. 2022, pp.


860–872. [Online]. Available: [https://aclanthology.org/2022.naacl-main.63](https://aclanthology.org/2022.naacl-main.63)


[98] X. Li, Y. Jia, and C.-C. Chiu, “Textless Direct Speech-to-Speech Translation with


Discrete Speech Representation,” in _ICASSP_ _2023_ _-_ _2023_ _IEEE_ _International_


_Conference on Acoustics, Speech and Signal Processing (ICASSP)_, 2023, pp. 1–


5.


91


[99] Q. Jin, C. Li, S. Chen, and H. Wu, “Speech emotion recognition with acoustic and


lexical features,” in _2015_ _IEEE_ _International_ _Conference_ _on_ _Acoustics,_ _Speech_


_and Signal Processing (ICASSP)_, 2015, pp. 4749–4753.


[100] S. Parthasarathy and C. Busso, “Ladder Networks for Emotion Recognition:


Using Unsupervised Auxiliary Tasks to Improve Predictions of Emotional At

tributes,” in _Interspeech_ _2018_, Hyderabad, India, September 2018, pp. 3698–


3702.


[101] Z. Aldeneh and E. Mower Provost, “Using regional saliency for speech emotion


recognition,” in _IEEE International Conference on Acoustics, Speech and Signal_


2745.


pp. 5084–5088.


[103] S. Yoon, S. Byun, S. Dey, and K. Jung, “Speech Emotion Recognition Using


Multi-hop Attention Mechanism,” in _ICASSP_ _2019_ _-_ _2019_ _IEEE_ _International_


_Conference_ _on_ _Acoustics,_ _Speech_ _and_ _Signal_ _Processing_ _(ICASSP)_, 2019, pp.


2822–2826.


[104] X. Kang, X. Shi, Y. Wu, and F. Ren, “Active Learning With Complementary


Sampling for Instructing Class-Biased Multi-Label Text Emotion Classification,”


_IEEE Transactions on Affective Computing_, vol. 14, no. 1, pp. 523–536, 2023.


[105] P. Xu, Z. Liu, G. I. Winata, Z. Lin, and P. Fung, “EmoGraph: Capturing Emotion


Correlations using Graph Networks,” _CoRR_, vol. abs/2008.09378, 2020.


92


[106] X. Wang, S. Zhao, and Y. Qin, “Supervised Contrastive Learning with Near

est Neighbor Search for Speech Emotion Recognition,” in _Proc. INTERSPEECH_


_2023_, 2023, pp. 1913–1917.


[107] Y. Zhao, J. Wang, C. Lu, S. Li, B. W. Schuller, Y. Zong, and W. Zheng, “Emotion

Aware Contrastive Adaptation Network for Source-Free Cross-Corpus Speech


Emotion Recognition,” in _ICASSP_ _2024_ _-_ _2024_ _IEEE_ _International_ _Conference_


_on Acoustics, Speech and Signal Processing (ICASSP)_, 2024, pp. 11 846–11 850.


[108] D. Zhang, X. Ju, J. Li, S. Li, Q. Zhu, and G. Zhou, “Multi-modal multi-label


emotion detection with modality and label dependence,” in _Empirical_ _Methods_


_in Natural Language Processing (EMNLP 2020)_, Virtual Conference, November


_speech 2021_, 2021, pp. 3415–3419.


[111] S. Schneider, A. Baevski, R. Collobert, and M. Auli, “wav2vec: Unsupervised


Pre-Training for Speech Recognition,” in _Proc._ _Interspeech_ _2019_, 2019, pp.


3465–3469.


[112] W.-C. Lin and C. Busso, “Chunk-Level Speech Emotion Recognition: A General


Framework of Sequence-to-One Dynamic Temporal Modeling,” _IEEE_ _Transac-_


_tions on Affective Computing_, vol. 14, no. 2, pp. 1215–1227, 2023.


[113] H. Fei, Y. Zhang, Y. Ren, and D. Ji, “Latent Emotion Memory for Multi-Label


Emotion Classification,” _Proceedings_ _of_ _the_ _AAAI_ _Conference_ _on_ _Artificial_


93


_Intelligence_, vol. 34, no. 05, pp. 7692–7699, Apr. 2020. [Online]. Available:


[https://ojs.aaai.org/index.php/AAAI/article/view/6271](https://ojs.aaai.org/index.php/AAAI/article/view/6271)


[114] H. Chou, L. Goncalves, S. Leem, A. N. Salman, C. Lee, and C. Busso, “Minority


views matter: Evaluating speech emotion classifiers with human subjective an

notations by an all-inclusive aggregation rule,” _IEEE_ _Transactions_ _on_ _Affective_


_Computing_, no. 01, pp. 1–15, jun 2024.


[115] E. Zhang, R. Trujillo, and C. Poellabauer, “The MERSA Dataset and a


Transformer-Based Approach for Speech Emotion Recognition,” in _Proceedings_


_of_ _the_ _62nd_ _Annual_ _Meeting_ _of_ _the_ _Association_ _for_ _Computational_ _Linguistics_


94


