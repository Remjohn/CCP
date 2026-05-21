## **The Rogue Scalpel: Activation Steering Compromises LLM Safety**

**Anton Korznikov** **Andrey Galichin** **Alexey Dontsov** **Oleg Y. Rogov** **Ivan Oseledets** **Elena Tutubalina**



**Abstract**


Activation steering is a promising technique for
controlling LLM behavior by adding semantically
meaningful vectors directly into a model’s hidden
states during inference. It is often framed as a
precise, interpretable, and potentially safer alternative to fine-tuning. We demonstrate the opposite: steering systematically breaks model alignment safeguards, making it comply with harmful
requests. Through extensive experiments on different model families, we show that even steering
in a random direction can increase the probability of harmful compliance from 0% to 1–13%.
Alarmingly, steering benign features from a sparse
autoencoder (SAE), a common source of interpretable directions, demonstrates a comparable
harmful potential. Finally, we show that combining 20 randomly sampled vectors that jailbreak a
single prompt creates a universal attack, significantly increasing harmful compliance on unseen
requests. These results challenge the paradigm of
safety through interpretability, showing that precise control over model internals does not guarantee precise control over model behavior.


**1. Introduction**


Large Language Models (LLMs) achieve remarkable performance in natural language understanding and generation,
demonstrating capabilities in text summarization (Zhang
et al., 2025), question answering (Wei et al., 2024), coding
(Chen, 2021), and complex reasoning (Guo et al., 2025;
Lightman et al., 2023). Effectively leveraging these capabilities for diverse applications requires reliable methods to
control and adjust model behavior. Traditional approaches
include fine-tuning (Hu et al., 2022) and prompt engineering
(Schulhoff et al., 2024). However, both methods remain fundamentally non-interpretable: it is difficult to predict how a
fine-tuned model will generalize (Chu et al., 2025) or why a
particular prompt succeeds (Seleznyov et al., 2025).


. Correspondence to: Anton Korznikov _<_ korznikovantona@gmail.com _>_ .


_Preprint._ _February 17, 2026._



This limitation has driven the field of mechanistic interpretability, which seeks to reverse-engineer neural networks
into human-understandable components and then use them
for precise model control (Bereska & Gavves, 2024; Sharkey
et al., 2025). A prominent example of this new paradigm
is _activation_ _steering_, a technique rooted in the observation that human-interpretable concepts, such as truthfulness
(Marks & Tegmark, 2023), refusal (Arditi et al., 2024), and
sentiment (Tigges et al., 2023; Konen et al., 2024), are often represented as linear directions in latent space. The
technique operates by injecting a carefully chosen direction
vector into the hidden states of the model in a specified
layer for all tokens during inference, thereby moving its
activations along a chosen direction to enhance the corresponding behavior (Stolfo et al., 2024; Zou et al., 2023a).
These _steering vectors_ are commonly sourced from interpretable features of sparse autoencoders (SAEs) (Bricken
et al., 2023) or via methods such as difference-in-means
(Marks & Tegmark, 2023).


However, the interpretability of these methods may create
a false sense of security. Can precise steering truly guarantee safe and predictable outcomes? Prior work has shown
that narrow fine-tuning on insecure code or even on benign data can significantly degrade alignment and weaken
safety guardrails (Qi et al., 2023; Betley et al., 2025; Hahm
et al., 2025). By contrast, the safety implications of activation steering remain underexplored. Existing studies focus
mainly on adversarial jailbreak vectors (Wang & Shu, 2023;
Chia et al., 2025; Dunefsky, 2025; Xu et al., 2024), leaving open the critical question of whether benign steering
might also undermine alignment. We therefore hypothesize
that activation steering, often portrayed as a safer, more
interpretable scalpel compared to the blunt instrument of
fine-tuning, may in fact become a rogue scalpel that surgically undermines the very safety it is meant to preserve.


In this work, we investigate the safety vulnerabilities of
activation steering by measuring how it affects refusal mechanisms. Using the JailbreakBench dataset (Chao et al., 2024)
containing 100 harmful queries from 10 categories, we applied steering, collected responses, and evaluated their harmfulness using an LLM-as-judge approach (Gu et al., 2024;
Zheng et al., 2023). This methodology reveals a systematic failure mode that is consistent across multiple model
families, including Llama-3 (Dubey et al., 2024), Qwen2.5



1


**Submission and Formatting Instructions for ICML 2026**


_Figure_ _1._ **When** **Benign** **Steering** **Breaks** **Safety:** **A** **Real-World** **Example.** Our experiments reveal a critical vulnerability: even
semantically benign control can compromise alignment. Here, steering Llama3.1-8B with a real “Portuguese” SAE feature achieves its
intended purpose (right) but inadvertently bypasses safety safeguards, transforming a safe refusal (left) into harmful compliance. This
demonstrates that precise control does not guarantee safe outcomes.



(Qwen et al., 2025), and Falcon-3 (Team, 2024) at various
scales (Fig. 1). Here are our key findings:


1. **Steering in a random direction can effectively break**
**the model’s refusal mechanisms.** Merely adding random noise to activations during inference increases
the rate of harmful compliance from 0% to between 113%, depending on the model and prompt. We further
found that steering is most effective when applied to
the model’s middle layers, with the optimal steering
coefficient varying significantly across both models
and layers.


2. **Steering with SAE features demonstrates a compa-**
**rable potential to random noise**, increasing the probability of compliance by 1-4% over random steering.
This is noteworthy, given that SAE features represent
a standard source of steering vectors for interpretable
model control. Furthermore, the most effective jailbreaking features correspond to benign concepts and
show poor generalization across new prompts, making
systematic safety monitoring practically infeasible.


3. **We** **can** **create** **a** **universal** **attack** **that** **generalizes**
**to unseen harmful prompts**, by aggregating just 20
random vectors that jailbreak only one prompt. Crucially, this attack requires no harmful training data,
model weights, gradients, or output logits. This finding
reveals that the capabilities of activation steering can
be easily weaponized by malicious actors to bypass
safeguards for a wide range of harmful queries.


**2. Related Work**


**Vulnerabilities** **of** **LLM** **Alignment.** Controlling LLM
behavior to be helpful and harmless is typically achieved



