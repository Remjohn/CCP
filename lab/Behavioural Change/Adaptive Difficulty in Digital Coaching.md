# **Adaptive Difficulty Scaling and Flow Optimization in Digital Coaching Systems**

The landscape of digital health and behavioral intervention has undergone a fundamental shift toward precision engagement. As non-communicable diseases (NCDs) continue to account for approximately 74% of global mortality, the integration of lifestyle medicine into scalable digital platforms has become a public health imperative.1 Central to the efficacy of these platforms is the ability to maintain user adherence, a challenge that has historically seen drop-off rates exceeding 80% within the first week of intervention.2 Modern digital coaching systems are increasingly leveraging AI-driven adaptive difficulty scaling to navigate the complex psychological terrain between user boredom and cognitive overwhelm. By synthesizing the principles of flow theory, behavioral design models, and real-time computational inference, these systems aim to create a "Goldilocks Zone" of engagement that fosters long-term habit formation while minimizing behavioral fatigue.

## **Theoretical Foundations of Dynamic Engagement**

The success of adaptive coaching rests upon three pillars of psychological theory: Mihaly Csikszentmihalyi’s Flow Theory, BJ Fogg’s Behavior Model, and Katy Milkman’s research on temporal landmarks and temptation bundling. Together, these frameworks provide the necessary roadmap for how an AI system should calibrate challenges to match the evolving capabilities of a user.

### **Flow Theory: The Architecture of Optimal Experience**

Flow theory, or "optimal experience theory," posits that individuals reach a state of peak engagement when they are fully absorbed in an activity that provides a clear set of goals and immediate feedback.3 In this state, the distinction between self and activity disappears, and time is often perceived as distorted.4 For a digital coach, inducing flow is the primary mechanism for preventing disengagement. The experience is governed by the balance between the challenge presented and the skills possessed by the individual.5

| Dimension of Flow | Description of Phenomenon | Application in Digital Coaching |
| :---- | :---- | :---- |
| Challenge-Skills Balance | Equality between task demand and user ability | Real-time difficulty adjustment based on performance 6 |
| Action-Awareness Merging | Total absorption in the present task | Minimizing UI clutter and extraneous notifications 6 |
| Clear Goals | Unambiguous purpose for every action | Well-defined behavioral milestones and daily quests 6 |
| Immediate Feedback | Constant, direct responses to user input | Real-time biometric alerts and progress visualization 4 |
| Sense of Control | Absolute mastery over performance | Allowing user-led adjustments (Adaptable Mode) 6 |
| Loss of Self-Consciousness | Suspension of ego and external social monitoring | Low-stakes, non-judgmental AI interactions 6 |
| Transformation of Time | Distortion of time perception (flying or slowing) | Immersive gamification and scenic environments 4 |
| Autotelic Experience | The activity is its own reward | Transitioning from extrinsic rewards to intrinsic motivation 4 |

The "Flow Matrix" illustrates that when challenges exceed skills, the user enters a state of anxiety; when skills exceed challenges, boredom ensues.5 Continuous exposure to the anxiety state leads to burnout, while chronic boredom leads to disengagement.5 Consequently, an adaptive system must function as a dynamic regulator, constantly shifting the task complexity to ensure the user stays within the flow channel. The very experience of flow acts as an incentive for growth, encouraging individuals to take on greater challenges as their skills improve.4

### **The Fogg Behavior Model and the Mechanics of Simplicity**

While flow theory provides the goal of the interaction, the Fogg Behavior Model (FBM) provides the mechanics of the behavioral act. Fogg asserts that behavior (B) occurs when Motivation (M), Ability (A), and a Prompt (P) converge: ![][image1].11 In many digital coaching contexts, motivation is volatile. Therefore, the most reliable lever for an AI system is "Ability," which Fogg reframes as "Simplicity".11

A behavior is more likely to be performed if it is made easy to do.11 Adaptive systems leverage this by implementing "micro-flows"—breaking down complex therapeutic or lifestyle goals into manageable steps.12 For example, instead of a static goal of "exercise for 30 minutes," an adaptive system might prompt a user to "do one push-up" or "walk for 5 minutes" during periods where the system infers low cognitive energy or high stress.12 This reduction in difficulty serves as a "failure safety net," ensuring the habit loop remains intact even when the user's resources are depleted.12

### **Temporal Landmarks and Motivation Scheduling**

Katy Milkman’s research on "Temporal Landmarks" and the "Fresh Start Effect" offers a temporal framework for difficulty adjustment. Humans perceive time as divided into mental accounting periods bounded by salient dates (e.g., Mondays, birthdays, New Year’s Day).14 These landmarks allow individuals to distance themselves from past imperfections and embrace an aspirational "future self".14

AI coaching systems can optimize the timing of challenge increases by aligning them with these landmarks. Experimental data shows that Google searches for health-related terms and gym visits spike following these dates.15 Furthermore, "temptation bundling"—pairing an instantly rewarding "want" (e.g., watching a favorite show) with a goal-aligned "should" (e.g., using a stationary bike)—can be suggested by the AI to overcome present-bias and inertia.16

## **Thresholds for Boredom and Cognitive Overwhelm**

A critical challenge in difficulty scaling is the identification of the specific thresholds at which a user moves from an optimal flow state into a maladaptive state of boredom or overwhelm. These thresholds are not static; they are mediated by individual neurobiology and cognitive load.

### **The MAC Model: Attentional Resources and Meaning**

