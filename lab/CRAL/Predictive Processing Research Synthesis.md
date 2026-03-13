# **The Predictive Processing Framework and Active Inference: A Unified Theory of Brain Function, Attention, and Strategic Communication**

The scientific understanding of the human brain is currently undergoing a paradigm shift, moving away from a traditional reactive model toward a proactive, predictive model. Historically, the brain was viewed as a passive recipient of sensory information—a stimulus-response organ that processes input in a bottom-up fashion to build a representation of the world.1 In this older view, perception begins at the sensory periphery and moves upward, gradually becoming more complex until a coherent image is formed. However, contemporary neurocognitive research, championed by Karl Friston and Andy Clark, posits a radical alternative: the brain is a prediction machine.3 This framework, known as predictive processing or hierarchical predictive coding, suggests that the brain’s fundamental goal is to match incoming sensory signals with internally generated top-down expectations. In this paradigm, perception, attention, and learning are all facets of a single imperative: the minimization of prediction error, which is the discrepancy between what the brain expects and what it actually senses.6

The implications of this shift extend far beyond neuroscience, offering a transformative lens for strategic communication and research design. By understanding the brain as an active inference engine, practitioners can move away from traditional models of filling knowledge gaps and toward a more effective strategy of targeting audience prediction profiles. This report provides an exhaustive analysis of the predictive processing framework, its neurological implementation, and its profound implications for belief updating and information processing.

## **The Free-Energy Principle and the Biological Imperative for Prediction**

At the deepest theoretical level, the predictive brain is grounded in the free-energy principle, a mathematical formulation of how biological systems maintain their integrity and resist a natural tendency toward disorder or entropy.9 All living organisms, from single cells to complex brains, must occupy a limited repertoire of states compatible with their physiological needs—a process known as homeostasis or allostasis.9 Mathematically, maintaining a low-entropy state is equivalent to minimizing surprisal, which is the negative log-probability of an outcome. Because a biological agent cannot directly calculate surprise on sampling data, it instead minimizes variational free energy, which serves as an information-theoretic bound on surprise.9

The brain achieves free-energy minimization through two primary channels: perception and action.9 Perception involves changing internal states (the brain’s beliefs) to better fit incoming sensory data, thereby optimizing predictions. Action, or active inference, involves changing the sensory input itself by moving the body to sample the environment in ways that fulfill internal expectations.1 For example, "feeling our way in darkness" involves anticipating a touch and then acting to confirm that expectation, thereby minimizing the prediction error that would result if the touch were unexpected.9

| Concept | Information-Theoretic Definition | Physiological Realization |
| :---- | :---- | :---- |
| **Surprisal** | **![][image1]** | Discrepancy between sensory input and generative model predictions.12 |
| **Free Energy** | **![][image2]** | Upper bound on surprise derived from internal states and sensory signals.9 |
| **Entropy** | Average surprise of outcomes | Measure of uncertainty; biological systems must keep this low to survive.9 |
| **Homeostasis** | Regulation of internal environment | Maintenance of states within physiological bounds.9 |
| **Allostasis** | Achieving stability through change | Anticipatory regulation based on predicted energy needs.1 |

The free-energy principle serves as a grand unified theory, connecting biological self-organization with the Bayesian brain hypothesis.12 It suggests that all aspects of brain function—perception, memory, and inference—are geared toward the same optimization goal: reducing information-theoretic free energy.4 This is not merely a metaphor but a principle of least action based on variational physics, establishing that any system resisting disorder must, in some abstract sense, perform action and perception to model its environment.11

## **Operational Architecture: Hierarchical Predictive Coding**

The neural implementation of prediction error minimization occurs within a hierarchical architecture that mirrors the organization of the mammalian cortex.4 In this bidirectional cascade, information flows in two primary directions. Higher-order cortical areas house generative models that generate predictions about the activity of lower-level areas.21 These predictions are sent downward via feedback or backward connections.22 Simultaneously, lower-level areas compare their actual activity with these top-down predictions. If a match occurs, the signal is silenced or "explained away".4 Only the residual discrepancies—the prediction errors—are propagated upward via feedforward connections to update the internal models at the next level.4

## **The Rao-Ballard Model and Receptive Field Effects**

A foundational demonstration of this architecture was provided by Rao and Ballard (1999) in their study of the visual cortex.21 They argued that visual neurons do not simply encode bottom-up features but act as residual error detectors.22 Their model explained extra-classical receptive field effects, such as endstopping, as the result of top-down predictions.21 In this phenomenon, a neuron in the primary visual cortex (V1) reduces its firing rate when a stimulus extends beyond its classical receptive field into the surrounding area.21 According to predictive coding, this happens because the higher level (V2), which has a larger receptive field, "sees" the extended stimulus and accurately predicts its continuation into the V1 field, thereby suppressing the V1 error signal.22

| Cortical Layer | Functional Identity | Signal Content | Connection Type |
| :---- | :---- | :---- | :---- |
| **Superficial (II, III)** | Error-detecting neurons | Discrepancy between prediction and input | Feedforward (Upward) 22 |
| **Layer IV** | Input destination | Afferent thalamic or lower-level input | Recipient of "news" 2 |
| **Deep (V, VI)** | Representation/Estimate units | Probabilistic generative model predictions | Feedback (Downward) 1 |
| **Various** | Precision units | Synaptic gain and reliability weighting | Modulatory 1 |

This architecture enables the brain to optimize bandwidth by transmitting only "news"—the unpredicted portion of the signal.4 If the top-down model is accurate, the lower level remains relatively quiet. This provides a functional explanation for why predictable stimuli evoke smaller BOLD responses in neuroimaging studies.26 The brain is essentially a hypothesis-testing machine, deriving a virtual version of the sensory data from high-level knowledge and only adjusting that fantasy when the actual input proves it wrong.4

## **Dynamics of Belief Updating**

