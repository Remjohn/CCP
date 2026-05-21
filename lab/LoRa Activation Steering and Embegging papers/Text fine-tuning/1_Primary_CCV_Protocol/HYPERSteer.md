## **HYPERSTEER: Activation Steering at Scale with Hypernetworks**



**Jiuding Sun** [*]
Stanford University
sunjd24@stanford.edu


**Michael Sklar**
Confirm Labs
michaelbsklar@gmail.com


**Abstract**



**Sidharth Baskaran** [*]
Pr(Ai) [2] R Group
Georgia Institute of Technology
sidnbaskaran@gmail.com


**Christopher Potts**
Stanford University
cgpotts@stanford.edu



**Zhengxuan Wu**
Stanford University
zhengxuan@stanford.edu


**Atticus Geiger**
Pr(Ai) [2] R Group
atticusg@gmail.com







Steering language models (LMs) by modifying
internal activations is a popular approach for
controlling text generation. Unsupervised dictionary learning methods, e.g., sparse autoencoders, can be scaled to produce many steering
vectors, but lack guarantees on the individual efficacy of each vector and control over the coverage of relevant steering tasks. In contrast, supervised methods for constructing steering vectors
are targeted and effective, but require more data
collection and training for each additional steering vector produced. In this work, we introduce HYPERSTEER, a family of hypernetworkbased architectures which are trained end-toend to generate steering vectors conditioned
on the natural language steering prompts and
the internals of the steered LM. In our evaluations, we show that scaling HYPERSTEER with
thousands of steering prompts exceeds the performance of state-of-the-art activation steering
methods, even on steering prompts never seen
during training. Moreover, HYPERSTEER performs on par with steering-via-prompting. We
release ours at � [stanfordnlp/axbench.](https://github.com/stanfordnlp/axbench)


**1** **Introduction**


How can the outputs of a language model (LM) be
reliably controlled? With instruction-tuned LMs,
the standard approach is prompt engineering. However, prompting-based approaches face challenges
from user jailbreaks, forgotten instructions, and
robustness to model misalignment. A more aggressive approach is (parameter-efficient) fine-tuning,
but this requires modifying or injecting new parameters into the model. Activation steering (Giulianelli et al., 2018) occupies a middle ground: it is
lightweight to implement (no parameters are modified or added) and can affect the model in ways
standard prompting cannot.
Methods for obtaining steering vectors can generally be classified into two groups: _unsuper-_


*Equal contribution.



Figure 1: The state-of-the-art HYPERSTEER Model: A
transformer hypernetwork uses self attention to process
a steering prompt and uses a cross attention module to
read from the residual stream of a base LM run on a
second prompt. The hypernetwork outputs a steering
vector that is added to the base LM residual stream.


_vised_, e.g., Sparse Autoencoders (SAEs) (Hernandez et al., 2022; Cunningham et al., 2023; Bricken
et al., 2023; Gao et al., 2024; Marks et al., 2025),
which produce a large number of unlabeled steering
vectors, and _supervised_, where task-specific steering vectors are either directly trained (Wu et al.,
2024a, 2025) or derived using labeled data (Li
et al., 2023a; Marks and Tegmark, 2023; Turner
et al., 2023; Rimsky et al., 2024). Unsupervised
methods are scalable, but lack the ability to create
steering vectors for specific tasks. Alternatively, a
supervised approach is effective and targeted, but
requires per-task data collection and/or training.
Our main contribution is HYPERSTEER, a suite
of end-to-end trainable hypernetwork architectures
which learn to generate steering vectors for an








































0.8


0.7


0.6


0.5


0.4


0.3


0.2


0.1









|Col1|Col2|Col3|Col4|Col5|Col6|Col7|Col8|Col9|Col10|Col11|Col12|Col13|Col14|Col15|Col16|Col17|Col18|Col19|Col20|Col21|Col22|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|||||||||||Ste|ering|via|p|romptin|g|||||||
|||||||||||||||||||||||
||~~Hy~~<br>No<br>~~In~~|~~per~~<br> Con<br>~~ ont~~|~~St~~<br> tex<br>~~ xt~~|~~e~~<br> t<br>~~ L~~|~~r~~<br>~~ a~~|~~ r~~|~~ i~~|~~ g~~||||||||||||||
||<br>Cro|<br>ss A|<br> tte|<br> nti|<br> o|<br> n||||Pre<br>Re|vious<br>T-r1|be<br> (Dic|st<br> ti|onary L|earni|ng)||||||
|||||||||||||||||||||||
|||||||||||||||||||||||
|||||||||||||||||||||||
|||||||||||||||||||||||
|||||||||||||||||||||||


Number of Steering Prompts


Figure 2: Performance on steering prompts that have
**never** **been** **seen** **during** **training** for HYPERSTEER
variants as the number of steering prompts used in training increases ( _x_ -axis in log scale). An exponential
increase in training data results in an approximately
linear increase in performance. When trained on all
_≈_ 16k steering prompts in AxBench, the performance of
HYPERSTEER on steering prompts never seen during
training surpasses ReFT-r1 steering vectors which are
trained and evaluated on the same steering prompt.


instruction-tuned base LM, conditioned on the
steering prompt and (optionally) the base LM
prompt and internal activations. We train and evaluate on the steering prompts from AXBENCH (Wu
et al., 2025). Our best HYPERSTEER variant outperforms the previous state-of-the-art activation
steering method from AXBENCH, even on held-out
steering prompts, never seen during training. We
show steering performance scales logarithmically
with number of steering prompts during training.
Surprisingly, we are even able to match the performance of the steering-via-prompting, which outperformed all activation steering methods on AxBench.
In sum, HYPERSTEER combines the scalability of
unsupervised dictionary learning with the targeted
control of supervised activation steering.


**2** **Preliminaries**


**Activation Steering** The goal of activation steering is to elicit a certain behavior from a base LM _B_
run on an base prompt by adding a steering vector
to a hidden vector **h** . Our hypernetwork-based approach to activation steering has the more general
goal of taking any base prompt _x_, e.g., _Explain how_
_to sort lists of numbers._, and any steering prompt
_s_, e.g., _Output using C/C++ programming syntax_,
and producing a steering vector ∆ _[x]_ _s_ [added] [to] **[h]** [.]
Denote the steered output:


**y** ˆsteer = _B_    - _x |_ **h** _←_ **h** + ∆ _[x]_ _s_    - _._ (1)



**Gemma-2-2b** **Gemma-2-9b**
**Method**
**Held-out** **Held-in** **Held-out** **Held-in**


LoReFT  - 0.722  - 0.777
SFT  - 0.714  -  LoRA  - 0.641  - 0.602


ReFT-r1  - 0.509  - 0.630
DiffMean  - 0.178  - 0.322
SAE  - 0.151  - 0.191
SAE-A  - 0.132  - 0.186
HYPERSTEER

  - No Context 0.373 0.512 0.633 0.751

  - In Context Learning 0.480 0.547 0.760 0.842

  - Cross Attention 0.608 **0.742** 0.934 **1.091**


Table 1: Steering results for baseline methods from
AxBench and our three HYPERSTEER variants, evaluated on Concept500-HO (steering prompts never seen
during training) and Concept500-HI (steering prompts
seen during training, base prompts unseen during training). The cross attention variant outperforms all other
variants by a large margin on held-out evaluation and approaches prompting performance on held-in evaluation,
while all variants outperform the ReFT-r1 baseline on
held-in evaluation. The intervention happened at Layer
20 of both models.


**Hypernetworks** Prior work has shown hypernetworks to be effective at zero-shot adaptation of
language models on a variety of tasks, matching
or exceeding comparable methods such as finetuning with parameter efficient methods (Phang
et al., 2023). Formally, a hypernetwork (Ha et al.,
2016) is a function _H_ : _T_ _→_ Θ that maps tasks
_t ∈T_ to parameters _θt_ = _H_ ( _t_ ).
For our purposes, the tasks are pairs on input
and steering prompts ( _x, s_ ) _∈T_ and the output
parameters are steering vectors:


_H_ ( _x, s_ ) = ∆ _[x]_ _s_ _[∈]_ [R] _[d][.]_ (2)


**Dataset and Evaluation** For all experiments, we
use AXBENCH (Wu et al., 2025) as the training
dataset and evaluation harness. The training data
sets consist of a total of 16,000 steering prompts
sourced from GemmaScope Sparse Autoencoder
(SAE) feature labels (Lieberum et al., 2024) and
base prompts sourced from a diverse instruction
pool (see App. A.5 for details). We keep fixed ratios of base prompt to steering prompt (72 : 1 for
train; 10 : 1 for evaluation).
For evaluation, the steering prompts are applied
on a set of different base prompts sourced from
AlpacaEval (Li et al., 2023b), and a gpt-4o-mini
judge model (OpenAI et al., 2024) computes discrete scores in _{_ 0 _,_ 1 _,_ 2 _}_ along three dimensions of


success: following the base prompt, following the
steering prompt, and text fluency. The harmonic
mean of these three scores is the final metric, which
we refer to as the _steering performance_ .
We evaluate on two datasets: Concept500-HI
(held-in), the standard AXBENCH setting with 500
steering prompts seen during training plus unseen
base prompts, and Concept500-HO (held-out), a
test set with 500 steering prompts not seen during
training. Notably, the only the prompt engineering
baseline from AxBench can be evaluated on the
held out test set alongside HYPERSTEER.


**Baselines** We report the fine-tuning, activation
steering, and prompting baselines from AXBENCH.
The state-of-the-art activation steering method
ReFT-r1 is an important point of comparison for
our method. See Appendix A.6 for details.


**3** **HYPERSTEER**


We consider multiple HYPERSTEER variants, all of
which employ a transformer hypernetwork _H_ with
_L_ layers and residual stream representations **h** _[t]_ _l_ [for]
each layer _l_ and token _t_ from the steering prompt **s**
with _T_ tokens. All variants have an MLP module
that maps from the residual stream of the last layer
and token to a steering vector:


_H_ ( _s, x_ ) = MLP( _h_ _[T]_ _L_ [) = ∆] _[x]_ _s_ _[.]_ (3)


We train _B_ on a language modeling loss using the
output **y** ˆsteer (see Equation 1) of the base model
_B_ under a steering intervention and an expected
output **y** label from AxBench:


_L_ LM( _x, s_ ) = CrossEntropy(ˆ **y** steer _,_ **y** label) _._ (4)


We consider a range of architectures with incrementally more access to the base LM _L_ and prompt _x_ .


**No** **context** No access to the base prompt _x_ or
the base LM _B_, meaning _H_ ( _x, s_ ) = _H_ ( _s_ ) = ∆ _s_ .


**In Context Learning** This variant appends the
base prompt _x_ to the source prompt _s_ and feeds the
resulting text into hypernetwork _H_ .


**Cross** **Attention** Our best-performing variant
conditions on both the steering prompt _s_ and the internal activations of the base LM _B_ run on prompt
_x_ . A cross-attention modules at each layer of the
hypernetwork _H_ uses the hypernetwork residual
stream for attention head queries and outputs and
the base LM residual stream at the steering layer _l_
as attention head keys and values (App. A.3). This
is a simplification of HyperDAS (Sun et al., 2025).


|Col1|Col2|Col3|Col4|Col5|Col6|Col7|Col8|
|---|---|---|---|---|---|---|---|
||||||ReFT-r1<br>|||
||||||HyperSt|eer||
|||||||||
||2.4 X|||||||
|||||||||
|||||||||
|||||||||
||||||~~0.07~~|~~ X~~|~~ X~~|
|||||||||



Figure 3: As the number of steering prompts in our
training dataset increases, the teraFLOPs (TFLOPS)
required to attain a similar loss on a _held-in_ evaluation set (steering prompts seen during training, but base
prompt unseen during training) decreases for our best
HYPERSTEER variant (cross attention). This value is
approximately constant for our dictionary learning baseline of ReFT-r1. See Appendix A.3.2 for details.


**4** **Experiments**


We implement HYPERSTEER building on the
AXBENCH (Wu et al., 2025) codebase using
pyvene (Wu et al., 2024b) to implement steering methods. Training runs are done on a single NVIDIA A100-80GB GPU. Hyperparameter
details in A.2. Ourexperiments steer two base
LMs, namely, the 2B and 9B variants of Gemma-2
instruction-tuned. (Rivière et al., 2024), with its
parameters frozen during training. The hypernetworks used are unfrozen copies of the base model
with later layers removed. We train each HYPERSTEER variant on steering prompt datasets ranging
from 10 up to the full _≈_ 16000 steering prompts
available in AXBENCH.


**Generalization** **Results** We evaluate HYPERSTEER on AXBENCH’s Concept500-HI and
Concept500-HO and report results in Table 1. **our**
**cross-attention HYPERSTEER variant performs**
**better on unseen steering prompts than every su-**
**pervised activation steering baseline trained and**
**evaluated** **on** **the** **same** **steering** **prompt.** However, HYPERSTEER falls slightly behind prompting and the best fine-tuning baselines. Figure 2
shows that the cross-attention variant outperforms
the other architectures at every dataset scale.


**Compute efficiency** We study the efficacy of HY
PERSTEER with respect to the FLOPs needed to
maintain the evaluation loss on a held-in dataset



1600


1400


1200


1000


800


600


400


200


0



10 100 1k 10k
Number of Steering Prompts (n)






**HYPERSTEER** **(Cross Attention)** Held-in Held-out


_Initialization_
Random 0.601 0.582


_Decoder Blocks_
_N_ = 2 0.707 0.549
_N_ = 4 0.713 0.597
_N_ = 8 0.721 0.610


**HYPERSTEER** **(No Context)**


_Training Objective_
Reconstruction Loss 0.511 0.375


Table 2: Ablation study using Gemma-2-2B on architecture choices of HYPERSTEER after 1 epoch of training
and evaluation on a small test set Concept10. We find
that pre-trained initialization of the cross-attention architecture improves performance in both held-in and
held-out scenarios, and in both cases performance improves with the number of hypernetwork decoder blocks.
For the no-context hypernetworks which do not condition steering vectors on input prompts, reconstructing
ground truth vectors is comparable to end-to-end training with a language modeling objective.


as we increase the training data used. We compare
against the state-of-the-art supervised activation
steering method ReFT-r1. Observe in Figure 3),
that as training data increases HYPERSTEER becomes much more economical than supervised activation steering. See details in Appendix A.3.2.


