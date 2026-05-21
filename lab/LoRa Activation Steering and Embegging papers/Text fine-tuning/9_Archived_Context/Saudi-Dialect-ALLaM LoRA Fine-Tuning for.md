# Saudi-Dialect-ALLaM: LoRA Fine-Tuning for Dialectal Arabic Generation

Hassan Barmandah
Department of Software Engineering
Umm Al-Qura University, Makkah, Saudi Arabia
s445001043@uqu.edu.sa



_**Abstract**_ **—Large** **language** **models** **(LLMs)** **for** **Arabic** **are** **still**
**dominated** **by** **Modern** **Standard** **Arabic** **(MSA),** **with** **limited**
**support** **for** **Saudi** **dialects** **such** **as** **Najdi** **and** **Hijazi.** **This**
**underrepresentation** **hinders** **their** **ability** **to** **capture** **authentic**
**dialectal** **variation.** **Using** **a** **privately** **curated** **Saudi** **Dialect**
**Instruction** **dataset** **(Hijazi** **&** **Najdi;** **5,466** **synthetic** **instruction–**
**response** **pairs;** **50/50** **split),** **we** **LoRA-tune** **ALLaM-7B-Instruct-**
**preview—the** **first** **foundation** **model** **developed** **in** **Saudi** **Ara-**
**bia—for** **Saudi** **dialect** **generation.** **We** **investigate** **two** **variants:**
**(i)** _**Dialect-Token**_ **training,** **which** **prepends** **an** **explicit** **dialect**
**tag** **to** **the** **instruction,** **and** **(ii)** _**No-Token**_ **training,** **which** **omits**
**the** **tag** **at** **formatting** **time.** **Evaluation** **on** **a** **held-out** **test** **set**
**combines** **an** **external** **dialect** **classifier** **with** **text** **fidelity** **metrics**
**(chrF++** **and** **BERTScore)** **and** **diversity** **measures.** **The** **Dialect-**
**Token** **model** **achieves** **the** **best** **control,** **raising** **the** **Saudi** **rate**
**from 47.97% to 84.21% and reducing MSA leakage from 32.63%**
**to** **6.21%;** **fidelity** **also** **improves** **(chrF++** +3 _._ 53 **,** **BERTScore**
+0 _._ 059 **). Both LoRA variants outperform strong generic instruc-**
**tion** **models** **(Falcon-7B-Instruct,** **Llama-3.1-8B-Instruct,** **Qwen-**
**2.5-7B-Instruct,** **AceGPT-v2-8B-Chat,** **JAIS-13B-Chat)** **in** **dialect**
**control** **and** **fidelity,** **while** **avoiding** **metadata-tag** **echoing** **that**
**these** **baselines** **frequently** **exhibit.** **We** **do** **not** **release** **the** **dataset**
**or** **any** **model** **weights/adapters;** **instead,** **we** **release** **train-**
**ing/evaluation/inference** **code** **and** **a** **detailed** **datasheet** **(schema**
**and** **aggregate** **statistics)** **to** **support** **independent** **verification.**
_**Index**_ _**Terms**_ **—Arabic** **NLP,** **Saudi** **dialects,** **LoRA,** **instruction**
**tuning,** **ALLaM,** **dialect** **identification**


I. INTRODUCTION


Large language models (LLMs) such as LLaMA [1] and
Arabic-centric systems like ALLaM [2], JAIS-13B-Chat [3],
and AraGPT2 [4] have accelerated progress in Arabic NLP.
However, coverage remains skewed toward _Modern_ _Standard_
_Arabic_ (MSA), with comparatively limited support for regional
dialects. This imbalance often yields overly formal, panArabic outputs that fail to capture cultural and pragmatic
nuance. In particular, Saudi dialects—Najdi and Hijazi—are
underrepresented in open models despite their widespread realworld use.
Insufficient support for Saudi dialects has practical consequences. When systems default to MSA, they underperform in everyday applications such as dialogue, education,
entertainment, and culturally aware assistants. Community
leaderboards (e.g., OALL) [5] repeatedly highlight gaps in
dialectal coverage. Moreover, widely used resources such as
MARBERT reveal that Gulf Arabic versus MSA remains a
confusable axis [6]. In our evaluation, we therefore adopt the
MARBERTv2 Arabic Written Dialect Classifier [7], a five-way



model (MAGHREB/LEV/MSA/GLF/EGY) fine-tuned from
MARBERTv2 for written dialect identification, where GLF
serves as a practical proxy for Saudi usage.
**Baselines.** We include Falcon-7B-Instruct [8] as a baseline.
While TII has announced Falcon-Arabic with strong results
on Arabic benchmarks (e.g., OALL v2) [5], [9], we evaluate
publicly available Falcon baselines and discuss Falcon-Arabic
qualitatively. Alongside Falcon, we compare against Llama3.1-8B-Instruct [1], Qwen-2.5-7B-Instruct [10], AceGPT-v28B-Chat [11], and JAIS-13B-Chat [3].
**This** **work.** We curate a balanced, synthetic instruction–response dataset for Saudi dialects (Hijazi/Najdi; 5,466
pairs) and train a LoRA-tuned variant of ALLaM-7B-Instructpreview specialized for Saudi dialect generation. We study
two strategies: (i) _Dialect-Token Conditioning_, which prepends
an explicit dialect tag to instructions, and (ii) _No-Token_
_Conditioning_, which omits tags and relies on the model
to infer dialect implicitly. While the dataset and trained
weights/adapters are not publicly released, we provide a
comprehensive datasheet (schema, cleaning pipeline, topic
taxonomy, and descriptive statistics) together with full training/evaluation/inference code to support reproducibility.
On a held-out Saudi test set, the Dialect-Token variant
achieves higher dialect fidelity (84.2% Saudi per the external classifier [7]) while substantially reducing MSA leakage
(6.2%). Both LoRA variants outperform strong generic instruction models (Falcon-7B-Instruct, Llama-3.1-8B-Instruct,
Qwen-2.5-7B-Instruct, AceGPT-v2-8B-Chat, JAIS-13B-Chat)
on Saudi-specific automatic metrics, while avoiding issues
such as tag echoing observed in those baselines.
**Contributions.** Our work makes four contributions:
(1) a curated, balanced instruction–response dataset dedicated
to Saudi Arabic (Hijazi/Najdi); although private, we disclose
a detailed datasheet and aggregate statistics;
(2) an experimental study and open codebase for LoRA
adaptation of ALLaM-7B-Instruct-preview for Saudi dialect
generation; neither the dataset nor trained weights/adapters are
released;
(3) a systematic comparison of Dialect-Token vs. No-Token
strategies, demonstrating the advantages of explicit conditioning for dialect control and MSA-leakage reduction;
(4) a transparent evaluation suite combining an external dialect classifier with fidelity and diversity metrics to enable
independent verification without access to the raw training set


or model weights.


II. RELATED WORK


