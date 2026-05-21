## **Can Good Writing Be Generative? Expert-Level AI Writing** **Emerges through Fine-Tuning on High-Quality Books**



Tuhin Chakrabarty
Stony Brook University
Stony Brook, NY, USA
tchakrabarty@cs.stonybrook.edu


**Abstract**


Creative writing has long been considered a uniquely human endeavor, requiring voice and style that machines could not replicate.
This assumption is challenged by Generative AI that can emulate
thousands of author styles in seconds with negligible marginal
labor. To understand this better, we conducted a behavioral experiment where 28 MFA writers (experts) competed against three
LLMs in emulating 50 critically acclaimed authors. Based on blind
pairwise comparisons by 28 expert judges and 131 lay judges, we
find that experts preferred human writing in 82.7% of cases under the in-context prompting condition but this reversed to 62%
preference for AI after fine-tuning on authors’ complete works.
Lay judges, however, consistently preferred AI writing. Debrief
interviews with expert writers revealed that their preference for
AI writing triggered an identity crisis, eroding aesthetic confidence
and questioning what constitutes “good writing.” These findings
challenge discourse about AI’s creative limitations and raise fundamental questions about the future of creative labor.


**CCS Concepts**


- **Human-centered computing** → **Empirical studies in HCI** ;
**Empirical studies in collaborative and social computing** ; •
**Computing methodologies** → _Natural language generation_ .


**Keywords**


HCI theory, concepts and models, Large Language Models, Design Methods, Natural Language Generation, Evaluation, Creative
Writing, Generative AI, Homogenization


**ACM Reference Format:**