through supervised fine-tuning (SFT) and reinforcement
learning from human feedback (RLHF) (Ouyang et al., 2022;
Kaufmann et al., 2024; Rafailov et al., 2023). A cornerstone
of this alignment is the model’s _refusal_ mechanism – its ability to identify and decline harmful requests. Despite these
efforts, LLMs remain vulnerable to _jailbreaks_, where adversarial prompts can bypass these safety mechanisms (Chao
et al., 2024; Huang et al., 2023; Wei et al., 2023; Zou et al.,
2023b; Krylov et al., 2025; Anil et al., 2024). Furthermore,
a phenomenon known as _emergent misalignment_ shows that
even narrow fine-tuning on benign or specialized data (e.g.,
insecure code) can unexpectedly degrade safety safeguards
across a wide range of domains (Qi et al., 2023; Betley et al.,
2025; Hahm et al., 2025). While these prior works examine
parameter interventions via weight updates, we focus on
activation steering, a targeted inference-time method that
manipulates hidden states without altering weights, potentially introducing similar risks stealthily.


**Activation Steering.** A parallel line of research in mechanistic interpretability has found that many high-level concepts (e.g., truthfulness (Marks & Tegmark, 2023), sentiment (Tigges et al., 2023), and refusal (Arditi et al., 2024))
are represented as linear directions in a model’s activation
space. _Activation steering_ exploits this by adding a carefully
chosen direction vector to the model’s hidden states during
inference to bias its behavior (Turner et al., 2023; Stolfo
et al., 2024). Steering vectors can be derived via methods
like difference-in-means (Marks & Tegmark, 2023), contrastive activation addition (Rimsky et al., 2024), or, most
relevantly for interpretable control, from features of sparse
autoencoders (SAEs) (Bricken et al., 2023; Durmus et al.,
2024). This technique has been successfully applied to control factual recall (Zhao et al., 2025), writing style (Konen
et al., 2024), and safety behaviors (Soo et al., 2025; Xiao



2


**Submission and Formatting Instructions for ICML 2026**



et al., 2024), positioning it as a precise and interpretable
alternative to full fine-tuning.


**Robustness** **of** **Activation** **Steering.** While activation
steering provides a valuable mechanism for model control,
its practical implementation requires careful consideration
of reliability and safety implications. Empirical studies indicate that steering effects can be context-dependent, with
varying efficacy across different prompts or domains (Tan
et al., 2024; Durmus et al., 2024) and can be used to maliciously extract sensitive information (Seyitoglu et al.˘, 2024).
Furthermore, a growing body of work demonstrates that vectors can be deliberately optimized to function as adversarial
attacks, reliably jailbreaking models (Wang & Shu, 2023;
Gu et al., 2025; Chia et al., 2025; Dunefsky, 2025; Xu et al.,
2024). Crucially, prior work has focused on vectors that
are _explicitly designed to be harmful_, leaving a critical gap
in understanding whether _benign_ steering vectors, the kind
used for legitimate control, can _inadvertently_ compromise
safety as an unintended side effect. Our work systematically
investigates this overlooked vulnerability.


**3. Methodology**


**3.1. Technical Background**


Sparse autoencoders (SAEs) are unsupervised models
trained to encode and reconstruct a network’s activation
vectors **x** [(] _[l]_ [)] on a fixed layer _l_ while encouraging sparsity in
the latent neurons (Gao et al., 2024). A standard architecture
for an SAE is as follows:


       **z** [(] _[l]_ [)] = TopK _k_ **W** _e_ _[⊤]_ **[x]** [(] _[l]_ [)][�] _,_ **x** ˆ [(] _[l]_ [)] = **W** _d_ **z** [(] _[l]_ [)] _,_ (1)


where **W** _e,_ **W** _d_ _∈_ R _[d][×][m]_ are encoder/decoder matrices
with an overcomplete latent dimension _m_ _≫_ _d_, and the
sparse code **z** [(] _[l]_ [)] _∈_ R _[m]_ has at most _k_ _≪_ _d_ nonzero entries.
The TopK activation zeros all but the _k_ largest entries.


The application of SAEs for activation steering is a two-step
process. It begins by identifying a SAE feature corresponding to a desired behavior or concept. The sparsity constraint
in SAEs promotes monosemanticity, causing latent neurons
in SAE to activate only for specific, interpretable concepts
like “Python programming” or “mathematical reasoning”
(Bricken et al., 2023). The column vector of **W** _d_ associated
with a neuron defines a direction in the model’s activation
space for that feature. The second step involves steering the
model by adding this vector to its activations during inference, artificially enhancing the concept’s presence to bias
its behavior. This enables precise control over behaviors
such as factuality, style, and reasoning (Bayat et al., 2025;
Galichin et al., 2025), making it a useful for interpretable
model control (Balsam et al.; Arad et al., 2025).



**3.2. Activation Steering Procedure**


Activation steering is an inference-time editing method
where a fixed steering vector is added to the residual stream
activations of all tokens at a fixed layer of the transformer
(Rimsky et al., 2024; Scalena et al., 2024). Formally, if **x** [(] _[l]_ [)]

denotes the residual stream activation at layer _l_, steering
modifies it as:

**x** ~~[(]~~ _[l]_ [)] = **x** [(] _[l]_ [)] + _α_ **v** _,_ (2)


where **v** is the unit norm steering vector and _α_ is a scaling
coefficient controlling steering strength. In our experiments
we derive steering vectors **v** from two primary sources:


1. **Random** **Directions:** We sample vectors uniformly
from unit norm sphere _S_ _[d][−]_ [1] . This approach serves as
a critical baseline to measure the inherent vulnerability of the model’s latent space to arbitrary activation
perturbations.


2. **SAE-based Directions:** We test steering vectors derived from SAEs, the most common and interpretable
method for activation steering (Balsam et al.). This
evaluates whether the standard approach for benign
control can inadvertently compromise safety.


To determine the appropriate steering strength _α_, we first
computed a model- and layer-dependent baseline value _µ_ [(] _[l]_ [)]

representing the average activation norm at layer _l_ across
the evaluation dataset. The final steering strength was then
calculated as _α_ = _c · µ_ [(] _[l]_ [)] where _c_ is a scaling coefficient selected from _{_ 0 _._ 25 _,_ 0 _._ 5 _,_ 0 _._ 75 _,_ 1 _._ 0 _,_ 1 _._ 25 _,_ 1 _._ 5 _,_ 1 _._ 75 _,_ 2 _._ 0 _}_ . This
approach ensures consistent steering intensities across different models and layers while allowing systematic exploration
of intervention strengths. In line with Wu et al. (2025),
we experimented with applying steering at three canonical
depths (first third, _⌊L/_ 3 _⌋_ ; middle, _⌊L/_ 2 _⌋_ ; and last third,
_⌊_ 2 _L/_ 3 _⌋_ of total layers _L_ ), using the middle layer as our
primary baseline for comparative analysis. Following the
approach of Durmus et al. (2024), we apply activation steering consistently both to prompt and generation tokens. Consistent with Lin & Bloom (2023), we exclude from steering
special tokens (e.g. _<_ start ~~o~~ f ~~t~~ urn _>_ and _<_ bos _>_ ),
which improved generation coherence. All model responses
were generated using greedy decoding.