The Meaning and Attentional Components (MAC) model redefines boredom as a multifaceted state rather than simple understimulation.19 Boredom occurs when there is a failure to engage attention in a meaningful way, which can happen even in highly stimulating environments if the individual lacks the cognitive resources to process the information.19

| Boredom Profile | Attention Levels | Activity Meaning | Predicted Behavior |
| :---- | :---- | :---- | :---- |
| Understimulation | High resources | Low meaning | Switching to "interesting" (eudaimonic) tasks 19 |
| Overstimulation/Overwhelm | Low resources | High meaning | Switching to "enjoyable" (hedonic) tasks 19 |
| Disengaged | Low resources | Low meaning | Withdrawal and dropout 19 |

This model suggests that if an AI coach detects a user has high cognitive resources but low engagement (understimulation), it should increase task complexity to foster eudaimonic experiences such as mastery and appreciation.19 Conversely, if the user is overwhelmed by the complexity (high demand but low available attention), the system should offer hedonic repair—simplifying the task to provide fun and relaxation, thereby preventing the emotional distress associated with "painful" boredom.19

### **Neurobiological Variance and the ADHD Boredom Threshold**

Individuals with Attention Deficit/Hyperactivity Disorder (ADHD) possess a significantly higher "boredom threshold" due to chronic dopamine dysregulation in the brain’s reward system.20 For neurotypical individuals, moderate levels of stimulation are sufficient to avoid boredom. However, for those with ADHD, standard activities may feel understimulating, leading to intense restlessness and an impulsive urge to escape the situation.20

Digital coaching systems for this population must provide a higher "dose" of stimulation, frequent novelty, and immediate feedback loops.20 Without these micro-adjustments, the ADHD user is likely to experience "trait boredom," a persistent tendency toward disengagement regardless of the environment.20

### **Digital Fatigue and the Infodemic Stressor**

The pervasive integration of technology has introduced "digital burnout" or "online fatigue," characterized by physical and emotional exhaustion from prolonged digital tool usage.23 This is exacerbated by "infodemic stress"—the burden of distinguishing between high volumes of information and falsehoods, which creates a cognitive load that impairs health behavioral decisions.24

| Indicator of Digital Fatigue | Mechanism of Impact | Behavioral Symptom |
| :---- | :---- | :---- |
| Reaction Time Latency | Slowed information processing due to exhaustion | Delayed response to coaching prompts 25 |
| Accuracy Decay | Disruption of prefrontal cortex/thalamic pathways | Repetitive mistakes in simple tasks 25 |
| Emotional Exhaustion | Depletion of self-regulatory resources | Increased irritability or "scroll stress" 23 |
| Cognitive Dissonance | Conflict between digital demands and personal goals | Detachment and perceived inability to finish 23 |

## **Metrics for Inferring User Capability in Adaptive Systems**

To stay within the "Goldilocks Zone," an AI system must translate physiological and behavioral data into an accurate inference of user capability. This involves a spectrum of metrics ranging from simple performance tracking to sophisticated biometric sensing.

### **Performance and Biometric Metrics**

Dynamic Difficulty Adjustment (DDA) primarily utilizes observable gameplay metrics, such as win-loss ratios, reaction times, and remaining health, to recalibrate challenges.28 If a player succeeds consistently, the system increases difficulty by enhancing AI behavior or spawn rates; if the player struggles, the system offers assistance.28

More advanced "emotion-based" DDA systems use affective computing to capture real-time emotional responses.28 Heart Rate Variability (HRV) and Skin Conductance (GSR) are used to infer stress levels, while Brainwaves (EEG) can detect levels of mental focus.28 Hybrid systems combine these channels: for instance, if a user performs well (high metrics) but shows high physiological stress, the system might maintain the challenge level rather than increasing it, preventing the user from tipping into overwhelm.28

### **Item Response Theory and the Zone of Proximal Development**

In educational and cognitive coaching, systems often employ the Rasch Model of Item Response Theory (IRT).29 This psychometric framework estimates a learner’s latent ability (![][image2]) and the difficulty of an item (![][image3]). The probability (![][image4]) of a correct response is modeled as:

![][image5]  
The system identifies the "Zone of Proximal Development" (ZPD) as the optimal difficulty band where learning is maximized.29 Research suggests that targeting a difficulty level where the user has an approximately 38% error rate (![][image6]) maximizes "information gain" and keeps the user in a state of productive struggle.29

### **Computational Optimization: Reinforcement Learning and GFPO**

Real-time adaptation is often achieved through reinforcement learning (RL) algorithms like Bayesian Multi-Armed Bandits (MAB).1 Algorithms such as Thompson Sampling balance exploration (trying new challenges) with exploitation (providing the most effective challenge level).1

Furthermore, techniques like Adaptive Difficulty GFPO (Group-Relative Policy Optimization) have been developed to address "length inflation" in AI-generated coaching outputs. This technique dynamically adjusts the group size of candidate responses based on real-time difficulty estimation—allocating more computational resources to complex prompts while aggressive filtering ensures conciseness for simple tasks.30 This ensures that the user is not bombarded with verbose, overwhelming content for straightforward behaviors.

## **Experimental Evidence: Static vs. Adaptive Design**

The core hypothesis of adaptive difficulty scaling is that personalized, dynamic interventions lead to better outcomes than "one-size-fits-all" static designs. Evidence across physical activity, education, and workplace productivity supports this transition.

### **Physical Activity and Goal Setting**

