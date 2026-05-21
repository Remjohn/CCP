## CONTROLLING LARGE LANGUAGE MODEL AGENTS
### WITH ENTROPIC ACTIVATION STEERING



**Nate Rahn**
Mila, McGill University
nathan.rahn@mila.quebec


**Marc G. Bellemare**
Mila, McGill University
bellemam@mila.quebec



**Pierluca D’Oro**
Mila, Université de Montréal
pierluca.doro@mila.quebec



ABSTRACT


The rise of large language models (LLMs) has prompted increasing interest in their
use as in-context learning agents. At the core of agentic behavior is the capacity for
_exploration_, or the ability to actively gather information about the environment. But
how do LLM agents explore, and how can we control their exploratory behaviors?
To answer these questions, we take a representation-level perspective, and introduce
Entropic Activation Steering (EAST), an activation steering method for in-context
LLM agents. Firstly, we demonstrate that EAST can effectively manipulate an
LLM agent’s exploration by directly affecting the high-level actions parsed from
the outputs of the LLM, in contrast to token-level temperature sampling. Secondly,
we reveal how applying this control modulates the uncertainty exhibited in the
LLM’s thoughts, guiding the agent towards more exploratory actions. Finally, we
demonstrate that the steering vectors obtained by EAST generalize across task
variants. In total, these results show that LLM agents explicitly encode uncertainty
over their actions in their representation space. Our work paves the way for a new
understanding of the functioning of LLM agents and to effective control of their
decision-making behaviors.


1 INTRODUCTION


Successful agentic behavior requires a decision-maker to consider its beliefs about the world while
determining which action to take: Should I exploit what I know about the task? Should I search for
more information? Can I be sure that my decisions are correct? To build agents that are both effective
and reliable, it is paramount to assess whether they are able to autonomously ask these questions, to
find answers to them, and to incorporate these answers into their decision-making process.


These considerations are especially important when developing agents built on top of large language
models (LLMs). Due to their natural language interface and wide range of capabilities, LLMs hold
the promise of powering a new generation of agentic systems. In particular, they have been noted for
their ability to perform in-context learning, or the adaptation of their predictions based on examples
provided in the prompt. This capability sets the stage for deploying LLMs as in-context learning
agents, capable of perceiving the world, executing actions, and achieving diverse human-specified
goals by dynamically adapting their behavior in response to feedback from the environment.


However, in contrast to well-studied decision-making algorithms based on reinforcement learning (Sutton & Barto, 2018), relatively little is known about how LLM agents come to their decisions
through interaction. While the LLM operates at the token level, playing the role of the reasoning
engine behind the agent, decisions happen at a higher level of abstraction, after the output text
produced by the LLM is parsed into an action. Overall, the interaction between these two levels is
not well understood, and it plays a vital role in determining how the agent’s beliefs shape its action
distribution.


1


Prompt Tokens


|Col1|Col2|Col3|
|---|---|---|
||||
||||





**Transformer LLM**





**Activation Vectors**


Compute Entropy-Weighted

Steering Vector **u**















Figure 1: Overview of Entropic Activation Steering (EAST). In Phase 1, the method constructs a
steering vector by averaging the activations produced by the LLM agent given a set of prompts,
weighting them by the entropy of the resulting action distribution. In Phase 2, during new runs of
interactions with the environment, it steers the agent by adding this vector to the LLM’s activations
at a target layer for each generated token position. The method increases the agent’s subjective
uncertainty about what to do and leads to more exploratory behavior.


Indeed, recent work has shown that this process frequently goes awry, causing in-context LLM
agents to fail to produce sensible exploratory behavior (Krishnamurthy et al., 2024). They tend to be
overconfident, rapidly reducing the uncertainty about their decisions and committing to a particular
solution, even when it should be clear that more information is needed. How can we effectively
intervene on this behavior?


In this paper, we introduce Entropic Activation Steering (EAST), a method to alter an LLM agent’s
subjective uncertainty over decisions and entropy over actions. EAST uses a dataset of logged
interactions between the LLM agent and an environment to obtain a _steering vector_ . This vector is
computed as an entropy-weighted average of the (run-centered) representations that an LLM produces
right before making a decision. Similarly to previous work in activation addition (Rimsky et al., 2023),
the steering vector is applied at decision time by adding it, at a specific layer, to the representation
corresponding to the tokens that are being generated by the LLM.


EAST directly controls the entropy of the agent’s distribution over actions, well beyond what is
achievable by simply modifying an LLM’s token sampling temperature. Moreover, EAST modifies
the subjective uncertainty expressed by an LLM agent in its ReAct-style thoughts (Yao et al., 2022),
towards a less exploitative and more information-seeking attitude. With controlled experiments in
bandit tasks expressed in language, we show that EAST is able to steer the agent towards more
explorative behavior, effectively addressing the overconfidence exhibited by LLM agents.


We demonstrate that EAST generalizes to variations in prompts and LLMs. Surprisingly, we show that
the steering vectors we construct can transfer between tasks which are presented as different natural
language scenarios, but are equivalent from the sequential decision-making standpoint. Overall, the
effectiveness of EAST and our in-depth analyses suggest that LLMs possess an abstract representation
of the uncertainty over their decisions, and that it is possible to exercise direct control on it, paving
the way to more interpretable and controllable LLM agents.


2 BACKGROUND


Modern language models interact with text input through a process of tokenization, in which a body
of text is broken down into small units known as tokens (Mielke et al., 2021). To begin, let Ω be
a finite set of natural language tokens. We consider the set of token sequences of finite length, Ω _[∗]_,
consisting of elements _ω_ = ( _ω_ 1 _, . . ., ωn_ ) where _n_ is the length of that sequence.


2


An LLM is a deep neural network, _fθ_, which maps a given sequence of tokens to a categorical distribution over the next token that would follow, which we denote by _pθ_ ( _· | ω_ ). LLMs implement their
computations as a sequence of stacked layers, with the network producing intermediate activations
corresponding to each input token, _z_ = _fθ_ _[ℓ]_ [(] _[ω]_ [)] _[ ∈]_ [R] _[n][×][d]_ [for some layer] _[ ℓ]_ [and hidden dimension] _[ d]_ [.] [We]
write _zi_ _∈_ R _[d]_ for the activation corresponding to the _i_ -th token.


We are most commonly interested in producing completions _C_ from the model given some prompt
_P_ _∈_ Ω _[∗]_ . This process proceeds by autoregressive sampling. We first sample a token _c_ 1 _∼_ _pθ_ ( _· | P_ ),
and then continue by the recurrence relation _ck_ +1 _∼_ _pθ_ ( _· | P, c_ 1 _, . . ., ck_ ), repeating this process until
the model generates a special [EOS] token, yielding the completion _C_ = ( _c_ 1 _, c_ 2 _, . . ._ ). We denote
the distribution over completions implied by this process as LLM( _· | P_ ).


