_2025-1-20_

# **Evolving Deeper LLM Thinking**


**Kuang-Huei Lee** [a,b,1] **, Ian Fischer** [a,1] **, Yueh-Hua Wu** [c,2] **, Dave Marwood** [1] **, Shumeet Baluja** [1] **, Dale Schuurmans** [1,3]

**and Xinyun Chen** [1]

aFirst author contribution, bSenior author contribution, cWork done as a student researcher at Google DeepMind, 1Google
DeepMind, [2] UC San Diego, [3] University of Alberta


**We explore an evolutionary search strategy for scaling inference time compute in Large Language Models.**

**The** **proposed** **approach,** **Mind** **Evolution,** **uses** **a** **language** **model** **to** **generate,** **recombine** **and** **refine**

**candidate** **responses.** **The** **proposed** **approach** **avoids** **the** **need** **to** **formalize** **the** **underlying** **inference**

**problem whenever a solution evaluator is available.** **Controlling for inference cost, we find that Mind**

**Evolution significantly outperforms other inference strategies such as Best-of-N and Sequential Revision**

**in natural language planning tasks.** **In the TravelPlanner and Natural Plan benchmarks, Mind Evolution**

**solves more than 98% of the problem instances using Gemini 1.5 Pro without the use of a formal solver.**


### **1. Introduction**

How can a large language model (LLM) be guided to
_think deeper_ about a complex problem and leverage
inference time compute to improve its problem solving ability? Prior research has investigated various
strategies for leveraging inference time compute, such
as chain-of-thought [41, 21], self-consistency [39], sequential revision based on feedback [36, 30, 8, 19, 1],
and search guided by auxiliary verifiers or evaluators [43]. When a solution evaluator is available,
search strategies have an advantage of being able
to reliably improve problem solving ability with increased compute. For example, methods such as Bestof-N [4, 24, 25] and tree search [37] naturally exploit
additional compute to explore a larger set of solution candidates, thereby increasing the probability of
finding a successful solution.


To better exploit inference time compute, we propose an evolutionary search strategy for LLMs that
combines free-flowing stochastic exploration with
large-scale iterative refinement. We refer to this approach as _Mind Evolution_ . As illustrated in Figure 1,
Mind Evolution is a genetic search strategy that evolves
a diverse population of candidate solutions, leveraging
an LLM to generate, recombine and refine solution
candidates based on feedback from an evaluator. The
overall process is analogous to combining divergent
thinking (free-flowing parallel idea exploration) with
convergent thinking (idea evaluation and selection),
considered as hallmarks of intelligent problem solving
behavior [14].


Unlike Best-of-N, which searches broadly by generating independent candidates for evaluation, Mind Evolution searches both broadly and deeply, exploring a diverse set of candidates and refining the most promising
alternatives. Unlike sequential reasoning approaches,


© 2025 Google DeepMind. All rights reserved



such as self-refinement or tree search [37, 25], which
require evaluation of individual reasoning steps, Mind
Evolution performs global refinement of complete solutions, and therefore only requires a global solution
evaluator rather than a stepwise process reward. Also,
typical of evolutionary methods, Mind Evolution can
be easily parallelized.


There has been prior work on combining evolutionary search with LLMs, primarily in the literature on
evolutionary program generation [34, 17, 29, 23, 6].
However, this prior work focuses on searching through
formal program spaces, using guidance from execution feedback or code explanation. By contrast, Mind
Evolution is not restricted to searching in a formal
space. This allows Mind Evolution to be applied to
problems that are not formalized, or remain difficult
to formalize, as long as a programmatic solution evaluator is available. In particular, we focus on natural
language planning tasks where candidate solutions
can still be automatically parsed, evaluated and critiqued using an implementable oracle evaluator. This
approach exploits the observation that it is often easier
to evaluate the quality of a candidate solution than it
is to generate good solutions for a given problem [11].


In the domain of natural language planning, we consider the TravelPlanner [42] and Natural Plan [47]
benchmarks, where constraint satisfaction problems
are expressed in natural language without any explicit
formalization of the underlying objectives, constraints
or variables. These problems require a set of interconnected decisions that satisfy a set of global and
local constraints. For example, in TravelPlanner, a
travel plan should be produced that respects various
accommodation and dinning constraints, while also
considering budget limitations and other preferences,
all expressed solely in natural language. To date, LLMs
have yet to achieve good performance on these tasks


Evolving Deeper LLM Thinking



































Figure 1 | Mind Evolution is a genetic-based evolutionary search strategy that operates in natural language
space. The figure illustrates how Mind Evolution evolves a population of solution candidates toward higher
quality candidates for a travel planning task. The candidate population is improved through an iterative process,
where an LLM is used to recombine and refine candidates in each iteration.



without the aid of formal solvers [16]. For example,
Gemini 1.5 Flash and o1-preview only achieve a success rate of 5.6% and 11.7% on TravelPlanner respectively, while for the Meeting Planning domain in Natural Plan, they respectively only achieve 20.8% and
44.2%. Even exploiting Best-of-N over 800 independently generated responses, Gemini 1.5 Flash still only
achieves 55.6% success on TravelPlanner and 69.4%
on Meeting Planning. In this paper, we show that
exploration and refinement with evolutionary search
can notably improve problem solving ability. In particular, when controlling for inference time compute,
Mind Evolution allows Gemini 1.5 Flash to achieve
a 95.6% success rate on TravelPlanner and 85.0%
on Meeting Planning. We further experiment with
a two-stage approach, where any unsolved problem
instances are subsequently tackled by Mind Evolution
with Gemini 1.5 Pro, which leads to 100% success on
TravelPlanner and 98.4% on Meeting Planning. All
of the experiments in this paper only use off-the-shelf
LLMs without any finetuning.


To our knowledge, the only prior work that achieves
comparable performance on the TravelPlanner benchmark is [16], which leverages an auxiliary formal
solver and requires the LLM to first translate a given
problem instance into an equivalent formalization. In
general, it takes significant effort and expertise to
correctly formalize a problem expressed in natural
language; prompting an LLM to correctly perform
such a translation requires at least as much domain
expertise. Mind Evolution removes this constraint by
directly optimizing solutions in the space of natural
language.



Finally, we introduce a new benchmark problem,
StegPoet, that involves encoding a hidden message in
a generated essay, story or poem. This form of stenography [33] is difficult to formalize and solve, yet a
hidden message detector can still be implemented to
programmatically guide the search. Our motivation is
to demonstrate the applicability of search beyond natural language domains that can be easily formalized.
We find that Mind Evolution allows Gemini 1.5 Pro to
achieve a success rate of 87% in this task.

### **2. Related Work**


**Pairing LLMs with Evolutionary Search** In addition
to the program generation studies discussed in Section 1, several recent works have explored combining
LLMs and evolution for numerical optimization [26, 3]
and combinatorial optimization [28, 44]. The problem spaces we tackle in this work, such as natural
language planning, can also be viewed as combinatorial optimization problems – optimizing plans subject
to constraints specified in natural language. In contrast to these previous studies, we focus on evolving
solutions in natural language spaces instead of formal
spaces. This removes the requirement of task formalization, which requires significant effort and expert
knowledge for each task instance.


Other works have also applied evolutionary search
to prompt optimization, with the goal of improving
performance on target tasks [45, 10, 15]. Among
these, EvoAgent [45] also evaluated their approach
on the TravelPlanner benchmark. In contrast to our
work, which performs evolutionary search directly on


2


Evolving Deeper LLM Thinking



plans, EvoAgent evolves new LLM agents to form a
multi-agent system for problem solving. Their best
success rate on the TravelPlanner validation set was
7 _._ 2% with GPT-4, while our approach achieved over
95% with Gemini 1.5 Flash.


**Pairing LLMs with Evaluators** In this work, we evaluate solutions with program-based evaluators during the evolutionary search. The idea of integrating
execution-based evaluators in the inference loop has
been widely adopted in the literature of code generation, where the execution environment provides
feedback for the LLM to fix bugs in the generated
code [7, 22, 27, 46, 8, 17, 29, 23, 6, 36].


Other prior work has also considered using learned
verifiers, reward models, or self-evaluation for response refinement [20, 30], search [37, 4, 9, 43, 35],
and improving model learning [40, 25, 32, 1]. These
approaches can often be applied to wider domains
and free-form solutions, but learned feedback models
or self-evaluators can be noisy and are not perfectly
reliable. We leave consideration of such approximate
feedback mechanisms for future work.

### **3. Method**


Mind Evolution employs a genetic search strategy, combined with an LLM and a tailored set of prompts, to
orchestrate an efficient search for solutions to natural language planning tasks. Before describing Mind
Evolution in detail, we first provide a brief overview
of language-based genetic algorithms.


**3.1.** **Language-based Genetic Algorithm Overview**


Genetic algorithms [18, 12, 31] are a meta-heuristic
inspired by natural selection. In a genetic algorithm,
a population of candidate solutions is evolved toward
populations that contain a greater proportion of higher
quality individuals with respect to a target optimization objective. Such an objective is also often referred
to as the “fitness” function. Each individual candidate
has a genetic representation that can be mutated and
recombined with others.


Evolutionary search usually begins with a population of independently generated candidate solutions.
In each generation, the fitness of every individual is
evaluated with respect to the target objective. Candidates are then stochastically selected for reproduction
based on their fitness (“selection”). In reproduction,
the genetic representations of selected parents are
combined (“crossover”) and potentially altered (“mutation”) to produce new child solutions. Such a process creates the next generation of children, which



then enter the population. Population fitness generally increases over successive generations, as parents
with greater fitness are more likely to be selected for
recombination.


**Island** **Model** To sustain diversity in an evolving
population it is also helpful to introduce an island
model [38, 5], where distinct sub-populations (“islands”) are created and evolved independently between “migration” and “island reset” events that occur
at specified frequencies. For a migration operation,
the solutions on one island are stochastically chosen
based on fitness to migrate to an adjacent island. For
an Island Reset operation, the populations on islands
with low overall fitness are replaced by strong solutions from the global population, which also has a
selection effect. The island model has been adopted
in recent successful efforts, such as FunSearch [34].


**Language-based Genetic Representation** The individual candidates in a language-based genetic algorithm are represented by natural language. This
allows the strong language understanding and generation capabilities of an LLM to be leveraged to implement powerful recombination (crossover and mutation) and island reset operations through prompting.


**3.2.** **Mind Evolution**


Figure 1 illustrates the design of Mind Evolution, with
its hyperparameters listed in Table 1. The core components of Mind Evolution are:


1. the specific choices for the selection and migration
operations;
2. the set of prompts that implement the initialization, recombination (crossover and mutation),
and island reset operations with an LLM;
3. the fitness function that evaluates the quality of
a given solution and optionally provides feedback
on issues detected.


