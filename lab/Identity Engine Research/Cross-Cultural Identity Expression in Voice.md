# **Cultural Modulation of Identity Expression in Voice Data: A Computational and Psycholinguistic Framework**

The production of coherent discourse is an interactive process that requires speakers to draw upon several different types of communicative knowledge that complement more code-based grammatical knowledge of sound, form, and meaning. Two aspects of communicative knowledge closely related to one another are expressive and social: the ability to use language to display personal and social identities, to convey attitudes and perform actions, and to negotiate relationships between self and other.1 In the context of globally deployable coaching products, such as the Cultural Bio-feedback Coaching System (CBCS), the extraction of identity from voice data necessitates a profound departure from English-centric keyword detection. The academic literature on cultural psychology and cross-cultural computational linguistics suggests that identity is not a static internal psychological phenomenon but a discursive construct that emerges through social action and language.3 This report delineates the theoretical underpinnings of cultural self-construal, provides a taxonomy of identity expression styles, examines the persistence of cultural markers in transcribed speech, and offers computational strategies for building culturally adaptive extraction systems.

## **Theoretical Foundations: The Mutual Constitution of Culture and Self**

The study of culture and self casts the understanding of identity or agency as central to the analysis and interpretation of behavior, demonstrating that cultures and selves define and build upon each other in an ongoing cycle of mutual constitution.4 Psychological realities are both biologically and socioculturally rooted, taking shape as individuals become attuned to the various environments they inhabit.4 Historically, mainstream personality psychology viewed the person as containing a set of biological potentials interacting within situational contexts. However, cultural psychology challenges this by focusing on the constraints and affordances inherent in the cultural environment that give shape to those biological potentials.5

### **Independent and Interdependent Self-Construal**

The seminal framework established by Markus and Kitayama (1991) posits two primary views of the self: independent and interdependent. In Western, primarily individualistic cultures, individuals possess an independent self-construal, where the person is seen as a bounded, unique, and more or less integrated motivational and cognitive universe.6 The cultural imperative in these societies is to become independent, unique, autonomous, and separate.6 Consequently, identity expression is direct, emphasizing internal traits and personal achievements.

In contrast, many Asian, African, and Latin American cultures prioritize an interdependent self-construal. Here, the self is defined in relation to others, reflecting the significant role of relationships with ingroup members in the construction of the self.5 The East Asian self, for example, is typically described as collectivistic, shaped by a common Confucian heritage that emphasizes roles, obligations, and social harmony.5 In these contexts, individuals must know their place and act accordingly, making the process of becoming a self contingent on seizing meanings from a relational environment.5

### **Neural Underpinnings of Cultural Identity**

Research in the emerging field of cultural neuroscience suggests that cultural values such as independence and interdependence are reflected in brain pathways.7 Active and sustained engagement in cultural tasks—daily routines designed to accomplish cultural values—yields culturally patterned neural activities.7 For example, in interdependent cultures, the representation of the "self" can neurally merge with significant others. Functional Magnetic Resonance Imaging (fMRI) studies have shown that native Chinese speakers exhibit a merger of the neural representation of "mother" with the "self" in brain activation patterns during self-reference tasks, a phenomenon not typically observed in Western samples.7

This neural overlap suggests that identity expression in collectivist cultures is not merely a linguistic preference but reflects a fundamentally different cognitive structure. Those with an interdependent identity are less likely to show "dispositional bias"—focusing on an individual's internal traits—and are more likely to elaborate on situational constraints and context when perceiving themselves and others.7

## **Taxonomy of Cultural Identity Expression Styles**

To build an effective extraction system, it is necessary to categorize the linguistic markers associated with different cultural frames. The following taxonomy identifies three primary styles: direct/individualist, relational/collectivist, and hybrid/diasporic.

### **Taxonomy of Identity Expression Patterns**