**Ablation Study** We show results for various ablation studies on the cross-attention variant of HY
PERSTEER in Table 2. We randomly initialize the
Gemma2-2B hypernetwork and find that pretrained
parameters provide a significant performance boost
(+0.112 steering score). We also remove a number of hypernetwork decoder blocks in the range
_N_ = _{_ 2 _,_ 4 _,_ 8 _,_ 20 _}_ and adjust learning rate ac
~~�~~
cordingly: lr( _n_ ) = 8 _×_ 10 _[−]_ [5] _·_ 20 _n_ [.] [Increased]

depth results in incremental improvements to steering performance on held in and held out test sets.
However, notably the number of decoder blocks
has a greater impact on generalization to steering
prompts unseen in training (+0.07) compared to
steering prompts unseen in training (+0.03).


We also perform an ablation on the no context
HYPERSTEER variant where we train the hypernetwork to reconstruct the steering vectors constructed
by the original AxBench ReFT baselines. Given
a steering vector _H_ ( _s, x_ ) = _H_ ( _s_ ) = ∆ _s_ and a



gold-label steering vector ∆ _[∗]_ _s_ [the loss is]


_L_ recon( _s_ ) = 1 _−_ CosSim(∆ _s,_ ∆ _[∗]_ _s_ [)+] _[||]_ [∆] _[s]_ _[−]_ [∆] _[∗]_ _s_ _[||]_ [2] 2 _[.]_