The overall evolution process is repeated until a valid
solution is found, or until _𝑁_ gens generations have been
completed, after which the best scoring candidate is
returned.


**Fitness** **Evaluation** As discussed in Section 1, we
implement a fitness function for each problem domain,
where candidate solutions are parsed and evaluated
programmatically. In principle, any function that can
evaluate solution quality can be used, including LLM
evaluation. The evaluation function plays three key


3


Evolving Deeper LLM Thinking


Parameter Default Value Description
_𝑁_ gens 10 The maximum number of generations to search for a solution.
_𝑁_ island 4 How many independent populations to evolve.
_𝑁_ convs 5 How many conversations per island.
_𝑁_ seq 4 How many turns per conversation.
_𝑁_ reset interval 3 How frequently to reset islands in generations.
_𝑁_ reset 2 How many islands to reset. Lowest mean score islands are chosen.
_𝑁_ top 5 How many starting parents to transfer to islands when reset.
_𝑁_ candidate 15 How many candidate parents to consider when resetting islands with the LLM.
_𝑁_ parent 5 Maximum number of parents a conversation can have.
_𝑃𝑟_ no parents 1/6 Probability of a conversation having no parents.
_𝑁_ emigrate 5 How many plans to emigrate to the next island after each island.
_𝑁_ retries 5 How many times to try to generate a plan before giving up at each turn.


Table 1 | Definition of hyperparameters in Mind Evolution. Unless otherwise specified, the experiments in work
use the default values. The product of the first four hyperparameters gives the maximum number of candidate
solutions generated (800 in the default setting).



roles in Mind Evolution: (1) scoring solutions by measuring the optimization objective, if any; (2) verifying
whether the solution satisfies given constraints; and
(3) providing corresponding textual feedback. For example, the evaluation function for the Meeting Planning task scores a proposed plan and provides textual
feedback based on how many constraints are violated
(e.g. meetings conflict with existing schedules), how
many valid meeting events are included in the schedule, and whether the plan follows the required format
(see Appendix A.2 for more details). We have found
that using textual feedback is important empirically,
as shown in our ablation study in Section 4.4.


Note that for many classical search problems (e.g.,
NP-complete problems), verifying solutions can be
much easier than solving the problem [11]. Similarly,
we observe that it is possible to write an evaluation
function for the natural language planning tasks we
consider. The ability to check the correctness of a candidate solution does not obviously lead to the ability
to generate a valid solution in the tasks we consider.
That is, implementing an evaluation function is not
equivalent to solving the task.


**Population** **Initialization** Given a target problem,
we independently sample _𝑁_ convs initial solutions by
prompting an LLM with a description of the problem,
any information needed for solving the problem, and
relevant instructions. If _𝑁_ seq _>_ 1, each of these initial
solutions is then evaluated and refined sequentially
through _𝑁_ seq − 1 additional turns of the “Refinement
through Critical Conversation” process explained below. In total, this initialization procedure generates
_𝑁_ convs × _𝑁_ seq candidate solutions, which forms the initial population on the first island for the first generation.



Figure 2 | Illustrating the Refinement through Critical
Conversation (RCC) process, where an initial solution
is first proposed, then evaluated and subjected to feedback from a critic, after which an author proposed a
refined solution and the process iterates.


**Refinement** **through** **Critical** **Conversation** **(RCC)**
Given a candidate solution (or a set of candidate solutions for the process of recombination) we leverage
an LLM to generate an improved solution by organizing a critical conversation between a “critic” character
and an “author” character, as illustrated in Figure 2.
Separating these two roles is intended to improve the
critical thinking ability of an LLM. Each conversational
turn is structured as a prompt-driven process, where
solutions are refined based on critical feedback, similar to Reflexion [36]. In particular, the critic first
analyzes the candidate solution(s) provided as input,
interprets the textual evaluation feedback, and suggest ways to correct any issues presented in the feedback. The author then proposes a single refined solution based on the input candidate(s), the subsequent
evaluation(s), and the critic’s analyses. The specific
prompts used to drive these conversations are given in
Appendix A.1. An ablation study in Section 4.4 shows
that the critic’s analysis step provides substantial performance improvements.


4






















Evolving Deeper LLM Thinking



**Selection** To produce the next generation of an island, we follow Boltzmann tournament selection [13]
where 0 to _𝑁_ parent parents are stochastically sampled
from the population according a probability distribution that is derived from a softmax transformation of
their fitness scores. In this way, higher-performing
solutions are more likely to be selected for reproduction, while other candidates can still be occasionally
selected for diversity.


**Crossover** **and** **Mutation** We implement the
crossover and mutation operations as a single
recombination step, where an LLM is instructed
to improve a given set of parents using the RCC
process described above (Figure 2). In particular, for
recombination we sample 1 to _𝑁_ parent parents and
alter Step (b) in Figure 2 to first incorporate the
evaluation results of the parents, then apply the critic
to all parents and propose the revised solution as
an “initial solution” for the next generation. Then,
if _𝑁_ seq _>_ 1, we continue to follow Steps (c)(d)(e)
to sequentially generate _𝑁_ seq - 1 child solutions by
refining each previous child using the RCC process.


For each generation on each island, _𝑁_ convs × _𝑁_ seq
child solutions are added to the island population,
with duplicate solutions removed. For selection, we
follow a Boltzmann tournament instead of explicitly
retiring candidate solutions, except when performing
an Island Reset below.


**Migration** **between** **Islands** Between migration
events, each island population is evolved independently. During a migration, the top _𝑁_ emigrate solutions
are cloned from the current Island _𝑖_ to the next Island
_𝑖_ + 1 after completing the generation on the current
island (we update the populations on the islands sequentially from 1 to _𝑁_ island). Migration is performed
cyclically between the islands, so emigrants from Island _𝑁_ island arrive at Island 1. We have found that
this form of cyclic migration accelerates the overall
evolution process.


**Island Reset** Island reset happens every _𝑁_ reset interval
generations. During an Island Reset event, the top
performers are first selected from the global population, the populations on _𝑁_ reset islands with the lowest
average scores are retired, and the selected top performers are cloned onto the reset islands. To select top
performers, we explore two approaches: (1) directly
select the top _𝑁_ top candidates according to fitness; and
(2) first select the top _𝑁_ candidate candidates according
to fitness, then prompt the LLM to select _𝑁_ top good
candidates from this pool that are substantially different from each other. The ablation study in Section 4.4



show that the latter strategy, using an LLM for Island
Reset, achieves better performance.

### **4. Experiments**


**Tasks** We evaluate Mind Evolution on three benchmark natural language planning domains: two tasks
from Natural Plan [47], including Trip Planning (Section 4.2) and Meeting Planning (Section 4.3), and
the TravelPlanner [42] benchmark (Section 4.1). (We
omit the Calendar Scheduling task from Natural Plan,
since these problems can be solved by enumeration.)
Implementation details for each task is provided in
Appendix A, including the prompts (Appendix A.1)
and evaluation functions used (Appendix A.2).


**Models** We use Gemini 1.5 Flash (gemini-1.5-flash001) as the default LLM in our experiments below.
The hyperparameters used when applying Mind Evolution to Flash are specified in Table 1. In addition to
evaluating Mind Evolution with the Flash model, we
also investigate a two-stage approach, where Gemini
1.5 Pro model (gemini-1.5-pro-exp-0827) is used to
tackle problems that are not solved within the _𝑁_ gens
generation limit. Such a two-stage approach provides
better cost-efficiency than using the Pro model on every problem instance. When applying Mind Evolution
to the Pro model we alter the hyperparameters from
those specified in Table 1 to: _𝑁_ convs = 8, _𝑁_ seq = 3,
_𝑁_ parent = 10, _𝑃𝑟_ no parents = 1/5.


**Baselines** For each task, we compare Mind Evolution
to three baseline search strategies that use the same
solution evaluator and task-specific prompts:


1. **1-Pass**, where a solution is proposed using a single forward pass of the LLM.
2. **Best-of-N** [4], where up to 800 candidate solutions are independently generated until a successful solution is found (the same upper bound as
Mind Evolution).
3. **Sequential-Revision+**, where 10 candidate solutions are proposed independently, then revised
separately for 80 turns using the RCC process
(Figure 2). Note that 10 independent threads of
80-turn refinements are used instead of a single
800-turn refinement, because we rarely observe
improvements after 80 turns. This baseline is
similar to running 10 trials of multi-turn Reflexion [36].


Additionally, for reference, we also include an additional 1-Pass baseline that uses OpenAI o1-preview.


5


Evolving Deeper LLM Thinking



**Metrics** We measure Success Rate as the percentage
of problem instances that are solved completely within
a benchmark domain, separating the validation and
test sets. (Note that the Success rate is referred to as
Solve Rate in Natural Plan [47] and Final Pass Rate
in TravelPlanner [42].)


To assess the cost of inference compute we report
the number of LLM calls, the number of input and output tokens, and the total API cost of calling the LLM.
(These costs are given in US Dollars, using prices from
October 2024 when the experiments were conducted.
The base rates are listed in Appendix D.) Note that
assessing computational cost is particularly important
when evaluating search strategies like Mind Evolution, since search is more expensive than generating a
single solution. These statistics can help researchers
and developers understand the cost-benefit trade-offs
when using search to enhance LLM problem solving
ability.


**4.1.** **TravelPlanner**


TravelPlanner [42] is a natural language planning
benchmark that simulates the problem of organizing
a trip plan for a user who expresses preferences and
constraints. We focus on the sole-planning mode (see

[42] for details), where each problem instance consists of a list of options regarding accommodation,
restaurants, attractions and transportation, plus additional constraints that specify user preferences for
budget, cuisine, etc. A plan is evaluated based on
whether it satisfies the user preferences and commonsense constraints.


Table 2 gives detailed results that compare the overall Success Rate and computational cost of Mind Evolution versus the baseline strategies. In terms of Success Rate, Mind Evolution clearly outperforms the
baseline strategies, achieving over 95%. By comparison, Sequential-Revision+ provides a reasonable baseline, achieving almost 83%, while Best-of-N struggles,
achieving only 55.6%. Overall, these results demonstrate a clear advantage of an evolutionary strategy
that combines a broad search, through stochastic exploration, with a deep search that leverages an LLM
for solution refinement.


Considering the two-stage approach, where Mind
Evolution uses Gemini 1.5 Pro for any unsolved problems, we find that nearly the entire dataset can be
solved, achieving a 100% success rate on validation
and 99.9% on test problems respectively. The only
work we are aware of that comes close to this success
rate is [16], which uses GPT-4 for auto-formalization
then leverages a formal solver to achieve 98.9% and
97.0% on validation and test respectively. Mind Evo