| Expression Style | Core Cultural Logic | Primary Linguistic Markers | Discursive Function |
| :---- | :---- | :---- | :---- |
| **Direct / Individualist** | Self as an autonomous, bounded entity. | 1st person singular ("I", "Me"); direct "I am" statements; internal trait adjectives. | Asserts uniqueness, autonomy, and personal agency.6 |
| **Relational / Collectivist** | Self as part of a social unit; focus on harmony. | Kinship terms; role nouns; passive voice; intransitive constructions; 1st person plural ("We"). | Emphasizes belonging, social roles, and situational context.5 |
| **Hybrid / Diasporic** | Self as multifaceted and fluid; navigating multiple worlds. | Code-switching; mixed metaphors; situational shifts in register or dialect. | Signals dual cultural affiliations; manages social distance and identity gaps.11 |

### **Linguistic Markers of Individualist Expression**

In individualist contexts, identity is often marked by a high frequency of first-person singular pronouns. Research has discovered a positive correlation between degrees of self-focus and the use of the word “I”.8 These speakers utilize agentive language—active transitive constructions like “The woman pushed the box”—where the agent’s action is connected to the subsequent result, conflating the action and the result into a single macro-event.14 This linguistic style explicitly connects the self to outcomes, reinforcing the theme of personal agency.

### **Linguistic Markers of Collectivist Expression**

Interdependent identity expression is characterized by "agent-backgrounding" or suppression. Speakers from cultures like Korea often prefer intransitive constructions (e.g., “The box moved”) to describe events, which backgrounds or eliminates the agent entirely.14 This structure focuses on the theme and its change of state as a simplex event rather than a causal one driven by an individual.14 Furthermore, "pro-drop" languages like Korean or Japanese frequently omit the subject (the "I") when it is recoverable from context, reflecting a cultural orientation toward group harmony rather than individual prominence.14

Relational identity is also expressed through the use of "relationship-implying language." First-person plural pronouns (e.g., “we”, “us”, “our”) indicate closeness and shared identity.10 The mere use of "we" implies the existence of a relationship and a shared understanding between the speaker and listener.10 In these cultures, identity is often framed through bare nouns representing kinship terms or roles, projecting a null possessor argument that allows for interpretation relative to the social group.9

## **Indirect Identity Expression: Narrative Framing and Positioning**

In cultures where direct self-assertion is discouraged, identity is not "stated" but "storied." Narrative identity—the internalized and evolving story of the self—provides individuals with a sense of unity and purpose.15 How people narrate suffering, change, and daily experiences reveals their cultural identity through indirect markers.

### **Positionality and Indexicality Principles**

According to the principles of sociocultural linguistics, identity is a relational phenomenon produced in linguistic interaction.3 Two key principles govern this:

1. **The Positionality Principle**: Identities encompass macro-level demographic categories but also include temporary interactional stances, participant roles, and local cultural positions.3 A speaker may express identity by taking an epistemic orientation (e.g., "I know this") or a specific footing within a conversation.  
2. **The Indexicality Principle**: Identities are indexed through overt mention of categories, but more importantly through pragmatic processes, implicatures, and stylistic structures associated with specific personas.3

### **Cross-National Variation in Narrative Identity: The Turner Study**

A comprehensive study of 438 adults across the United States, Japan, Denmark, and Israel reveals significant cultural differences in how people narrate adversity.18 While the "redemption" template—where bad events turn into good outcomes through personal growth—is a master narrative in the U.S., it does not fully capture identity expression in other contexts.18

#### **Japanese Narrative Indices**

Japanese narratives are characterized by "acceptance" rather than "agency." Instead of focusing on personal control to overcome difficulty, Japanese narrators often adopt a stance of accepting what has transpired, reflecting a cultural inclination toward fatalism (e.g., "que sera, sera").18 Furthermore, they often display an "attribution of blame" that is internally focused. This "darker side of agency" involves taking absolute responsibility for life's failures and attributing them to a central character weakness, such as being "weak" or "avoiding difficulty," rather than externalizing the problem.18

#### **Danish Narrative Indices**

