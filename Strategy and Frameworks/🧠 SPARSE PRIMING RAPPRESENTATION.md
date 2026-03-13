Sparse Priming Representation \(SPR\) is a strategy designed to compress complex information into a minimal set of keywords or phrases that can trigger associative learning in large language models \(LLMs\)\. This compression, much like how the human brain handles memory, allows for efficient recall and reconstruction of the original idea by activating the relevant parts of an __LLM’s latent space\. __Essentially, SPR acts as a "prompt within a prompt," providing just enough information to activate the model's latent knowledge while saving on tokens\.  
  
__SPR for Creative Priming:__

- __Priming Creativity__: SPR can be used to trigger specific creative directions by focusing the model on key themes, moods, or styles without overloading it with details\. For example, in writing a story, SPR could consist of a few keywords like "mysterious forest, lost civilization, ancient ritual\." This primes the model's latent knowledge related to fantasy, ancient history, or rituals, giving it the necessary context to build creatively\.
- __Efficiency__: In creative contexts, SPR allows you to evoke certain associations \(e\.g\., "dark, surreal, fragmented reality" for a story tone\) while leaving enough room for imaginative output\. You can push the model toward a specific atmosphere or creative style without stifling its ability to generate original ideas\.
- SPR primes the model with just the essential ideas, themes, or concepts, giving the model freedom to explore those in creative ways\. It allows for a more open\-ended generation, which is often what creativity needs\. 
- __Flow and Innovation__: Creative content thrives on unexpected ideas and associations\. 
- __Mimicking Human Creativity__: Human creative processes are often not linear or structured step\-by\-step, but more intuitive and associative\. SPR mirrors this process by priming key concepts and letting the model freely connect the dots\. This can lead to richer, more surprising creative content\.
- __Organic Storytelling__: For tasks like storytelling, poetry, or visual descriptions, you might want the model to "follow its muse" rather than be boxed into logical progressions\. SPR enables the model to start with an idea, mood, or setting and then freely elaborate, potentially leading to more unique outcomes\.
- __Emergence vs\. Structure__: Creativity often thrives on emergent properties—ideas that come to life through interaction, iteration, or improvisation\. SPR, by providing a "seed" of essential information, allows the model to generate emergent ideas naturally without imposing too much order, fostering more imaginative content\.

### <a id="_cg4hd9ss2etq"></a>__Use Case: How SPR Alone Enhances Creativity__

Here’s an example of how using only SPR might work better for creative generation:

#### <a id="_1qqe214es045"></a>__Example: Writing a Fantasy Short Story__

- __SPR__: "Medieval kingdom, forbidden magic, a young hero discovers ancient power, looming war with dark forces\."
- __Result__: The model can now freely explore multiple aspects of this world—whether it’s introducing the characters, crafting detailed settings, or allowing dramatic conflicts to emerge organically\. There's no structured guidance, so the story can take surprising turns, create poetic descriptions, or reveal complex emotions without being tied to specific steps\.

### <a id="_byut2pbrv103"></a>__Creative Writing or Visual Arts:__

- __Poetry__: SPR could provide themes and emotions \("love, longing, the passage of time, fleeting moments"\)\. Without CoT, the model has room to explore these in abstract ways, possibly generating more evocative and layered poetry\.
- __Visual Descriptions__: If you’re generating visual concepts or artistic descriptions, SPR alone might lead to more imaginative and visually dynamic outputs by simply focusing on key imagery or mood \("dreamlike landscape, shifting colors, floating islands"\)\.

# <a id="_jvcxz1655zbn"></a>__Sparse Priming Representations \(SPR\)__

Theory and Reasoning

Sparse Priming Representation \(SPR\) is a memory organization technique that aims to mimic the natural structure and recall patterns observed in human memory\. The fundamental idea behind SPR is to distill complex ideas, concepts, or knowledge into a concise, context\-driven list of statements that allows subject matter experts \(SMEs\) or large language models \(LLMs\) to reconstruct the full idea efficiently\.

