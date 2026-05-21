## Limits of n -gram Style Control for LLMs via Logit-Space Injection

Sami-ul Ahmed
University of Colorado Boulder
```
               ahmed.samiul.h@gmail.com

```

**Abstract**


Large language models (LLMs) are typically personalized via prompt engineering or parameterefficient fine-tuning such as LoRA. However, writing style can be difficult to distill into a single
prompt, and LoRA fine-tuning requires computationally intensive training and infrastructure. We
investigate a possible lightweight alternative: steering a frozen LLM with _n_ -gram style priors injected in logit space at decoding time. We train an _n_ -gram model on stylistically distinct corpora –
including Don Quixote, CNN/DailyMail news headlines, and arXiv abstracts - constructing an interpolated 1-to-3-gram prior over next-token probabilities. During generation we modify the LLM’s
logits by adding a weighted sum of style log-probabilities from each _n_ -gram order that matches the
current context, scaled by a control parameter _λ ∈_ [0 _,_ 1].
We sweep _λ_ and style corpora and report style perplexity under the _n_ -gram model, base-model
perplexity as a proxy for fluency, Jensen–Shannon (JS) divergence between the original and steered
token distributions, and token-overlap statistics. On TinyLlama-1.1B we identify a single narrow
regime (for the _Don_ _Quixote_ corpus at _λ_ = 0 _._ 1) where style perplexity improves by 24 _._ 7% and basemodel perplexity improves by 51 _._ 4% relative to the frozen model. Outside this regime, and for multiauthor corpora such as CNN/DailyMail and arXiv abstracts, even small nonzero _λ_ values generally
result in worse style and fluency, and larger _λ_ values lead to collapse with extreme perplexities
and incoherent text. Logit-space injection of _n_ -gram style priors provides lightweight, tunable style
control, but it is fragile: it operates effectively only within a narrow range of low _λ_ values and
is consistently outperformed by prompting and LoRA. Prompting alone yields significant stylistic
alignment while also substantially improving base-model perplexity, whereas LoRA is the most
reliable and effective method overall.


_Keywords:_ Large Language Models, Controlled Text Generation, _n_ -gram Language Models,
Logit-Space Injection, Style Control, Decoding-Time Steering, LoRA Fine-Tuning


**1.** **Introduction**


LLMs are widely used for writing tasks where we care not just about correctness but also about
style, such as matching a user’s tone, vocabulary, and syntactic habits. Today, this is usually
handled by fine-tuning models on specific data or writing prompts that describe the target style.
Fine-tuning introduces extra parameters, infrastructure, and privacy concerns while prompting can
be brittle and hard to control quantitatively. Therefore, we pose the question: Is there a lightweight,
at-decoding method to steer style without training the base model?
_n_ -gram models have been used in related work, learning token-by-token from a corpus to predict
the next token from the _n −_ 1 tokens before it. We define a style prior: an _n_ -gram model trained


using the target language model’s tokenizer on a body of text. The style prior is used to tell us:
based on these past _n −_ 1 tokens, what is most likely to come next under the target corpus.
In this work we explore a third option: using a style prior to steer LLM outputs in logit space:
the multidimensional vector space containing the raw prediction scores for the next token before
they are converted into probabilities. We train a small _n_ -gram model on a corpus with a distinct
style and use it to bias the LLM’s logits before softmax. This leaves the LLM frozen and offers a
single scalar knob _λ_ to increase the strength with which the logits are being modified. This method
requires no computationally expensive training as it leaves the base model untouched.
Similar methods have been explored in the past. Messner & Lippincott (2025) [1] use _n_ -gram
models to select dialect-specific subword realizations, which they used to generate text in the style
of AAVE. Plug-and-Play Language Models (PPLM) apply gradients from an attribute classifier to
the hidden state of a frozen LM to control sentiment or topic at inference time [2]. Other work
such as DeRa and PAD integrate reward-model scores during decoding to control alignment [3, 4].
In many of these cases, control is achieved through neural critics trained on supervised preference
data. In contrast, we investigate a purely non-parametric steering signal based on _n_ -gram statistics
extracted from a style corpus, and we study the effects of increasing the strength of the style prior
on text generations.
Selected corpora include _Don_ _Quixote_, CNN/DailyMail headlines, and arXiv abstracts. Each
of these offers a distinct style for us to attempt to emulate. If a corpus is too large to reasonably
compute _n_ -grams on, we train our model on a randomly sampled portion of it. We train our _n_ -gram
style prior using 1-, 2-, and 3-grams.
We sweep across _λ_ values and style corpora and evaluate performance with style perplexity
under an _n_ -gram LM, base-model perplexity as a proxy for fluency, JS divergence, and token-overlap
metrics. We compare these generations with prompt-only generation and LoRA fine-tuning.
We find that simple prompting works surprisingly well, sharply improving style alignment and
fluency. LoRA aligns incredibly well to style while substantially improving fluency. Logit-space
steering is tunable but fragile. Small _λ_ values yield minor style improvements on certain corpora
but increasing _λ_ does not improve style alignment. Increasing _λ_ above a certain threshold (around
_λ ≈_ 0 _._ 6) leads to collapse of model fluency; larger values of _λ_ fail to improve the model’s adherence
to the target style. Using sampling during inference reveals brittleness in the method, as some
unlikely or incoherent tokens become boosted. At high _λ_ values, generations under both sampling
and greedy decoding often become incoherent or fall into repetitive loops.
Our contributions are:


  - We formulate an _n_ -gram style prior over the LLM tokenization and inject it directly into the
