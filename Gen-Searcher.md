## **Gen-Searcher: Reinforcing Agentic Search for Image Generation**

**Kaituo Feng** [1] **Manyuan Zhang** [1] _[†]_ **Shawn Chen** [2] **Yunlong Lin** [1] **Kaixuan Fan** [1]


**Yilei Jiang** [1] **Hongyu Li** **Dian Zheng** [1] **Chenyang Wang** [3] **Xiangyu Yue** [1] _[‡]_


1MMLab, CUHK 2UCLA 3UC Berkeley


Home: [https://gen-searcher.vercel.app/](https://gen-searcher.vercel.app/)


Figure 1: Generated images using our proposed Gen-Searcher.


**ABSTRACT**


Recent image generation models have shown strong capabilities in generating high-fidelity and
photorealistic images. However, they are fundamentally constrained by frozen internal knowledge,
thus often failing on real-world scenarios that are knowledge-intensive or require up-to-date information. In this paper, we present Gen-Searcher, as the first attempt to train a search-augmented image
generation agent, which performs multi-hop reasoning and search to collect the textual knowledge
and reference images needed for grounded generation. To achieve this, we construct a tailored
data pipeline and curate two high-quality datasets, Gen-Searcher-SFT-10k and Gen-Searcher-RL-6k,
containing diverse search-intensive prompts and corresponding ground-truth synthesis images. We
further introduce KnowGen, a comprehensive benchmark that explicitly requires search-grounded
external knowledge for image generation and evaluates models from multiple dimensions. Based on
these resources, we train Gen-Searcher with SFT followed by agentic reinforcement learning with
dual reward feedback, which combines text-based and image-based rewards to provide more stable


_†_ Project Leader.

_‡_ Corresponding Author.


Gen-Searcher: Reinforcing Agentic Search for Image Generation


and informative learning signals for GRPO training. Experiments show that Gen-Searcher brings
substantial gains, improving Qwen-Image by around 16 points on KnowGen and 15 points on WISE.
We hope this work can serve as an open foundation for search agents in image generation, and we
fully open-source our data, models, and code.


**1** **Introduction**


Recent text-to-image generation models have achieved remarkable progress in producing high-fidelity and photorealistic
images [1, 2, 3]. Despite these advances, most of them remain fundamentally limited by frozen internal knowledge
acquired during pretraining. As a result, these models often struggle with real-world prompts that are knowledgeintensive or require up-to-date information. For instance, generating images involving specific landmarks, public figures,
newly released products, or other evolving real-world entities often requires external knowledge that cannot be reliably
inferred from the model’s parametric memory alone. In many cases, the necessary information is not directly available
from a single source, and instead requires multi-hop search over the web, where the model should iteratively search,
browse, and analyze evidence from multiple sources before generation. Currently, only a few advanced proprietary
models like Nano Banana Pro [2], support search before generation, yet they remain limited to text search without
retrieving visual references.


To mitigate this limitation, prior work has explored RAG-based approaches that retrieve relevant knowledge from
external databases to support generation [4, 5, 6]. However, these methods are limited by the coverage and freshness
of static databases, which cannot fully capture the vast and evolving knowledge of the real world. In addition, the
similarity-based single-round shallow retrieval makes them inadequate for complex real-world queries that require deep
search. Besides, A few prompt-based workflows [7, 8] are recently proposed to enhance image generation models by
directly searching for information on the web. However, these works rely on manually designed prompting strategies to
guide search and generation without training. As a result, the search behavior is often brittle and suboptimal, lacking
the ability to adaptively plan search steps, refine queries, or reason over retrieved evidence.


Inspired by the recent success of agentic reinforcement learning (agentic RL) [9, 10] in deep research tasks, we ask a
natural question: can we train an search agent for image generation that actively performs multi-hop web search and
reasoning to gather knowledge in the web for grounded image generation?


In this paper, we introduce Gen-Searcher, as the first attempt to train a multimodal deep search agent for image
generation. To achieve this goal, we build a dedicated data pipeline, in order to overcome the lack of suitable training
data for this task. Specifically, we first construct text prompts that require deep web search for image generation through
two strategies. Our primary approach uses carefully designed prompt engineering to instruct Gemini 3 Pro [11] to
generate multi-hop search-intensive prompts across around 20 diverse categories, including celebrities, anime, physics,
chemistry, posters, art, etc. The second approach converts existing deep research datasets into image-generation-oriented
prompts, primarily covering general news scenarios. After constructing the prompts, we iteratively employ Gemini 3 Pro
together with search tools to produce agentic trajectories, where the system performs search, browsing, and reasoning
to gather sufficient information before producing a final search-grounded prompt along with relevant reference images.
The resulting prompts are then fed into Nano Banana Pro to synthesize the corresponding images as ground truth. To
ensure data quality, we further employ Seed1.8 [12] to score and filter the generated samples. Based on this pipeline,
we construct two high-quality training datasets, Gen-Searcher-SFT-10k and Gen-Searcher-RL-6k, as well as KnowGen,
a comprehensive benchmark for evaluating search-grounded image generation on real-world, knowledge-intensive
prompts. We also introduce K-Score for evaluation on KnowGen benchmark.


Based on the constructed training datasets, we train Gen-Searcher in two stages: SFT equips the model with basic
tool-use abilities, enabling multi-step search, browsing, and reasoning for image generation; while agentic RL based
on GRPO [13, 14] further optimizes its tool-calling trajectories, encouraging the model to produce higher-quality
search-grounded prompts for generation. Notably, we find that this task poses unique challenges: due to the limited
capability and high generation variance of open-source image generators such as Qwen-Image [1], sometimes even
correct searched information may still fail to produce high-quality images, making pure image-based rewards noisy
and unstable. To address this issue, we introduce an additional text-based reward that evaluates whether the collected
search-grounded prompt contains sufficient information to generate the target image. We then combine both text-based
and image-based rewards to train the agent with GRPO, providing more stable and informative feedback for optimizing
the search and reasoning process.


2


Incorrect

text and

visual
features







Gen-Searcher: Reinforcing Agentic Search for Image Generation


|Previous paradigm<br>Image<br>Generator|Col2|
|---|---|
|Previous paradigm<br>Image<br>Generator||











Correct
text and

visual
features



Figure 2: Our proposed Gen-Searcher enables search-grounded generation in real-word knowledge-intensive scenarios.


We conduct extensive experiments to evaluate the effectiveness of Gen-Searcher. Our method consistently improves
image generation performance across different backbones, bringing around 16-point gains for Qwen-Image on KnowGen.
We further observe strong transferability: a Gen-Searcher trained with Qwen-Image can be directly applied to Seedream
4.5 [15] and Nano Banana Pro [2] without additional training, yielding about 16-point and 3-point improvements,
respectively. Beyond our proposed KnowGen benchmark, we also evaluate on WISE [16], where Gen-Searcher improves
Qwen-Image from 0.62 to 0.77, demonstrating its strong generalization in knowledge-intensive image generation tasks.


Our contributions can be summarized as follows:


    - We propose **Gen-Searcher**, the first attempt to explore training a multimodal deep search agent for image
generation. We fully open-source our project and hope that Gen-Searcher can serve as an open foundation for
future research.


    - To support training, we build a dedicated data pipeline to construct search-intensive image generation data,
resulting in two training datasets, **Gen-Searcher-SFT-10k** and **Gen-Searcher-RL-6k** . In addition, we introduce **KnowGen**, a new and challenging benchmark designed to evaluate search-grounded image generation in
knowledge-intensive real-world scenarios.


    - Extensive experiments validate the effectiveness of our proposed Gen-Searcher. For example, our method
improves Qwen-Image by around 16 points on KnowGen and around 15 points on WISE.


**2** **Related Works**


**2.1** **Image Generation Models**


Recent years have witnessed rapid progress in image generation models, enabling the synthesis of high-fidelity and
photorealistic images from natural language prompts [2, 17, 3, 18]. Early GAN-based methods demonstrated the
potential of neural image synthesis, while diffusion models later became the dominant paradigm [19]. This progress has
driven the development of a series of powerful models, including Stable Diffusion [20], Imagen [21], and more recent
models like FLUX [22], Qwen-Image [1], LongCat-Image [23], Z-Image [3], and Nano Banana Pro [2] have further
advanced image quality, multilingual text rendering, instruction following, and generation efficiency. Nevertheless,
most of existing models still largely depend on frozen parametric knowledge acquired during pretraining, which limits
their ability to handle prompts requiring rich world knowledge or up-to-date external information. Although a few
advanced proprietary models such as Nano Banana Pro [2], incorporate search before generation, they remain limited to
text-based search without visual search, often leading to inaccurate visual features in the generated images.


3


Gen-Searcher: Reinforcing Agentic Search for Image Generation


**2.2** **Agentic Reinforcement Learning**


Agentic reinforcement learning (RL) has recently emerged as an effective paradigm for training large language model
(LLM) agents to perform multi-step reasoning and tool interaction [24, 25, 26]. Building on RL with verifiable rewards

[27, 28, 29, 30, 31], recent studies explore training agents that can interact with external tools and environments through
long-horizon trajectories. For example, ARPO [24] introduces an agentic RL algorithm designed for multi-turn tool-use
agents, incorporating an entropy-aware rollout strategy to encourage exploration. GiGPO [32] proposes a hierarchical
group-based RL method that provides finer-grained step-level credit assignment for multi-turn agents. AdaTooler-V

[25] proposes an adaptive tool-usage framework for image and video tool use, which dynamically adjusts reward scales
to encourage invoking visual tools only when they provide measurable benefits. Vision-DeepResearch [33] enables
multimodal agents to perform long-horizon visual and textual search over real-world search engines. However, training
search agents for knowledge-intensive image generation with agentic RL remains unexplored.


**3** **Method**


**3.1** **Dataset Construction**


High-quality training data is essential for developing a search agent capable of performing multi-hop deep search
and reasoning for image generation. However, such data does not naturally exist, since it requires aligned pairs of
search-intensive prompts, agentic search trajectories, and grounded images. To address this challenge, we design a
dedicated data pipeline that automatically constructs training data for search-grounded image generation. The overall
pipeline consists of four stages: text prompt construction, agentic trajectory generation, grounded image synthesis, and
data filtering and curation. An illusration of our data pipeline can be found in Figure 3


**Text Prompt Construction.** We first construct text prompts that require deep web search before image generation.
To ensure diversity and realistic search difficulty, we adopt two complementary strategies. Our primary approach uses
carefully designed prompt engineering to instruct **Gemini 3 Pro** [11] to generate multi-hop search-intensive prompts
across a broad range of categories, including _Anime_, _Architecture_, _Art_, _Astronomy_, _Biology_, _Celebrities_, _Chemistry_,
_Culture_, _Engineering_, _Film_, _Game_, _Geography_, _History_, _Industry_, _Medicine_, _Physics_, _Politics_, _Posters_, _Religion_, and
_Sports_ . These prompts are explicitly designed such that the required information cannot be obtained by single-turn
search, and instead requires multi-step evidence aggregation and analysis across the web.


As a complementary strategy, we convert samples from existing deep research question answering datasets [34, 9] into
image-generation-oriented prompts. In particular, we use Gemini 3 Pro to transform information-seeking questions
into prompts that require generating a grounded visual depiction of the queried entity or event. This strategy primarily
contributes prompts related to _General News_, further expanding the coverage of diverse knowledge scenarios.


**Agentic** **Trajectory** **Generation.** Given the constructed text prompts, we generate agentic search trajectories to
perform deep search and gather sufficient evidence for producing the final search-grounded prompt together with
selected reference images for accurate visual features. Meanwhile, these trajectories also serve as valuable supervision
data for subsequent supervised fine-tuning. Specifically, we employ **Gemini 3 Pro** together with a set of search tools in a
multi-turn manner. The tool set includes search for retrieving textual information from the web, image_search for
searching relevant images via textual queries, and browse for reading and analyzing the detailed contents of retrieved
webpages. During this process, the agent continuously analyzes textual and visual feedback from the environment,
identifies useful evidence and reference images, and plans the next action accordingly. Through this multi-turn reasoning
and search procedure, the agent progressively aggregates information from multiple sources before finally producing a
grounded prompt and a set of relevant reference images for image synthesis.


**Ground-Truth Image Synthesis.** After obtaining the final grounded prompts and visual references, we synthesize
the corresponding images using the proprietary image generation model **Nano Banana Pro** [2]. The generated images
serve as synthesis ground truth for training the search agent. This process results in approximately **30K** raw samples
consisting of prompts, search trajectories, grounded prompts, reference images, and ground-truth images.


**Data Filtering and Benchmark Construction.** To ensure data quality, we further employ another strong proprietary
model **Seed1.8** [12] to score the generated samples from multiple perspectives, including whether the prompt genuinely


4


Gen-Searcher: Reinforcing Agentic Search for Image Generation









































































Figure 3: An illustration of our data curation pipeline.


requires search, the correctness of the generated content, faithfulness to the prompt, visual aesthetics, text rendering
clarity, and safety considerations. These model-based scores are combined with rule-based filtering, such as removing
prompts with excessively long token lengths or inconsistent search results. After filtering, we obtain approximately
**17K** high-quality samples.


From this curated dataset, we select **630 human-verified samples** to construct a held-out benchmark named **KnowGen**,
which will be introduced later. The remaining **16K** samples are used for training and are split into two datasets:
**Gen-Searcher-SFT-10k** for supervised fine-tuning and **Gen-Searcher-RL-6k** for agentic reinforcement learning. We
strictly ensure that no overlap exists between the training data and the evaluation benchmark.


**3.2** **KnowGen Benchmark**


For evaluation, we introduce **KnowGen**, a comprehensive benchmark designed to evaluate search-grounded image
generation under knowledge-intensive real-world scenarios. Unlike conventional text-to-image benchmarks that
mainly emphasize prompt following or visual quality, KnowGen explicitly focuses on _knowledge-intensive_ and _search-_
_dependent_ generation scenarios, where solving the prompt often requires retrieving and aggregating evidence from the
web. Each sample in KnowGen is built to require non-trivial external knowledge, and many samples further demand
multi-hop search over multiple sources. To ensure reliability, all evaluation samples are _manually verified_ .


**Category Composition.** To provide broad coverage over different types of search-grounded generation tasks, we
divide 630 samples in KnowGen into two high-level subsets: **Science & Knowledge** and **Pop Culture & News** . The
**Science & Knowledge** subset includes these categories: _astronomy_, _biology_, _chemistry_, _physics_, _engineering_, _medicine_,
_industry_, _architecture_, _history_, _geography_, _religion_, _politics_, _culture_, _art_, and _sports_ . These tasks typically require factual
world knowledge, entity disambiguation, or domain-specific information, and often involve fine-grained grounded
details that must be visually or textually realized correctly. The **Pop Culture & News** subset covers prompts related to
_anime_, _games_, _films_, _celebrities_, _posters_, and _General News_ . Compared with the first subset, these tasks more frequently
involve rapidly changing real-world information, popular culture entities, and prompt-required text or appearance
details that must be rendered accurately. This two-part design allows KnowGen to evaluate both relatively stable
knowledge-intensive scenarios and dynamic, high-update real-world scenarios within a unified benchmark. Figure 4
illustrates the categories and examples of our proposed KnowGen benchmark.


5


Gen-Searcher: Reinforcing Agentic Search for Image Generation























(a) Data categories and distribution of our KnowGen.



(b) Examples from our KnowGen.



Figure 4: Overview of the KnowGen benchmark.


**Evaluation Metric.** To evaluate generation quality on KnowGen, we introduce **K-Score**, a metric designed to assess
search-grounded image generation from multiple perspectives. We adopt **GPT-4.1** [35] as the judge to evaluate model
outputs, following WISE benchmark [16]. For each sample, the evaluator takes as input the original text prompt, the
ground-truth reference image, and the model-generated image, and scores the generated result from four dimensions:
**faithfulness**, **visual_correctness**, **text_accuracy**, and **aesthetics** . **Faithfulness** measures whether the generated image
follows the prompt at the scene-structure level, including the required subjects, relations, setting, and requested format.
**Visual correctness** evaluates whether the key grounded visual attributes are correct with respect to the target concept
and consistent with the reference image, such as subject appearance, object features, or other externally verifiable visual
cues. **Text accuracy** measures whether any prompt-required readable text in the image is present, legible, and correct;
when the prompt does not require readable text, this dimension is treated as not applicable and not counted into the
average score. **Aesthetics** measures the overall visual quality and artistic appeal of the generated image, including
composition, color harmony, lighting, etc. This dimension evaluates whether the image appears visually polished and
aesthetically pleasing. The evaluation prompt can be found in Appendix A.


Following our evaluation design, each dimension is scored using a three-level discrete scale of _{_ 0 _,_ 0 _._ 5 _,_ 1 _}_ . Specifically,
a score of 1 indicates the generated image fully satisfies the requirement of that dimension, 0 _._ 5 indicates that dimension
is largely correct or satisfied but contains minor issues or partial mismatches, and 0 indicates the generation fails to
meet the key requirement of that dimension. The final **K-Score** is computed as a weighted combination of these four
dimensions:


K-Score = 0 _._ 1 _·_ Faithfulness + 0 _._ 4 _·_ Visual Correctness + 0 _._ 4 _·_ Text Accuracy + 0 _._ 1 _·_ Aesthetics _._


This weighting emphasizes the two most critical aspects of search-grounded image generation, namely correctly
rendering grounded visual attributes and accurately reproducing required textual content, while still accounting for
overall prompt adherence and image aesthetic. We report K-Score both by the two high-level subsets and as an overall
average on KnowGen.


**3.3** **Training Scheme**


In this section, we train **Gen-Searcher** to act as a multimodal deep search agent that can iteratively gather external
knowledge and visual evidence from the web for image generation. Our training scheme follows a two-stage pipeline,
consisting of SFT and agentic RL.


6


Gen-Searcher: Reinforcing Agentic Search for Image Generation

















































Figure 5: An inference example of Gen-Searcher.


**Search Tools.** Gen-Searcher is equipped with three search tools. The first is search, which performs web text
search and returns the top- _k_ relevant webpage URLs for each query with their short snippets. This tool is mainly used
to verify factual information such as entity names, event details, dates, locations, and concise descriptions. The second
is image_search, which retrieves the top- _k_ relevant images given a textual query, together with image URLs and
brief descriptions, allowing the agent to ground identities, objects, landmarks, outfits, and other fine-grained appearance
details. The third is browse, which takes a webpage URL as input and returns a summary of the page content; in our
implementation, this summary is produced by Qwen3-VL-30B-A3B-Instruct. This tool is used when shallow search
results are insufficient and the agent needs to extract specific evidence from a webpage. At each step, the agent observes
the current prompt and accumulated search feedback, and then decides whether to continue searching, retrieve visual
references, browse a page for more details, or terminate with a final grounded prompt and selected reference images.


**Two-Stage** **Training.** We initialize Gen-Searcher from **Qwen3-VL-8B-Instruct** . In the first stage, we perform
supervised fine-tuning on **Gen-Searcher-SFT-10k**, which teaches the model to perform multi-turn tool use, including
issuing search queries, interpreting textual and visual feedback, selecting useful reference images, and composing
a final search-grounded prompt. In the second stage, we further optimize the model on **Gen-Searcher-RL-6k**
with reinforcement learning, enabling it to learn more effective search strategies and produce improved tool-calling


7


Gen-Searcher: Reinforcing Agentic Search for Image Generation


trajectories. It is worth noting that during training, the image generator remains fixed; we only optimize Qwen3-VL8B-Instruct to produce search-grounded prompts along with corresponding reference images. Figure 5 illustrates a
representative inference trajectory of Gen-Searcher.


**Dual Reward Feedback Design.** A natural choice for RL in our setting is to directly use an image-based reward ( _e.g_ .,
K-Score) to evaluate the final generated image. However, relying on image reward alone leads to substantial noise and
instability. This is because the final image quality depends not only on the correctness of the retrieved evidence, but also
on the capability and stochasticity of the downstream image generator. In particular, for open-source generators such as
Qwen-Image [1], even when the agent has collected correct information, complex prompts may still fail to produce
high-quality images, and even similar grounded prompts can result in noticeably different generations. As a result, pure
image-based reward introduces large variance and makes policy optimization unstable.


To address this issue, we introduce an additional _text-based reward_, denoted as _R_ text, which evaluates whether the final
output text contains sufficient, correct, and generation-relevant information for synthesizing the target image. We also
use **GPT-4.1** as the judge to score this reward on a five-level scale, with values in _{_ 0 _,_ 0 _._ 25 _,_ 0 _._ 5 _,_ 0 _._ 75 _,_ 1 _._ 0 _}_ . Compared
with image reward, text reward provides more direct supervision on the quality of information gathering, evidence
aggregation. However, using only text reward is also insufficient, since text that appears to contain sufficient information
does not necessarily support high-quality image generation. Optimizing only text reward would therefore ignore
the actual end-task generation outcome and may encourage outputs that are textually informative but not practically
effective for generation. The corresponding prompt can be founded in Appendix B.


Therefore, we combine both signals and adopt a dual-feedback reward design, where the text-based reward supervises
the quality of the gathered information and the image-based reward reflects the final generation performance. The final
reward is computed as
_R_ = (1 _−_ _α_ ) _R_ image + _αR_ text _,_ (1)
where _α_ is a balancing hyperparameter. Here we simply set _α_ = 0 _._ 5 and use K-Score as _R_ image.


**Optimization.** After computing the final reward, we optimize the policy using GRPO [13]. For each sampled output
_oi_ under query _q_, the advantage is computed by normalizing its reward with the mean and standard deviation of rewards
within the sampled group:

_Ai_ = _[R][i][ −]_ [mean(] _[{][R][j][}]_ [)] _._ (2)

std( _{Rj}_ )

The final policy update follows the standard GRPO objective:



_G_



_i_ =1




- - _πθ_ ( _oi|q_ ) - _πθ_ ( _oi|q_ ) - min [clip] [1 +] _[ ϵ]_ _Ai_
_πθ_ old( _oi|q_ ) _[A][i][,]_ _πθ_ old( _oi|q_ ) _[,]_ [ 1] _[ −]_ _[ϵ,]_



(3)



_J_ GRPO = E _q,{oi}_




1

_G_




                                      -                                       - [��]
_−β_ KL _D_ KL _πθ ∥_ _π_ ref _,_


where the variables and hyper-parameters are defined following the original GRPO algorithm [13].


**4** **Experiments**


**4.1** **Setup**



**Training Details.** We train Gen-Searcher-8B using 8 NVIDIA H800 GPUs, with Qwen3-VL-8B-Instruct [36] as the
base model. We first perform supervised fine-tuning on Gen-Searcher-SFT-10k, and then further conduct agentic RL
training on Gen-Searcher-RL-6k. For both SFT and RL, we use AdamW as the optimizer. The learning rate is set to
1 _×_ 10 _[−]_ [5] for SFT and 1 _×_ 10 _[−]_ [6] for RL, and the batch size is set to 8 in both stages. During RL training, we additionally
deploy Qwen-Image-Edit-2509 on 16 H800 GPUs to support rollout image generation, since we find that the 2509
version provides better text rendering quality than the 2511 version. We also deploy Qwen3-VL-30B-Instruct-A3B

[36] on 8 H800 GPUs as the summary model for the browse tool. For efficiency, we set the group size to 6, limit the
maximum number of interaction turns to 10, allow at most 5 returned images per turn, and set the maximum context
length to 36K. The model response length per turn is limited to 4K. Following prior practice, we mask out overlong
rollouts and rollouts with repetitive responses during training. The training process consumes around one day.


8


Gen-Searcher: Reinforcing Agentic Search for Image Generation


Table 1: Performance of different models on our KnowGen benchmark. Visual cor. and Text acc. denote Visual
correctness and Text accuracy, respectively. The overall K-Score is averaged over the Science & Knowledge and Pop
Culture & News subsets.


**Science & Knowledge** **Pop Culture & News** **Overall**
**Models**


Visual cor. Text acc. Faithfulness Aesthetics Visual cor. Text acc. Faithfulness Aesthetics K-Score


SD-3.5-Medium [41] 5.61 2.21 30.44 48.47 3.12 0.58 58.18 54.76 11.90


SD-3.5-Large [20] 5.44 2.04 31.29 46.77 5.21 2.01 55.36 58.33 12.53


Lumina-Image 2.0 [42] 1.19 0.34 30.95 36.05 2.68 0.58 54.76 47.62 9.43


FLUX.1-dev [22] 2.89 0.34 28.91 50.17 2.38 1.16 54.46 53.72 10.71


FLUX.1-Krea [22] 3.91 1.53 33.16 48.13 4.32 2.02 62.05 53.87 12.22


FLUX.2-klein-4B [43] 4.59 1.53 37.07 45.58 3.42 0.86 62.05 55.51 12.09


FLUX.2-klein-9B [43] 6.12 0.34 42.69 50.85 5.06 1.72 69.05 59.08 13.73


BAGEL [44] 4.93 1.70 43.37 51.87 8.33 2.59 64.14 53.57 13.85


HunyuanImage-3.0 [45] 4.76 1.19 40.14 56.46 6.10 2.51 63.99 64.14 14.15


Qwen-Image [1] 6.80 0.34 47.45 56.80 7.59 1.40 68.90 61.90 14.98


Z-Image-Turbo [3] 3.91 1.02 28.40 50.85 4.32 3.45 50.15 55.21 11.77


Z-Image [3] 6.80 2.72 41.16 43.54 7.89 2.00 70.24 57.29 14.49


**4.2** **Main Results on KnowGen**


**Benchmarks and Evaluation.** We evaluate Gen-Searcher on two benchmarks. The first is KnowGen, our proposed
benchmark for real-world search-grounded image generation, which focuses on real-world, knowledge-intensive
prompts that often require external search and multi-step evidence aggregation. The second is WISE [16], a relatively
simpler benchmark for knowledge-based image generation. During inference, we set the decoding parameters to
temperature = 0 _._ 6 and top- _p_ = 0 _._ 9, and use a maximum context length of 64K. At test time, we first feed the original
text prompt into Gen-Searcher, which produces a search-grounded prompt together with selected reference images,
and then pass them to the downstream image generator for final image synthesis. If Gen-Searcher fails to produce
a final search-grounded prompt due to issues such as overlong context or tool-call failure, we fall back to using the
original prompt for generation. For model families that separate text-only and editing models, such as Qwen-Image and
Qwen-Image-Edit, we use the text-only model for generation from pure text input and the editing model for generation
conditioned on both text and reference images.


**Challenging Nature of the KnowGen Benchmark.** Table 1 presents the main results on KnowGen. Overall, we can
find that KnowGen is a highly challenging benchmark for current image generation models, especially for open-source
ones. Even strong open-source baselines such as Qwen-Image, HunyuanImage-3.0, FLUX, and Z-Image achieve only


9


Gen-Searcher: Reinforcing Agentic Search for Image Generation


Table 2: Performance of different models on the WISE benchmark.


**Models** **Cultural** **Time** **Space** **Biology** **Physics** **Chemistry** **Overall**


FLUX.1-dev [22] 0.48 0.58 0.62 0.42 0.51 0.35 0.50


FLUX.1-schnell [22] 0.39 0.44 0.50 0.31 0.44 0.26 0.40


SD-3-Medium [46] 0.42 0.44 0.48 0.39 0.47 0.29 0.42


SD-3.5-Medium [41] 0.43 0.50 0.52 0.41 0.53 0.33 0.45


SD-3.5-Large [20] 0.44 0.50 0.58 0.44 0.52 0.31 0.46


Emu3 [47] 0.34 0.45 0.48 0.41 0.45 0.27 0.39


Qwen-Image [1] 0.62 0.63 0.77 0.57 0.75 0.40 0.62


HunyuanImage-3.0 [45] 0.58 0.57 0.70 0.56 0.63 0.31 0.57


LongCat-Image [23] 0.66 0.61 0.72 0.66 0.72 0.49 0.65


Gen-Searcher-8B + Qwen-Image 0.80 0.71 0.82 0.76 0.74 0.75 0.77


around 9 to 15 K-Score, showing that knowledge-intensive and search-grounded image generation remains far beyond
the capability of standard text-to-image systems. In contrast, proprietary models perform substantially better, with Nano
Banana Pro achieving the strongest baseline result of 50.38 and GPT-Image-1.5 reaching 44.97. This large gap indicates
that KnowGen poses significant challenges in both grounded knowledge retrieval and faithful visual realization, and
also highlights the clear difference between open-source and proprietary systems in handling such tasks.


**Effectiveness of Gen-Searcher.** Our method consistently brings significant performance gains across different image
generation backbones on KnowGen. When combined with Qwen-Image, Gen-Searcher-8B improves the overall
K-Score from 14.98 to 31.52, yielding a gain of 16.54 points. This large improvement shows that Gen-Searcher can
substantially compensate for the lack of built-in search capability in open-source image generators by actively gathering
grounded textual evidence and visual references from the web. More importantly, Gen-Searcher is not merely learning
a generator-specific prompting heuristic; instead, it learns a transferable search-and-grounding policy that generalizes
across different downstream image generators. Notably, although Gen-Searcher is trained with Qwen-Image as the
rollout generator during RL, it transfers well to other generators at test time. In particular, it improves Seedream 4.5
from 31.01 to 47.29, a gain of 16.28 points, and further boosts Nano Banana Pro from 50.38 to 53.30, achieving the
best overall result in the table. These results demonstrate not only the effectiveness of our search agent, but also its
strong transferability and robustness across image generators with very different native capabilities. Collectively, they
suggest that our proposed Gen-Searcher is a general and powerful model for enhancing image generation in real-world
knowledge-intensive scenarios.


**Analysis** **of** **Different** **Dimensions.** Analysis of the four evaluation dimensions shows that the gains from GenSearcher mainly come from improvements in visual correctness and text accuracy, which are also the two most
important components in KnowGen. This indicates that our search framework enables the image generator to better
produce accurate visual attributes and textual content that require real-world knowledge. In some cases, we observe
slight decreases in aesthetics, which may stem from the fact that the generator needs to integrate information from
multiple retrieved reference images and therefore cannot always produce the most ideal or visually pleasing composition.
We also find an interesting pattern on Nano Banana Pro: its improvement mainly comes from visual correctness, while
text accuracy remains almost unchanged. A possible explanation is that Nano Banana Pro already supports text-based
search internally, which helps preserve text-related performance, but it does not retrieve visual reference images, leaving
substantial room for improvement in grounding fine-grained visual attributes.


**4.3** **Performance on WISE**


Table 2 reports the performance of different models on the WISE benchmark. Compared with KnowGen, WISE is a
relatively simpler benchmark, but it still requires a certain amount of world knowledge for correct image generation.


10


Gen-Searcher: Reinforcing Agentic Search for Image Generation


Table 3: Ablation Study.


**Methods** **KnowGen**


Qwen-Image 14.98


Qwen-Image + workflow 22.91


Qwen-Image + Gen-Searcher-SFT 28.15


Qwen-Image + Gen-Searcher w.o. text reward 29.59


Qwen-Image + Gen-Searcher w.o. image reward 29.36


Qwen-Image + Gen-Searcher 31.52


Our Gen-Searcher-8B + Qwen-Image achieves the best overall performance of 0.77, significantly improving over the
original Qwen-Image baseline at 0.62 by 0.15. It also surpasses all other compared open-source models, including
LongCat-Image, HunyuanImage-3.0, and FLUX.1-dev. Looking at individual categories, our method brings clear gains
on Cultural, Time, Space, Biology, and especially Chemistry, where the score improves from 0.40 to 0.75. These results
further demonstrate that Gen-Searcher generalizes beyond KnowGen and can effectively enhance image generation on
knowledge-based image generation benchmarks.


**4.4** **Ablation Study**


In this section, we study several variants to verify the effectiveness of different components in Gen-Searcher and to
better understand the role played by each design choice in the overall framework. Specifically, we compare: (1) the
vanilla Qwen-Image baseline without any search augmentation, which directly generates images from the original
prompt; (2) Qwen-Image + workflow, which uses Qwen3-VL-8B-Instruct as the search agent in a manually designed
prompt-based search workflow without any additional training; (3) Qwen-Image + Gen-Searcher-SFT, which applies
only supervised fine-tuning to train Gen-Searcher without reinforcement learning; (4) Qwen-Image + Gen-Searcher
w.o. text reward, which removes the text-based reward and uses only image-based reward during RL training; (5)
Qwen-Image + Gen-Searcher w.o. image reward, which removes the image-based reward and uses only text-based
reward during RL training; and (6) the full Gen-Searcher model, which includes both SFT initialization and the proposed
dual reward feedback design during agentic RL training.


As shown in Table 3, all components contribute positively to the final performance. Compared with the plain QwenImage baseline, the prompt-based workflow improves the KnowGen score from 14.98 to 22.91, showing that introducing
external search alone provides benefits for knowledge-intensive image generation. Replacing the prompt-based workflow
with Gen-Searcher-SFT further improves the score to 28.15, demonstrating the advantage of learning tool-use behavior
directly from trajectory data instead of relying on manually designed prompting rules. This suggests that supervised
learning on curated search trajectories enables the model to better organize search actions, integrate retrieved evidence,
and produce more effective grounded prompts for generation. Agentic reinforcement learning brings additional gains
beyond SFT, and the full Gen-Searcher reaches the best performance of 31.52. This shows that while SFT provides
a strong initialization for basic tool use, RL is still crucial for further optimizing long-horizon search behavior and
improving the overall quality of the collected evidence and final outputs. Moreover, removing either the text reward or
the image reward leads to clear degradation, with scores dropping to 29.59 and 29.36, respectively. This confirms that
the two reward signals play complementary roles. The text reward provides more direct supervision on whether the
agent has gathered sufficient and correct information at the textual level, while the image reward aligns the policy with
the final generation outcome and encourages the collected evidence to be practically useful for image synthesis. Overall,
the ablation results validate the effectiveness of our overall framework, including learned search behavior, agentic RL
optimization, and the proposed dual-reward design.


**4.5** **Qualitative Visualization Analysis**


Figure 6 shows representative qualitative examples on the KnowGen benchmark. Overall, we find that Gen-Searcher
consistently enhances both the quality and correctness of generated images across different downstream generators


11


Prompt



Gen-Searcher: Reinforcing Agentic Search for Image Generation


Nano Pro + Gen-Searcher Nano Pro Qwen Image + Gen-Searcher Qwen Image



A professional portrait of the architect
who was awarded the Pritzker Architecture
Prize in 2024. He is seated in a minimalist
Yokohama studio; a small, elegant nameplate
on his desk must correctly show his full
name in the official English spelling. On a
shelf behind him, a monograph of his work
is visible, with the spine clearly displaying
the name of his first major housing project
and the year it was finished.


A scholarly interior featuring the 'Lothair
Crystal' resting on a velvet stand; the
accompanying museum placard correctly
lists the specific Carolingian king who
commissioned the artifact and the unique
'British Museum' accession ID assigned to
it.


A professional photograph of the 'Bahá'í
House of Worship' in Battambang,
Cambodia. A signage board in the
foreground identifies the name of the
architect who designed it and the specific
year it was dedicated to the local
community.


The divine general Vikala with her
mechanical mouse ears, the sheep-eared
general Anila, and the monkey-eared
general Andira from Granblue Fantasy
are sharing a bowl of steaming ramen at
a night festival stall under colorful
paper lanterns.


Figure 6: Examples of generated images by different methods on our KnowGen benchmark.


in knowledge-intensive, real-world scenarios. First, we observe that Nano Banana Pro still falls short in generating
accurate fine-grained visual attributes in real-world, knowledge-intensive scenarios, because it cannot perform image
search for precise visual references. As a result, the generated identity, object appearance, or architectural details
may deviate from the target even when some textual information is correct. In contrast, Gen-Searcher improves Nano
Banana Pro by searching relevant reference images and grounding the generation with more accurate visual evidence.
An interesting finding is that for Qwen-Image, even when the search agent has already collected correct information,
the final generation sometimes can still be inaccurate due to limitations of the image generator itself (e.g., multi-subject
consistency issue, poor text rendering issue). The fourth row in Figure 6 provides one such example, where the searched
content is correct but the generated image still fails to faithfully realize the required multi-character details. In summary,
these examples show that Gen-Searcher can substantially improve generation by providing grounded textual and visual
evidence for both strong propriety model Nano Banana Pro and open-source model Qwen-Image, while the some failure
cases also indicate that the capability of the downstream image generator also remains a challenge.


**4.6** **Parameter Analysis**


We further analyze the balancing coefficient _α_ between the text reward and the image reward in our dual-feedback
design. Figure 3 demonstrates the performance of our Gen-Searcher using different _α_ for RL training. We observe that
setting _α_ = 0 or _α_ = 1 _._ 0 leads to clear performance degradation, indicating that both reward signals are necessary for
effective training. This is consistent with our motivation: relying only on image reward introduces high variance due to
the stochasticity and limited capability of the downstream generator, while relying only on text reward ignores whether
the gathered information can actually support high-quality image synthesis. In contrast, we find that performance
remains consistently strong when _α_ is set in the range of 0 _._ 3 to 0 _._ 6, showing that our method is relatively insensitive to
this hyperparameter over a relatively broad range.


12


Gen-Searcher: Reinforcing Agentic Search for Image Generation


33

32

31

30

29

28

27

26

25


**5** **Conclusion**


**References**

|Col1|Col2|Col3|Col4|Col5|Col6|Col7|Col8|Col9|Col10|Col11|Col12|Col13|Col14|Col15|Col16|Col17|Col18|Col19|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
||||||||||||||||||||
||||||||||||||||||||
||||||||||||||||||||
||||||||||||||||||||
||||||||||||||||||||
||||||||||||||||||||
||||||||||||||||||||
||||||||||||||||||||
||||||||||||||||||||
||||||||||||||||||||
||||||||||||||||||||
|n-S<br>  nti<br> -10<br>  no<br>  e o<br> w th<br>  wh<br>  n fo<br>  ing<br> ica<br>emi<br>/, 2<br> , Ru<br> ffci<br> .<br>  u,<br>_ 09.1_<br> bin<br>_  rma_<br>u, <br>  m<br>  Sun<br> . _a_<br>  ng<br> age<br>  Zhe<br>rea<br>  ng,<br>rin<br>ini|~~0~~<br>   earche<br>  c RL. T<br> k, Gen<br>  wledge<br>  f super<br>  at Gen<br>  ile also<br>   r futur<br>  ren Zho<br> l report.<br>ni ima<br> 025.<br>  oyi Du<br> ent ima<br>  Chitwan<br>_ 4491_, 2<br>  Romba<br>_  tion Pr_<br>Binghui<br>  ultimod<br> , Yukan<br>_rXiv pre_<br>   Huang,<br> ntic cog<br>  n Zhang<br>king ne<br>  Manyu<br>g reaso<br> 3 pro.|~~0~~<br>   earche<br>  c RL. T<br> k, Gen<br>  wledge<br>  f super<br>  at Gen<br>  ile also<br>   r futur<br>  ren Zho<br> l report.<br>ni ima<br> 025.<br>  oyi Du<br> ent ima<br>  Chitwan<br>_ 4491_, 2<br>  Romba<br>_  tion Pr_<br>Binghui<br>  ultimod<br> , Yukan<br>_rXiv pre_<br>   Huang,<br> ntic cog<br>  n Zhang<br>king ne<br>  Manyu<br>g reaso<br> 3 pro.|r, th<br>   o en<br> -Sea<br>  -int<br>   vise<br>  -Sea<br>   exh<br>   e res<br>   u, Ju<br> _arX_<br>ge pr<br>  , Pen<br> ge g<br>   Saha<br> 022.<br>  ch, K<br>_  ocess_<br> Li, <br>  al ret<br>  g Fe<br>_ print_<br>   Don<br> nitiv<br>  , Xin<br> w fro<br>  an Z<br> ning r<br>htt|~~0.3~~<br>Figure<br>   e frst a<br>   able th<br> rcher-<br>  ensive<br>   d fne-t<br>  rcher b<br>   ibiting<br>    earch<br>   nyang L<br>_iv prepr_<br>o: Hig<br>   g Gao,<br>  eneratio<br>   ria, and<br>  aan Ok<br>_  ing Sys_<br>Geng C<br>  rieval a<br>   ng, Min<br>_ arXiv:_<br>   gzhi Ji<br> e search<br>   yu Wan<br> ntier of<br>   hang, T<br> eward<br>s://|~~0.3~~<br>Figure<br>   e frst a<br>   able th<br> rcher-<br>  ensive<br>   d fne-t<br>  rcher b<br>   ibiting<br>    earch<br>   nyang L<br>_iv prepr_<br>o: Hig<br>   g Gao,<br>  eneratio<br>   ria, and<br>  aan Ok<br>_  ing Sys_<br>Geng C<br>  rieval a<br>   ng, Min<br>_ arXiv:_<br>   gzhi Ji<br> e search<br>   yu Wan<br> ntier of<br>   hang, T<br> eward<br>s://|7: P<br>    ttem<br>    is se<br> RL-6<br>  imag<br>   unin<br>   ring<br>    stro<br>    on se<br>    in, K<br>_ int a_<br>h-qu<br>    Steve<br>  n fou<br>    Will<br>   tay, J<br>_   tems_,<br>hen, <br>   ugme<br>   glian<br>_ 2505._<br>    ang,<br>  and<br>    g, Q<br>  visio<br>   iansh<br>  mode<br>eep|~~0.4~~<br>arame<br>    pt to tr<br>    tting,<br> k, and<br>  e gene<br>   g and<br>   s subst<br>    ng tran<br>     arch a<br>    aiyuan<br>_ rXiv:25_<br>ality im<br>    n Hoi,<br>  ndation<br>    iam W<br>   onas M<br> 35:153<br> Chong <br>   nted m<br>   g Zhai<br>_ 15779_,<br>    Chenju<br>   reasoni<br>    iuchen<br>  n-langu<br>   uo Pen<br>  l for ag<br>mind.|~~0.4~~<br>arame<br>    pt to tr<br>    tting,<br> k, and<br>  e gene<br>   g and<br>   s subst<br>    ng tran<br>     arch a<br>    aiyuan<br>_ rXiv:25_<br>ality im<br>    n Hoi,<br>  ndation<br>    iam W<br>   onas M<br> 35:153<br> Chong <br>   nted m<br>   g Zhai<br>_ 15779_,<br>    Chenju<br>   reasoni<br>    iuchen<br>  n-langu<br>   uo Pen<br>  l for ag<br>mind.|ter A<br>     ain a<br>     we b<br>  intro<br>   ratio<br>    agen<br>   antia<br>    sfera<br>     gents<br>     Gao,<br>_ 08.02_<br>age <br>     Zhao<br>   mo<br>     Cohe<br>    üller,<br> 09–1<br> Che<br>   ultim<br>   , Yifa<br> 2025<br>    e Zha<br>   ng int<br>     Wang<br>  age d<br>    g, Zh<br>   ents. <br>goo|~~0.5~~<br> nlysis<br>      multim<br>     uild a<br>  duce t<br>   n. Ba<br>    tic rein<br>   l gains<br>    bility a<br>      for re<br>     Kun Ya<br>_ 324_, 20<br>generat<br>     hui Hou<br>   del with<br>     n. Re-i<br>    and Bj<br> 5324, 2<br>n, and <br>   odal ge<br>    n Chan<br> .<br>     ng, Le<br>   o imag<br>    , Ruixu<br>   eep res<br>    ixun Li<br> _arXiv p_<br>gle/m|~~0.5~~<br> nlysis<br>      multim<br>     uild a<br>  duce t<br>   n. Ba<br>    tic rein<br>   l gains<br>    bility a<br>      for re<br>     Kun Ya<br>_ 324_, 20<br>generat<br>     hui Hou<br>   del with<br>     n. Re-i<br>    and Bj<br> 5324, 2<br>n, and <br>   odal ge<br>    n Chan<br> .<br>     ng, Le<br>   o imag<br>    , Ruixu<br>   eep res<br>    ixun Li<br> _arXiv p_<br>gle/m|on_ α_<br>      odal<br>      dedi<br>   he K<br>sed o<br>     forc<br>    acro<br>     cros<br>      al-w<br>      n, Sh<br> 25.<br>ion.<br>     , Shi<br>    sing<br>mage<br>     örn O<br> 022.<br>Went<br>    nerat<br>     g, an<br>     qi Zh<br>    e gen<br>     e Din<br>   earch<br>    , Yile<br>_ repri_<br>ode|~~0.6~~<br> .<br>       deep s<br>      cated d<br>   nowGe<br> n thes<br>     ement<br>    ss diffe<br>     s imag<br>      orld im<br>      eng-mi<br>http<br>      jie Hua<br>    le-strea<br>n: Retri<br>     mmer. <br>ao Zha<br>    ion. _arX_<br>     d Kaip<br>      u, Renr<br>    eration. <br>      g, Che<br>    agent. <br>     i Jiang,<br>_ nt arXi_<br>s/ge|~~0.6~~<br> .<br>       deep s<br>      cated d<br>   nowGe<br> n thes<br>     ement<br>    ss diffe<br>     s imag<br>      orld im<br>      eng-mi<br>http<br>      jie Hua<br>    le-strea<br>n: Retri<br>     mmer. <br>ao Zha<br>    ion. _arX_<br>     d Kaip<br>      u, Renr<br>    eration. <br>      g, Che<br>    agent. <br>     i Jiang,<br>_ nt arXi_<br>s/ge|earc<br>       ata p<br>   n be<br> e res<br>     learn<br>     rent<br>     e gen<br>       age<br>      ng Y<br>s://<br>       ng, D<br>    m dif<br>eval-<br> Retr<br>ng. <br>_iv pr_<br>      eng<br>      ui Z<br> _arXi_<br>      nxi W<br> _arXi_<br>      Shu<br>_ v:260_<br>ini|~~1~~<br>       h agent<br>       ipelin<br>    nchma<br>  ources<br>     ing wi<br>     image<br>      erator<br>       genera<br>       in, Shua<br>deepm<br>       engyan<br>    fusion t<br>augmen<br>ieval-au<br>M2io-r1<br>_ eprint a_<br>      Zhang. <br>       hang, X<br>_v prepr_<br>       ang, Jia<br>_v prepri_<br>      ang Che<br>_ 1.2215_<br>/pro/|~~1~~<br>       h agent<br>       ipelin<br>    nchma<br>  ources<br>     ing wi<br>     image<br>      erator<br>       genera<br>       in, Shua<br>deepm<br>       engyan<br>    fusion t<br>augmen<br>ieval-au<br>M2io-r1<br>_ eprint a_<br>      Zhang. <br>       hang, X<br>_v prepr_<br>       ang, Jia<br>_v prepri_<br>      ang Che<br>_ 1.2215_<br>/pro/|fo<br>       e, c<br>    rk t<br> , w<br>      th<br>      gen<br>      s. W<br>       tion<br>       i B<br>in<br>       g Ji<br>     ran<br>ted<br>gm<br>: A<br>_ rXi_<br> Ia-t<br>       ian<br>_ int_<br>       lon<br>_ nt a_<br>       n,<br>_ 4_, 2<br>, 2|



[12] Bytedance Seed. Seed1.8 model card: Towards generalized real-world agency. [https://seed.bytedance.com/en/](https://seed.bytedance.com/en/seed1_8)
[seed1_8, 2025.](https://seed.bytedance.com/en/seed1_8)


13


Gen-Searcher: Reinforcing Agentic Search for Image Generation


[13] Daya Guo, Dejian Yang, Haowei Zhang, Junxiao Song, Peiyi Wang, Qihao Zhu, Runxin Xu, Ruoyu Zhang, Shirong Ma, Xiao
Bi, et al. Deepseek-r1: Incentivizing reasoning capability in llms via reinforcement learning. _arXiv preprint arXiv:2501.12948_,
2025.


[14] Kaituo Feng, Manyuan Zhang, Hongyu Li, Kaixuan Fan, Shuang Chen, Yilei Jiang, Dian Zheng, Peiwen Sun, Yiyuan Zhang,
Haoze Sun, et al. Onethinker: All-in-one reasoning model for image and video. _arXiv preprint arXiv:2512.03043_, 2025.


[15] Bytedance Seed. Seedream 4.5. [https://seed.bytedance.com/en/seedream4_5, 2025.](https://seed.bytedance.com/en/seedream4_5)


[16] Yuwei Niu, Munan Ning, Mengren Zheng, Weiyang Jin, Bin Lin, Peng Jin, Jiaqi Liao, Chaoran Feng, Kunpeng Ning, Bin Zhu,
et al. Wise: A world knowledge-informed semantic evaluation for text-to-image generation. _arXiv preprint arXiv:2503.07265_,
2025.


[17] Hongyu Li, Manyuan Zhang, Dian Zheng, Ziyu Guo, Yimeng Jia, Kaituo Feng, Hao Yu, Yexin Liu, Yan Feng, Peng Pei, et al.
Editthinker: Unlocking iterative reasoning for any image editor. _arXiv preprint arXiv:2512.05965_, 2025.


[18] Dian Zheng, Manyuan Zhang, Hongyu Li, Kai Zou, Hongbo Liu, Ziyu Guo, Kaituo Feng, Yexin Liu, Ying Luo, Yan Feng, et al.
Architecture decoupling is not all you need for unified multimodal model. _arXiv preprint arXiv:2511.22663_, 2025.


[19] Hang Chen, Qian Xiang, Jiaxin Hu, Meilin Ye, Chao Yu, Hao Cheng, and Lei Zhang. Comprehensive exploration of diffusion
models in image generation: a survey. _Artificial Intelligence Review_, 58(4):99, 2025.


[20] Stability AI. Stable diffusion 3.5 large. [https://huggingface.co/stabilityai/stable-diffusion-3.](https://huggingface.co/stabilityai/stable-diffusion-3.5-large)
[5-large, 2024.](https://huggingface.co/stabilityai/stable-diffusion-3.5-large)


[21] Google DeepMind. Imagen. [https://deepmind.google/models/imagen/, 2025.](https://deepmind.google/models/imagen/)


[22] black-forest labs. Flux 1. [https://github.com/black-forest-labs/flux, 2024.](https://github.com/black-forest-labs/flux)


[23] Meituan LongCat Team, Hanghang Ma, Haoxian Tan, Jiale Huang, Junqiang Wu, Jun-Yan He, Lishuai Gao, Songlin Xiao,
Xiaoming Wei, Xiaoqi Ma, et al. Longcat-image technical report. _arXiv preprint arXiv:2512.07584_, 2025.


[24] Guanting Dong, Hangyu Mao, Kai Ma, Licheng Bao, Yifei Chen, Zhongyuan Wang, Zhongxia Chen, Jiazhen Du, Huiyang
Wang, Fuzheng Zhang, et al. Agentic reinforced policy optimization. _arXiv preprint arXiv:2507.19849_, 2025.


[25] Chaoyang Wang, Kaituo Feng, Dongyang Chen, Zhongyu Wang, Zhixun Li, Sicheng Gao, Meng Meng, Xu Zhou, Manyuan
Zhang, Yuzhang Shang, et al. Adatooler-v: Adaptive tool-use for images and videos. _arXiv preprint arXiv:2512.16918_, 2025.


[26] Junfei Wu, Jian Guan, Kaituo Feng, Qiang Liu, Shu Wu, Liang Wang, Wei Wu, and Tieniu Tan. Reinforcing spatial reasoning
in vision-language models with interwoven thinking and visual drawing. _arXiv preprint arXiv:2506.09965_, 2025.


[27] Xiaoying Zhang, Yipeng Zhang, Hao Sun, Kaituo Feng, Chaochao Lu, Chao Yang, and Helen Meng. Critique-grpo: Advancing
llm reasoning with natural language and numerical feedback. _arXiv preprint arXiv:2506.03106_, 2025.


[28] Kaituo Feng, Kaixiong Gong, Bohao Li, Zonghao Guo, Yibing Wang, Tianshuo Peng, Junfei Wu, Xiaoying Zhang, Benyou
Wang, and Xiangyu Yue. Video-r1: Reinforcing video reasoning in mllms. _arXiv preprint arXiv:2503.21776_, 2025.


[29] Shuang Chen, Yue Guo, Zhaochen Su, Yafu Li, Yulun Wu, Jiacheng Chen, Jiayu Chen, Weijie Wang, Xiaoye Qu, and Yu Cheng.
Advancing multimodal reasoning: From optimized cold start to staged reinforcement learning. _arXiv preprint arXiv:2506.04207_,
2025.


[30] Kaixuan Fan, Kaituo Feng, Haoming Lyu, Dongzhan Zhou, and Xiangyu Yue. Sophiavl-r1: Reinforcing mllms reasoning with
thinking reward. _arXiv preprint arXiv:2505.17018_, 2025.


[31] Shuang Chen, Yue Guo, Yimeng Ye, Shijue Huang, Wenbo Hu, Haoxi Li, Manyuan Zhang, Jiayu Chen, Song Guo, and Nanyun
Peng. Ares: Multimodal adaptive reasoning via difficulty-aware token-level entropy shaping. _arXiv preprint arXiv:2510.08457_,
2025.


[32] Lang Feng, Zhenghai Xue, Tingcong Liu, and Bo An. Group-in-group policy optimization for llm agent training. _arXiv preprint_
_arXiv:2505.10978_, 2025.


[33] Wenxuan Huang, Yu Zeng, Qiuchen Wang, Zhen Fang, Shaosheng Cao, Zheng Chu, Qingyu Yin, Shuang Chen, Zhenfei Yin,
Lin Chen, et al. Vision-deepresearch: Incentivizing deepresearch capability in multimodal large language models. _arXiv_
_preprint arXiv:2601.22060_, 2026.


[34] Shuang Sun, Huatong Song, Yuhao Wang, Ruiyang Ren, Jinhao Jiang, Junjie Zhang, Fei Bai, Jia Deng, Wayne Xin Zhao,
Zheng Liu, et al. Simpledeepsearcher: Deep information seeking via web-powered reasoning trajectory synthesis. _arXiv_
_preprint arXiv:2505.16834_, 2025.


[35] OpenAI. Introducing gpt-4.1 in the api. [https://openai.com/index/gpt-4-1/, 2025.](https://openai.com/index/gpt-4-1/)


[36] Shuai Bai, Yuxuan Cai, Ruizhe Chen, Keqin Chen, Xionghui Chen, Zesen Cheng, Lianghao Deng, Wei Ding, Chang Gao,
Chunjiang Ge, et al. Qwen3-vl technical report. _arXiv preprint arXiv:2511.21631_, 2025.


[37] OpenAI. Gpt-image-1: Models and capabilities for image generation. [https://platform.openai.com/docs/](https://platform.openai.com/docs/models/gpt-image-1)
[models/gpt-image-1, 2024.](https://platform.openai.com/docs/models/gpt-image-1)


[38] OpenAI. [Gpt-image-1.5: Enhanced visual reasoning and creative generation. https://platform.openai.com/docs/](https://platform.openai.com/docs/models/gpt-image-1.5)
[models/gpt-image-1.5, 2025.](https://platform.openai.com/docs/models/gpt-image-1.5)


14


Gen-Searcher: Reinforcing Agentic Search for Image Generation


[39] Google DeepMind. Gemini image: High-quality image generation. [https://deepmind.google/models/](https://deepmind.google/models/gemini-image/flash/)
[gemini-image/flash/, 2025.](https://deepmind.google/models/gemini-image/flash/)


[40] Team Seedream, Yunpeng Chen, Yu Gao, Lixue Gong, Meng Guo, Qiushan Guo, Zhiyao Guo, Xiaoxia Hou, Weilin Huang,
Yixuan Huang, et al. Seedream 4.0: Toward next-generation multimodal image generation. _arXiv preprint arXiv:2509.20427_,
2025.


[41] Stability AI. Stable diffusion 3.5 medium. [https://huggingface.co/stabilityai/stable-diffusion-3.](https://huggingface.co/stabilityai/stable-diffusion-3.5-medium)
[5-medium, 2024.](https://huggingface.co/stabilityai/stable-diffusion-3.5-medium)


[42] Qi Qin, Le Zhuo, Yi Xin, Ruoyi Du, Zhen Li, Bin Fu, Yiting Lu, Xinyue Li, Dongyang Liu, Xiangyang Zhu, et al. Luminaimage 2.0: A unified and efficient image generative framework. In _Proceedings of the IEEE/CVF International Conference on_
_Computer Vision_, pages 20031–20042, 2025.


[43] black-forest labs. Flux 2. [https://github.com/black-forest-labs/flux2, 2025.](https://github.com/black-forest-labs/flux2)


[44] Chaorui Deng, Deyao Zhu, Kunchang Li, Chenhui Gou, Feng Li, Zeyu Wang, Shu Zhong, Weihao Yu, Xiaonan Nie, Ziang
Song, et al. Emerging properties in unified multimodal pretraining. _arXiv preprint arXiv:2505.14683_, 2025.


[45] Siyu Cao, Hangting Chen, Peng Chen, Yiji Cheng, Yutao Cui, Xinchi Deng, Ying Dong, Kipper Gong, Tianpeng Gu, Xiusen
Gu, et al. Hunyuanimage 3.0 technical report. _arXiv preprint arXiv:2509.23951_, 2025.


[46] Stability AI. Stable diffusion 3 medium. [https://huggingface.co/stabilityai/](https://huggingface.co/stabilityai/stable-diffusion-3-medium)
[stable-diffusion-3-medium, 2024.](https://huggingface.co/stabilityai/stable-diffusion-3-medium)


[47] Xinlong Wang, Xiaosong Zhang, Zhengxiong Luo, Quan Sun, Yufeng Cui, Jinsheng Wang, Fan Zhang, Yueze Wang, Zhen Li,
Qiying Yu, et al. Emu3: Next-token prediction is all you need. _arXiv preprint arXiv:2409.18869_, 2024.


15


Gen-Searcher: Reinforcing Agentic Search for Image Generation


**A** **KnowGen Benchmark Evaluation Prompt**





16


Gen-Searcher: Reinforcing Agentic Search for Image Generation





**B** **Text Reward Prompt**







17


Gen-Searcher: Reinforcing Agentic Search for Image Generation





**C** **System Prompt**







18


Gen-Searcher: Reinforcing Agentic Search for Image Generation





19


Gen-Searcher: Reinforcing Agentic Search for Image Generation





20


