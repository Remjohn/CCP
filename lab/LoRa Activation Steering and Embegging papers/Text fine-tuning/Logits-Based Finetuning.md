### **Logits-Based Finetuning**

**Jingyao Li** **[1]** **, Senqiao Yang** **[1]** **, Sitong Wu** **[1]** **, Han Shi** **[2]** **, Chuanyang Zheng** **[1]** **, Hong Xu** **[1]** **, Jiaya Jia** **[3]**


1The Chinese University of Hong Kong
2Huawei Noah’s Ark Lab
3Hong Kong University of Science and Technology



**Abstract**


In recent years, developing compact and efficient large language models (LLMs) has
emerged as a thriving area of research. Traditional Supervised Fine-Tuning (SFT), which
relies on singular ground truth labels, often fails
to capture token-level dependencies and linguistic diversity. To address these limitations, we
propose a logits-based fine-tuning framework
that integrates the strengths of supervised learning and knowledge distillation. Our approach
constructs enriched training targets by combining teacher logits with ground truth labels, preserving both correctness and linguistic diversity.
This ensures more reliable and effective training. We constructed a large-scale 1.2M logits
dataset and trained a series of science-focused
models. Experimental results demonstrate
that our method achieves significant improvements, with accuracy gains of 18% on Mawps
and 22.7% on TabMWP. Across nine widely
used mathematical benchmarks, our method
consistently outperforms prior SFT models,
achieving an average improvement of 7.28%.
[Codes are available at https://github.com/dvlab-](https://github.com/dvlab-research/Logits-Based-Finetuning)
[research/Logits-Based-Finetuning.](https://github.com/dvlab-research/Logits-Based-Finetuning)


**1** **Introduction**


Large language models (LLMs) have demonstrated
remarkable capabilities across a wide range of
NLP tasks (Brown et al., 2020; Thoppilan et al.,
2022; Chowdhery et al., 2022; OpenAI, 2023; Anil
et al., 2023), yet their immense computational demands pose significant challenges for deployment
in resource-constrained environments.
To address this, researchers have focused on developing compact and efficient LLMs, with Supervised Fine-Tuning (SFT) as a widely adopted
approach. However, SFT suffers from inherent limitations, particularly its inability to capture intertoken relationships and linguistic diversity. For
instance, as illustrated in Fig. 2, multiple valid expressions of the same idea, such as "There are 12



Figure 1: Conceptual overview of our logits-based distillation framework. (Up) Traditional supervised finetuning relies on singular ground truth labels, failing to
capture valid linguistic variations (e.g., "The cat is on
the mat" vs. "The cat lies on the mat"). (Down) Our
approach combines teacher model logits with ground
truth verification to create enriched training targets that
preserve both correctness and expression diversity.


inches in 1 foot" and "There are 12 inches in each
foot," highlight the nuanced token-level dependencies that SFT often overlooks. This limitation stems
from SFT’s reliance on singular ground truth labels
or teacher outputs, which fail to account for the
richness of alternative phrasings. Consequently,
the benefits of SFT are constrained by its inability
to fully exploit the intrinsic relationships between
tokens.
Distillation methods have proven successful in
creating lightweight and efficient models. For
example, models like BERT (Rusu et al., 2015;
Sanh et al., 2019; Jianping et al., 2021) have
demonstrated that distillation-based approaches
can achieve superior performance compared to direct training methods, offering both efficiency and
effectiveness. However, applying distillation to
LLMs presents unique challenges. First, the uncontrollability of teacher outputs poses a significant



CE Loss


KL Loss



**GT**



Where is the cat?


The cat **is** on the mat.


The cat **lies** on the mat.



The cat ?



is


lies


rests​


sits


stays


sleeps





1


hurdle. Even well-trained large language models,
such as LLaMA3.1-70B-instruct, can generate hallucinated or erroneous predictions, as shown in
Tab. 1. Relying solely on such outputs as supervision signals is unreliable and often necessitates
manual intervention to ensure high-quality annotations. Second, the computational cost of large-scale
distillation is prohibitive, as LLMs require substantial GPU memory, making direct online teacherstudent distillation impractical for many applications.

To address these challenges, we propose a novel
logits-based fine-tuning framework that integrates
the strengths of supervised learning and knowledge distillation. Our approach constructs enriched
training targets by combining teacher logits with
ground truth labels, preserving both correctness
and linguistic diversity. Unlike traditional distillation methods, which transfer teacher predictions
directly, our method creates a balanced target distribution that enhances the student model’s ability to
learn from both the teacher’s knowledge and taskspecific supervision. This ensures more reliable
and informed training while mitigating the risks
associated with erroneous teacher outputs.

In this work, we constructed a large-scale 1.2M
logits dataset and trained a series of sciencefocused models using our method. Experimental results show that our approach surpasses the
previous state-of-the-art methods on Mawps and
TabMWP by 18% and 22.7% in accuracy, respectively. Across nine widely used mathematical
benchmarks, our method consistently outperforms
prior SFT models, with an average improvement of
7.28%, highlighting the method’s robustness and
generalizability.

In summary, the main contributions of our work
are as follows:


1. We propose a simple yet effective logitsbased instruction tuning method that enhances
model performance by integrating teacher
knowledge with ground truth labels.
2. We release a 1.2M science logits dataset, enabling future research and development of
logits-based training methods.
3. We train and evaluate a series of sciencefocused models using our method. Our
models achieve significant improvements
over state-of-the-art supervised fine-tuning approaches, with an average accuracy gain of
7.28% across nine benchmarks.



**2** **Preliminaries**


In this section, we establishes the theoretical foundation for our logits-based fine-tuning approach.
We first formalize auto-regressive sequence modeling and then analyze existing knowledge distillation paradigms, highlighting their limitations that
motivate our method.


**2.1** **Auto-regressive Sequence Models**


We first define key components of sequence modeling. For any sequence pair, _x_ represents the
input and _y_ the output. The vocabulary V contains _M_ distinct tokens. We use _y<n_ +1 =
( _y_ 1 _, y_ 2 _, . . ., yn_ ) to represent the first _n_ tokens. An
auto-regressive model generates a probability distribution _p_ ( _.|y<n, x_ ) _∈_ [0 _,_ 1] _[M]_ over the vocabulary V
, considering both input _x_ and previous tokens _y<n_ .
When sampling, _y_ _∼_ _p_ ( _·|x_ ) produces a complete
output sequence. For brevity, we write _p_ ( _yn|x_ )
instead of _p_ ( _yn|y<n, x_ ). The generation process
predicts tokens sequentially. Each token probability _p_ ( _yn|x_ ) is computed using a temperaturecontrolled softmax:

_e_ _[z][n][/τ]_
_p_ ( _yn|x_ ) =      - _M_ _[,]_ (1)
_i_ =1 _[e][z][i][/τ]_

where _zn_ represents the logit for token _yn_, and _τ_
controls output randomness. Higher _τ_ increases
diversity, while lower values produce more focused
predictions. During student training, _τ_ = 1, while
evaluation uses greedy sampling ( _τ_ _→_ 0).


**2.2** **Distillation for Auto-regressive Models**


**KL-Based Divergences.** The Kullback-Leibler
(KL) divergence is a fundamental measure that
quantifies the difference between two probability
distributions. For two discrete probability distributions _P_ ( _·|x_ ) and _Q_ ( _·|x_ ) defined over the probability space _X_, the KL divergence is defined as (Hinton et al., 2015):



This measure is always non-negative and equals
zero if and only if the two distributions are identical.


**Supervised FT.** Given a fixed dataset of target
sequences, one simple strategy involves maximizing the student’s negative log-likelihood on these
sequences:


_LSFT_ ( _θ_ ) = E( _x,y_ ) _∼_ ( _X,Y_ )� _−_ log _p_ _[θ]_ S [(] _[y][|][x]_ [)]  - _._ (3)





_P_ ( _·|x_ ) log _[P]_ [(] _[·|][x]_ [)]

_Q_ ( _·|x_ )

_x∈X_



_DKL_ ( _P_ _|Q_ ) = 


(2)
_Q_ ( _·|x_ ) _[.]_



2


**Instruction**
Roger’s age is 5 more than twice Jill’s age. In 15 years, their age difference will be 30 years less than Finley’s age.
If Jill is 20 years old now, how old is Finley?


**Teacher Annotations** **Human Annotations**
Let’s break down the problem step by step. Twice Jill’s age is 2 _×_ 20 = 40.
First, we know that Jill is 20 years old now. We also If Roger’s age is 5 more than twice Jill’s age, he is
know that Roger’s age is 5 more than twice Jill’s age. So, 5+40=45 years old.
Roger’s age is 2 _×_ 20 + 5 = 45. In 15 years, Jill will be 20+15=35 years old.
In 15 years, Jill will be 20 + 15 = 35 years old, and Roger Roger’s age will be 45+15=60 years old in 15 years.
will be 45 + 15 = 60 years old. The problem states that The age difference between Roger and Jill in fifteen years
their age difference will be 30 years less than Finley’s age. will be 60-35=25 years.
So, we can set up the equation: In 15 years, the age difference between Roger and Jill will
60 - 35 = Finley’s age - 30 be 30 years less than Finley’s age, meaning in fifteen years
Simplifying the equation, we get: Finley will be 30+25=55 years old.
25 = Finley’s age - 30 Currently, Finley is **55-15=40** years old.
Adding 30 to both sides, we get:
Finley’s age = 55
Therefore, Finley is **55** years old now.


Table 1: An example from GSM8K (Cobbe et al., 2021) generated by teacher model, LLaMA3.1-70B-instruct. The
teacher model incorrectly interprets Finley’s age 15 years from now as his current age, leading to an erroneous
conclusion.



**Sequence-Level KD** (Kim and Rush, 2016a) extends this concept by training on teacher-generated
outputs _YT_ . This approach optimizes:


_LSeqKD_ ( _θ_ ) = E( _x,y_ ) _∼_ ( _X,YT_ )� _−_ log _p_ _[θ]_ S [(] _[y][|][x]_ [)] - _._ (4)


**Supervised KD** (Hinton et al., 2015) represents
a widely used distillation method where students
learn to match their teacher’s token-level probability distributions. The training objective minimizes
the KL divergence between teacher and student
distributions:


            -            _LSD_ ( _θ_ ) := E( _x,y_ ) _∼_ ( _X,YT_ ) _DKL_ - _p_ T _|p_ _[θ]_ S�( _y|x_ ) _,_
(5)


**3** **Logits-based Finetuning**


In this section, we first introduce the motivation
behind our logits-based fine-tuning approach in
Sec. 3.1. Then, in Sec. 3.2, we present the proposed
distribution, which integrates teacher model logits
with ground truth outputs. In Sec. 3.3, we describe
the construction of our logits dataset. Finally, in
Sec. 3.4, we detail our fine-tuning method.


**3.1** **Motivation**


To justify the proposal of the Logits-Based FineTuning method for improving small LLMs, we
first analyze the limitations of traditional widely
used method Supervised Fine-Tuning (SFT), and
the current distillation method Sequence-Level
Knowledge Distillation (SeqKD, Kim and Rush



(2016a)), and Supervised Distillation (SD, Hinton
et al. (2015)):


**Lack of Inter-Token Relationships.** For traditional SFT, the major issue is the lack of inter-token
relationships. Specifically, there may be multiple
expressions for the same idea, such as _There are_
_12 inches in 1 foot_ and _There are 12 inches in each_
_foot_ illustrated in Fig. 2. These alternative labels
reflect the model’s understanding of the intrinsic
relationships between tokens, which may not be
captured through singular annotations.


**Uncontrollability of Teacher Outputs.** Besides,
for the distillation method, the outputs from LLMs
are often uncontrollable; even well-trained models can produce erroneous or hallucinatory results.
For instance, as shown in Tab. 1, the well-trained
LLaMA3.1-70B-instruct model erroneously interprets Finley’s age 15 years from now as his current
age, resulting in incorrect conclusions. Therefore,
relying solely on the outputs of LLMs as supervision for models is unreliable and necessitates
human intervention to generate validated results.


**3.2** **Target Distribution Analysis**


To address these limitations, we aim to propose a
approach that enables the student model to learn
from both reliably annotated labels and the intrinsic
knowledge embedded in the teacher model.


**Problem Setup.** Consider two sequence models
with auto-regressive architectures: _p_ S (student) and



3


+ �� ��



��� + �� ��



Figure 2: Illustration of token probability distribution generation. The input tokens concated with ground truth
are processed by the teacher model, which predicts the next token probabilities _pT_ . Then the ground truth one-hot
vector _PGT_ is combined with the teacher’s top-K probabilities _pT_ to generate the proposed distribution _p_ our using
Eq. (7).



_p_ T (teacher), with different model capacities. The
student model has trainable parameters _θ_, and _p_ _[θ]_ S
maintains differentiability with respect to _θ_ . The
setup includes an input dataset _X_ . We define the
token-level distribution discrepancy between _p_ T
and _p_ S as:


_D_ - _p_ T _∥p_ _[θ]_ S�( _y|x_ )



_p_ GT( _yi_ ) = _{p_ GT _j_ ( _yi_ ) _}_ _[M]_ _j_ =1 _[∈]_ [[0] _[,]_ [ 1]] _[M]_ [, where]



_p_ GT( _yi_ ) _[j]_ =




1 _,_ if _j_ = _yi,_
(8)
0 _,_ otherwise _._



We define this distribution because it satisfies the
following constraints.


**Constraint 1.** To ensure that the greedy search on
the new distribution _q_ still yields the ground truth
_yi_, we require that the value _q_ ( _yi_ ) be the largest
at the ground truth index. Mathematically, this is
expressed as:


_qyi_ ( _yi_ ) _≥_ _qj_ ( _yi_ ) _,_ _∀_ 1 _≤_ _j_ _≤_ _M, j_ = _yi_ (9)


This constraint guarantees that the argmax of _q_ ( _yi_ )
remains _yi_, preserving the ground truth prediction.


**Constraint** **2.** We aim to maintain the relative
proportions of the top _K_ candidates from the original distribution _p_ T( _yi_ ) in the new distribution _q_ .
The constraint is formulated as:


_qj_ ( _yi_ )
_qk_ ( _yi_ ) [=] _p_ _[p]_ T [T] ( [(] _y_ _[y]_ _i_ _[i]_ ) [)] _k_ _[j]_ _,_ _∀j, k_ _∈_ Top _K_ ( _yi_ ) _, j, k_ = _yi_

(10)
This ensures that the proportional relationship between the probabilities determined by the original
distribution is preserved in the new distribution.


**Constraint** **3.** For indices outside the ground
truth and the top _K_ candidates, we require their
values in _q_ to be not larger than those within the set
_S_ = _{yi} ∪_ Top _Kp_ T( _yi_ ). This is expressed as:


_qj_ ( _yi_ ) _≤_ _qk_ ( _yi_ ) _,_ _∀j_ _∈/_ _S, ∀k_ _∈_ _S_ (11)



:= [1]

_Ly_



_Ly_ (6)

- _D_ - _p_ T( _·|y<n, x_ ) _∥p_ _[θ]_ S [(] _[·|][y][<n][, x]_ [)] - _,_

_n_ =1



where _x_ and _y_ denote the input and output sequences and _D_ represents divergence measure.


**Definition.** Let _M_ represent the vocabulary size
and _yi_ denote the _i_ -th ground truth index, where
0 _< yi_ _< M_ . The target distribution is denoted as
_q_ . Specifically, _qj_ ( _yi_ ) represents the value at the
_j_ -th position in the vocabulary for the _i_ -th token’s
logits in the target logits _q_ . Storing a vocabulary of
millions of tokens incurs significant storage overhead. Therefore, we retain only the sparse teacher
logits of the top _K_ instead of the complete set. For
simplicity, all subsequent references to _p_ T logits
refer to the Top-K sparsified results. We define
Top _Kp_ T( _yi_ ) = Top _K,_ 1 _≤j≤M_ _p_ T( _yi_ ).


**Proposed Distribution.** We propose our probability distribution _p_ L as follows:


_p_ T( _yi_ ) + _p_ GT( _yi_ )
_p_ L( _yi_ ) = _,_ (7)
_∥p_ T( _yi_ ) + _p_ GT( _yi_ ) _∥_ 1


where _∥· ∥_ 1 denotes the L1 norm. _p_ GT( _yi_ ) is the
one-hot encoded ground truth label. Specifically,



4


**Algorithm 1** Logits Dataset Generation Procedure


**Require:** Teacher model _p_ T, Dataset ( _X, Y_ ) =
( _xi, yi,_ ) _[N]_ _i_ =1
**Ensure:** Logits-based Dataset ( _X, Y, P_ L) =
( _xi, yi, p_ L _i_ ) _[N]_ _i_ =1
1: **for** each ( _x, y_ ) _∈_ ( _X, Y_ ) **do**

2: Compute Top- _K_ teacher logits _p_ T _←_ _T_ ( _x_ )

3: Create one-hot ground truth _p_ GT using
Eq. (8).

4: Compute _p_ L using Eq. (7).

5: **end for**

6: **return** Logits-based Dataset ( _X, Y, P_ L) =
( _xi, yi, p_ L _i_ ) _[N]_ _i_ =1


**Algorithm 2** Logits-based Finetuning Procedure

**Require:** Student model _p_ _[θ]_ S [, Logits-based Dataset]
( _X, Y, P_ L), Divergence _D_, learning rate _η_
**Ensure:** Trained student model _p_ _[θ]_ S
1: **for** batch _B_ _∈_ ( _X, Y, P_ L) **do**

2: Update student parameters _θ_ by minimizing
_L_ L (Eq. (13)):



_θ_ _←_ _θ −_ _η_ [1]

_B_


3: **end for**




 - _∇θD_ ( _p_ L _∥p_ _[θ]_ S [)(] _[y][|][x]_ [)]

( _x,y,p_ L) _∈B_



4: **return** Trained student model _p_ _[θ]_ S


This constraint helps in focusing the probability
mass on the ground truth and the top candidates,
reducing the influence of less relevant tokens.


**Constraint 4.** Finally, the new distribution _q_ ( _yi_ )
must be a valid probability distribution. This implies that each element must be within the range

[0, 1], and the sum of all elements must equal 1.
Mathematically:



pairs and enriches it with target distributions derived from a pre-trained teacher model.
For each input-target pair ( _x, y_ ), the teacher
model _p_ T is first used to compute the full logits
vector for input _x_, which is then sparsified by retaining only the top _K_ logits, denoted as _p_ T( _x_ ).
This sparsification is crucial for reducing storage
requirements and focusing on the teacher’s most
confident predictions. Concurrently, a one-hot vector _p_ GT( _y_ ) is created based on the ground truth
label _y_, as defined in Equation 8. The final target
distribution _p_ L( _y_ ) is then computed using Equation 7, which combines the sparsified teacher logits
_p_ T( _x_ ) and the one-hot ground truth vector _p_ GT( _y_ ).
This combination balances the teacher’s knowledge
with the emphasis on the correct target label. The
resulting logits-based dataset ( _X, Y, P_ L) is then
used to fine-tune a student model, leveraging the
target distributions for improved knowledge transfer.


**Dataset Details.** Table 2 presents the results of
supervised fine-tuning of LLaMA3.2-1B-Instruct
on a variety of mathematical reasoning datasets,
including Socratic (Yue et al., 2024), StackExchange (Yue et al., 2024), Camel-AI (Li
et al., 2023), MathInstruct (Jiang et al., 2024),
GSM8K (Cobbe et al., 2021), MetaMath (Yu
et al., 2023), MetaMath-GSM8K (Yu et al., 2023),
and OpenMathInstruct2 (Toshniwal et al., 2024).
Among them, OpenMathInstruct2 demonstrates the
strongest overall performance, achieving the highest average score (24.6%) and outperforming other
datasets on most dataset yields competitive performance (23.8%) and the best result on the Olympiad
Bench. These results suggest that datasets like
MetaMath-GSM8K and OpenMathInstruct2 can
lead to more robust and generalizable mathematical reasoning capabilities. Therefore, our final
1.2M logits dataset consists of 1M samples from
MetaMath-GSM8K and 240K from OpenMathInstruct2. More details are shown in Appendix B.
The teacher model utilized for logits generation is
LLaMA3.1-70B-Instruct (AI@Meta, 2024).


**3.4** **Finetuning Method**


Using the proposed distribution _pL_ mentioned
above, we fine-tune the student model.


**Loss** **Function.** Our Logits-based Finetuning
(LFT) method uses the Kullback-Leibler (KL) divergence as the loss function to train the student



_q_ ( _yi_ ) _∈_ [0 _,_ 1] _[M]_ _,_



_M_


_qj_ ( _yi_ ) = 1 (12)

_j_ =1



These constraints ensure that _q_ ( _yi_ ) is a well-formed
probability distribution, suitable for logits-based
fine-tuning. It can be easily demonstrated that _p_ L
satisfies the four constraints outlined above. Details
are in Appendix A.


**3.3** **Logits Dataset Generation**


The logits dataset generation procedure, as detailed
in Alg. 1, takes a standard dataset of input-target



5


Dataset GSM8K MATH College GaoKao Minerva Olympiad Average
Math 2023 en Math Bench


Baseline 46.9 31.6 18.6 26.2 5.5 7.0 22.6
Socratic 35.9 20.3 8.8 17.4 3.7 3.4 14.9
ScienceQA 39.7 21.6 11.7 15.8 4.4 5.9 16.5
StackExchange 37.8 22.3 12.9 19.5 3.3 4.6 16.7
Camel-AI 41.0 22.1 11.3 20.3 5.1 3.6 17.2
MathInstruct 40.9 24.4 12.7 20.0 6.2 4.6 18.1
GSM8K 45.7 29.4 16.9 23.6 5.9 5.8 21.2
MetaMath **54.8** 28.8 21.4 19.7 7.0 7.3 23.2


Table 2: Results of LLaMA3.2-1b-instruct after supervised fine-tuning on various datasets, including Socratic (Yue
et al., 2024), StackExchange (Yue et al., 2024), Camel-AI (Li et al., 2023), MathInstruct (Jiang et al., 2024),
GSM8K (Cobbe et al., 2021), MetaMath (Yu et al., 2023), MetaMath-GSM8K (Yu et al., 2023), and OpenMathInstruct2 (Toshniwal et al., 2024).



model. The loss function is defined as:


           -            _L_ L( _θ_ ) := E( _x,y_ ) _∼_ ( _X,Y_ ) _DKL_  - _p_ L _|p_ _[θ]_ S�( _y|x_ ) _,_
(13)
where _x_ and _y_ represent the input and output sequences. ( _X, Y_ ) is the dataset of input-output pairs.
E[ _·_ ] denotes the expectation over the dataset.


**Fine-tuning.** This Logits-Based Fine-tune leverages a pre-generated logits dataset, as described in
Sec. 3.3, to guide the training of a student model
_p_ _[θ]_ S [.] [Alg.][ 2][ details our logits-based fine-tuning pro-]
cedure. For each batch _B_ from the dataset, the
student’s parameters _θ_ are updated by minimizing
the loss _L_ L (Eq. (13)), which measures the divergence _D_ between _p_ L and _p_ _[θ]_ S [(] _[y][|][x]_ [)][.] [This] [process]
results in a trained student model that incorporates
knowledge from the teacher logits and ground truth
labels.


**4** **Experiment**


In this section, we present a comprehensive evaluation of our logits-based fine-tuning approach. We
first detail our evaluation benchmarks in Sec. 4.1
and training details in Sec. 4.2. Then, we analyze key components through ablation studies
in Sec. 4.3. Finally, we compare on multiple
datasets against baselines in Sec. 4.4.


**4.1** **Benchmark**


We evaluate our ScienceLLaMA on mathematical
benchmark including:


**GSM8K** (Grade School Math 8K, Cobbe et al.


|Col1|Col2|Col3|Col4|Col5|Col6|Col7|
|---|---|---|---|---|---|---|
||||||||
|||<br>Logits-Ba|<br>sed Finetune||||
||||||||
||||||||
||||||||
||||||||
||||||||
||||||||



Figure 3: Ablation of our logits-based finetune comparing with baseline trained on different percentage of
MetaMath-GSM8K (Yu et al., 2023) and evaluated on
GSM8K (Cobbe et al., 2021).


(2021)) is a dataset comprising 8.5K high-quality,
linguistically diverse grade school math word problems.


**MATH** (Hendrycks et al., 2021) consists of 12,500
challenging competition mathematics problems,
each accompanied by a detailed step-by-step solution.


**OlympiadBench** (He et al., 2024) presents an
Olympiad-level bilingual multimodal scientific
benchmark with 8,476 problems from challenging mathematics and physics competitions like the
Chinese college entrance exam.


**CollegeMath** (Tang et al., 2024) is a mathematical
reasoning dataset created using MathScale, containing two million math question-answer pairs.



56


54


52


50


48



0 25 50 75 100
Train Data (%)



6


**Data Source** **Data Description** **Data Count**


Problem Synthesize from Math 832k
OpenMathInstruct Problem Synthesize from GSM8K 138k
(Toshniwal et al., 2024) CoT Aug from Math 15k
CoT Aug from GSM8K 15k


Answer Aug from GSM8K 80k
MetaMath Rephrasing from GSM8K 80k
(Yu et al., 2023) Self-Verification from GSM8K 40k
Forward-Backward Reasoning from GSM8K 40k


Table 3: Source and description of our 1.2M logits dataset, including 240K from MetaMath-GSM8K (Yu et al.,
2023), and 1M from OpenMathInstruct2 (Toshniwal et al., 2024).



**GSM8K**


LLaMA3.2-1b-It 46.9
Supervsied Finetune 54.1


Table 4: Ablation of our logits-based finetune comparing with baseline trained on MetaMath-GSM8K (Yu
et al., 2023).


**SVAMP** (Simple Variations on Arithmetic Math
word Problems, Patel et al. (2021)) introduces a
challenge dataset for English math word problems.


**ASDiv** (Academia Sinica Diverse MWP
Dataset, Miao et al. (2020)) offers a diverse
English math word problem corpus consisting of
2,305 problems,.


**MAWPS** (MAth Word ProblemS, KoncelKedziorski et al. (2016)) is an online repository
providing a unified testbed to evaluate algorithms
on Math Word Problems.


**CarpEN** (Computation-intensive AlgebRa Problems, Zhang et al. (2023a)) constructs a Chinese
dataset focused on computation-intensive algebra
problems.


**TabMWP** (Tabular Math Word Problems, Lu et al.
(2023)) contains 38,431 open-domain grade-level
math problems requiring reasoning over textual and
tabular data.


**4.2** **Training Details**


We train the LLaMA3.2-1B/3B-Instruct as our
model on our constructed 1.2M science logits
dataset using our proposed logits-based fine-tuning
method. The resulting trained models are referred
to as ScienceLLaMA-1B/3B. We set the batch size



to 1 and the learning rate to 2 _×_ 10 _[−]_ [5] . All experiments are conducted on 8 Nvidia A800 GPUs.


**4.3** **Ablation**


Figure 3 presents the GSM8K accuracy of our
logits-based fine-tuning in comparison to supervised fine-tuning, trained on varying percentages
of the MetaMath-GSM8K dataset and evaluated
on the GSM8K benchmark. Both methods demonstrate improved performance as the proportion of
training data increases, but the logits-based finetuning consistently outperforms supervised finetuning across all data scales. Notably, the accuracy
achieved by the logits-based approach with just
25% of the training data exceeds that of the supervised method trained on 50% of the data. Furthermore, with half of the training data, the logits-based
approach achieves better results than the supervised
method trained on the full dataset. On the complete
training set, our logits-based fine-tuning achieves
an accuracy of 56.1%, surpassing the supervised
fine-tuning baseline by 2.0% and outperforming the
original pre-trained model by 9.2%. These findings
underscore the effectiveness of leveraging logits to
guide the learning process.


**4.4** **Performance**


As shown in Tab. 5, we evaluate our proposed
method on various math benchmarks. Our ScienceLLaMA significantly outperforms the SFT
model. Specifically, the ScienceLLaMA-1B model
surpasses the directly SFT-trained LLaMA3.2-1BInstruct on Mawps and TabMWP by 18% and
22.7% in accuracy, respectively. Furthermore, for
the average score across nine benchmarks, our
ScienceLLaMA-1B achieves a 7.28% higher accuracy. These results demonstrate that our method



7


Model GSM8K MATH College Olympiad Svamp ASDiv Mawps Carp TabMWP Avg
Math Bench en


Gemma-2-2b-It 61.9 26.1 20.6 5.3 68.7 77.6 89.7 32.7 42.7 47.26
Phi-3.5-Mini-It 87.2 45.2 35.9 12.3 83.7 85.9 88.1 35.1 55.7 58.79
LLaMA3.2-1b-It 46.9 31.6 18.6 7.0 69.3 70.0 79.3 30.5 33.4 42.96
LLaMA3.2-3b-It 81.3 51.7 34.1 17.2 86.4 89.0 96.7 45.1 70.0 63.50


Table 5: Performance of our ScienceLLaMA comparing with current SOTAs on various benchmarks, including
Socratic (Yue et al., 2024), StackExchange (Yue et al., 2024), Camel-AI (Li et al., 2023), MathInstruct (Jiang
et al., 2024), GSM8K (Cobbe et al., 2021), MetaMath (Yu et al., 2023), MetaMath-GSM8K (Yu et al., 2023), and
OpenMathInstruct2 (Toshniwal et al., 2024).



exhibits strong stability and generalization, significantly outperforming the Supervised-Finetuning
approach.


**5** **Related Works**


**Large Language Models.** Recently, LLMs have
demonstrated remarkable capabilities across a wide
range of tasks (Brown et al., 2020; Thoppilan
et al., 2022; Chowdhery et al., 2022; OpenAI, 2023;
Anil et al., 2023; Yang et al., 2024), including
machine translation (Li et al., 2024a), text summarization (Zheng et al., 2024), dialogue generation (Ouyang et al., 2022), and code generation (Li
et al., 2024b). While their capacity is impressive,
these advanced abilities often emerge only in models with substantial parameter sizes (Kaplan et al.,
2020; Wei et al., 2022), which demand significant
computational resources. As a result, model compression has become essential to facilitate the practical deployment of LLMs and to support further
research in the field.


**Knowledge Distillation.** Knowledge Distillation
(KD; Hinton et al. (2015)), a popular model compression method, focuses on training a smaller student model under the guidance of a larger teacher
model (Rusu et al., 2015; Sanh et al., 2019; Jianping et al., 2021). In NLP, KD has been widely
applied to classification tasks by replicating the
teacher model’s output distribution (Song et al.,
2020; Liang et al., 2021; Zhang et al., 2023b), internal layer representations (Jiao et al., 2020; Sun
et al., 2019), or attention patterns (Wang et al.,
2020, 2021). For text generation tasks, traditional
KD typically minimizes the Kullback-Leibler divergence (KLD) between the teacher’s and student’s
output distributions, using the teacher’s output as



supervision at every time step (Sanh et al., 2019)
or directly training the student on text sequences
generated by the teacher (Kim and Rush, 2016b;
Taori et al., 2023; Chiang et al., 2023; Peng et al.,
2023). Unlike recent studies (Agarwal et al., 2024;
Wen et al., 2023; Ko et al.; Gu et al., 2024), which
focus on alternative distribution discrepancy metrics in KD, our work emphasizes the creation of
a distribution that integrates the robustness of the
ground truth with the teacher’s token-level knowledge priors.


**6** **Conclusion**


In this work, we address the limitations of traditional supervised fine-tuning for developing compact and efficient LLMs by introducing a novel
logits-based fine-tuning framework. Our approach
integrates the strengths of supervised learning and
knowledge distillation, constructing enriched training targets that combine teacher logits with ground
truth labels. This method preserves both correctness and linguistic diversity, enabling the student
model to learn from the teacher’s knowledge while
maintaining task-specific supervision. We constructed a large-scale 1.2M science logits dataset
and trained a series of science-focused models, referred to as ScienceLLaMA. Experimental results
demonstrate that our method achieves significant
improvements over state-of-the-art supervised finetuning approaches, with accuracy gains of 18%
on Mawps and 22.7% on TabMWP. Across nine
widely used mathematical benchmarks, our method
consistently outperforms prior SFT models, achieving an average improvement of 7.28%. These results highlight the robustness of our logits-based
fine-tuning framework.



8


**Limitations**


While our work successfully introduces a distillation framework tailored for large language models (LLMs) using a logits-based instruction tuning
strategy, our experiments were constrained by computational resources, limiting the scale of the evaluated models. We plan to extend this approach to
larger model architectures in future work.


**Broader Impact**


By refining the distillation process to better preserve the teacher model’s reasoning capabilities,
our method may enable more compact and deployable models. This could make LLM-powered applications—such as real-time conversational assistants, on-device AI tools, and resource-constrained
edge computing—more accessible and practical.
However, the broader deployment of efficient, distilled models also introduces risks. If misused, malicious actors might exploit distillation techniques
to create highly optimized models for harmful purposes, such as generating convincing misinformation or automating fraudulent interactions. Responsible development and rigorous evaluation frameworks will be essential to mitigate these risks while
maximizing the societal benefits of our method.


**AI Assistance Disclosure**


In the preparation of this work, the authors used
large language models (LLMs) for writing assistance during manuscript composition. Following
initial drafting, the authors reviewed and edited the
content as needed and take full responsibility for
the final publication.


**References**


Rishabh Agarwal, Nino Vieillard, Yongchao Zhou, Piotr Stanczyk, Sabela Ramos, Matthieu Geist, and
Olivier Bachem. 2024. [On-policy distillation of lan-](https://arxiv.org/abs/2306.13649)
guage models: Learning from self-generated mis[takes.](https://arxiv.org/abs/2306.13649) _Preprint_, arXiv:2306.13649.


AI@Meta. 2024. [Llama 3 model card.](https://github.com/meta-llama/llama3/blob/main/MODEL_CARD.md)


Rohan Anil, Andrew M Dai, Orhan Firat, Melvin Johnson, Dmitry Lepikhin, Alexandre Passos, Siamak
Shakeri, Emanuel Taropa, Paige Bailey, Zhifeng
Chen, et al. 2023. Palm 2 [technical](https://arxiv.org/abs/2305.10403) report. _arXiv_
_preprint arXiv:2305.10403_ .


Tom Brown, Benjamin Mann, Nick Ryder, Melanie
Subbiah, et al. 2020. [Language models are few-shot](https://papers.nips.cc/paper/2020/hash/1457c0d6bfcb4967418bfb8ac142f64a-Abstract.html)
[learners.](https://papers.nips.cc/paper/2020/hash/1457c0d6bfcb4967418bfb8ac142f64a-Abstract.html) In _Proceedings of NeurIPS_ .



Wei-Lin Chiang, Zhuohan Li, Zi Lin, Ying Sheng,
Zhanghao Wu, Hao Zhang, Lianmin Zheng, Siyuan
Zhuang, Yonghao Zhuang, Joseph E. Gonzalez, Ion
Stoica, and Eric P. Xing. 2023. Vicuna: [An](https://lmsys.org/blog/2023-03-30-vicuna/) open[source chatbot impressing gpt-4 with 90%* chatgpt](https://lmsys.org/blog/2023-03-30-vicuna/)
[quality.](https://lmsys.org/blog/2023-03-30-vicuna/)


Aakanksha Chowdhery, Sharan Narang, Jacob Devlin,
Maarten Bosma, Gaurav Mishra, Adam Roberts,
Paul Barham, Hyung Won Chung, Charles Sutton,
Sebastian Gehrmann, et al. 2022. Palm: [Scaling](https://arxiv.org/abs/2204.02311)
language [modeling](https://arxiv.org/abs/2204.02311) with pathways. _arXiv_ _preprint_
_arXiv:2204.02311_ .


Karl Cobbe, Vineet Kosaraju, Mohammad Bavarian,
Mark Chen, Heewoo Jun, Lukasz Kaiser, Matthias
Plappert, Jerry Tworek, Jacob Hilton, Reiichiro
Nakano, Christopher Hesse, and John Schulman.
2021. Training verifiers to solve math word problems. _arXiv preprint arXiv:2110.14168_ .


Yuxian Gu, Li Dong, Furu Wei, and Minlie Huang. 2024.

Minillm: [Knowledge distillation of large language](https://arxiv.org/abs/2306.08543)
[models.](https://arxiv.org/abs/2306.08543) _Preprint_, arXiv:2306.08543.


Chaoqun He, Renjie Luo, Yuzhuo Bai, Shengding Hu,
Zhen Leng Thai, Junhao Shen, Jinyi Hu, Xu Han, Yujie Huang, Yuxiang Zhang, Jie Liu, Lei Qi, Zhiyuan
Liu, and Maosong Sun. 2024. Olympiadbench:
A challenging benchmark for promoting AGI with
olympiad-level bilingual multimodal scientific problems. In _ACL (1)_, pages 3828–3850. Association for
Computational Linguistics.


Dan Hendrycks, Collin Burns, Saurav Kadavath, Akul
Arora, Steven Basart, Eric Tang, Dawn Song, and
Jacob Steinhardt. 2021. Measuring mathematical
problem solving with the MATH dataset. In _NeurIPS_
_Datasets and Benchmarks_ .


Geoffrey Hinton, Oriol Vinyals, and Jeff Dean. 2015.

Distilling the [knowledge](https://arxiv.org/abs/1503.02531) in a neural network.
_Preprint_, arXiv:1503.02531.


Dongfu Jiang, Xuan He, Huaye Zeng, Cong Wei,
Max W.F. Ku, Qian Liu, and Wenhu Chen. 2024.
Mantis: [Interleaved multi-image instruction tuning.](https://openreview.net/forum?id=skLtdUVaJa)
_Transactions on Machine Learning Research_, 2024.


Gou Jianping, Yu Baosheng, Stephen J Maybank, and
Tao Dacheng. 2021. [Knowledge distillation:](https://link.springer.com/article/10.1007/s11263-021-01453-z) A sur[vey.](https://link.springer.com/article/10.1007/s11263-021-01453-z) _IJCV_ .


Xiaoqi Jiao, Yichun Yin, Lifeng Shang, Xin Jiang, Xiao
Chen, Linlin Li, Fang Wang, and Qun Liu. 2020.
Tinybert: [Distilling bert for natural language under-](https://aclanthology.org/2020.findings-emnlp.372/)
[standing.](https://aclanthology.org/2020.findings-emnlp.372/) In _Findings of EMNLP_ .


Jared Kaplan, Sam McCandlish, Tom Henighan, Tom B
Brown, Benjamin Chess, Rewon Child, Scott Gray,
Alec Radford, Jeffrey Wu, and Dario Amodei. 2020.
Scaling laws for [neural](https://arxiv.org/abs/2001.08361) language models. _arXiv_
_preprint arXiv:2001.08361_ .


Yoon Kim and Alexander M. Rush. 2016a.
Sequence-level [knowledge](https://arxiv.org/abs/1606.07947) distillation. _Preprint_,
arXiv:1606.07947.



9


Yoon Kim and Alexander M Rush. 2016b. [Sequence-](https://aclanthology.org/D16-1139.pdf)
level [knowledge](https://aclanthology.org/D16-1139.pdf) distillation. In _Proceedings_ _of_
_EMNLP_ .


Jongwoo Ko, Sungnyun Kim, Tianyi Chen, and SeYoung Yun. Distillm: Towards streamlined distillation for large language models. In _Forty-first Interna-_
_tional Conference on Machine Learning_ .


Rik Koncel-Kedziorski, Subhro Roy, Aida Amini, Nate
Kushman, and Hannaneh Hajishirzi. 2016. Mawps:
A math word problem repository. In _Proceedings of_
_the 2016 conference of the north american chapter of_
_the association for computational linguistics:_ _human_
_language technologies_, pages 1152–1157.


Guohao Li, Hasan Abed Al Kader Hammoud, Hani
Itani, Dmitrii Khizbullin, and Bernard Ghanem. 2023.
Camel: Communicative agents for "mind" exploration of large language model society. In _Thirty-_
_seventh Conference on Neural Information Process-_
_ing Systems_ .


Jingyao Li, Pengguang Chen, Sitong Wu, Chuanyang
Zheng, Hong Xu, and Jiaya Jia. 2024a. [Robocoder:](https://arxiv.org/abs/2406.03757)
Robotic learning from basic skills to general
tasks with large language models. _Preprint_,
arXiv:2406.03757.


Jingyao Li, Pengguang Chen, Bin Xia, Hong Xu, and
Jiaya Jia. 2024b. [Motcoder: Elevating large language](https://arxiv.org/abs/2312.15960)
[models with modular of thought for challenging pro-](https://arxiv.org/abs/2312.15960)
[gramming tasks.](https://arxiv.org/abs/2312.15960) _Preprint_, arXiv:2312.15960.


Kevin J Liang, Weituo Hao, Dinghan Shen, Yufan
Zhou, Weizhu Chen, Changyou Chen, and Lawrence
Carin. 2021. Mix{kd}: [Towards efficient distillation](https://openreview.net/forum?id=UFGEelJkLu5)
[of large-scale language models.](https://openreview.net/forum?id=UFGEelJkLu5) In _Proceedings of_
_ICLR_ .


Pan Lu, Liang Qiu, Kai-Wei Chang, Ying Nian Wu,
Song-Chun Zhu, Tanmay Rajpurohit, Peter Clark,
and Ashwin Kalyan. 2023. Dynamic prompt learning
via policy gradient for semi-structured mathematical
reasoning. In _International Conference on Learning_
_Representations (ICLR)_ .


Shen-yun Miao, Chao-Chun Liang, and Keh-Yih Su.
2020. A diverse corpus for evaluating and developing
english math word problem solvers. In _Proceedings_
_of_ _the_ _58th_ _Annual_ _Meeting_ _of_ _the_ _Association_ _for_
_Computational Linguistics_, pages 975–984.


OpenAI. 2023. GPT-4 [technical](https://arxiv.org/abs/2303.08774) report. _Preprint_,
arXiv:2303.08774.


Long Ouyang, Jeff Wu, Xu Jiang, Diogo Almeida, Carroll L. Wainwright, Pamela Mishkin, Chong Zhang,
Sandhini Agarwal, Katarina Slama, Alex Ray, John
Schulman, Jacob Hilton, Fraser Kelton, Luke Miller,
Maddie Simens, Amanda Askell, Peter Welinder,
Paul Christiano, Jan Leike, and Ryan Lowe. 2022.
[Training language models to follow instructions with](https://arxiv.org/abs/2203.02155)
[human feedback.](https://arxiv.org/abs/2203.02155) _Preprint_, arXiv:2203.02155.



Arkil Patel, Satwik Bhattamishra, and Navin Goyal.
2021. [Are NLP models really able to solve simple](https://doi.org/10.18653/v1/2021.naacl-main.168)
[math word problems?](https://doi.org/10.18653/v1/2021.naacl-main.168) In _Proceedings of the 2021_
_Conference_ _of_ _the_ _North_ _American_ _Chapter_ _of_ _the_
_Association for Computational Linguistics:_ _Human_
_Language Technologies_, pages 2080–2094, Online.
Association for Computational Linguistics.


Baolin Peng, Chunyuan Li, Pengcheng He, Michel Galley, and Jianfeng Gao. 2023. [Instruction tuning with](https://arxiv.org/abs/2304.03277)
[GPT-4.](https://arxiv.org/abs/2304.03277) _arXiv preprint arXiv:2304.03277_ .


Andrei A Rusu, Sergio Gomez Colmenarejo, Caglar
Gulcehre, Guillaume Desjardins, James Kirkpatrick, Razvan Pascanu, Volodymyr Mnih, Koray
Kavukcuoglu, and Raia Hadsell. 2015. [Policy distil-](https://arxiv.org/pdf/1511.06295.pdf)
[lation.](https://arxiv.org/pdf/1511.06295.pdf) _arXiv preprint arXiv:1511.06295_ .


Victor Sanh, Lysandre Debut, Julien Chaumond, and
Thomas Wolf. 2019. [DistilBERT, a distilled version](https://arxiv.org/pdf/1910.01108.pdf)
of bert: smaller, [faster,](https://arxiv.org/pdf/1910.01108.pdf) cheaper and lighter. _arXiv_
_preprint arXiv:1910.01108_ .


Kaitao Song, Hao Sun, Xu Tan, Tao Qin, Jianfeng Lu,
Hongzhi Liu, and Tie-Yan Liu. 2020. [LightPAFF: A](https://arxiv.org/pdf/2004.12817.pdf)
[two-stage distillation framework for pre-training and](https://arxiv.org/pdf/2004.12817.pdf)
[fine-tuning.](https://arxiv.org/pdf/2004.12817.pdf) _arXiv preprint arXiv:2004.12817_ .


Siqi Sun, Yu Cheng, Zhe Gan, and Jingjing Liu. 2019.

[Patient knowledge distillation for BERT model com-](https://aclanthology.org/D19-1441)
[pression.](https://aclanthology.org/D19-1441) In _Proceedings EMNLP_ .


Zhengyang Tang, Xingxing Zhang, Benyou Wang, and
Furu Wei. 2024. Mathscale: Scaling instruction tuning for mathematical reasoning. In _ICML_ . OpenReview.net.


Rohan Taori, Ishaan Gulrajani, Tianyi Zhang, Yann
Dubois, Xuechen Li, Carlos Guestrin, Percy Liang,
and Tatsunori B. Hashimoto. 2023. Stanford Alpaca:
An instruction-following LLaMA model. [https://](https://github.com/tatsu-lab/stanford_alpaca)
[github.com/tatsu-lab/stanford_alpaca.](https://github.com/tatsu-lab/stanford_alpaca)


Romal Thoppilan, Daniel De Freitas, Jamie Hall, Noam
Shazeer, Apoorv Kulshreshtha, Heng-Tze Cheng,
Alicia Jin, Taylor Bos, Leslie Baker, Yu Du, et al.
2022. Lamda: [Language models for dialog applica-](https://arxiv.org/abs/2201.08239)
[tions.](https://arxiv.org/abs/2201.08239) _arXiv preprint arXiv:2201.08239_ .


Shubham Toshniwal, Wei Du, Ivan Moshkov, Branislav
Kisacanin, Alexan Ayrapetyan, and Igor Gitman.
2024. Openmathinstruct-2: [Accelerating ai for math](https://arxiv.org/abs/2410.01560)
[with massive open-source instruction data.](https://arxiv.org/abs/2410.01560) _Preprint_,
arXiv:2410.01560.


Wenhui Wang, Hangbo Bao, Shaohan Huang, Li Dong,
and Furu Wei. 2021. MiniLMv2: [Multi-head](https://aclanthology.org/2021.findings-acl.188) selfattention relation [distillation](https://aclanthology.org/2021.findings-acl.188) for compressing pre[trained transformers.](https://aclanthology.org/2021.findings-acl.188) In _Findings of ACL_ .


Wenhui Wang, Furu Wei, Li Dong, Hangbo Bao, Nan
Yang, and Ming Zhou. 2020. MiniLM: [Deep](https://proceedings.neurips.cc/paper/2020/file/3f5ee243547dee91fbd053c1c4a845aa-Paper.pdf) self[attention distillation for task-agnostic compression of](https://proceedings.neurips.cc/paper/2020/file/3f5ee243547dee91fbd053c1c4a845aa-Paper.pdf)
[pre-trained transformers.](https://proceedings.neurips.cc/paper/2020/file/3f5ee243547dee91fbd053c1c4a845aa-Paper.pdf) In _Proceedings of NeurIPS_ .



10


Jason Wei, Yi Tay, Rishi Bommasani, Colin Raffel,
Barret Zoph, Sebastian Borgeaud, Dani Yogatama,
Maarten Bosma, Denny Zhou, Donald Metzler, et al.
2022. [Emergent abilities of large language models.](https://openreview.net/pdf?id=yzkSU5zdwD)
_Transactions on Machine Learning Research_ .


Yuqiao Wen, Zichao Li, Wenyu Du, and Lili Mou. 2023.

[f-divergence minimization for sequence-level knowl-](https://aclanthology.org/2023.acl-long.605.pdf)
[edge distillation.](https://aclanthology.org/2023.acl-long.605.pdf) In _Proceedings of ACL_ .


Senqiao Yang, Yukang Chen, Zhuotao Tian, Chengyao
Wang, Jingyao Li, Bei Yu, and Jiaya Jia. 2024. Visionzip: Longer is better but not necessary in vision
language models. _arXiv preprint arXiv:2412.04467_ .


Longhui Yu, Weisen Jiang, Han Shi, Jincheng Yu,
Zhengying Liu, Yu Zhang, James T Kwok, Zhenguo Li, Adrian Weller, and Weiyang Liu. 2023.
Metamath: Bootstrap your own mathematical questions for large language models. _arXiv_ _preprint_
_arXiv:2309.12284_ .


Xiang Yue, Tuney Zheng, Ge Zhang, and Wenhu Chen.
2024. Mammoth2: Scaling instructions from the web.
_Advances in Neural Information Processing Systems_ .


Beichen Zhang, Kun Zhou, Xilin Wei, Wayne Xin
Zhao, Jing Sha, Shijin Wang, and Ji-Rong Wen.
2023a. Evaluating and improving tool-augmented
computation-intensive math reasoning. _arXiv_
_preprint arXiv:2306.02408_ .


Rongzhi Zhang, Jiaming Shen, Tianqi Liu, Jialu Liu,
Michael Bendersky, Marc Najork, and Chao Zhang.
2023b. [Do not blindly imitate the teacher:](https://arxiv.org/pdf/2305.05010.pdf) Using per[turbed loss for knowledge distillation.](https://arxiv.org/pdf/2305.05010.pdf) _arXiv preprint_
_arXiv:2305.05010_ .


Chuanyang Zheng, Yihang Gao, Han Shi, Minbin
Huang, Jingyao Li, Jing Xiong, Xiaozhe Ren,
Michael Ng, Xin Jiang, Zhenguo Li, and Yu Li. 2024.
Dape: [Data-adaptive positional encoding for length](https://arxiv.org/abs/2405.14722)
[extrapolation.](https://arxiv.org/abs/2405.14722) _Preprint_, arXiv:2405.14722.


**A** **Verification of Constraints**


We now demonstrate that the proposed distribution
_p_ L( _yi_ ) satisfies the four constraints in Sec. 3.2.


**Constraint** **1.** Since _p_ T( _yi_ ) _∈_ [0 _,_ 1] _[M]_, and
_p_ GT( _yi_ ) is a one-hot vector with a value of 1 at
index _yi_ and 0 elsewhere, the largest value in
_p_ T( _yi_ ) + _p_ GT( _yi_ ) will always be at index _yi_ . The
normalization by the L1 norm preserves this relationship, ensuring _p_ L _yi_ ( _yi_ ) _≥_ _p_ L _j_ ( _yi_ ) for all
_j_ = _yi_ . Thus, Constraint 1 is satisfied.


**Constraint 2.** This constraint pertains to the relative proportions within the Top _K_ elements of
_p_ T( _yi_ ). Since _p_ GT( _yi_ ) only modifies the ground
truth index, and the normalization factor is applied



uniformly across all elements, the relative proportions among the other Top-K elements remain unchanged. Specifically, for _j, k_ _∈_ Top-K( _yi_ ) and
_j, k_ = _yi_, we have:


_p_ L _j_ ( _yi_ ) [+ 0)] _[/][∥][p]_ [T][(] _[y][i]_ [) +] _[ p]_ [GT][(] _[y][i]_ [)] _[∥]_ [1]

[(] _[p]_ [T][(] _[y][i]_ [)] _[j]_
_p_ L _k_ ( _yi_ ) [=] ( _p_ T( _yi_ ) _k_ + 0) _/∥p_ T( _yi_ ) + _p_ GT( _yi_ ) _∥_ 1

= _[p]_ [T][(] _[y][i]_ [)] _[j]_ _._

_p_ T( _yi_ ) _k_

(14)
If _yi_ is within the Top _K_, the ratio involving _yi_ also
holds due to the uniform scaling by the L1 norm.
Therefore, Constraint 2 is satisfied.


**Constraint 3.** For any _j_ _∈/_ _S_, _p_ T( _yi_ ) _j_ = 0 (due
to Top _K_ sparsification). Therefore, _p_ L _j_ ( _yi_ ) = 0.
For any _k_ _∈_ _S_, _p_ L _k_ ( _yi_ ) will be non-negative due
to either a non-zero value in _p_ T( _yi_ ) or the one-hot
vector _p_ GT( _yi_ ). Therefore, _p_ L _j_ ( _yi_ ) _≤_ _p_ L _k_ ( _yi_ ) for
all _j_ _∈/_ _S_ and _k_ _∈_ _S_, satisfying Constraint 3.


**Constraint 4.** By definition, the L1 norm normalization in Equation 7 ensures that the elements of
_p_ L( _yi_ ) sum to 1. Furthermore, since both _p_ T( _yi_ )
and _p_ GT( _yi_ ) have non-negative elements, _p_ L( _yi_ )
will also have non-negative elements. The normalization then ensures that all elements are within the
range [0, 1]. Thus, Constraint 4 is satisfied.


**B** **Dataset Details**


Table 7 provides a comprehensive overview of
the datasets used in our study, detailing their sampled sizes, data sources, and associated references.
The datasets include Socratic and StackExchange
from (Yue et al., 2024), Camel-AI (covering math,
physics, biology, and chemistry) from (Li et al.,
2023), MathInstruct from (Jiang et al., 2024),
GSM8K from (Cobbe et al., 2021), MetaMath and
MetaMath-GSM8K from (Yu et al., 2023), and
OpenMathInstruct2 from (Toshniwal et al., 2024).
For OpenMathInstruct2, which contains 1M samples, we sampled 10K for evaluation.


**C** **Logits-Based Dataset Example**


Table 6 presents a logits-based label visualization
for the sentence: "There are 12 inches in 1 foot,
so Vlad’s height is 6 _×_ 12 + 3 = 75 inches. His
sister’s height is 2 _×_ 12 + 10 = 34 inches."



11


Table 6: Example of the logits-based label of _There are_
_12 inches in 1 foot, so Vlad’s height is 6 * 12 + 3 = 75_
_inches._ _His sister’s height is 2 * 12 + 10 = 34 inches._ .



12


**Dataset** **Sampled Size** **Data Source** **Paper Source**


Socratic 511k [TIGER-Lab/WebInstructSub](https://huggingface.co/datasets/TIGER-Lab/WebInstructSub) Yue et al. (2024)
StackExchange 291k [TIGER-Lab/WebInstructSub](https://huggingface.co/datasets/TIGER-Lab/WebInstructSub) Yue et al. (2024)
ScienceQA 100k [ibivibiv/science_qa](https://huggingface.co/datasets/ibivibiv/science_qa)   
50k [camel-ai/math](https://huggingface.co/datasets/camel-ai/math) Li et al. (2023)
20k [camel-ai/physics](https://huggingface.co/datasets/camel-ai/physics) Li et al. (2023)

Camel-AI

20k [camel-ai/biology](https://huggingface.co/datasets/camel-ai/biology) Li et al. (2023)
20k [camel-ai/chemistry](https://huggingface.co/datasets/camel-ai/chemistry) Li et al. (2023)
MathInstruct 262k [TIGER-Lab/MathInstruct](https://huggingface.co/datasets/TIGER-Lab/MathInstruct) Jiang et al. (2024)
GSM8K 7.5k [openai/gsm8k](https://huggingface.co/datasets/openai/gsm8k) Cobbe et al. (2021)
MetaMath 395k [meta-math/MetaMathQA](https://huggingface.co/datasets/meta-math/MetaMathQA) Yu et al. (2023)
MetaMath-GSM8K 240k [meta-math/MetaMathQA](https://huggingface.co/datasets/meta-math/MetaMathQA) Yu et al. (2023)
OpenMathInstruct2 10k [nvidia/OpenMathInstruct-2](https://huggingface.co/datasets/nvidia/OpenMathInstruct-2) Toshniwal et al. (2024)


Table 7: Size and Source of the datasets, including Socratic (Yue et al., 2024), StackExchange (Yue et al., 2024),
Camel-AI (Li et al., 2023), MathInstruct (Jiang et al., 2024), GSM8K (Cobbe et al., 2021), MetaMath (Yu et al.,
2023), MetaMath-GSM8K (Yu et al., 2023), and OpenMathInstruct2 (Toshniwal et al., 2024).


13