model’s logits via a sparse, context-dependent logit update.


  - We systematically evaluate style-control methods using perplexity-based metrics, JS divergence across decoding steps, and token-overlap statistics.


  - On TinyLlama-1.1B, we show that there is a very narrow range of _λ_ where style and fluency
can simultaneously improve for one of three corpora, and that larger _λ_ values systematically
destabilize the model, leading to extreme perplexities and incoherent text, contradicting the
intuition that stronger priors always yield stronger style.


2


  - The most effective style control mechanism remains LoRA fine-tuning, with prompting still
providing significant control, and logit-space style injection offering only modest improvements
within a narrow range of _λ_ .


Our results indicate that logit-space steering is highly sensitive to corpus complexity and only
yields improvements within a low _λ_ regime on single-author data.


**2.** **Methods**


_2.1._ _Style_ _Prior_
The style prior is constructed through a sliding-window Markov-style probability construction.
The model will "learn" how likely a token is after its previous _n −_ 1 tokens, essentially assembling
a large table of conditional probabilities. For each order _n ∈{_ 1 _,_ 2 _,_ 3 _}_ :


_n_ -gram counts: _Cn_ (context, token)


        Context counts: _Nn_ (context) = _Cn_ (context, token)


token

We estimate smoothed conditional probabilities:


