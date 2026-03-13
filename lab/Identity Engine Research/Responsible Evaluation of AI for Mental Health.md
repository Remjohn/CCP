## **Responsible Evaluation of AI for Mental Health**

**Hiba Arnaout** **[1]** **, Anmol Goel** **[1]** **, H. Andrew Schwartz** **[2]** **, Steffen T. Eberhardt** **[3]** **,**
**Dana Atzil-Slonim** **[4]**, **Gavin Doherty** **[5]**, **Brian Schwartz** **[3]**, **Wolfgang Lutz** **[3]**,
**Tim Althoff** **[6]**, **Munmun De Choudhury** **[7]**, **Hamidreza Jamalabadi** **[8]**, **Raj Sanjay Shah** **[7]**,
**Flor Miriam Plaza-del-Arco** **[9]**, **Dirk Hovy** **[10]**, **Maria Liakata** **[11]**, **Iryna Gurevych** **[1]**


1Technische Universität Darmstadt, 2Vanderbilt University 3Trier University
4Bar-Ilan University 5Trinity College Dublin 6University of Washington
7Georgia Institute of Technology 8Phillips-Universität Marburg 9LIACS, Leiden University
10Bocconi University 11Queen Mary University London, Alan Turing Institute



**Abstract**


Although artificial intelligence (AI) shows
growing promise for mental health care, current approaches to evaluating AI tools in this
domain remain fragmented and poorly aligned
with clinical practice, social context, and firsthand user experience. This paper argues for
a rethinking of _responsible evaluation_   - what
is measured, by whom, and for what purpose –
by introducing an interdisciplinary framework
that integrates clinical soundness, social context, and equity, providing a structured basis
for evaluation. Through an analysis of 135 recent *CL publications, we identify recurring
limitations, including over-reliance on generic
metrics that do not capture clinical validity,
therapeutic appropriateness, or user experience,
limited participation from mental health professionals, and insufficient attention to safety
and equity. To address these gaps, we propose
a taxonomy of AI mental health support types

  - assessment-, intervention-, and information
synthesis-oriented   - each with distinct risks
and evaluative requirements, and illustrate its
use through case studies.


