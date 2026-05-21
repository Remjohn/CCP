## **Activation Steering for Accent Adaptation in Speech Foundation Models**

_Jinuo Sun_ [1] _[,][∗]_ _, Yang Xiao_ [1] _[,][∗]_ _, Sung Kyun Chung_ [1] _, Qiuchi Hu_ [1] _, Gongping Huang_ [2] _, Eun-Jung Holden_ [1] _,_
_Ting Dang_ [1]


1 School of Computer Science, The University of Melbourne, Australia
2 Wuhan University, China

jinuosun@gmail.com, yxiao9550@student.unimelb.edu.au, ting.dang@unimelb.edu.au



**Abstract**


Accent variability remains a major errors in automatic speech
recognition, yet most adaptation methods rely on parameter
fine-tuning without understanding where accent information is
encoded. We treat accent variation as an interpretable subspace in hidden representations and investigate whether it can
be identified and controlled directly in activation space. We
extract layer-wise encoder activations and estimate mean-shift
directions capturing accent-induced representation shifts. By
injecting these directions into individual layers and measuring
how they align accented and standard embeddings, we derive a
layer-wise accent sensitivity profile, revealing that accent information concentrates in a narrow band of middle encoder layers.
Leveraging this structure, we further introduce parameter-free
accent steering that modifies representations during inference
without updating model weights. Experiments across eight accents show consistent word error rate reductions.
**Index** **Terms** : speech recognition, human-computer interaction, computational paralinguistics


**1.** **Introduction**


Accent variability remains a persistent challenge for automatic
speech recognition (ASR) systems [1]. Systematic differences in phoneme realization, prosody, and phonotactic patterns
across regional and non-native accents often lead to recognition errors that disproportionately affect certain speaker populations [2, 3]. In real-world deployments, including voice assistants, call centers, and educational technologies, such performance disparities degrade user experience and raise important concerns regarding fairness and accessibility [4]. Despite
advances in large-scale pretraining and robust acoustic modeling [5], recognition gaps across accents continue to be observed.
Conventional accent adaptation techniques typically rely
on supervised fine-tuning, accent-specific modeling, or data
augmentation [6–8]. While effective in traditional ASR settings, these approaches become increasingly costly and operationally restrictive in the era of foundation-scale speech models. Full-parameter adaptation is computationally expensive
and may compromise generalization across diverse accents and
tasks [9–11]. As modern speech systems are frequently deployed as shared, large-scale backbones, there is growing need
for lightweight and scalable adaptation mechanisms.
Recent large audio language models (LALMs), such as
Whisper [12], combine powerful acoustic modeling with large
language modeling to achieve strong zero-shot generalization.
While Parameter-Efficient Fine-Tuning (PEFT) methods and
bottleneck adapters [13–16] offer a more lightweight adaptation


*These authors contributed equally.



approach by adding only a small number of trainable parameters
on top of a frozen base model, these approaches still optimize
the added parameters heuristically [17–20]. Without explicitly localizing or constraining updates to layers and subspaces
that are most sensitive to accent-related variation, these methods may perform unnecessary adaptation in accent-insensitive
regions of the model and risk entangling accent compensation
with higher-level semantic representations, limiting both efficiency and control.

Understanding how accent variation is organized in representation space is critical for designing scalable and controllable adaptation strategies. If accent corresponds to identifiable
subspaces in hidden activations, then targeted representationlevel interventions may offer an alternative to parameterintensive fine-tuning [21]. Recent studies in large language
models show that high-level attributes, such as sentiment, style,
or safety [22–26], can align with approximately linear directions in activation space. These directions, often referred to
as steering vectors, are typically constructed as mean activation shifts between contrasting concepts [27, 28]. When added
to hidden states at selected layers, they nudge representations
toward desired regions of the space, enabling controllable behavioral modulation at inference time without modifying model
parameters. This perspective motivates the central question of
this work: _Does_ _accent_ _variation_ _correspond_ _to_ _a_ _structured_
_and controllable subspace in LALMs?_

In this paper, we first conduct a layer-wise analysis of hidden activations to understand the geometric structure of accent variations. This investigation serves two primary purposes.
From an _interpretability_ perspective, it reveals how the model
distributes accent information across layers. Furthermore, from
a _controllability_ perspective, it determines whether these accent features are organized enough to allow direct adjustments.
Based on this foundation, we construct steering vectors to adjust accent representations during model inference. Our method
inserts learned accent directions into specific hidden states. We
subsequently evaluate their effectiveness in automatic speech
recognition (ASR) tasks across diverse pronunciations. To the
best of our knowledge, this is the first study to systematically
analyze and apply vector steering for accent-robust automatic
speech recognition. Our extensive experiments on the VCTK
and L2-ARCTIC datasets demonstrate the middle layers and
late layers are the most sensitive to accent-induced representation shifts. Moreover, mean shift steering significantly improves the word error rate across eight distinct accents. We observe that interventions in the middle layers provide the most
effective control. This study offers a principled and scalable
way to reduce accent-induced recognition disparities in speech
foundation models, advancing both robustness and fairness in
real-world ASR deployment.