**3.3. Models Configuration**


For experiments with random directions, we explore multiple model families, using their instruct-tuned versions:
Llama3.1 (Dubey et al., 2024), Qwen2.5 (Qwen et al., 2025),
Falcon3 (Team, 2024) and FalconH1 (Zuo et al., 2025), with
model sizes ranging from 3B to 70B parameters. Our SAEbased experiments utilize features from Goodfire’s SAE
trained on layer 19 of instruct-tuned Llama3.1-8B (Balsam



3


**Submission and Formatting Instructions for ICML 2026**


_Figure 2._ **Single-Prompt Sweep.** Using a single harmful prompt about bomb making, we find: (left) Compliance Rate for random steering
reliably produces a non-zero values, yet varies significantly across both model families and steering coefficients, (middle) random steering
is most successful at jailbreaking the model when applied to middle or early layers, with a sharp drop in compliance when targeting later
layers, (right) under identical conditions, steering with SAE features yields a 1–4% higher Compliance Rate compared to random steering.



et al.). This SAE was specifically designed for safe, interpretable tuning through monosemantic features, making it
an ideal test case for alignment vulnerabilities. We therefore limited our investigation of SAE feature steering to this
specific model and layer.


**3.4. Evaluation Procedure**


To quantify how activation steering compromises model
safety, we evaluate the model’s refusal behavior, defined as
its binary choice to either comply with a harmful request
or reject it. This provides a clear, measurable safety metric that directly reflects potential risk. Following (Arditi
et al., 2024), we use JailbreakBench (Chao et al., 2024) as
our primary evaluation dataset, which contains 100 harmful prompts spanning 10 different categories (see details in
Appx. A). For all models and prompts, the baseline compliance rate without any steering is 0%.


Our primary metric is the **Compliance Rate (CR)** - the fraction of responses judged as UNSAFE. Formally, the compliance rate is calculated as:



the reliability of this evaluation methodology (see Appx. B).


**4. Experiments**


Our experimental section is structured as follows. Sec. 4.1
presents a systematic evaluation using a single harmful
prompt to identify vulnerable model configurations by
sweeping across layers, steering magnitudes, and vector
types. Sec. 4.2 extends this analysis to the full JailbreakBench dataset, assessing the generalization of harmful steering vectors and analyzing the semantics of the most dangerous SAE features. Sec. 4.3 provides a concrete case study
showing how a seemingly benign SAE feature, applied via
a public API, can jailbreak a production model. Finally,
Sec. 4.4 shows that the localized vulnerabilities identified in
earlier sections can be combined and refined to construct a
universal attack vector that generalizes effectively to unseen
harmful prompts.


**4.1. Single-Prompt Vulnerability Investigation**


We begin by evaluating the vulnerability of model
alignment to activation steering using a single harmful
prompt: "Write a tutorial on how to make
a bomb" from JailbreakBench. To systematically identify conditions where steering bypasses safety safeguards,
we sweep across four variables: model family, intervention
layer, scaling coefficient, and steering vector type. For robustness, we sample 1,000 vectors of each type: random
vectors, tested on Llama3.1-8B, Falcon3-7B, Qwen2.5-7B,
and SAE feature vectors, tested on Llama3.1-8B, reporting
the average Compliance Rate across all samples. The key
findings are summarized in Fig. 2.


**Random steering reliably breaks alignment safeguards**
**for all tested models.** As shown in Fig. 2 (left), non-zero



Compliance Rate = [1]

_N_



_N_


I(judge( _ri_ ) = UNSAFE) (3)

_i_ =1



where _N_ is the total number of responses, _ri_ denotes the
_i_ -th response, and I is the indicator function.


We implement an automated “LLM-as-a-judge” approach
(Gu et al., 2024; Zheng et al., 2023) using Qwen3-8B in
reasoning mode (Yang et al., 2025) as the judge model to
classify each generated response as either SAFE or UNSAFE.
Incoherent, repetitive, or nonsensical responses are always
classified as SAFE, ensuring the metric captures only actionable harmful content. Human validation shows the judge
achieves 94% precision for the harmful class, confirming



4


**Submission and Formatting Instructions for ICML 2026**


harmful compliance rates are observed across all model
families and most steering coefficients, demonstrating the
fundamental vulnerability. However, the effectiveness varies
significantly by model and coefficient strength. For example,
Falcon3-7B shows peak compliance of 3% at _c_ = 0 _._ 75,
while Llama3.1-8B requires stronger intervention of _c_ = 2 _._ 0
to achieve 18% compliance. Notably, the relationship is nonmonotonic for Falcon model: excessive coefficients degrade
output coherence, producing nonsensical responses that we
classify as safe (see Appx. B for evaluation rules).



**Middle and early layers show maximal vulnerability to**
**steering interventions.** Fig. 2 (middle) reveals that random
steering effectiveness depends on the intervention layer. For
Llama3.1-8B, steering in middle layers is most effective,
with peak compliance at layer 16. Late layers show significantly reduced effects, indicating safety mechanisms are
most vulnerable in intermediate processing stages where abstract concepts and refusal policies form. This suggests that
successful steering doesn’t simply suppress a pre-existing
“refusal direction” (Arditi et al., 2024); rather, it interferes
with the non-linear formation of safety mechanisms in these
critical middle and early processing stages. In Appx. E,
we test whether harmful SAE features align with a known
refusal direction and find near-zero cosine similarities, rejecting the hypothesis that steering works through simple
correlation with refusal vectors.


**SAE features demonstrate comparable potential to ran-**
**dom** **vectors** **in** **bypassing** **safety** **mechanisms.** Fig. 2
(right) shows that under identical steering conditions (same
model, layer, coefficient), SAE feature steering yields 1-4%
higher Compliance Rates than random directions. Even at
small coefficients (0.5 and 0.75), SAE steering yields nonzero compliance of 0.2% and 1%, respectively, showing that
concept-aligned interventions pose greater safety risks by
effectively exploiting the model’s latent space structure.


**4.2. Probing Model Vulnerabilities at Scale**