Belief formation and updating under this framework are inherently Bayesian. The brain maintains a joint probability density over hidden causes and their consequences.9 When prediction errors arise, they act as the "teaching signal" that allows the generative model to adapt.20 This process, referred to as "analysis-by-synthesis," requires that internal models track the causal matrix responsible for the statistical structure of observed inputs.12 As an individual moves up the representational hierarchy, the spatial and temporal scope of these models increases, ranging from fast, fine-grained details at the lowest levels to slow, abstract regularities at the highest levels.22

## **Attention as a Mechanism of Precision-Weighting**

A central claim of Proposal 5 is that attention is not a spotlight directed at interesting stimuli but a mechanism for precision-weighting.3 In the predictive processing framework, every prediction error is not equally informative. The brain must estimate the precision—or inverse variance—of the error signal to determine how much weight it should carry in updating internal beliefs.8 High precision corresponds to high reliability, while low precision corresponds to noise.8

## **Gain Control and Signal Reliability**

Attention is defined as the process of optimizing precision during hierarchical inference.38 It functions as a context-sensitive gain control on prediction error units.4 By increasing the gain (or volume) of selected error units, the brain effectively increases the precision of those specific signals, making them more likely to override existing priors and drive model updating.36 This mechanism allows the system to treat even small prediction errors as significant if they are expected to be informative, such as in the case of spatial attention directed toward a likely target location.4

| Attentional Mode | Precision-Weighting Mechanism | Information Processing Outcome |
| :---- | :---- | :---- |
| **Exogenous (Bottom-up)** | Automatic response to strong/salient error | Abrupt capture of resources due to high informative value.38 |
| **Endogenous (Top-down)** | Volitional expectation of reliability | Deliberate gain enhancement for task-relevant features.4 |
| **Sensory Attenuation** | Downweighting of self-generated error | Suppressing signals during self-action (e.g., cannot tickle oneself).39 |
| **Feature-Based** | Gain modulation on identity/config units | Resolving ambiguity by upping gain on specific residual errors.4 |

Neurobiologically, this gain modulation is thought to be mediated by neuromodulators such as dopamine, which controls the precision of cortical unsigned prediction error signals.28 The ascending reticular activating system (ARAS) and superficial pyramidal cells also play critical roles in implementing this context-sensitive gating.16 When precision-weighting is set high, the system is malleable and adaptive; when it is set low, the system is robust to noise but resistant to change.8

## **The Paradox of Precision and Surprise**

An intriguing insight from this framework is that attention can "flip" the interpretation of the same sensory data.4 If the brain expects a high-precision signal in a particular spatial or feature domain, it can treat that signal as a self-fulfilling prophecy, upping the gain until it dominates the perceptual landscape.39 This highlights why "random surprise"—errors that are perceived as having low precision or high noise—fails to produce significant learning.36 The brain's architecture is built to selectively ignore surprise when it lacks structure, effectively "muting" the noise to prevent the generative model from collapsing into chaos.8

## **Learning Dynamics: Violation vs. Confirmation**

The predictive processing framework dictates that the depth of belief updating is determined by the nature of the prediction error encountered.4 Proposal 5 confirms that information which violates predictions in a structured, meaningful way drives the deepest updates, whereas confirming information produces minimal learning.4

## **The Failure of Confirmation**

When incoming signals match top-down expectations, they are successfully "silenced" or predicted away by the internal model.4 Because no error signal propagates forward, there is no trigger for the higher-level models to change their parameters.4 This leads to a state of high computational efficiency but zero information gain.43 In this state, the brain remains metabolically "lazy," as no adjustment to its internal representational scheme is required.4 This confirms that factual accuracy is secondary to "surprisal" in driving attention; a piece of information can be perfectly true, but if it was already expected, it will receive low attention and result in minimal updating of the audience's model.4

## **Structured Prediction Error as an Informative Signal**

Learning is fundamentally the proactive reduction of prediction error over time.8 Deep updating occurs when information departs from the predicted value in a way that provides a clear, precise signal rather than mere noise.4 For deep domains like language or social behavior, the brain employs knowledge-rich acquired generative models to track multiple interacting hidden variables.4 When these high-level structures are violated by a signal that is "optimally surprising"—meaning it has enough precision to be taken seriously but enough error to demand change—it forces a cascading revision of the entire model hierarchy.8

| Information Category | Signal Characteristics | Learning & Attention Outcome |
| :---- | :---- | :---- |
| **Confirmed Prediction** | Zero error; silenced.4 | Low attention; zero belief updating; metabolic efficiency.4 |
| **Random Surprise** | High uncertainty; low precision; treated as noise.36 | Muted signal; minimal learning; possible arousal without update.36 |
| **Structured Violation** | High precision error; pattern-driven discrepancy.33 | Strong attention; deep belief updating; model reconfiguration.4 |

This "optimally surprising" information occupies the limits of an agent's predictive capabilities—the "edge of informational chaos"—where the most significant error-reducing opportunities are found.33 This provides a neurological justification for seeking out "sweet spots" of complexity in information delivery, as seen in the research on children as Bayesian learners and the human attraction to fictional content that pushes the limits of understanding.33

## **Social Cognition and Audience Prediction Profiles**

The predictive mind is not an isolated engine; it is a social organ tailored to the problem of predicting other people.49 Social cognition is conceptualized as the process of mutual prediction between brains, realizing a dynamic coupling with minimized error.49 We understand other minds not through direct perception, but through top-down inference on the causes of their actions and expressions.49

## **Theory of Mind as Hierarchical Inference**

Successful interaction depends on building multi-layered models of others, where internal mental states (e.g., tiredness, intentions) and traits (e.g., agreeableness, power) support predictions about their observable actions.50 These dimensions combine to form a synthetic model used to anticipate social outcomes.50 In this context, an audience's "prediction profile" consists of the specific set of priors and expectations they hold about a communicator, a topic, or the likely trajectory of an interaction.34