Research on Arabic LLMs and dialect modeling has expanded rapidly with the rise of instruction tuning and Arabicnative evaluation. A recurring challenge is the dominance
of Modern Standard Arabic (MSA) in pretraining corpora,
which leaves regional varieties—especially Gulf and Saudi
dialects—underrepresented. Below, we review seven lines of
work shaping today’s Arabic LLM landscape across pretraining, instruction data, and dialect identification, framing our
focus on Saudi (Hijazi/Najdi) instruction tuning and GLFbased external evaluation.
Bari et al. [2] introduce _ALLaM-7B-Instruct-preview_, the
first Saudi foundation model [12]. Their work covers Arabiccentric pretraining and instruction-tuned variants, evaluated
through automatic metrics, LLM-as-a-judge assessments, and
human studies. It highlights practical recipes for aligning
Arabic models and demonstrates strong performance across
general Arabic tasks. Since our backbone is ALLaM-7BInstruct-preview, this research provides the architectural and
training substrate on which we apply LoRA and Saudi-dialect
supervision, illustrating how targeted data can further specialize a Saudi foundation model for dialect-specific generation.
Qarah [13] proposes _SaudiBERT_, an encoder pre-trained
on large-scale Saudi corpora (e.g., STMC tweets and Saudi
forums). The study argues that dialect-specific pretraining
better captures Saudi lexical, morphological, and pragmatic
phenomena than MSA-centric encoders. This strengthens the
case for Saudi-centric resources; we extend this idea to the
generative setting by curating (private) a balanced Saudi instruction dataset and measuring dialectal fidelity in generation.
Abdul-Mageed et al. [14] present _ARBERT/MARBERT_, Arabic transformers trained on massive social media text covering
diverse dialects. Beyond improving many Arabic benchmarks,
these models underpin later dialect-aware tools and datasets.
Their emphasis on informal, user-generated content foreshadows our evaluation focus: distinguishing Gulf/Saudi-style outputs from MSA in open-ended generation.
Amin [7] releases the _MARBERTv2_ _Arabic_
_Written_ _Dialect_ _Classifier_, a five-way identifier
(GLF/LEV/MSA/EGY/MAGH) fine-tuned from
MARBERTv2 [14] for short, written text. Community
usage has converged on this classifier as a practical external
judge for dialect labels in generated text. We adopt it to
quantify Saudi/Gulf alignment (via GLF) and to estimate
MSA leakage, providing an objective complement to human
judgments.
Sengupta et al. [3] introduce _JAIS-13B-Chat_, Arabic-centric
foundation and instruction-tuned models trained on mixed
Arabic–English corpora. The paper shows that Arabic-first
post-training substantially boosts instruction following in Arabic while retaining multilingual utility. We situate our LoRAtuned Saudi models against such open baselines to test whether
targeted Saudi supervision improves dialect fidelity beyond
generic instruction tuning.



The Falcon team [9] recently introduced _Falcon-Arabic_, a
7B-parameter model adapted from Falcon 3. Unlike earlier
efforts that relied on translated data, Falcon-Arabic was trained
on high-quality native Arabic corpora and extended with
32k Arabic-specific tokens to better capture morphology and
dialectal variation. The model excels in MSA while also
demonstrating strong coverage of regional dialects, outperforming not only Arabic-focused models of similar size but
even larger multilingual systems across benchmarks such as
Arabic MMLU, MadinahQA, and Aratrust. With a context
length of 32k tokens and alignment via supervised finetuning and Direct Preference Optimization, Falcon-Arabic sets
a new bar for Arabic-first LLMs. Our work differs in focus:
while Falcon-Arabic provides broad coverage across MSA and
multiple dialects, _we_ _curate_ _(private)_ a fine-grained Saudicentric dataset and train a LoRA-tuned variant of ALLaM7B-Instruct-preview (weights not released), targeting precise
control of Hijazi and Najdi generation.
Chouikhi et al. [15] introduce _GemmAr_, which leverages
large-scale Arabic instruction data. Its companion resource,
InstAr-500k [16], demonstrates that broad Arabic-focused
instruction tuning yields sizable gains even for models not
originally trained for Arabic. This underscores the leverage
of instruction data quality and coverage. Our contribution
complements this by balancing dialect labels and testing explicit dialect-token conditioning to control Saudi style during
generation.
Taken together, the reviewed literature underscores a shift
from MSA-centric modeling toward dialect-aware Arabic NLP,
spanning pretraining (e.g., SaudiBERT), instruction tuning
(e.g., ALLaM, JAIS, GemmAr/InstAr-500k), and standardized
dialect identification via MARBERT-family tools. Building
on these advances, our study targets the underrepresented
Saudi varieties (Hijazi/Najdi) _by_ _curating_ a balanced instruction–response dataset (kept private) and applying parameterefficient fine-tuning of ALLaM-7B-Instruct-preview with explicit dialect-token conditioning. Using an external writtendialect classifier (GLF/LEV/MSA/EGY/MAGH) as an objective judge, we quantify Saudi/Gulf alignment and MSA
leakage, demonstrating consistent gains over strong open baselines and offering a reproducible path for culturally grounded,
Saudi-centric generation.


III. DATASET AND ANALYSIS


_A._ _Dataset_ _Description_


We curate the _Saudi_ _Dialect_ _Instruction_ dataset (Hijazi
& Najdi), a synthetic instruction–response corpus targeting
Saudi Arabic. Each record consists of an instruction, a
dialect-pure response, and a categorical dialect label.
The dataset is **not** **publicly** **released** . We disclose the full
schema, preprocessing steps, and descriptive statistics to support transparency.


_B._ _Distribution_ _and_ _Coverage_


To validate balance and topical coverage, we analyze dialect
counts and category frequencies.


Dataset Distribution by Dialect


50.0% 50.0%



Hijazi (2733)



|Col1|Col2|Col3|Col4|Col5|Col6|Col7|Col8|Col9|Col10|Col11|Col12|Col13|Col14|Col15|Col16|Col17|Col18|Col19|Col20|Col21|Col22|Col23|Col24|Col25|Col26|Col27|Col28|Col29|Col30|Col31|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
||||||||||||||||||||||||||||||||
||||||||||||||||||||||||||||||||
||||||||||||||||||||||||||||||||
||||||||||||||||||||||||||||||||
||||||||||||||||||||||||||||||||
||||||||||||||||||||||||||||||||
||||||||||||||||||||||||||||||||
||||||||||||||||||||||||||||||||
||||||||||||||||||||||||||||||||


Fig. 3. Ranked frequency distribution of Arabic tokens.



2250

2000

1750

1500

1250

1000

750

500



Fig. 1. Dataset distribution by dialect (Hijazi vs. Najdi).



shopping_markets



work_careers





education_learning



health_fitness



technology_gadgets

family_relationships





food_cooking







sports_competitions



travel_tourism

history_heritage







|Col1|Col2|Col3|Col4|Col5|443|Col7|Col8|
|---|---|---|---|---|---|---|---|
|||||||||
||||||||442|
|||||||||
|||||||||
|||||||||
|||||||414|414|
|||||||||
|||||||||
|||||||||
|||||||||
|||||||||
|||||369||||
|||||||||
|||||||||
|||||||||
|||||||||
|||||||||
|||||||||
|||||||||
|||||||||
|||||||||


