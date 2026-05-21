### **1 Introduction**

Large Language Models (LLMs) have demonstrated near-human or even superhuman intellectual capabilities (Brown
et al., 2020; Ouyang et al., 2022; OpenAI et al., 2024). Yet despite these successes, they sometimes fail in striking
ways. A central failure mode is hallucination: the tendency to confidently generate false or unsupported information.
Hallucinations undermine trust and restrict the safe deployment of LLMs in real-world settings where factual reliability
is critical (Rawte et al., 2023; Gekhman et al., 2024a; Shen et al., 2025a).


Recent interpretability studies—using sparse autoencoder (SAE) features (Templeton et al., 2024) or residual stream
activations (Rimsky et al., 2024; Turner et al., 2024)—have revealed that LLMs encode a form of self-knowledge.
Specifically, the activations associated with known versus unknown knowledge can be separated along linear directions
(Ji et al., 2025; Ferrando et al., 2025). Moreover, steering these representations reduces overconfidence and enables
models to acknowledge uncertainty. However, prior work primarily focuses on inference-time interventions, leaving a
significant gap in their practicality as part of scalable alignment pipelines.


If LLMs’ internal states already reflect what is known versus unknown, why do they still produce confident but false
answers? We hypothesize that a key cause lies in the training and evaluation paradigm of LLMs (Li et al., 2025a;
Kalai et al., 2025). During pretraining, the language modeling objective rewards predicting the next token given the
training corpus distribution, incentivizing plausible continuations even under uncertainty rather than expressions of
ignorance. Post-training further amplifies this tendency: the training and evaluation framework optimizes models to be
good test-takers, rewarding guessing over acknowledging uncertainty (Gekhman et al., 2024b).


1


**Figure 1** **Overview of the CASAL algorithm.** (A) **Knowledge Probing** : CASAL starts by probing the model to figure out what
it knows vs doesn’t know. Multiple responses per query are sampled to classify queries as **known** ( _D_ **k** ) or **unknown** ( _D_ **u** ). (B)
**Steering** : Difference in means are computed to construct steering vectors ( **v** _u_ _[L][∗]_ and **v** _k_ _[L][∗]_ [).] [Target activations (] **[ t]** _[L]_ _u_ _[∗]_ and **t** _[L]_ _k_ _[∗]_ [) are]
obtained by adding these steering vectors to the residual stream activation. **Pre-CASAL Behavior** : Prior to training, the model
often hallucinates and produces incorrect answers for **unknown** queries. (C) **CASAL Training** : CASAL training is essentially
"amortized activation steering", where instead of repeatedly steering activations online, we train a small subnetwork (a single layer
NN) to approximate the steering solution offline. (D) **Post-CASAL Activations and Behavior** : After training, the model learns a
sharper representation with a clearer knowledge boundary. It maintains correct answers on **known** queries while abstaining from
answering **unknown** ones.


In this work, we propose an alternative training objective—one that leverages the model’s own internal representations to
align behavior with knowledge boundaries. Our core hypothesis is that if models are trained to **directly utilize their own**
**representations** of known and unknown, their generations will better reflect what they truly "know". Concretely, we
replace the standard cross-entropy loss with a local representation loss applied to residual stream activations. Whereas
cross-entropy loss provides a learning signal from _external_ supervision (the training corpus), representation loss provides
a learning signal from _within_ : model’s own hidden representation.


Importantly, CASAL is among the first approaches to _rely solely on a representation-level objective_ for training LLMs.
Prior studies such as RepE (Zou et al., 2025), ReFAT (Yu et al., 2025), and others (Yu et al., 2024a; Casademunt
et al., 2025; Chen et al., 2025b; Yousefpour et al., 2025) have explored representation-level fine-tuning, but all
employed representation losses as auxiliary signals alongside standard cross entropy loss. By contrast, **CASAL treats**
**representation loss as the only and the primary optimization objective**, directly teaching the model to utilize its
hidden representation.


Our approach connects insights from two fields: interpretability and amortized optimization. Amortized optimization
(Kingma and Welling, 2013; Rezende et al., 2014; Gershman and Goodman, 2014) is a paradigm where costly repeated
optimizations are replaced by training a parametric function that approximates the solution. CASAL instantiates this
idea by incorporating activation steering into training: **it "amortize" the activation steering process by training a**
**lightweight subnetwork** that learns to approximate the steering solution, embedding the knowledge boundary directly
into the model’s weights.


We highlight our main contributions as:


   - **Effective Algorithm** : Introducing a training method inspired by interpretability findings and amortized optimiza

2


**Algorithm 1** CASAL: Contrastive Activation Steering for Amortized Learning

**Require:** Dataset _D_ ; frozen model _M_ original with _l_ layers; target layer _L_ _[∗]_ ; steering strength _α_ ; training epochs _E_


**STEP 1:** **Knowledge boundary probing** **known / unknown**
1: Set _k_ = 10, threshold _τ_ = 7
2: **for** _x ∈D_ **do**

3: Sample _k_ responses _{y_ [(] _[i]_ [)] ( _x_ ) _}_ ; _s_ ( _x_ ) = [�] _i_ **[1]** [[] _[y]_ [(] _[i]_ [)][(] _[x]_ [)][ correct][]]

4: **if** _s_ ( _x_ ) _≥_ _τ_ **then** _D_ k _←D_ k _∪{x}_ _▷_ "known" set _D_ k
5: **else if** _k −_ _s_ ( _x_ ) _≥_ _τ_ **then** _D_ u _←D_ u _∪{x}_ _▷_ "unknown" set _D_ u
6: **end if**
7: **end for**



**STEP 2:** **Steering**
_Note:_ **a** _[L][∗]_ ( _x_ ) denotes residual activations at layer _L_ _[∗]_ for input _x_
8: **¯a** _[L]_ u _[∗]_ = _|D_ 1u _|_ - _x∈D_ u **[a]** _[L][∗]_ [(] _[x]_ [)] _[,]_ **¯a** _[L]_ k _[∗]_ = _|D_ 1k _|_ - _x∈D_ k **[a]** _[L][∗]_ [(] _[x]_ [)]



_x∈D_ u **[a]** _[L][∗]_ [(] _[x]_ [)] _[,]_ **¯a** _[L]_ k _[∗]_ = _|D_ 1k _|_ 


_x∈D_ k **[a]** _[L][∗]_ [(] _[x]_ [)] _▷_ mean activations



9: **v** u _[L][∗]_ = **¯a** _[L]_ u _[∗]_ _[−]_ **[¯a]** k _[L][∗]_ _[,]_ **v** k _[L][∗]_ = **¯a** _[L]_ k _[∗]_ _−_ **¯a** _[L]_ u _[∗]_ _▷_ steering vectors
10: **t** _[L]_ u _[∗]_ [(] _[x]_ [) =] **[ a]** _[L][∗]_ [(] _[x]_ [) +] _[ α][ ·]_ **[ v]** u _[L][∗]_ for _x ∈D_ u _▷_ "abstain when you don’t know"
11: **t** _[L]_ k _[∗]_ [(] _[x]_ [) =] **[ a]** _[L][∗]_ [(] _[x]_ [) +] _[ α][ ·]_ **[ v]** k _[L][∗]_ for _x ∈D_ k _▷_ "answer when you know"



**STEP 3:** **CASAL training**

12: Initialize one-layer network _M_ train with weight _W_ original _[L][∗]_ _▷_ one-layer fine-tuning
13: **for** _e_ = 1 _. . . E_ **do**
14: _L_ u = E _x∈D_ u _∥_ **t** _[L]_ u _[∗]_ [(] _[x]_ [)] _[ −]_ **[a]** _[L][∗]_ [(] _[x]_ [)] _[∥]_ [2] _▷_ "unknown" loss
15: _L_ k = E _x∈D_ k _∥_ **t** _[L]_ k _[∗]_ [(] _[x]_ [)] _[ −]_ **[a]** _[L][∗]_ [(] _[x]_ [)] _[∥]_ [2] _▷_ "known" loss
16: _L ←L_ u + _L_ k; update _M_ train weights by _∇L_

17: **end for**
18: _W_ CASAL _[L][∗]_ _[←]_ [trained weights from] _[ M]_ [train] _▷_ extract trained weights
19: _M_ CASAL _←_ _M_ original with _W_ original _[L][∗]_ [replaced by] _[ W][ L]_ CASAL _[∗]_ [at layer] _[ L][∗]_ _▷_ create output model
**Ensure:** Trained model _M_ CASAL with updated weights at layer _L_ _[∗]_


tion. CASAL enables models to admit ignorance for unknown questions, reducing hallucination rates by _∼_ 30% 40% across multiple short-form QA benchmarks.


   - **Efficiency Gains** : CASAL’s objective function enables local and lightweight parameter updates, delivering _∼_ **30x**
**higher compute efficiency (FLOPs per token)** and requires _∼_ **20x less training data** (with as little as _∼_ 640
training data) to achieve the same level of performance compared to LoRA-based SFT and DPO.


   - **Robust Generalization** : The trained model retains its general capabilities while avoiding excessive refusals. At
the same time, it successfully generalizes refusal behavior to unknown queries sampled from out-of-distribution
(OOD) data.


   - **Versatility** : CASAL training is modality-agnostic, effectively mitigating hallucination in both text-only and
**multimodal models** .


   - **Broad Applicability** : We present _the first_ ever steering-based training framework with _general_ applicability to
both **dense and Mixture-of-Experts (MoE) models.**

### **2 CASAL**


We now introduce our method, CASAL, which integrates insights from interpretability and amortized optimization to
build a lightweight, efficient training framework. The full pipeline is shown in Figure 1, summarized in Algorithm 1.
At a high level, CASAL can be understood as an instance of _amortized optimization_ : instead of repeatedly solving
the steering problem at inference time, we train a parametric subnetwork to approximate this solution once, thereby
"amortizing" the resource use of activation steering across all future queries. This perspective motivates the name:


3


**Figure 2** **CASAL is both sample efficient and compute efficient.** (A–B) CASAL achieves strong hallucination reduction with
orders-of-magnitude fewer training examples comparing to LoRA-based fine-tuning with SFT, DPO and GRPO. (C) CASAL is over
30 _×_ more compute-efficient than PEFT baselines such as LoRA. (D) Hallucination reduction after CASAL training correlates with
improved cluster separation between known and unknown queries, measured by silhouette score.


**C** ontrastive **A** ctivation **S** teering for **A** mortized **L** earning (CASAL). CASAL proceeds in three stages:


**2.1** **STEP 1:** **Knowledge Boundary Probing**


CASAL begins by probing the model to delineate its knowledge boundary. For each input _x ∈D_, we sample _k_ = 10
completions and compare them to ground-truth answers. For each question, if at least 7 generations are correct, _x_ is
labeled as known; if less than 3 are incorrect, it is labeled as unknown. This produces two subsets: _Dk_ and _Du_ . We
systematically evaluated different threshold values and found that hallucination reduction performance remains robust
across this range (Appendix I). We adopt a relatively strict threshold of _τ_ = 7 to ensure high-confidence separation: the
model abstains only on knowledge it does not possess, and responds only when it demonstrates consistent correctness.
This choice reduces ambiguous cases near the decision boundary. [1] We evaluate CASAL on three datasets: TriviaQA
(Joshi et al., 2017b), PopQA (Mallen et al., 2023b), and EntityQA (Ferrando et al., 2025). Dataset details provided in
Appendix G.1.


**2.2** **STEP 2:** **Steering**


Next, CASAL constructs contrastive steering vectors to obtain better knowledge boundaries (Rimsky et al., 2024; Turner
et al., 2024; Arditi et al., 2024). For each query _x_, we extract residual stream activations **a** _[L][∗]_ ( _x_ ) at a designated target
layer _L_ _[∗]_ from _the last token position of the question_ [2] . We then compute mean activations for known and unknown
subsets ( _a_ ¯ _[L]_ k _[∗]_ and ¯ _a_ _[L]_ u _[∗]_ [) and construct steering vectors by taking difference in means, resulting in two vectors:] **[v]** _u_ _[L][∗]_ for
abstaining when the model lacks knowledge, and **v** _k_ _[L][∗]_ for reinforcing correct answering when the model does know. The
steering vectors are then added to the residual stream activations, yielding target activations **t** _[L]_ _u_ _[∗]_ [and] **[ t]** _k_ _[L][∗]_ [.] [These target]
activations are cached and subsequently used to compute the representation loss in STEP 3. Further details for steering
and target layer selection procedures are included in Appendix C.


1Consistent with previous literature (Ferrando et al., 2025; Grattafiori et al., 2024), the knowledge probing step creates the known versus unknown
labels subsequently used for steering our training baseline methods such as SFT and DPO, and therefore does not introduce additional computational
cost specific to CASAL.
2By extracting activations from the last token position of the _question_, the steering vectors reflect properties of the question itself (whether it is
known or unknown to the model) rather than features of the _answer_ (whether the answer is correct or incorrect).


4


**2.3** **STEP 3:** **CASAL Training**

Finally, CASAL trains a lightweight **one-layer network** _M_ train, initialized with the weight _W_ original _[L][∗]_ [from layer] _[ L][∗]_ [of]
the original model. Using a mean squared error objective, CASAL minimizes the distance between current activation
**a** _[L][∗]_ ( _x_ ) and its corresponding target activation ( **t** _[L]_ _k_ _[∗]_ or **t** _[L]_ _u_ _[∗]_ [).] [After training, the learned weights] _[ W][ L]_ CASAL _[∗]_ [are extracted]
from _M_ train and substituted back into layer _L_ _[∗]_ of the original model, producing the final model _M_ CASAL. This process
embeds the knowledge boundary directly into the model weights, eliminating the need for repeated steering at inference.
**Importantly, this representation loss is the sole training objective**, not used as auxiliary loss with standard crossentropy. Because this loss is **local to layer** _L_ _[∗]_ (derived directly from residual activations at that layer), we only need
to train one single layer. This contrasts with cross-entropy loss, which requires a forward pass through all layers to
compute output probabilities. Even when updating only a single target layer with cross-entropy loss, the entire model
(with other layers frozen) must be deployed during the forward pass, adding much more computational cost compared
to training just the one-layer network _M_ train. We conducted systematic ablation studies (Appendix K) to examine
different fine-tuning strategies. Our results demonstrate that fine-tuning different submodules of the MLP layer yields
no statistically significant performance differences. Further details for the training process and hyperparameter research
are included in Appendix D and L.

### **3 CASAL is Effective and Efficient**


We evaluate CASAL against strong baselines including Supervised Fine-Tuning (SFT), Direct Preference Optimization
(DPO) and Group Relative Policy Optimization (GRPO), which represent the predominant fine-tuning approaches
deployed in production systems today (hyperparameters search and other training details are provided in Appendix M).
By demonstrating CASAL’s superiority over these widely-adopted techniques, we establish its practical applicability for
real-world deployment beyond toy settings.


**3.1** **Sample Efficiency**


We quantify hallucination reduction performance primarily using the _hallucination rate_, which captures the fraction of
unknown queries incorrectly attempted by the model. Figure 2 summarizes our key findings, with additional details
on the hallucination rate metric provided in Appendix H.2. CASAL achieves substantially lower hallucination rates
across a wide range of training set sizes. When trained on just 640 examples, CASAL already matches or surpasses the
performance of SFT, DPO and GRPO trained on 12 _,_ 800 examples (Figure 2A–B). This translates into more than **20** _×_
**higher data efficiency**, demonstrating that CASAL is especially practical in data-scarce settings.


**3.2** **Compute Efficiency**


Beyond sample efficiency, CASAL is also highly compute efficient. By updating only a lightweight sub-module within
a single transformer layer, CASAL is substantially more compute efficient than full fine-tuning or even LoRA-based
parameter-efficient fine-tuning (PEFT). As shown in Figure 2C, CASAL achieves lower hallucination rates while
requiring over **30** _×_ **fewer FLOPs per token** than LoRA during training, underscoring its practicality for large-scale
deployments.This efficiency stems from two key properties of CASAL’s loss function:


**Efficiency across model depth.** Because CASAL’s loss is local to layer _L_ _[∗]_, both forward and backward passes operate
exclusively within the single-layer network _M_ train. In contrast, methods using cross-entropy loss, even when updating
only a single layer with other layers frozen, must perform a forward pass through all layers end-to-end to compute
output probabilities and backpropagate gradients from the output back to the target layer. For example, when fine-tuning
layer 16 of a 32-layer model, cross-entropy-based methods require computations through 32 layers in the forward pass
and through 16 layers in the backward pass, while CASAL operates only on the target layer itself. This advantage scales
with model depth: the deeper the model, the greater CASAL’s computational savings.


**Efficiency across generation length.** CASAL computes loss at a single position—the last token of the question. In
contrast, SFT averages cross-entropy loss over _all tokens_ in the generated answer, while DPO computes log-probabilities
over _all tokens_ in both chosen and rejected responses. The computational cost thus scales with answer length for these
methods, whereas CASAL’s cost remains constant regardless of generation length. Longer answers make CASAL


5


increasingly cost-effective comparing to standard baselines. [3] Details of FLOPs calculations are included in Appendix N.


**3.3** **Learning Better Knowledge Boundaries**