Figure 3 | Success rate on the validation set of the
TravelPlanner benchmark, organized by problem instance difficulty and the number of travel days.


lution achieves comparable results without requiring
a formal solver.


Finally, we note that the TravelPlanner dataset is
organized into three levels of difficulty (Easy, Medium,
Hard) and three trip durations (3 days, 5 days, 7
days), rendering 9 different problem classes. Figure 3
presents a breakdown of the success rates achieved
across these different categories, showing that the
success rates of 1-Pass and Best-of-N decline when
planning for more travel days, but the trend is less
clear for Mind Evolution and Sequential-Revision+,
both of which iteratively refine proposed solutions.


**4.2.** **Natural Plan – Trip Planning**


The Trip Planning task [47] involves finding an
itinerary that consists of a sequence of cities to visit
and number of days in each that satisfies flight connectivity and scheduling constraints – see Table 3 for
a problem instance. We split the benchmark into 320
validation and 1,280 test instances (described in more
detail in Appendix B).


The results in Table 2 again show that Mind Evolution strongly outperforms the baselines on this task,
achieving 96.2% on the validation and 94.1% on the
test instances. Table 2 also shows a qualitative comparison between the results produced by Mind Evolution
and the baseline strategies. Note that Best-of-N performs better in this scenario (77.2%), even beating
Sequential-Revision+ (74.4%). We find that for the
two-stage approach, Mind Evolution achieves 100%
on the validation set and 99.6% on the test set. These
findings again highlight the benefit of evolutionary
search versus simple sampling and sequential refinement.


Finally, we note that the difficulty of this task varies
with the number of cities to visit, ranging from 3 to
10. Figure 4 shows a breakdown of the Success Rate
in terms of number of cities, where the relative advantage of Mind Evolution appears to increase as the
number of cities grows.


6



Mind Evolution (Ours) Seq. Revisions+ Best-of-N 1-Pass



100%


75%


50%


25%


0%



Easy
3-day



Easy
5-day



Easy
7-day



Medium

3-day



Medium

5-day



Medium

7-day



Hard
3-day



Hard
5-day



Hard
7-day


Evolving Deeper LLM Thinking

|Col1|Set|Success Rate|LLM Calls|Input Tokens|Output Tokens|API Cost (Oct 2024)|
|---|---|---|---|---|---|---|
|**TravelPlanner [42]**|**TravelPlanner [42]**|**TravelPlanner [42]**|**TravelPlanner [42]**|**TravelPlanner [42]**|**TravelPlanner [42]**|**TravelPlanner [42]**|
|1-Pass<br>(o1-preview 1-Pass)<br>Best-of-N<br>Sequential-Revision+<br>**Mind Evolution**<br>**(+pro)**|val<br>val<br>val<br>val<br>val<br>val|10/180 = 5_._6%<br>21/180 = 11_._7%<br>100/180 = 55_._6%<br>149/180 = 82_._8%<br>172/180 =** 95**_._**6**%<br>180/180 =** 100**%|1<br>1<br>472<br>280<br>174<br>(257)|0_._009M<br>0_._008M<br>4_._44M<br>35_._53M<br>3_._10M<br>(3_._25M)|0_._001M<br>0_._008M<br>0_._47M<br>0_._29M<br>0_._18M<br>(0_._19M)|US$0_._001<br>US$0_._601<br>US$0_._47<br>US$2_._75<br>US$0_._29<br>(US$0_._54)|
|**Mind Evolution**<br>**(+pro)**|test<br>test|952/1000 =** 95**_._**2**%<br>999/1000 =** 99**_._**9**%|167<br>(67)|3_._02M<br>(3_._05M)|0_._18M<br>(0_._18M)|US$0_._28<br>(US$0_._33)|
|**Natural Plan [47] Trip Planning**|**Natural Plan [47] Trip Planning**|**Natural Plan [47] Trip Planning**|**Natural Plan [47] Trip Planning**|**Natural Plan [47] Trip Planning**|**Natural Plan [47] Trip Planning**|**Natural Plan [47] Trip Planning**|
|1-Pass<br>(o1-preview 1-Pass)<br>Best-of-N<br>Sequential-Revision+<br>**Mind Evolution**<br>**(+pro)**|val<br>val<br>val<br>val<br>val<br>val|66/320 = 20_._6%<br>116/320 = 36_._2%<br>247/320 = 77_._2%<br>238/320 = 74_._4%<br>308/320 =** 96.2%**<br>320/320 =** 100%**|1<br>1<br>274<br>391<br>168<br>(111)|0_._002M<br>0_._002M<br>0_._61M<br>41_._57M<br>1_._48M<br>(1_._51M)|0_._001M<br>0_._008M<br>0_._18M<br>0_._38M<br>0_._19M<br>(0_._19M)|_<_US$0_._001<br>US$0_._53<br>US$0_._10<br>US$3_._23<br>US$0_._17<br>(US$0_._22)|
|**Mind Evolution**<br>**(+pro)**|test<br>test|1204/1280 =** 94.1%**<br>1275/1280 =** 99.6%**|196<br>(211)|1_._78M<br>(1_._86M)|0_._22M<br>(0_._24M)|US$0_._20<br>(US$0_._37)|
|**Natural Plan [47] Meeting Planning**|**Natural Plan [47] Meeting Planning**|**Natural Plan [47] Meeting Planning**|**Natural Plan [47] Meeting Planning**|**Natural Plan [47] Meeting Planning**|**Natural Plan [47] Meeting Planning**|**Natural Plan [47] Meeting Planning**|
|1-Pass<br>(o1-preview 1-Pass)<br>Best-of-N<br>Sequential-Revision+<br>**Mind Evolution**<br>**(+pro)**|val<br>val<br>val<br>val<br>val<br>val|104/500 = 20_._8%<br>221/500 = 44_._2%<br>347/500 = 69_._4%<br>310/500 = 62_._0%<br>425/500 =** 85.0%**<br>492/500 =** 98.4%**|1<br>1<br>444<br>484<br>406<br>(890)|0_._007M<br>0_._006M<br>3_._99M<br>32_._16M<br>5_._35M<br>(13_._36M)|0_._001M<br>0_._006M<br>0_._31M<br>0_._40M<br>0_._41M<br>(0_._91M)|US$0_._001<br>US$0_._47<br>US$0_._39<br>US$2_._53<br>US$0_._52<br>(US$2_._55)|
|**Mind Evolution**<br>**(+pro)**|test<br>test|419/500 =** 83.8%**<br>491/500 =** 98.2%**|394<br>(828)|5_._24M<br>(12_._25M)|0_._40M<br>(0_._83M)|US$0_._51<br>(US$2_._34)|



Table 2 | Experimental results on benchmark natural language planning tasks. “(+pro)” denotes the two-stage
results, where we use Gemini 1.5 Pro to solve the problems that were not solved in experiments using Gemini
1.5 Flash. Number of LLM calls, token counts, and API cost are averaged across the validation or test problem
set, and they are calculated only on the remaining problems for the “(+pro)” experiments. Here, we also show
OpenAI o1-preview results as a reference.



100%


75%


50%


25%


0%



Mind Evolution (Ours) Seq. Revisions+ Best-of-N 1-Pass


3 4 5 6 7 8 9 10

Number of Cities (to visit)



Figure 4 | Success rate on the validation set of the Trip
Planning benchmark per number of cities to visit.


**4.3.** **Natural Plan – Meeting Planning**


For the Meeting Planning task a sequence of meetings should be scheduled to maximize the number of
meetings between individuals subject to availability,
location and travel time constraints [47]. This task
differs from TravelPlanner and Trip Planning in that
not every meeting can be scheduled for every problem instance, implying that it is not possible to know
whether an optimal solution has been reached. There


fore, to obtain the results shown in Table 2, we allow
the searches to proceed until the upper bounds on
iteration counts have been reached. For this task, we
split the set of instances into 500 validation and 500
test instances (see Appendix B for details).


The results shown in Table 2 continue to demonstrate a significant performance for Mind Evolution
over baseline strategies, achieving an 85.0% Success
Rate on the validation set and 83.8% on the test set.
Notably, the two-stage approach using Gemini 1.5
Pro achieves success rates to 98.4% and 98.2% on
validation and test respectively.


Finally, Figure 5 shows the breakdown of success
rates by the number of people to schedule meetings
with. In this case, we find that Mind Evolution sustains
a significant advantage in success rate as the number
of people increases.


7


Evolving Deeper LLM Thinking


Table 3 | An example problem instance from the Trip Planning task in Natural Plan, with the predicted plans
from Mind Evolution and the baselines. 1-Pass and Best-of-N both make mistakes on number of days to stay,
but satisfy the requirements of being in Madrid and Santorini on specific days. The Sequential-Revision+ plan
omits the annual show in Madrid and plans a non-existent flight, but is correct in the number of days. In
contrast, the Mind Evolution plan satisfies all specified requirements.



100%


75%


50%


25%


0%



Mind Evolution (Ours) Seq. Revisions+ Best-of-N 1-Pass


1 2 3 4 5 6 7 8 9 10

Number of People (to meet)



Figure 5 | Success rate on the validation set of the
Meeting Planning benchmark per number of people
to meet with.


**4.4.** **Analysis and Ablation Studies**


To understand how Mind Evolution’s performance
scales, and how the different components affect its
behavior, we provide additional measurements and
ablations to gain additional insight.


**Scaling** Regarding scaling, Figure 6 reports the Success Rate achieved by Mind Evolution across the planning tasks as a function of the number of generations.
These results clearly show steady improvement for
Mind Evolution as the number of generations is increased.


To compare the scaling of Mind Evolution to that of
the baseline search methods, we also plot the Success



Rate and average task evaluation scores as a function of the number of candidate solutions generated
by the each strategy (Figures 7–9). The task evaluation scores are calculated by penalizing unsatisfied
constraints and suboptimality of the objective value,
hence the maximum score that can be achieved in any
problem instance is zero (see Appendix A.2 for details). In Appendix D, we provide another perspective
on the cost-benefit trade-offs in terms of the specific
API costs incurred.


Figures 7–9 show the results for the TravelPlanner,
Trip Planning and Meeting Planning tasks respectively.
In each case, we see that the overall success rates
and average task evaluation scores improve monotonically with an increasing number of proposed solutions
across all search methods. These plots also show that
Mind Evolution is consistently more effective than the
baseline strategies with respect to the number of candidate solutions needed to achieve a specified level of
success rate (or average task performance).


