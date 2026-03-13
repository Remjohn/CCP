# **The Unified Computational Framework for Humor Synthesis: A Benign Violation Theory Approach**

The psychological phenomenon of humor has historically been characterized by its subjective and elusive nature, leading to a fragmented landscape of theoretical explanations. Traditional accounts, ranging from relief theories focusing on the discharge of nervous energy to superiority theories emphasizing the triumph over others, have struggled to provide a predictive and unified model capable of explaining why diverse stimuli such as puns, slapstick, and sarcasm all elicit the same response of amusement. The emergence of the Benign Violation Theory (BVT), codified primarily by A. Peter McGraw and Caleb Warren in 2010, represents a paradigm shift in humor research by providing an empirically validated, integrated framework that identifies the precise cognitive conditions necessary and sufficient for humor to occur.1 The theory posits that humor emerges when a situation is simultaneously appraised as a violation and as being benign.3 This architectural precision offers a deterministic foundation for computational systems, specifically the Humor Skill Guide, which replaces vague creative instructions with falsifiable parameters and structured data fields such as the Violation-Benignness Matrix.6

## **The Foundational Mechanics of Benign Violation Theory**

The Benign Violation Theory integrates and extends earlier conceptualizations, most notably the work of Tom Veatch and the broader incongruity-resolution literature.3 While incongruity theory suggests that humor arises from a mismatch between expectations and reality, it fails to distinguish between humorous surprises and non-humorous ones, such as witnessing a tragedy or winning a lottery.8 BVT resolves this by refining the definition of incongruity to focus on a specific type of threat: the violation.

### **The Simultaneous Appraisal of Disparate States**

The core claim of BVT is that humor requires two distinct and often contradictory appraisals to occur in the same cognitive moment: the perception that something is wrong (a violation) and the perception that the situation is nevertheless okay (benign).1 This requirement for simultaneity is what differentiates humor from other emotional states. If a violation is present without a benign appraisal, the result is negative emotion, such as fear, disgust, or anger.5 If a situation is benign but contains no violation, the result is apathy or a lack of engagement.3 Laughter, from an evolutionary perspective, serves as a social signal indicating that a potentially threatening situation—such as a play-fight or a mock attack—is actually safe.16

### **The Three-Variable Precision for Computational Modeling**

For the development of generative agents, the BVT offers a three-variable structure that can be operationalized into a skill template. These variables allow for the deterministic creation of humor beats by mapping specific violation types against appropriate benignness sources within a singular temporal frame \[Query\].

| Variable | Computational Equivalent | Function |
| :---- | :---- | :---- |
| Variable 1: Violation Type | DEP-ENG-004 Negative Space | Identifies the target norm or belief to be "attacked" based on audience sensitivity. |
| Variable 2: Benignness Source | Voice DNA / Psychological Distance | Provides the safety signal through agent warmth, credibility, or framing. |
| Variable 3: Simultaneity | Compilation Timing | Ensures the violation and safety registers register in the same cognitive moment. |

This structural specification eliminates the need for agents to "guess" at being funny. Instead, the agent executes a controlled activation of the semantic field defined by the audience’s Negative Space—what they care about protecting—while modulating the threat level through Voice DNA and psychological distance levers \[Query\].

## **Variable One: The Taxonomy of Violations**

A violation is defined as anything that threatens a person’s beliefs about how the world should be.3 This includes threats to physical well-being, identity, social conventions, and logical patterns.16 In the context of a computational architecture, these violations are drawn from DEP-ENG-004 Negative Space, which encodes the specific vulnerabilities and normative commitments of the target audience \[Query\].

### **Physical Violations and Primitive Humor**

The most basic forms of humor are rooted in apparent physical threats. Laughter in primates and human infants frequently occurs during tickling or rough-and-tumble play, which are characterized as mock attacks.3 These situations are physical violations because they involve feigned aggression, but they are benign because the participants trust each other and know no actual harm is intended.18 Slapstick humor operates on this same principle; an audience finds a person falling down funny only if the victim is unhurt or if the audience possesses enough social distance to be unconcerned with the victim’s well-being.19 If the observer cares about the victim and the injury appears serious, the situation ceases to be benign and becomes a malign violation, eliciting distress instead of amusement.19

### **Moral and Social Violations**

As humans evolved higher-order cognitive functions and complex social structures, the range of humorous violations expanded to include moral and social norms.2 A moral violation involves behaviors that people consider "wrong" or "disrespectful".2 McGraw and Warren (2010) tested this by presenting participants with scenarios such as a person using a dead chicken for sexual purposes before eating it.12 While such scenarios are widely considered disgusting and wrong, they can be perceived as humorous if the behavior is seen as harmless (the chicken was already dead) and the scenario is framed as hypothetical.2