By training with a local representation loss, CASAL encourages clearer separation between activations corresponding
to known and unknown queries. We compute Silhouette score as a measure of cluster separation. As shown in
Figure 2D, Silhouette scores ( H.4). increase as training progresses, and this separation is correlated with the reduction
in hallucination rate. The strong correspondence (logistic fit, _R_ [2] = 0 _._ 945) between representational separation and
behavioral outcomes indicates that CASAL’s effectiveness arises from more faithfully encoding and utilizing knowledge
boundaries. Consistent with our hypothesis, CASAL demonstrates the best cluster separation and the clearest boundary
between known and unknown queries compared to the other methods ( Figure 22, Appendix Q). This validates that by
directly training a local representation loss, CASAL effectively encourages a distinct separation between these activation
states.


**Methods** **Refusal Rate (** _↓_ **)** **Accuracy (** _↑_ **)**


**PopQA** **TriviaQA** **EntityQA** **PopQA** **TriviaQA** **EntityQA**


Baseline **18.19%** _±_ **3.01** 7.93% _±_ 1.14 8.94% _±_ 2.18 **91.08%** _±_ **2.23** **95.82%** _±_ **2.24** 88.59% _±_ 1.46


SFT 20.32% _±_ 1.09 10.01% _±_ 1.16 11.08% _±_ 1.24 82.89% _±_ 1.33 92.45% _±_ 1.29 85.75% _±_ 1.18
DPO 21.79% _±_ 1.11 14.37% _±_ 2.06 17.66% _±_ 2.14 90.25% _±_ 1.06 95.30% _±_ 0.96 89.84% _±_ 1.16
GRPO 17.48% _±_ 4.46 17.77% _±_ 3.82 16.67% _±_ 4.42 85.78% _±_ 4.36 91.67% _±_ 2.76 85.48% _±_ 3.52
CASAL 19.89% _±_ 1.15 **7.29%** _±_ **1.34** **6.84%** _±_ **1.23** 85.11% _±_ 1.88 95.34% _±_ 2.25 **89.90%** _±_ **0.99**


**Table 1** CASAL does not introduce over-refusal nor degrade performance for known queries. Refusal rate and accuracy across three
different QA datasets are measured.


**Methods** **Accuracy (** _↑_ **)** **Win rate (** _↑_ **)**


**MMLU** **GSM8K** **GPQA** **MT Bench**
**(General)** **(Math)** **(Reasoning)** **(Coherence)**


Baseline 68.01 _±_ 0.34 77.48 _±_ 1.15 **33.31** _±_ **0.34** 7.38 _±_ 0.06


SFT 67.90 _±_ 0.23 75.66 _±_ 1.18 32.82 _±_ 0.34 7.44 _±_ 0.13
DPO 68.03 _±_ 0.26 **78.16** _±_ **1.14** 31.43 _±_ 0.37 7.39 _±_ 0.15
GRPO 67.73 _±_ 0.38 76.66 _±_ 1.21 31.92 _±_ 0.22 7.44 _±_ 0.11
CASAL **68.04** _±_ **0.44** 77.02 _±_ 1.16 33.18 _±_ 0.34 **7.57** _±_ **0.08**


**Table 2** CASAL preserves general capability. Performances (higher is better) on general capability, math, reasoning and contextaware conversational ability in multi-turn dialogues are measured.

### **4 CASAL Preserves Model Capability**


An important requirement for any practically useful hallucination-reduction method is that it should not degrade a
model’s general capabilities nor induce excessive refusals on queries the model can correctly answer. We therefore
evaluate CASAL across both refusal behavior and broad capability benchmarks. Table 1 reports refusal rates on three
QA datasets. CASAL achieves the lowest refusal rates on TriviaQA (7.29%) and EntityQA (6.84%), while maintaining a
competitive rate on PopQA (19.89%). These results demonstrate that CASAL reduces hallucination on unknown queries
without over-penalizing the model into unnecessary refusals for known ones. We also evaluate against Contrastive
Activation Addition (CAA), a popular inference-time steering method (Rimsky et al., 2024). As summarized in Section E,
while CASAL achieves comparable hallucination rates to CAA on unknown queries, it maintains performance on known


3The FLOPs comparison reported in this work is measured _per token_ . This makes our estimate of CASAL’s computational advantage (30 _×_ fewer
FLOPs than LoRA) conservative. For tasks requiring longer generations, CASAL’s efficiency gains over SFT, DPO and GRPO would be substantially
greater.


6


**Dataset** **Methods** **Hallucination Rate (Unknown) (** _↓_ **)** **Refusal Rate (Known) (** _↓_ **)** **Accuracy (Known) (** _↑_ **)**


**Train** **Test** **Train** **Test** **Train** **Test**


TriviaQA **Wiki** **Web** **Wiki** **Web** **Wiki** **Web**
Baseline 48.20% _±_ 1.34 50.74% _±_ 1.12 9.06% _±_ 0.93 **7.93%** _±_ **2.02** **94.22%** _±_ **1.44** **95.82%** _±_ **1.22**


SFT 24.44% _±_ 1.65 35.44% _±_ 1.64 14.77% _±_ 1.52 15.10% _±_ 1.77 91.23% _±_ 0.54 90.26% _±_ 1.15
DPO 23.28% _±_ 1.02 33.77% _±_ 0.99 13.62% _±_ 1.08 16.33% _±_ 1.19 90.23% _±_ 1.09 88.13% _±_ 1.30
GRPO 22.33% _±_ 1.34 33.12% _±_ 1.88 15.99% _±_ 1.30 18.10% _±_ 1.09 88.83% _±_ 0.96 87.27% _±_ 1.03
CASAL **20.47%** _±_ **1.11** **32.42%** _±_ **1.29** **8.28%** _±_ **1.16** 11.69% _±_ 2.22 92.03% _±_ 0.82 90.08% _±_ 1.33


PopQA **Group 1** **Group 2** **Group 1** **Group 2** **Group 1** **Group 2**
Baseline 74.87% _±_ 2.92 74.35% _±_ 1.56 18.95% _±_ 1.39 **18.19%** _±_ **1.46** **90.84%** _±_ **1.51** **91.08%** _±_ **0.92**


SFT 22.77% _±_ 1.08 24.02% _±_ 1.11 14.04% _±_ 1.16 20.88% _±_ 1.09 85.01% _±_ 1.06 85.74% _±_ 1.60
DPO 21.08% _±_ 1.33 24.88% _±_ 0.99 14.99% _±_ 1.62 19.19% _±_ 1.55 84.66% _±_ 0.90 84.01% _±_ 1.11
GRPO 20.19% _±_ 1.05 24.22% _±_ 1.32 18.07% _±_ 1.02 21.10% _±_ 1.33 80.13% _±_ 0.31 80.98% _±_ 1.06
CASAL **22.48%** _±_ **1.45** **23.42%** _±_ **1.94** **13.97%** _±_ **1.78** 19.10% _±_ 1.30 85.23% _±_ 0.86 84.27% _±_ 1.99


**Table 3** CASAL learns a generalizable notion of known vs. unknown, and can transfer between data sources within TriviaQA and
generalize across groups within PopQA.


queries, whereas CAA degrades accuracy for questions the model could previously answer correctly. This finding
aligns with previous work (Durmus et al., 2024; Chen et al., 2025b) showing that inference-time steering can introduce
undesirable side effects.


We further assess models’ general capability, including MMLU (Hendrycks et al., 2021) for general knowledge, GSM8K
(Cobbe et al., 2021) for math reasoning, GPQA(Rein et al., 2023) for scientific reasoning, and MT-Bench (Zheng et al.,
2023) for coherence in multi-turn conversations. As shown in Table 2, CASAL performs on par with strong baselines
across all metrics. Beyond these quantitative measures, we provide raw model outputs in Appendix F to allow readers
to assess the natural flow and coherence of generated responses after CASAL training. These results demonstrate
that CASAL reduces hallucinations on unknown queries while avoiding over-refusal on known queries, all without
sacrificing general capability—a balance critical for practical deployment.

### **5 CASAL is OOD Generalizable**


Does CASAL capture a generalizable notion of what the model knows versus does not know beyond its training
distribution? We test its ability to generalize across both in-distribution and out-of-distribution (OOD) settings. We first
evaluate whether CASAL’s learned knowledge boundary transfers across different groups within the same dataset. As
shown in Table 3, CASAL trained on Wikipedia-style data generalizes effectively to web data, reducing hallucination
rate from 50.7% to 32.4% while maintaining high accuracy on known queries (92.0% vs. 95.8%). A similar trend
is observed on PopQA (Table 3), where CASAL substantially reduces hallucinations in both Group 1 and Group 2,
lowering test hallucination rates from 74.4% to 23.4%. These results indicate that CASAL does not simply memorize
steering directions but learns a transferable notion of known versus unknown knowledge that holds across diverse data
groups.


We next evaluate a stronger OOD setting: training CASAL on one dataset and testing it on a completely different one.
Specifically, CASAL is trained on TriviaQA and evaluated on EntityQA (Table 4). Remarkably, hallucination rate on
the unseen EntityQA dataset drops from 50.7% to 11.7%, while accuracy on known queries remains above 95%. This
demonstrates that CASAL’s learned representations extend beyond the training domain, capturing knowledge boundaries
that remain robust even under OOD transfer. Together, these results establish that CASAL generalizes well both across
sub-groups within a dataset and across entirely distinct datasets. This robustness highlights that CASAL is not merely
overfitting to a narrow training distribution but instead induces a broadly applicable mechanism for distinguishing known
from unknown queries.


7


**Methods** **Hallucination Rate (** _↓_ **)** **Refusal Rate (** _↓_ **)** **Accuracy (** _↑_ **)**


**Train** **Test** **Train** **Test** **Train** **Test**


**TriviaQA** **EntityQA** **TriviaQA** **EntityQA** **TriviaQA** **EntityQA**


Baseline 48.2% _±_ 1.33 50.74% _±_ 0.92 **9.06%** _±_ **1.22** **12.89%** _±_ **1.49** **94.22%** _±_ **0.93** **95.82%** _±_ **2.32**


SFT 30.63% _±_ 1.53 23.13% _±_ 1.66 21.16% _±_ 1.34 29.84% _±_ 1.40 88.80% _±_ 1.33 80.77% _±_ 1.05
DPO 20.63% _±_ 2.21 18.30% _±_ 1.45 13.89% _±_ 1.22 22.02% _±_ 1.29 92.91% _±_ 1.06 87.41% _±_ 1.22
GRPO **14.00%** _±_ **0.55** 12.83% _±_ 4.18 21.43% _±_ 4.10 17.25% _±_ 5.56 85.69% _±_ 8.75 85.24% _±_ 4.32
CASAL 18.23% _±_ 1.03 **11.72%** _±_ **1.66** 9.29% _±_ 1.48 13.82% _±_ 1.55 93.36% _±_ 1.47 95.77% _±_ 1.64


**Table 4** CASAL supports OOD generalization across different datasets. The model is trained on the TriviaQA dataset and tested on
EntityQA as an out-of-distribution setting.

### **6 CASAL is Modality and Architecture Agnostic**


**6.1** **CASAL Reduces Hallucination in Vision-Language Models**


We apply CASAL to a vision-language model: Qwen2.5-VL-7B-Instruct (Qwen et al., 2024) and perform training
on the WorldCuisines-VQA (Winata et al., 2024) dataset. Finally, we evaluate whether CASAL generalizes beyond
standard dense transformer architectures and text-only settings. CASAL reduces hallucination rate (Table 5) by 38.74%.
Importantly, accuracy on known queries is preserved. This confirms that CASAL’s mechanism for sharpening knowledge
boundaries is not tied to language-only models but extends naturally to multimodal models. Further details for training
vision-language models are provided in Appendix O.


**6.2** **CASAL Reduces Hallucination in Mixture-of-Experts Models**


MoE models pose a unique challenge since knowledge and uncertainty may be distributed across different experts.
We first ask "how are unknown versus known queries represented across experts?" Are certain experts specialized in
representing known and others specialized in unknown? Or are they co-represented in the same experts? We started
our investigation by visualizing the activations in different experts in the OLMoE model (Muennighoff et al., 2025).
As illustrated in Figure 3A, activations for known and unknown queries are mostly co-represented in the same experts.
Similar to dense model training, CASAL applies a local representation loss on the residual stream activations with
converging signal across all experts (Figure 3B). After training, residual stream activations show a much clearer boundary
between known and unknown queries (Figure 3C), which translates into significant improvements in hallucination
rates. Hallucination rate for unknown queries drops by 42.9%, while accuracy on known queries remains unchanged
(Figure 3D). Further details regarding the CASAL training for MoE models can be found in Appendix P. These
results demonstrate that CASAL effectively extends to MoE architectures without sacrificing accuracy. Together, these
results establish that CASAL is both _architecture-agnostic_ and _modality-agnostic_ . Whether applied to dense or MoE
transformers, or to text-only versus vision-language models, CASAL consistently reduces hallucination rates while
maintaining high accuracy and balanced refusal behavior. This broad applicability highlights CASAL’s potential as a
scalable, general-purpose alignment technique.

### **7 Related Work**


**7.1** **Hallucination Mitigation**


**Inference-time Intervention.** Steering-based approaches (Rimsky et al., 2024; Turner et al., 2024) for hallucination
reduction typically apply interventions during inference (Ferrando et al., 2025; Ji et al., 2025; Li et al., 2024; Park et al.,
2025). While effective, this requires solving a local optimization problem for every input (e.g., shifting activations
along a direction at every forward pass), introducing extra computational overhead during deployment to monitor and
intervene. In contrast, CASAL eliminates the need for per-instance intervention by directly baking the knowledge
boundaries into model parameters, enabling scalable deployment in production.


8


_What is this dish known as in_
_France?_


_Where is this place?_



**Methods** **WorldCuisines Dataset**


**Unknown** **Known**


**Hallucination Rate (** _↓_ **)** **Refusal Rate (** _↓_ **)** **Accuracy (** _↑_ **)**


Baseline 72.35% _±_ 1.77 **13.91%** _±_ **1.37** 76.72% _±_ 1.67


SFT 35.05% _±_ 2.87 24.33% _±_ 2.76 87.42% _±_ 1.66
DPO 36.44% _±_ 3.77 24.02% _±_ 2.11 86.66% _±_ 1.74
GRPO 35.19% _±_ 2.99 28.73% _±_ 2.73 80.18% _±_ 1.64
CASAL **33.34%** _±_ **3.13** 25.44% _±_ 2.91 **90.36%** _±_ **1.96**


**Methods** **Landmark Dataset**


**Unknown** **Known**


**Hallucination Rate (** _↓_ **)** **Refusal Rate (** _↓_ **)** **Accuracy (** _↑_ **)**


Baseline 75.78% _±_ 1.69 3.59% _±_ 0.73 90.80% _±_ 1.55


SFT 39.05% _±_ 4.07 2.64% _±_ 3.01 92.77% _±_ 1.42
DPO 35.99% _±_ 1.03 6.06% _±_ 1.44 94.11% _±_ 1.01
GRPO 35.44% _±_ 1.81 8.19% _±_ 1.09 90.75% _±_ 1.31
CASAL **31.25%** _±_ **8.32** **3.12%** _±_ **3.01** **99%** _±_ **0.03**



**Table** **5** **CASAL** **is** **modality** **agnostic.** It reduces hallucination in vision-language model on WorldCuisines-VQA (top) and
Landmark-VQA (bottom). Example question-image pairs from the two datasets are shown on the left.


**In-weight Learning.** A complementary body of work modifies model parameters to encourage calibrated abstention and
reduce hallucination. Early approaches train models to abstain from uncertain predictions via probabilistic calibration.
Others focus on eliciting explicit confidence estimates in conversational models (Chen et al., 2024; Mielke et al., 2022).
Concurrent work Chen et al. (2025b) proposes persona vector extraction, where finetuning steers models away from
undesired persona directions. CASAL differs in two key ways: (i) rather than steering _away_ from undesirable traits, we
explicitly steer _towards_ desirable representations; and (ii) CASAL presents an efficient training framework, yielding
_∼_ 30 _×_ higher compute efficiency than SOTA parameter-efficient finetuning methods such as LoRA.


**7.2** **Amortized Optimization, Activation Steering and Representation Learning**


**Amortized** **Optimization.** Amortized optimization (Kingma and Welling, 2013; Rezende et al., 2014; Gershman
and Goodman, 2014) is a widely used paradigm in which expensive, repeated optimization is replaced by training a
parametric function that approximates the solution. Despite its influence in areas such as variational inference, sparse
coding, gradient-based meta-learning and reinforcement learning (Amos, 2025; Chen et al., 2021), this perspective
has been explored less in the context of interpretability or alignment (Paulus et al., 2025). CASAL can be viewed as
_amortized activation steering_, where the resource intensive process of online steering is distilled into a lightweight
subnetwork trained offline and reused at inference.


**Activation Steering.** A line of work has focused on inference-time interventions, where steering vectors are applied
dynamically to control model behavior without modifying weights (Ji et al., 2025; Li et al., 2024). Within this paradigm,
a common approach to derive steering vectors is to construct sample pairs differing along a target concept and compute
their difference-in-means (Arditi et al., 2024). Alternative methods further fine-tune the steering vectors to enable more
effective behavior control with less side effect (Cao et al., 2024; Stickland et al., 2024; Parekh et al., 2025). Another line
of work leverages sparse autoencoders (SAEs) to uncover interpretable features in an unsupervised manner, which can
then serve as handles for steering interventions (Ferrando et al., 2025).