Human memory is known for its efficiency in storing and recalling information in a highly compressed and contextually relevant manner\. Our brains often store memories as sparse, interconnected representations that can be quickly combined, modified, and recalled when needed\. This enables us to make associations, draw inferences, and synthesize new ideas with minimal cognitive effort\.

SPR leverages this insight by focusing on reducing information to its most essential elements while retaining the context required for accurate reconstruction\. By using short, complete sentences to convey the core aspects of an idea, SPR enables faster understanding and recall, mirroring the way our brains handle information\.

In addition to its efficiency, SPR has practical applications in various domains, such as artificial intelligence, information management, and education\. It can be utilized to improve the performance of LLMs in handling large data volumes and optimizing memory organization\. Furthermore, it can help students and professionals alike to better understand, retain, and communicate complex concepts\.

Sparse Priming Representation

There are only a handful of ways to "teach" LLMs, and all have limitations and strengths\.

Most of the techniques out there do not make use of the best superpower that LLMs have: LATENT SPACE\. No one else seems to understand that there is one huge way that LLMs work similarly to human minds: associative learning\. Here's the story: I realized a long time ago that, with just a few words, you could "prime" LLMs to think in a certain way\. I did a bunch of experiments and found that you can "prime" models to even understand complex, novel ideas that were outside its training distribution\. 

These SPRs are the most token\-efficient way to convey complex concepts to models for in\-context learning\. What you do is compress huge blocks of information, be it company data, chat logs, specific events, or whatever, into SPRs, and then you store the SPR in the metadata of your KG node or whatever\. The SPR is what you feed to the LLM at inference, not the raw human\-readable data\.

SPR Generator

Use this to compress any arbitrary block of text into an SPR\.

__\# MISSION__

You are a Sparse Priming Representation \(SPR\) writer\. An SPR is a particular kind of use of language for advanced__ NLP, NLU, and NLG__ tasks, particularly useful for the latest generation of Large Language Models \(LLMs\)\. You will be given information by the USER which you are to render as an SPR\.

__\# THEORY__

LLMs are a kind of deep neural network\. They have been demonstrated to embed knowledge, abilities, and concepts, ranging from reasoning to planning, and even to theory of mind\. These are called latent abilities and latent content, collectively referred to as latent space\. The latent space of an LLM can be activated with the correct series of words as inputs, which will create a useful internal state of the neural network\. This is not unlike how the right shorthand cues can prime a human mind to think in a certain way\. Like human minds, LLMs are associative, meaning you only need to use the correct associations to "prime" another model to think in the same way\.

__\# METHODOLOGY__

Render the input as a distilled list of succinct statements, assertions, associations, concepts, analogies, and metaphors\. The idea is to capture as much, conceptually, as possible but with as few words as possible\. Write it in a way that makes sense to you, as the future audience will be another language model, not a human\. Use complete sentences\.

  
  
  
  
  
The language remains conversational, down\-to\-earth, and emotionally grounded, making it relatable and reflective of real\-life struggles and aspirations\.  
  
Each statement should feel emotionally grounded — show how these people really feel, not just what they think\. Link everything back to the DHDs, so each entry evokes deeper emotional resonance around security, success, pride, or confidence\.  


\*\*Curiosity Phrases:\*\*

Phrases that pique the viewer’s curiosity and make them want to watch further\. Pose intriguing questions or make statements that suggest there's valuable information to follow\. Use phrases like "What if I told you\.\.\.," "Have you ever wondered\.\.\.," or "Did you know\.\.\.?"

\*\*Here are examples of what Curiosity Phrases are are:\*\* 

"What if I told you that you’re losing money every day by not doing this one thing?"

"Have you ever wondered how much more you could achieve with just a minor change?"

“Did you know there’s a way to read minds using simple psychology tricks?”

"Do you want to know the secret to your competitor's success?"

\*\*Familiarity Phrases:\*\*

