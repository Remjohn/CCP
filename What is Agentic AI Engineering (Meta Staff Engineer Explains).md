Well, hello there. So today I want to talk  
about agentic engineering. Now, this is a pretty new  
term that's been popping up all over social media lately. And I know a lot of people  
are going to probably say, isn't this just vibe coding?  
And in my opinion, it's totally different.  
There's a big difference between people just  
prompting ChatGPT or Gemini and one shouting  
some code that they're going to copy paste and saying,  
hey, look, I built something. And when you look at  
the image, it's just pointing to their local host. There's a  
big difference between that and what I do at work  
every single day. And don't get me wrong. I think it's  
amazing that a lot of people are actively trying to  
build things and they're excited about AI coding and  
just doing things. And I think that is great.  
But on the flip side, the term like vibe coding  
being synonymous with. AI coding, in my opinion,  
is essentially a disservice to the entire industry. Basically,  
when everyone who is doing AI coding is getting  
lumped up, all together with vibe coding, I don't think  
that's the right approach. So today we're gonna talk  
about what agentic engineering is and what I  
think are the five pillars that make up this  
new practice. Before we dive in, I wanna give two  
really good examples of this new term,  
agentic engineering. And I think Andre Caparthi  
tweeted about this, saying that what he's doing  
these days is not so much as  
vibe coding, but agentic engineering.  
And he specifically called out the use of the word  
engineering in this, because honestly,  
it is engineering. There's so much thought and  
a lot of designing, system designing, and just a  
ton of work that goes into this new workflow and this  
new practice. And another really good  
example is from Peter Steinberger, who recently joined OpenAI. But I saw a podcast of him  
with Gergay on the Pragmatic Engineer, and he also described that  
his work is agentic engineering. He even goes as far as  
to say, vibe coding is basically a slur now. I think, I think vibe coding is  
by now almost a slur. Oh yeah. I call it, I tell people I do, what I do  
is agentic engineering with a little star. Vibe coding starts at 3 a.m. And honestly, that was so  
relatable to me because I've definitely been there in those  
late nights when I'm no longer following the best  
practices and these pillars that I'm gonna talk about. Now, another interesting  
thing about all of this like agentic engineering stuff  
is that I actually discovered a lot of these pillars on  
my own, just through working with AI  
models every single day. And it kind of started before  
Opus 4.5 came out. But when that model  
came out, something like really shifted in the way I  
started to work because the models just became so  
capable and the tools around the model just had  
this moment where everything  
just clicked. And that's why you see ClockCode and  
CodexApp and all these agentic coding apps are just  
blowing up right now. And it's so interesting to  
me that all of these people that are  
actively building with these things are all kind of  
diverging on these like common topics, common things that  
are turning out to be this thing called  
agentic engineering. Okay, that was a  
long-winded setup, but let's get right into what is agentic engineering.  
Pillar number one is context engineering. And if you've seen any of  
my previous ClockCode videos, I think context engineering  
is king. Context is king. Context is  
best served fresh and condensed. Now, all of these pillars are  
very important, but in my opinion, context is probably the most  
important thing. You know, garbage in, you get  
garbage out, right? Now, a lot of people  
will say, hey, John, just feed it everything.  
We have such large context window these days, does it  
even matter? And in my opinion, even with the  
large context window, I don't think you should be  
trying to optimize for using all of it. Because the way  
these models actually work is that it's basically a  
statistical output, right? It's a statistical chance that  
something will happen, some output will be created  
based on the data that you feed it in. So for  
context engineering, you really need to think  
about what is the exact right amount of context  
that I need to give to the model so that it can do its  
work better. Nothing more, nothing less. And if you look at ClockCode  
and all of the inner workings of it, you know,  
the slash commands, the sub-agents, the skills,  
the MCPs, it's honestly just a tool for  
context engineering that happens to have a  
really good agentic loop and a model that supports it.  
Now, once you buy into this concept, that context  
engineering really matters and what you put into the  
models really matter, the next obvious thing is how do you organize this?  
How do you organize all of this like domain knowledge  
and context about your code and about your projects so  
that the AI can retrieve it efficiently and effectively?  
This is essentially the second brain concept. The second  
brain in a nutshell is how do you store context that isn't  
about the code itself, but about the domain  
around the code, like product,  
product information, product specs, config decisions, domain rules,  
everything that an engineer actually keeps inside of  
their head, where should that live so that the AI can retrieve  
it easily? And there's many ways to do this.  
For ClockCode, for example, you can have a local version  
of your .cloud and you could just put a bunch of things  
in there. I do this for things that may not belong in the  
code base directly. And the other obvious way is  
committing it directly into the code base. Recently,  
OpenAI ran this experiment and wrote about it in this  
article called Harness Engineering. And here they were saying  
that they're pushing more and more things into the  
code base for the AI to have context. Basically, they're optimizing  
the code base for the AI rather than just what we  
deem normally acceptable for humans. So a really interesting insight  
and a rule that they discovered through this  
experiment is that if the domain knowledge doesn't  
exist in the code base, then it doesn't exist for the  
agents at all. So to me, that was really  
interesting because like I said, we have so much that's just  
locked up right here when we work with like just  
other people outside of the code base. You know,  
decisions for meetings, business rules, some new architecture  
choices that we decided. And when the agent doesn't  
inherently just know this, we just complain that the  
agent is not working well. But what if you started  
compacting all of this domain knowledge into markdown files  
or documentation and everything that the  
agent needs, they can retrieve it using some  
rag system. What I've been doing with  
my work is really figuring out like what are the  
key things. I need to put into the code base directly so  
others can use it? And what are the things that I want  
in my workflow locally? So these are the things that  
I'm thinking about. And there's smart ways to  
do this because over time, if you really go deep on this  
second brain concept, you'll realize that you'll have a ton of markdown  
files everywhere. So like indexing things  
properly that points to other markdown files, like all of these things,  
the second brain concept, I think is a whole field of,  
of engineering that is gonna be a big thing. It already  
started with like rag systems, but this is just another layer  
on top of agentic engineering. Now, pillar number two is  
agentic validation. We just discussed that context is king  
and context is the most important, but for agentic validation,  
it's really asking the question, what kind of context  
is good? And in my opinion, a way to self validate an  
agent is gonna be one of the most important things for  
the agent's output to be dramatically better.  
Boris Chen, the creator of Cloud Code, talked about this  
in his workflows when he posted about it sometime  
in January. So if you give an agent a  
way to validate his own work, for example,  
like backend tasks, maybe some integration tests  
or unit tests, for front end, like client work, it might be  
the agent actually just navigates the Chrome  
browser and take screenshots and validates itself, right? And maybe for mobile,  
you can actually use the ADB to simulate interactions.  
Whatever the validation is, in my opinion, this is where  
a lot of creative engineering  
will happen. And Boris mentioned that having this  
validation is a big difference between you're getting  
crappy output versus something that  
actually works and is validated. And like I said, this is where  
a lot of interesting creative engineering is  
gonna happen, this agentic validation loop,  
right? For example, validation in my opinion  
is very, very hard, especially for like UI validation. How do  
you know that this interaction actually works? We don't really have really  
good video models in the loop yet with agent decoding, but how do you do that  
without it? Screenshots are okay, but it's  
not perfect. But you know, you could do things like  
create maybe a domain specific language that knows how to navigate  
your app using like the ADB simulator for mobile,  
for example. Like there's all these things  
that you can think about and do. And there's another  
layer of like logging. What are the observable  
things that the agent can see right now to help  
itself validate? For example, in that article,  
OpenAI started using a log QL to be able to log a bunch of  
files during the validation loop so that the agent can  
carry the logs and validate that, oh, the data is actually correct  
as well, rather than just relying on tests. And these  
are the things that you should be asking yourself for  
your own code base and your own agentic loops. Does the AI have enough  
data from its validation loop? Is the visual  
feedback loop enough? Or is there other mechanisms that  
you haven't thought of that the agent can use  
to self-validate? And I think agentic validation,  
in my opinion, is gonna be a huge part of  
agentic engineering. Now, pillar number three is  
around agentic tooling, and this ties directly into  
agentic validation. But I think it's a large enough  
subject that it should be a thing of its own.  
In this interview, Peter Steinberger talks about  
this topic a lot, and he describes it as friction. What are the things that are blocking the agent?  
What are the friction pieces in the agentic loop that the agent is  
struggling on? And we've seen this develop  
through many different channels already, right?  
ChatGPT and Gemini, they have search,  
agentic search. This is probably a really good  
example of agentic tooling. Deep research, multimodal,  
task systems, all of the things that  
ChatGPT and Gemini is adding into their  
chat interface, that's something you could  
think about as an agentic tool. But you can go a  
layer deeper. If you look at OpenClaw,  
which is a really good example of this, a lot of  
OpenClaw skills, they actually just point to  
CLI tools. And Peter even mentioned  
that every time he ran into something where the agent  
can't do something, he just first reached to build a CLI. And because he had built all  
these CLI tools to do a bunch of these like agentic  
orchestrations before, OpenClaw was able to be  
super successful because it's leveraged all of these things  
to get work done where previously the agent was not  
able to do. So in your own workflow, these are the  
things that you should be actively thinking about and  
actively building and finding ways for the agent  
to handle. You essentially need to get to a point  
where humans are no longer the bottleneck when it  
comes to the agentic execution. Whatever is slowing down  
the agents, recognize that that is a  
huge opportunity right now. And should you create a CLI  
tool or should you like find it or build a specific skill to like  
automate that workflow? Whatever it takes,  
you really need to think about actively pursuing to  
remove that friction from the agent. So the next time  
you run into something when you're coding where you  
have to manually change something or like there is no  
end point, so you have to like go to that website and  
change something. Think about ways so that  
you can build a system or a tool that the agent can use.  
So you don't have to manually ever do that again. Now, pillar number four is  
about agentic code bases. So the question you should  
ask yourself right now is, is your code base optimized  
for AI agents? I would say most  
brownfield projects aren't optimized for agents  
at all. You know, think about your code base. How much of it is dead code  
or bad patterns? How much of competing frameworks is  
in your codebase? Maybe you are partway  
through a migration that never finished and now your  
codebase have two different patterns for doing the  
same thing. We all know that our codebases that we  
work at at work or wherever has these kind  
of things but right now is a moment  
you should be actively cleaning that up.  
Cleaning up your codebase and doing better engineering  
has never been more important than right now  
because every time bad context goes into your  
agentic loop it's basically like the  
poisoning the agent and then you might wonder  
why like hey why is this agent doing this other thing  
that I don't want it to do? Like I said the agents are  
probabilistic in nature right? So if your code has weird  
competing patterns then you need to get rid of it.  
You need to actively get rid of it. So dead code and bad  
patterns is all one thing but in OpenAI's article  
they're even going a step further.  
They're optimizing their file structure so that it's  
always consistent. So that the AI can always generate  
things consistently. They're even adding logging that is like agent specific so  
that the agent can read the logs and things like that.  
And they're creating documentation not just for  
humans but for the agent so that they can keep track of  
the domain knowledge. Essentially they encode what  
they called the golden principles that directly into  
the repo. They're very opinionated about the rules  
and they keep things very consistent for future agents  
to run not future humans. And in my opinion, this is an  
area where we as engineers have to  
really think about what are good principles. You know,  
does dry really matter? Does solid matter? Does not  
commenting your code in a way that like really matter?  
There's all these things that we have, you know, as engineers have  
defined as good but I think a lot of that is  
going to change and a lot of this is still being figured out.  
What does an agentic codebase look like in  
the future? Because you need to remember that  
you're not just writing code. For the next  
engineer anymore. You're writing code for the  
next agent to run. Now pillar number five is  
when all of these things come together and it's called  
compound engineering. Dan Schipper co-founder of  
every talked about this concept. I think he  
essentially coined the term and it's a really powerful  
one if you think about it. Now all of the things that  
I've been talking about context engineering,  
agentic validation, agentic tooling,  
agentic codebase optimizations.  
If you do all these things, if you push everything into  
the codebase so that the agent can like see it and  
share it and then you all engineers working on this are  
bought into these concepts of agentic engineering,  
then you have this new behavior where it  
compounds over time, you know, so the next time  
you optimize some workflow with a new skill and then  
you land it or you develop a new MCP because there's no  
good api's or tools already every time you add those  
things and then you add it into the working library your  
working codebase. Then this compounds and that's  
exactly compound engineering.  
And the reason why I mentioned this as like this  
last point is because all of these things  
that I just talked about you really need to like internalize  
this and then like spread this out because one of the most  
common things that I've seen in my work is that people  
make workflows people do things locally and then  
everyone kind of works slightly different.  
Everyone has different workflows. That's actually a huge thing  
about cloud code. It's very customizable, but I  
think in the future, teams will be more like that  
open AI team who's essentially all agreed all  
bought into this concept and they're compounding the  
work the compounding the knowledge compounding the  
tools that the agent can use and over time making those  
agents be able to just self-validate and keep going  
and essentially have the code build itself. And in my  
opinion like having this mindset this last final piece  
of compound engineering. I think it's a piece that you  
really need to bring back to your teams. So that's it. Those are the  
five pillars. Five pillars of agentic engineering. Now,  
I don't have everything figured out.  
I'm still experimenting still learning by building new  
things every single day every single week, you know,  
some days you'll feel like this where you're building some  
some custom tool for the agent or some custom  
validation for the agent and it's just not working and you  
might have burned hours and hours going in circles  
and going back and forth and might think that hey,  
maybe I should just like written this myself. I think you should really  
challenge yourself to try to avoid that innate  
reaction because you know, I myself love to write code  
and I wrote an interesting article about mourning the  
loss of coding, but this is the future and I  
genuinely think that this is where engineering is going to  
go and the gap between people who are going to  
understand this agentic engineering and the people  
who are just still vibe coding or coding  
by hand. I think it's going to get wider every single month  
month over month as sad as it is to say I do. I truly  
believe the era of coding by hand is dead. It's sad, but it's true. So let me know in  
the comments. I would love to hear what your workflow  
is looking like. If any of this resonates with  
you also sign up for my newsletter push to prod.  
I write once a week or twice a week and there's some  
content that's not here that is there and if you're  
interested in AI coding, I have these videos for you,  
especially this cod code one that's been doing really well. But yeah, I hope you guys enjoy this  
video and until I see you on the next one.  