The two loss terms are roughly comparable, so we
use language modeling.


**5** **Qualitative Analyses**


We generate 2500 steering vectors using base and
steering prompts from our held-out test data.


**Geometric visualization of steering vectors** We
analyze steering vectors generated by HYPERSTEER (Cross Attention) using t-SNE (van der
Maaten and Hinton, 2008) and PCA (2 components) to find geometric structure among steering
vectors (see Fig. 4 and 5 in App. A.7.1).


**Pairwise similarity of steering vectors** We compute pairwise cosine similarities of steering vectors on both in-context (reconstruction) and cross
attention models to understand how conditioning
on the input prompt affects semantics. The crossattention variant (Figure 6a in App. A.7.1) yields
high within-concept alignment but still shows offdiagonal similarities driven by shared prompt templates and linguistic structure. In contrast, the nocontext variant (Figure 6b in A.7.1), conditioning
on steering prompt only, produces much weaker offdiagonal alignment. We find that cross-attention’s
residual inter-concept similarity is weakened by
this additional conditioning, but not at the cost of
steering performance. Initial experiments to determine if geometric structure emerges among steering vectors sharing a concept yielded a negative.
This is likely due to high semantic similarity of the
prompts used in our evaluation pipeline.


**6** **Conclusion**


Both held-in and held-out evaluations indicate
that HYPERSTEER is a scalable and effective approach for steering language models. In particular, HYPERSTEER (Cross Attention), our bestperforming variant, achieves significantly stronger
performance on held-out prompts—improving further with dataset scale. It also outperforms all activation steering baselines on held-in evaluations.
Without modifying model parameters, our method
narrows the performance gap with fine-tuning and
prompting. Finally, we demonstrate that HYPERSTEER becomes increasingly compute-efficient as
data scale increases, achieving the same held-out
loss with fewer training updates.


**7** **Limitations**


**Data** A key limitation of our approach is the limited scope and quantity of the concept datasets.
Using data with concepts of much greater complexity and difficulty from a model steering perspective
would likely improve model performance and help
make evaluation more robust. We also note that
quality and robustness of concepts is bounded by
the GemmaScope feature labels used to derive them,
and collecting data from humans or other high quality sources is a feasible alternative. This is a key
research priority we emphasize for future work.


**Steering Sites** All experiments in our work are
limited to intervening on the _residual stream_ activations of the base LM. There are other potentially
more performant sites for intervention, including
various points of the decoder block and during the
attention computation. We also adopt the convention of prior work to intervene at all token positions;
exploring more targeted interventions could reduce
detrimental off-target steering effects and improve
the overall steering score.


**Compute** Compared to supervised dictionary
learning, the compute requirements of training a
hypernetwork are large, as the number of trainable
parameters significantly exceeds a ReFT-r1.


**Model Scale** Due to to compute constraints we
only experimented with Gemma-2-2B architectures, which are worse instruction followers and
in-context learners than the leading open source
models with many more parameters. Training on
models at a variety of scale would help cement HY
PERSTEER ’s strong steering performance against
the improved in-context learning ability of larger
LMs.


