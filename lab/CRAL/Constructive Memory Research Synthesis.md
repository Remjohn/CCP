# **The Constructive Architecture of Memory: Theoretical Frameworks of Schema-Based Reconstruction and Encoding Specificity in Human and Artificial Intelligence**

The conceptualization of memory as a static repository of historical data has been fundamentally dismantled by a century of psychological and neuroscientific inquiry. Instead, memory is recognized as a dynamic, constructive process—a performance rather than a recording—where the act of retrieval is inextricably linked to the schemas, prior knowledge, and contextual cues available at the moment of recall.1 This transition from a "trace-based" to a "construction-based" paradigm was inaugurated by Frederic Bartlett, refined by Endel Tulving’s operationalization of retrieval contexts, and extended by Daniel Schacter into the realms of adaptive failure and future-oriented simulation.3 When these cognitive frameworks are applied to the evaluation of Large Language Models (LLMs), they reveal profound structural parallels, particularly regarding the "statistical centroid" problem. The tendency of generative systems to regress toward the mean of their training data is not merely an engineering shortcoming but a predictable manifestation of schema activation failure—a computational mirror of the human tendency to rationalize unfamiliar data into culturally available frameworks.6

## **The Bartlettian Foundation: Memory as Imaginative Reconstruction**

Frederic Bartlett’s 1932 volume, *Remembering: A Study in Experimental and Social Psychology*, stands as a radical departure from the associationist tradition represented by Hermann Ebbinghaus. While Ebbinghaus sought to study "pure" memory by utilizing nonsense syllables to eliminate the influence of meaning, Bartlett argued that memory could only be understood in its naturalistic, meaning-making context.9 He posited that remembering is an "active organization of past reactions" that operates as a unitary mass rather than a collection of individual elements.12 This perspective situated the mind not as a warehouse but as a functional system engaged in constant environmental adaptation.1

### **The Micro-Mechanisms of Schematic Distortion**

Bartlett’s investigations into the "War of the Ghosts," a Native American folk tale, provided the empirical substrate for his theory of reconstruction. Because the story featured unfamiliar cultural norms and supernatural logic, it forced British participants to rely on their own existing cognitive frameworks to bridge gaps in comprehension and recall.9 Through the methods of repeated and serial reproduction, Bartlett identified a set of systematic transformations that information undergoes during its assimilation into a dominant schema.10

| Distortion Type | Cognitive Function | Observed Effect in "War of the Ghosts" |
| :---- | :---- | :---- |
| Rationalization | Meaning-making and gap-filling | Supernatural elements were reinterpreted as physical events; the "black thing" leaving the mouth was treated as a symptom of disease.1 |
| Leveling | Reduction of cognitive load | Details deemed irrelevant to the Western "battle" schema, such as specific place names (Egulac) or quantities, were omitted.12 |
| Sharpening | Focal point reinforcement | Certain elements, like the fight or the death, were emphasized to make the narrative more punchy and conventional.18 |
| Cultural Assimilation | Framework alignment | Unfamiliar cultural items were replaced with local equivalents; "canoes" became "boats," and "hunting seals" became "fishing".16 |
| Elaboration | Schema-consistent fabrication | Participants added emotions or details (e.g., specific weapons) that were not in the text but fit the "war party" schema.12 |

The analysis suggests that these distortions are not random but move in a consistent direction toward a "final form" that matches the individual’s cultural expectations.10 This process, which Bartlett termed "turning round upon one's own schemata," illustrates the strategic, voluntary nature of remembering when an automatic response is insufficient for the environmental demand.14

### **Social Determinants and the Collective Scaffolding of Recall**

Bartlett’s later theoretical treatment in Part II of *Remembering* addressed the social origin of schemas. He argued that social organization provides a persistent framework into which all detailed recall must fit.22 The mind is "taken out of the head" and situated in the transactions between the individual and their social environment.14 While critical of the Jungian notion of a "collective unconscious" stored biologically in the brain, Bartlett maintained that customs, traditions, and technical secrets are literally properties of groups that act as determinants of individual recall.22

This social scaffolding ensures that reconstruction is not entirely idiosyncratic. Instead, it converges on the "statistical centroid" of the social group’s shared knowledge base.22 In the context of computational generative systems, this corresponds to the "Consensus Hull"—the boundary of statistically probable token sequences derived from a massive mixture of training samples.7 Without a specific "finding-level" trigger to pull the system away from this hull, the output regresses toward a culturally and statistically normalized average.7

## **Operational Precision: Tulving’s Encoding Specificity Framework**

While Bartlett established the "why" of reconstruction, Endel Tulving’s 1983 work, *Elements of Episodic Memory*, provided the "how" through the encoding specificity principle.5 Tulving argued that successful retrieval is not a matter of simply looking up a stored trace; it is a synergistic interaction between a stored episodic trace and a cognitively present retrieval cue.5

### **Synergistic Ecphory and the GAPS Framework**

Tulving introduced the General Abstract Processing System (GAPS) as a framework for the study of episodic remembering. The process begins with the witnessing of an event and ends with a recollective experience, mediated by three conceptually similar processes: encoding, recoding, and ecphory.5

| Component | Definition | Role in Reconstruction |
| :---- | :---- | :---- |
| Stored Trace | The episodic information retained after encoding | Serves as the raw, often fragmented, substrate for reconstruction.5 |
| Retrieval Cue | Information available at the time of recall | Acts as the trigger that activates specific sectors of the stored trace.5 |
| Ecphory | The interaction between trace and cue | The actual constructive act that yields "ecphoric information".5 |
| Recollective Experience | The conscious awareness of the past event | The final output of the construction, which may be more or less accurate depending on cue-fit.5 |

