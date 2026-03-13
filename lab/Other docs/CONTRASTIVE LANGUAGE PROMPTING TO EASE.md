**CONTRASTIVE LANGUAGE PROMPTING TO EASE**
**FALSE POSITIVES IN MEDICAL ANOMALY DETECTION**


_YeongHyeon Park_ _Myung Jin Kim_ _Hyeong Seok Kim_


SK Planet Co., Ltd.


_{_ yeonghyeon, myungjin, beman _}_ @sk.com



**ABSTRACT**


A pre-trained visual-language model, contrastive languageimage pre-training (CLIP), successfully accomplishes various
downstream tasks with text prompts, such as finding images or localizing regions within the image. Despite CLIP’s
strong multi-modal data capabilities, it remains limited in
specialized environments, such as medical applications. For
this purpose, many CLIP variants—i.e., BioMedCLIP, and
MedCLIP-SAMv2—have emerged, but false positives related to normal regions persist. Thus, we aim to present a
simple yet important goal of reducing false positives in medical anomaly detection. We introduce a _**C**_ _ontrastive_ _**LA**_ _nguage_
_**P**_ _rompting_ _(_ _**CLAP**_ _)_ method that leverages both positive and
negative text prompts. This straightforward approach identifies potential lesion regions by visual attention to the positive
prompts in the given image. To reduce false positives, we
attenuate attention on normal regions using negative prompts.
Extensive experiments with the BMAD dataset, including
six biomedical benchmarks, demonstrate that CLAP method
enhances anomaly detection performance. Our future plans
include developing an automated fine prompting method for
more practical usage.


_**Index Terms**_ **—** anomaly detection, attention mechanism,
visual-language model


**1.** **INTRODUCTION**


Recent advancements in multi-modal models, particularly
visual-language models (VLMs), have revolutionized various downstream tasks, such as image retrieval, captioning, and object localization. Among these, Contrastive
Language–Image Pre-training (CLIP) [3] has demonstrated
remarkable performance by leveraging natural language
prompts to interpret visual data. This capability enables
CLIP to handle a wide array of tasks without specialized
fine-tuning. However, its application to highly specialized
domains, such as medical imaging, has uncovered limitations.
In the medical field, accurate anomaly detection is crucial
for early diagnosis and treatment. Nevertheless, generalpurpose models like CLIP often struggle with the intricacies



Input Ground-truth _Apositive_ _Anegative_ _ACLAP_ (Ours)


**Fig.** **1** . Generated attention maps by leveraging BiomedCLIP [1]. _Apositive_ and _Anegative_ are the attention maps obtained
using positive or negative prompts only. _ACLAP_ shows results
of our proposal, dubbed _**C**_ _ontrastive_ _**LA**_ _nguage_ _**P**_ _rompting_
_(_ _**CLAP**_ _)_ . CLAP leverages both positive and negative prompts.
The negative prompts are used to attenuate false positive attention of normal regions.


of medical images, which contain subtle and features unique
to medical imaging essential for identifying pathological
regions. To improve performance in biomedical domains,
various adaptations of CLIP, such as BiomedCLIP [1] and
MedCLIP-SAMv2 [4], have been proposed to improve performance in biomedical domains. They shows surprising
enhancement of medical reasoning compared to ordinary
models, but the issue of false positives—incorrectly identifying normal regions as anomalous—remains prevalent. These
false positives can lead to unnecessary medical procedures,
increasing the burden on healthcare systems and potentially
harming patients.
To address this issue, we propose a novel method called
_**C**_ _ontrastive_ _**LA**_ _nguage_ _**P**_ _rompting (_ _**CLAP**_ _)_, which introduces
a more refined way of leveraging natural language prompts
for medical anomaly detection. By leveraging both positive
and negative prompts, our method aims to find out lesions
accurately with CLIP attention. Positive prompts guide the
CLIP attention toward potential lesion regions, while nega