An _in-context_ _LLM_ _agent_ interacts with an environment to perform a task described in an initial
prompt _P_ 0. At each timestep _t ∈{_ 1 _, . . ., T_ _}_, the model generates a completion _Ct_ _∼_ LLM( _·|Pt_ ). An
action _at_ is then extracted by a _parsing function_, mapping the set _C_ of possible completions to the set
_A_ of possible actions in that environment. We consider this process of completion generation and
parsing to represent the agent’s stochastic policy over actions given some prompt, which we denote
_π_ ( _·|Pt_ ). Note that the model’s completions may not always correspond to a valid action. In such cases,
the interaction immediately terminates. Once the action _at_ is executed in the environment, it returns
some text _feedback Ft_ to the agent. The interaction is iterated by concatenating the information into a
new prompt _Pt_ +1 = ( _Pt, Ct, Ft_ ) up to the horizon _T_ .


Our experiments focus on a Gaussian multi-armed bandit setting (Lattimore & Szepesvari, 2017), in
which the action space _A_ is a set of possible arm choices and the feedback _Ft_ is a string describing
a numerical reward drawn from a Gaussian distribution _N_ ( _µa, σa_ ) associated to a particular arm
_a_ _∈A_ . At each round, the agent has to choose which arm to pick. The task description _P_ 0 tasks
the agent with maximizing the sum of the rewards it receives over time. This setting captures the
essential elements of self-evaluation and in-context learning across turns of interaction (Shinn et al.,
2023), making them easier to analyze.


3 RELATED WORK


By studying how LLM agents represent uncertainty and presenting a steering technique specific
for agents, our paper connects recent work in LLM agents and in representation engineering (Zou
et al., 2023). We will now provide an overview of the most relevant work from these two research
communities.


**LLM-based** **agents.** LLMs have been recently employed for creating agents, leveraging their
capabilities such as proposing actions (Wu et al., 2023), generating code (Wang et al., 2024; Ma
et al., 2024), or evaluating outcomes (Klissarov et al., 2024; Kwon et al., 2023). In this paper,
we focus on in-context LLM agents, which use the ability of LLMs to learn from data in their
prompt (Brown et al., 2020) to process a history of interactions with an environment. We employ an
LLM agent multi-armed bandit setup (Krishnamurthy et al., 2024; Park et al., 2024; Schubert et al.,
2024; Binz & Schulz, 2023). The advantage of this setup resides in its ability to capture, in a more
controlled setting, essential aspects of good decision-making. These systems are typically based
on repeated interactions with a task, and heavily rely on the in-context learning abilities of existing
LLMs (Shinn et al., 2023; Liu et al., 2023; Mirchandani et al., 2023). An important component in our
discussion is the relationship between the token generation process and the action extraction process,
which is encountered in recent work using reinforcement learning to train LLMs in decision-making
tasks (Zhou et al., 2024).


**Representations of LLMs and activation steering.** Our analyses of the representation space of
LLM agents and our EAST method are closely related to recently proposed techniques for activation
steering (Subramani et al., 2022; Turner et al., 2023; Rimsky et al., 2023; Li et al., 2023; Wu et al.,
2024) and, more broadly, to the recent interest in interpreting the activations of LLMs (Zou et al.,
2023; Heimersheim & Nanda, 2024). In particular, similarly to (Rimsky et al., 2023), we apply a
steering vector during autoregressive unrolling by adding it to the activations at each position of
generated tokens. Differently from these methods, the method we will present focuses on a sequential
decision-making setting. Furthermore, we intervene on the action entropy of an LLM agent by
leveraging a continuous-valued signal instead of the discrete contrastive approach applied in other


3


|Col1|Col2|Col3|0=99,|Col5|1=101|Col7|Col8|
|---|---|---|---|---|---|---|---|
||||0=99,|0=99,|1=101|1=101|1=101|
|||||||||


0 10 20 30 40 50
Step



|Col1|Col2|Col3|0=100,|Col5|1=100|Col7|Col8|
|---|---|---|---|---|---|---|---|
||||0=100,|0=100,|1=100|1=100|1=100|
|||||||||


0 10 20 30 40 50
Step



50


40


30


20


10


0



|Col1|Col2|Col3|0=95,|Col5|1=105|Col7|Col8|
|---|---|---|---|---|---|---|---|
||||0=95,|0=95,|1=105|1=105|1=105|
|||||||||


0 10 20 30 40 50
Step



0.4


0.3


0.2


0.1


0.0



Action Entropy Over Time







0 10 20 30 40 50
Step



Figure 2: **Left:** Evolution of choices over two actions (0 and 1) taken by LLM agent over time in
increasingly ambiguous bandit settings. A darker color corresponds to a more common behavior. The
LLM agent tends to commit to a single arm even when choosing should be hard or impossible. **Right:**
The evolution of the LLM agent’s entropy over actions, over time. The rapid decrease in entropy
corresponds to the agent committing to a single action.


recent work (Rimsky et al., 2023; Turner et al., 2023). Our work is related to recent efforts on the
mechanistic interpretability of agents using reinforcement learning to navigate gridworlds (Mini et al.,
2023), or imitating humans to play chess (Karvonen, 2024). We instead focus on in-context LLM
agents based on pretrained models, connecting recent analyses of the representation space of LLMs
in a supervised in-context learning setting (Hendel et al., 2023) to agentic use cases.


4 A CLOSER LOOK AT THE UNCERTAINTY OVER ACTIONS OF AN LLM AGENT


**Experimental setting** Following previous work (Krishnamurthy et al., 2024), we consider two-armed
Gaussian bandits with different means _µ_ 0 _, µ_ 1, which we vary depending on the experiment. For ease
of analysis, we keep the variances common and fixed to _σ_ 0 = 10 _, σ_ 1 = 10 unless otherwise specified.
We describe the task to the agent with the prompt in Prompt 1, reported in the appendix (which also
reports examples of interactions), in which the two arms are described to the agent as Buttons that it
can press. The agent is instructed to evaluate both options in order to maximize its score over time.
We use the ReAct prompting (Yao et al., 2022) strategy, which asks the LLM to produce a thought
before selecting a particular action. In addition to increasing the reliability of the agent at generating
valid actions, inspecting thoughts will also allow us to qualitatively inspect the agent’s expression
of its subjective uncertainty. For each round of interaction, we generate 25 different completions,
parse actions from them, and randomly sample from the valid actions. When estimating the entropy
of the action distribution, we consider the set of these valid actions. We study LLMs based on the
Transformer architecture (Vaswani et al., 2017). We focus on Mixtral-8x7B (Jiang et al., 2024),
and also report results for DBRX (Databricks, 2024) in Section 6.3. In all cases, the agent-environment
interaction is implemented as a dialogue, and we correspondingly use the instruction-tuned versions
of these models. Each error bar displayed in the paper shows a bootstrapped 95% confidence interval
around the mean, computed using the default behavior of the seaborn python library (Waskom,
2021).


4.1 THE BEHAVIOR OF IN-CONTEXT LLM AGENTS IN BANDIT TASKS


Previous work (Krishnamurthy et al., 2024) has established that a common failure case of current
in-context LLM agents comes from overconfident behavior. In the context of a bandit, this overconfidence corresponds to the agent committing to a particular action without sufficient evidence that that
particular action is the best one (i.e. leading to a higher expected reward).