The encoding specificity principle states that "cues complement traces rather than merely selecting them".5 This synergy explains why a target word matched with an unrelated word pair at encoding is recalled better when prompted with that specific pair than when prompted with a semantically related but novel word.25 Retrieval failure, therefore, is frequently an "accessibility failure"—the information is present in the system but the cues are insufficient to trigger the correct reconstruction template.25

### **Contextual Congruency as a Filter for Noise**

The efficiency of reconstruction is governed by the "fit" between mental representations at encoding and retrieval.23 Factors such as physical environment, mood states, and even pharmacological states (intoxication) act as contextual retrieval cues.23

![][image1]  
This relationship highlights the "outshining hypothesis": context is a vital cue only when better, more specific cues are unavailable.25 In computational applications, this confirms that finding-level specificity (names, verifiable facts, precise mechanisms) provides a stronger reconstruction template than topical research. Specificity acts as a high-fidelity retrieval cue that "outshines" the generic noise of the statistical centroid.23

## **The Seven Sins and the Adaptive Purpose of Distortion**

Daniel Schacter’s 1996 work, *Searching for Memory*, redefined memory errors as "by-products of otherwise adaptive features" of the mind.4 Schacter categorized memory failures into seven "sins," divided between omission (forgetting) and commission (distortion).4

### **Detailed Analysis of Sins of Commission**

The sins of commission—misattribution, suggestibility, bias, and persistence—are particularly relevant for understanding why generative systems produce distorted outputs.4

* **Misattribution:** Correct recollection of information paired with incorrect recollection of the source. This often results from a failure to adequately bind features during encoding.3 In AI, this mirrors "hallucination" where a model correctly predicts a sequence of facts but attributes them to the wrong historical figure or event.29  
* **Suggestibility:** The tendency to incorporate external information into one's own recollections.2 This is the human equivalent of prompt-based steering, where leading questions can permanently alter the reconstruction of an event.2  
* **Bias:** The filtering of past events through current knowledge, beliefs, and feelings.2 This retrospective distortion ensures that a person's personal history remains consistent with their present self-image, similar to how an LLM filters historical data through its current "safety" or "alignment" weights.6

| Sin of Memory | Cognitive Mechanism | Parallel in Generative AI |
| :---- | :---- | :---- |
| Transience | Accessibility decay over time | Weight decay or lack of context window space.32 |
| Absent-mindedness | Attention-memory interface breakdown | Attention mechanism failure or shallow processing of prompt.32 |
| Blocking | Interference from related memories | Semantic overlap leading to "logic drift" or incorrect token selection.7 |
| Misattribution | Feature binding failure | Source confusion or hallucinated attribution.3 |
| Suggestibility | External information integration | Vulnerability to "prompt injection" or leading constraints.2 |
| Bias | Hindsight/Egocentric filtering | Training data bias or reinforcement learning from human feedback (RLHF).2 |
| Persistence | Unwanted recollection arousal | High-probability centroids that "drown out" nuanced data.33 |

These "sins" are the direct consequence of a system that extracts the "gist" rather than the verbatim record.11 This extraction is highly adaptive for humans, as it allows us to generalize knowledge across situations, but it presents a "statistical centroid problem" for research-intensive tasks where idiosyncratic precision is required.7

## **Constructive Episodic Simulation: Remembering the Past to Imagine the Future**

One of the most significant extensions of constructive memory theory is the "constructive episodic simulation hypothesis," proposed by Schacter and Donna Rose Addis in 2007\.39 This hypothesis posits that memory and imagination rely on a common neural network designed to retrieve and flexibly recombine past experiences into simulations of possible future events.39

### **The Core Neural Network of Reconstruction**

Neuroimaging research has confirmed that both remembering the past and imagining the future activate a common core network, primarily overlapping with the Default Mode Network (DMN).42

| Neural Structure | Primary Reconstruction Function | Implication for AI Architecture |
| :---- | :---- | :---- |
| Anterior Hippocampus | Relational processing and detail recombination | Mirrors the role of cross-attention in linking disparate data points.41 |
| Medial Prefrontal Cortex | Strategic scenario building and self-projection | Functional analog to high-level policy or reasoning layers.2 |
| Medial Temporal Lobe | Pattern completion and separation | Essential for preventing the blending of similar but distinct memories.3 |
| Posterior Cingulate | Spatial clarity and perceptual grounding | Mirrors the need for grounding mechanisms in generative systems.39 |

The hippocampus is notably more active during imagination than during simple retrieval, reflecting the increased "recombination demand" required to assemble novel scenarios from fragmented episodic details.41 This intensity of constructive processing is exactly where error typically enters the system: miscombining elements of the past or confusing imagined scenarios with actual occurrences.39 In patients with hippocampal damage, the inability to provide "internal" (episodic) details results in communications that are general, semanticized, and lacking in spatiotemporal richness—a direct analog to an AI system defaulting to a generic "consensus style" when its specific data triggers are weak.45

### **Specificity Induction as a Corrective Measure**

A pivotal finding in this research is that "episodic specificity induction"—brief training in describing specific past events—can shift the cognitive system from a gist-based mode to a detail-oriented mode.47 This induction increases the quality of subsequent future simulations and even creative thinking tasks.43 For trigger-indexed research systems, this provides scientific justification for providing specific "story beats" or "verification stories" within the input. By inducing a state of specificity, the generative system is forced to bypass its semantic centroid and operate in a "high-resolution" constructive mode.39

