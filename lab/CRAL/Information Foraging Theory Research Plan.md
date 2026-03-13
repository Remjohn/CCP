# **Information Foraging Theory: An Adaptationist Framework for Cognitive Information-Seeking and Research Penetration**

The conceptual landscape of information science underwent a paradigm shift with the introduction of Information Foraging Theory (IFT), a framework that reframes human information-seeking behavior not as a series of isolated cognitive tasks, but as an adaptive process shaped by the evolutionary pressures of our ancestral environment.1 At its core, IFT posits that modern humans, or "informavores," navigate the digital and institutional "flux of information" using the same optimization logic that governed biological foraging for energy and sustenance.3 This optimization is centered on the principle of maximizing the rate of information gain per unit cost, where costs are measured in temporal, cognitive, and physical effort.4 Central to this theory is the concept of "information scent," a proximal mechanism by which foragers evaluate the potential value of distal information sources based on environmental cues.5

## **The Biological Foundations: Optimal Foraging and the Marginal Value Theorem**

To understand the cognitive mechanics of information seeking, one must first examine the biological origins of the theory in the field of behavioral ecology. The work of Stephens and Krebs (1986) established the foundational models for how organisms interact with resources distributed in discrete patches.7 Biological foraging is characterized by two primary challenges: the "diet problem" (choosing which items to consume) and the "patch problem" (deciding when to leave a location for a more profitable one).7

The Marginal Value Theorem (MVT) serves as the cornerstone of this biological optimization logic.7 It predicts that a forager should remain in a resource patch as long as the instantaneous rate of gain within that patch remains higher than the average rate of gain expected from the habitat as a whole, including the time required to travel to a new patch.7 As a patch is exploited, the resources are depleted, and the rate of intake inevitably declines—a phenomenon known as the "gain function".7

### **Mathematical Representation of Optimal Patch Residence**

The MVT defines the optimal residence time (![][image1]) using the relationship between the cumulative gain (![][image2]), the time spent within the patch (![][image3]), and the travel time between patches (![][image4]).7 The goal is to maximize the long-term average rate of gain (![][image5]):

![][image6]  
The optimal solution occurs when the marginal rate of gain (the derivative of the gain function) equals the average rate of gain for the habitat 7:

![][image7]

| Biological Foraging Component | Information Foraging Equivalent | Optimization Implication |
| :---- | :---- | :---- |
| **Patch** | Website, database, or document collection | Resources are clustered; travel costs are real 1 |
| **Prey** | Specific facts, data points, or named entities | Items vary in value and "handling" time 8 |
| **Travel Time** | Latency, navigation time, or search effort | Increased travel time leads to longer patch persistence 7 |
| **Gain Function** | Cumulative knowledge extraction | Diminishing returns occur as easy data is found first 7 |
| **Giving-Up Density (GUD)** | Remaining unanswered queries in a source | Foragers leave when the "scent" falls below a threshold 9 |

This biological logic implies that if the "travel time" to a new information source is high—such as needing to switch between different institutional archives or overcoming complex authentication barriers—a researcher will naturally stay in their current source longer, even if its marginal returns are low.7 Conversely, in high-speed digital environments where travel time is nearly zero, researchers exhibit much shorter residence times, switching patches frequently to stay at the "steepest" part of the gain function.13

## **The Emergence of Information Foraging Theory (1999)**

In their foundational 1999 paper, Pirolli and Card transitioned these ecological concepts into a formal cognitive theory. They proposed that human information-gathering strategies are adaptations to the structure of the information environment.1 The theory is developed through two distinct lenses: adaptation (rational) analysis and the ACT-IF process model.1 Rational analysis assumes that the cognitive system has evolved to solve the problem of information scarcity and overload by selecting strategies that are superior in their returns per unit cost.4

### **The Informavore's Cognitive Architecture**

The ACT-IF (Adaptive Control of Thought in Information Foraging) model integrates the optimization logic of foraging into a broader cognitive architecture.1 This model suggests that the allocation of attention is the central problem in sense-making.4 Just as an animal must decide whether to stalk a high-value but elusive prey or settle for abundant but low-energy forage, the informavore must balance the "expected value" of information against the "cognitive handling costs".1