Count


Fig. 2. Top-10 topic frequencies in the dataset.


Figure 1 confirms a strict 50/50 balance across Hijazi and
Najdi labels. This design prevents dialect–topic confounds and
ensures that evaluation performance cannot be attributed to
skewed representation.
The most common topics are (shopping markets),
(work careers), (education learning), (health fitness), and
(technology gadgets). Together, these five domains account
for roughly 55% of the dataset, reflecting strong coverage of
everyday contexts.


_C._ _Lexical_ _Analysis_


We further analyze word-level distributions to inspect dialect authenticity.
The ranked distribution highlights frequent Saudi dialect
terms absent in MSA, confirming dialectal grounding. As a
qualitative complement, we generate a word cloud of the most
frequent tokens:
The cloud reveals salient lexical items typical of Saudi
everyday conversation, reinforcing dataset fidelity to regional
speech norms.


_D._ _Data_ _Preparation_ _Pipeline_


To construct training-ready inputs, we apply two key steps:


_•_ **Balance:** Enforce an exact 50/50 split between Hijazi
and Najdi examples, ensuring equal representation while
dropping any unknown or ambiguous dialect entries to
maintain dataset integrity.



Fig. 4. Word cloud (Arabic-only) across Hijazi and Najdi subsets.


_•_ **Dialect** **tags:** Prepend an explicit dialect token, such
as <DIALECT=HIJAZI> or <DIALECT=NAJDI>, to
the instruction field. This step enables controlled
conditioning for generation and allows the model to
clearly distinguish between Hijazi and Najdi outputs
during training.


This pipeline supports both the Dialect-Token and No-Token
strategies explored in Section 4.


_E._ _Limitations_


Despite strict cleaning and balancing, the dataset remains
synthetic in nature and does not include multi-turn dialogue,
natural conversations, or spontaneous interaction patterns. This
limits its ability to capture discourse flow, speaker variation,
and pragmatic context. Furthermore, the relatively small size
of 5.5k instruction–response pairs restricts coverage of less
common dialectal phenomena, idiomatic expressions, and lowfrequency lexical items that occur in everyday communication.
Other Saudi-dialect corpora exist, such as SauDial (game
localization) [17], SADLyC (song lyrics) [18], and SADA
(speech transcripts) [19]. However, these differ in format,
domain, and intended use cases. By contrast, our contribution is among the first balanced instruction–response corpora
targeting Saudi Arabic (Hijazi and Najdi); however, the dataset
is private and not shared publicly.


IV. METHODOLOGY


_A._ _Data_ _Preprocessing_


To ensure fair and balanced evaluation, the Saudi Dialect
Instruction Dataset was split into train/dev/test sets with
an 80/10/10 ratio. Stratified sampling was applied across
three metadata dimensions—dialect (Hijazi, Najdi), topic (18
categories), and length (short, medium, long)—to preserve
representative distributions in each split.
Each example was converted into the instruction–response
format used for instruction tuning:


Instruction: [user prompt]

Response: [dialectal output]


Text was tokenized using the ALLaM-7B-Instruct-preview
tokenizer, with sequences truncated or packed to a maximum
of 2048 tokens for GPU efficiency. We prepared two variants:


_•_ **Dialect-Token:** prepend an explicit tag (<HIJAZI> or
<NAJDI>) to the instruction, giving the model direct
conditioning signals;

_•_ **No-Token:** omit tags, leaving dialect inference implicit.

This preprocessing pipeline yields a clean, balanced dataset
suitable for LoRA fine-tuning of ALLaM-7B-Instruct-preview.


_B._ _Model_ _Architecture_


We adopt ALLaM-7B-Instruct-preview [2], a 7B-parameter
decoder-only transformer [20] designed for large-scale language modeling. The model follows an autoregressive
paradigm, where the probability of each token is conditioned
on all preceding tokens. Input text is mapped into embeddings with positional encodings, then passed through stacked
transformer blocks comprising multi-head self-attention and
feedforward sublayers with residual connections and normalization. This layered design captures both local and long-range
dependencies, enabling dialect-aware generation.
_Scaled_ _dot-product_ _attention:_



Fig. 5. High-level pipeline of ALLaM-7B-Instruct-preview with LoRA
adapters for Saudi dialect generation.


_Cross-entropy_ _loss:_



_LCE_ = _−_ [1]

_N_



_N_

- log _pθ_ ( _yi_ _| y<i, x_ )


_i_ =1




         - _QK_ _⊤_
Attention( _Q, K, V_ ) = softmax ~~_√_~~
_dk_




_V_



_Transformer_ _block_ _update_ _(residual_ _+_ _norm_ _+_ _FFN):_


_Zl_ = LayerNorm� _Xl_ + Attention( _Ql, Kl, Vl_ )� _,_

_Xl_ +1 = LayerNorm� _Zl_ + FFN( _Zl_ )� _._


Here, _Q_, _K_, and _V_ represent query, key, and value projections, while _dk_ denotes the key dimension. Attention provides
contextual weighting of tokens, and residual–normalization
ensures stable gradients. Stacking these blocks yields progressively richer contextual features.


_C._ _Fine-Tuning_


We fine-tune ALLaM-7B-Instruct-preview using supervised
next-token prediction with causal language modeling (CLM).
For an instruction–response pair, the model minimizes crossentropy between predicted token distributions and gold targets.
Model perplexity (PPL) is tracked as an intrinsic measure of
fit.



Training ran for 15 epochs with batch size 2 (gradient accumulation of 8), cosine learning rate with warmup, maximum
sequence length 2048, mixed-precision BF16, and sequence
packing for efficiency.


_D._ _Parameter-Efficient_ _Adaptation_ _(LoRA)_


To adapt the ALLaM-7B-Instruct-preview backbone efficiently, we employ Low-Rank Adaptation (LoRA) [21]. LoRA
injects trainable low-rank matrices into projection layers,
updating only these factors while keeping backbone weights
frozen. This reduces memory and compute costs, making it
practical for dialect specialization.
LoRA hyperparameters:


_•_ Rank _r_ = 32

_•_ Scaling factor _α_ = 64

_•_ Dropout _p_ = 0 _._ 1

_•_ Bias: none

_•_ Task type: Causal LM

Both Dialect-Token and No-Token models were trained with
identical configurations, differing only in whether the leading
dialect tag was included.


_E._ _Training_ _and_ _Inference_ _Setup_


**Optimization.** Fine-tuning used AdamW with a cosine
learning-rate schedule and restarts over 15 epochs. The effective batch size was 16 (per-device 2, gradient accumulation
8). Mixed-precision BF16 and gradient checkpointing reduced
memory usage and improved efficiency.


**Inference.** At generation time, we applied nucleus sampling [22] with temperature _T_ = 0 _._ 6, top- _p_ = 0 _._ 95, and maximum length of 256 tokens, balancing fluency and diversity
while avoiding excessive randomness.