## **Schemas as Default Frameworks: The Brewer-Nakamura Perspective**

Building upon Bartlett’s insights, William F. Brewer and Glenn V. Nakamura’s 1984 study, *The Nature and Functions of Schemas*, provided empirical evidence for the "framework hypothesis".49 They argued that schemas are not just after-the-fact retrieval tools but structural foundation pieces necessary for the initial encoding and preservation of episodic information.49

### **The Default to the Statistical Centroid**

Brewer and Nakamura demonstrated that memory for unorganized or schema-inconsistent information is significantly poorer than memory for organized scenes.49 However, the presence of a strong schema can lead to "false alarms"—remembering things that weren't there but *should* have been according to the schema.49

1. **Framework Activation:** If a schema (title or picture) is provided *before* information is encountered, recall is significantly improved.49  
2. **Statistical Inference:** In the absence of a specific framework, the brain abstracts a "generic cognitive representation"—a schema—based on cultural and environmental regularities.49  
3. **Centroid Regressions:** This abstraction process intentionally discards "outliers" (idiosyncratic details) in favor of the "organized mass".12

This research establishes that "schema activation is the default cognitive process." Without a specific trigger, the mind (and by extension, the large language model) defaults to the most active relational cluster—the statistical centroid.49

## **Synthesizing Human and Computational Failures: The "Bible Critique" Case Study**

The "Bible Critique" problem in Large Language Models offers a precise case study for these theoretical frameworks. When an LLM is asked to provide a critique of the Bible without specific constraints, it often produces a generic, middle-of-the-road summary.7 This phenomenon is frequently misdiagnosed as a "prompt engineering failure," but the research indicates it is a "schema activation failure".6

### **Spurious Correlations and Syntax-Domain Links**

A recent MIT study reveals that LLMs often mistakenly link specific sentence patterns (grammatical structures) with specific topics.6 If a model associates a particular "critical" syntactic template with geography, it may fail to apply that template correctly to theology.6

| Problem | Computational Cause | Human Cognitive Analog |
| :---- | :---- | :---- |
| Statistical Centroid | Optimizing for cross-entropy over a mixture of observers.7 | Cultural assimilation toward social norms.22 |
| Spurious Syntax Link | Over-reliance on "syntactic templates" from training.6 | Stereotypical bias; schematic interference.16 |
| Representation Fidelity | Mimicking the style of the consensus hull.7 | Gist-based recall that discards specific details.33 |
| Logic Drift | Autoregressive prediction without grounding checks.7 | Rationalization of incoherent story elements.12 |

The Bible Critique centroid occurs because the "critical schema" for such a vast and controversial text is diffuse. The most "likely" next token in the training set is drawn from the average of millions of observers, leading to a "Consensus Hull" response.7 To break this regression to the mean, the system requires "finding-level specificity"—a named person (e.g., "Voltaire's critique"), a verified story (e.g., "the council of Nicaea controversy"), or a precise mechanism (e.g., "documentary hypothesis").6 These triggers activate specific, narrower schemas that have few centroid-compatible interpretations, forcing the system to move beyond generic reconstruction toward high-fidelity synthesis.29

## **CCP Application: Confirming the Efficacy of Trigger-Indexed Research**

The research directives for CCP application are decisively confirmed by the intersection of Bartlett’s, Tulving’s, and Schacter’s work. The constructive nature of memory ensures that information is never "replayed" but always "re-assembled" through the lens of currently active schemas.1

### **Active Schemas as Reconstructive Templates**

Research findings are invariably reconstructed through the most active schema.17 In human memory, if a participant is operating under a "battle schema," they will reconstruct the "War of the Ghosts" as a battle, regardless of the ghosts' actual presence in the text.12

For a trigger-indexed research system, the "trigger" acts as a specificity induction. By indexing research at the finding level rather than the topical level, the system provides a reconstruction template that is as specific as the original encoding context.25

| Research Strategy | Schema Activation Level | Resulting Output |
| :---- | :---- | :---- |
| Topical Research | Broad/General | Regression to the statistical centroid; high "gist" but low accuracy.7 |
| Generic Research | Average/Middle | Regression toward the Consensus Hull; plausible but inaccurate.7 |
| Finding-Level Specificity | Narrow/High-Resolution | Correct reconstruction of idiosyncratic details; high fidelity.29 |

### **The Power of Verified Story Beats**

Finding-level specificity—incorporating names, verified stories, and precise mechanisms—provides a superior template because it leverages the anterior hippocampus's relational memory capabilities.41 These specific details act as "hard constraints" that override the parametric knowledge shortcuts that often cause LLMs to fail on atypical relations.29

When a model is forced to attend to a "causal graph" extracted from a specific narrative, it avoids inferring causality from mere event order or world knowledge.29 This confirms that a trigger-indexed system, which provides these story-beat constraints, will consistently outperform a generic retrieval system in the accuracy of its reconstructions.

## **Nuanced Conclusions and Actionable Synthesis**

The investigation into constructive memory and encoding specificity provides a robust scientific foundation for the development of high-fidelity information synthesis systems. The core insights are summarized as follows:

* **Memory is inherently reconstructive:** In both biological and artificial neural networks, recall is a generative act performed through the filter of available schemas.1  
* **The "Centroid Problem" is a schema failure:** Generic inputs fail to activate narrow schemas, causing systems to default to the statistical average (Consensus Hull) of their training or experience.7  
* **Encoding specificity is the key to accessibility:** Retrieval is successful only when retrieval cues (triggers) align with the specific conditions of the information's initial encoding.23  
* **Induction of specificity overrides heuristic errors:** Brief exposure to specific details (specificity induction) shifts the constructive engine from a gist default to a high-fidelity mode.47

