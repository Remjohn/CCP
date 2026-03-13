# **Computational Appraisal Profiling: Reverse-Engineering Scherer’s Component Process Model from Audience Behavioral Signatures**

The conceptualization of audience engagement has historically suffered from a reliance on aggregate sentiment analysis, a methodology that captures the valence of emotional outcomes but fails to elucidate the cognitive architecture of the emotion-generative process. While the coach-side of human-computer interaction and counseling has successfully integrated Klaus Scherer’s Component Process Model (CPM) to analyze five distinct appraisal variables, the audience-side lacks a comparable instrument for real-time cognitive profiling.1 This gap necessitates a paradigm shift toward reverse-engineering Stimulus Evaluation Checks (SECs)—specifically novelty, intrinsic pleasantness, goal relevance, coping potential, and norm compatibility—from observable digital footprints.3 Unlike self-report measures, which are susceptible to social desirability bias and post-hoc rationalization, behavioral signals such as purchase velocity, content engagement patterns (save versus share), and the linguistic morphology of complaint structures offer a more granular, process-oriented view of how an audience evaluates stimuli.2 By applying transformer-based architectures like RoBERTa at the clause level, as pioneered in the work of Pérez-Rosas et al., it becomes possible to extract per-individual appraisal sequences that map the temporal unfolding of an audience’s cognitive state.6

## **Theoretical Framework of the Component Process Model**

The Component Process Model (CPM) differentiates itself from basic emotion theories by defining emotions as dynamic, multi-componential episodes rather than static categorical states.1 At the core of this model is the assumption that the cognitive evaluation of a stimulus—the appraisal—is the primary driver that causes changes in four other subsystems: physiological arousal, motivational action tendencies, motor expression, and subjective feeling.3

### **The Sequence of Stimulus Evaluation Checks**

A central tenet of Scherer’s work is that appraisals are processed in a specific, recursive sequence. This sequence allows the organism to respond with increasing specificity to environmental changes.4 The CPM proposes four major stages of evaluation, each containing specific Stimulus Evaluation Checks (SECs) that fire in a precise order.

| Appraisal Stage | Information Assessed | SECs and Behavioral Correlates |
| :---- | :---- | :---- |
| Relevance | Personal significance and urgency. | Novelty, Intrinsic Pleasantness, Goal Relevance. |
| Implications | Consequences and well-being impact. | Causal Attribution, Outcome Probability, Goal Conduciveness. |
| Coping Potential | Ability to manage or respond. | Controllability, Power, Adjustment. |
| Normative Significance | Alignment with personal and social norms. | Internal Standards, External Norms. |

4

The sequential nature of these checks is not merely a theoretical requirement but a biological reality observed in temporal delays between facial muscle activations. For instance, muscle activity marking the relevance appraisal occurs significantly earlier than markers of goal conduciveness or power appraisals.9 This temporal signature provides a critical entry point for reverse-engineering; if behavioral signals exhibit a specific sequence of "firing," the underlying cognitive appraisal path can be reconstructed.

### **Synchronization as a Functional Emergence**

Emotions are viewed as "relevance detectors" that decouple behavioral reactions from stimulus events, replacing rigid reflex patterns with flexible, synchronized responses.3 This synchronization involves a "critical threshold" where changes across subsystems—such as a rise in heart rate alongside an aggressive motor expression—signal the emergence of a conscious emotional state.3 In the context of audience profiling, this suggests that high-intensity emotional reactions (e.g., a viral outrage cycle or a surge in brand loyalty) are the result of highly synchronized appraisal outcomes across a community.3

## **Computational Architectures for Appraisal Detection**

The transition from theory to application requires a computational mechanism capable of detecting these fine-grained appraisals within unstructured data.2 The shift from word-level sentiment analysis to clause-level appraisal detection is facilitated by contextualized language models that can resolve the "affect flow" within a conversation.8

### **The Superiority of RoBERTa in Appraisal Extraction**