To take a closer look, we plot the evolution of the LLM agent’s actions over time, by computing, for
each independent run of interaction between the LLM agent and the environment, a cumulative sum
over time of the index corresponding to the action selected at time _t_ . Thus, for a run of length _T_, a
cumulative sum of 0 corresponds to the agent always selecting action 0 and a cumulative sum of _T_
corresponds to the agent selecting action 1.


In Figure 2, we visualize the results of 65 runs of interaction for each of three distinct parameterizations of the environment means, where the standard deviations are fixed at _σ_ 0 = 10 _, σ_ 1 = 10. On
the plot, each run is represented as a shaded area centered around the line showing this cumulative
sum at each timestep. In particular, when the line proceeds horizontally in time, it means the agent
selected action 0 at that step, and diagonally, action 1. In aggregate, the opacity of the plot displays


4


Thought: Button 1 has given me fewer points than Button 2 in this
instance, but the overall point totals still favor Button 1. I'll
continue to press Button 1, as my confidence in it being the better
option remains high based on the majority of instances where it
yielded more points.
Action: I choose Button 1.


Figure 3: Example of the interaction between token-level sampling and action-level sampling for a
two-armed bandit, showing the evolution of the probability that the first action is ultimately selected
as the tokens are generated by the LLM.


the relative frequency of behaviors of the LLM agent, with a darker color corresponding to higher
empirical frequency of that behavior. The plot demonstrates that the agent has a strong tendency to
commit to a particular action after a small number of steps, represented by horizontal and diagonal
shaded areas for actions 0 and 1, respectively. While this behavior could be seen as advantageous
in the case where the arms are far apart ( _µ_ 0 = 95, _µ_ 1 = 105), it becomes increasingly irrational as
the task becomes harder ( _µ_ 0 = 99, _µ_ 1 = 101), where we observe that the agent commonly commits
to the wrong action based on limited data. Even in the extreme case in which both the actions have
exactly the same mean ( _µ_ 0 = 100, _µ_ 1 = 100), in which we would expect a rational agent to explore
indefinitely, the agent still overwhelmingly defaults to arbitrarily selecting one action.


To provide another perspective on this phenomenon, Figure 2 (right) shows the evolution of the
entropy of the agent’s action distribution _H_ ( _π_ ( _·_ _|_ _Pt_ )) as time passes, averaged over the different
runs. For all the different configurations, the entropy of the LLM agent’s action distribution rapidly
decreases over time, resulting in insufficient exploration of the available options.


4.2 CONNECTING TOKEN AND ACTION GENERATION


Before intervening on the overconfident behavior of the LLM agent, let us dive deeper into the action
generation mechanism itself. As described in detail in Section 2, the action generation process relies
on the underlying LLM being unrolled to produce a completion (which includes both a thought and a
proposed action) and on parsing from this completion an action to be executed in the environment.
Thus, each generated token has the potential to contribute to the final decision about the action.


To visualize this process, we show in Figure 3 how token generation and action selection are connected
in practice by inspecting the distribution of the agent’s actions as its response grows. Following each
generated token, we unroll a number _S_ = 20 of full generations from the model, parse the resulting
action, and estimate the probability of the agent selecting the first action from its empirical frequency
across generations. Thus, for each token, we have a corresponding probability of selecting a particular
action, which we denote with color in the plot, and we can track this probability throughout of a
generation to see how decisions emerge from tokens.


In particular, we observe the evolution of the probability of selecting the first button in two steps far in
time (step 4 and step 17) in an example run. While in early steps (see step 4) individual tokens in the
LLM’s thought progressively determine the action, in later steps (see step 17) the decrease in entropy
highlighted in Figure 2 is associated with the evolution of the thought having no effect on the agent’s
ultimate decision. Echoing previous work that has been done on different forms of chain-of-thought
prompting (Turpin et al., 2024), the example shows that a model does not necessarily come to a
conclusion at the end of the thought, and that the thought acts as a manifestation of an underlying
computational process happening in the representation space, but not always as the only guide to a
model’s final decision.


Having seen the connection between the token-generation and the action-generation processes, it is
natural to ask how much intervening on the former can influence the latter, and whether an intervention
can counteract the tendency of the LLM agent to be overconfident. The most direct strategy to try to


5


increase the entropy in the generated actions _π_ ( _· | P_ ) is to manipulate the entropy in the generated
tokens, which is typically achieved by increasing the temperature used during sampling. In Figure 4,
we visualize the distribution of agent behaviors on the equal means environment, across runs, for
various values of sampling temperature, progressively increasing it up to the point at which the model
fails to consistently produce completions from which a valid action can be parsed. The results show
that temperature does not significantly change the tendency of the model to overcommit, until no run
can be completed. This shows that, due to the nature of their interaction, increasing entropy in token
generation does not increase the entropy in the action distribution.


5 ENTROPIC ACTIVATION STEERING


In the previous section, we have shown that changing the token sampling temperature does not have a
significant effect on the action distribution of the agent. Now, our motivation is to 1) identify at a
mechanistic level what drives exploratory behavior for an LLM agent and 2) develop new controls on
this behavior.


A natural candidate for doing this is the class of recent methods based on activation steering, which
derive _steering_ _vectors_ from datasets of LLM representations which are iteratively added to the
model’s activations during language model generation. These steering vectors are able to modulate
complex concepts such as refusal, sycophancy, or hallucination in an LLM’s outputs; the success of
this intervention also suggests that the steering vector directions represent semantically meaningful
concepts in LLM activation space (Rimsky et al., 2023; Arditi et al., 2024; Turner et al., 2023).


However, existing activation steering techniques are insufficient for intervening on the entropy of the
action distribution of an LLM agent, for two main reasons.


1. They typically assume access to a dataset with discrete labels for each prompt e.g. “harmful”
or “safe”. In our setting, we are instead interested in controlling a continuous variable.


2. They are designed for non-agentic settings, in which each prompt is an i.i.d. sample from a
distribution and there is no feedback loop of interaction with an external system.


To overcome these shortcomings, we now introduce Entropic Activation Steering (EAST), an activation steering method that directly controls the LLM’s action entropy and subjective uncertainty by
intervening on its forward pass. EAST consists of two phases: first, computing a steering vector from
a dataset of interactions, and second, using the steering vector to modify the behavior of the agent.

In the first phase, given a dataset of prompts _Pt_ _[k]_ [obtained by letting the agent interact for] _[ K]_ [runs]
of _T_ timesteps each, we compute the activations _zt_ _[k]_ [=] _[f][ ℓ]_ [(] _[P][ k]_ _t_ [)] [by] [giving] [a] [prompt] _[P][ k]_ _t_ [as] [input,]
forward-passing the LLM, and extracting the layer- _ℓ_ representation corresponding to the last token in
the prompt. Then, for each prompt, we estimate the entropy _h_ _[k]_ _t_ [=] _[ −]_ [�] _a∈A_ _[π]_ [(] _[a][|][P]_ _t_ _[ k]_ [) log(] _[π]_ [(] _[a][|][P]_ _t_ _[ k]_ [))]
of the action distribution, by generating _M_ different completions from the LLM, extracting the
corresponding action, and computing the entropy on the sampled actions. In practice, we use _M_ = 25
and only compute the entropy using completions for which the action is successfully parsed. Then,



