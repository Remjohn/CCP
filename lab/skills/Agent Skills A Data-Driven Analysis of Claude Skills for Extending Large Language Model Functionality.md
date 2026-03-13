## **Agent Skills: A Data-Driven Analysis of Claude Skills for Extending Large** **Language Model Functionality**

**George Ling** **[1]** **, Shanshan Zhong** **[2]** **, Richard Huang** **[1]**

1Bosch Research, 2Carnegie Mellon University



**Abstract**


Agent skills extend large language model
(LLM) agents with reusable, program-like modules that define triggering conditions, procedural logic, and tool interactions. As these
skills proliferate in public marketplaces, it is
unclear what types are available, how users
adopt them, and what risks they pose. To
answer these questions, we conduct a largescale, data-driven analysis of 40,285 publicly
listed skills from a major marketplace. Our
results show that skill publication tends to occur in short bursts that track shifts in community attention. We also find that skill content
is highly concentrated in software engineering
workflows, while information retrieval and content creation account for a substantial share of
adoption. Beyond content trends, we uncover a
pronounced supply-demand imbalance across
categories, and we show that most skills remain within typical prompt budgets despite a
heavy-tailed length distribution. Finally, we
observe strong ecosystem homogeneity, with
widespread intent-level redundancy, and we
identify non-trivial safety risks, including skills
that enable state-changing or system-level actions. Overall, our findings provide a quantitative snapshot of agent skills as an emerging
infrastructure layer for agents and inform future work on skill reuse, standardization, and
safety-aware design.


**1** **Introduction**