| Social Layer | Information Represented | Role in Interaction |
| :---- | :---- | :---- |
| **Observable Actions** | Gestures, speech, expressions.50 | Raw sensory data for error detection. |
| **Hidden Mental States** | Momentary feelings or intentions.50 | Intermediate causes used to predict actions. |
| **Hidden Traits** | Enduring personality regularities.50 | High-level priors that set the context for states. |
| **Cultural Hyperpriors** | Skills, knowledge, and social norms.34 | Global constraints on the prediction mechanism. |

The "problem of perception" in social settings is determining the right hypothesis to explain ambiguous social cues.51 A person's mindset, co-constituted by culture-relative skills and norms, acts as a hyperprior that operates at the very top of this hierarchy.34 For strategic communication, this means that the message must be tailored to these hyperpriors to be even recognized as meaningful information.

## **From Knowledge Gaps to Prediction Profiles**

Traditional communication models often focus on "knowledge gaps"—the information an audience lacks. However, from a predictive processing standpoint, a knowledge gap is only useful if the audience has a predictive model that *anticipates* that information or is *surprised* by its absence.34 If a communicator delivers information for which the audience has no prior model, it may be categorized as random noise and attenuated.36 Conversely, if the audience already has a model that accurately predicts the message, the information will be explained away.4 The correct target for research design, therefore, is the audience's prediction profile—the specific violations and confirmations of their existing priors.34

## **Interoception, Affect, and Mood-Specific Prediction Profiles**

One of the most critical findings for research architecture is the relationship between interoceptive predictions and mood states.1 The EPIC model proposes that interoceptive experience—our sense of the body from within—is largely a reflection of limbic predictions about the body's expected state, constrained by ascending sensations.1

## **Interoception and Allostatic Budgeting**

Limbic regions, such as the anterior cingulate and anterior insula, are situated at the top of the predictive hierarchy.29 These regions issue visceromotor predictions to adjust autonomic, hormonal, and immune systems in anticipation of the body's needs.1 This process of "homeostatic budgeting" ensures that resources are mobilized efficiently.1 Affective properties—valence and arousal—emerge from these predictions, serving as basic features of consciousness that reflect the brain's "best guess" about the somatic consequences of action.8

## **Mood as a Hyperprior over Precision**

Mood states are increasingly understood as high-level hyperpriors that regulate the precision-weighting of lower-level predictions.8 This means that an audience’s current mood state defines what constitutes "optimally surprising" information for them. For example, in a depressed mood state, the brain may harbor a hyperprior that the world and body are uncontrollably uncertain.8 This leads to a computational pathology where sensory prediction errors are treated as "noisy" and ignored, effectively decoupling the brain's fantasy from the body's reality.1

| Mood State | Bayesian Profile (Hyperprior) | Informational Consequence |
| :---- | :---- | :---- |
| **Positive Affect** | High precision on controllable future.8 | Increased attention to "sweet-spot" challenges; fast updating. |
| **Negative Affect** | High uncertainty; loss of prior precision.8 | Signals treated as noise; low motivation for belief revision. |
| **Depression** | High expected uncertainty/uncontrollability.8 | Decoupling from error; sickness behavior; metabolic conservation.13 |
| **Anxiety** | Overly dominant top-down threat predictions.8 | Enhanced perception of threat from neutral stimuli (aberrant error).8 |

This establishes the neurological necessity of mood-specific research architecture. If mood determines the weighting of information, then the same piece of research or feedback will be processed entirely differently by an audience in an "anxious" state versus a "playful" or "positive" state.8 Strategic research must account for these profiles to identify the threshold at which information will be perceived as structured error rather than overwhelming noise or irrelevant confirmation.34

## **Functional Integration: The Meeting of Mind and Body**

The predictive processing framework successfully dissolves the artificial boundary between mind and body by showing that cognitive and visceral processes are governed by the same computational laws.1 The brain's visceromotor regions are "rich-club" hubs, highly connected nodes that integrate internal and external predictions into a single, amodal "sense of self".28

| Hub Region | Predictive Function | Integration Point |
| :---- | :---- | :---- |
| **Anterior Insula (aINS)** | High-level interoceptive priors; self-awareness.29 | Cortical interface where attention, prediction, and body input meet.61 |
| **Anterior Cingulate (ACC)** | Allostatic visceromotor control.1 | Integration of salience into "global emotional moments".30 |
| **Mid-Posterior Insula** | Primary interoceptive sensory cortex.63 | Site where prediction error is computed from visceral afferents.55 |
| **Default Mode Network** | Maintenance of high-level generative models.29 | Internal construction of meaningful concepts from sensations.29 |

Disruptions in the flow of these signals—either through inaccurate priors or faulty precision-weighting—lead to a range of pathologies, from chronic pain and eating disorders to schizophrenia.37 In schizophrenia, for instance, positive symptoms like hallucinations may result from an underweighting of sensory priors and an inappropriately high weighting of internally generated prediction errors, causing the brain to assign profound significance to neutral stimuli.8

## **Strategic Implications for the Cognitive Communication Program (CCP)**

The exhaustive research compiled here provides a definitive foundation for the principles of the CCP. By confirming that the brain is an active inference engine, we can derive a new set of rules for effective communication and intervention.

## **1\. Shift from Knowledge Gaps to Prediction Profiles**

The analysis confirms that audience prediction profiles are the correct target for research design.34 Information that confirms audience predictions, regardless of its factual accuracy, is silenced by the predictive hierarchy and produces minimal belief updating.4 Coaches and communicators must first identify the "priors" of their audience—what they expect the results to be—and then design research that selectively violates those expectations.4

## **2\. Utilizing Structured Prediction Error**