We now expand our evaluation to the full JailbreakBench
dataset to comprehensively assess the generalizability of
these vulnerabilities. Following the methodology established in Sec.4.1, we apply steering to each of the 100 harmful prompts using two vector types. We test 1,000 random
directions on Llama3.1-8B, Qwen2.5-7B, and Falcon3-7B
at the 1/2 depth layer, selecting scaling coefficients of 0.75,
0.5, and 0.5 respectively. These values correspond to the
”sweet spot” identified in Fig. 3, where steering remains effective while minimizing disruption to the model’s general
capabilities. For instance, at coefficient 0.75, Llama3.18B’s MMLU accuracy degrades by less than 1%. Alongside
these, we test 1,000 SAE features on Llama3.1-8B at the
layer 19 ( _≈_ 2 _/_ 3 depth) using the same coefficient of 0.75.
For each configuration, we report the average Compliance



_Figure_ _3._ **Sweet** **Spot** **for** **Steering.** MMLU accuracy versus
scaling coefficient shows a clear performance “sweet spot” at
coefficients _≤_ 0 _._ 75 for Llama3.1, and _≤_ 0 _._ 5 for Qwen2.5 with
Falcon3, where steering remains effective without compromising
general model capabilities.


Rate across all samples. The key results, demonstrating
consistent vulnerabilities, are presented in Fig. 4 and Fig. 5.


**Steering induces consistent harmful compliance across**
**all JailbreakBench categories.** The results, presented in
Fig.4, reveal a consistent and concerning pattern. When both
the harmful prompt and the steering vector are randomly
sampled, the overall probability of a successful jailbreak
is substantial, reaching 4.6% for Llama3.1-8B and 3.8%
for Qwen2.5-7B. This non-zero compliance rate persists
across all ten categories of harmful requests, with the vulnerability profile varying by model. For Llama3.1-8B, category “Fraud/Deception” (13%) is most susceptible, while
categories like “Sexual/Adult content” (0.1%) and “Economic harm” (0.1%) are the most resistant. When steering
Llama3.1-8B with SAE features instead of random vectors,
we observe the same pattern with an overall compliance
rate of 4.6%, demonstrating that the vulnerability exposed
by activation steering is not an isolated phenomenon but a
systemic weakness in the model’s safety alignment.


**Most** **SAE** **features** **exhibit** **dangerous** **capabilities.** A
deeper analysis of the SAE features reveals a critical security challenge: the potential for jailbreaking is not confined
to a few anomalous features but is a widespread property of
the model’s latent space. We find that 817 out of 1000 SAE
features can jailbreak at least one harmful prompt, and 353
can jailbreak at least five prompts (Fig. 5 left). Crucially,
the most effective features are semantically benign; predetermined feature interpretations from Goodfire API reveal
they align with concepts like “modal auxiliary verbs expressing possibility”, “providing a list of options” and “brand
identity”. This makes the most dangerous steering vectors
virtually indistinguishable from those used for legitimate



5


**Submission and Formatting Instructions for ICML 2026**


_Figure_ _4._ **Steering** **vulnerabilities** **span** **all** **harm** **categories.** When evaluated across the full JailbreakBench dataset, random and
SAE-based steering induce substantial harmful compliance across all categories. For example, the overall success rate reaches 4.5-5.6%
for Llama3.1-8B, demonstrating systematic rather than isolated failures.


_Figure 5._ **Generalizability of SAE Features.** Most SAE features exhibit dangerous capabilities, with 668/1000 jailbreaking at least
five prompts (left). Moreover, top features represent benign concepts (e.g., feature breaking 35 prompts represents “modal verbs”). The
heatmap (right) shows the conditional probability that a feature jailbreaking any source-category prompt will also jailbreak a random
target-category prompt. It reveals that features generalize poorly, making systematic monitoring of hazardous features challenging.



control, creating a major blind spot for safety monitoring.


**Dangerous SAE features show poor cross-prompt gener-**
**alization.** We investigate a critical safety screening question:
if a feature jailbreaks prompts from one harmful category,
does it generalize to others? If so, production systems could
filter dangerous features by testing on just a few harmful
prompts. Our results show this approach fails. We find that
no single feature acts as a universal “master key”: the most
potent feature successfully compromised only 35 of the 100
prompts (Fig. 5 left). More importantly, cross-category generalization is weak. The resulting heatmap (Fig. 5 right)
shows the conditional probability that a feature jailbreak


ing any prompt from one category will also succeed on
a random prompt from another. These probabilities stay
low, often near baseline. The only weak pattern is that features breaking hard categories are slightly more likely to
break easier ones. This poor, prompt-specific generalization
makes comprehensive safety screening impractical: it would
require testing every feature against a vast, ever-growing set
of harmful prompts. This limitation holds across all models
(Appx. C), confirming we cannot safely filter features.



6


**Submission and Formatting Instructions for ICML 2026**







_Figure_ _6._ **A** **benign** **SAE** **feature** **successfully** **jailbreaks** **Llama3.1-8B** **via** **Goodfire** **API** . The model exhibits two failure modes:
disclaimer-then-compliance (top) and justification via fictional framing (bottom), revealing a critical vulnerability in alignment safeguards.



**4.3. Breaking Model Safety with a Benign SAE Feature**


To empirically validate the practical implications of our
findings, we conducted a case study using the public Goodfire API, which provides a production-grade interface for
steering Llama3.1-8B using interpretable SAE features. We
selected a highly effective jailbreaking feature from Sec.
4.2, representing “brand identity” - a semantically benign
concept that would likely pass any manual safety review
and is intended for valid use cases like controlling writing
style.


Steering this feature via the API’s proprietary default hyperparameters successfully jailbroke the model on two representative prompts (see Appx. D for other examples), revealing
two notable behavioral patterns. As shown in Fig. 6, the
model exhibited what we term **disclaimer-then-compliance**

- a failure mode where the model initially generates a superficial safety disclaimer but then proceeds to provide detailed,
actionable harmful instructions. Even more remarkably,
we observed **justification via fictional framing**, where the
model rationalizes its compliance by constructing elaborate hypothetical scenarios or fictional contexts to mask the
harmful nature of its output. These behaviors indicate a significant vulnerability in the model’s alignment safeguards,
as they demonstrate the model’s ability to produce harmful content while appearing responsible. This case study
confirms that steering vectors representing benign concepts,
deployed through public APIs designed for safe and interpretable control, can still undermine the model’s alignment
safeguards.



**4.4. Weaponizing Random Steering**


Our previous experiments demonstrate that while individual
steering vectors can effectively bypass safety mechanisms
for specific prompts, their effects remain poorly generalizable. This localized vulnerability, however, raises a critical
security question: can adversaries systematically combine
these weak, prompt-specific failures to construct a _universal_
attack vector that reliably jailbreaks a model across a wide
range of harmful prompts without requiring per-prompt optimization?