Social violations involve breaches of etiquette, cultural practices, or identity expectations.16 Examples include awkward greetings, flatulence in formal settings, or unusual accents.15 The "Negative Space" encoded in DEP-ENG-004 is essential here, as what one group considers a minor social blunder, another might consider a severe identity threat \[Query\]. For a humor beat to succeed, the agent must identify a violation that is recognizable to the audience but not so severe that it cannot be rendered benign.5

### **Logical and Linguistic Violations**

Logical violations encompass absurdities, paradoxes, and departures from established patterns of reasoning.18 Linguistic violations are the foundation of wordplay and puns, where a single phrase or word breaks one communicative norm while adhering to another.16 For instance, a pun might use a word that is logically incorrect in the literal context but semantically relevant in a secondary sense.3 These are often considered "safe" or "benign-heavy" humor types because they rarely involve direct threats to a person's well-being or identity, making them ideal for audiences in a high-vigilance state.16

## **Variable Two: Mechanisms of Benignness**

For a violation to elicit laughter, the perceiver must reach an appraisal that the situation is "okay," "safe," or "acceptable".3 McGraw and Warren's research highlights three primary mechanisms that facilitate this benign appraisal: alternative norms, weak commitment, and psychological distance.1

### **Alternative Norms and Resolution**

A violation can seem benign if there is a salient alternative norm suggesting that the situation is acceptable.1 This is often referred to as "resolution" in the humor literature.2 In a joke setup, the initial information creates a logical or social violation, while the punchline provide a secondary interpretation that "explains" the discrepancy, thereby rendering it benign.19 Sarcasm functions similarly; the literal meaning of the words violates a conversational norm, but an exaggerated tone of voice provides a "meta-norm" that signals the speaker's true, playful intent.19

### **Weak Commitment to the Violated Norm**

Humor is highly dependent on the level of commitment an individual has to the norm being violated.1 If a person holds a weak commitment to a norm, they can recognize the violation without feeling personally threatened or offended.3 For example, studies show that men often find sexist jokes more amusing than women because they tend to have a lower normative commitment to the protection of female identity in that specific context.3 Conversely, individuals with a strong commitment to a particular moral or political viewpoint will find jokes mocking that viewpoint to be offensive rather than funny.18 This subjectivity confirms that humor is not a property of the stimulus but an outcome of the perceiver's internal appraisal system.16

### **Psychological Distance as the Primary modulatory Lever**

Of all the mechanisms for controlling benignness, psychological distance is established as the most versatile and powerful lever for generative systems.14 Psychological distance refers to the subjective experience that an event or object is removed from the self, the present, and the immediate reality.14 Follow-up research by McGraw et al. (2012, 2014\) categorized distance into four distinct varieties:

| Dimension of Distance | Mechanism of Safety | Implementation Strategy |
| :---- | :---- | :---- |
| Temporal | Distance in time. | Frame the violation as a historical event or a distant future possibility. 14 |
| Spatial | Distance in space. | Locate the violation in a geographically remote area ("a tragedy on Mars"). 14 |
| Social | Distance in relationships. | Attribute the mishap to a stranger or an out-group rather than the self or friends. 5 |
| Hypothetical | Distance from reality. | Use "what if" framing or clearly "fictional" characters/avatars. 14 |

The most significant finding in the distance literature is the interaction between distance and violation severity.14 Severe violations, such as major tragedies or disturbing images, require significant psychological distance to reach the "sweet spot" of humor.14 Without this buffer, the event is too threatening to be perceived as benign.21 In contrast, mild mishaps require psychological closeness to remain humorous; if a stubbed toe or a small error is too distant, it becomes uninteresting and fails to register as a violation at all.14

## **Mood State Routing and Regulatory Focus**

The effectiveness of a humor beat is inextricably linked to the audience's active motivational state, which can be defined through Regulatory Focus Theory.30 This theory distinguishes between two primary systems for regulating behavior: the Prevention Frame and the Promotion Frame.31 Mapping these frames to the BVT allows the agent to select the appropriate distance mechanism for the current context \[Query\].

### **The Prevention Frame: Safety and Vigilance**

Individuals in a prevention frame are focused on security, responsibility, and the avoidance of losses.30 They are highly vigilant and sensitive to potential threats.31 For this audience, any norm violation is likely to be viewed through a lens of risk.31 To successfully integrate humor for a prevention-focused audience, the generative agent must provide excessive psychological distance \[Query\]. The violation should be clearly hypothetical or historical, and the benignness must be strongly reinforced by the agent’s "Voice DNA"—natural warmth and high credibility signals that reassure the audience the interaction remains safe \[Query\].

### **The Promotion Frame: Growth and Achievement**