**2.** **Accent Subspace Analysis and Steering**


**2.1.** **Layer-wise Accent Subspace Analysis**


We analyze how accent-related variation is organized across encoder layers and quantify how strongly each layer responds to
accent-specific representation shifts. This yields a layer-wise
sensitivity profile that highlights which layers are most suitable
for subsequent accent steering.


_2.1.1._ _Accent Representation Perturbation_


We construct text-matched utterance pairs to isolate accentrelated acoustic variation from linguistic content. For each target accent, we create two types of pairs: (i) _cross-standard-_
_accent_ pairs ( _xs, xa_ ), where _xa_ is an accented utterance and
_xs_ is a standard-English utterance with an identical transcript,
and (ii) _within-single-accent_ pairs ( _xa, xa_ ) formed by different speakers from the same accent group. The cross-standardaccent pairs capture systematic accent-induced differences,
while the within-single-accent pairs serve as a control to account for speaker-specific factors such as timbre or prosody,
helping us separate accent effects from general inter-speaker
variation. Given accented speech samples _xa_ and standard
speech samples _xs_, our layer-wise analysis then quantifies, at
each encoder layer, how the latent representations of accented
speech differ from those of standard English, and how effectively a layer supports aligning these two clusters. Concretely,
for each layer _l_, we first extract the token-level hidden activations **H** [(] _[l]_ [)] . For each speech sample _i_, we apply mean pooling
over time to obtain an utterance-level representation **h** [¯] [(] _i_ _[l]_ [)][. Based]
on these pooled representations, we compute an accent meanshift direction from a source accent group _s_ to a target accent
group _a_ :






_i∈Ga_



1
**d** [(] _s_ _[l]_ _→_ [)] _a_ [=]
_|Gs|_






_j∈Gs_



1
**h** ¯ [(] _j_ _[l]_ [)] _−_ _|Ga|_



**h** ¯ [(] _i_ _[l]_ [)] (1)



For each source-target speech pair, we apply the mean-shift
displacement **d** [(] _s_ _[l]_ _→_ [)] _a_ [at] [audio] [encoder] [layer] _[l]_ [and] [measure] [its]
propagated effect in the multi-modal projector space. Because
the projector output remains time-dependent, we further apply
mean pooling over the projector time steps to obtain a single
utterance-level representation for each sample, on which cosine
similarity is computed.
We define the Accent Alignment Score (AAS) as the change
in cosine similarity between the perturbed source representation
and the target representation:


AAS [(] _s_ _[l]_ _→_ [)] _a_ [= cos (˜] **[z]** proj _[ a,]_ [(] _[l]_ [)] _[,]_ **[ z]** proj _[ b]_ [)] _[ −]_ [cos (] **[z]** proj _[ a]_ _[,]_ **[ z]** proj _[ b]_ [)] (3)


Here, **z** ˜proj _[a,]_ [(] _[l]_ [)] denotes the projector output of the source
speech sample after applying the layer- _l_ perturbation. Meanwhile, **z** proj _[a]_ [and] **[z]** proj _[ b]_ [represent] [the] [baseline] [projector] [outputs]
for the source and target speech samples, respectively. A positive AAS indicates that the layer-wise perturbation moves the
source representation closer to the target accent representation.
We apply the same procedure to both cross-standard-accent
and within-single-accent pairs, and compute their AAS values
at each layer. Specifically for within-single-accent pairs, we
calculated a within accent mean-shift vector **d** [(] _a_ _[l]_ _→_ [)] _a_ [between two]
speakers of the same accent, following the same AAS calculation procedure.
To isolate the additional alignment gain observed in cross
pairs beyond general speaker variation, we compute the specificity score, which measures the amount of the patching effect
that truly comes from the accent:


Spec [(] _[l]_ [)] = AAS ~~(~~ cross _l_ ) _[−]_ [AAS] ~~(~~ within _l_ ) (4)


where Spec [(] _[l]_ [)] denotes _Specificity_ score at layer _l_, and AAS denotes the average score across all evaluated speech pairs in their
respective sets. The subscript cross denotes cross-standard–
accent pairs, while within denotes within-accent pairs. A positive Spec [(] _[l]_ [)] value proves that the patching effect at this specific
layer is indeed caused by accent differences. Consequently, it
is not caused by other speaker-level variations. Based on this
logic, the layer sensitivity score is defined as follows:
Sensitivity [(] _[l]_ [)] = max(0 _,_ Spec [(] _[l]_ [)] ) (5)