### **Strategic Recommendations**

To mitigate the statistical centroid problem and leverage the constructive architecture of memory, next-generation research systems should:

1. **Replace topical indices with trigger-based finding indices:** Ensure that retrieval cues include "hard" identifiers like named individuals, specific dates, and precise mechanical descriptions to narrow the activated schema.23  
2. **Implement episodic specificity priming:** Precede generative tasks with detailed, verifiable "story beats" from the research substrate to shift the model into a detail-oriented constructive mode.47  
3. **Enforce "Contextual Fit" through causal graphs:** Require the explicit extraction and integration of causal relationships from the source material to prevent "logic drift" and regression toward parametric priors.7  
4. **Bypass social/statistical attractors:** Explicitly instruct the system to ignore consensus-level information in favor of idiosyncratic finding outliers, countering the inherent leveling effect of cultural schemas.7

By adopting these principles, trigger-indexed systems can replicate the adaptive power of human episodic memory—the ability to flexibly combine past findings to solve future problems—while avoiding the catastrophic distortions that occur when specific truths are leveled into statistical centroids. The quality of any synthesized output is, in the final analysis, a function of the specificity of the triggers used to invoke the system’s constructive capacity.6

#### **Sources des citations**

1. Reconstructive Memory & Schema Theory | McGraw Hill Canada, consulté le mars 10, 2026, [https://www.mheducation.ca/blog/series-classic-learning-science-reconstructive-memory-schema-theory](https://www.mheducation.ca/blog/series-classic-learning-science-reconstructive-memory-schema-theory)  
2. Constructive Memory \- The Decision Lab, consulté le mars 10, 2026, [https://thedecisionlab.com/reference-guide/psychology/constructive-memory](https://thedecisionlab.com/reference-guide/psychology/constructive-memory)  
3. The cognitive neuroscience of constructive memory: remembering the past and imagining the future \- PMC, consulté le mars 10, 2026, [https://pmc.ncbi.nlm.nih.gov/articles/PMC2429996/](https://pmc.ncbi.nlm.nih.gov/articles/PMC2429996/)  
4. The Seven Sins of Memory: An Update \- PMC \- NIH, consulté le mars 10, 2026, [https://pmc.ncbi.nlm.nih.gov/articles/PMC8285452/](https://pmc.ncbi.nlm.nih.gov/articles/PMC8285452/)  
5. Tulving's Memory : Canadian Journal of Psychology \- Ovid, consulté le mars 10, 2026, [https://www.ovid.com/journals/cajpsy/fulltext/10.1037/h0080876\~tulvings-memory](https://www.ovid.com/journals/cajpsy/fulltext/10.1037/h0080876~tulvings-memory)  
6. Researchers discover a shortcoming that makes LLMs less reliable ..., consulté le mars 10, 2026, [https://news.mit.edu/2025/shortcoming-makes-llms-less-reliable-1126](https://news.mit.edu/2025/shortcoming-makes-llms-less-reliable-1126)  
7. Why Large Language Models are Trapped in Consensus Hull | by Sean Wu | Medium, consulté le mars 10, 2026, [https://opencui.medium.com/why-large-language-model-is-trapped-in-consensus-hull-cbe1eb29ebb7](https://opencui.medium.com/why-large-language-model-is-trapped-in-consensus-hull-cbe1eb29ebb7)  
8. NarrativeLoom: Enhancing Creative Storytelling through Multi-Persona Collaborative Improvisation \- arXiv, consulté le mars 10, 2026, [https://arxiv.org/html/2603.07155v1](https://arxiv.org/html/2603.07155v1)  
9. Bartlett (Memory) \- Study Mind, consulté le mars 10, 2026, [https://studymind.co.uk/notes/bartlett-memory/](https://studymind.co.uk/notes/bartlett-memory/)  
10. Remembering: A Study in Experimental and Social Psychology \- ResearchGate, consulté le mars 10, 2026, [https://www.researchgate.net/publication/229679511\_Remembering\_A\_Study\_in\_Experimental\_and\_Social\_Psychology](https://www.researchgate.net/publication/229679511_Remembering_A_Study_in_Experimental_and_Social_Psychology)  
11. remembering \- a study in experimental and \- MPG.PuRe, consulté le mars 10, 2026, [https://pure.mpg.de/rest/items/item\_2273030/component/file\_2309291/content](https://pure.mpg.de/rest/items/item_2273030/component/file_2309291/content)  
12. The War of the Ghosts, consulté le mars 10, 2026, [https://mechanism.ucsd.edu/bill/teaching/philpsych.w03/memory4class.pdf](https://mechanism.ucsd.edu/bill/teaching/philpsych.w03/memory4class.pdf)  
13. Bartlett, Functionalism, and Modern Schema Theories \- The Journal of Mind and Behavior, consulté le mars 10, 2026, [https://jmb-online.com/pdf/05/Pages-from-JMB-21-1-2-37.pdf](https://jmb-online.com/pdf/05/Pages-from-JMB-21-1-2-37.pdf)  
14. (PDF) Bartlett's concept of schema in reconstruction \- ResearchGate, consulté le mars 10, 2026, [https://www.researchgate.net/publication/257472575\_Bartlett's\_concept\_of\_schema\_in\_reconstruction](https://www.researchgate.net/publication/257472575_Bartlett's_concept_of_schema_in_reconstruction)  
15. Bartlett's War Of The Ghosts | Procedure, Results, Strengths & Weaknesses, consulté le mars 10, 2026, [https://online-learning-college.com/knowledge-hub/gcses/gcse-psychology-help/bartletts-war-of-the-ghosts/](https://online-learning-college.com/knowledge-hub/gcses/gcse-psychology-help/bartletts-war-of-the-ghosts/)  
16. Bartlett's War of the Ghosts Study (AQA GCSE Psychology): Revision Note, consulté le mars 10, 2026, [https://www.savemyexams.com/gcse/psychology/aqa/19/revision-notes/memory/memory-as-an-active-process/bartletts-war-of-the-ghosts-study/](https://www.savemyexams.com/gcse/psychology/aqa/19/revision-notes/memory/memory-as-an-active-process/bartletts-war-of-the-ghosts-study/)  
17. Bartlett War of the Ghosts: Summary & Evaluation | Vaia, consulté le mars 10, 2026, [https://www.vaia.com/en-us/explanations/psychology/cognition/bartlett-war-of-the-ghosts/](https://www.vaia.com/en-us/explanations/psychology/cognition/bartlett-war-of-the-ghosts/)  
18. Bartlett's War of the Ghosts Study | PDF | Schema (Psychology) | Memory \- Scribd, consulté le mars 10, 2026, [https://www.scribd.com/document/357437772/KEY-STUDY-Bartlett-1932-War-of-the-Ghosts-4](https://www.scribd.com/document/357437772/KEY-STUDY-Bartlett-1932-War-of-the-Ghosts-4)  
19. MEMORY DISTORTIONS, consulté le mars 10, 2026, [https://us.sagepub.com/sites/default/files/upm-binaries/14511\_Chapter6.pdf](https://us.sagepub.com/sites/default/files/upm-binaries/14511_Chapter6.pdf)  
20. Bartlett War of Ghosts | PDF | Schema (Psychology) | Memory \- Scribd, consulté le mars 10, 2026, [https://www.scribd.com/document/492107933/Bartlett-War-of-Ghosts](https://www.scribd.com/document/492107933/Bartlett-War-of-Ghosts)  
21. Adaptive constructive processes and the future of memory \- PMC \- NIH, consulté le mars 10, 2026, [https://pmc.ncbi.nlm.nih.gov/articles/PMC3815569/](https://pmc.ncbi.nlm.nih.gov/articles/PMC3815569/)  
22. Social Psychology of Remembering (Chapter 5\) \- The Constructive Mind, consulté le mars 10, 2026, [https://www.cambridge.org/core/books/constructive-mind/social-psychology-of-remembering/4122008B75A39E6D7F4F99CAF454ACD4](https://www.cambridge.org/core/books/constructive-mind/social-psychology-of-remembering/4122008B75A39E6D7F4F99CAF454ACD4)  
23. Memory-Related Encoding-Specificity Paradigm: Experimental Application to the Exercise Domain \- PMC, consulté le mars 10, 2026, [https://pmc.ncbi.nlm.nih.gov/articles/PMC7909183/](https://pmc.ncbi.nlm.nih.gov/articles/PMC7909183/)  
24. Précis of Elements of episodic memory | Behavioral and Brain Sciences | Cambridge Core, consulté le mars 10, 2026, [https://www.cambridge.org/core/journals/behavioral-and-brain-sciences/article/precis-of-elements-of-episodic-memory/8EA952C5CDFC4F0AEC3555E7301F8E8A](https://www.cambridge.org/core/journals/behavioral-and-brain-sciences/article/precis-of-elements-of-episodic-memory/8EA952C5CDFC4F0AEC3555E7301F8E8A)  
25. Encoding specificity principle \- Wikipedia, consulté le mars 10, 2026, [https://en.wikipedia.org/wiki/Encoding\_specificity\_principle](https://en.wikipedia.org/wiki/Encoding_specificity_principle)  
26. Encoding Specificity Principle \- The Decision Lab, consulté le mars 10, 2026, [https://thedecisionlab.com/reference-guide/psychology/encoding-specificity-principle](https://thedecisionlab.com/reference-guide/psychology/encoding-specificity-principle)  
27. The history of episodic memory \- PMC, consulté le mars 10, 2026, [https://pmc.ncbi.nlm.nih.gov/articles/PMC11449151/](https://pmc.ncbi.nlm.nih.gov/articles/PMC11449151/)  
28. Tulving's Memory \- Ovid, consulté le mars 10, 2026, [https://www.ovid.com/journals/cajpsy/pdf/10.1037/h0080876\~tulvings-memory](https://www.ovid.com/journals/cajpsy/pdf/10.1037/h0080876~tulvings-memory)  
29. Failure Modes of LLMs for Causal Reasoning on Narratives \- arXiv, consulté le mars 10, 2026, [https://arxiv.org/html/2410.23884v5](https://arxiv.org/html/2410.23884v5)  
30. The seven sins of memory. Insights from psychology and cognitive neuroscience \- PubMed, consulté le mars 10, 2026, [https://pubmed.ncbi.nlm.nih.gov/10199218/](https://pubmed.ncbi.nlm.nih.gov/10199218/)  
31. The Seven Sins of Memory \- Ness Labs, consulté le mars 10, 2026, [https://nesslabs.com/the-seven-sins-of-memory](https://nesslabs.com/the-seven-sins-of-memory)  
32. The Seven Sins of Memory \- Wikipedia, consulté le mars 10, 2026, [https://en.wikipedia.org/wiki/The\_Seven\_Sins\_of\_Memory](https://en.wikipedia.org/wiki/The_Seven_Sins_of_Memory)  
33. The seven sins of memory \- American Psychological Association (APA), consulté le mars 10, 2026, [https://www.apa.org/monitor/oct03/sins](https://www.apa.org/monitor/oct03/sins)  
34. MEMORY SYSTEMS \- Sage, consulté le mars 10, 2026, [https://uk.sagepub.com/sites/default/files/upm-binaries/14510\_Chapter4.pdf](https://uk.sagepub.com/sites/default/files/upm-binaries/14510_Chapter4.pdf)  
35. (PDF) The cognitive neuroscience of constructive memory \- ResearchGate, consulté le mars 10, 2026, [https://www.researchgate.net/publication/13734381\_The\_cognitive\_neuroscience\_of\_constructive\_memory](https://www.researchgate.net/publication/13734381_The_cognitive_neuroscience_of_constructive_memory)  
36. The Seven Sins of Memory: Additional Insights With Daniel L. Schacter \- Psi Chi, consulté le mars 10, 2026, [https://www.psichi.org/page/191EyeFall14cCannon](https://www.psichi.org/page/191EyeFall14cCannon)  
37. The Seven Sins of Memory (Chapters Summary) \- The mystery of decisions | Julia Collado, consulté le mars 10, 2026, [https://juliacollado.wordpress.com/2014/02/26/the-seven-sins-of-memory-chapters-summary/](https://juliacollado.wordpress.com/2014/02/26/the-seven-sins-of-memory-chapters-summary/)  
38. Beyond Absent Mindedness: The Seven Sins Of Memory \- BetterHelp, consulté le mars 10, 2026, [https://www.betterhelp.com/advice/memory/what-are-the-seven-sins-of-memory/](https://www.betterhelp.com/advice/memory/what-are-the-seven-sins-of-memory/)  
39. Memory and Imagination: Perspectives on Constructive Episodic Simulation (Chapter 8), consulté le mars 10, 2026, [https://www.cambridge.org/core/books/cambridge-handbook-of-the-imagination/memory-and-imagination-perspectives-on-constructive-episodic-simulation/CB23E7398C4B524E63D937BA15F2C3C0](https://www.cambridge.org/core/books/cambridge-handbook-of-the-imagination/memory-and-imagination-perspectives-on-constructive-episodic-simulation/CB23E7398C4B524E63D937BA15F2C3C0)  
40. The cognitive neuroscience of constructive memory: remembering the past and imagining the future \- PubMed, consulté le mars 10, 2026, [https://pubmed.ncbi.nlm.nih.gov/17395575/](https://pubmed.ncbi.nlm.nih.gov/17395575/)  
41. The Hippocampus and Imagining the Future: Where Do We Stand? \- Frontiers, consulté le mars 10, 2026, [https://www.frontiersin.org/journals/human-neuroscience/articles/10.3389/fnhum.2011.00173/full](https://www.frontiersin.org/journals/human-neuroscience/articles/10.3389/fnhum.2011.00173/full)  
42. On the Seven Sins of Memory with Daniel Schacter \- Bridging the Gaps, consulté le mars 10, 2026, [https://www.bridgingthegaps.ie/2015/01/on-the-seven-sins-of-memory-with-daniel-schacter/](https://www.bridgingthegaps.ie/2015/01/on-the-seven-sins-of-memory-with-daniel-schacter/)  
43. Constructive Memory and Conscious Experience \- Smith Scholarworks, consulté le mars 10, 2026, [https://scholarworks.smith.edu/cgi/viewcontent.cgi?article=1241\&context=psy\_facpubs](https://scholarworks.smith.edu/cgi/viewcontent.cgi?article=1241&context=psy_facpubs)  
44. Putting Together the Puzzle of Adaptive Constructive Memory, consulté le mars 10, 2026, [https://www.cogneurosociety.org/adapting-to-a-new-way-of-thinking-about-our-constructive-memory/](https://www.cogneurosociety.org/adapting-to-a-new-way-of-thinking-about-our-constructive-memory/)  
45. Contributions of Episodic Memory to Imagining the Future, consulté le mars 10, 2026, [https://sites.harvard.edu/schacter-memory/files/2022/09/Contributions-of-Episodic-Memory-to-Imagining-the-Future.pdf](https://sites.harvard.edu/schacter-memory/files/2022/09/Contributions-of-Episodic-Memory-to-Imagining-the-Future.pdf)  
46. Imagining the future: evidence for a hippocampal contribution to constructive processing \- PMC, consulté le mars 10, 2026, [https://pmc.ncbi.nlm.nih.gov/articles/PMC3838494/](https://pmc.ncbi.nlm.nih.gov/articles/PMC3838494/)  
47. \[PDF\] The cognitive neuroscience of constructive memory: remembering the past and imagining the future | Semantic Scholar, consulté le mars 10, 2026, [https://www.semanticscholar.org/paper/The-cognitive-neuroscience-of-constructive-memory%3A-Schacter-Addis/dcdb11e347b552d79935b9979e0394790651650d](https://www.semanticscholar.org/paper/The-cognitive-neuroscience-of-constructive-memory%3A-Schacter-Addis/dcdb11e347b552d79935b9979e0394790651650d)  
48. Remembering the past and imagining the future: Identifying and enhancing the contribution of episodic memory \- PMC, consulté le mars 10, 2026, [https://pmc.ncbi.nlm.nih.gov/articles/PMC5289412/](https://pmc.ncbi.nlm.nih.gov/articles/PMC5289412/)  
49. (Open Access) The nature and functions of schemas. (1984) | William F. Brewer \- SciSpace, consulté le mars 10, 2026, [https://scispace.com/papers/the-nature-and-functions-of-schemas-5ckxrm4919](https://scispace.com/papers/the-nature-and-functions-of-schemas-5ckxrm4919)  
50. Role of Schemata in Memory for Places \- Semantic Scholar, consulté le mars 10, 2026, [https://www.semanticscholar.org/paper/Role-of-schemata-in-memory-for-places-Brewer-Treyens/66320acefb2caffe1b93c45e2b0017e4745491fd](https://www.semanticscholar.org/paper/Role-of-schemata-in-memory-for-places-Brewer-Treyens/66320acefb2caffe1b93c45e2b0017e4745491fd)  
51. The nature and functions of schemas. \- Semantic Scholar, consulté le mars 10, 2026, [https://www.semanticscholar.org/paper/The-nature-and-functions-of-schemas.-Brewer-Nakamura/e0cb87c89e702d559a2f11ae418793eb5ac5c6a7](https://www.semanticscholar.org/paper/The-nature-and-functions-of-schemas.-Brewer-Nakamura/e0cb87c89e702d559a2f11ae418793eb5ac5c6a7)  
52. Nature and Functions of Schemas | PDF \- Scribd, consulté le mars 10, 2026, [https://www.scribd.com/document/958854840/function-of-scheme](https://www.scribd.com/document/958854840/function-of-scheme)  
53. (PDF) The schema : a structural or a functional pattern \- ResearchGate, consulté le mars 10, 2026, [https://www.researchgate.net/publication/49176140\_The\_schema\_a\_structural\_or\_a\_functional\_pattern](https://www.researchgate.net/publication/49176140_The_schema_a_structural_or_a_functional_pattern)  
54. COLING 2018 The 27th International Conference on Computational Linguistics Proceedings of System Demonstrations August 20-26, 2018 Santa Fe, New Mexico, USA, consulté le mars 10, 2026, [http://coling2018.org/wp-content/uploads/2018/08/coling18-demo.pdf](http://coling2018.org/wp-content/uploads/2018/08/coling18-demo.pdf)

[image1]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAmwAAAAiCAYAAADiWIUQAAAK5klEQVR4Xu2beahvVRXHv9FM2UxRGWWpTUaFlRQNPyujubREGygjKm2wyAbTSk2kDBvMosGs9xSbnjlgEyXxoyC0JCoypQGuUolJRUF/pJTtT+ssz/rtd+69vndvL376/cDi/s75nbPP3muvs9f3rPO7kjHGGGOMMcYYY4wxxhhjjDHGGGOMMcYYY4wxxhhjjDHGGGOMMcYYY4wxxhhjjDHGGGOMMcYYY4wxxhhjjDHGGGOMMcYYY4wxxphl51bNXtXshmb3Hex3zb5WD5rgzs0e0u/suEOz85rdrf9iA3Bd+vvw/ouB+zTb1uwJirEc1OyqZretB+0gz262pdnfu/23NO7a7PRmz2p2YrN/K3w8a7Z1POx/DjH7nGb/VFyfmLip7NPsw4q+/z8gbu9Ytu+puNduU/btau7R7DfNDhi26d8fm33ixiN2nls3O7LZ0c3upJi7Q5r9stm9ynE7ylMVbe0M+Jo+GWPM0nFSsz+X7XcrBNxaPLnZo/udHSyoz+93bgL0d7UkffdmP1GIxeQYRX93BsbwxWaPaPak7rtbGk/UmCTxye/Ld/h4V/IG7ZzoIrYRTc/ov9hFELsIl4QHib3L9kZ5V7OLm13S7CPdd1Mgwi9SiLbKXxUPOxuF/vyl24cgPFsbE1zn9Dt3gAcrBKkxxiwdJN76NH25YhFPHtDs1YpqBovsoQpR9NJmD1RUoA5rtmezVwzHwJua7Td8TmjrtYq2gPNpGzivHs/TOd/RblbIWGyvvvGI7SHJ1EROxY3xVIFX+8A16f9dFNfZd9gHJIbXKZLXi7VYEaAygh8QrXn8WxXn097Bwz6S8zMVY0FkYBzPeYjZWm3hWCpHVCR3K/v68yvsRyxVYUzfuD7j2Sxup8UE/g+F+Emy2jrlA6BPByrGk2MD5vXpiiodY0mYd+ZoNYi/b5bt/Zu9UuFPfFHnJeH7KzTGbZJ9oMLE+fTx9cN+hH7GasZ5f42peaENxs9ccgzbb1H47XnDNn04Kk8YwAfcNy8YtjmXfhOfXJO5nnpQoq3vKARYQv9/rrFyNgX3yvH9TkXFlHuGNpj3FJn0g/snWSvWOA7xWPuUECMVjmXtyHYeo/B7xvds2M89+H6FHxHduS7wF1/Ohm2gX4cp2iEu8eWjml2giAM+G2PMUsGinQLmKc1OUyzMwGJ7VrO9mn1dIYAOb/Y3ReK7f7N3NvtYs08qFl0qGLsrxAevWpIvK9p6rKItFvsPKdqhXSoNJGGqY1yXV0Ukos9pTIgvbHbt8HkKhGet/JyheP2S9H1gvPT/SkX/f6XxdSuJ+WTFq7cq2Fj4f6hIOghbqggIGo6hHRIFfee4E5r9VHEtxnJcs1MVSfhCLVZBOI6kTJK9RnE+yQnB+SWN52cCxMffVyS7U4bjSVzsI6lva/bQ4diE7/PVd2/31qJoWgtiBiFZoe3eBwljQ4xT2ajzcaniFfe5CgHI2Jgj4o05IkamIGHXqh5zwOtaKn/MC9ehIpggvmmfuewFW/bh2GbfU7T1EoUoJNbPV8TkexRxTv/yGsQvbR2hsa+IDcbLHDCXxBMVrI8qxD/3BbHFfYbo5x6CnE/+Eh+0i48Z148U12R7qjqEL3jdi8/xIXPxccV9xXWnYEz0h/NWg/jjnktxjn/PHj6vF2vcs2/u9k3BPcb9kf56pMKviCquRxzkOoKvGCPfzRTzij+5R4jh9w3H4TsEGcKf++25ivaJwd8qxpD3uTHGLAUs2nONFSgW2FzIZs3+pUgqLPqPH/azeJPMAJFAoqrbQBUFAZRVkFmzzyja+pairaw8UBlISHxAYkX8AQt/iqW51v5tDa92T+p3Dsy0fR/oJ/3PhNQLls9rsZKzhxYF4dsVSe9xiv6uDPtJJCQ0xof4yooCfeO1LcyHbTheUT0ErscY1zv/ao3nMA4SJsciSBCKiL+cj82EuUhhXWG79wGGwMk+X6aYz34//aevxBtzRLwxR1NwHHOAsMntGoPAnFAdqzBXXD/p+0BC53eK+Jxz0+e0v941iJ9+XvBHjZ25xvmeiv06nwgt/IBfuGbGJ9fjuj0nls+IkpdrnPuXle8qjA/hMhUjCEpgDFQWU9QRX/RhvVhjPZlrnKNKClRAVOd9Dtxv+OD2CrFGm31VfUXjOfTvD81eoxB9+Jdz8Bvk2lHvawRv+tkYY5YGFq4qgEhqmaj4TCWDJ9cUdEASYmFNOJ7Fu2dF48JKW1QHaKvCufU3LpkAEV4IRxZfFm6SK7DY8sS/GjconrinWKsPfXJPLtKiAKRtREVC3xABJAU+n1O+S/L7PoHjM/pD4uY6KYBWtJjE8vxMgpDn8Dehb1S+GN9m/qNHD0I3BURP7wOEB//EkmTC7/cnxBs+qfHWMyUY+zhC5KSASojZtfpGXOXcVgGW9NfIeUHcpPBiPrJvCJOVYT9cq8XYrPdNPS+/Q2wA18QnUB+WKinYsrL2FY2/S3vj8LeH+2trv1MhTFOwcf/x4JX9wl/4bb1Yy1jv7zXaq7HDPUk/IOM7fZfjZ15qVRE/Iq6BvlB95jr9w1a/diT9fWOMMUsBYqRfMHkq5pXCTIsJ51PN7qeobpC0eT3E4t4nwoTFMhf/mcanWhJJtoUwuXLYf+DwF3jlyFMy1QGS+FGKJMZ++pYJpUKCXWsxnmn7PgD97xf1hKd3xppQEcjkQYLgeryCAvb3wo+EkomHpJvn0keEMt/j9xRyjIuEvMewv55PcuM7/L6nIpFmVYO2+ceIKkBO1vTvnTYCfmKua5Wk0vsAQYOwAXzOuXspkvzFeZDileThinirc0SM9BAzKWAS5jB9yJjpQxW9QNweVLaZt9oHfMd/F/dCLqnXYFx1XhgjryUfNvyFLYr5OkUxlxnTvHJl3uYK8YIhtLKihH/SZ5BCjnGlfw8p3wOvohFmdXxUfXkVyPVWg3urtsU8vK1s01/6DQ/S+A88VNjWizXWEXxW79XTtfibtvpKeIvi5w+AT7OqznWYyxxHVgU5F7/UquXBGudv/2bXD9/tN/xF2OEj/M09ZIwxSwEJjIoCSeAdigWP31SxaJ+mWNTeq1gsETcswECS+6BGoTfX9G9VvqFIQkBbFyjaOkNjWyygP2j2AS3+APs8xTWOVoiiExRtkMh4VdSzrdmfml2nRZFZmepDrVpNkRWFBB/RT37zx/iqOLxci8cCInOf4TOJeT58pp2vKkQXkFyPVFQLfq2xglnPp9Lws2YvGrYRA/iIV0EkONpk7hgf+xFwm0lWOqhi8vcXi1//lykfkCAZ25mK3wiStIEx40uEBskXAUy8MUfEG3PUc5VijplrEncy1xiDzCt+zUSe0OdeVGQfqErtPezD51OCba7xGhyDwQGKeWEMcIlivEco5jIrwsQu48uY+bRijDyAQM4nAulpwz7is47rUsXYiOUK27SXAj6h8lcFUg9ijWo28cw8IHj6NhBwjAcxRcx/QTc91n6s+M0YxzH//cMU/b5QIX6ZhxzXVo39+K7ifshx5PqTx7LNud9WzAE+O1fhDyqPxykecgDx+FmNMWiMMWbJIQGTFDIJm+WE5M1v4bZo+r8hb24gYhChM639WtkYY4y5WXCN4qncSW+5odp3hRarusYYY4wxxhhjjDHGGGOMMcYYY4wxxhhjjDHGGGOMMcYYY4wxxhhjjDHGGGOMMcYYY4wxxhhjjDHGGGOMMcYYY4wxxhhjjDHGGGOMWWL+A6Qh/uDdtlXDAAAAAElFTkSuQmCC>