Individuals in a promotion frame are motivated by growth, aspirations, and the attainment of gains.30 They exhibit an eager strategy and possess a much higher tolerance for risk and ambiguity.31 In this state, audiences are more likely to perceive a violation as an "identity opportunity" or a playful challenge rather than an attack.33 Consequently, promotion-frame audiences can tolerate closer violations, such as direct teasing or present-tense mishaps \[Query\].

### **Regulatory Fit and Processing Fluency**

Humor research indicates that "fit" between the humor style and the audience's regulatory focus enhances engagement and persuasiveness.36 This is mediated by processing fluency—the ease with which information is absorbed.36

* **Incongruity Humor and Prevention Focus:** Lighthearted, low-threat humor that relies on safe juxtapositions pairs best with prevention-focused messaging.36 This combination induces greater social proximity and trust.36  
* **Aggressive Humor and Promotion Focus:** Disparaging humor or "roasting" can be effective for promotion-focused audiences because it signals status and high-level wit.36 However, even in this frame, the agent must ensure the violation is perceived as benign to avoid suspecting "ulterior motives".37

## **Social Power and Mismatched Humor Sweet Spots**

The relationship between social distance, power, and the humor "sweet spot" is a critical consideration for any system representing an authority figure or coach.5 Social power is a primary determinant of social distance; high-power individuals naturally feel more distant from others and are prone to thinking more abstractly.5

### **The Asymmetry of Perceived Distance**

According to the Social Distance Theory of Power (SDTP), power creates a mismatch in how individuals perceive their closeness to one another.5 A low-power individual (e.g., a student or follower) often feels socially close to a high-power individual (e.g., an instructor or leader), while the high-power individual feels distant from the subordinate.15 This asymmetry leads to "empathic inaccuracy," where high-power joke-tellers fail to accurately judge the feelings of their audience.5

### **Impropriety Thresholds and Disputed "No-Man's-Land"**

Because power increases distance, it also raises the "impropriety threshold"—the level of violation required before a joke becomes offensive.5

1. **High-Power Tellers:** May perceive an edgy joke as a "benign violation" because their distance makes the threat feel abstract and safe.5  
2. **Low-Power Listeners:** Because they feel less distance, they may perceive that same joke as a "malign violation," leading to perceptions of bullying or harassment.5

This discrepancy creates a "disputed no-man's-land" in social interactions, where the intent of the teller and the perception of the listener are fundamentally misaligned.15 To mitigate this risk, the generative architecture specifies that benignness should be supplied by "Voice DNA"—the agent's consistent signals of warmth and credibility—which act as a cross-power safety signal that can bridge the distance gap.17

## **The 18 Studies: Evidence of Empirical Robustness**

The Benign Violation Theory is distinguished from other humor models by its extensive empirical validation across 18 studies \[Query\]. These experiments tested the theory's predictions across multiple domains, including moral psychology, tragedy, and social interaction.1

### **Key Experimental Findings from McGraw & Warren (2010)**

The initial five experimental studies focused on the domain of moral psychology to demonstrate that even behaviors considered "wrong" can be funny if they are benign.1