The "WalkIT Arizona" study compared static and adaptive goal-setting for moderate-to-vigorous physical activity (MVPA).31 Participants with a static 30-minute daily goal were compared to those with an adaptive goal based on their MVPA over the previous 9 days. Results indicated that adaptive goals significantly increased MVPA, particularly when combined with immediate reinforcement.31 In contrast, static goals often failed to account for context, leading to higher rates of disengagement during high-stress periods.32

| Feature | Static Intervention | Adaptive Intervention |
| :---- | :---- | :---- |
| Goal Structure | Fixed (e.g., 30 mins/day) | Dynamic (based on recent history) 32 |
| Reinforcement | Delayed/Interval | Immediate/Contingent 31 |
| Completion Rate | 45-65% (30-day challenges) | 70-85% (Micro-challenges) 13 |
| Long-term Adherence | High initial dropout | Sustained behavior change for finishers 13 |

### **E-Learning and Assessment**

Adaptive testing frameworks have demonstrated a substantial improvement in student engagement compared to traditional static assessments.34 Static systems are prone to "test fatigue," where students lose interest as they progress. Adaptive systems, by contrast, modify questions in real-time, resulting in a 30-40% reduction in test duration while achieving more accurate ability estimates.34 Qualitative data from platforms like "Moalemy" (an Arabic educational chatbot) indicate that adaptive assessments strengthen perceptions of competence and task usefulness, leading to a 97.2% satisfaction rate.35

### **Workplace Productivity and AI Synergy**

Studies on human-AI collaboration demonstrate that adaptive systems can significantly enhance performance metrics. For example, AI-augmented customer service agents saw a 14% improvement in resolution rates and a 9% reduction in handle times, with the strongest benefits observed for the least-experienced workers.37 This "scaffolding" effect allows lower-skilled individuals to perform at a higher level by reducing the cognitive labor of knowledge retrieval.37

## **The Moderating Role of Perceived Autonomy**

A significant finding in recent experimental studies is that "perceived autonomy" often moderates the effectiveness of adaptive difficulty. There is a delicate balance between a system that helps and a system that controls.

### **Adaptive vs. Adaptable Paradigms**

Research identifies three personalization paradigms based on the locus of control:

1. **Adaptive (System-driven):** The system takes complete control over content difficulty and sequencing.9  
2. **Adaptable (User-driven):** The user is given tools to choose their own difficulty level and navigation.9  
3. **Mixed (Collaborative):** Control is shared between the user and the system.36

| Metric | Static Mode | Adaptive Mode | Adaptable Mode | Mixed Mode |
| :---- | :---- | :---- | :---- | :---- |
| Engagement Median | Low | 0.56 | 0.67 (Highest) | 0.61 9 |
| Usability (SUS) | Moderate | Lowest | Highest (at low difficulty) | High 9 |
| Autonomy Support | None | Perceived as rigid | High 9 | Perceived as supportive |

Experimental results from chatbot studies show that the **adaptable** approach consistently achieves the highest engagement scores.9 This suggests that users prefer having a choice over their difficulty level, even if the system's automated choice might be more "accurate" from a purely psychometric standpoint.36 Giving users the "permission to commit" and the sense that "their decision matters" enhances self-efficacy and belief in the plan.39

### **The Danger of Substitution vs. Scaffolding**

If an AI coach becomes too controlling, it risks the "erosion of introspection" and "outsourcing of resilience".38 When a system dictates exactly what a user should feel or do at every moment (e.g., "you are stressed, take three breaths"), the individual may lose the opportunity to develop independent coping strategies.38 This creates a dependency on the technology, potentially leaving the user ill-equipped to handle stress in contexts where the AI is absent.38

To mitigate this, design principles must prioritize **scaffolding**—temporary support that fades as the user’s internal capacity grows—over **substitution**, which permanently assumes responsibility for regulation.38

## **Impact of Micro-Adjustments on Long-Term Adherence**

The granular nature of AI-driven interventions—often referred to as "Just-in-Time Adaptive Interventions" (JITAIs)—allows for micro-adjustments that maintain engagement beyond the initial novelty phase.2

### **Combating Novelty Decay**

The "novelty decay" phenomenon is a primary reason for the 80% first-week drop-off in health apps.2 JITAIs address this by tailoring support to contextual signals like mood, location, and time.2 For instance, a system might provide a "praise" message if a user meets a goal without a prompt, or a "nudge" if the user’s activity levels dip.1 These micro-reinforcements keep the content "fresh" and relevant to the user’s changing internal and external states.2

### **Desirable Friction and the Buy-In Effect**

Counter-intuitively, some research suggests that adding initial friction—rather than reducing it—can improve long-term follow-through.40 The "Buy-In Effect" occurs when users who endure a more effortful sign-up process (e.g., a 15-question domain-relevant survey) demonstrate 1.6 times more follow-through behavior over four months compared to those with a "one-click" sign-up.40 This "initial investment" enhances the perceived value of the behavior and signals personal motivation to the "present self".40 Adaptive difficulty systems can use this principle by occasionally introducing "productive struggle" or "intentional friction" (e.g., Socratic questioning) to ensure the user is actively processing the intervention rather than passively clicking through prompts.29

### **Long-Term Completion Rates by Duration**

| Duration Format | Typical Completion Rate | Impact on Habit Formation |
| :---- | :---- | :---- |
| 5-Minute Challenge | 70-85% | High entry, low intensity 13 |
| 30-Day Challenge | 45-65% | "Sweet spot" for many users 13 |
| 90-Day Challenge | 25-40% | High impact for finishers; highest burnout risk 13 |