Information delivery must aim for a specific precision level. Random surprise—information that is completely unrelated to the audience's current model—will be ignored as noise.36 Deep belief updating requires structured prediction error—information that is surprising but follows a discernible, learnable pattern that the generative model can use to reorganize itself.4 This is the "sweet spot" of information complexity.48

## **3\. Neurological Necessity of Mood-Specific Architecture**

Mood states act as hyperpriors that dictate how information is weighted.8 Because a depressed or anxious audience will have a different prediction profile and a different threshold for "optimally surprising" information than a positive one, communication strategies must be mood-specific.8 This establishes the neurological necessity of building mood-state profiles into research architecture to ensure that feedback is even processed by the target system.55

## **4\. Guided Active Inference**

Communicators should view themselves as "epistemic generators" who produce potential interpretive trajectories for the audience to follow.44 By moving away from a model of passive receipt and toward a model of guided active inference, communicators allow the audience to "self-supervise" the updating of their own mental models through information-rich sampling of the world.20

## **Conclusion**

The predictive processing framework and the principle of active inference offer a rigorous, unified account of how the mind-brain system functions. By prioritizing the minimization of prediction error through the flexible weighting of precision, the human brain maintains an adaptive grip on a volatile world.5 This report has detailed the hierarchical architecture, the modulatory role of attention, and the fundamental distinction between confirmation and violation that drives learning. For strategic communication, the message is clear: to change a mind, one must understand its predictions and deliver information that is structured enough to be believed, yet surprising enough to demand change.4 The future of research design lies not in uncovering what is unknown, but in challenging what is expected.

#### **Works cited**