A critical second-order insight from this 1999 work is that people do not just adapt *to* their environment; they actively modify the structure of the environment (the "interface") to improve their foraging returns.4 This is evident in the creation of personal archives, the use of bookmarks, and the development of specialized search filters, all of which serve to increase the "prey density" and reduce "travel costs" in the future.2

## **Information Scent: The Mechanism of Scent Gradient and Selection**

The most significant contribution of IFT to the understanding of search behavior is the concept of "information scent".3 Scent is the subjective perception of the value and relevance of a distal information source based on "proximal cues"—the titles, snippets, thumbnails, or metadata encountered during navigation.5 These cues act as a surrogate for the actual content, allowing the forager to make probabilistic assessments of where to direct their attention.5

### **The Scent Gradient and Patch Persistence**

In Pirolli’s 2007 expansion of the theory, Chapters 2 and 4 detail the "scent gradient" mechanism.14 A scent gradient is the perceived increase or decrease in relevance as a forager moves through a document hierarchy or web structure.15 When a researcher follows a path where the scent becomes progressively stronger and more specific—for example, moving from a broad category like "Legal Documents" to "Supreme Court Rulings" to "Environmental Law 2023"—the scent gradient is "steep".6

A steep and specific scent gradient serves as a high-penetration directive.13 It signals to the cognitive system that the target "prey" (e.g., a specific named-entity evidence or primary document) is highly likely to be found in the deeper layers of the current patch.15 This causes the researcher to "drill down" deeper into the source material than they would under generic conditions where the scent is weak or flat.6

| Scent Strength | Scent Specificity | Behavioral Manifestation | Research Depth |
| :---- | :---- | :---- | :---- |
| **Strong** | **High (Precise)** | Penetration into primary documents and raw data | Deep excavation; named-entity capture 6 |
| **Strong** | **Low (Broad)** | Exploration of multiple related sub-patches | High quantity of sources; topical breadth 6 |
| **Weak** | **High (Precise)** | Quick dismissal; "no-prey" signal | Minimal depth; rapid switching 6 |
| **Weak** | **Low (Generic)** | Surface skimming; berrypicking | Shallow; high reliance on broad stats 6 |

If the scent gradient fails to strengthen or begins to "thin out," the informavore reaches a "tipping point".20 This leads to patch abandonment, where the researcher returns to a "hub" (like a search engine or table of contents) to find a more promising trail.13

## **Empirical Validation: Modeling User Needs and Actions**

The concept of information scent is not merely metaphorical; it has been rigorously validated through computational modeling and experimental protocol analysis. Chi, Pirolli, Chen, and Pitkow (2001) demonstrated that user surfing patterns could be predicted with high accuracy using algorithms that measure the semantic relatedness between user goals and link labels.5

### **The SNIF-ACT Architecture and Semantic Relatedness**

The SNIF-ACT model utilizes Latent Semantic Analysis (LSA) to compute the "scent" of navigation options.13 LSA measures the semantic similarity between the user's information need and the text of a link by analyzing word co-occurrence in large corpora.5 The model successfully predicts that users will select links with the highest semantic match to their current goal, effectively "following the scent".5

Key results from empirical studies indicate that:

1. **Backtracking** is significantly more likely when the scent of the current path declines below a threshold.19  
2. **Visual Search** on a page is guided by scent; users fixate on cues that are semantically "closer" to their target while ignoring distractors.15  
3. **Site Stickiness** is a function of perceived value; if a site emits a strong scent of relevant "prey," users will sequentially visit multiple pages within that site rather than returning to a global search engine.6

This evidence confirms that the navigation of complex information spaces is not random but follows a directed, optimization-based path dictated by the specificity of the information scent.5

## **Scholars as Subsistence Foragers: Sandstrom’s Source Hierarchy**

While Pirolli and Card focused on digital navigation, Pamela Sandstrom (1994) applied foraging theory to the sociology of scholarly communication.25 She observed that scholars act as subsistence foragers who make strategic decisions about their "information diet" and "patch choice" to maximize their professional fitness.12

### **Source Hierarchy Logic and the Principle of Least Effort**