**Open** **Source** **Models** Our approach requires
white-box access to a model’s internals in order
to use steering vectors, a limitation prompting does
not encounter. Hence, we rely on the existence of
sufficiently capable open source models as a basis
for our research.


**8** **Ethical Considerations**


We present this work with the intention that HY
PERSTEER is a powerful tool for steering models
away from producing harmful responses and better tailor outputs to downstream tasks. However,
we acknowledge that model steering can also be



used by bad actors as a tool to circumvent a target models’s existing safety mechanisms or bias
models towards misleading outputs or malicious
persuasion. Hence, HYPERSTEER and hence steering vectors should be used responsibly and audited
to prevent such issues from arising, and having
a human-in-the-loop system could help mitigate
some of these concerns.


**9** **Acknowledgments**


**AI Usage** We use closed-source LLMs from OpenAI as a critical part of our work: synthetic concept data generation and evaluation pipelines utilize
gpt-4o-mini to generate ground truth labels and
judge responses according to criteria respectively.


**Other** This research was in part supported by a
grant from Open Philanthropy. We thank Aryaman
Arora, Róbert Csordás, and Qinan Yu for constant
and extremely helpful feedback during the discussion.


**References**


Trenton Bricken, Adly Templeton, Joshua Batson,
Brian Chen, Adam Jermyn, Tom Conerly, Nick
Turner, Cem Anil, Carson Denison, Amanda Askell,
Robert Lasenby, Yifan Wu, Shauna Kravec, Nicholas
Schiefer, Tim Maxwell, Nicholas Joseph, Zac
Hatfield-Dodds, Alex Tamkin, Karina Nguyen, and
6 others. 2023. Towards monosemanticity: Decomposing language models with dictionary learning.
_Transformer_ _Circuits_ _Thread_ . Https://transformercircuits.pub/2023/monosemanticfeatures/index.html.


Karl Cobbe, Vineet Kosaraju, Mohammad Bavarian,
Mark Chen, Heewoo Jun, Lukasz Kaiser, Matthias
Plappert, Jerry Tworek, Jacob Hilton, Reiichiro
Nakano, Christopher Hesse, and John Schulman.
2021. Training verifiers to solve math word problems. _arXiv preprint arXiv:2110.14168_ .


