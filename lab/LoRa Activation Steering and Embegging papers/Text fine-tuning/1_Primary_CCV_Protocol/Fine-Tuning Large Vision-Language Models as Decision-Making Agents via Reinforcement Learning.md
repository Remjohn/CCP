### **Fine-Tuning Large Vision-Language Models as** **Decision-Making Agents via Reinforcement Learning**

**Yuexiang Zhai** [1] _[∗]_ **Hao Bai** [2] _[†]_ **Zipeng Lin** [1] _[†]_ **Jiayi Pan** [1] _[†]_ **Shengbang Tong** [3] _[†]_ **Yifei Zhou** [1] _[†]_


**Alane Suhr** [1] **Saining Xie** [3] **Yann LeCun** [3] **Yi Ma** [1] **Sergey Levine** [1]


1UC Berkeley 2UIUC 3NYU



















Figure 1: **Method overview.** We propose a framework for training large Vision-Language Models (VLM) with
Reinforcement Learning (RL). At each time step, the VLM takes the current observation and a predesigned
prompt as input and outputs an utterance containing a chain of thought reasoning and a text action. The text
action is parsed into the environment for generating task rewards. Finally, we apply RL with the task reward to
fine-tune the entire VLM.


**Abstract**


Large vision-language models (VLMs) fine-tuned on specialized visual instructionfollowing data have exhibited impressive language reasoning capabilities across
various scenarios. However, this fine-tuning paradigm may not be able to efficiently learn optimal decision-making agents in multi-step goal-directed tasks from
interactive environments. To address this challenge, we propose an algorithmic
framework that fine-tunes VLMs with reinforcement learning (RL). Specifically,
our framework provides a task description and then prompts the VLM to generate chain-of-thought (CoT) reasoning, enabling the VLM to efficiently explore
intermediate reasoning steps that lead to the final text-based action. Next, the
open-ended text output is parsed into an executable action to interact with the environment to obtain goal-directed task rewards. Finally, our framework uses these
task rewards to fine-tune the entire VLM with RL. Empirically, we demonstrate
that our proposed framework enhances the decision-making capabilities of VLM


_∗_ Project Lead, email: simonzhai@berkeley.edu. Project page: `[https://rl4vlm.github.io/](https://rl4vlm.github.io/)`

_†_ Equal contribution, listed in alphabetical order, see Appendix A for list of contributions.


38th Conference on Neural Information Processing Systems (NeurIPS 2024).


agents across various tasks, enabling 7b models to outperform commercial models
such as GPT4-V or Gemini. Furthermore, we find that CoT reasoning is a crucial
component for performance improvement, as removing the CoT reasoning results
in a significant decrease in the overall performance of our method.


**1** **Introduction**


Large vision-language models (VLMs) [7, 44, 18] demonstrate remarkable capabilities as generalpurpose agents in solving various tasks through language reasoning. In particular, fine-tuning VLMs
with specialized visual instruction following data appears to be a key technique for improving the
capabilities of VLMs [34, 84, 33, 30]. However, visual instruction tuning may not be optimal for
training decision-making agents in multi-step interactive environments requiring visual recognition
and language understanding, as visual instruction tuning mainly performs supervised learning on precollected datasets without interacting with the environments [22]. Consequently, if the pre-collected
datasets lack sufficient diversity to cover a wide range of decision-making scenarios, visual instruction
tuning may fail to improve the VLM agent’s decision-making capabilities.


To unleash the learning capabilities of VLM agents in multi-step goal-directed decision-making
environments, reinforcement learning (RL), a method that has proven effective in training multi-step
interactive agents [41, 59, 6, 69], naturally offers a paradigm that supports this purpose. However,
while RL has been widely adopted for training purely text-based tasks for large language models
(LLMs) [60, 50, 1, 83], end-to-end VLM fine-tuning with RL for goal-directed multi-step tasks has
not yet been studied, to the best of our knowledge.


Our main contribution in this paper is an algorithmic framework that directly fine-tunes VLMs
with RL for multi-step goal-directed decision-making tasks requiring vision-language understanding.
In our framework, the VLM first receives a task description prompt, which guides it to generate
task-specific chain-of-thought (CoT) reasoning [75, 73] (blue parts in Figure 1), followed by a
text-based action (red parts in Figure 1). The CoT reasoning is designed for efficient explorations
by prompting the VLMs to generate intermediate reasoning that leads to the final text-based action.
Our framework then parses the text-based actions into executable actions for the environment, which
generates potentially goal-directed rewards and the next state for RL training.


To evaluate the effectiveness of our method in enhancing a VLM’s decision-making capabilities, we
adopt a 7b model [35] as the backbone VLM and apply our method to five decision-making tasks.
These tasks come from two domains: an original domain, which evaluates the VLM’s decision-making
capabilities requiring fine-grained visual recognition and language reasoning, and an embodied AI
domain [58] focusing on testing tasks demanding visual semantic reasoning capabilities. Empirical
results show that our method enhances the decision-making capabilities of VLMs in both domains,
enabling 7b models to surpass the performance of commercial models such as GPT4-V [44] and
Gemini [18]. Moreover, our experiments reveal that CoT reasoning is crucial for performance
improvement in our RL training. Specifically, we test our method on the same tasks _without_ the CoT
reasoning and observe a significant drop in overall performance in both domains.


**2** **Related Work**


**Training LLMs or VLMs with RL.** RL has been widely adopted for training LLMs and VLMs

[85, 61, 70, 45, 10, 50, 9, 43, 18, 62, 60, 1, 20, 83]. Some studies [85, 61, 45, 10, 43, 18, 62] focus
on applying RL from human feedback (RLHF), which involves learning reward models from human
feedback before deploying RL. Other research [50, 9, 60, 1, 20, 83] focuses on deploying RL with
task-specific reward functions without using human preference data. Our paper is similar to the
latter [50, 9, 60, 1, 20, 83] which applies RL to train LLMs on customized reward functions from
different environments. There are two major differences between our paper and prior works [50, 60, 1,
20, 83]. Firstly, our method incorporates visual inputs, broadening its applicability to a wider range of
tasks that require vision-language understanding or multimodal reasoning [29, 38]. Secondly, while
previous works do not explore how CoT reasoning affects RL training on large models in general, we
identify CoT reasoning as a crucial component for enhancing RL training. We empirically observe
that incorporating CoT reasoning significantly improves the overall performance of RL training on
_all_ tested domains.


2


**Adopting LLMs and VLMs as decision-making agents.** Many prior works have studied various
methods of using frozen LLMs and VLMs for decision-making. One line of work studies the
prompting techniques [75, 14, 79, 78, 74, 31, 76, 47, 71, 48, 24] for enhancing the decision-making
capabilities of large foundation models, see Dong et al. [14], Yang et al. [77] for a detailed survey for
other prompting based methods. Our work differs from all prompting-based methods since we directly
use RL to fine-tune the entire VLM as decision-making agents. Other studies [42, 64, 4, 52, 11]
integrate frozen VLMs ot LLMs into their training pipeline for processing task descriptions or
feature extraction, without using text-based actions. focuses on integrating different components
from VLMs for downstream RL training. For example, some studies use the VLMs or CLIP vision
encoder [46, 42, 64] as reward models for training, which differs from our method since we adopt
rewards from the environments. Other studies [42, 64, 11] integrate frozen VLMs/LLMs into their
training pipeline for processing task descriptions [42, 64, 46] or feature extraction [11], without using
text-based actions. Our paper differs from these works [42, 64, 11] in two major aspects. From a
technical perspective, we focus on a more challenging paradigm by directly fine-tuning the entire
VLM with RL, whereas previous methods [42, 64, 11] only train additional MLP or transformer
layers to connect the frozen LLM/VLM with the action space. More importantly, our method directly
interacts with the environments using _open-ended_ _text_, enabling it to utilize the CoT reasoning
capability of VLMs for more efficient explorations for decision-making.


**Evaluating VLMs as decision-making agents.** Previous studies have thoroughly examined the
fundamental evaluations of VLMs in non-interactive tasks [3, 37, 80, 32, 65, 81, 16]. Our focus,
however, is on evaluating a VLM’s decision-making capabilities in interactive environments that
require both visual recognition and language reasoning. Representative interactive environments
include purely text-based environments [13, 28, 72] or embodied AI environments [40, 58, 56, 15].
We adopt the ALFWorld [58] embodied environment for evaluating our method’s ability to improve
VLM’s visual semantic reasoning capabilities. In addition to the ALFWorld embodied AI environment,
we also design an original “gym-like” [8] environment to test VLM’s decision-making capabilities in
tasks that require fine-grained visual recognition and language reasoning.


**CoT prompting.** Recent studies in prompting for LLMs have demonstrated the crucial role of CoT
in enhancing complex reasoning capabilities [75, 26, 17, 73, 82, 79]. Wei et al. [75] show that CoT
reasoning can significantly boost LLMs’ performance across different reasoning tasks by showing
that adding simple exemplar-based prompts, leading to better performance on benchmarks such as
the GSM8K [12]. A follow-up study [73] proposes a novel self-consistency decoding strategy that
explores multiple reasoning paths, demonstrating substantial gains in arithmetic and commonsense
reasoning tasks. Other works [26, 82, 17] have shown that adding prompts to break complex tasks
into subtasks and solve them step-by-step significantly improves LLM’s reasoning capability. Our
work differs from these CoT prompting studies as we aim to provide an algorithmic framework that
can train VLMs with RL, where the CoT prompting appears as a key component of the framework.
In contrast, prior works focus on improving the reasoning capabilities of LLMs with increasingly
sophisticated prompting of frozen models.


**3** **Preliminaries**


**Standard RL terminologies.** We follow the standard notations from classic RL literature [63, 2].
Specifically, we use _M_ = _{S, A, P, r, γ}_ to denote an MDP, where _S_ denotes the state space, _A_
denotes the action space, _P_ denotes the transition dynamics, _r_ : _S_ _× A_ _→_ R denotes the reward
function and _γ_ _∈_ [0 _,_ 1] denotes the discount factor. Our goal is to learn a policy _π_ : _S_ _→A_ that

maximizes the overall discounted return max _π∈_ Π E _π_ �� _Tt_ =0 _[γ][t][r]_ [(] _[s][t][, a][t]_ [)] �, where _T_ is the maximum

number of steps per episode. Without loss of generality, we use _π_ ( _a|s_ ) _∈_ [0 _,_ 1] to denote probability
of _π_ choosing _a_ at _s_ .


**Adapting the RL formalism to VLMs.** We use _V_ to denote the discrete and finite vocabulary
(token) space, and we use _V_ _[m]_ _, V_ _[n]_ to represent the input and output text space, where _m_ and _n_
represent the maximum token length of the input and output sequence. We adapt the RL formalism
to VLMs by treating the combination of the _vision and language inputs_ to VLMs as the state space:
_S_ = _O × V_ _[m]_, where _O_ is the space of all RGB images. We view each utterance [1, 83] of the


3


language outputs from VLMs as the action space _V_ _[n]_ . Therefore, the input and output of a VLM
policy with parameter _θ_ can be written as _πθ_ : _O × V_ _[m]_ _→V_ _[n]_ . For example, in the `Blackjack` task
shown in Figure 1, each state _s_ consists of an RGB image _o_ with the cards of the dealer and the player,
as well as an input prompt _**v**_ [in] with maximum token length _m_, and the text output _**v**_ [out] = _πθ_ ( _o,_ _**v**_ [in] )
(with a maximum token _n_ ) will later be parsed as an action to interact with the environment. Similar
to the standard RL setting, we use _πθ_ ( _**v**_ [out] _|o,_ _**v**_ [in] ) _∈_ [0 _,_ 1] to denote the probability of a VLM policy
_πθ_ outputting _**v**_ [out] with input image _o_ and prompt _**v**_ [in] .


**4** **Training VLMs with RL**


Compared to classic MLP-based policy networks [53–55, 19], a natural advantage of VLM policies is
that they can leverage CoT reasoning for efficient exploration, by performing intermediate reasoning
steps that lead to the final decision. However, training a VLM policy _πθ_ with RL presents additional
challenges. First, the VLM policy _πθ_ ( _o,_ _**v**_ [in] ) directly generates open-ended text rather than vectorized
actions in classic policy gradient-based RL methods [53–55, 19], complicating direct interaction with
the environment. Even with a parsing mechanism _f_ : _V_ _[n]_ _→A_ that maps open-ended text _**v**_ [out] to
a _legal_ action _a_ for interaction with the environment, it remains unclear how to estimate the action
probability _πθ_ ( _a|o,_ _**v**_ [in] ) from the text generation process.


Figure 2 presents an overview of our framework, leveraging the CoT reasoning and addressing the two
aforementioned challenges. We design a task-specific prompt _**v**_ [in] that requires the VLM to generate a
formatted output _**v**_ [out], including the CoT reasoning. Next, we adopt a post-processing function _f_
to parse open-ended text into a _legal_ action _at_ that can directly interact with the environment. To
compute _πθ_ ( _a|o,_ _**v**_ [in] ), we develop a method to estimate its value based on the probability of each
output token in _**v**_ [out] .



















Figure 2: **A diagram of the proposed RL fine-tuning framework.** At time step _t_, the state _st_ contains an
input prompt _**v**_ [in] _t_ [and a visual observation] _[ o]_ _t_ [.] [The VLM takes] _[ s]_ _t_ [= [] _[o]_ _t_ _[,]_ _**[ v]**_ [in] _t_ []][ as input and outputs open-ended text]
_**v**_ [out] _t_ containing the CoT reasoning, keywords `"action"` : `"` _at_ `"`, and the log-likelihood of _**v**_ [out] _t_ [.] [We first apply a]
post-processing function _f_ on _**v**_ [out] _t_ [, to obtain a] _[ legal]_ [ action] _[ a]_ _t_ [which can interact with the environment.] [Then,]
we input _at_ to the environment for obtaining reward _r_ ( _st, at_ ) and the next observation _ot_ +1. Afterward, we
devise a method to compute a numerical value of _πθ_ ( _at|ot,_ _**v**_ [in] _t_ [)][.] [Finally, we use] _[ r]_ [(] _[s]_ _t_ _[, a]_ _t_ [)][ and] _[ π]_ _θ_ [(] _[a]_ _t_ _[|][o]_ _t_ _[,]_ _**[ v]**_ [in] _t_ [)][ for]
the RL training.


The remaining Section is structured as follows. First, we describe the format of our input prompt _**v**_ [in] _t_
and the desired output _**v**_ [out] _t_ (Section 4.1). Next, we present the post-processing function _f_ (Section 4.2).
Then, we introduce a method to compute a numerical value of _πθ_ ( _at|ot,_ _**v**_ [in] _t_ [)][ (Section][ 4.3][).] [Finally,]
we conclude our framework in Algorithm 1 (Section 4.4).


**4.1** **Prompt Design for Domain-Specific Outputs**