Sandstrom proposed a "source hierarchy logic" based on the Principle of Least Effort.26 In this model, researchers rank information sources based on their "profitability"—the expected information return relative to the time and effort required to extract it.12

* **High-Profitability Sources:** Peer-reviewed journals in the researcher's immediate niche, known primary archives, and expert colleagues.11  
* **Low-Profitability Sources:** Obscure publications, disorganized physical archives, or documents in foreign languages that require high "handling time".12

Scholars are naturally "opportunistic foragers".25 They will prioritize sources that offer a high "scent" of reliable information with minimal "travel" costs.12 However, the most profound insight from Sandstrom’s work is that the "depth" of a scholar's research is often constrained by their "diet breadth".25 If the initial research directive is too broad, the scholar becomes a generalist, consuming many low-value "prey" (generic facts) from easily accessible patches.6 Only when the directive is highly specific does the scholar narrow their diet to "high-yield" primary sources that require deeper excavation.6

## **Confirmation for CCP Application: The Specificity Thesis**

The research confirms a critical causal relationship: the specificity of the initial search directive is the primary determinant of research depth and the quality of findings.6 This "Specificity Thesis" can be broken down into three interlocking mechanisms that govern the transition from surface browsing to deep institutional excavation.

### **1\. The Trigger Mechanism as a High-Scent Directive**

A precise research directive—often containing a named entity (e.g., a specific person, corporation, or event) or a specific document type (e.g., a board meeting transcript or an internal memorandum)—functions as a "high-scent trigger".23 Because the target is unambiguous, the semantic "match" between the directive and proximal cues in institutional databases is exceptionally strong.5

This high-scent trigger creates a "tunnel effect" in navigation.18 The researcher is less likely to be distracted by tangential "scent trails" and more likely to invest the necessary cognitive effort to bypass complex search barriers.6 This directive specificity causes the agent to "penetrate" into primary documents and institutional sources because the scent of the specific evidence remains high even as the "cost" of deeper digging increases.6

### **2\. Patch-Abandonment and the Generic Directive**

Conversely, a generic or topical directive (e.g., "Research the history of environmental policy in the 1990s") produces a "flat scent profile".6 Because the directive matches thousands of potential cues, the "scent" of any single source is not sufficiently strong to justify high handling costs.6

In these conditions, the informavore follows a "satisficing" strategy.16 They will stay in a patch only as long as the information is "easy" to find—usually resulting in surface-level findings like broad statistics, introductory summaries, or unverifiable claims.6 As soon as the search requires significant effort (e.g., reading a 100-page primary report), the marginal rate of gain drops below the threshold, and the researcher abandons the patch for an easier, shallower source.6

### **3\. Finding Quality and Named-Entity Evidence**

The quality of findings is a direct byproduct of the "penetration depth" achieved during the foraging process. Primary documents and institutional records typically contain "dense prey"—highly specific evidence that is not available in surface-level "aggregated" summaries.1 Accessing this density requires a "sustained scent" that can only be generated by a specific initial directive.6

| Directive Type | Scent Persistence | Evidence Type Retrieved | Finding Quality |
| :---- | :---- | :---- | :---- |
| **Trigger-based (High Specificity)** | Persistent through complex barriers | Named-entities, primary documents, raw evidence | High (Authentic, specific, deep) 6 |
| **Topical (Generic)** | Rapidly decays during deep search | Summaries, broad stats, generic claims | Low (Surface-level, derivative) 6 |

Experimental evidence from eye-tracking studies confirms that users with specific instructions are "more diagnostic" and "stricter" in their appraisal of information.6 They reject "empty calories"—information that looks relevant but lacks substance—far more effectively than users with broad tasks.6

## **Synthesis and Implications for Complex Intelligence Analysis**

The application of Information Foraging Theory to complex research environments—such as military intelligence or high-stakes institutional auditing—reveals that the "foraging environment" must be carefully structured to support high-scent directives.15 If an intelligence analyst is given a broad topical directive, they will naturally gravitate toward "information overload" at the surface level, failing to identify the critical "named-entity evidence" buried in raw traffic or institutional archives.6