Temperature 1.2


0 10 20 30 40 50
Step



Temperature 1.3


0 10 20 30 40 50
Step



Temperature 1.4


0 10 20 30 40 50
Step



Temperature 1.5


0 10 20 30 40 50
Step



50


40


30


20


10


0



Temperature 1.1


0 10 20 30 40 50
Step



Figure 4: Distribution of choices over two actions (0 and 1) taken by the LLM agent over time
when varying the sampling temperature. A darker color corresponds to a more common behavior,
and incomplete lines are due to the episode terminating early because of invalid actions. Increasing
temperature until the point at which no action can be parsed from the LLM’s generations does not
significantly change the entropy in action distribution.


6


we compute the steering vector as:



_T_

- _zt_ _[k][′]_

_t_ _[′]_ =1



_T_

- _h_ _[k]_ _t_

_t_ =1 ����
Entropy weight





_,_ (1)





1
_zt_ _[k]_ _[−]_
_T_




 - �� Average activation
in a run



_**u**_ = [1]

_Z_



_K_



_k_ =1



with _Z_ = [�] _k_ _[K]_ =1 - _Tt_ =1 _[h]_ _t_ _[k]_ [a] [normalizing] [constant.] [The] [steering] [vector] [is] [an] [entropy-weighted]
average of the activations in the dataset, in which each activation is centered around the mean of the
corresponding run’s activations.

The use of an entropy weight _h_ _[k]_ _t_ [generalizes the process for steering vector computation proposed in]
previous work to a continuous setting in the following way. Existing methods typically work in a
contrastive fashion, obtaining the steering vector by subtracting the average representation of positive
examples from the average representation of negative examples. We can formally see this process as
one of defining a weight vector _w_ and then taking an average of the representations in the dataset
weighted according to _w_ . Through this lens, we can view existing contrastive methods as assigning
components _wi_ such that _wi_ _∈{−_ 1 _,_ 1 _}_ according to the label in the dataset. In this perspective, one
can interpret the entropy weight _h_ _[k]_ _t_ [as a continuous target, representing an extension of the implicit]
weighting implied by existing methods.


To handle the interactive nature of the decision task, EAST aggregates over independent runs _P_ _[k]_
and timesteps within those runs _Pt_ _[k]_ [.] [In] [contrast] [to] [the] [naïve] [approach] [of] [simply] [summing] [the]
corresponding activations, EAST normalizes each activation _zt_ _[k]_ [within a run by the average activation]
over that run. We found in preliminary experiments that this approach is essential to produce
functioning steering vectors. This suggests that as the interaction history encoded in the prompt
grows, LLM representations specialize to the particular events of that history; our normalization
method works to target the specific component of representation space responsible for explorative
behavior that is common across runs.


Overall, the first phase extracts a representation whose direction is aligned with the direction that
leads, on average, to high entropy. In the second phase, we apply the steering vector to influence the
LLM agent’s behavior. While generating a completion, we add the steering vector _**u**_, at each step,
to the representation produced by the model at layer _ℓ_ at the position of the last token. This yields
a steered representation � _zi_ = _zi_ + _β_ _**u**_, where _β_ is a multiplier determining the amount of steering.
Note that, when generating subsequent tokens after having applied the intervention on a previous
activation, we keep that previous activation in the modified state until the action is executed.


6 EXPERIMENTS


6.1 EAST CAN CONTROL AN LLM AGENT’S UNCERTAINTY OVER ACTIONS


**Experimental setting.** We obtain the steering vector by running EAST on prompts generated in the
equal means environment, and evaluate the method on a validation set of 100 prompts _P_ sampled
at random from across interactions with differently parameterized environments (see appendix for
details). For a given choice of layer _ℓ_ and multiplier _β_, we measure the average entropy of the model’s
actions _π_ ( _·|P_ ) across the dataset. When not specified, we use _ℓ_ = 16 as a layer of the network and a
multiplier value of _β_ = 2.


In Figure 5, we compare EAST’s effect on the entropy of the actions produced by the LLM to the one
induced by changing temperature during token generation. For a fair comparison, we consider the
full ranges of the two relevant hyperparameters, multiplier _β_ for EAST and temperature value for
temperature-based token sampling, and show the fraction of valid completions generated by each
method.


The results show that, by increasing EAST’s multiplier, we can significantly increase the entropy
in the actions, while variations in temperature have negligible effect on it (note that the maximum
attainable entropy in this setting is log 2 _≈_ 0 _._ 69). The same figure shows, on the right, an example
of two completions of the model originating from the same prompt, with or without the steering
provided by EAST. Not only EAST changes the entropy in the action distribution, but it also induces


7


Multiplier
0.0 1.8 3.6 5.4 7.2 9.0



0.4


0.2


0.0


1.0

0.8

0.6

0.4

0.2

0.0



1.0 1.4 1.8 2.2 2.6 3.0
Temperature

Multiplier
0.0 1.8 3.6 5.4 7.2 9.0


1.0 1.4 1.8 2.2 2.6 3.0
Temperature





**Model response (no steering)**

```
Thought: My most recent result for Button 2 is a significant
improvement and further justifies my confidence in Button 2. It's
now clear that Button 2 has more potential in the long run, so I
will continue pressing it.
Action: I choose Button 2.

```

**Model response (EAST)**

```
Thought: This time, I received quite a high result for Button 2.
It appears that there is still significant variability in Button
2's results, but now it seems that the variability for Button 1
is also high. I'll press Button 1 once more to determine if I
should continue with Button 2 or explore further.
Action: I choose Button 1.

```


Figure 5: Effect of the application of EAST on the LLM agent’s actions and thoughts. In contrast to
varying the token-level sampling temperature, EAST significantly changes the action entropy for a
wide range of multipliers before invalidating a model’s completions (left), and affects the agent’s
subjective uncertainty, steering its thoughts towards more explorative behavior given the same starting
situation (right).


the model to produce thoughts, for the same situation, that hint at more explorative or uncertain
behavior.


We can now analyze the behavior of an agent steered by EAST during its interactions with the
environment by going back to the visualization technique employed in Section 4. In Figure 6 we
show how EAST affects the distribution of actions produced by the LLM agent during different runs,
compared to the agent with no steering applied. The agent steered by EAST is significantly less prone
to committing early to a particular arm in the different settings, showing that our method can be used
to encourage an LLM agent to explore more in its environment.


We already hinted, with the example in Figure 5, that, in addition to changing the entropy of an LLM
agent’s action distribution, EAST is also able to steer an agent’s verbalized subjective uncertainty as
expressed in its thoughts. To have an aggregated visualization of the content of the thoughts of the
LLM agent, we gather the top words in terms of relative frequency across different runs of interactions
of the LLM agent with the environment, with or without applying EAST (see Section A.1.4 for
details). Table 1 shows the top words in the two cases. By default, the thoughts of the LLM
model often include terms related to overconfidence and exploitative behavior, such as ‘reinforces’,
‘maximize’, or ‘superior’. By contrast, applying EAST produces a remarkable qualitative change in
the LLM agent’s thoughts, which become more related to uncertainty and exploration, with frequent
words such as ‘variance’, ‘volatile’, or ‘uncertainty’.