Danish narratives emphasize "normality" and "balanced affect." There is a tendency to frame experiences within the context of being ordinary or following standard life patterns.18 Meaning is made through "communal growth," focusing on development that occurs within the context of shared relationships rather than individual triumph.18

#### **Israeli Narrative Indices**

Israeli narratives are unique in their emphasis on "collective responsibility." This thematic focus on shared duty and the impact of events on the larger society is deeply embedded in Israeli culture, partly due to historical security concerns and mandatory military service.18 Israeli narrators often display a "collective sense of agency" (e.g., “we will fight; we will survive”), linking individual identity to the national "master narrative".18

## **Voice-Specific Cultural Markers in Transcribed Speech**

Spoken language, even when transcribed, contains unique identity markers that are absent from formal written questionnaires. These include discourse particles and code-switching patterns.

### **Discourse Markers as Identity Glue**

Discourse markers—expressions like *well*, *but*, *oh*, and *y'know*—function as the "glue" that binds a piece of talk together.1 They are sequentially dependent elements that bracket units of talk and index the speaker's relationship to the information and the listener.1

* **Hedges and Social Relationships**: Discourse particles like *kind of*, *sort of*, or *I guess* function as hedges, reducing the force of an utterance to maintain social harmony or express modesty.22  
* **Cognitive and Pragmatic Functions**: Markers like *oh* display information as "new" or "unexpected," while *well* can introduce a tangential or disputed claim.2  
* **Cultural Transfer**: Research on Japanese speakers of English shows that the use of native discourse markers can influence the frequency and positioning of English markers like *and*, *so*, and *but*.24 This transfer serves as a subtle indicator of the speaker's original cultural linguistic framework.

### **Code-Switching as a Marker of Hybrid Identity**

Code-switching—the alternation between two or more languages in a single conversation—is a sophisticated form of linguistic flexibility rather than a sign of deficiency.12 For multilingual individuals, language choice is a dynamic social act that reflects belonging, emotion, and power.12

* **Identity-Marking Role**: Code-switching enables bilinguals to express dual cultural affiliations and perform a "hybrid selfhood".11 For instance, a French-Arabic speaker might slip into Arabic to signal ethnic solidarity within a French-speaking context.13  
* **Communicative Strategy**: Switching can facilitate clarity or convey rhetorical nuance that is difficult to express in a single language.11  
* **Transcription Survival**: While prosodic cues like pitch or intonation are lost in transcription, the "within-utterance" and "within-turn" switches are perfectly preserved, providing clear evidence of the speaker's multicultural identity.25

## **Validated Cross-Cultural Identity Coding Systems**

Standard personality assessments, such as the Big Five, often live on the "surface," focusing on broad dispositional traits.26 However, identity is best captured through McAdams' three-level framework: (1) dispositional traits, (2) characteristic adaptations (motives and goals), and (3) narrative identity (the evolving life story).16

### **Adapting McAdams’ Narrative Coding**

McAdams' manual for coding "Agency" and "Communion" provides a starting point for identity extraction. Agency captures the degree to which one is active and efficacious, while communion captures the degree to which one is connected and warm.27 However, these constructs require cultural adaptation.

| Construct | Western Definition | Collectivist Adaptation / Alternate Index |
| :---- | :---- | :---- |
| **Agency** | Personal self-mastery and achievement.28 | "Collective Agency" or "Agency-as-Obligation" (meeting group expectations).18 |
| **Communion** | Love, friendship, and interpersonal dialogue.28 | "Collective Responsibility" and "Acceptance" of social fate.18 |
| **Redemption** | Personal growth through overcoming adversity.20 | "Balanced Affect" and "Normality" (finding meaning in standard roles).18 |

The study of narrative identity must be conducted in tandem with the cultural context, as standard American templates like "redemption" may lead to false negatives when analyzing Japanese or Danish speakers who value "acceptance" and "normality".18

## **Computational Approaches to Cross-Cultural Identity Detection**