_F._ _Evaluation_ _Metrics_


We evaluate baselines and fine-tuned models with a multidimensional suite covering dialect classification, fluency, semantic similarity, and diversity:

_•_ **Saudi%** **(GLF)** _↑_  - proportion of outputs labeled Gulf
Arabic (GLF) by the MARBERTv2 Written Dialect Classifier [7]. Higher = more faithful Saudi style.



Saudi% = [1]

_N_



_N_

- **1** _{y_ ˆ _i_ = GLF _} ×_ 100


_i_ =1




_•_ **MSA** **leak%** _↓_ - proportion classified as MSA. Lower
= less leakage into formal MSA.



_A._ _Overall_ _Performance_


The ALLaM-LoRA-Token model achieves the strongest
overall performance, producing **84.2%** Saudi-aligned generations while limiting MSA leakage to **6.3%** . This demonstrates
the benefit of explicit dialect conditioning. In comparison,
the No-Token variant achieves 80.5% Saudi correctness but
exhibits slightly higher MSA interference.
Human evaluation corroborates these findings: the tokenbased model received the highest ratings for dialect correctness
(68.83%) and fluency (74.83%), consistent with automatic
metric trends.


_B._ _Training_ _and_ _Validation_ _Performance_


Figure 6 shows training and evaluation loss across epochs.
The token-based model converges faster and maintains lower
validation loss than the No-Token variant, underscoring the
effectiveness of explicit dialect supervision.



MSA leak% = [1]

_N_



_N_

- _p_ (MSA _| xi_ ) _×_ 100


_i_ =1



Eval Loss (token vs no_token)

|Col1|Col2|Col3|Col4|Col5|Col6|Col7|token|
|---|---|---|---|---|---|---|---|
||||||||no_token|
|||||||||
|||||||||
|||||||||
|||||||||
|||||||||



0 25 50 75 100 125 150 175 200
Step



Train Loss (token vs no_token)

|Col1|Col2|Col3|Col4|Col5|Col6|to|ken|
|---|---|---|---|---|---|---|---|
|||||||~~no~~|~~_token~~|
|||||||||
|||||||||
|||||||||
|||||||||



0 25 50 75 100 125 150 175
Step



3.0


2.8


2.6


2.4


2.2


2.0




_•_ **Low-conf%** _↓_ - fraction of outputs with classifier confidence _<_ 0 _._ 55. Lower = more stable dialect assignment.



3.5


3.0


2.5


2.0


1.5



Low-conf% = [1]

_N_



_N_

- **1** �max _p_ ( _c | xi_ ) _<_ 0 _._ 55� _×_ 100

_c_
_i_ =1




_•_ **chrF++** _↑_ - character-level _n_ -gram F-score measuring
surface overlap between generated output _hi_ and reference _ri_ [23].

chrF++ = [2] _[ ·][ P]_ [char] _[ ·][ R]_ [char]

_P_ char + _R_ char

_•_ **BERTScore F1** _↑_ - semantic similarity using contextual
embeddings [24].

BERTScore = [2] _[ ·][ P]_ [BERT] _[ ·][ R]_ [BERT]

_P_ BERT + _R_ BERT

_•_ **distinct-2/3** _↑_ - lexical diversity, ratio of unique bigrams/trigrams to total [25].


_[n]_ [-grams] _[|]_
distinct- _n_ = _[|]_ [unique]

_|_ total _n_ -grams _|_


_•_ **Self-BLEU** _↓_ - BLEU of each output _hi_ against all
others. Lower = higher variety [26].



(a) Training loss (b) Evaluation loss


Fig. 6. Training and evaluation loss curves across epochs for Token vs. NoToken models.


_C._ _Human_ _Evaluation_


To complement automatic metrics, we conducted a human
study with native Saudi speakers. Each annotator rated 40
prompts per model on a 1–5 Likert scale across three criteria:
(1) _Dialect_ _Correctness_, (2) _Fluency_ _/_ _Naturalness_, and (3)
_Task_ _Adherence_ .
Scores were normalized to percentages (5 _�→_ 100%). Table I shows that ALLaM-LoRA-Token leads on both Dialect
Correctness and Fluency while maintaining strong Task Adherence.


TABLE I
HUMAN EVALUATION RESULTS (%); HIGHER IS BETTER.


**Model** **Dialect** **%** _↑_ **Fluency** **%** _↑_ **Task** **%** _↑_


**ALLaM-LoRA-Token** **68.83** **74.83** **91.50**
ALLaM-LoRA-No-Token 66.92 72.67 88.50
AceGPT-v2-8B-Chat 28.67 31.50 90.17
Llama-3.1-8B-Instruct 28.17 31.25 72.92


_D._ _Detailed_ _Metrics_
Table II reports full evaluation results for baselines and finetuned variants. Metrics are grouped into two categories: _dialect_
_fidelity_ (Saudi%, MSA leak, Low-conf, chrF++, BERTScore)
and _diversity_ (distinct-2/3, Self-BLEU). Our LoRA models
achieve the best balance between fidelity and diversity, consistently outperforming external baselines.



Self-BLEU = [1]

_N_



_N_

- BLEU( _hi, {hj_ : _j_ = _i}_ )


_i_ =1



All models, both external baselines and fine-tuned variants,
are evaluated on the same held-out test set under this unified
pipeline.


V. EXPERIMENTAL RESULTS


We evaluate ALLaM-7B-Instruct-preview fine-tuned under
two regimes (Dialect-Token vs. No-Token) and compare them
against strong Arabic LLM baselines. Results are reported
using both automatic metrics (dialect fidelity, text quality, and
diversity) and human evaluation.


TABLE II
AUTOMATIC EVALUATION OF DIALECT FIDELITY AND DIVERSITY. ( **HIGHER** IS BETTER FOR SAUDI%, CHRF++, BERTSCORE, DISTINCT-2/3; **LOWER** IS
BETTER FOR MSA LEAK, LOW-CONF, AND SELF-BLEU). SELF-BLEU IS REPORTED ON THE 0–1 SCALE.


Model Saudi (%) _↑_ MSA leak (%) _↓_ Low-conf (%) _↓_ chrF++ _↑_ BERTScore F1 _↑_ distinct-2 _↑_ distinct-3 _↑_ Self-BLEU _↓_


AceGPT-v2-8B-Chat 67.94 22.02 6.94 21.59 0.6688 0.7902 0.9409 0.310
ALLaM-7B (base) 47.97 32.63 7.18 21.27 0.6796 0.7616 0.9142 0.017
ALLaM-LoRA-No-Token 80.50 9.26 4.55 23.70 0.7377 0.9038 0.9881 0.600
**ALLaM-LoRA-Token** **84.21** **6.21** **4.90** **24.80** **0.7386** **0.8875** **0.9838** **0.660**
Falcon-7B-Instruct 55.62 18.80 13.52 17.81 0.6321 0.7745 0.9073 0.219
JAIS-13B-Chat 28.83 44.27 10.41 15.95 0.6581 0.6933 0.8087 0.350
Llama-3.1-8B-Instruct 65.55 11.10 9.69 17.41 0.6290 0.6605 0.7957 0.051
Qwen-2.5-7B-Instruct 50.12 7.72 13.52 19.15 0.6327 0.6606 0.7957 0.061