Recent research indicates that transformer-based models, specifically RoBERTa (Robustly Optimized BERT Approach), significantly outperform traditional feature-based methods and earlier models like BERT in detecting deceptive intent and emotional nuances.7 RoBERTa’s ability to handle longer sequences and its more robust training on diverse linguistic datasets allow it to identify the subtle "fingerprints" of cognitive evaluation.7

| Model Approach | Task | F1 Score / Accuracy |
| :---- | :---- | :---- |
| BERT (Supervised) | Deception Detection (FakeNewsAMT) | 0.75 |
| RoBERTa (Supervised) | Deception Detection (FakeNewsAMT) | 0.97 |
| RoBERTa \+ CE Features | Misinformation Identification | 0.975 |
| AppraisePLM (RoBERTa-based) | 21 Appraisal Dimensions | State-of-the-Art |

7

Pérez-Rosas et al. demonstrated that by fine-tuning these models on appraisal-specific datasets—such as the crowd-ENVENT corpus—it is possible to predict dimensions like pleasantness, self-control, and alignment with social norms with high precision.8 These classifiers go beyond "positive/negative" labels, extracting the underlying "why" of the emotion.2

### **Clause-Level Analysis and Morphological Hardness**

A critical insight from computational linguistics is that appraisal variables are often embedded at the clause level rather than being uniformly distributed across a sentence.12 For example, a single customer review might say: "The product is innovative (Novelty+), but I can’t figure out how to use it (Coping-)." Word-level models often average these out, resulting in a neutral sentiment score that obscures the critical appraisal conflict.2 Redefining the task to the clause level provides a "neat interface" with contextualized language models, allowing for the assessment of morphological knowledge encoded within the model.12 This granularity is essential for reverse-engineering the SEC sequence, as it allows the system to track how an appraisal shifts from one clause to the next.8

## **Reverse-Engineering the SEC Sequence from Behavioral Signals**

Audience behavior is a form of "motor expression" that reflects the outcome of internal appraisals.3 By observing the sequence and nature of these behaviors, we can infer the state of the individual's Stimulus Evaluation Checks.2

### **Novelty and Intrinsic Pleasantness: The Relevance Threshold**

The earliest checks in the CPM sequence determine if a stimulus is worth the allocation of cognitive resources.16 In a digital environment, these checks are reflected in "bottom-up" attention capture.

* **Novelty Behavioral Signals**: High novelty appraisals are signaled by rapid spikes in community participation rhythms, high click-through rates on unexpected content, and exploratory search behavior.18 When novelty is low, behaviors become ritualized and rhythmic, reflecting "highly overlearned" states.16  
* **Intrinsic Pleasantness Behavioral Signals**: This is evaluated through immediate, aesthetic-driven engagement, such as the "like" function on visual platforms or low bounce rates on aesthetically pleasing interfaces.5 In linguistic data, this is often expressed through sensory adjectives and immediate valenced reactions.8

### **Goal Relevance and Goal Conduciveness: The Utility Mapping**

Once relevance is established, the audience evaluates the stimulus in relation to their current goals.4 This is the stage where "saves" and "shares" begin to diverge functionally.

* **The "Save" Signature**: A "save" or "bookmark" is a strong indicator of high Goal Relevance combined with a promotion orientation.18 It suggests that the user perceives the content as a necessary resource for future goal pursuit.22 This behavior is often accompanied by "System-2" processing, where the user allocates sustained attention to the stimulus.19  
* **Goal Conduciveness in Purchase Behavior**: Purchase behavior serves as the ultimate behavioral validation of high Goal Conduciveness.2 If a product is appraised as facilitative of a goal, the individual moves from "contemplation" to "transaction".2 Conversely, an "abandoned cart" may signal a sudden reappraisal of goal conduciveness or an assessment of high "outcome probability" for a negative consequence (e.g., financial strain).2

### **Coping Potential: From Power to Adjustment**

The assessment of coping potential—comprising controllability and power—determines whether the audience feels they can influence the situation or if they must adapt to it.11