[https://ukplab.github.io/nlp-mh-evals/](https://ukplab.github.io/nlp-mh-evals/)


**1** **Introduction**


Large Language Models (LLMs) hold considerable
promise for advancing mental health research and
practice. They offer new tools at scale to support
diagnosis, therapy, peer-support, and self-guided
support, where users interact with LLMs directly
for guidance or coping strategies (Demszky et al.,
2023; Cruz-Gonzalez et al., 2025). From detecting
early signs of depression in language (Lan et al.,
2025), to clinical documentation and summarizing
complex patient histories (Shah et al., 2025; Srivastava et al., 2024), and generating therapeutic or
supportive responses in online communities (Liu
et al., 2021; Gabriel et al., 2024), AI-enabled mental health tools have the potential to augment pro


fessional care and extend psychological support beyond traditional clinical encounters. This potential
is especially valuable due to the limited availability
of mental health resources, growing global demand,
and persistent inequities in access to care [1] .

Despite their promise, AI mental health tools
are fundamentally lacking in evaluation. Existing
evaluation practices are inconsistent (Yang et al.,
2021; Aich et al., 2022; Chen et al., 2024b) and
often insufficient (Tornero-Costa et al., 2023). This
is concerning because poor evaluation, particularly
in this domain, can lead to misleading conclusions,
unintended harm, and inequitable outcomes. Recurring issues include over-reliance on generic metrics that fail to capture clinical validity, therapeutic
appropriateness, or user experience, minimal participation from mental health professionals, and
insufficient attention to safety, equity, and longterm impact. While we do _not_ expect papers in
venues like ACL to be fully deployable in clinical
settings, careful evaluation is essential to responsibly translate research insights toward real-world
mental health impact. Our goal is to raise evaluation standards as much as possible so that research
outputs can earn the trust and approval of domain
experts, even when the tools are not yet – or are not
intended to be – used in actual clinical practice.

These limitations are not idiosyncratic model
bugs, but symptoms of an underlying disconnect
between the communities that build, use, and regulate AI for mental health tools. Current evaluations often default to technical benchmark wins,
while clinicians and other users judge success by
changes in symptoms, patient functioning, and
safety over time; social and implementation scientists, in turn, ask whether a tool fits workflows,
earns trust, and reaches people equitably. Without
a shared evaluative language, results travel poorly
across these communities: automated scores with

[1WHO 2025 report.](https://www.who.int/news/item/02-09-2025-over-a-billion-people-living-with-mental-health-conditions-services-require-urgent-scale-up)



1


out clinical anchors may overstate progress, “human studies” may lack meaningful involvement as
well as methodological transparency or expert input, and cross-disciplinary collaboration may arrive late - if at all. What is needed is a common, clinically grounded evaluation framework
that makes psychometric constructs accessible to
AI researchers, pairs them with human-centered
and implementation-science measures, and treats
safety, equity, and real-world utility as primary outcomes. This framework can then be the connective
tissue that enables mutual intelligibility and, ultimately, responsible deployment across research
contexts, clinics, and community platforms.
Consequently, we posit a fundamental reconsideration of evaluation for AI mental health tools according to clinical goals, typically falling into three
broad types: **(1) assessment** for inferring psychological states (e.g., language-based screening), **(2)**
**interventions** to deliver or scaffold support (e.g.,
therapeutic chatbots), and **(3) information synthe-**
**sis** to aid practitioners or researchers (e.g., clinical
summarization). This categorization clarifies how
different types of tools require context-sensitive
evaluation and enables the field to calibrate what
claims are supported by existing evaluations.
**Contributions.** Our paper makes four primary
contributions. (1) We identify key gaps and challenges in current evaluation practices for AI in
mental health (§ 2; see Appendix A for details
of surveyed papers); (2) we propose a structured
taxonomy of tool types and salient evaluation dimensions, highlighting differences between general generative AI evaluation and mental health
specific concerns (§ 3); (3) we demonstrate its utility through five illustrative case studies spanning
assessment, intervention, and support tools in diverse settings (§ 4); and (4), we synthesize these
insights into recommendations and guiding principles for responsible and comprehensive evaluation
moving forward (§ 5).
**Positionality.** Our call for rethinking evaluation
aligns with the broader reflection on the generative
AI evaluation crisis in the *CL community (Bommasani, 2023; Elangovan et al., 2024; Kotonya and
Toni, 2024; Zhou et al., 2025b), which emphasizes
the limitations of relying solely on automated metrics and benchmarks. Recent surveys on LLMs in
psychotherapy (Na et al., 2025), cognitive distortion detection (Sage et al., 2025), and mental health
conversational agents (Atapattu et al., 2025) highlight tasks and models but less so _how tools should_



**Observed practice** **%**


Rely only on AI/NLP metrics 50


No human evaluation 52


With human evaluation but no experts 29


Evaluation guidelines not shared 17


Limitations in evaluation not discussed 36


Table 1: Overview of the ACL Anthology study conducted to ground our position. We queried the ACL
Anthology database with mental health keywords [2], restricting results to the past five years and papers of types
“main” or “findings”. This yielded 135 papers on mental
health [3] . These manually-made observations provide
context for our broader discussion of challenges and
gaps in the evaluation of AI tools for mental health. We
show details about the surveyed papers in Appendix A;
Tables 3–17.


_be evaluated responsibly_, i.e., in ways that account
for clinical validity, user experience, ethical considerations, safety, and equitable outcomes. We
extend this conversation by proposing an interdisciplinary framework emphasizing clinical soundness,
social context, equity, and user experience as central to evaluation in mental health AI.


**2** **Observed Practices**


To ground our position, we conducted a quantitative
analysis of 135 papers on mental health, published
in the ACL Anthology [4] over the past 5 years, with
36% of them published in 2025. Table 1 summarizes key patterns that emerged from this review,
and Appendix A provides detailed annotations, including the tasks covered by these papers, and the
observed practices documented at a paper level.
Overall, we found that current evaluation practices
in this literature remain limited in scope and rigor,
especially considering the sensitivity and clinical
implications of the domain. While the surveyed
works cover a wide range of tasks, from detecting
mental health conditions (Chen et al., 2024b; Yang
et al., 2021; Lee et al., 2024a) to building therapeutic chatbots (Saha et al., 2022; Deng et al., 2023;
Shim, 2021), their evaluations often rely on narrow,
model-centric criteria.


2 _mental health_, _mental disorder_, _mental illness_, _therapy_
and _psychiatry_ ; Either in the title or in the abstract.
3After manual inspection to remove papers that mention
mental health _only in passing_ but not as the main focus; We
had 152 papers before the inspection.
[4https://aclanthology.org/; query date:](https://aclanthology.org/) 11-2025.



2


Specifically, five concerning patterns emerge.
Half of the papers rely _only_ on standard AI/NLP
metrics such as accuracy, F1, BLEU, or ROUGE,
ignoring psychological validity or clinical relevance. Over half (54%) include _no_ human evaluation, and among those that do, 29% do so _without_
involving mental health experts. Nearly one-fifth
of papers omit evaluation guidelines, and roughly a
third fail to discuss limitations in the way the evaluations have been conducted. These gaps indicate
that current practices assess technical performance
but often overlook safety, interpretability, and realworld utility (Thieme et al., 2020).
Overall, these findings reveal a methodological
gap: AI tools may score well on generic NLG metrics yet fall short of clinical standards or user needs.
This critique is not aimed at individual works, but
rather, highlights the need for shared, rigorous evaluation practices. The following sections build on
these observations to introduce a taxonomy (§ 3),
illustrate it with case studies (§ 4), and present
guiding principles for a clinically grounded and
human-centered evaluation (§ 5).


**3** **Proposed Taxonomy**


While new principles are needed to evaluate AI for
mental health, there is much to build on from a
century of work in psychological assessment ( _clas-_
_sical_ _quantitative_ _methods_ (Cook and Beckman,
2006)) and recent advances in applying technology
in human-computer interaction and health ( _imple-_
_mentation science_ (Lyon et al., 2023)).
**Classical quantitative methods.** _Validity_ and _re-_
_liability_ are foundational in psychological evaluation [5] . Validity asks whether a tool _does what it_
_is intended to do_, while reliability asks _whether it_
_does so consistently_ . Most current evaluations in
AI mental health work mainly focuses on one validity subtype, namely construct validity, for example,
through agreement with human annotations or existing scales (Park et al., 2020; Lee et al., 2024a),
but this is only a starting point for high-stakes applications. A classifier may correlate with overall
depression severity yet fail to predict specific symptoms or generalize across populations. Similarly,
a summarization tool may align with expert summaries but omit safety-critical information or misinterpret non-clinical expressions, thus highlighting
limits in discriminant validity and generalization.


5Evidenced by their inclusion in nearly every modern textbook on psychological research methods (Cohen et al., 1988;
Reynolds and Livingston, 2021; Meyer, 2010)



Near-perfect construct validity is not always desirable, as even established assessments have limitations.
**Implementation** **science.** Recent advances in
health informatics and human-computer interaction
highlight that barriers to using AI go beyond validity and reliability (Reddy, 2024). Implementation
science adds two pillars: _implementation_ –whether
an AI tool is feasible, acceptable, fits workflows,
and improves outcomes safely; and _maintenance_ whether it remains effective over time, handling
population shifts, language drift, inequities, or unintended consequences. Together with validity and
reliability, these four pillars define a multidimensional evaluation space for AI in mental health
across assessment, interventions, and information
synthesis (i.e., therapist support).
To organize these concepts, we introduce a taxonomy of evaluation dimensions (Table 2 [6] ), mapping classical psychometrics and implementation
science principles onto three common AI applications: assessment, intervention, and information
synthesis. These evaluation paradigms are multifaceted; no single score can capture the full opportunities and risks of AI, akin to a cockpit dashboard
where multiple readings are needed to assess performance.
_**Assessments**_ involve tools for measurement, screening, aiding diagnosis, or forecasting (e.g., scoring
depression severity, estimating suicide risk from social media, classifying psychosis-related language).
Validity focuses on convergent validity (alignment
with other measures of the same construct), discriminant validity (avoiding spurious alignment with
different constructs), and criterion validity (relation
to meaningful external outcomes like hospitalization or symptom trajectories). Reliability covers
stability over time (test-retest), robustness across
populations (clinics, demographics, cultures, neurodivergent groups), and internal consistency (coherent subcomponents). Implementation examines
feasibility, impact on diagnostic accuracy, equity,
acceptability, and bias mitigation. Maintenance
involves monitoring generalizability, performance
drift, population-level outcomes, unintended consequences, and evolving language norms.
_**Interventions**_ are tools aimed at changing outcomes, such as treatment agents, self-help aids,
prevention nudges, or adaptive therapy recommen

6While our focus is on clinical integration, this taxonomy
is intended to also cover peer-supported and community-based
AI mental health tools.



3


|Real-World Use Implementation Maintenance Can it be used effectively in real-world Does it remain effective and appropriate contexts? over time as users and contexts evolve?|1. Generalizability and Impact: Does performance remain stable as users or contexts evolve over time? Does it contribute to improved individual or population-level outcomes? 2. Unintended Consequences: Is it creating labeling bias?|1. Stability: Does the bene i ft sustain over time across different user groups and contexts? Are there equitable outcomes and access? 2. Safety: Are there emergent risks or harmful use patterns?|1. Tool-level Impact: Does it reduce administrative load, emo- tional burden, or improve care and sup- port quality across settings? 2. Unintended Consequences: Does it foster over-reliance or skill atro- phy?|
|---|---|---|---|
|**Real-World Use**<br>**Implementation**<br>_Can it be used effectively in real-world_<br>_contexts?_<br>**Maintenance**<br>_Does it remain effective and appropriate_<br>_over time as users and contexts evolve?_|**1. Feasibility:**<br>Does it ft into the workfows and rou-<br>tines of intended users (e.g., clinicians,<br>peer supporters, or individuals)?<br>**2. Effectiveness and Usefulness** (ex-<br>trinsic):<br>Is it consistent across diverse popula-<br>tions? Does it improve diagnostic ac-<br>curacy in practice?<br>**3. Acceptability:**<br>Are data gathering and feedback mecha-<br>nisms for assessment acceptable to both<br>patients and clinicians?|**1. Effectiveness:**<br>Does it improve symptoms, wellbeing,<br>or functioning under real-world condi-<br>tions (with or without clinician involve-<br>ment)?<br>**2. Usability and Engagement:**<br>Do users adhere to the intervention? Is<br>it easy to use?<br>**3. Implementation Risk:**<br>Is it being used as intended?<br>**4. Equity and Acceptability:**<br>Do diverse user groups fnd it acceptable<br>and trustworthy? Are potential biases<br>mitigated?|**1. Acceptability:**<br>Would intended users (clinicians, pa-<br>tients, peer supporters, community work-<br>ers) accept and trust the tool in their<br>workfows or daily lives?<br>**2. Usefulness:**<br>Do the users fnd it useful in their every-<br>day work or well-being activities?<br>**3. Impact:**<br>Does the support improve outcomes for<br>users or benefciaries (e.g., effciency,<br>understanding, well-being)?<br>**4. Equity and Bias Mitigation:**<br>Are there systematic biases in recom-<br>mendations or summaries?<br>Are they<br>identifed and mitigated?|
|**Quality Criteria**<br>**Validity**<br>_Does it do what it is intended?_<br>**Reliability**<br>_Does it do the same thing under_<br>_different conditions?_|**1. Across Time:**<br>What is the test-retest stability (at ap-<br>propriate time intervals)? Does it [not]<br>change if it should [not]?<br>**2. Across Populations:**<br>Does it work just as well across differ-<br>ent cultures, locations, neurodivergent<br>populations?<br>**3. Internal Consistency:**<br>To what extent do all components or<br>interactions of the tool function consis-<br>tently?|**1. Across Time:**<br>Does it keep working as well at future<br>points in time?<br>**2. Across Populations:**<br>Is the effect the same across cultures, lo-<br>cations, neurodivergence?<br>**3. Internal consistency:**<br>If the intervention has multiple mecha-<br>nisms or components, do they each con-<br>tribute consistently to desired outcomes?|**1. Scenarios:**<br>Does it perform reliably across different<br>use scenarios?<br>**2. Services:**<br>Does it integrate effectively across dif-<br>ferent service models or modalities?|
|**Quality Criteria**<br>**Validity**<br>_Does it do what it is intended?_<br>**Reliability**<br>_Does it do the same thing under_<br>_different conditions?_|**1. Construct Validity:**<br>How much does it match other tools or<br>indicators (e.g., clinical, community, or<br>self-report measures) intended to assess<br>the same construct (convergent) or a dif-<br>ferent construct (discriminant)?<br>**2. Criterion Validity:**<br>What is its association with external,<br>theoretically-related constructs or out-<br>comes (e.g., wellbeing, functioning, par-<br>ticipation)?|**1. Construct Validity:**<br>Does it make a change in the intended<br>direction (convergent) or have any ad-<br>verse or unintended effects (discrimi-<br>nant)? From experimentation, RCTs, or<br>real-world trials (effcacy or effective-<br>ness).<br>**2. Criterion Validity:**<br>Does it predict or improve external<br>downstream outcomes (e.g., wellbeing,<br>functioning, relationships, work, com-<br>munity participation)?|**1. Construct Validity:**<br>Does it provide accurate, contextually<br>appropriate, and unbiased summaries or<br>recommendations?<br>**2. Criterion Validity:**<br>Does it save users (e.g., clinicians or<br>peer supporters) time or improve the<br>quality of their decisions?|
|**Support type**|**Assessment**<br>(e.g.,<br>language-based<br>screening)|**Intervention**<br>(e.g., therapeutic chat-<br>bots)|**Information synthesis**<br>(e.g., clinical summa-<br>rization)|



4


dations. Validity includes construct validity (delivering the intended therapeutic ingredient), efficacy
(producing beneficial change and avoiding harm),
and criterion validity (predicting improvements in
functioning, relationships, or job stability). Reliability examines whether effects hold across time,
populations, settings, and intervention components.
Implementation considers real-world symptom improvement, user engagement, clinician usability,
low risk, and monitoring off-label use. Maintenance evaluates persistence of benefits and emergence of new risks, such as overuse or avoidance
of human care.
_**Information synthesis**_ tools augment care and administration efficiently. For automated care aids
(clinical summarization, triage notes, treatment recommendations), convergent validity asks whether
outputs are accurate as per the clinical evidence
base, while criterion validity asks whether they
save clinician time or improve documentation. Reliability emphasizes reproducibility across scenarios
(note types, specialties) and modalities (telehealth
vs. in-person, EHR variants). Implementation focuses on acceptability, usefulness in daily work,
and patient impact. Maintenance considers toollevel effects, like reduced burnout or unintended
consequences (over-reliance, skill atrophy).
In our evaluation framework, we prioritize these
evaluation dimensions because they draw from
long-standing clinical science (validity and reliability) and real-world mental health technology evaluation (implementation and maintenance), together
defining the minimum requirements for responsible
use in high-stakes mental health contexts.


**4** **Case Studies**


The following five case studies were selected to
illustrate the taxonomy across support types. They
were chosen for their representativeness, methodological rigor, and the variety of AI approaches
they exemplify, enabling a comprehensive demonstration of the taxonomy’s dimensions: _validity_,
_reliability_, _implementation_, and _maintenance_ .


**4.1** **Study I (** _**Assessment**_ **):** **LLM rating scales**
**for psychometric assessment of patient**
**engagement**


Eberhardt et al. (2025) introduced the LLM rating scale, a psychometric tool for automatically
transcribed psychotherapy sessions that measures
latent psychological constructs, such as patient en


gagement, by applying traditional psychometric
principles to AI-based assessment. The scale uses
structured items–prompts like “ _Please_ _rate_ _how_
_motivated the patient is to engage in therapy on a_
_scale from 0 to 100_ ”–to elicit zero-shot judgments
from the model. The study analyzed 1,131 sessions
from 155 patients using the DISCOVER framework (Hallmen et al., 2025), computing mean scale
scores from a large pool of manually developed
items, which were then evaluated for reliability and
multiple forms of validity.
Validity was assessed across multiple dimensions. Construct validity was supported by moderate, significant correlations between LLM rating scale scores and engagement determinants
like therapy motivation and between-session effort (Holdsworth et al., 2014). Criterion validity
was shown through associations with subsequent
therapy outcomes, where higher engagement predicted greater symptom improvement. Structural
validity was evaluated via multilevel confirmatory
factor analysis modeling a single latent factor, with
good fit (CFI = 0 _._ 968, SRMR = 0 _._ 022) though
RMSEA = 0 _._ 108 indicated some unexplained variance. Reliability was examined as the consistency
of the measurement across items, with internal consistency (McDonald’s _ω_ = 0 _._ 953) showing coherent and stable LLM responses.
The study demonstrated the psychometric soundness and potential of the LLM rating scale as an automated tool for psychotherapy research and feedback. Future work should extend analyses across
time and populations, assess robustness, fairness,
and safety (Lutz et al., 2024; Ryan et al., 2025), and
validate across contexts, languages, and constructs.
Implementation considerations, including presentation and integration (e.g., via XAI (Lavelle-Hill
et al., 2025)), affect real-world usefulness. Testing
within systems like the Trier Treatment Navigator (Lutz et al., 2024, 2025) can evaluate clinical
integration and early detection potential. Ongoing
maintenance is needed to monitor drift, bias, and
improvements with newer LLMs.


**4.2** **Study II (** _**Assessment**_ **):** **Natural language**
**response formats for assessing depression**
**and worry**


Gu et al. (2025) conducted a validity- and
reliability-based comparison of response formats
for LLM-based assessment of depression and
worry, building on prior work showing AI language
assessments can approach the reliability of human



5


scales (Kjell et al., 2022). The study compared
four response formats, from closed to open (predefined words, descriptive words, short phrases, fulltext responses), using a Sequential Evaluation with
Model Pre-Registration (SEMP) design. Models
were trained on a development set ( _N_ = 963) and
pre-registered before evaluation on a prospective
test set ( _N_ = 145) with validated scales, including the PHQ-9 (Spitzer et al., 1999) and GAD-7
(Spitzer et al., 2006). The results showed strong
convergent validity across formats, with correlations of _r_ = _._ 60- _._ 79, exceeding the pre-registered
threshold ( _r_ _>_ _._ 50). Combining all eight depression and worry models yielded correlations near
or above scale reliability limits (e.g., _r_ = _._ 83 for
CES-D vs. reliability _r_ = _._ 78), and incremental
validity analyses showed improved accuracy consistent with cognitive interview theory. However,
high inter-correlations among combined models
( _r_ = _._ 88- _._ 95) indicated reduced discriminant validity when the same responses were used to assess
both constructs.
Regarding reliability and implementation, twoweek test-retest correlations showed moderate to
strong stability, with performance generalizing well
to unseen data and prospective accuracies matching cross-validated estimates. Open-ended formats
showed internal consistency at the word level, with
depression- (e.g., “blue”) and worry-related (e.g.,
“anxious”) terms aligning with DSM-5 symptom
clusters (Diagnostic, 2013). Implementation effectiveness was demonstrated by predicting behavioral
indicators such as sick leave and mental healthrelated healthcare visits, often matching or exceeding standard rating scales. Feasibility analyses
showed that open formats provided richer information (Shannon diversity up to 561.0) but required
longer completion times (up to 4 times slower than
select-word tasks).
Overall, within the proposed taxonomy, this
work shows strong convergent, criterion, and external validity and temporal reliability, indicating that
well-designed LLM-based assessments can rival
traditional measures. However, discriminant validity and workflow feasibility remain open questions,
motivating future work on cross-population reliability and integration into digital clinical platforms.


**4.3** **Study III (** _**Intervention**_ **):** **Evaluating the**
**capabilities of LLMs vs.** **human therapists**
**to generate personalized interventions**


Bar-Shachar et al. (2025) developed an LLM-based



tool for generating context-sensitive therapeutic interventions during psychotherapy sessions. It uses
four specialized LLM agents, supportive, directive,
exploratory, and meaning-making, along with a
Judge-LLM that selects the most appropriate intervention based on the dialogue and the patient’s emotional and cognitive state. This setup reflects how
clinicians choose among multiple interventions and
tailor responses to patients’ evolving needs.
They evaluated the tool via human-AI comparisons on transcribed therapy segments, with both
therapists and the AI generating interventions that
expert clinicians rated for theoretical appropriateness, contextual fit, and helpfulness. High interrater reliability (ICC and Cohen’s _κ_ ) supported robustness, and AI interventions were generally clinically relevant and sometimes approached human
quality, though they lacked the depth and personalization of experienced clinicians.
Applying the taxonomy shows strong construct
validity and reliability, supported by theoretical
grounding and high rater agreement. However, ecological validity across therapies, languages, and
contexts, fairness across groups, and key implementation and maintenance issues, such as feasibility,
clinician acceptance, ethical oversight, model stability, and unintended effects, were not addressed.
Using the taxonomy, future evaluations could
go beyond expert ratings by testing validity across
modalities, populations, and contexts, examining
reliability across models and raters, and focusing on implementation through usability, clinicianpatient co-creation, and ethical integration. Ongoing maintenance would monitor drift, bias, and
unintended effects, including impacts on novice
therapists, ensuring the tool remains theoretically
sound, reliable, and clinically sustainable.


**4.4** **Study IV (** _**Intervention**_ **):** **A**
**clinically-grounded framework for**
**evaluating LM-assisted cognitive**
**restructuring**


Sharma et al. (2023, 2024) conducted a multi-stage
project to design, deploy, as well as evaluate a
human-LM interaction tool for cognitive restructuring, a core Cognitive Behavioral Therapy (CBT)
technique. Across all stages, the project integrated
clinical validity, ecological evaluation, safety, and
equity considerations.
The first stage defined and validated clinically
meaningful AI objectives. Working with mental
health professionals, the authors developed 7 lin


6


guistic attributes for reframing, including empathy,
positivity, actionability, specificity, and addressing thinking traps. To ensure clinical validity, 600
reframes were collected and annotated by practitioners. A randomized field study ( _N_ = 2 _,_ 067) on
the Mental Health America platform showed users
preferred highly empathic and specific reframes,
while overly positive ones were less effective.
Under the implementation dimension, the framework was operationalized into an interactive LMpowered tool supporting users in cognitive restructuring. Co-designed with mental health professionals, it included safety mechanisms such as classification and rule-based filtering, IRB approval,
and a user-reporting function, with flagged content (0.65%) confirming filter effectiveness. A
large-scale field study on the MHA website ( _N_ =
15 _,_ 531) evaluated user-reported outcomes, including emotional impact, therapeutic utility, and skill
acquisition. The tool showed measurable benefits,
with the majority of participants reporting reduced
negative emotion and helpfulness of reframes for
overcoming negative thoughts.
Under maintenance, the third stage assessed equity and found reduced effectiveness for adolescents aged 13-17. Targeted adaptations (simpler,
more casual reframes) improved helpfulness in
a follow-up trial without affecting other groups,
demonstrating ongoing monitoring and refinement.
This case study shows how a clinically grounded,
real-world evaluation framework centered on safety
and equity can produce a tool with measurable
utility. From a taxonomy perspective, it shows
validity (clinically aligned outcomes), reliability
(consistent effects), safety (content filtering and
user flagging), equity (targeted improvements), and
maintenance (iterative refinement). The tool has
since been deployed by Mental Health America,
serving over 160,000 users [7] .


**4.5** **Study V (** _**Information synthesis**_ **):**
**Hierarchical LLM-VAE tool for clinically**
**meaningful timeline summarization**


Song et al. (2024) proposed a hybrid tool that integrates hierarchical variational autoencoders (THVAEs) with LLMs to generate clinically meaningful summaries of long-term social media timelines.
It produces two layers: a first-person evidence
summary capturing subjective experiences, and a


[7https://screening.mhanational.org/](https://screening.mhanational.org/changing-thoughts-with-an-ai-assistant/)
[changing-thoughts-with-an-ai-assistant/](https://screening.mhanational.org/changing-thoughts-with-an-ai-assistant/)



third-person clinical summary mapping these experiences to diagnostic indicators, interpersonal
patterns, and moments of change. The goal is to
help clinicians and researchers synthesize key information from longitudinal mental health data.
Evaluation of the tool integrated both automatic
and expert-based components. Automatic metrics
assessed meaning preservation, factual consistency,
evidence appropriateness, coherence, and fluency.
Clinical experts rated summaries for usefulness,
diagnostic accuracy, and their ability to reflect dynamic psychological processes. Inter-rater agreement ensured the reliability of human judgments,
and ablation studies tested the contribution of specific model components, such as keyphrase extraction and expert-informed prompting.
Applying the proposed taxonomy shows that the
work addresses construct validity–alignment with
clinical constructs–and criterion validity through
correlations with expert judgments. It also touches
on reliability via inter-rater agreement. However,
because the tool was trained and evaluated only
on social media data, ecological validity and clinical generalizability is limited. Although the peersupport platform provides authentic language, selective self-disclosure gives the model only a partial
view of users’ psychological states. The authors
also acknowledge risks such as hallucinations, bias,
and unsafe inferences, but do not systematically
evaluate them, nor do they assess fairness across
demographic or linguistic groups. Implementation
and maintenance factors–such as clinical usability, practitioner acceptance, and long-term model
stability–were likewise not examined.
Future work could extend evaluation to generalizability, usability, and sustainability. Ecological
testing across cultures and clinical contexts, repeated assessments for reliability, clinician-focused
implementation studies, and ongoing monitoring
for drift or bias would support consistent performance, advancing the tool from proof of concept to
a clinically robust, ethical, and sustainable mental
health tool.


**5** **Moving Forward**


**Evaluation foundations and maturity pathways.**
Evaluation practices in AI for mental health remain concentrated in early-stage technical validation, with relatively few tools reaching implementation or maintenance. While this is typical for
an emerging field, it motivates the need for ex


7


plicit _minimum evaluation standards_ appropriate
for high-risk mental health contexts. Assessment
tools should demonstrate convergent and discriminant validity with clinical constructs. Intervention
tools should provide evidence of therapeutic benefit, safety, and acceptability, ideally supported by
prospective or randomized evaluations (Hofmann
and Weinberger, 2013; Cuijpers et al., 2019). Information synthesis tools should document measurable improvements in workflow, decision quality,
or clinical comprehension.
A robust evaluation strategy requires a multilayered, standardized pipeline, in which evaluation
depth increases with a tool’s intended role and potential harm. We distinguish three maturity layers:


1. **Early** **maturity** **(exploratory):** Technical
validation, including accuracy, robustness,
and agreement with human annotations, typically using retrospective datasets. At this
stage, evaluation supports feasibility assessment and hypothesis generation rather than
clinical claims.


2. **Intermediate** **maturity** **(validation):**
Human-centered evaluation, capturing
expert judgment, usability, acceptability,
and perceived clinical relevance, often
through prospective or external validation and
structured user studies.


3. **Advanced maturity (deployment):** Assessment of contextual and ecological characteristics, including workflow integration, feasibility across settings, long-term impact, equity,
safety, and monitoring of failure modes over
time.


This layered structure is particularly important
in mental health settings, where concerns about invasiveness, reduced human oversight, and potential
clinician deskilling are longstanding (Torous et al.,
2019).
**Safety, fairness, and adaptability.** Safety and fairness require proactive, domain-specific protocols
rather than retrospective checks. Because mental health involves power asymmetries and heightened risks of harm, AI support must be systematically stress-tested for hallucinations, inappropriate
reassurance, and biased outputs. Fairness assessments should examine performance across demographic, cultural, and linguistic groups, acknowledging that fairness definitions entail unavoidable



trade-offs (Kleinberg et al., 2016; Ryan et al., 2025).
Notable, most of our case studies lacked explicit
safety or fairness evaluations, highlighting a significant gap for future development. Recent advances
in mental health science impose additional requirements for adaptability. Clinical theory is shifting
from categorical diagnoses toward dimensional and
dynamic frameworks, including network-based and
dynamic-systems models that conceptualize mental health states as evolving systems of interacting components (Borsboom, 2017; Scheffer et al.,
2024; Ong et al., 2025). AI support must therefore
remain adaptable to evolving constructs and evidence, as theoretical advances directly shape evaluation targets, risk assessment, and patient safety.

**AI** **for** **mental** **health.** The taxonomy proposed
here links the tool type to appropriate evaluation requirements, guiding clinically aligned assessment.
It provides a framework for tailoring evaluation
to a tool’s intended function, potential risks, and
stage of development, supporting research across
both clinical and AI-focused venues. Its practical impact depends on integration into research
practices, including evaluation reporting and comparison across studies. As mental health science
increasingly adopts dimensional, network-based,
and dynamic perspectives, the constructs and outcomes used in evaluation will necessarily evolve,
reinforcing the need for adaptable and transparent evaluation frameworks. Operationalizing this
taxonomy requires shared infrastructure, including datasets with expert annotations, standardized
reporting practices, and reusable benchmarks, to
move from conceptual guidance to routine evaluation use. Near-term research should prioritize longitudinal validation, safety-critical failure testing,
and fairness auditing across diverse settings. The
aim is not simply improved model performance, but
evaluation practices that support safe, interpretable,
and context-aware mental health AI.


**6** **Conclusion**


Current evaluation practices for AI in mental health
are fragmented and often misaligned with clinical, social, and user-centered needs. By adopting an interdisciplinary framework and a taxonomy of assessment-, intervention-, and information synthesis-oriented tools, responsible evaluation can ensure AI is clinically meaningful, ethically grounded, and more likely to produce realworld impact in mental health care.



8


**Limitations**


This paper proposes a taxonomy and accompanying evaluation framework for mental health AI, but
several boundaries of scope should be noted. The
analysis is informed by a set of published case studies, which may not fully represent the breadth of
ongoing work or emerging AI for mental health
tools. The taxonomy and evaluation pathways are
conceptual rather than empirically validated, and
their applicability may vary across clinical, cultural, and linguistic contexts. Additionally, while
we outline key evaluation principles, we do not provide detailed operational metrics, leaving room for
future work to refine and adapt these ideas as the
field continues to develop.


**Acknowledgments**


The authors acknowledge the support of Schloss
Dagstuhl – Leibniz Center for Informatics through
the Dagstuhl Seminar ‘25361: Natural Language
Processing for Mental Health’.
This work was supported by the DYNAMIC
Center, funded through the LOEWE program of
the Hessian Ministry of Science and Arts (Grant
No. LOEWE/1/16/519/03/09.001(0009)/98),
and by the LOEWE Distinguished Chair
Ubiquitous Knowledge Processing, LOEWE
initiative, Hesse, Germany (Grant No.
LOEWE/4a//519/05/00.002(0002)/81). Additional support was provided in part by the
U.S. Centers for Disease Control and Prevention/National Institute for Occupational Safety
and Health (CDC/NIOSH) under Grant U01
OH012476, and by the German Research Foundation (Deutsche Forschungsgemeinschaft, DFG;
Grant Nos. 493169211 and 525286173). This
work was also partly supported by the National
Institutes of Health through Grants P50MH115838,
R01MH117172, and R01MH135488, as well
as by the American Foundation for Suicide
Prevention and the Betty and Gordon Moore
Foundation. Further support was provided by the
Excellence Cluster EXC3066 The Adaptive Mind,
the European Research Council (ERC) under
the European Union’s Horizon 2020 research
and innovation programme (Grant Agreement
No. 949944, INTEGRATOR), and the MUR
FARE 2020 initiative (Grant Agreement Prot.
R20YSMBZ8S, INDOMITA). One author is a
member of the Data and Marketing Insights Unit
of the Bocconi Institute for Data Science and



Analysis (BIDSA). This work was also supported
by Keystone grant funding from Responsible AI
UK (Grant No. EP/Y009800/1). This work was
also supported in part by the Research Ireland
Adapt Research Centre (grant 13/RC/2106_P2).


**References**


Nuredin Ali Abdelkadir, Charles Zhang, Ned Mayo, and
Stevie Chancellor. 2024. [Diverse perspectives, diver-](https://doi.org/10.18653/v1/2024.naacl-short.58)
gent models: [Cross-cultural evaluation of depression](https://doi.org/10.18653/v1/2024.naacl-short.58)
detection [on](https://doi.org/10.18653/v1/2024.naacl-short.58) Twitter. In _Proceedings_ _of_ _the_ _2024_
_Conference_ _of_ _the_ _North_ _American_ _Chapter_ _of_ _the_
_Association for Computational Linguistics:_ _Human_
_Language_ _Technologies_ _(Volume_ _2:_ _Short_ _Papers)_,
pages 672–680, Mexico City, Mexico. Association
for Computational Linguistics.


Aakash Kumar Agarwal, Saprativa Bhattacharjee, Mauli
Rastogi, Jemima S. Jacob, Biplab Banerjee, Rashmi
Gupta, and Pushpak Bhattacharyya. 2025. [ReDe-](https://doi.org/10.18653/v1/2025.emnlp-main.1758)
press: [A cognitive framework for detecting depres-](https://doi.org/10.18653/v1/2025.emnlp-main.1758)
[sion relapse from social media.](https://doi.org/10.18653/v1/2025.emnlp-main.1758) In _Proceedings of the_
_2025 Conference on Empirical Methods in Natural_
_Language Processing_, pages 34652–34670, Suzhou,
China. Association for Computational Linguistics.


Elham Aghakhani, Lu Wang, Karla T. Washington,
George Demiris, Jina Huh-Yoo, and Rezvaneh Rezapour. 2025. [From conversation to automation:](https://doi.org/10.18653/v1/2025.findings-acl.1292) Leveraging LLMs for [problem-solving](https://doi.org/10.18653/v1/2025.findings-acl.1292) therapy analysis.
In _Findings_ _of_ _the_ _Association_ _for_ _Computational_
_Linguistics:_ _ACL 2025_, pages 25189–25207, Vienna,
Austria. Association for Computational Linguistics.


Carlos Aguirre, Keith Harrigian, and Mark Dredze.
2021. Gender and racial [fairness](https://doi.org/10.18653/v1/2021.eacl-main.256) in depression re[search using social media.](https://doi.org/10.18653/v1/2021.eacl-main.256) In _Proceedings of the 16th_
_Conference of the European Chapter of the Associ-_
_ation for Computational Linguistics:_ _Main Volume_,
pages 2932–2949, Online. Association for Computational Linguistics.


Ankit Aich, Avery Quynh, Varsha Badal, Amy Pinkham,
Philip Harvey, Colin Depp, and Natalie Parde.
2022. Towards intelligent [clinically-informed](https://doi.org/10.18653/v1/2022.findings-emnlp.208) lan[guage analyses of people with bipolar disorder and](https://doi.org/10.18653/v1/2022.findings-emnlp.208)
[schizophrenia.](https://doi.org/10.18653/v1/2022.findings-emnlp.208) In _Findings_ _of_ _the_ _Association_ _for_
_Computational_ _Linguistics:_ _EMNLP_ _2022_, pages
2871–2887, Abu Dhabi, United Arab Emirates. Association for Computational Linguistics.


Mario Ezra Aragón, A. Pastor López-Monroy, Luis C.
González, David E. Losada, and Manuel Montes-y
Gómez. 2023. [DisorBERT: A double domain adapta-](https://doi.org/10.18653/v1/2023.acl-long.853)
tion model for detecting [signs](https://doi.org/10.18653/v1/2023.acl-long.853) of mental disorders
in [social](https://doi.org/10.18653/v1/2023.acl-long.853) media. In _Proceedings_ _of_ _the_ _61st_ _An-_
_nual Meeting of the Association for Computational_
_Linguistics (Volume 1:_ _Long Papers)_, pages 15305–
15318, Toronto, Canada. Association for Computational Linguistics.


Thushari Atapattu, Menasha Thilakaratne, Duc Nhan
Do, Mahen Herath, and Katrina E. Falkner. 2025.



9


Exploring the role of [mental](https://doi.org/10.18653/v1/2025.findings-acl.1069) health conversational
[agents in training medical students and professionals:](https://doi.org/10.18653/v1/2025.findings-acl.1069)
[A systematic literature review.](https://doi.org/10.18653/v1/2025.findings-acl.1069) In _Findings of the As-_
_sociation for Computational Linguistics:_ _ACL 2025_,
pages 20785–20798, Vienna, Austria. Association
for Computational Linguistics.


Simone Balloccu, Ehud Reiter, Karen Jia-Hui Li, Rafael
Sargsyan, Vivek Kumar, Diego Reforgiato, Daniele
Riboni, and Ondrej Dusek. 2024. [Ask the experts:](https://doi.org/10.18653/v1/2024.findings-emnlp.674)
[sourcing a high-quality nutrition counseling dataset](https://doi.org/10.18653/v1/2024.findings-emnlp.674)
[through human-AI collaboration.](https://doi.org/10.18653/v1/2024.findings-emnlp.674) In _Findings of the_
_Association for Computational Linguistics:_ _EMNLP_
_2024_, pages 11519–11545, Miami, Florida, USA.
Association for Computational Linguistics.


Yael Bar-Shachar, Dana Rafael, Anmol Goel, Ayal
Klein, Iryna Gurevych, and Dana Atzil-Slonim. 2025.
[Evaluating the capabilities of large language models](https://osf.io/pjhak/overview?view_only=2b72405451d54c33a4776aa2b20cb0c4)
(llms) versus human [therapists](https://osf.io/pjhak/overview?view_only=2b72405451d54c33a4776aa2b20cb0c4) to generate person[alized interventions.](https://osf.io/pjhak/overview?view_only=2b72405451d54c33a4776aa2b20cb0c4) Preprint on the Open Science
Framework.


Guanqun Bi, Zhuang Chen, Zhoufu Liu, Hongkai Wang,
Xiyao Xiao, Yuqiang Xie, Wen Zhang, Yongkang
Huang, Yuxuan Chen, Libiao Peng, and Minlie
Huang. 2025. [MAGI: Multi-agent guided interview](https://doi.org/10.18653/v1/2025.findings-acl.1278)
[for psychiatric assessment.](https://doi.org/10.18653/v1/2025.findings-acl.1278) In _Findings of the Asso-_
_ciation_ _for_ _Computational_ _Linguistics:_ _ACL_ _2025_,
pages 24898–24921, Vienna, Austria. Association
for Computational Linguistics.


Suhas Bn, Yash Mahajan, Dominik O. Mattioli, Andrew M. Sherrill, Rosa I. Arriaga, Christopher Wiese,
and Saeed Abdullah. 2025a. [The pursuit of empathy:](https://doi.org/10.18653/v1/2025.emnlp-main.1573)
[Evaluating small language models for PTSD dialogue](https://doi.org/10.18653/v1/2025.emnlp-main.1573)
[support.](https://doi.org/10.18653/v1/2025.emnlp-main.1573) In _Proceedings of the 2025 Conference on_
_Empirical Methods in Natural Language Processing_,
pages 30888–30910, Suzhou, China. Association for
Computational Linguistics.


Suhas Bn, Dominik O. Mattioli, Andrew M. Sherrill,
Rosa I. Arriaga, Christopher Wiese, and Saeed Abdullah. 2025b. [How real are synthetic therapy con-](https://doi.org/10.18653/v1/2025.findings-emnlp.1144)
versations? [evaluating fidelity in prolonged exposure](https://doi.org/10.18653/v1/2025.findings-emnlp.1144)
[dialogues.](https://doi.org/10.18653/v1/2025.findings-emnlp.1144) In _Findings of the Association for Compu-_
_tational_ _Linguistics:_ _EMNLP_ _2025_, pages 20986–
20995, Suzhou, China. Association for Computational Linguistics.


Rishi Bommasani. 2023. Evaluation for change. In
_Findings of the Association for Computational Lin-_
_guistics:_ _ACL_ _2023_, pages 8227–8239, Toronto,
Canada. Association for Computational Linguistics.


Denny Borsboom. 2017. [A network theory of mental](https://onlinelibrary.wiley.com/doi/full/10.1002/wps.20375)
[disorders.](https://onlinelibrary.wiley.com/doi/full/10.1002/wps.20375) _World psychiatry_, 16(1):5–13.


Layla Bouzoubaa, Elham Aghakhani, Max Song, Quang
Trinh, and Shadi Rezapour. 2024. [Decoding the nar-](https://doi.org/10.18653/v1/2024.findings-acl.367)
ratives: [Analyzing personal drug experiences shared](https://doi.org/10.18653/v1/2024.findings-acl.367)
[on Reddit.](https://doi.org/10.18653/v1/2024.findings-acl.367) In _Findings of the Association for Com-_
_putational Linguistics:_ _ACL 2024_, pages 6131–6148,
Bangkok, Thailand. Association for Computational
Linguistics.



Greg Buda, Ignacio J. Tripodi, Margaret Meagher, and
Elizabeth A. Olson. 2024. [Crisis counselor language](https://doi.org/10.18653/v1/2024.findings-emnlp.418)
[and perceived genuine concern in crisis conversations.](https://doi.org/10.18653/v1/2024.findings-emnlp.418)
In _Findings of the Association for Computational Lin-_
_guistics:_ _EMNLP_ _2024_, pages 7149–7160, Miami,
Florida, USA. Association for Computational Linguistics.


Mohit Chandra, Siddharth Sriraman, Gaurav Verma,
Harneet Singh Khanuja, Jose Suarez Campayo,
Zihang Li, Michael L. Birnbaum, and Munmun
De Choudhury. 2025. [Lived experience not found:](https://doi.org/10.18653/v1/2025.naacl-long.553)
[LLMs struggle to align with experts on addressing](https://doi.org/10.18653/v1/2025.naacl-long.553)
[adverse drug reactions from psychiatric medication](https://doi.org/10.18653/v1/2025.naacl-long.553)
[use.](https://doi.org/10.18653/v1/2025.naacl-long.553) In _Proceedings of the 2025 Conference of the_
_Nations of the Americas Chapter of the Association_
_for_ _Computational_ _Linguistics:_ _Human_ _Language_
_Technologies (Volume 1:_ _Long Papers)_, pages 11083–
11113, Albuquerque, New Mexico. Association for
Computational Linguistics.


Alicja Chaszczewicz, Raj Shah, Ryan Louie, Bruce
Arnow, Robert Kraut, and Diyi Yang. 2024. [Multi-](https://doi.org/10.18653/v1/2024.acl-long.227)
[level feedback generation with large language models](https://doi.org/10.18653/v1/2024.acl-long.227)
[for empowering novice peer counselors.](https://doi.org/10.18653/v1/2024.acl-long.227) In _Proceed-_
_ings of the 62nd Annual Meeting of the Association_
_for Computational Linguistics (Volume 1:_ _Long Pa-_
_pers)_, pages 4130–4161, Bangkok, Thailand. Association for Computational Linguistics.


Mingyu Chen, Jingkai Lin, Zhaojie Chu, Xiaofen Xing,
Yirong Chen, and Xiangmin Xu. 2025a. [CATCH: A](https://doi.org/10.18653/v1/2025.findings-emnlp.543)
[novel data synthesis framework for high therapy fi-](https://doi.org/10.18653/v1/2025.findings-emnlp.543)
[delity and memory-driven planning chain of thought](https://doi.org/10.18653/v1/2025.findings-emnlp.543)
in AI [counseling.](https://doi.org/10.18653/v1/2025.findings-emnlp.543) In _Findings_ _of_ _the_ _Association_
_for Computational Linguistics:_ _EMNLP 2025_, pages
10254–10286, Suzhou, China. Association for Computational Linguistics.


Siyuan Chen, Meilin Wang, Minghao Lv, Zhiling Zhang,
Juqianqian Juqianqian, Dejiyangla Dejiyangla, Yujia
Peng, Kenny Zhu, and Mengyue Wu. 2024a. [Map-](https://doi.org/10.18653/v1/2024.naacl-long.306)
[ping long-term causalities in psychiatric symptoma-](https://doi.org/10.18653/v1/2024.naacl-long.306)
[tology and life events from social media.](https://doi.org/10.18653/v1/2024.naacl-long.306) In _Proceed-_
_ings of the 2024 Conference of the North American_
_Chapter_ _of_ _the_ _Association_ _for_ _Computational_ _Lin-_
_guistics:_ _Human_ _Language_ _Technologies_ _(Volume_
_1:_ _Long_ _Papers)_, pages 5472–5487, Mexico City,
Mexico. Association for Computational Linguistics.


Siyuan Chen, Zhiling Zhang, Mengyue Wu, and Kenny
Zhu. 2023a. [Detection of multiple mental disorders](https://doi.org/10.18653/v1/2023.emnlp-main.562)
from social media with [two-stream](https://doi.org/10.18653/v1/2023.emnlp-main.562) psychiatric ex[perts.](https://doi.org/10.18653/v1/2023.emnlp-main.562) In _Proceedings_ _of_ _the_ _2023_ _Conference_ _on_
_Empirical Methods in Natural Language Processing_,
pages 9071–9084, Singapore. Association for Computational Linguistics.


Yujia Chen, Changsong Li, Yiming Wang, Tianjie Ju,
Qingqing Xiao, Nan Zhang, Zifan Kong, Peng Wang,
and Binyu Yan. 2025b. MIND: [Towards](https://doi.org/10.18653/v1/2025.findings-emnlp.499) immersive psychological [healing](https://doi.org/10.18653/v1/2025.findings-emnlp.499) with multi-agent inner
[dialogue.](https://doi.org/10.18653/v1/2025.findings-emnlp.499) In _Findings_ _of_ _the_ _Association_ _for_ _Com-_
_putational Linguistics:_ _EMNLP 2025_, pages 9380–
9413, Suzhou, China. Association for Computational
Linguistics.



10


Zhiyu Chen, Yujie Lu, and William Wang. 2023b. [Em-](https://doi.org/10.18653/v1/2023.findings-emnlp.284)
powering psychotherapy [with](https://doi.org/10.18653/v1/2023.findings-emnlp.284) large language models: [Cognitive distortion detection through diagnosis](https://doi.org/10.18653/v1/2023.findings-emnlp.284)
of thought prompting. In _Findings_ _of_ _the_ _Associa-_
_tion for Computational Linguistics:_ _EMNLP 2023_,
pages 4295–4304, Singapore. Association for Computational Linguistics.


Zhuang Chen, Jiawen Deng, Jinfeng Zhou, Jincenzi
Wu, Tieyun Qian, and Minlie Huang. 2024b. [De-](https://doi.org/10.18653/v1/2024.naacl-long.452)
[pression detection in clinical interviews with LLM-](https://doi.org/10.18653/v1/2024.naacl-long.452)
[empowered structural element graph.](https://doi.org/10.18653/v1/2024.naacl-long.452) In _Proceedings_
_of the 2024 Conference of the North American Chap-_
_ter of the Association for Computational Linguistics:_
_Human_ _Language_ _Technologies_ _(Volume_ _1:_ _Long_
_Papers)_, pages 8181–8194, Mexico City, Mexico. Association for Computational Linguistics.


Zhuohao Chen, Nikolaos Flemotomos, Zac Imel, David
Atkins, and Shrikanth Narayanan. 2022. [Leveraging](https://doi.org/10.18653/v1/2022.findings-emnlp.425)
open data and task [augmentation](https://doi.org/10.18653/v1/2022.findings-emnlp.425) to automated behavioral coding of [psychotherapy](https://doi.org/10.18653/v1/2022.findings-emnlp.425) conversations in
[low-resource scenarios.](https://doi.org/10.18653/v1/2022.findings-emnlp.425) In _Findings of the Associa-_
_tion for Computational Linguistics:_ _EMNLP 2022_,
pages 5787–5795, Abu Dhabi, United Arab Emirates.
Association for Computational Linguistics.


Jiale Cheng, Sahand Sabour, Hao Sun, Zhuang Chen,
and Minlie Huang. 2023. [PAL: Persona-augmented](https://doi.org/10.18653/v1/2023.findings-acl.34)
[emotional support conversation generation.](https://doi.org/10.18653/v1/2023.findings-acl.34) In _Find-_
_ings of the Association for Computational Linguis-_
_tics:_ _ACL_ _2023_, pages 535–554, Toronto, Canada.
Association for Computational Linguistics.


Ronald Jay Cohen, Pamela Montague, Linda Sue
Nathanson, and Mark E Swerdlik. 1988. _[Psychologi-](https://psycnet.apa.org/record/1996-97180-000)_
_cal testing:_ _[An introduction to tests & measurement.](https://psycnet.apa.org/record/1996-97180-000)_
Mayfield Publishing Co.


David A Cook and Thomas J Beckman. 2006. [Current](https://www.sciencedirect.com/science/article/pii/S0002934305010375)
[concepts in validity and reliability for psychometric](https://www.sciencedirect.com/science/article/pii/S0002934305010375)
instruments: [theory and application.](https://www.sciencedirect.com/science/article/pii/S0002934305010375) _The American_
_journal of medicine_, 119(2):166–e7.


Pablo Cruz-Gonzalez, Aaron Wan-Jia He, Elly PoPo
Lam, Ingrid Man Ching Ng, Mandy Wingman Li,
Rangchun Hou, Jackie Ngai-Man Chan, Yuvraj
Sahni, Nestor Vinas Guasch, Tiev Miller, and 1 others. 2025. [Artificial intelligence in mental health care:](https://www.cambridge.org/core/journals/psychological-medicine/article/artificial-intelligence-in-mental-health-care-a-systematic-review-of-diagnosis-monitoring-and-intervention-applications/04DBD2D05976C9B1873B475018695418)
a systematic review of [diagnosis,](https://www.cambridge.org/core/journals/psychological-medicine/article/artificial-intelligence-in-mental-health-care-a-systematic-review-of-diagnosis-monitoring-and-intervention-applications/04DBD2D05976C9B1873B475018695418) monitoring, and
intervention applications. _Psychological_ _medicine_,
55:e18.


Pim Cuijpers, Mirjam Reijnders, and Marcus JH
Huibers. 2019. [The role of common factors in psy-](https://www.annualreviews.org/content/journals/10.1146/annurev-clinpsy-050718-095424)
[chotherapy outcomes.](https://www.annualreviews.org/content/journals/10.1146/annurev-clinpsy-050718-095424) _Annual review of clinical psy-_
_chology_, 15(1):207–231.


Dorottya Demszky, Diyi Yang, David S Yeager, Christopher J Bryan, Margarett Clapper, Susannah Chandhok, Johannes C Eichstaedt, Cameron Hecht, Jeremy
Jamieson, Meghann Johnson, and 1 others. 2023. Using large language models in psychology. _Nature_
_Reviews Psychology_, 2(11):688–701.



Yang Deng, Wenxuan Zhang, Yifei Yuan, and Wai Lam.
2023. [Knowledge-enhanced](https://doi.org/10.18653/v1/2023.acl-long.225) mixed-initiative dialogue system for [emotional](https://doi.org/10.18653/v1/2023.acl-long.225) support conversations.
In _Proceedings_ _of_ _the_ _61st_ _Annual_ _Meeting_ _of_ _the_
_Association for Computational Linguistics (Volume_
_1:_ _Long Papers)_, pages 4079–4095, Toronto, Canada.
Association for Computational Linguistics.


AP Diagnostic. 2013. Statistical manual of mental disorders: Dsm-5 (ed.) washington. _DC:_ _American_
_Psychiatric Association_ .


Steffen T Eberhardt, Antonia Vehlen, Jana Schaffrath,
Brian Schwartz, Tobias Baur, Dominik Schiller, Tobias Hallmen, Elisabeth André, and Wolfgang Lutz.
2025. [Development and validation of large language](https://www.nature.com/articles/s41598-025-14923-y)
model rating scales for [automatically](https://www.nature.com/articles/s41598-025-14923-y) transcribed
psychological [therapy](https://www.nature.com/articles/s41598-025-14923-y) sessions. _Scientific_ _Reports_,
15(1):29541.


Aparna Elangovan, Ling Liu, Lei Xu, Sravan Babu Bodapati, and Dan Roth. 2024. [ConSiDERS-the-human](https://doi.org/10.18653/v1/2024.acl-long.63)
evaluation framework: [Rethinking human evaluation](https://doi.org/10.18653/v1/2024.acl-long.63)
[for generative large language models.](https://doi.org/10.18653/v1/2024.acl-long.63) In _Proceedings_
_of_ _the_ _62nd_ _Annual_ _Meeting_ _of_ _the_ _Association_ _for_
_Computational Linguistics (Volume 1:_ _Long Papers)_,
pages 1137–1160, Bangkok, Thailand. Association
for Computational Linguistics.


Yi Feng, Jiaqi Wang, Wenxuan Zhang, Zhuang Chen,
Shen Yutong, Xiyao Xiao, Minlie Huang, Liping
Jing, and Jian Yu. 2025. Reframe [your](https://doi.org/10.18653/v1/2025.emnlp-main.1245) life story:
[Interactive narrative therapist and innovative moment](https://doi.org/10.18653/v1/2025.emnlp-main.1245)
[assessment with large language models.](https://doi.org/10.18653/v1/2025.emnlp-main.1245) In _Proceed-_
_ings of the 2025 Conference on Empirical Methods in_
_Natural Language Processing_, pages 24495–24520,
Suzhou, China. Association for Computational Linguistics.


Saadia Gabriel, Isha Puri, Xuhai Xu, Matteo Malgaroli,
and Marzyeh Ghassemi. 2024. [Can AI relate:](https://doi.org/10.18653/v1/2024.findings-emnlp.120) Test[ing large language model response for mental health](https://doi.org/10.18653/v1/2024.findings-emnlp.120)
[support.](https://doi.org/10.18653/v1/2024.findings-emnlp.120) In _Findings of the Association for Computa-_
_tional Linguistics:_ _EMNLP 2024_, pages 2206–2221,
Miami, Florida, USA. Association for Computational
Linguistics.


Muskan Garg, Amirmohammad Shahbandegan, Amrit
Chadha, and Vijay Mago. 2023. [An annotated dataset](https://doi.org/10.18653/v1/2023.findings-acl.757)
[for explainable interpersonal risk factors of mental](https://doi.org/10.18653/v1/2023.findings-acl.757)
disturbance in [social](https://doi.org/10.18653/v1/2023.findings-acl.757) media posts. In _Findings_ _of_
_the Association for Computational Linguistics:_ _ACL_
_2023_, pages 11960–11969, Toronto, Canada. Association for Computational Linguistics.


Bhagesh Gaur, Karan Gupta, Aseem Srivastava, Manish Gupta, and Md Shad Akhtar. 2025. [Assess and](https://doi.org/10.18653/v1/2025.findings-emnlp.982)
prompt: [A generative RL framework for improving](https://doi.org/10.18653/v1/2025.findings-emnlp.982)
[engagement in online mental health communities.](https://doi.org/10.18653/v1/2025.findings-emnlp.982) In
_Findings of the Association for Computational Lin-_
_guistics: EMNLP 2025_, pages 18102–18118, Suzhou,
China. Association for Computational Linguistics.


Soumitra Ghosh, Gopendra Vikram Singh, Shambhavi
Shambhavi, Sabarna Choudhury, and Asif Ekbal.



11


2025. Just a scratch: [Enhancing LLM capabilities](https://doi.org/10.18653/v1/2025.acl-long.1330)
[for self-harm detection through intent differentiation](https://doi.org/10.18653/v1/2025.acl-long.1330)
[and emoji interpretation.](https://doi.org/10.18653/v1/2025.acl-long.1330) In _Proceedings of the 63rd_
_Annual Meeting of the Association for Computational_
_Linguistics (Volume 1:_ _Long Papers)_, pages 27428–
27445, Vienna, Austria. Association for Computational Linguistics.


Evangelia Gogoulou, Magnus Boman, Fehmi Ben Abdesslem, Nils Hentati Isacsson, Viktor Kaldo, and
Magnus Sahlgren. 2021. Predicting [treatment](https://doi.org/10.18653/v1/2021.eacl-main.46) outcome from patient [texts:the](https://doi.org/10.18653/v1/2021.eacl-main.46) case of Internet-based
[cognitive behavioural therapy.](https://doi.org/10.18653/v1/2021.eacl-main.46) In _Proceedings of the_
_16th Conference of the European Chapter of the Asso-_
_ciation for Computational Linguistics:_ _Main Volume_,
pages 575–580, Online. Association for Computational Linguistics.


Sujatha Gollapalli, Beng Ang, and See-Kiong Ng. 2023.

[Identifying Early Maladaptive Schemas from mental](https://doi.org/10.18653/v1/2023.findings-emnlp.792)
[health question texts.](https://doi.org/10.18653/v1/2023.findings-emnlp.792) In _Findings of the Association_
_for Computational Linguistics:_ _EMNLP 2023_, pages
11832–11843, Singapore. Association for Computational Linguistics.


Zhuojun Gu, Katarina Kjell, H Andrew Schwartz,
and Oscar Kjell. 2025. Natural [language](https://journals.sagepub.com/doi/full/10.1177/10731911251364022) response
formats for assessing [depression](https://journals.sagepub.com/doi/full/10.1177/10731911251364022) and worry with
large language models: A sequential evaluation
with model [pre-registration.](https://journals.sagepub.com/doi/full/10.1177/10731911251364022) _Assessment_, page
10731911251364022.


Tobias Hallmen, Dominik Schiller, Antonia Vehlen,
Steffen Eberhardt, Tobias Baur, Daksitha Withanage Don, Wolfgang Lutz, and Elisabeth André.
2025. Discover: a [data-driven](https://doi.org/10.3389/fdgth.2025.1638539) interactive system
[for comprehensive observation, visualization, and ex-](https://doi.org/10.3389/fdgth.2025.1638539)
ploration of [human](https://doi.org/10.3389/fdgth.2025.1638539) behavior. _Frontiers_ _in_ _Digital_
_Health_, Volume 7 - 2025.


Sarthak Harne, Monjoy Narayan Choudhury, Madhav Rao, T K Srikanth, Seema Mehrotra, Apoorva
Vashisht, Aarushi Basu, and Manjit Singh Sodhi.
2024. [CASE: Efficient curricular data pre-training](https://doi.org/10.18653/v1/2024.findings-emnlp.925)
[for building assistive psychology expert models.](https://doi.org/10.18653/v1/2024.findings-emnlp.925) In
_Findings of the Association for Computational Lin-_
_guistics:_ _EMNLP 2024_, pages 15769–15778, Miami,
Florida, USA. Association for Computational Linguistics.


Keith Harrigian, Carlos Aguirre, and Mark Dredze.
2020. [Do models of mental health based on social](https://doi.org/10.18653/v1/2020.findings-emnlp.337)
[media data generalize?](https://doi.org/10.18653/v1/2020.findings-emnlp.337) In _Findings of the Associa-_
_tion for Computational Linguistics:_ _EMNLP 2020_,
pages 3774–3788, Online. Association for Computational Linguistics.


Kilichbek Haydarov, Youssef Mohamed, Emilio Goldenhersch, Paul OCallaghan, Li-jia Li, and Mohamed
Elhoseiny. 2025. Towards [AI-assisted](https://doi.org/10.18653/v1/2025.emnlp-main.1664) psychotherapy: Emotion-guided [generative](https://doi.org/10.18653/v1/2025.emnlp-main.1664) interventions. In
_Proceedings_ _of_ _the_ _2025_ _Conference_ _on_ _Empirical_
_Methods_ _in_ _Natural_ _Language_ _Processing_, pages
32724–32743, Suzhou, China. Association for Computational Linguistics.



Amey Hengle, Atharva Kulkarni, Shantanu Deepak
Patankar, Madhumitha Chandrasekaran, Sneha
D’silva, Jemima S. Jacob, and Rashmi Gupta. 2024.
Still not quite there! [evaluating large language mod-](https://doi.org/10.18653/v1/2024.emnlp-main.931)
[els for comorbid mental health diagnosis.](https://doi.org/10.18653/v1/2024.emnlp-main.931) In _Proceed-_
_ings of the 2024 Conference on Empirical Methods in_
_Natural Language Processing_, pages 16698–16721,
Miami, Florida, USA. Association for Computational
Linguistics.


Anthony Hills, Talia Tseriotou, Xenia Miscouridou,
Adam Tsakalidis, and Maria Liakata. 2024. [Excit-](https://doi.org/10.18653/v1/2024.findings-acl.744)
ing mood changes: [A time-aware hierarchical trans-](https://doi.org/10.18653/v1/2024.findings-acl.744)
[former for change detection modelling.](https://doi.org/10.18653/v1/2024.findings-acl.744) In _Findings_
_of_ _the_ _Association_ _for_ _Computational_ _Linguistics:_
_ACL 2024_, pages 12526–12537, Bangkok, Thailand.
Association for Computational Linguistics.


Stefan G Hofmann and Joel Weinberger. 2013. _[The art](https://api.taylorfrancis.com/content/books/mono/download?identifierName=doi&identifierValue=10.4324/9780203943427&type=googlepdf)_
_[and science of psychotherapy](https://api.taylorfrancis.com/content/books/mono/download?identifierName=doi&identifierValue=10.4324/9780203943427&type=googlepdf)_ . Routledge.


Emma Holdsworth, Erica Bowen, Sarah Brown, and
Douglas Howat. 2014. Client [engagement](https://doi.org/10.1016/j.cpr.2014.06.004) in psy[chotherapeutic treatment and associations with client](https://doi.org/10.1016/j.cpr.2014.06.004)
characteristics, therapist characteristics, and treat[ment factors.](https://doi.org/10.1016/j.cpr.2014.06.004) _Clinical Psychology Review_, 34(5):428–
450.


Simin Hong, Jun Sun, and Hongyang Chen. 2025.

Third-person appraisal [agent:](https://doi.org/10.18653/v1/2025.findings-emnlp.1288) Simulating human
[emotional reasoning in text with large language mod-](https://doi.org/10.18653/v1/2025.findings-emnlp.1288)
[els.](https://doi.org/10.18653/v1/2025.findings-emnlp.1288) In _Findings_ _of_ _the_ _Association_ _for_ _Compu-_
_tational_ _Linguistics:_ _EMNLP_ _2025_, pages 23684–
23701, Suzhou, China. Association for Computational Linguistics.


Ben Hutchinson, Vinodkumar Prabhakaran, Emily Denton, Kellie Webster, Yu Zhong, and Stephen Denuyl.
2020. Social biases in NLP [models](https://doi.org/10.18653/v1/2020.acl-main.487) as barriers for
[persons with disabilities.](https://doi.org/10.18653/v1/2020.acl-main.487) In _Proceedings of the 58th_
_Annual Meeting of the Association for Computational_
_Linguistics_, pages 5491–5501, Online. Association
for Computational Linguistics.


Jiyue Jiang, Sheng Wang, Qintong Li, Lingpeng Kong,
and Chuan Wu. 2023. [A cognitive stimulation dia-](https://doi.org/10.18653/v1/2023.acl-long.593)
[logue system with multi-source knowledge fusion for](https://doi.org/10.18653/v1/2023.acl-long.593)
elders with [cognitive](https://doi.org/10.18653/v1/2023.acl-long.593) impairment. In _Proceedings_
_of_ _the_ _61st_ _Annual_ _Meeting_ _of_ _the_ _Association_ _for_
_Computational Linguistics (Volume 1:_ _Long Papers)_,
pages 10628–10640, Toronto, Canada. Association
for Computational Linguistics.


Swanie Juhng, Matthew Matero, Vasudha Varadarajan,
Johannes Eichstaedt, Adithya V Ganesan, and H. Andrew Schwartz. 2023. [Discourse-level](https://doi.org/10.18653/v1/2023.acl-short.128) representa[tions can improve prediction of degree of anxiety.](https://doi.org/10.18653/v1/2023.acl-short.128) In
_Proceedings_ _of_ _the_ _61st_ _Annual_ _Meeting_ _of_ _the_ _As-_
_sociation for Computational Linguistics (Volume 2:_
_Short Papers)_, pages 1500–1511, Toronto, Canada.
Association for Computational Linguistics.


Migyeong Kang, Goun Choi, Hyolim Jeon, Ji Hyun
An, Daejin Choi, and Jinyoung Han. 2024. [CURE:](https://doi.org/10.18653/v1/2024.emnlp-main.994)
[Context- and uncertainty-aware mental disorder de-](https://doi.org/10.18653/v1/2024.emnlp-main.994)
[tection.](https://doi.org/10.18653/v1/2024.emnlp-main.994) In _Proceedings of the 2024 Conference on_



12


_Empirical Methods in Natural Language Processing_,
pages 17924–17940, Miami, Florida, USA. Association for Computational Linguistics.


Mina Kian, Kaleen Shrestha, Katrin Fischer, Xiaoyuan
Zhu, Jonathan Ong, Aryan Trehan, Jessica Wang,
Gloria Chang, Séb Arnold, and Maja Mataric. 2025.
Using linguistic [entrainment](https://doi.org/10.18653/v1/2025.findings-naacl.430) to evaluate large language models for use in [cognitive](https://doi.org/10.18653/v1/2025.findings-naacl.430) behavioral ther[apy.](https://doi.org/10.18653/v1/2025.findings-naacl.430) In _Findings_ _of_ _the_ _Association_ _for_ _Computa-_
_tional Linguistics:_ _NAACL 2025_, pages 7724–7743,
Albuquerque, New Mexico. Association for Computational Linguistics.


Hyunjong Kim, Suyeon Lee, Yeongjae Cho, Eunseo
Ryu, Yohan Jo, Suran Seong, and Sungzoon Cho.
2025a. [KMI: A dataset of Korean motivational inter-](https://doi.org/10.18653/v1/2025.naacl-long.541)
[viewing dialogues for psychotherapy.](https://doi.org/10.18653/v1/2025.naacl-long.541) In _Proceedings_
_of the 2025 Conference of the Nations of the Amer-_
_icas Chapter of the Association for Computational_
_Linguistics:_ _Human Language Technologies (Volume_
_1:_ _Long Papers)_, pages 10803–10828, Albuquerque,
New Mexico. Association for Computational Linguistics.


Juhee Kim, Chunghu Mok, Jisun Lee, Hyang Sook Kim,
and Yohan Jo. 2025b. Dialogue [systems](https://doi.org/10.18653/v1/2025.acl-long.1395) for emo[tional support via value reinforcement.](https://doi.org/10.18653/v1/2025.acl-long.1395) In _Proceed-_
_ings of the 63rd Annual Meeting of the Association_
_for Computational Linguistics (Volume 1:_ _Long Pa-_
_pers)_, pages 28733–28766, Vienna, Austria. Association for Computational Linguistics.


Jun Seo Kim and Hye Hyeon Kim. 2025. [KoACD: The](https://doi.org/10.18653/v1/2025.findings-emnlp.1202)
[first Korean adolescent dataset for cognitive distor-](https://doi.org/10.18653/v1/2025.findings-emnlp.1202)
[tion analysis via role-switching multi-LLM negoti-](https://doi.org/10.18653/v1/2025.findings-emnlp.1202)
[ation.](https://doi.org/10.18653/v1/2025.findings-emnlp.1202) In _Findings_ _of_ _the_ _Association_ _for_ _Compu-_
_tational_ _Linguistics:_ _EMNLP_ _2025_, pages 22050–
22078, Suzhou, China. Association for Computational Linguistics.


Subin Kim, Hoonrae Kim, Heejin Do, and Gary Lee.
2025c. [Multimodal cognitive reframing therapy via](https://doi.org/10.18653/v1/2025.naacl-long.250)
[multi-hop psychotherapeutic reasoning.](https://doi.org/10.18653/v1/2025.naacl-long.250) In _Proceed-_
_ings_ _of_ _the_ _2025_ _Conference_ _of_ _the_ _Nations_ _of_ _the_
_Americas Chapter of the Association for Computa-_
_tional Linguistics:_ _Human Language Technologies_
_(Volume_ _1:_ _Long_ _Papers)_, pages 4863–4880, Albuquerque, New Mexico. Association for Computational Linguistics.


Subin Kim, Hoonrae Kim, Jihyun Lee, Yejin Jeon, and
Gary Lee. 2025d. MIRROR: [Multimodal](https://doi.org/10.18653/v1/2025.emnlp-main.751) cognitive reframing therapy [for](https://doi.org/10.18653/v1/2025.emnlp-main.751) rolling with resistance.
In _Proceedings_ _of_ _the_ _2025_ _Conference_ _on_ _Empir-_
_ical Methods in Natural Language Processing_, pages
14851–14880, Suzhou, China. Association for Computational Linguistics.


Oscar NE Kjell, Sverker Sikström, Katarina Kjell, and
H Andrew Schwartz. 2022. Natural [language](https://www.nature.com/articles/s41598-022-07520-w) ana[lyzed with ai-based transformers predict traditional](https://www.nature.com/articles/s41598-022-07520-w)
[subjective well-being measures approaching the the-](https://www.nature.com/articles/s41598-022-07520-w)
[oretical upper limits in accuracy.](https://www.nature.com/articles/s41598-022-07520-w) _Scientific reports_,
12(1):3918.



Jon Kleinberg, Sendhil Mullainathan, and Manish
Raghavan. 2016. Inherent [trade-offs](https://arxiv.org/abs/1609.05807) in the fair
determination of risk scores. _arXiv_ _preprint_
_arXiv:1609.05807_ .


Neema Kotonya and Francesca Toni. 2024. [Towards a](https://aclanthology.org/2024.lrec-main.1422/)
[framework for evaluating explanations in automated](https://aclanthology.org/2024.lrec-main.1422/)
fact [verification.](https://aclanthology.org/2024.lrec-main.1422/) In _Proceedings_ _of_ _the_ _2024_ _Joint_
_International Conference on Computational Linguis-_
_tics,_ _Language_ _Resources_ _and_ _Evaluation_ _(LREC-_
_COLING 2024)_, pages 16364–16377, Torino, Italia.
ELRA and ICCL.


Raja Kumar, Kishan Maharaj, Ashita Saxena, and Pushpak Bhattacharyya. 2024. [Mental disorder classifi-](https://doi.org/10.18653/v1/2024.findings-emnlp.639)
[cation via temporal representation of text.](https://doi.org/10.18653/v1/2024.findings-emnlp.639) In _Find-_
_ings of the Association for Computational Linguistics:_
_EMNLP 2024_, pages 10901–10916, Miami, Florida,
USA. Association for Computational Linguistics.


Gleb Kuzmin, Petr Strepetov, Maksim Stankevich, Natalia Chudova, Artem Shelmanov, and Ivan Smirnov.
2025. [Exploring large language models for detecting](https://doi.org/10.18653/v1/2025.emnlp-main.1752)
[mental disorders.](https://doi.org/10.18653/v1/2025.emnlp-main.1752) In _Proceedings of the 2025 Con-_
_ference on Empirical Methods in Natural Language_
_Processing_, pages 34523–34547, Suzhou, China. Association for Computational Linguistics.


Xiaochong Lan, Zhiguang Han, Yiming Cheng,
Li Sheng, Jie Feng, Chen Gao, and Yong Li. 2025.
[Depression detection on social media with large lan-](https://aclanthology.org/2025.emnlp-industry.151/)
[guage models.](https://aclanthology.org/2025.emnlp-industry.151/) In _Proceedings of the 2025 Confer-_
_ence_ _on_ _Empirical_ _Methods_ _in_ _Natural_ _Language_
_Processing:_ _Industry Track_, pages 2155–2171.


Rosa Lavelle-Hill, Gavin Smith, Hannah Deininger, and
Kou Murayama. 2025. [An explainable artificial intel-](https://psycnet.apa.org/fulltext/2026-46377-001.html)
[ligence handbook for psychologists:](https://psycnet.apa.org/fulltext/2026-46377-001.html) Methods, oppor[tunities, and challenges.](https://psycnet.apa.org/fulltext/2026-46377-001.html) _Psychological Methods_ .


Andrew Lee, Jonathan K. Kummerfeld, Larry An, and
Rada Mihalcea. 2021. [Micromodels](https://doi.org/10.18653/v1/2021.findings-emnlp.360) for efficient,
explainable, and [reusable](https://doi.org/10.18653/v1/2021.findings-emnlp.360) systems: A case study
on [mental](https://doi.org/10.18653/v1/2021.findings-emnlp.360) health. In _Findings_ _of_ _the_ _Association_
_for Computational Linguistics:_ _EMNLP 2021_, pages
4257–4272, Punta Cana, Dominican Republic. Association for Computational Linguistics.


Daeun Lee, Hyolim Jeon, Sejung Son, Chaewon Park,
Ji hyun An, Seungbae Kim, and Jinyoung Han. 2024a.
Detecting bipolar [disorder](https://doi.org/10.18653/v1/2024.naacl-long.278) from misdiagnosed ma[jor depressive disorder with mood-aware multi-task](https://doi.org/10.18653/v1/2024.naacl-long.278)
[learning.](https://doi.org/10.18653/v1/2024.naacl-long.278) In _Proceedings of the 2024 Conference of_
_the North American Chapter of the Association for_
_Computational Linguistics:_ _Human Language Tech-_
_nologies (Volume 1:_ _Long Papers)_, pages 4954–4970,
Mexico City, Mexico. Association for Computational
Linguistics.


Daeun Lee, Soyoung Park, Jiwon Kang, Daejin Choi,
and Jinyoung Han. 2020. [Cross-lingual](https://doi.org/10.18653/v1/2020.findings-emnlp.200) suicidal[oriented word embedding toward suicide prevention.](https://doi.org/10.18653/v1/2020.findings-emnlp.200)
In _Findings of the Association for Computational Lin-_
_guistics:_ _EMNLP_ _2020_, pages 2208–2217, Online.
Association for Computational Linguistics.



13


Gyeongeun Lee, Zhu Wang, Sathya N. Ravi, and Natalie
Parde. 2025. [From heart to words:](https://doi.org/10.18653/v1/2025.findings-acl.231) Generating em[pathetic responses via integrated figurative language](https://doi.org/10.18653/v1/2025.findings-acl.231)
[and semantic context signals.](https://doi.org/10.18653/v1/2025.findings-acl.231) In _Findings of the As-_
_sociation for Computational Linguistics:_ _ACL 2025_,
pages 4490–4502, Vienna, Austria. Association for
Computational Linguistics.


Suyeon Lee, Sunghwan Kim, Minju Kim, Dongjin
Kang, Dongil Yang, Harim Kim, Minseok Kang,
Dayi Jung, Min Hee Kim, Seungbeen Lee, KyongMee Chung, Youngjae Yu, Dongha Lee, and Jinyoung
Yeo. 2024b. Cactus: [Towards psychological counsel-](https://doi.org/10.18653/v1/2024.findings-emnlp.832)
[ing conversations using cognitive behavioral theory.](https://doi.org/10.18653/v1/2024.findings-emnlp.832)
In _Findings_ _of_ _the_ _Association_ _for_ _Computational_
_Linguistics:_ _EMNLP 2024_, pages 14245–14274, Miami, Florida, USA. Association for Computational
Linguistics.


Anqi Li, Yu Lu, Nirui Song, Shuai Zhang, Lizhi Ma,
and Zhenzhong Lan. 2024. [Understanding the thera-](https://doi.org/10.18653/v1/2024.findings-emnlp.69)
[peutic relationship between counselors and clients in](https://doi.org/10.18653/v1/2024.findings-emnlp.69)
[online text-based counseling using LLMs.](https://doi.org/10.18653/v1/2024.findings-emnlp.69) In _Find-_
_ings of the Association for Computational Linguistics:_
_EMNLP_ _2024_, pages 1280–1303, Miami, Florida,
USA. Association for Computational Linguistics.


Anqi Li, Lizhi Ma, Yaling Mei, Hongliang He, Shuai
Zhang, Huachuan Qiu, and Zhenzhong Lan. 2023.
Understanding client [reactions](https://doi.org/10.18653/v1/2023.acl-long.577) in online mental
health [counseling.](https://doi.org/10.18653/v1/2023.acl-long.577) In _Proceedings_ _of_ _the_ _61st_ _An-_
_nual Meeting of the Association for Computational_
_Linguistics (Volume 1:_ _Long Papers)_, pages 10358–
10376, Toronto, Canada. Association for Computational Linguistics.


Tong Li, Shu Yang, Junchao Wu, Jiyao Wei, Lijie Hu,
Mengdi Li, Derek F. Wong, Joshua R. Oltmanns, and
Di Wang. 2025. [Can large language models identify](https://doi.org/10.18653/v1/2025.findings-emnlp.998)
[implicit suicidal ideation?](https://doi.org/10.18653/v1/2025.findings-emnlp.998) an empirical evaluation.
In _Findings of the Association for Computational Lin-_
_guistics: EMNLP 2025_, pages 18392–18413, Suzhou,
China. Association for Computational Linguistics.


Inna Lin, Lucille Njoo, Anjalie Field, Ashish Sharma,
Katharina Reinecke, Tim Althoff, and Yulia Tsvetkov.
2022. Gendered mental [health](https://doi.org/10.18653/v1/2022.emnlp-main.139) stigma in masked
[language models.](https://doi.org/10.18653/v1/2022.emnlp-main.139) In _Proceedings of the 2022 Con-_
_ference on Empirical Methods in Natural Language_
_Processing_, pages 2152–2170, Abu Dhabi, United
Arab Emirates. Association for Computational Linguistics.


Inna Lin, Ashish Sharma, Christopher Rytting, Adam
Miner, Jina Suh, and Tim Althoff. 2024. [IMBUE: Im-](https://doi.org/10.18653/v1/2024.acl-long.47)
[proving interpersonal effectiveness through simula-](https://doi.org/10.18653/v1/2024.acl-long.47)
[tion and just-in-time feedback with human-language](https://doi.org/10.18653/v1/2024.acl-long.47)
model [interaction.](https://doi.org/10.18653/v1/2024.acl-long.47) In _Proceedings_ _of the_ _62nd_ _An-_
_nual Meeting of the Association for Computational_
_Linguistics (Volume 1:_ _Long Papers)_, pages 810–840,
Bangkok, Thailand. Association for Computational
Linguistics.


Shir Lissak, Nitay Calderon, Geva Shenkman, Yaakov
Ophir, Eyal Fruchter, Anat Brunstein Klomek, and



Roi Reichart. 2024. The colorful [future](https://doi.org/10.18653/v1/2024.naacl-long.113) of LLMs:
[Evaluating and improving LLMs as emotional sup-](https://doi.org/10.18653/v1/2024.naacl-long.113)
[porters for queer youth.](https://doi.org/10.18653/v1/2024.naacl-long.113) In _Proceedings of the 2024_
_Conference_ _of_ _the_ _North_ _American_ _Chapter_ _of_ _the_
_Association for Computational Linguistics:_ _Human_
_Language_ _Technologies_ _(Volume_ _1:_ _Long_ _Papers)_,
pages 2040–2079, Mexico City, Mexico. Association
for Computational Linguistics.


Siyang Liu, Bianca Brie, Wenda Li, Laura Biester, Andrew Lee, James Pennebaker, and Rada Mihalcea.
2025. Eeyore: Realistic [depression](https://doi.org/10.18653/v1/2025.findings-acl.707) simulation via
expert-in-the-loop [supervised](https://doi.org/10.18653/v1/2025.findings-acl.707) and preference opti[mization.](https://doi.org/10.18653/v1/2025.findings-acl.707) In _Findings of the Association for Compu-_
_tational Linguistics:_ _ACL 2025_, pages 13750–13770,
Vienna, Austria. Association for Computational Linguistics.


Siyang Liu, Naihao Deng, Sahand Sabour, Yilin Jia,
Minlie Huang, and Rada Mihalcea. 2023. [Task-](https://doi.org/10.18653/v1/2023.emnlp-main.944)
adaptive tokenization: [Enhancing long-form text gen-](https://doi.org/10.18653/v1/2023.emnlp-main.944)
[eration efficacy in mental health and beyond.](https://doi.org/10.18653/v1/2023.emnlp-main.944) In _Pro-_
_ceedings of the 2023 Conference on Empirical Meth-_
_ods in Natural Language Processing_, pages 15264–
15281, Singapore. Association for Computational
Linguistics.


Siyang Liu, Chujie Zheng, Orianna Demasi, Sahand
Sabour, Yu Li, Zhou Yu, Yong Jiang, and Minlie
Huang. 2021. Towards [emotional](https://aclanthology.org/2021.acl-long.269/) support dialog
[systems.](https://aclanthology.org/2021.acl-long.269/) In _Proceedings_ _of_ _the_ _59th_ _Annual_ _Meet-_
_ing of the Association for Computational Linguistics_
_and the 11th International Joint Conference on Natu-_
_ral Language Processing (Volume 1:_ _Long Papers)_,
pages 3469–3483.


Ryan Louie, Ananjan Nandi, William Fang, Cheng
Chang, Emma Brunskill, and Diyi Yang. 2024.
Roleplay-doh: Enabling domain-experts to create
[LLM-simulated patients via eliciting and adhering to](https://doi.org/10.18653/v1/2024.emnlp-main.591)
[principles.](https://doi.org/10.18653/v1/2024.emnlp-main.591) In _Proceedings of the 2024 Conference on_
_Empirical Methods in Natural Language Processing_,
pages 10570–10603, Miami, Florida, USA. Association for Computational Linguistics.


Daniel Lozoya, Alejandro Berazaluce, Juan Perches,
Eloy Lúa, Mike Conway, and Simon D’Alfonso.
2024. Generating mental [health](https://doi.org/10.18653/v1/2024.naacl-long.285) transcripts with
SAPE (Spanish [adaptive](https://doi.org/10.18653/v1/2024.naacl-long.285) prompt engineering). In
_Proceedings_ _of_ _the_ _2024_ _Conference_ _of_ _the_ _North_
_American Chapter of the Association for Computa-_
_tional Linguistics:_ _Human Language Technologies_
_(Volume 1:_ _Long Papers)_, pages 5096–5113, Mexico
City, Mexico. Association for Computational Linguistics.


Wolfgang Lutz, Brian Schwartz, Antonia Vehlen, Steffen T Eberhardt, and Jaime Delgadillo. 2025. [Ad-](https://pmc.ncbi.nlm.nih.gov/articles/PMC12434349/)
[vances in personalization of psychological interven-](https://pmc.ncbi.nlm.nih.gov/articles/PMC12434349/)
[tions.](https://pmc.ncbi.nlm.nih.gov/articles/PMC12434349/) _World Psychiatry_, 24(3):343.


Wolfgang Lutz, Antonia Vehlen, and Brian Schwartz.
2024. Data-informed [psychological](https://psycnet.apa.org/record/2025-41436-001) therapy,
[measurement-based care, and precision mental health.](https://psycnet.apa.org/record/2025-41436-001)
_Journal_ _of_ _Consulting_ _and_ _Clinical_ _Psychology_,
92(10):671.



14


Minghao Lv, Siyuan Chen, Haoan Jin, Minghao Yuan,
Qianqian Ju, Yujia Peng, Kenny Q. Zhu, and
Mengyue Wu. 2025. [Tracking life’s ups and downs:](https://doi.org/10.18653/v1/2025.acl-long.345)
[Mining life events from social media posts for mental](https://doi.org/10.18653/v1/2025.acl-long.345)
[health analysis.](https://doi.org/10.18653/v1/2025.acl-long.345) In _Proceedings of the 63rd Annual_
_Meeting_ _of_ _the_ _Association_ _for_ _Computational_ _Lin-_
_guistics (Volume 1:_ _Long Papers)_, pages 6950–6965,
Vienna, Austria. Association for Computational Linguistics.


Aaron Lyon, Sean A Munson, Madhu Reddy, Stephen M
Schueller, Elena Agapie, Svetlana Yarosh, Alex
Dopp, Ulrica von Thiele Schwarz, Gavin Doherty,
Andrea K Graham, and 1 others. 2023. [Bridging](https://dl.acm.org/doi/full/10.1145/3544549.3574132)
[hci and implementation science for innovation adop-](https://dl.acm.org/doi/full/10.1145/3544549.3574132)
[tion and public health impact.](https://dl.acm.org/doi/full/10.1145/3544549.3574132) In _Extended Abstracts_
_of the 2023 CHI Conference on Human Factors in_
_Computing Systems_, pages 1–7.


Zafarullah Mahmood, Soliman Ali, Jiading Zhu, Mohamed Abdelwahab, Michelle Yu Collins, Sihan
Chen, Yi Cheng Zhao, Jodi Wolff, Osnat C. Melamed,
Nadia Minian, Marta Maslej, Carolynne Cooper,
Matt Ratto, Peter Selby, and Jonathan Rose. 2025. [A](https://doi.org/10.18653/v1/2025.findings-acl.1283)
[fully generative motivational interviewing counsellor](https://doi.org/10.18653/v1/2025.findings-acl.1283)
[chatbot for moving smokers towards the decision to](https://doi.org/10.18653/v1/2025.findings-acl.1283)
[quit.](https://doi.org/10.18653/v1/2025.findings-acl.1283) In _Findings_ _of_ _the_ _Association_ _for_ _Computa-_
_tional Linguistics:_ _ACL 2025_, pages 25008–25043,
Vienna, Austria. Association for Computational Linguistics.


Patrick Meyer. 2010. _[Understanding measurement:](https://psycnet.apa.org/record/2010-09329-000)_ _re-_
_[liability](https://psycnet.apa.org/record/2010-09329-000)_ . Oxford University Press.


Do June Min, Verónica Pérez-Rosas, Kenneth Resnicow,
and Rada Mihalcea. 2022. [PAIR: Prompt-aware mar-](https://doi.org/10.18653/v1/2022.emnlp-main.11)
[gIn ranking for counselor reflection scoring in motiva-](https://doi.org/10.18653/v1/2022.emnlp-main.11)
[tional interviewing.](https://doi.org/10.18653/v1/2022.emnlp-main.11) In _Proceedings of the 2022 Con-_
_ference on Empirical Methods in Natural Language_
_Processing_, pages 148–158, Abu Dhabi, United Arab
Emirates. Association for Computational Linguistics.


Kshitij Mishra, Priyanshu Priya, Manisha Burja, and
Asif Ekbal. 2023a. [e-THERAPIST: I suggest you to](https://doi.org/10.18653/v1/2023.emnlp-main.861)
[cultivate a mindset of positivity and nurture uplifting](https://doi.org/10.18653/v1/2023.emnlp-main.861)
[thoughts.](https://doi.org/10.18653/v1/2023.emnlp-main.861) In _Proceedings_ _of_ _the_ _2023_ _Conference_
_on Empirical Methods in Natural Language Process-_
_ing_, pages 13952–13967, Singapore. Association for
Computational Linguistics.


Kshitij Mishra, Priyanshu Priya, and Asif Ekbal. 2023b.

PAL to lend a helping [hand:](https://doi.org/10.18653/v1/2023.acl-long.685) Towards building an
[emotion adaptive polite and empathetic counseling](https://doi.org/10.18653/v1/2023.acl-long.685)
[conversational agent.](https://doi.org/10.18653/v1/2023.acl-long.685) In _Proceedings of the 61st An-_
_nual Meeting of the Association for Computational_
_Linguistics (Volume 1:_ _Long Papers)_, pages 12254–
12271, Toronto, Canada. Association for Computational Linguistics.


Hongbin Na, Yining Hua, Zimu Wang, Tao Shen, Beibei
Yu, Lilin Wang, Wei Wang, John Torous, and Ling
Chen. 2025. [A survey of large language models in](https://doi.org/10.18653/v1/2025.findings-acl.385)
psychotherapy: [Current landscape and future direc-](https://doi.org/10.18653/v1/2025.findings-acl.385)
[tions.](https://doi.org/10.18653/v1/2025.findings-acl.385) In _Findings_ _of_ _the_ _Association_ _for_ _Compu-_
_tational Linguistics:_ _ACL 2025_, pages 7362–7376,



Vienna, Austria. Association for Computational Linguistics.


Thong Nguyen, Andrew Yates, Ayah Zirikly, Bart
Desmet, and Arman Cohan. 2022. [Improving](https://doi.org/10.18653/v1/2022.acl-long.578) the
[generalizability of depression detection by leverag-](https://doi.org/10.18653/v1/2022.acl-long.578)
ing clinical [questionnaires.](https://doi.org/10.18653/v1/2022.acl-long.578) In _Proceedings_ _of_ _the_
_60th Annual Meeting of the Association for Compu-_
_tational Linguistics (Volume 1:_ _Long Papers)_, pages
8446–8459, Dublin, Ireland. Association for Computational Linguistics.


Viet Cuong Nguyen, Mohammad Taher, Dongwan
Hong, Vinicius Konkolics Possobom, Vibha Thirunellayi Gopalakrishnan, Ekta Raj, Zihang Li, Heather J.
Soled, Michael L. Birnbaum, Srijan Kumar, and Munmun De Choudhury. 2025a. [Do large language mod-](https://doi.org/10.18653/v1/2025.findings-naacl.418)
[els align with core mental health counseling compe-](https://doi.org/10.18653/v1/2025.findings-naacl.418)
[tencies?](https://doi.org/10.18653/v1/2025.findings-naacl.418) In _Findings of the Association for Computa-_
_tional Linguistics:_ _NAACL 2025_, pages 7488–7511,
Albuquerque, New Mexico. Association for Computational Linguistics.


Vivian Nguyen, Sang Min Jung, Lillian Lee, Thomas D.
Hull, and Cristian Danescu-Niculescu-Mizil. 2024.
[Taking a turn for the better:](https://doi.org/10.18653/v1/2024.findings-emnlp.555) Conversation redirection
[throughout the course of mental-health therapy.](https://doi.org/10.18653/v1/2024.findings-emnlp.555) In
_Findings of the Association for Computational Lin-_
_guistics:_ _EMNLP_ _2024_, pages 9507–9521, Miami,
Florida, USA. Association for Computational Linguistics.


Vivian Nguyen, Lillian Lee, and Cristian DanescuNiculescu-Mizil. 2025b. Hanging in the balance:
[Pivotal moments in crisis counseling conversations.](https://doi.org/10.18653/v1/2025.acl-long.1440)
In _Proceedings_ _of_ _the_ _63rd_ _Annual_ _Meeting_ _of_ _the_
_Association for Computational Linguistics (Volume 1:_
_Long Papers)_, pages 29801–29817, Vienna, Austria.
Association for Computational Linguistics.


Clarissa W. Ong, Hiba Arnaout, Kate Sheehan, Estella Fox, Eugen Owtscharow, and Iryna Gurevych.
2025. Using large language models to create per[sonalized networks from therapy sessions.](https://arxiv.org/abs/2512.05836) _Preprint_,
arXiv:2512.05836.


Sungjoon Park, Kiwoong Park, Jaimeen Ahn, and Alice
Oh. 2020. Suicidal risk [detection](https://doi.org/10.18653/v1/2020.emnlp-main.198) for military per[sonnel.](https://doi.org/10.18653/v1/2020.emnlp-main.198) In _Proceedings of the 2020 Conference on_
_Empirical Methods in Natural Language Processing_
_(EMNLP)_, pages 2523–2531, Online. Association for
Computational Linguistics.


Priyanshu Priya, Gopendra Singh, Mauajama Firdaus,
Jyotsna Agrawal, and Asif Ekbal. 2024. [On the way](https://doi.org/10.18653/v1/2024.findings-naacl.290)
to gentle AI counselor: [Politeness cause elicitation](https://doi.org/10.18653/v1/2024.findings-naacl.290)
[and intensity tagging in code-mixed Hinglish conver-](https://doi.org/10.18653/v1/2024.findings-naacl.290)
sations for [social](https://doi.org/10.18653/v1/2024.findings-naacl.290) good. In _Findings_ _of_ _the_ _Associ-_
_ation for Computational Linguistics:_ _NAACL 2024_,
pages 4678–4696, Mexico City, Mexico. Association
for Computational Linguistics.


Huachuan Qiu, Hongliang He, Shuai Zhang, Anqi Li,
and Zhenzhong Lan. 2024a. [SMILE: Single-turn to](https://doi.org/10.18653/v1/2024.findings-emnlp.34)
[multi-turn inclusive language expansion via ChatGPT](https://doi.org/10.18653/v1/2024.findings-emnlp.34)



15


[for mental health support.](https://doi.org/10.18653/v1/2024.findings-emnlp.34) In _Findings of the Associ-_
_ation for Computational Linguistics:_ _EMNLP 2024_,
pages 615–636, Miami, Florida, USA. Association
for Computational Linguistics.


Huachuan Qiu and Zhenzhong Lan. 2025. [PsyDial:](https://doi.org/10.18653/v1/2025.acl-long.1049)
A large-scale long-term [conversational](https://doi.org/10.18653/v1/2025.acl-long.1049) dataset for
mental [health](https://doi.org/10.18653/v1/2025.acl-long.1049) support. In _Proceedings_ _of_ _the_ _63rd_
_Annual Meeting of the Association for Computational_
_Linguistics (Volume 1:_ _Long Papers)_, pages 21624–
21655, Vienna, Austria. Association for Computational Linguistics.


Huachuan Qiu, Lizhi Ma, and Zhenzhong Lan. 2024b.

[PsyGUARD: An automated system for suicide detec-](https://doi.org/10.18653/v1/2024.emnlp-main.264)
[tion and risk assessment in psychological counseling.](https://doi.org/10.18653/v1/2024.emnlp-main.264)
In _Proceedings_ _of_ _the_ _2024_ _Conference_ _on_ _Empiri-_
_cal Methods in Natural Language Processing_, pages
4581–4607, Miami, Florida, USA. Association for
Computational Linguistics.


Jiahao Qiu, Yinghui He, Xinzhe Juan, Yimin Wang,
Yuhan Liu, Zixin Yao, Yue Wu, Xun Jiang, Ling
Yang, and Mengdi Wang. 2025a. [EmoAgent:](https://doi.org/10.18653/v1/2025.emnlp-main.594) As[sessing and safeguarding human-AI interaction for](https://doi.org/10.18653/v1/2025.emnlp-main.594)
[mental health safety.](https://doi.org/10.18653/v1/2025.emnlp-main.594) In _Proceedings of the 2025 Con-_
_ference on Empirical Methods in Natural Language_
_Processing_, pages 11752–11767, Suzhou, China. Association for Computational Linguistics.


Wenyu Qiu, Yuxiong Wang, Jiajun Tan, Hanchao
Hou, Qinda Liu, Wei Yao, and Shiguang Ni. 2025b.
DeepWell-adol: A [scalable](https://doi.org/10.18653/v1/2025.emnlp-main.646) expert-based dialogue
[corpus for adolescent positive mental health and well-](https://doi.org/10.18653/v1/2025.emnlp-main.646)
[being promotion.](https://doi.org/10.18653/v1/2025.emnlp-main.646) In _Proceedings of the 2025 Con-_
_ference on Empirical Methods in Natural Language_
_Processing_, pages 12797–12821, Suzhou, China. Association for Computational Linguistics.


Federico Ravenda, Seyed Ali Bahrainian, Andrea Raballo, Antonietta Mira, and Noriko Kando. 2025. [Are](https://doi.org/10.18653/v1/2025.acl-long.440)
[LLMs effective psychological assessors?](https://doi.org/10.18653/v1/2025.acl-long.440) leveraging
[adaptive RAG for interpretable mental health screen-](https://doi.org/10.18653/v1/2025.acl-long.440)
[ing through psychometric practice.](https://doi.org/10.18653/v1/2025.acl-long.440) In _Proceedings_
_of_ _the_ _63rd_ _Annual_ _Meeting_ _of_ _the_ _Association_ _for_
_Computational Linguistics (Volume 1:_ _Long Papers)_,
pages 8975–8991, Vienna, Austria. Association for
Computational Linguistics.


Sandeep Reddy. 2024. [Generative ai in healthcare:](https://link.springer.com/article/10.1186/s13012-024-01357-9) an
[implementation science informed translational path](https://link.springer.com/article/10.1186/s13012-024-01357-9)
on application, [integration and governance.](https://link.springer.com/article/10.1186/s13012-024-01357-9) _Imple-_
_mentation Science_, 19(1):27.


Maor Reuben, Ortal Slobodin, Idan-Chaim Cohen,
Aviad Elyashar, Orna Braun-Lewensohn, Odeya Cohen, and Rami Puzis. 2025. [Assessment and manip-](https://doi.org/10.18653/v1/2025.acl-long.121)
[ulation of latent constructs in pre-trained language](https://doi.org/10.18653/v1/2025.acl-long.121)
[models using psychometric scales.](https://doi.org/10.18653/v1/2025.acl-long.121) In _Proceedings_
_of_ _the_ _63rd_ _Annual_ _Meeting_ _of_ _the_ _Association_ _for_
_Computational Linguistics (Volume 1:_ _Long Papers)_,
pages 2433–2444, Vienna, Austria. Association for
Computational Linguistics.


Cecil R Reynolds and RA Livingston. 2021. _[Mastering](https://link.springer.com/book/10.1007/978-3-030-59455-8)_
_[modern psychological testing](https://link.springer.com/book/10.1007/978-3-030-59455-8)_ . Springer.



Gony Rosenman, Talma Hendler, and Lior Wolf. 2024.

LLM questionnaire [completion](https://doi.org/10.18653/v1/2024.findings-emnlp.23) for automatic psy[chiatric assessment.](https://doi.org/10.18653/v1/2024.findings-emnlp.23) In _Findings of the Association_
_for Computational Linguistics:_ _EMNLP 2024_, pages
403–415, Miami, Florida, USA. Association for Computational Linguistics.


Seamus Ryan, Wanling Cai, Robert Bowman, and Gavin
Doherty. 2025. [Fairness challenges in the design of](https://doi.org/10.1145/3728368)
[machine learning applications for healthcare.](https://doi.org/10.1145/3728368) _ACM_
_Trans. Comput. Healthcare_, 6(4).


Archie Sage, Jeroen Keppens, and Helen Yannakoudakis. 2025. [A survey of cognitive distortion](https://doi.org/10.18653/v1/2025.findings-emnlp.804)
detection and [classification](https://doi.org/10.18653/v1/2025.findings-emnlp.804) in NLP. In _Findings_
_of_ _the_ _Association_ _for_ _Computational_ _Linguistics:_
_EMNLP 2025_, pages 14884–14899, Suzhou, China.
Association for Computational Linguistics.


Tulika Saha, Saichethan Reddy, Anindya Das, Sriparna
Saha, and Pushpak Bhattacharyya. 2022. [A shoulder](https://doi.org/10.18653/v1/2022.naacl-main.174)
to cry on: [Towards a motivational virtual assistant for](https://doi.org/10.18653/v1/2022.naacl-main.174)
[assuaging mental agony.](https://doi.org/10.18653/v1/2022.naacl-main.174) In _Proceedings of the 2022_
_Conference_ _of_ _the_ _North_ _American_ _Chapter_ _of_ _the_
_Association for Computational Linguistics:_ _Human_
_Language Technologies_, pages 2436–2449, Seattle,
United States. Association for Computational Linguistics.


Msvpj Sathvik, Zuhair Hasan Shaik, and Vivek Gupta.
2025. [M-help: Using social media data to detect men-](https://doi.org/10.18653/v1/2025.findings-emnlp.1225)
tal health [help-seeking](https://doi.org/10.18653/v1/2025.findings-emnlp.1225) signals. In _Findings_ _of_ _the_
_Association for Computational Linguistics:_ _EMNLP_
_2025_, pages 22510–22520, Suzhou, China. Association for Computational Linguistics.


Ramit Sawhney, Harshit Joshi, Lucie Flek, and Rajiv Ratn Shah. 2021a. [PHASE: Learning emotional](https://doi.org/10.18653/v1/2021.eacl-main.205)
[phase-aware representations for suicide ideation de-](https://doi.org/10.18653/v1/2021.eacl-main.205)
[tection on social media.](https://doi.org/10.18653/v1/2021.eacl-main.205) In _Proceedings of the 16th_
_Conference of the European Chapter of the Associ-_
_ation for Computational Linguistics:_ _Main Volume_,
pages 2415–2428, Online. Association for Computational Linguistics.


Ramit Sawhney, Harshit Joshi, Rajiv Ratn Shah, and Lucie Flek. 2021b. [Suicide ideation detection via social](https://doi.org/10.18653/v1/2021.naacl-main.176)
[and temporal user representations using hyperbolic](https://doi.org/10.18653/v1/2021.naacl-main.176)
[learning.](https://doi.org/10.18653/v1/2021.naacl-main.176) In _Proceedings of the 2021 Conference of_
_the North American Chapter of the Association for_
_Computational Linguistics:_ _Human Language Tech-_
_nologies_, pages 2176–2190, Online. Association for
Computational Linguistics.


Marten Scheffer, Claudi L Bockting, Denny Borsboom,
Roshan Cools, Clara Delecroix, Jessica A Hartmann, Kenneth S Kendler, Ingrid van de Leemput,
Han LJ Van Der Maas, Egbert van Nes, and 1 others.
2024. [A dynamical systems view of psychiatric disor-](https://jamanetwork.com/journals/jamapsychiatry/article-abstract/2817087)
[ders—theory: a review.](https://jamanetwork.com/journals/jamapsychiatry/article-abstract/2817087) _JAMA psychiatry_, 81(6):618–
623.


Raj Sanjay Shah, Lei Xu, Qianchu Liu, Jon Burnsky,
Andrew Bertagnolli, and Chaitanya Shivade. 2025.
TN-eval: [Rubric and evaluation protocols for mea-](https://doi.org/10.18653/v1/2025.acl-industry.14)
suring the quality of [behavioral](https://doi.org/10.18653/v1/2025.acl-industry.14) therapy notes. In



16


_Proceedings of the 63rd Annual Meeting of the As-_
_sociation for Computational Linguistics (Volume 6:_
_Industry Track)_, pages 179–199, Vienna, Austria. Association for Computational Linguistics.


Ashish Sharma, Adam Miner, David Atkins, and Tim Althoff. 2020. [A computational approach to understand-](https://doi.org/10.18653/v1/2020.emnlp-main.425)
[ing empathy expressed in text-based mental health](https://doi.org/10.18653/v1/2020.emnlp-main.425)
[support.](https://doi.org/10.18653/v1/2020.emnlp-main.425) In _Proceedings of the 2020 Conference on_
_Empirical Methods in Natural Language Processing_
_(EMNLP)_, pages 5263–5276, Online. Association for
Computational Linguistics.


Ashish Sharma, Kevin Rushton, Inna Lin, David Wadden, Khendra Lucas, Adam Miner, Theresa Nguyen,
and Tim Althoff. 2023. [Cognitive reframing of nega-](https://doi.org/10.18653/v1/2023.acl-long.555)
[tive thoughts through human-language model inter-](https://doi.org/10.18653/v1/2023.acl-long.555)
[action.](https://doi.org/10.18653/v1/2023.acl-long.555) In _Proceedings of the 61st Annual Meeting of_
_the Association for Computational Linguistics (Vol-_
_ume 1:_ _Long Papers)_, pages 9977–10000, Toronto,
Canada. Association for Computational Linguistics.


Ashish Sharma, Kevin Rushton, Inna Wanyin Lin,
Theresa Nguyen, and Tim Althoff. 2024. [Facilitat-](https://dl.acm.org/doi/full/10.1145/3613904.3642761)
[ing self-guided mental health interventions through](https://dl.acm.org/doi/full/10.1145/3613904.3642761)
[human-language model interaction:](https://dl.acm.org/doi/full/10.1145/3613904.3642761) A case study of
[cognitive restructuring.](https://dl.acm.org/doi/full/10.1145/3613904.3642761) In _Proceedings of the 2024_
_CHI_ _Conference_ _on_ _Human_ _Factors_ _in_ _Computing_
_Systems_, pages 1–29.


Heereen Shim. 2021. [Development of conversational](https://doi.org/10.18653/v1/2021.eacl-srw.17)
[AI for sleep coaching programme.](https://doi.org/10.18653/v1/2021.eacl-srw.17) In _Proceedings of_
_the 16th Conference of the European Chapter of the_
_Association for Computational Linguistics:_ _Student_
_Research Workshop_, pages 121–128, Online. Association for Computational Linguistics.


Jaemin Shin, Hyungjun Yoon, Seungjoo Lee, Sungjoon
Park, Yunxin Liu, Jinho Choi, and Sung-Ju Lee. 2023.
FedTherapist: [Mental health monitoring with user-](https://doi.org/10.18653/v1/2023.emnlp-main.734)
[generated linguistic expressions on smartphones via](https://doi.org/10.18653/v1/2023.emnlp-main.734)
[federated learning.](https://doi.org/10.18653/v1/2023.emnlp-main.734) In _Proceedings of the 2023 Con-_
_ference on Empirical Methods in Natural Language_
_Processing_, pages 11971–11988, Singapore. Association for Computational Linguistics.


Gopendra Vikram Singh, Sai Vardhan Vemulapalli,
Mauajama Firdaus, and Asif Ekbal. 2024. [Deci-](https://doi.org/10.18653/v1/2024.emnlp-main.1256)
[phering cognitive distortions in patient-doctor mental](https://doi.org/10.18653/v1/2024.emnlp-main.1256)
health conversations: [A multimodal LLM-based de-](https://doi.org/10.18653/v1/2024.emnlp-main.1256)
tection and [reasoning](https://doi.org/10.18653/v1/2024.emnlp-main.1256) framework. In _Proceedings_
_of_ _the_ _2024_ _Conference_ _on_ _Empirical_ _Methods_ _in_
_Natural Language Processing_, pages 22546–22570,
Miami, Florida, USA. Association for Computational
Linguistics.


Khushboo Singh, Vasudha Varadarajan, Adithya
V. Ganesan, August Håkan Nilsson, Nikita Soni,
Syeda Mahwish, Pranav Chitale, Ryan L. Boyd,
Lyle Ungar, Richard N. Rosenthal, and H. Andrew
Schwartz. 2025. Systematic [evaluation](https://doi.org/10.18653/v1/2025.findings-acl.971) of auto[encoding and large language model representations](https://doi.org/10.18653/v1/2025.findings-acl.971)
[for capturing author states and traits.](https://doi.org/10.18653/v1/2025.findings-acl.971) In _Findings of_
_the Association for Computational Linguistics:_ _ACL_
_2025_, pages 18955–18973, Vienna, Austria. Association for Computational Linguistics.



Karan Singla, Zhuohao Chen, David Atkins, and
Shrikanth Narayanan. 2020. Towards [end-2-end](https://doi.org/10.18653/v1/2020.acl-main.351)
[learning for predicting behavior codes from spoken](https://doi.org/10.18653/v1/2020.acl-main.351)
[utterances in psychotherapy conversations.](https://doi.org/10.18653/v1/2020.acl-main.351) In _Pro-_
_ceedings_ _of_ _the_ _58th_ _Annual_ _Meeting_ _of_ _the_ _Asso-_
_ciation for Computational Linguistics_, pages 3797–
3803, Online. Association for Computational Linguistics.


Hoyun Song, Huije Lee, Jisu Shin, Sukmin Cho,
Changgeon Ko, and Jong C. Park. 2025a. [Does](https://doi.org/10.18653/v1/2025.findings-acl.1119)
rationale quality matter? enhancing mental disor[der detection via selective reasoning distillation.](https://doi.org/10.18653/v1/2025.findings-acl.1119) In
_Findings of the Association for Computational Lin-_
_guistics:_ _ACL_ _2025_, pages 21738–21756, Vienna,
Austria. Association for Computational Linguistics.


Hoyun Song, Jisu Shin, Huije Lee, and Jong Park. 2023.

[A simple and flexible modeling for mental disorder](https://doi.org/10.18653/v1/2023.acl-long.681)
detection by learning [from](https://doi.org/10.18653/v1/2023.acl-long.681) clinical questionnaires.
In _Proceedings_ _of_ _the_ _61st_ _Annual_ _Meeting_ _of_ _the_
_Association for Computational Linguistics (Volume 1:_
_Long Papers)_, pages 12190–12206, Toronto, Canada.
Association for Computational Linguistics.


Jiayu Song, Mahmud Elahi Akhter, Dana Atzil-Slonim,
and Maria Liakata. 2025b. [Temporal reasoning for](https://doi.org/10.18653/v1/2025.acl-long.1362)
[timeline summarisation in social media.](https://doi.org/10.18653/v1/2025.acl-long.1362) In _Proceed-_
_ings of the 63rd Annual Meeting of the Association_
_for Computational Linguistics (Volume 1:_ _Long Pa-_
_pers)_, pages 28085–28101, Vienna, Austria. Association for Computational Linguistics.


Jiayu Song, Jenny Chim, Adam Tsakalidis, Julia Ive,
Dana Atzil-Slonim, and Maria Liakata. 2024. [Com-](https://doi.org/10.18653/v1/2024.findings-acl.873)
bining hierachical VAEs with LLMs for clinically
[meaningful timeline summarisation in social media.](https://doi.org/10.18653/v1/2024.findings-acl.873)
In _Findings of the Association for Computational Lin-_
_guistics:_ _ACL 2024_, pages 14651–14672, Bangkok,
Thailand. Association for Computational Linguistics.


Robert L Spitzer, Kurt Kroenke, Janet BW Williams,
Patient Health Questionnaire Primary Care Study
Group, and 1 others. 1999. [Validation and utility of](https://jamanetwork.com/journals/jama/fullarticle/192080)
[a self-report version of prime-md:](https://jamanetwork.com/journals/jama/fullarticle/192080) the phq primary
[care study.](https://jamanetwork.com/journals/jama/fullarticle/192080) _jama_, 282(18):1737–1744.


Robert L Spitzer, Kurt Kroenke, Janet BW Williams,
and Bernd Löwe. 2006. [A brief measure for assessing](https://jamanetwork.com/journals/jamainternalmedicine/fullarticle/410326)
[generalized anxiety disorder:](https://jamanetwork.com/journals/jamainternalmedicine/fullarticle/410326) the gad-7. _Archives of_
_internal medicine_, 166(10):1092–1097.


Aseem Srivastava, Smriti Joshi, Tanmoy Chakraborty,
and Md Shad Akhtar. 2024. [Knowledge planning in](https://doi.org/10.18653/v1/2024.emnlp-main.984)
[large language models for domain-aligned counseling](https://doi.org/10.18653/v1/2024.emnlp-main.984)
[summarization.](https://doi.org/10.18653/v1/2024.emnlp-main.984) In _Proceedings of the 2024 Confer-_
_ence on Empirical Methods in Natural Language Pro-_
_cessing_, pages 17775–17789, Miami, Florida, USA.
Association for Computational Linguistics.


Daniela Teodorescu, Tiffany Cheng, Alona Fyshe, and
Saif Mohammad. 2023. [Language and mental health:](https://doi.org/10.18653/v1/2023.emnlp-main.188)
[Measures of emotion dynamics from text as linguistic](https://doi.org/10.18653/v1/2023.emnlp-main.188)
[biosocial markers.](https://doi.org/10.18653/v1/2023.emnlp-main.188) In _Proceedings of the 2023 Con-_
_ference on Empirical Methods in Natural Language_



17


_Processing_, pages 3117–3133, Singapore. Association for Computational Linguistics.


Anja Thieme, Danielle Belgrave, and Gavin Doherty.
2020. [Machine learning in mental health:](https://doi.org/10.1145/3398069) A system[atic review of the HCI literature to support the devel-](https://doi.org/10.1145/3398069)
[opment of effective and implementable ML systems.](https://doi.org/10.1145/3398069)
_ACM Transactions on Computer-Human Interaction_,
27(5).


Roberto Tornero-Costa, Antonio Martinez-Millana,
Natasha Azzopardi-Muscat, Ledia Lazeri, Vicente
Traver, and David Novillo-Ortiz. 2023. [Methodolog-](https://mental.jmir.org/2023/1/e42045/)
[ical and quality flaws in the use of artificial intelli-](https://mental.jmir.org/2023/1/e42045/)
[gence in mental health research:](https://mental.jmir.org/2023/1/e42045/) systematic review.
_JMIR Mental Health_, 10(1):e42045.


John Torous, Hannah Wisniewski, Bruce Bird, Elizabeth Carpenter, Gary David, Eduardo Elejalde, Dan
Fulford, Synthia Guimond, Ryan Hays, Philip Henson, and 1 others. 2019. Creating a [digital](https://link.springer.com/article/10.1007/s41347-019-00095-w) health
[smartphone app and digital phenotyping platform for](https://link.springer.com/article/10.1007/s41347-019-00095-w)
[mental health and diverse healthcare needs:](https://link.springer.com/article/10.1007/s41347-019-00095-w) an inter[disciplinary and collaborative approach.](https://link.springer.com/article/10.1007/s41347-019-00095-w) _Journal of_
_Technology in Behavioral Science_, 4(2):73–85.


Adam Tsakalidis, Federico Nanni, Anthony Hills, Jenny
Chim, Jiayu Song, and Maria Liakata. 2022. [Identi-](https://doi.org/10.18653/v1/2022.acl-long.318)
[fying moments of change from longitudinal user text.](https://doi.org/10.18653/v1/2022.acl-long.318)
In _Proceedings_ _of_ _the_ _60th_ _Annual_ _Meeting_ _of_ _the_
_Association for Computational Linguistics (Volume_
_1:_ _Long Papers)_, pages 4647–4660, Dublin, Ireland.
Association for Computational Linguistics.


Talia Tseriotou, Adam Tsakalidis, Peter Foster, Terence
Lyons, and Maria Liakata. 2023. [Sequential](https://doi.org/10.18653/v1/2023.findings-acl.310) path
[signature networks for personalised longitudinal lan-](https://doi.org/10.18653/v1/2023.findings-acl.310)
[guage modeling.](https://doi.org/10.18653/v1/2023.findings-acl.310) In _Findings of the Association for_
_Computational Linguistics:_ _ACL 2023_, pages 5016–
5031, Toronto, Canada. Association for Computational Linguistics.


Adithya V Ganesan, Matthew Matero, Aravind Reddy
Ravula, Huy Vu, and H. Andrew Schwartz. 2021.
[Empirical evaluation of pre-trained transformers for](https://doi.org/10.18653/v1/2021.naacl-main.357)
[human-level NLP: The role of sample size and dimen-](https://doi.org/10.18653/v1/2021.naacl-main.357)
[sionality.](https://doi.org/10.18653/v1/2021.naacl-main.357) In _Proceedings of the 2021 Conference of_
_the North American Chapter of the Association for_
_Computational Linguistics:_ _Human Language Tech-_
_nologies_, pages 4515–4532, Online. Association for
Computational Linguistics.


Vasudha Varadarajan, Sverker Sikström, Oscar Kjell,
and H. Andrew Schwartz. 2024. [ALBA: Adaptive](https://doi.org/10.18653/v1/2024.naacl-long.136)
language-based [assessments](https://doi.org/10.18653/v1/2024.naacl-long.136) for mental health. In
_Proceedings_ _of_ _the_ _2024_ _Conference_ _of_ _the_ _North_
_American Chapter of the Association for Computa-_
_tional Linguistics:_ _Human Language Technologies_
_(Volume 1:_ _Long Papers)_, pages 2466–2478, Mexico
City, Mexico. Association for Computational Linguistics.


Krishnapriya Vishnubhotla, Daniela Teodorescu, Mallory J Feldman, Kristen Lindquist, and Saif M. Mohammad. 2024. [Emotion granularity from text:](https://doi.org/10.18653/v1/2024.emnlp-main.1069) An



aggregate-level [indicator](https://doi.org/10.18653/v1/2024.emnlp-main.1069) of mental health. In _Pro-_
_ceedings of the 2024 Conference on Empirical Meth-_
_ods in Natural Language Processing_, pages 19168–
19185, Miami, Florida, USA. Association for Computational Linguistics.


Bichen Wang, Pengfei Deng, Yanyan Zhao, and Bing
Qin. 2023a. C2D2 dataset: [A resource for the cog-](https://doi.org/10.18653/v1/2023.findings-emnlp.680)
nitive distortion analysis and its impact on mental
[health.](https://doi.org/10.18653/v1/2023.findings-emnlp.680) In _Findings_ _of_ _the_ _Association_ _for_ _Compu-_
_tational_ _Linguistics:_ _EMNLP_ _2023_, pages 10149–
10160, Singapore. Association for Computational
Linguistics.


Ming Wang, Peidong Wang, Lin Wu, Xiaocui Yang,
Daling Wang, Shi Feng, Yuxin Chen, Bixuan Wang,
and Yifei Zhang. 2025a. AnnaAgent: [Dynamic evo-](https://doi.org/10.18653/v1/2025.findings-acl.1192)
[lution agent system with multi-session memory for](https://doi.org/10.18653/v1/2025.findings-acl.1192)
[realistic seeker simulation.](https://doi.org/10.18653/v1/2025.findings-acl.1192) In _Findings of the Asso-_
_ciation_ _for_ _Computational_ _Linguistics:_ _ACL_ _2025_,
pages 23221–23235, Vienna, Austria. Association
for Computational Linguistics.


Ruiyi Wang, Stephanie Milani, Jamie C. Chiu, Jiayin
Zhi, Shaun M. Eack, Travis Labrum, Samuel M Murphy, Nev Jones, Kate V Hardy, Hong Shen, Fei Fang,
and Zhiyu Chen. 2024. PATIENT- _ψ_ [:](https://doi.org/10.18653/v1/2024.emnlp-main.711) Using large
language models to [simulate](https://doi.org/10.18653/v1/2024.emnlp-main.711) patients for training
[mental health professionals.](https://doi.org/10.18653/v1/2024.emnlp-main.711) In _Proceedings of the_
_2024 Conference on Empirical Methods in Natural_
_Language Processing_, pages 12772–12797, Miami,
Florida, USA. Association for Computational Linguistics.


Xiaoyi Wang, Jiwei Zhang, Guangtao Zhang, and Honglei Guo. 2025b. Feel the [difference?](https://doi.org/10.18653/v1/2025.findings-emnlp.1089) a comparative analysis of [emotional](https://doi.org/10.18653/v1/2025.findings-emnlp.1089) arcs in real and LLM[generated CBT sessions.](https://doi.org/10.18653/v1/2025.findings-emnlp.1089) In _Findings of the Associ-_
_ation for Computational Linguistics:_ _EMNLP 2025_,
pages 19999–20017, Suzhou, China. Association for
Computational Linguistics.


Zhong-Ling Wang, Po-Hsien Huang, Wen-Yau Hsu, and
Hen-Hsen Huang. 2023b. [Self-adapted utterance se-](https://doi.org/10.18653/v1/2023.eacl-main.105)
[lection for suicidal ideation detection in lifeline con-](https://doi.org/10.18653/v1/2023.eacl-main.105)
[versations.](https://doi.org/10.18653/v1/2023.eacl-main.105) In _Proceedings of the 17th Conference of_
_the European Chapter of the Association for Compu-_
_tational Linguistics_, pages 1436–1446, Dubrovnik,
Croatia. Association for Computational Linguistics.


Jason Wei, Kelly Finn, Emma Templeton, Thalia Wheatley, and Soroush Vosoughi. 2021. [Linguistic](https://doi.org/10.18653/v1/2021.naacl-main.352) com[plexity loss in text-based therapy.](https://doi.org/10.18653/v1/2021.naacl-main.352) In _Proceedings of_
_the 2021 Conference of the North American Chap-_
_ter of the Association for Computational Linguistics:_
_Human Language Technologies_, pages 4450–4459,
Online. Association for Computational Linguistics.


Mengxi Xiao, Qianqian Xie, Ziyan Kuang, Zhicheng
Liu, Kailai Yang, Min Peng, Weiguang Han, and
Jimin Huang. 2024. HealMe: [Harnessing cognitive](https://doi.org/10.18653/v1/2024.acl-long.93)
[reframing in large language models for psychother-](https://doi.org/10.18653/v1/2024.acl-long.93)
[apy.](https://doi.org/10.18653/v1/2024.acl-long.93) In _Proceedings of the 62nd Annual Meeting of_
_the Association for Computational Linguistics (Vol-_
_ume 1:_ _Long Papers)_, pages 1707–1725, Bangkok,
Thailand. Association for Computational Linguistics.



18


Haojie Xie, Yirong Chen, Xiaofen Xing, Jingkai Lin,
and Xiangmin Xu. 2025. PsyDT: [Using](https://doi.org/10.18653/v1/2025.acl-long.55) LLMs to
[construct the digital twin of psychological counselor](https://doi.org/10.18653/v1/2025.acl-long.55)
[with personalized counseling style for psychological](https://doi.org/10.18653/v1/2025.acl-long.55)
[counseling.](https://doi.org/10.18653/v1/2025.acl-long.55) In _Proceedings of the 63rd Annual Meet-_
_ing of the Association for Computational Linguistics_
_(Volume 1:_ _Long Papers)_, pages 1081–1115, Vienna,
Austria. Association for Computational Linguistics.


Yangyang Xu, Jinpeng Hu, Zhuoer Zhao, Zhangling
Duan, Xiao Sun, and Xun Yang. 2025. [MultiAgen-](https://doi.org/10.18653/v1/2025.emnlp-main.232)
[tESC: A LLM-based multi-agent collaboration frame-](https://doi.org/10.18653/v1/2025.emnlp-main.232)
[work for emotional support conversation.](https://doi.org/10.18653/v1/2025.emnlp-main.232) In _Proceed-_
_ings of the 2025 Conference on Empirical Methods_
_in Natural Language Processing_, pages 4665–4681,
Suzhou, China. Association for Computational Linguistics.


Shweta Yadav, Cornelia Caragea, Chenye Zhao, Naincy
Kumari, Marvin Solberg, and Tanmay Sharma. 2023.
Towards identifying [fine-grained](https://doi.org/10.18653/v1/2023.acl-long.495) depression symp[toms from memes.](https://doi.org/10.18653/v1/2023.acl-long.495) In _Proceedings of the 61st Annual_
_Meeting_ _of_ _the_ _Association_ _for_ _Computational_ _Lin-_
_guistics (Volume 1:_ _Long Papers)_, pages 8890–8905,
Toronto, Canada. Association for Computational Linguistics.


Chenghao Yang, Yudong Zhang, and Smaranda Muresan. 2021. [Weakly-supervised methods for suicide](https://doi.org/10.18653/v1/2021.acl-short.133)
[risk assessment: Role of related domains.](https://doi.org/10.18653/v1/2021.acl-short.133) In _Proceed-_
_ings of the 59th Annual Meeting of the Association for_
_Computational Linguistics and the 11th International_
_Joint Conference on Natural Language Processing_
_(Volume 2:_ _Short Papers)_, pages 1049–1057, Online.
Association for Computational Linguistics.


Jiamin Yang and David Jurgens. 2024. [Modeling em-](https://doi.org/10.18653/v1/2024.naacl-long.172)
[pathetic alignment in conversation.](https://doi.org/10.18653/v1/2024.naacl-long.172) In _Proceedings_
_of the 2024 Conference of the North American Chap-_
_ter of the Association for Computational Linguistics:_
_Human_ _Language_ _Technologies_ _(Volume_ _1:_ _Long_
_Papers)_, pages 3127–3148, Mexico City, Mexico. Association for Computational Linguistics.


Kailai Yang, Shaoxiong Ji, Tianlin Zhang, Qianqian
Xie, Ziyan Kuang, and Sophia Ananiadou. 2023. [To-](https://doi.org/10.18653/v1/2023.emnlp-main.370)
[wards interpretable mental health analysis with large](https://doi.org/10.18653/v1/2023.emnlp-main.370)
[language models.](https://doi.org/10.18653/v1/2023.emnlp-main.370) In _Proceedings of the 2023 Con-_
_ference on Empirical Methods in Natural Language_
_Processing_, pages 6056–6077, Singapore. Association for Computational Linguistics.


Qisen Yang, Zekun Wang, Honghui Chen, Shenzhi
Wang, Yifan Pu, Xin Gao, Wenhao Huang, Shiji
Song, and Gao Huang. 2024. [PsychoGAT: A novel](https://doi.org/10.18653/v1/2024.acl-long.779)
[psychological measurement paradigm through inter-](https://doi.org/10.18653/v1/2024.acl-long.779)
[active fiction games with LLM agents.](https://doi.org/10.18653/v1/2024.acl-long.779) In _Proceed-_
_ings of the 62nd Annual Meeting of the Association_
_for Computational Linguistics (Volume 1:_ _Long Pa-_
_pers)_, pages 14470–14505, Bangkok, Thailand. Association for Computational Linguistics.


Yizhe Yang, Palakorn Achananuparp, Heyan Huang,
Jing Jiang, Phey Ling Kit, Nicholas Gabriel Lim,
Cameron Tan Shi Ern, and Ee-Peng Lim. 2025a.



[CAMI: A counselor agent supporting motivational](https://doi.org/10.18653/v1/2025.acl-long.1024)
[interviewing through state inference and topic explo-](https://doi.org/10.18653/v1/2025.acl-long.1024)
[ration.](https://doi.org/10.18653/v1/2025.acl-long.1024) In _Proceedings of the 63rd Annual Meeting of_
_the Association for Computational Linguistics (Vol-_
_ume 1:_ _Long Papers)_, pages 21037–21081, Vienna,
Austria. Association for Computational Linguistics.


Yizhe Yang, Palakorn Achananuparp, Heyan Huang,
Jing Jiang, Nicholas Gabriel Lim, Cameron Tan Shi
Ern, Phey Ling Kit, Jenny Giam Xiuhui, John Pinto,
and Ee-Peng Lim. 2025b. [Consistent client simula-](https://doi.org/10.18653/v1/2025.acl-long.1021)
[tion for motivational interviewing-based counseling.](https://doi.org/10.18653/v1/2025.acl-long.1021)
In _Proceedings_ _of_ _the_ _63rd_ _Annual_ _Meeting_ _of_ _the_
_Association for Computational Linguistics (Volume 1:_
_Long Papers)_, pages 20959–20998, Vienna, Austria.
Association for Computational Linguistics.


Binwei Yao, Chao Shi, Likai Zou, Lingfeng Dai,
Mengyue Wu, Lu Chen, Zhen Wang, and Kai Yu.
2022. D4: [a Chinese dialogue dataset for depression-](https://doi.org/10.18653/v1/2022.emnlp-main.156)
[diagnosis-oriented chat.](https://doi.org/10.18653/v1/2022.emnlp-main.156) In _Proceedings of the 2022_
_Conference_ _on_ _Empirical_ _Methods_ _in_ _Natural_ _Lan-_
_guage_ _Processing_, pages 2438–2459, Abu Dhabi,
United Arab Emirates. Association for Computational Linguistics.


Sourabh Zanwar, Xiaofei Li, Daniel Wiechmann,
Yu Qiao, and Elma Kerz. 2023a. [What to fuse and](https://doi.org/10.18653/v1/2023.findings-acl.568)
how to fuse: [Exploring emotion and personality fu-](https://doi.org/10.18653/v1/2023.findings-acl.568)
sion strategies for [explainable](https://doi.org/10.18653/v1/2023.findings-acl.568) mental disorder de[tection.](https://doi.org/10.18653/v1/2023.findings-acl.568) In _Findings of the Association for Compu-_
_tational Linguistics:_ _ACL 2023_, pages 8926–8940,
Toronto, Canada. Association for Computational Linguistics.


Sourabh Zanwar, Daniel Wiechmann, Yu Qiao, and
Elma Kerz. 2023b. SMHD-GER: A large-scale
[benchmark dataset for automatic mental health detec-](https://doi.org/10.18653/v1/2023.findings-eacl.113)
[tion from social media in German.](https://doi.org/10.18653/v1/2023.findings-eacl.113) In _Findings of the_
_Association_ _for_ _Computational_ _Linguistics:_ _EACL_
_2023_, pages 1526–1541, Dubrovnik, Croatia. Association for Computational Linguistics.


Wei Zhai, Nan Bai, Qing Zhao, Jianqiang Li, Fan Wang,
Hongzhi Qi, Meng Jiang, Xiaoqin Wang, Bing Xiang
Yang, and Guanghui Fu. 2025. [MentalGLM series:](https://doi.org/10.18653/v1/2025.emnlp-main.686)
[Explainable large language models for mental health](https://doi.org/10.18653/v1/2025.emnlp-main.686)
analysis on [Chinese](https://doi.org/10.18653/v1/2025.emnlp-main.686) social media. In _Proceedings_
_of_ _the_ _2025_ _Conference_ _on_ _Empirical_ _Methods_ _in_
_Natural Language Processing_, pages 13599–13614,
Suzhou, China. Association for Computational Linguistics.


Wei Zhai, Hongzhi Qi, Qing Zhao, Jianqiang Li, Ziqi
Wang, Han Wang, Bing Yang, and Guanghui Fu.
2024. [Chinese MentalBERT: Domain-adaptive pre-](https://doi.org/10.18653/v1/2024.findings-acl.629)
[training on social media for Chinese mental health](https://doi.org/10.18653/v1/2024.findings-acl.629)
text [analysis.](https://doi.org/10.18653/v1/2024.findings-acl.629) In _Findings_ _of_ _the_ _Association_ _for_
_Computational Linguistics:_ _ACL 2024_, pages 10574–
10585, Bangkok, Thailand. Association for Computational Linguistics.


Enshi Zhang and Christian Poellabauer. 2025. [Mit-](https://doi.org/10.18653/v1/2025.findings-emnlp.650)
igating interviewer bias [in](https://doi.org/10.18653/v1/2025.findings-emnlp.650) multimodal depression
detection: [An approach with adversarial learning and](https://doi.org/10.18653/v1/2025.findings-emnlp.650)



19


contextual [positional](https://doi.org/10.18653/v1/2025.findings-emnlp.650) encoding. In _Findings_ _of_ _the_
_Association for Computational Linguistics:_ _EMNLP_
_2025_, pages 12169–12188, Suzhou, China. Association for Computational Linguistics.


Linhai Zhang, Ziyang Gao, Deyu Zhou, and Yulan He.
2025a. Explainable [depression](https://doi.org/10.18653/v1/2025.findings-acl.517) detection in clini[cal interviews with personalized retrieval-augmented](https://doi.org/10.18653/v1/2025.findings-acl.517)
[generation.](https://doi.org/10.18653/v1/2025.findings-acl.517) In _Findings of the Association for Com-_
_putational Linguistics:_ _ACL 2025_, pages 9927–9944,
Vienna, Austria. Association for Computational Linguistics.


Mian Zhang, Xianjun Yang, Xinlu Zhang, Travis
Labrum, Jamie C. Chiu, Shaun M. Eack, Fei Fang,
William Yang Wang, and Zhiyu Chen. 2025b. [CBT-](https://doi.org/10.18653/v1/2025.naacl-long.196)
bench: [Evaluating large language models on assist-](https://doi.org/10.18653/v1/2025.naacl-long.196)
ing cognitive [behavior](https://doi.org/10.18653/v1/2025.naacl-long.196) therapy. In _Proceedings_ _of_
_the 2025 Conference of the Nations of the Americas_
_Chapter_ _of_ _the_ _Association_ _for_ _Computational_ _Lin-_
_guistics:_ _Human Language Technologies (Volume 1:_
_Long Papers)_, pages 3864–3900, Albuquerque, New
Mexico. Association for Computational Linguistics.


Qiang Zhang, Jason Naradowsky, and Yusuke Miyao.
2023. Ask an expert: [Leveraging language models to](https://doi.org/10.18653/v1/2023.findings-acl.417)
[improve strategic reasoning in goal-oriented dialogue](https://doi.org/10.18653/v1/2023.findings-acl.417)
[models.](https://doi.org/10.18653/v1/2023.findings-acl.417) In _Findings of the Association for Compu-_
_tational Linguistics:_ _ACL 2023_, pages 6665–6694,
Toronto, Canada. Association for Computational Linguistics.


Xiangyu Zhang, Hexin Liu, Kaishuai Xu, Qiquan
Zhang, Daijiao Liu, Beena Ahmed, and Julien Epps.
2024. [When LLMs meets acoustic landmarks:](https://doi.org/10.18653/v1/2024.emnlp-main.8) An
[efficient approach to integrate speech into large lan-](https://doi.org/10.18653/v1/2024.emnlp-main.8)
[guage models for depression detection.](https://doi.org/10.18653/v1/2024.emnlp-main.8) In _Proceed-_
_ings of the 2024 Conference on Empirical Methods_
_in Natural Language Processing_, pages 146–158, Miami, Florida, USA. Association for Computational
Linguistics.


Xiangyu Zhang, Hexin Liu, Qiquan Zhang, Beena
Ahmed, and Julien Epps. 2025c. [SpeechT-RAG:](https://doi.org/10.18653/v1/2025.findings-acl.521)
[Reliable depression detection in LLMs with retrieval-](https://doi.org/10.18653/v1/2025.findings-acl.521)
[augmented generation using speech timing informa-](https://doi.org/10.18653/v1/2025.findings-acl.521)
[tion.](https://doi.org/10.18653/v1/2025.findings-acl.521) In _Findings_ _of_ _the_ _Association_ _for_ _Computa-_
_tional Linguistics:_ _ACL 2025_, pages 10019–10030,
Vienna, Austria. Association for Computational Linguistics.


Zhiling Zhang, Siyuan Chen, Mengyue Wu, and Kenny
Zhu. 2022. [Symptom identification for interpretable](https://doi.org/10.18653/v1/2022.emnlp-main.677)
[detection of multiple mental disorders on social me-](https://doi.org/10.18653/v1/2022.emnlp-main.677)
[dia.](https://doi.org/10.18653/v1/2022.emnlp-main.677) In _Proceedings of the 2022 Conference on Em-_
_pirical_ _Methods_ _in_ _Natural_ _Language_ _Processing_,
pages 9970–9985, Abu Dhabi, United Arab Emirates.
Association for Computational Linguistics.


Xinzhe Zheng, Sijie Ji, Jiawei Sun, Renqi Chen, Wei
Gao, and Mani Srivastava. 2025. [ProMind-LLM:](https://doi.org/10.18653/v1/2025.findings-acl.1033)
Proactive mental health [care](https://doi.org/10.18653/v1/2025.findings-acl.1033) via causal reasoning
[with sensor data.](https://doi.org/10.18653/v1/2025.findings-acl.1033) In _Findings of the Association for_
_Computational Linguistics:_ _ACL 2025_, pages 20150–
20171, Vienna, Austria. Association for Computational Linguistics.



Jinfeng Zhou, Yuxuan Chen, Jianing Yin, Yongkang
Huang, Yihan Shi, Xikun Zhang, Libiao Peng, Rongsheng Zhang, Tangjie Lv, Zhipeng Hu, Hongning
Wang, and Minlie Huang. 2025a. Crisp: Cogni[tive restructuring of negative thoughts through multi-](https://doi.org/10.18653/v1/2025.emnlp-main.1652)
turn [supportive](https://doi.org/10.18653/v1/2025.emnlp-main.1652) dialogues. In _Proceedings_ _of_ _the_
_2025 Conference on Empirical Methods in Natural_
_Language Processing_, pages 32462–32491, Suzhou,
China. Association for Computational Linguistics.


Naitian Zhou, David Bamman, and Isaac L. Bleaman.
2025b. Culture is not trivia: Sociocultural theory
for [cultural](https://doi.org/10.18653/v1/2025.acl-long.1256) NLP. In _Proceedings_ _of_ _the_ _63rd_ _An-_
_nual Meeting of the Association for Computational_
_Linguistics (Volume 1:_ _Long Papers)_, pages 25869–
25886, Vienna, Austria. Association for Computational Linguistics.


**A** **Details about the surveyed papers**


The full list of surveyed papers with the observed
practices are in Tables 3–16. Psychologically
grounded metrics are based on criteria derived
from psychological theory, clinical research, or expert input. AI/NLP metrics, by contrast, focus on
computational performance (e.g., accuracy, BLEU,
ROUGE) and are largely agnostic to psychological
or therapeutic soundness.
The tasks addressed in these papers are listed in
Table 17.
Some papers examine mental disorders at a
broad level, while others focus on specific diagnosed conditions. Among those that target specific conditions, the following named disorders are
examined: _Anxiety, Depression, Suicide ideation,_
_Cognitive distortions,_ _Post-Traumatic Stress Dis-_
_order_ _(PTSD),_ _Bipolar_ _Disorder,_ _Schizophrenia,_
_Self-harm,_ _Anorexia,_ _Trauma,_ _Stress,_ _Attention-_
_Deficit/Hyperactivity Disorder (ADHD), Obsessive-_
_Compulsive Disorder (OCD), Panic, and Addiction_ .



20


Paper Evaluation Human Expert Evaluation
metrics evaluation evaluators guidelines
provided



Discuss
limitations
of evaluation



Linguistic Complexity Loss in
Text-Based Therapy (Wei et al.,
2021)


Depression Detection in
Clinical Interviews with LLMEmpowered Structural Element
Graph (Chen et al., 2024b)


An Annotated Dataset for Explainable Interpersonal Risk Factors of Mental Disturbance in
Social Media Posts (Garg et al.,
2023)


Lived Experience Not Found:
LLMs Struggle to Align with
Experts on Addressing Adverse
Drug Reactions from Psychiatric
Medication Use (Chandra et al.,
2025)


Weakly-Supervised Methods for
Suicide Risk Assessment: Role
of Related Domains (Yang et al.,
2021)


Generating Mental Health
Transcripts with SAPE (Spanish
Adaptive Prompt Engineering) (Lozoya et al., 2024)



AI/NLP met- No No N. A. Yes
rics


AI/NLP met- No No N. A. No
rics


AI/NLP met- No No N. A. No
rics



Psychologically
grounded
metrics



Yes Yes Yes Yes



AI/NLP met- No No N. A. Yes
rics



Psychologically
grounded
metrics



Yes Yes No Yes



Suicidal Risk Detection for Mili- AI/NLP met- No No N. A. No
tary Personnel (Park et al., 2020) rics



C2D2 Dataset: A Resource for
the Cognitive Distortion Analysis and Its Impact on Mental
Health (Wang et al., 2023a)


Taking a turn for the better: Conversation redirection throughout
the course of mental-health therapy (Nguyen et al., 2024)


Towards Intelligent ClinicallyInformed Language Analyses of
People with Bipolar Disorder and
Schizophrenia (Aich et al., 2022)



AI/NLP met- No No N. A. Yes
rics



Psychologically
grounded
metrics



Yes No No Yes



AI/NLP met- No No N. A. Yes
rics



Table 3: List of surveyed papers _(part 1 of 14)_ .


21


Paper Evaluation Human Expert Evaluation
metrics evaluation evaluators guidelines
provided



Discuss
limitations
of evaluation



PAL: Persona-Augmented Emotional Support Conversation Generation (Cheng et al., 2023)


Towards end-2-end learning for
predicting behavior codes from
spoken utterances in psychotherapy conversations (Singla et al.,
2020)


Detecting Bipolar Disorder from
Misdiagnosed Major Depressive Disorder with Mood-Aware
Multi-Task Learning (Lee et al.,
2024a)



Psychologically
grounded
metrics



Yes No Yes Yes



AI/NLP met- No No N. A. No
rics


AI/NLP met- No No N. A. Yes
rics



Towards Emotional Support Dia- Psychologically
log Systems (Liu et al., 2021) grounded
metrics



Yes No Yes Yes



Mental Disorder Classification
via Temporal Representation of
Text (Kumar et al., 2024)


Discourse-Level Representations
can Improve Prediction of Degree of Anxiety (Juhng et al.,
2023)


Ask an Expert: Leveraging Language Models to Improve Strategic Reasoning in Goal-Oriented
Dialogue Models (Zhang et al.,
2023)


Empowering Psychotherapy with
Large Language Models: Cognitive Distortion Detection through
Diagnosis of Thought Prompting (Chen et al., 2023b)


Identifying Moments of
Change from Longitudinal User
Text (Tsakalidis et al., 2022)


Multi-Level Feedback Generation with Large Language Models for Empowering Novice Peer
Counselors (Chaszczewicz et al.,
2024)



AI/NLP met- No No N. A. No
rics


AI/NLP met- No No N. A. Yes
rics



Psychologically
grounded
metrics



Yes No Yes Yes



AI/NLP met- No No N. A. Yes
rics


AI/NLP met- Yes No Yes No
rics



Psychologically
grounded
metrics



Yes Yes Yes Yes



Table 4: List of surveyed papers _(part 2 of 14)_ .


22


Paper Evaluation Human Expert Evaluation
metrics evaluation evaluators guidelines
provided



Discuss
limitations
of evaluation



Using Linguistic Entrainment to
Evaluate Large Language Models for Use in Cognitive Behavioral Therapy (Kian et al., 2025)


Identifying Early Maladaptive
Schemas from Mental Health
Question Texts (Gollapalli et al.,
2023)


Understanding the Therapeutic Relationship between Counselors and Clients in Online
Text-based Counseling using
LLMs (Li et al., 2024)


Diverse Perspectives, Divergent
Models: Cross-Cultural Evaluation of Depression Detection on
Twitter (Abdelkadir et al., 2024)


PHASE: Learning Emotional
Phase-aware Representations for
Suicide Ideation Detection on
Social Media (Sawhney et al.,
2021a)


Improving the Generalizability
of Depression Detection by
Leveraging Clinical Questionnaires (Nguyen et al., 2022)


What to Fuse and How to Fuse:
Exploring Emotion and Personality Fusion Strategies for Explainable Mental Disorder Detection (Zanwar et al., 2023a)


Do Large Language Models Align with Core Mental
Health Counseling Competencies? (Nguyen et al., 2025a)


Cross-Lingual Suicidal-Oriented
Word Embedding toward Suicide
Prevention (Lee et al., 2020)


Understanding Client Reactions
in Online Mental Health Counseling (Li et al., 2023)



AI/NLP met- No No N. A. Yes
rics


AI/NLP met- No No N. A. Yes
rics



Psychologically
grounded
metrics



Yes Yes Yes Yes



AI/NLP met- No No N. A. No
rics


AI/NLP met- No No N. A. Yes
rics


AI/NLP met- No No N. A. Yes
rics


AI/NLP met- No No N. A. No
rics


AI/NLP met- No No N. A. Yes
rics


AI/NLP met- No No N. A. No
rics


AI/NLP met- No No N. A. Yes
rics



Table 5: List of surveyed papers _(part 3 of 14)_ .


23


Paper Evaluation Human Expert Evaluation
metrics evaluation evaluators guidelines
provided



Discuss
limitations
of evaluation



IMBUE: Improving Interpersonal
Effectiveness through Simulation
and Just-in-time Feedback with
Human-Language Model Interaction (Lin et al., 2024)


PsychoGAT: A Novel Psychological Measurement Paradigm
through Interactive Fiction Games
with LLM Agents (Yang et al.,
2024)


ALBA: Adaptive LanguageBased Assessments for Mental
Health (Varadarajan et al., 2024)


Ask the experts: sourcing a
high-quality nutrition counseling
dataset through Human-AI collaboration (Balloccu et al., 2024)


Cognitive Reframing of
Negative Thoughts through
Human-Language Model Interaction (Sharma et al., 2023)


A Computational Approach to Understanding Empathy Expressed
in Text-Based Mental Health Support (Sharma et al., 2020)


A Shoulder to Cry on: Towards A
Motivational Virtual Assistant for
Assuaging Mental Agony (Saha
et al., 2022)


Knowledge-enhanced Mixedinitiative Dialogue System for
Emotional Support Conversations (Deng et al., 2023)


Language and Mental Health:
Measures of Emotion Dynamics
from Text as Linguistic Biosocial
Markers (Teodorescu et al., 2023)


CURE: Context- and UncertaintyAware Mental Disorder Detection (Kang et al., 2024)



Psychologically
grounded
metrics


Psychologically
grounded
metrics



Yes Yes Yes Yes


Yes Yes No Yes



AI/NLP met- No No N. A. Yes
rics



Psychologically
grounded
metrics


Psychologically
grounded
metrics



Yes Yes Yes Yes


Yes Yes Yes Yes



AI/NLP met- No No N. A. No
rics


AI/NLP met- Yes No No No
rics



Psychologically
grounded
metrics



Yes No No Yes



AI/NLP met- No No N. A. Yes
rics


AI/NLP met- No No N. A. Yes
rics



Table 6: List of surveyed papers _(part 4 of 14)_ .


24


Paper Evaluation Human Expert Evaluation
metrics evaluation evaluators guidelines
provided



Discuss
limitations
of evaluation



Still Not Quite There! Evaluating Large Language Models for
Comorbid Mental Health Diagnosis (Hengle et al., 2024)


A Cognitive Stimulation
Dialogue System with Multisource Knowledge Fusion for
Elders with Cognitive Impairment (Jiang et al., 2023)


KMI: A Dataset of Korean Motivational Interviewing Dialogues
for Psychotherapy (Kim et al.,
2025a)


Combining Hierachical VAEs
with LLMs for clinically meaningful timeline summarisation in
social media (Song et al., 2024)


A Simple and Flexible Modeling
for Mental Disorder Detection by
Learning from Clinical Questionnaires (Song et al., 2023)


On the Way to Gentle AI Counselor: Politeness Cause Elicitation and Intensity Tagging in
Code-mixed Hinglish Conversations for Social Good (Priya et al.,
2024)


D4: a Chinese Dialogue Dataset
for Depression-DiagnosisOriented Chat (Yao et al., 2022)


Task-Adaptive Tokenization: Enhancing Long-Form Text Generation Efficacy in Mental Health
and Beyond (Liu et al., 2023)


Gendered Mental Health Stigma
in Masked Language Models (Lin et al., 2022)


LLM Questionnaire Completion
for Automatic Psychiatric Assessment (Rosenman et al., 2024)



AI/NLP met- No No N. A. Yes
rics



Psychologically
grounded
metrics


Psychologically
grounded
metrics


Psychologically
grounded
metrics



Yes No No No


Yes Yes Yes No


Yes Yes Yes Yes



AI/NLP met- No No N. A. Yes
rics


AI/NLP met- No No N. A. Yes
rics



Psychologically
grounded
metrics


Psychologically
grounded
metrics



Yes Yes No Yes


Yes Yes Yes No



AI/NLP met- No No N. A. Yes
rics


AI/NLP met- No No N. A. Yes
rics



Table 7: List of surveyed papers _(part 5 of 14)_ .


25


Paper Evaluation Human Expert Evaluation
metrics evaluation evaluators guidelines
provided



Discuss
limitations
of evaluation



Emotion Granularity from Text:
An Aggregate-Level Indicator
of Mental Health (Vishnubhotla
et al., 2024)


Leveraging Open Data and
Task Augmentation to Automated Behavioral Coding of
Psychotherapy Conversations in
Low-Resource Scenarios (Chen
et al., 2022)


CASE: Efficient Curricular Data
Pre-training for Building Assistive Psychology Expert Models (Harne et al., 2024)


Do Models of Mental Health
Based on Social Media Data Generalize? (Harrigian et al., 2020)


Self-Adapted Utterance Selection for Suicidal Ideation Detection in Lifeline Conversations (Wang et al., 2023b)


Can AI Relate: Testing Large
Language Model Response for
Mental Health Support (Gabriel
et al., 2024)


Suicide Ideation Detection via
Social and Temporal User Representations using Hyperbolic
Learning (Sawhney et al., 2021b)


PAIR: Prompt-Aware margIn
Ranking for Counselor Reflection Scoring in Motivational Interviewing (Min et al., 2022)


Crisis counselor language and
perceived genuine concern in crisis conversations (Buda et al.,
2024)


Empirical Evaluation of Pretrained Transformers for
Human-Level NLP: The Role of
Sample Size and Dimensionality (V Ganesan et al., 2021)



AI/NLP met- No No N. A. Yes
rics


AI/NLP met- No No N. A. No
rics


AI/NLP met- No No N. A. No
rics


AI/NLP met- No No N. A. No
rics


AI/NLP met- No No N. A. No
rics



Psychologically
grounded
metrics



Yes Yes Yes Yes



AI/NLP met- No No N. A. Yes
rics



Psychologically
grounded
metrics



Yes Yes Yes Yes



AI/NLP met- No No N. A. Yes
rics


AI/NLP met- No No N. A. No
rics



Table 8: List of surveyed papers _(part 6 of 14)_ .


26


Paper Evaluation Human Expert Evaluation
metrics evaluation evaluators guidelines
provided



Discuss
limitations
of evaluation



Roleplay-doh: Enabling
Domain-Experts to Create
LLM-simulated Patients via
Eliciting and Adhering to Principles (Louie et al., 2024)


Exciting Mood Changes: A
Time-aware Hierarchical Transformer for Change Detection
Modelling (Hills et al., 2024)


SMILE: Single-turn to Multiturn Inclusive Language Expansion via ChatGPT for Mental Health Support (Qiu et al.,
2024a)


PsyGUARD: An Automated System for Suicide Detection and
Risk Assessment in Psychological Counseling (Qiu et al.,
2024b)


FedTherapist: Mental Health
Monitoring with User-Generated
Linguistic Expressions on Smartphones via Federated Learning (Shin et al., 2023)


Modeling Empathetic Alignment
in Conversation (Yang and Jurgens, 2024)


Towards Interpretable Mental
Health Analysis with Large Language Models (Yang et al., 2023)


Multimodal Cognitive Reframing Therapy via Multi-hop Psychotherapeutic Reasoning (Kim
et al., 2025c)


SMHD-GER: A Large-Scale
Benchmark Dataset for Automatic Mental Health Detection
from Social Media in German (Zanwar et al., 2023b)


Towards Identifying FineGrained Depression Symptoms
from Memes (Yadav et al., 2023)



Psychologically
grounded
metrics



Yes Yes Yes Yes



AI/NLP met- Yes No Yes No
rics



Psychologically
grounded
metrics



Yes Yes Yes Yes



AI/NLP met- No No N. A. No
rics


AI/NLP met- No No N. A. Yes
rics


AI/NLP met- No No N. A. Yes
rics


AI/NLP met- Yes No Yes No
rics



Psychologically
grounded
metrics



Yes Yes Yes Yes



AI/NLP met- No No N. A. No
rics


AI/NLP met- Yes No No Yes
rics



Table 9: List of surveyed papers _(part 7 of 14)_ .


27


Paper Evaluation Human Expert Evaluation
metrics evaluation evaluators guidelines
provided



Discuss
limitations
of evaluation



Mapping Long-term Causalities
in Psychiatric Symptomatology
and Life Events from Social Media (Chen et al., 2024a)


Symptom Identification for Interpretable Detection of Multiple
Mental Disorders on Social Media (Zhang et al., 2022)


Gender and Racial Fairness in
Depression Research using Social Media (Aguirre et al., 2021)


CBT-Bench: Evaluating Large
Language Models on Assisting Cognitive Behavior Therapy (Zhang et al., 2025b)


e-THERAPIST: I suggest you
to cultivate a mindset of positivity and nurture uplifting
thoughts (Mishra et al., 2023a)


Knowledge Planning in Large
Language Models for DomainAligned Counseling Summarization (Srivastava et al., 2024)


PATIENT- _ψ_ : Using Large Language Models to Simulate Patients for Training Mental Health
Professionals (Wang et al., 2024)


Deciphering Cognitive Distortions in Patient-Doctor
Mental Health Conversations:
A Multimodal LLM-Based
Detection and Reasoning Framework (Singh et al., 2024)


Sequential Path Signature Networks for Personalised Longitudinal Language Modeling (Tseriotou et al., 2023)


DisorBERT: A Double Domain
Adaptation Model for Detecting
Signs of Mental Disorders in Social Media (Aragón et al., 2023)



AI/NLP met- No No N. A. No
rics


AI/NLP met- No No N. A. Yes
rics


AI/NLP met- No No N. A. Yes
rics



Psychologically
grounded
metrics


Psychologically
grounded
metrics


Psychologically
grounded
metrics


Psychologically
grounded
metrics



Yes Yes Yes Yes


Yes No No No


Yes Yes Yes Yes


Yes Yes Yes Yes



AI/NLP met- Yes No Yes Yes
rics


AI/NLP met- Yes No Yes No
rics


AI/NLP met- No No N. A. No
rics



Table 10: List of surveyed papers _(part 8 of 14)_ .


28


Paper Evaluation Human Expert Evaluation
metrics evaluation evaluators guidelines
provided



Discuss
limitations
of evaluation



Cactus: Towards Psychological Counseling Conversations using Cognitive Behavioral Theory (Lee et al., 2024b)


Development of Conversational
AI for Sleep Coaching Programme (Shim, 2021)


Social Biases in NLP Models as
Barriers for Persons with Disabilities (Hutchinson et al., 2020)


Chinese MentalBERT: DomainAdaptive Pre-training on Social
Media for Chinese Mental Health
Text Analysis (Zhai et al., 2024)


Micromodels for Efficient, Explainable, and Reusable Systems: A Case Study on Mental
Health (Lee et al., 2021)


HealMe: Harnessing Cognitive
Reframing in Large Language
Models for Psychotherapy (Xiao
et al., 2024)


PAL to Lend a Helping Hand:
Towards Building an Emotion
Adaptive Polite and Empathetic
Counseling Conversational
Agent (Mishra et al., 2023b)


Predicting Treatment Outcome
from Patient Texts:The Case
of Internet-Based Cognitive Behavioural Therapy (Gogoulou
et al., 2021)


Detection of Multiple Mental
Disorders from Social Media
with Two-Stream Psychiatric Experts (Chen et al., 2023a)


When LLMs Meets Acoustic
Landmarks: An Efficient Approach to Integrate Speech into
Large Language Models for Depression Detection (Zhang et al.,
2024)



Psychologically
grounded
metrics



Yes Yes Yes No



AI/NLP met- No No N. A. No
rics


AI/NLP met- No No N. A. Yes
rics


AI/NLP met- No No N. A. No
rics


AI/NLP met- No No N. A. No
rics



Psychologically
grounded
metrics


Psychologically
grounded
metrics



Yes Yes Yes No


Yes Yes No No



AI/NLP met- No No N. A. Yes
rics


AI/NLP met- No No N. A. No
rics


AI/NLP met- No No N. A. No
rics



Table 11: List of surveyed papers _(part 9 of 14)_ .


29


Paper Evaluation Human Expert Evaluation
metrics evaluation evaluators guidelines
provided



Discuss
limitations
of evaluation



The Colorful Future of LLMs:
Evaluating and Improving LLMs
as Emotional Supporters for Queer
Youth (Lissak et al., 2024)


Decoding the Narratives: Analyzing Personal Drug Experiences
Shared on Reddit (Bouzoubaa
et al., 2024)


A Fully Generative Motivational
Interviewing Counsellor Chatbot
for Moving Smokers Towards the
Decision to Quit (Mahmood et al.,
2025)


PsyDial: A Large-scale Long-term
Conversational Dataset for Mental Health Support (Qiu and Lan,
2025)


SpeechT-RAG: Reliable Depression Detection in LLMs with
Retrieval-Augmented Generation
Using Speech Timing Information (Zhang et al., 2025c)


DeepWell-Adol: A Scalable
Expert-Based Dialogue Corpus for
Adolescent Positive Mental Health
and Wellbeing Promotion (Qiu
et al., 2025b)


Hanging in the Balance: Pivotal
Moments in Crisis Counseling Conversations (Nguyen et al., 2025b)


Assess and Prompt: A Generative
RL Framework for Improving Engagement in Online Mental Health
Communities (Gaur et al., 2025)


AnnaAgent: Dynamic Evolution
Agent System with Multi-Session
Memory for Realistic Seeker Simulation (Wang et al., 2025a)


Tracking Life’s Ups and Downs:
Mining Life Events from Social
Media Posts for Mental Health
Analysis (Lv et al., 2025)



Psychologically
grounded
metrics



Yes No Yes No



AI/NLP met- No No N. A. Yes
rics



Psychologically
grounded
metrics


Psychologically
grounded
metrics



Yes No Yes Yes


Yes Yes Yes Yes



AI/NLP met- No No N. A. No
rics



Psychologically
grounded
metrics


Psychologically
grounded
metrics



Yes Yes Yes Yes


No No N. A. Yes



AI/NLP met- Yes No No Yes
rics



Psychologically
grounded
metrics


Psychologically
grounded
metrics



No No N. A. Yes


No No N. A. Yes



Table 12: List of surveyed papers _(part 10 of 14)_ .


30


Paper Evaluation Human Expert Evaluation
metrics evaluation evaluators guidelines
provided



Discuss
limitations
of evaluation



Can Large Language Models Identify Implicit Suicidal Ideation? An
Empirical Evaluation (Li et al.,
2025)


Eeyore: Realistic Depression Simulation via Expert-in-the-Loop Supervised and Preference Optimization (Liu et al., 2025)


Dialogue Systems for Emotional
Support via Value Reinforcement (Kim et al., 2025b)


MultiAgentESC: A LLM-based
Multi-Agent Collaboration Framework for Emotional Support Conversation (Xu et al., 2025)


MAGI: Multi-Agent Guided Interview for Psychiatric Assessment (Bi et al., 2025)


Systematic Evaluation of AutoEncoding and Large Language
Model Representations for Capturing Author States and Traits (Singh
et al., 2025)


The Pursuit of Empathy: Evaluating Small Language Models for
PTSD Dialogue Support (Bn et al.,
2025a)


Just a Scratch: Enhancing LLM Capabilities for Self-harm Detection
through Intent Differentiation and
Emoji Interpretation (Ghosh et al.,
2025)


Temporal reasoning for timeline
summarisation in social media (Song et al., 2025b)


MIRROR: Multimodal Cognitive
Reframing Therapy for Rolling
with Resistance (Kim et al., 2025d)



Psychologically
grounded
metrics


Psychologically
grounded
metrics


Psychologically
grounded
metrics


Psychologically
grounded
metrics


Psychologically
grounded
metrics



Psychologically
grounded
metrics


Psychologically
grounded
metrics



Yes Yes Yes No


Yes Yes Yes Yes


Yes Yes Yes Yes


Yes Yes Yes No


Yes Yes Yes Yes



AI/NLP met- No No N. A. No
rics



Psychologically
grounded
metrics



Yes No Yes Yes



AI/NLP met- No No N. A. Yes
rics



Yes Yes Yes No


Yes Yes Yes Yes



Table 13: List of surveyed papers _(part 11 of 14)_ .


31


Paper Evaluation Human Expert Evaluation
metrics evaluation evaluators guidelines
provided



Discuss
limitations
of evaluation



Are LLMs effective psychological assessors? Leveraging adaptive RAG for interpretable mental
health screening through psychometric practice (Ravenda et al., 2025)


ReDepress: A Cognitive Framework
for Detecting Depression Relapse
from Social Media (Agarwal et al.,
2025)


MentalGLM Series: Explainable
LLMs for Mental Health Analysis
on Chinese Social Media (Zhai et al.,
2025)


Towards AI-Assisted Psychotherapy:
Emotion-Guided Generative Interventions (Haydarov et al., 2025)


Mitigating Interviewer Bias in Multimodal Depression Detection: An
Approach with Adversarial Learning
and Contextual Positional Encoding (Zhang and Poellabauer, 2025)


Explainable Depression Detection in
Clinical Interviews with Personalized Retrieval-Augmented Generation (Zhang et al., 2025a)


From Heart to Words: Generating Empathetic Responses via Integrated Figurative Language and Semantic Context Signals (Lee et al.,
2025)


Reframe Your Life Story: Interactive Narrative Therapist and Innovative Moment Assessment with Large
Language Models (Feng et al., 2025)


From Conversation to Automation: Leveraging LLMs for
Problem-Solving Therapy Analysis (Aghakhani et al., 2025)


Feel the Difference? A Comparative Analysis of Emotional Arcs in
Real and LLM-Generated CBT Sessions (Wang et al., 2025b)



AI/NLP met- No No N. A. No
rics


AI/NLP met- No No N. A. No
rics



Psychologically
grounded
metrics


Psychologically
grounded
metrics



Yes Yes Yes Yes


Yes Yes Yes Yes



AI/NLP met- No No N. A. Yes
rics


AI/NLP met- No No N. A. No
rics



Psychologically
grounded
metrics


Psychologically
grounded
metrics



Yes No Yes Yes


Yes Yes Yes Yes



AI/NLP met- No No N. A. Yes
rics



Psychologically
grounded
metrics



No No N. A. Yes



Table 14: List of surveyed papers _(part 12 of 14)_ .


32


Paper Evaluation Human Expert Evaluation
metrics evaluation evaluators guidelines
provided



Discuss
limitations
of evaluation



CAMI: A Counselor Agent Supporting Motivational Interviewing
through State Inference and Topic
Exploration (Yang et al., 2025a)


Consistent Client Simulation for Motivational Interviewing-based Counseling (Yang et al., 2025b)


Does Rationale Quality Matter? Enhancing Mental Disorder Detection
via Selective Reasoning Distillation (Song et al., 2025a)


Crisp: Cognitive Restructuring of
Negative Thoughts through Multiturn Supportive Dialogues (Zhou
et al., 2025a)


ProMind-LLM: Proactive Mental
Health Care via Causal Reasoning
with Sensor Data (Zheng et al.,
2025)


EmoAgent: Assessing and Safeguarding Human-AI Interaction for
Mental Health Safety (Qiu et al.,
2025a)


MIND: Towards Immersive Psychological Healing with Multi-Agent Inner Dialogue (Chen et al., 2025b)


PsyDT: Using LLMs to Construct
the Digital Twin of Psychological
Counselor with Personalized Counseling Style for Psychological Counseling (Xie et al., 2025)


Third-Person Appraisal Agent: Simulating Human Emotional Reasoning in Text with Large Language
Models (Hong et al., 2025)


CATCH: A Novel Data Synthesis
Framework for High Therapy Fidelity and Memory-Driven Planning
Chain of Thought in AI Counseling (Chen et al., 2025a)



Psychologically
grounded
metrics


Psychologically
grounded
metrics


Psychologically
grounded
metrics


Psychologically
grounded
metrics


Psychologically
grounded
metrics


Psychologically
grounded
metrics


Psychologically
grounded
metrics


Psychologically
grounded
metrics


Psychologically
grounded
metrics


Psychologically
grounded
metrics



Yes Yes Yes Yes


Yes Yes Yes No


Yes Yes Yes Yes


Yes No Yes Yes


Yes Yes No Yes


No No N. A. Yes


Yes Yes Yes Yes


Yes Yes Yes Yes


Yes No Yes No


Yes Yes Yes No



Table 15: List of surveyed papers _(part 13 of 14)_ .


33


Paper Evaluation Human Expert Evaluation
metrics evaluation evaluators guidelines
provided



Discuss
limitations
of evaluation



Assessment and manipulation of latent constructs in pre-trained language models using psychometric
scales (Reuben et al., 2025)


How Real Are Synthetic Therapy Conversations? Evaluating Fidelity in Prolonged Exposure Dialogues (Bn et al., 2025b)


KoACD: The First Korean Adolescent Dataset for Cognitive Distortion
Analysis via Role-Switching MultiLLM Negotiation (Kim and Kim,
2025)


Exploring Large Language Models for Detecting Mental Disorders (Kuzmin et al., 2025)


M-Help: Using Social Media Data
to Detect Mental Health HelpSeeking Signals (Sathvik et al.,
2025)



Psychologically
grounded
metrics


Psychologically
grounded
metrics


Psychologically
grounded
metrics



No No N. A. No


Yes Yes Yes Yes


Yes Yes Yes Yes



AI/NLP met- No No N. A. Yes
rics


AI/NLP met- No No N. A. Yes
rics



Table 16: List of surveyed papers _(part 14 of 14)_ .


34


|Application Type|Tasks|
|---|---|
|**Assessment**|Anxiety detection; Depression detection; Classifcation of interpersonal<br>risk factors; Adverse drug reactions detection; Suicide risk detection;<br>Cognitive distortion detection; Detection of schizophrenia disorders; De-<br>tecting bipolar disorder; Mental disorder classifcation; Predicting degree<br>of anxiety; Detection of moments of change; Maladaptive schema de-<br>tection; Cross-cultural evaluation of depression detection; Psychological<br>profle generation; Measuring emotion granularity from text to detect<br>mental health conditions; Detecting mood changes in social media users<br>over time; Automatic detection of mental health conditions from social<br>media posts in German; Identifying depression symptoms from memes;<br>Multimodal LLM-based cognitive distortions detection; Personalized<br>mood change detection from users’ online text over time; Predicting<br>treatment outcome in internet-based therapy; Classifcation of Reddit<br>drug-use narratives into psychologically and socially meaningful cate-<br>gories; Chinese language model for psychological text analysis on social<br>media; Evaluating how well depression detection models generalize<br>across social media platforms; Identifying social biases toward disability<br>in NLP models; Analyze fairness and bias in depression detection models<br>on social media across gender and racial groups|
|**Intervention**|Emotional support conversation generation; Using entrainment in CBT;<br>Nutrition counseling; Synthetic dialogue generation for elders with cog-<br>nitive impairment; Mental illness conditioned motivational dialogue<br>generation; Generating motivational interviewing dialogues; Cognitive<br>reframing; AI-assisted multimodal therapy; Evaluating how well large<br>language models can assist cognitive behavioral therapy; Developing<br>dialogue system for mental health support; Structured, empathetic cog-<br>nitive reframing in psychotherapy; LLMs as emotional supporters for<br>queer youth; Generating synthetic therapy transcripts; Enhancing long-<br>form text generation for psychological question-answering; Evaluating<br>whether LLMs can provide ethical, empathetic, and theory-grounded<br>responses for mental health support|
|**Information**<br>**syn-**<br>**thesis**|Analysis of quality of therapy conversations; Behavior code predic-<br>tion; Understanding the therapeutic relationship between counselors and<br>clients; Evaluating LLM alignment with counseling competencies; En-<br>hancing interpersonal skills; Analysis of client reactions in online mental<br>health counseling; Understanding empathy in mental health support text;<br>Clinically meaningful timeline summarisation in social media; Politeness<br>and intensity tagging in conversations; Teaching AI to automatically<br>label behaviors in therapy conversations using small amounts of data;<br>Scoring counselor responses for refective listening in motivational inter-<br>viewing; Creating realistic AI-simulated patients for counselor training;<br>Counseling summarization; Patient simulation for training therapists|



Table 17: Overview of the diverse tasks addressed in the surveyed papers.


35