_E._ _Comparison_ _with_ _Baselines_


Relative to AceGPT-v2-8B-Chat, Falcon-7B-Instruct,
JAIS-13B-Chat, and Llama-3.1-8B-Instruct, our finetuned variants yield higher Saudi correctness, improved
chrF++ and BERTScore, and stronger diversity. The
ALLaM-LoRA-Token variant is particularly effective,
reducing MSA leakage while maintaining stable dialectal
alignment. Both automatic and human evaluations consistently
rank our models above baselines, particularly in dialect
correctness.


_F._ _Error_ _Analysis_


Residual MSA leakage appears most often in formal
prompts, where training coverage is limited. For example:
### Prompt: �� �� ��� �� � ��� [�] � �� [�] � � � �� [�] �� � �� [�] � � [�] ��� [�] �� � � Output: � ���� [�] �� �� [�] [�] ���� [�] [�] � ���� ��������� �� �� � � � ���� ����� ��� ����� � ��


We also observe occasional repetition in short, highfrequency prompts:
### Prompt: �� � � ��� [�] [�] �� � �� � � [�] �� �� ��� [�] Output: ���� ����� [�] �� [�] ������ ����� [�] �� [�] �� (repetition pattern)


Although such errors are less frequent than in external
baselines, they highlight the need for more conversational and
stylistically varied Saudi training data. Annotators similarly
noted occasional over-formality and repetition, but these issues
were significantly less frequent in the token-based model.


VI. LIMITATIONS


Saudi-Dialect-ALLaM was trained on single-turn, synthetic,
dialect-pure text and lacks explicit supervision for instructionfollowing or multi-turn dialogue. Consequently, the model is
optimized for free-form dialectal generation rather than taskoriented dialogue or question answering, and it may drift
toward formality on out-of-distribution prompts.

Our automatic evaluation relies on the MARBERTv2 classifier’s GLF label as a proxy for Saudi usage, which can
misclassify borderline cases and does not perfectly separate
Hijazi from Najdi. Evaluation is also restricted to written text



and short outputs; we do not assess speech, code-switching,
or robustness to adversarial prompts.
The dataset’s modest size (5.5k pairs) and limited topical
coverage may introduce bias and restrict the ability to capture
rarer Saudi expressions. Future work should expand the dataset
with larger-scale instruction-tuning data, multi-turn conversations, broader safety screening, and a Saudi-specific dialect
classifier.
Finally, our human evaluation is limited in scope: only three
annotators and 100 prompts per model were used, restricted
to single-turn judgments. The use of Likert scales may also
introduce subjective bias.


VII. CONCLUSION


We curated a balanced synthetic corpus covering Hijazi and
Najdi Arabic and used it to fine-tune ALLaM-7B-Instructpreview with LoRA. Our experiments compared Dialect-Token
and No-Token strategies, showing that explicit token conditioning significantly improves dialect correctness and reduces
MSA leakage while preserving fluency and task adherence.
Both automatic metrics and human evaluation by native Saudi
speakers confirm the advantages of the token-based model,
which consistently outperforms strong external baselines. This
work highlights the value of targeted, dialect-specific resources
for adapting Arabic LLMs and provides a reproducible framework for future Saudi-centric NLP research. Future extensions
include scaling to multi-turn conversations, developing Saudispecific dialect classifiers, and expanding human evaluations.


DATA AVAILABILITY


The Saudi Dialect Instruction dataset used in this study is
**not** **publicly** **available** . We also do **not** release any model
weights or LoRA adapters. We release only training, evaluation, and inference code, configuration files (hyperparameters
and random seeds), and a datasheet describing the dataset
schema, topic taxonomy, cleaning rules, and aggregate statistics. These artifacts enable independent verification of our
results without access to the raw training data or model
weights.


RESPONSIBLE USE & LEGAL CONSIDERATIONS


Our instruction–response pairs were synthesized via APIassisted prompting and then curated. To respect provider terms
and avoid redistribution risks, we do not release the raw


dataset or any fine-tuned weights/adapters derived from it.
We instead release code, configs, and a datasheet (schema,
cleaning rules, topic taxonomy, and aggregate statistics) so
others can reproduce our pipeline on their own data. The work
complies with the licenses of all referenced models and APIs.


ACKNOWLEDGMENTS


We thank the annotators for their contributions to the
human evaluation and the Saudi NLP community for inspiring
this work. This research benefited from open-source efforts,
including ALLaM, MARBERT, and related Arabic NLP resources. We also acknowledge the use of AI tools for grammar
checking and formatting support. Finally, we thank IEEE for
providing the IEEEtran L [A] TEX template.


REFERENCES