For each task _M_, our input prompt _**v**_ [in] _t_ [contains a description of the task, the legal action space of the]
current observation, and the desired output format (including the CoT reasoning). Our desired output
_**v**_ [out] _t_ [,] [contains] [a] [CoT] [reasoning] [followed] [by] [the] [keywords] `["][action]["]` [:] `["]` _[a][t]_ `["]` [for] [post-processing.]
Figure 3 provides an example of our input prompt _**v**_ [in] _t_ [and] [the] [desired] [formatted] [output] _**[v]**_ [out] _t_ [.] [In]
particular, we define a function _h_ which constructs _**v**_ [in] _t_ [from the current observation] _[ o][t]_ [:] _**[ v]**_ _t_ [in] [=] _[ h]_ [(] _[o][t]_ [)][, to]
accommodate for tasks that may contain observation-dependent information. [3] We provide additional
examples of _**v**_ [in] and _**v**_ [out] in Appendix B.


3E.g., the `alfworld` environment (to be introduced in Section 5.2) contains an observation-dependent
_admissible action_ space.


4


**CoT prompt** _**v**_ **[in]** _t_ **[for task]** _[ M]_
You are trying to solve a task _M_ . {Description of the task}. You are observing the current status of
the task. The action space of _M_ is {text version of all legal actions _a ∈A_ }. Your response should be
a valid json file in the following format:
{

"thoughts": "{first describe the current status of the task, then think carefully about which action to
choose}",
"action": {Choose an action " _a ∈A_ "}
}


**Formatted text output** _**v**_ [out] _t_
{

"thoughts": "I am solving task _T_, given the current status of the task, I should choose _at_ ",
"action": " _at_ "
}


Figure 3: **A template of our input prompt and output text.** The blue part represents the CoT reasoning and
the red part is the text-based action. Note that the CoT reasoning may contain **other task-specific descriptions**,
see Appendix B for more details.


**4.2** **Post-Processing Open-Ended Text for Legal Actions**


Our post-processing mechanism involves both _**v**_ [in] _t_ [and] _[ f]_ [.] [In the input prompt] _**[ v]**_ [in] _t_ [, we directly ask the]
VLM to output a text-based action in the format of `"action"` : `"` _at_ `"` (see Figure 1 and Figure 2 for
examples). After obtaining _**v**_ [out] _t_ [, our post-processing function] _[ f]_ [directly searches for the text-based]
keywords `"action"` : `"` _at_ `"` from _**v**_ [out] _t_ [, and maps it to a legal action] _[ a][t]_ [, either in symbolic or in text]
depending on the task of interest. For the case shown in Figure 1, _f_ will map _**v**_ [out] _t_ to the symbolic
operator that represents the action `"stand"` in the `Blackjack` task (to be introduced in Section 5.1),
as the `Blackjack` task takes symbolic actions as input. For the `alfworld` [58] environment shown
in Figure 2, _f_ will map _**v**_ [out] _t_ to the text `"look"`, because the `alfworld` environment takes text-based
actions as inputs.

However, VLMs are not always guaranteed to generate a _**v**_ [out] _t_ that contains the keywords `"action"` :
`"` _at_ `"`, even when we explicitly request a formatted output from _**v**_ [in] _t_ [.] [To continue the RL training when]
_**v**_ [out] _t_ does not contain any legal action, we perform _random exploration_ by selecting a legal action
_at_ _∈A_ uniformly at random. Mathematically, _f_ is defined as follows:


         - _a,_ if `"action"` : `"` _a_ `"` _∈_ _**v**_ [out] _,_
_f_ ( _**v**_ [out] ) = (4.1)
`Unif` ( _A_ ) _,_ otherwise.


**4.3** **Estimating Action Probabilities of VLM Policies**


To estimate the action probability log _πθ_ ( _at|ot,_ _**v**_ [in] _t_ [)] [(or] [equivalently] [log] _[ π][θ]_ [(] _[a][t][|][o][t][,]_ _**[ v]**_ [in] _t_ [)][)] [for] [pol-]
icy gradient-based methods [55], a naïve calculation is directly using log _πθ_ ( _**v**_ [out] _t_ _[|][o][t][,]_ _**[ v]**_ _t_ [in][)] [as]
log _πθ_ ( _at|ot,_ _**v**_ [in] _t_ [)][, by summing the log-likelihood of all tokens in] _**[ v]**_ _t_ [out][.] [This is because]