|s|Tru<br>False Positive<br>Suppression|
|---|---|
|s|False Positive<br>Suppression|













Result of CLAP













Language prompt







(b) Unsupervised anomaly detection (UAD) scheme







(a) Attention map generation by **C** ontrastive **LA** nguage **P** rompting (CLAP)



**Fig. 2** . Schematic diagram of our method. Existing positive prompt methods only utilize positive prompts. In this situation, the
false positive attention issue remains. In comparison, our method CLAP successfully suppresses false positives by additionally
exploiting negative prompts, shown in (a). After getting the attention map of CLAP, we employ the existing UAD model
EAR [2]. We only replace the saliency map for mosaic obfuscation with an attention map from CLAP, shown in (b).



tive prompts help attenuate the attention on normal regions,
thereby reducing the occurrence of strong attention to false
positives. This approach not only provides a more improved
understanding of the medical image but also aligns with the
demands for reliability in medical diagnostics by artificial intelligence.
We can just determine whether disease or not based on
the CLIP attention. Toward a more accurate diagnosis, we
employ an unsupervised anomaly detection (UAD) method
that features a reconstruction-by-inpainting strategy [2]. For
this, we obfuscate strong attention regions, over _µ_ + 0 _._ 674 _σ_
( _Q_ 3) [5] valued regions, by considering suspected disease regions. Then, we attempt to reconstruct obfuscated regions
into normal patterns by U-Net which is trained with normal
samples only. Finally, we determine the final disease based
on the reconstruction error obtained.
To evaluate the legitimacy of our proposal, we perform
extensive experiments using BMAD dataset [6]. This dataset
provides six benchmarks for five anatomies. Visual comparisons demonstrate that CLAP successfully overcomes issues
of strong attention in non-lesion regions. In addition, we
improved UAD performance compared to existing methods.
Through this work, we aim to bridge the gap between generalpurpose VLMs and the specific needs of medical anomaly detection. We conclude by discussing the potential for automating language prompt construction to further improve the usability of this approach in real-world clinical settings.


**2.** **METHODS**


In this section, we introduce a VLM-leveraged medical UAD
method. The proposed method as shown in Fig. 2 consists
of two major components as follows. (1) Obtain an attention map that indicates a suspected lesion area by zero-shot
inference of VLM. For this, we propose a method that overcomes an issue of false positive attention in a single positive
language prompting. (2) We present a UAD method using
a reconstruction-by-inpainting strategy. The UAD model attempts to reconstruct a suspected lesion area covered by an



attention mask. Then, it can be determined whether lesion
or not based on the reconstruction error. In-depth details are
introduced sequentially.


**2.1.** **Contrastive language prompting method**


The VLM takes each image _I_ as a visual prompt and each
text string _T_ as a language prompt. All CLIP variants are
consisted with image encoder Φ _I_ and text encoder Φ _T_ . In
this study, we exploit BiomedCLIP [1] which has special feature extraction capability on the biomedical domain by the
fine-tuning process. Specifically, we simply inherit an attention map generation method of MedCLIP-SAMv2 [4] summarized as (1). Note, _MI_ is the mutual information operation
and _β_ is a hyperparameter to balance each term.


_A_ = _MI_ ( _ZI_ _, ZT_ ; _θI_ _, θT_ ) _−_ _β × MI_ ( _ZI_ _, I_ ; _θI_ _, θT_ )

(1)
_w.r.t._ _ZI_ = Φ _I_ ( _I_ ; _θI_ ) _, ZT_ = Φ _T_ ( _T_ ; _θT_ )