| Coping Dimension | Behavioral Signature | Linguistic Profile |
| :---- | :---- | :---- |
| High Power / Control | Public tagging of brands, explicit demands for resolution, threats of exit. | Active voice, other-directed agency, "accountability" markers. |
| Low Power / Control | Vague venting in peer-to-peer forums, "disappointment" language, high churn rate. | Passive voice, "sadness" markers, focus on external barriers. |
| High Adjustment | Pivot to "workarounds," seeking community help rather than brand help. | Technical, low-emotion descriptions, "how-to" focus. |

2

Complaint language structure is particularly revealing of this dimension. Users who feel they have high power will use "other-accountability" language, blaming the brand for goal obstruction.2 Those with low coping potential express "disappointment" or "sadness," reflecting a cognitive state of resignation.2 Reverse-engineering this allows for targeted interventions: users with low coping potential need "support and empowerment," while those with high power need "resolution and compensation".24

### **Norm Compatibility: The Social and Ethical Standard**

The final check in the SEC sequence evaluates whether the event or the individual's reaction aligns with internal and social standards.4

* **Sharing Behavior**: Unlike a "save," a "share" is often a signal of Norm Compatibility evaluation.4 By sharing, the user signals alignment with a social group or reinforces a specific community norm.8  
* **Community Policing**: Behaviors such as "reporting" content or engaging in "call-out" culture are manifestations of a negative Norm Compatibility appraisal.8 In these cases, the "other-accountability" is framed not as a failure of utility (goal conduciveness) but as a failure of morality or ethics.4

## **The Mathematical Modeling of Appraisal Sequences**

To move from qualitative observation to quantitative profiling, the CPM’s sequential nature must be modeled mathematically. The probability of an emotional state ![][image1] at time ![][image2] can be expressed as a function of the conditional chain of SEC outcomes:

![][image3]  
This model captures the "preliminary closure" mentioned in Scherer’s work, where a stable appraisal pattern must be reached before the emotion becomes consciously represented.16 In an audience-side instrument, this means tracking the *accumulation* of signals. A single "like" is insufficient to profile a user, but a sequence of "Like (Pleasantness+) ![][image4] Save (Goal Relevance+) ![][image4] Repeat View (Goal Conduciveness+) ![][image4] Share (Norm Compatibility+)" provides a high-confidence map of a "Positive Transformation" appraisal path.2

### **Interaction Effects in Appraisal Clusters**

The outcomes of specific checks often interact to amplify or dampen the resulting emotional intensity.23 For instance, Scherer’s experiments showed that the effect of "goal conduciveness" on facial expressions was amplified when "power" was also appraised as high.9

| Appraisal Interaction | Emotional Output | Typical Audience Behavior |
| :---- | :---- | :---- |
| Goal Inconducive \+ High Power | Anger / Rage | Virulent social media attacks, direct confrontation. |
| Goal Inconducive \+ Low Power | Fear / Sadness | Silent churn, expressing "hopelessness" in reviews. |
| Goal Conducive \+ High Power | Joy / Pride | Public brand advocacy, "success story" forum posts. |
| Goal Conducive \+ Low Power | Relief | High retention, but low public engagement. |

2

By using multi-task learning frameworks, computational models can jointly predict these dimensions, revealing the underlying "why" behind behavior.2 Modeling these interactions allows for a more nuanced understanding of why people have different behavioral intentions after interacting with the same product.2

## **Deep-Reaching Second and Third-Order Insights**

The data suggests that the transition from sentiment to appraisal has profound implications for how we understand human-computer interaction and community health.

### **The Decoupling of Behavior and Reflex**

Scherer’s assertion that emotions "decouple" behavior from stimulus is a critical second-order insight.3 In a digital context, this means that as an audience becomes more "emotional," their behavior becomes less predictable by simple stimulus-response (S-R) models.3 Traditional marketing, which relies on "nudges" (S-R), fails when the audience enters a high-intensity emotional episode.3 Appraisal profiling allows for the detection of this "decoupling" threshold, signaling when an audience has shifted from passive consumption to active, appraisal-driven evaluation.3