**Representation Learning.** A parallel line of work (Tian et al., 2025; Yu et al., 2024a; Chen et al., 2025b; Casademunt
et al., 2025) focuses on shaping internal representations during finetuning to suppress undesired behaviors. Early
methods include representation fine-tuning (ReFT), which encourages task-specific interventions on hidden states (Wu
et al., 2024), and representation engineering (RepE), which monitors and manipulates high-level cognitive phenomena


9


**Figure 3** **CASAL is architecture-agnostic.** It effectively reduces hallucination for OLMoE. (A) Visualization of MLP activations
from different experts in a MoE model before CASAL training. (B) CASAL applies a local representation loss on residual stream
activations. During training, weights are updated on only a lightweight sub-module across experts. (C) Residual stream activations
before and after CASAL training. (D) CASAL reduces hallucination rate on unknown queries while maintaining low refusal score
and high accuracy for known queries.


in LLMs (Zou et al., 2025). Other techniques explicitly control harmful states: Zou et al. (2024) introduce circuit
breakers to block dangerous representations, while Yu et al. (2025) perform directional ablation of refusal features to
maintain robustness under adversarial attacks. Similarly, Yousefpour et al. (2025) propose representation bending to
disrupt harmful latent features. For unlearning, Shen et al. (2025b) train models to redirect unlearning data into refusal
regions. Compared to these efforts, CASAL provides _the first_ general steering-based training framework that is broadly
applicable to **both dense and sparse (MoE) architectures** .

### **8 Conclusion and Limitations**


In this work, we introduced CASAL, a lightweight, effective, and broadly applicable method for reducing hallucinations
in large language models. By embedding knowledge boundaries directly into model weights, CASAL achieves
substantial reductions in hallucination without degrading general capabilities, while being markedly more computeand data-efficient than standard baselines. Beyond its empirical results, CASAL provides initial evidence a broader
principle: insights from interpretability can be distilled into training objectives that scale.


While CASAL shows strong effectiveness and efficiency, several limitations remain. First, although CASAL generalizes
across short-form QA datasets, modalities, and architectures, its effectiveness in reasoning models remains to be
systematically tested. Second, our evaluation focuses specifically on hallucinations in short-form QA tasks. Exploring
CASAL’s effectiveness in reducing hallucinations during long-form generations (Obeso et al., 2025) represents an
important direction for future research. Finally, one particularly exciting future direction is the integration of CASAL into
LLM-based agentic systems. As LLMs move toward becoming tool-using agents integrated into everyday workflows,
their reliability becomes critical—misplaced confidence can lead to cascading errors with tangible consequences.
While modern agents increasingly leverage external tools to address factual uncertainty, effective tool orchestration
fundamentally depends on the agent’s ability to recognize the boundaries of its own knowledge. CASAL’s mechanism
for sharpening these knowledge boundaries could therefore serve as a component for more reliable agentic systems,
enabling agents to make better decisions about when to respond directly versus when to invoke tools such as web search
or specialized knowledge bases.


10


### **References**