[1] Meta AI, “Llama 3 model card,” 2024. [Online]. Available:
[https://github.com/meta-llama/llama3/blob/main/MODEL](https://github.com/meta-llama/llama3/blob/main/MODEL_CARD.md) CARD.md

[2] M. S. Bari, Y. Alnumay, N. A. Alzahrani, N. M. Alotaibi, H. A.
Alyahya, S. AlRashed, F. A. Mirza, S. Z. Alsubaie, H. A. Alahmed,
G. Alabduljabbar, R. Alkhathran, Y. Almushayqih, R. Alnajim,
S. Alsubaihi, M. Al Mansour, S. A. Hassan, M. Alrubaian,
A. Alammari, Z. Alawami, A. Al-Thubaity, A. Abdelali, J. Kuriakose,
A. Abujabal, N. Al-Twairesh, A. Alowisheq, and H. Khan, “ALLam:
Large language models for arabic and english,” in _ICLR_, 2025.

[Online]. Available: [https://openreview.net/forum?id=MscdsFVZrN](https://openreview.net/forum?id=MscdsFVZrN)

[3] N. Sengupta, S. K. Sahu, B. Jia, S. Katipomu, H. Li, F. Koto, O. M.
Afzal, S. Kamboj, O. Pandit, R. Pal, L. Pradhan, Z. M. Mujahid,
M. Baali, A. F. Aji, Z. Liu, A. Hock, A. Feldman, J. Lee, A. Jackson,
P. Nakov, T. Baldwin, and E. Xing, “Jais and jais-chat: Arabic-centric
foundation and instruction-tuned open generative large language models,” 2023.

[4] W. Antoun, F. Baly, and H. Hajj, “AraGPT2: Pre-trained transformer
for Arabic language generation,” in _Proceedings_ _of_ _the_ _Sixth_ _Arabic_
_Natural_ _Language_ _Processing_ _Workshop_ . Kyiv, Ukraine (Virtual):
Association for Computational Linguistics, Apr. 2021, pp. 196–207.

[Online]. Available: [https://www.aclweb.org/anthology/2021.wanlp-1.21](https://www.aclweb.org/anthology/2021.wanlp-1.21)

[5] A. El Filali, M. ALOUI, T. Husaain, A. Alzubaidi, B. E. A. Boussaha,
R. Cojocaru, C. Fourrier, N. Habib, and H. Hacid, “Open arabic
llm leaderboard 2,” https://huggingface.co/spaces/OALL/Open-ArabicLLM-Leaderboard, 2025.

[6] M. Abdul-Mageed, A. Elmadany, and E. M. B. Nagoudi, “Arbert &
marbert: Deep bidirectional transformers for arabic,” in _ACL_, 2021.

[Online]. Available: [https://aclanthology.org/2021.acl-long.551/](https://aclanthology.org/2021.acl-long.551/)

[7] I. Amin, “Marbertv2 arabic written dialect classifier,” 2025.

[Online]. Available: [https://huggingface.co/IbrahimAmin/marbertv2-](https://huggingface.co/IbrahimAmin/marbertv2-arabic-written-dialect-classifier)
[arabic-written-dialect-classifier](https://huggingface.co/IbrahimAmin/marbertv2-arabic-written-dialect-classifier)

[8] E. Almazrouei, H. Alobeidli, A. Alshamsi, A. Cappelli, R. Cojocaru,
M. Debbah, E. Goffinet, D. Heslow, J. Launay, Q. Malartic, B. Noune,
B. Pannier, and G. Penedo, “Falcon-40B: An open large language
model with state-of-the-art performance,” 2023. [Online]. Available:
[https://huggingface.co/tiiuae/falcon-7b-instruct](https://huggingface.co/tiiuae/falcon-7b-instruct)

[9] Falcon-LLM Team, “Falcon-arabic: A breakthrough in arabic language
models,” May 2025. [Online]. Available: [https://falcon-lm.github.io/](https://falcon-lm.github.io/blog/falcon-arabic)
[blog/falcon-arabic](https://falcon-lm.github.io/blog/falcon-arabic)

[10] Qwen Team, “Qwen2.5: A party of foundation models,” September
2024. [Online]. Available: [https://qwenlm.github.io/blog/qwen2.5/](https://qwenlm.github.io/blog/qwen2.5/)

[11] J. Liang, Z. Cai, J. Zhu, H. Huang, K. Zong, B. An, M. Alharthi, J. He,
L. Zhang, H. Li, B. Wang, and J. Xu, “Alignment at pre-training!
towards native alignment for arabic llms,” in _NeurIPS_, 2024. [Online].
Available: [https://openreview.net/forum?id=woRFmNJiLp](https://openreview.net/forum?id=woRFmNJiLp)

[12] Asharq Al-Awsat, “Humane launches allam, the first arabic artificial
intelligence model from saudi arabia, august 2025,” 2025. [Online].
Available: [https://aawsat.com/%D8%A7%D9%84%D8%A7%D9%82%](https://aawsat.com/%D8%A7%D9%84%D8%A7%D9%82%D8%AA%D8%B5%D8%A7%D8%AF/5174385-%D9%87%D9%8A%D9%88%D9%85%D8%A7%D9%8A%D9%86-%D8%A5%D8%B7%D9%84%D8%A7%D9%82-%D8%B9%D9%84%D9%91%D8%A7%D9%85-%D8%A3%D9%88%D9%84-%D9%86%D9%85%D9%88%D8%B0%D8%AC-%D8%B0%D9%83%D8%A7%D8%A1-%D8%A7%D8%B5%D8%B7%D9%86%D8%A7%D8%B9%D9%8A-%D8%B9%D8%B1%D8%A8%D9%8A-%D9%85%D9%86-%D8%A7%D9%84%D8%B3%D8%B9%D9%88%D8%AF%D9%8A%D8%A9-%D8%A3%D9%88%D8%A7%D8%AE%D8%B1-%D8%A3%D8%BA%D8%B3%D8%B7%D8%B3)
[D8%AA%D8%B5%D8%A7%D8%AF/5174385-%D9%87%D9%8A%](https://aawsat.com/%D8%A7%D9%84%D8%A7%D9%82%D8%AA%D8%B5%D8%A7%D8%AF/5174385-%D9%87%D9%8A%D9%88%D9%85%D8%A7%D9%8A%D9%86-%D8%A5%D8%B7%D9%84%D8%A7%D9%82-%D8%B9%D9%84%D9%91%D8%A7%D9%85-%D8%A3%D9%88%D9%84-%D9%86%D9%85%D9%88%D8%B0%D8%AC-%D8%B0%D9%83%D8%A7%D8%A1-%D8%A7%D8%B5%D8%B7%D9%86%D8%A7%D8%B9%D9%8A-%D8%B9%D8%B1%D8%A8%D9%8A-%D9%85%D9%86-%D8%A7%D9%84%D8%B3%D8%B9%D9%88%D8%AF%D9%8A%D8%A9-%D8%A3%D9%88%D8%A7%D8%AE%D8%B1-%D8%A3%D8%BA%D8%B3%D8%B7%D8%B3)
[D9%88%D9%85%D8%A7%D9%8A%D9%86-%D8%A5%D8%B7%](https://aawsat.com/%D8%A7%D9%84%D8%A7%D9%82%D8%AA%D8%B5%D8%A7%D8%AF/5174385-%D9%87%D9%8A%D9%88%D9%85%D8%A7%D9%8A%D9%86-%D8%A5%D8%B7%D9%84%D8%A7%D9%82-%D8%B9%D9%84%D9%91%D8%A7%D9%85-%D8%A3%D9%88%D9%84-%D9%86%D9%85%D9%88%D8%B0%D8%AC-%D8%B0%D9%83%D8%A7%D8%A1-%D8%A7%D8%B5%D8%B7%D9%86%D8%A7%D8%B9%D9%8A-%D8%B9%D8%B1%D8%A8%D9%8A-%D9%85%D9%86-%D8%A7%D9%84%D8%B3%D8%B9%D9%88%D8%AF%D9%8A%D8%A9-%D8%A3%D9%88%D8%A7%D8%AE%D8%B1-%D8%A3%D8%BA%D8%B3%D8%B7%D8%B3)
[D9%84%D8%A7%D9%82-%D8%B9%D9%84%D9%91%D8%A7%](https://aawsat.com/%D8%A7%D9%84%D8%A7%D9%82%D8%AA%D8%B5%D8%A7%D8%AF/5174385-%D9%87%D9%8A%D9%88%D9%85%D8%A7%D9%8A%D9%86-%D8%A5%D8%B7%D9%84%D8%A7%D9%82-%D8%B9%D9%84%D9%91%D8%A7%D9%85-%D8%A3%D9%88%D9%84-%D9%86%D9%85%D9%88%D8%B0%D8%AC-%D8%B0%D9%83%D8%A7%D8%A1-%D8%A7%D8%B5%D8%B7%D9%86%D8%A7%D8%B9%D9%8A-%D8%B9%D8%B1%D8%A8%D9%8A-%D9%85%D9%86-%D8%A7%D9%84%D8%B3%D8%B9%D9%88%D8%AF%D9%8A%D8%A9-%D8%A3%D9%88%D8%A7%D8%AE%D8%B1-%D8%A3%D8%BA%D8%B3%D8%B7%D8%B3)
[D9%85-%D8%A3%D9%88%D9%84-%D9%86%D9%85%D9%88%](https://aawsat.com/%D8%A7%D9%84%D8%A7%D9%82%D8%AA%D8%B5%D8%A7%D8%AF/5174385-%D9%87%D9%8A%D9%88%D9%85%D8%A7%D9%8A%D9%86-%D8%A5%D8%B7%D9%84%D8%A7%D9%82-%D8%B9%D9%84%D9%91%D8%A7%D9%85-%D8%A3%D9%88%D9%84-%D9%86%D9%85%D9%88%D8%B0%D8%AC-%D8%B0%D9%83%D8%A7%D8%A1-%D8%A7%D8%B5%D8%B7%D9%86%D8%A7%D8%B9%D9%8A-%D8%B9%D8%B1%D8%A8%D9%8A-%D9%85%D9%86-%D8%A7%D9%84%D8%B3%D8%B9%D9%88%D8%AF%D9%8A%D8%A9-%D8%A3%D9%88%D8%A7%D8%AE%D8%B1-%D8%A3%D8%BA%D8%B3%D8%B7%D8%B3)
[D8%B0%D8%AC-%D8%B0%D9%83%D8%A7%D8%A1-%D8%](https://aawsat.com/%D8%A7%D9%84%D8%A7%D9%82%D8%AA%D8%B5%D8%A7%D8%AF/5174385-%D9%87%D9%8A%D9%88%D9%85%D8%A7%D9%8A%D9%86-%D8%A5%D8%B7%D9%84%D8%A7%D9%82-%D8%B9%D9%84%D9%91%D8%A7%D9%85-%D8%A3%D9%88%D9%84-%D9%86%D9%85%D9%88%D8%B0%D8%AC-%D8%B0%D9%83%D8%A7%D8%A1-%D8%A7%D8%B5%D8%B7%D9%86%D8%A7%D8%B9%D9%8A-%D8%B9%D8%B1%D8%A8%D9%8A-%D9%85%D9%86-%D8%A7%D9%84%D8%B3%D8%B9%D9%88%D8%AF%D9%8A%D8%A9-%D8%A3%D9%88%D8%A7%D8%AE%D8%B1-%D8%A3%D8%BA%D8%B3%D8%B7%D8%B3)



[A7%D8%B5%D8%B7%D9%86%D8%A7%D8%B9%D9%8A-%D8%](https://aawsat.com/%D8%A7%D9%84%D8%A7%D9%82%D8%AA%D8%B5%D8%A7%D8%AF/5174385-%D9%87%D9%8A%D9%88%D9%85%D8%A7%D9%8A%D9%86-%D8%A5%D8%B7%D9%84%D8%A7%D9%82-%D8%B9%D9%84%D9%91%D8%A7%D9%85-%D8%A3%D9%88%D9%84-%D9%86%D9%85%D9%88%D8%B0%D8%AC-%D8%B0%D9%83%D8%A7%D8%A1-%D8%A7%D8%B5%D8%B7%D9%86%D8%A7%D8%B9%D9%8A-%D8%B9%D8%B1%D8%A8%D9%8A-%D9%85%D9%86-%D8%A7%D9%84%D8%B3%D8%B9%D9%88%D8%AF%D9%8A%D8%A9-%D8%A3%D9%88%D8%A7%D8%AE%D8%B1-%D8%A3%D8%BA%D8%B3%D8%B7%D8%B3)
[B9%D8%B1%D8%A8%D9%8A-%D9%85%D9%86-%D8%A7%D9%](https://aawsat.com/%D8%A7%D9%84%D8%A7%D9%82%D8%AA%D8%B5%D8%A7%D8%AF/5174385-%D9%87%D9%8A%D9%88%D9%85%D8%A7%D9%8A%D9%86-%D8%A5%D8%B7%D9%84%D8%A7%D9%82-%D8%B9%D9%84%D9%91%D8%A7%D9%85-%D8%A3%D9%88%D9%84-%D9%86%D9%85%D9%88%D8%B0%D8%AC-%D8%B0%D9%83%D8%A7%D8%A1-%D8%A7%D8%B5%D8%B7%D9%86%D8%A7%D8%B9%D9%8A-%D8%B9%D8%B1%D8%A8%D9%8A-%D9%85%D9%86-%D8%A7%D9%84%D8%B3%D8%B9%D9%88%D8%AF%D9%8A%D8%A9-%D8%A3%D9%88%D8%A7%D8%AE%D8%B1-%D8%A3%D8%BA%D8%B3%D8%B7%D8%B3)
[84%D8%B3%D8%B9%D9%88%D8%AF%D9%8A%D8%A9-%D8%](https://aawsat.com/%D8%A7%D9%84%D8%A7%D9%82%D8%AA%D8%B5%D8%A7%D8%AF/5174385-%D9%87%D9%8A%D9%88%D9%85%D8%A7%D9%8A%D9%86-%D8%A5%D8%B7%D9%84%D8%A7%D9%82-%D8%B9%D9%84%D9%91%D8%A7%D9%85-%D8%A3%D9%88%D9%84-%D9%86%D9%85%D9%88%D8%B0%D8%AC-%D8%B0%D9%83%D8%A7%D8%A1-%D8%A7%D8%B5%D8%B7%D9%86%D8%A7%D8%B9%D9%8A-%D8%B9%D8%B1%D8%A8%D9%8A-%D9%85%D9%86-%D8%A7%D9%84%D8%B3%D8%B9%D9%88%D8%AF%D9%8A%D8%A9-%D8%A3%D9%88%D8%A7%D8%AE%D8%B1-%D8%A3%D8%BA%D8%B3%D8%B7%D8%B3)
[A3%D9%88%D8%A7%D8%AE%D8%B1-%D8%A3%D8%BA%D8%](https://aawsat.com/%D8%A7%D9%84%D8%A7%D9%82%D8%AA%D8%B5%D8%A7%D8%AF/5174385-%D9%87%D9%8A%D9%88%D9%85%D8%A7%D9%8A%D9%86-%D8%A5%D8%B7%D9%84%D8%A7%D9%82-%D8%B9%D9%84%D9%91%D8%A7%D9%85-%D8%A3%D9%88%D9%84-%D9%86%D9%85%D9%88%D8%B0%D8%AC-%D8%B0%D9%83%D8%A7%D8%A1-%D8%A7%D8%B5%D8%B7%D9%86%D8%A7%D8%B9%D9%8A-%D8%B9%D8%B1%D8%A8%D9%8A-%D9%85%D9%86-%D8%A7%D9%84%D8%B3%D8%B9%D9%88%D8%AF%D9%8A%D8%A9-%D8%A3%D9%88%D8%A7%D8%AE%D8%B1-%D8%A3%D8%BA%D8%B3%D8%B7%D8%B3)
[B3%D8%B7%D8%B3](https://aawsat.com/%D8%A7%D9%84%D8%A7%D9%82%D8%AA%D8%B5%D8%A7%D8%AF/5174385-%D9%87%D9%8A%D9%88%D9%85%D8%A7%D9%8A%D9%86-%D8%A5%D8%B7%D9%84%D8%A7%D9%82-%D8%B9%D9%84%D9%91%D8%A7%D9%85-%D8%A3%D9%88%D9%84-%D9%86%D9%85%D9%88%D8%B0%D8%AC-%D8%B0%D9%83%D8%A7%D8%A1-%D8%A7%D8%B5%D8%B7%D9%86%D8%A7%D8%B9%D9%8A-%D8%B9%D8%B1%D8%A8%D9%8A-%D9%85%D9%86-%D8%A7%D9%84%D8%B3%D8%B9%D9%88%D8%AF%D9%8A%D8%A9-%D8%A3%D9%88%D8%A7%D8%AE%D8%B1-%D8%A3%D8%BA%D8%B3%D8%B7%D8%B3)

[13] F. Qarah, “Saudibert: A large language model pretrained on saudi dialect
corpora,” _arXiv_ _preprint_ _arXiv:2405.06239_, 2024.

[14] M. Abdul-Mageed, A. Elmadany, and E. M. B. Nagoudi, “Arbert &
marbert: Deep bidirectional transformers for arabic,” in _Proceedings_
_of_ _the_ _59th_ _Annual_ _Meeting_ _of_ _the_ _Association_ _for_ _Computational_
_Linguistics_ _and_ _the_ _11th_ _International_ _Joint_ _Conference_ _on_ _Natural_
_Language_ _Processing_ _(Volume_ _1:_ _Long_ _Papers)_ . misc: Association
for Computational Linguistics, Aug. 2021, pp. 7088–7105. [Online].
Available: [https://aclanthology.org/2021.acl-long.551](https://aclanthology.org/2021.acl-long.551)

[15] H. Chouikhi, M. Aloui, C. Ben Hammou, G. Chaabane, H. Kchaou,
and C. Dhaouadi, “Gemmar: Enhancing llms through arabic instructiontuning,” _arXiv_ _preprint_ _arXiv:2407.02147_, 2024. [Online]. Available:
[https://arxiv.org/abs/2407.02147](https://arxiv.org/abs/2407.02147)

[16] ——, “Llamar & gemmar: Enhancing llms through arabic instructiontuning,” 2024.

[17] H. Abu-Rayyash and N. Alanazi, “Saudial: The saudi arabic
dialects game localization dataset,” 2025. [Online]. Available: [https:](https://data.mendeley.com/datasets/mzdwkb2t6d/2)
[//data.mendeley.com/datasets/mzdwkb2t6d/2](https://data.mendeley.com/datasets/mzdwkb2t6d/2)

[18] S. S. Alahmari, “SADSLyC: A corpus for saudi Arabian multi-dialect
identification through song lyrics,” in _Proceedings_ _of_ _the_ _4th_ _Workshop_
_on_ _Arabic_ _Corpus_ _Linguistics_ _(WACL-4)_, S. Ezzini, H. Alami,
I. Berrada, A. Benlahbib, A. El Mahdaouy, S. Lamsiyah, H. Derrouz,
A. Haddad, M. Jarrar, M. El-Haj, R. Mitkov, and P. Rayson, Eds. Abu
Dhabi, UAE: Association for Computational Linguistics, Jan. 2025, pp.
38–43. [Online]. Available: [https://aclanthology.org/2025.wacl-1.4/](https://aclanthology.org/2025.wacl-1.4/)

[19] National Center for Artificial Intelligence (SDAIA) and Saudi
Broadcasting Authority, “Sada: Saudi audio dataset for arabic,”
2022, 667 hours of Saudi Arabic audio with transcripts across 57
TV programs. [Online]. Available: [https://www.kaggle.com/datasets/](https://www.kaggle.com/datasets/sdaiancai/sada2022)
[sdaiancai/sada2022](https://www.kaggle.com/datasets/sdaiancai/sada2022)

[20] A. Vaswani, N. Shazeer, N. Parmar, J. Uszkoreit, L. Jones, A. N. Gomez,
Ł. Kaiser, and I. Polosukhin, “Attention is all you need,” in _Advances_
_in_ _Neural_ _Information_ _Processing_ _Systems_ _(NeurIPS)_, vol. 30, 2017,
pp. 5998–6008. [Online]. Available: [https://arxiv.org/abs/1706.03762](https://arxiv.org/abs/1706.03762)

[21] E. J. Hu, Y. Shen, P. Wallis, Z. Allen-Zhu, Y. Li, L. Wang,
and W. Wang, “Lora: Low-rank adaptation of large language
models,” _arXiv_ _preprint_ _arXiv:2106.09685_, 2021. [Online]. Available:
[https://doi.org/10.48550/arXiv.2106.09685](https://doi.org/10.48550/arXiv.2106.09685)

[22] A. Holtzman, J. Buys, L. Du, M. Forbes, and Y. Choi, “The
curious case of neural text degeneration,” in _International_ _Conference_
_on_ _Learning_ _Representations_ _(ICLR)_, 2020. [Online]. Available:
[https://arxiv.org/abs/1904.09751](https://arxiv.org/abs/1904.09751)

[23] M. Popovi´c, “chrf++: words helping character n-grams,” in _Proceedings_
_of the Second Conference on Machine Translation (WMT)_ . Copenhagen,
Denmark: Association for Computational Linguistics, Sep. 2017, pp.
612–618. [Online]. Available: [https://aclanthology.org/W17-4770/](https://aclanthology.org/W17-4770/)

[24] T. Zhang, V. Kishore, F. Wu, K. Q. Weinberger, and Y. Artzi,
“Bertscore: Evaluating text generation with bert,” in _International_
_Conference_ _on_ _Learning_ _Representations_ _(ICLR)_, 2020. [Online].
Available: [https://arxiv.org/abs/1904.09675](https://arxiv.org/abs/1904.09675)

[25] J. Li, M. Galley, C. Brockett, J. Gao, and B. Dolan, “A diversitypromoting objective function for neural conversation models,” in
_Proceedings_ _of_ _the_ _2016_ _Conference_ _of_ _the_ _North_ _American_ _Chapter_
_of_ _the_ _Association_ _for_ _Computational_ _Linguistics:_ _Human_ _Language_
_Technologies_ _(NAACL-HLT)_ . San Diego, California: Association for
Computational Linguistics, 2016, pp. 110–119. [Online]. Available:
[https://aclanthology.org/N16-1014/](https://aclanthology.org/N16-1014/)

[26] Y. Zhu, S. Lu, L. Zheng, J. Guo, W. Zhang, J. Wang, and
Y. Yu, “Texygen: A benchmarking platform for text generation
models,” _arXiv_ _preprint_ _arXiv:1802.01886_, 2018. [Online]. Available:
[https://arxiv.org/abs/1802.01886](https://arxiv.org/abs/1802.01886)