While shorter challenges have higher completion rates, longer challenges (e.g., 90 days) align more closely with the 18 to 254-day timeline required for sustainable habit formation.13 Adaptive systems can bridge this gap by starting with low-barrier micro-habits and gradually increasing duration and intensity as the user's "behavioral immunity" strengthens.12

## **Evidence-Based Principles for Difficulty Calibration**

The synthesis of behavioral science and AI deployment research yields several evidence-based principles for implementing real-time difficulty calibration in digital coaching.

### **1\. Target the ZPD with Desirable Friction**

Systems should utilize psychometric modeling (like IRT) to identify the user's latent ability and target tasks within the Zone of Proximal Development.29 The target difficulty should aim for an approximate 38% error rate to maximize information gain and prevent the disengagement associated with trivial tasks.29 Furthermore, the introduction of "intentional friction"—such as asking a user to rate their confidence before answering—can prevent automation bias and promote metacognitive calibration.29

### **2\. Prioritize Adaptable over Adaptive Modes**

To maintain high engagement and user agency, systems should favor "adaptable" or "mixed" control modes over fully automated "adaptive" ones.9 Allowing users to choose their own challenge level or providing "flexible streaks" (e.g., 3-of-7 days) creates an "autonomous student-athlete climate" that fosters resilience and self-determined motivation.9

### **3\. Implement Multi-Tiered Scaffolding**

Coaching interventions should adjust the nature of support based on recent performance streaks 29:

* **Challenge Mode:** For high-ability users with consecutive successes, introduce atypical scenarios or "clinical noise" to prevent plateauing.29  
* **Minimal Scaffolding:** For users in the flow zone, use Socratic hints to encourage independent problem-solving.29  
* **Full Scaffolding:** For users experiencing consecutive failures, provide direct instruction or simplify the task to a "micro-flow" to prevent emotional distress and dropout.12

### **4\. Detect and Mitigate Behavioral Fatigue Biometrically**

Systems should monitor for the physiological and behavioral markers of digital fatigue, such as reaction time latency and heart rate variability.25 When fatigue is detected, the AI coach should preemptively lower the difficulty or suggest a "fresh start" rather than pushing for optimization, which could paradoxically heighten stress and anxiety.38

### **5\. Transition from Linear to Compounding Progress**

To turn behavior into identity, the system should ensure that today's successes make tomorrow easier.12 This "compounding value" can be achieved through:

* **Autofilling** past entries based on history.12  
* **Passive Resurfacing** of learned content (e.g., language apps resurfacing words).12  
* **Contextual Triggers** like geolocation nudges that prompt behaviors exactly when they are most convenient.12

## **Future Outlook and Ethical Governance**

The emergence of Large Language Models (LLMs) and advanced affective computing offers unprecedented potential for deep personalization in digital coaching.11 However, these technologies also amplify the "Engagement-Efficacy-Ethics Trilemma".11 Algorithmic personalization can lead to "extreme tailoring" that improves efficacy but reduces ethics by masking the logic behind interventions—creating a "black box" that undermines user transparency.11

The future of digital coaching lies in "Hybrid Intelligence," where the AI provides the computational scaffolding for personalization while preserving human agency and social connection.10 Studies suggest that while AI peers are more reliable for consistent support, human peers evoke a stronger "social presence" and "accountability".10 Consequently, the next generation of coaching systems should aim to fulfill the user’s basic psychological needs for competence, autonomy, and **relatedness** simultaneously.2

In conclusion, dynamic difficulty scaling is the technical bridge between a user's initial intention and their long-term habit formation. By meticulously calibrating the "sweet spot" of challenge, identifying the neurobiological markers of fatigue, and respecting the user's need for autonomy, AI-driven coaching environments can transform digital health from a series of fleeting interactions into a sustainable infrastructure for human resilience. The objective remains a system that is "safe enough to fail" but "challenging enough to grow," ensuring that the path of least resistance eventually leads to the highest level of mastery.12

#### **Works cited**