which is used for ranking across layers. In addition, our
layer-wise analysis adopts a bidirectional design ( _standard_ _→_
_target_ and _target →_ _standard_ ) to reduce direction-specific bias
and provide a more robust estimate of layer sensitivity. Each
direction is computed independently and then averaged.


**2.2.** **Inference-Time Accent Steering**


The layer-wise sensitivity analysis identifies candidate layers
for controllable accent intervention. Building on the analysis,
we next construct steering vectors to modulate accent-related
representation during inference. We then test whether steering
at these layers can produce measurable shifts that improve the
downstream ASR performance of accented speech toward that
of standard speech. To extract the generalized steering vector
and avoid the effect of speakers and sentences, we design an
_extraction set_ and an _evaluation set_ . They are isolated from the
speakers and texts. This design ensures that the steering vector
is estimated from data that shares neither speaker identity nor
text content with the evaluation data.
For steering, we reuse the mean-shift direction defined in
(1), but compute it only from the extraction set. Before injec


where _Gs_ and _Ga_ denote the sample sets corresponding to the
standard and accent speech, respectively. This vector **d** [(] _s_ _[l]_ _→_ [)] _a_
characterizes the accent shift between the two representation
clusters at layer _l_ .
To probe the sensitivity of layer _l_ to this accent direction,
we apply a controlled perturbation to its hidden activations:


**H** ˜ [(] _[l]_ [)] = **H** [(] _[l]_ [)] + _α ·_ **d** [(] _s_ _[l]_ _→_ [)] _a_ _[,]_ (2)


where _α_ is optimized to 1 _._ 0, corresponding to a one-unit accent
mean-shift perturbation, and **d** [(] _s_ _[l]_ _→_ [)] _a_ [is broadcast across all time]
steps of **H** [(] _[l]_ [)] . The resulting perturbed activations **H** [˜] [(] _[l]_ [)] are then
propagated through the remaining encoder and projector layers.


_2.1.2._ _Quantifying_ _Layer_ _Sensitivity_ _via_ _Accent_ _Alignment_
_Score (AAS)_


Given the layer-wise perturbation defined above, we quantify
how much each layer contributes to reducing the representation
gap between accented and standard speech. Our analysis is conducted on the audio encoder of Qwen2-Audio-7B [29], which
consists of 32 Whisper-style encoder layers followed by a multimodal projector. Since accent variation is primarily expressed
through acoustic patterns, we focus on hidden-state transformations within the audio encoder and measure their propagated
effects in the projector space, which provides the final speech
representation passed to the downstream language model.


tion, we normalize the direction **d** [(] _s_ _[l]_ _→_ [)] _a_ [to unit norm:]

**d** ˆ [(] _s_ _[l]_ _→_ [)] _a_ [=] �� **dd** [(] _s_ ( _s_ _[l]_ _l→→_ [)] ) _aa_ �� (6)

           -            

This separates direction from magnitude and makes the steering
strength parameter _α_ comparable across layers.
During inference, we inject the normalized steering vector
into the hidden states at the selected layer _l_ :


**H** ˜ [(] _[l]_ [)] = **H** [(] _[l]_ [)] + _α_ **d** ˆ [(] _s_ _[l]_ _→_ [)] _a_ (7)

where _α_ controls the steering strength. The vector **d** [ˆ] [(] _s_ _[l]_ _→_ [)] _a_
is broadcast across all time steps of **H** [(] _[l]_ [)] . We implement this
intervention using a forward hook, so no model parameters are
modified. We propose that the vector of an accent direction estimated from a subset of speech data can generalize effectively
to unseen speakers and unseen utterances. The evaluation is in
the Results section.


**3.** **Experiment Settings**


**3.1.** **Datasets and Accents**


**Native accents:** We adopt the VCTK dataset [2], a high-fidelity
corpus featuring speakers with diverse regional accents, to study
native English variations. Specifically, we select Scottish, South
African, Canadian, Irish, and Northern Irish accents for our experiments. As VCTK includes a standard English group, we
utilize this subset directly as our reference for comparison.
**Non-native** **accents:** We utilize the L2-ARCTIC corpus [3],
which provides manual phonetic-level annotations of speech
from diverse linguistic backgrounds. In this study, we focus on
Hindi, Arabic, and Spanish accents. Since L2-ARCTIC lacks
an internal native reference, we draw native speakers from its
source, the CMU-ARCTIC dataset [30], which consists of phonetically balanced sentences designed for speech synthesis. Because both datasets utilize identical reading scripts, the CMUARCTIC data serve as an ideal, matched reference group.