| Study | Focus | Key Result |
| :---- | :---- | :---- |
| Study 1 | Moral vs. Control Scenarios | Participants were significantly more likely to judge "violation" versions (e.g., snorting a father's ashes) as wrong (69% vs. 2%) yet laugh at them (44% vs. 5%) compared to control versions. 2 |
| Study 2 | Subjective Appraisals | Confirmed that humorous violations are perceived as being "wrong" and "not wrong" simultaneously. 1 |
| Study 3 | Mixed Emotions | Showed that benign moral violations elicit a combination of amusement and disgust, whereas malign violations elicit only negative emotion. 2 |
| Study 5 | Distance Manipulation | Using a coordinate plane plotting task to manipulate distance, the study showed that participants in the "far" condition were significantly more amused by violations (73%) than those in the "near" condition (39%). 2 |

### **Longitudinal Evidence: The Hurricane Sandy Study**

In a 2014 longitudinal study, McGraw et al. examined reactions to jokes about Hurricane Sandy over 100 days.14 This research challenged the belief that time monotonically increases humor. Instead, it revealed a "comedic sweet spot" in temporal distance 14:

* **The Rise:** Initially, the tragedy was too threatening for humor to occur (too close).  
* **The Peak:** Humor peaked approximately 36 days after landfall, when the event was distant enough to be benign but close enough to remain a significant violation.  
* **The Fall:** After 100 days, the event became "too far" to care about, becoming purely benign and therefore uninteresting/boring. 14

## **Cross-Cultural Consistency and Universal Patterns**

While specific cultural norms dictate what constitutes a violation, the structural requirement of a "benign breach" is a universal human trait.27 Research across 24 diverse societies showed that people can accurately identify the social relationship between laughers (friends vs. strangers) about 60% of the time, suggesting that laughter's function as a "safety signal" is globally understood.17

### **Replications in Non-Western Contexts**

Studies in Indonesia aimed to replicate the original BVT experiments using culturally specific stimuli, such as parody videos mocking internet content.40 The findings confirmed that perceived violation levels positively predicted amusement.40 However, the research also noted that Indonesians are highly reactive to jokes targeting disadvantaged groups or minorities, illustrating that if a violation is perceived as a threat to "harmony in the community," it cannot be rendered benign for that population.40

### **Interdependent vs. Independent Self-Construal**

The perception of social distance varies between independent cultures (Western) and interdependent cultures (Eastern).25

* **Interdependent Audiences:** Feel a stronger closeness and commitment to their in-groups. They are less likely to find humor in violations involving "close others" because the threat is felt more acutely.25 For these audiences, social distance is a required benignness mechanism for jokes involving identity.25  
* **Independent Audiences:** Show a weaker effect of social distance on humor appreciation, as their identity is less tied to a collective normative structure.25

## **Computational Implementation: The Violation-Benignness Matrix**

The practical output of integrating BVT into a generative architecture is the Violation-Benignness Matrix \[Query\]. This matrix operationalizes the three-variable precision of the theory into a structured field that specifies the target violation and the required modulatory levers \[Query\].

### **Architecture of the Humor Skill Guide**

The generative process is driven by the interaction between the system's internal data fields and the real-time context of the audience.6

1. **Selection of Violation (Variable 1):** The system identifies a "Negative Space" entry from DEP-ENG-004. This ensures the audience recognizes the violation because the system already knows what they care about \[Query\].  
2. **Modulation of Benignness (Variable 2):** The system assesses the active "Regulatory Frame" (Prevention vs. Promotion).  
   * If **Prevention**, it applies high distance (hypothetical/historical) and signals high warmth through "Voice DNA" \[Query\].  
   * If **Promotion**, it applies low distance (direct/first-person) and utilizes high wit or shared knowledge \[Query\].  
3. **Synthesizing the Beat (Variable 3):** The agent compiles the beat to ensure the violation and the safety signal register at the same cognitive moment, avoiding a sequence that leads to mere relief.9

### **Deterministic Reasoning vs. Generic Instructions**

The transition from a instruction like "create edgy but harmless humor" to a deterministic specification is the key architectural advantage of BVT \[Query\]. A generic instruction relies on the agent's internal "intuition," which often results in literal descriptions or non-humorous incongruities.6 The Violation-Benignness Matrix allows for a falsifiable reasoning chain:

| Step | Computational Reasoning | Source Identifier |
| :---- | :---- | :---- |
| Semantic Parsing | Identify visual or conversational cues for potential triggers. | 6 |
| Threat Appraisal | Map trigger to Negative Space (DEP-ENG-004). Is this a recognizable violation? | 6 |
| Benignness Selection | Assess mood state routing. Does this audience need distance or fit? | 14 |
| Distance Lever | Apply temporal, spatial, or hypothetical framing based on mood. | 14 |
| Safety Signaling | Layer Voice DNA (warmth/credibility) over the message. | \[Query\] |
| Discriminator | Evaluate: Is the violation too severe (offense) or too benign (boredom)? | 3 |

## **Second and Third-Order Social and Affective Implications**

The integration of humor into autonomous coaching and communication systems has ripple effects that extend into the affective states of the users and the normative climate of the environment.

### **Affective Benefits: Coping and Stress Reduction**

Humor is a powerful tool for emotion regulation.22 By successfully creating a benign violation, the agent allows the user to reframe a threatening situation as "okay," which significantly reduces levels of stress hormones such as cortisol and epinephrine.22 In high-stress contexts like health interventions or service failures, humor acts as a buffer that prevents the user from entering a state of defensive arousal, thereby maintaining openness to information and future engagement.22

### **Social Implications: Norm Acceptability and Deviance**

A subtle consequence of using humor in an authority role (such as a coach or leader) is the signaling of "norm violation acceptability".48 When an agent humorously violates a norm, it communicates that the boundary is not absolute, which can have both positive and negative outcomes.48

* **Positive Ripple Effect:** Fosters a "culture of fun" that attracts talent, increases task performance, and encourages creativity and "bootleg innovation".48  
* **Negative Ripple Effect:** May inadvertently sanction inappropriate behaviors, leading to increased follower deviance if the humor is perceived as a dismissal of essential responsibilities.49

### **Ethical Boundaries: The Risk of Malign Conversions**

The most critical failure state for a humor-enabled agent is the "malign conversion," where the intended benignness fails to register.15 This is particularly dangerous in online communication, where lack of facial cues makes the "safety signal" harder to communicate.26 Generative systems must be programmed with absolute boundaries regarding "Hate Speech," as certain severe violations (e.g., dehumanization) are so close to the audience's fundamental identity threats that they can almost never be rendered benign.13 The "Humor Mindset"—a cognitive state triggered by humor cues that allows recipients to interpret aggressive messages as playful—can be used maliciously to mask hateful intent, necessitating a robust "Discriminator" in the generative architecture to evaluate the ethical weight of the chosen violation.6

## **Synthesis and Conclusion: The Structural Superiority of BVT**

The Benign Violation Theory provides the most empirically validated and unified theoretical anchor in the humor literature, making it the non-negotiable foundation for sophisticated computational humor.1 Its structural clarity allows it to be integrated into an existing architecture through the relationship between Variable 1 (DEP-ENG-004 Negative Space) and Variable 2 (Voice DNA and psychological distance) \[Query\].

By transforming humor from a creative mystery into a deterministic specification, BVT enables generative agents to execute humor beats that are safe, fit-for-purpose, and contextually aware.6 The modulatory role of psychological distance, governed by the interaction between violation severity and recipient distance, ensures that the agent can land the joke in the "sweet spot"—far enough away to be safe, but close enough to matter.14 As systems increasingly utilize mood state routing to identify Prevention and Promotion frames, the deployment of humor will become a strategic tool for enhancing well-being, fostering bonding, and navigating complex social landscapes with human-level nuance.6

#### **Sources des citations**

1. Benign violations: making immoral behavior funny \- PubMed, consulté le mars 12, 2026, [https://pubmed.ncbi.nlm.nih.gov/20587696/](https://pubmed.ncbi.nlm.nih.gov/20587696/)  
2. (PDF) Benign Violations Making Immoral Behavior Funny \- ResearchGate, consulté le mars 12, 2026, [https://www.researchgate.net/publication/44851692\_Benign\_Violations\_Making\_Immoral\_Behavior\_Funny](https://www.researchgate.net/publication/44851692_Benign_Violations_Making_Immoral_Behavior_Funny)  
3. Benign Violation Theory \- Humor Research Lab (HuRL), consulté le mars 12, 2026, [https://humorresearchlab.com/benign-violation-theory/](https://humorresearchlab.com/benign-violation-theory/)  
4. A brief introduction to the benign violation theory of humor \- Peter McGraw, consulté le mars 12, 2026, [https://petermcgraw.org/a-brief-introduction-to-the-benign-violation-theory-of-humor/](https://petermcgraw.org/a-brief-introduction-to-the-benign-violation-theory-of-humor/)  
5. You Must Be Joking\! Benign Violations, Power Asymmetry, and Humor in a Broader Social Context \- Frontiers, consulté le mars 12, 2026, [https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2019.01380/full](https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2019.01380/full)  
6. HUMORCHAIN: Theory-Guided Multi-Stage Reasoning for Interpretable Multimodal Humor Generation \- arXiv.org, consulté le mars 12, 2026, [https://arxiv.org/pdf/2511.21732](https://arxiv.org/pdf/2511.21732)  
7. Benign Violation Theory \- Caleb Warren, A. Peter McGraw \- Google Books, consulté le mars 12, 2026, [https://books.google.com/books/about/Benign\_Violation\_Theory.html?id=JJ3pzwEACAAJ](https://books.google.com/books/about/Benign_Violation_Theory.html?id=JJ3pzwEACAAJ)  
8. Painfully Funny: Cringe Comedy, Benign Masochism, and Not-So-Benign Violations \- Tidsskrift.dk, consulté le mars 12, 2026, [https://tidsskrift.dk/lev/article/download/104693/153596/0](https://tidsskrift.dk/lev/article/download/104693/153596/0)  
9. 1 What makes things funny? Evidence for the benign-violation theory of humour \- UCT, consulté le mars 12, 2026, [https://humanities.uct.ac.za/media/251707](https://humanities.uct.ac.za/media/251707)  
10. Journal of Personality and Social Psychology \- University of Colorado Boulder, consulté le mars 12, 2026, [https://leeds-faculty.colorado.edu/mcgrawp/pdf/warren.mcgraw.2016.pdf](https://leeds-faculty.colorado.edu/mcgrawp/pdf/warren.mcgraw.2016.pdf)  
11. Benign Violation Theory, consulté le mars 12, 2026, [https://leeds-faculty.colorado.edu/mcgrawp/pdf/Benign\_Violation\_Theory.html](https://leeds-faculty.colorado.edu/mcgrawp/pdf/Benign_Violation_Theory.html)  
12. Benign Violations: Making Immoral Behavior Funny \- University of Colorado Boulder, consulté le mars 12, 2026, [https://leeds-faculty.colorado.edu/mcgrawp/pdf/mcgraw.warren.2010.pdf](https://leeds-faculty.colorado.edu/mcgrawp/pdf/mcgraw.warren.2010.pdf)  
13. That's disgusting\! …, But very amusing: Mixed feelings of amusement and disgust | Request PDF \- ResearchGate, consulté le mars 12, 2026, [https://www.researchgate.net/publication/247497153\_That's\_disgusting\_But\_very\_amusing\_Mixed\_feelings\_of\_amusement\_and\_disgust](https://www.researchgate.net/publication/247497153_That's_disgusting_But_very_amusing_Mixed_feelings_of_amusement_and_disgust)  
14. Social Psychological and Personality Science \- University of ..., consulté le mars 12, 2026, [https://leeds-faculty.colorado.edu/mcgrawp/pdf/mcgraw.williams.warren.2014b.pdf](https://leeds-faculty.colorado.edu/mcgrawp/pdf/mcgraw.williams.warren.2014b.pdf)  
15. You Must Be Joking\! Benign Violations, Power Asymmetry, and Humor in a Broader Social Context \- PMC, consulté le mars 12, 2026, [https://pmc.ncbi.nlm.nih.gov/articles/PMC6593112/](https://pmc.ncbi.nlm.nih.gov/articles/PMC6593112/)  
16. Humorous Complaining, consulté le mars 12, 2026, [https://marketing-business.media.uconn.edu/wp-content/uploads/sites/724/2020/07/Kan-Humorous-Complaining-JCR.pdf](https://marketing-business.media.uconn.edu/wp-content/uploads/sites/724/2020/07/Kan-Humorous-Complaining-JCR.pdf)  
17. The Science of Humor Is No Laughing Matter, consulté le mars 12, 2026, [https://www.psychologicalscience.org/observer/the-science-of-humor-is-no-laughing-matter](https://www.psychologicalscience.org/observer/the-science-of-humor-is-no-laughing-matter)  
18. What Is The BENIGN VIOLATION THEORY Of Humour? \- Jonathan Sandling, consulté le mars 12, 2026, [https://jonathansandling.com/what-is-the-benign-violation-theory-of-humour/](https://jonathansandling.com/what-is-the-benign-violation-theory-of-humour/)  
19. Benign Violation Theory, consulté le mars 12, 2026, [https://leeds-faculty.colorado.edu/mcgrawp/pdf/mcgraw.warren.2014.pdf](https://leeds-faculty.colorado.edu/mcgrawp/pdf/mcgraw.warren.2014.pdf)  
20. When Does Humorous Marketing Hurt Brands? \- We Are Social, consulté le mars 12, 2026, [https://wearesocial.com/uk/wp-content/uploads/sites/2/2021/09/warren.mcgraw.2016a.pdf](https://wearesocial.com/uk/wp-content/uploads/sites/2/2021/09/warren.mcgraw.2016a.pdf)  
21. Psychological Distance, consulté le mars 12, 2026, [https://leeds-faculty.colorado.edu/mcgrawp/pdf/mcgraw.williams.warren.2014a.pdf](https://leeds-faculty.colorado.edu/mcgrawp/pdf/mcgraw.williams.warren.2014a.pdf)  
22. Awfully Funny – Association for Psychological Science \- APS, consulté le mars 12, 2026, [https://www.psychologicalscience.org/observer/awfully-funny](https://www.psychologicalscience.org/observer/awfully-funny)  
23. Too Soon? Too Late? Psychological Distance Matters When It Comes to Humor, consulté le mars 12, 2026, [https://www.psychologicalscience.org/news/releases/too-soon-too-late-psychological-distance-matters-when-it-comes-to-humor.html](https://www.psychologicalscience.org/news/releases/too-soon-too-late-psychological-distance-matters-when-it-comes-to-humor.html)  
24. The Cross-Cultural Dynamics of Humor and the Benign Violation Theory: An Application to Travel Literature \- ResearchGate, consulté le mars 12, 2026, [https://www.researchgate.net/publication/366254521\_The\_Cross-Cultural\_Dynamics\_of\_Humor\_and\_the\_Benign\_Violation\_Theory\_An\_Application\_to\_Travel\_Literature](https://www.researchgate.net/publication/366254521_The_Cross-Cultural_Dynamics_of_Humor_and_the_Benign_Violation_Theory_An_Application_to_Travel_Literature)  
25. The Impact of Culture and Social Distance on Humor Appreciation, Sharing, and Production, consulté le mars 12, 2026, [https://pmc.ncbi.nlm.nih.gov/articles/PMC9893297/](https://pmc.ncbi.nlm.nih.gov/articles/PMC9893297/)  
26. Full article: The Thin Line Between Harmful and Benign: Perceptions of Humorous and Non-Humorous Hate Speech in Humorous and Neutral Social Media Contexts \- Taylor & Francis, consulté le mars 12, 2026, [https://www.tandfonline.com/doi/full/10.1080/15213269.2025.2580291](https://www.tandfonline.com/doi/full/10.1080/15213269.2025.2580291)  
27. Play-mirth theory: a cognitive appraisal theory of humor \- Frontiers, consulté le mars 12, 2026, [https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2024.1473742/full](https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2024.1473742/full)  
28. (PDF) Too Close for Comfort, or Too Far to Care? Finding Humor in Distant Tragedies and Close Mishaps \- ResearchGate, consulté le mars 12, 2026, [https://www.researchgate.net/publication/230786382\_Too\_Close\_for\_Comfort\_or\_Too\_Far\_to\_Care\_Finding\_Humor\_in\_Distant\_Tragedies\_and\_Close\_Mishaps](https://www.researchgate.net/publication/230786382_Too_Close_for_Comfort_or_Too_Far_to_Care_Finding_Humor_in_Distant_Tragedies_and_Close_Mishaps)  
29. The effects of psychological distance on spontaneous justice inferences: A construal level theory perspective \- PMC, consulté le mars 12, 2026, [https://pmc.ncbi.nlm.nih.gov/articles/PMC9752061/](https://pmc.ncbi.nlm.nih.gov/articles/PMC9752061/)  
30. Promotion, Prevention or Both: Regulatory Focus and Culture Revisited \- ScholarWorks@GVSU, consulté le mars 12, 2026, [https://scholarworks.gvsu.edu/cgi/viewcontent.cgi?article=1109\&context=orpc](https://scholarworks.gvsu.edu/cgi/viewcontent.cgi?article=1109&context=orpc)  
31. Exploring Regulatory Focus Theory and the Hedonic Principle \- Psychology Fanatic, consulté le mars 12, 2026, [https://psychologyfanatic.com/regulatory-focus-theory/](https://psychologyfanatic.com/regulatory-focus-theory/)  
32. Regulatory Focus Theory, consulté le mars 12, 2026, [https://www.communicationtheory.org/regulatory-focus-theory/](https://www.communicationtheory.org/regulatory-focus-theory/)  
33. “I Identify with Her,” “I Identify with Him”: Unpacking the Dynamics of Personal Identification in Organizations \- AOM Journals, consulté le mars 12, 2026, [https://journals.aom.org/doi/10.5465/amr.2014.0033](https://journals.aom.org/doi/10.5465/amr.2014.0033)  
34. Consumer Psychology of Individuals (Chapter 1\) \- Cambridge University Press & Assessment, consulté le mars 12, 2026, [https://www.cambridge.org/core/books/cambridge-handbook-of-consumer-psychology/consumer-psychology-of-individuals/B90879A24E9AEA750E7A047971FED1D1](https://www.cambridge.org/core/books/cambridge-handbook-of-consumer-psychology/consumer-psychology-of-individuals/B90879A24E9AEA750E7A047971FED1D1)  
35. Exploring the effect of humor in robot failure \- ResearchGate, consulté le mars 12, 2026, [https://www.researchgate.net/publication/361014104\_Exploring\_the\_effect\_of\_humor\_in\_robot\_failure](https://www.researchgate.net/publication/361014104_Exploring_the_effect_of_humor_in_robot_failure)  
36. Engaging Audience on Social Media: The Persuasive Impact of Fit Between Humor and Regulatory Focus in Health Messages | Request PDF \- ResearchGate, consulté le mars 12, 2026, [https://www.researchgate.net/publication/371224982\_Engaging\_Audience\_on\_Social\_Media\_The\_Persuasive\_Impact\_of\_Fit\_Between\_Humor\_and\_Regulatory\_Focus\_in\_Health\_Messages](https://www.researchgate.net/publication/371224982_Engaging_Audience_on_Social_Media_The_Persuasive_Impact_of_Fit_Between_Humor_and_Regulatory_Focus_in_Health_Messages)  
37. Humor and Violence | Request PDF \- ResearchGate, consulté le mars 12, 2026, [https://www.researchgate.net/publication/373600617\_Humor\_and\_Violence](https://www.researchgate.net/publication/373600617_Humor_and_Violence)  
38. The Rise and Fall of Humor: Psychological Distance Modulates ..., consulté le mars 12, 2026, [https://experts.arizona.edu/en/publications/the-rise-and-fall-of-humor-psychological-distance-modulates-humor/](https://experts.arizona.edu/en/publications/the-rise-and-fall-of-humor-psychological-distance-modulates-humor/)  
39. The Rise and Fall of Humor | Request PDF \- ResearchGate, consulté le mars 12, 2026, [https://www.researchgate.net/publication/270673470\_The\_Rise\_and\_Fall\_of\_Humor](https://www.researchgate.net/publication/270673470_The_Rise_and_Fall_of_Humor)  
40. Norms Violation and Dark Personality: Benign Violation Theory for Humor and Dark Humor \- ScholarWorks@GVSU, consulté le mars 12, 2026, [https://scholarworks.gvsu.edu/cgi/viewcontent.cgi?article=1328\&context=iaccp\_papers](https://scholarworks.gvsu.edu/cgi/viewcontent.cgi?article=1328&context=iaccp_papers)  
41. The Impact of Culture and Social Distance on Humor Appreciation, Sharing, and Production \- ScienceOpen, consulté le mars 12, 2026, [https://www.scienceopen.com/document\_file/01e11475-4e25-4e23-9bc1-247afb349079/PubMedCentral/01e11475-4e25-4e23-9bc1-247afb349079.pdf](https://www.scienceopen.com/document_file/01e11475-4e25-4e23-9bc1-247afb349079/PubMedCentral/01e11475-4e25-4e23-9bc1-247afb349079.pdf)  
42. Humour in trolley problems and other sacrificial dilemmas: killing is not funny at all | Request PDF \- ResearchGate, consulté le mars 12, 2026, [https://www.researchgate.net/publication/385754516\_Humour\_in\_trolley\_problems\_and\_other\_sacrificial\_dilemmas\_killing\_is\_not\_funny\_at\_all](https://www.researchgate.net/publication/385754516_Humour_in_trolley_problems_and_other_sacrificial_dilemmas_killing_is_not_funny_at_all)  
43. Who's Laughing Now? An Overview of Computational Humour Generation and Explanation, consulté le mars 12, 2026, [https://arxiv.org/html/2509.21175v1](https://arxiv.org/html/2509.21175v1)  
44. First They Scream, Then They Laugh: The Cognitive Intersections of Humor and Fear \- PMC, consulté le mars 12, 2026, [https://pmc.ncbi.nlm.nih.gov/articles/PMC11155347/](https://pmc.ncbi.nlm.nih.gov/articles/PMC11155347/)  
45. Developing a social functional account of laughter | Request PDF \- ResearchGate, consulté le mars 12, 2026, [https://www.researchgate.net/publication/324118078\_Developing\_a\_social\_functional\_account\_of\_laughter](https://www.researchgate.net/publication/324118078_Developing_a_social_functional_account_of_laughter)  
46. laughter therapy: Topics by Science.gov, consulté le mars 12, 2026, [https://www.science.gov/topicpages/l/laughter+therapy](https://www.science.gov/topicpages/l/laughter+therapy)  
47. Mixing emotions: The use of humor in fear advertising | Request PDF \- ResearchGate, consulté le mars 12, 2026, [https://www.researchgate.net/publication/264341030\_Mixing\_emotions\_The\_use\_of\_humor\_in\_fear\_advertising](https://www.researchgate.net/publication/264341030_Mixing_emotions_The_use_of_humor_in_fear_advertising)  
48. Linking Leader's Positive Humor and Employee Bootlegging: Empirical Evidence from China \- PMC, consulté le mars 12, 2026, [https://pmc.ncbi.nlm.nih.gov/articles/PMC10122859/](https://pmc.ncbi.nlm.nih.gov/articles/PMC10122859/)  
49. Benign Violations: Making Immoral Behavior Funny | Request PDF \- ResearchGate, consulté le mars 12, 2026, [https://www.researchgate.net/publication/315488336\_Benign\_Violations\_Making\_Immoral\_Behavior\_Funny](https://www.researchgate.net/publication/315488336_Benign_Violations_Making_Immoral_Behavior_Funny)  
50. A distinct look at a transcendental phenomenon: the grounded theory model of leader humour \- PMC, consulté le mars 12, 2026, [https://pmc.ncbi.nlm.nih.gov/articles/PMC11917014/](https://pmc.ncbi.nlm.nih.gov/articles/PMC11917014/)  
51. The relationship between humorous leadership and innovative behavior | Request PDF, consulté le mars 12, 2026, [https://www.researchgate.net/publication/283299743\_The\_relationship\_between\_humorous\_leadership\_and\_innovative\_behavior](https://www.researchgate.net/publication/283299743_The_relationship_between_humorous_leadership_and_innovative_behavior)  
52. When workplace humour turns into conflict: exploring HR practices in the case of conflict management | Employee Relations | Emerald Publishing, consulté le mars 12, 2026, [https://www.emerald.com/er/article/45/5/1275/45796/When-workplace-humour-turns-into-conflict](https://www.emerald.com/er/article/45/5/1275/45796/When-workplace-humour-turns-into-conflict)  
53. construal level theory: Topics by Science.gov, consulté le mars 12, 2026, [https://www.science.gov/topicpages/c/construal+level+theory.html](https://www.science.gov/topicpages/c/construal+level+theory.html)