Sentences that create a sense of connection and understanding between you and the viewer\. To build rapport and trust with the viewer\. Address common experiences, emotions, or challenges that your audience faces\. Write as if you are speaking to a friend\. Use phrases like "You know that feeling when\.\.\.," "We've all been there\.\.\.," or "I understand what you're going through\.\.\."

\*\*Here are examples of what Familiarity Phrases are are:\*\* 

"You know that sinking feeling of missing out on a great opportunity?"

"We’ve all been there, regretting not taking action sooner\."

”Remember how tedious shopping used to be?”

"You've seen others succeed while you struggle, haven't you?"

"Everyone wants to be the best in their field – don't you?"

\*\*Bold Claims:\*\*

Strong, confident statements that assert a particular point of view to create impact and make your message memorable\. Make definitive statements that provoke thought or challenge the viewer's current mindset\.

\*\*Here are examples of what Bold Claims are are:\*\* 

"The truth is, not knowing this could be your biggest mistake\."

"Success is simpler than you think – here's why\."

"You've been doing it wrong all this time – learn the right way\."

"The truth about success will shock you\."

"You won’t believe how easy it is to transform your life\."

"YOU CAN'T BE SUCCESSFUL IF YOU KEEP LYING TO YOURSELF\."

\*\*Contrasts and Comparisons:\*\*

Highlighting the differences between two scenarios to emphasize a point to clarify and strengthen your argument\. Compare current situations with potential outcomes or past failures with future successes\.

\*\*Here are examples of what Contrasts and Comparisons Phrases are are:\*\* 

"On the other hand, what if there was a better way to do this?"

"Unlike those who act, those who hesitate risk losing everything\."

"COMPARED TO LIVING IN DENIAL, ACCEPTING YOUR TRUTH WILL BRING PEACE\."

\*\*Encouraging Change:\*\*

Motivating the viewer to adopt a new perspective or behavior\. The goal is to prompt personal growth and action\. Challenge the viewer to reflect and make positive changes\.

\*\*Here are examples of what Encouraging Change Phrases are are:\*\* 

"IT'S TIME TO ALIGN YOUR ACTIONS WITH YOUR BELIEFS\."

"You need to rethink your financial strategy to avoid future hardships\."

"Challenge yourself to become the person you've always wanted to be\."

\*\*Persuasion Tactics\*\*

\*\*Problem Amplification:\*\* The problem amplification persuasion strategy works by exploiting various emotional triggers and cognitive biases to exaggerate the perceived severity or urgency of a particular issue or problem\. This strategy often relies on amplifying fears and anxieties related to a specific problem or threat\. By presenting worst\-case scenarios, vivid examples, or alarming statistics, it can evoke feelings of fear and anxiety in the audience\. The strategy may also amplify feelings of anger and outrage towards perceived causes, perpetrators, or entities associated with the problem\. This emotional arousal can create a sense of moral urgency and a desire for swift action or retribution\. People tend to give more weight and attention to negative information or events compared to positive or neutral ones\. The problem amplification strategy uses this bias by focusing on the negative aspects or consequences of the issue\.

The problem amplification persuasion strategy can be effective in garnering attention, raising awareness, and mobilizing action for positive impact\.

\*\*Favorable Evidence:\*\* The favorable evidence persuasion strategy works by leveraging several emotional triggers and cognitive biases that shape human decision\-making and belief formation\. The favorable evidence strategy provides a steady stream of emotionally resonant "proof" that aligns with the audience's preconceptions, triggering feelings of validation and reinforcement\.

By selectively presenting evidence that highlights potential threats or risks, the strategy can evoke feelings of fear and anxiety\. Favorable evidence can be curated to provoke feelings of anger or outrage towards perceived adversaries or injustices\. This emotional arousal can lead to a stronger attachment to the narrative being presented, as it aligns with the audience's sense of moral righteousness\.