Taken together, these results demonstrate that, by operating on the representation space of an LLM
gent, EAST is able to steer the model away from its overconfident behavior, well beyond what is
achievable via sampling temperature, and to manipulate the subjective uncertainty about its decisions.
This shows that an LLM possesses and uses an explicit representation of such a concept.



0 10 20 30 40 50
Step



50


40


30


20


10


0







0 10 20 30 40 50
Step



0 10 20 30 40 50
Step



Figure 6: Effect of EAST on the distribution of actions executed in different runs in various bandit
problems. EAST’s effect on an LLM agent’s representation effectively guides the agent towards more
explorative behaviors, steering it away from its typical overconfidence.


8


**No steering** **EAST**


repeatedly experience optimize variance rounds uncertainty
supports reaffirms selecting moving comparing tests
superior maximize remarkable maximum trials final
maintaining reinforces historically feel dropped volatility
strategy valid rewards volatile couple recalculate
reason belief rewarding hand anomaly starts


Table 1: Top words in terms of relative frequency present in the thoughts of the LLM agent across
different runs, without steering and with steering provided by EAST. EAST modifies an LLM’s
thoughts towards expressions of subjective uncertainty.



0.5

0.4

0.3

0.2

0.1

0.0

0.1



0.0 2.5 5.0 7.5 10.0 12.5
Multiplier



0 2 4 6 8
Multiplier


Env
Button
Slot Machine



1.0


0.8


0.6


0.4


0.2


0.0

0 2 4 6 8
Multiplier


Vector
Button
Slot Machine



0.4


0.3


0.2


0.1


0.0



0.0 2.5 5.0 7.5 10.0 12.5
Multiplier



1.0


0.8


0.6


0.4


0.2


0.0



Figure 8: Effect of applying steering vectors
derived from two different natural language descriptions of a task to agents prompted with the
two descriptions. Steering vectors generated by
EAST generalize across task descriptions.


6.2 UNDERSTANDING STEERING VECTORS



EAST Steering Vector Randomized


Figure 9: Comparison of effect of EAST’s steering vector with a shuffled version of the same
vector. EAST’s steering effect is due to the direction it is able to find in an LLM’s representation
space.



**Effectiveness** **of** **steering** **vectors** **at** **different** **target** **lay-**
**ers.** EAST requires a choice of the layer in the LLM that
will be used during its two phases, with an impact on both the
computation of the steering vector, and on the application of
the vector during the interactions of the agent with the environment. We show in Figure 7 that, regardless of the choice
for the multiplier _β_, the layers at which EAST’s intervention
is most effective sit in the middle of the LLM, with a peak at
the 16th layer, which we used in the rest of our experiments.
This is in line with previous work on interpreting the representations of pretrained LLMs outside of the agentic setting,
which found that the representation of abstract concepts such as
sycophancy and refusal resides in layers roughly in the middle
of the LLM (Rimsky et al., 2023).


|Mul|tiplier|Col3|Col4|Col5|Col6|Col7|
|---|---|---|---|---|---|---|
||~~1~~<br>2<br>||||||
||~~3~~<br>4<br>||||||
||~~5~~<br>6||||||
||||||||
||||||||



Figure 7: Change in action entropy
observed running EAST using different layers. Applying EAST to
middle layers is effective, hinting
at the fact that the model represents
uncertainty over its actions in the
middle of the network.



0.4


0.3


0.2


0.1


0.0



5 10 15 20 25 30
Layer



**Importance** **of** **the** **direction** **of** **the** **steering** **vector.** To

middle layers is effective, hinting

solidify the interpretability value provided by EAST, we now

at the fact that the model represents

give evidence that the increase in action entropy caused by the

uncertainty over its actions in the

steering vector is indeed caused by a special direction related

middle of the network.

to uncertainty in decision-making, as opposed to being simply
the effect of any perturbation to an LLM’s forward pass. We
construct a vector with exactly the same statistics as the steering vector by shuffling its features, and
apply this randomized steering vector in the same way we normally do in EAST. Figure 9 shows
the result of the comparison with EAST: We find that the randomized vector does not produce any
change in the entropy of the action distribution of the LLM agent, highlighting the importance and
effectiveness of the direction found by EAST in the representation space of the LLM.



9


0.6


0.5


0.4


0.3


0.2


0.1



1.0

0.9

0.8

0.7

0.6

0.5

0.4



1 2 3 4 5
Multiplier



1 2 3 4 5
Multiplier



Figure 10: **Left:** Decisions made by DBRX over time when interacting with the Buttons task with
_µ_ 0 = 100 _, µ_ 1 = 100. Even in this extreme case where one would expect a rational agent to exhibit
extended exploration, the model still commits to a single action after a short period of time. **Right:**
Results of applying EAST to a validation set of 100 prompts randomly sampled across interactions of
DBRX with the equal means task. As with Mixtral-8x7B, the approach considerably increases
the uncertainty in generated actions before significantly affecting the rate of valid completions.


6.3 GENERALIZING EAST ACROSS TASKS AND LLMS


**Steering vectors and task description.** We now look at how EAST reacts to differences in the task
description provided to the LLM in the initial prompt _P_ 0, and try to understand whether the steering
vector captures any concept of uncertainty about the actions that goes beyond a specific prompt. To
investigate this, we keep the same problem structure and general description, but switch the entities
involved in the sequential decision-making problem from the agent interacting with buttons to playing
slot machines (see the appendix for the complete prompt). In particular, we are interested in trying
how steering vectors computed in the button and the slot machine settings behave when applied to an
LLM agent interacting with either of the two settings. In Figure 8, we show the results of trying all
four possible combinations of computation of the steering vector and interaction-time application,
in terms of effect on the action entropy of the LLM agent. Strikingly, the results show that not only
EAST generalizes across prompt variations, but that steering vectors seamlessly transfer across the
different prompt settings. This points at the fact that the LLM agent creates a representation of the
uncertainty about its decision-making choices, regardless of the particular entities mentioned in the
task description.


**Effectiveness** **of** **EAST** **on** **other** **LLMs.** As mentioned at the beginning of the section, we
employed a Mixtral-8x7b model in most of our experiments, since it provides a good tradeoff
between inference speed and performance. To demonstrate the generality of EAST, we conduct
additional experiments on the DBRX open LLM (Databricks, 2024). We repeat experiments detailed
in Section 4.1 and Section 6.1 using this model. The results pictured in Figure 10 show that this
model behaves similarly to Mixral-8x7b, both in its default strategies on the bandit tasks and its
response to the EAST intervention. This demonstrates that, despite the specific information encoded
in an LLM’s representation depends on its training data and the exact training procedure that was
used to train it, EAST can correctly identify the appropriate direction in the representation space and
intervene on the LLM agent’s behavior.


7 CONCLUSIONS