[token][) +] _[ k]_
_Pn_ (token _|_ context) = _[C][n]_ [(][context,]

_Nn_ (context) + _kV_


where _k_ is a small smoothing constant and _V_ is the vocabulary size. We set _k_ = 10 _[−]_ [3] and truncate
each context’s table to the top _K_ = 512 tokens to retain the most probable outcomes. This allows
us to estimate the probability of a token occurring after a particular context.
We also assemble _Pmix_ :



_n_ _[w][n][P][n]_ [(][token] _[ |]_ [ context)]

  



     _Pmix_ (token _|_ context) =




            
_n_ _[w][n]_
We use mixture weights _w_ 1 = 0 _._ 1, _w_ 2 = 0 _._ 3, and _w_ 3 = 0 _._ 6 to prioritize higher-order _n_ -grams as they
capture more specific stylistic and syntactic patterns than lower order ones. This weighting scheme
assumes that tokens appearing after longer sequences (e.g. trigrams) provide a stronger signal of the
style compared to shorter, more generic sequences. When computing _Pmix_, only _n_ -gram orders for
which the given context exists are included in the sum; we fall back to a small uniform distribution
when no estimate exists. We use log _Pmix_ when computing style perplexity.



_2.2._ _Injection_ _Mechanism_
We modify the LLM’s logits during decoding with the following mechanism. Let


_zi_ : LLM logits for token _i_ pre-softmax
_λ_ : Parameter to control the strength of steering
_wn_ : The weight for the _n_ -gram of size _n_
_Pn_ ( _i |_ context): The _n_ -gram probability that token _i_ comes after the context


3


       _zi_ _[′]_ [=] _[ z][i]_ [+] _[ λ]_ _wn_ log _Pn_ ( _i |_ context)

_n_

The update is sparse [1] : at each decoding step we only modify logits for tokens that appear in
the _n_ -gram tables for the current context, leaving other logits unchanged. This method treats each
_n_ -gram order as an independent log-likelihood contributor and is computationally efficient since we
are just performing arithmetic on logits before softmax, and the LLM stays frozen. We test various
_λ_ values to gauge the effect of the style prior.
_λ_ values were intentionally selected within the range [0 _,_ 1]. _λ_ = 0 corresponds to where no style
is injected, while _λ_ = 1 gives a more strongly style-biased distribution. Values _λ <_ 0 would actively
repel the model from the style prior, which is outside the scope of style alignment. Values _λ_ _>_ 1
can allow the prior to dominate the logits and empirically destabilize decoding without improving
alignment. Therefore we limit the sweep to _λ ∈_ [0 _,_ 1], a stable and interpretable range.


**3.** **Metrics**


We evaluate generations using style perplexity, base-model perplexity, JS divergence, and tokenoverlap metrics.


_3.1._ _Style_ _Perplexity_
We compute perplexity of the generated text under the interpolated style prior:











_._



_T_




Style PPL = exp




_−_ [1]



_T_



log _Pmix_ ( _xt_ _| x<t_ )

_t_ =1



Lower style perplexity indicates greater style alignment.


_3.2._ _Base-Model_ _Perplexity_
We also compute perplexity of the generated text under the base language model, allowing us to
see if the generation is something that the language model would actually produce, which in turn
allows us to see if the text is actually fluent and coherent.


_3.3._ _Distribution_ _Divergence_
We compute Jensen-Shannon (JS) divergence as a metric for the distribution between base logits
and biased logits across _λ_ . JS divergence is computed across each decoding step and averaged across
all tokens. This allows us to quantify the change in logits due to the style prior.


_3.4._ _Token-Overlap_ _Metrics_
To evaluate surface-level stylistic vocab/phrase alignment, we measure unigram overlap rate and
bigram seen rate.
1. Unigram Overlap Rate: fraction of generated tokens that appear in the top _K_ = 5000 unigrams from the style corpus.
2. Bigram Seen Rate: fraction of generated bigrams that are observed at least once in the style
corpus.


1While the definition of _Pmix_ in section 2.1 is a linear probability mixture, the logit injection is a log-linear
combination


4


**4.** **Experimental** **Setup**


_4.1._ _Models_ _and_ _Inference_
The LLM chosen in this experiment was TinyLlama-1.1B, as its compact size allows rapid
iteration with limited resources. Tokenization was done using the model’s WordPiece tokenizer.
Inference was performed on Google Colab using Python with the T4 GPU runtime, with FP16 and
gradients disabled.
For each style corpus we construct the style prior on the model’s tokenization. For Don Quixote
we use the English translation and train on the full text. For CNN/DailyMail we use the headline
portion of the dataset and subsample 200 _,_ 000 headlines for efficiency. For arXiv we sample 200 _,_ 000
paper abstracts from the ‘gfissore/arxiv-abstracts-2021‘ dataset. The prompts used for evaluation
are generic and are not drawn from any of these corpora.
We evaluate the effects of the style prior using greedy decoding, with generations spanning the
values:


_λ ∈{_ 0 _._ 00 _,_ 0 _._ 05 _,_ 0 _._ 10 _,_ 0 _._ 15 _,_ 0 _._ 20 _,_ 0 _._ 25 _,_ 0 _._ 30 _,_ 0 _._ 40 _,_ 0 _._ 50 _,_ 0 _._ 60 _,_ 0 _._ 70 _,_ 0 _._ 80 _,_ 0 _._ 90 _,_ 1 _._ 00 _}_


across all prompts, with the output set to a fixed length of 256 tokens. 20 prompts were constructed
from a breadth of categories:


_Narrative_ _Prompts_
1. “I still remember the moment when everything began to change”
2. “At the edge of the city, far from the noise and lights”
3. “She had promised herself she would never return to this place”
4. “By the time anyone noticed the mistake, it was already too late”
5. “The evening air carried a quiet sense of anticipation”


_Dialogue_ _Prompts_
1. “Are you sure this is the right decision?” he asked
2. “If we don’t act now, we may lose our only chance,” she replied
3. “That’s not what I meant,” they said patiently
4. “Listen carefully, because I won’t repeat this again,”
5. “Look, here’s the thing nobody wants to admit,”


_Expository_ _Prompts_
1. There are three main reasons why this issue is important.
2. At first glance, it might seem that nothing unusual is happening.
3. In recent years, many people have argued that this trend is accelerating.
4. From a practical point of view, the situation can be summarized as follows.
5. However, this explanation leaves out an important detail:


5


_Technical_ _Prompts_
1. First, we outline the basic idea of the method.
2. The system consists of three main components:
3. The goal of this section is to show that the proposed approach is effective.
4. If we compare these two approaches, we find that several key differences emerge.
5. To understand this more clearly, consider the following example:


These 20 prompts span narrative, dialogue, expository, and technical styles to avoid overfitting
to a single genre and to probe how the style prior behaves across qualitatively different inputs.
Unless otherwise noted, we use greedy decoding to isolate the effect of the style prior from
sampling randomness. To evaluate whether the results were a cause of greedy decoding we repeat
selected experiments on the arXiv dataset using top-p sampling ( _p_ = 0 _._ 9, temperature 1 _._ 0) and
compare trends.


_4.2._ _Baseline_ _Comparisons_
We benchmark the style injection by comparing to text generations of prompt-only style steering
and a LoRA fine-tune upon the corpus.


  - Prompt-only Style Steering: We prompt the LLM with high level instructions to mimic the
style of the corpus.


**–** This was done for _Don_ _Quixote_


**–** Prompt: "Write in the style of Miguel de Cervantes in _Don_ _Quixote_ "


  - LoRA fine-tune: We train a low-rank adaptation (LoRA) fine-tune with rank 8, _α_ = 16, and
dropout 0.05 on CNN/DailyMail headlines. We fine-tune TinyLlama-1.1B for 800 steps with
batch size 8 and learning rate 2 _×_ 10 _[−]_ [4] in fp16, using only the headline text as supervision.
This provides a strong style-specialized baseline for the news corpus.


This allows us to compare our method with existing methods of stylistic alignment.


**5.** **Results**


We present a quantitative analysis of logit-space steering across three distinct corpora. We
use Jensen-Shannon (JS) Divergence to track the magnitude the distribution shifts by due to the
style prior. We measure alignment of the style prior using Style Perplexity. We use Base-Model
Perplexity to assess the impact of the style prior on linguistic fluency. Our results reveal that low
values of _λ_ can improve stylistic fit in specific contexts, but higher injection strengths lead to a
rapid degradation of model output coherence, eventually resulting in a complete collapse of fluency.
To quantitatively analyze our findings, we begin with an analysis of JS divergence across all
decoding steps to see if the style prior is affecting the generations, and how changing _λ_ affects it.


6


_5.1._ _Steering_ _Behavior_


Figure 1: Steering strength increases with _λ_ (average across all decoding steps)


JS divergence is near 0 at _λ_ = 0 and grows roughly monotonically with _λ_ for all three corpora,
reaching at most _≈_ 0 _._ 06 bits at _λ_ = 1 _._ 0 (0.0641 for _Don_ _Quixote_, 0.0534 for news, and 0.0558 for
arXiv) (Figure 1). This shows that _λ_ provides a continuous, well-behaved control parameter in
distribution space: larger _λ_ values reliably induce larger deviations between the base and modified
distributions.


7


_5.2._ _Fluency_ _Cost_


Figure 2: Fluency collapses at high _λ_


Fluency is robust only near _λ_ = 0 (and _λ_ = 0 _._ 1 for _Don_ _Quixote_ ). For _Don_ _Quixote_, base-model
perplexity improves from 43 _._ 4 at _λ_ = 0 to 21 _._ 1 at _λ_ = 0 _._ 1, but then degrades, exceeding 1 _,_ 500
at _λ_ = 0 _._ 8 and 2 _,_ 400–2 _,_ 600 at _λ_ _∈{_ 0 _._ 9 _,_ 1 _._ 0 _}_ . For the news corpus, many small nonzero _λ_ values
already yield base PPL in the 900–1 _,_ 700 range, and high _λ_ values reach 25 _,_ 000–27 _,_ 000. The arXiv
corpus is even more fragile, with _λ_ _≥_ 0 _._ 15 producing base PPL above 6 _,_ 000 in our greedy runs
(Figure 2).
The relationship between _λ_ and base-model perplexity is nonlinear and heavily context dependent. For arXiv, the style prior almost immediately creates a spike in base-model perplexity,
indicating an immediate loss of fluency. For _Don_ _Quixote_ and news headlines corpora, the basemodel perplexity follows a different trend: it remains stable up until _λ ≈_ 0 _._ 6, and that the collapse
regime begins at _λ_ _>_ 0 _._ 6. All corpora indicate exponential increases in base-model perplexity,
confirming that high-strength steering eventually overpowers the base model’s coherence.


8


_5.3._ _Style_ _Fit_


Figure 3: Higher _λ_ does not lead to "more style"


Quantitative evaluation of stylistic alignment reveals that logit-space injection is incredibly
fragile. Across all corpora and _λ_ values, we identify a single setting where the style prior successfully
improves style perplexity: for _Don_ _Quixote_ at _λ_ = 0 _._ 1, style perplexity decreases from 4751 _._ 3 at
_λ_ = 0 to 3577 _._ 7, a 24 _._ 7% improvement (Figure 3).
Outside of this regime, increasing the steering strength ( _λ_ ) is counterproductive:


  - Non-Monotonicity: Style perplexity does not decrease as _λ_ increases; instead, it sharply trends
upward for all corpora.


  - Magnitude of Failure: For the news and arXiv corpora, any non-zero _λ_ immediately degrades
stylistic fit. No value of _λ_ improves style perplexity for these corpora. Perplexity increases by
factors of 10 to 100 relative to the baseline.


_5.4._ _Fluency-Style_ _Tradeoff_ _(Pareto_ _Frontier)_


Figure 4: Higher _λ_ leads to collapse


9


The Pareto frontier in base-model perplexity–style perplexity space makes these trade-offs explicit (Figure 4). For _Don_ _Quixote_, the point corresponding to _λ_ = 0 _._ 1 (21 _._ 1 base-model perplexity,
3577 _._ 7 style perplexity) strictly dominates the baseline _λ_ = 0 point (43 _._ 4, 4751 _._ 3), forming a narrow area where both fluency and style improve. All larger _λ_ values move up and to the right,
degrading one or both metrics. For the news and arXiv corpora, the _λ_ = 0 point (43 _._ 4, 1698 _._ 1
for news; 43 _._ 4, 5631 _._ 5 for arXiv) is Pareto-optimal: every nonzero _λ_ yields higher style perplexity,
higher base-model perplexity, or both. This visualization allows us to quantify the fragility of logitspace steering. While a "sweet spot" exists for the Don Quixote corpus at _λ_ = 0 _._ 1, the immediate
divergence of the other two corpora proves that these improvements do not generalize.


_5.5._ _Lexical_ _Structure_ _Degradation_


Figure 5: Lexical resemblance declines at high _λ_


While the previous spikes in perplexity indicate a loss of statistical alignment, the unigram
overlap and bigram seen rate (Figure 5) explains the nature of the failure. As _λ_ increases, the
model does not just struggle with style, it begins to diverge from the target vocabulary.
For the news corpus, the unigram overlap rate decreases from 0 _._ 826 at _λ_ = 0 to 0 _._ 454 at _λ_ = 0 _._ 9.
This suggests that the model is generating tokens that do not exist in the desired style corpus. This
general trend of decreasing unigram overlap rates is shared across the three corpora.
The sharp decline in bigram seen rate for the _Don_ _Quixote_ corpus from 0 _._ 478 to 0 _._ 141 reveals
that the model is not properly utilizing bigrams from the desired corpora. Part of this is due to the
steering actually causing nonsensical repeating generations at high _λ_ (Table 1).
This reinforces previous results that stronger _n_ -gram steering often yields generations that are
less consistent with the desired style, and it adds the insight that part of the cause is unigram
overlap and bigram seen rates decreasing.


10


_5.6._ _Baseline_ _Comparison_


Figure 6: Comparing Decoding-Time Steering with Prompt-Only and LoRA


For _Don_ _Quixote_, the style perplexity is improved from baseline by 24 _._ 7% with _λ_ = 0 _._ 1 (Figure
6). However, prompt-only modification demonstrates a much closer style fit to the target corpus
and reduces base-model perplexity from 43 _._ 4 to 7 _._ 58. On the CNN/DailyMail news headlines and
arXiv abstracts corpora, no _λ_ leads to a better style perplexity than _λ_ = 0. On the news corpus,
LoRA yields an extremely strong style fit.
Prompt-only modification led to a 76 _._ 7% improvement in style perplexity from baseline on _Don_
_Quixote_ and an 82 _._ 5% reduction in base-model perplexity, while LoRA led to a 93 _._ 3% improvement
in style perplexity and a 96 _._ 8% reduction in base-model perplexity on the news corpus. Promptonly modification is incredibly cheap yet still yields strong style alignment and fluency gains, but
metrics-wise LoRA still outclasses it on the news domain.
The prompt-only and LoRA style methodologies lead to significantly better style alignment than
any style prior tested.


_5.7._ _Sampling_ _Robustness_
The main experiments were performed using greedy decoding to rule out randomness as the
cause of a generation and to isolate the effect of the style prior. We analyze one experiment over


11


the arXiv dataset to see if similar trends follow when we use sampling.


Figure 7: Sampling Robustness on arXiv Corpus


For arXiv, style perplexity under both greedy and sampling tends to increase with _λ_ (Figure 7).
Under greedy decoding, mean style perplexity rises from 5631 at _λ_ = 0 to over 1 _._ 1 _×_ 10 [5] at _λ_ = 1 _._ 0,
while the coefficient of variation (CV) drops from 3 _._ 09 to 1 _._ 42. Under sampling, the mean increases
from 4 _._ 24 _×_ 10 [4] at _λ_ = 0 to 1 _._ 78 _×_ 10 [5] at _λ_ = 1 _._ 0, with CV decreasing from 3 _._ 70 to 1 _._ 34. This
pattern suggests that stronger steering both worsens style perplexity and concentrates generations
into fewer, more stereotyped modes. The qualitative trends in sampling with respect to _λ_ mirror
those observed with greedy decoding.


_5.8._ _Qualitative_ _Analysis_
We analyze a sample of generations across the _Don_ _Quixote_ corpus.


Table 1: Full Qualitative Examples Across Lambda Values


_λ_ **Style** **PPL** **Base** **PPL** **Generated** **Text**


Continued on next page


12


|λ|Style PPL|Base PPL|Generated Text|
|---|---|---|---|
|0.0|784.1|1.9|I still remember the moment when everything began to change.<br>I was sitting in my room, staring at the ceiling, when I heard a<br>knock on the door. I opened it to fnd my best friend, Sarah,<br>standing there. "Hey, Emily," she said, smiling. "I heard you<br>were feeling down. I wanted to come over and talk to you." I<br>felt a wave of relief wash over me. Sarah was always there for<br>me, no matter what. "Thanks, Sarah," I said, feeling a little<br>nervous. "I’m just feeling a little down." Sarah sat down on the<br>bed next to me and put her arm around me. "Emily, I know<br>it’s hard to talk about, but you’re not alone. I’ve been through<br>a lot, too. I’m here for you." I felt a lump form in my throat.<br>Sarah had always been there for me, no matter what. "I’m sorry<br>if I’ve been a little distant lately," I said, trying to keep my voice<br>steady. "I’ve been busy with school and work, and I just needed<br>some time to myself."|
|0.2|646.0|2.1|I still remember the moment when everything began to change.<br>I was sitting in my room, staring at the ceiling, lost in thought.<br>I had just fnished my fnal exam and was feeling a sense of relief<br>wash over me. But as I looked up, I saw something that made<br>my heart skip a beat. There, in the corner of the room, was a<br>small, intricately designed fower. It was a delicate pink rose,<br>with delicate petals that seemed to glow in the dim light.<br>I<br>couldn’t believe my eyes. I picked up the rose and held it in my<br>hand, marveling at its beauty. It was unlike anything I had ever<br>seen before. The petals were soft and velvety, with a delicate<br>fragrance that flled the room.<br>As I looked closer, I realized<br>that the rose was not just any ordinary fower. It was a symbol<br>of hope, a reminder that even in the darkest of times, there is<br>always something beautiful to be found. From that moment on,<br>I began to see the world in a new light. I started to appreciate<br>the small things, the moments that seemed insignifcant at the<br>time but that would later on become cherished mem|


Continued on next page


13


|λ|Style PPL|Base PPL|Generated Text|
|---|---|---|---|
|0.4|392.6|1.4|I still remember the moment when everything began to change. I<br>remember the feeling of the rain on my skin, the taste of the salt<br>on my lips, and the warmth of the sun on my skin. I remember<br>the sound of the waves crashing against the shore, the feel of the<br>sand between my toes, and the smell of the ocean. I remember<br>the feeling of the waves crashing against the shore, the feel of the<br>sand between my toes, and the smell of the ocean. I remember<br>the feeling of the rain on my skin, the taste of the salt on my<br>lips, and the warmth of the sun on my skin. I remember the<br>feeling of the rain on my skin, the taste of the salt on my lips,<br>and the warmth of the sun on my skin. I remember the feeling<br>of the rain on my skin, the taste of the salt on my lips, and the<br>warmth of the sun on my skin. I remember the feeling of the<br>rain on my skin, the taste of the salt on my lips, and the warmth<br>of the sun on my skin. I remember the feeling of the rain on my<br>skin, the taste of the salt on my lips, and the warmth|
|0.6|2632.4|1.7|I still remember the moment when everything began to change.<br>Scene 2: INT. KITCHEN - DAY Jenna is cooking dinner for her<br>family, and Sarah walks in. JENNA Hi Sarah, dinner’s ready.<br>SARAH Thanks, Jenna.<br>JENNA You’re welcome.<br>JENNA<br>You’re welcome.<br>JENNA You’re welcome.<br>JENNA You’re<br>welcome.<br>JENNA You’re welcome.<br>JENNA You’re welcome.<br>JENNA You’re welcome.<br>JENNA You’re welcome.<br>JENNA<br>You’re welcome.<br>JENNA You’re welcome.<br>JENNA You’re<br>welcome.<br>JENNA You’re welcome.<br>JENNA You’re welcome.<br>JENNA You’re welcome.<br>JENNA You’re welcome.<br>JENNA<br>You’re welcome|
|0.8|5077.8|2.1|I still remember the moment when everything began to change.<br>Scene 2: INT. KITCHEN - DAY Jane is cooking dinner for her-<br>self and her family, surrounded by the smell of garlic and tomato<br>sauce. JANE (to herself) You’re doing this, Jane. You’re doing<br>this. Jane’s phone rings. JANE Hello, Jane’s phone rings. Jane<br>answers. JANE Hello, Jane’s voice. Jane’s husband, JOHN, an-<br>swers. JOHN Hi Jane, Jane’s husband, JOHN, answers. JOHN<br>Hi Jane, Jane’s husband, JOHN, speaks.<br>JOHN We’re sorry<br>to bother you, Jane, Jane’s husband, JOHN, speaks.<br>JOHN<br>We’re sorry to bother you, Jane, Jane’s husband, JOHN, speaks.<br>JOHN We’re sorry to|


Continued on next page


14


|λ|Style PPL|Base PPL|Generated Text|
|---|---|---|---|
|1.0|6826.5|2.9|I still remember the moment when everything began to change.<br>Scene 2: INT. KITCHEN - DAY Jane is cooking dinner for<br>herself and her family, surrounded by the smell of garlic and<br>tomato sauce. JANE "Mom, dinner’s ready!" Jane calls out to<br>her mother as she pours herself some water. MARILYN "Thank<br>god, Jane!" Marilyn looks relieved. Jane’s mother takes a sip of<br>the warm water, and Jane watches as she starts to choke. MAR-<br>ILYN "Oh no!" Jane’s mother gasps.<br>Jane’s mother tries to<br>breathe but fails, and Jane’s mother falls onto Jane’s lap. JANE<br>"Mom, what’s happening?" Jane asks as tears stream down her<br>face. MARILYN "Oh Jane, I’m so sorry. I’ve been drinking too<br>much." Marilyn looks ashamed. Jane’s mother looks defeated.<br>JANE "Mom, I’m sorry too."|
|Prompt|172.4|2.1|Write in the style of Miguel de Cervantes in _Don Quixote_. I still<br>remember the moment when everything began to change. It was<br>a warm summer evening, and I was sitting on the porch of my<br>grandparents’ house, reading a book. I was lost in the story, lost<br>in the world of the characters, lost in the words. Suddenly, I<br>heard a noise. It was a rustling in the bushes, and I knew that<br>it was not a bird or a squirrel. It was a man. I stood up, my<br>heart racing, and walked towards the sound. When I got closer,<br>I saw that it was a man in a white cloak, with a long beard and<br>a sword in his hand. He was walking towards me, and I could see<br>that he was not alone. There were two other men with him, and<br>they were also dressed in white. I was terrifed. I had never seen<br>anyone like this before. I had never seen a man with a sword<br>before. I had never seen a man with a white cloak before. I had<br>never seen a man with two other men with him before. The man<br>with the sword stopped in front of me, and I could see that he<br>was a knight. He was tall, with a long, fowing beard|


We can see that in some high _λ_ generations, nonsensical repetition cycles occur (Table 1), likely
due to the style prior elevating repeating tokens that usually would not be selected by the LLM.


**6.** **Discussion**


Our findings highlight that the style prior logit-space injection does not beat baseline methods of
modifying style. Tweaking _λ_ produces a narrow sweet spot where metrics improve on _Don_ _Quixote_,
but even so, prompt-only steering performs better, and LoRA remains substantially stronger overall
(Figure 6).
We see that small _λ_ outperforms large _λ_ in multiple metrics, likely because at higher _λ_ the
probabilistic model attempts to boost tokens that make sense at the trigram level, but not within
the general context. At lower _λ_ the LLM is able to "overpower" the style prior and keep generations
on the right track (Figure 3).
The _n_ -gram prior and the LLM distribution become mathematically incompatible at high _λ_ .
The _n_ -gram model is context-poor, while the LLM is context-rich. This forces the model to pick


15


words that satisfy local statistical patterns, violating the LLM’s global logic. Consequently, the
LLM collapses into a 3-gram repetition loop that it finds as the highest probability "style" move even as it destroys the global coherence of the generation (Table 1).
The style prior performed the best on _Don_ _Quixote_ . _Don_ _Quixote_ has one author, whereas the
CNN/DailyMail and arXiv abstracts datasets are aggregations of multiple authors and carry their
distinct tones, making it difficult for the Markovian model to pick up. The arXiv abstracts and news
headline datasets have high entropy because they contain technical jargon or diverse reporting styles
which are hard to grasp through an _n_ -gram model. _Don_ _Quixote_ has a single, distinguishable style,
allowing the model to learn stable patterns (Figure 3). The book contains archaic language patterns
such as "thou art" which are very distinct from the base LLM’s training data. Such patterns are
easy to build an _n_ -gram over and steer toward, even if fragile.
Within our sweep, we did not find an optimal configuration that uses _n_ -gram to capture the style
of arXiv abstracts and news headlines, the Pareto-optimal points for both are at baseline ( _λ_ =0).
This suggests that logit-space injection is not just worse, but results in degradation of both key
metrics simultaneously (Figure 4).
Additionally, unigrams, bigrams, and trigrams capture archaic repeated phrase structure, but
they do not capture longer academic/news rhetorical structure.
While our results demonstrate the fragility of logit-space injection, this exploration is essential
for exploring the usability and boundaries of modular AI control. These findings help to identify
possible areas where simple statistical priors can be valuable, while also contextualizing the method
in the space of style control.


**7.** **Related** **Work**


Decoding-time control for LLMs has been approached from several angles. Plug-and-Play Language Models steer generation by applying gradients from an attribute classifier to the hidden state
of a frozen LM, enabling sentiment or topic control at inference time without parameter updates [2].
Critic-guided decoding uses a critic model trained in an actor-critic framework to reweight token logits during decoding according to predicted reward [5]. Both methods demonstrate the fundamental
trade-off between control strength and fluency.
More recent work has focused on using external signals to modify logits directly during decoding.
DeRa introduces a continuous alignment knob by incorporating a reward-model alignment score into
decoding [3]. PAD extends this idea to personalization, training a user-specific reward model and
applying it at inference [4]. These approaches require neural critics trained on supervised preference
data; by contrast, our method requires no additional learned components.
Several lines of research revisit classical _n_ -gram models in the LLM era. Li et al. show that
learning a neural language model on the residual between an _n_ -gram model and the true distribution improves perplexity and rare-token prediction, indicating that _n_ -grams retain valuable local
structure [6]. Infini-gram further demonstrates that massive, web-scale _n_ -gram statistics remain
effective and efficient to query [7]. These results support our use of _n_ -gram statistics as a stylistic
prior rather than a full generative model. Messner & Lippincott (2025) [1] also operate in logit
space using _n_ -gram statistics, but with a different goal: they construct an _n_ -gram model from a
target style corpus and use its probabilities to rescale token logits to make the LLM select dialectspecific subword realizations (e.g., variations in AAVE). Their method is designed explicitly for style


16


and dialect transfer via extreme subword variation; their results demonstrate that _n_ -gram-based
logit-space steering can produce lightweight stylistic alignment without changing model weights.
By contrast, we treat the _n_ -gram model as a general-purpose Markov prior over the full nexttoken distribution and study its behavior as a tunable probabilistic component with _λ_ . We do not
optimize for dialect rewriting, and instead we focus on how increasing the strength of the style prior
trades off style and fluency. Overall, we analyze the dynamics of _n_ -gram style tuning.
Our approach departs from prior work in three ways: (1) it is fully non-parametric, requiring no
additional models or training; (2) it provides a continuous style-control knob analogous to DeRa’s
alignment parameter but grounded in empirical token transitions; and (3) it reframes _n_ -gram models
as a plug-in personalization signal rather than a fallback LM or safety filter.


**8.** **Conclusion**


We investigated stylistic control via logit-space injection of an _n_ -gram prior. Our results demonstrate that this approach is fragile, consistently resulting in collapse at higher strengths. Logit-space
injection is dominated by both prompt-only steering and LoRA fine-tuning across all tested regimes.
In fact, logit-space injection worsens style and base-LM perplexity in all cases beyond a narrow stability regime: on _Don_ _Quixote_ with _λ_ = 0 _._ 1 where style perplexity improved by 24.7% (Figure
3).
The core finding of this experiment is that logit-space steering results in collapse of the generation. When applied to high-entropy corpora such as news headlines and arXiv abstracts, the
baseline model with _λ_ = 0 remains the only Pareto-optimal configuration (Figure 4). Increasing
steering at all for these corpora results in worse metrics, and at higher _λ_ values the model is forced
into repetitive loops of nonsense where the generated text becomes highly implausible under both
the target style and natural language (Table 1). Ultimately, while logit-space steering is computationally lightweight, it is Pareto-dominated by weight-altering methods due to its failure to capture
longer-term structural patterns while maintaining global coherence.
Future work can explore:


  - Better calibrated priors or an _n_ -gram that looks further back.


  - Incorporating neural models that can retain longer-term sequences to guide style, as done by
Kim et al. (2023) [5]


  - Penalizing repeating and illogical generations.


  - Further analysis of style prior performance on single-author corpora.


**References**


[1] C. Messner, T. Lippincott, Transferring extreme subword style using ngram model-based logit
scaling, in: Proceedings of the 5th International Conference on Natural Language Processing for
Digital Humanities, Association for Computational Linguistics, Albuquerque, USA, 2025, pp.
272–280. doi:10.18653/v1/2025.nlp4dh-1.24.
URL `https://aclanthology.org/2025.nlp4dh-1.24/`


17


[2] S. Dathathri, A. Madotto, J. Lan, J. Hung, E. Frank, P. Molino, J. Yosinski, R. Liu, Plug
and play language models: A simple approach to controlled text generation, in: International
Conference on Learning Representations, 2020, arXiv:1912.02164.
URL `https://openreview.net/forum?id=H1edEyBKDS`


[3] T. Liu, S. Guo, L. Bianco, D. Calandriello, Q. Berthet, F. Llinares, J. Hoffmann, L. Dixon,
M. Valko, M. Blondel, Decoding-time realignment of language models, in: Proceedings of the
2024 Conference on Empirical Methods in Natural Language Processing, Association for Computational Linguistics, 2024.
URL `https://arxiv.org/abs/2402.02992`


[4] R. Chen, X. Zhang, M. Luo, W. Chai, Z. Liu, Pad: Personalized alignment of llms at decodingtime, arXiv preprint arXiv:2410.04070 (2024).
URL `https://arxiv.org/abs/2410.04070`


[5] M. Kim, H. Lee, K. M. Yoo, J. Park, H. Lee, K. Jung, Critic-guided decoding for controlled text generation, in: Findings of the Association for Computational Linguistics: ACL
2023, Association for Computational Linguistics, Toronto, Canada, 2023, pp. 4598–4612.
doi:10.18653/v1/2023.findings-acl.281.
URL `https://aclanthology.org/2023.findings-acl.281/`


[6] H. Li, D. Cai, J. Xu, T. Watanabe, _n_ -gram is back: Residual learning of neural text generation
with _n_ -gram language model, in: Findings of the Association for Computational Linguistics:
EMNLP 2022, Association for Computational Linguistics, Abu Dhabi, United Arab Emirates,
2022, pp. 1523–1533. doi:10.18653/v1/2022.findings-emnlp.109.
URL `https://aclanthology.org/2022.findings-emnlp.109`


[7] J. Liu, S. Min, L. Zettlemoyer, Y. Choi, H. Hajishirzi, Infini-gram: Scaling unbounded _n_ -gram
language models to a trillion tokens, arXiv preprint arXiv:2401.17377 (2024).
URL `https://arxiv.org/abs/2401.17377`


18