We note that Best-of-N appears to be significantly
underperforming on TravelPlanner. We hypothesize
that this occurs because this task involves implicit commonsense constraints (e.g., a trip plan should return
to the origin city, a restaurant cannot be visited twice,
etc.), which are not given in the problem instance
but instead learned from evaluation feedback, which
Best-of-N does not leverage.


8


Evolving Deeper LLM Thinking



1.0


0.9


0.8


0.7


0.6


0.5



1 2 3 4 5 6 7 8 9 10
Generations



0 200 400 600 800
# Candidate Solutions



0 200 400 600 800
# Candidate Solutions



1

2

3

4

5

6

7

8



0.8

0.7

0.6

0.5

0.4

0.3

0.2



Figure 6 | Success rate on the validation set for each
natural language planning benchmark at each generation of Mind Evolution.


|Critic<br>S/Q Prompts<br>Textual Feedback<br>Reset with LLM|✓ ✓ ✓ ✓<br>✓ ✓ ✓<br>✓ ✓<br>✓|
|---|---|
|Success Rate|46_._1%<br>71_._1%<br>76_._1%<br>91_._1%<br>95_._6%|



0 200 400 600 800
# Candidate Solutions



0


1


2


3


4



1.0


0.8


0.6


0.4


0.2



0 200 400 600 800
# Candidate Solutions



Figure 7 | TravelPlanner success rates and evaluation scores as the number of candidate solutions is
increased.



0 200 400 600 800
# Candidate Solutions



0


1


2


3


4



0 200 400 600 800
# Candidate Solutions



1.0


0.8


0.6


0.4


0.2



Figure 8 | Trip Planning success rates and evaluation scores as the number of candidate solutions is
increased.


**Ablations** We also conducted a set of ablations to
study the contribution of the different components of
Mind Evolution. Table 4 shows that using the critic
step in the RCC process (Figure 2 in Section 3.2) and
textual feedback from the evaluation functions are
the most critical to performance, although the other
components also make meaningful contributions to
performance.