The challenge for the CBCS is to move away from keyword-based systems that rely on polysemous terms and English-centric logic. Modern NLP offers several non-keyword approaches.

### **Abstract Meaning Representation (AMR) and Semantic Graphs**

To identify frames beyond word frequency, researchers utilize AMR to create semantic graphs.31 These graphs extract the core relationships between actors and events, capturing:

* **Verbal Senses and Roles**: Identifying who did what to whom, which is critical for detecting "agent-backgrounding" in collectivist speech.31  
* **Contextual Information**: Extracting time and location elements that provide the situational framing necessary for interdependent identity detection.31

### **Cultural Localization in Large Language Models**

Recent advancements in multilingual LLMs have enabled the localization of "culture-specific neurons".32 These are neuron populations more strongly associated with cultural propensities (values, norms, knowledge) than with purely linguistic signals.32 By isolating these neurons, models can be "intervened upon" to adjust their cultural awareness without retraining.32

* **Cultural Alignment**: Systems can be designed to apply cultural knowledge appropriately in specific situations where such knowledge is relevant.33  
* **Probing for Ideational Elements**: Computational probing can detect a model's understanding of culturally salient metaphors, proverbs, and norms, which are key indicators of a speaker's identity.32

### **Interactive Narrative Analytics (INA)**

INA combines computational narrative extraction with interactive visualization to support human sensemaking.34 Unlike traditional text analytics, INA is concerned with the holistic structure of narratives, including:

* **Event Sequences**: Tracking the temporal flow of a life story.34  
* **Causal Connections**: Identifying how a speaker links events to their self-understanding, which varies across cultures (e.g., causal coherence in individualist cultures vs. relational coherence in collectivist ones).34

### **Identity Lexicons and Disambiguation: The TIDE Approach**

The TIDE methodology focuses on the "Textual Identity Detection and Augmentation Lexicon" (TIDAL), which is designed to support multiple languages and handle the polysemy of identity terms.35 Rather than simple token matching, this approach uses:

* **Contextualization**: Associating terms with specific identity groups and connotations.35  
* **Disambiguation**: Using sense disambiguation to distinguish between identity-related and non-identity-related usage of words (e.g., "black" as a race vs. a color).35

## **Universal vs. Culturally Specific Dimensions of Identity**

A central goal of a globally deployable system is to distinguish between identity dimensions that are detectable across all cultures and those that require localized logic.

| Dimension | Universal (Across Cultures) | Culturally Specific (Required Local Logic) |
| :---- | :---- | :---- |
| **Agency / Communion** | Universal "metaconstructs" of the human experience.27 | Specific manifestations (e.g., "Fighter" vs. "Accepter").15 |
| **Narrative Coherence** | Universal cognitive ability to organize long-term memories.1 | Types of coherence (Causal vs. Relational vs. Thematic).34 |
| **Self-Referencing** | All humans distinguish between self and other.37 | Linguistic preference (Direct "I" vs. Passive/Intransitive "It").14 |
| **Adversity Framing** | All cultures have master narratives for difficult events.20 | Content of the arc (Redemption vs. Acceptance vs. Responsibility).18 |
| **Social Identifier** | Language always serves as a marker of belonging.38 | Markers used (Accent/Dialect vs. Code-switching vs. Role nouns).11 |

## **Recommendations for a Culturally Adaptive Identity Extraction System**

To address the current gaps in the CBCS and move toward a globally deployable product, the following strategic recommendations are proposed:

### **1\. Shift from Lexical to Structural Analysis**

The system must move beyond "I'm the type" keywords and incorporate syntactic parsing that detects the *omission* or *backgrounding* of the agent. By using Abstract Meaning Representation (AMR), the CBCS can identify when a speaker is expressing identity through relational positioning (e.g., "The team achieved success") even when direct self-referencing is absent.14

### **2\. Implement a Multilingual Code-Switching Module**