Large language model (LLM) agents have emerged
as a powerful paradigm for addressing complex,
multi-step tasks that require reasoning, tool use,
and interaction with external environments (Yao
et al., 2022; Wang et al., 2024). Rather than relying on a single prompt-response interaction, agents
operate over extended horizons: they interpret user
goals, decompose them into sub-tasks, and coordinate actions across diverse tools, data sources,
and intermediate states (Shinn et al., 2023; Wang


|0<br>0<br>0<br>0<br>0<br>0|Col2|Col3|Col4|Col5|Col6|Col7|
|---|---|---|---|---|---|---|
|0<br>0<br>0<br>0<br>0<br>0|~~Cu~~|~~mulative S~~|~~ ills~~||||
|0<br>0<br>0<br>0<br>0<br>0|<br>Op|<br>enClaw Cu|<br> mulative Sta|rs||4<br>8<br>1<br>1<br>2<br>0|
|0<br>0<br>0<br>0<br>0<br>0|||||||
|0<br>0<br>0<br>0<br>0<br>0|||||||
|0<br>0<br>0<br>0<br>0<br>0|||||||
|0<br>0<br>0<br>0<br>0<br>0|||||||



Figure 1: **Growth trend of agent skills** . According to
[the well-known agent skills platform skills.sh, the num-](https://skill.sh)
ber of recorded skills experienced rapid growth from
mid-January to early February 2026, exceeding 40,000
by early February. During the same period, the popular open-source skills application OpenClaw (openclaw
Community, 2026) saw a sharp surge in GitHub stars,
reaching over 25,000 stars in a single day at the end of
January, followed by a gradual decline, with the total
number of stars exceeding 170k.


et al., 2023; Sapkota et al., 2025). This agentic
execution model has enabled a growing range of
applications, from software development and data
analysis to personal assistance and workflow automation (Wang et al., 2024).
As agent-based systems scale in both complexity and deployment, new challenges arise around
reliability, reuse, and maintainability (Liu et al.,
2026a; Cemri et al., 2025; Raheem and Hossain,
2025). Many agent behaviors recur across tasks
and users, yet are repeatedly re-specified through
prompts or handcrafted control logic (Jin et al.,
2026; Liu et al., 2025). This has motivated the
emergence of agent skills (openclaw Community,
2026; Anthropic, 2025). The ecosystem around
these skills has expanded rapidly in recent months,
as reflected in Figure 1. This growth motivates
a closer look at what skills exist, how they are
adopted, and what risks they may introduce.
**What** **are** **agent** **skills?** Agent skills have recently emerged as an abstraction for structuring
reusable and scalable agent behaviors (Anthropic,
2025; Wu and Zhang, 2026; Lee, 2025). The con












26-01-16 26-01-20 26-01-24 26-01-28 26-02-01 26-02-05



1


cept has been systematized and popularized by Anthropic in the context of the Claude agent framework (Anthropic, 2025), where skills are sometimes referred to as _Claude Skills_ or _Claude agent_
_skills_ . An agent skill can be defined as a reusable,
plug-and-play module that specifies when the skill
should be invoked and how the corresponding subtask should be carried out, typically in a form
that can be shared, versioned, and composed. In
practical implementations, a skill often combines
lightweight metadata that supports discovery and
selection with executable instructions and supporting resources such as files, scripts, and tool configurations (Anthropic, 2025). Appendix A provides
a concrete example of skill structure.
**Why do agents need skills?** Agent-based systems often revisit similar subtasks, such as data
retrieval, information extraction, code modification, etc. Without explicit abstractions, these recurring behaviors must be specified repeatedly, either
through prompts or through ad hoc control logic.
This repetition increases prompt overhead, makes
behavior brittle under small context changes, and
complicates maintenance of shared procedures (Jin
et al., 2026). Agent skills address these issues by
packaging reusable behaviors into modular units
that capture task knowledge, procedural logic, and
tool use patterns. Because skills can be reused and
composed, they improve behavioral consistency
and reduce prompt complexity, making agent capabilities easier to extend and control. Shared skill
libraries also support standardization and continuous refinement across applications.
**How** **are** **agent** **skills** **used** **in** **practice?** In
real systems, skills are typically organized as selfcontained modules that an agent can select and
execute during task solving. A common pattern is
to load eligible skills into the system prompt as a
compact list of metadata with names and descriptions; the agent then selects a skill based on the
user request and follows the skill-defined instructions, issuing tool calls as needed. Appendix A
provides a concrete example (Figure 11) that illustrates how an agent uses different skills to solve
user questions.
Taken together, these observations suggest that
agent skills are growing quickly, but their functions
and potential impacts vary widely. This makes it
important to characterize what skills exist, how
they are used, and what risks they may introduce.
In this paper, we present a large-scale, data-driven
measurement of the emerging agent skills ecosys


tem. Using a corpus collected from a public skill
platform, we analyze the following aspects:

- **Growth trends** in Section 2: we quantify publication over time and show rapid, bursty growth.

- **Skill length and redundancy** in Section 3: we
measure prompt length and show a heavy-tailed
distribution, while most skills stay within typical
prompt budgets. We also find that near-duplicate
listings are common.

- **Skill** **usage** **patterns** in Section 4: we classify
skills into a taxonomy with 6 major categories
and 20 sub-categories, and we show strong concentration in software engineering workflows.
We further identify clear gaps between what is
published and what users install.

- **Safety risks** in Section 5: we audit skills and find
that most are low risk, while a non-trivial share
enables state-changing actions.
Our results point to several open problems. First,
the supply–demand gaps and high redundancy call
for better skill discovery, de-duplication, and quality signals. Second, the presence of action-enabling
skills motivates safety-aware design, including
clearer permission models, stronger sandboxing,
and more transparent risk labeling.


**2** **Skill Data and Growth Trends**


In this section, we introduce our skills dataset
and summarizes how the agent-skill ecosystem has
grown over time. We first describe how we collect
skills and their metadata, and then report statistics
that capture publication and adoption patterns.


**2.1** **Data Collection**


We construct our dataset by crawling agent skills
[listed on the public marketplace skills.sh.](https://skill.sh) For
each skill, we extract a lightweight set of metadata describing the skill, its hosting location, the
date when it first appeared on the marketplace, and
how widely it has been installed. Specifically, each
record includes the skill name, a repository field
that points to the hosted skill file, first_seen,
which records the date when the skill was first up[loaded to skills.sh,](https://skill.sh) and installed_on, which
reports per-platform installation counts across supported platforms.
We store each skill as a SKILL.md and a JSONlike object with the following structure:


{
"name": [SKILL NAME],
"repository": [REPOSITORY LINK],
"first_seen": [DD/MM/YY],



2


"installed_on": [

{"platform": "claude-code", "installs":
_�→_ [NUMBER OF INSTALL]},
{"platform": "codex", "installs": [NUMBER OF
_�→_ INSTALL]},
...
]
}


We finalize data collection on February 5, 2026,
yielding **40,285** skill metadata records. Unless otherwise stated, this snapshot underlies all analyses in
Sections 2.2–5. All measurements are based solely
on publicly accessible content; we avoid sensitive
attributions about individual creators and report
results only in aggregate.


**2.2** **Skill Growth Trends**


We study skill growth trends using the first_seen
field in Section 2.1, which records when a skill first
[appears on skills.sh.](https://skill.sh) To capture a parallel signal
of community attention, we also track the popularity of OpenClaw (openclaw Community, 2026)
by querying its GitHub star history via the GitHub
GraphQL API (api.github.com/graphql). Figure 1 plots the cumulative number of listed skills
and the cumulative number of OpenClaw stars.


**Growth is rapid and bursty.** The marketplace
grows from 2,179 skills on January 16, 2026 to
40,285 skills on February 5, 2026, a net increase
of 38,106 skills in 20 days. This corresponds to
an 18.5 _×_ increase and an average multiplicative
growth rate of about 15.7% per day. Despite a
mean inflow of 1,918 skills per day, arrivals are
concentrated in short spikes. The largest spike
occurs on January 25, 2026, when 8,857 skills are
added in a single day. This accounts for 23.2%
of all new skills in the window. At the weekly
level, the week centered on January 25 contributes
19,259 skills, or 47.8% of the full snapshot.


**Growth** **aligns** **with** **an** **application-level** **popu-**
**larity** **signal.** OpenClaw exhibits a concurrent
popularity shock. Daily new stars rise from the
hundreds in mid-January to 10,543 on January 25,
then peak at 25,432 on January 26, which is 2.4 _×_
the previous day. After the peak, daily gains decline
into early February. For example, OpenClaw gains
1,718 new stars on February 5, which coincides
with the slowdown in new listings. Taken together,
the synchronized spikes suggest a shared driver.
A wave of public attention likely encouraged both
skill publication and exploration of skill-based tooling. While GitHub stars are an imperfect proxy for


|Col1|Col2|Col3|Col4|Col5|Col6|Col7|Col8|Col9|Col10|Col11|Col12|Col13|Col14|Col15|Col16|Col17|Col18|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|||||||||||||||||||
||||||||||||||||50%<br>80%<br>|||
|||||||||||||||||||
|||||||||||||||||||
||||||||||||||||~~95%~~<br>98%|||
|||||||||||||||||||
|||||||||||||||||||
|||||||||||||||||||
|||||||||||||||||||
|||||||||||||||||||



Figure 2: **Token-count** **distribution** **of** **agent** **skills.**
The distribution is heavy-tailed: the median skill contains 1,414 tokens (mean: 1,895). 90% of skills are no
longer than 3,935 tokens and 99% are no longer than
9,253 tokens. A small fraction are exceptionally long,
with a maximum of 116,239 tokens.


real usage, their synchronized dynamics with marketplace listings provide evidence that rapid supply
growth coincides with strong community interest.


**3** **Skill Length and Redundancy**


This section summarizes skill content and usage at
scale. We first analyze skill length, and then report
intent-level redundancy.


**3.1** **Skill Length Characteristics**


We measure skill length by tokenizing each
SKILL.md and counting tokens. For every
skill record in Section 2.1, we consistently use
tiktoken (OpenAI, 2026) with the o200k_base
encoding. This approach allows token counts to
serve as a straightforward proxy for prompt budget
and inference cost.


**Typical skills are short.** Figure 2 shows a pronounced heavy-tailed distribution, but most skills
are still compact. The median length is 1,414 tokens and the mean is 1,895 tokens, indicating that
a typical skill fits comfortably alongside planning
context and tool schemas. Across quantiles, length
is rarely a binding constraint: 80% and 95% of
skills are within 2,955 and 5,077 tokens, and 90%
and 99% remain below 3,935 and 9,253 tokens.
Meanwhile, the standard deviation of 2,025 tokens
highlights substantial dispersion, even though the
central mass is short.


**A few skills are long due to the inclusion of mul-**
**tiple components.** This dispersion is driven by a
small set of extreme outliers. The top 1% of skills
exceed 9,253 tokens, and the maximum reaches
116,239 tokens, which can consume prompt budgets and hinder reliable selection and auditing when



6000


4000


2000


0



0 1000 2000 3000 4000 5000 6000 7000
Token Count



3


skill-creator







Figure 3: **Name based redundancy distribution.** Skills
are grouped by normalized names using case insensitive
matching after removing special characters. We report
the fraction of skills that appear _n_ times, denoted as _n×_ .
Skills that appear once account for 53.7%, while skills
that appear more than once account for 46.3%. The
names of the 30 most redundant skills under this metric
are listed in Appendix Figure 4.


loaded in full. Manual inspection suggests that
many of these long skills consolidate multiple components into a single file, including extended documentation, large code blocks, and reusable template collections. This pattern indicates that, while
most skills support direct in-context use, a minority
behave like libraries and may benefit from modularization or retrieval-based loading so only the
relevant portions are brought into context.


**3.2** **Intent-level Redundancy Analysis**


As the agent skills ecosystem grows, identical
user intents are frequently published more than
once, either by independent developers or through
template-driven generation. Moderate repetition
can be beneficial when it produces meaningfully
improved variants, such as stronger safety checks,
broader tool coverage, or clearer documentation.
However, when most copies differ only in wording,
marketplace volume rises without a corresponding
increase in capability diversity. We therefore quantify redundancy as the frequency with which the
same intent is re-listed in the corpus.


**Redundancy** **measuring.** We estimate redundancy with two signals. First, we apply namebased exact matching. We lowercase skill
names, remove special characters, and group
skills that share the same normalized name. Second, we apply semantic matching. We encode
Name:[NAME] + Description:[DESCRIPTION]
with BAAI/bge-m3 (Chen et al., 2024), and analyze
nearest neighbor similarity together with t-SNE visualizations. In this marketplace, descriptions are
often short, noisy, and template derived, so seman


|Col1|91<br>83<br>82<br>80<br>78<br>69<br>67<br>65<br>64|103<br>101|162|Col5|251|
|---|---|---|---|---|---|
|~~ 35~~<br>~~ 35~~<br>~~ 4~~<br> <br> <br> <br> <br>|~~ 2~~<br>~~ 43~~<br>~~ 43~~<br>~~ 43~~<br>~~ 44~~<br>~~ 45~~<br>~~ 48~~<br>~~ 48~~<br>~~ 50~~<br>~~ 50~~<br>~~ 58~~<br>~~ 59~~<br>~~ 60~~<br>~~ 61~~<br>~~ 63~~<br>|||||


Number of Duplicates


Figure 4: **Top** **30** **redundant** **skills** **by** **name** **based**
**matching.** We rank skills by the number of listings
that share the same normalized name, using the exact
matching procedure in Section 3.2. This figure lists
the 30 most frequently repeated skill names and their
repetition counts.


tically similar embeddings do not reliably separate
true duplicates from loosely related skills. For this
reason, we use strict name matching for the main
results and report the embedding analysis in Appendix B.


**Nearly half of listings are duplicates.** Figure 3
shows that unique entries only slightly outnumber repeated ones. Under strict exact matching,
53.7% of skills appear once, while 46.3% share a
normalized name with at least one other listing. Duplication is also concentrated. Pairs are common,
with 2 _×_ groups contributing 18.7% of the corpus.
Higher multiplicities still account for a nontrivial
share: 5 _×_ to 9 _×_ groups contribute 14.3%, and 10 _×_
to 49 _×_ groups contribute 8.8%. A small number
of names appear more than 100 times, which is
consistent with repeated reposting or automated
publication from shared templates. For concreteness, we provide the 30 most redundant skill names
in Figure 4.


**Implications** **for** **discovery** **and** **maintenance.**
High redundancy increases user search costs and
fragments feedback and adoption signals across
near identical listings, which makes it harder for
high quality implementations to become clear defaults. It also indicates that developer effort is often
spent re-packaging common workflows rather than



front-end-design
mcp-builder
code-review
pdf

xlsx

web-app-testing
docx
pptx









xlsx









vercel-react-bestpractices
brainstorming





brand-guidelines
canvas-design









web-design-guidelines
theme-factory



internal-comms
uiux-promax





template-skill

agent-browser







algorithmic-art





test-driven-development
slack-gif-creator



systematic-debugging
code-reviewer



doc-coauthoring
commit



research





web-artifacts-builder





change-log-generator
writing-plans



4


**Major Category** **Sub-Category** **# Skills** **% of Total** **Avg Tokens** **Avg Downloads**


Software Engineering Code Generation 5,743 14.3% 2004 235
Debug & Analysis 5,319 13.2% 1772 103
Version Control 1,275 3.2% 1403 71
Infrastructure 9,664 24.0% 1995 114


Information Retrieval Web Search 567 1.4% 1517 1268
Academic Search 1,083 2.7% 2100 73
Live Data Streams 277 0.7% 1514 48


Productivity Tools Team Communication 698 1.7% 1458 196
Document Systems 1,579 3.9% 1981 125
Task Management 2,275 5.6% 1656 106


Data & Analytics Data Processing 3,179 7.9% 2134 93
Math & Calculation 368 0.9% 2028 147
Data Visualization 736 1.8% 2322 108


Content Creation Image Generation 1,201 3.0% 2145 214
Text Generation 2,212 5.5% 1977 178
Audio & Video 1,466 3.6% 1744 266


Utilities & Other Local File Control 255 0.6% 1420 42
Command Execution 337 0.8% 1541 70
Memory & Cognition 929 2.3% 1475 54
Other Utilities 1,125 2.8% 1684 135


Table 1: **Functional taxonomy and category-level statistics of agent skills.** Skills are organized into 6 major
categories and 20 sub-categories. For each sub-category, we report its size (# skills and % of corpus), the average
skill length in tokens, and the mean downloads/installs.



expanding coverage into less served tasks. This
motivates platform mechanisms that encourage
reuse and differentiation, including clearer canonical skills, more explicit versioning, and modular
templates that reduce incentives to publish superficial copies.


**4** **Skill Usage Patterns**


In this section, we study what skills do and what
users actually install. We summarize skill functionality with a taxonomy to support a corpus-level
comparison of skills’ publication with adoption.


**4.1** **Taxonomy and Classification**


We define a two-level taxonomy with 6 major categories and 20 sub-categories (Table 1). The taxonomy covers end-to-end agent workflows and separates common intents that differ in practice, such
as Code Generation and Debug & Analysis. For
each sub-category, we report the number of skills,
the mean token length, and the mean downloads
or installs. Figure 5 provides qualitative signals
by showing category-wise word clouds from frequent words in full skill markdown documents. We



retained words only if their frequency in the target category exceeded 1 _._ 5 times the average of
the remaining five categories. Marketplace tags
are sparse and inconsistent, so we label skills with
Qwen2.5-32B-Instruct (Qwen et al., 2025). Given
a skill’s name and description, the model selects
one sub-category and returns a strict JSON record.
Appendix D lists the taxonomy definitions and the
prompt template.


**4.2** **Distribution of Supply and Demand**


**Data-centric** **skills** **are** **longer.** Token length
varies by function. Data Visualization and Data
Processing are the longest sub-categories on average, at 2,322 and 2,134 tokens. These skills often
include multi-step pipelines, configuration blocks,
and reusable templates. By comparison, Version
Control and Local File Control are shorter at 1,403
and 1,420 tokens and are typically more procedural.
These differences matter for prompt budgeting and
auditing, since a small category can still impose a
large review burden if its skills are long.


**Software** **Engineering** **dominates** **listings.** In
Table 1, Software Engineering accounts for 54.7%



5


Software Engineering Information Retrieval Productivity Tools


Data & Analytics Content Creation Utilities & Other


Figure 5: **Word** **clouds** **of** **skill** **names** **by** **major** **category.** For each major category in Section 4.2, we show
the most frequent terms derived from the skill document. Words are retained only if their frequency in the target
category exceeds 1 _._ 5 times the average of the remaining five categories. Font size is proportional to within-category
frequency, highlighting common topics and recurring workflow motifs.



14000


12000


10000


8000


6000


4000


2000


0





700


600


500


400


300


200


100


0


|Col1|Col2|Col3|Sup|ply (Num|ber of Skil|ls)|Col8|Col9|
|---|---|---|---|---|---|---|---|---|
||||~~De~~|~~and (Ave~~|~~ rage Insta~~|~~  ls)~~|~~  ls)~~||
||||||||||
||||||||||
||||||||||
||||||||||
||||||||||
||||||||||
||<br>|<br>|<br>|<br>|<br>|<br>|<br>||



Figure 6: **Supply–demand** **dynamics** **by** **major** **cat-**
**egory.** Supply denotes the number of de-duplicated
skills after redundancy filtering (Section 3.2). Demand
denotes the average installs per skill and is used as a
coarse proxy for adoption. Most categories are close
to balanced, while content creation is demand-heavy,
software engineering is supply-heavy, and information
retrieval is demand-heavy despite limited supply.


of the corpus across Code Generation, Debug &
Analysis, etc. Infrastructure is the largest subcategory with 9,664 skills, or 24.0% of all listings.
This suggests that developers often publish skills
for environment setup, DevOps automation, tool
configuration, and deployment.


**Adoption concentrates on a few general skills.**
Adoption follows a different pattern from publication. Web Search has the highest mean downloads
at 1,268, but it represents only 1.4% of listings.
This indicates that a small number of retrieval con


nectors are reused widely. Content creation also
shows high mean installs, with Audio & Video at
266 and Image Generation at 214. Code Generation
remains among the most installed at 235. In contrast, utility-focused skills have lower mean installs,
including Local File Control at 42 and Memory &
Cognition at 54. This may reflect narrower use
cases, higher perceived risk, or overlap with builtin agent capabilities. We analyze this publication
adoption gap further in Section 4.
Overall, the taxonomy provides a compact map
of the ecosystem. It distinguishes what developers build from what users reuse and clarifies how
content complexity varies across functions.


**4.3** **Supply–Demand Dynamics**


Ecosystem growth alone does not show whether
developers publish the capabilities that users adopt
most. We therefore compare supply and demand
across functional categories. Following Section 3.2,
we de-duplicate skills to reduce the impact of nearidentical reposts and template variants. We define
supply as the number of de-duplicated skills in a
category, and define demand as the average installs
per skill and use it as a coarse proxy for adoption.


**Broad** **alignment** **with** **systematic** **deviations.**
Figure 6 summarizes the results. In most categories,
supply and demand move in the same direction,
suggesting that publication broadly tracks user in


6


Overall


Prod. Tools


Soft. Eng.


Util. & Other


Data & Anal.


Info. Retr.


Cont. Creat.


|Col1|Col2|54%|Col4|Col5|Col6|5%|Col8|Col9|Col10|Col11|30%|Col13|Col14|Col15|9%|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
||~~4~~|~~3%~~|||~~7%~~||||||~~46%~~|~~46%~~||||
|||||||||||||||||
|||~~51%~~||||||~~3~~|~~3~~|~~3~~|~~%~~|~~%~~|||~~4%~~|
|||||||||||||||||
|||||||||||||||||
|||~~51%~~||||~~10~~|~~10~~||||~~26%~~|~~26%~~|||~~11%~~|
|||||||||||||||||
|||~~5~~|~~%~~|||||~~8%~~|~~8%~~|~~8%~~|~~2~~|~~2~~|~~%~~|~~%~~|~~8%~~|
|||||||||||||||||
||||~~68%~~||||||||~~11%~~|~~11%~~|~~17~~|~~17~~||
|||||||||||||||||
|||||||||||||||||
||||~~75%~~||||||||||~~21~~|~~21~~|~~%~~|
|||||||||||||||||





Figure 7: **Supply–demand dynamics by sub-category.**
Supply denotes the number of de-duplicated skills in
each of the 20 sub-categories, and demand denotes the
average installs per skill. The figure highlights where
publication volume and adoption diverge at a finer granularity than Figure 6.


terest. However, we observe three consistent gaps.
First, content creation is demand-heavy. Users repeatedly reuse writing and media workflows, even
when the number of listings is modest. Second,
software engineering is supply-heavy. Skills that
wrap coding, testing, and repository routines are
easy to produce and share, which increases overlap
and spreads installs across close substitutes. Third,
information retrieval (Zheng et al., 2025; Wu et al.,
2025) is demand-heavy despite limited supply. A
small number of reliable retrieval skills can attract
many installs because web and database access is
useful for everyday tasks. However, publishing
these skills is costly because it requires stable connectors, careful query design, and ongoing maintenance as external interfaces and rate limits change.
Figure 7 further provides the same comparison for all 20 sub-categories. Together, these results highlight where canonical implementations,
stronger tool integration, and maintenance incentives may reduce supply-demand mismatches.


**5** **Risk and Safety Assessment**


Skills are executable procedures that interact with
external services, local environments, and user context. Relative to prompt-only interactions, they
expand the harm surface because a skill may access sensitive data or trigger real-world side effects (Wu and Zhang, 2026; Schmotz et al., 2025;
Liu et al., 2026b). We therefore quantify how often published skills enable privacy-sensitive reads,
state-changing actions, or critical capabilities such



Figure 8: **Risk** **level** **distribution** overall and by major category, where L0 is the lowest risk and L3 is the
highest, audited with Qwen2.5-32B-Instruct using Appendix E.


as arbitrary command execution.


**LLM-based auditing protocol.** We audit each
skill with Qwen2.5-32B-Instruct using the rubric
in Appendix E. The model receives the skill name,
description, and full SKILL.md content, and assigns exactly one risk level from L0 to L3 under a
worst-case interpretation, where L0 is safe, L1 is
privacy risk, L2 is moderate risk, and L3 is critical
risk. To support automatic aggregation, we require
a strict JSON response:



{"skill_name": "{{SKILL_NAME}}", "risk_level":

_�→_ "L0" | "L1" | "L2" | "L3", "reasoning": "A

_�→_ concise sentence explaining the specific

_�→_ risk factor."}


We report results by the six major categories from
Section 4.2. For a finer breakdown across all 20
sub-categories, see Appendix Figure 13.


**Overall distribution.** Figure 8 shows that lowrisk skills dominate, but action-enabling skills are
widespread. Overall, 54% are L0, 5% are L1, 30%
are L2, and 9% are L3. Thus, nearly two fifths
of the marketplace can access sensitive context or
perform writes and actions, and a nontrivial share
exposes critical capabilities.


**Category-level** **patterns.** Risk concentrates in
categories that connect the model to external systems. Content Creation is the safest category, with
75% L0 and only a small L3 share, which matches
workflows whose outputs are mainly drafts or media artifacts. Information Retrieval is largely read
oriented, with 68% L0 and the largest L1 share at
11%, often because connectors rely on user-specific
tokens or private sources. Productivity Tools is
dominated by L2 at 46%, reflecting common actions such as creating, editing, and sending emails,
messages, calendar entries, and documents. Software Engineering has the highest L3 fraction at



7


L0: Safe (Information/Public) L1: Privacy Risk (Read Sensitive)


L2: Moderate Risk (Restricted Write/Action) L3: Critical Risk (High Impact/Destructive)


Figure 9: **Risk level wordcloud.** L0 lists safe design
words like "visual" and "component." L1 focuses on
private data with terms like "meeting" and "history."
L2 shows action words like "git" and "merge." L3 highlights critical system and security terms such as "sudo,"
"admin," and "password."


14%, consistent with skills that manage environments, run commands, or manipulate repositories.
Utilities & Other also shows elevated L1 at 10%
and L3 at 11%, driven by local file operations and
command execution utilities. Data & Analytics
falls between these extremes, with 59% L0 and
23% L2, consistent with ETL-style pipelines that
may write intermediate outputs. Figure 9 further
presents a detailed word cloud analysis across different risk levels from L0 to L3. Words are retained
only if their frequency in the target level exceeds
1 _._ 5 times the average of the remaining three levels.
Overall, the most severe cases are less about content generation and more about enabling external
side effects. These results motivate least-privilege
tool design and additional safeguards for high-risk
operations.


**6** **Potential Directions**


In this paper, our measurements suggest that the
agent skill ecosystem is at an inflection point.
Progress now depends on improving quality, reducing overhead, and managing risk at scale.
**First**, rapid growth of Agent Skills relies on community contribution, but long term value depends
on high quality, non redundant skills. Given pervasive intent level duplication, future work should
pair semantic de duplication with quality signals including documentation, execution reliability, maintenance, and usage. A practical goal is convergence
to a small set of canonical skills per intent, so developers extend capabilities instead of re packaging
the same workflows.



**Second**, the heavy tailed length distribution of
skills’ tokens means a small fraction of skills
can dominate prompt budgets. Future systems
should support selective loading and modularization, retrieving only the steps, parameters, and tool
schemas needed for the current subgoal. Summarization, pruning unused branches, and instruction
compression can further reduce overhead while preserving faithful execution.
**Third**, our observed supply-demand gaps in
Agent Skills indicate that publication effort does
not always track user adoption. In particular, information retrieval attracts high usage but remains
costly to build and maintain, while many software
engineering skills compete as close substitutes. Future Skills platforms can use demand signals to
guide authoring tools, incentives, and review effort, and can support demand driven synthesis that
adapts existing skills to new connectors, domains,
and user constraints.
**Finally**, the presence of high-risk skills calls
for the establishment of proactive security protocols. Current frameworks lack fine-grained control
over state-changing actions. Future research should
implement standardized sandboxing environments
that enforce the principle of least privilege. Such
protocols would allow agents to perform complex
tasks while protecting the host system from unauthorized or malicious operations.


**7** **Conclusion**


In this paper, we conducted a large-scale, datadriven measurement of the agent skills ecosystem,
analyzing over 40,000 publicly listed skills. Across
production, adoption, redundancy, and safety auditing, our results provide a quantitative snapshot
of skills as an emerging abstraction for extending
large language model agents. Overall, the ecosystem is expanding quickly but unevenly: supply is
dominated by software engineering skills, intentlevel redundancy is pervasive, and adoption concentrates on a smaller set of high-demand capabilities, notably information retrieval and content
creation. From a safety perspective, although most
skills appear low risk, a non-trivial subset enables
state-changing or system-level actions, underscoring the need for safety-aware skill design and review. Taken together, these findings position agent
skills as a measurable infrastructure layer for agent
systems and motivate future work on standardization, reuse, and governance.



8


**Limitation**


Our study has two main limitations. First, our measurements are derived from a single snapshot of one
public marketplace collected around early February 2026. As platform policies, ranking algorithms,
and community composition evolve, both the supply and the demand for skills may change, and the
bursty growth patterns we report may not persist.
Second, we operationalize adoption using publicly
visible signals rather than verified executions inside deployed agents. These signals can be affected
by interface changes, caching, and social dynamics such as coordinated promotion, and they may
under represent private usage that occurs through
enterprise deployments or custom agent stacks.


**References**


Anthropic. 2025. [Agent skills overview.](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)


Mert Cemri, Melissa Z Pan, Shuyi Yang, Lakshya A
Agrawal, Bhavya Chopra, Rishabh Tiwari, Kurt
Keutzer, Aditya Parameswaran, Dan Klein, Kannan Ramchandran, and 1 others. 2025. Why do
multi-agent llm systems fail? _arXiv_ _preprint_
_arXiv:2503.13657_ .


Jianlv Chen, Shitao Xiao, Peitian Zhang, Kun Luo, Defu
Lian, and Zheng Liu. 2024. Bge m3-embedding:
Multi-lingual, multi-functionality, multi-granularity
text embeddings through self-knowledge distillation.
_arXiv preprint arXiv:2402.03216_, 4(5).


Haibo Jin, Kuang Peng, Ye Yu, Xiaopeng Yuan, and
Haohan Wang. 2026. Agent primitives: Reusable
latent building blocks for multi-agent systems. _arXiv_
_preprint arXiv:2602.03695_ .


Han Lee. 2025. Claude agent skills: A first principles
deep dive. leehanchung.github.io/blogs/2025/
10/26/claude-skills-deep-dive/.


Daniel Liu, Krishna Upadhyay, Vinaik Chhetri, AB Siddique, and Umar Farooq. 2026a. A large-scale study
on the development and issues of multi-agent ai systems. _arXiv preprint arXiv:2601.07136_ .


Yi Liu, Weizhe Wang, Ruitao Feng, Yao Zhang,
Guangquan Xu, Gelei Deng, Yuekang Li, and Leo
Zhang. 2026b. Agent skills in the wild: An empirical study of security vulnerabilities at scale. _arXiv_
_preprint arXiv:2601.10338_ .


Yimeng Liu, Misha Sra, Jeevana Priya Inala, and Chenglong Wang. 2025. Reuseit: Synthesizing reusable ai
agent workflows for web automation. _arXiv preprint_
_arXiv:2510.14308_ .


OpenAI. 2026. tiktoken. [https://github.com/](https://github.com/openai/tiktoken)
[openai/tiktoken.](https://github.com/openai/tiktoken)



openclaw Community. 2026. openclaw. [https://](https://github.com/openclaw/openclaw)
[github.com/openclaw/openclaw.](https://github.com/openclaw/openclaw)


Qwen, :, An Yang, Baosong Yang, Beichen Zhang,
Binyuan Hui, Bo Zheng, Bowen Yu, Chengyuan
Li, Dayiheng Liu, Fei Huang, Haoran Wei, Huan
Lin, Jian Yang, Jianhong Tu, Jianwei Zhang, Jianxin
Yang, Jiaxi Yang, Jingren Zhou, and 25 others. 2025. Qwen2.5 [technical](https://arxiv.org/abs/2412.15115) report. _Preprint_,
arXiv:2412.15115.


Tayiba Raheem and Gahangir Hossain. 2025. Agentic ai systems: Opportunities, challenges, and trustworthiness. In _2025 IEEE International Conference_
_on Electro Information Technology (eIT)_, pages 618–
624. IEEE.


Ranjan Sapkota, Konstantinos I Roumeliotis, and Manoj
Karkee. 2025. Ai agents vs. agentic ai: A conceptual taxonomy, applications and challenges. _arXiv_
_preprint arXiv:2505.10468_ .


David Schmotz, Sahar Abdelnabi, and Maksym Andriushchenko. 2025. Agent skills enable a new class
of realistic and trivially simple prompt injections.
_arXiv preprint arXiv:2510.26328_ .


Noah Shinn, Federico Cassano, Ashwin Gopinath,
Karthik Narasimhan, and Shunyu Yao. 2023. Reflexion: Language agents with verbal reinforcement
learning. _Advances in Neural Information Process-_
_ing Systems_, 36:8634–8652.


Guanzhi Wang, Yuqi Xie, Yunfan Jiang, Ajay Mandlekar, Chaowei Xiao, Yuke Zhu, Linxi Fan, and
Anima Anandkumar. 2023. Voyager: An open-ended
embodied agent with large language models. _arXiv_
_preprint arXiv:2305.16291_ .


Lei Wang, Chen Ma, Xueyang Feng, Zeyu Zhang, Hao
Yang, Jingsen Zhang, Zhiyuan Chen, Jiakai Tang,
Xu Chen, Yankai Lin, and 1 others. 2024. A survey
on large language model based autonomous agents.
_Frontiers of Computer Science_, 18(6):186345.


Yaxiong Wu and Yongyue Zhang. 2026. Agent skills
from the perspective of procedural memory: A survey.
_Authorea Preprints_ .


Yujiang Wu, Shanshan Zhong, Yubin Kim, and Chenyan
Xiong. 2025. What generative [search](https://arxiv.org/abs/2510.11438) engines like
and how to optimize [web](https://arxiv.org/abs/2510.11438) content cooperatively.
_Preprint_, arXiv:2510.11438.


Shunyu Yao, Jeffrey Zhao, Dian Yu, Nan Du, Izhak
Shafran, Karthik R Narasimhan, and Yuan Cao. 2022.
React: Synergizing reasoning and acting in language
models. In _The eleventh international conference on_
_learning representations_ .


Boyuan Zheng, Michael Y Fatemi, Xiaolong Jin,
Zora Zhiruo Wang, Apurva Gandhi, Yueqi Song,
Yu Gu, Jayanth Srinivasa, Gaowen Liu, Graham Neubig, and 1 others. 2025. Skillweaver: Web agents can
self-improve by discovering and honing skills. _arXiv_
_preprint arXiv:2504.07079_ .



9


**Agent Skills**
Plug-and-play modules










|Col1|SKILL.md|
|---|---|
||scripts|
||...|
|||


|find-best-product<br>Reusable procedure for identifying the optima|find-best-produ|Col3|ct|Col5|
|---|---|---|---|---|
|find-best-product<br>Reusable procedure for identifying the optima<br>|find-best-produ|Reusable procedure for identifying the optima<br>|Reusable procedure for identifying the optima<br>|Reusable procedure for identifying the optima<br>|
|roduct based user needs, budget, and preferences, ...|roduct based user needs, budget, and preferences, ...|roduct based user needs, budget, and preferences, ...|roduct based user needs, budget, and preferences, ...|roduct based user needs, budget, and preferences, ...|
|||||Instructions|
||||||






|..., Use Amazon tool to search products, ...<br>Reference to Tooling|Col2|Col3|
|---|---|---|
||<br>Reference to Tooling|<br>Reference to Tooling|
||<br>Reference to Tooling|Reference to Tooling|



Figure 10: Internal structure of a typical agent skill,
illustrated using the find-best-product skill. The
SKILL.md file begins with YAML metadata that specifies the skill name and description, which are used for
skill discovery and selection. The subsequent Markdown sections define the procedural workflow and detailed execution instructions, including references to
external tools such as product search APIs. This structure enables lightweight semantic matching at discovery
time while supporting complex, tool-integrated execution when the skill is invoked.


**A** **Skill Structure and Integration in**
**Agents**


Skills provide a modular and expressive mechanism for extending agent capabilities. By encapsulating triggering conditions, procedural logic, and
tool interactions, skills enable agents to compose
complex behaviors dynamically at runtime, while
keeping the core agent architecture lightweight and
unchanged.


**A.1** **Skill Structure**


Skills act as first-class capability abstractions in
an agent system, allowing agents to solve complex
tasks through structured and reusable procedures.
Unlike ad hoc prompts or isolated tool calls, each
skill is defined as a lightweight, program-like unit
with explicit execution semantics. Formally, a skill
can be represented as:


Skill = {Metadata, Instructions, Resources},


where metadata specifies the applicability conditions of the skill, instructions define the procedural
steps to be executed, and resources link the skill to
external tools, scripts, APIs, or auxiliary artifacts.
In practice, each skill is organized within a dedicated directory containing a SKILL.md file that
materializes this abstraction. As shown in Fig. 10,
SKILL.md begins with a YAML frontmatter that
specifies the skill name and a concise description.
This metadata serves as a compact semantic signal
for skill discovery and selection. The remainder
of the file is written in Markdown and encodes the



Figure 11: Dynamic skill integration during agent execution. Given a user request, the agent reasons over the
injected skill index and selects the most relevant skill
based on semantic matching. The full skill specification
is then loaded, and the agent follows the skill’s instructions, potentially invoking external tools and producing
intermediate outputs. Different user intents trigger different skills, enabling modular, reusable, and contextaware agent behavior through conditional skill selection
and state-driven transitions.


procedural logic of the skill, including high-level
processing stages, decision criteria, and concrete
instructions for tool invocation. This design separates lightweight skill discovery from full procedural execution. During agent initialization, only
the metadata is exposed to the model, minimizing
prompt overhead. Detailed instructions and associated resources are loaded only when a skill is
selected, enabling rich, tool-augmented behavior
without inflating the agent’s baseline context.


**A.2** **Skill Integration in Agents**


Beyond the definition of individual skills, agent intelligence critically depends on how multiple skills
are dynamically coordinated during task execution.
At the start of a session, the agent is provided with a
summarized index of available skills, consisting of
their names and descriptions. Given a user request,
the agent performs high-level reasoning to infer the
underlying goal and decompose it into subgoals.
Rather than following a fixed execution pipeline,
the agent conditionally selects skills based on the
current subgoal and the evolving internal state.
Once a skill is invoked, the agent follows the
skill’s procedural instructions, potentially interacting with external tools and producing structured intermediate outputs. These outputs are incorporated
into the agent’s internal state and directly influence
subsequent decisions. For instance, the execution



Help me find a laptop ...


**Thinking:**
1. The user wants help finding a laptop ...
2. Scan the injected skills list. The "findbest-product" skill matches closely ...
3. Invoke "find-best-product", load the
full SKILL.md ...
4. Following skill instructions ... Get final
answer ...
**Response:**
Here are some laptop options you might
consider, depending on what you need ...


Schedule a team meeting ...


**Thinking:**
.. Invoke “event-management", load the
full SKILL.md ...



10


of an analysis skill may introduce new constraints
or observations, which in turn determine whether
the agent invokes a refinement skill, explores alternative strategies, or proceeds to a synthesis step.
As a result, skill execution induces a non-linear
control flow in which transitions between skills
are determined by intermediate state updates rather
than pre-defined task graphs. Through iterative
reasoning, skill selection, and execution, multiple
skills collaboratively contribute to the completion
of complex tasks.
Fig. 11 illustrates this execution paradigm. The
agent alternates between reasoning over the current state, selecting an appropriate skill from the
available index, and executing the selected skill
to update its state. Importantly, this coordination
emerges from model-driven decision-making over
skill abstractions, without relying on hard-coded orchestration rules or manually designed workflows.


**B** **Additional Analysis of Redundancy**


This section provides two complementary views
of redundancy that support the main analysis in
Section 3.2. First, we report redundancy under
exact name-based matching, which is a conservative signal that is easy to interpret. Figure 4 shows
that a small set of generic names is repeatedly published. This pattern is consistent with template
reuse and re-packaging of common workflows. Because name matching does not capture paraphrases,
the true amount of redundancy is likely larger,
which motivates our additional near-duplicate analysis in the main text. Second, we visualize skills in
a low-dimensional space to show how closely they
cluster by functionality as shown in Figure 12. It
provides a complementary view based on semantic similarity. Skills form visible clusters within
and across sub-categories, suggesting that many
listings share overlapping intent even when their
names differ.


**C** **Additional Analysis of Risk and Safety**
**Assessment**


This section complements the main results in Section 5 by reporting risk at the sub-category level.
We use the same auditing protocol and the same
four-level rubric, and we aggregate the predicted
L0–L3 labels within each of the 20 sub-categories
shown in Figure 13. This view helps identify where
risks concentrate and which types of skills most often enable state-changing actions or higher-impact



operations.


**D** **Skill Classification Prompt**


To label skill content at scale, we use an instructiontuned LLM to assign each skill to exactly one subcategory in our taxonomy. The prompt provides
definitions for all 6 major categories and 20 subcategories, and it takes the skill name and description as input. We require the model to return strict
JSON with both the chosen label and a brief justification so that outputs can be parsed reliably and
audited. Figure 14 shows the full prompt.


**E** **Skill Security Audit Prompt**


To assess potential harms beyond content, we use a
LLM to label each skill by security risk. Figure 15
shows the full prompt used by LLM. The prompt
asks the LLM to consider how a skill interacts with
data and tools, and to assign the highest applicable
level under a worst-case interpretation. We define
four levels, from L0 for read-only public operations
to L3 for high-impact actions such as destructive
writes or arbitrary command execution. The model
must output strict JSON so the labels can be parsed
at scale and reviewed.


**F** **The Examples of High-Risk (L3) Skills**


High-Risk (L3) skills are those that, if misused,
prompt-injected, or misconfigured, may enable irreversible or high-impact actions. Typical cases
include arbitrary command execution, handling of
credentials and other secrets, escalation to privileged access, and operations that directly move
or manage financial assets. To make these risks
concrete, Table 2 summarizes representative examples across multiple major categories and provides
concise rationales (see Section 5 for details) that
follow a worst-case reading of the skill instructions
and tool interfaces. To protect the privacy of skill
contributors, we omit skill names and redact identifiable keywords in black xxx. Moreover, we also
highlight risk-related keywords in light yellow to
help readers quickly locate the primary sources of
risk in corresponding skill.



11


Academic Search
Audio & Video
Code Generation
Command Execution



Data Processing
Data Visualization
Debug & Analysis
Document Systems



Image Generation
Infrastructure
Live Data Streams



Local File Control
Math & Calculation
Memory & Cognition



Other Utilities
Task Management
Team Communication



Text Generation
Version Control
Web Search



100


50


0


50


100

|Col1|Col2|Col3|Col4|Col5|Col6|
|---|---|---|---|---|---|
|||||||
|||||||
|||||||
|||||||
|||||||



t-SNE Dimension 1


Figure 12: **t-SNE view of skill embeddings by sub-category.** Each point is a skill represented by an embedding of
its name and description. Points are colored by the predicted sub-category. Tight clusters suggest many skills with
overlapping intent.





File Control
Team Comm.













Cmd Exec.
Ver. Control









Infra.
Doc. Systems
Memory & Cog.





Task Mgmt.



Data Proc.
Web Search
Live Streams
Audio & Video
Debug & Anal.





Other Util.
Image Gen.





Data Viz.
Code Gen.
Acad. Search

Text Gen.
Math & Calc.



|18|%|8%|Col4|Col5|57%|Col7|Col8|Col9|15%|
|---|---|---|---|---|---|---|---|---|---|
|~~2~~|~~1%~~|~~11~~||||~~63%~~|||~~3~~|
||~~2%~~|~~4%~~|~~2~~|~~%~~|||~~45%~~|||
||~~26%~~|||||~~69%~~||||
||~~31%~~||||~~40%~~|||~~25%~~||
|||~~42%~~||~~6%~~|||~~49%~~|||
|||~~48%~~|||~~20~~|||~~29%~~||
|||~~50%~~|||~~7%~~||~~39~~|||
|||~~52%~~|||~~9%~~||~~27%~~||~~10%~~|
|||~~53%~~|||~~10~~||~~30~~|~~%~~|~~5%~~|
|||~~56~~||||~~18%~~||~~14%~~|~~10%~~|
||||~~65%~~|||~~3%~~||~~30%~~||
||||~~65%~~|||~~7~~||~~20%~~|~~6%~~|
||||~~69%~~||||~~5%~~|~~16%~~|~~7%~~|
||||~~71%~~|||||~~27%~~||
||||~~75%~~||||~~6~~|~~1~~|~~7%~~|
||||~~76%~~|||||~~18%~~|~~4%~~|
||||~~79~~|~~%~~||||~~9%~~<br>|~~10%~~<br>|
|||||~~3%~~||||~~3%~~|~~12%~~|
|||||~~89%~~|||||~~7%~~|
|||||||||||


Figure 13: **Risk distribution by sub-category.** Risk level distribution across the 20 sub-categories in our taxonomy,
using the same auditing protocol as Figure 8. The figure shows how L0–L3 risks vary across sub-categories and
identifies the sub-categories that contribute the largest shares of L2 and L3 skills, which helps prioritize safeguards
and review.


12


Figure 14: Prompt for skill classification (Qwen2.5-32B-Instruct).


13


Figure 15: Prompt for skill security auditing (Qwen2.5-32B-Instruct).


14


Table 2: **Examples of High-Risk (L3) Agent Skills with Sensitive Information Handling** . To protect the privacy
of skill contributors, we do not display skill names and redact identifiable keywords in black xxx. In addition, we
highlight specific risk-related keywords in light yellow.


**Category** **Reasoning**



**Software**
**Engineering**



This skill involves handling and managing sensitive information such as API keys,

database passwords, and TLS certificates, which can lead to critical risks including
unauthorized access and data breaches if misused.







**Engineering**



extracting credentials, and performing destructive actions like creating persistent
access mechanisms and compromising domains, leading to severe security breaches.







**Engineering**



extracting credentials, and performing actions that can lead to permanent data loss or
system compromise.







**Engineering**



as unauthorized transfers or refunds.







**Engineering**



result in full system compromise, including data theft, modification, and permanent
damage.







**Information**
**Retrieval**



This skill handles and automates sensitive actions such as logging in with credentials
and filling payment information, which involves high-risk operations like credential
handling and financial transactions.







**Retrieval**



which could lead to financial loss if misused.







**Retrieval**



transactions, posing a high risk of financial loss if misused.


_Continued on next page..._


15


_Continued from previous page_



**Category** **Reasoning**







**Retrieval**



RCE and other high-impact risks.







**Retrieval**



which can lead to financial loss if misused.







**Productivity**
**Tools**



The skill enables a wide range of actions including sending emails, creating issues,
posting messages, and updating databases, which can lead to financial loss, data
leakage, or unauthorized access if misused.







**Tools**



wiping, which can lead to permanent data loss and account compromise.







**Tools**



which could lead to unauthorized access and triggering of sensitive workflows if
misused.



**Productivity** The skill includes examples of executing shell commands and performing actions that
**Tools**





The skill includes examples of executing shell commands and performing actions that
can lead to system-level changes, such as database failover and DNS updates, which
pose a high risk of causing significant damage if misused.







**Tools**



lead to irreversible data loss if misused.







**Data** **&**
**Analytics**



The skill enables operations that can lead to irreversible data destruction, such as
delete operations, and involves managing database users and permissions, which can

result in critical data loss or unauthorized access.







_Continued on next page..._



16


_Continued from previous page_



**Category** **Reasoning**



**Data** **&**
**Analytics**



This skill allows for the deletion of accounts, categories, category groups, payees, rules,
and schedules, which can lead to permanent data loss and significant disruption of
financial management.









can lead to data loss or unauthorized access.







**Data** **&**
**Analytics**



The skill allows for executing arbitrary SQL commands including destructive operations
like DELETE and DROP, which can lead to irreversible data loss or corruption.







**Analytics**



which can lead to irreversible data loss.







**Creation**



in-game currency and reviving players, which can lead to financial loss or abuse if
misused.







**Creation**



unauthorized content publication and potential account takeover if misused.







**Content**
**Creation**



The skill includes code execution capabilities through a built-in Python interpreter and
sandbox, which can lead to arbitrary code execution and potential system compromise.















**Content**
**Creation**



The skill includes code execution capabilities with a built-in Python interpreter and
sandbox, posing a critical risk for potential arbitrary code execution.


_Continued on next page..._


17


_Continued from previous page_



**Category** **Reasoning**









corruption.







**Other**



unauthorized access if misused or leaked.







**Utilities** **&**
**Other**



The skill allows for irreversible data destruction (e.g., delete operations) and
system-level configuration changes (e.g., Admin SDK operations), posing a high risk of
permanent data loss and account management issues.







**Utilities** **&**
**Other**



This skill involves executing commands that can generate cryptographic keys and
manage wallets, which poses a high risk of financial loss and data exposure if misused.















18