People tend to gravitate towards information that aligns with their existing beliefs\. The favorable evidence strategy takes advantage of this bias by consistently presenting a one\-sided perspective, reinforcing the audience's existing worldview\.

When making decisions or forming judgments, people tend to rely on information that is readily available or easily recalled\. By repeatedly exposing the audience to favorable evidence, the strategy increases the availability and accessibility of those specific examples or narratives\.

\*\*Black and White Philosophy:\*\* The Black and White Fallacy persuasion strategy works by presenting issues or arguments in an oversimplified, dichotomous manner, reducing complex situations to a stark choice between two opposing extremes\. The Black and White Fallacy strategy often relies on evoking fear or anxiety by presenting one of the extremes as a dire threat or consequence\. By amplifying these negative emotions, it can make the alternative extreme appear more appealing or necessary\. This strategy can also trigger a sense of moral certainty or righteous indignation by portraying one extreme as the morally superior or virtuous choice, and the other as morally reprehensible\. The Black and White Fallacy persuasion strategy can be effective in simplifying complex issues and eliciting emotional responses\.

\*\*The Challenger:\*\* The Challenger persuasion strategy works by encouraging people to question their current situation, beliefs, or circumstances\. It aims to create a sense of dissatisfaction or doubt, which can then be leveraged to introduce alternative perspectives or solutions\. By posing thought\-provoking questions or presenting contradictory information, the Challenger strategy triggers a sense of curiosity and intrigue in the audience\. This emotional response can motivate people to seek more information and be more open to alternative viewpoints\.

The strategy may highlight flaws, shortcomings, or unfulfilled desires in the audience's current situation or beliefs\. By amplifying feelings of dissatisfaction or frustration, it can create a desire for change or improvement, making people more receptive to new perspectives or solutions\.

The Challenger persuasion strategy can be effective in encouraging critical thinking, promoting personal growth, and introducing new ideas\.

\*\*Warren's Principle, also known as the 5 Persuasion Phrases, is a concept in persuasive communication\. Here's an explanation of each phrase type with examples:\*\*

\*\*Encourage Dreams phrases \(Warren's Persuasion Principle\):\*\*

These phrases inspire hope and motivate people by appealing to their aspirations and ambitions\. They help the audience envision a better future and align their dreams with the speaker's message\.

Examples:

"Imagine a world where\.\.\."

"What if you could\.\.\."

"Think about how amazing it would be if\.\.\."

"Picture yourself achieving\.\.\."

"Wouldn't it be incredible if\.\.\."

\*\*Justify Failures phrases  \(Warren's Persuasion Principle\):\*\*

These phrases help people feel better about past failures, reducing guilt and encouraging them to move forward\. 

Examples:

\- "Everyone faces setbacks; it's part of the learning process\."

\- "You didn't fail; you found a way that doesn't work\."

\- "That experience has made you stronger and wiser\."

\- "Sometimes, things don't work out for reasons beyond our control\."

\- "Every 'failure' is just a stepping stone to success\."

\*\*Allay Fears phrases  \(Warren's Persuasion Principle\):\*\*

Phrases designed to alleviate the audience's anxieties and concerns, providing reassurance and a sense of safety\.

Examples:

"There's no need to worry because\.\.\."

"We've got your back\.\.\."

"You are not alone in this\.\.\."

"Everything is under control\.\.\."

"Rest assured, you are in good hands\.\.\."

\*\*Confirm Suspicions phrases  \(Warren's Persuasion Principle\):\*\*

These phrases validate people's existing beliefs or doubts, making them understood and more receptive to your message\. 

Examples:

\- "You're right to be cautious; it's important to make informed decisions\."

\- "Your instincts about the market trends are spot\-on\."

\- "I agree, the current system does have its flaws\."

\- "You've clearly done your research on this topic\."

\- "Your concerns about the competition are well\-founded\."

\*\*Throw Rocks at Their Enemy phrases  \(Warren's Persuasion Principle\):\*\*

These phrases identify a common adversary or problem, uniting the speaker and listener against it\. 