Given that French-English mixing is common, the system should treat code-switching as a primary identity signal rather than linguistic noise. The module should categorize switches based on their social function: "Identity-marking" (asserting heritage) vs. "Communicative strategy" (seeking clarity).11 This allows the CBCS to accurately capture the hybrid identities of diasporic users.

### **3\. Locally Adapt Narrative Coding Manuals**

The core McAdams constructs (Agency and Communion) should be supplemented with localized indices derived from research like the Turner study. Specifically, for East Asian users, the system should search for themes of "Acceptance" and "Self-to-Blame" as markers of high self-reflection, rather than penalizing them for a lack of Western-style "Redemption" or "Agency".18

### **4\. Utilize Context-Aware Disambiguation**

Integrate identity lexicons like TIDAL to manage polysemy across languages. The system must use the surrounding discourse to determine if a role noun (e.g., "mother," "student," "leader") is being used as a temporary descriptor or a central identity anchor.3

### **5\. Monitor Temporal and Relational Arcs**

Identity in voice journals is "emergent" and "contextual" rather than fixed.3 The CBCS should use Interactive Narrative Analytics (INA) to track how a user's self-positioning changes over time across different topics (e.g., career vs. family).34 This longitudinal view helps avoid false negatives that might occur in a single, self-effacing entry.

### **6\. Detect Subtle Voice-Transcribed Markers**

The extraction logic should prioritize discourse particles (hEdges, connectors) and "pro-drop" patterns that survive transcription.22 High usage of collective "we" and passive constructions should trigger a "relational identity" frame, ensuring that collectivist users are identified even when they do not use explicit identity keywords.10

## **Conclusion**

The cultural modulation of identity expression requires a sophisticated system that acknowledges the "mutual constitution" of culture and the self. For the CBCS, this means evolving from a detector of keywords to an analyzer of narrative frames and structural positions. By integrating the insights from cultural neuroscience, sociocultural linguistics, and modern NLP, the platform can capture the nuanced, indirect, and often hybrid ways that individuals across the globe define who they are. The transition from an independent Western template to a culturally adaptive framework will not only reduce false negatives but also provide a more authentic and impactful coaching experience for a diverse global audience.

#### **Works cited**