To assess hyperparameter sensitivity, we investigated the Trip Planning task in greater detail, choosing the harder setting with 10 cities to better reveal
differences in performance. (Similar results are also



Figure 9 | Meeting Planning success rates and evaluation scores as the number of candidate solutions is
increased.


Table 4 | An ablation study of Mind Evolution components on the TravelPlanner validation set. Each
column in the table shows an experiment where ✓
indicates whether a component is used. If “Critic” is
disabled, we skip the critic step in Figure 2 and go
straight to the author step. “S/Q Prompts” stands for
Strategy/Question prompts, which are additional taskspecific instructions in the critical thinking prompts
(see Appendix A.1 for details). If “Textual Feedback” is
disabled, we do not include evaluation feedback in the
prompts. If “Reset with LLM” is disabled, we directly
select global elites by their evaluation scores in island
reset events, rather than use an LLM to choose, as
described in Section 3.2.

|Col1|Succ. Rate|
|---|---|
|w/ island model (_𝑁_island = 4, _𝑁_convs = 5)<br>w/o island model (_𝑁_ = 1, _𝑁_convs = 20)|<br>87.5%<br>77.4%|
|island  <br>_𝑁_convs = 10_, 𝑁_gens = 5<br>_𝑁_convs = 5_, 𝑁_gens = 10 (default)<br>_𝑁_convs = 4_, 𝑁_gens = 13|82.5%<br>87.5%<br>85.0%|



Table 5 | Hyperparameter studies on the Trip Planning
problem instances with 10 cities. The first two rows
show the difference between enabling and disabling
the island model. The bottom three rows illustrate
a trade-off between the number of candidates per
generation versus the number of generations. (Note
that the bottom row ( _𝑁_ convs = 4 _, 𝑁_ gens = 13) produces
slightly more than 800 solutions (832).


observed on the harder problem instances from the
other benchmark tasks.) In Table 5, the top two rows
compare the effect of including or excluding the island model from the evolutionary search, controlling
for the same number (800) of candidate solutions.
These results show that the island model significantly


9


Evolving Deeper LLM Thinking


Task Results (Cipher and Poem)



I like to walk, I like to stride,
With ROOSTER crows and FLOWERS by my side.
I like to walk, I like to roam,
Past BRIGHT green fields and FLAMES at home.
I like to walk, I like to stroll,
To see the CHERRY trees and a CRIMSON hole.
I like to walk, I like to ramble,
To watch the SUNSET and hold a RUBY’s gamble.
I like to walk, I like to wander,
To watch a SCARLET leaf, and a fire, BURNING, under.
I like to walk, I like to stride,
With ROOSTER crows and FLOWERS by my side.



Message To Encode (M):
10,20,30,40,
50,60,70,80,
90,100,10,20


Style: Poem
Inspiration: Shel Silverstein
Words Between (B): 4
Topic: "The Fun of Walking"



10 : rooster;
20 : flowers;
30 : bright;
40 : flames;
50 : cherry;
60 : crimson;
70 : sunset;
80 : ruby;
90 : scarlet;
100 : burning;



Figure 10 | **StegPoet example.** Example of the encoding of a StegPoet problem instance (left) and a correct
solution (right) that includes the number-to-word cipher and a poem in the style of a children’s poetry author.
Note that | _𝑀_ | = 12 in this instance. We added capitalization to the code words to highlight them.

|Col1|Set|Success Rate|Input Tokens|Output Tokens|API Cost (Oct 2024)|
|---|---|---|---|---|---|
|1-Pass<br>Best-of-N<br>Sequential-Revision+<br>**Mind Evolution**<br>**(+pro)**|val<br>val<br>val<br>val<br>val|0/101 = 0_._0%<br>1/101 = 1_._0%<br>20/101 = 19_._8%<br>47/101 =** 46.5%**<br>88/101 =** 87.1%**|0_._002M<br>1_._56M<br>41_._69M<br>3_._56M<br>3_._74M|_<_ 0_._001M<br>0_._25M<br>0_._24M<br>0_._20M<br>0_._22M|_<_$0_._001<br>$0_._19<br>$3_._20<br>$0_._33<br>$0_._65|
|**Mind Evolution**<br>**(+pro)**|test<br>test|106/245 =** 43.3%**<br>194/245 =** 79.2%**|$0_._34<br>$0_._72|3_._63M<br>3_._84M|0_._22M<br>0_._24M|



Table 6 | **Experimental** **results** **on** **StegPoet.** Price and token counts are averages per problem. All results
use Gemini 1.5 Flash, except **(+pro)**, which solves the problems that were not solved in the Flash runs, using
Gemini 1.5 Pro.



100%


75%


50%


25%


0%



Mind Evolution (Ours) Seq. Revisions+ Best-of-N 1-Pass


2 3 4 5 6 7 8

Min Required Word Spacing



Figure 11 | Histogram of Success Rate for each difficulty level. 1-Pass returns valid responses, but fails
to solve any of the problems, so it is not visible in the
histogram.


improves the performance of Mind Evolution. The
bottom three rows compare the effect of increasing
the number of candidate solutions per generation versus having more generations while controlling for a
similar number of candidates considered overall. In
this case, it appears that deeper evolutionary search
indeed has benefits, although it is also important to
continue exploring broadly in each generation.

### **5. A Challenging New Task: StegPoet**


We introduce a challenging new task, StegPoet, where
a hidden message should be stenographically encoded

[33] into a piece of creative writing. Even though the



problem is difficult to formalize, it remains amenable
to programmatic verification, which makes it addressable by the methods considered in this paper. In this
task, a hidden message ( _𝑀_ ) expressed by a sequence
of numbers should be encoded in a piece of creative
text about a particular topic, expressed in the form of
an essay, story or poem. The goal is to both provide a
number-to-word substitution cipher and a generated
text that uses the cipher to encode the message. Figure 10 gives an example. We impose an additional
constraint that there must be, on average, _𝐵_ words between successive cipher words in the generated text,
which ensures that simply listing the cipher words
as the text portion does not qualify as solution when
_𝐵>_ 0.


The difficulty of this problem varies along four axes:


1. Difficulty increases with the length of the hidden
message, _𝑀_ . We set 10 ≤| _𝑀_ | ≤ 30.
2. The repetition of the numbers in _𝑀_ . The more repetition, the more stringent the constraints.
3. The “closeness” of the repeated numbers to each
other. Each form of writing dictates how much repetition of the same word and proximity of occurrence
is acceptable. The LLM must balance adherence to
the form with the need to correctly encode the message.
4. Empirically, as _𝐵_ (the mean distance between cipher
words) grows, the problem becomes more difficult.


10


Evolving Deeper LLM Thinking



In our tests, 3 ≤ _𝐵_ ≤ 7.


We divide the problem instances into a validation split
of 101 instances and a test split of 245 instances. See
Appendix F for additional details about the StegPoet
evaluation.


Detailed performance results for Mind Evolution
and the baseline strategies are given in Table 6, while
Figure 11 shows performance per difficulty level. Here
the two-stage Mind Evolution (+pro) achieves 87.1%
on validation and 79.2% on test. Best-of-N only manages to solve 1% of the validation tasks.

### **6. Conclusion**


We have presented Mind Evolution, an evolutionary
search approach for solving challenging natural language planning problems, by scaling inference-time
compute for stochastic exploration and iterative refinement. An evaluation on the TravelPlanner and Natural
Plan natural language planning benchmarks, as well
as a new benchmark StegPoet introduced in this paper, demonstrates that Mind Evolution significantly
outperforms Best-of-N and sequential revision. To our
knowledge, this is the first approach that is able to
achieve such a level of success on these tasks without
explicitly leveraging a formal solver.


**Limitations** The main limitation of the current work
is the focus on natural language planning problems
where proposed solutions can be programmatically
evaluated and critiqued. In future work, we aim to extend beyond this limitation by developing LLM-based
evaluators that would enable broader applications.

### **Acknowledgement**


The authors thank Sergio Guadarrama and Doina Precup for supporting this work. We also thank Sirui Xie,
John Canny, and the Google DeepMind FunSearch
team for valuable discussion.

### **References**


[1] Y. Bai, S. Kadavath, S. Kundu, A. Askell,
J. Kernion, A. Jones, A. Chen, A. Goldie,
A. Mirhoseini, C. McKinnon, et al. Constitutional AI: Harmlessness from AI feedback. _arXiv_
_preprint arXiv:2212.08073_, 2022.


[2] B. Berger, M. S. Waterman, and Y. W. Yu. Levenshtein distance, sequence comparison and biological database search. _IEEE Transactions on In-_



_formation Theory_, 67(6):3287–3294, 2021. doi:
10.1109/TIT.2020.2996543.


[3] S. Brahmachary, S. M. Joshi, A. Panda, K. Koneripalli, A. K. Sagotra, H. Patel, A. Sharma, A. D.
Jagtap, and K. Kalyanaraman. Large language
model-based evolutionary optimizer: Reasoning
with elitism. _arXiv preprint arXiv:2403.02054_,
2024.


[4] B. Brown, J. Juravsky, R. Ehrlich, R. Clark,
Q. V. Le, C. Ré, and A. Mirhoseini. Large
language monkeys: Scaling inference compute with repeated sampling. _arXiv_ _preprint_
_arXiv:2407.21787_, 2024.


[5] E. Cantú-Paz et al. A survey of parallel genetic
algorithms. _Calculateurs_ _paralleles,_ _reseaux_ _et_
_systems repartis_, 10(2):141–171, 1998.


[6] A. Chen, D. M. Dohan, and D. R. So. EvoPrompting: Language models for code-level neural architecture search. In _Proceedings_ _of_ _the_ _37th_
_International Conference on Neural Information_
_Processing Systems_, pages 7787–7817, 2023.


[7] B. Chen, F. Zhang, A. Nguyen, D. Zan, Z. Lin,
J.-G. Lou, and W. Chen. CodeT: Code generation with generated tests. In _The_ _Eleventh_
_International_ _Conference_ _on_ _Learning_ _Represen-_
_tations_, 2023. URL [https://openreview.](https://openreview.net/forum?id=ktrw68Cmu9c)
[net/forum?id=ktrw68Cmu9c.](https://openreview.net/forum?id=ktrw68Cmu9c)


[8] X. Chen, M. Lin, N. Schärli, and D. Zhou.
Teaching large language models to selfdebug. In _The Twelfth International Conference_
_on_ _Learning_ _Representations_, 2024. URL
[https://openreview.net/forum?id=](https://openreview.net/forum?id=KuPixIqPiq)
[KuPixIqPiq.](https://openreview.net/forum?id=KuPixIqPiq)


[9] K. Cobbe, V. Kosaraju, M. Bavarian, M. Chen,
H. Jun, L. Kaiser, M. Plappert, J. Tworek,
J. Hilton, R. Nakano, et al. Training verifiers
to solve math word problems. _arXiv_ _preprint_
_arXiv:2110.14168_, 2021.


[10] C. Fernando, D. Banarse, H. Michalewski,
S. Osindero, and T. Rocktäschel. Promptbreeder:
Self-referential self-improvement via prompt
evolution. _arXiv_ _preprint_ _arXiv:2309.16797_,
2023.


[11] M. R. Garey and D. S. Johnson. _Computers and_
_Intractability:_ _A Guide to the Theory of NP Com-_
_pleteness_ . W. H. Freeman & Co., 1979.


[12] D. E. Golberg. _Genetic Algorithms in Search, Opti-_
_mization, and Machine Learning_ . Addison Wesley,
1989.


11


Evolving Deeper LLM Thinking




[13] D. E. Goldberg. A note on Boltzmann tournament selection for genetic algorithms and
population-oriented simulated annealing. _Com-_
_plex Systems_, 4:445–460, 1990.


[14] J. P. Guilford. _The Nature of Human Intelligence_ .
1967.


[15] Q. Guo, R. Wang, J. Guo, B. Li, K. Song, X. Tan,
G. Liu, J. Bian, and Y. Yang. Connecting
large language models with evolutionary algorithms yields powerful prompt optimizers. _arXiv_
_preprint arXiv:2309.08532_, 2023.


[16] Y. Hao, Y. Chen, Y. Zhang, and C. Fan. Large
language models can plan your travels rigorously
with formal verification tools. _arXiv_ _preprint_
_arXiv:2404.11891_, 2024.


[17] E. Hemberg, S. Moskal, and U.-M. O’Reilly. Evolving code with a large language model. _Genetic_
_Programming and Evolvable Machines_, 25(2):21,
2024.


[18] J. H. Holland. _Adaptation in Natural and Artificial_
_Systems_ . University of Michigan Press, Ann Arbor,
MI, 1975. second edition, 1992.


[19] G. Kim, P. Baldi, and S. McAleer. Language
models can solve computer tasks. _arXiv preprint_
_arxiv:2303.17491_, 2023.


[20] J. H. Kirchner, Y. Chen, H. Edwards, J. Leike,
N. McAleese, and Y. Burda. Prover-verifier games
improve legibility of LLM outputs. _arXiv preprint_
_arXiv:2407.13692_, 2024.


[21] T. Kojima, S. S. Gu, M. Reid, Y. Matsuo, and
Y. Iwasawa. Large language models are zeroshot reasoners. _Advances in Neural Information_
_Processing Systems_, 35:22199–22213, 2022.


[22] H. Le, Y. Wang, A. D. Gotmare, S. Savarese, and
S. C. H. Hoi. CodeRL: Mastering code generation
through pretrained models and deep reinforcement learning. _Advances in Neural Information_
_Processing Systems_, 35:21314–21328, 2022.


[23] J. Lehman, J. Gordon, S. Jain, K. Ndousse, C. Yeh,
and K. O. Stanley. Evolution through large models. In _Handbook of Evolutionary Machine Learn-_
_ing_, pages 331–366. Springer, 2023.


[24] Z. Liang, Y. Liu, T. Niu, X. Zhang, Y. Zhou, and
S. Yavuz. Improving LLM reasoning through
scaling inference computation with collaborative
verification. _arXiv_ _preprint_ _arXiv:2410.05318_,
2024.




[25] H. Lightman, V. Kosaraju, Y. Burda, H. Edwards, B. Baker, T. Lee, J. Leike, J. Schulman,
I. Sutskever, and K. Cobbe. Let’s verify step by
step. _arXiv preprint arXiv:2305.20050_, 2023.


[26] F. Liu, X. Lin, Z. Wang, S. Yao, X. Tong, M. Yuan,
and Q. Zhang. Large language model for
multi-objective evolutionary optimization. _arXiv_
_preprint arXiv:2310.12541_, 2023.


[27] J. Liu, Y. Zhu, K. Xiao, Q. FU, X. Han, Y. Wei,
and D. Ye. RLTF: Reinforcement learning
from unit test feedback. _Transactions_ _on_ _Ma-_
_chine_ _Learning_ _Research_, 2023. ISSN 28358856. URL [https://openreview.net/](https://openreview.net/forum?id=hjYmsV6nXZ)
[forum?id=hjYmsV6nXZ.](https://openreview.net/forum?id=hjYmsV6nXZ)


[28] S. Liu, C. Chen, X. Qu, K. Tang, and Y.-S. Ong.
Large language models as evolutionary optimizers. In _2024 IEEE Congress on Evolutionary Com-_
_putation (CEC)_, pages 1–8. IEEE, 2024.


[29] V. Liventsev, A. Grishina, A. Härmä, and L. Moonen. Fully autonomous programming with large
language models. In _Proceedings of the Genetic_
_and Evolutionary Computation Conference_, pages
1146–1155, 2023.


[30] A. Madaan, N. Tandon, P. Gupta, S. Hallinan,
L. Gao, S. Wiegreffe, U. Alon, N. Dziri, S. Prabhumoye, Y. Yang, et al. Self-refine: Iterative
refinement with self-feedback. _Advances in Neu-_
_ral Information Processing Systems_, 36, 2024.


[31] M. Mitchell. _An_ _Introduction_ _to_ _Genetic_ _Algo-_
_rithms_ . MIT press, 1998.


[32] J. S. Park, J. O’Brien, C. J. Cai, M. R. Morris,
P. Liang, and M. S. Bernstein. Generative agents:
Interactive simulacra of human behavior. In _Pro-_
_ceedings of the 36th Annual ACM Symposium on_
_User_ _Interface_ _Software_ _and_ _Technology_, pages
1–22, 2023.


[33] N. Provos and P. Honeyman. Hide and seek: An
introduction to steganography. _IEEE security &_
_privacy_, 1(3):32–44, 2003.


[34] B. Romera-Paredes, M. Barekatain, A. Novikov,
M. Balog, M. P. Kumar, E. Dupont, F. J. Ruiz, J. S.
Ellenberg, P. Wang, O. Fawzi, et al. Mathematical discoveries from program search with large
language models. _Nature_, 625(7995):468–475,
2024.


[35] A. Setlur, C. Nagpal, A. Fisch, X. Geng, J. Eisenstein, R. Agarwal, A. Agarwal, J. Berant, and
A. Kumar. Rewarding progress: Scaling automated process verifiers for LLM reasoning. _arXiv_
_preprint arXiv:2410.08146_, 2024.


12


Evolving Deeper LLM Thinking




[36] N. Shinn, F. Cassano, A. Gopinath,
K. Narasimhan, and S. Yao. Reflexion:
Language agents with verbal reinforcement
learning. _Advances_ _in_ _Neural_ _Information_
_Processing Systems_, 36, 2024.


[37] C. Snell, J. Lee, K. Xu, and A. Kumar. Scaling
LLM test-time compute optimally can be more
effective than scaling model parameters. _arXiv_
_preprint arXiv:2408.03314_, 2024.


[38] R. Tanese. _Distributed genetic algorithms for func-_
_tion optimization_ . University of Michigan, 1989.


[39] X. Wang, J. Wei, D. Schuurmans, Q. V. Le, E. H.
Chi, S. Narang, A. Chowdhery, and D. Zhou.
Self-consistency improves chain of thought reasoning in language models. In _The_ _Eleventh_
_International_ _Conference_ _on_ _Learning_ _Represen-_
_tations_, 2023. URL [https://openreview.](https://openreview.net/forum?id=1PL1NIMMrw)
[net/forum?id=1PL1NIMMrw.](https://openreview.net/forum?id=1PL1NIMMrw)


[40] Z. Wang, Y. Li, Y. Wu, L. Luo, L. Hou, H. Yu, and
J. Shang. Multi-step problem solving through
a verifier: An empirical analysis on modelinduced process supervision. _arXiv_ _preprint_
_arXiv:2402.02658_, 2024.


[41] J. Wei, X. Wang, D. Schuurmans, M. Bosma,
F. Xia, E. Chi, Q. V. Le, D. Zhou, et al. Chainof-thought prompting elicits reasoning in large
language models. _Advances in Neural Informa-_
_tion Processing Systems_, 35:24824–24837, 2022.


[42] J. Xie, K. Zhang, J. Chen, T. Zhu, R. Lou, Y. Tian,
Y. Xiao, and Y. Su. Travelplanner: A benchmark
for real-world planning with language agents.
_arXiv preprint arXiv:2402.01622_, 2024.


[43] S. Yao, D. Yu, J. Zhao, I. Shafran, T. L. Griffiths,
Y. Cao, and K. Narasimhan. Tree of thoughts:
Deliberate problem solving with large language
models. In _Proceedings of the 37th International_
_Conference on Neural Information Processing Sys-_
_tems_, pages 11809–11822, 2023.


[44] H. Ye, J. Wang, Z. Cao, F. Berto, C. Hua, H. Kim,
J. Park, and G. Song. ReEvo: Large language
models as hyper-heuristics with reflective evolution. _arXiv preprint arXiv:2402.01145_, 2024.


[45] S. Yuan, K. Song, J. Chen, X. Tan, D. Li, and
D. Yang. EvoAgent: Towards automatic multiagent generation via evolutionary algorithms.
_arXiv preprint arXiv:2406.14228_, 2024.


[46] K. Zhang, D. Wang, J. Xia, W. Y. Wang, and L. Li.
ALGO: Synthesizing algorithmic programs with
LLM-generated oracle verifiers. In _Proceedings_
_of_ _the_ _37th_ _International_ _Conference_ _on_ _Neural_



_Information_ _Processing_ _Systems_, pages 54769–
54784, 2023.


[47] H. S. Zheng, S. Mishra, H. Zhang, X. Chen,
M. Chen, A. Nova, L. Hou, H.-T. Cheng, Q. V.
Le, E. H. Chi, et al. NATURAL PLAN: Benchmarking LLMs on natural language planning.
_arXiv preprint arXiv:2406.04520_, 2024.


13


Evolving Deeper LLM Thinking


### **A. Implementation Details**

Here we describe the implementation details of Mind
Evolution. The code will be made available.


**A.1.** **Prompt Design**


We first use Meeting Planning as an example to illustrate the structure of the prompts used. The prompts,
as well as the model responses when parent solutions
are given, are shown in Figures 12-16. The prompts
begin with general instructions and a general problem
definition, few-shot examples, then a task description.
The few-shot examples help the LLM understand the
problem and generate solutions closer to the desired
formats. For TravelPlanner, we take two 3-day example plans from the training set and use them across all
tasks (3-7 days). For Trip Planning, we take two example plans from the few-shot examples provided by the
benchmark and use them across all tasks. For Meeting
Planning, we use the 5-shot examples provided by the
benchmark for each task.


After the task description, we include parent solutions with corresponding evaluation feedback, followed by critical thinking instructions (in Figures 14–
15). These instructions lead the LLM to improve the
parent solutions, following the Refinement through
Critical Conversation (RCC) process described in Section 3.2. The critical thinking instructions include
problem-specific Strategy/Question prompts based on
findings in each validation set (ablated in Section 4.4).
In the model responses, one can see that the LLM follows the critical thinking instructions in playing the
critic role to analyze the parent solutions, and playing
the author role to propose a new solution.


We also give an example of the prompt and a model
response for TravelPlanner, which has the same structure, in Figures 17–22.


**A.2.** **Evaluation Functions**


In this work, solutions are evaluated programmatically with a function. As described in Section 3.2, an
evaluation function has three main roles: (1) scoring
solutions by measuring the optimization objective, if
any; (2) verifying whether the solution satisfies given
constraints; and (3) providing corresponding textual
feedback. Specifically, we score natural language plans
by penalizing the constraints that are not satisfied, the
objectives that are not maximized, and for not following the required solution format. Thus the maximum
score for all tasks is zero. We also provide textual
feedback that describes how the constraints are not
satisfied and how the objectives are not maximized.



**TravelPlanner** Our evaluation function for TravelPlanner is modified from the TravelPlanner evaluation code [42]. The evaluation code expects travel
plans in JSON format. We modify the original evaluation code to make it output a cumulative score that reflects all the constraints that are not satisfied, instead
of simply answering whether or not a plan satisfies
all the constraints. We also make it provide textual
feedback for the violated constraints.


In the TravelPlanner validation set, the constraints
are provided in both user query text and a structured
JSON format. However, in the test set, the constraints
are only described in user query text. To make it
easier for the evaluation function to consider the constraints, we extract them from user query into JSON
using Gemini 1.5 Flash. For example, to extract the
requested cuisines, we prompt Gemini with “Look at
the following text and tell me if there are any cuisine
requirements on the upcoming trip...” multiple times,
and formulate the final answer via majority voting. To
verify the reliability of this approach, we tested on the
validation set and found complete agreement between
the JSON extracted from user query and the provided
JSON. In addition, we upload our test solutions to the
TravelPlanner evaluation server, and found that the
results agree with the official evaluation.


**Trip** **Planning** Similar to TravelPlanner, the Trip
Planning evaluation function expects plans in JSON
format. Since Trip Planning user queries are programmatically generated, we can parse the constraints specified in user queries. These constraints include number
of days to stay in a city, specific days to be in a city
(e.g., for events), and whether there are flights between cities. Our evaluation function scores a plan
by the constraints that are not satisfied and whether
it conforms with the desired JSON format, while also
providing corresponding textual feedback.


**Meeting Planning** The Meeting Planning evaluation
function also expects plans in JSON. Constraints are
also provided in structured JSON format. Unlike TravelPlanner and Trip Planning, Meeting Planning has
an optimization objective – the number of friends to
meet with. We modify the original evaluation evaluation function to score a proposed plan by how many
people that are not going to be met with; whether it
conflicts with the schedules of other people; whether
it includes meetings with the same person more than
once; whether any part of the plan conflict with other
parts; whether it follows the desired format as instructed. In Figures 23–24 we present the evaluation
function that implements the simple logic described
above as an example.


14


Evolving Deeper LLM Thinking


Figure 12 | Example Meeting Planning prompt and model response with parent solutions given (Part 1)



15


Evolving Deeper LLM Thinking


Figure 13 | Example Meeting Planning prompt and model response with parent solutions given (Part 2)



16


Evolving Deeper LLM Thinking


Figure 14 | Example Meeting Planning prompt and model response with parent solutions given (Part 3)



17


Evolving Deeper LLM Thinking


Figure 15 | Example Meeting Planning prompt and model response with parent solutions given (Part 4)



18


Evolving Deeper LLM Thinking


Figure 16 | Example Meeting Planning prompt and model response with parent solutions given (Part 5)



19


Evolving Deeper LLM Thinking


Figure 17 | Example TravelPlanner prompt and model response with parent solutions given (Part 1)



20


Evolving Deeper LLM Thinking


Figure 18 | Example TravelPlanner prompt and model response with parent solutions given (Part 2)



21


Evolving Deeper LLM Thinking


Figure 19 | Example TravelPlanner prompt and model response with parent solutions given (Part 3)



22


Evolving Deeper LLM Thinking


Figure 20 | Example TravelPlanner prompt and model response with parent solutions given (Part 4)



23


Evolving Deeper LLM Thinking


Figure 21 | Example TravelPlanner prompt and model response with parent solutions given (Part 5)



24


Evolving Deeper LLM Thinking


Figure 22 | Example TravelPlanner prompt and model response with parent solutions given (Part 6)



25


Evolving Deeper LLM Thinking





Figure 23 | The Meeting Planning evaluation function (part 1).



26


Evolving Deeper LLM Thinking


person = step . s p l i t ( " meet " ) [1]. s p l i t ( " for " ) [0]. s t r i p ()
i f person in met_with :
score −= 2
feedback . append( f " \ " { step }\" i s i n v a l i d because you would be meeting with { person }
more than once . " )
met_with [ person ] = 1
new_time = cur_time + datetime . timedelta (
minutes=friend_schedules [ person ] [ " meeting_time " ]
)


loc = friend_schedules [ person ] [ " location " ]
start_time = friend_schedules [ person ] [ " start_time "]
end_time = friend_schedules [ person ] [ " end_time "]
s t a r t _ t i m e _ s t r = start_time . s t r f t i m e ("%
end_time_str = end_time . s t r f t i m e ("%


i f cur_location == loc and cur_time >= start_time and new_time <= end_time :
score += 1
cur_time = new_time
else :
score −= 2
feedback . append( f " \ " { step }\" i s i n v a l i d because i t doesn ’ t match the schedule of {
person }, who w i l l be at { loc } from { s t a r t _ t i m e _ s t r } to { end_time_str } . " )
else :
r a i s e ValueError ( "Unknown plan format " )
except Exception :
score −= 10
feedback . append( f " \ " { step }\" i s i n v a l i d because the format doesn ’ t follow the examples
. " )


all_names = set ( friend_schedules . keys () )
not_met_with = ", " . join ( l i s t ( all_names −set ( met_with . keys () ) ) )


return score, feedback


Figure 24 | The Meeting Planning evaluation function (part 2).



27


Evolving Deeper LLM Thinking


### **B. Data Splits**

**TravelPlanner** TravelPlanner has 45 training tasks,
180 validation tasks, and 1,000 test tasks in the original benchmark.


**Natural** **Plan** **–** **Trip** **Planning** The Trip Planning
benchmakr has 1,600 example tasks. There are eight
different difficulty levels, ranging from 3 to 10 cities.
Each difficulty level has 200 examples. We split the
dataset into validation and test sets by putting the
first 40 examples from each difficulty level into validation, and the last 160 examples into test, giving
320 examples in validation (which we used for prompt
development) and 1,280 for test. In Figure 4, we show
the performance at each difficulty level.


**Natural Plan – Meeting Planning** The Meeting Planning benchmark has 1,000 example tasks. There are
ten different difficulty levels, ranging from meeting
one to ten different friends. Each difficulty level has
100 examples. We split the dataset into validation and
test sets by putting the first 50 examples from each difficulty level into validation, and the last 50 examples
into test, giving 500 examples in validation (which
we used for prompt development) and 500 for test. In
Figure 5, we show the performance at difficulty level.

### **C. GPT Results**


Table 7 presents the results of Mind Evolution using
GPT-4o-mini with the same sets of prompts. Specifically, with 1-pass inference, GPT-4o-mini also struggles at planning tasks, achieving 0% on TravelPlanner,
9.1% success rate on Trip Planning, and 20.2% success rate on Meeting Planning. Again, Mind Evolution
significantly improves the performance by over 100%
relatively across different benchmarks.

|Col1|Success Rate|
|---|---|
|**TravelPlanner [42]**<br>**Natural Plan [47] Trip Planning**<br>**Natural Plan [47] Meeting Planning**|79_._4%<br>48_._1%<br>86_._4%|



Table 7 | Mind Evolution with GPT-4o-Mini results on
validation sets.

### **D. Model Pricing and API Cost Curves**


Table 8 shows the API pricing of different models used
in our evaluation (Tables 2), at the time of writing
(October 2024).


Figure 25 gives insight into the scaling properties of
the various strategies in terms of their API cost, which



Model Input Token Output Token
Gemini 1.5 Flash $0 _._ 075/M $0 _._ 30/M
Gemini 1.5 Pro $1 _._ 25/M $5 _._ 00/M
GPT-4o-Mini $0 _._ 15 $0 _._ 60
OpenAI o1-preview $15 _._ 00/M $60 _._ 00/M


Table 8 | Pricing at the time of writing (October 2024).
These differences serve as a proxy for real computational cost differences among models.


is also a linear combination of the input token counts
and the output token counts, weighted by base rate
(Table 8).

### **E. Additional Examples**


In addition to Table 3, we present qualitative examples
of TravelPlanner and Meeting Planning in Table 9 and
Table 10, respectively.


28


100


80


60


40


20


0



|Mind Evolution (ours)<br>Seq. Revisions+<br>Best-of-N|Col2|Col3|
|---|---|---|
|Mind Evolution (ours)<br>Seq. Revisions+<br>Best-of-N|Mind Evolution (ours)<br>Seq. Revisions+<br>Best-of-N||
|Mind Evolution (ours)<br>Seq. Revisions+<br>Best-of-N|Mind Evolution (ours)<br>Seq. Revisions+<br>Best-of-N|Mind Evolution (ours)<br>Seq. Revisions+<br>Best-of-N|


0 1 2 3 4 5 6
API Cost on each task, USD (Oct 2024)



Evolving Deeper LLM Thinking

|Mind Evolution (ours)<br>Seq. Revisions+<br>Best-of-N|Col2|Col3|
|---|---|---|
|Mind Evolution (ours)<br>Seq. Revisions+<br>Best-of-N|Mind Evolution (ours)<br>Seq. Revisions+<br>Best-of-N|Mind Evolution (ours)<br>Seq. Revisions+<br>Best-of-N|



0 1 2 3 4 5 6
API Cost on each task, USD (Oct 2024)



100


80


60


40


20


0



|Mind Evolution (ours)<br>Seq. Revisions+<br>Best-of-N|Col2|Col3|
|---|---|---|
|Mind Evolution (ours)<br>Seq. Revisions+<br>Best-of-N|Mind Evolution (ours)<br>Seq. Revisions+<br>Best-of-N||
|Mind Evolution (ours)<br>Seq. Revisions+<br>Best-of-N|Mind Evolution (ours)<br>Seq. Revisions+<br>Best-of-N|Mind Evolution (ours)<br>Seq. Revisions+<br>Best-of-N|


0 1 2 3 4 5 6
API Cost on each task, USD (Oct 2024)



100


80


60


40


20


0



(a) **TravelPlanner**



(b) **Trip Planning**



(c) **Meeting Planning**



Figure 25 | **API cost per task (Oct 2024) vs.** **Success Rate** on the validation sets with Gemini 1.5 Flash. API
cost is also a linear combination of input token counts and output token counts. Note that Sequential-Revision+
curves are cut short. As the conversations can run up to 80 turns, it usually consumes a lot more tokens than
the other methods.


29


Evolving Deeper LLM Thinking


Q: Could you construct a 3-day journey for two people from Chicago to Albany that takes place from March 22nd to
March 24th, 2022? Our budget is $2,300. We require accommodations that allow smoking and should ideally be
entire rooms. We will not be self-driving during this trip. On the subject of cuisine, we’re open to any suggestions you
might have.


[Transportation Options] Taxi: N/A, Self-Driving: N/A, Flights: F3732604 **[...]**

[Accommodation Options in Albany] 2Br Union square Newly furnished (minimum 30 nights), **[...]**

**[...]**


**Method** **Answer**
1-Pass [Day 1] city: ’from Chicago to Albany’, accommodation: ’Spacious room with huge bay
window & natural light, Albany’, attraction: ’-’, breakfast: ’-’, dinner: ’Kaiser, Albany’,
lunch: ’-’, transportation’: ’Flight Number: F3983351, from Chicago to Albany, Departure
Time: 20:20, Arrival Time: 23:04’ [Day 2] city: ’Albany’, accommodation: ’Spacious room
with huge bay window & natural light, Albany’, attraction: ’Albany Pine Bush Preserve,
Albany;New York State Museum, Albany;’, breakfast: ’Desi Villa, Albany’, lunch: ’Just
Parkash, Albany’, dinner: ’Kaiser, Albany’, ’transportation’: ’-’ [Day 3] city: ’from Albany
to Chicago’, accommodation: ’-’, attraction: ’Hear about Here, Albany;’, breakfast: ’Cafe
Coffee Day The Square, Albany’, lunch: ’PiccoLicko, Albany’, dinner: ’StarvinMarvin, [´] Albany’,
transportation: ’Flight Number: F3813300, from Albany to Chicago, Departure Time: 16:40,
Arrival Time: 17:52’ �The total cost exceeds the budget of $2300 by $114, [...]
Best-of-N [Day 1] city: ’from Chicago to Albany’, accommodation: ’Mid Town East Side Apartment,
Albany’, attraction: ’New York State Museum, Albany’, breakfast: ’-’, dinner: ’Kaiser,
Albany’, lunch: ’-’, transportation’: ’Taxi, from Chicago to Albany, duration: 12 hours 53
mins, distance: 723 km, cost: 532’ [Day 2] city: ’Albany’, accommodation: ’Mid Town East
Side Apartment, Albany’, attraction: ’Albany Institute of History & Art, Albany’, breakfast:
’Echoes Satyaniketan, Albany’, lunch: ’Cafe Coffee Day The Square, Albany’, dinner: ’Urban
Punjab, Albany’, ’transportation’: ’-’ [Day 3] city: ’from Albany to Chicago’, accommodation:
’-’, attraction: ’Historic Cherry Hill, Albany’, breakfast: ’Just Parkash, Albany’, lunch: ’BKś
The Juice Bar, Albany’, dinner: ’-’, transportation: ’Flight Number: F4008387, from Albany
to Chicago, Departure Time: 05:05, Arrival Time: 06:11’ �Taxi from Chicago to Albany on
day 1 is not a valid option, [...]
Sequential Revisions+ [Day 1] city: ’from Chicago to Albany’, accommodation: ’2Br Union square Newly furnished’,
Albany’, attraction: ’-’, breakfast: ’-’, dinner: ’-’, lunch: ’-’, transportation’: ’Flight Number:
F3983350, from Chicago to Albany, Departure Time: 14:29, Arrival Time: 17:03’ [Day 2] city:
’Albany’, accommodation: ’2Br Union square Newly furnished’, attraction: ’New York State
Museum, Albany;Albany Pine Bush Preserve, Albany’, breakfast: ’Cafe Coffee Day, Albany’,
lunch: ’PiccoLicko, Albany’, dinner: ’Kaiser, Albany’, ’transportation’: ’-’ [Day 3] city: ’from
Albany to Chicago’, accommodation: ’-’, attraction: ’The McPherson Legacy to the City of
Albany             - Robert Burns Statue, Albany’, breakfast: ’-’, lunch: ’-’, dinner: ’-’, transportation:
’Flight Number: F3732604, from Albany to Chicago, Departure Time: 05:53, Arrival Time:
07:24’ �’2Br Union square Newly furnished’ requires staying at least 30 nights, [...]
Mind Evolution (ours) [Day 1] city: ’from Chicago to Albany’, accommodation: ’Mid Town East Side Apartment,
Albany’, attraction: ’-’, breakfast: ’-’, dinner: ’-’, lunch: ’-’, transportation’: ’Flight Number:
F3983350, from Chicago to Albany, Departure Time: 14:29, Arrival Time: 17:03’ [Day 2] city:
’Albany’, accommodation: ’Mid Town East Side Apartment, Albany’, attraction: ’Albany
Institute of History & Art, Albany’, breakfast: ’StarvinMarvin, [´] Albany’, lunch: ’Cafe Coffee
Day The Square, Albany’, dinner: ’PiccoLicko, Albany’, ’transportation’: ’-’ [Day 3] city:
’from Albany to Chicago’, accommodation: ’-’, attraction: ’The McPherson Legacy to the City
of Albany               - Robert Burns Statue, Albany’, breakfast: ’-’, lunch: ’-’, dinner: ’-’, transportation:
’Flight Number: F4008387, from Albany to Chicago, Departure Time: 05:05, Arrival Time:
06:11’              

Table 9 | An example TravelPlanner task and the solutions proposed by Mind Evolution and the baselines
method.


30


Evolving Deeper LLM Thinking


Q: You are visiting San Francisco for the day and want to meet as many friends as possible. Solve the problem by
considering various different schedules and picking the best one to optimize your goals.


Travel distances (in minutes):
The Castro to Sunset District: 17. The Castro to Presidio: 20. The Castro to Bayview: 19. The Castro to Chinatown:
20. The Castro to Mission District: 7. Sunset District to The Castro: 17. Sunset District to Presidio: 16. Sunset
District to Bayview: 22. Sunset District to Chinatown: 30. Sunset District to Mission District: 24. Presidio to The
Castro: 21. Presidio to Sunset District: 15. Presidio to Bayview: 31. Presidio to Chinatown: 21. Presidio to Mission
District: 26. Bayview to The Castro: 20. Bayview to Sunset District: 23. Bayview to Presidio: 31. Bayview to
Chinatown: 18. Bayview to Mission District: 13. Chinatown to The Castro: 22. Chinatown to Sunset District: 29.
Chinatown to Presidio: 19. Chinatown to Bayview: 22. Chinatown to Mission District: 18. Mission District to The
Castro: 7. Mission District to Sunset District: 24. Mission District to Presidio: 25. Mission District to Bayview: 15.
Mission District to Chinatown: 16.


CONSTRAINTS:
You arrive at The Castro at 9:00AM. Michelle will be at Sunset District from 6:30PM to 8:30PM. You’d like to meet
Michelle for a minimum of 120 minutes. Amanda will be at Presidio from 9:30PM to 10:00PM. You’d like to meet
Amanda for a minimum of 30 minutes. Sandra will be at Bayview from 10:00AM to 2:30PM. You’d like to meet
Sandra for a minimum of 90 minutes. Kevin will be at Chinatown from 6:15PM to 7:15PM. You’d like to meet Kevin
for a minimum of 45 minutes. Mark will be at Mission District from 12:30PM to 1:45PM. You’d like to meet Mark for
a minimum of 75 minutes.


**Method** **Answer**
1-Pass [’You start at The Castro at 9:00AM’, ’You travel to Bayview in 19 minutes and arrive at
9:19AM’, ’You meet Sandra for 90 minutes from 10:00AM to 11:30AM’, ’You travel to
Mission District in 13 minutes and arrive at 11:43AM’, ’You meet Mark for 75 minutes from
12:30PM to 1:45PM’, ’You travel to Sunset District in 24 minutes and arrive at 2:09PM’,
’You wait until 6:30PM’, ’You meet Michelle for 120 minutes from 6:30PM to 8:30PM’, ’You
travel to Chinatown in 30 minutes and arrive at 8:30PM’, ’You wait until 6:15PM’, ’You meet
Kevin for 45 minutes from 6:15PM to 7:00PM’, ’You travel to Presidio in 19 minutes and
arrive at 7:19PM’, ’You wait until 9:30PM’, ’You meet Amanda for 30 minutes from 9:30PM
to 10:00PM’] �’Meeting Mark for 75 minutes from 12:30PM to 1:45PM’ doesn [´] t match the
schedule of Mark, who will be at Mission District from 12:30PM to 01:45PM **[...]**
Best-of-N [’You start at The Castro at 9:00AM’, ’You travel to Bayview in 19 minutes and arrive at
9:19AM’, ’You wait until 10:00AM’, ’You meet Sandra for 90 minutes from 10:00AM to
11:30AM’, ’You travel to Mission District in 13 minutes and arrive at 11:43AM’, ’You wait
until 12:30PM’, ’You meet Mark for 75 minutes from 12:30PM to 1:45PM’, ’You travel to
Sunset District in 24 minutes and arrive at 2:09PM’, ’You wait until 6:30PM’, ’You meet
Michelle for 120 minutes from 6:30PM to 8:30PM’, ’You travel to Chinatown in 30 minutes
and arrive at 8:30PM ’, ’You wait until 6:15PM’, ’You meet Kevin for 45 minutes from
6:15PM to 7:00PM’, ’You travel to Presidio in 19 minutes and arrive at 7:19PM’, ’You wait
until 9:30PM’, ’You meet Amanda for 30 minutes from 9:30PM to 10:00PM’] �’Waiting
until 6:15PM’ is invalid because the previous step ends after 06:15PM.
Sequential Revisions+ [’You start at The Castro at 9:00AM’, ’You travel to Mission District in 7 minutes and arrive
at 9:07AM’, ’You wait until 12:30PM’, ’You meet Mark for 30 minutes from 12:30PM to
1:00PM’, ’You travel to Sunset District in 17 minutes and arrive at 1:17PM’, ’You wait until
6:30PM’, ’You meet Michelle for 30 minutes from 6:30PM to 7:00PM’, ’You travel to Presidio
in 16 minutes and arrive at 7:16PM’, ’You wait until 9:30PM’, ’You meet Amanda for 30
minutes from 9:30PM to 10:00PM’] Not meeting with Kevin and Sandra.
Mind Evolution (ours) [’You start at The Castro at 9:00AM’, ’You travel to Bayview in 19 minutes and arrive at
9:19AM’, ’You wait until 10:00AM’, ’You meet Sandra for 90 minutes from 10:00AM to
11:30AM’, ’You travel to Mission District in 13 minutes and arrive at 11:43AM’, ’You wait
until 12:30PM’, ’You meet Mark for 75 minutes from 12:30PM to 1:45PM’, ’You travel to
Chinatown in 16 minutes and arrive at 2:01PM’, ’You wait until 6:15PM’, ’You meet Kevin
for 45 minutes from 6:15PM to 7:00PM’, ’You travel to Presidio in 19 minutes and arrive
at 7:19PM’, ’You wait until 9:30PM’, ’You meet Amanda for 30 minutes from 9:30PM to
10:00PM’] �Not meeting with Michelle, but this is a best possible plan.


Table 10 | An example Meeting Planning task and the solutions proposed by Mind Evolution and the baselines
method.


31


Evolving Deeper LLM Thinking


### **F. Additional Details for StegPoet**

The prompt design used for StegPoet is given in Figure 26.


**StegPoet Evaluation** Each proposed solution should
contain a cipher and text component. The first step
is to calculate what is encoded in the text by finding all the cipher strings; this is done via simple
capitalization-agnostic character-matches. We refer
to the actual encoded string as _𝑀_ [′] . If _𝑀_ = _𝑀_ [′] the
problem is solved correctly. The numeric evaluation
of a proposed solution is computed as follows:


1. Invalid if the text or cipher component cannot be
parsed or violates constraints.


(a) Words in the cipher cannot be subsets of each
other (e.g., origin and original).
(b) Words in the cipher cannot be repeated.

(c) Words in the cipher should be at least 4 characters long.
(d) Words in the cipher should contain only alphabetic characters.


2. What is the first position, _𝑖_, in which _𝑀𝑖_ ≠ _𝑀𝑖_ [′][?] [This]
is the integer part of the score.
3. Compute the Levenshtein distance between _𝑀_ and
_𝑀_ [′] . Levenshtein distance is often used in information theory and linguistics to measure the difference
between two sequences [2]. This is scaled between
(0,1) and added to the integer component above.


Additionally, textual feedback, without numeric
penalties, is also provided in the revision request made
to the LLM.


1. A clearly marked list of what _𝑀_ [′] was found.
2. A list of number mappings missing from the cipher,
or unnecessary numbers specified in the cipher.



3. If a word appears an incorrect number of times (too
few or too many) in the text, it is indicated, along
with the error.
4. An annotated copy of the text is returned. The
annotations indicate where the cipher-keywords
were found (they are shown asterisked), and the
first error is indicated.
5. If the text encodes the cipher correctly, but also
encodes extra words, that is indicated.
6. If everything in _𝑀_ [′] is correct, but | _𝑀_ [′] | _<_ | _𝑀_ |, it is
indicated as such.


For this task, we experimented with many different
genre forms (poetry, short-story fiction, essay, monologue, etc.), as well as inspirations from contemporary
to classic writers.


32


Evolving Deeper LLM Thinking


For this task, you are the world’s best poet, linguist and hidden code creator!

You strive to write in the style of shel silverstein.

I would like you to come up with a 1:1 mapping from numbers to words for the list of numbers

demarcated by <HIDDEN-MESSAGE START> and <HIDDEN-MESSAGE END>.

Then, cleverly hide the numbers in an poem about the fun of walking.


SPECIFICS:

- [You] [can] [choose] [the] [words.]

- [A] [number] [cannot] [have] [more] [than] [one] [word] [assigned] [to] [it.]

- [A] [word] [cannot] [be] [used] [twice] [in] [the] [mapping.]

- [Create] [a] [substitution-ENCODING-CIPHER] [for] [each] [number] [and] [then] [put]
those words into the poem in the order that they appear in the hidden message.

- [If] [you] [use] [a] [word] [in] [the] [ENCODING-CIPHER] [in] [the] [poem,] [then] [it] [can] [only] [be] [used]
to encode a number. Nowhere else. Otherwise it will be mistaken as part of the message.

- [The] [numbers] [must] [be] [encoded] [in] [the] [order] [that] [they] [appear] [in] [the] [hidden] [message.]


<HIDDEN-MESSAGE START>

90 70 50 40 40 10 50 80 70 900 50 30

<HIDDEN-MESSAGE END>


Here are some guidelines to follow.

- [The] [poem] [must] [NOT] [contain] [any] [numbers.]

- [Numbers] [should] [not] [be] [encoded] [with] [a] [word] [or] [words] [that] [directly] [represent] [the] [number.]
For example, DO NOT represent "2" : "Dual". Similarly, "4" : "four" is not acceptable.

- [In] [general,] [numbers] [should] [not] [be] [represented] [by] [words] [that] [are] [numeric] [in] [nature.]

- [Numbers] [should] [not] [be] [represented] [by] [hyphenated] [words] [or] [using] [any]
other non alphabetic character. They should be encoded with single words.

- [The] [words] [used] [for] [ciphers] [should] [not] [be] [subsets] [of] [each] [other.]

- [Your] [poem] [should] [make] [sense,] [be] [understandable,] [and] [be] [in] [the] [style] [of] [shel] [silverstein.]

- [Your] [poem] [should] [not] [just] [be] [a] [list] [of] [words] [that] [look] [like] [jibberish.]
Try to have at least 4 words between your cipher words.


Absolutely crucial:

- [Important] [--] [make] [sure] [that] [each] [number] [in] [the] [hidden] [message] [is] [represented] [in] [the] [poem.]

- [DO] [NOT] [SKIP] [ANY] [numbers.] [The] [numbers] [must] [be] [encoded] [in] [the] [SAME] [order] [as] [they] [are] [given] [to] [you.]

- [PRECISION] [IS] [OF] [THE] [UTMOST] [IMPORTANCE.]

- [Note] [that] [we] [did] [not] [use] [common] [words] [such] [as] [’and’] [and] [’the’] [etc.] [to] [encode] [the] [numbers,]
as such words may be difficult to use only at the specific times

required to encode the hidden-message.

- [You] [should] not use common words to encode the numbers in the cipher.

- [The] [words] [you] [use] [in] [the] [cipher] [should] [be] [at] [least] [4] [characters] [long.]

- [Though] [you] [may] [have] [to] [use] [the] [same] [word] [multiple] [times,] [try] [to] [avoid] [using]
the same sentence or phrase multiple times.


Please begin and end your poem with <POEM START> and <POEM END>.


FORMATTING INSTRUCTIONS:

- [Please] [begin] [your] [answer] [by] [providing] [the] [mapping] [from] [the] [numbers] [in] [the] [hidden] [message]
to the words you select.

- [I’ve] [included] [3] [examples] [of] [successful] [ENCODING-CIPHERs] [below.]

- [VERY,] [VERY] [IMPORTANT:] You should come up with your own creative ENCODING-CIPHERs!

- [Note] [the] [semicolon] [that] [is] [required] [after] [each] [cipher] [entry] [in] [the] [ENCODING-CIPHER] [section.]
This must be present!


EXAMPLE #1:


Can you please hide the message demarcated by <HIDDEN-MESSAGE START> and <HIDDEN-MESSAGE END>

into a poem about computers.


<HIDDEN-MESSAGE START>

77 22 33 40 44 77 50 66 55 5 40 40 3 70 8

<HIDDEN-MESSAGE END>


<ENCODING-CIPHER START>

"22" : "computers";

"33" : "become";

"44" : "vital";

"55" : "them";

"66" : "need";

"77" : "everyday";

"40" : "more";

"50" : "need";

"70" : "certain";

"3" : "grow";

"5" : "exist";

"8" : "future";

<ENCODING-CIPHER END>


<POEM START>

Everyday, computers become more vital to our lives.

Everyday, we need them to exist more and more.

That will grow, for certain, in the future.

<POEM END>


Figure 26 | An example initial prompt for StegPoet. Only 1 of 3 examples is shown.



33