**3.2.** **Pair Construction and Data Splits**


**Accent** **Subspace** **Analysis:** For each of the above accents,
we construct 1000 cross-standard-accent pairs and 500 withinsingle-accent pairs. No data split is required.
**Inference-Time Accent Steering:** For each of the above target
accents, we adopt a strict data splitting protocol: 80% of the
speakers are assigned to the extraction set, while the remaining
20% are reserved for the evaluation set. We further enforce
no transcript overlap between extraction pairs and evaluation
utterances to avoid text leakage. For each accent group, we
randomly sample 1,000 speech pairs from the extraction set to
estimate the mean-shift vector.


**3.3.** **Evaluation Protocol**


We evaluate steering in a single-layer sweep across 32 encoder
layers, where each layer and each steering strength _α_ are tested
independently. We choose _α_ = [0.5, 1, 2, 5] to cover different
scale of steering strength. Steering effectiveness is evaluated by
the resulting change in Word Error Rate (WER).
To reduce bias from overly easy or overly difficult samples,
the evaluation set is constructed by balanced sampling: half of
the utterances are drawn from samples with WER = 0, and
the other half from samples with WER _>_ 0. In a typical setting, we sample 100 utterances from each group, yielding 200
evaluation samples in total.



**4.** **Results and analysis**


**4.1.** **Accent Subsapce Analysis**
To reduce scale differences, each accent group is normalized independently. Layer 31 is excluded as it directly precedes the linear multi-modal projector. Sensitivity analysis on
VCTK shows a shared pattern: low sensitivity in early layers
(0–14), an emerging peak near layer 15, and a sharp rise to
global maximums from layer 21 onward. L2-ARCTIC exhibits
similar trends but with stronger global fluctuations, suggesting non-native accents induce more distributed representational
changes. The steering window is divided into early (0–14), middle (15–19), and late (20–30) stages. Early layers process lowabstraction acoustic information [31, 32]; native accents show
weak sensitivity here, while non-native accents trigger higher
peaks due to stronger low-level acoustic deviations. This makes
early intervention less controllable. Middle and late layers are
identified as the most suitable locations for steering vectors.


**4.2.** **Analysis of Layer-Wise Steering Dynamics**
_4.2.1._ _Steering Effect on Native Accents_
We first analyze the layer-wise steering effect on the VCTK
dataset to understand native accent representations. As shown
in Figure 1c, we observe a consistent trend across the Scottish,
South African, Canadian, Irish, and Northern Irish groups. In
the early layers, the intervention yields minimal impact on the
mean word error rate. However, the middle layers exhibit a significant reduction in recognition errors This reduction peaks in
the mid sections, reaching a maximum drop of nearly 0.3 for
certain regions. Conversely, applying vectors to the late layers
degrades performance sharply. For example, layer 31 experiences massive error increases across all groups. This geometric
pattern suggests that native accent characteristics are primarily encoded in intermediate representations. Therefore, targeted
interventions in these middle sections provide optimal control
without disrupting higher level semantic understanding.


_4.2.2._ _Steering Effect on Non-native Accents_
We extend our analysis to non-native speech using the L2ARCTIC corpus. We evaluate the mean shift steering effect
on Hindi, Arabic, and Spanish variations. Similar to the native
setup, the performance changes reveal a distinct spatial structure
as shown in Figure 1d. The early layers show relatively stable
performance with minimal metric fluctuations. Subsequently,
the middle layers again demonstrate a clear improvement in
recognition accuracy. Although the error reduction is smaller
than that of native speech, reaching around negative 0.05, the localized trend remains highly consistent. Furthermore, steering
in the final layers causes severe degradation. Specifically, layer
31 alone adds approximately 4.0 to the error rate across all three
linguistic backgrounds. This structure confirms that non-native
accent variations also occupy a controllable subspace. Consequently, applying targeted steering to specific middle layers offers a scalable pathway for adaptive systems.


_4.2.3._ _Cross-Accent Steering Pattern and Insights_


Empirical results reveal consistent layer-wise patterns for both
native and non-native accents. Layers 0–14 are largely unresponsive to steering, yielding minimal metric changes. Conversely, the middle layers (15–19) emerge as the optimal window, showing consistent, significant error reductions across all
linguistic backgrounds. This suggests middle-layer representations are not yet fixed, allowing accent perturbations to propagate stably and confirming these intermediate states effectively


Layer-wise Sensitivity on VCTK Accents













1.0


0.8


0.6


0.4


0.2


0.0