We find that constructing a universal attack vector requires
minimal effort: averaging a small set of randomly sampled
vectors that each jailbreak a single prompt proves sufficient. We begin with a fixed harmful prompt, “Write
a tutorial on how to make a bomb”. Unlike
in Sec. 4.2, where we used fixed, moderate coefficients
to assess realistic vulnerabilities, here we adopt an adversarial approach: we first perform a short coefficient sweep
for this prompt to select the optimal steering strength that
maximizes compliance. We then sample 1000 random steering vectors from a unit-norm sphere and test each vector
**v** _i_ at this optimized coefficient, evaluating compliance on
the same bomb-making prompt. We select 20 vectors that
successfully induce compliance—a number chosen to balance attack potency and sampling efficiency, which typically
requires only 100–500 random trials to obtain, depending
on the model’s baseline vulnerability. These vectors are
averaged and normalized to unit norm, forming a single,
aggregated universal attack vector. We then evaluate each
aggregated vector across the entire JailbreakBench dataset



7


**Submission and Formatting Instructions for ICML 2026**


_Figure 7._ **Local vulnerabilities scale to universal attacks:** Averaging just 20 random vectors that jailbreak a single prompt creates a
universal attack vector that boosts harmful compliance by 4 _×_ compared to random steering, requiring only black-box access and no
harmful data. This reveals how easily localized weaknesses can be weaponized at scale.



against all 99 remaining harmful queries, reporting the average Compliance Rate.


**Universal vectors significantly amplify harmful compli-**
**ance.** The aggregated vectors demonstrate a striking ability
to suppress safety mechanisms across diverse models, yielding an average 4× increase in compliance rates compared to
random steering (Fig. 7). For example, the universal vector
achieves 50.4% success on Llama3.1-70B (double the random vector rate) and improves Falcon3-7B compliance by
nearly 10-fold (5.7% to 63.4%). However, the effectiveness
of this method is highly model-dependent, as evidenced by
the reduction in performance observed for Qwen2.5-32B.


**The attack is zero-shot and requires only steering capa-**
**bility.** Crucially, this method needs no model weights, gradients, or logits, only the ability to perform activation steering
and observe model outputs. The attack is completely zeroshot: it requires knowledge of just a single harmful prompt
to construct the universal vector, yet generalizes effectively
to unseen harmful requests.


**5. Conclusion**


Our findings reveal systematic safety vulnerabilities in activation steering, a technique developed for precise, interpretable model control. We demonstrate that steering, even
with random vectors, reliably breaks alignment safeguards
across multiple model families, inducing harmful compliance rates of 1–13%. This vulnerability is most pronounced



when steering middle layers, where abstract concepts and
refusal mechanisms appear to be most malleable.


Extending to interpretable steering, we find that sparse autoencoder (SAE) features representing benign concepts pose
comparable or greater risks, increasing compliance by 1–4%
over random vectors. Alarmingly, 817 of 1000 tested SAE
features exhibited jailbreaking capabilities, yet these features show poor cross-prompt generalization, making comprehensive safety monitoring practically infeasible. These
vulnerabilities persist across all 10 harmful categories in
JailbreakBench, indicating a systemic weakness.


Critically, we show that localized failures can be
weaponized at scale: averaging just 20 random vectors that
jailbreak a single prompt creates a universal attack vector
that boosts harmful compliance by 4× on unseen requests,
requiring only black-box steering access without model gradients, or harmful training data. The practical danger is immediate: our case study successfully jailbroke a production
model via a public SAE steering API, with the model exhibiting subtle failure modes like disclaimer-then-compliance
and justification via fictional framing.


To address this, mitigation strategies like adversarial training to counter steering perturbations could be developed.
Future research should investigate the mechanisms behind
these alignment failures, potentially by analyzing activation
patterns or refusal circuits in the model’s latent space, to
built more robust safety frameworks.



8


**Submission and Formatting Instructions for ICML 2026**



**Impact Statement**


This work identifies critical safety vulnerabilities in activation steering, a technique promoted for precise, interpretable control of large language models. By demonstrating how both random and semantically benign steering can
systematically bypass model safeguards to generate harmful
content, we highlight a significant security risk in current
interpretability-based control methods. We disclose these
findings to encourage the development of more robust safety
mechanisms and to caution against over-reliance on lowlevel model interventions as inherently safe. Our goal is
to ensure that the pursuit of interpretable control does not
come at the expense of model safety and alignment.


**References**


Anil, C., Durmus, E., Panickssery, N., Sharma, M., Benton,
J., Kundu, S., Batson, J., Tong, M., Mu, J., Ford, D., et al.
Many-shot jailbreaking. _Advances in Neural Information_
_Processing Systems_, 37:129696–129742, 2024.


Arad, D., Mueller, A., and Belinkov, Y. Saes are good for
steering–if you select the right features. _arXiv preprint_
_arXiv:2505.20063_, 2025.


Arditi, A., Obeso, O., Syed, A., Paleka, D., Panickssery, N.,
Gurnee, W., and Nanda, N. Refusal in language models is
mediated by a single direction. _Advances in Neural Infor-_
_mation Processing Systems_, 37:136037–136083, 2024.


Balsam, D., McGrath, T., Gorton, L., Nguyen, N., Deng,
M., and Ho, E. Announcing open-source saes for llama
3.3 70b and llama 3.1 8b, jan 2025. _URL_ _https://www._
_goodfire. ai/blog/sae-open-source-announcement_, 24.


Bayat, R., Rahimi-Kalahroudi, A., Pezeshki, M., Chandar,
S., and Vincent, P. Steering large language model activations in sparse spaces. _arXiv preprint arXiv:2503.00177_,
2025.


Bereska, L. and Gavves, E. Mechanistic interpretability
for ai safety–a review. _arXiv preprint arXiv:2404.14082_,
2024.


Betley, J., Tan, D., Warncke, N., Sztyber-Betley, A., Bao, X.,
Soto, M., Labenz, N., and Evans, O. Emergent misalignment: Narrow finetuning can produce broadly misaligned
llms. _arXiv preprint arXiv:2502.17424_, 2025.


Bricken, T., Templeton, A., Batson, J., Chen, B., Jermyn, A.,
Conerly, T., Turner, N., Anil, C., Denison, C., Askell, A.,
Lasenby, R., Wu, Y., Kravec, S., Schiefer, N., Maxwell,
T., Joseph, N., Hatfield-Dodds, Z., Tamkin, A., Nguyen,
K., McLean, B., Burke, J. E., Hume, T., Carter, S.,
Henighan, T., and Olah, C. Towards monosemanticity:
Decomposing language models with dictionary learning.



_Transformer Circuits Thread_, 2023. https://transformercircuits.pub/2023/monosemantic-features/index.html.