### **Appraisal flow as a Predictor of Community Longevity**

A community’s participation rhythms are not just engagement metrics but indicators of the aggregate "affect flow".8 If a community’s discourse shifts toward appraisals of "low coping potential" and "low goal conduciveness," the long-term trend is toward fragmentation and abandonment, even if sentiment remains "neutral" in the short term.3 The "Frustrated Power" cluster (high power \+ goal inconducive) is particularly dangerous for community stability, as it drives the most toxic forms of engagement.2

### **The Morphological Interface of Cognitive States**

The finding that clause-level tasks are "substantially harder" than word-level tasks for language models suggests that the "grammar of emotion" is complex and structural.12 Third-order implications suggest that we should stop looking for "emotion words" and start looking for "appraisal structures".8 For example, the presence of specific grammatical gender/number causal effects or the use of certain reinflection patterns may serve as hidden markers of "normative evaluation".12

## **Implementing the Audience-Side Appraisal Instrument**

To close the gap identified in the research request, the proposed instrument must integrate multi-modal data through a "Reverse Engineering of Deceptions" (RED) framework, treating digital footprints as fingerprints of internal knowledge and objectives.29

### **Pipeline for Computational Appraisal Extraction**

The system architecture consists of four primary processing spaces:

1. **Behavioral Sensing Space**: Extracts raw signals (clickstream, transaction logs, interaction rhythms).18  
2. **Linguistic Appraisal Space**: Applies RoBERTa-based clause-level classifiers to audience text to identify the 20+ dimensions of the PEACE-Reviews or crowd-ENVENT datasets.2  
3. **Sequential Synchronization Space**: Maps behavioral and linguistic data onto a temporal timeline to identify the "threshold of synchronization".3  
4. **Actionable Profiling Space**: Clusters users based on their appraisal trajectories (e.g., "The Disappointed Advocate" vs. "The Aesthetic Novelty-Seeker") to provide targeted coaching or intervention.2

### **Performance and Validation Metrics**

The efficacy of such an instrument is measured by its "individualized prediction" accuracy—the ability to predict a specific user's next action (e.g., share, churn, buy) based on their appraisal sequence.2 Standardized metrics like the F1-macro score for in-domain and out-of-distribution classification provide a benchmark for model reliability.7

| Task Type | Dataset | Best Reported Performance |
| :---- | :---- | :---- |
| Emotion Classification | News Titles | 90% (RoBERTa) |
| Appraisal Detection | crowd-ENVENT | AppraisePLM (SOTA) |
| Fake News Prediction | GossipCop | 0.80 (RoBERTa) |
| Fake News Prediction | PolitiFact | 0.93 (RoBERTa) |

7

These high-accuracy results in adjacent fields (like deception detection) demonstrate that the computational tools are ready for application to the more complex task of audience appraisal profiling.7

## **Conclusion: Toward a Nuanced Understanding of the Digital Audience**

The reverse-engineering of Scherer’s Component Process Model from audience behavioral signals represents a fundamental advancement in our ability to interpret human cognitive states.1 By moving beyond the "outcome" of sentiment and toward the "process" of appraisal, we gain the ability to see the audience as a collection of evaluating organisms rather than a simple data aggregate.3 The integration of RoBERTa-based clause-level analysis with non-self-report behavioral data allows for the first time the creation of an audience-side appraisal instrument that matches the sophistication of coach-side tools.2

This instrument provides the "why" behind the engagement, revealing whether a user is "saving" for utility or "sharing" for social alignment, and whether their "complaint" is a plea for power or a marker of resignation.2 Ultimately, the ability to track "affect flow" and "appraisal sequences" across digital footprints allows for the design of more empathetic, responsive, and effective human-computer systems that respect the complex cognitive architecture of the modern audience.8 The "critical threshold of synchronization" is no longer a theoretical abstraction but a measurable objective for community managers, product designers, and computational linguists seeking to navigate the intricate landscape of human emotion in the digital age.2