The results of a positive language prompt, denoted as
_Apositive_, are shown in Fig. 1. This prompt conveys commaseparated words, recommended words by ChatGPT, that
can be used to refer to lesions (e.g., “Glioma, Astrocytoma,
Oligodendroglioma ...”). There are many strong attention
regions, dubbed false positives, in _Apositive_ even if the input image was normal. To mitigate the false positive issue on
_Apositive_, we additionally check the results of negative prompts
as shown in _Anegative_ . Those results show not very strong attention on non-negative regions (false negatives). Moreover,
the true negative regions are mostly highlighted that can be
used to suppress the false positives of _Apositive_ .
In this study, we propose CLAP, a straightforward approach. CLAP shows a very intuitive approach to take attention map as ‘ _ACLAP_ = _Apositive_ _−_ _Anegative_ ’. This simple
method can be further refined with a parametric function and
deep neural networks. The purpose of this study is to take a
first step toward reducing false positive attention when utilizing VLM for the biomedical domain. Therefore, more refined
methods will be dealt with in the next study.


**Table 1** . Positive and negative language prompt examples for
each anatomy. Symbols ‘P’ and ‘N’ represent positive and
negative respectively.

|Anatomy|P/N|Language prompt|
|---|---|---|
|Brain MRI|P<br>N|Glioma, Astrocytoma, Oligodendroglioma .. .<br>Normal, Healthy gray matter . . .|
|Liver CT|P<br>N|Malignant cells, Dysplasia, Hyperplasia .. .<br>Normal, Healthy, Benign .. .|
|Retinal OCT|P<br>N|Retinal fuid, Drusen, Retinal detachment .. .<br>Normal, Healthy, Clear . ..|
|Chest X-ray|P<br>N|Consolidation, Fibrosis, Atelectasis .. .<br>Healthy, Clear felds, Normal .. .|
|Lymph node|P<br>N|Metastatic carcinoma, Tumor metastasis . . .<br>Normal, Healthy tissue .. .|



**2.2.** **Reconstruction-by-inpainting for UAD**


UAD approaches based on the U-Net aim to block abnormal
feature transmission from the encoder to the decoder through
skip connections [2]. Since it is not known in advance where
and how large the anomalous pattern exists in the given image, cutting out the anomalous region by masking is difficult
to prevent abnormal feature transmission.
To address this, an attention map-based saliency obfuscation method was developed [2]. We adopt this method in
this study, and the overall scheme is shown in Fig. 2 (b).
The saliency region _S_, suspected to be abnormal, is identified
using our CLAP method according to (2), where each pixel
value exceeding _µ_ + 0 _._ 674 _σ_ ( _Q_ 3) [5] is flagged. Here, _µ_ and
_σ_ are the mean and standard deviation of _ACLAP_ .


_S_ = _where_ ( _ACLAP_ _> µ_ + 0 _._ 674 _σ_ ) (2)


This region will be obfuscated by a mosaic process to prevent the UAD model from receiving the abnormal pattern.
The U-Net is trained to reconstruct the partially obfuscated
image to its original form, a process known as reconstructionby-inpainting. Only normal samples are used for training, ensuring the model generalizes well to normal patterns while
struggling with abnormal pattern reconstruction.
During inference, the U-Net attempts to reconstruct the
saliency-obfuscated image. A reconstruction error map is obtained based on the error between the reconstruction result
and the original input image before obfuscation. We can perform image-level diagnosis using the maximum value of reconstruction error map.


**3.** **EXPERIMENTS**


**3.1.** **Experimental Setup**


We conduct experiments on the BMAD dataset [6], which
comprises brain MRI, liver CT, retinal OCT, chest X-ray, and
lymph node histopathology images. The training set comprises only anomaly-free samples, whereas the test and validation sets include both anomaly-free and anomalous samples.



**Normal** **Abnormal**
Input _ADINO_ _ACLAP_ (ours) Input _ADINO_ _ACLAP_ (ours)


False positives


False positives


False negatives


**Fig.** **3** . Attention results of visual-only model and visuallanguage model. The visual-only model, DINO [7], performs effective visual saliency attention in the ordinary domain but shows short in the medical domain. When applying our method CLAP on the visual-language model BiomedCLIP [1], false attentions are successfully removed.