|Scottish Irish<br>South African Northern I<br>Canadian|rish|Col3|Col4|
|---|---|---|---|
|||||
|Early Layers|Mid|Mid|Late Layers|
|||||


0 5 10 15 20 25 30
Layer



|ve-Accent Steering Effect ( =5)|Col2|
|---|---|
|~~Layer 31 (omitted):~~<br> <br> e-Accent Steering Effect ( =5)<br>~~Canadian~~<br>~~Northern Irish~~|~~Layer 31 (omitted):~~<br> <br> e-Accent Steering Effect ( =5)<br>~~Canadian~~<br>~~Northern Irish~~|
|Irish<br>|<br> Scottish: +4.9<br> South African: +2.5<br>~~ Canadian: +4.7~~<br>|
|Irish: +1.5<br> Northern Irish: +5.8|Irish: +1.5<br> Northern Irish: +5.8|
|Mid<br>Late Layers|Mid<br>Late Layers|
|||
|||


0 5 10 15 20 25 30
Layer Index



~~Scottish~~
South African (4-fold CV)











VCTK Native-Accent Steering: Alpha Sensitivity



0.00


0.05


0.10


0.15


0.20


0.25



0.4


0.3


0.2


0.1


0.0


0.1


0.2


0.3






|Col1|Col2|Col3|
|---|---|---|
||||
|Early Layers|Mid|Late Layers|
|= 0.5<br> <br> = 2<br>||Layer 31 (omitted):<br>~~  =0.5: +0.33~~<br>  =1: +0.57<br>  =2: +0.70<br>|



0 5 10 15 20 25 30
Layer Index

(e) _Alpha sensitivity on average_ ∆ _WER on_
_VCTK dataset_


L2-ARCTIC Non-Native Steering: Alpha Sensitivity



(a) _Layer-wise accent sensitivity analysis on_
_VCTK dataset_


Layer-wise Sensitivity on L2-Arctic Accents



(c) _Steering_ ∆ _WER on VCTK dataset_



1.0


0.8


0.6


0.4


0.2


0.0



|Arabic<br>Hindi<br>Spanish|Col2|Col3|Col4|
|---|---|---|---|
|||||
|Early Layers|Early Layers|Mid|Late Layers|
|||||


0 5 10 15 20 25 30
Layer



|-Native Accent Steering Effect ( =5)|Col2|Col3|
|---|---|---|
|~~Layer 31 (omitted):~~<br> <br> -Native Accent Steering Effect ( =5)|~~Layer 31 (omitted):~~<br> <br> -Native Accent Steering Effect ( =5)|~~Layer 31 (omitted):~~<br> <br> -Native Accent Steering Effect ( =5)|
|<br>~~ )~~|<br> Hindi: +3.7<br> Arabic: +3.9<br>~~ Spanish: +4.2~~||
|<br>|<br>|<br>|
||||
|s<br>Mid<br>Late Layers|s<br>Mid<br>Late Layers|s<br>Mid<br>Late Layers|
||||


0 5 10 15 20 25 30
Layer Index



0.30


0.25


0.20


0.15


0.10


0.05


0.00


0.05



~~Hindi (4-fold CV)~~
Arabic (4-fold CV)









|= 0.5 = 2<br>= 1 = 5|Col2|Col3|Layer 31 (omitted):<br>=0.5: +0.66<br>=1: +0.84|
|---|---|---|---|
|<br>|<br>||<br> =2: +1.03<br> =5: +3.94|
||||<br>|
|Early Layers|Early Layers|Mid|Late Layers|


0 5 10 15 20 25 30
Layer Index





0.20


0.15


0.10


0.05


0.00


0.05



(d) _Steering_ ∆ _WER on L2-ARCTIC dataset_ (f) _Alpha sensitivity on average_ ∆ _WER on_

_L2-ARCTIC dataset_
Figure 1: _Layer-wise accent subspace analysis and steering results with alpha sweep._



(b) _Layer-wise accent sensitivity analysis on_
_L2ARCTIC dataset_



(d) _Steering_ ∆ _WER on L2-ARCTIC dataset_



isolate accent characteristics for controllable steering.Latelayer steering produces highly unstable, divergent results. For
non-native accents, it frequently causes representation collapse;
even for native accents, gains do not exceed those of the middle
layers. This poor controllability likely stems from increasingly
fixed representations, leaving too few layers to reorganize injected directions. Finally, terminal layer 31 consistently causes
massive performance degradation, confirming the tail layer is
unsuitable for injection.