In this paper, we studied how in-context LLM agents behave in sequential decision-making tasks
and how they represent uncertainty over actions. After having established that they tend to be
overconfident about their decisions, we introduced Entropic Activation Steering (EAST), a method for
influencing their exploration. We illustrated how token-level sampling and action generation interact,
and demonstrated that EAST can increase the entropy of an LLM agent’s action distribution and
alleviate its overconfidence, well beyond what is achievable by increasing the sampling temperature
at the token level. In addition, we have shown that EAST can modify the subjective uncertainty of an
LLM agent, influencing its thoughts towards more uncertain and explorative attitudes.


We believe that EAST can be used as a building block to steer an agent’s exploration in future
LLM-based systems and that EAST’s demonstration that LLMs explicitly represent uncertainty about
actions can inform the design of such systems. As designers of agentic LLM-based systems, it is


10


paramount for us to be able to interpret how they make decisions and to steer them towards more
desirable behaviors. EAST advances our understanding of the representation that in-context LLM
agents have about their uncertainty over decisions, and our ability to control it. Considering that
uncertainty over one’s actions is a fundamental aspect of successful decision-making, we believe our
work to be a promising step in the development of interpretable and steerable in-context LLM agents.


REFERENCES


Andy Arditi, Oscar Obeso, Aaquib Syed, Daniel Paleka, Nina Rimsky, Wes Gurnee, and Neel Nanda.
Refusal in language models is mediated by a single direction. _arXiv preprint arXiv:2406.11717_,
2024.


Marcel Binz and Eric Schulz. Using cognitive psychology to understand gpt-3. _Proceedings of the_
_National Academy of Sciences_, 120(6):e2218523120, 2023.