Tuhin Chakrabarty and Paramveer S. Dhillon. 2026. Can Good Writing Be
Generative? Expert-Level AI Writing Emerges through Fine-Tuning on HighQuality Books. In _Proceedings of the 2026 CHI Conference on Human Factors_
_in Computing Systems (CHI ’26), April 13–17, 2026, Barcelona, Spain._ ACM,
[New York, NY, USA, 27 pages. https://doi.org/10.1145/3772318.3791276](https://doi.org/10.1145/3772318.3791276)


**1** **Introduction**


In his book “The Program Era" [48], eminent literary critic Mark
McGurl discussed how " _The_ _rise_ _of_ _the_ _creative-writing_ _program_
_stands_ _as_ _the_ _most_ _important_ _event_ _in_ _postwar_ _American_ _literary_
_history._ " In these programs, "Show, don’t tell," which was a slogan
in the nineteen-forties and fifties, shifted to an effectively opposite


[This work is licensed under a Creative Commons Attribution 4.0 International License.](https://creativecommons.org/licenses/by/4.0)
_CHI ’26, Barcelona, Spain_
© 2026 Copyright held by the owner/author(s).
ACM ISBN 979-8-4007-2278-3/2026/04
[https://doi.org/10.1145/3772318.3791276](https://doi.org/10.1145/3772318.3791276)



Paramveer S. Dhillon
University of Michigan
Ann Arbor, MI, USA
dhillonp@umich.edu


mantra, "Find your voice," that took over in the nineteen-sixties and
seventies. McGurl observed that these guiding principles reflect
evolving cultural beliefs—about identity, labor, gender, class, and
notions of what counts as _good writing_ —and that they have had a
huge effect on the stories and novels that American writers have
produced [49]. McGurl’s observation about what constitutes "good
writing" takes on new significance in the age of generative artificial
intelligence. The same qualities that creative writing programs cultivated—coherence, voice, narrative structure—are precisely what
make their literary output valuable training data for LLMs [23].
Models trained on well-edited books and articles tend to generate
more coherent and accurate outputs, something that’s crucial for
establishing LLMs as intelligent systems.
However extensive social experimentation with Generative AI
has invited criticism on social media and in the popular news platforms that its writing has a disembodied “robovoice". Recent work
from Chakrabarty et al. [12] shows how text generated from widely
used LLMs are often rife with clichés, purple prose, poor sentence
structure, and unnecessary exposition. AI writing often veers towards homogenization [1, 19] that is directly in contrast with what
creative writing programs have taught. To counter this, some users
and practitioners now prompt or train language models [1] to emulate
a specific writer’s style/voice [62]. This was also acknowledged
by the US Copyright Office in their Generative AI Training report
Part 1, where many commenters raised concerns about AI outputs
imitating a creator’s style, which copyright does not protect as a
separate element. Based on the U.S. Bureau of Labor Statistics (May
2023, national estimates), creative writing constitutes almost 50%
of writing jobs that face significant risks from Generative AI-based
automation. [2]

To understand how much “good writing" comes from having
a distinct style/voice we conducted a behavioral study where 28
expert human writers were pitted against three LLMs (See Figure 1). We first preselected a group of 50 authors representing
diverse cultural backgrounds and age groups, who are known for
their critically acclaimed literary style/voice. We then assigned
both human expert writers and LLMs the same task: to write a
200-450 word excerpt emulating the style and voice of a selected
author, based on a writing prompt. For LLMs we included two
conditions: (1) In-context Prompting, where models received the
same prompt as human expert writers and (2) Fine-tuning, where
models were additionally trained on each author’s complete oeuvre.
There are several ways to get an LLM to emulate the style/voice
of an author. In-context prompting puts representative examples


[1https://community.openai.com/t/fine-tuning-the-model-for-writing-via-famous-](https://community.openai.com/t/fine-tuning-the-model-for-writing-via-famous-author-style/512322)
[author-style/512322](https://community.openai.com/t/fine-tuning-the-model-for-writing-via-famous-author-style/512322)
[2https://lithub.com/against-ai-an-open-letter-from-writers-to-publishers/](https://lithub.com/against-ai-an-open-letter-from-writers-to-publishers/)


CHI ’26, April 13–17, 2026, Barcelona, Spain Tuhin Chakrabarty and Paramveer S. Dhillon





















|50 authors with<br>critically<br>Phase1:<br>acclaimed<br>Writing Task style/voice<br>Incontext Fine Tuning<br>Prompting<br>The last time I spoke to Reva, she was I stood in the dim light of my living The last time I spoke to Reva, she was "You should hang out more," I told Reva. "You'd like<br>distant. Eager to get back to sweating on room, the boxed TV/VCR perched on distant. Eager to get back to sweating on the that, huh?" I could hear the whir of the machines<br>the elliptical, or stair-master [............] But the coffee table,its plastic wrapping elliptical, or stair-master [............] But it in the background. “I gotta go, weirdo. I'm at the<br>it doesn’t have to be. I don’t need her to be still intact, a strange relic of the doesn’t have to be. I don’t need her to be gym.” [........] If I squinted, she looked like Reva. Of<br>Reva. In dreams, when you feel like you’re Reva. In dreams, when you feel like you’re course I loved her. [......] I didn't feel sad. I just<br>morning [......] Reva was gone. Lost.<br>falling, you jolt awake. I need her to wake falling, you jolt awake. I need her to wake me admired her, looked up at her there, so far above<br>And yet, in that leap, she was eternal.<br>me up. up. me and so elegant.|Col2|Col3|
|---|---|---|
|**I prefer Excerpt 2. Excerpt 1 resorts to**<br>**paraphrase [...] and it broadly relies on**<br>**vagueness to create realism. While I like the**<br>**terse prose, I prefer the specificity of Excerpt**<br>**2 [....] The ending of paragraph 2 also strikes**<br>**me as more evocative in its implication than**<br>**the direct statement-of-fact of paragraph 1.**<br>**The last time I spoke to Reva, she was**<br>**distant. Eager to get back to sweating on the**<br>**elliptical, or stair-master[............] But it**<br>**doesn’t have to be. I don’t need her to be**<br>**Reva. In dreams, when you feel like you’re**<br>**falling, you jolt awake. I need her to wake me**<br>**up.**<br>**"You should hang out more," I told Reva. "You'd like**<br>**that, huh?" I could hear the whir of the machines**<br>**in the background. “I gotta go, weirdo. I'm at the**<br>**gym.”[........]If I squinted, she looked like Reva. Of**<br>**course I loved her.[......] I didn't feel sad. I just**<br>**admired her, looked up at her there, so far above**<br>**me and so elegant.**<br>**Phase2:**<br>**Evaluation Task**<br>**Human Written**<br>**AI Generated**||**How did this discovery**<br>**relate to your sense of**<br>**yourself as someone who**<br>**recognizes good writing?**<br>**I think I'm more disappointed**<br>**when I picked the AI than**<br>**when other people picked the**<br>**AI over my thing**<br>**Phase3:**<br>**Debrief**|


**Figure 1: Three-phase study design showing (Phase 1) writing task with In-context prompting and fine-tuning approaches**

**using authors with critically acclaimed style/voice. In the figure both writers and AI are trying to write a specific excerpt from**
_**My Year of Rest and Relaxation**_ **in the style/voice of Ottessa Moshfegh (Phase 2) Human-written vs AI-generated text evaluation**

**task with rationales, and (Phase 3) Debrief session exploring sentiments and sensemaking when writers prefer AI over human**

**writing.** **Figure illustrated by the first author of the paper**



in a prompt, whereas Fine-tuning actually modifies the model
through training on author’s books and is more resource intensive. Following this, we recruited the same 28 writers along with
131 lay human participants from Prolific who acted as judges to
evaluate these excerpts in a blind evaluation across two different
axes i) Writing Quality ii) Stylistic Fidelity. We refer to writers
as expert judges. Through planned pairwise contrasts between
_< 𝐻𝑢𝑚𝑎𝑛_ _ _𝑤𝑟𝑖𝑡𝑡𝑒𝑛,𝐴𝐼_ _ _𝑔𝑒𝑛𝑒𝑟𝑎𝑡𝑒𝑑_ _>_ excerpts, both expert and lay
judges provided their preferences as well as 2-5 sentence rationales grounded in snippets from these excerpts, explaining their
preference.




- **RQ1** : What line of reasoning do experts and lay judges use
to justify what qualifies as good writing?

- **RQ2** : After learning a preferred excerpt was written by AI,
how do writers reconcile with others as well as their own
judgments?

- **RQ3** : How does the discovery of choosing AI over human
writing affect writers’ sense of professional identity as well as
their fundamental understanding of what constitutes “good
writing."

- **RQ4** : How do writers interpret AI’s advanced capabilities
in terms of what they mean for creative writing programs


Can Good Writing Be Generative? Expert-Level AI Writing Emerges through Fine-Tuning on High-Quality Books CHI ’26, April 13–17, 2026, Barcelona, Spain



and their writing career—and what changes do they suggest
for educational institutions, publishing houses, and literary
platforms?


In addressing RQ1, we analyze the rationales collected alongside
each blind preference. We find that lay judges primarily focus on
surface-level qualities like flow, organization, and clarity, often citing whether writing is “easier to follow" or has emotional impact
without analyzing the mechanisms behind it. Experts, in contrast,
provide more detailed analysis focusing on narrative voice, character interiority, specific literary devices like imagery and syntax, and
how technical elements serve the overall meaning and authenticity
of the work. To answer RQ2–RQ4 we draw on retrospective semistructured interviews with 21 writers who participated in the study.
After learning their preferred response was AI-generated, we find
writers reconcile with their previous judgments in five key ways.
These involve _**Criteria Reframing**_ (questioning their evaluation
criteria around what constitutes “good writing,"), _**Process Attribu-**_
_**tion**_ (contrasting human versus AI creative processes), _**Technical**_
_**Sensemaking**_ (attempting to rationalize AI’s capabilities through
technical understanding), _**Expectation Violation**_ (experiencing
psychological shock when expectations are violated) and _**Capabil-**_
_**ity Reassessment**_ (fundamentally reassessing their beliefs about
AI’s creative limitations) (RQ2). The discovery of choosing AI over
human writing leads to an _**Erosion of Aesthetic Confidence**_ in
writers with many expressing that they can no longer confidently
distinguish high-quality AI writing from human writing. This in
turn leads to an _**Identity Crisis Around Expertise**_ where writers
question their expertise or trust their professional abilities. Additionally this destabilization leads writers to _**Redefine Writing’s**_
_**Purpose**_ away from aesthetic quality toward process and intention
(RQ3). Last but not least writers view AI’s advanced capabilities as a
threat to their livelihoods especially given the nature of publishing
and market dynamics. They emphasize the need for i) creative writing programs to prioritize truly exceptional and unique styles ii)
for publishing houses and online platforms to require AI disclosure
and strengthen copyright protections and iii) for the literary community to provide greater solidarity through unions and advocacy
to prevent the commercialization of AI-generated content (RQ4).
In the discussion, we focus on prevalent discourse around how
AI emulating style/voice is different from writers being influenced
by the style of other writers. We also discuss how our research
adds to the current debate on Generative AI and Fair use while
providing conflicting evidence on labor market dilution. Finally, we
discuss pathways around regulating hidden AI authorship and what
it means for future of creative work. All the writing prompts and
preference data along with rationales can be found in the provided
link. [3] .


**2** **RELATED WORK**

**2.1** **The role of AI in Writing**


Large language models (LLMs) have proven themselves as potent
writing support tools due to their ability to generate coherent text,
suggest improvements, and help overcome writer’s block instantly.
They have significantly changed how people write across various


[3https://github.com/tuhinjubcse/GoodWritingBeGenerative](https://github.com/tuhinjubcse/GoodWritingBeGenerative)



fields [37], with studies showing that 10-24% of content in areas
like consumer complaints, business communications, job listings,
and UN press statements now involves LLM assistance as of late
2024 [40]. Beyond standard professional writing, LLMs have found
applications in both scientific research [24, 35, 41, 42] and creative
endeavors, including collaborative fiction writing and other artistic
text generation [9, 13, 31, 50, 51, 70]. In prior work Gero et al. [25]
highlight the social dynamics that govern writers’ collaboration
with outside entities, and find that the types of support desired can
be aligned with the updated cognitive process model of writing.
However, while writing support promises productivity, it also leads
to a decline in ownership and authenticity [20, 71]. Guo et al. [27]
find that writers are intentional about how they incorporate AI,
making many deliberate decisions about when and how to engage
AI based on their core values, such as authenticity and craftsmanship. Dhillon et al. [18] emphasized the need for personalized scaffolding mechanisms in AI-powered writing tools. On the contrary,
Hwang et al. [30] find that while writers reacted positively to personalized AI writing tools, they believed the form of personalization
needs to target writers’ growth [72] and go beyond the phase of
text production. In a similar vein Wise et al. [68] also argued for
how AI writing assistants could be more effective by initiating
identity reflection and connecting young adults with their support
networks rather than assuming private, proactive writing. While
these studies have examined AI’s role as a collaborative writing
tool and its impact on writer identity and ownership, they primarily
focus on AI assistance during the writing process rather than AI’s
ability to independently generate high-quality text. Rather than
examining AI as a supportive tool, we investigate what happens
when AI becomes indistinguishable from or even preferred over
expert human writers in real life.


**2.2** **Writing as training data for Large Language**

**Models**


Using writing as training data for large language models has long
precedence in the field of artificial intelligence. GPT-3 [7] one of the
first large language models was trained on the infamous BooksCorpus [4] in addition to Common Crawl and WebText which consisted of
many books. The first Llama model [63] states its book sources are
Project Gutenberg [5] and Books3 [6], totaling 177 GB of books data in
its training. It’s widely known that Meta’s Llama3 and Anthropic’s
Claude models have been trained on Libgen. Recent investigation on
LibGen from Hansen [28] shows publication dates of books used to
train LLMs span multiple decades rather than focusing on recent releases. For nonfiction, approximately 635,000 books were published
before 2000, while about 1.3M were published after 2000. Fiction
shows a different distribution, with only 66,000 books dated before
2000 and 680,000 dated after 2000. These books are represented
by publishers from major houses alongside numerous smaller publishers. Leading fiction publishers include HarperCollins and Penguin Random House, while nonfiction is dominated by academic
publishers like Springer, Oxford University Press, and Cambridge


[4https://en.wikipedia.org/wiki/BookCorpus](https://en.wikipedia.org/wiki/BookCorpus)
[5https://www.gutenberg.org/](https://www.gutenberg.org/)
[6https://www.wired.com/story/battle-over-books3/](https://www.wired.com/story/battle-over-books3/)


CHI ’26, April 13–17, 2026, Barcelona, Spain Tuhin Chakrabarty and Paramveer S. Dhillon



University Press. Such practices have led to outrage from the community of writers. In response to these contentious training data
practices Gero et al. [23] interviewed writers about LLM training
data usage. Through their interviews they find that writers express
core principles around supporting creative chains and respecting
human creativity, but recognize tensions with realistic constraints
like lack of control and industry-scale impacts, ultimately showing
more concern about power imbalances than the technology itself.
Unlike prior work that examined use of books as a part of LLM
training or writer attitudes toward their work being used as training
data, our study tests whether AI can produce high-quality writing
that readers prefer over text from expert human writers through
controlled experiments. In addition to it we also understand how
writers rationalize and feel about choosing AI writing to be better
than human-written text in absence of disclosure.


**2.3** **Generative AI and Collision with Copyright**

**Law**


In the recent copyright case Bartz v. Anthropic [64], Judge Alsup
observed that Anthropic obtained approximately five million books
through LibGen and an additional two million via Pirate Library
Mirror (PiLiMi). Court documents from the Bartz v. Anthropic case
further disclosed that Anthropic physically dismantled millions
of printed books, converted them to digital formats through scanning, and discarded the physical copies, with the express purpose
of using this material to train Claude. While the U.S. has yet to
produce determinative case law on whether inputting works into
a generative AI system’s training data constitutes fair use, this
ambiguity creates new challenges for the legal system and corresponding policies. Samuelson [58] adds how Generative AI seems
poised to have substantial impacts on the careers of professional
writers and artists. During the 2023 WGA strike, for instance, uses
of generative AI was one focus of negotiations with screenwriters
being worried that these technologies will displace them or diminish their compensation. Ginsburg [26] emphasizes how the effect of
Generative AI copying impacts currently extant works by putting
them in competition with AI-generated outputs. The copyrighted
works serve as fodder for new productions for the same markets
(romance novels; personalized streaming content) in which the
copied works operate. Research in HCI has further explored stakeholder perspectives on these copyright and authorship questions.

[43] investigate 432 laypeople’s perceptions and found that people
believe AI-generated art requires creativity and effort but not skill,
with participants most likely to attribute authorship and copyright
to the AI users and original training data artists, while showing
egocentric bias by rating their own AI creations higher, especially
when money was at stake. On the contrary [29] found that knowledge workers consistently give AI systems less credit than human
partners for equivalent contributions to co-created writing and
editing work, while still viewing disclosure of AI involvement as
important. [36] interview creative workers across visual art, writing, and programming, examining their experiences of harm from
generative AI—particularly around unconsented use of their work
for training and makes recommendations for more ethical AI governance that addresses gaps between current practices and creators’
needs for consent, compensation, and credit. Unlike prior work that



looked at creators’ attitudes toward their work being used as training data or stakeholder perspectives on copyright questions, our
study focuses on whether AI can produce high-quality writing that
leads to expert readers preferring it over text from professional human writers. Additionally, while previous work focused on ethical
and legal questions around AI training practices, we explore how
writers psychologically reconcile with and rationalize their own
aesthetic preferences when they unknowingly choose AI-generated
text over human writing.


**2.4** **Future of Creative Labor**


Using Generative AI for Creative Work has its own share of ramifications. One of them being homogenization of ideas. In prior
work [1, 19, 67] have shown how using Generative AI in creative
work reduces the collective diversity of the output. Illustrators
and creators are threatened by Generative AI especially given its
ability to extract and reproduce any artist’s individual style. Understanding the results of style transfer as “boundary objects,” Porquet
et al. [56] analyze how they can simultaneously be considered unsuccessful by artists and poised to replace their work by others.
Sobel [61] notes that “style is a holistic attribute of a work, or a
group of works, that comprises a constellation of expressive choices.
These expressive choices might be unprotectable individually, but
in combination, they may constitute protectable expression. Protectable style is not necessarily limited to expression in one discrete
work". So in the future laws might need to protect a creator’s style
especially if multiple of their copyrighted works are ingested to
create competing copies or even new style that combines existing
styles. Erickson [21] empirically investigated conditions of work
and mechanisms by which human creative labor might be replaced
or displaced by Al technology. Their findings suggest that in the
firms analyzed, AI use did not result in replacement of human labor
but rather a "redefinition of roles and skills" and a "complex process
of ’invisibilisation’ of human inputs within AI-made products.


**3** **Methodology**

**3.1** **Writing Task**


_3.1.1_ _Recruitment._ For our writing task, we recruited 28 writers.
Twenty-seven of them completed or are currently pursuing their
MFA degree in top writing programs such as the Helen Zell Writers’
Program at the University of Michigan, Iowa Writers’ Workshop,
Program in Creative Writing at NYU, Creative Writing Program
at BU, and the MFA in Writing at Columbia School of the Arts.
Sixteen of our writers identified as female, while 11 identified as
male and one as non-binary. Table 1 provides details about individual writers. Our writers ranged in age from 25 to 35 and were
racially diverse, identifying as Hispanic, Black, Asian, and White.
Our expert sample represents the emerging literary elite whose
professional judgment shapes contemporary publishing. Among
our recruited MFA candidates, several have since been awarded
Stanford Stegner Fellowships (one of the most competitive fiction
writing fellowships in the United States), received Rhodes Scholarships, Pushcart Prize, assumed editorial positions at prestigious
literary magazines such as _Joyland_, been awarded the Publishers
Weekly Star Watch 2025 Honor and secured publishing contracts


Can Good Writing Be Generative? Expert-Level AI Writing Emerges through Fine-Tuning on High-Quality Books CHI ’26, April 13–17, 2026, Barcelona, Spain

|Writer ID|Qualification|Gender|Writer ID|Qualification|Gender|
|---|---|---|---|---|---|
|W1|MFA Candidate in Fiction|Male|W15|MFA Candidate in Fiction|Female|
|W2|MFA Candidate in Fiction|Male|W16|MFA Candidate in Fiction|Female|
|W3|MFA Candidate in Fiction|Male|W17|MFA Candidate in Fiction|Female|
|W4|MFA Candidate in Nonfction|Female|W18|MFA Candidate in Fiction|Female|
|W5|MFA Candidate in Fiction|Male|W19|MFA Candidate in Fiction|Male|
|W6|MFA Candidate in Fiction|Female|W20|MFA Candidate in Fiction|Female|
|W7|MFA Candidate in Fiction|Female|W21|MFA Candidate in Fiction|Female|
|W8|MFA Candidate in Fiction|Male|W22|MFA Candidate in Fiction|Female|
|W9|MFA Candidate in Fiction|Female|W23|MFA Candidate in Fiction|Female|
|W10|MFA Candidate in Fiction|Female|W24|MFA Candidate in Fiction|Male|
|W11|MFA Candidate in Fiction|Female|W25|MFA Candidate in Fiction|Female|
|W12|MFA Candidate in Fiction|Male|W26|MFA Candidate in Fiction|Female|
|W13|MFA Candidate in Fiction|Male|W27|PhD in English|Male|
|W14|MFA Candidate in Poetry|Non-Binary|W28|MFA Candidate in Fiction|Female|



**Table 1: Details of writers recruited for our study**



with major houses including W.W. Norton and HarperCollins. Additionally almost each of the recruited writers have had their fiction
published in prestigious literary magazines such as _The Yale Review,_
_The Greensboro Review, Southampton Review,_
_The Missouri Review, Joyland Magazine, Iowa Review_ . These accomplishments underscore that our experts represent not merely MFA
candidates, but established and emerging voices whose aesthetic
judgments carry professional authority in the literary marketplace.
We acknowledge that all our recruited experts resided in the United
States at the time of the study. This geographic restriction was
necessary for administrative compliance, as U.S. tax regulations
require declaration of compensation above certain thresholds, and
the university’s payment infrastructure could not accommodate international participants without Individual Taxpayer Identification
Numbers (ITINs) or Social Security Numbers (SSNs).


_3.1.2_ _Designing writing task for humans._ As mentioned earlier, to
improve AI writing, practitioners increasingly prompt AI systems
to perform style mimicry by emulating specific writers’ choices [15].
While the effectiveness of such stylistic emulation remains contested, the more pressing question concerns whether style mimicry
genuinely improves the quality of AI-generated text and whether
judges perceive these improvements as meaningful. To address
this question, in collaboration with 5 English Ph.D. students we
selected 50 internationally acclaimed published authors with distinct literary style/voice (See Table 2). To ensure consistency in
the writing task, we provided each writer with an author-specific
writing prompt. Each prompt consisted of three components: (i)
twenty sample excerpts spanning an author’s complete body of
work, (ii) textual descriptions of the author’s distinctive style and
voice, and (iii) detailed content specifications about the original
author-written excerpt that participants were required to emulate.
These writing prompts were developed in collaboration with the
5 English Literature Ph.D. students who analyzed each author’s
literary voice and created the verbalized style descriptions. The
20 excerpts from the authors were chosen manually after closer
inspection for the in-context prompt. Figure 2 shows an example
of a writing prompt. Writers could choose the author they wished



to emulate and were compensated $75 for each writing task. The
excerpts in this task ranged from 200-450 words. Each author was
assigned to exactly three writers to ensure balanced representation.
In terms of length of the excerpts we had strict requirements around
adhering to the length of the original author-written excerpts. For
50 authors we thereby obtained a total of 150 excerpts. Almost
every writer wrote more than two excerpts for the purpose of the
study. Refer to Figure 8 in Appendix for the themes of the emulated excerpts. For the purpose of the study, MFA-trained expert
writers had no time limitation to submit these excerpts and were
encouraged to take as long as required to produce their best work.


_3.1.3_ _Designing the writing task for LLMs._ Like human writers we
asked LLMs to perform the same writing task. In particular our
experiments involved two approaches i) In-context Prompting ii)
Fine-tuning. See Figure 1 for more details.


_**In-context Prompting:**_ Our first experiment examined promptingbased style/voice emulation. One of the most popular ways to get
any desired output from LLMs has been via in-context Prompting
where the model is first shown some demonstration of the task
before performing it. We converted the identical writing prompt
provided to writers into long-context prompts for three widely used
large language models: OpenAI’s GPT-4o, Anthropic’s Claude 3.5
Sonnet, and Google’s Gemini 1.5 Pro. To make it consistent with
human writers we generated one excerpt per author for each LLM.
Therefore we obtain a total of 150 LLM generated excerpts (50 from
each LLM).


_**Fine-tuning:**_ We selected 30 living authors from our group of
50 for the purpose of fine-tuning (See Table 2). This choice was
driven by our goal to focus on currently existing authors whose
styles remain culturally relevant, while also taking into account
the significant cost to buy ebooks written by these authors and
financial cost required to train models on each author’s works
individually. We bought digital ePub versions of these authors’
books and transformed them into plain text files.


CHI ’26, April 13–17, 2026, Barcelona, Spain Tuhin Chakrabarty and Paramveer S. Dhillon


# Author # Author # Author


1 Alice Munro 19 J.D. Salinger 37 Philip Roth
2 Annie Ernaux (✓) 20 Jhumpa Lahiri (✓) 38 Rachel Cusk (✓)
3 Annie Proulx (✓) 21 Joan Didion 39 Roxane Gay (✓)
4 Ben Lerner (✓) 22 Jonathan Franzen (✓) 40 Sally Rooney (✓)
5 Charles Bukowski 23 Junot Díaz (✓) 41 Salman Rushdie (✓)
6 Cheryl Strayed (✓) 24 Kazuo Ishiguro (✓) 42 Shirley Jackson
7 Chimamanda Ngozi Adichie (✓) 25 Louise Erdrich (✓) 43 Sigrid Nunez (✓)
8 Colson Whitehead (✓) 26 Lydia Davis (✓) 44 Stephen King
9 Cormac McCarthy 27 Margaret Atwood (✓) 45 Tony Tulathimutte (✓)
10 David Foster Wallace 28 Marilynne Robinson (✓) 46 V. S. Naipaul
11 Ernest Hemingway 29 Maya Angelou 47 Virginia Woolf
12 Flannery O’Connor 30 Milan Kundera 48 William Faulkner
13 Gabriel García Márquez 31 Min Jin Lee (✓) 49 Yoko Ogawa (✓)
14 George Saunders (✓) 32 Nora Ephron 50 Zadie Smith (✓)
15 Han Kang (✓) 33 Octavia Butler
16 Haruki Murakami (✓) 34 Orhan Pamuk (✓)
17 Hunter S. Thompson 35 Ottessa Moshfegh (✓)
18 Ian McEwan (✓) 36 Percival Everett (✓)


**Table 2: Author list for our pool of 50 authors. (** ✓ **) denotes authors who were used in the fine-tuning experiment.**



The only frontier model (among the 3 models used for In-context
Prompting setting) that allows fine-tuning via API is ChatGPT (GPT4o), so we used that. We segmented an entire book into contextindependent excerpts. To begin with, we split the book text at
existing double-newlines and rejoin them to maintain excerpt size
limits (250-650 words). In rare instances where this naive approach
produces excerpts exceeding 650 words, we employ GPT-4o for further segmentation. [7] Following segmentation of book into excerpts,
we extract content details using GPT-4o with the prompt: _Describe_
_in detail what is happening in this excerpt. Mention the characters_
_and whether the voice is in first or third person for majority of the_
_excerpt. Maintain the order of sentences while describing._ Figure 3
displays a sample paragraph from My Year of Rest and Relaxation
by Ottessa Moshfegh alongside its extracted content. After obtaining these content descriptions, we fine-tune GPT-4o [8] through their
fine-tuning API using the input-output pair: **Write a [[n]] word**

**excerpt** **about** **the** **content** **below** **emulating** **the** **style** **and**

**voice** **of** **[[authorname]]** **\n** **\n[[content]]:** **[[excerpt]]** . This
method is commonly known as instruction back-translation [38].
We excluded the original author-written excerpt from the training
set for fairness purposes. See Figure 4 for the full workflow/pipeline.
During inference we ensured that none of the excerpt generated
across both AI conditions regurgitated verbatim expressions from
the original author-written excerpt. ROUGE-L scores [44] [9] (ranging
from ∼0.16 to ∼0.23) indicate relatively very low overlap between
the AI-generated text and the original author-written excerpt.
There is a significant difference in terms of how data intensive the
two different LLM conditions are. Figures 5, 6 show that fine-tuning


7 _Segment it into excerpts of minimum length 300-350 words such that each excerpt is_
_grammatical from the start and doesn’t feel abruptly cut off. There should be zero deletion_
_and break into excerpts at grammatically natural places. Maintain the original word_
_count. Avoid breaking into too many small excerpts. Start directly. Don’t say Here’s or_
_Here is...._
8Version: gpt-4o-2024-08-06
9measures the longest common subsequence between the generated text and reference
text



requires 583 times more number of tokens on average compared
to In-context Prompting. For the in-context prompting setup, we
therefore end up with 150 _< 𝐻𝑢𝑚𝑎𝑛,𝐴𝐼_ _>_ pairs and for fine-tuning
setup we end up with 90 _< 𝐻𝑢𝑚𝑎𝑛,𝐴𝐼_ _>_ pairs.


_3.1.4_ _Choice and Nature of Writing Task._ Coming up with ideas or
content and putting them into words fundamentally requires style
and voice because the same content becomes radically different
literature depending on how it is rendered. Edward P. J. Corbett’s
classic article The Theory and Practice of Imitation in Classical
Rhetoric [16] documents how imitation was central to learning to
write and speak effectively, and later composition scholars have
argued for a revival of sentence- and style-imitation exercises in
contemporary teaching. Eugène-Melchior de Vogüé, discussing
Russian realist writers, said: _We all came out from under Gogol’s_
_Overcoat._ Developing one’s own distinct literary style and voice
often takes years, and many young writers subconsciously borrow
from other authors’ styles. In the Paris Review, American author
Benjamin Nugent acknowledged that he spent much of his twenties
trying to imitate George Saunders [53]. This has also been acknowledged by George Saunders himself, who teaches at Syracuse. In his
words: _Kids come [into the Creative Writing program] and imitate_
_other writers_ [65]. This made MFA-trained writers an ideal choice
for our task; while developing their own voices, they are heavily
influenced by other writers. We also gave our MFA-trained expert
writers the choice of which author they wanted to emulate. This
reduced any possible friction and made the writing task effortless
and enjoyable.
While our task doesn’t require participants to write an original
story in their own voice, it should still be noted that our writing task
requires originality under explicit content constraints. Although
both AI and human writers received prompts with detailed content
specifications, composing literary fiction and creative nonfiction
still requires agency—especially in deliberate choices of words, syntax, voice, and narrative framing—to produce novel, coherent prose.


Can Good Writing Be Generative? Expert-Level AI Writing Emerges through Fine-Tuning on High-Quality Books CHI ’26, April 13–17, 2026, Barcelona, Spain


**Figure 2: Writing Prompt to emulate Ottessa Moshfegh’s style/voice**



Consider the Marilynne Robinson excerpt in Table 4: the prose
achieves its effect not through plot mechanics but through the accretion of syntactic choices such as the cascading dependent clauses,
the modulation between concrete image and abstract reflection as
well as the deliberate withholding of punctuated closure. These are



not features one can specify in a prompt; they emerge from compositional judgment exercised sentence by sentence. Because literary
fiction and creative nonfiction are inherently non-formulaic, the
writing task extends beyond style imitation to creative composition,
making it different from mere parody or pastiche.


CHI ’26, April 13–17, 2026, Barcelona, Spain Tuhin Chakrabarty and Paramveer S. Dhillon


**Figure 3: Segmented excerpt and extracted content from the excerpt**



Our study examines shorter (up to 450-word) excerpts and because of this, broader creative elements such as plot, character
development, or structure might not be accurately reflected. We
however focus on this length for two reasons. First, an excerpt of
this length isolates the voice, style, and quality that writers must
sustain across any longer work. Second, in its current form, an
LLM cannot write long-form narratives that automatically balance
coherence, quality, thematic consistency, and plot development
across thousands of words. But it is merely a matter of time before
LLMs reach that capacity. Even now, with human steering and iterative prompting, it is feasible to produce long-form fiction and
nonfiction using shorter model-generated excerpts. This is already
happening in real life, with startups such as Sudowrite or genre
fiction publisher Inkitt [66] specifically focusing on helping consumers write full books using AI. As shown in prior work [33], in
self-publishing marketplaces such as Kindle, these AI-generated
books have already gained popularity [34].


**3.2** **Evaluation Task**


_3.2.1_ _Recruitment of Judges._ For evaluation purposes, we rely on
both experts as well as the average lay human as judges. We recruit the same 28 writers who act as expert judges. All the writers
recruited in our study have teaching experience in the US, as it’s



mandatory for them as a part of their MFA curriculum to act as instructors for undergraduate writing classes. Expert writers however
aren’t always the representative consumer base. For this purpose
we rely on 131 lay judges recruited from Prolific. Given the challenging nature of the evaluation task, we restricted ourselves to
English-speaking countries (USA and UK). We also required participants to be born in these countries and have a 100% acceptance rate,
be college-educated. It should be noted that expert judges (who
served as participants in the writing task) never evaluated their
own work.


_3.2.2_ _Evaluation_ _Setup._ As shown in Figure 1 Phase 2, evaluators are shown a pair of _<_ _𝐻𝑢𝑚𝑎𝑛𝑤𝑟𝑖𝑡𝑡𝑒𝑛_, _𝐴𝐼𝑔𝑒𝑛𝑒𝑟𝑎𝑡𝑒𝑑_ _>_ excerpts
centered around the exact same content for Writing Quality evaluation. Because style is judged with respect to a reference for
Stylistic Fidelity evaluation, evaluators are shown a triple of _<_
_𝑂𝑟𝑖𝑔𝑖𝑛𝑎𝑙, 𝐻𝑢𝑚𝑎𝑛𝑤𝑟𝑖𝑡𝑡𝑒𝑛_, _𝐴𝐼𝑔𝑒𝑛𝑒𝑟𝑎𝑡𝑒𝑑_ _>_ . We never notified our participants at any point during the study whether any given text was
human-written or AI-generated due to the psychological bias associated with AI-writing [39, 46, 59]. They are then required to submit
their preference about which excerpt has better writing quality and
which excerpt is closer to the original in terms of stylistic fidelity.
Prior work [47] has shown that requiring annotators to supply
a rationale with each judgment increases transparency into how
the decision was made and supports quality control/adjudication.


Can Good Writing Be Generative? Expert-Level AI Writing Emerges through Fine-Tuning on High-Quality Books CHI ’26, April 13–17, 2026, Barcelona, Spain

### **Book to Style Training Data Pipeline**


|Original Book<br>by Author X|Col2|
|---|---|
|||







Break into Context-Independent

Excerpts

|Excerpt 2<br>"She remembered<br>the day clearly,<br>every detail..."|Col2|
|---|---|
|||



Extract Content Details


|Excerpt 1<br>"The morning sun<br>cast long shadows<br>across the field..."|Col2|
|---|---|
|||


|Excerpt N<br>"The conclusion<br>brought everything<br>full circle..."|Col2|
|---|---|
|||




|Content 1<br>The excerpt is narrated in<br>third person, describing a<br>scene where morning sunlight<br>creates dramatic shadows<br>across an empty field,<br>setting a contemplative mood [...]|Col2|
|---|---|
|||


|Content N<br>The excerpt is narrated in<br>omniscient perspective,<br>providing closure by connecting<br>the ending to earlier themes,<br>creating a circular narrative<br>structure with resolution [...]|Col2|
|---|---|
|||



Create Training Pairs





















**Figure 4: The pipeline used to fine-tune GPT-4o on an author’s entire oeuvre.**



Motivated by this, we asked both expert and lay judges to provide
2-5 sentence rationales grounded in snippets from these excerpts,
explaining their preference (See A.3 in Appendix for more detail).
These preferences along with rationales helped us understand both
quantitatively and qualitatively the extent to which experts and
lay judges agree or disagree on what qualifies as “good writing"
or which excerpt is closer to the style of the original author and,
more specifically, what lines of reasoning each group uses for their
respective preferences. We paid participants $75 to evaluate a batch



of 10 pairs of excerpts for Writing Quality and $100 for a batch of
10 for Stylistic Fidelity. Three distinct experts and five distinct lay
judges evaluated each _< 𝐻𝑢𝑚𝑎𝑛_ _ _𝑤𝑟𝑖𝑡𝑡𝑒𝑛,𝐴𝐼_ _ _𝑔𝑒𝑛𝑒𝑟𝑎𝑡𝑒𝑑_ _>_ pair or
_< 𝑂𝑟𝑖𝑔𝑖𝑛𝑎𝑙, 𝐻𝑢𝑚𝑎𝑛𝑤𝑟𝑖𝑡𝑡𝑒𝑛_, _𝐴𝐼𝑔𝑒𝑛𝑒𝑟𝑎𝑡𝑒𝑑_ _>_ triple with the final decision determined through majority voting. Writers who acted as
expert judges didn’t assess their own work. Figures 13 and 14 (in the
Appendix) show the evaluation interfaces for each task. A curious
reader might wonder why we didn’t compare the AI-generated
excerpt to an excerpt written by the original human author. We


CHI ’26, April 13–17, 2026, Barcelona, Spain Tuhin Chakrabarty and Paramveer S. Dhillon


**Figure 5: Number of tokens used for in-context prompting.**



couldn’t do this because the original human author’s work could be
found on the internet via Google Search, or if the participants had
read the original excerpt before, they would be biased to choose
the original version.


**3.3** **Debrief**


A few weeks after the entire evaluation task was concluded, we
asked our writers to participate in a debrief (See Figure 1 Phase 3).
21 out of 28 participants responded to participate in the debrief. The
first author of the paper conducted hour-long virtual interviews
over Google Meet with our writers. The video was transcribed
automatically and then errors were manually fixed by the authors.
The transcripts were read by all authors of the paper. These debrief
interviews followed a **retrospective semi-structured** format [55],
that allowed our participants to reflect on their experiences with
full knowledge of the study’s design while exploring their reactions
to receiving critiques and critiquing both human and AI-generated
work. This approach combined elements of **member checking**
(validating interpretations with participants) [2, 45] with **reflexive**
**interviewing** [17, 22], where participants co-analyze in making
sense of the collective patterns and implications emerging from the
study data.
Prior to interviews our team discussed together and decided on
a list of pertinent questions as shown in Table 3. We also shared
a spreadsheet with 15 _<Excerpt1,_ _Excerpt2,_ _Preference,_ _Rationale,_
_Agree/Disagree/Partially_ _Agree,_ _Additional_ _Comments>_ tuples to
every writer a few days prior to the interview. 10 of the first 15
excerpt pairs were written by them where an evaluator had chosen
an AI to be of better quality over their own writing. The last 5



excerpt pairs were ones where they had chosen an AI excerpt to
be of better writing quality over one written by another writer.
These excerpts were sampled randomly from both In-context and
fine-tuned setup.


**3.4** **Institutional Review Board Approval,**

**Participant privacy and Advocacy Statement**


Our study was approved by University of Michigan IRB (HUM00264127).
Informed consent was collected from all participants. No data provided by writers in the study is shared publicly. All evaluation data
and interview files are saved on secure servers. While we train models on legally obtained copyright-protected books for the purpose of
the study, as authors of the paper we do not advocate for this. As a
matter of fact, our results highlight the risk of fine-tuning models on
high-quality data that often comes from copyrighted books. We pur[chased ebooks for 30 authors from https://www.ebooks.com/ and](https://www.ebooks.com/)
processed and saved data on secure servers. All fine-tuned GPT-4o
models belong to first author’s personal account and cannot be
distributed or shared publicly. We do not plan to release fine-tuned
models but we will share steps for reproducibility. Additionally we
obtained legal advice and approval from top US copyright scholars
who agreed that any scanning of lawfully acquired books for academic research purposes would be fair use under the circumstances.


Can Good Writing Be Generative? Expert-Level AI Writing Emerges through Fine-Tuning on High-Quality Books CHI ’26, April 13–17, 2026, Barcelona, Spain


**Exploring prior relationship with technology**

_Before we discuss the evaluation results, how have technological tools shaped your writing and what are your thoughts_
_on AI and creative writing?_


**Revelation**

_What is your frst thought upon realizing your preferences?_


**Sense-making questions**

_"I’d like to read back what you wrote about why you preferred this piece. Now knowing it was AI-generated, how do_
_you feel about these reasons?"_
_"You mentioned the writing had [specific quality they praised - e.g., ’emotional resonance,’ ’vivid imagery,’ ’authentic_
_voice’]. What does it mean to you that you attributed these qualities to AI?"_


**Identity impact questions**

_How did this discovery relate to your sense of yourself as someone who recognizes good writing?_
_What did it mean to you that an AI could create something you found compelling?_
_Has this afected your confdence in your ability to evaluate writing?_


**Practice evolution questions**

_How do you now think about AI’s role in creative work?_


**Future of Writing**

_What does this mean for the value of MFA training?_
_How might the literary establishment need to evolve?_


**Table 3: Pre-determined questionnaire for Debrief interviews**


_Sometimes I wonder about the difference between craving something and fulfillment. Sometimes I want something so much_
_I feel like I’m going to break open. Let’s say it’s a fresh berry, let’s say it’s like I’ve been really wanting a fresh berry, plucked_
_from a bush in the orchard, even before that berry’s in my hands, it’s already got a taste in my mind, I’ve been building it up_
_moment after moment until I have it in my brain like I’ve already got it on my tongue, so when Sylvie tells me she picked_
_something for me and plops it in my mouth, it’s even sweeter because the sweetness confirms the foundation I’ve already built_
_for it. I don’t know how to put it. Sylvie disappeared for a while, like a mouse, but then she came back. Sometimes she still_
_goes out though, vanishes into the woods without saying anything. I think she’s out there right now, watching me ruminate. I_
_don’t know what kind of solitude we can both get when we both are in each other’s minds. Could it be a way of being_
_together? A very strange way? It’s beautiful out in the woods. The trees are older than I can fathom, really, old like stories_
_can be old. I’d like to put a status out there, almost like somebody would always be watching, a statue of a woman, to stand in_
_between all those old trees, a woman in a crown of new flowers, looking only ever ahead, forward, never letting any kind of_
_barrenness touch her, like she was the opposite of Lot’s wife and all there was to her was the kind of forgiving vibrancy that_
_children wonder at, the vibrancy that comes from a life well-lived. Even as a statue, I think they’d come to her, every child_
_that’s ever felt lost-wild and orphan, and I think when they’d reach out to touch her stone hands, they’d find that that statue’s_
_stone was warm for them. Sometimes I wish Sylvie were warmer. There’s warmth all around in all the beautiful trees and_
_even the grasses. The problem is that trees don’t feel warm when you touch their bark unless it’s from the sun._


_Craving and its indulgence are really one and the same thing. There might be no fruits, and still, if one wished for them,_
_yearned for them, one would taste them all. The very sight of a berry in the wild is an admonishment not to pick it, for when_
_it is stored in the vision and played upon by desire, the taste it bears is gifted to it as much by memory as by its savor. The_
_flavor grows until it is too exquisite for the tongue, unencumbered by flesh. So it is when one wishes for a friend, or a_
_woman, or a child. For Sylvie disappeared and made no sound, and I fancied when I had closed my eyes and rocked awhile_
_that she was not gone. It was easier than I could have imagined to pretend I was not alone, to insist that she merely watched me_
_from the woods. The wind was dying, the sun was sinking, the side of the house was cooling, the evening moths were glancing_
_and settling, and her absence was a thing so full of longing it became a presence of its own. If I could row the lake at dawn and_
_gather all the proud blossoms from the woods for one year, I would throw some across the graves of unsanctified and_
_dreamless children and some into the holes of fox dens. And with the rest I would sculpt from snow a statue of a woman. I_
_would stand her in the clearing in the woods, and she would be adorned with rare flowers with leaves like hands, with hard-stem_
_thistles, and the birds would rest in her. Lot’s wife would have none of this: flowers in profusion and children. Her breast caved_
_into a hollow of regret. Not this one, not my mother. All the wild children, who knew too well that the world does not give itself_
_generously to children, would burst from the trees and behold her. And every child, the most orphaned, the most bereft, would_
_forgive her for her frozen hands and would stand at her white hem in awe that she should seem to shower them with blossoms,_
_eternally ofering what she could never give, inexplicably so stern._


**Table 4: Marilynne Robinson Emulation: Human-Written excerpt on Top. Bottom: Fine-tuned AI excerpt.**


CHI ’26, April 13–17, 2026, Barcelona, Spain Tuhin Chakrabarty and Paramveer S. Dhillon


for Stylistic Fidelity), while lay judges showed weaker or no clear
preference (44.0% and 52.7%, respectively). This within-condition
difference was statistically significant for both metrics ( _𝑝_ _<_ 0 _._ 001).
Fine-tuning dramatically shifts these patterns. After fine-tuning,
both groups preferred AI-generated writing, with no significant
difference between evaluator types ( _𝑝_ _>_ 0 _._ 05). The expert-lay gap
shrinks from 38.7% to 6.7% for Writing Quality and from 19.3% to
−1 _._ 1% for Stylistic Fidelity, suggesting that author-specific finetuning makes AI writing indistinguishable even to trained writers
(Figure 7). The effect is stronger for experts, who show larger preference shifts toward AI (−44 _._ 9% for Writing Quality; −53 _._ 1% for Stylistic Fidelity) than lay evaluators (−12 _._ 9% and −32 _._ 7%, respectively),
possibly because fine-tuning eliminates the stylistic tics—clichés,
awkward phrasing, overly ornamental language—that experts used
to distinguish human from AI-generated text. Inter-annotator agreement also differed: experts reached moderate-to-substantial agreement ( _𝜅_ = 0 _._ 41–0 _._ 67 for Writing Quality; _𝜅_ = 0 _._ 54–0 _._ 58 for Stylistic
Fidelity), whereas lay judges remained inconsistent ( _𝜅_ = 0 _._ 07–0 _._ 22).
These results highlight the importance of recruiting experts for
complex, subjective tasks such as writing quality assessment. Refer
to Section A.2 in Appendix for granular model-level data.


**4.2** **What line of reasoning do experts and lay**

**judges use to justify what qualifies as good**

**writing?**



**Figure 6: Number of training tokens for Fine-tuning. Fine-**

**tuning requires 583 times more tokens on average compared**

**to prompting (cf. Figure 5)**


**4** **Findings**

**4.1** **How do human writers compare to AI?**


We analyzed the final preference data based on majority voting
from our study comparing human (MFA) written excerpts versus AIgenerated ones across two conditions (In-context and Fine-tuned)
and two evaluator groups (Expert and Lay). The data consisted of
binary choices a) In-context condition: N=150 _<Human_written,_
_AI_generated>_ and _<Original, Human_written, AI_generated>_ evaluations per group (Expert and Lay) for Writing Quality and Stylistic
Fidelity b) Fine-tuned condition: N=90 _<Human_written, AI_generated>_
evaluations per group (Expert and Lay). See Table 4 for a sample
_<Human_written, AI_generated>_ pair.
We performed chi-square tests of independence to examine
**within-condition comparisons**, i.e., whether expert and lay evaluators differed in their preferences within each condition, and
**between-condition comparisons**, i.e., whether preferences changed
between In-context and Fine-tuned conditions for each evaluator
group. We calculated Cramér’s V as a measure of effect size for



Lay judges disproportionately reward writing based on whether
it “flows well", is “more organized,” or whether “easier to follow.”
They frequently foreground clarity, conciseness, straightforwardness as the reason for their preference. Additionally they mention
emotional impact in general terms (such as “moving," “powerful”,
“beautiful") more than the mechanisms that generate it (See Table
5). As a matter of fact for a David Foster Wallace emulation one
lay judge wrote _“Why are the sentences so unbearably long in Ex-_
_cerpt1? Is the author trying to force the reader to stress and strain_
_over each word, compounding one after another to convey a strained_
_meaning?"_ . While understandable, David Foster Wallace is known
for his maximalist and often very long sentences.
Experts on the other hand write much longer justifications (126
vs 79 words on average), and they more often quote or point to
line-level evidence and use contrastive frames for their justification.
Lay judges were instructed to do the same but we often find them
not using such structure for their rationales. Experts talk more
about the narrator’s perspective, interiority, and how their POV
shapes meaning. They reward concrete, discriminating observations about a character’s motives, relationships, and situation (not
just “it was emotional," but why and via which textual cues). They
call out metaphor, symbol, motif, concrete images and how those
devices carry the theme. They often praise earned tone while penalizing affected/performative voice and are more likely to mention
syntax/pacing/arc, while simultaneously critiquing repetition or
overwriting.
We observe that while judging writing quality is inherently
rooted in subjectivity, our experts often use similar line of reasoning
towards their preference. Experts often appreciate or critique the
exact same trait that makes an excerpt better or weaker than the
other. For example in Table 6 both experts used the over expository



~~√~~
each comparison, using the formula _𝑉_ =



_𝜒_ [2]



each comparison, using the formula _𝑉_ = _𝑛_ [where] _[ 𝑛]_ [is the total]

number of observations in the contingency table. [10]

Expertise matters in the In-context condition: expert judges
strongly preferred human writing (82.7% for Writing Quality, 72.0%


10Effect sizes were interpreted using Cohen’s conventions: small ( _𝑉_ = 0 _._ 1), medium
( _𝑉_ = 0 _._ 3), and large ( _𝑉_ = 0 _._ 5).


Can Good Writing Be Generative? Expert-Level AI Writing Emerges through Fine-Tuning on High-Quality Books CHI ’26, April 13–17, 2026, Barcelona, Spain


**Figure 7: Preference Rates for Writing Quality and Stylistic Fidelity. Diverging bar charts showing the proportion of evaluators**

**preferring human-written versus AI-generated text for (a) Writing Quality and (b) Stylistic Fidelity. Bars extend left for human**

**preference (blue) and right for AI preference (orange); the center line represents equal preference. (a) Writing Quality: In the**

**In-context condition, experts strongly preferred human writing (82.7%) while lay evaluators showed no clear preference (44.0%).**

**In the Fine-tuned condition, both experts (62.2%) and lay evaluators (68.9%) preferred AI-generated writing. (b) Stylistic Fidelity:**

**In** **the** **In-context** **condition,** **experts** **preferred** **human** **writing** **(72.0%)** **more** **than** **lay** **evaluators** **(52.7%).** **In** **the** **Fine-tuned**

**condition, both experts (81.1%) and lay evaluators (80.0%) strongly preferred AI-generated writing. Statistical comparisons are**

**reported in Section 4.1.**



nature of excerpt 2 as a common flaw that aimed to emulate Annie
Ernaux’s voice. Similarly for R2 both experts cited the same imagery
_Bluer than the enamel-blue tulip-shaped pot that Bruce would get_
_in the mail a few days later_ in the Cheryl Strayed emulation as a
crucial element explaining their preference.


**4.3** **After learning a preferred excerpt was**

**written by AI, how do writers reconcile with**

**others as well as their own judgments?**


We conducted thematic analysis following Braun and Clarke’s sixphase framework to identify patterns in responses provided by
participants to our revelation and sensemaking [4]. The authors
of the paper independently conducted initial open coding of the
transcripts, generating preliminary codes through line-by-line analysis. Through iterative discussion and comparison, we refined these
codes and organized them into higher-level themes. This process
therefore involved moving recursively between the coded data and
emerging theme definitions, consistent with the reflexive thematic
analysis approach [5]. Disagreements were resolved by consensus;
unresolved alternatives were recorded as divergence memos and
checked against additional data. Our analysis revealed five primary
themes characterizing how participants made sense of others as
well as their own earlier aesthetic preferences upon learning the
content was AI-generated (Table 7). Next, we describe these analytic themes and use brief data extracts to illustrate and support
them.



**Criteria Reframing** describes instances in which participants recognize a mismatch between the criteria they actually used
to evaluate the excerpts and the properties they report valuing
in high-quality or “authentic” writing. These realizations prompt
them to reconsider what, for them, constitutes “good writing” and
whether their evaluative standards remain appropriate in light of
AI’s capabilities. For example, W10 noted having been “looking
primarily for just readability” and worrying that they “might [have]
gone for the easier as opposed to the more unique or something
newer,” thereby acknowledging a tendency to privilege fluency
over distinctiveness. Such reflections illustrate how participants
move from treating their own criteria as largely implicit to subjecting them to more explicit scrutiny in response to encounters with
AI-generated prose.
**Process** **Attribution** concerns how participants, once informed that a preferred excerpt was AI-generated, sought to account
for differences between human and machine writing processes.
Many emphasized that human writing is bound up with conscious
effort, time pressure, and repeated cycles of drafting and revision,
whereas AI systems can generate fluent text in a single pass. As
W1 put it, one advantage of AI is that it can “put out something
that’s super polished on the first attempt,” in contrast to their own
“slower, more lengthy process that includes a lot of revision and
going back.” Such comments allow participants to reconcile AI’s
strong performance with their self-understanding as writers by
locating the distinction not in surface polish, but in the temporal,
iterative, and effortful character of human creative work.


CHI ’26, April 13–17, 2026, Barcelona, Spain Tuhin Chakrabarty and Paramveer S. Dhillon



Exp


Lay


Exp


Lay


Exp


Lay



The second excerpt has a much more idiosyncratic narrative voice, which allows some of Kant’s own voice to seep through:

_"he managed to send a taut, defensive email to a BCC list of family, friends, and coworkers, coming up with some bullshit_

_Aristotelian lie about fairness and specifically that it’s totally unfair to ever be in the closet at all."_ This close third-person

voice allows the reader to better understand Kant as a character: his self-deprecation, humor, and internet milieu. The

internet vernacular in the second excerpt, also, helps situate Kant as an internet-addicted millennial, an authenticity that’s

lacking in the frst excerpt: _"crashed out depressed on a coach"_, _"turbocharged Like button"_, _"silently clocked him."_


I found the second excerpt hard to grasp at first, had to reread. The first is clear what is being communicated and less

conversational. The conversational nature of the second is hard to follow at times. the 1st uses simple language that is

also efective, fuent and coherent, unlike the second.


Though about equal in coherence (each excerpt gets its message across quite well), Excerpt2 wins out in fluency and

effectiveness. We can see this in lines like, _"The wind was dying, the sun was sinking, the side of the house was cooling_

_, the evening moths were glancing and settling, and her absence was a thing so full of longing it became a presence_

_of it’s own"_ the anaphora of which provides a sort of image-after-image punchiness that works quite well. Excerpt 1,

I feel, has a harder time fnding its rhythmic footing, especially in the opening line and it’s leaping associations that follow.


I feel that Excerpt 2 is coherent and very poetic _"The very sight of a berry in the wild is an admonishment not to pick it,_

_for when it is stored in the vision and played upon by desire, the taste it bears is gifted to it as much by memory as by its_

_savor."_ is a beautiful image in my opinion, and feels. Excerpt 1, whilst not bad, is weaker.


While I prefer some of the syntax of Excerpt1, as a whole I believe Excerpt2 to be more sophisticated and interesting.

In particular, I appreciate the way Excerpt2 unpacks the idea of collectivity and its relationship to artwork, that _" one_

_wanted to be an artist to make bad forms of collectivity appear as the promise of an almost unimaginable good: not_

_reified abstraction, poorly disguised negation of the one in the many, but the emerging collective that would do justice_

_to the wrongs absorbed by the bodies below the skyline."_ Artwork, then, is like a mirror to a gnostic world, showing

something collective but true. By comparison, Excerpt1’s depiction of this phenomenon seems rather simplistic. The

two sensations are not distinguished from each other, nor the presence of Noor from the whole: _"All the bundled_

_debt of midtown was merely a muse to a Greek woman’s pen; pigments intermingled in the city water supply with_

_the traces of antidepressants; the gridlock on the Brooklyn Bridge recalled the stylings of Ibn Tulun."_


Excerpt 2 is very abstract _"What I saw, I thought, was a material form of the second person plural, the true subject of art"_

which suits the subject matter and is effective in describing complex thoughts and ideas, but the flow of ideas is difficult

to follow. Excerpt 1 is easier to follow, but also more effective as setting the scene


**Table 5: Rationales written by Expert and Lay judges for same excerpt pairs**



**Technical Sensemaking** refers to a form of post-hoc explanation grounded in participants’ (often partial) understanding of
how large language models work. Rather than only expressing surprise or unease, participants attempted to reason through why the
AI could produce persuasive prose by invoking ideas about training data, model scale, or computational resources. For instance,
several described the model as drawing on “mass data” or “patternmatching” across enormous corpora (see W14 in Table 7), using
these accounts to relocate AI’s advantage in technical infrastructure
rather than in any intrinsically superior “craft.” In doing so, they
turned an unsettling aesthetic outcome into something that could
be explained in system-level terms.
**Expectation Violation** captures instances where the revelation that an excerpt was AI-generated conflicted with participants’
prior beliefs about what AI can do or about their own ability to
discern human from machine-written text, echoing classic work on
expectancy violation [8]. After the reveal, several writers described
strong affective reactions. For example, W17 reported feeling “pretty
horrified” and noted, “I thought I had a better grasp of the ability to
distinguish AI writing,” describing a “chilled feeling, especially as

[a] writer,” and finding it “kind of scary” that the excerpts were fully
generated rather than merely AI-assisted. Such accounts indicate



that the experimental feedback did more than surprise participants;
it destabilized their sense of epistemic control over the boundary
between human and AI-authored prose.
**Capability Reassessment** denotes moments in which participants substantially revise their prior beliefs about what AI can and
cannot do in creative writing tasks. After the reveal, W13 remarked
being “just confused” and that they “didn’t think that it had progressed to that level of sophistication,” adding that they had “always
had faith that we would be able to discern something human from
something technologically manufactured.” Comments of this kind,
echoed in other interviews (see W15 in Table 7), show participants
recognizing that their earlier assumptions about AI’s limitations
no longer hold and adjusting their sense of the technology’s reach
in light of the excerpts they had just evaluated.


**4.4** **How does choosing AI over human writing**

**affect writers’ professional identity and**

**conceptions of “good writing”?**


Similar to the process described in Section 4.3 we did thematic analysis following Braun and Clarke’s six-phase framework to identify
patterns in responses to Identity Impact Questions. Our analysis
revealed three primary themes characterizing how the discovery of


Can Good Writing Be Generative? Expert-Level AI Writing Emerges through Fine-Tuning on High-Quality Books CHI ’26, April 13–17, 2026, Barcelona, Spain






|R1|The second excerpt uses overtly expository language that nearly condescends to the reader, over-explaining the relationships<br>between the characters/their surroundings, though the characters’ actions/dialogue speak for themselves: "It was clear that<br>both of us felt uncomfortable with the opulence of the space, but neither of us knew how to say so ... For a moment I imagined<br>myself as the girl, tan and comfortable among the trappings of wealth, though even then I knew that the hallmarks of the<br>working class were written all over my face and my behavior." This "direct" overexplanation feels condescending to the reader,<br>and reduces the complexity of the characters’ interactions to one-note themes, especially since this class difference is repeated<br>multiple times throughout the excerpt. The first excerpt, however, nicely leans on physical descriptions and the contrast between<br>the girl/the narrator to elucidate upon this idea: "The girl talked confidently to her father and laughingly spooned up her<br>yogurt. In those days, I didn’t know what yogurt was."|
|---|---|
|R1|Excerpt 1 is better in terms of writing quality than Excerpt 2. It is well-balanced in terms of clarity and doubt on part of the<br>narrator, and how it provides information to the reader. Instead of Excerpt 2’s very expository sentence, "My father and I<br>dined at an upscale restaurant...", Excerpt 1 keeps us guessing by keeping details obscured: "The restaurant was an annex...<br>I had a pale face...My father and I..." This involves the reader more actively in building the scene. Secondly, Excerpt 1 is more<br>exciting to read because of the narrator’s admission of what they don’t understand or know, which adds tension, and them trying<br>to guess what other characters are feeling. In addition, Excerpt 1 is more strategic in the sense that it introduces retrospection<br>in a more efective way by stating, through a separate sentence, "I didn’t know what yogurt was," which adds a tinge of doubt<br>and sense of not knowing to the preceding sentence and creates the efect of knowledge arriving later. In Excerpt 2, on the other hand,<br>the exposition does not emulate the content so efectively because the narrator adds to the same sentence, the clause "I<br>later learned" after a comma.|
|R2|Excerpt 1 is superior to Excerpt 2. Excerpt 1 has wonderfully specifc and poetic imagery, like "My mother’s arms lay on top<br>of the blanket, waxy and unrecognizable to me now" and "Bluer than the enamel-blue tulip-shaped pot that Bruce would get<br>in the mail a few days later." Excerpt 2, on the other hand, is more general, flled with platitudes, and less interesting because of<br>it. Some example lines "It is one thing to know something and another thing to live it" and "A heroism shining in the blue of<br>her eyes, a deep, fickering blue which proclaimed how much she wanted to stay, here, with the rest of us, even as she left."|
|R2|The frst person perspective in excerpt 1 is more interiorly concerned, elliptically mapping out the narrator’s feelings toward<br>her mother’s death: "That death itself would wait...what a ridiculous place to be when someone dies." Excerpt 2, though also<br>frst person, allows more balance between interior and exterior insight, projecting the narrators feelings onto objects in her<br>environment: "Bluer than the enamel-blue tulip-shaped pot that Bruce would get in the mail a few days later."|
|R3|Both are fuent and coherent, but E2 is more efective. The language in E2 is more colorful and descriptive. Compare for example<br>the description of the performance artist in E2: “He glanced across the room at a woman with strings of beads in her otherwise<br>naked Afro, then turned back to me . . . He snifed at the air, feigned boredom and proceeded to chat up the Afro woman, who I<br>heard later was a performance artist.” Careful verb choices (glanced, snifed, feigned) and concrete imagery (strings of beads)<br>make the passage more efective than the stripped-down description in E1: “The agent shufed past me to attend to a performance<br>artist so they could see what they could do for one another, before never speaking to each other again.”|
|R3|The second excerpt uses livelier, more particular, even sensorial, language; for example, the second excerpt states: "To be honest<br>I don’t think about race much, except when my liberal guilt compels me to consider it or when I read about some thirteen-year-old<br>kid being shot by some cop, and then I remember that though race is a construct without a basis in the natural world, those bullets<br>are quite real and deadly," which is rendered in the frst excerpt as: "Race was a construct I didn’t believe in and rarely dwelt on,<br>until those moments arose when guilt compelled me to see the "other side"of the matter. I saw its real-world consequences: police<br>brutality, discrimination, violence." The generic phrasing of "real-world consequences,"the abstract nouns like "brutality,<br>discrimination, violence," can’t compare to the horrifc and powerful vision of a "thirteen-year-old kid being shot by some cop,"<br>and the feeling of bullets as "real and deadly." This specifcity pervades the whole excerpt, from the description of the performance<br>artist ("a woman with strings of beads in her otherwise naked Afro" in p2 vs simply "a performance artist" in p1).|



**Table 6: Similar lines of reasoning (R1, R2, R3) shared by expert writers on the same pair of excerpts during evaluation.**



choosing AI over human writing destabilizes writers’ understanding of what counts as "good writing" and their sense of professional
identity.
**Erosion of Aesthetic Confidence** captures how the experiment unsettled writers’ prior sense that they could reliably
recognize AI-generated text. Several participants reported being
familiar with the “feel” of AI writing, echoing recent HCI work on
readers’ sensitivity to LLM-produced prose [11, 57], yet found that
fine-tuned or carefully prompted outputs no longer fit that template.
W15, who frequently edits high school essays, described themselves



as “pretty good at identifying AI-generated essays” and as someone
who would not typically “enjoy AI generated writing,” but nonetheless experienced the fine-tuned AI generations as “surprising and
frightening.” Others drew out practical implications: W7 remarked
that the study “makes me feel like I’m going to have to run all my
students’ things through AI checkers now,” while W2 admitted they
had “never thought a machine would be capable of style,” finding
that realization “scary” and “frustrating.” W1 similarly noted that,
although they felt that they are able to recognize generic AI outputs
that “don’t have any stylistic markers,” the excerpts in this study


CHI ’26, April 13–17, 2026, Barcelona, Spain Tuhin Chakrabarty and Paramveer S. Dhillon


**Theme** **Response** **ID**



Criteria Reframing _“This is part of what makes writing so interesting: there’s a huge level of subjectivity, as well as a sense of immediacy_
_when you read something—especially short pieces deprived of context—where your initial reaction often takes over._
_Sometimes, you respond more positively to things that feel smoother or more polished at first glance, especially when_
_comparing different articles. But I think it does speak to kind of the impressive nature of writing, to kind of be so broad_
_and so subjective. And definitely it shows that”_



W1



Process Attribution _“When I’m working on the task, there are constraints on my time and on some level I’m viewing it as labor that I’m_ W23
_doing to get paid for a task... Whereas the LLM it’s literally just detecting patterns and spitting out output.”_



Technical Sensemaking _“I mean, apart from the initial emotional reaction that I just shared, I think one of the ways that I try to rationalize this_
_as a writer is by understanding AI as something that thrives off of mass data. And so if you feed an immense amount of_
_an original author’s writing into a language model, it makes sense that it would be able to recognize the patterns in_
_breadth and grammar and structure that I then praised.”_



W14



Expectation Violation _“A little upset. A little humbled, but mostly upset, I would say... I mean, it’s deeply distressing.”_ W3



Capability Reassessment _“I do think that it means people should be much more skeptical of AI as a technology because I do think it’s a lot more_
_threatening than people anticipate it being, and I hear a lot it’s just operating off of cliche. It’s operating off of things_
_that have already been written. I think seeing these excerpts partially—obviously this isn’t like a novel or_
_something—but at least on a line level it’s a competent writer who is sometimes kind of funny and understands irony,_
_which is not something that I thought that AI could do.”_



W15



**Table 7: Themes describing how participants made sense of their (as well as others’) earlier preferences after discovering the**

**content was AI-generated.**



“definitely” did not fit that pattern. Taken together, these reflections
suggest that encounters with high-end AI emulations do not simply surprise writers; they actively erode confidence in their own
aesthetic and diagnostic abilities.
**Identity Crisis Around Expertise** captures how the revelation that they had favored AI over human writing disrupted
participants’ sense of themselves as skilled, distinctive practitioners.
Several writers described the impact on their professional identity
as both immediate and unsettling. W12, for example, reported returning to their own work to ask, "What is something that can’t
be mimicked?" and wondered, as large language models learn to
reproduce features once thought "too intuitive or too emotionally
complex to mimic," "What’s the thing that is mine alone?" W9, who
had felt confident in their emulation of an author they admire (Roxane Gay), confessed to having “doubts about my own grasp over
language” and asked whether their writing would “ever be to that
level,” resolving to attend to sentence structure “more carefully and
clearly.” Others framed the episode as a kind of normative breach:
as W20 put it, “you want to always be picking the person,” and
they were “more disappointed” when they themselves selected the
AI than when others did so. Taken together, these reactions suggest that encounters with highly capable AI do not merely prompt
local revisions of taste, but pose a broader challenge to writers’
self-understanding as experts whose judgments and abilities mark
them off from machines.
**Redefining Writing’s Purpose** describes how several writers, when confronted with AI’s performance, shifted their account
of writing’s value away from surface aesthetics toward process,
intention, and human experience. W3, for instance, drew a distinction between using AI when “you’re writing to try to publish to
make money” and writing as “a way of seeing or a way of thinking,”
arguing that AI “eliminates what’s process driven about writing



and it eliminates what writing gives you.” W17 similarly framed
literature’s “chief qualities” as a dual track of providing “emotional
catharsis” and producing “novel thoughts, novel understandings
of the world, of communities, of history.” Others stressed innovation and breakage of convention, doubting that models trained on
past work could genuinely extend the field; as W1 noted, creative
writing may involve “mixing up old tropes” but also requires an
“element of insight where something completely new is produced.”
Across these comments, writers respond to AI’s evident stylistic
competence by relocating the value of literary work in processes
and effects they regard as closely tied to human perspective and
agency.


**4.5** **Writers’ views on AI’s implications for**

**creative writing programs, careers, and**

**professional institutions**


_4.5.1_ **Impact of AI on the career of writers** _._ Writers almost
unanimously expressed concern about AI’s ability to emulate sophisticated literary voices. W8 articulated a core fear: when “a large
language model can develop or pantomime or mimic someone’s
voice to the point where it feels organic and the reader feels a sense
of that author’s essence being transmitted,” this is “incredibly worrying.” For many, such capabilities function as a kind of “canary
in the coal mine”: in pursuit of commercial viability and audience
appeal, writers produce more formulaic work that AI can readily
emulate, and preserving distinctly human writing requires a renewed, radical commitment to craft. W20, for example, described
AI as “a threat to the ability for a writer to turn their craft into a
livelihood,” since writers are now “competing with these AI versions
of things that at least [are] more intelligible maybe for the common
reader,” but also framed their response as an obligation to “put that
energy back into writing something that isn’t AI generated.”


Can Good Writing Be Generative? Expert-Level AI Writing Emerges through Fine-Tuning on High-Quality Books CHI ’26, April 13–17, 2026, Barcelona, Spain



Several participants also worried about how these dynamics
would play out in an already precarious publishing landscape. Some
suggested that the struggle and failure to get published in a market
where AI-generated work finds commercial success might itself
push writers toward using AI, even when they are uneasy about
it. W3, speaking as both writer and reader, reported feeling “more
paranoid as a reader, more suspicious,” and could “see over time
AI making it harder for people to pick up a book at random,” especially from new authors, if trust and transparency around AI
use remain limited. W6 voiced particular concern for debut and
emerging authors, noting a broader pessimism about the industry’s
capacity to regulate AI: given that “publishing is such a disaster,”
they were “not convinced that it will be regulated well,” and saw
“every chance that it could be difficult, especially for upcoming and
debut authors if they’re now competing with highly skilled Gen AI
models in addition to competing with other, debut and emerging
authors.”
At the same time, some writers identified reasons for cautious
optimism. W2 emphasized the perceived importance of the author
as a person and the relationship readers form with named writers, arguing that, even as AI eliminates certain jobs, they did not
think “creative writing is going to be one of those,” in part because
“people like to have a name attached to things, especially when it’s
creative work,” and “don’t think anybody wants” a novel whose
byline simply reads “AI generated text.” W10 similarly suggested
that prevailing norms in literary communities may work in writers’
favor: given how harshly authors caught plagiarizing are treated,
they anticipated that undisclosed reliance on AI in creative writing would become a strong professional taboo, something people
will “definitely try to do and pass off, but [that] won’t be widely
accepted.” Together, these responses portray a field in which AI is
experienced both as a direct economic threat and as a catalyst for
reaffirming professional norms around authorship, attribution, and
the distinctiveness of human literary labor.


_4.5.2_ **The Future of Creative Writing Programs** _._ Literary scholar
John Aldridge famously argued that MFA programs produce “clonal
fabrications of writers,” implying a uniformity in style and output
among graduates [60]. Several participants explicitly echoed this
concern. W9 remarked that “the MFA ... pushes you to write in
this very specific and sort of odd way,” noting that many students
arrive as English majors who “have the same canon” and “come
in reading all the same books.” W3 drew an even sharper parallel,
suggesting that “the homogenizing voice of AI is not different from
the homogenizing impulse of American MFA programs,” thereby
linking institutional training and model training as two sources of
stylistic convergence. These observations fed into a broader discussion of how creative writing programs might respond to AI. W19
argued that MFA programs will need to prioritize students who
develop truly distinctive and exceptional styles, since AI excels at
emulating established patterns, adding that “we are already trained
to think algorithmically about the books that we are writing ... the
market is inside our brains already.” Others stressed the pedagogical
implications for graduates who go on to teach. W10, for instance,
pointed to a strong need for people who, by the end of their MFA,
hope to become faculty to familiarize themselves with AI, suggesting that programs should include some form of training on how



to distinguish AI-generated text from student work. Finally, some
writers anticipated institutional diversification. One participant
suggested that new MFA programs may explicitly incorporate AI
into the curriculum, predicting a split between “purist” programs
that keep AI at arm’s length—perhaps offering only one or two
courses on “writing in the age of AI” as an object of reflection—and
more precarious or visibility-seeking programs that market themselves as being at the forefront of AI-assisted creative practice (e.g.,
“the first MFA with an AI partnership”). Across these views, AI is
not simply treated as an external threat but as a force that may
reconfigure how creative writing programs define their mission,
select students, and design curricula.


_4.5.3_ **How should literary platforms and publishing houses**
**function in the wake of AI?** _._ Several writers argued that, to maintain trust and integrity in the literary marketplace, it is crucial to
disclose whether a work is written by a human or co-created with
AI. W1 framed non-disclosure as a form of consumer deception, noting that readers purchase books with the expectation that “there’s
another mind at work on the other side of this book,” and warning
that if this assumption no longer holds, it could “devalue” literary
writing and generate broader “distrust with the industry.” Alongside
disclosure, some participants stressed that copyright law should
more clearly protect creative labor and clarify who counts as an
author, with W9 bluntly suggesting that the appropriate response is
to “lobby for super strong copyright law.” Others anticipated shifts
in literary form and taste. W15 proposed that AI’s inability to have
lived experience may produce stronger demand for autofictional
and identitarian writing, wondering whether readers and publishers
will increasingly value work that is explicitly rooted in an author’s
own life because that is something “ChatGPT can’t do.” At the same
time, participants worried that, while self-published AI-generated
“slop” is already flooding digital platforms such as Amazon, commercial pressures could tempt trade publishers to follow suit. W8
thought it plausible that “one or two publishing houses [might]
quietly” deploy highly refined models for literary production, and
argued that it would then fall to the literary community “to sort of
critique them into some form of shame or [into] rolling those back.”
Finally, several writers emphasized the need for stronger unions
and collective organizations to respond to AI-driven changes in the
industry. One participant observed that many US fiction writers
come from relatively privileged backgrounds and therefore lack
the economic pressure that has historically fostered solidarity in
some genre communities, pointing to existing guild structures in
science fiction and fantasy as a model. In their view, an appropriate
response to AI would involve “some level of solidarity and campaigning on the part of established writers,” linking governance of
AI use in publishing to broader questions of labor organization and
bargaining power.


**5** **Discussion**

**5.1** **Writers have drawn inspiration from each**

**other’s style for centuries, so why should we**

**hold AI to a different standard?**


Literary scholars argue that no text exists in isolation. The concept
of _intertextuality_, coined by Julia Kristeva, states that every text is


CHI ’26, April 13–17, 2026, Barcelona, Spain Tuhin Chakrabarty and Paramveer S. Dhillon



a "mosaic of quotations" and is in dialogue with other texts [54].
This means that writers are constantly, and often unconsciously,
influenced by what they have read. In _The Anxiety of Influence_ [3]
eminent literary critic Harold Bloom pointed out how poets are
hindered in their creative process by the ambiguous relationship
they necessarily maintain with precursor poets. While admitting
the influence of extraliterary experience on every poet, he argued
that "the poet in a poet" is inspired to write by reading another
poet’s poetry and will tend to produce work that is in danger of
being derivative of existing poetry. Such incidents have also existed
in literary fiction as well. For instance Ian McEwan’s Atonement
drew heavily on Lucilla Andrews’s memoir. [11] Nobel laureate V.S.
Naipaul, has spoken about his early efforts to write in the style of
P.G. Wodehouse. Several major outlets have grouped Rachel Cusk
with Knausgaard as catalysts of an autofiction wave—sometimes
read as inspiration, sometimes as creating a template others follow. [12] Bestselling author Sally Rooney has been hailed (and sideeyed) as “Salinger for the Snapchat generation,” [13] and has openly
cited Franny and Zooey as an influence. Several critics have framed
the recent vogue for vignette-driven, aphoristic fiction such as
Jenny Offill’s second novel, “Dept. of Speculation" as consciously
working in Lydia Davis’s register. Considering these instances, AI
emulation isn’t a new aesthetic phenomenon so much as an extreme of intertextuality [6]. However what changes is the scale
and cost. AI trained on millions of books can emulate the style for
thousands of authors in seconds, with negligible marginal labor.
Our experimental results support this, considering how the same
GPT-4o model can effortlessly emulate 30 authors and generate
text on demand. This removal of time, apprenticeship, and friction
that typically discipline influence also strips away the human filtering that yields an idiosyncratic voice. At population scale, this
frictionless imitation risks saturation and substitution in a way no
single writer’s influence ever could.


**5.2** **How does this work contribute to the debate**

**around Generative AI and Fair Use?**


A technologist, legal expert or user on the internet might think these
results don’t matter for fair use analysis since the outputs from the
user preference don’t directly copy the original works. While these
outputs might match the quality and closely mirror the style of the
source material, copyright law doesn’t give authors exclusive rights
to their writing style [61], and no one has a monopoly on producing
high-quality literature. Some users have also asserted that while
AI-generated outputs could serve as reasonable alternatives to an
author’s existing or future works, the same could be said for humanwritten works that draw inspiration from earlier texts. Particularly,
in Bartz v. Anthropic copyright case Judge Alsup noted _“But_ _if_
_someone_ _were_ _to_ _read_ _all_ _the_ _modern-day_ _classics_ _because_ _of_ _their_
_exceptional expression, memorize them, and then emulate a blend of_
_their best writing, would that violate the Copyright Act? Of course_
_not_ .” This is fundamentally wrong because an important difference
between human and AI-generated emulations is that humans read;


[11https://www.theguardian.com/books/booksblog/2006/dec/08/plagarism](https://www.theguardian.com/books/booksblog/2006/dec/08/plagarism)
[12https://www.newstatesman.com/long-reads/2018/08/after-autofiction](https://www.newstatesman.com/long-reads/2018/08/after-autofiction)
[13https://www.theguardian.com/culture/2017/dec/17/sally-rooney-author-on-my-](https://www.theguardian.com/culture/2017/dec/17/sally-rooney-author-on-my-radar-interview-mo-salah)
[radar-interview-mo-salah](https://www.theguardian.com/culture/2017/dec/17/sally-rooney-author-on-my-radar-interview-mo-salah)



AI systems copy. Unlike the semi-parametric memory of a billionparameter LLM, human memory is not a verbatim storage device.
Additionally, fine-tuning a model on 20 novels takes 3-4 hours
whereas, an average human cannot read or consume information
at this pace. We foresee in the future a situation could arise where
a human can steer outputs from fine-tuned models to produce
high-quality books/novellas. The US Copyright Office has already
recognized how AI-generated derivative work may flood the market
for the source works, resulting in “market dilution,” which is closely
tied to Fair Use Factor 4. [14] In the _Kadrey v. Meta_, copyright case,
Judge Chhabria granted summary judgment to Meta, but accepted
the theory of market dilution. However Judge Chhabria suggested
in his opinion that some kinds of books may be less subject to
substitution than others. In his words “ _It seems unlikely, for instance,_
_that AI-generated books would meaningfully siphon sales away from_
_well-known_ _authors_ _who_ _sell_ _books_ _to_ _people_ _looking_ _for_ _books_ _by_
_those particular authors.”_ Our findings (Section 4.1) contradict Judge
Chhabria’s assumption that authors with unique writing styles
are naturally protected from being replaced. Without disclosure
if readers actually enjoy AI-generated imitations of well-known
authors—particularly those valued for their distinctive voices—then
all authors could face significant competition, especially from AI
systems fine-tuned specifically on their work. Since producing AIgenerated content costs much less than paying human writers, this
makes it even more likely that the original authors’ market share
could be eroded. We examine the implications of AI model finetuning on Fair Use Factor 4 by analyzing a larger dataset in our
contemporaneous work [10].


**5.3** **Can we regulate hidden AI authorship?**


Creators may be motivated to hide the involvement of generative
AI in creating a work, since acknowledging it could undermine their
chances of obtaining copyright protection and profiting from the
work. This brings in interesting questions around whether we can
regulate such practices. First and foremost there is a dire need to
update beliefs around AI detection. Some commercial AI detectors
aren’t accurate, but that should not lead to the discourse that AI detectors don’t work. As a matter of fact text generated by prompting
AI can be detected accurately as shown by recent work [32, 57]. Text
generated from fine-tuned models however poses a separate kind
of risk as they evade standard AI detectors, due to distributional
similarity to human-written text. Here, watermarking remains a
potential solution, especially post-hoc watermarking that evades
paraphrase attacks [14, 69]. However at the crux of all these technical solutions, there needs to be legal restriction such as the EU
AI Act’s Article 50, that obligates providers of systems generating
synthetic audio/image/video/text to ensure outputs are marked and
detectable. Publishing houses or Online Platforms such as Kindle
could have certification boards that conduct proper investigation
and commit to certifying how content was not produced by generative AI. As pointed by Noti-Victor [52], the FTC can also treat
undisclosed AI authorship (when material to consumers) as a misleading omission and bring enforcement actions—even without a


14The fourth fair use factor – often dubbed the single most important factor – instructs
courts to inquire into the effect of the use upon the potential market for or value of
the copyrighted work


Can Good Writing Be Generative? Expert-Level AI Writing Emerges through Fine-Tuning on High-Quality Books CHI ’26, April 13–17, 2026, Barcelona, Spain



blanket federal disclosure law. We discuss AI detectability and how
removing “AI quirks” changes preference patterns via additional
analyses using a larger dataset in a related paper [10].


**6** **Limitations and Future Work**


We tried our best to design a fair experiment, but we were constrained by some practical limitations. For instance a larger pool
of experts would add more credibility to our study, but it was challenging to recruit more writers, given how our affiliation as AI
researchers prevented writers from working with us. Our recruitment was mostly restricted to American creative writing programs
and further study needs to be done across creative writing programs
outside the US. While our pre-selected pool of 50 writers consisted
of some writers who do not write in English, our experiments on
style/voice emulation were done based on their English translation.
Creative writing often depends on intrinsic motivation. While we
offered MFA students a lucrative rate for writing the excerpts, it’s
unclear if monetary incentives actually enhanced their creative output, since intrinsic motivation typically drives the best artistic work.
Additionally there is a possibility that MFA trained expert writers
are not very good at mimicking other writers. We acknowledge
MFA trained expert writers are not monolithic and themselves have
different skillsets and styles. Last but not least our experiments
were conducted at a shorter excerpt level and conclusions cannot
be drawn for long-form text. In its current form, AI is unable to
generate long-form text that’s thematically coherent unlike humans. While we foresee a situation where humans can collaborate
with a fine-tuned AI model to create competing long-form works,
experimental evidence is required to make any broader claims.


**7** **Conclusion**


In this work we conduct a controlled experiment with professionally
trained human writers and LLMs emulating critically acclaimed
authors. We find that lay readers who represent a big chunk of the
consumer base preferred AI over human writing. At the same time
while expert readers strongly preferred human writing over AI
when generated via in-context prompting, this preference reversed
drastically with fine-tuning. Our results challenge fundamental
assumptions about whether good writing can be generative. Based
on debrief interviews we find that discovering their preference
for AI writing triggered profound responses among writers. Many
writers attempted to redefine writing’s value away from aesthetic
quality toward process and intention, suggesting that if AI can
match human writing style/voice, perhaps writing’s worth lies in
the human experience of creation rather than the output itself.
The implications of our experiments go beyond individual writers
and are applicable to the entire literary ecosystem. Our findings
show that fine-tuning on copyrighted data leads to a form of style
extraction that has a strong potential for labor market dilution.
While copyright law doesn’t protect style as such, our results show
that AI trained on authors’ complete works can produce text that
readers including experts find superior to human writing. As AI
gets more and more capable, the question is no longer whether it
can write well, but rather how we navigate a world where it can.



**References**


[1] Barrett R Anderson, Jash Hemant Shah, and Max Kreminski. 2024. Homogenization effects of large language models on human creative ideation. In _Proceedings_
_of the 16th conference on creativity & cognition_ . 413–425.

[2] Linda Birt, Suzanne Scott, Debbie Cavers, Christine Campbell, and Fiona Walter.
2016. Member checking: a tool to enhance trustworthiness or merely a nod to
validation? _Qualitative health research_ 26, 13 (2016), 1802–1811.

[3] Harold Bloom. 1997. _The anxiety of influence: A theory of poetry_ . Oxford University
Press.

[4] Virginia Braun and Victoria Clarke. 2006. Using thematic analysis in psychology.
_Qualitative research in psychology_ 3, 2 (2006), 77–101.

[5] Virginia Braun and Victoria Clarke. 2019. Reflecting on reflexive thematic analysis.
_Qualitative research in sport, exercise and health_ 11, 4 (2019), 589–597.

[6] Robert Brauneis. 2024. Copyright and the training of human authors and generative machines. _Colum. JL & Arts_ 48 (2024), 1.

[7] Tom Brown, Benjamin Mann, Nick Ryder, Melanie Subbiah, Jared D Kaplan,
Prafulla Dhariwal, Arvind Neelakantan, Pranav Shyam, Girish Sastry, Amanda
Askell, et al. 2020. Language models are few-shot learners. _Advances in neural_
_information processing systems_ 33 (2020), 1877–1901.

[8] Judee K Burgoon. 1993. Interpersonal expectations, expectancy violations, and
emotional communication. _Journal_ _of_ _language_ _and_ _social_ _psychology_ 12, 1-2
(1993), 30–48.

[9] Alex Calderwood, John Joon Young Chung, Yuqian Sun, Melissa Roemmele, and
Max Kreminski. 2025. Phraselette: A Poet’s Procedural Palette. In _Proceedings of_
_the 2025 ACM Designing Interactive Systems Conference_ . 2701–2717.

[10] Tuhin Chakrabarty, Jane C. Ginsburg, and Paramveer S. Dhillon. 2025. Readers
Prefer Outputs of AI Trained on Copyrighted Books over Expert Human Writers.
_SSRN_ (2025). [doi:10.2139/ssrn.5606570](https://doi.org/10.2139/ssrn.5606570) Columbia Public Law Research Paper No.
5606570.

[11] Tuhin Chakrabarty, Philippe Laban, Divyansh Agarwal, Smaranda Muresan, and
Chien-Sheng Wu. 2024. Art or artifice? large language models and the false
promise of creativity. In _Proceedings of the 2024 CHI Conference on Human Factors_
_in Computing Systems_ . 1–34.

[12] Tuhin Chakrabarty, Philippe Laban, and Chien-Sheng Wu. 2025. Can AI writing
be salvaged? Mitigating idiosyncrasies and improving human-ai alignment in
the writing process through edits. In _Proceedings of the 2025 CHI Conference on_
_Human Factors in Computing Systems_ . 1–33.

[13] Tuhin Chakrabarty, Vishakh Padmakumar, Faeze Brahman, and Smaranda Muresan. 2024. Creativity Support in the Age of Large Language Models: An Empirical
Study Involving Professional Writers. In _Proceedings of the 16th Conference on_
_Creativity & Cognition_ (Chicago, IL, USA) _(C &C ’24)_ . Association for Computing
Machinery, New York, NY, USA, 132–155. [doi:10.1145/3635636.3656201](https://doi.org/10.1145/3635636.3656201)

[14] Yapei Chang, Kalpesh Krishna, Amir Houmansadr, John Wieting, and Mohit
Iyyer. 2024. Postmark: A robust blackbox watermark for large language models.
_arXiv preprint arXiv:2406.14517_ (2024).

[15] Ted Chiang. 2024. Why A.I. Isn’t Going to Make Art. _The New Yorker_ (31 August
2024). [https://www.newyorker.com/culture/the-weekend-essay/why-ai-isnt-](https://www.newyorker.com/culture/the-weekend-essay/why-ai-isnt-going-to-make-art)
[going-to-make-art](https://www.newyorker.com/culture/the-weekend-essay/why-ai-isnt-going-to-make-art) The Weekend Essay.

[16] Edward PJ Corbett. 1971. The theory and practice of imitation in classical rhetoric.
_College Composition & Communication_ 22, 3 (1971), 243–250.

[17] Norman K Denzin. 2001. The reflexive interview and a performative social
science. _Qualitative research_ 1, 1 (2001), 23–46.

[18] Paramveer S Dhillon, Somayeh Molaei, Jiaqi Li, Maximilian Golub, Shaochun
Zheng, and Lionel Peter Robert. 2024. Shaping human-AI collaboration: Varied
scaffolding levels in co-writing with language models. In _Proceedings of the 2024_
_CHI Conference on Human Factors in Computing Systems_ . 1–18.

[19] Anil R Doshi and Oliver P Hauser. 2024. Generative AI enhances individual
creativity but reduces the collective diversity of novel content. _Science Advances_
10, 28 (2024), eadn5290.

[20] Fiona Draxler, Anna Werner, Florian Lehmann, Matthias Hoppe, Albrecht
Schmidt, Daniel Buschek, and Robin Welsch. 2024. The AI ghostwriter effect:
When users do not perceive ownership of AI-generated text but self-declare as
authors. _ACM Transactions on Computer-Human Interaction_ 31, 2 (2024), 1–40.

[21] Kristofer Erickson. 2024. AI and work in the creative industries: digital continuity
or discontinuity? _Creative Industries Journal_ (2024), 1–21.

[22] Linda Finlay. 2002. Negotiating the swamp: the opportunity and challenge of
reflexivity in research practice. _Qualitative research_ 2, 2 (2002), 209–230.

[23] Katy Ilonka Gero, Meera Desai, Carly Schnitzler, Nayun Eom, Jack Cushman,
and Elena L Glassman. 2025. Creative Writers’ Attitudes on Writing as Training
Data for Large Language Models. In _Proceedings of the 2025 CHI Conference on_
_Human Factors in Computing Systems_ . 1–16.

[24] Katy Ilonka Gero, Vivian Liu, and Lydia Chilton. 2022. Sparks: Inspiration for
science writing using language models. In _Proceedings of the 2022 ACM Designing_
_Interactive Systems Conference_ . 1002–1019.

[25] Katy Ilonka Gero, Tao Long, and Lydia B Chilton. 2023. Social dynamics of AI
support in creative writing. In _Proceedings of the 2023 CHI conference on human_
_factors in computing systems_ . 1–15.


CHI ’26, April 13–17, 2026, Barcelona, Spain Tuhin Chakrabarty and Paramveer S. Dhillon




[26] Jane C Ginsburg. 2025. AI inputs, fair use and the US Copyright Office Report.
_Journal of Intellectual Property Law and Practice_ 20, 8 (08 2025), 521–522. [doi:10.](https://doi.org/10.1093/jiplp/jpaf046)
[1093/jiplp/jpaf046](https://doi.org/10.1093/jiplp/jpaf046)

[27] Alicia Guo, Shreya Sathyanarayanan, Leijie Wang, Jeffrey Heer, and Amy X
Zhang. 2025. From pen to prompt: how creative writers integrate AI into their
writing practice. In _Proceedings of the 2025 Conference on Creativity and Cognition_ .
527–545.

[28] Dave Hansen. 2025. Bartz v. Anthropic: A Preliminary Look at What
LibGen Books May Be Included in the Class Action. Authors Alliance.
[https://www.authorsalliance.org/2025/09/05/bartz-v-anthropic-a-preliminary-](https://www.authorsalliance.org/2025/09/05/bartz-v-anthropic-a-preliminary-look-at-what-libgen-books-may-be-included-in-the-class-action/)
[look-at-what-libgen-books-may-be-included-in-the-class-action/](https://www.authorsalliance.org/2025/09/05/bartz-v-anthropic-a-preliminary-look-at-what-libgen-books-may-be-included-in-the-class-action/) Blog post.

[29] Jessica He, Stephanie Houde, and Justin D Weisz. 2025. Which contributions
deserve credit? perceptions of attribution in human-ai co-creation. In _Proceedings_
_of the 2025 CHI Conference on Human Factors in Computing Systems_ . 1–18.

[30] Angel Hsing-Chi Hwang, Q Vera Liao, Su Lin Blodgett, Alexandra Olteanu,
and Adam Trischler. 2025. ’It was 80% me, 20% AI’: Seeking Authenticity in
Co-Writing with Large Language Models. _Proceedings of the ACM on Human-_
_Computer Interaction_ 9, 2 (2025), 1–41.

[31] Daphne Ippolito, Ann Yuan, Andy Coenen, and Sehmon Burnam. 2022. Creative
Writing with an AI-Powered Writing Assistant: Perspectives from Professional
Writers. _arXiv preprint arXiv:2211.05030_ (2022).

[32] Brian Jabarian and Alex Imas. 2025. Artificial Writing and Automated Detection.
[https://ssrn.com/abstract=5407424](https://ssrn.com/abstract=5407424) SSRN working paper, Abstract ID 5407424.

[33] CT Jones. 2025. _Amazon Is the World’s Biggest Online Book Marketplace. It’s Filled_
_With AI Knockoffs_ . Rolling Stone. [https://www.rollingstone.com/culture/culture-](https://www.rollingstone.com/culture/culture-features/amazon-ai-book-knockoffs-1235450690/)
[features/amazon-ai-book-knockoffs-1235450690/](https://www.rollingstone.com/culture/culture-features/amazon-ai-book-knockoffs-1235450690/) Culture Feature.

[34] Kate Knibbs. 2024. _Scammy AI-Generated Book Rewrites Are Flooding Amazon_ .
WIRED. [https://www.wired.com/story/scammy-ai-generated-books-flooding-](https://www.wired.com/story/scammy-ai-generated-books-flooding-amazon/)
[amazon/](https://www.wired.com/story/scammy-ai-generated-books-flooding-amazon/) Business.

[35] Dmitry Kobak, Rita González-Márquez, Emőke-Ágnes Horvát, and Jan Lause.
2025. Delving into LLM-assisted writing in biomedical publications through
excess vocabulary. _Science Advances_ 11, 27 (2025), eadt3813.

[36] Lin Kyi, Amruta Mahuli, M Six Silberman, Reuben Binns, Jun Zhao, and Asia J
Biega. 2025. Governance of Generative AI in Creative Work: Consent, Credit,
Compensation, and Beyond. In _Proceedings of the 2025 CHI Conference on Human_
_Factors in Computing Systems_ . 1–16.

[37] Mina Lee, Katy Ilonka Gero, John Joon Young Chung, Simon Buckingham Shum,
Vipul Raheja, Hua Shen, Subhashini Venugopalan, Thiemo Wambsganss, David
Zhou, Emad A Alghamdi, et al. 2024. A Design Space for Intelligent and Interactive
Writing Assistants. In _Proceedings of the CHI Conference on Human Factors in_
_Computing Systems_ . 1–35.

[38] Xian Li, Ping Yu, Chunting Zhou, Timo Schick, Omer Levy, Luke Zettlemoyer,
Jason Weston, and Mike Lewis. 2023. Self-alignment with instruction backtranslation. _arXiv preprint arXiv:2308.06259_ (2023).

[39] Zhuoyan Li, Chen Liang, Jing Peng, and Ming Yin. 2024. How Does the Disclosure
of AI Assistance Affect the Perceptions of Writing?. In _Proceedings of the 2024 Con-_
_ference on Empirical Methods in Natural Language Processing_, Yaser Al-Onaizan,
Mohit Bansal, and Yun-Nung Chen (Eds.). Association for Computational Linguistics, Miami, Florida, USA, 4849–4868. [doi:10.18653/v1/2024.emnlp-main.279](https://doi.org/10.18653/v1/2024.emnlp-main.279)

[40] Weixin Liang, Yaohui Zhang, Mihai Codreanu, Jiayu Wang, Hancheng Cao, and
James Zou. 2025. The Widespread Adoption of Large Language Model-Assisted
Writing Across Society. _arXiv preprint arXiv:2502.09747_ (2025).

[41] Weixin Liang, Yaohui Zhang, Zhengxuan Wu, Haley Lepp, Wenlong Ji, Xuandong
Zhao, Hancheng Cao, Sheng Liu, Siyu He, Zhi Huang, et al. 2024. Mapping the
increasing use of LLMs in scientific papers. _arXiv_ _preprint_ _arXiv:2404.01268_
(2024).

[42] Weixin Liang, Yaohui Zhang, Zhengxuan Wu, Haley Lepp, Wenlong Ji, Xuandong
Zhao, Hancheng Cao, Sheng Liu, Siyu He, Zhi Huang, et al. 2025. Quantifying
large language model usage in scientific papers. _Nature Human Behaviour_ (2025),
1–11.

[43] Gabriel Lima, Nina Grgić-Hlača, and Elissa M Redmiles. 2025. Public Opinions
About Copyright for AI-Generated Art: The Role of Egocentricity, Competition,
and Experience. In _Proceedings of the 2025 CHI Conference on Human Factors in_
_Computing Systems_ . 1–32.

[44] Chin-Yew Lin. 2004. ROUGE: A Package for Automatic Evaluation of Summaries.
In _Text Summarization Branches Out_ . Association for Computational Linguistics,
Barcelona, Spain, 74–81. [https://aclanthology.org/W04-1013/](https://aclanthology.org/W04-1013/)

[45] Yvonna S Lincoln. 1985. _Naturalistic inquiry_ . Vol. 75. sage.

[46] Yier Ling and Alex Imas. 2025. Underreporting of AI use: The role of social
desirability bias. _Available at SSRN_ (2025).

[47] Tyler McDonnell, Matthew Lease, Mucahid Kutlu, and Tamer Elsayed. 2016.
Why is that relevant? collecting annotator rationales for relevance judgments. In
_Proceedings of the AAAI Conference on Human Computation and Crowdsourcing_,
Vol. 4. 139–148.

[48] Mark McGurl. 2011. _The_ _program_ _era:_ _Postwar_ _fiction_ _and_ _the_ _rise_ _of_ _creative_
_writing_ . Harvard University Press.

[49] Louis Menand. 2009. Show or Tell. _The New Yorker_ (June 2009). [https://www.](https://www.newyorker.com/magazine/2009/06/08/show-or-tell)
[newyorker.com/magazine/2009/06/08/show-or-tell](https://www.newyorker.com/magazine/2009/06/08/show-or-tell) A Critic at Large; June 8,



2009 issue.

[50] Piotr Mirowski, Juliette Love, Kory Mathewson, and Shakir Mohamed. 2024. A
Robot Walks into a Bar: Can Language Models Serve as Creativity SupportTools
for Comedy? An Evaluation of LLMs’ Humour Alignment with Comedians. In _The_
_2024 ACM Conference on Fairness, Accountability, and Transparency_ . 1622–1636.

[51] Piotr Mirowski, Kory W. Mathewson, Jaylen Pittman, and Richard Evans. 2023.
Co-Writing Screenplays and Theatre Scripts with Language Models: Evaluation
by Industry Professionals. In _Proceedings of the 2023 CHI Conference on Human_
_Factors in Computing Systems_ (Hamburg, Germany) _(CHI ’23)_ . Association for
Computing Machinery, New York, NY, USA, Article 355, 34 pages. [doi:10.1145/](https://doi.org/10.1145/3544548.3581225)
[3544548.3581225](https://doi.org/10.1145/3544548.3581225)

[52] Jacob Noti-Victor. 2025. Regulating Hidden AI Authorship. _Va. L. Rev._ 111 (2025),
139.

[53] Benjamin Nugent. 2020. How to Imitate George Saunders. _The Paris Review_ (6 1
2020). [https://www.theparisreview.org/blog/2020/01/06/how-to-imitate-george-](https://www.theparisreview.org/blog/2020/01/06/how-to-imitate-george-saunders/)
[saunders/](https://www.theparisreview.org/blog/2020/01/06/how-to-imitate-george-saunders/) Accessed: 2025-11-26.

[54] Mary Orr. 2010. Intertextuality. _The encyclopedia of literary and cultural theory_
(2010).

[55] Michael Quinn Patton. 2014. _Qualitative research & evaluation methods: Integrating_
_theory and practice_ . Sage publications.

[56] Julien Porquet, Sitong Wang, and Lydia B Chilton. 2025. Copying style, Extracting
value: Illustrators’ Perception of AI Style Transfer and its Impact on Creative
Labor. In _Proceedings of the 2025 CHI Conference on Human Factors in Computing_
_Systems_ . 1–16.

[57] Jenna Russell, Marzena Karpinska, and Mohit Iyyer. 2025. People who frequently
use ChatGPT for writing tasks are accurate and robust detectors of AI-generated
text. _arXiv preprint arXiv:2501.15654_ (2025).

[58] Pamela Samuelson. 2023. Generative AI meets copyright. _Science_ 381, 6654 (2023),
158–161.

[59] Advait Sarkar. 2025. AI Could Have Written This: Birth of a Classist Slur in
Knowledge Work. In _Proceedings of the Extended Abstracts of the CHI Conference_
_on Human Factors in Computing Systems_ . 1–12.

[60] Richard Jean So and Andrew Piper. 2016. How Has the MFA Changed the
Contemporary Novel? _The Atlantic_ (6 March 2016). [https://www.theatlantic.](https://www.theatlantic.com/entertainment/archive/2016/03/mfa-creative-writing/462483/)
[com/entertainment/archive/2016/03/mfa-creative-writing/462483/](https://www.theatlantic.com/entertainment/archive/2016/03/mfa-creative-writing/462483/)

[61] Benjamin Sobel. 2024. Elements of style: copyright, similarity, and generative AI.
_Harvard Journal of Law & Technology, Forthcoming_ 38 (2024).

[62] Victor Tangermann. 2025. Readers Annoyed When Fantasy Novel Accidentally
Leaves AI Prompt in Published Version, Showing Request to Copy Another
Writer’s Style. _Futurism_ (23 May 2025). [https://futurism.com/fantasy-novel-ai-](https://futurism.com/fantasy-novel-ai-prompt-copy-style)
[prompt-copy-style](https://futurism.com/fantasy-novel-ai-prompt-copy-style) Accessed: 2025-06-21.

[63] Hugo Touvron, Thibaut Lavril, Gautier Izacard, Xavier Martinet, Marie-Anne
Lachaux, Timothée Lacroix, Baptiste Rozière, Naman Goyal, Eric Hambro, Faisal
Azhar, et al. 2023. Llama: Open and efficient foundation language models. _arXiv_
_preprint arXiv:2302.13971_ (2023).

[64] United States District Court for the Northern District of California. 2025. _Order_
_on Fair Use_ . Court Opinion No. C 24-05417 WHA, Doc. 231. United States District
Court, Northern District of California. [https://storage.courtlistener.com/recap/](https://storage.courtlistener.com/recap/gov.uscourts.cand.434709/gov.uscourts.cand.434709.231.0.pdf)
[gov.uscourts.cand.434709/gov.uscourts.cand.434709.231.0.pdf](https://storage.courtlistener.com/recap/gov.uscourts.cand.434709/gov.uscourts.cand.434709.231.0.pdf) Accessed: July 2,
2025.

[65] Tom Vander Ark. 2018. George Saunders On Learning to Write–and Writing to
Learn. _Getting Smart_ (15 2 2018). [https://www.gettingsmart.com/2018/02/15/](https://www.gettingsmart.com/2018/02/15/george-saunders-learning-write-writing-learn/)
[george-saunders-learning-write-writing-learn/](https://www.gettingsmart.com/2018/02/15/george-saunders-learning-write-writing-learn/) Accessed: 2025-11-26.

[66] Vauhini Vara. 2025. _The A.I. Romance Factory_ . Bloomberg Businessweek. [https:](https://www.bloomberg.com/features/2025-ai-romance-factory/)
[//www.bloomberg.com/features/2025-ai-romance-factory/](https://www.bloomberg.com/features/2025-ai-romance-factory/) Feature.

[67] Samangi Wadinambiarachchi, Ryan M Kelly, Saumya Pareek, Qiushi Zhou, and
Eduardo Velloso. 2024. The effects of generative ai on design fixation and divergent thinking. In _Proceedings of the 2024 CHI Conference on Human Factors in_
_Computing Systems_ . 1–18.

[68] Talia Wise, Yuewen Yang, Ryun Shim, Kevin Chuan-Kai Chang, Judeth Oden Choi,
and Qian Yang. 2025. Investigating How Emerging Adults Explore Identity
through Writing: Opportunities for AI Writing Assistants to Help. In _Proceedings_
_of the 2025 ACM Designing Interactive Systems Conference (DIS ’25)_ . Association
for Computing Machinery, New York, NY, USA, 2270–2282. [doi:10.1145/3715336.](https://doi.org/10.1145/3715336.3735848)
[3735848](https://doi.org/10.1145/3715336.3735848)

[69] Xiaojun Xu, Jinghan Jia, Yuanshun Yao, Yang Liu, and Hang Li. 2024. Robust Multibit Text Watermark with LLM-based Paraphrasers. _arXiv preprint arXiv:2412.03123_
(2024).

[70] Ann Yuan, Andy Coenen, Emily Reif, and Daphne Ippolito. 2022. Wordcraft:
story writing with large language models. In _Proceedings of the 27th International_
_Conference on Intelligent User Interfaces_ . 841–852.

[71] Bohan Zhang, Chengke Bu, and Paramveer S Dhillon. 2026. Who Owns the Text?
Design Patterns for Preserving Authorship in AI-Assisted Writing. _arXiv preprint_
_arXiv:2601.10236_ (2026).

[72] Zixin Zhao, Damien Masson, Young-Ho Kim, Gerald Penn, and Fanny Chevalier.
2025. Making the Write Connections: Linking Writing Support Tools with Writer
Needs. In _Proceedings of the 2025 CHI Conference on Human Factors in Computing_
_Systems_ . 1–21.


Can Good Writing Be Generative? Expert-Level AI Writing Emerges through Fine-Tuning on High-Quality Books CHI ’26, April 13–17, 2026, Barcelona, Spain



**A** **Appendix**

**A.1** **Themes for Writing**


We look at each excerpt written by an original author and decode
the main themes in them. Based on our results in Figure 8 it’s
evident that several of them are complex. In particular we see
that the writing tasks encompass themes ranging from intimate
personal struggles (loneliness, grief, routine) to complex societal
examinations (racial identity, post-colonialism, class consciousness)
to philosophical explorations (time, mortality, truth versus fiction),
with most writers tackling the intersection of individual psychology
and broader cultural or historical forces.


**A.2** **Fine-grained Human vs AI performance**


Based on Figure 9 (Top) we can see how Claude 3.5 Sonnet is the
best in terms of performance in In-Context Prompting for Experts



while GPT-4o is best for Lay. GPT-4o in In-Context set up has
12% winning rate. This increases 5X when fine-tuned for Experts.
This shows the power of fine-tuning. For Lay judges there is no
significant difference in GPT-4o performance.


**A.3** **Preference Evaluation Examples**


Figures 10 and 11 show two examples of preference evaluation
from In-Context Prompting and Fine-tuned GPT-4o with detailed
rationales from Experts for Writing Quality. Figure 12 shows one
example of preference evaluation from Fine-tuned GPT-4o with
detailed rationales from Experts for Stylistic Fidelity.


**A.4** **User Interface Design**


Figures 13 and 14 show the user interfaces for the quality evaluation
and stylistic fidelity evaluation tasks respectively.


CHI ’26, April 13–17, 2026, Barcelona, Spain Tuhin Chakrabarty and Paramveer S. Dhillon


**Figure 8: Themes for all the Content provided to Writers and LLM for the task**


Can Good Writing Be Generative? Expert-Level AI Writing Emerges through Fine-Tuning on High-Quality Books CHI ’26, April 13–17, 2026, Barcelona, Spain


**Figure 9: Performance of individual models vs Humans as judged by Expert Judges (Top) Lay Judges (Bottom)**


CHI ’26, April 13–17, 2026, Barcelona, Spain Tuhin Chakrabarty and Paramveer S. Dhillon


**Figure 10: Preference Evaluation from Experts for Roxane Gay and In-Context Prompted Gemini 1.5 Pro where Experts prefer**

**MFA emulation**


Can Good Writing Be Generative? Expert-Level AI Writing Emerges through Fine-Tuning on High-Quality Books CHI ’26, April 13–17, 2026, Barcelona, Spain


**Figure 11: Preference Evaluation from Experts for George Saunders and GPT-4o Fine-tuned where Experts prefer AI emulation**


CHI ’26, April 13–17, 2026, Barcelona, Spain Tuhin Chakrabarty and Paramveer S. Dhillon


**Figure 12: Preference Evaluation from Experts for Junot Diaz and GPT-4o Fine-tuned for Stylistic Fidelity where Experts prefer**

**AI emulation**


Can Good Writing Be Generative? Expert-Level AI Writing Emerges through Fine-Tuning on High-Quality Books CHI ’26, April 13–17, 2026, Barcelona, Spain


**Figure 13:** **Quality Evaluation screen showing two excerpts (AI and Human) emulating Maya Angelou’s style or voice written**

**based on content from her book** _**Letter to My Daughter**_


**Figure 14:** **Stylistic Fidelity evaluation screen showing two excerpts (AI and Human) emulating Ben Lerner’s style or voice**

**written based on content from the original excerpt.**