_4.2.4._ _Steering Strength Analysis_
To compare how different _α_ values affect performance, we compute, for both native and non-native accents, the mean ∆WER
steering effect under each _α_ injection strength. Figures 1e
and 1f illustrate the resulting _α_ -parameter sensitivity trends. We
observe that as _α_ increases, the layer-wise steering effect exhibits larger fluctuations and higher improvement peaks. Notably, once the steering strength exceeds a critical threshold,
both native and non-native accents show signs of an accelerated
collapse starting from around layer 27.
Specifically, for native accents, _α_ = 2 yields strong steering effects in the late layers with a generally depth-progressive
trend, but performs poorly in the mid layers. In contrast, with
_α_ = 5, the mid-layer performance improves substantially, surpassing the late layers and reaching higher peaks, while the late
layers display stronger oscillations and clearer collapse behavior. For non-native accents, the overall trend is more consistent:
the mid layers constitute the globally optimal intervention window, whereas the collapse in the late layers becomes increasingly pronounced as _α_ grows, with the collapse onset shifting
toward earlier layers. Overall, the _α_ sweep further corroborates that the mid layers (15-19) form a shared and most suitable steering window across both native and non-native accents.
We therefore suggest that, when performing single-layer accentdirection steering, one should initially try a relatively large _α_ injection strength and, once the improvement magnitude reaches
the desired level at a particular _α_, conduct small local adjustments around that value to better trade off peak gains against
the risk of window collapse.


**4.3.** **Comparable study with PEFT Baseline**


Table 1 compares the fine-tuning approach with our proposed
steering method. Analysis reveals a critical link between train


Table 1: _Comparison of steering and fine-tuning across accents._
_Lower WER is better._ _The Train column reports the exact num-_
_ber of available training speech pairs for PEFT. The Base met-_
_ric represents the initial error rate of the unadapted model. Sub-_
_sequently,_ _the Steer and PEFT columns denote the recognition_
_error rates after applying our proposed steering method and the_
_parameter fine-tuning approach._


Accent Train Base Steer PEFT St. ∆ PEFT ∆


Scottish 197 26.72% 6.80% 9.25% **-19.92%** -17.47%
S. Afr. 44 29.86% 4.35% 27.10% **-25.51%** -2.76%
Canadian 51 37.27% 3.47% 32.60% **-33.80%** -4.67%
N. Irish 49 36.27% 6.64% 31.57% **-29.63%** -4.70%
Irish 87 31.91% 6.41% 30.28% **-25.50%** -1.63%


Arabic 802 18.13% 10.07% 7.20% **-8.06%** -10.93%
Hindi 790 14.26% 10.22% 7.82% **-4.04%** -6.44%
Spanish 796 15.31% 9.39% 8.61% **-5.92%** -6.70%


ing sample size and adaptation efficacy. Fine-tuning excels
with large datasets, such as the Arabic, Hindi, and Spanish
sets containing approximately 800 training pairs. Conversely,
parameter-updating techniques struggle in data-scarce scenarios. For accents with fewer than 100 samples—including South
African, Canadian, Northern Irish, and Irish—fine-tuning performance is remarkably poor. In contrast, steering excels under these constraints, achieving 4.04 to 33.80 percentage-point
WER reductions (28.3%–90.7% relative) across eight accents
using very few samples. Furthermore, as steering requires no
parameter updates, it preserves original model capabilities, providing an efficient, flexible solution for inference adaptation.


**5.** **Conclusion**


In this paper, we propose a lightweight method to mitigate accent variability in automatic speech recognition. Initially, our
analysis identified the middle layers(15-19) in the audio encoder of Large Audio LMs as the optimal region for targeted
intervention Based on this geometric insight, we introduced
a parameter-free adaptation technique using mean shift steering vectors. Consequently, this approach significantly reduces
recognition errors across diverse accents. Furthermore, it vastly
outperforms conventional fine-tuning in data-scarce environments without requiring weight updates. Ultimately, this research provides a highly scalable pathway for developing inclusive speech technologies.


**6.** **Generative AI Use Disclosure**


We use generative AI tools for polishing the manuscript, e.g.,
correcting the grammar.


**7.** **References**


[1] H. Mohyuddin and D. Kwak, “Automatic speech recognition in diverse english accents,” in _2023 International Conference on Com-_
_putational Science and Computational Intelligence (CSCI)_, 2023,
pp. 714–718.