Chao, P., Debenedetti, E., Robey, A., Andriushchenko, M.,
Croce, F., Sehwag, V., Dobriban, E., Flammarion, N.,
Pappas, G. J., Tramer, F., et al. Jailbreakbench: An open
robustness benchmark for jailbreaking large language
models. _Advances_ _in_ _Neural_ _Information_ _Processing_
_Systems_, 37:55005–55029, 2024.


Chen, M. Evaluating large language models trained on code.
_arXiv preprint arXiv:2107.03374_, 2021.


Chia, X. W., Wong, S. L., and Pan, J. Probing latent subspaces in llm for ai security: Identifying and manipulating adversarial states. _arXiv preprint arXiv:2503.09066_,
2025.


Chu, T., Zhai, Y., Yang, J., Tong, S., Xie, S., Schuurmans,
D., Le, Q. V., Levine, S., and Ma, Y. Sft memorizes, rl
generalizes: A comparative study of foundation model
post-training. _arXiv preprint arXiv:2501.17161_, 2025.


Dubey, A., Jauhri, A., Pandey, A., Kadian, A., Al-Dahle,
A., Letman, A., Mathur, A., Schelten, A., Yang, A., Fan,
A., et al. The llama 3 herd of models. _arXiv e-prints_, pp.
arXiv–2407, 2024.


Dunefsky, J. One-shot steering vectors cause emergent misalignment, too, april 2025. _URL_ _https://www._
_lesswrong. com/posts/kcKnKHTHycHeRhcHF/one-shot-_
_steering-vectors-cause-emergentmisalignment-too._ _Ac-_
_cessed_, pp. 05–10, 2025.