1. Designing digital health interventions with causal ... \- Frontiers, accessed April 1, 2026, [https://www.frontiersin.org/journals/digital-health/articles/10.3389/fdgth.2025.1435917/full](https://www.frontiersin.org/journals/digital-health/articles/10.3389/fdgth.2025.1435917/full)  
2. Achieving clinically meaningful outcomes in digital health ... \- Frontiers, accessed April 1, 2026, [https://www.frontiersin.org/journals/digital-health/articles/10.3389/fdgth.2025.1713334/full](https://www.frontiersin.org/journals/digital-health/articles/10.3389/fdgth.2025.1713334/full)  
3. Flow Theory \- TheoryHub \- Academic theories reviews for research and T\&L, accessed April 1, 2026, [https://open.ncl.ac.uk/academic-theories/8/flow-theory/](https://open.ncl.ac.uk/academic-theories/8/flow-theory/)  
4. Flow conditions – Csikszentmihalyi's summary \- Leadership & Flow, accessed April 1, 2026, [https://flowleadership.org/flow-conditions-csikszentmihalyis-summary/](https://flowleadership.org/flow-conditions-csikszentmihalyis-summary/)  
5. Flow Theory: Unlocking the Secrets of Happiness at Work \- Planyway, accessed April 1, 2026, [https://planyway.com/blog/mihaly-csikszentmihalyi-flow-theory](https://planyway.com/blog/mihaly-csikszentmihalyi-flow-theory)  
6. 9 Dimensions of Flow \- Flow Centre, accessed April 1, 2026, [https://www.flowcentre.org/9-dimensions-to-flow](https://www.flowcentre.org/9-dimensions-to-flow)  
7. A Taxonomy of Motivational Affordances for Meaningful Gamified and Persuasive Technologies \- ETH Zurich Research Collection, accessed April 1, 2026, [https://www.research-collection.ethz.ch/server/api/core/bitstreams/d6e96e07-d6b5-400d-a1e9-8525a0ff5ca3/content](https://www.research-collection.ethz.ch/server/api/core/bitstreams/d6e96e07-d6b5-400d-a1e9-8525a0ff5ca3/content)  
8. Design of an AI-driven home-based pulmonary telerehabilitation system to enhance patient engagement \- PMC, accessed April 1, 2026, [https://pmc.ncbi.nlm.nih.gov/articles/PMC12602929/](https://pmc.ncbi.nlm.nih.gov/articles/PMC12602929/)  
9. Exploring Adaptive, Adaptable, Mixed, and Static Arabic Rule-Based ..., accessed April 1, 2026, [https://www.mdpi.com/2076-3417/15/24/13266](https://www.mdpi.com/2076-3417/15/24/13266)  
10. When Workout Buddies Are Virtual: AI Agents and Human Peers in a Longitudinal Physical Activity Study \- arXiv, accessed April 1, 2026, [https://arxiv.org/html/2602.01918v1](https://arxiv.org/html/2602.01918v1)  
11. Gamification in Digital Mental Health Interventions: A Systematic ..., accessed April 1, 2026, [https://www.mdpi.com/2078-2489/17/2/168](https://www.mdpi.com/2078-2489/17/2/168)  
12. What Designers Get Wrong About Habit Loops and How to Fix It | by Khushi Mehta \- Medium, accessed April 1, 2026, [https://medium.com/design-bootcamp/what-designers-get-wrong-about-habit-loops-and-how-to-fix-it-6fd47be714d2](https://medium.com/design-bootcamp/what-designers-get-wrong-about-habit-loops-and-how-to-fix-it-6fd47be714d2)  
13. 90-Day vs 30-Day Fitness Challenge Apps: Which Format Works Best? \- BenFit, accessed April 1, 2026, [https://benfit.co.uk/90-day-vs-30-day-fitness-challenge-apps/](https://benfit.co.uk/90-day-vs-30-day-fitness-challenge-apps/)  
14. Temporal Landmarks \- ModelThinkers, accessed April 1, 2026, [https://modelthinkers.com/mental-model/temporal-landmarks](https://modelthinkers.com/mental-model/temporal-landmarks)  
15. The Fresh Start Effect: Temporal Landmarks Motivate Aspirational Behavior \- PubsOnLine, accessed April 1, 2026, [https://pubsonline.informs.org/doi/10.1287/mnsc.2014.1901](https://pubsonline.informs.org/doi/10.1287/mnsc.2014.1901)  
16. The Mel Robbins Podcast: Episode Summaries, Insights, and Commentary \- Shortform, accessed April 1, 2026, [https://www.shortform.com/podcast/the-mel-robbins-podcast](https://www.shortform.com/podcast/the-mel-robbins-podcast)  
17. Why You Keep Falling Off Track; Tools That Help You Start Again with Katy Milkman, accessed April 1, 2026, [https://www.oneyoufeed.net/why-you-keep-falling-off-track/](https://www.oneyoufeed.net/why-you-keep-falling-off-track/)  
18. How to Overcome Procrastination | AIU \- American InterContinental University, accessed April 1, 2026, [https://www.aiuniv.edu/blog/2012/october/four-tips-for-breaking-through-procrastination](https://www.aiuniv.edu/blog/2012/october/four-tips-for-breaking-through-procrastination)  
19. Bored gamers: applying the Meaning and Attentional ... \- Frontiers, accessed April 1, 2026, [https://www.frontiersin.org/journals/communication/articles/10.3389/fcomm.2025.1578313/full](https://www.frontiersin.org/journals/communication/articles/10.3389/fcomm.2025.1578313/full)  
20. ADHD vs Boredom: How to Tell the Difference? | AMFM Mental Health Treatment, accessed April 1, 2026, [https://amfmtreatment.com/blog/adhd-vs-boredom-how-to-tell-the-difference/](https://amfmtreatment.com/blog/adhd-vs-boredom-how-to-tell-the-difference/)  
21. People are increasingly bored in our digital age \- PMC \- NIH, accessed April 1, 2026, [https://pmc.ncbi.nlm.nih.gov/articles/PMC11532334/](https://pmc.ncbi.nlm.nih.gov/articles/PMC11532334/)  
22. Connected by Boredom: A Systematic Review of the Role of Trait Boredom in Problematic Technology Use \- MDPI, accessed April 1, 2026, [https://www.mdpi.com/2076-3425/15/8/794](https://www.mdpi.com/2076-3425/15/8/794)  
23. Development and validation of a digital burnout scale in artificial intelligence era \- PMC, accessed April 1, 2026, [https://pmc.ncbi.nlm.nih.gov/articles/PMC12836882/](https://pmc.ncbi.nlm.nih.gov/articles/PMC12836882/)  
24. Unraveling the impact of infodemic stress on information and health behaviors: a double effect perspective \- Emerald Publishing, accessed April 1, 2026, [https://www.emerald.com/intr/article/doi/10.1108/INTR-12-2023-1137/1257089/Unraveling-the-impact-of-infodemic-stress-on?searchresult=1](https://www.emerald.com/intr/article/doi/10.1108/INTR-12-2023-1137/1257089/Unraveling-the-impact-of-infodemic-stress-on?searchresult=1)  
25. Examining the Landscape of Cognitive Fatigue Detection: A Comprehensive Survey \- MDPI, accessed April 1, 2026, [https://www.mdpi.com/2227-7080/12/3/38](https://www.mdpi.com/2227-7080/12/3/38)  
26. Healthcare Worker Fatigue Detection Using Wearable Sensors Preventing Medical Errors Through Biometric Alertness Monitoring \- The Review of Diabetic Studies, accessed April 1, 2026, [https://diabeticstudies.org/index.php/RDS/article/view/1759/1571](https://diabeticstudies.org/index.php/RDS/article/view/1759/1571)  
27. (PDF) Scroll, Stress, and Strain: A Model of Psychological Vulnerability in the Age of Social Media \- ResearchGate, accessed April 1, 2026, [https://www.researchgate.net/publication/395804085\_Scroll\_Stress\_and\_Strain\_A\_Model\_of\_Psychological\_Vulnerability\_in\_the\_Age\_of\_Social\_Media](https://www.researchgate.net/publication/395804085_Scroll_Stress_and_Strain_A_Model_of_Psychological_Vulnerability_in_the_Age_of_Social_Media)  
28. Dynamic Difficulty Adjustment in Games: Concepts, Techniques, and ..., accessed April 1, 2026, [https://www.intechopen.com/chapters/1228576](https://www.intechopen.com/chapters/1228576)  
29. Onco-Shikshak: An AI-Native Adaptive Learning Ecosystem for Medical Oncology Education, accessed April 1, 2026, [https://www.medrxiv.org/content/10.64898/2026.02.23.26346944v1.full-text](https://www.medrxiv.org/content/10.64898/2026.02.23.26346944v1.full-text)  
30. Adaptive Difficulty GFPO \- Emergent Mind, accessed April 1, 2026, [https://www.emergentmind.com/topics/adaptive-difficulty-gfpo](https://www.emergentmind.com/topics/adaptive-difficulty-gfpo)  
31. Variable Magnitude and Frequency Financial Reinforcement is Effective at Increasing Adults' Free-Living Physical Activity \- PMC, accessed April 1, 2026, [https://pmc.ncbi.nlm.nih.gov/articles/PMC7490290/](https://pmc.ncbi.nlm.nih.gov/articles/PMC7490290/)  
32. Rationale, Design, and Baseline Characteristics of WalkIT Arizona: A Factorial Randomized Trial Testing Adaptive Goals and Financial Reinforcement to Increase Walking across Higher and Lower Walkable Neighborhoods \- PMC, accessed April 1, 2026, [https://pmc.ncbi.nlm.nih.gov/articles/PMC6544173/](https://pmc.ncbi.nlm.nih.gov/articles/PMC6544173/)  
33. The Impact of Monetary Incentives on Delay Discounting Within a Year-Long Physical Activity Intervention \- PMC, accessed April 1, 2026, [https://pmc.ncbi.nlm.nih.gov/articles/PMC11008587/](https://pmc.ncbi.nlm.nih.gov/articles/PMC11008587/)  
34. Python-driven adaptive testing algorithms for personalized assessment in e-learning platforms \- SOAR, accessed April 1, 2026, [https://soar.wichita.edu/bitstreams/17993768-e380-4bcb-89ba-c1e62d70eb2a/download](https://soar.wichita.edu/bitstreams/17993768-e380-4bcb-89ba-c1e62d70eb2a/download)  
35. Adaptive Assessment in Digital Learning Environments: An Expectancy-Value Theory Approach to Enhancing Learner Motivation \- ERIC, accessed April 1, 2026, [https://files.eric.ed.gov/fulltext/EJ1486417.pdf](https://files.eric.ed.gov/fulltext/EJ1486417.pdf)  
36. (PDF) Exploring Adaptive, Adaptable, Mixed, and Static Arabic Rule-Based Chatbot Effects on Usability, Learning Success, and Engagement \- ResearchGate, accessed April 1, 2026, [https://www.researchgate.net/publication/398831126\_Exploring\_Adaptive\_Adaptable\_Mixed\_and\_Static\_Arabic\_Rule-Based\_Chatbot\_Effects\_on\_Usability\_Learning\_Success\_and\_Engagement](https://www.researchgate.net/publication/398831126_Exploring_Adaptive_Adaptable_Mixed_and_Static_Arabic_Rule-Based_Chatbot_Effects_on_Usability_Learning_Success_and_Engagement)  
37. Quantifying and Optimizing Human-AI Synergy: Evidence-Based Strategies for Adaptive Collaboration, accessed April 1, 2026, [https://www.innovativehumancapital.com/article/quantifying-and-optimizing-human-ai-synergy-evidence-based-strategies-for-adaptive-collaboration](https://www.innovativehumancapital.com/article/quantifying-and-optimizing-human-ai-synergy-evidence-based-strategies-for-adaptive-collaboration)  
38. Cognitive offloading or cognitive overload? How AI alters ... \- Frontiers, accessed April 1, 2026, [https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2025.1699320/full](https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2025.1699320/full)  
39. Clinical Rehabilitation Science Medicine Journal \- Gexin Publications, accessed April 1, 2026, [https://gexinonline.com/archive/journal-of-rehabilitation-practices-and-research/JRPR-168](https://gexinonline.com/archive/journal-of-rehabilitation-practices-and-research/JRPR-168)  
40. The Buy-In Effect: When Increasing Initial Effort Motivates Behavioral Follow-Through, accessed April 1, 2026, [https://www.hbs.edu/ris/Publication%20Files/24-020\_75c501e7-cb64-4532-a929-6778594bad05.pdf](https://www.hbs.edu/ris/Publication%20Files/24-020_75c501e7-cb64-4532-a929-6778594bad05.pdf)  
41. The Transformative Power of 6 Months: Benefits of Changing Your Life \- Medium, accessed April 1, 2026, [https://medium.com/@averageguymedianow/the-transformative-power-of-6-months-benefits-of-changing-your-life-11d40fe8f14d](https://medium.com/@averageguymedianow/the-transformative-power-of-6-months-benefits-of-changing-your-life-11d40fe8f14d)  
42. Examining Student Athletes' Perceptions Of Autonomy Support In Coaching And Learning Climates \- Sycamore Scholars, accessed April 1, 2026, [https://scholars.indianastate.edu/cgi/viewcontent.cgi?article=2935\&context=etds](https://scholars.indianastate.edu/cgi/viewcontent.cgi?article=2935&context=etds)  
43. (PDF) Gamification in Digital Mental Health Interventions: A Systematic Review of the Engagement–Efficacy–Ethics Trilemma \- ResearchGate, accessed April 1, 2026, [https://www.researchgate.net/publication/400553920\_Gamification\_in\_Digital\_Mental\_Health\_Interventions\_A\_Systematic\_Review\_of\_the\_Engagement-Efficacy-Ethics\_Trilemma](https://www.researchgate.net/publication/400553920_Gamification_in_Digital_Mental_Health_Interventions_A_Systematic_Review_of_the_Engagement-Efficacy-Ethics_Trilemma)  
44. The Influence of the Coach's Autonomy Support and Controlling Behaviours on Motivation and Sport Commitment of Youth Soccer Players \- PMC, accessed April 1, 2026, [https://pmc.ncbi.nlm.nih.gov/articles/PMC8394926/](https://pmc.ncbi.nlm.nih.gov/articles/PMC8394926/)  
45. The Double Win \- Transistor, accessed April 1, 2026, [https://feeds.transistor.fm/the-double-win-a602ba7a-b838-4bd2-91e5-5215cbb0a6a8](https://feeds.transistor.fm/the-double-win-a602ba7a-b838-4bd2-91e5-5215cbb0a6a8)

[image1]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAFwAAAAYCAYAAAB3JpoiAAADdUlEQVR4Xu2XS8hNURTHlzyivIlEkUjeSQbETMmA5BEihSRKoSQmyiMRefQVSclAJkoGUhJflAEGDEhKHnmUkgiFPNavtZd7zr733Hu+8n13YP/rl8/d+5yzz3+vvdY6IklJSf+3+ihd4x//lZYpp+pwUBnzd3bzlF3nAWVAfjgnzNoi+ffYpnTPTirQKOWhMjUeCOIe3Cv2KctapbdfECsZnle7G95XmRP4quxShgSGKXuUH8qiQLPk63yvfJJiQ9AC5bnyWBkf4PpG6qKcUH4r86IxVyexzV4lNm+DVPyaHLisPFGGh2uqtDCAsTOjMW70QmkN9MwOdrBYY4vyRYoNIUj2Kg+UM2IGQRnNUp5JfcNd+8Q2f2w8oJomFrzMqanjgafK4GhsgvJBOR8gCpql3WLR+0rZGo0hjN0stjGcghX54UIRRHBSWSK2odtzM/IirRDFt5Re0RiaL7ZpNQ3nQa2BC5I3lFxITnqpTAw0S6zziDJaLMfWehlOJ2kPozGtXtrJivmwXuyaRoZzith0gjQrP02cQoJ0Sn7YxJHgaMA5ZXGAxH9VrEAVFoCMMMRzWVnK5FUX6zwk9pxrYmvNpgtauZ1KD+W0clfpF8bqCfOIbPB3IIWezU6KNFv5JXaSXJ2V5YGP0VhOhP+3AHnLzSCSSCE3lRE+uY4wxDerLDOkfH5lnevC35jRKpVUgNaIFSxMxmzP3/XE+A6x3A3IDfcNrSU2FsPvSCU73FMOB7hHoTx318rfQ8WqPfmKvFWmrWovkb89RfDCvl6gC2EzMAjTy+Zv7ndDrOUEgmC18lqKGwTP32VPUJWS4R1oOBWWSkuxjAsm8uNJkRoYaIZ4cfpjfz5mUnO87yUt+IdQ2YJJQ9AiVquyaW6lWP9eZOhI5a1YnWizvGBSkWtVZfIauf2oNO5nKRZ0M22B09WNixuIdR6TyvPnKp+V/YHp4XfGyd1FZmW1VOxrtJaoEeTxWrnYC2aZE1QlLvKPnfiDZ5LYsb2u9I/GOlpE3cbM/711IxA8GFDZgsnn+0WpTqEuDC/6qKEdJWVxskqLXSLCvos16G8CHnnvwr+bxNqsZol1shbW+FO5JNaiEnlXxFo64DcM9LlE/31lnOQ1SLktdi/mkb+zwYSJjzLj3I+2GB/ou8HH8IuxpKSkpKSkpKSkpDL6A7OU8Lwo8sroAAAAAElFTkSuQmCC>

[image2]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAZCAYAAAAIcL+IAAAA1UlEQVR4Xu3QPwtBYRQG8CMGQgZKymRQZmUyCVksMigWk49gMvoC4gMwGWTyp2QQiw9gNRhks9k9597nva7trspTv7rveZ9O3VfkN1OCHWwp+30tUqAlxKBBY/CZUkTsLarGWZ0OvLfSggslODPFG6R0EIAFjMikTyeI6sBzMQMPmFAOqnCkNQS1WIaXfDY0oQt3GmpJ04YrJEmThyfpIiu6ZQ9h0vTgTPqmznBqDkgINtAhJ0WYif33qgIrsR/ZeWiN56Ie5jAg/U67C+74IU76/Y+VN8lFLQ4B93z0AAAAAElFTkSuQmCC>

[image3]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAwAAAAZCAYAAAAFbs/PAAAA+klEQVR4Xt3Sr4pCURAG8BERlFU2mASLYhEWDFabSRBZ0LJVg80gqLBFQSymDUYNPoFNuytYfQB9iX0Cv9n7XZ2DoHvDFj/4hTv3nPtn5og8b15gCivYUsVZYRKBAeR4naYdZPxFNg14N9cpOkDR1CVGY3g19RLtIWnqkqc2b5ShABuqX5d6CbyhaizhB44wJ22Gk0/Kmpr+05pqpi5xGJHOwEbfprTVl+hTO2STgG/q2hs6xR7ZvMGJnBlMYEYh1vQnF9Anv/6bQBui4m0Y0he0xOv9B4TpEj1YtgPaMR2c8wk2ek5upngvTfGOwJ+jvXa+8VECb/jfnAGzRislvkimoAAAAABJRU5ErkJggg==>

[image4]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA8AAAAYCAYAAAAlBadpAAAA0klEQVR4XmNgGPKAA4hLoXgWFtwFxcZAzAjVAwcUaQYJCENxFRC/B2JbIJaE4nAofgfEZVD1WMEcID4NxILoEkCwEIjvArE4ugQvFB8G4vkMqKZzQ/EeBhyaNaH4LRCno8npQDHIOxMYsDjbD4q/ALEpkjgfEC+F4u1AzI8kBwetUPwLiI8B8QEGiBeOAHEUFHPCFCMDmH9AeCsDJOqIBhRpVgLi51AMimeSgAsDxK8gDGKTBEC2wWwGuYIoEATET4D4LxD/h+JnQJyMrGgUDGkAAMY3M1QIiPX1AAAAAElFTkSuQmCC>

[image5]: <data:image/png;base64,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>

[image6]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGAAAAAXCAYAAAD0v0pBAAADVElEQVR4Xu2YW6hNQRjHPx1KIYTjWooiuXTkVhIePPDAg0spwoukHAkRRSIhKZejhEISIfLgksSOF1KKkBe1eaA88KRI4f9vvmnPmr3W2mu2vdc5af3q127PnrXXzHwz881aIgUFBQVdim7qMngL3oAX4RC3Us7w3ufVh/AY7OH8nge94Sw4GrZ4vyUxUKrbyWuHiRnjKli4SWUAbKWd8LitlDMj4TM4Q+0Or8LlbqUmYSfjKvgEroAH4E3Y16mXxAX4B36CH9WfcJskBGAy3K26FbaL+bO84ezhYB+VymAQtiV0QuyArX5hDcarb+AELWMbOqTSpjTOwS9iBv6eOltSrisCECXXALBwr5gb2ZsRLvnrcINTlhfz4Vc4xSmz7QmdEPvgUL+wBpx49Dns75Svg+/hYKcsjhMSbXsqTBhsJJMNnQunw5XwtmTb8xoJB/oyLIlpj4Xt5Iw865RlITQAnJCX1JJE27AQfpfag2sD0BP2UxOZBtfCXeo3+AGW4cxKtUT45+xgVt0OxTEKfoZ3xKxITgbaLqbzmytVMxEaALav5OgHgMl1gVMWxyF4V8xEuqY+gmPcShZmeh6zfBbDp1J7BfCEsjTAieayRNi533C/RK87BX9JfFvTaEYA+JnGGqmevOzPa/HyEZf7YYnf09jRtxLW+EbAvZcrgCuB2CTMxMYtiFuRD1fhQfW05ysx24lf3iHxM7IRAYjDXrvILWRnOEMYCB+efbMknEbDAPDs3Ue/D1fL+lsooSvgX3PAILgHTvLKbQAifeAsj+uUTYQ0LjguzBv2YSOLW81libA9Jal0nIcB+lLCj5MkNADEnoL8Fcf8UxYzIZKwA+0fl2NXAI9VfLrzH5uXiOkwn0bzhkfQ+2ICwPu/UOe5lQKoJwBM/vSdfhL7HEDteX6L+gPO0bKx8CTspd/tFsrEHMkBnNlHxDSQR7vV6hV4RjrvHRAHnu+h2K4HYpJyrVNHGvUEwA4aB/exmC1no5j3USOcejYAfGbhw6yFE9u+NuGRlHI1tTl1Ivs/z6vc66m/GjqDFol/oVUP9QTAhWPC7WOcZH8ZRwaIuW6qWtWXIgDZaFoAmIDX+4X/IdyTqzrfFUh6ACvICZ6zQ5ZUQUFBQYP4CwMJufAOGAuIAAAAAElFTkSuQmCC>