1. (PDF) Interoceptive predictions in the brain \- ResearchGate, accessed March 10, 2026, [https://www.researchgate.net/publication/277411625\_Interoceptive\_predictions\_in\_the\_brain](https://www.researchgate.net/publication/277411625_Interoceptive_predictions_in_the_brain)  
2. Interoceptive predictions in the brain, accessed March 10, 2026, [https://affective-science.org/pubs/2015/barrett-simmons-nature-neuroscience-2015.pdf](https://affective-science.org/pubs/2015/barrett-simmons-nature-neuroscience-2015.pdf)  
3. Whatever next? Predictive brains, situated agents, and the future of cognitive science, accessed March 10, 2026, [https://www.research.ed.ac.uk/en/publications/whatever-next-predictive-brains-situated-agents-and-the-future-of/](https://www.research.ed.ac.uk/en/publications/whatever-next-predictive-brains-situated-agents-and-the-future-of/)  
4. Whatever next? Predictive brains, situated agents, and the future of cognitive science \- FIL | UCL, accessed March 10, 2026, [https://www.fil.ion.ucl.ac.uk/\~karl/Whatever%20next.pdf](https://www.fil.ion.ucl.ac.uk/~karl/Whatever%20next.pdf)  
5. (PDF) Review of surfing uncertainty: prediction, action, and the embodied mind, by Andy Clark, Oxford University Press, 2016 \- ResearchGate, accessed March 10, 2026, [https://www.researchgate.net/publication/318185426\_Review\_of\_surfing\_uncertainty\_prediction\_action\_and\_the\_embodied\_mind\_by\_Andy\_Clark\_Oxford\_University\_Press\_2016](https://www.researchgate.net/publication/318185426_Review_of_surfing_uncertainty_prediction_action_and_the_embodied_mind_by_Andy_Clark_Oxford_University_Press_2016)  
6. The predictive brain and the “free will” illusion \- PMC \- NIH, accessed March 10, 2026, [https://pmc.ncbi.nlm.nih.gov/articles/PMC3639403/](https://pmc.ncbi.nlm.nih.gov/articles/PMC3639403/)  
7. Andy Clark's SURFING UNCERTAINTY Review \- Academia.edu, accessed March 10, 2026, [https://www.academia.edu/33727979/Andy\_Clarks\_SURFING\_UNCERTAINTY\_Review](https://www.academia.edu/33727979/Andy_Clarks_SURFING_UNCERTAINTY_Review)  
8. What we think about when we think about predictive processing \- PMC, accessed March 10, 2026, [https://pmc.ncbi.nlm.nih.gov/articles/PMC7509909/](https://pmc.ncbi.nlm.nih.gov/articles/PMC7509909/)  
9. The free-energy principle: a unified brain theory? \- FIL | UCL, accessed March 10, 2026, [https://www.fil.ion.ucl.ac.uk/\~karl/NRN.pdf](https://www.fil.ion.ucl.ac.uk/~karl/NRN.pdf)  
10. The free-energy principle: a unified brain theory?, accessed March 10, 2026, [https://www.uab.edu/medicine/cinl/images/KFriston\_FreeEnergy\_BrainTheory.pdf](https://www.uab.edu/medicine/cinl/images/KFriston_FreeEnergy_BrainTheory.pdf)  
11. A Free Energy Principle for Biological Systems \- PMC, accessed March 10, 2026, [https://pmc.ncbi.nlm.nih.gov/articles/PMC3510653/](https://pmc.ncbi.nlm.nih.gov/articles/PMC3510653/)  
12. Friston, K.J.: The free-energy principle: a unified brain theory? Nat. Rev. Neurosci. 11, 127-138 \- ResearchGate, accessed March 10, 2026, [https://www.researchgate.net/publication/41001209\_Friston\_KJ\_The\_free-energy\_principle\_a\_unified\_brain\_theory\_Nat\_Rev\_Neurosci\_11\_127-138](https://www.researchgate.net/publication/41001209_Friston_KJ_The_free-energy_principle_a_unified_brain_theory_Nat_Rev_Neurosci_11_127-138)  
13. An active inference theory of allostasis and interoception in depression | Philosophical Transactions of the Royal Society B, accessed March 10, 2026, [https://royalsocietypublishing.org/rstb/article/371/1708/20160011/42178/An-active-inference-theory-of-allostasis-and](https://royalsocietypublishing.org/rstb/article/371/1708/20160011/42178/An-active-inference-theory-of-allostasis-and)  
14. The Free Energy Principle | Request PDF \- ResearchGate, accessed March 10, 2026, [https://www.researchgate.net/publication/384215713\_The\_Free\_Energy\_Principle](https://www.researchgate.net/publication/384215713_The_Free_Energy_Principle)  
15. Free energy principle \- Wikipedia, accessed March 10, 2026, [https://en.wikipedia.org/wiki/Free\_energy\_principle](https://en.wikipedia.org/wiki/Free_energy_principle)  
16. Attention and prediction in human audition: a lesson from cognitive psychophysiology \- PMC, accessed March 10, 2026, [https://pmc.ncbi.nlm.nih.gov/articles/PMC4402002/](https://pmc.ncbi.nlm.nih.gov/articles/PMC4402002/)  
17. The Predictive Mind: Karl Friston's Free Energy Principle and Its Implications for Consciousness \- \- Taproot Therapy, accessed March 10, 2026, [https://gettherapybirmingham.com/the-predictive-mind-karl-fristons-free-energy-principle-and-its-implications-for-consciousness/](https://gettherapybirmingham.com/the-predictive-mind-karl-fristons-free-energy-principle-and-its-implications-for-consciousness/)  
18. (PDF) The free-energy principle: a unified brain theory? (2010) | Karl J. Friston \- SciSpace, accessed March 10, 2026, [https://scispace.com/papers/the-free-energy-principle-a-unified-brain-theory-3vz1twg7nv](https://scispace.com/papers/the-free-energy-principle-a-unified-brain-theory-3vz1twg7nv)  
19. Predictive Coding Theories of Cortical Function \- arXiv, accessed March 10, 2026, [https://arxiv.org/pdf/2112.10048](https://arxiv.org/pdf/2112.10048)  
20. Surfing Uncertainty \- Bookey, accessed March 10, 2026, [https://cdn.bookey.app/files/pdf/book/en/surfing-uncertainty.pdf](https://cdn.bookey.app/files/pdf/book/en/surfing-uncertainty.pdf)  
21. Predictive coding in the visual cortex: a functional interpretation of some extra-classical receptive-field effects \- PubMed, accessed March 10, 2026, [https://pubmed.ncbi.nlm.nih.gov/10195184/](https://pubmed.ncbi.nlm.nih.gov/10195184/)  
22. Predictive coding in the visual cortex: a functional interpretation of some extra-classical receptive-field effects, accessed March 10, 2026, [https://homes.cs.washington.edu/\~rao/Rao-Ballard-NN-1999.pdf](https://homes.cs.washington.edu/~rao/Rao-Ballard-NN-1999.pdf)  
23. (PDF) Predictive Coding in the Visual Cortex: a Functional Interpretation of Some Extra-classical Receptive-field Effects \- ResearchGate, accessed March 10, 2026, [https://www.researchgate.net/publication/13103385\_Predictive\_Coding\_in\_the\_Visual\_Cortex\_a\_Functional\_Interpretation\_of\_Some\_Extra-classical\_Receptive-field\_Effects](https://www.researchgate.net/publication/13103385_Predictive_Coding_in_the_Visual_Cortex_a_Functional_Interpretation_of_Some_Extra-classical_Receptive-field_Effects)  
24. Predictive Coding in Cortical Responses | PDF | Visual Cortex | Neuroscience \- Scribd, accessed March 10, 2026, [https://www.scribd.com/document/929245931/A-Theory-of-Cortical-Responses](https://www.scribd.com/document/929245931/A-Theory-of-Cortical-Responses)  
25. Is predictive coding theory articulated enough to be testable? \- Frontiers, accessed March 10, 2026, [https://www.frontiersin.org/journals/computational-neuroscience/articles/10.3389/fncom.2015.00111/full](https://www.frontiersin.org/journals/computational-neuroscience/articles/10.3389/fncom.2015.00111/full)  
26. Stimulus Predictability Reduces Responses in Primary Visual Cortex, accessed March 10, 2026, [https://www.jneurosci.org/content/30/8/2960](https://www.jneurosci.org/content/30/8/2960)  
27. Whatever next? Predictive brains, situated agents, and the future of cognitive science, accessed March 10, 2026, [https://www.cambridge.org/core/journals/behavioral-and-brain-sciences/article/whatever-next-predictive-brains-situated-agents-and-the-future-of-cognitive-science/33542C736E17E3D1D44E8D03BE5F4CD9](https://www.cambridge.org/core/journals/behavioral-and-brain-sciences/article/whatever-next-predictive-brains-situated-agents-and-the-future-of-cognitive-science/33542C736E17E3D1D44E8D03BE5F4CD9)  
28. Active interoceptive inference and the emotional brain \- PMC \- NIH, accessed March 10, 2026, [https://pmc.ncbi.nlm.nih.gov/articles/PMC5062097/](https://pmc.ncbi.nlm.nih.gov/articles/PMC5062097/)  
29. Attachment: a predictive coding approach \- arXiv.org, accessed March 10, 2026, [https://www.arxiv.org/pdf/2505.05476](https://www.arxiv.org/pdf/2505.05476)  
30. Ghosts in the Machine. Interoceptive Modeling for Chronic Pain Treatment \- Frontiers, accessed March 10, 2026, [https://www.frontiersin.org/journals/neuroscience/articles/10.3389/fnins.2016.00314/full](https://www.frontiersin.org/journals/neuroscience/articles/10.3389/fnins.2016.00314/full)  
31. Whatever Next? Predictive Brains, Situated Agents, and the Future of Cognitive Science, accessed March 10, 2026, [https://www.researchgate.net/publication/236689333\_Whatever\_Next\_Predictive\_Brains\_Situated\_Agents\_and\_the\_Future\_of\_Cognitive\_Science](https://www.researchgate.net/publication/236689333_Whatever_Next_Predictive_Brains_Situated_Agents_and_the_Future_of_Cognitive_Science)  
32. Predictive coding, accessed March 10, 2026, [https://homes.cs.washington.edu/\~rao/predcoding2011.pdf](https://homes.cs.washington.edu/~rao/predcoding2011.pdf)  
33. Surfing uncertainty with screams: predictive processing, error dynamics and horror films, accessed March 10, 2026, [https://pmc.ncbi.nlm.nih.gov/articles/PMC10725765/](https://pmc.ncbi.nlm.nih.gov/articles/PMC10725765/)  
34. The predictive mind and the experience of visual art work \- PMC, accessed March 10, 2026, [https://pmc.ncbi.nlm.nih.gov/articles/PMC4267174/](https://pmc.ncbi.nlm.nih.gov/articles/PMC4267174/)  
35. Andy Clark's Surfing Uncertainty // Reviewed by Andrew Buskell \- BSPS, accessed March 10, 2026, [https://www.thebsps.org/reviewofbooks/andy-clark-surfing-uncertainty-prediction-action-and-the-embodied-brain/](https://www.thebsps.org/reviewofbooks/andy-clark-surfing-uncertainty-prediction-action-and-the-embodied-brain/)  
36. The many faces of precision (Replies to commentaries on “Whatever ..., accessed March 10, 2026, [https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2013.00270/full](https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2013.00270/full)  
37. Neurocomputational Underpinnings of Expected Surprise \- PMC \- NIH, accessed March 10, 2026, [https://pmc.ncbi.nlm.nih.gov/articles/PMC8802931/](https://pmc.ncbi.nlm.nih.gov/articles/PMC8802931/)  
38. Three Problems for the Predictive Coding Theory of Attention \- Minds Online, accessed March 10, 2026, [https://mindsonline.philosophyofbrains.com/wp-content/uploads/2015/09/2015-Ransom-and-Fazelpour-Three-Problems-for-the-Predictive-Coding-Theory-of-Attention-extended-abstract.pdf](https://mindsonline.philosophyofbrains.com/wp-content/uploads/2015/09/2015-Ransom-and-Fazelpour-Three-Problems-for-the-Predictive-Coding-Theory-of-Attention-extended-abstract.pdf)  
39. Edinburgh Research Explorer \- Predictions, precision, and agentive attention \- Account, accessed March 10, 2026, [https://www.pure.ed.ac.uk/ws/portalfiles/portal/80715336/ClarkCC2017PredictionsPrecisionAndAgentiveAttention.pdf](https://www.pure.ed.ac.uk/ws/portalfiles/portal/80715336/ClarkCC2017PredictionsPrecisionAndAgentiveAttention.pdf)  
40. Decoding Prediction Errors in the Brain: A Laminar Neural Mass Model Approach, accessed March 10, 2026, [https://www.neuroelectrics.com/blog/decoding-prediction-errors-in-the-brain-a-laminar-neural-mass-model-approach](https://www.neuroelectrics.com/blog/decoding-prediction-errors-in-the-brain-a-laminar-neural-mass-model-approach)  
41. Attention is more than prediction precision | Behavioral and Brain Sciences | Cambridge Core, accessed March 10, 2026, [https://www.cambridge.org/core/journals/behavioral-and-brain-sciences/article/attention-is-more-than-prediction-precision/2AED030F4830149D14019EA3AC096E7C](https://www.cambridge.org/core/journals/behavioral-and-brain-sciences/article/attention-is-more-than-prediction-precision/2AED030F4830149D14019EA3AC096E7C)  
42. 02\_Hohwy \- — Philosophy and Predictive Processing, accessed March 10, 2026, [https://predictive-mind.net/epubs/how-to-entrain-your-evil-demon/OEBPS/02\_Hohwy.xhtml](https://predictive-mind.net/epubs/how-to-entrain-your-evil-demon/OEBPS/02_Hohwy.xhtml)  
43. Surfing Uncertainty: Prediction, Action, and the Embodied Mind by Andy Clark | Goodreads, accessed March 10, 2026, [https://www.goodreads.com/book/show/25823558-surfing-uncertainty](https://www.goodreads.com/book/show/25823558-surfing-uncertainty)  
44. Surfing Uncertainty: Prediction, Action, and the Embodied Mind | Request PDF, accessed March 10, 2026, [https://www.researchgate.net/publication/345888580\_Surfing\_Uncertainty\_Prediction\_Action\_and\_the\_Embodied\_Mind](https://www.researchgate.net/publication/345888580_Surfing_Uncertainty_Prediction_Action_and_the_Embodied_Mind)  
45. Precision weighting of cortical unsigned prediction errors is mediated by dopamine and benefits learning | bioRxiv, accessed March 10, 2026, [https://www.biorxiv.org/content/10.1101/288936v2.full-text](https://www.biorxiv.org/content/10.1101/288936v2.full-text)  
46. Predictive coding \- Wikipedia, accessed March 10, 2026, [https://en.wikipedia.org/wiki/Predictive\_coding](https://en.wikipedia.org/wiki/Predictive_coding)  
47. Surfing Uncertainty \- Hardcover \- Andy Clark \- Oxford University Press, accessed March 10, 2026, [https://global.oup.com/academic/product/surfing-uncertainty-9780190217013](https://global.oup.com/academic/product/surfing-uncertainty-9780190217013)  
48. Play in Predictive Minds: A Cognitive Theory of Play \- Monash University, accessed March 10, 2026, [https://researchmgt.monash.edu/ws/portalfiles/portal/558291917/444607213\_oa.pdf](https://researchmgt.monash.edu/ws/portalfiles/portal/558291917/444607213_oa.pdf)  
49. Is Social Cognition Merely a Predictive Process?, accessed March 10, 2026, [https://rikkyo.repo.nii.ac.jp/record/20956/files/Philosophy%20&%20cultural%20embodiment\_01-01\_03.pdf](https://rikkyo.repo.nii.ac.jp/record/20956/files/Philosophy%20&%20cultural%20embodiment_01-01_03.pdf)  
50. Modeling the predictive social mind \- PMC, accessed March 10, 2026, [https://pmc.ncbi.nlm.nih.gov/articles/PMC5828990/](https://pmc.ncbi.nlm.nih.gov/articles/PMC5828990/)  
51. The Predictive Mind \- Notre Dame Philosophical Reviews, accessed March 10, 2026, [https://ndpr.nd.edu/reviews/the-predictive-mind/](https://ndpr.nd.edu/reviews/the-predictive-mind/)  
52. Modeling the Predictive Social Mind | Request PDF \- ResearchGate, accessed March 10, 2026, [https://www.researchgate.net/publication/322573621\_Modeling\_the\_Predictive\_Social\_Mind](https://www.researchgate.net/publication/322573621_Modeling_the_Predictive_Social_Mind)  
53. Review of:The Predictive Mind. Jakob Hohwy. Oxford University Press, 2013, 286pp, Hardcover, £65, ISBN 9780199682737\. \- Academia.edu, accessed March 10, 2026, [https://www.academia.edu/32065143/Review\_of\_The\_Predictive\_Mind\_Jakob\_Hohwy\_Oxford\_University\_Press\_2013\_286pp\_Hardcover\_65\_ISBN\_9780199682737](https://www.academia.edu/32065143/Review_of_The_Predictive_Mind_Jakob_Hohwy_Oxford_University_Press_2013_286pp_Hardcover_65_ISBN_9780199682737)  
54. The power of predictions: An emerging paradigm for psychological ..., accessed March 10, 2026, [https://pmc.ncbi.nlm.nih.gov/articles/PMC6867616/](https://pmc.ncbi.nlm.nih.gov/articles/PMC6867616/)  
55. Interoceptive predictions in the brain \- PMC \- NIH, accessed March 10, 2026, [https://pmc.ncbi.nlm.nih.gov/articles/PMC4731102/](https://pmc.ncbi.nlm.nih.gov/articles/PMC4731102/)  
56. What is mood? A computational perspective \- PMC \- NIH, accessed March 10, 2026, [https://pmc.ncbi.nlm.nih.gov/articles/PMC6340107/](https://pmc.ncbi.nlm.nih.gov/articles/PMC6340107/)  
57. Evidence for a Large-Scale Brain System Supporting Allostasis and Interoception in Humans | bioRxiv, accessed March 10, 2026, [https://www.biorxiv.org/content/10.1101/098970v1.full-text](https://www.biorxiv.org/content/10.1101/098970v1.full-text)  
58. Surfing Uncertainty: Prediction, Action, and the Embodied Mind, accessed March 10, 2026, [https://www.research.ed.ac.uk/en/publications/surfing-uncertainty-prediction-action-and-the-embodied-mind/](https://www.research.ed.ac.uk/en/publications/surfing-uncertainty-prediction-action-and-the-embodied-mind/)  
59. \[PDF\] Interoceptive predictions in the brain \- Semantic Scholar, accessed March 10, 2026, [https://www.semanticscholar.org/paper/Interoceptive-predictions-in-the-brain-Barrett-Simmons/7a0b470ccc96aa1c8a95f0723c49e70cb18507b2](https://www.semanticscholar.org/paper/Interoceptive-predictions-in-the-brain-Barrett-Simmons/7a0b470ccc96aa1c8a95f0723c49e70cb18507b2)  
60. Interoception Network in the Rat Brain | bioRxiv, accessed March 10, 2026, [https://www.biorxiv.org/content/10.64898/2026.02.08.704721v1.full-text](https://www.biorxiv.org/content/10.64898/2026.02.08.704721v1.full-text)  
61. Hemispheric divergence of interoceptive processing across psychiatric disorders | eLife, accessed March 10, 2026, [https://elifesciences.org/articles/92820](https://elifesciences.org/articles/92820)  
62. Altered Interoceptive Activation Before, During, and After Aversive Breathing Load in Women Remitted from Anorexia Nervosa \- Eating Disorders Center for Treatment and Research, accessed March 10, 2026, [https://eatingdisorders.ucsd.edu/sites/default/files/eatingdisorders/files/publications/nihms971408.pdf](https://eatingdisorders.ucsd.edu/sites/default/files/eatingdisorders/files/publications/nihms971408.pdf)  
63. Structural connectivity of an interoception network in schizophrenia \- Clinical Neuroscience Lab, accessed March 10, 2026, [https://cnl.psy.msu.edu/wp-content/uploads/2023/07/Yao2023-1.pdf](https://cnl.psy.msu.edu/wp-content/uploads/2023/07/Yao2023-1.pdf)  
64. I \- Surfing Uncertainty \- Prediction, Action and The Embodied Mind \- I \- , by Andy Clark (Australasian Journal of Philosophy) (2017) | PDF | Mind | Perception \- Scribd, accessed March 10, 2026, [https://www.scribd.com/document/698630724/i-Surfing-Uncertainty-Prediction-Action-and-the-Embodied-Mind-i-by-Andy-Clark-Australasian-Journal-of-Philosophy-2017](https://www.scribd.com/document/698630724/i-Surfing-Uncertainty-Prediction-Action-and-the-Embodied-Mind-i-by-Andy-Clark-Australasian-Journal-of-Philosophy-2017)

[image1]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAFwAAAAUCAYAAAAA5FpZAAACUUlEQVR4Xu2YTagNYRjHH7lEKUmRUq66lBILlspGYkFE3VuULESysFO2FpJ8da2kfCUlCwu6W0lKd2Fja0FS94pSLCx8/H89z+ucM82M02nOcaY7v/p1zsz7njlz/u/M875zzBoaGhqGmnlyfnbnAFgdXpRLM229sFkez+4cJk7Ib/K73JJp6zcEfCMc7WzqGX4Dv2loaQL/D+yQX2ywgVPCzslTYVXUInBO8n28Doq18kW8YlU0gRfAxPZIjoRVUdvAr8if8rk8Ku+aB/RWbg2zLJE35Str1ebT8rZ8Is/LBdH3jjwb7/NI9f2BeV+8Z/4dZdQ2cDgjf8vDsc2VSOiEiln2yHF5yHwSxp3RxtKPwWK+ILRn0a+IS9YakP3hjNzwt0c+fQ18jTzYpaxPmagwS1ngH8zDSqSrDbPskqvMB+NpuCjaCOqz+TFT4AxQHgvlY/lGHpEbQ46Rd/7t1D7wd+YhJsoCh2Vy2vyzmNgrf8nd9u/AgX5fze+w5LGOHvn0NfCqqDJwjsGtvy0EBvm6+RW7wspLCn33WWswVlrrbin6znZqETjBEFIVgbP6mJXrQhgzr98HYptQ71v+pLlefjKv4UDfybCbIJvArQm8A06Op0xqJEGxjZfNH/nZ/9F8pfLSfKmYZJsSkUirGMK9FZ6UU3J7Wz8oWocvltfkBTlhPgHzRIppSVnG0AdeJdRbwiZMVie43PInalYdr634SZM6z/G6CbmdORV4UWnKg0G4anP0v5Qq4PZnFfLD/Kl0U1gG5ehhONrZ1DN9CfwPI2qbNty5+LoAAAAASUVORK5CYII=>

[image2]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAANMAAAAUCAYAAAAX6gjVAAAFDklEQVR4Xu2aacilYxjHL1myZpsMIbsSEqJsjYRIJEwZxAcfULIvYRQhRLJMpJQxZSlbkiWUgw+2D5YGJQpZQhTxYcjy/3Vdl/c+97znvIv3LDNz/+vXOc9+n+e5/vd93ddzzJqampqampqamprGSmuJLcU2YiuxdqxfL1g3lsdRtJX2N62m4gFfL94PvhIfi07wmvg01t8RjEIE4cnmbXlPXCGuFs+Lo8WTwf55wJgo79kf4kvzTmAuxX05U9wqNq22NQ1ZzUyDVTPTGqgjg7/FOdU2DHezuDsYprg2XCV+Nm9jqQ3EUvF7MG5mSnFPB2Gm9cVz4lexT7VtI3FZfDYNUTcFvQLyeHFJMEydEPwpzq22pfYSnweTtX0cxP0bhJkQhtqsXinNE/eJjesNTYNT9m7wrtg81vPgSa3QceLYYFgibXkr+Fps1735P9H+R4LaTAQZBYtRT/x7mYmCCYUUPueqeMJvBVLhV62ZaajaWXwXZBrHwzhfLMqdRiDSFtIX6Fj/oNgv2CKWdxcviMXiAvGyWBCgvc1Hsn/MU7A7xQPiI7EkIKVcKpaZm/lEDrTuY+Eh8aj58R+Ip8TWsW+qNhPGudw82M+2iU7jmtjGfDDnsK+I7cXDQc5rTzMfrZmPZUaxofloBNy3v8zb/qF5uw8R75ifozwPHQ7XYd0zsdw0C5FGZWD8Zn5DfxA/ij2K/fqJm/+YTRQupuJFc7PUeX4pgiPnQh3rb6ZSO4jl4phiHakgxQs4MNYR2AQ4wZXBc6hYEWCwLL2TAr8hNollPlkGgo+5G2I0fV28ZN3trc10qblx58fybgH7HB7rOBcB/qC5wZg3JtkuRLaAcepR+Uqb/L6VIz6dRo7aJ5mfe9Sj+CotRqOfgjQPKRVpUwbPKDSTkYkeGQiy62zllIpjOwHBScCkmRgFUgTk9wHGShGY5TnL8zEylWKkY45XHl+aiTSadPrxWIZdgzfNr5WiY/jEvFJ5e1Cng7SZDnC6ZkJkHcCotZP5/bgxvvcT7TllmvD81ihj5oPtBHnjebAXx/dRqexBvxDbdm3tFvMD4AES3P3MBCynmcrgzcCsg3MmZsI4jPJ8luvy+LxuaaaSOvgXil/EwUGtfmYqR9NSmAYwE6bieZNiThX8zUx9xEjEiJTVvNlqEGkeOiOgZM/nZCLFuiHAgPyOumBRpmXMb9axwZnpdPP2lmX80kzZSTxh3o5+Yl/mP/eaj1BAQJfqZ6a8JtuYX6UIclhi3pZbxEHF9qZZqHzw5cMfF2WVi4DiPVPdMxMQF5nn+4D2FN/YynOmb4OjYt1cmelpm0i9es2ZuM/l8XQMGJ4RoRSjEL06opO4SxwW358NmEdxnVQvM/EaI69JysnL3VoYaIV555bzvqZZqpmpmamZ6X+KwOMBUFYlv6d6B1lCHTdRWFhknpIy1yA4gVSJz0xbUgeYT+bvEdeKt8URAeI3UhbOCiYpKqVqDJuVTb6zjm3swzrMSKdTmukzc7OfZV6CL0vj+Xei+njaep75XBDD3BZQDOHdGNfMZ0Npn3dRy4NsG/tcGN/zGZYdIukgpfpl5ueu00OEgfhL1qn1hqbVX5hqF/N3PoxAdWWr1qBe2tZzJtpFwNfFg6lUHjfTY6cjzj/Pet+nHP3m1xuamoal2kyrihaYj+58AikkVdCmppFoR3G/TbxQ5p8jpFGT/T9u3LSv+TxqcUCVsJx/Nc1Q/wJ5aIrgtHX/RwAAAABJRU5ErkJggg==>