To overcome this, IFT suggests that systems should "enhance information scent cues" to make the path to primary documents more visible.15 This involves:

* **Improving Labeling:** Using specific terminology that matches the triggers of expert researchers.16  
* **Reducing Travel Costs:** Automating the transition between different "patches" or archives to keep the researcher at the steepest part of the gain function.19  
* **Goal-Targeting:** Providing tools that allow researchers to maintain a "persistent scent" of their goal even when navigating through thousands of pages of noise.15

Furthermore, the rise of Generative AI (GenAI) presents a new challenge for information foraging.1 GenAI often provides an "illusion of value" by synthesizing information into structured formats like bullet points.28 However, because the "scent" in these responses is often disconnected from the primary documents, it can lead to "empty calorie" consumption, where the researcher feels they are gaining knowledge but is actually only interacting with surface-level aesthetics.28 The solution, as proposed in frameworks like InForage, is to train search agents to prioritize "information gain" from primary sources rather than merely optimizing for narrative coherence.29

## **Conclusion**

Information Foraging Theory provides a robust, mathematically grounded explanation for why some research efforts result in profound, primary-source insights while others remain mired in surface-level generalities.1 The theory definitively demonstrates that the specificity of the search directive acts as a high-scent trigger that dictates the depth of penetration into the information landscape.6

When a researcher is armed with a specific, named-entity directive, the scent gradient remains steep enough to pull the agent through high-cost, high-value institutional patches.6 Without this specificity, the optimization logic of the human mind—evolved to conserve energy and avoid unproductive "travel"—will inevitably lead to patch abandonment and the acceptance of shallow, easily available forage.6 For any application requiring deep institutional excavation and the capture of named-entity evidence, the creation of high-scent, high-specificity directives is not merely a tactical choice, but a cognitive necessity derived from our evolutionary history as informavores.3

#### **Bibliografia**