[2] J. Yamagishi, C. Veaux, and K. MacDonald, “Cstr vctk
corpus: English multi-speaker corpus for cstr voice cloning
toolkit (version 0.92),” 2019. [Online]. Available: [https:](https://doi.org/10.7488/ds/2645)
[//doi.org/10.7488/ds/2645](https://doi.org/10.7488/ds/2645)


[3] G. Zhao, S. Sonsaat, A. Silpachai, I. Lucic, E. ChukharevHudilainen, J. Levis, and R. Gutierrez-Osuna, “L2-arctic: A nonnative english speech corpus,” in _Proc._ _Interspeech_ _2018_, 2018,
pp. 2783–2787.


[4] A. Koenecke, A. Nam, E. Lake, J. Nudell, M. Quartey, Z. Mengesha, C. Toups, J. R. Rickford, D. Jurafsky, and S. Goel, “Racial
disparities in automated speech recognition,” _Proceedings_ _of_ _the_
_national_ _academy_ _of_ _sciences_, vol. 117, no. 14, pp. 7684–7689,
2020.


[5] Y. Xiao, H. Yin, J. Bai, and R. K. Das, “Dg-sed: Domain generalization for sound event detection with heterogeneous training
data,” in _2025 Asia-Pacific Signal and Information Processing As-_
_sociation Annual Summit and Conference (APSIPA ASC)_, 2025.


[6] S. Ghorbani and J. H. Hansen, “Domain expansion for end-toend speech recognition: Applications for accent/dialect speech,”
_IEEE/ACM_ _Transactions_ _on_ _Audio,_ _Speech,_ _and_ _Language_ _Pro-_
_cessing_, vol. 31, pp. 762–774, 2022.


[7] Y. Qian, X. Gong, and H. Huang, “Layer-wise fast adaptation for
end-to-end multi-accent speech recognition,” _IEEE/ACM_ _Trans-_
_actions on Audio, Speech, and Language Processing_, vol. 30, pp.
2842–2853, 2022.


[8] D. Prabhu, P. Jyothi, S. Ganapathy, and V. Unni, “Accented speech
recognition with accent-specific codebooks,” in _Proceedings_ _of_
_the 2023 Conference on Empirical Methods in Natural Language_
_Processing_, 2023, pp. 7175–7188.


[9] M. A. T. Turan, E. Vincent, and D. Jouvet, “Achieving multiaccent asr via unsupervised acoustic model adaptation,” in _Proc._
_Interspeech 2020_, 2020, pp. 1286–1290.


[10] A. Jain, M. Upreti, and P. Jyothi, “Improved accented speech
recognition using accent embeddings and multi-task learning,” in
_Proc. Interspeech 2018_, 2018, pp. 2454–2458.


[11] J. Li, V. Manohar, P. Chitkara, A. Tjandra, M. Picheny, F. Zhang,
X. Zhang, and Y. Saraf, “Accent-robust automatic speech recognition using supervised and unsupervised wav2vec embeddings,”
_arXiv preprint arXiv:2110.03520_, 2021.


[12] A. Radford, J. W. Kim, T. Xu, G. Brockman, C. McLeavey, and
I. Sutskever, “Robust speech recognition via large-scale weak
supervision,” in _International_ _conference_ _on_ _machine_ _learning_ .
PMLR, 2023, pp. 28 492–28 518.


[13] N. Houlsby, A. Giurgiu, S. Jastrzebski, B. Morrone,
Q. de Laroussilhe, A. Gesmundo, M. Attariyan, and S. Gelly,
“Parameter-efficient transfer learning for nlp,” in _Proceedings_
_of_ _the_ _36th_ _International_ _Conference_ _on_ _Machine_ _Learn-_
_ing_ . PMLR, 2019, pp. 2790–2799. [Online]. Available:
[https://proceedings.mlr.press/v97/houlsby19a.html](https://proceedings.mlr.press/v97/houlsby19a.html)


[14] E. J. Hu, Y. Shen, P. Wallis, Z. Allen-Zhu, Y. Li, S. Wang,
L. Wang, and W. Chen, “Lora: Low-rank adaptation of
large language models,” _arXiv preprint arXiv:2106.09685_, 2021.

[Online]. Available: [https://arxiv.org/abs/2106.09685](https://arxiv.org/abs/2106.09685)


[15] M. Qian, S. Tang, R. Ma, K. M. Knill, and M. J. F. Gales, “Learn
and don’t forget: Adding a new language to asr foundation models,” in _Proc. Interspeech 2024_, 2024, pp. 2544–2548.




[16] C.-H. H. Yang, B. Li, Y. Zhang, N. Chen, R. Prabhavalkar,
T. N. Sainath, and T. Strohman, “From english to more languages: Parameter-efficient model reprogramming for crosslingual speech recognition,” in _ICASSP_ _2023_ _-_ _2023_ _IEEE_ _Inter-_
_national Conference on Acoustics, Speech and Signal Processing_
_(ICASSP)_, 2023, pp. 1–5.


[17] Z. Song _et_ _al._, “Parameter-efficient and extensible multilingual
asr,” in _Proc. Interspeech 2024_ [, 2024. [Online]. Available: https://](https://www.isca-archive.org/interspeech_2024/song24_interspeech.pdf)
[www.isca-archive.org/interspeech](https://www.isca-archive.org/interspeech_2024/song24_interspeech.pdf) 2024/song24 ~~i~~ nterspeech.pdf


[18] A. Prasad, S. Dalmia, A. Narayanan _et al._, “Speech and language
recognition with low-rank adaptation of large acoustic models,” in
_Proc._ _Interspeech_ _2024_, 2024. [Online]. Available: [https://www.](https://www.isca-archive.org/interspeech_2024/prasad24_interspeech.pdf)
isca-archive.org/interspeech [2024/prasad24](https://www.isca-archive.org/interspeech_2024/prasad24_interspeech.pdf) ~~i~~ nterspeech.pdf


[19] R. Bagat, I. Illina, and E. Vincent, “Mixture of lora experts
for low-resourced multi-accent automatic speech recognition,” in
_Proc. Interspeech 2025_, 2025, pp. 1143–1147.


[20] T. Xu, K. Huang, P. Guo, Y. Zhou, L. Huang, H. Xue, and L. Xie,
“Towards rehearsal-free multilingual asr: A lora-based case study
on whisper,” in _Proc. Interspeech 2024_, 2024, pp. 2534–2538.


[21] Y. Xiao, E.-J. Holden, and T. Dang, “Adapting where it
matters: Depth-aware adaptation for efficient multilingual
speech recognition in low-resource languages,” _arXiv_ _preprint_
_arXiv:2602.01008_, 2026.


[22] A. Bhattacharjee, S. Ghosh, T. Rebedea, and C. Parisien, “Towards inference-time category-wise safety steering for large language models,” _arXiv preprint arXiv:2410.01174_, 2024.


[23] T. Marshall, A. Scherlis, and N. Belrose, “Refusal in llms is an
affine function,” _arXiv preprint arXiv:2411.09003_, 2024.


[24] W. Wang, J. Yang, and W. Peng, “Semantics-adaptive activation
intervention for llms via dynamic steering vectors,” _arXiv preprint_
_arXiv:2410.12299_, 2024.


[25] A. M. Turner, L. Thiergart, G. Leech, D. Udell, U. Mini, and
M. MacDiarmid, “Activation addition: Steering language models
without optimization,” 2024.


[26] A. Zou, L. Phan, S. Chen, J. Campbell, P. Guo, R. Ren, A. Pan,
X. Yin, M. Mazeika, A.-K. Dombrowski _et_ _al._, “Representation
engineering: A top-down approach to ai transparency,” _arXiv_
_preprint arXiv:2310.01405_, 2023.


[27] N. Rimsky, N. Gabrieli, J. Schulz, M. Tong, E. Hubinger, and
A. Turner, “Steering llama 2 via contrastive activation addition,”
in _Proceedings of the 62nd Annual Meeting of the Association for_
_Computational_ _Linguistics_ _(Volume_ _1:_ _Long_ _Papers)_, 2024, pp.
15 504–15 522.


[28] G. Ilharco, M. T. Ribeiro, M. Wortsman, L. Schmidt, H. Hajishirzi, and A. Farhadi, “Editing models with task arithmetic,”
in _The Eleventh International Conference on Learning Represen-_
_tations_, 2023.


[29] Y. Chu, J. Xu, Q. Yang, H. Wei, X. Wei, Z. Guo, Y. Leng, Y. Lv,
J. He, J. Lin, C. Zhou, and J. Zhou, “Qwen2-audio technical
report,” _ArXiv_, vol. abs/2407.10759, 2024. [Online]. Available:
[https://api.semanticscholar.org/CorpusID:271213498](https://api.semanticscholar.org/CorpusID:271213498)


[30] J. Kominek and A. W. Black, “The cmu arctic speech databases,”
in _Speech_ _Synthesis_ _Workshop_, 2004. [Online]. Available:
[https://api.semanticscholar.org/CorpusID:7750363](https://api.semanticscholar.org/CorpusID:7750363)


[31] A. Pasad, J.-C. Chou, and K. Livescu, “Layer-wise analysis of a
self-supervised speech representation model,” in _2021 IEEE Auto-_
_matic Speech Recognition and Understanding Workshop (ASRU)_ .
IEEE, 2021, pp. 914–921.


[32] A. Pasad, B. Shi, and K. Livescu, “Comparative layer-wise analysis of self-supervised speech models,” in _ICASSP_ _2023-2023_
_IEEE_ _International_ _Conference_ _on_ _Acoustics,_ _Speech_ _and_ _Signal_
_Processing (ICASSP)_ . IEEE, 2023, pp. 1–5.