Brandon Amos. Tutorial on amortized optimization, 2025. [URL https://arxiv.org/abs/2202.00665.](https://arxiv.org/abs/2202.00665)


Andy Arditi, Oscar Obeso, Aaquib Syed, Daniel Paleka, Nina Panickssery, Wes Gurnee, and Neel Nanda. Refusal in language models
is mediated by a single direction, 2024. [URL https://arxiv.org/abs/2406.11717.](https://arxiv.org/abs/2406.11717)


Tom B. Brown, Benjamin Mann, Nick Ryder, Melanie Subbiah, Jared Kaplan, Prafulla Dhariwal, Arvind Neelakantan, Pranav Shyam,
Girish Sastry, Amanda Askell, Sandhini Agarwal, Ariel Herbert-Voss, Gretchen Krueger, Tom Henighan, Rewon Child, Aditya
Ramesh, Daniel M. Ziegler, Jeffrey Wu, Clemens Winter, Christopher Hesse, Mark Chen, Eric Sigler, Mateusz Litwin, Scott Gray,
Benjamin Chess, Jack Clark, Christopher Berner, Sam McCandlish, Alec Radford, Ilya Sutskever, and Dario Amodei. Language
models are few-shot learners, 2020. [URL https://arxiv.org/abs/2005.14165.](https://arxiv.org/abs/2005.14165)


Yuanpu Cao, Tianrong Zhang, Bochuan Cao, Ziyi Yin, Lu Lin, Fenglong Ma, and Jinghui Chen. Personalized steering of large
language models: Versatile steering vectors through bi-directional preference optimization. _Advances in Neural Information_
_Processing Systems_, 37:49519–49551, 2024.


Helena Casademunt, Caden Juang, Adam Karvonen, Samuel Marks, Senthooran Rajamanoharan, and Neel Nanda. Steering
out-of-distribution generalization with concept ablation fine-tuning, 2025. [URL https://arxiv.org/abs/2507.16795.](https://arxiv.org/abs/2507.16795)


Lida Chen, Zujie Liang, Xintao Wang, Jiaqing Liang, Yanghua Xiao, Feng Wei, Jinglei Chen, Zhenghong Hao, Bing Han, and
Wei Wang. Teaching large language models to express knowledge boundary from their own signals, 2024. URL [https:](https://arxiv.org/abs/2406.10881)
[//arxiv.org/abs/2406.10881.](https://arxiv.org/abs/2406.10881)


Lida Chen, Zujie Liang, Xintao Wang, Jiaqing Liang, Yanghua Xiao, Feng Wei, Jinglei Chen, Zhenghong Hao, Bing Han, and Wei
Wang. Teaching large language models to express knowledge boundary from their own signals. In Yuji Zhang, Canyu Chen, Sha
Li, Mor Geva, Chi Han, Xiaozhi Wang, Shangbin Feng, Silin Gao, Isabelle Augenstein, Mohit Bansal, Manling Li, and Heng
Ji, editors, _Proceedings of the 3rd Workshop on Towards Knowledgeable Foundation Models (KnowFM)_, pages 26–39, Vienna,
Austria, August 2025a. Association for Computational Linguistics. ISBN 979-8-89176-283-1. doi: 10.18653/v1/2025.knowllm-1.3.
[URL https://aclanthology.org/2025.knowllm-1.3/.](https://aclanthology.org/2025.knowllm-1.3/)


Runjin Chen, Andy Arditi, Henry Sleight, Owain Evans, and Jack Lindsey. Persona vectors: Monitoring and controlling character
traits in language models, 2025b. [URL https://arxiv.org/abs/2507.21509.](https://arxiv.org/abs/2507.21509)


Tianlong Chen, Xiaohan Chen, Wuyang Chen, Howard Heaton, Jialin Liu, Zhangyang Wang, and Wotao Yin. Learning to optimize:
A primer and a benchmark, 2021. [URL https://arxiv.org/abs/2103.12828.](https://arxiv.org/abs/2103.12828)


Karl Cobbe, Vineet Kosaraju, Mohammad Bavarian, Mark Chen, Heewoo Jun, Lukasz Kaiser, Matthias Plappert, Jerry Tworek, Jacob
Hilton, Reiichiro Nakano, Christopher Hesse, and John Schulman. Training verifiers to solve math word problems, 2021. URL
[https://arxiv.org/abs/2110.14168.](https://arxiv.org/abs/2110.14168)


Esin Durmus, Alex Tamkin, Jack Clark, Jerry Wei, Jonathan Marcus, Joshua Batson, Kunal Handa, Liane Lovitt, Meg Tong,
Miles McCain, Oliver Rausch, Saffron Huang, Sam Bowman, Stuart Ritchie, Tom Henighan, and Deep Ganguli. Evaluating feature steering: A case study in mitigating social biases, 2024. URL [https://anthropic.com/research/](https://anthropic.com/research/evaluating-feature-steering)
[evaluating-feature-steering.](https://anthropic.com/research/evaluating-feature-steering)


Javier Ferrando, Oscar Obeso, Senthooran Rajamanoharan, and Neel Nanda. Do i know this entity? knowledge awareness and
hallucinations in language models, 2025. [URL https://arxiv.org/abs/2411.14257.](https://arxiv.org/abs/2411.14257)


Zorik Gekhman, Gal Yona, Roee Aharoni, Matan Eyal, Amir Feder, Roi Reichart, and Jonathan Herzig. Does fine-tuning llms on new
knowledge encourage hallucinations? _arXiv preprint arXiv:2405.05904_, 2024a.


Zorik Gekhman, Gal Yona, Roee Aharoni, Matan Eyal, Amir Feder, Roi Reichart, and Jonathan Herzig. Does fine-tuning llms on new
knowledge encourage hallucinations?, 2024b. [URL https://arxiv.org/abs/2405.05904.](https://arxiv.org/abs/2405.05904)


Samuel J. Gershman and Noah D. Goodman. Amortized inference in probabilistic reasoning. _Cognitive Science_, 38(1):69–100, 2014.


Aaron Grattafiori, Abhimanyu Dubey, Abhinav Jauhri, Abhinav Pandey, Abhishek Kadian, Ahmad Al-Dahle, Aiesha Letman, Akhil
Mathur, Alan Schelten, Alex Vaughan, Amy Yang, Angela Fan, Anirudh Goyal, Anthony Hartshorn, Aobo Yang, Archi Mitra,
Archie Sravankumar, Artem Korenev, Arthur Hinsvark, Arun Rao, Aston Zhang, Aurelien Rodriguez, Austen Gregerson, Ava
Spataru, Baptiste Roziere, Bethany Biron, Binh Tang, Bobbie Chern, Charlotte Caucheteux, Chaya Nayak, Chloe Bi, Chris
Marra, Chris McConnell, Christian Keller, Christophe Touret, Chunyang Wu, Corinne Wong, Cristian Canton Ferrer, Cyrus
Nikolaidis, Damien Allonsius, Daniel Song, Danielle Pintz, Danny Livshits, Danny Wyatt, David Esiobu, Dhruv Choudhary,
Dhruv Mahajan, Diego Garcia-Olano, Diego Perino, Dieuwke Hupkes, Egor Lakomkin, Ehab AlBadawy, Elina Lobanova, Emily
Dinan, Eric Michael Smith, Filip Radenovic, Francisco Guzmán, Frank Zhang, Gabriel Synnaeve, Gabrielle Lee, Georgia Lewis
Anderson, Govind Thattai, Graeme Nail, Gregoire Mialon, Guan Pang, Guillem Cucurell, Hailey Nguyen, Hannah Korevaar,


11


Hu Xu, Hugo Touvron, Iliyan Zarov, Imanol Arrieta Ibarra, Isabel Kloumann, Ishan Misra, Ivan Evtimov, Jack Zhang, Jade Copet,
Jaewon Lee, Jan Geffert, Jana Vranes, Jason Park, Jay Mahadeokar, Jeet Shah, Jelmer van der Linde, Jennifer Billock, Jenny
Hong, Jenya Lee, Jeremy Fu, Jianfeng Chi, Jianyu Huang, Jiawen Liu, Jie Wang, Jiecao Yu, Joanna Bitton, Joe Spisak, Jongsoo
Park, Joseph Rocca, Joshua Johnstun, Joshua Saxe, Junteng Jia, Kalyan Vasuden Alwala, Karthik Prasad, Kartikeya Upasani,
Kate Plawiak, Ke Li, Kenneth Heafield, Kevin Stone, Khalid El-Arini, Krithika Iyer, Kshitiz Malik, Kuenley Chiu, Kunal Bhalla,
Kushal Lakhotia, Lauren Rantala-Yeary, Laurens van der Maaten, Lawrence Chen, Liang Tan, Liz Jenkins, Louis Martin, Lovish
Madaan, Lubo Malo, Lukas Blecher, Lukas Landzaat, Luke de Oliveira, Madeline Muzzi, Mahesh Pasupuleti, Mannat Singh,
Manohar Paluri, Marcin Kardas, Maria Tsimpoukelli, Mathew Oldham, Mathieu Rita, Maya Pavlova, Melanie Kambadur, Mike
Lewis, Min Si, Mitesh Kumar Singh, Mona Hassan, Naman Goyal, Narjes Torabi, Nikolay Bashlykov, Nikolay Bogoychev, Niladri
Chatterji, Ning Zhang, Olivier Duchenne, Onur Çelebi, Patrick Alrassy, Pengchuan Zhang, Pengwei Li, Petar Vasic, Peter Weng,
Prajjwal Bhargava, Pratik Dubal, Praveen Krishnan, Punit Singh Koura, Puxin Xu, Qing He, Qingxiao Dong, Ragavan Srinivasan,
Raj Ganapathy, Ramon Calderer, Ricardo Silveira Cabral, Robert Stojnic, Roberta Raileanu, Rohan Maheswari, Rohit Girdhar,
Rohit Patel, Romain Sauvestre, Ronnie Polidoro, Roshan Sumbaly, Ross Taylor, Ruan Silva, Rui Hou, Rui Wang, Saghar Hosseini,
Sahana Chennabasappa, Sanjay Singh, Sean Bell, Seohyun Sonia Kim, Sergey Edunov, Shaoliang Nie, Sharan Narang, Sharath
Raparthy, Sheng Shen, Shengye Wan, Shruti Bhosale, Shun Zhang, Simon Vandenhende, Soumya Batra, Spencer Whitman, Sten
Sootla, Stephane Collot, Suchin Gururangan, Sydney Borodinsky, Tamar Herman, Tara Fowler, Tarek Sheasha, Thomas Georgiou,
Thomas Scialom, Tobias Speckbacher, Todor Mihaylov, Tong Xiao, Ujjwal Karn, Vedanuj Goswami, Vibhor Gupta, Vignesh
Ramanathan, Viktor Kerkez, Vincent Gonguet, Virginie Do, Vish Vogeti, Vítor Albiero, Vladan Petrovic, Weiwei Chu, Wenhan
Xiong, Wenyin Fu, Whitney Meers, Xavier Martinet, Xiaodong Wang, Xiaofang Wang, Xiaoqing Ellen Tan, Xide Xia, Xinfeng
Xie, Xuchao Jia, Xuewei Wang, Yaelle Goldschlag, Yashesh Gaur, Yasmine Babaei, Yi Wen, Yiwen Song, Yuchen Zhang, Yue
Li, Yuning Mao, Zacharie Delpierre Coudert, Zheng Yan, Zhengxing Chen, Zoe Papakipos, Aaditya Singh, Aayushi Srivastava,
Abha Jain, Adam Kelsey, Adam Shajnfeld, Adithya Gangidi, Adolfo Victoria, Ahuva Goldstand, Ajay Menon, Ajay Sharma,
Alex Boesenberg, Alexei Baevski, Allie Feinstein, Amanda Kallet, Amit Sangani, Amos Teo, Anam Yunus, Andrei Lupu, Andres
Alvarado, Andrew Caples, Andrew Gu, Andrew Ho, Andrew Poulton, Andrew Ryan, Ankit Ramchandani, Annie Dong, Annie
Franco, Anuj Goyal, Aparajita Saraf, Arkabandhu Chowdhury, Ashley Gabriel, Ashwin Bharambe, Assaf Eisenman, Azadeh
Yazdan, Beau James, Ben Maurer, Benjamin Leonhardi, Bernie Huang, Beth Loyd, Beto De Paola, Bhargavi Paranjape, Bing
Liu, Bo Wu, Boyu Ni, Braden Hancock, Bram Wasti, Brandon Spence, Brani Stojkovic, Brian Gamido, Britt Montalvo, Carl
Parker, Carly Burton, Catalina Mejia, Ce Liu, Changhan Wang, Changkyu Kim, Chao Zhou, Chester Hu, Ching-Hsiang Chu, Chris
Cai, Chris Tindal, Christoph Feichtenhofer, Cynthia Gao, Damon Civin, Dana Beaty, Daniel Kreymer, Daniel Li, David Adkins,
David Xu, Davide Testuggine, Delia David, Devi Parikh, Diana Liskovich, Didem Foss, Dingkang Wang, Duc Le, Dustin Holland,
Edward Dowling, Eissa Jamil, Elaine Montgomery, Eleonora Presani, Emily Hahn, Emily Wood, Eric-Tuan Le, Erik Brinkman,
Esteban Arcaute, Evan Dunbar, Evan Smothers, Fei Sun, Felix Kreuk, Feng Tian, Filippos Kokkinos, Firat Ozgenel, Francesco
Caggioni, Frank Kanayet, Frank Seide, Gabriela Medina Florez, Gabriella Schwarz, Gada Badeer, Georgia Swee, Gil Halpern,
Grant Herman, Grigory Sizov, Guangyi, Zhang, Guna Lakshminarayanan, Hakan Inan, Hamid Shojanazeri, Han Zou, Hannah
Wang, Hanwen Zha, Haroun Habeeb, Harrison Rudolph, Helen Suk, Henry Aspegren, Hunter Goldman, Hongyuan Zhan, Ibrahim
Damlaj, Igor Molybog, Igor Tufanov, Ilias Leontiadis, Irina-Elena Veliche, Itai Gat, Jake Weissman, James Geboski, James Kohli,
Janice Lam, Japhet Asher, Jean-Baptiste Gaya, Jeff Marcus, Jeff Tang, Jennifer Chan, Jenny Zhen, Jeremy Reizenstein, Jeremy
Teboul, Jessica Zhong, Jian Jin, Jingyi Yang, Joe Cummings, Jon Carvill, Jon Shepard, Jonathan McPhie, Jonathan Torres, Josh
Ginsburg, Junjie Wang, Kai Wu, Kam Hou U, Karan Saxena, Kartikay Khandelwal, Katayoun Zand, Kathy Matosich, Kaushik
Veeraraghavan, Kelly Michelena, Keqian Li, Kiran Jagadeesh, Kun Huang, Kunal Chawla, Kyle Huang, Lailin Chen, Lakshya
Garg, Lavender A, Leandro Silva, Lee Bell, Lei Zhang, Liangpeng Guo, Licheng Yu, Liron Moshkovich, Luca Wehrstedt, Madian
Khabsa, Manav Avalani, Manish Bhatt, Martynas Mankus, Matan Hasson, Matthew Lennie, Matthias Reso, Maxim Groshev,
Maxim Naumov, Maya Lathi, Meghan Keneally, Miao Liu, Michael L. Seltzer, Michal Valko, Michelle Restrepo, Mihir Patel,
Mik Vyatskov, Mikayel Samvelyan, Mike Clark, Mike Macey, Mike Wang, Miquel Jubert Hermoso, Mo Metanat, Mohammad
Rastegari, Munish Bansal, Nandhini Santhanam, Natascha Parks, Natasha White, Navyata Bawa, Nayan Singhal, Nick Egebo,
Nicolas Usunier, Nikhil Mehta, Nikolay Pavlovich Laptev, Ning Dong, Norman Cheng, Oleg Chernoguz, Olivia Hart, Omkar
Salpekar, Ozlem Kalinli, Parkin Kent, Parth Parekh, Paul Saab, Pavan Balaji, Pedro Rittner, Philip Bontrager, Pierre Roux,
Piotr Dollar, Polina Zvyagina, Prashant Ratanchandani, Pritish Yuvraj, Qian Liang, Rachad Alao, Rachel Rodriguez, Rafi Ayub,
Raghotham Murthy, Raghu Nayani, Rahul Mitra, Rangaprabhu Parthasarathy, Raymond Li, Rebekkah Hogan, Robin Battey, Rocky
Wang, Russ Howes, Ruty Rinott, Sachin Mehta, Sachin Siby, Sai Jayesh Bondu, Samyak Datta, Sara Chugh, Sara Hunt, Sargun
Dhillon, Sasha Sidorov, Satadru Pan, Saurabh Mahajan, Saurabh Verma, Seiji Yamamoto, Sharadh Ramaswamy, Shaun Lindsay,
Shaun Lindsay, Sheng Feng, Shenghao Lin, Shengxin Cindy Zha, Shishir Patil, Shiva Shankar, Shuqiang Zhang, Shuqiang Zhang,
Sinong Wang, Sneha Agarwal, Soji Sajuyigbe, Soumith Chintala, Stephanie Max, Stephen Chen, Steve Kehoe, Steve Satterfield,
Sudarshan Govindaprasad, Sumit Gupta, Summer Deng, Sungmin Cho, Sunny Virk, Suraj Subramanian, Sy Choudhury, Sydney
Goldman, Tal Remez, Tamar Glaser, Tamara Best, Thilo Koehler, Thomas Robinson, Tianhe Li, Tianjun Zhang, Tim Matthews,
Timothy Chou, Tzook Shaked, Varun Vontimitta, Victoria Ajayi, Victoria Montanez, Vijai Mohan, Vinay Satish Kumar, Vishal
Mangla, Vlad Ionescu, Vlad Poenaru, Vlad Tiberiu Mihailescu, Vladimir Ivanov, Wei Li, Wenchen Wang, Wenwen Jiang, Wes
Bouaziz, Will Constable, Xiaocheng Tang, Xiaojian Wu, Xiaolan Wang, Xilun Wu, Xinbo Gao, Yaniv Kleinman, Yanjun Chen,
Ye Hu, Ye Jia, Ye Qi, Yenda Li, Yilin Zhang, Ying Zhang, Yossi Adi, Youngjin Nam, Yu, Wang, Yu Zhao, Yuchen Hao, Yundi
Qian, Yunlu Li, Yuzi He, Zach Rait, Zachary DeVito, Zef Rosnbrick, Zhaoduo Wen, Zhenyu Yang, Zhiwei Zhao, and Zhiyu Ma.


12


The llama 3 herd of models, 2024. [URL https://arxiv.org/abs/2407.21783.](https://arxiv.org/abs/2407.21783)


Dan Hendrycks, Collin Burns, Steven Basart, Andy Zou, Mantas Mazeika, Dawn Song, and Jacob Steinhardt. Measuring massive
multitask language understanding, 2021. [URL https://arxiv.org/abs/2009.03300.](https://arxiv.org/abs/2009.03300)


Ziwei Ji, Lei Yu, Yeskendir Koishekenov, Yejin Bang, Anthony Hartshorn, Alan Schelten, Cheng Zhang, Pascale Fung, and Nicola
Cancedda. Calibrating verbal uncertainty as a linear feature to reduce hallucinations, 2025. [URL https://arxiv.org/abs/](https://arxiv.org/abs/2503.14477)
[2503.14477.](https://arxiv.org/abs/2503.14477)


Mandar Joshi, Eunsol Choi, Daniel S. Weld, and Luke Zettlemoyer. Triviaqa: A large scale distantly supervised challenge dataset for
reading comprehension, 2017a. [URL https://arxiv.org/abs/1705.03551.](https://arxiv.org/abs/1705.03551)


Mandar Joshi, Eunsol Choi, Daniel S. Weld, and Luke Zettlemoyer. Triviaqa: A large scale distantly supervised challenge dataset for
reading comprehension, 2017b. [URL https://arxiv.org/abs/1705.03551.](https://arxiv.org/abs/1705.03551)


Saurav Kadavath, Tom Conerly, Amanda Askell, Tom Henighan, Dawn Drain, Ethan Perez, Nicholas Schiefer, Zac HatfieldDodds, Nova DasSarma, Eli Tran-Johnson, Scott Johnston, Sheer El-Showk, Andy Jones, Nelson Elhage, Tristan Hume, Anna
Chen, Yuntao Bai, Sam Bowman, Stanislav Fort, Deep Ganguli, Danny Hernandez, Josh Jacobson, Jackson Kernion, Shauna
Kravec, Liane Lovitt, Kamal Ndousse, Catherine Olsson, Sam Ringer, Dario Amodei, Tom Brown, Jack Clark, Nicholas Joseph,
Ben Mann, Sam McCandlish, Chris Olah, and Jared Kaplan. Language models (mostly) know what they know, 2022. URL
[https://arxiv.org/abs/2207.05221.](https://arxiv.org/abs/2207.05221)


Adam Tauman Kalai, Ofir Nachum, Santosh S. Vempala, and Edwin Zhang. Why language models hallucinate, 2025. URL

[https://arxiv.org/abs/2509.04664.](https://arxiv.org/abs/2509.04664)


Jared Kaplan, Sam McCandlish, Tom Henighan, Tom B. Brown, Benjamin Chess, Rewon Child, Scott Gray, Alec Radford, Jeffrey
Wu, and Dario Amodei. Scaling laws for neural language models, 2020. [URL https://arxiv.org/abs/2001.08361.](https://arxiv.org/abs/2001.08361)


Diederik P. Kingma and Max Welling. Auto-encoding variational bayes. _arXiv preprint arXiv:1312.6114_, 2013.


Kenneth Li, Oam Patel, Fernanda Viégas, Hanspeter Pfister, and Martin Wattenberg. Inference-time intervention: Eliciting truthful
answers from a language model, 2024. [URL https://arxiv.org/abs/2306.03341.](https://arxiv.org/abs/2306.03341)


Moxin Li, Yong Zhao, Wenxuan Zhang, Shuaiyi Li, Wenya Xie, See-Kiong Ng, Tat-Seng Chua, and Yang Deng. Knowledge boundary
of large language models: A survey. In _Proceedings of the 63rd Annual Meeting of the Association for Computational Linguistics_
_(ACL 2025)_ . Association for Computational Linguistics, 2025a. [URL https://aclanthology.org/2025.acl-long.](https://aclanthology.org/2025.acl-long.256)
[256.](https://aclanthology.org/2025.acl-long.256) Also available as arXiv:2412.12472.


Moxin Li, Yong Zhao, Wenxuan Zhang, Shuaiyi Li, Wenya Xie, See-Kiong Ng, Tat-Seng Chua, and Yang Deng. Knowledge boundary
of large language models: A survey. In _Proceedings of the 63rd Annual Meeting of the Association for Computational Linguistics_
_(ACL 2025)_ . Association for Computational Linguistics, 2025b. [URL https://aclanthology.org/2025.acl-long.](https://aclanthology.org/2025.acl-long.256)
[256.](https://aclanthology.org/2025.acl-long.256) Also available as arXiv:2412.12472.


Alex Mallen, Akari Asai, Victor Zhong, Rajarshi Das, Daniel Khashabi, and Hannaneh Hajishirzi. When not to trust language
models: Investigating effectiveness of parametric and non-parametric memories, 2023a. [URL https://arxiv.org/abs/](https://arxiv.org/abs/2212.10511)
[2212.10511.](https://arxiv.org/abs/2212.10511)


Alex Mallen, Akari Asai, Victor Zhong, Rajarshi Das, Daniel Khashabi, and Hannaneh Hajishirzi. When not to trust language
models: Investigating effectiveness of parametric and non-parametric memories, 2023b. [URL https://arxiv.org/abs/](https://arxiv.org/abs/2212.10511)
[2212.10511.](https://arxiv.org/abs/2212.10511)


Kenneth Marino, Mohammad Rastegari, Ali Farhadi, and Roozbeh Mottaghi. OK-VQA: A visual question answering benchmark
requiring external knowledge. _CoRR_, abs/1906.00067, 2019. [URL http://arxiv.org/abs/1906.00067.](http://arxiv.org/abs/1906.00067)


Sabrina J. Mielke, Arthur Szlam, Emily Dinan, and Y-Lan Boureau. Reducing conversational agents’ overconfidence through
linguistic calibration, 2022. [URL https://arxiv.org/abs/2012.14983.](https://arxiv.org/abs/2012.14983)


Tomas Mikolov, Wen-tau Yih, and Geoffrey Zweig. Linguistic regularities in continuous space word representations. In Lucy
Vanderwende, Hal Daumé III, and Katrin Kirchhoff, editors, _Proceedings of the 2013 Conference of the North American Chapter_
_of the Association for Computational Linguistics:_ _Human Language Technologies_, pages 746–751, Atlanta, Georgia, June 2013.
Association for Computational Linguistics. [URL https://aclanthology.org/N13-1090.](https://aclanthology.org/N13-1090)


Niklas Muennighoff, Luca Soldaini, Dirk Groeneveld, Kyle Lo, Jacob Morrison, Sewon Min, Weijia Shi, Pete Walsh, Oyvind Tafjord,
Nathan Lambert, Yuling Gu, Shane Arora, Akshita Bhagia, Dustin Schwenk, David Wadden, Alexander Wettig, Binyuan Hui, Tim
Dettmers, Douwe Kiela, Ali Farhadi, Noah A. Smith, Pang Wei Koh, Amanpreet Singh, and Hannaneh Hajishirzi. Olmoe: Open
mixture-of-experts language models, 2025. [URL https://arxiv.org/abs/2409.02060.](https://arxiv.org/abs/2409.02060)


13


Neel Nanda, Andrew Lee, and Martin Wattenberg. Emergent linear representations in world models of self-supervised sequence
models. In Yonatan Belinkov, Sophie Hao, Jaap Jumelet, Najoung Kim, Arya McCarthy, and Hosein Mohebbi, editors, _Proceedings_
_of the 6th BlackboxNLP Workshop:_ _Analyzing and Interpreting Neural Networks for NLP_, pages 16–30, Singapore, December
2023. Association for Computational Linguistics. doi: 10.18653/v1/2023.blackboxnlp-1.2. [URL https://aclanthology.](https://aclanthology.org/2023.blackboxnlp-1.2)
[org/2023.blackboxnlp-1.2.](https://aclanthology.org/2023.blackboxnlp-1.2)


Oscar Obeso, Andy Arditi, Javier Ferrando, Joshua Freeman, Cameron Holmes, and Neel Nanda. Real-time detection of hallucinated
entities in long-form generation, 2025. [URL https://arxiv.org/abs/2509.03531.](https://arxiv.org/abs/2509.03531)


OpenAI, Josh Achiam, Steven Adler, Sandhini Agarwal, Lama Ahmad, Ilge Akkaya, Florencia Leoni Aleman, Diogo Almeida,
Janko Altenschmidt, Sam Altman, Shyamal Anadkat, Red Avila, Igor Babuschkin, Suchir Balaji, Valerie Balcom, Paul Baltescu,
Haiming Bao, Mohammad Bavarian, Jeff Belgum, Irwan Bello, Jake Berdine, Gabriel Bernadett-Shapiro, Christopher Berner,
Lenny Bogdonoff, Oleg Boiko, Madelaine Boyd, Anna-Luisa Brakman, Greg Brockman, Tim Brooks, Miles Brundage, Kevin
Button, Trevor Cai, Rosie Campbell, Andrew Cann, Brittany Carey, Chelsea Carlson, Rory Carmichael, Brooke Chan, Che Chang,
Fotis Chantzis, Derek Chen, Sully Chen, Ruby Chen, Jason Chen, Mark Chen, Ben Chess, Chester Cho, Casey Chu, Hyung Won
Chung, Dave Cummings, Jeremiah Currier, Yunxing Dai, Cory Decareaux, Thomas Degry, Noah Deutsch, Damien Deville, Arka
Dhar, David Dohan, Steve Dowling, Sheila Dunning, Adrien Ecoffet, Atty Eleti, Tyna Eloundou, David Farhi, Liam Fedus, Niko
Felix, Simón Posada Fishman, Juston Forte, Isabella Fulford, Leo Gao, Elie Georges, Christian Gibson, Vik Goel, Tarun Gogineni,
Gabriel Goh, Rapha Gontijo-Lopes, Jonathan Gordon, Morgan Grafstein, Scott Gray, Ryan Greene, Joshua Gross, Shixiang Shane
Gu, Yufei Guo, Chris Hallacy, Jesse Han, Jeff Harris, Yuchen He, Mike Heaton, Johannes Heidecke, Chris Hesse, Alan Hickey,
Wade Hickey, Peter Hoeschele, Brandon Houghton, Kenny Hsu, Shengli Hu, Xin Hu, Joost Huizinga, Shantanu Jain, Shawn Jain,
Joanne Jang, Angela Jiang, Roger Jiang, Haozhun Jin, Denny Jin, Shino Jomoto, Billie Jonn, Heewoo Jun, Tomer Kaftan, Łukasz
Kaiser, Ali Kamali, Ingmar Kanitscheider, Nitish Shirish Keskar, Tabarak Khan, Logan Kilpatrick, Jong Wook Kim, Christina Kim,
Yongjik Kim, Jan Hendrik Kirchner, Jamie Kiros, Matt Knight, Daniel Kokotajlo, Łukasz Kondraciuk, Andrew Kondrich, Aris
Konstantinidis, Kyle Kosic, Gretchen Krueger, Vishal Kuo, Michael Lampe, Ikai Lan, Teddy Lee, Jan Leike, Jade Leung, Daniel
Levy, Chak Ming Li, Rachel Lim, Molly Lin, Stephanie Lin, Mateusz Litwin, Theresa Lopez, Ryan Lowe, Patricia Lue, Anna
Makanju, Kim Malfacini, Sam Manning, Todor Markov, Yaniv Markovski, Bianca Martin, Katie Mayer, Andrew Mayne, Bob
McGrew, Scott Mayer McKinney, Christine McLeavey, Paul McMillan, Jake McNeil, David Medina, Aalok Mehta, Jacob Menick,
Luke Metz, Andrey Mishchenko, Pamela Mishkin, Vinnie Monaco, Evan Morikawa, Daniel Mossing, Tong Mu, Mira Murati,
Oleg Murk, David Mély, Ashvin Nair, Reiichiro Nakano, Rajeev Nayak, Arvind Neelakantan, Richard Ngo, Hyeonwoo Noh,
Long Ouyang, Cullen O’Keefe, Jakub Pachocki, Alex Paino, Joe Palermo, Ashley Pantuliano, Giambattista Parascandolo, Joel
Parish, Emy Parparita, Alex Passos, Mikhail Pavlov, Andrew Peng, Adam Perelman, Filipe de Avila Belbute Peres, Michael Petrov,
Henrique Ponde de Oliveira Pinto, Michael, Pokorny, Michelle Pokrass, Vitchyr H. Pong, Tolly Powell, Alethea Power, Boris
Power, Elizabeth Proehl, Raul Puri, Alec Radford, Jack Rae, Aditya Ramesh, Cameron Raymond, Francis Real, Kendra Rimbach,
Carl Ross, Bob Rotsted, Henri Roussez, Nick Ryder, Mario Saltarelli, Ted Sanders, Shibani Santurkar, Girish Sastry, Heather
Schmidt, David Schnurr, John Schulman, Daniel Selsam, Kyla Sheppard, Toki Sherbakov, Jessica Shieh, Sarah Shoker, Pranav
Shyam, Szymon Sidor, Eric Sigler, Maddie Simens, Jordan Sitkin, Katarina Slama, Ian Sohl, Benjamin Sokolowsky, Yang Song,
Natalie Staudacher, Felipe Petroski Such, Natalie Summers, Ilya Sutskever, Jie Tang, Nikolas Tezak, Madeleine B. Thompson,
Phil Tillet, Amin Tootoonchian, Elizabeth Tseng, Preston Tuggle, Nick Turley, Jerry Tworek, Juan Felipe Cerón Uribe, Andrea
Vallone, Arun Vijayvergiya, Chelsea Voss, Carroll Wainwright, Justin Jay Wang, Alvin Wang, Ben Wang, Jonathan Ward, Jason
Wei, CJ Weinmann, Akila Welihinda, Peter Welinder, Jiayi Weng, Lilian Weng, Matt Wiethoff, Dave Willner, Clemens Winter,
Samuel Wolrich, Hannah Wong, Lauren Workman, Sherwin Wu, Jeff Wu, Michael Wu, Kai Xiao, Tao Xu, Sarah Yoo, Kevin Yu,
Qiming Yuan, Wojciech Zaremba, Rowan Zellers, Chong Zhang, Marvin Zhang, Shengjia Zhao, Tianhao Zheng, Juntang Zhuang,
William Zhuk, and Barret Zoph. Gpt-4 technical report, 2024. [URL https://arxiv.org/abs/2303.08774.](https://arxiv.org/abs/2303.08774)


Long Ouyang, Jeff Wu, Xu Jiang, Diogo Almeida, Carroll L. Wainwright, Pamela Mishkin, Chong Zhang, Sandhini Agarwal,
Katarina Slama, Alex Ray, John Schulman, Jacob Hilton, Fraser Kelton, Luke Miller, Maddie Simens, Amanda Askell, Peter
Welinder, Paul Christiano, Jan Leike, and Ryan Lowe. Training language models to follow instructions with human feedback,
2022. [URL https://arxiv.org/abs/2203.02155.](https://arxiv.org/abs/2203.02155)


Gerry Pallier, Rebecca Wilkinson, Vanessa Danthiir, Sabina Kleitman, Goran Knezevic, Lazar Stankov, and Richard D. Roberts. The
role of individual differences in the accuracy of confidence judgments. _The Journal of General Psychology_, 129(3):257–299, July
2002. doi: 10.1080/00221300209602099.


Jayneel Parekh, Pegah Khayatan, Mustafa Shukor, Arnaud Dapogny, Alasdair Newson, and Matthieu Cord. Learning to steer:
Input-dependent steering for multimodal llms. _arXiv preprint arXiv:2508.12815_, 2025.


Kiho Park, Yo Joong Choe, and Victor Veitch. The linear representation hypothesis and the geometry of large language models, 2023.
[URL https://arxiv.org/abs/2311.03658.](https://arxiv.org/abs/2311.03658)


Seongheon Park, Xuefeng Du, Min-Hsuan Yeh, Haobo Wang, and Yixuan Li. Steer llm latents for hallucination detection, 2025.
[URL https://arxiv.org/abs/2503.01917.](https://arxiv.org/abs/2503.01917)


14


Anselm Paulus, Arman Zharmagambetov, Chuan Guo, Brandon Amos, and Yuandong Tian. Advprompter: Fast adaptive adversarial
prompting for llms, 2025. [URL https://arxiv.org/abs/2404.16873.](https://arxiv.org/abs/2404.16873)


Qwen, :, An Yang, Baosong Yang, Beichen Zhang, Binyuan Hui, Bo Zheng, Bowen Yu, Chengyuan Li, Dayiheng Liu, Fei Huang,
Haoran Wei, Huan Lin, Jian Yang, Jianhong Tu, Jianwei Zhang, Jianxin Yang, Jiaxi Yang, Jingren Zhou, Junyang Lin, Kai Dang,
Keming Lu, Keqin Bao, Kexin Yang, Le Yu, Mei Li, Mingfeng Xue, Pei Zhang, Qin Zhu, Rui Men, Runji Lin, Tianhao Li, Tianyi
Tang, Tingyu Xia, Xingzhang Ren, Xuancheng Ren, Yang Fan, Yang Su, Yichang Zhang, Yu Wan, Yuqiong Liu, Zeyu Cui, Zhenru
Zhang, and Zihan Qiu. Qwen2.5 technical report, 2025. [URL https://arxiv.org/abs/2412.15115.](https://arxiv.org/abs/2412.15115)


A Yang Qwen, Baosong Yang, B Zhang, B Hui, B Zheng, B Yu, Chengpeng Li, D Liu, F Huang, H Wei, et al. Qwen2. 5 technical
report. _arXiv preprint_, 2024.


Vipula Rawte, Amit Sheth, and Amitava Das. A survey of hallucination in large foundation models. _arXiv preprint arXiv:2309.05922_,
2023.


David Rein, Betty Li Hou, Asa Cooper Stickland, Jackson Petty, Richard Yuanzhe Pang, Julien Dirani, Julian Michael, and Samuel R.
Bowman. Gpqa: A graduate-level google-proof q&a benchmark, 2023. [URL https://arxiv.org/abs/2311.12022.](https://arxiv.org/abs/2311.12022)


Danilo Jimenez Rezende, Shakir Mohamed, and Daan Wierstra. Stochastic backpropagation and approximate inference in deep
generative models. In _Proceedings of the 31st International Conference on Machine Learning_, pages 1278–1286, 2014.


Nina Rimsky, Nick Gabrieli, Julian Schulz, Meg Tong, Evan Hubinger, and Alexander Turner. Steering llama 2 via contrastive
activation addition. In Lun-Wei Ku, Andre Martins, and Vivek Srikumar, editors, _Proceedings of the 62nd Annual Meeting of_
_the Association for Computational Linguistics (Volume 1:_ _Long Papers)_, pages 15504–15522, Bangkok, Thailand, August 2024.
Association for Computational Linguistics. doi: 10.18653/v1/2024.acl-long.828. URL [https://aclanthology.org/](https://aclanthology.org/2024.acl-long.828/)
[2024.acl-long.828/.](https://aclanthology.org/2024.acl-long.828/)


Peter J Rousseeuw. Silhouettes: a graphical aid to the interpretation and validation of cluster analysis. _Journal of Computational and_
_Applied Mathematics_, 20:53–65, 1987.


William F Shen, Xinchi Qiu, Nicola Cancedda, and Nicholas D Lane. Don’t make it up: Preserving ignorance awareness in llm
fine-tuning. _arXiv preprint arXiv:2506.14387_, 2025a.


William F. Shen, Xinchi Qiu, Meghdad Kurmanji, Alex Iacob, Lorenzo Sani, Yihong Chen, Nicola Cancedda, and Nicholas D. Lane.
Lunar: Llm unlearning via neural activation redirection, 2025b. [URL https://arxiv.org/abs/2502.07218.](https://arxiv.org/abs/2502.07218)


Lazar Stankov and John D. Crawford. Confidence judgments in studies of individual differences. _Personality_ _and_ _Individual_
_Differences_, 21(6):971–986, 1996. ISSN 0191-8869. doi: 10.1016/S0191-8869(96)00130-4.


Asa Cooper Stickland, Alexander Lyzhov, Jacob Pfau, Salsabila Mahdi, and Samuel R Bowman. Steering without side effects:
Improving post-deployment control of language models. _arXiv preprint arXiv:2406.15518_, 2024.


Adly Templeton, Tom Conerly, Jonathan Marcus, Jack Lindsey, Trenton Bricken, Brian Chen, Adam Pearce, Craig Citro, Emmanuel
Ameisen, Andy Jones, Hoagy Cunningham, Nicholas L Turner, Callum McDougall, Monte MacDiarmid, Alex Tamkin, Esin
Durmus, Tristan Hume, Francesco Mosconi, C. Daniel Freeman, Theodore R. Sumers, Edward Rees, Joshua Batson, Adam
Jermyn, Shan Carter, Chris Olah, and Tom Henighan. Scaling monosemanticity: Extracting interpretable features from claude 3
sonnet, 2024. [URL https://transformer-circuits.pub/2024/scaling-monosemanticity/index.html.](https://transformer-circuits.pub/2024/scaling-monosemanticity/index.html)
Accessed: 2025-09-22.


Bowei Tian, Xuntao Lyu, Meng Liu, Hongyi Wang, and Ang Li. Why representation engineering works: A theoretical and empirical
study in vision-language models, 2025. [URL https://arxiv.org/abs/2503.22720.](https://arxiv.org/abs/2503.22720)


Alexander Matt Turner, Lisa Thiergart, Gavin Leech, David Udell, Juan J. Vazquez, Ulisse Mini, and Monte MacDiarmid. Steering
language models with activation engineering, 2024. [URL https://arxiv.org/abs/2308.10248.](https://arxiv.org/abs/2308.10248)


Jason Wei, Nguyen Karina, Hyung Won Chung, Yunxin Joy Jiao, Spencer Papay, Amelia Glaese, John Schulman, and William Fedus.
Measuring short-form factuality in large language models, 2024. [URL https://arxiv.org/abs/2411.04368.](https://arxiv.org/abs/2411.04368)


Genta Indra Winata, Frederikus Hudi, Patrick Amadeus Irawan, David Anugraha, Rifki Afina Putri, Yutong Wang, Adam Nohejl,
Ubaidillah Ariq Prathama, Nedjma Ousidhoum, Afifa Amriani, et al. Worldcuisines: A massive-scale benchmark for multilingual
and multicultural visual question answering on global cuisines. _arXiv preprint arXiv:2410.12705_, 2024.


Zhengxuan Wu, Aryaman Arora, Zheng Wang, Atticus Geiger, Dan Jurafsky, Christopher D. Manning, and Christopher Potts. Reft:
Representation finetuning for language models, 2024. [URL https://arxiv.org/abs/2404.03592.](https://arxiv.org/abs/2404.03592)


Wannan Yang and György Buzsáki. Interpretability of LLM deception: Universal motif. In _ICLR 2025 Conference_, 2025. URL

[https://openreview.net/forum?id=znL549Ymoi.](https://openreview.net/forum?id=znL549Ymoi) Submitted Sept 28, 2024; Last modified Feb 5, 2025; ICLR 2025
submission, under review.


15


Zhangyue Yin, Qiushi Sun, Qipeng Guo, Jiawen Wu, Xipeng Qiu, and Xuanjing Huang. Do large language models know
what they don’t know? In _Findings_ _of_ _the_ _Association_ _for_ _Computational_ _Linguistics_ _(ACL_ _2023)_, 2023a. URL [https:](https://aclanthology.org/2023.findings-acl.551/)
[//aclanthology.org/2023.findings-acl.551/.](https://aclanthology.org/2023.findings-acl.551/)


Zhangyue Yin, Qiushi Sun, Qipeng Guo, Jiawen Wu, Xipeng Qiu, and Xuanjing Huang. Do large language models know what they
don’t know?, 2023b. [URL https://arxiv.org/abs/2305.18153.](https://arxiv.org/abs/2305.18153)


Gal Yona, Roee Aharoni, and Mor Geva. Can large language models faithfully express their intrinsic uncertainty in words?, 2024.
[URL https://arxiv.org/abs/2405.16908.](https://arxiv.org/abs/2405.16908)


Ashkan Yousefpour, Taeheon Kim, Ryan S. Kwon, Seungbeen Lee, Wonje Jeung, Seungju Han, Alvin Wan, Harrison Ngan, Youngjae
Yu, and Jonghyun Choi. Representation bending for large language model safety, 2025. [URL https://arxiv.org/abs/](https://arxiv.org/abs/2504.01550)
[2504.01550.](https://arxiv.org/abs/2504.01550)


Lei Yu, Meng Cao, Jackie Chi Kit Cheung, and Yue Dong. Mechanistic understanding and mitigation of language model non-factual
hallucinations. In _Findings of the Association for Computational Linguistics:_ _EMNLP 2024_, pages 7943–7956, 2024a.


Lei Yu, Meng Cao, Jackie Chi Kit Cheung, and Yue Dong. Mechanistic understanding and mitigation of language model non-factual
hallucinations. _arXiv preprint arXiv:2403.18167_, 2024b. doi: 10.48550/arXiv.2403.18167.


Lei Yu, Virginie Do, Karen Hambardzumyan, and Nicola Cancedda. Robust llm safeguarding via refusal feature adversarial training,
2025. [URL https://arxiv.org/abs/2409.20089.](https://arxiv.org/abs/2409.20089)


Anqi Zhang, Yulin Chen, Jane Pan, Chen Zhao, Aurojit Panda, Jinyang Li, and He He. Reasoning models know when they’re right:
Probing hidden states for self-verification, 2025. [URL https://arxiv.org/abs/2504.05419.](https://arxiv.org/abs/2504.05419)


Lianmin Zheng, Wei-Lin Chiang, Ying Sheng, Siyuan Zhuang, Zhanghao Wu, Yonghao Zhuang, Zi Lin, Zhuohan Li, Dacheng Li,
Eric P. Xing, Hao Zhang, Joseph E. Gonzalez, and Ion Stoica. Judging llm-as-a-judge with mt-bench and chatbot arena, 2023.
[URL https://arxiv.org/abs/2306.05685.](https://arxiv.org/abs/2306.05685)


Andy Zou, Long Phan, Justin Wang, Derek Duenas, Maxwell Lin, Maksym Andriushchenko, Rowan Wang, Zico Kolter, Matt
Fredrikson, and Dan Hendrycks. Improving alignment and robustness with circuit breakers, 2024. [URL https://arxiv.](https://arxiv.org/abs/2406.04313)
[org/abs/2406.04313.](https://arxiv.org/abs/2406.04313)


Andy Zou, Long Phan, Sarah Chen, James Campbell, Phillip Guo, Richard Ren, Alexander Pan, Xuwang Yin, Mantas Mazeika,
Ann-Kathrin Dombrowski, Shashwat Goel, Nathaniel Li, Michael J. Byun, Zifan Wang, Alex Mallen, Steven Basart, Sanmi
Koyejo, Dawn Song, Matt Fredrikson, J. Zico Kolter, and Dan Hendrycks. Representation engineering: A top-down approach to ai
transparency, 2025. [URL https://arxiv.org/abs/2310.01405.](https://arxiv.org/abs/2310.01405)

### **9 Acknowledgement**


We also thank Nathaniel Li, Irene Zhang, Julian Coda-Forno, Sriyash Poddar, Anselm Paulus, Sai Surya Duvvuri, Rachit
Bansal, Devvrit Khatri, Ellie Pavlick and Jojo Yang for providing thoughtful feedback and insightful discussions on the
manuscript.


16


### **Appendix** **Table of Contents**

**A** **Further Discussion on Related Work** . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . **19**
A.1 Knowledge Representation and the Linear Representation Hypothesis . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 19


**B** **Further Discussion on Amortized Optimization** . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . **19**


**C** **Steering** . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . **20**
C.1 Steering Vector Construction . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 20
C.2 Layer Selection . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 20


**D** **CASAL Training** . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . **21**
D.1 Relationship between Activation Steering and CASAL Training . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 21
D.2 Weight Update before and after CASAL . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 22


**E** **Contrastive Activation Addition (CAA) VS CASAL** . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . **23**


**F** **Example Model Outputs** . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . **24**


**G** **Dataset** . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . **31**
G.1 Entity Dataset . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 31
G.2 TriviaQA Dataset . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 32
G.3 PopQA Dataset . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 32
G.4 WorldCuisines Dataset . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 32


**H** **Metrics for Performance and Cluster Separation** . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . **33**
H.1 Refusal Rate . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 33
H.2 Hallucination Rate . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 33
H.3 Accuracy . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 33
H.4 Silhouette Score . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 33


**I** **Knowledge Probing** . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . **35**
I.1 Knowledge Probing Threshold . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 37


**J** **Models** . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . **38**


**K** **Ablation** . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . **38**
K.1 Sub-module for training . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 39


**L** **Hyper-parameter Search for CASAL Training** . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . **39**
L.1 Learning Rate . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 39


17


L.2 Steering Strength . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 40


**M** **SFT and DPO Training** . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . **41**


**N** **Compute Cost of Calculation (FLOPs per Token)** . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . **42**
N.1 Full-parameter finetuning . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 42
N.2 Comparing full-parameter finetune and CASAL finetune . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 42
N.3 LoRA finetuning . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 43
N.4 Comparing full-parameter finetune and LoRA finetune . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 44


**O** **Multimodal Model** . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . **46**


**P** **Mixture-of-Experts (MoE) Training** . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . **49**
P.1 PCA Activation Across Experts . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 51


**Q** **PCA Activations After Different Training Methods** . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . **53**


**R** **Computational Requirements** . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . **55**


**S** **The Use of Large Language Models** . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . **55**


18


### **A Further Discussion on Related Work**

**A.1** **Knowledge Representation and the Linear Representation Hypothesis**


Humans often display systematic overconfidence: their subjective confidence often exceeds objective accuracy (Pallier
et al., 2002; Stankov and Crawford, 1996). Large language models (LLMs) exhibit a similar pattern: they are poorly
calibrated on general knowledge tasks, frequently producing answers with misplaced confidence (Kadavath et al., 2022;
Yin et al., 2023b; Yona et al., 2024; Zhang et al., 2025).


Recent interpretability studies (using sparse autoencoder (SAE) features (Ferrando et al., 2025) or residual stream
activations (Ji et al., 2025)) suggest that transformer models encode many abstract concepts as linear directions in
activation space (Nanda et al., 2023; Mikolov et al., 2013; Park et al., 2023; Arditi et al., 2024; Yang and Buzsáki, 2025).
Behavioral traits such as truthfulness, sycophancy, refusal (Arditi et al., 2024), and reasoning strategies have shown to
be linearly represented. Emerging evidence indicates that models may also possess intrinsic linear representations of
knowledge boundary (Ferrando et al., 2025) and uncertainty (Ji et al., 2025) for their own knowledge limitation, which
can be harnessed for calibrating overconfidence in LLMs.

### **B Further Discussion on Amortized Optimization**


_Amortized Optimization Perspective._ Our approach combines insights from interpretability and amortized optimization
(Kingma and Welling, 2013; Rezende et al., 2014; Gershman and Goodman, 2014). Formally, amortized optimization
replaces repeated problem-specific optimizations


_θ_ _[∗]_ ( _x_ ) = arg min _L_ ( _fθ, x_ )
_θ_


with the training of a parametric function _gϕ_ ( _x_ ) that directly predicts an approximate solution, i.e., _θ_ _[∗]_ ( _x_ ) _≈_ _gϕ_ ( _x_ ).
This paradigm reduces per-instance optimization compute cost by learning a global set of parameters _ϕ_ that amortize
inference across the data distribution.


VAEs provide a canonical example: instead of optimizing a separate variational posterior _q_ ( _z|x_ ) for every datapoint, the
encoder _qϕ_ ( _z|x_ ) is trained to amortize inference. The optimization signal is the evidence lower bound (ELBO),


_L_ ELBO( _θ, ϕ_ ) = E _qϕ_ ( _z|x_ )[log _pθ_ ( _x|z_ )] _−_ KL( _qϕ_ ( _z|x_ ) _∥_ _p_ ( _z_ )) _,_


Amortization arises from the parameterization of inference with a shared encoder network _qϕ_ ( _z|x_ ), which maps each
input x to distributional parameters in a single forward pass, replacing the need to optimize separate variational
parameters for each datapoint.


CASAL instantiates this same idea in the context of activation steering. Instead of repeatedly solving for a steering
direction _v_ _[∗]_ ( _x_ ) that separates known from unknown knowledge in residual activations _h_ ( _x_ ), we train a lightweight
subnetwork _sϕ_ to approximate this solution:


_v_ _[∗]_ ( _x_ ) _≈_ _sϕ_ ( _h_ ( _x_ )) _._


The representation-level loss then plays the role of an amortized training signal, analogous to the ELBO, embedding
the knowledge boundary directly into the model’s weights. This allows the model to align its outputs with its internal
representations in a single forward pass, making steering efficient and scalable.


19


### **C Steering**

**Figure** **4** **Illustration of steering vector and target activation construction.** (A) Mean activations at the target layer _L_ _[∗]_ are
computed for known queries ( _a_ ¯ _[L]_ _k_ _[∗]_ [) and][ unknown queries][ (] _[a]_ [¯] _u_ _[L][∗]_ [).] [(B) Steering vectors are defined by the difference of these means:]
_vk_ _[L][∗]_ = _a_ ¯ _[L]_ _k_ _[∗]_ _−_ _a_ ¯ _[L]_ _u_ _[∗]_ (pointing toward the known cluster) and _vu_ _[L][∗]_ = _a_ ¯ _[L]_ _u_ _[∗]_ _−_ _a_ ¯ _[L]_ _k_ _[∗]_ (pointing toward the unknown cluster). (C) Target
activations are generated by shifting the raw activations _a_ _[L][∗]_ ( _x_ ) along the corresponding steering vector: _t_ _[L]_ _k_ _[∗]_ [(] _[x]_ [)][ =] _[ a][L][∗]_ [(] _[x]_ [) +] _[ v]_ _k_ _[L][∗]_
for known queries, and _t_ _[L]_ _u_ _[∗]_ [(] _[x]_ [)][ =] _[ a][L][∗]_ [(] _[x]_ [) +] _[ v]_ _u_ _[L][∗]_ for unknown queries. These target activations serve as supervision signals during
CASAL training.


**C.1** **Steering Vector Construction**


_Known vs._ _Unknown Separation._ Queries are partitioned into _Dk_ (known) and _Du_ (unknown) based on the model’s
consistency across multiple sampled answers. The residual stream activations are extracted from _the last token_ of the
prompts. Averaged activations over each set yield mean activations:


_a_ ¯ _[L]_ _k_ _[∗]_ = E _x∈Dk_ [ _a_ _[L][∗]_ ( _x_ )] _,_ _a_ ¯ _[L]_ _u_ _[∗]_ = E _x∈Du_ [ _a_ _[L][∗]_ ( _x_ )] _._


_Steering Vectors and Target Activations._ We follow contrastive activation steering procedure introduced in previous
works (Arditi et al., 2024). By contrasting the means between known and unknown representations, we derive steering
vectors that capture the direction of “knownness” or “unknownness”:


_vu_ _[L][∗]_ = ¯ _a_ _[L]_ _u_ _[∗]_ _[−]_ _[a]_ [¯] _k_ _[L][∗]_ _[,]_ _vk_ _[L][∗]_ = ¯ _a_ _[L]_ _k_ _[∗]_ _−_ _a_ ¯ _[L]_ _u_ _[∗]_ _[.]_


Applying these shifts to an activation produces _target activations_ :


_t_ _[L]_ _u_ _[∗]_ [(] _[x]_ [)][ =] _[ a][L][∗]_ [(] _[x]_ [) +] _[ v]_ _u_ _[L][∗]_ _[,]_ _t_ _[L]_ _k_ _[∗]_ [(] _[x]_ [)][ =] _[ a][L][∗]_ [(] _[x]_ [) +] _[ v]_ _k_ _[L][∗]_ _[.]_

Intuitively, _t_ _[L]_ _u_ _[∗]_ [(] _[x]_ [)][ encourages the model to abstain when uncertain, while] _[ t]_ _k_ _[L][∗]_ [(] _[x]_ [)][ reinforces confident answering when]
the knowledge is present.


**C.2** **Layer Selection**


A crucial step in CASAL is selecting the optimal target layer _L_ _[∗]_ . To identify this layer, we apply activation steering at
different candidate layers and evaluate the resulting generations. Specifically, we measure two complementary metrics:


20


(1) the _hallucination_ _score_ on _Du_ (unknown queries), which quantifies the model’s tendency to produce incorrect
answers when it lacks knowledge, and (2) the _accuracy_ on _Dk_ (known queries), which ensures that steering does not
suppress correct answering. The optimal _L_ _[∗]_ is chosen as the layer that simultaneously minimizes hallucination for
unknowns while preserving high accuracy for knowns. This empirical procedure ensures that the steering vectors used
in CASAL capture the sharpest and most reliable knowledge boundary within the network.

### **D CASAL Training**


**D.1** **Relationship between Activation Steering and CASAL Training**


**Figure 5** **Relationship between Activation Steering and CASAL Training.** (A) **Activation Steering.** At the target layer _L_ _[∗]_,
activations _a_ _[L][∗]_ ( _x_ ) for known and unknown queries are separated by computing mean representations across each group. Their
difference defines steering vectors, which are applied to produce target activations _t_ _[L]_ _k_ _[∗]_ [(] _[x]_ [)][ (promoting answering for][ known][ queries)]
and _t_ _[L]_ _u_ _[∗]_ [(] _[x]_ [)] [(encouraging] [abstention] [for] [unknown] [queries).] [(B)] **[CASAL]** **[Training.]** [Instead] [of] [applying] [steering] [vectors] [online,]
CASAL trains a lightweight one-layer module at _L_ _[∗]_ to approximate these steering shifts. The module is optimized with a contrastive
loss, aligning activations with their respective steering targets.


Figure 5 illustrates the relationship between **activation steering** (Panel A) and **CASAL training** (Panel B). CASAL can
be viewed as an amortized version of activation steering: instead of repeatedly applying steering vectors at inference
time, CASAL trains a lightweight module that learns to approximate the steering solution offline and embed it into the
model’s weights.


**Residual Activation Extraction (Panel A).** For a given query _x_, with **one forward pass**, we extract the residual stream
activations _a_ _[L][∗][−]_ [1] ( _x_ ) and _a_ _[L][∗]_ ( _x_ ) before entering the target layer ( _L_ _[∗]_ _−_ 1) and immediately after passing the designated
target layer _L_ _[∗]_ . These activations are then cached and used for training later.


**Target Activation Construction (Panel A).** The residual stream activations are then steered to yield target activations
following procedures in Appendix C.1, producing _t_ _[L]_ _k_ _[∗]_ [(] _[x]_ [)][ for][ known][ queries and] _[ t]_ _u_ _[L][∗]_ [(] _[x]_ [)][ for][ unknown][ queries.]


**CASAL Training (Panel B).** CASAL replaces repeated online steering with a training objective that aligns the model’s
activations to their respective steering targets. At the target layer _L_ _[∗]_, instead of applying steering vectors directly, a small
trainable subnetwork maps _a_ _[L][∗][−]_ [1] ( _x_ ) to an updated residual activation ˆ _a_ _[L][∗]_ ( _x_ ). CASAL enforces that these updated
activations align with the steering targets defined in Panel A using the loss:

_L_ = E _x∈Du_ _∥t_ _[L]_ _u_ _[∗]_ [(] _[x]_ [)] _[ −]_ _[a][L][∗]_ [(] _[x]_ [)] _[∥]_ [2] [+] [E] _[x][∈][D]_ _k_ _[∥][t][L]_ _k_ _[∗]_ [(] _[x]_ [)] _[ −]_ _[a][L][∗]_ [(] _[x]_ [)] _[∥]_ [2] _[.]_


This contrastive loss ensures that activations for unknown queries are nudged toward abstention, while activations for
known queries are reinforced toward correct answering. Through training, the parameters of the subnetwork are updated


21


such that the model learns to approximate steering automatically. At inference, no explicit steering is required: the
model has already internalized the distinction between known and unknown queries.


In summary, the relationship between the steering stage and the training stage is that the steering stage prepares the
inputs ( _a_ _[L][∗][−]_ [1] ( _x_ )) and target outputs ( _t_ _[L]_ _u_ _[∗]_ [(] _[x]_ [)][ and] _[ t]_ _k_ _[L][∗]_ [(] _[x]_ [)][, which are part of the loss function).] [The arrows in Figure][ 5]
trace this flow.


**D.2** **Weight Update before and after CASAL**


Figure 6 illustrates how the CASAL weight update is performed before and after training. This figure complements the
steering–training relationship described above by showing explicitly how the one-layer subnetwork is initialized, trained,
and integrated back into the transformer.


**Figure 6** Before and After


**Before Training (Panel A).** We begin with the frozen pretrained model. At the target layer _L_ _[∗]_, the original weight
matrix _W_ original _[L][∗]_ [is used to compute the residual stream activations] _[ a][L][∗][−]_ [1][(] _[x]_ [)][ and target activations (] _[t]_ _u_ _[L][∗]_ [and] _[ t]_ _k_ _[L][∗]_ [).]


**CASAL Training (Panel B).** During CASAL training, we prepare a lightweight one-layer neural network, initialized
with _W_ original _[L][∗]_ [.] [This network takes the pre-activation] _[ a][L][∗][−]_ [1][(] _[x]_ [)][ as input and outputs an updated activation][ ˆ] _[a][L][∗]_ [(] _[x]_ [)][.] [The]
network is trained using the contrastive loss. Through optimization, the parameters of this one-layer network are updated,
yielding a trained weight _W_ trained _[L][∗]_ [that better separates][ known][ from][ unknown][ activations.]

**After Training (Panel C).** Once training is complete, the learned weight _W_ trained _[L][∗]_ [replaces the original] _[ W][ L]_ original _[∗]_ [directly]
inside the transformer. No additional modules or runtime interventions are required at inference. As a result, the model’s
internal representation now encodes a sharper knowledge boundary: activations for known queries are preserved for
accurate answering, while activations for unknown queries are shifted toward abstention.


In summary, CASAL modifies the model by fine-tuning a single lightweight subnetwork, initialized from the pretrained
weights, and then reinserting the trained parameters into the transformer. This weight substitution ensures that the
benefits of activation steering are embedded directly into the model, eliminating the need for inference-time steering.


22


### **E Contrastive Activation Addition (CAA) VS CASAL**

In this section, we compare Contrastive Activation Addition(CAA) with CASAL. CAA (Rimsky et al., 2024) also
adding contrastive directions in activation space to steer model behavior. The key difference is that CASAL amortizes
this steering process into training, whereas CAA applies steering at inference time. Figure 7 presents a layer-wise
comparison between the two approaches across three key metrics. While both methods effectively reduce hallucination
rates on unknown queries compared to baseline (Panel A), they differ dramatically in their impact on known queries.
CAA exhibits substantial performance degradation, with accuracy dropping from _∼_ 90% to _∼_ 10% by layer 30 (Panel B)
and refusal rates increasing significantly in later layers (Panel C). ). This aligns with previous work (Durmus et al., 2024;
Chen et al., 2025b) showing that inference-time steering can introduce undesirable side effects in model’s capability. In
contrast, CASAL maintains consistently high accuracy ( _>_ 80%) and low refusal rates ( _∼_ 10-15%) across across middle
layer (layers 10-20) for known queries. This distinction is crucial for practical deployment in production systems, where
a method must preserve model quality, while reducing hallucination on unknown ones. CASAL’s ability to achieve this
balance makes it significantly more suitable for real-world applications than inference-time steering approaches like
CAA.


**Figure 7** **Layer-wise comparison of CASAL and CAA performance.** **(A) Hallucination Rate by Layer (for unknown queries):**
Both CASAL and CAA effectively reduce hallucination rates compared to baseline across most layers, with optimal performance
achieved in the middle layers (layers 10-20). **(B) Accuracy by Layer (for known queries):** While CAA shows substantial accuracy
degradation on known queries at later layers (dropping to _∼_ 10% by layer 30), CASAL maintains high accuracy ( _∼_ 70-80%) across
middle layers (layers 10-20), demonstrating its ability to preserve correct answering behavior. **(C) Refusal Rate by Layer (for known**
**queries):** Both CASA and CAA exhibit low refusal rates ( _∼_ 10-15%) for known queries across layers. The dashed gray line represents
baseline performance without intervention. Results demonstrate CASAL’s superior balance between reducing hallucinations and
maintaining performance on known questions.


23


### **F Example Model Outputs**





24


25


26


27


28


29


30


### **G Dataset**

**G.1** **Entity Dataset**


[The Entity Dataset](https://github.com/javiferran/sae_entities/tree/main/dataset/processed/entity_prompts) from Ferrando et al. (2025) consists of 150k data from Wikipedia .


31


**Table 6** Entity Dataset Statistics for Llama-3.1-8B


**Entity Type** **Known Count** **Unknown Count** **Total Count**


song 5,065 27,124 33,792
movie 6,741 56,673 65,370
city 4,297 26,562 31,616
player 829 21,252 22,461


**TOTAL** **16,932** **131,611** **153,239**


**G.2** **TriviaQA Dataset**


[The TriviaQA dataset (Joshi et al., 2017a) includes](https://huggingface.co/datasets/mandarjoshi/trivia_qa) _∼_ 130K dataset from Wikipedia and Web.


**Table 7** TriviaQA Dataset Statistics for Llama-3.1-8B


**Entity Type** **Known Count** **Unknown Count** **Total Count**


web 51,862 18,803 76,496
wikipedia 45,138 12,303 61,888


**TOTAL** **97,000** **31,106** **138,384**


**G.3** **PopQA Dataset**


[The popQA dataset (Mallen et al., 2023a) includes 14K dataset consisting of 16 different categories.](https://huggingface.co/datasets/akariasai/PopQA)


**Table 8** PopQA Dataset Statistics for Llama-3.1-8B


**Entity Type** **Known Count** **Unknown Count** **Total Count**


director 397 1,507 1,999
screenwriter 337 1,559 1,999
genre 340 1,168 1,619
producer 170 1,271 1,520
author 350 1,101 1,514
composer 191 747 978
country 499 243 838
capital 508 112 645
placeofbirth 33 542 584
father 165 373 570
sport 136 392 547
occupation 82 433 532
capitalof 214 125 363
religion 71 222 338
mother 46 131 187
color 26 5 34


**TOTAL** **3,565** **9,931** **14,267**


**G.4** **WorldCuisines Dataset**


[We sub-select the English portion (lang="en") of the task1 train data from the WorldCuisines dataset (Winata et al.,](https://huggingface.co/datasets/worldcuisines/vqa)
2024).


32


**Table 9** WorldCuisines-VQA for Qwen-2.5-VL-7B


**Entity Type** **Known Count** **Unknown Count** **Total Count**


WorldCuisines 2281 23,964 27,000

### **H Metrics for Performance and Cluster Separation**


**H.1** **Refusal Rate**


For a model completion c_k in response to an known query, refusal_score(c_k) = 1 if c contains at least one “refusal
substring”; otherwise refusal_score(c_k) = 0. We follow Arditi et al. (2024) to check “Abstain Rate”. Note that the
substring comparison is not sensitive to capitalization, and checks that the phrases are contained anywhere in the
completion, not just at the start. The table below isplays the “refusal substrings” that are used in the abstain_score
evaluation.


**H.2** **Hallucination Rate**


For a model completion c_u in response to an unknown query, hallucination_score(c_u) = 0 if c contains at least one
“abstain substring”; otherwise hallucination_score(c_u) = 1 .


**H.3** **Accuracy**


We define accuracy as the model’s answer with respect to ground truth. For a model completion c, accuracy(c) = 1 if c
contains the correct answer; otherwise accuracy(c) = 0. Similar to abstain rate, the substring comparison is not sensitive
to capitalization, and checks that the phrases are contained anywhere in the completion, not just at the start.


**H.4** **Silhouette Score**


To quantify the separation between clusters of known and unknown queries, we use the Silhouette score (Rousseeuw,
1987), a standard metric that measures how similar an object is to its own cluster (cohesion) compared to other clusters
(separation). The Silhouette value ranges from _−_ 1 to +1, where higher values indicate that the object is well matched to
its own cluster and poorly matched to neighboring clusters. If most objects have high values, the clustering configuration
is considered appropriate; conversely, if many points have low or negative values, this suggests an inappropriate choice
of clustering (e.g., too many or too few clusters).


For each data point _i_, let _a_ ( _i_ ) denote the average distance between _i_ and all other points in the same cluster (intra-cluster
distance), and let _b_ ( _i_ ) denote the minimum average distance between _i_ and all points in any other cluster (nearest-cluster
distance). The Silhouette coefficient for point _i_ is then defined as:


_b_ ( _i_ ) _−_ _a_ ( _i_ )
_s_ ( _i_ ) =
max _{a_ ( _i_ ) _, b_ ( _i_ ) _}_ _[.]_


33


The overall Silhouette score is the mean of _s_ ( _i_ ) across all points:



_S_ = [1]

_N_



_N_

- _s_ ( _i_ ) _,_


_i_ =1



where _N_ is the number of data points. Higher values of _S_ indicate clearer separation between clusters. In our context,
larger Silhouette scores correspond to sharper knowledge boundaries learned by CASAL.


34


### **I Knowledge Probing**

For each input _x ∈D_, we sample _k_ = 10 completions for each query with the following configuration: temperature=0.7,
with nucleus sampling (p=0.8) and top-K sampling (top_ _k_ = 20).


If at least _τ_ = 7 generations are correct, _x_ is labeled as known; if at least _τ_ = 7 are incorrect, it is labeled as unknown.
This procedure yields two disjoint subsets: _Dk_ and _Du_, which are later used for contrastive steering.


We adopt a relatively strict threshold of _τ_ = 7 to ensure high-confidence separation: the model abstains only on
knowledge it does not possess, and responds only when it demonstrates consistent correctness. This choice reduces
ambiguous cases near the decision boundary. We selected _τ_ = 7 empirically, after observing that looser thresholds
(e.g., _τ_ = 5 or _τ_ = 6) produced noisier separations. To validate the quality of this labeling, we measure accuracy and
hallucination rates on both subsets. As expected, the model achieves high accuracy on _Dk_ and very low accuracy on _Du_,
while also exhibiting high hallucination rates on _Du_ . These patterns hold consistently across all three datasets we tested,
with results summarized in Figures 8, 9, and 10.


**Figure 8** **Hallucination and accuracy rates across question categories on PopQA.** (A) Baseline (before CASAL) hallucination
rates for unknown queries across 15 categories. (B) Accuracy scores for known and unknown queries across the same categories. A
strict threshold of _τ_ = 7 was used to label queries, ensuring high-confidence separation: the model answers only when consistently
correct and abstains otherwise. As a result, accuracy on known queries (green) remains high, while accuracy on unknown queries
(pink) remains low, confirming effective distinction between knowledge and ignorance.


35


**Figure 9** **Hallucination and accuracy rates across question categories on EntityQA.** (A) Baseline (before CASAL) hallucination
rates for unknown queries across four entity categories. (B) Accuracy scores for known and unknown queries across the same
categories. With the strict threshold _τ_ = 7, ambiguous cases are filtered out, leading to a sharp separation: accuracy is consistently
high on known queries (green) and remains near-zero on unknown queries (pink).


36


**Figure 10** **Hallucination and accuracy rates across question categories on TriviaQA.** (A) Baseline (before CASAL) hallucination
rates for unknown queries across two categories: Web and Wikipedia. (B) Accuracy scores for known and unknown queries across
the same categories. The strict threshold _τ_ = 7 enforces a conservative decision boundary, accuracy is consistently high on known
queries (green) and remains low on unknown queries (pink).


**I.1** **Knowledge Probing Threshold**


We systematically evaluated different threshold values _τ_ _∈{_ 3 _,_ 4 _,_ 5 _,_ 6 _,_ 7 _,_ 8 _}_ and found that hallucination reduction
performance remains robust across this range. We adopt a relatively strict threshold of _τ_ = 7 to ensure high-confidence
separation: the model abstains only on knowledge it does not possess, and responds only when it demonstrates consistent
correctness. This choice reduces ambiguous cases near the decision boundary.


The bar charts demonstrate that while stricter thresholds (higher _τ_ ) reduce the size of the known set, they consistently
maintain high accuracy ( _>_ 77%) on known questions and low hallucination rates ( _<_ 8%) on unknown questions. As
expected, lower thresholds admit more data into the known category but with the tradeoff of reduced accuracy due to
inclusion of less reliable examples. Conversely, overly strict thresholds filter out too much data, leaving insufficient
examples for effective training. Our choice of _τ_ = 7 strikes an optimal balance between boundary precision and training
data sufficiency, ensuring clean separation while retaining adequate data for robust model training.


37


**Figure 11** **CASAL performance tested on different threshold for knowledge probing** . Each panel shows the classification of
questions into known (green, _≥_ _τ_ /10 correct) and unknown (pink, _≥_ _τ_ /10 wrong) categories, along with the resulting accuracy on
known questions and hallucination rate on unknown questions.

### **J Models**


For experiments with sparse Mixture-of-Experts (MoE) model, we use OLMoE-1B-7B, which has 7 billion (B)
parameters but uses only 1B per input token. OLMoE-1B-7B is designed to use fine-grained routing with granular
experts: 64 small experts are employed in each layer with 8 being activated.


The full list of the models in the paper are detailed in Table 10.

|Model Type|Model Name|Model Size|Link|
|---|---|---|---|
|Dense, text-only|meta-llama/Llama-3.1-8B|8B|HF Link|
|Vision-language|Qwen/Qwen2.5-VL-7B-Instruct|7B|HF Link|
|MoE|allenai/OLMoE-1B-7B-0924-Instruct|7B(total)-1B(ACTIVE)|HF Link|



**Table 10** Diversity of Models Tested on CASAL

### **K Ablation**


Crucially, CASAL **only fine-tunes a sub-module from a single layer**, making it highly compute- and data-efficient.
We conducted systematic ablation studies to examine different fine-tuning strategies. Our results demonstrate that


38


fine-tuning the MLP-down projection layer, the MLP-up projection layer, or the entire MLP (up+down combined) yields
no statistically significant performance differences.


**K.1** **Different sub-modules for training**


**Figure** **12** **Ablation study on MLP sub-module fine-tuning strategies.** (A) Training (CASAL) only the MLP up-projection
layer achieves 88.0% mean accuracy on known samples with 6.9% mean hallucination rate on unknown samples. (B) Training
(CASAL)only the MLP down-projection layer achieves 86.0% mean accuracy on known samples with 3.7% mean hallucination rate
on unknown samples. (C) Training (CASAL) the entire MLP (both up and down projections) achieves mean 88.4% accuracy on
known samples with 2.7% mean hallucination rate on unknown samples. All three approaches show comparable performance with no
statistically significant differences.

### **L Hyper-parameter Search for CASAL Training**


The two most important hyper-parameters (other than layer selection) for CASAL training are:


1. Learning rate. 2. Steering strength ( _α_ ). 3. Steering layer (Refer to Layer Selection Section C.2)


**L.1** **Learning Rate**


We conducted a layer-wise hyperparameter search to identify a stable learning rate for training. As shown in Figure 13,
higher learning rates (e.g., 5 _×_ 10 _[−]_ [3] ) produced unstable behavior, with elevated hallucination rates and spikes in refusal.
In contrast, moderate learning rates (e.g., 1 _×_ 10 _[−]_ [3], 5 _×_ 10 _[−]_ [4], 1 _×_ 10 _[−]_ [4] ) yielded stable and consistent reductions in


39


hallucinations below the baseline (gray stars), while avoiding excessive increases in refusal. Very small learning rates
(e.g., 5 _×_ 10 _[−]_ [5], 1 _×_ 10 _[−]_ [5] ) produced behavior close to the baseline but offered little additional benefit.


Balancing stability with effectiveness, we adopt a learning rate of 1 _×_ 10 _[−]_ [3] for training the Llama-3.1-8B-Instruct model.


**Figure 13** Learning Rate


**Figure 14** **Layer-wise hyperparameter search for learning rate.** (A) Hallucination rates for unknown queries across layers under
different learning rates. (B) Refusal rates for known queries across layers.


**L.2** **Steering Strength**


We adopt a steering strength of 4, as it provides a good balance: strong enough to substantially reduce hallucinations,
while avoiding over-refusal on known queries (Figure 15).


40


**Figure 15** Strength


**Figure 16** **Layer-wise hyperparameter search for steering strength.** (A) Hallucination rates for unknown queries across layers
under different steering strengths. Stronger steering (e.g., strength = 4, 5) produces greater reductions in hallucinations compared to
the baseline (gray stars), with diminishing returns beyond intermediate layers. (B) Refusal rates for known queries across layers.
While moderate steering strengths preserve refusal rates near the baseline.


In conclusion, for training the text-only LLM (llama-3.1-8B-Instruct), we use the following parameters:


   - 1. learning rate (lr) = 1e-3


   - 2. steering layer (L) = 16


   - 3. steering strength ( _α_ ) = 4


   - 4. number of epoch (e) = 3

### **M SFT, DPO and GRPO Training**


_SFT Data construction._ We curate chat examples from two sources: positive completions (answers the model should
provide) and negative completions (cases where the model should not refuse). To ensure label quality, we apply simple
filters:


   - include a negative sample only if its steering-derived refusal score equals 1;


   - include a positive sample only if its refusal score equals 0.


_SFT Training._ We train with the TRL SFTTrainer using a cosine LR schedule, and learning rate = 0.0004. When
enabled, we attach LoRA adapters (rank=8, dropout 0 _._ 05, _α_ = 8).


_DPO Data construction._ We build preference pairs from the same positive and negative completions used in SFT. For
each prompt, we form a tuple _⟨x, y_ [+] _, y_ _[−]_ _⟩_ where:


   - _y_ [+] (preferred response) is drawn from positive completions with refusal score = 0,


   - _y_ _[−]_ (dispreferred response) is drawn from negative completions with refusal score = 1.


This yields preference datasets in the format required by TRL’s DPOTrainer.


41


_DPO Training._ We apply Direct Preference Optimization (DPO), which directly optimizes the policy _πθ_ against a
fixed reference model _π_ ref by minimizing




_[π][θ]_ [(] _[y]_ [+] _[|][x]_ [)] _[π][θ]_ [(] _[y][−][|][x]_ [)]

_π_ ref( _y_ [+] _|x_ ) _[−]_ [log] _π_ ref( _y_ _[−]_ _|x_



_L_ DPO = _−_ E( _x,y_ + _,y−_ )�log _σ_ - _β_ - log _[π][θ]_ [(] _[y]_ [+][+] _[|][x]_ [)]



_π_ _[π]_ ref _[θ]_ [(] ( _[y]_ _y_ _[−][−][|]_ _|_ _[x]_ _x_ [)] ) - [��] _,_



where _β_ controls the strength of preference alignment. Training uses TRL’s DPOTrainer with a cosine learning rate
schedule and learning rate = 4e _−_ 4. When enabled, we attach LoRA adapters (rank = 8, dropout 0 _._ 05, _α_ = 8).

### **N Compute Cost of Calculation (FLOPs per Token)**


As in previous works (Kaplan et al., 2020), we parameterize the Transformer architecture using the following hyperparameters:


   - _n_ layer : number of layers


   - _d_ model : dimension of the residual stream


   - _d_ ff : dimension of the intermediate feed-forward layer


   - _d_ attn : dimension of the attention output


   - _n_ heads : number of attention heads per layer


   - _n_ ctx : number of tokens in the input context


   - _r_ : low rank for parameter-efficient finetuning with LoRA


**N.1** **Full-parameter finetuning**


Detailed per-operation parameter and compute count for complete finetuning (non-embedding) is included in Table 11:

|Operation|Parameters|FLOPs per Token|
|---|---|---|
|Embed|_n_vocab_d_model|—|
|Attention: QKV|_n_layer_d_model3_d_attn|2_n_layer_d_model3_d_attn|
|Attention: Mask|—|2_n_layer_n_ctx_d_attn|
|Attention: Project|_n_layer_d_attn_d_model|2_n_layer_d_attn_d_embd|
|Feedforward|_n_layer2_d_model_d_ff|2_n_layer2_d_model_d_ff|
|De-embed|_n_vocab_d_model|—|
|**Total**|_N_ = 2_d_model_n_layer(2_d_attn +_ d_ff)|_C_forward _≈_2_N_ + 2_n_layer_n_ctx_d_attn|



**Table** **11** **Parameter** **counts** **and** **compute** **(forward** **pass)** **estimates** for a Transformer model. Sub-leading terms such as
nonlinearities, biases, and layer normalization are omitted. Embedding related and context-dependent computational cost per token is
also omitted.



For contexts and models with _d_ model _>_ _[n]_ 12 [ctx] [, the context-dependent computational cost per token is a relatively small]

fraction of the total compute. Following Kaplan et al. (2020), since we primarily study models where _d_ model _>_
_n_ 12ctx [,] [we] [do] [not] [include] [context-dependent] [terms] [in] [our] [training] [compute] [estimate.] [Accounting] [for] [the] [backwards]

pass (approximately twice the compute as the forwards pass), the estimated non-embedding compute as: _C_ full _≈_
6 _N_ floating point operators per training token.


**N.2** **Comparing full-parameter finetune and CASAL finetune**


Crucially, during CASAL training [4], **fine-tuning one single module of a FFN layer is needed** (either up or down
projections) and leaves all other layers frozen, the trainable parameters correspond to one single FFN layer:


4Note that only FLOPs during the stage 3 (casal training stage) are included in the calculation.


42


_N_ CASAL = _d_ model _d_ ff


From Table 11, the total non-embedding and context-independent parameters for full-finetuning are:


_N_ total = 2 _d_ model _n_ layer (2 _d_ attn + _d_ ff)


Thus, the ratio between CASAL parameters and total parameters is:


_N_ CASAL _d_ model _d_ ff _d_ ff

=
_N_ total 2 _d_ model _n_ layer (2 _d_ attn + _d_ ff) [=] 2 _n_ layer (2 _d_ attn + _d_ ff)


_Taking LLaMA-3.1-8B for example:_ _d_ model = _d_ attn = 4096, _d_ ff = 14336, and _n_ layer = 32:


_N_ CASAL 14336

= ( **0** _._ **994** %) _._
_N_ total 2 _×_ 32 _×_ (2 _×_ 4096 + 14336) _[≈]_ [0] _[.]_ [009943]


Therefore, CASAL only uses _∼_ 1% of parameter comparing to full fine-tuning and the advantage of CASAL increases
as the model becomes wider (larger value of _d_ model) and deeper (larger value for _n_ layer)


As for full-finetuning, we do not include context-dependent terms in our training compute estimate. Accounting for the
backwards pass (approximately twice the compute as the forwards pass), the estimated non-embedding compute as:
_C_ CASAL _≈_ 6 _N_ CASAL floating point operators per training token.


Taken together, _C_ CASAL is approximately 1% of _C_ full.


**N.3** **LoRA finetuning**


For a standard linear layer with input dimension _d_ in and output dimension _d_ out, LoRA introduces two smaller matrices
of rank _r_ . For each large dense weight matrix _W_ _∈_ R _[d][in][×][d][out]_ we replace it with two low-rank matrices _A ∈_ R _[d][in][×][r]_

and _B_ _∈_ R _[r][×][d][out]_, so the parameter count becomes _r_ ( _din_ + _dout_ ) instead of _dindout_ . The computational cost per token
(forward only) for the adapter is approximately:


FLOPsLoRA = 2 _r_ ( _d_ in + _d_ out)


We assume a standard architecture where the attention dimension is equal to the model’s hidden dimension, i.e.,
_d_ attn = _d_ model. Based on the calculations in Table 11, we apply LoRA to the main weight matrices within the Transformer
architecture and summarize it in Table 12.

|Operation|Parameters|FLOPs per Token|
|---|---|---|
|Attention: QKV|_n_layer3_r_(_d_attn +_ d_model)|2_n_layer3_r_(_d_attn +_ d_model)|
|Attention: Mask|—|2_n_layer_n_ctx_d_attn|
|Attention: Project|_n_layer_r_(_d_attn +_ d_model)|2_n_layer_r_(_d_attn +_ d_model)|
|Feedforward|_n_layer2_r_(_d_model +_ d_ff)|2_n_layer2_r_(_d_model_d_ff)|
|**Total**|_NLoRA_ = 2_d_model_n_layer_r_(2_d_attn +_ d_ff)|_C_forward _≈_2_NLoRA_ + 2_n_layer_n_ctx_d_attn|



**Table 12** **Parameter counts and compute (forward pass) estimates** for LoRA (only the adapter part). Sub-leading terms such as
nonlinearities, biases, and layer normalization are omitted. The context-dependent computational cost per token is also omitted.


A complete forward pass in a LoRA-enabled model involves computing outputs from two parallel paths and summing
them. The total FLOPs per token is the sum of the costs of these two paths:


   - **Base** **Model** **Forward** **FLOPs:** Based on the provided table ( _C_ forward _≈_ 2 _N_ ), the forward pass cost for the
original model’s non-embedding layers ( _C_ base_forward) is:


_C_ base_forward = _n_ layer _·_ (8 _d_ model _d_ attn + 4 _d_ model _d_ ff) (1)


43


   - **LoRA Adapter Forward FLOPs:** The forward pass cost for the lightweight LoRA adapters ( _C_ lora_forward) is:


_C_ lora_forward = 4 _d_ model _n_ layer _r_ (2 _d_ attn + _d_ ff) (2)


_Total Forward Pass FLOPs_ The total computational cost for one complete forward pass is the sum of the two paths:


_C_ total_forward = _C_ base_forward + _C_ lora_forward (3)


_Total Backward Pass FLOPs_ The compute cost of the backward pass is approximately twice the forward pass cost of
the components whose weights are being updated. In this case, only the LoRA adapters.


_C_ loral_backward _≈_ 2 _· C_ lora_forward


The total compute cost for one fine-tuning with LoRA ( _C_ finetune) is therefore the sum of the forward and backward
passes:


_C_ LoRA = _C_ total_forward + _C_ lora_backward
= ( _C_ base_forward + _C_ lora_forward) + (2 _· C_ lora_forward)

_C_ LoRA = _C_ base_forward + 3 _· C_ lora_forward (4)


**N.4** **Comparing full-parameter finetune and LoRA finetune**


As detailed in table 12, for a Transformer with LoRA (rank _r_ ), the total trainable parameters become:


_N_ LoRA = _n_ layer [3 _r_ ( _d_ model + _d_ attn) + _r_ ( _d_ attn + _d_ model) + 2 _r_ ( _d_ model + _d_ ff)]

(5)
= 2 _d_ model _n_ layer _r_ (2 _d_ attn + _d_ ff)


The ratio of LoRA parameters to the full parameter count is:



_N_ LoRA

= [2] _[d]_ [model] _[n]_ [layer] _[r]_ [(2] _[d]_ [attn][ +] _[ d]_ [ff][)]
_N_ total 2 _d_ model _n_ layer (2 _d_ attn + _d_ ff)



_N_ LoRA



(6)
2 _d_ model _n_ layer (2 _d_ attn + _d_ ff)



_N_ LoRA



_N_ LoRA

= [4] _[r]_ [(] _[d]_ [model][ +] _[ d]_ [attn][) + 2] _[r]_ [(] _[d]_ [model][ +] _[ d]_ [ff][)]
_N_ total 2 _d_ model (2 _d_ attn + _d_ ff)



(7)
2 _d_ model (2 _d_ attn + _d_ ff)



For GPT-style models (including llama-3.1-8b used in the paper) where _d_ model = _d_ attn and _d_ ff _≈_ 4 _d_ model:



_N_ LoRA



LoRA

= [4] _[r]_ [(2] _[d]_ [model][) + 2] _[r]_ [(5] _[d]_ [model][)]
_N_ total 2 _d_ model(6 _d_ model)



2 _d_ model(6 _d_ model)



= [8] _[rd]_ [model][ + 10] _[rd]_ [model]

12 _d_ [2] model



(8)



18 _r_
=
12 _d_ model

3 _r_
=
2 _d_ model


_Taking LLaMA-3.1-8B for example:_ With _d_ model = 4096 and _r_ = 8:



_N_ LoRA _≈_ 3 _×_ 8 ( **0** _._ **29** %) (9)

_N_ total 2 _×_ 4096 _[≈]_ [0] _[.]_ [00293]


_Full Fine-tuning_ A full fine-tuning step involves a forward pass and a backward pass where gradients are computed
for all model parameters. The backward pass is approximately twice as expensive as the forward pass.


_C_ Full _≈_ _C_ base_forward + (2 _· C_ base_forward) = 3 _· C_ base_forward (10)


44


_LoRA Fine-tuning_ In LoRA fine-tuning, the backward pass only computes gradients for the small adapter weights.


_C_ LoRA = _C_ base_forward + 3 _· C_ lora_forward (11)


where _C_ base_forward is the FLOPs for the base model’s forward pass and _C_ lora_forward is the FLOPs for the LoRA adapter’s
forward pass.


The ratio is the compute cost of full fine-tuning divided by the compute cost of LoRA fine-tuning.


3 _· C_ base_forward

Ratio = _[C]_ [Full] = _≈_ **3** (12)

_C_ LoRA _C_ base_forward + 3 _· C_ lora_forward


Since the term 3 _·_ _C_ lora_forward is much smaller than _C_ base_forward ( _C_ lora_forward is only 0 _._ 29% of _C_ base_forward ), which brings
the overall ratio close to 3. Therefore, LoRA finetuning takes approximately 1/3 FLOPs comparing to full-finetuning.
Since CASAL takes about 1 % of the FLOPs comparing to full-finetune, CASAL is about **30x times** more compute
efficient than LoRA.


45


### **O Multimodal Model**

**O.1** **Example Question and Answers from Vision-Language Model**


**Figure 17** Example Known Image # 1


46


**Figure 18** Example Known Image # 2

### **After CASAL Training:** **Example Known Question #1**


 - **Query:** _How do locals in Germany call this dish?_


 - **Qwen/Qwen2.5-VL-7B-Instruct; Generation #1:** The dish in the picture is a "Bratwurst", which is a
type of grilled sausage that is popular in Germany. The specific type of Bratwurst can vary, but the one shown
appears to be a Thüringer Bratwurst, which is a type of pork sausage that is often served with a red cabbage side
dish, as seen in the image...


 - **Qwen/Qwen2.5-VL-7B-Instruct; Generation #2:** The dish in the picture appears to be a variation of
"Bratwurst," a popular German dish consisting of grilled sausages. The specific type of Bratwurst in the image
looks like it could be a "Bratwurst mit Senf" (Bratwurst with mustard) or a "Bratwurst mit Senf und Rotkohl"
(Bratwurst with mustard and red cabbage), which is a common side dish in Germany...


 - **Qwen/Qwen2.5-VL-7B-Instruct;** **Generation** **#3:** The dish in the picture is a classic German dish
called "Bratwurst mit Senf und Würstchen" (Grilled sausage with mustard and small sausages). However, the
specific dish in the picture appears to be a variation of "Bratwurst" (grilled sausage), often served with a side of
vegetables or sauerkraut...


 - **Qwen/Qwen2.5-VL-7B-Instruct; Generation #4:** The dish in the picture is called "Bratwurst mit Senf
und Käse" (Grilled sausage with mustard and cheese) in Germany. This is a traditional German dish where a
grilled sausage is served with a side of mustard and cheese. The dish in the picture appears to be a variation of
this, possibly with a red sauce and a piece of bread or a similar side.


 - **Qwen/Qwen2.5-VL-7B-Instruct; Generation #5:** The dish in the picture appears to be a type of bratwurst,
which is a German sausage. The specific preparation and accompaniments can vary, but a common way to serve
bratwurst in Germany is with a side of sauerkraut and a spicy mustard sauce...47


 - **Qwen/Qwen2.5-VL-7B-Instruct;** **Generation** **#6:** The dish in the picture is called "Bratwurst mit
Rotkohl," which translates to "grilled sausage with red cabbage" in English. This is a traditional German dish
th t i l j d i ll d i ld th Th d bb i t i ll té d ith i


48


**O.2** **Known and unknown separation**


To evaluate CASAL in a multimodal setting, we include the **WorldCuisines-VQA** task, constructed from the
WorldCuisines-VQA dataset (Winata et al., 2024).Each example consists of a query–image pair ( _q, I_ ). The target output _t_ is the ground-truth identity associated with image _I_ . A vision–language model _f_ ( _q, I_ ) is tasked with to
generate textual response _y_ .


Similar to the text-only case, for each input ( _q, I_ ), we sample _k_ = 10 generations _{y_ ˆ1 _, . . .,_ ˆ _y_ 10 _}_ from _f_ ( _q, I_ ). Let _c_ (ˆ _yi_ )
be an indicator function for correctness with respect to the ground-truth label _y_ . We then define the confidence score as



_s_ ( _q, I_ ) =



_k_

- _c_ (ˆ _yi_ ) _._


_i_ =1



Using threshold _τ_ = 7, we label


( _q, I_ ) _∈Dk_ if _s_ ( _q, I_ ) _≥_ _τ,_ ( _q, I_ ) _∈Du_ if _s_ ( _q, I_ ) _≤_ _k −_ _τ,_


where _Dk_ and _Du_ denote the subsets of known and unknown images, respectively.


**O.3** **Steering procedure**


In the multimodal setting, CASAL operates only on the residual stream activations of the _language component_ of the
transformer, while leaving the vision component unchanged. Contrastive steering directions are derived from _Dk_ and
_Du_ in the same manner as for the text-only model. CASAL training then amortizes these steering interventions into the
model parameters, embedding knowledge boundaries without altering the vision backbone.


**O.4** **CASAL Training Procedure**


For training the vision-language LLM (qwen-2.5-VL-7B-Instruct), we use the following parameters:


   - 1. learning rate (lr) = 5e-4


   - 2. steering layer (L) = 18


   - 3. steering strength ( _α_ ) = 6


   - 4. number of epochs (e) = 5

### **P Mixture-of-Experts (MoE) Training**


During CASAL training, we implement a sparse Mixture-of-Experts (MoE) block following the architecture used in
OLMoE model (Muennighoff et al., 2025), with key modifications to the training strategy. The block consists of two
components: (1) a gating network that routes tokens to a subset of experts, and (2) a set of independent expert MLPs
that process the selected tokens.


_Expert MLPs._ Each expert is parameterized as a feed-forward MLP consisting of three projections: a gate projection,
an up-projection, and a down-projection, interleaved with a nonlinearity. Formally, given hidden states _x_ _∈_ R _[d]_, the
expert output is
_f_ expert( _x_ ) = _W_ down� _σ_ ( _W_ gate _x_ ) _⊙_ ( _W_ up _x_ )� _,_


where _σ_ denotes the activation function. Depending on the training configuration, we selectively freeze certain projections: - experts: only train _W_ up _, W_ down (freeze _W_ gate). - experts-down: only train _W_ down. - experts-mlp:
only train _W_ up.


49


_Sparse Routing._ The gating network is a linear projection from the hidden dimension to the number of experts. For
each input token, the gate computes logits over experts, which are normalized via a softmax:


_p_ = softmax( _W_ gate _h_ ) _,_


where _h_ denotes token hidden states. Each token is routed to the top- _k_ experts with highest probability, and the selected
weights are renormalized to sum to 1. This ensures a convex mixture over the selected experts. **Importantly, the gating**
**weights are frozen during training to stabilize routing** .


_Forward Computation._ The forward pass of the MoE block proceeds in four stages:


1. **Routing.** Compute expert probabilities _p_ and select top- _k_ experts for each token.


2. **Masking.** Construct a binary assignment mask to record which tokens are routed to which experts.


3. **Expert** **Processing.** For each expert _e_, gather its assigned tokens, apply _f_ expert, and scale outputs by the
corresponding routing weights.


4. **Aggregation.** Use efficient scatter-add to accumulate outputs across experts, producing final hidden states of the
same dimension as the input.


_Pseudocode._ The forward computation for MoE is summarized in Algorithm 2.


**Algorithm 2** Sparse Mixture-of-Experts Forward Pass

**Require:** hidden states _H_ _∈_ R _[B][×][T][ ×][d]_, gating weights _W_ gate, experts _{fe}_ _[E]_ _e_ =1
1: _H_ _←_ reshape( _H, B · T, d_ )
2: _P_ _←_ softmax( _HW_ gate _[⊤]_ [)] _▷_ Routing probabilities
3: ( _P_ top _, E_ sel) _←_ topk( _P, k_ ) _▷_ Select top- _k_ experts per token
4: _P_ top _←_ _P_ top _/_ [�] _P_ top _▷_ Normalize
5: Initialize _H_ out _←_ 0

6: **for** expert _e_ = 1 _. . . E_ **do**
7: Find tokens _Te_ = _{i_ : _e ∈_ _E_ sel[ _i_ ] _}_
8: _he_ _←_ _fe_ ( _H_ [ _Te_ ]) _⊙_ _P_ top[ _Te_ ]
9: _H_ out[ _Te_ ] += _he_
10: **end for**

11: **return** reshape( _H_ out _, B, T, d_ )


_Training._ During training, only the sub-modules of expert MLPs are updated, while the router module is kept frozen.
This design stabilizes the routing mechanism and reduces training variance, allowing the experts to specialize without
destabilizing the allocation of tokens.


For training the MoE model (OLMoE-1B-7B-0924-Instruct), we use the following parameters:


   - 1. learning rate (lr) = 1e-3


   - 2. steering layer (L) = 10


   - 3. steering strength ( _α_ ) = 4


   - 4. number of epoch (e) = 3


50


**P.1** **PCA Activations Across Experts**


Layer 2

|Col1|Col2|
|---|---|
|||


|7|Col2|Col3|
|---|---|---|
||||
||||



Expert 16 Expert 17 Expert 18 Expert 19 Expert 20 Expert 21 Exp ~~ert 22~~ Expert 23


Expert 24 Expert 25 Expert 26 Expert 27 Expert 28 Expert 29 Expert 30 Expert 31


Expert 32 Expert 33 Expert 34 Expert 35 Expert 36 Expert 37 Expert 38 Expert 39


Expert 40 Expert 41 Expert 42 Expert 43 Expert 44 Expert 45 Expert 46 Expert 47


Expert 48 Expert 49 Expert 50 Expert 51 Expert 52 Expert 53 Expert 54 Expert 55


Expert 56 Expert 57 Expert 58 Expert 59 Expert 60 Expert 61 Expert 62 Expert 63


**Figure 19** PCA Activation Across Experts at Layer 2 of OLMoE Model


51


Layer 8

|Exp|ert|1|
|---|---|---|
||||



Expert 8 Expert 9 ~~Expert 10~~ Expert 11 Expert 12 Expert 13 Expert 14 Expert 15

|Col1|Col2|Col3|
|---|---|---|
||||


|Col1|Col2|
|---|---|
|||



Expert 24 Expert 25 Expert 26 Expert 27 Expert 28 Expert 29 Expert 30 Expert 31


Expert 32 Expert 33 Expert 34 Expert 35 Expert 36 Expert 37 Expert 38 Expert 39


Expert 40 Expert 41 Expert 42 Expert 43 Expert 44 Expert 45 Expert 46 Expert 47


Expert 48 Expert 49 Expert 50 Expert 51 Expert 52 Expert 53 Expert 54 Expert 55


Expert 56 Expert 57 Expert 58 Expert 59 Expert 60 Expert 61 Expert 62 Expert 63


**Figure 20** PCA Activation Across Experts at Layer 8 of OLMoE Model


52


Layer 14


Expert 0 Expert 1 ~~Expert 2~~ ~~Expert 3~~ Expert 4 Expert 5 Expert 6 Expert 7


~~Expert 8~~ ~~Expert 9~~ Expert 10 E ~~xpert 11~~ Ex ~~pert 12~~ Exp ~~ert 13~~ Expert 14 Expert 15


Expert 16 Expert 17 Expert 18 Expert 19 Expert 20 Expert 21 Expert 22 Expert 23


~~Expert 24~~ Expert 25 Expert 26 Expert 27 Expert 28 Expert 29 Expert 30 Expert 31


Expert 32 Expert 33 Expert 34 Expert 35 Expert 36 Expert 37 Expert 38 Expert 39


Expert 40 Expert 41 Expert 42 Expert 43 Expert 44 Expert 45 Expert 46 Expert 47


Expert 48 Expert 49 Expert 50 Expert 51 Expert 52 Expert 53 Expert 54 Expert 55


Expert 56 Expert 57 Expert 58 Expert 59 Expert 60 Expert 61 Expert 62 Expert 63


**Figure 21** PCA Activation Across Experts at Layer 14 of OLMoE Model

### **Q PCA Activations After Different Training Methods**


We performed PCA on the hidden layer activations to compare decision boundaries between DPO, SFT, GRPO, and
CASAL. Consistent with our hypothesis, CASAL demonstrates the best cluster separation and the clearest boundary
between known and unknown queries compared to the other methods. This validates that by directly training a local
representation loss, CASAL effectively encourages a distinct separation between these activation states.


53


**Figure 22** PCA Activations After different methods.



54


### **R Computational Requirements**

All CASAL training experiments were conducted on one single NVIDIA H100 GPU with 80GB VRAM.Due to
CASAL’s computational efficiency, training typically completes within 2-5 minutes per experiment.

### **S The Use of Large Language Models**


Large language models (specifically GPT5, Claude Sonnet 4, Gemini 2.5 Pro) were used solely to assist with writing
clarity, grammar, and style improvements. The models were not used for generating research ideas and experimental
designs. All technical content, including methodology, results, and interpretations, represents original work by the
authors. Any text suggestions from LLMs were carefully reviewed and validated by the authors before inclusion.


55