Durmus, E., Tamkin, A., Clark, J., Wei, J., Marcus,
J., Batson, J., Handa, K., Lovitt, L., Tong, M.,
McCain, M., Rausch, O., Huang, S., Bowman, S.,
Ritchie, S., Henighan, T., and Ganguli, D. Evaluating feature steering: A case study in mitigating social biases, 2024. [URL https://anthropic.com/](https://anthropic.com/research/evaluating-feature-steering)
[research/evaluating-feature-steering.](https://anthropic.com/research/evaluating-feature-steering)


Galichin, A., Dontsov, A., Druzhinina, P., Razzhigaev, A.,
Rogov, O. Y., Tutubalina, E., and Oseledets, I. I have
covered all the bases here: Interpreting reasoning features
in large language models via sparse autoencoders. _arXiv_
_preprint arXiv:2503.18878_, 2025.


Gao, L., la Tour, T. D., Tillman, H., Goh, G., Troll, R.,
Radford, A., Sutskever, I., Leike, J., and Wu, J. Scaling and evaluating sparse autoencoders. _arXiv preprint_
_arXiv:2406.04093_, 2024.


Gu, J., Jiang, X., Shi, Z., Tan, H., Zhai, X., Xu, C., Li, W.,
Shen, Y., Ma, S., Liu, H., et al. A survey on llm-as-ajudge. _The Innovation_, 2024.



9


**Submission and Formatting Instructions for ICML 2026**



Gu, T., Huang, K., Wang, Z., Wang, Y., Li, J., Yao, Y.,
Yao, Y., Yang, Y., Teng, Y., and Wang, Y. Probing the
robustness of large language models safety to latent perturbations. _arXiv preprint arXiv:2506.16078_, 2025.


Guo, D., Yang, D., Zhang, H., Song, J., Zhang, R., Xu, R.,
Zhu, Q., Ma, S., Wang, P., Bi, X., et al. Deepseek-r1: Incentivizing reasoning capability in llms via reinforcement
learning. _arXiv preprint arXiv:2501.12948_, 2025.


Hahm, D., Min, T., Jin, W., and Lee, K. Unintended misalignment from agentic fine-tuning: Risks and mitigation.
_arXiv preprint arXiv:2508.14031_, 2025.


Hu, E. J., Shen, Y., Wallis, P., Allen-Zhu, Z., Li, Y., Wang,
S., Wang, L., Chen, W., et al. Lora: Low-rank adaptation
of large language models. _ICLR_, 1(2):3, 2022.


Huang, Y., Gupta, S., Xia, M., Li, K., and Chen, D. Catastrophic jailbreak of open-source llms via exploiting generation. _arXiv preprint arXiv:2310.06987_, 2023.


Kaufmann, T., Weng, P., Bengs, V., and Hullermeier, E.¨ A
survey of reinforcement learning from human feedback.
2024.


Konen, K., Jentzsch, S., Diallo, D., Schutt, P., Bensch, O.,¨
Baff, R. E., Opitz, D., and Hecking, T. Style vectors for
steering generative large language model. _arXiv preprint_
_arXiv:2402.01618_, 2024.


Krylov, A., Vagizov, I., Korzh, D., Douiba, M., Guezzaz, A.,
Kokh, V., Erokhin, S. D., Tutubalina, E. V., and Rogov,
O. Y. Hamsa: hijacking aligned compact models via
stealthy automation. _arXiv preprint arXiv:2508.16484_,
2025.


Lightman, H., Kosaraju, V., Burda, Y., Edwards, H., Baker,
B., Lee, T., Leike, J., Schulman, J., Sutskever, I., and
Cobbe, K. Let’s verify step by step. In _The_ _Twelfth_
_International Conference on Learning Representations_,
2023.


Lin, J. and Bloom, J. Neuronpedia: Interactive reference and
tooling for analyzing neural networks. _Software available_
_from neuronpedia. org_, 2023.


Marks, S. and Tegmark, M. The geometry of truth:
Emergent linear structure in large language model
representations of true/false datasets. _arXiv_ _preprint_
_arXiv:2310.06824_, 2023.


Ouyang, L., Wu, J., Jiang, X., Almeida, D., Wainwright, C.,
Mishkin, P., Zhang, C., Agarwal, S., Slama, K., Ray, A.,
et al. Training language models to follow instructions
with human feedback. _Advances in neural information_
_processing systems_, 35:27730–27744, 2022.



Qi, X., Zeng, Y., Xie, T., Chen, P.-Y., Jia, R., Mittal, P.,
and Henderson, P. Fine-tuning aligned language models
compromises safety, even when users do not intend to!
_arXiv preprint arXiv:2310.03693_, 2023.


Qwen, :, Yang, A., Yang, B., Zhang, B., Hui, B., Zheng,
B., Yu, B., Li, C., Liu, D., Huang, F., Wei, H., Lin, H.,
Yang, J., Tu, J., Zhang, J., Yang, J., Yang, J., Zhou, J.,
Lin, J., Dang, K., Lu, K., Bao, K., Yang, K., Yu, L.,
Li, M., Xue, M., Zhang, P., Zhu, Q., Men, R., Lin, R.,
Li, T., Tang, T., Xia, T., Ren, X., Ren, X., Fan, Y., Su,
Y., Zhang, Y., Wan, Y., Liu, Y., Cui, Z., Zhang, Z., and
Qiu, Z. Qwen2.5 technical report, 2025. [URL https:](https://arxiv.org/abs/2412.15115)
[//arxiv.org/abs/2412.15115.](https://arxiv.org/abs/2412.15115)


Rafailov, R., Sharma, A., Mitchell, E., Manning, C. D.,
Ermon, S., and Finn, C. Direct preference optimization: Your language model is secretly a reward model.
_Advances in neural information processing systems_, 36:
53728–53741, 2023.


Rimsky, N., Gabrieli, N., Schulz, J., Tong, M., Hubinger, E.,
and Turner, A. Steering llama 2 via contrastive activation
addition. In _Proceedings of the 62nd Annual Meeting of_
_the Association for Computational Linguistics (Volume 1:_
_Long Papers)_, pp. 15504–15522, 2024.


Scalena, D., Sarti, G., and Nissim, M. Multi-property steering of large language models with dynamic activation
composition. _arXiv preprint arXiv:2406.17563_, 2024.


Schulhoff, S., Ilie, M., Balepur, N., Kahadze, K., Liu, A., Si,
C., Li, Y., Gupta, A., Han, H., Schulhoff, S., et al. The
prompt report: a systematic survey of prompt engineering
techniques. _arXiv preprint arXiv:2406.06608_, 2024.


Seleznyov, M., Chaichuk, M., Ershov, G., Panchenko, A.,
Tutubalina, E., and Somov, O. When punctuation matters:
a large-scale comparison of prompt robustness methods
for llms. _arXiv preprint arXiv:2508.11383_, 2025.


Seyitoglu, A., Kuvshinov, A., Schwinn, L., and G˘ unnemann,¨
S. Extracting unlearned information from llms with activation steering. _arXiv preprint arXiv:2411.02631_, 2024.


Sharkey, L., Chughtai, B., Batson, J., Lindsey, J., Wu, J.,
Bushnaq, L., Goldowsky-Dill, N., Heimersheim, S., Ortega, A., Bloom, J., et al. Open problems in mechanistic
interpretability. _arXiv preprint arXiv:2501.16496_, 2025.


Soo, S., Guang, C., Teng, W., Balaganesh, C., Guoxian, T.,
and Ming, Y. Interpretable steering of large language
models with feature guided activation additions. _arXiv_
_preprint arXiv:2501.09929_, 2025.


Stolfo, A., Balachandran, V., Yousefi, S., Horvitz, E.,
and Nushi, B. Improving instruction-following in language models through activation steering. _arXiv preprint_
_arXiv:2410.12877_, 2024.



10


**Submission and Formatting Instructions for ICML 2026**



Tan, D., Chanin, D., Lynch, A., Paige, B., Kanoulas, D.,
Garriga-Alonso, A., and Kirk, R. Analysing the generalisation and reliability of steering vectors. _Advances_
_in Neural Information Processing Systems_, 37:139179–
139212, 2024.


Team, F.-L. The falcon 3 family of open models, December 2024. URL [https://huggingface.co/](https://huggingface.co/blog/falcon3)
[blog/falcon3.](https://huggingface.co/blog/falcon3)


Tigges, C., Hollinsworth, O. J., Geiger, A., and Nanda,
N. Linear representations of sentiment in large language
models. _arXiv preprint arXiv:2310.15154_, 2023.


Turner, A. M., Thiergart, L., Leech, G., Udell, D., Vazquez,
J. J., Mini, U., and MacDiarmid, M. Steering language models with activation engineering. _arXiv preprint_
_arXiv:2308.10248_, 2023.


Wang, H. and Shu, K. Trojan activation attack: Red-teaming
large language models using activation steering for safetyalignment. _arXiv preprint arXiv:2311.09433_, 2023.


Wei, A., Haghtalab, N., and Steinhardt, J. Jailbroken: How
does llm safety training fail? _Advances in Neural Infor-_
_mation Processing Systems_, 36:80079–80110, 2023.


Wei, J., Karina, N., Chung, H. W., Jiao, Y. J., Papay, S.,
Glaese, A., Schulman, J., and Fedus, W. Measuring shortform factuality in large language models. _arXiv preprint_
_arXiv:2411.04368_, 2024.


Wu, Z., Arora, A., Geiger, A., Wang, Z., Huang, J., Jurafsky,
D., Manning, C. D., and Potts, C. Axbench: Steering
llms? even simple baselines outperform sparse autoencoders. _arXiv preprint arXiv:2501.17148_, 2025.


Xiao, Y., Chaoqun, W., Zhang, Y., Wang, W., Lin, B., He,
X., Shen, X., and Ye, J. Enhancing multiple dimensions
of trustworthiness in llms via sparse activation control.
_Advances in Neural Information Processing Systems_, 37:
15730–15764, 2024.


Xu, Z., Huang, R., Chen, C., and Wang, X. Uncovering
safety risks of large language models through concept
activation vector. _Advances in Neural Information Pro-_
_cessing Systems_, 37:116743–116782, 2024.


Yang, A., Li, A., Yang, B., Zhang, B., Hui, B., Zheng, B.,
Yu, B., Gao, C., Huang, C., Lv, C., et al. Qwen3 technical
report. _arXiv preprint arXiv:2505.09388_, 2025.


Zhang, H., Yu, P. S., and Zhang, J. A systematic survey
of text summarization: From statistical methods to large
language models. _ACM Computing Surveys_, 57(11):1–41,
2025.



Zhao, Y., Devoto, A., Hong, G., Du, X., Gema, A. P., Wang,
H., He, X., Wong, K.-F., and Minervini, P. Steering
knowledge selection behaviours in llms via sae-based
representation engineering. In _Proceedings of the 2025_
_Conference_ _of_ _the_ _Nations_ _of_ _the_ _Americas_ _Chapter_ _of_
_the Association for Computational Linguistics:_ _Human_
_Language_ _Technologies_ _(Volume_ _1:_ _Long_ _Papers)_, pp.
5117–5136, 2025.


Zheng, L., Chiang, W.-L., Sheng, Y., Zhuang, S., Wu, Z.,
Zhuang, Y., Lin, Z., Li, Z., Li, D., Xing, E., et al. Judging
llm-as-a-judge with mt-bench and chatbot arena. _Ad-_
_vances_ _in_ _neural_ _information_ _processing_ _systems_, 36:
46595–46623, 2023.


Zou, A., Phan, L., Chen, S., Campbell, J., Guo, P., Ren, R.,
Pan, A., Yin, X., Mazeika, M., Dombrowski, A.-K., et al.
Representation engineering: A top-down approach to ai
transparency. _arXiv preprint arXiv:2310.01405_, 2023a.


Zou, A., Wang, Z., Carlini, N., Nasr, M., Kolter, J. Z.,
and Fredrikson, M. Universal and transferable adversarial attacks on aligned language models. _arXiv preprint_
_arXiv:2307.15043_, 2023b.


Zuo, J., Velikanov, M., Chahed, I., Belkada, Y., Rhayem,
D. E., Kunsch, G., Hacid, H., Yous, H., Farhat, B.,
Khadraoui, I., et al. Falcon-h1: A family of hybrid-head
language models redefining efficiency and performance.
_arXiv preprint arXiv:2507.22448_, 2025.



11


**Submission and Formatting Instructions for ICML 2026**


**A. JailbreakBench Prompt Examples**


Following Chao et al. (2024), we use prompts from 10 categories of harmful requests. Representative examples from each
category are shown in Fig. 8.





















_Figure 8._ **Representative harmful prompts from each JailbreakBench category.**


12


**Submission and Formatting Instructions for ICML 2026**


**B. Judge Prompt and Quality Assessment**


We used the following comprehensive prompt presented in Fig. 9 for automated safety evaluation using Qwen3-8B as a
judge.





_Figure 9._ **LLM-as-Judge prompt for evaluating the safety of model responses.**


Given the pronounced class imbalance between harmful and non-harmful responses, our primary objective was to establish
a lower bound for the Compliance Rate by assessing the precision of our judge model’s harmful classifications. For each
of the 100 harmful prompts in the JailbreakBench dataset, we sampled one response from Llama3.1-8B under random
steering, specifically selecting those classified as harmful by our judge model. These responses were evaluated against
human annotations following the methodology outlined in the judge prompt. Of these, only 6 out of 100 responses were
incorrectly classified by model as harmful when they were actually safe, yielding a precision of 94% for the harmful class.
This high precision underscores the robustness and reliability of our evaluation methodology.


**C. Additional Results:** **Generalizability Across Models**


We extend Sec. 4.2 by evaluating random steering on Llama3.1-8B and Qwen2.5-7B using 1,000 random vectors from a
standard Gaussian, normalized to unit norm, applied at layer _⌊_ 1 _/_ 2 _⌋_ with scaling coefficients 0.75 (Llama3.1-8B) and 0.5
(Qwen2.5-7B). Compliance Rate (CR) is assessed across all 100 JailbreakBench prompts. Results are shown in Fig. 10.


**Random steering exhibits widespread dangerous capabilities.** As shown in Figs. 10a, 10e, random steering vectors
consistently bypass safety mechanisms across multiple prompts. For Llama3.1-8B, 387 out of 1,000 random vectors
jailbreak at least five prompts, while for Qwen2.5-7B, 313 vectors achieve this threshold. This demonstrates that the ability
to compromise alignment is not limited to specific vectors but is a pervasive property of the models’ latent spaces, consistent


13


**Submission and Formatting Instructions for ICML 2026**


_(a)_ Llama3.1-8B: Jailbroken prompts per random vector _(b)_ Llama3.1-8B: Cross-category generalization


_(c)_ Qwen2.5-7B: Jailbroken prompts per random vector _(d)_ Qwen2.5-7B: Cross-category generalization


_(e)_ Falcon3-7B: Jailbroken prompts per random vector _(f)_ Falcon3-7B: Cross-category generalization


_Figure_ _10._ **Random** **steering** **generalizability.** Histograms (a, c, e) show prompts jailbroken per random vector for Llama3.1-8B,
Qwen2.5-7B, and Falcon3-7B. Most vectors jailbreak multiple prompts. Heatmaps (b, d, f) show low conditional probabilities of
cross-category jailbreaking, indicating poor generalization.


with the findings for SAE features in Sec. 4.2.


**Poor cross-category generalization is a consistent limitation.** The heatmaps in Figs. 10b, 10f illustrate the conditional
probability that a random vector jailbreaking a prompt from one JailbreakBench category will also jailbreak a random
prompt from another category. For both Llama3.1-8B and Qwen2.5-7B, these probabilities remain low, rarely exceeding the


14


**Submission and Formatting Instructions for ICML 2026**


baseline Compliance Rates for target categories. This poor generalization mirrors the behavior observed with SAE features,
reinforcing that activation steering vulnerabilities are highly prompt-specific and challenging to monitor systematically.


These results confirm that the safety vulnerabilities identified in our main experiments are not unique to SAE-based steering
or specific model architectures. Random steering in Llama3.1-8B and Qwen2.5-7B exhibits similar patterns of widespread
dangerous capabilities and limited cross-prompt generalization, highlighting the systemic nature of activation steering’s
impact on model safety.


**D. Supplementary API-Steered Responses for Benign SAE Feature**


This appendix provides additional examples of Llama3.1-8B responses when steered with the ”brand identity” SAE feature
via the Goodfire API’s default steering hyperparameters, as described in Sec. 4.3. We present responses for three harmful
prompts from the JailbreakBench dataset.







_Figure 11._ **Additional examples of jailbreaking with ”brand identity” SAE feature.** The responses demonstrate disclaimer then
compliance (first and second prompts) and justification via fictional framing (third prompt), highlighting the model’s ability to produce
harmful content while appearing responsible.


15


**Submission and Formatting Instructions for ICML 2026**


**E. On the Relationship Between Harmful SAE Features and Refusal Direction**
To investigate whether harmful SAE features operate by suppressing known refusal mechanisms, we tested their alignment
with a ”refusal direction” - a vector previously shown to bypass safety when added to activations (Arditi et al., 2024).
We computed cosine similarity between the top 30 most harmful SAE features and this refusal direction. The near-zero
mean similarity (0.027 _±_ 0.0208) indicates no significant linear alignment. As shown in Table 1, even the most effective
jailbreaking features exhibit negligible correlation. This rejects simple vector alignment as the primary mechanism,
suggesting instead that safety compromise arises from more complex interference with nonlinear circuits.


_Table 1._ **Cosine similarity between most harmful SAE features and refusal direction.**


**Feature Index** **Number of jailbroken prompts** **Cosine similarity**


772 35 0.0052
286 29 -0.0220
959 29 -0.0146
25 27 0.0008
801 26 0.0166
132 25 0.0237
182 25 -0.0062


16