#### **Works cited**

1. The Cognitive Emotion Process: Examining Appraisal Theory using Theoretical Modeling and Machine Learning, accessed March 6, 2026, [https://edoc.ub.uni-muenchen.de/26611/1/Israel\_Laura.pdf](https://edoc.ub.uni-muenchen.de/26611/1/Israel_Laura.pdf)  
2. Beyond Text: Leveraging Multi-Task Learning and Cognitive ..., accessed March 6, 2026, [https://arxiv.org/pdf/2407.08182](https://arxiv.org/pdf/2407.08182)  
3. The Dynamics of Emotions: Klaus Scherer's Component Process Model, accessed March 6, 2026, [https://psychologyfanatic.com/klaus-scherers-component-process-model/](https://psychologyfanatic.com/klaus-scherers-component-process-model/)  
4. Component Process Model (CPM; Scherer, 2001\) – Psychology of Human Emotion, accessed March 6, 2026, [https://psu.pb.unizin.org/psych425/chapter/component-process-model-cpm/](https://psu.pb.unizin.org/psych425/chapter/component-process-model-cpm/)  
5. Scherer, K. R., & Moors, A. (in press). The emotion process: Event appraisal and component differentia \- KU Leuven, accessed March 6, 2026, [https://ppw.kuleuven.be/okp/\_pdf/SchererInPressTEPEA.pdf](https://ppw.kuleuven.be/okp/_pdf/SchererInPressTEPEA.pdf)  
6. Modeling Empathetic Alignment in Conversation \- arXiv.org, accessed March 6, 2026, [https://arxiv.org/html/2405.00948v1](https://arxiv.org/html/2405.00948v1)  
7. Weakly Supervised Veracity Classification with LLM-Predicted Credibility Signals \- arXiv, accessed March 6, 2026, [https://arxiv.org/html/2309.07601v3](https://arxiv.org/html/2309.07601v3)  
8. An Appraisal Theoretic Approach to Modelling ... \- ACL Anthology, accessed March 6, 2026, [https://aclanthology.org/2025.conll-1.16.pdf](https://aclanthology.org/2025.conll-1.16.pdf)  
9. Appraisals Generate Specific Configurations of Facial Muscle Movements in a Gambling Task: Evidence for the Component Process Model of Emotion \- PMC, accessed March 6, 2026, [https://pmc.ncbi.nlm.nih.gov/articles/PMC4546426/](https://pmc.ncbi.nlm.nih.gov/articles/PMC4546426/)  
10. Emotions are emergent processes: they require a dynamic computational architecture \- PMC, accessed March 6, 2026, [https://pmc.ncbi.nlm.nih.gov/articles/PMC2781886/](https://pmc.ncbi.nlm.nih.gov/articles/PMC2781886/)  
11. Archive ouverte UNIGE First evidence for differential and sequential efferent effects of stimulus relevance and goal conducivene, accessed March 6, 2026, [https://access.archive-ouverte.unige.ch/access/metadata/2b223622-60a2-4cd2-aaa1-8bbc205b3c07/download](https://access.archive-ouverte.unige.ch/access/metadata/2b223622-60a2-4cd2-aaa1-8bbc205b3c07/download)  
12. Submission Information \- emnlp 2022, accessed March 6, 2026, [https://2022.emnlp.org/downloads/Accepted-Papers-20221122.xls](https://2022.emnlp.org/downloads/Accepted-Papers-20221122.xls)  
13. Health Misinformation Detection: Approaches, Challenges and Opportunities \- PMC, accessed March 6, 2026, [https://pmc.ncbi.nlm.nih.gov/articles/PMC12589804/](https://pmc.ncbi.nlm.nih.gov/articles/PMC12589804/)  
14. The Routledge Handbook of Discourse and Disinformation 9781032124254, 9781032124285, 9781003224495 \- DOKUMEN.PUB, accessed March 6, 2026, [https://dokumen.pub/the-routledge-handbook-of-discourse-and-disinformation-9781032124254-9781032124285-9781003224495.html](https://dokumen.pub/the-routledge-handbook-of-discourse-and-disinformation-9781032124254-9781032124285-9781003224495.html)  
15. A More Fine-Grained Aspect–Sentiment–Opinion Triplet Extraction Task \- MDPI, accessed March 6, 2026, [https://www.mdpi.com/2227-7390/11/14/3165](https://www.mdpi.com/2227-7390/11/14/3165)  
16. Affect and Learning \- Interactive Intelligence, accessed March 6, 2026, [https://ii.tudelft.nl/\~joostb/files/PhD%20Thesis%20Complete%20Broekens%20complete%2020-nov-2007.pdf](https://ii.tudelft.nl/~joostb/files/PhD%20Thesis%20Complete%20Broekens%20complete%2020-nov-2007.pdf)  
17. The Nature and Dynamics of Relevance and Valence Appraisals: Theoretical Advances and Recent Evidence | Request PDF \- ResearchGate, accessed March 6, 2026, [https://www.researchgate.net/publication/270676937\_The\_Nature\_and\_Dynamics\_of\_Relevance\_and\_Valence\_Appraisals\_Theoretical\_Advances\_and\_Recent\_Evidence](https://www.researchgate.net/publication/270676937_The_Nature_and_Dynamics_of_Relevance_and_Valence_Appraisals_Theoretical_Advances_and_Recent_Evidence)  
18. Episodic Memory for External Information \- Computer Science, accessed March 6, 2026, [https://csd.cs.cmu.edu/sites/default/files/phd-thesis/CMU-CS-96-167.pdf](https://csd.cs.cmu.edu/sites/default/files/phd-thesis/CMU-CS-96-167.pdf)  
19. Decision Making Under Scarcity: An Inquiry into The Effects of Cognitive Load \- UEA Digital Repository, accessed March 6, 2026, [https://ueaeprints.uea.ac.uk/93000/1/Thesis%20final\_Pande.pdf](https://ueaeprints.uea.ac.uk/93000/1/Thesis%20final_Pande.pdf)  
20. A Social Media Misinformation Detection Model Integrating Semantic and Twitter Features, accessed March 6, 2026, [https://ceur-ws.org/Vol-4173/T1-4.pdf](https://ceur-ws.org/Vol-4173/T1-4.pdf)  
21. FOREAL: RoBERTa Model for Fake News Detection based on Emotions \- SciTePress, accessed March 6, 2026, [https://www.scitepress.org/PublishedPapers/2022/108739/108739.pdf](https://www.scitepress.org/PublishedPapers/2022/108739/108739.pdf)  
22. Essays on emotional influences in consumer food choice \- HELDA \- University of Helsinki, accessed March 6, 2026, [https://helda.helsinki.fi/bitstreams/4d670d5a-cfbd-49ab-8bba-3975d867be27/download](https://helda.helsinki.fi/bitstreams/4d670d5a-cfbd-49ab-8bba-3975d867be27/download)  
23. Appraisals Generate Specific Configurations of Facial Muscle Movements in a Gambling Task: Evidence for the Component Process Model of Emotion \- PubMed, accessed March 6, 2026, [https://pubmed.ncbi.nlm.nih.gov/26295338/](https://pubmed.ncbi.nlm.nih.gov/26295338/)  
24. Emotions in Educators Implementing a Social-Emotional Development Framework \- Spark Bethel, accessed March 6, 2026, [https://spark.bethel.edu/cgi/viewcontent.cgi?article=1806\&context=etd](https://spark.bethel.edu/cgi/viewcontent.cgi?article=1806&context=etd)  
25. arXiv:2311.08299v2 \[cs.CL\] 8 Mar 2024, accessed March 6, 2026, [https://arxiv.org/pdf/2311.08299](https://arxiv.org/pdf/2311.08299)  
26. (PDF) Anno-MI: A Dataset of Expert-Annotated Counselling Dialogues \- ResearchGate, accessed March 6, 2026, [https://www.researchgate.net/publication/360792275\_Anno-MI\_A\_Dataset\_of\_Expert-Annotated\_Counselling\_Dialogues](https://www.researchgate.net/publication/360792275_Anno-MI_A_Dataset_of_Expert-Annotated_Counselling_Dialogues)  
27. VERVE: Template-based ReflectiVE Rewriting for MotiVational IntErviewing \- arXiv, accessed March 6, 2026, [https://arxiv.org/html/2311.08299v2](https://arxiv.org/html/2311.08299v2)  
28. Detecting harassment and defamation in cyberbullying with emotion-adaptive training, accessed March 6, 2026, [https://arxiv.org/html/2501.16925v1](https://arxiv.org/html/2501.16925v1)  
29. Reverse Engineering of Deceptions \- on Machine- and Human-Centric Attacks \- Computer Vision Lab, accessed March 6, 2026, [http://cvlab.cse.msu.edu/pdfs/RED\_survey\_FnT.pdf](http://cvlab.cse.msu.edu/pdfs/RED_survey_FnT.pdf)  
30. PROBAST: A Tool to Assess the Risk of Bias and Applicability of Prediction Model Studies | Annals of Internal Medicine \- ACP Journals, accessed March 6, 2026, [https://www.acpjournals.org/doi/10.7326/M18-1376](https://www.acpjournals.org/doi/10.7326/M18-1376)  
31. Fake news detection: deep semantic representation with enhanced feature engineering, accessed March 6, 2026, [https://pmc.ncbi.nlm.nih.gov/articles/PMC9998010/](https://pmc.ncbi.nlm.nih.gov/articles/PMC9998010/)  
32. Artificial Intelligence \- Professional Learning (CA Dept of Education), accessed March 6, 2026, [https://www.cde.ca.gov/ci/pl/aiincalifornia.asp](https://www.cde.ca.gov/ci/pl/aiincalifornia.asp)

[image1]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA8AAAAZCAYAAADuWXTMAAABBklEQVR4Xu3Rv0tCURQH8CM6FOpQQyEFirUIQkN7k5Ngg7hJ4OYuCA4OgYiLBDY0uEhDW/+AYzT6BzgbTkqLm0PZ97z7fbwfWoJOoV/48Lj33HPe4z6R3c4h1Ki7RgcSVhcThBNqwByyEKM4VWEK16bNSYBeYABH3rKVA3gSM9ATPay0sSdmkOYMjikMbZ7z5IpmUOaeDqhDkkKQ4dOTrZqL9A33UIAW9CFCv+aRRlAS0/zMvT8ThXd6FeezcpC3DyEXcONaW0nBJ1Vc+5dibtn+jVpLu+pWbuGL9EL80SHqQVZcVhPGdO6r6fqN9CVL2aj5TkyD/clK1x80gQUM6dS07fOP8gPm0DmhdJXAdQAAAABJRU5ErkJggg==>

[image2]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAcAAAAYCAYAAAA20uedAAAAmElEQVR4XmNgGMSAH4pLgFgSTY7BBYofArESmhxDORQfAGIemKAuEIcA8SEo3gbEAUAsApI0B+JUIH4PxZ1A7A/EQiBJEDAF4rtQrAkThIF0ID4NxYJocrglGYF4PhDPgWIUAFIJ0hENxSAA8q8siAHyygMGiKNAWAaIW4CYFSQJ8vBWIG6H4sVALA+SgAFmIBaGYhB7CAIAK5EZTM6QQ70AAAAASUVORK5CYII=>

[image3]: <data:image/png;base64,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>

[image4]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABMAAAAXCAYAAADpwXTaAAAAaElEQVR4XmNgGAWjgGqAFYjZoJhioAPEJVBMMQC5rAOKZdHkyAJqUNwNxPxociQDnIaBnO0MxCFk4FogPg3ETkDMDMTUNYwcoA/FfUDMjSZHEuAE4glQTHFsGgNxORRTDKiaA0YBFQEA6csTxY5I6CAAAAAASUVORK5CYII=>