Mike Conover, Matt Hayes, Ankit Mathur, Jianwei Xie,
Jun Wan, Sam Shah, Ali Ghodsi, Patrick Wendell,
Matei Zaharia, and Reynold Xin. 2023. [Free dolly:](https://www.databricks.com/blog/2023/04/12/dolly-first-open-commercially-viable-instruction-tuned-llm)
[Introducing the world’s first truly open instruction-](https://www.databricks.com/blog/2023/04/12/dolly-first-open-commercially-viable-instruction-tuned-llm)
[tuned llm.](https://www.databricks.com/blog/2023/04/12/dolly-first-open-commercially-viable-instruction-tuned-llm)


Hoagy Cunningham, Aidan Ewart, Logan Riggs, Robert
Huben, and Lee Sharkey. 2023. [Sparse autoencoders](https://arxiv.org/abs/2309.08600)
[find highly interpretable features in language models.](https://arxiv.org/abs/2309.08600)
_Preprint_, arXiv:2309.08600.


Leo Gao, Tom Dupré la Tour, Henk Tillman, Gabriel
Goh, Rajan Troll, Alec Radford, Ilya Sutskever, Jan
Leike, and Jeffrey Wu. 2024. [Scaling and evaluating](https://arxiv.org/abs/2406.04093)
[sparse autoencoders.](https://arxiv.org/abs/2406.04093) _Preprint_, arXiv:2406.04093.


Mario Giulianelli, Jack Harding, Florian Mohnert,
Dieuwke Hupkes, and Willem H. Zuidema. 2018.
Under the hood: Using [diagnostic](https://doi.org/10.18653/V1/W18-5426) classifiers to investigate and improve [how](https://doi.org/10.18653/V1/W18-5426) language models track
[agreement information.](https://doi.org/10.18653/V1/W18-5426) In _Proceedings of the Work-_
_shop:_ _Analyzing and Interpreting Neural Networks_
_for NLP, BlackboxNLP EMNLP 2018, Brussels, Bel-_
_gium, November 1, 2018_, pages 240–248. Association for Computational Linguistics.


David Ha, Andrew Dai, and Quoc V. Le. 2016. [Hyper-](https://arxiv.org/abs/1609.09106)
[networks.](https://arxiv.org/abs/1609.09106) _Preprint_, arXiv:1609.09106.


Evan Hernandez, Sarah Schwettmann, David Bau,
Teona Bagashvili, Antonio Torralba, and Jacob Andreas. 2022. [Natural language descriptions of deep](https://openreview.net/forum?id=NudBMY-tzDr)
[visual features.](https://openreview.net/forum?id=NudBMY-tzDr) In _ICLR_ .


Edward J Hu, Yelong Shen, Phillip Wallis, Zeyuan
Allen-Zhu, Yuanzhi Li, Shean Wang, Lu Wang,
Weizhu Chen, and 1 others. 2022. Lora: Low-rank
adaptation of large language models. _ICLR_, 1(2):3.


Kenneth Li, Oam Patel, Fernanda Viégas, Hanspeter
Pfister, and Martin Wattenberg. 2023a. [Inference-](https://openreview.net/forum?id=aLLuYpn83y)
time intervention: [Eliciting truthful answers from a](https://openreview.net/forum?id=aLLuYpn83y)
[language](https://openreview.net/forum?id=aLLuYpn83y) model. In _Thirty-seventh_ _Conference_ _on_
_Neural Information Processing Systems_ .


Xuechen Li, Tianyi Zhang, Yann Dubois, Rohan Taori,
Ishaan Gulrajani, Carlos Guestrin, Percy Liang, and
Tatsunori B. Hashimoto. 2023b. Alpacaeval: An
automatic evaluator of instruction-following models.
[https://github.com/tatsu-lab/alpaca_eval.](https://github.com/tatsu-lab/alpaca_eval)


Tom Lieberum, Senthooran Rajamanoharan, Arthur
Conmy, Lewis Smith, Nicolas Sonnerat, Vikrant
Varma, János Kramár, Anca D. Dragan, Rohin Shah,
and Neel Nanda. 2024. [Gemma scope:](https://doi.org/10.48550/ARXIV.2408.05147) Open sparse
autoencoders [everywhere](https://doi.org/10.48550/ARXIV.2408.05147) all at once on gemma 2.
_CoRR_, abs/2408.05147.


Samuel Marks, Can Rager, Eric J Michaud, Yonatan Belinkov, David Bau, and Aaron Mueller. 2025. [Sparse](https://openreview.net/forum?id=I4e82CIDxv)
[feature circuits: Discovering and editing interpretable](https://openreview.net/forum?id=I4e82CIDxv)
[causal graphs in language models.](https://openreview.net/forum?id=I4e82CIDxv) In _The Thirteenth_
_International_ _Conference_ _on_ _Learning_ _Representa-_
_tions_ .


Samuel Marks and Max Tegmark. 2023. [The geometry](https://doi.org/10.48550/ARXIV.2310.06824)
of truth: [Emergent linear structure in large language](https://doi.org/10.48550/ARXIV.2310.06824)
[model representations of true/false datasets.](https://doi.org/10.48550/ARXIV.2310.06824) _CoRR_,
abs/2310.06824.


OpenAI, :, Aaron Hurst, Adam Lerer, Adam P. Goucher,
Adam Perelman, Aditya Ramesh, Aidan Clark,
AJ Ostrow, Akila Welihinda, Alan Hayes, Alec
Radford, Aleksander M ˛adry, Alex Baker-Whitcomb,
Alex Beutel, Alex Borzunov, Alex Carney, Alex
Chow, Alex Kirillov, and 401 others. 2024. [Gpt-4o](https://arxiv.org/abs/2410.21276)
[system card.](https://arxiv.org/abs/2410.21276) _Preprint_, arXiv:2410.21276.


Jason Phang, Yi Mao, Pengcheng He, and Weizhu Chen.
2023. [HyperTuning: Toward adapting large language](https://proceedings.mlr.press/v202/phang23a.html)
models without [back-propagation.](https://proceedings.mlr.press/v202/phang23a.html) In _Proceedings_
_of_ _the_ _40th_ _International_ _Conference_ _on_ _Machine_



_Learning_, volume 202 of _Proceedings_ _of_ _Machine_
_Learning Research_, pages 27854–27875. PMLR.


Nina Rimsky, Nick Gabrieli, Julian Schulz, Meg Tong,
Evan Hubinger, and Alexander Turner. 2024. [Steer-](https://doi.org/10.18653/v1/2024.acl-long.828)
ing llama 2 via [contrastive](https://doi.org/10.18653/v1/2024.acl-long.828) activation addition. In
_Proceedings of the 62nd Annual Meeting of the As-_
_sociation for Computational Linguistics (Volume 1:_
_Long Papers)_, pages 15504–15522, Bangkok, Thailand. Association for Computational Linguistics.


Morgane Rivière, Shreya Pathak, Pier Giuseppe
Sessa, Cassidy Hardin, Surya Bhupatiraju, Léonard
Hussenot, Thomas Mesnard, Bobak Shahriari,
Alexandre Ramé, Johan Ferret, Peter Liu, Pouya
Tafti, Abe Friesen, Michelle Casbon, Sabela Ramos,
Ravin Kumar, Charline Le Lan, Sammy Jerome, Anton Tsitsulin, and 80 others. 2024. [Gemma](https://doi.org/10.48550/ARXIV.2408.00118) 2: Improving open language [models](https://doi.org/10.48550/ARXIV.2408.00118) at a practical size.
_CoRR_, abs/2408.00118.


Jiuding Sun, Jing Huang, Sidharth Baskaran, Karel
D’Oosterlinck, Christopher Potts, Michael Sklar, and
Atticus Geiger. 2025. [HyperDAS: Towards automat-](https://openreview.net/forum?id=6fDjUoEQvm)
[ing mechanistic interpretability with hypernetworks.](https://openreview.net/forum?id=6fDjUoEQvm)
In _The Thirteenth International Conference on Learn-_
_ing Representations_ .


Alexander Matt Turner, Lisa Thiergart, David Udell,
Gavin Leech, Ulisse Mini, and Monte MacDiarmid.
2023. Activation addition: [Steering language models](https://doi.org/10.48550/ARXIV.2308.10248)
[without optimization.](https://doi.org/10.48550/ARXIV.2308.10248) _CoRR_, abs/2308.10248.


Laurens van der Maaten and Geoffrey Hinton. 2008.

Visualizing [data](http://jmlr.org/papers/v9/vandermaaten08a.html) using t-sne. _Journal_ _of_ _Machine_
_Learning Research_, 9(86):2579–2605.


Zhengxuan Wu, Aryaman Arora, Atticus Geiger, Zheng
Wang, Jing Huang, Dan Jurafsky, Christopher D.
Manning, and Christopher Potts. 2025. [AxBench:](https://arxiv.org/abs/2501.17148)
Steering llms? even [simple](https://arxiv.org/abs/2501.17148) baselines outperform
[sparse autoencoders.](https://arxiv.org/abs/2501.17148) _Preprint_, arXiv:2501.17148.


Zhengxuan Wu, Aryaman Arora, Zheng Wang, Atticus
Geiger, Dan Jurafsky, Christopher D Manning, and
Christopher Potts. 2024a. [ReFT: Representation fine-](https://openreview.net/forum?id=fykjplMc0V)
tuning for [language](https://openreview.net/forum?id=fykjplMc0V) models. In _The_ _Thirty-eighth_
_Annual Conference on Neural Information Process-_
_ing Systems_ .


Zhengxuan Wu, Atticus Geiger, Aryaman Arora, Jing
Huang, Zheng Wang, Noah Goodman, Christopher
Manning, and Christopher Potts. 2024b. [pyvene:](https://aclanthology.org/2024.naacl-demo.16)
[A library for understanding and improving PyTorch](https://aclanthology.org/2024.naacl-demo.16)
[models via interventions.](https://aclanthology.org/2024.naacl-demo.16) In _Proceedings of the 2024_
_Conference_ _of_ _the_ _North_ _American_ _Chapter_ _of_ _the_
_Association for Computational Linguistics:_ _Human_
_Language Technologies (Volume 3:_ _System Demon-_
_strations)_, pages 158–165, Mexico City, Mexico. Association for Computational Linguistics.


**A** **Appendix**


**A.1** **Future Directions**


**Large-scale** **concept** **data** Prior works (Phang
et al., 2023) explore pre-training the architecture


prior to using task-specific data. Since HYPERSTEER uses a pre-trained model as a starting point,
we postulate that sourcing significantly more data
with more concepts of varying and complexity
would allow us to test the architecture’s limits.


**Generating other parameter types** Due to compute constraints and our focus on activation steering, we did not explore generating other types of
parameter-efficient modulations, including rank- _r_
generalizations such as ReFT (Wu et al., 2024a)
or LoRA (Hu et al., 2022) adapters. Such generalizations could potentially be more expressive and
allow the hypernetwork to adapt language models
to more difficult tasks.


**Architecture** **optimizations** HYPERSTEER
(Cross Attention) is a parameter-dense transformer
model itself. More efficient alternatives could
bridge the gap with the dictionary learning baseline
and scale up the approach given a limited compute
budget.


**A.2** **Hyperparameter Details**


For the ReFT-r1 baseline, we use the default hyperparameters and settings from AXBENCH. We
reduce the number of layer for the cross attention
variant to match the total number of parameter with
the cross-attention model.


**Hyperparameters** _**Cross Attention**_ _**Other variants**_


Gemma-2-2b
Batch size 12 6
LR 8e-5 8e-5
N epoch 3 3
Layer 22 26
Cross-attention heads 8  

Gemma-2-9b
Batch size 4 6
LR 5e-6 5e-6
N epoch 3 3
Layer 34 42
Cross-attention heads 8  

Table 3: Hyperparameter settings for each variant. For
all the unmentioned details such as hidden dimension
we use the default configuration of Gemma-2-2b and
Gemma-2-9b.


**A.3** **Cross-Attention Architecture Details**


A token sequence _s_ of length _|s|_ representing
the concept for steering is encoded as **h** 0 =
EmbΦ( **x** ) _∈_ R _[|][s][|×][d]_ . For clarity, we refer to this
as the zeroth layer of the residual stream for the
hypernetwork _H_ Φ.



This precedes _N_ decoder blocks. Each block
contains the standard multi-headed self-attention
(MHA) feed-forward layer (FFN), and a multiheaded cross-attention module to include information from LMbase. Let **S** _∈_ R _[|][s][|×][d]_ and **X** [(] _[p][−]_ [1)] _∈_
R _[|][s][|×][d]_ be the incoming residual stream. In the _p_ -th
block, we compute:


**X** [(] _[p]_ [)] := MHA� **Q** = **X** [(] **[p]** _[−]_ **[1]** [)] _,_ **K** = **X** [(] **[p]** _[−]_ **[1]** [)] _,_

**V** = **X** [(] **[p]** _[−]_ **[1]** [)][�] _,_

**X** [(] _[p]_ [)] := MHA� **Q** = **S** _,_ **K** = **X** [(] **[p]** [)] _,_

**V** = **X** [(] _[p]_ [)][�] _,_


        **X** [(] _[p]_ [)] := LayerNorm **X** [(] _[p][−]_ [1)] + FFN� **X** [(] _[p]_ [)][��] _._


We initialize the self-attention MHA blocks from
the pre-trained Gemma-2 base model and the cross
attention blocks according to the default PyTorch
weight initialization scheme.


**A.3.1** **Model Size**


Our largest HYPERSTEER (cross attention) architecture has 22 modified decoder blocks, and
has _≈_ 0 _._ 998 times the parameters as Gemma-2-2B,
which has 26 standard decoder blocks. Each cross
attention decoder block has _≈_ 1 _._ 18 times as many
parameters as a standard Gemma-2-2B decoder
block.


**A.3.2** **Detailed TFLOPs Analysis**


We demonstrate that the number of TFLOPs to
reach optimal steering performance decays with
the number of concepts in the dataset, or steering
prompts used. Thus, as we scale up steering data
HYPERSTEER becomes an efficient and superior
alternative to the supervised dictionary learning
baseline for steering language models. We focus
our best method, the cross attention architecture,
for this analysis.
Let _F_ ReFT _≈_ 666 _._ 27 _±_ 20 _._ 74 be the TFLOPs
required to train a single ReFT-r1 steering vector,
and _L_ [¯] _[⋆]_ joint [be the average optimal evaluation loss]
for computed on Concept10. We average over 5
different random seeds as well to obtain this constant. To train HYPERSTEER (cross attention) we
construct datasets _D_ ( _c_ ) of varying number of concepts (steering prompts) selected in the interval
_c ∈_ [10 _,_ 16000]. Concept10 is _held-in_ with respect
to _D_ ( _c_ ). We train HYPERSTEER on each _D_ ( _c_ )
until the eval loss on Concept10 reaches _L_ [¯] _[⋆]_ joint [.]
The TFLOPs per concept _FD_ ( _c_ ) for a dataset _D_ ( _c_ ),
where _N_ _[∗]_ gradient steps are taken until _L_ [¯] _[⋆]_ joint [is]


achieved is computed with the following formula:


_[F]_ [¯][step]
_FD_ ( _c_ ) = _[N]_ _[∗]_ _[·]_ _._ (5)

_c_

_F_ ¯step is the average TFLOPs per training step for
HYPERSTEER, a local per-training-run statistic
with low variance given that the distribution of sequence lengths of both input prompts and steering prompts across examples is observed to be
largely uniform. The number of layers is selected
to match the total number of parameters with the
target model.
We also fit a simple curve to approximate
_FD_ ( _c_ ), and find that an equation of the form
_f_ ( _c_ ) = _a_ + _b_ _·_ exp( _dc_ ) best fits the curve with
_a_ = 87 _._ 7035 _, b_ = 1521 _._ 1495 _, c_ = _−_ 0 _._ 0034 and
_R_ [2] = 0 _._ 9976. Clearly, lim _c→∞_ _f_ ( _c_ ) = _a_ and
_a < F_ ReFT, showing that HYPERSTEER is more
compute efficient to train when scaling up steering
tasks.


**A.4** **Details on Training Objective**


ReFT-r1 jointly optimizes for steering via causal
language modeling loss and concept detection by
selecting the top- _k_ sequence-level activations.


_L_ joint(LM _θ_ ) = (6)



_T_


log _Pθ_ ( _yt_ _|_ **x** _, y<t_ )

_t_ =1



E( **x** _,_ **y** ) _∼D_





_−_



**A.5** **Concept Dataset Details**


**Negative samples** AXBENCH uses negative examples to enable training and evaluation for concept detection. Since our work only focuses on
steering models and not concept detection, we discard this objective and omit negative examples in
training and evaluation data for all HYPERSTEER
variants. We note that the no-context reconstruction variant indirectly uses these negative samples,
for ground truth steering vectors ∆ _[∗]_ _s_ [were trained]
using the joint objective (7).


**Data Ratio** For all training datasets, the ratio of
base prompts to steering prompts is 72 : 1. During
evaluation, the ratio of base prompts to steering
prompts is 10 : 1. We keep these parameters consistent with AXBENCH save for the lack of negative
examples.


**Base prompt data distributions** Training base
prompts are sampled from a diverse instruction
pool of three genres: code, text, and math. The
open source datasets Dolly-15K (Conover et al.,
2023) and GSM8K (Cobbe et al., 2021) comprise
the instruction data in this pool. We point readers to Sec. I of the AXBENCH appendix for further details. Labels for training data are generated
from gpt-4o-mini. For evaluation base prompts,
we use sample instructions from AlpacaEval (Li
et al., 2023b) to ensure fairness. These settings and
choices are again identical to those of AXBENCH.


**A.6** **Baseline details**


We use prompting, fine-tuning, and activation steering baseliens from AXBENCH. The core comparisons however


**Supervised Dictionary Learning** ReFT-r1 is a
method proposed by AXBENCH (Wu et al., 2025)
to jointly perform the task of concept detection and
concept steering using a weakly supervised objective (7). At training time, we train one ReFT-r1 per
concept/steering prompt to populate a dictionary
of atoms, with each atom being a learned steering
vector.
At training time, the latent is computed from the
similarity between the hidden states of the modele
model and the learned steering vector:


Ψ [ReFT-r1] Detect [(] _[h][i]_ [) = ReLU(] _[h][i]_ _[·]_ **[ w]** [ReFT-r1][)] (9)


This latent is then inferred on the evaluation set




  + _λ_ _∥ai∥_ 1


_ai /∈_ TopK(Ψ( **h** ))




_._ (7)



Here,


Ψ( _hi_ ) = ReLU( _hi ·_ **w** ReFT-R1) _∈_ R _[d][×]_ [1] (8)


is a sequence-level concept detection latent. This
objective is also used in the regression and SFT
variants of HYPERSTEER, when the steering vector
is only conditioned on the concept.
Input-conditioned variants do not minimize an
additional concept detection loss term, hence do not
require an additional inference step to compute the
maximal activations on a per-concept basis. The
baseline ReFT-r1, end-to-end (no in-context learning), and regression variants require this additional
step, and the steering heads are modified to generate ∆ _s_ with unit norm. Input-conditioned methods
do not normalize ∆ _[x]_ _s_ [, eliminating this step.]
We note that the no-context reconstruction
method is trained on ground truth labels that do
utilize _L_ joint, hence evaluation on the regression
method requires this additional inference step.


**Short Description** **Full Description**


Structured Data Entries specific identifiers or entries
in a structured data format
Personal Identity References references to personal possessions and identity
Time References instances of specific time references or moments within
the text
Java Interface References references to Java interfaces
and their implementations
Legal Terminology references to legal terminology and concepts related to
law and justice
Mathematical Notation key phrases related to personal aspirations and career
transitions
Proper Nouns occurrences of mathematical
symbols or notation
Employment Contract Terms proper nouns and names
Object Specifications phrases related to employment contracts and compensation specifics
Other references to measurements,
specifications, and characteristics of objects


Table 4: Mapping of short concept descriptors to their
full labels in held-out Concept10.


to determine the final magnitude of the steering
vector for each concept at test time:



60


40


20


0


20


40


60



Concept

Structured Data Entries

Personal Identity Refere

Time References

Java Interface Referenc

Legal Terminology

Mathematical Notation

Proper Nouns

Employment Contract T

Object Specifications

Other



40 20 0 20 40 60
t-SNE 1


Figure 4: Concept10 t-SNE analysis of 2500 steering
vectors from HYPERSTEER (cross attention), 250 per
concept.



100


50


0


50


100



Concept

Structured Data Entries

Personal Identity Refere

Time References

Java Interface Referenc

Legal Terminology

Mathematical Notation

Proper Nouns

Employment Contract T

Object Specifications

Other



150 100 50 0 50 100 150 200
PC 1


Figure 5: Concept10 PCA analysis (2 components)
2500 steering vectors from HYPERSTEER (cross attention), 250 per concept.


cross-attention heatmaps across layers and heads
( _N_ = 20 layers).

A key takeaway is that all query (concept) tokens all tend to attend to the same or a few select
keys/values (input prompt) tokens with high mass.
This trend remains consistent across cross-attention
modules from layers 0-19 (9, 11, 12). Each crossattention module has 8 heads.


**A.7.3** **Data Distribution**


A potential issue with our dataset are the
use of ground truth labels samples from a
stronger “teacher model” gpt-4o-mini, whereas
Gemma-2-2B is a weaker “student” model we seek
to adapt. This is evidenced by the right-skewed distribution (see 7 for perplexities computed from base
LM when conditioned on the gpt-4o-mini output distribution. The perplexity distribution from
Gemma-2-2B outputs (8) comprises a much smaller
range in comparison.




  - 1
∆ _[x]_ _s_ [=]
_k_



��Top-k(ΨReFT-r1Detect [(] **[h]** [))] ��1




**w** ReFT-r1


(10)



**Prompt steering** This is a strong baseline which
is shown in AXBENCH to outperform other steering methods and does not require training. For a
given steering prompt _s_, gpt-4o-mini is used to
enhance _s →_ _s_ _[′]_ by explicitly instructing the model
to include the concept in its response, which is
pre-pended to a base prompt _x_ . We sample steered
generations from the target LM using this enhanced
prompt _s_ _[′]_ _⊕_ _x_ .


**A.7** **Additional Experiments**


**A.7.1** **Geometric structure using**
**dimensionality reduction**

We also analyze the structure of our high dimensional steering vectors on a held-out evaluation set
of steering prompts


**A.7.2** **Attention Heatmaps**

To better understand the interaction between the
base prompt _x_ and the steering prompt _s_ in the
In Context and Cross Attention HYPERSTEER
architectures, we analyze the self-attention and


Structured Data Entries


Personal Identity References


Time References


Java Interface References


Legal Terminology


Mathematical Notation


Proper Nouns


Employment Contract Terms


Object Specifications


Other





Structured Data Entries


Personal Identity References


Time References


Java Interface References


Legal Terminology


Mathematical Notation


Proper Nouns


Employment Contract Terms


Object Specifications


Other




|0.84|0.43|0.48|0.46|0.44|0.42|0.54|0.53|0.47|0.52|
|---|---|---|---|---|---|---|---|---|---|
|0.43|0.85|0.65|0.64|0.65|0.70|0.53|0.63|0.65|0.62|
|0.48|0.65|0.82|0.62|0.60|0.64|0.54|0.66|0.61|0.65|
|0.46|0.64|0.62|0.84|0.68|0.64|0.56|0.60|0.67|0.63|
|0.44|0.65|0.60|0.68|0.85|0.64|0.54|0.58|0.71|0.64|
|0.42|0.70|0.64|0.64|0.64|0.85|0.51|0.59|0.67|0.59|
|0.54|0.53|0.54|0.56|0.54|0.51|0.82|0.57|0.53|0.56|
|0.53|0.63|0.66|0.60|0.58|0.59|0.57|0.79|0.59|0.63|
|0.47|0.65|0.61|0.67|0.71|0.67|0.53|0.59|0.85|0.66|
|0.52|0.62|0.65|0.63|0.64|0.59|0.56|0.63|0.66|0.81|


|1.00|0.33|0.13|0.33|0.34|0.25|0.33|0.34|0.30|0.31|
|---|---|---|---|---|---|---|---|---|---|
|0.33|1.00|0.13|0.46|0.38|0.37|0.38|0.59|0.33|0.27|
|0.13|0.13|1.00|0.14|0.09|0.08|0.14|0.13|0.13|0.09|
|0.33|0.46|0.14|1.00|0.32|0.25|0.30|0.34|0.33|0.23|
|0.34|0.38|0.09|0.32|1.00|0.25|0.28|0.37|0.27|0.30|
|0.25|0.37|0.08|0.25|0.25|1.00|0.27|0.39|0.26|0.25|
|0.33|0.38|0.14|0.30|0.28|0.27|1.00|0.50|0.37|0.35|
|0.34|0.59|0.13|0.34|0.37|0.39|0.50|1.00|0.41|0.37|
|0.30|0.33|0.13|0.33|0.27|0.26|0.37|0.41|1.00|0.33|
|0.31|0.27|0.09|0.23|0.30|0.25|0.35|0.37|0.33|1.00|



(a) HYPERSTEER (cross attention)



(b) HYPERSTEER (no context)



Figure 6: Pairwise cosine similarities of steering vectors, averaged within each steering prompt, for our two
HYPERSTEER variants. (a) **Cross-attention** : strong on-diagonal (same steering prompt) alignment with some
off-diagonal variance due to prompt conditioning. (b) **No-context** : generally weaker off-diagonal alignment. We
hypothesize that cross-attention’s higher off-diagonal similarity arises from shared semantic and linguistic structure
across prompts even when steering prompt labels differ.



35


30


25


20


15


10


5


0



|Col1|Col2|Col3|Col4|Col5|Col6|Col7|Col8|Col9|Col10|Col11|Col12|Col13|Col14|Col15|Col16|Col17|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
||||||||||||||||||
||||||||||||||||||
||||||||||||||||||
||||||||||||||||||
||||||||||||||||||
||||||||||||||||||
||||||||||||||||||
||||||||||||||||||
||||||||||||||||||
||||||||||||||||||
||||||||||||||||||
||||||||||||||||||
||||||||||||||||||


Perplexity (clipped at 200)



|Col1|Col2|Col3|Col4|Col5|Col6|Col7|Col8|Col9|Col10|Col11|Col12|Col13|Col14|Col15|Col16|Col17|Col18|Col19|Col20|Col21|Col22|Col23|Col24|Col25|Col26|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|||||||||||||||||||||||||||
|||||||||||||||||||||||||||
|||||||||||||||||||||||||||
|||||||||||||||||||||||||||
|||||||||||||||||||||||||||
|||||||||||||||||||||||||||
|||||||||||||||||||||||||||


Perplexity



8


6


4


2


0



Figure 7: Concept10 perplexity distribution on data
labels sampled from gpt-4o-mini.


We ran preliminary experiments by training on
labels from both distributions, and find steering
performance is still better with the gpt-4o-mini
labels. We suspect that this could be a result of
either lower quality of Gemma-2-2B responses due
prompt-engineering being the method of generation or the LLM-as-a-judge evaluation setup (which
also uses gpt-4o-mini) being biased towards outputs from the same model.


**A.8** **Sample generations**


We use the best cross attention model for steering
and the steering factor that yields the best aggregate



Figure 8: Concept10 perplexity distribution won data
labels sampled from Gemma-2-2B.


score during evaluation. We also include responses
from a prompt steered baseline for comparison.
Generation is done with temperature of 1.0 and
with multinomial sampling, following AXBENCH.
See example generations 13, 14, 15, 16, 17, 18, 19,
20, 21, 22.


Figure 9: Layer 0 attention map.


Figure 10: Layer 5 attention map.



Figure 11: Layer 10 attention map.


Figure 12: Layer 19 attention map.


Figure 13: Successful steering and instruction following by HYPERSTEER.







Figure 14: Successful steering and instruction following by HYPERSTEER.







Figure 15: Successful steering and instruction following by HYPERSTEER.


Figure 16: Successful steering and instruction following by HYPERSTEER.







Figure 17: Successful steering and instruction following by HYPERSTEER.







Figure 18: Failed steering by HYPERSTEER, but successful instruction following.


Figure 19: Failed steering and instruction following by HYPERSTEER.







Figure 20: Failed steering by HYPERSTEER.







Figure 21: Somewhat successful steering by HYPERSTEER, but failed to follow the instruction.


Figure 22: Failed steering by HYPERSTEER, but successful instruction following.