**Implementation** **Details.** Following EAR [2], we use a UNet reconstruction model (Fig. 2) with five convolutional
blocks in both the encoder and decoder. Each encoder feature
map is directly connected to its corresponding decoder block
through skip connections. The U-Net is trained to minimize
reconstruction loss between the input image _I_ and the reconstruction output _I_ [ˆ] . We train U-Net with 20 epochs. In
each epoch, we randomly select 3k samples of the training
set to shorten the experimental period at this time. We plan
to conduct a full experiment in which the entire sample is
trained for longer epochs in future works.
**Suspected** **Disease** **Obfuscation.** EAR [2] uses DINO [7]
attention maps to generate mask candidates; however, since
DINO is not trained on biomedical data, it may produce inaccurate saliency predictions. To address this, we replace
DINO with our CLAP method. We compare results using
DINO [7] and BiomedCLIP [1] within EAR to set mask candidates. Specifically, we use two BiomedCLIP [1] configurations: (1) positive language prompting (PLP) alone and (2)
CLAP, which combines both positive and negative prompts.
Example prompts are provided in Table 1.
**Evaluation** **Metric.** We perform image-level detection on
the BMAD dataset [6] and evaluate using AUROC. Anomaly
scores are based on U-Net reconstruction error, illustrated in
Fig.2 (b). The reconstruction error between _I_ and _I_ [ˆ] is computed via MSGMS, represented as (3), following EAR [2].



**3.2.** **Qualitative results**


Qualitative results are shown in Fig. 1 and Fig. 3. Fig. 1
presents attention maps obtained with individual positive and
negative prompts, compared to our method. Using only the











_MSGMS_ ( _I,_ _I_ [ˆ] ) =



_S_



_s_ =1



2 _g_ ( _I_ _[s]_ ) _g_ ( _I_ [ˆ] _[s]_ ) + _c_
1 _−_



_g_ ( _I_ _[s]_ ) [2] + _g_ ( _I_ [ˆ] _[s]_ ) [2] + _c_



(3)


**Table** **2** . Comparison of anomaly detection performance on
the BMAD dataset [6], where PLP denotes positive language
prompting, and our proposed method is CLAP.

|Anatomy|Brain MRI<br>BraTS2021|Liver CT|Retinal OCT|Col5|Chest X-ray|Lymph node|Average|
|---|---|---|---|---|---|---|---|
|**Dataset**|**Dataset**|**BTCV + LiTs**|**RESC**|**OCT2017**|**RSNA**|**CAMELYON16**|**CAMELYON16**|
|EAR [2]<br>PLP<br>CLAP (ours)|77.37<br>73.54<br>**78.55**|72.51<br>**72.76**<br>72.60|86.42<br>90.08<br>**91.66**|**97.46**<br>96.77<br>96.38|**71.69**<br>65.23<br>65.76|63.39<br>64.98<br>**68.42**|78.21<br>77.23<br>**78.89**|



positive prompt produces strong false positives in _Apositive_,
while the negative prompt _Anegative_ includes some false negatives but yields mainly true negatives. This combination helps
suppress false positives in _Apositive_, resulting in the final attention map _ACLAP_ .
We further compare the attention results of DINO [7] and
CLAP in Fig. 3. DINO tends to highlight regions with distinct
features, which often leads to unintended attention on nonlesion areas. In contrast, CLAP, built on BiomedCLIP [1],
leverages language prompts to focus on specific lesion regions within an image. This capability allows BiomedCLIP
to generate precise attention maps for lesions by modulating
the language prompts. Designed to minimize false positive
attention, CLAP demonstrates relatively accurate lesion localization compared to DINO, which aids in the accurate obfuscation of suspected defect regions before the image is input
into the U-Net.


**3.3.** **Quantitative results**