1. (PDF) Information Foraging \- ResearchGate, accesso eseguito il giorno marzo 10, 2026, [https://www.researchgate.net/publication/229101074\_Information\_Foraging](https://www.researchgate.net/publication/229101074_Information_Foraging)  
2. Information Foraging Theory \- Peter Pirolli, accesso eseguito il giorno marzo 10, 2026, [https://www.peterpirolli.com/ewExternalFiles/31354\_C01\_UNCORRECTED\_PROOF.pdf](https://www.peterpirolli.com/ewExternalFiles/31354_C01_UNCORRECTED_PROOF.pdf)  
3. Tracking the scent of information \- American Psychological Association (APA), accesso eseguito il giorno marzo 10, 2026, [https://www.apa.org/monitor/2012/03/information](https://www.apa.org/monitor/2012/03/information)  
4. Information foraging theory \- ResearchGate, accesso eseguito il giorno marzo 10, 2026, [https://www.researchgate.net/profile/Peter-Pirolli/publication/229101074\_Information\_Foraging/links/02bfe50f098acc0ea8000000/Information-Foraging.pdf](https://www.researchgate.net/profile/Peter-Pirolli/publication/229101074_Information_Foraging/links/02bfe50f098acc0ea8000000/Information-Foraging.pdf)  
5. Using Information Scent to Model User Information Needs and Actions on the Web, accesso eseguito il giorno marzo 10, 2026, [https://www.researchgate.net/publication/221517585\_Using\_Information\_Scent\_to\_Model\_User\_Information\_Needs\_and\_Actions\_on\_the\_Web](https://www.researchgate.net/publication/221517585_Using_Information_Scent_to_Model_User_Information_Needs_and_Actions_on_the_Web)  
6. Understanding the effects of task and topical knowledge in the ..., accesso eseguito il giorno marzo 10, 2026, [https://www.emerald.com/jd/article/74/1/162/207679/Understanding-the-effects-of-task-and-topical](https://www.emerald.com/jd/article/74/1/162/207679/Understanding-the-effects-of-task-and-topical)  
7. How optimal foragers should respond to habitat changes: a ..., accesso eseguito il giorno marzo 10, 2026, [https://pmc.ncbi.nlm.nih.gov/articles/PMC4194746/](https://pmc.ncbi.nlm.nih.gov/articles/PMC4194746/)  
8. Optimal Foraging Theory: An Introduction, accesso eseguito il giorno marzo 10, 2026, [https://www.cec.org/files/sem/20231030/aaa003.pdf](https://www.cec.org/files/sem/20231030/aaa003.pdf)  
9. Testing Marginal Value Theorem in Saimiri sciureus \- Bucknell Digital Commons, accesso eseguito il giorno marzo 10, 2026, [https://digitalcommons.bucknell.edu/cgi/viewcontent.cgi?article=1311\&context=honors\_theses](https://digitalcommons.bucknell.edu/cgi/viewcontent.cgi?article=1311&context=honors_theses)  
10. State dependent behavior and the Marginal Value Theorem \- Oxford Academic, accesso eseguito il giorno marzo 10, 2026, [https://academic.oup.com/beheco/article/12/1/71/392385](https://academic.oup.com/beheco/article/12/1/71/392385)  
11. Fishing for the Right Words: Decision Rules for Human Foraging Behavior in Internal Search Tasks, accesso eseguito il giorno marzo 10, 2026, [https://malagr.de/hutch/hutchpub/cogsci1.pdf](https://malagr.de/hutch/hutchpub/cogsci1.pdf)  
12. The handicap principle: A new perspective for library and information science research, accesso eseguito il giorno marzo 10, 2026, [http://d-scholarship.pitt.edu/25116/1/colis/colis23.html](http://d-scholarship.pitt.edu/25116/1/colis/colis23.html)  
13. Information foraging \- Wikipedia, accesso eseguito il giorno marzo 10, 2026, [https://en.wikipedia.org/wiki/Information\_foraging](https://en.wikipedia.org/wiki/Information_foraging)  
14. Information Foraging Theory \- Peter Pirolli, accesso eseguito il giorno marzo 10, 2026, [https://www.peterpirolli.com/Professional/About\_Me\_files/IFT%20Ch%201.pdf](https://www.peterpirolli.com/Professional/About_Me_files/IFT%20Ch%201.pdf)  
15. Information foraging theory | Semantic Scholar, accesso eseguito il giorno marzo 10, 2026, [https://www.semanticscholar.org/paper/Information-foraging-theory-Pirolli/57039425c233b73f42de261e248a9dbafa146653](https://www.semanticscholar.org/paper/Information-foraging-theory-Pirolli/57039425c233b73f42de261e248a9dbafa146653)  
16. Chapter 10 How Search Engine Users Evaluate and Select Web Search Results: The Impact of the Search Engine Interface on Credibility Assessments \- Emerald Publishing, accesso eseguito il giorno marzo 10, 2026, [https://www.emerald.com/books/edited-volume/13820/chapter/84609872/Chapter-10-How-Search-Engine-Users-Evaluate-and](https://www.emerald.com/books/edited-volume/13820/chapter/84609872/Chapter-10-How-Search-Engine-Users-Evaluate-and)  
17. Information Foraging Theory:Adaptive Interaction with Information \- Google Libros, accesso eseguito il giorno marzo 10, 2026, [https://books.google.com.co/books?id=LADEE\_1fwLQC](https://books.google.com.co/books?id=LADEE_1fwLQC)  
18. The Information Architecture of Behavior Change Websites \- Journal of Medical Internet Research, accesso eseguito il giorno marzo 10, 2026, [https://www.jmir.org/2005/2/e12/](https://www.jmir.org/2005/2/e12/)  
19. CHI 2001 \- Research, accesso eseguito il giorno marzo 10, 2026, [https://research.cs.vt.edu/ns/cs5724papers/5.usageenvir.adaptation.card.infoscent.pdf](https://research.cs.vt.edu/ns/cs5724papers/5.usageenvir.adaptation.card.infoscent.pdf)  
20. 1 Nolan J. Taylor Kelley School of Business Indiana University Indianapolis, IN 46202 notaylor@iupui.edu 317-274-0185 Fax \- SSRN, accesso eseguito il giorno marzo 10, 2026, [https://papers.ssrn.com/sol3/Delivery.cfm/SSRN\_ID2518647\_code1287059.pdf?abstractid=2518647\&mirid=1](https://papers.ssrn.com/sol3/Delivery.cfm/SSRN_ID2518647_code1287059.pdf?abstractid=2518647&mirid=1)  
21. Using information scent to model user information needs and actions and the Web, accesso eseguito il giorno marzo 10, 2026, [https://research.google/pubs/using-information-scent-to-model-user-information-needs-and-actions-and-the-web/](https://research.google/pubs/using-information-scent-to-model-user-information-needs-and-actions-and-the-web/)  
22. Identification of Web User Traffic Composition using Multi-Modal Clustering and Information Scent, accesso eseguito il giorno marzo 10, 2026, [https://homes.cs.washington.edu/\~jheer/files/2001-Lumberjack-SIAM.pdf](https://homes.cs.washington.edu/~jheer/files/2001-Lumberjack-SIAM.pdf)  
23. Information Foraging Theory: A Framework for Intelligence ... \- DTIC, accesso eseguito il giorno marzo 10, 2026, [https://apps.dtic.mil/sti/tr/pdf/AD1003600.pdf](https://apps.dtic.mil/sti/tr/pdf/AD1003600.pdf)  
24. Modeling Goal-Directed User Exploration in Human-Computer Interaction, accesso eseguito il giorno marzo 10, 2026, [http://reports-archive.adm.cs.cmu.edu/anon/hcii/CMU-HCII-11-102.pdf](http://reports-archive.adm.cs.cmu.edu/anon/hcii/CMU-HCII-11-102.pdf)  
25. An Optimal Foraging Approach to Information Seeking and Use | The Library Quarterly, accesso eseguito il giorno marzo 10, 2026, [https://www.journals.uchicago.edu/doi/abs/10.1086/602724](https://www.journals.uchicago.edu/doi/abs/10.1086/602724)  
26. An Optimal Foraging Approach to Information Seeking and Use ..., accesso eseguito il giorno marzo 10, 2026, [https://www.semanticscholar.org/paper/An-Optimal-Foraging-Approach-to-Information-Seeking-Sandstrom/c037a9dab2f07a218637b73a5335f385d1ede349](https://www.semanticscholar.org/paper/An-Optimal-Foraging-Approach-to-Information-Seeking-Sandstrom/c037a9dab2f07a218637b73a5335f385d1ede349)  
27. Evaluation of Online Information in University Students: Development and Scaling of the Screening Instrument EVON \- PMC, accesso eseguito il giorno marzo 10, 2026, [https://pmc.ncbi.nlm.nih.gov/articles/PMC7773327/](https://pmc.ncbi.nlm.nih.gov/articles/PMC7773327/)  
28. Conversations over Clicks: Impact of Chatbots on Information Search in Interdisciplinary Learning \- arXiv, accesso eseguito il giorno marzo 10, 2026, [https://arxiv.org/html/2507.21490v2](https://arxiv.org/html/2507.21490v2)  
29. Scent of Knowledge: Optimizing Search-Enhanced Reasoning with ..., accesso eseguito il giorno marzo 10, 2026, [https://openreview.net/forum?id=26kUrQm4zw\&referrer=%5Bthe%20profile%20of%20Hongjin%20Qian%5D(%2Fprofile%3Fid%3D\~Hongjin\_Qian1)](https://openreview.net/forum?id=26kUrQm4zw&referrer=%5Bthe+profile+of+Hongjin+Qian%5D\(/profile?id%3D~Hongjin_Qian1\))

[image1]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA8AAAAYCAYAAAAlBadpAAAA5ElEQVR4XmNgGNaAGYgZoZhkQFAzPxCXQLEkVAykGKSxA4g1oZgFKocCXID4IRQrQcW0gHgVEPcA8XQormOAGIgCyoH4ABTzQMVAigKA+A4Qz4FimKvAQBeIQ4D4EBBvg2KQBhEGiDN9gDgBiI2gOIoByenmQJwKxO+BuBOK/YFYCKaAAWIAyEYUW2HAFIjvMiAChSSQDsSngVgQikkCZGsGxeV8BkhIkgxANoFsjUYSA8W5LBIfJwBF1QMGSKDJQHELELMiqcEJQAliKxC3A/FiKJZHUUEAgFKSMJTGSHqjYDAAAGJNH4m6XXB0AAAAAElFTkSuQmCC>

[image2]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACUAAAAYCAYAAAB9ejRwAAACbElEQVR4Xu2WTahNURTHl1AU+Uz5Sj4iEcnHQJQBxcAEhQwVhqKQEQOJkigTGTBQwgwz8ZIiBsxNkBhIMlBG+P/uXvvdfdY5x3uvR67yq1/vvr3P3Xfttdfe+5j95+8wWZ6UE2NHgP7jcoI7ICPcZfKG/CDfymdyi5whz7rj/TvA4DfliqLtV6yRZ9zRoa9GzwVF+hkYX8lNcqT3jZUX5Ht50S056jYxTh6T84s2Js5S4+GivQIzvS8fuAQYWSo/y21uZq587H+bWGdpMstDO+PhEzk79HXSd9nSFxe4TUy3tIyL3cx+eVuOKtpKyOBzOSm0j3HvyF2hrzPr7/JEaI8Q1DVLy4FAIAR0KD9kaWnWuvwYAT2SO+Sc4rkMO/FK2UCk9ywtC6kcKsyeH91atBHoBveA/GKpoAlqZv9TXUhKn3UnarPkO2tO72Agey/lytjhbJQfrV5PJUzojaWxOjDYV3ndUtpL+H+fpXrLXpKLXBgoqLZ6Kvk3gmIXfbJUwE1wJbAb2bYv5EJLuzUfeG1B5Z1FvVaKuIFaUJxPTy0UWmCepZM9HpjAQBy01E4JBY2v5R5vW2/ppogQVC2b2+U3udu610yGz0fkD6semBkm0mf1PjKHbKLVliZ/Xk4pH3I4Tsgome2HH95p6Vh46O5171o6R85Z9cAsIYOnQts0l1U4bak82r7P8rZdUZ06WeVypnBpVqJvYbOlw7HpNYQxp1r3Di2hHbmiYk0OG5aQ9FMzQ4HJIFlsu6KGBVm9aultYjCQ1VvuktD32+jJoIAdeNDqh3CEOmPzxFegPwZvo01FXUJ/+dba+/wELTN4lYmUKN0AAAAASUVORK5CYII=>

[image3]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABIAAAAYCAYAAAD3Va0xAAABCklEQVR4Xu3UvUoDQRSG4SNqodEuIEKqYJNCUomVEMFCC1OIZSSQKgGTW0hlp42N+NOJIIIQewsvw8LGxsab8P2cE3aSIuyGhVj4wVPszOzhcHZYs//MJAvoua2xvUwp48sdjO1lSt2SQiqaOZs4xgveXcPXM2UbJ/jAg1PhSnwobfTSt4XZ5DIfzWaq+QyTW6FLvKLgpsoK3nAWrWlmu9FzqqzjE0dYdCq64a7Q9rMd7LguWr7+myU84xq3Tt3MoYlD3Fjo/NFCt6Jro2IjmUfRko7inGPfwkd4wqqropYcmxx1cY8S9nAX7an4WvQ8MfojXOAUfQwsXBXRTFMnt0LDaCaaoyy7P54f8PUpGvQ2K9IAAAAASUVORK5CYII=>

[image4]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA0AAAAZCAYAAADqrKTxAAAA40lEQVR4Xu3RvwsBYRzH8UeYKPk1KBKDMsgk/4CdwWaU7FLKKCX/gyg2O7OsNrviL/Av+Hzdx3X33D2ly+hdr+7qe88dz6PUP08JGkNOmxlr0QPK2szYhE4Qd4+81aALZzpCBzLOh/QCLWrCAJ60hDaknA/51YAbVbWZsSFcKKnNfAvBBlakV4cZ2cmb5Qs9kuS8CryXXzEiO9m9u7L+l8jDHLKwVdbmXEl29V2gRXL6B1jQDoqcyVntefWcWxjSJPef5MtriNBXySaIElXcY//6MOVVRN1jczFlnaX4ukCLftML0Noq2ppg2xUAAAAASUVORK5CYII=>

[image5]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA8AAAAYCAYAAAAlBadpAAABDklEQVR4Xu3SsUtCURQG8CMqFOkgQRBEQZtz4BRONrg02NoWEjgKLS1N/hMRhLtrKOEgOAZutQdhQzTaoIR+p/Pd132PCw7SEPjBDx73vHPf4b4r8u+zAVd0G3BB267Bz0rNKbGCuoYJVGAXDuCG3qHEnmDu4AkK3ppuol7hQWzSWPI0hHuxaVwOSb8cbC7SJ1wmauc0g9NE7Se6qL6gKjbmHtThmU4kPlGUFn2Ija2n3IUX2KdgtqBPHchwfRN6YpslzyHKSs3uJFXTW3ebDijn1aLohZiSPru4TdsUjN6qN9ITdjkSu21+cwN29KEm1vANcxrL79f1pRE80pnYH3FnsjRZKNMxpOPldf4+CwNhQfFsQMghAAAAAElFTkSuQmCC>

[image6]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAmwAAAAuCAYAAACVmkVrAAAD4ElEQVR4Xu3dO6icRRQH8Ak+MCqY+A4JaIIgIiIBBQUjPkksFFEDAQsbNWoh4hNSCIJBrATBQiNobAQJiIUoYhFE8AnaKdoE0TQiNmojoucw35LZyc3u3pvF5N78fvBn9zvz3VsfZnZmSgEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABgsrMjz/XFKTZFTumLAAAszU2RDyMHIvsjl0Web8bfiWxunmf1WGRVXwQAYHYXRX6IrO7qv0euHr5vHNI6GLmyqy1kW+SjvggAwOw+jnzZF8OnkXOH7zsjJzdj6avI2q62kPwfX/RFAABmk83Ud5EL+oFGNmXZnI3cEHko8mLknqY+ya6+AADAbHLJc185fPastS7ybVe7pcy2HDryTOTMvggAwHTZeGUzNZKbA7IR+6XURu2k4bNt2E6LvN88pzXDZ/59ZkMzljRsAABLlBsJ3ijjuzivi/zdPGfD9mPzvL7UnaRpS+TWUn/jlsuq+bc5/v0wPpIN26RZPACAZee1BXLO2Bvz81Tkr8i9kUdKbb5eGXujlJeb7+dHPo/sLfXoj7S71IbsreF5x/CZzih2iQIAK9Alkc8i35Q6w5VHb/wR2dq+NEe5zJkbCC7vBwZ5NMdZzXMehpvLpSk/95S6geGDUhvL7cNYyqYuGzwAgBUlf1v2T+SOpvZbqUdwHCtvlsPPamtl05f6mw3eLXVWDgBgRcljMLJBGy05pmzg7m6e/293lXprwWLkcuhVfREAYCX4OfJ1qb9dy6XRT8aHx+RS5pFyRfPeSO7WPB4CALCstcuhufsyD7edl7wTNHdxHsu8XQAAlrH8Ldj+cmgWqj9mo/fThDzZvAcAwJxsKuPHaNwe+Xf4/nBTBwDgOJKzbjnTNjpKAwCAE0AedPtoX5yD6yMP9kUAABYvNzUc7ItT5PLsNAdKvTUBAICjkMd9vFfqjs2Fjv44kkkNW950cGfkz1LvDu0P0AUAYJF+jdzWF6eY1LCl/K3d630RAIClyeXQ3JE6kpsazmueR9oL6PMS9/Y5D+dtrS+WQwEA5iLPeNs9fL8xsiayr9SGa5JpM2y5FLq21P9/aqnLoqOl0fzMq6ryIGAAAKZYV+rdoNlEXRrZUurl7jc37yxkWsO2N7Iqsr3Upu3pyOOl7kjNGbzclZqzdAAATLE68mpkz/A8aqimmdawPRB5IfJE5OJSNzRsK3XmLpON4rOjlwEAmF02a6dH7usHOhf2hSmuLXXGbefwvDWy8dAwAACzuiayK7K5HzhKGyL3R14qtWnbUWoDBwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAnjv8AOBONS0Uw4c4AAAAASUVORK5CYII=>

[image7]: <data:image/png;base64,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>