_t_ _[,]_ _**[ v]**_ _t_ [out][)]
log _πθ_ ( _**v**_ [out] _t_ _[|][o]_ _t_ _[,]_ _**[ v]**_ [in] _t_ [) = log] _[P]_ [(] _[o][t][,]_ _**[ v]**_ [in]
_P_ ( _ot,_ _**v**_ [in] _t_ [)]







(4.2)

_._








_P_ ( _ot,_ _**v**_ [in] _t_ _[,]_ _**[ v]**_ [: _i_ ] [)]
_P_ ( _ot,_ _**v**_ [in] _t_ _[,]_ _**[ v]**_ [[:] _[i][−]_ [1]][)]



= log




_P_ ( _ot,_ _**v**_ [in] _t_ _[,]_ _**[ v]**_ [: _n_ ] [)] _[P]_ [(] _[o][t][,]_ _**[ v]**_ _t_ [in] _[,]_ _**[ v]**_ [:2] [)] _P_ ( _ot,_ _**v**_ [in] _t_ _[,]_ _**[ v]**_ [:1] [)]
_P_ ( _ot,_ _**v**_ [in] _t_ _[,]_ _**[ v]**_ [[:] _[n][−]_ [1]][)] _[. . .]_ _P_ ( _ot,_ _**v**_ [in] _t_ _[,]_ _**[ v]**_ [[:1]][)] _P_ ( _ot,_ _**v**_ [in] _t_ [)]



=



_n_

- log


_i_ =1



In the equation above, we use _**v**_ to denote the output token _**v**_ [out] _t_ for simplicity, and we use _**v**_ [: _i_ ]
to denote the first _i_ tokens in _**v**_ [out] _t_ [,] [and] [we] [slightly] [abuse] [our] [notion] [by] [using] _[P]_ [(] _[o][t][,]_ _**[ v]**_ [in] _t_ _[,]_ _**[ v]**_ [:0] [)] [to]
denote _P_ ( _ot,_ _**v**_ [in] _t_ [)] [in] [the] [log] [summation.] [Hence,] [a] [natural] [way] [to] [compute] [a] [numerical] [value] [for]




             - _P_ ( _ot,_ _**v**_ [in] _t_ _[,]_ _**[v]**_ [[:] _[i]_ []][)]
log _πθ_ ( _at|ot,_ _**v**_ [in] _t_ [)][ is][ �] _i_ _[n]_ =1 [log] _P_ ( _ot,_ _**v**_ [in] _t_ _[,]_ _**[v]**_ [[:] _[i][−]_ [1]][)]




.




                             - _P_ ( _ot,_ _**v**_ [in] _t_ _[,]_ _**[v]**_ [[:] _[i]_ []][)]
However, the naïve calculation log _πθ_ ( _at|ot,_ _**v**_ [in] _t_ [)] _[←]_ [�] _[n]_ _i_ =1 [log] _P_ ( _ot,_ _**v**_ [in] _t_ _[,]_ _**[v]**_ [[:] _[i][−]_ [1]][)]




may not be



ideal for computing _πθ_ ( _at|ot,_ _**v**_ [in] _t_ [)] [since] [our] [formatted] [output] _**[v]**_ [out] _t_ also contains CoT reasoning. This is because in _**v**_ [out] _t_ = [ _**v**_ [tht] _t_ _[,]_ _**[ v]**_ _t_ [act][]][,] [the] [CoT] [reasoning] [tokens] _**[v]**_ [tht] _t_ are generally much


5


longer than the action tokens _**v**_ [act] _t_ (see the blue and red parts in Figure 3 for examples, and
see Table 1 for a relative scaling of their sum log-likelihood). Hence the naïve computation log _πθ_ ( _at|ot,_ _**v**_ [in] _t_ [)] _[ ←]_ [log] _[ π][θ]_ [(] _**[v]**_ _t_ [tht] _[|][o][t][,]_ _**[ v]**_ _t_ [in][) + log] _[ π][θ]_ [(] _**[v]**_ _t_ [act] _[|][o][t][,]_ _**[ v]**_ _t_ [in] _[,]_ _**[ v]**_ _t_ [tht][)][ will make][ log] _[ π][θ]_ [(] _[a][t][|][o][t][,]_ _**[ v]**_ _t_ [in][)]
largely determined by the CoT tokens log _πθ_ ( _**v**_ [tht] _t_ _[|][o][t][,]_ _**[ v]**_ _t_ [in][)][, which is practically undesirable because]
our post-processing function _f_ only relies on _**v**_ [act] _t_ for decision-making.



As shown in Table 1, log _πθ_ ( _**v**_ [tht] _t_ _[|][o][t][,]_ _**[ v]**_ _t_ [in][)] [typically] [has]
a much larger magnitude than log _P_ ( _**v**_ [act] _t_ _[|][o][t][,]_ _**[ v]**_ _t_ [in] _[,]_ _**[ v]**_ _t_ [tht][)]
across all tasks we have tested (in terms of absolute
value). Hence, to mitigate the effect of the CoT tokens, we adopt a scaling factor _λ ∈_ [0 _,_ 1] to scale down
log _πθ_ ( _**v**_ [tht] _t_ _[|][o][t][,]_ _**[ v]**_ _t_ [in][)][ for obtaining a regularized version of]
log _πθ_ ( _at|ot,_ _**v**_ [in] _t_ [)][, which results in]

log _πθ_ ( _at|ot,_ _**v**_ [in] _t_ [)]

(4.3)
_←_ _λ_ log _πθ_ ( _**v**_ [tht] _t_ _[|][o]_ _t_ _[,]_ _**[ v]**_ [in] _t_ [) + log] _[ π]_ _θ_ [(] _**[v]**_ [act] _t_ _[|][o]_ _t_ _[,]_ _**[ v]**_ [in] _t_ _[,]_ _**[ v]**_ _t_ [tht][)] _[.]_



log `NL` `BJ` `EZP` `P24` `ALF`


_**v**_ [tht] _t_ -3.4 -2.2 -9.0 -37.6 -20.3
_**v**_ [act] _t_ 0.0 0.0 0.0 0.0 -0.4


Table 1: **The** **absolute** **values** **of** **sum** **log**
**probability of** _**v**_ **[tht]** _t_ **is much larger than** _**v**_ **[act]** _t_ **[.]**
Each number is averaged among 1000 samples
on our evaluation tasks to be introduced in
Section 5.



Empirically, we observe the scaling factor _λ_ could largely affect the final performance. As we will
show in Section 6.2, choosing an extreme _λ_ value (close to 1 or 0) will degrade overall performance.
All of our experiments adopt _λ ∈_ [0 _._ 2 _,_ 0 _._ 5].


**4.4** **Formal Implementation**


Putting the prompt construction function _h_ (Section 4.1), the post-processing function _f_ (Section 4.2),
and the computation of _πθ_ ( _at|ot,_ _**v**_ [in] _t_ [)][ (Section][ 4.3][) together, we conclude our method in Algorithm][ 1][.]


**Algorithm 1** Training VLM with RL


1: **Input:** An environment `env`, an initial VLM with parameters _θ_ 0.
2: **Input:** A post-processing function _f_, a CoT reasoning scaling factor _λ_ .
3: **Input:** Replay buffer size _B_, maximum episode length _T_ .
4: **for** _k_ = 0 _, . . ., K −_ 1 **do**
5: _t_ = 0 _▷_ Reset RL time step
6: _ot_ = `env` _._ `reset` () _▷_ Reset the initial state
7: _**v**_ [in] _t_ [=] _[ h]_ [(] _[o][t]_ [)] _▷_ Generate _**v**_ [in] _t_ [from] _[ o][t]_ [,] _[ h]_ [ is defined in Section][ 4.1]
8: _Bk_ = _∅_ _▷_ Initialize an on-policy replay buffer
9: **while** _|Bk| ≤_ _B_ **do**
10: _**v**_ [out] _t_ = _πθk_ ( _ot,_ _**v**_ [in] _t_ [)] _▷_ Generate text output
11: _at_ = _f_ ( _**v**_ [out] _t_ [)] _▷_ Obtain a legal action from _**v**_ [out] _t_ [,] _[ f]_ [is defined in Equation][ 4.1]
12: log _πθk_ ( _at|ot,_ _**v**_ [in] _t_ [) =] _[ λ]_ [ log] _[ π][θ]_ _k_ [(] _**[v]**_ [tht] _t_ _[|]_ _**[v]**_ _t_ [in][) + log] _[ π][θ]_ _k_ [(] _**[v]**_ [act] _t_ _[|][o][t][,]_ _**[ v]**_ _t_ [in] _[,]_ _**[ v]**_ _t_ [tht][)] _▷_ Equation 4.2
13: _rt, ot_ +1 = `env` _._ `step` ( _at_ )
14: _Bk_ = _Bk ∪{_ ( _ot, at, rt,_ _**v**_ [out] _t_ _[,]_ [ log] _[ π][θ]_ _k_ [(] _[a][t][|][o][t][,]_ _**[ v]**_ [in] _t_ [))] _[}]_ _▷_ Add data to the buffer _Bk_
15: _t_ = _t_ + 1
16: **if** _t_ = _T_ **then**
17: _t_ = 0 _▷_ Reset RL time step if the maximum step is reached
18: _o_ 0 = `env` _._ `reset` () _▷_ Reset environment
19: **end if**
20: _**v**_ [in] _t_ [=] _[ h]_ [(] _[o][t]_ [)] _▷_ Prepare the next _**v**_ [in] _t_
21: **end while**
22: Run PPO [55] with data _Bk_ to obtain _θk_ +1
23: **end for**
24: **Output:** _θK_ .


**5** **Evaluation Tasks**


How does our method improve a VLM’s decision-making capabilities in tasks that require finegrained vision-language reasoning or semantic understanding? To study this question, we adopt two
different domains: `gym_cards` and `alfworld` [58]. Our original `gym_cards` domain is a “gym-like”
environment [8] containing four tasks designed to test the decision-making capabilities of VLMs.


6


These tasks require fine-grained visual-language reasoning, specifically focusing on recognizing
numbers for arithmetic reasoning. In addition, we also adopt `alfworld` [58], which assesses the
decision-making capabilities of VLMs in an embodied AI setting that demands visual semantic
understanding. We present some examples of the visual observations of each task in Figure 4. We do
not include standard image-based Atari benchmarks [5, 39] due to limited computation resources. [4]


(a) `NumberLine` (b) `EZPoints` (c) `Points24` (d) `Blackjack` (e) `alfworld`


Figure 4: **Examples of observation of our evaluation tasks** . (a)-(d) are from our original `gym_cards` domain.
(a)-(c) are deterministic tasks with _increasing difficulties_ ; (d) is a stochastic task.


**5.1** **Gym Cards**


Our `gym_cards` domain is designed to evaluate a VLM’s decision-making capabilities requiring
fine-grained vision recognition and language reasoning. More precisely, tasks in the `gym_cards`
domain require the VLM to recognize the numbers (potentially from cards) and utilize the numbers
for language reasoning. As depicted in Figure 4, the first three tasks— `NumberLine`, `EZPoints`, and
`Points24` —are deterministic, and developed to assess the VLMs’ ability to identify and process numbers or mathematical operators at each time step. These tasks increase in complexity: `NumberLine`
requires recognition of two numbers in an image, `EZPoints` involves identifying numbers from two
cards, and `Points24` extends to recognizing four cards. The `Blackjack` task challenges the VLM
further by requiring the agent to reason based on visual information and adapt to stochastic outcomes.
This subsection outlines the goals of each task, and we leave the detailed descriptions of their state
spaces, action spaces, and reward functions to Appendix B.1.


**NumberLine.** In this task, **the goal is to move a number to the target on a synthetic number**
**line.** At each state _st_, the visual observation _ot_ contains two lines of text: “Target: _x_ ” and “Current:
_yt_ ”. The agent needs to move the current number _yt_ to the target number _x_, by outputting text _**v**_ [out] _t_
that interacts with the discrete action space { `"` + `"`, `"` _−_ `"` }. Mapping the _**v**_ [out] _t_ to `"` + `"` or `"` _−_ `"` will
increase or decrease the current number by 1, respectively.


**EZPoints.** In this task, **the goal is to output a formula using the numbers in the cards that**
**evaluates to 12.** At each state _st_, the agent observes an image of two cards and a text version of
(potentially incomplete) “formula” below the cards. The goal is to use _all_ numbers in the cards (only
once) to compute 12. The action space contains natural numbers in [1 _,_ 10], as well as operator in
_{_ `"` + `"` _,_ `"` _∗_ `"` _,_ `"` = `"` _}_ . At each state _st_, only operators and numbers that appear in the cards are _legal_
actions, and “J”, “Q”, or “K” are treated as “10”. In particular, if the output text _**v**_ [out] _t_ is mapped to
a legal action _at_ at state _st_, the text version of _at_ will be appended to the “formula” in the current
image of _st_ resulting _st_ +1, otherwise _st_ +1 will remain the same as _st_ .


**Points24.** In this task, **the** **goal** **is** **to** **output** **a** **formula** **using** **the** **numbers** **in** **the** **cards** **that**
**evaluates to 24.** The `Points24` task is a harder version of `EZPoints` as it contains 4 cards, hence
requiring the VLMs to generate a longer formula. The rules of `Points24` are similar to `EZPoints`,
despite two minor differences: the `Points24` task requires the VLM to compute a target number of
24, and its action space contains more operators: _{_ `"` + `"` _,_ `"` _−_ `"` _,_ `"` _∗_ `"` _,_ `"` _/_ `"` _,_ `"` = `"` _}_ .


**Blackjack.** In this task, **the goal is to win the current blackjack game.** At each state _st_, the visual
observation _ot_ consists of two cards (one face-down) from the dealer and all cards from the player.


4Image-based Atari tasks generally take at least 2 million environment steps to reach a reasonable performance [23]. Our method needs roughly 30 hours to run 15k environment steps due to the model size of the
backbone VLMs, which requires roughly half a year to run 2 million environment steps.


7


The agent’s goal in this task is to win the current game, by outputting text _**v**_ [out] _t_ that can be mapped to
{ `"stand"` _,_ `"hit"` }. The agent will receive one more card if _**v**_ [out] _t_ is mapped to `"hit"`, and the game
will terminate if _**v**_ [out] _t_ is mapped to `"stand"` .


**5.2** **ALFWorld**


While the `gym_cards` domain is designed to assess the VLM’s arithmetic reasoning requiring finegrained visual recognition, the `alfworld` environment aims at testing VLM’s decision-making tasks
requiring visual semantic understanding.


**ALFWorld.** The ALFWorld embodied environment [58] is combines a text-based interactive
environment [13] with a large vision-language instruction following dataset [57]. It contains 6
different types of goal-conditioned tasks (“Pick & Place”, “Examine in Light”, “Clean & Place”,
“Heat & Place”, “Cool & Place”, and “Pick Two & Place”), and **the agent’s goal is to navigate in the**
**environment via text-based actions** (e.g., `"go to shelf 1"`, `"examine sidetable 1"` ). Unlike
our original `gym_cards` environment, where all states share the same action space, the `alfworld`
environment contains a state-dependent _admissible action_ space – some actions are only available at
certain states. For example, if the agent’s goal is to “put some pillows on armchair”, then the agent
can only put a pillow _after_ picking up a pillow. Hence, to incorporate the state-dependent admissible
action set, our prompt of `alfworld` asks the VLM to choose among an admissible action. See
Figure 2 for an example of the visual observation of `alfworld` . We leave the detailed descriptions of
the `alfworld` (state space, action space, reward functions, and the CoT prompt) to Appendix B.2.


**6** **Experimental Results**


The first part of our experiment examines how our method improves the decision-making capabilities
of VLMs (Section 6.1). The second part investigates the role of CoT reasoning in our method
(Section 6.2). Details of our experimental setup are provided in Appendix C.


**6.1** **Improving VLM Decision-Making Capabilities**


Does our method improve the decision-making capabilities of VLM agents across various domains?
To investigate this, we assess how our method improves arithmetic tasks requiring fine-grained visual
recognition in the `gym_cards` domain and visual semantic reasoning in the `alfworld` domain. The
`gym_cards` experiments include deterministic tasks ( `NumberLine`, `EZPoints`, and `Points24`, each
with increasing difficulty) and a stochastic task ( `Blackjack` ). In the `alfworld` domain, we evaluate
overall performance and detailed task-specific performance as discussed in Section 5.2. We instantiate
our method on top of the llava-v1.6-mistral-7b [35] model and compare it against commercial models
(GPT4-V and Gemini), a supervised fine-tuned version of the llava-v1.6-mistral-7b model (LLaVAsft), [5] and a vanilla RL implementation using a CNN-based policy network (CNN+RL). [6] The final
results and learning curves are presented in Table 2 and Figure 5. Details of the experimental setup
are provided in Appendix C.


**Enhancing decision-making capabilities of VLM agents across various tasks.** As illustrated
in Table 2 and Figure 5, our method demonstrates consistent improvement across various tasks,
including deterministic ( `NumberLine` and `EZPoints` ) [7] or stochastic ( `Blackjack` ) arithmetic tasks
and visual semantic reasoning task ( `alfworld` ). Specifically, our method improves the average
performance from the initial LLaVA-sft model by **27.1%** on arithmetic tasks (18.4% _→_ 45.5%) and


5To ensure the RL training starts from a model with reasonable instruction following capabilities [45], our
RL training for VLM starts from the LLaVA-sft checkpoint of each task, we leave the detailed training pipeline
of our method to Appendix C.1.
6The CNN-based method adopts the same CLIP vision encoder as LLaVA-7b. Additionally, for tasks that
require text inputs (e.g., `alfworld` ), we adopt the `RoBERTa-base` [36] model to encode the text feature and
concatenate the text and CLIP visual features for downstream RL training. Details of our CNN-based model are
provided to Appendix C.2.
7Although `Points24` shares similar rules with `EZPoints`, it requires the VLM to recognize all four cards
and generate much longer equations. Most failure cases in `Points24` are caused by either inaccurate visual
perception or flawed language reasoning. We provide some examples of these failures in Appendix C.5.


8


```
             gym_cards alfworld

```

`NL` `EZP` `P24` `BJ` Avg. Exp. Data Pick Look Clean Heat Cool Pick2 Avg.


BUTLER _g_  -  -  -  -  - ✓ 33.0 17.0 26.0 70.0 76.0 12.0 22.0
BUTLER  -  -  -  -  - ✓ 46.0 22.0 39.0 74.0 100.0 24.0 37.0


CNN+RL 87.1 0 0 38.8 31.5 ✗ 0 0 0 0 0 0 0
GPT4-V 65.5 10.5 0 25.5 25.4 ✗ 38.2 12.1 **18.8** 6.7 17.8 14.6 19.4
Gemini 82.5 2.0 0 30.0 28.6 ✗ 34.6 **16.7** 0 0 0 12.0 13.5
LLaVA-sft 24.8 23.0 **2.6** 23.1 18.4 ✗ 39.2 0 14.4 11.1 0 **28.6** 17.7
Ours **89.4** **50.0** 2.3 **40.2** **45.5** ✗ **47.4** 14.7 10.4 **14.4** **18.8** 18.0 **21.7**
Table 2: **Average episode success rates (%) of different methods on** `gym_cards` **and** `alfworld` **.** For all
RL-based methods (CNN+RL and our method), we present the peak numbers (first 15k environment steps for the
`gym_cards` and 5k environment steps for `alfworld` ) from each training curve from Figure 5. We average the
performance of all 4 tasks on `gym_cards` with equal weight. Due to the nature of the `alfworld` environment,
where each subtask does not appear with equal probability, the average performance on `alfworld` is a weighted
average among all types of tasks. We mark the BUTLER _g_ and BUTLER agent [58] in gray since they require
expert data, while the remaining methods do not require expert data. As discussed by Shridhar et al. [58], the
performance discrepancy between BUTLER _g_ and BUTLER happens due to different decoding strategies in
evaluation strategies: BUTLER _g_ uses greedy decoding, which may repeat failed actions, whereas BUTLER
employs beam search during evaluation.



45


40


35


30


25

0 5k 10k 15k
env steps



20


10


|Col1|Ours|
|---|---|
||~~CNN+R~~<br>GPT4-V<br>~~Gemini~~<br>LLaVA-|



0



80


60


40


20



gym_cards/Numberline


0 5k 10k 15k
env steps



50

40

30

20

10

0



1k 2k 3k 4k 5k
env steps



5k 10k 15k
env steps



0



Figure 5: **Episode success rates (%) of different methods on** `gym_cards` **and** `alfworld` **during training** .
Left to right: `gym_cards/Numberline`, `gym_cards/EZPoints`, `gym_cards/Blackjack`, and `alfworld` (all).
The curves of `Points24` are not included because none of the tested methods achieve reasonable performance.


**4.0%** on visual semantic decision-making task (17.7% _→_ 21.7%). In addition, our method also
achieves the best performance among all comparative methods, surpassing the second-best method
by 14.0% (CNN+RL) on `gym_cards` and 2.3% (GPT4-V) on `alfworld` .


**6.2** **Understanding the Role of the CoT Reasoning**


In Section 6.1, we have demonstrated that our method improves the arithmetic and visual semantic
reasoning capabilities of VLM agents. Conceptually, our method can be viewed as an augmented
version of the standard CNN-based RL, where the text output [ _**v**_ [tht] _,_ _**v**_ [act] ] (from Figure 3) serve as the
text action _**v**_ [act], augmented by CoT reasoning _**v**_ [tht] . This raises an important question: How does the
CoT reasoning _**v**_ [tht] influence the overall performance of our method? To assess the impact of CoT
reasoning on our method’s performance, we conduct two sets of ablation experiments. The first set
(presented in Table 3 and Figure 6) evaluates our method without the CoT reasoning, and the second
part (shown in Figure 7) examines various scaling hyperparameters _λ_ for the log-likelihood of CoT
tokens, as defined in Equation 4.3.

```
               gym_cards alfworld

```

CoT `NL` `EZP` `P24` `BJ` Avg. Pick Examine Clean Heat Cool Pick 2 Avg.


✓ **89.4** **50.0** **2.3** 40.2 **45.5** **47.4** **14.7** **10.4** **14.4** **18.8** **18.0** **21.7**
✗ 26.9 29.9 0 **40.4** 24.3 40.5 12.0 2.8 8.5 14.4 17.7 16.3


Diff. (✓- ✗) **+62.5** **+20.1** **+2.3** -0.2 **+21.2** **+6.9** **+2.7** **+7.6** **+5.9** **+4.4** **+0.3** **+5.4**
Table 3: **Episode success rates (%) of our method with and without CoT reasoning.** We report the _best_
results from Figure 6 (first 15k environment steps for the `gym_cards` and 5k environment steps for `alfworld` ).


9


0



0 5k 10k 15k
env steps



1k 2k 3k 4k 5k
env steps



80


60


40


20





40


35


30


25



25


20


15


10



0 5k 10k 15k
env steps



50


40


30


20



5k 10k 15k
env steps



Figure 6: **Training** **curves** **of** **our** **method** **without** **and** **without** **the** **CoT** **reasoning.** Left to right:
`gym_cards/Numberline`, `gym_cards/EZPoints`, `gym_cards/Blackjack`, and `alfworld` (all). The curves
of `Points24` are not included because none of the tested methods achieve reasonable performance.


**The crucial role of CoT reasoning in performance improvement.** As presented in Table 3 and
Figure 6, the performance of our method significantly decreases without the CoT reasoning. [8] Besides
the improvement in the final performance, CoT reasoning appears to be a crucial component for
deterministic arithmetic tasks ( `NumberLine` and `EZPoints` ), as our method fails to improve these
two tasks without the CoT reasoning.



**The** **importance** **of** **moderate** **scaling** **factors** _λ_ **.** As discussed in Section 4.3, integrating CoT reasoning into our framework involves tuning an additional hyperparameter, _λ ∈_ [0 _,_ 1]
(proposed in Equation 4.3). To identify an optimal range for
_λ_, we conduct experiments assessing the impact of various _λ_ .
Our results in Figure 7 indicate that a moderate _λ_ (between
0.3 and 0.5) enables effective training on the `NumberLine` task.
Conversely, our method fails when _λ_ is set too large ( _≥_ 0 _._ 7)
or too small ( _≤_ 0 _._ 1), and we empirically find that an optimal
_λ_ typically falls within 0.2 to 0.5. This is because a large _λ_
results in an estimate of log _πθ_ ( _at|ot,_ _**v**_ [in] _t_ [)][ being overly influ-]
enced by log _πθ_ ( _**v**_ [tht] _t_ _[|][o][t][,]_ _**[ v]**_ _t_ [in][)][, while a small] _[ λ]_ [ value causes] _[ π][θ]_ [to]
be predominantly affected by log _πθ_ ( _**v**_ [act] _t_ _[|][o][t][,]_ _**[ v]**_ _t_ [in] _[,]_ _**[ v]**_ _t_ [tht][)][, thereby]
reducing the effect of the CoT reasoning in RL training.



80


60


40


20


|Col1|Col2|Col3|Col4|
|---|---|---|---|
||||0.1<br>0.3<br>|
||||0.5<br>0.7<br>|
||||~~0.9~~|
|||||
|||||
|||||



0



2k 4k 6k 8k 10k
env steps



Figure 7: **Episode success rates (%)**
**of our method under different** _λ_ **on**
`NumberLine` **.**



**7** **Conclusions, Limitations, and Future Directions**


In this paper, we introduce an algorithmic framework that directly fine-tunes VLMs using RL, with
the help of the VLM’s CoT reasoning capability. Empirical results demonstrate that our method can
enhance the decision-making abilities of VLMs across diverse domains that require fine-grained visual
recognition or visual semantic understanding. In addition, we demonstrate that CoT reasoning is a
crucial component for enabling RL training, allowing 7b VLMs to outperform established commercial
models such as GPT-4V and Gemini on most tasks. While our results suggest that CoT reasoning is
crucial to the performance improvement of VLM training with RL, we have not extensively explored
the effects of different prompting techniques in this work, which will be an interesting future direction.
The performance gain of our method is also limited by the size of the action space and the difficulties
of the task. For example `alfworld` does not enjoy as much performance gain as `gym_cards`, since
`alfworld` is a multi-task environment and it has a much larger action space than `gym_cards` .


**8** **Acknowledgement**


We would like to thank William Chen, Kuan Fang, Aviral Kumar, Qiyang Li, Fangchen Liu, Oier
Mees, Seohong Park, Karl Pertsch, Haozhi Qi, Chun-Hsiao Yeh, and Andrea Zanette for the early
discussions and suggestions on the project. A.S. is partly supported by AI2 Young Investigator
Grant, and a Gemma Academic Program Award. S.X. is partly supported by an Amazon research
award and the Google TRC program. This research was supported by NSF RI IIS-2246811, AFOSR
FA9550-22-1-0273, the joint Simons Foundation-NSF DMS grant #2031899, the ONR grant N0001422-1-2102, Tsinghua Berkeley Shenzhen Institute (TBSI) Research Fund, and the Hong Kong Center
for Construction Robotics Limited (HKCRC) Award 052245. We would also like to thank Hyperbolic
Labs for the computing support.


8Except for the `Blackjack` task, where the peak performance without CoT is slightly better (+0.2%).


10


**References**


[1] Marwa Abdulhai, Isadora White, Charlie Snell, Charles Sun, Joey Hong, Yuexiang Zhai, Kelvin
Xu, and Sergey Levine. Lmrl gym: Benchmarks for multi-turn reinforcement learning with
language models. _arXiv preprint arXiv:2311.18232_, 2023.

[2] Alekh Agarwal, Nan Jiang, Sham M Kakade, and Wen Sun. Reinforcement learning: Theory
and algorithms. _CS Dept., UW Seattle, Seattle, WA, USA, Tech. Rep_, 32, 2019.

[3] Stanislaw Antol, Aishwarya Agrawal, Jiasen Lu, Margaret Mitchell, Dhruv Batra, C Lawrence
Zitnick, and Devi Parikh. Vqa: Visual question answering. In _Proceedings_ _of_ _the_ _IEEE_
_international conference on computer vision_, pages 2425–2433, 2015.

[4] Kate Baumli, Satinder Baveja, Feryal Behbahani, Harris Chan, Gheorghe Comanici, Sebastian
Flennerhag, Maxime Gazeau, Kristian Holsheimer, Dan Horgan, Michael Laskin, et al. Visionlanguage models as a source of rewards. _arXiv preprint arXiv:2312.09187_, 2023.

[5] M. G. Bellemare, Y. Naddaf, J. Veness, and M. Bowling. The arcade learning environment: An
evaluation platform for general agents. _Journal of Artificial Intelligence Research_, 47:253–279,
jun 2013.

[6] Christopher Berner, Greg Brockman, Brooke Chan, Vicki Cheung, Przemysław D˛ebiak, Christy
Dennison, David Farhi, Quirin Fischer, Shariq Hashme, Chris Hesse, et al. Dota 2 with large
scale deep reinforcement learning. _arXiv preprint arXiv:1912.06680_, 2019.

[7] Rishi Bommasani, Drew A Hudson, Ehsan Adeli, Russ Altman, Simran Arora, Sydney von
Arx, Michael S Bernstein, Jeannette Bohg, Antoine Bosselut, Emma Brunskill, et al. On the
opportunities and risks of foundation models. _arXiv preprint arXiv:2108.07258_, 2021.

[8] Greg Brockman, Vicki Cheung, Ludwig Pettersson, Jonas Schneider, John Schulman, Jie Tang,
and Wojciech Zaremba. Openai gym. _arXiv preprint arXiv:1606.01540_, 2016.

[9] Thomas Carta, Clément Romac, Thomas Wolf, Sylvain Lamprier, Olivier Sigaud, and PierreYves Oudeyer. Grounding large language models in interactive environments with online
reinforcement learning. In _International Conference on Machine Learning_, pages 3676–3713.
PMLR, 2023.

[10] Louis Castricato, Alex Havrilla, Shahbuland Matiana, Duy V. Phung, Aman Tiwari, Jonathan
Tow, and Maksym Zhuravinsky. trlX: A scalable framework for RLHF, June 2023. URL
`[https://github.com/CarperAI/trlx](https://github.com/CarperAI/trlx)` .

[11] William Chen, Oier Mees, Aviral Kumar, and Sergey Levine. Vision-language models provide
promptable representations for reinforcement learning. _arXiv preprint arXiv:2402.02651_, 2024.

[12] Karl Cobbe, Vineet Kosaraju, Mohammad Bavarian, Mark Chen, Heewoo Jun, Lukasz Kaiser,
Matthias Plappert, Jerry Tworek, Jacob Hilton, Reiichiro Nakano, et al. Training verifiers to
solve math word problems. _arXiv preprint arXiv:2110.14168_, 2021.

[13] Marc-Alexandre Côté, Akos Kádár, Xingdi Yuan, Ben Kybartas, Tavian Barnes, Emery Fine,
James Moore, Matthew Hausknecht, Layla El Asri, Mahmoud Adada, et al. Textworld: A
learning environment for text-based games. In _Computer Games:_ _7th Workshop, CGW 2018,_
_Held in Conjunction with the 27th International Conference on Artificial Intelligence, IJCAI_
_2018, Stockholm, Sweden, July 13, 2018, Revised Selected Papers 7_, pages 41–75. Springer,
2019.

[14] Qingxiu Dong, Lei Li, Damai Dai, Ce Zheng, Zhiyong Wu, Baobao Chang, Xu Sun, Jingjing
Xu, and Zhifang Sui. A survey for in-context learning. _arXiv preprint arXiv:2301.00234_, 2022.

[15] Linxi Fan, Guanzhi Wang, Yunfan Jiang, Ajay Mandlekar, Yuncong Yang, Haoyi Zhu, Andrew
Tang, De-An Huang, Yuke Zhu, and Anima Anandkumar. Minedojo: Building open-ended
embodied agents with internet-scale knowledge. _Advances in Neural Information Processing_
_Systems_, 35:18343–18362, 2022.

[16] Chaoyou Fu, Peixian Chen, Yunhang Shen, Yulei Qin, Mengdan Zhang, Xu Lin, Zhenyu Qiu,
Wei Lin, Jinrui Yang, Xiawu Zheng, et al. Mme: A comprehensive evaluation benchmark for
multimodal large language models. _arXiv preprint arXiv:2306.13394_, 2023.

[17] Yao Fu, Hao Peng, Ashish Sabharwal, Peter Clark, and Tushar Khot. Complexity-based
prompting for multi-step reasoning. In _The Eleventh International Conference on Learning_
_Representations_, 2023. URL `[https://openreview.net/forum?id=yf1icZHC-l9](https://openreview.net/forum?id=yf1icZHC-l9)` .


11


[18] DeepMind Google. Introducing gemini: our largest and most capable ai model, 2023. URL

`[https://blog.google/technology/ai/google-gemini-ai/](https://blog.google/technology/ai/google-gemini-ai/)` .

[19] Tuomas Haarnoja, Aurick Zhou, Pieter Abbeel, and Sergey Levine. Soft actor-critic: Offpolicy maximum entropy deep reinforcement learning with a stochastic actor. In _International_
_conference on machine learning_, pages 1861–1870. PMLR, 2018.

[20] Joey Hong, Sergey Levine, and Anca Dragan. Zero-shot goal-directed dialogue via rl on
imagined conversations. _arXiv preprint arXiv:2311.05584_, 2023.

[21] Edward J Hu, yelong shen, Phillip Wallis, Zeyuan Allen-Zhu, Yuanzhi Li, Shean Wang,
Lu Wang, and Weizhu Chen. LoRA: Low-rank adaptation of large language models. In
_International Conference on Learning Representations_, 2022. URL `[https://openreview.](https://openreview.net/forum?id=nZeVKeeFYf9)`
`[net/forum?id=nZeVKeeFYf9](https://openreview.net/forum?id=nZeVKeeFYf9)` .

[22] Jiaxing Huang, Jingyi Zhang, Kai Jiang, Han Qiu, and Shijian Lu. Visual instruction tuning
towards general-purpose multimodal model: A survey. _arXiv preprint arXiv:2312.16602_, 2023.

[23] Shengyi Huang, Quentin Gallouédec, Florian Felten, Antonin Raffin, Rousslan Fernand Julien
Dossa, Yanxiao Zhao, Ryan Sullivan, Viktor Makoviychuk, Denys Makoviichuk, Mohamad H
Danesh, et al. Open rl benchmark: Comprehensive tracked experiments for reinforcement
learning. _arXiv preprint arXiv:2402.03046_, 2024.

[24] Wenlong Huang, Chen Wang, Ruohan Zhang, Yunzhu Li, Jiajun Wu, and Li Fei-Fei. Voxposer: Composable 3d value maps for robotic manipulation with language models. In _7th_
_Annual Conference on Robot Learning_, 2023. URL `[https://openreview.net/forum?id=](https://openreview.net/forum?id=9_8LF30mOC)`
`[9_8LF30mOC](https://openreview.net/forum?id=9_8LF30mOC)` .

[25] Albert Q Jiang, Alexandre Sablayrolles, Arthur Mensch, Chris Bamford, Devendra Singh
Chaplot, Diego de las Casas, Florian Bressand, Gianna Lengyel, Guillaume Lample, Lucile
Saulnier, et al. Mistral 7b. _arXiv preprint arXiv:2310.06825_, 2023.

[26] Takeshi Kojima, Shixiang Shane Gu, Machel Reid, Yutaka Matsuo, and Yusuke Iwasawa. Large
language models are zero-shot reasoners. _Advances in neural information processing systems_,
35:22199–22213, 2022.

[27] Ilya Kostrikov. Pytorch implementations of reinforcement learning algorithms. `[https://](https://github.com/ikostrikov/pytorch-a2c-ppo-acktr-gail)`
`[github.com/ikostrikov/pytorch-a2c-ppo-acktr-gail](https://github.com/ikostrikov/pytorch-a2c-ppo-acktr-gail)`, 2018.

[28] Heinrich Küttler, Nantas Nardelli, Alexander Miller, Roberta Raileanu, Marco Selvatici, Edward
Grefenstette, and Tim Rocktäschel. The nethack learning environment. _Advances in Neural_
_Information Processing Systems_, 33:7671–7684, 2020.

[29] Chunyuan Li. Large multimodal models: Notes on cvpr 2023 tutorial. _arXiv_ _preprint_
_arXiv:2306.14895_, 2023.

[30] Chunyuan Li, Zhe Gan, Zhengyuan Yang, Jianwei Yang, Linjie Li, Lijuan Wang, and Jianfeng
Gao. Multimodal foundation models: From specialists to general-purpose assistants. _arXiv_
_preprint arXiv:2309.10020_, 1(2):2, 2023.

[31] Hunter Lightman, Vineet Kosaraju, Yura Burda, Harri Edwards, Bowen Baker, Teddy Lee, Jan
Leike, John Schulman, Ilya Sutskever, and Karl Cobbe. Let’s verify step by step. _arXiv preprint_
_arXiv:2305.20050_, 2023.

[32] Fuxiao Liu, Tianrui Guan, Zongxia Li, Lichang Chen, Yaser Yacoob, Dinesh Manocha, and
Tianyi Zhou. Hallusionbench: You see what you think? or you think what you see? an imagecontext reasoning benchmark challenging for gpt-4v (ision), llava-1.5, and other multi-modality
models. _arXiv preprint arXiv:2310.14566_, 2023.

[33] Haotian Liu, Chunyuan Li, Yuheng Li, and Yong Jae Lee. Improved baselines with visual
instruction tuning. _arXiv preprint arXiv:2310.03744_, 2023.

[34] Haotian Liu, Chunyuan Li, Qingyang Wu, and Yong Jae Lee. Visual instruction tuning. In
_Thirty-seventh_ _Conference_ _on_ _Neural_ _Information_ _Processing_ _Systems_, 2023. URL `[https:](https://openreview.net/forum?id=w0H2xGHlkw)`
`[//openreview.net/forum?id=w0H2xGHlkw](https://openreview.net/forum?id=w0H2xGHlkw)` .

[35] Haotian Liu, Chunyuan Li, Yuheng Li, Bo Li, Yuanhan Zhang, Sheng Shen, and Yong Jae Lee.
Llava-next: Improved reasoning, ocr, and world knowledge, 2024.

[36] Yinhan Liu, Myle Ott, Naman Goyal, Jingfei Du, Mandar Joshi, Danqi Chen, Omer Levy, Mike
Lewis, Luke Zettlemoyer, and Veselin Stoyanov. Roberta: A robustly optimized bert pretraining
approach. _arXiv preprint arXiv:1907.11692_, 2019.


12


[37] Yuan Liu, Haodong Duan, Yuanhan Zhang, Bo Li, Songyang Zhang, Wangbo Zhao, Yike Yuan,
Jiaqi Wang, Conghui He, Ziwei Liu, et al. Mmbench: Is your multi-modal model an all-around
player? _arXiv preprint arXiv:2307.06281_, 2023.


[38] Chaochao Lu, Chen Qian, Guodong Zheng, Hongxing Fan, Hongzhi Gao, Jie Zhang, Jing Shao,
Jingyi Deng, Jinlan Fu, Kexin Huang, et al. From gpt-4 to gemini and beyond: Assessing the
landscape of mllms on generalizability, trustworthiness and causality through four modalities.
_arXiv preprint arXiv:2401.15071_, 2024.


[39] Marlos C. Machado, Marc G. Bellemare, Erik Talvitie, Joel Veness, Matthew J. Hausknecht,
and Michael Bowling. Revisiting the arcade learning environment: Evaluation protocols and
open problems for general agents. _Journal_ _of_ _Artificial_ _Intelligence_ _Research_, 61:523–562,
2018.


[40] Manolis Savva*, Abhishek Kadian*, Oleksandr Maksymets*, Yili Zhao, Erik Wijmans, Bhavana
Jain, Julian Straub, Jia Liu, Vladlen Koltun, Jitendra Malik, Devi Parikh, and Dhruv Batra.
Habitat: A Platform for Embodied AI Research. In _Proceedings of the IEEE/CVF International_
_Conference on Computer Vision (ICCV)_, 2019.


[41] Volodymyr Mnih, Koray Kavukcuoglu, David Silver, Andrei A Rusu, Joel Veness, Marc G
Bellemare, Alex Graves, Martin Riedmiller, Andreas K Fidjeland, Georg Ostrovski, et al.
Human-level control through deep reinforcement learning. _nature_, 518(7540):529–533, 2015.


[42] Yao Mu, Qinglong Zhang, Mengkang Hu, Wenhai Wang, Mingyu Ding, Jun Jin, Bin Wang,
Jifeng Dai, Yu Qiao, and Ping Luo. Embodiedgpt: Vision-language pre-training via embodied
chain of thought. _arXiv preprint arXiv:2305.15021_, 2023.


[43] OpenAI. Gpt-4, 2023. URL `[https://openai.com/research/gpt-4](https://openai.com/research/gpt-4)` .


[44] OpenAI. Gpt-4v, 2023. URL `[https://openai.com/research/gpt-4v-system-card](https://openai.com/research/gpt-4v-system-card)` .


[45] Long Ouyang, Jeffrey Wu, Xu Jiang, Diogo Almeida, Carroll Wainwright, Pamela Mishkin,
Chong Zhang, Sandhini Agarwal, Katarina Slama, Alex Ray, et al. Training language models to
follow instructions with human feedback. _Advances in Neural Information Processing Systems_,
35:27730–27744, 2022.


[46] Jiayi Pan, Yichi Zhang, Nicholas Tomlin, Yifei Zhou, Sergey Levine, and Alane Suhr. Autonomous evaluation and refinement of digital agents. _arXiv preprint arXiv:2404.06474_, 2024.


[47] Liangming Pan, Michael Saxon, Wenda Xu, Deepak Nathani, Xinyi Wang, and William Yang
Wang. Automatically correcting large language models: Surveying the landscape of diverse
self-correction strategies. _arXiv preprint arXiv:2308.03188_, 2023.


[48] Joon Sung Park, Joseph O’Brien, Carrie Jun Cai, Meredith Ringel Morris, Percy Liang, and
Michael S Bernstein. Generative agents: Interactive simulacra of human behavior. In _Proceed-_
_ings of the 36th Annual ACM Symposium on User Interface Software and Technology_, pages
1–22, 2023.


[49] Alec Radford, Jong Wook Kim, Chris Hallacy, Aditya Ramesh, Gabriel Goh, Sandhini Agarwal,
Girish Sastry, Amanda Askell, Pamela Mishkin, Jack Clark, et al. Learning transferable visual
models from natural language supervision. In _International conference on machine learning_,
pages 8748–8763. PMLR, 2021.


[50] Rajkumar Ramamurthy, Prithviraj Ammanabrolu, Kianté Brantley, Jack Hessel, Rafet Sifa,
Christian Bauckhage, Hannaneh Hajishirzi, and Yejin Choi. Is reinforcement learning (not) for
natural language processing: Benchmarks, baselines, and building blocks for natural language
policy optimization. In _The Eleventh International Conference on Learning Representations_,
2023. URL `[https://openreview.net/forum?id=8aHzds2uUyB](https://openreview.net/forum?id=8aHzds2uUyB)` .


[51] Jeff Rasley, Samyam Rajbhandari, Olatunji Ruwase, and Yuxiong He. Deepspeed: System
optimizations enable training deep learning models with over 100 billion parameters. In
_Proceedings of the 26th ACM SIGKDD International Conference on Knowledge Discovery &_
_Data Mining_, pages 3505–3506, 2020.


[52] Juan Rocamonde, Victoriano Montesinos, Elvis Nava, Ethan Perez, and David Lindner. Visionlanguage models are zero-shot reward models for reinforcement learning. In _The_ _Twelfth_
_International Conference on Learning Representations_, 2024. URL `[https://openreview.](https://openreview.net/forum?id=N0I2RtD8je)`
`[net/forum?id=N0I2RtD8je](https://openreview.net/forum?id=N0I2RtD8je)` .


13


[53] John Schulman, Sergey Levine, Pieter Abbeel, Michael Jordan, and Philipp Moritz. Trust
region policy optimization. In _International conference on machine learning_, pages 1889–1897.
PMLR, 2015.


[54] John Schulman, Philipp Moritz, Sergey Levine, Michael Jordan, and Pieter Abbeel. Highdimensional continuous control using generalized advantage estimation. In _Proceedings of the_
_International Conference on Learning Representations (ICLR)_, 2016.


[55] John Schulman, Filip Wolski, Prafulla Dhariwal, Alec Radford, and Oleg Klimov. Proximal
policy optimization algorithms. _arXiv preprint arXiv:1707.06347_, 2017.


[56] Bokui Shen, Fei Xia, Chengshu Li, Roberto Martín-Martín, Linxi Fan, Guanzhi Wang, Claudia
Pérez-D’Arpino, Shyamal Buch, Sanjana Srivastava, Lyne Tchapmi, et al. igibson 1.0: A
simulation environment for interactive tasks in large realistic scenes. In _2021_ _IEEE/RSJ_
_International Conference on Intelligent Robots and Systems (IROS)_, pages 7520–7527. IEEE,
2021.


[57] Mohit Shridhar, Jesse Thomason, Daniel Gordon, Yonatan Bisk, Winson Han, Roozbeh Mottaghi, Luke Zettlemoyer, and Dieter Fox. Alfred: A benchmark for interpreting grounded
instructions for everyday tasks. In _Proceedings of the IEEE/CVF conference on computer vision_
_and pattern recognition_, pages 10740–10749, 2020.


[58] Mohit Shridhar, Xingdi Yuan, Marc-Alexandre Cote, Yonatan Bisk, Adam Trischler, and
Matthew Hausknecht. {ALFW}orld: Aligning text and embodied environments for interactive
learning. In _International_ _Conference_ _on_ _Learning_ _Representations_, 2021. URL `[https:](https://openreview.net/forum?id=0IOX0YcCdTn)`
`[//openreview.net/forum?id=0IOX0YcCdTn](https://openreview.net/forum?id=0IOX0YcCdTn)` .


[59] David Silver, Aja Huang, Chris J Maddison, Arthur Guez, Laurent Sifre, George Van Den Driessche, Julian Schrittwieser, Ioannis Antonoglou, Veda Panneershelvam, Marc Lanctot, et al. Mastering the game of go with deep neural networks and tree search. _nature_, 529(7587):484–489,
2016.


[60] Charlie Victor Snell, Ilya Kostrikov, Yi Su, Sherry Yang, and Sergey Levine. Offline RL for
natural language generation with implicit language q learning. In _The Eleventh International_
_Conference on Learning Representations_, 2023. URL `[https://openreview.net/forum?](https://openreview.net/forum?id=aBH_DydEvoH)`
`[id=aBH_DydEvoH](https://openreview.net/forum?id=aBH_DydEvoH)` .


[61] Nisan Stiennon, Long Ouyang, Jeffrey Wu, Daniel Ziegler, Ryan Lowe, Chelsea Voss, Alec
Radford, Dario Amodei, and Paul F Christiano. Learning to summarize with human feedback.
_Advances in Neural Information Processing Systems_, 33:3008–3021, 2020.


[62] Zhiqing Sun, Sheng Shen, Shengcao Cao, Haotian Liu, Chunyuan Li, Yikang Shen, Chuang
Gan, Liang-Yan Gui, Yu-Xiong Wang, Yiming Yang, et al. Aligning large multimodal models
with factually augmented rlhf. _arXiv preprint arXiv:2309.14525_, 2023.


[63] Richard S Sutton and Andrew G Barto. _Reinforcement learning:_ _An introduction_ . MIT press,
2018.


[64] Andrew Szot, Max Schwarzer, Harsh Agrawal, Bogdan Mazoure, Walter Talbott, Katherine
Metcalf, Natalie Mackraz, Devon Hjelm, and Alexander Toshev. Large language models as
generalizable policies for embodied tasks. _arXiv preprint arXiv:2310.17722_, 2023.


[65] Shengbang Tong, Zhuang Liu, Yuexiang Zhai, Yi Ma, Yann LeCun, and Saining Xie. Eyes wide
shut? exploring the visual shortcomings of multimodal llms. _arXiv preprint arXiv:2401.06209_,
2024.


[66] Hugo Touvron, Thibaut Lavril, Gautier Izacard, Xavier Martinet, Marie-Anne Lachaux, Timothée Lacroix, Baptiste Rozière, Naman Goyal, Eric Hambro, Faisal Azhar, et al. Llama: Open
and efficient foundation language models. _arXiv preprint arXiv:2302.13971_, 2023.


[67] Hugo Touvron, Louis Martin, Kevin Stone, Peter Albert, Amjad Almahairi, Yasmine Babaei,
Nikolay Bashlykov, Soumya Batra, Prajjwal Bhargava, Shruti Bhosale, et al. Llama 2: Open
foundation and fine-tuned chat models. _arXiv preprint arXiv:2307.09288_, 2023.


[68] Mark Towers, Jordan K. Terry, Ariel Kwiatkowski, John U. Balis, Gianluca de Cola, Tristan
Deleu, Manuel Goulão, Andreas Kallinteris, Arjun KG, Markus Krimmel, Rodrigo PerezVicente, Andrea Pierré, Sander Schulhoff, Jun Jet Tai, Andrew Tan Jin Shen, and Omar G.
Younis. Gymnasium, March 2023. URL `[https://zenodo.org/record/8127025](https://zenodo.org/record/8127025)` .


14


[69] Oriol Vinyals, Igor Babuschkin, Wojciech M Czarnecki, Michaël Mathieu, Andrew Dudzik, Junyoung Chung, David H Choi, Richard Powell, Timo Ewalds, Petko Georgiev, et al. Grandmaster
level in starcraft ii using multi-agent reinforcement learning. _Nature_, 575(7782):350–354, 2019.

[70] Leandro von Werra, Younes Belkada, Lewis Tunstall, Edward Beeching, Tristan Thrush, Nathan
Lambert, and Shengyi Huang. Trl: Transformer reinforcement learning. `[https://github.](https://github.com/huggingface/trl)`
`[com/huggingface/trl](https://github.com/huggingface/trl)`, 2020.

[71] Guanzhi Wang, Yuqi Xie, Yunfan Jiang, Ajay Mandlekar, Chaowei Xiao, Yuke Zhu, Linxi Fan,
and Anima Anandkumar. Voyager: An open-ended embodied agent with large language models.
_arXiv preprint arXiv:2305.16291_, 2023.

[72] Ruoyao Wang, Peter Alexander Jansen, Marc-Alexandre Côté, and Prithviraj Ammanabrolu. Scienceworld: Is your agent smarter than a 5th grader? In _Conference on Empirical Methods in Nat-_
_ural Language Processing_, 2022. URL `[https://api.semanticscholar.org/CorpusID:](https://api.semanticscholar.org/CorpusID:247451124)`
`[247451124](https://api.semanticscholar.org/CorpusID:247451124)` .

[73] Xuezhi Wang, Jason Wei, Dale Schuurmans, Quoc V Le, Ed H. Chi, Sharan Narang, Aakanksha
Chowdhery, and Denny Zhou. Self-consistency improves chain of thought reasoning in language
models. In _The Eleventh International Conference on Learning Representations_, 2023. URL
`[https://openreview.net/forum?id=1PL1NIMMrw](https://openreview.net/forum?id=1PL1NIMMrw)` .

[74] Zihao Wang, Shaofei Cai, Guanzhou Chen, Anji Liu, Xiaojian Ma, and Yitao Liang. Describe,
explain, plan and select: Interactive planning with large language models enables open-world
multi-task agents. _arXiv preprint arXiv:2302.01560_, 2023.

[75] Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten Bosma, Fei Xia, Ed Chi, Quoc V Le,
Denny Zhou, et al. Chain-of-thought prompting elicits reasoning in large language models.
_Advances in Neural Information Processing Systems_, 35:24824–24837, 2022.

[76] Zhiheng Xi, Wenxiang Chen, Xin Guo, Wei He, Yiwen Ding, Boyang Hong, Ming Zhang,
Junzhe Wang, Senjie Jin, Enyu Zhou, et al. The rise and potential of large language model
based agents: A survey. _arXiv preprint arXiv:2309.07864_, 2023.

[77] Sherry Yang, Ofir Nachum, Yilun Du, Jason Wei, Pieter Abbeel, and Dale Schuurmans. Foundation models for decision making: Problems, methods, and opportunities. _arXiv_ _preprint_
_arXiv:2303.04129_, 2023.

[78] Shunyu Yao, Dian Yu, Jeffrey Zhao, Izhak Shafran, Thomas L Griffiths, Yuan Cao, and Karthik
Narasimhan. Tree of thoughts: Deliberate problem solving with large language models. _arXiv_
_preprint arXiv:2305.10601_, 2023.

[79] Shunyu Yao, Jeffrey Zhao, Dian Yu, Nan Du, Izhak Shafran, Karthik R Narasimhan, and
Yuan Cao. React: Synergizing reasoning and acting in language models. In _The_ _Eleventh_
_International Conference on Learning Representations_, 2023. URL `[https://openreview.](https://openreview.net/forum?id=WE_vluYUL-X)`
`[net/forum?id=WE_vluYUL-X](https://openreview.net/forum?id=WE_vluYUL-X)` .

[80] Weihao Yu, Zhengyuan Yang, Linjie Li, Jianfeng Wang, Kevin Lin, Zicheng Liu, Xinchao Wang,
and Lijuan Wang. Mm-vet: Evaluating large multimodal models for integrated capabilities.
_arXiv preprint arXiv:2308.02490_, 2023.

[81] Yuexiang Zhai, Shengbang Tong, Xiao Li, Mu Cai, Qing Qu, Yong Jae Lee, and Yi Ma.
Investigating the catastrophic forgetting in multimodal large language model fine-tuning. In
_Conference on Parsimony and Learning_, pages 202–227. PMLR, 2024.

[82] Denny Zhou, Nathanael Schärli, Le Hou, Jason Wei, Nathan Scales, Xuezhi Wang, Dale Schuurmans, Claire Cui, Olivier Bousquet, Quoc V Le, and Ed H. Chi. Least-to-most prompting
enables complex reasoning in large language models. In _The_ _Eleventh_ _International_ _Con-_
_ference on Learning Representations_, 2023. URL `[https://openreview.net/forum?id=](https://openreview.net/forum?id=WZH7099tgfM)`
`[WZH7099tgfM](https://openreview.net/forum?id=WZH7099tgfM)` .

[83] Yifei Zhou, Andrea Zanette, Jiayi Pan, Sergey Levine, and Aviral Kumar. Archer: Training
language model agents via hierarchical multi-turn rl. _arXiv preprint arXiv:2402.19446_, 2024.

[84] Deyao Zhu, Jun Chen, Xiaoqian Shen, Xiang Li, and Mohamed Elhoseiny. Minigpt-4: Enhancing vision-language understanding with advanced large language models. _arXiv preprint_
_arXiv:2304.10592_, 2023.

[85] Daniel M Ziegler, Nisan Stiennon, Jeffrey Wu, Tom B Brown, Alec Radford, Dario Amodei,
Paul Christiano, and Geoffrey Irving. Fine-tuning language models from human preferences.
_arXiv preprint arXiv:1909.08593_, 2019.


15


**A** **Contributions**


    - **YXZ:** proposed, led, and managed the project; integrated all code bases; ran all ablations for
method development; babysat all experiments; implemented the post-processing function _f_ ;
proposed and implemented the scaling factor _λ_ for action tokens; beautified the `gym_cards`
environment; maintained all codebases; wrote the major part of the paper.


    - **HB:** set up the infrastructure and initial experiments for supervised fine-tuning before RL
training; maintained all codebases; partially wrote the paper.


    - **ZL:** set up the `alfworld` environment; set up major infrastructures for data collection;
maintained all codebases; partially wrote the paper.


    - **JP:** proposed the CoT idea for end-to-end RL training; optimized the RL training framework
with quantization and enabled distributed training; implemented the initial version of the
`gym_cards` environment; partially wrote the paper.


    - **ST:** maintained the usage of LLaVA repo [34, 33, 35]; implemented the queries for GPT4-V
and Gemini; partially wrote the paper.


    - **YFZ:** implemented the initial version of RL training on LLaVA; partially wrote the paper.


    - **AS, SX, YL, YM, SL:** provided suggestions for the project. **AS, SX, SL** also provided
feedbacks on writing. **YM, SL** inspired **YXZ** to initiate the entire project.


**B** **Additional Details of the Evaluation Tasks**


**B.1** **Gym Cards**


**B.1.1** **NumberLine**


**State and action space.** In the `NumberLine` task, the visual observation at each state _st_ contains two
lines of text: “Target: _x_ ” and “Current: _yt_ ”, where _x, yt_ are both integers such that _x, yt_ _∈_ [0 _, n_ max ],
where _n_ max is an environment input variable that controls the maximum position of the numbers.
The goal is to move the current number _yt_ to the target number _x_, by sequentially choosing actions
from the discrete action space { `"` + `"`, `"` _−_ `"` }. We set _n_ max = 5 for all experiments in this work, but
_n_ max can be set to any positive integers. Choosing `"` + `"` or `"` _−_ `"` will increase or decrease the current
number _yt_ by 1, respectively, and the agent will stay at the boundary if it takes an action that attempts
to cross the boundary (e.g., taking _at_ = `"` + `"` when _yt_ = _n_ max or _at_ = `"` _−_ `"` when _xt_ = 0). See an
example of the state action transition in Figure 8.


_−→_ `"action"` : `"` + `"` _−→_


Figure 8: **An example of the transition in** `NumberLine` **.**


**Reward** **functions** **and** **the** **CoT** **prompts.** An episode in `NumberLine` ends when the current
number equals the target number or the maximum step _T_ = 2 _n_ max is reached. The agent receives
a terminal reward of _r_ ( _st, at_ ) = 1 when _yt_ +1 = _x_ . The agent also receives a reward penalty of
_r_ ( _st, at_ ) = _−_ 1 upon taking an incorrect action that does not result in a closer position to the target
( _|x −_ _yt| ≥|x −_ _yt_ +1 _|_ ), otherwise the agent receives reward _r_ ( _st, at_ ) = 0. In the example provided
above (Figure 8), the agent receives a reward _r_ = 0, since it moves closer to the target, but not
reaching the target yet. For the `NumberLine` task, we adopt the following CoT prompt in Figure 9,
and for the case without CoT reasoning (discussed in Section 6.2), we use the same prompt but
without the blue CoT reasoning parts.


16


**CoT prompt** _**v**_ **[in]** _t_ **[for task]** `[ NumberLine]`
You are playing a game called number line. You will see a target number and a current number in the
image. And your goal is to move the current number closer to the target by choosing either adding
or subtracting one to the current number. Your response should be a valid json file in the following
format:
{

"current number": "x",
"target number": "x",
"thoughts": {first read out the current and target number, then think carefully about which action to
choose},
"action": "-" or "+"
}


Figure 9: **Task-specific CoT prompt input** _**v**_ **[in]** _t_ **[for]** `[ NumberLine]` **[.]** [The][ blue][ part represents the CoT reasoning]
and the red part is the text-based action.


**B.1.2** **EZPoints**


**State and action space.** In the `EZPoints` task, the agent will observe an image of two cards and
a text version of “formula” below the cards, at each state _st_ . The goal is to use the cards in the
image to compute a target number of 12 and we view { `"J"`, `"Q"`, `"K"` } as `"10"` . The action space of
`EZPoints` is { `"1"`, `"2"`, .. ., `"10"`, `"` + `"`, `"` _∗_ `"`, `"` = `"` } and each number in the cards can _only be used_
_once_ . Any action attempting to either select a number not shown in the cards or use a card more than
once are _illegal_ . At _st_, if a _legal_ action _at_ is taken, the action will be appended to the text “formula”
in _st_ and becomes the next state _st_ +1. On the other hand, when an illegal action is taken, _st_ +1 will
remain the same as _st_ . All images generated from the `EZPoints` environment are guaranteed to have
a viable solution for computing 12.


_−→_ `"action"` : `"` + `"` _−→_


Figure 10: **An example of the transition in** `EZPoints` **.**


**Reward** **functions** **and** **the** **CoT** **prompts.** An episode terminates when `"` = `"` is taken or the
maximum step _T_ = 5 is reached. The agent receives a reward of _r_ = _−_ 1 upon taking an _illegal_
action, and _r_ = 0 while taking a legal action. When `"` = `"` is taken, the agent will receive a positive
reward _r_ = 10 if the formula equals 12, and _r_ = _−_ 1 otherwise. For the `EZPoints` task, we adopt the
following CoT prompt in Figure 11, and for the case without CoT reasoning (discussed in Section 6.2),
we use the same prompt but without the blue CoT reasoning parts and the brown part in Figure 11 is
the text version of the current formula directly extracted from the current state _st_ .


17


**CoT prompt** _**v**_ **[in]** _t_ **[for]** `[ EZPoints]`
You are an expert card game player. You are observing two cards in the image. You are observing the
current formula: `'` 5 `'` . You can choose between [ `'` 1 `'`, `'` 2 `'`, `'` 3 `'`, `'` 4 `'`, `'` 5 `'`, `'` 6 `'`, `'` 7 `'`, `'` 8 `'`, `'` 9 `'`, `'` 10 `'`,
`'` + `'`, `'`   - `'`, `'` = `'` ]. The number or operator you choose will be appended to the current formula. Note
that `'` J `'`, `'` Q `'`, and `'` K `'` count as `'` 10 `'` . Your goal is to output a formula that evaluates to 12, and each
number can only be used once. Your response should be a valid json file in the following format:
{

"cards": [x, y],
"current formula": `'` 5 `'`,
"thoughts": {First check whether the current formula `'` z `'` is complete. If the current formula `'` z `'`
is complete, output `'` = `'` . Otherwise consider which number or operator should be appended to the
current formula to make it equal 12.}
"action": "{number}" or "{operator}"
}


Figure 11: **Task-specific CoT prompt input** _**v**_ **[in]** _t_ **[for]** `[ EZPoints]` **[ given the observation in Figure][ 10]** [.] [The][ blue]
part represents the CoT reasoning, the red part is the text-based action, and the brown part is the state-dependent
text from the formula in the image.


**B.1.3** **Points24**


**State and action space.** Similar to `EZPoints`, the goal of `Points24` is also to generate a formula
to compute the target number of 24, using all four cards. `Points24` has a slightly larger action space:
{ `"1"`, `"2"`, . . ., `"10"`, `"` + `"`, `"` _−_ `"`, `"` _∗_ `"`, `"` _/_ `"`, `"` ( `"`, `"` ) `"`, `"` = `"` } and two more cards. Each number in the
cards can _only be used once_ . Similar to `EZPoints`, any action attempting to either select a number
not shown in the cards or use a card more than once are _illegal_ . At _st_, if a _legal_ action _at_ is taken,
the action will be appended to the text “formula” in _st_ and becomes the next state _st_ +1. When an
illegal action is taken, _st_ +1 will remain the same as _st_ . Different from `EZPoints` where all images
are guaranteed to have a viable solution for computing 12, the images generated by `Points24` do not
always have a viable solution to 24.


_−→_ `"action"` : `"` + `"` _−→_


Figure 12: **An example of the transition in** `Points24` **.**


**Reward functions and the CoT prompts.** The reward functions and termination conditions of
`Points24` are the same as those in `EZPoints` . An episode terminates when `"` = `"` is taken or the
maximum step _T_ = 20 is reached. The agent receives a reward of _r_ = _−_ 1 upon taking an _illegal_
action, and _r_ = 0 while taking legal actions. When `"` = `"` is taken, the agent will receive a positive
reward _r_ = 10 when the formula equals 24, and _r_ = _−_ 1 otherwise. For the `Points24` task, we
adopt the following CoT prompt in Figure 13, and for the case without CoT reasoning (discussed
in Section 6.2), we use the same prompt but without the blue CoT reasoning parts and the brown
part in Figure 13 is the text version of the current formula directly extracted from the current state _st_ .
We also provide an additional feature that allows us to view { `"J",` `"Q",` `"K"` } as { `"11",` `"12",`
`"13"` }, instead of { `"10"` }.


18


**CoT prompt** _**v**_ **[in]** _t_ **[for]** `[ Points24]`
You are an expert 24 points card game player. You are observing these four cards in the image. You
are observing the current formula: `'` (2 `'` . You can choose between [ `'` 1 `'`, `'` 2 `'`, `'` 3 `'`, `'` 4 `'`, `'` 5 `'`, `'` 6 `'`,
`'` 7 `'`, `'` 8 `'`, `'` 9 `'`, `'` 10 `'`, `'` + `'`, `'`   - `'`, `'`   - `'`, `'` / `'`, `'` ( `'`, `'` ) `'`, `'` = `'` ]. The number or operator you choose will be
appended to the current formula. Note that `'` J `'`, `'` Q `'`, and `'` K `'` count as `'` 10 `'` . Your goal is to output
a formula that evaluates to 24, and each number can only be used once. Your response should be a
valid json file in the following format:
{

"cards": [x, y, z, w],
"current formula": `'` (2 `'`
"thoughts": {First check whether the current formula equals 24. If the current formula equals 24,
output `'` = `'` . Otherwise consider which number or operator should be appended to the current formula
to make it equal 24.}
"action": "{number}" or "{operator}"
}


Figure 13: **Task-specific CoT prompt input** _**v**_ **[in]** _t_ **[for]** `[ Points24]` **[ given the observation in Figure][ 12][.]** [The][ blue]
part represents the CoT reasoning and the red part is the text-based action, brown part is the state-dependent text
that directly obtained from the formula in the image.


**B.1.4** **Blackjack**


**State and action space.** For the `Blackjack` task, the visual observation at state _st_ consists of two
cards (one face-down) from the dealer and all cards from the player. The agent’s goal in this task is to
win the current game, by choosing actions in { `"stand"` _,_ `"hit"` }. The agent will receive a new card
upon choosing `"hit"` . See Figure 14 for an example transition.


_−→_ `"action"` : `"hit"` _−→_


Figure 14: **An example of the transition in** `Blackjack` **.**


**Reward functions and the CoT prompts.** The game terminates when the player chooses `"stand"`
or busts (total points exceed 21). We adopt the same reward function as the `Blackjack-v1` task in
Gymnasiym [68], where _r_ ( _st, at_ ) = 1 _,_ 0 _, −_ 1 upon win, draw, and loss, respectively. We also provide
a similar feature as Gymnasium [68], where the “blackjack” winning (the agent win with an `"A"`
and a `"10",` `"J",` `"Q"` or `"K"` ) reward _r_ of the player will become 1 _._ 5. In the example provided in
Figure 14, the game has not terminated after taking the action `"hit"`, hence the agent will not receive
any rewards, even though it has total points of 21. For the `Blackjack` task, we adopt the following
CoT prompt in Figure 15, and for the case without CoT reasoning (discussed in Section 6.2), we use
the same prompt but without the blue CoT reasoning parts.


**CoT prompt** _**v**_ **[in]** _t_ **[for]** `[ Blackjack]`
You are a blackjack player. You are observing the current game state, you can choose between

[ `'` stand `'`, `'` hit `'` ]. Your response should be a valid json file in the following format:
{

"thoughts": "{first describe your total points and the dealer’s total points then think about which
action to choose}",
"action": "stand" or "hit"
}


Figure 15: **Task-specific CoT prompt input** _**v**_ **[in]** _t_ **[for]** `[ Blackjack]` **[.]** [The][ blue][ part represents the CoT reasoning]
and the red part is the text-based action.


19


**B.2** **ALFWorld**


**State** **and** **action** **space.** Inherited from Text World [13], at each state _st_ of `alfworld`, the
agent will observe an RGB image and text-based description. The action space of `alfworld`
can be summarized these following format [58]: (1) `goto` `{recep}` ; (2) `take` `{obj}` `from`
`{recep}` ; (3) `put` `{obj}` `in/on` `{recep}` ; (4) `open` `{recep}` ; (5) `close` `{recep}` ; (6) `toggle`
`{obj}{recep}` ; (7) `clean` `{obj}` `with` `{recep}` ; (8) `heat` `{obj}` `with` `{recep}` ; (9) `cool`
`{obj}` `with` `{recep}`, where `{obj}` and `{recep}` stands for objects and receptacles. See Figure 16

for an example of the state action transition in the `alfworld` environment.


`"action"` :
_−→_ `"go to cabinet 2"` _[−→]_



You arrive at loc 0. The cabinet 1 is
open. On the cabinet 1, you see a pan
1, a kettle 1, a winebottle 1, a apple
1, a stoveknob 1, a stoveknob 2, a
stoveknob 3, a stoveknob 4, a knife 1,
a saltshaker 1, and a bread 1.



You arrive at loc 2. The cabinet 2
is open. On the cabinet 2, you see
a houseplant 1, a pot 1, a bread 1, a
kettle 1, a bowl 1, a soapbottle 1, and
a knife 2.



Figure 16: **An example of the transition in** `alfworld` **.**


**Reward functions and the CoT prompts.** Each state _s ∈S_ of `alfworld` has a set of _admissible_
_actions A_ `adm` ( _s_ ), a final goal _g_ `task`, and subgoals _g_ `sub` . Since the goal of `alfworld` is to complete the
language-based goal-conditioned tasks, we reward the agent upon reaching subgoals and completing
the task, while penalizing the agent upon taking inadmissible actions. To summarize, we define the
reward function of `alfworld` as _r_ ( _st, at, st_ +1 _|g_ `task` ) = 50 _∗_ **1** _{st_ +1 = _g_ `task` _}_ + **1** _{st_ +1 = _g_ `sub` _} −_
**1** _{at_ _∈A/_ `adm` ( _st_ ) _}_ . For the `alfworld` task, we adopt the following CoT prompt in Figure 17, and for
the case without CoT reasoning (discussed in Section 6.2), we use the same prompt but without the
blue CoT reasoning parts and the brown part in Figure 17 is the text description of the task directly
extracted from the current state _st_ .


20


**CoT prompt** _**v**_ **[in]** _t_ **[for]** `[ alfworld]`
Your are an expert in the ALFRED Embodied Environment. You are also given the following text
description of the current scene: [ `'` You arrive at loc 0. The cabinet 1 is open. On the cabinet 1, you
see a pan 1, a kettle 1, a winebottle 1, a apple 1, a stoveknob 1, a stoveknob 2, a stoveknob 3, a
stoveknob 4, a knife 1, a saltshaker 1, and a bread 1. `'` ]. Your task is to put a cool mug in cabinet.
Your admissible actions of the current situation are: [ `'` go to countertop 1 `'`, `'` go to cabinet 2 `'`, `'` go to
countertop 2 `'`, `'` go to stoveburner 1 `'`, `'` go to drawer 1 `'`, `'` go to drawer 2 `'`, `'` go to drawer 3 `'`, `'` go to
stoveburner 2 `'`, `'` go to stoveburner 3 `'`, `'` go to stoveburner 4 `'`, `'` go to drawer 4 `'`, `'` go to cabinet 3 `'`,
`'` go to cabinet 4 `'`, `'` go to microwave 1 `'`, `'` go to cabinet 5 `'`, `'` go to cabinet 6 `'`, `'` go to cabinet 7 `'`, `'` go
to sink 1 `'`, `'` go to sinkbasin 1 `'`, `'` go to fridge 1 `'`, `'` go to toaster 1 `'`, `'` go to coffeemachine 1 `'`, `'` go to
cabinet 8 `'`, `'` go to drawer 5 `'`, `'` go to drawer 6 `'`, `'` go to drawer 7 `'`, `'` go to drawer 8 `'`, `'` go to shelf
1 `'`, `'` go to shelf 2 `'`, `'` go to countertop 3 `'`, `'` go to shelf 3 `'`, `'` go to drawer 9 `'`, `'` go to garbagecan 1 `'`,
`'` open cabinet 1 `'`, `'` close cabinet 1 `'`, `'` take pan 1 from cabinet 1 `'`, `'` take kettle 1 from cabinet 1 `'`,
`'` take winebottle 1 from cabinet 1 `'`, `'` take apple 1 from cabinet 1 `'`, `'` take stoveknob 1 from cabinet
1 `'`, `'` take stoveknob 2 from cabinet 1 `'`, `'` take stoveknob 3 from cabinet 1 `'`, `'` take stoveknob 4 from
cabinet 1 `'`, `'` take knife 1 from cabinet 1 `'`, `'` take saltshaker 1 from cabinet 1 `'`, `'` take bread 1 from
cabinet 1 `'`, `'` inventory `'`, `'` look `'`, `'` examine cabinet 1 `'` ]. Your response should be a valid json file in
the following format:
{

"thoughts": "first describe what do you see in the image using the text description, then carefully
think about which action to complete the task. ",
"action": "an admissible action"
}


Figure 17: **Task-specific CoT prompt input** _**v**_ **[in]** _t_ **[for]** `[ alfworld]` **[ given the observation in Figure][ 16][.]** [The][ blue]
part represents the CoT reasoning and the red part is the text-based action, brown part is the state-dependent text
that directly obtained from the text description and the admissible actions of the current state.


**C** **Additional Details on the Experiments**


We provide additional detailed of the experimental results in Section 6 here. Details of our experimental pipeline is provided in Section C.1, including preparing the initial SFT checkpoints and the RL
training. Section C.2 contains details setup of all comparative methods. We list task-specific training
details in Section C.3. We provide additional experimental results in Section C.4. Section C.5 lists
several failure examples of the `Points24` tasks.


**C.1** **Experimental Pipeline**


Our experiments adopt a similar pipeline as RLHF [45], where we first apply supervised fine-tuning
(SFT) to the backbone llava-v1.6-mistral-7b model, before RL training. As outlined by Ouyang et al.

[45], the RLHF training procedure consists of three distinct stages: SFT, learning reward models from
human preference data, and applying RL with the learned reward models. Our pipeline is analogous
to RLHF but without requiring the collection of human preference data for learning reward models,
as we can directly collect rewards from the environment. [9] Consequently, our experimental pipeline
only contains two stages: SFT and RL, which we will explain below.


**Supervised** **fine-tuning.** For the original `gym_cards` environment, we manually construct
instruction-following data for all tasks following the format specified in Figure 3 of Section 4.1.
As for `alfworld`, we use GPT4-V [44] to collect instruction following data for SFT. For all tasks,
we prepare two versions of the instruction-following data, one with CoT and one without. We
leave the details of the CoT prompts for each task, and the details of each fine-tuning dataset in
Appendix D. After constructing the instruction-following data (with and without CoT), we finetune llava-v1.6-mistral-7b for 1 epoch on the collected data for each task and report the results for
LLaVA-sft.


**RL training.** For each task, we start our RL training from the LLaVA-sft checkpoint. The LLaVA
model [34] consists of three jointly trainable components, a CLIP vision encoder [49], an LLM


9We adopt the same pipeline for the evaluation without CoT reasoning (discussed in Section 6.2) while
changing the data for SFT as well as _**v**_ [in] (see more details on our SFT data and _**v**_ [in] in Appendix D)


21


backbone [66, 67, 25], and an MLP projector that connects visual features and the word embeddings,
and we directly apply PPO [55] to train all three components. Due to computation resource limitations,
we instantiate our experiments via LoRA [21], with the LoRA configuration of _r_ = 128 _, α_ =
256 _,_ `dropout` = 0 _._ 05, for all trainable components. For the CoT coefficient _λ_, we set _λ_ = 0 _._ 5 in the
`gym_cards` domain and _λ_ = 0 _._ 2 in `alfworld` .


**C.2** **Experimental Setup for Comparative Methods**


**GPT4-V and Gemini.** All of our experimental results on GPT4-V [44] and Gemini [18] are tested
on March 15, 2024, using the same prompt for our RL training (see detailed prompts in Appendix D).
For `gym_cards`, the numbers from both GPT4-V and Gemini are averaged among the same number
of episodes: 200 episodes for deterministic tasks ( `NumberLine`, `EZPoints` and `Points24` ); 1000
episodes for stochastic task ( `Blackjack` ). As for `alfworld`, we report the performance of GPT4-V
on all 1000 episodes we collected, see Appendix D.5 for our data collection on `alfworld` using
GPT4-V. Due to the financial budget, we report the results of Gemini using 100 episodes.


**LLaVA-sft.** For each number of LLaVA-sft, we first collect the instruction-following dataset for
each task and then fine-tune LLaVA-1.6-7b for 1 epoch on the collected data using the official LLaVA
fine-tuning script. [10] Details of our data collection process is provided in Appendix D. We also _use_
_the same LLaVA-sft checkpoint as initializations for the downstream RL training_ .


**CNN-based RL.** Since the LLaVA-7b model adopts a CLIP ViT-L/14 vision encoder which is more
powerful than vanilla CNN embeddings, we instantiate our CNN-based method using the feature from
the same CLIP ViT-L/14 for a fair comparison. For tasks ( `EZPoints`, `Points24`, and `alfworld`,
see our detailed prompt in Appendix D) that require text inputs, we adopt the `RoBERTa-base` [36]
model to encode the text feature and concatenate the text and CLIP visual features for downstream
RL training. After obtaining the CLIP (potentially concatenated with text) features, we adopt 2 MLP
layers followed by a fully connected layer to map the clip features into the action space. We adopt
the PPO [55] implementation from Kostrikov [27] as the backbone RL algorithm. In addition, we
adopt a `CosineAnnealingLR` learning rate scheduler, with the initial learning rate of 3 _e −_ 4, the
final learning rate of 1 _e −_ 8, and the maximum learning rate step of 25. The remaining task specific
hyperparameters are the same as the VLM case in Section C.3.


**C.3** **General Setup for End-to-End RL Training**


All experiments are conducted on an 8 A100s DGX machine (80G), while the maximum VRAM
requirement is _<_ 40G. Each curve from Figure 5 and 6 takes at most 36 hours to finish. We adopt
DeepSpeed zero2 [51] for multi-gpu training. During our training for the VLM, we directly train
all trainable components (vision encoder, LLM, and the MLP projector). We adopt an open-source
implementation [27] for the PPO. Inspired by von Werra et al. [70], Castricato et al. [10], we apply a
3-layer MLP as the value head, on top of the output hidden states layer _before the output tokens_, to
estimate the value function _V_ _[π][θ]_ . After obtaining the value estimate _Vϕ_, we adopt the generalized
advantage estimator (GAE) [54] to estimate the return function _R_ [ˆ] ( _s_ ) and the advantage function _A_ [ˆ] _[π][θ]_
of _πθ_ . In addition, we adopt a `CosineAnnealingLR` learning rate scheduler, with the initial learning
rate of 1 _e −_ 5, the final learning rate of 1 _e −_ 9, and the maximum learning rate step of 25. For
all experiments in the `gym_cards` and `alfworld` environment, we set the scaling hyperparameter
_λ_ = 0 _._ 5 _,_ 0 _,_ 2, respectively. The learning rate decay happens after every PPO update, which consists
of 4 epochs of gradient updates with PPO. The number of data for on-policy training and batch size
is task-dependent, we list them below.


**Numberline** **and** **Blackjack.** For `NumberLine` and `Blackjack`, our VLM training curves in
Figure 5 use 4 GPUs. Our implementation naturally enables different random seeds on different
GPUs, hence our VLM curves are averaged among 4 seeds. For one PPO update on each GPU,
we collect 512 transitions, with a batch size of 128 per GPU (batch size = 512 in total). The
episode return and success rate are averaged with `NumberLine`, `Blackjack` are averaged among 200
and 1000 episodes, respectively. We averaged the return of `Blackjack` on more episodes because


10 `[https://github.com/haotian-liu/LLaVA/blob/main/scripts/v1_5/finetune.sh](https://github.com/haotian-liu/LLaVA/blob/main/scripts/v1_5/finetune.sh)` . We start
from the llava-v1.6-mistral-7b instead of the v1.5 checkpoint in the script.


22


`Blackjack` contains stochastic while `NumberLine` is a deterministic task. We adopt the same number
of transitions and batch size for the on-policy training in the CNN-based method on both tasks. The
CNN-based methods are averaged among 4 random seeds as well.


**EZPoints and Points24.** For `EZPoints` and `Points24`, our VLM training curves in Figure 5 use
4 GPUs. Our implementation naturally enables different random seeds on different GPUs, hence
our VLM curves are averaged among 4 seeds. For one PPO update on each GPU, we collect 1024
transitions, with a batch size of 128 per GPU (batch size = 512 in total). We use 1024 transitions
because the episodes of `EZPoints` and `Points24` usually have longer horizons than `NumberLine`
and `Blackjack` . The episode return and success rate are averaged with `EZPoints` and `Points24`
are averaged among 200. We adopt the same number of transitions and batch size for the on-policy
training in the CNN-based method on both tasks. The CNN-based methods are averaged among 4
random seeds as well.


**ALFWorld.** For the `alfworld` environment, each run of our VLM training curves in Figure 5
and Figure 19 are conducted on one GPU, and each curve is averaged among 4 seeds. We do not
conduct multi-GPU training for `alfworld` because the on-policy sampling time has a huge variance
on different GPUs, which will largely increase the synchronization time across different GPUs. For
each PPO update, we collect 1024 transitions, and with a batch size of 256. The episode success rates
are averaged among 200 episodes. We adopt the same number of transitions and batch size for the
on-policy training in the CNN-based method on both tasks. The CNN-based methods are averaged
among 4 random seeds as well.


**C.4** **Additional Experimental Results**


We provide some additional experimental results on the episode returns on the `gym_cards` and the
task-specific training curves for `alfworld` here.


Episode Success Rate (%) Episode Return

```
             NL EZP P24 BJ NL EZP P24 BJ

```

Table 4: **Average episode success rates and returns of different methods on** `gym_cards` **.** For all RL-based
methods (CNN and our method), we report the _best_ results in each training curve from Figure 18.



gym_cards/Numberline
1.0


0.0



0 5k 10k 15k
env steps



4.0


2.0


0.0


-2.0


-4.0



-1.0


-2.0


-3.0



|Col1|Col2|Col3|Col4|Col5|Col6|
|---|---|---|---|---|---|
|||||||
|||||||
||||||~~Ours~~<br>|
||||||~~CNN+RL~~<br>GPT4-V<br>|
|||||||
||||||~~Gemini~~|
||||||LLaVA-sft|


0 5k 10k 15k
env steps



0



5k 10k 15k
env steps



-0.1


-0.2


-0.3


-0.4


-0.5



Figure 18: **Episode returns of different methods on** `gym_cards` **.** An extended version of Figure 5 containing
episode success rates and returns.


23


|Col1|Col2|Col3|Col4|Col5|Col6|
|---|---|---|---|---|---|
|||||||
|||||||
|||||||
|||||||


1k 2k 3k 4k 5k
env steps

|Col1|Col2|Col3|Col4|Col5|Col6|
|---|---|---|---|---|---|
|||||||
|||||||
|||||||
|||||||
|||||||
|||||||



1k 2k 3k 4k 5k
env steps



60


40


20


0


40


30


20


10


0



|Col1|Col2|Col3|Col4|Col5|Col6|
|---|---|---|---|---|---|
|||||||
|||||||
|||||||
|||||||


1k 2k 3k 4k 5k
env steps

|Col1|Col2|Col3|Col4|Col5|Col6|Col7|
|---|---|---|---|---|---|---|
||||||||
||||||||
||||||||
||||||||
||||||||



1k 2k 3k 4k 5k
env steps



20


15


10


5


0


|Col1|Col2|Col3|Col4|Col5|Col6|
|---|---|---|---|---|---|
|||||||
|||||||
|||||||
|||||||
|||||||



100

80

60

40

20

0



1k 2k 3k 4k 5k
env steps



30


20


10


0


50

40

30

20

10

0



|Col1|Col2|Col3|Col4|Col5|Col6|Col7|
|---|---|---|---|---|---|---|
||||||Ours<br>||
||||||~~CNN+RL~~<br>GPT4-V||
||||||Gemini||
||||||LLaVA-sft||
||||||||
||||||||
||||||||


1k 2k 3k 4k 5k
env steps



Figure 19: **Episode success rates our method on different types of tasks from** `alfworld` **.** The curves come
from the same run as experiments from the `alfworld` figure of Figure 5.


**C.5** **Failure Examples of** `Points24`


**Ground Truth Cards:** **[2, 8, 5, J]**
**Error Type:** **Fail to recognize all numbers**
{
"cards": [10, 10, 5, 9],
"formula": "10+",
"thoughts": " `'` 10+ `'` is an incomplete formula, since `'` 10+10-5+9=24 `'`, I should append `'` 10 `'` to the
current formula",
"action": "10"
}


Figure 20: **Failure example of** `Points24` **due to incorrect perception.** In this example, the VLM fails to
recognize the four numbers from the cards correctly as it only recognizes 2 numbers correctly. The reasoning
part is correct, as it indeed generates a formula that equals 24.


**Ground Truth Cards:** **[J, K, 5, 6]**
**Error Type:** **Fail to recognize all numbers**
{
"cards": [10, 10, 5, 7],
"formula": "10+10+5+",
"thoughts": " `'` 10+10+5 `'` is an incomplete formula, since `'` 10+10+5+7=24 `'`, I should append `'` 7 `'` to
the current formula",
"action": "7"
}


Figure 21: **Failure example of** `Points24` **due to incorrect perception and reasoning.** In this example, the
VLM fails to recognize the four numbers from the cards correctly as it only recognizes 3 numbers correctly. The
reasoning part is also incorrect, 10+10+5+7 does not equal 24.


24


**D** **Details on Supervised Fine-tuning Data**


In this section, we provide detailed descriptions of the supervised fine-tuning data for all tasks.


**D.1** **NumberLine**


In the `NumberLine` task, we collect 20k instruction-following expert data samples using a task solver.
See examples with and without CoT in Figure 22 and 23, respectively.


**Inputs:**
You are playing a game called number line. You will see a target number
and a current number in the image. And your goal is to move the current
number closer to the target by choosing either adding or subtracting one
to the current number. Your response should be a valid json file in the
following format:
{
"current number": "x",
"target number": "x",
"thoughts": {first read out the current and target number, then think
carefully about which action to choose},
"action": "-" or "+"
}


**Responses:**
{
"current number": "0",
"target number": "3",
"thoughts": "The current number is 0, which is smaller than the target number is 3. To move the
current number closer to the target, I should increase the current number by choosing +.",
"action": "+"
}


Figure 22: An example of the supervised fine-tuning data for `NumberLine` with CoT.


**Inputs:**
You are playing a game called number line. You will see a target number
and a current number in the image. And your goal is to move the current
number closer to the target by choosing either adding or subtracting one
to the current number. Your response should be a valid json file in the
following format:
{
"action": "-" or "+"
}


**Responses:**
{
"action": "+"
}


Figure 23: An example of the supervised fine-tuning data for `NumberLine` without CoT.


25


**D.2** **Blackjack**


In the `Blackjack` task, we collect 50k instruction-following expert data samples following an
open-sourced solver. [11] See examples with and without CoT in Figure 24 and 25, respectively.


**Inputs:**
You are a blackjack player. You are observing the current game state, you
can choose between [ `'` stand `'`, `'` hit `'` ]. Your response should be a valid
json file in the following format:
{
"thoughts": "{first describe your total points and the dealer’s total points
then think about which action to choose}",
"action": "stand" or "hit"
}


**Responses:**
{
"thoughts": "I have 13 points and the dealer has 8 points. I think I should hit.",
"action": "hit"
}


Figure 24: An example of the supervised fine-tuning data for `Blackjack` with CoT.


**Inputs:**
You are a blackjack player. You are observing the current game state, you
can choose between [ `'` stand `'`, `'` hit `'` ]. Your response should be a valid
json file in the following format:
{
"action": "stand" or "hit"
}


**Responses:**
{
"action": "hit"
}


Figure 25: An example of the supervised fine-tuning data for `Blackjack` without CoT.


11 `[https://www.cs.cmu.edu/~chengwen/blackjack/blackjack.html](https://www.cs.cmu.edu/~chengwen/blackjack/blackjack.html)`


26


**D.3** **EZPoints**


In the `EZPoints` task, we directly collect 50k instruction-following expert data samples using a task
solver. See examples with and without CoT in Figure 26 and 27, respectively.


**Inputs:**
You are an expert card game player. You are observing two cards in the
image. You are observing the current formula: `'` 5 `'` . You can choose
between [ `'` 1 `'`, `'` 2 `'`, `'` 3 `'`, `'` 4 `'`, `'` 5 `'`, `'` 6 `'`, `'` 7 `'`, `'` 8 `'`, `'` 9 `'`, `'` 10 `'`, `'` + `'`, `'` - `'`,
`'` = `'` ]. The number or operator you choose will be appended to the current
formula. Note that `'` J `'`, `'` Q `'`, and `'` K `'` count as `'` 10 `'` . Your goal is to
output a formula that evaluates to 12, and each number can only be used
once. Your response should be a valid json file in the following format:
{
"cards": [x, y],
"current formula": `'` 5 `'`,
"thoughts": {First check whether the current formula `'` z `'` is complete. If the current formula `'` z `'` is
complete, output `'` = `'` . Otherwise consider which number or operator should be appended to the
current formula to make it equal 12.}
"action": "{number}" or "{operator}"
}


**Responses:**
{
"cards": [7, 5],
"formula": "5",
"thoughts": " `'` 5 `'` is an incomplete formula, since `'` 5+7=12 `'`, I should append `'` + `'` to the current
formula", "action": "+"
}"


Figure 26: An example of the supervised fine-tuning data for `EZPoints` with CoT.


**Inputs:**
You are an expert card game player. You are observing two cards in the
image. You are observing the current formula: `'` 5 `'` . You can choose
between [ `'` 1 `'`, `'` 2 `'`, `'` 3 `'`, `'` 4 `'`, `'` 5 `'`, `'` 6 `'`, `'` 7 `'`, `'` 8 `'`, `'` 9 `'`, `'` 10 `'`, `'` + `'`, `'` - `'`,
`'` = `'` ]. The number or operator you choose will be appended to the current
formula. Note that `'` J `'`, `'` Q `'`, and `'` K `'` count as `'` 10 `'` . Your goal is to
output a formula that evaluates to 12, and each number can only be used
once. Your response should be a valid json file in the following format:
{
"action": "{number}" or "{operator}"
}


**Responses:**
{
"action": "+"
}"


Figure 27: An example of the supervised fine-tuning data for `Blackjack` without CoT.


27


**D.4** **Points24**


In the `Points24` task, we directly collect 50k instruction-following expert data samples using a task
solver. See examples with and without CoT in Figure 28 and 29, respectively. Note that the supervised
fine-tuning data has a slightly different distribution as the states in the `Points24` environment, since
the expert data always have a viable solution to 24, while not all states from `Points24` has a viable
solution to 24.


**Inputs:**
You are an expert card game player. You are observing two cards in the
image. You are observing the current formula: `'` 5 `'` . You can choose
between [ `'` 1 `'`, `'` 2 `'`, `'` 3 `'`, `'` 4 `'`, `'` 5 `'`, `'` 6 `'`, `'` 7 `'`, `'` 8 `'`, `'` 9 `'`, `'` 10 `'`, `'` + `'`, `'` - `'`,
`'` = `'` ]. The number or operator you choose will be appended to the current
formula. Note that `'` J `'`, `'` Q `'`, and `'` K `'` count as `'` 10 `'` . Your goal is to
output a formula that evaluates to 12, and each number can only be used
once. Your response should be a valid json file in the following format:
{
"cards": [x, y],
"current formula": `'` (2 `'`,
"thoughts": {First check whether the current formula `'` z `'` is complete. If the current formula `'` z `'` is
complete, output `'` = `'` . Otherwise consider which number or operator should be appended to the
current formula to make it equal 12.}
"action": "{number}" or "{operator}"
}


**Responses:**
{
"cards": [1, 2, 10, 1],
"formula": "(2",
"thoughts": " `'` (2 `'` is an incomplete formula, since `'` (2+10)*(1+1)=24 `'`, I should append `'` + `'` to the
current formula",
"action": "+"
}"


Figure 28: An example of the supervised fine-tuning data for `Points24` with CoT.


**Inputs:**
You are an expert card game player. You are observing two cards in the
image. You are observing the current formula: `'` 5 `'` . You can choose
between [ `'` 1 `'`, `'` 2 `'`, `'` 3 `'`, `'` 4 `'`, `'` 5 `'`, `'` 6 `'`, `'` 7 `'`, `'` 8 `'`, `'` 9 `'`, `'` 10 `'`, `'` + `'`, `'` - `'`,
`'` = `'` ]. The number or operator you choose will be appended to the current
formula. Note that `'` J `'`, `'` Q `'`, and `'` K `'` count as `'` 10 `'` . Your goal is to
output a formula that evaluates to 12, and each number can only be used
once. Your response should be a valid json file in the following format:
{
"action": "{number}" or "{operator}"
}


**Responses:**
{
"action": "+"
}"


Figure 29: An example of the supervised fine-tuning data for `Points24` without CoT.


28


**D.5** **ALFWorld**


The data collection procedure of the `alfworld` embodied environment is slightly different than the
`gym_cards`, as we do not have solvers to generate the instruction-following data, even with the expert
text action. Therefore, we take a step back and directly use our prompt as presented in Figure 17 (or
Figure 30) to collect 1k episodes (around 45k) instruction-following data from GPT4-V [44] with the
CoT reasoning for the instruction-following fine-tuning with CoT. As for the case without CoT, we
directly clean the collected CoT by removing the CoT reasonings. See examples with and without
CoT in Figure 30 and 31, respectively.


**Inputs:**
Your are an expert in the ALFRED Embodied Environment. You are
also given the following text description of the current scene: [ `'` You
arrive at loc 0. The cabinet 1 is open. On the cabinet 1, you see a pan
1, a kettle 1, a winebottle 1, a apple 1, a stoveknob 1, a stoveknob 2, a
stoveknob 3, a stoveknob 4, a knife 1, a saltshaker 1, and a bread 1. `'` ].
Your task is to put a cool mug in cabinet. Your admissible actions of the
current situation are: [ `'` go to countertop 1 `'`, `'` go to cabinet 2 `'`, `'` go to
countertop 2 `'`, `'` go to stoveburner 1 `'`, `'` go to drawer 1 `'`, `'` go to drawer
2 `'`, `'` go to drawer 3 `'`, `'` go to stoveburner 2 `'`, `'` go to stoveburner 3 `'`, `'` go
to stoveburner 4 `'`, `'` go to drawer 4 `'`, `'` go to cabinet 3 `'`, `'` go to cabinet 4 `'`, `'` go to microwave 1 `'`, `'` go
to cabinet 5 `'`, `'` go to cabinet 6 `'`, `'` go to cabinet 7 `'`, `'` go to sink 1 `'`, `'` go to sinkbasin 1 `'`, `'` go to fridge
1 `'`, `'` go to toaster 1 `'`, `'` go to coffeemachine 1 `'`, `'` go to cabinet 8 `'`, `'` go to drawer 5 `'`, `'` go to drawer
6 `'`, `'` go to drawer 7 `'`, `'` go to drawer 8 `'`, `'` go to shelf 1 `'`, `'` go to shelf 2 `'`, `'` go to countertop 3 `'`, `'` go
to shelf 3 `'`, `'` go to drawer 9 `'`, `'` go to garbagecan 1 `'`, `'` open cabinet 1 `'`, `'` close cabinet 1 `'`, `'` take pan
1 from cabinet 1 `'`, `'` take kettle 1 from cabinet 1 `'`, `'` take winebottle 1 from cabinet 1 `'`, `'` take apple
1 from cabinet 1 `'`, `'` take stoveknob 1 from cabinet 1 `'`, `'` take stoveknob 2 from cabinet 1 `'`, `'` take
stoveknob 3 from cabinet 1 `'`, `'` take stoveknob 4 from cabinet 1 `'`, `'` take knife 1 from cabinet 1 `'`,
`'` take saltshaker 1 from cabinet 1 `'`, `'` take bread 1 from cabinet 1 `'`, `'` inventory `'`, `'` look `'`, `'` examine
cabinet 1 `'` ]. Your response should be a valid json file in the following format:
{
"thoughts": "first describe what do you see in the image using the text description, then carefully
think about which action to complete the task. ",
"action": "an admissible action"
}


**Responses:**
{
"thoughts": "Based on the text description, I am at loc 0 with an open cabinet 1 in front of me. Items
such as a pan, kettle, wine bottle, apple, several stoveknobs, a knife, saltshaker, and bread are visible
on the cabinet 1. To find a cool mug to put in the cabinet, I may need to first locate a mug, which
might be in one of the cabinets or drawers. Since the task does not involve any items currently in
cabinet 1, and the mug is not mentioned in the description, my best course of action would be to start
by searching the other cabinets or drawers for the mug.",
"action": "go to cabinet 2"
}"


Figure 30: An example of the supervised fine-tuning data for `alfworld` with CoT.


29


**Inputs:**
Your are an expert in the ALFRED Embodied Environment. You are
also given the following text description of the current scene: [ `'` You
arrive at loc 0. The cabinet 1 is open. On the cabinet 1, you see a pan
1, a kettle 1, a winebottle 1, a apple 1, a stoveknob 1, a stoveknob 2, a
stoveknob 3, a stoveknob 4, a knife 1, a saltshaker 1, and a bread 1. `'` ].
Your task is to put a cool mug in cabinet. Your admissible actions of the
current situation are: [ `'` go to countertop 1 `'`, `'` go to cabinet 2 `'`, `'` go to
countertop 2 `'`, `'` go to stoveburner 1 `'`, `'` go to drawer 1 `'`, `'` go to drawer
2 `'`, `'` go to drawer 3 `'`, `'` go to stoveburner 2 `'`, `'` go to stoveburner 3 `'`, `'` go
to stoveburner 4 `'`, `'` go to drawer 4 `'`, `'` go to cabinet 3 `'`, `'` go to cabinet 4 `'`, `'` go to microwave 1 `'`, `'` go
to cabinet 5 `'`, `'` go to cabinet 6 `'`, `'` go to cabinet 7 `'`, `'` go to sink 1 `'`, `'` go to sinkbasin 1 `'`, `'` go to fridge
1 `'`, `'` go to toaster 1 `'`, `'` go to coffeemachine 1 `'`, `'` go to cabinet 8 `'`, `'` go to drawer 5 `'`, `'` go to drawer
6 `'`, `'` go to drawer 7 `'`, `'` go to drawer 8 `'`, `'` go to shelf 1 `'`, `'` go to shelf 2 `'`, `'` go to countertop 3 `'`, `'` go
to shelf 3 `'`, `'` go to drawer 9 `'`, `'` go to garbagecan 1 `'`, `'` open cabinet 1 `'`, `'` close cabinet 1 `'`, `'` take pan
1 from cabinet 1 `'`, `'` take kettle 1 from cabinet 1 `'`, `'` take winebottle 1 from cabinet 1 `'`, `'` take apple
1 from cabinet 1 `'`, `'` take stoveknob 1 from cabinet 1 `'`, `'` take stoveknob 2 from cabinet 1 `'`, `'` take
stoveknob 3 from cabinet 1 `'`, `'` take stoveknob 4 from cabinet 1 `'`, `'` take knife 1 from cabinet 1 `'`,
`'` take saltshaker 1 from cabinet 1 `'`, `'` take bread 1 from cabinet 1 `'`, `'` inventory `'`, `'` look `'`, `'` examine
cabinet 1 `'` ]. Your response should be a valid json file in the following format:
{
"action": "an admissible action"
}


**Responses:**
{
"action": "go to cabinet 2"
}"


Figure 31: An example of the supervised fine-tuning data for `alfworld` without CoT.


30