1. 3 Discourse Markers: Language, Meaning, and Context, accessed March 6, 2026, [https://www.blackwellpublishing.com/content/bpl\_images/content\_store/WWW\_Content/9780631205951/003.pdf](https://www.blackwellpublishing.com/content/bpl_images/content_store/WWW_Content/9780631205951/003.pdf)  
2. Discourse Markers Language, Meaning, and Context \- City Tech OpenLab, accessed March 6, 2026, [https://openlab.citytech.cuny.edu/wp-content/uploads/group-documents/19864/1522867039-MaschlerSchiffrinproofsfinal.pdf](https://openlab.citytech.cuny.edu/wp-content/uploads/group-documents/19864/1522867039-MaschlerSchiffrinproofsfinal.pdf)  
3. Identity and interaction: a sociocultural linguistic ... \- Mary Bucholtz, accessed March 6, 2026, [https://bucholtz.linguistics.ucsb.edu/sites/secure.lsit.ucsb.edu.ling.d7\_b/files/sitefiles/research/publications/BucholtzHall2005-DiscourseStudies.pdf](https://bucholtz.linguistics.ucsb.edu/sites/secure.lsit.ucsb.edu.ling.d7_b/files/sitefiles/research/publications/BucholtzHall2005-DiscourseStudies.pdf)  
4. Cultures and Selves: A Cycle of Mutual Constitution \- Stanford University, accessed March 6, 2026, [https://web.stanford.edu/\~hazelm/cgi-bin/wordpress/wp-content/uploads/2011/02/2010-Markus-Kitayama\_Culture-and-Self-A-cycle-of-mutual-constitution.pdf](https://web.stanford.edu/~hazelm/cgi-bin/wordpress/wp-content/uploads/2011/02/2010-Markus-Kitayama_Culture-and-Self-A-cycle-of-mutual-constitution.pdf)  
5. A decade ago Markus and Kitayama sparked a ... \- Description, accessed March 6, 2026, [https://www2.psych.ubc.ca/\~heine/docs/asianself.rtf](https://www2.psych.ubc.ca/~heine/docs/asianself.rtf)  
6. Culture and self: An empirical assessment of Markus and Kitayama's theory of independent and interdependent self- construals \- David Matsumoto, accessed March 6, 2026, [https://www.davidmatsumoto.com/content/1999%20Culture%20and%20Self.pdf](https://www.davidmatsumoto.com/content/1999%20Culture%20and%20Self.pdf)  
7. Cultural neuroscience of the self: understanding the social ..., accessed March 6, 2026, [https://pmc.ncbi.nlm.nih.gov/articles/PMC2894676/](https://pmc.ncbi.nlm.nih.gov/articles/PMC2894676/)  
8. Text-Based Detection of the Risk of Depression \- Frontiers, accessed March 6, 2026, [https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2019.00513/full](https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2019.00513/full)  
9. The Syntax of Null Possessors with Kinship Terms and Body Part Nouns in Vietnamese, accessed March 6, 2026, [https://www.mdpi.com/2226-471X/10/7/158](https://www.mdpi.com/2226-471X/10/7/158)  
10. Are Not the Same as : Causal Effects of Minor Language Var \- Information Technology \- UF Warrington College of Business, accessed March 6, 2026, [http://bear.warrington.ufl.edu/sela/Sela\_Wheeler\_Sarial-Abi\_2012.pdf](http://bear.warrington.ufl.edu/sela/Sela_Wheeler_Sarial-Abi_2012.pdf)  
11. (PDF) Code-Switching as a Marker of Hybrid Identity and Communicative Strategy in Multicultural Europe \- ResearchGate, accessed March 6, 2026, [https://www.researchgate.net/publication/395314895\_Code-Switching\_as\_a\_Marker\_of\_Hybrid\_Identity\_and\_Communicative\_Strategy\_in\_Multicultural\_Europe](https://www.researchgate.net/publication/395314895_Code-Switching_as_a_Marker_of_Hybrid_Identity_and_Communicative_Strategy_in_Multicultural_Europe)  
12. Identity and Code-Switching: Linguistic Flexibility in Multilingual Speakers | by Baghriche Rayane | Medium, accessed March 6, 2026, [https://medium.com/@baghricherayane05/identity-and-code-switching-linguistic-flexibility-in-multilingual-speakers-4327a95726b2](https://medium.com/@baghricherayane05/identity-and-code-switching-linguistic-flexibility-in-multilingual-speakers-4327a95726b2)  
13. Code-Switching as a Marker of Hybrid Identity and Communicative Strategy in Multicultural Europe, accessed March 6, 2026, [https://egarp.lt/index.php/JPURM/article/download/366/361](https://egarp.lt/index.php/JPURM/article/download/366/361)  
14. The Role of Language in Expressing Agentivity in Caused Motion ..., accessed March 6, 2026, [https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2022.878277/full](https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2022.878277/full)  
15. Variation in Narrative Identity is Associated with Trajectories of Mental Health over Several Years \- PMC, accessed March 6, 2026, [https://pmc.ncbi.nlm.nih.gov/articles/PMC4395856/](https://pmc.ncbi.nlm.nih.gov/articles/PMC4395856/)  
16. Narrative identity \- Wikipedia, accessed March 6, 2026, [https://en.wikipedia.org/wiki/Narrative\_identity](https://en.wikipedia.org/wiki/Narrative_identity)  
17. “I want to lift my people up”: Exploring the psychological correlates of racial themes within the life stories of midlife Black Americans \- PMC, accessed March 6, 2026, [https://pmc.ncbi.nlm.nih.gov/articles/PMC11891957/](https://pmc.ncbi.nlm.nih.gov/articles/PMC11891957/)  
18. Narrative Identity in Context: How Adults in Japan, Denmark, Israel, and the United States Narrate Difficult Life Events | Request PDF \- ResearchGate, accessed March 6, 2026, [https://www.researchgate.net/publication/384695615\_Narrative\_Identity\_in\_Context\_How\_Adults\_in\_Japan\_Denmark\_Israel\_and\_the\_United\_States\_Narrate\_Difficult\_Life\_Events](https://www.researchgate.net/publication/384695615_Narrative_Identity_in_Context_How_Adults_in_Japan_Denmark_Israel_and_the_United_States_Narrate_Difficult_Life_Events)  
19. Narrative identity in context: How adults in Japan, Denmark, Israel, and the United States narrate difficult life events \- PubMed, accessed March 6, 2026, [https://pubmed.ncbi.nlm.nih.gov/39374127/](https://pubmed.ncbi.nlm.nih.gov/39374127/)  
20. A Comparison of Turning-Point Memories Among US and UK Emerging Adults: Adversity, Redemption, and Unresolved Trauma \- PMC, accessed March 6, 2026, [https://pmc.ncbi.nlm.nih.gov/articles/PMC12382990/](https://pmc.ncbi.nlm.nih.gov/articles/PMC12382990/)  
21. Discourse Markers, accessed March 6, 2026, [https://warwick.ac.uk/fac/soc/al/globalpad-rip/openhouse/academicenglishskills/grammar/discourse/](https://warwick.ac.uk/fac/soc/al/globalpad-rip/openhouse/academicenglishskills/grammar/discourse/)  
22. Chapter 4 Spoken Discourse Pg. 77-92 | PDF \- Scribd, accessed March 6, 2026, [https://www.scribd.com/document/839958193/Chapter-4-Spoken-Discourse-pg-77-92](https://www.scribd.com/document/839958193/Chapter-4-Spoken-Discourse-pg-77-92)  
23. Discourse markers: a discourse-pragmatic view \- BU Personal Websites, accessed March 6, 2026, [https://people.bu.edu/bfraser/Pragmatically%20Oriented/Lewis%20-%20DM%20in%20E%20-%20A%20Prag.%20View.doc](https://people.bu.edu/bfraser/Pragmatically%20Oriented/Lewis%20-%20DM%20in%20E%20-%20A%20Prag.%20View.doc)  
24. A Cross-linguistic Analysis of Discourse Marker Use in Different Speech Tasks \- ERIC, accessed March 6, 2026, [https://files.eric.ed.gov/fulltext/EJ1414434.pdf](https://files.eric.ed.gov/fulltext/EJ1414434.pdf)  
25. Filling lexical gaps and more: code-switching for the power of expression by young bilinguals \- PMC, accessed March 6, 2026, [https://pmc.ncbi.nlm.nih.gov/articles/PMC9813271/](https://pmc.ncbi.nlm.nih.gov/articles/PMC9813271/)  
26. The stories in our minds: Enterprising students push narrative identity in unexpected directions, accessed March 6, 2026, [https://news.weinberg.northwestern.edu/2024/01/04/the-stories-in-our-minds/](https://news.weinberg.northwestern.edu/2024/01/04/the-stories-in-our-minds/)  
27. Synthesizing contemporary integrative interpersonal theory and the narrative identity approach to examine personality dynamics a \- ZORA, accessed March 6, 2026, [https://www.zora.uzh.ch/server/api/core/bitstreams/4d6dfb92-61da-480c-8edf-69db544fe3ee/content](https://www.zora.uzh.ch/server/api/core/bitstreams/4d6dfb92-61da-480c-8edf-69db544fe3ee/content)  
28. (PDF) Narrative Identity \- ResearchGate, accessed March 6, 2026, [https://www.researchgate.net/publication/269603657\_Narrative\_Identity](https://www.researchgate.net/publication/269603657_Narrative_Identity)  
29. Coding Autobiographical Episodes for Themes of Agency and Communion \- ResearchGate, accessed March 6, 2026, [https://www.researchgate.net/publication/251398635\_Coding\_Autobiographical\_Episodes\_for\_Themes\_of\_Agency\_and\_Communion](https://www.researchgate.net/publication/251398635_Coding_Autobiographical_Episodes_for_Themes_of_Agency_and_Communion)  
30. Themes of Agency and Communion In Significant Autobiographical Scenes \- ResearchGate, accessed March 6, 2026, [https://www.researchgate.net/publication/229863932\_Themes\_of\_Agency\_and\_Communion\_In\_Significant\_Autobiographical\_Scenes](https://www.researchgate.net/publication/229863932_Themes_of_Agency_and_Communion_In_Significant_Autobiographical_Scenes)  
31. Computational Narrative Framing: Towards Identifying Frames ..., accessed March 6, 2026, [https://tugraz.elsevierpure.com/en/publications/computational-narrative-framing-towards-identifying-frames-throug/](https://tugraz.elsevierpure.com/en/publications/computational-narrative-framing-towards-identifying-frames-throug/)  
32. Isolating Culture Neurons in Multilingual Large Language Models \- arXiv.org, accessed March 6, 2026, [https://arxiv.org/html/2508.02241v1](https://arxiv.org/html/2508.02241v1)  
33. Culture is Not Trivia: Sociocultural Theory for Cultural NLP \- arXiv, accessed March 6, 2026, [https://arxiv.org/html/2502.12057v1](https://arxiv.org/html/2502.12057v1)  
34. Interactive Narrative Analytics: Bridging Computational Narrative Extraction and Human Sensemaking \- arXiv, accessed March 6, 2026, [https://arxiv.org/html/2601.11459v1](https://arxiv.org/html/2601.11459v1)  
35. arxiv.org, accessed March 6, 2026, [https://arxiv.org/html/2309.04027v2](https://arxiv.org/html/2309.04027v2)  
36. Personal narratives, relational selves: Residential histories in the living and telling \- Research Explorer \- The University of Manchester, accessed March 6, 2026, [https://research.manchester.ac.uk/en/publications/personal-narratives-relational-selves-residential-histories-in-th/](https://research.manchester.ac.uk/en/publications/personal-narratives-relational-selves-residential-histories-in-th/)  
37. Individual differences in physical self-representation \- CentAUR, accessed March 6, 2026, [https://centaur.reading.ac.uk/72226/1/21016798\_Chakraborty\_thesis.pdf](https://centaur.reading.ac.uk/72226/1/21016798_Chakraborty_thesis.pdf)  
38. Exploring the Deep Link Between Language and Identity | Salvador Ordorica, accessed March 6, 2026, [https://www.salvadorordorica.com/exploring-the-deep-link-between-language-and-identity/](https://www.salvadorordorica.com/exploring-the-deep-link-between-language-and-identity/)  
39. How Does Language Affect Cultural Identity? → Question \- Lifestyle → Sustainability Directory, accessed March 6, 2026, [https://lifestyle.sustainability-directory.com/question/how-does-language-affect-cultural-identity/](https://lifestyle.sustainability-directory.com/question/how-does-language-affect-cultural-identity/)  
40. Linguistic Predictors of Cultural Identification in Bilinguals \- PMC \- NIH, accessed March 6, 2026, [https://pmc.ncbi.nlm.nih.gov/articles/PMC5603315/](https://pmc.ncbi.nlm.nih.gov/articles/PMC5603315/)  
41. Ariana F. Turner's research works | Georgia Institute of Technology and other places, accessed March 6, 2026, [https://www.researchgate.net/scientific-contributions/Ariana-F-Turner-2184552063](https://www.researchgate.net/scientific-contributions/Ariana-F-Turner-2184552063)  
42. Computational Models of Identity Presentation in Language \- Carnegie Mellon University, accessed March 6, 2026, [https://kilthub.cmu.edu/articles/thesis/Computational\_Models\_of\_Identity\_Presentation\_in\_Language/21753632](https://kilthub.cmu.edu/articles/thesis/Computational_Models_of_Identity_Presentation_in_Language/21753632)