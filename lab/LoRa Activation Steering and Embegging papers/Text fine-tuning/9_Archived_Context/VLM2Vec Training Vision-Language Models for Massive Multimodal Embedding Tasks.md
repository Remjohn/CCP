Manuscript

## VLM2VEC: TRAINING VISION-LANGUAGE MODELS
### FOR MASSIVE MULTIMODAL EMBEDDING TASKS


**Ziyan Jiang** [1] _[∗]_ **, Rui Meng** [2] **, Xinyi Yang** [2] **, Semih Yavuz** [2] **, Yingbo Zhou** [2] **, Wenhu Chen** [1]

1University of Waterloo, 2Salesforce Research
ziyanjiang528@gmail.com, ruimeng@salesforce.com, wenhuchen@uwaterloo.ca


[https://tiger-ai-lab.github.io/VLM2Vec/](https://tiger-ai-lab.github.io/VLM2Vec/)


ABSTRACT


Embedding models have been crucial in enabling various downstream tasks such
as semantic similarity, information retrieval, and clustering. Recently, there has
been a surge of interest in developing universal text embedding models that can
generalize across tasks (e.g., MTEB). However, progress in learning universal
multimodal embedding models has been relatively slow despite its importance
and practicality. In this work, we aim to explore the potential of building universal multimodal embeddings capable of handling a wide range of downstream
tasks. Our contributions are two fold: (1) we propose MMEB (Massive Multimodal Embedding Benchmark), which covers 4 meta-tasks (i.e. classification,
visual question answering, multimodal retrieval, and visual grounding) and 36
datasets, including 20 training datasets and 16 evaluation datasets covering both
in-distribution and out-of-distribution tasks, and (2) VL M2VE C (Vision-Language
Model _→_ Vector), a contrastive training framework that converts any visionlanguage model into an embedding model via contrastive training on MMEB.
Unlike previous models such as CLIP or BLIP, which encodes text or images
independently without any task instruction, VL M2VE C can **process** **any** **combi-**
**nation** **of** **images** **and** **text** to generate a fixed-dimensional vector **based** **on** **the**
**given task instructions** . We build a series of VL M2VE C models on SoTA VLMs
like Phi-3.5-V, LLaVA-1.6 and evaluate them on MMEB’s evaluation split. With
LoRA tuning, VLM2VEC can achieve an improvement of 10% to 20% over existing multimodal embedding models on MMEB evaluation sets. We show that
VLMs are secretly strong embedding models.


1 INTRODUCTION


Embeddings, or distributed representations, encode inputs (whether text or images) as
fixed-dimensional vectors, enabling a range of downstream tasks. Since the advent of
Word2Vec (Mikolov, 2013) and GloVe (Pennington et al., 2014), substantial research efforts have
focused on learning textual embeddings (Kiros et al., 2015; Conneau et al., 2017) and image embeddings (Radford et al., 2021; Li et al., 2022; Jia et al., 2021; Yu et al., 2022). These embeddings
facilitate a variety of applications, including textual and visual semantic similarity (Agirre et al.,
2012; Marelli et al., 2014; Chechik et al., 2010; Cer et al., 2017), information retrieval (Mitra et al.,
2017; Karpukhin et al., 2020; Lin et al., 2014), automatic evaluation (Zhang et al., 2020; Sellam
et al., 2020), prompt retrieval for in-context learning (Liu et al., 2022; Rubin et al., 2022; Hongjin
et al., 2022), and retrieval-augmented generation (Lewis et al., 2020; Guu et al., 2020; Izacard &
Grave, 2020). A recent shift in research has focused on developing universal embeddings that can
generalize across a wide range of tasks. For instance, Muennighoff et al. (2023) introduced MTEB
(Massive Text Embedding Benchmark) to comprehensively assess text embeddings across tasks such
as classification and clustering. MTEB has become the standard for evaluating universal text embeddings. Recent works (Wang et al., 2022a; Su et al., 2023; Wang et al., 2024; Springer et al.,
2024; BehnamGhader et al., 2024) have demonstrated promising results on the MTEB benchmark.
However, progress in multimodal embeddings has been relatively slower. Despite advancements


_∗_ Work done during an internship at University of Waterloo in collaboration with Salesforce Research. Corresponding authors are Ziyan Jiang, Rui Meng and Wenhu Chen


1


Manuscript

























Figure 1: We develop a universal multimodal embedding benchmark, MMEB, along with
VL M2VEC, an embedding model adapted from vision-language models (VLMs). VL M2VE C is capable of following instructions and performing various multimodal embedding tasks, accommodating
any combination of image and text modalities.


in text embeddings, the lack of both benchmarks and methodologies in the multimodal embedding
domain remains a challenge.


Current research in multimodal embeddings faces two primary limitations: (1) existing studies typically evaluate visual embeddings on isolated tasks, such as ImageNet classification (Deng et al.,
2009; Hendrycks et al., 2021a;b) or MSCOCO/Flickr retrieval (Lin et al., 2014; Plummer et al.,
2015); (2) most existing models, such as CLIP (Radford et al., 2021), BLIP (Li et al., 2022), and
SigLIP (Zhai et al., 2023), either process text and images separately or perform shallow fusion of
visual and textual information (Wei et al., 2023), limiting their ability to fully capture the relationships between text and image modalities. Furthermore, these models exhibit limited reasoning and
generalization capabilities, particularly in zero-shot scenarios for complex reasoning tasks.


In this paper, we attempt to build an universal multimodal embedding framework to pave road for
the future research, which consists of two efforts:


**- MMEB:** We introduce a novel benchmark, MMEB (Massive Multimodal Embedding Benchmark),
which includes 36 datasets spanning four meta-task categories: classification, visual question answering, retrieval, and visual grounding. MMEB provides a comprehensive framework for training
and evaluating embedding models across various combinations of text and image modalities. All
tasks are reformulated as ranking tasks, where the model follows instructions, processes a query,
and selects the correct target from a set of candidates. The query and target can be an image, text,
or a combination of both. MMEB is divided into 20 in-distribution datasets, which can be used for
training, and 16 out-of-distribution datasets, reserved for evaluation.


**- VL M2VEC:** We adopt the pre-trained vision-language models like Phi-3.5-V (Abdin et al., 2024)
and LLaVA-1.6 (Li et al., 2024) as the backbone for VL M2VE C. In contrast to other multimodal
embedding models like UniIR (Wei et al., 2023) and MagicLens (Zhang et al., 2024), which rely
on late fusion of CLIP (Radford et al., 2021) features, our approach leverages the deep integration
of vision and language features within a transformer architecture. There are several advantages to
this approach: (1) VLMs are trained on massive multimodal datasets and can handle any combination of images and text, as well as high-resolution images and long text inputs; (2) vision and
language features are deeply fused in the transformer model, improving the model’s ability to capture cross-modal relationships; and (3) these models are well-suited for generalizing across diverse
tasks, particularly those requiring instruction-following capabilities. These factors make VL M2VE C
an ideal choice for task generalization. We trained VL M2VE C on the 20 MMEB training datasets
using contrastive learning and compared its performance with various baselines.


2


Manuscript


Following extensive contrastive training, **VL M2VE C** **can** **handle** **any** **combination** **of** **images** **and**
**text,** **producing** **fixed-dimensional** **vectors** . We evaluate VL M2VE C against a wide array of multimodal embedding models, including CLIP (Radford et al., 2021), BLIP2 (Li et al., 2023a),
SigLIP (Zhai et al., 2023), MagicLens (Zhang et al., 2024), UniIR (Wei et al., 2023) and E5-V (Jiang
et al., 2024), demonstrating consistent improvements across all task categories. Notably, compared
to the best baseline model without fine-tuning, our model achieves a 18.2 point improvement (from
44.7 to 62.9) across all 36 MMEB datasets and a 15.4-point increase (from 41.7 to 57.1) on 16 out-ofdistribution datasets for zero-shot evaluation. Compared to the best baseline model with fine-tuning,
our model achieves a 15.7 point improvement (from 47.2 to 62.9) across all 36 MMEB datasets and
a 14.0-point increase (from 43.1 to 57.1) on 16 out-of-distribution datasets for zero-shot evaluation.
Moreover, as a general multimodal representation model, VL M2VE C can still achieve competitive
zero-shot T2I (Text-to-Image) and I2T (Image-to-Text) performance on Flickr30K compared to existing CLIP-like models, as presented in Table 11.


2 MMEB: A BENCHMARK FOR MULTIMODAL EMBEDDINGS


2.1 DATASET OVERVIEW


We present MMEB (Massive Multimodal Embedding Benchmark), a comprehensive benchmark
designed to evaluate multimodal embeddings across a diverse set of tasks. MMEB consists of 36
datasets organized into four meta-tasks: classification, visual question answering, retrieval, and
visual grounding. Each task is reformulated as a ranking problem, where the model is provided with
an instruction and a query (which may consist of text, images, or both) and is tasked with selecting
the correct answer from a set of candidates. These candidates could be text, images, or additional
instructions. The datasets are divided into two categories: 20 in-distribution datasets for training and
16 out-of-distribution datasets for evaluation. We report performance metrics across all 36 tasks. An
overview of MMEB is provided in Figure 2 and the dataset statistics are provided in Table 1.


The embedding models are supposed to compress the query side into a vector and the target candidates into a set of vectors. The candidate with the highest dot-product will be selected as the
prediction for evaluation. We measure the Precision@1 to reflect the percentage of top candidate
matching the groundtruth. For the number of target candidates, a higher count could increase evaluation costs and hinder rapid model iteration, while a lower count might make the benchmark too
simple and prone to saturation. To strike a balance between these extremes, we have chosen 1,000
candidates. Further details about this decision can be found in Section A.2.


MMEB offers a wide range of tasks from various domains, such as common, news, Wikipedia,
web, and fashion. The benchmark incorporates diverse combinations of modalities for both queries
and targets, including text, images, and text-image pairs. Additionally, tasks are designed to follow
different types of instructions. For instance, tasks may involve object recognition (e.g., _“Identify the_
_object_ _shown_ _in_ _the_ _image.”_ ), retrieval (e.g., _“Find_ _an_ _image_ _that_ _matches_ _the_ _given_ _caption.”_ ), or
visual grounding (e.g., _“Select the portion of the image that answers the question.”_ ). Examples for
each dataset in MMEB are provided in Tables 7, 8, 9 and 10. The diversity in MMEB makes it an
ideal testbed for universal embeddings.


2.2 META-TASK AND DATASET DESIGN


MMEB is organized into four primary meta-task categories:


**Classification** The query consists of an instruction, an image, optionally accompanied by related
text, while the target is the class label. The number of candidates equals the number of classes.


**Visual Question Answering** The query consists of an instruction, an image, and a piece of text as
the question, while the target is the answer. Each query has 1 ground truth and 999 distractors as
candidates.


**Information Retrieval** Both the query and target sides can involve a combination of text, images,
and instructions. Each query has 1 ground truth and 999 distractors as candidates.


**Visual** **Grounding** The category is adapted from object detection tasks. The query combines an
instruction (e.g., “Select the portion of the image that isolates the object of the given label: red


3


Manuscript


Table 1: The statistics of MMEB: 36 datasets across 4 meta-task categories, with 20 in-distribution
datasets used for training and 16 out-of-distribution datasets used exclusively for evaluation.






|Meta-Task|Dataset|Query|Target|OOD?|#Training|#Eval|#Candidates|
|---|---|---|---|---|---|---|---|
|Classifcation<br>(10 Tasks)|ImageNet-1K|I|T||100K|1000|1000|
|Classifcation<br>(10 Tasks)|N24News|I + T|I||49K|1000|24|
|Classifcation<br>(10 Tasks)|HatefulMemes|I|T||8K|1000|2|
|Classifcation<br>(10 Tasks)|VOC2007|I|T||8K|1000|20|
|Classifcation<br>(10 Tasks)|SUN397|I|T||20K|1000|397|
|Classifcation<br>(10 Tasks)|Place365|I|T|✓|-|1000|365|
|Classifcation<br>(10 Tasks)|ImageNet-A|I|T|✓|-|1000|1000|
|Classifcation<br>(10 Tasks)|ImageNet-R|I|T|✓|-|1000|200|
|Classifcation<br>(10 Tasks)|ObjectNet|I|T|✓|-|1000|313|
|Classifcation<br>(10 Tasks)|Country-211|I|T|✓|-|1000|211|
|VQA<br>(10 Tasks)|OK-VQA|I + T|T||9K|1000|1000|
|VQA<br>(10 Tasks)|A-OKVQA|I + T|T||17K|1000|1000|
|VQA<br>(10 Tasks)|DocVQA|I + T|T||40K|1000|1000|
|VQA<br>(10 Tasks)|InfographicVQA|I + T|T||24K|1000|1000|
|VQA<br>(10 Tasks)|ChartQA|I + T|T||28K|1000|1000|
|VQA<br>(10 Tasks)|Visual7W|I + T|T||70K|1000|1000|
|VQA<br>(10 Tasks)|ScienceQA|I + T|T|✓|-|1000|1000|
|VQA<br>(10 Tasks)|VizWiz|I + T|T|✓|-|1000|1000|
|VQA<br>(10 Tasks)|GQA|I + T|T|✓|-|1000|1000|
|VQA<br>(10 Tasks)|TextVQA|I + T|T|✓|-|1000|1000|
|Retrieval<br>(12 Tasks)|VisDial|T|I||123K|1000|1000|
|Retrieval<br>(12 Tasks)|CIRR|I + T|I||26K|1000|1000|
|Retrieval<br>(12 Tasks)|VisualNews ~~t~~2i|T|I||100K|1000|1000|
|Retrieval<br>(12 Tasks)|VisualNews ~~i~~2t|I|T||100K|1000|1000|
|Retrieval<br>(12 Tasks)|MSCOCO ~~t~~2i|T|I||100K|1000|1000|
|Retrieval<br>(12 Tasks)|MSCOCO ~~i~~2t|I|T||113K|1000|1000|
|Retrieval<br>(12 Tasks)|NIGHTS|I|I||16K|1000|1000|
|Retrieval<br>(12 Tasks)|WebQA|T|I + T||17K|1000|1000|
|Retrieval<br>(12 Tasks)|OVEN|I + T|I + T|✓|-|1000|1000|
|Retrieval<br>(12 Tasks)|FashionIQ|I + T|I|✓|-|1000|1000|
|Retrieval<br>(12 Tasks)|EDIS|T|I + T|✓|-|1000|1000|
|Retrieval<br>(12 Tasks)|Wiki-SS-NQ|T|I|✓|-|1000|1000|
|Visual Grounding<br>(4 Tasks)|MSCOCO|I + T|I||100K|1000|1000|
|Visual Grounding<br>(4 Tasks)|Visual7W-Pointing|I + T|I|✓|-|1000|1000|
|Visual Grounding<br>(4 Tasks)|RefCOCO|I + T|I|✓|-|1000|1000|
|Visual Grounding<br>(4 Tasks)|RefCOCO-Matching|I + T|I + T|✓|-|1000|1000|



apple”) with the full image. This instruction guides the model to focus on a specific object within
the image. Each candidate corresponds to cropped regions (bounding boxes) of the image, including
both the object of interest and distractor regions. Each query includes 1,000 candidates: 1 ground
truth and 999 distractors. These distractors may include hard negatives from the same object class,
other objects in the image, or random objects from different images.


Further details on dataset processing can be found in Section A.1.


3 VL M2VE C: TRANSFORMING LVMS TO EMBEDDERS


3.1 CONTRASTIVE TRAINING


We develop VLM2VEC, a contrastive training framework designed to convert any state-of-the-art
vision-language model into an embedding model, as illustrated in Figure 3. A relevant query-target
pair is denoted as ( _q, t_ [+] ). Both _q_ and _t_ [+] could be either single image, text or single image + text.
We define _q_ : ( _qt, qi_ ) and _t_ [+] : ( _t_ [+] _t_ _[, t]_ _i_ [+][)][.]


We then apply the instruction to the original query _q_ to generate a new one _q_ inst:


_q_ inst = [IMAGE ~~T~~ OKEN]Instruct: _{task_ ~~_d_~~ _efinition} \n_ Query: _{q}_ (1)


4


Manuscript















































Figure 2: An overview of the tasks and datasets in MMEB. MMEB includes four meta-tasks and
36 datasets: 20 in-distribution datasets (blue) used for training and 16 out-of-distribution (orange)
datasets used exclusively for evaluation.


where “ _{task_ ~~_d_~~ _efinition}_ ” is a placeholder for a one-sentence description of the embedding task.
To enhance the embedding model’s generalizability by better understanding instructions, we have
crafted task-specific instructions, as shown in Tables 7, 8, 9 and 10.


Given a pretrained VLM, we feed query and target into it to obtain the query and target embeddings
( **h** _q_ inst _,_ **h** _t_ +) by taking the last layer vector representation of the last token. To train the embedding
model, we adopt the standard InfoNCE loss _L_ over the in-batch negatives and hard negatives:



min _L_ = _−_ log _ϕ_ ( **h** _q_ inst _,_ **h** _t_ +)



inst (2)


( _ϕ_ ( **h** _q_ inst _,_ **h** _t−_ ))
_t_ _[−]_ _∈_ N




   _ϕ_ ( **h** _q_ inst _,_ **h** _t_ +) +



where N denotes the set of all negatives, and _ϕ_ ( **h** _q,_ **h** _t_ ) is a function that computes the matching
score between query _q_ and target _t_ . In this paper, we adopt the temperature-scaled cosine similarity
function as _ϕ_ ( **h** _q,_ **h** _t_ ) = exp( _τ_ [1] [cos(] **[h]** _[q][,]_ **[ h]** _[t]_ [))][,where] _[ τ]_ [is a temperature hyper-parameter.]


3.2 INCREASING BATCH SIZE THROUGH GRADCACHE


Since hard negatives are often difficult or ambiguous to collect for most multimodal datasets, using
larger batch sizes becomes crucial. This increases the number of in-batch random negatives, which
in turn helps improve the performance of the embedding model.


A bottleneck lies in the GPU memory that limits us from increasing the batch size and the number
of in-batch random negatives during training, as each training instance may include one image (either from the query or target side) or multiple images (from both query and target sides), resulting in
substantial memory consumption. We apply GradCache (Gao et al., 2021a), a gradient caching technique that decouples backpropagation between contrastive loss and the encoder, removing encoder
backward pass data dependency along the batch dimension.


Mathematically, supposed we have a large batch of queries _Q_, and we divide it into a set of subbatches, each of which can fit into memory for gradient computation: _Q_ = _{Q_ [ˆ] 1 _,_ _Q_ [ˆ] 2 _, . . . }_ . There
are two major steps: “Representation Gradient Computation and Caching” and “Sub-batch Gradient
Accumulation”. First, gradient tensors within each subbatch is calculated and stored: **u** _i_ = _∂f∂_ ( _Lqi_ ) [.]


Then gradients are accumulated for encoder parameters across all sub-batches:



_∂L_ - _∂_ Θ [=]

_Q_ ˆ _j_ _∈Q_ _qi∈Q_ [ˆ] _j_



_∂L_ _∂f_ ( _qi_ )
_∂f_ ( _qi_ ) _∂_ Θ



_Q_ ˆ _j_ _∈_ Q



_i_ =   
_∂_ Θ








- **u** _i_ _∂f_ ( _qi_ )

_∂_ Θ

_qi∈Q_ [ˆ] _j_



_∂_ Θ (3)



5


Manuscript

















Figure 3: VLM2VEC uses a VLM as the backbone to deeply integrate image and text features. It
is trained with a contrastive loss between the query and target, following task-specific instructions.
The training data consists of diverse combinations of modalities on both the query and target sides,
which may include images, text, or image-text pairs.


4 EXPERIMENTS


In this section, we adopt Phi-3.5-V and LLaVA-1.6 as the backbone VLMs, with training conducted
via either full model fine-tuning or LoRA. The temperature for the loss function is set to 0.02, with a
batch size of 1,024, a maximum text length of 256 tokens, and 2K training steps. The LoRA variant
uses a rank of 8. For VLM2VEC leveraging Phi-3.5-V as the backbone, we configure the number of
sub-image crops to 4. For VLM2VEC using LLaVA-1.6 as the backbone, we resize the input images
to a uniform resolution, employing two setups: a high-resolution configuration of 1344 × 1344 and
a low-resolution configuration of 336 × 336.


For the 20 training datasets, if a dataset contains more than 50K samples, we randomly select 50K
for consistency, resulting in a total training set of 662K data points. When using GradCache, we set
a sub-batch size of 4 to enable full model tuning, with the total batch size accumulated to 1,024. All
experiments were run on 8 H100 GPUs.


We report Precision@1 for all models in Table 2. It measures the ratio of positive candidates being
ranked in the top place for all queries.


4.1 BASELINES


Four groups of baselines are reported in this study.


**CLIP-family:** We utilize vision/language encoders such as CLIP (Radford et al., 2021), OpenCLIP (Cherti et al., 2023), SigLIP (Zhai et al., 2023), and BLIP2 (Li et al., 2023a) as our baseline.
Due to the length limitations of the text encoder, some queries or target text in certain tasks may
be truncated. We apply score-level fusion by combining multimodal features using element-wise
addition with equal weights ( _w_ 1 = _w_ 2 = 1). We do not use instructions, as they could potentially
degrade performance. For more details, please refer to Section 4.3.4.


**UniIR:** UniIR (Wei et al., 2023) is a unified, instruction-guided multimodal retriever designed to
handle eight different retrieval tasks across multiple modalities. The model builds on CLIP and
BLIP, employing shallow fusion techniques such as score-level and feature-level fusion to integrate
modalities. In this study, we use the CLIP ~~S~~ F and BLIP ~~F~~ F variations as baselines.


**MagicLens:** MagicLens (Zhang et al., 2024) is a self-supervised image retrieval model capable of
handling open-ended instructions. It utilizes a dual-encoder architecture with shared parameters,
initializing the vision and language encoders with either CoCa or CLIP. The model uses a multihead attention pooler to unify multimodal inputs into a single embedding. For this study, we report
results using the CLIP-Large backbone.


**E5-V:** E5-V (Jiang et al., 2024) is a contemporary model that also leverages vision-language models
for multimodal embedding tasks. It proposes a single-modality training approach, where the model
is trained exclusively on text pairs. In contrast, our model is trained on multimodal pairs, which
include various combinations of image and text modalities on both the query and target sides.


6


Manuscript


For all our baselines, we first use their original versions. Additionally, we have fine-tuned both
CLIP and OpenCLIP on MMEB training datasets. We adopt the same experimental configurations
as VLM2VEC to ensure a fair comparison. For the remaining baseline models, UniIR and MagicLens
also utilize a shallow fusion approach based on CLIP models, with their primary contribution being
the datasets they were trained on. E5-V proposes training exclusively on text pairs, making it unsuitable for fine-tuning on our datasets. Therefore, we have not included the fine-tuned versions of
these three models in this comparison.


4.2 MAIN RESULT


Table 2: Results on the MMEB benchmark. The scores are averaged per meta-task. For detailed
scores per dataset, see Table 6. We include baselines with and without fine-tuning on MMEB training
datasets and our models with LLaVA-1.6 and Phi-3.5 backbones. FFT means fully fine-tuned.


**Per Meta-Task Score** **Average Score**
**Model**

Classification VQA Retrieval Grounding IND OOD Overall


# of datasets _→_ 10 10 12 4 20 16 36


_Baseline Models (No Fine-tuning on MMEB Training)_


CLIP (Radford et al., 2021) 42.8 9.1 53.0 51.8 37.1 38.7 37.8
BLIP2 (Li et al., 2023a) 27.0 4.2 33.9 47.0 25.3 25.1 25.2
SigLIP (Zhai et al., 2023) 40.3 8.4 31.6 59.5 32.3 38.0 34.8
OpenCLIP (Cherti et al., 2023) 47.8 10.9 52.3 53.3 39.3 40.2 39.7
UniIR (BLIP ~~F~~ F) (Wei et al., 2023) 42.1 15.0 60.1 62.2 44.7 40.4 42.8
UniIR (CLIP ~~S~~ F) (Wei et al., 2023) 44.3 16.2 61.8 65.3 47.1 41.7 44.7
E5-V (Jiang et al., 2024) 21.8 4.9 11.5 19.0 14.9 11.5 13.3
Magiclens (Zhang et al., 2024) 38.8 8.3 35.4 26.0 31.0 23.7 27.8


_Baseline Models (Fine-tuning on MMEB Training)_


CLIP-FFT 55.2 19.7 53.2 62.2 47.6 42.8 45.4
OpenCLIP-FFT 56.0 21.9 55.4 64.1 50.5 43.1 47.2


_Ours (_ VL M2VE C _)_


Phi-3.5-V, FFT (bs=1024) 52.8 50.3 57.8 72.3 62.8 47.4 55.9


From Table 2, the best variant of VLM2VE C leverages LLaVA-1.6, is trained with LoRA, and processes input images at a relatively high resolution of 1344 × 1344. It achieves an average precision@1 of 62.9% across all 36 datasets from MMEB. Additionally, it maintains an average precision@1 of 57.1% on 16 out-of-distribution tasks in zero-shot evaluation, suggesting strong generalization ability. This indicates that our model, when well-trained on datasets from diverse task
categories, domains, and modality combinations, can effectively follow instructions to align the
visual and text spaces and generalize well to unseen tasks. It is important to emphasize that LLaVA1.6 (Li et al., 2024) has a transparent pre-training data recipe and nearly no overlap with our MMEB
OOD datasets. This demonstrates that the strong zero-shot results achieved by VL M2VE C are not
attributable to prior exposure of the LLaVA-1.6 backbone to the OOD datasets. When using the
same backbone, the full fine-tuning variant achieves slightly lower scores than the LoRA version.
For a detailed discussion comparing full fine-tuning and LoRA, please refer to Section 4.3.1.


Compared to other baseline models, with or without fine-tuning on MMEB training data, our model
demonstrates consistent improvements. Compared to the best baseline model without fine-tuning,
our model achieves a 18.2 point improvement (from 44.7 to 62.9) across all 36 MMEB datasets and
a 15.4-point increase (from 41.7 to 57.1) on 16 out-of-distribution datasets for zero-shot evaluation.
Compared to the best baseline model with fine-tuning, our model achieves a 15.7 point improvement
(from 47.2 to 62.9) across all 36 MMEB datasets and a 14.0-point increase (from 43.1 to 57.1) on 16
out-of-distribution datasets for zero-shot evaluation. Additionally, unlike the baseline models, which
fail to demonstrate reasonable performance across all different task categories, VL M2VE C achieves
relatively strong performance (at least 50%) across all four meta-task categories. This highlights its
capability to handle a wide range of multimodal embedding tasks effectively.


7


Manuscript


4.3 RESULT ANALYSIS


To train an effective and generalizable multimodal embedding, various factors need to be considered,
ranging from the data to the training setup. In this section, we present detailed ablation studies on
these factors. We will discuss two training setups: Full Fine-Tuning vs. LoRA, along with Training
parameters, and two topics related to data: Meta-task generalization and Impact of instructions.


4.3.1 FULL FINE-TUNING VS. LORA


When fine-tuning the VLMs, a key decision is whether to conduct full fine-tuning, which updates
all parameters in the model, or to use a parameter-efficient method such as LoRA. We compare
the performance of fully fine-tuned VL M2VE C with its LoRA variants at different ranks. The training and data setups are kept consistent across all models. We observe that LoRA achieves better
performance when the rank is appropriately configured.


Table 3: We compare the performance of fully fine-tuned VL M2VE C with its LoRA variants at
different ranks. LoRA can achieve better performance when the rank is appropriately configured.
All the models utilize Phi-3.5-V as their backbone.


**Meta-Task Average Score** **Average Score**
**Model**

Classification VQA Retrieval Grounding IND OOD Overall


# of datasets _→_ 10 10 12 4 20 16 36


Full Fine-Tuning (bs=256) 50.4 46.4 52.6 68.6 57.9 44.7 52.0
LoRA r = 4 (bs=256) 52.7 **53.6** **60.1** **80.2** **64.9** **50.4** **58.4**
LoRA r = 8 (bs=256) **52.9** 52.5 60.3 80.0 64.2 50.8 58.2
LoRA r = 16 (bs=256) 51.1 40.5 52.0 72.5 54.9 45.8 50.8
LoRA r = 32 (bs=256) 50.6 47.8 53.9 72.5 58.9 46.5 53.4


4.3.2 TRAINING PARAMETERS


During our experiments, we identified three key parameters that significantly impact the performance of VLM2VEC: training batch size, the number of sub-image crops, and the number of training
steps. In Figure 4, we observe that the final performance gradually improves as we increase the
batch size, training step size, and number of sub-image crops. We particularly want to highlight
the impact of batch size. Due to the lack of hard negatives, using a large batch size with plenty
of random negatives, supported by the GradCache technique, plays a crucial role in enhancing the
performance of VLM2VEC, as discussed in Section 3.2.



56


54


52


50

|Batch|h Size In|nfluence|e on Pe|erforma|ance|
|---|---|---|---|---|---|
|||||||
|||||||
|||||||
|||||||



Batch Size



Number of Crops Influence on Performance


54


52


50


48

|Col1|Col2|Col3|Col4|
|---|---|---|---|
|||||
|||||
|||||
|||||



Number of Crops



55


54


53


52


51


50



Step Size Influence on Performance

|Col1|Col2|Col3|Col4|Col5|
|---|---|---|---|---|
||||||
||||||
||||||
||||||
||||||
||||||



Step Size



Figure 4: The figures demonstrate the influence of the training setup on VL M2VE C’s final performance. Here, we examine the effects of training batch size, the number of sub-image crops, and the
number of training steps. All the models utilize Phi-3.5-V as their backbone.


8


Manuscript


4.3.3 META-TASK GENERALIZATION


We have demonstrated that VLM2VE C has the potential to transfer to out-of-distribution datasets
after being trained on a diverse range of in-distribution datasets, with the instruction-following settings. An interesting question arises as to whether focusing on a specific meta-task can enhance the
model’s overall generalizability. We have trained three models, each focused solely on one meta-task
(classification, visual question answering, and retrieval). Visual grounding was not included due to
the limited number of training datasets. We then evaluated the models’ transferability to other metatasks. We refer to these three models as VL M2VE C RET, trained on 8 retrieval tasks, VL M2VE C VQA,
trained on 6 visual question answering tasks, and VL M2VE C CLS, trained on 5 classification tasks.


Figure 5 illustrates the generalizability of these three models on unseen meta-tasks. We could observe that VLM2VEC RET has better generalizablilty on other meta-task, compared with other two
models, especially on visual grounding categories. The reason is that retrieval tasks involve a more
diverse combination of text and visual modalities from both the query and target sides, which helps
the model generalize better to unseen meta-tasks. This observation highlights the benefits of using
more diverse tasks in the VLM2VEC training process.



VLM2VecVQA vs VLM2VecRET



VLM2VecRET vs VLM2VecCLS





60


50


40


30


20


10



VLM2VecVQA vs VLM2VecCLS





60


50


40


30


20


10


|VLM2VecVQA|Col2|
|---|---|
|VLM2VecRET|VLM2VecRET|
|||


|VLM2VecVQA|Col2|
|---|---|
|VLM2VecCLS|VLM2VecCLS|
|||


|VLM2VecRET|Col2|
|---|---|
|VLM2VecCLS|VLM2VecCLS|
|||









60


50


40


30


20


10















0



0



0


|VLM2VecVQA VLM2VecRET|Col2|Col3|Col4|51.3|Col6|
|---|---|---|---|---|---|
|||||||
|~~35.9~~<br>33.3<br>29.1|~~35.9~~<br>33.3<br>29.1|~~35.9~~<br>33.3<br>29.1|~~35.9~~<br>33.3<br>29.1|||
|||||||
|||||||
|||||||
|||||||
|||||||


|VLM2VecVQA VLM2VecCLS|Col2|Col3|Col4|Col5|Col6|
|---|---|---|---|---|---|
|||||||
|33.0<br>~~35.1~~|33.0<br>~~35.1~~|33.0<br>~~35.1~~|33.0<br>~~35.1~~|33.0<br>~~35.1~~|33.0<br>~~35.1~~|
|33.0<br>~~35.1~~|33.0<br>~~35.1~~|33.0<br>~~35.1~~|33.0<br>~~35.1~~|||
|33.0<br>~~35.1~~|33.0<br>~~35.1~~|33.0<br>~~35.1~~||||
|||||||
|13.0<br>13.8|13.0<br>13.8|13.0<br>13.8||||
|||||||
|||||||


|VLM2VecRET VLM2VecCLS|Col2|Col3|51.3|Col5|Col6|
|---|---|---|---|---|---|
|||||||
|||||~~35.1~~|~~35.1~~|
|||||||
|||||||
|14.2<br>12.6|14.2<br>12.6|14.2<br>12.6||||
|||||||
|||||||



Figure 5: The figures show the generalization ability of models trained on one meta-task to other
unseen meta-tasks. For example, the first subplot compares the performance of VL M2VE C trained
exclusively on VQA datasets with VL M2VE C trained exclusively on retrieval datasets across the
other two meta-task categories: classification and visual grounding. Overall, VL M2VE C trained on
retrieval tasks demonstrate better generalization ability because retrieval tasks involve a more diverse
combination of text and visual modalities from both the query and target sides. VL M2VE C utilizes
Phi-3.5-V as its backbone.


4.3.4 IMPACT OF INSTRUCTIONS


Previous studies have shown the influence of instructions on addressing various tasks. VL M2VE C,
which leverages a VLM as its backbone and is trained on large-scale datasets with instructions,
is expected to better generalize across tasks and improve performance in multimodal embedding
tasks. In this section, we evaluate the performance of both CLIP and VL M2VE C with and without
task-specific instructions to quantify the impact of incorporating instructions into the embedding
process. As shown in Table 4, incorporating instructions reduces the CLIP model’s performance by
29.4%, while our VLM2VEC achieves a 49.4% improvement. This highlights how a VLM backbone
enhances the embedding model’s instruction-following capability and emphasizes the advantages of
instruction-guided embeddings.


5 RELATED WORK


5.1 TEXT EMBEDDING


Text embeddings have demonstrated significant potential in powering downstream applications such
as information retrieval (Karpukhin et al., 2020; Xiong et al., 2020), text similarity (Gao et al.,
2021b), prompt retrieval for in-context learning (Hongjin et al., 2022), and classification (Logeswaran & Lee, 2018; Reimers & Gurevych, 2019). Early work focused on creating effective


9


Manuscript


Table 4: Comparison of CLIP and our VL M2VE C with and without task-specific instructions. Incorporating instructions could decrease CLIP’s performance by 29.4%, whereas our VL M2VE C achieves
a 49.4% improvement. VLM2VEC utilizes Phi-3.5-V as its backbone.


**Meta-Task Average Score** **Average Score**
**Model**

Classification VQA Retrieval Grounding IND OOD Overall


# of datasets _→_ 10 10 12 4 20 16 36


_CILP_


w/o instruction 42.8 9.1 53.0 51.8 37.1 38.7 37.8


_Ours (_ VL M2VE C _)_


w/o instruction 36.7 33.5 31.1 44.3 37.3 31.6 34.8


embeddings for specific tasks. With the rise of pretrained language models, efforts have shifted toward developing universal embedding models capable of handling a wide range of embedding tasks.
Studies such as GTR (Ni et al., 2022) and E5 (Wang et al., 2022a) leveraged large amounts of noisy
paired data to pretrain and fine-tune dense retrievers. More recent works like TART (Asai et al.,
2022) and InstructOR (Su et al., 2023) introduced natural language prompts to guide embedding
models in producing task-relevant embeddings. Building on this, models like E5Mistral(Wang et al.,
2024), SFR-Embedding(Meng et al., 2024), RepLLaMA(Ma et al., 2024b), GTE-Qwen2(Li et al.,
2023b), and NV-Embed (Lee et al., 2024) have utilized pretrained large language models (LLMs)
as their backbone, fine-tuning them with multi-task data and instructions. These models have delivered significant improvements over earlier approaches that did not use LLMs for initialization or
instruction tuning.


5.2 MULTIMODAL EMBEDDINGS


Multimodal embeddings have long been a significant research challenge. Early works like
CLIP (Radford et al., 2021), BLIP (Li et al., 2022; 2023a), Align (Jia et al., 2021), SigLIP (Zhai
et al., 2023), SimVLM Wang et al. (2022b) and CoCa (Yu et al., 2022) primarily focused on learning universal representations from large-scale, weakly supervised image-text pairs. These models
generally encode images and text separately, projecting them into a shared space. This approach has
laid the groundwork for more recent multimodal models like LLaVA (Liu et al., 2024).


Most research on universal multimodal embeddings involves fine-tuning models like CLIP or BLIP,
typically using simple fusion mechanisms to combine visual and language information. For instance,
UniIR (Wei et al., 2023) creates multimodal embeddings by simply adding text and visual features,
while MagicLens (Zhang et al., 2024) employs shallow self-attention layers to integrate these features more effectively. The study most similar to ours is E5-V (Jiang et al., 2024), a contemporary
work that fine-tunes a vision-language model using only text training data.


5.3 EMBEDDING BENCHMARKS


Significant efforts have been made to develop benchmarks for evaluating retrieval systems. For text
retrieval models, MS MARCO (Nguyen et al., 2016) and Natural Questions (Kwiatkowski et al.,
2019b) are two of the most widely used benchmarks in general domains. To broaden the evaluation
across more diverse domains, BEIR (Thakur et al.) was introduced, incorporating 18 datasets from
various fields. Building on this, MTEB (Muennighoff et al., 2023) further expands BEIR’s scope by
adding more tasks, such as classification, clustering, and semantic textual similarity (STS).


For multimodal retrieval, several benchmarks have been introduced to evaluate model performance
across different modalities. MBEIR (Wei et al., 2023) includes 8 tasks and 16 datasets, designed to
test models’ ability to retrieve information based on various forms of queries and instructions.


10


Manuscript


6 CONCLUSION


In this paper, we aim to build the first large-scale multimodal embedding framework, comprising
two main components: MMEB and VL M2VE C. MMEB includes 36 datasets across four meta-task
categories, providing a comprehensive and diverse framework for training and evaluating embedding models. VLM2VEC leverages VLMs as a backbone to deeply fuse visual and textual spaces,
enhancing generalization to unseen tasks through instruction following.


11


Manuscript


REFERENCES


Marah Abdin, Sam Ade Jacobs, Ammar Ahmad Awan, Jyoti Aneja, Ahmed Awadallah, Hany
Awadalla, Nguyen Bach, Amit Bahree, Arash Bakhtiari, Harkirat Behl, et al. Phi-3 technical report: A highly capable language model locally on your phone. _arXiv preprint arXiv:2404.14219_,
2024.


Eneko Agirre, Daniel Cer, Mona Diab, and Aitor Gonzalez-Agirre. SemEval-2012 task 6: A pilot on
semantic textual similarity. In Eneko Agirre, Johan Bos, Mona Diab, Suresh Manandhar, Yuval
Marton, and Deniz Yuret (eds.), _*SEM_ _2012:_ _The_ _First_ _Joint_ _Conference_ _on_ _Lexical_ _and_ _Com-_
_putational Semantics – Volume 1:_ _Proceedings of the main conference and the shared task,_ _and_
_Volume_ _2:_ _Proceedings_ _of_ _the_ _Sixth_ _International_ _Workshop_ _on_ _Semantic_ _Evaluation_ _(SemEval_
_2012)_, pp. 385–393, Montr´eal, Canada, 7-8 June 2012. Association for Computational Linguistics. [URL https://aclanthology.org/S12-1051.](https://aclanthology.org/S12-1051)


Akari Asai, Timo Schick, Patrick Lewis, Xilun Chen, Gautier Izacard, Sebastian Riedel, Hannaneh Hajishirzi, and Wen-tau Yih. Task-aware retrieval with instructions. _arXiv_ _preprint_
_arXiv:2211.09260_, 2022.


Andrei Barbu, David Mayo, Julian Alverio, William Luo, Christopher Wang, Dan Gutfreund, Josh
Tenenbaum, and Boris Katz. Objectnet: A large-scale bias-controlled dataset for pushing the
limits of object recognition models. _Advances_ _in_ _neural_ _information_ _processing_ _systems_, 32,
2019.


Parishad BehnamGhader, Vaibhav Adlakha, Marius Mosbach, Dzmitry Bahdanau, Nicolas Chapados, and Siva Reddy. Llm2vec: Large language models are secretly powerful text encoders. _arXiv_
_preprint arXiv:2404.05961_, 2024.


Daniel Cer, Mona Diab, Eneko Agirre, I˜nigo Lopez-Gazpio, and Lucia Specia. SemEval-2017
task 1: Semantic textual similarity multilingual and crosslingual focused evaluation. In Steven
Bethard, Marine Carpuat, Marianna Apidianaki, Saif M. Mohammad, Daniel Cer, and David Jurgens (eds.), _Proceedings of the 11th International Workshop on Semantic Evaluation (SemEval-_
_2017)_, pp. 1–14, Vancouver, Canada, August 2017. Association for Computational Linguistics.
doi: 10.18653/v1/S17-2001. [URL https://aclanthology.org/S17-2001.](https://aclanthology.org/S17-2001)


Yingshan Chang, Mridu Narang, Hisami Suzuki, Guihong Cao, Jianfeng Gao, and Yonatan Bisk.
Webqa: Multihop and multimodal qa. In _Proceedings of the IEEE/CVF conference on computer_
_vision and pattern recognition_, pp. 16495–16504, 2022.


Gal Chechik, Varun Sharma, Uri Shalit, and Samy Bengio. Large scale online learning of image
similarity through ranking. _Journal of Machine Learning Research_, 11(3), 2010.


Mehdi Cherti, Romain Beaumont, Ross Wightman, Mitchell Wortsman, Gabriel Ilharco, Cade Gordon, Christoph Schuhmann, Ludwig Schmidt, and Jenia Jitsev. Reproducible scaling laws for
contrastive language-image learning. In _Proceedings of the IEEE/CVF Conference on Computer_
_Vision and Pattern Recognition_, pp. 2818–2829, 2023.


Alexis Conneau, Douwe Kiela, Holger Schwenk, Lo¨ıc Barrault, and Antoine Bordes. Supervised
learning of universal sentence representations from natural language inference data. In _Proceed-_
_ings of the 2017 Conference on Empirical Methods in Natural Language Processing_, pp. 670–680,
2017.


Abhishek Das, Satwik Kottur, Khushi Gupta, Avi Singh, Deshraj Yadav, Jos´e MF Moura, Devi
Parikh, and Dhruv Batra. Visual dialog. In _Proceedings_ _of_ _the_ _IEEE_ _conference_ _on_ _computer_
_vision and pattern recognition_, pp. 326–335, 2017.


Jia Deng, Wei Dong, Richard Socher, Li-Jia Li, Kai Li, and Li Fei-Fei. Imagenet: A large-scale hierarchical image database. In _2009 IEEE conference on computer vision and pattern recognition_,
pp. 248–255. Ieee, 2009.


Mark Everingham, S. M. Ali Eslami, Luc Van Gool, Christopher K. I. Williams, John M. Winn, and
Andrew Zisserman. The pascal visual object classes challenge: A retrospective. _International_
_Journal of Computer Vision_ [, 111:98 – 136, 2014. URL https://api.semanticscholar.](https://api.semanticscholar.org/CorpusID:207252270)
[org/CorpusID:207252270.](https://api.semanticscholar.org/CorpusID:207252270)


12


Manuscript


Stephanie Fu, Netanel Tamir, Shobhita Sundaram, Lucy Chai, Richard Zhang, Tali Dekel, and
Phillip Isola. Dreamsim: Learning new dimensions of human visual similarity using synthetic
data. _arXiv preprint arXiv:2306.09344_, 2023.


Luyu Gao, Yunyi Zhang, Jiawei Han, and Jamie Callan. Scaling deep contrastive learning batch size
under memory limited setup. _arXiv preprint arXiv:2101.06983_, 2021a.


Tianyu Gao, Xingcheng Yao, and Danqi Chen. Simcse: Simple contrastive learning of sentence
embeddings. In _Proceedings of the 2021 Conference on Empirical Methods in Natural Language_
_Processing_, pp. 6894–6910, 2021b.


Danna Gurari, Qing Li, Abigale J Stangl, Anhong Guo, Chi Lin, Kristen Grauman, Jiebo Luo, and
Jeffrey P Bigham. Vizwiz grand challenge: Answering visual questions from blind people. In
_Proceedings of the IEEE conference on computer vision and pattern recognition_, pp. 3608–3617,
2018.


Kelvin Guu, Kenton Lee, Zora Tung, Panupong Pasupat, and Mingwei Chang. Retrieval augmented
language model pre-training. In _International conference on machine learning_, pp. 3929–3938.
PMLR, 2020.


Dan Hendrycks, Steven Basart, Norman Mu, Saurav Kadavath, Frank Wang, Evan Dorundo, Rahul
Desai, Tyler Zhu, Samyak Parajuli, Mike Guo, et al. The many faces of robustness: A critical analysis of out-of-distribution generalization. In _Proceedings of the IEEE/CVF international_
_conference on computer vision_, pp. 8340–8349, 2021a.


Dan Hendrycks, Kevin Zhao, Steven Basart, Jacob Steinhardt, and Dawn Song. Natural adversarial
examples. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recogni-_
_tion_, pp. 15262–15271, 2021b.


SU Hongjin, Jungo Kasai, Chen Henry Wu, Weijia Shi, Tianlu Wang, Jiayi Xin, Rui Zhang, Mari
Ostendorf, Luke Zettlemoyer, Noah A Smith, et al. Selective annotation makes language models
better few-shot learners. In _The Eleventh International Conference on Learning Representations_,
2022.


Hexiang Hu, Yi Luan, Yang Chen, Urvashi Khandelwal, Mandar Joshi, Kenton Lee, Kristina
Toutanova, and Ming-Wei Chang. Open-domain visual entity recognition: Towards recognizing millions of wikipedia entities. In _Proceedings of the IEEE/CVF International Conference on_
_Computer Vision_, pp. 12065–12075, 2023.


Drew A Hudson and Christopher D Manning. Gqa: A new dataset for real-world visual reasoning
and compositional question answering. In _Proceedings of the IEEE/CVF conference on computer_
_vision and pattern recognition_, pp. 6700–6709, 2019.


Gautier Izacard and Edouard Grave. Leveraging passage retrieval with generative models for open
domain question answering, 2020. [URL https://arxiv.org/abs/2007.0128.](https://arxiv.org/abs/2007.0128)


Chao Jia, Yinfei Yang, Ye Xia, Yi-Ting Chen, Zarana Parekh, Hieu Pham, Quoc Le, Yun-Hsuan
Sung, Zhen Li, and Tom Duerig. Scaling up visual and vision-language representation learning
with noisy text supervision. In _International_ _conference_ _on_ _machine_ _learning_, pp. 4904–4916.
PMLR, 2021.


Ting Jiang, Minghui Song, Zihan Zhang, Haizhen Huang, Weiwei Deng, Feng Sun, Qi Zhang,
Deqing Wang, and Fuzhen Zhuang. E5-v: Universal embeddings with multimodal large language
models. _arXiv preprint arXiv:2407.12580_, 2024.


Vladimir Karpukhin, Barlas Oguz, Sewon Min, Patrick Lewis, Ledell Wu, Sergey Edunov, Danqi
Chen, and Wen-tau Yih. Dense passage retrieval for open-domain question answering. In
_Proceedings_ _of_ _the_ _2020_ _Conference_ _on_ _Empirical_ _Methods_ _in_ _Natural_ _Language_ _Processing_
_(EMNLP)_, pp. 6769–6781, 2020.


Sahar Kazemzadeh, Vicente Ordonez, Mark Matten, and Tamara Berg. Referitgame: Referring to
objects in photographs of natural scenes. In _Proceedings_ _of_ _the_ _2014_ _conference_ _on_ _empirical_
_methods in natural language processing (EMNLP)_, pp. 787–798, 2014.


13


Manuscript


Douwe Kiela, Hamed Firooz, Aravind Mohan, Vedanuj Goswami, Amanpreet Singh, Pratik Ringshia, and Davide Testuggine. The hateful memes challenge: Detecting hate speech in multimodal
memes. _Advances in neural information processing systems_, 33:2611–2624, 2020.


Ryan Kiros, Yukun Zhu, Russ R Salakhutdinov, Richard Zemel, Raquel Urtasun, Antonio Torralba,
and Sanja Fidler. Skip-thought vectors. _Advances in neural information processing systems_, 28,
2015.


Tom Kwiatkowski, Jennimaria Palomaki, Olivia Redfield, Michael Collins, Ankur Parikh, Chris
Alberti, Danielle Epstein, Illia Polosukhin, Jacob Devlin, Kenton Lee, et al. Natural questions: a
benchmark for question answering research. _Transactions of the Association for Computational_
_Linguistics_, 7:453–466, 2019a.


Tom Kwiatkowski, Jennimaria Palomaki, Olivia Redfield, Michael Collins, Ankur Parikh, Chris
Alberti, Danielle Epstein, Illia Polosukhin, Jacob Devlin, Kenton Lee, et al. Natural questions: A
benchmark for question answering research. _Transactions of the Association for Computational_
_Linguistics_, 7:452–466, 2019b.


Chankyu Lee, Rajarshi Roy, Mengyao Xu, Jonathan Raiman, Mohammad Shoeybi, Bryan Catanzaro, and Wei Ping. Nv-embed: Improved techniques for training llms as generalist embedding
models. _arXiv preprint arXiv:2405.17428_, 2024.


Patrick Lewis, Ethan Perez, Aleksandra Piktus, Fabio Petroni, Vladimir Karpukhin, Naman Goyal,
Heinrich K¨uttler, Mike Lewis, Wen-tau Yih, Tim Rockt¨aschel, et al. Retrieval-augmented generation for knowledge-intensive nlp tasks. _Advances in Neural Information Processing Systems_, 33:
9459–9474, 2020.


Feng Li, Renrui Zhang, Hao Zhang, Yuanhan Zhang, Bo Li, Wei Li, Zejun Ma, and Chunyuan Li.
Llava-next-interleave: Tackling multi-image, video, and 3d in large multimodal models. _arXiv_
_preprint arXiv:2407.07895_, 2024.


Junnan Li, Dongxu Li, Caiming Xiong, and Steven Hoi. Blip: Bootstrapping language-image pretraining for unified vision-language understanding and generation. In _International conference on_
_machine learning_, pp. 12888–12900. PMLR, 2022.


Junnan Li, Dongxu Li, Silvio Savarese, and Steven Hoi. Blip-2: Bootstrapping language-image
pre-training with frozen image encoders and large language models. In _International conference_
_on machine learning_, pp. 19730–19742. PMLR, 2023a.


Zehan Li, Xin Zhang, Yanzhao Zhang, Dingkun Long, Pengjun Xie, and Meishan Zhang. Towards
general text embeddings with multi-stage contrastive learning. _arXiv preprint arXiv:2308.03281_,
2023b.


Tsung-Yi Lin, Michael Maire, Serge Belongie, James Hays, Pietro Perona, Deva Ramanan, Piotr
Doll´ar, and C Lawrence Zitnick. Microsoft coco: Common objects in context. In _Computer_
_Vision–ECCV_ _2014:_ _13th_ _European_ _Conference,_ _Zurich,_ _Switzerland,_ _September_ _6-12,_ _2014,_
_Proceedings, Part V 13_, pp. 740–755. Springer, 2014.


Fuxiao Liu, Yinghan Wang, Tianlu Wang, and Vicente Ordonez. Visual news: Benchmark and
challenges in news image captioning. _arXiv preprint arXiv:2010.03743_, 2020.


Haotian Liu, Chunyuan Li, Qingyang Wu, and Yong Jae Lee. Visual instruction tuning. _Advances_
_in neural information processing systems_, 36, 2024.


Jiachang Liu, Dinghan Shen, Yizhe Zhang, Bill Dolan, Lawrence Carin, and Weizhu Chen. What
makes good in-context examples for gpt-3? _DeeLIO 2022_, pp. 100, 2022.


Siqi Liu, Weixi Feng, Tsu-jui Fu, Wenhu Chen, and William Yang Wang. Edis: Entity-driven image
search over multimodal web content. _arXiv preprint arXiv:2305.13631_, 2023.


Zheyuan Liu, Cristian Rodriguez-Opazo, Damien Teney, and Stephen Gould. Image retrieval on
real-life images with pre-trained vision-and-language models. In _Proceedings of the IEEE/CVF_
_International Conference on Computer Vision_, pp. 2125–2134, 2021.


14


Manuscript


Lajanugen Logeswaran and Honglak Lee. An efficient framework for learning sentence representations. In _International_ _Conference_ _on_ _Learning_ _Representations_, 2018. URL [https:](https://openreview.net/forum?id=rJvJXZb0W)
[//openreview.net/forum?id=rJvJXZb0W.](https://openreview.net/forum?id=rJvJXZb0W)


Pan Lu, Swaroop Mishra, Tanglin Xia, Liang Qiu, Kai-Wei Chang, Song-Chun Zhu, Oyvind Tafjord,
Peter Clark, and Ashwin Kalyan. Learn to explain: Multimodal reasoning via thought chains for
science question answering. _Advances in Neural Information Processing Systems_, 35:2507–2521,
2022.


Xueguang Ma, Sheng-Chieh Lin, Minghan Li, Wenhu Chen, and Jimmy Lin. Unifying multimodal
retrieval via document screenshot embedding. _arXiv preprint arXiv:2406.11251_, 2024a.


Xueguang Ma, Liang Wang, Nan Yang, Furu Wei, and Jimmy Lin. Fine-tuning llama for multi-stage
text retrieval. In _Proceedings of the 47th International ACM SIGIR Conference on Research and_
_Development in Information Retrieval_, pp. 2421–2425, 2024b.


Marco Marelli, Stefano Menini, Marco Baroni, Luisa Bentivogli, Raffaella Bernardi, and Roberto
Zamparelli. A SICK cure for the evaluation of compositional distributional semantic models.
In Nicoletta Calzolari, Khalid Choukri, Thierry Declerck, Hrafn Loftsson, Bente Maegaard,
Joseph Mariani, Asuncion Moreno, Jan Odijk, and Stelios Piperidis (eds.), _Proceedings_ _of_ _the_
_Ninth_ _International_ _Conference_ _on_ _Language_ _Resources_ _and_ _Evaluation_ _(LREC’14)_, pp. 216–
223, Reykjavik, Iceland, May 2014. European Language Resources Association (ELRA). URL
[http://www.lrec-conf.org/proceedings/lrec2014/pdf/363_Paper.pdf.](http://www.lrec-conf.org/proceedings/lrec2014/pdf/363_Paper.pdf)


Kenneth Marino, Mohammad Rastegari, Ali Farhadi, and Roozbeh Mottaghi. Ok-vqa: A visual
question answering benchmark requiring external knowledge. In _Proceedings_ _of_ _the_ _IEEE/cvf_
_conference on computer vision and pattern recognition_, pp. 3195–3204, 2019.


Ahmed Masry, Do Xuan Long, Jia Qing Tan, Shafiq Joty, and Enamul Hoque. Chartqa: A benchmark for question answering about charts with visual and logical reasoning. _arXiv_ _preprint_
_arXiv:2203.10244_, 2022.


Minesh Mathew, Dimosthenis Karatzas, and CV Jawahar. Docvqa: A dataset for vqa on document
images. In _Proceedings of the IEEE/CVF winter conference on applications of computer vision_,
pp. 2200–2209, 2021.


Minesh Mathew, Viraj Bagal, Rub`en Tito, Dimosthenis Karatzas, Ernest Valveny, and CV Jawahar.
Infographicvqa. In _Proceedings of the IEEE/CVF Winter Conference on Applications of Computer_
_Vision_, pp. 1697–1706, 2022.


Rui Meng, Ye Liu, Shafiq Joty, Caiming Xiong, Yingbo Zhou, and Semih Yavuz. Sfr-embedding-2:
Advanced text embedding with multi-stage training, 2024. URL [https://huggingface.](https://huggingface.co/Salesforce/SFR-Embedding-2_R)
[co/Salesforce/SFR-Embedding-2_R.](https://huggingface.co/Salesforce/SFR-Embedding-2_R)


Tomas Mikolov. Efficient estimation of word representations in vector space. _arXiv_ _preprint_
_arXiv:1301.3781_, 2013.


Bhaskar Mitra, Fernando Diaz, and Nick Craswell. Learning to match using local and distributed
representations of text for web search. In _Proceedings_ _of_ _the_ _26th_ _international_ _conference_ _on_
_world wide web_, pp. 1291–1299, 2017.


Niklas Muennighoff, Nouamane Tazi, Loic Magne, and Nils Reimers. Mteb: Massive text embedding benchmark. In _Proceedings_ _of_ _the_ _17th_ _Conference_ _of_ _the_ _European_ _Chapter_ _of_ _the_
_Association for Computational Linguistics_, pp. 2014–2037, 2023.


Tri Nguyen, Mir Rosenberg, Xia Song, Jianfeng Gao, Saurabh Tiwary, Rangan Majumder, and
Li Deng. Ms marco: A human generated machine reading comprehension dataset. November 2016. URL [https://www.microsoft.com/en-us/research/publication/](https://www.microsoft.com/en-us/research/publication/ms-marco-human-generated-machine-reading-comprehension-dataset/)
[ms-marco-human-generated-machine-reading-comprehension-dataset/.](https://www.microsoft.com/en-us/research/publication/ms-marco-human-generated-machine-reading-comprehension-dataset/)


Jianmo Ni, Chen Qu, Jing Lu, Zhuyun Dai, Gustavo Hernandez Abrego, Ji Ma, Vincent Zhao,
Yi Luan, Keith Hall, Ming-Wei Chang, et al. Large dual encoders are generalizable retrievers. In
_Proceedings of the 2022 Conference on Empirical Methods in Natural Language Processing_, pp.
9844–9855, 2022.


15


Manuscript


Jeffrey Pennington, Richard Socher, and Christopher D Manning. Glove: Global vectors for word
representation. In _Proceedings of the 2014 conference on empirical methods in natural language_
_processing (EMNLP)_, pp. 1532–1543, 2014.


Bryan A Plummer, Liwei Wang, Chris M Cervantes, Juan C Caicedo, Julia Hockenmaier, and Svetlana Lazebnik. Flickr30k entities: Collecting region-to-phrase correspondences for richer imageto-sentence models. In _Proceedings of the IEEE international conference on computer vision_, pp.
2641–2649, 2015.


Alec Radford, Jong Wook Kim, Chris Hallacy, Aditya Ramesh, Gabriel Goh, Sandhini Agarwal,
Girish Sastry, Amanda Askell, Pamela Mishkin, Jack Clark, et al. Learning transferable visual
models from natural language supervision. In _International conference on machine learning_, pp.
8748–8763. PMLR, 2021.


Nils Reimers and Iryna Gurevych. Sentence-BERT: Sentence embeddings using Siamese BERTnetworks. In _Proceedings_ _of_ _the_ _2019_ _Conference_ _on_ _Empirical_ _Methods_ _in_ _Natural_ _Lan-_
_guage_ _Processing_ _and_ _the_ _9th_ _International_ _Joint_ _Conference_ _on_ _Natural_ _Language_ _Processing_
_(EMNLP-IJCNLP)_, pp. 3982–3992, Hong Kong, China, November 2019. Association for Computational Linguistics. doi: 10.18653/v1/D19-1410. [URL https://aclanthology.org/](https://aclanthology.org/D19-1410)
[D19-1410.](https://aclanthology.org/D19-1410)


Ohad Rubin, Jonathan Herzig, and Jonathan Berant. Learning to retrieve prompts for in-context
learning. In _Proceedings of the 2022 Conference of the North American Chapter of the Associa-_
_tion for Computational Linguistics:_ _Human Language Technologies_, pp. 2655–2671, 2022.


Dustin Schwenk, Apoorv Khandelwal, Christopher Clark, Kenneth Marino, and Roozbeh Mottaghi.
A-okvqa: A benchmark for visual question answering using world knowledge. In _European_
_conference on computer vision_, pp. 146–162. Springer, 2022.


Thibault Sellam, Dipanjan Das, and Ankur Parikh. Bleurt: Learning robust metrics for text generation. In _Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics_,
pp. 7881–7892, 2020.


Amanpreet Singh, Vivek Natarajan, Meet Shah, Yu Jiang, Xinlei Chen, Dhruv Batra, Devi Parikh,
and Marcus Rohrbach. Towards vqa models that can read. In _Proceedings_ _of_ _the_ _IEEE/CVF_
_conference on computer vision and pattern recognition_, pp. 8317–8326, 2019.


Jacob Mitchell Springer, Suhas Kotha, Daniel Fried, Graham Neubig, and Aditi Raghunathan. Repetition improves language model embeddings. _arXiv preprint arXiv:2402.15449_, 2024.


Hongjin Su, Weijia Shi, Jungo Kasai, Yizhong Wang, Yushi Hu, Mari Ostendorf, Wen-tau Yih,
Noah A Smith, Luke Zettlemoyer, and Tao Yu. One embedder, any task: Instruction-finetuned
text embeddings. In _Findings_ _of_ _the_ _Association_ _for_ _Computational_ _Linguistics:_ _ACL_ _2023_, pp.
1102–1121, 2023.


Quan Sun, Yuxin Fang, Ledell Wu, Xinlong Wang, and Yue Cao. Eva-clip: Improved training
techniques for clip at scale. _arXiv preprint arXiv:2303.15389_, 2023.


Nandan Thakur, Nils Reimers, Andreas R¨uckl´e, Abhishek Srivastava, and Iryna Gurevych. Beir: A
heterogeneous benchmark for zero-shot evaluation of information retrieval models. In _Thirty-fifth_
_Conference on Neural Information Processing Systems Datasets and Benchmarks Track (Round_
_2)_ .


Liang Wang, Nan Yang, Xiaolong Huang, Binxing Jiao, Linjun Yang, Daxin Jiang, Rangan Majumder, and Furu Wei. Text embeddings by weakly-supervised contrastive pre-training. _arXiv_
_preprint arXiv:2212.03533_, 2022a.


Liang Wang, Nan Yang, Xiaolong Huang, Linjun Yang, Rangan Majumder, and Furu Wei. Improving text embeddings with large language models. _arXiv preprint arXiv:2401.00368_, 2024.


Zhen Wang, Xu Shan, Xiangxie Zhang, and Jie Yang. N24news: A new dataset for multimodal
news classification. _arXiv preprint arXiv:2108.13327_, 2021.


16


Manuscript


Zirui Wang, Jiahui Yu, Adams Wei Yu, Zihang Dai, Yulia Tsvetkov, and Yuan Cao. Simvlm: Simple visual language model pretraining with weak supervision. In _International_ _Conference_ _on_
_Learning Representations_, 2022b.


Cong Wei, Yang Chen, Haonan Chen, Hexiang Hu, Ge Zhang, Jie Fu, Alan Ritter, and Wenhu Chen.
Uniir: Training and benchmarking universal multimodal information retrievers. _arXiv_ _preprint_
_arXiv:2311.17136_, 2023.


Hui Wu, Yupeng Gao, Xiaoxiao Guo, Ziad Al-Halah, Steven Rennie, Kristen Grauman, and Rogerio Feris. Fashion iq: A new dataset towards retrieving images by natural language feedback.
In _Proceedings_ _of_ _the_ _IEEE/CVF_ _Conference_ _on_ _computer_ _vision_ _and_ _pattern_ _recognition_, pp.
11307–11317, 2021.


Jianxiong Xiao, James Hays, Krista A Ehinger, Aude Oliva, and Antonio Torralba. Sun database:
Large-scale scene recognition from abbey to zoo. In _2010 IEEE computer society conference on_
_computer vision and pattern recognition_, pp. 3485–3492. IEEE, 2010.


Lee Xiong, Chenyan Xiong, Ye Li, Kwok-Fung Tang, Jialin Liu, Paul Bennett, Junaid Ahmed,
and Arnold Overwijk. Approximate nearest neighbor negative contrastive learning for dense text
retrieval. _arXiv preprint arXiv:2007.00808_, 2020.


Jiahui Yu, Zirui Wang, Vijay Vasudevan, Legg Yeung, Mojtaba Seyedhosseini, and Yonghui Wu.
Coca: Contrastive captioners are image-text foundation models. _Transactions on Machine Learn-_
_ing Research_, 2022.


Xiaohua Zhai, Basil Mustafa, Alexander Kolesnikov, and Lucas Beyer. Sigmoid loss for language
image pre-training. In _Proceedings_ _of_ _the_ _IEEE/CVF_ _International_ _Conference_ _on_ _Computer_
_Vision_, pp. 11975–11986, 2023.


Kai Zhang, Yi Luan, Hexiang Hu, Kenton Lee, Siyuan Qiao, Wenhu Chen, Yu Su, and Ming-Wei
Chang. Magiclens: Self-supervised image retrieval with open-ended instructions. _arXiv preprint_
_arXiv:2403.19651_, 2024.


Tianyi Zhang, Varsha Kishore, Felix Wu, Kilian Q Weinberger, and Yoav Artzi. Bertscore: Evaluating text generation with bert. In _International Conference on Learning Representations_, 2020.


Bolei Zhou, Agata Lapedriza, Aditya Khosla, Aude Oliva, and Antonio Torralba. Places: A 10 million image database for scene recognition. _IEEE Transactions on Pattern Analysis and Machine_
_Intelligence_, 2017.


Yuke Zhu, Oliver Groth, Michael Bernstein, and Li Fei-Fei. Visual7w: Grounded question answering in images. In _Proceedings of the IEEE conference on computer vision and pattern recognition_,
pp. 4995–5004, 2016.


17


Manuscript


A DETAILS OF MMEB


In this section, we provide additional details about our proposed benchmark, MMEB (Massive Multimodal Embedding Benchmark). Section A.1 outlines the specifics of the 36 datasets used in the
MMEB benchmark. Section A.2 explains the process for determining the number of candidates in
MMEB.


A.1 DATASET DETAILS


A.1.1 CLASSIFICATION


There are a total of 10 datasets for classification tasks.


**ImageNet-1K** (Deng et al., 2009) The dataset is s large-scale dataset commonly used in image
classification, consisting of over 1 million images across 1K different classes.


**ImageNet-A** (Hendrycks et al., 2021b) The dataset contains images from a distribution unlike the
ImageNet training distribution. ImageNet-A examples belong to ImageNet classes, but the examples are harder and can cause mistakes across various models. They cause consistent classification
mistakes due to scene complications encountered in the long tail of scene configurations and by
exploiting classifier blind spots.


**ImageNet-R** (Hendrycks et al., 2021a) The dataset contains set of images labeled with ImageNet
labels obtained by collecting art, cartoons, deviantart, graffiti, embroidery, graphics, origami, paintings, patterns, plastic objects, plush objects, sculptures, sketches, tattoos, toys, and video game
renditions of ImageNet classes.


**VOC2007** (Everingham et al., 2014) The dataset focuses on recognizing objects in realistic scenarios
and contains 20 object classes.


**N24News** (Wang et al., 2021) The dataset is sourced from the New York Times and consists of 24
categories, with each news article containing both text and image information. The task is to classify
the given news image and its accompanying text into one of the 24 categories.


**HatefulMemes** (Kiela et al., 2020) The dataset proposes a new challenge set for multimodal classification, focusing on detecting hate speech in multimodal memes.


**Place365** (Zhou et al., 2017) The dataset is a repository of 10 million scene photographs, labeled
with scene semantic categories, comprising a large and diverse list of the types of environments
encountered in the world.


**SUN397** (Xiao et al., 2010) The dataset is a dataset for scene recognition consisting of 397 categories.


**ObjectNet** (Barbu et al., 2019) The dataset is a crowd-sourced test set of 50K images featuring
objects in unusual poses and cluttered scenes, designed to challenge recognition performance. It
includes controls for rotation, background, and viewpoint, and covers 313 object classes.


**Country-211** (Radford et al., 2021) The dataset is designed to assess the geolocation capability of
visual representations. It filters the YFCC100M dataset to find 211 countries that have at least 300
photos with GPS coordinates.


A.1.2 VISUAL QUESTION ANSWERING (VQA)


There are a total of 10 datasets for VQA tasks.


**OK-VQA** (Marino et al., 2019) The dataset includes questions that require external resources for
answers.


**A-OKVQA** (Schwenk et al., 2022) The dataset is an augmented successor of OK-VQA, requiring
a broad base of commonsense and world knowledge to answer. The questions generally cannot be
answered by simply querying a knowledge base, and instead require some form of commonsense
reasoning about the scene depicted in the image.


18


Manuscript


**DocVQA** (Mathew et al., 2021) The dataset contains questions for document analysis and recognition over document images of various types and content.


**InfographicsVQA** (Mathew et al., 2022) The dataset comprises a diverse collection of infographics
accompanied by natural language question and answer annotations. The questions require methods
capable of jointly reasoning over the document layout, textual content, graphical elements, and data
visualizations.


**ChartQA** (Masry et al., 2022) The dataset is designed for question answering about charts, with a
focus on visual and logical reasoning applied to real-world charts.


**ScienceQA** (Lu et al., 2022) The dataset contains questions with diverse science topics and annotations of their answers with corresponding lectures and explanations.


**Visual7W-telling** (Zhu et al., 2016) The dataset establishes a semantic link between textual descriptions and image regions through object-level grounding. It has two types of questions: “telling”
and “pointing”. It leverages the six W questions (what, where, when, who, why, and how) to systematically examine a model’s capability for visual understanding through telling questions. Additionally, a seventh “which” question is appended for visual answers as pointing questions. We use
“Visual7W-telling” in our VQA category and “Visual7W-pointing” in our visual grounding category.


**VizWiz** (Gurari et al., 2018) The dataset originates from a natural visual question answering scenario, where blind individuals captured images and recorded spoken questions about them, along
with 10 crowdsourced answers for each visual question. For our task, we select only the answerable
questions.


**TextVQA** (Singh et al., 2019) The dataset is designed to benchmark visual reasoning based on text
within images. Models need to read and reason about the text in images to answer related questions.


**GQA** (Hudson & Manning, 2019) The dataset is designed for real-world visual reasoning and compositional question answering. It uses real images from the Visual Genome dataset. Each image
is accompanied by scene graph annotations that describe the classes and attributes of objects in the
scene, as well as their pairwise relationships.


A.1.3 RETRIEVAL


There are a total of 12 datasets for retrieval tasks.


**VisDial** (Das et al., 2017) The dataset features dialogues created by two Amazon Mechanical Turk
workers. One worker takes the role of the “questioner”, who only sees the text description of an
image, while the other plays the “answerer”, who has access to the image. They engage in a 10round Q&A session about the image. We repurpose this dataset as a retrieval task, where the goal is
to retrieve the image based on the given dialogue.


**CIRR** (Liu et al., 2021) The dataset is designed for the task of composed image retrieval. It consists
of pairs of real-life reference and target images, along with a modification sentence that describes
the changes made between the two images.


**FashionIQ** (Wu et al., 2021) The dataset contains images of fashion products with crowd-sourced
descriptions highlighting the differences between these products. Similar to CIRR, FashionIQ can
also be used for the task of composed image retrieval, where each test case consists of a pair of
reference and target images, along with a modification sentence that describes the changes between
the two images.


**VisualNews** (Liu et al., 2020) The dataset contains publicly available news image paired with captions. We split this task into two setups: **“VisualNews** ~~**i**~~ **2t”**, which retrieves the caption given the
news image and **“VisualNews** ~~**t**~~ **2i”**, which retrieves the news image given the caption.


**MSCOCO** (Lin et al., 2014) The dataset is a well-known image caption dataset. Similar to VisualNews, WE split this task into two setups: **“MSCOCO** ~~**i**~~ **2t’**, which retrieves the caption given the
image and **“MSCOCO** ~~**t**~~ **2i”**, which retrieves the image given the caption.


**WebQA** (Chang et al., 2022) The dataset is a multihop, multimodal QA dataset that requires retrieving a Wikipedia page to answer a given question. We use the Wikipedia page’s image and text
descriptions as the candidates for retrieval.


19


Manuscript


**NIGHTS** (Fu et al., 2023) The dataset contains human similarity judgments on image pairs that are
alike in various ways. The original dataset consists of triplets: a reference image and two perturbed
versions, along with human judgments indicating which version is most similar to the reference.
Following M-BEIR (Wei et al., 2023), we refactor this dataset into a retrieval task to match pairwise
images, where the reference image serves as the query, and the perturbed version that aligns with
human judgment is the target.


**OVEN** (Hu et al., 2023) The dataset contains instances that include an image and a visual recognition text question. Additionally, each instance provides a related Wikipedia image along with its
corresponding text description (the Wikipedia title and the first 100 tokens of its summary) as a
reference for answering the question, which we treat as the target candidate.


**EDIS** (Liu et al., 2023) The dataset is a cross-modal image search in the news domain. This dataset
contains entity-rich queries, requiring the model to understand both entities and events from the text
queries. The candidate consists of the news image and its accompanying headline.


**Wiki-SS-NQ** (Ma et al., 2024a) The dataset is another retrieval-based VQA dataset. Unlike the
original Natural Questions dataset (Kwiatkowski et al., 2019a), which uses a Wikipedia paragraph
to answer the question, this dataset leverages Wiki-SS, utilizing Wikipedia page screenshots as the
corpus. The screenshot provides more comprehensive information than a plain Wikipedia paragraph.


For **CIRR**, **FashionIQ**, **VisualNews**, **MSCOCO**, **WebQA**, **NIGHTS**, **OVEN** and **EDIS**, we use
the processed versions from M-BEIR (Wei et al., 2023).


A.1.4 VISUAL GROUNDING


There are a total of 4 datasets for visual grounding tasks.


**MSCOCO** (Lin et al., 2014) The dataset includes an object detection task, which involves recognizing an object from a given class in an image. We have repurposed this task into a ranking problem
within the MMEB format. The query consists of the image and the object name, while the target
is the cropped image of the specified object. We gather distractors from other objects in the same
image as well as from different images. We discard test cases where the object is too small.


**RefCOCO** (Kazemzadeh et al., 2014) The dataset includes an object detection task that requires
more reasoning than MSCOCO. Unlike simply identifying the object class, the RefCOCO dataset
uses language expressions to refer to specific objects within an image. In our MMEB, we have two
tasks related to RefCOCO: **“RefCOCO”** and **“RefCOCO-Matching”** . In “RefCOCO”, the query
consists of the image and the language expressions referring to a specific object, while the target is
the cropped image of that object. In “RefCOCO-Matching”, both the query and the target contain
the image and the language expressions referring to a specific object, where the two objects are
identical.


**Visual7W-pointing** (Zhu et al., 2016) The dataset establishes a semantic link between textual descriptions and image regions through object-level grounding. It has two types of questions: “telling”
and “pointing”. It leverages the six W questions (what, where, when, who, why, and how) to systematically examine a model’s capability for visual understanding through telling questions. Additionally, a seventh “which” question is appended for visual answers as pointing questions. We use
“Visual7W-telling” in our VQA category and “Visual7W-pointing” in our visual grounding category.


A.2 SELECTION OF NUMBER OF CANDIDATES


A large number of candidates can make the benchmark more challenging and realistic. However,
we also considered the computational cost when designing the benchmark. Choosing an excessively
large number of candidates could result in very high inference costs, which may hinder rapid model
iteration. As shown in Table 5, we compare the performance of VL M2VE C with different numbers of
candidates in the MMEB benchmark. The results show that if the number of candidates is too small,
the benchmark becomes saturated quickly. To balance evaluation cost with benchmark difficulty, we
selected 1,000 as the optimal number of candidates.


20


Manuscript


Table 5: We compare the performance of VL M2VE C using different numbers of candidates in
MMEB. To balance evaluation cost with benchmark difficulty, we selected 1,000 as the optimal
number of candidates.


**Meta-Task Average Score** **Average Score**
**#Candidates**

Classification VQA Retrieval Grounding IND OOD Overall


# of datasets _→_ 10 10 12 4 20 16 36


100 54.8 81.8 86.1 89.6 85.2 65.9 76.6
500 54.8 65.9 72.6 82.8 74.6 57.3 66.9
1000 54.8 54.9 62.3 79.5 66.5 52.0 60.1
2000 54.8 50.1 56.7 71.0 62.2 48.0 55.9
5000 54.8 41.3 46.5 65.3 54.5 43.2 49.5


21


Manuscript


Table 6: The detailed results of the baselines and our VL M2VE C on MMEB, which includes 20 indistribution datasets and 16 out-of-distribution datasets. The out-of-distribution datasets are highlighted with a yellow background in the table. We include only the best version of VL M2VE C in the
table, which uses LLaVA-1.6 as backbone.


ImageNet-1K 55.8 63.5 45.4 10.3 48.0 9.6 58.3 74.5
N24News 34.7 38.6 13.9 36.0 33.7 23.4 42.5 80.3
HatefulMemes 51.1 51.7 47.2 49.6 49.0 49.7 56.4 67.9
VOC2007 50.7 52.4 64.3 52.1 51.6 49.9 66.2 91.5
SUN397 43.4 68.8 39.6 34.5 57.0 33.1 63.2 75.8

_All Classification_ 42.8 47.8 40.3 27.0 38.8 21.8 44.3 61.2


**VQA (10 tasks)**
OK-VQA 7.5 11.5 2.4 8.7 12.7 8.9 25.4 69.0
A-OKVQA 3.8 3.3 1.5 3.2 2.9 5.9 8.8 54.4
DocVQA 4.0 5.3 4.2 2.6 3.0 1.7 6.2 52.0
InfographicsVQA 4.6 4.6 2.7 2.0 5.9 2.3 4.6 30.7
ChartQA 1.4 1.5 3.0 0.5 0.9 2.4 1.6 34.8
Visual7W 4.0 2.6 1.2 1.3 2.5 5.8 14.5 49.8

_All VQA_ 9.1 10.9 8.4 4.2 8.3 4.9 16.2 49.9


**Retrieval (12 tasks)**
VisDial 30.7 25.4 21.5 18.0 24.8 9.2 42.2 80.9
CIRR 12.6 15.4 15.1 9.8 39.1 6.1 51.3 49.9
VisualNews ~~t~~ 2i 78.9 74.0 51.0 48.1 50.7 13.5 74.3 75.4
VisualNews ~~i~~ 2t 79.6 78.0 52.4 13.5 21.1 8.1 76.8 80.0
MSCOCO t2i 59.5 63.6 58.3 53.7 54.1 20.7 68.5 75.7
MSCOCO i2t 57.7 62.1 55.0 20.3 40.0 14.0 72.1 73.1
NIGHTS 60.4 66.1 62.9 56.5 58.1 4.2 66.2 65.5
WebQA 67.5 62.1 58.1 55.4 43.0 17.7 89.6 87.6

_All Retrieval_ 53.0 52.3 31.6 33.9 35.4 11.5 61.8 67.4


**Visual Grounding (4 tasks)**
MSCOCO 33.8 34.5 46.4 28.9 22.1 10.8 46.6 80.6

_All Visual Grounding_ 51.8 53.3 59.5 47.0 26.0 19.0 65.3 86.1


**Final Score (36 tasks)**
All 37.8 39.7 34.8 25.2 27.8 13.3 44.7 62.9
All IND 37.1 39.3 32.3 25.3 31.0 14.9 47.1 67.5
All OOD 38.7 40.2 38.0 25.1 23.7 11.5 41.7 57.1


22


Manuscript


Table 7: Examples of datasets in MMEB (Part 1 of 4). _Instructions_ are written in italic font style.





















23


Manuscript


Table 8: Examples of datasets in MMEB (Part 2 of 4). _Instructions_ are written in italic font style.

























24


Manuscript


Table 9: Examples of datasets in MMEB (Part 3 of 4). _Instructions_ are written in italic font style.

















25








Manuscript


Table 10: Examples of datasets in MMEB (Part 4 of 4). _Instructions_ are written in italic font style.





























Table 11: Zero-shot text-image retrieval performance on Flickr30K. As a general multimodal representation model, VLM2VEC can still achieve competitive T2I (Text-to-Image) and I2T (Imageto-Text) scores when compared to existing CLIP-like models. The baseline numbers are sourced
from Sun et al. (2023) and Zhang et al. (2024). We use the best version of VL M2VE C here, which
is built upon the LLaVA-1.6 backbone.


**Model** **image** retrieval **text** retrieval


R@1 R@5 R@10 R@1 R@5 R@10


OpenAI CLIP-B/16 62.1 85.6 91.8 81.9 96.2 98.8
Open CLIP-B/16 69.8 90.4 94.6 86.3 97.9 99.4
EVA-02-CLIP-B/16 71.2 91.0 94.7 85.7 96.7 98.9
OpenAI CLIP-L/14 65.2 87.3 92.0 85.2 97.3 99.0
Open CLIP-L/14 75.0 92.5 95.6 88.7 98.4 99.2
EVA-02-CLIP-L/14 77.3 93.6 96.8 89.7 98.6 99.2
MagicLens-B 76.2 93.7 96.5 87.9 97.7 99.5
MagicLens-L 79.7 95.0 97.4 89.6 98.7 99.4
VLM2VEC **80.3** **95.0** **97.4** **94.6** **99.5** **99.8**


26