To quantitatively assess the UAD performance, we report AUROC values in Table 2. The primary objective of this study is
to enhance the true positive detection capability of BiomedCLIP [1] in biomedical anomaly detection tasks.
Accordingly, we compare the attention performance of
the non-biomedical model DINO [7] with that of BiomedCLIP using PLP, positive language prompting, and our CLAP
method. The performance of basic DINO, marked with EAR,
and PLP is almost the same. This means that DINO attention can catch the lesion to some extent without biomedical
knowledge. At the same time, PLP has biomedical knowledge
but contains false attention alarms. CLAP not only improves
performance over PLP by attenuating false attention but also
achieves better overall performance compared to EAR. Notably, CLAP performs particularly well on subsets of images
with small, irregular patterns, such as those in ‘RESC’ and
‘CAMELYON16’.


**4.** **CONCLUSION**


In this work, we introduced a novel approach, _**C**_ _ontrastive_
_**LA**_ _nguage_ _**P**_ _rompting (_ _**CLAP**_ _)_, aimed at reducing false positives in medical anomaly detection using VLMs like BiomedCLIP [1]. By utilizing both positive and negative prompts,
our method enhances the identification of lesion regions
while suppressing attention on normal areas, addressing a



key limitation in previous models that only leveraged positive prompts. Extensive experiments with the BMAD dataset
demonstrate that CLAP improves anomaly detection accuracy across various medical image types, outperforming both
DINO [7] and single-prompt methods. Furthermore, we integrated CLAP with a reconstruction-by-inpainting U-Net approach, enhancing its diagnostic utility. Moving forward, we
aim to refine this technique by automating language prompt
generation to further support real-world clinical applications,
reducing manual intervention and enhancing the scalability
of this method in diverse medical scenarios.


**5.** **ACKNOWLEDGMENTS**


This work was supported by SK Planet Co., Ltd., Korea.


**6.** **REFERENCES**


[1] Sheng Zhang, Yanbo Xu, Naoto Usuyama, Hanwen Xu,
Jaspreet Bagga, Robert Tinn, Sam Preston, Rajesh Rao,
Mu Wei, Naveen Valluri, et al., “Biomedclip: a multimodal biomedical foundation model pretrained from fifteen million scientific image-text pairs,” _arXiv_ _preprint_
_arXiv:2303.00915_, 2023.


[2] YeongHyeon Park, Sungho Kang, Myung Jin Kim,
Yeonho Lee, Hyeong Seok Kim, and Juneho Yi, “Visual
defect obfuscation based self-supervised anomaly detection,” _Scientific Reports_, vol. 14, no. 1, pp. 18872, 2024.


[3] Alec Radford, Jong Wook Kim, Chris Hallacy, Aditya
Ramesh, Gabriel Goh, Sandhini Agarwal, Girish Sastry, Amanda Askell, Pamela Mishkin, Jack Clark, et al.,
“Learning transferable visual models from natural language supervision,” in _International_ _conference_ _on_ _ma-_
_chine learning_ . PMLR, 2021, pp. 8748–8763.


[4] Taha Koleilat, Hojat Asgariandehkordi, Hassan Rivaz,
and Yiming Xiao, “Medclip-samv2: Towards universal
text-driven medical image segmentation,” _arXiv preprint_
_arXiv:2409.19483_, 2024.


[5] John Wilder Tukey, “Exploratory data analysis,”
_Reading/Addison-Wesley_, 1977.


[6] Jinan Bao, Hanshi Sun, Hanqiu Deng, Yinsheng He,
Zhaoxiang Zhang, and Xingyu Li, “Bmad: Benchmarks
for medical anomaly detection,” in _Proceedings_ _of_ _the_
_IEEE/CVF_ _Conference_ _on_ _Computer_ _Vision_ _and_ _Pattern_
_Recognition_, 2024, pp. 4042–4053.


[7] Mathilde Caron, Hugo Touvron, Ishan Misra, Herv´e
J´egou, Julien Mairal, Piotr Bojanowski, and Armand
Joulin, “Emerging properties in self-supervised vision
transformers,” in _Proceedings of the IEEE/CVF interna-_
_tional_ _conference_ _on_ _computer_ _vision_, 2021, pp. 9650–
9660.


