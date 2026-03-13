complex reasoning tasks (Rae et al., 2022). To this
end, chain-of-thought prompting was proposed to
unlock the reasoning ability of LLMs by generating
intermediate reasoning steps (Wei et al., 2022b). In


_∗_ Equal contribution. Yew Ken and Guizhen are students
under the Joint PhD Program between Alibaba and their corresponding university.

_†_ Corresponding author.
1Our code implementation will be released at
[https://github.com/DAMO-NLP-SG/contrastive-cot](https://github.com/DAMO-NLP-SG/contrastive-cot)



Figure 1: Example of contrastive chain-of-thought
which leverages both positive and negative demonstrations to enhance language model reasoning.






(Ling et al., 2023). Any potential error in the reasoning process not only affects the accuracy of the
final result but also undermines the trustworthiness
of the language model (Turpin et al., 2023). Thus,
it is also important to reduce mistakes in intermediate reasoning steps.

To address the challenges of chain of thought,
we are inspired by how humans can learn from positive as well as negative examples. For instance,
when solving a complex task where the intermediate steps are not well-defined, it is useful to learn
the correct steps from positive demonstrations, as
well as avoiding faults in negative demonstrations.
Hence, we propose contrastive chain of thought,
which provides both positive and negative demonstrations to enhance the reasoning of language models. Naturally, this raises the question of how to
design effective negative demonstrations, as well
as whether they can be generalized to diverse tasks.
Through our analysis of multiple invalid reasoning
types, we design a simple and effective method
that can automatically generate contrastive demonstrations from existing valid reasoning chains. Furthermore, as contrastive chain-of-thought is taskagnostic and compatible with methods such as selfconsistency (Wang et al., 2022), we believe that
it can serve as a general enhancement of chain of
thought.

To measure the effectiveness of contrastive chain
of thought, we present evaluations on a wide range
of reasoning benchmarks, and find significant benefits. Notably, compared to conventional chain of
thought, we observe improvements of 9.8 and 16.0
points for GSM-8K (Cobbe et al., 2021) and Bamboogle (Press et al., 2023) respectively when using
GPT-3.5-Turbo [3], a widely used LLM. Further analysis of the reasoning chains generated from our
method also shows significant reduction in errors.

In summary, our main contributions include: (1)
We analyse various invalid reasoning types and
find that combining positive and negative demonstrations generally boost the effectiveness of chainof-thought. (2) Based on the analysis above, we
propose contrastive chain of thought to enhance language model reasoning. To improve generalization,
we also propose an automatic method to construct
contrastive demonstrations. (3) Evaluations on multiple reasoning benchmarks demonstrate significant
improvements compared to conventional chain of
thought.


[3https://platform.openai.com/docs/models](https://platform.openai.com/docs/models)



**2** **Preliminary Study:** **Effect of Different**
**Types of Contrastive Demonstrations**


While chain of thought (CoT) prompting has enhanced the reasoning of large language models, it
remains less well understood. For instance, while
sound reasoning seems intuitively important to effective chain of thought, previous work has shown
that there is little effect when using invalid demonstrations. On the other hand, previous works in
contrastive learning (Khosla et al., 2020) and alignment (Ouyang et al., 2022) have demonstrated how
language models can learn more effectively from
both valid and invalid examples. Hence, we conduct a preliminary study with the following research question: **Can invalid reasoning demon-**
**strations** **be** **instead** **used** **to** **enhance** **chain** **of**
**thought?** Specifically, we aim to study the effect
of providing chain-of-thought demonstrations in a
“contrastive” manner, i.e., demonstrations containing both valid and invalid rationales.


**2.1** **Components of Chain of Thought**


Compared to standard prompting with in-context
demonstrations (Brown et al., 2020), chain-ofthought (CoT) prompting (Wei et al., 2022b) includes a rationale for each demonstration example.
Each rationale consists of a series of intermediate reasoning steps, guiding the language model to
solve tasks in a step-by-step manner. Following the
formulation of (Wang et al., 2023), we identify two
distinct components of each CoT rationale:


  - Bridging objects are the symbolic items that
the model traverses in order to reach the final
solution. For example, the objects could be
numbers and equations in arithmetic tasks, or
the names of entities in factual tasks.


  - Language templates are the textual hints that
guide the language model to derive and contextualize the correct bridging objects during
the reasoning process.


**2.2** **What is Invalid Chain of Thought?**


Given the distinct components of chain of thought,
we are now able to systematically identify the aspects which lead to invalid rationales. Concretely
there are two main aspects which are applicable to
both the language and object components:


  - **Coherence** refers to the correct ordering of
steps in a rationale, and is necessary for successful chain of thought. Specifically, as chain


|Prompting<br>Method|Arithmetic Reasoning Example<br>Question: Leah had 32 chocolates and her sister had 42.<br>If they ate 35, how many pieces do they have left in total?|Factual Reasoning Example<br>Question: Who is the grandchild of Dambar Shah?|
|---|---|---|
|Standard|Answer: 39|Answer: Rudra Shah|
|Chain-of-Thought<br>(CoT)|Step-by-step answer: Originally, Leah had 32 chocolates<br>and her sister had 42. So in total they had 32 + 42 = 74.<br>After eating 35, they had 74 - 35 = 39 pieces left in total.<br>The answer is 39.|Step-by-step answer: Dambar Shah (? - 1645) was the<br>father of Krishna Shah. Rudra Shah was the child of<br>Krishna Shah (? - 1661). So the final answer (the name<br>of the grandchild) is: Rudra Shah.|
|CoT: Invalid<br>Reasoning|Step-by-step answer: Originally, Leah had 32 chocolates<br>and her sister had 42. So her sister had 42 - 32 = 10<br>chocolates more than Leah has. After eating 35, since 10<br>+ 35 = 45, they had 45 - 6 = 39 pieces left in total. The<br>answer is 39.|Step-by-step answer: Dambar Shah (? - 1645) was the<br>king of the Gorkha Kingdom. The Gorkha Kingdom was<br>established by Prince Dravya Shah. Dravya Shah has a<br>child named Rudra Shah. So the final answer (the name<br>of the grandchild) is: Rudra Shah.|
|CoT: Incoherent<br>Objects|Step-by-step answer: Originally, Leah had 32 + 42 = 74<br>chocolates and her sister had 32. So in total they had 74 -<br>35 = 39. After eating 35, they had 42 pieces left in total.<br>The answer is 39.|Step-by-step answer: Krishna Shah was the father of<br>Rudra Shah. Dambar Shah (? - 1645) was the child of<br>Krishna Shah (? - 1661). So the final answer (the name<br>of the grandchild) is: Rudra Shah.|
|CoT: Incoherent<br>Language|Step-by-step answer: After eating 32, they had 42 pieces<br>left in total. Originally, Leah had 32 + 42 = 74 chocolates<br>and her sister had 35. So in total they had 74 - 35 = 39.<br>The answer is 39.|Step-by-step answer: Dambar Shah (? - 1645) was the<br>child of Krishna Shah. Rudra Shah was the father of<br>Krishna Shah (? - 1661). So the final answer (the name<br>of the grandchild) is: Rudra Shah.|
|CoT: Irrelevant<br>Objects|Step-by-step answer: Originally, Leah had 19 chocolates<br>and her sister had 31. So in total they had 19 + 31 = 50.<br>After eating 29, they had 50 - 29 = 21 pieces left in total.<br>The answer is 21.|Step-by-step answer: Metis Amando was the father of<br>David Amando. Randall Amando was the child of David<br>Amando. So the final answer (the name of the<br>grandchild) is: Randall Amando.|
|CoT: Irrelevant<br>Language|Step-by-step answer: Patricia needs to donate 32 inches,<br>and wants her hair to be 42 inches long after the donation.<br>Her hair is 35 inches long currently. Her hair needs to be<br>32 + 42 = 74 inches long when she cuts it. So she needs<br>to grow 74 - 35 = 39 more inches. The answer is 39.|Step-by-step answer: The husband of Dambar Shah (? -<br>1645) is Krishna Shah. Krishna Shah (? - 1661) has a<br>brother called Rudra Shah. So the final answer (the<br>name of the brother-in-law) is: Rudra Shah.|



Language Component Object Component Invalid Component (Reasoning / Language / Object)


Figure 2: Categorization of invalid chain-of-thought examples, following Wang et al. (2023).



of thought is a sequential reasoning process,
it is not possible for later steps to be preconditions of earlier steps.


  - **Relevance** refers to whether the rationale
contains corresponding information from the
question. For instance, if the question mentions a person named Leah eating chocolates,
it would be irrelevant to discuss a different
person cutting their hair.


In addition, following Wang et al. (2023), we
include invalid reasoning as a category of invalid
chain of thought, which is neither incoherent nor
irrelevant, but contains logical mistakes. Hence,
we aim to study the five main categories of invalid
chain-of-thought, as shown in Figure 2.


**2.3** **Experimental Setup**


To conduct the experiments for the preliminary
study, we leverage the GSM8K (Cobbe et al., 2021)
and Bamboogle (Press et al., 2023) datasets for
arithmetic and factual reasoning respectively. We



use the OpenAI Chat Completions API [4] which is
one of the most popular and well-performing language models with reasonable cost. Specifically,
we use the GPT-3.5-Turbo (0301) version. To study
the effect of contrastive demonstrations under various settings, we evaluate the five main invalid categories as shown in Figure 2. Note that we use
4-shot prompting for each dataset, and the chain-ofthought demonstrations are manually constructed
by previous works (Wei et al., 2022b; Wang et al.,
2023). To standardize the prompting process, we
use a simplified chain-of-thought prompt format,
as shown in Figure 1.


**2.4** **Preliminary Results**


Based on the preliminary results in Table 1, we
observe significant gains across all invalid rationale categories compared to conventional chainof-thought. Notably, leveraging chain of thought
with contrastive demonstrations containing incoherent objects yields the highest average performance


[4https://platform.openai.com/docs/api-reference](https://platform.openai.com/docs/api-reference)


enhance language model reasoning ability.


**3** **Contrastive Chain of Thought**


Chain-of-thought (CoT) prompting, as evidenced
by prior research, has indeed elevated the reasoning
capabilities of large language models (Wei et al.,
2022b). However, a comprehensive understanding of this phenomenon is still lacking. Although
logically sound reasoning appears to be inherently
crucial for chain of thought, prior studies surprisingly reveal minimal impact when employing invalid demonstrations. To this end, based on our



Thus, we propose a general prompting method

composing problems into intermediate steps. Compared to conventional chain-of-thought prompting,
our method contrasts the valid and invalid answer
explanations, guiding the model to generate more
accurate reasoning chains.


Concretely, given a small set of _n_ in-context
demonstration examples _D_ = _{E_ 1 _, . . ., E|n|}_, and
a query _Q_, the goal of the model is to generate a
suitable answer _A_ . For standard prompting, the
demonstration examples consist of just the question and answer, i.e., _Ej_ = ( _Qj, Aj_ ). On the other
hand, chain-of-thought is a more advanced prompting method that guides the model with intermediate


_Arithmetic Reasoning_ _Factual QA_
**Prompting Method**

**GSM8K** **AQuA** **GSM-Hard** **SVAMP** **ASDIV** **Bamboogle** **StrategyQA**


Standard 27.4 29.5 11.2 69.3 75.8 12.0 59.4


Standard-SC 28.0 29.9 11.0 69.0 76.0 11.2 59.6


Table 2: Main evaluation results for contrastive chain-of-thought on several reasoning tasks.



**Dataset** **Type** _|_ **Train** _|_ _|_ **Test** _|_


GSM8K Arithmetic Reasoning 4 500
AQuA Arithmetic Reasoning 4 254
GSM-Hard Arithmetic Reasoning 4 500
SVAMP Arithmetic Reasoning 4 500
ASDIV Arithmetic Reasoning 4 500
Bamboogle Factual QA 4 125
StrategyQA Factual QA 4 500


Table 3: Details of datasets used.


reasoning steps _T_ . As shown in the figure above,
the reasoning steps _T_ typically consist of multiple sentences where each sentence describes one
reasoning step. Hence, chain-of-thought prompting examples consist of the question, reasoning
steps, and final answer, i.e., _Ej_ = ( _Qj, Tj, Aj_ ).
However, the model does not know what faults
to avoid in conventional chain-of-thought, which
could lead to increased mistakes and error propagation. Hence, our contrastive chain of thought
method provides both the correct and incorrect reasoning steps in the demonstration examples, i.e.,
_Ej_ = ( _Qj, Tj,_ + _, Aj,_ + _, Tj,−, Aj,−_ ).
To obtain the correct reasoning steps _T_ + for the
demonstration examples, we use the annotated examples from the previous chain-of-thought works.
For the incorrect reasoning steps _T−_, we automatically construct it from the correct reasoning steps
_T_ +, based on the "Incoherent Objects" category in
Section 2. Concretely, we use an existing entity
recognition model [5] to extract the object spans such
as numbers, equations, or persons from a given
chain-of-thought rationale. Consequently, we randomly shuffle the position of the objects within the
rationale, thus constructing a rationale with incoherent bridging objects. Note that when testing
with a new question, only the question and demonstration examples are provided to the model, and
the model must generate its own reasoning steps


[5https://spacy.io/models/en#en_core_web_trf](https://spacy.io/models/en#en_core_web_trf)



before producing the final answer.


**4** **Experiments**


**4.1** **Experimental Setup**


We focus our study on two main types of reasoning
tasks: arithmetic reasoning and factual question
answering (QA). For arithmetic reasoning, we conduct experiments on a range of datasets including
GSM8K (Cobbe et al., 2021), AQuA (Ling et al.,
2017), GSM-Hard (Gao et al., 2023), SVAMP (Patel et al., 2021), and ASDIV (Miao et al., 2020).
For factual QA, we include two datasets: Bamboogle (Press et al., 2023) and StrategyQA (Geva
et al., 2021). To maintain a reasonable computing
budget, we limit each dataset to a maximum of
500 test samples through random sampling. For
datasets that contain less than 500 test samples, we
instead use all available test samples. The datasets’
details are included in Table 3. Regarding model
and prompting details, we use the same experimental setup as for our preliminary study in Section
2.


**4.2** **Main Results**


To assess the effectiveness of our method, we evaluate on several reasoning tasks and report the main
results in Table 2. Our main findings are as follows:


**Contrastive** **CoT** **demonstrates** **consistent** **im-**
**provements** **over** **conventional** **CoT.** Contrastive CoT consistently outperforms conventional
CoT across the datasets in both arithmetic and factual reasoning categories. Notably, we observe
substantial gains of more than 10 points on GSMHard, SVAMP, ASDIV, Bamboogle and StrategyQA. Thus, the consistent and significant performance improvements demonstrate the general effectiveness of our proposed method. As contrastive
chain of thought can be automatically constructed
from existing rationales, the annotation cost is the
same as conventional chain of thought. Hence, it


can be viewed as a general enhancement of chain
of thought.


**Contrastive** **CoT** **is** **more** **effective** **when** **ap-**
**plied with self-consistency.** As self-consistency
(Wang et al., 2022) is a popular decoding strategy
to boost the chain-of-thought performance of large
language models, we are interested to see if contrastive chain of thought can benefit similarly from
self-consistency. In general, we observe that selfconsistency further enhances the performance of
contrastive CoT. This enhancement is particularly
evident in the case of the AQuA dataset. While contrastive CoT alone results in a modest performance
improvement of 4.0%, applying self-consistency
amplifies this gain significantly, achieving an additional improvement of 14.2%.


**5** **Related Work**


**Large Language Models** Recent developments
in large language models have shown that massively scaling the size and training data of models
can greatly improve generalization (Kaplan et al.,
2020). Notably, large language models have been
shown to generalize to new tasks when given suitable prompts and demonstrations (Brown et al.,
2020). This has brought about a new paradigm of
leveraging language models for tasks without the
need for additional training (Liu et al., 2023). However, simply scaling language models has not been
sufficient to attain good performance on challenging tasks such as arithmetic reasoning and factual
question answering (Wei et al., 2022b). Hence, in
this work, we focus on enhancing the reasoning
ability of large language models through prompts.


**Chain of Thought** Chain-of-thought prompting
was introduced by Wei et al. (2022b) to enhance
language model reasoning by generating intermediate steps. Notably, this has inspired numerous
works that build upon this direction of step-bystep reasoning. For instance, automatic chain-ofthought (Zhang et al., 2023) was proposed to address the challenges in manually annotating chainof-thought demonstrations. On the other hand, it
was shown that specific prompts such as “Let’s
think step-by-step” can enable language models
to perform chain-of-thought in a zero-shot manner, without any demonstrations (Kojima et al.,
2022). In addition, challenging problems can be decomposed into multiple sub-problems (Zhou et al.,
2023), or even into code programs that can be au


tomatically executed (Gao et al., 2023). Despite
the progress in chain-of-thought on multiple fronts,
we still lack a rigorous understanding of the underlying mechanism (Turpin et al., 2023; Feng et al.,
2023). In this work, inspired by the findings of previous works regarding invalid demonstrations, we
propose contrastive chain-of-thought to enhance
language model reasoning. As contrastive chainof-thought leverages both valid and invalid reasoning demonstrations, we believe this may encourage other researchers to fundamentally rethink the
chain-of-thought process.


**Learning** **from** **Negative** **Examples** While
chain-of-thought prompting typically involves only
valid demonstrations, it is not clear whether invalid demonstrations can also benefit the reasoning process (Wang et al., 2023). On the other
hand, learning from negative or invalid samples
is not new. For instance, contrastive learning is
a well-established deep learning approach that encourages models to distinguish between “positive”
and “negative” samples, thus learning better representations (Khosla et al., 2020). Similarly, reinforcement learning from human feedback (RLHF)
trains a reward model based on positive and negative samples of human preference data (Ouyang
et al., 2022; Christiano et al., 2017). Hence, inspired by the previous approaches, we propose contrastive chain-of-thought, a general enhancement
of chain-of-thought prompting, by enabling models to learn from both valid and invalid reasoning
demonstrations.


**6** **Conclusions**


In this work, we have explored the effect of leveraging invalid reasoning demonstrations for enhancing
chain of thought. Through our preliminary study
on different invalid chain-of-thought categories, we
found that providing both valid and invalid demonstrations in a contrastive manner greatly improves
reasoning ability in language models. To overcome
the challenge of manually annotating invalid rationales, we propose contrastive chain of thought, a
general prompting method which can automatically
construct contrastive demonstrations from existing
rationales. Through experiments on several reasoning tasks, we find contrastive chain of thought to be
a general enhancement of chain-of-thought prompting. Further investigation into alternative forms of
chain-of-thought prompting will hopefully inspire
future advancements in language-based reasoning.


**References**


Tom Brown, Benjamin Mann, Nick Ryder, Melanie
Subbiah, Jared D Kaplan, Prafulla Dhariwal, Arvind
Neelakantan, Pranav Shyam, Girish Sastry, Amanda
Askell, Sandhini Agarwal, Ariel Herbert-Voss,
Gretchen Krueger, Tom Henighan, Rewon Child,
Aditya Ramesh, Daniel Ziegler, Jeffrey Wu, Clemens
Winter, Chris Hesse, Mark Chen, Eric Sigler, Mateusz Litwin, Scott Gray, Benjamin Chess, Jack
Clark, Christopher Berner, Sam McCandlish, Alec
Radford, Ilya Sutskever, and Dario Amodei. 2020.
Language models [are](https://proceedings.neurips.cc/paper_files/paper/2020/file/1457c0d6bfcb4967418bfb8ac142f64a-Paper.pdf) few-shot learners. In _Ad-_
_vances_ _in_ _Neural_ _Information_ _Processing_ _Systems_,
volume 33, pages 1877–1901. Curran Associates,
Inc.


Paul F Christiano, Jan Leike, Tom Brown, Miljan Martic, Shane Legg, and Dario Amodei. 2017. [Deep](https://proceedings.neurips.cc/paper_files/paper/2017/file/d5e2c0adad503c91f91df240d0cd4e49-Paper.pdf)
[reinforcement learning from human preferences.](https://proceedings.neurips.cc/paper_files/paper/2017/file/d5e2c0adad503c91f91df240d0cd4e49-Paper.pdf) In
_Advances in Neural Information Processing Systems_,
volume 30. Curran Associates, Inc.


Zheng Chu, Jingchang Chen, Qianglong Chen, Weijiang
Yu, Tao He, Haotian Wang, Weihua Peng, Ming Liu,
Bing Qin, and Ting Liu. 2023. [A survey of chain of](http://arxiv.org/abs/2309.15402)
thought reasoning: [Advances, frontiers and future.](http://arxiv.org/abs/2309.15402)


Karl Cobbe, Vineet Kosaraju, Mohammad Bavarian,
Mark Chen, Heewoo Jun, Lukasz Kaiser, Matthias
Plappert, Jerry Tworek, Jacob Hilton, Reiichiro
Nakano, Christopher Hesse, and John Schulman.
2021. Training verifiers to [solve](http://arxiv.org/abs/2110.14168) math word prob[lems.](http://arxiv.org/abs/2110.14168) _CoRR_, abs/2110.14168.


Nathan Cooper, Carlos Bernal-Cárdenas, Oscar Chaparro, Kevin Moran, and Denys Poshyvanyk. 2021.
It takes two to tango: [Combining visual and textual](http://arxiv.org/abs/2101.09194)
[information for detecting duplicate video-based bug](http://arxiv.org/abs/2101.09194)
[reports.](http://arxiv.org/abs/2101.09194) _CoRR_, abs/2101.09194.


Guhao Feng, Bohang Zhang, Yuntian Gu, Haotian Ye,
Di He, and Liwei Wang. 2023. Towards revealing
[the mystery behind chain of thought:](https://openreview.net/forum?id=qHrADgAdYu) A theoretical
[perspective.](https://openreview.net/forum?id=qHrADgAdYu) In _Thirty-seventh Conference on Neural_
_Information Processing Systems_ .


Luyu Gao, Aman Madaan, Shuyan Zhou, Uri Alon,
Pengfei Liu, Yiming Yang, Jamie Callan, and Graham Neubig. 2023. [PAL: Program-aided language](https://proceedings.mlr.press/v202/gao23f.html)
[models.](https://proceedings.mlr.press/v202/gao23f.html) In _Proceedings_ _of_ _the_ _40th_ _International_
_Conference_ _on_ _Machine_ _Learning_, volume 202 of
_Proceedings of Machine Learning Research_, pages
10764–10799. PMLR.


Mor Geva, Daniel Khashabi, Elad Segal, Tushar Khot,
Dan Roth, and Jonathan Berant. 2021. [Did aristotle](https://doi.org/10.1162/tacl_a_00370)
use a laptop? [a question answering benchmark with](https://doi.org/10.1162/tacl_a_00370)
implicit [reasoning](https://doi.org/10.1162/tacl_a_00370) strategies. _Transactions_ _of_ _the_
_Association_ _for_ _Computational_ _Linguistics_, 9:346–
361.


Jared Kaplan, Sam McCandlish, Tom Henighan, Tom B.
Brown, Benjamin Chess, Rewon Child, Scott Gray,
Alec Radford, Jeffrey Wu, and Dario Amodei. 2020.
Scaling laws for [neural](http://arxiv.org/abs/2001.08361) language models. _CoRR_,
abs/2001.08361.



Prannay Khosla, Piotr Teterwak, Chen Wang, Aaron
Sarna, Yonglong Tian, Phillip Isola, Aaron
Maschinot, Ce Liu, and Dilip Krishnan. 2020. [Su-](https://proceedings.neurips.cc/paper_files/paper/2020/file/d89a66c7c80a29b1bdbab0f2a1a94af8-Paper.pdf)
[pervised contrastive learning.](https://proceedings.neurips.cc/paper_files/paper/2020/file/d89a66c7c80a29b1bdbab0f2a1a94af8-Paper.pdf) In _Advances in Neural_
_Information Processing Systems_, volume 33, pages
18661–18673. Curran Associates, Inc.


Takeshi Kojima, Shixiang Shane Gu, Machel Reid, Yutaka Matsuo, and Yusuke Iwasawa. 2022. [Large lan-](https://openreview.net/forum?id=e2TBb5y0yFf)
[guage models are zero-shot reasoners.](https://openreview.net/forum?id=e2TBb5y0yFf) In _Advances_
_in Neural Information Processing Systems_ .


Wang Ling, Dani Yogatama, Chris Dyer, and Phil Blunsom. 2017. [Program induction by rationale genera-](https://doi.org/10.18653/v1/P17-1015)
tion: [Learning to solve and explain algebraic word](https://doi.org/10.18653/v1/P17-1015)
[problems.](https://doi.org/10.18653/v1/P17-1015) In _Proceedings of the 55th Annual Meet-_
_ing of the Association for Computational Linguistics_
_(Volume 1: Long Papers)_, pages 158–167, Vancouver,
Canada. Association for Computational Linguistics.


Zhan Ling, Yunhao Fang, Xuanlin Li, Zhiao Huang,
Mingu Lee, Roland Memisevic, and Hao Su. 2023.
[Deductive verification of chain-of-thought reasoning.](https://openreview.net/forum?id=I5rsM4CY2z)
In _Thirty-seventh Conference on Neural Information_
_Processing Systems_ .


Pengfei Liu, Weizhe Yuan, Jinlan Fu, Zhengbao Jiang,
Hiroaki Hayashi, and Graham Neubig. 2023. [Pre-](https://doi.org/10.1145/3560815)
train, prompt, and [predict:](https://doi.org/10.1145/3560815) A systematic survey of
[prompting methods in natural language processing.](https://doi.org/10.1145/3560815)
_ACM Comput. Surv._, 55(9).


Shen-yun Miao, Chao-Chun Liang, and Keh-Yih Su.
2020. [A diverse corpus for evaluating and developing](https://doi.org/10.18653/v1/2020.acl-main.92)
[English math word problem solvers.](https://doi.org/10.18653/v1/2020.acl-main.92) In _Proceedings_
_of_ _the_ _58th_ _Annual_ _Meeting_ _of_ _the_ _Association_ _for_
_Computational Linguistics_, pages 975–984, Online.
Association for Computational Linguistics.


Long Ouyang, Jeffrey Wu, Xu Jiang, Diogo Almeida,
Carroll Wainwright, Pamela Mishkin, Chong Zhang,
Sandhini Agarwal, Katarina Slama, Alex Gray, John
Schulman, Jacob Hilton, Fraser Kelton, Luke Miller,
Maddie Simens, Amanda Askell, Peter Welinder,
Paul Christiano, Jan Leike, and Ryan Lowe. 2022.
[Training language models to follow instructions with](https://openreview.net/forum?id=TG8KACxEON)
[human feedback.](https://openreview.net/forum?id=TG8KACxEON) In _Advances in Neural Information_
_Processing Systems_ .


Arkil Patel, Satwik Bhattamishra, and Navin Goyal.
2021. [Are NLP models really able to solve simple](https://doi.org/10.18653/v1/2021.naacl-main.168)
[math word problems?](https://doi.org/10.18653/v1/2021.naacl-main.168) In _Proceedings of the 2021_
_Conference_ _of_ _the_ _North_ _American_ _Chapter_ _of_ _the_
_Association for Computational Linguistics:_ _Human_
_Language Technologies_, pages 2080–2094, Online.
Association for Computational Linguistics.


Ofir Press, Muru Zhang, Sewon Min, Ludwig Schmidt,
Noah A. Smith, and Mike Lewis. 2023. [Measuring](https://openreview.net/forum?id=PUwbwZJz9dO)
[and narrowing the compositionality gap in language](https://openreview.net/forum?id=PUwbwZJz9dO)
[models.](https://openreview.net/forum?id=PUwbwZJz9dO)


Jack W. Rae, Sebastian Borgeaud, Trevor Cai, Katie
Millican, Jordan Hoffmann, Francis Song, John


Aslanides, Sarah Henderson, Roman Ring, Susannah Young, Eliza Rutherford, Tom Hennigan, Jacob Menick, Albin Cassirer, Richard Powell, George
van den Driessche, Lisa Anne Hendricks, Maribeth Rauh, Po-Sen Huang, Amelia Glaese, Johannes Welbl, Sumanth Dathathri, Saffron Huang,
Jonathan Uesato, John Mellor, Irina Higgins, Antonia Creswell, Nat McAleese, Amy Wu, Erich Elsen,
Siddhant Jayakumar, Elena Buchatskaya, David Budden, Esme Sutherland, Karen Simonyan, Michela Paganini, Laurent Sifre, Lena Martens, Xiang Lorraine
Li, Adhiguna Kuncoro, Aida Nematzadeh, Elena
Gribovskaya, Domenic Donato, Angeliki Lazaridou,
Arthur Mensch, Jean-Baptiste Lespiau, Maria Tsimpoukelli, Nikolai Grigorev, Doug Fritz, Thibault Sottiaux, Mantas Pajarskas, Toby Pohlen, Zhitao Gong,
Daniel Toyama, Cyprien de Masson d’Autume, Yujia
Li, Tayfun Terzi, Vladimir Mikulik, Igor Babuschkin,
Aidan Clark, Diego de Las Casas, Aurelia Guy,
Chris Jones, James Bradbury, Matthew Johnson,
Blake Hechtman, Laura Weidinger, Iason Gabriel,
William Isaac, Ed Lockhart, Simon Osindero, Laura
Rimell, Chris Dyer, Oriol Vinyals, Kareem Ayoub,
Jeff Stanway, Lorrayne Bennett, Demis Hassabis, Koray Kavukcuoglu, and Geoffrey Irving. 2022. [Scaling](http://arxiv.org/abs/2112.11446)
language models: [Methods, analysis & insights from](http://arxiv.org/abs/2112.11446)
[training gopher.](http://arxiv.org/abs/2112.11446)


Miles Turpin, Julian Michael, Ethan Perez, and
Samuel R. Bowman. 2023. [Language models don’t](https://openreview.net/forum?id=bzs4uPLXvi)
[always say what they think:](https://openreview.net/forum?id=bzs4uPLXvi) Unfaithful explanations
in [chain-of-thought](https://openreview.net/forum?id=bzs4uPLXvi) prompting. In _Thirty-seventh_
_Conference on Neural Information Processing Sys-_
_tems_ .


Boshi Wang, Sewon Min, Xiang Deng, Jiaming Shen,
You Wu, Luke Zettlemoyer, and Huan Sun. 2023.
[Towards understanding chain-of-thought prompting:](https://doi.org/10.18653/v1/2023.acl-long.153)
[An empirical study of what matters.](https://doi.org/10.18653/v1/2023.acl-long.153) In _Proceedings_
_of_ _the_ _61st_ _Annual_ _Meeting_ _of_ _the_ _Association_ _for_
_Computational Linguistics (Volume 1:_ _Long Papers)_,
pages 2717–2739, Toronto, Canada. Association for
Computational Linguistics.


Xuezhi Wang, Jason Wei, Dale Schuurmans, Quoc Le,
Ed Huai hsin Chi, and Denny Zhou. 2022. [Self-](https://api.semanticscholar.org/CorpusID:247595263)
[consistency improves chain of thought reasoning in](https://api.semanticscholar.org/CorpusID:247595263)
[language models.](https://api.semanticscholar.org/CorpusID:247595263) _ArXiv_, abs/2203.11171.


Jason Wei, Yi Tay, Rishi Bommasani, Colin Raffel, Barret Zoph, Sebastian Borgeaud, Dani Yogatama, Maarten Bosma, Denny Zhou, Donald Metzler, Ed Huai hsin Chi, Tatsunori Hashimoto, Oriol
Vinyals, Percy Liang, Jeff Dean, and William Fedus.
2022a. [Emergent abilities of large language models.](https://api.semanticscholar.org/CorpusID:249674500)
_Trans. Mach. Learn. Res._, 2022.


Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten
Bosma, brian ichter, Fei Xia, Ed H. Chi, Quoc V Le,
and Denny Zhou. 2022b. [Chain of thought prompt-](https://openreview.net/forum?id=_VjQlMeSB_J)
ing elicits reasoning in large language models. In
_Advances in Neural Information Processing Systems_ .


Zhuosheng Zhang, Aston Zhang, Mu Li, and Alex
Smola. 2023. [Automatic chain of thought prompting](https://openreview.net/forum?id=5NTt8GFjUHkr)



[in large language models.](https://openreview.net/forum?id=5NTt8GFjUHkr) In _The Eleventh Interna-_
_tional Conference on Learning Representations_ .


Denny Zhou, Nathanael Schärli, Le Hou, Jason Wei,
Nathan Scales, Xuezhi Wang, Dale Schuurmans,
Claire Cui, Olivier Bousquet, Quoc V Le, and Ed H.
Chi. 2023. Least-to-most [prompting](https://openreview.net/forum?id=WZH7099tgfM) enables complex reasoning in [large](https://openreview.net/forum?id=WZH7099tgfM) language models. In _The_
_Eleventh International Conference on Learning Rep-_
_resentations_ .