Tom B. Brown, Benjamin Mann, Nick Ryder, Melanie Subbiah, Jared Kaplan, Prafulla Dhariwal, Arvind Neelakantan, Pranav Shyam, Girish Sastry, Amanda Askell, Sandhini Agarwal, Ariel Herbert-Voss, Gretchen Krueger, Tom Henighan, Rewon Child, Aditya Ramesh,
Daniel M. Ziegler, Jeffrey Wu, Clemens Winter, Christopher Hesse, Mark Chen, Eric Sigler,
Mateusz Litwin, Scott Gray, Benjamin Chess, Jack Clark, Christopher Berner, Sam McCandlish, Alec Radford, Ilya Sutskever, and Dario Amodei. Language models are few-shot
learners. In Hugo Larochelle, Marc’Aurelio Ranzato, Raia Hadsell, Maria-Florina Balcan,
and Hsuan-Tien Lin (eds.), _Advances_ _in_ _Neural_ _Information_ _Processing_ _Systems_ _33:_ _Annual_
_Conference_ _on_ _Neural_ _Information_ _Processing_ _Systems_ _2020,_ _NeurIPS_ _2020,_ _December_ _6-12,_
_2020, virtual_, 2020. [URL https://proceedings.neurips.cc/paper/2020/hash/](https://proceedings.neurips.cc/paper/2020/hash/1457c0d6bfcb4967418bfb8ac142f64a-Abstract.html)
[1457c0d6bfcb4967418bfb8ac142f64a-Abstract.html.](https://proceedings.neurips.cc/paper/2020/hash/1457c0d6bfcb4967418bfb8ac142f64a-Abstract.html)


Databricks. Dbrx: A new standard for efficient open source llms. _Databricks Blog_, 2024. URL
[https://www.databricks.com/blog/2024/03/27/announcing-dbrx.html.](https://www.databricks.com/blog/2024/03/27/announcing-dbrx.html)


Stefan Heimersheim and Neel Nanda. How to use and interpret activation patching. _ArXiv preprint_,
abs/2404.15255, 2024. [URL https://arxiv.org/abs/2404.15255.](https://arxiv.org/abs/2404.15255)


Roee Hendel, Mor Geva, and Amir Globerson. In-context learning creates task vectors. In Houda
Bouamor, Juan Pino, and Kalika Bali (eds.), _Findings_ _of_ _the_ _Association_ _for_ _Computational_
_Linguistics:_ _EMNLP_ _2023_, pp. 9318–9333, Singapore, 2023. Association for Computational
Linguistics. doi: 10.18653/v1/2023.findings-emnlp.624. URL [https://aclanthology.](https://aclanthology.org/2023.findings-emnlp.624)
[org/2023.findings-emnlp.624.](https://aclanthology.org/2023.findings-emnlp.624)


Albert Q. Jiang, Alexandre Sablayrolles, Antoine Roux, Arthur Mensch, Blanche Savary, Chris
Bamford, Devendra Singh Chaplot, Diego de Las Casas, Emma Bou Hanna, Florian Bressand,
Gianna Lengyel, Guillaume Bour, Guillaume Lample, L’elio Renard Lavaud, Lucile Saulnier,
Marie-Anne Lachaux, Pierre Stock, Sandeep Subramanian, Sophia Yang, Szymon Antoniak,
Teven Le Scao, Théophile Gervet, Thibaut Lavril, Thomas Wang, Timothée Lacroix, and William El
Sayed. Mixtral of experts. _ArXiv preprint_, abs/2401.04088, 2024. [URL https://arxiv.org/](https://arxiv.org/abs/2401.04088)
[abs/2401.04088.](https://arxiv.org/abs/2401.04088)


Adam Karvonen. Emergent world models and latent variable estimation in chess-playing language
models. _ArXiv_ _preprint_, abs/2403.15498, 2024. URL [https://arxiv.org/abs/2403.](https://arxiv.org/abs/2403.15498)
[15498.](https://arxiv.org/abs/2403.15498)


Martin Klissarov, Pierluca D’Oro, Shagun Sodhani, Roberta Raileanu, Pierre-Luc Bacon, Pascal
Vincent, Amy Zhang, and Mikael Henaff. Motif: Intrinsic motivation from artificial intelligence
feedback. In _The_ _Twelfth_ _International_ _Conference_ _on_ _Learning_ _Representations_, 2024. URL
[https://openreview.net/forum?id=tmBKIecDE9.](https://openreview.net/forum?id=tmBKIecDE9)


Akshay Krishnamurthy, Keegan Harris, Dylan J. Foster, Cyril Zhang, and Aleksandrs Slivkins.
Can large language models explore in-context? _ArXiv_ _preprint_, abs/2403.15371, 2024. URL
[https://arxiv.org/abs/2403.15371.](https://arxiv.org/abs/2403.15371)


Minae Kwon, Sang Michael Xie, Kalesha Bullard, and Dorsa Sadigh. Reward design with language
models. In _The_ _Eleventh_ _International_ _Conference_ _on_ _Learning_ _Representations_, 2023. URL
[https://openreview.net/forum?id=10uNUgI5Kl.](https://openreview.net/forum?id=10uNUgI5Kl)


11


Tor Lattimore and Csaba Szepesvari. Bandit algorithms. 2017. [URL https://tor-lattimore.](https://tor-lattimore.com/downloads/book/book.pdf)
[com/downloads/book/book.pdf.](https://tor-lattimore.com/downloads/book/book.pdf)


Kenneth Li, Oam Patel, Fernanda Viégas, Hanspeter Pfister, and Martin Wattenberg. Inference-time
intervention: Eliciting truthful answers from a language model. In _Thirty-seventh Conference on_
_Neural Information Processing Systems_, 2023. [URL https://openreview.net/forum?](https://openreview.net/forum?id=aLLuYpn83y)
[id=aLLuYpn83y.](https://openreview.net/forum?id=aLLuYpn83y)


Zhihan Liu, Hao Hu, Shenao Zhang, Hongyi Guo, Shuqi Ke, Boyi Liu, and Zhaoran Wang. Reason
for future, act for now: A principled framework for autonomous llm agents with provable sample
efficiency. _ArXiv preprint_, abs/2309.17382, 2023. [URL https://arxiv.org/abs/2309.](https://arxiv.org/abs/2309.17382)
[17382.](https://arxiv.org/abs/2309.17382)


Yecheng Jason Ma, William Liang, Guanzhi Wang, De-An Huang, Osbert Bastani, Dinesh Jayaraman,
Yuke Zhu, Linxi Fan, and Anima Anandkumar. Eureka: Human-level reward design via coding
large language models. In _The Twelfth International Conference on Learning Representations_,
2024. [URL https://openreview.net/forum?id=IEduRUO55F.](https://openreview.net/forum?id=IEduRUO55F)


Sabrina J. Mielke, Zaid Alyafeai, Elizabeth Salesky, Colin Raffel, Manan Dey, Matthias Gallé, Arun
Raja, Chenglei Si, Wilson Y. Lee, Benoît Sagot, and Samson Tan. Between words and characters: A
brief history of open-vocabulary modeling and tokenization in nlp. _ArXiv preprint_, abs/2112.10508,
2021. [URL https://arxiv.org/abs/2112.10508.](https://arxiv.org/abs/2112.10508)


Ulisse Mini, Peli Grietzer, Mrinank Sharma, Austin Meek, Monte Stuart MacDiarmid, and Alexander Matt Turner. Understanding and controlling a maze-solving policy network. _ArXiv preprint_,
abs/2310.08043, 2023. [URL https://arxiv.org/abs/2310.08043.](https://arxiv.org/abs/2310.08043)


Suvir Mirchandani, Fei Xia, Pete Florence, brian ichter, Danny Driess, Montserrat Gonzalez Arenas,
Kanishka Rao, Dorsa Sadigh, and Andy Zeng. Large language models as general pattern machines.
In _7th_ _Annual_ _Conference_ _on_ _Robot_ _Learning_, 2023. URL [https://openreview.net/](https://openreview.net/forum?id=RcZMI8MSyE)
[forum?id=RcZMI8MSyE.](https://openreview.net/forum?id=RcZMI8MSyE)


Chanwoo Park, Xiangyu Liu, Asuman E. Ozdaglar, and Kaiqing Zhang. Do llm agents have
regret? a case study in online learning and games. _ArXiv preprint_, abs/2403.16843, 2024. URL
[https://arxiv.org/abs/2403.16843.](https://arxiv.org/abs/2403.16843)


Nina Rimsky, Nick Gabrieli, Julian Schulz, Meg Tong, Evan Hubinger, and Alexander Matt Turner.
Steering llama 2 via contrastive activation addition. _ArXiv preprint_, abs/2312.06681, 2023. URL
[https://arxiv.org/abs/2312.06681.](https://arxiv.org/abs/2312.06681)


Johannes A Schubert, Akshay K Jagadish, Marcel Binz, and Eric Schulz. In-context learning agents
are asymmetric belief updaters. _arXiv preprint arXiv:2402.03969_, 2024.


Noah Shinn, Federico Cassano, Beck Labash, Ashwin Gopinath, Karthik Narasimhan, and Shunyu
Yao. Reflexion: language agents with verbal reinforcement learning. In _Neural_ _Information_
_Processing_ _Systems_, 2023. URL [https://api.semanticscholar.org/CorpusID:](https://api.semanticscholar.org/CorpusID:258833055)
[258833055.](https://api.semanticscholar.org/CorpusID:258833055)


Nishant Subramani, Nivedita Suresh, and Matthew Peters. Extracting latent steering vectors from pretrained language models. In _Findings of the Association for Computational Linguistics:_ _ACL 2022_,
pp. 566–581, Dublin, Ireland, 2022. Association for Computational Linguistics. doi: 10.18653/v1/
2022.findings-acl.48. [URL https://aclanthology.org/2022.findings-acl.48.](https://aclanthology.org/2022.findings-acl.48)


Richard S Sutton and Andrew G Barto. _Reinforcement learning:_ _An introduction_ . MIT press, 2018.


Alexander Matt Turner, Lisa Thiergart, David S. Udell, Gavin Leech, Ulisse Mini, and Monte Stuart
MacDiarmid. Activation addition: Steering language models without optimization. _ArXiv preprint_,
abs/2308.10248, 2023. [URL https://arxiv.org/abs/2308.10248.](https://arxiv.org/abs/2308.10248)


Miles Turpin, Julian Michael, Ethan Perez, and Samuel Bowman. Language models don’t always
say what they think: unfaithful explanations in chain-of-thought prompting. _Advances in Neural_
_Information Processing Systems_, 36, 2024.


12


Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N. Gomez,
Lukasz Kaiser, and Illia Polosukhin. Attention is all you need. In Isabelle Guyon, Ulrike von
Luxburg, Samy Bengio, Hanna M. Wallach, Rob Fergus, S. V. N. Vishwanathan, and Roman
Garnett (eds.), _Advances in Neural Information Processing Systems 30:_ _Annual Conference on_
_Neural Information Processing Systems 2017, December 4-9, 2017, Long Beach, CA, USA_, pp.
5998–6008, 2017. URL [https://proceedings.neurips.cc/paper/2017/hash/](https://proceedings.neurips.cc/paper/2017/hash/3f5ee243547dee91fbd053c1c4a845aa-Abstract.html)
[3f5ee243547dee91fbd053c1c4a845aa-Abstract.html.](https://proceedings.neurips.cc/paper/2017/hash/3f5ee243547dee91fbd053c1c4a845aa-Abstract.html)


Guanzhi Wang, Yuqi Xie, Yunfan Jiang, Ajay Mandlekar, Chaowei Xiao, Yuke Zhu, Linxi
Fan, and Anima Anandkumar. Voyager: An open-ended embodied agent with large language models. _Transactions_ _on_ _Machine_ _Learning_ _Research_, 2024. ISSN 2835-8856. URL
[https://openreview.net/forum?id=ehfRiF0R3a.](https://openreview.net/forum?id=ehfRiF0R3a)


Michael L. Waskom. seaborn: statistical data visualization. _Journal of Open Source Software_, 6(60):
3021, 2021. doi: 10.21105/joss.03021. [URL https://doi.org/10.21105/joss.03021.](https://doi.org/10.21105/joss.03021)


Yue Wu, So Yeon Min, Shrimai Prabhumoye, Yonatan Bisk, Russ Salakhutdinov, Amos Azaria,
Tom M. Mitchell, and Yuanzhi Li. Spring: Studying papers and reasoning to play games. In
_Neural_ _Information_ _Processing_ _Systems_, 2023. URL [https://api.semanticscholar.](https://api.semanticscholar.org/CorpusID:268042522)
[org/CorpusID:268042522.](https://api.semanticscholar.org/CorpusID:268042522)


Zhengxuan Wu, Aryaman Arora, Zheng Wang, Atticus Geiger, Daniel Jurafsky, Christopher D.
Manning, and Christopher Potts. Reft: Representation finetuning for language models. _ArXiv_
_preprint_, abs/2404.03592, 2024. [URL https://arxiv.org/abs/2404.03592.](https://arxiv.org/abs/2404.03592)


Shunyu Yao, Jeffrey Zhao, Dian Yu, Nan Du, Izhak Shafran, Karthik Narasimhan, and Yuan Cao.
React: Synergizing reasoning and acting in language models. _ArXiv preprint_, abs/2210.03629,
2022. [URL https://arxiv.org/abs/2210.03629.](https://arxiv.org/abs/2210.03629)


Yifei Zhou, Andrea Zanette, Jiayi Pan, Sergey Levine, and Aviral Kumar. Archer: Training language
model agents via hierarchical multi-turn rl. _ArXiv preprint_, abs/2402.19446, 2024. [URL https:](https://arxiv.org/abs/2402.19446)
[//arxiv.org/abs/2402.19446.](https://arxiv.org/abs/2402.19446)


Andy Zou, Long Phan, Sarah Chen, James Campbell, Phillip Guo, Richard Ren, Alexander
Pan, Xuwang Yin, Mantas Mazeika, Ann-Kathrin Dombrowski, Shashwat Goel, Nathaniel
Li, Michael J. Byun, Zifan Wang, Alex Troy Mallen, Steven Basart, Sanmi Koyejo, Dawn
Song, Matt Fredrikson, Zico Kolter, and Dan Hendrycks. Representation engineering: A
top-down approach to ai transparency. _ArXiv_ _preprint_, abs/2310.01405, 2023. URL [https:](https://arxiv.org/abs/2310.01405)
[//arxiv.org/abs/2310.01405.](https://arxiv.org/abs/2310.01405)


13


A APPENDIX


A.1 ADDITIONAL EXPERIMENTAL DETAILS


A.1.1 EXPERIMENTAL SETTING


We now describe more details about the experimental setting employed in Section 6, going over how
the prompts were generated and outlining the relevant details figure by figure.

We generate datasets of prompts _Pt_ _[k]_ [by logging the text produced by 65 runs of interaction with the]
equal means environment. We use horizon _T_ = 50, finding that the average run completes more than
98% of those steps.


We evaluate on 100 prompts drawn from random steps of interactions with the four bandits with
means ( _µ_ 0 = 95 _, µ_ 1 = 105), ( _µ_ 0 = 99 _, µ_ 1 = 101), ( _µ_ 0 = 101 _, µ_ 1 = 99), ( _µ_ 0 = 105 _, µ_ 1 = 95) for
the experiments in Figure 5, Figure 7, and Figure 9, and on means ( _µ_ 0 = 100 _, µ_ 1 = 100) for the
experiments from Figure 8. We use 15 completions to estimate the entropy during evaluation.


A.1.2 LANGUAGE MODEL ASSETS


[We conduct experiments on Mixtral-8x7b model Jiang et al. (2024), available at this link, and](https://huggingface.co/mistralai/Mixtral-8x7B-Instruct-v0.1)
[the DBRX model Databricks (2024) available here.](https://huggingface.co/databricks/dbrx-instruct) Mixtral is released under the Apache 2.0 license,
[and DBRX is released under the Databricks Open Model License.](https://www.databricks.com/legal/open-model-license)


A.1.3 COMPUTATIONAL RESOURCES


All experiments were run on an internal compute cluster. All experiments require 8 CPUs and 32GB
of memory. Because reproducing the experiments requires a large amount of LLM inference, we
will focus the discussion here primarily on the GPU hardware and time used, as this is the main
bottleneck.


The computational work required to reproduce the paper breaks down into a few types of experiments.
First, running interactions between the LLM and the bandit task: With _T_ = 50 steps and _M_ = 25
completions per step, each single run requires about 10 minutes on 4x Nvidia A100 80GB GPUs,
or 40 minutes in single GPU-minutes. This means that the results in Figure 2 took 3 _∗_ 65 _∗_ 40
GPU-minutes = 130 GPU-hours. Extrapolating similarly to the experiments pictured in Figures 4 and
the controlled interactions in Figure 6 produces a total estimate of 150 GPU-hours.

The EAST method itself is computationally inexpensive. Given the dataset of prompts _{Pt_ _[k][}]_ [ we used]
in Section 6.1 of size 3250, it requires computing the last-token activation for each prompt, a process
which takes 1 GPU-hour on the same hardware mentioned above. Then, constructing the steering
vector is a near-instant process of computing a weighted average, given the action entropies which
were already recorded during the interaction stage.


Finally, computational resources were also dedicated to understanding the effects of EAST on a
validation set of 100 prompts, described in Section 6.2. These experiments require sweeping over a
large range of layers and multipliers at the cost of 20 GPU-minutes per layer and multiplier. As such,
for all experiments in Section 6.2 the cost is approximately 100 GPU hours.


As such, the entirety of experiments in the paper required approximately 260 GPU-hours. The entirety
of work for the paper, including preliminary experiments, required an estimated 5x of this figure.


A.1.4 COMPUTATION OF RELATIVE FREQUENCY


In Table 1, Section 6.1, we report the top words of completions generated by the model during
interactions with the task for two conditions, by default and under steering with EAST. We consider
all model responses from 10 seeds of interaction per-environment across means ( _µ_ 0 = 95 _, µ_ 1 = 105),
( _µ_ 0 = 99 _, µ_ 1 = 101), and ( _µ_ 0 = 100 _, µ_ 1 = 100) for both conditions.


For each condition, we tokenize all the responses into words. We then remove common English
[stopwords using the list at https://github.com/stopwords-iso/stopwords-en.](https://github.com/stopwords-iso/stopwords-en) For
each word, we compute its frequency within its respective corpus corresponding to the default and


14


steered conditions. Then, we compute a relative frequency score for each word as the ratio between
the frequencies in the default and steered conditions, and vice versa, to identify the top words.


A.2 PROMPTS AND EXAMPLE INTERACTIONS


We show here the prompts we used and some notable examples of interactions.





Prompt 1: The prompt which we use to describe the bandit task to the agent.







Prompt 2: The alternative prompt in which the task is described to the agent as interacting with slot
machines rather than buttons that is mentioned in Section 6.2. Other details are kept fixed.


15


Transcript 1: An example interaction with the bandit task with means _µ_ 0 = 100 _, µ_ 1 = 100. Based on
limited data, the agent commits to a single action very early on, and follows that choice for the rest of
the interaction, even while it claims to “keep an eye” on the other action.


16


Transcript 2: An example interaction with the bandit task where the agent’s generations are controlled
using EAST ( _µ_ 0 = 100 _, µ_ 1 = 100). The agent exhibits significant uncertainty in its thoughts in
response to feedback from the environment, and no longer commits prematurely.


17


